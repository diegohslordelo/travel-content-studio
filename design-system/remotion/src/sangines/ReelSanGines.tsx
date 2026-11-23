/**
 * Reel da Chocolatería San Ginés (reels/san-gines/) · Narrado (Trello, formato 04): a voz do Diego gravada em 23/11/2026
 * sobre as imagens da viagem a Madrid (19 e 20/03/2026), em tela cheia. Segue o padrão de edição de todo vídeo
 * (CLAUDE.md, 12; primeiro uso na Disney): edição natural, legenda que acende palavra a palavra com a voz, imagens
 * estáveis e sem tratamento de cor, sem sombreado na base da tela, gancho em letras garrafais, keen no fim do gancho,
 * sem música. O DS V2 só entra no CTA final (placa + clack).
 *
 * Pedidos do Diego para este Reel (23/11/2026):
 * - gancho com uma animação que traduza a decepção, em 3 opções para ele aprovar (gancho.anim):
 *   "pb"     · a imagem perde a cor e escurece na palavra "decepção" (ideia dele);
 *   "queda"  · o texto entra reto e "DECEPÇÃO" despenca, solta de um lado; no fim a frase cai da tela (ideia dele);
 *   "apagao" · a luz do lugar pisca e apaga, como uma lâmpada que queima;
 *   "queda_pb" · a escolhida pelo Diego (23/11/2026): a queda do texto sobre a Puerta del Sol, com a imagem ficando P&B;
 *   o efeito de cor só vale no gancho, por pedido dele (exceção deste Reel, não regra);
 * - sem sombreado atrás do texto do gancho: só a imagem e as letras (a sombra nas letras fica, para ler);
 * - os vídeos do TikTok entram como prova ("a mais famosa", "imperdível"): cartões de vídeo que aparecem um a um, com clique.
 * Tudo vem das props (_tmp/props.json, gerado por reels/san-gines/scripts/reel.py).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { COR, TEXTO, TITULO, clamp01, ease, easeIn, lerp } from "../disney/estilo";

type Palavra = { t: string; i: number; f: number };
type Grupo = { p: Palavra[]; ini: number; fim: number };
type Cena = { id: string; ini_q: number; fim_q: number; video: string; kb: [number, number] };
type Cartao = { id: string; video: string; ini: number; fim: number; x: number; y: number; w: number; h: number; rot: number };
export type AnimGancho = "pb" | "queda" | "apagao" | "queda_pb";
export type PropsSanGines = {
  fps: number;
  largura: number;
  altura: number;
  quadros: number;
  cenas: Cena[];
  gancho: {
    anim: AnimGancho;
    topo: number;
    fim: number; // s: corte para a cena seguinte (pico do keen)
    decepcao: number; // s: início da palavra "decepção"
    linhas: { texto: string; tam: number; em: number; cor?: string | null; peso?: boolean }[];
  };
  cartoes: Cartao[];
  legendas: Grupo[];
  legendaY: number;
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasSanGines: PropsSanGines = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  quadros: 30,
  cenas: [],
  gancho: { anim: "pb", topo: 300, fim: 0, decepcao: 0, linhas: [] },
  cartoes: [],
  legendas: [],
  legendaY: 1320,
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosSanGines: CalculateMetadataFunction<PropsSanGines> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Opção "apagao": brilho da imagem depois de "decepção" (s desde o início da palavra). Pisca duas vezes e apaga até 30%. */
const brilhoApagao = (d: number) => {
  if (d < 0) return 1;
  const pisca: [number, number][] = [[0.0, 0.38], [0.07, 1.0], [0.13, 0.3], [0.21, 0.85], [0.27, 0.85]];
  for (let k = pisca.length - 1; k >= 0; k--) if (d >= pisca[k][0]) return d < 0.27 ? pisca[k][1] : lerp(d, 0.27, 0.62, 0.85, 0.3);
  return 1;
};

