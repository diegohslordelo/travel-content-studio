/**
 * Selo PERRENGUE, o Carimbo (DS V2, 2.2). Tinta vermelha com falha (~12% sem tinta) sobre recorte
 * de papel, borda dupla, triângulo "!", PERRENGUE em Condensed 800 96 px e data em Plex Mono 28 px.
 * Assinatura BATIDA: cai de 1,6× (ease-drop), impacto aos 160 ms com tremor de 2 quadros na cena,
 * assenta, a tinta espalha e a data é impressa letra a letra. No máximo 1 por Reel.
 */
import React from "react";
import { useVideoConfig } from "remotion";
import { Fibra } from "./material";
import { Alerta } from "./icones";
import { kf, useMs } from "./tempo";
import { COR, DUR, EASE, EFEITO, FONTE, RAIO, ROT, SOMBRA } from "./tokens";

/** Máscara de falha da tinta (implementação de prévia, pd-bundle.css --pd-inkmask). */
const MASCARA_TINTA =
  "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='m'><feTurbulence type='fractalNoise' baseFrequency='.55' numOctaves='3' seed='7' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -5 4'/></filter><rect width='100%' height='100%' filter='url(%23m)'/></svg>\")";

export type CarimboProps = {
  palavra?: string;
  /** Data e hora do registro real: "DIA 1 · 13H52 · ROMA". */
  data: string;
  x?: number;
  y?: number;
  /** ms em que a queda começa (o impacto é 160 ms depois). */
  entrada?: number;
  saida?: number;
};

export const Carimbo: React.FC<CarimboProps> = ({ palavra = "PERRENGUE", data, x = 420, y = 900, entrada = 0, saida }) => {
  const agora = useMs();
  const t = agora - entrada;
  const ts = saida === undefined ? -Infinity : agora - saida;
  if (t < 0 || ts >= DUR.fast) return null;
  const escala = t < 160 ? kf(t, [0, 160], [1.6, 0.96], EASE.drop) : kf(t, [160, 260], [0.96, 1], EASE.out);
  const opac = kf(t, [0, 160], [0, 1], EASE.drop) * kf(ts, [0, DUR.fast], [1, 0], EASE.exit);
  const tinta = kf(t, [160, 260], [2, 0], EASE.out);
  const sombraFirme = kf(t, [0, 160], [0, 1], EASE.drop);
  const dataRevela = kf(t, [260, 500], [0, 100]);
  const rot = ROT.carimbo + kf(ts, [0, DUR.fast], [0, -5], EASE.exit);
  const sobe = kf(ts, [0, DUR.fast], [0, -40], EASE.exit);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        padding: 20,
        background: COR.papel,
        borderRadius: RAIO.papel,
        overflow: "hidden",
        rotate: `${rot}deg`,
        translate: `0 ${sobe}px`,
        scale: String(escala),
        opacity: opac,
        boxShadow: sombraFirme > 0.99 ? SOMBRA.papel : `0 1px 1px rgba(0,0,0,${0.2 * sombraFirme}), 0 ${14 + 30 * (1 - sombraFirme)}px ${26 + 40 * (1 - sombraFirme)}px -10px rgba(0,0,0,${0.5 * sombraFirme})`,
      }}
    >
      <Fibra semente={5} />
      <div
        style={{
          position: "relative",
          color: COR.vermelho,
          border: "6px solid currentColor",
          boxShadow: `inset 0 0 0 6px ${COR.papel}, inset 0 0 0 9px currentColor`,
          padding: "24px 34px 18px",
          WebkitMaskImage: MASCARA_TINTA,
          maskImage: MASCARA_TINTA,
          WebkitMaskSize: "260px 260px",
          opacity: 0.92,
          filter: tinta > 0.05 ? `blur(${tinta}px)` : undefined,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
          <Alerta tamanho={78} cor="currentColor" />
          <span style={{ fontFamily: FONTE.display, fontWeight: 800, fontSize: 96, lineHeight: 0.9, letterSpacing: "0.04em", textTransform: "uppercase" }}>
            {palavra}
          </span>
        </div>
        <div
          style={{
            fontFamily: FONTE.mono,
            fontWeight: 500,
            fontSize: 28,
            lineHeight: 1,
            letterSpacing: "0.06em",
            textAlign: "center",
            marginTop: 14,
            paddingTop: 12,
            borderTop: "3px solid currentColor",
            whiteSpace: "nowrap",
            clipPath: `inset(0 ${100 - dataRevela}% 0 0)`,
          }}
        >
          {data}
        </div>
      </div>
    </div>
  );
};

/**
 * Efeito da Batida na CENA (aplicar no contêiner do vídeo): escurece 8% nos 60 ms antes da queda
 * (antecipação) e treme 2 quadros no impacto (±6 px, depois ±3 px).
 */
export const useBatidaNaCena = (entrada: number): { filter?: string; translate?: string } => {
  const t = useMs() - entrada;
  const { fps } = useVideoConfig();
  const q = 1000 / fps;
  const out: { filter?: string; translate?: string } = {};
  const escuro = t >= -60 && t < 160 ? kf(t, [-60, 0, 160], [0, 0.08, 0]) : 0;
  if (escuro > 0) out.filter = `brightness(${1 - escuro})`;
  if (t >= 160 && t < 160 + q) out.translate = `${EFEITO.tremor1}px ${-EFEITO.tremor1 * 0.66}px`;
  else if (t >= 160 + q && t < 160 + 2 * q) out.translate = `${-EFEITO.tremor2}px ${EFEITO.tremor2 * 0.66}px`;
  return out;
};
