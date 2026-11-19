/**
 * Reel na linguagem do FORMATO (docs/FORMATOS_REELS.md e docs/REFERENCIA_EDICAO_FORMATOS.md), narrado sobre o acervo.
 * Primeiro uso: reels/bxl-decepcao/rev1 (Bruxelas × Bruges). Tudo vem das props (rev1/props_rev1.json, gerado por
 * rev1/montar_rev1.py) e do --public-dir do Reel; a voz, a trilha e os efeitos são mixados fora (rev1/mixar_rev1.py).
 *
 * DS só no CTA (decisão do Diego, 28/10/2026): do gancho até antes do CTA, só a linguagem do formato
 * (Anton no gancho, Inter 800 nas legendas, âmbar #E0AE5C de destaque, fundo #14120F nas animações, grão 6%).
 * O único componente do DS V2 é a Placa do CTA final (DS V2, 2.1 e 2.7), com a Chegada.
 *
 * Os valores do formato abaixo vêm de FORMATOS_REELS (2, 4, 5.4, 6) e não são tokens do DS: o formato tem
 * linguagem própria, adotada por decisão do Diego em Reels específicos (ver o cabeçalho daquele guia).
 */
import React from "react";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Easing,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { loadFont } from "@remotion/fonts";
import anton400 from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";
import { Placa } from "../ds/Placa";

// ---------------------------------------------------------------- linguagem do formato (FORMATOS_REELS)
const F = {
  fundo: "#14120F", // 5.4: fundo das animações
  traco: "#ECE5D8", // 5.4: traço
  ambar: "#E0AE5C", // 5.4 e 6: destaque
  costura: "rgba(0,0,0,0.55)", // 2: linha de 6 px entre metades
  sombraLegenda: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)", // 6
  margem: 72, // zona segura (DS V2): x 72–944
  centro: 540, // CLAUDE.md, 6: centro geométrico do canvas
};

let fontes: Promise<unknown> | null = null;
const carregar = () => {
  if (!fontes) {
    fontes = Promise.all([
      loadFont({ family: "Anton", url: anton400, weight: "400", display: "block" }),
      loadFont({ family: "Inter", url: inter800, weight: "800", display: "block" }),
    ]);
  }
  return fontes;
};
carregar();

// ---------------------------------------------------------------- props
type Plano = { arquivo: string; entra: number; fim: number; cidade: "bxl" | "bru"; rotulo?: string | null };
type Mapa = {
  caminho: string;
  altura: number;
  bruxelas: [number, number];
  bruges: [number, number];
  caixa: { x: number; y: number; w: number };
  marcos: { belgica?: number; ponto?: number; linha?: number; bruges?: number };
};
type Cena = {
  id: string;
  tipo: "video" | "split" | "grade" | "mapa" | "comparar";
  ini: number;
  fim: number;
  cidade: "bxl" | "bru";
  planos: Plano[];
  zoom?: [number, number];
  zoom_kf?: { t: number[]; z: number[] };
  origem?: string;
  desat?: { ini: number; fim: number; sat: number };
  grade_quente?: boolean;
  cinema?: number;
  luz?: boolean;
  modo?: "belgica" | "trem";
  mapa?: Mapa;
  cta?: boolean;
  entrada?: "dissolve";
  /** desfoque do fundo enquanto um recorte fica por cima (quadros: entra, sai) */
  desfoque?: { ini: number; fim: number };
  /** escurece a cena (foto clara em tela cheia com legenda: FORMATOS_REELS 3) */
  brilho?: number;
};
type Legenda = { texto: string; destaque: string | null; ini: number; fim: number };
export type PropsReelFormato = {
  fps: number;
  duracao: number;
  cenas: Cena[];
  gancho: { ate: number; linhas: { texto: string; em: number; tam: number; destaque?: boolean }[] };
  noticia: { arquivo: string; entra: number; destaque: number; sai: number; marca?: { x: number; y: number; w: number; h: number }; largura?: number; alturaImg?: number; larguraImg?: number };
  legendas: Legenda[];
  cta: { entra: number; destino: string; rotulo?: string };
  luz: { corte: number };
};

export const propsFormatoVazias: PropsReelFormato = {
  fps: 24,
  duracao: 24,
  cenas: [],
  gancho: { ate: 0, linhas: [] },
  noticia: { arquivo: "", entra: 0, destaque: 0, sai: 0 },
  legendas: [],
  cta: { entra: 0, destino: "" },
  luz: { corte: -100 },
};

