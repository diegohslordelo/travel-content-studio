/**
 * Reel em tela dividida · "3 formas de economizar com comida na viagem" · REV2 (reels/comida-3-regras/rev2).
 * Parte da REV1 (ComidaReel, que não muda). REV2 (Diego, 17/11/2026): gancho metade no prato do bouillon, metade na
 * paella, com a legenda normal; ele em tela cheia só depois da pergunta; mais acervo real. O componente Gancho (páginas
 * em letras garrafais) ficou disponível, mas a REV2 não o usa (props.gancho.paginas vazio: o Diego recusou essa versão).
 * Notas da REV1:
 * Parte do modelo de Veneza REV4 (VenezaReel4, que não muda). Pedidos do Diego (16/11/2026):
 * - sequência da gravação, decupada sem espaço entre as falas e sem cortar palavra;
 * - legenda karaokê (a palavra dita fica amarela), caixa normal, nada antes de ser dito;
 * - nada na frente do rosto: na tela dividida o rosto fica a 42% da metade de baixo; em tela cheia a legenda
 *   vai na posição calculada pelo rosto de cada grupo (props.gy); a placa da CTA vai abaixo do queixo;
 * - gancho: só o prato do bouillon em cima e ele embaixo, sem animação na frente da comida;
 * - "Bora que eu vou te mostrar": ele em tela cheia, depois volta a tela dividida;
 * - "E nas outras refeições, rapaz, vai ficar sem comer?" em preto e branco (a resposta volta à cor);
 * - nenhuma cor no vídeo dele nem no acervo (só a conversão HLG→SDR do preparo); acervo sem zoom e sem
 *   mudar a velocidade;
 * - imagens, animações e textos com pelo menos 2,5 s na tela;
 * - o que aparece em cima sempre ilustra o que ele está falando (o "menorzinho de toda manhã" é o café preto:
 *   foto dele com o café na rua, em Florença); imagens reais do acervo sempre que existirem (supermercado em Amsterdam).
 * Linguagem do formato (FORMATOS_REELS): Anton/Inter, paleta "Mesa" (só deste Reel, não é paleta da marca);
 * DS V2 só no CTA (placa + clack).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Easing,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Placa } from "../ds/Placa";
import { Som } from "../ds/Som";
import pdxImpacto from "../../../sons/externos/PDX_impacto.wav";
import pdxSwish from "../../../sons/externos/PDX_swish.wav";
import pdxObturador from "../../../sons/externos/PDX_obturador.wav";
import pdxRiser from "../../../sons/externos/PDX_riser.wav";

/* Paleta "Mesa" (só deste Reel; não é paleta da marca) */
const AMBAR = "#FFD23F"; // destaque da legenda (igual a Veneza REV4)
const AMBAR_CTA = "#E0AE5C";
const CREME = "#FFF4E0";
const TOMATE = "#E8463A";
const MOSTARDA = "#FFC233";
const VERDE = "#2E8B57";
const CAFE = "#5A3A22";
const NOITE = "#1E2A55";
const TINTA = "#2B1B12";
const BRANCO = "#FFFFFF";
const BG = {
  formas: "linear-gradient(160deg, #FF6B5B 0%, #E8463A 100%)",
  cafe: "linear-gradient(160deg, #FFD36B 0%, #FFA53D 100%)",
  mercado: "linear-gradient(160deg, #4CC08A 0%, #2E8B57 100%)",
  inverte: "linear-gradient(160deg, #FFF4E0 0%, #FFE2B8 100%)",
  cinquenta: "linear-gradient(160deg, #3FB27F 0%, #1F7A4F 100%)",
  balanca: "linear-gradient(160deg, #34488F 0%, #1E2A55 100%)",
};
const SOMBRA = "0 3px 0 rgba(0,0,0,0.16), 0 6px 20px rgba(0,0,0,0.22)";
const COSTURA = 900;
const H = COSTURA;

