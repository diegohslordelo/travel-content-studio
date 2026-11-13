/**
 * Reel em tela dividida · "Veneza não te quer lá" · REV2 (reels/veneza-bate-volta/rev2).
 * Linguagem do formato (docs/FORMATOS_REELS.md): Anton/Inter, destaque âmbar; DS V2 só no CTA (placa + clack).
 * Legenda karaokê (pedido do Diego, 12/11/2026): a palavra dita fica âmbar; as outras, brancas.
 *
 * Diferenças da REV1 (pedidos do Diego, 13/11/2026):
 * - toda troca de imagem cai no mesmo quadro de um corte da gravação ou a ≥ 0,5 s dele (sem "piscadas");
 * - cada clipe começa do início da sua cena (Sequence) e cobre a cena até o último quadro;
 * - grafismos novos, sem barras decorativas; cada imagem mostra o que está sendo dito;
 * - Diego em tela cheia de "E eu fiquei" até "não faça isso" e no CTA (sem tela dividida);
 * - corte de zoom quando há corte da gravação dentro de uma cena com o Diego em tela cheia.
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
export type Cena2 = {
  ini: number;
  fim: number;
  tipo: "video" | "foto" | "diego" | "graf";
  src?: string;
  /** segundo clipe que entra em dissolve (dia → noite) */
  src2?: string;
  tx?: number;
  graf?: string;
  dados?: Record<string, number | string>;
  escuro?: number;
  zoom?: [number, number];
  rotulo?: { txt: string; t: number };
  /** enquadramento vertical do clipe na área de cima (0 = topo, 0,5 = centro, 1 = base) */
  foco?: number;
};
type Sfx = { t: number; som: "impacto" | "swish" | "obturador" | "riser"; db: number };
export type PropsVeneza2 = {
  dur: number;
  palavras: Palavra[];
  cenas: Cena2[];
  grupos: number[][];
  gancho: { linhas: { txt: string; t: number; tam: number; cor?: string }[]; fim: number }[];
  sfx: Sfx[];
  cta: { ini: number };
};

export const propsVeneza2Vazias: PropsVeneza2 = { dur: 1, palavras: [], cenas: [], grupos: [], gancho: [], sfx: [], cta: { ini: 0 } };

export const metadadosVeneza2: CalculateMetadataFunction<PropsVeneza2> = ({ props }) => ({
  durationInFrames: Math.ceil(props.dur * 30),
});

