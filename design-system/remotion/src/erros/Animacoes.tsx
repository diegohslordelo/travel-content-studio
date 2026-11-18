/**
 * Animações do Reel "Erros de viagem". Pedido do Diego (18/11/2026): toda animação fica SOBRE uma foto
 * (nunca sobre fundo de cor) e só mostra o que a fala diz. Textos na tela = palavras ditas.
 */
import React from "react";
import { Img, staticFile } from "remotion";
import { GRADE_FOTO, PALETA, SOMBRA_TEXTO, TITULO, clamp01, ease, easeBack, easeInOut, lerp } from "./estilo";

export type Marcos = Record<string, number>;
type Area = { w: number; h: number; t: number; dur: number };

/** Foto que cobre a área, com aproximação lenta e linear (Ken Burns). */
export const Foto: React.FC<
  Area & { src: string; kb?: [number, number]; foco?: [number, number]; filtro?: string; desfoque?: number; escurecer?: number }
> = ({ src, w, h, t, dur, kb = [1.0, 1.06], foco = [0.5, 0.5], filtro = GRADE_FOTO, desfoque = 0, escurecer = 0 }) => {
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
          scale: String(z * (desfoque ? 1.08 : 1)),
          transformOrigin: `${foco[0] * 100}% ${foco[1] * 100}%`,
          filter: `${filtro}${desfoque ? ` blur(${desfoque}px)` : ""}${escurecer ? ` brightness(${1 - escurecer})` : ""}`,
        }}
      />
    </div>
  );
};

const aparece = (t: number, em: number, d = 0.22) => ease((t - em) / d);

/* ------------------------------------------------------------------ ícones (traço simples) */

const Pino: React.FC<{ x: number; y: number; s?: number; cor?: string; children?: React.ReactNode; o?: number; k?: number }> = ({
  x,
  y,
  s = 1,
  cor = PALETA.branco,
  children,
  o = 1,
  k = 1,
}) => (
  <g transform={`translate(${x} ${y}) scale(${s * k})`} opacity={o}>
    <path d="M0 0 C -34 -46 -40 -62 -40 -78 A 40 40 0 1 1 40 -78 C 40 -62 34 -46 0 0 Z" fill={cor} stroke="rgba(0,0,0,0.35)" strokeWidth={4} />
    <g transform="translate(0 -80)">{children}</g>
  </g>
);

const Cama: React.FC = () => (
  <g fill="none" stroke={PALETA.fundo} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round">
    <path d="M-24 14 V-14 M-24 4 H24 V14 M-24 -4 H24 V4" />
    <circle cx={-12} cy={-6} r={0.5} />
    <rect x={-20} y={-12} width={12} height={8} rx={3} fill={PALETA.fundo} stroke="none" />
  </g>
);

const Estrela: React.FC = () => (
  <path d="M0 -20 L6 -6 L21 -6 L9 3 L13 18 L0 9 L-13 18 L-9 3 L-21 -6 L-6 -6 Z" fill={PALETA.fundo} />
);

export const Moeda: React.FC<{ x: number; y: number; r?: number; o?: number }> = ({ x, y, r = 34, o = 1 }) => (
  <g transform={`translate(${x} ${y})`} opacity={o}>
    <circle r={r} fill={PALETA.ambar} stroke="#9C7633" strokeWidth={5} />
    <circle r={r * 0.68} fill="none" stroke="#9C7633" strokeWidth={3} />
    <text y={r * 0.36} textAnchor="middle" style={{ font: `400 ${r}px ${TITULO}`, fill: "#7A5A22" }}>
      $
    </text>
  </g>
);

const Xis: React.FC<{ x: number; y: number; s: number; p: number; cor?: string }> = ({ x, y, s, p, cor = PALETA.ambar }) => {
  const a = clamp01(p * 2);
  const b = clamp01(p * 2 - 1);
  if (a <= 0) return null;
  return (
    <g transform={`translate(${x} ${y})`} stroke={cor} strokeWidth={s * 0.16} strokeLinecap="round" fill="none">
      <line x1={-s / 2} y1={-s / 2} x2={-s / 2 + s * a} y2={-s / 2 + s * a} />
      {b > 0 && <line x1={s / 2} y1={-s / 2} x2={s / 2 - s * b} y2={-s / 2 + s * b} />}
    </g>
  );
};

