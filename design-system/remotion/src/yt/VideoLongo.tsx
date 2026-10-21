/**
 * Vídeo longo do YouTube (16:9) montado a partir de uma lista de decisões (`reels/<video>/revN/props_revN.json`),
 * gerada pelo script da revisão: a decupagem (trechos da fonte na ordem de saída) e os eventos (objetos do DS,
 * efeitos e sons) já no relógio do vídeo final, em ms. O som da fonte NÃO sai daqui: voz, música e mixagem são
 * feitas pelo script da revisão (padrão de áudio); este render leva só a imagem e os efeitos sonoros.
 */
import React from "react";
import { Audio, Video } from "@remotion/media";
import { AbsoluteFill, CalculateMetadataFunction, Freeze, Sequence, staticFile, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Placar, ValorPlacar } from "../ds/Placar";
import { Recibo, ReciboProps } from "../ds/Cards";
import { Ticket, TicketProps } from "../ds/Ticket";
import { Bilhete, BilheteProps } from "../ds/Bilhete";
import { Grao } from "../ds/material";
import { NomeSom, Som } from "../ds/Som";
import { kf, useMs } from "../ds/tempo";
import { EASE, SOM, YT } from "../ds/tokens";
import { LIKE_APERTA, LIKE_INSCRITO } from "../ds/Placa";
import { ChamadaInstagram, DUR_PAGINA, EtiquetaLugar, LOWER_BASE, MapaRota, Quadro, TelaFinal, VOLUME_PAGINA_DB, VirarPagina } from "./Objetos16x9";
import { FogosMurchos, GuiaNarracao, Nota, PrintSite } from "./Efeitos";

/** `congela`: mostra só o quadro `src` (imagem parada; o som da mixagem segue). */
export type Trecho = { src: number; de: number; ate: number; pagina?: boolean; congela?: boolean };

type Base = { ini: number; fim: number };
export type Evento =
  | ({ tipo: "placa"; rotulo?: string; destino: string; modulo?: "seta" | "um" | "like"; tamanho?: "G" | "M" | "P"; x?: number; y?: number; entrada: number; saida?: number; som?: boolean })
  | ({ tipo: "etiqueta"; lugar: string; detalhe: string } & Base)
  | ({ tipo: "recibo"; escala?: number } & Omit<ReciboProps, "refLufs">)
  | { tipo: "placar"; valores: ValorPlacar[]; ligar: number; desligar?: number }
  | ({ tipo: "nota"; titulo: string; linhas: string[]; x: number; y: number; largura?: number; cor?: string; cor2?: string; icone?: "alerta" | "dica" | "relogio" } & Base)
  | { tipo: "fogos"; em: number; x: number; y: number; altura?: number }
  | { tipo: "som"; nome: NomeSom; em: number; relDb: number }
  | { tipo: "audio"; arquivo: string; em: number; volume: number }
  | ({ tipo: "instagram" } & Base)
  | { tipo: "like"; entrada: number; saida: number; x?: number; y?: number }
  | { tipo: "quadro"; linhas: { em: number; nome: string; complemento?: string }[]; fim: number; x: number; y: number; escala?: number }
  | ({ tipo: "ticket"; escala?: number } & TicketProps)
  | ({ tipo: "bilhete"; escala?: number } & BilheteProps)
  | ({ tipo: "print"; arquivo: string; endereco: string; x: number; y: number; largura: number; alturaJanela: number; rolagem?: number } & Base)
  | ({ tipo: "mapa"; arquivo: string; desenho?: number } & Base)
  | { tipo: "telafinal"; ini: number; proximo: string }
  | { tipo: "guia"; inicio: number; fim: number; frases: { ini: number; fim: number; texto: string }[] };

/** Zoom da imagem (ex.: tensão crescendo no rufar): keyframes em ms do vídeo final, origem em % da tela. */
export type Zoom = { ms: number[]; escala: number[]; origem?: [number, number] };

export type PropsVideoLongo = {
  video: string;
  duracao: number;
  trechos: Trecho[];
  eventos: Evento[];
  zooms?: Zoom[];
  refLufs: number;
};

