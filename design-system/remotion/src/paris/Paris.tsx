/**
 * Reel "Paris não quer você lá" · tela dividida (reels/paris-formigueiro/rev1).
 * Base: a composição do Reel de Bruges (mesmo formato), com o que as referências de tela dividida ensinam
 * (docs/REFERENCIA_EDICAO_FORMATOS.md, 10): empurrão da tela dividida para a tela cheia, clarão na volta para o rosto,
 * luz de passagem na ida, mergulho, palavra-chave em dupla tipografia, prova na tela (print) e animações próprias.
 * Camadas: Diego (vídeo contínuo das falas decupadas) · apoio (acervo, foto da web ou animação) · legenda · gancho · CTA.
 * O DS V2 aparece só no CTA final (Placa + clack), por decisão do Diego (28/10/2026).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Placa, Modulo } from "../ds/Placa";
import { Som } from "../ds/Som";
import {
  Calendario,
  Fita,
  Gato,
  Lista,
  Mapa9,
  MapaParis,
  NumeroDica,
  Ranking,
} from "./Graficos";
import {
  GRADE_FOTO,
  GRADE_VIDEO,
  PALETA,
  SERIFA,
  SOMBRA_TEXTO,
  TEXTO,
  TITULO,
  clamp,
  comOrdinal,
  ease,
  easeInOut,
  lerp,
} from "./estilo";

type Palavra = { texto: string; ini: number; fim: number; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "broll" | "foto" | "fala" | "anim";
  ini_q: number;
  fim_q: number;
  extra_q?: number;
  arquivo?: string;
  layout?: "full" | "split" | "card";
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  foto?: string;
  foto2?: string;
  kb2?: [number, number];
  foco2?: [number, number];
  selo?: string;
  selo2?: string;
  anim?: "ranking" | "lista" | "gato" | "mapa9";
  print?: string;
  itens?: {
    foto: string;
    linhas: string[];
    em: string;
    foco?: [number, number];
  }[];
  fita?: { em: string; y: number; giro: number; lado: "esq" | "dir" }[];
  numero?: number;
  /** foto encaixada pela largura e apoiada na costura (não corta o topo; o que sobra em cima fica sob a interface) */
  aspecto?: number;
  /** grade de cor própria do plano (ex.: pôr do sol que a grade padrão apagaria) */
  grade?: string;
  calendario?: boolean;
  origem?: [number, number];
  marcos?: Record<string, number>;
  zoom?: [number, number];
  zoom2?: number;
  transicao?: Transicao;
  saida?: Transicao | null;
  letreiro?: { texto: string; tam: number; em: number; cor?: string }[];
};
/** Transição de entrada de uma cena (REV3: uma em cada troca, escolhida pelo sentido da troca). */
type Transicao =
  | "empurrao"
  | "queda"
  | "clarao"
  | "luz"
  | "whip"
  | "dissolve"
  | "zoom"
  | "mergulho";
