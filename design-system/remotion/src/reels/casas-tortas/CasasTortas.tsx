/**
 * Reel "As casas que dançam" (AMS-casas-tortas, REV1): narração do Diego, planos reais parados de até 3 s,
 * três cenas desenhadas e só a legenda do DS (sem a placa de abertura, a pedido do Diego), com o CTA do
 * vídeo completo no YouTube no fim. Decisões em `reels/amsterdam-casas-tortas/rev1/rev1.json`; tempos e
 * arquivos nas props geradas por `rev1.py props` (ms na linha do tempo do Reel).
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Img, Sequence, staticFile, useVideoConfig } from "remotion";
import { Placa, Modulo } from "../../ds/Placa";
import { Grao, ScrimBase, Vinheta } from "../../ds/material";
import { GrupoLegenda, LegendaEmocional, LegendaInformacao, LegendaPadrao } from "../../ds/Legendas";
import { Cinema, CenaRota, Varredura } from "../../ds/Transicoes";
import { ARQUIVOS, NomeSom } from "../../ds/Som";
import { kf, useMs } from "../../ds/tempo";
import { EASE, EFEITO } from "../../ds/tokens";
import { CenaFileira, CenaGancho, CenaSolo } from "./cenas";

type Plano = {
  id: string;
  tipo: "foto" | "video" | "desenho";
  ini: number;
  fim: number;
  arquivo?: string;
  desenho?: "retas" | "empurrao" | "solo" | "gancho";
  transicao?: "varredura" | "cinema" | "rota";
};

export type PropsCasasTortas = {
  fps: number;
  largura: number;
  altura: number;
  duracao: number;
  planos: Plano[];
  eventos: Record<string, number | number[]>;
  legendas: GrupoLegenda[];
  emocional: { texto: string; ini: number; fim: number } | null;
  informacao: { rotulo: string; numero: string; ini: number; fim: number }[];
  cta: { rotulo: string; destino: string; modulo: Modulo; tamanho: "G" | "M" | "P"; ini: number };
  capa: { arquivo: string; rotulo: string; destino: string; modulo: Modulo; tamanho: "G" | "M" | "P" };
  voz: { arquivo: string; ini: number; dur: number }[];
  ambientes: { arquivo: string; ini: number; fim: number; cinema: boolean }[];
  sons: { nome: string; em: number; volume: number; ds: boolean }[];
  mix: { cinema_ambiente_rel_db: number; ambiente_lufs: number; voz_lufs: number };
};

export const propsCasasTortasVazias: PropsCasasTortas = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  duracao: 1000,
  planos: [],
  eventos: {},
  legendas: [],
  emocional: null,
  informacao: [],
  cta: { rotulo: "", destino: "", modulo: "seta", tamanho: "M", ini: 0 },
  capa: { arquivo: "", rotulo: "", destino: "", modulo: "seta", tamanho: "M" },
  voz: [],
  ambientes: [],
  sons: [],
  mix: { cinema_ambiente_rel_db: -6, ambiente_lufs: -31, voz_lufs: -16 },
};

export const metadadosCasasTortas: CalculateMetadataFunction<PropsCasasTortas> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.round((props.duracao * props.fps) / 1000)),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Rota: a cena que sai continua por baixo enquanto a linha revela a que entra (500 ms + folga). */
const SOBRA_ROTA = 560;

/** Foto (só as 2 do WhatsApp, sem vídeo): zoom lento 100 → 104% no plano inteiro (DS 4.5), para não parecer parada. */
const FotoViva: React.FC<{ pl: Plano }> = ({ pl }) => {
  const t = useMs();
  const z = kf(t, [0, pl.fim - pl.ini + SOBRA_ROTA], [1, EFEITO.zoomSutil]);
  return <Img src={staticFile(pl.arquivo as string)} style={{ width: "100%", height: "100%", objectFit: "cover", scale: String(z) }} />;
};

