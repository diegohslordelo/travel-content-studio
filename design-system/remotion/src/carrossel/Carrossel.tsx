/**
 * Carrossel 1080 × 1440 (DS V2, 5.3): um slide por still, a partir de carrosseis/<carrossel>/revN/revN.json.
 * Nenhuma decisão de conteúdo mora aqui: textos, fotos e paradas vêm das props. Este arquivo só aplica o DS.
 *
 * Em todo slide: etiqueta de série no canto superior esquerdo, contador `02 / 07` em Plex Mono no direito
 * (x 1000, y 80) e a Rota (linha amarela contínua de 8 px) atravessando a borda direita em y 1360,
 * para continuar no slide seguinte.
 */
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Bilhete } from "../ds/Bilhete";
import { Fibra } from "../ds/material";
import { Placa, alturaPlaca } from "../ds/Placa";
import { Simbolo1 } from "../ds/Simbolo1";
import { CAR, COR, FONTE, RAIO, SOMBRA, TIPO } from "../ds/tokens";

const ROTA_Y = 1360; // 5.3: a Rota cruza a borda direita na mesma altura em todos os slides
const ROTA_ESP = 8; // 1.6: linha contínua de 8 px
const PARADA = 56; // 1.6: número de parada, círculo grafite 56 px
const PONTO = 24; // 1.6: paradas da Rota como círculos de 24 px
const CONTADOR_X = 1000; // 1.3: contador alinhado à direita em x 1000 · y 80
const TOPO = 80;
const ETIQUETA_ALT = 48; // 2.7: etiqueta de série, mini-placa de 48 px
const SIMBOLO = 96; // 5.3: símbolo 1º de 96 px no encerramento, x 904 · y 1264
const SOMBRA_TEXTO = "0 2px 0 rgba(0,0,0,.35), 0 0 24px rgba(0,0,0,.45)"; // 3.1 (texto sobre foto)

export type Parada = {
  /** Número da parada; sem número = ponto de passagem (círculo de 24 px). */
  n?: number;
  hora: string;
  lugar: string;
  nota: string;
};

export type Slide =
  | { tipo: "capa"; foto: string; rotulo?: string; destino: string; coordenadas: string }
  | { tipo: "roteiro"; titulo: string; paradas: Parada[] }
  | { tipo: "foto"; foto: string; legenda: string }
  | { tipo: "dica"; texto: string; pictograma?: "a-pe" }
  | { tipo: "encerramento"; bilhete: string; marca?: "vale" | "pula" | "circulo"; cta: string };

export type PropsCarrossel = {
  serie: string;
  slides: Slide[];
  /** Slide renderizado (0 = capa). */
  indice: number;
};

export const propsCarrosselVazias: PropsCarrossel = {
  serie: "ROTEIRO",
  slides: [{ tipo: "roteiro", titulo: "", paradas: [] }],
  indice: 0,
};

/** Etiqueta de série (2.7): mini-placa amarela de 48 px, Condensed 600 28 px +8%, sem módulo. */
const EtiquetaSerie: React.FC<{ texto: string }> = ({ texto }) => (
  <div
    style={{
      position: "absolute",
      left: CAR.margem,
      top: TOPO,
      height: ETIQUETA_ALT,
      boxSizing: "border-box",
      padding: "0 16px",
      display: "flex",
      alignItems: "center",
      background: COR.amarelo,
      borderRadius: RAIO.tag,
      boxShadow: `${SOMBRA.papel}, ${SOMBRA.relevo}`,
      color: COR.grafite,
      fontFamily: FONTE.display,
      fontWeight: TIPO.h3.fontWeight,
      fontSize: 28,
      letterSpacing: TIPO.label.letterSpacing,
      textTransform: "uppercase",
      overflow: "hidden",
    }}
  >
    <Fibra opacidade={0.05} semente={5} />
    <span style={{ position: "relative" }}>{texto}</span>
  </div>
);

/** Contador `02 / 07` (1.3): Plex Mono 30 px, alinhado à direita em x 1000, na altura da etiqueta. */
const Contador: React.FC<{ i: number; total: number; sobreFoto?: boolean }> = ({ i, total, sobreFoto }) => (
  <div
    style={{
      position: "absolute",
      right: CAR.largura - CONTADOR_X,
      top: TOPO,
      height: ETIQUETA_ALT,
      display: "flex",
      alignItems: "center",
      fontFamily: FONTE.mono,
      fontWeight: TIPO.micro.fontWeight,
      fontSize: TIPO.micro.fontSize,
      letterSpacing: TIPO.micro.letterSpacing,
      color: sobreFoto ? COR.recibo : COR.grafite,
      textShadow: sobreFoto ? SOMBRA_TEXTO : undefined,
      fontVariantNumeric: "tabular-nums",
    }}
  >
    {String(i + 1).padStart(2, "0")} / {String(total).padStart(2, "0")}
  </div>
);

