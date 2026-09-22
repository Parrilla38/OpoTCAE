"""Muestra la estructura HTML cruda de un artículo del BOE.

Para diseñar el parser final. Uso:
    python scripts/sondea_articulo.py <url> <ancla>
    python scripts/sondea_articulo.py https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229 a1
"""
from __future__ import annotations

import re
import sys
import urllib.request


def baja(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; opotcae/0.1)"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else (
        "https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229"
    )
    ancla = sys.argv[2] if len(sys.argv) > 2 else "a1"
    html = baja(url)

    # ¿cómo está marcado el artículo?
    print(f"== ocurrencias de id={ancla!r} ==")
    for m in re.finditer(rf'id="{ancla}"', html):
        print(f"  pos {m.start()}")

    # primer bloque class="articulo"
    m = re.search(r'class="[^"]*articulo[^"]*"', html)
    if m:
        ini = max(0, m.start() - 300)
        print("\n== crudo alrededor del primer class=articulo ==")
        print(html[ini : m.start() + 1200])

    print("\n== los 5 primeros bloques articulo con su HTML ==")
    for i, mm in enumerate(re.finditer(r'<p class="articulo"[^>]*>(.*?)</p>', html, re.S)):
        if i >= 5:
            break
        print(f"--- {i} ---")
        print(mm.group(0)[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
