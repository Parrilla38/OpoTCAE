import { useEffect, useState } from "react";
import { cargaTodo } from "./data";
import type { Cluster, ConceptosData, Examen, Meta, Pregunta } from "./types";
import Practicar from "./views/Practicar";
import Aprender from "./views/Aprender";
import Examenes from "./views/Examenes";
import Progreso from "./views/Progreso";

type Vista = "practicar" | "aprender" | "examenes" | "progreso";

const NAV: { id: Vista; texto: string; icono: string }[] = [
  { id: "practicar", texto: "Practicar", icono: "🎯" },
  { id: "aprender", texto: "Aprender", icono: "📖" },
  { id: "examenes", texto: "Exámenes", icono: "🗓" },
  { id: "progreso", texto: "Mi progreso", icono: "👤" },
];

function BotonTema() {
  const [oscuro, setOscuro] = useState(() => document.documentElement.classList.contains("dark"));
  useEffect(() => {
    document.documentElement.classList.toggle("dark", oscuro);
    localStorage.setItem("opotcae-tema", oscuro ? "oscuro" : "claro");
  }, [oscuro]);
  return (
    <button
      type="button"
      onClick={() => setOscuro((v) => !v)}
      aria-label={oscuro ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
      className="flex h-11 w-11 items-center justify-center rounded-full text-xl transition hover:bg-stone-200/60 dark:hover:bg-stone-800/60"
    >
      {oscuro ? "☀️" : "🌙"}
    </button>
  );
}

export default function App() {
  const [vista, setVista] = useState<Vista>("practicar");
  const [datos, setDatos] = useState<{
    clusters: Cluster[];
    preguntas: Pregunta[];
    examenes: Examen[];
    meta: Meta;
    conceptos: ConceptosData | null;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    cargaTodo()
      .then(setDatos)
      .catch((e) => setError(String(e)));
  }, []);

  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col px-4 pb-28 pt-5">
      <header className="mb-6 flex items-center justify-between gap-3">
        <div>
          <h1 className="text-lg font-bold leading-tight tracking-tight">OpoTCAE</h1>
          <p className="text-xs text-stone-500 dark:text-stone-400">
            Lo que más se pregunta en el TCAE de Andalucía
          </p>
        </div>
        <BotonTema />
      </header>

      {error && (
        <div className="rounded-2xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
          <p className="font-semibold">No se han podido cargar las preguntas</p>
          <p className="text-xs">{error}</p>
        </div>
      )}

      {!datos && !error && (
        <div className="rounded-2xl border border-stone-200 bg-white p-5 text-sm text-stone-500 dark:border-stone-800 dark:bg-stone-900">
          Cargando preguntas…
        </div>
      )}

      {datos && (
        <main className="flex-1">
          {vista === "practicar" && (
            <Practicar clusters={datos.clusters} meta={datos.meta} onIrAProgreso={() => setVista("progreso")} />
          )}
          {vista === "aprender" && (
            <Aprender clusters={datos.clusters} meta={datos.meta} conceptos={datos.conceptos} />
          )}
          {vista === "examenes" && (
            <Examenes preguntas={datos.preguntas} examenes={datos.examenes} clusters={datos.clusters} />
          )}
          {vista === "progreso" && <Progreso clusters={datos.clusters} meta={datos.meta} />}
        </main>
      )}

      {datos && (
        <>
          <footer className="mt-10 border-t border-stone-200 pt-4 text-[11px] leading-relaxed text-stone-500 dark:border-stone-800 dark:text-stone-400">
            <p>
              <b>Fuente:</b> {datos.meta.fuente}. {datos.meta.aviso}
            </p>
            <p className="mt-1">
              {datos.meta.totales.preguntas} preguntas de exámenes oficiales ({datos.meta.anios.join(", ")}).
              Gratuito y sin cuenta.
            </p>
          </footer>

          <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-stone-200 bg-white/95 backdrop-blur dark:border-stone-800 dark:bg-stone-950/95">
            <div className="mx-auto flex max-w-2xl">
              {NAV.map((n) => {
                const activo = vista === n.id;
                return (
                  <button
                    key={n.id}
                    type="button"
                    onClick={() => setVista(n.id)}
                    aria-current={activo ? "page" : undefined}
                    className={
                      "flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-medium transition " +
                      (activo
                        ? "text-emerald-700 dark:text-emerald-400"
                        : "text-stone-500 hover:text-stone-800 dark:text-stone-400 dark:hover:text-stone-200")
                    }
                  >
                    <span aria-hidden className="text-lg leading-none">
                      {n.icono}
                    </span>
                    {n.texto}
                  </button>
                );
              })}
            </div>
          </nav>
        </>
      )}
    </div>
  );
}
