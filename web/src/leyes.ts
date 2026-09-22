/** Ficha de una norma (sin su articulado, que pesa). */
export interface NormaIndice {
  clave: string;
  nombre: string;
  corto: string;
  abrev: string;
  origen: string | null;
  fuente: string;
  temas: number[];
  n_articulos: number;
}

export interface Articulo {
  numero: number;
  titulo: string;
  epigrafe: string;
  texto: string;
}

export interface Norma extends NormaIndice {
  articulos: Record<string, Articulo>;
}

const caché: Record<string, unknown> = {};

async function carga<T>(ruta: string): Promise<T> {
  if (ruta in caché) return caché[ruta] as T;
  const res = await fetch(ruta);
  if (!res.ok) throw new Error(`No se pudo cargar ${ruta} (${res.status})`);
  const datos = (await res.json()) as T;
  caché[ruta] = datos;
  return datos;
}

/** Índice de normas: ligero, se pide una sola vez. */
export function cargaIndiceNormas(): Promise<NormaIndice[]> {
  return carga<NormaIndice[]>("leyes/indice.json");
}

/** Articulado completo de una norma. Se pide solo al abrir un artículo. */
export function cargaNorma(clave: string): Promise<Norma> {
  return carga<Norma>(`leyes/${clave}.json`);
}

/**
 * Normas que pueden contener un artículo citado en un tema concreto.
 * Un tema puede tener más de una norma (p. ej. T03: LGS y Ley 2/1998): se
 * devuelven todas y la UI muestra el artículo donde exista de verdad.
 */
export async function normasDeTema(tema: number | null): Promise<NormaIndice[]> {
  const indice = await cargaIndiceNormas();
  if (tema === null) return indice;
  const directas = indice.filter((n) => n.temas.includes(tema));
  return directas.length ? directas : indice;
}

/**
 * Busca un artículo por número dentro de las normas de un tema.
 * Devuelve solo las normas donde ese artículo exista de verdad: nunca se
 * inventa texto legal.
 */
export async function buscaArticulo(
  tema: number | null,
  numero: number
): Promise<{ norma: Norma; articulo: Articulo }[]> {
  const candidatas = await normasDeTema(tema);
  const hallados: { norma: Norma; articulo: Articulo }[] = [];
  for (const ind of candidatas) {
    if (!ind.n_articulos) continue;
    try {
      const norma = await cargaNorma(ind.clave);
      const art = norma.articulos[String(numero)];
      if (art) hallados.push({ norma, articulo: art });
    } catch {
      /* norma sin articulado embebido */
    }
  }
  return hallados;
}
