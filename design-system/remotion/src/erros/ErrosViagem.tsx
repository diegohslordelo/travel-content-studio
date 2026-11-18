/**
 * Reel "Erros de viagem" · tela dividida (reels/erros-de-viagem/rev1).
 * Camadas: imagem de apoio (foto ou animação sobre foto) · Diego (metade de baixo ou tela cheia) · costura ·
 * grão · legenda · gancho · CTA (DS V2: placa + clack, único lugar do DS, decisão do Diego de 28/10/2026).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import {
  AntesDuranteDepois,
  CartaoDica,
  Foto,
  LongeDeTudo,
  Marcos,
  NoPapel,
  NoticiaSerasa,
  OlhoFechado,
  PlacaValet,
  PulosDoGato,
  SeparadoRisco,
  TempoOuro,
  VinteDolares,
} from "./Animacoes";
import { PALETA, SOMBRA_TEXTO, TEXTO, TITULO, ease, lerp } from "./estilo";

type Palavra = { texto: string; ini: number; fim: number; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "gancho" | "foto" | "anim" | "dica" | "diego" | "cta";
  layout: "split" | "full";
  ini_q: number;
  fim_q: number;
  foto?: string;
  foto2?: string;
  kb?: [number, number];
  foco?: [number, number];
  anim?: string;
  marcos?: Marcos;
  zoom?: [number, number];
  dica?: { n: number; titulo: string[]; simbolo: "xis" | "carro" | "nenhum" };
  extra?: Record<string, unknown>;
};
type SomEv = { arquivo: string; em: number; ganho_db: number };
export type PropsErros = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  quadros: number;
  cenas: Cena[];
  imagens: Record<string, { arquivo: string }>;
  gancho: { txt: string; tam: number; em: number; destaque?: string }[];
  legendas: Grupo[];
  sons: SomEv[];
  cta: { ini: number; entrada_ms: number; rotulo: string; destino: string; clack_db_rel: number };
  voz_lufs: number;
  /** Só a camada de gráficos (fundo transparente, sem o Diego): a gravação entra crua por baixo, no ffmpeg (HDR intacto). */
  soGraficos?: boolean;
};

export const propsVaziasErros: PropsErros = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 470,
  quadros: 30,
  cenas: [],
  imagens: {},
  gancho: [],
  legendas: [],
  sons: [],
  cta: { ini: 0, entrada_ms: 200, rotulo: "", destino: "", clack_db_rel: -6 },
  voz_lufs: -14,
};

export const metadadosErros: CalculateMetadataFunction<PropsErros> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const img = (p: PropsErros, k?: string) => (k ? p.imagens[k]?.arquivo ?? "" : "");

/** Diego: um vídeo contínuo (os 10 blocos concatenados), na metade de baixo ou em tela cheia. */
const Diego: React.FC<{ p: PropsErros; cena: Cena; t: number }> = ({ p, cena, t }) => {
  const cheia = cena.tipo === "diego";
  const fora = cena.layout === "full" && !cheia;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (cheia) {
    const z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    video = { scale: String(z), transformOrigin: `540px ${p.rostoY}px` };
  } else {
    const h = p.altura - p.costura;
    box = { top: p.costura, height: h };
    video = { translate: `0 ${Math.round(h * 0.42 - p.rostoY)}px` };
  }
  return (
    <div style={{ position: "absolute", left: 0, width: p.largura, overflow: "hidden", opacity: fora ? 0 : 1, ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: p.altura, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: p.largura, height: p.altura }} />
      </div>
    </div>
  );
};

/** Foto do gancho (enviada pelo Diego, 620 × 430): largura toda da metade de cima, fundo com a própria foto desfocada. */
const GanchoFoto: React.FC<{ p: PropsErros; src: string; t: number; dur: number }> = ({ p, src, t, dur }) => {
  const z = lerp(t, 0, dur, 1.0, 1.05, (x) => x);
  const hImg = Math.round((p.largura * 430) / 620);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: p.costura, overflow: "hidden" }}>
      <Img src={staticFile(src)} style={{ position: "absolute", inset: 0, width: p.largura, height: p.costura, objectFit: "cover", filter: "blur(28px) brightness(0.55)", scale: "1.15" }} />
      <Img
        src={staticFile(src)}
        style={{ position: "absolute", left: 0, top: p.costura - hImg, width: p.largura, height: hImg, scale: String(z), transformOrigin: "70% 60%" }}
      />
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(90deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.45) 48%, rgba(0,0,0,0) 78%)" }} />
    </div>
  );
};

