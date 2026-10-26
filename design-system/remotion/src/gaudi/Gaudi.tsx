/**
 * Reel do Gaudí · tela dividida (reel_gaudi/), no padrão do Reel "Casa de Anne Frank" (padrao.md).
 * Camadas: imagem de apoio (vídeo do acervo, foto ou animação) · Diego (tela cheia, metade de baixo ou desfocado
 * como fundo do cartão) · legendas · gancho · CTA. Cortes secos; o DS V2 aparece só no CTA final (Placa + clack).
 * Diferença registrada em relação ao Anne Frank: sem rótulo de crédito na tela (o pedido de 26/10/2026 proíbe texto,
 * nome ou data que não estejam na fala); os créditos ficam em creditos.md e na legenda do post.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { Comparar, Data, Fracao } from "./Graficos";
import { GRADE_FOTO, GRADE_VIDEO, PALETA, TEXTO, TITULO, ease, lerp } from "./estilo";

type Palavra = { texto: string; ini: number; fim: number; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "broll" | "foto" | "fala" | "anim";
  ini_q: number;
  fim_q: number;
  arquivo?: string;
  layout?: "full" | "split" | "card";
  kb?: [number, number];
  foco?: [number, number];
  foto?: string;
  anim?: "data" | "fracao" | "comparar";
  marcos?: Record<string, number>;
  zoom?: [number, number];
  texto?: string[];
  tom?: "escuro" | "pb" | "noite";
  fundo?: string;
  fotos?: [string, string];
  continua?: boolean; // o plano segue por baixo do CTA até o fim
};
export type PropsGaudi = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  quadros: number;
  cenas: Cena[];
  imagens: Record<string, { arquivo: string }>;
  gancho: { linhas: string[]; tamanhos: number[]; tempos: number[] }[];
  fimGancho: number;
  legendas: Grupo[];
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
};

export const propsVaziasGaudi: PropsGaudi = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 640,
  quadros: 30,
  cenas: [],
  imagens: {},
  gancho: [],
  fimGancho: 0,
  legendas: [],
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -10 },
};

export const metadadosGaudi: CalculateMetadataFunction<PropsGaudi> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const posicaoFala = (c: Cena): "cheia" | "baixo" | "fundo" | "fora" => {
  if (c.tipo === "fala") return "cheia";
  if (c.layout === "split") return "baixo";
  if (c.layout === "card") return "fundo";
  return "fora";
};

/** Diego: um único vídeo contínuo (as falas decupadas), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsGaudi; cena: Cena; t: number }> = ({ p, cena, t }) => {
  const pos = posicaoFala(cena);
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (pos === "cheia") {
    const z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    video = { scale: String(z), transformOrigin: `540px ${p.rostoY}px` };
  } else if (pos === "baixo") {
    const h = p.altura - p.costura;
    box = { top: p.costura, height: h };
    video = { translate: `0 ${Math.round(h * 0.42 - p.rostoY)}px` }; // rosto a 42% da metade de baixo
  } else if (pos === "fundo") {
    video = { scale: "1.15", filter: "blur(26px) grayscale(1) brightness(0.42)" };
  }
  return (
    <div style={{ position: "absolute", left: 0, width: p.largura, overflow: "hidden", opacity: pos === "fora" ? 0 : 1, ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: p.altura, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: p.largura, height: p.altura }} />
      </div>
    </div>
  );
};

const FILTROS = {
  escuro: "grayscale(0.85) brightness(0.55) contrast(1.1)",
  pb: "grayscale(1) contrast(1.08) brightness(0.92)",
  noite: "grayscale(1) brightness(0.4) contrast(1.2)", // foto clara em tela cheia: a legenda branca precisa de fundo escuro
};

const Foto: React.FC<{ src: string; w: number; h: number; t: number; dur: number; kb?: [number, number]; foco?: [number, number]; filtro?: string }> = ({
  src,
  w,
  h,
  t,
  dur,
  kb = [1, 1.05],
  foco = [0.5, 0.5],
  filtro = GRADE_FOTO,
}) => {
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <Img
        src={staticFile(src)}
        style={{
          width: w,
          height: h,
          objectFit: "cover",
          objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`,
          scale: String(z),
          transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`,
          filter: filtro,
        }}
      />
    </div>
  );
};

/** Imagem de apoio da cena (atrás do Diego, ou acima dele na tela dividida). */
const Apoio: React.FC<{ p: PropsGaudi; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps;
  const dur = ((cena.continua ? p.quadros : cena.fim_q) - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  if (cena.tipo === "broll" && cena.arquivo) {
    const z = cena.kb ? lerp(t, 0, dur, cena.kb[0], cena.kb[1], (x) => x) : 1;
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
        <div style={{ width: p.largura, height: h, scale: String(z), filter: cena.tom ? FILTROS[cena.tom] : GRADE_VIDEO }}>
          <Video src={staticFile(cena.arquivo)} muted style={{ width: p.largura, height: h }} />
        </div>
      </div>
    );
  }
  if (cena.tipo === "foto" && cena.foto) {
    const im = p.imagens[cena.foto];
    if (cena.layout === "card") {
      // cartão flutuante sobre o Diego desfocado (como no Reel Anne Frank)
      const e = ease(Math.min(1, t / 0.32));
      return (
        <div
          style={{
            position: "absolute",
            left: 140,
            top: 330,
            width: 800,
            height: 900,
            borderRadius: 20,
            overflow: "hidden",
            boxShadow: "0 30px 80px rgba(0,0,0,0.6)",
            opacity: e,
            scale: String(0.9 + 0.1 * e),
          }}
        >
          <Foto src={im.arquivo} w={800} h={900} t={t} dur={dur} kb={cena.kb ?? [1.0, 1.05]} foco={cena.foco ?? [0.5, 0.35]} filtro={cena.tom ? FILTROS[cena.tom] : GRADE_FOTO} />
        </div>
      );
    }
    return <Foto src={im.arquivo} w={p.largura} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} filtro={cena.tom ? FILTROS[cena.tom] : GRADE_FOTO} />;
  }
  if (cena.tipo === "anim") {
    const fundo = cena.fundo ? p.imagens[cena.fundo]?.arquivo : undefined;
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
        {cena.anim === "data" && <Data t={t} linhas={cena.texto ?? []} fundo={fundo} />}
        {cena.anim === "fracao" && <Fracao t={t} fundo={fundo} marco={cena.marcos?.quarto ?? 0.4} />}
        {cena.anim === "comparar" && cena.fotos && (
          <Comparar t={t} altura={h} a={p.imagens[cena.fotos[0]].arquivo} b={p.imagens[cena.fotos[1]].arquivo} marco={cena.marcos?.troca ?? 1} focoA={[0.5, 0.25]} focoB={[0.5, 0.3]} />
        )}
      </div>
    );
  }
  return null;
};

