/**
 * Reel narrado · "Barcelona acaba com os viajantes que não montam um roteiro com estratégia" · REV1
 * (reels/barcelona-3-dias/rev1). Pedido do Diego (17/11/2026):
 * - narração dele (9 gravações) decupada sem falhas; imagens do vlog do YouTube (Barcelona_3dias), na vertical e mudas;
 * - takes limpos e estáticos, sem repetir vídeo; animação só onde ajuda a compor a fala;
 * - legenda que acompanha a fala, com a palavra dita colorida (karaokê); nada aparece antes de ser dito;
 * - Design System V2 só no fim (placa do CTA + clack). Música: o Diego coloca depois (entrega sem trilha).
 * Linguagem do formato (FORMATOS_REELS 5.4 e 6): Anton/Inter, fundo #14120F, traço #ECE5D8, destaque âmbar #E0AE5C.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Easing,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import pdxImpacto from "../../../sons/externos/PDX_impacto.wav";
import pdxSwish from "../../../sons/externos/PDX_swish.wav";
import pdxObturador from "../../../sons/externos/PDX_obturador.wav";
import pdxRiser from "../../../sons/externos/PDX_riser.wav";
import pdxArLongo from "../../../sons/externos/PDX_ar_longo.wav";
import pdxPagina from "../../../sons/externos/PDX_pagina.wav";

/* Linguagem do formato (FORMATOS_REELS 5.4) */
const FUNDO = "#14120F";
const TRACO = "#ECE5D8";
const AMBAR = "#E0AE5C";
const COR_DIA = ["#FF7A59", AMBAR, "#6FC3DF"]; // rotas do mapa (só deste Reel)
const SOMBRA_TXT = "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)";
const W = 1080;
const H = 1920;
const LEG_Y = 1320; // FORMATOS_REELS 6: legenda em tela cheia

