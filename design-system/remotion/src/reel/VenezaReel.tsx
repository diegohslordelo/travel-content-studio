/**
 * Reel em tela dividida · "Veneza não te quer lá" (reels/veneza-bate-volta/rev1).
 * Linguagem do formato (docs/FORMATOS_REELS.md): Anton/Inter, destaque âmbar, grão; DS V2 só no CTA (placa + clack).
 * Legenda karaokê (pedido do Diego, 12/11/2026): a palavra que está sendo dita fica âmbar; as outras, brancas.
 * Tempos nas props em segundos da linha do tempo final.
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

const AMBAR = "#E0AE5C";
const FUNDO = "#14120F";
const TRACO = "#ECE5D8";
const COSTURA = 900;

let fontesOk = false;
const fontes = () => {
  if (fontesOk) return;
  fontesOk = true;
  loadFont({ family: "Anton", url: staticFile("fontes/anton-latin-400-normal.woff2"), weight: "400" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-800-normal.woff2"), weight: "800" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-600-normal.woff2"), weight: "600" });
};

type Palavra = { w: string; s: number; e: number };
type Cena = {
  ini: number;
  fim: number;
  tipo: "video" | "foto" | "diego" | "graf";
  src?: string;
  /** cheia = apoio em tela cheia (Diego sai); diego = Diego em tela cheia */
  cheia?: boolean;
  graf?: string;
  dados?: Record<string, unknown>;
  escuro?: number;
  zoom?: [number, number];
};
type Sfx = { t: number; som: "impacto" | "swish" | "obturador" | "riser"; db: number };
export type PropsVeneza = {
  dur: number;
  palavras: Palavra[];
  cenas: Cena[];
  grupos: number[][];
  gancho: { linhas: { txt: string; t: number; tam: number; cor?: string }[]; fim: number }[];
  sfx: Sfx[];
  cta: { ini: number };
};

export const propsVenezaVazias: PropsVeneza = { dur: 1, palavras: [], cenas: [], grupos: [], gancho: [], sfx: [], cta: { ini: 0 } };

export const metadadosVeneza: CalculateMetadataFunction<PropsVeneza> = ({ props }) => ({
  durationInFrames: Math.ceil(props.dur * 30),
});

const useT = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return f / fps;
};

const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lin = (t: number, a: number, b: number, v0: number, v1: number, e = ease) =>
  interpolate(t, [a, b], [v0, v1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });

/* ---------- camadas ---------- */

const Diego: React.FC<{ cheio: boolean; zoom: number }> = ({ cheio, zoom }) => {
  // vídeo 1080×1920. Dividida: rosto (≈ y 610 no quadro) a 42% da metade de baixo → desloca +700.
  const dy = cheio ? 0 : 700;
  return (
    <AbsoluteFill style={{ top: cheio ? 0 : COSTURA, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top: cheio ? 0 : dy - COSTURA, width: 1080, height: 1920, transform: `scale(${zoom})`, transformOrigin: "50% 32%" }}>
        <Video src={staticFile("diego.mp4")} muted style={{ width: 1080, height: 1920 }} />
      </div>
    </AbsoluteFill>
  );
};

const Apoio: React.FC<{ c: Cena; t: number }> = ({ c, t }) => {
  const H = c.cheia ? 1920 : COSTURA;
  const z = c.zoom ?? [1.0, 1.07];
  const k = lin(t, c.ini, c.fim, z[0], z[1], Easing.linear);
  const filtro = c.tipo === "video" ? "saturate(0.85) contrast(1.06) brightness(0.98)" : "contrast(1.05)";
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, overflow: "hidden", background: "#000" }}>
      <div style={{ position: "absolute", inset: 0, transform: `scale(${k})` }}>
        {c.tipo === "video" ? (
          <div style={{ position: "absolute", left: 0, width: 1080, height: 1920, top: (H - 1920) / 2 }}>
            <Video src={staticFile(c.src!)} muted style={{ width: 1080, height: 1920, filter: filtro }} />
          </div>
        ) : (
          <Img src={staticFile(c.src!)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: filtro }} />
        )}
      </div>
      {c.escuro ? <AbsoluteFill style={{ background: `rgba(0,0,0,${c.escuro})` }} /> : null}
      {c.cheia ? <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.62) 100%)" }} /> : null}
    </div>
  );
};

