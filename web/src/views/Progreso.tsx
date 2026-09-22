import { useEffect, useMemo, useState } from "react";
import {
  cargaProgreso,
  cargaSm2,
  altaTarjeta,
  reiniciaProgreso,
  reiniciaTarjeta,
  repasaTarjeta,
  resumenProgreso,
} from "../store";
import { enDias, vencidas, proximas } from "../sm2";
import type { Cluster, Letra, Meta } from "../types";
import { AccionSecundaria, Boton, ListaOpciones, NombreTema, Opcion, Segmentado } from "../components/ui";

type Pestana = "repasar" | "mis" | "estadisticas";

const BOTONES = [
  { q: 1, t: "No la sé", d: "hoy" },
  { q: 3, t: "Casi", d: "1 día" },
  { q: 4, t: "Bien", d: "3 días" },
  { q: 5, t: "Fácil", d: "más" },
];

export default function Progreso({ clusters, meta }: { clusters: Cluster[]; meta: Meta }) {
  const [pestana, setPestana] = useState<Pestana>("repasar");
  const [, rerender] = useState(0);
  const porId = useMemo(() => new Map(clusters.map((c) => [c.cluster_id, c])), [clusters]);

  const [cola, setCola] = useState<number[]>([]);
  const [revelada, setRevelada] = useState(false);
  const [idxMis, setIdxMis] = useState(0);
  const [reveladaMis, setReveladaMis] = useState(false);

  useEffect(() => {
    if (pestana === "repasar") {
      setCola(vencidas(cargaSm2()).map((t) => t.id));
      setRevelada(false);
    }
  }, [pestana]);

  function responde(q: number) {
    if (!cola.length) return;
    repasaTarjeta(cola[0], q);
    setCola((c) => c.slice(1));
    setRevelada(false);
    rerender((n) => n + 1);
  }

  const ts = cargaSm2();
  const todas = Object.values(ts).sort((a, b) => a.proximo - b.proximo);
  const resumen = resumenProgreso();

  return (
    <section className="space-y-5">
      <div>
        <span className="etiqueta">Tu progreso</span>
        <h2 className="mt-3 text-[33px] font-medium leading-[1.06] tracking-[-0.035em]">Mi progreso</h2>
        <p className="mt-2 max-w-[38ch] text-sm leading-relaxed text-suave">
          Se guarda solo en este navegador. Sin cuenta y sin contraseña.
        </p>
      </div>

      <Segmentado
        valor={pestana}
        onChange={(p) => setPestana(p as Pestana)}
        opciones={[
          {
            valor: "repasar" as Pestana,
            etiqueta: cola.length > 0 ? `Hoy · ${cola.length}` : "Hoy",
          },
          {
            valor: "mis" as Pestana,
            etiqueta: todas.length ? `Tarjetas · ${todas.length}` : "Tarjetas",
          },
          { valor: "estadisticas" as Pestana, etiqueta: "Datos" },
        ]}
      />

      {pestana === "repasar" && (
        <div className="space-y-4">
          {todas.length === 0 && (
            <div className="tarjeta px-5 py-8 text-center text-sm text-suave">
              Todavía no tienes preguntas pendientes. Se guardan solas cuando fallas en un test.
            </div>
          )}
          {todas.length > 0 && cola.length === 0 && (
            <div className="tarjeta px-5 py-8 text-center">
              <p className="text-2xl">✓</p>
              <p className="mt-2 text-[15.5px] font-semibold tracking-tight">
                Repaso de hoy terminado
              </p>
              <p className="mt-1 text-sm text-suave">
                {proximas(ts).length > 0
                  ? `La próxima vuelve ${enDias(proximas(ts)[0].proximo)}.`
                  : "No hay más repasos programados."}
              </p>
            </div>
          )}
          {cola.length > 0 && porId.get(cola[0]) && (
            <RepasoCard
              c={porId.get(cola[0])!}
              revelada={revelada}
              setRevelada={setRevelada}
              nRestantes={cola.length}
              onResponde={responde}
            />
          )}
        </div>
      )}

      {pestana === "mis" && (
        <div className="space-y-4">
          {todas.length === 0 ? (
            <div className="tarjeta px-5 py-8 text-center text-sm text-suave">
              Aún no has guardado ninguna tarjeta.
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between gap-2">
                <Boton
                  onClick={() => {
                    setIdxMis((i) => Math.max(0, i - 1));
                    setReveladaMis(false);
                  }}
                  disabled={idxMis === 0}
                >
                  Atrás
                </Boton>
                <span className="font-mono text-[12px] tabular-nums text-suave">
                  {idxMis + 1} de {todas.length}
                </span>
                <Boton
                  onClick={() => {
                    setIdxMis((i) => Math.min(todas.length - 1, i + 1));
                    setReveladaMis(false);
                  }}
                  disabled={idxMis >= todas.length - 1}
                >
                  Siguiente
                </Boton>
              </div>
              {(() => {
                const t = todas[idxMis];
                const c = porId.get(t.id);
                if (!c) return null;
                return (
                  <article className="tarjeta p-5">
                    <NombreTema cluster={c} />
                    <h3 className="mt-3 text-[16px] font-medium leading-snug tracking-tight">
                      {c.enunciado}
                    </h3>
                    {reveladaMis ? (
                      <ListaOpciones opciones={c.opciones} correcta={c.correcta} />
                    ) : (
                      <p className="mt-3 text-sm text-suave">
                        Piensa la respuesta y luego revélala.
                      </p>
                    )}
                    <div className="mt-4 flex flex-wrap gap-2">
                      {!reveladaMis ? (
                        <Boton tipo="uno" onClick={() => setReveladaMis(true)} ancho>
                          Ver respuesta
                        </Boton>
                      ) : (
                        <>
                          <Boton
                            onClick={() => {
                              altaTarjeta(c.cluster_id);
                              reiniciaTarjeta(c.cluster_id);
                              rerender((n) => n + 1);
                            }}
                          >
                            Dejar para hoy
                          </Boton>
                          <Boton
                            onClick={() => {
                              if (confirm("¿Quitar esta tarjeta de tu lista?")) {
                                reiniciaTarjeta(c.cluster_id);
                                const nts = cargaSm2();
                                delete nts[c.cluster_id];
                                localStorage.setItem("opotcae-sm2-v1", JSON.stringify(nts));
                                setIdxMis((i) =>
                                  Math.max(0, Math.min(i, Object.keys(cargaSm2()).length - 1))
                                );
                                rerender((n) => n + 1);
                              }
                            }}
                          >
                            Quitarla
                          </Boton>
                        </>
                      )}
                    </div>
                  </article>
                );
              })()}
            </>
          )}
        </div>
      )}

      {pestana === "estadisticas" && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {[
              { t: "Tests", v: resumen.intentos, tono: "text-cobalto" },
              { t: "Bien", v: resumen.aciertos, tono: "text-verde" },
              { t: "Mal", v: resumen.fallos, tono: "text-mal" },
              { t: "Nota media", v: resumen.notaMedia, tono: "text-albero" },
            ].map((s) => (
              <div key={s.t} className="tarjeta px-3 py-4 text-center">
                <div className={`font-mono text-2xl font-bold tabular-nums ${s.tono}`}>{s.v}</div>
                <div className="etiqueta mt-1">{s.t}</div>
              </div>
            ))}
          </div>

          <div className="tarjeta p-5">
            <span className="etiqueta">Cómo vas en cada tema</span>
            <p className="mt-2 text-sm text-suave">
              Porcentaje de aciertos sobre lo que has respondido.
            </p>
            <ul className="mt-4 space-y-3.5">
              {meta.temas
                .filter((t) => t.preguntas > 0)
                .map((t) => {
                  const progreso = cargaProgreso();
                  let bien = 0;
                  let mal = 0;
                  for (const c of clusters) {
                    if (c.tema !== t.tema) continue;
                    bien += progreso.aciertos[c.cluster_id] ?? 0;
                    mal += progreso.errores[c.cluster_id] ?? 0;
                  }
                  const total = bien + mal;
                  const pct = total ? Math.round((bien / total) * 100) : null;
                  return (
                    <li key={t.tema ?? t.corto}>
                      <div className="mb-1.5 flex items-baseline justify-between gap-2">
                        <span className="text-[13.8px]">{t.corto}</span>
                        <span className="font-mono text-[11px] font-bold tabular-nums text-suave">
                          {total === 0 ? "sin datos" : `${pct}%`}
                        </span>
                      </div>
                      <div className="h-1.5 w-full overflow-hidden rounded-full bg-aguaverde">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{
                            width: `${pct ?? 0}%`,
                            background:
                              pct === null
                                ? "transparent"
                                : pct >= 70
                                  ? "rgb(var(--verde))"
                                  : pct >= 40
                                    ? "rgb(var(--albero))"
                                    : "rgb(var(--mal))",
                          }}
                        />
                      </div>
                    </li>
                  );
                })}
            </ul>
          </div>

          <div className="grid gap-2 sm:grid-cols-2">
            <AccionSecundaria
              marca="↓"
              onClick={() => exporta(clusters, meta)}
              subtitulo="resumen en texto, para leer o imprimir"
            >
              Descargar resumen
            </AccionSecundaria>
            <AccionSecundaria
              marca="⎙"
              onClick={() => window.print()}
              subtitulo="imprime esta pantalla"
            >
              Imprimir
            </AccionSecundaria>
          </div>

          <Boton
            ancho
            onClick={() => {
              if (confirm("¿Borrar todo? Tests, tarjetas y estadísticas.")) {
                reiniciaProgreso();
                rerender((n) => n + 1);
              }
            }}
          >
            Borrar todo mi progreso
          </Boton>
        </div>
      )}
    </section>
  );
}

