/**
 * Animações explicativas do Reel "Casa de Anne Frank": as 8 pessoas escondidas, a linha do tempo
 * do esconderijo e a data da prisão. Paleta e fontes próprias do Reel (estilo.ts), fora do DS.
 */
import React from "react";
import { PALETA, TEXTO, TITULO, easeInOut, lerp } from "./estilo";

const NOMES = [
  ["OTTO", "EDITH", "MARGOT", "ANNE"],
  ["HERMANN", "AUGUSTE", "PETER", "FRITZ"],
];
const XS = [240, 440, 640, 840];

const Figura: React.FC<{ x: number; y: number; cor: string; anel?: number; opacidade: number; escala: number }> = ({ x, y, cor, anel = 0, opacidade, escala }) => (
  <g transform={`translate(${x} ${y}) scale(${escala})`} opacity={opacidade}>
    {anel > 0 && <circle cx={0} cy={-8} r={84} fill="none" stroke={PALETA.ambar} strokeWidth={5} opacity={anel} />}
    <circle cx={0} cy={-44} r={30} fill={cor} />
    <path d="M -58 52 Q -58 -6 0 -6 Q 58 -6 58 52 Z" fill={cor} />
  </g>
);

export type EstadoPessoas = "apresenta" | "presas" | "unico";

export const Pessoas: React.FC<{ t: number; altura: number; estado: EstadoPessoas; marcos: Record<string, number> }> = ({ t, altura, estado, marcos }) => {
  const cheia = altura > 1000;
  const ys = cheia ? [700, 1060] : [300, 640];
  const rotY = cheia ? [520, 880] : [130, 470];
  const nomeDy = cheia ? 130 : 96;

  const figuras = NOMES.flatMap((linha, r) =>
    linha.map((nome, k) => {
      let entra = 1;
      let cor: string = PALETA.papel;
      let opac = 1;
      let anel = 0;
      if (estado === "apresenta") {
        const ini = (r === 0 ? marcos.familia : marcos.outras) - 0.12 + k * 0.06;
        entra = lerp(t, ini, ini + 0.3, 0, 1);
      } else if (estado === "presas") {
        const p = lerp(t, marcos.presas - 0.05, marcos.presas + 0.6, 0, 1, easeInOut);
        opac = 1 - 0.62 * p;
        cor = p > 0.5 ? PALETA.cinza : PALETA.papel;
      } else {
        const p = r === 0 && k === 0 ? lerp(t, marcos.unico - 0.15, marcos.unico + 0.3, 0, 1) : 0;
        opac = r === 0 && k === 0 ? 0.38 + 0.62 * p : 0.32;
        cor = r === 0 && k === 0 && p > 0.3 ? PALETA.branco : PALETA.cinza;
        anel = r === 0 && k === 0 ? p : 0;
      }
      return { nome, x: XS[k], y: ys[r], entra, cor, opac, anel, destaque: estado === "unico" && r === 0 && k === 0 && anel > 0.3 };
    }),
  );

  const rotulo = (texto: string, y: number, ini: number, cor: string = PALETA.papel) => (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
        textAlign: "center",
        font: `700 30px ${TEXTO}`,
        letterSpacing: 5,
        color: cor,
        opacity: lerp(t, ini, ini + 0.3, 0, 1),
      }}
    >
      {texto}
    </div>
  );

  return (
    <div style={{ position: "absolute", inset: 0, height: altura, background: PALETA.fundo, overflow: "hidden" }}>
      <svg viewBox={`0 0 1080 ${altura}`} width={1080} height={altura} style={{ position: "absolute", inset: 0 }}>
        {figuras.map((f) => (
          <Figura key={f.nome} x={f.x} y={f.y} cor={f.cor} anel={f.anel} opacidade={f.entra * f.opac} escala={0.85 + 0.15 * f.entra} />
        ))}
      </svg>
      {figuras.map((f) => (
        <div
          key={f.nome}
          style={{
            position: "absolute",
            left: f.x - 100,
            width: 200,
            top: f.y + nomeDy - 40,
            textAlign: "center",
            font: `${f.destaque ? 800 : 600} 24px ${TEXTO}`,
            letterSpacing: 2,
            color: f.destaque ? PALETA.ambar : PALETA.papel,
            opacity: f.entra * (f.destaque ? 1 : f.opac),
          }}
        >
          {f.nome}
        </div>
      ))}
      {estado === "apresenta" && rotulo("FAMÍLIA FRANK", rotY[0], marcos.familia - 0.1)}
      {estado === "apresenta" && rotulo("+ 4 PESSOAS", rotY[1], marcos.outras - 0.1)}
      {estado === "presas" && rotulo("8 PESSOAS ESCONDIDAS", rotY[0] - 40, -1)}
      {estado === "unico" && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 330,
            textAlign: "center",
            font: `400 170px ${TITULO}`,
            color: PALETA.branco,
            opacity: lerp(t, marcos.unico, marcos.unico + 0.3, 0, 1),
            translate: `0 ${lerp(t, marcos.unico, marcos.unico + 0.3, 20, 0)}px`,
          }}
        >
          1 DE 8
        </div>
      )}
    </div>
  );
};

