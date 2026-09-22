"""Cuenta menciones literales de 'Constitución' y de artículos por cuadernillo.

Métrica transparente de apoyo al informe FASE0_INVENTARIO.md. Complementa a
estima_ce.py (que es inclusivo y por temas): aquí solo se cuenta lo literal.

Uso: python scripts/menciones.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import DOCUMENTOS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"

RE_CONSTITUCION = re.compile(r"constituci[oó]n", re.IGNORECASE)
RE_ART = re.compile(r"art(?:[íi]cul?)?o?\s*n[úu]m\.?\s*\d+|art(?:[íi]cul?)?o?\s*\.?\s*\d+", re.IGNORECASE)
RE_ART_NUM = re.compile(r"art(?:[íi]cul?)?o?\s*\.?\s*(\d{1,3})", re.IGNORECASE)


def cargar_texto(doc_id: str) -> str:
    datos = json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))
    return "\n".join(p["texto"] for p in datos.get("paginas", []))


def main() -> int:
    filas = []
    total_c = total_a = 0
    for d in DOCUMENTOS:
        if d["tipo"] != "cuadernillo":
            continue
        texto = cargar_texto(d["id"])
        n_c = len(RE_CONSTITUCION.findall(texto))
        n_a = len(RE_ART.findall(texto))
        arts = sorted({int(n) for n in RE_ART_NUM.findall(texto) if 1 <= int(n) <= 169})
        filas.append((d["id"], n_c, n_a, arts))
        total_c += n_c
        total_a += n_a

    ancho = max(len(f[0]) for f in filas)
    print(f"{'id':<{ancho}}  {'Constitución':>12}  {'art. NN':>8}  artículos citados")
    print("-" * (ancho + 60))
    for did, n_c, n_a, arts in filas:
        arts_s = ",".join(str(a) for a in arts[:14])
        if len(arts) > 14:
            arts_s += ",..."
        print(f"{did:<{ancho}}  {n_c:>12}  {n_a:>8}  {arts_s}")
    print("-" * (ancho + 60))
    print(f"{'TOTAL':<{ancho}}  {total_c:>12}  {total_a:>8}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
