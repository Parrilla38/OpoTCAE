"""Clustering de preguntas del bloque común + generación del radar.

Match exacto sobre enunciado normalizado + fuzzy (difflib) para casi-idénticas.
Es la primera pasada: los clústeres salen a validación en
docs/VALIDACION_BLOQUE_COMUN.md y el radar en docs/RADAR_BLOQUE_COMUN.md.

Score de repetición:  score = frecuencia × (1 + 0.25 × años_diferentes)

Uso: python scripts/radar.py
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "parsed" / "preguntas.json"
CLUSTERS = RAIZ / "data" / "parsed" / "clusters.json"
DOCS = RAIZ / "docs"

TEMAS = {
    1: "Constitución Española de 1978",
    2: "Estatuto de Autonomía para Andalucía",
    3: "Organización sanitaria (I): SSPA",
    4: "Organización sanitaria (II): Consejería de Salud y SAS",
    5: "Protección de datos y transparencia",
    6: "Prevención de riesgos laborales",
    7: "Igualdad y violencia de género en Andalucía",
    8: "Estatuto Marco del personal estatutario",
    9: "Autonomía del paciente y derechos y deberes",
    10: "TIC en el SAS",
    11: "La documentación sanitaria",
    12: "El trabajo en equipo y la comunicación",
    13: "La atención al usuario",
    14: "Principios fundamentales de la Bioética",
    15: "Higiene hospitalaria e IRA",
    16: "Limpieza, desinfección y esterilización",
    17: "El aislamiento hospitalario",
    18: "Gestión de los residuos sanitarios",
    19: "Muestras biológicas",
    20: "Necesidad de higiene",
    21: "Necesidad de eliminación",
    22: "Necesidad de alimentación",
    23: "Necesidad de movilización",
    24: "Úlceras por presión",
    25: "Exploración y quirófano",
    26: "Salud mental",
    27: "El anciano",
    28: "Terminal y paliativos",
    29: "RCP y primeros auxilios",
}

RE_ART = re.compile(r"art(?:[íi]cul?)?o?\s*n[úu]m\.?\s*(\d{1,3})|art(?:[íi]cul?)?o?\s*\.?\s*(\d{1,3})", re.I)
RE_SALTO = re.compile(r"\s+")


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return RE_SALTO.sub(" ", texto).strip()


def articulos_de(texto: str) -> list[int]:
    """Extrae números de artículo SOLO del enunciado (no de las opciones)."""
    nums = []
    for a, b in RE_ART.findall(texto):
        n = a or b
        if n and 1 <= int(n) <= 169:
            nums.append(int(n))
    return sorted(set(nums))


def similitud(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def agrupa(pares_similares: list[tuple[str, str]], claves: list[str]) -> dict[str, str]:
    """Une cadenas con Union-Find sobre los pares ya aceptados. O(n·α)."""
    padre = {k: k for k in claves}

    def busca(x: str) -> str:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for a, b in pares_similares:
        ra, rb = busca(a), busca(b)
        if ra != rb:
            padre[ra] = rb
    raices: dict[str, str] = {}
    for k in claves:
        raices[k] = busca(k)
    return raices


def main() -> int:
    preguntas = json.loads(SALIDA.read_text(encoding="utf-8"))
    comunes = [p for p in preguntas if not p.get("anulada")]
    print(f"preguntas analizadas: {len(comunes)}")

    # normaliza y etiqueta artículos (solo del enunciado: en las opciones
    # aparecen números de leyes ajenas que ensucian el conteo)
    for p in comunes:
        p["_norm"] = normalizar(p["enunciado"])
        p["_arts"] = articulos_de(p["enunciado"])

    # ── clustering: primero exacto, luego fuzzy sobre los restantes ──
    por_norm: dict[str, list[dict]] = defaultdict(list)
    for p in comunes:
        por_norm[p["_norm"]].append(p)

    claves = sorted(por_norm.keys(), key=lambda k: -len(por_norm[k]))
    # fuzzy solo entre claves de longitud similar y comparten algún token:
    # evita comparar las ~120k parejas y baja de minutos a segundos.
    tokens = {k: set(k.split()) for k in claves}
    pares_sim: list[tuple[str, str]] = []
    for i, a in enumerate(claves):
        for b in claves[i + 1:]:
            if abs(len(a) - len(b)) > 40:
                continue
            ta, tb = tokens[a], tokens[b]
            if not ta or not tb:
                continue
            inter = len(ta & tb)
            if inter == 0 or inter / min(len(ta), len(tb)) < 0.4:
                continue
            if similitud(a, b) >= 0.85:
                pares_sim.append((a, b))
    raices = agrupa(pares_sim, claves)

    grupos: dict[str, list[dict]] = defaultdict(list)
    for k in claves:
        grupos[raices[k]].extend(por_norm[k])

    final = [{"miembros": m, "match": "exacto" if len({x["_norm"] for x in m}) == 1 else "exacto+fuzzy"}
             for m in grupos.values()]

    # ── métricas por clúster ──
    for c in final:
        años = sorted({m["anio"] for m in c["miembros"]})
        c["frecuencia"] = len(c["miembros"])
        c["años"] = años
        c["n_años"] = len(años)
        c["score"] = round(c["frecuencia"] * (1 + 0.25 * len(años)), 2)
        c["tema"] = c["miembros"][0].get("tema")
        c["tema_nombre"] = c["miembros"][0].get("tema_nombre")
        c["tema_corto"] = c["miembros"][0].get("tema_corto")
        c["enunciado"] = c["miembros"][0]["enunciado"]
        c["correcta"] = c["miembros"][0].get("correcta")
        arts: set[int] = set()
        for m in c["miembros"]:
            arts.update(m.get("_arts") or [])
        c["articulos"] = sorted(arts)

    final.sort(key=lambda c: -c["score"])

    # ── persiste ──
    salida_clusters = []
    for i, c in enumerate(final, 1):
        salida_clusters.append({
            "cluster_id": i,
            "tema": c["tema"],
            "tema_nombre": TEMAS.get(c["tema"]),
            "enunciado": c["enunciado"],
            "opciones": c["miembros"][0]["opciones"],
            "correcta": c["correcta"],
            "frecuencia": c["frecuencia"],
            "años": c["años"],
            "n_años": c["n_años"],
            "score": c["score"],
            "articulos": c["articulos"],
            "match": c["match"],
            "ocurrencias": [
                {
                    "id": m["id"],
                    "exam_id": m["exam_id"],
                    "anio": m["anio"],
                    "modalidad": m["modalidad"],
                    "numero": m["numero"],
                    "correcta": m.get("correcta"),
                }
                for m in c["miembros"]
            ],
        })
    CLUSTERS.write_text(json.dumps(salida_clusters, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── radar por tema y por artículo ──
    por_tema: dict[int, list[dict]] = defaultdict(list)
    for c in salida_clusters:
        if c["tema"]:
            por_tema[c["tema"]].append(c)

    articulos_conteo: dict[tuple[int, int], dict] = {}
    for c in salida_clusters:
        for a in c["articulos"]:
            clave = (c["tema"], a)
            d = articulos_conteo.setdefault(clave, {"tema": c["tema"], "art": a, "frecuencia": 0, "años": set(), "enunciados": []})
            d["frecuencia"] += c["frecuencia"]
            d["años"].update(c["años"])
            d["enunciados"].append(c["enunciado"][:90])

    # ══════════════════ VALIDACION_BLOQUE_COMUN.md ══════════════════
    DOCS.mkdir(exist_ok=True)
    lin = []
    lin.append("# Validación — Bloque común (Temas 1-10)")
    lin.append("")
    lin.append("**Necesita tu revisión.** Clústeres generados por match exacto + fuzzy (≥0,85).")
    lin.append("Marca en tu cabeza lo que no cuadre y dímelo; los corrijo antes del radar final.")
    lin.append("")
    lin.append(f"Total clústeres: **{len(salida_clusters)}** · "
               f"preguntas: **{len(comunes)}** · "
               f"repetidos: **{sum(1 for c in salida_clusters if c['frecuencia'] > 1)}**")
    lin.append("")
    for tema in sorted(por_tema):
        lin.append(f"## Tema {tema} — {TEMAS.get(tema, 'Sin título')}")
        lin.append("")
        lin.append("| # | frec | años | score | enunciado | correcta |")
        lin.append("|---|------|------|-------|-----------|----------|")
        for c in sorted(por_tema[tema], key=lambda c: -c["score"]):
            enun = c["enunciado"][:110].replace("|", "/")
            años = ",".join(str(a) for a in c["años"])
            lin.append(f"| {c['cluster_id']} | {c['frecuencia']} | {años} | {c['score']} | {enun} | {c['correcta']} |")
        lin.append("")
    lin.append("## Sin tema asignado (específicos colados en el filtro)")
    lin.append("")
    sin_tema = [c for c in salida_clusters if not c["tema"]]
    if sin_tema:
        lin.append("| # | frec | enunciado |")
        lin.append("|---|------|-----------|")
        for c in sorted(sin_tema, key=lambda c: -c["score"]):
            lin.append(f"| {c['cluster_id']} | {c['frecuencia']} | {c['enunciado'][:110].replace('|', '/')} |")
    else:
        lin.append("_ninguno_")
    lin.append("")
    (DOCS / "VALIDACION_BLOQUE_COMUN.md").write_text("\n".join(lin), encoding="utf-8")

    # ══════════════════ RADAR_BLOQUE_COMUN.md ══════════════════
    lin = []
    lin.append("# Radar — Bloque común TCAE SAS (Temas 1-10)")
    lin.append("")
    lin.append("Preguntas más repetidas en los exámenes oficiales del SAS **2016-2025**.")
    lin.append("Fuente: cuadernillos y plantillas oficiales del Servicio Andaluz de Salud.")
    lin.append("2008 queda archivado (estructura no comparable).")
    lin.append("")
    lin.append("**Score** = `frecuencia × (1 + 0,25 × años_diferentes)`. "
               "Se prioriza la **persistencia multi-año** sobre la frecuencia cruda.")
    lin.append("")
    total_anios = sorted({m["anio"] for p in comunes for m in [p]})
    lin.append(f"Años cubiertos: **{', '.join(str(a) for a in sorted({p['anio'] for p in comunes}))}**")
    lin.append(f"Clústeres: **{len(salida_clusters)}** · preguntas: **{len(comunes)}** · "
               f"repetidas: **{sum(1 for c in salida_clusters if c['frecuencia'] > 1)}**")
    lin.append("")

    lin.append("## Top 25 — las más preguntadas")
    lin.append("")
    lin.append("| # | score | frec | años | Tema | Enunciado | Art. |")
    lin.append("|---|-------|------|------|------|-----------|------|")
    for c in salida_clusters[:25]:
        enun = c["enunciado"][:100].replace("|", "/")
        años = ",".join(str(a) for a in c["años"])
        arts = ",".join(str(a) for a in c["articulos"]) or "—"
        tema_c = f"T{c['tema']:02d}" if c["tema"] else "?"
        lin.append(f"| {c['cluster_id']} | {c['score']} | {c['frecuencia']} | {años} | {tema_c} | {enun} | {arts} |")
    lin.append("")

    lin.append("## Peso por tema")
    lin.append("")
    lin.append("| Tema | Nombre | clústeres | preguntas | % del bloque |")
    lin.append("|------|--------|-----------|-----------|--------------|")
    total_com = len(comunes)
    for tema in sorted(por_tema):
        cl = por_tema[tema]
        n_preg = sum(c["frecuencia"] for c in cl)
        lin.append(f"| T{tema:02d} | {TEMAS[tema]} | {len(cl)} | {n_preg} | {100*n_preg/total_com:.1f}% |")
    lin.append("")

    lin.append("## Artículos / apartados más preguntados")
    lin.append("")
    lin.append("Conteo de clústeres que citan el artículo. Sirve para priorizar el repaso.")
    lin.append("")
    lin.append("| Tema | Art. | frec | años | ejemplo de enunciado |")
    lin.append("|------|------|------|------|---------------------|")
    arts_ord = sorted(
        articulos_conteo.values(),
        key=lambda d: (-d["frecuencia"], d["tema"] or 0, d["art"]),
    )
    for d in arts_ord[:30]:
        años = ",".join(str(a) for a in sorted(d["años"]))
        ejemplo = d["enunciados"][0].replace("|", "/")
        etiqueta_tema = f"T{d['tema']:02d}" if d["tema"] else "clínica"
        lin.append(f"| {etiqueta_tema} | {d['art']} | {d['frecuencia']} | {años} | {ejemplo} |")
    lin.append("")

    lin.append("## Heatmap tema × año (preguntas del bloque común)")
    lin.append("")
    anios = sorted({p["anio"] for p in comunes})
    lin.append("| Tema | " + " | ".join(str(a) for a in anios) + " | total |")
    lin.append("|------|" + "|".join(["---"] * len(anios)) + "|-------|")
    for tema in sorted(por_tema):
        fila = []
        total = 0
        for a in anios:
            n = sum(1 for p in comunes if p.get("tema") == tema and p["anio"] == a)
            fila.append(str(n) if n else "·")
            total += n
        lin.append(f"| T{tema:02d} | " + " | ".join(fila) + f" | **{total}** |")
    lin.append("")

    lin.append("## Repeticiones multi-año (las más persistentes)")
    lin.append("")
    lin.append("Clústeres que han caído en 3 o más años distintos. Es lo que más se repite de verdad.")
    lin.append("")
    lin.append("| # | años | frec | Tema | Enunciado |")
    lin.append("|---|------|------|------|-----------|")
    for c in sorted(salida_clusters, key=lambda c: (-c["n_años"], -c["frecuencia"])):
        if c["n_años"] >= 3:
            enun = c["enunciado"][:100].replace("|", "/")
            años = ",".join(str(a) for a in c["años"])
            tema_c = f"T{c['tema']:02d}" if c["tema"] else "?"
            lin.append(f"| {c['cluster_id']} | {años} | {c['frecuencia']} | {tema_c} | {enun} |")
    lin.append("")
    lin.append("---")
    lin.append("")
    lin.append("_Generado por `scripts/radar.py` sobre `data/parsed/clusters.json`. "
               "Validar contra `docs/VALIDACION_BLOQUE_COMUN.md` antes de publicar._")
    lin.append("")
    (DOCS / "RADAR_BLOQUE_COMUN.md").write_text("\n".join(lin), encoding="utf-8")

    print(f"clústeres: {len(salida_clusters)}  "
          f"(repetidos: {sum(1 for c in salida_clusters if c['frecuencia'] > 1)}, "
          f"multi-año: {sum(1 for c in salida_clusters if c['n_años'] >= 2)})")
    print(f"escrito: docs/VALIDACION_BLOQUE_COMUN.md")
    print(f"escrito: docs/RADAR_BLOQUE_COMUN.md")
    print(f"escrito: data/parsed/clusters.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
