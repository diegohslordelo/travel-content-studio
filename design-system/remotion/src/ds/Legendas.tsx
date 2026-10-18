/**
 * Legendas e tipografia cinética (DS V2, 3.1 a 3.3). Estilos: Padrão (com Destaque), Emocional,
 * Narrativa e Informação. O Humor é o Bilhete (Bilhete.tsx, `semPapel` para caneta direto na cena).
 * Base comum: scrim sempre ligado no Reel (material.tsx) + sombra de texto; bloco centralizado no
 * centro do canvas (x 540, decisão do Diego, CLAUDE.md 6), base em y 1420.
 */
import React from "react";
import { kf, useMs } from "./tempo";
import { BLUR, COR, DUR, EASE, FONTE, RAIO, REEL, SOMBRA, TIPO, rgba } from "./tokens";

const SOMBRA_TEXTO = "0 2px 0 rgba(0,0,0,.35), 0 0 24px rgba(0,0,0,.45)"; // 3.1
const BASE_LEGENDA = REEL.altura - 1420; // base do bloco em y 1420 (3.1)
const LARGURA_CAIXA = 872; // largura da caixa da legenda na prévia (pd-bundle.css); ver pendência 13 do CLAUDE.md

/* ---------------- texto que gira (números do Placar, preço, Informação) ---------------- */

/** Cada algarismo rola verticalmente de 0 até o valor (Giro, 3.3: 240 ms). Marque destaque com "*palavra" ou "*palavra*". */
export const TextoGiro: React.FC<{ valor: string; t: number; dur?: number }> = ({ valor, t, dur = DUR.base }) => {
  const p = kf(t, [0, dur], [0, 1], EASE.out);
  return (
    <span style={{ fontVariantNumeric: "tabular-nums" }}>
      {valor.replace(/ /g, "\u00A0").split("").map((c, i) => {
        const digito = /[0-9]/.test(c) && c !== "0";
        return (
          <span key={i} style={{ display: "inline-block", position: "relative", overflow: "hidden", height: "1em", lineHeight: "1em", verticalAlign: "top" }}>
            <span style={{ visibility: "hidden" }}>{c}</span>
            {digito && p < 1 && <span style={{ position: "absolute", left: 0, top: 0, translate: `0 ${-p * 100}%` }}>0</span>}
            <span style={{ position: "absolute", left: 0, top: 0, translate: `0 ${digito ? (1 - p) * 100 : 0}%` }}>{c}</span>
          </span>
        );
      })}
    </span>
  );
};

/* ---------------- Padrão + Destaque ---------------- */

export type GrupoLegenda = {
  /** Palavras separadas por espaço; "|" quebra a linha; "*palavra" = Destaque (mini-placa). */
  texto: string;
  /** ms */
  ini: number;
  fim: number;
  /** ms de cada palavra (modo palavra a palavra) ou só da palavra destacada. */
  palavras?: number[];
};

const MiniPlaca: React.FC<{ children: React.ReactNode; escala: number }> = ({ children, escala }) => (
  <span
    style={{
      display: "inline-block",
      background: COR.amarelo,
      color: COR.grafite,
      textShadow: "none",
      padding: "4px 14px",
      borderRadius: RAIO.tag,
      boxShadow: `${SOMBRA.relevo}, 0 3px 0 rgba(0,0,0,.25), 0 10px 18px -6px rgba(0,0,0,.5)`,
      scale: String(escala),
    }}
  >
    {children}
  </span>
);

/**
 * Legenda Padrão: 1 grupo de fala por vez (2 a 6 palavras), máx. 2 linhas × 26 caracteres.
 * modo "palavra": cada palavra sobe 10 px em 160 ms quando é dita. modo "grupo" (fala > 3 palavras/s,
 * freio 4 da 3.3): o grupo inteiro entra em 120 ms. Saída do grupo: some e sobe 6 px em 120 ms.
 */