const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lin = (t: number, a: number, b: number, v0: number, v1: number, e: (x: number) => number = ease) =>
  interpolate(t, [a, b], [v0, v1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const entra = (t: number, t0: number, d = 0.25) => lin(t, t0, t0 + d, 0, 1);

/* ---------- camadas de vídeo ---------- */

/** Vídeo vertical 1080×1920 cobrindo uma área W×H (centralizado). */
const VideoCobre: React.FC<{ src: string; W: number; H: number; zoom?: number; focoY?: number }> = ({ src, W, H, zoom = 1, focoY = 0.5 }) => {
  const k = Math.max(W / 1080, H / 1920) * zoom;
  const w = 1080 * k;
  const h = 1920 * k;
  // focoY: 0 = topo do quadro vertical, 0,5 = centro, 1 = base (onde está a multidão nos planos de praça)
  return (
    <div style={{ position: "absolute", left: (W - w) / 2, top: (H - h) * focoY, width: w, height: h }}>
      <Video src={staticFile(src)} muted style={{ width: w, height: h }} />
    </div>
  );
};

const FotoCobre: React.FC<{ src: string; W: number; H: number; zoom?: number; foco?: string }> = ({ src, W, H, zoom = 1, foco = "50% 50%" }) => (
  <div style={{ position: "absolute", inset: 0, width: W, height: H, overflow: "hidden" }}>
    <Img src={staticFile(src)} style={{ width: W, height: H, objectFit: "cover", objectPosition: foco, transform: `scale(${zoom})`, transformOrigin: foco }} />
  </div>
);

const Diego: React.FC<{ cheio: boolean; zoom: number }> = ({ cheio, zoom }) => (
  <AbsoluteFill style={{ top: cheio ? 0 : COSTURA, overflow: "hidden" }}>
    {/* dividida: rosto (≈ y 610 no quadro) a 42% da metade de baixo */}
    <div style={{ position: "absolute", left: 0, top: cheio ? 0 : 700 - COSTURA, width: 1080, height: 1920, transform: `scale(${zoom})`, transformOrigin: "50% 32%" }}>
      <Video src={staticFile("diego.mp4")} muted style={{ width: 1080, height: 1920 }} />
    </div>
  </AbsoluteFill>
);

/* ---------- elementos de grafismo ---------- */

const Txt: React.FC<{ txt: string; t: number; t0: number; tam: number; y: number; cor?: string; fonte?: "Anton" | "Inter"; x?: number; alinhar?: "center" | "left" }> = ({
  txt, t, t0, tam, y, cor, fonte = "Anton", x, alinhar = "center",
}) => {
  const p = entra(t, t0, 0.22);
  return (
    <div
      style={{
        position: "absolute", left: x ?? 0, right: x === undefined ? 0 : undefined, top: y, textAlign: alinhar,
        fontFamily: fonte, fontWeight: fonte === "Inter" ? 800 : 400, fontSize: tam, lineHeight: 1, color: cor ?? TRACO,
        letterSpacing: fonte === "Inter" ? 3 : 0, opacity: p, transform: `translateY(${(1 - p) * 30}px)`, textShadow: "0 4px 24px rgba(0,0,0,0.55)",
      }}
    >
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

const Calendario: React.FC<{ s?: number; num?: string }> = ({ s = 1, num }) => (
  <svg width={160 * s} height={160 * s} viewBox="0 0 160 160">
    <rect x={10} y={24} width={140} height={126} rx={18} fill={TRACO} />
    <rect x={10} y={24} width={140} height={38} rx={18} fill={AMBAR} />
    <rect x={10} y={46} width={140} height={16} fill={AMBAR} />
    <rect x={42} y={10} width={12} height={30} rx={6} fill={FUNDO} />
    <rect x={106} y={10} width={12} height={30} rx={6} fill={FUNDO} />
    {num ? (
      <text x={80} y={132} textAnchor="middle" fontFamily="Anton" fontSize={70} fill={FUNDO}>{num}</text>
    ) : (
      [0, 1, 2].map((r) => [0, 1, 2, 3].map((c) => <rect key={`${r}${c}`} x={28 + c * 28} y={76 + r * 22} width={18} height={14} rx={3} fill={FUNDO} opacity={0.75} />))
    )}
  </svg>
);

const Relogio: React.FC<{ s?: number; t: number }> = ({ s = 1, t }) => (
  <svg width={160 * s} height={160 * s} viewBox="0 0 160 160">
    <circle cx={80} cy={84} r={64} fill={TRACO} />
    <circle cx={80} cy={84} r={64} fill="none" stroke={AMBAR} strokeWidth={10} />
    <line x1={80} y1={84} x2={80} y2={44} stroke={FUNDO} strokeWidth={9} strokeLinecap="round" transform={`rotate(${t * 240} 80 84)`} />
    <line x1={80} y1={84} x2={110} y2={84} stroke={FUNDO} strokeWidth={9} strokeLinecap="round" transform={`rotate(${t * 20} 80 84)`} />
    <circle cx={80} cy={84} r={7} fill={FUNDO} />
  </svg>
);

const Sol: React.FC = () => (
  <svg width={150} height={150} viewBox="0 0 110 110">
    <circle cx={55} cy={55} r={24} fill={AMBAR} />
    {Array.from({ length: 8 }, (_, i) => (
      <line key={i} x1={55} y1={14} x2={55} y2={24} stroke={AMBAR} strokeWidth={8} strokeLinecap="round" transform={`rotate(${i * 45} 55 55)`} />
    ))}
  </svg>
);

const Lua: React.FC<{ riscada?: number }> = ({ riscada = 0 }) => (
  <svg width={150} height={150} viewBox="0 0 110 110">
    <path d="M 70 18 A 38 38 0 1 0 92 70 A 30 30 0 1 1 70 18 Z" fill={TRACO} />
    <line x1={16} y1={16} x2={16 + 78 * riscada} y2={16 + 78 * riscada} stroke="#ff5a4a" strokeWidth={10} strokeLinecap="round" />
  </svg>
);

/* ---------- grafismos (área de cima 1080×900) ---------- */

const H = COSTURA;
const BASE: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: H, background: FUNDO, overflow: "hidden" };

const Grafismo: React.FC<{ c: Cena2; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const at = (k: string) => Number(d[k] ?? c.ini);
  const g = c.graf;

  if (g === "milhoes") {
    // praça lotada + contador 0 → 30 milhões no tempo da fala
    const p = lin(t, at("t0"), at("t1"), 0, 1, Easing.out(Easing.cubic));
    return (
      <div style={BASE}>
        <VideoCobre src={c.src!} W={1080} H={H} zoom={lin(t, c.ini, c.fim, 1.0, 1.06, Easing.linear)} focoY={c.foco ?? 0.5} />
        <AbsoluteFill style={{ height: H, background: "linear-gradient(to bottom, rgba(0,0,0,0.25), rgba(0,0,0,0.7))" }} />
        <Txt txt={`${Math.round(30 * p)} MILHÕES`} t={t} t0={at("t0")} tam={190} y={H / 2 - 150} cor="#fff" />
        <Txt txt="DE PESSOAS NO ANO" t={t} t0={at("t0") + 0.3} tam={46} y={H / 2 + 70} fonte="Inter" cor="#fff" />
      </div>
    );
  }

  if (g === "tres4") {
    // 3 de 4 bonecos acendem em "três em cada quatro"; o print da Fortune sobe em "desses visitantes"
    const t3 = at("t3");
    const tp = at("tp");
    const pc = entra(t, tp, 0.35);
    const pulso = at("tb") ? 0.5 + 0.5 * Math.sin(Math.max(0, t - at("tb")) * 9) * lin(t, at("tb"), at("tb") + 1.2, 1, 0) : 0;
    return (
      <div style={BASE}>
        <svg width={1080} height={300} style={{ position: "absolute", left: 0, top: 30 }}>
          {[0, 1, 2, 3].map((i) => {
            const pi = entra(t, c.ini + i * 0.1, 0.25);
            const amb = t >= t3 + i * 0.12 && i < 3;
            return <Pessoa key={i} x={300 + i * 160} y={170} cor={amb ? AMBAR : "#5A544B"} p={pi} s={1.35} />;
          })}
        </svg>
        <Txt txt="3 EM CADA 4" t={t} t0={t3} tam={110} y={272} cor={AMBAR} />
        <div style={{ position: "absolute", left: 50, top: 410, width: 980, background: "#fff", borderRadius: 18, boxShadow: "0 24px 60px rgba(0,0,0,0.6)", padding: "26px 30px 30px", opacity: pc, transform: `translateY(${(1 - pc) * 120}px)` }}>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 26, letterSpacing: 3, color: "#111", marginBottom: 12 }}>FORTUNE · 03/01/2024</div>
          <Img src={staticFile("fortune_titulo.png")} style={{ width: 920, display: "block" }} />
          <div style={{ height: 2, background: "#ddd", margin: "14px 0" }} />
          <div style={{ position: "relative" }}>
            <Img src={staticFile("fortune_paragrafo.png")} style={{ width: 920, display: "block" }} />
            <div style={{ position: "absolute", inset: -6, borderRadius: 10, boxShadow: `0 0 0 ${4 + 6 * pulso}px rgba(224,174,92,${0.5 * pulso})` }} />
          </div>
        </div>
      </div>
    );
  }

  if (g === "pedagio") {
    // bilhete de entrada com QR; em "pra quem vai e não dorme": sol (vai) e lua riscada (não dorme)
    const p = entra(t, c.ini, 0.4);
    const tv = at("tvai");
    const tn = at("tdorme");
    const qr = Array.from({ length: 81 }, (_, i) => ((i * 7919) % 13) % 3 !== 0 || i % 10 === 0);
    return (
      <div style={BASE}>
        <div style={{ position: "absolute", left: 210, top: 70, width: 660, height: 420, background: TRACO, borderRadius: 28, boxShadow: "0 30px 70px rgba(0,0,0,0.6)", transform: `translateY(${(1 - p) * -520}px) rotate(${(1 - p) * 6 - 2}deg)` }}>
          <div style={{ position: "absolute", left: 44, top: 40, fontFamily: "Anton", fontSize: 120, lineHeight: 1, color: FUNDO }}>PEDÁGIO</div>
          <div style={{ position: "absolute", left: 48, top: 190, fontFamily: "Inter", fontWeight: 800, fontSize: 34, letterSpacing: 4, color: "#7a6a52" }}>VENEZA</div>
          <div style={{ position: "absolute", right: 44, top: 170, width: 200, height: 200, display: "grid", gridTemplateColumns: "repeat(9,1fr)", gap: 3 }}>
            {qr.map((on, i) => <div key={i} style={{ background: on ? FUNDO : "transparent" }} />)}
          </div>
          <div style={{ position: "absolute", left: 0, top: 300, width: 400, borderTop: `5px dashed ${FUNDO}`, opacity: 0.3, marginLeft: 44 }} />
        </div>
        <div style={{ position: "absolute", left: 110, top: 530, width: 400, textAlign: "center", opacity: entra(t, tv), transform: `translateY(${(1 - entra(t, tv)) * 30}px)` }}>
          <Sol />
          <div style={{ fontFamily: "Anton", fontSize: 92, color: "#fff", marginTop: 4 }}>VAI</div>
        </div>
        <div style={{ position: "absolute", left: 570, top: 530, width: 420, textAlign: "center", opacity: entra(t, tn), transform: `translateY(${(1 - entra(t, tn)) * 30}px)` }}>
          <Lua riscada={lin(t, tn + 0.15, tn + 0.45, 0, 1)} />
          <div style={{ fontFamily: "Anton", fontSize: 92, color: "#fff", marginTop: 4 }}>NÃO DORME</div>
        </div>
      </div>
    );
  }

  if (g === "precos") {
    const t5 = at("t5");
    const t10 = at("t10");
    const tnp = at("tnp");
    const apaga = lin(t, tnp, tnp + 0.3, 1, 0.35);
    const card = (x: number, t0: number, icone: React.ReactNode, preco: string, rot: string) => {
      const p = entra(t, t0, 0.3);
      return (
        <div style={{ position: "absolute", left: x, top: 90, width: 420, height: 560, borderRadius: 30, background: "#221F1A", border: `4px solid ${AMBAR}`, opacity: p * apaga, transform: `translateY(${(1 - p) * 80}px) scale(${0.92 + 0.08 * p})`, textAlign: "center" }}>
          <div style={{ marginTop: 40 }}>{icone}</div>
          <div style={{ fontFamily: "Anton", fontSize: 190, lineHeight: 1.05, color: AMBAR, marginTop: 10 }}>{preco}</div>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 40, letterSpacing: 4, color: TRACO, marginTop: 10 }}>{rot}</div>
        </div>
      );
    };
    return (
      <div style={BASE}>
        {card(90, t5, <Calendario />, "5 €", "PROGRAMADO")}
        {card(570, t10, <Relogio t={t - t10} />, "10 €", "NA HORA")}
        <Txt txt="E SE NÃO PAGAR?" t={t} t0={tnp} tam={110} y={710} cor="#fff" />
      </div>
    );
  }

  if (g === "multa") {
    const p = lin(t, c.ini, c.ini + 0.18, 0, 1, Easing.out(Easing.back(2)));
    const dt = t - c.ini;
    const tremor = dt < 0.35 ? Math.sin(dt * 90) * 12 * (1 - dt / 0.35) : 0;
    return (
      <div style={{ ...BASE, background: "#2a0f0c" }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 200, textAlign: "center", transform: `translateX(${tremor}px) rotate(-6deg) scale(${2 - p})`, opacity: p }}>
          <span style={{ fontFamily: "Anton", fontSize: 260, color: "#ff5a4a", border: "16px solid #ff5a4a", borderRadius: 34, padding: "0 56px" }}>MULTA</span>
        </div>
        <Txt txt="PRA DOER NO BOLSO" t={t} t0={at("tbolso")} tam={70} y={640} cor="#fff" />
      </div>
    );
  }

  if (g === "mapa") return <Mapa c={c} t={t} />;

  if (g === "hospedagem") {
    // Verona (−25%) × Veneza (cidade dos canais), lado a lado
    const pv = entra(t, c.ini, 0.35);
    const pb = lin(t, at("t25"), at("t25") + 0.9, 0, 1, Easing.out(Easing.cubic));
    const pz = entra(t, at("tcanais"), 0.35);
    const cartao = (x: number, p: number, conteudo: React.ReactNode, nome: string) => (
      <div style={{ position: "absolute", left: x, top: 36, width: 470, height: 600, borderRadius: 26, overflow: "hidden", boxShadow: "0 24px 60px rgba(0,0,0,0.6)", opacity: p, transform: `translateY(${(1 - p) * 90}px)` }}>
        {conteudo}
        <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75))" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 28, textAlign: "center", fontFamily: "Anton", fontSize: 84, color: "#fff" }}>{nome}</div>
      </div>
    );
    return (
      <div style={BASE}>
        {cartao(lin(t, at("tcanais") - 0.1, at("tcanais") + 0.3, 305, 50), pv, <FotoCobre src="ponte_pietra.jpg" W={470} H={600} zoom={lin(t, c.ini, c.fim, 1.05, 1.15, Easing.linear)} foco="40% 50%" />, "VERONA")}
        {cartao(560, pz, (
          <Sequence from={Math.round((at("tcanais") - c.ini) * 30)} layout="none">
            <VideoCobre src="canais.mp4" W={470} H={600} />
          </Sequence>
        ), "VENEZA")}
        <div style={{ position: "absolute", left: lin(t, at("tcanais") - 0.1, at("tcanais") + 0.3, 305, 50), top: 650, width: 470, textAlign: "center", opacity: entra(t, at("t25")) }}>
          <span style={{ fontFamily: "Anton", fontSize: 104, color: AMBAR }}>ATÉ {Math.round(25 * pb)}%</span>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 32, letterSpacing: 3, color: TRACO, marginTop: -4 }}>MAIS BARATO</div>
        </div>
      </div>
    );
  }

  if (g === "reserva") {
    const t4 = at("t4");
    const t5 = at("t5");
    const tl = at("tlink");
    const sai = lin(t, tl - 0.05, tl + 0.25, 1, 0);
    const pl = entra(t, tl, 0.35);
    return (
      <div style={BASE}>
        <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, opacity: sai, transform: `scale(${0.92 + 0.08 * sai})` }}>
          <div style={{ position: "absolute", left: lin(t, t5 - 0.45, t5 - 0.1, 360, 110), top: 170, textAlign: "center", width: 360, opacity: entra(t, c.ini), transform: `scale(${0.9 + 0.1 * entra(t, c.ini)})` }}>
            <Calendario s={2} num={t >= t4 ? "4" : ""} />
            <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 40, letterSpacing: 3, color: TRACO, marginTop: 10, opacity: entra(t, t4) }}>DIAS ANTES</div>
          </div>
          <div style={{ position: "absolute", left: 480, top: 300, fontFamily: "Anton", fontSize: 120, color: TRACO, opacity: entra(t, t5 - 0.2) }}>→</div>
          <div style={{ position: "absolute", left: 600, top: 220, width: 380, textAlign: "center", fontFamily: "Anton", fontSize: 230, color: AMBAR, opacity: entra(t, t5), transform: `scale(${lin(t, t5, t5 + 0.25, 1.35, 1)})` }}>5 €</div>
        </div>
        <div style={{ position: "absolute", left: 70, top: 190, width: 940, opacity: pl, transform: `translateY(${(1 - pl) * 80}px)` }}>
          <Img src={staticFile("cda_cabecalho.jpg")} style={{ width: 940, borderRadius: 16, boxShadow: "0 20px 50px rgba(0,0,0,0.6)", display: "block" }} />
          <div style={{ textAlign: "center", fontFamily: "Anton", fontSize: 104, color: AMBAR, marginTop: 40 }}>LINK NA LEGENDA ↓</div>
        </div>
      </div>
    );
  }
  return <div style={BASE} />;
};