/* ---------- grafismos (fundo escuro do formato) ---------- */

const Num: React.FC<{ txt: string; t0: number; t: number; tam: number; y: number; cor?: string }> = ({ txt, t0, t, tam, y, cor }) => {
  const p = lin(t, t0, t0 + 0.22, 0, 1);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, textAlign: "center", fontFamily: "Anton", fontSize: tam, lineHeight: 1, color: cor ?? TRACO, opacity: p, transform: `translateY(${(1 - p) * 40}px) scale(${0.9 + 0.1 * p})` }}>
      {txt}
    </div>
  );
};

const Rotulo: React.FC<{ txt: string; t0: number; t: number; y: number; cor?: string }> = ({ txt, t0, t, y, cor }) => {
  const p = lin(t, t0, t0 + 0.2, 0, 1);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, textAlign: "center", fontFamily: "Inter", fontWeight: 600, fontSize: 40, letterSpacing: 4, color: cor ?? TRACO, opacity: p * 0.9 }}>
      {txt}
    </div>
  );
};

const Pessoa: React.FC<{ x: number; y: number; cor: string; p: number; s?: number }> = ({ x, y, cor, p, s = 1 }) => (
  <g transform={`translate(${x},${y + (1 - p) * 30}) scale(${s})`} opacity={p}>
    <circle cx={0} cy={-62} r={26} fill={cor} />
    <path d="M -42 40 Q -42 -24 0 -26 Q 42 -24 42 40 Z" fill={cor} />
  </g>
);

