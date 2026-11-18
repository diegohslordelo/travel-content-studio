/**
 * Reel "Erros de viagem" (reels/erros-de-viagem/rev1): linguagem do formato tela dividida (docs/FORMATOS_REELS.md).
 * Por decisão do Diego (28/10/2026), o DS V2 só entra no CTA final; estas fontes e cores são as do formato
 * (Anton, Inter, âmbar), não do DS, e não valem para outras peças sem decisão dele.
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter700 from "@fontsource/inter/files/inter-latin-700-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const PALETA = {
  branco: "#FFFFFF",
  papel: "#ECE5D8", // traço das animações
  preto: "#0B0A09",
  fundo: "#14120F",
  ambar: "#E0AE5C", // destaque das legendas e das animações
} as const;

export const TITULO = "Anton";
export const TEXTO = "Inter";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesErros = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({ family: TEXTO, url: inter700, weight: "700", display: "block" }),
      loadFont({ family: TEXTO, url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};

export const GRADE_FOTO = "grayscale(0.12) contrast(1.05)";
export const SOMBRA_TEXTO = "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)";

export const clamp01 = (p: number) => Math.min(1, Math.max(0, p));
export const ease = (p: number) => 1 - Math.pow(1 - clamp01(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp01(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Volta com leve passagem do alvo (entrada de número e de cartão). */
export const easeBack = (p: number) => {
  const x = clamp01(p);
  const c1 = 1.4;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
};
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));
