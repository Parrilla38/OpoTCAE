import { useState } from "react";

/** Explicación del método, en español llano, bajo demanda. */
export default function ComoFunciona() {
  const [abierto, setAbierto] = useState(false);
  return (
    <div className="rounded-accion border border-hilo bg-fondo">
      <button
        type="button"
        onClick={() => setAbierto((v) => !v)}
        className="flex w-full items-center gap-2 px-4 py-3.5 text-left text-[14.5px] font-semibold"
      >
        <span className="flex-1">¿Cómo funciona?</span>
        <span className="font-mono text-suave">{abierto ? "−" : "+"}</span>
      </button>
      {abierto && (
        <div className="space-y-3 border-t border-hilo px-4 py-4 text-[13.8px] leading-relaxed text-suave">
          <p>
            Hemos analizado las <b className="text-tinta">1.539 preguntas</b> de los{" "}
            <b className="text-tinta">exámenes oficiales</b> del Servicio Andaluz de Salud de 2016 a
            2025.
          </p>
          <p>
            El descubrimiento importante: <b className="text-tinta">las preguntas casi nunca se
            repiten tal cual</b>. Lo que se repite es <b className="text-tinta">el tema y el
            artículo</b>. El artículo 47 de la Ley de Salud de Andalucía se ha preguntado en 2019 y
            en 2022, con dos redacciones distintas.
          </p>
          <p>Por eso aquí puedes:</p>
          <ul className="space-y-1.5 pl-4">
            <li>
              <b className="text-tinta">Practicar</b> con lo que más se pregunta, no con preguntas
              al azar.
            </li>
            <li>
              <b className="text-tinta">Aprender</b> qué temas y apartados son los que más caen, en
              orden de importancia real.
            </li>
            <li>
              <b className="text-tinta">Repasar</b> lo que fallas: vuelven cuando estés a punto de
              olvidarlos.
            </li>
          </ul>
          <p className="pt-1 font-mono text-[10px] uppercase tracking-etiqueta">
            Gratis · sin cuenta · sin publicidad
          </p>
        </div>
      )}
    </div>
  );
}