/** Filtro do gancho (só na cena do gancho): é a animação de decepção pedida pelo Diego, não tratamento de cor do vídeo. */
const filtroGancho = (p: PropsSanGines, tS: number) => {
  const g = p.gancho;
  const d = tS - g.decepcao;
  if (g.anim === "pb" || g.anim === "queda_pb") {
    const k = ease(d / 0.75);
    if (k <= 0) return undefined;
    return `grayscale(${k}) brightness(${1 - 0.42 * k}) contrast(${1 + 0.12 * k})`;
  }
  if (g.anim === "apagao") {
    const b = brilhoApagao(d);
    return b >= 0.999 ? undefined : `brightness(${b})`;
  }
  return undefined;
};

const CenaVideo: React.FC<{ p: PropsSanGines; c: Cena; gancho: boolean }> = ({ p, c, gancho }) => {
  const q = useCurrentFrame();
  const dur = (c.fim_q - c.ini_q) / p.fps;
  const t = q / p.fps;
  const z = lerp(t, 0, dur, c.kb[0], c.kb[1], clamp01);
  const filtro = gancho ? filtroGancho(p, (c.ini_q + q) / p.fps) : undefined;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* imagem do acervo sem tratamento de cor (Diego, 19/11/2026): só recorte, estabilização e aproximação */}
      <AbsoluteFill style={{ scale: String(z), filter: filtro }}>
        <Video src={staticFile(c.video)} muted style={{ width: p.largura, height: p.altura }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Legenda que acende com a voz: o grupo aparece branco e cada palavra fica âmbar quando é dita (CLAUDE.md, 12). */
const Legenda: React.FC<{ p: PropsSanGines; tS: number }> = ({ p, tS }) => {
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
        // sem sombreado na base da tela e sem caixa: só a sombra nas letras (Diego, 19/11/2026)
        textShadow: "0 2px 3px rgba(0,0,0,0.75), 0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.9), 0 0 40px rgba(0,0,0,0.45)",
        scale: String(0.94 + 0.06 * e),
        opacity: e,
        whiteSpace: "nowrap",
      }}
    >
      {g.p.map((w, i) => {
        const k = ease((tS - w.i + 0.02) / 0.08);
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

/** Mola amortecida de 0 a 1 (passa do ponto e volta), para a palavra que despenca e fica pendurada. */
const mola = (d: number, f = 2.2, amort = 5.5) => (d <= 0 ? 0 : 1 - Math.exp(-amort * d) * Math.cos(2 * Math.PI * f * d));

/**
 * Gancho: a 1ª frase falada em letras garrafais (Anton, x 72), cada linha entra quando é dita (como na Grand-Place).
 * Sem degradê e sem caixa atrás (pedido do Diego): só a sombra nas letras.
 */
const Gancho: React.FC<{ p: PropsSanGines; tS: number }> = ({ p, tS }) => {
  const g = p.gancho;
  if (!g.linhas.length || tS >= g.fim) return null;
  const queda = g.anim === "queda" || g.anim === "queda_pb";
  // "queda": a palavra de peso solta do lado direito 0,35 s depois de dita (gira no canto de baixo à esquerda e fica torta);
  // nos últimos 0,3 s antes do corte, a frase inteira cai da tela, com gravidade, e o corte fica no pico do keen
  const dPeso = tS - (g.decepcao + 0.35);
  const giroPeso = queda ? 11 * mola(dPeso) : 0;
  const dCai = tS - (g.fim - 0.3);
  const cai = queda && dCai > 0 ? 0.5 * 26000 * dCai * dCai : 0;
  // "pb" e "apagao": a frase some no corte (como a Grand-Place)
  const sai = queda ? 1 : lerp(tS, g.fim - 0.08, g.fim, 1, 0, clamp01);
  return (
    <div style={{ opacity: sai }}>
      <div style={{ position: "absolute", left: 72, right: 72, top: g.topo, textShadow: "0 3px 6px rgba(0,0,0,0.6), 0 6px 40px rgba(0,0,0,0.65), 0 0 80px rgba(0,0,0,0.35)" }}>
        {g.linhas.map((l, k) => {
          const e = l.em <= 0 ? 1 : ease((tS - l.em) / 0.16);
          // a linha abaixo da palavra que despenca é empurrada junto (não encosta na palavra torta)
          const kPeso = g.linhas.findIndex((x) => x.peso);
          const empurra = queda && kPeso >= 0 && k > kPeso ? 10 * giroPeso : 0;
          const caiLinha = queda && dCai > 0 ? cai * (1 + 0.18 * k) : 0;
          const giroQueda = queda && dCai > 0 ? (k % 2 ? -1 : 1) * Math.min(14, 60 * dCai) : 0;
          return (
            <div
              key={k}
              style={{
                font: `400 ${l.tam}px ${TITULO}`,
                lineHeight: 1.02,
                color: l.cor ?? COR.branco,
                opacity: e,
                width: "fit-content",
                transformOrigin: "8% 92%",
                translate: `0 ${(1 - e) * 24 + caiLinha + empurra + (l.peso ? 0.9 * giroPeso : 0)}px`,
                rotate: `${(l.peso ? giroPeso : 0) + giroQueda}deg`,
              }}
            >
              {l.texto}
            </div>
          );
        })}
      </div>
    </div>
  );
};

/**
 * Cartão de vídeo do TikTok (prova de que a churrería é "a mais famosa" e "imperdível"): o vídeo inteiro, mudo, com
 * cantos arredondados; entra com um "pop" (62% → 104% → 100% em 200 ms, no clique) e sai com os outros, descendo.
 */
const CartaoTikTok: React.FC<{ p: PropsSanGines; c: Cartao; tS: number }> = ({ p, c, tS }) => {
  const d = tS - c.ini;
  const s = d < 0.12 ? lerp(d, 0, 0.12, 0.62, 1.04) : lerp(d, 0.12, 0.2, 1.04, 1.0);
  const fora = tS - (c.fim - 0.18);
  const desce = fora > 0 ? 1400 * easeIn(fora / 0.18) : 0;
  return (
    <div
      style={{
        position: "absolute",
        left: c.x - c.w / 2,
        top: c.y - c.h / 2,
        width: c.w,
        height: c.h,
        rotate: `${c.rot}deg`,
        scale: String(s),
        translate: `0 ${desce}px`,
        opacity: clamp01(d / 0.05),
        borderRadius: 34,
        overflow: "hidden",
        boxShadow: "0 18px 50px rgba(0,0,0,0.55), 0 0 0 5px rgba(255,255,255,0.92)",
      }}
    >
      <Video src={staticFile(c.video)} muted style={{ width: c.w, height: c.h, objectFit: "cover" }} />
    </div>
  );
};

export const ReelSanGines: React.FC<PropsSanGines> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: COR.preto }} />;
  const tS = q / fps;
  const ctaQ = Math.round(p.cta.ini * fps);
  return (
    <AbsoluteFill style={{ background: COR.preto }}>
      {p.cenas.map((c, k) => (
        <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={30} name={c.id}>
          <CenaVideo p={p} c={c} gancho={k === 0} />
        </Sequence>
      ))}
      {p.cartoes.map((c) => (
        <Sequence key={c.id} from={Math.round(c.ini * fps)} durationInFrames={Math.max(1, Math.round((c.fim - c.ini) * fps))} premountFor={30} name={c.id}>
          <CartaoTikTok p={p} c={c} tS={tS} />
        </Sequence>
      ))}
      <Legenda p={p} tS={tS} />
      <Gancho p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (placa de direção com verbo + módulo de seta; Chegada; clack) */}
      {p.cta.rotulo && (
        <Sequence from={ctaQ} name="CTA (DS V2)">
          <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada} />
          <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
        </Sequence>
      )}
      <Audio src={staticFile("voz.wav")} />
      {p.sfx && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};
