"""Placa -> consulta de multas -> un PDF por comparendo.

Uso:
    python auto.py VSK24D --perfil perfil.json

Consulta las multas SIMIT de la placa en PlacApi (https://placapi.com, requiere
API key en la variable PLACAPI_KEY), guarda la respuesta cruda y genera un
escrito por cada comparendo encontrado. `perfil.json` contiene el bloque
"solicitante" (ver ejemplos/caso_ejemplo.json).
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path

import requests

from analizador import _fecha, analizar, informe
from generar_pdf import generar

API = "https://placapi.com/api"

# Nombres con los que SIMIT y los proveedores suelen publicar cada dato.
ALIAS = {
    "numero": ["numeroComparendo", "numero_comparendo", "comparendo", "numero", "numeroResolucion"],
    "fecha_infraccion": ["fechaComparendo", "fecha_comparendo", "fechaInfraccion", "fecha"],
    "codigo_infraccion": ["codigoInfraccion", "codigo_infraccion", "infraccion", "codigo"],
    "descripcion": ["descripcionInfraccion", "descripcion_infraccion", "descripcion"],
    "valor": ["valorPagar", "valor_pagar", "valorTotal", "total", "valor"],
    "estado_simit": ["estadoComparendo", "estado_comparendo", "estadoCartera", "estado"],
    "organismo": ["organismoTransito", "organismo_transito", "secretaria", "secretaría", "organismo"],
    "numero_resolucion": ["numeroResolucion", "numero_resolucion", "resolucion"],
    "fecha_resolucion": ["fechaResolucion", "fecha_resolucion"],
    "fecha_notificacion": ["fechaNotificacion", "fecha_notificacion"],
}


def consultar(placa: str) -> dict:
    r = requests.post(
        f"{API}/multas",
        json={"placa": placa},
        headers={"x-api-key": os.environ.get("PLACAPI_KEY", "sin-clave"),
                 "accept": "application/json"},
        timeout=60,
    )
    if r.status_code != 200:
        raise SystemExit(f"PlacApi respondió {r.status_code}: {r.text[:300]}")
    return r.json()


def _registros(obj) -> list[dict]:
    """Busca en cualquier nivel los objetos que parecen un comparendo o multa."""
    out = []
    if isinstance(obj, dict):
        llaves = {k.lower() for k in obj}
        if any("comparendo" in k or "resolucion" in k for k in llaves) and \
                any("fecha" in k for k in llaves):
            out.append(obj)
        else:
            for v in obj.values():
                out += _registros(v)
    elif isinstance(obj, list):
        for v in obj:
            out += _registros(v)
    return out


def _dato(reg: dict, campo: str):
    plano = dict(reg)
    for v in reg.values():  # un nivel de anidación (p. ej. "infracciones": [{...}])
        if isinstance(v, list) and v and isinstance(v[0], dict):
            plano = {**v[0], **plano}
        elif isinstance(v, dict):
            plano = {**v, **plano}
    for a in ALIAS[campo]:
        v = plano.get(a)
        if v not in (None, "", [], {}) and not isinstance(v, (dict, list, bool)):
            return v
    return None


def a_comparendo(reg: dict, placa: str) -> dict:
    c = {k: _dato(reg, k) for k in ALIAS}
    if c["fecha_infraccion"]:
        c["fecha_infraccion"] = str(c["fecha_infraccion"])[:10]
    for k in ("fecha_resolucion", "fecha_notificacion"):
        c[k] = str(c[k])[:10] if c[k] else None
    if c["valor"] is not None:
        v = re.sub(r"[^\d.,]", "", str(c["valor"]))
        if re.fullmatch(r"\d{1,3}([.,]\d{3})+", v):  # separador de miles
            v = re.sub(r"[.,]", "", v)
        c["valor"] = int(float(v.replace(",", ".") or 0))
    texto = json.dumps(reg, ensure_ascii=False).lower()
    c["tipo"] = "fotodeteccion" if re.search(r"foto|electr[oó]nic|sast|c[aá]mara", texto) else "en_via"
    c["placa"] = placa
    return c


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("placa")
    ap.add_argument("--perfil", required=True, help="JSON con el bloque 'solicitante'")
    ap.add_argument("--desde-json", help="usar una respuesta ya guardada en vez de consultar")
    ap.add_argument("--salida", default="casos")
    args = ap.parse_args()

    placa = args.placa.upper().replace(" ", "").replace("-", "")
    perfil = json.loads(Path(args.perfil).read_text(encoding="utf-8"))
    carpeta = Path(args.salida) / placa
    carpeta.mkdir(parents=True, exist_ok=True)

    if args.desde_json:
        cruda = json.loads(Path(args.desde_json).read_text(encoding="utf-8"))
    else:
        cruda = consultar(placa)
        (carpeta / "respuesta.json").write_text(
            json.dumps(cruda, indent=2, ensure_ascii=False), encoding="utf-8")

    regs = _registros(cruda)
    if not regs:
        print(f"La placa {placa} no registra comparendos ni multas en la respuesta.")
        return
    hoy = date.today()
    for reg in regs:
        comp = a_comparendo(reg, placa)
        if not comp["fecha_infraccion"]:
            print(f"Sin fecha de infracción, se omite: {comp['numero']}")
            continue
        _fecha(comp["fecha_infraccion"])
        caso = {"solicitante": perfil.get("solicitante", perfil),
                "autoridad": {"nombre": comp.pop("organismo") or "Organismo de tránsito"},
                "comparendo": comp}
        hallazgos = analizar(comp, hoy)
        base = carpeta / re.sub(r"\W+", "_", str(comp["numero"] or "comparendo"))
        base.with_suffix(".json").write_text(
            json.dumps(caso, indent=2, ensure_ascii=False), encoding="utf-8")
        generar(caso, hallazgos, str(base.with_suffix(".pdf")), hoy)
        print(informe(caso, hallazgos))
        print(f"PDF generado: {base.with_suffix('.pdf')}\n")


if __name__ == "__main__":
    main()
