# Padrão dos Reels antigos (medido)

Medido em 26/10/2026 com ffprobe, ffmpeg (`ebur128`, detecção de corte), 1 quadro por segundo (`qa/` não guarda essas folhas; foram geradas no scratchpad) e leitura de pixels em quadros de 1080 × 1920. O projeto de origem do Reel em tela dividida (Remotion `ReelAnneFrank` + `rev2.py`) foi lido e é a **base** deste Reel: a composição `ReelGaudi` (`design-system/remotion/src/gaudi/`) foi feita a partir dele, com os mesmos valores.

## 1. Reels analisados

| Reel | Arquivo | Resolução | qps | Vídeo | Taxa total | Áudio | Duração | Loudness | Pico |
|---|---|---|---:|---|---:|---|---:|---:|---:|
| **Anne Frank REV2** (tela dividida) | `reels/anne-frank/rev2/reel_anne-frank_rev2.mp4` | 1080 × 1920 | 30 | H.264 High, yuvj420p, 20,2 Mb/s | 20,4 Mb/s | AAC-LC 48 kHz estéreo, 240 kb/s | 50,80 s | −14,0 LUFS | −1,9 dBTP |
| Anne Frank REV1 (tela dividida) | `reels/anne-frank/rev1/…_rev1.mp4` | 1080 × 1920 | 30 | H.264 High, 20,2 Mb/s | 20,5 Mb/s | AAC 300 kb/s | 50,40 s | −14,0 LUFS | −1,4 dBTP |
| Casas tortas de Amsterdam REV3 (Diego explicando) | `reels/amsterdam-casas-tortas/rev3/…_rev3.mp4` | 1080 × 1920 | 24 | H.264 High, 28,7 Mb/s | 29,1 Mb/s | AAC 300 kb/s | 26,00 s | −14,1 LUFS | −1,4 dBTP |
| Greves na Europa REV2 (Tela Verde) | `reels/greves-europa/rev2/reel_tela_verde_legenda_baixa.mp4` | 1080 × 1920 | 24 | H.264 High, 10,3 Mb/s | 10,5 Mb/s | AAC 248 kb/s | 29,29 s | −14,0 LUFS | −1,6 dBTP |

**O único Reel em tela dividida do acervo é o Anne Frank** (REV1 e REV2). Os outros dois mostram o Diego explicando em tela cheia e servem de comparação (mesmo master: −14 LUFS, pico ≤ −1 dBTP). Onde eles divergem do Anne Frank (24 qps, legenda do DS), **vale o Anne Frank**, porque o pedido é tela dividida.

## 2. Tela dividida

| Item | Medida | Como foi medido |
|---|---|---|
| Quem fica onde | **Imagem de apoio em cima, Diego embaixo** | Quadros a cada 1 s (13 cenas em tela dividida na REV2) |
| Divisão | **Costura em y 900**: metade de cima 1080 × 900, metade de baixo 1080 × 1020 | Pixels: faixa escura em y 897–902 em todas as cenas medidas; `costura_y: 900` no `rev2.json` |
| Linha entre as metades | **6 px, preto a 55%** (`rgba(0,0,0,0.55)`), y 897–902; sem margem nem moldura | Luminância média da linha: 70–76 contra 109–194 nas linhas vizinhas (4 quadros) |
| Diego na metade de baixo | Vídeo 1080 × 1920 inteiro deslocado para cima, sem escala: o rosto fica a 42% da metade de baixo | `AnneFrank.tsx` (`translate: h·0,42 − rostoY`) e quadros |
| Imagem da outra metade | **Cobre a área** (corte central na proporção 1,2 : 1), **zoom lento linear** (Ken Burns) de 100 → 104–109% ou ao contrário, durante a cena; vídeo do acervo **mudo**, grade `saturate(0.7) contrast(1.06) brightness(0.96)`; fotos com `grayscale(0.15) contrast(1.05)` | `rev2.json` (`kb`) e `estilo.ts` |
| Outras composições do mesmo Reel | Tela cheia de apoio (8 cenas), cartão 800 × 900 com cantos de 20 px sobre o Diego desfocado em P&B (2), Diego em tela cheia (2), animações em fundo `#14120F` | Folha de quadros |
| Grão | Ruído de película 6% em `overlay` sobre tudo | `AnneFrank.tsx` |

## 3. Legendas

