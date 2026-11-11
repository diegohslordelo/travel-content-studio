/**
 * Animações da Parte 2 do Reel da Disney (reels/disney-parte2/), na mesma linguagem da Parte 1 (./Graficos):
 * traço papel, destaque âmbar, fundo do parque desfocado. Só se escreve na tela o que a fala diz (FORMATOS_REELS 6).
 * Mapa, linha de trem, relógio, parques, termômetro e dragão são desenho: não se passam por foto.
 */
import React from "react";
import { evolvePath } from "@remotion/paths";
import { PALETA, TITULO, clamp, ease, easeInOut } from "../paris/estilo";
import { FundoParque, Linha, Rotulos } from "./Graficos";

const PAPEL = PALETA.papel;
const AMBAR = PALETA.ambar;
const FUNDO = PALETA.fundo;
const VERMELHO = PALETA.vermelho;
const TRACO = 6;
const pop = (p: number) => {
  const x = clamp(p);
  if (x <= 0) return 0;
  return x < 0.6 ? ease(x / 0.6) * 1.12 : 1.12 - 0.12 * easeInOut((x - 0.6) / 0.4);
};

type Props = { t: number; marcos: Record<string, number>; fundo?: string; linhas?: Linha[] };

// ---------------------------------------------------------------- dica 1: de Paris até a Disney (RER A)
const SENA = "M60 690 C 160 640, 220 760, 330 700 S 470 600, 560 660 S 760 760, 860 690 S 990 640, 1040 680";
const LINHA_A = "M240 600 C 360 560, 470 640, 600 600 S 800 520, 900 560";
/** Paris (contorno do anel viário e a Torre em traço) à esquerda, a Disney (castelo) à direita; a linha A do RER se desenha
 * em "RER", o trem corre por ela e o relógio "40 MIN" entra na palavra. */
export const MapaRER: React.FC<Props> = ({ t, marcos, fundo, linhas = [] }) => {
  const mr = marcos.rer ?? 1.5;
  const m40 = marcos.quarenta ?? 2.5;
  const evSena = evolvePath(easeInOut(t / 0.8), SENA);
  const evA = evolvePath(easeInOut((t - mr + 0.1) / 0.8), LINHA_A);
  const trem = clamp((t - mr - 0.5) / 1.6);
  // posição aproximada do trem na curva (amostra da Bézier por partes)
  const px = 240 + (900 - 240) * easeInOut(trem);
  const py = 600 - 40 * Math.sin(Math.PI * easeInOut(trem) * 2) + (560 - 600) * easeInOut(trem);
  const e40 = pop((t - m40 + 0.05) / 0.35);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <path d={SENA} fill="none" stroke="rgba(120,170,220,0.55)" strokeWidth={14} strokeLinecap="round" strokeDasharray={evSena.strokeDasharray} strokeDashoffset={evSena.strokeDashoffset} />
        {/* Paris: anel viário + Torre */}
        <g transform={`translate(240 600) scale(${pop((t - 0.05) / 0.4)})`}>
          <ellipse rx={140} ry={95} fill="rgba(236,229,216,0.06)" stroke={PAPEL} strokeWidth={TRACO} />
          <path d="M-18 40 L0 -70 L18 40 M-12 5 L12 5 M-7 -30 L7 -30" fill="none" stroke={PAPEL} strokeWidth={5} strokeLinejoin="round" />
          <circle r={12} cy={60} fill={AMBAR} />
        </g>
        {/* Disney: castelo */}
        <g transform={`translate(900 560) scale(${pop((t - 0.2) / 0.4)})`}>
          <circle r={95} fill="rgba(224,174,92,0.12)" stroke={AMBAR} strokeWidth={TRACO} />
          <path d="M-50 40 V-6 H-36 V-24 H-22 V-6 H-8 V-46 L0 -70 L8 -46 V-6 H22 V-24 H36 V-6 H50 V40 Z" fill={AMBAR} stroke={FUNDO} strokeWidth={3} strokeLinejoin="round" />
        </g>
        {/* linha A do RER (vermelha, como no mapa de Paris) */}
        <path d={LINHA_A} fill="none" stroke={VERMELHO} strokeWidth={12} strokeLinecap="round" strokeDasharray={evA.strokeDasharray} strokeDashoffset={evA.strokeDashoffset} />
        {t > mr && (
          <g transform={`translate(${px} ${py})`}>
            <rect x={-34} y={-18} width={68} height={36} rx={12} fill={PAPEL} stroke={FUNDO} strokeWidth={3} />
            <rect x={-24} y={-10} width={16} height={12} rx={3} fill={FUNDO} />
            <rect x={-2} y={-10} width={16} height={12} rx={3} fill={FUNDO} />
          </g>
        )}
        {t > mr - 0.05 && (
          <g transform={`translate(560 520) scale(${pop((t - mr) / 0.3)})`}>
            <rect x={-80} y={-34} width={160} height={68} rx={34} fill={VERMELHO} />
            <text y={20} textAnchor="middle" style={{ font: `400 52px ${TITULO}` }} fill="#fff">RER A</text>
          </g>
        )}
        {/* relógio 40 MIN */}
        {e40 > 0 && (
          <g transform={`translate(560 780) scale(${e40})`}>
            <rect x={-150} y={-52} width={300} height={104} rx={52} fill={FUNDO} stroke={AMBAR} strokeWidth={5} />
            <circle cx={-92} r={30} fill="none" stroke={AMBAR} strokeWidth={5} />
            <line x1={-92} y1={0} x2={-92} y2={-18} stroke={AMBAR} strokeWidth={5} strokeLinecap="round" />
            <line x1={-92} y1={0} x2={-78} y2={8} stroke={AMBAR} strokeWidth={5} strokeLinecap="round" />
            <text x={30} y={22} textAnchor="middle" style={{ font: `400 64px ${TITULO}` }} fill={AMBAR}>40 MIN</text>
          </g>
        )}
      </svg>
      <Rotulos t={t} x={250} y={300} w={800} linhas={linhas} />
    </div>
  );
};