/** Legenda: 1 a 3 palavras, Inter 800 66 px com sombra; palavra de destaque em âmbar (padrão do Reel Anne Frank). */
const Legenda: React.FC<{ p: PropsGaudi; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const pos = posicaoFala(cena);
  const y = pos === "baixo" ? p.costura : pos === "fundo" ? 1375 : 1320;
  const e = ease(Math.min(1, (tS - g.ini) / 0.12));
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y,
        translate: "0 -50%",
        textAlign: "center",
        padding: "0 90px",
        font: `800 66px ${TEXTO}`,
        lineHeight: 1.1,
        color: PALETA.branco,
        textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)",
        scale: String(0.94 + 0.06 * e),
        opacity: e,
      }}
    >
      {g.palavras.map((w, i) => (
        <span key={i} style={{ color: w.destaque ? PALETA.ambar : undefined }}>
          {(i ? " " : "") + w.texto}
        </span>
      ))}
    </div>
  );
};

/** Gancho: a 1ª frase falada, em letras grandes, à esquerda sobre a imagem; cada linha entra quando é dita. */
const Gancho: React.FC<{ p: PropsGaudi; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho) return null;
  const linha = (txt: string, tam: number, ini: number, k: number) => {
    const e = ini <= 0 ? 1 : ease(Math.min(1, Math.max(0, (tS - ini) / 0.16)));
    return (
      <div key={k} style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 1.02, color: PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
        {txt}
      </div>
    );
  };
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 1250, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0.7) 100%)" }} />
      <div style={{ position: "absolute", left: 72, right: 72, top: 690, textShadow: "0 4px 30px rgba(0,0,0,0.45)" }}>
        {p.gancho.map((b, i) => (
          <React.Fragment key={i}>
            {i > 0 && <div style={{ height: 34 }} />}
            {b.linhas.map((l, k) => linha(l, b.tamanhos[k], b.tempos[k], i * 10 + k))}
          </React.Fragment>
        ))}
      </div>
    </>
  );
};

/** Grão de película próprio do Reel (não é o grão do DS). */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-gaudi">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-gaudi)" />
  </svg>
);

export const ReelGaudi: React.FC<PropsGaudi> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / fps;
  const cena = p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ?? p.cenas[p.cenas.length - 1];
  const t = (q - cena.ini_q) / fps;
  const split = cena.layout === "split" && cena.tipo !== "fala";
  const ctaQ = Math.round(p.cta.ini * fps);

  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      <Fala p={p} cena={cena} t={t} />
      {p.cenas
        .filter((c) => c.tipo !== "fala")
        .map((c) => (
          <Sequence key={c.id} from={c.ini_q} durationInFrames={(c.continua ? p.quadros : c.fim_q) - c.ini_q} premountFor={20} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
      <Gancho p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (2.7: placa de direção com verbo + módulo de seta; Chegada; clack) */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada} />
        <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
    </AbsoluteFill>
  );
};
