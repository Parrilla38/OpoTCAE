# Fase 0 — Inventario de exámenes TCAE SAS

**Estado**: ✅ COMPLETADA
**Fecha**: 2026-09-22
**Siguiente**: Fase 1 — Constitución: normalización, clústeres y radar (`RADAR_CONSTITUCION.md`)

Fuente única: **Servicio Andaluz de Salud** (`sspa.juntadeandalucia.es` y archivo histórico `ws027.sspa.juntadeandalucia.es`).
Índice de verificación cruzada: [Opoluz · exámenes TCAE SAS](https://opoluz.com/examenes-oficiales/sas/tcae/).
Atribución obligatoria en cualquier superficie pública: *Cuadernillos y plantillas oficiales del Servicio Andaluz de Salud (Junta de Andalucía)*.

---

## 1. Resultado de la descarga

| Métrica | Valor |
|---|---|
| Documentos en el manifiesto | **45** |
| Descargados con éxito | **45** (0 errores) |
| Cuadernillos | **13** |
| Plantillas / erratas / correcciones | **32** |
| Peso total en `data/pdfs/` | **10,39 MB** |
| JSON crudos en `data/raw/` | 45 + 1 informe |

Manifiesto canónico: `scripts/manifiesto.py`.
Descarga idempotente: `python scripts/descargar.py` (`--force` para re-descargar).

## 2. Calidad de extracción de texto

| Estado | Docs | Significado |
|---|---|---|
| `texto_completo` | **36** | todas las páginas con texto |
| `texto_parcial` | **9** | alguna página sin texto |
| `escaneado_sin_texto` | **0** | — |
| `error_lectura` | **0** | — |

**Ningún PDF requiere OCR.** Las páginas sin texto son portadas, contraportadas o páginas en blanco del cuadernillo — **ninguna contiene preguntas**:

| Documento | Páginas sin texto | Contenido observado |
|---|---|---|
| `2025_pi_plantilla_def` | 2 | cierre «Planilla de Respuestas DEFINITIVA» |
| `2022_aplazada_cuadernillo` | 2, 34, 35 | portada / cierre |
| `2021_libre_cuadernillo` | 31, 32 | cierre |
| `2021_pi_cuadernillo` | 31, 32 | cierre |
| `2021_pi_plantilla_def` | 2 | cierre |
| `2019_libre_cuadernillo` | 30, 31, 32 | pie «AUXILIAR DE ENFERMERÍA» + cierre |
| `2019_pi_cuadernillo` | 2, 31, 32 | portada + pie + cierre |
| `2016_libre_cuadernillo` | 33, 34, 35, 36 | cierre |
| `2016_pi_cuadernillo` | 33, 34, 35, 36 | cierre |

---

## 3. HALLAZGO — el reglamento cambió: 150 → 75 preguntas

La discrepancia «75 vs 100» que figuraba como PENDIENTE en el plan está **resuelta**: no era ruido de fuentes, son dos reglamentos distintos.

| Período | Preguntas | Reservas | Numeración de reservas |
|---|---|---|---|
| **2008** | **105** (cuestionario teórico) | — | — |
| **2016 – 2022** | **150** | 3 | **siempre 151, 152, 153** |
| **2024 – 2025** | **75** | 3 | **siempre 151, 152, 153** |

La numeración de las reservas es una convención del SAS y **no depende** de que el examen tenga 75 o 150 preguntas. Hay que modelarlo en el schema desde el día 1.

### Estructura especial de 2008

2008 no es un cuestionario único. El cuadernillo tiene **270 bloques `A)`** repartidos así:

| Parte | Preguntas |
|---|---|
| Cuestionario teórico | 105 |
| Supuesto práctico **A** | 55 |
| Supuesto práctico **B** | 55 |
| Supuesto práctico **C** | 55 |

Son **tres supuestos distintos** (A, B, C), no tres copias del mismo. Para Fase 1 hay que decidir si 2008 entra en el análisis de repetición o se archiva aparte (su estructura y su antigüedad lo hacen poco comparable con 2016+).

---

## 4. Las 13 convocatorias

| Año | Fecha | Modalidad | Preguntas | Anuladas (plantilla válida) |
|---|---|---|---|---|
| 2025 | 07-06 | libre + PI *(cuadernillo común)* | 75 + 75 | 151 (en ambos) |
| 2025 | 28-07 | aplazada | 75 | — |
| 2024 | 10-02 | centros SAS | 75 | 45, 51 |
| 2024 | 10-02 | APES extinguidas | 75 | 45, 51 |
| 2024 | 29-04 | aplazada | 75 | — |
| 2022 | 03-04 | aplazada | 150 | — |
| 2021 | 19-12 | libre | 150 | 107, 109 |
| 2021 | 19-12 | promoción interna | 150 | 107, 109 |
| 2019 | 27-04 | libre | 150 | 53, 73, 88, 139 |
| 2019 | 27-04 | promoción interna | 150 | 53, 73, 88, 139 |
| 2016 | 30-01 | libre | 150 | 3, 53, 57, 74, 76, 78, 137, 141 |
| 2016 | 30-01 | promoción interna | 150 | 50, 56, 74, 76, 78, 137, 141 |
| 2008 | 30-11 | concurso-oposición | 105 + 3×55 supuestos | 6, 77, 102 (teórico) |

**Total preguntas en el corpus**: 75×6 + 150×6 + 105 + 55×3 = **1.635 preguntas** (incluye reservas y supuestos de 2008).

### Corrección a usar (prioridad)

Las plantillas del SAS se publican en varias fases y se corrigen. Para cada convocatoria se usa **la primera que exista** de esta lista:

1. `plantilla_corr` / `correccion` — corrección posterior a la definitiva (2016 libre y PI, 2008)
2. `plantilla_def` — definitiva tras alegaciones
3. `plantilla_inicial` — solo si no hay nada mejor
4. `plantilla_prov` — provisional, solo trazabilidad

---

## 5. Formatos tipográficos (3 + 2)

Fase 1 necesita un parser por formato. Detectado en `scripts/conteo.py`:

### Cuadernillos

| Estilo | Años | Señal |
|---|---|---|
| **A** | 2025, 2024, 2021 | número **solo en su línea**, luego enunciado, luego `A) ` |
| **B** | 2019, 2016 (libre) | número **al final** del enunciado, justo antes de `A) ` |
| **C** | 2008 | `6. enunciado` al inicio de línea |

### Plantillas

| Formato | Ejemplo | Dónde |
|---|---|---|
| Columna simple | `1 A` / `45 ANULADA` | 2025 prov, 2024 prov, 2008 |
| Rejilla multicolumna | `1 B 51 C 101 D 151 A` | 2025 def, 2021 def, 2019, 2016 |

Valor `ANULADA` = pregunta anulada por el tribunal. **Se excluye del dataset** (o se marca `anulada: true` y se filtra en los modos de estudio).

---

## 6. Constitución en el corpus (estimación)

Métrica transparente, sin inventar:

| Métrica | Valor |
|---|---|
| Menciones **literales** de «Constitución» en todo el corpus | **13** |
| Preguntas etiquetadas por keyword inclusivo (estima_ce.py) | **29 / 1.809 bloques (1,6 %)** |
| Preguntas de CE observadas por cuadernillo | **0 – 4** |
| Artículos citados literalmente (no todos de la CE) | 1, 2, 3, 4, 10, 16, 17, 20, 26, 30, 36, 43, 47, 55, 71, 95, 110, 124 |

> **Estas cifras son un SUELO, no el dato real.** Muchas preguntas de CE **no nombran la Constitución** (p. ej. «¿cuál es el plazo para ser nombrado Presidente del Gobierno?» = art. 99 CE, sin citarlo). El etiquetado de Fase 1 por tema y artículo es el que vale.

### Consecuencia de producto

**La Constitución es una porción pequeña del cuestionario (aprox. 2–5 %).** Eso tiene dos lecturas:

- ✅ El corpus de Fase 1 es **manejable y preciso**: decenas de preguntas, no cientos. El clustering manual es viable y fiable.
- ⚠️ Una plataforma que solo cubra Constitución es una **herramienta nicho**. El valor está en la **profundidad del análisis** (qué artículos se repiten año tras año), no en el volumen de preguntas.

Si tras Fase 1 el radar resulta escaso, hay dos salidas: (a) mantener el foco y posicionarlo como «el módulo de Constitución del TCAE», o (b) ampliar a los Temas 2-10 (bloque común / legislación) con el mismo pipeline. **Decisión pendiente de Jesús.**

---

## 7. Anomalías de datos detectadas

Cosas raras que Fase 1 debe resolver **antes** de calcular frecuencias. Si se ignoran, el análisis de repetición sale sesgado.

| # | Anomalía | Impacto | Acción en Fase 1 |
|---|---|---|---|
| 1 | **2025 libre+PI comparten cuadernillo** (156 bloques `A)` = 78 × 2) | Contaría las preguntas dos veces | Partir el cuadernillo en dos secciones por su cabecera («PREGUNTAS ACCESO LIBRE» / PI) |
| 2 | **2019 libre y PI tienen idénticas anuladas** (53, 73, 88, 139) | Sospecha de copy-paste en la plantilla | Comparar los enunciados de esas 4 preguntas en libre vs PI. Si coinciden, es dato real; si no, descartar la marca de anulada |
| 3 | **2021 libre y PI tienen idénticas anuladas** (107, 109) | Ídem | Ídem |
| 4 | **2016 plantilla_def tiene un typo** (marca «72 ANULADA» dos veces y omite la 74) | Corrección errónea | **Ya resuelto**: se usa `2016_*_plantilla_corr`, que sí marca la 74 |
| 5 | **2024_apes_plantilla_prov** da 0 pares al parsear | No aporta | **Ya resuelto**: se usa la `plantilla_def`, que sí parsea |
| 6 | **Nombres internos engañosos** | Clasificar mal el año | Ya corregido en el manifiesto: manda la fecha de celebración, no el nombre del PDF (2024 dice «2023», 2022 dice «2021», MAD rotula 2016 como «2015») |
| 7 | **2008 tiene 3 supuestos distintos** (A, B, C) | No comparable con 2016+ | Decidir si entra en el análisis de repetición o se archiva aparte |

---

## 8. Cubrimiento vs. fuentes alternativas

| Año | SAS oficial | Opoluz | MAD (sinfsa.com) |
|---|---|---|---|
| 2008 | ✅ | ✅ | — |
| 2015/16 | ✅ | ✅ | ✅ *(mismo PDF, rotulado 2015)* |
| 2019 | ✅ | ✅ | — |
| 2021 | ✅ | ✅ | ✅ |
| 2022 | ✅ | ✅ | — |
| 2023/24 | ✅ | ✅ | ✅ *(mismo PDF, rotulado 2023)* |
| 2025 | ✅ | ✅ | ✅ |

**MAD es un mirror estricto y no aporta años nuevos.** Opoluz aporta el índice, no los PDFs: los originales están en el SAS. No se copia contenido de ninguno de los dos.

---

## 9. Cómo reproducir

```bash
cd "Proyecto tcae"
python -m pip install pypdf fonttools

python scripts/descargar.py        # 45 PDFs -> data/pdfs/   (idempotente)
python scripts/extraer_pdf.py      # PDF -> data/raw/*.json  (texto por página)
python scripts/conteo.py           # preguntas y plantillas por convocatoria
python scripts/menciones.py        # menciones literales de Constitución
python scripts/estima_ce.py        # estimación inclusiva de peso de CE
python scripts/muestra.py <id> [n] # volcado de una página concreta
```

Dependencias: `pypdf`, `fontTools` (ambas ya instaladas en el venv).

---

## 10. Qué queda para Fase 1 (no hecho aquí a propósito)

- [ ] Parseo de **preguntas individuales**: `enunciado` + `opciones: {a,b,c,d}` (3 parsers, uno por estilo tipográfico)
- [ ] Merge **cuadernillo ↔ plantilla**: respuesta correcta por pregunta, respetando `ANULADA`
- [ ] Partición del cuadernillo 2025 libre+PI (anomalía #1)
- [ ] Verificación de anomalías #2 y #3 (anuladas idénticas libre vs PI)
- [ ] Decisión sobre 2008 (anomalía #7)
- [ ] **Filtrado Tema 1 (Constitución)** — keyword + revisión manual
- [ ] Normalización de texto y clustering (exacto → difuso)
- [ ] Etiquetado por artículo de la CE (regex + revisión)
- [ ] Score de repetición: `frecuencia × (1 + 0,25 × años_diferentes)`
- [ ] Entregable: `docs/RADAR_CONSTITUCION.md` **para validación de Jesús**

Nada de esto se publica sin el visto bueno de Jesús sobre `RADAR_CONSTITUCION.md`.
