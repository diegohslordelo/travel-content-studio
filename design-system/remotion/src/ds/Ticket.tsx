/**
 * Selo SURPREENDE, o Ticket (DS V2, 2.3). Ingresso de papel com entalhes laterais, picote, canhoto com
 * estrela amarela e microcopy em Plex Mono. Variantes: SURPREENDE · SABIA? (2.6, sem estrela, "?" no
 * canhoto) · VALE. (canhoto com ✓ verde).
 * Assinatura SUBIDA: sobe de +260 px com ease-arrive, assenta, brilho de foil (440–900 ms), furo da
 * estrela aos 900 ms (0 → 1,15 → 1 em 160 ms) com 4 raios de 24 px. Glow amarelo 300 na permanência.
 */
import React from "react";
import { Fibra } from "./material";
import { Estrela, Interrogacao } from "./icones";
import { kf, useMs } from "./tempo";
import { COR, DUR, EASE, EFEITO, FONTE, RAIO, ROT, rgba } from "./tokens";

export type TicketProps = {
  variante?: "surpreende" | "sabia" | "vale";
  palavra?: string;
  micro?: string;
  x?: number;
  y?: number;
  entrada?: number;
  saida?: number;
};

const ENTALHE = 28;

export const Ticket: React.FC<TicketProps> = ({ variante = "surpreende", palavra, micro = "ACIMA DA EXPECTATIVA · DIA 1", x = 300, y = 900, entrada = 0, saida }) => {
  const agora = useMs();
  const t = agora - entrada;
  const ts = saida === undefined ? -Infinity : agora - saida;
  if (t < 0 || ts >= DUR.base) return null;
  const texto = palavra ?? (variante === "vale" ? "VALE." : variante === "sabia" ? "SABIA?" : "SURPREENDE");
  const curta = variante === "sabia"; // Subida curta (2.6)
  const fimSubida = curta ? 240 : 320;
  const fimAssenta = curta ? 330 : 440;

  const yy = kf(t, [0, fimSubida, fimAssenta], [260, -8, 0], [EASE.arrive, EASE.out]) + kf(ts, [0, DUR.base], [0, -120], EASE.exit);
  const esc = kf(t, [0, fimSubida, fimAssenta], [0.9, 1.03, 1], [EASE.arrive, EASE.out]);
  const rot = kf(t, [0, fimSubida, fimAssenta], [0, 5, ROT.ticket], [EASE.arrive, EASE.out]);
  const opac = kf(t, [0, 120], [0, 1], EASE.out) * kf(ts, [0, DUR.base], [1, 0], EASE.exit);
  const ergue = kf(t, [0, fimSubida, fimAssenta], [0, 1, 0], [EASE.out, EASE.out]);
  const foil = kf(t, [fimAssenta, 900], [0, 1], EASE.cinema);
  const furo = kf(t, [900, 900 + 112, 900 + DUR.fast], [0, 1.15, 1], [EASE.arrive, EASE.out]);
  const raio = kf(t, [900, 1100], [0, 1], EASE.out);
  const glow = kf(t, [900, 1500], [0, EFEITO.glow], EASE.out);

  // shadow-paper em repouso → shadow-lift no ápice. drop-shadow, porque a máscara dos entalhes corta box-shadow.
  const sombra = `drop-shadow(0 1px 1px rgba(0,0,0,${0.2 * (1 - ergue)})) drop-shadow(0 ${14 + 14 * ergue}px ${13 + 12 * ergue}px rgba(0,0,0,${0.42 + 0.13 * ergue}))`;
  const mascara = `radial-gradient(circle ${ENTALHE}px at left center, transparent 97%, #000) left / 51% 100% no-repeat, radial-gradient(circle ${ENTALHE}px at right center, transparent 97%, #000) right / 51% 100% no-repeat`;

  const canhoto = (() => {
    if (variante === "sabia") return <Interrogacao tamanho={72} cor={COR.grafite} />;
    if (variante === "vale")
      return (
        <svg viewBox="0 0 100 100" width={80} height={80} aria-hidden style={{ scale: String(furo) }}>
          <path d="M18 54l22 22 44-52" fill="none" stroke={COR.verde} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    return (
      <div style={{ position: "relative", width: 72, height: 72 }}>
        <Estrela tamanho={72} cor={COR.amarelo} contorno={COR.grafite} style={{ scale: String(furo) }} />
        {raio > 0 && raio < 1 &&
          [45, 135, 225, 315].map((a) => (
            <i
              key={a}
              style={{
                position: "absolute",
                left: 36 - 3,
                top: 36 - 12,
                width: 6,
                height: 24,
                borderRadius: 3,
                background: COR.amarelo,
                opacity: 1 - raio,
                transform: `rotate(${a}deg) translateY(${-40 - 38 * raio}px)`,
              }}
            />
          ))}
      </div>
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
        scale: String(esc),
        opacity: opac,
        filter: sombra,
      }}
    >
      {variante !== "sabia" && glow > 0 && (
        <div
          style={{
            position: "absolute",
            inset: -EFEITO.glowRaio,
            borderRadius: 40,
            background: `radial-gradient(closest-side, ${rgba(COR.amarelo300, 1)}, ${rgba(COR.amarelo300, 0)})`,
            opacity: glow,
            zIndex: -1,
          }}
        />
      )}
      <div
        style={{
          position: "relative",
          display: "flex",
          background: COR.papel,
          borderRadius: RAIO.papel,
          overflow: "hidden",
          color: COR.grafite,
          WebkitMask: mascara,
          mask: mascara,
        }}
      >
        <Fibra semente={9} />
        {foil > 0 && foil < 1 && (
          <span
            style={{
              position: "absolute",
              top: "-30%",
              bottom: "-30%",
              left: 0,
              width: "40%",
              background: `linear-gradient(100deg, ${rgba(COR.amarelo300, 0)}, ${rgba(COR.amarelo300, 0.9)} 50%, ${rgba(COR.amarelo300, 0)})`,
              transform: `translateX(${-160 + foil * 480}%) skewX(-14deg)`,
              mixBlendMode: "multiply",
              opacity: 0.55,
            }}
          />
        )}
        <div style={{ padding: "30px 34px 32px 62px" }}>
          <div style={{ fontFamily: FONTE.mono, fontWeight: 500, fontSize: 28, lineHeight: 1, letterSpacing: "0.06em", color: COR.asfalto, textTransform: "uppercase", whiteSpace: "nowrap" }}>
            {micro}
          </div>
          <div style={{ fontFamily: FONTE.display, fontStyle: "italic", fontWeight: 800, fontSize: 96, lineHeight: 0.9, letterSpacing: "0.01em", textTransform: "uppercase", marginTop: 14, whiteSpace: "nowrap" }}>
            {texto}
          </div>
        </div>
        <div
          style={{
            width: 150,
            flex: "none",
            display: "grid",
            placeItems: "center",
            marginRight: 30,
            // picote: furos de 6 px a cada 16 px (1.6)
            backgroundImage: `radial-gradient(circle 3px, ${COR.concreto} 98%, transparent)`,
            backgroundSize: "6px 16px",
            backgroundRepeat: "repeat-y",
            backgroundPosition: "0 0",
          }}
        >
          {canhoto}
        </div>
      </div>
    </div>
  );
};
