/**
 * Cards de informação como objetos (DS V2, 2.6): Recibo (preço) e Etiqueta de valor (preço rápido).
 * Valores sempre em € e R$ com cotação datada (7.1). Nunca inventar nem arredondar sem "≈".
 */
import React from "react";
import { Fibra } from "./material";
import { TextoGiro } from "./Legendas";
import { SomMoeda } from "./Som";
import { kf, useMs } from "./tempo";
import { COR, DUR, EASE, FONTE, REEL, SOMBRA } from "./tokens";

/** Etiqueta de valor: mini-recibo de 1 linha, € PD Placar 64 + ≈ R$ Barlow 500 40, picote no topo. Desliza da esquerda em 160 ms. */
export const EtiquetaValor: React.FC<{
  euro: string;
  real: string;
  rotulo?: string;
  ini: number;
  fim: number;
  x?: number;
  y?: number;
}> = ({ euro, real, rotulo, ini, fim, x = REEL.seguroEsq, y = 1090 }) => {
  const t = useMs();
  if (t < ini || t > fim + DUR.base) return null;
  const entra = kf(t - ini, [0, DUR.fast], [0, 1], EASE.out);
  const sai = kf(t - fim, [0, DUR.base], [0, 1], EASE.exit);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        display: "inline-flex",
        flexDirection: "column",
        gap: 6,
        background: COR.recibo,
        padding: "20px 30px 18px",
        borderTop: `5px dotted ${COR.concreto}`,
        borderRadius: 2,
        boxShadow: SOMBRA.papel,
        color: COR.grafite,
        translate: `${(1 - entra) * -140 + sai * 1100}px 0`,
        opacity: entra * (1 - sai),
      }}
    >
      {rotulo && (
        <div
          style={{
            fontFamily: FONTE.mono,
            fontWeight: 500,
            fontSize: 24,
            letterSpacing: "0.08em",
            color: COR.asfalto,
            textTransform: "uppercase",
          }}
        >
          {rotulo}
        </div>
      )}
      <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
        <span
          style={{
            fontFamily: FONTE.dados,
            fontWeight: 700,
            fontSize: 64,
            lineHeight: 1,
          }}
        >
          <TextoGiro valor={euro} t={t - ini} />
        </span>
        <span
          style={{
            fontFamily: FONTE.texto,
            fontWeight: 500,
            fontSize: 40,
            color: COR.asfalto,
          }}
        >
          {real}
        </span>
      </div>
    </div>
  );
};

export type ReciboProps = {
  lugar: string;
  /** Linha do cabeçalho em Plex Mono: hora, data. */
  cabecalho: string;
  linhas: [string, string][];
  total: string;
  real: string;
  /** "cotação € 1 = R$ X,XX · DD/MM" */
  rodape: string;
  ini: number;
  fim: number;
  x?: number;
  y?: number;
  /** Liga o som do Recibo (padrão): máquina de moeda quando ele aparece. Desligue só para evitar dois sons a menos de 1,5 s (ex.: soma do Placar no mesmo instante). */
  som?: boolean;
  /** Loudness da voz na cena (LUFS), referência dos volumes da 4.6. Padrão: −16. */
  refLufs?: number;
  /**
   * Correção de valor falado errado (vídeo longo de Amsterdam, pedido do Diego, 21/10/2026): em `em` ms um
   * traço de marcador risca o total e, embaixo, a correção é escrita à mão (revelada da esquerda para a direita).
   * A cor vem da camada de efeitos (não é cor do DS).
   */
  correcao?: { em: number; nota: string; cor: string };
};

const DENTE = 16; // 1.4: borda inferior serrilhada, dentes de 16 px

/** Recibo de papel térmico (600 px): sai "impresso" de cima para baixo (máscara 320 ms); o total gira depois. */
/** Recibo (decisão do Diego, 16/10/2026): TODA vez que aparece, toca a máquina de moeda (sem a impressora). */
export const Recibo: React.FC<ReciboProps> = ({
  som = true,
  refLufs = -16,
  ...p
}) => (
  <>
    <ReciboVisual {...p} />
    {som && <SomMoeda em={p.ini} refLufs={refLufs} />}
  </>
);