let fontesOk = false;
const fontes = () => {
  if (fontesOk) return;
  fontesOk = true;
  loadFont({ family: "Anton", url: staticFile("fontes/anton-latin-400-normal.woff2"), weight: "400" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-800-normal.woff2"), weight: "800" });
  loadFont({ family: "Inter", url: staticFile("fontes/inter-latin-600-normal.woff2"), weight: "600" });
};

type Palavra = { w: string; s: number; e: number };
type Rot = { txt: string; t: number }[];
export type CenaComida = {
  ini: number;
  fim: number;
  tipo: "video" | "foto" | "diego" | "graf" | "grafcheio";
  src?: string;
  graf?: string;
  dados?: Record<string, number | string | Rot>;
  rotulo?: Rot;
  foco?: number;
};
type Corte = { ini: number; fim: number; take: string; pb: boolean; div_off: number };
type Sfx = { t: number; som: "impacto" | "swish" | "obturador" | "riser"; db: number };
type Pagina = { ini: number; fim: number; linhas: { tam: number; cor?: string; palavras: Rot }[] };
export type PropsComida2 = {
  dur: number;
  palavras: Palavra[];
  cenas: CenaComida[];
  grupos: number[][];
  gy: number[];
  sfx: Sfx[];
  cortes: Corte[];
  cta: { ini: number; placa_y: number; leg_fim: number };
  gancho: { fim: number; paginas: Pagina[] };
};

export const propsComida2Vazias: PropsComida2 = {
  dur: 1, palavras: [], cenas: [], grupos: [], gy: [], sfx: [], cortes: [], cta: { ini: 0, placa_y: 1218, leg_fim: 0 }, gancho: { fim: 0, paginas: [] },
};

export const metadadosComida2: CalculateMetadataFunction<PropsComida2> = ({ props }) => ({
  durationInFrames: Math.ceil(props.dur * 30 - 1e-6),
});

const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const lin = (t: number, a: number, b: number, v0: number, v1: number, e: (x: number) => number = ease) =>
  interpolate(t, [a, b], [v0, v1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
/** Entra no instante t0 (nunca antes): 0 → 1 em d segundos. */
const entra = (t: number, t0: number, d = 0.2) => (t < t0 ? 0 : lin(t, t0, t0 + d, 0, 1));
/** Pula com "back" no instante t0 (nunca antes). */
const pula = (t: number, t0: number, d = 0.24, k = 1.8) => (t < t0 ? 0 : lin(t, t0, t0 + d, 0, 1, Easing.out(Easing.back(k))));
/** Para o que abre uma cena (desenho sem texto falado): já visível no 1º quadro, só assenta. */
const abre = (t: number, t0: number) => 0.6 + 0.4 * lin(t, t0, t0 + 0.18, 0, 1);

/** Palavras que entram uma a uma, cada uma no início da sua fala; as futuras ficam invisíveis no lugar. */
const Palavras: React.FC<{ itens: Rot; t: number; estilo: React.CSSProperties; sobe?: number }> = ({ itens, t, estilo, sobe = 18 }) => (
  <div style={estilo}>
    {itens.map((p, i) => {
      const o = entra(t, p.t, 0.12);
      return (
        <span key={i} style={{ display: "inline-block", opacity: o, transform: `translateY(${(1 - o) * sobe}px)`, whiteSpace: "pre" }}>
          {(i ? " " : "") + p.txt}
        </span>
      );
    })}
  </div>
);

/* ---------- camadas de vídeo ---------- */

/** Vídeo do acervo cobrindo a área, sem zoom e sem mudar a velocidade (pedido do Diego). */
const VideoCobre: React.FC<{ src: string; W: number; H: number; focoY?: number; ar?: number }> = ({ src, W, H: Hh, focoY = 0.5, ar = 1080 / 1920 }) => {
  const k = Math.max(W / 1080, Hh / (1080 / ar));
  const w = 1080 * k;
  const h = (1080 / ar) * k;
  return (
    <div style={{ position: "absolute", left: (W - w) / 2, top: (Hh - h) * focoY, width: w, height: h }}>
      <Video src={staticFile(src)} muted style={{ width: w, height: h }} />
    </div>
  );
};

/** Gravação do Diego. Sem filtro nenhum; P&B puro só no take pedido. Na tela dividida, rosto a 42% da metade de baixo. */
const Diego: React.FC<{ cheio: boolean; pb: boolean; divOff: number }> = ({ cheio, pb, divOff }) => (
  <AbsoluteFill style={{ top: cheio ? 0 : COSTURA, overflow: "hidden", filter: pb ? "grayscale(1)" : undefined }}>
    <div style={{ position: "absolute", left: 0, top: cheio ? 0 : divOff, width: 1080, height: 1920 }}>
      <Video src={staticFile("diego.mp4")} muted style={{ width: 1080, height: 1920 }} />
    </div>
  </AbsoluteFill>
);

/* ---------- desenhos (traço, não foto) ---------- */

const Xicara: React.FC<{ s?: number; t: number }> = ({ s = 1, t }) => (
  <svg width={300 * s} height={300 * s} viewBox="0 0 300 300">
    {[0, 1, 2].map((i) => {
      const y = 20 + ((t * 40 + i * 30) % 90);
      return <path key={i} d={`M ${110 + i * 40} ${120 - y * 0.2} q 14 -18 0 -36 q -14 -18 0 -36`} stroke={BRANCO} strokeWidth={10} fill="none" strokeLinecap="round" opacity={0.85 - (y - 20) / 140} />;
    })}
    <ellipse cx={150} cy={262} rx={120} ry={22} fill={BRANCO} />
    <path d="M 60 140 L 240 140 L 222 236 Q 216 252 198 252 L 102 252 Q 84 252 78 236 Z" fill={BRANCO} />
    <path d="M 238 162 q 50 0 44 38 q -6 34 -52 30" stroke={BRANCO} strokeWidth={16} fill="none" />
    <ellipse cx={150} cy={142} rx={90} ry={14} fill={CAFE} />
  </svg>
);

const Sino: React.FC<{ s?: number; risco: number }> = ({ s = 1, risco }) => (
  <svg width={150 * s} height={130 * s} viewBox="0 0 150 130">
    <rect x={10} y={104} width={130} height={14} rx={7} fill={BRANCO} />
    <path d="M 22 102 Q 22 40 75 38 Q 128 40 128 102 Z" fill={BRANCO} />
    <rect x={66} y={22} width={18} height={16} rx={6} fill={BRANCO} />
    <line x1={14} y1={14} x2={14 + 122 * risco} y2={14 + 108 * risco} stroke={TOMATE} strokeWidth={13} strokeLinecap="round" opacity={risco > 0 ? 1 : 0} />
  </svg>
);

const Carrinho: React.FC<{ s?: number; sacola: number; giro: number }> = ({ s = 1, sacola, giro }) => (
  <svg width={360 * s} height={300 * s} viewBox="0 0 360 300">
    <g opacity={sacola} transform={`translate(0 ${(1 - sacola) * -60})`}>
      <rect x={120} y={40} width={130} height={120} rx={14} fill={CREME} />
      <path d="M 150 44 q 35 -50 70 0" stroke={CREME} strokeWidth={12} fill="none" />
      <rect x={140} y={70} width={30} height={60} rx={8} fill={MOSTARDA} />
      <circle cx={210} cy={90} r={24} fill={TOMATE} />
    </g>
    <path d="M 10 60 L 70 60 L 110 210 L 300 210 L 330 100 L 86 100" stroke={BRANCO} strokeWidth={16} fill="none" strokeLinejoin="round" strokeLinecap="round" />
    {[130, 280].map((cx) => (
      <g key={cx} transform={`rotate(${giro} ${cx} 250)`}>
        <circle cx={cx} cy={250} r={26} fill={BRANCO} />
        <line x1={cx - 18} y1={250} x2={cx + 18} y2={250} stroke={VERDE} strokeWidth={6} />
      </g>
    ))}
  </svg>
);

const Cama: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <svg width={340 * s} height={220 * s} viewBox="0 0 340 220">
    <rect x={20} y={30} width={26} height={170} rx={10} fill={BRANCO} />
    <rect x={46} y={110} width={274} height={60} rx={16} fill={BRANCO} />
    <rect x={60} y={78} width={86} height={42} rx={18} fill={MOSTARDA} />
    <rect x={150} y={92} width={170} height={34} rx={14} fill={CREME} />
    <rect x={46} y={168} width={20} height={36} rx={6} fill={BRANCO} />
    <rect x={300} y={168} width={20} height={36} rx={6} fill={BRANCO} />
  </svg>
);

const Sol: React.FC<{ s?: number; cor?: string }> = ({ s = 1, cor = MOSTARDA }) => (
  <svg width={150 * s} height={150 * s} viewBox="0 0 110 110">
    <circle cx={55} cy={55} r={24} fill={cor} />
    {Array.from({ length: 8 }, (_, i) => (
      <line key={i} x1={55} y1={14} x2={55} y2={24} stroke={cor} strokeWidth={8} strokeLinecap="round" transform={`rotate(${i * 45} 55 55)`} />
    ))}
  </svg>
);

const Lua: React.FC<{ s?: number; cor?: string }> = ({ s = 1, cor = BRANCO }) => (
  <svg width={150 * s} height={150 * s} viewBox="0 0 110 110">
    <path d="M 70 18 A 38 38 0 1 0 92 70 A 30 30 0 1 1 70 18 Z" fill={cor} />
  </svg>
);

const Talheres: React.FC<{ s?: number; cor?: string }> = ({ s = 1, cor = BRANCO }) => (
  <svg width={260 * s} height={200 * s} viewBox="0 0 260 200">
    <circle cx={130} cy={100} r={78} fill="none" stroke={cor} strokeWidth={12} />
    <circle cx={130} cy={100} r={50} fill="none" stroke={cor} strokeWidth={6} opacity={0.6} />
    <rect x={22} y={20} width={10} height={160} rx={5} fill={cor} />
    <rect x={10} y={20} width={8} height={56} rx={4} fill={cor} />
    <rect x={36} y={20} width={8} height={56} rx={4} fill={cor} />
    <path d="M 232 20 Q 252 70 236 110 L 236 180" stroke={cor} strokeWidth={12} fill="none" strokeLinecap="round" />
  </svg>
);

const Pino: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <svg width={110 * s} height={150 * s} viewBox="0 0 110 150">
    <path d="M 55 146 Q 8 84 8 56 A 47 47 0 1 1 102 56 Q 102 84 55 146 Z" fill={TOMATE} />
    <circle cx={55} cy={55} r={18} fill={CREME} />
  </svg>
);

const Nota: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <svg width={460 * s} height={230 * s} viewBox="0 0 460 230">
    <rect x={6} y={6} width={448} height={218} rx={18} fill="#BFE3B4" stroke={BRANCO} strokeWidth={8} />
    <rect x={30} y={30} width={400} height={170} rx={12} fill="none" stroke={VERDE} strokeWidth={4} strokeDasharray="10 8" />
    <circle cx={230} cy={115} r={62} fill={VERDE} />
    <text x={230} y={146} textAnchor="middle" fontFamily="Anton" fontSize={92} fill="#BFE3B4">€</text>
  </svg>
);

const Moedas: React.FC<{ s?: number }> = ({ s = 1 }) => (
  <svg width={200 * s} height={120 * s} viewBox="0 0 200 120">
    {[0, 1, 2].map((i) => (
      <g key={i} transform={`translate(${30 + i * 60} ${i % 2 ? 20 : 34})`}>
        <circle cx={30} cy={40} r={34} fill={MOSTARDA} stroke={TINTA} strokeWidth={5} />
        <text x={30} y={58} textAnchor="middle" fontFamily="Anton" fontSize={46} fill={TINTA}>€</text>
      </g>
    ))}
  </svg>
);

/* ---------- grafismos (área de cima 1080×900) ---------- */

const BASE: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: 1080, height: H, overflow: "hidden" };
const centro = (top: number, extra: React.CSSProperties = {}): React.CSSProperties => ({ position: "absolute", left: 0, right: 0, top, textAlign: "center", ...extra });
const ANTON = (tam: number, cor = BRANCO, sombra = true): React.CSSProperties => ({ fontFamily: "Anton", fontSize: tam, lineHeight: 1, color: cor, textShadow: sombra ? SOMBRA : "none" });
const INTER = (tam: number, cor = BRANCO, sombra = true): React.CSSProperties => ({ fontFamily: "Inter", fontWeight: 800, fontSize: tam, letterSpacing: 3, color: cor, textShadow: sombra ? SOMBRA : "none" });

