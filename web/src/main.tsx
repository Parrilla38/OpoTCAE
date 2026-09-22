import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// modo oscuro: respeta la preferencia guardada, si no la del sistema
const guardado = localStorage.getItem("tcae-tema");
const oscuro =
  guardado === "oscuro" ||
  (guardado === null && window.matchMedia("(prefers-color-scheme: dark)").matches);
document.documentElement.classList.toggle("dark", oscuro);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
