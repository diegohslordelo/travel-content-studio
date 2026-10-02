import {Config} from '@remotion/cli/config';

// Chromium headless já instalado no ambiente (evita download de navegador).
// Em outra máquina, apague esta linha e o Remotion usa o navegador dele.
Config.setBrowserExecutable('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell');
Config.setVideoImageFormat('png');
Config.setConcurrency(4);
// Codifica em BT.709 (matriz e tags). O padrão do Remotion 4 ('default') codificava em BT.601 sem tag, e o
// export marcava como BT.709: pequeno erro de matiz e saturação. Revisão de cor de 02/10/2026.
Config.setColorSpace('bt709');
