/**
 * Ilustração esquemática da Prinsengracht 263 em corte: casa da frente, armário que esconde a passagem
 * e o anexo secreto. Não é planta: é explicação ("ILUSTRAÇÃO" fica na tela o tempo todo).
 */
import React from "react";
import { PALETA, TEXTO, TITULO, easeInOut, lerp } from "./estilo";

const CHAO = 1180;
// casa da frente
const F = { x0: 170, x1: 545, topo: 520, cume: 335 };
// anexo
const A = { x0: 655, x1: 945, topo: 650, cume: 520 };
const ANDARES = [1010, 840, 680];
// armário na entrada da passagem (1º andar)
const ARM = { x: 548, y: 862, w: 92, h: 146 };
const FOCO = { x: ARM.x + ARM.w / 2, y: ARM.y + ARM.h / 2 };
const CAMINHO = `M 300 ${ANDARES[0] - 50} L ${(A.x0 + A.x1) / 2} ${ANDARES[0] - 50} L ${(A.x0 + A.x1) / 2} ${ANDARES[1] - 60}`;

const Traco: React.FC<{ d: string; t: number; ini: number; dur?: number; comp?: number; cor?: string; largura?: number; tracejado?: boolean }> = ({
  d,
  t,
  ini,
  dur = 0.45,
  comp = 2400,
  cor = PALETA.papel,
  largura = 5,
  tracejado = false,
}) => {
  const p = lerp(t, ini, ini + dur, 0, 1, easeInOut);
  if (p <= 0) return null;
  return (
    <path
      d={d}
      fill="none"
      stroke={cor}
      strokeWidth={largura}
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeDasharray={tracejado ? undefined : comp}
      strokeDashoffset={tracejado ? undefined : comp * (1 - p)}
      style={tracejado ? { clipPath: `inset(0 ${100 - p * 100}% 0 0)` } : undefined}
    />
  );
};