/** Mapa Verona → Veneza (posições por latitude/longitude reais; costa, laguna e Lago de Garda simplificados). */
const Mapa: React.FC<{ c: Cena2; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const X = (lon: number) => 80 + (lon - 10.6) * 435;
  const Y = (lat: number) => 430 - (lat - 45.44) * 620;
  const P = (pts: [number, number][]) => pts.map(([lo, la], i) => `${i ? "L" : "M"} ${X(lo).toFixed(1)} ${Y(la).toFixed(1)}`).join(" ");
  const garda = P([[10.70, 45.88], [10.84, 45.86], [10.87, 45.70], [10.72, 45.56], [10.71, 45.44], [10.62, 45.44], [10.52, 45.55], [10.55, 45.68], [10.64, 45.74]]) + " Z";
  const mar = P([[12.24, 44.6], [12.28, 45.10], [12.27, 45.20], [12.33, 45.33], [12.40, 45.42], [12.55, 45.50], [12.70, 45.53], [12.95, 45.60], [12.95, 44.6]]) + " Z";
  const laguna = P([[12.22, 45.24], [12.25, 45.40], [12.30, 45.47], [12.45, 45.55], [12.55, 45.52], [12.40, 45.42], [12.33, 45.33], [12.27, 45.20]]) + " Z";
  const rota: [number, number][] = [[10.994, 45.438], [11.546, 45.546], [11.877, 45.406], [12.232, 45.482], [12.32, 45.441]];
  const pts = rota.map(([lo, la]) => ({ x: X(lo), y: Y(la) }));
  const segs = pts.slice(1).map((q, i) => Math.hypot(q.x - pts[i].x, q.y - pts[i].y));
  const total = segs.reduce((a, b) => a + b, 0);
  const ponto = (f: number) => {
    let r = f * total;
    for (let i = 0; i < segs.length; i++) {
      if (r <= segs[i]) { const k = r / segs[i]; return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * k, y: pts[i].y + (pts[i + 1].y - pts[i].y) * k }; }
      r -= segs[i];
    }
    return pts[pts.length - 1];
  };
  const tl0 = c.ini + 0.3;
  const tl1 = Number(d.thora ?? c.ini + 1.5);
  const pLinha = lin(t, tl0, tl1, 0, 1, Easing.inOut(Easing.cubic));
  const tb = Number(d.tbate ?? c.fim);
  // bate-volta: trem vai (0,55 s) e volta (0,55 s)
  const ida = lin(t, tb, tb + 0.55, 0, 1, Easing.inOut(Easing.cubic));
  const volta = lin(t, tb + 0.6, tb + 1.15, 0, 1, Easing.inOut(Easing.cubic));
  const f = t < tb ? pLinha : ida - volta;
  const trem = ponto(Math.max(0, Math.min(1, f)));
  const pin = (q: { x: number; y: number }, nome: string, t0: number, dx: number) => {
    const s = lin(t, t0, t0 + 0.3, 0, 1, Easing.out(Easing.back(2)));
    return (
      <g transform={`translate(${q.x},${q.y})`}>
        <circle r={24 * s} fill={AMBAR} />
        <circle r={10 * s} fill={FUNDO} />
        <text x={dx} y={-48} textAnchor="middle" fontFamily="Anton" fontSize={66} fill="#fff" opacity={s}>{nome}</text>
      </g>
    );
  };
  const pHora = entra(t, tl1 - 0.15);
  const pBate = entra(t, tb);
  return (
    <div style={{ ...BASE, background: "#1d2a22" }}>
      <svg width={1080} height={H} style={{ position: "absolute", inset: 0 }}>
        <path d={mar} fill="#1f3f57" />
        <path d={laguna} fill="#2b5874" />
        <path d={garda} fill="#1f3f57" />
        <path d={P(rota)} stroke="#3d4a42" strokeWidth={12} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={P(rota)} stroke={AMBAR} strokeWidth={12} fill="none" strokeDasharray={total} strokeDashoffset={total * (1 - pLinha)} strokeLinecap="round" strokeLinejoin="round" />
        {pts.slice(1, -1).map((q, i) => <circle key={i} cx={q.x} cy={q.y} r={9} fill={pLinha > (i + 1) / (pts.length - 1) ? AMBAR : "#3d4a42"} />)}
        {pin(pts[0], "VERONA", c.ini, 0)}
        {pin(pts[pts.length - 1], "VENEZA", tl1 - 0.1, -40)}
        <g transform={`translate(${trem.x},${trem.y})`} opacity={(t > tl0 && t < tl1) || (t >= tb && t < tb + 1.2) ? 1 : 0}>
          <rect x={-34} y={-22} width={68} height={44} rx={12} fill={TRACO} stroke={FUNDO} strokeWidth={4} />
          <rect x={-24} y={-12} width={20} height={14} rx={3} fill={FUNDO} />
          <rect x={4} y={-12} width={20} height={14} rx={3} fill={FUNDO} />
        </g>
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 600, textAlign: "center", opacity: pHora * (1 - pBate) }}>
        <div style={{ fontFamily: "Anton", fontSize: 120, color: "#fff" }}>1H E POUQUINHO</div>
        <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 40, letterSpacing: 4, color: TRACO }}>DE TREM</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 620, textAlign: "center", opacity: pBate, transform: `scale(${0.9 + 0.1 * pBate})` }}>
        <div style={{ fontFamily: "Anton", fontSize: 140, color: AMBAR }}>⇄ BATE-VOLTA</div>
      </div>
    </div>
  );
};