export const propsVideoLongoVazias: PropsVideoLongo = { video: "", duracao: 1000, trechos: [], eventos: [], zooms: [], refLufs: -16 };

export const metadadosVideoLongo: CalculateMetadataFunction<PropsVideoLongo> = ({ props }) => ({
  durationInFrames: Math.max(1, Math.round((props.duracao * 24) / 1000)),
  fps: 24,
});

const TrechoBase: React.FC<{ v: string; tr: Trecho }> = ({ v, tr }) => {
  const { fps } = useVideoConfig();
  const q = (ms: number) => Math.round((ms * fps) / 1000);
  const dur = q(tr.ate) - q(tr.de) + (tr.pagina ? q(DUR_PAGINA) : 0);
  const base = <Video src={v.startsWith("http") ? v : staticFile(v)} trimBefore={q(tr.src)} muted objectFit="cover" style={{ width: "100%", height: "100%" }} />;
  const video = tr.congela ? <Freeze frame={0}>{base}</Freeze> : base;
  return (
    <Sequence from={q(tr.de)} durationInFrames={dur} name={`fonte ${(tr.src / 1000).toFixed(2)} s`}>
      {tr.pagina ? <VirarPagina corte={tr.ate - tr.de}>{video}</VirarPagina> : <AbsoluteFill>{video}</AbsoluteFill>}
    </Sequence>
  );
};

const CamadaBase: React.FC<{ p: PropsVideoLongo }> = ({ p }) => {
  const t = useMs();
  let escala = 1;
  let origem: [number, number] = [50, 50];
  for (const z of p.zooms ?? []) {
    if (t >= z.ms[0] && t <= z.ms[z.ms.length - 1]) {
      escala = kf(t, z.ms, z.escala, EASE.out);
      origem = z.origem ?? origem;
    }
  }
  return (
    <AbsoluteFill style={{ scale: String(escala), transformOrigin: `${origem[0]}% ${origem[1]}%` }}>
      {/* de trás para a frente: a cena que vira a página fica por cima da seguinte */}
      {[...p.trechos].reverse().map((tr, i) => (
        <TrechoBase key={`${tr.de}-${i}`} v={p.video} tr={tr} />
      ))}
    </AbsoluteFill>
  );
};

const Escala: React.FC<{ x?: number; y?: number; escala?: number; children: React.ReactNode }> = ({ x = 0, y = 0, escala = 1, children }) => (
  <div style={{ position: "absolute", left: x, top: y, scale: String(escala), transformOrigin: "0 0" }}>{children}</div>
);

