/**
 * Placar do Dia (DS V2, 2.5): ativo nº 2. Painel grafite com +HH:MM e € gasto, PD Placar 56 px amarelo.
 * Assinatura GIRO: ao ligar, acende em 80 ms com flicker de 1 quadro e os dígitos rolam até o valor
 * (240 ms, ease-out). A cada gasto, só os dígitos que mudam giram (80 ms) e o valor pisca amarelo 300
 * por 1 quadro. Regra de honestidade: sem registro de campo, não há placar.
 */
import React from "react";
import { useVideoConfig } from "remotion";
import { Relogio } from "./icones";
import { kf, useMs } from "./tempo";
import { COR, DUR, EASE, FONTE, RAIO, REEL, SOMBRA, TIPO } from "./tokens";

export type ValorPlacar = { em: number; tempo: string; gasto: string };

const Digito: React.FC<{ antes: string; agora: string; t: number; dur: number; flash: boolean }> = ({ antes, agora, t, dur, flash }) => {
  const p = kf(t, [0, dur], [0, 1], EASE.out);
  const mudou = antes !== agora;
  return (
    <span style={{ display: "inline-block", position: "relative", overflow: "hidden", height: "1em", lineHeight: "1em", verticalAlign: "top" }}>
      <span style={{ display: "block", visibility: "hidden" }}>{agora}</span>
      {mudou && p < 1 && (
        <span style={{ position: "absolute", left: 0, top: 0, translate: `0 ${-p * 100}%` }}>{antes}</span>
      )}
      <span style={{ position: "absolute", left: 0, top: 0, translate: `0 ${mudou ? (1 - p) * 100 : 0}%`, color: flash ? COR.amarelo300 : undefined }}>
        {agora}
      </span>
    </span>
  );
};

const Valor: React.FC<{ seq: string[]; tempos: number[]; t: number; ligar: number }> = ({ seq, tempos, t, ligar }) => {
  const { fps } = useVideoConfig();
  let i = 0;
  while (i < seq.length - 1 && t >= tempos[i + 1]) i++;
  const atual = seq[i].replace(/ /g, "\u00A0");
  const primeiro = i === 0;
  const anterior = primeiro ? atual.replace(/[0-9]/g, "0") : seq[i - 1].replace(/ /g, "\u00A0");
  const desde = t - (primeiro ? ligar : tempos[i]);
  const dur = primeiro ? DUR.base : DUR.tick;
  const flash = !primeiro && desde >= 0 && desde < 1000 / fps && anterior !== atual;
  return (
    <span>
      {atual.split("").map((c, k) => (
        <Digito key={k} antes={anterior[k] ?? c} agora={c} t={desde} dur={dur} flash={flash} />
      ))}
    </span>
  );
};

export const Placar: React.FC<{ valores: ValorPlacar[]; ligar?: number; desligar?: number; x?: number; y?: number }> = ({
  valores,
  ligar = 0,
  desligar,
  x = REEL.seguroEsq,
  y = REEL.placarY,
}) => {
  const t = useMs();
  const { fps } = useVideoConfig();
  if (t < ligar) return null;
  const quadro = 1000 / fps;
  // acende em 80 ms com 1 quadro de flicker
  let opac = kf(t - ligar, [0, DUR.tick], [0, 1]);
  if (t - ligar >= DUR.tick && t - ligar < DUR.tick + quadro) opac = 0.4;
  if (desligar !== undefined) opac *= kf(t - desligar, [0, DUR.tick], [1, 0]);
  const tempos = valores.map((v) => v.em);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        height: 96,
        display: "inline-flex",
        alignItems: "center",
        gap: 22,
        padding: "0 28px",
        background: COR.grafite,
        borderRadius: RAIO.tag,
        boxShadow: `${SOMBRA.placa}, inset 0 0 0 2px rgba(255,255,255,.08)`,
        color: COR.amarelo,
        fontFamily: FONTE.dados,
        fontWeight: 700,
        fontSize: TIPO.data.fontSize,
        lineHeight: 1,
        fontVariantNumeric: "tabular-nums",
        opacity: opac,
      }}
    >
      <Relogio tamanho={32} cor={COR.amarelo} />
      <Valor seq={valores.map((v) => v.tempo)} tempos={tempos} t={t} ligar={ligar} />
      <i style={{ width: 8, height: 8, borderRadius: "50%", background: COR.amarelo, opacity: 0.6 }} />
      <Valor seq={valores.map((v) => v.gasto)} tempos={tempos} t={t} ligar={ligar} />
    </div>
  );
};
