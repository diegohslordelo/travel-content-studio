/**
 * Reel da Disney (reels/disney-atracoes/) · Narrado (Trello, formato 04): a voz do Diego gravada no quarto sobre as
 * imagens da viagem, em tela cheia. Pedido do Diego (19/11/2026): edição natural, como se ele soubesse editar, sem cara
 * de agência (nada de mosaico de vários quadros); legenda que acende palavra a palavra com a voz; imagens estáveis;
 * gancho em letras garrafais como no Reel da Grand-Place (Bruxelas). O DS V2 aparece só no CTA final (placa + clack).
 * Camadas: vídeos (um por cena, já estabilizados e recortados em 9:16 por reels/disney-atracoes/scripts/reel.py) ·
 * legenda · gancho · CTA. As imagens ficam como estão no Drive: sem grade de cor, grão, degradê ou tom (Diego, 19/11/2026). Tudo vem das props (_tmp/props.json).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Freeze, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { COR, TEXTO, TITULO, ease, easeIn, easeInOut, lerp } from "./estilo";

type Palavra = { t: string; i: number; f: number };
type Grupo = { p: Palavra[]; ini: number; fim: number };
type Transicao = "queda" | "chicote";
type Cena = {
  id: string;
  ini_q: number;
  fim_q: number;
  pre_q: number; // quadros de vídeo antes do início da cena (a transição de entrada começa antes do corte)
  video: string;
  kb: [number, number];
  entrada?: Transicao;
  congelar?: number; // segundos desde o início da cena
};
export type PropsDisney = {
  fps: number;
  largura: number;
  altura: number;
  quadros: number;
  cenas: Cena[];
  transDur: { queda: number; chicote: number };
  gancho: { topo: number; fim: number; linhas: { texto: string; tam: number; em: number; cor?: string | null }[] };
  legendas: Grupo[];
  legendaY: number;
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasDisney: PropsDisney = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  quadros: 30,
  cenas: [],
  transDur: { queda: 0.3, chicote: 0.24 },
  gancho: { topo: 300, fim: 0, linhas: [] },
  legendas: [],
  legendaY: 1320,
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosDisney: CalculateMetadataFunction<PropsDisney> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/**
 * Deslocamento da cena (px) e desfoque durante uma transição. A cena que entra com "queda" sobe de baixo (a câmera
 * despenca, como o elevador da Torre do Terror); com "chicote" ela entra pela direita (panorâmica rápida). A cena
 * anterior sai junto, pelo lado oposto. Fora da janela da transição: parado e nítido.
 */
const movimento = (tipo: Transicao, p: number, entrando: boolean, w: number, h: number) => {
  const k = tipo === "queda" ? easeIn(p) : easeInOut(p);
  const v = tipo === "queda" ? 3 * p * p : 1.5 * Math.sin(Math.PI * p); // velocidade relativa, para o desfoque
  const desfoque = Math.min(18, 16 * v);
  if (tipo === "queda") return { x: 0, y: entrando ? (1 - k) * h : -k * h, desfoque };
  return { x: entrando ? (1 - k) * w : -k * w, y: 0, desfoque };
};

