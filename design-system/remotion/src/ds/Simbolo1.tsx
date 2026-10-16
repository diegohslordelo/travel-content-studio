/**
 * Símbolo 1º com a assinatura NASCER (DS V2, 4.3): o sol amarelo sobe de trás da linha do
 * horizonte (o traço do ordinal) e o "1" aparece ao lado. 700 ms, ease-cinema.
 * Desenho da implementação de prévia (pd-bundle.js, função one()).
 */
import React, { useId } from "react";
import { kf } from "./tempo";
import { COR, DUR, EASE } from "./tokens";

type Props = {
  altura: number;
  /** ms desde o início do Nascer. Use Infinity para o símbolo estático. */
  t: number;
  corNumero?: string;
  corSol?: string;
};

export const Simbolo1: React.FC<Props> = ({ altura, t, corNumero = COR.grafite, corSol = COR.amarelo }) => {
  const id = `c${useId().replace(/:/g, "")}`;
  const sol = kf(t, [0, DUR.cinema], [36, 0], EASE.cinema);
  const traco = kf(t, [0, 300], [0, 1], EASE.out);
  const numOpac = kf(t, [500, 500 + DUR.base], [0, 1], EASE.out);
  const numY = kf(t, [500, 500 + DUR.base], [10, 0], EASE.out);
  return (
    <svg viewBox="0 0 100 100" height={altura} width={altura} style={{ overflow: "visible", display: "block" }} aria-label="1º">
      <clipPath id={id}>
        <rect x={50} y={-20} width={60} height={58} />
      </clipPath>
      <path fill={corNumero} opacity={numOpac} transform={`translate(0 ${numY})`} d="M26 4h22v96H26V30l-14 7V16z" />
      <g clipPath={`url(#${id})`}>
        <circle cx={76} cy={17 + sol} r={15} fill={corSol} />
      </g>
      <rect x={58.7} y={38} width={34.5 * traco} height={5.5} fill={corSol} />
    </svg>
  );
};
