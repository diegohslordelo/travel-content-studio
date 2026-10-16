/**
 * Amostra do fim do vídeo longo (16:9): placa de fechamento + Nascer do 1º sobre a última cena, a cena vira
 * como página e revela a tela final de 20 s. Clipe real de Amsterdam; assets em `reels/amostra-yt/public`.
 */
import React from "react";
import { Video } from "@remotion/media";
import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import { Placa } from "../ds/Placa";
import { Grao } from "../ds/material";
import { Som } from "../ds/Som";
import { SOM, YT } from "../ds/tokens";
import { DUR_PAGINA, LOWER_BASE, TelaFinal, VOLUME_PAGINA_DB, VirarPagina } from "./Objetos16x9";

const REF = -16;
const VIRA = 6000; // ms: a última cena vira e revela a tela final
export const DUR_AMOSTRA_FIM = VIRA + 20000;

export const AmostraFimYT: React.FC = () => {
  const { fps } = useVideoConfig();
  const q = (ms: number) => Math.round((ms * fps) / 1000);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <TelaFinal ini={VIRA} proximo="bruxelas" refLufs={REF} />
      <Sequence durationInFrames={q(VIRA + DUR_PAGINA)} name="última cena">
        <VirarPagina corte={VIRA}>
          <AbsoluteFill>
            <Video src={staticFile("clipes/IMG_1418.mp4")} trimBefore={q(2000)} objectFit="cover" style={{ width: "100%", height: "100%" }} volume={0.8} />
          </AbsoluteFill>
          <Placa rotulo="E ISSO FOI SÓ O" destino="PRIMEIRO DIA." modulo="um" tamanho="M" x={YT.margemTitulo} y={LOWER_BASE - 166} entrada={1200} />
          <Grao />
        </VirarPagina>
      </Sequence>
      <Som nome="clack" em={1200 + 280} relDb={SOM.clack} refLufs={REF} />
      <Som nome="pagina" em={VIRA} relDb={VOLUME_PAGINA_DB} refLufs={REF} />
    </AbsoluteFill>
  );
};