export const Casa: React.FC<{ t: number; marcos: { armario: number; passagem: number; anexo: number } }> = ({ t, marcos }) => {
  const { armario, passagem, anexo } = marcos;
  // câmera: aproxima do armário quando ele é dito, afasta para mostrar a passagem
  const zoomIn = lerp(t, armario - 0.45, armario + 0.15, 1, 2.05, easeInOut);
  const zoom = t < passagem - 0.3 ? zoomIn : lerp(t, passagem - 0.3, passagem + 0.3, 2.05, 1, easeInOut);
  // o armário vai para o centro da tela à medida que a câmera aproxima
  const k = (zoom - 1) / (2.05 - 1);
  const tx = FOCO.x * (1 - k) + 540 * k - zoom * FOCO.x;
  const ty = FOCO.y * (1 - k) + 820 * k - zoom * FOCO.y;
  const abre = lerp(t, armario + 0.15, armario + 0.65, 0, 1, easeInOut); // porta-estante gira
  const caminho = lerp(t, passagem - 0.05, passagem + 0.75, 0, 1, easeInOut);
  const luzAnexo = lerp(t, anexo - 0.1, anexo + 0.35, 0, 1);
  const rotulo = (ini: number) => ({ opacity: lerp(t, ini, ini + 0.3, 0, 1), translate: `0 ${lerp(t, ini, ini + 0.3, 14, 0)}px` });

  const livros = Array.from({ length: 4 }, (_, prat) =>
    Array.from({ length: 6 }, (__, k) => ({
      x: 6 + k * 13.5,
      y: 8 + prat * 35,
      h: 22 + ((k * 7 + prat * 3) % 4) * 2.5,
      c: ["#8C6B4A", "#5E6B73", "#9A8F7C", "#6E4E3A", "#7C8467", "#A5835A"][(k + prat * 2) % 6],
    })),
  ).flat();

  return (
    <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 70% at 50% 45%, #1F1B16 0%, ${PALETA.fundo} 60%, #0A0908 100%)` }}>
      <svg viewBox="0 0 1080 1920" width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <g transform={`translate(${tx} ${ty}) scale(${zoom})`}>
          {/* canal */}
          <Traco t={t} ini={0} d={`M 40 ${CHAO - 40} Q 70 ${CHAO - 52} 100 ${CHAO - 40} T 160 ${CHAO - 40}`} cor="#6F8A93" largura={4} />
          <Traco t={t} ini={0.05} d={`M 40 ${CHAO - 14} Q 70 ${CHAO - 26} 100 ${CHAO - 14} T 160 ${CHAO - 14}`} cor="#6F8A93" largura={4} />
          {/* luz do anexo */}
          <rect x={A.x0} y={A.topo} width={A.x1 - A.x0} height={CHAO - A.topo} fill={PALETA.ambar} opacity={0.2 * luzAnexo} />
          <polygon points={`${A.x0},${A.topo} ${(A.x0 + A.x1) / 2},${A.cume} ${A.x1},${A.topo}`} fill={PALETA.ambar} opacity={0.2 * luzAnexo} />
          {/* chão */}
          <Traco t={t} ini={0} d={`M 30 ${CHAO} L 1050 ${CHAO}`} largura={4} cor={PALETA.cinza} />
          {/* casa da frente */}
          <Traco t={t} ini={0.05} d={`M ${F.x0} ${CHAO} L ${F.x0} ${F.topo} L ${(F.x0 + F.x1) / 2} ${F.cume} L ${F.x1} ${F.topo} L ${F.x1} ${ARM.y - 2}`} />
          <Traco t={t} ini={0.05} d={`M ${F.x1} ${ARM.y + ARM.h + 2} L ${F.x1} ${CHAO}`} comp={300} />
          {ANDARES.map((y, i) => (
            <Traco key={y} t={t} ini={0.15 + i * 0.05} d={`M ${F.x0} ${y} L ${F.x1} ${y}`} largura={3} cor="#A79F92" comp={400} />
          ))}
          {/* janelas da fachada (lado do canal) */}
          {[600, 760, 920, 1080].map((y, i) => (
            <rect key={y} x={F.x0 - 6} y={y} width={12} height={70} fill={PALETA.papel} opacity={lerp(t, 0.3 + i * 0.04, 0.5 + i * 0.04, 0, 0.8)} />
          ))}
          {/* passagem (corredor) */}
          <Traco t={t} ini={0.25} d={`M ${F.x1} ${ARM.y - 2} L ${A.x0} ${ARM.y - 2}`} largura={4} comp={200} />
          <Traco t={t} ini={0.25} d={`M ${F.x1} ${ANDARES[0]} L ${A.x0} ${ANDARES[0]}`} largura={4} comp={200} />
          {/* anexo */}
          <Traco t={t} ini={0.2} d={`M ${A.x0} ${ARM.y - 2} L ${A.x0} ${A.topo} L ${(A.x0 + A.x1) / 2} ${A.cume} L ${A.x1} ${A.topo} L ${A.x1} ${CHAO} L ${A.x0} ${CHAO} L ${A.x0} ${ANDARES[0]}`} />
          {ANDARES.slice(0, 2).map((y, i) => (
            <Traco key={y} t={t} ini={0.3 + i * 0.05} d={`M ${A.x0} ${y} L ${A.x1} ${y}`} largura={3} cor="#A79F92" comp={300} />
          ))}
          {/* vão escondido atrás do armário */}
          <rect x={ARM.x} y={ARM.y} width={ARM.w} height={ARM.h} fill="#050404" />
          <rect x={ARM.x + 8} y={ARM.y + 6} width={ARM.w - 16} height={ARM.h - 6} fill={PALETA.ambar} opacity={0.55 * abre} />
          {/* armário (porta-estante): gira para fora pela dobradiça da esquerda */}
          <g transform={`translate(${ARM.x} ${ARM.y}) scale(${1 - 0.82 * abre} 1)`} opacity={lerp(t, 0.35, 0.6, 0, 1)}>
            <rect x={0} y={0} width={ARM.w} height={ARM.h} fill="#3A2E24" stroke={PALETA.papel} strokeWidth={3} />
            {[35, 70, 105].map((y) => (
              <line key={y} x1={0} x2={ARM.w} y1={y} y2={y} stroke={PALETA.papel} strokeWidth={2} opacity={0.7} />
            ))}
            {livros.map((l, i) => (
              <rect key={i} x={l.x} y={l.y + (30 - l.h)} width={10} height={l.h} fill={l.c} />
            ))}
          </g>
          {/* caminho secreto: pontilhado revelado por uma máscara que avança ao longo do trajeto */}
          <defs>
            <mask id="revela-caminho" maskUnits="userSpaceOnUse" x={0} y={0} width={1080} height={1920}>
              <path d={CAMINHO} fill="none" stroke="#fff" strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - caminho} />
            </mask>
          </defs>
          <path d={CAMINHO} fill="none" stroke={PALETA.ambar} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" strokeDasharray="1 20" mask="url(#revela-caminho)" />
        </g>
      </svg>
      {/* rótulos (fora da câmera, só quando ela está aberta) */}
      <div style={{ position: "absolute", right: 72, top: CHAO + 18, font: `600 24px ${TEXTO}`, letterSpacing: 4, color: PALETA.cinza }}>ILUSTRAÇÃO</div>
      {zoom < 1.05 && (
        <>
          <div style={{ position: "absolute", left: F.x0, top: F.cume - 92, font: `700 30px ${TEXTO}`, letterSpacing: 3, color: PALETA.papel, ...rotulo(0.35) }}>
            CASA DA FRENTE
          </div>
          <div style={{ position: "absolute", left: 40, top: CHAO + 18, font: `600 24px ${TEXTO}`, letterSpacing: 3, color: "#6F8A93", ...rotulo(0.3) }}>CANAL</div>
          <div style={{ position: "absolute", left: (A.x0 + A.x1) / 2 - 280, width: 560, textAlign: "center", top: A.cume - 112, font: `400 76px ${TITULO}`, color: PALETA.ambar, ...rotulo(anexo - 0.05) }}>
            ANEXO SECRETO
          </div>
        </>
      )}
    </div>
  );
};
