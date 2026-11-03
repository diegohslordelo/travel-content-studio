/**
 * Reel "Primeiro dia em Amsterdam" (reels/amsterdam-primeiro-dia/) · formato TELA VERDE (Trello; docs/FORMATOS_TRELLO.md):
 * o Diego de hoje (gravação do quarto, recortado por IA) no canto inferior direito, e atrás dele a jornada do dia 1 com os
 * vídeos da viagem, na ordem da narração. Camadas: fundo (vídeos da viagem, ou a grade do dia no gancho e no CTA) ·
 * escurecimentos · Diego · Placar do DS (pedido do Diego para este Reel) · legenda · gancho · luz · CTA (placa do DS).
 * Tudo vem das props (reels/amsterdam-primeiro-dia/scripts/reel.py → _tmp/props.json), com as cenas ancoradas nas palavras.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Placa } from "../ds/Placa";
import { Placar, ValorPlacar } from "../ds/Placar";
import { EtiquetaValor } from "../ds/Cards";
import { Som } from "../ds/Som";
import { GRADE_VIDEO, PALETA, TEXTO, TITULO, clamp, ease, easeIn, lerp } from "./estilo";

type Entrada = "corte" | "chicote" | "mergulho" | "fusao";
type Cena = { id: string; ini_q: number; fim_q: number; ext_q: number; video: string; kb: [number, number]; entra: Entrada; sai?: "chicote" };
type Tile = { video: string; em_q: number };
type Grade = { ini_q: number; fim_q: number; tiles: Tile[]; mergulho_q?: number; brilho: number };
type Grupo = { palavras: { texto: string; destaque: boolean }[]; ini: number; fim: number };

export type PropsAMS = {
  fps: number;
  quadros: number;
  cenas: Cena[];
  grades: Grade[];
  diego: { x: number; y: number; w: number; h: number };
  legendaY: number;
  legendas: Grupo[];
  gancho: {
    linhas: string[];
    tamanhos: number[];
    tempos: number[];
    cores: (string | null)[];
    topos: number[];
    fim: number;
    placa?: { destino: string; entrada: number; saida: number };
  };
  placar: { valores: ValorPlacar[]; ligar: number };
  etiquetas: { ini: number; fim: number; euro: string; rotulo: string }[];
  etiqueta: { x: number; y: number; escala: number };
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
  transicoes: { tipo: "luz" | "clarao"; q: number }[];
};

export const propsVaziasAMS: PropsAMS = {
  fps: 30,
  quadros: 30,
  cenas: [],
  grades: [],
  diego: { x: 520, y: 924, w: 560, h: 996 },
  legendaY: 1080,
  legendas: [],
  gancho: { linhas: [], tamanhos: [], tempos: [], cores: [], topos: [], fim: 0 },
  placar: { valores: [], ligar: 0 },
  etiquetas: [],
  etiqueta: { x: 652, y: 262, escala: 0.6 },
  cta: { ini: 0, rotulo: "", destino: "", entrada: 0 },
  mix: { voz_lufs: -16, clack_db_rel: -6 },
  sfx: false,
  transicoes: [],
};

export const metadadosAMS: CalculateMetadataFunction<PropsAMS> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: 1080,
  height: 1920,
});

/** Uma cena da viagem em tela cheia (já recortada em 9:16, muda, SDR), com aproximação lenta e linear e a entrada/saída dela. */
const CenaViagem: React.FC<{ c: Cena }> = ({ c }) => {
  const q = useCurrentFrame(); // quadro dentro da cena
  const dur = c.fim_q - c.ini_q;
  let z = lerp(q, 0, dur, c.kb[0], c.kb[1], (x) => clamp(x));
  let tx = 0;
  let blur = 0;
  let op = 1;
  if (c.entra === "chicote" && q < 4) {
    const p = ease(q / 4);
    tx = (1 - p) * 420;
    blur = (1 - p) * 16;
  } else if (c.entra === "mergulho" && q < 9) {
    const p = ease(q / 9);
    z *= 1 + 0.16 * (1 - p);
    blur = 12 * (1 - p);
  } else if (c.entra === "fusao") {
    op = clamp(q / 9);
  }
  if (c.sai === "chicote" && q >= dur - 4 && q < dur) {
    const p = easeIn((q - (dur - 4)) / 4);
    tx = -p * 420;
    blur = p * 16;
  }
  return (
    <AbsoluteFill style={{ opacity: op, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, scale: String(z), translate: `${tx}px 0`, filter: `${GRADE_VIDEO}${blur > 0.2 ? ` blur(${blur.toFixed(1)}px)` : ""}` }}>
        <Video src={staticFile(c.video)} muted style={{ width: 1080, height: 1920 }} />
      </div>
    </AbsoluteFill>
  );
};

