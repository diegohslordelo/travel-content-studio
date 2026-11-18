/**
 * Quadros de conferência de um Reel (qualquer composição 1080 × 1920), num único bundle.
 *   node scripts/quadros_reel.mjs <Composicao> <props.json> <public-dir> <saida-dir> <q1,q2,...> [escala]
 */
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const chromes = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell", "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"];
const browserExecutable = chromes.find((c) => existsSync(c)) ?? null;
const [id, arqProps, publicDir, saida, lista, escala = "0.5"] = process.argv.slice(2);
const inputProps = JSON.parse(readFileSync(arqProps, "utf-8"));
const serveUrl = await bundle({ entryPoint: path.join(raiz, "src", "index.ts"), publicDir: path.resolve(publicDir) });
const composition = await selectComposition({ serveUrl, id, inputProps, browserExecutable, logLevel: "warn" });
mkdirSync(saida, { recursive: true });
for (const q of lista.split(",").map(Number)) {
  await renderStill({ serveUrl, composition, frame: q, output: path.join(saida, `q${String(q).padStart(5, "0")}.jpg`), imageFormat: "jpeg", jpegQuality: 85, scale: Number(escala), inputProps, browserExecutable, logLevel: "warn" });
  process.stdout.write(`${q} `);
}
console.log("ok");
