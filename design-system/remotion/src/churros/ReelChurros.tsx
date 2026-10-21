/**
 * Reels dos churros: "Churros em Barcelona" (reels/churros-barcelona/rev1) e "Churros em Madrid"
 * (reels/churros-madrid/revN), mesmo roteiro e mesmas animações.
 *
 * Montagem a partir de `revN.json` + medições do `revN.py preparar` (props). As cenas de vídeo já vêm
 * recortadas em 9:16, com cor convertida e sem áudio; aqui entram a câmera virtual, as transições,
 * os textos, as cartelas, o globo e o desenho de som (faixa separada, opcional).
 *
 * Linguagem visual própria deste Reel (tema.ts). Do DS V2 só entram a placa do CTA (2.7) e a capa,
 * por decisão do Diego de 21/10/2026.
 *
 * Nenhum áudio de clipe: os <Video> são sempre `muted` e as cenas preparadas não têm faixa de áudio.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Sequence, random, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { kf, useMs } from "../ds/tempo";
import { Comparacao, Veredito } from "./Cartelas";
import { Destino, Globo } from "./Globo";
import { EstiloTexto, TextoNaTela } from "./Textos";
import { C, CURVA, carregarFontesChurros } from "./tema";

carregarFontesChurros();

type EfeitoCena = "plano" | "mergulho" | "congela" | "suspense" | "fundo" | "globo" | "veredito" | "comparacao";
type Cena = {
  id: string;
  bloco: string;
  grafico?: boolean;
  arquivo?: string;
  quadros: number;
  dur: number;
  camera?: { de: number; para: number };
  /** tratamento da cena; sem ele, vale o mapa por id da REV1 de Barcelona */
  efeito?: EfeitoCena;
  /** origem do zoom ("x% y%"): onde a câmera mira */
  mira?: string;
  /** congela: ms em que o quadro para; foco: centro do foco de luz ("x% y%") */
  congela_ms?: number;
  foco?: string;
};
type TextoProps = {
  cena: string;
  t: number;
  fim: number;
  estilo: EstiloTexto;
  linhas: string[];
  kicker?: string;
  sub?: string;
  numero?: string;
  y: number;
};
export type PropsChurros = {
  fps: number;
  largura: number;
  altura: number;
  cenas: Cena[];
  textos: TextoProps[];
  cta?: { cena: string; t: number; rotulo: string; x?: number };
  /** "cacau" (REV1 de Barcelona) ou "colorido" (globo e cartelas em cores vivas) */
  paleta?: "cacau" | "colorido";
  destino?: Destino;
  cartelas?: { abaixo_veredito?: string; acucar_destino?: number };
  efeitos?: Efeito[];
  capa?: { cena: string; t: number; rotulo?: string; destino: string; modulo?: "seta" | "interrogacao" };
};

export const propsVaziasChurros: PropsChurros = { fps: 24, largura: 1080, altura: 1920, cenas: [], textos: [] };

/** Quadros que o globo invade a cena seguinte (dissolve do mergulho em Barcelona). */
const SOBRA_GLOBO = 8;

