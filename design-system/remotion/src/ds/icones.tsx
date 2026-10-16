/**
 * Ícones desenhados (DS V2, 1.2: "Seta, ✓, ✗ e ! são desenhados, nunca digitados").
 * Traçados da implementação de prévia (pd-bundle.js), em viewBox 100 × 100.
 */
import React from "react";

type P = { tamanho: number; cor: string; style?: React.CSSProperties };

/** Seta de placa: haste + ponta triangular cheia, sempre para a direita (1.6). */
export const Seta: React.FC<P> = ({ tamanho, cor, style }) => (
  <svg viewBox="0 0 100 100" width={tamanho} height={tamanho} style={style} aria-hidden>
    <path fill={cor} d="M8 41h50V18l38 32-38 32V59H8z" />
  </svg>
);

/** "?" desenhado: módulo da variante Hook (2.1). Mesmo peso de traço do ✗. */
export const Interrogacao: React.FC<P> = ({ tamanho, cor, style }) => (
  <svg viewBox="0 0 100 100" width={tamanho} height={tamanho} style={style} aria-hidden>
    <path
      d="M31 32C31 18 41 10 52 10C64 10 72 18 72 29C72 41 62 45 56 51C52 55 51 59 51 66"
      fill="none"
      stroke={cor}
      strokeWidth={16}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx={51} cy={87} r={9} fill={cor} />
  </svg>
);

/** ✗ (vermelho sobre papel no módulo "Não faça"; PULA). */
export const Xis: React.FC<P> = ({ tamanho, cor, style }) => (
  <svg viewBox="0 0 100 100" width={tamanho} height={tamanho} style={style} aria-hidden>
    <path d="M22 22l56 56M78 22L22 78" fill="none" stroke={cor} strokeWidth={16} strokeLinecap="round" />
  </svg>
);

/** Triângulo com "!" do Carimbo PERRENGUE (2.2). */
export const Alerta: React.FC<P> = ({ tamanho, cor, style }) => (
  <svg viewBox="0 0 100 90" width={tamanho} height={tamanho * 0.9} style={style} aria-hidden>
    <path fill="none" stroke={cor} strokeWidth={9} strokeLinejoin="round" d="M50 7L94 84H6z" />
    <rect x={45} y={30} width={10} height={30} rx={3} fill={cor} />
    <circle cx={50} cy={70} r={6} fill={cor} />
  </svg>
);

/** Estrela do Ticket: amarela com contorno grafite de 3 px no tamanho de 72 px (2.3). */
export const Estrela: React.FC<P & { contorno: string }> = ({ tamanho, cor, contorno, style }) => (
  <svg viewBox="0 0 100 100" width={tamanho} height={tamanho} style={style} aria-hidden>
    <path
      fill={cor}
      stroke={contorno}
      strokeWidth={(3 / tamanho) * 100 * 1.4}
      strokeLinejoin="round"
      d="M50 6l12.6 28.6 31 3.2-23.3 20.7 6.7 30.5L50 73.4 23 89l6.7-30.5L6.4 37.8l31-3.2z"
    />
  </svg>
);

/** Relógio do Placar (pictograma 32 px, 2.5). */
export const Relogio: React.FC<P> = ({ tamanho, cor, style }) => (
  <svg viewBox="0 0 40 40" width={tamanho} height={tamanho} style={style} aria-hidden>
    <circle cx={20} cy={20} r={16} fill="none" stroke={cor} strokeWidth={4} />
    <path d="M20 10v11l7 5" fill="none" stroke={cor} strokeWidth={4} strokeLinecap="round" />
  </svg>
);
