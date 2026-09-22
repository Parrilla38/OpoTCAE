import { useMemo, useState } from "react";
import type { Cluster, Examen, Letra, Pregunta } from "../types";
import { Etiqueta, NombreTema } from "../components/ui";

const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

const MODALIDAD: Record<string, string> = {
  libre: "Acceso libre",
  pi: "Promoción interna",
  libre_pi: "Libre y promoción interna",
  aplazada: "Prueba aplazada",
  centros_sas: "Centros SAS",
  apes: "APES extinguidas",
  concurso: "Concurso-oposición",
};

function fecha(iso: string): string {
  const [a, m, d] = iso.split("-").map(Number);
  return `${d} ${MESES[m - 1]} ${a}`;
}

export default function Examenes({
  preguntas,
  examenes,
  clusters,
}: {
  preguntas: Pregunta[];
  examenes: Examen[];
  clusters: Cluster[];
}) {
  const [abierto, setAbierto] = useState<string | null>(null);
  const porId = useMemo(() => new Map(clusters.map((c) => [c.cluster_id, c])), [clusters]);
  const anios = useMemo(() => [...new Set(examenes.map((e) => e.anio))].sort((a, b) => b - a), [examenes]);

  const primeraVez = useMemo(() => {
    const m = new Map<number, number>();
    for (const c of clusters) m.set(c.cluster_id, Math.min(...c.anios));
    return m;
  }, [clusters]);

  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Exámenes anteriores</h2>
        <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">
          Qué preguntó el tribunal cada año y qué se repite respecto a los anteriores.
        </p>
      </div>

      {anios.map((anio) => (
        <div key={anio} className="space-y-2">
          <h3 className="text-sm font-bold uppercase tracking-wide text-stone-500">{anio}</h3>
          {examenes
            .filter((e) => e.anio === anio)
            .map((e) => {
              const ps = preguntas.filter((p) => p.exam_id === e.exam_id).sort((a, b) => a.numero - b.numero);
              const nuevas = ps.filter((p) => p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio);
              const repetidas = ps.filter((p) => p.cluster_id !== null && (primeraVez.get(p.cluster_id) ?? 0) < anio);
              const estaAbierto = abierto === e.exam_id;
              return (
                <article key={e.exam_id} className="rounded-2xl border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-900">
                  <button
                    type="button"
                    onClick={() => setAbierto(estaAbierto ? null : e.exam_id)}
                    className="flex w-full items-center gap-3 p-4 text-left"
                  >
                    <span className="flex-1">
                      <span className="block text-[15px] font-semibold">
                        {fecha(e.fecha)} · {MODALIDAD[e.modalidad] ?? e.modalidad}
                      </span>
                      <span className="mt-0.5 block text-xs text-stone-500 dark:text-stone-400">
                        {e.n_preguntas_comun} preguntas · {nuevas.length} nuevas · {repetidas.length}{" "}
                        ya habían caído
                      </span>
                    </span>
                    <span className="text-xl text-stone-300 dark:text-stone-600">{estaAbierto ? "⌄" : "›"}</span>
                  </button>
                  {estaAbierto && (
                    <ol className="space-y-3 border-t border-stone-200 p-4 dark:border-stone-800">
                      {ps.map((p) => {
                        const cl = p.cluster_id !== null ? porId.get(p.cluster_id) : undefined;
                        const esNueva = p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio;
                        return (
                          <li key={p.id} className="rounded-xl bg-stone-50 p-4 dark:bg-stone-800/50">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="text-xs font-bold text-stone-400">#{p.numero}</span>
                              {cl && <NombreTema cluster={cl} />}
                              <Etiqueta tono={esNueva ? "verde" : "ambar"}>
                                {esNueva ? "Nueva este año" : "Ya había caído"}
                              </Etiqueta>
                            </div>
                            <p className="mt-2 text-sm font-medium leading-snug">{p.enunciado}</p>
                            <ul className="mt-2 grid gap-1 text-xs text-stone-600 dark:text-stone-300">
                              {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                                <li
                                  key={l}
                                  className={l === p.correcta ? "font-semibold text-emerald-700 dark:text-emerald-400" : ""}
                                >
                                  <span className="font-bold">{l})</span> {p.opciones[l]}
                                  {l === p.correcta && " ✓"}
                                </li>
                              ))}
                            </ul>
                          </li>
                        );
                      })}
                    </ol>
                  )}
                </article>
              );
            })}
        </div>
      ))}

      <div className="rounded-2xl border border-stone-200 bg-white p-5 text-xs leading-relaxed text-stone-500 dark:border-stone-800 dark:bg-stone-900">
        Fuente: cuadernillos y plantillas oficiales del Servicio Andaluz de Salud (Junta de
        Andalucía). Solo se muestran las preguntas de los temas del temario oficial; el examen real
        incluía además anatomía y clínica.
      </div>
    </section>
  );
}
