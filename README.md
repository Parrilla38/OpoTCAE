# OpoTCAE · Lo que más se repite en los exámenes de TCAE (Andalucía)

Plataforma gratuita para repasar las preguntas del bloque común (Temas 1-10) de
los **exámenes oficiales de TCAE del Servicio Andaluz de Salud**, analizando
qué artículos y conceptos son los que de verdad se repiten convocatoria tras
convocatoria.

Sin cuenta, sin cookies de seguimiento, sin muros de pago. El progreso se queda
en tu navegador.

---

## El hallazgo que ordena todo el proyecto

Se analizaron **1.539 preguntas** de las convocatorias oficiales de **2016 a
2025** (2008 queda archivado: estructura no comparable). Del bloque común salen
**166 preguntas** agrupadas en **120 clústeres**.

> **La repetición *literal* entre años es casi nula: 1 sola pregunta de 166.**

Las 43 «repeticiones» del corpus son en su mayoría **libre + promoción interna
del mismo año** (el SAS reutiliza preguntas entre turnos), no reutilización
interanual.

Lo que sí se repite es el **artículo y el concepto**, no la redacción:

| Señal | Ejemplo |
|---|---|
| Art. 47 Ley 2/1998 (Salud de Andalucía) | cae en 2019 y 2022 con redacciones distintas |
| Art. 55 Ley 14/1986 (LGS) | competencias de los Servicios de Salud |
| Arts. 1, 10 y 43 CE | valores superiores, principios del orden político, derecho a la salud |
| Biobanco del SSPA | 4 formulaciones distintas en 2016, 2019, 2021 y 2022 |

De ahí que la herramienta principal sea el **Modo Repaso por artículos**, y que
el Modo Test muestree ponderado por peso de artículo/tema y no por coincidencia
literal de enunciado.

---

## Modos de estudio

| Modo | Qué hace |
|---|---|
| **🎯 Test** | 5 / 10 / 25 / 50 preguntas. Banco filtrable: solo repetidas, todo el bloque, por tema, o mis errores. Penalización configurable (0 · ¼ como el SAS · ⅓). Cronómetro opcional. Muestreo ponderado por score. Corrección con referencia de artículo y norma. |
| **📖 Repaso** | Temas ordenados por peso real en el examen → artículos ordenados por score → preguntas con su año de aparición. |
| **🗓️ Exámenes** | Por año y convocatoria. Cada pregunta va marcada como **«Nueva este año»** o **«Ya había caído»**. |
| **📕 Errores** | Libreta que acumula tus fallos y sirve de filtro en el Modo Test. |
| **📊 Stats** | Nota media, dominio por tema, últimos intentos. Todo local. |

Extras: modo oscuro, PWA instalable, diseño móvil-first.

---

## Cómo se calcula el «score» de repetición

```
score = frecuencia × (1 + 0,25 × años_diferentes)
```

Se prioriza la **persistencia multi-año** sobre la frecuencia cruda: una
pregunta que cae cuatro veces en dos años pesa más que otra que cae cuatro
veces en un solo año (libre + PI + aplazadas).

---

## Estructura

```
data/
  parsed/      dataset curado: preguntas.json, clusters.json  ← el corazón
scripts/       pipeline de extracción y análisis (Python)
docs/          inventario, radar y validación
web/           SPA (Vite + React + TypeScript + Tailwind)
```

## Reproducir el análisis

Necesita Python 3.11+ con `pypdf` y `fontTools`.

```bash
python scripts/descargar.py        # 45 PDFs oficiales del SAS -> data/pdfs/
python scripts/extraer_pdf.py      # PDF -> data/raw/*.json
python scripts/parsear.py          # -> data/parsed/preguntas.json
python scripts/limpia_parseo.py    # corrige portadas y enunciados sueltos
python scripts/clasificar.py       # etiqueta Temas 1-10 vs específico
python scripts/radar.py            # clústeres + RADAR + VALIDACION
python scripts/exporta_web.py      # -> web/public/data/
```

`limpia_parseo.py` es idempotente sobre `parsear.py`, pero **no lo corras dos
veces sobre el mismo JSON** (acumula recortes). Para regenerar desde cero,
empieza siempre por `parsear.py`.

## Correr la web

```bash
cd web
npm install
npm run dev        # http://localhost:5173
npm run build      # genera web/dist
```

## Desplegar en Vercel

```bash
cd web
npm i -g vercel
vercel --prod
```

`web/vercel.json` ya fija `framework: vite`, `outputDirectory: dist`, fallback
SPA y cabeceras de caché.

---

## Fuente de los datos y atribución

Los cuadernillos y las plantillas de respuestas proceden del **Servicio Andaluz
de Salud (Junta de Andalucía)**, publicados en su web institucional
(`sspa.juntadeandalucia.es`). Este proyecto es una **transcripción con fines de
estudio** y siempre enlaza y atribuye al original.

> **Aviso legal.** La reutilización de los documentos del sector público se rige
> por la Ley 37/2007. **Este punto está pendiente de verificación** antes de
> considerar el proyecto plenamente publicado. Mientras tanto, el repositorio
> **no redistribuye los PDFs oficiales**: se re-descargan con
> `python scripts/descargar.py`. Consulte siempre el original en la web del SAS.

### Convocatorias analizadas

| Año | Fecha | Modalidad | Preguntas |
|---|---|---|---|
| 2025 | 07-06 | libre + PI (común) | 75 + 75 |
| 2025 | 28-07 | aplazada | 75 |
| 2024 | 10-02 | Centros SAS | 75 |
| 2024 | 10-02 | APES extinguidas | 75 |
| 2024 | 29-04 | aplazada | 75 |
| 2022 | 03-04 | aplazada | 150 |
| 2021 | 19-12 | libre | 150 |
| 2021 | 19-12 | promoción interna | 150 |
| 2019 | 27-04 | libre | 150 |
| 2019 | 27-04 | promoción interna | 150 |
| 2016 | 30-01 | libre | 150 |
| 2016 | 30-01 | promoción interna | 150 |

El reglamento cambió: **150 preguntas en 2016-2022 → 75 en 2024-2025**. Las
3 preguntas de reserva siempre se numeran 151-153. 2008 (105 teórico + 3
supuestos prácticos de 55) queda archivado por no ser comparable.

---

## Estado y hoja de ruta

- [x] **Fase 0** — inventario y extracción de 45 PDFs oficiales
- [x] **Fase 1** — parseo, clasificación por tema, clustering y radar del bloque común
- [x] **Fase 2** — MVP web con los cinco modos
- [ ] **Fase 3** — repetición espaciada, heatmap, simulacro cronometrado, flashcards y *matching* semántico para repetición de concepto
- [ ] **Fase 4** — multiusuario y estadísticas agregadas (solo si el uso lo justifica)
- [ ] **Fase 5** — expansión a los Temas 11-29 (bloque específico)

Pendiente: nombre y dominio definitivos, y verificación de la Ley 37/2007.
