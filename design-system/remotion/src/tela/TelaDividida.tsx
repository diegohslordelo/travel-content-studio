/**
 * Reel em TELA DIVIDIDA (docs/FORMATOS_REELS.md): apoio em cima (1080 × 900), Diego embaixo, costura em y 900.
 * Linguagem do formato do gancho até antes do CTA (Anton, Inter 800, âmbar #E0AE5C, fundo #14120F, grão 6%).
 * O DS V2 entra só no CTA: placa (Placa.tsx) + clack (decisão do Diego, 28/10/2026).
 * Tudo vem das props montadas por reels/<reel>/revN/revN.py (âncoras por palavra, em ms).
 */
import React from "react";
import { AbsoluteFill, Audio, CalculateMetadataFunction, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { kf } from "../ds/tempo";
import { EASE } from "../ds/tokens";
import { carregarFontesFormato, ANTON, INTER } from "./fontes";

// ---------- valores do formato (FORMATOS_REELS.md, 2, 4, 5.4, 6) ----------
const W = 1080;
const H = 1920;
const COSTURA = 900;
const FUNDO = "#14120F";
const TRACO = "#ECE5D8";
const AMBAR = "#E0AE5C";
const SOMBRA_LEG = "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)";
const FILTRO_FOTO = "grayscale(0.15) contrast(1.05)";

carregarFontesFormato();

// ---------- tipos das props ----------
type Palavra = { txt: string; s: number; e: number; tomada: string };
type Grupo = { palavras: number[]; de: number; ate: number };
type Etiqueta = { txt: string; em: number; x: number; y: number; troca?: boolean; pequena?: boolean; giro?: number; fixa?: boolean };
type Conteudo = Record<string, any> & { tipo: string };
type Cena = { id: string; layout: "dividida" | "apoio" | "diego"; de: number; ate: number; conteudo?: Conteudo; zoom?: [number, number]; entrada?: string };
type Som = { src: string; em: number; ganho_db: number; dur: number };
export type PropsTela = {
  fps: number;
  duracao: number;
  voz: string;
  diegoY: number;
  palavras: Palavra[];
  grupos: Grupo[];
  semLegenda: { de: number; ate: number }[];
  cenas: Cena[];
  sons: Som[];
  gancho: { linhas: { txt: string; em: number; tam: number; destaque?: boolean }[] };
  cta: { destino: string; rotulo?: string; em: number };
  /** Cortes de zoom no rosto (punch-in): durante [de, ate) o Diego fica `esc` vezes maior, com corte seco. */
  zooms?: { de: number; ate: number; esc: number }[];
  popLegenda?: boolean;
};

export const propsTelaVazias: PropsTela = {
  fps: 24, duracao: 1000, voz: "", diegoY: 0, palavras: [], grupos: [], semLegenda: [], cenas: [], sons: [], gancho: { linhas: [] }, cta: { destino: "", em: 0 },
};

export const metadadosTela: CalculateMetadataFunction<PropsTela> = ({ props }) => ({
  fps: props.fps,
  durationInFrames: Math.max(1, Math.round((props.duracao * props.fps) / 1000)),
});

const useMsAbs = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (f * 1000) / fps;
};

const sai = EASE.out;
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));

// ---------- peças comuns ----------
const semente = (txt: string) => txt.split("").reduce((a, ch) => (a * 31 + ch.charCodeAt(0)) % 1000, 7);
const Foto: React.FC<{ src: string; t: number; dur: number; zoom?: [number, number]; foco?: [number, number]; filtro?: string; mao?: number }> = ({ src, t, dur, zoom = [1, 1.07], foco = [0.5, 0.5], filtro, mao = 1 }) => {
  const z = zoom[0] + (zoom[1] - zoom[0]) * clamp(t / dur) + 0.02 * mao;
  const k = semente(src);
  const dx = mao * (Math.sin(t / 830 + k) * 5 + Math.sin(t / 370 + k * 2) * 2);
  const dy = mao * (Math.sin(t / 970 + k * 3) * 4 + Math.sin(t / 290 + k) * 1.5);
  const rot = mao * Math.sin(t / 1300 + k) * 0.25;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: FUNDO }}>
      <Img
        src={staticFile(`img/${src}.jpg`)}
        style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`, transform: `translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(${z})`, transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`, filter: filtro ?? FILTRO_FOTO }}
      />
    </AbsoluteFill>
  );
};

/** Etiqueta de preço/informação: entra com "pop" (180 ms) e leve giro. */
const EtiquetaV: React.FC<{ e: Etiqueta; t: number; w: number; h: number; saiEm?: number }> = ({ e, t, w, h, saiEm }) => {
  const d = e.fixa ? 10000 : t - e.em;
  if (d < 0) return null;
  if (saiEm !== undefined && t >= saiEm) return null;
  const esc = kf(d, [0, 120, 200], [0.86, 1.02, 1], [sai, sai]);
  const op = kf(d, [0, 90], [0, 1]);
  const giro = e.troca ? kf(d, [0, 200], [90, 0], sai) : 0;
  const tam = e.pequena ? 44 : 118;
  return (
    <div style={{ position: "absolute", left: e.x * w, top: e.y * h, transform: `translate(-50%, -50%) scale(${esc}) rotate(${e.giro ?? -2}deg) rotateX(${giro}deg)`, opacity: op }}>
      <div
        style={{
          fontFamily: e.pequena ? INTER : ANTON, fontWeight: e.pequena ? 800 : 400, fontSize: tam, lineHeight: 1, color: e.pequena ? TRACO : AMBAR,
          backgroundColor: "rgba(20,18,15,0.88)", padding: e.pequena ? "14px 26px" : "18px 34px 14px", borderRadius: 18, whiteSpace: "nowrap",
          border: `4px solid ${e.pequena ? "rgba(236,229,216,0.35)" : AMBAR}`, boxShadow: "0 18px 40px rgba(0,0,0,0.55)", letterSpacing: e.pequena ? "0.06em" : "0.01em",
        }}
      >
        {e.txt}
      </div>
    </div>
  );
};

