/**
 * Reel "GTA 6 × cidades de jogo" (reels/gta6-cidades/revN), formato Tela dividida.
 * Linguagem do formato (docs/FORMATOS_REELS.md) do gancho até antes do CTA; DS V2 só no CTA (Placa).
 * Até o fim da fala sobre o GTA (props.fimGta) as cores de destaque são as do GTA VI (pedido do Diego);
 * depois, o âmbar do formato.
 * Render: --public-dir=reels/gta6-cidades/revN/public --props=reels/gta6-cidades/revN/public/props.json
 */
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { loadFont } from "@remotion/fonts";
import { fitText } from "@remotion/layout-utils";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";
import { Placa } from "../ds/Placa";

loadFont({ family: "Anton", url: anton, weight: "400" });
loadFont({ family: "Inter", url: inter800, weight: "800" });

type Cena = {
  id: string;
  tipo: "topo" | "cheia" | "diego" | "grade" | "contador" | "cta";
  ini: number;
  fim: number;
  video?: string;
  foto?: string;
  zoom?: [number, number];
  fotos?: string[];
  entra_em?: number[];
  numero?: { linhas: string[]; em: number; linhas_em: number[] };
  transicao?: "clarao" | "luz" | null;
  diego?: string;
  placa?: { rotulo?: string; destino: string; modulo?: "seta" };
};
type Legenda = { ini: number; fim: number; palavras: { t: string; destaque: boolean }[] };
type Linha = { t: string; em: number; tam: number; grad?: boolean };
export type PropsGta = {
  fps: number;
  duracao: number;
  fimGta: number;
  voz: number;
  cenas: Cena[];
  legendas: Legenda[];
  gancho: { ini: number; fim: number; linhas: Linha[] }[];
};

// ---- valores do formato (FORMATOS_REELS.md) e cores do GTA VI (amostradas do logo oficial) ----
const W = 1080;
const H = 1920;
const COSTURA = 900;
const ROSTO_DESLOC = 648; // rosto a 42% da metade de baixo
const FUNDO_ANIM = "#14120F";
const TRACO = "#ECE5D8";
const AMBAR = "#E0AE5C";
const GTA_ROSA = "#F06080";
const GTA_LARANJA = "#F09040";
const GTA_ROXO = "#4050C0";
const GRAD_GTA = `linear-gradient(90deg, ${GTA_ROSA} 0%, #F05090 35%, ${GTA_LARANJA} 100%)`;
const X0 = 72;
const LARG_MAX = 872;

const useT = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return f / fps;
};
const sq = (s: number, fps: number) => Math.round(s * fps);

/** Imagem/vídeo cobrindo a área, com zoom lento e linear (fotos). */
const Midia: React.FC<{ c: Cena; w: number; h: number }> = ({ c, w, h }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = (c.fim - c.ini) * fps;
  const z = c.zoom ? interpolate(f, [0, dur], c.zoom, { extrapolateRight: "clamp" }) : 1;
  const est: React.CSSProperties = { width: w, height: h, objectFit: "cover", transform: `scale(${z})` };
  return (
    <div style={{ width: w, height: h, overflow: "hidden", position: "absolute", left: 0, top: 0 }}>
      {c.video ? <OffthreadVideo src={staticFile(c.video)} muted style={est} /> : c.foto ? <Img src={staticFile(c.foto)} style={est} /> : null}
    </div>
  );
};

