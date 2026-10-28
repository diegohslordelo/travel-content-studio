/**
 * Reel "A multa que salvou o trem" (reels/florenca-multa/rev1) · formato Tela verde.
 * O Diego (recorte por IA da gravação no quarto) fica fixo embaixo; atrás dele passam acervo e animações,
 * cada troca ancorada numa palavra da fala. DS V2 só no CTA final (Placa + clack). Decisões: reels/florenca-multa/rev1/QA_REV1.md.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Grao } from "../ds/material";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { db } from "../ds/tempo";
import arLongo from "../../../sons/externos/PDX_ar_longo.wav";
import impacto from "../../../sons/externos/PDX_impacto.wav";
import obturador from "../../../sons/externos/PDX_obturador.wav";
import pagina from "../../../sons/externos/PDX_pagina.wav";
import riser from "../../../sons/externos/PDX_riser.wav";
import swish from "../../../sons/externos/PDX_swish.wav";
import { Bilhete, CameraMapa, EtiquetaTrem, Fiscais, Mapa, Multa, PONTOS, Pessoa, Relogio, Titulo } from "./Graficos";
import { COR, GRADE_VIDEO, SOMBRA_TEXTO, TEXTO, carregarFontesFlorenca, clamp, ease, easeIn, easeInOut, lerp, mola } from "./tema";

carregarFontesFlorenca();

type Segmento = { tomada: string; arquivo: string; de: number; ini: number; dur: number; salto: boolean; s: number; tx: number; ty: number };
type Palavra = { w: string; t: number; fim: number };
type Legenda = { ini: number; fim: number; texto: string };
export type PropsFlorenca = {
  duracao: number;
  fala_fim: number;
  segmentos: Segmento[];
  palavras: Palavra[];
  legendas: Legenda[];
  voz: string;
  trilha: string | null;
  voz_lufs: number;
  /** false = versão sem rostos de outras pessoas (pedido do Diego, 28/10/2026). */
  rostos: boolean;
};

export const propsVaziasFlorenca: PropsFlorenca = { duracao: 1, fala_fim: 1, segmentos: [], palavras: [], legendas: [], voz: "voz.wav", trilha: null, voz_lufs: -16, rostos: true };

export const metadadosFlorenca: CalculateMetadataFunction<PropsFlorenca> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.round(props.duracao * 24)),
  fps: 24,
});

const useT = () => useCurrentFrame() / useVideoConfig().fps;

// ------------------------------------------------------------------ peças

/** Clipe de acervo (mudo) com zoom lento linear e transição de entrada/saída. */
const Clipe: React.FC<{
  src: string; ini: number; fim: number; de?: number; vel?: number; zoom?: [number, number]; origem?: string;
  estilo?: (t: number) => React.CSSProperties; grade?: string;
}> = ({ src, ini, fim, de = 0, vel = 1, zoom = [1.0, 1.06], origem = "50% 40%", estilo, grade = GRADE_VIDEO }) => {
  const { fps } = useVideoConfig();
  const t = useT();
  const a = Math.round(ini * fps), b = Math.round(fim * fps);
  const z = lerp(t, ini, fim, zoom[0], zoom[1], (p) => p);
  return (
    <Sequence from={a} durationInFrames={Math.max(1, b - a)} layout="none">
      <AbsoluteFill style={{ overflow: "hidden", ...(estilo ? estilo(t) : {}) }}>
        <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: origem, filter: grade }}>
          <Video src={staticFile(src)} muted trimBefore={Math.round(de * fps)} playbackRate={vel} objectFit="cover" style={{ width: "100%", height: "100%" }} />
        </AbsoluteFill>
      </AbsoluteFill>
    </Sequence>
  );
};

/** Janela de cena (renderiza só no intervalo, com folga para as transições). */
const Janela: React.FC<{ ini: number; fim: number; children: React.ReactNode }> = ({ ini, fim, children }) => {
  const t = useT();
  return t >= ini && t < fim ? <>{children}</> : null;
};

