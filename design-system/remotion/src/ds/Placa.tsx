/**
 * Placa "PRIMEIRO DIA →" (DS V2, 2.1): ativo nº 1.
 * Face amarela esmaltada (relevo, filete, 2 rebites, grão) + módulo de seta grafite.
 * Assinatura CHEGADA (560 ms) + brilho de esmalte (700–1300 ms), saída de 240 ms pela direita
 * e troca de texto por giro no eixo horizontal.
 *
 * Os overshoots são keyframes explícitos (como nas receitas do CapCut, 6.2), não dependem da
 * curva: metal passa no máximo 24 px do ponto (4.2).
 */
import React from "react";
import { Fibra, useDesfoqueX } from "./material";
import { Interrogacao, Polegar, Seta, Visto, Xis } from "./icones";
import { Simbolo1 } from "./Simbolo1";
import { kf, useMs } from "./tempo";
import { BLUR, COR, DUR, EASE, FONTE, RAIO, REEL, SOMBRA, TIPO, rgba } from "./tokens";

export type Modulo = "seta" | "interrogacao" | "um" | "xis" | "like";

/** Momentos do módulo de like (ms desde o início da Chegada): o polegar é "apertado" e depois vira ✓ (inscrito). */
export const LIKE_APERTA = 700;
export const LIKE_INSCRITO = 2300;

/** Módulo da chamada "DEIXA O LIKE E SE INSCREVE": aperta (82% → 112% → 100%, 360 ms) e troca por ✓ com o mesmo giro. */
const ModuloLike: React.FC<{ t: number; lado: number }> = ({ t, lado }) => {
  const d = t - LIKE_APERTA;
  const escala = d < 0 ? 1 : kf(d, [0, 80, 200, 360], [1, 0.82, 1.12, 1], [EASE.out, EASE.out, EASE.out]);
  const di = t - LIKE_INSCRITO;
  const inscrito = di >= DUR.base / 2;
  const giro = di < 0 ? 0 : di < DUR.base / 2 ? kf(di, [0, DUR.base / 2], [0, 90], EASE.cinema) : kf(di, [DUR.base / 2, DUR.base], [90, 0], EASE.cinema);
  return (
    <div style={{ scale: String(escala), transform: `perspective(600px) rotateY(${giro}deg)` }}>
      {inscrito ? <Visto tamanho={lado} cor={COR.amarelo} /> : <Polegar tamanho={lado} cor={COR.amarelo} />}
    </div>
  );
};

export type PlacaProps = {
  rotulo?: string;
  destino: string;
  modulo?: Modulo;
  /** G = 100% (Reel) · M = 75% · P = 50% (DS V2, 2.8). */
  tamanho?: "G" | "M" | "P";
  x?: number;
  y?: number;
  /** ms em que a Chegada começa. null = placa estática (brilho congelado a 30% do percurso). */
  entrada?: number | null;
  /** ms em que a saída (240 ms) começa. */
  saida?: number;
  /** Empurrões extras da seta (só no hook, 1 a cada 2,4 s). */
  empurroes?: number[];
  /** Troca de texto com a placa na tela (ex.: DIA 1 → DIA 2). */
  trocas?: { em: number; rotulo?: string; destino: string }[];
  /** Variante Carrossel (2.1): sobre papel ou foto, com `shadow-paper` (menos profunda). */
  carrossel?: boolean;
};

const ESCALA = { G: 1, M: 0.75, P: 0.5 } as const;
const PAD_V = 28; // 2.1, Anatomia: padding 28 × 36
const PAD_H = 36;
const GAP_LINHAS = 12; // distância rótulo → destino da implementação de prévia (pd-bundle.css)
const LADO_SETA = 96; // 2.1: seta amarela 96 px

const LARGURA_MAX = 872; // 2.1: largura máxima da placa
const H1_ALT = 104; // 2.1: tamanho alternativo do destino

/** Largura do texto em Barlow Condensed 800 (em), calibrada no render: letra 0,42 em, espaço 0,2 em, ponto 0,23 em. */
const larguraEm = (texto: string): number =>
  texto.split("").reduce((s, c) => s + (c === " " ? 0.2 : c === "." || c === "," ? 0.23 : 0.42), 0);

const altura = (rotulo: string | undefined, tam: number): number =>
  2 * PAD_V + (rotulo ? TIPO.label.fontSize * TIPO.label.lineHeight + GAP_LINHAS : 0) + tam * TIPO.h1.lineHeight;