export const metadadosFormato: CalculateMetadataFunction<PropsReelFormato> = ({ props }) => ({
  durationInFrames: Math.max(1, props.duracao),
  fps: props.fps,
});

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const suave = Easing.bezier(0.45, 0, 0.55, 1);
const saida = Easing.bezier(0.16, 1, 0.3, 1);

// ---------------------------------------------------------------- grade de cor
// Bruxelas: contida (menos saturação). Bruges: quente e viva. É a "evolução visual" pedida no prompt.
const filtroBase = (cidade: "bxl" | "bru", quente?: boolean): { sat: number; contraste: number; brilho: number } => {
  if (cidade === "bru") return { sat: 1.12, contraste: 1.06, brilho: 1.01 };
  if (quente) return { sat: 0.98, contraste: 1.05, brilho: 1.0 };
  return { sat: 0.84, contraste: 1.04, brilho: 0.98 };
};

const useFiltro = (cena: Cena, cidade: "bxl" | "bru", extraSat = 1): string => {
  const f = useCurrentFrame();
  const b = filtroBase(cidade, cena.grade_quente);
  let sat = b.sat * extraSat;
  if (cena.desat) sat *= interpolate(f, [cena.desat.ini, cena.desat.fim], [1, cena.desat.sat], { ...clamp, easing: suave });
  let extra = "";
  let brilho = b.brilho * (cena.brilho ?? 1);
  if (cena.desfoque) {
    const k = interpolate(f, [cena.desfoque.ini, cena.desfoque.ini + 6, cena.desfoque.fim, cena.desfoque.fim + 7], [0, 1, 1, 0], clamp);
    extra = ` blur(${(14 * k).toFixed(1)}px)`;
    brilho *= 1 - 0.42 * k;
  }
  return `saturate(${sat.toFixed(3)}) contrast(${b.contraste}) brightness(${brilho.toFixed(3)})${extra}`;
};

const useZoom = (cena: Cena): number => {
  const f = useCurrentFrame();
  if (cena.zoom_kf) return interpolate(f, cena.zoom_kf.t, cena.zoom_kf.z, { ...clamp, easing: suave });
  if (cena.zoom) return interpolate(f, [cena.ini, cena.fim], cena.zoom, clamp);
  return 1;
};

/** Um plano numa camada absoluta. O vídeo começa no quadro em que o plano entra (Sequence). */
const Camada: React.FC<{
  plano: Plano;
  cena: Cena;
  estilo: React.CSSProperties;
  zoom?: number;
  extraSat?: number;
  posicaoObjeto?: string;
}> = ({ plano, cena, estilo, zoom = 1, extraSat = 1, posicaoObjeto = "50% 50%" }) => {
  const filtro = useFiltro(cena, plano.cidade, extraSat);
  return (
    <div style={{ position: "absolute", overflow: "hidden", ...estilo }}>
      <Sequence from={plano.entra} durationInFrames={Math.max(1, plano.fim - plano.entra + 8)} layout="none">
        <OffthreadVideo
          src={staticFile(plano.arquivo)}
          muted
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: posicaoObjeto,
            transform: `scale(${zoom})`,
            transformOrigin: cena.origem ?? "50% 50%",
            filter: filtro,
          }}
        />
      </Sequence>
      {plano.cidade === "bru" ? (
        <AbsoluteFill style={{ background: "rgba(255,170,90,0.07)", mixBlendMode: "soft-light" }} />
      ) : null}
    </div>
  );
};

const Costura: React.FC<{ y?: number; x?: number }> = ({ y, x }) =>
  y !== undefined ? (
    <div style={{ position: "absolute", left: 0, right: 0, top: y - 3, height: 6, background: F.costura }} />
  ) : (
    <div style={{ position: "absolute", top: 0, bottom: 0, left: (x ?? 0) - 3, width: 6, background: F.costura }} />
  );

// ---------------------------------------------------------------- tipos de cena
const CenaVideo: React.FC<{ cena: Cena }> = ({ cena }) => {
  const f = useCurrentFrame();
  const zoom = useZoom(cena);
  const op = cena.entrada === "dissolve" ? interpolate(f, [cena.ini, cena.ini + 7], [0, 1], clamp) : 1;
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Camada plano={cena.planos[0]} cena={cena} estilo={{ left: 0, top: 0, width: 1080, height: 1920 }} zoom={zoom} />
    </AbsoluteFill>
  );
};

