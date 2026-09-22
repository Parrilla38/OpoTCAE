import type { ConfigTest, IntentoTest, Letra, Progreso, ResultadoPregunta } from "./types";
import type { EstadoSm2 } from "./sm2";
import { nuevaTarjeta, repasa } from "./sm2";

const CLAVE = "tcae-progreso-v1";
const CLAVE_SM2 = "tcae-sm2-v1";

export function cargaProgreso(): Progreso {
  try {
    const crudo = localStorage.getItem(CLAVE);
    if (!crudo) return { intentos: [], errores: {}, aciertos: {}, visitados: {} };
    const p = JSON.parse(crudo) as Progreso;
    return {
      intentos: p.intentos ?? [],
      errores: p.errores ?? {},
      aciertos: p.aciertos ?? {},
      visitados: p.visitados ?? {},
    };
  } catch {
    return { intentos: [], errores: {}, aciertos: {}, visitados: {} };
  }
}

export function guardaProgreso(p: Progreso): void {
  localStorage.setItem(CLAVE, JSON.stringify(p));
}

export function reiniciaProgreso(): void {
  localStorage.removeItem(CLAVE);
  localStorage.removeItem(CLAVE_SM2);
}

// ─────────────────────────── SM-2 ───────────────────────────

export function cargaSm2(): Record<number, EstadoSm2> {
  try {
    const crudo = localStorage.getItem(CLAVE_SM2);
    return crudo ? (JSON.parse(crudo) as Record<number, EstadoSm2>) : {};
  } catch {
    return {};
  }
}

export function guardaSm2(ts: Record<number, EstadoSm2>): void {
  localStorage.setItem(CLAVE_SM2, JSON.stringify(ts));
}

/** Da de alta una tarjeta si no existía (al fallar una pregunta). */
export function altaTarjeta(clusterId: number): void {
  const ts = cargaSm2();
  if (!ts[clusterId]) {
    ts[clusterId] = nuevaTarjeta(clusterId);
    guardaSm2(ts);
  }
}

/** Registra un repaso de la tarjeta con calidad q (0-5). */
export function repasaTarjeta(clusterId: number, q: number): EstadoSm2 {
  const ts = cargaSm2();
  const actual = ts[clusterId] ?? nuevaTarjeta(clusterId);
  const nuevo = repasa(actual, q);
  ts[clusterId] = nuevo;
  guardaSm2(ts);
  return nuevo;
}

export function reiniciaTarjeta(clusterId: number): void {
  const ts = cargaSm2();
  ts[clusterId] = nuevaTarjeta(clusterId);
  guardaSm2(ts);
}

export function registraIntento(
  config: ConfigTest,
  resultados: ResultadoPregunta[]
): IntentoTest {
  const p = cargaProgreso();
  let aciertos = 0;
  let fallos = 0;
  let en_blanco = 0;
  for (const r of resultados) {
    if (r.elegida === null) {
      en_blanco++;
      continue;
    }
    if (r.acierto) {
      aciertos++;
      p.aciertos[r.cluster_id] = (p.aciertos[r.cluster_id] ?? 0) + 1;
    } else {
      fallos++;
      p.errores[r.cluster_id] = (p.errores[r.cluster_id] ?? 0) + 1;
      altaTarjeta(r.cluster_id); // entra en repetición espaciada
    }
  }
  const bruto = aciertos - config.penalizacion * fallos;
  const nota = Math.max(0, Math.round((bruto / resultados.length) * 10 * 100) / 100);
  const intento: IntentoTest = {
    id: `${Date.now()}`,
    fecha: new Date().toISOString(),
    config,
    resultados,
    aciertos,
    fallos,
    en_blanco,
    nota,
  };
  p.intentos = [intento, ...p.intentos].slice(0, 50);
  guardaProgreso(p);
  return intento;
}

export function marcaVisitado(clusterId: number): void {
  const p = cargaProgreso();
  p.visitados[clusterId] = (p.visitados[clusterId] ?? 0) + 1;
  guardaProgreso(p);
}

export function idsConErrores(): number[] {
  const p = cargaProgreso();
  return Object.entries(p.errores)
    .filter(([, n]) => (n as number) > 0)
    .map(([k]) => Number(k));
}

export function cuentaErrores(clusterId: number): number {
  return cargaProgreso().errores[clusterId] ?? 0;
}

export function cuentaAciertos(clusterId: number): number {
  return cargaProgreso().aciertos[clusterId] ?? 0;
}

export function resumenProgreso(): {
  intentos: number;
  aciertos: number;
  fallos: number;
  clustersFallados: number;
  notaMedia: number;
} {
  const p = cargaProgreso();
  let aciertos = 0;
  let fallos = 0;
  let sumaNotas = 0;
  for (const i of p.intentos) {
    aciertos += i.aciertos;
    fallos += i.fallos;
    sumaNotas += i.nota;
  }
  return {
    intentos: p.intentos.length,
    aciertos,
    fallos,
    clustersFallados: Object.keys(p.errores).length,
    notaMedia: p.intentos.length ? Math.round((sumaNotas / p.intentos.length) * 100) / 100 : 0,
  };
}

export const CONFIG_DEFECTO: ConfigTest = {
  n: 10,
  penalizacion: 0.25,
  filtro: "repetidas",
  tema: null,
  cronometrado: false,
  minutos: 15,
};

export type { ConfigTest, Letra };
