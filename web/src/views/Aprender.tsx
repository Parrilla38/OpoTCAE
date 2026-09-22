import { useEffect, useMemo, useState } from "react";
import { agrupaPorArticulo, cargaConceptos, cohesion, porTema } from "../data";
import type { Cluster, Concepto, ConceptosData, Letra, Meta } from "../types";
import { AccionSecundaria, Boton, Etiqueta, Fila, NombreTema, Segmentado } from "../components/ui";

type Pestana = "temas" | "conceptos" | "calendario";
type Vista =
  | { tipo: "lista" }
  | { tipo: "apartados"; tema: number }
  | { tipo: "preguntas"; tema: number; apartado: number };

export default function Aprender({
  clusters,
  meta,
}: {
  clusters: Cluster[];
  meta: Meta;
}) {
  const [pestana, setPestana] = useState<Pestana>("temas");
  const [vista, setVista] = useState<Vista>({ tipo: "lista" });
  const [abierto, setAbierto] = useState<number | null>(null);

  // los conceptos por embeddings (~250 KB) solo se piden al abrir esa pestaña
  const [conceptos, setConceptos] = useState<ConceptosData | null>(null);
  useEffect(() => {
    if (pestana !== "conceptos" || conceptos) return;
    cargaConceptos().then(setConceptos).catch(() => setConceptos(null));
  }, [pestana, conceptos]);

  const temas = useMemo(() => [...meta.temas].sort((a, b) => b.preguntas - a.preguntas), [meta.temas]);

  const apartados = useMemo(() => {
    if (vista.tipo !== "apartados") return new Map<number, Cluster[]>();
    const cs = porTema(clusters, vista.tema);
    const m = agrupaPorArticulo(cs);
    return new Map(
      [...m.entries()].sort(
        (a, b) => b[1].reduce((s, c) => s + c.score, 0) - a[1].reduce((s, c) => s + c.score, 0)
      )
    );
  }, [clusters, vista]);

  const preguntas = useMemo(() => {
    if (vista.tipo !== "preguntas") return [];
    const cs = porTema(clusters, vista.tema);
    if (vista.apartado === 0) return cs.filter((c) => !c.articulos.length);
    return cs.filter((c) => c.articulos.includes(vista.apartado));
  }, [clusters, vista]);

  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Lo que más se pregunta</h2>
        <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">
          Ordenado por lo que de verdad cae en los exámenes, no por el orden del temario.
        </p>
      </div>

      <Segmentado
        valor={pestana}
        onChange={(p) => {
          setPestana(p as Pestana);
          setVista({ tipo: "lista" });
        }}
        opciones={[
          { valor: "temas" as Pestana, etiqueta: "Por tema" },
          { valor: "conceptos" as Pestana, etiqueta: "Conceptos" },
          { valor: "calendario" as Pestana, etiqueta: "Calendario" },
        ]}
      />

      {pestana === "calendario" && (
        <Calendario
          clusters={clusters}
          meta={meta}
          onAbre={(tema, art) => {
            setPestana("temas");
            setVista({ tipo: "preguntas", tema, apartado: art });
          }}
        />
      )}

      {pestana === "conceptos" && (
        <Conceptos conceptos={conceptos} abierto={abierto} setAbierto={setAbierto} />
      )}

      {pestana === "temas" && vista.tipo === "lista" && (
        <ol className="space-y-2">
          {temas.map((t, i) => {
            const id = t.tema;
            const sinPreguntas = t.preguntas === 0;
            return (
              <li key={t.tema ?? t.corto} className={sinPreguntas ? "opacity-55" : undefined}>
                <Fila
                  titulo={t.corto}
                  detalle={
                    sinPreguntas
                      ? "Prácticamente no cae · apenas aparece en los exámenes"
                      : `${t.preguntas} preguntas${id !== null && id <= 10 ? " · bloque común" : ""}`
                  }
                  onClick={() => {
                    if (sinPreguntas) return;
                    if (id === null) {
                      setVista({ tipo: "preguntas", tema: -1, apartado: 0 });
                    } else if (id <= 10) {
                      setVista({ tipo: "apartados", tema: id });
                    } else {
                      setVista({ tipo: "preguntas", tema: id, apartado: 0 });
                    }
                  }}
                  derecha={
                    <span className="text-sm font-bold tabular-nums text-stone-400">{i + 1}</span>
                  }
                />
              </li>
            );
          })}
          {conceptos && conceptos.n_multi_anio > 0 && (
            <li className="pt-2">
              <AccionSecundaria
                icono="🔁"
                onClick={() => setPestana("conceptos")}
                subtitulo={`${conceptos.n_multi_anio} preguntas que se repiten con otras palabras`}
              >
                Ver lo que se repite con otras palabras
              </AccionSecundaria>
            </li>
          )}
        </ol>
      )}

      {pestana === "temas" && vista.tipo === "apartados" && (
        <ol className="space-y-2">
          <div className="flex items-center gap-2">
            <Boton tipo="fantasma" onClick={() => setVista({ tipo: "lista" })}>
              ← Temas
            </Boton>
            <span className="text-sm font-bold">
              {meta.temas.find((t) => t.tema === vista.tema)?.corto}
            </span>
          </div>
          {[...apartados.entries()]
            .filter(([art]) => art !== 0)
            .map(([art, cs], i) => (
              <li key={art}>
                <Fila
                  titulo={`Artículo ${art}`}
                  detalle={`${cs.length} pregunta${cs.length === 1 ? "" : "s"} · ha caído en ${[
                    ...new Set(cs.flatMap((c) => c.anios)),
                  ]
                    .sort()
                    .join(", ")}`}
                  onClick={() => setVista({ tipo: "preguntas", tema: vista.tema, apartado: art })}
                  derecha={<span className="text-sm font-bold tabular-nums text-stone-400">{i + 1}</span>}
                />
              </li>
            ))}
          {[...apartados.entries()].some(([art]) => art === 0) && (
            <li>
              <Fila
                titulo="Preguntas sin artículo concreto"
                detalle="Definiciones y conceptos generales del tema"
                onClick={() => setVista({ tipo: "preguntas", tema: vista.tema, apartado: 0 })}
              />
            </li>
          )}
        </ol>
      )}

      {pestana === "temas" && vista.tipo === "preguntas" && (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Boton
              tipo="fantasma"
              onClick={() =>
                setVista(
                  vista.tema > 0 && vista.tema <= 10
                    ? { tipo: "apartados", tema: vista.tema }
                    : { tipo: "lista" }
                )
              }
            >
              ← Atrás
            </Boton>
            <span className="text-sm font-bold">
              {vista.apartado === 0
                ? meta.temas.find((t) => t.tema === vista.tema)?.corto
                : `Artículo ${vista.apartado}`}
            </span>
          </div>
          <p className="text-sm text-stone-500">
            {preguntas.length} pregunta{preguntas.length === 1 ? "" : "s"} ordenadas por lo que más
            se repiten.
          </p>
          {preguntas.map((c) => (
            <TarjetaPregunta key={c.cluster_id} c={c} />
          ))}
        </div>
      )}
    </section>
  );
}