const Grafismo: React.FC<{ c: CenaComida; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const at = (k: string) => Number(d[k] ?? c.ini);
  const rt = (k: string) => (d[k] ?? []) as Rot;
  const g = c.graf;

  if (g === "formas") {
    // "três formas que eu uso pra não gastar uma nota com comida durante a viagem."
    const p3 = pula(t, at("t3"), 0.26, 1.8);
    const pn = pula(t, at("tnota"), 0.3, 1.6);
    return (
      <div style={{ ...BASE, background: BG.formas }}>
        <div style={{ position: "absolute", left: 110, top: 70, ...ANTON(380, MOSTARDA, false), textShadow: "0 8px 0 rgba(120,20,10,0.35)", opacity: p3, transform: `scale(${0.6 + 0.4 * p3})`, transformOrigin: "50% 60%" }}>3</div>
        <Palavras itens={rt("formas")} t={t} estilo={{ position: "absolute", left: 380, top: 170, ...ANTON(180) }} />
        <div style={{ position: "absolute", left: 540, top: 420, opacity: pn, transform: `translateY(${(1 - pn) * -160}px) rotate(${-8 + 4 * pn}deg)` }}>
          <Nota s={0.95} />
        </div>
        <Palavras itens={rt("gastar")} t={t} estilo={{ position: "absolute", left: 90, top: 470, width: 470, ...ANTON(96), lineHeight: 1.05 }} />
      </div>
    );
  }

  if (g === "cafe") {
    // "A primeira coisa é economizar no café da manhã. Se não tá incluso no hotel,"
    const p1 = pula(t, at("t1"));
    const tinc = at("tincluso");
    return (
      <div style={{ ...BASE, background: BG.cafe }}>
        <div style={{ position: "absolute", left: 90, top: 50, ...ANTON(300, BRANCO, false), textShadow: "0 8px 0 rgba(150,70,0,0.3)", opacity: p1, transform: `scale(${0.6 + 0.4 * p1})` }}>1</div>
        <div style={{ position: "absolute", left: 560, top: 40, opacity: abre(t, c.ini) }}>
          <Xicara s={1.25} t={t} />
        </div>
        <Palavras itens={rt("cafe")} t={t} estilo={{ position: "absolute", left: 90, top: 410, ...ANTON(120, TINTA, false) }} />
        <div style={{ position: "absolute", left: 90, top: 590, display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ opacity: entra(t, at("thotel") - 0.6, 0.2) }}>
            <Sino s={0.9} risco={t < tinc ? 0 : lin(t, tinc, tinc + 0.3, 0, 1)} />
          </div>
          <Palavras itens={rt("incluso")} t={t} estilo={{ ...INTER(54, BRANCO) }} />
        </div>
      </div>
    );
  }

  if (g === "mercado") {
    // "a gente passa no supermercado e compra algumas coisas para comer no quarto mesmo."
    const ts = at("tsuper");
    const tc = at("tcompra");
    const tq = at("tquarto");
    const x = t < tq - 0.25 ? lin(t, c.ini, ts + 0.1, -380, 330, Easing.out(Easing.cubic)) : lin(t, tq - 0.25, tq + 0.2, 330, 1150, Easing.in(Easing.cubic));
    const giro = (x + 380) * 1.2;
    const pc = pula(t, tq, 0.3, 1.6);
    return (
      <div style={{ ...BASE, background: BG.mercado }}>
        <Palavras itens={rt("super")} t={t} estilo={centro(60, ANTON(120))} />
        <div style={{ position: "absolute", left: x, top: 230 }}>
          <Carrinho s={1.15} sacola={entra(t, tc, 0.3)} giro={giro} />
        </div>
        <div style={{ position: "absolute", left: 370, top: 300, opacity: pc, transform: `translateY(${(1 - pc) * 80}px)` }}>
          <Cama s={1.0} />
        </div>
        <Palavras itens={rt("quarto")} t={t} estilo={centro(620, ANTON(110, MOSTARDA, false), )} />
      </div>
    );
  }

  if (g === "jantar") {
    // "Geralmente escolhemos o jantar porque é mais no final do dia, a gente já fez tudo e pode comer com calma."
    const tf = at("tfinal");
    const k = lin(t, c.ini, tf + 0.4, 0, 1, Easing.inOut(Easing.cubic));
    const ceu = `linear-gradient(180deg, ${k < 0.5 ? "#7FD3F7" : "#F7A35C"} 0%, ${k < 0.5 ? "#3FA9E0" : "#E86A4A"} 100%)`;
    const pj = pula(t, at("tjantar"));
    return (
      <div style={{ ...BASE, background: ceu }}>
        <AbsoluteFill style={{ height: H, background: `linear-gradient(180deg, #2B3F7A 0%, ${NOITE} 100%)`, opacity: lin(t, tf - 0.2, tf + 0.6, 0, 1) }} />
        <div style={{ position: "absolute", left: lin(t, c.ini, tf + 0.4, 120, 760, Easing.inOut(Easing.quad)), top: 60 + 380 * k * k }}>
          <Sol s={1.2} />
        </div>
        <div style={{ position: "absolute", left: 120, top: lin(t, tf, tf + 0.8, 520, 60), opacity: entra(t, tf, 0.4) }}>
          <Lua s={1.1} cor={MOSTARDA} />
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 330, textAlign: "center", opacity: pj, transform: `scale(${0.7 + 0.3 * pj})` }}>
          <Talheres s={1} />
          <div style={{ ...ANTON(170, BRANCO), marginTop: 6 }}>JANTAR</div>
        </div>
        <Palavras itens={rt("final")} t={t} estilo={centro(150, INTER(54))} />
        <Palavras itens={rt("calma")} t={t} estilo={{ position: "absolute", right: 70, top: 710, ...ANTON(96, MOSTARDA, false), textShadow: "0 5px 0 rgba(0,0,0,0.3)" }} />
      </div>
    );
  }

  if (g === "inverte") {
    // "Mas quem define? Seu roteiro. Se tem algum restaurante que vale a pena ir na hora do almoço
    //  por conta de uma vista ou experiência do lugar, aí você inverte."
    const tr = at("troteiro");
    const ta = at("talmoco");
    const ti = at("tinverte");
    const sobe = lin(t, c.ini, c.ini + 0.3, 0.6, 1);
    const pa = entra(t, ta, 0.3);
    const badgeX = t < ti ? 750 : lin(t, ti, ti + 0.45, 750, 260, Easing.inOut(Easing.cubic));
    const badgeY = t < ti ? 330 : 330 - Math.sin(Math.min(1, (t - ti) / 0.45) * Math.PI) * 120;
    const card = (x: number, p: number, icone: React.ReactNode, nome: React.ReactNode, destaque: number) => (
      <div style={{ position: "absolute", left: x, top: 290, width: 400, height: 430, borderRadius: 30, background: BRANCO, boxShadow: `0 18px 40px rgba(120,60,0,0.25), 0 0 0 ${10 * destaque}px ${MOSTARDA}`, opacity: p, transform: `translateY(${(1 - p) * 80}px)`, textAlign: "center" }}>
        <div style={{ marginTop: 50 }}>{icone}</div>
        <div style={{ ...ANTON(96, TINTA, false), marginTop: 14 }}>{nome}</div>
      </div>
    );
    return (
      <div style={{ ...BASE, background: BG.inverte }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 70 - 40 * sobe, display: "flex", justifyContent: "center", alignItems: "center", gap: 24, transform: `scale(${1 - 0.3 * sobe})` }}>
          <div style={{ opacity: entra(t, tr, 0.2) }}><Pino s={0.9} /></div>
          <div>
            <Palavras itens={rt("quem")} t={t} estilo={{ ...INTER(54, TINTA, false) }} />
            <Palavras itens={rt("roteiro")} t={t} estilo={{ ...ANTON(130, TOMATE, false) }} />
          </div>
        </div>
        {card(90, pa, <Sol s={1.1} />, <Palavras itens={rt("almoco")} t={t} estilo={{}} />, t >= ti ? lin(t, ti + 0.3, ti + 0.5, 0, 1) : 0)}
        {card(590, abre(t, c.ini), <Lua s={1.1} cor={NOITE} />, "JANTAR", t < ti ? 1 : lin(t, ti, ti + 0.2, 1, 0))}
        {/* "vista ou experiência" numa linha própria; dá lugar ao "⇄ INVERTE" quando ele diz "inverte" */}
        <div style={centro(762, { opacity: t < ti ? 1 : lin(t, ti - 0.05, ti + 0.1, 1, 0) })}>
          <Palavras itens={rt("vista")} t={t} estilo={{ ...ANTON(84, NOITE, false) }} />
        </div>
        <div style={{ position: "absolute", left: badgeX, top: badgeY, opacity: abre(t, c.ini) }}>
          <Moedas s={1} />
        </div>
        <Palavras itens={rt("inv")} t={t} estilo={centro(762, ANTON(84, TOMATE, false))} />
      </div>
    );
  }

  if (g === "cinquenta") {
    // "Por exemplo, vamos supor que você vai para a Europa e quer gastar 50 euros por dia com comida."
    const t50 = at("t50");
    const p = pula(t, t50, 0.28, 1.6);
    return (
      <div style={{ ...BASE, background: BG.cinquenta }}>
        <Palavras itens={rt("supor")} t={t} estilo={centro(70, INTER(50))} />
        <Palavras itens={rt("europa")} t={t} estilo={centro(150, ANTON(96, MOSTARDA, false))} />
        <div style={centro(280, { ...ANTON(330, BRANCO, false), textShadow: "0 8px 0 rgba(0,40,20,0.35)", opacity: p, transform: `scale(${0.6 + 0.4 * p})` })}>50 €</div>
        <Palavras itens={rt("dia")} t={t} estilo={centro(660, ANTON(110, MOSTARDA, false))} />
      </div>
    );
  }

  if (g === "balanca") {
    // "Então você vai usar esse valor pra balancear suas refeições de acordo com a dica número 2."
    const tb = at("tbal");
    const ang = t < tb ? -14 : -14 * Math.cos((t - tb) * 7) * Math.exp(-(t - tb) * 2.2);
    const pd = pula(t, at("tdica"), 0.28, 1.8);
    const pratoY = (lado: number) => Math.sin((ang * Math.PI) / 180) * 260 * lado;
    return (
      <div style={{ ...BASE, background: BG.balanca }}>
        <Palavras itens={rt("valor")} t={t} estilo={centro(50, INTER(52))} />
        <svg width={1080} height={560} style={{ position: "absolute", left: 0, top: 120 }}>
          <rect x={530} y={140} width={20} height={330} rx={10} fill={BRANCO} />
          <path d="M 440 490 L 640 490 L 600 450 L 480 450 Z" fill={BRANCO} />
          <g transform={`rotate(${ang} 540 150)`}>
            <rect x={270} y={140} width={540} height={18} rx={9} fill={MOSTARDA} />
            <circle cx={540} cy={150} r={22} fill={MOSTARDA} />
          </g>
          {[-1, 1].map((lado) => {
            const cx = 540 + lado * 260;
            const cy = 150 + pratoY(lado);
            return (
              <g key={lado}>
                <line x1={cx} y1={cy} x2={cx - 70} y2={cy + 120} stroke={BRANCO} strokeWidth={5} />
                <line x1={cx} y1={cy} x2={cx + 70} y2={cy + 120} stroke={BRANCO} strokeWidth={5} />
                <path d={`M ${cx - 110} ${cy + 120} Q ${cx} ${cy + 190} ${cx + 110} ${cy + 120} Z`} fill={BRANCO} />
                <g transform={`translate(${cx - 45} ${cy + 30})`}>
                  {lado < 0 ? <Sol s={0.6} /> : <Lua s={0.6} cor={MOSTARDA} />}
                </g>
              </g>
            );
          })}
        </svg>
        <div style={centro(700, { opacity: pd, transform: `scale(${0.7 + 0.3 * pd})` })}>
          <span style={{ ...ANTON(110, NOITE, false), background: MOSTARDA, borderRadius: 20, padding: "6px 34px" }}>DICA Nº 2</span>
        </div>
      </div>
    );
  }
  return <div style={BASE} />;
};