/** Tela dividida: o 1º plano (1080×1920) ocupa tudo e é empurrado para a metade de cima quando o 2º entra por baixo. */
const CenaSplit: React.FC<{ cena: Cena }> = ({ cena }) => {
  const f = useCurrentFrame();
  const [a, b] = cena.planos;
  const p = interpolate(f, [b.entra, b.entra + 8], [0, 1], { ...clamp, easing: saida });
  const altA = 1920 - 960 * p;
  const zoom = interpolate(f, [cena.ini, cena.fim], [1.0, 1.04], clamp);
  return (
    <AbsoluteFill style={{ background: F.fundo }}>
      <Camada plano={a} cena={cena} estilo={{ left: 0, top: 0, width: 1080, height: altA }} zoom={zoom} />
      {f >= b.entra ? (
        <>
          <Camada plano={b} cena={cena} estilo={{ left: 0, top: 960 + 960 * (1 - p), width: 1080, height: 960 }} zoom={1.02} />
          <Costura y={960 + 960 * (1 - p)} />
        </>
      ) : null}
    </AbsoluteFill>
  );
};

/** Comparar: 1º plano em tela cheia; na divisão, Bruxelas (sem cor) em cima e Bruges (viva) entra por baixo. */
const CenaComparar: React.FC<{ cena: Cena }> = ({ cena }) => {
  const f = useCurrentFrame();
  const [a, cima, baixo] = cena.planos;
  const divide = baixo.entra;
  const p = interpolate(f, [divide, divide + 9], [0, 1], { ...clamp, easing: saida });
  const zoomA = interpolate(f, [cena.ini, divide], [1.0, 1.05], clamp);
  const rot = (texto: string, y: number, em: number) => {
    const o = interpolate(f, [em + 4, em + 8], [0, 1], clamp);
    return (
      <div
        style={{
          position: "absolute",
          left: F.margem,
          top: y,
          fontFamily: "Anton",
          fontSize: 76,
          color: "#fff",
          letterSpacing: 1,
          opacity: o,
          transform: `translateY(${(1 - o) * 18}px)`,
          textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.8)",
        }}
      >
        {texto}
      </div>
    );
  };
  return (
    <AbsoluteFill style={{ background: F.fundo }}>
      {f < divide ? <Camada plano={a} cena={cena} estilo={{ left: 0, top: 0, width: 1080, height: 1920 }} zoom={zoomA} /> : null}
      {f >= divide ? (
        <>
          <Camada plano={cima} cena={{ ...cena, desat: undefined }} estilo={{ left: 0, top: 0, width: 1080, height: 960 }} zoom={1.03} extraSat={0.3} />
          <Camada plano={baixo} cena={{ ...cena, desat: undefined }} estilo={{ left: 0, top: 960 + 960 * (1 - p), width: 1080, height: 960 }} zoom={1.03} />
          <Costura y={960 + 960 * (1 - p)} />
          {cima.rotulo ? rot(cima.rotulo, 290, divide) : null}
          {baixo.rotulo ? rot(baixo.rotulo, 990 + 960 * (1 - p), divide + 2) : null}
        </>
      ) : null}
    </AbsoluteFill>
  );
};

/** Grade 2×2: cada quadro entra na palavra que mostra. */
const CenaGrade: React.FC<{ cena: Cena }> = ({ cena }) => {
  const f = useCurrentFrame();
  const pos = [
    { left: 0, top: 0 },
    { left: 540, top: 0 },
    { left: 0, top: 960 },
    { left: 540, top: 960 },
  ];
  return (
    <AbsoluteFill style={{ background: F.fundo }}>
      {cena.planos.map((pl, i) => {
        if (f < pl.entra) return null;
        const p = interpolate(f, [pl.entra, pl.entra + 5], [0, 1], { ...clamp, easing: saida });
        return (
          <div key={i} style={{ position: "absolute", ...pos[i], width: 540, height: 960, overflow: "hidden", opacity: p }}>
            <Camada
              plano={pl}
              cena={cena}
              estilo={{ left: 0, top: 0, width: 540, height: 960 }}
              zoom={interpolate(f, [pl.entra, pl.entra + 6, cena.fim], [1.1, 1.02, 1.0], clamp)}
            />
          </div>
        );
      })}
      <Costura x={540} />
      <Costura y={960} />
    </AbsoluteFill>
  );
};