export const LegendaPadrao: React.FC<{ grupos: GrupoLegenda[]; modo?: "palavra" | "grupo"; base?: number }> = ({ grupos, modo = "grupo", base = BASE_LEGENDA }) => {
  const t = useMs();
  const g = grupos.find((x) => t >= x.ini && t < x.fim + 120);
  if (!g) return null;
  const saida = kf(t, [g.fim, g.fim + 120], [0, 1], EASE.out);
  const entradaGrupo = kf(t, [g.ini, g.ini + 120], [0, 1], EASE.out);
  // só o espaço comum separa palavras: o espaço sem quebra (U+00A0) mantém 2 palavras na mesma mini-placa
  const linhas = g.texto.split("|").map((l) => l.trim().split(/ +/));
  let idx = 0;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        width: LARGURA_CAIXA,
        marginInline: "auto",
        bottom: base,
        textAlign: "center",
        color: COR.legenda,
        fontFamily: FONTE.texto,
        fontWeight: TIPO.caption.fontWeight,
        fontSize: TIPO.caption.fontSize,
        lineHeight: TIPO.caption.lineHeight,
        textShadow: SOMBRA_TEXTO,
        opacity: (modo === "grupo" ? entradaGrupo : 1) * (1 - saida),
        translate: `0 ${(modo === "grupo" ? (1 - entradaGrupo) * 10 : 0) - saida * 6}px`,
      }}
    >
      {linhas.map((ws, li) => (
        <div key={li}>
          {ws.map((w, wi) => {
            const i = idx++;
            const destaque = w.includes("*");
            const palavra = w.replace(/\*/g, "");
            const tw = g.palavras?.[i] ?? g.ini;
            const e = modo === "palavra" ? kf(t, [tw, tw + DUR.fast], [0, 1], EASE.out) : 1;
            const pop = destaque ? kf(t, [tw, tw + 0.6 * DUR.base, tw + DUR.base], [0.85, 1.06, 1], [EASE.arrive, EASE.out]) : 1;
            return (
              <React.Fragment key={wi}>
                {wi > 0 && " "}
                <span style={{ display: "inline-block", opacity: e, translate: `0 ${(1 - e) * 10}px` }}>
                  {destaque ? <MiniPlaca escala={t < tw ? 0.85 : pop}>{palavra}</MiniPlaca> : palavra}
                </span>
              </React.Fragment>
            );
          })}
        </div>
      ))}
    </div>
  );
};

/* ---------------- Emocional ---------------- */

/**
 * Legenda Emocional (1 por Reel): Condensed 300 itálico 88 px + 1 palavra em 800, centro y 960,
 * scrim radial leve (35%). Tracking +12% → −1% e desfoque 6 → 0 em 500 ms (ease-cinema);
 * a palavra 800 entra 120 ms depois. Marque a palavra 800 com "*": "eu não esperava *isso*".
 */
export const LegendaEmocional: React.FC<{ texto: string; ini: number; fim: number }> = ({ texto, ini, fim }) => {
  const t = useMs();
  if (t < ini || t > fim + 120) return null;
  const a = kf(t - ini, [0, 500], [0, 1], EASE.cinema);
  const b = kf(t - ini, [120, 620], [0, 1], EASE.cinema);
  const saida = kf(t, [fim, fim + 120], [1, 0], EASE.out);
  const estilo = (p: number): React.CSSProperties => ({
    letterSpacing: `${0.12 + (-0.01 - 0.12) * p}em`,
    filter: p < 0.99 ? `blur(${6 * (1 - p)}px)` : undefined,
    opacity: p,
  });
  const linhas = texto.split("|");
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 960 - 360,
          height: 720,
          background: `radial-gradient(ellipse at 50% 50%, ${rgba(COR.grafite, 0.35)} 0%, ${rgba(COR.grafite, 0)} 65%)`,
          opacity: a * saida,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          width: LARGURA_CAIXA,
          marginInline: "auto",
          top: 960,
          translate: "0 -50%",
          textAlign: "center",
          color: COR.legenda,
          fontFamily: FONTE.display,
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: TIPO.editorial.fontSize,
          lineHeight: TIPO.editorial.lineHeight,
          textShadow: "0 2px 0 rgba(0,0,0,.25), 0 0 40px rgba(0,0,0,.5)",
          opacity: saida,
        }}
      >
        {linhas.map((l, i) => (
          <div key={i}>
            {l.split(/(\*[^*]+\*)/).map((p, k) =>
              p.startsWith("*") ? (
                <span key={k} style={{ display: "inline-block", fontStyle: "normal", fontWeight: 800, textTransform: "uppercase", ...estilo(b) }}>
                  {p.replace(/\*/g, "")}
                </span>
              ) : (
                <span key={k} style={{ display: "inline-block", whiteSpace: "pre", ...estilo(a) }}>
                  {p}
                </span>
              ),
            )}
          </div>
        ))}
      </div>
    </>
  );
};

