"""Arma el escrito (derecho de petición y solicitudes de fondo) en PDF."""
from __future__ import annotations

from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer

from analizador import FUERTE, MEDIA, Hallazgo, fmt

BASE = ParagraphStyle("base", fontName="Helvetica", fontSize=10.5, leading=14.5,
                      alignment=TA_JUSTIFY, spaceAfter=7)
IZQ = ParagraphStyle("izq", parent=BASE, alignment=0, spaceAfter=2)
TIT = ParagraphStyle("tit", parent=BASE, fontName="Helvetica-Bold", fontSize=11,
                     alignment=0, spaceBefore=10, spaceAfter=6)
SUB = ParagraphStyle("sub", parent=BASE, fontName="Helvetica-Bold", alignment=0, spaceAfter=3)
ITEM = ParagraphStyle("item", parent=BASE, leftIndent=18, firstLineIndent=-18)
SUBITEM = ParagraphStyle("subitem", parent=BASE, leftIndent=36, firstLineIndent=-14, spaceAfter=4)


def _p(texto: str, estilo=BASE) -> Paragraph:
    return Paragraph(escape(texto), estilo)


def _pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillGray(0.4)
    canvas.drawRightString(LETTER[0] - 2.5 * cm, 1.4 * cm, f"Página {doc.page}")
    canvas.restoreState()


