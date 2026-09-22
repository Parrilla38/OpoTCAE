import { useEffect, useState } from "react";
import { cargaTodo } from "./data";
import type { Cluster, ConceptosData, Examen, Meta, Pregunta } from "./types";
import TestMode from "./modes/TestMode";
import ReviewMode from "./modes/ReviewMode";
import PastExamsMode from "./modes/PastExamsMode";
import CardsMode from "./modes/CardsMode";
import StatsMode from "./modes/StatsMode";

type Vista = "test" | "repaso" | "examenes" | "tarjetas" | "stats";

const NAV: { id: Vista; etiqueta: string; icono: string }[] = [
  { id: "test", etiqueta: "Test", icono: "🎯" },
  { id: "repaso", etiqueta: "Repaso", icono: "📖" },
  { id: "examenes", etiqueta: "Exámenes", icono: "🗓️" },
  { id: "tarjetas", etiqueta: "Tarjetas", icono: "🃏" },
  { id: "stats", etiqueta: "Stats", icono: "📊" },
];

function BotonTema() {
  const [oscuro, setOscuro] = useState(() => document.documentElement.classList.contains("dark"));
  useEffect(() => {
    document.documentElement.classList.toggle("dark", oscuro);
    localStorage.setItem("tcae-tema", oscuro ? "oscuro" : "claro");
  }, [oscuro]);
  return (
    <button
      type="button"
      onClick={() => setOscuro((v) => !v)}
      aria-label={oscuro ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
      title={oscuro ? "Modo claro" : "Modo oscuro"}
      className="btn-fantasma h-10 w-10 rounded-full p-0 text-base"
    >
      {oscuro ? "☀️" : "🌙"}
    </button>
  );
}

export default function App() {
  const [vista, setVista] = useState<Vista>("test");
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
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col px-4 pb-24 pt-4">
      <header className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h1 className="text-lg font-bold leading-tight tracking-tight">
            TCAE Andalucía
          </h1>
          <p className="text-xs text-stone-500 dark:text-stone-400">
            Lo que más se repite en los exámenes oficiales del SAS
          </p>
        </div>
        <BotonTema />
      </header>

      {error && (
        <div className="card border-rose-300 bg-rose-50 text-rose-800 dark:border-rose-800 dark:bg-rose-950/40 dark:text-rose-200">
          <p className="text-sm font-semibold">No se pudieron cargar los datos</p>
          <p className="text-xs">{error}</p>
        </div>
      )}

      {!datos && !error && (
        <div className="card animate-pulse text-sm text-stone-500">Cargando preguntas…</div>
      )}

      {datos && (
        <main className="flex-1">
          {vista === "test" && (
            <TestMode
              clusters={datos.clusters}
              meta={datos.meta}
              onIrAErrores={() => setVista("tarjetas")}
            />
          )}
          {vista === "repaso" && (
            <ReviewMode clusters={datos.clusters} meta={datos.meta} conceptos={datos.conceptos} />
          )}
          {vista === "examenes" && (
            <PastExamsMode
              preguntas={datos.preguntas}
              examenes={datos.examenes}
              clusters={datos.clusters}
            />
          )}
          {vista === "tarjetas" && (
            <CardsMode clusters={datos.clusters} onIrATest={() => setVista("test")} />
          )}
          {vista === "stats" && <StatsMode clusters={datos.clusters} meta={datos.meta} />}
        </main>
      )}

      {datos && (
        <>
          <footer className="mt-8 border-t border-stone-200 pt-4 text-[11px] leading-relaxed text-stone-500 dark:border-stone-800 dark:text-stone-400">
            <p>
              <strong>Fuente:</strong> {datos.meta.fuente}. {datos.meta.aviso}
            </p>
            <p className="mt-1">
              Análisis sobre {datos.meta.totales.preguntas} preguntas de bloque común (
              {datos.meta.anios.join(", ")}). Score = frecuencia × (1 + 0,25 × años). 2008 queda
              archivado. Gratuito, sin cuenta.
            </p>
          </footer>

          <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-stone-200 bg-white/95 backdrop-blur dark:border-stone-800 dark:bg-stone-950/95">
            <div className="mx-auto flex max-w-3xl">
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
                        ? "text-marca-700 dark:text-marca-400"
                        : "text-stone-500 hover:text-stone-800 dark:text-stone-400 dark:hover:text-stone-200")
                    }
                  >
                    <span aria-hidden className="text-lg leading-none">
                      {n.icono}
                    </span>
                    {n.etiqueta}
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
