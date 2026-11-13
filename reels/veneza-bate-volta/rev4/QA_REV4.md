# QA · Veneza bate-volta · REV4 (13/11/2026)

**Entrega:** `veneza_bate_volta_rev4.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa: `capa_rev4.jpg` (+ `capa_rev4_grade_3x4.jpg`, a mesma da REV2/REV3). Legendas: `legenda_post.md`.
**Fontes:** gravação original (`fonte/gravacao.mp4`, Drive Itália/Veneza, 4AF31B30…, 63,3 s) e gravações novas (`fonte/novas.mp4`, Drive Itália/Veneza, 1CC52CD5…, 47,2 s, 13/11/2026). A REV3 não foi alterada.
**Composição:** `VenezaReel4` (`design-system/remotion/src/reel/VenezaReel4.tsx`). Scripts: `preparar.py` (decupagem, voz, apoio) → `cenas.py` (cenas, legenda, posições) → render → master → `analise_quadros.py`.

## Pedidos do Diego (13/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| Fim do bloco 2: "Ou seja, Veneza quer que você fique na cidade" + "E eu fiquei por duas noites" no lugar de "Ou seja, é que tá… durma na cidade. E eu fiquei, e" | Trocado (take B1). "Não gostei. Não faça isso." (bloco 3) mantido |
| Bloco 4 novo: "Não me leve a mal. Veneza de dia é o cenário de filme… Mas à noite eu acho a cidade deserta." | Trocado (take B2). "Sim, Diego, eu vou fazer o quê? Vou pagar a taxa?" mantido em P&B |
| Bloco 5: manter até "E no bolso?" e trocar o resto pelo take novo (macete) até "link na legenda" | Feito (takes A8, A9 e B3–B4) |
| Antes do bloco 6: "Ah, Diego, mas…" em P&B e a resposta "Durma e tire suas próprias conclusões…" | Acrescentados (B5 em P&B, B6). Depois, o bloco 6 (CTA) |
| Decupar sem espaço entre as falas, sem cortar palavra | 15 trechos, 0,10–0,15 s de silêncio entre uma fala e a outra (só a folga para não cortar). Toda emenda cai em silêncio (≤ −61 dBFS nos 20 ms de cada lado). **Prova:** a voz final foi transcrita de novo (Whisper large-v3) e tem todas as palavras, na ordem |
| Legenda sem caixa alta | Caixa normal (maiúscula no começo da frase e nos nomes, pontuação do português). Karaokê mantido: a palavra dita fica amarela. O gancho também (é a legenda dos primeiros 3,3 s). Ficam em caixa alta só os rótulos dos grafismos (MULTA, PEDÁGIO, 30 MILHÕES…) e a capa |
| Nenhum item de legenda antes da hora | Cada palavra da legenda, do gancho e dos rótulos entra no início dela; as que ainda não foram ditas ficam invisíveis no lugar. **Causa na REV3:** os tempos eram do Whisper, que marca o início até 0,4 s antes da voz, e vários rótulos estavam presos à palavra errada ("5 €" em "São", "VAI" em "quem", "NÃO DORME" em "e", "PROGRAMADO" em "pros", "NA HORA" em "paga", "1H E POUQUINHO" em "só", e a placa da CTA em "E se" em vez de "me segue"). Agora: alinhamento forçado (wav2vec2 PT + CTC, FORMATOS_REELS 7.2) e cada âncora presa ao texto da palavra |
| Nada no rosto | Rosto medido quadro a quadro (detector Haar, `rosto.py`). Tela cheia: legenda em y 1320 (abaixo do queixo); nos dois takes em que ele chega perto da câmera ("Não gostei / Não faça isso" e "Sim, Diego… taxa?"), o queixo desce até y ≈ 1330, então a legenda do take inteiro vai para cima da cabeça (y 359 e 295). Tela dividida: rosto a 42% da metade de baixo (FORMATOS_REELS 2), longe da faixa da interface; legenda na costura, acima do cabelo. CTA: placa em y 1218 (base 1437), abaixo do queixo (no pior quadro, em "toda semana", a barba termina em y ≈ 1190); a legenda sai em "já me segue aí" e a placa entra em "me segue" no lugar dela (diz o mesmo que a fala) |
| Nenhum filtro ou cor no vídeo dele | Nenhum. A gravação é HDR (HLG) e passa só pela conversão HLG→SDR padrão da REV1 (sem grade, sem LUT, sem contraste). O P&B é `grayscale(1)` puro (a REV3 tinha também `contrast(1.08)`, que saiu). O acervo também vai sem grade |
| Ver se os takes e animações fazem sentido | Ver "Fala × imagem" abaixo. Trocas: "Veneza quer que você fique" → Veneza à noite vista de um hotel; "cenário de filme" → pôr do sol no Grande Canal (acervo, IMG_6098, novo); "à noite… deserta" → Grande Canal à noite vazio (dissolve); "quem dorme em Veneza já paga a taxa" → grafismo novo (cama + "JÁ PAGA A TAXA"); "a magia da viagem" → fogos do Ano-Novo em Veneza (acervo, IMG_6156, novo). "4 dias antes" virou "DIAS DE ANTECEDÊNCIA" (o que ele fala) |

## Texto falado (o que vai na legenda)

| Take | Fonte (s) | Final (s) | Texto |
|---|---|---|---|
| A1 | orig. 0,00–5,63 | 0,00–5,63 | Veneza não te quer lá e dessa vez é de verdade. (senta) Em partes. |
| A2 | orig. 5,87–14,17 | 5,63–13,93 | Veneza recebe quase 30 milhões de pessoas no ano, sendo que três em cada quatro desses visitantes vão de bate-volta. Por isso a cidade criou um pedágio pra quem vai e não dorme. |
| A3 | orig. 14,57–21,17 (pausa de 0,23 s tirada antes de "multa") | 13,93–20,30 | São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar, multa pra doer no bolso, pai. |
| B1 | nova 0,00–3,87 | 20,30–24,17 | Ou seja, Veneza quer que você fique na cidade. E eu fiquei por duas noites. |
| A5 | orig. 28,40–30,13 | 24,17–25,90 | Não gostei. Não faça isso. |
| B2 | nova 5,03–9,83 | 25,90–30,70 | Não me leve a mal. Veneza de dia é o cenário de filme que você sempre sonhou. Mas à noite eu acho a cidade deserta. |
| A7 (P&B) | orig. 36,33–38,27 | 30,70–32,63 | Sim, Diego, eu vou fazer o quê? Vou pagar a taxa? |
| A8 | orig. 38,47–47,67 | 32,63–41,83 | Exatamente. Você vai incluir Verona no seu roteiro da Itália, uma cidade que fica só uma hora e pouquinho de Veneza, e um dia você faz um bate-volta pra lá e no outro você conhece a cidade do Romeu e Julieta. |
| A9 (P&B) | orig. 48,40–49,40 | 41,83–42,83 | E no bolso? |
| B3 | nova 10,77–18,43 | 42,83–50,50 | Aí que tá o macete. Quem dorme em Veneza já paga a taxa no valor da hospedagem. Então ficar em Verona pode ser até 25% mais barato do que dormir na cidade dos canais. |
| B4 | nova 23,20–28,07 | 50,50–55,37 | E reservar o pedágio quatro dias de antecedência, você paga só cinco euros. Eu vou deixar o link na legenda. |
| B5 (P&B) | nova 33,27–35,03 | 55,37–57,13 | Ah, Diego, mas eu quero dormir na cidade. |
| B6 | nova 39,30–44,83 | 57,13–62,67 | Durma e tire suas próprias conclusões. Aí que tá a magia da viagem. Cada experiência toca a pessoa de uma maneira diferente. |
| A11 | orig. 59,37–63,27 | 62,67–66,57 | E se você gostou, já me segue aí, porque eu dou dicas de viagem toda semana por aqui. |

**Divergências com o que o Diego descreveu no pedido (a legenda segue a gravação, FORMATOS_REELS 6):** "mas à noite *eu acho a cidade* deserta" (não "ela fica deserta"); "Ah, Diego, mas *eu quero* dormir na cidade" (não "e se eu quiser"); "Durma *e* tire suas próprias conclusões"; "E reservar o pedágio quatro dias de antecedência" (sem "com"). **Leituras a conferir no ouvido:** "Aí que tá o macete" (o Whisper ouve "Aqui tá uma cita"; com a palavra "macete" de dica, confiança 0,85) e "Aí que tá a magia da viagem" (sem dica ele ouve "Que tá"); um "a" de 40 ms antes de "Veneza" no take B1 ("Ou seja, a Veneza…") fica fora da legenda.

## Cortes do próprio Diego nas gravações (1º quadro do take novo, pela diferença entre quadros)

- Original: 174 (5,80 s), 432, 642, 851, 908, 1082, 1150, 1444, 1484, 1773 (59,10 s).
- Nova: 139 (4,63 s), 316, 614, 910, 1117 (37,23 s).

Nenhum trecho da REV4 começa antes do corte do take nem termina depois do seguinte.

## Fala × imagem

| Final (s) | Fala | Imagem |
|---|---|---|
| 0,00–3,33 | Veneza não te quer lá e dessa vez é de verdade. | Palácio Ducal lotado + gancho palavra por palavra (Diego embaixo) |
| 3,33–5,63 | (senta) Em partes. | Diego em tela cheia |
| 5,63–8,12 | Veneza recebe quase 30 milhões de pessoas no ano, | Praça São Marcos cheia · "QUASE" · "30" · "MILHÕES" · "DE PESSOAS NO ANO", cada um na palavra |
| 8,12–11,23 | sendo que três em cada quatro desses visitantes vão de bate-volta. | 3 de 4 bonecos · "3 EM CADA 4" · print da Fortune (80%) |
| 11,23–13,93 | Por isso a cidade criou um pedágio pra quem vai e não dorme. | Bilhete · "PEDÁGIO" · sol "VAI" · lua riscada "NÃO DORME" |
| 13,93–18,67 | São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar, | Cartões "5 € / PROGRAMADO" e "10 € / NA HORA" · "E SE NÃO PAGAR?" |
| 18,67–20,30 | multa pra doer no bolso, pai. | Carimbo "MULTA" · "PRA DOER NO BOLSO" |
| 20,30–22,68 | Ou seja, Veneza quer que você fique na cidade. | Santa Maria della Salute à noite, vista de um hotel (Commons) |
| 22,68–26,57 | E eu fiquei por duas noites. Não gostei. Não faça isso. Não me leve a mal. | Diego em tela cheia (3 takes) |
| 26,57–30,70 | Veneza de dia é o cenário de filme que você sempre sonhou. Mas à noite eu acho a cidade deserta. | Pôr do sol no Grande Canal (acervo, 31/12/2024) → dissolve em "Mas" → Grande Canal à noite vazio |
| 30,70–33,39 | Sim, Diego, eu vou fazer o quê? Vou pagar a taxa? (P&B) Exatamente. | Diego em tela cheia; volta à cor em "Exatamente" |
| 33,39–35,36 | Você vai incluir Verona no seu roteiro da Itália, | Arena de Verona · "VERONA" |
| 35,36–39,47 | uma cidade que fica só uma hora e pouquinho de Veneza, e um dia você faz um bate-volta pra lá | Mapa: linha do trem · "1H E POUQUINHO / DE VENEZA" · "⇄ BATE-VOLTA" |
| 39,47–41,83 | e no outro você conhece a cidade do Romeu e Julieta. | Varanda de Julieta · "ROMEU E JULIETA" |
| 41,83–44,05 | E no bolso? (P&B) Aí que tá o macete. Quem dorme | Diego em tela cheia; volta à cor em "Aí" |
| 44,05–46,22 | em Veneza já paga a taxa no valor da hospedagem. | Grafismo novo: "QUEM DORME EM VENEZA" · cama e lua · "JÁ PAGA A TAXA" · "NO VALOR DA HOSPEDAGEM" |
| 46,22–50,50 | Então ficar em Verona pode ser até 25% mais barato do que dormir na cidade dos canais. | Cartões Verona × cidade dos canais · "ATÉ 25%" · "MAIS BARATO" |
| 50,50–55,37 | E reservar o pedágio quatro dias de antecedência, você paga só cinco euros. Eu vou deixar o link na legenda. | Calendário "4 / DIAS DE ANTECEDÊNCIA" → "5 €" · título do site oficial · "LINK NA LEGENDA ↓" |
| 55,37–58,94 | Ah, Diego, mas eu quero dormir na cidade. (P&B) Durma e tire suas próprias conclusões. | Diego em tela cheia; volta à cor em "Durma" |
| 58,94–62,67 | Aí que tá a magia da viagem. Cada experiência toca a pessoa de uma maneira diferente. | Fogos do Ano-Novo na laguna (acervo, 01/01/2025 00:11) |
| 62,67–66,57 | E se você gostou, já me segue aí, porque eu dou dicas de viagem toda semana por aqui. | Diego em tela cheia + placa do DS "DICAS DE VIAGEM TODA SEMANA / ME SEGUE" em "me segue" + *clack* |

Regras de montagem conferidas por `cenas.py`: troca de imagem no mesmo quadro de um corte da gravação ou a ≥ 0,5 s dele; nada gravado pelo Diego (acervo, rosto em tela cheia) por menos de 2 s (o menor é 2,22 s, "E no bolso? Aí que tá o macete. Quem dorme").

## Imagens: origem e crédito

- **Acervo do Diego** (sem o rosto dele nem da Marina nos trechos usados): IMG_6062 6,0–9,6 s · IMG_6063 12,3–15,5 s · IMG_6098 7,0–10,5 s (novo) · IMG_6128 1,0–4,4 s · IMG_6016 3,0–6,0 s · IMG_6156 9,3–13,7 s (novo; a multidão no pé do quadro fica fora do corte).
- **Wikimedia Commons** (as mesmas da REV2/REV3, conferidas lado a lado; crédito no comentário fixado): Arena di Verona, Andrea Bertozzi, CC BY-SA 4.0 · Ponte Pietra, Maupao70, CC BY-SA 4.0 · Verona – Juliet Balcony, Guilhem Dulous, CC BY-SA 1.0 · Santa Maria della Salute from Hotel Monaco nightview, Wolfgang Moroder, CC BY-SA 3.0. A API do Commons respondeu 429 nesta sessão; a autoria vem da QA da REV2.
- **Prints:** Fortune, 03/01/2024 (manchete e parágrafo do 80%, refeitos nesta sessão com o destaque na própria página) · título da página oficial cda.ve.it (o site bloqueia acesso automático, erro 15; recortado do quadro da REV3, 940 × 172, o tamanho em que aparece).

## Fato novo da fala

"Quem dorme em Veneza já paga a taxa no valor da hospedagem": quem dorme na cidade paga a taxa de turismo (*imposta di soggiorno*), cobrada pela hospedagem, e por isso fica isento do pedágio. Mas precisa pedir a isenção no cda.ve.it. A legenda do post avisa. Fontes: The Local (20240422), Hostaway (guia de Veneza), Untold Italy (2026).
