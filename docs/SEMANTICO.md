# Matching semántico — conceptos repetidos

Modelo **paraphrase-multilingual-MiniLM-L12-v2** · umbral de similitud **0.72** · 1504 preguntas analizadas.

Agrupa preguntas que pregunten **lo mismo con otras palabras**. Es el complemento al clustering literal: donde `radar.py` encuentra enunciados idénticos, esto encuentra el concepto subyacente.

- **487** conceptos con ≥2 formulaciones distintas
- **126** de ellos caen en **2 o más años distintos** (la señal fuerte de «esto se repite»)
- 234 preguntas quedaron como formulación única

## Conceptos que caen en varios años

Ordenados por `score = nº preguntas × (1 + 0,35 × años) × similitud_media`.

### 1. La ley 41/2002, básica reguladora de la autonomía del paciente y derechos y obligaciones en materia de información y documentación

**10 formulaciones** · años **2016, 2019, 2021, 2022, 2024** · temas T09, T11 · similitud media 0.82 · score **22.55**

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

### 2. El dispositivo asistencial de salud mental, destinado a atender las necesidades de hospitalización en salud mental de la población

**12 formulaciones** · años **2016, 2022, 2024, 2025** · temas T26 · similitud media 0.772 · score **22.23**

- `2016 · libre` — El Hospital de Día de Salud Mental es:
- `2016 · pi` — El Hospital de Día de Salud Mental es:
- `2022 · aplazada` — La Comunidad Terapéutica de Salud Mental, es:
- `2024 · centros_sas` — La estructura organizativa responsable de la atención especializada a la salud mental de la población, que incorpora los
- `2024 · centros_sas` — ¿Cuál es el dispositivo de atención ambulatoria con el que se coordinan el resto de dispositivos asistenciales de atenci
- `2024 · apes` — La estructura organizativa responsable de la atención especializada a la salud mental de la población, que incorpora los
- `2024 · apes` — ¿Cuál es el dispositivo de atención ambulatoria con el que se coordinan el resto de dispositivos asistenciales de atenci
- `2024 · aplazada` — El dispositivo asistencial de salud mental, destinado a atender las necesidades de hospitalización en salud mental de la
- `2024 · aplazada` — ¿A qué tipo de dispositivo pertenece la unidad cuya finalidad es el tratamiento intensivo de pacientes con Trastorno Men
- `2025 · libre` — ¿Cuál es el dispositivo que tiene como finalidad el tratamiento intensivo de pacientes con Trastorno Mental Grave que re
- `2025 · pi` — ¿Cuál es el dispositivo que tiene como finalidad el tratamiento intensivo de pacientes con Trastorno Mental Grave que re
- `2025 · aplazada` — De las siguientes funciones, ¿cuál pertenece al hospital de día de salud mental?

### 3. Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posición de de

**11 formulaciones** · años **2019, 2021, 2024, 2025** · temas T24 · similitud media 0.775 · score **20.47**

- `2019 · libre` — Señala la respuesta correcta en cuanto a los factores situacionales de las ulceras por presión:
- `2019 · pi` — Señala la respuesta correcta en cuanto a los factores situacionales de las ulceras por presión:
- `2021 · libre` — De las siguientes medidas relacionadas con el manejo de la presión en pacientes sentados, ¿cuál llevarías a cabo con un 
- `2021 · libre` — Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posi
- `2021 · libre` — ¿En cuál de las siguientes situaciones NO sería necesario reevaluar el riesgo de desarrollar úlceras por presión en un p
- `2021 · pi` — De las siguientes medidas relacionadas con el manejo de la presión en pacientes sentados, ¿cuál llevarías a cabo con un 
- `2021 · pi` — Para la prevención de las úlceras por presión, ¿qué zonas corporales del paciente se han de proteger cuándo está en posi
- `2021 · pi` — ¿En cuál de las siguientes situaciones NO sería necesario reevaluar el riesgo de desarrollar úlceras por presión en un p
- `2024 · aplazada` — Las posiciones anatómicas básicas del plan de cuidados en la prevención de úlceras por presión son:
- `2024 · aplazada` — En la prevención de las úlceras por presión, ¿cuál es la escala que valora: incontinencia, nutrición/ingesta, estado men
- `2025 · aplazada` — ¿Qué escala de valoración del riesgo de padecer úlceras por presión es recomendada por la NIC, NOC, y la GNEAUPP?

