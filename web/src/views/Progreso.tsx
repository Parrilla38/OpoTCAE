import { useEffect, useMemo, useState } from "react";
import { cargaProgreso, cargaSm2, altaTarjeta, reiniciaProgreso, reiniciaTarjeta, repasaTarjeta, resumenProgreso } from "../store";
import { enDias, vencidas, proximas } from "../sm2";
import type { Cluster, Letra, Meta } from "../types";
import { AccionSecundaria, Boton, NombreTema, Opcion, Segmentado } from "../components/ui";

type Pestana = "repasar" | "mis" | "estadisticas";

const BOTONES = [
  { q: 1, t: "No la sé", d: "hoy", c: "border-rose-300 text-rose-700 hover:bg-rose-50 dark:border-rose-900 dark:hover:bg-rose-950/40" },
  { q: 3, t: "Casi", d: "1 día", c: "border-amber-300 text-amber-700 hover:bg-amber-50 dark:border-amber-900 dark:hover:bg-amber-950/40" },
  { q: 4, t: "Bien", d: "3 días", c: "border-emerald-300 text-emerald-700 hover:bg-emerald-50 dark:border-emerald-900 dark:hover:bg-emerald-950/40" },
  { q: 5, t: "Fácil", d: "más", c: "border-sky-300 text-sky-700 hover:bg-sky-50 dark:border-sky-900 dark:hover:bg-sky-950/40" },
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
    <section className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Mi progreso</h2>
        <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">
          Se guarda solo en este navegador. Sin cuenta y sin contraseña.
        </p>
      </div>

      <Segmentado
        valor={pestana}
        onChange={(p) => setPestana(p as Pestana)}
        opciones={[
          { valor: "repasar" as Pestana, etiqueta: cola.length > 0 ? `Hoy (${cola.length})` : "Hoy" },
          { valor: "mis" as Pestana, etiqueta: `Mis tarjetas${todas.length ? ` (${todas.length})` : ""}` },
          { valor: "estadisticas" as Pestana, etiqueta: "Datos" },
        ]}
      />

      {pestana === "repasar" && (
        <div className="space-y-4">
          {todas.length === 0 && (
            <div className="rounded-2xl border border-stone-200 bg-white p-6 text-center dark:border-stone-800 dark:bg-stone-900">
              <p className="text-sm text-stone-500">
                Todavía no tienes preguntas pendientes. Se guardan solas cuando fallas en un test.
              </p>
            </div>
          )}
          {todas.length > 0 && cola.length === 0 && (
            <div className="rounded-2xl border border-stone-200 bg-white p-6 text-center dark:border-stone-800 dark:bg-stone-900">
              <p className="text-3xl">🎉</p>
              <p className="mt-2 text-[15px] font-semibold">Repaso de hoy terminado</p>
              <p className="mt-1 text-sm text-stone-500">
                {proximas(ts).length > 0
                  ? `La próxima vuelve ${enDias(proximas(ts)[0].proximo)}.`
                  : "No hay más repasos programados."}
              </p>
            </div>
          )}
          {cola.length > 0 && porId.get(cola[0]) && <RepasoCard c={porId.get(cola[0])!} revelada={revelada} setRevelada={setRevelada} nRestantes={cola.length} onResponde={responde} />}
        </div>
      )}

      {pestana === "mis" && (
        <div className="space-y-4">
          {todas.length === 0 ? (
            <div className="rounded-2xl border border-stone-200 bg-white p-6 text-center dark:border-stone-800 dark:bg-stone-900">
              <p className="text-sm text-stone-500">Aún no has guardado ninguna tarjeta.</p>
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
                  ←
                </Boton>
                <span className="text-sm font-semibold tabular-nums">
                  {idxMis + 1} de {todas.length}
                </span>
                <Boton
                  onClick={() => {
                    setIdxMis((i) => Math.min(todas.length - 1, i + 1));
                    setReveladaMis(false);
                  }}
                  disabled={idxMis >= todas.length - 1}
                >
                  →
                </Boton>
              </div>
              {(() => {
                const t = todas[idxMis];
                const c = porId.get(t.id);
                if (!c) return null;
                return (
                  <article className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
                    <NombreTema cluster={c} />
                    <h3 className="mt-3 text-[15px] font-semibold leading-snug">{c.enunciado}</h3>
                    {reveladaMis ? (
                      <div className="mt-3 grid gap-1.5 text-sm">
                        {(["A", "B", "C", "D"] as Letra[]).map((l) => (
                          <p
                            key={l}
                            className={
                              l === c.correcta
                                ? "font-semibold text-emerald-700 dark:text-emerald-400"
                                : "text-stone-600 dark:text-stone-300"
                            }
                          >
                            <span className="font-bold">{l})</span> {c.opciones[l]}
                            {l === c.correcta && " ✓"}
                          </p>
                        ))}
                      </div>
                    ) : (
                      <p className="mt-3 text-sm text-stone-500">Piensa la respuesta y luego revélala.</p>
                    )}
                    <div className="mt-4 flex flex-wrap gap-2">
                      {!reveladaMis ? (
                        <Boton tipo="principal" onClick={() => setReveladaMis(true)} ancho>
                          Ver respuesta
                        </Boton>
                      ) : (
                        <>
                          <Boton
                            tipo="secundario"
                            onClick={() => {
                              altaTarjeta(c.cluster_id);
                              reiniciaTarjeta(c.cluster_id);
                              rerender((n) => n + 1);
                            }}
                          >
                            Dejar para hoy
                          </Boton>
                          <Boton
                            tipo="secundario"
                            onClick={() => {
                              if (confirm("¿Quitar esta tarjeta de tu lista?")) {
                                reiniciaTarjeta(c.cluster_id);
                                const nts = cargaSm2();
                                delete nts[c.cluster_id];
                                localStorage.setItem("tcae-sm2-v1", JSON.stringify(nts));
                                setIdxMis((i) => Math.max(0, Math.min(i, Object.keys(cargaSm2()).length - 1)));
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
              { t: "Tests", v: resumen.intentos },
              { t: "Bien", v: resumen.aciertos },
              { t: "Mal", v: resumen.fallos },
              { t: "Nota media", v: resumen.notaMedia },
            ].map((s) => (
              <div key={s.t} className="rounded-2xl border border-stone-200 bg-white p-4 text-center dark:border-stone-800 dark:bg-stone-900">
                <div className="text-2xl font-bold tabular-nums">{s.v}</div>
                <div className="text-xs uppercase tracking-wide text-stone-500">{s.t}</div>
              </div>
            ))}
          </div>

          <div className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
            <h3 className="text-sm font-bold">Cómo vas en cada tema</h3>
            <p className="mb-3 text-xs text-stone-500">Porcentaje de aciertos sobre lo que has respondido.</p>
            <ul className="space-y-3">
              {meta.temas.map((t) => {
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
                    <div className="mb-1 flex items-baseline justify-between gap-2">
                      <span className="text-sm">{t.corto}</span>
                      <span className="text-xs tabular-nums text-stone-500">
                        {total === 0 ? "sin datos" : `${pct}%`}
                      </span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-stone-200 dark:bg-stone-800">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${pct ?? 0}%`,
                          background: pct === null ? "transparent" : pct >= 70 ? "#059669" : pct >= 40 ? "#d97706" : "#e11d48",
                        }}
                      />
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          <AccionSecundaria
            icono="⬇"
            onClick={() => exporta(clusters, meta)}
            subtitulo="Resumen con tus errores y lo que más se repite, para repasar en papel"
          >
            Descargar resumen
          </AccionSecundaria>

          <Boton
            ancho
            tipo="secundario"
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
      <p className="text-sm text-stone-500">
        {nRestantes} pregunta{nRestantes === 1 ? "" : "s"} por repasar
      </p>
      <article className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
        <NombreTema cluster={c} />
        <h3 className="mt-3 text-lg font-semibold leading-snug">{c.enunciado}</h3>
        {revelada ? (
          <div className="mt-4 grid gap-2">
            {(["A", "B", "C", "D"] as Letra[]).map((l) => (
              <Opcion key={l} opciones={c.opciones} letra={l} estado={l === c.correcta ? "correcta" : "neutra"} />
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm text-stone-500">Piensa la respuesta y luego revélala.</p>
        )}
      </article>
      {!revelada ? (
        <Boton tipo="principal" onClick={() => setRevelada(true)} ancho>
          Ver respuesta
        </Boton>
      ) : (
        <div className="grid grid-cols-4 gap-2">
          {BOTONES.map((b) => (
            <button
              key={b.q}
              type="button"
              onClick={() => onResponde(b.q)}
              className={`flex flex-col items-center rounded-xl border bg-white py-3 dark:bg-stone-900 ${b.c}`}
            >
              <span className="text-sm font-bold">{b.t}</span>
              <span className="text-[10px] opacity-70">{b.d}</span>
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

  const L: string[] = ["# Mi repaso TCAE", ""];
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
    L.push(`| ${c.anios.join(", ")} | ${c.tema_corto ?? "—"} | ${c.enunciado.replace(/\|/g, "/").slice(0, 90)} |`);
  }
  L.push("", `---`, "", `_Fuente: ${meta.fuente}_`, "");

  const blob = new Blob([L.join("\n")], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `repaso-tcae-${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
}
