import { useMemo, useState } from "react";
import { ordenaPorScore } from "../data";
import { registraIntento, cargaSm2 } from "../store";
import { vencidas } from "../sm2";
import type { Cluster, ConfigTest, Letra, Meta, ResultadoPregunta } from "../types";
import { AccionPrincipal, AccionSecundaria, Barra, Boton, Chip, NombreTema, Opcion, Segmentado } from "../components/ui";
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
    setSegundos(config.cronometrado ? config.n * 72 : 0);
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

  // ─────────── inicio ───────────
  if (fase === "inicio") {
    return (
      <section className="space-y-5">
        <div>
          <span className="etiqueta">Servicio Andaluz de Salud · 2016–2025</span>
          <h2 className="mt-3 text-[33px] font-medium leading-[1.06] tracking-[-0.035em]">
            ¿Qué hacemos hoy?
          </h2>
          <p className="mt-2 max-w-[38ch] text-sm leading-relaxed text-suave">
            {meta.totales.preguntas} preguntas de los exámenes oficiales, ordenadas por lo que de
            verdad cae cada año.
          </p>
        </div>

        <div className="filete" />

        <AccionPrincipal
          cifra={ajustes.n}
          onClick={() => empieza(ajustes)}
          subtitulo={ajustes.penaliza ? "penaliza el error, como en el examen" : "sin penalizar"}
        >
          Empezar ahora
        </AccionPrincipal>

        {porRepasar > 0 && (
          <AccionSecundaria
            marca={String(porRepasar)}
            onClick={onIrAProgreso}
            subtitulo={`${porRepasar} pregunta${porRepasar === 1 ? "" : "s"} por repasar hoy`}
          >
            Repasar lo que fallé
          </AccionSecundaria>
        )}

        <AccionSecundaria
          marca="⏱"
          onClick={() => {
            const cfg = { ...ajustes, n: 50, penaliza: true, cronometrado: true, soloRepetidas: true };
            setAjustes(cfg);
            empieza(cfg);
          }}
          subtitulo="50 preguntas · 60 minutos · penaliza el error"
        >
          Simulacro como el examen
        </AccionSecundaria>

        <div className="rounded-accion border border-hilo bg-fondo">
          <button
            type="button"
            onClick={() => setVerAjustes((v) => !v)}
            className="flex w-full items-center gap-2 px-4 py-3.5 text-left text-[14.5px] font-semibold"
          >
            <span className="flex-1">Cambiar preguntas</span>
            <span className="font-mono text-suave">{verAjustes ? "−" : "+"}</span>
          </button>
          {verAjustes && (
            <div className="space-y-5 border-t border-hilo px-4 pb-4 pt-4">
              <div>
                <span className="etiqueta">Cuántas</span>
                <div className="mt-2">
                  <Segmentado
                    valor={String(ajustes.n)}
                    onChange={(n) => setAjustes({ ...ajustes, n: Number(n) })}
                    opciones={[
                      { valor: "5", etiqueta: "5" },
                      { valor: "10", etiqueta: "10" },
                      { valor: "25", etiqueta: "25" },
                      { valor: "50", etiqueta: "50" },
                    ]}
                  />
                </div>
              </div>
              <div>
                <span className="etiqueta">De qué tema</span>
                <select
                  className="campo mt-2"
                  value={ajustes.tema === null ? "" : String(ajustes.tema)}
                  onChange={(e) =>
                    setAjustes({ ...ajustes, tema: e.target.value ? Number(e.target.value) : null })
                  }
                >
                  <option value="">Todos los temas</option>
                  {meta.temas
                    .filter((t) => t.tema !== null && t.preguntas > 0)
                    .map((t) => (
                      <option key={String(t.tema)} value={String(t.tema)}>
                        {t.corto} ({t.preguntas})
                      </option>
                    ))}
                </select>
              </div>
              <div>
                <span className="etiqueta">Penalizar errores</span>
                <div className="mt-2">
                  <Segmentado
                    valor={ajustes.penaliza ? "si" : "no"}
                    onChange={(v) => setAjustes({ ...ajustes, penaliza: v === "si" })}
                    opciones={[
                      { valor: "si", etiqueta: "Sí" },
                      { valor: "no", etiqueta: "No" },
                    ]}
                  />
                </div>
              </div>
              <div className="space-y-3 pt-1">
                <label className="flex items-center gap-3 text-sm">
                  <input
                    type="checkbox"
                    checked={ajustes.cronometrado}
                    onChange={(e) => setAjustes({ ...ajustes, cronometrado: e.target.checked })}
                    className="h-4 w-4 rounded border-hilo text-verde accent-[rgb(var(--verde))]"
                  />
                  Poner cronómetro
                </label>
                <label className="flex items-center gap-3 text-sm">
                  <input
                    type="checkbox"
                    checked={ajustes.soloRepetidas}
                    onChange={(e) => setAjustes({ ...ajustes, soloRepetidas: e.target.checked })}
                    className="h-4 w-4 rounded border-hilo text-verde accent-[rgb(var(--verde))]"
                  />
                  Solo lo que más se repite
                </label>
              </div>
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
          <span className="etiqueta">
            {idx + 1} de {bateria.length}
          </span>
          {ajustes.cronometrado && segundos > 0 && (
            <span className="font-mono text-[13px] font-medium tabular-nums text-suave">
              {min}:{seg}
            </span>
          )}
          <Boton tipo="fantasma" onClick={termina}>
            Terminar
          </Boton>
        </div>
        <Barra valor={respondidas} total={bateria.length} />

        <article className="tarjeta p-5">
          <NombreTema cluster={c} />
          <h2 className="mt-3 text-[18px] font-medium leading-snug tracking-tight">{c.enunciado}</h2>
          <div className="mt-4 grid gap-2">
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
            <p className="mt-3 text-center font-mono text-[10px] uppercase tracking-etiqueta text-suave">
              puedes cambiar tu respuesta
            </p>
          )}
        </article>

        <div className="flex gap-2">
          <Boton onClick={() => setIdx((i) => Math.max(0, i - 1))} disabled={idx === 0} ancho>
            Atrás
          </Boton>
          {idx < bateria.length - 1 ? (
            <Boton tipo="uno" onClick={() => setIdx((i) => i + 1)} ancho>
              Siguiente
            </Boton>
          ) : (
            <Boton tipo="uno" onClick={termina} ancho>
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
      <div className="tarjeta px-5 py-8 text-center">
        <span className="etiqueta">Tu nota</span>
        <p className="mt-2 font-mono text-6xl font-medium leading-none tabular-nums text-verde">
          {resultado?.nota ?? 0}
          <span className="text-xl text-suave">/10</span>
        </p>
        <p className="mt-3 font-mono text-[12px] uppercase tracking-wider text-suave">
          {resultado?.aciertos} bien · {resultado?.fallos} mal · {resultado?.en_blanco} en blanco
        </p>
        {ajustes.penaliza && (resultado?.fallos ?? 0) > 0 && (
          <p className="mt-1.5 text-xs text-suave">se descontó ¼ por cada error</p>
        )}
      </div>

      {(resultado?.fallos ?? 0) > 0 && (
        <div className="rounded-accion border border-hilo bg-superficie px-4 py-3.5 text-[13.8px] text-suave">
          Has fallado {resultado?.fallos}. Se han guardado en tu lista: vuelven solas cuando estés
          a punto de olvidarlas.{" "}
          <button type="button" onClick={onIrAProgreso} className="font-semibold text-verde underline">
            Ir a repasar
          </button>
        </div>
      )}

      <span className="etiqueta">Repaso de las preguntas</span>
      {bateria.map((c, i) => {
        const elegida = respuestas[c.cluster_id] ?? null;
        const bien = elegida === c.correcta;
        return (
          <article key={c.cluster_id} className="tarjeta p-5">
            <div className="flex items-center justify-between gap-2">
              <span className="font-mono text-[11px] text-suave">
                {String(i + 1).padStart(2, "0")}
              </span>
              {bien ? <Chip tono="verde">bien</Chip> : <Chip tono="mal">mal</Chip>}
            </div>
            <h3 className="mt-2.5 text-[15.5px] font-medium leading-snug tracking-tight">
              {c.enunciado}
            </h3>
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
            <p className="mt-3 font-mono text-[10px] uppercase tracking-wider text-suave">
              ha caído en {c.anios.join(", ")}
              {c.articulos.length > 0 && <> · art. {c.articulos.join(", ")}</>}
            </p>
          </article>
        );
      })}

      <div className="flex gap-2">
        <Boton onClick={() => setFase("inicio")} ancho>
          Volver
        </Boton>
        <Boton tipo="uno" onClick={() => empieza(ajustes)} ancho>
          Otra vez
        </Boton>
      </div>
    </section>
  );
}