### 4. La definición de úlcera por presión (UPP) es:

**10 formulaciones** · años **2016, 2019, 2021, 2025** · temas T24 · similitud media 0.832 · score **19.97**

- `2016 · libre` — La definición de ulcera por presión es:
- `2016 · pi` — La definición de ulcera por presión es:
- `2019 · libre` — La definición de úlcera por presión (UPP) es:
- `2019 · pi` — La definición de úlcera por presión (UPP) es:
- `2021 · libre` — ¿Qué definirías por úlcera por presión?
- `2021 · libre` — El orden en el proceso de cicatrización de una úlcera por presión (UPP) sería:
- `2021 · pi` — ¿Qué definirías por úlcera por presión?
- `2021 · pi` — El orden en el proceso de cicatrización de una úlcera por presión (UPP) sería:
- `2025 · libre` — Las úlceras por presión (UPP) son lesiones de origen:
- `2025 · pi` — Las úlceras por presión (UPP) son lesiones de origen:

### 5. Antes de ponerle el enema debemos de colocar al paciente en posición:

**10 formulaciones** · años **2016, 2019, 2021** · temas T21, T23 · similitud media 0.805 · score **16.5**

- `2016 · libre` — Antes de ponerle un enema debemos de colocar al paciente en posición:
- `2016 · pi` — Antes de ponerle un enema debemos de colocar al paciente en posición:
- `2019 · libre` — Para mover los miembros inferiores del paciente debemos:
- `2019 · libre` — Antes de ponerle el enema debemos de colocar al paciente en posición:
- `2019 · pi` — Para mover los miembros inferiores del paciente debemos:
- `2019 · pi` — Antes de ponerle el enema debemos de colocar al paciente en posición:
- `2021 · libre` — Cuando colocamos al paciente con los brazos extendidos a lo largo del cuerpo, en decúbito supino con las piernas separad
- `2021 · libre` — La posición en la que el paciente está colocado en posición decúbito lateral, con la espalda alineada al borde de la cam
- `2021 · pi` — Cuando colocamos al paciente con los brazos extendidos a lo largo del cuerpo, en decúbito supino con las piernas separad
- `2021 · pi` — La posición en la que el paciente está colocado en posición decúbito lateral, con la espalda alineada al borde de la cam

### 6. En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un tratamiento cur

**7 formulaciones** · años **2019, 2021, 2022, 2024** · temas T28 · similitud media 0.842 · score **14.15**

- `2019 · libre` — Cual de éstos párrafos es correcto, hablando de Cuidados Paliativos:
- `2019 · pi` — Cual de éstos párrafos es correcto, hablando de Cuidados Paliativos:
- `2021 · libre` — La atención a los pacientes cuya enfermedad no responde a tratamiento curativo, y cuyo fin es lograr la mayor calidad de
- `2021 · pi` — La atención a los pacientes cuya enfermedad no responde a tratamiento curativo, y cuyo fin es lograr la mayor calidad de
- `2022 · aplazada` — Indica la definición correcta de cuidados paliativos según la Organización Mundial de la Salud:
- `2024 · centros_sas` — En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un trata
- `2024 · apes` — En relación con la atención a los pacientes, cuyo objetivo es aumentar la calidad de vida cuando no responden a un trata

### 7. Se define almacenamiento de residuos como:

**8 formulaciones** · años **2016, 2021, 2025** · temas T18 · similitud media 0.808 · score **13.25**