/** Texto Anton que sobe de trás de uma máscara (180 ms). */
const TextoSobe: React.FC<{ txt: string; t: number; em: number; tam: number; cor?: string; estilo?: React.CSSProperties }> = ({ txt, t, em, tam, cor = "#fff", estilo }) => {
  const d = t - em;
  if (d < 0) return null;
  const y = kf(d, [0, 180], [tam * 0.9, 0], sai);
  return (
    <div style={{ overflow: "hidden", paddingTop: tam * 0.12, ...estilo }}>
      <div style={{ fontFamily: ANTON, fontSize: tam, lineHeight: 1.02, color: cor, transform: `translateY(${y}px)`, textShadow: "0 6px 28px rgba(0,0,0,0.6)", whiteSpace: "nowrap" }}>{txt}</div>
    </div>
  );
};

// ---------- conteúdos ----------
const Gancho: React.FC<{ c: Conteudo; t: number; dur: number; w: number; h: number; linhas: PropsTela["gancho"]["linhas"]; t0: number }> = ({ c, t, dur, w, h, linhas, t0 }) => {
  const dn = t - (c.notas - t0);
  return (
    <AbsoluteFill>
      <Foto src={c.foto} t={t} dur={dur} zoom={[1.12, 1.0]} foco={[0.5, 0.6]} />
      {c.notas !== undefined && <Notas t={dn} w={w} h={h} />}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.0) 0%, rgba(0,0,0,0.55) 26%, rgba(0,0,0,0.62) 70%, rgba(0,0,0,0.25) 100%)" }} />
      <div style={{ position: "absolute", left: 72, top: 262 }}>
        {linhas.map((l, i) => {
          const d = c.fixo ? 10000 : t - (l.em - t0);
          if (d < 0) return null;
          const op = kf(d, [0, 160], [0, 1]);
          const y = kf(d, [0, 160], [24, 0], sai);
          const pulso = l.destaque && !c.fixo ? kf(d, [0, 120, 260], [0.9, 1.06, 1], [sai, sai]) : 1;
          return (
            <div key={i} style={{ fontFamily: ANTON, fontSize: l.tam, lineHeight: 1.0, color: l.destaque ? AMBAR : "#fff", opacity: op, transform: `translateY(${y}px) scale(${pulso})`, transformOrigin: "left center", textShadow: "0 6px 30px rgba(0,0,0,0.7)", whiteSpace: "nowrap" }}>
              {l.txt}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/** Cédulas desenhadas (ilustração, não foto) caindo: chuva de "milhão". */
const Notas: React.FC<{ t: number; w: number; h: number }> = ({ t, w, h }) => {
  if (t < 0) return null;
  const notas = Array.from({ length: 14 }, (_, i) => {
    const x = ((i * 397) % 1000) / 1000;
    const atraso = (i * 73) % 600;
    const vel = 0.75 + ((i * 31) % 50) / 100;
    const giro0 = ((i * 53) % 60) - 30;
    return { x, atraso, vel, giro0, i };
  });
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {notas.map((n) => {
        const d = t - n.atraso;
        if (d < 0) return null;
        const y = -160 + d * n.vel * 0.9;
        if (y > h + 100) return null;
        const g = n.giro0 + d * 0.06 * (n.i % 2 ? 1 : -1);
        const balanco = Math.sin(d / 220 + n.i) * 30;
        return (
          <div key={n.i} style={{ position: "absolute", left: n.x * (w - 220) + balanco, top: y, width: 220, height: 104, transform: `rotate(${g}deg) rotateX(${Math.sin(d / 300 + n.i) * 40}deg)`, borderRadius: 10, backgroundColor: "#D9CBA3", border: `3px solid ${AMBAR}`, boxShadow: "0 10px 24px rgba(0,0,0,0.45)", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: 32, color: "#5A4A2A", opacity: 0.95 }}>
            <div style={{ position: "absolute", inset: 8, border: "2px solid rgba(90,74,42,0.5)", borderRadius: 6 }} />
            500.000 DONG
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** Painel de câmbio (estilo letreiro de aeroporto): cada valor vira letra por letra na palavra falada. */
const Placar: React.FC<{ c: Conteudo; t: number; t0: number; w: number; h: number }> = ({ c, t, t0 }) => {
  const dc = t - (c.carimbo.em - t0);
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO, alignItems: "center", justifyContent: "center" }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 45%, rgba(224,174,92,0.10), rgba(0,0,0,0) 60%)" }} />
      <div style={{ display: "flex", flexDirection: "column", gap: 38, marginTop: 120 }}>
        {c.linhas.map((l: any, i: number) => {
          const d = t - (l.em - t0);
          const rot = kf(t, [i * 120, i * 120 + 240], [0, 1], sai);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 34, opacity: rot, transform: `translateY(${(1 - rot) * 30}px)` }}>
              <div style={{ width: 250, fontFamily: INTER, fontWeight: 800, fontSize: 58, color: TRACO, letterSpacing: "0.04em" }}>{l.rotulo}</div>
              <div style={{ display: "flex", gap: 8 }}>
                {l.valor.split("").map((ch: string, k: number) => {
                  const dk = d - k * 45;
                  const virado = dk >= 120;
                  const ang = dk < 0 ? 0 : dk < 120 ? kf(dk, [0, 120], [0, 180]) : 180;
                  const mostra = virado ? ch : dk < 60 && dk >= 0 ? " " : d < 0 ? " " : " ";
                  return (
                    <div key={k} style={{ width: ch === " " ? 26 : ch === "," ? 44 : 84, height: 132, backgroundColor: ch === " " ? "transparent" : "#221F1A", borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: 104, color: virado ? (dc >= 0 ? AMBAR : "#fff") : "#fff", boxShadow: ch === " " ? "none" : "inset 0 -66px 0 rgba(255,255,255,0.03), 0 6px 14px rgba(0,0,0,0.5)", position: "relative", transform: `rotateX(${ang > 90 && ang < 180 ? 180 - ang : ang < 90 ? ang : 0}deg)` }}>
                      {ch === " " ? "" : mostra}
                      {ch !== " " && <div style={{ position: "absolute", left: 0, right: 0, top: 65, height: 2, backgroundColor: "rgba(0,0,0,0.6)" }} />}
                    </div>
                  );
                })}
              </div>
              {dc >= 0 && (
                <div style={{ fontFamily: ANTON, fontSize: 96, color: AMBAR, transform: `translateY(${kf(dc - i * 90, [0, 220], [40, 0], sai)}px)`, opacity: kf(dc - i * 90, [0, 160], [0, 1]) }}>↑</div>
              )}
            </div>
          );
        })}
      </div>
      {dc >= 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, margin: "0 auto", top: 255, width: "fit-content", transform: `rotate(-5deg) scale(${kf(dc, [0, 110, 220], [1.6, 0.94, 1], [sai, sai])})`, opacity: kf(dc, [0, 80], [0, 1]), border: `6px solid ${AMBAR}`, borderRadius: 14, padding: "10px 30px 6px", fontFamily: ANTON, fontSize: 76, color: AMBAR, backgroundColor: "rgba(20,18,15,0.85)", whiteSpace: "nowrap" }}>
          {c.carimbo.txt}
        </div>
      )}
    </AbsoluteFill>
  );
};

