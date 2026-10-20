/**
 * As três cenas desenhadas do Reel "As casas que dançam" (AMS-casas-tortas, REV1). Os eventos vêm das
 * props (ms no relógio da cena), ancorados nas palavras da narração em `reels/amsterdam-casas-tortas/rev1/rev1.json`.
 * Curvas e durações são as do DS V2 (4.1): ease-arrive (passa do ponto e assenta), ease-out, ease-drop e ease-cinema.
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { Fibra } from "../../ds/material";
import { kf, useMs } from "../../ds/tempo";
import { COR, EASE, OPAC } from "../../ds/tokens";
import { Agua, Casa, CasaDesenho, LINHA, Mao, Sofa, Sol, TRACO } from "./desenho";

const centros = (casas: CasaDesenho[], vao: number, meio = 540): number[] => {
  const total = casas.reduce((s, c) => s + c.w, 0) + vao * (casas.length - 1);
  let x = meio - total / 2;
  return casas.map((c) => {
    const cx = x + c.w / 2;
    x += c.w + vao;
    return cx;
  });
};

const Papel: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: COR.papel }}>
    <svg viewBox="0 0 1080 1920" width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      {children}
    </svg>
    <Fibra opacidade={OPAC.fibra} semente={5} />
  </AbsoluteFill>
);

/* ------------------------------------------------------------------ 1. fileira: retas → cada uma para um lado → empurrão */

const BASE_FILEIRA = 1120;
const FILEIRA: CasaDesenho[] = [
  { w: 176, hb: 560, hg: 150, tipo: "degrau", cor: COR.concreto },
  { w: 168, hb: 640, hg: 140, tipo: "pescoco", cor: COR.grafite700, viga: true },
  { w: 184, hb: 520, hg: 170, tipo: "sino", cor: COR.recibo },
  { w: 168, hb: 600, hg: 150, tipo: "pescoco", cor: COR.amarelo, viga: true },
  { w: 176, hb: 580, hg: 120, tipo: "bico", cor: COR.asfalto },
];
/** Inclinação de cada casa (graus): duas para a esquerda, duas para a direita; a última fica reta até a mão. */
const INCLINA = [-4, -3, 3, 2];
const EMPURRADA = 6;

export type EventosFileira = { sobe?: number; inclina?: number[]; mao?: number };

export const CenaFileira: React.FC<{ modo: "retas" | "empurrao"; ev: EventosFileira }> = ({ modo, ev }) => {
  const t = useMs();
  const xs = centros(FILEIRA, 8);
  const cais = modo === "retas" ? kf(t, [0, 450], [0, 1], EASE.out) : 1;
  const mao = ev.mao ?? 0;

  const rot = (i: number): number => {
    if (i < 4) return modo === "retas" && ev.inclina ? kf(t, [ev.inclina[i], ev.inclina[i] + 380], [0, INCLINA[i]], EASE.arrive) : INCLINA[i];
    return modo === "empurrao" ? kf(t, [mao + 300, mao + 560], [0, EMPURRADA], EASE.arrive) : 0;
  };
  const sobe = (i: number): number => (modo === "retas" ? kf(t, [(ev.sobe ?? 0) + i * 110, (ev.sobe ?? 0) + i * 110 + 420], [0, 1], EASE.arrive) : 1);

  // mão: vem de cima à esquerda (por cima da vizinha), cutuca a ponta da empena da última casa em 300 ms,
  // acompanha a casa enquanto ela tomba e volta
  const c4 = FILEIRA[4];
  const alvo = { x: xs[4] - 12, y: BASE_FILEIRA - c4.hb - c4.hg + 18 };
  const ang = 38;
  const off = modo === "empurrao" ? kf(t, [mao, mao + 300, mao + 560, mao + 950], [-1100, 0, 64, -1100], [EASE.out, EASE.out, EASE.exit]) : -1100;
  const dir = { x: Math.cos((ang * Math.PI) / 180), y: Math.sin((ang * Math.PI) / 180) };

  return (
    <Papel>
      <defs>
        <clipPath id="fileira-acima">
          <rect x={0} y={0} width={1080} height={BASE_FILEIRA + 2} />
        </clipPath>
      </defs>
      <g clipPath="url(#fileira-acima)">
        {FILEIRA.map((c, i) => (
          <g key={i} transform={`translate(${xs[i]} ${BASE_FILEIRA + (1 - sobe(i)) * (c.hb + c.hg + 30)}) rotate(${rot(i)})`}>
            <Casa casa={c} />
          </g>
        ))}
      </g>
      <rect x={0} y={BASE_FILEIRA} width={1080 * cais} height={34} fill={COR.grafite800} />
      <Agua y={BASE_FILEIRA + 34} t={t} />
      {off > -1100 && (
        <g transform={`translate(${alvo.x + dir.x * off} ${alvo.y + dir.y * off}) rotate(${ang}) scale(1.15)`}>
          <Mao />
        </g>
      )}
    </Papel>
  );
};