const UmEvento: React.FC<{ e: Evento; refLufs: number }> = ({ e, refLufs }) => {
  const { fps } = useVideoConfig();
  switch (e.tipo) {
    case "placa":
      return (
        <>
          <Placa rotulo={e.rotulo} destino={e.destino} modulo={e.modulo} tamanho={e.tamanho ?? "M"} x={e.x ?? YT.margemTitulo} y={e.y ?? YT.margemTitulo} entrada={e.entrada} saida={e.saida} />
          {e.som !== false && <Som nome="clack" em={e.entrada + 280} relDb={SOM.clack} refLufs={refLufs} />}
        </>
      );
    case "etiqueta":
      return <EtiquetaLugar lugar={e.lugar} detalhe={e.detalhe} ini={e.ini} fim={e.fim} />;
    case "recibo": {
      const { escala = 0.72, x = 1400, y = 150, ...r } = e;
      return (
        <>
          <Escala x={x} y={y} escala={escala}>
            <Recibo {...r} x={0} y={0} som={false} />
          </Escala>
          {e.som !== false && <Som nome="moeda" em={e.ini} relDb={-10} refLufs={refLufs} />}
          {e.correcao && <Som nome="clique" em={e.ini + e.correcao.em} relDb={SOM.clique} refLufs={refLufs} />}
        </>
      );
    }
    case "placar":
      // as somas do Placar acontecem junto com o Recibo, que já toca a moeda: o Placar fica sem som (som={false}), como prevê o Remotion (pendência 14)
      return <Placar valores={e.valores} ligar={e.ligar} desligar={e.desligar} x={YT.margemTitulo} y={72} som={false} refLufs={refLufs} />;
    case "nota":
      return <Nota {...e} />;
    case "fogos":
      return <FogosMurchos em={e.em} x={e.x} y={e.y} altura={e.altura} />;
    case "som":
      return <Som nome={e.nome} em={e.em} relDb={e.relDb} refLufs={refLufs} />;
    case "audio":
      return (
        <Sequence from={Math.round((e.em * fps) / 1000)} layout="none" name={`som ${e.arquivo}`}>
          <Audio src={staticFile(e.arquivo)} volume={e.volume} />
        </Sequence>
      );
    case "instagram":
      return <ChamadaInstagram ini={e.ini} fim={e.fim} />;
    case "like":
      return (
        <>
          <Placa rotulo="DEIXA O LIKE E" destino="SE INSCREVE" modulo="like" tamanho="M" x={e.x ?? YT.margemTitulo} y={e.y ?? LOWER_BASE - 166} entrada={e.entrada} saida={e.saida} />
          <Som nome="clique" em={e.entrada + LIKE_APERTA} relDb={SOM.clique} refLufs={refLufs} />
          <Som nome="ding" em={e.entrada + LIKE_INSCRITO} relDb={SOM.ding} refLufs={refLufs} />
        </>
      );
    case "quadro":
      return <Quadro linhas={e.linhas} fim={e.fim} x={e.x} y={e.y} escala={e.escala} />;
    case "ticket": {
      const { escala = 0.8, x = 0, y = 0, ...r } = e;
      return (
        <>
          <Escala x={x} y={y} escala={escala}>
            <Ticket {...r} x={0} y={0} />
          </Escala>
          <Som nome="ding" em={(e.entrada ?? 0) + 900} relDb={SOM.ding} refLufs={refLufs} />
        </>
      );
    }
    case "bilhete": {
      const { escala = 0.8, x = 0, y = 0, ...r } = e;
      return (
        <>
          <Escala x={x} y={y} escala={escala}>
            <Bilhete {...r} x={0} y={0} />
          </Escala>
          <Som nome="clique" em={(e.entrada ?? 0) + 240} relDb={SOM.clique} refLufs={refLufs} />
        </>
      );
    }
    case "print":
      return <PrintSite {...e} />;
    case "mapa":
      return <MapaRota arquivo={e.arquivo} ini={e.ini} fim={e.fim} desenho={e.desenho} refLufs={refLufs} />;
    case "telafinal":
      return <TelaFinal ini={e.ini} proximo={e.proximo} refLufs={refLufs} />;
    case "guia":
      return <GuiaNarracao frases={e.frases} inicio={e.inicio} fim={e.fim} />;
    default:
      return null;
  }
};

/** A transição Página toca a folha virando no corte. */
const SonsPagina: React.FC<{ trechos: Trecho[]; refLufs: number }> = ({ trechos, refLufs }) => (
  <>
    {trechos
      .filter((t) => t.pagina)
      .map((t) => (
        <Som key={`pg${t.ate}`} nome="pagina" em={t.ate} relDb={VOLUME_PAGINA_DB} refLufs={refLufs} />
      ))}
  </>
);

export const VideoLongo: React.FC<PropsVideoLongo> = (p) => {
  const fundo = p.eventos.filter((e) => e.tipo === "telafinal");
  const resto = p.eventos.filter((e) => e.tipo !== "telafinal" && e.tipo !== "guia");
  const guia = p.eventos.filter((e) => e.tipo === "guia");
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {fundo.map((e, i) => (
        <UmEvento key={`tf${i}`} e={e} refLufs={p.refLufs} />
      ))}
      <CamadaBase p={p} />
      {resto.map((e, i) => (
        <UmEvento key={`ev${i}`} e={e} refLufs={p.refLufs} />
      ))}
      <SonsPagina trechos={p.trechos} refLufs={p.refLufs} />
      <Grao />
      {guia.map((e, i) => (
        <UmEvento key={`g${i}`} e={e} refLufs={p.refLufs} />
      ))}
    </AbsoluteFill>
  );
};
