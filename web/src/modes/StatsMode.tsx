import { useMemo } from "react";
import { cargaProgreso, resumenProgreso } from "../store";
import type { Cluster, Meta } from "../types";

function exportaMd(clusters: Cluster[], meta: Meta) {
  const p = cargaProgreso();
  const fallados = Object.entries(p.errores)
    .filter(([, n]) => (n as number) > 0)
    .map(([k, n]) => ({ id: Number(k), veces: n as number }))
    .sort((a, b) => b.veces - a.veces);
  const porId = new Map(clusters.map((c) => [c.cluster_id, c]));

  const L: string[] = ["# Repaso TCAE Andalucía — mi libreta y el radar", ""];
  L.push(`_Exportado el ${new Date().toLocaleString("es-ES")}_`, "");
  L.push("## Mi libreta de errores", "");
  if (!fallados.length) L.push("_Todavía no hay errores registrados._", "");
  for (const { id, veces } of fallados) {
    const c = porId.get(id);
    if (!c) continue;
    L.push(`### [${veces} fallo${veces === 1 ? "" : "s"}] ${c.enunciado}`);
    L.push("");
    for (const l of ["A", "B", "C", "D"] as const) {
      L.push(`- ${l}${l === c.correcta ? " ✓" : ""}) ${c.opciones[l]}`);
    }
    L.push(
      "",
      `T${String(c.tema ?? 0).padStart(2, "0")} · ${c.tema_corto} · ${
        c.articulos.length ? `art. ${c.articulos.join(", ")}` : "sin art."
      } · cae en ${c.anios.join(", ")}`,
      ""
    );
  }

  L.push("## Radar — lo que más se repite", "");
  L.push("| # | score | años | Tema | Art. | Enunciado |");
  L.push("|---|-------|------|------|------|-----------|");
  for (const c of [...clusters].sort((a, b) => b.score - a.score).slice(0, 40)) {
    L.push(
      `| ${c.cluster_id} | ${c.score} | ${c.anios.join(",")} | T${String(c.tema ?? 0).padStart(2, "0")} | ${
        c.articulos.join(",") || "—"
      } | ${c.enunciado.replace(/\|/g, "/").slice(0, 90)} |`
    );
  }
  L.push("", "## Peso por tema", "");
  for (const t of meta.temas) {
    L.push(`- T${String(t.tema).padStart(2, "0")} · ${t.nombre}: ${t.preguntas} preguntas`);
  }
  L.push("", "---", "", `_Fuente: ${meta.fuente}. ${meta.aviso}_`, "");

  const blob = new Blob([L.join("\n")], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `tcae-repaso-${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
}

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
          {meta.totales.conceptos_multi_anio !== undefined && (
            <li>
              ·{" "}
              <b className="text-stone-700 dark:text-stone-200">
                {meta.totales.conceptos_multi_anio} conceptos multi-año
              </b>{" "}
              (de {meta.totales.conceptos} detectados por embeddings)
            </li>
          )}
          <li>· {meta.totales.examenes} convocatorias ({meta.anios.join(", ")})</li>
          <li>· Score = {meta.score_formula}</li>
        </ul>
        <p className="mt-2 text-[11px] text-stone-500">
          Dato clave: la repetición <em>literal</em> entre años es casi nula. Lo que se repite es el
          artículo y el concepto, no la redacción. Por eso el Modo Repaso por artículos y la vista
          de Conceptos son las herramientas principales.
        </p>
      </div>

      <div className="card">
        <h3 className="text-sm font-bold">Repaso en papel</h3>
        <p className="mb-3 text-xs text-stone-500 dark:text-stone-400">
          Exporta tu libreta de errores y el radar de artículos para repasar sin pantalla.
        </p>
        <div className="grid gap-2 sm:grid-cols-2">
          <button type="button" onClick={() => exportaMd(clusters, meta)} className="btn-secundario">
            ⬇ Exportar resumen (.md)
          </button>
          <button type="button" onClick={() => window.print()} className="btn-secundario">
            🖨 Imprimir
          </button>
        </div>
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
