/**
 * As três cenas desenhadas do Reel "As casas que dançam" (AMS-casas-tortas, REV1). Os eventos vêm das
 * props (ms no relógio da cena), ancorados nas palavras da narração em `reels/amsterdam-casas-tortas/rev1/rev1.json`.
 * Cores: paleta própria da ilustração (`PAL`, desenho.tsx), por decisão do Diego (21/10/2026).
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { kf, useMs } from "../../ds/tempo";
import { EASE } from "../../ds/tokens";
import { Agua, Barco, Casa, CasaDesenho, Ceu, Defs, LINHA, Lua, Mao, PAL, Sofa, Sol, TRACO, mistura, mola } from "./desenho";

const centros = (casas: CasaDesenho[], vao: number, meio = 540): number[] => {
  const total = casas.reduce((s, c) => s + c.w, 0) + vao * (casas.length - 1);
  let x = meio - total / 2;
  return casas.map((c) => {
    const cx = x + c.w / 2;
    x += c.w + vao;
    return cx;
  });
};

const Tela: React.FC<{ id: string; children: React.ReactNode }> = ({ id, children }) => (
  <AbsoluteFill style={{ background: PAL.ceuBase }}>
    <svg viewBox="0 0 1080 1920" width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <Defs id={id} />
      {children}
    </svg>
  </AbsoluteFill>
);

/** Dois pássaros cruzando o céu devagar. */
const Passaros: React.FC<{ t: number; y: number }> = ({ t, y }) => (
  <g fill="none" stroke={LINHA} strokeWidth={4} strokeLinecap="round">
    {[0, 1].map((i) => {
      const x = ((t * 0.09 + i * 90) % 1400) - 160;
      const bate = Math.sin(t / 110 + i) * 8;
      return <path key={i} d={`M${x - 18} ${y + i * 40 - bate} Q${x - 8} ${y + i * 40 - 10} ${x} ${y + i * 40} Q${x + 8} ${y + i * 40 - 10} ${x + 18} ${y + i * 40 - bate}`} />;
    })}
  </g>
);

/** Nuvenzinhas de poeira na base de uma casa que tomba. */
const Poeira: React.FC<{ t: number; x: number; y: number; w: number }> = ({ t, x, y, w }) => {
  if (t < 0 || t > 650) return null;
  const p = t / 650;
  return (
    <g opacity={1 - p}>
      {[-1, -0.4, 0.4, 1].map((k, i) => (
        <circle key={i} cx={x + (k * w) / 2 + k * 40 * p} cy={y - 10 - 26 * p} r={10 + 18 * p} fill={PAL.creme} />
      ))}
    </g>
  );
};

/* ------------------------------------------------------------------ 1. fileira: retas → cada uma para um lado → empurrão */

const BASE_FILEIRA = 1120;
const FILEIRA: CasaDesenho[] = [
  { w: 176, hb: 560, hg: 150, tipo: "degrau", cor: PAL.tijoloClaro, porta: PAL.portaVerde },
  { w: 168, hb: 640, hg: 140, tipo: "pescoco", cor: PAL.escura, viga: true, porta: PAL.portaVermelha, flores: true },
  { w: 184, hb: 520, hg: 170, tipo: "sino", cor: PAL.creme, porta: PAL.portaVerde, flores: true },
  { w: 168, hb: 600, hg: 150, tipo: "pescoco", cor: PAL.ocre, viga: true, porta: PAL.portaVermelha },
  { w: 176, hb: 580, hg: 120, tipo: "bico", cor: PAL.tijolo, porta: PAL.portaVerde },
];
/** Inclinação final de cada casa (graus): cada uma para um lado; a última fica reta até a mão. */
const INCLINA = [-4, -3, 3, 2];
const EMPURRADA = 6;

export type EventosFileira = { sobe?: number; inclina?: number[]; mao?: number };

