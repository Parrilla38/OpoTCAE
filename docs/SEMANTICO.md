# Matching semántico — conceptos repetidos

Modelo **paraphrase-multilingual-MiniLM-L12-v2** · umbral de similitud **0.72** · 1504 preguntas analizadas.

Agrupa preguntas que pregunten **lo mismo con otras palabras**. Es el complemento al clustering literal: donde `radar.py` encuentra enunciados idénticos, esto encuentra el concepto subyacente.

- **486** conceptos con ≥2 formulaciones distintas
- **123** de ellos caen en **2 o más años distintos** (la señal fuerte de «esto se repite»)
- 273 preguntas quedaron como formulación única

## Conceptos que caen en varios años

Ordenados por `score = nº preguntas × (1 + 0,35 × años) × similitud_media`.

### 1. Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posición de de

**14 formulaciones** · años **2016, 2019, 2021, 2024, 2025** · temas — · similitud media 0.762 · score **29.32**

- `2016 · libre` — Señala la respuesta correcta en cuanto a los factores que influyen en las úlceras por presión:
- `2019 · libre` — Señala la respuesta correcta en cuanto a los factores situacionales de las ulceras por presión:
- `2019 · pi` — Señala la respuesta correcta en cuanto a los factores situacionales de las ulceras por presión:
- `2021 · libre` — De las siguientes medidas relacionadas con el manejo de la presión en pacientes sentados, ¿cuál llevarías a cabo con un 
- `2021 · libre` — Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posi
- `2021 · libre` — Entre los factores que predisponen el desarrollo de las úlceras por presión se encuentran los factores intrínsecos del p
- `2021 · libre` — ¿En cuál de las siguientes situaciones NO sería necesario reevaluar el riesgo de desarrollar úlceras por presión en un p
- `2021 · pi` — De las siguientes medidas relacionadas con el manejo de la presión en pacientes sentados, ¿cuál llevarías a cabo con un 
- `2021 · pi` — Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posi
- `2021 · pi` — Entre los factores que predisponen el desarrollo de las úlceras por presión se encuentran los factores intrínsecos del p
- `2021 · pi` — ¿En cuál de las siguientes situaciones NO sería necesario reevaluar el riesgo de desarrollar úlceras por presión en un p
- `2024 · aplazada` — Las posiciones anatómicas básicas del plan de cuidados en la prevención de úlceras por presión son:
- `2024 · aplazada` — En la prevención de las úlceras por presión, ¿cuál es la escala que valora: incontinencia, nutrición/ingesta, estado men
- `2025 · aplazada` — ¿Qué escala de valoración del riesgo de padecer úlceras por presión es recomendada por la NIC, NOC, y la GNEAUPP?

### 2. La estructura organizativa responsable de la atención especializada a la salud mental de la población, que incorpora los dispositi

**11 formulaciones** · años **2016, 2019, 2022, 2024, 2025** · temas — · similitud media 0.784 · score **23.71**

- `2016 · libre` — En el equipo de atención comunitaria, la atención de salud mental sigue un modelo integral de atención interdisciplinari
- `2016 · pi` — En el equipo de atención comunitaria, la atención de salud mental sigue un modelo integral de atención interdisciplinari
- `2019 · libre` — Dentro de las funciones de salud mental comunitaria está:
- `2019 · pi` — Dentro de las funciones de salud mental comunitaria está:
- `2022 · aplazada` — La Comunidad Terapéutica de Salud Mental, es:
- `2024 · centros_sas` — La estructura organizativa responsable de la atención especializada a la salud mental de la población, que incorpora los
- `2024 · apes` — La estructura organizativa responsable de la atención especializada a la salud mental de la población, que incorpora los
- `2024 · aplazada` — El dispositivo asistencial de salud mental, destinado a atender las necesidades de hospitalización en salud mental de la
- `2025 · libre` — ¿Cómo se denomina la Unidad de Salud Mental que funciona como un dispositivo que tiene por objeto la recuperación de hab
- `2025 · pi` — ¿Cómo se denomina la Unidad de Salud Mental que funciona como un dispositivo que tiene por objeto la recuperación de hab
- `2025 · aplazada` — De las siguientes funciones, ¿cuál pertenece al hospital de día de salud mental?

