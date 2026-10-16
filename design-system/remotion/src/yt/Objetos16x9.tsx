/**
 * Objetos do vídeo longo do YouTube (16:9, 1920 × 1080). Decisões do Diego de 16/10/2026 em
 * `docs/VIDEO_LONGO_YOUTUBE.md`. Cores, fontes, sombras, raios, curvas e durações vêm dos tokens;
 * as posições vêm da grade 16:9 do DS V2 (1.3): margem de título 96, lower third com base em y 960.
 */
import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, staticFile } from "remotion";
import { Fibra } from "../ds/material";
import { GlifoInstagram, Seta } from "../ds/icones";
import { Bilhete } from "../ds/Bilhete";
import { Simbolo1 } from "../ds/Simbolo1";
import { Som } from "../ds/Som";
import { kf, useMs } from "../ds/tempo";
import { COR, DUR, EASE, FONTE, RAIO, SOM, SOMBRA, TIPO, YT, rgba } from "../ds/tokens";

/** Volumes (rel. à voz) dos sons novos do vídeo longo: provisórios, o mesmo do clack, a calibrar na escuta. */
const VOLUME_PLIM_DB = -10;
export const VOLUME_PAGINA_DB = -10;

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
  parque: string[];
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
 * Mapa do dia (DS 5.4, 2.3.0): mapa próprio a partir do OpenStreetMap em cores naturais (tokens `color.map`),
 * Rota amarela contínua de 8 px com contorno grafite que se desenha, paradas numeradas com a hora e Pin 1º
 * no destino. Som (decisões de 16/10/2026): whoosh suave quando a Rota começa e o "plim" quando o Pin
 * assenta no destino. Crédito do OSM na tela.
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
        <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{ position: "absolute", inset: 0, background: COR.mapaTerra, opacity: opac }}>
          <g transform={`translate(960 565) scale(${zoom}) translate(-960 -540)`}>
            <rect x={-400} y={-400} width={2720} height={1880} fill={COR.mapaTerra} />
            {dados.parque.map((d, i) => <path key={`p${i}`} d={d} fill={COR.mapaParque} />)}
            {dados.agua.map((d, i) => <path key={`a${i}`} d={d} fill={COR.mapaAgua} />)}
            {dados.canal.map((d, i) => <path key={`c${i}`} d={d} fill="none" stroke={COR.mapaAgua} strokeWidth={10} strokeLinecap="round" />)}
            {dados.minor.map((d, i) => <path key={`mc${i}`} d={d} fill="none" stroke={COR.mapaRuaContorno} strokeWidth={6} strokeLinecap="round" />)}
            {dados.major.map((d, i) => <path key={`Mc${i}`} d={d} fill="none" stroke={COR.mapaRuaContorno} strokeWidth={11} strokeLinecap="round" />)}
            {dados.minor.map((d, i) => <path key={`m${i}`} d={d} fill="none" stroke={COR.mapaRua} strokeWidth={3.5} strokeLinecap="round" />)}
            {dados.major.map((d, i) => <path key={`M${i}`} d={d} fill="none" stroke={COR.mapaVia} strokeWidth={8} strokeLinecap="round" />)}
            <polyline
              points={dados.rota.map((q) => q.join(",")).join(" ")}
              fill="none"
              stroke={COR.grafite}
              strokeWidth={14 / zoom}
              strokeLinejoin="round"
              strokeLinecap="round"
              strokeDasharray={L}
              strokeDashoffset={L * (1 - p)}
            />
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
                    <rect x={0} y={0} width={40 + 17.6 * (s.nome.length + s.hora.length + 3)} height={48} rx={RAIO.tag} fill={COR.grafite} stroke={rgba(COR.papel, 0.15)} />
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
          <text x={1920 - YT.margemAcao} y={1080 - YT.margemAcao + 20} textAnchor="end" fontFamily={FONTE.mono} fontSize={18} fill={COR.asfalto}>
            © OpenStreetMap contributors
          </text>
        </svg>
      )}
      <Som nome="whoosh" em={ini + 300} relDb={SOM.whoosh} refLufs={refLufs} />
      {/* chegada no destino (pedido do Diego, 16/10/2026): "plim" quando o Pin 1º assenta */}
      <Som nome="plim" em={ini + 300 + desenho} relDb={VOLUME_PLIM_DB} refLufs={refLufs} />
    </>
  );
};

/**
 * Transição Página (pedido do Diego, 16/10/2026, troca de dia no vídeo longo): a cena que sai vira como a
 * folha de um caderno, presa na borda esquerda, mostrando o verso de papel (fibra), e revela a cena nova
 * por baixo, com a sombra da folha passando sobre ela. 700 ms com `ease-cinema`. Som: folha virando,
 * no início do giro (`PD_pagina_v1.wav`). Envolve a cena que SAI; a cena que entra fica por baixo, já tocando.
 */