type Bloco = {
  linhas: string[];
  tamanhos: number[];
  cores: string[];
  tempos: number[];
  ini: number;
};
type Chave = {
  ini: number;
  fim: number;
  tipo?: "local";
  linhas: {
    texto: string;
    estilo: "titulo" | "serifa" | "rotulo";
    em: string;
  }[];
};
export type PropsParis = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  quadros: number;
  cenas: Cena[];
  imagens: Record<string, { arquivo: string }>;
  gancho: Bloco[];
  fimGancho: number;
  ganchoLayout: { split: boolean; topo: number };
  legendas: Grupo[];
  chaves: (Chave & { tempos?: number[] })[];
  mapa9: MapaParis;
  cta: {
    ini: number;
    rotulo: string;
    destino: string;
    modulo: Modulo;
    entrada: number;
  };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasParis: PropsParis = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 680,
  quadros: 30,
  cenas: [],
  imagens: {},
  gancho: [],
  fimGancho: 0,
  ganchoLayout: { split: true, topo: 275 },
  legendas: [],
  chaves: [],
  mapa9: { w: 1080, h: 900, distritos: [] },
  cta: { ini: 0, rotulo: "", destino: "", modulo: "seta", entrada: 0 },
  mix: { voz_lufs: -16, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosParis: CalculateMetadataFunction<PropsParis> = ({
  props,
}) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const EMPURRAO = 0.63; // s (≈ 19 quadros, referência 1)

const posicaoFala = (c: Cena): "cheia" | "baixo" | "fundo" | "fora" => {
  if (c.tipo === "fala") return "cheia";
  if (c.layout === "split") return "baixo";
  if (c.layout === "card") return "fundo";
  return "fora";
};

/** Diego: um único vídeo contínuo (as falas decupadas), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsParis; cena: Cena; t: number }> = ({
  p,
  cena,
  t,
}) => {
  const pos = posicaoFala(cena);
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const hBaixo = p.altura - p.costura;
  const desl = Math.round(hBaixo * 0.42 - p.rostoY); // rosto a 42% da metade de baixo
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (pos === "cheia") {
    let z = cena.zoom
      ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x)
      : 1;
    if (cena.zoom2 && cena.marcos?.zoom !== undefined && t >= cena.marcos.zoom)
      z = cena.zoom2; // corte de zoom
    if (cena.transicao === "empurrao" && t < EMPURRAO) {
      // a metade de baixo cresce até a tela cheia
      const e = easeInOut(t / EMPURRAO);
      const top = p.costura * (1 - e);
      box = { top, height: p.altura - top };
      video = { translate: `0 ${Math.round(desl * (1 - e))}px` };
    } else {
      video = { scale: String(z), transformOrigin: `540px ${p.rostoY}px` };
    }
  } else if (pos === "baixo") {
    box = { top: p.costura, height: hBaixo };
    video = { translate: `0 ${desl}px` };
  } else if (pos === "fundo") {
    video = {
      scale: "1.15",
      filter: "blur(26px) grayscale(1) brightness(0.42)",
    };
  }
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        width: p.largura,
        overflow: "hidden",
        opacity: pos === "fora" ? 0 : 1,
        ...box,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: p.largura,
          height: p.altura,
          ...video,
        }}
      >
        <Video
          src={staticFile("fala.mp4")}
          muted
          style={{ width: p.largura, height: p.altura }}
        />
      </div>
    </div>
  );
};

const Foto: React.FC<{
  src: string;
  w: number;
  h: number;
  t: number;
  dur: number;
  kb?: [number, number];
  foco?: [number, number];
  focoFim?: [number, number];
  filtro?: string;
}> = ({
  src,
  w,
  h,
  t,
  dur,
  kb = [1, 1.05],
  foco = [0.5, 0.5],
  focoFim,
  filtro = GRADE_FOTO,
}) => {
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  const fim = focoFim ?? foco;
  const fx = lerp(t, 0, dur, foco[0], fim[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], fim[1], easeInOut);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: w,
        height: h,
        overflow: "hidden",
        background: PALETA.preto,
      }}
    >
      <Img
        src={staticFile(src)}
        style={{
          width: w,
          height: h,
          objectFit: "cover",
          objectPosition: `${fx * 100}% ${fy * 100}%`,
          scale: String(z),
          transformOrigin: `${fx * 100}% ${fy * 100}%`,
          filter: filtro,
        }}
      />
    </div>
  );
};

/** Selo discreto que diferencia representação artística, gravura e registro histórico de foto atual (pedido do Diego). */
const Selo: React.FC<{ texto: string; x: number; y: number; t: number }> = ({
  texto,
  x,
  y,
  t,
}) => {
  const e = ease((t - 0.1) / 0.25);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        padding: "9px 16px 8px",
        borderRadius: 8,
        background: "rgba(11,10,9,0.72)",
        border: `2px solid ${PALETA.ambar}`,
        font: `700 25px ${TEXTO}`,
        letterSpacing: "0.14em",
        color: PALETA.ambar,
        opacity: e,
        translate: `0 ${(1 - e) * 10}px`,
      }}
    >
      {texto}
    </div>
  );
};

/** Quadros de entrada de cada transição (a saída usa o extra_q que o preparar.py dá à cena que sai). */
const ENTRADA_Q: Partial<Record<Transicao, number>> = {
  whip: 8,
  zoom: 12,
  mergulho: 14,
};
const DESLOC_WHIP = 420; // px: chicote lateral (o "arrasto" refeito sem a cor do DS)

/**
 * Invólucro de transição da imagem de apoio. A cena que sai continua extra_q quadros por cima da que entra
 * e sai com o movimento da transição; a que entra faz o movimento complementar. Tipos:
 * - whip: chicote lateral com desfoque direcional (as duas cenas andam juntas para a esquerda);
 * - dissolve: a cena que sai some por cima da que entra;
 * - zoom: a que sai cresce e desfoca, a que entra assenta de 122% para 100%;
 * - mergulho: a câmera entra na capela de cima do desenho e encontra a próxima imagem;
 * - empurrao: a metade de cima sai pelo topo (o Diego cresce até a tela cheia).
 */