/** Um quadro da grade: entra com 5 quadros de opacidade e escala (86% → 100%). */
const QuadroGrade: React.FC<{ t: Tile; i: number; brilho: number }> = ({ t, i, brilho }) => {
  const e = ease(useCurrentFrame() / 5);
  return (
    <div style={{ position: "absolute", left: (i % 3) * 360, top: Math.floor(i / 3) * 640, width: 360, height: 640, overflow: "hidden", opacity: e, scale: String(0.86 + 0.14 * e) }}>
      <div style={{ position: "absolute", inset: 0, filter: `${GRADE_VIDEO} brightness(${brilho})` }}>
        <Video src={staticFile(t.video)} muted style={{ width: 360, height: 640 }} />
      </div>
      <div style={{ position: "absolute", inset: 0, boxShadow: "inset 0 0 0 3px rgba(11,10,9,0.9)" }} />
    </div>
  );
};

/** A grade do dia: 9 vídeos 360 × 640 que entram um a um (gancho: "isso é tudo"; CTA: a volta ao começo). No fim do
 * gancho a câmera mergulha no 1º quadro (o aeroporto), que vira a 1ª cena: a viagem começa de dentro da grade. */
const GradeDia: React.FC<{ g: Grade }> = ({ g }) => {
  const q = useCurrentFrame() + g.ini_q; // quadro do Reel
  let z = 1;
  let blur = 0;
  if (g.mergulho_q !== undefined && q >= g.mergulho_q) {
    const p = easeIn((q - g.mergulho_q) / (g.fim_q - g.mergulho_q));
    z = 1 + 2 * p; // o 1º quadro (360 × 640) chega a 1080 × 1920
    blur = 10 * p;
  }
  return (
    <AbsoluteFill style={{ background: PALETA.preto, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, scale: String(z), transformOrigin: "0px 0px", filter: blur > 0.2 ? `blur(${blur.toFixed(1)}px)` : undefined }}>
        {g.tiles.map((t, i) => (
          <Sequence key={i} from={t.em_q - g.ini_q} premountFor={20}>
            <QuadroGrade t={t} i={i} brilho={g.brilho} />
          </Sequence>
        ))}
      </div>
    </AbsoluteFill>
  );
};

/** Legenda do formato: 1 a 4 palavras, Inter 800 66 px com sombra, centrada em x 540; palavra de destaque em âmbar. */
const Legenda: React.FC<{ p: PropsAMS; tS: number }> = ({ p, tS }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const e = ease((tS - g.ini) / 0.12);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: p.legendaY,
        translate: "0 -50%",
        textAlign: "center",
        font: `800 66px ${TEXTO}`,
        lineHeight: 1.1,
        color: PALETA.branco,
        whiteSpace: "nowrap",
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

/** Gancho: a 1ª frase falada em letras grandes, alinhada em x 72; cada linha entra quando é dita (160 ms). */
const Gancho: React.FC<{ p: PropsAMS; tS: number }> = ({ p, tS }) => {
  const g = p.gancho;
  if (!g.linhas.length || tS >= g.fim) return null;
  const sai = lerp(tS, g.fim - 0.3, g.fim - 0.18, 1, 0, (x) => clamp(x));
  return (
    <div style={{ opacity: sai }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 1250, background: "linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.5) 55%, rgba(0,0,0,0) 100%)" }} />
      {g.linhas.map((l, k) => {
        const e = g.tempos[k] <= 0 ? 1 : ease((tS - g.tempos[k]) / 0.16);
        return (
          <div
            key={k}
            style={{
              position: "absolute",
              left: 72,
              right: 72,
              top: g.topos[k],
              font: `400 ${g.tamanhos[k]}px ${TITULO}`,
              lineHeight: 1.0,
              color: g.cores[k] ?? PALETA.branco,
              textShadow: "0 4px 30px rgba(0,0,0,0.55)",
              opacity: tS < g.tempos[k] ? 0 : e,
              translate: `0 ${(1 - e) * 24}px`,
            }}
          >
            {l}
          </div>
        );
      })}
    </div>
  );
};

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS.md, 3.2 e 10.4): luz quente desce, o corte fica no pico (≤ 85%, 4 quadros). */
const LuzPassagem: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte;
  let a = 0;
  if (d >= -5 && d < -2) a = lerp(d, -5, -2, 0.08, 0.85, (x) => clamp(x));
  else if (d >= -2 && d < 2) a = 0.85;
  else if (d >= 2 && d < 6) a = lerp(d, 2, 6, 0.85, 0, (x) => clamp(x));
  if (a <= 0) return null;
  const desce = clamp((d + 5) / 3);
  const recua = clamp((d - 2) / 4);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: a,
        mixBlendMode: "screen",
        background: `radial-gradient(ellipse ${1500 - 900 * recua}px ${2600 * desce - 1600 * recua}px at ${540 + 500 * recua}px ${-100 - 200 * recua}px, #FFE2B0 0%, #FFB45E 38%, rgba(226,120,40,0.6) 62%, rgba(0,0,0,0) 100%)`,
      }}
    />
  );
};

