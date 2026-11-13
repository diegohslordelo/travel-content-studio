/**
 * Reel em tela dividida · "Veneza não te quer lá" · REV4 (reels/veneza-bate-volta/rev4).
 * Parte da REV3 (VenezaReel3, que não muda). Pedidos do Diego (13/11/2026):
 * - legenda em caixa normal (maiúscula só no começo da frase e nos nomes), karaokê mantido;
 * - nada aparece antes de ser dito: cada palavra da legenda, do gancho e dos rótulos entra no início dela
 *   (as palavras que ainda não foram ditas ficam invisíveis no lugar, para o texto não "andar");
 * - nada no rosto: na tela dividida o rosto fica a 42% da metade de baixo (deslocamento medido por trecho);
 *   em tela cheia a legenda vai na posição calculada pelo rosto de cada grupo (props.gy); a placa da CTA
 *   vai abaixo do queixo e a legenda sai quando ela entra;
 * - nenhum filtro ou cor no vídeo dele: só o preto e branco puro (grayscale) nos 3 takes que ele pediu.
 * Linguagem do formato (FORMATOS_REELS): Anton/Inter, paleta "Veneza ensolarada" da REV3 (só deste Reel);
 * DS V2 só no CTA (placa + clack).
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

/* Paleta "Veneza ensolarada" (REV3; só deste Reel, não é paleta da marca) */
const AMBAR = "#FFD23F";
const FUNDO = "#12355B";
const TRACO = "#FFFFFF";
const CORAL = "#FF5E5B";
const AZUL = "#1F8FD6";
const AMBAR_CTA = "#E0AE5C"; // CTA igual à REV2/REV3
const BG = {
  base: "linear-gradient(160deg, #3CC8E0 0%, #1F8FD6 100%)",
  tres4: "linear-gradient(160deg, #3CC8E0 0%, #1F8FD6 100%)",
  pedagio: "linear-gradient(160deg, #FFA062 0%, #FF5E7E 100%)",
  precos: "linear-gradient(160deg, #FFE27A 0%, #FFB238 100%)",
  multa: "linear-gradient(160deg, #FF6B5E 0%, #E8344A 100%)",
  dorme: "linear-gradient(160deg, #5B7CFA 0%, #2E44C2 100%)",
  hospedagem: "linear-gradient(160deg, #5FD0F5 0%, #2A9DF4 100%)",
  reserva: "linear-gradient(160deg, #34D1BF 0%, #149E94 100%)",
};
const SOMBRA = "0 3px 0 rgba(0,0,0,0.16), 0 6px 20px rgba(0,0,0,0.22)";
const COSTURA = 900;
const H = COSTURA;

let fontesOk = false;
const fontes = () => {
  if (fontesOk) return;
  fontesOk = true;
  loadFont({ family: "Anton", url: staticFile("fontes/anton-latin-400-normal.woff2"), weight: "400" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-800-normal.woff2"), weight: "800" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-600-normal.woff2"), weight: "600" });
};

type Palavra = { w: string; s: number; e: number };
type Rot = { txt: string; t: number }[];
export type Cena4 = {
  ini: number;
  fim: number;
  tipo: "video" | "foto" | "diego" | "graf";
  src?: string;
  src2?: string;
  tx?: number;
  graf?: string;
  dados?: Record<string, number | string | Rot>;
  zoom?: [number, number];
  rotulo?: Rot;
  foco?: number;
};
type Corte = { ini: number; fim: number; take: string; pb: boolean; div_off: number };
type Sfx = { t: number; som: "impacto" | "swish" | "obturador" | "riser"; db: number };
export type PropsVeneza4 = {
  dur: number;
  palavras: Palavra[];
  cenas: Cena4[];
  grupos: number[][];
  gy: number[];
  gancho: { fim: number; linhas: { tam: number; cor?: string; palavras: Rot }[] };
  sfx: Sfx[];
  cortes: Corte[];
  cta: { ini: number; placa_y: number; leg_fim: number };
};

export const propsVeneza4Vazias: PropsVeneza4 = {
  dur: 1, palavras: [], cenas: [], grupos: [], gy: [], gancho: { fim: 0, linhas: [] }, sfx: [], cortes: [], cta: { ini: 0, placa_y: 1218, leg_fim: 0 },
};

export const metadadosVeneza4: CalculateMetadataFunction<PropsVeneza4> = ({ props }) => ({
  durationInFrames: Math.ceil(props.dur * 30 - 1e-6),
});