/** Rota tracejada que se desenha com um avião (ilustração em traço). */
const Aviao: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, w, h }) => {
  const p = kf(t, [0, dur * 0.95], [0, 1], EASE.cinema);
  const path = `M 90 ${h - 140} C ${w * 0.3} ${h * 0.25}, ${w * 0.62} ${h * 0.9}, ${w - 120} ${300}`;
  const comp = 1500;
  // ponto do avião sobre a curva (Bezier cúbica)
  const P = (u: number) => {
    const p0 = [90, h - 140], p1 = [w * 0.3, h * 0.25], p2 = [w * 0.62, h * 0.9], p3 = [w - 120, 300];
    const a = (1 - u) ** 3, b = 3 * (1 - u) ** 2 * u, cc = 3 * (1 - u) * u * u, d = u ** 3;
    return [a * p0[0] + b * p1[0] + cc * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + cc * p2[1] + d * p3[1]];
  };
  const [x, y] = P(p);
  const [x2, y2] = P(Math.min(1, p + 0.01));
  const ang = (Math.atan2(y2 - y, x2 - x) * 180) / Math.PI;
  const ds = t - (c.sonham - t0);
  if (c.semRota) return <Foto src={c.foto} t={t} dur={dur} zoom={c.zoom ?? [1.0, 1.12]} foco={[0.5, 0.45]} />;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      {c.foto && <Foto src={c.foto} t={t} dur={dur} zoom={[1.0, 1.08]} foco={[0.5, 0.45]} filtro={`${FILTRO_FOTO} brightness(0.5)`} />}
      <AbsoluteFill style={{ background: "radial-gradient(circle at 30% 70%, rgba(224,174,92,0.10), rgba(0,0,0,0) 55%)" }} />
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        {Array.from({ length: 9 }, (_, i) => (
          <circle key={i} cx={(i * 211 + 80) % w} cy={280 + ((i * 137) % (h - 380))} r={3} fill="rgba(236,229,216,0.25)" />
        ))}
        <path d={path} fill="none" stroke="rgba(236,229,216,0.18)" strokeWidth={6} strokeDasharray="18 18" />
        <path d={path} fill="none" stroke={AMBAR} strokeWidth={7} strokeDasharray={comp} strokeDashoffset={comp * (1 - p)} strokeLinecap="round" />
        <circle cx={90} cy={h - 140} r={14} fill={TRACO} />
        <g transform={`translate(${w - 120}, 300)`} opacity={ds >= 0 ? kf(ds, [0, 200], [0, 1]) : 0}>
          <g transform={`scale(${ds >= 0 ? kf(ds, [0, 160, 280], [0.4, 1.15, 1], [sai, sai]) : 0})`}>
            <path d="M0 -70 C 38 -70 52 -40 52 -18 C 52 16 0 60 0 60 C 0 60 -52 16 -52 -18 C -52 -40 -38 -70 0 -70 Z" fill={AMBAR} />
            <circle cx={0} cy={-20} r={18} fill={FUNDO} />
          </g>
        </g>
        <g transform={`translate(${x}, ${y}) rotate(${ang + 90})`}>
          <path d="M0 -58 C 7 -58 10 -48 10 -36 L 10 -10 L 58 18 L 58 30 L 10 14 L 10 38 L 24 50 L 24 58 L 0 51 L -24 58 L -24 50 L -10 38 L -10 14 L -58 30 L -58 18 L -10 -10 L -10 -36 C -10 -48 -7 -58 0 -58 Z" fill={TRACO} stroke={FUNDO} strokeWidth={3} />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/** Três cartões (o 3º com "?": gancho secundário). Ou revelados, no fechamento. */
const RECT_CARTAO = (i: number, h: number) => ({ x: 60 + i * 340, y: h / 2 - 210 + 70, w: 300, h: 420 });
const Cartoes: React.FC<{ c: Conteudo; t: number; t0: number; w: number; h: number }> = ({ c, t, t0, h }) => {
  const d0 = t - (c.em - t0);
  const dr = c.rico !== undefined ? t - (c.rico - t0) : -1;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 60%, rgba(224,174,92,0.12), rgba(0,0,0,0) 60%)" }} />
      {c.fotos.map((f: string | null, i: number) => {
        const d = d0 - i * 170;
        if (d < 0) return null;
        const r = RECT_CARTAO(i, h);
        const esc = c.simples ? 1 : kf(d, [0, 160, 260], [0.7, 1.05, 1], [sai, sai]);
        const op = kf(d, [0, c.simples ? 200 : 120], [0, 1]);
        const sobe = c.simples ? kf(d, [0, 200], [20, 0], sai) : 0;
        const balanca = f === null && dr >= 0 ? Math.sin(dr / 60) * kf(dr, [0, 500], [7, 0]) : 0;
        return (
          <div key={i} style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, transform: `translateY(${sobe}px) scale(${esc}) rotate(${c.simples ? 0 : (i - 1) * 3 + balanca}deg)`, opacity: op, borderRadius: 22, overflow: "hidden", boxShadow: "0 24px 50px rgba(0,0,0,0.6)", border: f === null ? `5px solid ${AMBAR}` : "5px solid rgba(236,229,216,0.9)", backgroundColor: "#211D18" }}>
            {f !== null ? (
              <Img src={staticFile(`img/${f}.jpg`)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: FILTRO_FOTO }} />
            ) : (
              <div style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: 230, color: AMBAR, transform: `scale(${c.simples ? 1 : 1 + Math.sin(t / 180) * 0.04})` }}>?</div>
            )}
            <div style={{ position: "absolute", left: 18, top: 12, fontFamily: ANTON, fontSize: 72, color: "#fff", textShadow: "0 4px 18px rgba(0,0,0,0.8)" }}>{i + 1}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** "Número N: PAÍS" sobre a foto; contador opcional (milhão de dong). */
