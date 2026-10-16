/**
 * Amostra de 30 s dos grafismos do vídeo longo (16:9), sobre clipes reais de Amsterdam (dia 1, 12/03).
 * Serve só para o Diego aprovar o visual e o som: os valores do Recibo e do Placar são de EXEMPLO
 * (os custos reais ainda não chegaram). Assets em `reels/amostra-yt/public` (--public-dir).
 */
import React from "react";
import { Video } from "@remotion/media";
import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import { Placa, LIKE_APERTA, LIKE_INSCRITO } from "../ds/Placa";
import { Placar } from "../ds/Placar";
import { Recibo } from "../ds/Cards";
import { Grao } from "../ds/material";
import { Som } from "../ds/Som";
import { SOM, YT } from "../ds/tokens";
import { ChamadaInstagram, DUR_PAGINA, EtiquetaLugar, LOWER_BASE, MapaRota, VOLUME_PAGINA_DB, VirarPagina } from "./Objetos16x9";

const REF = -16; // loudness de referência da voz (LUFS) para os volumes da 4.6

/** `pagina`: a cena sai virando como página (troca de dia), por cima da cena seguinte. */
type Clipe = { arquivo: string; de: number; ate: number; inicio: number; pagina?: boolean };

// ms na linha do tempo da amostra; `inicio` = ms dentro do clipe
const CLIPES: Clipe[] = [
  { arquivo: "clipes/IMG_1375.mp4", de: 0, ate: 4000, inicio: 800, pagina: true },
  { arquivo: "clipes/IMG_1406.mp4", de: 4000, ate: 10000, inicio: 300 },
  { arquivo: "clipes/IMG_1449.mp4", de: 15000, ate: 22000, inicio: 1000 },
  { arquivo: "clipes/IMG_1440.mp4", de: 22000, ate: 30000, inicio: 1500 },
];

const ClipeFundo: React.FC<{ c: Clipe }> = ({ c }) => {
  const { fps } = useVideoConfig();
  const q = (ms: number) => Math.round((ms * fps) / 1000);
  const video = <Video src={staticFile(c.arquivo)} trimBefore={q(c.inicio)} objectFit="cover" style={{ width: "100%", height: "100%" }} volume={0.8} />;
  return (
    <Sequence from={q(c.de)} durationInFrames={q(c.ate - c.de + (c.pagina ? DUR_PAGINA : 0))} name={c.arquivo}>
      {c.pagina ? <VirarPagina corte={c.ate - c.de}>{video}</VirarPagina> : <AbsoluteFill>{video}</AbsoluteFill>}
    </Sequence>
  );
};

export const AmostraYT: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    {/* de trás para a frente: a cena que vira a página fica por cima da seguinte */}
    {[...CLIPES].reverse().map((c) => (
      <ClipeFundo key={c.arquivo} c={c} />
    ))}

    {/* 0:00 marca: Placa de abertura sobre a chegada (DS 5.4) */}
    <Placa rotulo="3 DIAS EM" destino="AMSTERDAM" tamanho="M" x={YT.margemTitulo} y={LOWER_BASE - 166} entrada={300} saida={3000} />
    <Som nome="clack" em={300 + 280} relDb={SOM.clack} refLufs={REF} />

    {/* 0:04 início do dia: transição Página (folha virando) + Placa de capítulo depois que a folha assenta */}
    <Som nome="pagina" em={4000} relDb={VOLUME_PAGINA_DB} refLufs={REF} />
    <Placa rotulo="QUINTA · 12/03" destino="DIA 1" tamanho="M" x={YT.margemTitulo} y={YT.margemTitulo} entrada={4700} saida={6900} />
    <Som nome="clack" em={4700 + 280} relDb={SOM.clack} refLufs={REF} />

    {/* Placar do dia: liga depois que o capítulo sai (mesmo canto), sem som; soma com moeda */}
    <Placar
      x={YT.margemTitulo}
      y={72}
      ligar={7300}
      valores={[
        { em: 7300, tempo: "+02:00", gasto: "€ 0,00" },
        { em: 18000, tempo: "+03:06", gasto: "€ 6,50" },
      ]}
      refLufs={REF}
    />

    {/* lugar */}
    <EtiquetaLugar lugar="DAMRAK" detalhe="CENTRUM · 16H30" ini={6600} fim={9700} />

    {/* 0:10 mapa do dia com a Rota */}
    <MapaRota arquivo="mapa_centro.json" ini={10000} fim={15000} refLufs={REF} />

    {/* 0:15 compra */}
    <EtiquetaLugar lugar="MANNEKEN PIS" detalhe="SPUISTRAAT · 17H36" ini={15400} fim={18800} />
    <div style={{ position: "absolute", left: 1400, top: 150, scale: "0.72", transformOrigin: "0 0" }}>
      <Recibo
        lugar="MANNEKEN PIS"
        cabecalho="DIA 1 · 17H36 · AMSTERDAM"
        linhas={[["Batata frita média", "€ 6,50"]]}
        total="€ 6,50"
        real="valor de exemplo"
        rodape="AMOSTRA · SEM DADOS REAIS"
        ini={18000}
        fim={21400}
        x={0}
        y={0}
        som={false}
      />
    </div>

    {/* 0:22 Instagram (sem som) e chamada de like e inscrição */}
    <ChamadaInstagram ini={22300} fim={25000} />
    <Placa rotulo="DEIXA O LIKE E" destino="SE INSCREVE" modulo="like" tamanho="M" x={YT.margemTitulo} y={LOWER_BASE - 166} entrada={25700} saida={29400} />
    <Som nome="clique" em={25700 + LIKE_APERTA} relDb={SOM.clique} refLufs={REF} />
    <Som nome="ding" em={25700 + LIKE_INSCRITO} relDb={SOM.ding} refLufs={REF} />

    <Grao />
  </AbsoluteFill>
);
