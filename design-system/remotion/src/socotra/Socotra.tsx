/**
 * Reel de Socotra · tela dividida (reels/socotra/), no padrão do formato (docs/FORMATOS_REELS.md) e da composição do Gaudí.
 * Camadas: imagem de apoio (foto do Commons ou animação) · Diego (tela cheia ou metade de baixo) · legendas · gancho · CTA.
 * Cortes secos; o DS V2 aparece só no CTA final (Placa + clack), por decisão do Diego (28/10/2026).
 * Transições ligadas ao tema (REFERENCIA_EDICAO_FORMATOS.md, 3.2):
 *  - gancho "ficção → real": a foto começa com grade fria de ficção científica (linhas de varredura) e, na palavra "real",
 *    um clarão revela a cor natural;
 *  - guarda-chuva desenhado em traço sobre a foto real da árvore, descendo até a copa ("colocou em cima de um tronco");
 *  - cosmos → Terra → Socotra: um movimento contínuo de câmera do planeta fictício até o arquipélago (mapa Natural Earth).
 * Ilustração nunca se passa por foto: tudo o que é criado é traço ou mapa.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { geoGraticule10, geoOrthographic, geoPath } from "d3-geo";
import type { FeatureCollection, MultiPolygon } from "geojson";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, random, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { GRADE_FOTO, PALETA, TEXTO, TITULO, ease, easeInOut, lerp } from "./estilo";
import regiaoJson from "./geo/regiao_10m.json";
import terraJson from "./geo/terra_110m.json";

const REGIAO = regiaoJson as unknown as FeatureCollection<MultiPolygon, { iso: string }>;
const TERRA = terraJson as unknown as FeatureCollection;

type Palavra = { texto: string; ini: number; fim: number; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Cena = {
  id: string;
  tipo: "foto" | "fala" | "anim";
  ini_q: number;
  fim_q: number;
  layout?: "full" | "split";
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  foto?: string;
  fundo?: string;
  anim?: "guarda" | "cosmos" | "fracao";
  efeito?: "scifi";
  marcos?: Record<string, number>;
  zoom?: [number, number];
  continua?: boolean;
};
export type PropsSocotra = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  quadros: number;
  cenas: Cena[];
  imagens: Record<string, { arquivo: string }>;
  gancho: { linhas: string[]; tamanhos: number[]; tempos: number[] }[];
  fimGancho: number;
  ganchoLayout: { split: boolean; topo: number };
  legendas: Grupo[];
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
  mix: { voz_lufs: number; clack_db_rel: number };
  sfx: boolean;
};

export const propsVaziasSocotra: PropsSocotra = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 740,
  quadros: 30,
  cenas: [],
  imagens: {},
  gancho: [],
  fimGancho: 0,
  ganchoLayout: { split: true, topo: 275 },
  legendas: [],
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
  mix: { voz_lufs: -14, clack_db_rel: -6 },
  sfx: false,
};

export const metadadosSocotra: CalculateMetadataFunction<PropsSocotra> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const VERMELHO = "#B3261E"; // só nas gotas desenhadas ("sangue escorrendo"): cor da resina, não é cor da marca
const SCIFI = "grayscale(1) sepia(1) hue-rotate(140deg) saturate(2.4) contrast(1.18) brightness(0.78)";
const lin = (x: number) => x;
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

const posicaoFala = (c: Cena): "cheia" | "baixo" | "fora" => {
  if (c.tipo === "fala") return "cheia";
  if (c.layout === "split") return "baixo";
  return "fora";
};

/** Diego: um único vídeo contínuo (as falas decupadas), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsSocotra; cena: Cena; t: number }> = ({ p, cena, t }) => {
  const pos = posicaoFala(cena);
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (pos === "cheia") {
    const z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], lin) : 1;
    const punch = cena.marcos?.punch !== undefined && t >= cena.marcos.punch ? 1.12 : 1; // corte de zoom (seco) na fala longa
    video = { scale: String(z * punch), transformOrigin: `540px ${p.rostoY}px` };
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

const Foto: React.FC<{ src: string; w: number; h: number; t: number; dur: number; kb?: [number, number]; foco?: [number, number]; focoFim?: [number, number]; filtro?: string }> = ({
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
  const z = lerp(t, 0, dur, kb[0], kb[1], lin);
  const fim = focoFim ?? foco;
  const fx = lerp(t, 0, dur, foco[0], fim[0], easeInOut);
  const fy = lerp(t, 0, dur, foco[1], fim[1], easeInOut);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
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

/** Gancho "ficção → real": grade fria com varredura até a palavra "real"; clarão e cor natural depois. */
const FotoScifi: React.FC<{ src: string; w: number; h: number; t: number; dur: number; cena: Cena }> = ({ src, w, h, t, dur, cena }) => {
  const real = cena.marcos?.real ?? Infinity;
  const ficcao = t < real;
  const pisca = ficcao ? 1 + 0.035 * Math.sin(t * 37) * Math.sin(t * 11) : 1; // cintilação leve de tela
  const clarao = t >= real ? 1 - clamp01((t - real) / (5 / 30)) : 0; // 5 quadros: o "Clarão de volta" do guia
  const desloc = ficcao ? 5 : 0;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, filter: ficcao ? `brightness(${pisca})` : undefined }}>
        <Foto src={src} w={w} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} filtro={ficcao ? SCIFI : `${GRADE_FOTO} saturate(1.12)`} />
      </div>
      {ficcao && (
        <>
          {/* franja de cor (aberração cromática) só na versão "ficção" */}
          <div style={{ position: "absolute", inset: 0, translate: `${desloc}px 0`, mixBlendMode: "screen", opacity: 0.22 }}>
            <Foto src={src} w={w} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} filtro="grayscale(1) sepia(1) hue-rotate(-50deg) saturate(5) brightness(0.6)" />
          </div>
          <div style={{ position: "absolute", inset: 0, background: "repeating-linear-gradient(to bottom, rgba(0,0,0,0.22) 0px, rgba(0,0,0,0.22) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 5px)" }} />
          <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 45%, rgba(0,20,26,0.65) 100%)" }} />
        </>
      )}
      {clarao > 0 && <div style={{ position: "absolute", inset: 0, background: "#FFF6E6", opacity: 0.92 * clarao }} />}
    </div>
  );
};

