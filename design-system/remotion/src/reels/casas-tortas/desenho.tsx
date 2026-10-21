/**
 * Desenho animado do Reel "As casas que dançam" (AMS-casas-tortas, REV1). Ilustração deste Reel, colorida
 * com as cores reais das casas de Amsterdam (decisão do Diego, 21/10/2026: o DS V2 vale para os componentes
 * de vídeo; a paleta desta animação é livre). Legendas, transições e CTA continuam no DS.
 */
import React from "react";

/** Paleta da ilustração: tijolo, cerâmica, caixilho branco, canal, céu, madeira e terra. */
export const PAL = {
  contorno: "#2A1D18",
  ceuTopo: "#6FB1DE",
  ceuBase: "#D6ECF7",
  nuvem: "#FFFFFF",
  tijolo: "#A2432E",
  tijoloClaro: "#B9583D",
  tijoloEscuro: "#7C3122",
  marrom: "#5C3B2D",
  escura: "#2E3A38",
  ocre: "#D9A23F",
  creme: "#EEE2C6",
  cinzaAzul: "#6D8395",
  branco: "#FFFFFF",
  vidro: "#2C4257",
  vidroBrilho: "#7FA3BF",
  luz: "#FFD37A",
  telha: "#B4533A",
  ardosia: "#4B515B",
  portaVerde: "#2F6B4F",
  portaVermelha: "#A3342A",
  flores: ["#E5484D", "#F2A93B", "#F06BA8"],
  folha: "#4E8A3E",
  cais: "#8F8A82",
  caisPedra: "#7A766F",
  agua: "#3F7A8C",
  aguaFunda: "#1F4656",
  reflexo: "#A6D3DC",
  terra: "#6B4A35",
  turfa: "#4A3225",
  argila: "#5E4130",
  gota: "#8CC7DD",
  areia: "#DCBD80",
  areiaPonto: "#B8944F",
  madeira: "#B07B40",
  madeiraVeio: "#7A5229",
  sol: "#FFC93C",
  solBrilho: "#FFE89A",
  lua: "#F4F1DE",
  noiteTopo: "#14203D",
  noiteBase: "#2D3F6B",
  entardecer: "#F29A5A",
  sofa: "#2E8C82",
  sofaClaro: "#49AC9F",
  sofaPe: "#6B4423",
  pele: "#F1C59D",
  manga: "#3D5A80",
  ferro: "#363636",
  corda: "#C9A776",
} as const;

export const TRACO = 5;
export const LINHA = PAL.contorno;

/** Mistura de duas cores hex. */
export const mistura = (a: string, b: string, p: number): string => {
  const ca = parseInt(a.slice(1), 16);
  const cb = parseInt(b.slice(1), 16);
  const c = (s: number) => Math.round(((ca >> s) & 255) * (1 - p) + ((cb >> s) & 255) * p);
  return `#${((c(16) << 16) | (c(8) << 8) | c(0)).toString(16).padStart(6, "0")}`;
};

/** Mola: 0 → 1 passando do ponto e voltando 2 vezes, cada vez menos (dança das casas, balanço). */
export const mola = (p: number, oscila = 2.5, amortece = 6): number =>
  p <= 0 ? 0 : p >= 1 ? 1 : 1 - Math.exp(-amortece * p) * Math.cos(oscila * Math.PI * p);

export type Empena = "degrau" | "pescoco" | "sino" | "bico" | "reta";

export type CasaDesenho = {
  w: number;
  hb: number;
  hg: number;
  tipo: Empena;
  cor: string;
  porta?: string;
  /** viga de içar com gancho no alto (vista de frente) */
  viga?: boolean;
  /** floreira nas janelas do 1º andar */
  flores?: boolean;
};

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