/* ---------- grafismo em tela cheia (1080×1920; ele sai da tela, a voz continua) ---------- */

/** Toldo de café de rua (faixas e recortes), desenho de traço. */
const Toldo: React.FC = () => (
  <svg width={1080} height={260} viewBox="0 0 1080 260" style={{ position: "absolute", left: 0, top: 0 }}>
    {Array.from({ length: 9 }, (_, i) => (
      <g key={i}>
        <rect x={i * 120} y={0} width={120} height={190} fill={i % 2 ? CREME : TOMATE} />
        <path d={`M ${i * 120} 190 Q ${i * 120 + 60} 260 ${i * 120 + 120} 190 Z`} fill={i % 2 ? CREME : TOMATE} />
      </g>
    ))}
  </svg>
);

/** Xícara pequena de café preto (espresso), com fumaça. */
const Cafezinho: React.FC<{ t: number }> = ({ t }) => (
  <svg width={620} height={560} viewBox="0 0 620 560">
    {[0, 1, 2].map((i) => {
      const y = (t * 55 + i * 40) % 120;
      return <path key={i} d={`M ${250 + i * 60} ${200 - y * 0.5} q 22 -26 0 -52 q -22 -26 0 -52`} stroke={BRANCO} strokeWidth={14} fill="none" strokeLinecap="round" opacity={Math.max(0, 0.9 - y / 130)} />;
    })}
    <ellipse cx={310} cy={500} rx={250} ry={42} fill={BRANCO} />
    <ellipse cx={310} cy={492} rx={170} ry={22} fill="#EADBC6" />
    <path d="M 150 250 L 470 250 L 448 430 Q 440 468 400 468 L 220 468 Q 180 468 172 430 Z" fill={BRANCO} />
    <path d="M 466 290 q 80 0 72 60 q -8 52 -84 46" stroke={BRANCO} strokeWidth={26} fill="none" />
    <ellipse cx={310} cy={252} rx={160} ry={24} fill={TINTA} />
    <ellipse cx={290} cy={248} rx={60} ry={7} fill="#5B3A28" />
  </svg>
);

