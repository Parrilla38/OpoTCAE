import { useMemo, useState } from "react";
import { agrupaPorArticulo, cohesion, porTema } from "../data";
import { marcaVisitado } from "../store";
import type { Cluster, Concepto, ConceptosData, Meta } from "../types";
import { EtiquetaRepeticion, RefArticulos } from "../components/ui";

type Pestana = "temas" | "heatmap" | "conceptos";
type Nivel =
  | { tipo: "temas" }
  | { tipo: "articulos"; tema: number }
  | { tipo: "preguntas"; tema: number; articulo: number };

export default function ReviewMode({
  clusters,
  meta,
  conceptos,
}: {
  clusters: Cluster[];
  meta: Meta;
  conceptos: ConceptosData | null;
}) {
  const [pestana, setPestana] = useState<Pestana>("temas");
  const [nivel, setNivel] = useState<Nivel>({ tipo: "temas" });
  const [abierto, setAbierto] = useState<number | null>(null);

  const temas = useMemo(
    () => [...meta.temas].sort((a, b) => b.score_total - a.score_total),
    [meta.temas]
  );

  const articulos = useMemo(() => {
    if (nivel.tipo !== "articulos") return new Map<number, Cluster[]>();
    const cs = porTema(clusters, nivel.tema);
    const m = agrupaPorArticulo(cs);
    return new Map(
      [...m.entries()].sort((a, b) => {
        const sa = a[1].reduce((s, c) => s + c.score, 0);
        const sb = b[1].reduce((s, c) => s + c.score, 0);
        return sb - sa;
      })
    );
  }, [clusters, nivel]);

  const preguntas = useMemo(() => {
    if (nivel.tipo !== "preguntas") return [];
    const cs = porTema(clusters, nivel.tema);
    if (nivel.articulo === 0) return cs.filter((c) => !c.articulos.length);
    return cs.filter((c) => c.articulos.includes(nivel.articulo));
  }, [clusters, nivel]);

  return (
    <section className="space-y-4">
      <header className="card bg-gradient-to-br from-sky-600 to-indigo-700 text-white dark:from-sky-800 dark:to-indigo-900">
        <h2 className="text-base font-bold">Modo Repaso</h2>
        <p className="mt-1 text-sm text-sky-50">
          Qué temas, qué artículos y qué conceptos son los que más se preguntan. Ordenado por peso
          real en los exámenes oficiales, no por el orden del temario.
        </p>
      </header>

      <div className="flex gap-2 rounded-xl bg-stone-200/60 p-1 dark:bg-stone-800/60">
        {(
          [
            ["temas", "Temas"],
            ["heatmap", "Heatmap"],
            ["conceptos", "Conceptos"],
          ] as [Pestana, string][]
        ).map(([id, t]) => (
          <button
            key={id}
            type="button"
            onClick={() => {
              setPestana(id);
              if (id === "temas") setNivel({ tipo: "temas" });
            }}
            className={
              "flex-1 rounded-lg px-3 py-2 text-sm font-semibold transition " +
              (pestana === id
                ? "bg-white shadow dark:bg-stone-900"
                : "text-stone-600 dark:text-stone-300")
            }
          >
            {t}
          </button>
        ))}
      </div>

      {pestana === "heatmap" && <Heatmap clusters={clusters} meta={meta} onAbre={(t, a) => {
        setPestana("temas");
        setNivel({ tipo: "preguntas", tema: t, articulo: a });
      }} />}

      {pestana === "conceptos" && (
        <Conceptos conceptos={conceptos} meta={meta} abierto={abierto} setAbierto={setAbierto} />
      )}

      {pestana === "temas" && nivel.tipo === "temas" && (
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
      )}

      {pestana === "temas" && nivel.tipo === "articulos" && (
        <ol className="space-y-2">
          <div className="card">
            <button
              type="button"
              onClick={() => setNivel({ tipo: "temas" })}
              className="btn-fantasma -ml-2 mb-1 text-xs"
            >
              ← Todos los temas
            </button>
            <h3 className="text-base font-bold">
              T{String(nivel.tema).padStart(2, "0")} ·{" "}
              {meta.temas.find((x) => x.tema === nivel.tema)?.nombre}
            </h3>
            <p className="text-sm text-stone-500 dark:text-stone-400">
              Artículos / apartados por peso. Empieza por lo de arriba.
            </p>
          </div>
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
                      {cs.length} pregunta{cs.length === 1 ? "" : "s"} · score{" "}
                      {Math.round(score * 10) / 10} · {años.join(", ")}
                    </span>
                  </span>
                  <span className="text-xl text-stone-300 dark:text-stone-600">›</span>
                </button>
              </li>
            );
          })}
        </ol>
      )}

      {pestana === "temas" && nivel.tipo === "preguntas" && (
        <div className="space-y-3">
          <div className="card">
            <button
              type="button"
              onClick={() => setNivel({ tipo: "articulos", tema: nivel.tema })}
              className="btn-fantasma -ml-2 mb-1 text-xs"
            >
              ← Artículos
            </button>
            <h3 className="text-base font-bold">
              T{String(nivel.tema).padStart(2, "0")} ·{" "}
              {nivel.articulo === 0 ? "Sin artículo" : `Art. ${nivel.articulo}`}
            </h3>
            <p className="text-sm text-stone-500 dark:text-stone-400">
              {preguntas.length} pregunta{preguntas.length === 1 ? "" : "s"} con su año de aparición.
            </p>
          </div>
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
                    <li
                      key={l}
                      className={
                        l === c.correcta
                          ? "font-semibold text-emerald-700 dark:text-emerald-400"
                          : ""
                      }
                    >
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
      )}
    </section>
  );
}

