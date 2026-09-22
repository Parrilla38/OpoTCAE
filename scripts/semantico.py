"""Matching semántico: agrupa preguntas que pregunten lo mismo aunque la
redacción cambie.

El clustering literal (scripts/radar.py) solo encuentra enunciados idénticos.
Aquí se codifican los enunciados con un modelo multilingüe y se agrupan por
similitud de coseno, que captura el CONCEPTO: es lo que explica que el
art. 47 de la Ley 2/1998 caiga en 2019 y 2022 con dos redacciones distintas.

Salida:
  data/parsed/clusters_semanticos.json
  docs/SEMANTICO.md                 (informe de revisión)

Uso: python scripts/semantico.py [--umbral 0.72]
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
PARSED = RAIZ / "data" / "parsed"
DOCS = RAIZ / "docs"

MODELO = "paraphrase-multilingual-MiniLM-L12-v2"

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
}


def normaliza(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.split())


def texto_a_codificar(p: dict) -> str:
    """El enunciado es la señal; se le añade la respuesta correcta como ancla."""
    return f"{p['enunciado']} {p['opciones'].get(p.get('correcta') or 'A', '')}".strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umbral", type=float, default=0.72,
                    help="similitud mínima de coseno para agrupar (0-1)")
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import AgglomerativeClustering

    preguntas = json.loads((PARSED / "preguntas.json").read_text(encoding="utf-8"))
    preguntas = [p for p in preguntas if not p.get("anulada")]
    print(f"preguntas: {len(preguntas)}")
    print(f"modelo:    {MODELO}  (la primera vez se descarga)")

    modelo = SentenceTransformer(MODELO)
    textos = [texto_a_codificar(p) for p in preguntas]
    embeddings = modelo.encode(textos, show_progress_bar=True, normalize_embeddings=True)
    print(f"embeddings: {embeddings.shape}")

    # clustering aglomerativo sobre distancia de coseno
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=1.0 - args.umbral,
        metric="cosine",
        linkage="average",
    )
    etiquetas = clustering.fit_predict(embeddings)

    # similitud intra-grupo (para informar de la cohesión de cada grupo)
    sims = embeddings @ embeddings.T

    grupos: dict[int, list[int]] = defaultdict(list)
    for i, e in enumerate(etiquetas):
        grupos[int(e)].append(i)

    salida = []
    for etiqueta, idxs in sorted(grupos.items(), key=lambda kv: -len(kv[1])):
        if len(idxs) == 1:
            # pregunta suelta: no es un concepto repetido
            continue
        anios = sorted({preguntas[i]["anio"] for i in idxs})
        temas = sorted({preguntas[i].get("tema") for i in idxs if preguntas[i].get("tema")})
        pares = [(i, j) for i in idxs for j in idxs if i < j]
        sim_media = float(np.mean([sims[i][j] for i, j in pares])) if pares else 1.0
        # el "concepto" se representa por la pregunta más conectada al resto
        centro = max(idxs, key=lambda i: float(np.mean([sims[i][j] for j in idxs if j != i])))
        salida.append({
            "concepto_id": etiqueta,
            "n_preguntas": len(idxs),
            "anios": anios,
            "n_anios": len(anios),
            "temas": temas,
            "similitud_media": round(sim_media, 3),
            "representante": preguntas[centro]["enunciado"],
            "representante_id": preguntas[centro]["id"],
            "score_concepto": round(len(idxs) * (1 + 0.35 * len(anios)) * sim_media, 2),
            "miembros": [
                {
                    "id": preguntas[i]["id"],
                    "exam_id": preguntas[i]["exam_id"],
                    "anio": preguntas[i]["anio"],
                    "modalidad": preguntas[i]["modalidad"],
                    "numero": preguntas[i]["numero"],
                    "tema": preguntas[i].get("tema"),
                    "enunciado": preguntas[i]["enunciado"],
                    "correcta": preguntas[i].get("correcta"),
                    "cluster_id": None,
                }
                for i in sorted(idxs, key=lambda i: preguntas[i]["anio"])
            ],
        })

    # enlaza cada miembro con su clúster literal (si lo tiene)
    if (PARSED / "clusters.json").exists():
        literales = json.loads((PARSED / "clusters.json").read_text(encoding="utf-8"))
        id_a_cluster = {}
        for c in literales:
            for o in c.get("ocurrencias", []):
                id_a_cluster[o["id"]] = c["cluster_id"]
        for g in salida:
            for m in g["miembros"]:
                m["cluster_id"] = id_a_cluster.get(m["id"])

    salida.sort(key=lambda g: -g["score_concepto"])
    for n, g in enumerate(salida, 1):
        g["rank"] = n

    (PARSED / "clusters_semanticos.json").write_text(
        json.dumps({
            "modelo": MODELO,
            "umbral": args.umbral,
            "n_preguntas": len(preguntas),
            "n_conceptos": len(salida),
            "conceptos": salida,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # ── informe de revisión ──
    multi = [g for g in salida if g["n_anios"] >= 2]
    lineas = [
        "# Matching semántico — conceptos repetidos",
        "",
        f"Modelo **{MODELO}** · umbral de similitud **{args.umbral}** · "
        f"{len(preguntas)} preguntas analizadas.",
        "",
        "Agrupa preguntas que pregunten **lo mismo con otras palabras**. Es el "
        "complemento al clustering literal: donde `radar.py` encuentra enunciados "
        "idénticos, esto encuentra el concepto subyacente.",
        "",
        f"- **{len(salida)}** conceptos con ≥2 formulaciones distintas",
        f"- **{len(multi)}** de ellos caen en **2 o más años distintos** "
        f"(la señal fuerte de «esto se repite»)",
        f"- {len(preguntas) - sum(g['n_preguntas'] for g in salida)} preguntas "
        f"quedaron como formulación única",
        "",
        "## Conceptos que caen en varios años",
        "",
        "Ordenados por `score = nº preguntas × (1 + 0,35 × años) × similitud_media`.",
        "",
    ]
    for g in multi[:40]:
        lineas.append(f"### {g['rank']}. {g['representante'][:130]}")
        lineas.append("")
        lineas.append(
            f"**{g['n_preguntas']} formulaciones** · años **{', '.join(map(str, g['anios']))}** · "
            f"temas {', '.join('T%02d' % t for t in g['temas']) or '—'} · "
            f"similitud media {g['similitud_media']} · score **{g['score_concepto']}**"
        )
        lineas.append("")
        for m in g["miembros"]:
            lineas.append(f"- `{m['anio']} · {m['modalidad']}` — {m['enunciado'][:120]}")
        lineas.append("")

    lineas += [
        "---",
        "",
        "_Generado por `scripts/semantico.py`. Revisar agrupaciones dudosas y "
        "ajustar `--umbral` si hace falta (bajar = más grupos, subir = menos)._",
        "",
    ]
    (DOCS / "SEMANTICO.md").write_text("\n".join(lineas), encoding="utf-8")

    print()
    print(f"conceptos con >=2 formulaciones: {len(salida)}")
    print(f"  de ellos en >=2 años:          {len(multi)}")
    print(f"preguntas sueltas:               {len(preguntas) - sum(g['n_preguntas'] for g in salida)}")
    print(f"escrito: data/parsed/clusters_semanticos.json")
    print(f"escrito: docs/SEMANTICO.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
