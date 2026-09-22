"""Verificación de las anomalías 2 y 3 de Fase 0 y del tema T13.

Anomalía 2: en 2019 las anuladas (53, 73, 88, 139) son idénticas en libre y PI.
Anomalía 3: en 2021 las anuladas (107, 109) son idénticas en libre y PI.
Sospecha de copy-paste en la plantilla. Aquí se comprueba comparando enunciados.

T13 (Atención al usuario) sale con 0 preguntas clasificadas.

Uso: python scripts/verifica_anomalias.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clasificar import REGLAS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
PARSED = RAIZ / "data" / "parsed"

PARES = [
    ("2019-04-27_libre", "2019-04-27_pi", [53, 73, 88, 139],
     "ANOMALÍA 2 · 2019 libre vs PI · anuladas 53, 73, 88, 139"),
    ("2021-12-19_libre", "2021-12-19_pi", [107, 109],
     "ANOMALÍA 3 · 2021 libre vs PI · anuladas 107, 109"),
]

LEXICO_T13 = re.compile(
    r"atenci[óo]n|usuario|acogida|quejas|reclamaciones|satisfacci|"
    r"entrevista|derivaci[óo]n|carta de servicios|defensor del paciente",
    re.I,
)


def main() -> int:
    preguntas = json.loads((PARSED / "preguntas.json").read_text(encoding="utf-8"))
    por = {(p["exam_id"], p["numero"]): p for p in preguntas}

    for a, b, nums, titulo in PARES:
        print("=" * 78)
        print(titulo)
        print("=" * 78)
        todos_iguales = True
        for n in nums:
            pa, pb = por.get((a, n)), por.get((b, n))
            if not pa or not pb:
                print(f"  #{n}: FALTA en {a if not pa else b}")
                todos_iguales = False
                continue
            mismo_enun = pa["enunciado"].strip() == pb["enunciado"].strip()
            mismas_ops = pa["opciones"] == pb["opciones"]
            misma_ok = pa.get("correcta") == pb.get("correcta")
            print(
                f"  #{n}: enunciado={mismo_enun}  opciones={mismas_ops}  "
                f"correcta={pa.get('correcta')}/{pb.get('correcta')} igual={misma_ok}"
            )
            if not mismo_enun:
                todos_iguales = False
                print(f"      L: {pa['enunciado'][:110]}")
                print(f"      P: {pb['enunciado'][:110]}")
            if not mismas_ops:
                todos_iguales = False
                for k in "ABCD":
                    if pa["opciones"].get(k) != pb["opciones"].get(k):
                        print(f"      opcion {k} difiere:")
                        print(f"        L: {pa['opciones'].get(k, '')[:90]}")
                        print(f"        P: {pb['opciones'].get(k, '')[:90]}")
        veredicto = (
            "CONTRASTE OK: son la misma pregunta en ambos turnos. "
            "La anulación idéntica es dato real, no copy-paste."
            if todos_iguales
            else "DIFIEREN: la anulación idéntica es sospechosa. Revisar plantilla a mano."
        )
        print(f"  -> {veredicto}")
        print()

    # ── T13 ──
    print("=" * 78)
    print("TEMA 13 · Atención al usuario · por qué sale 0")
    print("=" * 78)
    t13 = [r for r in REGLAS if r[0] == 13][0][1]
    print(f"regex ({len(t13.pattern)} chars): {t13.pattern[:180]}...")
    print()
    candidatos = [p for p in preguntas if LEXICO_T13.search(p["enunciado"])]
    print(f"preguntas con léxico T13 en el enunciado: {len(candidatos)}")
    por_tema: dict[str, int] = {}
    matchean = 0
    for p in candidatos:
        texto = p["enunciado"] + " " + " ".join(p["opciones"].values())
        if t13.search(texto):
            matchean += 1
        clave = f"T{p['tema']:02d}" if p.get("tema") else (p.get("bloque") or "?")
        por_tema[clave] = por_tema.get(clave, 0) + 1
    print(f"de ellas, T13 matchea: {matchean}")
    print("dónde acaban (por clasificación actual):")
    for k, v in sorted(por_tema.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<12} {v}")
    print()
    print("muestra de candidatos y su clasificación actual:")
    for p in candidatos[:12]:
        marca = "T13-OK" if t13.search(p["enunciado"] + " " + " ".join(p["opciones"].values())) else "----"
        destino = f"T{p['tema']:02d}" if p.get("tema") else (p.get("bloque") or "?")
        print(f"  [{marca}] -> {destino:<10} {p['enunciado'][:85]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