// ─────────────────────────── heatmap ───────────────────────────

function Heatmap({
  clusters,
  meta,
  onAbre,
}: {
  clusters: Cluster[];
  meta: Meta;
  onAbre: (tema: number, articulo: number) => void;
}) {
  const anios = meta.anios;
  // (tema, articulo) -> recuento por año
  const celdas = useMemo(() => {
    const m = new Map<string, { tema: number; art: number; porAnio: Map<number, number>; total: number }>();
    for (const c of clusters) {
      const arts = c.articulos.length ? c.articulos : [0];
      for (const a of arts) {
        const k = `${c.tema}:${a}`;
        const d = m.get(k) ?? { tema: c.tema ?? 0, art: a, porAnio: new Map(), total: 0 };
        for (const anio of c.anios) {
          d.porAnio.set(anio, (d.porAnio.get(anio) ?? 0) + 1);
          d.total += 1;
        }
        m.set(k, d);
      }
    }
    return [...m.values()].sort((a, b) => b.total - a.total);
  }, [clusters]);

  const max = Math.max(1, ...celdas.map((c) => c.total));

  return (
    <div className="card overflow-x-auto">
      <h3 className="text-sm font-bold">Heatmap artículo × año</h3>
      <p className="mb-3 text-xs text-stone-500 dark:text-stone-400">
        Cuántas veces cae cada artículo en cada convocatoria. Más oscuro = más veces. Toca una fila
        para ver las preguntas.
      </p>
      <table className="w-full border-collapse text-xs">
        <thead>
          <tr>
            <th className="sticky left-0 bg-white px-2 py-1 text-left dark:bg-stone-900">Art.</th>
            {anios.map((a) => (
              <th key={a} className="px-2 py-1 text-center font-semibold">
                {a}
              </th>
            ))}
            <th className="px-2 py-1 text-center font-semibold">Σ</th>
          </tr>
        </thead>
        <tbody>
          {celdas.slice(0, 30).map((c) => (
            <tr key={`${c.tema}:${c.art}`}>
              <td className="sticky left-0 bg-white px-2 py-1 dark:bg-stone-900">
                <button
                  type="button"
                  onClick={() => onAbre(c.tema, c.art)}
                  className="text-left underline decoration-dotted underline-offset-2 hover:text-marca-700"
                >
                  T{String(c.tema).padStart(2, "0")} ·{" "}
                  {c.art === 0 ? "sin art." : `art. ${c.art}`}
                </button>
              </td>
              {anios.map((a) => {
                const n = c.porAnio.get(a) ?? 0;
                const op = n === 0 ? 0 : 0.18 + (n / max) * 0.82;
                return (
                  <td key={a} className="px-1 py-1 text-center">
                    <span
                      className="inline-flex h-6 w-8 items-center justify-center rounded font-bold tabular-nums"
                      style={{
                        background: n ? `rgba(5, 150, 105, ${op})` : "transparent",
                        color: n && op > 0.55 ? "#fff" : undefined,
                      }}
                      title={`${a}: ${n} vez/veces`}
                    >
                      {n || "·"}
                    </span>
                  </td>
                );
              })}
              <td className="px-2 py-1 text-center font-bold tabular-nums">{c.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ─────────────────────────── conceptos ───────────────────────────

function Conceptos({
  conceptos,
  meta,
  abierto,
  setAbierto,
}: {
  conceptos: ConceptosData | null;
  meta: Meta;
  abierto: number | null;
  setAbierto: (n: number | null) => void;
}) {
  if (!conceptos) {
    return (
      <div className="card text-sm text-stone-500">
        El análisis semántico no está disponible en este build.
      </div>
    );
  }
  return (
    <div className="space-y-3">
      <div className="card">
        <h3 className="text-sm font-bold">Conceptos que caen en varios años</h3>
        <p className="mt-1 text-xs text-stone-500 dark:text-stone-400">
          {conceptos.n_multi_anio} conceptos con ≥2 años distintos, de {conceptos.n_conceptos_total}{" "}
          detectados sobre {meta.totales.preguntas} preguntas. Agrupados con{" "}
          <code className="rounded bg-stone-100 px-1 dark:bg-stone-800">{conceptos.modelo}</code> —
          esto sí captura «lo mismo dicho de otra manera».
        </p>
        <p className="mt-2 text-[11px] text-stone-500">
          Cohesión: <b>alta</b> = casi la misma pregunta · <b>media</b> = el mismo concepto con
          distinto enfoque · <b>baja</b> = mismo tema, preguntas distintas.
        </p>
      </div>
      {conceptos.conceptos.map((c) => (
        <TarjetaConcepto
          key={c.concepto_id}
          c={c}
          abierto={abierto === c.concepto_id}
          toggle={() => setAbierto(abierto === c.concepto_id ? null : c.concepto_id)}
        />
      ))}
    </div>
  );
}

function TarjetaConcepto({
  c,
  abierto,
  toggle,
}: {
  c: Concepto;
  abierto: boolean;
  toggle: () => void;
}) {
  const coh = cohesion(c.similitud_media);
  const colorCoh =
    coh === "alta"
      ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200"
      : coh === "media"
        ? "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200"
        : "bg-stone-200 text-stone-700 dark:bg-stone-800 dark:text-stone-200";
  return (
    <article className="card">
      <button type="button" onClick={toggle} className="w-full text-left">
        <div className="flex flex-wrap items-center gap-2">
          <span className="chip bg-stone-200 text-stone-600 dark:bg-stone-800 dark:text-stone-300">
            #{c.rank}
          </span>
          <span className="chip bg-violet-100 text-violet-800 dark:bg-violet-950 dark:text-violet-200">
            {c.n_preguntas} formulaciones
          </span>
          <span className="chip bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-200">
            {c.anios.join(", ")}
          </span>
          <span className={"chip " + colorCoh}>cohesión {coh}</span>
          {c.temas.map((t) => (
            <span key={t} className="chip bg-stone-200 text-stone-600 dark:bg-stone-800 dark:text-stone-300">
              T{String(t).padStart(2, "0")}
            </span>
          ))}
        </div>
        <h3 className="mt-2 text-sm font-semibold leading-snug">{c.representante}</h3>
        <p className="mt-1 text-[11px] text-stone-500">
          similitud media {c.similitud_media} · score {c.score}
        </p>
      </button>
      {abierto && (
        <ul className="mt-3 space-y-2 border-t border-stone-200 pt-3 dark:border-stone-800">
          {c.miembros.map((m) => (
            <li key={m.id} className="rounded-xl bg-stone-50 p-2.5 text-xs dark:bg-stone-800/50">
              <div className="flex flex-wrap items-center gap-1.5">
                <span className="chip bg-stone-200 text-stone-600 dark:bg-stone-800 dark:text-stone-300">
                  {m.anio} · {m.modalidad} · #{m.numero}
                </span>
                {m.tema !== null && (
                  <span className="chip bg-stone-200 text-stone-600 dark:bg-stone-800 dark:text-stone-300">
                    T{String(m.tema).padStart(2, "0")}
                  </span>
                )}
              </div>
              <p className="mt-1 leading-snug">{m.enunciado}</p>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}
