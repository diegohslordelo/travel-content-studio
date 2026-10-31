/**
 * Reel da Grand-Place (reels/bruxelas-grand-place/) · tela dividida, na linguagem dos Reels do perfil nesse formato
 * (docs/FORMATOS_REELS.md), a partir da composição do Reel da cratera de Darvaza. Camadas: apoio (vídeo do acervo do
 * Diego, gravura ou pintura do Commons) · Diego (metade de baixo ou tela cheia) · legendas · gancho · títulos ·
 * transições · CTA. O DS V2 aparece só no CTA final (placa + clack).
 * Tudo vem das props (reels/bruxelas-grand-place/scripts/reel.py → _tmp/props.json): cenas ancoradas nas palavras.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { Clarao, Cortina, DadosMapa, Envio, FotoFundo, Linha, LuzPassagem, MapaCartao, Titulo } from "./Graficos";
import { GRADE_FOTO, GRADE_VIDEO, PALETA, TEXTO, TITULO, ease, easeInOut, lerp } from "./estilo";

type Palavra = { texto: string; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "foto" | "video" | "fala";
  ini_q: number;
  fim_q: number;
  layout: "split" | "full";
  foto?: string;
  video?: string;
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  tom?: "natural" | "gravura" | "pintura";
  titulo?: { linhas: Linha[]; centroY: number; sai?: number };
  apagar?: [number, number, number];
  sepia?: [number, number];
  zoom?: [number, number];
  punch?: { em: number; z: number };
  envio?: { entra: number; voa: number; x: number; y: number };
  mapa?: { entra: number; cidade: number; pais: number };
  comparar?: { video: string; de: number; ate: number };
};
export type PropsGP = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  rostoX: number;
  quadros: number;
  cenas: Cena[];
  gancho: { linhas: string[]; tamanhos: number[]; tempos: number[]; cores?: (string | null)[] }[];
  fimGancho: number;
  ganchoTopo: number;
  legendas: Grupo[];
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
  transicoes: { tipo: "luz" | "clarao"; q: number }[];
  mapa: DadosMapa;
};

export const propsVaziasGP: PropsGP = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 690,
  rostoX: 510,
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
  mapa: { paises: [], ponto: [0, 0] },
};

export const metadadosGP: CalculateMetadataFunction<PropsGP> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const FILTRO = {
  natural: GRADE_FOTO,
  gravura: "grayscale(1) sepia(0.28) contrast(1.12) brightness(0.92)", // gravura em P&B com tom de papel antigo
  pintura: "saturate(1.08) contrast(1.08) brightness(0.95)",
};

const posicaoFala = (c: Cena): "cheia" | "baixo" | "fora" => (c.tipo === "fala" ? "cheia" : c.layout === "split" ? "baixo" : "fora");

/** Diego: um único vídeo contínuo (as falas decupadas), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsGP; cena: Cena; t: number }> = ({ p, cena, t }) => {
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

/** Filtro da cena: tom base, virada para sépia ("volta no tempo") e escurecimento sob um título. */
const filtroCena = (cena: Cena, t: number, base: string) => {
  let f = base;
  if (cena.sepia) {
    const k = lerp(t, cena.sepia[0], cena.sepia[1], 0, 1, easeInOut);
    f += ` sepia(${0.85 * k}) saturate(${1 - 0.45 * k}) contrast(${1 + 0.08 * k})`;
  }
  if (cena.apagar) f += ` brightness(${lerp(t, cena.apagar[0], cena.apagar[1], 1, cena.apagar[2], easeInOut)})`;
  return f;
};

const Foto: React.FC<{ cena: Cena; w: number; h: number; t: number; dur: number }> = ({ cena, w, h, t, dur }) => {
  const kb = cena.kb ?? [1, 1.05];
  const foco = cena.foco ?? [0.5, 0.5];
  const fim = cena.foco_fim ?? foco;
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  const fx = lerp(t, 0, dur, foco[0], fim[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], fim[1], easeInOut);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <Img
        src={staticFile(cena.foto as string)}
        style={{ width: w, height: h, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, scale: String(z), transformOrigin: `${fx * 100}% ${fy * 100}%`, filter: filtroCena(cena, t, FILTRO[cena.tom ?? "natural"]) }}
      />
    </div>
  );
};

/** Vídeo do acervo do Diego (já recortado na proporção da camada, mudo, HDR → SDR), com aproximação lenta e linear. */
const VideoApoio: React.FC<{ cena: Cena; src: string; w: number; h: number; t: number; dur: number }> = ({ cena, src, w, h, t, dur }) => {
  const kb = cena.kb ?? [1, 1.04];
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <div style={{ position: "absolute", inset: 0, scale: String(z), filter: filtroCena(cena, t, GRADE_VIDEO) }}>
        <Video src={staticFile(src)} muted style={{ width: w, height: h }} />
      </div>
    </div>
  );
};

