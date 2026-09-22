"""Busca el corte entre secciones (libre / PI) dentro de un cuadernillo.

Uso: python scripts/busca_corte.py <doc_id>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"

CLAVES = [
    "PREGUNTAS", "ACCESO LIBRE", "PROMOCION", "PROMOCIÓN", "INTERNA",
    "TURNO", "LIBRE", "CUESTIONARIO", "PRÁCTIC", "PRACTIC", "SUPUESTO",
    "RESERVA", "TEÓRICO", "TEORICO", "OEP", "APLAZAD", "ESTABILIZ",
]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    did = sys.argv[1]
    datos = json.loads((RAW / f"{did}.json").read_text(encoding="utf-8"))
    for p in datos["paginas"]:
        for i, linea in enumerate((p["texto"] or "").split("\n")):
            s = linea.strip()
            if not s:
                continue
            up = s.upper()
            if any(k in up for k in CLAVES):
                print(f"p{p['n']:>3}:{i:<3} | {s[:100]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
