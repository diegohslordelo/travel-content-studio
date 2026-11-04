/**
 * Reel "Bruges não quer você lá" (reels/bruges-bate-volta/), formato tela dividida → paisagens em tela cheia.
 * Camadas: Diego (um vídeo contínuo com as falas decupadas) · apoio (vídeo, foto, mapa ou grafismo) · transições ·
 * grão · legenda · gancho · CTA (o único ponto com o DS V2: Placa + clack, CLAUDE.md 6).
 * Tudo vem de reels/bruges-bate-volta/revN/props.json (gerado por scripts/reel.py).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { Captura, Comparar, Contador, Relogio } from "./Graficos";
import { DadosMapa, Mapa, ModoMapa } from "./Mapa";
import { GRADE_FOTO, GRADE_NATURAL, GRADE_VIDEO, PALETA, TEXTO, TITULO, clamp01, ease, easeInOut, lerp } from "./estilo";

type Palavra = { texto: string; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
export type CenaBruges = {
  id: string;
  tipo: "broll" | "foto" | "fala" | "mapa" | "captura" | "comparar";
  ini: number; // s
  fim: number;
  layout: "split" | "full";
  arquivo?: string;
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  modo?: ModoMapa;
  zoom?: [number, number];
  punch?: number; // s (relativo à cena): corte de zoom no rosto
  marcos?: Record<string, number>;
  escuro?: number; // 0–1: escurece o vídeo (para número por cima)
  entrada?: "empurrao" | "luz" | "cinema" | "clarao";
};
export type PropsBruges = {
  fps: number;
  quadros: number;
  costura: number;
  rostoY: number;
  cenas: CenaBruges[];
  legendas: Grupo[];
  semLegenda: [number, number][];
  gancho: { linhas: { tam: number; palavras: { texto: string; em: number; cor?: string }[] }[]; fim: number; topo: number };
  fitas: { ini: number; fim: number; entradas: number[]; texto: string; tops: number[]; giros: number[] } | null;
  contador: { ini: number; fim: number; marcos: Record<string, number> } | null;
  relogio: { ini: number; fim: number; em: number } | null;
  captura: { titulo: string; trecho: string; fundo: string; troca: number };
  comparar: { a: string; b: string; marco: number; focoA: [number, number]; focoB: [number, number] };
  mapa: DadosMapa;
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  /** REV2+: montagem calma (pedido do Diego, 04/11/2026): cor natural, sem zoom nem deslizes, textos só com fade. */
  calmo?: boolean;
  /** false: o vídeo sai mudo e a voz + clack são mixados fora (scripts/reel.py), com um único AAC no master. */
  audio?: boolean;
  /** Textos grandes por cima da imagem (números ditos na fala), só com fade. */
  textos?: { ini: number; fim: number; top: number; linhas: { texto: string; tam: number; cor?: string; fonte?: "titulo" | "texto"; em?: number }[] }[];
};

export const propsVaziasBruges: PropsBruges = {
  fps: 30,
  quadros: 30,
  costura: 900,
  rostoY: 720,
  cenas: [],
  legendas: [],
  semLegenda: [],
  gancho: { linhas: [], fim: 0, topo: 280 },
  fitas: null,
  contador: null,
  relogio: null,
  captura: { titulo: "", trecho: "", fundo: "", troca: 0 },
  comparar: { a: "", b: "", marco: 0, focoA: [0.5, 0.5], focoB: [0.5, 0.5] },
  mapa: { paises: {}, cidades: {} },
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
};

export const metadadosBruges: CalculateMetadataFunction<PropsBruges> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: 1080,
  height: 1920,
});

const ALTURA = 1920;
const LARGURA = 1080;

