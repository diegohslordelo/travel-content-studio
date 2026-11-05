/**
 * Reel "3 pontos turísticos da Vice City" (reels/gta6-vice-city/revN), formato Tela dividida.
 * Linguagem do formato (docs/FORMATOS_REELS.md); sem CTA, então sem DS V2.
 * Pedidos do Diego (05/11/2026):
 *  - ponto turístico = "comparar": Vice City do jogo em cima, Miami de verdade embaixo;
 *  - palavra de ênfase da legenda nas cores do GTA VI (o resto em branco);
 *  - versão B: luz roxa do GTA muito leve só nas gravações do Diego (props.roxo = opacidade; 0 = versão A).
 * Render: --public-dir=reels/gta6-vice-city/revN/public --props=reels/gta6-vice-city/revN/public/props.json
 */
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { loadFont } from "@remotion/fonts";
import { fitText } from "@remotion/layout-utils";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";

loadFont({ family: "Anton", url: anton, weight: "400" });
loadFont({ family: "Inter", url: inter800, weight: "800" });

type Cena = {
  id: string;
  tipo: "topo" | "diego" | "comparar";
  ini: number;
  fim: number;
  video?: string;
  foto?: string;
  foto_baixo?: string;
  zoom?: [number, number];
  zoom_baixo?: [number, number];
  origem?: string;
  origem_baixo?: string;
  tag_cima?: string;
  tag_baixo?: string;
  numero?: string;
  transicao?: "clarao" | "luz" | "dissolve" | null;
};
type Legenda = { ini: number; fim: number; palavras: { t: string; destaque: boolean }[] };
type Linha = { t: string; em: number; tam: number; forte?: boolean };
export type PropsVice = {
  fps: number;
  duracao: number;
  voz: number;
  roxo: number;
  cenas: Cena[];
  legendas: Legenda[];
  gancho: { ini: number; fim: number; linhas: Linha[] }[];
};

// ---- valores do formato (FORMATOS_REELS.md) e cores do GTA VI (amostradas do logo oficial, mesmas do Reel gta6-cidades) ----
const W = 1080;
const H = 1920;
const COSTURA = 900;
const ROSTO_DESLOC = 648;
const GTA_ROSA = "#F06080";
const GTA_LARANJA = "#F09040";
const GTA_ROXO = "#4050C0";
const GRAD_GTA = `linear-gradient(90deg, ${GTA_ROSA} 0%, #F05090 35%, ${GTA_LARANJA} 100%)`;
const LUZ_ROXA = "#8A3CFF"; // luz da versão B: o roxo do céu do logo/trailer do GTA VI
const X0 = 72;
const LARG_MAX = 872;

const useT = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return f / fps;
};
const sq = (s: number, fps: number) => Math.round(s * fps);

/** Foto/vídeo cobrindo a área, Ken Burns linear. */
const Midia: React.FC<{ src?: string; video?: string; w: number; h: number; zoom?: [number, number]; origem?: string; dur: number }> = ({ src, video, w, h, zoom, origem, dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const z = zoom ? interpolate(f, [0, dur * fps], zoom, { extrapolateRight: "clamp" }) : 1;
  const est: React.CSSProperties = { width: w, height: h, objectFit: "cover", transform: `scale(${z})`, transformOrigin: origem ?? "50% 50%" };
  return (
    <div style={{ width: w, height: h, overflow: "hidden", position: "absolute", left: 0, top: 0 }}>
      {video ? <OffthreadVideo src={staticFile(video)} muted style={est} /> : src ? <Img src={staticFile(src)} style={est} /> : null}
    </div>
  );
};

/** Etiqueta pequena (jogo: gradiente do GTA; real: branco). */
const Tag: React.FC<{ t: string; jogo: boolean; x: number; y: number; em: number }> = ({ t, jogo, x, y, em }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const d = f / fps - em;
  const o = interpolate(d, [0, 0.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dx = interpolate(d, [0, 0.25], [-18, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o, transform: `translateX(${dx}px)`, padding: "8px 16px", borderRadius: 10,
      background: jogo ? GRAD_GTA : "rgba(255,255,255,0.94)", color: jogo ? "#FFFFFF" : "#14120F", fontFamily: "Inter", fontWeight: 800, fontSize: 30,
      letterSpacing: 1, textShadow: jogo ? "0 2px 6px rgba(64,80,192,0.6)" : undefined, boxShadow: "0 6px 20px rgba(0,0,0,0.45)", whiteSpace: "nowrap" }}>
      {t}
    </div>
  );
};

/** Número do ponto turístico (Anton, gradiente do GTA), no canto do jogo. */
const Numero: React.FC<{ n: string }> = ({ n }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const d = f / fps;
  const s = interpolate(d, [0, 0.22], [1.35, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.6)) });
  const o = interpolate(d, [0, 0.12], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", right: X0, top: 222, opacity: o, transform: `scale(${s})`, transformOrigin: "100% 0%", fontFamily: "Anton", fontSize: 190, lineHeight: 1 }}>
      <span style={{ backgroundImage: GRAD_GTA, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", filter: `drop-shadow(0 6px 0 ${GTA_ROXO}) drop-shadow(0 10px 26px rgba(0,0,0,0.7))` }}>{n}</span>
    </div>
  );
};

/** Comparar: jogo em cima (corta seco), Miami de verdade embaixo (desliza da direita em 0,35 s). */
const Comparar: React.FC<{ c: Cena }> = ({ c }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const d = f / fps;
  const dur = c.fim - c.ini;
  const dx = interpolate(d, [0, 0.35], [W, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ height: COSTURA, overflow: "hidden" }}>
        <Midia src={c.foto} video={c.video} w={W} h={COSTURA} zoom={c.zoom} origem={c.origem} dur={dur} />
        <div style={{ position: "absolute", left: 0, top: 0, width: W, height: 360, background: "linear-gradient(180deg, rgba(0,0,0,0.35), rgba(0,0,0,0))" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ top: COSTURA, height: H - COSTURA, overflow: "hidden", backgroundColor: "#000" }}>
        <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H - COSTURA, transform: `translateX(${dx}px)` }}>
          <Midia src={c.foto_baixo} w={W} h={H - COSTURA} zoom={c.zoom_baixo} origem={c.origem_baixo} dur={dur} />
        </div>
      </AbsoluteFill>
      {c.numero && <Numero n={c.numero} />}
      {c.tag_cima && <Tag t={c.tag_cima} jogo x={X0} y={240} em={0.1} />}
      {c.tag_baixo && <Tag t={c.tag_baixo} jogo={false} x={X0} y={COSTURA + 72} em={0.35} />}
    </AbsoluteFill>
  );
};