/** Imagem de apoio da cena (atrás do Diego, ou acima dele na tela dividida). */
const Apoio: React.FC<{ p: PropsGP; cena: Cena }> = ({ p, cena }) => {
  const q = useCurrentFrame();
  const t = q / p.fps;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  const conteudo =
    cena.tipo === "video" && cena.video ? (
      <VideoApoio cena={cena} src={cena.video} w={p.largura} h={h} t={t} dur={dur} />
    ) : cena.foto ? (
      <Foto cena={cena} w={p.largura} h={h} t={t} dur={dur} />
    ) : null;
  const c = cena.comparar;
  const pc = c ? lerp(t, c.de, c.ate, 0, 1, easeInOut) : 0;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
      {conteudo}
      {c && (
        <Cortina p={pc} w={p.largura} h={h}>
          <Sequence from={Math.round(c.de * p.fps)} layout="none" name="hoje (cortina)">
            <div style={{ position: "absolute", inset: 0, filter: GRADE_VIDEO }}>
              <Video src={staticFile(c.video)} muted style={{ width: p.largura, height: h }} />
            </div>
          </Sequence>
        </Cortina>
      )}
      {!split && !cena.titulo && cena.tipo !== "fala" && (
        // tela cheia clara: degradê escuro na base para a legenda branca (FORMATOS_REELS.md, 3)
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 960, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 55%, rgba(0,0,0,0.62) 100%)" }} />
      )}
      {cena.titulo && !split && (
        // título em tela cheia sobre imagem clara: faixa escura atrás do título que continua até a base (legenda)
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(to bottom, rgba(0,0,0,0) 0px, rgba(0,0,0,0.36) ${cena.titulo.centroY - 200}px, rgba(0,0,0,0.36) ${cena.titulo.centroY + 200}px, rgba(0,0,0,0.3) 1180px, rgba(0,0,0,0.62) 1920px)`,
          }}
        />
      )}
      {split && (
        // legenda na costura sobre imagem clara (gravura, céu): degradê escuro na base da metade de cima
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 240, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 100%)" }} />
      )}
      {cena.mapa && <MapaCartao t={t} dados={p.mapa} m={cena.mapa} x={170} y={300} w={740} h={440} />}
      {cena.titulo && <Titulo t={t} linhas={cena.titulo.linhas} centroY={cena.titulo.centroY} sai={cena.titulo.sai} />}
    </div>
  );
};

/** Legenda: 1 a 4 palavras, Inter 800 66 px com sombra; palavra de destaque em âmbar. */
const Legenda: React.FC<{ p: PropsGP; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
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
const Gancho: React.FC<{ p: PropsGP; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho) return null;
  const sai = lerp(tS, p.fimGancho - 0.12, p.fimGancho, 1, 0, (x) => x);
  const linha = (txt: string, tam: number, ini: number, cor: string | null | undefined, k: number) => {
    const e = ini <= 0 ? 1 : ease(Math.min(1, Math.max(0, (tS - ini) / 0.16)));
    return (
      <div key={k} style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 1.02, color: cor ?? PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
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
            {b.linhas.map((l, k) => linha(l, b.tamanhos[k], b.tempos[k], b.cores?.[k], i * 10 + k))}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

/** Grão de película do formato (6%, overlay); não é o grão do DS. */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-gp">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-gp)" />
  </svg>
);

export const ReelGrandPlace: React.FC<PropsGP> = (p) => {
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
      {cena.tipo === "fala" && (
        // Diego em tela cheia de camiseta branca: degradê na base para a legenda branca (FORMATOS_REELS.md, 3)
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 900, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.42) 45%, rgba(0,0,0,0.5) 100%)" }} />
      )}
      {cena.envio && <Envio t={t} m={cena.envio} x={cena.envio.x} y={cena.envio.y} />}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
      <Gancho p={p} tS={tS} />
      {p.transicoes.map((tr, i) => (tr.tipo === "luz" ? <LuzPassagem key={i} q={q} corte={tr.q} /> : <Clarao key={i} q={q} corte={tr.q} />))}
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

/** Capa (1080 × 1920): imagem de fundo, título e o Diego embaixo; usada como still. */
export const CapaGrandPlace: React.FC<{ foto: string; quadro: string; linhas: Linha[]; centroY: number; costura: number; rostoY: number; filtro?: string; posicao?: string }> = ({
  foto,
  quadro,
  linhas,
  centroY,
  costura,
  rostoY,
  filtro,
  posicao,
}) => {
  const h = 1920 - costura;
  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      <div style={{ position: "absolute", left: 0, top: costura, width: 1080, height: h, overflow: "hidden" }}>
        <Img src={staticFile(quadro)} style={{ position: "absolute", left: 0, top: Math.round(h * 0.42 - rostoY), width: 1080, height: 1920 }} />
      </div>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: costura, overflow: "hidden" }}>
        <FotoFundo src={foto} w={1080} h={costura} filtro={filtro ?? "saturate(1.08) contrast(1.08) brightness(0.8)"} posicao={posicao} />
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.3) 55%, rgba(0,0,0,0.55) 100%)" }} />
        <Titulo t={9} linhas={linhas} centroY={centroY} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />
      <Grao q={0} />
    </AbsoluteFill>
  );
};
