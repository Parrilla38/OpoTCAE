"""Manifiesto de PDFs oficiales del SAS — OpoTCAE.

Fuente primaria: Servicio Andaluz de Salud (sspa.juntadeandalucia.es).
Índice de verificación cruzada: opoluz.com/examenes-oficiales/sas/tcae/
MAD (sinfsa.com) es un mirror estricto de 4 de estos PDFs: no aporta años nuevos.

Cada entrada:
  id            identificador estable del fichero
  anio          año REAL de celebración (manda sobre el año del nombre del PDF)
  fecha         fecha de la prueba (ISO)
  modalidad     libre | pi | aplazada | centros_sas | apes | concurso
  tipo          cuadernillo | plantilla_prov | plantilla_def | plantilla_corr |
                plantilla_inicial | correccion | fe_erratas
  url           URL oficial de descarga
  destino       nombre del fichero bajo data/pdfs/

Las plantillas 'def' (y 'corr' / 'correccion', que las sustituyen) son las que
valen para corregir. Las 'prov' / 'inicial' se conservan solo por trazabilidad.
"""

BASE_SAS = (
    "https://www.sspa.juntadeandalucia.es/servicioandaluzdesalud/"
    "sites/default/files/sincfiles/wsas-media-mediafile_sasdocumento/"
)
BASE_WS027 = "https://ws027.sspa.juntadeandalucia.es/library/plantillas/externa.asp?pag="


def _sas(sub: str) -> str:
    return BASE_SAS + sub


def _ws027(sub: str) -> str:
    return BASE_WS027 + sub


