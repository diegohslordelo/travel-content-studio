/**
 * Viagem Brasil → destino (Barcelona, Madrid…) num globo em duas paletas:
 * - "cacau" (REV1 de Barcelona): o mergulho no chocolate do gancho "vira" o oceano;
 * - "colorido" (Madrid): cores naturais e vivas — oceano azul, terras verdes, Brasil em verde e amarelo,
 *   Espanha em vermelho e amarelo, céu estrelado. O chocolate do mergulho se dissolve no céu.
 *
 * Projeção ortográfica feita aqui (sem d3): o centro da câmera acompanha o avião pelo arco de círculo
 * máximo, e no fim a câmera mergulha no destino. Contornos: Natural Earth 1:50m (domínio público),
 * em reels/<reel>/revN/geo/mundo.json. Só aparecem os nomes BRASIL e o do destino; nenhum
 * número (duração, distância) é mostrado.
 */
import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile } from "remotion";
import { kf, useMs } from "../ds/tempo";
import { C, CURVA, F } from "./tema";

type Pais = { iso: string; aneis: [number, number][][] };
type LonLat = [number, number];

const RAD = Math.PI / 180;
/** Ponto de partida: interior do Nordeste, só para o arco sair de dentro do Brasil (sem nome de cidade). */
const ORIGEM: LonLat = [-44.5, -12.5];
/** Destino padrão (REV1 de Barcelona). */
const BARCELONA: Destino = { nome: "BARCELONA", lon: 2.17, lat: 41.39 };

export type Destino = { nome: string; lon: number; lat: number };

const paraVetor = ([lon, lat]: LonLat): [number, number, number] => [
  Math.cos(lat * RAD) * Math.cos(lon * RAD),
  Math.cos(lat * RAD) * Math.sin(lon * RAD),
  Math.sin(lat * RAD),
];
const paraLonLat = ([x, y, z]: [number, number, number]): LonLat => [Math.atan2(y, x) / RAD, Math.asin(Math.max(-1, Math.min(1, z))) / RAD];

/** Interpolação esférica (arco de círculo máximo) entre dois pontos. */
const slerp = (a: LonLat, b: LonLat, p: number): LonLat => {
  const va = paraVetor(a);
  const vb = paraVetor(b);
  const dot = Math.max(-1, Math.min(1, va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2]));
  const om = Math.acos(dot);
  if (om < 1e-6) return a;
  const s = Math.sin(om);
  const k1 = Math.sin((1 - p) * om) / s;
  const k2 = Math.sin(p * om) / s;
  return paraLonLat([va[0] * k1 + vb[0] * k2, va[1] * k1 + vb[1] * k2, va[2] * k1 + vb[2] * k2]);
};

/** Projeção ortográfica com centro (lon0, lat0). Retorna [x, y, visível]; o lado de trás é empurrado para o horizonte. */
const projetor = (centro: LonLat, R: number, cx: number, cy: number) => {
  const l0 = centro[0] * RAD;
  const f0 = centro[1] * RAD;
  const sf0 = Math.sin(f0);
  const cf0 = Math.cos(f0);
  return ([lon, lat]: LonLat): [number, number, boolean] => {
    const l = lon * RAD - l0;
    const f = lat * RAD;
    const cf = Math.cos(f);
    const sf = Math.sin(f);
    const cl = Math.cos(l);
    const cosc = sf0 * sf + cf0 * cf * cl;
    let x = cf * Math.sin(l);
    let y = cf0 * sf - sf0 * cf * cl;
    if (cosc < 0) {
      const n = Math.hypot(x, y) || 1;
      x /= n;
      y /= n;
    }
    return [cx + x * R, cy - y * R, cosc >= 0];
  };
};

const useMundo = (): Pais[] | null => {
  const [dados, setDados] = useState<Pais[] | null>(null);
  const [h] = useState(() => delayRender("mundo.json"));
  useEffect(() => {
    fetch(staticFile("mundo.json"))
      .then((r) => r.json())
      .then((j: { paises: Pais[] }) => {
        setDados(j.paises);
        continueRender(h);
      });
  }, [h]);
  return dados;
};

/** Avião visto de cima, apontando para cima (0°). */
const Aviao: React.FC<{ x: number; y: number; ang: number; escala: number }> = ({ x, y, ang, escala }) => (
  <g transform={`translate(${x} ${y}) rotate(${ang}) scale(${escala})`}>
    <ellipse cx={6} cy={14} rx={30} ry={34} fill="rgba(0,0,0,.35)" filter="url(#sombraAviao)" />
    <path
      d="M0,-46 C5,-46 7,-38 7,-30 L7,-10 L44,8 L44,17 L7,9 L6,30 L17,39 L17,46 L0,41 L-17,46 L-17,39 L-6,30 L-7,9 L-44,17 L-44,8 L-7,-10 L-7,-30 C-7,-38 -5,-46 0,-46 Z"
      fill={C.creme}
      stroke={C.cacau}
      strokeWidth={2}
    />
  </g>
);

