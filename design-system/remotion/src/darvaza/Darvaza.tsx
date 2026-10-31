/**
 * Reel da cratera de Darvaza (reels/darvaza-cratera/) · tela dividida, na linguagem dos Reels do perfil nesse formato
 * (docs/FORMATOS_REELS.md). Camadas: imagem de apoio (foto do Commons, ilustração, mapa) · Diego (metade de baixo ou
 * tela cheia) · legendas · gancho · títulos · transições · CTA. O DS V2 aparece só no CTA final (placa + clack).
 * Tudo vem das props (reels/darvaza-cratera/scripts/cenas.py → _tmp/props.json): cenas ancoradas nas palavras.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { BrilhoMergulho, Clarao, DadosMapa, Envio, FotoFundo, GasEspalha, Linha, LuzPassagem, Mapa, Perfuracao, Fosforo, Titulo } from "./Graficos";
import { GRADE_FOTO, PALETA, TEXTO, TITULO, ease, easeInOut, lerp } from "./estilo";

type Palavra = { texto: string; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "foto" | "fala" | "anim" | "mapa";
  ini_q: number;
  fim_q: number;
  layout: "split" | "full";
  foto?: string;
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  tom?: "titulo" | "noite" | "natural";
  anim?: "perfuracao" | "gas" | "fosforo" | "gasfosforo";
  marcos?: Record<string, number>;
  desloc?: number;
  estatico?: boolean;
  titulo?: { linhas: Linha[]; centroY: number; sai?: number };
  apagar?: [number, number, number];
  zoom?: [number, number];
  punch?: { em: number; z: number };
  envio?: { entra: number; voa: number; x: number; y: number };
  mergulho?: { foco: [number, number]; dur: number };
  nasce?: boolean;
};
export type PropsDarvaza = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  rostoX: number;
  quadros: number;
  cenas: Cena[];
  gancho: { linhas: string[]; tamanhos: number[]; tempos: number[] }[];
  fimGancho: number;
  ganchoTopo: number;
  legendas: Grupo[];
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
  transicoes: { tipo: "luz" | "clarao" | "mergulho"; q: number }[];
  mapa: DadosMapa;
};

export const propsVaziasDarvaza: PropsDarvaza = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 800,
  rostoX: 600,
  quadros: 30,
  cenas: [],
  gancho: [],
  fimGancho: 0,
  ganchoTopo: 275,
  legendas: [],
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
  sfx: false,
  transicoes: [],
  mapa: { paises: [], darvaza: [0, 0] },
};

export const metadadosDarvaza: CalculateMetadataFunction<PropsDarvaza> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const FILTRO = {
  natural: "saturate(1.05) contrast(1.06)",
  noite: "saturate(1.08) contrast(1.1) brightness(0.92)",
  titulo: "saturate(0.95) contrast(1.08) brightness(0.62)",
};

const posicaoFala = (c: Cena): "cheia" | "baixo" | "fora" => (c.tipo === "fala" ? "cheia" : c.layout === "split" ? "baixo" : "fora");

/** Diego: um único vídeo contínuo (as falas decupadas), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsDarvaza; cena: Cena; t: number }> = ({ p, cena, t }) => {
  const pos = posicaoFala(cena);
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (pos === "cheia") {
    let z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    if (cena.punch && t >= cena.punch.em) z *= cena.punch.z; // corte de zoom (punch-in), seco
    video = { scale: String(z), transformOrigin: `${p.rostoX}px ${p.rostoY}px` };
  } else if (pos === "baixo") {
    const h = p.altura - p.costura;
    box = { top: p.costura, height: h };
    video = { translate: `0 ${Math.round(h * 0.42 - p.rostoY)}px` }; // rosto a 42% da metade de baixo
  }
  return (
    <div style={{ position: "absolute", left: 0, width: p.largura, overflow: "hidden", opacity: pos === "fora" ? 0 : 1, ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: p.altura, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: p.largura, height: p.altura }} />
      </div>
    </div>
  );
};

const Foto: React.FC<{ cena: Cena; w: number; h: number; t: number; dur: number }> = ({ cena, w, h, t, dur }) => {
  const kb = cena.kb ?? [1, 1.05];
  const foco = cena.foco ?? [0.5, 0.5];
  const fim = cena.foco_fim ?? foco;
  let z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  const fx = lerp(t, 0, dur, foco[0], fim[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], fim[1], easeInOut);
  let filtro = FILTRO[cena.tom ?? "natural"] ?? GRADE_FOTO;
  let ox = fx;
  let oy = fy;
  if (cena.apagar) filtro += ` brightness(${lerp(t, cena.apagar[0], cena.apagar[1], 1, cena.apagar[2], easeInOut)})`;
  if (cena.mergulho) {
    // mergulho: a câmera afunda no fogo, desfoca e clareia; o corte fica escondido no quadro mais claro
    const m = cena.mergulho;
    const k = lerp(t, dur - m.dur, dur, 0, 1, (x) => x * x * x);
    z *= 1 + 1.8 * k;
    ox = lerp(k, 0, 1, fx, m.foco[0], (x) => x);
    oy = lerp(k, 0, 1, fy, m.foco[1], (x) => x);
    filtro += ` blur(${16 * k}px) brightness(${1 + 0.9 * k})`;
  }
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <Img
        src={staticFile(cena.foto as string)}
        style={{ width: w, height: h, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, scale: String(z), transformOrigin: `${ox * 100}% ${oy * 100}%`, filter: filtro }}
      />
    </div>
  );
};

/** Imagem de apoio da cena (atrás do Diego, ou acima dele na tela dividida). */
const Apoio: React.FC<{ p: PropsDarvaza; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  const nasce = cena.nasce ? lerp(t, 0, 0.32, 1, 0, easeInOut) : 0;
  let conteudo: React.ReactNode = null;
  if (cena.tipo === "foto" && cena.foto) {
    conteudo = (
      <>
        <Foto cena={cena} w={p.largura} h={h} t={t} dur={dur} />
        {!split && !cena.titulo && (
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 900, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 50%, rgba(0,0,0,0.72) 100%)" }} />
        )}
      </>
    );
  } else if (cena.tipo === "anim") {
    const ta = t + (cena.desloc ?? 0);
    const m = cena.marcos ?? {};
    conteudo =
      cena.anim === "perfuracao" ? (
        <Perfuracao t={ta} m={m} altura={h} estatico={cena.estatico} />
      ) : cena.anim === "gas" ? (
        <GasEspalha t={ta} m={m} altura={h} />
      ) : cena.anim === "fosforo" ? (
        <Fosforo t={ta} m={m} altura={h} />
      ) : cena.anim === "gasfosforo" ? (
        // gás e fósforo na mesma cena: o fósforo entra por cima do gás que se espalha, sem corte no meio
        <>
          <GasEspalha t={ta} m={m} altura={h} />
          <Fosforo t={ta} m={m} altura={h} sobre />
        </>
      ) : null;
  } else if (cena.tipo === "mapa") {
    conteudo = <Mapa t={t} dados={p.mapa} m={cena.marcos ?? { pais: 0.4, ponto: 0.6 }} altura={h} />;
  }
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, scale: String(1 + 0.25 * nasce), filter: nasce > 0 ? `blur(${12 * nasce}px)` : undefined }}>{conteudo}</div>
      {cena.titulo && <Titulo t={t} linhas={cena.titulo.linhas} centroY={cena.titulo.centroY} sai={cena.titulo.sai} />}
    </div>
  );
};

