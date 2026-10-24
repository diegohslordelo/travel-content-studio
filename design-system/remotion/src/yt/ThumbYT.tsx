/**
 * Thumbnail do vídeo longo do YouTube (DS V2, 5.5): 1280 × 720.
 * Fórmula: lugar (placa) + emoção (rosto) + prova (Recibo com o total). Frame real com contraste +10, Placa
 * pequena (75%) no canto superior esquerdo com margem 48, 1 objeto da história, no máximo 4 palavras de texto.
 */
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { COR, FONTE } from "../ds/tokens";
import { Placa } from "../ds/Placa";
import { Recibo, ReciboProps } from "../ds/Cards";

export type PropsThumbYT = {
  /** arquivo da foto na pasta pública */
  foto: string;
  /** largura da foto no quadro de 1280 px, e deslocamento do canto superior esquerdo da foto */
  fotoLargura: number;
  fotoX: number;
  fotoY: number;
  /** sem `destino`, não há Placa */
  rotulo?: string;
  destino?: string;
  /** sem `recibo`, não há Recibo */
  recibo?: Omit<ReciboProps, "ini" | "fim" | "x" | "y" | "som"> | null;
  /** só o nome, em Condensed 800 amarelo (Display, DS 3.2), no lugar da Placa */
  titulo?: string;
  tituloTamanho?: number;
  reciboX: number;
  reciboY: number;
  reciboEscala: number;
};

export const propsThumbVazias: PropsThumbYT = {
  foto: "",
  fotoLargura: 1280,
  fotoX: 0,
  fotoY: 0,
  recibo: null,
  reciboX: 0,
  reciboY: 0,
  reciboEscala: 1,
};

export const ThumbYT: React.FC<PropsThumbYT> = (p) => (
  <AbsoluteFill style={{ background: COR.grafite, overflow: "hidden" }}>
    <Img
      src={staticFile(p.foto)}
      style={{ position: "absolute", left: p.fotoX, top: p.fotoY, width: p.fotoLargura, filter: "contrast(1.1) brightness(1.18)" }}
    />
    {/* scrim grafite de apoio à placa e ao recibo (DS 1.4: grafite 15–20% da peça) */}
    <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(18,19,23,.42) 0%, rgba(18,19,23,0) 36%, rgba(18,19,23,0) 62%, rgba(18,19,23,.38) 100%)" }} />
    {p.recibo && (
      <div style={{ position: "absolute", left: p.reciboX, top: p.reciboY, transformOrigin: "top left", transform: `scale(${p.reciboEscala})` }}>
        <Recibo {...p.recibo} ini={-10000} fim={10000000} x={0} y={0} som={false} />
      </div>
    )}
    {p.destino && <Placa rotulo={p.rotulo} destino={p.destino} tamanho="M" x={48} y={48} entrada={null} />}
    {p.titulo && (
      <div
        style={{
          position: "absolute",
          left: 48,
          top: 40,
          fontFamily: FONTE.display,
          fontWeight: 800,
          fontSize: p.tituloTamanho ?? 168,
          lineHeight: 0.88,
          letterSpacing: "-0.01em",
          color: COR.amarelo,
          textShadow: "0 3px 0 rgba(0,0,0,.35), 0 0 28px rgba(0,0,0,.5)",
        }}
      >
        {p.titulo}
      </div>
    )}
  </AbsoluteFill>
);