const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lin = (t: number, a: number, b: number, v0: number, v1: number, e: (x: number) => number = ease) =>
  interpolate(t, [a, b], [v0, v1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
/** Entra no instante t0 (nunca antes): 0 → 1 em d segundos. */
const entra = (t: number, t0: number, d = 0.2) => (t < t0 ? 0 : lin(t, t0, t0 + d, 0, 1));
/** Para o que abre uma cena (imagem, cartão sem texto falado): já visível no 1º quadro, só assenta. */
const abre = (t: number, t0: number) => 0.6 + 0.4 * lin(t, t0, t0 + 0.18, 0, 1);

/** Palavras que entram uma a uma, cada uma no início da sua fala; as futuras ficam invisíveis no lugar. */
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

/* ---------- camadas de vídeo ---------- */

const VideoCobre: React.FC<{ src: string; W: number; H: number; zoom?: number; focoY?: number }> = ({ src, W, H: Hh, zoom = 1, focoY = 0.5 }) => {
  const k = Math.max(W / 1080, Hh / 1920) * zoom;
  const w = 1080 * k;
  const h = 1920 * k;
  return (
    <div style={{ position: "absolute", left: (W - w) / 2, top: (Hh - h) * focoY, width: w, height: h }}>
      <Video src={staticFile(src)} muted style={{ width: w, height: h }} />
    </div>
  );
};

const FotoCobre: React.FC<{ src: string; W: number; H: number; zoom?: number; foco?: string }> = ({ src, W, H: Hh, zoom = 1, foco = "50% 50%" }) => (
  <div style={{ position: "absolute", inset: 0, width: W, height: Hh, overflow: "hidden" }}>
    <Img src={staticFile(src)} style={{ width: W, height: Hh, objectFit: "cover", objectPosition: foco, transform: `scale(${zoom})`, transformOrigin: foco }} />
  </div>
);

/** Gravação do Diego. Sem filtro nenhum; P&B puro só nos takes pedidos. Na tela dividida, rosto a 42% da metade de baixo. */
const Diego: React.FC<{ cheio: boolean; zoom: number; pb: boolean; divOff: number }> = ({ cheio, zoom, pb, divOff }) => (
  <AbsoluteFill style={{ top: cheio ? 0 : COSTURA, overflow: "hidden", filter: pb ? "grayscale(1)" : undefined }}>
    <div style={{ position: "absolute", left: 0, top: cheio ? 0 : divOff, width: 1080, height: 1920, transform: `scale(${zoom})`, transformOrigin: "50% 32%" }}>
      <Video src={staticFile("diego.mp4")} muted style={{ width: 1080, height: 1920 }} />
    </div>
  </AbsoluteFill>
);

/* ---------- elementos de grafismo ---------- */

const Pessoa: React.FC<{ x: number; y: number; cor: string; p: number; s?: number }> = ({ x, y, cor, p, s = 1 }) => (
  <g transform={`translate(${x},${y + (1 - p) * 30}) scale(${s})`} opacity={p}>
    <circle cx={0} cy={-62} r={26} fill={cor} />
    <path d="M -42 40 Q -42 -24 0 -26 Q 42 -24 42 40 Z" fill={cor} />
  </g>
);

const Calendario: React.FC<{ s?: number; num?: string }> = ({ s = 1, num }) => (
  <svg width={160 * s} height={160 * s} viewBox="0 0 160 160">
    <rect x={10} y={24} width={140} height={126} rx={18} fill={TRACO} />
    <rect x={10} y={24} width={140} height={38} rx={18} fill={CORAL} />
    <rect x={10} y={46} width={140} height={16} fill={CORAL} />
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
    <circle cx={80} cy={84} r={64} fill="none" stroke={CORAL} strokeWidth={10} />
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

const Lua: React.FC<{ riscada?: number; s?: number; cor?: string }> = ({ riscada = 0, s = 1, cor = TRACO }) => (
  <svg width={150 * s} height={150 * s} viewBox="0 0 110 110">
    <path d="M 70 18 A 38 38 0 1 0 92 70 A 30 30 0 1 1 70 18 Z" fill={cor} />
    <line x1={16} y1={16} x2={16 + 78 * riscada} y2={16 + 78 * riscada} stroke={CORAL} strokeWidth={12} strokeLinecap="round" opacity={riscada > 0 ? 1 : 0} />
  </svg>
);

/** Cama de hotel (desenho de traço, não foto). */
const Cama: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <svg width={340 * s} height={220 * s} viewBox="0 0 340 220">
    <rect x={20} y={30} width={26} height={170} rx={10} fill={TRACO} />
    <rect x={46} y={110} width={274} height={60} rx={16} fill={TRACO} />
    <rect x={60} y={78} width={86} height={42} rx={18} fill={AMBAR} />
    <rect x={150} y={92} width={170} height={34} rx={14} fill="#C9D6FF" />
    <rect x={46} y={168} width={20} height={36} rx={6} fill={TRACO} />
    <rect x={300} y={168} width={20} height={36} rx={6} fill={TRACO} />
  </svg>
);

/* ---------- grafismos (área de cima 1080×900) ---------- */

const BASE: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: H, background: BG.base, overflow: "hidden" };
const centro = (top: number, extra: React.CSSProperties = {}): React.CSSProperties => ({ position: "absolute", left: 0, right: 0, top, textAlign: "center", ...extra });
const ANTON = (tam: number, cor = TRACO, sombra = true): React.CSSProperties => ({ fontFamily: "Anton", fontSize: tam, lineHeight: 1, color: cor, textShadow: sombra ? SOMBRA : "none" });
const INTER = (tam: number, cor = TRACO, sombra = true): React.CSSProperties => ({ fontFamily: "Inter", fontWeight: 800, fontSize: tam, letterSpacing: 3, color: cor, textShadow: sombra ? SOMBRA : "none" });

const Grafismo: React.FC<{ c: Cena4; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const at = (k: string) => Number(d[k] ?? c.ini);
  const rt = (k: string) => (d[k] ?? []) as Rot;
  const g = c.graf;

  if (g === "milhoes") {
    const t30 = at("n30");
    const tm = at("milhoes");
    const p30 = t < t30 ? 0 : lin(t, t30, t30 + 0.22, 0, 1, Easing.out(Easing.back(1.6)));
    const pm = t < tm ? 0 : lin(t, tm, tm + 0.18, 0, 1);
    return (
      <div style={BASE}>
        <VideoCobre src={c.src!} W={1080} H={H} zoom={lin(t, c.ini, c.fim, 1.0, 1.06, Easing.linear)} focoY={c.foco ?? 0.5} />
        <AbsoluteFill style={{ height: H, background: "linear-gradient(to bottom, rgba(0,0,0,0.12), rgba(0,0,0,0.5))" }} />
        <Palavras itens={[{ txt: "QUASE", t: at("quase") }]} t={t} estilo={centro(H / 2 - 250, ANTON(90))} />
        <div style={centro(H / 2 - 150, { ...ANTON(190, AMBAR, false), textShadow: "0 5px 0 rgba(0,0,0,0.25), 0 8px 26px rgba(0,0,0,0.4)" })}>
          <span style={{ display: "inline-block", opacity: p30, transform: `scale(${0.8 + 0.2 * p30})` }}>30</span>
          <span style={{ display: "inline-block", opacity: pm, transform: `scale(${0.9 + 0.1 * pm})`, whiteSpace: "pre" }}> MILHÕES</span>
        </div>
        <Palavras itens={rt("rot")} t={t} estilo={centro(H / 2 + 70, INTER(46))} />
      </div>
    );
  }

  if (g === "tres4") {
    const t3 = at("t3");
    const tp = at("tp");
    const pc = entra(t, tp, 0.35);
    const tb = at("tb");
    const pulso = t >= tb ? 0.5 + 0.5 * Math.sin((t - tb) * 9) * lin(t, tb, tb + 1.2, 1, 0) : 0;
    return (
      <div style={{ ...BASE, background: BG.tres4 }}>
        <svg width={1080} height={300} style={{ position: "absolute", left: 0, top: 20 }}>
          {[0, 1, 2, 3].map((i) => {
            const amb = t >= t3 + i * 0.12 && i < 3;
            return <Pessoa key={i} x={300 + i * 160} y={170} cor={amb ? AMBAR : "rgba(255,255,255,0.45)"} p={abre(t, c.ini)} s={1.35} />;
          })}
        </svg>
        <Palavras itens={rt("rot")} t={t} estilo={centro(262, ANTON(110, AMBAR))} />
        {/* cartão termina em y ≈ 853: 10 px acima da legenda da costura (863) */}
        <div style={{ position: "absolute", left: 50, top: 392, width: 980, background: "#fff", borderRadius: 18, boxShadow: "0 18px 40px rgba(10,40,80,0.35)", padding: "18px 30px 20px", opacity: pc, transform: `translateY(${(1 - pc) * 120}px)` }}>
          <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 26, lineHeight: 1.2, letterSpacing: 3, color: "#111", marginBottom: 8 }}>FORTUNE · 03/01/2024</div>
          <Img src={staticFile("fortune_titulo.png")} style={{ width: 920, display: "block" }} />
          <div style={{ height: 2, background: "#ddd", margin: "10px 0" }} />
          <div style={{ position: "relative" }}>
            <Img src={staticFile("fortune_paragrafo.png")} style={{ width: 920, display: "block" }} />
            <div style={{ position: "absolute", inset: -6, borderRadius: 10, boxShadow: `0 0 0 ${4 + 6 * pulso}px rgba(255,210,63,${0.7 * pulso})` }} />
          </div>
        </div>
      </div>
    );
  }

  if (g === "pedagio") {
    const p = abre(t, c.ini);
    const tped = at("tped");
    const tv = at("tvai");
    const tn = at("tnao");
    const td = at("tdorme");
    const qr = Array.from({ length: 81 }, (_, i) => ((i * 7919) % 13) % 3 !== 0 || i % 10 === 0);
    return (
      <div style={{ ...BASE, background: BG.pedagio }}>
        <div style={{ position: "absolute", left: 210, top: 70, width: 660, height: 420, background: TRACO, borderRadius: 28, boxShadow: "0 24px 50px rgba(120,20,40,0.35)", transform: `translateY(${(1 - p) * -520}px) rotate(${(1 - p) * 6 - 2}deg)` }}>
          <div style={{ position: "absolute", left: 44, top: 40, fontFamily: "Anton", fontSize: 120, lineHeight: 1, color: FUNDO, opacity: entra(t, tped, 0.12), transform: `scale(${t < tped ? 1.4 : lin(t, tped, tped + 0.2, 1.4, 1, Easing.out(Easing.back(1.8)))})`, transformOrigin: "20% 50%" }}>PEDÁGIO</div>
          <div style={{ position: "absolute", right: 44, top: 170, width: 200, height: 200, display: "grid", gridTemplateColumns: "repeat(9,1fr)", gap: 3 }}>
            {qr.map((on, i) => <div key={i} style={{ background: on ? FUNDO : "transparent" }} />)}
          </div>
          <div style={{ position: "absolute", left: 0, top: 300, width: 400, borderTop: `5px dashed ${FUNDO}`, opacity: 0.3, marginLeft: 44 }} />
        </div>
        <div style={{ position: "absolute", left: 110, top: 530, width: 400, textAlign: "center", opacity: entra(t, tv), transform: `translateY(${(1 - entra(t, tv)) * 30}px)` }}>
          <Sol />
          <div style={{ ...ANTON(92), marginTop: 4 }}>VAI</div>
        </div>
        <div style={{ position: "absolute", left: 570, top: 530, width: 420, textAlign: "center", opacity: entra(t, tn), transform: `translateY(${(1 - entra(t, tn)) * 30}px)` }}>
          <Lua riscada={t < td ? 0 : lin(t, td, td + 0.3, 0, 1)} />
          <Palavras itens={[{ txt: "NÃO", t: tn }, { txt: "DORME", t: td }]} t={t} estilo={{ ...ANTON(92), marginTop: 4 }} />
        </div>
      </div>
    );
  }

  if (g === "precos") {
    const t5 = at("t5");
    const t10 = at("t10");
    const np = rt("np");
    const tnp = np.length ? np[0].t : c.fim;
    const apaga = lin(t, tnp, tnp + 0.3, 1, 0.35);
    const card = (x: number, t0: number, icone: React.ReactNode, preco: string, tp: number, rot: Rot, corPreco: string) => {
      const p = t0 <= c.ini + 0.01 ? abre(t, t0) : entra(t, t0, 0.3);
      const pp = t < tp ? 0 : lin(t, tp, tp + 0.2, 0, 1, Easing.out(Easing.back(1.6)));
      return (
        <div style={{ position: "absolute", left: x, top: 90, width: 420, height: 560, borderRadius: 30, background: "#fff", boxShadow: "0 18px 40px rgba(150,80,0,0.28)", opacity: p * apaga, transform: `translateY(${(1 - p) * 80}px) scale(${0.92 + 0.08 * p})`, textAlign: "center" }}>
          <div style={{ marginTop: 40 }}>{icone}</div>
          <div style={{ fontFamily: "Anton", fontSize: 190, lineHeight: 1.05, color: corPreco, marginTop: 10, opacity: pp, transform: `scale(${0.8 + 0.2 * pp})` }}>{preco}</div>
          <Palavras itens={rot} t={t} estilo={{ ...INTER(40, FUNDO, false), letterSpacing: 4, marginTop: 10 }} />
        </div>
      );
    };
    return (
      <div style={{ ...BASE, background: BG.precos }}>
        {card(90, c.ini, <Calendario />, "5 €", t5, [{ txt: "PROGRAMADO", t: at("tprog") }], AZUL)}
        {card(570, at("tsao"), <Relogio t={t - t10} />, "10 €", t10, rt("hora"), CORAL)}
        <Palavras itens={np} t={t} estilo={centro(710, ANTON(110, FUNDO, false))} />
      </div>
    );
  }

  if (g === "multa") {
    const tm = at("tmulta");
    const p = t < tm ? 0 : lin(t, tm, tm + 0.18, 0, 1, Easing.out(Easing.back(2)));
    const dt = t - tm;
    const tremor = dt >= 0 && dt < 0.35 ? Math.sin(dt * 90) * 12 * (1 - dt / 0.35) : 0;
    return (
      <div style={{ ...BASE, background: BG.multa }}>
        <div style={centro(200, { transform: `translateX(${tremor}px) rotate(-6deg) scale(${2 - p})`, opacity: p })}>
          <span style={{ fontFamily: "Anton", fontSize: 260, color: "#fff", border: "16px solid #fff", borderRadius: 34, padding: "0 56px", textShadow: "0 5px 0 rgba(0,0,0,0.18)" }}>MULTA</span>
        </div>
        <Palavras itens={rt("rot")} t={t} estilo={centro(640, ANTON(70))} />
      </div>
    );
  }

  if (g === "mapa") return <Mapa c={c} t={t} />;

  if (g === "dorme") {
    // "Quem dorme em Veneza já paga a taxa no valor da hospedagem."
    const taxa = rt("taxa");
    const tt = taxa.length ? taxa[taxa.length - 1].t : c.fim;
    const pc = abre(t, c.ini);
    const ps = t < tt ? 0 : lin(t, tt, tt + 0.2, 0, 1, Easing.out(Easing.back(1.8)));
    return (
      <div style={{ ...BASE, background: BG.dorme }}>
        <Palavras itens={rt("titulo").map((p) => ({ ...p, t: Math.max(p.t, 0) }))} t={t} estilo={centro(60, ANTON(84))} />
        <div style={{ position: "absolute", left: 160, top: 200, opacity: pc, transform: `translateY(${(1 - pc) * 40}px)` }}>
          <Cama s={1.25} />
        </div>
        <div style={{ position: "absolute", left: 640, top: 170, opacity: pc }}>
          <Lua s={1.1} cor={AMBAR} />
        </div>
        <div style={centro(500, { transform: `rotate(-3deg) scale(${t < tt ? 1 : 1 + 0.25 * (1 - ps)})` })}>
          <Palavras itens={taxa} t={t} estilo={{ ...ANTON(120, AMBAR, false), textShadow: "0 6px 0 rgba(10,20,90,0.35)" }} />
        </div>
        <Palavras itens={rt("valor")} t={t} estilo={centro(680, INTER(44))} />
      </div>
    );
  }

  if (g === "hospedagem") {
    // Verona (até 25% mais barato) × cidade dos canais, lado a lado
    const pv = abre(t, c.ini);
    const tc = at("tcanais");
    const pz = entra(t, tc, 0.35);
    const xv = t < tc - 0.1 ? 305 : lin(t, tc - 0.1, tc + 0.3, 305, 50);
    const cartao = (x: number, p: number, conteudo: React.ReactNode, nome: Rot, tam = 84) => (
      <div style={{ position: "absolute", left: x, top: 36, width: 470, height: 600, borderRadius: 26, overflow: "hidden", border: "6px solid #fff", boxShadow: "0 18px 40px rgba(10,60,120,0.35)", opacity: p, transform: `translateY(${(1 - p) * 90}px)` }}>
        {conteudo}
        <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75))" }} />
        <Palavras itens={nome} t={t} estilo={{ position: "absolute", left: 10, right: 10, bottom: 28, textAlign: "center", ...ANTON(tam), lineHeight: 1.02 }} />
      </div>
    );
    const p25 = rt("p25");
    return (
      <div style={{ ...BASE, background: BG.hospedagem }}>
        {cartao(xv, pv, <FotoCobre src="ponte_pietra.jpg" W={470} H={600} zoom={lin(t, c.ini, c.fim, 1.05, 1.15, Easing.linear)} foco="40% 50%" />, [{ txt: "VERONA", t: at("tverona") }])}
        {cartao(560, pz, (
          <Sequence from={Math.round((tc - c.ini) * 30)} layout="none">
            <VideoCobre src="canais.mp4" W={470} H={600} />
          </Sequence>
        ), rt("cidade"), 60)}
        <div style={{ position: "absolute", left: xv, top: 650, width: 470, textAlign: "center" }}>
          <Palavras itens={p25} t={t} estilo={{ ...ANTON(104, AMBAR, false), textShadow: "0 5px 0 rgba(10,40,90,0.35)" }} />
          <Palavras itens={rt("barato")} t={t} estilo={{ ...INTER(32), marginTop: -4 }} />
        </div>
      </div>
    );
  }

  if (g === "reserva") {
    const t4 = at("t4");
    const t5 = at("t5");
    const tl = at("tlink");
    const sai = t < tl - 0.05 ? 1 : lin(t, tl - 0.05, tl + 0.25, 1, 0);
    const pl = entra(t, tl, 0.3);
    return (
      <div style={{ ...BASE, background: BG.reserva }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, opacity: sai, transform: `scale(${0.92 + 0.08 * sai})` }}>
          <div style={{ position: "absolute", left: t < t5 - 0.45 ? 360 : lin(t, t5 - 0.45, t5 - 0.1, 360, 90), top: 150, textAlign: "center", width: 400, opacity: abre(t, c.ini), transform: `scale(${0.96 + 0.04 * abre(t, c.ini)})` }}>
            <Calendario s={2} num={t >= t4 ? "4" : ""} />
            <Palavras itens={rt("dias")} t={t} estilo={{ ...INTER(34), marginTop: 12, lineHeight: 1.25 }} />
          </div>
          <div style={{ position: "absolute", left: 500, top: 300, ...ANTON(120), opacity: entra(t, t5) }}>→</div>
          <div style={{ position: "absolute", left: 610, top: 220, width: 380, textAlign: "center", fontFamily: "Anton", fontSize: 230, color: AMBAR, opacity: entra(t, t5, 0.12), transform: `scale(${t < t5 ? 1.35 : lin(t, t5, t5 + 0.25, 1.35, 1)})`, textShadow: "0 6px 0 rgba(0,60,60,0.3)" }}>5 €</div>
        </div>
        <div style={{ position: "absolute", left: 70, top: 190, width: 940, opacity: pl, transform: `translateY(${(1 - pl) * 80}px)` }}>
          <Img src={staticFile("cda_cabecalho.png")} style={{ width: 940, borderRadius: 16, boxShadow: "0 16px 36px rgba(0,60,60,0.35)", display: "block" }} />
          <Palavras itens={rt("link")} t={t} estilo={{ textAlign: "center", ...ANTON(104, AMBAR, false), marginTop: 40, textShadow: "0 6px 0 rgba(0,60,60,0.3)" }} />
        </div>
      </div>
    );
  }
  return <div style={BASE} />;
};

