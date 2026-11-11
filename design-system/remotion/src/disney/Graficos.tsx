/**
 * Animações do Reel "Disney de Paris não quer você lá" (reels/disney-5-dicas/), na linguagem do formato tela dividida
 * (fundo #14120F ou o parque desfocado, traço papel, destaque âmbar): a mesma do Reel de Paris.
 * Nada aqui se passa por foto: carteira, ingresso, gato, calendário, mapa, bandeja e mochila são desenho;
 * os prints (AirMagique e App Store) são as páginas reais, só recortadas.
 * Só se escreve na tela o que a fala diz (FORMATOS_REELS 6). O DS V2 não entra aqui (só no CTA).
 */
import React from "react";
import { evolvePath } from "@remotion/paths";
import { Img, staticFile } from "remotion";
import { PALETA, SOMBRA_TEXTO, TEXTO, TITULO, clamp, ease, easeInOut, lerp } from "../paris/estilo";

const PAPEL = PALETA.papel;
const AMBAR = PALETA.ambar;
const FUNDO = PALETA.fundo;
const TRACO = 6;

/** Recuo com sobra (pouso de objeto que cai): passa 6% e volta. */
export const pouso = (p: number) => {
  const x = clamp(p);
  if (x < 0.7) return ease(x / 0.7) * 1.06;
  return 1.06 - 0.06 * easeInOut((x - 0.7) / 0.3);
};
/** Entrada com "pop" (escala 0 → 112% → 100%). */
const pop = (p: number) => {
  const x = clamp(p);
  if (x <= 0) return 0;
  return x < 0.6 ? ease(x / 0.6) * 1.12 : 1.12 - 0.12 * easeInOut((x - 0.6) / 0.4);
};

// ---------------------------------------------------------------- fundo e rótulos
/** Fundo das animações: o próprio parque (quadro do acervo) desfocado e escurecido, para a cena não ficar chapada. */
export const FundoParque: React.FC<{ src?: string; t: number }> = ({ src, t }) => (
  <div style={{ position: "absolute", inset: 0, background: FUNDO, overflow: "hidden" }}>
    {src && (
      <Img
        src={staticFile(src)}
        style={{
          position: "absolute",
          inset: -60,
          width: 1200,
          height: 1020,
          objectFit: "cover",
          filter: "blur(22px) brightness(0.34) saturate(0.8)",
          scale: String(1.04 + 0.02 * clamp(t / 4)),
        }}
      />
    )}
    <div
      style={{
        position: "absolute",
        inset: 0,
        background: "radial-gradient(circle at 40% 55%, rgba(224,174,92,0.14) 0%, rgba(20,18,15,0) 62%)",
      }}
    />
  </div>
);

export type Linha = { texto: string; em: number; ate?: number; tam?: number; cor?: "ambar" | "branco" | "vermelho" | "papel"; fonte?: "titulo" | "texto" };

/** Bloco de rótulos: cada linha sobe de trás de uma máscara no instante da palavra (como o letreiro do formato). */
export const Rotulos: React.FC<{ t: number; x: number; y: number; w: number; linhas: Linha[]; alinhar?: "left" | "center" }> = ({
  t,
  x,
  y,
  w,
  linhas,
  alinhar = "left",
}) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, textAlign: alinhar, textShadow: SOMBRA_TEXTO }}>
    {linhas.map((l, i) => {
      const e = ease((t - l.em) / 0.18);
      const s = 1 - ease((t - (l.ate ?? Infinity)) / 0.18);
      if (e <= 0 || s <= 0) return null;
      const cor = l.cor === "ambar" ? AMBAR : l.cor === "vermelho" ? PALETA.vermelho : l.cor === "papel" ? PAPEL : PALETA.branco;
      const fonte = l.fonte === "texto" ? `800 ${l.tam ?? 40}px ${TEXTO}` : `400 ${l.tam ?? 96}px ${TITULO}`;
      return (
        <div key={i} style={{ overflow: "hidden", paddingTop: 24, marginTop: -24 }}>
          <div
            style={{
              font: fonte,
              lineHeight: 1.0,
              letterSpacing: l.fonte === "texto" ? "0.12em" : undefined,
              color: cor,
              translate: `0 ${(1 - e) * 100}%`,
              opacity: s,
            }}
          >
            {l.texto}
          </div>
        </div>
      );
    })}
  </div>
);