| Item | Medida |
|---|---|
| Queimadas no vídeo | Sim |
| Fonte | **Inter 800**, **66 px**, altura de linha 1,1 |
| Cor | Branco; **palavra de destaque em âmbar `#E0AE5C`** (≈ 1 por grupo: números, nomes, palavra-chave) |
| Contorno/sombra | Sem contorno; sombra `0 3px 0 rgba(0,0,0,0.35)` + `0 4px 22px rgba(0,0,0,0.85)` |
| Posição | Centrada no canvas (x 540: centro medido 539,5–540,5); **centro vertical na costura (y 900)** na tela dividida, **y 1320** na tela cheia (texto medido em y 1296–1343), **y 1375** no cartão |
| Palavras por vez | **1 a 3** (até ~24 caracteres), sempre **1 linha**, quebra na pontuação e sem terminar em artigo/preposição |
| Entrada | 120 ms: opacidade 0 → 1 e escala 94 → 100% |
| Gancho | A 1ª frase falada em **Anton** (caixa-alta, branco), à esquerda em x 72, topo y 690, sobre degradê escuro na base; o 2º bloco entra linha a linha quando é dito. Sem legenda por baixo do gancho |
| CTA | Única peça do DS V2: Placa de direção (verbo + módulo de seta) em x 72 · y 640, Chegada 560 ms + *clack* a −10 dB da voz |

## 4. Transições e ritmo

| Item | Medida |
|---|---|
| Transição | **Corte seco** entre imagens (20 cortes detectados na REV2, todos de 1 quadro). As animações têm movimento interno, não transição |
| Duração de cada imagem | **média 2,03 s · mediana 1,90 s · mínimo 0,83 s · máximo 4,10 s** (25 cenas em 50,8 s); o gancho dura ≈ 4 s |
| Troca de imagem | Cai na palavra que a imagem mostra (âncora palavra ± 0,04–0,12 s) |
| Zoom no Diego | Só nas cenas em que ele aparece em tela cheia: aproximação lenta e linear 110 → 116% e 100 → 105% (2 vezes); na tela dividida, sem zoom |

## 5. Áreas seguras

Nada de texto na faixa da interface do Instagram: **y 1440–1920**, nem acima de y 256. Legendas e CTA ficam dentro da zona segura do DS V2 (x 72–944 · y 256–1440). O centro dos elementos centralizados é x 540 (CLAUDE.md, 6).

## 6. Trilha e áudio

| Item | Medida |
|---|---|
| Faixas | **Só a voz original** (mono centralizado) + o *clack* do CTA. **Sem trilha no render**: a música entra no Instagram, 8 a 10 dB abaixo da voz |
| Volume | Voz a −14 LUFS antes do master; master −14,0 LUFS integrados, pico verdadeiro −1,9 dBTP (REV2) |
| Tratamento | Passa-alta 70 Hz, ganho linear, limitador com sobreamostragem 4×. Sem redução de ruído na REV2 |
| Cortes | Takes emendados em corte seco, com fade de 12 ms na entrada e 30–60 ms na saída; nenhum silêncio digital entre falas |

## 7. Como este Reel segue o padrão

Tudo acima foi reproduzido com os mesmos valores (a composição `ReelGaudi` partiu da `ReelAnneFrank`; `estilo.ts` copiado sem mudança). Diferenças, todas por regra do pedido de 26/10/2026 ou por medida:

1. **Sem rótulo de crédito na imagem** (o Anne Frank mostrava "o que é · ano · autor · licença"). O pedido proíbe texto, nome ou data fora do roteiro; os créditos ficam em `creditos.md` e vão na legenda do post.
2. **Degradê escuro na base das tomadas claras em tela cheia** (o mesmo do gancho), porque a legenda branca em y 1320 sumia sobre a pedra clara da Sagrada. O Anne Frank tinha fundos escuros (entardecer) e não precisou.
3. **Redução leve de ruído** na voz (`afftdn`, 8 dB), pedida neste Reel.
4. **CTA com a fala**: o Diego gravou o CTA (parte 9), então a Placa entra quando ele diz "salva" e a legenda continua; no Anne Frank o CTA era só na tela, depois da fala.
5. Alguns grupos de legenda têm 4 palavras curtas (ex.: "de carne e osso", "Já salva esse vídeo"), sempre em 1 linha e até 24 caracteres (o mais largo tem 744 px).
