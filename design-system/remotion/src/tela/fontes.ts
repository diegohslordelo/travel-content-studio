/**
 * Fontes da LINGUAGEM DO FORMATO tela dividida (docs/FORMATOS_REELS.md, 4 e 6): Anton (gancho, números) e Inter 800 (legenda).
 * Não são fontes do DS V2: valem do gancho até antes do CTA (decisão do Diego, 28/10/2026). Pacotes @fontsource (OFL 1.1).
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const ANTON = "Anton, Impact, sans-serif";
export const INTER = "Inter, Arial, sans-serif";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesFormato = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: "Anton", url: anton, weight: "400", display: "block" }),
      loadFont({ family: "Inter", url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};
