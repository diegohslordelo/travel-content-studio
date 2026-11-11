// Renderiza vários quadros de uma composição com um único bundle (QA visual rápida).
// uso: node scripts/quadros_teste.mjs <Composicao> <props.json> <public-dir> <saida-dir> <escala> <q1,q2,...>
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
const [id, propsArq, pub, saida, escala, lista] = process.argv.slice(2);
const inputProps = JSON.parse(fs.readFileSync(propsArq, "utf8"));
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts"), publicDir: pub });
const comp = await selectComposition({ serveUrl, id, inputProps });
fs.mkdirSync(saida, { recursive: true });
for (const q of lista.split(",").map(Number)) {
  await renderStill({ composition: comp, serveUrl, output: path.join(saida, `q${String(q).padStart(5, "0")}.jpg`), frame: q, inputProps, imageFormat: "jpeg", jpegQuality: 80, scale: Number(escala) });
  process.stdout.write(`${q} `);
}
console.log("ok");
