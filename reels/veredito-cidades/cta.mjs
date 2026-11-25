#!/usr/bin/env node
/**
 * Renderiza as placas do CTA (DS V2, Remotion) com fundo transparente, em _tmp/cta/.
 * Rode de dentro da pasta do Reel:  node cta.mjs
 * Usa o design-system/remotion (npm install feito lá) e a composições Kit-Placa-Abertura (CTA) e Kit-Placa-Marca (assinatura).
 */
import { createRequire } from "node:module";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const remotion = path.resolve(aqui, "..", "..", "design-system", "remotion");
const req = createRequire(path.join(remotion, "package.json"));
const { bundle } = req("@remotion/bundler");
const { renderMedia, selectComposition } = req("@remotion/renderer");

const chrome = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell";
const browserExecutable = existsSync(chrome) ? chrome : null;
const saida = path.join(aqui, "_tmp", "cta");
mkdirSync(saida, { recursive: true });

const serveUrl = await bundle({ entryPoint: path.join(remotion, "src", "index.ts") });
const comum = { serveUrl, browserExecutable, logLevel: "warn" };

const placas = [
  // CTA único (comentar): entra com a Chegada e sai.
  { arq: "placa_cta.mov", id: "Kit-Placa-Abertura", props: { rotulo: "ME CONTA SE", destino: "VOCÊ CONCORDA", saida: 2300 } },
  // Assinatura do perfil.
  { arq: "placa_perfil.mov", id: "Kit-Placa-Marca", props: { destino: "@PRIMEIRODIAEM" } },
];
for (const { arq, id, props } of placas) {
  const composition = await selectComposition({ ...comum, id, inputProps: props });
  await renderMedia({
    ...comum,
    composition: { ...composition, durationInFrames: arq === "placa_cta.mov" ? 78 : 75 },
    inputProps: props,
    outputLocation: path.join(saida, arq),
    codec: "prores",
    proResProfile: "4444",
    imageFormat: "png",
    pixelFormat: "yuva444p10le",
    muted: true,
  });
  console.log("✓", arq);
}
