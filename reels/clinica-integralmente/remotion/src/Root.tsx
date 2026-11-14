import { Composition } from "remotion";
import { Rota, DURACAO } from "./Rota";
export const Root = () => (
  <Composition id="Rota" component={Rota} durationInFrames={DURACAO} fps={30} width={1080} height={1920} />
);