const Carro: React.FC<{ x: number; y: number; s: number }> = ({ x, y, s }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill="none" stroke={PALETA.branco} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round">
    <path d="M-70 10 V-12 L-52 -14 L-34 -42 H34 L52 -14 L70 -12 V10 Z" />
    <path d="M-30 -14 H30 L18 -34 H-18 Z" />
    <circle cx={-40} cy={12} r={14} fill={PALETA.fundo} />
    <circle cx={40} cy={12} r={14} fill={PALETA.fundo} />
  </g>
);

const Aviao: React.FC<{ s?: number; cor?: string }> = ({ s = 1, cor = PALETA.fundo }) => (
  <path
    transform={`scale(${s})`}
    d="M-30 4 L-6 2 L4 22 H12 L8 2 L24 0 L30 8 H36 L32 -2 L36 -12 H30 L24 -4 L8 -6 L12 -26 H4 L-6 -6 L-30 -8 Z"
    fill={cor}
  />
);

/* ------------------------------------------------------------------ 1. notícia real da Serasa */

/**
 * Print real do release da Serasa (serasa.com.br/imprensa, lido em 18/11/2026): cabeçalho em "Segundo o Serasa",
 * rola até a frase do 49% na palavra "49" e a frase é marcada em âmbar. Fundo: o próprio print, desfocado.
 */
export const NoticiaSerasa: React.FC<Area & { m: Marcos; src: string; pagW: number; linhas: { x: number; y: number; w: number; h: number }[] }> = ({
  w,
  h,
  t,
  dur,
  m,
  src,
  pagW,
  linhas,
}) => {
  const cardX = 90;
  const cardY = 150;
  const cardW = w - 2 * cardX;
  const cardH = h - cardY - 44;
  const s = cardW / pagW;
  const alvo = linhas[0].y * s - cardH * 0.42;
  const rola = lerp(t, m.rola, m.rola + 0.55, 0, alvo, easeInOut);
  const entra = ease(t / 0.25);
  const marca = (i: number) => clamp01((t - (m.marca + i * 0.35)) / 0.35);
  const selo = easeBack((t - m.selo) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
        <Img
          src={staticFile(src)}
          style={{ width: w, position: "absolute", top: -rola * 0.4, scale: "1.2", filter: "blur(22px) brightness(0.5)" }}
        />
      </div>
      <div
        style={{
          position: "absolute",
          left: cardX,
          top: cardY,
          width: cardW,
          height: cardH,
          borderRadius: 26,
          overflow: "hidden",
          boxShadow: "0 30px 70px rgba(0,0,0,0.55)",
          background: "#fff",
          opacity: entra,
          scale: String(0.94 + 0.06 * entra),
        }}
      >
        <div style={{ position: "absolute", left: 0, top: -rola, width: cardW }}>
          <Img src={staticFile(src)} style={{ width: cardW, display: "block" }} />
          {linhas.map((l, i) => (
            <div
              key={i}
              style={{
                position: "absolute",
                left: l.x * s - 6,
                top: l.y * s - 4,
                width: (l.w * s + 12) * marca(i),
                height: l.h * s + 8,
                background: "rgba(224,174,92,0.55)",
                mixBlendMode: "multiply",
                borderRadius: 6,
              }}
            />
          ))}
        </div>
      </div>
      {t >= m.selo && (
        <div
          style={{
            position: "absolute",
            right: 136,
            top: cardY + cardH - 250,
            font: `400 230px ${TITULO}`,
            lineHeight: 1,
            color: PALETA.ambar,
            textShadow: "0 8px 30px rgba(0,0,0,0.6)",
            rotate: "-6deg",
            scale: String(0.5 + 0.5 * selo),
            opacity: clamp01(selo * 1.5),
          }}
        >
          49%
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 2. olho fechado para os gastos */

/** Foto de pagamento com cartão; notificações de compra empilhando (só ícones) e "pálpebras" que fecham em "olho fechado". */
export const OlhoFechado: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const notifs = [m.n1, m.n2, m.n3, m.n4];
  const fecha = lerp(t, m.olho, m.olho + 0.35, 0, 1, easeInOut) * (1 - lerp(t, m.abre, m.abre + 0.3, 0, 1, easeInOut));
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.04, 1.12]} foco={[0.5, 0.5]} escurecer={0.15} />
      {notifs.map((em, i) => {
        const p = easeBack((t - em) / 0.28);
        if (t < em) return null;
        const y = 300 + i * 128;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 150,
              top: y,
              width: w - 300,
              height: 108,
              borderRadius: 26,
              background: "rgba(255,255,255,0.92)",
              boxShadow: "0 12px 30px rgba(0,0,0,0.35)",
              display: "flex",
              alignItems: "center",
              gap: 26,
              padding: "0 28px",
              translate: `0 ${(1 - p) * -60}px`,
              opacity: clamp01(p * 1.4),
            }}
          >
            <svg width={70} height={50} viewBox="0 0 70 50">
              <rect x={2} y={2} width={66} height={46} rx={8} fill={PALETA.fundo} />
              <rect x={2} y={12} width={66} height={9} fill={PALETA.ambar} />
            </svg>
            <div style={{ flex: 1 }}>
              <div style={{ height: 16, width: "62%", borderRadius: 8, background: "#2a2a2a" }} />
              <div style={{ height: 12, width: "40%", borderRadius: 6, background: "#9a9a9a", marginTop: 12 }} />
            </div>
            <svg width={52} height={52} viewBox="0 0 52 52">
              <circle cx={26} cy={26} r={24} fill="#2E9E57" />
              <path d="M14 27 L23 35 L39 18" stroke="#fff" strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
        );
      })}
      {/* pálpebras */}
      <div style={{ position: "absolute", left: 0, top: 0, width: w, height: (h / 2) * fecha * 0.92, background: PALETA.preto, borderBottomLeftRadius: "50% 40px", borderBottomRightRadius: "50% 40px" }} />
      <div style={{ position: "absolute", left: 0, bottom: 0, width: w, height: (h / 2) * fecha * 0.92, background: PALETA.preto, borderTopLeftRadius: "50% 40px", borderTopRightRadius: "50% 40px" }} />
    </div>
  );
};