/** Mapa (animação do formato): contorno real da Bélgica (Natural Earth), Bruxelas e, no 2º uso, a linha do trem até Bruges. */
const CenaMapa: React.FC<{ cena: Cena }> = ({ cena }) => {
  const f = useCurrentFrame();
  const m = cena.mapa!;
  const trem = cena.modo === "trem";
  const desenho = trem ? 1 : interpolate(f, [cena.ini, cena.ini + 12], [0, 1], { ...clamp, easing: suave });
  const rotBelgica = trem ? 1 : interpolate(f, [m.marcos.belgica ?? 0, (m.marcos.belgica ?? 0) + 4], [0, 1], clamp);
  const ponto = trem ? 1 : interpolate(f, [m.marcos.ponto ?? 0, (m.marcos.ponto ?? 0) + 5], [0, 1], { ...clamp, easing: saida });
  const linha = trem ? interpolate(f, [m.marcos.linha ?? 0, (m.marcos.bruges ?? 0) + 2], [0, 1], { ...clamp, easing: suave }) : 0;
  const rotBruges = trem ? interpolate(f, [m.marcos.bruges ?? 0, (m.marcos.bruges ?? 0) + 4], [0, 1], clamp) : 0;
  const [bx, by] = m.bruxelas;
  const [gx, gy] = m.bruges;
  const tx = bx + (gx - bx) * linha;
  const ty = by + (gy - by) * linha;
  const pulso = 1 + 0.25 * Math.max(0, Math.sin(((f - (m.marcos.ponto ?? 0)) / 24) * Math.PI * 2)) * (trem ? 0 : 1);
  const zoom = interpolate(f, [cena.ini, cena.fim], trem ? [1.0, 1.06] : [1.0, 1.04], clamp);
  const origem = trem ? `${(bx + gx) / 2}px ${(by + gy) / 2}px` : `${bx}px ${by}px`;
  const comp = 4000;
  const rotulo = (texto: string, x: number, y: number, op: number, cor = "#fff", ancora: "start" | "end" = "start") => (
    <text
      x={x}
      y={y}
      textAnchor={ancora}
      fontFamily="Anton"
      fontSize={64}
      fill={cor}
      opacity={op}
      style={{ letterSpacing: 1 }}
    >
      {texto}
    </text>
  );
  return (
    <AbsoluteFill style={{ background: F.fundo }}>
      <svg width={1080} height={1920} style={{ transform: `scale(${zoom})`, transformOrigin: origem }}>
        <path d={m.caminho} fill="rgba(236,229,216,0.06)" stroke={F.traco} strokeWidth={4} strokeLinejoin="round" strokeDasharray={comp} strokeDashoffset={comp * (1 - desenho)} />
        {rotulo("BÉLGICA", m.caixa.x + m.caixa.w / 2 + 40, m.caixa.y + m.altura - 60, rotBelgica, "rgba(236,229,216,0.85)")}
        {trem ? (
          <line x1={bx} y1={by} x2={tx} y2={ty} stroke={F.ambar} strokeWidth={8} strokeDasharray="22 14" strokeLinecap="round" />
        ) : null}
        <circle cx={bx} cy={by} r={18 * ponto * pulso} fill={F.ambar} />
        <circle cx={bx} cy={by} r={34 * ponto} fill="none" stroke={F.ambar} strokeWidth={3} opacity={0.6 * ponto} />
        {rotulo("BRUXELAS", bx + 46, by + 22, ponto)}
        {trem && linha > 0 ? <circle cx={tx} cy={ty} r={14} fill="#fff" /> : null}
        {trem ? (
          <>
            <circle cx={gx} cy={gy} r={20 * rotBruges} fill={F.ambar} />
            <circle cx={gx} cy={gy} r={38 * rotBruges} fill="none" stroke={F.ambar} strokeWidth={3} opacity={0.6 * rotBruges} />
            {rotulo("BRUGES", gx - 40, gy - 50, rotBruges, F.ambar, "start")}
          </>
        ) : null}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- camadas por cima
/** Gancho (FORMATOS_REELS 4.1): 1ª frase em letras grandes, Anton caixa-alta, à esquerda em x 72, linha a linha na fala. */
const Gancho: React.FC<{ g: PropsReelFormato["gancho"] }> = ({ g }) => {
  const f = useCurrentFrame();
  if (f >= g.ate) return null;
  let y = 330;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.55) 0px, rgba(0,0,0,0.35) 560px, rgba(0,0,0,0) 980px)" }} />
      {g.linhas.map((l, i) => {
        const p = interpolate(f, [l.em, l.em + 4], [0, 1], { ...clamp, easing: saida });
        const top = y;
        y += l.tam * 1.02;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: F.margem,
              top,
              fontFamily: "Anton",
              fontSize: l.tam,
              lineHeight: 1,
              color: l.destaque ? F.ambar : "#fff",
              opacity: p,
              transform: `translateY(${(1 - p) * 24}px)`,
              textShadow: "0 4px 0 rgba(0,0,0,0.3), 0 6px 30px rgba(0,0,0,0.6)",
              whiteSpace: "nowrap",
            }}
          >
            {l.texto}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/** Legenda do formato (FORMATOS_REELS 6): Inter 800 66 px, branca, 1 palavra em âmbar, centro x 540. */
const Legendas: React.FC<{ legendas: Legenda[]; y: (f: number) => number }> = ({ legendas, y }) => {
  const f = useCurrentFrame();
  const l = legendas.find((x) => f >= x.ini && f < x.fim);
  if (!l) return null;
  const p = interpolate(f, [l.ini, l.ini + 3], [0, 1], clamp);
  const partes: React.ReactNode[] = [];
  if (l.destaque) {
    const i = l.texto.toLowerCase().indexOf(l.destaque.toLowerCase());
    if (i >= 0) {
      partes.push(l.texto.slice(0, i));
      partes.push(
        <span key="d" style={{ color: F.ambar }}>
          {l.texto.slice(i, i + l.destaque.length)}
        </span>,
      );
      partes.push(l.texto.slice(i + l.destaque.length));
    } else partes.push(l.texto);
  } else partes.push(l.texto);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: y(f) - 40,
        textAlign: "center",
        fontFamily: "Inter",
        fontWeight: 800,
        fontSize: 66,
        lineHeight: 1.1,
        color: "#fff",
        textShadow: F.sombraLegenda,
        opacity: p,
        transform: `scale(${0.94 + 0.06 * p})`,
        transformOrigin: `${F.centro}px 40px`,
        whiteSpace: "nowrap",
      }}
    >
      {partes}
    </div>
  );
};