/* ------------------------------------------------------------------ 2. solo: terreno macio, estacas, o tempo, o terreno cede */

const BASE_SOLO = 800;
const RUA = 30;
const AREIA = 1500;
const ESTACA = 400;
const SOLO: CasaDesenho[] = [
  { w: 200, hb: 330, hg: 120, tipo: "pescoco", cor: COR.grafite700, viga: true },
  { w: 190, hb: 370, hg: 130, tipo: "degrau", cor: COR.concreto },
  { w: 200, hb: 310, hg: 140, tipo: "sino", cor: COR.amarelo },
  { w: 190, hb: 350, hg: 120, tipo: "pescoco", cor: COR.asfalto, viga: true },
];
/** Quanto cada casa afunda (px) e inclina (graus) quando o terreno cede de maneira desigual. */
const CEDE = [
  { s: 8, a: -3 },
  { s: 26, a: 4 },
  { s: 20, a: -2 },
  { s: 6, a: 3 },
];

export type EventosSolo = { terreno: number; estacas: number; fundacoes: number; tempo: number; cede: number; inclina: number };

const onda = (y: number, t: number, fase: number, desloca: (x: number) => number): string => {
  let d = "";
  for (let x = -20; x <= 1100; x += 20) {
    const yy = y + Math.sin(x / 26 + fase + t / 1400) * 6 + desloca(x);
    d += `${x === -20 ? "M" : " L"}${x} ${yy.toFixed(1)}`;
  }
  return d;
};

export const CenaSolo: React.FC<{ ev: EventosSolo }> = ({ ev }) => {
  const t = useMs();
  const xs = centros(SOLO, 12);
  const revela = kf(t, [ev.terreno, ev.terreno + 650], [0, 1], EASE.cinema);
  const p = kf(t, [ev.cede, ev.inclina + 450], [0, 1], EASE.cinema);
  const afunda = (x: number): number =>
    p * SOLO.reduce((s, c, i) => s + CEDE[i].s * Math.exp(-(((x - xs[i]) / (c.w * 0.62)) ** 2)), 0);

  // sol: dois dias passando (2 × 700 ms), por trás das casas
  const ps = (t - ev.tempo) / 1400;
  const fr = ps * 2 - Math.floor(ps * 2);
  const fe = EASE.cinema(fr);
  const sol = ps >= 0 && ps < 1 ? { x: 40 + 1000 * fe, y: 720 - 470 * Math.sin(Math.PI * fe) } : null;

  const bolhas = [
    [150, 980], [330, 1120], [470, 900], [610, 1300], [760, 1050], [900, 1210], [240, 1380], [520, 1180], [820, 1400], [980, 940], [60, 1240], [680, 960],
  ];

  return (
    <Papel>
      {sol && <Sol x={sol.x} y={sol.y} />}

      {/* subsolo: antes da explicação é só chão escuro */}
      <rect x={0} y={BASE_SOLO} width={1080} height={1920 - BASE_SOLO} fill={COR.grafite} />
      <defs>
        <clipPath id="solo-revela">
          <rect x={0} y={BASE_SOLO + RUA} width={1080} height={(1920 - BASE_SOLO - RUA) * revela} />
        </clipPath>
      </defs>
      <g clipPath="url(#solo-revela)">
        {/* terreno macio e encharcado: camadas onduladas e bolhas de água */}
        <rect x={0} y={BASE_SOLO + RUA} width={1080} height={AREIA - BASE_SOLO - RUA} fill={COR.grafite800} />
        {Array.from({ length: 10 }, (_, k) => {
          const y = BASE_SOLO + RUA + 40 + k * 62;
          const peso = Math.max(0, 1 - (y - BASE_SOLO - RUA) / 600);
          return <path key={k} d={onda(y, t, k * 1.3, (x) => afunda(x) * peso)} fill="none" stroke={COR.concreto} strokeOpacity={0.3} strokeWidth={4} strokeLinecap="round" />;
        })}
        {bolhas.map(([x, y0], i) => {
          const y = y0 - ((t * 0.03 + i * 37) % 90);
          return <circle key={i} cx={x} cy={y} r={6 + (i % 3) * 2} fill="none" stroke={COR.concreto} strokeOpacity={0.45} strokeWidth={3} />;
        })}
        {/* camada firme de areia, bem mais funda que as estacas */}
        <rect x={0} y={AREIA} width={1080} height={1920 - AREIA} fill={COR.grafite700} />
        {Array.from({ length: 16 }, (_, r) =>
          Array.from({ length: 22 }, (_, c) => (
            <circle key={`${r}-${c}`} cx={c * 50 + (r % 2) * 25 + 10} cy={AREIA + 22 + r * 26} r={4} fill={COR.concreto} fillOpacity={0.5} />
          )),
        )}
        <path d={onda(AREIA, 0, 0.5, () => 0)} fill="none" stroke={COR.concreto} strokeOpacity={0.4} strokeWidth={4} />
      </g>

      {/* casas, fundações e estacas (afundam e inclinam juntas) */}
      {SOLO.map((c, i) => {
        const s = CEDE[i].s * p;
        const a = CEDE[i].a * p;
        const viga = kf(t, [ev.fundacoes + i * 60, ev.fundacoes + i * 60 + 260], [0, 1], EASE.out);
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
                <path key={j} d={`M${x - 12} ${y0} L${x + 12} ${y0} L${x + 12} ${y1 - 16} L${x} ${y1} L${x - 12} ${y1 - 16} Z`}
                  fill={COR.amarelo} stroke={LINHA} strokeWidth={4} strokeLinejoin="round" />
              );
            })}
            {viga > 0 && (
              <rect x={(-c.w / 2 + 4) * viga} y={RUA} width={(c.w - 8) * viga} height={18} rx={3} fill={COR.amarelo300} stroke={LINHA} strokeWidth={4} />
            )}
            <Casa casa={c} />
          </g>
        );
      })}
      {/* rua por cima da base das casas: quando afundam, a base some no chão */}
      <rect x={0} y={BASE_SOLO} width={1080} height={RUA} fill={COR.grafite800} />
    </Papel>
  );
};

