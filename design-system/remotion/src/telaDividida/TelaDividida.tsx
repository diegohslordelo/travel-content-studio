/**
 * Reel em tela dividida (docs/FORMATOS_REELS.md): apoio em cima (1080 x 900), o Diego embaixo,
 * costura em y 900. Montado só a partir das props (reels/<reel>/revN/props.json + --public-dir).
 *
 * Padrão de edição (CLAUDE.md, 12): imagens sem tratamento de cor, sem degradê na base,
 * legenda que acompanha a voz palavra a palavra. DS V2 só no CTA (placa).
 * O áudio entra já mixado (voz + efeitos), um arquivo por versão.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { loadFont } from "@remotion/fonts";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Placa, Modulo } from "../ds/Placa";

type Cena = {
  id: string;
  tipo: "video" | "foto" | "diego";
  src?: string;
  ini: number;
  fim: number;
  zoom?: [number, number];
  cx?: number;
  cy?: number;
};
type Palavra = { t: string; ini: number };
type Grupo = { ini: number; fim: number; palavras: Palavra[]; px?: number };
export type TelaDivididaProps = {
  dur: number;
  diego: { src: string; offsetY: number; zoomCheia: [number, number] };
  audio: string;
  cenas: Cena[];
  gancho: { linhas: { t: string; px: number; cor?: string }[]; ini: number; fim: number; topo: number };
  legendas: Grupo[];
  pb: { ini: number; fim: number };
  cta: { destino: string; modulo: Modulo; entrada: number; rotulo?: string };
  estilo: { destaque: string; fonteLegenda: string; fonteGancho: string };
};

export const propsTelaDivididaVazias: TelaDivididaProps = {
  dur: 1,
  diego: { src: "", offsetY: 0, zoomCheia: [1, 1] },
  audio: "",
  cenas: [],
  gancho: { linhas: [], ini: 0, fim: 0, topo: 280 },
  legendas: [],
  pb: { ini: -1, fim: -1 },
  cta: { destino: "COMENTA", modulo: "seta", entrada: 1e9 },
  estilo: { destaque: "#E0AE5C", fonteLegenda: "", fonteGancho: "" },
};

export const metadadosTelaDividida: CalculateMetadataFunction<TelaDivididaProps> = ({ props }) => ({
  durationInFrames: Math.round(props.dur * 30),
  fps: 30,
  width: 1080,
  height: 1920,
});

const W = 1080;
const COSTURA = 900;
const SOMBRA_TEXTO = "0 3px 0 rgba(0,0,0,0.35), 0 4px 22px rgba(0,0,0,0.85), 0 0 3px rgba(0,0,0,0.9)";

let fontes: Promise<unknown> | null = null;
const carregar = (e: TelaDivididaProps["estilo"]) => {
  if (!fontes && e.fonteLegenda) {
    fontes = Promise.all([
      loadFont({ family: "Inter PD", url: staticFile(e.fonteLegenda), weight: "800" }),
      loadFont({ family: "Anton PD", url: staticFile(e.fonteGancho), weight: "400" }),
    ]);
  }
};

/** Imagem de apoio: cobre a área; zoom lento e linear durante a cena (FORMATOS_REELS 2). */
const Apoio: React.FC<{ c: Cena; altura: number }> = ({ c, altura }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const durQ = Math.max(1, Math.round((c.fim - c.ini) * fps));
  const [z0, z1] = c.zoom ?? [1, 1];
  const z = interpolate(frame, [0, durQ], [z0, z1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const origem = `${(c.cx ?? 0.5) * 100}% ${(c.cy ?? 0.5) * 100}%`;
  const estilo: React.CSSProperties = { width: W, height: altura, objectFit: "cover", objectPosition: origem, transform: `scale(${z})`, transformOrigin: origem };
  if (c.tipo === "foto") return <Img src={staticFile(c.src as string)} style={estilo} />;
  return <Video src={staticFile(c.src as string)} muted style={estilo} />;
};

const Legenda: React.FC<{ g: Grupo; y: number; destaque: string }> = ({ g, y, destaque }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = g.ini + frame / fps;
  const e = interpolate(frame, [0, 0.12 * fps], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, height: 0, display: "flex", justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          fontFamily: "Inter PD",
          fontWeight: 800,
          fontSize: g.px ?? 66,
          lineHeight: 1.1,
          whiteSpace: "nowrap",
          textShadow: SOMBRA_TEXTO,
          opacity: e,
          transform: `scale(${0.94 + 0.06 * e})`,
        }}
      >
        {g.palavras.map((p, i) => (
          <span key={i} style={{ color: t >= p.ini ? destaque : "#FFFFFF" }}>
            {i > 0 ? " " : ""}
            {p.t}
          </span>
        ))}
      </div>
    </div>
  );
};

