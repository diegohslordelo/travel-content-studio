/**
 * Mapa animado do Reel de Bruges: contornos reais (Natural Earth 1:10m, domínio público), projetados em
 * reels/bruges-bate-volta/scripts/mapa.py para uma caixa 1080 × 900. Cores e fontes da linguagem do formato.
 *
 * Modos:
 * - bloqueio: as rotas de Amsterdam, Bruxelas e Paris chegam em Bruges; a cancela bate ("não quer você lá").
 * - multidao: aproxima em Bruges; os pontos (gente) se amontoam na cancela ("todo mundo vai").
 * - saida: a cancela sai e os pontos voltam pelas rotas ("a galera do bate e volta vai embora").
 * - aberto: Bruges acesa, sem cancela, poucos pontos (fundo do CTA).
 */
import React from "react";
import { getLength, getPointAtLength } from "@remotion/paths";
import { PALETA, TEXTO, clamp01, ease, easeBack, easeInOut, lerp } from "./estilo";

export type DadosMapa = {
  paises: Record<string, string>;
  cidades: Record<string, [number, number]>;
};
export type ModoMapa = "bloqueio" | "multidao" | "saida" | "aberto";

type Pt = { x: number; y: number };
const pt = (c: [number, number]): Pt => ({ x: c[0], y: c[1] });

/** Rotas reais de trem até Bruges, simplificadas: Amsterdam–Antuérpia–Gent, Paris–Lille–Kortrijk, Bruxelas–Gent. */
const rotas = (c: DadosMapa["cidades"]) => {
  const B = pt(c.Bruges);
  const G = pt(c.Gent);
  const X = pt(c.Bruxelas);
  const A = pt(c.Amsterdam);
  const P = pt(c.Paris);
  const antuerpia = { x: 927.7, y: 529.6 }; // 4.40 E, 51.22 N
  const lille = { x: 639.2, y: 734.0 }; // 3.06 E, 50.63 N
  const kortrijk = { x: 682.0, y: 665.0 }; // 3.26 E, 50.83 N
  const curva = (pts: Pt[]) => {
    // Catmull-Rom → Bézier: rota suave passando pelas cidades
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[Math.max(0, i - 1)];
      const p1 = pts[i];
      const p2 = pts[i + 1];
      const p3 = pts[Math.min(pts.length - 1, i + 2)];
      const c1 = { x: p1.x + (p2.x - p0.x) / 6, y: p1.y + (p2.y - p0.y) / 6 };
      const c2 = { x: p2.x - (p3.x - p1.x) / 6, y: p2.y - (p3.y - p1.y) / 6 };
      d += ` C ${c1.x} ${c1.y} ${c2.x} ${c2.y} ${p2.x} ${p2.y}`;
    }
    return d;
  };
  return [curva([A, antuerpia, G, B]), curva([P, lille, kortrijk, B]), curva([X, G, B])];
};

const aleatorio = (i: number, k = 0) => {
  const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453;
  return s - Math.floor(s);
};

/** Cancela: placa circular de "proibido entrar" no traço do formato (branco), sem cor nova. */
const Cancela: React.FC<{ x: number; y: number; r: number; escala: number; giro: number; opacidade: number }> = ({ x, y, r, escala, giro, opacidade }) => (
  <g transform={`translate(${x},${y}) rotate(${giro}) scale(${escala})`} opacity={opacidade}>
    <circle r={r * 1.55} fill={PALETA.preto} opacity={0.55} />
    <circle r={r} fill="none" stroke={PALETA.branco} strokeWidth={r * 0.2} />
    <rect x={-r * 0.68} y={-r * 0.13} width={r * 1.36} height={r * 0.26} rx={r * 0.05} fill={PALETA.branco} />
  </g>
);