- `2016 · libre` — El almacenamiento temporal de residuos no debe superar nunca:
- `2016 · libre` — Plan de Gestión de Residuos de la Dirección General de Asistencia Sanitaria y Resultados en Salud. Los recipientes o env
- `2016 · pi` — El almacenamiento temporal de residuos no debe superar nunca:
- `2016 · pi` — Plan de Gestión de Residuos de la Dirección General de Asistencia Sanitaria y Resultados en Salud. Los recipientes o env
- `2021 · libre` — Se define almacenamiento de residuos como:
- `2021 · pi` — Se define almacenamiento de residuos como:
- `2025 · libre` — En general, el tiempo de almacenamiento final, por parte de los productores de los residuos peligrosos, no excederá de:
- `2025 · pi` — En general, el tiempo de almacenamiento final, por parte de los productores de los residuos peligrosos, no excederá de:

### 8. Una infección nosocomial se define como:

**6 formulaciones** · años **2016, 2019, 2021** · temas T15 · similitud media 0.96 · score **11.81**

- `2016 · libre` — La infección nosocomial se define como:
- `2016 · pi` — La infección nosocomial se define como:
- `2019 · libre` — La infección nosocomial se define como:
- `2019 · pi` — La infección nosocomial se define como:
- `2021 · libre` — Una infección nosocomial se define como:
- `2021 · pi` — Una infección nosocomial se define como:

### 9. ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospitalario?

**7 formulaciones** · años **2019, 2021, 2022** · temas T15, T17 · similitud media 0.803 · score **11.53**

- `2019 · libre` — Una atención limpia es una atención más segura. A fin de prevenir la septicemia en la atención sanitaria que preste a An
- `2019 · pi` — Una atención limpia es una atención más segura. A fin de prevenir la septicemia en la atención sanitaria que preste a An
- `2021 · libre` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2021 · pi` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2022 · aplazada` — ¿Cuál es la medida individual que se considera más eficaz para reducir/eliminar la transmisión de gérmenes a nivel hospi
- `2022 · aplazada` — La medida más adecuada para evitar las infecciones cruzadas entre pacientes - personal asistencial es:
- `2022 · aplazada` — A lo largo de la jornada, los TCAE se lavan las manos frecuentemente ya que, como buenos profesionales, saben que la med

### 10. Para movilizar a un paciente encamado, tendremos en cuenta:

**8 formulaciones** · años **2016, 2019** · temas T23 · similitud media 0.838 · score **11.4**

