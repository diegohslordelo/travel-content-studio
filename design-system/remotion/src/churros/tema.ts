/**
 * Reel "Churros em Barcelona" (reels/churros-barcelona): identidade visual própria do vídeo.
 *
 * Decisão do Diego (21/10/2026): o DS V2 fica para vídeos do YouTube, capa de Reels e CTA. Este Reel
 * usa linguagem de gastronomia premium: paleta tirada do próprio assunto (cacau do chocolate, creme
 * da massa, dourado do churro frito) e tipografia de cartaz de cinema (Anton) com acento editorial
 * (Instrument Serif itálico). Os valores daqui valem só para este Reel; não são tokens da marca.
 */
import { loadFont } from "@remotion/fonts";
import { Easing } from "remotion";

import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import serifItal from "@fontsource/instrument-serif/files/instrument-serif-latin-400-italic.woff2";
import serifItalExt from "@fontsource/instrument-serif/files/instrument-serif-latin-ext-400-italic.woff2";
import inter600 from "@fontsource/inter/files/inter-latin-600-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const C = {
  cacau: "#1E120C",
  cacau2: "#2E1C13",
  cacau3: "#4A2E1F",
  chocolate: "#5B3422",
  creme: "#F7EBDA",
  creme2: "#E9D6BC",
  dourado: "#E9A63A",
  douradoClaro: "#F6C66B",
  canela: "#B4652B",
  // só na comparação Brasil × Barcelona
  verdeBr: "#1FA35B",
  amareloBr: "#FFD43B",
  vermelhoEs: "#D7263D",
} as const;

export const F = {
  cartaz: "Anton, 'Barlow Condensed', sans-serif",
  serifa: "'Instrument Serif', Georgia, serif",
  rotulo: "Inter, 'Barlow', sans-serif",
} as const;

let carregadas: Promise<unknown> | null = null;
export const carregarFontesChurros = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: "Anton", url: anton, weight: "400", display: "block" }),
      loadFont({ family: "Instrument Serif", url: serifItal, weight: "400", style: "italic", display: "block" }),
      loadFont({ family: "Instrument Serif", url: serifItalExt, weight: "400", style: "italic", display: "block" }),
      loadFont({ family: "Inter", url: inter600, weight: "600", display: "block" }),
      loadFont({ family: "Inter", url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};

/** Curvas do Reel: saída expo (entradas de texto), in-out suave (câmera) e in-expo (mergulhos). */
export const CURVA = {
  sai: Easing.bezier(0.16, 1, 0.3, 1),
  suave: Easing.bezier(0.45, 0, 0.55, 1),
  entra: Easing.bezier(0.7, 0, 0.84, 0),
  mola: Easing.bezier(0.34, 1.56, 0.64, 1),
} as const;

/** Margens de leitura no 1080 × 1920: fora da faixa da interface do Instagram (topo e base). */
export const SEGURO = { esq: 72, dir: 72, topo: 220, base: 1480 } as const;
