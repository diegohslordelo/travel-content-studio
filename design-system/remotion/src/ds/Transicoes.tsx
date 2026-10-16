/**
 * Transições (DS V2, 4.4). Regra geral: 70% dos cortes são secos; no máx. 3 famílias e 5 transições
 * por Reel de até 30 s; nunca duas seguidas sem 1,5 s de cena entre elas.
 * Todas recebem `corte`: o ms do corte entre as cenas, no relógio da Sequence.
 */
import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";
import { Fibra, useDesfoqueX } from "./material";
import { Seta } from "./icones";
import { kf, useMs } from "./tempo";
import { BLUR, COR, EASE, EFEITO, FONTE, SOMBRA, TIPO } from "./tokens";

/** Varredura de Placa (320 ms): painel amarelo com o módulo de seta na borda dianteira atravessa → ; corte aos 160 ms. */
export const Varredura: React.FC<{ corte: number }> = ({ corte }) => {
  const t = useMs() - (corte - 160);
  if (t < 0 || t > 320) return null;
  const x = kf(t, [0, 320], [-1180, 1180], EASE.cinema);
  return (
    <div style={{ position: "absolute", top: -40, bottom: -40, left: 0, width: 1180, translate: `${x}px 0`, background: COR.amarelo, boxShadow: SOMBRA.relevo, overflow: "hidden" }}>
      <Fibra opacidade={0.05} semente={13} />
      <div style={{ position: "absolute", right: 0, top: 0, bottom: 0, width: 180, background: COR.grafite, display: "grid", placeItems: "center" }}>
        <Seta tamanho={110} cor={COR.amarelo} />
      </div>
    </div>
  );
};

/** Snap (100 ms): 1 quadro de flash papel a 30% no corte. Use com `useSnapZoom` na cena que entra. */
export const FlashSnap: React.FC<{ corte: number }> = ({ corte }) => {
  const t = useMs() - corte;
  const { fps } = useVideoConfig();
  if (t < 0 || t >= 1000 / fps) return null;
  return <AbsoluteFill style={{ background: COR.recibo, opacity: EFEITO.flash }} />;
};

/** Zoom do Snap na cena que entra: 104% → 100% em 3 quadros. */
export const useSnapZoom = (corte: number): number => {
  const t = useMs() - corte;
  const { fps } = useVideoConfig();
  return t < 0 ? 1 : kf(t, [0, (3 * 1000) / fps], [EFEITO.zoomSutil, 1], EASE.out);
};

/** Cinema (700 ms): escurece até grafite em 300 ms, 2 quadros de preto, abre em 400 ms com vazamento de luz quente (8%). O corte acontece no preto. */
export const Cinema: React.FC<{ corte: number }> = ({ corte }) => {
  const { fps } = useVideoConfig();
  const q = 1000 / fps;
  const t = useMs() - (corte - 300 - q);
  if (t < 0 || t > 700 + 2 * q + 400) return null;
  const escuro = t < 300 ? kf(t, [0, 300], [0, 1], EASE.cinema) : t < 300 + 2 * q ? 1 : kf(t, [300 + 2 * q, 700 + 2 * q], [1, 0], EASE.cinema);
  const leak = kf(t, [300 + 2 * q, 500 + 2 * q, 1100 + 2 * q], [0, 1, 0], [EASE.out, EASE.out]);
  return (
    <>
      <AbsoluteFill style={{ background: COR.grafite, opacity: escuro }} />
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse at 85% 20%, rgba(255,170,90,1), rgba(255,170,90,0) 60%)",
          mixBlendMode: "screen",
          opacity: leak * EFEITO.lightLeak,
        }}
      />
    </>
  );
};