/** "Ela é a última estação da linha e tem várias carinhas do Mickey pra te guiar": a linha com as paradas; a última acende
 * e as carinhas do Mickey (três círculos) entram uma a uma, como placas guiando. */
export const LinhaFinal: React.FC<Props> = ({ t, marcos, fundo, linhas = [] }) => {
  const mu = marcos.ultima ?? 1.0;
  const mm = marcos.carinhas ?? 2.4;
  const N = 6;
  const x0 = 110;
  const dx = 165;
  const desenha = easeInOut(t / 0.6);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <line x1={x0} y1={620} x2={x0 + (N - 1) * dx * desenha} y2={620} stroke={VERMELHO} strokeWidth={14} strokeLinecap="round" />
        {Array.from({ length: N }).map((_, i) => {
          const ultima = i === N - 1;
          const e = pop((t - 0.1 - i * 0.08) / 0.3);
          const acende = ultima ? ease((t - mu + 0.05) / 0.3) : 0;
          const pulso = ultima && t > mu ? 1 + 0.08 * Math.sin((t - mu) * 8) : 1;
          return (
            <g key={i} transform={`translate(${x0 + i * dx} 620) scale(${e * pulso})`}>
              <circle r={ultima ? 34 : 20} fill={ultima ? `rgba(224,174,92,${0.3 + 0.7 * acende})` : PAPEL} stroke={ultima ? AMBAR : FUNDO} strokeWidth={ultima ? 8 : 4} />
            </g>
          );
        })}
        {/* carinhas do Mickey guiando até a última estação */}
        {[0, 1, 2].map((k) => {
          const e = pop((t - mm - k * 0.18) / 0.3);
          if (e <= 0) return null;
          const x = x0 + (2.4 + k * 1.1) * dx;
          return (
            <g key={k} transform={`translate(${x} 500) scale(${e})`}>
              <line x1={0} y1={30} x2={0} y2={95} stroke={PAPEL} strokeWidth={6} />
              <circle r={36} fill={FUNDO} stroke={AMBAR} strokeWidth={5} />
              <circle cx={-30} cy={-30} r={20} fill={FUNDO} stroke={AMBAR} strokeWidth={5} />
              <circle cx={30} cy={-30} r={20} fill={FUNDO} stroke={AMBAR} strokeWidth={5} />
              <path d="M-14 6 L10 6 M2 -6 L14 6 L2 18" fill="none" stroke={AMBAR} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
            </g>
          );
        })}
      </svg>
      <Rotulos t={t} x={72} y={300} w={936} linhas={linhas} />
    </div>
  );
};

