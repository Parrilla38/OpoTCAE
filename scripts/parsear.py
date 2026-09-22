"""Parser universal de cuadernillos y plantillas del SAS -> preguntas individuales.

Las preguntas se detectan por GRUPOS DE 4 OPCIONES (A-D en cualquier orden):
es la señal más fiable y no depende del estilo tipográfico. El texto de la
última opción del grupo se corta del enunciado siguiente con una heurística
doble: corte en el número de pregunta si lo hay al inicio del hueco, o corte
en la primera línea en mayúscula/¿ que parezca enunciado.

Formatos de cuadernillo (FASE0_INVENTARIO.md §5):
  A) 2025 / 2024 / 2021  — número solo en su línea, ENUNCIADO, luego A-B-C-D
  B) 2019 / 2016-libre   — ENUNCIADO, número solo o al final, luego A-B-C-D
  C) 2022                — número + ENUNCIADO en la misma línea, luego A-B-C-D
  D) 2016-PI             — número solo, luego D-C-B-A (inverso), luego ENUNCIADO

Salida: data/parsed/preguntas.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifiesto import DOCUMENTOS, ANIO_ARCHIVADO  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
SALIDA = RAIZ / "data" / "parsed"

SECCIONES = [
    {"exam_id": "2025-06-07_libre", "cuadernillo": "2025_librepi_cuadernillo",
     "plantilla": "2025_libre_plantilla_def", "plantilla_prov": "2025_libre_plantilla_prov",
     "anio": 2025, "fecha": "2025-06-07", "modalidad": "libre", "pages": (1, 16), "n_main": 75},
    {"exam_id": "2025-06-07_pi", "cuadernillo": "2025_librepi_cuadernillo",
     "plantilla": "2025_pi_plantilla_def", "plantilla_prov": "2025_pi_plantilla_prov",
     "anio": 2025, "fecha": "2025-06-07", "modalidad": "pi", "pages": (17, 32), "n_main": 75},
    {"exam_id": "2025-07-28_aplazada", "cuadernillo": "2025_aplazada_cuadernillo",
     "plantilla": "2025_aplazada_plantilla_def", "plantilla_prov": "2025_aplazada_plantilla_prov",
     "anio": 2025, "fecha": "2025-07-28", "modalidad": "aplazada", "pages": None, "n_main": 75},
    {"exam_id": "2024-02-10_centros-sas", "cuadernillo": "2024_centros_cuadernillo",
     "plantilla": "2024_centros_plantilla_def", "plantilla_prov": "2024_centros_plantilla_prov",
     "anio": 2024, "fecha": "2024-02-10", "modalidad": "centros_sas", "pages": None, "n_main": 75},
    {"exam_id": "2024-02-10_apes", "cuadernillo": "2024_apes_cuadernillo",
     "plantilla": "2024_apes_plantilla_def", "plantilla_prov": "2024_apes_plantilla_prov",
     "anio": 2024, "fecha": "2024-02-10", "modalidad": "apes", "pages": None, "n_main": 75},
    {"exam_id": "2024-04-29_aplazada", "cuadernillo": "2024_aplazada_cuadernillo",
     "plantilla": "2024_aplazada_plantilla_def", "plantilla_prov": "2024_aplazada_plantilla_prov",
     "anio": 2024, "fecha": "2024-04-29", "modalidad": "aplazada", "pages": None, "n_main": 75},
    {"exam_id": "2022-04-03_aplazada", "cuadernillo": "2022_aplazada_cuadernillo",
     "plantilla": "2022_aplazada_plantilla_def", "plantilla_prov": "2022_aplazada_plantilla_prov",
     "anio": 2022, "fecha": "2022-04-03", "modalidad": "aplazada", "pages": None, "n_main": 150},
    {"exam_id": "2021-12-19_libre", "cuadernillo": "2021_libre_cuadernillo",
     "plantilla": "2021_libre_plantilla_def", "plantilla_prov": "2021_libre_plantilla_prov",
     "anio": 2021, "fecha": "2021-12-19", "modalidad": "libre", "pages": None, "n_main": 150},
    {"exam_id": "2021-12-19_pi", "cuadernillo": "2021_pi_cuadernillo",
     "plantilla": "2021_pi_plantilla_def", "plantilla_prov": "2021_pi_plantilla_prov",
     "anio": 2021, "fecha": "2021-12-19", "modalidad": "pi", "pages": None, "n_main": 150},
    {"exam_id": "2019-04-27_libre", "cuadernillo": "2019_libre_cuadernillo",
     "plantilla": "2019_libre_plantilla_def", "plantilla_prov": "2019_libre_plantilla_prov",
     "anio": 2019, "fecha": "2019-04-27", "modalidad": "libre", "pages": None, "n_main": 150},
    {"exam_id": "2019-04-27_pi", "cuadernillo": "2019_pi_cuadernillo",
     "plantilla": "2019_pi_plantilla_def", "plantilla_prov": "2019_pi_plantilla_prov",
     "anio": 2019, "fecha": "2019-04-27", "modalidad": "pi", "pages": None, "n_main": 150},
    {"exam_id": "2016-01-30_libre", "cuadernillo": "2016_libre_cuadernillo",
     "plantilla": "2016_libre_plantilla_corr", "plantilla_prov": "2016_libre_plantilla_prov",
     "anio": 2016, "fecha": "2016-01-30", "modalidad": "libre", "pages": None, "n_main": 150},
    {"exam_id": "2016-01-30_pi", "cuadernillo": "2016_pi_cuadernillo",
     "plantilla": "2016_pi_plantilla_corr", "plantilla_prov": "2016_pi_plantilla_prov",
     "anio": 2016, "fecha": "2016-01-30", "modalidad": "pi", "pages": None, "n_main": 150},
]

RE_OPCION = re.compile(r"(?m)^[ \t]*([A-Da-d])\)[ \t]*")
RE_PLANTILLA = re.compile(r"\b(\d{1,3})\s+([A-Da-d]|ANULADA)\b")
RE_NUM_EN_HUECO = re.compile(r"(?m)^[ \t]*(\d{1,3})[ \t]*$")
RE_NUM_INICIO = re.compile(r"(?m)^[ \t]*(\d{1,3})[ \t]+(?=[A-ZÁÉÍÓÚÜÑ¿¡\"«])")

RE_RUIDO = re.compile(
    r"(?m)^[ \t]*(?:"
    r"P[áa]gina[ \t]+\d+[ \t]*(?:de|/)[ \t]*\d+|P[áa]gina[ \t]+\d+|"
    r"CUESTIONARIO(?:[ \t]+TE[ÓO]RICO(?:-PR[ÁA]CTICO)?|[ \t]+PR[ÁA]CTICO|[ \t]+RESERVA)?|"
    r"TE[ÓO]RICO(?:-PR[ÁA]CTICO)?|PR[ÁA]CTICO|RESERVA|"
    r"PREGUNTAS[ \t]+ACCESO.*|PREGUNTAS|"
    r"OEP[ \t]+\d{4}(?:-\d{2,4})?[ \t]/.*|"
    r"(?:AUXILIAR(?:[ \t]+DE)?[ \t]+ENFERMER[ÍI]A?|T[ÉE]CNICO(?:/A|[ \t]+ESPECIALISTA)?.*ENFERMER[ÍI]A).*|"
    r"SAS_.*|\d+[ \t]*(?:ª|\.ª|a)[ \t]*PRUEBA:.*|CONCURSO-OPOSICI[ÓO]N.*|"
    r"PRUEBA[ \t]+[ÚU]NICA:.*|Servicio[ \t]+Andaluz[ \t]+de[ \t]+Salud|"
    r"SOBRE[ \t]+LA[ \t]+FORMA[ \t]+DE.*|ESTE[ \t]+CUADERNILLO.*|"
    r"CONTIN[ÚU]A[ \t]+EN[ \t]+LA.*|ABRIR[ \t]+SOLO.*|ADVERTENCIAS.*|"
    r"CONSIDERACIONES.*|PRUEBA:[ \t]+CUESTIONARIO.*|"
    r"Turno[ \t]+(?:libre|de[ \t]+promoci[óo]n[ \t]+interna).*"
    r")[ \t]*$"
)
RE_NUM_SOLA = re.compile(r"(?m)^[ \t]*\d{1,3}[ \t]*$")
RE_ALFA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]")


def cargar_raw(doc_id: str) -> dict:
    return json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))


def texto_seccion(datos: dict, pages: tuple[int, int] | None) -> str:
    paginas = datos.get("paginas", [])
    if pages:
        lo, hi = pages
        paginas = [p for p in paginas if lo <= p["n"] <= hi]
    return "\n".join(p["texto"] for p in paginas)


def limpiar(texto: str) -> str:
    texto = RE_RUIDO.sub("", texto)
    texto = RE_NUM_SOLA.sub("", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{2,}", "\n", texto)
    return texto.strip()


def n_alfa(texto: str) -> int:
    return len(RE_ALFA.findall(texto or ""))


def extraer_numero(pre: str) -> int | None:
    """Saca el número de pregunta del pre EN CRUDO (antes de limpiar())."""
    m = RE_NUM_EN_HUECO.search(pre)
    if m:
        return int(m.group(1))
    m = RE_NUM_INICIO.search(pre)
    if m:
        return int(m.group(1))
    m = re.search(r"(?<!\d)(\d{1,3})[ \t]*\r?\n[ \t]*$", pre)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{1,3})[ \t]*$", pre.rstrip())
    if m and 1 <= int(m.group(1)) <= 153:
        return int(m.group(1))
    return None


def cortar_hueco(hueco: str) -> tuple[str, str, int | None]:
    """Parte el hueco posterior a la última opción en (texto_opcion, pre, numero).

    - Si el número va AL INICIO del pre (formatos A/C/D): se corta justo antes.
    - Si el número va AL FINAL del pre (formato B): se corta en el inicio del
      enunciado (primera línea en mayúscula/¿ que parezca enunciado).
    """
    # 1) ¿el número va al inicio del pre? (hay número y después hay enunciado)
    m = RE_NUM_INICIO.search(hueco)
    if not m:
        m = RE_NUM_EN_HUECO.search(hueco)
    if m and n_alfa(hueco[m.end():]) >= 15:
        numero = int(m.group(1))
        return hueco[: m.start()].rstrip(), hueco[m.start():].strip(), numero

    # 2) número al final del pre (formato B) o formato D: corte por mayúscula
    for m2 in re.finditer(r"\n(?=[A-ZÁÉÍÓÚÜÑ¿¡\"«])", hueco):
        previo = hueco[: m2.start()]
        resto = hueco[m2.end():]
        linea = (resto.split("\n", 1) or [""])[0].strip()
        if n_alfa(previo) < 3:
            continue
        if len(linea) >= 25 or linea.endswith((":", "?", "¿")):
            pre = resto
            numero = None
            mf = re.search(r"(?<!\d)(\d{1,3})[ \t]*$", pre.strip())
            if mf:
                numero = int(mf.group(1))
                pre = pre.strip()[: mf.start()].strip()
            return previo.rstrip(), pre, numero
        if previo.rstrip().endswith(".") and len(linea) >= 12:
            pre = resto
            numero = None
            mf = re.search(r"(?<!\d)(\d{1,3})[ \t]*$", pre.strip())
            if mf:
                numero = int(mf.group(1))
                pre = pre.strip()[: mf.start()].strip()
            return previo.rstrip(), pre, numero

    # 3) fallback: todo es texto de opción, pre vacío
    mf = re.search(r"(?<!\d)(\d{1,3})[ \t]*$", hueco.strip())
    if mf:
        return hueco.strip()[: mf.start()].strip(), "", int(mf.group(1))
    return hueco.rstrip(), "", None


def agrupar_opciones(texto: str) -> list[list[tuple[int, int, str]]]:
    marcas = [(m.start(), m.end(), m.group(1).upper()) for m in RE_OPCION.finditer(texto)]
    grupos: list[list[tuple[int, int, str]]] = []
    actual: list[tuple[int, int, str]] = []
    vistas: set[str] = set()
    for marca in marcas:
        letra = marca[2]
        if letra in vistas:
            if len(actual) == 4:
                grupos.append(actual)
            actual = [marca]
            vistas = {letra}
        else:
            actual.append(marca)
            vistas.add(letra)
        if len(actual) == 4:
            grupos.append(actual)
            actual = []
            vistas = set()
    return grupos


def parsear_cuadernillo(texto: str, n_main: int) -> list[dict]:
    grupos = agrupar_opciones(texto)
    preguntas: list[dict] = []
    pre_acumulado = texto[: grupos[0][0][0]] if grupos else ""

    for idx, grupo in enumerate(grupos):
        letras = [l for _, _, l in grupo]
        if sorted(letras) != ["A", "B", "C", "D"]:
            continue
        opciones: dict[str, str] = {}
        for i, (ini, fin, letra) in enumerate(grupo):
            if i + 1 < len(grupo):
                crudo = texto[fin:grupo[i + 1][0]]
            else:
                crudo = texto[fin:]
            opciones[letra] = crudo

        # hueco tras la última opción: [texto de la última opción][pre de la sig.]
        hueco = texto[grupo[-1][1]:]
        if idx + 1 < len(grupos):
            hueco = texto[grupo[-1][1]:grupos[idx + 1][0][0]]
        texto_ultima, pre_sig, numero_sig = cortar_hueco(hueco)
        opciones[grupo[-1][2]] = texto_ultima

        orden_inverso = letras == ["D", "C", "B", "A"]
        # el número se extrae del pre EN CRUDO: limpiar() borra las líneas de número
        numero = extraer_numero(pre_acumulado)
        if orden_inverso:
            # formato D: el número va en el pre (antes de las opciones) y el
            # enunciado viene DESPUÉS de la última opción
            enunciado = pre_sig
        else:
            enunciado = limpiar(pre_acumulado)
            if numero is not None:
                m = re.search(r"^\s*" + str(numero) + r"\b", enunciado)
                if m:
                    enunciado = enunciado[m.end():].strip()
                else:
                    m = re.search(r"(?<!\d)" + str(numero) + r"\s*$", enunciado)
                    if m:
                        enunciado = enunciado[: m.start()].strip()
            if numero is None:
                numero = numero_sig

        preguntas.append({
            "pos": idx,
            "numero": numero,
            "enunciado": re.sub(r"\s+", " ", limpiar(enunciado)).strip(),
            "opciones": {k: re.sub(r"\s+", " ", limpiar(v)).strip() for k, v in opciones.items()},
            "orden_opciones": "".join(letras),
            "formato": "D" if orden_inverso else "ABC",
        })
        pre_acumulado = pre_sig

    for i, p in enumerate(preguntas):
        if p["numero"] is None:
            p["numero"] = i + 1 if i < n_main else 151 + (i - n_main)
            p["numero_inferido"] = True
        else:
            p["numero_inferido"] = False
    return preguntas


def parsear_plantilla(texto: str) -> dict[int, str]:
    tabla: dict[int, str] = {}
    for n_s, letra in RE_PLANTILLA.findall(texto):
        tabla.setdefault(int(n_s), letra.upper())
    return tabla


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    salida: list[dict] = []
    resumen: list[dict] = []

    for sec in SECCIONES:
        if sec["anio"] == ANIO_ARCHIVADO:
            continue
        datos = cargar_raw(sec["cuadernillo"])
        texto = texto_seccion(datos, sec["pages"])
        preguntas = parsear_cuadernillo(texto, sec["n_main"])
        plant = parsear_plantilla(texto_seccion(cargar_raw(sec["plantilla"]), None))
        plant_prov = parsear_plantilla(
            texto_seccion(cargar_raw(sec["plantilla_prov"]), None)
        )

        con_respuesta = anuladas = 0
        for p in preguntas:
            letra = plant.get(p["numero"])
            origen = sec["plantilla"]
            if letra is None:
                letra = plant_prov.get(p["numero"])
                origen = sec["plantilla_prov"]
            if letra == "ANULADA":
                p["correcta"], p["anulada"] = None, True
                anuladas += 1
            elif letra in ("A", "B", "C", "D"):
                p["correcta"], p["anulada"] = letra, False
                con_respuesta += 1
            else:
                p["correcta"], p["anulada"] = None, False
            p["plantilla_origen"] = origen if letra else None
            p["exam_id"] = sec["exam_id"]
            p["anio"] = sec["anio"]
            p["fecha"] = sec["fecha"]
            p["modalidad"] = sec["modalidad"]
            p["es_reserva"] = p["numero"] > sec["n_main"]
            if sec["n_main"] == 150:
                p["parte"] = (
                    "teorico" if p["numero"] <= 100
                    else "practico" if p["numero"] <= 150 else "reserva"
                )
            else:
                p["parte"] = "teorico_practico" if p["numero"] <= sec["n_main"] else "reserva"
            p["cuadernillo"] = sec["cuadernillo"]
            p["id"] = f"{sec['exam_id']}_{p['numero']:03d}"
            salida.append(p)

        resumen.append({
            "exam_id": sec["exam_id"],
            "preguntas": len(preguntas),
            "esperadas": sec["n_main"] + 3,
            "con_respuesta": con_respuesta,
            "anuladas": anuladas,
            "sin_respuesta": len(preguntas) - con_respuesta - anuladas,
            "nums": sorted({p["numero"] for p in preguntas}),
        })

    (SALIDA / "preguntas.json").write_text(
        json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (SALIDA / "_resumen_parseo.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"{'exam_id':<26} {'preg':>5} {'esp':>5} {'ok':>5} {'anul':>5} {'sin':>4}  nums")
    print("-" * 90)
    for r in resumen:
        marca = "" if r["preguntas"] == r["esperadas"] else "  <-- DIFIERE"
        nums = r["nums"]
        huecos = [n for n in range(1, (max(nums) if nums else 0) + 1)
                  if n not in nums and not (101 <= n <= 150 and r["esperadas"] == 78)]
        huecos_s = ",".join(str(h) for h in huecos[:8]) + ("..." if len(huecos) > 8 else "")
        print(
            f"{r['exam_id']:<26} {r['preguntas']:>5} {r['esperadas']:>5} "
            f"{r['con_respuesta']:>5} {r['anuladas']:>5} {r['sin_respuesta']:>4}  {huecos_s}{marca}"
        )
    print("-" * 90)
    tot = sum(r["preguntas"] for r in resumen)
    ok = sum(r["con_respuesta"] for r in resumen)
    an = sum(r["anuladas"] for r in resumen)
    sn = sum(r["sin_respuesta"] for r in resumen)
    print(f"{'TOTAL':<26} {tot:>5} {'':>5} {ok:>5} {an:>5} {sn:>4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