/* ------------------------------------------------------------------ 3. no papel era mais barato */

export const NoPapel: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const e = aparece(t, m.papel, 0.25);
  const risca = clamp01((t - m.risca) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.07]} escurecer={0.25} />
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 360,
          padding: "26px 40px 18px",
          background: PALETA.papel,
          boxShadow: "0 18px 40px rgba(0,0,0,0.45)",
          rotate: "-4deg",
          opacity: e,
          scale: String(0.9 + 0.1 * e),
        }}
      >
        <div style={{ font: `400 126px ${TITULO}`, lineHeight: 1, color: PALETA.fundo, position: "relative" }}>
          MAIS BARATO
          <div style={{ position: "absolute", left: -10, top: "52%", height: 14, width: `${risca * 104}%`, background: PALETA.ambar, borderRadius: 7, rotate: "-3deg" }} />
        </div>
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ 4. 3 pulos do gato */

export const PulosDoGato: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const n = easeBack((t - m.tres) / 0.3);
  const txt = aparece(t, m.pulos, 0.25);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.08]} foco={[0.62, 0.45]} />
      <div style={{ position: "absolute", left: 0, top: 0, width: w, height: h, background: "linear-gradient(90deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.15) 60%, rgba(0,0,0,0) 100%)" }} />
      {t >= m.tres && (
        <div style={{ position: "absolute", left: 72, top: 250, display: "flex", alignItems: "flex-end", gap: 26, textShadow: "0 8px 30px rgba(0,0,0,0.55)" }}>
          <div style={{ font: `400 420px ${TITULO}`, lineHeight: 0.92, color: PALETA.ambar, scale: String(0.6 + 0.4 * n), transformOrigin: "50% 100%" }}>3</div>
          <div style={{ font: `400 108px ${TITULO}`, lineHeight: 0.98, color: PALETA.branco, opacity: txt, translate: `0 ${(1 - txt) * 24}px`, paddingBottom: 22 }}>
            PULOS
            <br />
            DO GATO
          </div>
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 5. cartão de capítulo: DICA 1, 2, 3 */

/**
 * Pedido do Diego: deixar claro qual é a dica 1, 2 e 3 com transição, porque ele não diz o número.
 * O cartão entra com zoom e desfoque (cobrindo a tela desde o 1º quadro) e o número bate; sai ampliando com desfoque.
 */
export const CartaoDica: React.FC<Area & { src: string; n: number; titulo: string[]; simbolo: "xis" | "carro" | "nenhum"; foco?: [number, number] }> = ({
  w,
  h,
  t,
  dur,
  src,
  n,
  titulo,
  simbolo,
  foco,
}) => {
  // cobre a tela inteira desde o 1º quadro (sem área vazia): entra com zoom e desfoque, sai ampliando com desfoque
  const ent = ease(t / 0.28);
  const sai = ease(clamp01((t - (dur - 0.18)) / 0.18));
  const z = (1.25 - 0.25 * ent) * (1 + 0.15 * sai);
  const blur = (1 - ent) * 20 + sai * 14;
  const num = easeBack((t - 0.2) / 0.32);
  const tit = aparece(t, 0.42, 0.25);
  const xis = clamp01((t - 0.75) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden", scale: String(z), filter: blur > 0.3 ? `blur(${blur}px)` : undefined }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.08, 1.14]} foco={foco} desfoque={5} escurecer={0.5} />
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 0%, rgba(0,0,0,0.55) 85%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center", color: PALETA.branco, textShadow: "0 8px 34px rgba(0,0,0,0.6)" }}>
        <div style={{ font: `400 120px ${TITULO}`, letterSpacing: 8, lineHeight: 1 }}>DICA</div>
        <div style={{ font: `400 560px ${TITULO}`, lineHeight: 0.9, color: PALETA.ambar, scale: String(0.4 + 0.6 * num), opacity: clamp01(num * 2) }}>{n}</div>
        <div style={{ marginTop: 34, opacity: tit, translate: `0 ${(1 - tit) * 30}px` }}>
          {titulo.map((l, i) => (
            <div key={i} style={{ font: `400 92px ${TITULO}`, lineHeight: 1.04 }}>
              {l}
            </div>
          ))}
        </div>
        {simbolo !== "nenhum" && (
          <svg width={w} height={200} style={{ position: "absolute", left: 0, top: 1080 + (titulo.length - 1) * 96 }}>
            {simbolo === "xis" && <Xis x={w / 2} y={100} s={120} p={xis} />}
            {simbolo === "carro" && t > 0.7 && <Carro x={w / 2} y={110} s={1.25 * aparece(t, 0.7, 0.25)} />}
          </svg>
        )}
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ 6. fica longe de tudo (mapa sobre foto aérea) */

export const LongeDeTudo: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  // centro (atrações) à esquerda; hotel longe, à direita embaixo
  const centro = { x: 300, y: 520 };
  const hotel = { x: 900, y: 790 };
  const path = `M ${hotel.x} ${hotel.y - 20} C 860 620, 700 760, 600 640 S 420 560, ${centro.x + 40} ${centro.y + 10}`;
  const comp = 900;
  const desenho = clamp01((t - m.rota) / 1.1);
  const hotelIn = easeBack((t - m.hotel) / 0.3);
  const atr = (i: number) => easeBack((t - (m.hotel - 0.25 + i * 0.08)) / 0.3);
  const moedas = [0, 1, 2].map((i) => {
    const em = m.economia + i * 0.22;
    const p = clamp01((t - em) / 0.55);
    return { o: t < m.hotel ? 0 : 1 - p, y: hotel.y - 190 - i * 54 + p * 140, x: hotel.x - 120 + i * 16 };
  });
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.06]} escurecer={0.35} />
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        <path d={path} fill="none" stroke={PALETA.ambar} strokeWidth={12} strokeLinecap="round" strokeDasharray={`${comp * desenho} ${comp}`} />
        <path d={path} fill="none" stroke="rgba(0,0,0,0.0)" strokeWidth={1} />
        {[0, 1, 2].map((i) => (
          <Pino key={i} x={centro.x + [-80, 40, 150][i]} y={centro.y + [30, -40, 40][i]} s={0.85} k={Math.max(0, atr(i))}>
            <Estrela />
          </Pino>
        ))}
        <Pino x={hotel.x} y={hotel.y} s={1.15} cor={PALETA.ambar} k={Math.max(0, hotelIn)}>
          <Cama />
        </Pino>
        {moedas.map((c, i) => (
          <Moeda key={i} x={c.x} y={c.y} r={30} o={Math.max(0, c.o)} />
        ))}
      </svg>
    </div>
  );
};