// transições (estilo aplicado à cena que sai ou entra)
const chicoteSai = (t0: number) => (t: number): React.CSSProperties => {
  const p = easeIn((t - t0) / 0.2);
  return { transform: `translateX(${-30 * p}%)`, filter: `blur(${12 * p}px)` };
};
const chicoteEntra = (t0: number) => (t: number): React.CSSProperties => {
  const p = ease((t - t0) / 0.2);
  return { transform: `translateX(${30 * (1 - p)}%)`, filter: `blur(${12 * (1 - p)}px)` };
};
const mergulhoSai = (t0: number, ox = "50%", oy = "45%") => (t: number): React.CSSProperties => {
  const p = easeIn((t - t0) / 0.45);
  return { transform: `scale(${1 + 2.2 * p})`, transformOrigin: `${ox} ${oy}`, filter: `blur(${22 * p}px)`, opacity: 1 - clamp((t - t0 - 0.3) / 0.15) };
};
const mergulhoEntra = (t0: number) => (t: number): React.CSSProperties => {
  const p = ease((t - t0) / 0.45);
  return { transform: `scale(${1.6 - 0.6 * p})`, filter: `blur(${20 * (1 - p)}px)`, opacity: clamp((t - t0) / 0.18) };
};
const fusaoEntra = (t0: number, d = 0.35) => (t: number): React.CSSProperties => ({ opacity: easeInOut((t - t0) / d) });

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS, 10.4): entra 3 quadros, pico ≤ 4 quadros (até 85%), sai 4 quadros. O corte fica no pico. */
const LuzDePassagem: React.FC<{ corte: number }> = ({ corte }) => {
  const t = useT();
  const q = 1 / 24;
  const i0 = corte - 5 * q, p0 = corte - 2 * q, p1 = corte + 2 * q, f1 = corte + 6 * q;
  if (t < i0 || t > f1) return null;
  const o = t < p0 ? lerp(t, i0, p0, 0.08, 0.85) : t < p1 ? 0.85 : lerp(t, p1, f1, 0.85, 0, (x) => x);
  const desce = t < p0 ? lerp(t, i0, p0, 30, 100) : 100;
  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        mixBlendMode: "screen",
        opacity: o,
        background: `radial-gradient(120% ${desce}% at ${t > p1 ? 15 : 50}% 0%, #FFD08A 0%, #FF9A4D 45%, rgba(255,120,60,0) 100%)`,
      }}
    />
  );
};
/** Clarão de volta: 1º quadro estourado, normal em 5 quadros. */
const Clarao: React.FC<{ em: number }> = ({ em }) => {
  const t = useT();
  if (t < em || t > em + 6 / 24) return null;
  return <AbsoluteFill style={{ background: "#FFF8EC", opacity: lerp(t, em, em + 5 / 24, 0.9, 0, (x) => x) }} />;
};

// ------------------------------------------------------------------ Diego (recorte), legendas, sons

