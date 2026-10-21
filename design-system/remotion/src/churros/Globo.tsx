/**
 * Viagem Brasil → Barcelona num globo cor de cacau (o mergulho no chocolate do gancho "vira" o oceano).
 *
 * Projeção ortográfica feita aqui (sem d3): o centro da câmera acompanha o avião pelo arco de círculo
 * máximo, e no fim a câmera mergulha em Barcelona. Contornos: Natural Earth 1:50m (domínio público),
 * em reels/churros-barcelona/rev1/geo/mundo.json. Só aparecem os nomes BRASIL e BARCELONA; nenhum
 * número (duração, distância) é mostrado.
 */
import React, { useEffect, useMemo, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile } from "remotion";
import { kf, useMs } from "../ds/tempo";
import { C, CURVA, F } from "./tema";

type Pais = { iso: string; aneis: [number, number][][] };
type LonLat = [number, number];

const RAD = Math.PI / 180;
/** Ponto de partida: interior do Nordeste, só para o arco sair de dentro do Brasil (sem nome de cidade). */
const ORIGEM: LonLat = [-44.5, -12.5];
/** Barcelona (Xurreria Trebol fica a ~3 km daqui; no globo é o mesmo ponto). */
const DESTINO: LonLat = [2.17, 41.39];

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

export const DUR_ROTA = { surge: 600, voo: [650, 2850] as [number, number], mergulho: [2950, 4230] as [number, number] };

export const Globo: React.FC = () => {
  const t = useMs();
  const mundo = useMundo();

  // ---- câmera: surge sobre o Brasil, acompanha o avião, mergulha em Barcelona
  const pVoo = kf(t, DUR_ROTA.voo, [0, 1], CURVA.suave);
  // a câmera vai atrás do avião com atraso: ele atravessa a tela em vez de ficar parado no centro
  const pCam = kf(t, [DUR_ROTA.voo[0] + 250, DUR_ROTA.mergulho[0] + 100], [0, 1], CURVA.suave);
  // mergulho em Barcelona: crescimento contínuo (potência), sem esperar o fim para acelerar
  const pMerg = Math.pow(kf(t, DUR_ROTA.mergulho, [0, 1]), 2.2);
  const pontoCentro = slerp(ORIGEM, DESTINO, 0.1 + 0.9 * pCam);
  const centro: LonLat = [pontoCentro[0], pontoCentro[1] - 8 * (1 - pCam)];
  const surge = kf(t, [0, DUR_ROTA.surge], [0, 1], CURVA.sai);
  const R = (380 + 150 * surge + 80 * pCam) * Math.pow(34, pMerg);
  const cx = 540;
  const cy = 1000 - 40 * pCam;
  const proj = projetor(centro, R, cx, cy);

  const caminhos = useMemo(() => {
    if (!mundo) return [];
    return mundo.map((p) => ({ iso: p.iso, aneis: p.aneis }));
  }, [mundo]);

  if (!mundo) return null;

  const corPais = (iso: string): { fill: string; op: number } => {
    if (iso === "BRA") return { fill: C.dourado, op: kf(t, [150, 650], [0.25, 1], CURVA.sai) * (1 - 0.35 * pVoo) };
    if (iso === "ESP") return { fill: C.dourado, op: kf(t, [2700, 3200], [0.25, 1], CURVA.sai) };
    return { fill: C.creme2, op: 0.36 };
  };

  const paths = caminhos.map(({ iso, aneis }) => {
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
    const cor = corPais(iso);
    return d ? <path key={iso} d={d} fill={cor.fill} fillOpacity={cor.op} stroke={C.cacau} strokeOpacity={0.55} strokeWidth={1.2} /> : null;
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
  const rotuloBcn = kf(t, [2850, 3250], [0, 1], CURVA.sai) * kf(t, DUR_ROTA.mergulho, [1, 0], CURVA.entra);
  const pulso = (t - 2900) / 900;

  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 80% at 50% 52%, ${C.cacau2} 0%, ${C.cacau} 70%)` }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: surge }}>
        <defs>
          <radialGradient id="oceano" cx="42%" cy="38%" r="70%">
            <stop offset="0%" stopColor={C.chocolate} />
            <stop offset="65%" stopColor={C.cacau3} />
            <stop offset="100%" stopColor={C.cacau2} />
          </radialGradient>
          <radialGradient id="brilho" cx="35%" cy="28%" r="55%">
            <stop offset="0%" stopColor="rgba(255,236,210,.20)" />
            <stop offset="100%" stopColor="rgba(255,236,210,0)" />
          </radialGradient>
          <radialGradient id="atmosfera" cx="50%" cy="50%" r="50%">
            <stop offset="88%" stopColor="rgba(233,166,58,0)" />
            <stop offset="96%" stopColor="rgba(233,166,58,.28)" />
            <stop offset="100%" stopColor="rgba(233,166,58,0)" />
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
          <path d={grade.join("")} fill="none" stroke={C.creme} strokeOpacity={0.07} strokeWidth={1.2} />
          {paths}
          {rota.length > 1 && (
            <>
              <polyline points={rota.join(" ")} fill="none" stroke={C.dourado} strokeWidth={14} strokeOpacity={0.45} filter="url(#brilhoRota)" />
              <polyline points={rota.join(" ")} fill="none" stroke={C.douradoClaro} strokeWidth={6} strokeLinecap="round" strokeDasharray="2 16" />
            </>
          )}
          <circle cx={ox} cy={oy} r={11} fill={C.creme} stroke={C.cacau} strokeWidth={3} opacity={kf(t, [200, 500], [0, 1])} />
          {t > 2850 && (
            <>
              <circle cx={bx} cy={by} r={14 + 70 * Math.max(0, Math.min(1, pulso))} fill="none" stroke={C.douradoClaro} strokeWidth={4} opacity={Math.max(0, 1 - pulso)} />
              <circle cx={bx} cy={by} r={13} fill={C.douradoClaro} stroke={C.cacau} strokeWidth={3} />
            </>
          )}
          <circle cx={cx} cy={cy} r={R} fill="url(#brilho)" />
        </g>
        {escAviao > 0.01 && <Aviao x={posAviao[0]} y={posAviao[1]} ang={ang} escala={escAviao} />}
      </svg>
      <RotuloMapa x={ox - 60} y={oy + 60} texto="BRASIL" opacidade={rotuloBr} />
      <RotuloMapa x={bx} y={by - 120} texto="BARCELONA" opacidade={rotuloBcn} />
    </AbsoluteFill>
  );
};

const RotuloMapa: React.FC<{ x: number; y: number; texto: string; opacidade: number }> = ({ x, y, texto, opacidade }) =>
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
          color: C.creme,
          padding: "6px 26px 10px",
          background: "rgba(30,18,12,.55)",
          borderRadius: 14,
          border: `2px solid ${C.dourado}`,
          lineHeight: 1,
        }}
      >
        {texto}
      </div>
    </div>
  );
