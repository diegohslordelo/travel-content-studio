/**
 * Primeiro Dia · DS V2 em Remotion.
 * - Kit-animacoes / Kit-png: objetos, assinaturas, legendas e transições do DS (exportáveis com alfa).
 * - Catalogo: todas as animações em sequência, com os sons da 4.6.
 * - Reel / CapaReel: montagem de um Reel a partir de reels/<reel>/revN (props + --public-dir).
 * - ReelSocotra: Reel de Socotra em tela dividida (reels/socotra/revN, props + --public-dir).
 * - AmostraYT: amostra de 30 s dos grafismos do vídeo longo do YouTube (16:9), --public-dir=reels/amostra-yt/public.
 */
import React from "react";
import { Composition, Still } from "remotion";
import { carregarFontes } from "./ds/fontes";
import { KitComposicoes } from "./kit/Kit";
import { CapaReel, Reel, metadadosReel, propsVazias } from "./reel/Reel";
import { ReelSocotra, metadadosSocotra, propsVaziasSocotra } from "./socotra/Socotra";
import { carregarFontesSocotra } from "./socotra/estilo";
import { AmostraYT } from "./yt/AmostraYT";
import { AmostraFimYT, DUR_AMOSTRA_FIM } from "./yt/AmostraFimYT";

carregarFontes();
carregarFontesSocotra();

export const RemotionRoot: React.FC = () => (
  <>
    <KitComposicoes />
    <Composition id="Reel" component={Reel} durationInFrames={30} fps={30} width={1080} height={1920} defaultProps={propsVazias} calculateMetadata={metadadosReel} />
    <Composition id="ReelSocotra" component={ReelSocotra} durationInFrames={30} fps={30} width={1080} height={1920} defaultProps={propsVaziasSocotra} calculateMetadata={metadadosSocotra} />
    <Composition id="AmostraYT" component={AmostraYT} durationInFrames={900} fps={30} width={1920} height={1080} />
    <Composition id="AmostraFimYT" component={AmostraFimYT} durationInFrames={Math.round((DUR_AMOSTRA_FIM * 30) / 1000)} fps={30} width={1920} height={1080} />
    <Still id="CapaReel" component={CapaReel} width={1080} height={1920} defaultProps={propsVazias} />
  </>
);