/* ------------------------------------------------------------------ 7. você perde tempo · tempo em viagem é ouro */

export const TempoOuro: React.FC<Area & { m: Marcos; src: string; srcOuro: string }> = ({ w, h, t, dur, m, src, srcOuro }) => {
  const giro = t < m.tempo ? 0 : (t - m.tempo) * 720 * Math.min(1, (t - m.tempo) / 0.4 + 0.3);
  const ouro = clamp01((t - m.ouro) / 0.35);
  const relIn = easeBack((t - m.tempo + 0.1) / 0.3);
  const txt = aparece(t, m.frase, 0.25);
  const cx = w / 2;
  const cy = 470;
  const R = 190;
  const cor = ouro > 0.5 ? PALETA.ambar : PALETA.branco;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.06]} escurecer={0.4} />
      <div style={{ position: "absolute", inset: 0, opacity: ouro }}>
        <Foto src={srcOuro} w={w} h={h} t={t} dur={dur} kb={[1.05, 1.12]} escurecer={0.35} />
      </div>
      <svg width={w} height={h} style={{ position: "absolute", inset: 0, opacity: clamp01(relIn * 1.5) }}>
        <g transform={`translate(${cx} ${cy}) scale(${0.6 + 0.4 * Math.max(0, relIn)})`}>
          <circle r={R} fill="rgba(0,0,0,0.35)" stroke={cor} strokeWidth={16} />
          {Array.from({ length: 12 }).map((_, i) => (
            <line key={i} x1={0} y1={-R + 22} x2={0} y2={-R + 44} stroke={cor} strokeWidth={8} transform={`rotate(${i * 30})`} strokeLinecap="round" />
          ))}
          <line x1={0} y1={0} x2={0} y2={-R * 0.55} stroke={cor} strokeWidth={14} strokeLinecap="round" transform={`rotate(${giro / 12})`} />
          <line x1={0} y1={0} x2={0} y2={-R * 0.8} stroke={cor} strokeWidth={9} strokeLinecap="round" transform={`rotate(${giro})`} />
          <circle r={14} fill={cor} />
        </g>
      </svg>
      {t >= m.frase && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 690, textAlign: "center", font: `400 104px ${TITULO}`, lineHeight: 1, color: PALETA.branco, textShadow: "0 6px 26px rgba(0,0,0,0.7)", opacity: txt, translate: `0 ${(1 - txt) * 24}px` }}>
          TEMPO É <span style={{ color: PALETA.ambar }}>OURO</span>
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 8. estacionamento grátis? (placa real de valet) */

