/**
 * Reel "Paris não quer você lá" (reels/paris-formigueiro/): linguagem do formato tela dividida (docs/FORMATOS_REELS.md),
 * a mesma do Reel de Bruges (Anton + Inter, destaque âmbar, grão 6%, serifa itálica na palavra-chave em dupla tipografia).
 * O DS V2 só entra no CTA final (decisão do Diego, 28/10/2026); estas fontes e cores NÃO são do DS.
 * Acréscimos deste Reel (QA_REV1): vermelho e branco da fita zebrada no gancho; vermelho só em "DÓI NA CONTA".
 */
import React from "react";
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter700 from "@fontsource/inter/files/inter-latin-700-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";
import cormorant from "@fontsource/cormorant-garamond/files/cormorant-garamond-latin-700-italic.woff2";

export const PALETA = {
  branco: "#FFFFFF",
  papel: "#ECE5D8", // traço das ilustrações
  preto: "#0B0A09",
  fundo: "#14120F", // fundo das animações
  ambar: "#E0AE5C", // ouro do relicário: destaque das legendas, mapas e animações
  vermelho: "#D63A2F", // fita zebrada do gancho e "DÓI NA CONTA"
  terra: "#211D18", // terra nos mapas
  mar: "#0E0D0B",
} as const;

export const TITULO = "Anton";
export const TEXTO = "Inter";
export const SERIFA = "Cormorant Garamond";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesParis = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({
        family: TEXTO,
        url: inter700,
        weight: "700",
        display: "block",
      }),
      loadFont({
        family: TEXTO,
        url: inter800,
        weight: "800",
        display: "block",
      }),
      loadFont({
        family: SERIFA,
        url: cormorant,
        weight: "700",
        style: "italic",
        display: "block",
      }),
    ]);
  }
  return carregadas;
};

/** Grade das imagens: cor contida, sem o rosa saturado do HDR convertido (FORMATOS_REELS 2). */
export const GRADE_VIDEO = "saturate(0.78) contrast(1.06) brightness(0.97)";
export const GRADE_FOTO = "grayscale(0.12) contrast(1.05)";
export const SOMBRA_TEXTO =
  "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)";

export const clamp = (x: number) => Math.min(1, Math.max(0, x));
export const ease = (p: number) => 1 - Math.pow(1 - clamp(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
export const lerp = (
  t: number,
  t0: number,
  t1: number,
  v0: number,
  v1: number,
  curva: (p: number) => number = ease,
) => v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));

/**
 * Ordinal legível em Anton: o "º" da fonte parece um zero ("1º" lia "10"). Aqui ele vira um "o" minúsculo,
 * alto e sublinhado, como se escreve à mão.
 */
export const comOrdinal = (texto: string): React.ReactNode => {
  const partes = texto.split("º");
  return partes.map((p, i) => (
    <React.Fragment key={i}>
      {p}
      {i < partes.length - 1 && (
        <span
          style={{
            display: "inline-block",
            fontSize: "0.5em",
            lineHeight: 1,
            verticalAlign: "top",
            marginTop: "0.18em",
            marginLeft: "0.04em",
            paddingBottom: "0.02em",
            borderBottom: "0.09em solid currentColor",
          }}
        >
          o
        </span>
      )}
    </React.Fragment>
  ));
};
