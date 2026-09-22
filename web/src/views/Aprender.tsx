import { useEffect, useMemo, useState } from "react";
import { agrupaPorArticulo, cargaConceptos, cohesion, porTema } from "../data";
import type { Cluster, Concepto, ConceptosData, Meta, Selector } from "../types";
import { Boton, Chip, Fila, ListaOpciones, NombreTema, Segmentado } from "../components/ui";

type Pestana = "temas" | "conceptos" | "calendario";
type Vista =
  | { tipo: "lista" }
  | { tipo: "apartados"; sel: Selector }
  | { tipo: "preguntas"; sel: Selector; apartado: number };

export default function Aprender({ clusters, meta }: { clusters: Cluster[]; meta: Meta }) {
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
    const cs = porTema(clusters, vista.sel);
    const m = agrupaPorArticulo(cs);
    return new Map(
      [...m.entries()].sort(
        (a, b) => b[1].reduce((s, c) => s + c.score, 0) - a[1].reduce((s, c) => s + c.score, 0)
      )
    );
  }, [clusters, vista]);

  const preguntas = useMemo(() => {
    if (vista.tipo !== "preguntas") return [];
    const cs = porTema(clusters, vista.sel);
    if (vista.apartado === 0) return cs.filter((c) => !c.articulos.length);
    return cs.filter((c) => c.articulos.includes(vista.apartado));
  }, [clusters, vista]);

  const nombreSel = (sel: Selector) =>
    meta.temas.find((t) => t.clave === sel)?.corto ?? "Sin clasificar";

  return (
    <section className="space-y-5">
      <div>
        <span className="etiqueta">Servicio Andaluz de Salud</span>
        <h2 className="mt-3 text-[33px] font-medium leading-[1.06] tracking-[-0.035em]">
          Lo que más se pregunta
        </h2>
        <p className="mt-2 max-w-[38ch] text-sm leading-relaxed text-suave">
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
          onAbre={(sel, art) => {
            setPestana("temas");
            setVista({ tipo: "preguntas", sel, apartado: art });
          }}
        />
      )}

      {pestana === "conceptos" && (
        <Conceptos conceptos={conceptos} abierto={abierto} setAbierto={setAbierto} />
      )}

      {pestana === "temas" && vista.tipo === "lista" && (
        <ol className="space-y-2">
          {temas.map((t, i) => {
            const sel = t.clave;
            const sinPreguntas = t.preguntas === 0;
            const esOficial = typeof sel === "number";
            return (
              <li key={String(sel)}>
                <Fila
                  atenuado={sinPreguntas}
                  titulo={t.corto}
                  detalle={
                    sinPreguntas
                      ? "Prácticamente no cae · apenas aparece en los exámenes"
                      : `${t.preguntas} preguntas${esOficial && sel <= 10 ? " · bloque común" : ""}`
                  }
                  onClick={() => {
                    if (sinPreguntas) return;
                    // los temas legales tienen artículos; el resto va directo a preguntas
                    if (esOficial && (sel as number) <= 10) setVista({ tipo: "apartados", sel });
                    else setVista({ tipo: "preguntas", sel, apartado: 0 });
                  }}
                  derecha={
                    <span className="font-mono text-[11px] font-bold tabular-nums text-suave">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  }
                />
              </li>
            );
          })}
        </ol>
      )}

      {pestana === "temas" && vista.tipo === "apartados" && (
        <ol className="space-y-2">
          <div className="flex items-center gap-2">
            <Boton tipo="fantasma" onClick={() => setVista({ tipo: "lista" })}>
              Atrás
            </Boton>
            <span className="text-sm font-semibold tracking-tight">{nombreSel(vista.sel)}</span>
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
                  onClick={() => setVista({ tipo: "preguntas", sel: vista.sel, apartado: art })}
                  derecha={
                    <span className="font-mono text-[11px] font-bold tabular-nums text-suave">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                  }
                />
              </li>
            ))}
          {[...apartados.entries()].some(([art]) => art === 0) && (
            <li>
              <Fila
                titulo="Preguntas sin artículo concreto"
                detalle="Definiciones y conceptos generales del tema"
                onClick={() => setVista({ tipo: "preguntas", sel: vista.sel, apartado: 0 })}
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
                  typeof vista.sel === "number" && vista.sel <= 10
                    ? { tipo: "apartados", sel: vista.sel }
                    : { tipo: "lista" }
                )
              }
            >
              Atrás
            </Boton>
            <span className="text-sm font-semibold tracking-tight">
              {vista.apartado === 0 ? nombreSel(vista.sel) : `Artículo ${vista.apartado}`}
            </span>
          </div>
          <span className="etiqueta">
            {preguntas.length} pregunta{preguntas.length === 1 ? "" : "s"} · por lo que más se repiten
          </span>
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
    <article className="tarjeta p-5">
      <div className="flex flex-wrap items-center gap-1.5">
        <NombreTema cluster={c} />
        <Chip tono="cobalto">ha caído en {c.anios.join(", ")}</Chip>
      </div>
      <h3 className="mt-2.5 text-[15.5px] font-medium leading-snug tracking-tight">{c.enunciado}</h3>
      <ListaOpciones opciones={c.opciones} correcta={c.correcta} />
      <p className="mt-3 font-mono text-[10.5px] font-bold uppercase tracking-wider text-suave">
        {c.frecuencia} vez/veces
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
  if (!conceptos) {
    return <div className="tarjeta px-4 py-5 text-sm text-suave">Cargando conceptos…</div>;
  }
  if (!conceptos.conceptos.length) {
    return (
      <div className="tarjeta px-4 py-5 text-sm text-suave">
        No hay datos de conceptos en esta versión.
      </div>
    );
  }
  return (
    <div className="space-y-3">
      <div className="rounded-accion border border-hilo bg-fondo px-4 py-4 text-[13.8px] leading-relaxed text-suave">
        El tribunal casi nunca repite la misma pregunta. Lo que hace es preguntar{" "}
        <b className="text-tinta">lo mismo con otras palabras</b>. Aquí están esos casos:{" "}
        <b className="text-tinta">{conceptos.n_multi_anio} preguntas que se repiten</b> a lo largo
        de {new Set(conceptos.conceptos.flatMap((c) => c.anios)).size} años. Con su respuesta, para
        poder estudiarla.
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
      ? "casi la misma pregunta"
      : coh === "media"
        ? "mismo concepto"
        : "mismo tema";
  const tonoCoh = coh === "alta" ? "verde" : coh === "media" ? "albero" : "neutro";
  return (
    <article className="tarjeta">
      <button type="button" onClick={toggle} className="w-full p-5 text-left">
        <div className="flex flex-wrap items-center gap-1.5">
          <Chip tono="cobalto">ha caído en {c.anios.join(", ")}</Chip>
          <Chip tono={tonoCoh as "verde" | "albero" | "neutro"}>{etiquetaCoh}</Chip>
          <Chip tono="berenjena">concepto</Chip>
        </div>
        <h3 className="mt-3 text-[15.5px] font-medium leading-snug tracking-tight">
          {c.representante}
        </h3>
        <p className="mt-1.5 font-mono text-[10.5px] font-bold uppercase tracking-wider text-suave">
          formulada de {c.n_preguntas} formas distintas
          {c.temas.length > 0 && (
            <> · {c.temas.map((t) => `T${String(t).padStart(2, "0")}`).join(" ")}</>
          )}
          {" · "}
          {abierto ? "tocar para cerrar" : "tocar para ver las respuestas"}
        </p>
      </button>
      {abierto && (
        <ul className="space-y-4 border-t border-hilo px-5 pb-5 pt-4">
          {c.miembros.map((m) => (
            <li key={m.id} className="rounded-opcion bg-superficie px-4 py-3.5">
              <div className="flex flex-wrap items-center gap-1.5">
                <Chip tono="cobalto">
                  {m.anio} · {m.modalidad}
                </Chip>
                {m.tema !== null && <Chip>T{String(m.tema).padStart(2, "0")}</Chip>}
              </div>
              <p className="mt-2.5 text-[14.5px] font-medium leading-snug tracking-tight">
                {m.enunciado}
              </p>
              {m.opciones ? (
                <ListaOpciones opciones={m.opciones} correcta={m.correcta} />
              ) : (
                <p className="mt-2 font-mono text-[10.5px] uppercase tracking-wider text-suave">
                  respuesta: {m.correcta ?? "—"}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}

function Calendario({
  clusters,
  meta,
  onAbre,
}: {
  clusters: Cluster[];
  meta: Meta;
  onAbre: (sel: Selector, articulo: number) => void;
}) {
  const anios = meta.anios;
  const filas = useMemo(() => {
    const m = new Map<
      string,
      { sel: Selector; art: number; etiqueta: string; porAnio: Map<number, number>; total: number }
    >();
    for (const c of clusters) {
      const arts = c.articulos.length ? c.articulos : [0];
      for (const a of arts) {
        const k = `${String(c.clave)}:${a}`;
        const d = m.get(k) ?? {
          sel: c.clave,
          art: a,
          etiqueta: c.tema_corto || c.tema_nombre || "Sin clasificar",
          porAnio: new Map<number, number>(),
          total: 0,
        };
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
      <div className="rounded-accion border border-hilo bg-fondo px-4 py-4 text-[13.8px] leading-relaxed text-suave">
        Qué artículos caen en cada convocatoria. <b className="text-tinta">Más verde = más veces</b>.
        Toca una fila para ver las preguntas.
      </div>
      <div className="overflow-x-auto rounded-accion border border-hilo bg-fondo p-4">
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="sticky left-0 bg-fondo py-2 pr-2 text-left">
                <span className="etiqueta">Artículo</span>
              </th>
              {anios.map((a) => (
                <th key={a} className="px-1.5 py-2">
                  <span className="etiqueta">{a}</span>
                </th>
              ))}
              <th className="py-2 pl-2">
                <span className="etiqueta">Total</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {filas.slice(0, 30).map((f) => (
              <tr key={`${String(f.sel)}:${f.art}`} className="border-t border-hilo">
                <td className="sticky left-0 bg-fondo py-2 pr-2">
                  <button
                    type="button"
                    onClick={() => onAbre(f.sel, f.art)}
                    className="text-left text-[13px] font-semibold underline decoration-dotted underline-offset-2 hover:text-verde"
                  >
                    {f.art === 0 ? f.etiqueta : `Art. ${f.art}`}
                  </button>
                </td>
                {anios.map((a) => {
                  const n = f.porAnio.get(a) ?? 0;
                  const op = n === 0 ? 0 : 0.18 + (n / max) * 0.82;
                  return (
                    <td key={a} className="px-1 py-1.5 text-center">
                      <span
                        className="inline-flex h-6 w-8 items-center justify-center rounded-[4px] font-mono text-[11px] font-bold tabular-nums"
                        style={{
                          background: n ? `rgba(15, 81, 50, ${op})` : "transparent",
                          color: n && op > 0.55 ? "#fff" : undefined,
                        }}
                      >
                        {n || "·"}
                      </span>
                    </td>
                  );
                })}
                <td className="py-2 pl-2 text-center font-mono text-[13px] font-bold tabular-nums">
                  {f.total}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