const ReciboVisual: React.FC<Omit<ReciboProps, "som" | "refLufs">> = ({
  correcao,
  lugar,
  cabecalho,
  linhas,
  total,
  real,
  rodape,
  ini,
  fim,
  x = 240,
  y = 300,
}) => {
  const t = useMs();
  if (t < ini || t > fim + DUR.base) return null;
  const imprime = kf(t - ini, [0, 320], [0, 1], EASE.out);
  const sai = kf(t - fim, [0, DUR.base], [0, 1], EASE.exit);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: 600,
        color: COR.grafite,
        filter:
          "drop-shadow(0 1px 1px rgba(0,0,0,.18)) drop-shadow(0 14px 16px rgba(0,0,0,.35))",
        clipPath: `inset(0 0 ${(1 - imprime) * 100}% 0)`,
        translate: `${sai * 1100}px ${(1 - imprime) * -30}px`,
        opacity: 1 - sai,
      }}
    >
      <div
        style={{
          position: "relative",
          background: COR.recibo,
          padding: "40px 44px 26px",
          opacity: 0.92,
        }}
      >
        <Fibra semente={4} />
        <div
          style={{
            fontFamily: FONTE.mono,
            fontWeight: 500,
            fontSize: 26,
            lineHeight: 1.35,
            letterSpacing: "0.04em",
            textTransform: "uppercase",
            color: COR.asfalto,
            paddingBottom: 18,
            borderBottom: `3px dashed ${COR.concreto}`,
          }}
        >
          <div
            style={{
              fontFamily: FONTE.display,
              fontWeight: 700,
              fontSize: 52,
              lineHeight: 1,
              letterSpacing: "0.02em",
              color: COR.grafite,
              marginBottom: 10,
            }}
          >
            {lugar}
          </div>
          {cabecalho}
        </div>
        {linhas.map(([item, v], i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "baseline",
              paddingTop: 16,
              fontFamily: FONTE.texto,
              fontWeight: 500,
              fontSize: 38,
              lineHeight: 1.1,
            }}
          >
            <span>{item}</span>
            <span
              style={{
                fontFamily: FONTE.dados,
                fontWeight: 700,
                fontSize: 42,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {v}
            </span>
          </div>
        ))}
        <div
          style={{
            marginTop: 22,
            paddingTop: 18,
            borderTop: `3px solid ${COR.grafite}`,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-end",
          }}
        >
          <span
            style={{
              fontFamily: FONTE.display,
              fontWeight: 600,
              fontSize: 32,
              letterSpacing: "0.08em",
            }}
          >
            TOTAL
          </span>
          <div style={{ textAlign: "right", position: "relative" }}>
            {correcao && t >= ini + correcao.em && (
              <svg width={330} height={150} viewBox="0 0 330 150" style={{ position: "absolute", right: -14, top: -8, overflow: "visible" }}>
                <path
                  d="M6 92 C 90 70, 200 52, 322 30"
                  fill="none"
                  stroke={correcao.cor}
                  strokeWidth={11}
                  strokeLinecap="round"
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={1 - kf(t - ini - correcao.em, [0, 220], [0, 1], EASE.out)}
                  opacity={0.9}
                />
              </svg>
            )}
            <div
              style={{
                fontFamily: FONTE.dados,
                fontWeight: 700,
                fontSize: 96,
                lineHeight: 0.85,
              }}
            >
              <TextoGiro valor={total} t={t - ini - 320} />
            </div>
            <div
              style={{
                fontFamily: FONTE.texto,
                fontWeight: 500,
                fontSize: 40,
                color: COR.asfalto,
                marginTop: 10,
              }}
            >
              {real}
            </div>
          </div>
        </div>
        {correcao && (
          <div
            style={{
              height: 74,
              marginTop: 10,
              fontFamily: FONTE.caneta,
              fontSize: 54,
              lineHeight: "74px",
              color: correcao.cor,
              whiteSpace: "nowrap",
              rotate: "-2deg",
              clipPath: `inset(0 ${100 - kf(t - ini - correcao.em - 260, [0, DUR.slow], [0, 100], EASE.out)}% 0 0)`,
            }}
          >
            {correcao.nota}
          </div>
        )}
        <div
          style={{
            fontFamily: FONTE.mono,
            fontWeight: 500,
            fontSize: 24,
            lineHeight: 1.3,
            color: COR.asfalto,
            marginTop: 22,
            letterSpacing: "0.03em",
          }}
        >
          {rodape}
        </div>
      </div>
      <div
        style={{
          height: DENTE,
          opacity: 0.92,
          background: `linear-gradient(-45deg, transparent ${DENTE / 2}px, ${COR.recibo} 0) 0 0 / ${DENTE}px ${DENTE}px repeat-x, linear-gradient(45deg, transparent ${DENTE / 2}px, ${COR.recibo} 0) 0 0 / ${DENTE}px ${DENTE}px repeat-x`,
        }}
      />
    </div>
  );
};