/** Clarão de volta: quadro superexposto que volta ao normal em 5 quadros. */
const Clarao: React.FC<{ q: number; corte: number }> = ({ q, corte }) => {
  const d = q - corte;
  if (d < 0 || d >= 5) return null;
  return <div style={{ position: "absolute", inset: 0, background: "#FFF6E8", opacity: 0.75 * (1 - d / 5), mixBlendMode: "screen" }} />;
};

/** Grão de película do formato (6%, overlay); não é o grão do DS. */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-ams">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-ams)" />
  </svg>
);

export const ReelAmsterdam1: React.FC<PropsAMS> = (p) => {
  const q = useCurrentFrame();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / p.fps;
  const ctaQ = Math.round(p.cta.ini * p.fps);
  const d = p.diego;
  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      {p.cenas.map((c) => (
        <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q + c.ext_q} premountFor={30} name={c.id}>
          <CenaViagem c={c} />
        </Sequence>
      ))}
      {p.grades.map((g, i) => (
        <Sequence key={`g${i}`} from={g.ini_q} durationInFrames={g.fim_q - g.ini_q} premountFor={30} name={`grade ${i}`}>
          <GradeDia g={g} />
        </Sequence>
      ))}
      {/* escurecimentos: topo (Placar) e base (legenda e recorte do Diego) */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 560, background: "linear-gradient(to bottom, rgba(0,0,0,0.38) 0%, rgba(0,0,0,0) 100%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 760, bottom: 0, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.42) 40%, rgba(0,0,0,0.55) 100%)" }} />
      {/* o Diego de hoje (quarto), recortado, no canto inferior direito; tamanho fixo, sem zoom */}
      <div style={{ position: "absolute", left: d.x, top: d.y, width: d.w, height: d.h, filter: "drop-shadow(0 10px 28px rgba(0,0,0,0.55))" }}>
        <OffthreadVideo src={staticFile("diego.webm")} transparent muted style={{ width: d.w, height: d.h }} />
      </div>
      <Grao q={q} />
      {/* Placar do Dia (DS V2, 2.5): hora de cada ponto e gasto acumulado do dia, como no vlog do YouTube */}
      {p.placar.valores.length > 0 && <Placar valores={p.placar.valores} ligar={p.placar.ligar} refLufs={p.mix.voz_lufs} som={false} />}
      {/* o que entrou no Placar: Etiqueta de valor do DS (2.6) ao lado dele, reduzida (pedido do Diego para este Reel) */}
      {p.etiquetas.map((e, i) => (
        <div key={i} style={{ position: "absolute", inset: 0, scale: String(p.etiqueta.escala), transformOrigin: `${p.etiqueta.x}px ${p.etiqueta.y}px` }}>
          <EtiquetaValor euro={e.euro} real="" rotulo={e.rotulo} ini={e.ini} fim={e.fim} x={p.etiqueta.x} y={p.etiqueta.y} />
        </div>
      ))}
      <Legenda p={p} tS={tS} />
      <Gancho p={p} tS={tS} />
      {p.gancho.placa && (
        // "primeiro dia" com o logotipo da marca: placa PRIMEIRO DIA → (DS V2, 2.1, variante Marca), x 72 · y 640, Chegada
        <Sequence from={0} durationInFrames={Math.round(p.gancho.fim * p.fps)} name="placa do logotipo (gancho)">
          <Placa destino={p.gancho.placa.destino} modulo="seta" entrada={p.gancho.placa.entrada} saida={p.gancho.placa.saida} />
        </Sequence>
      )}
      {p.transicoes.map((tr, i) => (tr.tipo === "luz" ? <LuzPassagem key={i} q={q} corte={tr.q} /> : <Clarao key={i} q={q} corte={tr.q} />))}
      {/* CTA: placa de direção do DS V2 (verbo + módulo de seta), Chegada e clack */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada} />
        <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};
