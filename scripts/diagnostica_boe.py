"""Diagnostica por qué una norma del BOE da menos artículos de los esperados.

Uso: python scripts/diagnostica_boe.py <boe_id>
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request


def baja(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; opotcae/0.1)"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> int:
    boe_id = sys.argv[1] if len(sys.argv) > 1 else "BOE-A-1986-10495"
    url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
    try:
        html = baja(url)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} para {url}")
        return 1

    t = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    print(f"titulo: {re.sub(r'<[^>]+>', ' ', t.group(1)).strip()[:110] if t else 'n/a'}")
    print(f"bytes: {len(html)}")
    print()
    for nombre, patron in [
        ('div class="bloque" id="aN"', r'<div class="bloque" id="(a\d+)">'),
        ('id="aN" suelto', r'id="(a\d+)"'),
        ('id="artN"', r'id="(art\d+)"'),
        ('h5 class="articulo"', r'<h5 class="articulo">'),
        ('class="articulo" cualquiera', r'class="[^"]*articulo'),
        ("Artículo N visible", r"Art[ií]culo\s+\d+"),
        ('p class="parrafo"', r'<p class="parrafo"'),
    ]:
        print(f"  {nombre:<32} {len(re.findall(patron, html, re.I))}")

    print("\n-- primeros id= que parezcan de artículo --")
    ids = re.findall(r'id="([^"]*)"', html)
    sos = [i for i in ids if re.match(r"^(a|art)\d+$", i)]
    print(f"  {sos[:20]}")

    print("\n-- primer bloque con class=articulo (crudo) --")
    m = re.search(r'<h5 class="articulo">(.{0,1200})', html, re.S)
    if m:
        print(m.group(0)[:1000])
    else:
        print("  (no hay h5.articulo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