### 3. La ley 41/2002, básica reguladora de la autonomía del paciente y derechos y obligaciones en materia de información y documentación

**10 formulaciones** · años **2016, 2019, 2021, 2022, 2024** · temas T09 · similitud media 0.819 · score **22.53**

- `2016 · libre` — Uno de estos derechos no se contempla en la Ley 41/2002 básica reguladora de la autonomía del paciente y de derechos y o
- `2019 · libre` — La ley 41/2002, básica reguladora de la Autonomía de autonomía del paciente y derechos y obligaciones en materia de info
- `2019 · pi` — La ley 41/2002, básica reguladora de la autonomía del paciente y derechos y obligaciones en materia de información y doc
- `2021 · libre` — ¿Cuál es la ley básica reguladora de la autonomía del paciente y de derechos y obligaciones en materia de información y 
- `2021 · libre` — El derecho que tiene la persona que recibe la atención sanitaria, a que toda la información de carácter personal, utiliz
- `2021 · pi` — ¿Cuál es la ley básica reguladora de la autonomía del paciente y de derechos y obligaciones en materia de información y 
- `2021 · pi` — El derecho que tiene la persona que recibe la atención sanitaria, a que toda la información de carácter personal, utiliz
- `2022 · aplazada` — Según la Ley 41/2002, de autonomía del paciente, ¿quién tiene derecho a la información asistencial?
- `2022 · aplazada` — Según la ley 41/2002, de 14 de noviembre, básica reguladora de la autonomía del paciente y de derechos y obligaciones en
- `2024 · aplazada` — Según el artículo 20 de la Ley 41/2002, de 14 de noviembre, reguladora de la autonomía del paciente y de derechos y obli

### 4. La definición de úlcera por presión (UPP) es:

**9 formulaciones** · años **2016, 2019, 2021, 2025** · temas — · similitud media 0.815 · score **17.61**

- `2016 · pi` — La definición de ulcera por presión es:
- `2019 · libre` — La definición de úlcera por presión (UPP) es:
- `2019 · pi` — La definición de úlcera por presión (UPP) es:
- `2021 · libre` — ¿Qué definirías por úlcera por presión?
- `2021 · libre` — El orden en el proceso de cicatrización de una úlcera por presión (UPP) sería:
- `2021 · pi` — ¿Qué definirías por úlcera por presión?
- `2021 · pi` — El orden en el proceso de cicatrización de una úlcera por presión (UPP) sería:
- `2025 · libre` — Las úlceras por presión (UPP) son lesiones de origen:
- `2025 · pi` — Las úlceras por presión (UPP) son lesiones de origen:

### 5. de enfermería, tiene que realizar el aseo de un paciente encamado. En relación con esta tarea indique la afirmación mas correcta:

**10 formulaciones** · años **2016, 2019, 2021** · temas — · similitud media 0.814 · score **16.7**

- `2016 · libre` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2016 · libre` — La Auxiliar de Enfermería tiene que realizar el aseo de un paciente encamado para ello debe de:
- `2016 · pi` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2016 · pi` — La Auxiliar de Enfermería tiene que realizar el aseo de un paciente encamado para ello debe de:
- `2019 · libre` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2019 · libre` — de enfermería, tiene que realizar el aseo de un paciente encamado. En relación con esta tarea indique la afirmación mas 
- `2019 · pi` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2019 · pi` — de enfermería, tiene que realizar el aseo de un paciente encamado. En relación con esta tarea indique la afirmación mas 
- `2021 · libre` — Señale la respuesta correcta a la hora de realizar el aseo de un paciente encamado:
- `2021 · pi` — Señale la respuesta correcta a la hora de realizar el aseo de un paciente encamado:

### 6. Se define almacenamiento de residuos como:

**8 formulaciones** · años **2016, 2021, 2025** · temas — · similitud media 0.809 · score **13.26**