// ---------------------------------------------------------------- dica 2: horário dos portões
/** Relógio cujos ponteiros giram; em "estação do ano" o sol vira floco de neve; em "30" entra "30 MIN ANTES". */
export const Relogio: React.FC<Props> = ({ t, marcos, fundo, linhas = [] }) => {
  const me = marcos.estacao ?? 2.0;
  const giro = t * 220;
  const troca = ease((t - me) / 0.5);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <g transform={`translate(290 600) scale(${pop((t - 0.03) / 0.35)})`}>
          <circle r={190} fill="rgba(20,18,15,0.7)" stroke={PAPEL} strokeWidth={TRACO + 2} />
          {Array.from({ length: 12 }).map((_, i) => (
            <line key={i} x1={0} y1={-160} x2={0} y2={i % 3 ? -172 : -182} stroke={PAPEL} strokeWidth={i % 3 ? 4 : 7} transform={`rotate(${i * 30})`} />
          ))}
          <line x1={0} y1={0} x2={0} y2={-120} stroke={PAPEL} strokeWidth={10} strokeLinecap="round" transform={`rotate(${giro / 12})`} />
          <line x1={0} y1={0} x2={0} y2={-160} stroke={AMBAR} strokeWidth={7} strokeLinecap="round" transform={`rotate(${giro})`} />
          <circle r={12} fill={AMBAR} />
          {/* estação do ano: sol → floco */}
          <g transform="translate(140 -150)">
            <g opacity={1 - troca}>
              <circle r={34} fill={AMBAR} />
              {Array.from({ length: 8 }).map((_, i) => (
                <line key={i} x1={0} y1={-46} x2={0} y2={-60} stroke={AMBAR} strokeWidth={6} strokeLinecap="round" transform={`rotate(${i * 45})`} />
              ))}
            </g>
            <g opacity={troca} transform={`rotate(${troca * 60})`}>
              {[0, 60, 120].map((r) => (
                <line key={r} x1={0} y1={-50} x2={0} y2={50} stroke="#cfe6ff" strokeWidth={7} strokeLinecap="round" transform={`rotate(${r})`} />
              ))}
            </g>
          </g>
        </g>
      </svg>
      <Rotulos t={t} x={560} y={330} w={480} linhas={linhas} />
    </div>
  );
};

// ---------------------------------------------------------------- dica 3: os dois parques
/** Dois cartões de parque: o da esquerda (Vingadores, montanha-russa) ganha o "1º" em "começa"; o da direita (castelo) fica para depois. */
export const Parques: React.FC<Props> = ({ t, marcos, fundo, linhas = [] }) => {
  const mc = marcos.comeca ?? 2.4;
  const ma = marcos.adventure ?? 3.2;
  const card = (x: number, k: number, conteudo: React.ReactNode, destaque: number) => {
    const e = pop((t - 0.05 - k * 0.12) / 0.35);
    return (
      <g transform={`translate(${x} 640) scale(${e})`}>
        <rect x={-200} y={-180} width={400} height={340} rx={30} fill={destaque > 0 ? `rgba(224,174,92,${0.12 + 0.16 * destaque})` : "rgba(20,18,15,0.65)"} stroke={destaque > 0 ? AMBAR : PAPEL} strokeWidth={TRACO} />
        {conteudo}
      </g>
    );
  };
  const d1 = ease((t - mc) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        {card(
          290,
          0,
          <g>
            {/* escudo com estrela (Vingadores) + trilho de montanha-russa */}
            <path d="M0 -120 L80 -90 L70 10 Q 40 70 0 90 Q -40 70 -70 10 L-80 -90 Z" fill="none" stroke={PAPEL} strokeWidth={TRACO} strokeLinejoin="round" />
            <path d="M0 -60 L14 -24 L52 -22 L22 2 L32 40 L0 18 L-32 40 L-22 2 L-52 -22 L-14 -24 Z" fill={AMBAR} />
            <path d="M-160 130 C -110 60, -60 60, -30 120 S 60 160, 160 100" fill="none" stroke={PAPEL} strokeWidth={5} />
          </g>,
          d1,
        )}
        {card(
          790,
          1,
          <g>
            <path d="M-80 90 V10 H-58 V-20 H-36 V10 H-14 V-60 L0 -100 L14 -60 V10 H36 V-20 H58 V10 H80 V90 Z" fill="none" stroke={PAPEL} strokeWidth={TRACO} strokeLinejoin="round" />
          </g>,
          0,
        )}
        {/* seta 1º → depois */}
        {d1 > 0 && (
          <g opacity={d1}>
            <path d="M505 640 L575 640 M555 618 L578 640 L555 662" fill="none" stroke={AMBAR} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
            <g transform={`translate(460 475) scale(${pop((t - mc) / 0.3)})`}>
              <circle r={52} fill={AMBAR} />
              <text y={22} textAnchor="middle" style={{ font: `400 64px ${TITULO}` }} fill={FUNDO}>1</text>
            </g>
          </g>
        )}
        {t > ma - 0.05 && (
          <text x={290} y={850} textAnchor="middle" style={{ font: `400 52px ${TITULO}` }} fill={AMBAR} opacity={ease((t - ma) / 0.2)}>
            DISNEY ADVENTURE
          </text>
        )}
      </svg>
      <Rotulos t={t} x={250} y={300} w={800} linhas={linhas} />
    </div>
  );
};

