/**
 * Render da composição `VideoLongo` (vídeo longo do YouTube) a partir das props de uma revisão.
 *
 *   node scripts/videolongo.mjs <props.json> <public-dir> quadros <saida-dir> <q1,q2,...>   PNGs de conferência (ESCALA=2: 4K)
 *   node scripts/videolongo.mjs <props.json> <public-dir> trecho  <saida.mp4> <q-ini> <q-fim> [escala]
 *   node scripts/videolongo.mjs <props.json> <public-dir> tudo    <saida.mp4> [escala]
 *
 * Imagem em H.264 (CRF 20) + os efeitos sonoros do Remotion; voz e música são mixadas depois pelo script da revisão.
 * `escala` < 1 gera a prévia leve (ex.: 0.667 → 1280 × 720); 2 gera o 4K (3840 × 2160).
 * X264_PRESET (ex.: veryfast) troca o preset do x264 (padrão do Remotion: medium) e CRF troca o CRF (padrão 20).
 * MAXRATE (ex.: 12M) limita a taxa do CRF (buffer = 2 × MAXRATE): com o grão do DS, o CRF puro pesa (a prévia 720p em
 * CRF 20 passava de 2 GB).
 * CONCURRENCY (padrão: nº de núcleos) e OFFTHREAD_CACHE_MB (cache de quadros do <OffthreadVideo>; padrão do Remotion:
 * metade da memória) seguram a memória do 4K: com os padrões, a máquina de 15 GB reiniciou no meio do render 4K
 * (provável falta de memória: no 1080p, o compositor sozinho passou de 5,8 GB).
 */
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "..");
const chrome = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell";
const browserExecutable = existsSync(chrome) ? chrome : null;

const [arqProps, publicDir, modo, saida, ...resto] = process.argv.slice(2);
const inputProps = JSON.parse(readFileSync(arqProps, "utf-8"));
// BUNDLE_DIR: reaproveita um bundle já feito (a pasta pública tem o proxy de GBs; copiar a cada render custa caro)
const pronto = process.env.BUNDLE_DIR && existsSync(path.join(process.env.BUNDLE_DIR, "index.html"));
const serveUrl = pronto
  ? process.env.BUNDLE_DIR
  : await bundle({ entryPoint: path.join(raiz, "src", "index.ts"), publicDir: path.resolve(publicDir), ...(process.env.BUNDLE_DIR ? { outDir: process.env.BUNDLE_DIR } : {}) });
// 10 min por quadro: antes do 1º quadro o Remotion copia o vídeo-fonte para o /tmp (proxy de 3,7 GB, fonte 4K de
// 4,7 GB), e os 30 s padrão (e até 3 min, com o disco ocupado) estouram
const comum = { serveUrl, browserExecutable, logLevel: "warn", inputProps, timeoutInMilliseconds: 600000 };
const codificacao = {
  codec: "h264",
  crf: Number(process.env.CRF ?? 20),
  ...(process.env.X264_PRESET ? { x264Preset: process.env.X264_PRESET } : {}),
  ...(process.env.MAXRATE ? { encodingMaxRate: process.env.MAXRATE, encodingBufferSize: `${parseFloat(process.env.MAXRATE) * 2}M` } : {}),
};
const composition = await selectComposition({ ...comum, id: "VideoLongo" });
const concurrency = Number(process.env.CONCURRENCY ?? Math.max(1, os.cpus().length));
const memoria = process.env.OFFTHREAD_CACHE_MB ? { offthreadVideoCacheSizeInBytes: Number(process.env.OFFTHREAD_CACHE_MB) * 1024 * 1024 } : {};
let ultimo = -1;
const progresso = ({ progress }) => {
  const p = Math.floor(progress * 100);
  if (p >= ultimo + 5) {
    ultimo = p;
    console.log(`  ${p}%`);
  }
};

if (modo === "quadros") {
  mkdirSync(saida, { recursive: true });
  for (const q of resto[0].split(",").map(Number)) {
    await renderStill({ ...comum, composition, frame: q, output: path.join(saida, `q${String(q).padStart(6, "0")}.png`), scale: Number(process.env.ESCALA ?? 1) });
    console.log("quadro", q);
  }
} else if (modo === "trecho") {
  const [ini, fim, escala = "1"] = resto;
  await renderMedia({ ...comum, composition, ...codificacao, enforceAudioTrack: true, outputLocation: saida, frameRange: [Number(ini), Number(fim)], scale: Number(escala), concurrency, ...memoria, onProgress: progresso });
} else if (modo === "tudo") {
  const [escala = "1"] = resto;
  await renderMedia({ ...comum, composition, ...codificacao, enforceAudioTrack: true, outputLocation: saida, scale: Number(escala), concurrency, ...memoria, onProgress: progresso });
} else {
  console.error("modo: quadros | trecho | tudo");
  process.exit(1);
}
console.log("ok", saida);
