/**
 * Mapa da Europa com destaque de países e câmera animada (Reel "Greves na Europa").
 * Geometria: Natural Earth 1:50m (domínio público), projetada em Mercator por reels/greves-europa/rev1/mapa_europa.py.
 * Todas as datas do vídeo são nacionais, então o destaque pinta o país inteiro (sem sugerir alcance maior ou menor).
 */
import React, { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";
import { EASE } from "../ds/tokens";
import { ED, FONTE_ED, prog, useSeg } from "./tema";

type Pais = { id: string | null; nome: string; codigo: string | null; d: string };
type DadosMapa = { largura: number; altura: number; pontos: Record<string, [number, number]>; paises: Pais[] };
export type Camera = { t: number; alvo: string; zoom: number; tela: [number, number] };

const useMapa = (arquivo: string): DadosMapa | null => {
  const [dados, setDados] = useState<DadosMapa | null>(null);
  const [h] = useState(() => delayRender("mapa"));
  useEffect(() => {
    fetch(staticFile(arquivo))
      .then((r) => r.json())
      .then((j: DadosMapa) => {
        setDados(j);
        continueRender(h);
      });
  }, [arquivo, h]);
  return dados;
};

/** Interpola a câmera entre os pontos-chave com ease-cinema (lento nas pontas). */
const camera = (t: number, cams: Camera[], pontos: DadosMapa["pontos"]) => {
  let i = 0;
  while (i < cams.length - 1 && t >= cams[i + 1].t) i++;
  const a = cams[i];
  const b = cams[Math.min(i + 1, cams.length - 1)];
  const p = a === b ? 0 : prog(t, a.t, b.t, EASE.cinema);
  const mix = (u: number, v: number) => u + (v - u) * p;
  const pa = pontos[a.alvo];
  const pb = pontos[b.alvo];
  return { cx: mix(pa[0], pb[0]), cy: mix(pa[1], pb[1]), zoom: mix(a.zoom, b.zoom), sx: mix(a.tela[0], b.tela[0]), sy: mix(a.tela[1], b.tela[1]) };
};

export const MapaEuropa: React.FC<{
  ini: number;
  fim: number;
  cameras: Camera[];
  destaques: { pais: string; em: number }[];
  rotulos?: { pais: string; texto: string; ponto: string; em: number }[];
  escurecer?: { ini: number; fim: number; valor: number }[];
}> = ({ ini, fim, cameras, destaques, rotulos = [], escurecer = [] }) => {
  const t = useSeg();
  const dados = useMapa("mapa_europa.json");
  if (!dados || t < ini - 0.4 || t > fim + 0.6) return null;
  const { cx, cy, zoom, sx, sy } = camera(t, cameras, dados.pontos);
  // escala base: largura do plano (4000 px) → 1080 px mostra ~1/3,7 do plano; zoom multiplica
  const base = 1080 / 1500;
  const k = base * zoom;
  const tx = sx - cx * k;
  const ty = sy - cy * k;
  const esc = escurecer.reduce((m, e) => Math.max(m, Math.min(prog(t, e.ini, e.ini + 0.3), 1 - prog(t, e.fim, e.fim + 0.3)) * e.valor), 0);
  return (
    <div style={{ position: "absolute", inset: 0, background: `radial-gradient(ellipse at 55% 45%, #121A2A 0%, ${ED.mar} 70%)`, overflow: "hidden" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <filter id="brilhoPais" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation={10 / k} result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <pattern id="gradeMapa" width={60} height={60} patternUnits="userSpaceOnUse">
            <path d="M60 0H0V60" fill="none" stroke="rgba(255,255,255,0.035)" strokeWidth={1} />
          </pattern>
        </defs>
        <rect width={1080} height={1920} fill="url(#gradeMapa)" />
        <g transform={`translate(${tx} ${ty}) scale(${k})`}>
          {dados.paises.map((p, i) => {
            const dest = destaques.find((x) => x.pais === p.codigo);
            const a = dest ? prog(t, dest.em, dest.em + 0.45, EASE.out) : 0;
            return (
              <path
                key={i}
                d={p.d}
                fill={a > 0 ? mixCor(ED.terra, ED.alerta, a * 0.85) : ED.terra}
                stroke={a > 0 ? mixCor(ED.terraBorda, "#FFB3AA", a) : ED.terraBorda}
                strokeWidth={(a > 0 ? 2.4 : 1.3) / k}
                strokeLinejoin="round"
                filter={a > 0.05 ? "url(#brilhoPais)" : undefined}
              />
            );
          })}
        </g>
      </svg>
      {rotulos.map((r) => {
        const pt = dados.pontos[r.ponto];
        const a = prog(t, r.em + 0.15, r.em + 0.45, EASE.out);
        if (a <= 0) return null;
        return (
          <div
            key={r.pais}
            style={{
              position: "absolute",
              left: tx + pt[0] * k,
              top: ty + pt[1] * k,
              translate: "-50% -50%",
              fontFamily: FONTE_ED.mono,
              fontSize: 26,
              letterSpacing: "0.16em",
              color: ED.branco,
              textShadow: "0 2px 10px rgba(0,0,0,.8)",
              opacity: a,
            }}
          >
            {r.texto}
          </div>
        );
      })}
      <div style={{ position: "absolute", inset: 0, background: ED.tinta, opacity: esc }} />
      <div style={{ position: "absolute", right: 140, bottom: 470, fontFamily: FONTE_ED.mono, fontSize: 16, color: "rgba(167,176,191,.6)" }}>Natural Earth</div>
    </div>
  );
};

const hex = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
const mixCor = (a: string, b: string, p: number): string => {
  const x = hex(a);
  const y = hex(b);
  return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * p)).join(",")})`;
};
