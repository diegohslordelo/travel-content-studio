/**
 * Sons da marca (DS V2, 4.6) a partir de `design-system/sons/PD_*_v1.wav`.
 * O volume da tabela 4.6 é relativo à voz (ou ao ambiente, em cena sem fala). Os arquivos têm loudness
 * de evento conhecida (sons_v1.json, LUFS K-ponderados em 50 ms), então o ganho é
 *   ganho dB = (loudness de referência da cena + dB relativo da 4.6) − loudness do arquivo.
 * Regras: só nos eventos da 4.6; no máx. 1 efeito a cada 1,5 s; nada em toda palavra de legenda.
 */
import React from "react";
import { Audio } from "@remotion/media";
import { Sequence, useVideoConfig } from "remotion";
import { db, quadros } from "./tempo";
import { SOM } from "./tokens";
import niveis from "../../../sons/sons_v1.json";
import clack from "../../../sons/PD_clack_v1.wav";
import tum from "../../../sons/PD_tum_v1.wav";
import ding from "../../../sons/PD_ding_v1.wav";
import clique from "../../../sons/PD_clique_v1.wav";
import tick from "../../../sons/PD_tick_v1.wav";
import impressora from "../../../sons/PD_impressora_v1.wav";
import obturador from "../../../sons/PD_obturador_v1.wav";
import whoosh from "../../../sons/PD_whoosh_v1.wav";
import nascer from "../../../sons/PD_nascer_v1.wav";
import moeda from "../../../sons/PD_moeda_v1.wav";

export const ARQUIVOS = {
  clack,
  tum,
  ding,
  clique,
  tick,
  impressora,
  obturador,
  whoosh,
  nascer,
  moeda,
} as const;
export type NomeSom = keyof typeof ARQUIVOS;

export const nivelArquivo = (nome: NomeSom): number =>
  (niveis as Record<string, { lufs_50ms: number }>)[`PD_${nome}_v1.wav`]
    .lufs_50ms;

/** Ganho (dB) para o som soar `relDb` abaixo da referência `refLufs`. */
export const ganhoSom = (
  nome: NomeSom,
  relDb: number,
  refLufs: number,
): number => refLufs + relDb - nivelArquivo(nome);

export const Som: React.FC<{
  nome: NomeSom;
  em: number;
  relDb: number;
  refLufs: number;
}> = ({ nome, em, relDb, refLufs }) => {
  const { fps } = useVideoConfig();
  const g = Math.min(1, db(ganhoSom(nome, relDb, refLufs)));
  return (
    <Sequence from={quadros(em, fps)} layout="none" name={`som ${nome}`}>
      <Audio src={ARQUIVOS[nome]} volume={g} />
    </Sequence>
  );
};

/**
 * Evento do Recibo (decisão do Diego, 16/10/2026): sempre que o Recibo aparece, a impressora imprime e a
 * moeda cai quando o total assenta (320 ms depois, o fim da impressão), para dar a sensação de "gastar
 * dinheiro". Conta como UM efeito sonoro, como o ding + furador do Ticket. A moeda usa o volume da linha
 * do Recibo na 4.6 (−14 dB da voz); calibrar depois da escuta.
 */
export const SomRecibo: React.FC<{ em: number; refLufs: number }> = ({
  em,
  refLufs,
}) => (
  <>
    <Som nome="impressora" em={em} relDb={SOM.impressora} refLufs={refLufs} />
    <Som nome="moeda" em={em + 320} relDb={SOM.impressora} refLufs={refLufs} />
  </>
);
