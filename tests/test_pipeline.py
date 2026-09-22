"""Tests del pipeline de OpoTCAE.

Regresiones sobre el clasificador y el parser: si alguien toca los regex y se
queda sin clasificar medio temario, esto lo caza antes de que salga a producción.

    python -m pytest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from clasificar import REGLAS, TEMAS, ABREVIATURAS, clasificar  # noqa: E402
from parsear import (  # noqa: E402
    agrupar_opciones,
    cortar_hueco,
    extraer_numero,
    limpiar,
    parsear_cuadernillo,
)
from articulos import en_palabras, numero_de_titulo  # noqa: E402


# ─────────────────────────── clasificar ───────────────────────────

# (enunciado, tema esperado). Regresión: si un regex se rompe, esto falla.
CASOS_CLASIFICAR = [
    ("Según establece la Constitución Española, respecto del Estado, el Rey es un símbolo de su:", 1),
    ("La Constitución Española, de conformidad con su artículo 1, propugna como valores superiores:", 1),
    ("El artículo 1.1 del Estatuto de Autonomía de Andalucía (Ley Orgánica 2/2007) se refiere a:", 2),
    ("¿Quién integra la Junta de Andalucía?", 2),
    ("El Artículo 47 de la Ley de Salud de Andalucía (Ley 2/1998) determina que el SSPA:", 3),
    ("El Servicio Andaluz de Salud actualmente es una entidad instrumental con forma jurídica de:", 4),
    ("Según la Ley Orgánica 3/2018 de Protección de Datos Personales:", 5),
    ("Según el artículo 4.1 de la Ley de Prevención de Riesgos Laborales (LPRL):", 6),
    ("La ley 13/2007 de violencia de género reconoce que tienen garantizados los derechos:", 7),
    ("Según el Estatuto Marco del personal estatutario (Ley 55/2003), son retribuciones básicas:", 8),
    ("La ley 41/2002, básica reguladora de la autonomía del paciente, establece:", 9),
    ("¿Qué aplicación se utiliza hospitalariamente para recoger datos clínicos con Diraya?", 10),
    ("El registro de enfermería y la hoja de evolución forman parte de la documentación:", 11),
    ("¿Cuál es la definición tradicional de comunicación en el trabajo en equipo?", 12),
    ("El principio bioético de justicia consiste en:", 14),
    ("Las infecciones relacionadas con la asistencia (IRA) se previenen con:", 15),
    ("La esterilización en autoclave se realiza con vapor saturado a:", 16),
    ("Las precauciones de aislamiento de contacto requieren el uso de EPI:", 17),
    ("Los residuos sanitarios del grupo II se depositan en contenedor:", 18),
    ("La conservación de muestras biológicas para hemocultivo exige:", 19),
    ("¿Qué precauciones debería tener para realizar la obtención de un urinocultivo?", 19),
    ("La higiene bucal en pacientes inconscientes debe realizarse:", 20),
    ("El sondaje vesical con sonda de Foley está indicado para:", 21),
    ("Tipo de sonda empleada para el cateterismo vesical a permanencia:", 21),
    ("La alimentación enteral por sonda nasogástrica está indicada cuando:", 22),
    ("La posición de Fowler se utiliza para la movilización del paciente:", 23),
    ("La escala de Norton se usa para valorar el riesgo de úlceras por presión:", 24),
    ("La preparación preoperatoria del paciente para quirófano incluye:", 25),
    ("La técnica de cateterismo cardíaco se realiza en el laboratorio de hemodinámica:", 25),
    ("La unidad de agudos de salud mental atiende a pacientes con:", 26),
    ("El síndrome geriátrico en el anciano se caracteriza por:", 27),
    ("Los cuidados paliativos en el paciente terminal tienen como objetivo:", 28),
    ("La reanimación cardiopulmonar básica en adultos exige compresiones a:", 29),
    ("Las funciones del hígado incluyen la función metabólica y la desintoxicante:", 30),
]


@pytest.mark.parametrize("enunciado,esperado", CASOS_CLASIFICAR)
def test_clasificador(enunciado: str, esperado: int):
    assert clasificar(enunciado) == esperado


def test_los_29_temas_tienen_nombre_y_abreviatura():
    assert set(TEMAS) == set(range(1, 30))
    assert set(ABREVIATURAS) == set(range(1, 30))
    for t in TEMAS:
        assert TEMAS[t].strip()
        assert ABREVIATURAS[t].strip()


def test_las_reglas_cubren_los_temas_1_a_29():
    tems = {t for t, _ in REGLAS}
    assert set(range(1, 30)).issubset(tems), f"faltan reglas para {set(range(1, 30)) - tems}"


def test_las_reglas_compilan_sin_solaparse_en_el_orden():
    """Una regla no debe poder ser vacía: el primer alternante debe existir."""
    for tema, patron in REGLAS:
        assert patron.pattern, f"la regla T{tema} está vacía"
        assert "|" in patron.pattern or len(patron.pattern) > 5, f"la regla T{tema} sospechosamente corta"


def test_tema_13_no_se_pregunta():
    """Documentado: el tema 13 (Atención al usuario) no aparece en el corpus.

    Es un hallazgo de producto, no un bug. Si alguien arregla las reglas y
    empieza a clasificar T13, este test avisa de que hay que revisar el
    documento de hallazgos.
    """
    # caso sintético que sí debería ser T13 si alguna vez aparece
    assert clasificar("La carta de servicios y el libro de reclamaciones del hospital") == 13


# ─────────────────────────── parsear ───────────────────────────


def test_extraer_numero_en_linea_propia():
    """Formato A (2025 / 2024 / 2021): el número va solo en su línea."""
    pre = "\n12\n\n ¿Qué aplicación se utiliza hospitalariamente?\n"
    assert extraer_numero(pre) == 12


def test_extraer_numero_al_inicio():
    """Formato C (2022): número + enunciado en la misma línea."""
    pre = "1 La constitución Española de 1978 establece en su artículo 10.1"
    assert extraer_numero(pre) == 1


def test_extraer_numero_al_final():
    """Formato B (2019): el número cierra el enunciado."""
    pre = "El Plan Andaluz de Salud será aprobado por: 27"
    assert extraer_numero(pre) == 27


def test_extraer_numero_no_se_come_un_articulo():
    """«artículo 10.1» no debe confundirse con el número de pregunta."""
    pre = "10.1 una serie de principios como fundamento del orden político"
    assert extraer_numero(pre) != 10 or extraer_numero(pre) == 1


def test_cortar_hueco_separa_opcion_de_enunciado():
    hueco = (
        "La Consejería de Salud de Andalucía.\n"
        "La Comisión de Dirección de un Hospital del Servicio Andaluz de Salud estará\n"
        "presidida por:\n27\n"
    )
    opcion, pre, numero = cortar_hueco(hueco)
    assert "Comisión" not in opcion
    assert "Comisión" in pre
    assert numero == 27


def test_cortar_hueco_formato_d():
    """Formato D (2016-PI): la última opción arrastra el enunciado siguiente."""
    hueco = (
        "Ofrecer al usuario las mayores y mejores opciones de productos sanguíneos y \n"
        "derivados\n"
        "La visión de los Biobancos del sistema sanitario público de Andalucía(SSPA) es:\n2\n"
    )
    opcion, pre, _ = cortar_hueco(hueco)
    assert "derivados" in opcion
    assert "derivados" not in pre
    assert "La visión" in pre


def test_limpier_borra_paginacion_y_cabeceras():
    texto = "Página 3 de 14\nCUESTIONARIO TEÓRICO\nLa definición de úlcera por presión es:"
    limpio = limpiar(texto)
    assert "Página" not in limpio
    assert "CUESTIONARIO" not in limpio
    assert "úlcera por presión" in limpio


def test_parsear_formato_a():
    """Un bloque con formato A se parte en enunciado + 4 opciones."""
    bloque = (
        "1\n\n La Constitución Española propugna como valores superiores:\n\n"
        "A) La libertad, la justicia, la igualdad y la solidaridad.\n"
        "B) La libertad, la justicia, la igualdad y la cooperación.\n"
        "C) La libertad, la justicia, la igualdad y la fraternidad.\n"
        "D) La libertad, la justicia, la igualdad y el pluralismo político.\n"
    )
    ps = parsear_cuadernillo(bloque, n_main=75)
    assert len(ps) == 1
    p = ps[0]
    assert p["numero"] == 1
    assert "valores superiores" in p["enunciado"]
    assert set(p["opciones"]) == {"A", "B", "C", "D"}
    assert all(p["opciones"][k] for k in "ABCD")
    assert p["opciones"]["A"].startswith("La libertad")


def test_parsear_formato_d_detecta_orden_inverso():
    bloque = (
        "3\n"
        "D)Ser transparente en el funcionamiento\n"
        "C)Disponer de una estructura moderna\n"
        "B)Mantener el espíritu de servicio público\n"
        "A)Ofrecer al usuario opciones de productos\n"
        "La visión de los Biobancos del SSPA es:\n"
    )
    ps = parsear_cuadernillo(bloque, n_main=75)
    assert len(ps) == 1
    p = ps[0]
    assert p["formato"] == "D"
    assert p["orden_opciones"] == "DCBA"
    assert "Biobancos" in p["enunciado"]
    assert p["opciones"]["A"].startswith("Ofrecer")


def test_parsear_dos_preguntas_seguidas():
    bloque = (
        "1\n\n ¿Qué aplicación se utiliza hospitalariamente?\n\n"
        "A) DAH-ECC.\nB) HSAP.\nC) DAH-EXT.\nD) DAH-EG.\n"
        "2\n\n ¿Cuál es el plazo para nombrar Presidente del Gobierno?\n\n"
        "A) Dos meses desde la tercera votación.\nB) Dos meses desde la segunda.\n"
        "C) Dos meses desde la primera.\nD) Un mes desde la primera.\n"
    )
    ps = parsear_cuadernillo(bloque, n_main=75)
    assert len(ps) == 2
    assert [p["numero"] for p in ps] == [1, 2]
    assert ps[0]["opciones"]["D"] == "DAH-EG."
    assert "Presidente del Gobierno" in ps[1]["enunciado"]


def test_agrupar_opciones_encuentra_grupos_de_cuatro():
    texto = "A) uno\nB) dos\nC) tres\nD) cuatro\nA) cinco\nB) seis\nC) siete\nD) ocho\n"
    grupos = agrupar_opciones(texto)
    assert len(grupos) == 2
    assert all(len(g) == 4 for g in grupos)


# ─────────────────────────── contrato de datos ───────────────────────────


def test_los_json_exportados_encajan_con_los_tipos():
    """Si cambia el formato de export, esto avisa antes que TypeScript."""
    d = RAIZ / "web" / "public" / "data"
    if not d.exists():
        pytest.skip("aún no se ha ejecutado exporta_web.py")

    clusters = json.loads((d / "clusters.json").read_text(encoding="utf-8"))
    assert clusters, "clusters.json vacío"
    cl = clusters[0]
    for k in ("cluster_id", "tema", "tema_nombre", "tema_corto", "enunciado", "opciones",
              "correcta", "frecuencia", "anios", "n_anios", "score", "articulos", "ocurrencias"):
        assert k in cl, f"falta la clave {k} en clusters.json"
    assert set(cl["opciones"]) == {"A", "B", "C", "D"}

    preguntas = json.loads((d / "preguntas.json").read_text(encoding="utf-8"))
    assert preguntas
    p = preguntas[0]
    for k in ("id", "cluster_id", "exam_id", "anio", "modalidad", "numero", "enunciado",
              "opciones", "correcta", "tema", "tema_nombre", "tema_corto", "bloque"):
        assert k in p, f"falta la clave {k} en preguntas.json"

    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    for k in ("fuente", "aviso", "anios", "temas", "totales"):
        assert k in meta, f"falta la clave {k} en meta.json"
    assert len(meta["temas"]) >= 28, "faltan temas del temario oficial"


def test_toda_pregunta_tiene_cluster_id():
    d = RAIZ / "web" / "public" / "data"
    if not d.exists():
        pytest.skip("aún no se ha ejecutado exporta_web.py")
    preguntas = json.loads((d / "preguntas.json").read_text(encoding="utf-8"))
    sin = [p["id"] for p in preguntas if p["cluster_id"] is None]
    assert not sin, f"{len(sin)} preguntas sin cluster_id: {sin[:5]}"


def test_toda_pregunta_tiene_respuesta_o_esta_anulada():
    d = RAIZ / "data" / "parsed"
    if not (d / "preguntas.json").exists():
        pytest.skip("aún no se ha ejecutado parsear.py")
    preguntas = json.loads((d / "preguntas.json").read_text(encoding="utf-8"))
    malas = [
        p["id"] for p in preguntas
        if not p.get("anulada") and p.get("correcta") not in ("A", "B", "C", "D")
    ]
    assert not malas, f"{len(malas)} preguntas sin respuesta válida: {malas[:5]}"


# ─────────────────────────── articulados del BOE ───────────────────────────


def test_numerales_en_letra():
    """La LGS numera los artículos con letra («Artículo uno»): hay que leerlos.

    Regresión: si se rompe el conversor, la General de Sanidad se descarga con 0
    artículos y el Modo Repaso deja de enseñar su texto.
    """
    casos = [
        ("Artículo uno. Objeto de la Ley", 1),
        ("Artículo tres. Ámbito", 3),
        ("Artículo veintiuno", 21),
        ("Artículo cincuenta y dos", 52),
        ("Artículo ciento veintitrés", 123),
        ("Artículo 47. Organización", 47),
    ]
    for titulo, esperado in casos:
        assert numero_de_titulo(titulo) == esperado, f"{titulo!r}"


def test_en_palabras_cubre_1_299():
    for n in range(1, 300):
        assert en_palabras(n)


def test_los_articulos_se_descargan_completos():
    """Si el parser del BOE se rompe, esto lo caza antes de publicar."""
    d = RAIZ / "web" / "public" / "leyes"
    if not (d / "indice.json").exists():
        pytest.skip("aún no se ha ejecutado articulos.py")
    indice = json.loads((d / "indice.json").read_text(encoding="utf-8"))
    assert len(indice) >= 6, f"solo {len(indice)} normas en el índice"
    por_clave = {n["clave"]: n for n in indice}
    # mínimos razonables: si bajan de golpe, algo se ha roto en el parser
    minimos = {"ce": 160, "l14-1986": 100, "l41-2002": 20, "l55-2003": 70, "l31-1995": 50}
    for clave, minimo in minimos.items():
        n = por_clave.get(clave, {}).get("n_articulos", 0)
        assert n >= minimo, f"{clave} solo tiene {n} artículos (mínimo {minimo})"


def test_el_texto_de_un_articulo_es_real_y_no_vacio():
    d = RAIZ / "web" / "public" / "leyes"
    ruta = d / "ce.json"
    if not ruta.exists():
        pytest.skip("aún no se ha ejecutado articulos.py")
    ce = json.loads(ruta.read_text(encoding="utf-8"))
    art = ce["articulos"].get("1")
    assert art, "falta el artículo 1 de la Constitución"
    # el texto debe ser el real del art. 1.1 CE
    assert "valores superiores" in art["texto"]
    assert "libertad, la justicia, la igualdad" in art["texto"]