DOCUMENTOS = [
    # ───────────────────────────── 2025 ─────────────────────────────
    # 7-jun-2025 ordinaria (libre + PI, cuadernillo común) + 28-jul-2025 aplazada
    # Opoluz: 75 preguntas en la experiencia interactiva de la ordinaria.
    {
        "id": "2025_librepi_cuadernillo",
        "anio": 2025, "fecha": "2025-06-07", "modalidad": "libre_pi",
        "tipo": "cuadernillo",
        "url": _sas("2025/tecnicoa_en_cuidados_auxiliares_de_enfermeria_librepi.pdf"),
        "destino": "2025-06-07_libre-pi_cuadernillo.pdf",
    },
    {
        "id": "2025_libre_plantilla_prov",
        "anio": 2025, "fecha": "2025-06-07", "modalidad": "libre",
        "tipo": "plantilla_prov",
        "url": _sas("2025/plantilla_respuestas_90008_tecnicoa_en_cuidados_auxiliares_de_enfermeria_libre.pdf"),
        "destino": "2025-06-07_libre_plantilla-prov.pdf",
    },
    {
        "id": "2025_libre_plantilla_def",
        "anio": 2025, "fecha": "2025-06-07", "modalidad": "libre",
        "tipo": "plantilla_def",
        "url": _sas("2026/plantdef_tcae_l.pdf"),
        "destino": "2025-06-07_libre_plantilla-def.pdf",
    },
    {
        "id": "2025_pi_plantilla_prov",
        "anio": 2025, "fecha": "2025-06-07", "modalidad": "pi",
        "tipo": "plantilla_prov",
        "url": _sas("2025/plantilla_respuestas_90006_tecnicoa_en_cuidados_auxiliares_de_enfermeria_pi.pdf"),
        "destino": "2025-06-07_pi_plantilla-prov.pdf",
    },
    {
        "id": "2025_pi_plantilla_def",
        "anio": 2025, "fecha": "2025-06-07", "modalidad": "pi",
        "tipo": "plantilla_def",
        "url": _sas("2026/plantdef_tcae_pi.pdf"),
        "destino": "2025-06-07_pi_plantilla-def.pdf",
    },
    {
        "id": "2025_aplazada_cuadernillo",
        "anio": 2025, "fecha": "2025-07-28", "modalidad": "aplazada",
        "tipo": "cuadernillo",
        "url": _sas("2025/tecnico_a_en_cuidados_auxiliares_de_enfermeria_prueba_aplazada.pdf"),
        "destino": "2025-07-28_aplazada_cuadernillo.pdf",
    },
    {
        "id": "2025_aplazada_plantilla_prov",
        "anio": 2025, "fecha": "2025-07-28", "modalidad": "aplazada",
        "tipo": "plantilla_prov",
        "url": _sas("2025/plantilla_respuestas_tecnico_a_en_cuidados_auxiliares_de_enfermeria_prueba_aplazada.pdf"),
        "destino": "2025-07-28_aplazada_plantilla-prov.pdf",
    },
    {
        "id": "2025_aplazada_plantilla_def",
        "anio": 2025, "fecha": "2025-07-28", "modalidad": "aplazada",
        "tipo": "plantilla_def",
        "url": _sas("2026/plantdef_tcae_def_l_aplazada.pdf"),
        "destino": "2025-07-28_aplazada_plantilla-def.pdf",
    },

    # ───────────────────────────── 2024 ─────────────────────────────
    # 10-feb-2024 (Centros SAS + APES extinguidas) + 29-abr-2024 aplazada.
    # OEP extraordinaria Decreto-ley 12/2022 · estabilización.
    # OJO: nombres internos de los PDF dicen "2023" (año del proceso); la
    # celebración real es 2024 y manda. Scribd: 75 preguntas + 3 de reserva.
    {
        "id": "2024_centros_cuadernillo",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "centros_sas",
        "tipo": "cuadernillo",
        "url": _sas("2024/20240210_57008_tcae.pdf"),
        "destino": "2024-02-10_centros-sas_cuadernillo.pdf",
    },
    {
        "id": "2024_centros_plantilla_prov",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "centros_sas",
        "tipo": "plantilla_prov",
        "url": _sas("2024/20240210_plantilla_respuestas_57008_tcae.pdf"),
        "destino": "2024-02-10_centros-sas_plantilla-prov.pdf",
    },
    {
        "id": "2024_centros_plantilla_def",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "centros_sas",
        "tipo": "plantilla_def",
        "url": _sas("2024/def_tcae_sas_2023.pdf"),
        "destino": "2024-02-10_centros-sas_plantilla-def.pdf",
    },
    {
        "id": "2024_apes_cuadernillo",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "apes",
        "tipo": "cuadernillo",
        "url": _sas("2024/20240210_57008_tcae_apes.pdf"),
        "destino": "2024-02-10_apes_cuadernillo.pdf",
    },
    {
        "id": "2024_apes_plantilla_prov",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "apes",
        "tipo": "plantilla_prov",
        "url": _sas("2024/20240210_plantilla_respuestas_57008_tcae_apes.pdf"),
        "destino": "2024-02-10_apes_plantilla-prov.pdf",
    },
    {
        "id": "2024_apes_plantilla_def",
        "anio": 2024, "fecha": "2024-02-10", "modalidad": "apes",
        "tipo": "plantilla_def",
        "url": _sas("2024/def_tcae_agencias_2023.pdf"),
        "destino": "2024-02-10_apes_plantilla-def.pdf",
    },
    {
        "id": "2024_aplazada_cuadernillo",
        "anio": 2024, "fecha": "2024-04-29", "modalidad": "aplazada",
        "tipo": "cuadernillo",
        "url": _sas("2024/70006_tcae_prueba_aplazada.pdf"),
        "destino": "2024-04-29_aplazada_cuadernillo.pdf",
    },
    {
        "id": "2024_aplazada_plantilla_prov",
        "anio": 2024, "fecha": "2024-04-29", "modalidad": "aplazada",
        "tipo": "plantilla_prov",
        "url": _sas("2024/plantilla_prov_aplazada_tcae_2023.pdf"),
        "destino": "2024-04-29_aplazada_plantilla-prov.pdf",
    },
    {
        "id": "2024_aplazada_plantilla_def",
        "anio": 2024, "fecha": "2024-04-29", "modalidad": "aplazada",
        "tipo": "plantilla_def",
        "url": _sas("2024/def_tcae_aplazada_sas_2023.pdf"),
        "destino": "2024-04-29_aplazada_plantilla-def.pdf",
    },

    # ───────────────────────────── 2022 ─────────────────────────────
    # 3-abr-2022 · llamamiento aplazado del acceso libre OEP 2021-22.
    {
        "id": "2022_aplazada_cuadernillo",
        "anio": 2022, "fecha": "2022-04-03", "modalidad": "aplazada",
        "tipo": "cuadernillo",
        "url": _sas("2022/Cuadernillo_TCAE_Aplazado.pdf"),
        "destino": "2022-04-03_aplazada_cuadernillo.pdf",
    },
    {
        "id": "2022_aplazada_plantilla_prov",
        "anio": 2022, "fecha": "2022-04-03", "modalidad": "aplazada",
        "tipo": "plantilla_prov",
        "url": _sas("2022/Plantilla_respuestas_TCAE_Aplazado.pdf"),
        "destino": "2022-04-03_aplazada_plantilla-prov.pdf",
    },
    {
        "id": "2022_aplazada_plantilla_def",
        "anio": 2022, "fecha": "2022-04-03", "modalidad": "aplazada",
        "tipo": "plantilla_def",
        "url": _sas("2022/def_plantilla_tcae_aplazado_l.pdf"),
        "destino": "2022-04-03_aplazada_plantilla-def.pdf",
    },

    # ───────────────────────────── 2021 ─────────────────────────────
    # 19-dic-2021 · libre + PI · OEP 2021-22 (ofertas 2018-2021).
    # Opoluz: 100 preguntas en el examen de acceso libre → el reglamento
    # de este año es distinto al de 2024/2025 (75). Ver FASE0_INVENTARIO.
    {
        "id": "2021_libre_cuadernillo",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "libre",
        "tipo": "cuadernillo",
        "url": _sas("2021/13001_tcae_libre.pdf"),
        "destino": "2021-12-19_libre_cuadernillo.pdf",
    },
    {
        "id": "2021_libre_plantilla_prov",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "libre",
        "tipo": "plantilla_prov",
        "url": _sas("2021/plantilla_respuestas_13001_tcae_li.pdf"),
        "destino": "2021-12-19_libre_plantilla-prov.pdf",
    },
    {
        "id": "2021_libre_plantilla_def",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "libre",
        "tipo": "plantilla_def",
        "url": _sas("2022/plantilla_respuestas_def13001_tcae_li.pdf"),
        "destino": "2021-12-19_libre_plantilla-def.pdf",
    },
    {
        "id": "2021_pi_cuadernillo",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "pi",
        "tipo": "cuadernillo",
        "url": _sas("2021/13002_tcae_pi.pdf"),
        "destino": "2021-12-19_pi_cuadernillo.pdf",
    },
    {
        "id": "2021_pi_plantilla_prov",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "pi",
        "tipo": "plantilla_prov",
        "url": _sas("2021/plantilla_respuestas_13002_tcae_pi.pdf"),
        "destino": "2021-12-19_pi_plantilla-prov.pdf",
    },
    {
        "id": "2021_pi_plantilla_def",
        "anio": 2021, "fecha": "2021-12-19", "modalidad": "pi",
        "tipo": "plantilla_def",
        "url": _sas("2022/plantilla_respuestas_def_13002_tcae_pi.pdf"),
        "destino": "2021-12-19_pi_plantilla-def.pdf",
    },

    # ───────────────────────────── 2019 ─────────────────────────────
    # 27-abr-2019 · libre + PI · OEP 2016-2017 y estabilización.
    # Denominación histórica en el cuadernillo: "Auxiliar de Enfermería".
    {
        "id": "2019_libre_cuadernillo",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "libre",
        "tipo": "cuadernillo",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190427_aux_enferm_examen_l.pdf"),
        "destino": "2019-04-27_libre_cuadernillo.pdf",
    },
    {
        "id": "2019_libre_fe_erratas",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "libre",
        "tipo": "fe_erratas",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190427_aux_enferm_examen_l_fe_de_erratas.pdf"),
        "destino": "2019-04-27_libre_fe-de-erratas.pdf",
    },
    {
        "id": "2019_libre_plantilla_prov",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "libre",
        "tipo": "plantilla_prov",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190427_aux_enferm_respuestas_l.pdf"),
        "destino": "2019-04-27_libre_plantilla-prov.pdf",
    },
    {
        "id": "2019_libre_plantilla_def",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "libre",
        "tipo": "plantilla_def",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190530_plantilla_def_aux_enf_l.pdf"),
        "destino": "2019-04-27_libre_plantilla-def.pdf",
    },
    {
        "id": "2019_pi_cuadernillo",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "pi",
        "tipo": "cuadernillo",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190427_aux_enferm_examen_p.pdf"),
        "destino": "2019-04-27_pi_cuadernillo.pdf",
    },
    {
        "id": "2019_pi_plantilla_prov",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "pi",
        "tipo": "plantilla_prov",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190427_aux_enferm_respuestas_p.pdf"),
        "destino": "2019-04-27_pi_plantilla-prov.pdf",
    },
    {
        "id": "2019_pi_plantilla_def",
        "anio": 2019, "fecha": "2019-04-27", "modalidad": "pi",
        "tipo": "plantilla_def",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/2017/20190530_plantilla_def_aux_enf_pi.pdf"),
        "destino": "2019-04-27_pi_plantilla-def.pdf",
    },

    # ───────────────────────────── 2016 ─────────────────────────────
    # 30-ene-2016 · libre + PI · OEP 2013-2015.
    # MAD rotula estos PDFs como "2015" (año de convocatoria); la celebración
    # real es 30-ene-2016 y manda. Hay plantilla_def + corrección posterior.
    {
        "id": "2016_libre_cuadernillo",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "libre",
        "tipo": "cuadernillo",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Examen_AE_L.pdf"),
        "destino": "2016-01-30_libre_cuadernillo.pdf",
    },
    {
        "id": "2016_libre_plantilla_prov",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "libre",
        "tipo": "plantilla_prov",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AE_L.pdf"),
        "destino": "2016-01-30_libre_plantilla-prov.pdf",
    },
    {
        "id": "2016_libre_plantilla_def",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "libre",
        "tipo": "plantilla_def",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AUX_ENF_L_D.pdf"),
        "destino": "2016-01-30_libre_plantilla-def.pdf",
    },
    {
        "id": "2016_libre_plantilla_corr",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "libre",
        "tipo": "plantilla_corr",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AUX_ENF_L_C.pdf"),
        "destino": "2016-01-30_libre_plantilla-corr.pdf",
    },
    {
        "id": "2016_pi_cuadernillo",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "pi",
        "tipo": "cuadernillo",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Examen_AE_PI.pdf"),
        "destino": "2016-01-30_pi_cuadernillo.pdf",
    },
    {
        "id": "2016_pi_plantilla_prov",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "pi",
        "tipo": "plantilla_prov",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AE_PI.pdf"),
        "destino": "2016-01-30_pi_plantilla-prov.pdf",
    },
    {
        "id": "2016_pi_plantilla_def",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "pi",
        "tipo": "plantilla_def",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AUX_ENF_PI_D.pdf"),
        "destino": "2016-01-30_pi_plantilla-def.pdf",
    },
    {
        "id": "2016_pi_plantilla_corr",
        "anio": 2016, "fecha": "2016-01-30", "modalidad": "pi",
        "tipo": "plantilla_corr",
        "url": _ws027("/contenidos/profesionales/seleccion/oep/plantillas/Respuestas_AUX_ENF_PI_C.pdf"),
        "destino": "2016-01-30_pi_plantilla-corr.pdf",
    },

    # ───────────────────────────── 2008 ─────────────────────────────
    # 30-nov-2008 · concurso-oposición · OEP 2004-2007 · proceso 6000.
    # Cadena de plantillas: inicial → corrección de errores → definitiva.
    {
        "id": "2008_cuadernillo",
        "anio": 2008, "fecha": "2008-11-30", "modalidad": "concurso",
        "tipo": "cuadernillo",
        "url": _ws027("../../contenidos/profesionales/OPE2007/resoluciones/Examen20081130_6000.pdf"),
        "destino": "2008-11-30_concurso_cuadernillo.pdf",
    },
    {
        "id": "2008_plantilla_inicial",
        "anio": 2008, "fecha": "2008-11-30", "modalidad": "concurso",
        "tipo": "plantilla_inicial",
        "url": _ws027("../../contenidos/profesionales/OPE2007/resoluciones/REx20081130_6000.pdf"),
        "destino": "2008-11-30_concurso_plantilla-inicial.pdf",
    },
    {
        "id": "2008_correccion",
        "anio": 2008, "fecha": "2008-11-30", "modalidad": "concurso",
        "tipo": "correccion",
        "url": _ws027("../../contenidos/profesionales/OPE2007/resoluciones/CEREx20081130_6000.pdf"),
        "destino": "2008-11-30_concurso_correccion-errores.pdf",
    },
    {
        "id": "2008_plantilla_def",
        "anio": 2008, "fecha": "2008-11-30", "modalidad": "concurso",
        "tipo": "plantilla_def",
        "url": _ws027("../../contenidos/profesionales/OPE2007/resoluciones/RExDef_6000.pdf"),
        "destino": "2008-11-30_concurso_plantilla-def.pdf",
    },
]

# Tipos que aportan la corrección válida, en orden de preferencia.
TIPOS_CORRECCION_VALIDOS = ("plantilla_corr", "correccion", "plantilla_def", "plantilla_inicial", "plantilla_prov")

# 2008 queda ARCHIVADO (decisión de Jesús, 2026-09-22): su estructura
# (105 teórico + 3 supuestos prácticos A/B/C de 55) no es comparable con 2016+.
# Se conserva el PDF y el JSON crudo por trazabilidad, pero NO entra en el
# análisis de repetición ni en los modos de estudio.
ANIO_ARCHIVADO = 2008

if __name__ == "__main__":
    cuadernillos = [d for d in DOCUMENTOS if d["tipo"] == "cuadernillo"]
    print(f"Total documentos: {len(DOCUMENTOS)}")
    print(f"Cuadernillos:     {len(cuadernillos)}")
    print(f"Resto (plantillas, erratas, correcciones): {len(DOCUMENTOS) - len(cuadernillos)}")
    for d in cuadernillos:
        print(f"  {d['fecha']}  {d['modalidad']:<12}  {d['destino']}")
