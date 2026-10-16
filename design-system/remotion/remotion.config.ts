/**
 * Primeiro Dia · Remotion (DS V2).
 * Opções da CLI. Quem renderiza pela API Node passa as opções direto.
 * https://remotion.dev/docs/config
 */
import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(95);
Config.setOverwriteOutput(true);
Config.setDefaultPremountInSeconds(2);
// FPS de produção ainda não definido no DS (pendência 5): as composições usam 30 fps,
// o FPS das receitas do DS (6.2). Os tempos dos componentes estão em ms.