// ---------------------------------------------------------------- print que cai (comprovação)
export type Marca = { r: [number, number, number, number]; em: number };
/** Print real (página da AirMagique com os números da TEA) cai na metade de cima, quica e assenta; marca-texto âmbar nas palavras ditas. */
export const PrintCai: React.FC<{
  t: number;
  src: string;
  w0: number;
  h0: number;
  W: number;
  x: number;
  y: number;
  marcas: Marca[];
  linhas: Linha[];
  colX: number;
  colY: number;
  colW: number;
  fundo?: string;
}> = ({ t, src, w0, h0, W, x, y, marcas, linhas, colX, colY, colW, fundo }) => {
  const esc = W / w0;
  const H = Math.round(h0 * esc);
  const queda = pouso(t / 0.5);
  const yy = lerp(queda, 0, 1, -H - 80, y, (v) => v);
  const giro = (1 - clamp(t / 0.5)) * -6;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <div
        style={{
          position: "absolute",
          left: x,
          top: yy,
          width: W,
          height: H,
          rotate: `${giro}deg`,
          borderRadius: 16,
          overflow: "hidden",
          boxShadow: "0 40px 90px rgba(0,0,0,0.7)",
          border: `3px solid rgba(236,229,216,0.85)`,
        }}
      >
        <Img src={staticFile(src)} style={{ width: W, height: H }} />
        {marcas.map((m, i) => {
          const k = easeInOut((t - m.em) / 0.35);
          if (k <= 0) return null;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: m.r[0] * esc - 3,
                top: m.r[1] * esc - 2,
                width: (m.r[2] * esc + 6) * k,
                height: m.r[3] * esc + 4,
                background: "rgba(224,174,92,0.5)",
                mixBlendMode: "screen",
                borderBottom: `3px solid ${AMBAR}`,
                borderRadius: 3,
              }}
            />
          );
        })}
      </div>
      <Rotulos t={t} x={colX} y={colY} w={colW} linhas={linhas} alinhar="center" />
    </div>
  );
};

// ---------------------------------------------------------------- três cartões (lista falada)
export type Cartao = { src?: string; desenho?: "restaurante"; linhas: string[]; em: number; foco?: [number, number] };
/** "Pessoas rodando… fugir de fila… restaurantes cheios": um cartão por item, cada um cai na sua palavra. */
export const Cartoes: React.FC<{ t: number; itens: Cartao[]; fundo?: string }> = ({ t, itens, fundo }) => (
  <div style={{ position: "absolute", inset: 0 }}>
    <FundoParque src={fundo} t={t} />
    {itens.map((it, i) => {
      const e = pouso((t - it.em + 0.08) / 0.38);
      const vist = t >= it.em - 0.08;
      const xx = 48 + i * 336;
      const giro = [-3, 2, -2][i] * (1 + (1 - clamp((t - it.em) / 0.38)) * 3);
      const z = lerp(t, it.em, it.em + 3, 1.0, 1.08, (p) => p);
      return (
        <div
          key={i}
          style={{ position: "absolute", left: xx, top: 286, width: 312, opacity: vist ? 1 : 0, translate: `0 ${(1 - e) * -560}px`, rotate: `${giro}deg` }}
        >
          <div
            style={{
              width: 312,
              height: 390,
              borderRadius: 16,
              overflow: "hidden",
              border: `5px solid ${PAPEL}`,
              boxShadow: "0 30px 60px rgba(0,0,0,0.6)",
              background: FUNDO,
            }}
          >
            {it.src ? (
              <Img
                src={staticFile(it.src)}
                style={{
                  width: 302,
                  height: 380,
                  objectFit: "cover",
                  objectPosition: `${(it.foco ?? [0.5, 0.5])[0] * 100}% ${(it.foco ?? [0.5, 0.5])[1] * 100}%`,
                  scale: String(z),
                  filter: "saturate(0.8) contrast(1.05) brightness(0.97)",
                }}
              />
            ) : (
              <Restaurante t={t - it.em} />
            )}
          </div>
          <div style={{ marginTop: 18, textAlign: "center", textShadow: SOMBRA_TEXTO }}>
            {it.linhas.map((l, k) => (
              <div
                key={k}
                style={{
                  font: `400 ${k === it.linhas.length - 1 ? 58 : 46}px ${TITULO}`,
                  lineHeight: 1.04,
                  color: k === it.linhas.length - 1 ? AMBAR : PALETA.branco,
                }}
              >
                {l}
              </div>
            ))}
          </div>
        </div>
      );
    })}
  </div>
);

/** Desenho do cartão "restaurantes cheios": mesas ocupadas, todas as cadeiras com gente. */
const Restaurante: React.FC<{ t: number }> = ({ t }) => {
  const mesas: [number, number][] = [
    [80, 120],
    [220, 120],
    [80, 270],
    [220, 270],
  ];
  return (
    <svg width={302} height={380} viewBox="0 0 302 380">
      <rect width={302} height={380} fill="#1d1a16" />
      {/* toldo */}
      <path d="M0 0 H302 V34 Q 287 52 272 34 Q 257 52 242 34 Q 227 52 212 34 Q 197 52 182 34 Q 167 52 152 34 Q 137 52 122 34 Q 107 52 92 34 Q 77 52 62 34 Q 47 52 32 34 Q 17 52 0 34 Z" fill={PALETA.vermelho} opacity={0.9} />
      {mesas.map(([cx, cy], i) => {
        const e = pop((t - 0.1 - i * 0.07) / 0.3);
        return (
          <g key={i} transform={`translate(${cx} ${cy}) scale(${e})`}>
            {[
              [-46, 0],
              [46, 0],
              [0, -44],
              [0, 46],
            ].map(([dx, dy], k) => (
              <g key={k}>
                <circle cx={dx} cy={dy} r={17} fill={k % 2 ? AMBAR : PAPEL} />
                <circle cx={dx} cy={dy - 2} r={7} fill="#1d1a16" opacity={0.25} />
              </g>
            ))}
            <circle r={30} fill="#1d1a16" stroke={PAPEL} strokeWidth={5} />
            <circle r={9} fill={AMBAR} />
          </g>
        );
      })}
    </svg>
  );
};

