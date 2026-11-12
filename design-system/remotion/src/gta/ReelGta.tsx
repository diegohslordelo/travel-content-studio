/**
 * Reel GTA 6 × Miami · tela dividida (reels/gta6-miami/rev1). Props montadas por reels/gta6-miami/scripts/montar.py.
 * Camadas: Diego (um só vídeo contínuo, já decupado: metade de baixo ou tela cheia) · apoio na metade de cima
 * (plano recortado, foto ou animação) · costura com as listras do pôr do sol · legenda · gancho · 975 MIL · CTA do DS V2.
 * Cores do GTA VI só neste Reel (pedido do Diego, 12/11/2026). Sem ajuste de cor no vídeo do Diego. O áudio é mixado
 * fora (scripts/mixar.py) e juntado no fim: esta composição sai muda.
 */
import React from "react";
import { Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Placa } from "../ds/Placa";
import { Banana, Barra, Carta, Comparar, Condado, Contador, FotoKB, Marcos, Xerife } from "./Graficos";
import { PORDOSOL, SOMBRA_TXT, TEXTO, TITULO, VC, clamp01, ease, lerp } from "./estilo";

type Cena = {
  id: string;
  tipo: "clipe" | "foto" | "anim" | "diego";
  ini_q: number;
  fim_q: number;
  arquivo?: string;
  anim?: "contador" | "banana" | "barra" | "condado" | "xerife" | "carta" | "comparar";
  marcos?: Marcos;
  fotos?: [string, string];
  focos?: [[number, number], [number, number]];
  kb?: [number, number];
  foco?: [number, number];
  foco_fim?: [number, number];
  racha?: number; // s desde o início da cena: a imagem racha ao meio ("partindo a cidade no meio")
  zoom?: [number, number];
};
type Palavra = { texto: string; destaque: boolean };
export type PropsGta = {
  fps: number;
  quadros: number;
  costura: number;
  rostoY: number;
  cenas: Cena[];
  gancho: { topo: number; fim: number; linhas: { texto: string; tam: number; ini: number; grad?: boolean }[] };
  legendas: { ini: number; fim: number; palavras: Palavra[] }[];
  numero: { ini: number; fim: number; partes: { texto: string; em: number }[] };
  batidas: number[];
  luz: number[];
  cta: { ini: number; rotulo: string; destino: string; entrada: number };
};

export const propsVaziasGta: PropsGta = {
  fps: 30,
  quadros: 30,
  costura: 900,
  rostoY: 760,
  cenas: [],
  gancho: { topo: 275, fim: 0, linhas: [] },
  legendas: [],
  numero: { ini: 0, fim: 0, partes: [] },
  batidas: [],
  luz: [],
  cta: { ini: 0, rotulo: "", destino: "", entrada: 200 },
};

export const metadadosGta: CalculateMetadataFunction<PropsGta> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: 1080,
  height: 1920,
});

const W = 1080;
const H = 1920;

/** Batida do "975 mil": chacoalho e soco de zoom que decaem em ~0,25 s. */
const impacto = (tS: number, batidas: number[]) => {
  let z = 0;
  let dx = 0;
  let dy = 0;
  for (const b of batidas) {
    const d = tS - b;
    if (d < 0 || d > 0.4) continue;
    const k = Math.exp(-d * 14);
    z += 0.06 * k;
    dx += 16 * k * Math.sin(d * 95);
    dy += 10 * k * Math.cos(d * 80);
  }
  return { z, dx, dy };
};

