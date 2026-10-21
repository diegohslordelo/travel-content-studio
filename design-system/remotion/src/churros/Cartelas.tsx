/**
 * Cartelas gráficas do Reel dos churros:
 * - Veredito: pausa tipográfica ("A gente prefere / O BRASILEIRO"), sobre cacau ou sobre o verde do Brasil.
 * - Comparação: os dois churros ilustrados lado a lado. Não há imagem do churro brasileiro no acervo,
 *   então os dois são desenho (ilustração assumida), nunca foto apresentada como nossa.
 * Tempos em ms relativos à Sequence.
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { kf, useMs } from "../ds/tempo";
import { C, CURVA, F } from "./tema";

const fundoCacau = `radial-gradient(110% 70% at 50% 45%, ${C.cacau2} 0%, ${C.cacau} 72%)`;

export type PaletaCartela = "cacau" | "colorido";

/** Cores das cartelas: "cacau" (REV1 de Barcelona) e "colorido" (verde e amarelo do Brasil × vermelho e amarelo da Espanha). */
const CORES = {
  cacau: {
    veredito: fundoCacau,
    acima: C.creme,
    principal: C.douradoClaro,
    faixa: [C.verdeBr, C.amareloBr],
    abaixo: C.creme2,
    esq: fundoCacau,
    dir: fundoCacau,
    divisoria: C.dourado,
    xFundo: C.cacau,
    xBorda: C.dourado,
    xTexto: C.douradoClaro,
    visto: C.douradoClaro,
    luz: "233,166,58",
  },
  colorido: {
    veredito: "radial-gradient(110% 75% at 50% 42%, #1DB45C 0%, #0F8A43 55%, #075E2D 100%)",
    acima: "#FFFFFF",
    principal: "#FFD43B",
    faixa: ["#FFD43B", "#1E4FD8"],
    abaixo: "rgba(255,255,255,.88)",
    esq: "linear-gradient(160deg, #1DB45C 0%, #0B7A3B 100%)",
    dir: "linear-gradient(200deg, #E5322D 0%, #A3111E 100%)",
    divisoria: "#FFFFFF",
    xFundo: "#FFFFFF",
    xBorda: "#FFD43B",
    xTexto: "#E5322D",
    visto: "#FFD43B",
    luz: "255,212,59",
  },
} as const;

