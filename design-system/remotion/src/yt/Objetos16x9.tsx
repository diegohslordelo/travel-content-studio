/**
 * Objetos do vídeo longo do YouTube (16:9, 1920 × 1080). Decisões do Diego de 16/10/2026 em
 * `docs/VIDEO_LONGO_YOUTUBE.md`. Cores, fontes, sombras, raios, curvas e durações vêm dos tokens;
 * as posições vêm da grade 16:9 do DS V2 (1.3): margem de título 96, lower third com base em y 960.
 */
import React, { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";
import { Fibra } from "../ds/material";
import { GlifoInstagram, Seta } from "../ds/icones";
import { Som } from "../ds/Som";
import { kf, useMs } from "../ds/tempo";
import { COR, DUR, EASE, FONTE, RAIO, SOM, SOMBRA, TIPO, YT, rgba } from "../ds/tokens";

/** Base do lower third (DS V2, 1.3). */
export const LOWER_BASE = 960;

/** Entrada curta (Chegada de 320 ms, DS 5.4) e saída de 240 ms pela direita. */
const useEntradaSaida = (ini: number, fim: number) => {
  const t = useMs();
  const te = t - ini;
  const ts = t - fim;
  const visivel = te >= 0 && ts < DUR.base;
  const x = kf(te, [0, 220, 320], [-720, 12, 0], [EASE.out, EASE.out]) + kf(ts, [0, DUR.base], [0, 1150], EASE.exit);
  const opac = kf(te, [0, 120], [0, 1]) * kf(ts, [80, DUR.base], [1, 0]);
  return { visivel, x, opac, te };
};

/**
 * Etiqueta de lugar (lower third, DS 5.4): placa de direção pequena com o lugar (H3) e, em Plex Mono,
 * bairro e hora da visita (decisão de 16/10/2026: hora no lugar das coordenadas). Sem som.
 */
export const EtiquetaLugar: React.FC<{ lugar: string; detalhe: string; ini: number; fim: number }> = ({ lugar, detalhe, ini, fim }) => {
  const { visivel, x, opac } = useEntradaSaida(ini, fim);
  if (!visivel) return null;
  const H = 128;
  return (
    <div style={{ position: "absolute", left: YT.margemTitulo, top: LOWER_BASE - H, display: "flex", translate: `${x}px 0`, opacity: opac, filter: "drop-shadow(0 10px 18px rgba(0,0,0,.35))" }}>
      <div
        style={{
          position: "relative",
          height: H,
          boxSizing: "border-box",
          padding: "0 30px 0 36px",
          background: COR.amarelo,
          borderRadius: `${RAIO.placa}px 0 0 ${RAIO.placa}px`,
          boxShadow: SOMBRA.relevo,
          color: COR.grafite,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 10,
          overflow: "hidden",
        }}
      >
        <Fibra opacidade={0.05} semente={7} />
        <div style={{ fontFamily: FONTE.display, fontWeight: TIPO.h3.fontWeight, fontSize: TIPO.h3.fontSize, lineHeight: TIPO.h3.lineHeight, letterSpacing: TIPO.h3.letterSpacing, textTransform: "uppercase", whiteSpace: "nowrap" }}>{lugar}</div>
        <div style={{ fontFamily: FONTE.mono, fontWeight: 500, fontSize: 26, lineHeight: 1, letterSpacing: "0.06em", color: rgba(COR.grafite, 0.8), whiteSpace: "nowrap" }}>{detalhe}</div>
      </div>
      <div style={{ width: H, height: H, display: "grid", placeItems: "center", background: COR.grafite, borderRadius: `0 ${RAIO.placa}px ${RAIO.placa}px 0`, boxShadow: "inset 0 0 0 2px rgba(255,255,255,.08)" }}>
        <Seta tamanho={64} cor={COR.amarelo} />
      </div>
    </div>
  );
};

/** Chamada do Instagram (decisão de 16/10/2026): glifo oficial + "SEGUE NO INSTA" + @primeirodiaem, no espaço do lower third. Sem som. */
export const ChamadaInstagram: React.FC<{ ini: number; fim: number; usuario?: string }> = ({ ini, fim, usuario = "@primeirodiaem" }) => {
  const { visivel, x, opac } = useEntradaSaida(ini, fim);
  if (!visivel) return null;
  return (
    <div
      style={{
        position: "absolute",
        left: YT.margemTitulo,
        top: LOWER_BASE - 128,
        height: 128,
        boxSizing: "border-box",
        display: "flex",
        alignItems: "center",
        gap: 26,
        padding: "0 40px 0 30px",
        background: COR.grafite,
        borderRadius: RAIO.placa,
        boxShadow: `${SOMBRA.placa}, inset 0 0 0 2px rgba(255,255,255,.08)`,
        translate: `${x}px 0`,
        opacity: opac,
      }}
    >
      <GlifoInstagram tamanho={76} cor={COR.papel} />
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <span style={{ fontFamily: FONTE.display, fontWeight: TIPO.label.fontWeight, fontSize: TIPO.label.fontSize, lineHeight: 1, letterSpacing: TIPO.label.letterSpacing, color: COR.amarelo }}>SEGUE NO INSTA</span>
        <span style={{ fontFamily: FONTE.texto, fontWeight: 700, fontSize: 52, lineHeight: 1, color: COR.papel }}>{usuario}</span>
      </div>
    </div>
  );
};

type DadosMapa = {
  major: string[];
  minor: string[];
  agua: string[];
  canal: string[];
  rota: [number, number][];
  paradas: { n: number; nome: string; hora: string; xy: [number, number] }[];
};

const comprimento = (pts: [number, number][]): number =>
  pts.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);