/** Diego: um só vídeo contínuo, na metade de baixo (tela dividida) ou em tela cheia. */
const Diego: React.FC<{ p: PropsGta; cena: Cena; t: number; tS: number }> = ({ p, cena, t, tS }) => {
  const cheia = cena.tipo === "diego";
  let box: React.CSSProperties = { top: 0, height: H };
  let video: React.CSSProperties = {};
  if (cheia) {
    const dur = (cena.fim_q - cena.ini_q) / p.fps;
    const z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    const im = impacto(tS, p.batidas);
    video = { scale: String(z + im.z), translate: `${im.dx}px ${im.dy}px`, transformOrigin: `540px ${p.rostoY}px` };
  } else {
    const h = H - p.costura;
    box = { top: p.costura, height: h };
    video = { translate: `0 ${Math.round(h * 0.42 - (p.rostoY - 0))}px` }; // rosto a 42% da metade de baixo
  }
  return (
    <div style={{ position: "absolute", left: 0, width: W, overflow: "hidden", ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: W, height: H }} />
      </div>
    </div>
  );
};

/** Plano em vídeo; com "racha", a imagem parte ao meio por uma rachadura de néon. */
const Clipe: React.FC<{ cena: Cena; t: number }> = ({ cena, t }) => {
  const v = <Video src={staticFile(cena.arquivo!)} muted style={{ width: W, height: 900 }} />;
  if (cena.racha === undefined || t < cena.racha) return <div style={{ position: "absolute", inset: 0, width: W, height: 900, overflow: "hidden" }}>{v}</div>;
  const d = lerp(t, cena.racha, cena.racha + 0.35, 0, 64, ease);
  const zig = "56% 0%, 50% 14%, 57% 27%, 48% 41%, 55% 55%, 46% 69%, 53% 84%, 47% 100%";
  const esq = `polygon(0% 0%, ${zig}, 0% 100%)`;
  const dir = `polygon(${zig}, 100% 100%, 100% 0%)`;
  const brilho = 0.6 + 0.4 * Math.sin(t * 30);
  return (
    <div style={{ position: "absolute", inset: 0, width: W, height: 900, overflow: "hidden", background: VC.preto }}>
      <svg width={W} height={900} style={{ position: "absolute", inset: 0 }}>
        <polyline
          points={zig.split(", ").map((s) => { const [x, y] = s.split(" ").map((n) => parseFloat(n)); return `${(x / 100) * W},${(y / 100) * 900}`; }).join(" ")}
          fill="none"
          stroke={VC.rosa}
          strokeWidth={10 + d * 0.6}
          opacity={brilho}
          style={{ filter: "blur(6px)" }}
        />
      </svg>
      <div style={{ position: "absolute", inset: 0, clipPath: esq, translate: `${-d}px ${d * 0.25}px`, rotate: `${-d * 0.03}deg` }}>{v}</div>
      <div style={{ position: "absolute", inset: 0, clipPath: dir, translate: `${d}px ${-d * 0.25}px`, rotate: `${d * 0.03}deg` }}>{v}</div>
    </div>
  );
};

/** Metade de cima: plano, foto ou animação da cena. */
const Apoio: React.FC<{ p: PropsGta; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps;
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const m = cena.marcos ?? {};
  const g = { t, m, w: W, h: 900 };
  let el: React.ReactNode = null;
  if (cena.tipo === "clipe") el = <Clipe cena={cena} t={t} />;
  else if (cena.tipo === "foto") el = <FotoKB src={cena.arquivo!} t={t} dur={dur} w={W} h={900} kb={cena.kb} foco={cena.foco} focoFim={cena.foco_fim} />;
  else if (cena.anim === "contador") el = <Contador {...g} />;
  else if (cena.anim === "banana") el = <Banana {...g} />;
  else if (cena.anim === "barra") el = <Barra {...g} />;
  else if (cena.anim === "condado") el = <Condado {...g} />;
  else if (cena.anim === "xerife") el = <Xerife {...g} />;
  else if (cena.anim === "carta") el = <Carta {...g} />;
  else if (cena.anim === "comparar" && cena.fotos) el = <Comparar {...g} a={cena.fotos[0]} b={cena.fotos[1]} focoA={cena.focos?.[0]} focoB={cena.focos?.[1]} />;
  return <div style={{ position: "absolute", left: 0, top: 0, width: W, height: 900, overflow: "hidden" }}>{el}</div>;
};

