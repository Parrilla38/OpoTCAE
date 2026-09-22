"""Extrae el contenido de los PDFs del manifiesto a JSON crudo.

Hace dos cosas:
  1. Sondea si el PDF tiene texto extraíble (vs. escaneado sin OCR).
  2. Vuelca el texto de cada página a data/raw/{doc_id}.json.

NO parsea aún preguntas/respuestas: eso es Fase 1. Aquí solo se aterriza el
material de origen y se documenta su calidad de extracción.

Uso:
    python scripts/extraer_pdf.py
    python scripts/extraer_pdf.py --solo 2025_librepi_cuadernillo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import DOCUMENTOS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
PDFS = RAIZ / "data" / "pdfs"
RAW = RAIZ / "data" / "raw"

# Un PDF "con texto" tiene palabras reales, no solo espacios o símbolos.
MIN_CARACTERES_POR_PAGINA = 40
MIN_PALABRAS_POR_PAGINA = 5
RE_PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{3,}")


def limpiar_texto(texto: str) -> str:
    """Normaliza saltos de línea y espacios múltiples sin tocar contenido."""
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def extraer_doc(doc: dict) -> dict:
    ruta = PDFS / doc["destino"]
    if not ruta.exists():
        return {
            **doc,
            "estado": "no_descargado",
            "n_paginas": 0,
            "paginas": [],
            "muestra": "",
        }

    try:
        reader = PdfReader(str(ruta))
    except Exception as e:  # noqa: BLE001
        return {
            **doc,
            "estado": f"error_lectura:{type(e).__name__}",
            "n_paginas": 0,
            "paginas": [],
            "muestra": "",
        }

    paginas = []
    con_texto = 0
    sin_texto = 0
    for i, page in enumerate(reader.pages, 1):
        try:
            crudo = page.extract_text() or ""
        except Exception:  # noqa: BLE001
            crudo = ""
        texto = limpiar_texto(crudo)
        palabras = RE_PALABRA.findall(texto)
        tiene_texto = (
            len(texto) >= MIN_CARACTERES_POR_PAGINA
            and len(palabras) >= MIN_PALABRAS_POR_PAGINA
        )
        if tiene_texto:
            con_texto += 1
        else:
            sin_texto += 1
        paginas.append({"n": i, "texto": texto, "tiene_texto": tiene_texto})

    n_paginas = len(paginas)
    if n_paginas == 0:
        estado = "vacio"
    elif con_texto == n_paginas:
        estado = "texto_completo"
    elif con_texto == 0:
        estado = "escaneado_sin_texto"
    else:
        estado = "texto_parcial"

    return {
        **doc,
        "estado": estado,
        "n_paginas": n_paginas,
        "paginas_con_texto": con_texto,
        "paginas_sin_texto": sin_texto,
        "paginas": paginas,
        "muestra": " ".join(p["texto"] for p in paginas if p["tiene_texto"])[:400],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solo", help="id de un único documento")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    docs = [d for d in DOCUMENTOS if not args.solo or d["id"] == args.solo]
    if not docs:
        print(f"No hay documento con id={args.solo!r}")
        return 1

    informe = []
    for doc in docs:
        resultado = extraer_doc(doc)
        out = RAW / f"{doc['id']}.json"
        out.write_text(
            json.dumps(resultado, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        informe.append(
            {
                "id": resultado["id"],
                "anio": resultado["anio"],
                "fecha": resultado["fecha"],
                "modalidad": resultado["modalidad"],
                "tipo": resultado["tipo"],
                "destino": resultado["destino"],
                "estado": resultado["estado"],
                "n_paginas": resultado["n_paginas"],
                "paginas_con_texto": resultado.get("paginas_con_texto", 0),
                "paginas_sin_texto": resultado.get("paginas_sin_texto", 0),
                "muestra": resultado["muestra"][:160],
            }
        )

    (RAW / "_informe_extraccion.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    ancho = max(len(r["id"]) for r in informe)
    print(f"{'id':<{ancho}}  {'estado':<22}  {'pags':>4}  {'texto':>5}  {'sin':>4}")
    for r in informe:
        print(
            f"{r['id']:<{ancho}}  {r['estado']:<22}  {r['n_paginas']:>4}  "
            f"{r['paginas_con_texto']:>5}  {r['paginas_sin_texto']:>4}"
        )

    resumen: dict[str, int] = {}
    for r in informe:
        resumen[r["estado"]] = resumen.get(r["estado"], 0) + 1
    print()
    for estado, n in sorted(resumen.items()):
        print(f"  {estado}: {n}")
    print(f"\nJSON crudo en {RAW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
