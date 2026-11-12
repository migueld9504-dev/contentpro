"""Analiza un comparendo y genera el escrito en PDF listo para radicar.

Uso:
    python defensa.py ejemplos/caso_ejemplo.json
    python defensa.py mi_caso.json --salida peticion.pdf --hoy 2026-11-12
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from analizador import _fecha, analizar, informe
from generar_pdf import generar


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("caso", help="archivo JSON con los datos del caso")
    ap.add_argument("--salida", help="ruta del PDF (por defecto, junto al JSON)")
    ap.add_argument("--hoy", help="fecha del escrito AAAA-MM-DD (por defecto, hoy)")
    args = ap.parse_args()

    caso = json.loads(Path(args.caso).read_text(encoding="utf-8"))
    for campo in ("nombre", "documento"):
        if not caso.get("solicitante", {}).get(campo):
            raise SystemExit(f"Falta solicitante.{campo} en {args.caso}")
    hoy = _fecha(args.hoy) if args.hoy else date.today()
    hallazgos = analizar(caso["comparendo"], hoy)
    salida = args.salida or str(Path(args.caso).with_suffix(".pdf"))
    generar(caso, hallazgos, salida, hoy)
    print(informe(caso, hallazgos))
    print(f"PDF generado: {salida}")


if __name__ == "__main__":
    main()
