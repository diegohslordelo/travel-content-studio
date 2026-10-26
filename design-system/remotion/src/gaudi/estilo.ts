/**
 * Reel do Gaudí (reel_gaudi/): mesma linguagem visual do Reel "Casa de Anne Frank" (reels/anne-frank, branch
 * claude/reel-anne-frank), copiada sem mudança de valor porque o Diego pediu (26/10/2026) o padrão dos Reels antigos
 * em tela dividida (medido em reel_gaudi/padrao.md). O DS V2 só entra no CTA final; estas fontes e cores NÃO são do DS.
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
  ambar: "#E0AE5C", // luz de lamparina: destaque das legendas e do caminho secreto
  cinza: "#7D776E",
} as const;

export const TITULO = "Anton"; // gancho, números e títulos: pesada e condensada
export const TEXTO = "Inter"; // legendas e rótulos

let carregadas: Promise<unknown> | null = null;
export const carregarFontesGaudi = () => {
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

/** Grade das imagens de apoio: cor contida, sem o rosa saturado do entardecer convertido do HDR. */
export const GRADE_VIDEO = "saturate(0.7) contrast(1.06) brightness(0.96)";
export const GRADE_FOTO = "grayscale(0.15) contrast(1.05)";

export const ease = (p: number) => 1 - Math.pow(1 - Math.min(1, Math.max(0, p)), 3);
export const easeInOut = (p: number) => {
  const x = Math.min(1, Math.max(0, p));
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Interpolação linear com trava nas pontas e curva opcional. */
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));
