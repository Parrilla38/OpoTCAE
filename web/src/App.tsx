import { useEffect, useState } from "react";
import { cargaBase, cargaClusters, cargaPreguntas } from "./data";
import { Sello } from "./components/ui";
import Practicar from "./views/Practicar";
import Aprender from "./views/Aprender";
import Examenes from "./views/Examenes";
import Progreso from "./views/Progreso";
import Guia from "./views/Guia";

type Vista = "practicar" | "aprender" | "examenes" | "progreso";

const NAV: { id: Vista; texto: string }[] = [
  { id: "practicar", texto: "Practicar" },
  { id: "aprender", texto: "Aprender" },
  { id: "examenes", texto: "Exámenes" },
  { id: "progreso", texto: "Progreso" },
];

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

function BotonGuia({ onClick }: { onClick: () => void }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label="Cómo se usa"
      title="Cómo se usa"
      className="grid h-8 w-8 place-items-center rounded-full border border-hilo font-mono text-[13px] font-bold text-suave transition hover:bg-superficie hover:text-tinta"
    >
      ?
    </button>
  );
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
      className="grid h-8 w-8 place-items-center rounded-full border border-hilo text-suave transition hover:bg-superficie"
    >
      <span aria-hidden className="text-[13px]">
        {oscuro ? "☾" : "◐"}
      </span>
    </button>
  );
}

function Cargando({ texto = "Cargando…" }: { texto?: string }) {
  return (
    <div className="tarjeta px-4 py-5 text-sm text-suave">{texto}</div>
  );
}

function Aviso({ error }: { error: string }) {
  return (
    <div className="rounded-accion border border-mal bg-aguamal px-4 py-3.5 text-[13.8px] text-mal">
      <p className="font-semibold">No se han podido cargar las preguntas</p>
      <p className="mt-0.5 text-xs">{error}</p>
    </div>
  );
}

export default function App() {
  const [vista, setVista] = useState<Vista>("practicar");
  const [verGuia, setVerGuia] = useState(false);
  const { datos: base, error: errorBase } = useDatos(cargaBase, true);
  const { datos: clusters, error: errorClusters } = useDatos(
    cargaClusters,
    vista === "practicar" || vista === "aprender" || vista === "progreso"
  );
  const { datos: preguntas, error: errorPreguntas } = useDatos(cargaPreguntas, vista === "examenes");

  const error = errorBase ?? (vista === "examenes" ? errorPreguntas : errorClusters);

  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col px-4 pb-28 pt-5">
      {verGuia && <Guia onCerrar={() => setVerGuia(false)} />}
      <header className="mb-7 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <Sello />
          <div>
            <h1 className="text-[17px] font-semibold leading-none tracking-tight">opotcae</h1>
            <p className="etiqueta mt-1">TCAE · Andalucía</p>
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          <BotonGuia onClick={() => setVerGuia(true)} />
          <BotonTema />
        </div>
      </header>

      {error && <Aviso error={error} />}

      <main className="flex-1 space-y-3">
        {!base && !errorBase && <Cargando />}

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
          <footer className="mt-10 border-t border-hilo pt-4 text-[11px] leading-relaxed text-suave">
            <p>
              <b className="text-tinta">Fuente:</b> {base.meta.fuente}. {base.meta.aviso}
            </p>
            <p className="mt-1.5 font-mono uppercase tracking-wider">
              {base.meta.totales.preguntas} preguntas · {base.meta.anios.join(", ")} · gratis y sin
              cuenta
            </p>
            <p className="mt-2">
              <button
                type="button"
                onClick={() => setVerGuia(true)}
                className="font-semibold text-verde underline underline-offset-2"
              >
                ¿Cómo se usa? Lee la guía
              </button>
            </p>
          </footer>

          <nav className="pie">
            <div className="pie-caja">
              {NAV.map((n) => (
                <button
                  key={n.id}
                  type="button"
                  onClick={() => setVista(n.id)}
                  aria-current={vista === n.id ? "page" : undefined}
                  className={`pie-item${vista === n.id ? " pie-item-on" : ""}`}
                >
                  {n.texto}
                </button>
              ))}
            </div>
          </nav>
        </>
      )}
    </div>
  );
}