const Grafismo: React.FC<{ c: Cena; t: number }> = ({ c, t }) => {
  const d = (c.dados ?? {}) as Record<string, number | string>;
  const H = c.cheia ? 1920 : COSTURA;
  const base: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: H, background: FUNDO, overflow: "hidden" };
  const g = c.graf;
  const at = (k: string) => Number(d[k] ?? c.ini);

  if (g === "milhoes") {
    // contador 0 → 30.000.000 e multidão de pontos
    const p = lin(t, c.ini, c.ini + 1.1, 0, 1, Easing.out(Easing.cubic));
    const n = Math.round(p * 30);
    const pts = Array.from({ length: 220 }, (_, i) => i);
    return (
      <div style={base}>
        <svg width={1080} height={H} style={{ position: "absolute", inset: 0 }}>
          {pts.map((i) => {
            const x = ((i * 137.5) % 1000) + 40;
            const y = ((i * 71.3) % (H - 120)) + 60;
            const on = i / pts.length < p;
            return <circle key={i} cx={x} cy={y} r={6} fill={TRACO} opacity={on ? 0.14 : 0} />;
          })}
        </svg>
        <Num txt={`${n} MILHÕES`} t0={c.ini} t={t} tam={170} y={H / 2 - 150} />
        <Rotulo txt="DE VISITANTES POR ANO" t0={c.ini + 0.3} t={t} y={H / 2 + 50} />
      </div>
    );
  }
  if (g === "tres4") {
    const t0 = at("t3");
    return (
      <div style={base}>
        <svg width={1080} height={H} style={{ position: "absolute", inset: 0 }}>
          {[0, 1, 2, 3].map((i) => {
            const p = lin(t, c.ini + i * 0.12, c.ini + i * 0.12 + 0.25, 0, 1);
            const amb = i < 3 && t >= t0 + i * 0.1;
            return <Pessoa key={i} x={240 + i * 200} y={H / 2 - 20} cor={amb ? AMBAR : "#5A544B"} p={p} s={1.7} />;
          })}
        </svg>
        <Num txt="3 EM CADA 4" t0={t0} t={t} tam={120} y={H / 2 + 110} cor={AMBAR} />
      </div>
    );
  }
  if (g === "print") {
    // print da Fortune (03/01/2024): manchete e o trecho dos 80%
    const p1 = lin(t, c.ini, c.ini + 0.3, 0, 1);
    const p2 = lin(t, at("t2"), at("t2") + 0.3, 0, 1);
    return (
      <div style={{ ...base, background: "#1d1b18" }}>
        <div style={{ position: "absolute", left: 60, top: 70, width: 960, background: "#fff", borderRadius: 18, boxShadow: "0 20px 60px rgba(0,0,0,0.6)", padding: "34px 40px", opacity: p1, transform: `translateY(${(1 - p1) * 40}px) rotate(-1deg)` }}>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 30, letterSpacing: 2, color: "#111" }}>FORTUNE · 03/01/2024</div>
          <Img src={staticFile("fortune_titulo.png")} style={{ width: "100%", marginTop: 14 }} />
        </div>
        <div style={{ position: "absolute", left: 90, top: 470, width: 900, background: "#fff", borderRadius: 14, boxShadow: "0 20px 60px rgba(0,0,0,0.7)", padding: 26, opacity: p2, transform: `translateY(${(1 - p2) * 60}px) scale(${0.96 + 0.04 * p2}) rotate(1deg)` }}>
          <Img src={staticFile("fortune_80.png")} style={{ width: "100%" }} />
        </div>
      </div>
    );
  }
  if (g === "pedagio") {
    // catraca/bilhete com QR
    const p = lin(t, c.ini, c.ini + 0.35, 0, 1);
    const qr = Array.from({ length: 81 }, (_, i) => ((i * 7919) % 13) % 3 !== 0);
    return (
      <div style={base}>
        <div style={{ position: "absolute", left: 250, top: 120, width: 580, height: 560, background: TRACO, borderRadius: 26, transform: `translateY(${(1 - p) * 500}px) rotate(${(1 - p) * -8}deg)`, boxShadow: "0 30px 70px rgba(0,0,0,0.6)" }}>
          <div style={{ position: "absolute", left: 40, top: 34, fontFamily: "Anton", fontSize: 92, color: FUNDO }}>PEDÁGIO</div>
          <div style={{ position: "absolute", left: 40, top: 170, width: 300, height: 300, display: "grid", gridTemplateColumns: "repeat(9,1fr)", gap: 4 }}>
            {qr.map((on, i) => (
              <div key={i} style={{ background: on ? FUNDO : "transparent" }} />
            ))}
          </div>
          <div style={{ position: "absolute", right: 40, top: 200, width: 150, height: 240, borderLeft: `6px dashed ${FUNDO}` }} />
        </div>
      </div>
    );
  }
  if (g === "precos") {
    const t10 = at("t10");
    return (
      <div style={base}>
        <Num txt="5 €" t0={c.ini} t={t} tam={230} y={150} cor={t < t10 ? AMBAR : TRACO} />
        <Rotulo txt="PROGRAMADO" t0={c.ini + 0.2} t={t} y={410} />
        <div style={{ position: "absolute", left: 540, top: 140, width: 4, height: 0 }} />
        <Num txt="10 €" t0={t10} t={t} tam={230} y={500} cor={AMBAR} />
        <Rotulo txt="NA HORA" t0={t10 + 0.2} t={t} y={760} />
      </div>
    );
  }
  if (g === "multa") {
    const p = lin(t, c.ini, c.ini + 0.18, 0, 1, Easing.out(Easing.back(2)));
    const shake = t - c.ini < 0.35 ? Math.sin((t - c.ini) * 90) * 10 * (1 - (t - c.ini) / 0.35) : 0;
    return (
      <div style={{ ...base, background: "#2a0f0c" }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: H / 2 - 170, textAlign: "center", transform: `translateX(${shake}px) rotate(-6deg) scale(${2 - p})`, opacity: p }}>
          <span style={{ fontFamily: "Anton", fontSize: 250, color: "#ff5a4a", border: "14px solid #ff5a4a", borderRadius: 30, padding: "0 50px" }}>MULTA</span>
        </div>
      </div>
    );
  }
  if (g === "mapa") return <Mapa c={c} t={t} H={H} />;
  if (g === "barato") {
    const p = lin(t, at("t25"), at("t25") + 0.9, 0, 1, Easing.out(Easing.cubic));
    return (
      <div style={base}>
        <Rotulo txt="HOSPEDAGEM EM VERONA" t0={c.ini} t={t} y={150} />
        <Num txt={`ATÉ ${Math.round(25 * p)}%`} t0={at("t25")} t={t} tam={220} y={260} cor={AMBAR} />
        <Rotulo txt="MAIS BARATO" t0={at("t25") + 0.3} t={t} y={530} />
        <div style={{ position: "absolute", left: 240, top: 640, width: 600, height: 26, background: "#3a352e", borderRadius: 13 }}>
          <div style={{ width: `${100 - 25 * p}%`, height: "100%", background: AMBAR, borderRadius: 13 }} />
        </div>
      </div>
    );
  }
  if (g === "reserva") {
    const t5 = at("t5");
    const p = lin(t, c.ini, c.ini + 0.3, 0, 1);
    return (
      <div style={base}>
        <div style={{ position: "absolute", left: 140, top: 150, width: 360, height: 400, background: TRACO, borderRadius: 24, opacity: p, transform: `translateY(${(1 - p) * 60}px)` }}>
          <div style={{ height: 90, background: AMBAR, borderRadius: "24px 24px 0 0" }} />
          <div style={{ textAlign: "center", fontFamily: "Anton", fontSize: 170, color: FUNDO, marginTop: 10 }}>4</div>
          <div style={{ textAlign: "center", fontFamily: "Inter", fontWeight: 800, fontSize: 40, color: FUNDO }}>DIAS ANTES</div>
        </div>
        <div style={{ position: "absolute", left: 560, top: 150, width: 380, height: 400, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <div style={{ fontFamily: "Anton", fontSize: 220, color: AMBAR, opacity: lin(t, t5, t5 + 0.2, 0, 1), transform: `scale(${lin(t, t5, t5 + 0.25, 1.4, 1)})` }}>5 €</div>
        </div>
        {d.tLink ? <Rotulo txt="LINK NA LEGENDA ↓" t0={Number(d.tLink)} t={t} y={680} cor={AMBAR} /> : null}
      </div>
    );
  }
  return <div style={base} />;
};

/** Mapa estilizado Verona → Veneza (posições pela longitude/latitude reais, escala aproximada). */
const Mapa: React.FC<{ c: Cena; t: number; H: number }> = ({ c, t, H }) => {
  // Verona 45.438 N 10.994 E · Veneza 45.437 N 12.335 E · Pádua 45.406 N 11.877 E · Vicenza 45.546 N 11.546 E
  const X = (lon: number) => 120 + ((lon - 10.75) / (12.6 - 10.75)) * 840;
  const Y = (lat: number) => 470 - ((lat - 45.43) / 0.5) * 840;
  const vr = { x: X(10.994), y: Y(45.438) };
  const ve = { x: X(12.335), y: Y(45.437) };
  const pts = [vr, { x: X(11.546), y: Y(45.546) }, { x: X(11.877), y: Y(45.406) }, { x: X(12.23), y: Y(45.48) }, ve];
  const p = lin(t, c.ini + 0.3, c.ini + 1.6, 0, 1, Easing.inOut(Easing.cubic));
  const path = pts.map((q, i) => `${i ? "L" : "M"} ${q.x} ${q.y}`).join(" ");
  const len = 900;
  const trem = (() => {
    const seg = p * (pts.length - 1);
    const i = Math.min(Math.floor(seg), pts.length - 2);
    const f = seg - i;
    return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * f, y: pts[i].y + (pts[i + 1].y - pts[i].y) * f };
  })();
  const pin = (q: { x: number; y: number }, nome: string, t0: number, dir: number) => {
    const s = lin(t, t0, t0 + 0.25, 0, 1, Easing.out(Easing.back(2)));
    return (
      <g transform={`translate(${q.x},${q.y}) scale(${s})`}>
        <circle r={22} fill={AMBAR} />
        <circle r={9} fill={FUNDO} />
        <text x={0} y={dir * 70} textAnchor="middle" fontFamily="Anton" fontSize={64} fill={TRACO}>
          {nome}
        </text>
      </g>
    );
  };
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, background: "#1b2a22", overflow: "hidden" }}>
      <svg width={1080} height={H} style={{ position: "absolute", inset: 0 }}>
        {/* Adriático e laguna (contorno simplificado) */}
        <path d={`M ${X(12.18)} ${H} L ${X(12.2)} ${Y(45.3)} Q ${X(12.3)} ${Y(45.4)} ${X(12.45)} ${Y(45.47)} Q ${X(12.55)} ${Y(45.52)} 1080 ${Y(45.6)} L 1080 ${H} Z`} fill="#20425a" />
        <path d={`M ${X(12.26)} ${Y(45.38)} Q ${X(12.32)} ${Y(45.47)} ${X(12.42)} ${Y(45.5)}`} stroke="#2f5f7d" strokeWidth={30} fill="none" opacity={0.6} />
        <path d={path} stroke="#3c4b42" strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={path} stroke={AMBAR} strokeWidth={10} fill="none" strokeDasharray={len} strokeDashoffset={len * (1 - p)} strokeLinecap="round" strokeLinejoin="round" />
        {pin(vr, "VERONA", c.ini, -1)}
        {pin(ve, "VENEZA", c.ini + 1.3, -1)}
        <g transform={`translate(${trem.x},${trem.y})`} opacity={p > 0 && p < 1 ? 1 : 0}>
          <rect x={-26} y={-16} width={52} height={32} rx={10} fill={TRACO} />
        </g>
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: H - 250, textAlign: "center", opacity: lin(t, c.ini + 1.4, c.ini + 1.7, 0, 1) }}>
        <span style={{ fontFamily: "Anton", fontSize: 110, color: TRACO }}>1H E POUQUINHO</span>
        <div style={{ fontFamily: "Inter", fontWeight: 600, fontSize: 38, letterSpacing: 4, color: TRACO, opacity: 0.85 }}>DE TREM</div>
      </div>
    </div>
  );
};

