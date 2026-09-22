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

ABREVIATURAS = {
    1: "Constitución", 2: "Estatuto Andalucía", 3: "Organización sanitaria I",
    4: "Organización sanitaria II", 5: "Protección de datos", 6: "Prevención riesgos",
    7: "Igualdad y violencia género", 8: "Estatuto Marco", 9: "Autonomía del paciente",
    10: "TIC SAS", 11: "Documentación sanitaria", 12: "Equipo y comunicación",
    13: "Atención al usuario", 14: "Bioética", 15: "Higiene hospitalaria / IRA",
    16: "Limpieza y esterilización", 17: "Aislamiento hospitalario", 18: "Residuos sanitarios",
    19: "Muestras biológicas", 20: "Necesidad de higiene", 21: "Necesidad de eliminación",
    22: "Necesidad de alimentación", 23: "Necesidad de movilización", 24: "Úlceras por presión",
    25: "Exploración y quirófano", 26: "Salud mental", 27: "El anciano",
    28: "Terminal y paliativos", 29: "RCP y primeros auxilios",
}

# Clínica y anatomía: NO es uno de los 29 temas oficiales del BOJA 153.
# Es contenido transversal del título de TCAE (FP de Grado Medio) que el
# examen sí pregunta. Se marca aparte para no confundirlo con el temario.
NOMBRE_CLINICA = "Anatomía, fisiología y clínica"
CORTO_CLINICA = "Anatomía y clínica"

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
        if p.get("anulada"):
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
            "tema_corto": p.get("tema_corto"),
            "bloque": p.get("bloque"),
        })

    clusters_out = []
    for c in clusters:
        clusters_out.append({
            "cluster_id": c["cluster_id"],
            "tema": c.get("tema"),
            "tema_nombre": c.get("tema_nombre"),
            "tema_corto": ABREVIATURAS.get(c.get("tema"))
            or (CORTO_CLINICA if not c.get("tema") else ""),
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
    clinica = {"tema": None, "nombre": "Anatomía, fisiología y clínica", "corto": "Anatomía y clínica",
               "clusters": 0, "preguntas": 0, "score_total": 0.0, "es_clinica": True}
    sin_tema = {"tema": None, "nombre": "Otros y sin clasificar", "corto": "Otros",
                "clusters": 0, "preguntas": 0, "score_total": 0.0, "es_clinica": True}
    for c in clusters_out:
        t = c["tema"]
        nombre = (c.get("tema_nombre") or "").lower()
        if t is not None:
            d = por_tema.setdefault(t, {
                "tema": t,
                "nombre": TEMAS.get(t, ""),
                "corto": ABREVIATURAS.get(t, ""),
                "clusters": 0,
                "preguntas": 0,
                "score_total": 0.0,
                "es_clinica": False,
            })
            d["clusters"] += 1
            d["preguntas"] += c["frecuencia"]
            d["score_total"] += c["score"]
        elif "anatom" in nombre or "clínic" in nombre or "clinic" in nombre or "fisiolog" in nombre:
            clinica["clusters"] += 1
            clinica["preguntas"] += c["frecuencia"]
            clinica["score_total"] += c["score"]
        else:
            # Sin tema oficial asignado: anatomía, farmacología y clínica que el
            # temario del BOJA 153 no enumera. Se agrupan como «Otros» para no
            # inventar un tema que no existe.
            sin_tema["clusters"] += 1
            sin_tema["preguntas"] += c["frecuencia"]
            sin_tema["score_total"] += c["score"]
    for d in list(por_tema.values()) + [clinica, sin_tema]:
        d["score_total"] = round(d["score_total"], 2)

    temas_lista = [por_tema[t] for t in sorted(por_tema)]
    if clinica["preguntas"]:
        temas_lista.append(clinica)
    if sin_tema["preguntas"]:
        temas_lista.append(sin_tema)

    meta = {
        "fuente": FUENTE,
        "aviso": (
            "Cuadernillos y plantillas oficiales del Servicio Andaluz de Salud "
            "(Junta de Andalucía). Transcripción con fines de estudio. "
            "Consulte siempre el original en la web del SAS."
        ),
        "anios": sorted({p["anio"] for p in preguntas_out}),
        "temas": temas_lista,
        "totales": {
            "preguntas": len(preguntas_out),
            "clusters": len(clusters_out),
            "repetidos": sum(1 for c in clusters_out if c["frecuencia"] > 1),
            "multi_anio": sum(1 for c in clusters_out if c["n_anios"] >= 2),
            "examenes": len(examenes_out),
        },
        "score_formula": "frecuencia × (1 + 0.25 × años_diferentes)",
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
