import { useEffect, useMemo, useState } from "react";
import { cargaSm2, repasaTarjeta, altaTarjeta, reiniciaProgreso } from "../store";
import { enDias, vencidas, proximas } from "../sm2";
import type { Cluster, Letra } from "../types";
import { EtiquetaRepeticion, EtiquetaTema, RefArticulos, TarjetaOpcion } from "../components/ui";

type Pestana = "hoy" | "tarjetas";

const BOTONES_SM2 = [
  { q: 1, t: "Otra vez", d: "hoy", cls: "border-rose-400 text-rose-700 hover:bg-rose-50 dark:hover:bg-rose-950/40" },
  { q: 3, t: "Difícil", d: "1 d", cls: "border-amber-400 text-amber-700 hover:bg-amber-50 dark:hover:bg-amber-950/40" },
  { q: 4, t: "Bien", d: "3 d", cls: "border-emerald-400 text-emerald-700 hover:bg-emerald-50 dark:hover:bg-emerald-950/40" },
  { q: 5, t: "Fácil", d: "×ef", cls: "border-sky-400 text-sky-700 hover:bg-sky-50 dark:hover:bg-sky-950/40" },
];

export default function CardsMode({
  clusters,
  onIrATest,
}: {
  clusters: Cluster[];
  onIrATest: () => void;
}) {
  const [pestana, setPestana] = useState<Pestana>("hoy");
  const [, rerender] = useState(0);
  const porId = useMemo(() => {
    const m = new Map<number, Cluster>();
    for (const c of clusters) m.set(c.cluster_id, c);
    return m;
  }, [clusters]);

  // ── estado del repaso de hoy ──
  const [cola, setCola] = useState<number[]>([]);
  const [revelada, setRevelada] = useState(false);

  useEffect(() => {
    if (pestana !== "hoy") return;
    const ts = cargaSm2();
    const hoy = vencidas(ts).map((t) => t.id);
    setCola(hoy);
    setRevelada(false);
  }, [pestana]);

  function responde(q: number) {
    if (!cola.length) return;
    const id = cola[0];
    repasaTarjeta(id, q);
    setCola((c) => c.slice(1));
    setRevelada(false);
    rerender((n) => n + 1);
  }

  const ts = cargaSm2();
  const totalTarjetas = Object.keys(ts).length;
  const programadas = proximas(ts);

  // ── pestaña de tarjetas: navegación libre ordenada por score ──
  const ordenadas = useMemo(() => [...clusters].sort((a, b) => b.score - a.score), [clusters]);
  const [idxTarjeta, setIdxTarjeta] = useState(0);
  const [reveladaT, setReveladaT] = useState(false);

  if (pestana === "hoy") {
    const id = cola[0];
    const c = id !== undefined ? porId.get(id) : undefined;
    return (
      <section className="space-y-4">
        <header className="card bg-gradient-to-br from-amber-500 to-orange-600 text-white dark:from-amber-700 dark:to-orange-800">
          <h2 className="text-base font-bold">Repaso del día</h2>
          <p className="mt-1 text-sm text-amber-50">
            Repetición espaciada (SM-2) sobre tus errores. Las tarjetas vuelven
            cuando están a punto de olvidarse, no antes.
          </p>
        </header>

        <Pestanas pestana={pestana} setPestana={setPestana} nHoy={cola.length} nTarjetas={totalTarjetas} />

        {totalTarjetas === 0 && (
          <div className="card text-center">
            <p className="text-sm text-stone-500">
              Todavía no hay tarjetas. Se crean solas cuando fallas una pregunta en un test.
            </p>
            <button type="button" onClick={onIrATest} className="btn-primario mt-3">
              Hacer un test
            </button>
          </div>
        )}

        {totalTarjetas > 0 && cola.length === 0 && (
          <div className="card text-center">
            <p className="text-2xl">🎉</p>
            <p className="mt-1 text-sm font-semibold">Repaso de hoy terminado</p>
            <p className="mt-1 text-xs text-stone-500">
              {programadas.length > 0
                ? `Próxima tarjeta ${enDias(programadas[0].proximo)}.`
                : "No hay más tarjetas programadas."}
            </p>
          </div>
        )}

        {c && (
          <>
            <article className="card space-y-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold text-stone-400">
                  {cola.length} por repasar
                </span>
                <div className="flex flex-wrap items-center gap-2">
                  <EtiquetaTema cluster={c} />
                  <RefArticulos articulos={c.articulos} tema={c.tema} />
                </div>
              </div>
              <h3 className="text-base font-semibold leading-snug">{c.enunciado}</h3>
              {revelada ? (
                <ul className="grid gap-1.5 text-sm">
                  {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                    <TarjetaOpcion
                      key={l}
                      opciones={c.opciones}
                      letra={l}
                      estado={l === c.correcta ? "correcta" : "ninguna"}
                      elegida={null}
                    />
                  ))}
                </ul>
              ) : (
                <p className="text-center text-sm text-stone-500">
                  Piensa la respuesta y luego revélala.
                </p>
              )}
            </article>

            {!revelada ? (
              <button type="button" onClick={() => setRevelada(true)} className="btn-primario w-full py-3">
                Ver respuesta
              </button>
            ) : (
              <div className="grid grid-cols-4 gap-2">
                {BOTONES_SM2.map((b) => (
                  <button
                    key={b.q}
                    type="button"
                    onClick={() => responde(b.q)}
                    className={"btn flex-col border bg-white py-2 dark:bg-stone-900 " + b.cls}
                  >
                    <span className="text-sm font-bold">{b.t}</span>
                    <span className="text-[10px] opacity-70">{b.d}</span>
                  </button>
                ))}
              </div>
            )}
          </>
        )}

        {programadas.length > 0 && (
          <div className="card">
            <h3 className="text-sm font-bold">Calendario</h3>
            <ul className="mt-2 space-y-1 text-xs text-stone-500">
              {programadas.slice(0, 5).map((t) => (
                <li key={t.id}>
                  {enDias(t.proximo)} · {(porId.get(t.id)?.enunciado ?? "").slice(0, 60)}…
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    );
  }

  // ── pestaña tarjetas ──
  const c = ordenadas[idxTarjeta];
  return (
    <section className="space-y-4">
      <header className="card bg-gradient-to-br from-emerald-600 to-teal-700 text-white dark:from-emerald-800 dark:to-teal-900">
        <h2 className="text-base font-bold">Tarjetas de lo más preguntado</h2>
        <p className="mt-1 text-sm text-emerald-50">
          Las {ordenadas.length} preguntas del bloque común ordenadas por peso real en los
          exámenes. Primero las que más caen.
        </p>
      </header>

      <Pestanas pestana={pestana} setPestana={setPestana} nHoy={cola.length} nTarjetas={totalTarjetas} />

      <div className="flex items-center justify-between gap-2">
        <button
          type="button"
          onClick={() => {
            setIdxTarjeta((i) => Math.max(0, i - 1));
            setReveladaT(false);
          }}
          disabled={idxTarjeta === 0}
          className="btn-secundario"
        >
          ←
        </button>
        <span className="text-sm font-semibold tabular-nums">
          {idxTarjeta + 1} / {ordenadas.length}
        </span>
        <button
          type="button"
          onClick={() => {
            setIdxTarjeta((i) => Math.min(ordenadas.length - 1, i + 1));
            setReveladaT(false);
          }}
          disabled={idxTarjeta >= ordenadas.length - 1}
          className="btn-secundario"
        >
          →
        </button>
      </div>

      {c && (
        <article className="card space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <EtiquetaTema cluster={c} />
            <EtiquetaRepeticion cluster={c} />
            <RefArticulos articulos={c.articulos} tema={c.tema} />
          </div>
          <h3 className="text-base font-semibold leading-snug">{c.enunciado}</h3>
          {reveladaT ? (
            <>
              <ul className="grid gap-1.5 text-sm">
                {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                  <TarjetaOpcion
                    key={l}
                    opciones={c.opciones}
                    letra={l}
                    estado={l === c.correcta ? "correcta" : "ninguna"}
                    elegida={null}
                  />
                ))}
              </ul>
              <p className="text-xs text-stone-500">
                Aparece en {c.anios.join(", ")} · {c.ocurrencias
                  .map((o) => o.modalidad)
                  .join(" / ")}
              </p>
              <button
                type="button"
                onClick={() => altaTarjeta(c.cluster_id)}
                className="btn-secundario w-full text-xs"
              >
                + Añadir a mis tarjetas
              </button>
            </>
          ) : (
            <button
              type="button"
              onClick={() => setReveladaT(true)}
              className="btn-primario w-full py-3"
            >
              Ver respuesta
            </button>
          )}
        </article>
      )}

      <button
        type="button"
        onClick={() => {
          if (confirm("¿Borrar todo el progreso (intentos, errores, tarjetas y stats)?")) {
            reiniciaProgreso();
            rerender((n) => n + 1);
          }
        }}
        className="btn-secundario w-full text-rose-600"
      >
        Vaciar progreso y tarjetas
      </button>
    </section>
  );
}

function Pestanas({
  pestana,
  setPestana,
  nHoy,
  nTarjetas,
}: {
  pestana: Pestana;
  setPestana: (p: Pestana) => void;
  nHoy: number;
  nTarjetas: number;
}) {
  return (
    <div className="flex gap-2 rounded-xl bg-stone-200/60 p-1 dark:bg-stone-800/60">
      <button
        type="button"
        onClick={() => setPestana("hoy")}
        className={
          "flex-1 rounded-lg px-3 py-2 text-sm font-semibold transition " +
          (pestana === "hoy"
            ? "bg-white shadow dark:bg-stone-900"
            : "text-stone-600 dark:text-stone-300")
        }
      >
        Hoy {nHoy > 0 && <span className="ml-1 chip bg-rose-100 text-rose-800">{nHoy}</span>}
      </button>
      <button
        type="button"
        onClick={() => setPestana("tarjetas")}
        className={
          "flex-1 rounded-lg px-3 py-2 text-sm font-semibold transition " +
          (pestana === "tarjetas"
            ? "bg-white shadow dark:bg-stone-900"
            : "text-stone-600 dark:text-stone-300")
        }
      >
        Tarjetas {nTarjetas > 0 && <span className="ml-1 chip bg-stone-200 text-stone-700">{nTarjetas}</span>}
      </button>
    </div>
  );
}