/** Gradientes e texturas compartilhados (um por cena: `id` evita colisão entre cenas na mesma página). */
export const Defs: React.FC<{ id: string }> = ({ id }) => (
  <defs>
    <linearGradient id={`${id}-sombra`} x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stopColor="#FFFFFF" stopOpacity={0.12} />
      <stop offset="0.55" stopColor="#000000" stopOpacity={0} />
      <stop offset="1" stopColor="#000000" stopOpacity={0.22} />
    </linearGradient>
    <pattern id={`${id}-tijolo`} width={24} height={14} patternUnits="userSpaceOnUse">
      <path d="M0 13.5 H24 M12 0 V7 M0 7 H24 M0 7 V14 M24 7 V14" stroke="#000000" strokeOpacity={0.1} strokeWidth={1.5} fill="none" />
    </pattern>
    <linearGradient id={`${id}-vidro`} x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stopColor={PAL.vidroBrilho} />
      <stop offset="0.45" stopColor={PAL.vidro} />
      <stop offset="1" stopColor="#1B2A38" />
    </linearGradient>
    <linearGradient id={`${id}-agua`} x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stopColor={PAL.agua} />
      <stop offset="1" stopColor={PAL.aguaFunda} />
    </linearGradient>
    <pattern id={`${id}-pedra`} width={34} height={22} patternUnits="userSpaceOnUse">
      <rect width={34} height={22} fill={PAL.cais} />
      <path d="M0 11 H34 M17 0 V11 M8 11 V22 M26 11 V22" stroke={PAL.caisPedra} strokeWidth={2} />
    </pattern>
    <radialGradient id={`${id}-sol`}>
      <stop offset="0" stopColor={PAL.solBrilho} stopOpacity={0.9} />
      <stop offset="1" stopColor={PAL.solBrilho} stopOpacity={0} />
    </radialGradient>
    <radialGradient id={`${id}-luz`}>
      <stop offset="0" stopColor={PAL.luz} stopOpacity={0.55} />
      <stop offset="1" stopColor={PAL.luz} stopOpacity={0} />
    </radialGradient>
  </defs>
);

const Janela: React.FC<{ id: string; x: number; y: number; w: number; h: number; luz: number; flores?: boolean; semente: number }> = ({
  id, x, y, w, h, luz, flores, semente,
}) => {
  const acesa = luz > 0 && semente % 3 !== 0;
  return (
    <g>
      <rect x={x - 4} y={y - 4} width={w + 8} height={h + 8} rx={3} fill={PAL.branco} stroke={LINHA} strokeWidth={2.5} />
      <rect x={x} y={y} width={w} height={h} fill={`url(#${id}-vidro)`} />
      {acesa && <rect x={x} y={y} width={w} height={h} fill={PAL.luz} opacity={luz * 0.9} />}
      <path d={`M${x + w / 2} ${y} V${y + h} M${x} ${y + h * 0.45} H${x + w}`} stroke={PAL.branco} strokeWidth={3.5} />
      <path d={`M${x + w * 0.15} ${y + h * 0.15} L${x + w * 0.38} ${y + h * 0.05}`} stroke="#FFFFFF" strokeOpacity={0.45} strokeWidth={3} strokeLinecap="round" />
      <rect x={x - 7} y={y + h + 3} width={w + 14} height={6} rx={2} fill={PAL.branco} stroke={LINHA} strokeWidth={2} />
      {flores && (
        <g>
          <rect x={x - 2} y={y + h + 9} width={w + 4} height={12} rx={2} fill={PAL.madeira} stroke={LINHA} strokeWidth={2} />
          {Array.from({ length: 5 }, (_, i) => (
            <circle key={i} cx={x + 2 + (i * (w - 4)) / 4} cy={y + h + 7} r={4.5} fill={PAL.flores[(i + semente) % 3]} stroke={LINHA} strokeWidth={1.2} />
          ))}
        </g>
      )}
    </g>
  );
};

