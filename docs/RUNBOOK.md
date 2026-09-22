# Runbook — cómo mantener OpoTCAE vivo

Guía para cuando el SAS publique una convocatoria nueva (la de 2026, o cualquier
aplazada) o cuando haya que rehacer el análisis. Escrita para que se pueda seguir
sin haber tocado nunca este código.

---

## 1. Añadir una convocatoria nueva

### 1.1 Encontrar los PDFs

1. Entrar en [el archivo de exámenes del SAS](https://www.sspa.juntadeandalucia.es/servicioandaluzdesalud/profesionales/ofertas-de-empleo/oferta-de-empleo-publico-puestos-base) → categoría TCAE.
2. De cada prueba hacen falta **dos cosas**: el **cuadernillo** (el examen) y la
   **plantilla de respuestas**. Si hay plantilla provisional **y** definitiva, se
   descargan las dos: se usa la definitiva, y la provisional solo sirve para
   trazabilidad.
3. Apuntar la **fecha real de celebración**. Importa más que el año que ponga el
   nombre del PDF: hay cuadernillos que dicen «2023» y se celebraron en febrero
   de 2024.

Fuentes de referencia cruzada (para verificar que no falta nada):
- [Opoluz · exámenes TCAE SAS](https://opoluz.com/examenes-oficiales/sas/tcae/)
- [MAD · exámenes anteriores TCAE SAS](https://mad.es/blog/examenes-anteriores-tcae-sas/)

### 1.2 Registrar el documento

Editar `scripts/manifiesto.py` y añadir una entrada por cada PDF:

```python
{
    "id": "2026_libre_cuadernillo",
    "anio": 2026, "fecha": "2026-06-06", "modalidad": "libre",
    "tipo": "cuadernillo",
    "url": _sas("2026/algo.pdf"),
    "destino": "2026-06-06_libre_cuadernillo.pdf",
},
```

`tipo` admite: `cuadernillo`, `plantilla_prov`, `plantilla_def`, `plantilla_corr`,
`plantilla_inicial`, `correccion`, `fe_erratas`.

### 1.3 Registrar la sección de examen

Editar `SECCIONES` dentro de `scripts/parsear.py`. Una **sección** es un
conjunto de preguntas con su propia plantilla. Ojo: un solo cuadernillo puede
tener dos secciones (en 2025 libre y promoción interna compartían PDF, y se
parte por rangos de páginas):

```python
{
    "exam_id": "2026-06-06_libre", "cuadernillo": "2026_libre_cuadernillo",
    "plantilla": "2026_libre_plantilla_def", "plantilla_prov": "2026_libre_plantilla_prov",
    "anio": 2026, "fecha": "2026-06-06", "modalidad": "libre",
    "pages": None,          # None = todo el PDF, o (inicio, fin) 1-indexed
    "n_main": 75,           # 75 desde 2024; 150 antes
},
```

**`n_main` es importante.** Las 3 preguntas de reserva siempre se numeran
151-153, sea el examen de 75 o de 150 preguntas.

### 1.4 Ejecutar el pipeline entero

Empezar siempre por `parsear.py`: `limpia_parseo.py` acumula recortes si se
ejecuta dos veces sobre el mismo JSON.

```bash
pip install -r requirements.txt

python scripts/descargar.py
python scripts/extraer_pdf.py
python scripts/parsear.py
python scripts/limpia_parseo.py
python scripts/clasificar.py
python scripts/radar.py
python scripts/semantico.py      # tarda ~1 min (descarga de embeddings)
python scripts/exporta_web.py
```

### 1.5 Comprobar que ha salido bien

```bash
python -m pytest                # tests del pipeline
python scripts/verifica_anomalias.py   # contraste libre vs PI
```

Mirar `scripts/parsear.py` al final: la tabla de salida debe marcar
`preg == esp` en todas las filas. Si una fila dice `DIFIERE`, o se ha perdido
una pregunta al parsear o `n_main` está mal.

Y revisar `docs/SEMANTICO.md`: salirán conceptos nuevos multi-año.

### 1.6 Actualizar la documentación

- `README.md`: la tabla de convocatorias y las cifras totales.
- `docs/ESTADO.md`: las cifras de la tabla de datos.

### 1.7 Publicar

```bash
cd web
npm install
npm run build
vercel --prod
```

También subir a git: `git add -A && git commit && git push`.

---

## 2. Rehacer el análisis desde cero

```bash
rm -rf data/raw data/parsed web/public/data
python scripts/descargar.py
# ... resto del pipeline de arriba
```

**No** borres `data/pdfs/` si no quieres volver a descargar 10 MB.

---

## 3. Si una pregunta sale mal clasificada

Las reglas viven en `scripts/clasificar.py`, en `REGLAS`, de más a menos
específico: **gana la primera que encaje**. Para arreglar una pregunta
concreta:

1. Mirar a qué tema se le está yendo: `python scripts/clasificar.py` te da los
   totales.
2. Buscar el enunciado en `data/parsed/preguntas.json`.
3. Añadir una palabra clave al tema correcto, o mover la regla de sitio si la
   están pisando desde un tema anterior.
4. `python scripts/clasificar.py` y comprobar que la pregunta cae donde toca.

Hay una bolsa **«Otros»** (anatomía, fisiología, farmacología, obstetricia y
clínica) que el temario oficial de 29 temas no enumera. Es normal que crezca:
el examen pregunta contenido del título de FP que no está en el BOJA.

---

## 4. Si una pregunta sale mal parseada

Los problemas típicos, por síntoma:

| Síntoma | Causa | Dónde se arregla |
|---|---|---|
| Opciones vacías | el texto de la última opción se pegó al enunciado siguiente | `cortar_hueco()` en `scripts/parsear.py` |
| Enunciado con texto de portada | falta una línea de basura en `RE_RUIDO` | `scripts/parsear.py` o `scripts/limpia_parseo.py` |
| Enunciado vacío | el enunciado se coló en la opción anterior | `recuperar_de_opcion_anterior()` en `scripts/limpia_parseo.py` |
| Número de pregunta mal | el formato del PDF es nuevo | `extraer_numero()` en `scripts/parsear.py` |

Hay 4 formatos de cuadernillo conocidos (ver `docs/FASE0_INVENTARIO.md` §5). Si
sale uno nuevo, añadirlo ahí y ajustar `cortar_hueco()`.

---

## 5. El contrato de datos

Si cambias el formato de `web/public/data/*.json`, hay que tocar también los
tipos de `web/src/types.ts` y `scripts/exporta_web.py`. `npm run build` falla si
no encajan: es el tipo de error que se caza solo.

---

## 6. Contacto

Proyecto gratuito y público. Código bajo licencia MIT (ver `LICENSE`). Las
preguntas de examen son transcripciones de los cuadernillos oficiales del
Servicio Andaluz de Salud, con atribución a su fuente.