export const metadadosChurros: CalculateMetadataFunction<PropsChurros> = ({ props }) => ({
  durationInFrames: Math.max(1, props.cenas.reduce((s, c) => s + c.quadros, 0)),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

// ---------------------------------------------------------------- planos

/** Origem do zoom de cada plano da REV1 de Barcelona (as revisões novas trazem `mira` no JSON). */
const MIRA: Record<string, string> = {
  h_bandeja: "50% 60%",
  h_mergulho: "76% 74%",
  b_sagrada: "50% 35%",
  c_cone: "50% 70%",
  c_mordida: "45% 35%",
  k_aponta: "61% 48%",
  k_marina: "48% 45%",
  r_mastiga: "47% 32%",
  f_pergunta: "50% 55%",
};

const Plano: React.FC<{ cena: Cena; soco?: boolean; extra?: (t: number) => React.CSSProperties }> = ({ cena, soco, extra }) => {
  const t = useMs();
  const dur = cena.dur * 1000;
  const cam = cena.camera ?? { de: 1, para: 1 };
  const escala = kf(t, [0, dur], [cam.de, cam.para], CURVA.suave);
  // "soco" de entrada no gancho e na chegada: 5% em 180 ms, acompanha o corte
  const s = soco ? 1 + 0.05 * (1 - kf(t, [0, 180], [0, 1], CURVA.sai)) : 1;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill style={{ scale: String(escala * s), transformOrigin: cena.mira ?? MIRA[cena.id] ?? "50% 50%", ...(extra ? extra(t) : {}) }}>
        <Video src={staticFile(cena.arquivo as string)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Gancho → globo: a câmera mergulha no chocolate e o marrom vira o oceano do globo. */
const Mergulho: React.FC<{ cena: Cena }> = ({ cena }) => {
  const t = useMs();
  const dur = cena.dur * 1000;
  // mira o chocolate do copo (canto inferior direito do plano) e afunda nele nos últimos 650 ms
  const p = Math.pow(kf(t, [dur - 650, dur], [0, 1]), 2);
  return (
    <AbsoluteFill>
      <Plano cena={cena} soco extra={() => ({ scale: String(1 + 3.2 * p), filter: p > 0.05 ? `blur(${12 * p}px)` : undefined })} />
      <AbsoluteFill style={{ background: C.cacau2, opacity: kf(t, [dur - 260, dur], [0, 1], CURVA.entra) }} />
    </AbsoluteFill>
  );
};

/** Mudança de ritmo: o quadro congela (no produto), flash curto e foco de luz nele. */
const Congela: React.FC<{ cena: Cena; congelaEm: number; foco?: string }> = ({ cena, congelaEm, foco: centroFoco = "61% 48%" }) => {
  const t = useMs();
  const d = t - congelaEm;
  const flash = d >= 0 ? kf(d, [0, 40, 200], [0, 0.85, 0], [CURVA.sai, CURVA.suave]) : 0;
  const foco = kf(d, [0, 380], [0, 1], CURVA.sai);
  return (
    <AbsoluteFill>
      <Plano cena={cena} extra={() => ({ filter: foco > 0 ? `saturate(${1 - 0.25 * foco})` : undefined })} />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${centroFoco}, rgba(0,0,0,0) 0px, rgba(0,0,0,0) ${300 - 60 * foco}px, rgba(20,10,5,${0.62 * foco}) ${520 - 60 * foco}px)`,
        }}
      />
      <AbsoluteFill style={{ background: C.creme, opacity: flash }} />
    </AbsoluteFill>
  );
};

/** Pausa antes do veredito: barras de cinema, menos cor, câmera fechando. */
const Suspense: React.FC<{ cena: Cena }> = ({ cena }) => {
  const t = useMs();
  const dur = cena.dur * 1000;
  const barra = kf(t, [0, 520], [0, 170], CURVA.sai);
  const dessat = kf(t, [0, dur], [0, 0.35], CURVA.suave);
  return (
    <AbsoluteFill>
      <Plano cena={cena} extra={() => ({ filter: `saturate(${1 - dessat}) contrast(${1 + 0.06 * dessat})` })} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: barra, background: "#0B0705" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: barra, background: "#0B0705" }} />
    </AbsoluteFill>
  );
};

/** Fundo da pergunta final: a bandeja do gancho, desfocada e escurecida (o fim emenda no começo). */
const FundoPergunta: React.FC<{ cena: Cena }> = ({ cena }) => {
  const t = useMs();
  const entra = kf(t, [0, 420], [0, 1], CURVA.sai);
  return (
    <AbsoluteFill>
      <Plano cena={cena} extra={() => ({ filter: `blur(${12 * entra}px) brightness(${1 - 0.5 * entra})` })} />
      <AbsoluteFill style={{ background: `linear-gradient(180deg, rgba(30,18,12,.35), rgba(30,18,12,.15) 50%, rgba(30,18,12,.55))`, opacity: entra }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- acabamento

/** Grão de filme leve (SVG turbulência com semente por quadro) + vinheta suave. */
const Pelicula: React.FC = () => {
  const q = useCurrentFrame();
  const semente = Math.floor(random(`grao-${q}`) * 1000);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.07, mixBlendMode: "overlay" }}>
        <filter id="grao">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={semente} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grao)" />
      </svg>
      <AbsoluteFill style={{ background: "radial-gradient(120% 90% at 50% 50%, rgba(0,0,0,0) 60%, rgba(10,5,2,.32) 100%)" }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- som (opcional, faixa separada)

type Efeito = { arq: string; cena: string; t: number; vol: number };

/** Tratamento das cenas da REV1 de Barcelona (as revisões novas trazem `efeito` no JSON). */
const EFEITO_POR_ID: Record<string, EfeitoCena> = {
  mapa: "globo",
  h_mergulho: "mergulho",
  k_aponta: "congela",
  r_mastiga: "suspense",
  r_veredito: "veredito",
  f_comparacao: "comparacao",
  f_pergunta: "fundo",
};
/** Efeitos sintetizados no rev1.py (pico −6 dBFS); o master leva o conjunto a ≈ −24 LUFS. */
const EFEITOS: Efeito[] = [
  { arq: "sfx_whoosh.wav", cena: "h_mergulho", t: -0.12, vol: 0.45 },
  { arq: "sfx_pop.wav", cena: "h_mergulho", t: 0.62, vol: 0.5 },
  { arq: "sfx_mergulho.wav", cena: "h_mergulho", t: 1.25, vol: 0.9 },
  { arq: "sfx_aviao.wav", cena: "mapa", t: 0.55, vol: 0.55 },
  { arq: "sfx_pin.wav", cena: "mapa", t: 2.9, vol: 0.45 },
  { arq: "sfx_whoosh.wav", cena: "b_sagrada", t: -0.25, vol: 0.6 },
  { arq: "sfx_pop.wav", cena: "b_fachada", t: 0.3, vol: 0.4 },
  { arq: "sfx_whoosh.wav", cena: "c_cone", t: -0.15, vol: 0.4 },
  { arq: "sfx_pop.wav", cena: "k_aponta", t: 0.62, vol: 0.6 },
  { arq: "sfx_tum.wav", cena: "r_veredito", t: 0.42, vol: 1 },
  { arq: "sfx_whoosh.wav", cena: "f_comparacao", t: -0.1, vol: 0.5 },
  { arq: "sfx_pop.wav", cena: "f_comparacao", t: 1.35, vol: 0.45 },
  { arq: "sfx_pop.wav", cena: "f_pergunta", t: 0.25, vol: 0.45 },
];

// ---------------------------------------------------------------- composição

export const ReelChurros: React.FC<PropsChurros> = (p) => {
  const { fps } = useVideoConfig();
  const ini: Record<string, number> = {};
  let acc = 0;
  for (const c of p.cenas) {
    ini[c.id] = acc;
    acc += c.quadros;
  }
  const q = (s: number) => Math.round(s * fps);
  const cena = (id: string) => p.cenas.find((c) => c.id === id) as Cena;

  const paleta = p.paleta ?? "cacau";
  const conteudo = (c: Cena): React.ReactNode => {
    switch (c.efeito ?? EFEITO_POR_ID[c.id] ?? "plano") {
      case "veredito":
        return <Veredito dur={c.dur * 1000} paleta={paleta} abaixo={p.cartelas?.abaixo_veredito} />;
      case "comparacao":
        return <Comparacao dur={c.dur * 1000} paleta={paleta} direita={p.destino?.nome} acucarDireita={p.cartelas?.acucar_destino} />;
      case "mergulho":
        return <Mergulho cena={c} />;
      case "congela":
        return <Congela cena={c} congelaEm={c.congela_ms ?? 620} foco={c.foco} />;
      case "suspense":
        return <Suspense cena={c} />;
      case "fundo":
        return <FundoPergunta cena={c} />;
      default:
        return <Plano cena={c} soco={c.bloco === "gancho" || c.bloco === "chegada"} />;
    }
  };
  const idGlobo = p.cenas.find((c) => (c.efeito ?? EFEITO_POR_ID[c.id]) === "globo")?.id;

  return (
    <AbsoluteFill style={{ background: C.cacau }}>
      {p.cenas
        .filter((c) => c.id !== idGlobo)
        .map((c) => (
          <Sequence key={c.id} name={c.id} from={ini[c.id]} durationInFrames={c.quadros}>
            {conteudo(c)}
          </Sequence>
        ))}

      {/* o globo fica por cima e dissolve sobre o primeiro plano da cidade enquanto ainda mergulha */}
      {idGlobo && (
        <Sequence name="globo" from={ini[idGlobo]} durationInFrames={cena(idGlobo).quadros + SOBRA_GLOBO}>
          <SaidaGlobo quadros={cena(idGlobo).quadros}>
            <Globo paleta={paleta} destino={p.destino} corEntrada={paleta === "colorido" ? C.cacau2 : undefined} />
          </SaidaGlobo>
        </Sequence>
      )}

      {p.textos.map((tx, i) => (
        <Sequence key={`tx${i}`} name={`texto ${tx.linhas.join(" ")}`} from={ini[tx.cena] + q(tx.t)} durationInFrames={q(tx.fim - tx.t)}>
          <TextoNaTela estilo={tx.estilo} linhas={tx.linhas} kicker={tx.kicker} sub={tx.sub} numero={tx.numero} y={tx.y} dur={(tx.fim - tx.t) * 1000} />
        </Sequence>
      ))}

      {/* CTA do DS V2 (2.7): placa pequena com verbo + módulo de seta */}
      {p.cta && (
        <Sequence name="CTA (DS)" from={ini[p.cta.cena] + q(p.cta.t)} durationInFrames={cena(p.cta.cena).quadros - q(p.cta.t)}>
          <Placa destino={p.cta.rotulo} modulo="seta" tamanho="M" x={p.cta.x ?? 72} y={1150} entrada={0} />
        </Sequence>
      )}

      <Pelicula />

      {(p.efeitos ?? EFEITOS).filter((e) => ini[e.cena] !== undefined).map((e, i) => (
        <Sequence key={`sfx${i}`} name={`som ${e.arq}`} from={Math.max(0, ini[e.cena] + q(e.t))} layout="none">
          <Audio src={staticFile(e.arq)} volume={e.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const SaidaGlobo: React.FC<{ quadros: number; children: React.ReactNode }> = ({ quadros, children }) => {
  const q = useCurrentFrame();
  const op = kf(q, [quadros - 2, quadros + SOBRA_GLOBO], [1, 0], CURVA.suave);
  return <AbsoluteFill style={{ opacity: op }}>{children}</AbsoluteFill>;
};

// ---------------------------------------------------------------- capa (DS V2: placa sobre o quadro)

export const CapaChurros: React.FC<PropsChurros> = (p) => {
  const { fps } = useVideoConfig();
  if (!p.capa) return <AbsoluteFill style={{ background: C.cacau }} />;
  const c = p.cenas.find((x) => x.id === p.capa?.cena) as Cena;
  return (
    <AbsoluteFill style={{ background: C.cacau }}>
      <AbsoluteFill style={{ scale: String(c.camera?.de ?? 1), transformOrigin: c.mira ?? MIRA[c.id] ?? "50% 50%" }}>
        <Video src={staticFile(c.arquivo as string)} muted trimBefore={Math.round(p.capa.t * fps)} objectFit="cover" style={{ width: "100%", height: "100%" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(20,10,5,.35), rgba(20,10,5,0) 45%)" }} />
      <Placa rotulo={p.capa.rotulo} destino={p.capa.destino} modulo={p.capa.modulo ?? "seta"} entrada={null} />
    </AbsoluteFill>
  );
};