- `2016 · libre` — El almacenamiento temporal de residuos no debe superar nunca:
- `2016 · libre` — Plan de Gestión de Residuos de la Dirección General de Asistencia Sanitaria y Resultados en Salud. Los recipientes o env
- `2016 · pi` — El almacenamiento temporal de residuos no debe superar nunca:
- `2016 · pi` — Plan de Gestión de Residuos de la Dirección General de Asistencia Sanitaria y Resultados en Salud. Los recipientes o env
- `2021 · libre` — Se define almacenamiento de residuos como:
- `2021 · pi` — Se define almacenamiento de residuos como:
- `2025 · libre` — En general, el tiempo de almacenamiento final, por parte de los productores de los residuos peligrosos, no excederá de:
- `2025 · pi` — En general, el tiempo de almacenamiento final, por parte de los productores de los residuos peligrosos, no excederá de:

### 7. Para realizar la higiene bucal en pacientes inconscientes debemos tener en cuenta cuál de estas acciones no es la correcta:

**8 formulaciones** · años **2016, 2019, 2021** · temas — · similitud media 0.799 · score **13.1**

- `2016 · libre` — Para realizar la higiene bucal en pacientes inconscientes debemos tener en cuenta cuál de estas acciones no es la correc
- `2016 · pi` — Para realizar la higiene bucal en pacientes inconscientes debemos tener en cuenta cuál de estas acciones no es la correc
- `2019 · libre` — Para realizar la higiene bucal en pacientes inconscientes; cuál de estas acciones no es la correcta:
- `2019 · libre` — Se entiende por higiene bucal:
- `2019 · pi` — Para realizar la higiene bucal en pacientes inconscientes; cuál de estas acciones no es la correcta:
- `2019 · pi` — Se entiende por higiene bucal:
- `2021 · libre` — Señale la respuesta correcta en cuanto a la limpieza de la boca en un paciente inconsciente.
- `2021 · pi` — Señale la respuesta correcta en cuanto a la limpieza de la boca en un paciente inconsciente.

### 8. ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?

**6 formulaciones** · años **2021, 2022, 2024, 2025** · temas — · similitud media 0.765 · score **11.02**

- `2021 · libre` — ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?
- `2021 · pi` — Los restos de material de pequeñas curas, bolsas de orina vacías, filtros de diálisis, pañales y yesos, pertenecen al gr
- `2021 · pi` — ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?
- `2022 · aplazada` — Las agujas sanitarias son un residuo:
- `2024 · aplazada` — ¿Qué tipo de residuos no pueden compactarse o triturarse, en ningún caso?
- `2025 · aplazada` — ¿En qué grupo se clasifican los residuos hospitalarios excretados que pueden transmitir el cólera?

### 9. La obligación de guardar secreto profesional, afecta a:

**6 formulaciones** · años **2016, 2019, 2022** · temas T09 · similitud media 0.877 · score **10.79**

- `2016 · libre` — La obligación de guardar secreto profesional, afecta a:
- `2016 · pi` — La obligación de guardar secreto profesional, afecta a:
- `2019 · libre` — La obligación de guardar secreto profesional, afecta a:
- `2019 · pi` — La obligación de guardar secreto profesional, afecta a:
- `2022 · aplazada` — ¿En qué caso se puede romper el secreto profesional?
- `2022 · aplazada` — La obligación de guardar secreto profesional, afecta a:

### 10. Señale la opción INCORRECTA en relación al Biobanco del Sistema Sanitario Público de Andalucía:

**6 formulaciones** · años **2016, 2019, 2021** · temas T03 · similitud media 0.818 · score **10.06**

- `2016 · libre` — La visión de los Biobancos del sistema sanitario público de Andalucía(SSPA) es:
- `2016 · pi` — La visión de los Biobancos del sistema sanitario público de Andalucía(SSPA) es:
- `2019 · libre` — El Biobanco del SSPA depende de:
- `2019 · pi` — El Biobanco del SSPA depende de:
- `2021 · libre` — Señale la opción INCORRECTA en relación al Biobanco del Sistema Sanitario Público de Andalucía:
- `2021 · pi` — Señale la opción INCORRECTA en relación al Biobanco del Sistema Sanitario Público de Andalucía:

### 11. De los principales eslabones de la cadena epidemiológica, cual es la correcta:

**5 formulaciones** · años **2016, 2019, 2021** · temas — · similitud media 0.952 · score **9.76**