// ---------------------------------------------------------------- conta: não são baratos + fast pass caro
/** Carteira que se esvazia ("já não são baratos") e, em "comprando", o passe de fila com o carimbo "CARO". */
export const Conta: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const mb = marcos.baratos ?? 1.0;
  const mc = marcos.comprando ?? 3.0;
  const mcaro = marcos.caro ?? 3.6;
  const mfast = marcos.fast ?? 4.1;
  const sai = ease((t - mc + 0.05) / 0.35);
  const entra = ease((t - mc) / 0.4);
  const abre = ease((t - mb + 0.25) / 0.35);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      {/* carteira */}
      <div style={{ position: "absolute", inset: 0, translate: `${-sai * 1100}px 0`, opacity: 1 - sai * 0.6 }}>
        <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
          {Array.from({ length: 7 }).map((_, i) => {
            const p = clamp((t - mb + 0.15 - i * 0.07) / 0.9);
            if (p <= 0) return null;
            const x = 330 + Math.sin(i * 1.7) * 60 + p * (i % 2 ? 140 : -140) * (0.6 + i * 0.08);
            const y = 560 - Math.sin(Math.PI * p) * (230 + i * 18) + p * 160;
            return (
              <g key={i} transform={`translate(${x} ${y}) rotate(${p * 300 * (i % 2 ? 1 : -1)})`} opacity={1 - clamp((p - 0.75) / 0.25)}>
                <ellipse rx={30} ry={30 * Math.abs(Math.cos(p * 8 + i))} fill={AMBAR} stroke="#8a6326" strokeWidth={4} />
              </g>
            );
          })}
          <g transform="translate(330 610)">
            <rect x={-170} y={-110} width={340} height={220} rx={26} fill="#2a241d" stroke={PAPEL} strokeWidth={TRACO} />
            <path d={`M-170 -60 Q 0 ${-60 - 70 * abre} 170 -60`} fill="none" stroke={PAPEL} strokeWidth={TRACO} />
            <rect x={90} y={-20} width={95} height={70} rx={16} fill={FUNDO} stroke={PAPEL} strokeWidth={TRACO} />
            <circle cx={128} cy={15} r={10} fill={AMBAR} />
          </g>
        </svg>
        <Rotulos
          t={t}
          x={560}
          y={430}
          w={460}
          linhas={[
            { texto: "JÁ NÃO SÃO", em: mb - 0.55, tam: 84 },
            { texto: "BARATOS", em: mb - 0.05, tam: 130, cor: "ambar" },
          ]}
        />
      </div>
      {/* passe de fila */}
      <div style={{ position: "absolute", inset: 0, translate: `${(1 - entra) * 1100}px 0`, opacity: entra > 0 ? 1 : 0 }}>
        <div
          style={{
            position: "absolute",
            left: 140,
            top: 420,
            width: 800,
            height: 330,
            borderRadius: 26,
            background: "linear-gradient(135deg, #2b2620 0%, #1c1915 100%)",
            border: `6px solid ${PAPEL}`,
            boxShadow: "0 40px 80px rgba(0,0,0,0.6)",
            rotate: "-3deg",
          }}
        >
          <div style={{ position: "absolute", left: 210, top: 0, bottom: 0, borderLeft: `6px dashed ${PAPEL}`, opacity: 0.6 }} />
          <svg width={210} height={330} style={{ position: "absolute", left: 0, top: 0 }}>
            {/* relógio (fila) */}
            <circle cx={105} cy={165} r={62} fill="none" stroke={AMBAR} strokeWidth={TRACO + 2} />
            <line x1={105} y1={165} x2={105} y2={122} stroke={AMBAR} strokeWidth={TRACO + 2} strokeLinecap="round" />
            <line x1={105} y1={165} x2={138} y2={180} stroke={AMBAR} strokeWidth={TRACO + 2} strokeLinecap="round" />
          </svg>
          <div
            style={{
              position: "absolute",
              left: 250,
              top: 104,
              font: `400 120px ${TITULO}`,
              lineHeight: 1,
              whiteSpace: "nowrap",
              color: PALETA.branco,
              opacity: ease((t - mfast + 0.05) / 0.2),
              translate: `0 ${(1 - ease((t - mfast + 0.05) / 0.2)) * 30}px`,
            }}
          >
            FAST PASS
          </div>
        </div>
        {/* carimbo CARO */}
        {t >= mcaro - 0.05 && (
          <div
            style={{
              position: "absolute",
              left: 640,
              top: 300,
              padding: "6px 34px 2px",
              border: `10px solid ${PALETA.vermelho}`,
              borderRadius: 14,
              font: `400 130px ${TITULO}`,
              color: PALETA.vermelho,
              rotate: "-14deg",
              scale: String(lerp(t, mcaro - 0.05, mcaro + 0.12, 2.2, 1, ease)),
              opacity: clamp((t - mcaro + 0.05) / 0.08),
              background: "rgba(20,18,15,0.35)",
              textShadow: "0 0 1px rgba(0,0,0,0.3)",
            }}
          >
            CARO
          </div>
        )}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- cinco pulos do gato (castelo em traço)