- `2016 · libre` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2016 · libre` — La Auxiliar de Enfermería tiene que realizar el aseo de un paciente encamado para ello debe de:
- `2016 · pi` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2016 · pi` — La Auxiliar de Enfermería tiene que realizar el aseo de un paciente encamado para ello debe de:
- `2019 · libre` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2019 · libre` — Antonia junto con su compañera Belén, también técnico en cuidados de enfermería, tiene que realizar el aseo de un pacien
- `2019 · pi` — Para movilizar a un paciente encamado, tendremos en cuenta:
- `2019 · pi` — Antonia junto con su compañera Belén, también técnico en cuidados de enfermería, tiene que realizar el aseo de un pacien

### 11. La obligación de guardar secreto profesional, afecta a:

**6 formulaciones** · años **2016, 2019, 2022** · temas T09 · similitud media 0.918 · score **11.29**

- `2016 · libre` — La obligación de guardar secreto profesional, afecta a:
- `2016 · pi` — La obligación de guardar secreto profesional, afecta a:
- `2019 · libre` — La obligación de guardar secreto profesional, afecta a:
- `2019 · pi` — La obligación de guardar secreto profesional, afecta a:
- `2022 · aplazada` — ¿En qué caso se puede romper el secreto profesional?
- `2022 · aplazada` — La obligación de guardar secreto profesional, afecta a:

### 12. ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?

**6 formulaciones** · años **2021, 2022, 2024, 2025** · temas T18 · similitud media 0.765 · score **11.02**

- `2021 · libre` — ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?
- `2021 · pi` — Los restos de material de pequeñas curas, bolsas de orina vacías, filtros de diálisis, pañales y yesos, pertenecen al gr
- `2021 · pi` — ¿Cuál de las siguientes definiciones se corresponde con la de residuo sanitario del Grupo II?
- `2022 · aplazada` — Las agujas sanitarias son un residuo:
- `2024 · aplazada` — ¿Qué tipo de residuos no pueden compactarse o triturarse, en ningún caso?
- `2025 · aplazada` — ¿En qué grupo se clasifican los residuos hospitalarios excretados que pueden transmitir el cólera?

### 13. Que observación es incorrecta en la administración por vía rectal:

**6 formulaciones** · años **2016, 2019, 2021** · temas — · similitud media 0.894 · score **11.0**

- `2016 · libre` — Que observación es incorrecta en la administración por vía rectal:
- `2016 · pi` — Que observación es incorrecta en la administración por vía rectal:
- `2019 · libre` — Que observación no es correcta en la administración por vía rectal:
- `2019 · pi` — Que observación no es correcta en la administración por vía rectal:
- `2021 · libre` — ¿Qué observación NO es correcta en la administración de medicación por vía rectal?
- `2021 · pi` — ¿Qué observación NO es correcta en la administración de medicación por vía rectal?

### 14. Para realizar la higiene bucal en pacientes inconscientes; cuál de estas acciones no es la correcta:

**6 formulaciones** · años **2016, 2019, 2021** · temas T20 · similitud media 0.883 · score **10.86**

- `2016 · libre` — Para realizar la higiene bucal en pacientes inconscientes debemos tener en cuenta cuál de estas acciones no es la correc
- `2016 · pi` — Para realizar la higiene bucal en pacientes inconscientes debemos tener en cuenta cuál de estas acciones no es la correc
- `2019 · libre` — Para realizar la higiene bucal en pacientes inconscientes; cuál de estas acciones no es la correcta:
- `2019 · pi` — Para realizar la higiene bucal en pacientes inconscientes; cuál de estas acciones no es la correcta:
- `2021 · libre` — Señale la respuesta correcta en cuanto a la limpieza de la boca en un paciente inconsciente.
- `2021 · pi` — Señale la respuesta correcta en cuanto a la limpieza de la boca en un paciente inconsciente.

### 15. Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental que desar

**6 formulaciones** · años **2016, 2019, 2025** · temas T22 · similitud media 0.874 · score **10.75**

- `2016 · libre` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2016 · pi` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2019 · libre` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2019 · pi` — Con respecto a la Alimentación en la mujer gestante, cada sustancia nutritiva tiene, entre otras, una misión fundamental
- `2025 · libre` — ¿Cómo se llaman los nutrientes que aportan al organismo humano gran cantidad de vitaminas y sales minerales?
- `2025 · pi` — ¿Cómo se llaman los nutrientes que aportan al organismo humano gran cantidad de vitaminas y sales minerales?

### 16. De los principales eslabones de la cadena epidemiológica, cual es la afirmación mas correcta:

**5 formulaciones** · años **2016, 2019, 2021** · temas T15 · similitud media 0.97 · score **9.94**

- `2016 · pi` — De los principales eslabones de la cadena epidemiológica, cual es la correcta:
- `2019 · libre` — De los principales eslabones de la cadena epidemiológica, cual es la afirmación mas correcta:
- `2019 · pi` — De los principales eslabones de la cadena epidemiológica, cual es la afirmación mas correcta:
- `2021 · libre` — Los eslabones de la cadena epidemiológica son:
- `2021 · pi` — Los eslabones de la cadena epidemiológica son:

### 17. El cuidado del ombligo debe hacerse:

**6 formulaciones** · años **2016, 2019, 2024** · temas T20 · similitud media 0.798 · score **9.82**