/** Diego: tela cheia (cena "fala") ou metade de baixo (cena em tela dividida). */
const Fala: React.FC<{ p: PropsBruges; cena: CenaBruges; t: number }> = ({ p, cena, t }) => {
  const cheia = cena.tipo === "fala";
  const split = cena.layout === "split";
  if (!cheia && !split) return null;
  let box: React.CSSProperties = { top: 0, height: ALTURA };
  let video: React.CSSProperties = {};
  if (cheia) {
    let z = cena.zoom ? lerp(t, 0, cena.fim - cena.ini, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    if (cena.punch !== undefined && t >= cena.punch) z *= 1.16; // corte de zoom (referências 2 e 6)
    video = { scale: String(z), transformOrigin: `540px ${p.rostoY}px` };
  } else {
    const h = ALTURA - p.costura;
    box = { top: p.costura, height: h };
    video = { translate: `0 ${Math.round(h * 0.42 - p.rostoY)}px` }; // rosto a 42% da metade de baixo
  }
  return (
    <div style={{ position: "absolute", left: 0, width: LARGURA, overflow: "hidden", ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: LARGURA, height: ALTURA, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: LARGURA, height: ALTURA }} />
      </div>
    </div>
  );
};

const Foto: React.FC<{ src: string; w: number; h: number; t: number; dur: number; kb?: [number, number]; foco?: [number, number]; focoFim?: [number, number]; filtro?: string }> = ({
  src,
  w,
  h,
  t,
  dur,
  kb = [1, 1.06],
  foco = [0.5, 0.5],
  focoFim,
  filtro = GRADE_FOTO,
}) => {
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  const fim = focoFim ?? foco;
  const fx = lerp(t, 0, dur, foco[0], fim[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], fim[1], easeInOut);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <Img
        src={staticFile(src)}
        style={{ width: w, height: h, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, scale: String(z), transformOrigin: `${fx * 100}% ${fy * 100}%`, filter: filtro }}
      />
    </div>
  );
};

/** Imagem de apoio de uma cena. Na tela dividida ocupa a metade de cima; na entrada "empurrão" cresce até a tela cheia. */
const Apoio: React.FC<{ p: PropsBruges; cena: CenaBruges }> = ({ p, cena }) => {
  const q = useCurrentFrame();
  const t = q / p.fps;
  const dur = cena.fim - cena.ini;
  let h = cena.layout === "split" ? p.costura : ALTURA;
  if (cena.entrada === "empurrao") h = lerp(t, 0, 0.42, p.costura, ALTURA, easeInOut); // a paisagem toma a tela
  const corpo = (() => {
    if (cena.tipo === "broll" && cena.arquivo) {
      const z = cena.kb ? lerp(t, 0, dur, cena.kb[0], cena.kb[1], (x) => x) : 1;
      return (
        // os clipes são verticais (1080 × 1920): o vídeo fica inteiro e a caixa recorta pelo centro (sem esticar)
        // foco[1]: que altura do vídeo vertical aparece quando a caixa é menor (tela dividida); 0,5 = centro
        <div style={{ position: "absolute", left: 0, top: (h - ALTURA) * (cena.foco?.[1] ?? 0.5), width: LARGURA, height: ALTURA, scale: String(z), filter: p.calmo ? GRADE_NATURAL : GRADE_VIDEO }}>
          <Video src={staticFile(cena.arquivo)} muted style={{ width: LARGURA, height: ALTURA }} />
        </div>
      );
    }
    if (cena.tipo === "foto" && cena.arquivo) return <Foto src={cena.arquivo} w={LARGURA} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} focoFim={cena.foco_fim} filtro={p.calmo ? GRADE_NATURAL : GRADE_FOTO} />;
    if (cena.tipo === "mapa") return <Mapa t={t} modo={cena.modo ?? "bloqueio"} dados={p.mapa} largura={LARGURA} altura={h} dur={dur} />;
    if (cena.tipo === "captura") return <Captura t={t} dur={dur} fundo={p.captura.fundo} titulo={p.captura.titulo} trecho={p.captura.trecho} troca={p.captura.troca} calmo={p.calmo} />;
    if (cena.tipo === "comparar") return <Comparar t={t} dur={dur} a={p.comparar.a} b={p.comparar.b} marco={p.comparar.marco} focoA={p.comparar.focoA} focoB={p.comparar.focoB} calmo={p.calmo} />;
    return null;
  })();
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: LARGURA, height: h, overflow: "hidden" }}>
      {corpo}
      {cena.escuro ? <div style={{ position: "absolute", inset: 0, background: `rgba(11,10,9,${cena.escuro})` }} /> : null}
      {/* tela cheia clara: degradê na base para a legenda branca (FORMATOS_REELS 3) */}
      {cena.layout === "full" && cena.tipo !== "captura" && cena.tipo !== "comparar" && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            height: p.calmo ? 760 : 960,
            background: p.calmo ? "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.32) 60%, rgba(0,0,0,0.42) 100%)" : "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.45) 55%, rgba(0,0,0,0.62) 100%)",
          }}
        />
      )}
    </div>
  );
};