/** Zoom de corte (punch-in) nos saltos de fala e nos momentos de ênfase. Centro no rosto (x 540 · y 1400). */
const PUNCHES: [number, number, number][] = [];
const Diego: React.FC<{ segs: Segmento[]; punches: [number, number, number][] }> = ({ segs, punches }) => {
  const { fps } = useVideoConfig();
  const t = useT();
  let k = 1;
  for (const [a, b, z] of punches) if (t >= a && t < b) k = z;
  return (
    <AbsoluteFill style={{ transform: `scale(${k})`, transformOrigin: "540px 1400px" }}>
      {segs.map((s, i) => {
        const a = Math.round(s.ini * fps), d = Math.round((s.ini + s.dur) * fps) - a;
        const salto = s.salto ? 1.07 : 1;
        return (
          <Sequence key={i} from={a} durationInFrames={Math.max(1, d)} layout="none">
            <AbsoluteFill style={{ transform: `scale(${salto})`, transformOrigin: "540px 1400px" }}>
              <div
                style={{
                  position: "absolute", left: 0, top: 0, width: 1080, height: 1920,
                  transform: `translate(${s.tx}px, ${s.ty}px) scale(${s.s})`, transformOrigin: "0 0",
                  filter: "brightness(1.1) contrast(1.05) saturate(1.04) drop-shadow(0 0 2px rgba(255,236,214,.55)) drop-shadow(0 26px 46px rgba(0,0,0,.6))",
                }}
              >
                <OffthreadVideo src={staticFile(s.arquivo)} transparent muted trimBefore={Math.round(s.de * fps)} style={{ width: 1080, height: 1920 }} />
              </div>
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const Legendas: React.FC<{ legendas: Legenda[] }> = ({ legendas }) => {
  const t = useT();
  const l = legendas.find((x) => t >= x.ini && t < x.fim);
  if (!l) return null;
  const k = clamp((t - l.ini) / 0.12);
  const partes = l.texto.split(/(\*[^*]+\*)/).filter(Boolean);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1652, display: "flex", justifyContent: "center", opacity: k, transform: `scale(${0.94 + 0.06 * k})` }}>
      <div style={{ fontFamily: TEXTO, fontWeight: 800, fontSize: 66, lineHeight: 1.1, color: COR.branco, textShadow: SOMBRA_TEXTO, whiteSpace: "nowrap" }}>
        {partes.map((p, i) => (p.startsWith("*") ? <span key={i} style={{ color: COR.ambar }}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>))}
      </div>
    </div>
  );
};

const NIVEL = { arLongo: -9.8, impacto: -9.3, obturador: -22.7, pagina: -13.1, riser: -9.2, swish: -11.2 } as const;
const ARQ = { arLongo, impacto, obturador, pagina, riser, swish } as const;
const Efeito: React.FC<{ nome: keyof typeof ARQ; em: number; rel: number; ref: number }> = ({ nome, em, rel, ref }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.max(0, Math.round(em * fps))} layout="none" name={`efeito ${nome}`}>
      <Audio src={ARQ[nome]} volume={Math.min(1, db(ref + rel - NIVEL[nome]))} />
    </Sequence>
  );
};

/** Cartão de foto/vídeo (moldura clara, leve rotação) que entra com mola. */
const Cartao: React.FC<{ src: string; em: number; ate: number; x: number; y: number; rot: number; de?: number; lado: 1 | -1 }> = ({ src, em, ate, x, y, rot, de = 0, lado }) => {
  const { fps } = useVideoConfig();
  const t = useT();
  const k = clamp((t - em) / 0.45);
  const sai = clamp((t - ate + 0.2) / 0.2);
  const a = Math.round(em * fps);
  return (
    <Sequence from={a} durationInFrames={Math.max(1, Math.round(ate * fps) - a)} layout="none">
      <div style={{ position: "absolute", left: x, top: y, width: 470, height: 640, padding: 14, background: COR.papel, borderRadius: 18, boxShadow: "0 30px 70px rgba(0,0,0,.6)", transform: `translateX(${(1 - mola(k)) * 600 * lado}px) rotate(${rot}deg)`, opacity: 1 - sai, boxSizing: "border-box" }}>
        <div style={{ width: "100%", height: "100%", overflow: "hidden", borderRadius: 10 }}>
          <Video src={staticFile(src)} muted trimBefore={Math.round(de * fps)} objectFit="cover" style={{ width: "100%", height: "100%", filter: GRADE_VIDEO }} />
        </div>
      </div>
    </Sequence>
  );
};

// ------------------------------------------------------------------ composição

export const ReelFlorenca: React.FC<PropsFlorenca> = (p) => {
  const t = useT();
  const { fps } = useVideoConfig();
  if (!p.palavras.length) return <AbsoluteFill style={{ background: COR.fundo }} />;
  const W = (i: number) => p.palavras[i].t;
  const ref = p.voz_lufs;

  // marcos (palavras)
  const s2 = 3.3, s4 = 7.25, s5 = 9.15, s6 = 17.35, s7 = W(85) - 0.12, s8 = W(100) - 0.08, s9 = 28.75, s10 = W(130) - 0.02;
  const s11 = W(139) - 0.06, revela = W(175), s12 = W(178) - 0.1, s13 = W(199) - 0.27, s14 = s13 + 2.1, s15 = W(225), s16 = W(231) - 0.09;
  const placa = W(236) - 0.3;

  // câmera do mapa
  let cam: CameraMapa = { x: 540, y: 640, zoom: 1 };
  if (t >= s5 && t < s6 + 0.5) {
    const z = t < W(73) ? lerp(t, s5, W(73), 1.0, 1.08, (x) => x) : lerp(t, W(73), s6, 1.08, 1.14);
    cam = { x: 560, y: 640, zoom: z };
  } else if (t >= s11 && t < revela) {
    cam = { x: PONTOS.parada.x + 40, y: PONTOS.parada.y - 60, zoom: lerp(t, s11, revela, 2.3, 2.85, easeInOut) };
  } else if (t >= revela && t < s12) {
    cam = { x: lerp(t, revela, revela + 0.6, PONTOS.parada.x + 40, PONTOS.parada.x), y: lerp(t, revela, revela + 0.6, PONTOS.parada.y - 60, 300), zoom: lerp(t, revela, revela + 0.6, 2.85, 2.1) };
  } else if (t >= s12) {
    cam = { x: 600, y: 620, zoom: lerp(t, s12, s13, 1.02, 1.1, (x) => x) };
  }
  const agonia = t >= W(73) - 0.05 && t < s6 ? Math.max(0, Math.sin((t - W(73)) * 9)) : 0;

  const punches: [number, number, number][] = [...PUNCHES, [W(2) - 0.02, W(4), 1.05], [W(107) - 0.04, W(112), 1.1], [revela - 0.02, s12 - 0.1, 1.07], [W(193) - 0.03, W(199) - 0.3, 1.05]];
  const fundoEscuro = <AbsoluteFill style={{ background: `radial-gradient(90% 60% at 50% 30%, #2A251F 0%, ${COR.fundo} 70%)` }} />;

  return (
    <AbsoluteFill style={{ background: COR.fundo }}>
      {/* ---------- FUNDOS ---------- */}
      {/* S1 gancho: Duomo */}
      <Clipe src="acervo/5554.mp4" ini={0} fim={s2 + 0.4} zoom={p.rostos ? [1.08, 1.0] : [1.32, 1.24]} origem={p.rostos ? "50% 30%" : "50% 0%"} />
      {/* S2 último dia → S3 família */}
      <Clipe src={p.rostos ? "acervo/5939.mp4" : "acervo/5812.mp4"} ini={s2} fim={s4 + 0.25} de={p.rostos ? 1.5 : 6.0} zoom={[1.0, 1.08]} estilo={(tt) => ({ ...fusaoEntra(s2)(tt), ...(tt > W(17) ? { filter: `blur(${lerp(tt, W(17), W(17) + 0.5, 0, 14)}px) brightness(${lerp(tt, W(17), W(17) + 0.5, 1, 0.6)})` } : {}), ...(tt >= s4 ? chicoteSai(s4)(tt) : {}) })} />
      <Janela ini={s2} fim={s4 + 0.25}>
        <AbsoluteFill style={t >= s4 ? chicoteSai(s4)(t) : undefined}>
          {p.rostos ? (
            <>
              <Cartao src="acervo/5658.mp4" em={W(19) - 0.12} ate={s4 + 0.25} x={70} y={300} rot={-4} de={1.0} lado={-1} />
              <Cartao src="acervo/5808.mp4" em={W(22) - 0.14} ate={s4 + 0.25} x={540} y={350} rot={3.5} de={0.8} lado={1} />
            </>
          ) : (
            <div style={{ position: "absolute", left: 0, right: 0, top: 470, display: "flex", justifyContent: "center", gap: 26, transform: "scale(2.1)", transformOrigin: "50% 0" }}>
              {[W(17), W(19), W(19) + 0.1, W(19) + 0.2, W(22)].map((em, i) => (
                <Pessoa key={i} k={clamp((t - em + 0.06) / 0.35)} cor={i === 0 ? COR.ambar : COR.papel} />
              ))}
            </div>
          )}
        </AbsoluteFill>
      </Janela>
      {/* S4 saiu correndo: rua */}
      <Clipe src="acervo/5718.mp4" ini={s4} fim={s5 + 0.45} de={0.5} vel={1.35} zoom={[1.05, 1.15]} estilo={(tt) => (tt < s5 ? chicoteEntra(s4)(tt) : mergulhoSai(s5, "50%", "45%")(tt))} />
      {/* S5 mapa: rotas, obra, volta, perder o trem, agonia, ônibus */}
      <Janela ini={s5} fim={s6 + 0.5}>
        <AbsoluteFill style={t < s6 ? mergulhoEntra(s5)(t) : mergulhoSai(s6, "52%", "58%")(t)}>
          <Mapa t={t} camera={cam} fases={{ rotas: W(41) - 0.3, mudado: W(44), obra: W(51) - 0.06, google: W(57), perder: W(67), onibus: W(76) - 0.1, agonia: W(73) }} />
          <EtiquetaTrem t={t} t0={W(67) - 0.06} />
          <AbsoluteFill style={{ boxShadow: `inset 0 0 220px rgba(229,72,77,${0.55 * agonia})` }} />
        </AbsoluteFill>
      </Janela>
      {/* S6 ônibus + bilhete esquecido */}
      <Clipe src="acervo/5680.mp4" ini={s6} fim={s7 + 0.1} de={2.7} zoom={[1.1, 1.02]} estilo={(tt) => ({ ...mergulhoEntra(s6)(tt), ...(tt > s7 - 0.05 ? { filter: `brightness(${lerp(tt, s7 - 0.05, s7 + 0.1, 1, 0)})` } : {}) })} />
      <Janela ini={s6} fim={s7}>
        <Bilhete t={t} t0={W(80) - 0.12} risca={W(84)} />
      </Janela>
      {/* S7 Murphy */}
      <Janela ini={s7} fim={s8}>
        <AbsoluteFill style={{ opacity: clamp((t - s7) / 0.3) }}>
          {fundoEscuro}
          <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", fontFamily: TEXTO, fontWeight: 800, fontSize: 38, letterSpacing: 10, color: COR.ambar, opacity: clamp((t - W(89)) / 0.2) }}>MURPHY</div>
          <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center", fontFamily: "Anton", fontSize: 200, lineHeight: 1, color: COR.ambar, opacity: 0.35 * clamp((t - W(89)) / 0.3) }}>“</div>
          <Titulo t={t} top={540} alinhar="centro" impacto={W(97)} linhas={[
            { texto: "SE TEM ALGUMA COISA", em: W(90), tam: 92 },
            { texto: "PRA DAR ERRADO,", em: W(94), tam: 92 },
            { texto: "VAI DAR ERRADO.", em: W(97), tam: 132, cor: COR.alerta, peso: true },
          ]} />
        </AbsoluteFill>
      </Janela>
      {/* S8 fiscalização: porta, fiscais, carimbo; "vieram direto na gente" */}
      <Janela ini={s8} fim={s9}>
        <AbsoluteFill style={{ opacity: t > W(114) ? 1 - clamp((t - W(114) - 0.5) / 0.25) : 1 }}>
          <Fiscais t={t} abre={W(102) - 0.1} sobem={W(103) - 0.05} carimbo={W(106)} vem={W(107)} />
        </AbsoluteFill>
      </Janela>
      {/* S9 multa */}
      <Janela ini={s9} fim={s10}>
        {fundoEscuro}
        <Multa t={t} t0={s9} multa={W(119) - 0.05} quarenta={W(121) - 0.05} cada={W(123) - 0.05} passagem={W(129) - 0.05} />
      </Janela>
      {/* S10 15 minutos */}
      <Janela ini={s10} fim={s11}>
        {fundoEscuro}
        <Relogio t={t} t0={s10} varre={W(132)} />
        <Titulo t={t} top={840} alinhar="centro" linhas={[{ texto: "15 MINUTOS", em: W(132) - 0.04, tam: 120, cor: COR.ambar, peso: true }]} />
      </Janela>
      {/* S11 a pergunta → ironia → revelação da estação */}
      <Janela ini={s11} fim={s12 + 0.05}>
        <Mapa t={t} camera={cam} estacaoApagada rotuloEstacao={false} dessaturar={t < revela ? lerp(t, s11, W(166), 0.25, 0.6) : 0} fases={{ parada: s11, revela }} />
        <Titulo t={t} top={300} alinhar="centro" sai={W(166) - 0.1} linhas={[
          { texto: "QUAL O CAMINHO", em: W(152) - 0.04, tam: 104 },
          { texto: "MAIS RÁPIDO?", em: W(155) - 0.04, tam: 132, cor: COR.ambar, peso: true },
        ]} />
        <Titulo t={t} top={300} alinhar="centro" linhas={[
          { texto: "NA FRENTE", em: revela - 0.02, tam: 150, cor: COR.ambar, peso: true },
          { texto: "DA ESTAÇÃO", em: W(176) - 0.04, tam: 104 },
        ]} />
        <AbsoluteFill style={{ background: "black", opacity: t >= W(166) && t < revela ? lerp(t, W(166), W(171), 0, 0.45) : 0 }} />
      </Janela>
      {/* S12 a volta enorme · mais caro */}
      <Janela ini={s12} fim={s13 + 0.45}>
        <AbsoluteFill style={t >= s13 ? mergulhoSai(s13, "60%", "40%")(t) : undefined}>
          <Mapa t={t} camera={cam} fases={{ parada: s12 - 2, revela: s12 - 2, volta: W(181) }} />
          <Titulo t={t} top={860} alinhar="centro" sai={W(193) - 0.08} linhas={[{ texto: "UMA VOLTA ENORME", em: W(185) - 0.04, tam: 104, cor: COR.alerta, peso: true }]} />
          <Titulo t={t} top={860} alinhar="centro" linhas={[{ texto: "MAIS CARO", em: W(193) - 0.04, tam: 132, cor: COR.alerta, peso: true }]} />
        </AbsoluteFill>
      </Janela>
      {/* S13 o trem (se não fosse a multa) */}
      {p.rostos ? (
        <Clipe src="acervo/5986.mp4" ini={s13} fim={s14} de={0.5} zoom={[1.0, 1.06]} estilo={mergulhoEntra(s13)} />
      ) : (
        <Janela ini={s13} fim={s14}>
          <AbsoluteFill style={mergulhoEntra(s13)(t)}>
            <Mapa t={t} camera={{ x: 420, y: 330, zoom: lerp(t, s13, s14, 1.7, 1.85, (x) => x) }} fases={{ revela: s13 - 3, trem: s13 + 0.25 }} />
          </AbsoluteFill>
        </Janela>
      )}
      {/* S14 a dica */}
      <Clipe src={p.rostos ? "acervo/5591.mp4" : "acervo/5718.mp4"} ini={s14} fim={s15 + 0.25} de={p.rostos ? 1.0 : 3.5} zoom={[1.0, 1.08]} estilo={(tt) => (tt >= s15 ? chicoteSai(s15)(tt) : { filter: "brightness(0.85)" })} />
      <Janela ini={s14} fim={s15}>
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 55%)" }} />
        <Titulo t={t} top={300} linhas={[
          { texto: "DICA", em: s14, tam: 64, cor: COR.ambar },
          { texto: "CIDADE EM OBRA?", em: W(211) - 0.04, tam: 112 },
        ]} sai={W(218) - 0.2} />
        <Titulo t={t} top={300} linhas={[
          { texto: "PERGUNTAR PARA", em: W(218) - 0.04, tam: 104 },
          { texto: "ALGUÉM QUE É", em: W(220) - 0.04, tam: 104 },
          { texto: "DE LÁ", em: W(223) - 0.04, tam: 150, cor: COR.ambar, peso: true },
        ]} />
      </Janela>
      {/* S15 paga a passagem */}
      <Clipe src={p.rostos ? "acervo/5680.mp4" : "acervo/5554.mp4"} ini={s15} fim={s16 + 0.4} de={p.rostos ? 4.7 : 0.5} zoom={p.rostos ? [1.05, 1.12] : [1.3, 1.36]} origem={p.rostos ? "50% 40%" : "50% 0%"} estilo={(tt) => ({ ...chicoteEntra(s15)(tt), filter: "brightness(.8)" })} />
      <Janela ini={s15} fim={s16}>
        <Bilhete t={t} t0={W(226) - 0.1} ok={W(228)} />
      </Janela>
      {/* S16 Murphy de novo → CTA sobre a Ponte Vecchio */}
      <Clipe src="acervo/5812.mp4" ini={s16} fim={p.duracao} de={1.0} zoom={[1.0, 1.08]} estilo={fusaoEntra(s16, 0.4)} grade="saturate(0.95) contrast(1.05)" />

      {/* ---------- transições de luz ---------- */}
      <LuzDePassagem corte={revela} />
      <Clarao em={s12} />

      {/* ---------- base do Diego (assenta o recorte no fundo) ---------- */}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 52%, rgba(0,0,0,.5) 78%, rgba(0,0,0,.72) 100%)" }} />
      <Diego segs={p.segmentos} punches={punches} />

      {/* ---------- gancho ---------- */}
      <Janela ini={0} fim={s2 + 0.3}>
        <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,.25) 45%, rgba(0,0,0,0) 60%)" }} />
        <Titulo t={t} top={290} sai={s2 - 0.1} impacto={W(2)} linhas={[
          { texto: "LEVAMOS UMA", em: 0.04, tam: 104 },
          { texto: "MULTA", em: W(2) - 0.04, tam: 230, cor: COR.alerta, peso: true },
          { texto: "EM FLORENÇA", em: W(4) - 0.04, tam: 104 },
          { texto: "E FOI A MELHOR COISA", em: W(5) - 0.04, tam: 82, cor: COR.ambar },
          { texto: "QUE ACONTECEU.", em: W(10) - 0.04, tam: 82, cor: COR.ambar },
        ]} />
      </Janela>

      {/* ---------- CTA (DS V2) ---------- */}
      <Sequence from={Math.round(placa * fps)} layout="none">
        <Placa rotulo="MANDA PRA QUEM VAI PRA" destino="ITÁLIA" modulo="seta" tamanho="G" x={72} y={640} entrada={0} />
      </Sequence>

      <Legendas legendas={p.legendas} />
      <Grao opacidade={0.06} />

      {/* ---------- áudio ---------- */}
      <Audio src={staticFile(p.voz)} />
      <Efeito nome="impacto" em={W(2) - 0.03} rel={-4} ref={ref} />
      <Efeito nome="swish" em={s4 - 0.05} rel={-6} ref={ref} />
      <Efeito nome="arLongo" em={s5 - 0.1} rel={-6} ref={ref} />
      <Efeito nome="impacto" em={W(51) - 0.03} rel={-6} ref={ref} />
      <Efeito nome="impacto" em={W(67) - 0.03} rel={-8} ref={ref} />
      <Efeito nome="arLongo" em={s6 - 0.1} rel={-6} ref={ref} />
      <Efeito nome="impacto" em={W(84) - 0.02} rel={-6} ref={ref} />
      <Efeito nome="impacto" em={W(97) - 0.02} rel={-4} ref={ref} />
      <Efeito nome="impacto" em={W(106) - 0.02} rel={-4} ref={ref} />
      <Efeito nome="pagina" em={s9 + 0.05} rel={-8} ref={ref} />
      <Efeito nome="obturador" em={W(129) - 0.05} rel={-8} ref={ref} />
      <Efeito nome="riser" em={W(166) - 0.82} rel={-8} ref={ref} />
      <Efeito nome="impacto" em={revela - 0.02} rel={-4} ref={ref} />
      <Efeito nome="swish" em={s12 - 0.06} rel={-6} ref={ref} />
      <Efeito nome="arLongo" em={s13 - 0.1} rel={-6} ref={ref} />
      <Efeito nome="swish" em={s15 - 0.05} rel={-6} ref={ref} />
      <Som nome="clack" em={(placa + 0.267) * 1000} relDb={-6} refLufs={ref} />
    </AbsoluteFill>
  );
};

