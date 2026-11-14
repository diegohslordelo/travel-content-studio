/**
 * Reel "A Disney de Paris está te obrigando a ir dois dias" (reels/disney-frozen/rev1) · tela verde + Diego inteiro.
 * Formato do Trello "Tela verde" (docs/FORMATOS_TRELLO.md): só o corpo do Diego aparece e, atrás dele, o que ele fala.
 * Não havia fundo verde: o recorte é por IA (RobustVideoMatting), como no Reel das greves.
 * Pedido do Diego (13/11/2026): misturar tela verde e ele inteiro; "É brincadeira, velho?" inteiro e em preto e branco;
 * legenda que colore a palavra que ele está falando (não a de entonação); prints do comentário e do site oficial;
 * fogos do castelo (acervo) e o show do Frozen.
 * Camadas: fundo da cena (vídeo, cartão com print ou tela dividida em dois) · Diego (recorte com alfa ou vídeo inteiro) ·
 * gancho · legenda · CTA. O DS V2 aparece só no CTA final (Placa + clack), decisão do Diego (28/10/2026).
 * Nenhum filtro sobre o Diego além da conversão HDR → SDR neutra; o preto e branco é pedido dele, só na cena "pb".
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Img,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Placa, Modulo } from "../ds/Placa";
import { Som } from "../ds/Som";
import { Fita } from "../paris/Graficos";
import {
  PALETA,
  SOMBRA_TEXTO,
  TEXTO,
  TITULO,
  clamp,
  ease,
  easeInOut,
} from "../paris/estilo";

/** Vídeo de apoio 1080 × 1920 posicionado: o ponto (u, v) do plano vai para (x, y) da tela, com escala s. */
type Plano = {
  arquivo: string;
  /** quadro parado e desfocado do mesmo plano, que cobre o que o plano deslocado deixa vazio */
  fundo?: string;
  s?: number;
  u?: number;
  v?: number;
  x?: number;
  y?: number;
  /** aproximação lenta e linear durante a cena (1 → zoom) */
  zoom?: number;
};
type Marca = { r: [number, number, number, number]; em: number };
type Cartao = {
  img: string;
  /** largura e altura do print (px do arquivo) */
  w0: number;
  h0: number;
  /** caixa do cartão na tela */
  x: number;
  y: number;
  w: number;
  entra: number;
  sai?: number;
  marcas?: Marca[];
  /** aproximação do print dentro do cartão a partir de "em" (centro cx, cy em px do print; escala s) */
  zoom?: { em: number; cx: number; cy: number; s: number };
  rotulo?: string;
};
type Painel = Plano & { img?: string; foco?: [number, number] };
type Fundo =
  | { tipo: "video"; plano: Plano; escurecer?: { ate: number } }
  | { tipo: "cartao"; plano?: Plano; img?: string; cartao: Cartao; escurecer?: { ate: number } }
  | {
      tipo: "dois";
      esq: Painel;
      dir: Painel;
      marcos: { cinza?: number; esq?: number; dir?: number };
    };
type Cena = {
  id: string;
  modo: "verde" | "inteiro";
  pb?: boolean;
  ini_q: number;
  fim_q: number;
  /** deslocamento vertical do recorte (px) nesta cena */
  desl?: number;
  fundo?: Fundo;
  fita?: { em: number; y: number; giro: number; lado: "esq" | "dir" }[];
};
type Palavra = { texto: string; ini: number; fim: number };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Bloco = { linhas: string[]; tamanhos: number[]; cores: string[]; tempos: number[]; ini: number };