/** Costura da tela dividida: listras do pôr do sol (laranja, rosa, roxo). */
const Costura: React.FC<{ y: number }> = ({ y }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top: y - 5, height: 10 }}>
    <div style={{ height: 3, background: VC.laranja }} />
    <div style={{ height: 4, background: VC.rosa }} />
    <div style={{ height: 3, background: VC.lilas }} />
  </div>
);

/** Legenda: 1 a 4 palavras, Inter 800 66 px; a palavra de destaque em rosa néon (cor do GTA VI). */
const Legenda: React.FC<{ p: PropsGta; tS: number; cheia: boolean }> = ({ p, tS, cheia }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g) return null;
  // grupos ditos durante o gancho ou o 975 MIL ficam só no texto grande: não reaparecem como legenda depois
  if (g.ini < p.gancho.fim || (g.ini >= p.numero.ini - 0.2 && g.ini < p.numero.fim)) return null;
  const e = ease(Math.min(1, (tS - g.ini) / 0.12));
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: cheia ? 1320 : p.costura,
        translate: "0 -50%",
        textAlign: "center",
        padding: "0 90px",
        font: `800 66px ${TEXTO}`,
        lineHeight: 1.1,
        color: VC.branco,
        textShadow: "0 3px 0 rgba(0,0,0,0.4), 0 4px 22px rgba(0,0,0,0.9)",
        scale: String(0.94 + 0.06 * e),
        opacity: e,
        whiteSpace: "nowrap",
      }}
    >
      {g.palavras.map((w, i) => (
        <span key={i} style={{ color: w.destaque ? VC.rosa : undefined }}>
          {(i ? " " : "") + w.texto}
        </span>
      ))}
    </div>
  );
};

/** Gancho: a 1ª frase em letras grandes na metade de cima, linha a linha no tempo da fala. */
const Gancho: React.FC<{ p: PropsGta; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.linhas.length || tS >= p.gancho.fim) return null;
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: p.gancho.topo - 40, height: p.costura - p.gancho.topo + 40, background: "linear-gradient(to bottom, rgba(7,4,13,0) 0%, rgba(7,4,13,0.5) 30%, rgba(7,4,13,0.78) 100%)" }} />
      <div style={{ position: "absolute", left: 72, right: 72, top: p.gancho.topo }}>
        {p.gancho.linhas.map((l, k) => {
          const e = l.ini <= 0 ? 1 : ease(clamp01((tS - l.ini) / 0.16));
          const estilo: React.CSSProperties = l.grad
            ? { backgroundImage: PORDOSOL, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", filter: "drop-shadow(0 6px 0 rgba(0,0,0,0.5)) drop-shadow(0 0 30px rgba(255,61,154,0.45))" }
            : { color: VC.branco, textShadow: SOMBRA_TXT };
          return (
            <div key={k} style={{ font: `400 ${l.tam}px ${TITULO}`, lineHeight: 1.0, opacity: e, translate: `0 ${(1 - e) * 24}px`, ...estilo }}>
              {l.texto}
            </div>
          );
        })}
      </div>
    </>
  );
};

/** "975 MIL" em tela cheia: cada parte entra na palavra e pulsa em cada batida. */
const Numero: React.FC<{ p: PropsGta; tS: number }> = ({ p, tS }) => {
  const n = p.numero;
  if (tS < n.ini || tS >= n.fim) return null;
  const im = impacto(tS, p.batidas);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 1180, display: "flex", justifyContent: "center", gap: 34, translate: `${im.dx * 1.4}px ${im.dy}px`, scale: String(1 + im.z * 2.2) }}>
      {n.partes.map((pt, i) => {
        const e = (tS - pt.em) / 0.14;
        if (tS < pt.em) return null;
        return (
          <div
            key={i}
            style={{
              font: `400 260px ${TITULO}`,
              lineHeight: 1,
              backgroundImage: PORDOSOL,
              WebkitBackgroundClip: "text",
              backgroundClip: "text",
              color: "transparent",
              filter: "drop-shadow(0 10px 0 rgba(0,0,0,0.55)) drop-shadow(0 0 36px rgba(255,61,154,0.6))",
              scale: String(lerp(e, 0, 1, 1.6, 1, ease)),
              opacity: clamp01(e * 3),
            }}
          >
            {pt.texto}
          </div>
        );
      })}
    </div>
  );
};

