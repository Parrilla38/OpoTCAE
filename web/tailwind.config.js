/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Los valores van por variables CSS para que el modo oscuro cambie solo.
        fondo: "rgb(var(--fondo) / <alpha-value>)",
        superficie: "rgb(var(--superficie) / <alpha-value>)",
        tinta: "rgb(var(--tinta) / <alpha-value>)",
        suave: "rgb(var(--suave) / <alpha-value>)",
        hilo: "rgb(var(--hilo) / <alpha-value>)",
        verde: "rgb(var(--verde) / <alpha-value>)",
        aguaverde: "rgb(var(--aguaverde) / <alpha-value>)",
        mal: "rgb(var(--mal) / <alpha-value>)",
        aguamal: "rgb(var(--aguamal) / <alpha-value>)",
        // color por significado, no decorativo
        albero: "rgb(var(--albero) / <alpha-value>)", // tierra de la Alhambra · «ya había caído», nivel medio
        aguaalbero: "rgb(var(--aguaalbero) / <alpha-value>)",
        cobalto: "rgb(var(--cobalto) / <alpha-value>)", // azulejo de Triana · convocatorias, información
        aguacobalto: "rgb(var(--aguacobalto) / <alpha-value>)",
        berenjena: "rgb(var(--berenjena) / <alpha-value>)", // conceptos y análisis semántico
        aguaberenjena: "rgb(var(--aguaberenjena) / <alpha-value>)",
      },
      fontFamily: {
        sans: ['"Familjen Grotesk"', "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ['"IBM Plex Mono"', "ui-monospace", "monospace"],
      },
      borderRadius: {
        accion: "14px",
        tarjeta: "18px",
        opcion: "12px",
        pastilla: "16px",
      },
      letterSpacing: {
        etiqueta: "0.28em",
      },
    },
  },
  plugins: [],
};
