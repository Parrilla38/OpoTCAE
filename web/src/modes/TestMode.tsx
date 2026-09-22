import { useEffect, useMemo, useRef, useState } from "react";
import { ordenaPorScore } from "../data";
import { CONFIG_DEFECTO, idsConErrores, registraIntento } from "../store";
import type { Cluster, ConfigTest, Letra, Meta, ResultadoPregunta } from "../types";
import { BarraProgreso, EtiquetaRepeticion, EtiquetaTema, RefArticulos, TarjetaOpcion } from "../components/ui";

type Fase = "config" | "jugando" | "resultado";

function eligePreguntas(clusters: Cluster[], cfg: ConfigTest, fallados: Set<number>): Cluster[] {
  let base = [...clusters];
  if (cfg.filtro === "repetidas") {
    base = ordenaPorScore(base.filter((c) => c.frecuencia > 1 || c.n_anios > 1));
    if (base.length < cfg.n) {
      const extras = ordenaPorScore(clusters).filter((c) => !base.includes(c));
      base = [...base, ...extras];
    }
  } else if (cfg.filtro === "tema" && cfg.tema !== null) {
    base = ordenaPorScore(base.filter((c) => c.tema === cfg.tema));
  } else if (cfg.filtro === "errores") {
    base = ordenaPorScore(base.filter((c) => fallados.has(c.cluster_id)));
  } else {
    base = ordenaPorScore(base);
  }
  // muestreo ponderado por score: lo más repetido sale antes
  const pool = [...base];
  const salida: Cluster[] = [];
  while (salida.length < cfg.n && pool.length) {
    const total = pool.reduce((s, c) => s + c.score + 0.5, 0);
    let r = Math.random() * total;
    let idx = 0;
    for (let i = 0; i < pool.length; i++) {
      r -= pool[i].score + 0.5;
      if (r <= 0) {
        idx = i;
        break;
      }
    }
    salida.push(pool[idx]);
    pool.splice(idx, 1);
  }
  return salida;
}