/** Mapa Verona → Veneza (posições por latitude/longitude reais; costa, laguna e Lago de Garda simplificados). */
const Mapa: React.FC<{ c: Cena4; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const at = (k: string, pad: number) => Number(d[k] ?? pad);
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
  const tveneza = at("tveneza", c.ini + 1.5);
  const pLinha = lin(t, tl0, tveneza, 0, 1, Easing.inOut(Easing.cubic));
  const tb = at("tbate", c.fim);
  const ida = lin(t, tb, tb + 0.55, 0, 1, Easing.inOut(Easing.cubic));
  const volta = lin(t, tb + 0.6, tb + 1.15, 0, 1, Easing.inOut(Easing.cubic));
  const f = t < tb ? pLinha : ida - volta;
  const trem = ponto(Math.max(0, Math.min(1, f)));
  const pin = (q: { x: number; y: number }, nome: string, t0: number, dx: number) => {
    const s = t < t0 ? 0 : lin(t, t0, t0 + 0.3, 0, 1, Easing.out(Easing.back(2)));
    return (
      <g transform={`translate(${q.x},${q.y})`}>
        <circle r={26 * s} fill={CORAL} stroke="#fff" strokeWidth={6} />
        <circle r={9 * s} fill="#fff" />
        <text x={dx} y={-52} textAnchor="middle" fontFamily="Anton" fontSize={68} fill={FUNDO} stroke="#fff" strokeWidth={10} paintOrder="stroke" opacity={s}>{nome}</text>
      </g>
    );
  };
  const pBate = entra(t, tb, 0.2);
  const hora: Rot = [{ txt: "1H", t: at("t1h", c.fim) }, { txt: "E", t: at("te", c.fim) }, { txt: "POUQUINHO", t: at("tpouq", c.fim) }];
  const deVeneza: Rot = [{ txt: "DE", t: at("tde", c.fim) }, { txt: "VENEZA", t: tveneza }];
  return (
    <div style={{ ...BASE, background: "#C9EDB8" }}>
      <svg width={1080} height={H} style={{ position: "absolute", inset: 0 }}>
        <path d={mar} fill="#5EC4F2" />
        <path d={laguna} fill="#9BDDF7" />
        <path d={garda} fill="#5EC4F2" />
        <path d={P(rota)} stroke="#fff" strokeWidth={16} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={P(rota)} stroke={CORAL} strokeWidth={12} fill="none" strokeDasharray={total} strokeDashoffset={total * (1 - pLinha)} strokeLinecap="round" strokeLinejoin="round" />
        {pts.slice(1, -1).map((q, i) => <circle key={i} cx={q.x} cy={q.y} r={10} fill={pLinha > (i + 1) / (pts.length - 1) ? CORAL : "#fff"} stroke={FUNDO} strokeWidth={3} />)}
        {pin(pts[0], "VERONA", c.ini, 0)}
        {pin(pts[pts.length - 1], "VENEZA", tveneza, -40)}
        <g transform={`translate(${trem.x},${trem.y})`} opacity={(t > tl0 && t < tveneza) || (t >= tb && t < tb + 1.2) ? 1 : 0}>
          <rect x={-34} y={-22} width={68} height={44} rx={12} fill={TRACO} stroke={FUNDO} strokeWidth={4} />
          <rect x={-24} y={-12} width={20} height={14} rx={3} fill={FUNDO} />
          <rect x={4} y={-12} width={20} height={14} rx={3} fill={FUNDO} />
        </g>
      </svg>
      <div style={centro(600, { opacity: 1 - pBate })}>
        <Palavras itens={hora} t={t} estilo={ANTON(120, FUNDO, false)} />
        <Palavras itens={deVeneza} t={t} estilo={{ ...INTER(40, FUNDO, false), letterSpacing: 4 }} />
      </div>
      <div style={centro(620, { opacity: pBate, transform: `scale(${0.9 + 0.1 * pBate})` })}>
        <div style={{ fontFamily: "Anton", fontSize: 140, color: CORAL, textShadow: "0 5px 0 rgba(255,255,255,0.9)" }}>⇄ BATE-VOLTA</div>
      </div>
    </div>
  );
};