export const TelaDividida: React.FC<TelaDivididaProps> = (p) => {
  carregar(p.estilo);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const q = (s: number) => Math.round(s * fps);
  const cenaAtual = p.cenas.find((c) => t >= c.ini && t < c.fim) ?? p.cenas[p.cenas.length - 1];
  const cheia = cenaAtual?.tipo === "diego";
  const pb = t >= p.pb.ini && t < p.pb.fim;

  // Diego: um único vídeo contínuo (a boca nunca sai de sincronia); só muda o enquadramento
  let estiloDiego: React.CSSProperties;
  if (cheia) {
    const [z0, z1] = p.diego.zoomCheia;
    const z = interpolate(t, [cenaAtual.ini, cenaAtual.fim], [z0, z1]);
    estiloDiego = { transform: `scale(${z})`, transformOrigin: "50% 34%" };
  } else {
    estiloDiego = { transform: `translateY(${p.diego.offsetY}px)`, clipPath: `inset(${COSTURA - p.diego.offsetY}px 0 0 0)` };
  }

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <AbsoluteFill style={{ filter: pb ? "grayscale(1)" : undefined }}>
        <AbsoluteFill style={estiloDiego}>
          <Video src={staticFile(p.diego.src)} muted style={{ width: W, height: 1920 }} />
        </AbsoluteFill>
        {!cheia && (
          <div style={{ position: "absolute", left: 0, top: 0, width: W, height: COSTURA, overflow: "hidden" }}>
            {p.cenas.map((c) =>
              c.tipo === "diego" ? null : (
                <Sequence key={c.id} from={q(c.ini)} durationInFrames={q(c.fim) - q(c.ini)} name={c.id} layout="none">
                  <Apoio c={c} altura={COSTURA} />
                </Sequence>
              ),
            )}
          </div>
        )}
        {!cheia && <div style={{ position: "absolute", left: 0, top: COSTURA - 3, width: W, height: 6, backgroundColor: "rgba(0,0,0,0.55)" }} />}
      </AbsoluteFill>

      {/* Gancho: frase inteira já escrita desde o 1º quadro (pedido do Diego), sem legenda por baixo */}
      <Sequence from={q(p.gancho.ini)} durationInFrames={q(p.gancho.fim) - q(p.gancho.ini)} name="gancho" layout="none">
        <div style={{ position: "absolute", left: 72, top: p.gancho.topo, width: 872 }}>
          {p.gancho.linhas.map((l, i) => (
            <div key={i} style={{ fontFamily: "Anton PD", fontSize: l.px, lineHeight: 1.0, color: l.cor ?? "#FFFFFF", textTransform: "uppercase", textShadow: SOMBRA_TEXTO, whiteSpace: "nowrap" }}>
              {l.t}
            </div>
          ))}
        </div>
      </Sequence>

      {p.legendas.map((g, i) => {
        const t0 = g.palavras[0]?.ini ?? g.ini; // posição pela 1ª palavra (o grupo entra 60 ms antes dela)
        const cena = p.cenas.find((c) => t0 >= c.ini - 0.001 && t0 < c.fim);
        const y = cena?.tipo === "diego" ? 1320 : COSTURA;
        return (
          <Sequence key={i} from={q(g.ini)} durationInFrames={Math.max(1, q(g.fim) - q(g.ini))} name={`legenda ${i}`} layout="none">
            <Legenda g={g} y={y} destaque={p.estilo.destaque} />
          </Sequence>
        );
      })}

      {/* CTA: única entrada do DS V2 no Reel (decisão do Diego, 28/10/2026) */}
      <Placa destino={p.cta.destino} rotulo={p.cta.rotulo} modulo={p.cta.modulo} entrada={p.cta.entrada * 1000} />

      {p.audio && <Audio src={staticFile(p.audio)} />}
    </AbsoluteFill>
  );
};