const CASTELO =
  "M0 820 L60 820 L60 640 L80 640 L80 620 L100 620 L100 640 L120 640 L120 620 L140 620 L140 640 L160 640 L160 820 " +
  "L220 820 L220 560 L240 560 L240 540 L260 540 L260 560 L280 560 L280 540 L300 540 L300 560 L320 560 L320 820 " +
  "L400 820 L400 500 L470 500 L470 400 L500 330 L515 250 L525 170 L540 120 L555 170 L565 250 L580 330 L610 400 L610 500 L680 500 L680 820 " +
  "L760 820 L760 560 L780 560 L780 540 L800 540 L800 560 L820 560 L820 540 L840 540 L840 560 L860 560 L860 820 " +
  "L920 820 L920 640 L940 640 L940 620 L960 620 L960 640 L980 640 L980 620 L1000 620 L1000 640 L1020 640 L1020 820 L1080 820";
const POUSOS5: [number, number][] = [
  [30, 816],
  [110, 616],
  [270, 536],
  [435, 496],
  [645, 496],
  [810, 536],
];

const GatoSentado: React.FC<{ cor: string }> = ({ cor }) => (
  <g>
    <path d="M-30 0 C -34 -30, -26 -58, 0 -62 C 26 -58, 34 -30, 30 0 Z" fill={cor} />
    <circle cx={0} cy={-74} r={22} fill={cor} />
    <path d="M-20 -86 L-17 -112 L-4 -94 Z" fill={cor} />
    <path d="M20 -86 L17 -112 L4 -94 Z" fill={cor} />
    <path d="M26 -6 C 58 -10, 62 -46, 44 -60" stroke={cor} strokeWidth={9} strokeLinecap="round" fill="none" />
    <circle cx={-8} cy={-76} r={3.2} fill={FUNDO} />
    <circle cx={8} cy={-76} r={3.2} fill={FUNDO} />
  </g>
);

export const Gato5: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const ev = evolvePath(easeInOut(t / 0.6), CASTELO);
  const s0 = marcos.pulos ?? 0.1;
  const DUR = 0.36;
  const PASSO = 0.42;
  let gx = POUSOS5[0][0];
  let gy = POUSOS5[0][1];
  let squash = 1;
  for (let k = 0; k < 5; k++) {
    const ini = s0 + k * PASSO;
    if (t >= ini) {
      const p = clamp((t - ini) / DUR);
      const [x0, y0] = POUSOS5[k];
      const [x1, y1] = POUSOS5[k + 1];
      const pe = easeInOut(p);
      const alto = k === 3 ? 230 : 120;
      gx = x0 + (x1 - x0) * pe;
      gy = y0 + (y1 - y0) * pe - Math.sin(Math.PI * pe) * alto;
      const d = t - ini - DUR;
      if (d >= 0 && d < 0.1) squash = 0.82 + 0.18 * (d / 0.1);
    }
  }
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <path
          d={CASTELO}
          fill="none"
          stroke={PAPEL}
          strokeWidth={5}
          strokeLinejoin="round"
          strokeDasharray={ev.strokeDasharray}
          strokeDashoffset={ev.strokeDashoffset}
        />
        {POUSOS5.slice(1).map(([x, y], i) => {
          const e = pop((t - (s0 + i * PASSO + DUR)) / 0.25);
          if (e <= 0) return null;
          return (
            <g key={i} transform={`translate(${x} ${y - 150}) scale(${e})`}>
              <circle r={30} fill={AMBAR} />
              <text y={13} textAnchor="middle" style={{ font: `400 40px ${TITULO}` }} fill={FUNDO}>
                {i + 1}
              </text>
            </g>
          );
        })}
        <g transform={`translate(${gx} ${gy}) scale(${1 / squash} ${squash})`}>
          <GatoSentado cor={AMBAR} />
        </g>
      </svg>
      <Rotulos
        t={t}
        x={680}
        y={300}
        w={360}
        alinhar="left"
        linhas={[
          { texto: "5 PULOS", em: s0 - 0.2, tam: 104, cor: "ambar" },
          { texto: "DO GATO", em: s0 + 0.1, tam: 76 },
        ]}
      />
    </div>
  );
};

// ---------------------------------------------------------------- dica 1: dia de semana
/** Sete colunas de calendário (sem rótulos de dia: só o que é dito); as cinco do meio da semana acendem em âmbar, o fim de semana fica apagado. */
export const Semana: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const em = marcos.semana ?? 1.0;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      {Array.from({ length: 7 }).map((_, i) => {
        const fds = i >= 5;
        const e = pouso((t - 0.05 - i * 0.05) / 0.35);
        const acende = fds ? 0 : ease((t - em + 0.25 - i * 0.07) / 0.2);
        const x = 72 + i * 134;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: 500,
              width: 120,
              height: 300,
              borderRadius: 18,
              border: `5px solid ${fds ? "rgba(236,229,216,0.35)" : PAPEL}`,
              background: fds
                ? "repeating-linear-gradient(-45deg, rgba(236,229,216,0.08) 0 14px, rgba(0,0,0,0) 14px 28px)"
                : `rgba(224,174,92,${0.92 * acende})`,
              translate: `0 ${(1 - e) * -420}px`,
              opacity: e > 0 ? 1 : 0,
              boxShadow: acende > 0.5 ? "0 0 50px rgba(224,174,92,0.45)" : "0 20px 40px rgba(0,0,0,0.45)",
            }}
          >
            <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 46, borderBottom: `5px solid ${fds ? "rgba(236,229,216,0.35)" : PAPEL}` }} />
            {!fds && acende > 0.5 && (
              <svg width={120} height={250} style={{ position: "absolute", top: 46 }}>
                <path
                  d="M28 128 L52 154 L94 100"
                  fill="none"
                  stroke={FUNDO}
                  strokeWidth={12}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeDasharray={120}
                  strokeDashoffset={120 * (1 - clamp((acende - 0.5) * 2))}
                />
              </svg>
            )}
          </div>
        );
      })}
      <Rotulos
        t={t}
        x={250}
        y={300}
        w={800}
        linhas={[
          { texto: "DIA DE", em: em - 0.45, tam: 84 },
          { texto: "SEMANA", em: em - 0.1, tam: 110, cor: "ambar" },
        ]}
      />
    </div>
  );
};

