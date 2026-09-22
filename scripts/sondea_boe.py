"""Sondea cómo se lee el articulado en el BOE.

Solo para descubrir el formato: qué marcadores hay y cómo extraer el texto de un
artículo. No es parte del pipeline final.

Uso: python scripts/sondea_boe.py <url>
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
    html = baja(url)
    print(f"bytes: {len(html)}")
    t = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    print(f"titulo: {re.sub(r'<[^>]+>', ' ', t.group(1)).strip()[:110] if t else 'n/a'}")

    print("\n-- marcadores --")
    for nombre, patron in [
        ("'articulo' en clase", r'class="[^"]*articulo'),
        ("id=art_..", r'id="art_\d+'),
        ("'Artículo N' visible", r"Art[ií]culo\s+\d+"),
        ("párrafos <p>", r"<p[\s>]"),
        ("spans", r"<span[\s>]"),
    ]:
        print(f"  {nombre:<24} {len(re.findall(patron, html, re.I))}")

    print("\n-- primeros ids= que empiezan por art --")
    ids = re.findall(r'id="(art[^"]*)"', html)
    print(f"  {ids[:15]}")

    # ¿qué estructura tiene un artículo concreto?
    print("\n-- trozo alrededor de 'Artículo 1' --")
    i = html.find("Artículo 1")
    if i > 0:
        trozo = html[i - 200 : i + 700]
        print(re.sub(r"\s+", " ", trozo)[:600])
    else:
        print("  no aparece 'Artículo 1'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
