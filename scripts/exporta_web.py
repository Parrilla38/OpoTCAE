"""Exporta el dataset curado a web/public/data/ para la SPA estática.

Sale de data/parsed/{preguntas,clusters}.json y deja en web/public/data/:
  clusters.json   — clústeres del bloque común con métricas
  preguntas.json  — preguntas del bloque común (con cluster_id)
  examenes.json   — metadatos de cada convocatoria
  meta.json       — temas, años, conteos (para la UI)

Uso: python scripts/exporta_web.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PARSED = RAIZ / "data" / "parsed"
DESTINO = RAIZ / "web" / "public" / "data"

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

ABREVIATURAS = {
    1: "Constitución",
    2: "Estatuto Andalucía",
    3: "Organización sanitaria I",
    4: "Organización sanitaria II",
    5: "Protección de datos",
    6: "Prevención riesgos",
    7: "Igualdad y violencia género",
    8: "Estatuto Marco",
    9: "Autonomía del paciente",
    10: "TIC SAS",
}

FUENTE = "Servicio Andaluz de Salud (Junta de Andalucía)"


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    preguntas = json.loads((PARSED / "preguntas.json").read_text(encoding="utf-8"))
    clusters = json.loads((PARSED / "clusters.json").read_text(encoding="utf-8"))

    # mapa cluster_id -> pregunta original id
    ids_por_cluster: dict[int, set[str]] = defaultdict(set)
    for c in clusters:
        for o in c.get("ocurrencias", []):
            ids_por_cluster[c["cluster_id"]].add(o["id"])

    preguntas_out = []
    for p in preguntas:
        if p.get("bloque") != "comun" or p.get("anulada"):
            continue
        cluster_id = None
        for cid, ids in ids_por_cluster.items():
            if p["id"] in ids:
                cluster_id = cid
                break
        preguntas_out.append({
            "id": p["id"],
            "cluster_id": cluster_id,
            "exam_id": p["exam_id"],
            "anio": p["anio"],
            "fecha": p["fecha"],
            "modalidad": p["modalidad"],
            "numero": p["numero"],
            "enunciado": p["enunciado"],
            "opciones": p["opciones"],
            "correcta": p.get("correcta"),
            "es_reserva": p.get("es_reserva", False),
            "parte": p.get("parte"),
            "tema": p.get("tema"),
            "tema_nombre": p.get("tema_nombre"),
        })

    clusters_out = []
    for c in clusters:
        clusters_out.append({
            "cluster_id": c["cluster_id"],
            "tema": c.get("tema"),
            "tema_nombre": c.get("tema_nombre"),
            "tema_corto": ABREVIATURAS.get(c.get("tema"), ""),
            "enunciado": c["enunciado"],
            "opciones": c["opciones"],
            "correcta": c.get("correcta"),
            "frecuencia": c["frecuencia"],
            "anios": c["años"],
            "n_anios": c["n_años"],
            "score": c["score"],
            "articulos": c.get("articulos", []),
            "match": c.get("match"),
            "ocurrencias": c.get("ocurrencias", []),
        })

    # exámenes: agrupa preguntas por convocatoria
    por_exam: dict[str, dict] = {}
    for p in preguntas_out:
        e = por_exam.setdefault(p["exam_id"], {
            "exam_id": p["exam_id"],
            "anio": p["anio"],
            "fecha": p["fecha"],
            "modalidad": p["modalidad"],
            "n_preguntas_comun": 0,
            "clusters": set(),
        })
        e["n_preguntas_comun"] += 1
        if p["cluster_id"] is not None:
            e["clusters"].add(p["cluster_id"])
    examenes_out = []
    for e in sorted(por_exam.values(), key=lambda x: (x["anio"], x["fecha"], x["modalidad"])):
        examenes_out.append({
            "exam_id": e["exam_id"],
            "anio": e["anio"],
            "fecha": e["fecha"],
            "modalidad": e["modalidad"],
            "n_preguntas_comun": e["n_preguntas_comun"],
            "cluster_ids": sorted(e["clusters"]),
        })

    # meta: temas con conteos, años, totales
    por_tema: dict[int, dict] = {}
    for c in clusters_out:
        t = c["tema"]
        if t is None:
            continue
        d = por_tema.setdefault(t, {
            "tema": t,
            "nombre": TEMAS.get(t, ""),
            "corto": ABREVIATURAS.get(t, ""),
            "clusters": 0,
            "preguntas": 0,
            "score_total": 0.0,
        })
        d["clusters"] += 1
        d["preguntas"] += c["frecuencia"]
        d["score_total"] += c["score"]
    for d in por_tema.values():
        d["score_total"] = round(d["score_total"], 2)

    meta = {
        "fuente": FUENTE,
        "aviso": (
            "Cuadernillos y plantillas oficiales del Servicio Andaluz de Salud "
            "(Junta de Andalucía). Transcripción con fines de estudio. "
            "Consulte siempre el original en la web del SAS."
        ),
        "anios": sorted({p["anio"] for p in preguntas_out}),
        "temas": [por_tema[t] for t in sorted(por_tema)],
        "totales": {
            "preguntas": len(preguntas_out),
            "clusters": len(clusters_out),
            "repetidos": sum(1 for c in clusters_out if c["frecuencia"] > 1),
            "multi_anio": sum(1 for c in clusters_out if c["n_anios"] >= 2),
            "examenes": len(examenes_out),
        },
        "score_formula": "frecuencia * (1 + 0.25 * anios_diferentes)",
    }

    (DESTINO / "clusters.json").write_text(
        json.dumps(clusters_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DESTINO / "preguntas.json").write_text(
        json.dumps(preguntas_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DESTINO / "examenes.json").write_text(
        json.dumps(examenes_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # conceptos semánticos (si existe el análisis)
    sem_path = PARSED / "clusters_semanticos.json"
    if sem_path.exists():
        sem = json.loads(sem_path.read_text(encoding="utf-8"))
        conceptos_out = []
        for g in sem.get("conceptos", []):
            # solo los que caen en >=2 años: es la señal fuerte de repetición
            if g.get("n_anios", 0) < 2:
                continue
            conceptos_out.append({
                "concepto_id": g["concepto_id"],
                "rank": g["rank"],
                "representante": g["representante"],
                "n_preguntas": g["n_preguntas"],
                "anios": g["anios"],
                "n_anios": g["n_anios"],
                "temas": g["temas"],
                "similitud_media": g["similitud_media"],
                "score": g["score_concepto"],
                "miembros": g["miembros"],
            })
        conceptos_out.sort(key=lambda g: -g["score"])
        for n, g in enumerate(conceptos_out, 1):
            g["rank"] = n
        (DESTINO / "conceptos.json").write_text(
            json.dumps({
                "modelo": sem.get("modelo"),
                "umbral": sem.get("umbral"),
                "n_conceptos_total": sem.get("n_conceptos"),
                "n_multi_anio": len(conceptos_out),
                "conceptos": conceptos_out,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        meta["totales"]["conceptos_multi_anio"] = len(conceptos_out)
        meta["totales"]["conceptos"] = sem.get("n_conceptos")
        (DESTINO / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"conceptos:  {len(conceptos_out):>4}  -> {DESTINO / 'conceptos.json'}")

    print(f"clusters:   {len(clusters_out):>4}  -> {DESTINO / 'clusters.json'}")
    print(f"preguntas:  {len(preguntas_out):>4}  -> {DESTINO / 'preguntas.json'}")
    print(f"examenes:   {len(examenes_out):>4}  -> {DESTINO / 'examenes.json'}")
    print(f"temas:      {len(por_tema):>4}  -> {DESTINO / 'meta.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