const Apoio: React.FC<{ p: PropsParis; cena: Cena }> = ({ p, cena }) => {
  const q = useCurrentFrame();
  const durQ = cena.fim_q - cena.ini_q;
  let estilo: React.CSSProperties = {};
  let blurX = 0;
  let z = 1;
  const eQ = cena.transicao ? ENTRADA_Q[cena.transicao] : undefined;
  if (eQ && q < eQ) {
    const e = easeInOut(q / eQ);
    if (cena.transicao === "whip") {
      estilo = {
        translate: `${(1 - e) * DESLOC_WHIP}px 0`,
        opacity: Math.min(1, 0.2 + e * 1.4),
      };
      blurX = (1 - e) * 38;
    } else if (cena.transicao === "zoom") {
      estilo = {
        scale: String(1.22 - 0.22 * e),
        opacity: e,
        filter: `blur(${(1 - e) * 14}px)`,
      };
    } else if (cena.transicao === "mergulho") {
      estilo = {
        scale: String(1.08 - 0.08 * e),
        filter: `blur(${(1 - e) * 8}px)`,
      };
    }
  }
  if (q >= durQ && cena.extra_q) {
    const k = clamp((q - durQ) / cena.extra_q);
    const e = easeInOut(k);
    z = 2;
    if (cena.saida === "whip") {
      estilo = { translate: `${-e * DESLOC_WHIP}px 0`, opacity: 1 - e };
      blurX = e * 38;
    } else if (cena.saida === "dissolve") {
      estilo = { opacity: 1 - e };
    } else if (cena.saida === "zoom") {
      estilo = {
        scale: String(1 + 0.5 * e),
        opacity: 1 - e,
        filter: `blur(${e * 16}px)`,
        transformOrigin: "540px 760px",
      };
    } else if (cena.saida === "mergulho") {
      estilo = {
        scale: String(1 + 1.9 * k * k),
        opacity: 1 - clamp((k - 0.35) / 0.65),
        filter: `blur(${e * 18}px)`,
        transformOrigin: cena.origem
          ? `${cena.origem[0]}px ${cena.origem[1]}px`
          : "540px 620px",
      };
    } else if (cena.saida === "empurrao") {
      estilo = { translate: `0 ${-p.costura * e}px` };
    }
  }
  const filtroId = `mb-${cena.id}`;
  return (
    <div style={{ position: "absolute", inset: 0, zIndex: z }}>
      {blurX > 0.5 && (
        <svg width={0} height={0} style={{ position: "absolute" }}>
          <filter id={filtroId} x="-20%" y="0" width="140%" height="100%">
            <feGaussianBlur stdDeviation={`${blurX.toFixed(1)} 0`} />
          </filter>
        </svg>
      )}
      <div
        style={{
          position: "absolute",
          inset: 0,
          ...estilo,
          ...(blurX > 0.5 ? { filter: `url(#${filtroId})` } : {}),
        }}
      >
        <ApoioConteudo p={p} cena={cena} />
      </div>
    </div>
  );
};

/** Letreiro grande na metade de cima, linha a linha no tempo da fala ("DESDE A / IDADE MÉDIA"). */
const Letreiro: React.FC<{
  linhas: NonNullable<Cena["letreiro"]>;
  t: number;
  altura: number;
}> = ({ linhas, t, altura }) => (
  <>
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: 0,
        height: altura,
        background:
          "linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0.25) 100%)",
        opacity: ease((t - linhas[0].em + 0.2) / 0.3),
      }}
    />
    <div
      style={{
        position: "absolute",
        left: 72,
        right: 72,
        top: 300,
        textShadow: "0 4px 30px rgba(0,0,0,0.55)",
      }}
    >
      {linhas.map((l, i) => {
        const e = ease((t - l.em) / 0.18);
        return (
          <div
            key={i}
            style={{ overflow: "hidden", paddingTop: 30, marginTop: -30 }}
          >
            <div
              style={{
                font: `400 ${l.tam}px ${TITULO}`,
                lineHeight: 1.0,
                color:
                  l.cor === "ambar"
                    ? PALETA.ambar
                    : l.cor === "vermelho"
                      ? PALETA.vermelho
                      : PALETA.branco,
                translate: `0 ${(1 - e) * 100}%`,
                opacity: e > 0 ? 1 : 0,
              }}
            >
              {comOrdinal(l.texto)}
            </div>
          </div>
        );
      })}
    </div>
  </>
);