/** Casa de canal de frente: tijolo com textura e luz lateral, caixilhos brancos, porta colorida e (opcional) viga com gancho. */
export const Casa: React.FC<{ casa: CasaDesenho; id: string; luz?: number }> = ({ casa, id, luz = 0 }) => {
  const { w, hb, hg, tipo, cor, viga, porta, flores } = casa;
  const terreo = 150;
  const n = Math.max(2, Math.round((hb - terreo) / 140));
  const hA = (hb - terreo) / n;
  const cols = w > 180 ? 3 : 2;
  const margem = w * 0.16;
  const vao = w * 0.11;
  const ww = (w - 2 * margem - (cols - 1) * vao) / cols;
  const wh = hA * 0.56;
  const sil = silhueta(casa);
  const topo = -hb - hg;
  const sotao = tipo !== "reta" && tipo !== "bico";
  const janelas: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    for (let c = 0; c < cols; c++) {
      janelas.push(
        <Janela key={`${i}-${c}`} id={id} x={-w / 2 + margem + c * (ww + vao)} y={-hb + i * hA + hA * 0.2} w={ww} h={wh} luz={luz}
          flores={flores && i === n - 1} semente={i * 3 + c + Math.round(w)} />,
      );
    }
  }
  return (
    <g>
      <path d={sil} fill={cor} />
      <path d={sil} fill={`url(#${id}-tijolo)`} />
      <path d={sil} fill={`url(#${id}-sombra)`} />
      {/* cornija branca na base da empena */}
      {tipo !== "reta" && <rect x={-w / 2 - 4} y={-hb - 6} width={w + 8} height={10} rx={2} fill={PAL.branco} stroke={LINHA} strokeWidth={2.5} />}
      <path d={sil} fill="none" stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" />
      {janelas}
      {/* térreo: porta com bandeira e degrau, vitrine */}
      <rect x={-w / 2 + margem - 4} y={-terreo + 26} width={w * 0.26 + 8} height={terreo - 26} rx={4} fill={PAL.branco} stroke={LINHA} strokeWidth={2.5} />
      <rect x={-w / 2 + margem} y={-terreo + 48} width={w * 0.26} height={terreo - 48} rx={3} fill={porta ?? PAL.portaVerde} stroke={LINHA} strokeWidth={2.5} />
      <path d={`M${-w / 2 + margem} ${-terreo + 44} a${w * 0.13} ${w * 0.1} 0 0 1 ${w * 0.26} 0`} fill={`url(#${id}-vidro)`} stroke={LINHA} strokeWidth={2} />
      <circle cx={-w / 2 + margem + w * 0.2} cy={-terreo / 2 + 20} r={3} fill={PAL.ocre} />
      <rect x={-w / 2 + margem - 8} y={-6} width={w * 0.26 + 16} height={6} fill={PAL.caisPedra} stroke={LINHA} strokeWidth={2} />
      <Janela id={id} x={w / 2 - margem - w * 0.3} y={-terreo + 40} w={w * 0.3} h={terreo * 0.42} luz={luz} semente={7} />
      {sotao && <Janela id={id} x={-w * 0.09} y={-hb - hg * 0.5} w={w * 0.18} h={hg * 0.3} luz={luz} semente={4} />}
      {viga && (
        <g>
          <rect x={-12} y={topo + hg * 0.08} width={24} height={28} rx={3} fill={PAL.branco} stroke={LINHA} strokeWidth={3} />
          <path d={`M0 ${topo + hg * 0.08 + 28} V${topo + hg * 0.08 + 56} q0 14 -12 12`} fill="none" stroke={PAL.ferro} strokeWidth={4} strokeLinecap="round" />
        </g>
      )}
    </g>
  );
};