export const PlacaValet: React.FC<Area & { m: Marcos; src: string; caixa: { x: number; y: number; w: number; h: number } }> = ({ w, h, t, dur, m, src, caixa }) => {
  const tag = easeBack((t - m.tag) / 0.3);
  const caixaP = clamp01((t - m.caixa) / 0.45);
  const per = 2 * (caixa.w + caixa.h);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.02]} foco={[0.5, 0.45]} filtro="contrast(1.06)" />
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        <rect x={caixa.x} y={caixa.y} width={caixa.w} height={caixa.h} rx={14} fill="none" stroke={PALETA.ambar} strokeWidth={10} strokeDasharray={`${per * caixaP} ${per}`} />
      </svg>
      {t >= m.tag && (
        <div
          style={{
            position: "absolute",
            left: 72,
            top: 690,
            padding: "14px 30px 10px",
            background: PALETA.ambar,
            color: PALETA.fundo,
            font: `400 74px ${TITULO}`,
            lineHeight: 1,
            boxShadow: "0 14px 34px rgba(0,0,0,0.5)",
            rotate: "-3deg",
            scale: String(0.5 + 0.5 * tag),
            opacity: clamp01(tag * 1.6),
            transformOrigin: "0% 50%",
          }}
        >
          ESTACIONAMENTO GRÁTIS?
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 9. US$ 20 todo dia */

export const VinteDolares: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const n = easeBack((t - m.vinte) / 0.3);
  const dias = 7;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.07]} escurecer={0.45} />
      {t >= m.vinte && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", color: PALETA.ambar, textShadow: "0 8px 30px rgba(0,0,0,0.6)" }}>
          <span style={{ font: `400 300px ${TITULO}`, lineHeight: 1, display: "inline-block", scale: String(0.5 + 0.5 * n), opacity: clamp01(n * 1.6) }}>US$ 20</span>
        </div>
      )}
      {t >= m.dia && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 590, display: "flex", justifyContent: "center", gap: 14 }}>
          {Array.from({ length: dias }).map((_, i) => {
            const p = easeBack((t - (m.dia + i * 0.11)) / 0.25);
            return (
              <div
                key={i}
                style={{
                  width: 96,
                  height: 112,
                  borderRadius: 14,
                  background: PALETA.papel,
                  boxShadow: "0 10px 24px rgba(0,0,0,0.45)",
                  overflow: "hidden",
                  scale: String(Math.max(0, p)),
                  opacity: clamp01(p * 2),
                }}
              >
                <div style={{ height: 30, background: PALETA.ambar }} />
                <div style={{ font: `400 52px ${TITULO}`, color: PALETA.fundo, textAlign: "center", lineHeight: "84px" }}>$</div>
              </div>
            );
          })}
        </div>
      )}
      {t >= m.dia && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 740, textAlign: "center", font: `400 92px ${TITULO}`, color: PALETA.branco, textShadow: "0 6px 26px rgba(0,0,0,0.7)", opacity: aparece(t, m.dia + 0.3, 0.25) }}>
          TODO DIA
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 10. comprar separado já é um risco */