let fontesOk = false;
const fontes = () => {
  if (fontesOk) return;
  fontesOk = true;
  loadFont({ family: "Anton", url: staticFile("fontes/anton-latin-400-normal.woff2"), weight: "400" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-800-normal.woff2"), weight: "800" });
};

type Palavra = { w: string; s: number; e: number };
type Rot = { txt: string; t: number }[];
type Tile = { src: string; t: number; nome: Rot; foco?: number };
export type CenaBcn = {
  ini: number;
  fim: number;
  tipo: "video" | "split" | "grade" | "mapa" | "retrato";
  src?: string;
  zoom?: [number, number];
  foco?: number; // posição vertical do recorte quando a imagem fica em meia tela (0 = topo, 1 = base)
  srcB?: string;
  tB?: number; // B entra na metade de baixo
  tC?: number; // B ocupa a tela toda
  focoB?: number;
  tiles?: Tile[];
  rotulo?: Rot;
  rotuloY?: number;
  dados?: Record<string, number>;
  mergulhoSai?: { t: number; x: number; y: number }; // zoom através de um ponto no fim da cena
  mergulhoEntra?: number; // duração da entrada (s) vindo do desfoque
};
type Sfx = { t: number; som: keyof typeof SFX; db: number };
export type PropsBarcelona = {
  dur: number;
  palavras: Palavra[];
  cenas: CenaBcn[];
  grupos: number[][];
  gancho: { fim: number; linhas: { tam: number; palavras: number[] }[] };
  dias: { t: number; txt: string }[];
  sfx: Sfx[];
  cta: { ini: number; rotulo: string; destino: string };
};

export const propsBarcelonaVazias: PropsBarcelona = {
  dur: 1, palavras: [], cenas: [], grupos: [], gancho: { fim: 0, linhas: [] }, dias: [], sfx: [],
  cta: { ini: 0, rotulo: "", destino: "SALVA" },
};

export const metadadosBarcelona: CalculateMetadataFunction<PropsBarcelona> = ({ props }) => ({
  durationInFrames: Math.ceil(props.dur * 30 - 1e-6),
});

const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lin = (t: number, a: number, b: number, v0: number, v1: number, e: (x: number) => number = ease) =>
  interpolate(t, [a, b], [v0, v1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
/** Entra no instante t0 (nunca antes). */
const entra = (t: number, t0: number, d = 0.2) => (t < t0 ? 0 : lin(t, t0, t0 + d, 0, 1));

const Palavras: React.FC<{ itens: Rot; t: number; estilo: React.CSSProperties; sobe?: number }> = ({ itens, t, estilo, sobe = 18 }) => (
  <div style={estilo}>
    {itens.map((p, i) => {
      const o = entra(t, p.t, 0.12);
      return (
        <span key={i} style={{ display: "inline-block", opacity: o, transform: `translateY(${(1 - o) * sobe}px)`, whiteSpace: "pre" }}>
          {(i ? " " : "") + p.txt}
        </span>
      );
    })}
  </div>
);

/** Vídeo vertical 1080×1920 numa caixa: cobre a caixa, recorte vertical por "foco". */
const VideoCaixa: React.FC<{ src: string; x: number; y: number; w: number; h: number; zoom?: number; foco?: number; filtro?: string }> = ({
  src, x, y, w, h, zoom = 1, foco = 0.5, filtro,
}) => {
  const k = Math.max(w / W, h / H) * zoom;
  const vw = W * k;
  const vh = H * k;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: (w - vw) / 2, top: (h - vh) * foco, width: vw, height: vh, filter: filtro }}>
        <Video src={staticFile(src)} muted style={{ width: vw, height: vh }} />
      </div>
    </div>
  );
};

/* ---------- cenas ---------- */

const CenaVideo: React.FC<{ c: CenaBcn; t: number }> = ({ c, t }) => {
  const z = c.zoom ?? [1.0, 1.05];
  let k = lin(t, c.ini, c.fim, z[0], z[1], Easing.linear);
  let ox = 0;
  let oy = 0;
  let blur = 0;
  let escurece = 0;
  if (c.mergulhoSai && t >= c.mergulhoSai.t) {
    // zoom através do ponto (portal da Sagrada): acelera, desfoca e clareia no corte
    const p = lin(t, c.mergulhoSai.t, c.fim, 0, 1, Easing.in(Easing.cubic));
    k *= 1 + 1.6 * p;
    ox = (0.5 - c.mergulhoSai.x) * W * (k - 1);
    oy = (0.5 - c.mergulhoSai.y) * H * (k - 1);
    blur = 14 * p;
    escurece = 0.35 * p;
  }
  if (c.mergulhoEntra) {
    const p = lin(t, c.ini, c.ini + c.mergulhoEntra, 1, 0, Easing.out(Easing.cubic));
    k *= 1 + 0.25 * p;
    blur = Math.max(blur, 14 * p);
    escurece = Math.max(escurece, 0.35 * p);
  }
  return (
    <AbsoluteFill style={{ background: FUNDO }}>
      <div style={{ position: "absolute", inset: 0, transform: `translate(${ox}px, ${oy}px) scale(${k})`, filter: blur ? `blur(${blur}px)` : undefined }}>
        <Video src={staticFile(c.src!)} muted style={{ width: W, height: H }} />
      </div>
      {escurece > 0 && <AbsoluteFill style={{ background: `rgba(255,236,200,${escurece})` }} />}
      {c.rotulo && <Rotulo itens={c.rotulo} t={t} y={c.rotuloY ?? 560} />}
    </AbsoluteFill>
  );
};

/** Rótulo grande (Anton) sobre o vídeo, palavra por palavra, só com o que é dito. */
const Rotulo: React.FC<{ itens: Rot; t: number; y: number; tam?: number }> = ({ itens, t, y, tam = 230 }) => {
  const t0 = itens.length ? itens[0].t : Infinity;
  const p = entra(t, t0, 0.22);
  return (
    <>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 40%, rgba(0,0,0,0.45), rgba(0,0,0,0) 70%)", opacity: p }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: y, textAlign: "center", transform: `scale(${t < t0 ? 1.25 : lin(t, t0, t0 + 0.22, 1.25, 1, Easing.out(Easing.back(1.6)))})` }}>
        <Palavras itens={itens} t={t} sobe={0} estilo={{ fontFamily: "Anton", fontSize: tam, lineHeight: 1, color: AMBAR, textShadow: "0 6px 0 rgba(0,0,0,0.35), 0 10px 40px rgba(0,0,0,0.6)" }} />
      </div>
    </>
  );
};