export default function TestMode({
  clusters,
  meta,
  onIrAErrores,
}: {
  clusters: Cluster[];
  meta: Meta;
  onIrAErrores: () => void;
}) {
  const [fase, setFase] = useState<Fase>("config");
  const [cfg, setCfg] = useState<ConfigTest>(CONFIG_DEFECTO);
  const [bateria, setBateria] = useState<Cluster[]>([]);
  const [respuestas, setRespuestas] = useState<Record<number, Letra | null>>({});
  const [idx, setIdx] = useState(0);
  const [nota, setNota] = useState<{ aciertos: number; fallos: number; en_blanco: number; nota: number } | null>(null);
  const [segundos, setSegundos] = useState(0);
  const cronometro = useRef<number | null>(null);

  const fallados = useMemo(() => new Set(idsConErrores()), [fase]);

  useEffect(() => {
    if (fase !== "jugando" || !cfg.cronometrado) return;
    setSegundos(cfg.minutos * 60);
    cronometro.current = window.setInterval(() => {
      setSegundos((s) => {
        if (s <= 1) {
          window.clearInterval(cronometro.current ?? undefined);
          finaliza();
          return 0;
        }
        return s - 1;
      });
    }, 1000);
    return () => window.clearInterval(cronometro.current ?? undefined);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fase, cfg.cronometrado]);

  function empieza() {
    const sel = eligePreguntas(clusters, cfg, fallados);
    if (!sel.length) {
      alert("No hay preguntas con ese filtro. Prueba con «Todo el bloque».");
      return;
    }
    setBateria(sel);
    setRespuestas({});
    setIdx(0);
    setNota(null);
    setFase("jugando");
  }

  function finaliza() {
    const resultados: ResultadoPregunta[] = bateria.map((c) => {
      const elegida = respuestas[c.cluster_id] ?? null;
      return {
        cluster_id: c.cluster_id,
        elegida,
        acierto: elegida !== null && elegida === c.correcta,
      };
    });
    const intento = registraIntento(cfg, resultados);
    setNota({ aciertos: intento.aciertos, fallos: intento.fallos, en_blanco: intento.en_blanco, nota: intento.nota });
    setFase("resultado");
  }

  const minutos = String(Math.floor(segundos / 60)).padStart(2, "0");
  const segs = String(segundos % 60).padStart(2, "0");

  if (fase === "config") {
    return (
      <section className="space-y-4">
        <div className="card bg-gradient-to-br from-marca-600 to-emerald-700 text-white dark:from-marca-700 dark:to-emerald-900">
          <h2 className="text-base font-bold">Modo Test</h2>
          <p className="mt-1 text-sm text-emerald-50">
            {meta.totales.preguntas} preguntas del bloque común (Temas 1-10), extraídas de{" "}
            {meta.totales.examenes} exámenes oficiales del SAS ({meta.anios.join(", ")}). Lo que más
            se repite sale primero.
          </p>
        </div>

        <div className="card space-y-4">
          <div>
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-stone-500">
              Nº de preguntas
            </label>
            <div className="grid grid-cols-4 gap-2">
              {[5, 10, 25, 50].map((n) => (
                <button
                  key={n}
                  type="button"
                  onClick={() => setCfg({ ...cfg, n })}
                  className={cfg.n === n ? "btn-primario" : "btn-secundario"}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-stone-500">
              Banco de preguntas
            </label>
            <div className="grid gap-2 sm:grid-cols-2">
              {[
                { id: "repetidas", t: "Solo lo repetido", d: "Lo que cae más de una vez" },
                { id: "todas", t: "Todo el bloque", d: "Las 166 preguntas del bloque común" },
                { id: "tema", t: "Por tema", d: "Elige un Tema 1-10" },
                { id: "errores", t: "Mis errores", d: `${fallados.size} preguntas en la libreta` },
              ].map((o) => (
                <button
                  key={o.id}
                  type="button"
                  onClick={() => setCfg({ ...cfg, filtro: o.id as ConfigTest["filtro"] })}
                  className={
                    "rounded-xl border p-3 text-left text-sm transition " +
                    (cfg.filtro === o.id
                      ? "border-marca-600 bg-marca-50 ring-1 ring-marca-600 dark:bg-marca-950"
                      : "border-stone-200 bg-white hover:border-marca-400 dark:border-stone-800 dark:bg-stone-900")
                  }
                >
                  <div className="font-semibold">{o.t}</div>
                  <div className="text-xs text-stone-500 dark:text-stone-400">{o.d}</div>
                </button>
              ))}
            </div>
          </div>

          {cfg.filtro === "tema" && (
            <div>
              <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-stone-500">
                Tema
              </label>
              <select
                className="campo"
                value={cfg.tema ?? ""}
                onChange={(e) => setCfg({ ...cfg, tema: e.target.value ? Number(e.target.value) : null })}
              >
                <option value="">— elige tema —</option>
                {meta.temas.map((t) => (
                  <option key={t.tema} value={t.tema}>
                    T{String(t.tema).padStart(2, "0")} · {t.nombre} ({t.preguntas})
                  </option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-stone-500">
              Penalización por error
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { v: 0, t: "Sin penalizar" },
                { v: 0.25, t: "¼ (como el SAS)" },
                { v: 0.333, t: "⅓" },
              ].map((o) => (
                <button
                  key={o.v}
                  type="button"
                  onClick={() => setCfg({ ...cfg, penalizacion: o.v })}
                  className={cfg.penalizacion === o.v ? "btn-primario" : "btn-secundario"}
                >
                  {o.t}
                </button>
              ))}
            </div>
          </div>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={cfg.cronometrado}
              onChange={(e) => setCfg({ ...cfg, cronometrado: e.target.checked })}
              className="h-4 w-4 rounded border-stone-300 text-marca-600 focus:ring-marca-600"
            />
            Cronometrado
            {cfg.cronometrado && (
              <input
                type="number"
                min={1}
                max={180}
                value={cfg.minutos}
                onChange={(e) => setCfg({ ...cfg, minutos: Number(e.target.value) || 15 })}
                className="campo w-20"
                aria-label="minutos"
              />
            )}
            {cfg.cronometrado && <span className="text-xs text-stone-500">minutos</span>}
          </label>

          <button type="button" onClick={empieza} className="btn-primario w-full py-3 text-base">
            Empezar test
          </button>
          {cfg.filtro === "errores" && fallados.size === 0 && (
            <p className="text-center text-xs text-stone-500">
              Aún no tienes errores.{" "}
              <button type="button" onClick={onIrAErrores} className="underline">
                Ver libreta
              </button>
            </p>
          )}
        </div>
      </section>
    );
  }

  if (fase === "jugando") {
    const c = bateria[idx];
    const elegida = respuestas[c.cluster_id] ?? null;
    const respondidas = Object.keys(respuestas).length;
    return (
      <section className="space-y-4">
        <div className="flex items-center justify-between gap-3">
          <div className="text-sm font-semibold">
            {idx + 1} / {bateria.length}
          </div>
          {cfg.cronometrado && (
            <div className={"text-sm font-mono font-bold " + (segundos < 60 ? "text-rose-600" : "")}>
              ⏱ {minutos}:{segs}
            </div>
          )}
          <button type="button" onClick={finaliza} className="btn-fantasma text-xs">
            Terminar
          </button>
        </div>
        <BarraProgreso valor={respondidas} total={bateria.length} />

        <article className="card space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <EtiquetaTema cluster={c} />
            <EtiquetaRepeticion cluster={c} />
          </div>
          <h2 className="text-base font-semibold leading-snug">{c.enunciado}</h2>
          <div className="grid gap-2">
            {(["A", "B", "C", "D"] as Letra[]).map((l) => (
              <TarjetaOpcion
                key={l}
                opciones={c.opciones}
                letra={l}
                estado="neutra"
                elegida={elegida}
                onElige={(letra) => setRespuestas({ ...respuestas, [c.cluster_id]: letra })}
              />
            ))}
          </div>
          <p className="text-center text-xs text-stone-500">
            En blanco si dudas: no penaliza. En el examen real sí penaliza el error.
          </p>
        </article>

        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setIdx((i) => Math.max(0, i - 1))}
            disabled={idx === 0}
            className="btn-secundario flex-1"
          >
            ← Anterior
          </button>
          {idx < bateria.length - 1 ? (
            <button type="button" onClick={() => setIdx((i) => i + 1)} className="btn-primario flex-1">
              Siguiente →
            </button>
          ) : (
            <button type="button" onClick={finaliza} className="btn-primario flex-1">
              Corregir
            </button>
          )}
        </div>
      </section>
    );
  }

  // fase === "resultado"
  return (
    <section className="space-y-4">
      <div className="card text-center">
        <p className="text-xs font-semibold uppercase tracking-wide text-stone-500">Resultado</p>
        <p className="mt-1 text-4xl font-bold tabular-nums">
          {nota?.nota ?? 0}
          <span className="text-lg text-stone-400">/10</span>
        </p>
        <p className="mt-1 text-sm text-stone-600 dark:text-stone-300">
          {nota?.aciertos ?? 0} aciertos · {nota?.fallos ?? 0} fallos · {nota?.en_blanco ?? 0} en
          blanco
        </p>
        {cfg.penalizacion > 0 && (
          <p className="mt-1 text-xs text-stone-500">
            Penalización aplicada: −{cfg.penalizacion} por error
          </p>
        )}
      </div>

      <div className="space-y-3">
        {bateria.map((c, i) => {
          const elegida = respuestas[c.cluster_id] ?? null;
          const acierto = elegida === c.correcta;
          return (
            <article
              key={c.cluster_id}
              className={"card space-y-3 " + (acierto ? "" : "border-l-4 border-l-rose-500")}
            >
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold text-stone-400">{i + 1}</span>
                <div className="flex flex-wrap items-center gap-2">
                  <EtiquetaTema cluster={c} />
                  <RefArticulos articulos={c.articulos} tema={c.tema} />
                </div>
              </div>
              <h3 className="text-sm font-semibold leading-snug">{c.enunciado}</h3>
              <div className="grid gap-2">
                {(["A", "B", "C", "D"] as Letra[]).map((l) => {
                  const estado =
                    l === c.correcta ? "correcta" : l === elegida ? "fallada" : "ninguna";
                  return (
                    <TarjetaOpcion
                      key={l}
                      opciones={c.opciones}
                      letra={l}
                      estado={estado}
                      elegida={elegida}
                    />
                  );
                })}
              </div>
              <p className="text-xs text-stone-500">
                Aparece en {c.anios.join(", ")} · {c.frecuencia} vez/veces ·{" "}
                {c.ocurrencias.map((o) => o.modalidad).join(" / ")}
              </p>
            </article>
          );
        })}
      </div>

      <div className="flex gap-2">
        <button type="button" onClick={() => setFase("config")} className="btn-secundario flex-1">
          Nuevo test
        </button>
        <button type="button" onClick={onIrAErrores} className="btn-primario flex-1">
          Ver mis errores
        </button>
      </div>
    </section>
  );
}
