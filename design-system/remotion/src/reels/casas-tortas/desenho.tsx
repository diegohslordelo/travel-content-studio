/**
 * Desenho animado do Reel "As casas que dançam" (AMS-casas-tortas, REV1). Peças de ilustração: casa de
 * canal (5 tipos de empena), água, sofá, mão e sol. É ilustração deste Reel, não componente da marca:
 * usa só cores e traço do DS V2 (papel, grafite, asfalto, concreto, recibo e amarelo), sem valor visual novo.
 */
import React from "react";
import { COR } from "../../ds/tokens";

/** Traço do desenho: 6 px a 1080 px, o mesmo peso do traço de caneta (DS 1.6), em grafite. */
export const TRACO = 6;
export const LINHA = COR.grafite;

export type Empena = "degrau" | "pescoco" | "sino" | "bico" | "reta";

export type CasaDesenho = {
  w: number;
  /** altura do corpo (até a cornija) */
  hb: number;
  /** altura da empena */
  hg: number;
  tipo: Empena;
  cor: string;
  /** viga de içar com gancho no alto (vista de frente) */
  viga?: boolean;
};

const ESCURAS = [COR.grafite, COR.grafite800, COR.grafite700, COR.asfalto];

/** Contorno da casa com a origem no meio da base (y para cima é negativo). */
export const silhueta = ({ w, hb, hg, tipo }: CasaDesenho): string => {
  const a = w / 2;
  const topo = -hb - hg;
  switch (tipo) {
    case "degrau": {
      const s = w * 0.11;
      const d = hg / 3;
      const pts = [
        [-a, 0], [-a, -hb], [-a + s, -hb], [-a + s, -hb - d], [-a + 2 * s, -hb - d], [-a + 2 * s, -hb - 2 * d],
        [-a + 3 * s, -hb - 2 * d], [-a + 3 * s, topo], [a - 3 * s, topo], [a - 3 * s, -hb - 2 * d], [a - 2 * s, -hb - 2 * d],
        [a - 2 * s, -hb - d], [a - s, -hb - d], [a - s, -hb], [a, -hb], [a, 0],
      ];
      return "M" + pts.map((p) => p.join(" ")).join(" L") + " Z";
    }
    case "pescoco": {
      const n = w * 0.24;
      const ombro = -hb - hg * 0.55;
      return (
        `M${-a} 0 L${-a} ${-hb} C${-a + w * 0.12} ${-hb} ${-n} ${-hb - hg * 0.2} ${-n} ${ombro} ` +
        `L${-n} ${-hb - hg * 0.78} L${-n - 10} ${-hb - hg * 0.78} L0 ${topo} L${n + 10} ${-hb - hg * 0.78} L${n} ${-hb - hg * 0.78} ` +
        `L${n} ${ombro} C${n} ${-hb - hg * 0.2} ${a - w * 0.12} ${-hb} ${a} ${-hb} L${a} 0 Z`
      );
    }
    case "sino": {
      const n = w * 0.2;
      return (
        `M${-a} 0 L${-a} ${-hb} C${-a + w * 0.1} ${-hb - hg * 0.15} ${-n - 6} ${-hb - hg * 0.25} ${-n} ${-hb - hg * 0.62} ` +
        `C${-n + 4} ${topo - 8} ${n - 4} ${topo - 8} ${n} ${-hb - hg * 0.62} ` +
        `C${n + 6} ${-hb - hg * 0.25} ${a - w * 0.1} ${-hb - hg * 0.15} ${a} ${-hb} L${a} 0 Z`
      );
    }
    case "bico":
      return `M${-a} 0 L${-a} ${-hb} L${-a + 8} ${-hb} L0 ${topo} L${a - 8} ${-hb} L${a} ${-hb} L${a} 0 Z`;
    default: {
      const c = hg * 0.35;
      return `M${-a} 0 L${-a} ${-hb - c} L${-a - 10} ${-hb - c} L${-a - 10} ${-hb - c - 18} L${a + 10} ${-hb - c - 18} L${a + 10} ${-hb - c} L${a} ${-hb - c} L${a} 0 Z`;
    }
  }
};

const Janela: React.FC<{ x: number; y: number; w: number; h: number; escura: boolean }> = ({ x, y, w, h, escura }) => (
  <g>
    <rect x={x} y={y} width={w} height={h} rx={3} fill={COR.grafite800} stroke={escura ? COR.recibo : LINHA} strokeWidth={5} />
    <path d={`M${x + w / 2} ${y} V${y + h} M${x} ${y + h * 0.45} H${x + w}`} stroke={COR.recibo} strokeWidth={3} opacity={0.85} />
  </g>
);