/** A em tela cheia → em tB, A sobe para a metade de cima e B entra na de baixo → em tC, B ocupa tudo. */
const CenaSplit: React.FC<{ c: CenaBcn; t: number }> = ({ c, t }) => {
  const tB = c.tB!;
  const tC = c.tC!;
  const d = 0.38;
  const pb = lin(t, tB, tB + d, 0, 1, Easing.inOut(Easing.cubic));
  const pc = lin(t, tC, tC + d, 0, 1, Easing.inOut(Easing.cubic));
  // caixa de A
  const aH = H - (H / 2) * pb;
  const aY = -(H / 2) * pc;
  // caixa de B
  const bY = H - (H / 2) * pb - (H / 2) * pc;
  const bH = H / 2 + (H / 2) * pc;
  const zA = lin(t, c.ini, tC + d, 1.0, 1.05, Easing.linear);
  const zB = lin(t, tB, c.fim, 1.04, 1.0, Easing.linear);
  const fB = Math.round((tB - c.ini) * 30);
  return (
    <AbsoluteFill style={{ background: FUNDO }}>
      {pc < 1 && <VideoCaixa src={c.src!} x={0} y={aY} w={W} h={aH} zoom={zA} foco={c.foco ?? 0.5} />}
      {t >= tB && (
        <Sequence from={fB} layout="none">
          <VideoCaixa src={c.srcB!} x={0} y={bY} w={W} h={bH} zoom={zB} foco={c.focoB ?? 0.5} />
        </Sequence>
      )}
      {t >= tB && pc < 1 && <div style={{ position: "absolute", left: 0, top: bY - 3, width: W, height: 6, background: "rgba(0,0,0,0.55)" }} />}
    </AbsoluteFill>
  );
};

