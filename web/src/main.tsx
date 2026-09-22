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