export const Veredito: React.FC<{ dur: number; paleta?: PaletaCartela; abaixo?: string }> = ({ dur, paleta = "cacau", abaixo = "desculpa, Barcelona." }) => {
  const K = CORES[paleta];
  const t = useMs();
  const a = kf(t, [0, 480], [0, 1], CURVA.sai);
  const b = kf(t, [420, 900], [0, 1], CURVA.mola);
  const faixa = kf(t, [620, 1100], [0, 1], CURVA.sai);
  const c = kf(t, [1250, 1700], [0, 1], CURVA.sai);
  const saida = kf(t, [dur - 200, dur], [0, 1], CURVA.entra);
  // leve "respiração" do bloco depois do impacto
  const resp = 1 + 0.025 * kf(t, [900, dur], [0, 1], CURVA.suave);
  return (
    <AbsoluteFill style={{ background: K.veredito, alignItems: "center", justifyContent: "center" }}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", scale: String(resp), opacity: 1 - saida, marginTop: -120 }}>
        <div style={{ overflow: "hidden" }}>
          <div style={{ fontFamily: F.serifa, fontStyle: "italic", fontSize: 124, color: K.acima, translate: `0 ${(1 - a) * 100}%`, lineHeight: 1.05 }}>
            A gente prefere
          </div>
        </div>
        <div
          style={{
            fontFamily: F.cartaz,
            fontSize: 196,
            lineHeight: 1,
            color: K.principal,
            letterSpacing: "0.01em",
            scale: String(1.35 - 0.35 * b),
            opacity: Math.min(1, b * 2.5),
            marginTop: 8,
            textShadow: "0 10px 40px rgba(0,0,0,.45)",
            whiteSpace: "nowrap",
          }}
        >
          O BRASILEIRO
        </div>
        <div style={{ display: "flex", gap: 0, marginTop: 26, height: 14, width: 760, justifyContent: "center" }}>
          <div style={{ width: 380 * faixa, background: K.faixa[0], borderRadius: "7px 0 0 7px" }} />
          <div style={{ width: 380 * faixa, background: K.faixa[1], borderRadius: "0 7px 7px 0" }} />
        </div>
        <div
          style={{
            fontFamily: F.rotulo,
            fontWeight: 600,
            fontSize: 46,
            letterSpacing: "0.03em",
            color: K.abaixo,
            marginTop: 54,
            opacity: c,
            translate: `0 ${(1 - c) * 16}px`,
          }}
        >
          {abaixo}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- ilustrações

/** Churro em pé: corpo com estrias (estrela da massa), açúcar e, opcional, recheio aparente no topo. */
const Churro: React.FC<{ w: number; h: number; recheio?: boolean; id: string; acucar?: number }> = ({ w, h, recheio, id, acucar = 40 }) => {
  const estrias = 6;
  const pontos = Array.from({ length: acucar }, (_, i) => {
    const r = Math.sin(i * 12.9898 + w) * 43758.5453;
    const r2 = Math.sin(i * 78.233 + h) * 12345.678;
    return [(r - Math.floor(r)) * (w - 16) + 8, (r2 - Math.floor(r2)) * (h - 40) + 30] as [number, number];
  });
  return (
    <svg width={w} height={h + 40} viewBox={`0 -40 ${w} ${h + 40}`} style={{ overflow: "visible" }}>
      <defs>
        <linearGradient id={`massa-${id}`} x1="0" x2="1">
          <stop offset="0" stopColor="#9C5420" />
          <stop offset="0.35" stopColor="#E3A24A" />
          <stop offset="0.6" stopColor="#F2BE66" />
          <stop offset="1" stopColor="#A85E24" />
        </linearGradient>
        <clipPath id={`corpo-${id}`}>
          <rect x={0} y={0} width={w} height={h} rx={w * 0.42} />
        </clipPath>
      </defs>
      <rect x={0} y={0} width={w} height={h} rx={w * 0.42} fill={`url(#massa-${id})`} />
      <g clipPath={`url(#corpo-${id})`}>
        {Array.from({ length: estrias - 1 }, (_, i) => (
          <line key={i} x1={((i + 1) * w) / estrias} y1={0} x2={((i + 1) * w) / estrias} y2={h} stroke="rgba(110,52,16,.55)" strokeWidth={Math.max(2, w * 0.035)} />
        ))}
        {Array.from({ length: estrias - 1 }, (_, i) => (
          <line key={`l${i}`} x1={((i + 1) * w) / estrias + w * 0.05} y1={0} x2={((i + 1) * w) / estrias + w * 0.05} y2={h} stroke="rgba(255,226,160,.35)" strokeWidth={Math.max(1, w * 0.02)} />
        ))}
        {pontos.map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r={Math.max(1.6, w * 0.018)} fill="rgba(255,248,235,.85)" />
        ))}
      </g>
      {recheio && (
        <>
          <ellipse cx={w / 2} cy={10} rx={w * 0.47} ry={w * 0.2} fill="#8A4A1C" />
          <ellipse cx={w / 2} cy={10} rx={w * 0.3} ry={w * 0.12} fill="#C9792E" />
          <path d={`M${w * 0.32},14 C${w * 0.3},-30 ${w * 0.62},-46 ${w * 0.6},8 Z`} fill="#C9792E" />
          <path d={`M${w * 0.6},12 C${w * 0.66},40 ${w * 0.72},70 ${w * 0.66},92 C${w * 0.6},70 ${w * 0.56},40 ${w * 0.52},14 Z`} fill="#B86A28" />
        </>
      )}
    </svg>
  );
};

const Xicara: React.FC = () => (
  <svg width={230} height={190} viewBox="0 0 230 190">
    <path d="M15,40 L35,170 C38,182 48,188 60,188 L170,188 C182,188 192,182 195,170 L215,40 Z" fill={C.creme} />
    <path d="M195,70 C240,70 240,140 188,140" fill="none" stroke={C.creme} strokeWidth={16} />
    <ellipse cx={115} cy={40} rx={100} ry={26} fill={C.creme2} />
    <ellipse cx={115} cy={42} rx={88} ry={20} fill="#4B2716" />
    <ellipse cx={95} cy={38} rx={30} ry={6} fill="rgba(255,220,190,.25)" />
  </svg>
);

const Rotulo: React.FC<{ texto: string; cores: string[] }> = ({ texto, cores }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
    <div style={{ display: "flex", height: 10, width: 140, borderRadius: 5, overflow: "hidden" }}>
      {cores.map((c, i) => (
        <div key={i} style={{ flex: 1, background: c }} />
      ))}
    </div>
    <div style={{ fontFamily: F.cartaz, fontSize: 86, color: C.creme, letterSpacing: "0.02em", lineHeight: 1 }}>{texto}</div>
  </div>
);