/** Lista rápida: cada lugar entra num quadro da grade no instante em que é dito. */
const CenaGrade: React.FC<{ c: CenaBcn; t: number }> = ({ c, t }) => {
  const tiles = c.tiles!;
  const tw = 476;
  const th = 430;
  const gx = [50, 554];
  const gy = [392, 842]; // abaixo do marcador do dia (y ≤ 370) e acima da legenda (topo em 1283)
  return (
    <AbsoluteFill style={{ background: FUNDO }}>
      {tiles.map((tl, i) => {
        const p = entra(t, tl.t, 0.26);
        if (t < tl.t) return null;
        const x = gx[i % 2];
        const y = gy[Math.floor(i / 2)];
        const s = 0.86 + 0.14 * lin(t, tl.t, tl.t + 0.26, 0, 1, Easing.out(Easing.back(1.5)));
        return (
          <Sequence key={i} from={Math.round((tl.t - c.ini) * 30)} layout="none">
            <div style={{ position: "absolute", left: x, top: y, width: tw, height: th, borderRadius: 22, overflow: "hidden", opacity: p, transform: `scale(${s})`, boxShadow: "0 18px 40px rgba(0,0,0,0.55)", border: `5px solid ${TRACO}` }}>
              <VideoCaixa src={tl.src} x={0} y={0} w={tw - 10} h={th - 10} zoom={lin(t, tl.t, c.fim, 1.0, 1.06, Easing.linear)} foco={tl.foco ?? 0.5} />
              <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 160, background: "linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,0.75))" }} />
              <Palavras itens={tl.nome} t={t} sobe={10} estilo={{ position: "absolute", left: 8, right: 8, bottom: 22, textAlign: "center", fontFamily: "Anton", fontSize: 58, lineHeight: 1, color: "#fff", textShadow: SOMBRA_TXT }} />
            </div>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

/* Mapa de Barcelona simplificado (desenho, não é mapa oficial): posições por latitude/longitude reais. */
const LON0 = 2.112;
const LAT0 = 41.421;
const KX = 11000; // px por grau de longitude (Camp Nou em x ≈ 165, Barceloneta em x ≈ 941: dentro da zona segura)
const KY = KX / Math.cos((41.39 * Math.PI) / 180);
const MX = (lon: number) => 46 + (lon - LON0) * KX;
const MY = (lat: number) => 330 + (LAT0 - lat) * KY; // Park Güell y ≈ 425 · Montjuïc y ≈ 1176 (legenda em 1283)
const caminho = (pts: [number, number][], fecha = false) =>
  pts.map(([lo, la], i) => `${i ? "L" : "M"} ${MX(lo).toFixed(1)} ${MY(la).toFixed(1)}`).join(" ") + (fecha ? " Z" : "");
const COSTA: [number, number][] = [
  [2.150, 41.330], [2.163, 41.350], [2.172, 41.362], [2.176, 41.370], [2.181, 41.373], [2.186, 41.372],
  [2.189, 41.369], [2.191, 41.373], [2.194, 41.380], [2.199, 41.386], [2.207, 41.391], [2.216, 41.396], [2.228, 41.403], [2.240, 41.410],
];
const MAR: [number, number][] = [...COSTA, [2.240, 41.330]];
const VERDES: [number, number][][] = [
  [[2.150, 41.372], [2.160, 41.375], [2.170, 41.369], [2.168, 41.360], [2.157, 41.360], [2.149, 41.366]], // Montjuïc
  [[2.183, 41.392], [2.190, 41.389], [2.188, 41.385], [2.182, 41.388]], // Ciutadella
  [[2.148, 41.416], [2.156, 41.416], [2.157, 41.412], [2.149, 41.411]], // Park Güell
];
const ROTAS: [number, number][][] = [
  // dia 1: Camp Nou → Montjuïc → Colombo → Barceloneta → Ciutadella → Arco do Triunfo
  [[2.1228, 41.3809], [2.1661, 41.3633], [2.1777, 41.3758], [2.1925, 41.3784], [2.1873, 41.3881], [2.1806, 41.3910]],
  // dia 2: Casa Vicens → Gótico (Catedral) → La Rambla/Boqueria → Passeig de Gràcia (Batlló, Milà)
  [[2.1508, 41.4035], [2.1762, 41.3840], [2.1716, 41.3817], [2.1650, 41.3916], [2.1619, 41.3953]],
  // dia 3: Sagrada Família → Park Güell
  [[2.1744, 41.4036], [2.1527, 41.4145]],
];

const CenaMapa: React.FC<{ c: CenaBcn; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const tRotas = d.rotas ?? c.ini + 0.5; // antes do início da cena = rotas já desenhadas
  const dest = d.destaque ?? 0; // rota do dia em destaque (0 = dia 1, 2 = dia 3)
  const tDest = d.tDestaque ?? c.fim;
  const tDist = d.distantes ?? c.fim;
  const abre = lin(t, c.ini, c.ini + 0.35, 0, 1);
  const foco = lin(t, tDest, tDest + 0.4, 0, 1);
  const pulso = t >= tDist ? 0.5 + 0.5 * Math.sin((t - tDist) * 10) : 0;
  return (
    <AbsoluteFill style={{ background: FUNDO, opacity: 0.3 + 0.7 * abre, transform: `scale(${0.96 + 0.04 * abre})` }}>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        <path d={caminho(MAR, true)} fill="#1C2C35" />
        <path d={caminho(COSTA)} fill="none" stroke={TRACO} strokeWidth={4} strokeOpacity={0.7} />
        {VERDES.map((v, i) => <path key={i} d={caminho(v, true)} fill="#26331F" />)}
        {ROTAS.map((r, i) => {
          const t0 = tRotas + i * 0.42;
          const p = tRotas < c.ini ? 1 : lin(t, t0, t0 + 0.55, 0, 1, Easing.inOut(Easing.cubic));
          const pts = r.map(([lo, la]) => ({ x: MX(lo), y: MY(la) }));
          const len = pts.slice(1).reduce((s, q, k) => s + Math.hypot(q.x - pts[k].x, q.y - pts[k].y), 0);
          const eh = i === dest;
          const apaga = eh ? 1 : 1 - 0.7 * foco;
          return (
            <g key={i} opacity={(t >= t0 || tRotas < c.ini ? 1 : 0) * apaga}>
              <path d={caminho(r)} fill="none" stroke={COR_DIA[i]} strokeWidth={eh ? 10 + 4 * foco : 10} strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
              {pts.map((q, k) => {
                const vis = p >= k / Math.max(1, pts.length - 1) - 0.001;
                const raio = eh ? 15 + 9 * pulso * foco : 13;
                return <circle key={k} cx={q.x} cy={q.y} r={vis ? raio : 0} fill={COR_DIA[i]} stroke="#fff" strokeWidth={5} />;
              })}
            </g>
          );
        })}
      </svg>
      {d.barcelona !== undefined && (
        <Palavras itens={[{ txt: "BARCELONA", t: d.barcelona }]} t={t} estilo={{ position: "absolute", left: 0, width: 944, top: 278, textAlign: "right", fontFamily: "Anton", fontSize: 84, color: TRACO, letterSpacing: 5, opacity: 0.9 }} />
      )}
    </AbsoluteFill>
  );
};

/** Retrato em cartão (foto de arquivo, domínio público), com o nome quando é dito. */
const CenaRetrato: React.FC<{ c: CenaBcn; t: number }> = ({ c, t }) => {
  const p = lin(t, c.ini, c.ini + 0.3, 0, 1);
  const z = lin(t, c.ini, c.fim, 1.0, 1.06, Easing.linear);
  return (
    <AbsoluteFill style={{ background: FUNDO }}>
      <div style={{ position: "absolute", left: 110, top: 300, width: 860, height: 960, borderRadius: 20, overflow: "hidden", boxShadow: "0 24px 60px rgba(0,0,0,0.6)", opacity: p, transform: `translateY(${(1 - p) * 60}px)` }}>
        <Img src={staticFile(c.src!)} style={{ width: 860, height: 960, objectFit: "cover", objectPosition: "50% 22%", transform: `scale(${z})`, filter: "grayscale(1) contrast(1.05)" }} />
      </div>
      {c.rotulo && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 1000 }}>
          <Palavras itens={c.rotulo} t={t} sobe={20} estilo={{ textAlign: "center", fontFamily: "Anton", fontSize: 190, color: AMBAR, textShadow: "0 6px 0 rgba(0,0,0,0.45), 0 10px 40px rgba(0,0,0,0.6)" }} />
        </div>
      )}
    </AbsoluteFill>
  );
};

/* ---------- textos ---------- */

const Legenda: React.FC<{ p: PropsBarcelona; t: number }> = ({ p, t }) => {
  const idx = p.grupos.findIndex((gr, k) => {
    const a = p.palavras[gr[0]].s;
    const prox = p.grupos[k + 1];
    const fimG = p.palavras[gr[gr.length - 1]].e + 0.3;
    const b = prox ? Math.min(p.palavras[prox[0]].s, fimG) : fimG;
    return t >= a && t < b;
  });
  if (idx < 0) return null;
  const g = p.grupos[idx];
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: LEG_Y - 37, textAlign: "center" }}>
      <span style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, textShadow: SOMBRA_TXT }}>
        {g.map((i, j) => {
          const w = p.palavras[i];
          const prox = j < g.length - 1 ? p.palavras[g[j + 1]].s : w.e + 0.15;
          const o = entra(t, w.s, 0.06);
          const ativa = t >= w.s && t < Math.max(w.e, prox);
          return (
            <span key={i} style={{ color: ativa ? AMBAR : "#fff", opacity: o, whiteSpace: "pre" }}>
              {(j ? " " : "") + w.w}
            </span>
          );
        })}
      </span>
    </div>
  );
};