- `2016 · libre` — El cuidado del ombligo debe hacerse:
- `2016 · libre` — En nuestro turno de tarde / noche tenemos un paciente encamado al que le realizaremos los cuidados generales como:
- `2016 · pi` — El cuidado del ombligo debe hacerse:
- `2016 · pi` — En nuestro turno de tarde / noche tenemos un paciente encamado al que le realizaremos los cuidados generales como:
- `2019 · pi` — El cuidado del ombligo debe hacerse:
- `2024 · aplazada` — La higiene de un paciente encamado hay que realizarla por partes. ¿Cuál es la última parte que se debe lavar a un pacien

### 18. En los enfermos renales está indicada una dieta:

**5 formulaciones** · años **2016, 2019, 2025** · temas T22 · similitud media 0.945 · score **9.69**

- `2016 · libre` — En los enfermos renales está indicada una dieta:
- `2016 · pi` — En los enfermos renales está indicada una dieta:
- `2019 · libre` — En los enfermos renales está indicada una dieta:
- `2019 · pi` — En los enfermos renales está indicada una dieta:
- `2025 · aplazada` — La dieta hipoproteica está prescrita o indicada en pacientes que padecen:

### 19. Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH, ¿a que grupo de clasificación corr

**5 formulaciones** · años **2016, 2019, 2024** · temas T18 · similitud media 0.915 · score **9.38**

- `2016 · pi` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH a que grupo corresponde:
- `2019 · libre` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH, ¿a que grupo de clasific
- `2019 · pi` — Los residuos procedentes de Hemodiálisis de pacientes no contaminados por virus VHC, VHB y VIH, ¿a que grupo de clasific
- `2024 · centros_sas` — En el grupo II Residuos sanitarios asimilables a urbanos, se incluyen:
- `2024 · apes` — En el grupo II Residuos sanitarios asimilables a urbanos, se incluyen:

### 20. Las vitaminas se clasifican en:

**5 formulaciones** · años **2016, 2019, 2022** · temas T22 · similitud media 0.911 · score **9.34**

- `2016 · libre` — Las vitaminas se clasifican en:
- `2016 · pi` — Las vitaminas se clasifican en:
- `2019 · libre` — Las vitaminas se clasifican en:
- `2019 · pi` — Las vitaminas se clasifican en:
- `2022 · aplazada` — Entre las vitaminas hidrosolubles se encuentran:

### 21. El masaje cardiaco externo en adultos, ¿con qué frecuencia debe de realizarse?

**5 formulaciones** · años **2016, 2019, 2022** · temas T29 · similitud media 0.891 · score **9.13**

- `2016 · libre` — El masaje cardiaco externo en adultos, ¿con qué frecuencia debe de realizarse?
- `2016 · pi` — El masaje cardiaco externo en adultos, ¿con qué frecuencia debe de realizarse?
- `2019 · libre` — El masaje cardiaco externo en adultos, ¿con qué frecuencia debe de realizarse?
- `2019 · pi` — El masaje cardiaco externo en adultos, ¿con qué frecuencia debe de realizarse?
- `2022 · aplazada` — ¿Cómo se realiza y cuál sería la posición del masaje cardiaco en neonatos?

### 22. En una Parada Cardiorrespiratoria, el cerebro empieza a deteriorarse aproximadamente:

**5 formulaciones** · años **2016, 2019, 2022** · temas T29 · similitud media 0.871 · score **8.93**

- `2016 · libre` — En una Parada Cardiorrespiratoria, el cerebro empieza a deteriorarse aproximadamente:
- `2016 · pi` — En una Parada Cardiorrespiratoria, el cerebro empieza a deteriorarse aproximadamente:
- `2019 · libre` — En una PCR (Parada Cardio Respiratoria), el cerebro empieza a deteriorarse aproximadamente:
- `2019 · pi` — En una PCR (Parada Cardio Respiratoria), el cerebro empieza a deteriorarse aproximadamente:
- `2022 · aplazada` — ¿Cuántos minutos son necesarios para que el cerebro humano comience a deteriorarse sin oxígeno?

### 23. Algunos de los objetivos de los cuidados preoperatorios son:

**6 formulaciones** · años **2016, 2019** · temas T25 · similitud media 0.863 · score **8.8**

