/**
 * Linguagem visual própria do Reel "Greves na Europa" (reels/greves-europa/rev1).
 *
 * Por pedido do Diego para esta peça, as cores do DS V2 ficam só nos componentes do sistema (Placa do CTA,
 * legenda Padrão com mini-placa, scrim e grão). Mapa, linha do tempo, cartelas e textos de impacto usam esta
 * paleta editorial, que conta a emoção do roteiro: alerta (vermelho-coral) → dúvida (laranja) → controle (verde-água).
 * Exceção desta peça: não vira regra da marca (CLAUDE.md, 4).
 */
import { createContext, useContext } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { FONTE } from "../ds/tokens";

export const ED = {
  tinta: "#0A0D14",
  tinta2: "#121826",
  painel: "rgba(10,13,20,0.84)",
  linha: "#2A3245",
  branco: "#F3F5F8",
  cinza: "#A7B0BF",
  cinzaEsc: "#5F697A",
  alerta: "#FF5544",
  alertaEsc: "#B8281C",
  duvida: "#FF9F43",
  calma: "#34D3A0",
  calmaEsc: "#0F7A5C",
  terra: "#1A2130",
  terraBorda: "#39445A",
  mar: "#0B1019",
} as const;

export const FONTE_ED = {
  impacto: FONTE.display,
  texto: FONTE.texto,
  mono: FONTE.mono,
} as const;

/** Sombra de texto para impacto sobre vídeo. */
export const SOMBRA_IMPACTO = "0 4px 0 rgba(0,0,0,.35), 0 0 40px rgba(0,0,0,.55)";

/** Margens da zona segura do Reel (DS V2, 1.3): x 72–944 · y 256–1440. */
export const SEG = { x0: 72, x1: 944, y0: 256, y1: 1440, centro: 540 } as const;

/**
 * Dentro de uma Sequence o quadro do Remotion é relativo ao início dela. As cenas embrulham o conteúdo em
 * `Deslocamento.Provider` com o início da Sequence (s), e `useSeg` devolve sempre os segundos absolutos.
 */
export const Deslocamento = createContext(0);

export const useSeg = (): number => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  return q / fps + useContext(Deslocamento);
};

/** Progresso 0 → 1 entre a e b (em segundos), com curva opcional. */
export const prog = (t: number, a: number, b: number, curva?: (x: number) => number): number => {
  const p = Math.min(1, Math.max(0, (t - a) / (b - a)));
  return curva ? curva(p) : p;
};
