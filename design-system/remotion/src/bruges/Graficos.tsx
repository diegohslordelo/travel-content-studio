/**
 * Animações do Reel de Bruges, na linguagem do formato (fundo #14120F, traço papel, destaque âmbar).
 * Nenhuma se passa por foto: mapas e corte das capelas são desenho (traço), e só escrevem o que a fala diz.
 */
import React from "react";
import { evolvePath } from "@remotion/paths";
import { Img, staticFile } from "remotion";
import { PALETA, SOMBRA_TEXTO, TEXTO, TITULO, clamp, ease, easeInOut, lerp } from "./estilo";

export type Pais = { nome: string; d: string; destaque: boolean };
export type Mapa = { w: number; h: number; paises: Pais[]; bruges: [number, number]; jerusalem?: [number, number] };

/** Linha que sobe de trás de uma máscara (com folga de 50 px para acentos). */
const Linha: React.FC<{ t: number; em: number; children: React.ReactNode; style: React.CSSProperties }> = ({ t, em, children, style }) => {
  const e = ease((t - em) / 0.22);
  return (
    <div style={{ overflow: "hidden", paddingTop: 50, marginTop: -50 }}>
      <div style={{ ...style, translate: `0 ${(1 - e) * 110}%`, opacity: e > 0 ? 1 : 0 }}>{children}</div>
    </div>
  );
};

const Pino: React.FC<{ x: number; y: number; t: number; em: number }> = ({ x, y, t, em }) => {
  const e = ease((t - em) / 0.25);
  const onda = clamp((t - em) / 0.9);
  return (
    <g opacity={e > 0 ? 1 : 0}>
      <circle cx={x} cy={y} r={14 + 46 * onda} fill="none" stroke={PALETA.ambar} strokeWidth={3} opacity={1 - onda} />
      <circle cx={x} cy={y} r={13 * (0.6 + 0.4 * e)} fill={PALETA.ambar} stroke={PALETA.preto} strokeWidth={3} />
    </g>
  );
};

/** "em Bruges, na Bélgica": mapa da região (Natural Earth), Bélgica em âmbar, pino em Bruges. */
export const MapaBelgica: React.FC<{ t: number; mapa: Mapa; altura: number; marcos: Record<string, number> }> = ({ t, mapa, altura, marcos }) => {
  const z = lerp(t, 0, 1.2, 1.0, 1.12, (x) => x);
  const [bx, by] = mapa.bruges;
  const eb = ease((t - marcos.belgica) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, height: altura, background: PALETA.mar, overflow: "hidden" }}>
      <svg width={mapa.w} height={mapa.h} style={{ position: "absolute", left: 0, top: (altura - mapa.h) / 2, scale: String(z), transformOrigin: `${bx}px ${by}px` }}>
        {mapa.paises.map((p) => (
          <path
            key={p.nome}
            d={p.d}
            fill={p.destaque ? PALETA.ambar : PALETA.terra}
            fillOpacity={p.destaque ? 0.22 + 0.13 * eb : 1}
            stroke={p.destaque ? PALETA.ambar : PALETA.papel}
            strokeOpacity={p.destaque ? 0.95 : 0.28}
            strokeWidth={p.destaque ? 3 : 1.5}
            strokeLinejoin="round"
          />
        ))}
        <Pino x={bx} y={by} t={t} em={marcos.bruges - 0.05} />
        {/* rótulos: só o que a fala diz */}
        <text x={bx + 30} y={by - 28} style={{ font: `400 74px ${TITULO}` }} fill={PALETA.branco} stroke={PALETA.preto} strokeWidth={2} paintOrder="stroke" opacity={ease((t - marcos.bruges) / 0.2)}>
          BRUGES
        </text>
      </svg>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 770, // abaixo da Bélgica, longe do rótulo BRUGES e acima da legenda na costura
          textAlign: "center",
          font: `700 40px ${TEXTO}`,
          letterSpacing: "0.32em",
          color: PALETA.ambar,
          textShadow: SOMBRA_TEXTO,
          opacity: eb,
          translate: `0 ${(1 - eb) * 16}px`,
        }}
      >
        BÉLGICA
      </div>
    </div>
  );
};