export type PropsFrozen = {
  fps: number;
  largura: number;
  altura: number;
  quadros: number;
  cenas: Cena[];
  gancho: Bloco[];
  ganchoTopo: number;
  fimGancho: number;
  legendas: Grupo[];
  legendaY: number;
  cta: { ini: number; rotulo: string; destino: string; modulo: Modulo; entrada: number; x?: number; y?: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasFrozen: PropsFrozen = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  quadros: 30,
  cenas: [],
  gancho: [],
  ganchoTopo: 270,
  fimGancho: 0,
  legendas: [],
  legendaY: 1380,
  cta: { ini: 0, rotulo: "", destino: "", modulo: "seta", entrada: 0 },
  mix: { voz_lufs: -16, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosFrozen: CalculateMetadataFunction<PropsFrozen> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Grade do acervo noturno: só tira o rosa saturado do HDR convertido (FORMATOS_REELS 2). */
const GRADE = "saturate(0.85) contrast(1.05)";

/** Grão de película do formato, só no fundo (nunca sobre o Diego, pedido dele na Parte 2). */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-frozen">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-frozen)" />
  </svg>
);

/** Plano de vídeo 1080 × 1920 levado de (u, v) para (x, y) com escala s; o que sobra embaixo é o quadro desfocado. */
const PlanoVideo: React.FC<{ p: Plano; t: number; dur: number; w?: number; filtro?: string }> = ({ p, t, dur, w = 1080, filtro }) => {
  const s0 = p.s ?? 1;
  const s = s0 * (1 + ((p.zoom ?? 1) - 1) * clamp(t / dur));
  const u = p.u ?? 0.5;
  const v = p.v ?? 0.5;
  const x = p.x ?? w / 2;
  const y = p.y ?? 960;
  const tx = x - u * 1080 * s;
  const ty = y - v * 1920 * s;
  const W = 1080 * s;
  const H = 1920 * s;
  const borda = (dentro: boolean, dir: string, px: number) =>
    `linear-gradient(${dir}, ${dentro ? `transparent 0px, #000 ${px}px` : "#000 0px, #000 1px"})`;
  const mascara = [
    borda(ty + H < 1920 - 1, "to top", Math.round(H * 0.14)),
    borda(tx > 1, "to right", 160),
    borda(tx + W < w - 1, "to left", 160),
  ].join(", ");
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", filter: filtro }}>
      {p.fundo && (
        <Img
          src={staticFile(p.fundo)}
          style={{ position: "absolute", left: (w - 1080) / 2, top: 0, width: 1080, height: 1920, scale: "1.15", filter: `blur(28px) brightness(0.55) ${GRADE}` }}
        />
      )}
      <div
        style={{
          position: "absolute",
          left: tx,
          top: ty,
          width: 1080 * s,
          height: 1920 * s,
          // bordas suaves onde o plano deslocado não chega à beira da tela: ele funde no quadro desfocado, sem emenda
          maskImage: mascara,
          WebkitMaskImage: mascara,
          maskComposite: "intersect",
          WebkitMaskComposite: "source-in",
        }}
      >
        <Video src={staticFile(p.arquivo)} muted style={{ width: "100%", height: "100%", filter: GRADE }} />
      </div>
    </div>
  );
};

/** Print real num cartão claro (sombra e cantos de 20 px), entra caindo e pode sair para cima. Marca-texto âmbar nas células. */
const CartaoPrint: React.FC<{ c: Cartao; t: number }> = ({ c, t }) => {
  const e = ease((t - c.entra) / 0.38);
  if (e <= 0) return null;
  const sai = c.sai !== undefined ? easeInOut((t - c.sai) / 0.4) : 0;
  const esc = c.w / c.w0;
  const h = c.h0 * esc;
  let z = 1;
  let ox = 0;
  let oy = 0;
  if (c.zoom) {
    const ez = easeInOut((t - c.zoom.em) / 0.6);
    z = 1 + (c.zoom.s - 1) * ez;
    // mantém o ponto (cx, cy) do print no centro do cartão à medida que aproxima
    ox = (c.w0 / 2 - c.zoom.cx) * esc * (z - 1) * 1;
    oy = (c.h0 / 2 - c.zoom.cy) * esc * (z - 1) * 1;
  }
  return (
    <div
      style={{
        position: "absolute",
        left: c.x,
        top: c.y,
        width: c.w,
        height: h,
        borderRadius: 20,
        overflow: "hidden",
        background: "#FFFFFF",
        boxShadow: "0 18px 50px rgba(0,0,0,0.55)",
        opacity: e * (1 - sai),
        translate: `0 ${(1 - e) * -60 - sai * 220}px`,
        scale: String(0.94 + 0.06 * e),
        rotate: `${(1 - e) * -2}deg`,
      }}
    >
      <div style={{ position: "absolute", inset: 0, scale: String(z), translate: `${ox}px ${oy}px` }}>
        <Img src={staticFile(c.img)} style={{ position: "absolute", inset: 0, width: c.w, height: h }} />
        {(c.marcas ?? []).map((m, i) => {
          const em = easeInOut((t - m.em) / 0.35);
          if (em <= 0) return null;
          const [mx, my, mw, mh] = m.r;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: mx * esc,
                top: my * esc,
                width: mw * esc * em,
                height: mh * esc,
                background: "rgba(224,174,92,0.55)",
                mixBlendMode: "multiply",
                borderRadius: 4,
              }}
            />
          );
        })}
      </div>
      {c.rotulo && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            font: `800 40px ${TEXTO}`,
            color: "#5B5750",
            textAlign: "center",
            padding: 40,
          }}
        >
          {c.rotulo}
        </div>
      )}
    </div>
  );
};