- `2016 · libre` — Algunos de los objetivos de los cuidados preoperatorios son:
- `2016 · pi` — Algunos de los objetivos de los cuidados preoperatorios son:
- `2019 · libre` — Algunos de los objetivos de los cuidados preoperatorios son:
- `2019 · libre` — Son pacientes susceptibles de visita pre-quirúrgica:
- `2019 · pi` — Algunos de los objetivos de los cuidados preoperatorios son:
- `2019 · pi` — Son pacientes susceptibles de visita pre-quirúrgica:

### 24. Los colores de los contenedores que se utilizan en la gestión de residuos son:

**5 formulaciones** · años **2016, 2019, 2021** · temas T18 · similitud media 0.85 · score **8.71**

- `2016 · pi` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2019 · libre` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2019 · pi` — Los colores de los contenedores que se utilizan en la gestión de residuos son:
- `2021 · libre` — ¿A qué grupo pertenecen los residuos que se recogen en bolsa de color rojo y contenedores, reciclables o de un solo uso,
- `2021 · pi` — ¿A qué grupo pertenecen los residuos que se recogen en bolsa de color rojo y contenedores, reciclables o de un solo uso,

### 25. El Biobanco del SSPA depende de:

**5 formulaciones** · años **2016, 2019, 2022** · temas T03 · similitud media 0.838 · score **8.59**

- `2016 · libre` — Los valores de los Biobancos del SSPA son:
- `2016 · pi` — Los valores de los Biobancos del SSPA son:
- `2019 · libre` — El Biobanco del SSPA depende de:
- `2019 · pi` — El Biobanco del SSPA depende de:
- `2022 · aplazada` — El Biobanco del SSPA se encuentra bajo la dependencia de:

### 26. Leonardo, paciente con hemiplejia, está encamado por un cuadro febril. Hay que movilizarlo. ¿Dónde nos colocaríamos?

**6 formulaciones** · años **2016, 2019** · temas T21 · similitud media 0.838 · score **8.55**

- `2016 · libre` — Leonardo, paciente con hemiplejia, está encamado por un cuadro febril. Hay que movilizarlo. ¿Dónde nos colocaríamos?
- `2016 · pi` — Leonardo, paciente con hemiplejia, está encamado por un cuadro febril. Hay que movilizarlo. ¿Dónde nos colocaríamos?
- `2019 · libre` — Leonardo es paciente con hemiplejia ingresado en la habitación 501 A, está encamado por un cuadro febril, su familiar ll
- `2019 · libre` — Leonardo sufre de incontinencia urinaria, ¿qué cuidados le brindaría?
- `2019 · pi` — Leonardo es paciente con hemiplejia ingresado en la habitación 501 A, está encamado por un cuadro febril, su familiar ll
- `2019 · pi` — Leonardo sufre de incontinencia urinaria, ¿qué cuidados le brindaría?

### 27. ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?

**6 formulaciones** · años **2022, 2024** · temas T24 · similitud media 0.833 · score **8.5**

- `2022 · aplazada` — Según el sistema de clasificación/estadiaje de las úlceras por presión, ¿qué estadio corresponde una úlcera por presión 
- `2024 · centros_sas` — ¿En qué estadio se encuentra una úlcera por presión, cuando existe un eritema cutáneo en piel intacta que no cede al des
- `2024 · centros_sas` — ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?
- `2024 · apes` — ¿En qué estadio se encuentra una úlcera por presión, cuando existe un eritema cutáneo en piel intacta que no cede al des
- `2024 · apes` — ¿Cuál es la zona del cuerpo en las que aparece con mayor frecuencia las úlceras por presión?
- `2024 · aplazada` — ¿En qué zonas presenta úlceras por presión un paciente colocado en decúbito lateral?

### 28. ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?

**6 formulaciones** · años **2021, 2025** · temas T14, T28 · similitud media 0.83 · score **8.47**

