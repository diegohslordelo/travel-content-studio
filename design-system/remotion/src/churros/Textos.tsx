/**
 * Textos na tela do Reel dos churros. Cada linha sobe de dentro de uma máscara (curva expo) com 70 ms
 * de defasagem; a saída é um deslize curto para cima com fade. Um véu escuro no topo garante contraste
 * sobre imagens claras (balcão branco, céu) sem cobrir a comida, que fica na metade de baixo.
 * Tempos em ms relativos à Sequence do texto.
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { kf, useMs } from "../ds/tempo";
import { C, CURVA, F, SEGURO } from "./tema";

export type EstiloTexto = "gancho" | "serifa" | "lugar" | "capitulo" | "serifa_pequena" | "pergunta";

export type Texto = {
  estilo: EstiloTexto;
  linhas: string[];
  kicker?: string;
  sub?: string;
  numero?: string;
  y: number;
  /** duração total em ms (a saída acontece nos últimos 220 ms) */
  dur: number;
};

const SOMBRA_TXT = "0 6px 28px rgba(20,10,5,.55), 0 2px 6px rgba(20,10,5,.45)";

/** Linha que sobe de dentro da máscara. */
const Linha: React.FC<{ t: number; atraso: number; children: React.ReactNode; style: React.CSSProperties }> = ({ t, atraso, children, style }) => {
  const p = kf(t - atraso, [0, 520], [0, 1], CURVA.sai);
  return (
    // a folga em cima não deixa a máscara cortar acentos (Á, Ê) acima da altura da linha
    <div style={{ overflow: "hidden", paddingTop: "0.24em", marginTop: "-0.24em", paddingBottom: "0.08em", marginBottom: "-0.08em" }}>
      <div style={{ ...style, translate: `0 ${(1 - p) * 110}%`, opacity: Math.min(1, p * 3) }}>{children}</div>
    </div>
  );
};

const Veu: React.FC<{ op: number; ate?: number }> = ({ op, ate = 46 }) => (
  <AbsoluteFill
    style={{
      background: `linear-gradient(180deg, rgba(24,14,9,.62) 0%, rgba(24,14,9,.38) ${ate * 0.55}%, rgba(24,14,9,0) ${ate}%)`,
      opacity: op,
    }}
  />
);

