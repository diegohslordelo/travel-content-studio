/**
 * Animações do Reel de Paris, na linguagem do formato (fundo #14120F, traço papel, destaque âmbar).
 * Nada aqui se passa por foto: fita, gato, calendário e mapa são desenho; o print é a página real da Euromonitor.
 * Só se escreve na tela o que a fala diz (FORMATOS_REELS 6).
 */
import React from "react";
import { evolvePath } from "@remotion/paths";
import { Img, staticFile } from "remotion";
import {
  PALETA,
  SOMBRA_TEXTO,
  TEXTO,
  TITULO,
  clamp,
  comOrdinal,
  ease,
  easeInOut,
  lerp,
} from "./estilo";

/** Recuo com sobra (pouso de objeto que cai): passa 6% e volta. */
const pouso = (p: number) => {
  const x = clamp(p);
  if (x < 0.7) return ease(x / 0.7) * 1.06;
  return 1.06 - 0.06 * easeInOut((x - 0.7) / 0.3);
};

// ---------------------------------------------------------------- gancho: fita zebrada
/**
 * Fita zebrada (vermelho e branco) que atravessa a imagem do gancho: desenho chapado, sem textura de foto,
 * para não parecer que a fita estava na cena real (CLAUDE.md 9, contexto verdadeiro). Cada faixa entra
 * deslizando da lateral no instante da palavra e fica balançando de leve.
 */
export const Fita: React.FC<{
  t: number;
  faixas: { em: number; y: number; giro: number; lado: "esq" | "dir" }[];
}> = ({ t, faixas }) => (
  <>
    {faixas.map((f, i) => {
      const e = easeInOut((t - f.em) / 0.32);
      if (e <= 0) return null;
      const dx = (1 - e) * (f.lado === "esq" ? -1400 : 1400);
      const balanco = Math.sin((t - f.em) * 3.1 + i) * 0.6;
      return (
        <div
          key={i}
          style={{
            position: "absolute",
            left: -200,
            top: f.y,
            width: 1480,
            height: 74,
            translate: `${dx}px 0`,
            rotate: `${f.giro + balanco}deg`,
            background: `repeating-linear-gradient(-45deg, ${PALETA.vermelho} 0 46px, #F4F1EA 46px 92px)`,
            boxShadow: "0 14px 30px rgba(0,0,0,0.45)",
            borderTop: "2px solid rgba(255,255,255,0.35)",
            borderBottom: "2px solid rgba(0,0,0,0.25)",
          }}
        />
      );
    })}
  </>
);

// ---------------------------------------------------------------- ranking (print da Euromonitor)
/**
 * O print cai na metade de cima quando o Diego aponta para cima ("esse ranking aqui"), quica e assenta.
 * Na palavra "primeiro", um marca-texto âmbar passa na frase "Paris is crowned the world's leading city"
 * e o "1º" entra à direita.
 */