// ---------------------------------------------------------------- dica 1: ingresso park hopper
export const ParkHopper: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const e = pouso((t - 0.02) / 0.42);
  const m2 = marcos.dois ?? 1.4;
  const m1 = marcos.unico ?? 2.3;
  const parte = (em: number) => ease((t - em + 0.05) / 0.22);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 330,
          width: 860,
          height: 440,
          borderRadius: 30,
          background: "linear-gradient(135deg, #322a20 0%, #1d1915 100%)",
          border: `6px solid ${PAPEL}`,
          boxShadow: "0 40px 90px rgba(0,0,0,0.6)",
          translate: `${(1 - e) * 1200}px 0`,
          rotate: `${(1 - clamp(t / 0.42)) * 8 - 2}deg`,
        }}
      >
        <div style={{ position: "absolute", left: 230, top: 0, bottom: 0, borderLeft: `6px dashed ${PAPEL}`, opacity: 0.55 }} />
        <svg width={230} height={440} style={{ position: "absolute", left: 0, top: 0 }}>
          {/* dois castelinhos: os dois parques */}
          {[0, 1].map((k) => {
            const a = pop((t - m2 - k * 0.12) / 0.3);
            return (
              <g key={k} transform={`translate(${115} ${k ? 300 : 150}) scale(${0.25 + 0.75 * a})`} opacity={0.35 + 0.65 * a}>
                <path d="M-50 40 V-10 H-36 V-30 H-22 V-10 H-8 V-46 L0 -70 L8 -46 V-10 H22 V-30 H36 V-10 H50 V40 Z" fill={a > 0.5 ? AMBAR : "none"} stroke={AMBAR} strokeWidth={5} strokeLinejoin="round" />
              </g>
            );
          })}
        </svg>
        <div style={{ position: "absolute", left: 270, top: 60, font: `400 112px ${TITULO}`, lineHeight: 1, color: AMBAR, whiteSpace: "nowrap" }}>PARK HOPPER</div>
        <div
          style={{
            position: "absolute",
            left: 274,
            top: 230,
            font: `400 86px ${TITULO}`,
            color: PALETA.branco,
            opacity: parte(m2),
            translate: `0 ${(1 - parte(m2)) * 24}px`,
          }}
        >
          2 PARQUES
        </div>
        <div
          style={{
            position: "absolute",
            left: 274,
            top: 324,
            font: `400 86px ${TITULO}`,
            color: PALETA.branco,
            opacity: parte(m1),
            translate: `0 ${(1 - parte(m1)) * 24}px`,
          }}
        >
          1 DIA
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- dica 1: aproveitar tudo
/** Três ícones de atração (castelo, montanha-russa, fogos) recebem o visto, um a um. */
export const Aproveitar: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const em = marcos.aproveitar ?? 0.5;
  const icones = [
    "M-46 40 V-6 H-32 V-24 H-18 V-6 H-6 V-40 L0 -64 L6 -40 V-6 H18 V-24 H32 V-6 H46 V40 Z",
    "M-60 40 C -40 -60, -10 -60, 0 0 C 10 50, 40 50, 60 -40 M-60 40 L-60 52 M-20 -20 L-20 52 M20 30 L20 52 M60 -40 L60 52",
    "M0 0 L0 -50 M0 0 L42 -30 M0 0 L-42 -30 M0 0 L30 32 M0 0 L-30 32 M0 0 L52 6 M0 0 L-52 6",
  ];
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      {icones.map((d, i) => {
        const e = pop((t - 0.05 - i * 0.08) / 0.3);
        const ok = clamp((t - em - i * 0.16) / 0.18);
        const x = 220 + i * 320;
        return (
          <div key={i} style={{ position: "absolute", left: x - 120, top: 470, width: 240, height: 240, scale: String(e) }}>
            <svg width={240} height={240} viewBox="-120 -120 240 240">
              <circle r={104} fill={ok >= 1 ? "rgba(224,174,92,0.22)" : "rgba(20,18,15,0.6)"} stroke={PAPEL} strokeWidth={TRACO} />
              <path d={d} fill="none" stroke={PAPEL} strokeWidth={TRACO} strokeLinejoin="round" strokeLinecap="round" />
              {ok > 0 && (
                <g transform="translate(72 -72)">
                  <circle r={34} fill={AMBAR} transform={`scale(${pop(ok)})`} />
                  <path d="M-15 0 L-4 12 L16 -12" fill="none" stroke={FUNDO} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={50} strokeDashoffset={50 * (1 - ok)} />
                </g>
              )}
            </svg>
          </div>
        );
      })}
      <Rotulos
        t={t}
        x={72}
        y={290}
        w={936}
        alinhar="center"
        linhas={[{ texto: "APROVEITAR TUDO", em: em - 0.1, tam: 120, cor: "ambar" }]}
      />
    </div>
  );
};