type Paleta = {
  fundo: string;
  estrelas: boolean;
  oceano: [string, string, string];
  brilho: string;
  atmosfera: string;
  grade: string;
  gradeOp: number;
  terra: string;
  terraOp: number;
  contorno: string;
  contornoOp: number;
  brasil: string;
  brasilBorda: string;
  destino: string;
  destinoBorda: string;
  rota: string;
  rotaBrilho: string;
  ponto: string;
  pontoBorda: string;
  rotuloOrigem: { fundo: string; borda: string; texto: string };
  rotuloDestino: { fundo: string; borda: string; texto: string };
};

const PALETAS: Record<"cacau" | "colorido", Paleta> = {
  cacau: {
    fundo: `radial-gradient(120% 80% at 50% 52%, ${C.cacau2} 0%, ${C.cacau} 70%)`,
    estrelas: false,
    oceano: [C.chocolate, C.cacau3, C.cacau2],
    brilho: "rgba(255,236,210,.20)",
    atmosfera: "rgba(233,166,58,.28)",
    grade: C.creme,
    gradeOp: 0.07,
    terra: C.creme2,
    terraOp: 0.36,
    contorno: C.cacau,
    contornoOp: 0.55,
    brasil: C.dourado,
    brasilBorda: C.cacau,
    destino: C.dourado,
    destinoBorda: C.cacau,
    rota: C.douradoClaro,
    rotaBrilho: C.dourado,
    ponto: C.douradoClaro,
    pontoBorda: C.cacau,
    rotuloOrigem: { fundo: "rgba(30,18,12,.55)", borda: C.dourado, texto: C.creme },
    rotuloDestino: { fundo: "rgba(30,18,12,.55)", borda: C.dourado, texto: C.creme },
  },
  colorido: {
    fundo: "radial-gradient(120% 85% at 50% 50%, #17336E 0%, #0B1A3D 55%, #050B1E 100%)",
    estrelas: true,
    oceano: ["#3C9BEA", "#1F64C4", "#103E8A"],
    brilho: "rgba(255,255,255,.30)",
    atmosfera: "rgba(120,205,255,.55)",
    grade: "#FFFFFF",
    gradeOp: 0.1,
    terra: "#7CC46B",
    terraOp: 1,
    contorno: "#2F6B3A",
    contornoOp: 0.7,
    brasil: "#13A24F",
    brasilBorda: "#FFD43B",
    destino: "#E5322D",
    destinoBorda: "#FFC72C",
    rota: "#FFD43B",
    rotaBrilho: "#FFB000",
    ponto: "#FFFFFF",
    pontoBorda: "#E5322D",
    rotuloOrigem: { fundo: "#13A24F", borda: "#FFD43B", texto: "#FFFFFF" },
    rotuloDestino: { fundo: "#E5322D", borda: "#FFC72C", texto: "#FFFFFF" },
  },
};

/** Estrelas fixas (posições pseudoaleatórias determinísticas), com cintilação leve. */
const Estrelas: React.FC<{ t: number }> = ({ t }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
    {Array.from({ length: 140 }, (_, i) => {
      const a = Math.sin(i * 91.7) * 43758.5453;
      const b = Math.sin(i * 47.3 + 3) * 24634.6345;
      const x = (a - Math.floor(a)) * 1080;
      const y = (b - Math.floor(b)) * 1920;
      const r = 1 + ((i * 7) % 3) * 0.7;
      const pisca = 0.45 + 0.55 * Math.abs(Math.sin(t / 600 + i));
      return <circle key={i} cx={x} cy={y} r={r} fill="#FFFFFF" opacity={0.55 * pisca} />;
    })}
  </svg>
);

export const DUR_ROTA = { surge: 600, voo: [650, 2850] as [number, number], mergulho: [2950, 4230] as [number, number] };

