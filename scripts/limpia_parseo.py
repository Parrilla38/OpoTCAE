"""Limpieza posterior al parseo: corrige los casos raros sin tocar parsear.py.

Corrige:
  1. Enunciados vacíos: el enunciado se coló en la última opción de la anterior.
  2. Enunciados que arrastran texto de portada/instrucciones (pregunta 1).
  3. Opciones vacías.

Uso: python scripts/limpia_parseo.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "parsed" / "preguntas.json"

RE_BASURA = re.compile(
    r"INSTRUCCIONES|CUADERNILLO|HOJA DE RESPUESTAS|ALEGACIONES|"
    r"TELEFONO M[ÓO]VIL|EXPULSI[ÓO]N|PRECINTO|ANOMAL[ÍI]A|"
    r"CONTIN[ÚU]A EN LA CONTRA|SOBRE LA FORMA DE|"
    r"Si desea un ejemplar|p[áa]gina web del Organismo|"
    r"LAS INSTRUCCIONES|SU TOTALIDAD AL FINALIZAR|"
    r"DEL PROCESO|ABRIR SOLAMENTE|TRIBUNAL|PERSONA RESPONSABLE|"
    r"prohibida la entrada|prohibido hablar|prohibido el uso|"
    r"incumplimiento de las instrucciones|expulsi[óo]n del proceso|"
    r"Compruebe que|no olvide firmarla|solo se calificar[áa]n|"
    r"tiempo de duraci[óo]n|dos horas|120 minutos|"
    r"rompa el precinto|solicite su sustituci[óo]n|"
    r"4 respuestas alternativas|siendo s[óo]lo una|"
    r"concurso-oposici[óo]n|plazas b[áa]sicas vacantes|"
    r"T[ÉE]CNICOS?/?A?S? EN CUIDADOS|AUXILIARES? DE ENFERMER|"
    r"EXAMEN APLAZADO|TURNO LIBRE|PROMOCI[ÓO]N INTERNA|"
    r"OEP \d{4}|CONCURSO-OPOSICI[ÓO]N",
    re.IGNORECASE,
)
# fragmentos sueltos que se pegan al inicio del enunciado al cortar páginas
RE_FRAGMENTO = re.compile(r"^[\s\.\,\;\:]*[a-záéíóúüñ]{1,3}\s+(?=[A-ZÁÉÍÓÚÜÑ¿¡])")


def recortar_portada(enunciado: str) -> str:
    # fragmentos sueltos pegados al inicio ("ia Según la Constitución...")
    enunciado = RE_FRAGMENTO.sub("", enunciado)
    if not RE_BASURA.search(enunciado):
        return enunciado
    # si hay un ¿ tras la basura, es el inicio real del enunciado
    pos = enunciado.find("?")
    if pos != -1:
        inicio = enunciado.rfind("¿", 0, pos + 1)
        if inicio != -1:
            return enunciado[inicio:].strip()
    # si no hay ¿, corta en la última basura
    cortes = list(RE_BASURA.finditer(enunciado))
    if cortes:
        return enunciado[cortes[-1].end():].strip()
    return enunciado


def recuperar_de_opcion_anterior(preguntas: list[dict], i: int) -> bool:
    """Si preguntas[i] tiene enunciado vacío, lo saca de la última opción de la anterior."""
    if i == 0 or preguntas[i]["enunciado"]:
        return False
    prev = preguntas[i - 1]
    for letra in ("D", "C", "B", "A"):
        opt = prev["opciones"].get(letra, "")
        if len(opt) >= 12 and (opt.endswith((":", "?", "¿")) or "?" in opt):
            # parte por el último ':' o '?' que parezca cierre de enunciado
            for sep in (":", "?"):
                p = opt.rfind(sep)
                if p >= 8:
                    prev["opciones"][letra] = opt[p + 1 :].strip()
                    preguntas[i]["enunciado"] = opt[: p + 1].strip()
                    return True
    return False


def main() -> int:
    preguntas = json.loads(SALIDA.read_text(encoding="utf-8"))
    arreglos = {"portada": 0, "enunciado_vacio": 0, "opcion_vacia": 0}
    problemas: list[str] = []

    for i, p in enumerate(preguntas):
        antes = p["enunciado"]
        p["enunciado"] = recortar_portada(p["enunciado"])
        if p["enunciado"] != antes:
            arreglos["portada"] += 1
        if not p["enunciado"] and recuperar_de_opcion_anterior(preguntas, i):
            arreglos["enunciado_vacio"] += 1
        for letra in "ABCD":
            if not p["opciones"].get(letra):
                arreglos["opcion_vacia"] += 1
                problemas.append(f"{p['id']}: opcion {letra} vacia")

    for p in preguntas:
        if len(p["enunciado"]) < 8:
            problemas.append(f"{p['id']}: enunciado corto/vacio ({p['enunciado']!r})")
        if not p["correcta"] and not p["anulada"]:
            problemas.append(f"{p['id']}: sin respuesta y no anulada")

    SALIDA.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"arreglos: {arreglos}")
    print(f"problemas restantes: {len(problemas)}")
    for x in problemas[:30]:
        print(f"  {x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
