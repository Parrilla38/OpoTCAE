import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// modo oscuro: respeta la preferencia guardada, si no la del sistema
// (migración: antes las claves se llamaban tcae-*)
for (const [antiguo, nuevo] of [
  ["tcae-tema", "opotcae-tema"],
  ["tcae-progreso-v1", "opotcae-progreso-v1"],
  ["tcae-sm2-v1", "opotcae-sm2-v1"],
] as const) {
  const v = localStorage.getItem(antiguo);
  if (v !== null && localStorage.getItem(nuevo) === null) {
    localStorage.setItem(nuevo, v);
    localStorage.removeItem(antiguo);
  }
}
const guardado = localStorage.getItem("opotcae-tema");
const oscuro =
  guardado === "oscuro" ||
  (guardado === null && window.matchMedia("(prefers-color-scheme: dark)").matches);
document.documentElement.classList.toggle("dark", oscuro);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Service worker: hace que la app abra sin conexión una vez usada.
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((reg) => {
        // si hay una versión nueva del SW, recargar sola al terminar de instalar:
        // así un deploy nunca se queda sin ver por culpa de la cache
        reg.addEventListener("updatefound", () => {
          const nuevo = reg.installing;
          if (!nuevo) return;
          nuevo.addEventListener("statechange", () => {
            if (nuevo.state === "installed" && navigator.serviceWorker.controller) {
              window.location.reload();
            }
          });
        });
      })
      .catch(() => {});
  });
}
