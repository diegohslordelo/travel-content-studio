/**
 * Materiais e efeitos de base (DS V2, 1.4 e 4.5): grão do vídeo, fibra do papel,
 * scrim das legendas, desfoque direcional e vinheta.
 */
import React, { useId } from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { COR, EFEITO, OPAC, REEL } from "./tokens";

/** Grão 5% no vídeo inteiro (fixo: a intensidade não anima; o padrão muda a cada quadro, como grão real). */
export const Grao: React.FC<{ opacidade?: number }> = ({ opacidade = OPAC.grao }) => {
  const quadro = useCurrentFrame();
  const id = useId().replace(/:/g, "");
  return (
    <AbsoluteFill style={{ pointerEvents: "none", mixBlendMode: "overlay", opacity: opacidade }}>
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <filter id={`g${id}`} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={quadro % 97} stitchTiles="stitch" />
          <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.1 -0.3" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${id})`} />
      </svg>
    </AbsoluteFill>
  );
};

/** Fibra de papel 4% (fica dentro do objeto de papel, que precisa de position: relative e overflow hidden). */
export const Fibra: React.FC<{ opacidade?: number; semente?: number }> = ({ opacidade = OPAC.fibra, semente = 3 }) => {
  const id = useId().replace(/:/g, "");
  return (
    <svg
      style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: opacidade, mixBlendMode: "multiply", pointerEvents: "none", borderRadius: "inherit" }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <filter id={`f${id}`} x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={semente} stitchTiles="stitch" />
        <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.1 -0.3" />
      </filter>
      <rect width="100%" height="100%" filter={`url(#f${id})`} />
    </svg>
  );
};

/** Scrim inferior: grafite 0 → 63% de y 1150 a y 1500, 63% até a base (DS V2, 3.1). Sempre ligado nos Reels. */
export const ScrimBase: React.FC<{ opacidade?: number }> = ({ opacidade = 1 }) => {
  const topo = 1150;
  const cheio = 1500;
  const altura = REEL.altura - topo;
  const p = ((cheio - topo) / altura) * 100;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: topo,
        height: altura,
        opacity: opacidade,
        background: `linear-gradient(180deg, rgba(18,19,23,0) 0%, ${COR.scrim} ${p}%, ${COR.scrim} 100%)`,
        pointerEvents: "none",
      }}
    />
  );
};

/** Scrim superior a 63% (DS V2, 1.1: placa sobre fundo amarelo puro). */
export const ScrimTopo: React.FC = () => (
  <div
    style={{
      position: "absolute",
      left: 0,
      right: 0,
      top: 0,
      height: 520,
      background: `linear-gradient(0deg, rgba(18,19,23,0), ${COR.scrim})`,
      pointerEvents: "none",
    }}
  />
);

/** Vinheta 15%: só em plano emocional (Emocional / SURPREENDE). */
export const Vinheta: React.FC<{ opacidade?: number }> = ({ opacidade = 1 }) => (
  <AbsoluteFill
    style={{
      pointerEvents: "none",
      opacity: opacidade,
      background: `radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,${EFEITO.vinheta}) 100%)`,
    }}
  />
);

/**
 * Desfoque direcional horizontal (Chegada, saída da placa, Arrasto). CSS não tem blur direcional,
 * então é um filtro SVG com desvio só no eixo x.
 */
export const useDesfoqueX = (px: number): { defs: React.ReactNode; filter: string | undefined } => {
  const id = `dx${useId().replace(/:/g, "")}`;
  if (px < 0.05) return { defs: null, filter: undefined };
  return {
    defs: (
      <svg width="0" height="0" style={{ position: "absolute" }} aria-hidden>
        <filter id={id} x="-20%" y="-5%" width="140%" height="110%">
          <feGaussianBlur stdDeviation={`${px} 0`} />
        </filter>
      </svg>
    ),
    filter: `url(#${id})`,
  };
};