/** "teria chegado a Bruges depois das cruzadas": a rota da Terra Santa até Bruges se desenha. */
export const Rota: React.FC<{ t: number; mapa: Mapa; marcos: Record<string, number> }> = ({ t, mapa, marcos }) => {
  const [bx, by] = mapa.bruges;
  const [jx, jy] = mapa.jerusalem ?? [0, 0];
  const top = 0;
  const caminho = `M ${jx} ${jy} Q ${(jx + bx) / 2 - 120} ${(jy + by) / 2 - 40} ${bx} ${by}`;
  const p = easeInOut((t - 0.05) / Math.max(0.3, marcos.bruges - 0.05));
  const ev = evolvePath(p, caminho);
  const z = lerp(t, 0, 1.2, 1.0, 1.06, (x) => x);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.mar, overflow: "hidden" }}>
      <svg width={mapa.w} height={mapa.h} style={{ position: "absolute", left: 0, top, scale: String(z), transformOrigin: `${(jx + bx) / 2}px ${(jy + by) / 2}px` }}>
        {mapa.paises.map((pp) => (
          <path key={pp.nome} d={pp.d} fill={PALETA.terra} stroke={PALETA.papel} strokeOpacity={0.25} strokeWidth={1.2} strokeLinejoin="round" />
        ))}
        <path d={caminho} fill="none" stroke={PALETA.ambar} strokeWidth={7} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
        <circle cx={jx} cy={jy} r={11} fill={PALETA.papel} stroke={PALETA.preto} strokeWidth={3} />
        <Pino x={bx} y={by} t={t} em={marcos.bruges - 0.05} />
        <text x={bx + 30} y={by - 26} style={{ font: `400 70px ${TITULO}` }} fill={PALETA.branco} opacity={ease((t - marcos.bruges) / 0.2)}>
          BRUGES
        </text>
      </svg>
    </div>
  );
};

/** "Lá tem duas capelas, uma mais simples… e outra gótica": corte desenhado da basílica, dois andares que se enchem de foto. */
export const Capelas: React.FC<{ t: number; baixo: string; cima: string; marcos: Record<string, number> }> = ({ t, baixo, cima, marcos }) => {
  const L = 150;
  const R = 930;
  const piso = 900; // piso entre as capelas
  const chao = 1230;
  const beiral = 560;
  const contorno = `M ${L} ${chao} L ${L} ${beiral} L 540 300 L ${R} ${beiral} L ${R} ${chao} Z`;
  const evC = evolvePath(easeInOut((t - 0.0) / 0.55), contorno);
  const evP = evolvePath(easeInOut((t - 0.25) / 0.4), `M ${L} ${piso} L ${R} ${piso}`);
  const foto = (src: string, em: number, y0: number, y1: number, clip: string, foco: string) => {
    const e = ease((t - em) / 0.3);
    const z = lerp(t, em, em + 3, 1.08, 1.0, (x) => x);
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, clipPath: clip, opacity: e }}>
        <Img
          src={staticFile(src)}
          style={{ position: "absolute", left: L, top: y0, width: R - L, height: y1 - y0, objectFit: "cover", objectPosition: foco, scale: String(z), filter: "contrast(1.05)" }}
        />
      </div>
    );
  };
  const brilho = (em: number) => 1 - clamp((t - em) / 0.6);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo, overflow: "hidden" }}>
      {/* andar de cima: gótico (polígono com o telhado) · andar de baixo: retângulo */}
      {foto(cima, marcos.cima - 0.05, 300, piso, `polygon(${L}px ${piso}px, ${L}px ${beiral}px, 540px 300px, ${R}px ${beiral}px, ${R}px ${piso}px)`, "50% 45%")}
      {foto(baixo, marcos.baixo - 0.05, piso, chao, `polygon(${L}px ${chao}px, ${L}px ${piso}px, ${R}px ${piso}px, ${R}px ${chao}px)`, "50% 55%")}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <path d={contorno} fill="none" stroke={PALETA.papel} strokeWidth={6} strokeLinejoin="round" strokeDasharray={evC.strokeDasharray} strokeDashoffset={evC.strokeDashoffset} />
        <path d={`M ${L} ${piso} L ${R} ${piso}`} stroke={PALETA.ambar} strokeWidth={6} strokeDasharray={evP.strokeDasharray} strokeDashoffset={evP.strokeDashoffset} />
        {/* realce de cada andar quando é citado */}
        <rect x={L} y={piso} width={R - L} height={chao - piso} fill="none" stroke={PALETA.ambar} strokeWidth={10} opacity={t > marcos.baixo - 0.05 ? brilho(marcos.baixo - 0.05) : 0} />
        <path
          d={`M ${L} ${piso} L ${L} ${beiral} L 540 300 L ${R} ${beiral} L ${R} ${piso} Z`}
          fill="none"
          stroke={PALETA.ambar}
          strokeWidth={10}
          strokeLinejoin="round"
          opacity={t > marcos.cima - 0.05 ? brilho(marcos.cima - 0.05) : 0}
        />
        {/* cruz no topo: o prédio é uma igreja */}
        <path d="M 540 300 L 540 214 M 510 244 L 570 244" stroke={PALETA.papel} strokeWidth={6} strokeLinecap="round" opacity={ease((t - 0.45) / 0.2)} />
      </svg>
    </div>
  );
};

