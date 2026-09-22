import type { Cluster, Letra, Opciones } from "../types";

/** Botón de opción de respuesta. Sin jerga: solo se ve si es correcta o no. */
export function Opcion({
  opciones,
  letra,
  estado,
  elegida,
  onElige,
}: {
  opciones: Opciones;
  letra: Letra;
  estado: "neutra" | "correcta" | "fallada";
  elegida?: Letra | null;
  onElige?: (l: Letra) => void;
}) {
  const base =
    "flex w-full items-start gap-3 rounded-2xl border p-4 text-left text-[15px] leading-snug transition " +
    "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 " +
    "disabled:cursor-default";
  const visual =
    estado === "correcta"
      ? "border-emerald-600 bg-emerald-50 ring-1 ring-emerald-600 dark:bg-emerald-950/40"
      : estado === "fallada"
        ? "border-rose-500 bg-rose-50 ring-1 ring-rose-500 dark:bg-rose-950/40"
        : elegida === letra
          ? "border-emerald-600 bg-emerald-50 ring-1 ring-emerald-600 dark:bg-emerald-950/40"
          : "border-stone-200 bg-white hover:border-emerald-400 hover:bg-emerald-50/50 dark:border-stone-800 dark:bg-stone-900";
  const marca = estado === "correcta" ? "✓" : estado === "fallada" ? "✗" : letra;
  return (
    <button type="button" className={`${base} ${visual}`} onClick={() => onElige?.(letra)} disabled={!onElige}>
      <span
        className={
          "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-bold " +
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

/** Barra de progreso. */
export function Barra({ valor, total }: { valor: number; total: number }) {
  const pct = total ? Math.round((valor / total) * 100) : 0;
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-stone-200 dark:bg-stone-800">
      <div
        className="h-full rounded-full bg-emerald-600 transition-all duration-300"
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

/** Etiqueta pequeña. Solo donde aporta: máximo una por tarjeta. */
export function Etiqueta({
  children,
  tono = "gris",
}: {
  children: React.ReactNode;
  tono?: "gris" | "verde" | "ambar" | "azul";
}) {
  const colores = {
    gris: "bg-stone-200 text-stone-700 dark:bg-stone-800 dark:text-stone-200",
    verde: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200",
    ambar: "bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-200",
    azul: "bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-200",
  };
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${colores[tono]}`}>
      {children}
    </span>
  );
}

/** Nombre corto del tema, sin número si no es oficial. */
export function NombreTema({ cluster }: { cluster: Cluster }) {
  if (!cluster.tema_corto) return <Etiqueta>{cluster.tema_nombre ?? "Sin clasificar"}</Etiqueta>;
  return <Etiqueta>{cluster.tema_corto}</Etiqueta>;
}

/** Botón de sección tipo «fila». */
export function Fila({
  titulo,
  detalle,
  onClick,
  derecha,
}: {
  titulo: string;
  detalle?: string;
  onClick: () => void;
  derecha?: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex w-full items-center gap-3 rounded-2xl border border-stone-200 bg-white p-4 text-left transition hover:border-emerald-400 hover:bg-emerald-50/50 dark:border-stone-800 dark:bg-stone-900 dark:hover:bg-stone-800"
    >
      <span className="flex-1">
        <span className="block text-[15px] font-semibold leading-snug">{titulo}</span>
        {detalle && (
          <span className="mt-0.5 block text-xs text-stone-500 dark:text-stone-400">{detalle}</span>
        )}
      </span>
      {derecha}
      <span className="text-xl text-stone-300 dark:text-stone-600">›</span>
    </button>
  );
}

/** Botón grande de acción principal. */
export function AccionPrincipal({
  children,
  onClick,
  subtitulo,
  icono,
}: {
  children: React.ReactNode;
  onClick: () => void;
  subtitulo?: string;
  icono?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex w-full items-center gap-4 rounded-2xl bg-emerald-600 p-5 text-left text-white shadow-sm transition hover:bg-emerald-700 active:bg-emerald-800"
    >
      {icono && (
        <span aria-hidden className="text-3xl">
          {icono}
        </span>
      )}
      <span className="flex-1">
        <span className="block text-lg font-bold leading-tight">{children}</span>
        {subtitulo && <span className="mt-0.5 block text-sm text-emerald-50">{subtitulo}</span>}
      </span>
    </button>
  );
}

/** Botón secundario grande. */
export function AccionSecundaria({
  children,
  onClick,
  subtitulo,
  icono,
}: {
  children: React.ReactNode;
  onClick: () => void;
  subtitulo?: string;
  icono?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex w-full items-center gap-4 rounded-2xl border border-stone-200 bg-white p-4 text-left transition hover:border-emerald-400 hover:bg-emerald-50/50 dark:border-stone-800 dark:bg-stone-900 dark:hover:bg-stone-800"
    >
      {icono && (
        <span aria-hidden className="text-2xl">
          {icono}
        </span>
      )}
      <span className="flex-1">
        <span className="block text-[15px] font-semibold leading-tight">{children}</span>
        {subtitulo && (
          <span className="mt-0.5 block text-xs text-stone-500 dark:text-stone-400">{subtitulo}</span>
        )}
      </span>
    </button>
  );
}

/** Botón pequeño de navegación (atrás / siguiente). */
export function Boton({
  children,
  onClick,
  tipo = "secundario",
  disabled,
  ancho,
}: {
  children: React.ReactNode;
  onClick: () => void;
  tipo?: "principal" | "secundario" | "fantasma";
  disabled?: boolean;
  ancho?: boolean;
}) {
  const t =
    tipo === "principal"
      ? "bg-emerald-600 text-white hover:bg-emerald-700"
      : tipo === "fantasma"
        ? "text-stone-600 hover:bg-stone-200/60 dark:text-stone-300 dark:hover:bg-stone-800/60"
        : "border border-stone-300 bg-white text-stone-800 hover:bg-stone-100 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-100";
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold transition disabled:opacity-40 ${t} ${ancho ? "w-full" : ""}`}
    >
      {children}
    </button>
  );
}

/** Selector segmentado. */
export function Segmentado<T extends string | number>({
  opciones,
  valor,
  onChange,
}: {
  opciones: { valor: T; etiqueta: string }[];
  valor: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex gap-1 rounded-xl bg-stone-200/60 p-1 dark:bg-stone-800/60">
      {opciones.map((o) => (
        <button
          key={String(o.valor)}
          type="button"
          onClick={() => onChange(o.valor)}
          className={
            "flex-1 rounded-lg px-2 py-2 text-sm font-semibold transition " +
            (valor === o.valor
              ? "bg-white shadow dark:bg-stone-900"
              : "text-stone-600 dark:text-stone-300")
          }
        >
          {o.etiqueta}
        </button>
      ))}
    </div>
  );
}