const GrafCheio: React.FC<{ c: CenaComida; t: number }> = ({ c, t }) => {
  const d = c.dados ?? {};
  const rt = (k: string) => (d[k] ?? []) as Rot;
  // "O que sobra para comprar na rua é só um menorzinho de toda manhã que não pode faltar, né?"
  const tm = Number(d.tmenor ?? c.ini);
  const px = pula(t, tm, 0.32, 1.7);
  const faltar = rt("faltar");
  const tf = faltar.length ? faltar[faltar.length - 1].t : c.fim;
  const pc = pula(t, tf, 0.3, 2);
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #FFE7B8 0%, #FFB45E 100%)" }}>
      <div style={{ position: "absolute", left: 760, top: lin(t, c.ini, c.ini + 1.6, 520, 300, Easing.out(Easing.cubic)) }}>
        <Sol s={1.6} cor="#FFF4C2" />
      </div>
      <Toldo />
      <Palavras itens={rt("rua")} t={t} estilo={centro(330, ANTON(150, TINTA, false))} />
      <div style={{ position: "absolute", left: 230, top: 470, opacity: px, transform: `scale(${0.5 + 0.5 * px})`, transformOrigin: "50% 80%" }}>
        <Cafezinho t={t} />
      </div>
      <Palavras itens={rt("manha")} t={t} estilo={centro(1110, ANTON(110, BRANCO, false))} sobe={24} />
      <div style={centro(1222, { display: "flex", justifyContent: "center", alignItems: "center", gap: 18 })}>
        <Palavras itens={faltar} t={t} estilo={{ ...INTER(52, TINTA, false) }} />
        <span style={{ display: "inline-block", ...ANTON(64, VERDE, false), opacity: pc, transform: `scale(${pc})` }}>✓</span>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- apoio (vídeo do acervo, sem efeito) ---------- */

const Apoio: React.FC<{ c: CenaComida; t: number }> = ({ c, t }) => {
  const r0 = c.rotulo && c.rotulo.length ? c.rotulo[0].t : Infinity;
  const ar = Number(c.dados?.ar ?? 1080 / 1920);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: H, overflow: "hidden", background: "#000" }}>
      {c.tipo === "foto" ? (
        // foto do Diego, parada e sem filtro (sem zoom: pedido dele para o acervo)
        <Img src={staticFile(c.src!)} style={{ position: "absolute", inset: 0, width: 1080, height: H, objectFit: "cover", objectPosition: String(c.dados?.foco ?? "50% 50%") }} />
      ) : (
        <VideoCobre src={c.src!} W={1080} H={H} focoY={c.foco ?? 0.5} ar={ar} />
      )}
      {c.rotulo ? (
        <>
          <AbsoluteFill style={{ height: H, background: "linear-gradient(to bottom, rgba(0,0,0,0) 50%, rgba(0,0,0,0.6) 100%)", opacity: entra(t, r0) }} />
          <Palavras itens={c.rotulo} t={t} estilo={centro(H - 230, ANTON(130))} />
        </>
      ) : null}
    </div>
  );
};