/** Desenho de traço que "se escreve" (stroke-dashoffset) entre t0 e t0 + d. */
const Traco: React.FC<{ d: string; t: number; t0: number; dur: number; cor?: string; largura?: number; comp?: number }> = ({ d, t, t0, dur, cor = PALETA.papel, largura = 7, comp = 3000 }) => {
  const k = clamp01((t - t0) / dur);
  if (k <= 0) return null;
  return <path d={d} fill="none" stroke={cor} strokeWidth={largura} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={comp} strokeDashoffset={comp * (1 - ease(k))} />;
};

/** "Parece que alguém pegou um guarda-chuva gigante e colocou em cima de um tronco": traço sobre a foto real da árvore. */
const GuardaChuva: React.FC<{ p: PropsSocotra; cena: Cena; t: number; dur: number }> = ({ p, cena, t, dur }) => {
  const m = cena.marcos ?? {};
  const h = p.costura;
  const src = p.imagens[cena.foto ?? ""].arquivo;
  const z = lerp(t, 0, dur, 1.0, 1.04, lin);
  // geometria medida na foto (recorte 1080 × 900): ápice da copa em (550, 80), bordas em (38, 350) e (1062, 425)
  const desce = easeInOut(clamp01((t - m.colocou) / 0.5));
  const quica = t > m.colocou + 0.5 ? Math.sin(clamp01((t - m.colocou - 0.5) / 0.25) * Math.PI) * -10 : 0;
  const dy = -230 * (1 - desce) + quica;
  const esc = 0.82 + 0.18 * desce;
  const escuro = lerp(t, m.guarda - 0.2, m.guarda + 0.2, 0, 1) * (1 - 0.5 * lerp(t, m.tronco + 0.3, m.tronco + 0.8, 0, 1));
  const rim = 300;
  const n = 8;
  const pontas = Array.from({ length: n + 1 }, (_, i) => -515 + (1030 * i) / n);
  const copa = "M -515 300 C -455 70 -235 0 0 0 C 235 0 455 70 515 300";
  const recortes = pontas.slice(0, -1).map((x, i) => `M ${x} ${rim} Q ${x + 1030 / n / 2} ${rim - 42} ${pontas[i + 1]} ${rim}`).join(" ");
  const varetas = pontas.map((x) => `M 0 4 Q ${x * 0.55} ${40 + Math.abs(x) * 0.06} ${x} ${rim}`).join(" ");
  const gotas = [
    { x: 528, y0: 545, y1: 700, a: 0 },
    { x: 590, y0: 548, y1: 655, a: 0.15 },
    { x: 556, y0: 600, y1: 790, a: 0.3 },
  ];
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, scale: String(z), transformOrigin: "50% 40%" }}>
        <Foto src={src} w={p.largura} h={h} t={0} dur={1} kb={[1, 1]} filtro={`${GRADE_FOTO} brightness(${1 - 0.42 * escuro})`} />
        <svg width={p.largura} height={h} style={{ position: "absolute", inset: 0, overflow: "visible", filter: "drop-shadow(0 3px 6px rgba(0,0,0,0.55))" }}>
          <g transform={`translate(550 ${80 + dy}) rotate(4.4) scale(${esc})`}>
            <Traco d={copa} t={t} t0={m.guarda} dur={0.45} comp={1400} />
            <Traco d={recortes} t={t} t0={m.guarda + 0.2} dur={0.35} largura={6} comp={2200} />
            <Traco d={varetas} t={t} t0={m.guarda + 0.3} dur={0.4} largura={4} comp={5200} />
            {/* cabo do guarda-chuva enquanto ele flutua; some quando o tronco assume o lugar dele */}
            <g opacity={1 - clamp01((t - m.tronco) / 0.3)}>
              <Traco d="M 0 4 L 0 330 Q 0 372 -40 372 Q -70 372 -70 342" t={t} t0={m.guarda + 0.35} dur={0.35} largura={6} comp={600} />
            </g>
          </g>
          {/* tronco: contorno real da foto (x 512–600, y 530–875) */}
          <Traco d="M 515 532 C 508 640 505 760 492 872 M 598 532 C 604 640 606 760 630 872" t={t} t0={m.tronco} dur={0.4} largura={6} comp={760} />
          {gotas.map((g, i) => {
            const k = clamp01((t - m.sangue - g.a) / 0.7);
            if (k <= 0) return null;
            const y = g.y0 + (g.y1 - g.y0) * ease(k);
            return (
              <g key={i}>
                <path d={`M ${g.x} ${g.y0} L ${g.x} ${y}`} stroke={VERMELHO} strokeWidth={9} strokeLinecap="round" />
                <path d={`M ${g.x} ${y - 6} q 11 18 0 26 q -11 -8 0 -26 z`} fill={VERMELHO} />
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};

/** Estrelas para o cosmos: pontos fixos que se afastam do centro (câmera avançando). */
const Estrelas: React.FC<{ t: number; fade: number }> = ({ t, fade }) => {
  const pts = React.useMemo(
    () => Array.from({ length: 240 }, (_, i) => ({ a: random(`a${i}`) * Math.PI * 2, r: 40 + random(`r${i}`) * 1150, s: 0.8 + random(`s${i}`) * 2.2, b: 0.35 + random(`b${i}`) * 0.65 })),
    [],
  );
  const k = Math.pow(1.22, t);
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: fade }}>
      {pts.map((s, i) => {
        const r = s.r * k;
        const x = 540 + Math.cos(s.a) * r;
        const y = 820 + Math.sin(s.a) * r;
        if (x < -10 || x > 1090 || y < -10 || y > 1930) return null;
        return <circle key={i} cx={x} cy={y} r={s.s * Math.min(2, k * 0.9)} fill={PALETA.papel} opacity={s.b * (0.75 + 0.25 * Math.sin(t * 5 + i))} />;
      })}
    </svg>
  );
};

