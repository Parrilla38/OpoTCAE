import type { Cluster, Letra, Opciones } from "../types";

export function TarjetaOpcion({
  opciones,
  letra,
  estado,
  elegida,
  onElige,
}: {
  opciones: Opciones;
  letra: Letra;
  estado: "ninguna" | "correcta" | "fallada" | "neutra";
  elegida: Letra | null;
  onElige?: (l: Letra) => void;
}) {
  const clases = [
    "opcion",
    estado === "correcta" ? "opcion-correcta" : "",
    estado === "fallada" ? "opcion-fallada" : "",
    estado === "ninguna" ? "opcion-ninguna" : "",
    estado === "neutra" && elegida === letra ? "opcion-elegida" : "",
    estado === "neutra" && elegida !== letra ? "opcion-ninguna" : "",
    onElige ? "" : "opcion-deshabilitada",
  ]
    .filter(Boolean)
    .join(" ");
  const marca =
    estado === "correcta" ? "✓" : estado === "fallada" ? "✗" : letra;
  return (
    <button type="button" className={clases} onClick={() => onElige?.(letra)} disabled={!onElige}>
      <span
        className={
          "mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold " +
          (estado === "correcta"
            ? "bg-emerald-600 text-white"
            : estado === "fallada"
              ? "bg-rose-500 text-white"
              : "bg-stone-200 text-stone-700 dark:bg-stone-800 dark:text-stone-200")
        }
      >
        {marca}
      </span>
      <span className="flex-1">{opciones[letra] || <em className="text-stone-400">vacía</em>}</span>
    </button>
  );
}

export function BarraProgreso({ valor, total }: { valor: number; total: number }) {
  const pct = total ? Math.round((valor / total) * 100) : 0;
  return (
    <div className="progreso" role="progressbar" aria-valuenow={valor} aria-valuemax={total}>
      <div className="progreso-relleno" style={{ width: `${pct}%` }} />
    </div>
  );
}

export function EtiquetaTema({ cluster }: { cluster: Cluster }) {
  return (
    <span className="chip bg-stone-200 text-stone-700 dark:bg-stone-800 dark:text-stone-200">
      T{String(cluster.tema ?? 0).padStart(2, "0")} · {cluster.tema_corto || "sin tema"}
    </span>
  );
}

export function EtiquetaRepeticion({ cluster }: { cluster: Cluster }) {
  const años = cluster.anios.join(", ");
  return (
    <span
      className="chip bg-marca-100 text-marca-800 dark:bg-marca-950 dark:text-marca-200"
      title={`Aparece ${cluster.frecuencia} veces en ${cluster.n_anios} año(s): ${años}`}
    >
      ×{cluster.frecuencia} · {cluster.n_anios} año{cluster.n_anios === 1 ? "" : "s"}
    </span>
  );
}

export function RefArticulos({ articulos, tema }: { articulos: number[]; tema: number | null }) {
  if (!articulos.length) return null;
  const norma =
    tema === 1
      ? "CE"
      : tema === 2
        ? "EAA"
        : tema === 3
          ? "Ley 2/1998 / LGS"
          : tema === 4
            ? "Ley 8/1986"
            : tema === 5
              ? "LO 3/2018"
              : tema === 6
                ? "Ley 31/1995"
                : tema === 7
                  ? "LO 1/2004"
                  : tema === 8
                    ? "Ley 55/2003"
                    : tema === 9
                      ? "Ley 41/2002"
                      : "normativa SAS";
  return (
    <span className="chip bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200">
      Art. {articulos.join(", ")} · {norma}
    </span>
  );
}