export const TextoNaTela: React.FC<Texto> = ({ estilo, linhas, kicker, sub, numero, y, dur }) => {
  const t = useMs();
  const saida = kf(t, [dur - 220, dur], [0, 1], CURVA.entra);
  const veu = kf(t, [0, 260], [0, 1]) * (1 - saida);
  const caixa: React.CSSProperties = {
    position: "absolute",
    left: SEGURO.esq,
    right: SEGURO.dir,
    top: y,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    textAlign: "center",
    translate: `0 ${-40 * saida}px`,
    opacity: 1 - saida,
    filter: saida > 0 ? `blur(${6 * saida}px)` : undefined,
  };
  const kick: React.CSSProperties = {
    fontFamily: F.rotulo,
    fontWeight: 800,
    fontSize: 36,
    letterSpacing: "0.18em",
    color: C.douradoClaro,
    textShadow: SOMBRA_TXT,
    whiteSpace: "nowrap",
  };
  const cartaz = (tam: number): React.CSSProperties => ({
    fontFamily: F.cartaz,
    fontSize: tam,
    lineHeight: 0.98,
    letterSpacing: "0.01em",
    color: C.creme,
    textShadow: SOMBRA_TXT,
    whiteSpace: "nowrap",
  });
  const serifa = (tam: number): React.CSSProperties => ({
    fontFamily: F.serifa,
    fontStyle: "italic",
    fontSize: tam,
    lineHeight: 0.92,
    color: C.creme,
    textShadow: SOMBRA_TXT,
    whiteSpace: "nowrap",
  });

  if (estilo === "gancho")
    return (
      <AbsoluteFill>
        <Veu op={veu} ate={52} />
        <div style={caixa}>
          {kicker && (
            <Linha t={t} atraso={0} style={kick}>
              {kicker}
            </Linha>
          )}
          <div style={{ height: 18 }} />
          {linhas.map((l, i) => (
            <Linha key={i} t={t} atraso={140 + i * 90} style={cartaz(140)}>
              {l}
            </Linha>
          ))}
        </div>
      </AbsoluteFill>
    );

  if (estilo === "serifa" || estilo === "serifa_pequena") {
    const tam = estilo === "serifa" ? 200 : 104;
    // sublinhado dourado que se desenha sob a última linha
    const traco = kf(t, [260 + linhas.length * 90, 760 + linhas.length * 90], [0, 1], CURVA.sai);
    return (
      <AbsoluteFill>
        <Veu op={veu} />
        <div style={caixa}>
          {linhas.map((l, i) => (
            <Linha key={i} t={t} atraso={i * 90} style={serifa(tam)}>
              {l}
            </Linha>
          ))}
          {estilo === "serifa" && (
            <svg width={520} height={40} style={{ marginTop: 6, overflow: "visible" }}>
              <path
                d="M10,26 C140,8 300,8 510,22"
                fill="none"
                stroke={C.dourado}
                strokeWidth={9}
                strokeLinecap="round"
                pathLength={1}
                strokeDasharray="1 1"
                strokeDashoffset={1 - traco}
              />
            </svg>
          )}
        </div>
      </AbsoluteFill>
    );
  }

  if (estilo === "lugar") {
    // etiqueta de lugar na parte de baixo (acima da faixa da legenda do Instagram), com véu de baixo
    const regua = kf(t, [200, 700], [0, 1], CURVA.sai);
    return (
      <AbsoluteFill>
        <AbsoluteFill
          style={{ background: "linear-gradient(0deg, rgba(24,14,9,0) 0%, rgba(24,14,9,.6) 26%, rgba(24,14,9,.25) 40%, rgba(24,14,9,0) 52%)", opacity: veu }}
        />
        <div style={caixa}>
          {kicker && (
            <Linha t={t} atraso={0} style={kick}>
              {kicker}
            </Linha>
          )}
          <div style={{ height: 14, width: 360 * regua, borderBottom: `3px solid ${C.dourado}`, marginBottom: 22 }} />
          {linhas.map((l, i) => (
            <Linha key={i} t={t} atraso={120 + i * 90} style={cartaz(96)}>
              {l}
            </Linha>
          ))}
        </div>
      </AbsoluteFill>
    );
  }

  if (estilo === "capitulo") {
    const anel = kf(t, [0, 420], [0, 1], CURVA.sai);
    return (
      <AbsoluteFill>
        <Veu op={veu} />
        <div style={caixa}>
          {numero && (
            <div
              style={{
                width: 84,
                height: 84,
                borderRadius: 42,
                border: `3px solid ${C.dourado}`,
                display: "grid",
                placeItems: "center",
                fontFamily: F.rotulo,
                fontWeight: 800,
                fontSize: 30,
                letterSpacing: "0.06em",
                color: C.douradoClaro,
                scale: String(0.6 + 0.4 * anel),
                opacity: anel,
                marginBottom: 22,
                background: "rgba(30,18,12,.35)",
              }}
            >
              {numero}
            </div>
          )}
          {linhas.map((l, i) => (
            <Linha key={i} t={t} atraso={90 + i * 90} style={cartaz(146)}>
              {l}
            </Linha>
          ))}
          {sub && (
            <Linha t={t} atraso={260} style={{ ...serifa(72), color: C.douradoClaro, marginTop: 6 }}>
              {sub}
            </Linha>
          )}
        </div>
      </AbsoluteFill>
    );
  }

  // pergunta
  return (
    <AbsoluteFill>
      <div style={caixa}>
        {kicker && (
          <Linha t={t} atraso={0} style={{ ...serifa(120), color: C.douradoClaro }}>
            {kicker}
          </Linha>
        )}
        {linhas.map((l, i) => (
          <Linha key={i} t={t} atraso={140 + i * 100} style={cartaz(156)}>
            {l}
          </Linha>
        ))}
      </div>
    </AbsoluteFill>
  );
};