/* ---------- legenda karaokê (caixa normal, palavra por palavra) ---------- */

const Legenda: React.FC<{ p: PropsComida2; t: number; cheio: boolean; cor: string }> = ({ p, t, cheio, cor }) => {
  const idx = p.grupos.findIndex((gr, k) => {
    const a = p.palavras[gr[0]].s;
    const prox = p.grupos[k + 1];
    const fimG = p.palavras[gr[gr.length - 1]].e + 0.3;
    const b = prox ? Math.min(p.palavras[prox[0]].s, fimG) : fimG;
    return t >= a && t < b;
  });
  if (idx < 0) return null;
  const g = p.grupos[idx];
  const y = cheio ? p.gy[idx] : COSTURA;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y - 37, textAlign: "center" }}>
      <span style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 66, lineHeight: 1.1, textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)" }}>
        {g.map((i, j) => {
          const w = p.palavras[i];
          const prox = j < g.length - 1 ? p.palavras[g[j + 1]].s : w.e + 0.15;
          const o = entra(t, w.s, 0.06);
          const ativa = t >= w.s && t < Math.max(w.e, prox);
          return (
            <span key={i} style={{ color: ativa ? cor : "#fff", opacity: o, whiteSpace: "pre" }}>
              {(j ? " " : "") + w.w}
            </span>
          );
        })}
      </span>
    </div>
  );
};

