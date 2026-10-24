/**
 * Thumbnail do vídeo longo (composição `ThumbYT`, 1280 × 720).
 *
 *   node scripts/thumb.mjs <props.json> <public-dir> <saida.png>
 */
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..");
const chrome = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell";
const browserExecutable = existsSync(chrome) ? chrome : null;
const [arqProps, publicDir, saida] = process.argv.slice(2);
const inputProps = JSON.parse(readFileSync(arqProps, "utf-8"));
const serveUrl = await bundle({ entryPoint: path.join(raiz, "src", "index.ts"), publicDir: path.resolve(publicDir) });
const comum = { serveUrl, browserExecutable, logLevel: "warn", inputProps };
const composition = await selectComposition({ ...comum, id: "ThumbYT" });
await renderStill({ ...comum, composition, frame: 0, output: saida, imageFormat: "png" });
console.log("ok", saida);
