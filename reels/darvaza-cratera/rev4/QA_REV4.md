# QA · Reel da cratera de Darvaza · REV4 (31/10/2026)

**Veredito: pronto.** A REV4 parte da REV3 (`../rev3/QA_REV3.md`, não alterada) e muda o **ritmo das cenas**. Voz, legendas, gancho, títulos, transições e CTA são os mesmos.

**Pedido do Diego (31/10/2026):** "Respeite a regra dos 3 segundos para cada foto… tem que ser de 2 a 3 segundos ali na tela. Tá muito rápido."

**Regra aplicada a todo o Reel:** cada cena (foto, ilustração, mapa ou o Diego em tela cheia) fica **de 2 a 3 s** na tela. Isso substitui, neste Reel, o ritmo de ≈ 2 s por imagem do guia do formato (docs/FORMATOS_REELS.md, 5.1, que aceitava fotos de 0,9 s). Se o Diego quiser a regra em todos os Reels, falta registrar no guia.

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_darvaza_rev4.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **40,97 s**, **−14,1 LUFS**, pico **−1,4 dBTP** |
| `reel_darvaza_rev4_previa.mp4` | Prévia leve (540 × 960) |
| `capa_darvaza_rev4.jpg` | Capa (igual à das revisões anteriores) |
| `qa_frames/` | Um quadro por cena · um quadro por segundo |

## Cenas (17; eram 25 na REV3)

| # | Tempo (s) | Dur. | Fala | Imagem |
|---|---|---|---|---|
| 1 | 0,00–2,17 | 2,17 | Imagine encontrar um buraco gigante em chamas | Chamas de perto + texto do gancho |
| 2 | 2,17–5,07 | 2,90 | no meio do deserto. Tem fogo pra todo lado, e quando a noite chega | Cratera no deserto à noite; a câmera se aproxima (zoom 1,16 → 1,5) |
| 3 | 5,07–7,33 | 2,27 | parece que abriram uma porta direto pro inferno | Borda em chamas + mergulho no fogo |
| 4 | 7,33–9,90 | 2,57 | A história começou com a perfuração em busca de gás natural | Ilustração: perfuração |
| 5 | 9,90–12,10 | 2,20 | e aí o solo cedeu e formou essa enorme cratera | Ilustração: desabamento (tela cheia) |
| 6 | 12,10–14,33 | 2,23 | Para evitar que o gás se espalhasse, decidiram colocar | Ilustração: gás + fósforo |
| 7 | 14,33–17,27 | 2,93 | fogo nele, acreditando que ele se apagaria em poucos dias. Antes de eu | Fogo real que escurece em "apagaria" + POUCOS DIAS |
| 8 | 17,27–19,37 | 2,10 | falar onde fica, já manda esse vídeo para aquela pessoa que | Você em tela cheia + ícone de envio |
| 9 | 19,37–21,37 | 2,00 | teria coragem de chegar perto desse lugar! | Carro e pessoas na borda à noite |
| 10 | 21,37–24,03 | 2,67 | Esse lugar existe de verdade e fica no Turcomenistão. É a | Luz de passagem → mapa + TURCOMENISTÃO + ponto |
| 11 | 24,03–26,03 | 2,00 | cratera da Darvaza. Ele também é mundialmente | A CRATERA / DARVAZA |
| 12 | 26,03–28,20 | 2,17 | conhecido como a Porta do Inferno. E o mais impres- | PORTA DO INFERNO |
| 13 | 28,20–30,20 | 2,00 | -sionante é que a cratera continuou queimando durante | Você em tela cheia + clarão + corte de zoom |
| 14 | 30,20–32,53 | 2,33 | décadas, o que começou com uma exploração natural | Rastros de estrelas + DÉCADAS |
| 15 | 32,53–35,07 | 2,53 | se transformando nas paisagens mais surreais do planeta | Panorama com movimento lateral |
| 16 | 35,07–38,00 | 2,93 | Agora me diz, você teria coragem de ver isso de perto? Já segue esse | A câmera se aproxima da cratera ao amanhecer (a placa do CTA entra em "segue") |
| 17 | 38,00–40,97 | 2,97 | perfil para não perder outros lugares imperdíveis pelo mundo! | Chamas de perto (mesmo plano do gancho: loop) + placa |

**Medido no vídeo renderizado** (detecção de corte na metade de cima e no quadro inteiro): cortes em 2,17 · 5,07 · 7,3 · 9,90 · 12,10 · 14,33 · 17,27 · 19,37 · 21,37 · 24,03 · 26,03 · 28,20 · 30,20 · 32,53 · 35,07 · 38,00 s. **Menor cena 2,00 s, maior 2,97 s, média 2,41 s.**

**Tempo de leitura** (`scripts/tempos.py`, saída em `../_tmp/tempos_rev4.txt`): todo título e animação fica ≥ 0,8 s completo na tela antes do corte.

## O que saiu para caber

- **Fotos:** brilho no anoitecer, interior vermelho, cratera de dia, fumaça à noite, pessoa de braços abertos e foto diurna das chamas. Continuam em `../imagens/` e nas revisões anteriores.
- **Ilustração:** a torre que voltava em "exploração natural".
- **"Esse lugar existe de verdade":** agora entra junto com o mapa, que começa na luz de passagem.
- **Crédito na legenda do post:** continua certo. Todos os autores citados ainda têm foto no Reel.

## Outras mudanças

- Cauda depois de "pelo mundo!": 0,5 → **0,4 s**, para a última cena ficar em 2,97 s (≤ 3 s). O vídeo termina antes de você esticar a mão para parar a gravação.
- O *swish* do avião de envio segue a nova âncora ("pessoa" − 0,2 s).

## Conferir no ouvido

Os mesmos itens das revisões anteriores: "Imagine/Imagina", "solo", "Ele também", "exploração natural" e os efeitos sonoros.
