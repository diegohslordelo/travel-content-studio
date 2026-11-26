/**
 * Reel de custos de Madrid (reels/madrid-custo/): mesma linguagem do Reel da Disney (src/disney, branch claude/new-session-a5toxu) e visual dos Reels do perfil nos formatos do Trello
 * (docs/FORMATOS_REELS.md), copiada sem mudança de valor: Anton no gancho, Inter 800 nas legendas, âmbar #E0AE5C.
 * Sem grade de cor e sem grão nos vídeos (pedido do Diego, 19/11/2026). O DS V2 só entra no CTA final; estas fontes e cores NÃO são do DS (CLAUDE.md, 6).
 */
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

export const COR = {
  branco: "#FFFFFF",
  preto: "#0B0A09",
  ambar: "#E0AE5C", // destaque das legendas do formato (FORMATOS_REELS.md, 6)
} as const;

export const TITULO = "Anton";
export const TEXTO = "Inter";

let carregadas: Promise<unknown> | null = null;
export const carregarFontesMadrid = () => {
  if (!carregadas) {
    carregadas = Promise.all([
      loadFont({ family: TITULO, url: anton, weight: "400", display: "block" }),
      loadFont({ family: TEXTO, url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return carregadas;
};

/* Sem grade de cor nos vídeos: o Diego pediu as imagens exatamente como estão no Drive (19/11/2026). */

export const clamp01 = (p: number) => Math.min(1, Math.max(0, p));
export const ease = (p: number) => 1 - Math.pow(1 - clamp01(p), 3);
export const easeIn = (p: number) => Math.pow(clamp01(p), 3);
export const easeInOut = (p: number) => {
  const x = clamp01(p);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
export const lerp = (t: number, t0: number, t1: number, v0: number, v1: number, curva: (p: number) => number = ease) =>
  v0 + (v1 - v0) * curva((t - t0) / (t1 - t0));