/** "≈ 2 anos": de 6 de julho de 1942 (entrada no anexo) a 4 de agosto de 1944 (prisão). */
export const LinhaTempo: React.FC<{ t: number; altura: number }> = ({ t, altura }) => {
  const p = lerp(t, 0.15, 1.5, 0, 1, easeInOut);
  const x0 = 120;
  const x1 = 960;
  return (
    <div style={{ position: "absolute", inset: 0, height: altura, background: PALETA.fundo }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center", font: `400 230px ${TITULO}`, color: PALETA.branco, lineHeight: 1 }}>
        2 ANOS
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 410, textAlign: "center", font: `700 30px ${TEXTO}`, letterSpacing: 5, color: PALETA.papel }}>
        ESCONDIDOS NO ANEXO
      </div>
      <div style={{ position: "absolute", left: x0, width: x1 - x0, top: 560, height: 10, background: "#3A352D", borderRadius: 5 }} />
      <div style={{ position: "absolute", left: x0, width: (x1 - x0) * p, top: 560, height: 10, background: PALETA.ambar, borderRadius: 5 }} />
      {[
        { x: x0, txt: "JUL 1942", a: 0 },
        { x: x1, txt: "AGO 1944", a: 1 },
      ].map((m) => (
        <React.Fragment key={m.txt}>
          <div
            style={{
              position: "absolute",
              left: m.x - 13,
              top: 552,
              width: 26,
              height: 26,
              borderRadius: 13,
              background: p >= m.a ? PALETA.ambar : "#3A352D",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: m.x - 150,
              width: 300,
              top: 610,
              textAlign: "center",
              font: `700 34px ${TEXTO}`,
              letterSpacing: 2,
              color: PALETA.papel,
              opacity: m.a === 0 ? 1 : lerp(t, 1.2, 1.5, 0.35, 1),
            }}
          >
            {m.txt}
          </div>
        </React.Fragment>
      ))}
    </div>
  );
};

/** Data em tela cheia, linha a linha subindo de trás de uma máscara. */
export const Data: React.FC<{ t: number; linhas: string[] }> = ({ t, linhas }) => (
  <div style={{ position: "absolute", inset: 0, background: PALETA.preto }}>
    <div style={{ position: "absolute", left: 72, top: 560 }}>
      {linhas.map((l, i) => {
        const p = lerp(t, 0.05 + i * 0.18, 0.55 + i * 0.18, 0, 1);
        return (
          <div key={l} style={{ overflow: "hidden", height: 250 }}>
            <div style={{ font: `400 250px ${TITULO}`, lineHeight: 1, color: PALETA.branco, translate: `0 ${(1 - p) * 250}px` }}>{l}</div>
          </div>
        );
      })}
    </div>
  </div>
);