/** Gancho: texto grande, palavra por palavra, a palavra dita em âmbar. */
const Gancho: React.FC<{ p: PropsBarcelona; t: number }> = ({ p, t }) => {
  if (!p.gancho.linhas.length || t >= p.gancho.fim) return null;
  let y = 300;
  return (
    <>
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.55), rgba(0,0,0,0.25) 45%, rgba(0,0,0,0) 62%)" }} />
      {p.gancho.linhas.map((l, i) => {
        const top = y;
        y += l.tam * 1.06;
        return (
          <div key={i} style={{ position: "absolute", left: 72, top, fontFamily: "Anton", fontSize: l.tam, lineHeight: 1.05, textShadow: "0 4px 24px rgba(0,0,0,0.65)", whiteSpace: "pre" }}>
            {l.palavras.map((k, j) => {
              const w = p.palavras[k];
              const o = entra(t, w.s, 0.12);
              const prox = k + 1 < p.palavras.length ? p.palavras[k + 1].s : w.e;
              const ativa = t >= w.s && t < Math.max(w.e, prox);
              return (
                <span key={j} style={{ display: "inline-block", opacity: o, transform: `translateY(${(1 - o) * 24}px)`, color: ativa ? AMBAR : "#fff" }}>
                  {(j ? " " : "") + w.w}
                </span>
              );
            })}
          </div>
        );
      })}
    </>
  );
};

