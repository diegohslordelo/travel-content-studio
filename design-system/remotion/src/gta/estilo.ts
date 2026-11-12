/**
 * Reel GTA 6 × Miami (reels/gta6-miami): linguagem visual do formato tela dividida, com as cores temáticas do
 * GTA VI (pôr do sol de Vice City: amarelo → laranja → rosa → roxo, néon rosa e ciano), a pedido do Diego (12/11/2026,
 * só neste Reel). NÃO são cores nem fontes do DS V2: o DS entra só no CTA final (placa + clack).
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter700 from "@fontsource/inter/files/inter-latin-700-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";
import inter900 from "@fontsource/inter/files/inter-latin-900-normal.woff2";

export const VC = {
  noite: "#120A24",
  noite2: "#2A0F45",
  roxo: "#6A2BB0",
  lilas: "#B16CFF",
  rosa: "#FF3D9A",
  rosaClaro: "#FF8CC8",
  laranja: "#FF8A3D",
  amarelo: "#FFD166",
  ciano: "#2EE6E0",
  branco: "#FFFFFF",
  preto: "#07040D",
} as const;

/** Pôr do sol do GTA VI, de cima para baixo. */
export const PORDOSOL = `linear-gradient(180deg, ${VC.amarelo} 0%, ${VC.laranja} 32%, ${VC.rosa} 66%, ${VC.roxo} 100%)`;
export const PORDOSOL_H = `linear-gradient(90deg, ${VC.laranja} 0%, ${VC.rosa} 50%, ${VC.lilas} 100%)`;

export const TITULO = "Anton";
export const TEXTO = "Inter";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesGta = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({ family: TEXTO, url: inter700, weight: "700", display: "block" }),
      loadFont({ family: TEXTO, url: inter800, weight: "800", display: "block" }),
      loadFont({ family: TEXTO, url: inter900, weight: "900", display: "block" }),
    ]);
  }
  return carregadas;
};

export const clamp01 = (p: number) => Math.min(1, Math.max(0, p));
export const ease = (p: number) => 1 - Math.pow(1 - clamp01(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp01(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Saída com passagem do ponto (para "pop" de texto e ícones): 0 → 1,12 → 1. */
export const pop = (p: number) => {
  const x = clamp01(p);
  return x < 0.6 ? ease(x / 0.6) * 1.12 : 1.12 - 0.12 * easeInOut((x - 0.6) / 0.4);
};
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));

/** Sombra dos textos sobre imagem. */
export const SOMBRA_TXT = "0 4px 0 rgba(0,0,0,0.35), 0 6px 28px rgba(0,0,0,0.75)";
