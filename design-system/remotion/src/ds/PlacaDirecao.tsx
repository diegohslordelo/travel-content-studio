/**
 * Placa de direção (DS V2, 2.6, "Distância / tempo"): placa pequena grafite com o destino em H3, a linha
 * de distância/tempo em Plex Mono amarelo e a seta de direção (1.6: seta de placa a 45° ↗ ou a 90° ↑).
 * Entrada: Chegada curta (320 ms). Saída: a da Placa (2.1), 240 ms pela direita.
 *
 * O DS não detalha a anatomia desta placa. A implementação reaproveita a da Placa (2.1: padding 28 × 36,
 * raio da placa, módulo quadrado com lado = altura do conteúdo, seta "pequena" de 72 px) e o material
 * Painel (1.4: grafite 900 + filete claro de 2 px a 8% + shadow-plate), porque a face é grafite.
 * Nenhum valor novo: ver README, "Decisões de implementação".
 */
import React from "react";
import { useDesfoqueX } from "./material";
import { Seta } from "./icones";
import { kf, useMs } from "./tempo";
import { BLUR, COR, DUR, EASE, FONTE, RAIO, REEL, SOMBRA, TIPO } from "./tokens";

export type PlacaDirecaoProps = {
  /** Destino em H3 (CAIXA-ALTA). */
  destino: string;
  /** Linha de distância/tempo em Plex Mono (ex.: "1,2 KM · 15 MIN"). */
  linha: string;
  /** Seta de direção: 45° (↗, padrão do 2.6) ou 90° (↑). */
  seta?: "diagonal" | "cima";
  x?: number;
  y?: number;
  /** ms em que a Chegada curta começa. null = placa estática. */
  entrada?: number | null;
  /** ms em que a saída (240 ms) começa. */
  saida?: number;
};

const PAD_V = 28; // 2.1, Anatomia: padding 28 × 36
const PAD_H = 36;
const GAP_LINHAS = 12; // o mesmo da Placa (Placa.tsx)
const LADO_SETA = 72; // 2.1, variante Pequena: seta 72 px
const FILETE = "rgba(255,255,255,.08)"; // 1.1 e 1.4: filete claro de 2 px do Painel (placar, quadro)
const CURTA = 320 / DUR.arrive; // Chegada curta (2.6): 320 ms em vez de 560 ms

/** Altura da placa: padding + destino (H3) + distância entre as linhas + linha em Plex Mono. */
export const alturaPlacaDirecao = (): number =>
  2 * PAD_V + TIPO.h3.fontSize * TIPO.h3.lineHeight + GAP_LINHAS + TIPO.micro.fontSize * TIPO.micro.lineHeight;

export const PlacaDirecao: React.FC<PlacaDirecaoProps> = ({
  destino,
  linha,
  seta = "diagonal",
  x = REEL.seguroEsq,
  y = REEL.placaY,
  entrada = 0,
  saida,
}) => {
  const t = useMs();
  const estatica = entrada === null;
  const te = estatica ? Infinity : t - (entrada as number);
  const ts = saida === undefined ? -Infinity : t - saida;

  // os tempos da Chegada (2.1: 280 · 360 · 400 · 480 · 560 ms) comprimidos para 320 ms
  const c = (ms: number) => ms * CURTA;
  const desfoqueEntrada = estatica ? 0 : kf(te, [0, c(280)], [BLUR.movimento, 0], EASE.out);
  const desfoqueSaida = kf(ts, [80, 240], [0, BLUR.movimento], EASE.exit);
  const { defs, filter } = useDesfoqueX(Math.max(desfoqueEntrada, desfoqueSaida));

  if (!estatica && te < 0) return null;
  if (ts >= 240) return null;

  const H = alturaPlacaDirecao();
  // CHEGADA curta: passa 24 px do ponto (metal, 4.2) e assenta; depois a seta empurra 10 px na direção dela
  const xPlaca = estatica ? 0 : kf(te, [0, c(280), c(360), c(400)], [-1100, 24, -4, 0], [EASE.out, EASE.out, EASE.out]);
  const rotacao = estatica ? 0 : kf(te, [0, c(280), c(400)], [-3, 0.6, 0], [EASE.out, EASE.out]);
  const sombra = estatica ? 1 : kf(te, [0, c(400)], [0, 1], EASE.out);
  const empurraoEntrada = estatica ? 0 : kf(te, [c(400), c(480), c(560)], [0, 10, 0], [EASE.out, EASE.out]);
  // SAÍDA (2.1 e receita 6.2): a seta empurra 80 ms e a placa sai pela direita com ease-exit
  const empurraoSaida = kf(ts, [0, 40, 80], [0, 10, 0], [EASE.out, EASE.out]);
  const xSaida = kf(ts, [80, 240], [0, 1150], EASE.exit);
  const empurrao = Math.max(empurraoEntrada, empurraoSaida);
  const angulo = seta === "cima" ? -90 : -45;
  const rad = (angulo * Math.PI) / 180;

  // sombra de duas camadas assentando (como na Placa): 40 px a 15% → 18 px a 55%
  const yS = 40 + (18 - 40) * sombra;
  const aS = 0.15 + (0.55 - 0.15) * sombra;
  const sombraPlaca = estatica ? SOMBRA.placa : `0 3px 0 rgba(0,0,0,${0.28 * sombra}), 0 ${yS}px 32px -10px rgba(0,0,0,${aS})`;

  return (
    <div style={{ position: "absolute", left: x, top: y }}>
      {defs}
      <div
        style={{
          display: "flex",
          alignItems: "stretch",
          height: H,
          translate: `${xPlaca + xSaida}px 0`,
          rotate: `${rotacao}deg`,
          transformOrigin: "0 50%",
          filter,
          background: COR.grafite,
          borderRadius: RAIO.placa,
          boxShadow: `${sombraPlaca}, inset 0 0 0 2px ${FILETE}`,
        }}
      >
        <div
          style={{
            boxSizing: "border-box",
            padding: `${PAD_V}px ${PAD_H}px`,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            whiteSpace: "nowrap",
          }}
        >
          <div
            style={{
              fontFamily: FONTE.display,
              fontWeight: TIPO.h3.fontWeight,
              fontSize: TIPO.h3.fontSize,
              lineHeight: TIPO.h3.lineHeight,
              letterSpacing: TIPO.h3.letterSpacing,
              textTransform: "uppercase",
              color: COR.papel,
            }}
          >
            {destino}
          </div>
          <div
            style={{
              marginTop: GAP_LINHAS,
              fontFamily: FONTE.mono,
              fontWeight: TIPO.micro.fontWeight,
              fontSize: TIPO.micro.fontSize,
              lineHeight: TIPO.micro.lineHeight,
              letterSpacing: TIPO.micro.letterSpacing,
              textTransform: "uppercase",
              color: COR.amarelo,
            }}
          >
            {linha}
          </div>
        </div>
        {/* módulo da seta: mesma peça, separado pelo filete claro */}
        <div
          style={{
            width: H,
            flex: "none",
            display: "grid",
            placeItems: "center",
            boxShadow: `inset 2px 0 0 ${FILETE}`,
          }}
        >
          <Seta
            tamanho={LADO_SETA}
            cor={COR.amarelo}
            style={{
              rotate: `${angulo}deg`,
              translate: `${empurrao * Math.cos(rad)}px ${empurrao * Math.sin(rad)}px`,
            }}
          />
        </div>
      </div>
    </div>
  );
};
