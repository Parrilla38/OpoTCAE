"""Trae el articulado de las leyes que más caen desde el BOE.

Ojo: el texto NO se inventa nunca. Se baja del BOE y se guarda tal cual, con la
URL de origen en cada norma. Si una norma no está en el BOE (las andaluzas están
en el BOJA), se queda sin texto y se marca `origen: null` para que la web muestre
el enlace en vez de un hueco.

Salida:
  data/parsed/leyes/<clave>.json
  web/public/data/leyes/<clave>.json

Uso:
    python scripts/articulos.py            # todo
    python scripts/articulos.py ce         # una sola norma
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO_PARED = RAIZ / "data" / "parsed" / "leyes"
DESTINO_WEB = RAIZ / "web" / "public" / "leyes"

# ── normas que más caen en el examen ─────────────────────────────────
# `temas` indica a qué temas pertenece: sirve para saber qué texto enseñar
# cuando en una pregunta se cita un artículo.
NORMAS = [
    {
        "clave": "ce",
        "nombre": "Constitución Española",
        "corto": "Constitución",
        "abrev": "CE",
        "boe_id": "BOE-A-1978-31229",
        "temas": [1],
    },
    {
        "clave": "l41-2002",
        "nombre": "Ley 41/2002, básica reguladora de la autonomía del paciente",
        "corto": "Autonomía del paciente",
        "abrev": "Ley 41/2002",
        "boe_id": "BOE-A-2002-22188",
        "temas": [9],
    },
    {
        "clave": "l14-1986",
        "nombre": "Ley 14/1986, General de Sanidad",
        "corto": "General de Sanidad",
        "abrev": "Ley 14/1986",
        "boe_id": "BOE-A-1986-10499",
        "temas": [3],
    },
    {
        "clave": "l31-1995",
        "nombre": "Ley 31/1995, de Prevención de Riesgos Laborales",
        "corto": "Prevención de riesgos",
        "abrev": "Ley 31/1995",
        "boe_id": "BOE-A-1995-24292",
        "temas": [6],
    },
    {
        "clave": "l55-2003",
        "nombre": "Ley 55/2003, Estatuto Marco del personal estatutario",
        "corto": "Estatuto Marco",
        "abrev": "Ley 55/2003",
        "boe_id": "BOE-A-2003-23101",
        "temas": [8],
    },
    {
        "clave": "lo2-2007",
        "nombre": "Ley Orgánica 2/2007, Estatuto de Autonomía para Andalucía",
        "corto": "Estatuto Andalucía",
        "abrev": "LO 2/2007",
        "boe_id": "BOE-A-2007-35424",
        "temas": [2],
    },
    {
        "clave": "lo3-2018",
        "nombre": "Ley Orgánica 3/2018, Protección de Datos y garantía de los derechos digitales",
        "corto": "Protección de datos",
        "abrev": "LO 3/2018",
        "boe_id": "BOE-A-2018-16673",
        "temas": [5],
    },
    # Andaluzas: en el BOJA, no en el BOE. Se dejan sin texto y con enlace.
    {
        "clave": "l2-1998",
        "nombre": "Ley 2/1998, de Salud de Andalucía",
        "corto": "Salud de Andalucía",
        "abrev": "Ley 2/1998",
        "boe_id": None,
        "origen": "https://www.juntadeandalucia.es/boja/1998/98/BOJA9809800133.pdf",
        "temas": [3],
    },
]

UNIDADES = {
    0: "", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis",
    7: "siete", 8: "ocho", 9: "nueve", 10: "diez", 11: "once", 12: "doce",
    13: "trece", 14: "catorce", 15: "quince", 16: "dieciséis", 17: "diecisiete",
    18: "dieciocho", 19: "diecinueve", 20: "veinte", 21: "veintiuno",
    22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticinco",
    26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve",
}
DECENAS = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta",
           70: "setenta", 80: "ochenta", 90: "noventa"}
CENTENAS = {100: "ciento", 200: "doscientos", 300: "trescientos",
            400: "cuatrocientos", 500: "quinientos", 600: "seiscientos",
            700: "setecientos", 800: "ochocientos", 900: "novecientos"}


def en_palabras(n: int) -> str:
    if n < 0 or n > 999:
        raise ValueError(n)
    if n == 0:
        return "cero"
    if n == 100:
        return "cien"
    partes = []
    c = (n // 100) * 100
    resto = n % 100
    if c:
        partes.append(CENTENAS[c])
    if resto:
        if resto <= 29:
            partes.append(UNIDADES[resto])
        else:
            d = (resto // 10) * 10
            u = resto % 10
            if u:
                partes.append(f"{DECENAS[d]} y {UNIDADES[u]}")
            else:
                partes.append(DECENAS[d])
    return " ".join(partes)


# mapa palabra -> número, para leer los títulos «Artículo uno» de leyes antiguas
PALABRA_A_NUM = {}
for _n in range(1, 300):
    PALABRA_A_NUM[en_palabras(_n)] = _n
    _sin_acentos = (
        en_palabras(_n)
        .replace("é", "e").replace("í", "i").replace("ó", "o")
        .replace("á", "a").replace("ú", "u")
    )
    PALABRA_A_NUM[_sin_acentos] = _n

PATRON_TITULO = re.compile(r'<h5 class="articulo">(.*?)</h5>', re.S)
PATRON_NUM_DIGITO = re.compile(r"Art[ií]culo\s+(\d+)", re.I)
# tras «Artículo » va el número, en dígito o en letra: se toma hasta la puntuación
PATRON_NUM_PALABRA = re.compile(r"Art[ií]culo\s+([a-záéíóúüñ]+(?:\s+(?:y\s+)?[a-záéíóúüñ]+)*)", re.I)


def numero_de_titulo(titulo: str) -> int | None:
    """'Artículo 47' -> 47 · 'Artículo cincuenta y dos' -> 52 · si no, None."""
    m = PATRON_NUM_DIGITO.search(titulo)
    if m:
        return int(m.group(1))
    m = PATRON_NUM_PALABRA.search(titulo)
    if not m:
        return None
    bruto = m.group(1).strip().lower().rstrip(".,:;")
    # se prueban prefijos largos primero para «ciento veintitrés» y similares
    palabras = bruto.split()
    for i in range(len(palabras), 0, -1):
        clave = " ".join(palabras[:i])
        if clave in PALABRA_A_NUM:
            return PALABRA_A_NUM[clave]
    return None


def extrae_articulos(html: str) -> dict[str, dict]:
    """numero de artículo -> {numero, titulo, epigrafe, texto}

    El BOE ancla algunos artículos con `id="aN"` pero no todos (la LOPDGDD solo
    ancla 9 de sus 144). Lo fiable es `h5.articulo`, que va siempre. Además, leyes
    antiguas como la LGS numeran los artículos con letra («Artículo uno»): se
    convierte con PALABRA_A_NUM. Si un título no se puede numerar, se descarta en
    vez de inventarle un número.
    """
    titulos = list(PATRON_TITULO.finditer(html))
    if not titulos:
        return {}

    salida: dict[str, dict] = {}
    for i, m in enumerate(titulos):
        ini = m.start()
        fin = titulos[i + 1].start() if i + 1 < len(titulos) else len(html)
        trozo = html[ini:fin]

        titulo = quita_html(m.group(1))
        numero = numero_de_titulo(titulo)
        if numero is None or numero in salida:
            continue

        epi = re.search(r'<h6 class="epigrafe">(.*?)</h6>', trozo, re.S)
        epigrafe = quita_html(epi.group(1)) if epi else ""

        textos = [
            quita_html(p)
            for p in re.findall(r'<p class="parrafo[^"]*"[^>]*>(.*?)</p>', trozo, re.S)
        ]
        textos = [t for t in textos if t and not t.startswith("[Bloque")]
        cuerpo = "\n\n".join(textos)
        if not cuerpo:
            continue

        salida[str(numero)] = {
            "numero": numero,
            "titulo": titulo,
            "epigrafe": epigrafe,
            "texto": cuerpo,
        }
    return salida


def quita_html(html: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", html)
    s = re.sub(r"</p>", "\n\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&aacute;", "á").replace("&eacute;", "é")
    s = s.replace("&iacute;", "í").replace("&oacute;", "ó").replace("&uacute;", "ú")
    s = s.replace("&ntilde;", "ñ").replace("&uuml;", "ü").replace("&iexcl;", "¡")
    s = s.replace("&iquest;", "¿").replace("&ordm;", "º").replace("&deg;", "°")
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    s = s.replace("&quot;", '"').replace("&ldquo;", "«").replace("&rdquo;", "»")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def baja(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; opotcae/0.1)"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", errors="replace")




def procesa(norma: dict) -> dict | None:
    if not norma.get("boe_id"):
        return {
            **{k: v for k, v in norma.items() if k != "origen"},
            "origen": norma.get("origen"),
            "fuente": "BOJA (sin texto embebido)",
            "n_articulos": 0,
            "articulos": {},
        }
    url = f"https://www.boe.es/buscar/act.php?id={norma['boe_id']}"
    try:
        html = baja(url)
    except (urllib.error.URLError, OSError) as e:
        print(f"  ERROR al bajar {norma['clave']}: {e}")
        return None

    arts = extrae_articulos(html)
    print(f"  {norma['clave']:<10} {len(arts):>4} artículos  <- {norma['corto']}")
    return {
        **{k: v for k, v in norma.items() if k != "origen"},
        "origen": url,
        "fuente": "BOE",
        "n_articulos": len(arts),
        "articulos": arts,
    }


def main() -> int:
    DESTINO_PARED.mkdir(parents=True, exist_ok=True)
    DESTINO_WEB.mkdir(parents=True, exist_ok=True)

    solo = sys.argv[1] if len(sys.argv) > 1 else None
    indice = []
    print("Descargando articulado del BOE:")
    for norma in NORMAS:
        if solo and norma["clave"] != solo:
            continue
        datos = procesa(norma)
        if datos is None:
            continue
        (DESTINO_PARED / f"{norma['clave']}.json").write_text(
            json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        shutil.copy(
            DESTINO_PARED / f"{norma['clave']}.json", DESTINO_WEB / f"{norma['clave']}.json"
        )
        indice.append(
            {
                "clave": datos["clave"],
                "nombre": datos["nombre"],
                "corto": datos["corto"],
                "abrev": datos["abrev"],
                "origen": datos["origen"],
                "fuente": datos["fuente"],
                "temas": datos["temas"],
                "n_articulos": datos["n_articulos"],
            }
        )
        time.sleep(0.4)

    # índice para que la web sepa qué normas hay sin cargarlas todas
    (DESTINO_PARED / "indice.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    shutil.copy(DESTINO_PARED / "indice.json", DESTINO_WEB / "indice.json")
    print(f"\nÍndice con {len(indice)} normas -> {DESTINO_WEB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