/**
 * A Rota (1.6 e 5.3): linha amarela contínua de 8 px, cantos em 45°. `pontos` em px; o último ponto
 * costuma estar na borda direita (y 1360), para a linha continuar no slide seguinte.
 */
const LinhaRota: React.FC<{ pontos: [number, number][] }> = ({ pontos }) => (
  <svg width={CAR.largura} height={CAR.altura} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
    <polyline
      points={pontos.map(([x, y]) => `${x},${y}`).join(" ")}
      fill="none"
      stroke={COR.amarelo}
      strokeWidth={ROTA_ESP}
      strokeLinejoin="miter"
      strokeLinecap="butt"
    />
  </svg>
);

const Papel: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: COR.papel }}>
    <Fibra />
    {children}
  </AbsoluteFill>
);

/** Pictograma "a pé" (1.5): quadrado grafite `radius-tag`, figura amarela; grid 48 com ícone de 36, em escala 2×. */
const PictogramaAPe: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 96,
      height: 96,
      borderRadius: RAIO.tag,
      background: COR.grafite,
      boxShadow: SOMBRA.papel,
      display: "grid",
      placeItems: "center",
    }}
  >
    <svg viewBox="0 0 36 36" width={72} height={72} aria-label="a pé">
      <circle cx={19.5} cy={4.6} r={3.4} fill={COR.amarelo} />
      <g fill="none" stroke={COR.amarelo} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round">
        <path d="M18.6 11.2 L16.4 21.2" />
        <path d="M18.4 12 L12.6 15.6 L10.4 20" />
        <path d="M18.4 12 L22.6 16.6 L27 17.6" />
        <path d="M16.4 21.2 L20.6 26 L20.8 33" />
        <path d="M16.4 21.2 L13.6 27 L8.6 31.6" />
      </g>
    </svg>
  </div>
);

const SlideCapa: React.FC<{ s: Extract<Slide, { tipo: "capa" }> }> = ({ s }) => {
  const base = 1240; // 5.3: Placa G na base esquerda, x 80 · base y 1240
  const h = alturaPlaca(s.rotulo, s.destino);
  return (
    <AbsoluteFill>
      <Img src={staticFile(s.foto)} style={{ width: CAR.largura, height: CAR.altura, objectFit: "cover" }} />
      <div
        style={{
          position: "absolute",
          left: CAR.margem,
          top: base - h - 24 - TIPO.micro.fontSize * TIPO.micro.lineHeight,
          fontFamily: FONTE.mono,
          fontWeight: TIPO.micro.fontWeight,
          fontSize: TIPO.micro.fontSize,
          lineHeight: TIPO.micro.lineHeight,
          letterSpacing: TIPO.micro.letterSpacing,
          color: COR.recibo,
          textShadow: SOMBRA_TEXTO,
          whiteSpace: "pre",
        }}
      >
        {s.coordenadas}
      </div>
      <Placa rotulo={s.rotulo} destino={s.destino} x={CAR.margem} y={base - h} entrada={null} carrossel />
      <LinhaRota pontos={[[CAR.margem, ROTA_Y], [CAR.largura, ROTA_Y]]} />
    </AbsoluteFill>
  );
};

