import type { Cluster, ConceptosData, Examen, Meta, Pregunta } from "./types";

let _clusters: Cluster[] | null = null;
let _preguntas: Pregunta[] | null = null;
let _examenes: Examen[] | null = null;
let _meta: Meta | null = null;
let _conceptos: ConceptosData | null = null;

async function carga<T>(ruta: string): Promise<T> {
  const res = await fetch(ruta);
  if (!res.ok) throw new Error(`No se pudo cargar ${ruta} (${res.status})`);
  return (await res.json()) as T;
}

export async function cargaTodo(): Promise<{
  clusters: Cluster[];
  preguntas: Pregunta[];
  examenes: Examen[];
  meta: Meta;
  conceptos: ConceptosData | null;
}> {
  if (_clusters && _preguntas && _examenes && _meta) {
    return {
      clusters: _clusters,
      preguntas: _preguntas,
      examenes: _examenes,
      meta: _meta,
      conceptos: _conceptos,
    };
  }
  const [clusters, preguntas, examenes, meta, conceptos] = await Promise.all([
    carga<Cluster[]>("data/clusters.json"),
    carga<Pregunta[]>("data/preguntas.json"),
    carga<Examen[]>("data/examenes.json"),
    carga<Meta>("data/meta.json"),
    carga<ConceptosData>("data/conceptos.json").catch(() => null),
  ]);
  _clusters = clusters;
  _preguntas = preguntas;
  _examenes = examenes;
  _meta = meta;
  _conceptos = conceptos;
  return { clusters, preguntas, examenes, meta, conceptos };
}

/** Alta/Media/Baja cohesión intra-grupo según la similitud de coseno. */
export function cohesion(sim: number): "alta" | "media" | "baja" {
  if (sim >= 0.85) return "alta";
  if (sim >= 0.78) return "media";
  return "baja";
}

export function ordenaPorScore<T extends { score: number }>(xs: T[]): T[] {
  return [...xs].sort((a, b) => b.score - a.score);
}

export function porTema(clusters: Cluster[], tema: number): Cluster[] {
  return ordenaPorScore(clusters.filter((c) => c.tema === tema));
}

export function agrupaPorArticulo(clusters: Cluster[]): Map<number, Cluster[]> {
  const m = new Map<number, Cluster[]>();
  for (const c of clusters) {
    if (!c.articulos.length) {
      const k = 0;
      m.set(k, [...(m.get(k) ?? []), c]);
      continue;
    }
    for (const a of c.articulos) {
      m.set(a, [...(m.get(a) ?? []), c]);
    }
  }
  return m;
}

export function textoRespuesta(c: { opciones: Record<string, string>; correcta: string | null }, letra: string | null): string {
  if (!letra) return "—";
  return c.opciones[letra] ?? "—";
}