/** Camadas por cima da imagem de apoio: fita do gancho, letreiro, número da dica e calendário. */
const Sobreposicoes: React.FC<{
  p: PropsParis;
  cena: Cena;
  t: number;
  h: number;
}> = ({ cena, t, h }) => {
  const m = cena.marcos ?? {};
  return (
    <>
      {cena.fita && (
        <Fita
          t={t}
          faixas={cena.fita.map((f, i) => ({ ...f, em: m[`fita${i}`] ?? 0 }))}
        />
      )}
      {cena.calendario && <Calendario t={t} marcos={m} />}
      {cena.letreiro && <Letreiro linhas={cena.letreiro} t={t} altura={h} />}
      {cena.numero !== undefined && (
        <NumeroDica t={t} em={m.numero ?? 0} n={cena.numero} />
      )}
      {cena.selo && <Selo texto={cena.selo} x={72} y={290} t={t} />}
    </>
  );
};

/** Imagem de apoio da cena (acima do Diego na tela dividida ou em tela cheia). */
const ApoioConteudo: React.FC<{ p: PropsParis; cena: Cena }> = ({
  p,
  cena,
}) => {
  const t = useCurrentFrame() / p.fps;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  const degrade = !split && (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 0,
        height: 960,
        background:
          "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.62) 100%)",
      }}
    />
  );
  let conteudo: React.ReactNode = null;
  if (cena.tipo === "broll" && cena.arquivo) {
    const z = cena.kb ? lerp(t, 0, dur, cena.kb[0], cena.kb[1], (x) => x) : 1;
    conteudo = (
      <div
        style={{
          width: p.largura,
          height: h,
          scale: String(z),
          filter: cena.grade ?? GRADE_VIDEO,
        }}
      >
        <Video
          src={staticFile(cena.arquivo)}
          muted
          style={{ width: p.largura, height: h }}
        />
      </div>
    );
  } else if (cena.tipo === "foto" && cena.foto) {
    const troca = cena.marcos?.troca ?? Infinity;
    const d2 = lerp(t, troca - 0.12, troca + 0.3, 0, 1, easeInOut); // dissolve para a 2ª foto
    const hf = cena.aspecto ? Math.round(p.largura / cena.aspecto) : h;
    conteudo = (
      <>
        <div
          style={{
            position: "absolute",
            left: 0,
            top: h - hf,
            width: p.largura,
            height: hf,
          }}
        >
          <Foto
            src={p.imagens[cena.foto].arquivo}
            w={p.largura}
            h={hf}
            t={t}
            dur={dur}
            kb={cena.kb}
            foco={cena.foco}
            focoFim={cena.foco_fim}
          />
        </div>
        {cena.foto2 && d2 > 0 && (
          <div style={{ position: "absolute", inset: 0, opacity: d2 }}>
            <Foto
              src={p.imagens[cena.foto2].arquivo}
              w={p.largura}
              h={h}
              t={t - troca}
              dur={dur - troca}
              kb={cena.kb2 ?? [1.0, 1.05]}
              foco={cena.foco2 ?? [0.5, 0.5]}
            />
          </div>
        )}
      </>
    );
  } else if (cena.tipo === "anim") {
    const m = cena.marcos ?? {};
    conteudo = (
      <>
        {cena.anim === "ranking" && cena.print && (
          <Ranking t={t} src={p.imagens[cena.print].arquivo} marcos={m} />
        )}
        {cena.anim === "lista" && cena.itens && (
          <Lista
            t={t}
            marcos={m}
            itens={cena.itens.map((it) => ({
              src: p.imagens[it.foto].arquivo,
              linhas: it.linhas,
              em: it.em,
              foco: it.foco,
            }))}
          />
        )}
        {cena.anim === "gato" && <Gato t={t} marcos={m} />}
        {cena.anim === "mapa9" && <Mapa9 t={t} mapa={p.mapa9} marcos={m} />}
      </>
    );
  }
  if (!conteudo) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        width: p.largura,
        height: h,
        overflow: "hidden",
        background: PALETA.preto,
      }}
    >
      {conteudo}
      {cena.tipo !== "anim" && degrade}
      <Sobreposicoes p={p} cena={cena} t={t} h={h} />
    </div>
  );
};

/** Legenda: 1 a 4 palavras, Inter 800 66 px com sombra; palavra de destaque em âmbar (padrão do formato). */
const Legenda: React.FC<{ p: PropsParis; tS: number; cena: Cena }> = ({
  p,
  tS,
  cena,
}) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const pos = posicaoFala(cena);
  const y = pos === "baixo" ? p.costura : pos === "fundo" ? 1375 : 1320;
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