/* ------------------------------------------------------------------ 3. gancho: fachada para a frente, sofá subindo */

const CHAO = 1200;
const PIVO = { x: 560, y: CHAO };
const GANCHO = { x: 400, y: 440 };
const L0 = 630; // sofá no chão
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
  const teta = kf(t, [ev.inclina, ev.inclina + 600], [0, -6], EASE.arrive);
  const L =
    t < ev.bate
      ? kf(t, [ev.sobe, ev.bate], [L0, L_BATE], EASE.out)
      : t < ev.sobe2
        ? L_BATE + kf(t, [ev.bate, ev.bate + 90, ev.bate + 300], [0, 10, 6], [EASE.out, EASE.out])
        : kf(t, [ev.sobe2, ev.sobe2 + 1500], [L_BATE + 6, L_TOPO], EASE.cinema);
  // balanço: sobe balançando até bater no peitoril; depois do baque volta 1 vez; ao inclinar, fica para trás e assenta
  let fi = 0;
  if (t >= ev.sobe && t < ev.bate) fi = 4.2 * Math.sin((Math.PI / 2) * Math.min(1, (t - ev.sobe) / (ev.bate - ev.sobe))) ** 2;
  else if (t >= ev.bate && t < ev.inclina) fi = kf(t, [ev.bate, ev.bate + 220, ev.bate + 520, ev.bate + 900], [4.2, -3, 1.2, 0], [EASE.out, EASE.out, EASE.out]);
  else if (t >= ev.inclina && t < ev.sobe2) {
    // fica para trás quando a viga anda e volta 1 vez; termina antes da subida (a fala dá ≈ 800 ms entre as duas)
    const d = Math.min(780, ev.sobe2 - ev.inclina);
    fi = kf(t, [ev.inclina, ev.inclina + d * 0.32, ev.inclina + d * 0.7, ev.inclina + d], [0, 3, -1.2, 0], [EASE.out, EASE.out, EASE.out]);
  }
  else if (t >= ev.sobe2 && t < ev.entra) fi = 1.2 * Math.sin((t - ev.sobe2) / 260);
  // tremor de 2 quadros no baque (DS 4.5: camera shake só no impacto, ±6 → ±3 px)
  const tremor = t >= ev.bate && t < ev.bate + 67 ? (t < ev.bate + 33 ? 6 : -3) : 0;

  const g = gira(GANCHO, teta);
  const fr = (fi * Math.PI) / 180;
  const entra = kf(t, [ev.entra, ev.entra + 450], [0, 280], EASE.cinema);
  const topo = { x: g.x + L * Math.sin(fr) + entra, y: g.y + L * Math.cos(fr) };
  const cordas = 1 - kf(t, [ev.entra + 150, ev.entra + 400], [0, 1]);
  const prumo = kf(t, [ev.inclina + 150, ev.inclina + 450], [0, 1], EASE.out);

  return (
    <Papel>
      <g transform={`translate(${tremor} 0)`}>
        {/* sofá (por trás da casa: ao entrar pela porta do sótão, some dentro dela) */}
        {cordas > 0 && (
          <g stroke={LINHA} strokeWidth={4} strokeLinecap="round" opacity={cordas}>
            <line x1={g.x} y1={g.y} x2={topo.x - 78 * Math.cos(fr)} y2={topo.y + 78 * Math.sin(fr)} />
            <line x1={g.x} y1={g.y} x2={topo.x + 78 * Math.cos(fr)} y2={topo.y - 78 * Math.sin(fr)} />
          </g>
        )}
        <g transform={`translate(${topo.x} ${topo.y}) rotate(${-fi})`}>
          <Sofa />
        </g>

        {/* casa de perfil: gira em torno da quina da frente (fachada inclinada para a frente) */}
        <g transform={`rotate(${teta} ${PIVO.x} ${PIVO.y})`}>
          <rect x={560} y={430} width={340} height={CHAO - 430} fill={COR.grafite700} stroke={LINHA} strokeWidth={TRACO} />
          {[640, 830, 1020].map((y) => (
            <line key={y} x1={566} y1={y} x2={894} y2={y} stroke={COR.concreto} strokeOpacity={0.18} strokeWidth={4} />
          ))}
          <path d={`M560 430 L560 330 L900 380 L900 430 Z`} fill={COR.grafite800} stroke={LINHA} strokeWidth={TRACO} strokeLinejoin="round" />
          {/* fachada vista de lado: faixa clara, cornija, janelas e peitoris */}
          <rect x={546} y={330} width={28} height={CHAO - 330} fill={COR.recibo} stroke={LINHA} strokeWidth={5} />
          <rect x={534} y={320} width={52} height={18} rx={3} fill={COR.recibo} stroke={LINHA} strokeWidth={5} />
          {PEITORIS.map((y) => (
            <g key={y}>
              <rect x={538} y={y - 128} width={10} height={128} fill={COR.recibo} stroke={LINHA} strokeWidth={4} />
              <rect x={524} y={y - 6} width={26} height={12} rx={2} fill={COR.recibo} stroke={LINHA} strokeWidth={4} />
            </g>
          ))}
          {/* porta do sótão aberta */}
          <rect x={546} y={470} width={28} height={150} fill={COR.grafite} stroke={LINHA} strokeWidth={5} />
          {/* viga de içar, polia e gancho */}
          <path d="M560 368 L522 368 L560 404 Z" fill={COR.recibo} stroke={LINHA} strokeWidth={5} strokeLinejoin="round" />
          <rect x={384} y={344} width={176} height={24} rx={3} fill={COR.recibo} stroke={LINHA} strokeWidth={5} />
          <line x1={408} y1={372} x2={556} y2={478} stroke={LINHA} strokeWidth={4} strokeLinecap="round" />
          <circle cx={400} cy={386} r={17} fill={COR.grafite800} stroke={LINHA} strokeWidth={5} />
          <circle cx={400} cy={386} r={5} fill={COR.recibo} />
          <path d={`M400 403 V${GANCHO.y - 8} q0 14 -12 12`} fill="none" stroke={LINHA} strokeWidth={6} strokeLinecap="round" />
        </g>

        {/* prumo: a vertical fica, a fachada se inclina */}
        {prumo > 0 && (
          // depois de inclinar, o prumo fica sobre a parede escura: concreto tracejado (linha de referência, não é Rota)
          <g opacity={prumo} stroke={COR.concreto} strokeWidth={6} strokeDasharray="18 14" fill="none" strokeLinecap="round">
            <line x1={PIVO.x} y1={PIVO.y} x2={PIVO.x} y2={PIVO.y - 760} />
            <path d={`M${PIVO.x} ${PIVO.y - 170} A170 170 0 0 0 ${gira({ x: PIVO.x, y: PIVO.y - 170 }, teta).x} ${gira({ x: PIVO.x, y: PIVO.y - 170 }, teta).y}`} />
          </g>
        )}

        <rect x={-20} y={CHAO} width={1120} height={40} fill={COR.grafite800} />
        <Agua y={CHAO + 40} t={t} />
      </g>
    </Papel>
  );
};
