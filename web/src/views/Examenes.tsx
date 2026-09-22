import { useMemo, useState } from "react";
import type { Cluster, Examen, Letra, Pregunta } from "../types";
import { Chip, NombreTema } from "../components/ui";

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
    <section className="space-y-5">
      <div>
        <span className="etiqueta">Convocatorias oficiales</span>
        <h2 className="mt-3 text-[33px] font-medium leading-[1.06] tracking-[-0.035em]">
          Exámenes anteriores
        </h2>
        <p className="mt-2 max-w-[38ch] text-sm leading-relaxed text-suave">
          Qué preguntó el tribunal cada año y qué se repite respecto a los anteriores.
        </p>
      </div>

      {anios.map((anio) => (
        <div key={anio} className="space-y-2">
          <span className="etiqueta">{anio}</span>
          {examenes
            .filter((e) => e.anio === anio)
            .map((e) => {
              const ps = preguntas.filter((p) => p.exam_id === e.exam_id).sort((a, b) => a.numero - b.numero);
              const nuevas = ps.filter((p) => p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio);
              const repetidas = ps.filter((p) => p.cluster_id !== null && (primeraVez.get(p.cluster_id) ?? 0) < anio);
              const estaAbierto = abierto === e.exam_id;
              return (
                <article key={e.exam_id} className="tarjeta overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setAbierto(estaAbierto ? null : e.exam_id)}
                    className="flex w-full items-center gap-3 px-4 py-3.5 text-left"
                  >
                    <span className="flex-1">
                      <span className="block text-[15px] font-semibold tracking-tight">
                        {fecha(e.fecha)} · {MODALIDAD[e.modalidad] ?? e.modalidad}
                      </span>
                      <span className="mt-0.5 block font-mono text-[10.5px] uppercase tracking-wider text-suave">
                        {e.n_preguntas_comun} preguntas · {nuevas.length} nuevas · {repetidas.length}{" "}
                        repetidas
                      </span>
                    </span>
                    <span className="font-mono text-suave">{estaAbierto ? "−" : "+"}</span>
                  </button>
                  {estaAbierto && (
                    <ol className="space-y-3 border-t border-hilo p-4">
                      {ps.map((p) => {
                        const cl = p.cluster_id !== null ? porId.get(p.cluster_id) : undefined;
                        const esNueva = p.cluster_id !== null && primeraVez.get(p.cluster_id) === anio;
                        return (
                          <li key={p.id} className="rounded-opcion bg-fondo px-4 py-3.5">
                            <div className="flex flex-wrap items-center gap-1.5">
                              <span className="font-mono text-[11px] text-suave">
                                {String(p.numero).padStart(2, "0")}
                              </span>
                              {cl && <NombreTema cluster={cl} />}
                              <Chip tono={esNueva ? "verde" : "neutro"}>
                                {esNueva ? "nueva este año" : "ya había caído"}
                              </Chip>
                            </div>
                            <p className="mt-2.5 text-[14.5px] font-medium leading-snug tracking-tight">
                              {p.enunciado}
                            </p>
                            <ul className="mt-2.5 grid gap-1 text-[13px] leading-snug text-suave">
                              {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                                <li
                                  key={l}
                                  className={
                                    l === p.correcta
                                      ? "flex gap-2 font-medium text-verde"
                                      : "flex gap-2"
                                  }
                                >
                                  <span className="font-mono text-[11px] font-semibold">{l}</span>
                                  <span className="flex-1">
                                    {p.opciones[l]}
                                    {l === p.correcta && " ✓"}
                                  </span>
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

      <div className="rounded-accion border border-hilo bg-fondo px-4 py-4 font-mono text-[10px] uppercase leading-relaxed tracking-wider text-suave">
        Fuente: cuadernillos y plantillas oficiales del Servicio Andaluz de Salud (Junta de
        Andalucía). Solo se muestran las preguntas de los temas del temario oficial.
      </div>
    </section>
  );
}