/* ---------- apoio (vídeo/foto) ---------- */

const Apoio: React.FC<{ c: Cena4; t: number }> = ({ c, t }) => {
  const z = c.zoom ?? [1.0, 1.06];
  const k = lin(t, c.ini, c.fim, z[0], z[1], Easing.linear);
  const px = c.tx !== undefined ? lin(t, c.tx - 0.25, c.tx + 0.25, 0, 1, Easing.inOut(Easing.quad)) : 0;
  const r0 = c.rotulo && c.rotulo.length ? c.rotulo[0].t : Infinity;
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
      {c.rotulo ? (
        <>
          <AbsoluteFill style={{ height: H, background: "linear-gradient(to bottom, rgba(0,0,0,0) 45%, rgba(0,0,0,0.6) 100%)", opacity: entra(t, r0) }} />
          <Palavras itens={c.rotulo} t={t} estilo={centro(H - 210, ANTON(130))} />
        </>
      ) : null}
    </div>
  );
};

/* ---------- legenda karaokê (caixa normal, palavra por palavra) ---------- */

const Legenda: React.FC<{ p: PropsVeneza4; t: number; cheio: boolean; cor: string }> = ({ p, t, cheio, cor }) => {
  const idx = p.grupos.findIndex((gr, k) => {
    const a = p.palavras[gr[0]].s;
    const prox = p.grupos[k + 1];
    const fimG = p.palavras[gr[gr.length - 1]].e + 0.3;
    const b = prox ? Math.min(p.palavras[prox[0]].s, fimG) : fimG;
    return t >= a && t < b;
  });
  if (idx < 0) return null;
  const g = p.grupos[idx];
  const y = cheio ? p.gy[idx] : COSTURA;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y - 37, textAlign: "center" }}>
      <span style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
        {g.map((i, j) => {
          const w = p.palavras[i];
          const prox = j < g.length - 1 ? p.palavras[g[j + 1]].s : w.e + 0.15;
          const o = entra(t, w.s, 0.06);
          const ativa = t >= w.s && t < Math.max(w.e, prox);
          return (
            <span key={i} style={{ color: ativa ? cor : "#fff", opacity: o, whiteSpace: "pre" }}>
              {(j ? " " : "") + w.w}
            </span>
          );
        })}
      </span>
    </div>
  );
};

