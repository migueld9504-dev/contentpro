"""Motor de análisis jurídico de comparendos de tránsito (Colombia).

Recibe los datos de un comparendo y devuelve una lista de hallazgos. Cada
hallazgo dice qué tan fuerte es, en qué hechos concretos se apoya, la norma
que lo respalda, lo que se le pide a la autoridad y las pruebas que hay que
exigir para confirmarlo.

Fuerza de un hallazgo:
  FUERTE        las fechas o hechos aportados ya configuran la causal.
  MEDIA         hay un indicio serio, pero depende de un documento que tiene la autoridad.
  POR VERIFICAR requisito legal que la autoridad debe demostrar; se le exige la prueba.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from festivos import dias_habiles_entre, sumar_anios

FUERTE, MEDIA, VERIFICAR = "FUERTE", "MEDIA", "POR VERIFICAR"

# Infracciones por las que el propietario responde por deber propio
# (art. 10 de la Ley 2161 de 2021, declarado exequible en la Sentencia C-321 de 2022).
LEY_2161 = date(2021, 11, 26)
CODIGOS_DEBER_PROPIETARIO = {"C29", "D04", "D02", "C35", "C14"}


@dataclass
class Hallazgo:
    id: str
    titulo: str
    fuerza: str
    hechos: str
    fundamento: str
    peticion: str
    pruebas: list[str] = field(default_factory=list)
    advertencia: str = ""


def _fecha(v) -> date | None:
    if not v:
        return None
    if isinstance(v, date):
        return v
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(str(v).strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Fecha no reconocida: {v!r} (use AAAA-MM-DD)")


def fmt(d: date) -> str:
    meses = ("enero febrero marzo abril mayo junio julio agosto septiembre "
             "octubre noviembre diciembre").split()
    return f"{d.day} de {meses[d.month - 1]} de {d.year}"


def analizar(comp: dict, hoy: date | None = None) -> list[Hallazgo]:
    hoy = hoy or date.today()
    h: list[Hallazgo] = []
    num = comp.get("numero") or "(sin número)"
    fi = _fecha(comp.get("fecha_infraccion"))
    fn = _fecha(comp.get("fecha_notificacion"))
    fr = _fecha(comp.get("fecha_resolucion"))
    fmp = _fecha(comp.get("fecha_notificacion_mandamiento"))
    foto = (comp.get("tipo") or "").lower().startswith("foto")
    codigo = (comp.get("codigo_infraccion") or "").upper().replace(".", "").replace(" ", "")

    # ---------- 1. Prescripción de la sanción (art. 159 CNTT) ----------
    if fi:
        limite = sumar_anios(fi, 3)
        base = ("Artículo 159 de la Ley 769 de 2002, modificado por el artículo 206 del "
                "Decreto Ley 019 de 2012: la ejecución de las sanciones por infracciones de "
                "tránsito prescribe en tres (3) años contados a partir de la ocurrencia del "
                "hecho, y la prescripción solo se interrumpe con la notificación del "
                "mandamiento de pago. La misma norma ordena a la autoridad declararla de "
                "oficio.")
        pet = (f"DECLARAR la prescripción de la sanción derivada del comparendo No. {num} "
               "y, en consecuencia, ordenar la terminación y archivo del proceso de cobro, "
               "el levantamiento de las medidas cautelares si las hubiere, y la "
               "actualización del reporte en el SIMIT y en el RUNT.")
        prueba = ("Copia del mandamiento de pago y de la constancia de su notificación "
                  "(guía de correo certificado, acta de notificación personal o aviso), "
                  "con la fecha en que se surtió.")
        if fmp and fmp > limite:
            h.append(Hallazgo(
                "prescripcion", "Prescripción: el mandamiento de pago se notificó por fuera de los tres años",
                FUERTE,
                f"Los hechos ocurrieron el {fmt(fi)}. El término de tres años venció el "
                f"{fmt(limite)} y el mandamiento de pago solo se notificó el {fmt(fmp)}, "
                "cuando la prescripción ya había operado y no había nada que interrumpir.",
                base, pet, [prueba]))
        elif fmp and hoy > sumar_anios(fmp, 3):
            h.append(Hallazgo(
                "prescripcion", "Prescripción: más de tres años desde la notificación del mandamiento de pago",
                FUERTE,
                f"El mandamiento de pago se notificó el {fmt(fmp)}. Interrumpida la "
                f"prescripción, el término comenzó a correr de nuevo y venció el "
                f"{fmt(sumar_anios(fmp, 3))} sin que se haya hecho efectivo el cobro.",
                base + " Interrumpido el término, este corre de nuevo por el mismo lapso "
                "(artículo 818 del Estatuto Tributario, aplicable al cobro coactivo por "
                "remisión del artículo 5 de la Ley 1066 de 2006).",
                pet, [prueba],
                "Algunas secretarías sostienen que tras el mandamiento de pago corren 5 años "
                "(art. 817 E.T.) y no 3. Si responden eso, el argumento es que la norma "
                "especial de tránsito (art. 159) fija 3 años y prevalece sobre la general."))
        elif not fmp and hoy > limite:
            h.append(Hallazgo(
                "prescripcion", "Prescripción: más de tres años desde los hechos",
                FUERTE,
                f"Los hechos ocurrieron el {fmt(fi)}; el término de tres años venció el "
                f"{fmt(limite)}. Al suscrito no le ha sido notificado mandamiento de pago "
                "alguno dentro de ese término.",
                base, pet, [prueba],
                "Depende de que la autoridad no pueda probar que notificó en debida forma "
                "un mandamiento de pago antes del " + fmt(limite) + "."))

    # ---------- 2. Caducidad de la acción contravencional (art. 161 CNTT) ----------
    if fi:
        limite = sumar_anios(fi, 1)
        base = ("Artículo 161 de la Ley 769 de 2002, modificado por el artículo 11 de la "
                "Ley 1843 de 2017: la acción por contravención de las normas de tránsito "
                "caduca al año (1) contado a partir de la ocurrencia de los hechos; dentro "
                "de ese término debe decidirse sobre la imposición de la sanción.")
        pet = (f"DECLARAR la caducidad de la acción contravencional respecto del comparendo "
               f"No. {num}, archivar la actuación y retirar el registro del SIMIT.")
        prueba = ("Copia íntegra de la resolución sancionatoria, con su fecha de expedición, "
                  "constancia de notificación y constancia de ejecutoria.")
        if fr and fr > limite:
            h.append(Hallazgo(
                "caducidad", "Caducidad: la sanción se impuso después de un año",
                FUERTE,
                f"Los hechos ocurrieron el {fmt(fi)} y la resolución sancionatoria es del "
                f"{fmt(fr)}, es decir, posterior al {fmt(limite)}, fecha en que caducó la "
                "facultad sancionatoria.",
                base, pet, [prueba]))
        elif not fr and hoy > limite:
            h.append(Hallazgo(
                "caducidad", "Caducidad: más de un año sin resolución sancionatoria conocida",
                MEDIA,
                f"Los hechos ocurrieron el {fmt(fi)}. Ha transcurrido más de un año "
                f"(venció el {fmt(limite)}) y al suscrito no le ha sido notificada "
                "resolución sancionatoria alguna.",
                base, pet, [prueba],
                "Si la autoridad expidió resolución dentro del año, la caducidad no opera; "
                "por eso se exige la copia con fecha y constancia de notificación."))

    # ---------- 3. Fotodetección ----------
    if foto:
        if comp.get("recibio_notificacion") is False:
            h.append(Hallazgo(
                "notificacion", "Indebida notificación del comparendo electrónico",
                MEDIA,
                "El suscrito nunca recibió la orden de comparendo ni sus soportes en la "
                "dirección registrada en el RUNT; se enteró de su existencia al consultar "
                "el SIMIT." + (
                    " La dirección a la que se dice haber enviado no corresponde a la "
                    "registrada en el RUNT."
                    if comp.get("direccion_notificacion_coincide_runt") is False else ""),
                "Artículo 8 de la Ley 1843 de 2017 (envío del comparendo y sus soportes al "
                "propietario dentro de los tres días hábiles siguientes a la validación, a "
                "la dirección registrada en el RUNT); artículos 67 a 69 y 72 de la Ley 1437 "
                "de 2011 (sin notificación en debida forma la decisión no produce efectos); "
                "artículo 29 de la Constitución; Sentencias C-980 de 2010 y T-051 de 2016 de "
                "la Corte Constitucional.",
                f"REVOCAR DIRECTAMENTE (artículo 93, numeral 1, de la Ley 1437 de 2011) la "
                f"resolución sancionatoria derivada del comparendo No. {num} por violación "
                "del debido proceso, y rehacer la actuación desde la notificación, "
                "garantizando el derecho de defensa y los descuentos de ley.",
                ["Guía de la empresa de correo con la que se envió el comparendo, con "
                 "dirección de destino, fecha de envío y resultado de la entrega "
                 "(nombre y firma de quien recibió o causal de devolución).",
                 "Si hubo notificación por aviso: copia del aviso, constancia de su "
                 "publicación y fechas de fijación y desfijación.",
                 "Certificación de la dirección registrada en el RUNT para la fecha de "
                 "los hechos."],
                "Si la guía muestra entrega efectiva en su dirección RUNT, este argumento "
                "cae. Verifique qué dirección tenía registrada en el RUNT en esa fecha."))
        if fi and fn:
            dh = dias_habiles_entre(fi, fn)
            if dh > 13:
                h.append(Hallazgo(
                    "plazo_envio", "Envío extemporáneo del comparendo electrónico",
                    MEDIA,
                    f"Entre la fecha de los hechos ({fmt(fi)}) y la fecha en que se "
                    f"recibió el comparendo ({fmt(fn)}) transcurrieron {dh} días hábiles.",
                    "Artículo 8 de la Ley 1843 de 2017: el comparendo y sus soportes deben "
                    "enviarse dentro de los tres (3) días hábiles siguientes a su validación; "
                    "la validación por el agente de tránsito debe hacerse dentro de los diez "
                    "(10) días hábiles siguientes a la infracción (Resolución 20203040011245 "
                    "de 2020 del Ministerio de Transporte y la ANSV). Artículo 29 de la "
                    "Constitución.",
                    f"DECLARAR que el comparendo No. {num} fue validado y/o enviado por "
                    "fuera de los términos legales y, en consecuencia, revocar la actuación "
                    "adelantada con base en él.",
                    ["Constancia de la fecha y hora de validación del comparendo, con "
                     "nombre y placa del agente de tránsito que la realizó.",
                     "Guía de correo con la fecha de entrega a la empresa de mensajería."],
                    "Lo que la ley mide es la fecha de ENVÍO, no la de recibo. Hay que ver "
                    "la guía: si el envío se hizo dentro de los 13 días hábiles, no prospera."))
        if comp.get("conductor_identificado") is not True:
            deber = codigo in CODIGOS_DEBER_PROPIETARIO and fi and fi >= LEY_2161
            h.append(Hallazgo(
                "conductor", "Falta de identificación del conductor infractor",
                VERIFICAR if deber else MEDIA,
                "La evidencia del sistema de fotodetección registra la placa del vehículo, "
                "pero no identifica a la persona que lo conducía. La sanción se dirige "
                "contra el suscrito únicamente por figurar como propietario.",
                "Sentencia C-038 de 2020 de la Corte Constitucional, que declaró inexequible "
                "el parágrafo 1 del artículo 8 de la Ley 1843 de 2017 (responsabilidad "
                "solidaria del propietario): la responsabilidad en materia sancionatoria es "
                "personal, y corresponde al Estado probar quién cometió la infracción. "
                "Artículo 29 de la Constitución (presunción de inocencia); artículo 129 de la "
                "Ley 769 de 2002.",
                f"Indicar con qué prueba se identificó a la persona que conducía el vehículo "
                f"en la fecha del comparendo No. {num} y, de no existir, revocar la sanción "
                "impuesta al suscrito por ausencia de prueba de la autoría.",
                ["Registro fotográfico o de video completo y sin editar de la presunta "
                 "infracción.",
                 "Prueba con la que se estableció la identidad del conductor."],
                ("Para esta infracción y esta fecha el argumento es débil: desde la Ley 2161 "
                 "de 2021 (art. 10, avalado en la Sentencia C-321 de 2022) el propietario "
                 "responde por deber propio en exceso de velocidad, semáforo en rojo, SOAT, "
                 "tecnomecánica y circulación en lugares u horarios prohibidos. Se pide la "
                 "prueba, pero no es el argumento principal.") if deber else
                "Las secretarías suelen contestar con la Ley 2161 de 2021; esa ley solo "
                "cubre ciertas infracciones y hechos posteriores al 26 de noviembre de 2021."))
        h.append(Hallazgo(
            "requisitos_sast", "Requisitos técnicos y legales del sistema de fotodetección",
            VERIFICAR,
            "La autoridad no ha acreditado que el equipo con el que se captó la presunta "
            "infracción cumpliera, en la fecha de los hechos, los requisitos legales de "
            "operación.",
            "Artículos 2 y 10 de la Ley 1843 de 2017 (autorización previa de cada sistema y "
            "señalización visible que advierta la zona vigilada, ubicada 500 metros antes); "
            "Resolución 20203040011245 de 2020 (criterios técnicos de instalación y "
            "operación); Resolución 352 de 2020 del Instituto Nacional de Metrología "
            "(trazabilidad metrológica de los medidores de velocidad); parágrafo 2 del "
            "artículo 129 de la Ley 769 de 2002.",
            "Entregar copia de los documentos que acreditan el cumplimiento de estos "
            "requisitos y, si alguno no existía en la fecha de los hechos, revocar la "
            f"actuación derivada del comparendo No. {num} por haberse obtenido la prueba "
            "con violación del debido proceso (artículo 29 de la Constitución).",
            ["Acto de autorización del sistema o equipo de fotodetección para el punto "
             "exacto de la presunta infracción, vigente en la fecha de los hechos.",
             "Certificado de calibración o verificación metrológica del equipo vigente en "
             "la fecha de los hechos, con número de serie.",
             "Registro fotográfico y ubicación georreferenciada de la señalización "
             "preventiva instalada antes de la zona vigilada.",
             "Nombre, placa y acto de nombramiento del agente de tránsito que validó el "
             "comparendo."]))
    else:
        # ---------- 4. Comparendo impuesto en vía ----------
        if comp.get("firmo_comparendo") is False and comp.get("hubo_testigo") is not True:
            h.append(Hallazgo(
                "firma", "Comparendo sin firma del conductor ni de testigo",
                MEDIA,
                "La orden de comparendo no fue firmada por el suscrito ni por testigo alguno.",
                "Artículo 135 de la Ley 769 de 2002, modificado por el artículo 22 de la Ley "
                "1383 de 2010: la orden de comparendo debe ser firmada por el conductor y, "
                "si este se niega, debe firmar por él un testigo.",
                f"Entregar copia legible del comparendo No. {num} y, de verificarse la "
                "ausencia de firma del conductor y de testigo, excluirlo como prueba y "
                "revocar la sanción.",
                ["Copia legible, por ambas caras, de la orden de comparendo original."]))
        if comp.get("recibio_copia") is False:
            h.append(Hallazgo(
                "copia", "No se entregó copia del comparendo al conductor",
                MEDIA,
                "El agente no entregó al suscrito copia de la orden de comparendo, por lo "
                "que no conoció el término para comparecer ni la infracción imputada.",
                "Artículo 135 de la Ley 769 de 2002 (el agente debe entregar copia de la "
                "orden de comparendo al conductor); artículo 29 de la Constitución.",
                f"Revocar la actuación derivada del comparendo No. {num} por violación del "
                "derecho de defensa.",
                ["Copia de la orden de comparendo con la constancia de entrega."]))
        h.append(Hallazgo(
            "requisitos_via", "Legalidad del procedimiento en vía",
            VERIFICAR,
            "La autoridad no ha acreditado la competencia del agente ni el cumplimiento "
            "del procedimiento del artículo 135 del Código Nacional de Tránsito.",
            "Artículos 3, 7 y 135 de la Ley 769 de 2002 (autoridades de tránsito, "
            "competencia territorial, entrega del comparendo al organismo de tránsito "
            "dentro de las doce horas siguientes); Resolución 3027 de 2010 del Ministerio "
            "de Transporte (formulario único de comparendo).",
            f"Entregar los documentos que acreditan la legalidad del procedimiento y, de "
            f"no existir, revocar la actuación derivada del comparendo No. {num}.",
            ["Nombre, placa y acto de nombramiento o convenio que acredita la calidad y "
             "la jurisdicción del agente que impuso el comparendo.",
             "Constancia de la fecha y hora en que el agente entregó el comparendo al "
             "organismo de tránsito.",
             "Si se uso alcohosensor, radar u otro equipo: certificado de calibración "
             "vigente en la fecha de los hechos y certificado de idoneidad del operador.",
             "Pruebas que obran en el expediente (videos, fotografías, informe del agente)."]))

    # ---------- 5. Errores en los datos del comparendo ----------
    if comp.get("errores_datos"):
        h.append(Hallazgo(
            "errores", "Inconsistencias en los datos del comparendo",
            MEDIA,
            "La orden de comparendo contiene las siguientes inconsistencias: "
            + str(comp["errores_datos"]).rstrip(".") + ".",
            "Artículo 135 de la Ley 769 de 2002 y Resolución 3027 de 2010 (contenido "
            "obligatorio de la orden de comparendo); artículo 29 de la Constitución: la "
            "imputación debe ser clara, precisa y corresponder a los hechos.",
            f"Verificar las inconsistencias señaladas y revocar la actuación derivada del "
            f"comparendo No. {num} por indebida individualización de la conducta, del "
            "vehículo o del presunto infractor.",
            ["Copia legible de la orden de comparendo original."]))

    orden = {FUERTE: 0, MEDIA: 1, VERIFICAR: 2}
    return sorted(h, key=lambda x: orden[x.fuerza])


def informe(caso: dict, hallazgos: list[Hallazgo]) -> str:
    """Informe interno para el usuario (no se envía a la autoridad)."""
    c = caso["comparendo"]
    out = [f"ANÁLISIS DEL COMPARENDO {c.get('numero', '')} - PLACA {c.get('placa', '')}", ""]
    if not any(x.fuerza == FUERTE for x in hallazgos):
        out += ["No hay una causal que ya esté probada solo con las fechas. El escrito "
                "exige el expediente; con la respuesta se define el siguiente paso.", ""]
    for x in hallazgos:
        out.append(f"[{x.fuerza}] {x.titulo}")
        out.append(f"    {x.hechos}")
        if x.advertencia:
            out.append(f"    OJO: {x.advertencia}")
        out.append("")
    return "\n".join(out)