/** Grade 2×2 das quatro cidades (acervo do Diego), cada foto entra na palavra. */
const Grade: React.FC<{ c: Cena }> = ({ c }) => {
  const t = useT() + c.ini;
  return (
    <AbsoluteFill style={{ backgroundColor: FUNDO_ANIM }}>
      {c.fotos!.map((src, i) => {
        const d = t - c.entra_em![i];
        const o = interpolate(d, [0, 0.12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const s = interpolate(d, [0, 0.16], [0.9, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
        const x = (i % 2) * 540;
        const y = Math.floor(i / 2) * 450;
        return (
          <div key={i} style={{ position: "absolute", left: x + 6, top: y + 6, width: 528, height: 438, overflow: "hidden", opacity: o, transform: `scale(${s})`, borderRadius: 14 }}>
            <Img src={staticFile(src)} style={{ width: 528, height: 438, objectFit: "cover" }} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** Número em tela cheia: linhas Anton sobem de trás de uma máscara (folga de 50 px para acentos). */
const Numero: React.FC<{ linhas: string[]; em: number[]; cenaIni: number; fundo?: boolean; y: number; corDest: string }> = ({ linhas, em, cenaIni, fundo, y, corDest }) => {
  const t = useT() + cenaIni;
  let topo = y;
  return (
    <AbsoluteFill style={{ backgroundColor: fundo ? FUNDO_ANIM : undefined }}>
      {linhas.map((l, i) => {
        const tamAlvo = i === 0 ? 250 : 120;
        const tam = Math.min(tamAlvo, fitText({ text: l, withinWidth: LARG_MAX, fontFamily: "Anton", fontWeight: "400" }).fontSize);
        const d = t - em[i];
        const sobe = interpolate(d, [0, 0.18], [tam * 1.1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
        const alt = tam * 1.05 + 50;
        const el = (
          <div key={i} style={{ position: "absolute", left: 0, right: 0, top: topo - 50, height: alt, overflow: "hidden" }}>
            {d >= 0 && (
              <div style={{ position: "absolute", left: 0, right: 0, top: 50, textAlign: "center", transform: `translateY(${sobe}px)`, fontFamily: "Anton", fontSize: tam, lineHeight: 1.05, color: i === 0 ? TRACO : corDest, textShadow: "0 6px 30px rgba(0,0,0,0.6)" }}>
                {l}
              </div>
            )}
          </div>
        );
        topo += tam * 1.05 + 14;
        return el;
      })}
    </AbsoluteFill>
  );
};

/** Texto do gancho: Anton, alinhado à esquerda em x 72, linha a linha no tempo da fala. */
const Gancho: React.FC<{ blocos: PropsGta["gancho"] }> = ({ blocos }) => {
  const t = useT();
  const b = blocos.find((x) => t >= x.ini && t < x.fim);
  if (!b) return null;
  let topo = 285;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, top: 240, width: W, height: COSTURA - 240, background: "linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.38) 55%, rgba(0,0,0,0) 100%)" }} />
      {b.linhas.map((l, i) => {
        const tam = Math.min(l.tam, fitText({ text: l.t, withinWidth: LARG_MAX, fontFamily: "Anton", fontWeight: "400" }).fontSize);
        const d = t - l.em;
        const o = interpolate(d, [0, 0.16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const dy = interpolate(d, [0, 0.16], [24, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
        const el = (
          <div key={i} style={{ position: "absolute", left: X0, top: topo, opacity: o, transform: `translateY(${dy}px)`, fontFamily: "Anton", fontSize: tam, lineHeight: 1.0, whiteSpace: "nowrap", textTransform: "uppercase" }}>
            {l.grad ? (
              <span style={{ backgroundImage: GRAD_GTA, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", filter: `drop-shadow(0 5px 0 ${GTA_ROXO}) drop-shadow(0 8px 24px rgba(0,0,0,0.7))` }}>{l.t}</span>
            ) : (
              <span style={{ color: "#FFFFFF", textShadow: "0 4px 0 rgba(0,0,0,0.35), 0 6px 24px rgba(0,0,0,0.85)" }}>{l.t}</span>
            )}
          </div>
        );
        topo += tam * 1.0 + 10;
        return el;
      })}
    </AbsoluteFill>
  );
};

/** Legenda do formato: Inter 800 66 px, 1 linha, centrada em x 540; 1 palavra de destaque. */
const Legendas: React.FC<{ p: PropsGta }> = ({ p }) => {
  const t = useT();
  const l = p.legendas.find((x) => t >= x.ini && t < x.fim);
  if (!l) return null;
  const cena = p.cenas.find((c) => t >= c.ini && t < c.fim);
  const y = cena && (cena.tipo === "diego" || cena.tipo === "cheia") ? 1320 : COSTURA;
  const cor = l.ini < p.fimGta ? GTA_ROSA : AMBAR;
  const d = t - l.ini;
  const o = interpolate(d, [0, 0.12], [0, 1], { extrapolateRight: "clamp" });
  const s = interpolate(d, [0, 0.12], [0.94, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, transform: `translateY(-50%) scale(${s})`, opacity: o, textAlign: "center", fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, color: "#FFFFFF", whiteSpace: "nowrap", textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
      {l.palavras.map((w, i) => (
        <span key={i} style={{ color: w.destaque ? cor : undefined }}>
          {i > 0 ? " " : ""}
          {w.t}
        </span>
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

/** Clarão de volta (≈170 ms) e Luz de passagem (≈370 ms, pico ≤ 85% por 4 quadros, corte escondido no pico). */
const Transicoes: React.FC<{ p: PropsGta }> = ({ p }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <>
      {p.cenas.filter((c) => c.transicao).map((c) => {
        const corte = sq(c.ini, fps);
        const d = f - corte;
        if (c.transicao === "clarao") {
          if (d < 0 || d > 5) return null;
          const o = interpolate(d, [0, 5], [0.85, 0]);
          return <AbsoluteFill key={c.id} style={{ backgroundColor: "#FFFFFF", opacity: o }} />;
        }
        if (d < -6 || d > 5) return null;
        const o = interpolate(d, [-6, -3, -2, 1, 5], [0.08, 0.6, 0.85, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return <AbsoluteFill key={c.id} style={{ background: "linear-gradient(180deg, #FFD9A0 0%, #F7B267 45%, rgba(247,178,103,0.0) 100%)", opacity: o, mixBlendMode: "screen" }} />;
      })}
    </>
  );
};

export const GtaCidades: React.FC<PropsGta> = (p) => {
  const { fps } = useVideoConfig();
  const t = useT();
  const cenaAtual = p.cenas.find((c) => t >= c.ini && t < c.fim);
  const dividida = cenaAtual && (cenaAtual.tipo === "topo" || cenaAtual.tipo === "grade" || cenaAtual.tipo === "cta");
  const naGta = t < p.fimGta;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Diego embaixo durante toda a fala (vídeo decupado, em sincronia com a voz) */}
      <Sequence durationInFrames={sq(p.voz, fps)} layout="none">
        <AbsoluteFill style={{ top: COSTURA, height: H - COSTURA, overflow: "hidden" }}>
          <OffthreadVideo src={staticFile("diego.mp4")} muted style={{ position: "absolute", top: ROSTO_DESLOC - COSTURA, left: 0, width: W, height: H }} />
        </AbsoluteFill>
      </Sequence>

      {p.cenas.map((c) => (
        <Sequence key={c.id} from={sq(c.ini, fps)} durationInFrames={sq(c.fim, fps) - sq(c.ini, fps)} name={c.id} layout="none">
          {c.tipo === "topo" && (
            <AbsoluteFill style={{ height: COSTURA, overflow: "hidden" }}>
              <Midia c={c} w={W} h={COSTURA} />
            </AbsoluteFill>
          )}
          {c.tipo === "grade" && (
            <AbsoluteFill style={{ height: COSTURA, overflow: "hidden" }}>
              <Grade c={c} />
            </AbsoluteFill>
          )}
          {c.tipo === "diego" && <DiegoCheio c={c} />}
          {c.tipo === "cheia" && (
            <AbsoluteFill>
              <Midia c={c} w={W} h={H} />
              <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.12) 38%, rgba(0,0,0,0.5) 58%, rgba(0,0,0,0.78) 100%)" }} />
              {c.numero && <Numero linhas={c.numero.linhas} em={c.numero.linhas_em} cenaIni={c.ini} y={520} corDest={AMBAR} />}
            </AbsoluteFill>
          )}
          {c.tipo === "contador" && c.numero && <Numero linhas={c.numero.linhas} em={c.numero.linhas_em} cenaIni={c.ini} fundo y={640} corDest={AMBAR} />}
          {c.tipo === "cta" && (
            <AbsoluteFill>
              <AbsoluteFill style={{ height: COSTURA, overflow: "hidden" }}>
                <Midia c={c} w={W} h={COSTURA} />
              </AbsoluteFill>
              <AbsoluteFill style={{ top: COSTURA, height: H - COSTURA, overflow: "hidden" }}>
                <OffthreadVideo src={staticFile(c.diego!)} muted style={{ position: "absolute", top: ROSTO_DESLOC - COSTURA, left: 0, width: W, height: H }} />
              </AbsoluteFill>
            </AbsoluteFill>
          )}
        </Sequence>
      ))}

      {/* costura: linha de 6 px; nas cenas do GTA, no gradiente do GTA */}
      {dividida && (
        <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: W, height: 6, background: naGta ? GRAD_GTA : "rgba(0,0,0,0.55)" }} />
      )}

      <Gancho blocos={p.gancho} />
      <Legendas p={p} />
      <Transicoes p={p} />

      {/* CTA: único elemento do DS V2 no Reel */}
      {p.cenas.filter((c) => c.tipo === "cta").map((c) => (
        <Sequence key="placa" from={sq(c.ini, fps)} layout="none">
          <Placa rotulo={c.placa!.rotulo} destino={c.placa!.destino} modulo={c.placa!.modulo ?? "seta"} entrada={0} />
        </Sequence>
      ))}
      <Grao />
    </AbsoluteFill>
  );
};

/** Diego em tela cheia, aproximação lenta e linear (100 → 105%). */
const DiegoCheio: React.FC<{ c: Cena }> = ({ c }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const z = interpolate(f, [0, (c.fim - c.ini) * fps], [1, 1.05]);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo src={staticFile("diego.mp4")} muted startFrom={sq(c.ini, fps)} style={{ width: W, height: H, transform: `scale(${z})` }} />
    </AbsoluteFill>
  );
};

export const metadadosGta = ({ props }: { props: PropsGta }) => ({
  durationInFrames: Math.max(1, Math.round((props.duracao ?? 1) * (props.fps ?? 30))),
  fps: props.fps ?? 30,
});
