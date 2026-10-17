/**
 * Reel montado a partir das decisões de uma revisão (reels/<reel>/revN/revN.json + medições do
 * `revN.py preparar`). Nenhuma decisão de conteúdo mora aqui: cenas, cortes, legendas, objetos,
 * sons e mixagem vêm das props. Este arquivo só aplica o DS V2.
 *
 * Tempos nas props: segundos. `cena` + `t` = relativo ao início da cena na linha do tempo.
 * `audio` + `ini`/`fim` (legendas) = tempo do arquivo-fonte daquele áudio.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  Sequence,
  staticFile,
  useVideoConfig,
} from "remotion";
import { Placa, Modulo } from "../ds/Placa";
import { PlacaDirecao } from "../ds/PlacaDirecao";
import { Grao, ScrimBase } from "../ds/material";
import { LegendaInformacao, LegendaPadrao } from "../ds/Legendas";
import {
  CenaArrasto,
  Cinema,
  FlashSnap,
  Varredura,
  useSnapZoom,
} from "../ds/Transicoes";
import { NomeSom, Som } from "../ds/Som";
import { kf, useMs } from "../ds/tempo";
import { EFEITO } from "../ds/tokens";

type Cena = {
  id: string;
  fonte: string;
  in: number;
  arquivo: string;
  quadros: number;
  dur: number;
  audio: "voz" | "ambiente" | "mudo";
  audio_arquivo?: string;
  kenburns?: boolean;
  /** Quadros extras antes/depois do trecho (alças para transições com sobreposição). */
  alca_antes_q?: number;
  alca_depois_q?: number;
};
type AudioExtra = {
  id: string;
  in: number;
  dur: number;
  tipo: "voz" | "ambiente";
  audio_arquivo: string;
  inicio: { cena: string; t: number };
};
type Transicao = {
  tipo: "arrasto" | "snap" | "cinema" | "varredura";
  entra: string;
};
type LegendaBloco = {
  audio?: string;
  cena?: string;
  modo?: "palavra" | "grupo";
  grupos: { texto: string; ini: number; fim: number; destaque_em?: number }[];
};

export type PropsReel = {
  fps: number;
  largura: number;
  altura: number;
  cenas: Cena[];
  audios: AudioExtra[];
  transicoes: Transicao[];
  placa?: {
    cena: string;
    t: number;
    saida?: number;
    rotulo?: string;
    destino: string;
    modulo?: Modulo;
    tamanho?: "G" | "M" | "P";
  };
  /** Placa de direção (2.6): destino H3 + linha em Plex Mono + seta de direção. */
  placa_direcao?: {
    cena: string;
    t: number;
    saida?: { cena: string; t: number };
    destino: string;
    linha: string;
    seta?: "diagonal" | "cima";
    /** Topo da placa (px). Padrão: y 640 do DS; outro valor só como exceção registrada na QA do Reel. */
    y?: number;
  };
  informacao?: {
    cena: string;
    t: number;
    fim: number;
    rotulo: string;
    numero: string;
    complemento?: string;
  }[];
  legendas: LegendaBloco[];
  sons: {
    nome: NomeSom;
    cena: string;
    t: number;
    rel_db: number;
  }[];
  mix: { voz_lufs: number; ambiente_lufs: number };
  capa?: {
    cena: string;
    t: number;
    placa: {
      rotulo?: string;
      destino: string;
      modulo?: Modulo;
      tamanho?: "G" | "M" | "P";
    };
  };
};

export const propsVazias: PropsReel = {
  fps: 30,
  largura: 1080,
  altura: 1920,
  cenas: [],
  audios: [],
  transicoes: [],
  legendas: [],
  sons: [],
  mix: { voz_lufs: -16, ambiente_lufs: -19 },
};

export const metadadosReel: CalculateMetadataFunction<PropsReel> = ({
  props,
}) => ({
  durationInFrames: Math.max(
    1,
    props.cenas.reduce((s, c) => s + c.quadros, 0),
  ),
  fps: props.fps,
  width: props.largura,
  height: props.altura,
});