const CenaVideo: React.FC<{ p: PropsDisney; c: Cena; prox?: Cena }> = ({ p, c, prox }) => {
  const q = useCurrentFrame(); // relativo ao início da Sequence (= ini_q - pre_q)
  const qCena = q - c.pre_q; // 0 no corte de entrada
  const dur = (c.fim_q - c.ini_q) / p.fps;
  const t = qCena / p.fps;
  let x = 0;
  let y = 0;
  let desfoque = 0;
  if (c.entrada && qCena < 0) {
    const d = p.transDur[c.entrada];
    const m = movimento(c.entrada, 1 + t / d, true, p.largura, p.altura);
    ({ x, y, desfoque } = m);
  }
  if (prox?.entrada) {
    const d = p.transDur[prox.entrada];
    const tFim = (c.fim_q - c.ini_q) / p.fps;
    if (t > tFim - d) {
      const m = movimento(prox.entrada, (t - (tFim - d)) / d, false, p.largura, p.altura);
      ({ x, y, desfoque } = m);
    }
  }
  const tKb = c.congelar != null ? Math.min(t, c.congelar) : t;
  const congelado = c.congelar != null && t >= c.congelar;
  // no congelamento, um corte de zoom seco (×1,05) deixa o "clique" visível mesmo num plano parado
  const z = lerp(tKb, 0, dur, c.kb[0], c.kb[1], (k) => Math.min(1, Math.max(0, k))) * (congelado ? 1.05 : 1);
  const qCongela = c.congelar != null ? Math.round(c.congelar * p.fps) + c.pre_q : 0;
  return (
    <AbsoluteFill style={{ overflow: "hidden", translate: `${x}px ${y}px`, filter: desfoque > 0.3 ? `blur(${desfoque}px)` : undefined }}>
      {/* imagem do acervo sem tratamento nenhum de cor (pedido do Diego, 19/11/2026): só recorte, estabilização e aproximação */}
      <AbsoluteFill style={{ scale: String(z) }}>
        <Freeze frame={qCongela} active={congelado}>
          <Video src={staticFile(c.video)} muted style={{ width: p.largura, height: p.altura }} />
        </Freeze>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Legenda que acende com a voz: o grupo (1 a 4 palavras) aparece branco e cada palavra fica âmbar quando é dita. */
const Legenda: React.FC<{ p: PropsDisney; tS: number }> = ({ p, tS }) => {
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
        padding: "0 90px",
        font: `800 66px ${TEXTO}`,
        lineHeight: 1.1,
        // sem degradê sobre a imagem: a leitura vem só da sombra das letras
        textShadow: "0 2px 3px rgba(0,0,0,0.75), 0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.9), 0 0 40px rgba(0,0,0,0.45)",
        scale: String(0.94 + 0.06 * e),
        opacity: e,
        whiteSpace: "nowrap",
      }}
    >
      {g.p.map((w, i) => {
        const k = ease((tS - w.i + 0.02) / 0.08); // acende em 80 ms, no início da palavra
        const atual = tS >= w.i && tS < w.f;
        return (
          <span key={i} style={{ color: k >= 1 ? COR.ambar : k <= 0 ? COR.branco : mistura(k), display: "inline-block", translate: `0 ${atual ? -3 : 0}px` }}>
            {(i ? " " : "") + w.t}
          </span>
        );
      })}
    </div>
  );
};

const mistura = (k: number) => {
  const a = [255, 255, 255];
  const b = [0xe0, 0xae, 0x5c];
  return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * k)).join(",")})`;
};

/** Gancho: a 1ª frase falada em letras garrafais (Anton, x 72), cada linha entra quando é dita (como na Grand-Place). */
const Gancho: React.FC<{ p: PropsDisney; tS: number }> = ({ p, tS }) => {
  const g = p.gancho;
  if (!g.linhas.length || tS >= g.fim) return null;
  const sai = lerp(tS, g.fim - 0.08, g.fim, 1, 0, (k) => Math.min(1, Math.max(0, k)));
  return (
    <div style={{ opacity: sai }}>
      <div style={{ position: "absolute", left: 72, right: 72, top: g.topo, textShadow: "0 3px 6px rgba(0,0,0,0.6), 0 6px 40px rgba(0,0,0,0.65), 0 0 80px rgba(0,0,0,0.35)" }}>
        {g.linhas.map((l, k) => {
          const e = l.em <= 0 ? 1 : ease((tS - l.em) / 0.16);
          return (
            <div key={k} style={{ font: `400 ${l.tam}px ${TITULO}`, lineHeight: 1.02, color: l.cor ?? COR.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
              {l.texto}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const ReelDisney: React.FC<PropsDisney> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: COR.preto }} />;
  const tS = q / fps;
  const ctaQ = Math.round(p.cta.ini * fps);
  return (
    <AbsoluteFill style={{ background: COR.preto }}>
      {p.cenas.map((c, k) => (
        <Sequence key={c.id} from={c.ini_q - c.pre_q} durationInFrames={c.fim_q - c.ini_q + c.pre_q} premountFor={30} name={c.id}>
          <CenaVideo p={p} c={c} prox={p.cenas[k + 1]} />
        </Sequence>
      ))}
      <Legenda p={p} tS={tS} />
      <Gancho p={p} tS={tS} />
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
