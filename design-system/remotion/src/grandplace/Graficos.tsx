/**
 * Grafismos do Reel da Grand-Place: títulos em Anton, mapa em cartão (Natural Earth, domínio público), ícone de envio,
 * cortina antes/depois e as transições do Reel (luz de passagem e clarão). Títulos, ícone de envio e transições vêm do
 * Reel da cratera de Darvaza sem mudança de valor. Linguagem do formato (docs/FORMATOS_REELS.md, 5.4), não do DS V2.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { PALETA, TEXTO, TITULO, ease, easeInOut, lerp } from "./estilo";

const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));

/* ------------------------------------------------------------------ títulos */

export type Linha = { texto: string; tam: number; em: number; cor?: string };

/** Linhas em Anton que sobem de trás de uma máscara (folga de 50 px acima para os acentos), centradas em x 540. */
export const Titulo: React.FC<{ t: number; linhas: Linha[]; centroY: number; sai?: number }> = ({ t, linhas, centroY, sai }) => {
  const total = linhas.reduce((s, l) => s + l.tam * 1.02, 0);
  let y = centroY - total / 2;
  const fora = sai !== undefined ? lerp(t, sai, sai + 0.18, 0, 1, easeInOut) : 0;
  return (
    <>
      {linhas.map((l, i) => {
        const e = ease(clamp((t - l.em) / 0.22));
        const topo = y;
        y += l.tam * 1.02;
        if (t < l.em) return null;
        return (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: topo - 50, height: l.tam * 1.02 + 50, overflow: "hidden", opacity: 1 - fora }}>
            <div
              style={{
                position: "absolute",
                left: 0,
                right: 0,
                top: 50 + (1 - e) * l.tam * 1.05,
                textAlign: "center",
                font: `400 ${l.tam}px ${TITULO}`,
                lineHeight: 1.02,
                color: l.cor ?? PALETA.branco,
                textShadow: "0 6px 40px rgba(0,0,0,0.55)",
                scale: String(1 + 0.04 * (1 - e)),
              }}
            >
              {l.texto}
            </div>
          </div>
        );
      })}
    </>
  );
};

/* ------------------------------------------------------------------ mapa em cartão */

export type DadosMapa = { paises: { nome: string; d: string }[]; ponto: [number, number] };

/**
 * Cartão com o mapa (cobre a parte de cima da cena de revelação, sobre o vídeo da chegada à praça).
 * m.entra = o cartão desce; m.cidade = o ponto cai em Bruxelas e o nome aparece; m.pais = a Bélgica acende e o mapa
 * abre para mostrar os vizinhos. Tempos em segundos da cena.
 */
export const MapaCartao: React.FC<{ t: number; dados: DadosMapa; m: Record<string, number>; x: number; y: number; w: number; h: number }> = ({ t, dados, m, x, y, w, h }) => {
  if (t < m.entra) return null;
  const [cx, cy] = dados.ponto;
  const e = ease(clamp((t - m.entra) / 0.3));
  // zoom: começa perto de Bruxelas e abre na palavra "Bélgica" (o país inteiro e os vizinhos)
  const abre = lerp(t, m.pais - 0.1, m.pais + 0.6, 0, 1, easeInOut);
  const largura = lerp(abre, 0, 1, 46, 120, (v) => v) * (1 + 0.06 * (1 - e));
  const alturaV = (largura * h) / w;
  const vx = cx - largura / 2;
  const vy = cy - alturaV * 0.5;
  const acende = clamp((t - m.pais) / 0.2);
  const ponto = ease(clamp((t - m.cidade) / 0.25));
  const onda = (((t - m.cidade) % 0.9) + 0.9) % 0.9 / 0.9;
  const px = ((cx - vx) / largura) * w;
  const py = ((cy - vy) / alturaV) * h;
  const rotulo = ease(clamp((t - m.cidade - 0.08) / 0.2));
  const pais = ease(clamp((t - m.pais) / 0.22));
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        borderRadius: 20,
        overflow: "hidden",
        background: "#121417",
        boxShadow: "0 18px 60px rgba(0,0,0,0.55)",
        opacity: e,
        translate: `0 ${(1 - e) * -40}px`,
      }}
    >
      <svg width={w} height={h} viewBox={`${vx} ${vy} ${largura} ${alturaV}`} style={{ position: "absolute", inset: 0 }}>
        {dados.paises.map((p) => {
          const be = p.nome === "Belgium";
          return (
            <path
              key={p.nome}
              d={p.d}
              fill={be ? `rgba(224,174,92,${0.16 + 0.74 * acende})` : "#4A443B"}
              stroke={be ? PALETA.ambar : "#6A6257"}
              strokeWidth={be ? 2.5 : 1}
              vectorEffect="non-scaling-stroke"
            />
          );
        })}
      </svg>
      {ponto > 0 && (
        <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
          <circle cx={px} cy={py} r={18 + 50 * onda} fill="none" stroke={PALETA.branco} strokeWidth={4} opacity={(1 - onda) * ponto} />
          <circle cx={px} cy={py - (1 - ponto) * 100} r={15} fill={PALETA.branco} stroke={PALETA.preto} strokeWidth={4} opacity={ponto} />
          <circle cx={px} cy={py - (1 - ponto) * 100} r={6.5} fill="#E2582C" opacity={ponto} />
        </svg>
      )}
      {rotulo > 0 && (
        <div
          style={{
            position: "absolute",
            left: px + 30,
            top: py - 22,
            font: `800 38px ${TEXTO}`,
            color: PALETA.branco,
            letterSpacing: 1,
            textShadow: "0 2px 12px rgba(0,0,0,0.9)",
            opacity: rotulo,
            translate: `${(1 - rotulo) * -14}px 0`,
          }}
        >
          BRUXELAS
        </div>
      )}
      {pais > 0 && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 26,
            textAlign: "center",
            font: `400 76px ${TITULO}`,
            color: PALETA.branco,
            textShadow: "0 4px 24px rgba(0,0,0,0.8)",
            opacity: pais,
            translate: `0 ${(1 - pais) * 24}px`,
          }}
        >
          BÉLGICA
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ antes / depois */

