# QA · Reel "Barcelona em 20 segundos (POV)" · REV3

**O que mudou da REV2 (pedido do Diego):** só a abertura e o fechamento. A montagem (4 planos, cortes, áudio) é a mesma da REV2. A REV2 não foi alterada.

**Arquivo:** `barcelona20s_rev3.mp4` (prévia: `barcelona20s_rev3_previa_leve.mp4`) · 1080 × 1920 · 24 fps · 524 quadros · **21,833 s** · −14,5 LUFS · pico −1,4 dBTP · nenhum objeto parado nas zonas da interface.

## 1. Abertura: `POV: 20s EM / BARCELONA →`

| Item | Valor | Fonte |
|---|---|---|
| Variante | Abertura: rótulo + destino + módulo de seta | DS 2.1 (modelo `PRIMEIRO DIA EM / ROMA`) |
| Por que duas linhas | 21 caracteres não cabem numa linha; acima de 16 letras o DS manda abreviar | DS 2.1, Anatomia |
| Rótulo | `POV: 20s EM`, Barlow Condensed 600, 36 px, +8% | DS 1.2 Label |
| Destino | `BARCELONA`, Barlow Condensed 800, 128 px, +0,5% | DS 1.2 H1 |
| "20s" | "s" minúsculo, como o Diego escreveu ("20S" se leria como "anos 20") | Exceção registrada |
| Medidas | 849 × 219 px (face 630 + módulo 219), x 72 · y 640 (até y 859); padding 28 × 36, entrelinha de 12 px | DS 2.1 + bundle |
| Movimento | Chegada (assenta em 400 ms, módulo sai de trás da face, empurrão da seta, brilho de esmalte); sai pela direita até 2,00 s | DS 2.1 |

## 2. Fechamento: módulo 1º com Chegada + Nascer

O símbolo solto da REV2 não seguia o DS. No vídeo, o DS define o 1º como "sol amarelo sobre grafite" (2.1, variante Fechamento), nascendo no módulo (4.3). O kit tem esse módulo sozinho: `PD_placa_modulo_1.png`, "Módulo com símbolo 1º, 176 × 176" (6.1). Sobre os churros, o sol solto sumia, e a animação não se percebia.

| Tempo no Reel | Quadros | O que acontece |
|---|---|---|
| 19,83–20,23 s | 476–485 | **Chegada:** o módulo grafite 176 × 176 entra pela esquerda (−3°, desfoque), passa 24 px e assenta em x 72 · y 640 |
| 20,23–20,93 s | 486–502 | **Nascer** (700 ms, `ease-cinema`): o sol amarelo sobe de trás da linha do horizonte (a barra do ordinal), e a barra cresce da esquerda em 300 ms |
| 20,73–20,97 s | 497–502 | O "1" (papel `#FCFBF8`) sobe 10 px e aparece em 240 ms |
| 20,97–21,83 s | 503–523 | Parado |
| 21,83 s → 0 s | — | Corte seco para o início (loop) |

O 1º usa o desenho do bundle (`one()`, 70% do módulo); o painel usa o material do DS (grafite 900, filete claro e `shadow-plate`). Sem texto, sem @, sem CTA.

**Decisão a registrar no DS:** sozinho, o módulo tem os 4 cantos arredondados (`radius-plate` 16). Na placa, só os da direita são arredondados, porque o lado esquerdo encosta na face.

## 3. O que ficou igual à REV2

Ruas (IMG_0702, 7,5 s) → metrô (IMG_0493, inteiro) → sax (IMG_0952, inteiro) → churros (IMG_1221, inteiro). 3 cortes secos, áudio ambiente equilibrado, grão 5%, sem scrim. Preset PD Chegada v1: continua sem valores no repositório.
