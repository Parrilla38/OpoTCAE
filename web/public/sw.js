/** Service worker de OpoTCAE.
 *
 *  Estrategia, pensada para que NUNCA se sirva una versión vieja de la app:
 *
 *   - HTML y navegación: **network-first**. Si hay red se usa la versión nueva;
 *     solo se recurre a la cache sin conexión. Es lo que evita que un deploy
 *     pase inadvertido (el fallo que nos costó una revisión: cacheábamos
 *     index.html con cache-first y el usuario seguía viendo lo viejo).
 *   - /assets/* (nombre con hash): **cache-first**. Son inmutables de por sí.
 *   - /data/*.json: **stale-while-revalidate**. Se pinta al instante y se
 *     actualiza por detrás.
 *   - Resto (iconos, manifest): stale-while-revalidate.
 *
 *  La versión del cache va en el nombre: al subirla se descarta lo anterior.
 */

const VERSION = "v2";
const SHELL = `opotcae-shell-${VERSION}`;
const DATOS = `opotcae-datos-${VERSION}`;
const TODAS = [SHELL, DATOS];

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (evento) => {
  evento.waitUntil(
    caches
      .keys()
      .then((claves) =>
        Promise.all(claves.filter((k) => !TODAS.includes(k)).map((k) => caches.delete(k)))
      )
      .then(() => self.clients.claim())
  );
});

/** ¿Es un documento HTML que hay que servir siempre lo más fresco posible? */
function esDocumento(url) {
  return (
    url.pathname === "/" ||
    url.pathname.endsWith(".html") ||
    url.pathname.endsWith("/")
  );
}

self.addEventListener("fetch", (evento) => {
  const { request } = evento;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin) return;
  // el propio service worker y las peticiones de actualización no se cachean
  if (url.pathname === "/sw.js") return;

  const esDato = url.pathname.startsWith("/data/");
  const esAsset = url.pathname.startsWith("/assets/");
  const cache = esDato ? DATOS : SHELL;

  // HTML: network-first, con caída a cache solo si no hay red
  if (esDocumento(url)) {
    evento.respondWith(
      fetch(request)
        .then((res) => {
          if (res.ok) {
            const copia = res.clone();
            caches.open(cache).then((c) => c.put(request, copia));
          }
          return res;
        })
        .catch(() => caches.match(request).then((g) => g || caches.match("/")))
    );
    return;
  }

  // assets con hash: son inmutables, cache-first
  if (esAsset) {
    evento.respondWith(
      caches.match(request).then(
        (g) =>
          g ||
          fetch(request).then((res) => {
            if (res.ok) {
              const copia = res.clone();
              caches.open(cache).then((c) => c.put(request, copia));
            }
            return res;
          })
      )
    );
    return;
  }

  // datos y el resto: stale-while-revalidate
  evento.respondWith(
    caches.open(cache).then(async (c) => {
      const guardada = await c.match(request);
      const red = fetch(request)
        .then((res) => {
          if (res.ok) c.put(request, res.clone());
          return res;
        })
        .catch(() => guardada);
      return guardada || red;
    })
  );
});
