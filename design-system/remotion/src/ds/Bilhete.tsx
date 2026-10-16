/**
 * Bilhete na letra do Diego (DS V2, 2.4): ativo nº 3. Papel, caneta azul 72 px no vídeo, minúsculas,
 * máx. 2 linhas × 22 caracteres, rotação +3° (segundo bilhete −2°).
 * Assinatura ESCRITA: o papel entra de baixo 24 px girando 0 → 3° (ease-arrive, 240 ms); a letra é
 * revelada da esquerda para a direita em 400 ms; ✓/✗ em 200 ms depois do texto; círculo em 280 ms.
 * Saída: desce 40 px e some em 200 ms. Variante Humor: `semPapel` (caneta direto em área calma da cena).
 * Fonte "Caneta Diego" ainda não existe: os tokens caem para Reenie Beanie (provisória).
 */
import React from "react";
import { Fibra } from "./material";
import { kf, useMs } from "./tempo";
import { COR, DUR, EASE, FONTE, RAIO, ROT, SOMBRA } from "./tokens";

export type BilheteProps = {
  /** Linhas separadas por "|" (máx. 2). */
  texto: string;
  marca?: "vale" | "pula" | "circulo";
  segundo?: boolean;
  semPapel?: boolean;
  x?: number;
  y?: number;
  entrada?: number;
  saida?: number;
};

const TAM_VIDEO = 72; // 2.4: Caneta 72 px no vídeo

export const Bilhete: React.FC<BilheteProps> = ({ texto, marca, segundo = false, semPapel = false, x = 520, y = 900, entrada = 0, saida }) => {
  const agora = useMs();
  const t = agora - entrada;
  const ts = saida === undefined ? -Infinity : agora - saida;
  if (t < 0 || ts >= 200) return null;
  const rotFinal = segundo ? -2 : ROT.bilhete;
  const yy = kf(t, [0, DUR.base], [24, 0], EASE.arrive) + kf(ts, [0, 200], [0, 40], EASE.exit);
  const rot = semPapel ? 0 : kf(t, [0, DUR.base], [0, rotFinal], EASE.arrive);
  const opac = kf(t, [0, 80], [0, 1]) * kf(ts, [0, 200], [1, 0], EASE.exit);
  const inicioEscrita = semPapel ? 0 : DUR.base;
  const revela = kf(t, [inicioEscrita, inicioEscrita + DUR.slow], [0, 100], EASE.out);
  const fimTexto = inicioEscrita + DUR.slow;
  const traco = kf(t, [fimTexto, fimTexto + (marca === "circulo" ? 280 : 200)], [0, 1], EASE.out);
  const linhas = texto.split("|");

  const marcaSvg = (() => {
    if (!marca) return null;
    const comum = { position: "absolute" as const, overflow: "visible" as const, fill: "none", strokeWidth: 6, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
    if (marca === "vale")
      return (
        <svg viewBox="0 0 110 110" style={{ ...comum, right: -74, top: -40, width: 110, height: 110 }} stroke={COR.verde}>
          <path d="M22 58l20 22 46-56" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - Math.min(1, traco * 2)} />
          <path d="M55 4C20 4 4 30 6 56s26 50 54 48 46-24 44-52S84 2 50 6" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - Math.max(0, traco * 2 - 1)} />
        </svg>
      );
    if (marca === "pula")
      return (
        <svg viewBox="0 0 100 100" style={{ ...comum, right: -26, top: -30, width: 100, height: 100 }} stroke={COR.vermelho}>
          <path d="M24 24l52 52M76 24L24 76" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - traco} />
        </svg>
      );
    return (
      <svg viewBox="0 0 100 60" preserveAspectRatio="none" style={{ ...comum, left: -18, top: -14, width: "calc(100% + 36px)", height: "calc(100% + 28px)" }} stroke={COR.caneta}>
        <path d="M50 4C20 3 3 14 4 30s22 27 48 26 45-12 44-28S72 2 44 6" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - traco} vectorEffect="non-scaling-stroke" />
      </svg>
    );
  })();

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        translate: `0 ${yy}px`,
        rotate: `${rot}deg`,
        opacity: opac,
        padding: semPapel ? 0 : "24px 32px",
        background: semPapel ? "transparent" : COR.papel,
        borderRadius: RAIO.papel,
        boxShadow: semPapel ? undefined : SOMBRA.papel,
        color: COR.caneta,
        fontFamily: FONTE.caneta,
        fontWeight: 400,
        fontSize: TAM_VIDEO,
        lineHeight: 1.05,
        textTransform: "lowercase",
        whiteSpace: "nowrap",
      }}
    >
      {!semPapel && <Fibra semente={2} />}
      <div style={{ position: "relative", clipPath: `inset(-20% ${100 - revela}% -20% -5%)` }}>
        {linhas.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      {marcaSvg}
    </div>
  );
};