const Gancho: React.FC<{ p: PropsErros; tS: number }> = ({ p, tS }) => (
  <div style={{ position: "absolute", left: 72, top: 300, textShadow: "0 4px 30px rgba(0,0,0,0.5)" }}>
    {p.gancho.map((l, k) => {
      const e = l.em <= 0 ? 1 : ease((tS - l.em) / 0.16);
      if (tS < l.em) return null;
      const partes = l.destaque ? l.txt.split(l.destaque) : [l.txt];
      return (
        <div key={k} style={{ font: `400 ${l.tam}px ${TITULO}`, lineHeight: 0.98, color: PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
          {l.destaque ? (
            <>
              {partes[0]}
              <span style={{ color: PALETA.ambar }}>{l.destaque}</span>
              {partes[1]}
            </>
          ) : (
            l.txt
          )}
        </div>
      );
    })}
  </div>
);

/** Imagem de cima (split) ou de tela cheia (full) da cena. */
const Apoio: React.FC<{ p: PropsErros; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const w = p.largura;
  const h = cena.layout === "split" ? p.costura : p.altura;
  const m = cena.marcos ?? {};
  const src = img(p, cena.foto);
  const a = { w, h, t, dur, m, src };
  switch (cena.tipo) {
    case "gancho":
    case "cta":
      if (cena.tipo === "gancho") return <GanchoFoto p={p} src={src} t={t} dur={dur} />;
      return <Foto src={src} w={w} h={h} t={t} dur={dur + 2} kb={cena.kb} foco={cena.foco} />;
    case "foto":
      return <Foto src={src} w={w} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} />;
    case "dica":
      return <CartaoDica w={w} h={h} t={t} dur={dur} src={src} n={cena.dica!.n} titulo={cena.dica!.titulo} simbolo={cena.dica!.simbolo} foco={cena.foco} />;
    case "anim": {
      const ex = (cena.extra ?? {}) as Record<string, never>;
      switch (cena.anim) {
        case "serasa":
          return <NoticiaSerasa {...a} pagW={ex.pagW} linhas={ex.linhas} />;
        case "olho":
          return <OlhoFechado {...a} />;
        case "papel":
          return <NoPapel {...a} />;
        case "gato":
          return <PulosDoGato {...a} />;
        case "longe":
          return <LongeDeTudo {...a} />;
        case "tempo":
          return <TempoOuro {...a} srcOuro={img(p, cena.foto2)} />;
        case "valet":
          return <PlacaValet {...a} caixa={ex.caixa} />;
        case "vinte":
          return <VinteDolares {...a} />;
        case "separado":
          return <SeparadoRisco {...a} />;
        case "antes":
          return <AntesDuranteDepois {...a} />;
      }
      return null;
    }
  }
  return null;
};

/** Legenda do formato: Inter 800, 66 px, branco com 1 palavra em âmbar; y 900 na tela dividida, 1320 em tela cheia. */
const Legenda: React.FC<{ p: PropsErros; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
  if (cena.tipo === "gancho" || cena.tipo === "cta") return null;
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const y = cena.layout === "split" ? p.costura : 1320;
  const e = ease((tS - g.ini) / 0.12);
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
        textShadow: SOMBRA_TEXTO,
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

const Grao: React.FC<{ q: number; h?: number }> = ({ q, h = 1920 }) => (
  <svg width={1080} height={h} style={{ position: "absolute", left: 0, top: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-erros">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-erros)" />
  </svg>
);

export const ReelErrosViagem: React.FC<PropsErros> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: p.soGraficos ? "transparent" : PALETA.preto }} />;
  const tS = q / fps;
  const cena = p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ?? p.cenas[p.cenas.length - 1];
  const t = (q - cena.ini_q) / fps;
  const split = cena.layout === "split";
  const ctaQ = Math.round(p.cta.ini * fps);
  return (
    <AbsoluteFill style={{ background: p.soGraficos ? "transparent" : PALETA.preto }}>
      {!p.soGraficos && <Diego p={p} cena={cena} t={t} />}
      {p.cenas
        .filter((c) => c.tipo !== "diego")
        .map((c) => (
          <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={20} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      {cena.tipo !== "diego" && <Grao q={q} h={split ? p.costura : p.altura} />}
      <Legenda p={p} tS={tS} cena={cena} />
      {cena.tipo === "gancho" && <Gancho p={p} tS={tS} />}
      {p.sons.map((s, i) => (
        <Sequence key={i} from={Math.round(s.em * fps)} layout="none" name={`som ${s.arquivo}`}>
          <Audio src={staticFile(s.arquivo)} volume={Math.min(1, Math.pow(10, s.ganho_db / 20))} />
        </Sequence>
      ))}
      {/* CTA: único lugar do Reel com o DS V2 (placa de direção com verbo + módulo de seta; Chegada; clack) */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada_ms} />
        <Som nome="clack" em={p.cta.entrada_ms + 280} relDb={p.cta.clack_db_rel} refLufs={p.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
    </AbsoluteFill>
  );
};

