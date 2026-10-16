#!/usr/bin/env node
/**
 * Exporta o kit do DS V2 (6.1) a partir das composições do Remotion.
 *
 *   npm run kit:png                      PNGs do kit           → ../kit/png/
 *   npm run kit:mov                      animações genéricas   → ../kit/mov/ (ProRes 4444 com alfa, para o CapCut)
 *   npm run kit:mov -- Kit-Placa-Abertura '{"rotulo":"PRIMEIRO DIA EM","destino":"MADRID"}'
 *                                        uma composição com textos reais (cidade, hora, valor)
 *   npm run kit:catalogo                 catálogo com som      → ../kit/catalogo_ds_v2.mp4
 */
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..");
const kit = path.resolve(raiz, "..", "kit");
const chrome = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell";
const browserExecutable = existsSync(chrome) ? chrome : null;

// composição → arquivo. Só entram as que não dependem de dado de viagem (cidade, hora, valor).
const MOV = {
  "Kit-Placa-Marca": "PD_placa_marca_chegada_saida.mov",
  "Kit-Placa-Fechamento": "PD_placa_fechamento_nascer.mov",
  "Kit-Simbolo-Nascer": "PD_simbolo_1_nascer.mov",
  "Kit-Ticket-Surpreende": "PD_ticket_surpreende_subida.mov",
  "Kit-Varredura": "PD_transicao_varredura.mov",
  "Kit-Cinema": "PD_transicao_cinema.mov",
};
const PNG = {
  "PNG-Scrim-Base": "PD_scrim_base.png",
  "PNG-Varredura": "PD_varredura.png",
  "PNG-Brilho": "PD_brilho.png",
  "PNG-Placa-Marca": "PD_placa_marca.png",
  "PNG-Placa-Fechamento": "PD_placa_fechamento.png",
  "PNG-Carimbo-Perrengue": "PD_carimbo_perrengue.png",
  "PNG-Ticket-Surpreende": "PD_ticket_surpreende.png",
  "PNG-Bilhete-Vazio": "PD_bilhete_vazio.png",
};

const [modo, unica, propsJson] = process.argv.slice(2);
if (!["png", "mov", "catalogo"].includes(modo)) {
  console.error("uso: node scripts/kit.mjs png|mov|catalogo [composição] [props JSON]");
  process.exit(1);
}

console.log("empacotando…");
const serveUrl = await bundle({ entryPoint: path.join(raiz, "src", "index.ts") });
const comum = { serveUrl, browserExecutable, logLevel: "warn" };

const comp = async (id, inputProps = {}) => selectComposition({ ...comum, id, inputProps });

if (modo === "png") {
  mkdirSync(path.join(kit, "png"), { recursive: true });
  for (const [id, arq] of Object.entries(PNG)) {
    const composition = await comp(id);
    const output = path.join(kit, "png", arq);
    await renderStill({ ...comum, composition, output, imageFormat: "png" });
    console.log("✓", path.relative(raiz, output));
  }
}

if (modo === "mov") {
  mkdirSync(path.join(kit, "mov"), { recursive: true });
  const lista = unica ? { [unica]: `${unica.replace(/^Kit-/, "PD_").toLowerCase()}.mov` } : MOV;
  const inputProps = propsJson ? JSON.parse(propsJson) : {};
  for (const [id, arq] of Object.entries(lista)) {
    const composition = await comp(id, inputProps);
    const output = path.join(kit, "mov", arq);
    await renderMedia({
      ...comum,
      composition,
      inputProps,
      outputLocation: output,
      codec: "prores",
      proResProfile: "4444",
      imageFormat: "png",
      pixelFormat: "yuva444p10le",
      muted: true,
    });
    console.log("✓", path.relative(raiz, output));
  }
}

/** Loudness integrada e pico verdadeiro (ffmpeg ebur128). */
const medir = (arq) => {
  const r = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], { encoding: "utf8" });
  const i = [...r.stderr.matchAll(/I:\s+(-?[\d.]+) LUFS/g)].pop()[1];
  const p = [...r.stderr.matchAll(/Peak:\s+(-?[\d.]+) dBFS/g)].pop()[1];
  return [Number(i), Number(p)];
};

if (modo === "catalogo") {
  // Sem voz, o catálogo leva ganho linear até −16 LUFS e limitador de pico (sobreamostragem 4×), como o master do Reel.
  const composition = await comp("Catalogo");
  const bruto = path.join(kit, "_catalogo_bruto.mov");
  const output = path.join(kit, "catalogo_ds_v2.mp4");
  await renderMedia({ ...comum, composition, outputLocation: bruto, codec: "h264", crf: 20, audioCodec: "pcm-16" });
  const [i0] = medir(bruto);
  const ganho = -16 - i0;
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", bruto, "-c:v", "copy", "-af",
    `volume=${ganho.toFixed(2)}dB,aresample=192000,alimiter=limit=0.70:attack=1:release=60:level=false,aresample=48000`,
    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", output]);
  rmSync(bruto);
  const [i, tp] = medir(output);
  console.log("✓", path.relative(raiz, output), `${i} LUFS · pico ${tp} dBTP`);
}