// ---------------------------------------------------------------- dica 2: o app (print real da App Store)
/**
 * Celular com o print da App Store que o Diego enviou: cai na palavra "aplicativo"; em "fila" a tela rola até as prévias
 * (a da direita fala da fila rápida, o Premier Access); em "print" (fala 8) o celular volta e pisca como captura de tela.
 */
export const Celular: React.FC<{
  t: number;
  src: string;
  marcos: Record<string, number>;
  linhas: Linha[];
  rola?: boolean;
  cai?: boolean;
  fundo?: string;
}> = ({ t, src, marcos, linhas, rola = true, cai = true, fundo }) => {
  const W0 = 1206; // print: 1206 × 2622
  const SW = 440; // largura da tela
  const esc = SW / W0;
  const JANELA = 540;
  const topo0 = 300; // a tela começa abaixo da barra de status (sem o relógio do celular)
  const topo1 = 1180;
  const mc = marcos.cai ?? 0;
  const mr = marcos.rola ?? 99;
  const mf = marcos.flash ?? 99;
  const q = cai ? pouso((t - mc) / 0.5) : ease(t / 0.3);
  const y0 = 300;
  const yy = cai ? lerp(q, 0, 1, -JANELA - 160, y0, (v) => v) : y0 + (1 - q) * 40;
  const giro = cai ? (1 - clamp((t - mc) / 0.5)) * 7 : 0;
  const r = rola ? easeInOut((t - mr + 0.1) / 0.6) : 0;
  const off = (topo0 + (topo1 - topo0) * r) * esc;
  const flash = t >= mf ? Math.max(0, 1 - (t - mf) / 0.28) : 0;
  const aperta = t >= mf ? 1 - 0.04 * Math.sin(Math.PI * clamp((t - mf) / 0.25)) : 1;
  const marca = rola ? easeInOut((t - mr - 0.45) / 0.35) : 0;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <div
        style={{
          position: "absolute",
          left: 572,
          top: yy,
          width: SW + 28,
          height: JANELA + 28,
          borderRadius: 54,
          background: "#0d0d0d",
          border: "3px solid #3a3a3a",
          boxShadow: "0 40px 90px rgba(0,0,0,0.7)",
          rotate: `${giro}deg`,
          scale: String(aperta),
          opacity: cai ? (t >= mc - 0.02 ? 1 : 0) : q,
        }}
      >
        <div style={{ position: "absolute", left: 14, top: 14, width: SW, height: JANELA, borderRadius: 42, overflow: "hidden", background: "#000" }}>
          <Img src={staticFile(src)} style={{ position: "absolute", left: 0, top: -off, width: SW, height: 2622 * esc }} />
          {/* marca na prévia da fila rápida (x 795–1206, y 1904–2073 no print) */}
          {marca > 0 && (
            <div
              style={{
                position: "absolute",
                left: 795 * esc - 4,
                top: 1904 * esc - off - 4,
                width: (1206 - 795) * esc + 8,
                height: (2073 - 1904) * esc + 8,
                border: `5px solid ${AMBAR}`,
                borderRadius: 14,
                opacity: marca,
                boxShadow: "0 0 30px rgba(224,174,92,0.55)",
              }}
            />
          )}
          <div style={{ position: "absolute", inset: 0, background: "#fff", opacity: flash }} />
        </div>
      </div>
      <Rotulos t={t} x={72} y={470} w={480} linhas={linhas} />
    </div>
  );
};

