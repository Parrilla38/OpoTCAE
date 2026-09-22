/** Repetición espaciada SM-2 (SuperMemo 2), sobre localStorage.
 *
 * Cada pregunta fallada es una «tarjeta». Tras cada repaso el usuario dice
 * cuánto le ha costado (0-5) y se recalcula el intervalo hasta el siguiente
 * repaso. Es el algoritmo clásico de Anki, simple y suficiente aquí.
 */

export interface EstadoSm2 {
  id: number;
  ef: number; // facilidad (1,3..2,5)
  n: number; // nº de respuestas correctas seguidas
  intervalo: number; // días hasta el próximo repaso
  proximo: number; // timestamp del próximo repaso
  repasos: number; // total de repasos hechos
  ultima: number; // timestamp del último repaso
}

const EF_INICIAL = 2.5;

export function nuevaTarjeta(id: number): EstadoSm2 {
  return { id, ef: EF_INICIAL, n: 0, intervalo: 0, proximo: Date.now(), repasos: 0, ultima: 0 };
}

/** q = calidad de la respuesta (0-5). <3 = fallada. */
export function repasa(t: EstadoSm2, q: number): EstadoSm2 {
  const ef = Math.max(1.3, t.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)));
  let n: number;
  let intervalo: number;
  if (q < 3) {
    n = 0;
    intervalo = 0; // se repite hoy
  } else {
    n = t.n + 1;
    if (n === 1) intervalo = 1;
    else if (n === 2) intervalo = 3;
    else intervalo = Math.round(t.intervalo * ef);
    intervalo = Math.min(intervalo, 365);
  }
  const ahora = Date.now();
  return {
    id: t.id,
    ef,
    n,
    intervalo,
    proximo: ahora + Math.max(0, intervalo) * 86_400_000,
    repasos: t.repasos + 1,
    ultima: ahora,
  };
}

export function vencidas(ts: Record<number, EstadoSm2>): EstadoSm2[] {
  const ahora = Date.now();
  return Object.values(ts)
    .filter((t) => t.proximo <= ahora)
    .sort((a, b) => a.proximo - b.proximo);
}

export function proximas(ts: Record<number, EstadoSm2>): EstadoSm2[] {
  const ahora = Date.now();
  return Object.values(ts)
    .filter((t) => t.proximo > ahora)
    .sort((a, b) => a.proximo - b.proximo);
}

export function enDias(ts: number): string {
  const d = Math.ceil((ts - Date.now()) / 86_400_000);
  if (d <= 0) return "hoy";
  if (d === 1) return "mañana";
  return `en ${d} días`;
}