/* ---------------- Narrativa (vidro) ---------------- */

/**
 * Legenda Narrativa: Barlow 500 44 px sobre vidro (grafite 55% + desfoque 24 px + filete 1 px claro),
 * alinhada à esquerda em x 72, base y 1420, máx. 3 linhas × 34 caracteres.
 * O vidro abre em 200 ms e as linhas entram uma a uma, a cada 120 ms.
 */
export const LegendaNarrativa: React.FC<{ linhas: string[]; ini: number; fim: number; rotulo?: string }> = ({ linhas, ini, fim, rotulo }) => {
  const t = useMs();
  if (t < ini || t > fim + 120) return null;
  const abre = kf(t - ini, [0, 200], [0.2, 1], EASE.out);
  const opacVidro = kf(t - ini, [0, 200], [0, 1], EASE.out);
  const saida = kf(t, [fim, fim + 120], [1, 0], EASE.out);
  return (
    <div
      style={{
        position: "absolute",
        left: REEL.seguroEsq,
        bottom: BASE_LEGENDA,
        maxWidth: LARGURA_CAIXA,
        padding: "26px 34px 28px",
        borderRadius: RAIO.tag,
        background: COR.vidro,
        backdropFilter: `blur(${BLUR.vidro}px)`,
        WebkitBackdropFilter: `blur(${BLUR.vidro}px)`,
        boxShadow: "inset 0 0 0 1px rgba(255,255,255,.14)",
        color: COR.legenda,
        fontFamily: FONTE.texto,
        fontWeight: TIPO.narrative.fontWeight,
        fontSize: TIPO.narrative.fontSize,
        lineHeight: TIPO.narrative.lineHeight,
        transformOrigin: "50% 100%",
        scale: `1 ${abre}`,
        opacity: opacVidro * saida,
      }}
    >
      {rotulo && (
        <div style={{ fontFamily: FONTE.mono, fontWeight: 500, fontSize: 24, letterSpacing: "0.08em", color: COR.concreto, marginBottom: 12, textTransform: "uppercase" }}>
          {rotulo}
        </div>
      )}
      {linhas.map((l, i) => {
        const e = kf(t - ini, [200 + i * 120, 200 + i * 120 + DUR.fast], [0, 1], EASE.out);
        return (
          <div key={i} style={{ opacity: e, translate: `0 ${(1 - e) * 8}px` }}>
            {l}
          </div>
        );
      })}
    </div>
  );
};

/* ---------------- Informação (etiqueta de papel) ---------------- */

/**
 * Legenda Informação (1 dado): etiqueta de papel tipo mini-recibo com picote no topo, rótulo Plex Mono
 * 30 px (asfalto) + número PD Placar 64 px (grafite), acima da legenda Padrão, em x 72.
 * Desliza da esquerda em 160 ms; o número gira até o valor em 240 ms. Sai pela direita em 240 ms.
 */
export const LegendaInformacao: React.FC<{ rotulo: string; numero: string; complemento?: string; ini: number; fim: number; y?: number }> = ({
  rotulo,
  numero,
  complemento,
  ini,
  fim,
  y = 1090,
}) => {
  const t = useMs();
  if (t < ini || t > fim + DUR.base) return null;
  const entra = kf(t - ini, [0, DUR.fast], [0, 1], EASE.out);
  const sai = kf(t - fim, [0, DUR.base], [0, 1], EASE.exit);
  return (
    <div
      style={{
        position: "absolute",
        left: REEL.seguroEsq,
        top: y,
        display: "inline-flex",
        flexDirection: "column",
        gap: 8,
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
      <div style={{ fontFamily: FONTE.mono, fontWeight: 500, fontSize: TIPO.micro.fontSize, lineHeight: 1, letterSpacing: "0.06em", color: COR.asfalto, textTransform: "uppercase", whiteSpace: "nowrap" }}>
        {rotulo}
      </div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
        <span style={{ fontFamily: FONTE.dados, fontWeight: 700, fontSize: 64, lineHeight: 1 }}>
          <TextoGiro valor={numero} t={t - ini} />
        </span>
        {complemento && <span style={{ fontFamily: FONTE.texto, fontWeight: 500, fontSize: 40, color: COR.asfalto }}>{complemento}</span>}
      </div>
    </div>
  );
};
