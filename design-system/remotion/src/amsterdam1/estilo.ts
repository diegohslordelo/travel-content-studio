/**
 * Reel "Primeiro dia em Amsterdam" (reels/amsterdam-primeiro-dia/): linguagem visual dos Reels do perfil
 * (docs/FORMATOS_REELS.md: Anton no gancho, Inter 800 na legenda, destaque âmbar, grão 6%), copiada sem mudança de valor.
 * Estas fontes e cores NÃO são do DS V2. O DS entra só no Placar (pedido do Diego para este Reel, 02/11/2026) e no CTA.
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const PALETA = {
  branco: "#FFFFFF",
  preto: "#0B0A09",
  ambar: "#E0AE5C",
} as const;

export const TITULO = "Anton";
export const TEXTO = "Inter";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesAMS = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({ family: TEXTO, url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};

/** Grade dos vídeos da viagem (FORMATOS_REELS.md, 2): tira o rosa saturado do HDR convertido. */
export const GRADE_VIDEO = "saturate(0.7) contrast(1.06) brightness(0.96)";

export const clamp = (x: number) => Math.min(1, Math.max(0, x));
export const ease = (p: number) => 1 - Math.pow(1 - clamp(p), 3);
export const easeIn = (p: number) => Math.pow(clamp(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));