export const DUR_PAGINA = 700;

export const VirarPagina: React.FC<{ corte: number; children: React.ReactNode }> = ({ corte, children }) => {
  const t = useMs() - corte;
  const p = kf(t, [0, DUR_PAGINA], [0, 1], EASE.cinema);
  if (t >= DUR_PAGINA) return null;
  const ang = -180 * p;
  const sombra = Math.sin(Math.PI * p);
  return (
    <AbsoluteFill style={{ perspective: 2600, perspectiveOrigin: "0 50%" }}>
      {t >= 0 && (
        <AbsoluteFill style={{ background: `linear-gradient(90deg, ${rgba(COR.grafite, 0.55 * sombra)}, ${rgba(COR.grafite, 0)} ${30 + 60 * p}%)` }} />
      )}
      <AbsoluteFill style={{ transformOrigin: "0 50%", transform: `rotateY(${ang}deg)`, transformStyle: "preserve-3d" }}>
        <AbsoluteFill style={{ backfaceVisibility: "hidden", overflow: "hidden" }}>
          {children}
          <AbsoluteFill style={{ background: `linear-gradient(90deg, ${rgba(COR.grafite, 0)} 40%, ${rgba(COR.grafite, 0.45 * sombra)})` }} />
        </AbsoluteFill>
        <AbsoluteFill style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)", background: COR.recibo, overflow: "hidden" }}>
          <Fibra opacidade={0.08} semente={21} />
          <AbsoluteFill style={{ background: `linear-gradient(270deg, ${rgba(COR.grafite, 0.25 * sombra)}, ${rgba(COR.grafite, 0)} 60%)` }} />
        </AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Espaço de vídeo da tela final: moldura onde o YouTube coloca o elemento de vídeo (16:9). */
const EspacoVideo: React.FC<{ x: number; y: number; w: number; rotulo: string; t: number }> = ({ x, y, w, rotulo, t }) => {
  const o = kf(t, [0, DUR.base], [0, 1], EASE.out);
  const h = (w * 9) / 16;
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o, translate: `0 ${(1 - o) * 16}px` }}>
      <div style={{ fontFamily: FONTE.mono, fontWeight: 500, fontSize: 24, letterSpacing: "0.08em", color: COR.asfalto, marginBottom: 12 }}>{rotulo}</div>
      <div style={{ width: w, height: h, boxSizing: "border-box", borderRadius: RAIO.foto, border: `4px solid ${rgba(COR.grafite, 0.18)}`, background: rgba(COR.grafite, 0.06) }} />
    </div>
  );
};

/**
 * Tela final do vídeo longo (DS 5.4): 20 s, fundo papel com fibra, 2 espaços de vídeo à direita (onde o
 * YouTube põe os elementos da tela final, que vão nos últimos 5–20 s) e o Bilhete "próximo dia:" à esquerda,
 * com o símbolo 1º. Nada de legenda. Som: os 2 cliques de caneta quando o Bilhete começa a ser escrito.
 */
export const TelaFinal: React.FC<{ ini: number; proximo: string; refLufs?: number }> = ({ ini, proximo, refLufs = -16 }) => {
  const t = useMs() - ini;
  const larg = 760;
  const xSlot = 1920 - YT.margemTitulo - larg;
  return (
    <>
      {t >= 0 && (
        <AbsoluteFill style={{ background: COR.papel }}>
          <Fibra semente={31} />
          <div style={{ position: "absolute", left: YT.margemTitulo + 24, top: 250, scale: "1.35", transformOrigin: "0 0" }}>
            <Bilhete texto={`próximo dia:|${proximo} →`} x={0} y={0} entrada={ini + 400} />
          </div>
          <div style={{ position: "absolute", left: YT.margemTitulo, bottom: YT.margemTitulo, display: "flex", alignItems: "center", gap: 20, opacity: kf(t, [900, 900 + DUR.base], [0, 1]) }}>
            <div style={{ width: 96, height: 96, borderRadius: RAIO.placa, background: COR.grafite, display: "grid", placeItems: "center" }}>
              <Simbolo1 altura={70} t={t - 900} corNumero={COR.recibo} />
            </div>
            <span style={{ fontFamily: FONTE.texto, fontWeight: 700, fontSize: 40, color: COR.grafite }}>@primeirodiaem</span>
          </div>
          <EspacoVideo x={xSlot} y={YT.margemTitulo - 10} w={larg} rotulo="PRÓXIMO VÍDEO" t={t - 200} />
          <EspacoVideo x={xSlot} y={YT.margemTitulo + 470} w={larg} rotulo="ASSISTA TAMBÉM" t={t - 350} />
        </AbsoluteFill>
      )}
      <Som nome="clique" em={ini + 400 + DUR.base} relDb={SOM.clique} refLufs={refLufs} />
    </>
  );
};
