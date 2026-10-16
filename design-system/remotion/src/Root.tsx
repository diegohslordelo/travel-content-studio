/**
 * Primeiro Dia · DS V2 em Remotion.
 * - Kit-animacoes / Kit-png: objetos, assinaturas, legendas e transições do DS (exportáveis com alfa).
 * - Catalogo: todas as animações em sequência, com os sons da 4.6.
 * - Reel / CapaReel: montagem de um Reel a partir de reels/<reel>/revN (props + --public-dir).
 */
import React from "react";
import { Composition, Still } from "remotion";
import { carregarFontes } from "./ds/fontes";
import { KitComposicoes } from "./kit/Kit";
import { CapaReel, Reel, metadadosReel, propsVazias } from "./reel/Reel";

carregarFontes();

export const RemotionRoot: React.FC = () => (
  <>
    <KitComposicoes />
    <Composition id="Reel" component={Reel} durationInFrames={30} fps={30} width={1080} height={1920} defaultProps={propsVazias} calculateMetadata={metadadosReel} />
    <Still id="CapaReel" component={CapaReel} width={1080} height={1920} defaultProps={propsVazias} />
  </>
);
