/**
 * Tokens do DS V2 lidos direto de `design-system/primeiro-dia-tokens-v2.json`.
 * Nenhum valor visual nasce aqui: cor, fonte, sombra, curva, duração, raio, rotação,
 * opacidade, posição e volume vêm do JSON (fonte 2 do CLAUDE.md). Valores que o DS
 * define só no brand book (ex.: anatomia da placa) ficam nos componentes, com a seção citada.
 */
import { Easing } from "remotion";
import raw from "../../../primeiro-dia-tokens-v2.json";

type Json = Record<string, unknown>;

const pegar = (caminho: string): unknown => {
  let no: unknown = raw;
  for (const parte of caminho.split(".")) {
    no = (no as Json)[parte];
    if (no === undefined) throw new Error(`Token inexistente: ${caminho}`);
  }
  return no;
};

const valor = (caminho: string): unknown => {
  const v = (pegar(caminho) as Json)["$value"];
  if (typeof v === "string" && v.startsWith("{") && v.endsWith("}")) {
    return valor(v.slice(1, -1));
  }
  return v;
};

const cor = (caminho: string): string => {
  const v = valor(`color.${caminho}`) as { hex: string; alpha?: number };
  if (v.alpha === undefined) return v.hex;
  const n = parseInt(v.hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${v.alpha})`;
};

const px = (caminho: string): number => (valor(caminho) as { value: number }).value;
const num = (caminho: string): number => valor(caminho) as number;
const bezier = (nome: string) => {
  const [a, b, c, d] = valor(`easing.${nome}`) as number[];
  return Easing.bezier(a, b, c, d);
};
const familia = (nome: string): string =>
  (valor(`font.family.${nome}`) as string[]).map((f) => (f.includes(" ") ? `"${f}"` : f)).join(", ");

/** Mistura cor hex com alpha (para sombras e filetes descritos no DS em %). */
export const rgba = (hex: string, alpha: number): string => {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${alpha})`;
};

export const COR = {
  amarelo: cor("signal.500"),
  amarelo100: cor("signal.100"),
  amarelo300: cor("signal.300"),
  amarelo700: cor("signal.700"),
  grafite: cor("night.900"),
  grafite800: cor("night.800"),
  grafite700: cor("night.700"),
  asfalto: cor("night.500"),
  poeira: cor("night.400"),
  concreto: cor("night.300"),
  papel: cor("paper.500"),
  recibo: cor("paper.0"),
  vermelho: cor("stamp.500"),
  vermelho700: cor("stamp.700"),
  caneta: cor("ink.500"),
  verde: cor("exit.600"),
  legenda: cor("semantic.caption-text"),
  scrim: cor("semantic.scrim"),
  vidro: cor("semantic.glass"),
} as const;

export const FONTE = {
  display: familia("display"),
  texto: familia("text"),
  dados: familia("data"),
  mono: familia("mono"),
  caneta: familia("pen"),
} as const;

type Estilo = { fontSize: number; fontWeight: number; lineHeight: number; letterSpacing: string };
const estilo = (nome: string): Estilo => {
  const v = valor(`font.style.${nome}`) as Json;
  const tam = ((v.fontSize as Json)["$value"] as { value: number }).value;
  const ls = ((v.letterSpacing as Json)["$value"] as { value: number }).value;
  return { fontSize: tam, fontWeight: v.fontWeight as number, lineHeight: v.lineHeight as number, letterSpacing: `${ls}em` };
};

export const TIPO = {
  display: estilo("display"),
  h1: estilo("h1"),
  h2: estilo("h2"),
  h3: estilo("h3"),
  label: estilo("label"),
  editorial: estilo("editorial"),
  caption: estilo("caption"),
  body: estilo("body"),
  narrative: estilo("narrative"),
  dataXl: estilo("data-xl"),
  data: estilo("data"),
  micro: estilo("micro"),
  pen: estilo("pen"),
} as const;

export const ESPACO = (n: number): number => px(`space.${n}`);

export const RAIO = {
  papel: px("radius.paper"),
  tag: px("radius.tag"),
  placa: px("radius.plate"),
  foto: px("radius.photo"),
} as const;

export const SOMBRA = {
  placa: valor("shadow.shadow-plate") as string,
  relevo: valor("shadow.shadow-plate-bevel") as string,
  papel: valor("shadow.shadow-paper") as string,
  ergue: valor("shadow.shadow-lift") as string,
} as const;

/** Durações em ms (DS V2, 4.1). */
export const DUR = {
  tick: px("duration.dur-tick"),
  fast: px("duration.dur-fast"),
  base: px("duration.dur-base"),
  slow: px("duration.dur-slow"),
  arrive: px("duration.dur-arrive"),
  cinema: px("duration.dur-cinema"),
} as const;

/** Curvas (DS V2, 4.1). */
export const EASE = {
  arrive: bezier("ease-arrive"),
  out: bezier("ease-out"),
  exit: bezier("ease-exit"),
  drop: bezier("ease-drop"),
  cinema: bezier("ease-cinema"),
} as const;

export const ROT = {
  bilhete: num("rotation.rot-note"),
  carimbo: num("rotation.rot-stamp"),
  ticket: num("rotation.rot-ticket"),
  etiqueta: num("rotation.rot-tag"),
} as const;

export const OPAC = {
  grao: num("opacity.op-grain"),
  fibra: num("opacity.op-fiber"),
  scrim: num("opacity.op-scrim"),
  vidro: num("opacity.op-glass"),
} as const;

export const BLUR = {
  vidro: px("blur.blur-glass"),
  movimento: px("blur.blur-motion"),
} as const;

export const EFEITO = {
  maxSimultaneos: num("effect.max-simultaneous"),
  zoomSutil: num("effect.zoom-subtle"),
  tremor1: px("effect.shake-1"),
  tremor2: px("effect.shake-2"),
  flash: num("effect.flash-opacity"),
  lightLeak: num("effect.light-leak-opacity"),
  vinheta: num("effect.vignette-opacity"),
  glow: num("effect.glow-opacity"),
  glowRaio: px("effect.glow-radius"),
} as const;

/** Volumes relativos à voz em dB (DS V2, 4.6). */
export const SOM = {
  clack: num("sound.clack"),
  tum: num("sound.tum"),
  ding: num("sound.ding"),
  clique: num("sound.clique"),
  tick: num("sound.tick"),
  impressora: num("sound.impressora"),
  obturador: num("sound.obturador"),
  whoosh: num("sound.whoosh"),
  intervaloMin: px("sound.min-interval"),
  masterLufs: num("sound.master-loudness"),
  masterPico: num("sound.master-true-peak"),
} as const;

export const REEL = {
  largura: px("layout.reel.width"),
  altura: px("layout.reel.height"),
  seguroTopo: px("layout.reel.safe-top"),
  seguroBase: px("layout.reel.safe-bottom"),
  seguroEsq: px("layout.reel.safe-left"),
  seguroDir: px("layout.reel.safe-right"),
  placarY: px("layout.reel.zone-scoreboard-y"),
  placaY: px("layout.reel.zone-plate-y"),
  objetoY: px("layout.reel.zone-object-y"),
  legendaTopoY: px("layout.reel.zone-caption-y"),
  legendaLimiteY: px("layout.reel.caption-limit-y"),
} as const;