/** Transições da linguagem do formato (REFERENCIA_EDICAO_FORMATOS 3.2), desenhadas por cima do corte. */
const Transicao: React.FC<{ tipo: CenaBruges["entrada"]; dt: number }> = ({ tipo, dt }) => {
  const f = dt * 30; // quadros desde o corte (negativo = antes)
  if (tipo === "luz") {
    // Luz de passagem: entra pelo topo 3 quadros antes, pico ≤ 85% por até 4 quadros com o corte no meio, recua em 4 (10.4)
    let a = 0;
    if (f >= -5 && f < -2) a = lerp(f, -5, -2, 0.08, 0.85, (x) => x);
    else if (f >= -2 && f < 2) a = 0.85;
    else if (f >= 2 && f < 6) a = lerp(f, 2, 6, 0.85, 0, (x) => x);
    if (a <= 0) return null;
    const desce = clamp01((f + 5) / 4);
    return (
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: a,
          background: `radial-gradient(ellipse 120% ${60 + 80 * desce}% at 50% 0%, rgba(255,214,150,1) 0%, rgba(255,190,110,0.9) 40%, rgba(224,174,92,0.0) 100%)`,
          mixBlendMode: "screen",
        }}
      />
    );
  }
  if (tipo === "cinema") {
    // escurece até o preto (2 quadros) e abre a noite com luz quente fraca
    let a = 0;
    if (f >= -9 && f < -2) a = lerp(f, -9, -2, 0, 1, easeInOut);
    else if (f >= -2 && f < 1) a = 1;
    else if (f >= 1 && f < 12) a = lerp(f, 1, 12, 1, 0, (x) => ease(x));
    if (a <= 0) return null;
    return <div style={{ position: "absolute", inset: 0, background: PALETA.preto, opacity: a }} />;
  }
  if (tipo === "clarao") {
    // Clarão de volta: quadro superexposto que volta ao normal em 5 quadros
    if (f < 0 || f >= 6) return null;
    return <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: lerp(f, 0, 6, 0.9, 0, (x) => x), mixBlendMode: "screen" }} />;
  }
  return null;
};

const Legenda: React.FC<{ p: PropsBruges; tS: number; cena: CenaBruges }> = ({ p, tS, cena }) => {
  if (p.semLegenda.some(([a, b]) => tS >= a && tS < b)) return null;
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
        textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)",
        scale: p.calmo ? undefined : String(0.94 + 0.06 * e),
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

/** Gancho: a 1ª frase em letras grandes na metade de cima, cada linha na palavra; o Diego embaixo desde o 1º quadro. */
const Gancho: React.FC<{ p: PropsBruges; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.linhas.length || tS >= p.gancho.fim) return null;
  const sai = clamp01((tS - (p.gancho.fim - 0.18)) / 0.18);
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 760, background: "linear-gradient(to bottom, rgba(11,10,9,0.55) 0%, rgba(11,10,9,0.35) 55%, rgba(11,10,9,0) 100%)", opacity: 1 - sai }} />
      <div style={{ position: "absolute", left: 72, top: p.gancho.topo, opacity: 1 - sai, textShadow: "0 4px 30px rgba(0,0,0,0.55)" }}>
        {p.gancho.linhas.map((l, k) => (
          <div key={k} style={{ font: `400 ${l.tam}px ${TITULO}`, lineHeight: 1.0, whiteSpace: "nowrap" }}>
            {l.palavras.map((w, j) => {
              const e = w.em <= 0 ? 1 : ease((tS - w.em) / 0.14);
              return (
                <span key={j} style={{ display: "inline-block", color: w.cor ?? PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 22}px`, scale: String(0.9 + 0.1 * e), marginRight: "0.22em" }}>
                  {w.texto}
                </span>
              );
            })}
          </div>
        ))}
      </div>
    </>
  );
};


/**
 * Fitas de isolamento da polícia belga (inscrição real "POLITIE · POLICE") cruzando a metade de cima no gancho.
 * Gancho B escolhido pelo Diego (04/11/2026). O vermelho é o da fita de verdade e fica fora da paleta do formato
 * (registrado na QA da REV1). Cada fita entra deslizando, passa do ponto e assenta.
 */
const VERMELHO_FITA = "#D7262E";
const Fitas: React.FC<{ f: NonNullable<PropsBruges["fitas"]>; tS: number; costura: number }> = ({ f, tS, costura }) => {
  if (tS < f.ini || tS >= f.fim) return null;
  const t = tS - f.ini;
  const sai = clamp01((tS - (f.fim - 0.12)) / 0.12);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: LARGURA, height: costura, overflow: "hidden", opacity: 1 - sai }}>
      {f.entradas.map((em, i) => {
        if (t < em - 0.12) return null;
        const p = clamp01((t - em + 0.12) / 0.2);
        const lado = i % 2 === 0 ? -1 : 1;
        const desl = (1 - ease(p)) * 1400 * lado + Math.sin(clamp01((t - em) / 0.3) * Math.PI) * 18 * -lado * (t > em ? 1 : 0);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: -240 + desl,
              top: f.tops[i],
              width: 1560,
              height: 92,
              rotate: `${f.giros[i]}deg`,
              background: `repeating-linear-gradient(90deg, ${VERMELHO_FITA} 0 120px, #fff 120px 240px)`,
              boxShadow: "0 14px 40px rgba(0,0,0,0.55)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 220,
              whiteSpace: "nowrap",
            }}
          >
            {[0, 1, 2].map((k) => (
              <span key={k} style={{ background: "#fff", padding: "6px 20px", font: `800 36px ${TEXTO}`, letterSpacing: 6, color: PALETA.preto, whiteSpace: "nowrap" }}>
                {f.texto}
              </span>
            ))}
          </div>
        );
      })}
    </div>
  );
};

const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-bruges">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-bruges)" />
  </svg>
);