/** Linha do tempo: início de cada cena em quadros e em ms. */
const linhaDoTempo = (p: PropsReel) => {
  const ini: Record<string, number> = {};
  let acc = 0;
  for (const c of p.cenas) {
    ini[c.id] = acc;
    acc += c.quadros;
  }
  const ms = (cena: string, t: number) => (ini[cena] * 1000) / p.fps + t * 1000;
  const inicioAudio = (a: AudioExtra) => ms(a.inicio.cena, a.inicio.t);
  return { ini, ms, inicioAudio };
};

const CenaVideo: React.FC<{ cena: Cena; zoom: boolean }> = ({ cena, zoom }) => {
  const { fps } = useVideoConfig();
  const t = useMs() - ((cena.alca_antes_q ?? 0) * 1000) / fps;
  const kb = cena.kenburns
    ? kf(t, [0, cena.dur * 1000], [1, EFEITO.zoomSutil])
    : 1; // Ken Burns 100 → 104% (4.5)
  const snap = useSnapZoom(((cena.alca_antes_q ?? 0) * 1000) / fps);
  return (
    <AbsoluteFill style={{ scale: String(kb * (zoom ? snap : 1)) }}>
      <Video
        src={staticFile(cena.arquivo)}
        muted
        objectFit="cover"
        style={{ width: "100%", height: "100%" }}
      />
    </AbsoluteFill>
  );
};