/* ---------- gancho (caixa normal, palavra por palavra) ---------- */

const Gancho: React.FC<{ p: PropsVeneza4; t: number }> = ({ p, t }) => {
  if (!p.gancho.linhas.length || t >= p.gancho.fim) return null;
  let y = 270;
  return (
    <>
      <AbsoluteFill style={{ height: COSTURA, background: "linear-gradient(to bottom, rgba(0,0,0,0.45), rgba(0,0,0,0.1) 75%, rgba(0,0,0,0))" }} />
      {p.gancho.linhas.map((l, i) => {
        const top = y;
        y += l.tam * 1.08;
        return (
          <Palavras key={i} itens={l.palavras} t={t} sobe={24}
            estilo={{ position: "absolute", left: 72, top, fontFamily: "Anton", fontSize: l.tam, lineHeight: 1.05, color: l.cor ?? "#fff", textShadow: "0 4px 24px rgba(0,0,0,0.6)" }} />
        );
      })}
    </>
  );
};

const SFX = { impacto: pdxImpacto, swish: pdxSwish, obturador: pdxObturador, riser: pdxRiser } as const;

export const VenezaReel4: React.FC<PropsVeneza4> = (p) => {
  fontes();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const cena = p.cenas.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cenas[p.cenas.length - 1];
  const corte = p.cortes.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cortes[p.cortes.length - 1];
  const cheio = cena.tipo === "diego";
  const z = cena.zoom ?? [1, 1];
  const zoomDiego = cheio ? lin(t, cena.ini, cena.fim, z[0], z[1], Easing.linear) : 1;
  const fromC = Math.round(cena.ini * fps);
  const naCta = f >= Math.round(p.cenas[p.cenas.length - 1].ini * fps);
  const legendaVisivel = t >= p.gancho.fim && t < p.cta.leg_fim;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(2 * fps)}>
          <Audio src={SFX[s.som]} volume={Math.pow(10, s.db / 20)} />
        </Sequence>
      ))}
      <Diego cheio={cheio} zoom={zoomDiego} pb={!!corte?.pb} divOff={corte?.div_off ?? -340} />
      {!cheio && (
        <Sequence key={cena.ini} from={fromC} durationInFrames={Math.max(1, Math.round(cena.fim * fps) - fromC + 2)} layout="none">
          {cena.tipo === "graf" ? <Grafismo c={cena} t={t} /> : <Apoio c={cena} t={t} />}
          <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: 1080, height: 6, background: "rgba(0,0,0,0.55)" }} />
        </Sequence>
      )}
      <Gancho p={p} t={t} />
      {legendaVisivel && <Legenda p={p} t={t} cheio={cheio} cor={naCta ? AMBAR_CTA : AMBAR} />}
      <Placa rotulo="DICAS DE VIAGEM TODA SEMANA" destino="ME SEGUE" entrada={p.cta.ini * 1000} y={p.cta.placa_y} />
      <Som nome="clack" em={p.cta.ini * 1000} relDb={-6} refLufs={-14} />
    </AbsoluteFill>
  );
};