const Numero: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, w, h }) => {
  const k = c.contador;
  const dk = k ? t - (k.de - t0) : -1;
  const saiTitulo = k && dk >= 0 ? kf(dk, [0, 200], [1, 0]) : 1;
  // entrada a partir do cartão 1 (a foto cresce do cartão até a tela: Mergulho)
  let wrap: React.CSSProperties = {};
  if (c.entrada === "cartao0") {
    const r = RECT_CARTAO(0, COSTURA);
    const p = kf(t, [0, 420], [0, 1], EASE.cinema);
    const sx = r.w / w + (1 - r.w / w) * p, sy = r.h / h + (1 - r.h / h) * p;
    const tx = r.x * (1 - p), ty = r.y * (1 - p);
    wrap = { transform: `translate(${tx}px, ${ty}px) scale(${sx}, ${sy})`, transformOrigin: "0 0", borderRadius: 22 * (1 - p), overflow: "hidden", filter: `blur(${kf(t, [0, 200, 420], [0, 6, 0])}px)` };
  }
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      <AbsoluteFill style={wrap}>
        <Foto src={c.foto} t={t} dur={dur} zoom={c.zoom ?? [1.0, 1.1]} foco={c.foco} filtro={k && dk >= 0 ? `${FILTRO_FOTO} brightness(${kf(dk, [0, 250], [1, 0.42])})` : FILTRO_FOTO} />
        <AbsoluteFill style={{ background: h > 1000 ? "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.0) 32%, rgba(0,0,0,0.0) 55%, rgba(0,0,0,0.55) 100%)" : "linear-gradient(180deg, rgba(0,0,0,0) 20%, rgba(0,0,0,0.0) 45%, rgba(0,0,0,0.55) 100%)" }} />
      </AbsoluteFill>
      {c.n && <div style={{ position: "absolute", left: 72, top: c.tituloY ?? 270, opacity: saiTitulo, display: "flex", alignItems: "flex-end", gap: 26 }}>
        <TextoSobe txt={c.n} t={t} em={c.tituloEm !== undefined ? c.tituloEm - t0 : c.entrada === "cartao0" ? 200 : 0} tam={300} cor={AMBAR} />
        <div style={{ paddingBottom: 30 }}>
          <TextoSobe txt={c.nome} t={t} em={(c.tituloEm !== undefined ? c.tituloEm - t0 : c.entrada === "cartao0" ? 200 : 0) + 160} tam={c.nome.length > 7 ? 104 : 128} />
        </div>
      </div>}
      {c.print && t - (c.print.em - t0) >= 0 && (() => {
        const pr = c.print;
        const dp = t - (pr.em - t0);
        const pw = pr.largura ?? 760, ph = (pr.tamanho[1] * pw) / pr.tamanho[0];
        const e = kf(dp, [0, 220], [0, 1], sai);
        return (
          <div style={{ position: "absolute", left: (w - pw) / 2, top: pr.y ?? h * 0.42, width: pw, height: ph, opacity: e, transform: `translateY(${(1 - e) * 40}px)`, borderRadius: 24, overflow: "hidden", boxShadow: "0 24px 60px rgba(0,0,0,0.6)", backgroundColor: "#fff" }}>
            <Img src={staticFile(`img/${pr.src}.jpg`)} style={{ width: "100%", height: "100%", display: "block" }} />
          </div>
        );
      })()}
      {k && dk >= 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: h * 0.36, textAlign: "center" }}>
          <div style={{ fontFamily: ANTON, fontSize: 150, color: "#fff", textShadow: "0 8px 30px rgba(0,0,0,0.7)", transform: `scale(${kf(dk, [0, 140], [0.8, 1], sai)})` }}>
            {Math.round(k.valor * kf(dk, [0, k.ate - k.de], [0, 1], EASE.out)).toLocaleString("pt-BR")}
            {k.sufixo}
          </div>
          {t - (k.igual.em - t0) >= 0 && (
            <div style={{ fontFamily: ANTON, fontSize: 120, color: AMBAR, marginTop: 6, transform: `scale(${kf(t - (k.igual.em - t0), [0, 120, 220], [0.6, 1.08, 1], [sai, sai])})`, textShadow: "0 8px 30px rgba(0,0,0,0.7)" }}>{k.igual.txt}</div>
          )}
        </div>
      )}
    </AbsoluteFill>
  );
};

/** Ícone de tigela em traço (prato de rua). */
const Tigela: React.FC<{ tam: number; cheio: boolean }> = ({ tam, cheio }) => (
  <svg width={tam} height={tam} viewBox="0 0 100 100">
    <path d="M30 30 C 34 20, 26 16, 30 6" stroke={TRACO} strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.7} />
    <path d="M50 30 C 54 20, 46 16, 50 6" stroke={TRACO} strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.7} />
    <path d="M70 30 C 74 20, 66 16, 70 6" stroke={TRACO} strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.7} />
    <path d="M10 44 L 90 44 C 90 70, 72 88, 50 88 C 28 88, 10 70, 10 44 Z" fill={cheio ? AMBAR : "none"} stroke={TRACO} strokeWidth={5} strokeLinejoin="round" />
    <line x1={60} y1={30} x2={92} y2={10} stroke={TRACO} strokeWidth={5} strokeLinecap="round" />
    <line x1={52} y1={32} x2={86} y2={6} stroke={TRACO} strokeWidth={5} strokeLinecap="round" />
  </svg>
);