/** Recorte da notícia: cai como papel, marca-texto em "most disappointing sight" e sai para baixo revelando a cena. */
const Noticia: React.FC<{ n: PropsReelFormato["noticia"] }> = ({ n }) => {
  const f = useCurrentFrame();
  if (f < n.entra || f > n.sai + 10) return null;
  const larg = n.largura ?? 940;
  const esc = larg / (n.larguraImg ?? 1317);
  const alt = (n.alturaImg ?? 1080) * esc;
  const x = (1080 - larg) / 2;
  const y0 = 400;
  const e = interpolate(f, [n.entra, n.entra + 9], [0, 1], { ...clamp, easing: Easing.bezier(0.34, 1.4, 0.64, 1) });
  const s = interpolate(f, [n.sai, n.sai + 7], [0, 1], { ...clamp, easing: Easing.bezier(0.5, 0, 0.75, 0) });
  const y = y0 - 1300 * (1 - e) + 1500 * s;
  const rot = -6 + 4.5 * e + 4 * s;
  const marca = interpolate(f, [n.destaque, n.destaque + 8], [0, 1], { ...clamp, easing: suave });
  const mk = n.marca ?? { x: 64, y: 330, w: 1130, h: 102 };
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: x,
          top: y,
          width: larg,
          height: alt,
          opacity: 1 - s,
          transform: `rotate(${rot}deg)`,
          boxShadow: "0 18px 40px rgba(0,0,0,0.45), 0 2px 6px rgba(0,0,0,0.3)",
          background: "#fff",
        }}
      >
        <Img src={staticFile(n.arquivo)} style={{ width: larg, height: alt, display: "block" }} />
        <div
          style={{
            position: "absolute",
            left: mk.x * esc,
            top: mk.y * esc,
            width: mk.w * esc * marca,
            height: mk.h * esc,
            background: "rgba(224,174,92,0.55)",
            mixBlendMode: "multiply",
            borderRadius: 6,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

/** Luz de passagem (REFERENCIA_EDICAO_FORMATOS 3.2): luz quente desce do topo em 3 q, cobre 4 q (pico 85%), o corte fica
 * escondido no quadro mais claro, e recua para um canto em 4 q. */
const LuzDePassagem: React.FC<{ corte: number }> = ({ corte }) => {
  const f = useCurrentFrame();
  const d = f - corte;
  if (d < -6 || d > 6) return null;
  const op = interpolate(d, [-6, -3, -1, 0, 1, 2, 6], [0, 0.45, 0.8, 0.85, 0.8, 0.6, 0], clamp);
  const alcance = interpolate(d, [-6, -3, 0, 6], [10, 70, 130, 40], clamp);
  const cx = interpolate(d, [0, 6], [50, 85], clamp);
  return (
    <AbsoluteFill
      style={{
        opacity: op,
        background: `radial-gradient(ellipse 120% ${alcance}% at ${cx}% 0%, rgba(255,236,200,1) 0%, rgba(255,196,120,0.9) 35%, rgba(255,160,80,0) 100%)`,
        mixBlendMode: "screen",
      }}
    />
  );
};

const FaixasCinema: React.FC<{ de: number; ate: number }> = ({ de, ate }) => {
  const f = useCurrentFrame();
  if (f < de || f >= ate) return null;
  const h = interpolate(f, [de, de + 10], [0, 250], { ...clamp, easing: suave });
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: h, background: "#000" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: h, background: "#000" }} />
    </>
  );
};

