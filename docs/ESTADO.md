# OpoTCAE — continuidad

Plataforma web gratuita para repasar lo que más se pregunta en los exámenes
oficiales de **TCAE del Servicio Andaluz de Salud** (Andalucía).

**Nombre: OpoTCAE** · **Dominio: <https://opotcae.vercel.app/>** (decidido por
Jesús, 2026-09-22) · **Código: <https://github.com/Parrilla38/OpoTCAE>**

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
| Nombre y dominio | **OpoTCAE** en `opotcae.vercel.app` |
| **Estilo visual** | **Patio Blanco** (decidido por Jesús, 2026-09-22) |

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
| — | Rediseño visual (maquetas → Patio Blanco) | ✅ |

## Estilo visual — Patio Blanco

Se exploraron cuatro direcciones en `web/public/maquetas.html` (**A Alhambra**,
**B Azulejo**, **C Áureo**, **D Patio Blanco**) y Jesús eligió **D**.

Carácter del sistema, que hay que respetar al tocar la UI:

- **Paleta**: blanco cal `#FFFFFF`, superficie `#F6F8F6`, tinta `#14261C`,
  suave `#3F7A5C`, hilo `#DDE6DF`, verde de bandera `#0F5132`, agua de verde
  `#E7F0E9`, mal `#C2453B`. En oscuro se oscurece todo menos el verde, que se
  aclara a `#5FA875` para no perder contraste.
- **Tipografía**: Familjen Grotesk para texto (tracking ligeramente negativo) e
  IBM Plex Mono para etiquetas, cifras y numerales. Las etiquetas van en mono,
  versalitas y `letter-spacing: 0.28em`.
- **Radios deliberados**: acción 14px, tarjeta 18px, opción 12px, pastilla 16px.
  Nada de `rounded-2xl` por defecto.
- **Ornamento mínimo**: el sello de 4 cuadrados verde/blanco es el único guiño a
  Andalucía. Filetes de 1px, cero sombras marcadas, cero degradados.
- **Estados**: acierto = agua de verde con borde verde; fallo = agua de mal con
  borde mal. Solo cambian fondo y disco de la letra, no la forma.
- **Navegación inferior**: pastilla con 4 botones dentro; el activo se ilumina con
  el color de fondo y una sombra mínima.

**Contra el aspecto «hecho por IA»**: tipografías con carácter en vez de Inter,
cero emoji como iconos, cero degradados, paleta corta de 7 valores, y estados que
diferencian por color sin cambiar la geometría.

Para cambiar algo de estilo, empezar por las variables de `web/src/index.css`
(`:root` y `.dark`) y por los bloques `@layer components`. El resto de la UI se
construye con esas clases (`etiqueta`, `sello`, `accion-uno`, `accion-dos`,
`tarjeta`, `op` / `op-ok` / `op-mal`, `boton-*`, `chip-*`, `campo`, `fila`,
`pie-*`, `pestanas`, `filete`).

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

1. ~~Nombre y dominio~~ — **cerrado**: OpoTCAE en `opotcae.vercel.app`.
2. ~~Verificar la Ley 37/2007~~ — **descartado por Jesús**: material público, proyecto gratuito.
3. ~~Anomalías 2 y 3~~ — **cerradas**: contraste OK, el dato es real.
4. **338 preguntas sin tema** asignado: hoy en «Otros» por decisión de Jesús.

Lo único abierto es la **Fase 4** (multiusuario y estadísticas agregadas), y solo
si el uso real lo justifica.

## Limpieza de 2026-09-22 (post-Fase 5)

Se cierra la cola de «qué queda por hacer»:

| Qué | Estado |
|---|---|
| **Licencia** | ✅ `LICENSE` con MIT para código y documentación, y nota aparte sobre el contenido de examen atribuido al SAS |
| **Peso al entrar** | ✅ carga diferida: `meta.json` + `examenes.json` (26 KB) al abrir, `clusters.json` al usar Practicar/Aprender/Progreso, `preguntas.json` solo en Exámenes, `conceptos.json` solo al abrir esa pestaña |
| **SEO** | ✅ `index.html` con contenido estático real (H1/H2 con palabras clave, lista de los temas más pesados, el hallazgo de la repetición), JSON-LD `WebApplication`, Open Graph, `sitemap.xml`, `robots.txt`, canónica |
| **Runbook** | ✅ `docs/RUNBOOK.md`: cómo añadir una convocatoria nueva, cómo rehacer el análisis, cómo arreglar clasificación y parseo |
| **Tests del pipeline** | ✅ `tests/test_pipeline.py`, **52 tests**: regresión del clasificador (31 casos con tema esperado), parser de los 4 formatos, y contrato de los JSON exportados |
| **Offline** | ✅ `public/sw.js` con cache-first para el shell y stale-while-revalidate para `/data/`. Se registra solo en producción |
| **Iconos PWA** | ✅ `icono-192.png` y `icono-512.png` generados desde el SVG con `web/scripts/genera-iconos.mjs` |
| **T13 marcado** | ✅ los 29 temas oficiales salen siempre en la lista; si no han caído se muestran atenuados con «Prácticamente no cae» |
| **Precisión por tema** | ✅ revisada sobre muestra. T22 (89) y T24 (84) están limpios; T25 tenía fugas hacia T21/T19 por `cateterismo` a secas, ya acotado y con test |

**Bug real encontrado por los tests**: el cajón de clínica (T30) se había puesto
a robar de T14 («principio bioético de justicia») porque llevaba esa frase entre
sus palabras clave. Los tests lo cazaron al primer `pytest`. T30 ahora solo
contiene material que no pertenece a ningún tema oficial.
