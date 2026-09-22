import { useMemo } from "react";
import { cargaProgreso, resumenProgreso } from "../store";
import type { Cluster, Meta } from "../types";

export default function StatsMode({ clusters, meta }: { clusters: Cluster[]; meta: Meta }) {
  const resumen = useMemo(() => resumenProgreso(), []);
  const progreso = useMemo(() => cargaProgreso(), []);
  const porId = useMemo(() => {
    const m = new Map<number, Cluster>();
    for (const c of clusters) m.set(c.cluster_id, c);
    return m;
  }, [clusters]);

  // aciertos/fallos por tema
  const porTema = useMemo(() => {
    const m = new Map<number, { aciertos: number; fallos: number }>();
    for (const [k, n] of Object.entries(progreso.aciertos)) {
      const c = porId.get(Number(k));
      if (!c?.tema) continue;
      const d = m.get(c.tema) ?? { aciertos: 0, fallos: 0 };
      d.aciertos += n as number;
      m.set(c.tema, d);
    }
    for (const [k, n] of Object.entries(progreso.errores)) {
      const c = porId.get(Number(k));
      if (!c?.tema) continue;
      const d = m.get(c.tema) ?? { aciertos: 0, fallos: 0 };
      d.fallos += n as number;
      m.set(c.tema, d);
    }
    return [...m.entries()].sort((a, b) => {
      const pa = a[1].aciertos + a[1].fallos;
      const pb = b[1].aciertos + b[1].fallos;
      return pb - pa;
    });
  }, [progreso, porId]);

  return (
    <section className="space-y-4">
      <header className="card bg-gradient-to-br from-stone-700 to-stone-900 text-white dark:from-stone-800 dark:to-black">
        <h2 className="text-base font-bold">Tus estadísticas</h2>
        <p className="mt-1 text-sm text-stone-300">
          Se guardan solo en este navegador. Sin cuenta, sin servidor, sin cookies de seguimiento.
        </p>
      </header>

      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        {[
          { t: "Intentos", v: resumen.intentos },
          { t: "Aciertos", v: resumen.aciertos },
          { t: "Fallos", v: resumen.fallos },
          { t: "Nota media", v: resumen.notaMedia },
        ].map((s) => (
          <div key={s.t} className="card text-center">
            <div className="text-2xl font-bold tabular-nums">{s.v}</div>
            <div className="text-xs uppercase tracking-wide text-stone-500">{s.t}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 className="text-sm font-bold">Dominio por tema</h3>
        <p className="mb-3 text-xs text-stone-500 dark:text-stone-400">
          Proporción de aciertos sobre lo que has respondido en los tests.
        </p>
        <ul className="space-y-3">
          {meta.temas.map((t) => {
            const d = porTema.find(([k]) => k === t.tema)?.[1] ?? { aciertos: 0, fallos: 0 };
            const total = d.aciertos + d.fallos;
            const pct = total ? Math.round((d.aciertos / total) * 100) : null;
            return (
              <li key={t.tema}>
                <div className="mb-1 flex items-baseline justify-between gap-2">
                  <span className="text-sm">
                    T{String(t.tema).padStart(2, "0")} · {t.corto}
                  </span>
                  <span className="text-xs tabular-nums text-stone-500">
                    {total === 0 ? "sin datos" : `${pct}% · ${total} resp.`}
                  </span>
                </div>
                <div className="progreso">
                  <div
                    className="progreso-relleno"
                    style={{
                      width: `${pct ?? 0}%`,
                      background:
                        pct === null ? "transparent" : pct >= 70 ? "#059669" : pct >= 40 ? "#d97706" : "#e11d48",
                    }}
                  />
                </div>
              </li>
            );
          })}
        </ul>
      </div>

      <div className="card">
        <h3 className="text-sm font-bold">Contexto del análisis</h3>
        <ul className="mt-2 space-y-1 text-xs text-stone-500 dark:text-stone-400">
          <li>· {meta.totales.preguntas} preguntas de bloque común (Temas 1-10)</li>
          <li>· {meta.totales.clusters} clústeres distintos</li>
          <li>· {meta.totales.repetidos} se repiten en el corpus</li>
          <li>· {meta.totales.multi_anio} caen en 2+ años distintos</li>
          <li>· {meta.totales.examenes} convocatorias ({meta.anios.join(", ")})</li>
          <li>· Score = {meta.score_formula}</li>
        </ul>
        <p className="mt-2 text-[11px] text-stone-500">
          Dato clave: la repetición <em>literal</em> entre años es casi nula. Lo que se repite es el
          artículo y el concepto, no la redacción. Por eso el Modo Repaso por artículos es la
          herramienta principal.
        </p>
      </div>

      {progreso.intentos.length > 0 && (
        <div className="card">
          <h3 className="text-sm font-bold">Últimos intentos</h3>
          <ul className="mt-2 space-y-1 text-xs text-stone-500 dark:text-stone-400">
            {progreso.intentos.slice(0, 8).map((i) => (
              <li key={i.id} className="flex items-center justify-between gap-2">
                <span>
                  {new Date(i.fecha).toLocaleDateString("es-ES", {
                    day: "2-digit",
                    month: "short",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </span>
                <span className="tabular-nums">
                  {i.nota}/10 · {i.aciertos}✓ {i.fallos}✗ {i.en_blanco}—
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