/** Painel da tela em dois (castelo × Frozen): vídeo ou imagem, com o assunto fora do centro (o Diego fica na frente). */
const PainelDois: React.FC<{ p: Painel; lado: "esq" | "dir"; t: number; dur: number; cinza: number; luz: number }> = ({ p, lado, t, dur, cinza, luz }) => {
  const filtro = `grayscale(${cinza}) brightness(${0.55 + 0.45 * luz})`;
  return (
    <div style={{ position: "absolute", top: 0, bottom: 0, left: lado === "esq" ? 0 : 540, width: 540, overflow: "hidden" }}>
      {p.img ? (
        <Img
          src={staticFile(p.img)}
          style={{
            position: "absolute",
            inset: 0,
            width: 540,
            height: 1920,
            objectFit: "cover",
            objectPosition: `${(p.foco ?? [0.5, 0.3])[0] * 100}% ${(p.foco ?? [0.5, 0.3])[1] * 100}%`,
            filter: filtro,
          }}
        />
      ) : (
        <PlanoVideo p={{ ...p, x: p.x ?? 270 }} t={t} dur={dur} w={540} filtro={filtro} />
      )}
    </div>
  );
};

const FundoCena: React.FC<{ cena: Cena; fps: number }> = ({ cena, fps }) => {
  const q = useCurrentFrame();
  const t = q / fps;
  const dur = (cena.fim_q - cena.ini_q) / fps;
  const f = cena.fundo;
  if (!f) return null;
  let corpo: React.ReactNode = null;
  if (f.tipo === "video" || f.tipo === "cartao") {
    // escurece o fundo enquanto um cartão está na frente; volta ao normal quando ele sai
    const esc = f.escurecer ? 1 - easeInOut((t - f.escurecer.ate) / 0.4) : 0;
    corpo = (
      <>
        {f.plano && <PlanoVideo p={f.plano} t={t} dur={dur} filtro={esc > 0 ? `brightness(${1 - 0.5 * esc}) blur(${6 * esc}px)` : undefined} />}
        {f.tipo === "cartao" && f.img && (
          <Img src={staticFile(f.img)} style={{ position: "absolute", inset: 0, width: 1080, height: 1920, objectFit: "cover", scale: "1.1", filter: "blur(22px) brightness(0.45)" }} />
        )}
      </>
    );
  } else if (f.tipo === "dois") {
    const cinza = f.marcos.cinza !== undefined ? easeInOut((t - f.marcos.cinza) / 0.3) : 0;
    const ve = f.marcos.esq !== undefined ? easeInOut((t - f.marcos.esq) / 0.25) : 0;
    const vd = f.marcos.dir !== undefined ? easeInOut((t - f.marcos.dir) / 0.25) : 0;
    // "desiste" apaga os dois; "escolhe um dos dois" acende um de cada vez
    const ce = cinza * (1 - ve * (1 - vd));
    const cd = cinza * (1 - vd);
    corpo = (
      <>
        <PainelDois p={f.esq} lado="esq" t={t} dur={dur} cinza={ce} luz={1 - ce} />
        <PainelDois p={f.dir} lado="dir" t={t} dur={dur} cinza={cd} luz={1 - cd} />
        <div style={{ position: "absolute", left: 537, top: 0, width: 6, height: 1920, background: "rgba(0,0,0,0.55)" }} />
      </>
    );
  }
  return (
    <AbsoluteFill>
      {corpo}
      <Grao q={q} />
      {f.tipo === "cartao" && <CartaoPrint c={f.cartao} t={t} />}
    </AbsoluteFill>
  );
};

/** Diego recortado (tela verde): o mesmo vídeo das falas, com alfa, deslocado para baixo para abrir o fundo em cima. */
const DiegoVerde: React.FC<{ desl: number }> = ({ desl }) => (
  <div style={{ position: "absolute", left: 0, top: desl, width: 1080, height: 1920 }}>
    <OffthreadVideo src={staticFile("fala_alfa.webm")} transparent muted style={{ width: 1080, height: 1920 }} />
  </div>
);

