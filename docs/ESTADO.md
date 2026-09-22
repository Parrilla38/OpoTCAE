# Proyecto TCAE — continuidad

Plataforma web gratuita para repasar lo que más se pregunta en los exámenes
oficiales de **TCAE del Servicio Andaluz de Salud** (Andalucía).

**En producción: <https://opotcae.vercel.app/>** · **Código: <https://github.com/Parrilla38/OpoTCAE>**

## Decisiones cerradas

| Decisión | Valor |
|---|---|
| Alcance | Los 29 temas del BOJA 153 + «Otros» (clínica, el temario no la enumera) |
| Uso | Gratuito y público, sin cuenta. Progreso en `localStorage` |
| Stack | **Vercel** + SPA estática (Vite / React / TS / Tailwind) |
| Matching | Literal (`radar.py`) + semántico (`semantico.py`) |
| 2008 | Archivado (estructura no comparable) |
| **UX** | **Lo más fácil posible. Sin jerga, una acción obvia por pantalla, lo avanzado desplegado** |
| Ley 37/2007 | Descartada por Jesús: material público, proyecto gratuito |
| «Otros» (anatomía y clínica) | Se queda como bucket propio, sin inventar tema oficial |

## Estado por fase

| Fase | Contenido | Estado |
|---|---|---|
| 0 | Inventario y extracción de 45 PDFs | ✅ `docs/FASE0_INVENTARIO.md` |
| 1 | Parseo, clustering literal y radar | ✅ **validado por Jesús** |
| 2 | MVP web con los modos de estudio | ✅ desplegado |
| 3 | Matching semántico, heatmap, simulacro, SM-2, tarjetas | ✅ |
| 4 | Multiusuario y stats agregadas | ⬜ solo si el uso lo justifica |
| 5 | Los 29 temas + pasada de UX | ✅ |
| — | **Pasada de UX seria** | ✅ |
| — | Cierre de anomalías, T13, heatmap e impresión recuperados | ✅ |

## Hallazgos clave (no olvidar)

1. **El reglamento cambió**: 150 preguntas (2016-2022) → 75 (2024-2025). Reservas siempre 151-153.
2. **2008 es distinto**: 105 teórico + 3 supuestos × 55. Archivado.
3. **La repetición *literal* entre años es casi nula** (1 de 166 en el bloque común). Lo que se repite es el **artículo y el concepto**.
4. **El matching semántico lo confirma**: 486 conceptos con ≥2 formulaciones, **123 en ≥2 años** (frente a 3 del match literal).
5. **La Constitución es un nicho**: 9 preguntas en todo el corpus.
6. **El examen pregunta anatomía, fisiología, farmacología y obstetricia**, que el temario oficial de 29 temas **no enumera** (es contenido implícito del título FP). Van en el bucket «Otros» para no inventar temas.

## Datos

| Qué | Dónde |
|---|---|
| Dataset curado | `data/parsed/{preguntas,clusters,clusters_semanticos}.json` |
| PDFs oficiales (no en git) | `data/pdfs/` — `python scripts/descargar.py` |
| Informes | `docs/{FASE0_INVENTARIO,RADAR_BLOQUE_COMUN,SEMANTICO,VALIDACION_BLOQUE_COMUN}.md` |
| JSON que sirve la web | `web/public/data/` |

Cifras actuales: **1.504 preguntas** · **902 clústeres** · **486 conceptos** ·
**13 convocatorias** (2016-2025) · **28 temas del BOJA** cubiertos.

## Pipeline reproducible

```bash
pip install -r requirements.txt
python scripts/descargar.py        # 45 PDFs -> data/pdfs/
python scripts/extraer_pdf.py      # -> data/raw/*.json
python scripts/parsear.py          # -> data/parsed/preguntas.json
python scripts/limpia_parseo.py    # corrige portadas y enunciados sueltos
python scripts/clasificar.py       # 29 temas + clínica
python scripts/radar.py            # clústeres literales + RADAR
python scripts/semantico.py        # clústeres semánticos + SEMANTICO.md
python scripts/exporta_web.py      # -> web/public/data/
```

`limpia_parseo.py` NO se debe correr dos veces sobre el mismo JSON (acumula
recortes). Para regenerar: empezar siempre por `parsear.py`.

## Web

```bash
cd web
npm install
npm run dev        # http://localhost:5173
npm run build      # -> web/dist
vercel --prod
```

## UX — principios que se deben respetar

Es la instrucción más importante de Jesús: **la plataforma debe ser lo más fácil
de usar posible**.

1. **Una acción obvia por pantalla.** Siempre hay un botón grande que dice qué hacer.
2. **Sin jerga.** Nada de «clúster», «score», «cohesión», «SM-2», «formulaciones». Se dice «lo que más se repite», «esto ya había caído».
3. **Progresivo.** Lo simple a la vista; lo avanzado bajo «Cambiar preguntas» / desplegables.
4. **Pocas decisiones** antes de empezar. El test arranca en un toque.
5. **Feedback inmediato.** Siempre se ve el progreso y el siguiente paso.
6. **Español llano.** Etiquetas cortas, verbos, sin tecnicismos.

Navegación actual (4 items): **Practicar · Aprender · Exámenes · Mi progreso**.

## Anomalías de Fase 0 — estado

| # | Anomalía | Estado |
|---|---|---|
| 1 | Cuadernillo 2025 libre+PI común | ✅ resuelta al parsear (corte por páginas 1-16 / 17-32) |
| 2 | Anuladas idénticas libre vs PI en **2019** (53, 73, 88, 139) | ✅ **CONTRASTE OK** — los enunciados y las opciones son idénticos. Es dato real del SAS, no copy-paste |
| 3 | Anuladas idénticas libre vs PI en **2021** (107, 109) | ✅ **CONTRASTE OK** — idem |
| 4 | Typo en la plantilla definitiva de 2016 | ✅ resuelta: se usa `plantilla_corr` |
| 5 | Plantilla prov. de APES inservible | ✅ resuelta: se usa la definitiva |
| 6 | Nombres internos de PDF engañosos | ✅ corregido en el manifiesto |
| 7 | 2008 con 3 supuestos distintos | ✅ **archivado** por decisión de Jesús |

Script de contraste: `python scripts/verifica_anomalias.py`

## T13 «Atención al usuario» — no se pregunta

Diagnóstico cerrado (2026-09-22). El tema sale con **0 preguntas** y **es correcto**:
el examen no lo evalúa.

De 56 preguntas que mencionan «atención», «usuario», «acogida» o «reclamaciones»
en el enunciado, **ninguna** encaja con el contenido del tema (carta de servicios,
quejas y sugerencias, acogida formal, satisfacción del usuario). Se van a T26
(salud mental), T29 (primeros auxilios) o clínica, donde pertenecen.

**Consecuencia de producto:** es información útil para quien oposita — el Tema 13
se puede estudiar a fondo bajo. Se puede mostrar en la UI como «prácticamente no
cae» si se quiere.

## Pendiente de Jesús

1. **Nombre y dominio** definitivos (hoy `opotcae.vercel.app`).
2. ~~Verificar la Ley 37/2007~~ — **descartado por Jesús (2026-09-22)**: material público de internet y el proyecto es gratuito.
3. ~~Anomalías 2 y 3~~ — **cerradas**: contraste OK, el dato es real.
4. **338 preguntas sin tema** asignado: decidir si se afinan reglas o se dejan en «Otros» (hoy en «Otros» por decisión de Jesús).