export const Reel: React.FC<PropsReel> = (p) => {
  const { fps } = useVideoConfig();
  const { ini, ms, inicioAudio } = linhaDoTempo(p);
  const q = (m: number) => Math.round((m * fps) / 1000);
  const tr = (id: string) => p.transicoes.find((x) => x.entra === id);
  const proximo = (i: number) => p.cenas[i + 1]?.id;

  // referência de loudness em cada ponto (para os sons da 4.6)
  const refLufs = (cena: string): number => {
    const c = p.cenas.find((x) => x.id === cena);
    if (c && c.audio !== "mudo") return p.mix[`${c.audio}_lufs`];
    const a = p.audios.find((x) => x.inicio.cena === cena);
    return a ? p.mix[`${a.tipo}_lufs`] : p.mix.ambiente_lufs;
  };

  // legendas → ms da composição
  const grupos = p.legendas.flatMap((b) => {
    const extra = b.audio ? p.audios.find((a) => a.id === b.audio) : undefined;
    const cenaAudio =
      b.audio && !extra ? p.cenas.find((c) => c.id === b.audio) : undefined;
    const conv = (s: number): number => {
      if (extra) return inicioAudio(extra) + (s - extra.in) * 1000;
      if (cenaAudio) return ms(cenaAudio.id, s - cenaAudio.in);
      return ms(b.cena as string, s);
    };
    return b.grupos.map((g) => ({
      texto: g.texto,
      ini: conv(g.ini),
      fim: conv(g.fim),
      palavras:
        g.destaque_em !== undefined
          ? g.texto
              .split(/[\s|]+/)
              .filter(Boolean)
              .map((w) =>
                w.startsWith("*") ? conv(g.destaque_em as number) : conv(g.ini),
              )
          : undefined,
    }));
  });
  const modo = p.legendas[0]?.modo ?? "grupo";

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* cenas (camada isolada: o zIndex do Arrasto não pode passar por cima das legendas) */}
      <AbsoluteFill style={{ isolation: "isolate" }}>
        {p.cenas.map((c, i) => {
          const entra = tr(c.id);
          const sai = proximo(i) ? tr(proximo(i) as string) : undefined;
          const antes = c.alca_antes_q ?? 0;
          const depois = c.alca_depois_q ?? 0;
          const msAntes = (antes * 1000) / fps;
          let conteudo = <CenaVideo cena={c} zoom={entra?.tipo === "snap"} />;
          if (sai?.tipo === "arrasto")
            conteudo = (
              <CenaArrasto corte={msAntes + c.dur * 1000} papel="sai">
                {conteudo}
              </CenaArrasto>
            );
          if (entra?.tipo === "arrasto")
            conteudo = (
              <CenaArrasto corte={msAntes} papel="entra">
                {conteudo}
              </CenaArrasto>
            );
          return (
            <Sequence
              key={c.id}
              name={`cena ${c.id}`}
              from={ini[c.id] - antes}
              durationInFrames={c.quadros + antes + depois}
            >
              {conteudo}
            </Sequence>
          );
        })}
      </AbsoluteFill>

      {/* áudio das cenas e áudios extras (J-cut) */}
      {p.cenas
        .filter((c) => c.audio_arquivo)
        .map((c) => (
          <Sequence
            key={`a-${c.id}`}
            name={`áudio ${c.id}`}
            from={ini[c.id]}
            durationInFrames={c.quadros}
            layout="none"
          >
            <Audio src={staticFile(c.audio_arquivo as string)} />
          </Sequence>
        ))}
      {p.audios.map((a) => (
        <Sequence
          key={`x-${a.id}`}
          name={`áudio ${a.id}`}
          from={q(inicioAudio(a))}
          durationInFrames={Math.round(a.dur * fps)}
          layout="none"
        >
          <Audio src={staticFile(a.audio_arquivo)} />
        </Sequence>
      ))}

      <ScrimBase />

      {/* transições que são camadas por cima */}
      {p.transicoes.map((t) => {
        const corte = ms(t.entra, 0);
        if (t.tipo === "varredura")
          return <Varredura key={t.entra} corte={corte} />;
        if (t.tipo === "cinema") return <Cinema key={t.entra} corte={corte} />;
        if (t.tipo === "snap") return <FlashSnap key={t.entra} corte={corte} />;
        return null;
      })}

      {p.placa && (
        <Placa
          rotulo={p.placa.rotulo}
          destino={p.placa.destino}
          modulo={p.placa.modulo}
          tamanho={p.placa.tamanho}
          entrada={ms(p.placa.cena, p.placa.t)}
          saida={
            p.placa.saida !== undefined
              ? ms(p.placa.cena, p.placa.saida)
              : undefined
          }
        />
      )}

      {p.placa_direcao && (
        <PlacaDirecao
          destino={p.placa_direcao.destino}
          linha={p.placa_direcao.linha}
          seta={p.placa_direcao.seta}
          y={p.placa_direcao.y}
          entrada={ms(p.placa_direcao.cena, p.placa_direcao.t)}
          saida={
            p.placa_direcao.saida
              ? ms(p.placa_direcao.saida.cena, p.placa_direcao.saida.t)
              : undefined
          }
        />
      )}

      {p.informacao?.map((info, i) => (
        <LegendaInformacao
          key={i}
          rotulo={info.rotulo}
          numero={info.numero}
          complemento={info.complemento}
          ini={ms(info.cena, info.t)}
          fim={ms(info.cena, info.fim)}
        />
      ))}

      <LegendaPadrao grupos={grupos} modo={modo} />

      {p.sons.map((s, i) => (
        <Som
          key={i}
          nome={s.nome}
          em={ms(s.cena, s.t)}
          relDb={s.rel_db}
          refLufs={refLufs(s.cena)}
        />
      ))}

      <Grao />
    </AbsoluteFill>
  );
};

/** Capa do Reel: quadro de uma cena com a placa estática (brilho congelado a 30%, DS 2.1). */
export const CapaReel: React.FC<PropsReel> = (p) => {
  const { fps } = useVideoConfig();
  if (!p.capa) return <AbsoluteFill style={{ background: "#000" }} />;
  const cena = p.cenas.find((c) => c.id === p.capa?.cena) as Cena;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Video
        src={staticFile(cena.arquivo)}
        muted
        trimBefore={Math.round(p.capa.t * fps) + (cena.alca_antes_q ?? 0)}
        objectFit="cover"
        style={{ width: "100%", height: "100%" }}
      />
      <Placa {...p.capa.placa} entrada={null} />
      <Grao />
    </AbsoluteFill>
  );
};
