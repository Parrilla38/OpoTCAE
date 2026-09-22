export interface Opciones {
  A: string;
  B: string;
  C: string;
  D: string;
}

export type Letra = keyof Opciones;

export interface Ocurrencia {
  id: string;
  exam_id: string;
  anio: number;
  modalidad: string;
  numero: number;
  correcta: string | null;
}

export interface Cluster {
  cluster_id: number;
  tema: number | null;
  tema_nombre: string | null;
  tema_corto: string;
  /** Clave estable para filtrar: nº de tema del BOJA, o "clinica" / "otros". */
  clave: Selector;
  enunciado: string;
  opciones: Opciones;
  correcta: string | null;
  frecuencia: number;
  anios: number[];
  n_anios: number;
  score: number;
  articulos: number[];
  match: string;
  ocurrencias: Ocurrencia[];
}

/** Un tema del BOJA es su número; lo que el temario no enumera es "clinica"/"otros". */
export type Selector = number | "clinica" | "otros";

export interface Pregunta {
  id: string;
  cluster_id: number | null;
  exam_id: string;
  anio: number;
  fecha: string;
  modalidad: string;
  numero: number;
  enunciado: string;
  opciones: Opciones;
  correcta: string | null;
  es_reserva: boolean;
  parte: string | null;
  tema: number | null;
  tema_nombre: string | null;
  tema_corto?: string | null;
  bloque?: string;
}

export interface Examen {
  exam_id: string;
  anio: number;
  fecha: string;
  modalidad: string;
  n_preguntas_comun: number;
  cluster_ids: number[];
}

export interface TemaMeta {
  tema: number | null;
  /** Misma clave que lleva cada clúster. Sirve para filtrar. */
  clave: Selector;
  nombre: string;
  corto: string;
  clusters: number;
  preguntas: number;
  score_total: number;
  es_clinica?: boolean;
  /** Presente cuando el tema existe en el temario pero no ha caído nunca. */
  nota?: string;
}

export interface Meta {
  fuente: string;
  aviso: string;
  anios: number[];
  temas: TemaMeta[];
  totales: {
    preguntas: number;
    clusters: number;
    repetidos: number;
    multi_anio: number;
    examenes: number;
    conceptos?: number;
    conceptos_multi_anio?: number;
  };
  score_formula: string;
}

export interface MiembroConcepto {
  id: string;
  exam_id: string;
  anio: number;
  modalidad: string;
  numero: number;
  tema: number | null;
  enunciado: string;
  correcta: string | null;
  cluster_id: number | null;
  /** Opciones de esta formulación, para poder estudiar su respuesta. */
  opciones?: Opciones;
}

export interface Concepto {
  concepto_id: number;
  rank: number;
  representante: string;
  n_preguntas: number;
  anios: number[];
  n_anios: number;
  temas: number[];
  similitud_media: number;
  score: number;
  miembros: MiembroConcepto[];
}

export interface ConceptosData {
  modelo: string;
  umbral: number;
  n_conceptos_total: number;
  n_multi_anio: number;
  conceptos: Concepto[];
}

export interface ResultadoPregunta {
  cluster_id: number;
  elegida: Letra | null;
  acierto: boolean;
}

export interface IntentoTest {
  id: string;
  fecha: string;
  config: ConfigTest;
  resultados: ResultadoPregunta[];
  aciertos: number;
  fallos: number;
  en_blanco: number;
  nota: number;
}

export interface ConfigTest {
  n: number;
  penalizacion: number;
  filtro: "repetidas" | "tema" | "errores" | "todas";
  tema: number | null;
  cronometrado: boolean;
  minutos: number;
}

export interface Progreso {
  intentos: IntentoTest[];
  errores: Record<number, number>;
  aciertos: Record<number, number>;
  visitados: Record<number, number>;
}
