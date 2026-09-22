"""Diagnóstico rápido de Fase 0.

Responde tres preguntas sin tocar el parseo de preguntas (eso es Fase 1):
  1. ¿Qué páginas se quedaron sin texto y por qué (portada, figura, tabla)?
  2. ¿Cuántas preguntas numeradas se ven en cada cuadernillo?
  3. ¿Cuántas líneas de respuesta se ven en cada plantilla definitiva?

Uso: python scripts/diagnostico.py
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

# "1.-" "1." "1)" "1 -" al inicio de línea (típico de cuadernillo SAS)
RE_INICIO_PREGUNTA = re.compile(r"^\s*(\d{1,3})\s*[\.\-\)]\s", re.MULTILINE)
# Plantillas: "1 A" "1.- A" "1)B" o simplemente columnas "n letra"
RE_LINEA_PLANTILLA = re.compile(r"^\s*(\d{1,3})\s*[\.\-\)]?\s*([A-Da-d])\b", re.MULTILINE)
RE_SOLO_NUMERO = re.compile(r"^\s*(\d{1,3})\s*$", re.MULTILINE)


def cargar(doc_id: str) -> dict | None:
    ruta = RAW / f"{doc_id}.json"
    if not ruta.exists():
        return None
    return json.loads(ruta.read_text(encoding="utf-8"))


def texto_completo(datos: dict) -> str:
    return "\n".join(p["texto"] for p in datos.get("paginas", []))


def main() -> int:
    print("=" * 78)
    print("1. PÁGINAS SIN TEXTO (posibles portadas, figuras o escaneos)")
    print("=" * 78)
    for doc in DOCUMENTOS:
        datos = cargar(doc["id"])
        if not datos:
            continue
        sin = [p for p in datos.get("paginas", []) if not p.get("tiene_texto")]
        if not sin:
            continue
        nums = ", ".join(str(p["n"]) for p in sin)
        print(f"\n{doc['id']}  ({doc['tipo']})")
        print(f"  páginas sin texto: {nums}  de {datos['n_paginas']}")
        for p in sin[:3]:
            preview = (p.get("texto") or "").replace("\n", " / ")[:100]
            print(f"    pág {p['n']:<3} len={len(p.get('texto') or ''):<5} {preview!r}")

    print()
    print("=" * 78)
    print("2. PREGUNTAS NUMERADAS EN CUADERNILLOS")
    print("=" * 78)
    filas = []
    for doc in DOCUMENTOS:
        if doc["tipo"] != "cuadernillo":
            continue
        datos = cargar(doc["id"])
        if not datos:
            continue
        texto = texto_completo(datos)
        nums = sorted({int(m) for m in RE_INICIO_PREGUNTA.findall(texto)})
        # cuenta cuántas veces aparece cada número (detecta cortes de columna)
        ocurrencias = RE_INICIO_PREGUNTA.findall(texto)
        filas.append((doc, nums, ocurrencias))
        faltan = [n for n in range(1, (max(nums) if nums else 0) + 1) if n not in nums]
        print(
            f"{doc['id']:<32} n_detectados={len(nums):>3}  "
            f"rango={nums[0] if nums else '-'}-{nums[-1] if nums else '-'}  "
            f"apariciones={len(ocurrencias):>3}"
        )
        if faltan:
            print(f"    faltan: {faltan[:20]}{' ...' if len(faltan) > 20 else ''}")

    print()
    print("=" * 78)
    print("3. LÍNEAS DE RESPUESTA EN PLANTILLAS")
    print("=" * 78)
    for doc in DOCUMENTOS:
        if not doc["tipo"].startswith("plantilla") and doc["tipo"] not in ("correccion",):
            continue
        datos = cargar(doc["id"])
        if not datos:
            continue
        texto = texto_completo(datos)
        pares = RE_LINEA_PLANTILLA.findall(texto)
        numeros = sorted({int(n) for n, _ in pares})
        print(
            f"{doc['id']:<32} tipo={doc['tipo']:<17} "
            f"pares_n_letra={len(pares):>3}  "
            f"numeros={numeros[0] if numeros else '-'}-{numeros[-1] if numeros else '-'}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
