"""Clasificador por tema del temario oficial TCAE SAS (Res. 31-jul-2024, BOJA 153).

Los 29 temas del temario. Se evalúan de MÁS a MENOS específico: si una pregunta
de úlceras por presión menciona también «movilización», manda UPP (T24).

Bloque COMÚN (1-10) y ESPECÍFICO (11-29). El etiquetado es por palabras clave
con revisión manual en el dump de validación.

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
    1: "La Constitución Española de 1978",
    2: "El Estatuto de Autonomía para Andalucía",
    3: "Organización sanitaria (I): SSPA",
    4: "Organización sanitaria (II): Consejería de Salud y SAS",
    5: "Protección de datos y transparencia",
    6: "Prevención de riesgos laborales",
    7: "Igualdad y violencia de género en Andalucía",
    8: "Estatuto Marco del personal estatutario",
    9: "Autonomía del paciente y derechos y deberes",
    10: "TIC en el SAS",
    11: "La documentación sanitaria",
    12: "El trabajo en equipo y la comunicación",
    13: "La atención al usuario",
    14: "Principios fundamentales de la Bioética",
    15: "Higiene hospitalaria e infección relacionada con la asistencia",
    16: "Limpieza, desinfección y esterilización",
    17: "El aislamiento hospitalario",
    18: "Gestión de los residuos sanitarios",
    19: "Muestras biológicas: obtención, conservación y transporte",
    20: "Atención y cuidados en las necesidades de higiene",
    21: "Atención y cuidados en las necesidades de eliminación",
    22: "Atención y cuidados en las necesidades de alimentación",
    23: "Atención y cuidados en las necesidades de movilización",
    24: "Atención y cuidados de las úlceras por presión",
    25: "Preparación del paciente para exploración o intervención quirúrgica",
    26: "Atención y cuidados al paciente de Salud Mental",
    27: "Atención y cuidados en el anciano",
    28: "Atención al paciente en situación terminal y cuidados paliativos",
    29: "Reanimación cardiopulmonar básica y primeros auxilios",
}

ABREVIATURAS = {
    1: "Constitución", 2: "Estatuto Andalucía", 3: "Organización sanitaria I",
    4: "Organización sanitaria II", 5: "Protección de datos", 6: "Prevención riesgos",
    7: "Igualdad y violencia género", 8: "Estatuto Marco", 9: "Autonomía del paciente",
    10: "TIC SAS", 11: "Documentación sanitaria", 12: "Equipo y comunicación",
    13: "Atención al usuario", 14: "Bioética", 15: "Higiene hospitalaria / IRA",
    16: "Limpieza y esterilización", 17: "Aislamiento hospitalario", 18: "Residuos sanitarios",
    19: "Muestras biológicas", 20: "Necesidad de higiene", 21: "Necesidad de eliminación",
    22: "Necesidad de alimentación", 23: "Necesidad de movilización", 24: "Úlceras por presión",
    25: "Exploración y quirófano", 26: "Salud mental", 27: "El anciano",
    28: "Terminal y paliativos", 29: "RCP y primeros auxilios",
}

# (tema, regex) en orden: gana el primero que encaje. Los específicos clínicos
# van ANTES que los legales porque son más estrechos.
REGLAS: list[tuple[int, re.Pattern]] = [
    # ── T29 · RCP y primeros auxilios ──
    (29, re.compile(
        r"reanimaci[óo]n cardiopulmonar|\bRCP\b|soporte vital b[áa]sico|\bSVB\b|"
        r"desfibrilador|\bDEA\b|parada cardiorrespiratoria|\bPCR\b|"
        r"masaje cardiaco|compresiones tor[áa]cicas|frecuencia.*compresion|"
        r"maniobra de heimlich|obstrucci[óo]n de la v[íi]a a[ée]rea|"
        r"primeros auxilios|valoraci[óo]n primaria|"
        r"quemadura|fractura|esguince|luxaci[óo]n|intoxicaci[óo]n|"
        r"hemorragia.*externa|torniquete|vendaje compresivo|"
        r"posici[óo]n lateral de seguridad|"
        r"carro de parada|cuidados cr[íi]ticos|zona de cuidados|"
        r"pinzas.*cuerpo extra[ñn]o|cuerpo extra[ñn]o.*v[íi]a a[ée]rea|"
        r"emergencia.*define|definici[óo]n.*emergencia|situaci[óo]n que altera.*orden normal|"
        r"dolor agudo|intensidad del dolor|escala.*dolor|m[ée]todos subjetivos.*dolor",
        re.I)),

    # ── T24 · Úlceras por presión ──
    (24, re.compile(
        r"[úu]lcera[s]? por presi[óo]n|\bUPP\b|[úu]lcera[s]? de dec[úu]bito|"
        r"lesiones por presi[óo]n|escala de norton|escala de braden|escala de waterlow|"
        r"prevenci[óo]n de [úu]lceras|tratamiento de [úu]lceras|"
        r"cura de [úu]lceras|ap[óo]sito|cambio postural.*[úu]lcera|"
        r"estad[íi]o de la [úu]lcera|grado de la [úu]lcera|"
        r"[úu]lceras? iatrog[ée]nicas|iatrog[ée]nica.*piel|"
        r"escala de.*percepci[óo]n sensorial|humedad.*actividad f[íi]sica",
        re.I)),

    # ── T26 · Salud mental ──
    (26, re.compile(
        r"salud mental|trastorno mental|trastornos mentales|"
        r"esquizofrenia|trastorno bipolar|trastorno depresivo|"
        r"depresi[óo]n mayor|ansiedad generalizada|trastorno de ansiedad|"
        r"intento autol[íi]tico|conducta suicida|ideaci[óo]n suicida|"
        r"contenci[óo]n mec[áa]nica|sujeci[óo]n del paciente|"
        r"unidad de agudos|unidad de salud mental|rehabilitaci[óo]n psicosocial|"
        r"alucinaci[óo]n|delirium|crisis de angustia|trastorno de la conducta alimentaria|"
        r"personalidad l[íi]mite|trastorno obsesivo-compulsivo|trastorno de p[áa]nico|"
        r"desorientaci[óo]n|estado de desorientaci[óo]n|paciente desorientado|"
        r"cuadro confusional|agitaci[óo]n psicomotora|insomnio.*psiqui|"
        r"conducta del paciente|trastornos de la conducta",
        re.I)),

    # ── T28 · Terminal y paliativos ──
    (28, re.compile(
        r"paciente terminal|cuidados paliativos|final de la vida|final de vida|"
        r"sedaci[óo]n paliativa|sedaci[óo]n terminal|tanatolog[íi]a|duelo|"
        r"soporte vital avanzado|limitaci[óo]n del esfuerzo terap[ée]utico|"
        r"distanasia|ortotanasia|eutanasia|suicidio asistido|"
        r"cuidados al cad[áa]ver|cuidados post[- ]mortem|toilette del cad[áa]ver|"
        r"situaci[óo]n de agon[íi]a|sintomatolog[íi]a final|"
        r"muerte digna|declaraci[óo]n de voluntades anticipadas.*final",
        re.I)),

    # ── T27 · El anciano ──
    (27, re.compile(
        r"ancianos?|personas mayores|geriatr[íi]a|gerontolog[íi]a|"
        r"s[íi]ndrome geri[áa]trico|valoraci[óo]n geri[áa]trica|"
        r"demencia|alzheimer|deterioro cognitivo|"
        r"s[íi]ndrome de inmovilidad|fragilidad del anciano|"
        r"edadismo|residencia de mayores|centro de d[íi]a|"
        r"dependencia del anciano|persona mayor institucionalizada",
        re.I)),

    # ── T25 · Exploración y quirófano ──
    (25, re.compile(
        r"quir[óo]fano|intervenci[óo]n quir[úu]rgica|cirug[íi]a|"
        r"preoperatorio|prequir[úu]rgico|postoperatorio|postquir[úu]rgico|"
        r"pre-operatoria|preparaci[óo]n f[íi]sica del paciente|fase pre-?operatoria|"
        r"preparaci[óo]n del paciente.*exploraci|preparaci[óo]n del paciente.*intervenci|"
        r"exploraci[óo]n complementaria|exploraci[óo]n radiol[óo]gica|"
        r"endoscopia|colonoscopia|gastroscopia|broncoscopia|"
        r"radiograf[íi]a|tomograf[íi]a|\bTAC\b|resonancia magn[ée]tica|ecograf[íi]a|"
        r"punci[óo]n lumbar|biopsia|"
        r"cateterismo (?:card[íi]aco|cardiaco|vascular|venoso|central|arterial)|"
        r"hemodin[áa]mica|"
        r"rasurado prequir|ayunas prequir|consentimiento quir[úu]rgico|"
        r"bata quir[úu]rgica|gorro quir|campo quir[úu]rgico|"
        r"posici[óo]n quir[úu]rgica|anestesia general|anestesia local|sedaci[óo]n para exploraci",
        re.I)),

    # ── T19 · Muestras biológicas ──
    (19, re.compile(
        r"muestra[s]? biol[óo]gica|obtenci[óo]n de muestras|conservaci[óo]n de muestras|"
        r"transporte de muestras|cadena de custodia.*muestra|"
        r"hemocultivo|urocultivo|coprocultivo|esputo|baciloscopia|"
        r"exudado far[íi]ngeo|exudado nasal|hisopo|"
        r"tubo de ensayo|tapa del tubo|color de la tapa|"
        r"hemograma|bioqu[íi]mica|anal[íi]tica de sangre|extracci[óo]n de sangre|"
        r"punci[óo]n venosa|venopunci[óo]n|extracci[óo]n venosa|"
        r"reacci[óo]n de mantoux|muestra de orina|recogida de orina|recogida de heces|"
        r"urinocultivo|uocultivo|coprocultivo|"
        r"frasco de recogida|contenedor de muestras|"
        r"estudio.*bioqu[íi]mico|paciente debe.*extracci|ayunas.*extracci|"
        r"error en la identificaci[óo]n de la muestra",
        re.I)),

    # ── T18 · Residuos sanitarios ──
    (18, re.compile(
        r"residuos sanitarios|residuos cl[íi]nicos|gesti[óo]n de residuos|"
        r"plan de gesti[óo]n de residuos|residuos peligrosos|residuos biosanitarios|"
        r"grupo I\b|grupo II\b|grupo III\b|grupos de residuos|clasificaci[óo]n de residuos|"
        r"contenedor amarillo|contenedor negro|contenedor blanco|contenedor rojo|"
        r"puntocortantes|punzocortantes|c[áa]psula del rotulo|"
        r"aguja desechable|eliminaci[óo]n de material cortante|"
        r"valorizaci[óo]n de residuos|incineraci[óo]n de residuos|"
        r"almacenamiento.*residuo|almacenamiento temporal.*residuo|"
        r"residuos radiactivos|residuos citost[áa]ticos|residuos quimioter[áa]picos|"
        r"residuos excretados|transmitir el c[óo]lera|residuos infecciosos|"
        r"productores de residuos|tratamiento de residuos|vertedero de residuos",
        re.I)),

    # ── T16 · Limpieza, desinfección y esterilización ──
    (16, re.compile(
        r"esterilizaci[óo]n|material est[ée]ril|t[ée]cnica as[ée]ptica|asepsia|"
        r"autoclave|vapor saturado|[óo]xido de etileno|plasma.*esteriliz|"
        r"m[ée]todo de esterilizaci[óo]n|indicador qu[íi]mico|indicador biol[óo]gico|"
        r"desinfecci[óo]n de alto nivel|desinfecci[óo]n de nivel intermedio|"
        r"descontaminaci[óo]n|prelavado del material|"
        r"limpieza del material|material de un solo uso|material reutilizable|"
        r"clorhexidina|alcohol de 70|hipoclorito|glutaraldeh[íi]do|per[óo]xido de hidr[óo]geno|"
        r"tiempo de contacto del desinfectante|reprocesado del material|"
        r"central de esterilizaci[óo]n|"
        r"detergente|detergentes|pH.*detergente|detergente.*pH|"
        r"limpieza.*incubadora|incubadora.*limpieza|"
        r"pr[áa]ctica adecuada de limpieza|proceso de limpieza|"
        r"desinfectante de superficies|limpieza de superficies|"
        r"material de curas.*limpieza|instrumental quir[úu]rgico.*limpieza",
        re.I)),

    # ── T17 · Aislamiento hospitalario ──
    (17, re.compile(
        r"aislamiento del paciente|aislamiento hospitalario|"
        r"aislamiento de contacto|aislamiento respiratorio|aislamiento por gotas|"
        r"aislamiento a[ée]reo|aislamiento estricto|"
        r"equipo de protecci[óo]n individual|\bEPI\b|"
        r"bata de aislamiento|mascarilla.*aislamiento|guantes de aislamiento|"
        r"habitaci[óo]n de aislamiento|presi[óo]n negativa|"
        r"precauciones de transmisión|precauciones de transmisi[óo]n|"
        r"elemento.*entrar en la habitaci[óo]n|antes de entrar en la habitaci[óo]n",
        re.I)),

    # ── T20 · Necesidad de higiene ──
    (20, re.compile(
        r"aseo del paciente|ba[ñn]o del paciente|ba[ñn]o en cama|ducha en cama|"
        r"higiene del paciente|higiene corporal|higiene bucal|higiene dental|"
        r"higiene del encamado|higiene de la persona encamada|"
        r"cepillado dental|higiene de la boca en inconscientes|"
        r"cuidado del cabello|cuidado de las u[ñn]as|"
        r"lavado del cabello en cama|cuidado del ombligo|higiene del reci[ée]n nacido|"
        r"higiene se define|definici[óo]n de higiene|la higiene.*consiste|"
        r"prevenci[óo]n de lesiones en la piel por higiene",
        re.I)),

    # ── T21 · Necesidad de eliminación ──
    (21, re.compile(
        r"eliminaci[óo]n.*orina|eliminaci[óo]n.*deposiciones|necesidad de eliminaci[óo]n|"
        r"diuresis|medici[óo]n de la diuresis|balance h[íi]drico|"
        r"sonda urinaria|sondaje vesical|bolsa de orina|recogida de orina de 24 horas|"
        r"sonda de foley|sonda de doble v[íi]a|sonda de tres v[íi]a|tipo de sonda|"
        r"calibre de la sonda|globo de la sonda|cateterismo vesical|sonda.*permanencia|"
        r"incontinencia urinaria|incontinencia fecal|"
        r"estre[ñn]imiento|diarrea|catarsis|oclusi[óo]n intestinal|"
        r"cat[áa]rtico|enema|lavativa|"
        r"ileostom[íi]a|colostom[íi]a|estoma|"
        r"retenci[óo]n urinaria|globo vesical|sacacat[ée]teres",
        re.I)),

    # ── T22 · Necesidad de alimentación ──
    (22, re.compile(
        r"alimentaci[óo]n del paciente|nutrici[óo]n del paciente|necesidad de alimentaci[óo]n|"
        r"dieta blanda|dieta l[íi]quida|dieta pastosa|dieta astringente|dieta baja en sodio|"
        r"dieta diab[ée]tica|dieta hipocal[óo]rica|dieta hiperprot[ée]ica|"
        r"dieta sin residuos|dieta de textura modificada|dieta recomendable|"
        r"disfagia|degluci[óo]n|"
        r"alimentaci[óo]n enteral|nutrici[óo]n enteral|sonda nasog[áa]strica|\bSNG\b|"
        r"gastrostom[íi]a|nutrici[óo]n parenteral|alimentaci[óo]n parenteral|"
        r"hidrataci[óo]n del paciente|balance hidrico|"
        r"alergia alimentaria|intolerancia alimentaria|"
        r"edulcorante|conservante|aditivo alimentario|colorante alimentario|"
        r"[áa]cidos grasos|vitamina|vitaminas|tiamina|riboflavina|"
        r"anorexia|bulimia|obesidad|[íi]ndice de masa corporal|"
        r"insulina|metabolismo.*insulina|hormonas.*metabolismo|"
        r"glucemia|hiperglucemia|hipoglucemia|cetosis|cetoacidosis|"
        r"dieta hipogluc|alimentos.*energ[ée]tica|valor cal[óo]rico|"
        r"nutrientes|hidratos de carbono|prote[íi]nas.*dieta|l[íi]pidos.*dieta",
        re.I)),

    # ── T23 · Necesidad de movilización ──
    (23, re.compile(
        r"movilizaci[óo]n del paciente|mec[áa]nica corporal|movilidad del paciente|"
        r"movilizaci[óo]n precoz|levantar al paciente|ponerlo de pie|deambulaci[óo]n precoz|"
        r"dec[úu]bito supino|dec[úu]bito prono|dec[úu]bito lateral|"
        r"posici[óo]n de fowler|posici[óo]n de sims|posici[óo]n de trendelenburg|"
        r"posici[óo]n ginecol[óo]gica|posici[óo]n de litotom[íi]a|"
        r"dec[úu]bito pélvico|posici[óo]n de rosenthal|"
        r"traslado del paciente|cambio postural|"
        r"ayudas t[ée]cnicas|muletas|bast[óo]n|silla de ruedas|andadera|"
        r"gr[úu]a de traslado|tablero de traslado|cinta deslizante|"
        r"prevenci[óo]n de ca[íi]das|barrera en la cama|cama antica[íi]das|"
        r"bipedestaci[óo]n|marcha del paciente|"
        r"ergonom[íi]a del traslado|espalda del cuidador|"
        r"paciente encamado.*moviliz|moviliz.*encamado|rehabilitaci[óo]n motora",
        re.I)),

    # ── T15 · Higiene hospitalaria e IRA ──
    (15, re.compile(
        r"infecci[óo]n relacionada con la asistencia|\bIRA\b|infecci[óo]n nosocomial|"
        r"infecci[óo]n intrahospitalaria|higiene hospitalaria|"
        r"control de infecciones|comisi[óo]n de infecciones|"
        r"precauciones est[áa]ndar|precauciones est[áa]ndares|"
        r"cadena de transmisi[óo]n|fuente de infecci[óo]n|"
        r"higiene de manos|lavado de manos|desinfecci[óo]n de manos|"
        r"gel hidroalcoh[óo]lico|\bGHA\b|"
        r"infecci[óo]n de v[íi]a urinaria.*sonda|infecci[óo]n de herida quir[úu]rgica|"
        r"neumon[íi]a asociada a ventilaci[óo]n|"
        r"antibioticoterapia.*profilaxis|resistencia bacteriana|"
        r"interacciones.*agente y hu[ée]sped|triada epidemiol[óo]gica|cadena epidemiol[óo]gica",
        re.I)),

    # ── T14 · Bioética ──
    (14, re.compile(
        r"bio[ée]tica|principios? bio[ée]tic|principio bio[ée]tico|"
        r"beneficencia|no maleficencia|"
        r"dilema [ée]tico|conflicto [ée]tico|"
        r"comisi[óo]n de bio[ée]tica|comisi[óo]n deontol[óo]gica|"
        r"c[óo]digo deontol[óo]gico|[ée]tica profesional|"
        r"principio de justicia.*bio[ée]t|principio de autonom[íi]a.*bio[ée]t|"
        r"justicia.*bio[ée]tic|bio[ée]tic.*justicia|"
        r"investigaci[óo]n biom[ée]dica.*[ée]tic|comit[ée] de [ée]tica",
        re.I)),

    # ── T12 · Trabajo en equipo y comunicación ──
    (12, re.compile(
        r"trabajo en equipo|equipo de trabajo|equipo multidisciplinar|equipo asistencial|"
        r"comunicaci[óo]n verbal|comunicaci[óo]n no verbal|comunicaci[óo]n terap[ée]utica|"
        r"definici[óo]n.*comunicaci[óo]n|comunicaci[óo]n se define|comunicaci[óo]n.*denomina|"
        r"empat[íi]a|escucha activa|asertividad|asertivo|"
        r"liderazgo|l[íi]der del equipo|estilos de liderazgo|"
        r"motivaci[óo]n del equipo|clima laboral|"
        r"resoluci[óo]n de conflictos|gesti[óo]n de conflictos|"
        r"din[áa]mica de grupos|roles del grupo|grupo de trabajo|"
        r"reuni[óo]n de equipo|sesi[óo]n cl[íi]nica|pase de guardia|informaci[óo]n de guardia|"
        r"burnout|s[íi]ndrome de desgaste profesional|estr[ée]s laboral.*equipo|"
        r"agresi[óo]n al profesional|acoso laboral|mobbing|"
        r"desgaste profesional|fatiga por compasi[óo]n|"
        r"comunicaci[óo]n no verbal.*manifest|lenguaje corporal|gestos.*emociones",
        re.I)),

    # ── T13 · Atención al usuario ──
    (13, re.compile(
        r"atenci[óo]n al usuario|atenci[óo]n al paciente|atenci[óo]n sanitaria al usuario|"
        r"acogida del paciente|acogida del usuario|"
        r"informaci[óo]n al usuario|informaci[óo]n al paciente|"
        r"carta de servicios|satisfacci[óo]n del usuario|satisfacci[óo]n del paciente|"
        r"quejas y sugerencias|libro de reclamaciones|hojas de reclamaciones|"
        r"defensor del paciente|"
        r"entrevista con el paciente|entrevista cl[íi]nica|"
        r"relaci[óo]n terap[ée]utica|relaci[óo]n de ayuda|"
        r"derivar al paciente|derivaci[óo]n asistencial|"
        r"acceso a la atenci[óo]n|lista de espera|"
        r"cuidados.*delegad|funciones delegadas.*higiene|"
        r"derechos del usuario.*sanitario|carta de derechos.*usuario",
        re.I)),

    # ── T11 · Documentación sanitaria ──
    (11, re.compile(
        r"documentaci[óo]n sanitaria|documentaci[óo]n cl[íi]nica|documentaci[óo]n de enfermer[íi]a|"
        r"registro de enfermer[íi]a|hoja de evoluci[óo]n|hoja de enfermer[íi]a|"
        r"hoja de balance|hoja de constantes|hoja de medicaci[óo]n|"
        r"protocolo de documentaci[óo]n|"
        r"c[óo]digo \bCIE\b|clasificaci[óo]n internacional de enfermedades|"
        r"codificaci[óo]n diagn[óo]stica|"
        r"informe de alta|informe de enfermer[íi]a|epicrisis|"
        r"cierre de historia|apertura de historia|archivo de historias|"
        r"resonancia de la historia|copiador de historia|"
        r"pulseras identificativas|identificaci[óo]n del paciente|datos inequ[íi]vocos|"
        r"documentaci[óo]n obligatoria.*paciente|historia cl[íi]nica.*document",
        re.I)),

    # ─────────────── bloque común (1-10) ───────────────

    # ── T10 · TIC SAS ──
    (10, re.compile(
        r"\bDAH[- ]?ECC\b|\bDAH[- ]?EXT\b|\bDAH[- ]?EG\b|\bHSAP\b|\bDiraya\b|"
        r"historia de salud digital|expediente cl[íi]nico electr[óo]nico|"
        r"receta electr[óo]nica|telemedicina|teleasistencia sanitaria|"
        r"tecnolog[íi]as? de la informaci[óo]n y la comunicaci[óo]n|"
        r"aplicaci[óo]n.*hospitalariamente.*datos cl[íi]nicos",
        re.I)),

    # ── T5 · Protección de datos ──
    (5, re.compile(
        r"protecci[óo]n de datos|LOPDGDD|LOPD|RGPD|Reglamento \(UE\) 2016/679|"
        r"ley org[áa]nica 3/2018|agencia espa[ñn]ola de protecci[óo]n de datos|"
        r"datos de car[áa]cter personal|consentimiento.*datos|"
        r"derecho de acceso.*datos|derecho de rectificaci[óo]n|derecho de supresi[óo]n|"
        r"derecho al olvido|transparencia.*informaci[óo]n p[úu]blica|ley 19/2013",
        re.I)),

    # ── T6 · Prevención de riesgos laborales ──
    (6, re.compile(
        r"prevenci[óo]n de riesgos laborales|ley 31/1995|riesgo laboral|riesgos laborales|"
        r"inspecci[óo]n de trabajo|instituto nacional de seguridad e higiene|"
        r"servicio de prevenci[óo]n|t[ée]cnico superior en prevenci[óo]n|"
        r"acci[óo]n preventiva|evaluaci[óo]n de riesgos|plan de prevenci[óo]n|"
        r"ergonom[íi]a|psicosociolog[íi]a aplicada|higiene industrial|"
        r"seguridad y salud en el trabajo|riesgo psicosocial|"
        r"acoso laboral|estr[ée]s laboral|s[íi]ndrome de desgaste|"
        r"mutua.*acci[óo]n social|"
        r"ex[áa]menes de salud.*trabajador|vigilancia de la salud.*trabajador|"
        r"enfermedades? infecciosas.*riesgo|fluidos biol[óo]gicos.*riesgo|"
        r"riesgo biol[óo]gico|riesgo qu[íi]mico|riesgo f[íi]sico|riesgo el[ée]ctrico|"
        r"agentes biol[óo]gicos|carga de trabajo|esfuerzo f[íi]sico.*trabajo",
        re.I)),

    # ── T7 · Igualdad y violencia de género ──
    (7, re.compile(
        r"violencia de g[ée]nero|ley 13/2007|ley org[áa]nica 1/2004|ley org[áa]nica 3/2007|"
        r"ley 12/2007|igualdad de g[ée]nero|igualdad de trato|igualdad efectiva|"
        r"discriminaci[óo]n por raz[óo]n de sexo|plan andaluz.*igualdad|"
        r"perspectiva de g[ée]nero|unidad de valoraci[óo]n.*g[ée]nero|"
        r"protocolo.*acoso.*sexual|acoso sexual",
        re.I)),

    # ── T8 · Estatuto Marco ──
    (8, re.compile(
        r"estatuto marco|ley 55/2003|personal estatutario|estatutario fijo|estatutario temporal|"
        r"promoci[óo]n interna|provisi[óo]n de puestos|movilidad voluntaria|"
        r"situaciones administrativas|servicios especiales|excedencia|"
        r"trienios|r[ée]tribuciones b[áa]sicas|complemento de destino|"
        r"r[ée]gimen disciplinario|faltas leves|faltas graves|faltas muy graves|"
        r"\bLOPS\b|ley 44/2003|profesiones sanitarias|colegios profesionales|"
        r"\bEBEP\b|ley 7/2007.*empleado p[úu]blico|funcionario|empleados p[úu]blicos|"
        r"incompatibilidades|r[ée]gimen de incompatibilidades",
        re.I)),

    # ── T9 · Autonomía del paciente ──
    (9, re.compile(
        r"autonom[íi]a del paciente|ley 41/2002|consentimiento informado|"
        r"consentimiento por representaci[óo]n|instrucciones previas|voluntades anticipadas|"
        r"testamento vital|historia cl[íi]nica|derechos del paciente|carta de derechos|"
        r"derecho a la informaci[óo]n asistencial|revocar.*consentimiento|"
        r"confidencialidad.*paciente|secreto profesional|"
        r"intimidad del paciente|dignidad del paciente",
        re.I)),

    # ── T2 · Estatuto de Autonomía ──
    (2, re.compile(
        r"estatuto de autonom[íi]a|ley org[áa]nica 2/2007|parlamento de andaluc[íi]a|"
        r"consejo de gobierno de la junta|presidente de la junta de andaluc[íi]a|"
        r"junta de andaluc[íi]a|defensor del pueblo andaluz|"
        r"tribunal de cuentas de andaluc[íi]a|diputaciones provinciales|"
        r"competencias exclusivas de andaluc[íi]a|"
        r"art[íi]?c?u?l?o?\s*\.?\s*\d+.*estatuto de autonom|"
        r"estatuto de autonom.*art[íi]?c?u?l?o?\s*\.?\s*\d+|"
        r"s[íi]mbolos de andaluc[íi]a|d[íi]a de andaluc[íi]a|escudo de andaluc[íi]a|"
        r"himno de andaluc[íi]a|bandera de andaluc[íi]a",
        re.I)),

    # ── T3 · Organización sanitaria (I) ──
    (3, re.compile(
        r"sistema sanitario p[úu]blico de andaluc[íi]a|\bSSPA\b|ley 2/1998|"
        r"ley de salud de andaluc[íi]a|plan andaluz de salud|"
        r"[áa]reas de gesti[óo]n sanitaria|[áa]reas de salud|zonas b[áa]sicas de salud|"
        r"sistema nacional de salud|\bSNS\b|ley 14/1986|ley general de sanidad|"
        r"ley 16/2003|cohesi[óo]n y calidad del SNS|consejo interterritorial|"
        r"principios.*universalidad|principios.*generalidad|"
        r"financiaci[óo]n.*servicios sanitarios|"
        r"biobanco del sistema sanitario|centros.*investigaci[óo]n biom[ée]dica|"
        r"ley 14/2007.*investigaci[óo]n biom[ée]dica",
        re.I)),

    # ── T4 · Organización sanitaria (II) ──
    (4, re.compile(
        r"servicio andaluz de salud|\bSAS\b|consejer[íi]a de salud|"
        r"consejer[íi]a de salud y familias|consejer[íi]a de salud y consumo|"
        r"direcci[óo]n gerencia|direcciones gerencias|"
        r"atenci[óo]n primaria de salud|centro de salud|"
        r"unidades de gesti[óo]n cl[íi]nica|\bUGC\b|hospital.*servicio andaluz|"
        r"ley 8/1986.*servicio andaluz|agencia p[úu]blica empresarial|agencia administrativa|"
        r"consejo andaluz de salud|foro marco para el di[áa]logo social|cartera de servicios|"
        r"direcci[óo]n de salud|direcci[óo]n m[ée]dica|comisi[óo]n de direcci[óo]n",
        re.I)),

    # ── T1 · Constitución Española ──
    (1, re.compile(
        r"constituci[óo]n espa[ñn]ola|constituci[óo]n de 1978|\bCE\b|cortes generales|"
        r"congreso de los diputados|tribunal constitucional|tribunal supremo|"
        r"consejo general del poder judicial|poder judicial|defensor del pueblo|"
        r"tribunal de cuentas|consejo de estado|presidente del gobierno|"
        r"soberan[íi]a nacional|forma pol[íi]tica del estado|monarqu[íi]a parlamentaria|"
        r"valores superiores.*ordenamiento|art[íi]?c?u?l?o?\s*\.?\s*1\.1|art[íi]?c?u?l?o?\s*\.?\s*1\.2|"
        r"derechos fundamentales|libertades p[úu]blicas|garant[íi]as.*derechos|recurso de amparo|"
        r"estado de alarma|estado de excepci[óo]n|estado de sitio|"
        r"procedimiento de reforma|reforma constitucional|t[íi]tulo preliminar|"
        r"principio de legalidad|jerarqu[íi]a normativa|"
        r"irretroactividad de las disposiciones sancionadoras|seguridad jur[íi]dica|"
        r"responsabilidad del estado|inconstitucionalidad|partidos pol[íi]ticos|"
        r"sindicatos|organizaciones empresariales|sucesi[óo]n a la corona|regencia|refrendo",
        re.I)),

    # ── Clínica y anatomía ──
    # NO es uno de los 29 temas oficiales del BOJA 153. El examen incluye
    # anatomía, fisiología, patología, farmacología y obstetricia por ser
    # contenido implícito del título de TCAE (FP de Grado Medio). Se marca
    # como `bloque: "clinica"` para no confundirlo con el temario oficial.
    #
    # Esta regla va LA ÚLTIMA y solo debe contener material que no pertenece
    # a ningún tema oficial. Si se cuela algo de un tema 1-29, el clasificador
    # pierde esa pregunta: por eso no se mezclan palabras clave de otros temas.
    (30, re.compile(
        r"funciones? (?:del|de la|de los|de las)|[óo]rganos? (?:del|de la)|"
        r"gl[áa]ndula|hormona|hormonas|c[ée]lula[s]?|tejido[s]? |hueso|f[ée]mur|tibia|"
        r"articulaci[óo]n|sinartrosis|diartrosis|anfiartrosis|"
        r"anatom[íi]a|fisiolog[íi]a|patolog[íi]a|histolog[íi]a|"
        r"metabolismo|metabolitos|"
        r"arteria|vena|nervio|capilar|sistema cardiovascular|sistema nervioso|"
        r"sistema digestivo|sistema respiratorio|sistema musculoesquel[ée]tico|"
        r"sistema endocrino|sistema inmunol[óo]gico|sistema inmunitario|"
        r"h[íi]gado|ri[ñn][óo]n|pulm[óo]n|est[óo]mago|p[áa]ncreas|bazo|intestino|"
        r"cerebro|cerebelo|m[ée]dula [óo]sea|enc[ée]falo|meninges|"
        r"[úu]tero|ovocito|[óo]vulo|espermatozoide|embri[óo]n|feto|gestaci[óo]n|embarazo|parto|"
        r"amnio|amniocele|amniorrexis|placenta|l[íi]quido amni[óo]tico|"
        r"[óo]rganos? de los sentidos|retina|c[óo]rnea|t[íi]mpano|c[óo]clea|"
        r"dermis|epidermis|hipodermis|foliculo piloso|gl[áa]ndula sudor[íi]para|"
        r"enfermedad|s[íi]ndrome|tumor|neoplasia|c[áa]ncer|met[áa]stasis|"
        r"diabetes|hipertensi[óo]n|hipotensi[óo]n|anemia|edema|[íi]ctero|fiebre|"
        r"dolor (?:agudo|cr[óo]nico|persistente|neurop[áa]tico)|"
        r"f[áa]rmaco|medicamento|principio activo|dosis|v[íi]a de administraci[óo]n|"
        r"agonista|antagonista|efecto secundario|interacci[óo]n farmacol|"
        r"ampolla|comprimido|jarabe|gotas|pomada|inyecci[óo]n|vial|"
        r"administraci[óo]n de f[áa]rmacos|v[íi]a intraneural|v[íi]a endovenosa|"
        r"v[íi]a intramuscular|v[íi]a subcut[áa]nea|v[íi]a oral|v[íi]a t[óo]pica|"
        r"odontofagia|odinofagia|disfon[íi]a|disnea|taquicardia|bradicardia|"
        r"hemograma|leucocito|hematies?|plaquetas?|hemoglobina|hematocrito|"
        r"c[ée]lulas destructoras del hueso|osteoclasto|osteoblasto|s[íi]nfisis|"
        r"cuadrantes del abdomen|regi[óo]n.*anat[óo]mica",
        re.I)),
]


def clasificar(texto: str) -> int | None:
    """Devuelve el tema (1-29) o None si no encaja en ninguno."""
    for tema, patron in REGLAS:
        if patron.search(texto):
            return tema
    return None


def main() -> int:
    preguntas = json.loads(SALIDA.read_text(encoding="utf-8"))
    conteo: dict[int, int] = {}
    sin_tema = 0
    for p in preguntas:
        if p.get("anulada"):
            p["tema"] = None
            p["bloque"] = "anulada"
            p["tema_nombre"] = None
            p["tema_corto"] = None
            continue
        # PRIMERO solo el enunciado: si entran las opciones, una opción que
        # mencione «estatuto» clasifica como T2 una pregunta de la LGS.
        tema = clasificar(p["enunciado"])
        if tema is None:
            tema = clasificar(f"{p['enunciado']} {' '.join(p['opciones'].values())}")
        p["tema"] = tema if tema != 30 else None
        p["bloque"] = (
            "clinica" if tema == 30
            else "comun" if tema and tema <= 10
            else "especifico" if tema
            else "sin_tema"
        )
        p["tema_nombre"] = (
            "Anatomía, fisiología y clínica" if tema == 30
            else TEMAS.get(tema) if tema
            else None
        )
        p["tema_corto"] = (
            "Anatomía y clínica" if tema == 30
            else ABREVIATURAS.get(tema) if tema
            else None
        )
        if tema == 30:
            conteo["clinica"] = conteo.get("clinica", 0) + 1
        elif tema:
            conteo[tema] = conteo.get(tema, 0) + 1
        else:
            sin_tema += 1

    SALIDA.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(v for k, v in conteo.items() if k != "clinica") + conteo.get("clinica", 0) + sin_tema
    comun = sum(v for t, v in conteo.items() if isinstance(t, int) and t <= 10)
    especifico = sum(v for t, v in conteo.items() if isinstance(t, int) and t > 10)
    clinica = conteo.get("clinica", 0)
    print("Clasificación por tema (preguntas no anuladas)")
    print("-" * 68)
    for t in sorted(k for k in conteo if isinstance(k, int)):
        marca = "común" if t <= 10 else "espec."
        print(f"  T{t:02d}  {conteo[t]:>5}  [{marca}]  {TEMAS[t]}")
    if clinica:
        print(f"  ----  {clinica:>5}  [clíni]  Anatomía, fisiología y clínica (transversal del título FP)")
    print(f"  ----  -----")
    print(f"  sin tema asignado: {sin_tema}")
    print("-" * 68)
    print(f"  TOTAL          {total:>5}")
    print(f"  bloque común   {comun:>5}  ({100*comun/total:.1f}%)")
    print(f"  específico     {especifico:>5}  ({100*especifico/total:.1f}%)")
    print(f"  clínica        {clinica:>5}  ({100*clinica/total:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