/** Céu em degradê (com cor variável para o ciclo do dia), nuvens que andam devagar. */
export const Ceu: React.FC<{ id: string; t: number; altura: number; topo?: string; base?: string; nuvens?: number }> = ({
  id, t, altura, topo = PAL.ceuTopo, base = PAL.ceuBase, nuvens = 1,
}) => {
  const lista = [
    [120, 250, 1.1], [620, 170, 0.8], [880, 360, 1.25], [380, 420, 0.7],
  ];
  return (
    <g>
      <defs>
        <linearGradient id={`${id}-ceu`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0" stopColor={topo} />
          <stop offset="1" stopColor={base} />
        </linearGradient>
      </defs>
      <rect x={0} y={0} width={1080} height={altura} fill={`url(#${id}-ceu)`} />
      {nuvens > 0 &&
        lista.map(([x, y, e], i) => {
          const xx = ((x + t * (0.012 + i * 0.004)) % 1300) - 110;
          return (
            <g key={i} transform={`translate(${xx} ${y}) scale(${e})`} opacity={0.92 * nuvens}>
              <ellipse cx={0} cy={0} rx={70} ry={26} fill={PAL.nuvem} />
              <circle cx={-28} cy={-14} r={26} fill={PAL.nuvem} />
              <circle cx={14} cy={-22} r={32} fill={PAL.nuvem} />
              <circle cx={46} cy={-6} r={22} fill={PAL.nuvem} />
            </g>
          );
        })}
    </g>
  );
};

/** Água do canal: degradê, reflexos que andam e brilho. */
export const Agua: React.FC<{ id: string; y: number; t: number; altura?: number }> = ({ id, y, t, altura = 1920 }) => {
  const linhas = [
    [120, 40, 120], [520, 90, 160], [860, 60, 110], [300, 160, 90], [700, 220, 140], [80, 300, 100],
    [480, 360, 130], [900, 410, 90], [220, 500, 150], [640, 580, 110], [380, 660, 120],
  ];
  return (
    <g>
      <rect x={0} y={y} width={1080} height={altura - y} fill={`url(#${id}-agua)`} />
      {linhas
        .filter(([, dy]) => y + dy < altura - 20)
        .map(([x, dy, l], i) => {
          const dx = Math.sin(t / 700 + i * 1.7) * 26;
          const o = 0.25 + 0.15 * Math.sin(t / 500 + i);
          return <line key={i} x1={x + dx} y1={y + dy} x2={x + dx + l} y2={y + dy} stroke={PAL.reflexo} strokeOpacity={o} strokeWidth={5} strokeLinecap="round" />;
        })}
    </g>
  );
};

/** Barco de passeio do canal (vista de lado), proa para a direita. */
export const Barco: React.FC = () => (
  <g stroke={LINHA} strokeWidth={3} strokeLinejoin="round">
    <path d="M-110 0 L110 0 Q130 0 122 22 L-104 22 Q-118 22 -110 0 Z" fill={PAL.creme} />
    <rect x={-90} y={-30} width={150} height={30} rx={10} fill={PAL.branco} />
    {[-78, -50, -22, 6, 34].map((x) => (
      <rect key={x} x={x} y={-24} width={20} height={16} rx={3} fill={PAL.vidro} strokeWidth={2} />
    ))}
    <path d="M-104 14 H118" stroke={PAL.portaVermelha} strokeWidth={4} />
  </g>
);

/** Sofá de frente, 190 × 130, origem no meio do topo do encosto: tecido verde-água, almofadas, pés de madeira. */
export const Sofa: React.FC = () => (
  <g stroke={LINHA} strokeWidth={4} strokeLinejoin="round">
    <rect x={-80} y={0} width={160} height={60} rx={14} fill={PAL.sofa} />
    <path d="M0 4 V56" stroke={PAL.contorno} strokeOpacity={0.35} strokeWidth={3} />
    <rect x={-95} y={44} width={190} height={56} rx={12} fill={PAL.sofaClaro} />
    <path d="M0 48 V96" stroke={PAL.contorno} strokeOpacity={0.35} strokeWidth={3} />
    <rect x={-97} y={28} width={32} height={80} rx={12} fill={PAL.sofa} />
    <rect x={65} y={28} width={32} height={80} rx={12} fill={PAL.sofa} />
    <rect x={-60} y={10} width={42} height={30} rx={8} fill={PAL.ocre} />
    <path d="M-82 108 l-4 20 M82 108 l4 20" stroke={PAL.sofaPe} strokeWidth={8} strokeLinecap="round" />
  </g>
);

/** Mão que empurra: manga azul, punho branco e o indicador apontando para +x (origem na ponta do dedo). */
export const Mao: React.FC = () => (
  <g stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" strokeLinecap="round">
    <rect x={-640} y={-62} width={380} height={124} rx={20} fill={PAL.manga} />
    <path d="M-560 -40 H-300" stroke="#FFFFFF" strokeOpacity={0.25} strokeWidth={8} />
    <rect x={-276} y={-70} width={44} height={140} rx={12} fill={PAL.branco} />
    <path
      d="M-236 -60 C-190 -78 -140 -70 -112 -44 L-18 -42 C10 -42 10 -2 -18 -2 L-100 -2 C-92 22 -98 40 -112 52 C-140 74 -196 74 -236 64 Z"
      fill={PAL.pele}
    />
    <path d="M-112 -2 C-120 10 -150 12 -168 6 M-104 24 C-118 32 -146 34 -164 28" fill="none" strokeWidth={3} />
  </g>
);

/** Sol com halo e raios girando devagar. */
export const Sol: React.FC<{ id: string; x: number; y: number; t: number; r?: number }> = ({ id, x, y, t, r = 46 }) => (
  <g>
    <circle cx={x} cy={y} r={r * 2.6} fill={`url(#${id}-sol)`} />
    <g transform={`rotate(${t / 40} ${x} ${y})`}>
      {Array.from({ length: 10 }, (_, i) => {
        const a = (i * Math.PI) / 5;
        return (
          <line key={i} x1={x + Math.cos(a) * (r + 14)} y1={y + Math.sin(a) * (r + 14)} x2={x + Math.cos(a) * (r + 34)} y2={y + Math.sin(a) * (r + 34)}
            stroke={PAL.sol} strokeWidth={7} strokeLinecap="round" />
        );
      })}
    </g>
    <circle cx={x} cy={y} r={r} fill={PAL.sol} stroke={PAL.ocre} strokeWidth={4} />
  </g>
);

/** Lua crescente. */
export const Lua: React.FC<{ x: number; y: number; cor: string }> = ({ x, y, cor }) => (
  <path d={`M${x + 10} ${y - 40} a42 42 0 1 0 30 70 a34 34 0 1 1 -30 -70 Z`} fill={PAL.lua} stroke={cor} strokeWidth={0} />
);