/* ---------- legenda karaokê ---------- */

const Legenda: React.FC<{ p: PropsVeneza; t: number; y: number }> = ({ p, t, y }) => {
  const g = p.grupos.find((gr) => {
    const a = p.palavras[gr[0]].s - 0.05;
    const prox = p.grupos[p.grupos.indexOf(gr) + 1];
    const fimG = p.palavras[gr[gr.length - 1]].e + 0.35;
    const b = prox ? Math.min(p.palavras[prox[0]].s - 0.05, fimG) : fimG;
    return t >= a && t < b;
  });
  if (!g) return null;
  const t0 = p.palavras[g[0]].s - 0.05;
  const k = lin(t, t0, t0 + 0.12, 0.94, 1);
  const o = lin(t, t0, t0 + 0.12, 0, 1);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y - 40, textAlign: "center", opacity: o, transform: `scale(${k})` }}>
      <span style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
        {g.map((i, j) => {
          const w = p.palavras[i];
          const ativa = t >= w.s - 0.03 && (t < w.e || (j < g.length - 1 ? t < p.palavras[g[j + 1]].s - 0.03 : t < w.e + 0.15));
          return (
            <span key={i} style={{ color: ativa ? AMBAR : "#fff" }}>
              {(j ? " " : "") + w.w.toUpperCase()}
            </span>
          );
        })}
      </span>
    </div>
  );
};

