/**
 * Reel "Casa de Anne Frank" · tela dividida (reels/anne-frank/rev1).
 * Camadas: imagem de apoio (vídeo, foto ou animação) · Diego (tela cheia, metade de baixo ou desfocado
 * como fundo do cartão) · rótulos · legendas · gancho · CTA.
 * O DS V2 aparece só no CTA final (Placa + clack), por decisão do Diego (24/10/2026).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import { Casa } from "./Casa";
import { Data, LinhaTempo, Pessoas, EstadoPessoas } from "./Graficos";
import { GRADE_FOTO, GRADE_VIDEO, PALETA, TEXTO, TITULO, ease, lerp } from "./estilo";

type Palavra = { texto: string; ini: number; fim: number; destaque: boolean };
type Grupo = { palavras: Palavra[]; ini: number; fim: number };
type Imagem = { arquivo: string; rotulo: string; credito: string };
type Cena = {
  id: string;
  tipo: "broll" | "foto" | "fala" | "anim" | "cta";
  ini_q: number;
  fim_q: number;
  arquivo?: string;
  layout?: "full" | "split" | "card";
  kb?: [number, number];
  foco?: [number, number];
  foto?: string;
  anim?: "casa" | "linha" | "pessoas" | "data";
  estado?: EstadoPessoas;
  marcos?: Record<string, number>;
  numero?: { grande: string; pequeno: string; em: number };
  zoom?: [number, number];
  texto?: string[];
  tom?: "escuro";
};
export type PropsAF = {
  fps: number;
  largura: number;
  altura: number;
  costura: number;
  rostoY: number;
  quadros: number;
  fimFalas: number;
  cenas: Cena[];
  imagens: Record<string, Imagem>;
  gancho: { linhas: string[]; em: number }[];
  legendas: Grupo[];
  cta: { ini: number; duracao: number; rotulo: string; destino: string };
  mix: { voz_lufs: number; clack_db_rel: number };
};

export const propsVaziasAF: PropsAF = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  costura: 900,
  rostoY: 560,
  quadros: 30,
  fimFalas: 0,
  cenas: [],
  imagens: {},
  gancho: [],
  legendas: [],
  cta: { ini: 0, duracao: 1, rotulo: "", destino: "" },
  mix: { voz_lufs: -14, clack_db_rel: -10 },
};

export const metadadosAF: CalculateMetadataFunction<PropsAF> = ({ props }) => ({
  durationInFrames: Math.max(1, props.quadros),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Layout da cena: onde fica o Diego. */
const posicaoFala = (c: Cena): "cheia" | "baixo" | "fundo" | "fora" => {
  if (c.tipo === "fala") return "cheia";
  if (c.layout === "split") return "baixo";
  if (c.layout === "card") return "fundo";
  return "fora";
};

/** Diego: um único vídeo contínuo (a fala concatenada), reposicionado a cada cena. */
const Fala: React.FC<{ p: PropsAF; cena: Cena; t: number }> = ({ p, cena, t }) => {
  const pos = posicaoFala(cena);
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  let box: React.CSSProperties = { top: 0, height: p.altura };
  let video: React.CSSProperties = {};
  if (pos === "cheia") {
    const z = cena.zoom ? lerp(t, 0, dur, cena.zoom[0], cena.zoom[1], (x) => x) : 1;
    video = { scale: String(z), transformOrigin: `540px ${p.rostoY}px` };
  } else if (pos === "baixo") {
    const h = p.altura - p.costura;
    box = { top: p.costura, height: h };
    // rosto a 42% da metade de baixo
    video = { translate: `0 ${Math.round(h * 0.42 - p.rostoY)}px` };
  } else if (pos === "fundo") {
    video = { scale: "1.15", filter: "blur(26px) grayscale(1) brightness(0.42)" };
  }
  return (
    <div style={{ position: "absolute", left: 0, width: p.largura, overflow: "hidden", opacity: pos === "fora" ? 0 : 1, ...box }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: p.altura, ...video }}>
        <Video src={staticFile("fala.mp4")} muted style={{ width: p.largura, height: p.altura }} />
      </div>
    </div>
  );
};