const SlideRoteiro: React.FC<{ s: Extract<Slide, { tipo: "roteiro" }> }> = ({ s }) => {
  const xLinha = CAR.margem + PARADA / 2;
  const xTexto = CAR.margem + PARADA + 32;
  const topoParadas = 360;
  const passo = 248;
  const ys = s.paradas.map((_, i) => topoParadas + i * passo);
  const canto = 28;
  const centroH3 = TIPO.micro.fontSize * TIPO.micro.lineHeight + 8 + TIPO.h3.fontSize / 2; // hora + respiro + meia linha do lugar
  return (
    <Papel>
      <div
        style={{
          position: "absolute",
          left: CAR.margem,
          top: 176,
          width: CAR.largura - 2 * CAR.margem,
          fontFamily: FONTE.display,
          fontWeight: TIPO.h2.fontWeight,
          fontSize: TIPO.h2.fontSize,
          lineHeight: TIPO.h2.lineHeight,
          letterSpacing: TIPO.h2.letterSpacing,
          color: COR.grafite,
        }}
      >
        {s.titulo}
      </div>
      {/* a linha vem da borda esquerda (slide anterior), desce pelas paradas e sai pela direita em y 1360 */}
      <LinhaRota pontos={[[0, ROTA_Y], [xLinha + canto, ROTA_Y], [CAR.largura, ROTA_Y]]} />
      <LinhaRota pontos={[[xLinha, ys[0] + centroH3], [xLinha, ROTA_Y - canto], [xLinha + canto, ROTA_Y]]} />
      {s.paradas.map((p, i) => {
        const y = ys[i];
        const numerada = p.n !== undefined;
        const lado = numerada ? PARADA : PONTO;
        return (
          <React.Fragment key={i}>
            <div
              style={{
                position: "absolute",
                left: xLinha - lado / 2,
                top: y + centroH3 - lado / 2,
                width: lado,
                height: lado,
                borderRadius: "50%",
                background: COR.grafite,
                boxShadow: numerada ? SOMBRA.papel : undefined,
                display: "grid",
                placeItems: "center",
                color: COR.amarelo,
                fontFamily: FONTE.dados,
                fontWeight: TIPO.data.fontWeight,
                fontSize: TIPO.label.fontSize,
                lineHeight: 1,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {numerada ? p.n : null}
            </div>
            <div style={{ position: "absolute", left: xTexto, top: y, width: CONTADOR_X - xTexto, color: numerada ? COR.grafite : COR.asfalto }}>
              <div
                style={{
                  fontFamily: FONTE.mono,
                  fontWeight: TIPO.micro.fontWeight,
                  fontSize: TIPO.micro.fontSize,
                  lineHeight: TIPO.micro.lineHeight,
                  letterSpacing: TIPO.micro.letterSpacing,
                  color: COR.asfalto,
                }}
              >
                {p.hora}
              </div>
              <div
                style={{
                  marginTop: 8,
                  fontFamily: FONTE.display,
                  fontWeight: TIPO.h3.fontWeight,
                  fontSize: TIPO.h3.fontSize,
                  lineHeight: TIPO.h3.lineHeight,
                  letterSpacing: TIPO.h3.letterSpacing,
                  textTransform: "uppercase",
                  whiteSpace: "nowrap",
                }}
              >
                {p.lugar}
              </div>
              <div
                style={{
                  marginTop: 8,
                  fontFamily: FONTE.texto,
                  fontWeight: TIPO.body.fontWeight,
                  fontSize: TIPO.body.fontSize,
                  lineHeight: TIPO.body.lineHeight,
                  color: COR.asfalto,
                }}
              >
                {p.nota}
              </div>
            </div>
          </React.Fragment>
        );
      })}
    </Papel>
  );
};

const SlideFoto: React.FC<{ s: Extract<Slide, { tipo: "foto" }> }> = ({ s }) => {
  const lado = CAR.largura - 2 * CAR.margem;
  return (
    <Papel>
      <div
        style={{
          position: "absolute",
          left: CAR.margem,
          top: 176,
          width: lado,
          height: lado,
          borderRadius: RAIO.foto,
          overflow: "hidden",
          boxShadow: SOMBRA.papel,
        }}
      >
        <Img src={staticFile(s.foto)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </div>
      <div
        style={{
          position: "absolute",
          left: CAR.margem,
          top: 176 + lado + 32,
          width: lado,
          fontFamily: FONTE.texto,
          fontWeight: TIPO.body.fontWeight,
          fontSize: TIPO.body.fontSize,
          lineHeight: TIPO.body.lineHeight,
          color: COR.grafite,
        }}
      >
        {s.legenda}
      </div>
      <LinhaRota pontos={[[0, ROTA_Y], [CAR.largura, ROTA_Y]]} />
    </Papel>
  );
};

const SlideDica: React.FC<{ s: Extract<Slide, { tipo: "dica" }> }> = ({ s }) => (
  <Papel>
    {s.pictograma === "a-pe" && <PictogramaAPe x={CAR.margem} y={500} />}
    <Bilhete texto={s.texto} x={CAR.margem} y={660} entrada={-10000} tamanho={TIPO.pen.fontSize} />
    <LinhaRota pontos={[[0, ROTA_Y], [CAR.largura, ROTA_Y]]} />
  </Papel>
);

const SlideEncerramento: React.FC<{ s: Extract<Slide, { tipo: "encerramento" }> }> = ({ s }) => (
  <Papel>
    <Bilhete texto={s.bilhete} marca={s.marca} x={CAR.margem} y={400} entrada={-10000} tamanho={TIPO.pen.fontSize} />
    <Placa destino={s.cta} tamanho="M" x={CAR.margem} y={760} entrada={null} carrossel />
    <LinhaRota pontos={[[0, ROTA_Y], [CAR.largura - CAR.margem - SIMBOLO, ROTA_Y]]} />
    <div style={{ position: "absolute", left: CAR.largura - CAR.margem - SIMBOLO, top: ROTA_Y - SIMBOLO }}>
      <Simbolo1 altura={SIMBOLO} t={Infinity} />
    </div>
  </Papel>
);

export const Carrossel: React.FC<PropsCarrossel> = ({ serie, slides, indice }) => {
  const s = slides[indice];
  const sobreFoto = s.tipo === "capa";
  return (
    <AbsoluteFill style={{ background: COR.papel }}>
      {s.tipo === "capa" && <SlideCapa s={s} />}
      {s.tipo === "roteiro" && <SlideRoteiro s={s} />}
      {s.tipo === "foto" && <SlideFoto s={s} />}
      {s.tipo === "dica" && <SlideDica s={s} />}
      {s.tipo === "encerramento" && <SlideEncerramento s={s} />}
      <EtiquetaSerie texto={serie} />
      <Contador i={indice} total={slides.length} sobreFoto={sobreFoto} />
    </AbsoluteFill>
  );
};