export const CenaFileira: React.FC<{ modo: "retas" | "empurrao"; ev: EventosFileira }> = ({ modo, ev }) => {
  const t = useMs();
  const id = `fil-${modo}`;
  const xs = centros(FILEIRA, 8);
  const cais = modo === "retas" ? kf(t, [0, 450], [0, 1], EASE.out) : 1;
  const mao = ev.mao ?? 0;

  // inclinação com mola: as casas "dançam" até parar no ângulo
  const rot = (i: number): number => {
    if (i < 4) return modo === "retas" && ev.inclina ? INCLINA[i] * mola((t - ev.inclina[i]) / 750) : INCLINA[i];
    return modo === "empurrao" ? EMPURRADA * mola((t - mao - 300) / 800) : 0;
  };
  // nascer: sobe do chão e estica/achata (squash & stretch) até assentar
  const nasce = (i: number) => {
    if (modo !== "retas") return { dy: 0, sx: 1, sy: 1 };
    const p = (t - (ev.sobe ?? 0) - i * 110) / 560;
    if (p <= 0) return { dy: 2000, sx: 1, sy: 1 };
    if (p >= 1) return { dy: 0, sx: 1, sy: 1 };
    const s = 1 + 0.1 * Math.sin(2.4 * Math.PI * p) * Math.exp(-3 * p);
    return { dy: (1 - EASE.out(Math.min(1, p * 1.6))) * (FILEIRA[i].hb + FILEIRA[i].hg + 30), sx: 1 / Math.sqrt(s), sy: s };
  };

  const c4 = FILEIRA[4];
  const alvo = { x: xs[4] - 12, y: BASE_FILEIRA - c4.hb - c4.hg + 18 };
  const ang = 38;
  const off = modo === "empurrao" ? kf(t, [mao, mao + 300, mao + 560, mao + 950], [-1100, 0, 64, -1100], [EASE.out, EASE.out, EASE.exit]) : -1100;
  const dir = { x: Math.cos((ang * Math.PI) / 180), y: Math.sin((ang * Math.PI) / 180) };
  const barco = modo === "retas" ? -240 + t * 0.2 : 1400;

  const casas = (reflexo: boolean) =>
    FILEIRA.map((c, i) => {
      const n = nasce(i);
      return (
        <g key={i} transform={`translate(${xs[i]} ${BASE_FILEIRA + n.dy}) rotate(${rot(i)}) scale(${n.sx} ${n.sy})`}>
          <Casa casa={c} id={id} />
          {!reflexo && <ellipse cx={0} cy={4} rx={c.w * 0.55} ry={10} fill="#000000" opacity={0.18} />}
        </g>
      );
    });

  return (
    <Tela id={id}>
      <Ceu id={id} t={t} altura={BASE_FILEIRA} />
      <Passaros t={t} y={300} />
      <defs>
        <clipPath id={`${id}-acima`}>
          <rect x={0} y={0} width={1080} height={BASE_FILEIRA + 2} />
        </clipPath>
        <clipPath id={`${id}-agua`}>
          <rect x={0} y={BASE_FILEIRA + 34} width={1080} height={1920} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${id}-acima)`}>{casas(false)}</g>
      <rect x={0} y={BASE_FILEIRA} width={1080 * cais} height={34} fill={`url(#${id}-pedra)`} stroke={LINHA} strokeWidth={3} />
      <Agua id={id} y={BASE_FILEIRA + 34} t={t} />
      {/* reflexo das casas no canal */}
      <g clipPath={`url(#${id}-agua)`} opacity={0.2}>
        <g transform={`translate(0 ${2 * (BASE_FILEIRA + 34)}) scale(1 -1) translate(${Math.sin(t / 400) * 4} 0)`}>{casas(true)}</g>
      </g>
      <g transform={`translate(${barco} ${BASE_FILEIRA + 92})`}>
        <Barco />
      </g>
      {modo === "empurrao" && <Poeira t={t - mao - 320} x={xs[4]} y={BASE_FILEIRA} w={c4.w} />}
      {off > -1100 && (
        <g transform={`translate(${alvo.x + dir.x * off} ${alvo.y + dir.y * off}) rotate(${ang}) scale(1.15)`}>
          <Mao />
        </g>
      )}
    </Tela>
  );
};

/* ------------------------------------------------------------------ 2. solo: terreno macio, estacas, o tempo, o terreno cede */