/** Luz roxa muito leve sobre o Diego (versão B). */
const LuzRoxa: React.FC<{ roxo: number }> = ({ roxo }) =>
  roxo > 0 ? (
    <>
      <AbsoluteFill style={{ backgroundColor: LUZ_ROXA, mixBlendMode: "soft-light", opacity: roxo }} />
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 75% 60% at 88% 18%, ${LUZ_ROXA} 0%, rgba(138,60,255,0) 70%)`, mixBlendMode: "screen", opacity: roxo * 0.55 }} />
    </>
  ) : null;

/** Texto do gancho: Anton, à esquerda em x 72, linha a linha no tempo da fala (sem cor do GTA: o jogo só aparece no "sofá"). */
const Gancho: React.FC<{ blocos: PropsVice["gancho"] }> = ({ blocos }) => {
  const t = useT();
  const b = blocos.find((x) => t >= x.ini && t < x.fim);
  if (!b) return null;
  // texto na base da metade de cima (a ação da foto fica livre em cima)
  const tams = b.linhas.map((l) => Math.min(l.tam, fitText({ text: l.t, withinWidth: LARG_MAX, fontFamily: "Anton", fontWeight: "400" }).fontSize));
  let topo = COSTURA - 44 - tams.reduce((a, x) => a + x + 6, 0);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, top: 380, width: W, height: COSTURA - 380, background: "linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.4) 55%, rgba(0,0,0,0) 100%)" }} />
      {b.linhas.map((l, i) => {
        const tam = tams[i];
        const d = t - l.em;
        const o = interpolate(d, [0, 0.12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const s = l.forte ? interpolate(d, [0, 0.16], [1.18, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 1;
        const el = (
          <div key={i} style={{ position: "absolute", left: X0, top: topo, opacity: o, transform: `scale(${s})`, transformOrigin: "0% 50%", fontFamily: "Anton", fontSize: tam, lineHeight: 1.0, whiteSpace: "nowrap", color: "#FFFFFF",
            textShadow: "0 4px 0 rgba(0,0,0,0.35), 0 6px 26px rgba(0,0,0,0.9)" }}>
            {l.t}
          </div>
        );
        topo += tam * 1.0 + 6;
        return el;
      })}
    </AbsoluteFill>
  );
};

/** Legenda do formato: Inter 800 66 px, 1 linha, centrada em x 540; ênfase no gradiente do GTA. */
const Legendas: React.FC<{ p: PropsVice }> = ({ p }) => {
  const t = useT();
  const l = p.legendas.find((x) => t >= x.ini && t < x.fim);
  if (!l) return null;
  const cena = p.cenas.find((c) => t >= c.ini && t < c.fim);
  const y = cena && cena.tipo === "diego" ? 1320 : COSTURA;
  const d = t - l.ini;
  const o = interpolate(d, [0, 0.1], [0, 1], { extrapolateRight: "clamp" });
  const s = interpolate(d, [0, 0.1], [0.94, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, transform: `translateY(-50%) scale(${s})`, opacity: o, textAlign: "center", fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, color: "#FFFFFF", whiteSpace: "nowrap", textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
      {l.palavras.map((w, i) => (
        <React.Fragment key={i}>
          {i > 0 ? " " : ""}
          {w.destaque ? (
            <span style={{ backgroundImage: GRAD_GTA, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", textShadow: "none", filter: `drop-shadow(0 3px 0 ${GTA_ROXO}) drop-shadow(0 4px 14px rgba(0,0,0,0.8))` }}>{w.t}</span>
          ) : (
            <span>{w.t}</span>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

/** Grão de 6% (overlay), semente por quadro. */
const Grao: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.06, pointerEvents: "none" }}>
      <svg width={W} height={H}>
        <filter id={`g${f}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={f % 97} />
        </filter>
        <rect width={W} height={H} filter={`url(#g${f})`} />
      </svg>
    </AbsoluteFill>
  );
};