/** Planeta fictício (só traço): "isso não é Pandora e nenhum planeta distante". Não imita nenhum filme. */
const PlanetaFicticio: React.FC<{ t: number; m: Record<string, number> }> = ({ t, m }) => {
  const entra = ease(clamp01((t - m.pandora) / 0.35));
  const sai = easeInOut(clamp01((t - m.distante) / 0.7));
  if (entra <= 0 || sai >= 1) return null;
  const esc = (0.6 + 0.4 * entra) * (1 - 0.85 * sai);
  const x = 540 - 260 * sai;
  const y = 780 - 420 * sai;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: entra * (1 - sai) }}>
      <defs>
        <clipPath id="pf">
          <circle cx={0} cy={0} r={230} />
        </clipPath>
        <radialGradient id="pfg" cx="35%" cy="30%" r="80%">
          <stop offset="0%" stopColor="#1E5A5E" />
          <stop offset="100%" stopColor="#0B0A09" />
        </radialGradient>
      </defs>
      <g transform={`translate(${x} ${y}) scale(${esc}) rotate(-18)`}>
        <ellipse cx={0} cy={0} rx={420} ry={92} fill="none" stroke={PALETA.papel} strokeWidth={5} opacity={0.55} />
        <circle cx={0} cy={0} r={230} fill="url(#pfg)" stroke={PALETA.papel} strokeWidth={6} />
        <g clipPath="url(#pf)" stroke={PALETA.papel} strokeWidth={3} opacity={0.45} fill="none">
          {[-150, -90, -30, 30, 90, 150].map((yy) => (
            <path key={yy} d={`M -240 ${yy} Q 0 ${yy + 26} 240 ${yy}`} />
          ))}
        </g>
        <path d="M -420 0 A 420 92 0 0 0 420 0" fill="none" stroke={PALETA.papel} strokeWidth={5} opacity={0.9} />
      </g>
    </svg>
  );
};

