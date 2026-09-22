/** Genera los iconos PNG de la PWA a partir de public/favicon.svg.
 *
 *  node scripts/genera-iconos.mjs
 *
 *  iOS no ofrece «Añadir a pantalla de inicio» con solo SVG: hacen falta PNG
 *  de 192 y 512 px. Se regeneran al cambiar el favicon.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { Resvg } from "@resvg/resvg-js";

const raiz = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const svg = readFileSync(resolve(raiz, "public/favicon.svg"), "utf8");

for (const lado of [192, 512]) {
  const png = new Resvg(svg, { fitTo: { mode: "width", value: lado } }).render().asPng();
  const salida = resolve(raiz, `public/icono-${lado}.png`);
  writeFileSync(salida, png);
  console.log(`icono-${lado}.png  ${png.length} bytes`);
}
