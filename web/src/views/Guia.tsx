import { Boton, Chip } from "../components/ui";

/**
 * Guía de uso, en castellano llano y para todo el mundo.
 * Está pensada para quien no ha usado nunca una web de estas: frases cortas,
 * verbos, y «toca aquí» en vez de tecnicismos.
 */
export default function Guia({ onCerrar }: { onCerrar: () => void }) {
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-fondo">
      <div className="mx-auto max-w-2xl px-4 pb-24 pt-5">
        <header className="mb-6 flex items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-semibold leading-tight tracking-tight">Cómo se usa</h1>
            <p className="etiqueta mt-1">OpoTCAE · guía rápida</p>
          </div>
          <Boton tipo="fantasma" onClick={onCerrar}>
            Cerrar ✕
          </Boton>
        </header>

        <section className="space-y-4">
          <div className="tarjeta p-5">
            <span className="etiqueta">Qué es esto</span>
            <p className="mt-3 text-[15.5px] leading-relaxed">
              Es una web para preparar las <b>oposiciones de TCAE de Andalucía</b>. Está hecha con
              las preguntas de los exámenes oficiales de años anteriores. Te enseña{" "}
              <b>qué se repite más</b> para que estudies lo que de verdad cae.
            </p>
            <p className="mt-2.5 text-[15.5px] leading-relaxed">
              Es <b>gratis</b>, no hay que registrarse y no guarda datos tuyos en ningún servidor.
            </p>
          </div>

          <div className="tarjeta p-5">
            <span className="etiqueta">Para empezar, en un minuto</span>
            <ol className="mt-4 space-y-3.5">
              <Paso n={1} texto={<>Abajo hay 4 botones. Toca el primero: <b>Practicar</b>.</>} />
              <Paso n={2} texto={<>Toca el botón verde grande: <b>Empezar ahora</b>.</>} />
              <Paso n={3} texto={<>Lee la pregunta y toca la respuesta que creas buena.</>} />
              <Paso n={4} texto={<>Al final verás tu nota y las respuestas correctas.</>} />
            </ol>
            <p className="mt-4 text-sm text-suave">
              Eso es todo. Ya lo estás usando. Lo demás son detalles.
            </p>
          </div>

          <div>
            <span className="etiqueta">Los 4 botones de abajo</span>
            <div className="mt-3 space-y-2">
              <Guion
                icono="🎯"
                titulo="Practicar"
                texto="Para hacer tests. Es lo que harás casi siempre. Puedes elegir cuántas preguntas, de qué tema, y si quieres que penalicen los fallos como en el examen de verdad."
              />
              <Guion
                icono="📖"
                titulo="Aprender"
                texto="Para estudiar. Te enseña los temas y artículos que más caen, ordenados por importancia real. Dentro están las preguntas de verdad y el texto de la ley."
              />
              <Guion
                icono="🗓"
                titulo="Exámenes"
                texto="Para ver los exámenes de otros años tal cual salieron. Cada pregunta dice si es nueva ese año o si ya había salido antes."
              />
              <Guion
                icono="👤"
                titulo="Mi progreso"
                texto="Aquí se guardan las preguntas que fallas. Vuelven solas cada pocos días, justo antes de que las olvides. También están tus estadísticas."
              />
            </div>
          </div>

          <div className="tarjeta p-5">
            <span className="etiqueta">Las tres cosas más útiles</span>
            <ol className="mt-4 space-y-4">
              <li>
                <p className="text-[15.5px] font-semibold">1 · Estudia por lo que más cae, no por el orden del temario.</p>
                <p className="mt-1 text-sm leading-relaxed text-suave">
                  En <b>Aprender</b> → <b>Por tema</b>, los temas están ordenados por cuántas
                  preguntas han caído. Empieza por el primero.
                </p>
              </li>
              <li>
                <p className="text-[15.5px] font-semibold">2 · Lee el artículo de la ley.</p>
                <p className="mt-1 text-sm leading-relaxed text-suave">
                  Casi nunca se repite la misma pregunta, pero sí el mismo artículo. Cuando veas
                  «art. 47», ábrelo: debajo de las preguntas está el texto de la ley para que lo
                  estudies.
                </p>
              </li>
              <li>
                <p className="text-[15.5px] font-semibold">3 · Repasa lo que fallas.</p>
                <p className="mt-1 text-sm leading-relaxed text-suave">
                  Cada vez que fallas, la pregunta se guarda sola. En <b>Mi progreso</b> →{" "}
                  <b>Hoy</b> verás las que toca repasar. Dales a <b>Ver respuesta</b> y di si te
                  costó: la web se encarga del resto.
                </p>
              </li>
            </ol>
          </div>

          <div className="tarjeta p-5">
            <span className="etiqueta">Preguntas que se hacen todos</span>
            <dl className="mt-4 space-y-4">
              <Duda
                q="¿Tengo que registrarme?"
                a="No. Abres la web y ya puedes usarla. Tus datos se guardan solo en tu móvil u ordenador."
              />
              <Duda
                q="¿Se pierde mi progreso si borro el navegador?"
                a="Sí. Si borras los datos del navegador, se borra lo que hayas hecho. No está en ningún servidor, así que no se puede recuperar."
              />
              <Duda
                q="¿Va bien en el móvil?"
                a="Sí, está pensado para eso. Lo puedes incluso instalar como una app: en el navegador, busca «Añadir a pantalla de inicio»."
              />
              <Duda
                q="¿Se puede usar sin internet?"
                a="Una vez la hayas usado con internet, sí. Al volver a abrirla sin conexión, se abre con lo último que cargó."
              />
              <Duda
                q="¿Me van a hacer preguntas nuevas que no están aquí?"
                a="Probablemente sí. Estas son las de exámenes oficiales pasadas. Sirven para saber por dónde tirar, no para memorizarlas tal cual: casi nunca se repiten."
              />
              <Duda
                q="¿Esto me asegura la plaza?"
                a="No, eso no lo asegura nada. Es una herramienta para usar tu tiempo donde más cobra."
              />
            </dl>
          </div>

          <div className="rounded-accion border border-hilo bg-fondo px-4 py-4 font-mono text-[10px] uppercase leading-relaxed tracking-wider text-suave">
            Las preguntas son transcripciones de los exámenes oficiales del Servicio Andaluz de
            Salud (Junta de Andalucía). Los artículos son del BOE. Todo atribuido a su fuente.
          </div>

          <Boton tipo="uno" ancho onClick={onCerrar}>
            Entendido, a estudiar
          </Boton>
        </section>
      </div>
    </div>
  );
}

function Paso({ n, texto }: { n: number; texto: React.ReactNode }) {
  return (
    <li className="flex gap-3">
      <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-verde font-mono text-[12px] font-bold text-fondo">
        {n}
      </span>
      <span className="flex-1 pt-1 text-[15.5px] leading-snug">{texto}</span>
    </li>
  );
}

function Guion({
  icono,
  titulo,
  texto,
}: {
  icono: string;
  titulo: string;
  texto: string;
}) {
  return (
    <div className="fila">
      <span aria-hidden className="text-xl">
        {icono}
      </span>
      <span className="flex-1">
        <span className="block text-[15px] font-semibold tracking-tight">{titulo}</span>
        <span className="mt-0.5 block text-[13.5px] leading-snug text-suave">{texto}</span>
      </span>
    </div>
  );
}

function Duda({ q, a }: { q: string; a: string }) {
  return (
    <div>
      <dt className="flex items-center gap-2 text-[15px] font-semibold tracking-tight">
        <Chip tono="cobalto">¿?</Chip>
        {q}
      </dt>
      <dd className="mt-1.5 text-sm leading-relaxed text-suave">{a}</dd>
    </div>
  );
}