/** Legenda: 1 a 4 palavras, Inter 800 66 px com sombra; palavra de destaque em âmbar. */
const Legenda: React.FC<{ p: PropsDarvaza; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  // no CTA a placa do DS ocupa até y ≈ 861: a legenda desce para o espaço entre a costura e a cabeça do Diego
  const y = posicaoFala(cena) === "baixo" ? (tS >= p.cta.ini ? p.costura + 70 : p.costura) : 1320;
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

/** Gancho: a 1ª frase falada em letras grandes na metade de cima, alinhada em x 72; cada linha entra quando é dita. */
const Gancho: React.FC<{ p: PropsDarvaza; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho) return null;
  const sai = lerp(tS, p.fimGancho - 0.12, p.fimGancho, 1, 0, (x) => x);
  const linha = (txt: string, tam: number, ini: number, k: number) => {
    const e = ini <= 0 ? 1 : ease(Math.min(1, Math.max(0, (tS - ini) / 0.16)));
    return (
      <div key={k} style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 1.02, color: PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
        {txt}
      </div>
    );
  };
  return (
    <div style={{ opacity: sai }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 240, height: p.costura - 240, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.42) 40%, rgba(0,0,0,0.7) 100%)" }} />
      <div style={{ position: "absolute", left: 72, right: 72, top: p.ganchoTopo, textShadow: "0 4px 30px rgba(0,0,0,0.5)" }}>
        {p.gancho.map((b, i) => (
          <React.Fragment key={i}>
            {i > 0 && <div style={{ height: 18 }} />}
            {b.linhas.map((l, k) => linha(l, b.tamanhos[k], b.tempos[k], i * 10 + k))}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

/** Grão de película do formato (6%, overlay); não é o grão do DS. */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-darvaza">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-darvaza)" />
  </svg>
);

export const ReelDarvaza: React.FC<PropsDarvaza> = (p) => {
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
          <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={20} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {cena.envio && <Envio t={t} m={cena.envio} x={cena.envio.x} y={cena.envio.y} />}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
      <Gancho p={p} tS={tS} />
      {p.transicoes.map((tr, i) =>
        tr.tipo === "luz" ? <LuzPassagem key={i} q={q} corte={tr.q} /> : tr.tipo === "clarao" ? <Clarao key={i} q={q} corte={tr.q} /> : <BrilhoMergulho key={i} q={q} corte={tr.q} fps={fps} />,
      )}
      {/* CTA: único lugar do Reel com o DS V2 (2.7: placa de direção com verbo + módulo de seta; Chegada; clack) */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada} />
        <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};

/** Capa (1080 × 1920): foto de fundo, título e o Diego embaixo; usada como still. */
export const CapaDarvaza: React.FC<{ foto: string; quadro: string; linhas: Linha[]; centroY: number; costura: number; rostoY: number }> = ({ foto, quadro, linhas, centroY, costura, rostoY }) => {
  const h = 1920 - costura;
  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      <div style={{ position: "absolute", left: 0, top: costura, width: 1080, height: h, overflow: "hidden" }}>
        <Img src={staticFile(quadro)} style={{ position: "absolute", left: 0, top: Math.round(h * 0.42 - rostoY), width: 1080, height: 1920 }} />
      </div>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: costura, overflow: "hidden" }}>
        <FotoFundo src={foto} w={1080} h={costura} filtro="saturate(1.08) contrast(1.1) brightness(0.8)" />
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.35) 60%, rgba(0,0,0,0.55) 100%)" }} />
        <Titulo t={9} linhas={linhas} centroY={centroY} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />
      <Grao q={0} />
    </AbsoluteFill>
  );
};