/** Flash rosa curto em cada batida (só na tela cheia do 975 MIL). */
const Flash: React.FC<{ p: PropsGta; tS: number }> = ({ p, tS }) => {
  if (tS < p.numero.ini || tS >= p.numero.fim) return null;
  let a = 0;
  for (const b of p.batidas) if (tS >= b && tS - b < 0.2) a = Math.max(a, 0.28 * Math.exp(-(tS - b) * 18));
  return <div style={{ position: "absolute", inset: 0, background: VC.rosa, opacity: a, mixBlendMode: "screen" }} />;
};

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS 3.2 e 10.4): luz quente desce, pico ≤ 4 quadros a 85% com o corte escondido, recua. */
const Luz: React.FC<{ p: PropsGta; q: number }> = ({ p, q }) => {
  for (const s of p.luz) {
    const f = q - Math.round(s * p.fps);
    if (f < -5 || f > 5) continue;
    const a = f < -2 ? lerp(f, -5, -2, 0.08, 0.85, (x) => x) : f <= 1 ? 0.85 : lerp(f, 1, 5, 0.85, 0, (x) => x);
    return (
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: W,
          height: p.costura,
          opacity: a,
          background: `radial-gradient(ellipse at ${f > 1 ? 85 : 50}% 0%, ${VC.amarelo} 0%, ${VC.laranja} 35%, ${VC.rosa} 70%, rgba(255,61,154,0) 100%)`,
          mixBlendMode: "screen",
        }}
      />
    );
  }
  return null;
};

/** Grão leve só na metade de cima (o vídeo do Diego fica como ele editou). */
const Grao: React.FC<{ q: number; altura: number }> = ({ q, altura }) => (
  <svg width={W} height={altura} style={{ position: "absolute", left: 0, top: 0, opacity: 0.05, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-gta">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-gta)" />
  </svg>
);

export const ReelGta: React.FC<PropsGta> = (p) => {
  const q = useCurrentFrame();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: VC.preto }} />;
  const tS = q / p.fps;
  const cena = p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ?? p.cenas[p.cenas.length - 1];
  const t = (q - cena.ini_q) / p.fps;
  const cheia = cena.tipo === "diego";
  const naoLegenda = tS < p.gancho.fim || (tS >= p.numero.ini && tS < p.numero.fim);
  return (
    <AbsoluteFill style={{ background: VC.preto }}>
      <Diego p={p} cena={cena} t={t} tS={tS} />
      {p.cenas
        .filter((c) => c.tipo !== "diego")
        .map((c) => (
          <Sequence key={c.id} from={c.ini_q} durationInFrames={c.fim_q - c.ini_q} premountFor={30} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {!cheia && <Grao q={q} altura={p.costura} />}
      {!cheia && <Luz p={p} q={q} />}
      {!cheia && <Costura y={p.costura} />}
      <Flash p={p} tS={tS} />
      <Numero p={p} tS={tS} />
      {!naoLegenda && <Legenda p={p} tS={tS} cheia={cheia} />}
      <Gancho p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (placa de direção com verbo + seta, Chegada; o clack entra na mixagem) */}
      <Sequence from={Math.round(p.cta.ini * p.fps)} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={p.cta.entrada} />
      </Sequence>
    </AbsoluteFill>
  );
};