const Pratos: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, w }) => {
  const a = c.de - t0, b = c.ate - t0;
  const n = Math.floor(kf(t, [a, b], [0, c.n]));
  const cols = 5, tam = 150, gap = 28;
  const largura = cols * tam + (cols - 1) * gap;
  return (
    <AbsoluteFill>
      <Foto src={c.foto} t={t} dur={dur} zoom={[1.0, 1.08]} filtro={`${FILTRO_FOTO} brightness(0.38)`} />
      <div style={{ position: "absolute", left: (w - largura) / 2, top: 470, display: "grid", gridTemplateColumns: `repeat(${cols}, ${tam}px)`, gap }}>
        {Array.from({ length: c.n }, (_, i) => {
          const d = t - a - (i * (b - a)) / c.n;
          const esc = d < 0 ? 0.0 : kf(d, [0, 110, 200], [0.4, 1.12, 1], [sai, sai]);
          return (
            <div key={i} style={{ transform: `scale(${esc})`, opacity: d < 0 ? 0.0 : 1 }}>
              <Tigela tam={tam} cheio={i < n} />
            </div>
          );
        })}
      </div>
      {n > 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 230, textAlign: "center", fontFamily: ANTON, fontSize: 210, color: AMBAR, textShadow: "0 8px 30px rgba(0,0,0,0.7)" }}>{n}</div>
      )}
    </AbsoluteFill>
  );
};

const IconeRefeicao: React.FC<{ tipo: number; tam: number }> = ({ tipo, tam }) => (
  <svg width={tam} height={tam} viewBox="0 0 100 100">
    {tipo === 0 && (
      <g stroke={TRACO} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round">
        <path d="M18 40 L 72 40 L 66 82 L 24 82 Z" />
        <path d="M72 48 C 88 48, 88 70, 70 70" />
        <path d="M36 30 C 40 22, 32 18, 36 10" />
        <path d="M52 30 C 56 22, 48 18, 52 10" />
      </g>
    )}
    {tipo === 1 && <Tigela tam={100} cheio={false} />}
    {tipo === 2 && (
      <g stroke={TRACO} strokeWidth={5} fill="none" strokeLinecap="round">
        <circle cx={50} cy={54} r={30} />
        <circle cx={50} cy={54} r={18} />
        <path d="M10 22 L 10 86 M 4 22 L 4 40 C 4 46, 16 46, 16 40 L 16 22" />
        <path d="M90 22 C 80 30, 80 50, 90 54 L 90 86" />
      </g>
    )}
  </svg>
);