/** Pin 1º (DS 1.6): gota grafite com o sol-horizonte amarelo dentro; contorno papel para destacar no mapa escuro. */
const Pin: React.FC<{ x: number; y: number; t: number }> = ({ x, y, t }) => {
  if (t < 0) return null;
  const s = kf(t, [0, 160, 280], [0, 1.15, 1], [EASE.out, EASE.out]);
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <path d="M0 0 C-10 -18 -30 -32 -30 -54 A30 30 0 1 1 30 -54 C30 -32 10 -18 0 0Z" fill={COR.grafite} stroke={COR.papel} strokeWidth={4} />
      <path d="M-16 -50 A16 16 0 0 1 16 -50Z" fill={COR.amarelo} />
      <rect x={-20} y={-48} width={40} height={5} rx={2} fill={COR.amarelo} />
    </g>
  );
};

/**
 * Mapa do dia (DS 5.4): mapa próprio a partir do OpenStreetMap (fundo grafite 900, ruas grafite 700,
 * água grafite 800), Rota amarela contínua de 8 px que se desenha, paradas numeradas com a hora e Pin 1º
 * no destino. Som: whoosh suave quando a Rota começa (decisão de 16/10/2026). Crédito do OSM na tela.
 */
export const MapaRota: React.FC<{ arquivo: string; ini: number; fim: number; desenho?: number; refLufs?: number }> = ({ arquivo, ini, fim, desenho = 2000, refLufs = -16 }) => {
  const t = useMs();
  const [dados, setDados] = useState<DadosMapa | null>(null);
  const [h] = useState(() => delayRender(`mapa ${arquivo}`));
  useEffect(() => {
    fetch(staticFile(arquivo))
      .then((r) => r.json())
      .then((d: DadosMapa) => {
        setDados(d);
        continueRender(h);
      });
  }, [arquivo, h]);
  if (!dados) return null;
  const te = t - ini;
  const visivel = te >= 0 && t < fim + DUR.base;
  const L = comprimento(dados.rota);
  const p = kf(te, [300, 300 + desenho], [0, 1], EASE.cinema);
  const zoom = kf(te, [0, fim - ini], [0.9, 0.93]);
  const opac = kf(te, [0, DUR.base], [0, 1]) * kf(t - fim, [0, DUR.base], [1, 0]);
  const fimRota = 300 + desenho;
  return (
    <>
      {visivel && (
        <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{ position: "absolute", inset: 0, background: COR.grafite, opacity: opac }}>
          <g transform={`translate(960 565) scale(${zoom}) translate(-960 -540)`}>
            {dados.agua.map((d, i) => <path key={`a${i}`} d={d} fill={COR.grafite800} />)}
            {dados.canal.map((d, i) => <path key={`c${i}`} d={d} fill="none" stroke={COR.grafite800} strokeWidth={10} strokeLinecap="round" />)}
            {dados.minor.map((d, i) => <path key={`m${i}`} d={d} fill="none" stroke={COR.grafite700} strokeWidth={2.5} strokeLinecap="round" />)}
            {dados.major.map((d, i) => <path key={`M${i}`} d={d} fill="none" stroke={COR.grafite700} strokeWidth={6} strokeLinecap="round" />)}
            <polyline
              points={dados.rota.map((q) => q.join(",")).join(" ")}
              fill="none"
              stroke={COR.amarelo}
              strokeWidth={8 / zoom}
              strokeLinejoin="round"
              strokeLinecap="round"
              strokeDasharray={L}
              strokeDashoffset={L * (1 - p)}
            />
            {dados.paradas.map((s, i) => {
              const aparece = i === 0 ? 300 : fimRota;
              const tp = te - aparece;
              if (tp < 0) return null;
              const o = kf(tp, [0, DUR.fast], [0, 1], EASE.out);
              const ultima = i === dados.paradas.length - 1;
              const [x, y] = s.xy;
              const labelY = ultima ? y + 40 : y - 64;
              return (
                <g key={s.n} opacity={o}>
                  {!ultima && <circle cx={x} cy={y} r={14 / zoom} fill={COR.grafite} stroke={COR.amarelo} strokeWidth={4} />}
                  {!ultima && (
                    <text x={x} y={y + 7 / zoom} textAnchor="middle" fontFamily={FONTE.dados} fontWeight={700} fontSize={20 / zoom} fill={COR.amarelo}>
                      {s.n}
                    </text>
                  )}
                  <g transform={`translate(${x + 30} ${labelY}) scale(${1 / zoom})`}>
                    <rect x={0} y={0} width={34 + 16.2 * (s.nome.length + s.hora.length + 3)} height={48} rx={RAIO.tag} fill={COR.grafite} stroke={rgba(COR.papel, 0.15)} />
                    <text x={18} y={33} fontFamily={FONTE.mono} fontWeight={500} fontSize={27} letterSpacing="0.04em" fill={COR.papel}>
                      {s.nome} <tspan fill={COR.amarelo}>· {s.hora}</tspan>
                    </text>
                  </g>
                </g>
              );
            })}
            {(() => {
              const s = dados.paradas[dados.paradas.length - 1];
              return <g transform={`translate(${s.xy[0]} ${s.xy[1]}) scale(${1 / zoom}) translate(${-s.xy[0]} ${-s.xy[1]})`}><Pin x={s.xy[0]} y={s.xy[1]} t={te - fimRota} /></g>;
            })()}
          </g>
          <text x={1920 - YT.margemAcao} y={1080 - YT.margemAcao + 20} textAnchor="end" fontFamily={FONTE.mono} fontSize={18} fill={COR.poeira}>
            © OpenStreetMap contributors
          </text>
        </svg>
      )}
      <Som nome="whoosh" em={ini + 300} relDb={SOM.whoosh} refLufs={refLufs} />
    </>
  );
};