// ---------------------------------------------------------------- dica 2: roteiro e pedido de comida
/** Mapa em traço com 4 pinos e a rota tracejada que se desenha em "roteiro"; em "pedir" vira o pedido no celular. */
export const RoteiroComida: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const mr = marcos.roteiro ?? 0.6;
  const mp = marcos.pedir ?? 1.6;
  const mcom = marcos.comida ?? 2.0;
  const troca = ease((t - mp + 0.05) / 0.3);
  const ROTA = "M180 760 C 260 640, 360 700, 420 600 S 600 520, 640 620 S 820 720, 880 560";
  const ev = evolvePath(easeInOut((t - mr + 0.2) / 0.7), ROTA);
  const pinos: [number, number][] = [
    [180, 760],
    [420, 600],
    [640, 620],
    [880, 560],
  ];
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <div style={{ position: "absolute", inset: 0, opacity: 1 - troca, translate: `${-troca * 200}px 0` }}>
        <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
          {/* quadras do parque */}
          {[
            "M90 480 Q 300 430 520 470 T 990 450 L 990 850 L 90 850 Z",
          ].map((d, i) => (
            <path key={i} d={d} fill="rgba(236,229,216,0.05)" stroke="rgba(236,229,216,0.35)" strokeWidth={4} />
          ))}
          <path d="M130 820 C 300 700, 500 820, 700 700 S 940 760, 980 640" fill="none" stroke="rgba(236,229,216,0.25)" strokeWidth={26} strokeLinecap="round" />
          <path d={ROTA} fill="none" stroke={AMBAR} strokeWidth={9} strokeLinecap="round" strokeDasharray={`${ev.strokeDasharray}`} strokeDashoffset={ev.strokeDashoffset} />
          {pinos.map(([x, y], i) => {
            const e = pop((t - 0.05 - i * 0.08) / 0.3);
            return (
              <g key={i} transform={`translate(${x} ${y}) scale(${e})`}>
                <path d="M0 0 C -10 -18, -26 -30, -26 -48 A 26 26 0 1 1 26 -48 C 26 -30, 10 -18, 0 0 Z" fill={i === 3 ? AMBAR : PAPEL} stroke={FUNDO} strokeWidth={3} />
                <circle cy={-48} r={10} fill={FUNDO} />
              </g>
            );
          })}
        </svg>
        <Rotulos t={t} x={72} y={300} w={936} linhas={[{ texto: "ROTEIRO", em: mr - 0.1, tam: 130, cor: "ambar" }]} />
      </div>
      <div style={{ position: "absolute", inset: 0, opacity: troca, translate: `${(1 - troca) * 200}px 0` }}>
        <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
          <g transform="translate(270 590)">
            <rect x={-120} y={-230} width={240} height={440} rx={36} fill="#151310" stroke={PAPEL} strokeWidth={TRACO} />
            <rect x={-40} y={-210} width={80} height={14} rx={7} fill={PAPEL} opacity={0.5} />
            {/* bandeja com lanche */}
            <g transform={`translate(0 -20) scale(${pop((t - mcom + 0.1) / 0.3)})`}>
              <path d="M-70 30 H70 L56 64 H-56 Z" fill="none" stroke={PAPEL} strokeWidth={5} strokeLinejoin="round" />
              <path d="M-52 14 Q 0 -60 52 14 Z" fill={AMBAR} />
              <rect x={-56} y={14} width={112} height={14} rx={7} fill={PAPEL} />
            </g>
            <g transform={`translate(0 130) scale(${pop((t - mcom - 0.35) / 0.3)})`}>
              <circle r={40} fill={AMBAR} />
              <path d="M-18 0 L-5 14 L20 -14" fill="none" stroke={FUNDO} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
            </g>
          </g>
        </svg>
        <Rotulos
          t={t}
          x={470}
          y={430}
          w={560}
          linhas={[
            { texto: "PEDIR A", em: mp - 0.05, tam: 92 },
            { texto: "COMIDA", em: mcom - 0.1, tam: 130, cor: "ambar" },
            { texto: "ANTES", em: (marcos.antes ?? mcom + 0.35) - 0.1, tam: 92 },
          ]}
        />
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- dica 3: comida cara
/** Bandeja com hambúrguer, batata e refrigerante; "CARA MESMO" e, em "nem é lá essas coisas", o lanche murcha. */
export const Comida: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const mc = marcos.cara ?? 1.4;
  const mn = marcos.nem ?? 2.5;
  const murcha = ease((t - mn) / 0.5);
  const e = pouso((t - 0.05) / 0.4);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <g transform={`translate(330 ${640 + (1 - e) * -500})`}>
          {/* bandeja */}
          <path d="M-250 120 H250 L220 170 H-220 Z" fill="#2a241d" stroke={PAPEL} strokeWidth={TRACO} strokeLinejoin="round" />
          {/* refrigerante */}
          <g transform="translate(170 0)">
            <path d="M-50 -110 H50 L38 110 H-38 Z" fill={PALETA.vermelho} stroke={PAPEL} strokeWidth={5} strokeLinejoin="round" />
            <rect x={-56} y={-130} width={112} height={22} rx={8} fill={PAPEL} />
            <path d="M10 -130 L30 -200" stroke={PAPEL} strokeWidth={9} strokeLinecap="round" />
          </g>
          {/* batata */}
          <g transform="translate(-170 10)">
            {[-36, -18, 0, 18, 36].map((x, i) => (
              <rect key={i} x={x - 7} y={-120 + (i % 2) * 14} width={14} height={110} rx={5} fill={AMBAR} transform={`rotate(${(x / 36) * 8 + murcha * (i % 2 ? 22 : -18)} ${x} -10)`} />
            ))}
            <path d="M-60 -40 H60 L46 100 H-46 Z" fill={PALETA.vermelho} stroke={PAPEL} strokeWidth={5} strokeLinejoin="round" />
          </g>
          {/* hambúrguer */}
          <g transform={`translate(0 ${30 + murcha * 18}) scale(1 ${1 - 0.22 * murcha})`}>
            <path d="M-110 -10 Q 0 -150 110 -10 Z" fill={AMBAR} stroke={PAPEL} strokeWidth={5} />
            <rect x={-118} y={-10} width={236} height={18} rx={9} fill="#6aa84f" />
            <rect x={-112} y={8} width={224} height={30} rx={12} fill="#5a3a26" stroke={PAPEL} strokeWidth={4} />
            <path d="M-110 38 H110 Q 100 84 0 84 Q -100 84 -110 38 Z" fill={AMBAR} stroke={PAPEL} strokeWidth={5} />
          </g>
        </g>
      </svg>
      <Rotulos
        t={t}
        x={630}
        y={410}
        w={420}
        linhas={[
          { texto: "CARA", em: mc - 0.1, ate: mn - 0.05, tam: 150, cor: "ambar" },
          { texto: "MESMO", em: mc + 0.15, ate: mn - 0.05, tam: 110 },
        ]}
      />
      <Rotulos
        t={t}
        x={630}
        y={410}
        w={420}
        linhas={[
          { texto: "NEM É LÁ", em: mn + 0.05, tam: 90 },
          { texto: "ESSAS", em: mn + 0.2, tam: 90 },
          { texto: "COISAS", em: mn + 0.35, tam: 110, cor: "ambar" },
        ]}
      />
    </div>
  );
};

