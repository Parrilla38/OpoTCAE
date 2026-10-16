"""Genera web/public/data/migracion_ids.json: cluster_id viejo -> nuevo.

La web lo usa una vez para trasladar el progreso guardado en localStorage.
Solo incluye los ids viejos que ya no existen; se emparejan por el enunciado
normalizado del clúster viejo contra las preguntas actuales. Un id viejo sin
pareja se deja fuera (el progreso de esa pregunta se descarta, no se inventa).

Uso: python scripts/mapa_migracion_ids.py <clusters_viejos.json>
    (git show e202d93:web/public/data/clusters.json > /tmp/viejo.json)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from radar import normalizar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "web" / "public" / "data"


def main() -> int:
    viejos = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    preguntas = json.loads((DATA / "preguntas.json").read_text(encoding="utf-8"))
    vivos = {p["cluster_id"] for p in preguntas}
    por_texto = {normalizar(p["enunciado"]): p["cluster_id"] for p in preguntas}
    mapa: dict[str, int] = {}
    sin_pareja = []
    for c in viejos:
        if c["cluster_id"] in vivos:
            continue
        nuevo = por_texto.get(normalizar(c["enunciado"]))
        if nuevo is None:
            sin_pareja.append(c["cluster_id"])
        else:
            mapa[str(c["cluster_id"])] = nuevo
    (DATA / "migracion_ids.json").write_text(
        json.dumps({"version": 2, "ids": mapa}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(mapa)} ids remapeados; {len(sin_pareja)} sin pareja: {sin_pareja}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