/**
 * Cortina antes/depois: uma linha clara atravessa a imagem da esquerda para a direita e, atrás dela, a imagem de hoje
 * substitui a de 1695 (a mesma praça). p = progresso 0 → 1 (já com a curva).
 */
export const Cortina: React.FC<{ p: number; w: number; h: number; children: React.ReactNode }> = ({ p, w, h, children }) => {
  if (p <= 0) return null;
  const x = p * (w + 40) - 20;
  return (
    <>
      <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, clipPath: `inset(0 ${Math.max(0, w - x)}px 0 0)` }}>{children}</div>
      {p < 1 && (
        <div
          style={{
            position: "absolute",
            left: x - 3,
            top: 0,
            width: 6,
            height: h,
            background: "#FFF6E8",
            boxShadow: "0 0 26px 8px rgba(255,214,150,0.65)",
          }}
        />
      )}
    </>
  );
};

/* ------------------------------------------------------------------ ícone de envio (CTA do meio) */

/** Avião de papel (o gesto de "enviar"), em círculo branco; aparece em m.entra e sai voando em m.voa. */
export const Envio: React.FC<{ t: number; m: Record<string, number>; x: number; y: number }> = ({ t, m, x, y }) => {
  const e = clamp((t - m.entra) / 0.22);
  const pop = e < 1 ? 1.15 * ease(e) - (0.15 * Math.max(0, e - 0.7)) / 0.3 : 1;
  const v = clamp((t - m.voa) / 0.4);
  const vv = v * v;
  if (t < m.entra) return null;
  return (
    <div style={{ position: "absolute", left: x - 90, top: y - 90, width: 180, height: 180, scale: String(Math.max(0, pop)) }}>
      <div style={{ position: "absolute", inset: 0, borderRadius: 90, background: PALETA.branco, opacity: 1 - v, boxShadow: "0 10px 40px rgba(0,0,0,0.45)" }} />
      <svg width={180} height={180} viewBox="0 0 180 180" style={{ position: "absolute", inset: 0, translate: `${vv * 520}px ${-vv * 640}px`, rotate: `${-12 * v}deg` }}>
        <path d="M44 88 L138 46 L104 140 L88 100 Z M88 100 L138 46" fill={v > 0 ? PALETA.ambar : "none"} stroke={v > 0 ? PALETA.ambar : PALETA.preto} strokeWidth={9} strokeLinejoin="round" />
      </svg>
    </div>
  );
};

/* ------------------------------------------------------------------ transições */

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS.md, 10.4): luz quente desce do topo em 3 quadros, pico de até 85% por 4
 * quadros com o corte no meio, recua para o canto em 4 quadros. */
export const LuzPassagem: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte; // em quadros
  let a = 0;
  if (d >= -5 && d < -2) a = lerp(d, -5, -2, 0.08, 0.85, (x) => x);
  else if (d >= -2 && d < 2) a = 0.85;
  else if (d >= 2 && d < 6) a = lerp(d, 2, 6, 0.85, 0, (x) => x);
  if (a <= 0) return null;
  const desce = clamp((d + 5) / 3);
  const recua = clamp((d - 2) / 4);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: a,
        mixBlendMode: "screen",
        background: `radial-gradient(ellipse ${1500 - 900 * recua}px ${2600 * desce - 1600 * recua}px at ${540 + 500 * recua}px ${-100 - 200 * recua}px, #FFE2B0 0%, #FFB45E 38%, rgba(226,120,40,0.6) 62%, rgba(0,0,0,0) 100%)`,
      }}
    />
  );
};

/** Clarão de volta: quadro superexposto que volta ao normal em 5 quadros. */
export const Clarao: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte;
  if (d < 0 || d >= 5) return null;
  return <div style={{ position: "absolute", inset: 0, background: "#FFF6E8", opacity: 0.75 * (1 - d / 5), mixBlendMode: "screen" }} />;
};

export const FotoFundo: React.FC<{ src: string; w: number; h: number; filtro: string; posicao?: string }> = ({ src, w, h, filtro, posicao }) => (
  <Img src={staticFile(src)} style={{ position: "absolute", inset: 0, width: w, height: h, objectFit: "cover", objectPosition: posicao, filter: filtro }} />
);