/* ---------- gancho: a pergunta em letras garrafais (Anton), palavra por palavra, em páginas ---------- */

const Gancho: React.FC<{ p: PropsComida2; t: number }> = ({ p, t }) => {
  const pg = p.gancho.paginas.find((x) => t >= x.ini && t < x.fim);
  if (!pg) return null;
  let y = 270;
  return (
    <>
      <AbsoluteFill style={{ height: COSTURA, background: "linear-gradient(to bottom, rgba(0,0,0,0.55), rgba(0,0,0,0.25) 70%, rgba(0,0,0,0.05))" }} />
      {pg.linhas.map((l, i) => {
        const top = y;
        y += l.tam * 1.08;
        return (
          <Palavras key={`${pg.ini}-${i}`} itens={l.palavras} t={t} sobe={24}
            estilo={{ position: "absolute", left: 72, top, fontFamily: "Anton", fontSize: l.tam, lineHeight: 1.05, color: l.cor ?? "#fff", textShadow: "0 4px 24px rgba(0,0,0,0.6)", whiteSpace: "nowrap" }} />
        );
      })}
    </>
  );
};

const SFX = { impacto: pdxImpacto, swish: pdxSwish, obturador: pdxObturador, riser: pdxRiser } as const;

export const ComidaReel2: React.FC<PropsComida2> = (p) => {
  fontes();
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const cena = p.cenas.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cenas[p.cenas.length - 1];
  const corte = p.cortes.find((c) => f >= Math.round(c.ini * fps) && f < Math.round(c.fim * fps)) ?? p.cortes[p.cortes.length - 1];
  const cheio = cena.tipo === "diego";
  const grafCheio = cena.tipo === "grafcheio";
  const fromC = Math.round(cena.ini * fps);
  const naCta = f >= Math.round(p.cenas[p.cenas.length - 1].ini * fps);
  const legendaVisivel = t >= p.gancho.fim && t < p.cta.leg_fim;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile("voz.wav")} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(2 * fps)}>
          <Audio src={SFX[s.som]} volume={Math.pow(10, s.db / 20)} />
        </Sequence>
      ))}
      <Diego cheio={cheio} pb={!!corte?.pb} divOff={corte?.div_off ?? -340} />
      {grafCheio && (
        <Sequence key={cena.ini} from={fromC} durationInFrames={Math.max(1, Math.round(cena.fim * fps) - fromC + 2)} layout="none">
          <GrafCheio c={cena} t={t} />
        </Sequence>
      )}
      {!cheio && !grafCheio && (
        <Sequence key={cena.ini} from={fromC} durationInFrames={Math.max(1, Math.round(cena.fim * fps) - fromC + 2)} layout="none">
          {cena.tipo === "graf" ? <Grafismo c={cena} t={t} /> : <Apoio c={cena} t={t} />}
          <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: 1080, height: 6, background: "rgba(0,0,0,0.55)" }} />
        </Sequence>
      )}
      <Gancho p={p} t={t} />
      {legendaVisivel && <Legenda p={p} t={t} cheio={cheio || grafCheio} cor={naCta ? AMBAR_CTA : AMBAR} />}
      <Placa rotulo="PRA VIAJAR MELHOR" destino="ME SEGUE" entrada={p.cta.ini * 1000} y={p.cta.placa_y} />
      <Som nome="clack" em={p.cta.ini * 1000} relDb={-6} refLufs={-14} />
    </AbsoluteFill>
  );
};
