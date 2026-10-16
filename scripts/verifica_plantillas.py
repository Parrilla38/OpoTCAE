"""Verifica cada pregunta parseada contra la plantilla oficial del SAS.

Para cada pregunta (exam_id + numero) compara lo que dice `preguntas.json`
(correcta / anulada) con lo que dice la plantilla, que aquí se lee por un camino
PROPIO (no reutiliza `parsear.tabla_plantilla`) para que un fallo del parser no
pueda darse por bueno a sí mismo. Saca por examen:

  cuadran          la letra (o la anulación) coincide con la plantilla
  fallan           la plantilla dice otra cosa
  no comprobables  la plantilla no trae ese número, o lo trae con dos respuestas distintas

Además de las claves, comprueba la ESTRUCTURA, que es donde nacía el error original
(un número mal asignado le pega a una pregunta la clave de otra y la clave "cuadra"
con la plantilla igualmente): ids únicos, numeración exacta 1..N + 151..153, ningún
número inferido, ninguna opción vacía y ningún texto colado (cabeceras, pies, «CASO
PRÁCTICO»).

Con `--pdftotext` repite la numeración de forma independiente, sobre el texto de
`pdftotext -raw` (otro extractor que pypdf) y exigiendo la secuencia esperada, y
la contrasta con la que trae `preguntas.json`. Es la prueba que habría cazado el
desplazamiento de +1 de 2019 y 2016.

Uso:
    python scripts/verifica_plantillas.py
    python scripts/verifica_plantillas.py --pdftotext --json
Sale con código 1 si algo no cuadra.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import ANIO_ARCHIVADO, DOCUMENTOS  # noqa: E402
from parsear import SECCIONES, secuencia_esperada  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
PDFS = RAIZ / "data" / "pdfs"
PREGUNTAS = RAIZ / "data" / "parsed" / "preguntas.json"
INFORME = RAIZ / "data" / "parsed" / "_verificacion_plantillas.json"

# «1 A», «1A», «153 ANULADA». Sin cruzar líneas; no empieza en medio de un número
# («2025 A») ni de una fecha o una norma («41/2002 A»).
RE_PAR = re.compile(r"(?<![\d/.,\-])(\d{1,3})[ \t]*(ANULADA|[A-D])\b")
RE_COLADO = re.compile(
    r"(?i:CASO\s+PR[ÁA]CTICO|P[áa]gina\s+\d+)|CUESTIONARIO|AUXILIARES?\s+DE\s+ENFERMER|"
    r"T[ÉE]CNICO(?:/A)?\s+(?:ESPECIALISTA\s+)?EN\s+CUIDADOS|OEP\s+\d{4}|INSTRUCCIONES\s+PARA|"
    r"\bRESERVA\b|PRUEBA\s+APLAZADA|TURNO\s+LIBRE"
)
# En un enunciado «caso práctico» o «técnico en cuidados» pueden ser legítimos: solo se
# vigilan cabeceras y pies de página, en mayúsculas como salen en el PDF.
RE_COLADO_ENUNCIADO = re.compile(r"(?i:P[áa]gina\s+\d+\s+de\s+\d+)|CUESTIONARIO|OEP\s+\d{4}|INSTRUCCIONES\s+PARA")
DESTINO = {d["id"]: d["destino"] for d in DOCUMENTOS}


def hay_pdftotext() -> bool:
    return shutil.which("pdftotext") is not None


def _texto_raw(doc_id: str) -> str:
    datos = json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))
    return "\n".join(p["texto"] for p in datos["paginas"])


def _texto_layout(doc_id: str) -> str:
    out = subprocess.run(
        ["pdftotext", "-layout", str(PDFS / DESTINO[doc_id]), "-"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def leer_plantilla(texto: str) -> tuple[dict[int, str], dict[int, set[str]]]:
    """Devuelve (tabla, conflictos). Si un número aparece con dos respuestas distintas
    entra en `conflictos` y se considera NO comprobable."""
    vistas: dict[int, set[str]] = collections.defaultdict(set)
    for linea in texto.splitlines():
        for n_s, valor in RE_PAR.findall(linea):
            vistas[int(n_s)].add(valor)
    tabla = {n: next(iter(v)) for n, v in vistas.items() if len(v) == 1}
    conflictos = {n: v for n, v in vistas.items() if len(v) > 1}
    return tabla, conflictos


def comparar_claves(sec: dict, preguntas: list[dict], leer_texto) -> dict:
    tabla, conflictos = leer_plantilla(leer_texto(sec["plantilla"]))
    tabla_prov, conflictos_prov = leer_plantilla(leer_texto(sec["plantilla_prov"]))
    cuadran = fallan = no_comp = desde_prov = 0
    detalle: list[dict] = []
    for p in preguntas:
        n = p["numero"]
        if n in conflictos and n not in tabla:
            esperado, origen = None, "conflicto"
        elif n in tabla:
            esperado, origen = tabla[n], "definitiva"
        elif n in tabla_prov and n not in conflictos_prov:
            esperado, origen = tabla_prov[n], "provisional"
            desde_prov += 1
        else:
            esperado, origen = None, "ausente"
        if esperado is None:
            no_comp += 1
            detalle.append({"id": p["id"], "estado": "no_comprobable", "motivo": origen})
            continue
        if esperado == "ANULADA":
            ok = bool(p.get("anulada")) and p.get("correcta") is None
        else:
            ok = (not p.get("anulada")) and p.get("correcta") == esperado
        if ok:
            cuadran += 1
        else:
            fallan += 1
            detalle.append({
                "id": p["id"], "estado": "falla", "plantilla": esperado,
                "parseada": "ANULADA" if p.get("anulada") else p.get("correcta"),
            })
    return {
        "cuadran": cuadran, "fallan": fallan, "no_comprobables": no_comp,
        "desde_provisional": desde_prov,
        "conflictos_plantilla": sorted(conflictos),
        "detalle": detalle,
    }


def comprobar_estructura(sec: dict, preguntas: list[dict]) -> list[str]:
    """Problemas de estructura de un examen (lista vacía = bien)."""
    problemas: list[str] = []
    esperados = secuencia_esperada(sec["n_main"])
    ordenadas = sorted(preguntas, key=lambda p: p["pos"])
    numeros = [p["numero"] for p in ordenadas]
    if numeros != esperados:
        falta = sorted(set(esperados) - set(numeros))
        sobra = [n for n, c in collections.Counter(numeros).items() if c > 1 or n not in esperados]
        problemas.append(
            f"numeración distinta de la esperada (faltan {falta[:6]}, sobran/repetidos {sobra[:6]}, "
            f"{len(numeros)} preguntas frente a {len(esperados)})"
        )
    ids = [p["id"] for p in preguntas]
    for i, c in collections.Counter(ids).items():
        if c > 1:
            problemas.append(f"id repetido {i} x{c}")
    for p in preguntas:
        if p.get("numero_inferido"):
            problemas.append(f"{p['id']}: número inferido, no localizado en el texto")
        if not p["enunciado"].strip():
            problemas.append(f"{p['id']}: enunciado vacío")
        if sorted(p["opciones"]) != ["A", "B", "C", "D"]:
            problemas.append(f"{p['id']}: opciones {sorted(p['opciones'])}")
        for letra, t in p["opciones"].items():
            if not t.strip():
                problemas.append(f"{p['id']}: opción {letra} vacía")
            elif RE_COLADO.search(t):
                problemas.append(f"{p['id']}: opción {letra} con texto colado ({t[-50:]!r})")
        m = RE_COLADO_ENUNCIADO.search(p["enunciado"])
        if m:
            problemas.append(f"{p['id']}: enunciado con texto colado ({m.group(0)!r})")
    return problemas


# ───────────── numeración independiente (pdftotext -raw) ─────────────

RE_OPT = re.compile(r"^\s*([A-Da-d])\)\s*(.*)$")
RE_NUM = re.compile(r"^\s*(\d{1,3})(?:\s+(\S.*))?$")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9áéíóúñ]", "", s.lower())


def numeracion_independiente(sec: dict) -> list[dict]:
    """Numera los grupos A-D del cuadernillo con pdftotext, sin usar parsear.py: cada
    grupo toma el número que le toca por secuencia SI ese número aparece en una línea
    del hueco anterior a sus opciones (o pegado a su último enunciado)."""
    args = ["pdftotext", "-raw"]
    if sec["pages"]:
        args += ["-f", str(sec["pages"][0]), "-l", str(sec["pages"][1])]
    args += [str(PDFS / DESTINO[sec["cuadernillo"]]), "-"]
    lineas = subprocess.run(args, capture_output=True, text=True, check=True).stdout.splitlines()

    marcas = [(i, m.group(1).upper(), m.group(2)) for i, l in enumerate(lineas) if (m := RE_OPT.match(l))]
    grupos, actual, vistas = [], [], set()
    for mk in marcas:
        if mk[1] in vistas:
            if len(actual) == 4:
                grupos.append(actual)
            actual, vistas = [mk], {mk[1]}
        else:
            actual.append(mk)
            vistas.add(mk[1])
        if len(actual) == 4:
            grupos.append(actual)
            actual, vistas = [], set()

    esperados = secuencia_esperada(sec["n_main"])
    filas, fin_prev = [], -1
    for gi, g in enumerate(grupos):
        esperado = esperados[gi] if gi < len(esperados) else None
        region = lineas[fin_prev + 1:g[0][0]]
        visto = False
        for l in region:
            m = RE_NUM.match(l)
            if m and int(m.group(1)) == esperado:
                visto = True
            elif esperado is not None and re.search(rf"(?<!\d){esperado}\s*$", l):
                visto = True
        a = next(x for x in g if x[1] == "A")
        filas.append({"num": esperado, "visto": visto, "a": _norm(a[2])[:22]})
        fin_prev = g[-1][0]
    return filas


def comparar_numeracion(sec: dict, preguntas: list[dict]) -> list[str]:
    filas = numeracion_independiente(sec)
    problemas: list[str] = []
    if len(filas) != len(preguntas):
        problemas.append(f"{len(filas)} grupos en pdftotext frente a {len(preguntas)} preguntas parseadas")
    por_pos = {p["pos"]: p for p in preguntas}
    for pos, f in enumerate(filas):
        p = por_pos.get(pos)
        if p is None:
            continue
        if not f["visto"]:
            problemas.append(f"pos {pos}: el número {f['num']} no aparece junto a sus opciones en pdftotext")
        if p["numero"] != f["num"]:
            problemas.append(f"pos {pos}: parseada con número {p['numero']}, pdftotext dice {f['num']}")
        a_parseada = _norm(p["opciones"].get("A", ""))[:15]
        if a_parseada and f["a"] and not (f["a"].startswith(a_parseada) or a_parseada.startswith(f["a"][:15])):
            # en formato D (inverso) la A trae su propia línea; en el resto, mismo texto de arranque
            problemas.append(f"pos {pos} ({p['id']}): la opción A no coincide con la del grupo de pdftotext")
    return problemas


# ─────────────────────────────── main ───────────────────────────────

def verificar(usar_pdftotext: bool = False, ruta: Path = PREGUNTAS) -> dict:
    preguntas = json.loads(ruta.read_text(encoding="utf-8"))
    por_examen: dict[str, list[dict]] = collections.defaultdict(list)
    for p in preguntas:
        por_examen[p["exam_id"]].append(p)

    informe = {"examenes": [], "global": {}, "revisar": []}
    for sec in SECCIONES:
        if sec["anio"] == ANIO_ARCHIVADO:
            continue
        ps = por_examen.get(sec["exam_id"], [])
        claves = comparar_claves(sec, ps, _texto_raw)
        estructura = comprobar_estructura(sec, ps)
        independiente: list[str] = []
        if usar_pdftotext:
            independiente = comparar_numeracion(sec, ps)
            # además, la plantilla leída con -layout (otro extractor) debe dar lo mismo
            lay = comparar_claves(sec, ps, _texto_layout)
            if (lay["cuadran"], lay["fallan"]) != (claves["cuadran"], claves["fallan"]):
                independiente.append(
                    f"plantilla con pdftotext -layout: {lay['cuadran']} cuadran/{lay['fallan']} fallan "
                    f"(frente a {claves['cuadran']}/{claves['fallan']} con pypdf)"
                )
        informe["examenes"].append({
            "exam_id": sec["exam_id"], "preguntas": len(ps),
            **{k: v for k, v in claves.items() if k != "detalle"},
            "detalle_fallos": [d for d in claves["detalle"] if d["estado"] == "falla"],
            "problemas_estructura": estructura,
            "problemas_independientes": independiente,
        })
    informe["revisar"] = [
        {"id": p["id"], "revisar": p["revisar"], "correcta": p.get("correcta")}
        for p in preguntas if p.get("revisar")
    ]
    ex = informe["examenes"]
    informe["global"] = {
        "preguntas": sum(e["preguntas"] for e in ex),
        "cuadran": sum(e["cuadran"] for e in ex),
        "fallan": sum(e["fallan"] for e in ex),
        "no_comprobables": sum(e["no_comprobables"] for e in ex),
        "problemas_estructura": sum(len(e["problemas_estructura"]) for e in ex),
        "problemas_independientes": sum(len(e["problemas_independientes"]) for e in ex),
        "ids_repetidos": len(preguntas) - len({p["id"] for p in preguntas}),
        "independiente_ejecutado": usar_pdftotext,
    }
    return informe


def imprimir(informe: dict) -> None:
    print(f"{'examen':<26} {'preg':>5} {'cuadran':>8} {'fallan':>7} {'no comp.':>9} {'prov.':>6} {'estruct.':>9}")
    print("-" * 78)
    for e in informe["examenes"]:
        print(
            f"{e['exam_id']:<26} {e['preguntas']:>5} {e['cuadran']:>8} {e['fallan']:>7} "
            f"{e['no_comprobables']:>9} {e['desde_provisional']:>6} {len(e['problemas_estructura']):>9}"
        )
    g = informe["global"]
    print("-" * 78)
    print(
        f"{'TOTAL':<26} {g['preguntas']:>5} {g['cuadran']:>8} {g['fallan']:>7} "
        f"{g['no_comprobables']:>9} {'':>6} {g['problemas_estructura']:>9}"
    )
    print(f"ids repetidos: {g['ids_repetidos']}")
    if g["independiente_ejecutado"]:
        print(f"numeración independiente (pdftotext): {g['problemas_independientes']} discrepancias")
    for e in informe["examenes"]:
        for d in e["detalle_fallos"][:10]:
            print(f"  FALLA {d['id']}: plantilla {d['plantilla']}, parseada {d['parseada']}")
        for t in e["problemas_estructura"][:10]:
            print(f"  ESTRUCTURA {e['exam_id']}: {t}")
        for t in e["problemas_independientes"][:10]:
            print(f"  INDEPENDIENTE {e['exam_id']}: {t}")
        if e["conflictos_plantilla"]:
            print(f"  CONFLICTO en plantilla de {e['exam_id']}: números {e['conflictos_plantilla']}")
    for r in informe["revisar"]:
        print(f"  REVISAR {r['id']}: clave guardada {r['correcta']} ({r['revisar']})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdftotext", action="store_true",
                    help="numeración independiente con pdftotext (requiere poppler y los PDF)")
    ap.add_argument("--json", action="store_true", help=f"guarda el informe en {INFORME.relative_to(RAIZ)}")
    ap.add_argument("--preguntas", type=Path, default=PREGUNTAS,
                    help="otro preguntas.json a verificar (p. ej. una versión anterior)")
    args = ap.parse_args()
    if args.pdftotext and not hay_pdftotext():
        print("--pdftotext necesita poppler (pdftotext) en el PATH")
        return 2
    informe = verificar(args.pdftotext, args.preguntas)
    imprimir(informe)
    if args.json:
        INFORME.write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
    g = informe["global"]
    malo = g["fallan"] or g["problemas_estructura"] or g["problemas_independientes"] or g["ids_repetidos"]
    return 1 if malo else 0


if __name__ == "__main__":
    raise SystemExit(main())