/** Marcador do dia (linguagem do formato, não é objeto do DS): entra quando o dia é dito. */
const MarcaDia: React.FC<{ p: PropsBarcelona; t: number }> = ({ p, t }) => {
  const atual = [...p.dias].reverse().find((d) => t >= d.t);
  if (!atual || t >= p.cta.ini) return null;
  const pop = lin(t, atual.t, atual.t + 0.3, 0, 1, Easing.out(Easing.back(1.8)));
  return (
    <div style={{ position: "absolute", left: 72, top: 280, transform: `scale(${0.7 + 0.3 * pop})`, transformOrigin: "0% 50%", opacity: Math.min(1, pop * 1.5) }}>
      <div style={{ fontFamily: "Anton", fontSize: 78, lineHeight: 1, color: "#fff", textShadow: SOMBRA_TXT, letterSpacing: 2 }}>{atual.txt}</div>
      <div style={{ width: 120, height: 10, background: AMBAR, marginTop: 8, borderRadius: 5, boxShadow: "0 3px 12px rgba(0,0,0,0.5)" }} />
    </div>
  );
};

const SFX = { impacto: pdxImpacto, swish: pdxSwish, obturador: pdxObturador, riser: pdxRiser, ar_longo: pdxArLongo, pagina: pdxPagina } as const;

export const BarcelonaReel: React.FC<PropsBarcelona> = (p) => {
  fontes();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const cena = p.cenas.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cenas[p.cenas.length - 1];
  const fromC = Math.round(cena.ini * fps);
  const legendaVisivel = t >= p.gancho.fim && t < p.cta.ini;
  return (
    <AbsoluteFill style={{ background: FUNDO }}>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(2.5 * fps)}>
          <Audio src={SFX[s.som]} volume={Math.pow(10, s.db / 20)} />
        </Sequence>
      ))}
      <Sequence key={cena.ini} from={fromC} durationInFrames={Math.max(1, Math.round(cena.fim * fps) - fromC + 2)} layout="none">
        {cena.tipo === "video" && <CenaVideo c={cena} t={t} />}
        {cena.tipo === "split" && <CenaSplit c={cena} t={t} />}
        {cena.tipo === "grade" && <CenaGrade c={cena} t={t} />}
        {cena.tipo === "mapa" && <CenaMapa c={cena} t={t} />}
        {cena.tipo === "retrato" && <CenaRetrato c={cena} t={t} />}
      </Sequence>
      {/* degradê da legenda (FORMATOS_REELS 3: tela cheia clara precisa de base escura) */}
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.62) 100%)" }} />
      <MarcaDia p={p} t={t} />
      <Gancho p={p} t={t} />
      {legendaVisivel && <Legenda p={p} t={t} />}
      <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} entrada={p.cta.ini * 1000} />
      <Som nome="clack" em={p.cta.ini * 1000} relDb={-6} refLufs={-14} />
    </AbsoluteFill>
  );
};
