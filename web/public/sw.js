/** Service worker de OpoTCAE.
 *
 *  Estrategia:
 *   - Shell de la app (HTML, JS, CSS, iconos): cache-first. Es contenido con
 *     nombre por hash, así que se puede cachear sin miedo.
 *   - Datos (data/*.json): stale-while-revalidate. Se muestra lo cacheado
 *     al instante y se actualiza en segundo plano cuando hay red.
 *  Con eso la app abre sin conexión una vez la hayas usado, que es lo que se
 *  espera de una herramienta de estudio.
 */

const SHELL = "opotcae-shell-v1";
const DATOS = "opotcae-datos-v1";

self.addEventListener("install", (evento) => {
  evento.waitUntil(
    caches.open(SHELL).then((c) => c.addAll(["/", "/manifest.webmanifest", "/favicon.svg"]))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (evento) => {
  evento.waitUntil(
    caches
      .keys()
      .then((claves) =>
        Promise.all(claves.filter((k) => k !== SHELL && k !== DATOS).map((k) => caches.delete(k)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (evento) => {
  const url = new URL(evento.request.url);
  if (evento.request.method !== "GET" || url.origin !== self.location.origin) return;

  const esDato = url.pathname.startsWith("/data/");
  const cache = esDato ? DATOS : SHELL;

  if (esDato) {
    // stale-while-revalidate: responde con la cache y actualiza por detrás
    evento.respondWith(
      caches.open(cache).then(async (c) => {
        const guardada = await c.match(evento.request);
        const red = fetch(evento.request)
          .then((res) => {
            if (res.ok) c.put(evento.request, res.clone());
            return res;
          })
          .catch(() => guardada);
        return guardada || red;
      })
    );
    return;
  }

  // cache-first para el shell
  evento.respondWith(
    caches.match(evento.request).then(
      (guardada) =>
        guardada ||
        fetch(evento.request).then((res) => {
          if (res.ok && res.type === "basic") {
            const copia = res.clone();
            caches.open(cache).then((c) => c.put(evento.request, copia));
          }
          return res;
        })
    )
  );
});