const SOCOTRA_LONLAT: [number, number] = [53.85, 12.5];
const IEMEN_LONLAT: [number, number] = [46.2, 15.9];
const FINAL = { lon: 50.5, lat: 14.6, R: 4300 };
const CENTRO_Y = 760;

/** Cosmos → Terra → Socotra: um só movimento de câmera, com o mapa real (Natural Earth, domínio público). */
const Cosmos: React.FC<{ t: number; m: Record<string, number> }> = ({ t, m }) => {
  const nasce = ease(clamp01((t - m.terra) / 0.55));
  const gira = easeInOut(clamp01((t - m.terra) / (m.zoom + 0.9 - m.terra)));
  const zk = easeInOut(clamp01((t - m.zoom) / 0.95));
  const lon = lerp(gira, 0, 1, -38, FINAL.lon, lin);
  const lat = lerp(gira, 0, 1, -8, FINAL.lat, lin);
  const R0 = 360 * nasce;
  const R = R0 * Math.pow(FINAL.R / 360, zk);
  const proj = geoOrthographic().rotate([-lon, -lat]).scale(Math.max(1, R)).translate([540, CENTRO_Y]).clipAngle(90).precision(0.3);
  const path = geoPath(proj);
  const detalhe = clamp01((R - 1200) / 1600); // troca do contorno de 110 m pelo de 10 m durante o zoom
  const terraFill = `rgba(236,229,216,${0.9 - 0.5 * detalhe})`;
  const pino = proj(SOCOTRA_LONLAT) ?? [0, 0];
  const iem = proj(IEMEN_LONLAT) ?? [0, 0];
  const ks = clamp01((t - m.socotra) / 0.3);
  const ki = clamp01((t - m.iemen) / 0.3);
  const yem = REGIAO.features.find((f) => f.properties.iso === "YEM");
  const ehSocotra = (poly: number[][][]) => poly[0].every(([x, y]) => x > 52 && x < 55.2 && y > 11.8 && y < 13.2);
  const ilhas = yem ? { type: "MultiPolygon" as const, coordinates: yem.geometry.coordinates.filter(ehSocotra) } : null;
  const continente = yem ? { type: "MultiPolygon" as const, coordinates: yem.geometry.coordinates.filter((pp) => !ehSocotra(pp)) } : null;
  if (nasce <= 0) return null;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
      <defs>
        <radialGradient id="atm" cx="50%" cy="50%" r="50%">
          <stop offset="86%" stopColor="rgba(224,174,92,0)" />
          <stop offset="100%" stopColor="rgba(224,174,92,0.16)" />
        </radialGradient>
        <filter id="brilho" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="10" />
        </filter>
      </defs>
      {R < 3000 && <circle cx={540} cy={CENTRO_Y} r={R * 1.08} fill="url(#atm)" opacity={1 - detalhe} />}
      <path d={path({ type: "Sphere" }) ?? ""} fill="#15202A" stroke={PALETA.papel} strokeOpacity={0.5 * (1 - detalhe)} strokeWidth={2} />
      <path d={path(geoGraticule10()) ?? ""} fill="none" stroke={PALETA.papel} strokeOpacity={0.1 * (1 - detalhe)} strokeWidth={1} />
      {detalhe < 1 && <path d={path(TERRA) ?? ""} fill={terraFill} opacity={1 - detalhe} />}
      {detalhe > 0 && (
        <g opacity={detalhe}>
          <path d={path(REGIAO) ?? ""} fill={terraFill} stroke={PALETA.papel} strokeOpacity={0.55} strokeWidth={1.6} />
        </g>
      )}
      {continente && ki > 0 && (
        <path d={path(continente) ?? ""} fill={`rgba(224,174,92,${0.22 * ki})`} stroke={PALETA.ambar} strokeWidth={3} strokeOpacity={ki} />
      )}
      {ilhas && ks > 0 && (
        <>
          <path d={path(ilhas) ?? ""} fill={PALETA.ambar} opacity={0.8 * ks} filter="url(#brilho)" />
          <path d={path(ilhas) ?? ""} fill={PALETA.ambar} stroke="#FFF2D6" strokeWidth={1.5} opacity={ks} />
          {[0, 0.45].map((a) => {
            const k = clamp01((t - m.socotra - a) / 0.9);
            return k > 0 && k < 1 ? <circle key={a} cx={pino[0]} cy={pino[1]} r={40 + 150 * ease(k)} fill="none" stroke={PALETA.ambar} strokeWidth={4} opacity={1 - k} /> : null;
          })}
        </>
      )}
      {ks > 0 && (
        <text x={pino[0]} y={pino[1] + 118} textAnchor="middle" style={{ font: `400 76px ${TITULO}`, letterSpacing: 2 }} fill={PALETA.branco} opacity={ks}>
          SOCOTRA
        </text>
      )}
      {ki > 0 && (
        <text x={iem[0]} y={iem[1]} textAnchor="middle" style={{ font: `400 64px ${TITULO}`, letterSpacing: 2 }} fill={PALETA.branco} opacity={ki}>
          IÊMEN
        </text>
      )}
    </svg>
  );
};