export const Globo: React.FC<{ paleta?: "cacau" | "colorido"; destino?: Destino; corEntrada?: string }> = ({
  paleta = "cacau",
  destino = BARCELONA,
  corEntrada,
}) => {
  const t = useMs();
  const mundo = useMundo();
  const P = PALETAS[paleta];
  const DESTINO: LonLat = [destino.lon, destino.lat];

  // ---- câmera: surge sobre o Brasil, acompanha o avião, mergulha no destino
  const pVoo = kf(t, DUR_ROTA.voo, [0, 1], CURVA.suave);
  // a câmera vai atrás do avião com atraso: ele atravessa a tela em vez de ficar parado no centro
  const pCam = kf(t, [DUR_ROTA.voo[0] + 250, DUR_ROTA.mergulho[0] + 100], [0, 1], CURVA.suave);
  // mergulho no destino: crescimento contínuo (potência), sem esperar o fim para acelerar
  const pMerg = Math.pow(kf(t, DUR_ROTA.mergulho, [0, 1]), 2.2);
  const pontoCentro = slerp(ORIGEM, DESTINO, 0.1 + 0.9 * pCam);
  const centro: LonLat = [pontoCentro[0], pontoCentro[1] - 8 * (1 - pCam)];
  const surge = kf(t, [0, DUR_ROTA.surge], [0, 1], CURVA.sai);
  const R = (380 + 150 * surge + 80 * pCam) * Math.pow(34, pMerg);
  const cx = 540;
  const cy = 1000 - 40 * pCam;
  const proj = projetor(centro, R, cx, cy);

  if (!mundo) return null;

  const corPais = (iso: string): { fill: string; op: number; borda?: string } => {
    if (iso === "BRA") return { fill: P.brasil, op: kf(t, [150, 650], [paleta === "colorido" ? 0.6 : 0.25, 1], CURVA.sai) * (1 - 0.35 * pVoo * (paleta === "cacau" ? 1 : 0)), borda: P.brasilBorda };
    if (iso === "ESP") return { fill: P.destino, op: kf(t, [2700, 3200], [paleta === "colorido" ? 0 : 0.25, 1], CURVA.sai), borda: P.destinoBorda };
    return { fill: P.terra, op: P.terraOp };
  };

  const paths = mundo.map(({ iso, aneis }) => {
    let d = "";
    for (const anel of aneis) {
      let algumVisivel = false;
      const pts = anel.map((ll) => {
        const [x, y, v] = proj(ll);
        if (v) algumVisivel = true;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      });
      if (algumVisivel) d += `M${pts.join("L")}Z`;
    }
    if (!d) return null;
    const cor = corPais(iso);
    const base = <path key={iso} d={d} fill={P.terra} fillOpacity={P.terraOp} stroke={P.contorno} strokeOpacity={P.contornoOp} strokeWidth={1.2} />;
    if (paleta === "colorido" && cor.borda) {
      // destaque por cima da terra comum: cor + borda acesa
      return (
        <g key={iso}>
          {base}
          <path d={d} fill={cor.fill} fillOpacity={cor.op} stroke={cor.borda} strokeOpacity={cor.op} strokeWidth={4} strokeLinejoin="round" />
        </g>
      );
    }
    return <path key={iso} d={d} fill={cor.fill} fillOpacity={cor.op} stroke={P.contorno} strokeOpacity={P.contornoOp} strokeWidth={1.2} />;
  });

  // graticulado leve (15°)
  const grade: string[] = [];
  for (let lon = -180; lon < 180; lon += 15) {
    const pts: string[] = [];
    let ok = false;
    for (let lat = -80; lat <= 80; lat += 4) {
      const [x, y, v] = proj([lon, lat]);
      if (v) ok = true;
      pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
    }
    if (ok) grade.push(`M${pts.join("L")}`);
  }
  for (let lat = -60; lat <= 75; lat += 15) {
    const pts: string[] = [];
    for (let lon = -180; lon <= 180; lon += 4) {
      const [x, y, v] = proj([lon, lat]);
      if (v) pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
      else if (pts.length) break;
    }
    if (pts.length > 1) grade.push(`M${pts.join("L")}`);
  }

  // rota até o ponto atual
  const N = 90;
  const rota: string[] = [];
  for (let i = 0; i <= N * pVoo; i++) {
    const [x, y] = proj(slerp(ORIGEM, DESTINO, i / N));
    rota.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  }
  const posAviao = proj(slerp(ORIGEM, DESTINO, pVoo));
  const frente = proj(slerp(ORIGEM, DESTINO, Math.min(1, pVoo + 0.01)));
  const tras = proj(slerp(ORIGEM, DESTINO, Math.max(0, pVoo - 0.01)));
  const ang = (Math.atan2(frente[0] - tras[0], -(frente[1] - tras[1])) * 180) / Math.PI;
  // o avião sobe da pista (escala) e pousa no destino
  const escAviao = 1.35 * kf(t, [DUR_ROTA.voo[0] - 150, DUR_ROTA.voo[0] + 250], [0, 1], CURVA.mola) * kf(t, [DUR_ROTA.voo[1] - 250, DUR_ROTA.voo[1] + 100], [1, 0], CURVA.entra);

  const [ox, oy] = proj(ORIGEM);
  const [bx, by] = proj(DESTINO);
  const rotuloBr = kf(t, [300, 700], [0, 1], CURVA.sai) * kf(t, [1600, 2000], [1, 0]);
  const rotuloDest = kf(t, [2850, 3250], [0, 1], CURVA.sai) * kf(t, DUR_ROTA.mergulho, [1, 0], CURVA.entra);
  const pulso = (t - 2900) / 900;
  const entrada = corEntrada ? kf(t, [0, 380], [1, 0], CURVA.suave) : 0;

  return (
    <AbsoluteFill style={{ background: P.fundo }}>
      {P.estrelas && <Estrelas t={t} />}
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: surge }}>
        <defs>
          <radialGradient id="oceano" cx="42%" cy="38%" r="70%">
            <stop offset="0%" stopColor={P.oceano[0]} />
            <stop offset="65%" stopColor={P.oceano[1]} />
            <stop offset="100%" stopColor={P.oceano[2]} />
          </radialGradient>
          <radialGradient id="brilho" cx="35%" cy="28%" r="55%">
            <stop offset="0%" stopColor={P.brilho} />
            <stop offset="100%" stopColor="rgba(255,255,255,0)" />
          </radialGradient>
          <radialGradient id="atmosfera" cx="50%" cy="50%" r="50%">
            <stop offset="88%" stopColor="rgba(255,255,255,0)" />
            <stop offset="96%" stopColor={P.atmosfera} />
            <stop offset="100%" stopColor="rgba(255,255,255,0)" />
          </radialGradient>
          <clipPath id="esfera">
            <circle cx={cx} cy={cy} r={R} />
          </clipPath>
          <filter id="brilhoRota" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" />
          </filter>
          <filter id="sombraAviao">
            <feGaussianBlur stdDeviation="6" />
          </filter>
        </defs>
        <circle cx={cx} cy={cy} r={R * 1.09} fill="url(#atmosfera)" />
        <circle cx={cx} cy={cy} r={R} fill="url(#oceano)" />
        <g clipPath="url(#esfera)">
          <path d={grade.join("")} fill="none" stroke={P.grade} strokeOpacity={P.gradeOp} strokeWidth={1.2} />
          {paths}
          {rota.length > 1 && (
            <>
              <polyline points={rota.join(" ")} fill="none" stroke={P.rotaBrilho} strokeWidth={14} strokeOpacity={0.45} filter="url(#brilhoRota)" />
              <polyline points={rota.join(" ")} fill="none" stroke={P.rota} strokeWidth={6} strokeLinecap="round" strokeDasharray="2 16" />
            </>
          )}
          <circle cx={ox} cy={oy} r={11} fill={P.ponto} stroke={P.brasilBorda === C.cacau ? C.cacau : P.brasil} strokeWidth={3} opacity={kf(t, [200, 500], [0, 1])} />
          {t > 2850 && (
            <>
              <circle cx={bx} cy={by} r={14 + 70 * Math.max(0, Math.min(1, pulso))} fill="none" stroke={P.rota} strokeWidth={4} opacity={Math.max(0, 1 - pulso)} />
              <circle cx={bx} cy={by} r={13} fill={P.ponto} stroke={P.pontoBorda} strokeWidth={3} />
            </>
          )}
          <circle cx={cx} cy={cy} r={R} fill="url(#brilho)" />
        </g>
        {escAviao > 0.01 && <Aviao x={posAviao[0]} y={posAviao[1]} ang={ang} escala={escAviao} />}
      </svg>
      <RotuloMapa x={ox - 60} y={oy + 60} texto="BRASIL" opacidade={rotuloBr} cores={P.rotuloOrigem} />
      <RotuloMapa x={bx} y={by - 120} texto={destino.nome} opacidade={rotuloDest} cores={P.rotuloDestino} />
      {entrada > 0 && <AbsoluteFill style={{ background: corEntrada, opacity: entrada }} />}
    </AbsoluteFill>
  );
};

const RotuloMapa: React.FC<{ x: number; y: number; texto: string; opacidade: number; cores: Paleta["rotuloOrigem"] }> = ({ x, y, texto, opacidade, cores }) =>
  opacidade <= 0.001 ? null : (
    <div
      style={{
        position: "absolute",
        left: 0,
        width: 1080,
        top: y,
        display: "flex",
        justifyContent: "center",
        translate: `${x - 540}px ${(1 - opacidade) * 18}px`,
        opacity: opacidade,
      }}
    >
      <div
        style={{
          fontFamily: F.cartaz,
          fontSize: 84,
          letterSpacing: "0.04em",
          color: cores.texto,
          padding: "6px 26px 10px",
          background: cores.fundo,
          borderRadius: 14,
          border: `3px solid ${cores.borda}`,
          lineHeight: 1,
          boxShadow: "0 8px 24px rgba(0,0,0,.35)",
        }}
      >
        {texto}
      </div>
    </div>
  );