/** Clarão de volta (≈170 ms) e Luz de passagem (≈370 ms, corte escondido no pico). O dissolve fica na própria cena. */
const Transicoes: React.FC<{ p: PropsVice }> = ({ p }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <>
      {p.cenas.filter((c) => c.transicao === "clarao" || c.transicao === "luz").map((c) => {
        const d = f - sq(c.ini, fps);
        if (c.transicao === "clarao") {
          if (d < 0 || d > 5) return null;
          return <AbsoluteFill key={c.id} style={{ backgroundColor: "#FFFFFF", opacity: interpolate(d, [0, 5], [0.85, 0]) }} />;
        }
        if (d < -6 || d > 5) return null;
        const o = interpolate(d, [-6, -3, -2, 1, 5], [0.08, 0.6, 0.85, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return <AbsoluteFill key={c.id} style={{ background: "linear-gradient(180deg, #FFD9A0 0%, #F7B267 45%, rgba(247,178,103,0.0) 100%)", opacity: o, mixBlendMode: "screen" }} />;
      })}
    </>
  );
};

/** Dissolve de 0,4 s da cena anterior para esta (volta no tempo: jogo de 2002). */
const Dissolve: React.FC<{ anterior: Cena; c: Cena }> = ({ anterior, c }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const o = interpolate(f / fps, [0, 0.4], [1, 0], { extrapolateRight: "clamp" });
  if (o <= 0) return null;
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <Sequence from={-sq(c.ini - anterior.ini, fps)} layout="none">
        <Comparar c={anterior} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const GtaViceCity: React.FC<PropsVice> = (p) => {
  const { fps } = useVideoConfig();
  const t = useT();
  const atual = p.cenas.find((c) => t >= c.ini && t < c.fim);
  const dividida = atual && atual.tipo !== "diego";
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Diego embaixo durante toda a fala (vídeo decupado, em sincronia com a voz) */}
      <Sequence durationInFrames={sq(p.duracao, fps)} layout="none">
        <AbsoluteFill style={{ top: COSTURA, height: H - COSTURA, overflow: "hidden" }}>
          <OffthreadVideo src={staticFile("diego.mp4")} muted style={{ position: "absolute", top: ROSTO_DESLOC - COSTURA, left: 0, width: W, height: H }} />
          <LuzRoxa roxo={p.roxo} />
        </AbsoluteFill>
      </Sequence>

      {p.cenas.map((c, i) => (
        <Sequence key={c.id} from={sq(c.ini, fps)} durationInFrames={sq(c.fim, fps) - sq(c.ini, fps)} name={c.id} layout="none">
          {c.tipo === "topo" && (
            <AbsoluteFill style={{ height: COSTURA, overflow: "hidden" }}>
              <Midia src={c.foto} video={c.video} w={W} h={COSTURA} zoom={c.zoom} origem={c.origem} dur={c.fim - c.ini} />
              {c.tag_cima && <Tag t={c.tag_cima} jogo x={X0} y={240} em={0.15} />}
            </AbsoluteFill>
          )}
          {c.tipo === "diego" && <DiegoCheio c={c} roxo={p.roxo} />}
          {c.tipo === "comparar" && <Comparar c={c} />}
          {c.transicao === "dissolve" && i > 0 && <Dissolve anterior={p.cenas[i - 1]} c={c} />}
        </Sequence>
      ))}

      {/* costura: linha de 6 px no gradiente do GTA */}
      {dividida && <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: W, height: 6, background: atual?.id === "gancho" ? "rgba(0,0,0,0.55)" : GRAD_GTA }} />}

      <Gancho blocos={p.gancho} />
      <Legendas p={p} />
      <Transicoes p={p} />
      <Grao />
    </AbsoluteFill>
  );
};

/** Diego em tela cheia (plano aberto no sofá), aproximação lenta e linear (100 → 105%). */
const DiegoCheio: React.FC<{ c: Cena; roxo: number }> = ({ c, roxo }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const z = interpolate(f, [0, (c.fim - c.ini) * fps], [1, 1.05]);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo src={staticFile("diego.mp4")} muted startFrom={sq(c.ini, fps)} style={{ width: W, height: H, transform: `scale(${z})` }} />
      <LuzRoxa roxo={roxo} />
    </AbsoluteFill>
  );
};

export const metadadosVice = ({ props }: { props: PropsVice }) => ({
  durationInFrames: Math.max(1, Math.round((props.duracao ?? 1) * (props.fps ?? 30))),
  fps: props.fps ?? 30,
});