/* ---------- apoio (vídeo/foto) ---------- */

const Apoio: React.FC<{ c: Cena2; t: number }> = ({ c, t }) => {
  const z = c.zoom ?? [1.0, 1.06];
  const k = lin(t, c.ini, c.fim, z[0], z[1], Easing.linear);
  const px = c.tx !== undefined ? lin(t, c.tx - 0.25, c.tx + 0.25, 0, 1, Easing.inOut(Easing.quad)) : 0;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, overflow: "hidden", background: "#000" }}>
      {c.tipo === "video" ? <VideoCobre src={c.src!} W={1080} H={H} zoom={k} focoY={c.foco ?? 0.5} /> : <FotoCobre src={c.src!} W={1080} H={H} zoom={k} />}
      {c.src2 && c.tx !== undefined && (
        <Sequence from={Math.round((c.tx - 0.25 - c.ini) * 30)} layout="none">
          <AbsoluteFill style={{ height: H, opacity: px }}>
            <VideoCobre src={c.src2} W={1080} H={H} zoom={lin(t, c.tx, c.fim, 1.04, 1.0, Easing.linear)} />
          </AbsoluteFill>
        </Sequence>
      )}
      {c.escuro ? <AbsoluteFill style={{ height: H, background: `rgba(0,0,0,${c.escuro})` }} /> : null}
      {c.rotulo ? (
        <>
          <AbsoluteFill style={{ height: H, background: "linear-gradient(to bottom, rgba(0,0,0,0) 45%, rgba(0,0,0,0.6) 100%)", opacity: entra(t, c.rotulo.t) }} />
          <Txt txt={c.rotulo.txt} t={t} t0={c.rotulo.t} tam={130} y={H - 210} cor="#fff" />
        </>
      ) : null}
    </div>
  );
};

