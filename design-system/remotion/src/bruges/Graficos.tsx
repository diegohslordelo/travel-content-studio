/**
 * Grafismos do Reel de Bruges na linguagem do formato (Anton, Inter, âmbar). Cada número e cada texto
 * vêm da fala do Diego (FORMATOS_REELS 6: nada na tela que não esteja na fala), exceto o selo "CAPTURA REAL",
 * que marca a prova (REFERENCIA_EDICAO_FORMATOS 6).
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { GRADE_FOTO, PALETA, TEXTO, TITULO, clamp01, ease, easeBack, easeInOut, lerp } from "./estilo";

const sombraTexto = "0 4px 30px rgba(0,0,0,0.65), 0 2px 0 rgba(0,0,0,0.35)";

/** Contador "120 MIL HABITANTES" → "8 MILHÕES DE TURISTAS EM 1 ANO", sobre o vídeo escurecido. */
export const Contador: React.FC<{ t: number; m: Record<string, number> }> = ({ t, m }) => {
  const a = ease((t - m.cento) / 0.18);
  const conta120 = Math.round(120 * easeInOut((t - m.cento) / 0.6));
  const b = t >= m.milhoes ? easeBack((t - m.milhoes) / 0.26) : 0;
  const conta8 = Math.max(1, Math.round(8 * ease((t - m.milhoes) / 0.32)));
  const sobe = ease((t - m.milhoes) / 0.3); // o 120 MIL sobe e encolhe quando os 8 milhões batem
  const rot = (txt: string, ini: number, tam: number, cor: string = PALETA.papel) => (
    <div style={{ font: `800 ${tam}px ${TEXTO}`, letterSpacing: 3, color: cor, opacity: ease((t - ini) / 0.16), translate: `0 ${(1 - ease((t - ini) / 0.16)) * 14}px` }}>{txt}</div>
  );
  return (
    <>
      <div style={{ position: "absolute", inset: 0, background: `rgba(11,10,9,${0.5 * clamp01((t - m.cento + 0.2) / 0.3)})` }} />
      {t >= m.cento && (
        <div style={{ position: "absolute", left: 0, right: 0, top: lerp(sobe, 0, 1, 560, 330, (x) => x), textAlign: "center", opacity: a * (1 - 0.45 * sobe), scale: String(1 - 0.38 * sobe), textShadow: sombraTexto }}>
          <div style={{ font: `400 230px ${TITULO}`, lineHeight: 1, color: PALETA.branco }}>{conta120} MIL</div>
          {rot("HABITANTES", m.habitantes, 52)}
        </div>
      )}
      {t >= m.milhoes && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 640, textAlign: "center", scale: String(0.6 + 0.4 * b), opacity: clamp01(b * 2), textShadow: sombraTexto }}>
          <div style={{ font: `400 300px ${TITULO}`, lineHeight: 1, color: PALETA.ambar }}>{conta8} MILHÕES</div>
          {rot("DE TURISTAS", m.turistas, 58, PALETA.branco)}
          {rot("EM 1 ANO", m.ano, 58, PALETA.branco)}
        </div>
      )}
    </>
  );
};

/** Relógio: os ponteiros giram até 11h e o "11H" entra na palavra (Cheguei lá às 11 horas). */
export const Relogio: React.FC<{ t: number; em: number }> = ({ t, em }) => {
  const e = ease((t - em + 0.25) / 0.3);
  const giro = easeInOut((t - em + 0.25) / 0.45);
  const horas = lerp(giro, 0, 1, 8, 11, (x) => x); // 8h → 11h: a manhã que passou
  const angH = (horas % 12) * 30;
  const angM = (horas * 60) % 60 * 6 + (1 - giro) * 360 * 3;
  const txt = ease((t - em) / 0.2);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 470, display: "flex", flexDirection: "column", alignItems: "center", opacity: e }}>
      <svg width={300} height={300} viewBox="-150 -150 300 300" style={{ filter: "drop-shadow(0 10px 30px rgba(0,0,0,0.6))" }}>
        <circle r={128} fill="rgba(11,10,9,0.72)" stroke={PALETA.papel} strokeWidth={10} />
        {Array.from({ length: 12 }).map((_, i) => (
          <line key={i} x1={0} y1={-104} x2={0} y2={i % 3 === 0 ? -86 : -94} stroke={PALETA.papel} strokeWidth={i % 3 === 0 ? 8 : 4} transform={`rotate(${i * 30})`} />
        ))}
        <line x1={0} y1={0} x2={0} y2={-62} stroke={PALETA.papel} strokeWidth={12} strokeLinecap="round" transform={`rotate(${angH})`} />
        <line x1={0} y1={0} x2={0} y2={-96} stroke={PALETA.ambar} strokeWidth={7} strokeLinecap="round" transform={`rotate(${angM})`} />
        <circle r={11} fill={PALETA.ambar} />
      </svg>
      <div style={{ font: `400 170px ${TITULO}`, lineHeight: 1, color: PALETA.branco, marginTop: 8, opacity: txt, scale: String(0.8 + 0.2 * easeBack(txt)), textShadow: sombraTexto }}>11H</div>
    </div>
  );
};

