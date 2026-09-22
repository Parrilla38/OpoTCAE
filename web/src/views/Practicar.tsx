import { useMemo, useState } from "react";
import { ordenaPorScore } from "../data";
import { registraIntento, cargaSm2 } from "../store";
import { vencidas } from "../sm2";
import type { Cluster, ConfigTest, Letra, Meta, ResultadoPregunta } from "../types";
import { AccionPrincipal, AccionSecundaria, Barra, Boton, NombreTema, Opcion, Segmentado } from "../components/ui";
import ComoFunciona from "../components/ComoFunciona";

type Fase = "inicio" | "jugando" | "resultado";

interface Ajustes {
  n: number;
  tema: number | null;
  penaliza: boolean;
  cronometrado: boolean;
  soloRepetidas: boolean;
}

const AJUSTES_INICIO: Ajustes = {
  n: 10,
  tema: null,
  penaliza: true,
  cronometrado: false,
  soloRepetidas: false,
};

function eligePreguntas(clusters: Cluster[], a: Ajustes): Cluster[] {
  let base = [...clusters];
  if (a.soloRepetidas) base = base.filter((c) => c.frecuencia > 1 || c.n_anios > 1);
  if (a.tema !== null) base = base.filter((c) => c.tema === a.tema);
  base = ordenaPorScore(base);
  // muestreo ponderado: lo que más cae sale antes, pero no siempre lo mismo
  const pool = [...base];
  const salida: Cluster[] = [];
  while (salida.length < a.n && pool.length) {
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

export default function Practicar({
  clusters,
  meta,
  onIrAProgreso,
}: {
  clusters: Cluster[];
  meta: Meta;
  onIrAProgreso: () => void;
}) {
  const [fase, setFase] = useState<Fase>("inicio");
  const [ajustes, setAjustes] = useState<Ajustes>(AJUSTES_INICIO);
  const [verAjustes, setVerAjustes] = useState(false);
  const [bateria, setBateria] = useState<Cluster[]>([]);
  const [respuestas, setRespuestas] = useState<Record<number, Letra | null>>({});
  const [idx, setIdx] = useState(0);
  const [segundos, setSegundos] = useState(0);
  const [resultado, setResultado] = useState<{ aciertos: number; fallos: number; en_blanco: number; nota: number } | null>(null);

  const porRepasar = useMemo(() => vencidas(cargaSm2()).length, [fase]);

  function empieza(config: Ajustes) {
    const sel = eligePreguntas(clusters, config);
    if (!sel.length) {
      alert("No hay preguntas con ese filtro. Prueba con otro tema.");
      return;
    }
    setBateria(sel);
    setRespuestas({});
    setIdx(0);
    setResultado(null);
    setSegundos(config.cronometrado ? config.n * 72 : 0); // ~72 s por pregunta
    setFase("jugando");
  }

  function termina() {
    const resultados: ResultadoPregunta[] = bateria.map((c) => {
      const elegida = respuestas[c.cluster_id] ?? null;
      return { cluster_id: c.cluster_id, elegida, acierto: elegida !== null && elegida === c.correcta };
    });
    const cfg: ConfigTest = {
      n: bateria.length,
      penalizacion: ajustes.penaliza ? 0.25 : 0,
      filtro: ajustes.soloRepetidas ? "repetidas" : ajustes.tema !== null ? "tema" : "todas",
      tema: ajustes.tema,
      cronometrado: ajustes.cronometrado,
      minutos: Math.round(ajustes.n * 1.2),
    };
    const i = registraIntento(cfg, resultados);
    setResultado({ aciertos: i.aciertos, fallos: i.fallos, en_blanco: i.en_blanco, nota: i.nota });
    setFase("resultado");
  }

  // ─────────── pantalla de inicio ───────────
  if (fase === "inicio") {
    return (
      <section className="space-y-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">¿Qué hacemos hoy?</h2>
          <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">
            {meta.totales.preguntas} preguntas de los exámenes oficiales del SAS, con lo que más se
            repite primero.
          </p>
        </div>

        <AccionPrincipal
          icono="🎯"
          onClick={() => empieza(ajustes)}
          subtitulo={`${ajustes.n} preguntas${ajustes.penaliza ? " · penaliza el error, como en el examen" : ""}`}
        >
          Empezar ahora
        </AccionPrincipal>

        {porRepasar > 0 && (
          <AccionSecundaria
            icono="🃏"
            onClick={onIrAProgreso}
            subtitulo={`${porRepasar} pregunta${porRepasar === 1 ? "" : "s"} que fallaste y toca revisar`}
          >
            Repasar lo que fallé
          </AccionSecundaria>
        )}

        <AccionSecundaria
          icono="⏱"
          onClick={() => {
            const cfg = { ...ajustes, n: 50, penaliza: true, cronometrado: true, soloRepetidas: true };
            setAjustes(cfg);
            empieza(cfg);
          }}
          subtitulo="50 preguntas · 60 minutos · penaliza el error"
        >
          Simulacro como el examen
        </AccionSecundaria>

        <div className="rounded-2xl border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-900">
          <button
            type="button"
            onClick={() => setVerAjustes((v) => !v)}
            className="flex w-full items-center gap-2 p-4 text-left text-sm font-semibold"
          >
            <span className="flex-1">Cambiar preguntas</span>
            <span className="text-stone-400">{verAjustes ? "−" : "+"}</span>
          </button>
          {verAjustes && (
            <div className="space-y-4 px-4 pb-4">
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">
                  Cuántas
                </p>
                <Segmentado
                  valor={ajustes.n}
                  onChange={(n) => setAjustes({ ...ajustes, n })}
                  opciones={[
                    { valor: 5, etiqueta: "5" },
                    { valor: 10, etiqueta: "10" },
                    { valor: 25, etiqueta: "25" },
                    { valor: 50, etiqueta: "50" },
                  ]}
                />
              </div>
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">
                  De qué tema
                </p>
                <select
                  className="w-full rounded-xl border border-stone-300 bg-white px-3 py-3 text-sm dark:border-stone-700 dark:bg-stone-900"
                  value={ajustes.tema === null ? "" : String(ajustes.tema)}
                  onChange={(e) =>
                    setAjustes({ ...ajustes, tema: e.target.value ? Number(e.target.value) : null })
                  }
                >
                  <option value="">Todos los temas</option>
                  {meta.temas
                    .filter((t) => t.tema !== null)
                    .map((t) => (
                      <option key={String(t.tema)} value={String(t.tema)}>
                        {t.corto} ({t.preguntas})
                      </option>
                    ))}
                </select>
              </div>
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-stone-500">
                  Penalizar errores
                </p>
                <Segmentado
                  valor={ajustes.penaliza ? "si" : "no"}
                  onChange={(v) => setAjustes({ ...ajustes, penaliza: v === "si" })}
                  opciones={[
                    { valor: "si", etiqueta: "Sí (como el examen)" },
                    { valor: "no", etiqueta: "No" },
                  ]}
                />
              </div>
              <label className="flex items-center gap-3 text-sm">
                <input
                  type="checkbox"
                  checked={ajustes.cronometrado}
                  onChange={(e) => setAjustes({ ...ajustes, cronometrado: e.target.checked })}
                  className="h-5 w-5 rounded border-stone-300 text-emerald-600"
                />
                Poner cronómetro
              </label>
              <label className="flex items-center gap-3 text-sm">
                <input
                  type="checkbox"
                  checked={ajustes.soloRepetidas}
                  onChange={(e) => setAjustes({ ...ajustes, soloRepetidas: e.target.checked })}
                  className="h-5 w-5 rounded border-stone-300 text-emerald-600"
                />
                Solo lo que más se repite
              </label>
            </div>
          )}
        </div>

        <ComoFunciona />
      </section>
    );
  }

  // ─────────── jugando ───────────
  if (fase === "jugando") {
    const c = bateria[idx];
    const elegida = respuestas[c.cluster_id] ?? null;
    const respondidas = Object.keys(respuestas).length;
    const min = String(Math.floor(segundos / 60)).padStart(2, "0");
    const seg = String(segundos % 60).padStart(2, "0");
    return (
      <section className="space-y-4">
        <div className="flex items-center justify-between gap-3">
          <span className="text-sm font-semibold">
            {idx + 1} de {bateria.length}
          </span>
          {ajustes.cronometrado && segundos > 0 && (
            <span className="font-mono text-sm font-bold tabular-nums">
              {min}:{seg}
            </span>
          )}
          <Boton tipo="fantasma" onClick={termina}>
            Terminar
          </Boton>
        </div>
        <Barra valor={respondidas} total={bateria.length} />

        <article className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
          <NombreTema cluster={c} />
          <h2 className="mt-3 text-lg font-semibold leading-snug">{c.enunciado}</h2>
          <div className="mt-4 grid gap-2.5">
            {(["A", "B", "C", "D"] as Letra[]).map((l) => (
              <Opcion
                key={l}
                opciones={c.opciones}
                letra={l}
                estado="neutra"
                elegida={elegida}
                onElige={(letra) => setRespuestas({ ...respuestas, [c.cluster_id]: letra })}
              />
            ))}
          </div>
          {elegida && (
            <p className="mt-3 text-center text-xs text-stone-500">
              Puedes cambiar tu respuesta antes de seguir.
            </p>
          )}
        </article>

        <div className="flex gap-2">
          <Boton onClick={() => setIdx((i) => Math.max(0, i - 1))} disabled={idx === 0} ancho>
            ← Atrás
          </Boton>
          {idx < bateria.length - 1 ? (
            <Boton tipo="principal" onClick={() => setIdx((i) => i + 1)} ancho>
              Siguiente →
            </Boton>
          ) : (
            <Boton tipo="principal" onClick={termina} ancho>
              Ver resultado
            </Boton>
          )}
        </div>
      </section>
    );
  }

  // ─────────── resultado ───────────
  return (
    <section className="space-y-4">
      <div className="rounded-2xl border border-stone-200 bg-white p-6 text-center dark:border-stone-800 dark:bg-stone-900">
        <p className="text-xs font-semibold uppercase tracking-wide text-stone-500">Tu nota</p>
        <p className="mt-1 text-5xl font-bold tabular-nums">
          {resultado?.nota ?? 0}
          <span className="text-xl text-stone-400">/10</span>
        </p>
        <p className="mt-2 text-sm text-stone-600 dark:text-stone-300">
          {resultado?.aciertos} bien · {resultado?.fallos} mal · {resultado?.en_blanco} sin contestar
        </p>
        {ajustes.penaliza && (resultado?.fallos ?? 0) > 0 && (
          <p className="mt-1 text-xs text-stone-500">Se descontó ¼ por cada error.</p>
        )}
      </div>

      {(resultado?.fallos ?? 0) > 0 && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-100">
          Has fallado {resultado?.fallos}. Se han guardado en tu lista para repasarlas: vuelven
          solas cuando estés a punto de olvidarlas.{" "}
          <button type="button" onClick={onIrAProgreso} className="font-semibold underline">
            Ir a repasar
          </button>
        </div>
      )}

      <h3 className="text-sm font-bold text-stone-500">Repaso de las preguntas</h3>
      {bateria.map((c, i) => {
        const elegida = respuestas[c.cluster_id] ?? null;
        const bien = elegida === c.correcta;
        return (
          <article
            key={c.cluster_id}
            className={`rounded-2xl border bg-white p-5 dark:bg-stone-900 ${
              bien ? "border-stone-200 dark:border-stone-800" : "border-rose-300 dark:border-rose-900"
            }`}
          >
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs font-bold text-stone-400">{i + 1}</span>
              <NombreTema cluster={c} />
            </div>
            <h3 className="mt-2 text-[15px] font-semibold leading-snug">{c.enunciado}</h3>
            <div className="mt-3 grid gap-2">
              {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                <Opcion
                  key={l}
                  opciones={c.opciones}
                  letra={l}
                  estado={l === c.correcta ? "correcta" : l === elegida ? "fallada" : "neutra"}
                  elegida={elegida}
                />
              ))}
            </div>
            <p className="mt-3 text-xs text-stone-500">
              Ha caído en {c.anios.join(", ")}
              {c.articulos.length > 0 && <> · art. {c.articulos.join(", ")}</>}
            </p>
          </article>
        );
      })}

      <div className="flex gap-2">
        <Boton onClick={() => setFase("inicio")} ancho>
          Volver
        </Boton>
        <Boton tipo="principal" onClick={() => empieza(ajustes)} ancho>
          Otra vez
        </Boton>
      </div>
    </section>
  );
}