/** Casa de canal de frente: corpo + empena, janelas brancas, porta e (opcional) a viga com o gancho. */
export const Casa: React.FC<{ casa: CasaDesenho }> = ({ casa }) => {
  const { w, hb, hg, tipo, cor, viga } = casa;
  const escura = ESCURAS.includes(cor);
  const terreo = 150;
  const n = Math.max(2, Math.round((hb - terreo) / 140));
  const hA = (hb - terreo) / n;
  const cols = w > 180 ? 3 : 2;
  const margem = w * 0.15;
  const vao = w * 0.1;
  const ww = (w - 2 * margem - (cols - 1) * vao) / cols;
  const wh = hA * 0.58;
  const janelas: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    for (let c = 0; c < cols; c++) {
      janelas.push(<Janela key={`${i}-${c}`} x={-w / 2 + margem + c * (ww + vao)} y={-hb + i * hA + hA * 0.22} w={ww} h={wh} escura={escura} />);
    }
  }
  const topo = -hb - hg;
  const sotao = tipo !== "reta" && tipo !== "bico";
  return (
    <g>
      <path d={silhueta(casa)} fill={cor} stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" />
      {janelas}
      {/* térreo: porta e uma janela */}
      <rect x={-w / 2 + margem} y={-terreo + 34} width={w * 0.24} height={terreo - 34} rx={4} fill={COR.grafite800} stroke={escura ? COR.recibo : LINHA} strokeWidth={5} />
      <Janela x={w / 2 - margem - w * 0.32} y={-terreo + 34} w={w * 0.32} h={terreo * 0.48} escura={escura} />
      {/* porta do sótão (por onde entra a mudança) */}
      {sotao && <Janela x={-w * 0.09} y={-hb - hg * 0.48} w={w * 0.18} h={hg * 0.32} escura={escura} />}
      {viga && (
        <g>
          <rect x={-11} y={topo + hg * 0.1} width={22} height={26} rx={3} fill={COR.recibo} stroke={LINHA} strokeWidth={5} />
          <path d={`M0 ${topo + hg * 0.1 + 26} V${topo + hg * 0.1 + 52} q0 14 -12 12`} fill="none" stroke={LINHA} strokeWidth={5} strokeLinecap="round" />
        </g>
      )}
    </g>
  );
};

/** Água do canal: grafite com reflexos curtos de papel que andam devagar. */
export const Agua: React.FC<{ y: number; t: number; altura?: number }> = ({ y, t, altura = 1920 }) => {
  const linhas = [
    [120, 60, 120], [520, 110, 160], [860, 70, 110], [300, 190, 90], [700, 250, 140], [80, 320, 100],
    [480, 380, 130], [900, 430, 90], [220, 520, 150], [640, 600, 110],
  ];
  return (
    <g>
      <rect x={0} y={y} width={1080} height={altura - y} fill={COR.grafite} />
      {linhas
        .filter(([, dy]) => y + dy < altura - 20)
        .map(([x, dy, l], i) => {
          const dx = Math.sin(t / 900 + i * 1.7) * 22;
          return <line key={i} x1={x + dx} y1={y + dy} x2={x + dx + l} y2={y + dy} stroke={COR.recibo} strokeOpacity={0.2} strokeWidth={4} strokeLinecap="round" />;
        })}
    </g>
  );
};

/** Sofá de frente (a mudança que sobe pelo gancho), 190 × 130, origem no meio do topo do encosto. */
export const Sofa: React.FC = () => (
  <g stroke={LINHA} strokeWidth={5} strokeLinejoin="round">
    <rect x={-80} y={0} width={160} height={58} rx={12} fill={COR.amarelo300} />
    <rect x={-95} y={44} width={190} height={58} rx={10} fill={COR.amarelo} />
    <rect x={-95} y={30} width={30} height={80} rx={10} fill={COR.amarelo} />
    <rect x={65} y={30} width={30} height={80} rx={10} fill={COR.amarelo} />
    <path d="M-80 110 v18 M80 110 v18" strokeWidth={8} strokeLinecap="round" />
  </g>
);

/** Mão que empurra: manga grafite, punho de papel e o indicador apontando para +x (origem na ponta do dedo). */
export const Mao: React.FC = () => (
  <g stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" strokeLinecap="round">
    <rect x={-640} y={-62} width={380} height={124} rx={20} fill={COR.grafite800} />
    <rect x={-276} y={-70} width={44} height={140} rx={12} fill={COR.recibo} />
    <path
      d="M-236 -60 C-190 -78 -140 -70 -112 -44 L-18 -42 C10 -42 10 -2 -18 -2 L-100 -2 C-92 22 -98 40 -112 52 C-140 74 -196 74 -236 64 Z"
      fill={COR.papel}
    />
    <path d="M-112 -2 C-120 10 -150 12 -168 6 M-104 24 C-118 32 -146 34 -164 28" fill="none" strokeWidth={4} />
  </g>
);

/** Sol do desenho (passagem do tempo): amarelo com contorno grafite. */
export const Sol: React.FC<{ x: number; y: number; r?: number }> = ({ x, y, r = 46 }) => (
  <g>
    <circle cx={x} cy={y} r={r} fill={COR.amarelo} stroke={LINHA} strokeWidth={TRACO} />
    {Array.from({ length: 8 }, (_, i) => {
      const a = (i * Math.PI) / 4;
      return (
        <line key={i} x1={x + Math.cos(a) * (r + 14)} y1={y + Math.sin(a) * (r + 14)} x2={x + Math.cos(a) * (r + 34)} y2={y + Math.sin(a) * (r + 34)}
          stroke={LINHA} strokeWidth={5} strokeLinecap="round" />
      );
    })}
  </g>
);
