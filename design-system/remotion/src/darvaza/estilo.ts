/**
 * Reel da cratera de Darvaza (reels/darvaza-cratera/): mesma linguagem visual dos Reels em tela dividida do perfil
 * (Gaudí e Anne Frank; docs/FORMATOS_REELS.md), copiada sem mudança de valor. O DS V2 só entra no CTA final; estas
 * fontes e cores NÃO são do DS (CLAUDE.md, 6: DS só no CTA dos Reels).
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
  ambar: "#E0AE5C", // destaque das legendas e traço quente das ilustrações
  cinza: "#7D776E",
} as const;

export const TITULO = "Anton"; // gancho, números e títulos: pesada e condensada
export const TEXTO = "Inter"; // legendas e rótulos

let carregadas: Promise<unknown> | null = null;
export const carregarFontesDarvaza = () => {
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
/** Interpolação com trava nas pontas (o progresso fica entre 0 e 1 antes da curva) e curva opcional. */
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva(Math.min(1, Math.max(0, (t - t0) / (t1 - t0))));
