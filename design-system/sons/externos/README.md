# Sons externos (transições)

Efeitos de **transição** baixados em 28/10/2026 da biblioteca oficial do Remotion (`@remotion/sfx`, https://www.remotion.dev/docs/sfx) e versões processadas deles. Pedido do Diego: sons de transição "mais marcantes" e kit profissional (28/10/2026). Os sons da marca (`PD_*_v1.wav`, um nível acima) continuam sendo os sons dos objetos do DS V2.

**Ninguém ouviu estes arquivos.** O Claude não escuta áudio: duração e pico foram medidos com ffmpeg. A escuta é do Diego (CLAUDE.md, 12).

## Originais (CC0, sem atribuição obrigatória)

| Arquivo | Origem | Autor · licença | Duração |
|---|---|---|---|
| `remotion_whip.wav` | `@remotion/sfx` `whip` | JW_Audio, freesound.org/s/838766 · CC0 | 0,17 s |
| `remotion_whoosh.wav` | `@remotion/sfx` `whoosh` | 1bob, freesound.org/s/831936 · CC0 | 0,15 s |
| `remotion_page-turn.wav` | `@remotion/sfx` `pageTurn` | kenney.nl ("Draw Knife 1") · CC0 | 0,40 s |
| `remotion_shutter-modern.wav` | `@remotion/sfx` `shutterModern` | ristooooo1, freesound.org/s/539136 · CC0 | 0,49 s |
| `remotion_shutter-old.wav` | `@remotion/sfx` `shutterOld` | hmilleo, freesound.org/s/409093 · CC0 | 0,31 s |
| `remotion_mouse-click.wav` | `@remotion/sfx` `mouseClick` | Pixeliota, freesound.org/s/678248 · CC0 | — |

Ficaram de fora os sons do pacote sem licença livre declarada (`ding`, `recordScratch`) e os de meme (`vineBoom`, `bruh` etc.), que não combinam com a marca.

## Processados (`PDX_*`, 48 kHz mono, pico −1 dBFS)

Feitos com ffmpeg a partir dos originais acima (e uma senoide de 55 Hz no impacto). Mesma licença (CC0).

| Arquivo | Feito de | Uso pensado |
|---|---|---|
| `PDX_swish.wav` | whip | Chicote rápido: Arrasto, corte por correspondência com movimento |
| `PDX_riser.wav` | whoosh invertido, esticado, com eco | Sobe **até** o corte: antes da virada ou da revelação (termina no quadro do corte) |
| `PDX_ar_longo.wav` | whoosh lento, sem graves, com cauda | Mergulho (zoom através), fusão de fundo |
| `PDX_impacto.wav` | whip em tom mais grave + sub de 55 Hz | Data, número ou revelação em tela cheia |
| `PDX_pagina.wav` | page-turn | Dissolve de foto, voltar no tempo |
| `PDX_obturador.wav` | shutter-modern | Snap, print, captura real |

Volumes de uso: `docs/REFERENCIA_EDICAO_FORMATOS.md`, seção 4.

## Som do fim do gancho (`keen`)

Pedido do Diego (01/11/2026): **em todo vídeo, o `keen` toca no fim do gancho** (regra no CLAUDE.md, seção 7).

| Arquivo | O que é |
|---|---|
| `keen_original.m4a` | Áudio original, copiado sem recompressão do vídeo que o Diego enviou (`copy_00072611-1662-4A2A-9675-0A1FA2F768C2.mov`, 4,16 s, AAC 44,1 kHz estéreo) |
| `keen.wav` | O trecho útil (0,10–1,85 s do original), 48 kHz mono, pico −1 dBFS. **1,75 s**: sobe de forma contínua, chega ao **pico em 0,96 s** e cai em ≈ 0,8 s |

**Como usar:** alinhar o **pico** (0,96 s do arquivo) no corte entre o gancho e a cena seguinte; a subida fica sob o fim da frase do gancho. Volume de trabalho: −6 dB da voz (o de transição, `docs/REFERENCIA_EDICAO_FORMATOS.md`, 4.1), a calibrar na escuta.

**Origem e licença:** o Diego enviou o som; a origem e a licença não foram informadas. **Ninguém ouviu** o arquivo pelo repositório: duração e pico foram medidos com ffmpeg.