/** Gancho: a 1ª frase falada em letras grandes na metade de cima; cada linha entra quando é dita; o 2º bloco substitui o 1º. */
const Gancho: React.FC<{ p: PropsParis; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho + EMPURRAO) return null;
  const sai = easeInOut((tS - p.fimGancho) / EMPURRAO);
  const bloco = [...p.gancho].reverse().find((b) => tS >= b.ini) ?? p.gancho[0];
  const cor = (c: string) =>
    c === "ambar"
      ? PALETA.ambar
      : c === "vermelho"
        ? PALETA.vermelho
        : PALETA.branco;
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        translate: `0 ${-p.costura * clamp(sai)}px`,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 240,
          height: p.costura - 240,
          background:
            "linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.5) 45%, rgba(0,0,0,0.72) 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 72,
          right: 72,
          top: p.ganchoLayout.topo,
          textShadow: "0 4px 30px rgba(0,0,0,0.5)",
        }}
      >
        {bloco.linhas.map((l, k) => {
          const ini = bloco.tempos[k];
          const e = ini <= 0 ? 1 : ease((tS - ini) / 0.16);
          return (
            <div
              key={`${bloco.ini}-${k}`}
              style={{
                font: `400 ${bloco.tamanhos[k]}px ${TITULO}`,
                lineHeight: 1.02,
                color: cor(bloco.cores[k]),
                opacity: e,
                translate: `0 ${(1 - e) * 24}px`,
              }}
            >
              {l}
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** Palavra-chave em dupla tipografia (referência 1): sans pesada + serifa itálica, sobre o Diego em tela cheia. */
const PalavraChave: React.FC<{ p: PropsParis; tS: number }> = ({ p, tS }) => {
  const c = p.chaves.find((k) => tS >= k.ini - 0.01 && tS < k.fim);
  if (!c) return null;
  const sai = 1 - ease((tS - (c.fim - 0.15)) / 0.15);
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: 900,
          background:
            "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.7) 100%)",
          opacity: ease((tS - c.ini) / 0.2) * sai,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 72,
          right: 72,
          top: 1170,
          textShadow: SOMBRA_TEXTO,
          opacity: sai,
        }}
      >
        {c.linhas.map((l, i) => {
          const em = c.tempos?.[i] ?? c.ini;
          const e = ease((tS - em) / 0.18);
          return l.estilo === "rotulo" ? (
            <div
              key={i}
              style={{
                font: `700 42px ${TEXTO}`,
                letterSpacing: "0.34em",
                color: PALETA.ambar,
                marginTop: 10,
                marginLeft: c.tipo === "local" ? 74 : 0,
                opacity: e,
                translate: `0 ${(1 - e) * 16}px`,
              }}
            >
              {l.texto}
            </div>
          ) : (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 18,
                font:
                  l.estilo === "titulo"
                    ? `400 ${c.tipo === "local" ? 118 : 104}px ${TITULO}`
                    : `italic 700 142px ${SERIFA}`,
                lineHeight: l.estilo === "titulo" ? 1.0 : 0.95,
                color: l.estilo === "titulo" ? PALETA.branco : PALETA.ambar,
                textTransform: l.estilo === "titulo" ? "uppercase" : undefined,
                opacity: e,
                translate: `0 ${(1 - e) * 26}px`,
              }}
            >
              {c.tipo === "local" && i === 0 && <Pin />}
              {l.texto}
            </div>
          );
        })}
      </div>
    </>
  );
};

/** Pino de mapa da etiqueta de lugar (desenho próprio do formato, âmbar). */
const Pin: React.FC = () => (
  <svg width={56} height={76} viewBox="0 0 56 76">
    <path
      d="M28 74 C 18 56, 3 42, 3 27 A 25 25 0 1 1 53 27 C 53 42, 38 56, 28 74 Z"
      fill={PALETA.ambar}
      stroke={PALETA.preto}
      strokeWidth={3}
    />
    <circle cx={28} cy={27} r={10} fill={PALETA.preto} />
  </svg>
);