export const Mapa: React.FC<{ t: number; modo: ModoMapa; dados: DadosMapa; largura: number; altura: number; dur: number }> = ({ t, modo, dados, largura, altura, dur }) => {
  const B = pt(dados.cidades.Bruges);
  const caminhos = React.useMemo(() => rotas(dados.cidades), [dados]);
  const comps = React.useMemo(() => caminhos.map((d) => getLength(d)), [caminhos]);

  // câmera: Bruges vai para (cx, cy) com zoom z
  let cx = B.x;
  let cy = B.y;
  let z = 1;
  let tremor = 0;
  const slam = 0.62; // s: a cancela bate (entre "não" e "quer")
  if (modo === "bloqueio") {
    z = lerp(t, 0, dur, 1.0, 1.08, (x) => x);
    const k = t - slam;
    tremor = k > 0 && k < 0.35 ? 9 * Math.exp(-k * 9) * Math.sin(k * 70) : 0;
  } else if (modo === "multidao") {
    z = lerp(t, 0, dur, 1.15, 2.3, easeInOut);
    cx = lerp(t, 0, dur, B.x, 600, easeInOut);
    cy = lerp(t, 0, dur, B.y, 520, easeInOut);
  } else if (modo === "saida") {
    z = lerp(t, 0, dur, 2.2, 1.35, easeInOut);
    cx = 540;
    cy = lerp(t, 0, dur, 880, 940, easeInOut);
  } else {
    z = 1.5;
    cx = 790;
    cy = 520;
  }

  // traço das rotas
  const desenho = modo === "bloqueio" ? ease(t / 0.75) : 1;
  // cancela
  let escalaC = 1;
  let giroC = 0;
  let opC = 1;
  if (modo === "bloqueio") {
    escalaC = t < slam ? 0 : easeBack((t - slam) / 0.24);
  } else if (modo === "saida") {
    const s = clamp01((t - 0.12) / 0.35);
    escalaC = 1 - 0.4 * ease(s);
    giroC = -90 * ease(s);
    opC = 1 - s;
  } else if (modo === "aberto") {
    opC = 0;
  }
  const raio = 50 / Math.sqrt(z);

  // pontos (gente): seguem as rotas até Bruges; com a cancela, param e se amontoam antes dela
  const n = modo === "multidao" ? Math.round(lerp(t, 0, dur, 70, 260, (x) => x)) : modo === "bloqueio" ? 54 : modo === "saida" ? 160 : 24;
  const pontos: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    const r = i % 3;
    const d = caminhos[r];
    const L = comps[r];
    const vel = 0.32 + 0.22 * aleatorio(i, 1); // fração da rota por segundo
    const fase = aleatorio(i, 2);
    let u: number;
    let jx = 0;
    let jy = 0;
    let op = 1;
    if (modo === "saida") {
      // saem de perto de Bruges e voltam pelas rotas
      u = clamp01(0.97 - (fase * 0.25 + Math.max(0, t - 0.25) * vel * 1.3));
      op = u <= 0.02 ? 0 : 1;
    } else if (modo === "aberto") {
      u = (fase + t * vel * 0.4) % 1;
      op = Math.sin(u * Math.PI);
    } else {
      const tt = modo === "multidao" ? t + 2.45 : t;
      const parada = 0.93 - 0.11 * aleatorio(i, 3); // fila antes da cancela
      const bruto = tt * vel * 1.4 - fase * 1.6 + 0.35; // cada ponto sai da origem num instante diferente
      if (bruto < 0) continue;
      u = Math.min(parada, bruto);
      if (u >= parada - 0.001) {
        const amp = 16 + 46 * aleatorio(i, 4);
        jx = Math.sin(tt * 3 + i) * 2 + (aleatorio(i, 5) - 0.5) * amp;
        jy = Math.cos(tt * 2.6 + i) * 2 + (aleatorio(i, 6) - 0.5) * amp;
      }
      op = clamp01((u * L) / 40) * (desenho >= u ? 1 : 0);
    }
    const p = getPointAtLength(d, clamp01(u) * L) ?? { x: 0, y: 0 };
    pontos.push(<circle key={i} cx={p.x + jx} cy={p.y + jy} r={(modo === "multidao" ? 6 : 4.6) / Math.sqrt(z)} fill={PALETA.ambar} opacity={0.92 * op} />);
  }

  const brilho = modo === "aberto" || modo === "saida" ? 0.55 + 0.25 * Math.sin(t * 4) : 0.18;
  const rotulo = (txt: string, c: Pt, dx: number, dy: number, cor: string = PALETA.papel, tam = 26, peso = 700) => (
    <text x={c.x + dx / z} y={c.y + dy / z} fill={cor} fontFamily={TEXTO} fontWeight={peso} fontSize={tam / z} letterSpacing={2 / z} style={{ paintOrder: "stroke" }} stroke={PALETA.preto} strokeWidth={6 / z}>
      {txt}
    </text>
  );

  return (
    <svg width={largura} height={altura} viewBox={`0 0 ${largura} ${altura}`} style={{ position: "absolute", left: 0, top: 0, background: PALETA.preto }}>
      <defs>
        <radialGradient id="brilho-bruges">
          <stop offset="0%" stopColor={PALETA.ambar} stopOpacity={0.9} />
          <stop offset="100%" stopColor={PALETA.ambar} stopOpacity={0} />
        </radialGradient>
      </defs>
      <g transform={`translate(${cx + tremor},${cy}) scale(${z}) translate(${-B.x},${-B.y})`}>
        {Object.entries(dados.paises).map(([iso, d]) => (
          <path key={iso} d={d} fill={iso === "BEL" ? PALETA.ambar : PALETA.papel} fillOpacity={iso === "BEL" ? 0.16 : 0.08} stroke={PALETA.papel} strokeOpacity={0.3} strokeWidth={1.4} vectorEffect="non-scaling-stroke" />
        ))}
        {caminhos.map((d, i) => (
          <path key={i} d={d} fill="none" stroke={PALETA.ambar} strokeOpacity={0.75} strokeWidth={4} strokeLinecap="round" vectorEffect="non-scaling-stroke" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - desenho} />
        ))}
        {pontos}
        <circle cx={B.x} cy={B.y} r={70 / Math.sqrt(z)} fill="url(#brilho-bruges)" opacity={brilho} />
        {(["Bruxelas", "Amsterdam", "Gent"] as const).map((k) => (
          <circle key={k} cx={dados.cidades[k][0]} cy={dados.cidades[k][1]} r={7 / z} fill={PALETA.papel} />
        ))}
        {rotulo("BRUXELAS", pt(dados.cidades.Bruxelas), 14, 34)}
        {rotulo("AMSTERDAM", pt(dados.cidades.Amsterdam), -190, 50)}
        {modo !== "aberto" && rotulo("PARIS ↓", { x: 500, y: 860 }, 0, 0)}
        <circle cx={B.x} cy={B.y} r={10 / z} fill={PALETA.ambar} stroke={PALETA.preto} strokeWidth={3 / z} />
        {rotulo("BRUGES", B, -70, modo === "aberto" ? 60 : 108, PALETA.ambar, 38, 800)}
        <Cancela x={B.x} y={B.y} r={raio} escala={escalaC} giro={giroC} opacidade={opC} />
      </g>
    </svg>
  );
};
