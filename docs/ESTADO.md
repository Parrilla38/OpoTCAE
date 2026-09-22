# Proyecto TCAE — continuidad

Plataforma web para repasar las preguntas más repetidas en los exámenes oficiales
de **TCAE del Servicio Andaluz de Salud** (Andalucía), con foco inicial en la
**Constitución Española (Tema 1)**.

## Decisiones cerradas

| Decisión | Valor |
|---|---|
| Alcance v1 | Solo Constitución (Tema 1) |
| Uso | Gratuito y público (comunidad) |
| Stack | **Vercel** + SPA estática (Vite/React). Backend solo si llega Fase 4 |
| Análisis de repetición | Match exacto + normalización, con validación manual |
| Fuente de datos | Solo PDFs oficiales del SAS (no Opoluz, no MAD, no Wuolah) |
| Backend v1 | **Ninguno**: JSON estático + localStorage. Workers/D1 van en Fase 4 |

## Estado por fase

| Fase | Contenido | Estado |
|---|---|---|
| **0** | Inventario y extracción cruda | ✅ `docs/FASE0_INVENTARIO.md` |
| **1** | Bloque común (Temas 1-10): parseo, clústeres, radar | ✅ **VALIDADO por Jesús** |
| **2** | MVP plataforma (Modo Test / Modo Repaso / Últimos exámenes) | ✅ `web/` build OK, 54 KB gzip |
| **3** | Libreta de errores, heatmap, simulacro, flashcards | ⬜ pendiente |
| **4** | Multiusuario (Workers + D1), stats agregadas | ⬜ pendiente |
| **5** | Expansión a Temas 2-29 | ⬜ pendiente |

Regla: implementar la fase pedida, verificar, marcarla aquí y **PARAR**.
No saltar de fase sin confirmación.

## Hallazgos clave de Fase 0

- **El reglamento cambió**: 150 preguntas (2016-2022) → 75 preguntas (2024-2025). Reservas siempre numeradas 151-153.
- **2008 es distinto**: 105 teórico + 3 supuestos prácticos (A/B/C, 55 preguntas cada uno).
- **Ningún PDF necesita OCR**. 36/45 con texto completo, 9 con páginas de portada/cierre sin texto.
- **La Constitución es solo ≈2-5 % del cuestionario**. El valor del producto está en la profundidad del análisis, no en el volumen.
- **7 anomalías de datos** documentadas en `FASE0_INVENTARIO.md` §7. Fase 1 debe resolverlas antes de calcular frecuencias.

## Hallazgos clave de Fase 1

Datos: **1.539 preguntas** parseadas (2016-2025, sin 2008), 1.504 con respuesta,
35 anuladas, 10 incidencias menores (0,66 %). Bloque común: **166 preguntas**.

| Métrica | Valor |
|---|---|
| Preguntas de bloque común | 166 (11,0 %) |
| Clústeres generados | 120 |
| Clústeres repetidos | 43 |
| Clústeres multi-año (≥2 años) | **3** |
| Preguntas que se repiten ENTRE años (literal) | **1** |

**⚠️ HALLAZGO DE PRODUCTO — la repetición literal entre años es casi nula.**
Solo 1 pregunta del bloque común se repite idéntica en dos años distintos.
Las 43 «repeticiones» son en su mayoría **libre + PI del mismo año** (el SAS
reutiliza preguntas entre turnos), no reutilización interanual.

Lo que sí se repite es el **artículo / concepto**, no la redacción:
- Art. 47 Ley 2/1998 (Salud de Andalucía) — cae en 2019 y 2022 con distinta redacción
- Art. 55 Ley 14/1986 (LGS) — competencias de los Servicios de Salud
- Art. 1 y 10 CE — valores superiores y principios del orden político
- Art. 43 CE — derecho a la protección de la salud
- Biobanco del SSPA — 3 formulaciones distintas en 2016, 2019, 2021, 2022

**Consecuencia para la plataforma:**
- El **«Modo Repaso por artículo»** es la feature FUERTE: es donde está la señal.
- El **«Modo Test sobre las más repetidas»** debe construirse sobre frecuencia
  de **artículo/tema**, no de coincidencia literal de enunciado.
- Para captar repetición de **concepto** (misma pregunta con otras palabras)
  haría falta matching semántico (embeddings). Es candidato natural a Fase 3
  o a una fase nueva. Decisión pendiente de Jesús.

**Constitución (T01): 9 preguntas / 8 clústeres en todo el corpus.** Solo 1 se
repite («plazo para nombrar Presidente del Gobierno», art. 99 CE, 2024 libre+PI).
El radar de Constitución es, por volumen, **una herramienta nicho**.

**Reparto por tema (bloque común):**

