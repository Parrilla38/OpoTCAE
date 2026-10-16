"""Parser universal de cuadernillos y plantillas del SAS -> preguntas individuales.

Las preguntas se detectan por GRUPOS DE 4 OPCIONES (A-D en cualquier orden):
es la señal más fiable y no depende del estilo tipográfico.

El NÚMERO de cada pregunta se asigna por SECUENCIA ESPERADA (1..n_main y las
reservas 151..153), nunca leyendo "el último entero del hueco": un pie
«Página 2 de 31» o una opción numérica ("A) 4") no pueden hacerse pasar por
número de pregunta. El texto solo sirve para localizar DÓNDE está el número
esperado y así cortar bien la última opción del enunciado siguiente.
Si no se encuentra, la pregunta lleva `numero_inferido: true`.

Formatos de cuadernillo (FASE0_INVENTARIO.md §5):
  A) 2025 / 2024 / 2021  — número solo en su línea, ENUNCIADO, luego A-B-C-D
  B) 2019 / 2016-libre   — ENUNCIADO, número solo o pegado al final, luego A-B-C-D
  C) 2022                — número + ENUNCIADO, luego A-B-C-D
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

# Preguntas cuya clave oficial está en duda y no se decide aquí (regla: ante el
# conflicto se marca, no se decide). La clave que se guarda es SIEMPRE la de la
# plantilla oficial; el campo `revisar` avisa a quien la mire.
REVISAR = {
    "2016-01-30_libre_134": "Jesús: plantilla dice D, el usuario cree C",
}

RE_OPCION = re.compile(r"(?m)^[ \t]*([A-Da-d])\)[ \t]*")
RE_PLANTILLA = re.compile(r"(?<![\d/.])(\d{1,3})[ \t]*(ANULADA|[A-D])\b")

# Cabeceras y pies que no son contenido. Se sustituyen por un CENTINELA (no se
# borran) para que la línea siga existiendo: así se sabe dónde acaba el preámbulo
# del cuadernillo y dónde empieza la primera pregunta.
CENTINELA = "\x00"
RE_RUIDO = re.compile(
    r"(?m)^[ \t]*(?:"
    r"P[áa]gina[ \t]+\d+[ \t]*(?:de|/)[ \t]*\d+|P[áa]gina[ \t]+\d+|"
    r"CUESTIONARIO(?:[ \t]+TE[ÓO]RICO(?:-PR[ÁA]CTICO)?|[ \t]+PR[ÁA]CTICO|[ \t]+RESERVA)?|"
    r"TE[ÓO]RICO(?:-PR[ÁA]CTICO)?|PR[ÁA]CTICO|RESERVA|"
    r"PREGUNTAS[ \t]+ACCESO.*|PREGUNTAS|"
    r"OEP[ \t]+\d{4}(?:-\d{2,4})?[ \t]/.*|"
    r"(?:AUXILIAR(?:[ \t]+DE)?[ \t]+ENFERMER[ÍI]A?|T[ÉE]CNICO(?:/A|[ \t]+ESPECIALISTA)?.*ENFERMER[ÍI]A).*|"
    r"(?i:AUXILIAR(?:[ \t]+DE)?[ \t]+ENFERMER[ÍI]A?)|"
    r"CATEGOR[ÍI]A:.*|"
    r"SAS_.*|\d+[ \t]*(?:ª|\.ª|a)[ \t]*PRUEBA:.*|CONCURSO-OPOSICI[ÓO]N.*|"
    r"PRUEBA[ \t]+[ÚU]NICA:.*|Servicio[ \t]+Andaluz[ \t]+de[ \t]+Salud|"
    r"SOBRE[ \t]+LA[ \t]+FORMA[ \t]+DE.*|ESTE[ \t]+CUADERNILLO.*|"
    r"CONTIN[ÚU]A[ \t]+EN[ \t]+LA.*|ABRIR[ \t]+SOLO.*|ABRIR[ \t]+SOLAMENTE.*|ADVERTENCIAS.*|"
    r"CONSIDERACIONES.*|PRUEBA:[ \t]+CUESTIONARIO.*|"
    r"Turno[ \t]+(?:libre|de[ \t]+promoci[óo]n[ \t]+interna).*"
    r")[ \t]*$"
)
# Restos de la cabecera de página que RE_RUIDO no ve porque sale partida en varias
# líneas ("TÉCNICO EN CUIDADOS / AUXILIARES DE ENFERMERÍA / 2021 / LIBRE"). Solo se
# recortan del FINAL de la última opción de una pregunta.
RE_CABECERA_COLA = re.compile(
    r"^(?:(?:APES_|SAS_)?T[ÉE]CNICO.*|(?:EN[ \t]+)?CUIDADOS.*|AUXILIARES.*|ENFERMER[ÍI]A\b.*|"
    r"\d{4}(?:[ \t]*/.*)?|LIBRE|PRUEBA[ \t]+APLAZADA|TURNO[ \t]+LIBRE.*|PROMOCI[ÓO]N[ \t]+INTERNA)$"
)
# Un caso práctico abre un bloque nuevo: su planteamiento va entre la última
# opción de la pregunta anterior y el número de la siguiente.
RE_CASO = re.compile(r"(?mi)^[ \t]*CASO[ \t]+PR[ÁA]CTICO\b")
RE_FIN_DOCUMENTO = re.compile(r"INSTRUCCIONES[ \t]+PARA|SOBRE[ \t]+LA[ \t]+UTILIZACI[ÓO]N")
RE_INICIO_ENUNCIADO =r"[A-ZÁÉÍÓÚÜÑ¿¡\"«]"
RE_ALFA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]")


def cargar_raw(doc_id: str) -> dict:
    return json.loads((RAW / f"{doc_id}.json").read_text(encoding="utf-8"))


def texto_seccion(datos: dict, pages: tuple[int, int] | None) -> str:
    paginas = datos.get("paginas", [])
    if pages:
        lo, hi = pages
        paginas = [p for p in paginas if lo <= p["n"] <= hi]
    return "\n".join(p["texto"] for p in paginas)


def marcar_ruido(texto: str) -> str:
    return RE_RUIDO.sub(CENTINELA, texto)


def sin_centinela(texto: str) -> str:
    return texto.replace(CENTINELA, "")


def limpiar(texto: str) -> str:
    """Quita ruido y normaliza espacios. NO toca las líneas que son solo un número:
    pueden ser una opción ("A) 4"), y el número de pregunta ya se localiza por secuencia."""
    texto = sin_centinela(marcar_ruido(texto))
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{2,}", "\n", texto)
    return texto.strip()


def n_alfa(texto: str) -> int:
    return len(RE_ALFA.findall(texto or ""))


def secuencia_esperada(n_main: int) -> list[int]:
    """Números que lleva cada cuadernillo, en orden: 1..n_main y las 3 reservas 151..153."""
    return list(range(1, n_main + 1)) + [151, 152, 153]


def _limpia_final(texto: str) -> str:
    return re.sub(r"\s+", " ", sin_centinela(texto)).strip()


def numero_antes(region: str, n: int) -> tuple[int, int] | None:
    """Número ANTES del enunciado (formatos A y C): solo en su línea (o al inicio de la
    del enunciado), con enunciado detrás. Se prefiere la forma «solo en su línea»."""
    patrones = (rf"(?m)^[ \t]*{n}[ \t]*$", rf"(?m)^[ \t]*{n}[ \t]+(?={RE_INICIO_ENUNCIADO})")
    for patron in patrones:
        for m in re.finditer(patron, region):
            if n_alfa(sin_centinela(region[m.end():])) >= 3:
                return m.start(), m.end()
    return None


def numero_despues(region: str, n: int) -> tuple[int, int] | None:
    """Número JUSTO ANTES de las opciones (formatos B y D): solo en su línea o pegado al
    final de la última línea del enunciado ("...es:1"). Gana el último: es el más
    cercano a las opciones."""
    cands = list(re.finditer(rf"(?m)^[ \t]*{n}[ \t]*$", region))
    cands += list(re.finditer(rf"(?m)(?<=\S)[ \t]*(?<!\d){n}[ \t]*$", region))
    if not cands:
        return None
    m = max(cands, key=lambda c: c.start())
    return m.start(), m.end()


def _separar_por_mayuscula(texto: str) -> tuple[str, str]:
    """Heurística de reserva: corta donde empieza una línea que parece enunciado."""
    for m in re.finditer(rf"\n(?={RE_INICIO_ENUNCIADO})", texto):
        previo = texto[: m.start()]
        resto = texto[m.end():]
        linea = resto.split("\n", 1)[0].strip()
        if n_alfa(previo) < 3:
            continue
        if len(linea) >= 25 or linea.endswith((":", "?", "¿")):
            return previo.rstrip(), resto
        if previo.rstrip().endswith(".") and len(linea) >= 12:
            return previo.rstrip(), resto
    return texto.rstrip(), ""


def separar_opcion_enunciado(texto: str) -> tuple[str, str]:
    """Parte [última opción][enunciado siguiente]. Las líneas partidas por el ancho de
    página acaban en espacio y las que cierran un párrafo no: la primera línea sin
    espacio final es el fin de la opción. Si el PDF no distingue (todas con espacio),
    se cae a la heurística de mayúsculas."""
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        if not sin_centinela(linea).strip():
            continue
        if linea.endswith((" ", "\t")):
            continue
        resto = lineas[i + 1:]
        if any(sin_centinela(x).strip() for x in resto):
            return "\n".join(lineas[: i + 1]), "\n".join(resto)
        break
    return _separar_por_mayuscula(texto)


def cortar_caso(opcion: str) -> tuple[str, str | None]:
    """Separa de la última opción el planteamiento del caso práctico que la sigue."""
    m = RE_CASO.search(opcion)
    if not m:
        return opcion, None
    return opcion[: m.start()], _limpia_final(opcion[m.start():])


def recortar_cabecera_cola(opcion: str) -> str:
    lineas = opcion.split("\n")
    while lineas:
        ult = sin_centinela(lineas[-1]).strip()
        if not ult or RE_CABECERA_COLA.match(ult):
            lineas.pop()
        else:
            break
    return "\n".join(lineas)


def partir_region(region: str, esperado: int | None, primera: bool) -> tuple[str, str, bool]:
    """Divide el hueco anterior a un grupo de opciones en (última opción previa,
    enunciado que contiene, número encontrado). El número que se busca es SOLO el
    esperado por la secuencia: ningún otro entero del hueco puede hacerse pasar por él."""
    if esperado is not None:
        hit = numero_antes(region, esperado)
        if hit:
            return region[: hit[0]], region[hit[1]:], True
        hit = numero_despues(region, esperado)
        if hit:
            previo = region[: hit[0]]
            if primera:
                # no hay opción previa: el enunciado es lo que sigue al preámbulo
                return "", previo[previo.rfind(CENTINELA) + 1:], True
            opcion, enun = separar_opcion_enunciado(previo)
            return opcion, enun, True
    if primera:
        return "", region[region.rfind(CENTINELA) + 1:], False
    opcion, enun = separar_opcion_enunciado(region)
    return opcion, enun, False


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
    """Cuadernillo -> preguntas. El número de cada pregunta es el que le toca por
    secuencia; el texto solo se usa para ver DÓNDE está y cortar bien."""
    texto = marcar_ruido(texto)
    grupos = agrupar_opciones(texto)
    esperados = secuencia_esperada(n_main)
    n = len(grupos)
    inversos = [[l for _, _, l in g] == ["D", "C", "B", "A"] for g in grupos]

    opciones: list[dict[str, str]] = []
    for g in grupos:
        d: dict[str, str] = {}
        for i, (_, fin, letra) in enumerate(g[:-1]):
            d[letra] = texto[fin:g[i + 1][0]]
        opciones.append(d)

    enunciados = [""] * n
    hallado = [False] * n
    caso_en: list[str | None] = [None] * n
    fin_prev = 0
    for k, g in enumerate(grupos):
        region = texto[fin_prev:g[0][0]]
        fin_prev = g[-1][1]
        esperado = esperados[k] if k < len(esperados) else None
        previo, enun, ok = partir_region(region, esperado, primera=(k == 0))
        hallado[k] = ok
        if k > 0:
            previo, caso_en[k] = cortar_caso(previo)
            opciones[k - 1][grupos[k - 1][-1][2]] = recortar_cabecera_cola(previo)
        # formato D: el enunciado va DESPUÉS de las opciones, o sea en el hueco siguiente
        if k > 0 and inversos[k - 1]:
            enunciados[k - 1] = enun
        if not inversos[k]:
            enunciados[k] = enun
    if n:
        cola = texto[fin_prev:]
        # tras la última pregunta vienen las instrucciones de la prueba: no son de la opción
        fin_doc = RE_FIN_DOCUMENTO.search(cola)
        if fin_doc:
            cola = cola[: fin_doc.start()]
        if inversos[-1]:
            cola, enunciados[-1] = separar_opcion_enunciado(cola)
        cola, _ = cortar_caso(cola)
        opciones[-1][grupos[-1][-1][2]] = recortar_cabecera_cola(cola)

    preguntas: list[dict] = []
    caso = None
    for k, g in enumerate(grupos):
        numero = esperados[k] if k < len(esperados) else None
        if caso_en[k]:
            caso = caso_en[k]
        if numero is not None and numero > 150:
            caso = None  # las reservas no cuelgan de ningún caso práctico
        p = {
            "pos": k,
            "numero": numero,
            "enunciado": _limpia_final(enunciados[k]),
            "opciones": {l: _limpia_final(opciones[k][l]) for _, _, l in g},
            "orden_opciones": "".join(l for _, _, l in g),
            "formato": "D" if inversos[k] else "ABC",
            "numero_inferido": not hallado[k],
        }
        if caso:
            p["caso"] = caso
        preguntas.append(p)
    return preguntas


def tabla_plantilla(texto: str) -> dict[int, str]:
    """Plantilla -> {número: letra | 'ANULADA'}. Línea a línea (nunca cruza saltos de
    línea) y tolerante a «1A» sin espacio. Si un número sale con dos respuestas gana la
    primera: eso lo destapa verifica_plantillas.py como conflicto."""
    tabla: dict[int, str] = {}
    for linea in texto.splitlines():
        for n_s, letra in RE_PLANTILLA.findall(linea):
            tabla.setdefault(int(n_s), letra)
    return tabla


parsear_plantilla = tabla_plantilla


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    salida: list[dict] = []
    resumen: list[dict] = []
    avisos: list[str] = []

    for sec in SECCIONES:
        if sec["anio"] == ANIO_ARCHIVADO:
            continue
        datos = cargar_raw(sec["cuadernillo"])
        texto = texto_seccion(datos, sec["pages"])
        preguntas = parsear_cuadernillo(texto, sec["n_main"])
        plant = tabla_plantilla(texto_seccion(cargar_raw(sec["plantilla"]), None))
        plant_prov = tabla_plantilla(
            texto_seccion(cargar_raw(sec["plantilla_prov"]), None)
        )

        con_respuesta = anuladas = desde_prov = 0
        for p in preguntas:
            letra = plant.get(p["numero"])
            origen = sec["plantilla"]
            if letra is None:
                letra = plant_prov.get(p["numero"])
                origen = sec["plantilla_prov"]
                if letra is not None:
                    desde_prov += 1
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
            if p["id"] in REVISAR:
                p["revisar"] = REVISAR[p["id"]]
            salida.append(p)

        if desde_prov:
            avisos.append(
                f"{sec['exam_id']}: {desde_prov} respuestas salen de la plantilla PROVISIONAL "
                f"({sec['plantilla_prov']}) porque la definitiva no las trae"
            )
        inferidas = sum(1 for p in preguntas if p["numero_inferido"])
        if inferidas:
            avisos.append(f"{sec['exam_id']}: {inferidas} números no localizados en el texto (inferidos por secuencia)")

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
                  if n not in nums and not (r["esperadas"] == 78 and 76 <= n <= 150)]
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
    for a in avisos:
        print(f"AVISO {a}")
    return 0 if all(r["preguntas"] == r["esperadas"] for r in resumen) else 1


if __name__ == "__main__":
    raise SystemExit(main())