// ---------------------------------------------------------------- dica 4: frio
/** Termômetro que desce e flocos caindo; "NÃO VÁ DE PEITO ABERTO" e "SUBESTIMEI" na palavra. */
export const Frio: React.FC<Props> = ({ t, fundo, linhas = [] }) => {
  const nivel = 1 - 0.75 * easeInOut(clamp((t - 0.3) / 2.2));
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        {Array.from({ length: 14 }).map((_, i) => {
          const x = (i * 157) % 1080;
          const y = ((t * (60 + (i % 5) * 18) + i * 97) % 700) + 260;
          return (
            <g key={i} transform={`translate(${x} ${y}) rotate(${t * 40 + i * 20})`} opacity={0.75}>
              {[0, 60, 120].map((r) => (
                <line key={r} x1={0} y1={-12} x2={0} y2={12} stroke="#dcecff" strokeWidth={3} strokeLinecap="round" transform={`rotate(${r})`} />
              ))}
            </g>
          );
        })}
        <g transform={`translate(310 620) scale(${pop((t - 0.03) / 0.35)})`}>
          <rect x={-36} y={-230} width={72} height={330} rx={36} fill="rgba(20,18,15,0.75)" stroke={PAPEL} strokeWidth={TRACO} />
          <circle cy={140} r={62} fill="#7fb7ff" stroke={PAPEL} strokeWidth={TRACO} />
          <rect x={-16} y={-200 + 290 * (1 - nivel)} width={32} height={290 * nivel + 40} rx={16} fill="#7fb7ff" />
          {[0, 1, 2, 3].map((k) => (
            <line key={k} x1={40} y1={-180 + k * 70} x2={66} y2={-180 + k * 70} stroke={PAPEL} strokeWidth={4} />
          ))}
        </g>
      </svg>
      <Rotulos t={t} x={420} y={340} w={620} linhas={linhas} />
    </div>
  );
};

// ---------------------------------------------------------------- dica 5: o dragão embaixo do castelo
/** Castelo em traço e, embaixo do chão, o calabouço: o dragão (silhueta e olho âmbar) aparece em "dragão". */
export const Dragao: React.FC<Props> = ({ t, marcos, fundo, linhas = [] }) => {
  const md = marcos.dragao ?? 2.6;
  const mc = marcos.calabouco ?? 1.8;
  const ev = evolvePath(easeInOut(t / 0.7), "M40 560 H1040");
  const cav = ease((t - mc + 0.1) / 0.4);
  const dr = Math.max(0.55 * ease((t - mc - 0.2) / 0.5), ease((t - md + 0.05) / 0.4)); // silhueta já no calabouço; inteira em "dragão"
  const pisca = t > md + 0.6 && Math.floor((t - md) * 2.2) % 5 === 0 ? 0.2 : 1;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        {/* castelo em cima do chão */}
        <g transform={`translate(300 560) scale(${pop((t - 0.03) / 0.4)})`}>
          <path d="M-150 0 V-80 H-120 V-120 H-90 V-80 H-50 V-170 L-30 -230 L-10 -170 V-80 H10 V-170 L30 -230 L50 -170 V-80 H90 V-120 H120 V-80 H150 V0 Z" fill="rgba(20,18,15,0.6)" stroke={PAPEL} strokeWidth={TRACO} strokeLinejoin="round" />
          <path d="M-22 0 V-46 Q 0 -70 22 -46 V0" fill="none" stroke={PAPEL} strokeWidth={5} />
        </g>
        <path d="M40 560 H1040" stroke={PAPEL} strokeWidth={5} strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
        {/* calabouço */}
        <g opacity={cav}>
          <path d="M40 575 Q 300 900 560 575 Z" fill="rgba(8,7,6,0.85)" stroke={AMBAR} strokeWidth={4} strokeDasharray="14 10" />
        </g>
        {/* dragão: corpo enrolado, cabeça e olho */}
        <g opacity={dr} transform={`translate(${300 - 40 * (1 - dr)} 720) scale(0.85)`}>
          <path d="M-220 40 C -160 -40, -60 60, 0 0 S 140 -30, 180 -10" fill="none" stroke="#3f7a4f" strokeWidth={34} strokeLinecap="round" />
          <path d="M150 -40 L235 -20 L215 10 L150 10 Z" fill="#3f7a4f" />
          <path d="M150 -40 L165 -78 L182 -40 Z M180 -36 L200 -70 L210 -30 Z" fill="#3f7a4f" />
          <circle cx={200} cy={-18} r={9} fill={AMBAR} opacity={t > md ? pisca : 0.15} />
          {[-170, -110, -50, 10, 70].map((x, i) => (
            <path key={i} d={`M${x} ${i % 2 ? -8 : 6} l14 -26 l14 26`} fill="#2e5a3a" />
          ))}
        </g>
      </svg>
      <Rotulos t={t} x={600} y={300} w={450} linhas={linhas} />
    </div>
  );
};