// ---------------------------------------------------------------- dica 3: lanche na mochila
export const Mochila: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const ml = marcos.lanche ?? 0.5;
  const mg = marcos.gastar ?? 2.4;
  const e = pouso((t - 0.02) / 0.4);
  const cai = clamp((t - ml + 0.15) / 0.45);
  const yBar = -420 + 420 * easeInOut(cai);
  const pula = t > ml + 0.3 ? Math.max(0, Math.sin((t - ml - 0.3) * 18) * Math.exp(-(t - ml - 0.3) * 6)) * 10 : 0;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <g transform={`translate(320 ${620 - pula}) scale(${e})`}>
          {/* barra de cereal caindo dentro da mochila */}
          {cai > 0 && cai < 1 && (
            <g transform={`translate(0 ${yBar}) rotate(${(1 - cai) * 30})`}>
              <rect x={-90} y={-30} width={180} height={60} rx={14} fill={AMBAR} stroke={PAPEL} strokeWidth={5} />
              <path d="M-90 -30 L-110 -40 L-110 40 L-90 30 M90 -30 L110 -40 L110 40 L90 30" fill={AMBAR} stroke={PAPEL} strokeWidth={4} />
            </g>
          )}
          {/* mochila */}
          <path d="M-60 -170 Q 0 -230 60 -170" fill="none" stroke={PAPEL} strokeWidth={TRACO + 2} />
          <rect x={-150} y={-170} width={300} height={330} rx={70} fill="#2a241d" stroke={PAPEL} strokeWidth={TRACO} />
          <rect x={-105} y={10} width={210} height={120} rx={30} fill="#1d1915" stroke={PAPEL} strokeWidth={5} />
          <path d="M-150 -60 Q 0 -10 150 -60" fill="none" stroke={PAPEL} strokeWidth={5} />
          <circle cx={0} cy={-40} r={9} fill={AMBAR} />
          {cai >= 1 && (
            <g transform="translate(0 -150)">
              <rect x={-60} y={-24} width={120} height={40} rx={10} fill={AMBAR} stroke={PAPEL} strokeWidth={4} />
            </g>
          )}
        </g>
      </svg>
      <Rotulos
        t={t}
        x={600}
        y={380}
        w={450}
        linhas={[
          { texto: "LANCHE", em: ml - 0.05, tam: 130, cor: "ambar" },
          { texto: "NA MOCHILA", em: ml + 0.3, tam: 84 },
        ]}
      />
      <Rotulos t={t} x={600} y={640} w={450} linhas={[{ texto: "NÃO GASTAR MUITO", em: mg - 0.05, tam: 40, fonte: "texto", cor: "papel" }]} />
    </div>
  );
};

// ---------------------------------------------------------------- dica de ouro
export const DicaOuro: React.FC<{ t: number; marcos: Record<string, number>; fundo?: string }> = ({ t, marcos, fundo }) => {
  const md = marcos.dica ?? 0.5;
  const e = pop((t - 0.03) / 0.35); // a medalha já entra no começo da cena; o rótulo espera a palavra "dica"
  const brilho = clamp((t - md) / 0.6);
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <FundoParque src={fundo} t={t} />
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <g transform={`translate(300 590) scale(${e}) rotate(${(1 - clamp((t - 0.03) / 0.4)) * -25})`}>
          <path d="M-70 -40 L-120 170 L-60 140 L-30 200 L10 -10 Z" fill={PALETA.vermelho} stroke={PAPEL} strokeWidth={4} />
          <path d="M70 -40 L120 170 L60 140 L30 200 L-10 -10 Z" fill={PALETA.vermelho} stroke={PAPEL} strokeWidth={4} />
          <circle r={150} fill="#d4a24c" stroke="#f3d38a" strokeWidth={10} />
          <circle r={112} fill="none" stroke="#9a6d27" strokeWidth={6} />
          <path d="M0 -70 L20 -22 L72 -20 L32 12 L46 62 L0 34 L-46 62 L-32 12 L-72 -20 L-20 -22 Z" fill="#f6dc9a" />
          <path d={`M${-150 + 300 * brilho} -150 L${-110 + 300 * brilho} -150 L${-260 + 300 * brilho} 150 L${-300 + 300 * brilho} 150 Z`} fill="#fff" opacity={0.35 * (1 - brilho)} />
        </g>
      </svg>
      <Rotulos
        t={t}
        x={530}
        y={430}
        w={520}
        linhas={[
          { texto: "DICA DE", em: md - 0.1, tam: 100 },
          { texto: "OURO", em: md + 0.1, tam: 170, cor: "ambar" },
        ]}
      />
    </div>
  );
};