/* ---------- gancho ---------- */
const Gancho: React.FC<{ p: PropsVeneza; t: number }> = ({ p, t }) => {
  const bloco = p.gancho.find((b) => t >= b.linhas[0].t - 0.05 && t < b.fim);
  if (!bloco) return null;
  let y = 290;
  return (
    <>
      <AbsoluteFill style={{ height: COSTURA, background: "linear-gradient(to bottom, rgba(0,0,0,0.55), rgba(0,0,0,0.15) 75%, rgba(0,0,0,0))" }} />
      {bloco.linhas.map((l, i) => {
        const pr = lin(t, l.t - 0.05, l.t + 0.11, 0, 1);
        const top = y;
        y += l.tam * 1.02;
        return (
          <div key={i} style={{ position: "absolute", left: 72, top, fontFamily: "Anton", fontSize: l.tam, lineHeight: 1, color: l.cor ?? "#fff", opacity: pr, transform: `translateY(${(1 - pr) * 24}px)`, textShadow: "0 4px 24px rgba(0,0,0,0.6)" }}>
            {l.txt}
          </div>
        );
      })}
    </>
  );
};

const SFX = { impacto: pdxImpacto, swish: pdxSwish, obturador: pdxObturador, riser: pdxRiser } as const;

export const VenezaReel: React.FC<PropsVeneza> = (p) => {
  fontes();
  const t = useT();
  const { fps } = useVideoConfig();
  const cena = p.cenas.find((c) => t >= c.ini && t < c.fim) ?? p.cenas[p.cenas.length - 1];
  const diegoCheio = cena?.tipo === "diego";
  const apoioCheio = !!cena?.cheia && cena.tipo !== "diego";
  const zoomDiego = diegoCheio ? lin(t, cena.ini, cena.fim, (cena.zoom ?? [1, 1.05])[0], (cena.zoom ?? [1, 1.05])[1], Easing.linear) : 1;
  const noCta = t >= p.cta.ini;
  const legY = noCta ? 1330 : diegoCheio || apoioCheio ? 1320 : COSTURA;
  const noGancho = p.gancho.some((b) => t >= b.linhas[0].t - 0.05 && t < b.fim);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(2 * fps)}>
          <Audio src={SFX[s.som]} volume={Math.pow(10, s.db / 20)} />
        </Sequence>
      ))}
      {!apoioCheio && <Diego cheio={diegoCheio} zoom={zoomDiego} />}
      {cena && cena.tipo !== "diego" && (cena.tipo === "graf" ? (
        <Grafismo c={cena} t={t} />
      ) : (
        // o clipe começa do início em cada cena (Sequence), não na posição absoluta da linha do tempo
        <Sequence key={cena.ini} from={Math.round(cena.ini * fps)} durationInFrames={Math.max(1, Math.round((cena.fim - cena.ini) * fps))} layout="none">
          <Apoio c={cena} t={t} />
        </Sequence>
      ))}
      {!diegoCheio && !apoioCheio && <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: 1080, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      <Gancho p={p} t={t} />
      {!noGancho && <Legenda p={p} t={t} y={legY} />}
      {noCta && (
        <>
          <Placa rotulo="DICAS DE VIAGEM TODA SEMANA" destino="ME SEGUE" entrada={p.cta.ini * 1000} y={1010} />
          <Som nome="clack" em={p.cta.ini * 1000} relDb={-6} refLufs={-14} />
        </>
      )}
      {/* grão 6% */}
      <AbsoluteFill style={{ opacity: 0.06, mixBlendMode: "overlay", backgroundImage: "radial-gradient(rgba(255,255,255,0.9) 1px, transparent 1px)", backgroundSize: "3px 3px" }} />
    </AbsoluteFill>
  );
};
