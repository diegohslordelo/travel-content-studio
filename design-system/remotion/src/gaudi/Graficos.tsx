/**
 * Animações do Reel do Gaudí: data em tela cheia (padrão "AGOSTO DE 1944" do Reel Anne Frank), a fração "1/4"
 * da igreja pronta e a comparação das duas fotos de Gaudí. Só texto que está na fala; paleta e fontes de estilo.ts.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { GRADE_FOTO, PALETA, TITULO, ease, easeInOut, lerp } from "./estilo";

/** Data em tela cheia, linha a linha subindo de trás de uma máscara (igual ao Reel Anne Frank). */
export const Data: React.FC<{ t: number; linhas: string[]; fundo?: string }> = ({ t, linhas, fundo }) => (
  <div style={{ position: "absolute", inset: 0, background: PALETA.preto }}>
    {fundo && (
      <Img
        src={staticFile(fundo)}
        style={{ position: "absolute", inset: 0, width: 1080, height: 1920, objectFit: "cover", filter: "grayscale(1) brightness(0.32) contrast(1.1)", scale: String(lerp(t, 0, 3, 1.04, 1.0, (x) => x)) }}
      />
    )}
    <div style={{ position: "absolute", left: 72, top: 510 }}>
      {linhas.map((l, i) => {
        const p = lerp(t, 0.05 + i * 0.18, 0.55 + i * 0.18, 0, 1);
        return (
          // máscara com folga de 50 px em cima: o acento de "TRÊS" fica acima da altura das maiúsculas
          <div key={l} style={{ overflow: "hidden", height: 300, marginTop: i ? -50 : 0 }}>
            <div style={{ font: `400 250px ${TITULO}`, lineHeight: 1, paddingTop: 50, color: PALETA.branco, translate: `0 ${(1 - p) * 300}px` }}>{l}</div>
          </div>
        );
      })}
    </div>
  </div>
);

/** "1/4": a igreja pronta quando ele morreu. Um círculo de traço com 1/4 em âmbar e o número grande. */
export const Fracao: React.FC<{ t: number; fundo?: string; marco: number }> = ({ t, fundo, marco }) => {
  const r = 230;
  const cx = 540;
  const cy = 700;
  const p = lerp(t, marco - 0.1, marco + 0.55, 0, 1, easeInOut); // o quarto enche quando "quarto" é dito
  const ang = -Math.PI / 2 + p * (Math.PI / 2);
  const x1 = cx + r * Math.cos(ang);
  const y1 = cy + r * Math.sin(ang);
  const contorno = lerp(t, 0, 0.45, 0, 1);
  const circ = 2 * Math.PI * r;
  const n = lerp(t, marco - 0.05, marco + 0.25, 0, 1);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.preto }}>
      {fundo && (
        <Img
          src={staticFile(fundo)}
          style={{ position: "absolute", inset: 0, width: 1080, height: 1920, objectFit: "cover", filter: "grayscale(1) brightness(0.3) contrast(1.1)", scale: String(lerp(t, 0, 3, 1.0, 1.05, (x) => x)) }}
        />
      )}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={PALETA.papel} strokeWidth={6} strokeDasharray={circ} strokeDashoffset={circ * (1 - contorno)} transform={`rotate(-90 ${cx} ${cy})`} opacity={0.85} />
        {p > 0 && <path d={`M ${cx} ${cy} L ${cx} ${cy - r} A ${r} ${r} 0 0 1 ${x1} ${y1} Z`} fill={PALETA.ambar} opacity={0.95} />}
        <line x1={cx} y1={cy - r} x2={cx} y2={cy + r} stroke={PALETA.papel} strokeWidth={3} opacity={0.35 * contorno} />
        <line x1={cx - r} y1={cy} x2={cx + r} y2={cy} stroke={PALETA.papel} strokeWidth={3} opacity={0.35 * contorno} />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 990, textAlign: "center", font: `400 230px ${TITULO}`, lineHeight: 1, color: PALETA.branco, opacity: n, scale: String(0.92 + 0.08 * n) }}>
        1/4
      </div>
    </div>
  );
};

/** As duas fotos de Gaudí lado a lado: a de 1878 primeiro; a de 1924 entra no marco ("se desligou de aparência"). */
export const Comparar: React.FC<{ t: number; altura: number; a: string; b: string; marco: number; focoA?: [number, number]; focoB?: [number, number] }> = ({
  t,
  altura,
  a,
  b,
  marco,
  focoA = [0.5, 0.3],
  focoB = [0.5, 0.3],
}) => {
  const w = 540;
  const pb = lerp(t, marco - 0.1, marco + 0.35, 0, 1);
  const za = lerp(t, 0, 4, 1.02, 1.08, (x) => x);
  const quadro = (src: string, foco: [number, number], z: number, filtro: string): React.ReactNode => (
    <Img
      src={staticFile(src)}
      style={{ width: w, height: altura, objectFit: "cover", objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`, scale: String(z), transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`, filter: filtro }}
    />
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.preto, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: lerp(pb, 0, 1, 270, 0, (x) => x), top: 0, width: w, height: altura, overflow: "hidden" }}>
        {quadro(a, focoA, za, GRADE_FOTO)}
      </div>
      <div style={{ position: "absolute", left: w, top: 0, width: w, height: altura, overflow: "hidden", opacity: ease(pb), translate: `${(1 - pb) * 80}px 0` }}>
        {quadro(b, focoB, za, "grayscale(1) contrast(1.08) brightness(0.92)")}
      </div>
      <div style={{ position: "absolute", left: w - 3, top: 0, width: 6, height: altura, background: "rgba(0,0,0,0.55)", opacity: pb }} />
    </div>
  );
};