function RepasoCard({
  c,
  revelada,
  setRevelada,
  nRestantes,
  onResponde,
}: {
  c: Cluster;
  revelada: boolean;
  setRevelada: (v: boolean) => void;
  nRestantes: number;
  onResponde: (q: number) => void;
}) {
  return (
    <>
      <span className="etiqueta">
        {nRestantes} pregunta{nRestantes === 1 ? "" : "s"} por repasar
      </span>
      <article className="tarjeta p-5">
        <NombreTema cluster={c} />
        <h3 className="mt-3 text-[18px] font-medium leading-snug tracking-tight">{c.enunciado}</h3>
        {revelada ? (
          <div className="mt-4 grid gap-2">
            {(["A", "B", "C", "D"] as Letra[]).map((l) => (
              <Opcion key={l} opciones={c.opciones} letra={l} estado={l === c.correcta ? "correcta" : "neutra"} />
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm text-suave">Piensa la respuesta y luego revélala.</p>
        )}
      </article>
      {!revelada ? (
        <Boton tipo="uno" onClick={() => setRevelada(true)} ancho>
          Ver respuesta
        </Boton>
      ) : (
        <div className="grid grid-cols-4 gap-2">
          {BOTONES.map((b) => (
            <button
              key={b.q}
              type="button"
              onClick={() => onResponde(b.q)}
              className="flex flex-col items-center rounded-accion border border-hilo bg-fondo py-3 transition hover:bg-superficie"
            >
              <span className="text-[13.5px] font-semibold tracking-tight">{b.t}</span>
              <span className="mt-0.5 font-mono text-[10px] uppercase tracking-wider text-suave">
                {b.d}
              </span>
            </button>
          ))}
        </div>
      )}
    </>
  );
}

function exporta(clusters: Cluster[], meta: Meta) {
  const p = cargaProgreso();
  const fallados = Object.entries(p.errores)
    .filter(([, n]) => (n as number) > 0)
    .map(([k, n]) => ({ id: Number(k), veces: n as number }))
    .sort((a, b) => b.veces - a.veces);
  const porId = new Map(clusters.map((c) => [c.cluster_id, c]));

  const L: string[] = ["# Mi repaso OpoTCAE", ""];
  L.push(`_Exportado el ${new Date().toLocaleString("es-ES")}_`, "", "## Lo que fallé", "");
  if (!fallados.length) L.push("_Aún no hay errores._", "");
  for (const { id, veces } of fallados) {
    const c = porId.get(id);
    if (!c) continue;
    L.push(`### [${veces} fallo${veces === 1 ? "" : "s"}] ${c.enunciado}`, "");
    for (const l of ["A", "B", "C", "D"] as const) {
      L.push(`- ${l}${l === c.correcta ? " ✓" : ""}) ${c.opciones[l]}`);
    }
    L.push("", `_${c.tema_corto ?? c.tema_nombre} · cae en ${c.anios.join(", ")}_`, "");
  }
  L.push("## Lo que más se repite", "", "| Años | Tema | Pregunta |", "|---|---|---|");
  for (const c of [...clusters].sort((a, b) => b.score - a.score).slice(0, 40)) {
    L.push(
      `| ${c.anios.join(", ")} | ${c.tema_corto ?? "—"} | ${c.enunciado.replace(/\|/g, "/").slice(0, 90)} |`
    );
  }
  L.push("", `---`, "", `_Fuente: ${meta.fuente}_`, "");

  const blob = new Blob([L.join("\n")], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `opotcae-repaso-${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
}
