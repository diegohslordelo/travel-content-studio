/**
 * Render de uma composição do formato (ex.: `TrailerFormato`) a partir das props de uma revisão. Só a imagem: o som
 * é mixado pelo script da revisão e entra no mux.
 *
 *   node scripts/formato.mjs <Composicao> <props.json> <public-dir> tudo    <saida.mp4>
 *   node scripts/formato.mjs <Composicao> <props.json> <public-dir> quadros <saida-dir> <q1,q2,...>
 */
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const chrome = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell", "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"].find((c) => existsSync(c));
const [id, arqProps, publicDir, modo, saida, lista] = process.argv.slice(2);
const inputProps = JSON.parse(readFileSync(arqProps, "utf-8"));
const serveUrl = await bundle({ entryPoint: path.join(raiz, "src", "index.ts"), publicDir: path.resolve(publicDir) });
const comum = { serveUrl, browserExecutable: chrome ?? null, logLevel: "warn", inputProps, timeoutInMilliseconds: 300000 };
const composition = await selectComposition({ ...comum, id });
if (modo === "quadros") {
  mkdirSync(saida, { recursive: true });
  for (const q of lista.split(",").map(Number)) {
    await renderStill({ ...comum, composition, frame: q, output: path.join(saida, `q${String(q).padStart(5, "0")}.png`) });
  }
} else {
  let ultimo = -1;
  await renderMedia({ ...comum, composition, codec: "h264", crf: 17, muted: true, outputLocation: saida,
    onProgress: ({ progress }) => { const p = Math.floor(progress * 100); if (p >= ultimo + 10) { ultimo = p; console.log(`  ${p}%`); } } });
}
console.log("ok", saida);