/** "Desde a Idade Média": linhas grandes que sobem, no instante em que são ditas. */
export const DataIdade: React.FC<{ t: number; marcos: Record<string, number> }> = ({ t, marcos }) => {
  const e = ease(t / 0.5);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
      <div style={{ width: 760 * e, height: 4, background: PALETA.ambar, marginBottom: 46, opacity: 0.85 }} />
      <Linha t={t} em={marcos.l0 - 0.06} style={{ font: `400 120px ${TITULO}`, color: PALETA.papel, lineHeight: 1.05, textAlign: "center" }}>
        DESDE A
      </Linha>
      <Linha t={t} em={marcos.l1 - 0.06} style={{ font: `400 250px ${TITULO}`, color: PALETA.ambar, lineHeight: 1.0, textAlign: "center" }}>
        IDADE
      </Linha>
      <Linha t={t} em={marcos.l1 + 0.12} style={{ font: `400 250px ${TITULO}`, color: PALETA.ambar, lineHeight: 1.0, textAlign: "center" }}>
        MÉDIA
      </Linha>
      <div style={{ width: 760 * e, height: 4, background: PALETA.ambar, marginTop: 40, opacity: 0.85 }} />
    </div>
  );
};

/** "reconhecida pela UNESCO como um patrimônio cultural imaterial da humanidade". */
export const Patrimonio: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const z = lerp(t, 0, 3, 1.08, 1.0, (x) => x);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo, overflow: "hidden" }}>
      {fundo && (
        <Img
          src={staticFile(fundo)}
          style={{ position: "absolute", inset: 0, width: 1080, height: 1920, objectFit: "cover", scale: String(z), filter: "grayscale(1) brightness(0.28) blur(6px)" }}
        />
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: 520, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ font: `700 44px ${TEXTO}`, letterSpacing: "0.42em", color: PALETA.ambar, marginBottom: 34, opacity: ease(t / 0.25), paddingLeft: "0.42em" }}>UNESCO</div>
        <Linha t={t} em={marcos.l1 - 0.06} style={{ font: `400 156px ${TITULO}`, color: PALETA.branco, lineHeight: 1.04, textAlign: "center" }}>
          PATRIMÔNIO
        </Linha>
        <Linha t={t} em={marcos.l2 - 0.06} style={{ font: `400 156px ${TITULO}`, color: PALETA.branco, lineHeight: 1.04, textAlign: "center" }}>
          CULTURAL
        </Linha>
        <Linha t={t} em={marcos.l3 - 0.06} style={{ font: `400 156px ${TITULO}`, color: PALETA.ambar, lineHeight: 1.04, textAlign: "center" }}>
          IMATERIAL
        </Linha>
        <Linha t={t} em={marcos.l4 - 0.06} style={{ font: `400 96px ${TITULO}`, color: PALETA.branco, lineHeight: 1.1, textAlign: "center" }}>
          DA HUMANIDADE
        </Linha>
      </div>
    </div>
  );
};

/** "sua origem não é comprovada": círculo desenhado à mão e ponto de interrogação sobre o relicário. */
export const Interrogacao: React.FC<{ t: number; em: number; cx: number; cy: number }> = ({ t, em, cx, cy }) => {
  const rx = 300;
  const ry = 330;
  // círculo "à mão": elipse que passa um pouco do ponto de partida
  const d = `M ${cx - rx * 0.2} ${cy - ry} C ${cx + rx * 0.9} ${cy - ry * 1.05}, ${cx + rx * 1.05} ${cy + ry * 0.9}, ${cx} ${cy + ry} C ${cx - rx * 1.1} ${cy + ry * 1.0}, ${cx - rx * 1.05} ${cy - ry * 0.85}, ${cx + rx * 0.25} ${cy - ry * 1.04}`;
  const ev = evolvePath(easeInOut((t - em + 0.1) / 0.45), d);
  const e = ease((t - em - 0.25) / 0.25);
  return (
    <>
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <path d={d} fill="none" stroke={PALETA.ambar} strokeWidth={9} strokeLinecap="round" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} opacity={t > em - 0.1 ? 1 : 0} />
      </svg>
      <div
        style={{
          position: "absolute",
          left: cx + rx * 0.92,
          top: cy - ry * 0.55,
          font: `400 230px ${TITULO}`,
          color: PALETA.ambar,
          textShadow: "0 6px 30px rgba(0,0,0,0.7)",
          opacity: e,
          scale: String(0.7 + 0.3 * e),
          rotate: "8deg",
        }}
      >
        ?
      </div>
    </>
  );
};