const Foto: React.FC<{ src: string; w: number; h: number; t: number; dur: number; kb?: [number, number]; foco?: [number, number]; filtro?: string }> = ({
  src,
  w,
  h,
  t,
  dur,
  kb = [1, 1.05],
  foco = [0.5, 0.5],
  filtro = GRADE_FOTO,
}) => {
  const z = lerp(t, 0, dur, kb[0], kb[1], (x) => x);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "hidden", background: PALETA.preto }}>
      <Img
        src={staticFile(src)}
        style={{
          width: w,
          height: h,
          objectFit: "cover",
          objectPosition: `${foco[0] * 100}% ${foco[1] * 100}%`,
          scale: String(z),
          transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`,
          filter: filtro,
        }}
      />
    </div>
  );
};

/** Rótulo da imagem de apoio: o que é e quando (crédito completo na legenda do post e no QA). */
const Rotulo: React.FC<{ texto: string; credito?: string; x?: number; y: number; t: number }> = ({ texto, credito, x = 72, y, t }) => (
  <div style={{ position: "absolute", left: x, top: y, opacity: lerp(t, 0.12, 0.4, 0, 1), translate: `${lerp(t, 0.12, 0.4, -12, 0)}px 0` }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
      <div style={{ width: 6, height: 34, background: PALETA.ambar }} />
      <div style={{ font: `700 28px ${TEXTO}`, color: PALETA.branco, textShadow: "0 2px 10px rgba(0,0,0,0.85)" }}>{texto}</div>
    </div>
    {credito && <div style={{ font: `600 18px ${TEXTO}`, color: "rgba(255,255,255,0.7)", marginLeft: 20, marginTop: 4, textShadow: "0 1px 6px rgba(0,0,0,0.9)" }}>{credito}</div>}
  </div>
);

/** Número em destaque sobre a imagem de cima ("13 anos", "1960"). */
const Numero: React.FC<{ n: { grande: string; pequeno: string; em: number }; t: number; y: number }> = ({ n, t, y }) => {
  const p = lerp(t, n.em - 0.08, n.em + 0.22, 0, 1);
  if (p <= 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        right: 72,
        top: y,
        textAlign: "right",
        opacity: p,
        scale: String(0.9 + 0.1 * p),
        transformOrigin: "100% 100%",
        textShadow: "0 6px 30px rgba(0,0,0,0.7)",
        color: PALETA.branco,
      }}
    >
      <span style={{ font: `400 230px ${TITULO}`, lineHeight: 1 }}>{n.grande}</span>
      {n.pequeno && <span style={{ font: `400 90px ${TITULO}`, marginLeft: 16 }}>{n.pequeno}</span>}
    </div>
  );
};

/** Imagem de apoio da cena (atrás do Diego, ou acima dele na tela dividida). */
const Apoio: React.FC<{ p: PropsAF; cena: Cena }> = ({ p, cena }) => {
  const t = useCurrentFrame() / p.fps; // relativo ao início da cena (Sequence)
  const dur = (cena.fim_q - cena.ini_q) / p.fps;
  const split = cena.layout === "split";
  const h = split ? p.costura : p.altura;
  if (cena.tipo === "broll" && cena.arquivo) {
    const z = cena.kb ? lerp(t, 0, cena.id === "marcas" ? dur + p.cta.duracao : dur, cena.kb[0], cena.kb[1], (x) => x) : 1;
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: h, overflow: "hidden" }}>
        <div style={{ width: p.largura, height: h, scale: String(z), filter: GRADE_VIDEO }}>
          <Video src={staticFile(cena.arquivo)} muted style={{ width: p.largura, height: h }} />
        </div>
      </div>
    );
  }
  if (cena.tipo === "foto" && cena.foto) {
    const im = p.imagens[cena.foto];
    if (cena.layout === "card") {
      // cartão flutuante sobre o Diego desfocado (como nas referências)
      const e = ease(Math.min(1, t / 0.32));
      return (
        <div
          style={{
            position: "absolute",
            left: 140,
            top: 330,
            width: 800,
            height: 900,
            borderRadius: 20,
            overflow: "hidden",
            boxShadow: "0 30px 80px rgba(0,0,0,0.6)",
            opacity: e,
            scale: String(0.9 + 0.1 * e),
          }}
        >
          <Foto src={im.arquivo} w={800} h={900} t={t} dur={dur} kb={[1.0, 1.05]} foco={[0.5, 0.35]} />
        </div>
      );
    }
    const filtro = cena.tom === "escuro" ? "grayscale(0.85) brightness(0.55) contrast(1.1)" : im.arquivo.includes("diario") || im.arquivo.includes("2026") ? "saturate(0.55) contrast(1.05) brightness(0.95)" : GRADE_FOTO;
    return <Foto src={im.arquivo} w={p.largura} h={h} t={t} dur={dur} kb={cena.kb} foco={cena.foco} filtro={filtro} />;
  }
  if (cena.tipo === "anim") {
    const altura = split ? p.costura : p.altura;
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: p.largura, height: altura, overflow: "hidden" }}>
        {cena.anim === "casa" && (
          <Casa
            t={t}
            marcos={{
              armario: cena.marcos?.armario ?? 1.4,
              passagem: cena.marcos?.passagem ?? 2.6,
              anexo: cena.marcos?.anexo ?? 3.5,
            }}
          />
        )}
        {cena.anim === "linha" && <LinhaTempo t={t} altura={altura} />}
        {cena.anim === "pessoas" && <Pessoas t={t} altura={altura} estado={cena.estado ?? "apresenta"} marcos={cena.marcos ?? {}} />}
        {cena.anim === "data" && <Data t={t} linhas={cena.texto ?? []} />}
      </div>
    );
  }
  return null;
};

/** Legenda: 1 a 3 palavras, Inter 800 com sombra; palavra de destaque em âmbar. */
const Legenda: React.FC<{ p: PropsAF; tS: number; cena: Cena }> = ({ p, tS, cena }) => {
  const g = p.legendas.find((x) => tS >= x.ini && tS < x.fim);
  if (!g || cena.tipo === "cta") return null;
  const pos = posicaoFala(cena);
  const y = pos === "baixo" ? p.costura : pos === "fundo" ? 1375 : cena.anim === "casa" ? 1380 : 1320;
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

/** Gancho: a 1ª frase falada, em letras grandes, alinhada à esquerda sobre a imagem (como a capa de referência). */
const Gancho: React.FC<{ p: PropsAF; tS: number }> = ({ p, tS }) => {
  if (!p.gancho.length) return null;
  const fim = (p.cenas[1]?.ini_q ?? 0) / p.fps;
  if (tS >= fim) return null;
  const [b1, b2] = p.gancho;
  const linha = (txt: string, tam: number, ini: number, k: number) => {
    const e = ini <= 0 ? 1 : ease(Math.min(1, Math.max(0, (tS - ini) / 0.16)));
    return (
      <div key={k} style={{ font: `400 ${tam}px ${TITULO}`, lineHeight: 0.98, color: PALETA.branco, opacity: e, translate: `0 ${(1 - e) * 24}px` }}>
        {txt}
      </div>
    );
  };
  // o 2º bloco entra linha a linha, no tempo da fala (também · mais tristes · da cidade)
  const tempos2 = [b2.em, b2.em + 0.58, b2.em + 1.4];
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 1250, background: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0.7) 100%)" }} />
      <div style={{ position: "absolute", left: 72, right: 72, top: 690, textShadow: "0 4px 30px rgba(0,0,0,0.45)" }}>
        {b1.linhas.map((l, k) => linha(l, 128, b1.em, k))}
        <div style={{ height: 34 }} />
        {b2.linhas.map((l, k) => linha(l, k === 1 ? 196 : 104, tempos2[k], 10 + k))}
      </div>
    </>
  );
};

/** Grão de película próprio do Reel (não é o grão do DS). */
const Grao: React.FC<{ q: number }> = ({ q }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay", pointerEvents: "none" }}>
    <filter id="grao-af">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={q % 7} stitchTiles="stitch" />
    </filter>
    <rect width="100%" height="100%" filter="url(#grao-af)" />
  </svg>
);

export const ReelAnneFrank: React.FC<PropsAF> = (p) => {
  const q = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!p.cenas.length) return <AbsoluteFill style={{ background: PALETA.preto }} />;
  const tS = q / fps;
  const cena = p.cenas.find((c) => q >= c.ini_q && q < c.fim_q) ?? p.cenas[p.cenas.length - 1];
  // no CTA o último plano (entardecer) continua por baixo
  const visual = cena.tipo === "cta" ? p.cenas[p.cenas.length - 2] : cena;
  const t = (q - visual.ini_q) / fps;
  const im = visual.tipo === "foto" && visual.foto ? p.imagens[visual.foto] : null;
  const split = visual.layout === "split" && visual.tipo !== "fala";
  const ctaQ = Math.round(p.cta.ini * fps);

  return (
    <AbsoluteFill style={{ background: PALETA.preto }}>
      {/* fundo do cartão e Diego atrás das imagens de tela cheia */}
      <Fala p={p} cena={visual} t={t} />
      {p.cenas
        .filter((c) => c.tipo !== "cta" && c.tipo !== "fala")
        .map((c) => (
          <Sequence key={c.id} from={c.ini_q} durationInFrames={(c.id === "marcas" ? p.quadros : c.fim_q) - c.ini_q} premountFor={20} name={c.id}>
            <Apoio p={p} cena={c} />
          </Sequence>
        ))}
      {split && <div style={{ position: "absolute", left: 0, right: 0, top: p.costura - 3, height: 6, background: "rgba(0,0,0,0.55)" }} />}
      {im && cena.tipo !== "cta" && (
        <Rotulo
          texto={im.rotulo}
          credito={im.credito}
          t={t}
          y={visual.layout === "card" ? 1244 : 290}
          x={visual.layout === "card" ? 140 : 72}
        />
      )}
      {visual.numero && <Numero n={visual.numero} t={t} y={split ? 420 : 900} />}
      <Grao q={q} />
      <Legenda p={p} tS={tS} cena={cena} />
      <Gancho p={p} tS={tS} />
      {/* CTA: único lugar do Reel com o DS V2 (2.7: placa de direção com verbo + módulo de seta; Chegada; clack) */}
      <Sequence from={ctaQ} name="CTA (DS V2)">
        <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" entrada={200} />
        <Som nome="clack" em={200 + 280} relDb={p.mix.clack_db_rel} refLufs={p.mix.voz_lufs} />
      </Sequence>
      <Audio src={staticFile("voz.wav")} />
    </AbsoluteFill>
  );
};
