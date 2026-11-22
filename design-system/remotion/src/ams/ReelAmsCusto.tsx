/**
 * Reel "Amsterdã é cara mesmo?" (reels/ams-custo/) · Narrado (Trello, formato 04): a voz do Diego gravada no quarto sobre as
 * imagens da viagem, em tela cheia. Mesma linguagem do Reel da Disney (padrão de edição do CLAUDE.md, seção 12): corte seco
 * na palavra, legenda que acende palavra a palavra com a voz, gancho em letras garrafais, imagens sem tratamento de cor.
 * Pedidos do Diego para este Reel (22/11/2026): parecer feito por ele, com o mínimo de animação; imagens sem efeito
 * nenhum (sem aproximação), o mais abertas possível e centralizadas; gancho só com as letras sobre o canal no fim de tarde;
 * a única "animação" é a notícia recortada, com o canal escurecido ao fundo enquanto ele fala dela.
 * Camadas: vídeos (um por cena, recortados em 9:16 por reels/ams-custo/scripts/reel.py) · notícia · legenda · gancho · CTA.
 * O DS V2 aparece só no CTA final (placa + clack). Tudo vem das props (_tmp/props.json).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { COR, TEXTO, TITULO, ease, lerp } from "./estilo";

type Palavra = { t: string; i: number; f: number };
type Grupo = { p: Palavra[]; ini: number; fim: number };
type Cena = { id: string; ini_q: number; fim_q: number; video: string };
export type PropsAms = {
  fps: number;
  largura: number;
  altura: number;
  quadros: number;
  cenas: Cena[];
  gancho: { topo: number; fim: number; linhas: { texto: string; tam: number; em: number; cor?: string | null }[] };
  noticia: { ini: number; fim: number; img: string; largura: number; topo: number; escuro: number };
  legendas: Grupo[];
  legendaY: number;
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasAms: PropsAms = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  quadros: 30,
  cenas: [],
  gancho: { topo: 300, fim: 0, linhas: [] },
  noticia: { ini: 0, fim: 0, img: "noticia.png", largura: 940, topo: 470, escuro: 0.55 },
  legendas: [],
  legendaY: 1320,
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosAms: CalculateMetadataFunction<PropsAms> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Imagem do acervo exatamente como está no Drive (sem cor, sem aproximação): só o recorte 9:16 feito no reel.py. */
const CenaVideo: React.FC<{ p: PropsAms; c: Cena }> = ({ p, c }) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <Video src={staticFile(c.video)} muted style={{ width: p.largura, height: p.altura }} />
  </AbsoluteFill>
);

/**
 * A notícia: o canal escurece (o vídeo continua andando por trás) e o recorte da página entra subindo 24 px; sai do mesmo
 * jeito quando ele termina de falar dela. Pedido do Diego (22/11/2026): "fundo escurecido, meio transparente, com o canal
 * de Amsterdã no fundo, e a notícia ali recortada enquanto eu tô falando".
 */
const Noticia: React.FC<{ p: PropsAms; tS: number }> = ({ p, tS }) => {
  const n = p.noticia;
  if (!n.fim || tS < n.ini - 0.01 || tS > n.fim + 0.3) return null;
  const entra = ease((tS - n.ini) / 0.3);
  const sai = 1 - ease((tS - n.fim) / 0.25);
  const k = Math.min(entra, sai);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `rgba(0,0,0,${n.escuro * k})` }} />
      <Img
        src={staticFile(n.img)}
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          marginInline: "auto", // centro geométrico do canvas (x 540), CLAUDE.md, 6
          top: n.topo,
          width: n.largura,
          opacity: k,
          translate: `0 ${(1 - k) * 24}px`,
          borderRadius: 18,
          boxShadow: "0 18px 50px rgba(0,0,0,0.55)",
        }}
      />
    </AbsoluteFill>
  );
};

/** Legenda que acende com a voz: o grupo (1 a 4 palavras) aparece branco e cada palavra fica âmbar quando é dita. */
const Legenda: React.FC<{ p: PropsAms; tS: number }> = ({ p, tS }) => {
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
        // sem sombreado na base da tela e sem caixa: só a sombra nas letras, que garante a leitura (CLAUDE.md, 12)
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
          <React.Fragment key={i}>
            {/* o espaço fica fora do span: dentro de um inline-block o espaço inicial some e as palavras grudam */}
            {i ? " " : null}
            <span style={{ color: k >= 1 ? COR.ambar : k <= 0 ? COR.branco : mistura(k), display: "inline-block", translate: `0 ${atual ? -3 : 0}px` }}>{w.t}</span>
          </React.Fragment>
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

/** Gancho: a 1ª frase falada em letras garrafais (Anton, x 72), cada linha entra quando é dita; sem nada atrás das letras. */
const Gancho: React.FC<{ p: PropsAms; tS: number }> = ({ p, tS }) => {
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

export const ReelAmsCusto: React.FC<PropsAms> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: COR.preto }} />;
  const tS = q / fps;
  const ctaQ = Math.round(p.cta.ini * fps);
  return (
    <AbsoluteFill style={{ background: COR.preto }}>
      {p.cenas.map((c) => (
        <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={30} name={c.id}>
          <CenaVideo p={p} c={c} />
        </Sequence>
      ))}
      <Noticia p={p} tS={tS} />
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
