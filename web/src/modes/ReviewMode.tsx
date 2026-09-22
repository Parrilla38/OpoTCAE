import { useMemo, useState } from "react";
import { agrupaPorArticulo, porTema } from "../data";
import { marcaVisitado } from "../store";
import type { Cluster, Meta } from "../types";
import { EtiquetaRepeticion, RefArticulos } from "../components/ui";

type Nivel = { tipo: "temas" } | { tipo: "articulos"; tema: number } | { tipo: "preguntas"; tema: number; articulo: number };

export default function ReviewMode({ clusters, meta }: { clusters: Cluster[]; meta: Meta }) {
  const [nivel, setNivel] = useState<Nivel>({ tipo: "temas" });

  const temas = useMemo(
    () => [...meta.temas].sort((a, b) => b.score_total - a.score_total),
    [meta.temas]
  );

  const articulos = useMemo(() => {
    if (nivel.tipo !== "articulos") return new Map<number, Cluster[]>();
    const cs = porTema(clusters, nivel.tema);
    const m = agrupaPorArticulo(cs);
    return new Map([...m.entries()].sort((a, b) => {
      const sa = a[1].reduce((s, c) => s + c.score, 0);
      const sb = b[1].reduce((s, c) => s + c.score, 0);
      return sb - sa;
    }));
  }, [clusters, nivel]);

  const preguntas = useMemo(() => {
    if (nivel.tipo !== "preguntas") return [];
    const cs = porTema(clusters, nivel.tema);
    if (nivel.articulo === 0) return cs.filter((c) => !c.articulos.length);
    return cs.filter((c) => c.articulos.includes(nivel.articulo));
  }, [clusters, nivel]);

  if (nivel.tipo === "temas") {
    return (
      <section className="space-y-4">
        <header className="card bg-gradient-to-br from-sky-600 to-indigo-700 text-white dark:from-sky-800 dark:to-indigo-900">
          <h2 className="text-base font-bold">Modo Repaso</h2>
          <p className="mt-1 text-sm text-sky-50">
            Qué temas y qué artículos son los que más se preguntan. Ordenado por peso real en los
            exámenes oficiales, no por el orden del temario.
          </p>
        </header>
        <ol className="space-y-2">
          {temas.map((t, i) => (
            <li key={t.tema}>
              <button
                type="button"
                onClick={() => setNivel({ tipo: "articulos", tema: t.tema })}
                className="card flex w-full items-center gap-3 text-left transition hover:border-marca-400 hover:bg-marca-50/50 dark:hover:bg-stone-800"
              >
                <span className="w-6 shrink-0 text-center text-lg font-bold text-stone-300 dark:text-stone-600">
                  {i + 1}
                </span>
                <span className="flex-1">
                  <span className="block text-sm font-semibold">
                    T{String(t.tema).padStart(2, "0")} · {t.nombre}
                  </span>
                  <span className="block text-xs text-stone-500 dark:text-stone-400">
                    {t.preguntas} preguntas · {t.clusters} clústeres · score {t.score_total}
                  </span>
                </span>
                <span className="text-xl text-stone-300 dark:text-stone-600">›</span>
              </button>
            </li>
          ))}
        </ol>
      </section>
    );
  }

  if (nivel.tipo === "articulos") {
    const t = meta.temas.find((x) => x.tema === nivel.tema);
    return (
      <section className="space-y-4">
        <header className="card">
          <button type="button" onClick={() => setNivel({ tipo: "temas" })} className="btn-fantasma -ml-2 mb-1 text-xs">
            ← Todos los temas
          </button>
          <h2 className="text-base font-bold">
            T{String(nivel.tema).padStart(2, "0")} · {t?.nombre}
          </h2>
          <p className="text-sm text-stone-500 dark:text-stone-400">
            Artículos / apartados por peso. Empieza por lo de arriba.
          </p>
        </header>
        <ol className="space-y-2">
          {[...articulos.entries()].map(([art, cs], i) => {
            const score = cs.reduce((s, c) => s + c.score, 0);
            const años = [...new Set(cs.flatMap((c) => c.anios))].sort();
            return (
              <li key={art}>
                <button
                  type="button"
                  onClick={() => setNivel({ tipo: "preguntas", tema: nivel.tema, articulo: art })}
                  className="card flex w-full items-center gap-3 text-left transition hover:border-marca-400 hover:bg-marca-50/50 dark:hover:bg-stone-800"
                >
                  <span className="w-6 shrink-0 text-center text-lg font-bold text-stone-300 dark:text-stone-600">
                    {i + 1}
                  </span>
                  <span className="flex-1">
                    <span className="block text-sm font-semibold">
                      {art === 0 ? "Sin artículo citado" : `Art. ${art}`}
                    </span>
                    <span className="block text-xs text-stone-500 dark:text-stone-400">
                      {cs.length} pregunta{cs.length === 1 ? "" : "s"} · score {Math.round(score * 10) / 10} ·{" "}
                      {años.join(", ")}
                    </span>
                  </span>
                  <span className="text-xl text-stone-300 dark:text-stone-600">›</span>
                </button>
              </li>
            );
          })}
        </ol>
      </section>
    );
  }

  return (
    <section className="space-y-4">
      <header className="card">
        <button
          type="button"
          onClick={() => setNivel({ tipo: "articulos", tema: nivel.tema })}
          className="btn-fantasma -ml-2 mb-1 text-xs"
        >
          ← Artículos
        </button>
        <h2 className="text-base font-bold">
          T{String(nivel.tema).padStart(2, "0")} · {nivel.articulo === 0 ? "Sin artículo" : `Art. ${nivel.articulo}`}
        </h2>
        <p className="text-sm text-stone-500 dark:text-stone-400">
          {preguntas.length} pregunta{preguntas.length === 1 ? "" : "s"} con su año de aparición.
        </p>
      </header>
      <div className="space-y-3">
        {preguntas.map((c) => {
          marcaVisitado(c.cluster_id);
          return (
            <article key={c.cluster_id} className="card space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <EtiquetaRepeticion cluster={c} />
                <RefArticulos articulos={c.articulos} tema={c.tema} />
              </div>
              <h3 className="text-sm font-semibold leading-snug">{c.enunciado}</h3>
              <ul className="grid gap-1 text-sm">
                {(["A", "B", "C", "D"] as const).map((l) => (
                  <li key={l} className={l === c.correcta ? "font-semibold text-emerald-700 dark:text-emerald-400" : ""}>
                    <span className="font-bold">{l})</span> {c.opciones[l]}
                    {l === c.correcta && "  ✓"}
                  </li>
                ))}
              </ul>
              <p className="text-xs text-stone-500">
                Aparece en {c.ocurrencias.map((o) => `${o.anio} (${o.modalidad})`).join(" · ")}
              </p>
            </article>
          );
        })}
      </div>
    </section>
  );
}
