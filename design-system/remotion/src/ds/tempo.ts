/**
 * Tempo em ms (DS V2, 6.2: "tempo manda, quadro converte").
 * Os componentes calculam tudo em ms a partir do quadro atual, então funcionam em qualquer FPS.
 */
import { useCurrentFrame, useVideoConfig } from "remotion";

export type Curva = (t: number) => number;

/** ms desde o início da Sequence atual. */
export const useMs = (): number => {
  const quadro = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (quadro * 1000) / fps;
};

export const quadros = (ms: number, fps: number): number => Math.round((ms * fps) / 1000);

/**
 * Keyframes por segmento: `kf(t, [0, 280, 400], [-1100, 24, 0], [EASE.out, EASE.out])`.
 * Cada segmento tem a própria curva (como as receitas do CapCut, 6.2). Fora do intervalo, trava.
 */
export const kf = (t: number, ms: number[], valores: number[], curvas?: Curva | Curva[]): number => {
  if (t <= ms[0]) return valores[0];
  const ultimo = ms.length - 1;
  if (t >= ms[ultimo]) return valores[ultimo];
  let i = 0;
  while (i < ultimo - 1 && t >= ms[i + 1]) i++;
  const p = (t - ms[i]) / (ms[i + 1] - ms[i]);
  const curva = Array.isArray(curvas) ? curvas[i] : curvas;
  const e = curva ? curva(p) : p;
  return valores[i] + (valores[i + 1] - valores[i]) * e;
};

/** dB → ganho linear. */
export const db = (valor: number): number => Math.pow(10, valor / 20);
