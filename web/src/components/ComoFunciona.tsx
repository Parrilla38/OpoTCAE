import { useState } from "react";

/** Explicación corta del método, en español llano. Se despliega bajo demanda. */
export default function ComoFunciona() {
  const [abierto, setAbierto] = useState(false);
  return (
    <div className="rounded-2xl border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-900">
      <button
        type="button"
        onClick={() => setAbierto((v) => !v)}
        className="flex w-full items-center gap-2 p-4 text-left text-sm font-semibold"
      >
        <span className="flex-1">¿Cómo funciona?</span>
        <span className="text-stone-400">{abierto ? "−" : "+"}</span>
      </button>
      {abierto && (
        <div className="space-y-3 px-4 pb-4 text-sm leading-relaxed text-stone-600 dark:text-stone-300">
          <p>
            Hemos analizado las <b>1.539 preguntas</b> de los <b>exámenes oficiales</b> del
            Servicio Andaluz de Salud de 2016 a 2025.
          </p>
          <p>
            El descubrimiento importante: <b>las preguntas casi nunca se repiten tal cual</b>. Lo
            que se repite es <b>el tema y el artículo</b>. Por ejemplo, el artículo 47 de la Ley de
            Salud de Andalucía se ha preguntado en 2019 y en 2022, con dos redacciones distintas.
          </p>
          <p>Por eso aquí puedes:</p>
          <ul className="list-disc space-y-1 pl-5">
            <li>
              <b>Practicar</b> con lo que más se pregunta, no con preguntas al azar.
            </li>
            <li>
              <b>Aprender</b> qué temas y apartados son los que más caen, en orden de importancia
              real.
            </li>
            <li>
              <b>Repasar</b> lo que fallas con repasos espaciados: vuelven cuando estés a punto de
              olvidarlos.
            </li>
          </ul>
          <p className="text-xs text-stone-500">
            Fuente: cuadernillos y plantillas oficiales del Servicio Andaluz de Salud (Junta de
            Andalucía). Todo gratis y sin cuenta: tu progreso se guarda solo en este navegador.
          </p>
        </div>
      )}
    </div>
  );
}