const BASE_SOLO = 800;
const RUA = 30;
const AREIA = 1500;
const ESTACA = 400;
const SOLO: CasaDesenho[] = [
  { w: 200, hb: 330, hg: 120, tipo: "pescoco", cor: PAL.tijolo, viga: true, porta: PAL.portaVerde, flores: true },
  { w: 190, hb: 370, hg: 130, tipo: "degrau", cor: PAL.creme, porta: PAL.portaVermelha },
  { w: 200, hb: 310, hg: 140, tipo: "sino", cor: PAL.ocre, porta: PAL.portaVerde, flores: true },
  { w: 190, hb: 350, hg: 120, tipo: "pescoco", cor: PAL.escura, viga: true, porta: PAL.portaVermelha },
];
/** Quanto cada casa afunda (px) e inclina (graus) quando o terreno cede de maneira desigual. */
const CEDE = [
  { s: 8, a: -3 },
  { s: 26, a: 4 },
  { s: 20, a: -2 },
  { s: 6, a: 3 },
];

export type EventosSolo = { terreno: number; estacas: number; fundacoes: number; tempo: number; cede: number; inclina: number };

const onda = (y: number, t: number, fase: number, desloca: (x: number) => number, amp = 7): string => {
  let d = "";
  for (let x = -20; x <= 1100; x += 20) {
    const yy = y + Math.sin(x / 30 + fase + t / 1300) * amp + desloca(x);
    d += `${x === -20 ? "M" : " L"}${x} ${yy.toFixed(1)}`;
  }
  return d;
};

/** Ciclo de dois dias em 1,8 s: amanhecer → dia → pôr do sol → noite → … (f = fração do dia). */
const CEU_DIA: [number, string, string][] = [
  [0, PAL.entardecer, "#FBD7A6"],
  [0.12, PAL.ceuTopo, PAL.ceuBase],
  [0.38, PAL.ceuTopo, PAL.ceuBase],
  [0.5, "#C8664A", PAL.entardecer],
  [0.62, PAL.noiteTopo, PAL.noiteBase],
  [0.88, PAL.noiteTopo, PAL.noiteBase],
  [1, PAL.entardecer, "#FBD7A6"],
];
const corDoCeu = (f: number): [string, string] => {
  let i = 0;
  while (i < CEU_DIA.length - 2 && f > CEU_DIA[i + 1][0]) i++;
  const [f0, a0, b0] = CEU_DIA[i];
  const [f1, a1, b1] = CEU_DIA[i + 1];
  const p = (f - f0) / (f1 - f0);
  return [mistura(a0, a1, p), mistura(b0, b1, p)];
};