export const ReelBruges: React.FC<PropsBruges> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / fps;
  const cena = p.cenas.find((c) => tS >= c.ini && tS < c.fim) ?? p.cenas[p.cenas.length - 1];
  const t = tS - cena.ini;
  // a cena anterior continua por baixo durante o empurrão (o Diego some quando a paisagem cobre a tela)
  const anterior = p.cenas[p.cenas.indexOf(cena) - 1];
  const empurrando = cena.entrada === "empurrao" && t < 0.45 && anterior;
  const iq = (s: number) => Math.round(s * fps);

  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      <Fala p={p} cena={empurrando ? anterior : cena} t={t} />
      {p.cenas
        .filter((c) => c.tipo !== "fala")
        .map((c) => (
          <Sequence key={c.id} from={iq(c.ini)} durationInFrames={iq(c.fim) - iq(c.ini)} premountFor={30} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {p.fitas && <Fitas f={p.fitas} tS={tS} costura={p.costura} />}
      {p.contador && (
        <Sequence from={iq(p.contador.ini)} durationInFrames={iq(p.contador.fim) - iq(p.contador.ini)} name="contador">
          <Contador t={tS - p.contador.ini} m={p.contador.marcos} />
        </Sequence>
      )}
      {(p.textos ?? []).map((x, k) =>
        tS >= x.ini && tS < x.fim ? (
          <div key={k} style={{ position: "absolute", left: 0, right: 0, top: x.top, textAlign: "center", opacity: ease((tS - x.ini) / 0.25) * (1 - clamp01((tS - (x.fim - 0.2)) / 0.2)), textShadow: "0 4px 30px rgba(0,0,0,0.65), 0 2px 0 rgba(0,0,0,0.35)" }}>
            {x.linhas.map((l, j) => (
              <div key={j} style={{ font: l.fonte === "texto" ? `800 ${l.tam}px ${TEXTO}` : `400 ${l.tam}px ${TITULO}`, letterSpacing: l.fonte === "texto" ? 3 : 0, lineHeight: 1.02, color: l.cor ?? PALETA.branco, opacity: l.em === undefined ? 1 : ease((tS - l.em) / 0.25) }}>
                {l.texto}
              </div>
            ))}
          </div>
        ) : null,
      )}
      {p.relogio && tS >= p.relogio.ini && tS < p.relogio.fim && <Relogio t={tS - p.relogio.ini} em={p.relogio.em - p.relogio.ini} />}
      {cena.layout === "split" && !empurrando && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      {p.cenas.filter((c) => c.entrada && c.entrada !== "empurrao").map((c) => (Math.abs(tS - c.ini) < 0.5 ? <Transicao key={c.id} tipo={c.entrada} dt={tS - c.ini} /> : null))}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
      <Gancho p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (2.7: placa de direção; Chegada; clack) */}
      <Sequence from={iq(p.cta.ini)} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="interrogacao" entrada={p.cta.entrada} />
        {p.audio !== false && <Som nome="clack" em={p.cta.entrada + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />}
      </Sequence>
      {p.audio !== false && <Audio src={staticFile("voz.wav")} />}
      {p.audio !== false && <Audio src={staticFile("sfx.wav")} />}
    </AbsoluteFill>
  );
};
