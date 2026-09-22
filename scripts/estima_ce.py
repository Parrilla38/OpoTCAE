"""Estimación rápida del peso de la Constitución en cada cuadernillo.

ES UNA ESTIMACIÓN POR PALABRAS CLAVE, no un etiquetado. El etiquetado
definitivo de Fase 1 es manual + revisión. Sirve para dimensionar el
trabajo y para el informe FASE0_INVENTARIO.md.

Criterio inclusivo a propósito: preferimos falso positivo (luego se descarta
en Fase 1) a falso negativo.

Uso: python scripts/estima_ce.py
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

RE_OPCION_A = re.compile(r"^\s*A\)", re.MULTILINE)

# Bloques de un enunciado: hasta el siguiente "A)" o "N)" o fin.
RE_BLOQUE = re.compile(
    r"(?:^|\n)\s*(?:\d{1,3}\s*[.)]?\s*)?(.{20,600}?)\s*\n\s*A\)",
    re.DOTALL,
)

PATRONES_CE = [
    r"constituci[oó]n",
    r"\bCE\b",
    r"art(?:[íi]culo)?\.?\s*\d+\s*(?:de\s+la\s+)?(?:constituci[oó]n|CE)",
    r"cortes generales",
    r"congreso de los diputados",
    r"senado",
    r"tribunal constitucional",
    r"tribunal supremo",
    r"defensor del pueblo",
    r"poder judicial",
    r"presidente del gobierno",
    r"poder legislativo",
    r"poder ejecutivo",
    r"soberan[íi]a nacional",
    r"deberes y derechos",
    r"deberes c[íi]vicos",
    r"t[íi]tulo preliminar",
    r"reforma constitucional",
    r"procedimiento de reforma",
    r"delito de rebeli[oó]n",
    r"estado de alarma",
    r"estado de excepci[oó]n",
    r"estado de sitio",
    r"declaraci[oó]n del estado",
    r"consejo general del poder judicial",
    r"audiencia nacional",
    r"defensor del pueblo",
    r"partidos pol[íi]ticos",
    r"sindicatos",
    r"organizaciones empresariales",
    r"tribunal de cuentas",
    r"consejo de estado",
    r"banco de espa[ñn]a",
    r"ley org[áa]nica",
    r"refrendo",
    r"sucesi[oó]n a la corona",
    r"regencia",
    r"minor[íi]a de edad del rey",
    r"interinidad",
    r"principio de legalidad",
    r"jerarqu[íi]a normativa",
    r"publicaci[oó]n de las normas",
    r"irretroactividad",
    r"seguridad jur[íi]dica",
    r"responsabilidad del estado",
    r"subsidiariedad de la ley penal",
]

RE_CE = re.compile("|".join(f"(?:{p})" for p in PATRONES_CE), re.IGNORECASE)

# Señales de que NO es Constitución (para la estimación "optimista")
RE_NO_CE = re.compile(
    r"estatuto de autonom[íi]a|estatuto marco|ley 14/1986|ley 2/1998|"
    r"ley 55/2003|ley 41/2002|ley 44/2003|ley 16/2003|LOPDGDD|"
    r"prevenci[oó]n de riesgos|bio[ée]tica|esterilizaci[oó]n|"
    r"[úu]lcera|historia cl[íi]nica|consentimiento informado|"
    r"sistema nacional de salud|servicio andaluz de salud",
    re.IGNORECASE,
)


def cargar_texto(doc_id: str) -> str:
    datos = json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))
    return "\n".join(p["texto"] for p in datos.get("paginas", []))


def estimar(texto: str) -> dict:
    bloques = RE_BLOQUE.findall(texto)
    if not bloques:
        return {"bloques": 0, "ce": 0, "ce_neto": 0, "ejemplos": []}
    positivos = []
    for b in bloques:
        b_limpio = re.sub(r"\s+", " ", b).strip()
        if RE_CE.search(b_limpio):
            positivos.append(b_limpio)
    netos = [b for b in positivos if not RE_NO_CE.search(b)]
    return {
        "bloques": len(bloques),
        "ce": len(positivos),
        "ce_neto": len(netos),
        "ejemplos": netos[:3],
    }


def main() -> int:
    print(f"{'id':<32} {'bloques':>8} {'CE (amplio)':>12} {'CE (neto)':>10} {'% neto':>8}")
    print("-" * 76)
    tot_b = tot_c = tot_n = 0
    for doc in DOCUMENTOS:
        if doc["tipo"] != "cuadernillo":
            continue
        texto = cargar_texto(doc["id"])
        r = estimar(texto)
        pct = (100 * r["ce_neto"] / r["bloques"]) if r["bloques"] else 0
        print(
            f"{doc['id']:<32} {r['bloques']:>8} {r['ce']:>12} {r['ce_neto']:>10} {pct:>7.1f}%"
        )
        tot_b += r["bloques"]
        tot_c += r["ce"]
        tot_n += r["ce_neto"]

    print("-" * 76)
    pct = (100 * tot_n / tot_b) if tot_b else 0
    print(f"{'TOTAL':<32} {tot_b:>8} {tot_c:>12} {tot_n:>10} {pct:>7.1f}%")
    print()
    print("Nota: 'CE (neto)' excluye enunciados que mencionan CE pero claramente")
    print("tratan de otra norma (Estatuto Marco, LGS, LOPDGDD...). Es una")
    print("estimación para dimensionar; el etiquetado de Fase 1 es el válido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