- `2021 · libre` — Los valores y principios de la Bioética son:
- `2021 · pi` — Los valores y principios de la Bioética son:
- `2025 · libre` — ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?
- `2025 · pi` — El rechazo al tratamiento, ¿dentro de qué principio básico de la Bioética se encuadraría?
- `2025 · pi` — ¿En qué principios de la Bioética se encuadrarían los cuidados paliativos?
- `2025 · aplazada` — ¿Sobre qué principios de la Bioética se apoya toda la asistencia sanitaria?

### 29. Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los drenajes d

**5 formulaciones** · años **2016, 2019, 2022** · temas — · similitud media 0.815 · score **8.36**

- `2016 · libre` — Rocío es intervenida de reconstrucción mamaria. Cuando sube a planta trae dos drenajes de aspiración (Redón). Como norma
- `2016 · pi` — Rocío es intervenida de reconstrucción mamaria. Cuando sube a planta trae dos drenajes de aspiración (Redón). Como norma
- `2019 · libre` — Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los 
- `2019 · pi` — Cuando Julia sube a planta después de su intervención, trae dos drenajes de aspiración (Redón). Como norma general, los 
- `2022 · aplazada` — El drenaje que tiene colocado María es un drenaje de aspiración tipo Redon. ¿Qué precaución debe usted tener con este ti

### 30. El núcleo de la aplicación informática Diraya se estructura en:

**5 formulaciones** · años **2016, 2019, 2022** · temas T10 · similitud media 0.807 · score **8.28**

- `2016 · libre` — La finalidad del proyecto Diraya es:
- `2016 · pi` — La finalidad del proyecto Diraya es:
- `2019 · libre` — El núcleo de la aplicación informática Diraya se estructura en:
- `2019 · pi` — El núcleo de la aplicación informática Diraya se estructura en:
- `2022 · aplazada` — El núcleo de DIRAYA está formado por:

### 31. Que factores se predisponen a la infección respiratoria:

**5 formulaciones** · años **2016, 2021, 2022** · temas — · similitud media 0.808 · score **8.28**

- `2016 · libre` — Que factores se predisponen a la infección respiratoria:
- `2016 · pi` — Que factores se predisponen a la infección respiratoria:
- `2021 · libre` — ¿Cuál de las siguientes infecciones requiere precaución de transmisión aérea?
- `2021 · pi` — ¿Cuál de las siguientes infecciones requiere precaución de transmisión aérea?
- `2022 · aplazada` — Con respecto a las infecciones nosocomiales, se debe saber que:

### 32. El medico de familia de su centro de Salud tras la valoración de un paciente que ha acudido a su consulta decide debe ser atendido

**6 formulaciones** · años **2016, 2019** · temas T26 · similitud media 0.81 · score **8.26**

- `2016 · libre` — Para su correcto funcionamiento, la Atención Primaria se considera puerta de entrada y filtro hacia los servicios especi
- `2016 · libre` — En el equipo de atención comunitaria, la atención de salud mental sigue un modelo integral de atención interdisciplinari
- `2016 · pi` — Para su correcto funcionamiento, la Atención Primaria se considera puerta de entrada y filtro hacia los servicios especi
- `2016 · pi` — En el equipo de atención comunitaria, la atención de salud mental sigue un modelo integral de atención interdisciplinari
- `2019 · libre` — El medico de familia de su centro de Salud tras la valoración de un paciente que ha acudido a su consulta decide debe se
- `2019 · pi` — El medico de familia de su centro de Salud tras la valoración de un paciente que ha acudido a su consulta decide debe se

### 33. La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:

**5 formulaciones** · años **2016, 2021, 2022** · temas T06 · similitud media 0.761 · score **7.8**

- `2016 · libre` — Según se recoge en el artículo 26. Protección de la maternidad de la Ley 31/95 de Prevención de Riesgos Laborales, si lo
- `2016 · pi` — Prevención de riesgos laborales entendido como "condición de trabajo", cualquier característica del mismo que pueda tene
- `2021 · libre` — La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:
- `2021 · pi` — La función de vigilancia y control de la normativa sobre prevención de riesgos laborales corresponde:
- `2022 · aplazada` — Señale la afirmación correcta sobre el objeto de la Ley 31/1995, de 8 de noviembre, de Prevención de Riesgos Laborales, 