const Refeicoes: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, h }) => {
  const dv = t - (c.valor.em - t0);
  return (
    <AbsoluteFill>
      {c.foto ? <Foto src={c.foto} t={t} dur={dur} zoom={[1.0, 1.08]} filtro={`${FILTRO_FOTO} brightness(0.4)`} /> : <AbsoluteFill style={{ backgroundColor: FUNDO }} />}
      {dv >= 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, top: h > 1000 ? 330 : 275, display: "flex", justifyContent: "center" }}>
          <div style={{ transform: `rotate(-3deg) scale(${kf(dv, [0, 120, 220], [0.5, 1.1, 1], [sai, sai])})`, fontFamily: ANTON, fontSize: h > 1000 ? 200 : 170, color: AMBAR, backgroundColor: "rgba(20,18,15,0.88)", border: `6px solid ${AMBAR}`, borderRadius: 24, padding: "10px 48px 4px" }}>{c.valor.txt}</div>
        </div>
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: h > 1000 ? 720 : 545, display: "flex", justifyContent: "center", gap: 70 }}>
        {c.icones.map((em: number, i: number) => {
          const d = t - (em - t0);
          const aparece = t - (c.valor.em - t0) - 250 - i * 120;
          if (aparece < 0) return <div key={i} style={{ width: 200 }} />;
          return (
            <div key={i} style={{ width: 200, height: 200, position: "relative", opacity: kf(aparece, [0, 150], [0, 1]), transform: `translateY(${kf(aparece, [0, 200], [30, 0], sai)}px)`, borderRadius: 30, backgroundColor: "rgba(20,18,15,0.7)", border: `4px solid ${d >= 0 ? AMBAR : "rgba(236,229,216,0.35)"}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <IconeRefeicao tipo={i} tam={130} />
              {d >= 0 && (
                <div style={{ position: "absolute", right: -22, top: -22, width: 70, height: 70, borderRadius: 35, backgroundColor: AMBAR, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${kf(d, [0, 120, 200], [0, 1.2, 1], [sai, sai])})` }}>
                  <svg width={40} height={40} viewBox="0 0 40 40"><path d="M8 21 L 17 30 L 33 11" stroke={FUNDO} strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/** Calendário: dias marcados um a um ("todo dia"). */
const Calendario: React.FC<{ d: number }> = ({ d }) => {
  if (d < 0) return null;
  const op = kf(d, [0, 150], [0, 1]);
  return (
    <div style={{ position: "absolute", left: 72, bottom: 70, opacity: op, transform: `translateY(${kf(d, [0, 200], [30, 0], sai)}px)`, backgroundColor: "rgba(20,18,15,0.9)", borderRadius: 20, padding: "18px 20px", border: "3px solid rgba(236,229,216,0.3)" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 46px)", gap: 8 }}>
        {Array.from({ length: 14 }, (_, i) => {
          const di = d - 120 - i * 55;
          return (
            <div key={i} style={{ width: 46, height: 46, borderRadius: 10, backgroundColor: di >= 0 ? AMBAR : "rgba(236,229,216,0.12)", display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${di >= 0 ? kf(di, [0, 90, 160], [0.6, 1.15, 1], [sai, sai]) : 1})` }}>
              {di >= 0 && <svg width={26} height={26} viewBox="0 0 40 40"><path d="M8 21 L 17 30 L 33 11" stroke={FUNDO} strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const FotoEtiquetas: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, w, h }) => {
  const ets: Etiqueta[] = c.etiquetas ?? [];
  return (
    <AbsoluteFill>
      <Foto src={c.src} t={t} dur={dur} zoom={c.zoom} foco={c.foco} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.12) 0%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.35) 100%)" }} />
      {ets.map((e, i) => {
        const prox = ets.slice(i + 1).find((o) => o.troca && Math.abs(o.x - e.x) < 0.01 && Math.abs(o.y - e.y) < 0.01);
        return <EtiquetaV key={i} e={{ ...e, em: e.em - t0 }} t={t} w={w} h={h} saiEm={prox ? prox.em - t0 : undefined} />;
      })}
      {c.calendario && <Calendario d={t - (c.calendario.em - t0)} />}
    </AbsoluteFill>
  );
};

/** Egito: o cartão "?" do começo volta, gira e revela as pirâmides em tela cheia (fecha o gancho secundário). */
const Revela: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number }> = ({ c, t, dur, t0, w, h }) => {
  const dv = t - (c.virar - t0);
  const ent = kf(t, [0, 260], [0, 1], sai);
  const cw = 520, ch = 720;
  const giro = dv < 0 ? 0 : kf(dv, [0, 260], [0, 180], EASE.cinema);
  const frente = giro < 90;
  const expande = dv < 280 ? 0 : kf(dv - 280, [0, 420], [0, 1], EASE.cinema);
  const x = (w - cw) / 2 * (1 - expande), y = ((h - ch) / 2 - 120) * (1 - expande);
  const ww = cw + (w - cw) * expande, hh = ch + (h - ch) * expande;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 42%, rgba(224,174,92,0.16), rgba(0,0,0,0) 55%)" }} />
      <div style={{ position: "absolute", left: x, top: y, width: ww, height: hh, transform: `perspective(1600px) rotateY(${frente ? giro : giro - 180}deg) scale(${0.85 + 0.15 * ent})`, opacity: ent, borderRadius: 26 * (1 - expande), overflow: "hidden", border: expande > 0.98 ? "none" : `6px solid ${frente ? AMBAR : "rgba(236,229,216,0.9)"}`, boxShadow: "0 30px 60px rgba(0,0,0,0.6)", backgroundColor: "#211D18" }}>
        {frente ? (
          <div style={{ width: "100%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: 380, color: AMBAR, transform: `scale(${1 + Math.sin(t / 160) * 0.04})` }}>?</div>
        ) : (
          <Foto src={c.foto} t={Math.max(0, dv)} dur={dur} zoom={[1.15, 1.0]} foco={c.foco ?? [0.5, 0.55]} />
        )}
        <div style={{ position: "absolute", left: 26, top: 14, fontFamily: ANTON, fontSize: 110, color: "#fff", textShadow: "0 4px 18px rgba(0,0,0,0.8)", opacity: frente ? 1 : 0 }}>{c.n}</div>
      </div>
      {dv >= 640 && (
        <div style={{ position: "absolute", left: 72, top: 300, display: "flex", alignItems: "flex-end", gap: 26 }}>
          <TextoSobe txt={c.n} t={dv} em={640} tam={300} cor={AMBAR} />
          <div style={{ paddingBottom: 30 }}>
            <TextoSobe txt={c.nome} t={dv} em={800} tam={150} />
          </div>
        </div>
      )}
      {dv >= 280 && <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.0) 60%, rgba(0,0,0,0.6) 100%)", opacity: expande }} />}
    </AbsoluteFill>
  );
};

/** "R$ 6 × € 1": a moeda de 1 euro que não se compra (ilustração). */
const Euro: React.FC<{ c: Conteudo; t: number; t0: number; w: number; h: number }> = ({ c, t, t0, w }) => {
  const dm = t - (c.moeda - t0);
  const dx = t - (c.xis - t0);
  const r = 230;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 38%, rgba(224,174,92,0.18), rgba(0,0,0,0) 55%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 330, display: "flex", justifyContent: "center" }}>
        <div style={{ fontFamily: ANTON, fontSize: 170, color: "#fff", transform: `rotate(-3deg) scale(${kf(t, [0, 120, 220], [0.6, 1.08, 1], [sai, sai])})`, backgroundColor: "rgba(236,229,216,0.08)", border: "5px solid rgba(236,229,216,0.4)", borderRadius: 24, padding: "4px 44px 0" }}>R$ 6</div>
      </div>
      {dm >= 0 && (
        <svg width={w} height={r * 2 + 60} style={{ position: "absolute", left: 0, top: 640 }}>
          <g transform={`translate(${w / 2}, ${r + 30}) scale(${kf(dm, [0, 140, 240], [0.3, 1.08, 1], [sai, sai])}) rotate(${kf(dm, [0, 240], [-30, 0], sai)})`}>
            <circle r={r} fill="#C9A35C" stroke="#8E6E33" strokeWidth={10} />
            <circle r={r * 0.68} fill="#B9B3A6" stroke="#6F6A60" strokeWidth={8} />
            <text x={0} y={30} textAnchor="middle" fontFamily={ANTON} fontSize={180} fill="#3A3832">1</text>
            <text x={0} y={-r * 0.78} textAnchor="middle" fontFamily={ANTON} fontSize={56} fill="#5A4520">EURO</text>
            {Array.from({ length: 12 }, (_, i) => {
              const a = (i / 12) * Math.PI * 2;
              return <text key={i} x={Math.cos(a) * r * 0.84} y={Math.sin(a) * r * 0.84 + 12} textAnchor="middle" fontSize={34} fill="#5A4520">★</text>;
            })}
            {dx >= 0 && (
              <g stroke={AMBAR} strokeWidth={34} strokeLinecap="round">
                <line x1={-r * 0.95} y1={-r * 0.95} x2={-r * 0.95 + r * 1.9 * kf(dx, [0, 140], [0, 1], sai)} y2={-r * 0.95 + r * 1.9 * kf(dx, [0, 140], [0, 1], sai)} />
                {dx > 120 && <line x1={r * 0.95} y1={-r * 0.95} x2={r * 0.95 - r * 1.9 * kf(dx - 120, [0, 140], [0, 1], sai)} y2={-r * 0.95 + r * 1.9 * kf(dx - 120, [0, 140], [0, 1], sai)} />}
              </g>
            )}
          </g>
        </svg>
      )}
    </AbsoluteFill>
  );
};

/** Print real da cotação (enviado pelo Diego): entra como captura (flash de 80 ms) e os valores são marcados na palavra falada. */
const Print: React.FC<{ c: Conteudo; t: number; t0: number; w: number; h: number }> = ({ c, t, t0, w, h }) => {
  const pw = c.largura ?? 940;
  const esc = pw / c.tamanho[0];
  const ph = c.tamanho[1] * esc;
  const x0 = (w - pw) / 2, y0 = c.topo ?? 300;
  const te = c.em !== undefined ? t - (c.em - t0) : t;
  const ent = kf(te, [0, 220], [0, 1], sai);
  const flash = c.flash === false ? 0 : kf(te, [0, 40, 120], [0.9, 0.9, 0]);
  const dc = c.carimbo ? t - (c.carimbo.em - t0) : -1;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      {c.fundo && <Foto src={c.fundo} t={t} dur={c.dur ?? 3000} zoom={[1.04, 1.1]} filtro={`${FILTRO_FOTO} brightness(0.42)`} />}
      {!c.fundo && <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 50%, rgba(224,174,92,0.12), rgba(0,0,0,0) 60%)" }} />}
      <div style={{ position: "absolute", left: x0, top: c.centro ? (h - ph) / 2 + (c.desloc ?? 0) : y0, width: pw, height: ph, transform: `translateY(${(1 - ent) * 40}px)`, opacity: ent, borderRadius: c.raio ?? 28, overflow: "hidden", boxShadow: "0 30px 70px rgba(0,0,0,0.7)", border: "4px solid rgba(236,229,216,0.85)" }}>
        <Img src={staticFile(`img/${c.src}.jpg`)} style={{ width: "100%", height: "100%", display: "block" }} />
        <svg width={pw} height={ph} style={{ position: "absolute", inset: 0 }}>
          {(c.marcas ?? []).map((m: any, i: number) => {
            const d = t - (m.em - t0);
            if (d < 0) return null;
            const rw = m.w * esc, rh = m.h * esc, per = 2 * (rw + rh);
            const p = kf(d, [0, 260], [0, 1], sai);
            return (
              <g key={i}>
                <rect x={m.x * esc} y={m.y * esc} width={rw} height={rh} rx={18} fill={`rgba(224,174,92,${0.18 * p})`} />
                <rect x={m.x * esc} y={m.y * esc} width={rw} height={rh} rx={18} fill="none" stroke={AMBAR} strokeWidth={7} strokeDasharray={per} strokeDashoffset={per * (1 - p)} />
              </g>
            );
          })}
        </svg>
        <AbsoluteFill style={{ backgroundColor: "#fff", opacity: flash }} />
      </div>
      {dc >= 0 && (
        <div style={{ position: "absolute", left: 0, right: 0, margin: "0 auto", top: y0 + ph - 46, width: "fit-content", transform: `rotate(-4deg) scale(${kf(dc, [0, 110, 220], [1.6, 0.94, 1], [sai, sai])})`, opacity: kf(dc, [0, 80], [0, 1]), border: `6px solid ${AMBAR}`, borderRadius: 14, padding: "10px 30px 6px", fontFamily: ANTON, fontSize: 76, color: AMBAR, backgroundColor: "rgba(20,18,15,0.9)", whiteSpace: "nowrap" }}>
          {c.carimbo.txt}
        </div>
      )}
    </AbsoluteFill>
  );
};

/** Cartão "?" parado no centro (gancho secundário, versão simples: sem giro). */
const Interrogacao: React.FC<{ c: Conteudo; t: number; w: number; h: number }> = ({ c, t, w, h }) => {
  const cw = 480, ch = 660;
  const e = kf(t, [0, 200], [0, 1], sai);
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 50% 42%, rgba(224,174,92,0.14), rgba(0,0,0,0) 55%)" }} />
      <div style={{ position: "absolute", left: (w - cw) / 2, top: (h - ch) / 2 - 140, width: cw, height: ch, opacity: e, borderRadius: 26, border: `6px solid ${AMBAR}`, backgroundColor: "#211D18", boxShadow: "0 30px 60px rgba(0,0,0,0.6)", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: ANTON, fontSize: 360, color: AMBAR }}>
        ?
        <div style={{ position: "absolute", left: 26, top: 14, fontFamily: ANTON, fontSize: 110, color: "#fff" }}>{c.n}</div>
      </div>
    </AbsoluteFill>
  );
};

/** Vídeo de apoio gravado pelo Diego (mudo, cobre a área, sem filtro). */
const VideoApoio: React.FC<{ c: Conteudo; t0: number }> = ({ c, t0 }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.round((t0 * fps) / 1000)} layout="none">
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: FUNDO }}>
      <OffthreadVideo src={staticFile(`video/${c.src}.mp4`)} muted startFrom={Math.round(((c.inicio ?? 0) * fps) / 1000)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: `50% ${(c.focoY ?? 0.5) * 100}%` }} />
    </AbsoluteFill>
    </Sequence>
  );
};

const ConteudoV: React.FC<{ c: Conteudo; t: number; dur: number; t0: number; w: number; h: number; props: PropsTela }> = ({ c, t, dur, t0, w, h, props }) => {
  switch (c.tipo) {
    case "gancho":
      return <Gancho c={c} t={t} dur={dur} w={w} h={h} linhas={props.gancho.linhas} t0={t0} />;
    case "placar":
      return <Placar c={c} t={t} t0={t0} w={w} h={h} />;
    case "aviao":
      return <Aviao c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "cartoes":
      return <Cartoes c={c} t={t} t0={t0} w={w} h={h} />;
    case "numero":
      return <Numero c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "pratos":
      return <Pratos c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "refeicoes":
      return <Refeicoes c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "foto":
      return <FotoEtiquetas c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "revela":
      return <Revela c={c} t={t} dur={dur} t0={t0} w={w} h={h} />;
    case "video":
      return <VideoApoio c={c} t0={t0} />;
    case "interrogacao":
      return <Interrogacao c={c} t={t} w={w} h={h} />;
    case "print":
      return <Print c={c} t={t} t0={t0} w={w} h={h} />;
    case "euro":
      return <Euro c={c} t={t} t0={t0} w={w} h={h} />;
    default:
      return <AbsoluteFill style={{ backgroundColor: "#f0f", color: "#fff", fontSize: 60 }}>FALTA: {c.tipo}</AbsoluteFill>;
  }
};

// ---------- legenda: acende palavra a palavra, no tempo da fala ----------
const Legenda: React.FC<{ props: PropsTela; ms: number; y: number }> = ({ props, ms, y }) => {
  if (props.semLegenda.some((s) => ms >= s.de && ms < s.ate)) return null;
  const g = props.grupos.find((x) => ms >= x.de - 60 && ms < x.ate);
  if (!g) return null;
  const d = ms - (g.de - 60);
  const op = kf(d, [0, 120], [0, 1]);
  const esc = kf(d, [0, 120], [0.94, 1], sai);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, transform: `translateY(-50%) scale(${esc})`, opacity: op, display: "flex", justifyContent: "center" }}>
      <div style={{ fontFamily: INTER, fontWeight: 800, fontSize: 66, lineHeight: 1.1, whiteSpace: "nowrap", textShadow: SOMBRA_LEG, maxWidth: 872, textAlign: "center" }}>
        {g.palavras.map((i, k) => {
          const p = props.palavras[i];
          const dita = ms >= p.s;
          const agora = ms >= p.s && ms < p.e + 40;
          const pop = agora && props.popLegenda ? kf(ms - p.s, [0, 90, 180], [1, 1.1, 1.04], [sai, sai]) : 1;
          return (
            <span key={k} style={{ display: "inline-block", color: dita ? AMBAR : "#FFFFFF", transform: `scale(${pop})`, margin: "0 0.13em" }}>
              {p.txt}
            </span>
          );
        })}
      </div>
    </div>
  );
};

// ---------- grão (6%, overlay) ----------
const Grao: React.FC<{ seed: number }> = ({ seed }) => (
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity: 0.06, pointerEvents: "none" }}>
    <filter id={`g${seed}`}>
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={seed} stitchTiles="stitch" />
      <feColorMatrix type="saturate" values="0" />
    </filter>
    <rect width={W} height={H} filter={`url(#g${seed})`} />
  </svg>
);

// ---------- composição ----------
export const TelaDividida: React.FC<PropsTela> = (props) => {
  const ms = useMsAbs();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const idx = Math.max(0, props.cenas.findIndex((c) => ms >= c.de && ms < c.ate));
  const cena = props.cenas[idx] ?? props.cenas[0];
  if (!cena) return <AbsoluteFill style={{ backgroundColor: "#000" }} />;
  const anterior = props.cenas[idx - 1];
  const t = ms - cena.de;
  const dur = cena.ate - cena.de;

  // posição do Diego: dividida = vídeo inteiro deslocado (rosto a ~42% da metade de baixo); diego = tela cheia com aproximação lenta
  let diegoY = props.diegoY;
  let diegoEsc = 1;
  let topoY = 0; // deslocamento da metade de cima (entrada "desce")
  if (cena.layout === "diego") {
    diegoY = 0;
    const z = cena.zoom ?? [1, 1.05];
    diegoEsc = z[0] + (z[1] - z[0]) * clamp(t / dur);
  } else if (cena.layout === "dividida" && anterior?.layout === "diego") {
    // Empurrão ao contrário: a metade de cima desce e o Diego volta para baixo, com desaceleração (≈ 420 ms)
    const p = kf(t, [0, 420], [0, 1], EASE.cinema);
    topoY = -COSTURA * (1 - p);
    diegoY = props.diegoY * p;
  }
  for (const z of props.zooms ?? []) if (ms >= z.de && ms < z.ate) diegoEsc *= z.esc;
  const yLeg = cena.layout === "dividida" ? COSTURA : 1320;
  const qms = 1000 / fps;
  let luz = 0;
  for (const c of props.cenas) {
    if (c.entrada !== "luz") continue;
    const d = (ms - c.de) / qms; // em quadros, 0 = corte
    if (d >= -5 && d <= 6) luz = Math.max(luz, kf(d, [-5, -2, 2, 6], [0.08, 0.85, 0.85, 0], [EASE.out, EASE.out, EASE.out]));
  }
  const clarao = cena.entrada === "clarao" ? kf(t, [0, 40, 170], [0.85, 0.85, 0], EASE.out) : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Diego (sempre rodando; mudo aqui, o áudio vem do <Audio> abaixo) */}
      <AbsoluteFill style={{ opacity: cena.layout === "apoio" ? 0 : 1 }}>
        <OffthreadVideo src={staticFile(props.voz)} muted style={{ position: "absolute", left: 0, top: 0, width: W, height: H, transform: `translateY(${diegoY}px) scale(${diegoEsc})`, transformOrigin: "50% 700px" }} />
      </AbsoluteFill>

      {/* apoio */}
      {cena.conteudo && cena.layout !== "diego" && (
        <div style={{ position: "absolute", left: 0, top: topoY, width: W, height: cena.layout === "dividida" ? COSTURA : H, overflow: "hidden" }}>
          <ConteudoV c={cena.conteudo} t={t} dur={dur} t0={cena.de} w={W} h={cena.layout === "dividida" ? COSTURA : H} props={props} />
        </div>
      )}
      {cena.layout === "dividida" && <div style={{ position: "absolute", left: 0, top: COSTURA - 3 + topoY, width: W, height: 6, backgroundColor: "rgba(0,0,0,0.55)" }} />}

      {/* degradê para a legenda em tela cheia */}
      {cena.layout !== "dividida" && <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 960, background: "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.62) 100%)", opacity: cena.layout === "diego" ? 0.55 : 0.8 }} />}

      <Legenda props={props} ms={ms} y={yLeg} />

      {/* CTA: placa do DS V2 (única peça do DS no Reel) */}
      {ms >= props.cta.em && <Sequence from={Math.round((props.cta.em * fps) / 1000)} layout="none"><Placa rotulo={props.cta.rotulo} destino={props.cta.destino} modulo="seta" entrada={0} /></Sequence>}

      {luz > 0 && <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 0%, rgba(255,214,150,1) 0%, rgba(255,170,90,0.9) 45%, rgba(255,140,60,0.55) 100%)", opacity: luz, mixBlendMode: "screen" }} />}
      {clarao > 0 && <AbsoluteFill style={{ backgroundColor: "#FFF6E6", opacity: clarao }} />}
      <Grao seed={f % 8} />

      {/* áudio: voz + efeitos */}
      <Audio src={staticFile(props.voz)} />
      {props.sons.map((s, i) => (
        <Sequence key={i} from={Math.max(0, Math.round((s.em * fps) / 1000))} durationInFrames={Math.round(((s.dur + 200) * fps) / 1000)} layout="none">
          <Audio src={staticFile(s.src)} volume={Math.min(1, Math.pow(10, s.ganho_db / 20))} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