/** "Cerca de 37% das espécies de plantas": anel âmbar que enche até 37% e contador. */
const Fracao37: React.FC<{ t: number; marco: number; fundo?: string }> = ({ t, marco, fundo }) => {
  const k = ease(clamp01((t - marco) / 0.75));
  const r = 300;
  const circ = 2 * Math.PI * r;
  const num = Math.round(37 * k);
  const entra = ease(clamp01(t / 0.25));
  return (
    <AbsoluteFill style={{ background: PALETA.fundo }}>
      {fundo && <Foto src={fundo} w={1080} h={1920} t={t} dur={3} kb={[1.08, 1.0]} filtro="grayscale(0.5) brightness(0.3) blur(2px)" />}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: entra }}>
        <circle cx={540} cy={CENTRO_Y} r={r} fill="none" stroke={PALETA.papel} strokeOpacity={0.2} strokeWidth={26} />
        <circle
          cx={540}
          cy={CENTRO_Y}
          r={r}
          fill="none"
          stroke={PALETA.ambar}
          strokeWidth={26}
          strokeLinecap="butt"
          strokeDasharray={`${circ * 0.37 * k} ${circ}`}
          transform={`rotate(-90 540 ${CENTRO_Y})`}
        />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: CENTRO_Y, translate: "0 -50%", textAlign: "center", font: `400 230px ${TITULO}`, lineHeight: 1, color: PALETA.branco, opacity: clamp01((t - marco + 0.05) / 0.12), scale: String(0.9 + 0.1 * k) }}>
        {num}
        <span style={{ fontSize: 120 }}>%</span>
      </div>
    </AbsoluteFill>
  );
};

/** Avião de papel (traço) que sai na palavra "manda", contornando o rosto pela esquerda. */
const Aviao: React.FC<{ t: number; t0: number }> = ({ t, t0 }) => {
  const k = clamp01((t - t0) / 0.85);
  if (k <= 0 || k >= 1) return null;
  const P = [
    [150, 1290],
    [90, 620],
    [700, 380],
    [990, 300],
  ];
  const b = (u: number) => {
    const v = 1 - u;
    return [0, 1].map((i) => v * v * v * P[0][i] + 3 * v * v * u * P[1][i] + 3 * v * u * u * P[2][i] + u * u * u * P[3][i]);
  };
  const u = easeInOut(k);
  const [x, y] = b(u);
  const [x2, y2] = b(Math.min(1, u + 0.01));
  const ang = (Math.atan2(y2 - y, x2 - x) * 180) / Math.PI;
  const rastro = Array.from({ length: 24 }, (_, i) => b((u * i) / 23));
  const op = k < 0.85 ? 1 : 1 - (k - 0.85) / 0.15;
  return (
    <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: op, filter: "drop-shadow(0 3px 8px rgba(0,0,0,0.6))" }}>
      <polyline points={rastro.map(([a, c]) => `${a},${c}`).join(" ")} fill="none" stroke={PALETA.papel} strokeWidth={5} strokeDasharray="14 14" strokeLinecap="round" opacity={0.85} />
      <g transform={`translate(${x} ${y}) rotate(${ang}) scale(1.6)`}>
        <path d="M 40 0 L -30 -26 L -14 0 L -30 26 Z" fill={PALETA.ambar} stroke={PALETA.preto} strokeWidth={2} strokeLinejoin="round" />
        <path d="M 40 0 L -14 0 L -22 14 Z" fill="#B98A3E" />
      </g>
    </svg>
  );
};