const Bilhete: React.FC<{ x: number; y: number; rot: number }> = ({ x, y, rot }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 330,
      height: 190,
      borderRadius: 20,
      background: PALETA.papel,
      boxShadow: "0 16px 36px rgba(0,0,0,0.5)",
      rotate: `${rot}deg`,
      overflow: "hidden",
    }}
  >
    <div style={{ height: 52, background: PALETA.ambar }} />
    <svg width={330} height={138} style={{ position: "absolute", top: 52 }}>
      <g transform="translate(70 62)">
        <Aviao s={1.6} />
      </g>
      {Array.from({ length: 14 }).map((_, i) => (
        <rect key={i} x={150 + i * 11} y={34} width={i % 3 === 0 ? 7 : 4} height={66} fill={PALETA.fundo} />
      ))}
    </svg>
  </div>
);

export const SeparadoRisco: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const sep = lerp(t, m.separado, m.separado + 0.45, 0, 1, easeInOut);
  const av = easeBack((t - m.risco) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.06]} escurecer={0.45} />
      <Bilhete x={w / 2 - 330 + 6 - sep * 150} y={330} rot={-4 - sep * 4} />
      <Bilhete x={w / 2 - 6 + sep * 150} y={340} rot={3 + sep * 4} />
      {t >= m.risco && (
        <div style={{ position: "absolute", left: 0, right: 0, top: 560, textAlign: "center", scale: String(0.5 + 0.5 * av), opacity: clamp01(av * 1.6) }}>
          <svg width={170} height={150} viewBox="0 0 170 150">
            <path d="M85 8 L162 142 H8 Z" fill={PALETA.ambar} stroke={PALETA.fundo} strokeWidth={6} strokeLinejoin="round" />
            <rect x={78} y={50} width={14} height={52} rx={6} fill={PALETA.fundo} />
            <circle cx={85} cy={120} r={9} fill={PALETA.fundo} />
          </svg>
          <div style={{ font: `400 96px ${TITULO}`, color: PALETA.branco, lineHeight: 1, textShadow: "0 6px 26px rgba(0,0,0,0.7)" }}>RISCO</div>
        </div>
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ 11. antes, durante e depois */

export const AntesDuranteDepois: React.FC<Area & { m: Marcos; src: string }> = ({ w, h, t, dur, m, src }) => {
  const itens = [
    { txt: "ANTES", em: m.antes },
    { txt: "DURANTE", em: m.durante },
    { txt: "DEPOIS", em: m.depois },
  ];
  const linha = clamp01((t - m.antes) / (m.depois - m.antes + 0.2));
  const y = 560;
  const x0 = 260;
  const passo = 280;
  return (
    <div style={{ position: "absolute", inset: 0, width: w, height: h, overflow: "hidden" }}>
      <Foto src={src} w={w} h={h} t={t} dur={dur} kb={[1.0, 1.07]} escurecer={0.35} />
      <svg width={w} height={h} style={{ position: "absolute", inset: 0 }}>
        <line x1={x0} y1={y} x2={x0 + 2 * passo * linha} y2={y} stroke={PALETA.ambar} strokeWidth={10} strokeLinecap="round" />
        {itens.map((it, i) => {
          const p = easeBack((t - it.em) / 0.28);
          return t >= it.em ? <circle key={i} cx={x0 + i * passo} cy={y} r={26 * Math.max(0, p)} fill={PALETA.ambar} stroke={PALETA.fundo} strokeWidth={6} /> : null;
        })}
      </svg>
      {itens.map((it, i) => {
        const p = aparece(t, it.em, 0.22);
        const x = x0 + i * passo;
        return t >= it.em ? (
          <div key={i} style={{ position: "absolute", left: x - 200, width: 400, top: y - 150, textAlign: "center", font: `400 84px ${TITULO}`, color: PALETA.branco, textShadow: SOMBRA_TEXTO, opacity: p, translate: `0 ${(1 - p) * 26}px` }}>
            {it.txt}
          </div>
        ) : null;
      })}
    </div>
  );
};
