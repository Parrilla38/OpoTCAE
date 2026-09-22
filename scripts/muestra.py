"""Vuelca por consola muestras de texto de los JSON crudos.

Uso:
    python scripts/muestra.py <doc_id> [n_pagina]
    python scripts/muestra.py --plantillas
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"

PLANTILLAS = [
    "2025_libre_plantilla_prov",
    "2025_libre_plantilla_def",
    "2024_centros_plantilla_prov",
    "2024_centros_plantilla_def",
    "2022_aplazada_plantilla_prov",
    "2021_libre_plantilla_prov",
    "2021_libre_plantilla_def",
    "2019_libre_plantilla_def",
    "2016_libre_plantilla_def",
    "2016_libre_plantilla_corr",
    "2008_plantilla_def",
]


def cargar(doc_id: str) -> dict:
    return json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--plantillas":
        for did in PLANTILLAS:
            d = cargar(did)
            print("=" * 70)
            print(f"{did} | paginas: {d['n_paginas']} | estado: {d['estado']}")
            print("=" * 70)
            for p in d["paginas"]:
                print(f"--- pág {p['n']} ---")
                print((p["texto"] or "")[:1500])
            print()
        return 0

    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    did = sys.argv[1]
    d = cargar(did)
    paginas = d["paginas"]
    if len(sys.argv) >= 3:
        n = int(sys.argv[2])
        paginas = [p for p in paginas if p["n"] == n]
    for p in paginas:
        print(f"===== {did} pág {p['n']} =====")
        print(p["texto"] or "(sin texto)")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
