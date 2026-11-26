# QA · REV3 · "3 países onde o brasileiro vive como rico" (tela dividida)

**Entrega:** `reel_paises_real_rev3.mp4` (1080 × 1920, 24 qps, 48,4 s, −14,1 LUFS, pico −1,5 dBTP) · prévia `reel_paises_real_rev3_previa.mp4` · capa `capa_reel_paises_real_rev3.jpg`. Os .mp4 ficam fora do git (cota de Git LFS estourada) e foram enviados ao Diego pela conversa.
**Parte da REV2** (não alterada): mesmos cortes, voz, legendas, print e paisagens.
**Refazer:** de dentro de `rev3/`: `python3 rev3.py preparar && python3 rev3.py render && python3 rev3.py master`.

## Pedidos do Diego (26/11/2026)

**1. Placa "SEGUE PARA MAIS DICAS".** Em uma linha, a placa passaria da largura máxima de 872 px do DS (≈ 1.080 px, mesmo no tamanho de 104 px). Ficou no formato de duas linhas que o DS já prevê (rótulo + destino, como "PRIMEIRO DIA EM / BARCELONA"): rótulo `SEGUE PARA` e destino `MAIS DICAS`, com o módulo de seta. A fala continua "já me segue aí para não perder nada"; a legenda do post usa o mesmo verbo ("Segue pra mais dicas…").

**2. Menos cara de IA.** O que denunciava edição automática e o que mudou:

| Sinal de "IA/template" na REV2 | REV3 |
|---|---|
| Ilustrações vetoriais (cédulas caindo, rota com aviãozinho, 20 tigelas, 3 ícones de refeição, calendário, moeda de euro desenhada) | Saíram todas. Ficaram só fotos reais + etiquetas de texto: janela do avião (só a foto), pho com "≈ 20 PRATOS", wok com "R$ 150", loja de massagem com "1 HORA", "≈ R$ 50" e "TODO DIA" |
| Toda foto com o mesmo zoom lento e linear | Câmera na mão: deriva irregular (dois senos fora de fase, ±5 px, ±0,25°), diferente em cada foto, e zooms em sentidos variados |
| Nenhum corte no rosto | 4 cortes de zoom (punch-in, corte seco) nas frases de peso: "isso sem contar as taxas…" (1,14×), "onde o real é valorizado" (1,12×), "dá pra fazer todo dia" (1,12×), "você não compra nem um euro com isso" (1,2×, com você em tela cheia no lugar da moeda desenhada) |
| Legenda com pulo em toda palavra | Só a cor acende no tempo da fala (pedido da REV1 mantido), sem pulo |
| Etiquetas com "pop" exagerado e giro fixo de −3° | Entrada seca (86% → 102% → 100%), giro variado |
| 15 efeitos sonoros (um em quase todo corte) | 6: impacto no "milionário", obturador do print, riser da virada, ar na Luz de passagem, impacto na revelação do Egito, clack da placa |
| 5 transições com efeito | 3: Luz de passagem (Tailândia), giro do cartão (Egito), Empurrão (volta da tela cheia). Vietnã entra em corte seco; o Clarão saiu |

Ficaram como na REV2: o print da cotação, as paisagens em tela cheia, os cartões com o "?" (gancho secundário) e o letreiro do gancho.

## Pendências (continuam)

1. Escuta humana dos efeitos e das emendas.
2. "pratos" ou "praças" (≈ 24 s).
3. Texto da placa `SEGUE PARA / MAIS DICAS →`: pedido do Diego; não está entre os exemplos do DS V2 (2.7), registrar na próxima versão do brand book se for padrão.
4. Crédito das fotos na legenda do post (`legenda_post.md`).
