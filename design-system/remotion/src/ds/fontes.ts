/**
 * Fontes do DS V2 (1.2), carregadas dos pacotes @fontsource (OFL 1.1), sem rede no render.
 * Faltam no repositório: "PD Placar" (os tokens caem para Barlow Condensed, com algarismos
 * tabulares) e "Caneta Diego" (os tokens caem para Reenie Beanie). Pendências 1 e 7 do CLAUDE.md.
 */
import { loadFont } from "@remotion/fonts";

import bc300i from "@fontsource/barlow-condensed/files/barlow-condensed-latin-300-italic.woff2";
import bc600 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-600-normal.woff2";
import bc700 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-700-normal.woff2";
import bc800 from "@fontsource/barlow-condensed/files/barlow-condensed-latin-800-normal.woff2";
import bc800i from "@fontsource/barlow-condensed/files/barlow-condensed-latin-800-italic.woff2";
import b500 from "@fontsource/barlow/files/barlow-latin-500-normal.woff2";
import b700 from "@fontsource/barlow/files/barlow-latin-700-normal.woff2";
import mono500 from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2";
import reenie from "@fontsource/reenie-beanie/files/reenie-beanie-latin-400-normal.woff2";

const lista: { family: string; url: string; weight: string; style: "normal" | "italic" }[] = [
  { family: "Barlow Condensed", url: bc300i, weight: "300", style: "italic" },
  { family: "Barlow Condensed", url: bc600, weight: "600", style: "normal" },
  { family: "Barlow Condensed", url: bc700, weight: "700", style: "normal" },
  { family: "Barlow Condensed", url: bc800, weight: "800", style: "normal" },
  { family: "Barlow Condensed", url: bc800i, weight: "800", style: "italic" },
  { family: "Barlow", url: b500, weight: "500", style: "normal" },
  { family: "Barlow", url: b700, weight: "700", style: "normal" },
  { family: "IBM Plex Mono", url: mono500, weight: "500", style: "normal" },
  { family: "Reenie Beanie", url: reenie, weight: "400", style: "normal" },
];

let carregadas: Promise<unknown> | null = null;

export const carregarFontes = () => {
  if (!carregadas) {
    carregadas = Promise.all(
      lista.map((f) => loadFont({ family: f.family, url: f.url, weight: f.weight, style: f.style, display: "block" })),
    );
  }
  return carregadas;
};
