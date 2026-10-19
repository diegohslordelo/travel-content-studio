/**
 * Tela de Stories 1080 × 1920 (DS V2, 5.6), a partir de stories/<sequência>/revN/revN.json.
 * Fundo (fotograma do acervo), Placa na posição do 9:16 (x 72 · y 640), legenda Padrão com scrim e
 * Bilhete na zona de objeto. Interações (caixa de pergunta, enquete) são figurinhas nativas do
 * Instagram: a tela só deixa o espaço livre.
 *
 * Renderize o quadro 45 (1,5 s): legenda e bilhete já assentados, placa estática.
 */
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Bilhete } from "../ds/Bilhete";
import { LegendaPadrao } from "../ds/Legendas";
import { Grao, ScrimBase } from "../ds/material";
import { Modulo, Placa } from "../ds/Placa";

export type PropsStory = {
  fundo: string;
  placa?: { rotulo?: string; destino: string; modulo?: Modulo; tamanho?: "G" | "M" | "P" };
  /** Legenda Padrão (linhas separadas por "|"; *palavra* = Destaque). */
  legenda?: string;
  bilhete?: { texto: string; x: number; y: number; marca?: "vale" | "pula" | "circulo" };
  /** y da base da legenda; padrão 1420 (3.1). Nos Stories pode descer até 1600 (1.3: base segura de 320 px). */
  legendaBaseY?: number;
};

export const propsStoryVazias: PropsStory = { fundo: "" };

export const Story: React.FC<PropsStory> = ({ fundo, placa, legenda, bilhete, legendaBaseY = 1420 }) => (
  <AbsoluteFill style={{ background: "#000" }}>
    {fundo && <Img src={staticFile(fundo)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
    {legenda && <ScrimBase />}
    {placa && <Placa {...placa} entrada={null} />}
    {bilhete && <Bilhete texto={bilhete.texto} marca={bilhete.marca} x={bilhete.x} y={bilhete.y} entrada={-10000} />}
    {legenda && (
      <LegendaPadrao
        grupos={[{ texto: legenda, ini: 0, fim: 600000, palavras: legenda.split(/[\s|]+/).filter(Boolean).map(() => 0) }]}
        modo="grupo"
        base={1920 - legendaBaseY}
      />
    )}
    <Grao />
  </AbsoluteFill>
);
