import { useMemo, useState } from "react";
import type { Cluster, Examen, Pregunta } from "../types";
import { EtiquetaTema, RefArticulos } from "../components/ui";

const MESES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
];

const MODALIDAD: Record<string, string> = {
  libre: "Acceso libre",
  pi: "Promoción interna",
  libre_pi: "Libre + PI (común)",
  aplazada: "Prueba aplazada",
  centros_sas: "Centros SAS",
  apes: "APES extinguidas",
  concurso: "Concurso-oposición",
};

function fechaLarga(iso: string): string {
  const [a, m, d] = iso.split("-").map(Number);
  return `${d} de ${MESES[m - 1]} de ${a}`;
}

export default function PastExamsMode({
  preguntas,
  examenes,
  clusters,
}: {
  preguntas: Pregunta[];
  examenes: Examen[];
  clusters: Cluster[];
}) {
  const [abrierto, setAbrierto] = useState<string | null>(null);
  const porId = useMemo(() => {
    const m = new Map<number, Cluster>();
    for (const c of clusters) m.set(c.cluster_id, c);
    return m;
  }, [clusters]);

  const anios = useMemo(() => [...new Set(examenes.map((e) => e.anio))].sort((a, b) => b - a), [examenes]);

  // clústeres que aparecieron por primera vez en cada año
  const primeraVez = useMemo(() => {
    const m = new Map<number, number>();
    for (const c of clusters) {
      const primero = Math.min(...c.anios);
      m.set(c.cluster_id, primero);
    }
    return m;
  }, [clusters]);

  return (
    <section className="space-y-4">
      <header className="card bg-gradient-to-br from-violet-600 to-fuchsia-700 text-white dark:from-violet-800 dark:to-fuchsia-900">
        <h2 className="text-base font-bold">Últimos exámenes</h2>
        <p className="mt-1 text-sm text-violet-50">
          Qué cayó en cada convocatoria del SAS y qué se repite respecto al año anterior. Solo el
          bloque común (Temas 1-10).
        </p>
      </header>

      {anios.map((anio) => {
        const exams = examenes.filter((e) => e.anio === anio);
        return (
          <div key={anio} className="space-y-2">
            <h3 className="text-sm font-bold uppercase tracking-wide text-stone-500">{anio}</h3>
            {exams.map((e) => {
              const preguntasExam = preguntas
                .filter((p) => p.exam_id === e.exam_id)
                .sort((a, b) => a.numero - b.numero);
              const nuevos = preguntasExam.filter(
                (p) => p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio
              );
              const repetidos = preguntasExam.filter(
                (p) => p.cluster_id !== null && (primeraVez.get(p.cluster_id) ?? 0) < anio
              );
              const abierto = abrierto === e.exam_id;
              return (
                <article key={e.exam_id} className="card">
                  <button
                    type="button"
                    onClick={() => setAbrierto(abierto ? null : e.exam_id)}
                    className="flex w-full items-center gap-3 text-left"
                  >
                    <span className="flex-1">
                      <span className="block text-sm font-semibold">
                        {fechaLarga(e.fecha)} · {MODALIDAD[e.modalidad] ?? e.modalidad}
                      </span>
                      <span className="block text-xs text-stone-500 dark:text-stone-400">
                        {e.n_preguntas_comun} preguntas de bloque común ·{" "}
                        <span className="text-emerald-700 dark:text-emerald-400">
                          {nuevos.length} nuevas
                        </span>{" "}
                        ·{" "}
                        <span className="text-amber-700 dark:text-amber-400">
                          {repetidos.length} repetidas
                        </span>
                      </span>
                    </span>
                    <span className="text-xl text-stone-300 dark:text-stone-600">
                      {abierto ? "⌄" : "›"}
                    </span>
                  </button>

                  {abierto && (
                    <ol className="mt-3 space-y-2 border-t border-stone-200 pt-3 dark:border-stone-800">
                      {preguntasExam.map((p) => {
                        const cl = p.cluster_id !== null ? porId.get(p.cluster_id) : undefined;
                        const esNuevo = p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio;
                        return (
                          <li key={p.id} className="rounded-xl bg-stone-50 p-3 dark:bg-stone-800/50">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="chip bg-stone-200 text-stone-600 dark:bg-stone-800 dark:text-stone-300">
                                #{p.numero}
                              </span>
                              {cl && <EtiquetaTema cluster={cl} />}
                              {cl && <RefArticulos articulos={cl.articulos} tema={cl.tema} />}
                              <span
                                className={
                                  "chip " +
                                  (esNuevo
                                    ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200"
                                    : "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200")
                                }
                              >
                                {esNuevo ? "Nueva este año" : "Ya había caído"}
                              </span>
                            </div>
                            <p className="mt-2 text-sm font-medium leading-snug">{p.enunciado}</p>
                            <ul className="mt-1 grid gap-0.5 text-xs text-stone-600 dark:text-stone-300">
                              {(["A", "B", "C", "D"] as const).map((l) => (
                                <li
                                  key={l}
                                  className={
                                    l === p.correcta ? "font-semibold text-emerald-700 dark:text-emerald-400" : ""
                                  }
                                >
                                  <span className="font-bold">{l})</span> {p.opciones[l]}
                                  {l === p.correcta && " ✓"}
                                </li>
                              ))}
                            </ul>
                            {cl && cl.ocurrencias.length > 1 && (
                              <p className="mt-1 text-[11px] text-stone-500">
                                También en:{" "}
                                {cl.ocurrencias
                                  .filter((o) => o.exam_id !== p.exam_id)
                                  .map((o) => `${o.anio} (${o.modalidad})`)
                                  .join(" · ")}
                              </p>
                            )}
                          </li>
                        );
                      })}
                    </ol>
                  )}
                </article>
              );
            })}
          </div>
        );
      })}
    </section>
  );
}
