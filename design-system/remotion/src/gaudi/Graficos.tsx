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

/**
 * Bonde em traço (ilustração criada; não é foto nem o bonde do acidente): os prédios e os trilhos se desenham,
 * o bonde entra pela direita e freia no centro. Mesma geometria de reel_gaudi/imagens/criadas/bonde_ilustracao.svg.
 */
export const Bonde: React.FC<{ t: number; altura: number }> = ({ t, altura }) => {
  const traco = (ini: number, dur: number) => lerp(t, ini, ini + dur, 1, 0, easeInOut); // fração ainda não desenhada
  const entra = lerp(t, 0.05, 0.75, 760, 0, ease); // bonde desliza da direita e para
  const balanço = t > 0.75 ? Math.sin((t - 0.75) * 18) * 2.5 * Math.exp(-(t - 0.75) * 5) : 0;
  const rastro = lerp(t, 0.1, 0.5, 0, 1) * lerp(t, 0.7, 1.1, 1, 0);
  const escala = altura / 900;
  const L = 1800; // comprimento máximo de traço para o dasharray
  const linha = (d: string, p: number, extra: React.SVGProps<SVGPathElement> = {}) => (
    <path d={d} strokeDasharray={L} strokeDashoffset={L * p} {...extra} />
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <svg width={1080} height={900} viewBox="0 0 1080 900" style={{ position: "absolute", left: 0, top: (altura - 900 * escala) / 2, scale: String(escala), transformOrigin: "0 0" }}>
        <g fill="none" stroke={PALETA.papel} strokeLinecap="round" strokeLinejoin="round" opacity={0.32} strokeWidth={3}>
          {linha("M0 520 V250 H150 V520 M150 520 V210 H330 V520 M330 520 V270 H470 V520", traco(0, 0.6))}
          {linha("M610 520 V230 H790 V520 M790 520 V260 H930 V520 M930 520 V200 H1080", traco(0.1, 0.6))}
        </g>
        <g fill="none" stroke={PALETA.papel} strokeLinecap="round" strokeWidth={4}>
          {linha("M0 150 H1080", traco(0, 0.5), { strokeWidth: 3, opacity: 0.8 })}
          {linha("M0 742 H1080 M0 770 H1080", traco(0, 0.45))}
        </g>
        <g transform={`translate(${entra} ${balanço})`} fill="none" stroke={PALETA.papel} strokeLinecap="round" strokeLinejoin="round" strokeWidth={5}>
          <path d="M560 330 L690 152 M690 152 l18 0" strokeWidth={4} />
          <path d="M230 420 Q230 360 300 350 H860 Q930 360 930 420 V680 Q930 700 910 700 H250 Q230 700 230 680 Z" fill={PALETA.fundo} />
          <path d="M250 350 Q260 318 330 315 H830 Q900 318 910 350" fill={PALETA.fundo} />
          <path d="M500 315 h170 v-22 h-170z" strokeWidth={4} />
          <path d="M270 400 h90 v130 h-90z M380 400 h90 v130 h-90z M490 400 h90 v130 h-90z M600 400 h90 v130 h-90z M710 400 h90 v130 h-90z M820 400 h80 v130 h-80z" strokeWidth={4} />
          <path d="M230 560 H930" strokeWidth={4} />
          <path d="M232 585 H928" stroke={PALETA.ambar} strokeWidth={6} />
          {[340, 420, 740, 820].map((x) => (
            <g key={x} transform={`rotate(${(-(760 - entra) / 30) * 57.3} ${x} 712)`}>
              <circle cx={x} cy={712} r={30} />
              <line x1={x} y1={688} x2={x} y2={736} strokeWidth={3} />
            </g>
          ))}
          <circle cx={905} cy={625} r={14} stroke={PALETA.ambar} />
        </g>
        <g stroke={PALETA.papel} strokeLinecap="round" strokeWidth={4} opacity={0.45 * rastro} transform={`translate(${entra + 880} 0)`}>
          <path d="M60 470 H190 M90 520 H200 M40 610 H180 M110 660 H210" />
        </g>
      </svg>
    </div>
  );
};
