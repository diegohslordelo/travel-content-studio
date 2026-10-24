/**
 * Thumbnail do vídeo longo do YouTube (DS V2, 5.5): 1280 × 720.
 * Fórmula: lugar (placa) + emoção (rosto) + prova (Recibo com o total). Frame real com contraste +10, Placa
 * pequena (75%) no canto superior esquerdo com margem 48, 1 objeto da história, no máximo 4 palavras de texto.
 */
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { COR } from "../ds/tokens";
import { Placa } from "../ds/Placa";
import { Recibo, ReciboProps } from "../ds/Cards";

export type PropsThumbYT = {
  /** arquivo da foto na pasta pública */
  foto: string;
  /** largura da foto no quadro de 1280 px, e deslocamento do canto superior esquerdo da foto */
  fotoLargura: number;
  fotoX: number;
  fotoY: number;
  rotulo: string;
  destino: string;
  recibo: Omit<ReciboProps, "ini" | "fim" | "x" | "y" | "som">;
  reciboX: number;
  reciboY: number;
  reciboEscala: number;
};

export const propsThumbVazias: PropsThumbYT = {
  foto: "",
  fotoLargura: 1280,
  fotoX: 0,
  fotoY: 0,
  rotulo: "",
  destino: "",
  recibo: { lugar: "", cabecalho: "", linhas: [], total: "", real: "", rodape: "" },
  reciboX: 0,
  reciboY: 0,
  reciboEscala: 1,
};

export const ThumbYT: React.FC<PropsThumbYT> = (p) => (
  <AbsoluteFill style={{ background: COR.grafite, overflow: "hidden" }}>
    <Img
      src={staticFile(p.foto)}
      style={{ position: "absolute", left: p.fotoX, top: p.fotoY, width: p.fotoLargura, filter: "contrast(1.1)" }}
    />
    {/* scrim grafite de apoio à placa e ao recibo (DS 1.4: grafite 15–20% da peça) */}
    <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(18,19,23,.42) 0%, rgba(18,19,23,0) 36%, rgba(18,19,23,0) 62%, rgba(18,19,23,.38) 100%)" }} />
    <div style={{ position: "absolute", left: p.reciboX, top: p.reciboY, transformOrigin: "top left", transform: `scale(${p.reciboEscala})` }}>
      <Recibo {...p.recibo} ini={-10000} fim={10000000} x={0} y={0} som={false} />
    </div>
    <Placa rotulo={p.rotulo} destino={p.destino} tamanho="M" x={48} y={48} entrada={null} />
  </AbsoluteFill>
);