/**
 * Arrasto (200 ms, 6 quadros): chicote horizontal com desfoque direcional de 12 px. As duas cenas
 * deslizam para a esquerda e estão 30% deslocadas no instante do corte (a que sai em −30%, a que
 * entra em +30%). Para não abrir buraco preto, cada cena precisa de uma alça de 100 ms do outro lado
 * do corte (a que sai continua até −60%, a que entra começa em +60% por baixo dela).
 * `corte` = ms do corte no relógio da Sequence da cena (que já inclui a alça).
 */
export const CenaArrasto: React.FC<{ corte: number; papel: "sai" | "entra"; children: React.ReactNode }> = ({ corte, papel, children }) => {
  const t = useMs() - corte;
  const { width } = useVideoConfig();
  const u = kf(t, [-100, 100], [0, 1]);
  const e = EASE.cinema(u);
  const ativo = t > -100 && t < 100;
  const x = papel === "sai" ? -0.6 * width * e : 0.6 * width * (1 - e);
  const { defs, filter } = useDesfoqueX(ativo ? BLUR.movimento * Math.sin(Math.PI * u) : 0);
  const z = papel === "sai" ? 1 : t < 0 ? 0 : 2;
  return (
    <AbsoluteFill style={{ translate: `${x}px 0`, filter, zIndex: z }}>
      {defs}
      {children}
    </AbsoluteFill>
  );
};

/**
 * Rota (500 ms): uma linha amarela contínua de 8 px se desenha atravessando a tela (cantos em 45°) e a
 * nova cena se revela seguindo a linha; as coordenadas aparecem no ponto final.
 */
export const CenaRota: React.FC<{ corte: number; coordenadas?: string; children: React.ReactNode }> = ({ corte, coordenadas, children }) => {
  const t = useMs() - corte;
  const p = kf(t, [0, 500], [0, 1], EASE.cinema);
  if (t < 0) return null;
  // percurso: entra pela esquerda em y 1180, sobe a 45° e sai pela direita em y 700
  const pontos: [number, number][] = [
    [-20, 1180],
    [380, 1180],
    [860, 700],
    [1100, 700],
  ];
  const comp = pontos.slice(1).reduce((s, pt, i) => s + Math.hypot(pt[0] - pontos[i][0], pt[1] - pontos[i][1]), 0);
  let resta = p * comp;
  let ponta = pontos[0];
  for (let i = 1; i < pontos.length && resta > 0; i++) {
    const [ax, ay] = pontos[i - 1];
    const [bx, by] = pontos[i];
    const l = Math.hypot(bx - ax, by - ay);
    const f = Math.min(1, resta / l);
    ponta = [ax + (bx - ax) * f, ay + (by - ay) * f];
    resta -= l;
  }
  const revela = t >= 500 ? 100 : (ponta[0] / 1080) * 100;
  const coordOpac = kf(t, [400, 560], [0, 1], EASE.out) * kf(t, [900, 1100], [1, 0], EASE.out);
  return (
    <>
      <AbsoluteFill style={{ clipPath: `inset(0 ${100 - Math.max(0, revela)}% 0 0)` }}>{children}</AbsoluteFill>
      {t < 1100 && (
        <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: kf(t, [700, 1100], [1, 0]) }}>
          <polyline
            points={pontos.map((pt) => pt.join(",")).join(" ")}
            fill="none"
            stroke={COR.amarelo}
            strokeWidth={8}
            strokeLinejoin="round"
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1 - p}
          />
        </svg>
      )}
      {coordenadas && (
        <div
          style={{
            position: "absolute",
            right: 136 + 8,
            top: 700 - 64,
            fontFamily: FONTE.mono,
            fontWeight: TIPO.micro.fontWeight,
            fontSize: TIPO.micro.fontSize,
            letterSpacing: "0.02em",
            color: COR.amarelo,
            textShadow: "0 2px 0 rgba(0,0,0,.35), 0 0 24px rgba(0,0,0,.45)",
            opacity: coordOpac,
            whiteSpace: "pre",
          }}
        >
          {coordenadas}
        </div>
      )}
    </>
  );
};
