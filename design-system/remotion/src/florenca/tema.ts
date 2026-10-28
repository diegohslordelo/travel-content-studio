/**
 * Reel "A multa que salvou o trem" (reels/florenca-multa): linguagem do formato Tela verde (docs/FORMATOS_REELS.md,
 * docs/REFERENCIA_EDICAO_FORMATOS.md). DS V2 só no CTA final (decisão do Diego, 28/10/2026): estas fontes e cores NÃO são do DS.
 * Mesma linguagem dos Reels Gaudí e Anne Frank (Anton + Inter, âmbar), com um vermelho de alerta para a multa e a fiscalização.
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter600 from "@fontsource/inter/files/inter-latin-600-normal.woff2";
import inter700 from "@fontsource/inter/files/inter-latin-700-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const COR = {
  branco: "#FFFFFF",
  papel: "#ECE5D8",
  fundo: "#14120F",
  ambar: "#E0AE5C",
  cinza: "#7D776E",
  alerta: "#E5484D", // multa, fiscalização, rota bloqueada (exceção desta peça)
  rio: "#2E3B47",
  ok: "#5FBF8A", // "paga a passagem"
} as const;

export const TITULO = "Anton";
export const TEXTO = "Inter";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesFlorenca = () => {
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

export const GRADE_VIDEO = "saturate(0.78) contrast(1.06) brightness(0.92)";

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const ease = (p: number) => 1 - Math.pow(1 - clamp(p), 3);
export const easeIn = (p: number) => Math.pow(clamp(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
/** Volta de mola curta (entrada de objeto que "assenta"). */
export const mola = (p: number) => {
  const x = clamp(p);
  return 1 - Math.exp(-6 * x) * Math.cos(10 * x);
};
/** v0 → v1 entre t0 e t1 (segundos), travado nas pontas. */
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));

export const SOMBRA_TEXTO = "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)";