/** Imagem de apoio da cena (atrás do Diego, ou acima dele na tela dividida). */
const Apoio: React.FC<{ p: PropsSocotra; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps;
  const dur = ((cena.continua ? p.quadros : cena.fim_q) - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  const m = cena.marcos ?? {};
  if (cena.tipo === "foto" && cena.foto) {
    const src = p.imagens[cena.foto].arquivo;
    if (cena.efeito === "scifi") return <FotoScifi src={src} w={p.largura} h={h} t={t} dur={dur} cena={cena} />;
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
        <Foto src={src} w={p.largura} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} focoFim={cena.foco_fim} />
        {/* tela cheia: degradê de base para a legenda branca (y 1320) se ler sobre céu e areia claros */}
        {!split && <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 960, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.62) 100%)" }} />}
      </div>
    );
  }
  if (cena.tipo === "anim") {
    if (cena.anim === "guarda") return <GuardaChuva p={p} cena={cena} t={t} dur={dur} />;
    if (cena.anim === "fracao") return <Fracao37 t={t} marco={m.numero ?? 0.3} fundo={cena.fundo ? p.imagens[cena.fundo].arquivo : undefined} />;
    if (cena.anim === "cosmos")
      return (
        <AbsoluteFill style={{ background: PALETA.preto }}>
          <Estrelas t={t} fade={1 - 0.6 * clamp01((t - m.zoom) / 0.6)} />
          <PlanetaFicticio t={t} m={m} />
          <Cosmos t={t} m={m} />
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 760, background: "linear-gradient(to bottom, rgba(11,10,9,0) 0%, rgba(11,10,9,0.55) 60%, rgba(11,10,9,0.7) 100%)" }} />
        </AbsoluteFill>
      );
  }
  return null;
};

/** Legenda: 1 a 4 palavras, Inter 800 66 px com sombra; palavra de destaque em âmbar (padrão do formato). */
const Legenda: React.FC<{ p: PropsSocotra; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  const y = posicaoFala(cena) === "baixo" ? p.costura : 1320;
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

/** Gancho: a 1ª frase falada, em letras grandes, à esquerda sobre a imagem; cada linha entra quando é dita. */
const Gancho: React.FC<{ p: PropsSocotra; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length || tS >= p.fimGancho) return null;
  const linha = (txt: string, tam: number, ini: number, k: number) => {
    const e = ini <= 0 ? 1 : ease(Math.min(1, Math.max(0, (tS - ini) / 0.16)));
    return (
      <div key={k} style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 1.02, color: PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
        {txt}
      </div>
    );
  };
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 240, height: p.costura - 240, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.45) 40%, rgba(0,0,0,0.72) 100%)" }} />
      <div style={{ position: "absolute", left: 72, right: 72, top: p.ganchoLayout.topo, textShadow: "0 4px 30px rgba(0,0,0,0.45)" }}>
        {p.gancho.map((b, i) => (
          <React.Fragment key={i}>
            {i > 0 && <div style={{ height: 18 }} />}
            {b.linhas.map((l, k) => linha(l, b.tamanhos[k], b.tempos[k], i * 10 + k))}
          </React.Fragment>
        ))}
      </div>
    </>
  );
};

/** Grão de película do formato (não é o grão do DS). */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-socotra">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-socotra)" />
  </svg>
);

export const ReelSocotra: React.FC<PropsSocotra> = (p) => {
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
          <Sequence key={c.id} from={c.ini_q} durationInFrames={(c.continua ? p.quadros : c.fim_q) - c.ini_q} premountFor={20} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {cena.tipo === "fala" && cena.marcos?.manda !== undefined && <Aviao t={t} t0={cena.marcos.manda} />}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
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