function TarjetaPregunta({ c }: { c: Cluster }) {
  return (
    <article className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
      <NombreTema cluster={c} />
      <h3 className="mt-2 text-[15px] font-semibold leading-snug">{c.enunciado}</h3>
      <div className="mt-3 grid gap-1.5 text-sm">
        {(["A", "B", "C", "D"] as Letra[]).map((l) => (
          <p
            key={l}
            className={
              l === c.correcta ? "font-semibold text-emerald-700 dark:text-emerald-400" : "text-stone-600 dark:text-stone-300"
            }
          >
            <span className="font-bold">{l})</span> {c.opciones[l]}
            {l === c.correcta && " ✓"}
          </p>
        ))}
      </div>
      <p className="mt-3 text-xs text-stone-500">
        Ha caído en {c.anios.join(", ")} ({c.frecuencia} vez/veces)
        {c.articulos.length > 0 && <> · art. {c.articulos.join(", ")}</>}
      </p>
    </article>
  );
}

function Conceptos({
  conceptos,
  abierto,
  setAbierto,
}: {
  conceptos: ConceptosData | null;
  abierto: number | null;
  setAbierto: (n: number | null) => void;
}) {
  if (!conceptos || !conceptos.conceptos.length) {
    return (
      <div className="rounded-2xl border border-stone-200 bg-white p-5 text-sm text-stone-500 dark:border-stone-800 dark:bg-stone-900">
        No hay datos de conceptos en esta versión.
      </div>
    );
  }
  return (
    <div className="space-y-3">
      <div className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
        <p className="text-sm leading-relaxed text-stone-600 dark:text-stone-300">
          El tribunal casi nunca repite la misma pregunta. Lo que hace es preguntar{" "}
          <b>lo mismo con otras palabras</b>. Aquí están esos casos:{" "}
          <b>{conceptos.n_multi_anio} preguntas que se repiten</b> a lo largo de{" "}
          {new Set(conceptos.conceptos.flatMap((c) => c.anios)).size} años.
        </p>
      </div>
      {conceptos.conceptos.map((c) => (
        <TarjetaConcepto
          key={c.concepto_id}
          c={c}
          abierto={abierto === c.concepto_id}
          toggle={() => setAbierto(abierto === c.concepto_id ? null : c.concepto_id)}
        />
      ))}
    </div>
  );
}