| Tema | preguntas | % |
|---|---|---|
| T03 Organización sanitaria (I): SSPA | 43 | 25,9 % |
| T09 Autonomía del paciente | 32 | 19,3 % |
| T04 Consejería de Salud y SAS | 26 | 15,7 % |
| T06 Prevención de riesgos laborales | 19 | 11,4 % |
| T02 Estatuto de Autonomía | 9 | 5,4 % |
| T01 Constitución Española | 9 | 5,4 % |
| T08 Estatuto Marco | 10 | 6,0 % |
| T10 TIC en el SAS | 8 | 4,8 % |
| T05 Protección de datos | 7 | 4,2 % |
| T07 Igualdad y violencia de género | 3 | 1,8 % |

## Decisiones de Jesús (2026-09-22)

- **2008 se archiva**: fuera del análisis de repetición (estructura no comparable: 105 + 3 supuestos).
- **Producto gratuito y público**, sin nombre ni dominio todavía.
- **Fase 1 ampliada a Temas 1-10** (bloque común / legislación), no solo Constitución.

## Pipeline de Fase 1 (reproducible)

```bash
python scripts/parsear.py        # PDFs -> data/parsed/preguntas.json
python scripts/limpia_parseo.py  # corrige portadas, enunciados vacíos
python scripts/clasificar.py     # etiqueta Temas 1-10 vs específico
python scripts/radar.py          # clústeres + RADAR + VALIDACION
python scripts/exporta_web.py    # -> web/public/data/
```

`limpia_parseo.py` es idempotente sobre `parsear.py`, NO lo corras dos veces
sobre el mismo JSON (acumula recortes).

## Pendiente de Jesús

1. **Nombre y dominio** de la plataforma.
2. **Reutilización de los PDFs del SAS** (Ley 37/2007): verificar antes del deploy público. Medida conservadora actual: enlazar al original + atribución visible.
3. **Matching semántico** (embeddings): queda en **Fase 3** (decisión de Jesús, 2026-09-22).
4. **Anomalías 2 y 3 de Fase 0** (anuladas idénticas libre vs PI en 2019 y 2021): verificar comparando enunciados.

## Fase 2 — MVP lista para deploy

Stack: **Vite + React 18 + TypeScript + Tailwind 3** en `web/`. Sin backend.
Datos como JSON estático en `web/public/data/`, progreso en `localStorage`.

| Comprobación | Resultado |
|---|---|
| `tsc -b` (strict) | ✅ sin errores |
| `vite build` | ✅ 174 KB JS (54 KB gzip) + 28 KB CSS (5 KB gzip) |
| Integridad de datos | ✅ 166/166 preguntas con `cluster_id`, 0 `correcta` inválidas |
| `vite preview` | ✅ HTTP 200 en `/`, `/data/meta.json`, `/data/clusters.json` |

### Modos incluidos

1. **🎯 Modo Test** — configurable: 5/10/25/50 preguntas, banco (solo repetidas / todo el bloque / por tema / mis errores), penalización (0 · ¼ SAS · ⅓), cronómetro opcional. Muestreo **ponderado por score**: lo más repetido sale antes. Corrección con referencia de artículo y norma.
2. **📖 Modo Repaso** — temas ordenados por peso real → artículos ordenados por score → preguntas con año de aparición. Es la feature fuerte.
3. **🗓️ Últimos exámenes** — por año y convocatoria, con cada pregunta marcada como **«Nueva este año»** o **«Ya había caído»**.
4. **📕 Libreta de errores** — acumula fallos, sirve de filtro en el Modo Test.
5. **📊 Stats** — nota media, dominio por tema, últimos intentos. Todo local.

Extras: modo oscuro, PWA instalable, responsive móvil-first, atribución al SAS visible.

### Deploy a Vercel

Decisionó Jesús (2026-09-22): **Vercel**, no Cloudflare Pages. Para la v1 (SPA
estática sin backend) es equivalente y más simple. El backend de Fase 4 si se
hace, será con Vercel Functions + almacenamiento de Vercel (no Workers+D1).

```bash
cd web
npm i -g vercel          # una vez
npm run build
vercel --prod            # o conectar el repo en vercel.com y se auto-deploya
```

`web/vercel.json` ya fija: `framework: vite`, `outputDirectory: dist`, fallback
SPA, caché inmutable para `/assets/` y revalidable para `/data/*.json`.

PENDIENTE: crear el proyecto en Vercel, elegir dominio, y **verificar la
reutilización de los PDFs del SAS (Ley 37/2007)** antes de hacerlo público.

## Comandos

```bash
cd "Proyecto tcae"
python scripts/descargar.py        # 45 PDFs -> data/pdfs/
python scripts/extraer_pdf.py      # PDF -> data/raw/*.json
python scripts/conteo.py           # preguntas y plantillas
python scripts/menciones.py        # menciones de Constitución
python scripts/estima_ce.py        # estimación de peso de CE
python scripts/muestra.py <id> [n] # volcado de una página
```

Dependencias: `pypdf`, `fontTools`.
