# QA · Reel "Primeiro dia em Amsterdam" · REV8 (04/11/2026) · versão para postar

**Veredito: pronto.** A REV8 parte da REV7 (`../rev7/QA_REV7.md`, não alterada) com quatro pedidos do Diego (04/11/2026).

## O que mudou

| # | Pedido | Na REV8 |
|---|---|---|
| 1 | "Coloque os preços e o placar de novo" | Placar do Dia (DS V2, 2.5) e as etiquetas de valor de volta, como na REV5 (fecha em **€ 78,85**, sem a pizza), com a moeda em cada soma |
| 2 | "Coloque em formato narrado, tire de tela verde" | **Formato Narrado** (Trello): o recorte do Diego sai da tela; a voz dele narra sobre as imagens da viagem em tela cheia. A legenda desce para a posição de tela cheia (**y 1320**, FORMATOS_REELS.md, 6). Regra do Narrado (no máximo 3 s por cena): a Red Light vai até "E por último" (2,50 s) e o canal noturno cai de 3,5 para **3,0 s** |
| 3 | Kalverstraat com dois takes iguais | Fica o 1º (IMG_1464, a rua); o 2º (IMG_1472, a mesma rua) vira **IMG_1466**, a fachada de uma loja de perto (tremor 0,2–0,4). O IMG_1467 (LEGO) tem 2,33 s, menos que a cena (2,37 s), e não dá para esticar |
| 4 | "Coloque a outra CTA no lugar do vídeo do YouTube" | O CTA final é o **IMG_7632**: "Já manda esse vídeo pra alguém que vai pra Amsterdã e comenta aqui o que você quer saber de lá." (0,24–3,74 s da tomada). A placa do DS entra com **"MANDA PRA ALGUÉM QUE VAI PRA / AMSTERDAM →"** e fica assim até o fim; o "comenta aqui o que você quer saber de lá" fica só na fala e na legenda (pedido do Diego). A grade do dia entra em "vídeo" (53,27 s), para o McDonald's ficar 2,0 s |

O Reel passa de 60,6 s para **56,9 s** (o CTA novo é mais curto). As legendas do post trocam o CTA do YouTube pelo de envio e comentário.

## Medido no vídeo final

Preenchido depois do render (`scripts/conferir.py`).

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel usa € 7,15.
2. **Escuta:** `keen` (2,72 s), moeda e efeitos, e as palavras de transcrição duvidosa ("um/o ônibus", "estava/tava", "vamos/fomos").
