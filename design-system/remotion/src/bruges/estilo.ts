/**
 * Reel "Bruges não quer você lá" (reels/bruges-bate-volta/): linguagem do formato tela dividida
 * (docs/FORMATOS_REELS.md), a mesma dos Reels Anne Frank e Gaudí, sem valor novo. O DS V2 só entra no CTA final.
 * Estas fontes e cores NÃO são do DS (CLAUDE.md, 6: DS só no CTA dos Reels).
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter600 from "@fontsource/inter/files/inter-latin-600-normal.woff2";
import inter700 from "@fontsource/inter/files/inter-latin-700-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const PALETA = {
  branco: "#FFFFFF",
  papel: "#ECE5D8", // traço das ilustrações
  preto: "#0B0A09",
  fundo: "#14120F", // fundo das animações
  ambar: "#E0AE5C", // destaque das legendas, rotas e números
  cinza: "#7D776E",
} as const;

export const TITULO = "Anton"; // gancho, números e títulos
export const TEXTO = "Inter"; // legendas e rótulos

let carregadas: Promise<unknown> | null = null;
export const carregarFontesBruges = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({ family: TEXTO, url: inter600, weight: "600", display: "block" }),
      loadFont({ family: TEXTO, url: inter700, weight: "700", display: "block" }),
      loadFont({ family: TEXTO, url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};

/** Grade das imagens de apoio (FORMATOS_REELS, 2). */
export const GRADE_VIDEO = "saturate(0.7) contrast(1.06) brightness(0.96)";
export const GRADE_FOTO = "grayscale(0.15) contrast(1.05)";
/** REV2: cor natural (o Diego achou as imagens apagadas com a grade de dessaturação). */
export const GRADE_NATURAL = "contrast(1.03)";

export const clamp01 = (p: number) => Math.min(1, Math.max(0, p));
export const ease = (p: number) => 1 - Math.pow(1 - clamp01(p), 3);
export const easeIn = (p: number) => Math.pow(clamp01(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp01(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Sobe com um passo além do alvo e assenta (entrada de objeto que "bate"). */
export const easeBack = (p: number) => {
  const x = clamp01(p);
  const c1 = 1.9;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
};
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));
