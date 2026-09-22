"""Inspecciona preguntas parseadas de data/parsed/preguntas.json.

Uso:
    python scripts/inspecciona.py <exam_id> [n]
    python scripts/inspecciona.py --muestra          # 2 por formato detectado
    python scripts/inspecciona.py --raras            # enunciados cortos u opciones vacías
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "parsed" / "preguntas.json"


def cargar() -> list[dict]:
    return json.loads(SALIDA.read_text(encoding="utf-8"))


def mostrar(p: dict) -> None:
    print(f"--- {p['id']}  n={p['numero']}  formato={p['formato']}  "
          f"orden={p['orden_opciones']}  correcta={p['correcta']}  "
          f"anulada={p['anulada']}  parte={p.get('parte')}")
    print(f"    ENUN: {p['enunciado'][:180]}")
    for k in ("A", "B", "C", "D"):
        print(f"    {k}) {p['opciones'].get(k, '')[:120]}")


def main() -> int:
    preguntas = cargar()
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    arg = sys.argv[1]
    if arg == "--muestra":
        por_formato: dict[str, list[dict]] = {}
        for p in preguntas:
            por_formato.setdefault(p["formato"] + "/" + p["orden_opciones"], []).append(p)
        for clave, grupo in sorted(por_formato.items()):
            print(f"===== formato {clave}  ({len(grupo)} preguntas) =====")
            for p in grupo[:2]:
                mostrar(p)
            print()
        return 0

    if arg == "--raras":
        raras = [
            p for p in preguntas
            if len(p["enunciado"]) < 25
            or any(len(p["opciones"].get(k, "")) < 2 for k in "ABCD")
            or p.get("numero_inferido")
        ]
        print(f"preguntas raras: {len(raras)} de {len(preguntas)}")
        for p in raras[:25]:
            mostrar(p)
        return 0

    exam_id = arg
    seleccion = [p for p in preguntas if p["exam_id"] == exam_id]
    if len(sys.argv) >= 3:
        n = int(sys.argv[2])
        seleccion = [p for p in seleccion if p["numero"] == n]
    print(f"{len(seleccion)} preguntas")
    for p in seleccion[:20]:
        mostrar(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
