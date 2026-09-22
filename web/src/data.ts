import type { Cluster, ConceptosData, Examen, Meta, Pregunta, Selector } from "./types";

/** Caché en memoria de los JSON, para no repetir fetch. */
const caché: Record<string, unknown> = {};

async function carga<T>(ruta: string): Promise<T> {
  if (ruta in caché) return caché[ruta] as T;
  const res = await fetch(ruta);
  if (!res.ok) throw new Error(`No se pudo cargar ${ruta} (${res.status})`);
  const datos = (await res.json()) as T;
  caché[ruta] = datos;
  return datos;
}

/**
 * Ligero: solo lo imprescindible para pintar la interfaz.
 * ~26 KB. Lo demás va bajo demanda para no atascar el móvil.
 */
export async function cargaBase(): Promise<{ meta: Meta; examenes: Examen[] }> {
  const [meta, examenes] = await Promise.all([
    carga<Meta>("data/meta.json"),
    carga<Examen[]>("data/examenes.json"),
  ]);
  return { meta, examenes };
}

/** Preguntas agrupadas (~955 KB). Para Practicar, Aprender y Mi progreso. */
export function cargaClusters(): Promise<Cluster[]> {
  return carga<Cluster[]>("data/clusters.json");
}

/** Preguntas por convocatoria (~1,2 MB). Solo la vista Exámenes. */
export function cargaPreguntas(): Promise<Pregunta[]> {
  return carga<Pregunta[]>("data/preguntas.json");
}

/** Conceptos por embeddings (~250 KB). Solo la pestaña Conceptos. */
export function cargaConceptos(): Promise<ConceptosData | null> {
  return carga<ConceptosData | null>("data/conceptos.json");
}

export function cohesion(sim: number): "alta" | "media" | "baja" {
  if (sim >= 0.85) return "alta";
  if (sim >= 0.78) return "media";
  return "baja";
}

export function ordenaPorScore<T extends { score: number }>(xs: T[]): T[] {
  return [...xs].sort((a, b) => b.score - a.score);
}

/** Filtra por tema del BOJA (número) o por el bloque «clinica» / «otros». */
export function porTema(clusters: Cluster[], sel: Selector): Cluster[] {
  return ordenaPorScore(clusters.filter((c) => c.clave === sel));
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