### 34. La Unidad de rehabilitación de salud mental es el dispositivo asistencial de salud mental que está enfocado a:

**5 formulaciones** · años **2019, 2025** · temas T26 · similitud media 0.869 · score **7.38**

- `2019 · libre` — La Unidad de rehabilitación de salud mental es el dispositivo asistencial de salud mental que está enfocado a:
- `2019 · pi` — La Unidad de rehabilitación de salud mental es el dispositivo asistencial de salud mental que está enfocado a:
- `2025 · libre` — ¿Cómo se denomina la Unidad de Salud Mental que funciona como un dispositivo que tiene por objeto la recuperación de hab
- `2025 · pi` — ¿Cómo se denomina la Unidad de Salud Mental que funciona como un dispositivo que tiene por objeto la recuperación de hab
- `2025 · aplazada` — Dentro del contexto de un hospital de día de salud mental, ¿qué significa la "rehabilitación psicosocial"?

### 35. El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas para invest

**4 formulaciones** · años **2021, 2022, 2024** · temas T03, T19 · similitud media 0.859 · score **7.05**

- `2021 · libre` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas p
- `2021 · pi` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA), en su área de tejidos, sustancias y muestras biológicas p
- `2022 · aplazada` — El Biobanco del SSPA, en su área de tejidos, sustancias y muestras biológicas para investigación, está organizado como u
- `2024 · aplazada` — El Biobanco del Sistema Sanitario Público de Andalucía (SSPA) lleva a cabo una actividad descentralizada a través de sus

### 36. A que se denomina ASEPSIA:

**4 formulaciones** · años **2016, 2019** · temas T16 · similitud media 1.0 · score **6.8**

- `2016 · libre` — A que se denomina ASEPSIA:
- `2016 · pi` — A que se denomina ASEPSIA:
- `2019 · libre` — A que se denomina ASEPSIA:
- `2019 · pi` — A que se denomina ASEPSIA:

### 37. El uso de bastones en la deambulación:

**4 formulaciones** · años **2016, 2019** · temas T23 · similitud media 1.0 · score **6.8**

- `2016 · libre` — El uso de bastones en la deambulación:
- `2016 · pi` — El uso de bastones en la deambulación:
- `2019 · libre` — El uso de bastones en la deambulación:
- `2019 · pi` — El uso de bastones en la deambulación:

### 38. ¿Qué es la clasificación de SPAUDING?

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 1.0 · score **6.8**

- `2016 · libre` — ¿Qué es la clasificación de SPAUDING?
- `2016 · pi` — ¿Qué es la clasificación de SPAUDING?
- `2019 · libre` — ¿Qué es la clasificación de SPAUDING?
- `2019 · pi` — ¿Qué es la clasificación de SPAUDING?

### 39. La vía de administración más útil en pediatría, es:

**4 formulaciones** · años **2016, 2019** · temas — · similitud media 1.0 · score **6.8**

- `2016 · libre` — La vía de administración más útil en pediatría, es:
- `2016 · pi` — La vía de administración más útil en pediatría, es:
- `2019 · libre` — La vía de administración más útil en pediatría, es:
- `2019 · pi` — La vía de administración más útil en pediatría, es:

### 40. Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Patologías c

**4 formulaciones** · años **2016, 2019** · temas T27 · similitud media 0.998 · score **6.79**

- `2016 · libre` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2016 · pi` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2019 · libre` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa
- `2019 · pi` — Debilidad muscular. Déficit de la marcha y equilibrio. Deterioro cognitivo. Polimedicación. Disminución de la visión. Pa

---

_Generado por `scripts/semantico.py`. Revisar agrupaciones dudosas y ajustar `--umbral` si hace falta (bajar = más grupos, subir = menos)._
