import type { Cluster, Letra, Opciones } from "../types";

/** Sello verde/blanco. Guiño a la bandera andaluza sin ser una bandera. */
export function Sello() {
  return (
    <span className="sello" aria-hidden>
      <i />
      <i />
      <i />
      <i />
    </span>
  );
}

/** Etiqueta de sección: mono, versalitas, tracking amplio. */
export function Etiqueta({ children }: { children: React.ReactNode }) {
  return <span className="etiqueta">{children}</span>;
}

/** Chip pequeño. */
export function Chip({
  children,
  tono = "neutro",
}: {
  children: React.ReactNode;
  tono?: "verde" | "neutro" | "mal";
}) {
  const c = tono === "verde" ? "chip-verde" : tono === "mal" ? "chip-mal" : "chip-neutro";
  return <span className={c}>{children}</span>;
}

/** Nombre del tema, sin número. */
export function NombreTema({ cluster }: { cluster: Cluster }) {
  return <Chip>{cluster.tema_corto || cluster.tema_nombre || "Sin clasificar"}</Chip>;
}

/** Opción de respuesta. Estados: neutra, acertada o fallada. */
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
  const clase =
    estado === "correcta" ? "op op-ok" : estado === "fallada" ? "op op-mal" : "op";
  const marca = estado === "correcta" ? "✓" : estado === "fallada" ? "✗" : letra;
  const Tag = onElige ? "button" : "div";
  return (
    <Tag
      {...(onElige ? { type: "button" as const, onClick: () => onElige(letra) } : {})}
      className={`${clase}${elegida === letra && estado === "neutra" ? " ring-1 ring-verde" : ""}`}
    >
      <span className="let">{marca}</span>
      <span className="flex-1">{opciones[letra] || <em className="opacity-50">vacía</em>}</span>
    </Tag>
  );
}

/** Barra de progreso, plana y verde. */
export function Barra({ valor, total }: { valor: number; total: number }) {
  const pct = total ? Math.round((valor / total) * 100) : 0;
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-aguaverde">
      <div
        className="h-full rounded-full bg-verde transition-all duration-300"
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

/** Acción principal de la pantalla de inicio. */
export function AccionPrincipal({
  children,
  onClick,
  subtitulo,
  cifra,
}: {
  children: React.ReactNode;
  onClick: () => void;
  subtitulo?: string;
  cifra?: string | number;
}) {
  return (
    <button type="button" onClick={onClick} className="accion-uno">
      {cifra !== undefined && <span className="cifra">{cifra}</span>}
      <span>
        <strong className="block text-[16px] font-semibold tracking-tight">{children}</strong>
        {subtitulo && <span className="mt-0.5 block text-[12.5px] opacity-80">{subtitulo}</span>}
      </span>
    </button>
  );
}

/** Acción secundaria de la pantalla de inicio. */
export function AccionSecundaria({
  children,
  onClick,
  subtitulo,
  marca,
}: {
  children: React.ReactNode;
  onClick: () => void;
  subtitulo?: string;
  marca?: string;
}) {
  return (
    <button type="button" onClick={onClick} className="accion-dos">
      {marca && <span className="num">{marca}</span>}
      <span>
        <strong className="block text-[14.5px] font-semibold tracking-tight">{children}</strong>
        {subtitulo && <span className="mt-0.5 block text-[12.5px] text-suave">{subtitulo}</span>}
      </span>
    </button>
  );
}

/** Fila de lista (temas, artículos, convocatorias). */
export function Fila({
  titulo,
  detalle,
  onClick,
  derecha,
  atenuado,
}: {
  titulo: string;
  detalle?: string;
  onClick: () => void;
  derecha?: React.ReactNode;
  atenuado?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={atenuado}
      className={`fila${atenuado ? " opacity-50" : ""}`}
    >
      <span className="flex-1">
        <span className="block text-[15px] font-semibold tracking-tight">{titulo}</span>
        {detalle && <span className="mt-0.5 block text-[12.5px] text-suave">{detalle}</span>}
      </span>
      {derecha}
      {!atenuado && <span className="text-suave">›</span>}
    </button>
  );
}

/** Botón pequeño de navegación. */
export function Boton({
  children,
  onClick,
  tipo = "dos",
  disabled,
  ancho,
}: {
  children: React.ReactNode;
  onClick: () => void;
  tipo?: "uno" | "dos" | "fantasma";
  disabled?: boolean;
  ancho?: boolean;
}) {
  const c = tipo === "uno" ? "boton-uno" : tipo === "fantasma" ? "boton-fantasma" : "boton-dos";
  return (
    <button type="button" onClick={onClick} disabled={disabled} className={`${c}${ancho ? " w-full" : ""}`}>
      {children}
    </button>
  );
}

/** Selector segmentado tipo pastilla. */
export function Segmentado<T extends string>({
  opciones,
  valor,
  onChange,
}: {
  opciones: { valor: T; etiqueta: string }[];
  valor: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="pestanas" role="tablist">
      {opciones.map((o) => (
        <button
          key={o.valor}
          type="button"
          role="tab"
          aria-selected={valor === o.valor}
          onClick={() => onChange(o.valor)}
          className={`pestana${valor === o.valor ? " pestana-on" : ""}`}
        >
          {o.etiqueta}
        </button>
      ))}
    </div>
  );
}