export const Comparacao: React.FC<{ dur: number; paleta?: PaletaCartela; direita?: string; acucarDireita?: number }> = ({
  dur,
  paleta = "cacau",
  direita = "BARCELONA",
  acucarDireita = 22,
}) => {
  const K = CORES[paleta];
  const t = useMs();
  const esq = kf(t, [0, 620], [0, 1], CURVA.sai);
  const dir = kf(t, [220, 840], [0, 1], CURVA.sai);
  const x = kf(t, [380, 760], [0, 1], CURVA.mola);
  const visto = kf(t, [1350, 1800], [0, 1], CURVA.sai);
  const brilho = kf(t, [1350, 2000], [0, 1], CURVA.sai);
  const saida = kf(t, [dur - 260, dur], [0, 1], CURVA.entra);
  const flutua = (fase: number) => Math.sin((t / 1000) * 2 + fase) * 6;
  return (
    <AbsoluteFill style={{ background: fundoCacau, opacity: 1 - saida }}>
      {/* metades com as cores de cada lado (no "cacau" as duas são o próprio fundo) */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 540, height: 1920, background: K.esq, translate: `${(1 - esq) * -540}px 0` }} />
      <div style={{ position: "absolute", left: 540, top: 0, width: 540, height: 1920, background: K.dir, translate: `${(1 - dir) * 540}px 0` }} />
      {/* luz quente atrás do vencedor */}
      <div
        style={{
          position: "absolute",
          left: 270 - 320,
          top: 980 - 420,
          width: 640,
          height: 840,
          borderRadius: "50%",
          background: `radial-gradient(closest-side, rgba(${K.luz},${0.32 * brilho}), rgba(${K.luz},0))`,
        }}
      />
      <div style={{ position: "absolute", left: 540 - 1.5, top: 520, width: 3, height: 980 * x, background: `linear-gradient(${K.divisoria}, rgba(255,255,255,0))`, opacity: 0.6 }} />
      <div
        style={{
          position: "absolute",
          left: 540 - 56,
          top: 900,
          width: 112,
          height: 112,
          borderRadius: 56,
          background: K.xFundo,
          border: `3px solid ${K.xBorda}`,
          display: "grid",
          placeItems: "center",
          fontFamily: F.serifa,
          fontStyle: "italic",
          fontSize: 76,
          color: K.xTexto,
          scale: String(x),
        }}
      >
        ×
      </div>

      {/* BRASIL */}
      <div style={{ position: "absolute", left: 0, width: 540, top: 300, display: "flex", flexDirection: "column", alignItems: "center", translate: `${(1 - esq) * -260}px 0`, opacity: esq }}>
        <Rotulo texto="BRASIL" cores={[C.verdeBr, C.amareloBr]} />
        <div style={{ marginTop: 120, rotate: "-8deg", translate: `0 ${flutua(0)}px` }}>
          <Churro w={150} h={640} recheio id="br" acucar={70} />
        </div>
      </div>

      {/* destino (Barcelona, Madrid…) */}
      <div style={{ position: "absolute", left: 540, width: 540, top: 300, display: "flex", flexDirection: "column", alignItems: "center", translate: `${(1 - dir) * 260}px 0`, opacity: dir }}>
        <Rotulo texto={direita} cores={[C.amareloBr, C.vermelhoEs, C.amareloBr]} />
        <div style={{ position: "relative", marginTop: 120, width: 360, height: 700, translate: `0 ${flutua(1.7)}px` }}>
          <div style={{ position: "absolute", left: 92, top: 0, rotate: "-14deg" }}>
            <Churro w={62} h={520} id="es1" acucar={acucarDireita} />
          </div>
          <div style={{ position: "absolute", left: 150, top: -20, rotate: "-2deg" }}>
            <Churro w={62} h={540} id="es2" acucar={acucarDireita} />
          </div>
          <div style={{ position: "absolute", left: 208, top: 6, rotate: "11deg" }}>
            <Churro w={62} h={510} id="es3" acucar={acucarDireita} />
          </div>
          <div style={{ position: "absolute", left: 66, top: 470 }}>
            <Xicara />
          </div>
        </div>
      </div>

      {/* visto de caneta no vencedor */}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <path
          d="M150,1520 L230,1600 L400,1400"
          fill="none"
          stroke={K.visto}
          strokeWidth={22}
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={1}
          strokeDasharray="1 1"
          strokeDashoffset={1 - visto}
        />
      </svg>
    </AbsoluteFill>
  );
};
