# Defensa de comparendos de tránsito (Colombia)

Analiza un comparendo, detecta las causales que sí aplican a ese caso (con fechas
calculadas, no con plantilla) y genera el escrito en PDF listo para radicar.

```bash
pip install reportlab
python defensa.py ejemplos/caso_ejemplo.json
```

Imprime un informe interno (qué tan fuerte es cada argumento y de qué depende) y
crea el PDF junto al JSON. `ejemplos/caso_ejemplo.json` es un caso ficticio que
sirve de molde: copie el archivo y cambie los datos.

## Qué revisa

| Causal | Norma | Cuándo sale como FUERTE |
|---|---|---|
| Prescripción | Art. 159 CNTT (D.L. 019/2012 art. 206) | Más de 3 años desde los hechos sin mandamiento de pago notificado, o más de 3 años desde su notificación |
| Caducidad | Art. 161 CNTT (Ley 1843/2017 art. 11) | Resolución sancionatoria expedida después de 1 año |
| Indebida notificación (fotomulta) | Ley 1843/2017 art. 8; CPACA arts. 67-72; T-051/2016 | Depende de la guía de correo (MEDIA) |
| Envío extemporáneo (fotomulta) | Ley 1843/2017 art. 8; Res. 20203040011245/2020 | Más de 13 días hábiles (calcula festivos colombianos) |
| Conductor no identificado | C-038/2020; límite: Ley 2161/2021 art. 10 y C-321/2022 | El informe avisa cuando el argumento es débil |
| Requisitos del equipo | Ley 1843/2017 arts. 2 y 10; Res. INM 352/2020 | Se exige la prueba: autorización, calibración, señalización |
| Comparendo en vía | Art. 135 CNTT; Res. 3027/2010 | Firma, testigo, copia, competencia del agente |

Fuerza: **FUERTE** (los datos ya configuran la causal), **MEDIA** (indicio serio
que depende de un documento de la autoridad), **POR VERIFICAR** (requisito que la
autoridad debe probar).

## Campos del caso

`fecha_infraccion` es el único dato imprescindible para los cálculos. Los campos
de sí/no aceptan `true`, `false` o `null` (no sé). **Ponga solo lo que sea
cierto**: el escrito afirma esos hechos bajo su firma.

- `tipo`: `fotodeteccion` o `en_via`
- `recibio_notificacion`, `direccion_notificacion_coincide_runt`, `fecha_notificacion`
- `fecha_resolucion`, `numero_resolucion`, `fecha_notificacion_mandamiento`
- `conductor_identificado`, `firmo_comparendo`, `hubo_testigo`, `recibio_copia`
- `errores_datos`: texto libre (p. ej. "la placa anotada es de un automóvil y mi vehículo es una motocicleta")

## De dónde salen los datos

Del estado de cuenta en <https://www.fcm.org.co/simit/> (consulta gratuita por
placa o documento) y de la copia del comparendo. Esta herramienta no consulta
SIMIT de forma automática: el portal protege la consulta con un captcha.

## Límites

Es una ayuda para redactar, no reemplaza a un abogado. Las normas y sentencias
citadas deben revisarse contra el texto oficial antes de radicar, sobre todo el
plazo de validación de 10 días hábiles (tomado de fuentes secundarias sobre la
Resolución 20203040011245 de 2020).