export const CenaSolo: React.FC<{ ev: EventosSolo }> = ({ ev }) => {
  const t = useMs();
  const id = "solo";
  const xs = centros(SOLO, 12);
  const revela = kf(t, [ev.terreno, ev.terreno + 700], [0, 1], EASE.cinema);
  const pc = kf(t, [ev.cede, ev.inclina + 450], [0, 1], EASE.cinema);
  const fimCede = ev.inclina + 450;
  const balanco = t > fimCede ? Math.sin(((t - fimCede) / 380) * 2 * Math.PI) * Math.exp(-(t - fimCede) / 280) * 0.25 : 0;
  const afunda = (x: number): number => pc * SOLO.reduce((s, c, i) => s + CEDE[i].s * Math.exp(-(((x - xs[i]) / (c.w * 0.62)) ** 2)), 0);

  // o tempo passando: 2 dias em 1,8 s, com sol, lua, estrelas e janelas acendendo
  const DUR_TEMPO = 1800;
  const pt = (t - ev.tempo) / DUR_TEMPO;
  const noTempo = pt >= 0 && pt < 1;
  const f = noTempo ? (pt * 2) % 1 : 0.25;
  const [topo, base] = corDoCeu(f);
  const noite = noTempo ? Math.max(0, Math.min(1, (f - 0.52) / 0.08, (0.98 - f) / 0.08)) : 0;
  const fd = Math.min(1, f / 0.5);
  const sol = noTempo && f < 0.5 ? { x: 40 + 1000 * fd, y: 700 - 470 * Math.sin(Math.PI * fd) } : null;
  const fl = (f - 0.5) / 0.5;
  const lua = noTempo && f >= 0.5 ? { x: 40 + 1000 * fl, y: 700 - 430 * Math.sin(Math.PI * fl) } : null;
  const solFixo = !noTempo ? { x: 900, y: 200 } : null;

  const gotas = [
    [150, 960], [330, 1100], [470, 900], [610, 1290], [760, 1040], [900, 1200], [240, 1380], [520, 1170], [820, 1400], [980, 940], [60, 1240], [680, 960], [400, 1320], [130, 1120],
  ];

  return (
    <Tela id={id}>
      <Ceu id={id} t={t} altura={BASE_SOLO} topo={topo} base={base} nuvens={1 - noite} />
      {noite > 0 &&
        Array.from({ length: 22 }, (_, i) => (
          <circle key={i} cx={(i * 197) % 1080} cy={60 + ((i * 113) % 520)} r={2 + (i % 3)} fill="#FFFFFF" opacity={noite * (0.6 + 0.4 * Math.sin(t / 120 + i))} />
        ))}
      {sol && <Sol id={id} x={sol.x} y={sol.y} t={t} />}
      {solFixo && <Sol id={id} x={solFixo.x} y={solFixo.y} t={t} r={38} />}
      {lua && <Lua x={lua.x} y={lua.y} cor={PAL.lua} />}
      {!noTempo && <Passaros t={t} y={340} />}

      {/* subsolo: antes da explicação é só terra; depois, o corte mostra as camadas */}
      <rect x={0} y={BASE_SOLO} width={1080} height={1920 - BASE_SOLO} fill={PAL.terra} />
      <defs>
        <clipPath id="solo-revela">
          <rect x={0} y={BASE_SOLO + RUA} width={1080} height={(1920 - BASE_SOLO - RUA) * revela} />
        </clipPath>
      </defs>
      <g clipPath="url(#solo-revela)">
        <rect x={0} y={BASE_SOLO + RUA} width={1080} height={AREIA - BASE_SOLO - RUA} fill={PAL.turfa} />
        {/* camadas de turfa e argila, onduladas (macio) */}
        {Array.from({ length: 10 }, (_, k) => {
          const y = BASE_SOLO + RUA + 40 + k * 62;
          const peso = Math.max(0, 1 - (y - BASE_SOLO - RUA) / 600);
          return (
            <path key={k} d={onda(y, t, k * 1.3, (x) => afunda(x) * peso)} fill="none" stroke={k % 3 === 0 ? PAL.argila : PAL.terra} strokeWidth={k % 3 === 0 ? 14 : 6}
              strokeLinecap="round" opacity={0.9} />
          );
        })}
        {/* lençol d'água: o terreno é encharcado */}
        <path d={onda(BASE_SOLO + RUA + 70, t * 1.6, 0.4, (x) => afunda(x) * 0.9, 9)} fill="none" stroke={PAL.gota} strokeWidth={6} strokeDasharray="22 14" opacity={0.85} />
        {gotas.map(([x, y0], i) => {
          const y = y0 + ((t * 0.05 + i * 41) % 110);
          return <path key={i} d={`M${x} ${y - 14} Q${x + 9} ${y} ${x} ${y + 6} Q${x - 9} ${y} ${x} ${y - 14} Z`} fill={PAL.gota} opacity={0.85} />;
        })}
        {/* camada firme de areia, bem mais funda que as estacas */}
        <rect x={0} y={AREIA} width={1080} height={1920 - AREIA} fill={PAL.areia} />
        {Array.from({ length: 16 }, (_, r) =>
          Array.from({ length: 22 }, (_, c) => (
            <circle key={`${r}-${c}`} cx={c * 50 + (r % 2) * 25 + 10} cy={AREIA + 22 + r * 26} r={4} fill={PAL.areiaPonto} />
          )),
        )}
        <path d={onda(AREIA, 0, 0.5, () => 0)} fill="none" stroke={PAL.areiaPonto} strokeWidth={6} />
      </g>

      {/* casas, fundações e estacas (afundam e inclinam juntas) */}
      {SOLO.map((c, i) => {
        const s = CEDE[i].s * pc;
        const a = CEDE[i].a * (pc + balanco);
        const viga = kf(t, [ev.fundacoes + i * 60, ev.fundacoes + i * 60 + 300], [0, 1], EASE.arrive);
        return (
          <g key={i} transform={`translate(${xs[i]} ${BASE_SOLO + s}) rotate(${a})`}>
            {[-1, 0, 1].map((j) => {
              const k = i * 3 + j + 1;
              const l = kf(t, [ev.estacas + k * 70, ev.estacas + k * 70 + 320], [0, 1], EASE.drop);
              if (l <= 0) return null;
              const x = j * c.w * 0.33;
              const y0 = RUA + 16;
              const y1 = y0 + ESTACA * l;
              return (
                <g key={j}>
                  <path d={`M${x - 13} ${y0} L${x + 13} ${y0} L${x + 13} ${y1 - 18} L${x} ${y1} L${x - 13} ${y1 - 18} Z`} fill={PAL.madeira} stroke={LINHA} strokeWidth={3} strokeLinejoin="round" />
                  <path d={`M${x - 5} ${y0 + 10} V${y1 - 26} M${x + 5} ${y0 + 30} V${y1 - 40}`} stroke={PAL.madeiraVeio} strokeWidth={2.5} />
                </g>
              );
            })}
            {viga > 0 && (
              <rect x={(-c.w / 2 + 4) * viga} y={RUA} width={(c.w - 8) * viga} height={20} rx={3} fill={PAL.madeira} stroke={LINHA} strokeWidth={3} />
            )}
            <Casa casa={c} id={id} luz={noite} />
          </g>
        );
      })}
      {noite > 0 &&
        SOLO.map((c, i) => <ellipse key={i} cx={xs[i]} cy={BASE_SOLO - c.hb / 2} rx={c.w * 0.8} ry={c.hb * 0.6} fill={`url(#${id}-luz)`} opacity={noite * 0.5} />)}
      {/* rua de pedra por cima da base das casas: quando afundam, a base some no chão */}
      <rect x={-10} y={BASE_SOLO} width={1100} height={RUA} fill={`url(#${id}-pedra)`} stroke={LINHA} strokeWidth={3} />
      {SOLO.map((c, i) => (
        <Poeira key={i} t={t - ev.inclina + 100 - i * 80} x={xs[i]} y={BASE_SOLO + 6} w={c.w} />
      ))}
    </Tela>
  );
};