/** Luz de passagem (ida para o apoio): luz quente desce do topo em 3 quadros, cobre por 4 (o corte fica no mais claro) e recua para um canto em 4. */
const LuzDePassagem: React.FC<{ q: number; corte: number }> = ({
  q,
  corte,
}) => {
  const f = q - (corte - 5);
  if (f < 0 || f > 10) return null;
  let op = 0;
  let alto = 1920;
  let canto = 0;
  if (f <= 2) {
    op = 0.08 + (0.85 - 0.08) * ((f + 1) / 3);
    alto = 900 * (f + 1); // a borda de baixo some no degradê
  } else if (f <= 6) {
    op = 0.85;
  } else {
    canto = (f - 6) / 4;
    op = 0.85 * (1 - canto);
  }
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        mixBlendMode: "screen",
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1080,
          height: alto,
          opacity: op,
          background:
            canto > 0
              ? `radial-gradient(circle at 100% 0%, rgba(255,176,96,1) 0%, rgba(255,140,70,0.9) ${60 - 40 * canto}%, rgba(255,120,60,0) ${95 - 50 * canto}%)`
              : f <= 2
                ? "linear-gradient(to bottom, rgba(255,186,110,1) 0%, rgba(255,150,80,0.85) 55%, rgba(255,130,70,0) 100%)"
                : "linear-gradient(to bottom, rgba(255,186,110,1) 0%, rgba(255,150,80,0.95) 60%, rgba(255,130,70,0.75) 100%)",
        }}
      />
    </div>
  );
};

/** Clarão (volta para o rosto): quadro superexposto que volta ao normal em 5 quadros. */
const Clarao: React.FC<{ q: number; ini: number }> = ({ q, ini }) => {
  const f = q - ini;
  if (f < 0 || f > 4) return null;
  const op = [0.85, 0.6, 0.36, 0.16, 0.05][f];
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background: "#FFF6E8",
        opacity: op,
        pointerEvents: "none",
      }}
    />
  );
};

/** Grão de película próprio do formato (não é o grão do DS). */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg
    width={1080}
    height={1920}
    style={{
      position: "absolute",
      inset: 0,
      opacity: 0.06,
      mixBlendMode: "overlay",
      pointerEvents: "none",
    }}
  >
    <filter id="grao-paris">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.85"
        numOctaves={2}
        seed={q % 7}
        stitchTiles="stitch"
      />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-paris)" />
  </svg>
);

export const ReelParis: React.FC<PropsParis> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length)
    return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / fps;
  const cena =
    p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ??
    p.cenas[p.cenas.length - 1];
  const t = (q - cena.ini_q) / fps;
  const empurrando = cena.transicao === "empurrao" && t < EMPURRAO;
  const split = (cena.layout === "split" && cena.tipo !== "fala") || empurrando;
  const ctaQ = Math.round(p.cta.ini * fps);
  const linhaY = empurrando
    ? p.costura * (1 - easeInOut(t / EMPURRAO))
    : p.costura;

  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      <Fala p={p} cena={cena} t={t} />
      {p.cenas
        .filter((c) => c.tipo !== "fala")
        .map((c) => (
          <Sequence
            key={c.id}
            from={c.ini_q}
            durationInFrames={c.fim_q - c.ini_q + (c.extra_q ?? 0)}
            premountFor={20}
            name={c.id}
          >
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {/* camadas de cima (acima das imagens de apoio, inclusive da que está saindo numa transição) */}
      <div style={{ position: "absolute", inset: 0, zIndex: 3 }}>
        {split && (
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: linhaY - 3,
              height: 6,
              background: "rgba(0,0,0,0.55)",
            }}
          />
        )}
        <Grao q={q} />
        <Legenda p={p} tS={tS} cena={cena} />
        <PalavraChave p={p} tS={tS} />
        <Gancho p={p} tS={tS} />
        {p.cenas
          .filter((c) => c.transicao === "luz")
          .map((c) => (
            <LuzDePassagem key={c.id} q={q} corte={c.ini_q} />
          ))}
        {p.cenas
          .filter((c) => c.transicao === "clarao")
          .map((c) => (
            <Clarao key={c.id} q={q} ini={c.ini_q} />
          ))}
        {/* CTA: único lugar do Reel com o DS V2 (2.7: placa de direção com verbo + módulo; Chegada; clack) */}
        <Sequence from={ctaQ} name="CTA (DS V2)">
          <Placa
            rotulo={p.cta.rotulo}
            destino={p.cta.destino}
            modulo={p.cta.modulo}
            entrada={p.cta.entrada}
          />
          <Som
            nome="clack"
            em={p.cta.entrada + 280}
            relDb={p.mix.clack_db_rel}
            refLufs={p.mix.voz_lufs}
          />
        </Sequence>
      </div>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};