export const Ranking: React.FC<{
  t: number;
  src: string;
  marcos: Record<string, number>;
}> = ({ t, src, marcos }) => {
  const W = 620;
  const esc = W / 1290; // o print (recortado do título à data) tem 1290 × 995 px
  const H = Math.round(995 * esc);
  const queda = pouso(t / 0.5);
  const y = lerp(queda, 0, 1, -H - 60, 300, (x) => x);
  const giro = (1 - clamp(t / 0.5)) * -7;
  const mp = marcos.primeiro ?? 99;
  const marca = easeInOut((t - mp + 0.05) / 0.4);
  const um = ease((t - mp - 0.1) / 0.3);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 35% 45%, rgba(224,174,92,0.16) 0%, rgba(20,18,15,0) 60%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 72,
          top: y,
          width: W,
          height: H,
          rotate: `${giro}deg`,
          borderRadius: 18,
          overflow: "hidden",
          background: "#fff",
          boxShadow: "0 40px 90px rgba(0,0,0,0.65)",
        }}
      >
        <Img src={staticFile(src)} style={{ width: W, height: H }} />
        {/* marca-texto: linha 1 do subtítulo (x 26–1121, y 566–646 no print) */}
        <div
          style={{
            position: "absolute",
            left: 26 * esc,
            top: 566 * esc,
            width: 1095 * esc * marca,
            height: 80 * esc,
            background: "rgba(224,174,92,0.55)",
            mixBlendMode: "multiply",
            borderRadius: 4,
          }}
        />
      </div>
      <div
        style={{
          position: "absolute",
          left: 740,
          top: 300,
          width: 290,
          textAlign: "center",
          opacity: um,
          scale: String(0.6 + 0.4 * um),
          textShadow: SOMBRA_TEXTO,
        }}
      >
        <div
          style={{
            font: `400 250px ${TITULO}`,
            lineHeight: 1,
            color: PALETA.ambar,
          }}
        >
          {comOrdinal("1º")}
        </div>
        <div
          style={{
            font: `700 38px ${TEXTO}`,
            letterSpacing: "0.2em",
            color: PALETA.papel,
            marginTop: 8,
          }}
        >
          DESTINO
        </div>
        <div
          style={{
            font: `700 38px ${TEXTO}`,
            letterSpacing: "0.2em",
            color: PALETA.papel,
          }}
        >
          NO MUNDO
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- lista (3 cartões)
/** "Hospedagem cara, pontos turísticos e restaurantes lotados": um cartão por item, cada um cai na sua palavra. */
export const Lista: React.FC<{
  t: number;
  itens: {
    src: string;
    linhas: string[];
    em: string;
    foco?: [number, number];
  }[];
  marcos: Record<string, number>;
}> = ({ t, itens, marcos }) => (
  <div style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
    {itens.map((it, i) => {
      const em = marcos[it.em] ?? 0;
      const e = pouso((t - em + 0.08) / 0.38);
      const vis = t >= em - 0.08;
      const x = 48 + i * 336;
      const giro = [-3, 2, -2][i] * (1 + (1 - clamp((t - em) / 0.38)) * 3);
      const z = lerp(t, em, em + 3, 1.0, 1.08, (p) => p);
      return (
        <div
          key={i}
          style={{
            position: "absolute",
            left: x,
            top: 290,
            width: 312,
            opacity: vis ? 1 : 0,
            translate: `0 ${(1 - e) * -520}px`,
            rotate: `${giro}deg`,
          }}
        >
          <div
            style={{
              width: 312,
              height: 400,
              borderRadius: 16,
              overflow: "hidden",
              border: `5px solid ${PALETA.papel}`,
              boxShadow: "0 30px 60px rgba(0,0,0,0.6)",
              background: PALETA.preto,
            }}
          >
            <Img
              src={staticFile(it.src)}
              style={{
                width: 302,
                height: 390,
                objectFit: "cover",
                objectPosition: `${(it.foco ?? [0.5, 0.5])[0] * 100}% ${(it.foco ?? [0.5, 0.5])[1] * 100}%`,
                scale: String(z),
                filter: "contrast(1.05) saturate(0.95)",
              }}
            />
          </div>
          <div
            style={{
              marginTop: 22,
              textAlign: "center",
              textShadow: SOMBRA_TEXTO,
            }}
          >
            {it.linhas.map((l, k) => (
              <div
                key={k}
                style={{
                  font: `400 ${k === it.linhas.length - 1 ? 58 : 46}px ${TITULO}`,
                  lineHeight: 1.04,
                  color:
                    k === it.linhas.length - 1 ? PALETA.ambar : PALETA.branco,
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

// ---------------------------------------------------------------- três pulos do gato
const TELHADOS =
  "M0 820 L0 750 L80 750 L80 710 L150 670 L220 710 L220 750 L260 750 L260 660 L290 660 L290 700 L380 700 L380 620 L400 620 L400 700 L470 700 L520 650 L570 700 L620 700 L620 760 L660 760 L660 680 L700 640 L760 640 L800 680 L800 740 L840 740 L840 660 L870 660 L870 740 L1080 740 L1080 820";
/** Pousos do gato (o 1º salto parte do 1º telhado) e a Torre ao fundo, tudo em traço. */
const POUSOS: [number, number][] = [
  [150, 666],
  [395, 616],
  [700, 636],
  [930, 736],
];

const GatoSentado: React.FC<{ cor: string }> = ({ cor }) => (
  <g>
    <path
      d="M-30 0 C -34 -30, -26 -58, 0 -62 C 26 -58, 34 -30, 30 0 Z"
      fill={cor}
    />
    <circle cx={0} cy={-74} r={22} fill={cor} />
    <path d="M-20 -86 L-17 -112 L-4 -94 Z" fill={cor} />
    <path d="M20 -86 L17 -112 L4 -94 Z" fill={cor} />
    <path
      d="M26 -6 C 58 -10, 62 -46, 44 -60"
      stroke={cor}
      strokeWidth={9}
      strokeLinecap="round"
      fill="none"
    />
    <circle cx={-8} cy={-76} r={3.2} fill={PALETA.fundo} />
    <circle cx={8} cy={-76} r={3.2} fill={PALETA.fundo} />
  </g>
);

export const Gato: React.FC<{ t: number; marcos: Record<string, number> }> = ({
  t,
  marcos,
}) => {
  const ev = evolvePath(easeInOut(t / 0.7), TELHADOS);
  const s0 = marcos.tres ?? 0.1;
  const DUR = 0.55;
  const PASSO = 0.62;
  // salto k vai de POUSOS[k] a POUSOS[k+1]
  let gx = POUSOS[0][0];
  let gy = POUSOS[0][1];
  let squash = 1;
  for (let k = 0; k < 3; k++) {
    const ini = s0 + k * PASSO;
    const p = clamp((t - ini) / DUR);
    if (t >= ini) {
      const [x0, y0] = POUSOS[k];
      const [x1, y1] = POUSOS[k + 1];
      const pe = easeInOut(p);
      gx = x0 + (x1 - x0) * pe;
      gy = y0 + (y1 - y0) * pe - Math.sin(Math.PI * pe) * 150;
      const d = t - ini - DUR;
      if (d >= 0 && d < 0.12) squash = 0.82 + 0.18 * (d / 0.12);
    }
  }
  const torre =
    "M960 740 L990 480 L1000 360 L1004 280 L1008 360 L1018 480 L1048 740 M972 620 L1036 620 M985 530 L1023 530 M996 420 L1012 420";
  const evT = evolvePath(easeInOut((t - 0.2) / 0.8), torre);
  return (
    <div style={{ position: "absolute", inset: 0, background: PALETA.fundo }}>
      <svg width={1080} height={900} style={{ position: "absolute", inset: 0 }}>
        <path
          d={TELHADOS}
          fill="none"
          stroke={PALETA.papel}
          strokeWidth={5}
          strokeLinejoin="round"
          strokeDasharray={ev.strokeDasharray}
          strokeDashoffset={ev.strokeDashoffset}
        />
        <path
          d={torre}
          fill="none"
          stroke={PALETA.papel}
          strokeOpacity={0.5}
          strokeWidth={4}
          strokeDasharray={evT.strokeDasharray}
          strokeDashoffset={evT.strokeDashoffset}
        />
        {/* rastro pontilhado de cada salto */}
        {[0, 1, 2].map((k) => {
          const ini = s0 + k * PASSO;
          const [x0, y0] = POUSOS[k];
          const [x1, y1] = POUSOS[k + 1];
          const d = `M${x0} ${y0 - 40} Q ${(x0 + x1) / 2} ${Math.min(y0, y1) - 330} ${x1} ${y1 - 40}`;
          const e = evolvePath(easeInOut((t - ini) / DUR), d);
          return (
            <g key={k} opacity={t >= ini ? 1 : 0}>
              <path
                d={d}
                fill="none"
                stroke={PALETA.ambar}
                strokeOpacity={0.55}
                strokeWidth={4}
                strokeDasharray={e.strokeDasharray}
                strokeDashoffset={e.strokeDashoffset}
              />
              <text
                x={x1}
                y={y1 - 150}
                textAnchor="middle"
                fontFamily={TITULO}
                fontSize={74}
                fill={PALETA.ambar}
                opacity={ease((t - ini - DUR) / 0.18)}
              >
                {k + 1}
              </text>
            </g>
          );
        })}
        <g
          transform={`translate(${gx} ${gy}) scale(${1 / squash} ${squash})`}
          opacity={t > 0.15 ? 1 : 0}
        >
          <GatoSentado cor={PALETA.ambar} />
        </g>
      </svg>
      <div
        style={{
          position: "absolute",
          left: 72,
          top: 286,
          display: "flex",
          gap: 26,
          textShadow: SOMBRA_TEXTO,
        }}
      >
        {[
          { txt: "3 PULOS", em: s0 - 0.05, cor: PALETA.branco },
          {
            txt: "DO GATO",
            em: (marcos.gato ?? s0 + 0.6) - 0.05,
            cor: PALETA.ambar,
          },
        ].map((l, i) => {
          const e = ease((t - l.em) / 0.2);
          return (
            <div
              key={i}
              style={{ overflow: "hidden", paddingTop: 40, marginTop: -40 }}
            >
              <div
                style={{
                  font: `400 112px ${TITULO}`,
                  lineHeight: 1,
                  color: l.cor,
                  translate: `0 ${(1 - e) * 110}%`,
                  opacity: e > 0 ? 1 : 0,
                }}
              >
                {l.txt}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- número da dica
/** Selo redondo com o número da dica (1, 2, 3), entra com um "pop" na palavra. */
export const NumeroDica: React.FC<{ t: number; em: number; n: number }> = ({
  t,
  em,
  n,
}) => {
  const p = (t - em) / 0.3;
  if (p < 0) return null;
  const e =
    p < 0.6 ? ease(p / 0.6) * 1.12 : 1.12 - 0.12 * easeInOut((p - 0.6) / 0.4);
  return (
    <div
      style={{
        position: "absolute",
        left: 72,
        top: 290,
        width: 150,
        height: 150,
        borderRadius: 75,
        background: PALETA.ambar,
        boxShadow: "0 16px 40px rgba(0,0,0,0.55)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        font: `400 112px ${TITULO}`,
        color: PALETA.preto,
        scale: String(e),
        paddingTop: 4,
      }}
    >
      {n}
    </div>
  );
};

// ---------------------------------------------------------------- dica 1: calendário
/** "Fique no mínimo quatro dias": 4 folhas de calendário, uma marcada por vez, e "4 DIAS". Some em "encantar". */
export const Calendario: React.FC<{
  t: number;
  marcos: Record<string, number>;
}> = ({ t, marcos }) => {
  const em = marcos.quatro ?? 0.6;
  const sai = marcos.sai ?? 99;
  const vis = ease((t - em + 0.1) / 0.25) * (1 - ease((t - sai) / 0.3));
  if (vis <= 0) return null;
  return (
    <div style={{ position: "absolute", inset: 0, opacity: vis }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.25) 100%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: 72,
          top: 480,
          display: "flex",
          gap: 22,
        }}
      >
        {[0, 1, 2, 3].map((k) => {
          const ek = pouso((t - em - k * 0.1) / 0.3);
          const marca = clamp((t - em - 0.25 - k * 0.12) / 0.15);
          return (
            <div
              key={k}
              style={{
                width: 150,
                height: 170,
                borderRadius: 14,
                background: "#F4F1EA",
                boxShadow: "0 14px 34px rgba(0,0,0,0.5)",
                overflow: "hidden",
                translate: `0 ${(1 - ek) * -80}px`,
                opacity: ek > 0 ? 1 : 0,
                position: "relative",
              }}
            >
              <div style={{ height: 38, background: PALETA.vermelho }} />
              <div
                style={{
                  font: `400 92px ${TITULO}`,
                  color: PALETA.preto,
                  textAlign: "center",
                  lineHeight: "128px",
                }}
              >
                {k + 1}
              </div>
              <svg
                width={150}
                height={170}
                style={{ position: "absolute", left: 0, top: 0 }}
              >
                <path
                  d="M 30 104 L 64 140 L 124 66"
                  fill="none"
                  stroke={PALETA.ambar}
                  strokeWidth={13}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeDasharray={200}
                  strokeDashoffset={200 * (1 - marca)}
                />
              </svg>
            </div>
          );
        })}
      </div>
      <div
        style={{
          position: "absolute",
          left: 72,
          top: 680,
          font: `400 150px ${TITULO}`,
          lineHeight: 1,
          color: PALETA.branco,
          textShadow: SOMBRA_TEXTO,
          opacity: ease((t - (marcos.dias ?? em + 0.3)) / 0.2),
          translate: `0 ${(1 - ease((t - (marcos.dias ?? em + 0.3)) / 0.2)) * 30}px`,
        }}
      >
        4 <span style={{ color: PALETA.ambar }}>DIAS</span>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- dica 3: mapa dos distritos
export type MapaParis = {
  w: number;
  h: number;
  distritos: { n: number; d: string; cx: number; cy: number }[];
};

/** Os 20 distritos se desenham; o 9º enche de âmbar na palavra "nono", com "9º DISTRITO". */
export const Mapa9: React.FC<{
  t: number;
  mapa: MapaParis;
  marcos: Record<string, number>;
}> = ({ t, mapa, marcos }) => {
  const nono = marcos.nono ?? 0.8;
  const enche = easeInOut((t - nono + 0.05) / 0.35);
  const nove = mapa.distritos.find((d) => d.n === 9);
  const zoom = lerp(t, 0, 3.2, 1.0, 1.06, (p) => p);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background: PALETA.fundo,
        overflow: "hidden",
      }}
    >
      <svg
        width={mapa.w}
        height={mapa.h}
        style={{
          position: "absolute",
          inset: 0,
          scale: String(zoom),
          transformOrigin: nove ? `${nove.cx}px ${nove.cy}px` : "50% 50%",
        }}
      >
        {mapa.distritos.map((d, i) => {
          const ev = evolvePath(easeInOut((t - i * 0.02) / 0.7), d.d);
          const e9 = d.n === 9;
          return (
            <path
              key={d.n}
              d={d.d}
              fill={
                e9
                  ? `rgba(224,174,92,${0.92 * enche})`
                  : "rgba(236,229,216,0.04)"
              }
              stroke={e9 && enche > 0 ? PALETA.ambar : PALETA.papel}
              strokeOpacity={e9 && enche > 0 ? 1 : 0.55}
              strokeWidth={e9 && enche > 0 ? 6 : 3}
              strokeLinejoin="round"
              strokeDasharray={ev.strokeDasharray}
              strokeDashoffset={ev.strokeDashoffset}
            />
          );
        })}
        {nove && (
          <text
            x={nove.cx}
            y={nove.cy + 26}
            textAnchor="middle"
            fontFamily={TITULO}
            fontSize={84}
            fill={PALETA.preto}
            opacity={enche}
          >
            9
          </text>
        )}
      </svg>
      <div
        style={{
          position: "absolute",
          right: 72,
          top: 300,
          textAlign: "right",
          textShadow: SOMBRA_TEXTO,
          opacity: ease((t - nono - 0.15) / 0.25),
          translate: `0 ${(1 - ease((t - nono - 0.15) / 0.25)) * 24}px`,
        }}
      >
        <div
          style={{
            font: `400 150px ${TITULO}`,
            lineHeight: 1,
            color: PALETA.ambar,
          }}
        >
          {comOrdinal("9º")}
        </div>
        <div
          style={{
            font: `400 64px ${TITULO}`,
            lineHeight: 1,
            color: PALETA.branco,
          }}
        >
          DISTRITO
        </div>
      </div>
    </div>
  );
};
