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

Ficaram de fora os sons do pacote sem licença livre declarada (`ding`, `recordScratch`) e os de meme (`vineBoom`, `bruh` etc.), que não combinam com a marca. Em 02/11/2026, a pedido do Diego, entraram `fah`, `vineBoom` e `ding` (seção "Kit SFX virais", abaixo).

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

## Kit "SFX virais" (02/11/2026)

Pedido do Diego (02/11/2026): baixar todos os sons de um Reel de referência (gravação de tela de `@eu.ilka`, "Comente SONS e te envio os SFXs mais virais", feito com o app Edits) e deixá-los prontos para os vídeos. **Os arquivos do vídeo não foram extraídos** (a fala está por cima de todos e o áudio é de outra criadora): cada som foi buscado na internet pelo nome.

**Transcrição do vídeo de referência** (Whisper large-v3, conferida com a legenda na tela; o Whisper ouviu "Flap" e "a tensão"):

> Use o **Faaah** pra captar atenção, ou também o **Punch**. *[Vine boom: sem fala, só a reação]* Já use o **Magic Reveal** pra revelar algo. Use o **Woosh** pra zoom in e zoom out. E o **Camera Shutter** pra transições rápidas. E o **Ding** é perfeito pra notificação, então já aproveita e me segue.

O rótulo na tela diz "Magic review"; o nome falado e o efeito (brilho dourado) são **Magic Reveal**.

### Originais

| Arquivo | Origem | Autor · licença |
|---|---|---|
| `remotion_fah.wav` | `@remotion/sfx` `fah` (remotion.media/fah.wav), tirado do MyInstants | Taileons (meme) · **sem licença livre declarada** |
| `remotion_vine-boom.wav` | `@remotion/sfx` `vineBoom`, tirado do MyInstants | sem autor · **sem licença livre declarada** |
| `remotion_ding.wav` | `@remotion/sfx` `ding`, tirado do MyInstants | sem autor · **sem licença livre declarada** |
| `kenney_impactPunch_heavy_000.ogg`, `kenney_impactPunch_medium_002.ogg` | Kenney "Impact Sounds" (kenney.nl/assets/impact-sounds) | Kenney · CC0 (`kenney_impact-sounds_License.txt`) |
| `oga_magical_3.ogg`, `oga_magical_5.ogg` | OpenGameArt "Magic Spell SFX" (opengameart.org/content/magic-spell-sfx) | JaggedStone · CC0 |
| `remotion_whoosh.wav`, `remotion_shutter-modern.wav` | já estavam no kit (28/10/2026) | CC0 |

A página do Remotion diz, sobre os três sem licença: "not explicitly released under a free license, but it is probably fine to use given its widespread use". Não é garantia: são áudios de meme sem dono declarado. O Freesound (onde há versões CC0 de *boom* e *ding*) bloqueia o acesso automático daqui.

### Processados (48 kHz mono, pico −1 dBFS, silêncio do início e do fim cortado)

| Som do vídeo | Arquivo | Feito de | Duração | Uso pensado |
|---|---|---|---|---|
| Faaah | `PDX_faaah.wav` | `remotion_fah` | 1,85 s | Grito de "deu ruim": perrengue real, na pausa da fala |
| Punch | `PDX_punch.wav` | Kenney punch heavy 000 | 0,50 s | Soco com corpo: corte seco no gancho, número que pesa |
| Punch (alternativa) | `PDX_punch_seco.wav` | Kenney punch medium 002 | 0,35 s | Soco mais curto e agudo: texto que entra de uma vez |
| Vine boom | `PDX_vine_boom.wav` | `remotion_vine-boom` | 1,14 s | Reação, olhar para a câmera, "como assim?" |
| Magic Reveal | `PDX_magic_reveal.wav` | OGA magical 3 | 1,80 s | Revelação: lugar, preço que surpreende, antes × depois |
| Magic Reveal (alternativa) | `PDX_magic_brilho.wav` | OGA magical 5 | 1,41 s | Brilho mais leve e mais agudo |
| Woosh | `PDX_woosh.wav` | `remotion_whoosh` | 0,12 s | Zoom in e zoom out (o `PDX_ar_longo` continua para o mergulho) |
| Camera Shutter | `PDX_obturador.wav` | já existia | 0,49 s | Transição rápida, foto, print |
| Ding | `PDX_ding.wav` | `remotion_ding` | 1,26 s | Notificação no meio do Reel (mensagem, lembrete, alerta) |

**Limites de uso:**
- Faaah e Vine boom são sons de meme. A personalidade do DS é "bem-humorado (mas não palhaço)" (DS V2, Plataforma). Uso proposto: **no máximo 1 dos dois por Reel**, e só num perrengue ou surpresa que aconteceu de verdade (CLAUDE.md, 9).
- O Faaah é uma voz: nunca por cima da fala do Diego.
- No CTA valem os sons do DS (`PD_*`); o `PDX_ding` não substitui o `PD_ding_v1` ali (CLAUDE.md, 6).
- Continua valendo: no máximo 1 efeito a cada 1,5 s e nada de som em todo corte (`docs/REFERENCIA_EDICAO_FORMATOS.md`, 4.2).

Volumes de uso: `docs/REFERENCIA_EDICAO_FORMATOS.md`, seção 4.
