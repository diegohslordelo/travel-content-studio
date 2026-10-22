/**
 * Componentes editoriais reutilizáveis do Reel "Greves na Europa": textos de impacto, etiquetas de situação e
 * abrangência, rótulo de acervo e funil. Agenda, colagem de manchetes e telas ficam em Telas.tsx.
 * Todos recebem tempos em segundos absolutos da composição.
 */
import React from "react";
import { EASE } from "../ds/tokens";
import { ED, FONTE_ED, SEG, SOMBRA_IMPACTO, prog, useSeg } from "./tema";

/* ---------------------------------------------------------------- texto de impacto */

/**
 * Linhas grandes que entram de baixo com máscara, uma depois da outra (90 ms). `enfase` pinta as linhas indicadas
 * na cor de destaque a partir de `enfaseEm`, com um sublinhado que cresce da esquerda para a direita.
 */
export const TextoImpacto: React.FC<{
  linhas: string[];
  ini: number;
  fim: number;
  y?: number;
  tamanho?: number;
  cor?: string;
  enfase?: number[];
  enfaseEm?: number;
  corEnfase?: string;
  palavraCor?: { linha: number; palavra: string; cor: string };
}> = ({ linhas, ini, fim, y = 300, tamanho = 132, cor = ED.branco, enfase = [], enfaseEm, corEnfase = ED.alerta, palavraCor }) => {
  const t = useSeg();
  if (t < ini - 0.01 || t > fim + 0.3) return null;
  const saida = prog(t, fim, fim + 0.22, EASE.exit);
  const e = enfaseEm !== undefined ? prog(t, enfaseEm, enfaseEm + 0.18, EASE.out) : 0;
  return (
    <div style={{ position: "absolute", left: SEG.x0, top: y, width: SEG.x1 - SEG.x0, opacity: 1 - saida, translate: `0 ${-saida * 30}px` }}>
      {linhas.map((l, i) => {
        const p = prog(t, ini + i * 0.09, ini + i * 0.09 + 0.34, EASE.out);
        const realce = enfase.includes(i) ? e : 0;
        return (
          <div key={i} style={{ overflow: "hidden", lineHeight: 0.92, paddingBottom: 6 }}>
            <div
              style={{
                fontFamily: FONTE_ED.impacto,
                fontWeight: 800,
                fontSize: tamanho,
                letterSpacing: "-0.01em",
                color: realce > 0.5 ? corEnfase : cor,
                textShadow: SOMBRA_IMPACTO,
                translate: `0 ${(1 - p) * 110}%`,
                position: "relative",
                display: "inline-block",
                scale: String(1 + 0.04 * Math.sin(Math.PI * realce)),
                transformOrigin: "left center",
              }}
            >
              {palavraCor && palavraCor.linha === i
                ? l.split(" ").map((w, k) => (
                    <React.Fragment key={k}>
                      {k > 0 && " "}
                      <span style={{ color: w === palavraCor.palavra ? palavraCor.cor : undefined }}>{w}</span>
                    </React.Fragment>
                  ))
                : l}
              {enfase.includes(i) && (
                <div style={{ position: "absolute", left: 0, bottom: -2, height: 12, width: `${realce * 100}%`, background: corEnfase, borderRadius: 3, boxShadow: "0 4px 18px rgba(0,0,0,.45)" }} />
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------------------------- etiqueta de situação / abrangência */

export type Tom = "alerta" | "duvida" | "calma" | "neutro";
const COR_TOM: Record<Tom, string> = { alerta: ED.alerta, duvida: ED.duvida, calma: ED.calma, neutro: ED.cinza };

export const EtiquetaStatus: React.FC<{ texto: string; tom?: Tom; tamanho?: number }> = ({ texto, tom = "neutro", tamanho = 22 }) => (
  <span
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 10,
      fontFamily: FONTE_ED.mono,
      fontWeight: 500,
      fontSize: tamanho,
      letterSpacing: "0.06em",
      color: COR_TOM[tom],
      border: `2px solid ${COR_TOM[tom]}`,
      borderRadius: 999,
      padding: `${tamanho * 0.25}px ${tamanho * 0.7}px`,
      background: "rgba(10,13,20,0.55)",
      whiteSpace: "nowrap",
    }}
  >
    <span style={{ width: tamanho * 0.42, height: tamanho * 0.42, borderRadius: 99, background: COR_TOM[tom] }} />
    {texto}
  </span>
);

/* ---------------------------------------------------------------- rótulo de acervo */

/** Identifica imagem do acervo próprio (lugar e data reais da gravação), para não parecer registro da greve. */
export const RotuloAcervo: React.FC<{ texto: string; ini: number; fim: number }> = ({ texto, ini, fim }) => {
  const t = useSeg();
  if (t < ini || t > fim) return null;
  const o = Math.min(prog(t, ini, ini + 0.2), 1 - prog(t, fim - 0.25, fim));
  return (
    <div
      style={{
        position: "absolute",
        left: SEG.x0,
        top: 266,
        fontFamily: FONTE_ED.mono,
        fontSize: 22,
        letterSpacing: "0.08em",
        color: "rgba(243,245,248,.88)",
        background: "rgba(10,13,20,.5)",
        padding: "6px 12px",
        borderRadius: 6,
        opacity: o,
      }}
    >
      {texto}
    </div>
  );
};

/* ---------------------------------------------------------------- funil "o impacto depende" */

export const Funil: React.FC<{ ini: number; fim: number; titulo: string; itens: { texto: string; em: number }[] }> = ({ ini, fim, titulo, itens }) => {
  const t = useSeg();
  if (t < ini || t > fim + 0.3) return null;
  const s = prog(t, fim, fim + 0.25, EASE.exit);
  const pt = prog(t, ini, ini + 0.3, EASE.out);
  const larguras = [820, 720, 620, 520];
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 330, opacity: 1 - s }}>
      <div style={{ textAlign: "center", fontFamily: FONTE_ED.impacto, fontWeight: 700, fontSize: 52, color: ED.branco, textShadow: SOMBRA_IMPACTO, letterSpacing: "0.02em", opacity: pt, translate: `0 ${(1 - pt) * 20}px` }}>{titulo}</div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14, marginTop: 24 }}>
        {itens.map((it, i) => {
          const p = prog(t, it.em - 0.05, it.em + 0.25, EASE.arrive);
          const ultimo = i === itens.length - 1;
          return (
            <div
              key={it.texto}
              style={{
                width: larguras[i],
                height: 92,
                borderRadius: 14,
                display: "grid",
                placeItems: "center",
                fontFamily: FONTE_ED.impacto,
                fontWeight: 800,
                fontSize: 60,
                letterSpacing: "0.01em",
                color: ultimo ? ED.tinta : ED.branco,
                background: ultimo ? ED.calma : "rgba(10,13,20,.72)",
                border: `3px solid ${ED.calma}`,
                boxShadow: "0 20px 40px -14px rgba(0,0,0,.7)",
                opacity: p,
                scale: String(0.9 + 0.1 * p),
              }}
            >
              {it.texto}
            </div>
          );
        })}
      </div>
    </div>
  );
};