- `2016 · pi` — De los principales eslabones de la cadena epidemiológica, cual es la correcta:
- `2019 · libre` — De los principales eslabones de la cadena epidemiológica, cual es la afirmación mas correcta:
- `2019 · pi` — De los principales eslabones de la cadena epidemiológica, cual es la afirmación mas correcta:
- `2021 · libre` — Los eslabones de la cadena epidemiológica son:
- `2021 · pi` — Los eslabones de la cadena epidemiológica son:

### 12. En los enfermos renales está indicada una dieta:

**5 formulaciones** · años **2016, 2019, 2025** · temas — · similitud media 0.923 · score **9.46**

- `2016 · libre` — En los enfermos renales está indicada una dieta:
- `2016 · pi` — En los enfermos renales está indicada una dieta:
- `2019 · libre` — En los enfermos renales está indicada una dieta:
- `2019 · pi` — En los enfermos renales está indicada una dieta:
- `2025 · aplazada` — La dieta hipoproteica está prescrita o indicada en pacientes que padecen:

### 13. Antes de proceder al baño de la paciente encamada deben tener en cuenta:

**5 formulaciones** · años **2016, 2019, 2022, 2024** · temas — · similitud media 0.76 · score **9.12**

- `2016 · pi` — El cuidado del ombligo debe hacerse:
- `2019 · libre` — Antes de proceder al baño de la paciente encamada deben tener en cuenta:
- `2019 · pi` — Antes de proceder al baño de la paciente encamada deben tener en cuenta:
- `2022 · aplazada` — Cuando se realice el baño a las pacientes de la habitación 16, que son pacientes encamadas, se procederá a: (Señale la r
- `2024 · aplazada` — La higiene de un paciente encamado hay que realizarla por partes. ¿Cuál es la última parte que se debe lavar a un pacien

### 14. En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un tratamiento cur

**5 formulaciones** · años **2021, 2022, 2024** · temas — · similitud media 0.883 · score **9.06**

- `2021 · libre` — La atención a los pacientes cuya enfermedad no responde a tratamiento curativo, y cuyo fin es lograr la mayor calidad de
- `2021 · pi` — La atención a los pacientes cuya enfermedad no responde a tratamiento curativo, y cuyo fin es lograr la mayor calidad de
- `2022 · aplazada` — Indica la definición correcta de cuidados paliativos según la Organización Mundial de la Salud:
- `2024 · centros_sas` — En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un trata
- `2024 · apes` — En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un trata

### 15. Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental que desar

**5 formulaciones** · años **2016, 2019, 2025** · temas — · similitud media 0.859 · score **8.8**

- `2016 · pi` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2019 · libre` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2019 · pi` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2025 · libre` — ¿Cómo se llaman los nutrientes que aportan al organismo humano gran cantidad de vitaminas y sales minerales?
- `2025 · pi` — ¿Cómo se llaman los nutrientes que aportan al organismo humano gran cantidad de vitaminas y sales minerales?

### 16. Los colores de los contenedores que se utilizan en la gestión de residuos son:

**5 formulaciones** · años **2016, 2019, 2021** · temas — · similitud media 0.846 · score **8.67**

- `2016 · pi` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2019 · libre` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2019 · pi` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2021 · libre` — ¿A qué grupo pertenecen los residuos que se recogen en bolsa de color rojo y contenedores, reciclables o de un solo uso,
- `2021 · pi` — ¿A qué grupo pertenecen los residuos que se recogen en bolsa de color rojo y contenedores, reciclables o de un solo uso,

### 17. El paciente Antonio José Álvarez, es un hombre de 69 años, se interviene el 19-04- 2015 . Practicando hemicolectomía derecha por v

**6 formulaciones** · años **2016, 2019** · temas — · similitud media 0.848 · score **8.65**

- `2016 · libre` — El paciente Antonio José Álvarez, es un hombre de 69 años, se interviene el 19-04- 2015 . Practicando hemicolectomía der
- `2016 · libre` — El paciente Antonio José Álvarez, es un hombre de 69 años, se interviene el 19-04- 2015 . Practicando hemicolectomía der
- `2016 · pi` — El paciente Antonio José Álvarez, es un hombre de 69 años, se interviene el 19-04- 2015 . Practicando hemicolectomía der
- `2016 · pi` — El paciente Antonio José Álvarez, es un hombre de 69 años, se interviene el 19-04- 2015 . Practicando hemicolectomía der
- `2019 · libre` — ía a los pacientes de forma directa o delegadas relacionadas con la higiene, la alimentación, la movilización, la ayuda 
- `2019 · pi` — ía a los pacientes de forma directa o delegadas relacionadas con la higiene, la alimentación, la movilización, la ayuda 

### 18. Las vitaminas se clasifican en:

**5 formulaciones** · años **2016, 2019, 2022** · temas — · similitud media 0.841 · score **8.62**

- `2016 · libre` — Las vitaminas se clasifican en:
- `2016 · pi` — Las vitaminas se clasifican en:
- `2019 · libre` — Las vitaminas se clasifican en:
- `2019 · pi` — Las vitaminas se clasifican en:
- `2022 · aplazada` — Entre las vitaminas hidrosolubles se encuentran:

### 19. Antes de ponerle el enema debemos de colocar al paciente en posición:

**5 formulaciones** · años **2016, 2019, 2022** · temas — · similitud media 0.84 · score **8.61**

- `2016 · libre` — Antes de ponerle un enema debemos de colocar al paciente en posición:
- `2016 · pi` — Antes de ponerle un enema debemos de colocar al paciente en posición:
- `2019 · libre` — Antes de ponerle el enema debemos de colocar al paciente en posición:
- `2019 · pi` — Antes de ponerle el enema debemos de colocar al paciente en posición:
- `2022 · aplazada` — Antes de administrarle el enema al paciente de la 20, tenemos que: (señale la respuesta INCORRECTA)

### 20. Leonardo es paciente con hemiplejia ingresado en la habitación 501 A, está encamado por un cuadro febril, su familiar llama al tim

**6 formulaciones** · años **2016, 2019** · temas — · similitud media 0.837 · score **8.54**

- `2016 · libre` — Leonardo, paciente con hemiplejia, está encamado por un cuadro febril. Hay que movilizarlo. ¿Dónde nos colocaríamos?
- `2016 · pi` — Leonardo, paciente con hemiplejia, está encamado por un cuadro febril. Hay que movilizarlo. ¿Dónde nos colocaríamos?
- `2019 · libre` — Leonardo es paciente con hemiplejia ingresado en la habitación 501 A, está encamado por un cuadro febril, su familiar ll
- `2019 · libre` — Isidro comparte habitación con Leonardo, ha sufrido un ictus y lleva 10 días encamado. Queremos ponerlo en decúbito late
- `2019 · pi` — Leonardo es paciente con hemiplejia ingresado en la habitación 501 A, está encamado por un cuadro febril, su familiar ll
- `2019 · pi` — Isidro comparte habitación con Leonardo, ha sufrido un ictus y lleva 10 días encamado. Queremos ponerlo en decúbito late

### 21. ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?

**6 formulaciones** · años **2022, 2024** · temas — · similitud media 0.833 · score **8.5**

- `2022 · aplazada` — Según el sistema de clasificación/estadiaje de las úlceras por presión, ¿qué estadio corresponde una úlcera por presión 
- `2024 · centros_sas` — ¿En qué estadio se encuentra una úlcera por presión, cuando existe un eritema cutáneo en piel intacta que no cede al des
- `2024 · centros_sas` — ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?
- `2024 · apes` — ¿En qué estadio se encuentra una úlcera por presión, cuando existe un eritema cutáneo en piel intacta que no cede al des
- `2024 · apes` — ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?
- `2024 · aplazada` — ¿En qué zonas presenta úlceras por presión un paciente colocado en decúbito lateral?

### 22. ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?

**6 formulaciones** · años **2021, 2025** · temas — · similitud media 0.83 · score **8.47**

- `2021 · libre` — Los valores y principios de la Bioética son:
- `2021 · pi` — Los valores y principios de la Bioética son:
- `2025 · libre` — ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?
- `2025 · pi` — El rechazo al tratamiento, ¿dentro de qué principio básico de la Bioética se encuadraría?
- `2025 · pi` — ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?
- `2025 · aplazada` — ¿Sobre qué principios de la Bioética se apoya toda la asistencia sanitaria?

### 23. La infección nosocomial se define como:

**5 formulaciones** · años **2019, 2022, 2024** · temas — · similitud media 0.822 · score **8.42**

- `2019 · libre` — La infección nosocomial se define como:
- `2019 · pi` — La infección nosocomial se define como:
- `2022 · aplazada` — Cuando la infección nosocomial es causada por microorganismos pertenecientes a la propia flora del paciente, se denomina
- `2024 · centros_sas` — ¿A qué se denomina “Tropismo” en las infecciones nosocomiales?
- `2024 · apes` — ¿A qué se denomina “Tropismo” en las infecciones nosocomiales?

### 24. Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH a que grupo corresponde:

**5 formulaciones** · años **2016, 2019, 2024** · temas — · similitud media 0.818 · score **8.38**

- `2016 · pi` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH a que grupo corresponde:
- `2019 · libre` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH, ¿a que grupo de clasific
- `2019 · pi` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH, ¿a que grupo de clasific
- `2024 · centros_sas` — En el grupo II Residuos sanitarios asimilables a urbanos, se incluyen:
- `2024 · apes` — En el grupo II Residuos sanitarios asimilables a urbanos, se incluyen:

### 25. Mateo, paciente en situación terminal y con una infección oral en la cavidad bucal, debido a las deficiencias nutricionales y al c

**6 formulaciones** · años **2016, 2021** · temas — · similitud media 0.795 · score **8.11**

- `2016 · libre` — Mateo, paciente en situación terminal y con una infección oral en la cavidad bucal, debido a las deficiencias nutriciona
- `2016 · libre` — Antonio, paciente de 48 años ingresado en la planta de digestivo, ingresa en turno de tarde para cirugía al día siguient
- `2016 · pi` — Mateo, paciente en situación terminal y con una infección oral en la cavidad bucal, debido a las deficiencias nutriciona
- `2016 · pi` — Antonio, paciente de 48 años ingresado en la planta de digestivo, ingresa en turno de tarde para cirugía al día siguient
- `2021 · libre` — Antonia, paciente de 60 años, sin antecedentes personales de interés, se encuentra ingresada en el box 9 por dolor abdom
- `2021 · pi` — Antonia, paciente de 60 años, sin antecedentes personales de interés, se encuentra ingresada en el box 9 por dolor abdom

### 26. Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los drenajes d

**5 formulaciones** · años **2016, 2019, 2022** · temas — · similitud media 0.79 · score **8.1**

- `2016 · libre` — Rocío es intervenida de reconstrucción mamaria. Cuando sube a planta trae dos drenajes de aspiración (Redón). Como norma
- `2016 · pi` — Rocío es intervenida de reconstrucción mamaria. Cuando sube a planta trae dos drenajes de aspiración (Redón). Como norma
- `2019 · libre` — Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los 
- `2019 · pi` — Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los 
- `2022 · aplazada` — El drenaje que tiene colocado María es un drenaje de aspiración tipo Redon. ¿Qué precaución debe usted tener con este ti

### 27. ¿A qué tipo de dispositivo pertenece la unidad cuya finalidad es el tratamiento intensivo de pacientes con Trastorno Mental Grave 

**5 formulaciones** · años **2024, 2025** · temas — · similitud media 0.885 · score **7.52**

- `2024 · centros_sas` — ¿Cuál es el dispositivo de atención ambulatoria con el que se coordinan el resto de dispositivos asistenciales de atenci
- `2024 · apes` — ¿Cuál es el dispositivo de atención ambulatoria con el que se coordinan el resto de dispositivos asistenciales de atenci
- `2024 · aplazada` — ¿A qué tipo de dispositivo pertenece la unidad cuya finalidad es el tratamiento intensivo de pacientes con Trastorno Men
- `2025 · libre` — ¿Cuál es el dispositivo que tiene como finalidad el tratamiento intensivo de pacientes con Trastorno Mental Grave que re
- `2025 · pi` — ¿Cuál es el dispositivo que tiene como finalidad el tratamiento intensivo de pacientes con Trastorno Mental Grave que re

### 28. Pedro está ingresado, encamado y con sonda nasogástrica. A la hora de administrarle la alimentación necesitas:

**5 formulaciones** · años **2016, 2019** · temas — · similitud media 0.883 · score **7.51**

- `2016 · libre` — Pedro está ingresado, encamado y con sonda nasogástrica. A la hora de administrarle la alimentación necesitas:
- `2016 · libre` — Pedro está ingresado, encamado y con sonda nasogástrica. A la hora de administrarle la alimentación necesitas:
- `2016 · pi` — Pedro está ingresado, encamado y con sonda nasogástrica. A la hora de administrarle la alimentación necesitas:
- `2019 · libre` — Pedro está ingresado en la habitación contigua a Dolores, encamado y con sonda nasogástrica. A la hora de administrarle 
- `2019 · pi` — Pedro está ingresado en la habitación contigua a Dolores, encamado y con sonda nasogástrica. A la hora de administrarle 

### 29. ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospitalario?

**5 formulaciones** · años **2021, 2022** · temas — · similitud media 0.837 · score **7.11**

- `2021 · libre` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2021 · pi` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2022 · aplazada` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2022 · aplazada` — La medida más adecuada para evitar las infecciones cruzadas entre pacientes - personal asistencial es:
- `2022 · aplazada` — A lo largo de la jornada, los TCAE se lavan las manos frecuentemente ya que, como buenos profesionales, saben que la med

### 30. El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas para invest

**4 formulaciones** · años **2021, 2022, 2024** · temas T03 · similitud media 0.859 · score **7.05**

- `2021 · libre` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas p
- `2021 · pi` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas p
- `2022 · aplazada` — El Biobanco del SSPA, en su área de tejidos, sustancias y muestras biológicas para investigación, está organizado como u
- `2024 · aplazada` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA) lleva a cabo una actividad descentralizada a través de sus

### 31. Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Patologías c

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 0.998 · score **6.79**

- `2016 · libre` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2016 · pi` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2019 · libre` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2019 · pi` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa

### 32. Señale la respuesta correcta sobre las condiciones de almacenamiento y conservación de los medicamentos::

**5 formulaciones** · años **2021, 2025** · temas T08 · similitud media 0.795 · score **6.76**

- `2021 · libre` — Señale la respuesta correcta sobre las condiciones de almacenamiento y conservación de los medicamentos:
- `2021 · libre` — La enfermera ha administrado a Pedro una medicación termolábil. ¿Cuál es la temperatura en la que deben conservarse los 
- `2021 · pi` — Señale la respuesta correcta sobre las condiciones de almacenamiento y conservación de los medicamentos::
- `2021 · pi` — La enfermera ha administrado a Pedro una medicación termolábil. ¿Cuál es la temperatura en la que deben conservarse los 
- `2025 · aplazada` — ¿Cómo debemos conservar la mayoría de los medicamentos termolábiles?

### 33. Dolores es una paciente ingresada en la planta a la que le han insertado un tubo de gastrostomía. Te dispones a darle la alimentac

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 0.958 · score **6.52**

- `2016 · libre` — Dolores es una paciente a la que le han insertado un tubo de gastrostomía. Te dispones a darle la alimentación, ¿qué no 
- `2016 · pi` — Dolores es una paciente a la que le han insertado un tubo de gastrostomía. Te dispones a darle la alimentación, ¿qué no 
- `2019 · libre` — Dolores es una paciente ingresada en la planta a la que le han insertado un tubo de gastrostomía. Te dispones a darle la
- `2019 · pi` — Dolores es una paciente ingresada en la planta a la que le han insertado un tubo de gastrostomía. Te dispones a darle la

### 34. La infección nosocomial se define como:

**4 formulaciones** · años **2016, 2021** · temas — · similitud media 0.956 · score **6.5**

- `2016 · libre` — La infección nosocomial se define como:
- `2016 · pi` — La infección nosocomial se define como:
- `2021 · libre` — Una infección nosocomial se define como:
- `2021 · pi` — Una infección nosocomial se define como:

### 35. Con las nuevas tendencias de atención a la salud, impulsadas por la Ley General de Sanidad de 1986 (LGS), los Servicios de Salud M

**4 formulaciones** · años **2016, 2019** · temas T03 · similitud media 0.954 · score **6.49**

- `2016 · libre` — Con las nuevas tendencias de atención a la salud, impulsadas por la Ley General de Sanidad de 1986 (LGS), los Servicios 
- `2016 · pi` — Con las nuevas tendencias de atención a la salud, impulsadas por la Ley General de Sanidad de 1986 (LGS), los Servicios 
- `2019 · libre` — Con las nuevas tendencias de atención a la salud, impulsadas por la Ley General de Sanidad de 1986 (LGS), los Servicios 
- `2019 · pi` — Con las nuevas tendencias de atención a la salud, impulsadas por la Ley General de Sanidad de 1986 (LGS), los Servicios 

### 36. La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:

**4 formulaciones** · años **2016, 2021, 2022** · temas T06 · similitud media 0.788 · score **6.46**

- `2016 · pi` — Prevención de riesgos laborales entendido como "condición de trabajo", cualquier característica del mismo que pueda tene
- `2021 · libre` — La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:
- `2021 · pi` — La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:
- `2022 · aplazada` — Señale la afirmación correcta sobre el objeto de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, 

### 37. El Artículo 47 de la Ley de Salud de Andalucía determina que el Sistema Sanitario Público de Andalucía se organiza en demarcacione

**4 formulaciones** · años **2016, 2019, 2022** · temas T03, T04 · similitud media 0.784 · score **6.43**

- `2016 · libre` — El Decreto 197/2007, de 3 de julio, ha venido a regular la estructura, organización y funcionamiento de los servicios de
- `2019 · libre` — No forma parte del objeto de la Ley de Salud de Andalucía, expresado en su primer Artículo…
- `2019 · libre` — El Artículo 47 de la Ley de Salud de Andalucía determina que el Sistema Sanitario Público de Andalucía se organiza en de
- `2022 · aplazada` — El Artículo 47 de la Ley de Salud de Andalucía (Ley 2/1998, de 15 de junio) determina que el Sistema Sanitario Público d

### 38. ¿Quién fue la pionera mundial en la atención a los pacientes con enfermedades en fase terminal? :

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 0.938 · score **6.38**

- `2016 · libre` — ¿Quién fue la pionera mundial en la atención a los pacientes con enfermedades en fase terminal? :
- `2016 · pi` — ¿Quién fue la pionera mundial en la atención a los pacientes con enfermedades en fase terminal? :
- `2019 · libre` — ¿Quién fue la pionera mundial en la atención a los pacientes con enfermedades en fase terminal? :
- `2019 · pi` — ¿Quién fue la pionera mundial en la atención a los pacientes con enfermedades en fase terminal? :

### 39. De las siguientes posiciones, ¿cuál se utiliza para la higiene del cabello en un paciente encamado?

**4 formulaciones** · años **2024, 2025** · temas — · similitud media 0.931 · score **6.33**

- `2024 · centros_sas` — De las siguientes posiciones, ¿cuál se utiliza para la higiene del cabello en un paciente encamado?
- `2024 · apes` — De las siguientes posiciones, ¿cuál se utiliza para la higiene del cabello en un paciente encamado?
- `2025 · libre` — Para una correcta higiene del cabello en los pacientes encamados, ¿en qué posición debemos colocarla/o?
- `2025 · pi` — Para una correcta higiene del cabello en los pacientes encamados, ¿en qué posición debemos colocarla/o?

### 40. La vía de administración más útil en pediatría, es:

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 0.924 · score **6.28**

- `2016 · libre` — La vía de administración más útil en pediatría, es:
- `2016 · pi` — La vía de administración más útil en pediatría, es:
- `2019 · libre` — La vía de administración más útil en pediatría, es:
- `2019 · pi` — La vía de administración más útil en pediatría, es:

---

_Generado por `scripts/semantico.py`. Revisar agrupaciones dudosas y ajustar `--umbral` si hace falta (bajar = más grupos, subir = menos)._