const ConteudoPlano: React.FC<{ pl: Plano; ev: (nome: string) => number; evs: (nome: string) => number[] }> = ({ pl, ev, evs }) => {
  if (pl.tipo === "foto") return <FotoViva pl={pl} />;
  if (pl.tipo === "video")
    return <Video src={staticFile(pl.arquivo as string)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />;
  switch (pl.desenho) {
    case "retas":
      return <CenaFileira modo="retas" ev={{ sobe: ev("retas.sobe"), inclina: evs("retas.inclina") }} />;
    case "empurrao":
      return <CenaFileira modo="empurrao" ev={{ mao: ev("empurrao.mao") }} />;
    case "solo":
      return (
        <CenaSolo
          ev={{ terreno: ev("solo.terreno"), estacas: ev("solo.estacas"), fundacoes: ev("solo.fundacoes"), tempo: ev("solo.tempo"), cede: ev("solo.cede"), inclina: ev("solo.inclina") }}
        />
      );
    default:
      return (
        <CenaGancho ev={{ sobe: ev("gancho.sobe"), bate: ev("gancho.bate"), inclina: ev("gancho.inclina"), sobe2: ev("gancho.sobe2"), entra: ev("gancho.entra") }} />
      );
  }
};

/** Vinheta 15% só no plano emocional (DS 4.5), entrando e saindo com a legenda Emocional. */
const VinhetaEmocional: React.FC<{ ini: number; fim: number }> = ({ ini, fim }) => {
  const t = useMs();
  const o = kf(t, [ini, ini + 400], [0, 1], EASE.cinema) * kf(t, [fim, fim + 300], [1, 0], EASE.cinema);
  return o > 0 ? <Vinheta opacidade={o} /> : null;
};

export const CasasTortas: React.FC<PropsCasasTortas> = (p) => {
  const { fps } = useVideoConfig();
  const q = (ms: number) => Math.round((ms * fps) / 1000);

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ isolation: "isolate" }}>
        {p.planos.map((pl, i) => {
          const prox = p.planos[i + 1];
          const fim = pl.fim + (prox?.transicao === "rota" ? SOBRA_ROTA : 0);
          const rel = (v: number) => v - pl.ini;
          const ev = (nome: string) => rel(p.eventos[nome] as number);
          const evs = (nome: string) => (p.eventos[nome] as number[]).map(rel);
          let conteudo = <ConteudoPlano pl={pl} ev={ev} evs={evs} />;
          if (pl.transicao === "rota") conteudo = <CenaRota corte={0}>{conteudo}</CenaRota>;
          return (
            <Sequence key={pl.id} name={`plano ${pl.id}`} from={q(pl.ini)} durationInFrames={q(fim) - q(pl.ini)}>
              <AbsoluteFill>{conteudo}</AbsoluteFill>
            </Sequence>
          );
        })}
      </AbsoluteFill>

      <ScrimBase />
      {p.emocional && <VinhetaEmocional ini={p.emocional.ini} fim={p.emocional.fim} />}

      {/* transições de camada (DS 4.4): Varredura de Placa e Cinema */}
      {p.planos
        .filter((pl) => pl.transicao === "varredura" || pl.transicao === "cinema")
        .map((pl) => (pl.transicao === "varredura" ? <Varredura key={pl.id} corte={pl.ini} /> : <Cinema key={pl.id} corte={pl.ini} />))}

      {p.informacao.map((info, i) => (
        <LegendaInformacao key={i} rotulo={info.rotulo} numero={info.numero} ini={info.ini} fim={info.fim} />
      ))}
      <LegendaPadrao grupos={p.legendas} modo="grupo" />
      {p.emocional && <LegendaEmocional texto={p.emocional.texto} ini={p.emocional.ini} fim={p.emocional.fim} />}

      {/* CTA (DS 2.7): placa de direção para o vídeo completo, com a Chegada */}
      <Placa rotulo={p.cta.rotulo} destino={p.cta.destino} modulo={p.cta.modulo} tamanho={p.cta.tamanho} entrada={p.cta.ini} />

      {/* voz, ambiente e efeitos */}
      {p.voz.map((v) => (
        <Sequence key={v.arquivo} name={`voz ${v.arquivo}`} from={q(v.ini)} durationInFrames={q(v.dur)} layout="none">
          <Audio src={staticFile(v.arquivo)} />
        </Sequence>
      ))}
      {p.ambientes.map((a) => {
        const ganho = Math.pow(10, (p.mix.voz_lufs + p.mix.cinema_ambiente_rel_db - p.mix.ambiente_lufs) / 20);
        return (
          <Sequence key={a.arquivo} name={`ambiente ${a.arquivo}`} from={q(a.ini)} durationInFrames={q(a.fim + 40) - q(a.ini)} layout="none">
            <Audio
              src={staticFile(a.arquivo)}
              volume={(f) => (a.cinema ? kf((f * 1000) / fps, [0, 700, 1300], [ganho, ganho, 1], EASE.cinema) : 1)}
            />
          </Sequence>
        );
      })}
      {p.sons.map((s, i) => (
        <Sequence key={i} name={`som ${s.nome}`} from={q(s.em)} layout="none">
          <Audio src={s.ds ? ARQUIVOS[s.nome as NomeSom] : staticFile(`sfx_${s.nome}.wav`)} volume={s.volume} />
        </Sequence>
      ))}

      <Grao />
    </AbsoluteFill>
  );
};

/** Capa (1080 × 1920; o recorte 3:4 do grid fica entre y 240 e 1680): gancho com a placa Hook estática. */
export const CapaCasasTortas: React.FC<PropsCasasTortas> = (p) => (
  <AbsoluteFill style={{ background: "#000" }}>
    {p.capa.arquivo && <Img src={staticFile(p.capa.arquivo)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
    <Placa rotulo={p.capa.rotulo} destino={p.capa.destino} modulo={p.capa.modulo} tamanho={p.capa.tamanho} entrada={null} />
    <Grao />
  </AbsoluteFill>
);