/* ---------- legenda karaokê ---------- */

const Legenda: React.FC<{ p: PropsVeneza2; t: number; y: number }> = ({ p, t, y }) => {
  const idx = p.grupos.findIndex((gr, k) => {
    const a = p.palavras[gr[0]].s - 0.05;
    const prox = p.grupos[k + 1];
    const fimG = p.palavras[gr[gr.length - 1]].e + 0.25;
    const b = prox ? Math.min(p.palavras[prox[0]].s - 0.05, fimG) : fimG;
    return t >= a && t < b;
  });
  if (idx < 0) return null;
  const g = p.grupos[idx];
  const t0 = p.palavras[g[0]].s - 0.05;
  const k = lin(t, t0, t0 + 0.12, 0.94, 1);
  const o = lin(t, t0, t0 + 0.12, 0, 1);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y - 40, textAlign: "center", opacity: o, transform: `scale(${k})` }}>
      <span style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
        {g.map((i, j) => {
          const w = p.palavras[i];
          const prox = j < g.length - 1 ? p.palavras[g[j + 1]].s - 0.03 : w.e + 0.15;
          const ativa = t >= w.s - 0.03 && t < Math.max(w.e, prox);
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

const Gancho: React.FC<{ p: PropsVeneza2; t: number }> = ({ p, t }) => {
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

export const VenezaReel2: React.FC<PropsVeneza2> = (p) => {
  fontes();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  // cena pelo quadro (evita arredondamento entre cena e Sequence)
  const cena = p.cenas.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cenas[p.cenas.length - 1];
  const diegoCheio = cena.tipo === "diego";
  const zoomDiego = diegoCheio ? lin(t, cena.ini, cena.fim, (cena.zoom ?? [1, 1.04])[0], (cena.zoom ?? [1, 1.04])[1], Easing.linear) : 1;
  const legY = diegoCheio ? 1320 : COSTURA;
  const noGancho = p.gancho.some((b) => t >= b.linhas[0].t - 0.05 && t < b.fim);
  const fromC = Math.round(cena.ini * fps);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(2 * fps)}>
          <Audio src={SFX[s.som]} volume={Math.pow(10, s.db / 20)} />
        </Sequence>
      ))}
      <Diego cheio={diegoCheio} zoom={zoomDiego} />
      {!diegoCheio && (
        <Sequence key={cena.ini} from={fromC} durationInFrames={Math.max(1, Math.round(cena.fim * fps) - fromC + 2)} layout="none">
          {cena.tipo === "graf" ? <Grafismo c={cena} t={t} /> : <Apoio c={cena} t={t} />}
          <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: 1080, height: 6, background: "rgba(0,0,0,0.55)" }} />
        </Sequence>
      )}
      <Gancho p={p} t={t} />
      {!noGancho && <Legenda p={p} t={t} y={legY} />}
      <Placa rotulo="DICAS DE VIAGEM TODA SEMANA" destino="ME SEGUE" entrada={p.cta.ini * 1000} y={1010} />
      <Som nome="clack" em={p.cta.ini * 1000} relDb={-6} refLufs={-14} />
    </AbsoluteFill>
  );
};