function TarjetaConcepto({ c, abierto, toggle }: { c: Concepto; abierto: boolean; toggle: () => void }) {
  const coh = cohesion(c.similitud_media);
  const etiquetaCoh =
    coh === "alta"
      ? "Casi la misma pregunta"
      : coh === "media"
        ? "Mismo concepto, otro enfoque"
        : "Mismo tema, preguntas distintas";
  return (
    <article className="rounded-2xl border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-900">
      <button type="button" onClick={toggle} className="w-full p-5 text-left">
        <div className="flex flex-wrap items-center gap-2">
          <Etiqueta tono="verde">Ha caído en {c.anios.join(", ")}</Etiqueta>
          <Etiqueta tono="ambar">{etiquetaCoh}</Etiqueta>
        </div>
        <h3 className="mt-3 text-[15px] font-semibold leading-snug">{c.representante}</h3>
        <p className="mt-1.5 text-xs text-stone-500">
          Formulada de {c.n_preguntas} formas distintas
          {c.temas.length > 0 && (
            <> · {c.temas.map((t) => `T${String(t).padStart(2, "0")}`).join(", ")}</>
          )}
        </p>
      </button>
      {abierto && (
        <ul className="space-y-3 border-t border-stone-200 px-5 pb-5 pt-4 dark:border-stone-800">
          {c.miembros.map((m) => (
            <li key={m.id} className="rounded-xl bg-stone-50 p-3 text-sm dark:bg-stone-800/50">
              <Etiqueta>{`${m.anio} · ${m.modalidad}`}</Etiqueta>
              <p className="mt-2 leading-snug">{m.enunciado}</p>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}

/** Calendario artículo × año. Cuántas veces cae cada apartado en cada convocatoria. */
function Calendario({
  clusters,
  meta,
  onAbre,
}: {
  clusters: Cluster[];
  meta: Meta;
  onAbre: (tema: number, articulo: number) => void;
}) {
  const anios = meta.anios;
  const filas = useMemo(() => {
    const m = new Map<string, { tema: number; art: number; porAnio: Map<number, number>; total: number }>();
    for (const c of clusters) {
      const arts = c.articulos.length ? c.articulos : [0];
      for (const a of arts) {
        const k = `${c.tema ?? 0}:${a}`;
        const d = m.get(k) ?? { tema: c.tema ?? 0, art: a, porAnio: new Map<number, number>(), total: 0 };
        for (const anio of c.anios) {
          d.porAnio.set(anio, (d.porAnio.get(anio) ?? 0) + 1);
          d.total += 1;
        }
        m.set(k, d);
      }
    }
    return [...m.values()].sort((a, b) => b.total - a.total);
  }, [clusters]);

  const max = Math.max(1, ...filas.map((f) => f.total));

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-stone-200 bg-white p-5 dark:border-stone-800 dark:bg-stone-900">
        <p className="text-sm leading-relaxed text-stone-600 dark:text-stone-300">
          Qué artículos caen en cada convocatoria. <b>Más verde = más veces</b>. Toca una fila para
          ver las preguntas de ese artículo.
        </p>
      </div>
      <div className="overflow-x-auto rounded-2xl border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <table className="w-full border-collapse text-xs">
          <thead>
            <tr>
              <th className="sticky left-0 bg-white px-2 py-2 text-left dark:bg-stone-900">Artículo</th>
              {anios.map((a) => (
                <th key={a} className="px-2 py-2 text-center font-semibold">
                  {a}
                </th>
              ))}
              <th className="px-2 py-2 text-center font-semibold">Total</th>
            </tr>
          </thead>
          <tbody>
            {filas.slice(0, 30).map((f) => (
              <tr key={`${f.tema}:${f.art}`} className="border-t border-stone-100 dark:border-stone-800">
                <td className="sticky left-0 bg-white px-2 py-2 dark:bg-stone-900">
                  <button
                    type="button"
                    onClick={() => onAbre(f.tema, f.art)}
                    className="text-left underline decoration-dotted underline-offset-2 hover:text-emerald-700"
                  >
                    {f.art === 0
                      ? meta.temas.find((t) => t.tema === f.tema)?.corto ?? "Sin artículo"
                      : `Art. ${f.art}`}
                  </button>
                </td>
                {anios.map((a) => {
                  const n = f.porAnio.get(a) ?? 0;
                  const op = n === 0 ? 0 : 0.18 + (n / max) * 0.82;
                  return (
                    <td key={a} className="px-1 py-1 text-center">
                      <span
                        className="inline-flex h-7 w-9 items-center justify-center rounded font-bold tabular-nums"
                        style={{
                          background: n ? `rgba(5, 150, 105, ${op})` : "transparent",
                          color: n && op > 0.55 ? "#fff" : undefined,
                        }}
                      >
                        {n || "·"}
                      </span>
                    </td>
                  );
                })}
                <td className="px-2 py-2 text-center font-bold tabular-nums">{f.total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