/**
 * 2.1: destino 128 px; 104 px se tiver de 13 a 16 letras. Também cai para 104 px quando a placa
 * (face + módulo) passaria da largura máxima de 872 px: é o caso de "PRIMEIRO DIA." no fechamento.
 */
const tamanhoDestino = (rotulo: string | undefined, destino: string): number => {
  if (destino.replace(/[^\p{L}\p{N}]/gu, "").length >= 13) return H1_ALT;
  const tam = TIPO.h1.fontSize;
  const largura = 2 * PAD_H + larguraEm(destino) * tam + altura(rotulo, tam);
  return largura > LARGURA_MAX ? H1_ALT : tam;
};

export const alturaPlaca = (rotulo: string | undefined, destino: string): number => altura(rotulo, tamanhoDestino(rotulo, destino));

export const Placa: React.FC<PlacaProps> = ({
  rotulo,
  destino,
  modulo = "seta",
  tamanho = "G",
  x = REEL.seguroEsq,
  y = REEL.placaY,
  entrada = 0,
  saida,
  empurroes = [],
  trocas = [],
  carrossel = false,
}) => {
  const t = useMs();
  const estatica = entrada === null;
  const te = estatica ? Infinity : t - (entrada as number);
  const ts = saida === undefined ? -Infinity : t - saida;

  // texto vigente (trocas)
  let rot = rotulo;
  let dest = destino;
  let giro = 0;
  for (const tr of trocas) {
    const d = t - tr.em;
    if (d >= DUR.base / 2) {
      rot = tr.rotulo;
      dest = tr.destino;
    }
    if (d >= 0 && d < DUR.base) giro = d < DUR.base / 2 ? kf(d, [0, DUR.base / 2], [0, 90], EASE.cinema) : kf(d, [DUR.base / 2, DUR.base], [90, 0], EASE.cinema);
  }

  const desfoqueSaida = kf(ts, [80, 240], [0, BLUR.movimento], EASE.exit);
  const desfoqueEntrada = estatica ? 0 : kf(te, [0, 280], [BLUR.movimento, 0], EASE.out);
  const { defs, filter } = useDesfoqueX(Math.max(desfoqueEntrada, desfoqueSaida));

  if (!estatica && te < 0) return null;
  if (ts >= 240) return null;

  const H = alturaPlaca(rot, dest);
  const tamDest = tamanhoDestino(rot, dest);

  // CHEGADA (2.1)
  const xFace = estatica ? 0 : kf(te, [0, 280, 360, 400], [-1100, 24, -4, 0], [EASE.out, EASE.out, EASE.out]);
  const rotacao = estatica ? 0 : kf(te, [0, 280, 400], [-3, 0.6, 0], [EASE.out, EASE.out]);
  const xModulo = estatica ? 0 : kf(te, [280, 400], [-H, 0], EASE.out);
  const sombra = estatica ? 1 : kf(te, [0, 400], [0, 1], EASE.out);
  let empurrao = estatica ? 0 : kf(te, [400, 480, 560], [0, 10, 0], [EASE.out, EASE.out]);
  for (const e of empurroes) {
    const d = t - e;
    if (d >= 0 && d < 160) empurrao = kf(d, [0, 80, 160], [0, 10, 0], [EASE.out, EASE.out]);
  }
  const brilho = estatica ? 0.3 : kf(te, [700, 1300], [0, 1], EASE.cinema);
  const brilhoVisivel = estatica || (te >= 700 && te <= 1300);

  // SAÍDA (2.1 e receita 6.2): a seta empurra 80 ms, a placa sai pela direita com ease-exit
  const xSaidaModulo = kf(ts, [0, 40, 80], [0, 10, 0], [EASE.out, EASE.out]);
  const xSaida = kf(ts, [80, 240], [0, 1150], EASE.exit);

  // sombra de duas camadas, deslocada 40 px a 15% no início e assentando em 18 px a 55%
  const yS = 40 + (18 - 40) * sombra;
  const aS = 0.15 + (0.55 - 0.15) * sombra;
  const sombraPlaca = carrossel ? SOMBRA.papel : estatica ? SOMBRA.placa : `0 3px 0 rgba(0,0,0,${0.28 * sombra}), 0 ${yS}px 32px -10px rgba(0,0,0,${aS})`;

  const iconeModulo = (() => {
    switch (modulo) {
      case "interrogacao":
        return <Interrogacao tamanho={LADO_SETA} cor={COR.amarelo} />;
      case "like":
        return <ModuloLike t={estatica ? Infinity : te} lado={LADO_SETA} />;
      case "xis":
        return <Xis tamanho={LADO_SETA} cor={COR.vermelho} />;
      case "um":
        return <Simbolo1 altura={H * 0.7} t={estatica ? Infinity : te - 400} corNumero={COR.recibo} />;
      default:
        return <Seta tamanho={LADO_SETA} cor={COR.amarelo} style={{ translate: `${empurrao}px 0` }} />;
    }
  })();

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transformOrigin: "0 0",
        scale: String(ESCALA[tamanho]),
      }}
    >
      {defs}
      <div
        style={{
          display: "flex",
          alignItems: "stretch",
          translate: `${xFace + xSaida}px 0`,
          rotate: `${rotacao}deg`,
          transformOrigin: "0 50%",
          filter,
          color: COR.grafite,
        }}
      >
        {/* face */}
        <div
          style={{
            position: "relative",
            zIndex: 2,
            boxSizing: "border-box",
            height: H,
            background: COR.amarelo,
            borderRadius: `${RAIO.placa}px 0 0 ${RAIO.placa}px`,
            padding: `${PAD_V}px ${PAD_H}px`,
            boxShadow: `${sombraPlaca}, ${SOMBRA.relevo}`,
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            transform: `perspective(1200px) rotateX(${giro}deg)`,
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: 10,
              border: `2px solid ${rgba(COR.grafite, 0.25)}`,
              borderRight: 0,
              borderRadius: "8px 0 0 8px",
              pointerEvents: "none",
            }}
          />
          {[{ top: 22 }, { bottom: 22 }].map((pos, i) => (
            <i
              key={i}
              style={{
                position: "absolute",
                left: 22,
                width: 10,
                height: 10,
                borderRadius: "50%",
                ...pos,
                background: `radial-gradient(circle at 35% 30%, rgba(255,255,255,.6) 0 2px, rgba(255,255,255,0) 3px), ${rgba(COR.grafite, 0.35)}`,
                boxShadow: "inset 0 -1px 0 rgba(0,0,0,.35)",
              }}
            />
          ))}
          <Fibra opacidade={0.05} semente={11} />
          {brilhoVisivel && (
            <span
              style={{
                position: "absolute",
                top: "-20%",
                bottom: "-20%",
                left: 0,
                width: "34%",
                background: "linear-gradient(100deg, rgba(255,255,255,0), rgba(255,255,255,.4) 50%, rgba(255,255,255,0))",
                transform: `translateX(${-160 + brilho * 480}%) skewX(-14deg)`,
                mixBlendMode: "soft-light",
                pointerEvents: "none",
              }}
            />
          )}
          {rot && (
            <div
              style={{
                fontFamily: FONTE.display,
                fontWeight: TIPO.label.fontWeight,
                fontSize: TIPO.label.fontSize,
                lineHeight: TIPO.label.lineHeight,
                letterSpacing: TIPO.label.letterSpacing,
                textTransform: "uppercase",
                whiteSpace: "nowrap",
              }}
            >
              {rot}
            </div>
          )}
          <div
            style={{
              fontFamily: FONTE.display,
              fontWeight: TIPO.h1.fontWeight,
              fontSize: tamDest,
              lineHeight: TIPO.h1.lineHeight,
              letterSpacing: TIPO.h1.letterSpacing,
              textTransform: "uppercase",
              whiteSpace: "nowrap",
              marginTop: rot ? GAP_LINHAS : 0,
            }}
          >
            {dest}
          </div>
        </div>
        {/* módulo (sai de trás da face) */}
        <div
          style={{
            position: "relative",
            zIndex: 1,
            width: H,
            height: H,
            flex: "none",
            display: "grid",
            placeItems: "center",
            background: modulo === "xis" ? COR.papel : COR.grafite,
            borderRadius: `0 ${RAIO.placa}px ${RAIO.placa}px 0`,
            boxShadow: `${sombraPlaca}, inset 0 0 0 2px rgba(255,255,255,.08)`,
            translate: `${xModulo + xSaidaModulo}px 0`,
            overflow: "hidden",
          }}
        >
          {iconeModulo}
        </div>
      </div>
    </div>
  );
};
