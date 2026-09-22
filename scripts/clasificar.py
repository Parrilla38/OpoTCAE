"""Clasificador por tema del temario oficial TCAE SAS (Res. 31-jul-2024, BOJA 153).

Bloque COMÚN (Temas 1-10):
  1  Constitución Española de 1978
  2  Estatuto de Autonomía para Andalucía
  3  Organización sanitaria (I): sistema sanitario público de Andalucía
  4  Organización sanitaria (II): Consejería de Salud y SAS
  5  Protección de datos y transparencia
  6  Prevención de riesgos laborales
  7  Igualdad y contra la violencia de género en Andalucía
  8  Estatuto Marco del personal estatutario
  9  Autonomía del paciente y derechos y deberes
 10  TIC en el SAS

Bloque ESPECÍFICO = Temas 11-29 (se marca como 'especifico'; el detalle por
tema se hace en Fase 5).

El etiquetado es POR PALABRAS CLAVE con prioridad (lo más específico primero).
Es una primera pasada: el dump de validación es para que Jesús lo revise.

Uso: python scripts/clasificar.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "parsed" / "preguntas.json"

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

# (tema, regex) — se evalúan en orden; gana el primero que encaje.
# El orden prioriza lo MÁS específico: si una pregunta menciona el Estatuto
# Marco y la LGS, manda el Estatuto Marco (Tema 8).
REGLAS: list[tuple[int, re.Pattern]] = [
    # ── Tema 10 · TIC SAS (lo más específico, se evalúa antes) ──
    (10, re.compile(
        r"\bDAH[- ]?ECC\b|\bDAH[- ]?EXT\b|\bDAH[- ]?EG\b|\bHSAP\b|\bDiraya\b|"
        r"historia de salud digital|aplicaci[óo]n.*hospitalariamente.*datos cl[íi]nicos|"
        r"expediente cl[íi]nico electr[óo]nico|receta electr[óo]nica|"
        r"telemedicina|teleasistencia sanitaria|"
        r"tecnolog[íi]as? de la informaci[óo]n y la comunicaci[óo]n",
        re.I)),

    # ── Tema 5 · Protección de datos y transparencia ──
    (5, re.compile(
        r"protecci[óo]n de datos|LOPDGDD|LOPD|RGPD|"
        r"Reglamento \(UE\) 2016/679|ley org[áa]nica 3/2018|"
        r"agencia espa[ñn]ola de protecci[óo]n de datos|"
        r"datos de car[áa]cter personal|consentimiento.*datos|"
        r"derecho de acceso.*datos|derecho de rectificaci[óo]n|"
        r"derecho de supresi[óo]n|derecho al olvido|"
        r"transparencia.*informaci[óo]n p[úu]blica|"
        r"ley 19/2013|portal de transparencia",
        re.I)),

    # ── Tema 6 · Prevención de riesgos laborales ──
    (6, re.compile(
        r"prevenci[óo]n de riesgos laborales|ley 31/1995|"
        r"riesgo laboral|riesgos laborales|"
        r"inspecci[óo]n de trabajo|instituto nacional de seguridad e higiene|"
        r"servicio de prevenci[óo]n|t[ée]cnico superior en prevenci[óo]n|"
        r"mutua.*acci[óo]n social|acci[óo]n preventiva|"
        r"evaluaci[óo]n de riesgos|plan de prevenci[óo]n|"
        r"ergonom[íi]a|psicosociolog[íi]a aplicada|higiene industrial|"
        r"seguridad y salud en el trabajo|riesgo psicosocial|"
        r"acoso laboral|estr[ée]s laboral|burnout|s[íi]ndrome de desgaste",
        re.I)),

    # ── Tema 7 · Igualdad y violencia de género ──
    (7, re.compile(
        r"violencia de g[ée]nero|ley 13/2007|ley org[áa]nica 1/2004|"
        r"ley org[áa]nica 3/2007|ley 12/2007|"
        r"igualdad de g[ée]nero|igualdad de trato|igualdad efectiva|"
        r"discriminaci[óo]n por raz[óo]n de sexo|"
        r"plan andaluz.*igualdad|perspectiva de g[ée]nero|"
        r"violencia de g[ée]nero en andaluc[íi]a|"
        r"unidad de valoraci[óo]n.*g[ée]nero|"
        r"protocolo.*acoso.*sexual|acoso sexual",
        re.I)),

    # ── Tema 8 · Estatuto Marco / personal estatutario ──
    (8, re.compile(
        r"estatuto marco|ley 55/2003|"
        r"personal estatutario|estatutario fijo|estatutario temporal|"
        r"promoci[óo]n interna|provisi[óo]n de puestos|movilidad voluntaria|"
        r"situaciones administrativas|servicios especiales|excedencia|"
        r"trienios|r[ée]tribuciones b[áa]sicas|complemento de destino|"
        r"r[ée]gimen disciplinario|faltas leves|faltas graves|faltas muy graves|"
        r"ley 55/2003|LOPS|ley 44/2003|profesiones sanitarias|"
        r"colegios profesionales|ley 44/2003 de ordenaci[óo]n|"
        r"EBEP|ley 7/2007.*empleado p[úu]blico|"
        r"funcionario|empleados p[úu]blicos|"
        r"incompatibilidades|r[ée]gimen de incompatibilidades",
        re.I)),

    # ── Tema 9 · Autonomía del paciente ──
    (9, re.compile(
        r"autonom[íi]a del paciente|ley 41/2002|"
        r"consentimiento informado|consentimiento por representaci[óo]n|"
        r"instrucciones previas|voluntades anticipadas|testamento vital|"
        r"historia cl[íi]nica|documentaci[óo]n cl[íi]nica|"
        r"derechos del paciente|carta de derechos|"
        r"derecho a la informaci[óo]n asistencial|"
        r"revocar.*consentimiento|"
        r"confidencialidad.*paciente|secreto profesional.*paciente|"
        r"intimidad del paciente|dignidad del paciente",
        re.I)),

    # ── Tema 2 · Estatuto de Autonomía de Andalucía ──
    (2, re.compile(
        r"estatuto de autonom[íi]a|ley org[áa]nica 2/2007|"
        r"parlamento de andaluc[íi]a|consejo de gobierno de la junta|"
        r"presidente de la junta de andaluc[íi]a|junta de andaluc[íi]a|"
        r"defensor del pueblo andaluz|"
        r"tribunal de cuentas de andaluc[íi]a|"
        r"diputaciones provinciales|"
        r"competencias exclusivas de andaluc[íi]a|"
        r"art[íi]?c?u?l?o?\s*\.?\s*\d+.*estatuto de autonom|"
        r"estatuto de autonom.*art[íi]?c?u?l?o?\s*\.?\s*\d+|"
        r"s[íi]mbolos de andaluc[íi]a|d[íi]a de andaluc[íi]a|"
        r"escudo de andaluc[íi]a|himno de andaluc[íi]a|"
        r"bandera de andaluc[íi]a",
        re.I)),

    # ── Tema 3 · Organización sanitaria (I): SSPA ──
    (3, re.compile(
        r"sistema sanitario p[úu]blico de andaluc[íi]a|\bSSPA\b|"
        r"ley 2/1998|ley de salud de andaluc[íi]a|"
        r"plan andaluz de salud|"
        r"[áa]reas de gesti[óo]n sanitaria|[áa]reas de salud|"
        r"zonas b[áa]sicas de salud|"
        r"sistema nacional de salud|\bSNS\b|"
        r"ley 14/1986|ley general de sanidad|"
        r"ley 16/2003|cohesi[óo]n y calidad del SNS|"
        r"consejo interterritorial|"
        r"principios.*universalidad|principios.*generalidad|"
        r"financiaci[óo]n.*servicios sanitarios|"
        r"biobanco del sistema sanitario|centros.*investigaci[óo]n biom[ée]dica|"
        r"ley 14/2007.*investigaci[óo]n biom[ée]dica",
        re.I)),

    # ── Tema 4 · Organización sanitaria (II): Consejería y SAS ──
    (4, re.compile(
        r"servicio andaluz de salud|\bSAS\b|"
        r"consejer[íi]a de salud|consejer[íi]a de salud y familias|"
        r"consejer[íi]a de salud y consumo|"
        r"direcci[óo]n gerencia|direcciones gerencias|"
        r"atenci[óo]n primaria de salud|centro de salud|"
        r"unidades de gesti[óo]n cl[íi]nica|\bUGC\b|"
        r"hospital.*servicio andaluz|"
        r"ley 8/1986.*servicio andaluz|"
        r"agencia p[úu]blica empresarial|agencia administrativa|"
        r"consejo andaluz de salud|foro marco para el di[áa]logo social|"
        r"cartera de servicios|"
        r"[áa]reas de gesti[óo]n sanitaria.*depend|"
        r"direcci[óo]n de salud|direcci[óo]n m[ée]dica|"
        r"comisi[óo]n de direcci[óo]n",
        re.I)),

    # ── Tema 1 · Constitución Española ──
    (1, re.compile(
        r"constituci[óo]n espa[ñn]ola|constituci[óo]n de 1978|\bCE\b|"
        r"cortes generales|congreso de los diputados|"
        r"tribunal constitucional|tribunal supremo|"
        r"consejo general del poder judicial|poder judicial|"
        r"defensor del pueblo|tribunal de cuentas|consejo de estado|"
        r"presidente del gobierno|presidente del gobierno de la naci[óo]n|"
        r"soberan[íi]a nacional|forma pol[íi]tica del estado|"
        r"monarqu[íi]a parlamentaria|"
        r"valores superiores.*ordenamiento|"
        r"art[íi]?c?u?l?o?\s*\.?\s*1\.1|art[íi]?c?u?l?o?\s*\.?\s*1\.2|"
        r"derechos fundamentales|libertades p[úu]blicas|"
        r"garant[íi]as.*derechos|recurso de amparo|"
        r"estado de alarma|estado de excepci[óo]n|estado de sitio|"
        r"procedimiento de reforma|reforma constitucional|"
        r"t[íi]tulo preliminar|"
        r"principio de legalidad|jerarqu[íi]a normativa|"
        r"irretroactividad de las disposiciones sancionadoras|"
        r"seguridad jur[íi]dica|responsabilidad del estado|"
        r"inconstitucionalidad|"
        r"partidos pol[íi]ticos|sindicatos|organizaciones empresariales|"
        r"sucesi[óo]n a la corona|regencia|refrendo",
        re.I)),
]


def clasificar(texto: str) -> tuple[int | None, str]:
    """Devuelve (tema, bloque). tema=None si es específico u otro."""
    for tema, patron in REGLAS:
        if patron.search(texto):
            return tema, "comun"
    return None, "especifico"


def main() -> int:
    preguntas = json.loads(SALIDA.read_text(encoding="utf-8"))
    conteo: dict[str, int] = {}
    for p in preguntas:
        if p.get("anulada"):
            p["tema"] = None
            p["bloque"] = "anulada"
            p["tema_nombre"] = None
            continue
        # PRIMERO solo el enunciado: si las opciones entran en juego, una
        # opción que mencione "estatuto" clasifica como T02 una pregunta de
        # la LGS. El enunciado es la señal fuerte; las opciones, la débil.
        tema, bloque = clasificar(p["enunciado"])
        if tema is None:
            tema, bloque = clasificar(
                f"{p['enunciado']} {' '.join(p['opciones'].values())}"
            )
        p["tema"] = tema
        p["bloque"] = bloque
        p["tema_nombre"] = TEMAS.get(tema) if tema else None
        clave = f"T{tema:02d}" if tema else "especifico"
        conteo[clave] = conteo.get(clave, 0) + 1

    SALIDA.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Clasificación por tema (preguntas no anuladas)")
    print("-" * 50)
    for clave in sorted(conteo, key=lambda k: (k == "especifico", k)):
        nombre = TEMAS.get(int(clave[1:]), "Temas 11-29 (específico)") if clave != "especifico" else "Temas 11-29 (específico)"
        print(f"  {clave:<12} {conteo[clave]:>5}  {nombre}")
    print("-" * 50)
    total = sum(conteo.values())
    comun = sum(v for k, v in conteo.items() if k != "especifico")
    print(f"  {'TOTAL':<12} {total:>5}")
    print(f"  bloque común   {comun:>5}  ({100*comun/total:.1f}%)")
    print(f"  específico     {conteo.get('especifico', 0):>5}  ({100*conteo.get('especifico', 0)/total:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
