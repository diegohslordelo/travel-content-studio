/**
 * Trailer de Reel na linguagem do formato (docs/FORMATOS_REELS.md): vídeo de base já cortado e enquadrado, texto do
 * gancho em Anton (linha a linha, no tempo da fala), legenda Inter 800 com 1 palavra em âmbar, grão 6% e degradê
 * escuro na base. O DS V2 entra só no CTA final: a Placa com o módulo de seta (CLAUDE.md, 6).
 *
 * layout "v" = 1080 × 1920 (valores do formato); "h" = 1920 × 1080 (adaptação para o Reel horizontal: sem valor do
 * formato, os tamanhos foram escolhidos para a leitura no celular com o vídeo reduzido a 1080 px de largura).
 * O som é mixado fora (rev1/montar_trailer.py) e entra no mux.
 */
import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { loadFont } from "@remotion/fonts";
import anton from "@fontsource/anton/files/anton-latin-400-normal.woff2";
import inter800 from "@fontsource/inter/files/inter-latin-800-normal.woff2";
import { Placa } from "../ds/Placa";
import { Grao } from "../ds/material";
import { useMs } from "../ds/tempo";

loadFont({ family: "Anton", url: anton, weight: "400", display: "block" });
loadFont({ family: "Inter", url: inter800, weight: "800", display: "block" });

const AMBAR = "#E0AE5C"; // FORMATOS_REELS.md, 6 (cor de destaque do formato, fora do DS)

export type PropsTrailer = {
  layout: "v" | "h";
  largura: number;
  altura: number;
  video: string;
  duracao: number;
  fps: number;
  gancho: { texto: string; em: number; tam: 1 | 2 }[];
  ganchoFim: number;
  legendas: { texto: string; destaque: string | null; ini: number; fim: number }[];
  cta: { rotulo: string; destino: string; entrada: number };
};

export const propsTrailerVazias: PropsTrailer = {
  layout: "v", largura: 1080, altura: 1920, video: "base.mp4", duracao: 1000, fps: 30, gancho: [], ganchoFim: 0, legendas: [],
  cta: { rotulo: "VÍDEO COMPLETO", destino: "NO YOUTUBE", entrada: 0 },
};

export const metadadosTrailer = ({ props }: { props: PropsTrailer }) => ({
  durationInFrames: Math.round((props.duracao * props.fps) / 1000),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

const L = {
  v: { gx: 72, gy: 300, g1: 120, g2: 156, legY: 1320, legTam: 66, degrade: 960, ctaX: 72, ctaY: 640, ctaTam: "G" as const },
  h: { gx: 96, gy: 84, g1: 104, g2: 150, legY: 930, legTam: 80, degrade: 560, ctaX: 96, ctaY: 794, ctaTam: "M" as const },
};

const sobe = (t: number, dur: number) => Math.max(0, Math.min(1, t / dur));

export const TrailerFormato: React.FC<PropsTrailer> = (p) => {
  const t = useMs();
  const l = L[p.layout];
  const leg = p.legendas.find((g) => t >= g.ini && t < g.fim);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <OffthreadVideo src={staticFile(p.video)} muted />
      {/* degradê escuro na base (legenda branca sobre céu e pedra) e na região do gancho */}
      <AbsoluteFill style={{ background: `linear-gradient(to bottom, rgba(0,0,0,0) ${p.altura - l.degrade}px, rgba(0,0,0,0.62) ${p.altura}px)` }} />
      {t < p.ganchoFim && (
        <AbsoluteFill style={{ background: `linear-gradient(to bottom, rgba(0,0,0,0.55) 0px, rgba(0,0,0,0) ${l.gy + 4 * l.g1 + 160}px)` }} />
      )}
      {t < p.ganchoFim && (
        <div style={{ position: "absolute", left: l.gx, top: l.gy, display: "flex", flexDirection: "column", alignItems: "flex-start" }}>
          {p.gancho.map((g) => {
            const k = sobe(t - g.em, 160);
            return (
              <div
                key={g.texto}
                style={{
                  fontFamily: "Anton", fontSize: g.tam === 2 ? l.g2 : l.g1, lineHeight: 1.08, color: "#fff", textTransform: "uppercase",
                  opacity: k, transform: `translateY(${(1 - k) * 24}px)`, textShadow: "0 4px 22px rgba(0,0,0,0.6)", whiteSpace: "nowrap",
                }}
              >
                {g.texto}
              </div>
            );
          })}
        </div>
      )}
      {leg && (
        <div style={{ position: "absolute", left: 0, right: 0, top: l.legY, display: "flex", justifyContent: "center" }}>
          <div
            style={{
              transform: `translateY(-50%) scale(${0.94 + 0.06 * sobe(t - leg.ini, 120)})`, opacity: sobe(t - leg.ini, 120),
              fontFamily: "Inter", fontWeight: 800, fontSize: l.legTam, lineHeight: 1.1, color: "#fff", whiteSpace: "nowrap",
              textShadow: "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85)",
            }}
          >
            {leg.texto.split(" ").map((w, i) => (
              <span key={i} style={{ color: leg.destaque && w === leg.destaque ? AMBAR : "#fff" }}>
                {i ? " " : ""}
                {w}
              </span>
            ))}
          </div>
        </div>
      )}
      <Grao opacidade={0.06} />
      <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} tamanho={l.ctaTam} x={l.ctaX} y={l.ctaY} entrada={p.cta.entrada} />
    </AbsoluteFill>
  );
};
