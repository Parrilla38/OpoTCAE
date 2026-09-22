"""Descarga los PDFs oficiales del SAS listados en scripts/manifiesto.py.

Uso:
    python scripts/descargar.py            # idempotente: salta los que ya existen
    python scripts/descargar.py --force    # re-descarga todo

Guarda en data/pdfs/ con verificación de tamaño mínimo y tipo MIME.
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import DOCUMENTOS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "pdfs"

TAMANO_MINIMO = 2048  # bytes
USER_AGENT = "Mozilla/5.0 (compatible; tcae-dataset-builder/0.1)"
PAUSA_ENTRE_DESCARGAS = 0.4  # s, para no martillar al SAS


def descargar(doc: dict, force: bool = False) -> tuple[str, str]:
    """Devuelve (estado, detalle) con estado en {ok, ya_existe, error}."""
    destino = DESTINO / doc["destino"]
    if destino.exists() and destino.stat().st_size >= TAMANO_MINIMO and not force:
        return "ya_existe", f"{destino.stat().st_size} B"

    destino.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(doc["url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            datos = resp.read()
            ctype = resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return "error", f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return "error", f"URL: {e.reason}"
    except Exception as e:  # noqa: BLE001
        return "error", f"{type(e).__name__}: {e}"

    if len(datos) < TAMANO_MINIMO:
        return "error", f"demasiado pequeño ({len(datos)} B), ctype={ctype!r}"
    if not datos.startswith(b"%PDF"):
        # ws027.sspa sirve vía externa.asp: puede devolver HTML de error.
        cabecera = datos[:120].decode("latin-1", errors="replace").replace("\n", " ")
        return "error", f"no es PDF (ctype={ctype!r}) cabecera={cabecera!r}"

    destino.write_bytes(datos)
    return "ok", f"{len(datos)} B"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-descarga todo")
    args = ap.parse_args()

    DESTINO.mkdir(parents=True, exist_ok=True)
    resumen = {"ok": 0, "ya_existe": 0, "error": 0}
    errores: list[tuple[dict, str]] = []

    print(f"Descargando {len(DOCUMENTOS)} documentos -> {DESTINO}")
    for i, doc in enumerate(DOCUMENTOS, 1):
        estado, detalle = descargar(doc, force=args.force)
        resumen[estado] += 1
        marca = {"ok": "OK ", "ya_existe": "== ", "error": "ERR"}[estado]
        print(f"[{i:02}/{len(DOCUMENTOS)}] {marca} {doc['id']:<32} {detalle}")
        if estado == "error":
            errores.append((doc, detalle))
        if estado == "ok":
            time.sleep(PAUSA_ENTRE_DESCARGAS)

    print()
    print(f"OK {resumen['ok']} · ya existentes {resumen['ya_existe']} · errores {resumen['error']}")
    if errores:
        print("\nERRORES:")
        for doc, detalle in errores:
            print(f"  {doc['id']}: {detalle}")
            print(f"    {doc['url']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
