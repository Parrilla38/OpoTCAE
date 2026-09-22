import { useEffect, useState } from "react";
import { cargaBase, cargaClusters, cargaPreguntas } from "./data";
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

/** Hook: pide datos la primera vez que hacen falta y los mantiene. */
function useDatos<T>(pedir: () => Promise<T>, activo: boolean) {
  const [datos, setDatos] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    if (!activo || datos) return;
    pedir()
      .then(setDatos)
      .catch((e) => setError(String(e)));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activo]);
  return { datos, error };
}

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

function Cargando({ texto = "Cargando preguntas…" }: { texto?: string }) {
  return (
    <div className="rounded-2xl border border-stone-200 bg-white p-5 text-sm text-stone-500 dark:border-stone-800 dark:bg-stone-900">
      {texto}
    </div>
  );
}

function Aviso({ error }: { error: string }) {
  return (
    <div className="rounded-2xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
      <p className="font-semibold">No se han podido cargar las preguntas</p>
      <p className="text-xs">{error}</p>
    </div>
  );
}

export default function App() {
  const [vista, setVista] = useState<Vista>("practicar");
  const { datos: base, error: errorBase } = useDatos(cargaBase, true);
  const { datos: clusters, error: errorClusters } = useDatos(
    cargaClusters,
    vista === "practicar" || vista === "aprender" || vista === "progreso"
  );
  const { datos: preguntas, error: errorPreguntas } = useDatos(cargaPreguntas, vista === "examenes");

  const error = errorBase ?? (vista === "examenes" ? errorPreguntas : errorClusters);

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

      {error && <Aviso error={error} />}

      <main className="flex-1 space-y-3">
        {!base && !errorBase && <Cargando texto="Cargando…" />}

        {base && vista === "practicar" && (
          <>
            {!clusters && !errorClusters && <Cargando />}
            {clusters && (
              <Practicar
                clusters={clusters}
                meta={base.meta}
                onIrAProgreso={() => setVista("progreso")}
              />
            )}
          </>
        )}

        {base && vista === "aprender" && (
          <>
            {!clusters && !errorClusters && <Cargando />}
            {clusters && <Aprender clusters={clusters} meta={base.meta} />}
          </>
        )}

        {base && vista === "examenes" && (
          <>
            {!preguntas && !errorPreguntas && <Cargando texto="Cargando exámenes…" />}
            {preguntas && clusters && (
              <Examenes preguntas={preguntas} examenes={base.examenes} clusters={clusters} />
            )}
            {!preguntas && !clusters && !errorClusters && <Cargando />}
          </>
        )}

        {base && vista === "progreso" && (
          <>
            {!clusters && !errorClusters && <Cargando />}
            {clusters && <Progreso clusters={clusters} meta={base.meta} />}
          </>
        )}
      </main>

      {base && (
        <>
          <footer className="mt-10 border-t border-stone-200 pt-4 text-[11px] leading-relaxed text-stone-500 dark:border-stone-800 dark:text-stone-400">
            <p>
              <b>Fuente:</b> {base.meta.fuente}. {base.meta.aviso}
            </p>
            <p className="mt-1">
              {base.meta.totales.preguntas} preguntas de exámenes oficiales (
              {base.meta.anios.join(", ")}). Gratuito y sin cuenta.
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