/** Captura real da matéria (Afar, 18/06/2019): título e depois o trecho destacado. */
export const Captura: React.FC<{ t: number; dur: number; fundo: string; titulo: string; trecho: string; troca: number }> = ({ t, dur, fundo, titulo, trecho, troca }) => {
  const e = ease(t / 0.3);
  const d = easeInOut((t - troca) / 0.35);
  const card = (src: string, alt: number, op: number, ty: number, kb: number) => (
    <div style={{ position: "absolute", left: 90, width: 900, top: 800 - alt / 2 + ty, height: alt, borderRadius: 26, overflow: "hidden", boxShadow: "0 40px 90px rgba(0,0,0,0.7)", opacity: op, background: "#fff" }}>
      <Img src={staticFile(src)} style={{ width: 900, height: alt, objectFit: "cover", objectPosition: "50% 0%", scale: String(kb), transformOrigin: "50% 40%" }} />
    </div>
  );
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", background: PALETA.preto }}>
      <Img src={staticFile(fundo)} style={{ position: "absolute", inset: -60, width: 1200, height: 2040, objectFit: "cover", filter: "blur(28px) brightness(0.42) saturate(0.6)" }} />
      {card(titulo, 920, e * (1 - d), (1 - e) * 80 - 40 * d, 1.0 + 0.03 * clamp01(t / troca))}
      {t > troca - 0.4 && card(trecho, 800, d, (1 - d) * 60, lerp(t, troca, dur, 1.0, 1.08, (x) => x))}
      <div style={{ position: "absolute", left: 90, top: 800 - 460 - 74, font: `800 30px ${TEXTO}`, letterSpacing: 4, color: PALETA.preto, background: PALETA.ambar, padding: "10px 20px", borderRadius: 10, opacity: e }}>CAPTURA REAL</div>
    </div>
  );
};

/** "Bruges era igual um domingo de sol no Porto da Barra": Bruges em cima, o Porto da Barra sobe por baixo, "=" na costura. */
export const Comparar: React.FC<{ t: number; dur: number; a: string; b: string; marco: number; focoA: [number, number]; focoB: [number, number] }> = ({ t, dur, a, b, marco, focoA, focoB }) => {
  const e = ease((t - marco) / 0.32);
  const igual = easeBack((t - marco - 0.12) / 0.3);
  const foto = (src: string, foco: [number, number], kb: number, filtro: string) => (
    <Img src={staticFile(src)} style={{ width: 1080, height: 960, objectFit: "cover", objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`, scale: String(kb), transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`, filter: filtro }} />
  );
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.preto, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: lerp(e, 0, 1, 480, 0, (x) => x), width: 1080, height: 960, overflow: "hidden" }}>{foto(a, focoA, lerp(t, 0, dur, 1.0, 1.06, (x) => x), "saturate(0.8) contrast(1.06)")}</div>
      <div style={{ position: "absolute", left: 0, top: 960 + (1 - e) * 960, width: 1080, height: 960, overflow: "hidden" }}>{foto(b, focoB, lerp(t, marco, dur, 1.0, 1.08, (x) => x), GRADE_FOTO)}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 957, height: 6, background: "rgba(0,0,0,0.55)", opacity: e }} />
      {t > marco && (
        <div style={{ position: "absolute", left: 540 - 70, top: 960 - 70, width: 140, height: 140, borderRadius: 70, background: PALETA.ambar, display: "flex", alignItems: "center", justifyContent: "center", scale: String(igual), boxShadow: "0 12px 40px rgba(0,0,0,0.5)" }}>
          <div style={{ font: `400 120px ${TITULO}`, lineHeight: 1, color: PALETA.preto, marginTop: -6 }}>=</div>
        </div>
      )}
    </div>
  );
};