/* ------------------------------------------------------------------ 3. gancho: fachada para a frente, sofá subindo */

const CHAO = 1200;
const PIVO = { x: 560, y: CHAO };
const GANCHO = { x: 400, y: 440 };
const L0 = 630;
const L_BATE = 430;
const L_TOPO = 40;
const PEITORIS = [790, 980, 1150];

export type EventosGancho = { sobe: number; bate: number; inclina: number; sobe2: number; entra: number };

const gira = (pt: { x: number; y: number }, graus: number) => {
  const r = (graus * Math.PI) / 180;
  const dx = pt.x - PIVO.x;
  const dy = pt.y - PIVO.y;
  return { x: PIVO.x + dx * Math.cos(r) - dy * Math.sin(r), y: PIVO.y + dx * Math.sin(r) + dy * Math.cos(r) };
};

export const CenaGancho: React.FC<{ ev: EventosGancho }> = ({ ev }) => {
  const t = useMs();
  const id = "gancho";
  const teta = -6 * mola((t - ev.inclina) / 800, 2, 6);
  const L =
    t < ev.bate
      ? kf(t, [ev.sobe, ev.bate], [L0, L_BATE], EASE.out)
      : t < ev.sobe2
        ? L_BATE + kf(t, [ev.bate, ev.bate + 90, ev.bate + 300], [0, 10, 6], [EASE.out, EASE.out])
        : kf(t, [ev.sobe2, ev.sobe2 + 1500], [L_BATE + 6, L_TOPO], EASE.cinema);
  let fi = 0;
  if (t >= ev.sobe && t < ev.bate) fi = 4.2 * Math.sin((Math.PI / 2) * Math.min(1, (t - ev.sobe) / (ev.bate - ev.sobe))) ** 2;
  else if (t >= ev.bate && t < ev.inclina) fi = kf(t, [ev.bate, ev.bate + 220, ev.bate + 520, ev.bate + 900], [4.2, -3, 1.2, 0], [EASE.out, EASE.out, EASE.out]);
  else if (t >= ev.inclina && t < ev.sobe2) {
    const d = Math.min(780, ev.sobe2 - ev.inclina);
    fi = kf(t, [ev.inclina, ev.inclina + d * 0.32, ev.inclina + d * 0.7, ev.inclina + d], [0, 3, -1.2, 0], [EASE.out, EASE.out, EASE.out]);
  } else if (t >= ev.sobe2 && t < ev.entra) fi = 1.2 * Math.sin((t - ev.sobe2) / 260);
  const tremor = t >= ev.bate && t < ev.bate + 67 ? (t < ev.bate + 33 ? 6 : -3) : 0;

  const g = gira(GANCHO, teta);
  const fr = (fi * Math.PI) / 180;
  const entra = kf(t, [ev.entra, ev.entra + 450], [0, 280], EASE.cinema);
  const topo = { x: g.x + L * Math.sin(fr) + entra, y: g.y + L * Math.cos(fr) };
  const cordas = 1 - kf(t, [ev.entra + 150, ev.entra + 400], [0, 1]);
  const prumo = kf(t, [ev.inclina + 150, ev.inclina + 450], [0, 1], EASE.out);
  const impacto = t >= ev.bate && t < ev.bate + 260 ? 1 - (t - ev.bate) / 260 : 0;
  const bracos = kf(t, [ev.entra - 350, ev.entra, ev.entra + 450, ev.entra + 750], [0, 1, 1, 0], [EASE.out, EASE.out, EASE.exit]);
  const porta = gira({ x: 546, y: 545 }, teta);

  return (
    <Tela id={id}>
      <Ceu id={id} t={t} altura={CHAO} />
      <Passaros t={t + 3000} y={220} />
      <g transform={`translate(${tremor} 0)`}>
        {/* corda e sofá (por trás da casa: ao entrar pela porta do sótão, some dentro dela) */}
        {cordas > 0 && (
          <g stroke={PAL.corda} strokeWidth={5} strokeLinecap="round" opacity={cordas}>
            <line x1={g.x} y1={g.y} x2={topo.x - 78 * Math.cos(fr)} y2={topo.y + 78 * Math.sin(fr)} />
            <line x1={g.x} y1={g.y} x2={topo.x + 78 * Math.cos(fr)} y2={topo.y - 78 * Math.sin(fr)} />
          </g>
        )}
        <g transform={`translate(${topo.x} ${topo.y}) rotate(${-fi})`}>
          <Sofa />
        </g>
        {impacto > 0 && (
          <g stroke={PAL.ocre} strokeWidth={6} strokeLinecap="round" opacity={impacto}>
            {[-40, 0, 40].map((a) => {
              const r = (a * Math.PI) / 180;
              const cx = 520;
              const cy = topo.y + 70;
              return <line key={a} x1={cx + Math.cos(r) * 30} y1={cy + Math.sin(r) * 30} x2={cx + Math.cos(r) * (52 + 20 * (1 - impacto))} y2={cy + Math.sin(r) * (52 + 20 * (1 - impacto))} />;
            })}
          </g>
        )}

        {/* casa de perfil: gira em torno da quina da frente (fachada inclinada para a frente) */}
        <g transform={`rotate(${teta} ${PIVO.x} ${PIVO.y})`}>
          <rect x={560} y={430} width={340} height={CHAO - 430} fill={PAL.tijolo} />
          <rect x={560} y={430} width={340} height={CHAO - 430} fill={`url(#${id}-tijolo)`} />
          <rect x={560} y={430} width={340} height={CHAO - 430} fill={`url(#${id}-sombra)`} />
          <rect x={560} y={430} width={340} height={CHAO - 430} fill="none" stroke={LINHA} strokeWidth={TRACO} />
          <path d="M560 430 L560 330 L900 380 L900 430 Z" fill={PAL.telha} stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" />
          {[0, 1, 2, 3].map((k) => (
            <path key={k} d={`M560 ${352 + k * 22} L900 ${396 + k * 9}`} stroke={PAL.tijoloEscuro} strokeWidth={3} opacity={0.7} />
          ))}
          <rect x={860} y={300} width={26} height={80} fill={PAL.tijoloEscuro} stroke={LINHA} strokeWidth={3} />
          {/* fachada vista de lado: faixa creme, cornija, janelas e peitoris brancos */}
          <rect x={546} y={330} width={28} height={CHAO - 330} fill={PAL.creme} stroke={LINHA} strokeWidth={4} />
          <rect x={532} y={318} width={56} height={20} rx={4} fill={PAL.branco} stroke={LINHA} strokeWidth={4} />
          {PEITORIS.map((y) => (
            <g key={y}>
              <rect x={538} y={y - 128} width={12} height={128} fill={PAL.branco} stroke={LINHA} strokeWidth={3} />
              <rect x={522} y={y - 6} width={30} height={12} rx={3} fill={PAL.branco} stroke={LINHA} strokeWidth={3} />
            </g>
          ))}
          {/* porta do sótão aberta, com a folha verde */}
          <rect x={546} y={470} width={28} height={150} fill="#1E1714" stroke={LINHA} strokeWidth={4} />
          <path d="M546 470 L506 486 L506 606 L546 620 Z" fill={PAL.portaVerde} stroke={LINHA} strokeWidth={3} strokeLinejoin="round" />
          {/* viga de içar, polia e gancho */}
          <path d="M560 368 L522 368 L560 404 Z" fill={PAL.branco} stroke={LINHA} strokeWidth={4} strokeLinejoin="round" />
          <rect x={384} y={344} width={176} height={24} rx={4} fill={PAL.branco} stroke={LINHA} strokeWidth={4} />
          <line x1={408} y1={372} x2={556} y2={478} stroke={PAL.corda} strokeWidth={5} strokeLinecap="round" />
          <circle cx={400} cy={386} r={17} fill={PAL.ferro} stroke={LINHA} strokeWidth={4} />
          <circle cx={400} cy={386} r={6} fill={PAL.ocre} transform={`rotate(${t / 3} 400 386)`} />
          <path d={`M400 403 V${GANCHO.y - 8} q0 14 -12 12`} fill="none" stroke={PAL.ferro} strokeWidth={6} strokeLinecap="round" />
        </g>
        {/* braços de quem recebe o sofá no sótão */}
        {bracos > 0 && (
          <g transform={`translate(${porta.x} ${porta.y}) rotate(${teta})`} opacity={bracos}>
            {[-22, 22].map((dy) => (
              <rect key={dy} x={-70 * bracos} y={dy - 9} width={74 * bracos} height={18} rx={9} fill={PAL.pele} stroke={LINHA} strokeWidth={3} />
            ))}
          </g>
        )}

        {/* prumo: a vertical fica, a fachada se inclina */}
        {prumo > 0 && (
          <g opacity={prumo} stroke={PAL.branco} strokeWidth={6} strokeDasharray="18 14" fill="none" strokeLinecap="round">
            <line x1={PIVO.x} y1={PIVO.y} x2={PIVO.x} y2={PIVO.y - 760} />
            <path d={`M${PIVO.x} ${PIVO.y - 170} A170 170 0 0 0 ${gira({ x: PIVO.x, y: PIVO.y - 170 }, teta).x} ${gira({ x: PIVO.x, y: PIVO.y - 170 }, teta).y}`} strokeDasharray="none" />
          </g>
        )}

        <rect x={-20} y={CHAO} width={1120} height={40} fill={`url(#${id}-pedra)`} stroke={LINHA} strokeWidth={3} />
        <Agua id={id} y={CHAO + 40} t={t} />
      </g>
    </Tela>
  );
};