/** Grão 6% em overlay (FORMATOS_REELS 2). */
const Grao: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ opacity: 0.06, mixBlendMode: "overlay" }}>
      <svg width={1080} height={1920}>
        <filter id="grao">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={f % 12} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={1080} height={1920} filter="url(#grao)" />
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- composição
export const ReelFormato: React.FC<PropsReelFormato> = (p) => {
  const f = useCurrentFrame();
  const cenaEm = (q: number) => p.cenas.find((c) => q >= c.ini && q < c.fim);
  const atual = cenaEm(f);
  const cinema = p.cenas.find((c) => c.cinema !== undefined);
  // legenda: y 1320 na tela cheia (FORMATOS_REELS 6); com as faixas de cinema, sobe para dentro da imagem
  const yLeg = () => 1320;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {p.cenas.map((c) => {
        // se a cena seguinte entra em dissolve, esta fica por baixo mais 8 quadros
        const C =
          c.tipo === "split" ? CenaSplit : c.tipo === "grade" ? CenaGrade : c.tipo === "mapa" ? CenaMapa : c.tipo === "comparar" ? CenaComparar : CenaVideo;
        const proxima = p.cenas[p.cenas.indexOf(c) + 1];
        const visivel = f >= c.ini && (f < c.fim || (proxima?.entrada === "dissolve" && f < c.fim + 8));
        if (!visivel) return null;
        return (
          <AbsoluteFill key={c.id} style={{ zIndex: f < c.fim ? 2 : 1 }}>
            <C cena={c} />
          </AbsoluteFill>
        );
      })}
      <AbsoluteFill style={{ zIndex: 5, pointerEvents: "none" }}>
        {/* degradê na base para a legenda branca não sumir em céu e pedra (FORMATOS_REELS 3) */}
        {atual && atual.tipo !== "mapa" && !atual.cta ? (
          <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 900px, rgba(0,0,0,0.42) 1220px, rgba(0,0,0,0.58) 1440px, rgba(0,0,0,0.62) 1920px)" }} />
        ) : null}
        <Noticia n={p.noticia} />
        {cinema ? <FaixasCinema de={cinema.cinema!} ate={cinema.fim} /> : null}
        <Gancho g={p.gancho} />
        <Legendas legendas={p.legendas} y={yLeg} />
        <LuzDePassagem corte={p.luz.corte} />
        <Grao />
      </AbsoluteFill>
      {/* CTA: único elemento do DS V2 no Reel (decisão do Diego, 28/10/2026) */}
      <Sequence from={p.cta.entra} layout="none">
        <AbsoluteFill style={{ zIndex: 10 }}>
          <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo="seta" tamanho="M" entrada={0} />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
