"""Crea data/curado/cluster_ids.json a partir de una generación ANTERIOR del pipeline.

El progreso del usuario (localStorage: aciertos, errores, tarjetas SM-2) cuelga de
`cluster_id`. Hasta ahora ese id era el puesto del clúster en el ranking, y cambia
cada vez que se regenera. `radar.py` ahora lo toma de un registro (huella del
enunciado normalizado -> id); este script lo siembra UNA vez para que los clústeres
que ya existían en la web conserven su id tras corregir el parser.

Empareja por POSICIÓN en el cuadernillo (exam_id + pos), no por id de pregunta: los
ids de pregunta de 2016 y 2019 estaban mal numerados, pero el grupo de opciones n.º k
de cada cuadernillo es el mismo antes y después de la corrección.

Uso:
    python scripts/migra_cluster_ids.py --preguntas-viejas viejo/preguntas.json \\
        --clusters-viejos viejo/clusters.json
    (los viejos se sacan con `git show HEAD:data/parsed/preguntas.json` y análogo)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from radar import REGISTRO, CURADO, huella, normalizar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
PREGUNTAS = RAIZ / "data" / "parsed" / "preguntas.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--preguntas-viejas", type=Path, required=True)
    ap.add_argument("--clusters-viejos", type=Path, required=True)
    ap.add_argument("--forzar", action="store_true", help="sobrescribe un registro existente")
    args = ap.parse_args()
    if REGISTRO.exists() and not args.forzar:
        print(f"{REGISTRO.relative_to(RAIZ)} ya existe: no se toca (usa --forzar para rehacerlo)")
        return 1

    viejas = json.loads(args.preguntas_viejas.read_text(encoding="utf-8"))
    clusters = json.loads(args.clusters_viejos.read_text(encoding="utf-8"))
    por_posicion = {(p["exam_id"], p["pos"]): p["id"] for p in viejas}
    id_a_cluster = {o["id"]: c["cluster_id"] for c in clusters for o in c["ocurrencias"]}

    votos: dict[str, Counter] = defaultdict(Counter)
    sin_cluster = 0
    for p in json.loads(PREGUNTAS.read_text(encoding="utf-8")):
        if p.get("anulada"):
            continue
        vieja = por_posicion.get((p["exam_id"], p["pos"]))
        cid = id_a_cluster.get(vieja)
        if cid is None:
            sin_cluster += 1  # estaba anulada o no estaba en la web: tendrá un id nuevo
            continue
        votos[huella(normalizar(p["enunciado"]))][cid] += 1

    ids = {h: min(c, key=lambda k: (-c[k], k)) for h, c in votos.items()}
    siguiente = max(c["cluster_id"] for c in clusters) + 1
    CURADO.mkdir(parents=True, exist_ok=True)
    REGISTRO.write_text(
        json.dumps({"siguiente": siguiente, "ids": ids}, ensure_ascii=False, indent=1, sort_keys=True),
        encoding="utf-8",
    )
    print(f"registro sembrado: {len(ids)} enunciados -> {len(set(ids.values()))} ids "
          f"(siguiente id libre: {siguiente}); {sin_cluster} preguntas sin clúster previo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