def generar(caso: dict, hallazgos: list[Hallazgo], salida: str, hoy: date | None = None) -> str:
    hoy = hoy or date.today()
    s, c = caso["solicitante"], caso["comparendo"]
    a = caso.get("autoridad", {})
    num = c.get("numero") or "(sin número)"
    de_fondo = [x for x in hallazgos if x.fuerza in (FUERTE, MEDIA)]
    calidad = s.get("calidad", "propietario")
    doc_id = f"{s.get('tipo_documento', 'C.C.')} No. {s['documento']}"

    f: list = []
    f.append(_p(f"{s.get('ciudad', a.get('ciudad', ''))}, {fmt(hoy)}", IZQ))
    f.append(Spacer(1, 10))
    f.append(_p("Señores", IZQ))
    f.append(Paragraph(f"<b>{escape(a.get('nombre', 'ORGANISMO DE TRÁNSITO').upper())}</b>", IZQ))
    if a.get("ciudad"):
        f.append(_p(a["ciudad"], IZQ))
    f.append(Spacer(1, 10))

    asunto = "Derecho de petición (artículo 23 de la Constitución y Ley 1755 de 2015)"
    if de_fondo:
        asunto += " con solicitud de " + _nombre_solicitud(de_fondo)
    f.append(Paragraph(f"<b>Asunto:</b> {escape(asunto)}.", BASE))
    ref = f"Orden de comparendo No. {num}"
    if c.get("fecha_infraccion"):
        from analizador import _fecha
        ref += f" del {fmt(_fecha(c['fecha_infraccion']))}"
    ref += f". Vehículo de placa {c.get('placa', '')}."
    if c.get("numero_resolucion"):
        ref += f" Resolución No. {c['numero_resolucion']}."
    f.append(Paragraph(f"<b>Referencia:</b> {escape(ref)}", BASE))

    f.append(_p(
        f"{s['nombre'].upper()}, mayor de edad, identificado(a) con {doc_id}, en calidad de "
        f"{calidad} del vehículo de placa {c.get('placa', '')}, en ejercicio del derecho "
        "fundamental de petición, presento ante ustedes las siguientes solicitudes, con "
        "fundamento en los hechos y razones que expongo a continuación."))

    # ---- Hechos ----
    f.append(_p("I. HECHOS", TIT))
    hechos = []
    desc = f" por la presunta infracción {c['codigo_infraccion']}" if c.get("codigo_infraccion") else ""
    if c.get("descripcion"):
        desc += f" ({c['descripcion'].rstrip('.')})"
    hechos.append(
        f"En el Sistema Integrado de Información sobre Multas y Sanciones por Infracciones "
        f"de Tránsito (SIMIT) figura a mi nombre la orden de comparendo No. {num}{desc}, "
        f"asociada al vehículo de placa {c.get('placa', '')}"
        + (", por valor de $" + f"{int(c['valor']):,}".replace(",", ".") if c.get("valor") else "")
        + (f", en estado «{c['estado_simit']}»" if c.get("estado_simit") else "") + ".")
    if (c.get("tipo") or "").lower().startswith("foto"):
        hechos.append("Según el registro, el comparendo fue impuesto mediante un sistema "
                      "automático o semiautomático de detección de infracciones (fotodetección).")
    hechos += [x.hechos for x in hallazgos]
    for i, t in enumerate(hechos, 1):
        f.append(_p(f"{i}.  {t}", ITEM))

    # ---- Peticiones ----
    f.append(_p("II. PETICIONES", TIT))
    n = 0
    if de_fondo:
        f.append(_p("Peticiones de fondo", SUB))
        for x in de_fondo:
            n += 1
            f.append(_p(f"{n}.  {x.peticion}", ITEM))
    f.append(_p("Peticiones de información y documentos" if de_fondo
                else "Peticiones de información y documentos (artículo 14, numeral 1, de la Ley 1755 de 2015)", SUB))
    n += 1
    f.append(_p(f"{n}.  Expedir a mi costa copia íntegra y legible del expediente "
                f"contravencional y de cobro coactivo correspondiente al comparendo No. {num}, "
                "y en particular de los siguientes documentos, indicando expresamente cuáles "
                "de ellos no existen o no reposan en el expediente:", ITEM))
    pruebas: list[str] = []
    for x in hallazgos:
        for p in x.pruebas:
            if p not in pruebas:
                pruebas.append(p)
    for i, p in enumerate(pruebas):
        f.append(_p(f"{chr(97 + i)})  {p}", SUBITEM))
    n += 1
    f.append(_p(f"{n}.  Informar el estado actual del proceso, la etapa en que se encuentra "
                "y el nombre y cargo del funcionario responsable.", ITEM))
    n += 1
    f.append(_p(
        f"{n}.  Resolver de fondo, de manera clara, precisa y congruente CADA UNO de los "
        "numerales anteriores, pronunciándose sobre los hechos y fechas concretos aquí "
        "expuestos. Una respuesta en formato genérico, que no se refiera a lo pedido o que "
        "se limite a transcribir normas, no satisface el núcleo esencial del derecho de "
        "petición (Corte Constitucional, Sentencias T-377 de 2000 y T-206 de 2018) y dará "
        "lugar a la acción de tutela y a la queja disciplinaria prevista en el artículo 31 "
        "de la Ley 1755 de 2015.", ITEM))

    # ---- Fundamentos ----
    f.append(_p("III. FUNDAMENTOS DE DERECHO", TIT))
    for i, x in enumerate(hallazgos, 1):
        f.append(KeepTogether([_p(f"{i}. {x.titulo}", SUB), _p(x.fundamento)]))
    f.append(KeepTogether([
        _p(f"{len(hallazgos) + 1}. Derecho de petición y acceso al expediente", SUB),
        _p("Artículos 23, 29 y 74 de la Constitución Política; artículos 13, 14 y 31 de la "
           "Ley 1437 de 2011, sustituidos por la Ley 1755 de 2015 (término de quince días "
           "hábiles para resolver peticiones y de diez días hábiles para entregar "
           "documentos; vencido este último sin respuesta, la solicitud de copias se "
           "entiende aceptada y deben entregarse dentro de los tres días siguientes); "
           "artículo 36 de la Ley 1437 de 2011 (derecho a examinar el expediente y obtener "
           "copias).")]))

    # ---- Anexos y notificaciones ----
    f.append(_p("IV. ANEXOS", TIT))
    anexos = ["Copia de mi documento de identidad.",
              "Copia de la licencia de tránsito (tarjeta de propiedad) del vehículo.",
              "Pantallazo de la consulta del estado de cuenta en el SIMIT."]
    anexos += caso.get("anexos", [])
    for i, t in enumerate(anexos, 1):
        f.append(_p(f"{i}.  {t}", ITEM))

    f.append(_p("V. NOTIFICACIONES", TIT))
    partes = []
    if s.get("email"):
        partes.append(f"al correo electrónico {s['email']}, medio por el cual autorizo "
                      "expresamente ser notificado (artículo 56 de la Ley 1437 de 2011)")
    if s.get("direccion"):
        partes.append(f"en la dirección {s['direccion']}, {s.get('ciudad', '')}".rstrip(", "))
    f.append(_p(("Recibo notificaciones " + " y ".join(partes)
                + (f". Teléfono: {s['telefono']}" if s.get("telefono") else "") + ".").replace("..", ".")))

    f.append(Spacer(1, 6))
    f.append(KeepTogether([
        _p("Atentamente,", IZQ), Spacer(1, 38),
        _p("______________________________________", IZQ),
        Paragraph(f"<b>{escape(s['nombre'].upper())}</b>", IZQ),
        _p(doc_id, IZQ)]))

    SimpleDocTemplate(
        salida, pagesize=LETTER, leftMargin=2.8 * cm, rightMargin=2.5 * cm,
        topMargin=2.5 * cm, bottomMargin=2.3 * cm,
        title=f"Derecho de petición - comparendo {num}", author=s["nombre"],
    ).build(f, onFirstPage=_pie, onLaterPages=_pie)
    return salida


def _nombre_solicitud(hs: list[Hallazgo]) -> str:
    ids = [x.id for x in hs]
    nombres = []
    if "prescripcion" in ids:
        nombres.append("prescripción")
    if "caducidad" in ids:
        nombres.append("caducidad")
    if any(i not in ("prescripcion", "caducidad") for i in ids):
        nombres.append("revocatoria directa")
    return ", ".join(nombres[:-1]) + (" y " if len(nombres) > 1 else "") + nombres[-1]