/** Diego inteiro: o vídeo das falas sem recorte e sem filtro; preto e branco só onde ele pediu. */
const DiegoInteiro: React.FC<{ pb?: boolean }> = ({ pb }) => (
  <AbsoluteFill>
    <Video src={staticFile("fala.mp4")} muted style={{ width: 1080, height: 1920, filter: pb ? "grayscale(1)" : undefined }} />
  </AbsoluteFill>
);

/**
 * Legenda (pedido do Diego): Inter 800 66 px, branca, 1 a 4 palavras; as palavras aparecem quando são ditas e a que ele
 * está falando fica âmbar (a cor de destaque de sempre), em vez da palavra de entonação.
 */
const Legenda: React.FC<{ p: PropsFrozen; tS: number }> = ({ p, tS }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const e = ease((tS - g.ini) / 0.12);
  // palavra "atual": a última que já começou; fica âmbar até a próxima começar (ou até o fim dela + 0,25 s)
  let atual = -1;
  g.palavras.forEach((w, i) => {
    if (tS >= w.ini - 0.03) atual = i;
  });
  const acesa = atual >= 0 && tS < Math.max(g.palavras[atual].fim + 0.25, (g.palavras[atual + 1]?.ini ?? 0) - 0.03);
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
        color: PALETA.branco,
        textShadow: SOMBRA_TEXTO,
        scale: String(0.94 + 0.06 * e),
        opacity: e,
      }}
    >
      {g.palavras.map((w, i) => {
        const ap = ease((tS - (w.ini - 0.03)) / 0.08);
        return (
          <span
            key={i}
            style={{
              opacity: ap,
              color: i === atual && acesa ? PALETA.ambar : undefined,
              display: "inline-block",
              translate: `0 ${(1 - ap) * 10}px`,
            }}
          >
            {(i ? " " : "") + w.texto}
          </span>
        );
      })}
    </div>
  );
};

/** Gancho: a 1ª frase em letras grandes no alto, cada linha quando é dita (FORMATOS_REELS 4.1). */
const Gancho: React.FC<{ p: PropsFrozen; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho) return null;
  const bloco = [...p.gancho].reverse().find((b) => tS >= b.ini) ?? p.gancho[0];
  const cor = (c: string) => (c === "ambar" ? PALETA.ambar : c === "vermelho" ? PALETA.vermelho : PALETA.branco);
  return (
    <div style={{ position: "absolute", left: 72, right: 72, top: p.ganchoTopo, textShadow: "0 4px 30px rgba(0,0,0,0.65), 0 2px 0 rgba(0,0,0,0.35)" }}>
      {bloco.linhas.map((l, k) => {
        const ini = bloco.tempos[k];
        const e = ini <= 0 ? 1 : ease((tS - ini) / 0.16);
        return (
          <div
            key={`${bloco.ini}-${k}`}
            style={{ font: `400 ${bloco.tamanhos[k]}px ${TITULO}`, lineHeight: 1.02, color: cor(bloco.cores[k]), opacity: e, translate: `0 ${(1 - e) * 24}px` }}
          >
            {l}
          </div>
        );
      })}
    </div>
  );
};

export const ReelFrozen: React.FC<PropsFrozen> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / fps;
  const cena = p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ?? p.cenas[p.cenas.length - 1];
  const t = (q - cena.ini_q) / fps;
  const ctaQ = Math.round(p.cta.ini * fps);
  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      {p.cenas
        .filter((c) => c.modo === "verde")
        .map((c) => (
          <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={20} name={c.id}>
            <FundoCena cena={c} fps={fps} />
          </Sequence>
        ))}
      {cena.modo === "verde" && cena.fita && (
        <Fita t={t} faixas={cena.fita} />
      )}
      {cena.modo === "verde" ? <DiegoVerde desl={cena.desl ?? 0} /> : <DiegoInteiro pb={cena.pb} />}
      {cena.id === p.cenas[0].id && tS < p.fimGancho && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 80,
            height: 760,
            // começa transparente (sem borda visível) e escurece só atrás das linhas do gancho
            background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.42) 22%, rgba(0,0,0,0.22) 76%, rgba(0,0,0,0) 100%)",
          }}
        />
      )}
      <Gancho p={p} tS={tS} />
      <Legenda p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (placa de direção + módulo; Chegada; clack) */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo={p.cta.modulo} entrada={p.cta.entrada} x={p.cta.x} y={p.cta.y} />
        <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};
