import { useMemo, useState } from "react";
import { cargaProgreso, reiniciaProgreso } from "../store";
import type { Cluster } from "../types";
import { EtiquetaTema, RefArticulos } from "../components/ui";

export default function NotebookMode({
  clusters,
  onIrATest,
}: {
  clusters: Cluster[];
  onIrATest: () => void;
}) {
  const [, forzar] = useState(0);
  const progreso = useMemo(() => cargaProgreso(), []);
  const fallados = useMemo(
    () =>
      Object.entries(progreso.errores)
        .filter(([, n]) => (n as number) > 0)
        .map(([k, n]) => ({ id: Number(k), veces: n as number }))
        .sort((a, b) => b.veces - a.veces),
    [progreso]
  );
  const porId = useMemo(() => {
    const m = new Map<number, Cluster>();
    for (const c of clusters) m.set(c.cluster_id, c);
    return m;
  }, [clusters]);

  if (!fallados.length) {
    return (
      <section className="space-y-4">
        <header className="card">
          <h2 className="text-base font-bold">Libreta de errores</h2>
          <p className="text-sm text-stone-500 dark:text-stone-400">
            Aquí se acumulan las preguntas que fallas en los tests. Todavía está vacía.
          </p>
        </header>
        <button type="button" onClick={onIrATest} className="btn-primario w-full">
          Hacer un test
        </button>
      </section>
    );
  }

  return (
    <section className="space-y-4">
      <header className="card">
        <h2 className="text-base font-bold">Libreta de errores</h2>
        <p className="text-sm text-stone-500 dark:text-stone-400">
          {fallados.length} pregunta{fallados.length === 1 ? "" : "s"} con fallos. Ordenadas por las
          que más fallas. Prueba el filtro «Mis errores» del Modo Test para repasarlas.
        </p>
      </header>

      <button
        type="button"
        onClick={() => {
          if (confirm("¿Borrar todo el progreso (intentos, errores y stats)?")) {
            reiniciaProgreso();
            forzar((n) => n + 1);
          }
        }}
        className="btn-secundario w-full text-rose-600"
      >
        Vaciar libreta y progreso
      </button>

      <ol className="space-y-2">
        {fallados.map(({ id, veces }, i) => {
          const c = porId.get(id);
          if (!c) return null;
          return (
            <li key={id} className="card space-y-2">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold text-stone-400">{i + 1}</span>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="chip bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-200">
                    {veces} fallo{veces === 1 ? "" : "s"}
                  </span>
                  <EtiquetaTema cluster={c} />
                  <RefArticulos articulos={c.articulos} tema={c.tema} />
                </div>
              </div>
              <p className="text-sm font-semibold leading-snug">{c.enunciado}</p>
              <ul className="grid gap-0.5 text-xs text-stone-600 dark:text-stone-300">
                {(["A", "B", "C", "D"] as const).map((l) => (
                  <li
                    key={l}
                    className={l === c.correcta ? "font-semibold text-emerald-700 dark:text-emerald-400" : ""}
                  >
                    <span className="font-bold">{l})</span> {c.opciones[l]}
                    {l === c.correcta && " ✓"}
                  </li>
                ))}
              </ul>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
