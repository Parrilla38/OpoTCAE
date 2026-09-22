"""Busca el id de BOE de una norma por su título.

El identificador BOE-A-YYYY-NNNNN se asigna por orden de publicación, no por
norma: hay que buscarlo. Uso:

    python scripts/busca_boe.py "Ley 14/1986 General de Sanidad"
"""
from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request


def baja(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; opotcae/0.1)"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> int:
    consulta = " ".join(sys.argv[1:]) or "Ley 14/1986 General de Sanidad"
    url = (
        "https://www.boe.es/buscar/boe.php?accion=buscar&campo%5B0%5D=TIT&dato%5B0%5D="
        + urllib.parse.quote(consulta)
    )
    html = baja(url)
    # los resultados vienen como <a href=".../act.php?id=BOE-A-...">Título</a>
    resultados = re.findall(
        r'href="([^"]*act\.php\?id=(BOE-A-[^"&]+))"[^>]*>(.*?)</a>', html, re.S
    )
    vistos = set()
    print(f"consulta: {consulta}")
    print(f"resultados: {len(resultados)}")
    for enlace, boe_id, titulo in resultados[:12]:
        if boe_id in vistos:
            continue
        vistos.add(boe_id)
        t = re.sub(r"<[^>]+>", " ", titulo)
        t = re.sub(r"\s+", " ", t).strip()
        print(f"  {boe_id:<24} {t[:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
