"""Conteo robusto de preguntas y respuestas en los JSON crudos de Fase 0.

Formatos observados en los cuadernillos del SAS:
  A) 2025 / 2024 / 2021  — número solo en su línea, luego enunciado, luego "A) "
  B) 2019                — número al FINAL del enunciado, antes de "A) "
  C) 2008                — "6. enunciado" al inicio de línea

Formatos de plantilla:
  - columna simple:  "1 A" / "45 ANULADA"
  - rejilla multicolumna: "1 B 51 C 101 D 151 A"
  La numeración de reservas SIEMPRE es 151, 152, 153 (convención del SAS,
  independientemente de que el examen tenga 75 o 150 preguntas).

Uso: python scripts/conteo.py
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

# Un enunciado siempre arranca su bloque de opciones con "A)".
RE_OPCION_A = re.compile(r"^\s*A\)", re.MULTILINE)
RE_OPCIONES = re.compile(r"^\s*([A-D])\)", re.MULTILINE)

# Número de pregunta en su propia línea (formato 2025/2024/2021)
RE_NUM_LINEA = re.compile(r"^\s*(\d{1,3})\s*$", re.MULTILINE)
# "6. enunciado" (formato 2008)
RE_NUM_PUNTO = re.compile(r"^\s*(\d{1,3})\.\s+\S", re.MULTILINE)
# Número al final de la última línea del enunciado (formato 2019):
# se detecta mirando el trozo justo antes de cada "A)".
RE_NUM_ANTES_DE_A = re.compile(r"(?:^|\n)\s*(\d{1,3})\s*\n\s*A\)")

# Plantilla: "n <A-D|ANULADA>" en cualquier disposición (una o varias columnas).
RE_PLANTILLA = re.compile(r"\b(\d{1,3})\s+([A-Da-d]|ANULADA)\b")

RE_ANULADA = re.compile(r"\bANULADA\b", re.IGNORECASE)


def cargar(doc_id: str) -> dict | None:
    ruta = RAW / f"{doc_id}.json"
    if not ruta.exists():
        return None
    return json.loads(ruta.read_text(encoding="utf-8"))


def texto_completo(datos: dict) -> str:
    return "\n".join(p["texto"] for p in datos.get("paginas", []))


def contar_cuadernillo(texto: str) -> dict:
    n_a = len(RE_OPCION_A.findall(texto))
    nums_linea = sorted({int(m) for m in RE_NUM_LINEA.findall(texto)})
    nums_punto = sorted({int(m) for m in RE_NUM_PUNTO.findall(texto)})
    nums_antes_a = sorted({int(m) for m in RE_NUM_ANTES_DE_A.findall(texto)})

    if nums_punto and max(nums_punto) >= n_a * 0.8:
        estilo = "2008 (n. punto inicio)"
        nums = nums_punto
    elif nums_antes_a and len(nums_antes_a) >= n_a * 0.5:
        estilo = "2019 (n. al final del enunciado)"
        nums = nums_antes_a
    elif nums_linea:
        estilo = "2025/2024/2021 (n. solo en linea)"
        nums = nums_linea
    else:
        estilo = "indeterminado"
        nums = []

    # filtra números de paginacion ("Página 1 de 14") y otros ruidos
    nums = [n for n in nums if 1 <= n <= 200]
    faltan = [n for n in range(1, (max(nums) if nums else 0) + 1) if n not in set(nums)]
    return {
        "estilo": estilo,
        "preguntas_por_opcion_A": n_a,
        "numeros_detectados": len(nums),
        "rango": f"{nums[0]}-{nums[-1]}" if nums else "-",
        "faltan": faltan,
    }


def contar_plantilla(texto: str) -> dict:
    pares = RE_PLANTILLA.findall(texto)
    # descarta el ruido de cabeceras ("Orden Examen Respuesta Correcta")
    pares = [(int(n), letra.upper()) for n, letra in pares]
    vistos: dict[int, str] = {}
    for n, letra in pares:
        vistos.setdefault(n, letra)

    reales = sorted(n for n in vistos if n <= 150)
    reservas = sorted(n for n in vistos if n > 150)
    anuladas = sorted(n for n, letra in vistos.items() if letra == "ANULADA")
    faltan = [n for n in range(1, (max(reales) if reales else 0) + 1) if n not in vistos]
    return {
        "pares_leidos": len(vistos),
        "preguntas_1_a_150": len(reales),
        "rango_reales": f"{reales[0]}-{reales[-1]}" if reales else "-",
        "reservas_151_153": reservas,
        "anuladas": anuladas,
        "faltan": faltan,
    }


def main() -> int:
    print("=" * 100)
    print("CUADERNILLOS")
    print("=" * 100)
    cab = f"{'id':<32} {'estilo':<34} {'A)':>4} {'nums':>5} {'rango':>8}"
    print(cab)
    print("-" * 100)
    cuad_resumen = []
    for doc in DOCUMENTOS:
        if doc["tipo"] != "cuadernillo":
            continue
        datos = cargar(doc["id"])
        if not datos:
            continue
        c = contar_cuadernillo(texto_completo(datos))
        cuad_resumen.append((doc, c))
        print(
            f"{doc['id']:<32} {c['estilo']:<34} "
            f"{c['preguntas_por_opcion_A']:>4} {c['numeros_detectados']:>5} {c['rango']:>8}"
        )
        if c["faltan"]:
            print(f"    faltan: {c['faltan'][:25]}{' ...' if len(c['faltan']) > 25 else ''}")

    print()
    print("=" * 100)
    print("PLANTILLAS")
    print("=" * 100)
    cab = f"{'id':<32} {'tipo':<17} {'pares':>5} {'1-150':>6} {'rango':>8} {'res':>7} {'anul':>5}"
    print(cab)
    print("-" * 100)
    plant_resumen = []
    for doc in DOCUMENTOS:
        if not (doc["tipo"].startswith("plantilla") or doc["tipo"] == "correccion"):
            continue
        datos = cargar(doc["id"])
        if not datos:
            continue
        p = contar_plantilla(texto_completo(datos))
        plant_resumen.append((doc, p))
        res = ",".join(str(n) for n in p["reservas_151_153"]) or "-"
        anul = ",".join(str(n) for n in p["anuladas"]) or "-"
        print(
            f"{doc['id']:<32} {doc['tipo']:<17} {p['pares_leidos']:>5} "
            f"{p['preguntas_1_a_150']:>6} {p['rango_reales']:>8} {res:>7} {anul:>5}"
        )
        if p["faltan"]:
            print(f"    faltan: {p['faltan'][:25]}{' ...' if len(p['faltan']) > 25 else ''}")

    # ---- cierre: nº de preguntas por convocatoria, usando la plantilla más fiable
    print()
    print("=" * 100)
    print("CIERRE: nº DE PREGUNTAS POR CONVOCATORIA (según plantilla definitiva/corr)")
    print("=" * 100)
    por_conv: dict[tuple[int, str], list[tuple[str, dict]]] = {}
    for doc, p in plant_resumen:
        clave = (doc["anio"], doc["modalidad"])
        por_conv.setdefault(clave, []).append((doc["tipo"], p))

    prioridad = {"plantilla_corr": 0, "correccion": 0, "plantilla_def": 1,
                 "plantilla_inicial": 2, "plantilla_prov": 3}
    for (anio, modalidad), items in sorted(por_conv.items()):
        items.sort(key=lambda t: prioridad.get(t[0], 9))
        tipo, p = items[0]
        marca = "ANULADA en " + ",".join(str(n) for n in p["anuladas"]) if p["anuladas"] else "-"
        print(
            f"{anio} {modalidad:<14} -> {p['rango_reales']:>7}  "
            f"(reservas {p['reservas_151_153'] or '-'})  fuente={tipo}  {marca}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
