# Reel "Amsterdã é cara mesmo?" · REV3 · QA

**Entrega (22/11/2026):** `rev3/reel_ams-custo_rev3.mp4` (**59,97 s**, 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, −14,1 LUFS, pico −1,4 dBTP, sem música), prévia `rev3/reel_ams-custo_rev3_previa.mp4`, capa `rev3/capa_ams-custo_rev3.jpg`, folhas `rev3/qa_frames/`. MP4 fora do git (cota de Git LFS estourada) e entregues pelo app.

**Parte da REV2** (não alterada). Pedidos do Diego:
1. **Duas correções de valor:** gravação 13 no lugar da 11 (comida e bebida, agora "quinhentos e setenta e cinco") e gravação 14 no lugar da 8 (passeios, agora "duzentos e sessenta e oito... por pessoa"). Conferido com o wav2vec2: perda do CTC 34 × 114 ("cinco" × "dois") e 154 × 184 ("sessenta" × "setenta"). **Fala e legenda agora batem** em todos os valores, e a exceção da REV2 (legenda diferente da fala) deixou de existir.
2. **CTA nova:** gravação 15, com a frase do fim ("Toda semana eu posto dicas, custos e roteiros de viagens aqui no meu perfil, e se você gostou, já me segue aí pra não perder nada.").
3. **Até 60 s:** "1,03, mas que fique abaixo ou até 60 segundos; se passar, use o multiplicador que leva a 60". O render deu **62,37 s**. Em 1,03 ficaria 60,55 s, ainda acima. Para ficar em 60 s o multiplicador foi **1,04** (vídeo inteiro, imagem e voz juntas, voz sem mudar o tom; `scripts/reel.py`, passo `velocidade`, limite em `cenas.json` → `duracao_max_s`). Exceção pedida pelo Diego à regra "a voz nunca é acelerada" (CLAUDE.md, 12), só neste Reel. A cauda depois da última palavra caiu de 1,6 para 1,2 s, para o multiplicador ser o menor possível.

## Falas novas

| # | Fala (= legenda) |
|---|---|
| 7 (gravação 13) | Contando tudo o que a gente comeu e bebeu, ficou 575 reais por pessoa, 192 por dia. |
| 8 (gravação 14) | E passeios: nós fomos para a Casa de Anne Frank e o museu da primeira fábrica da Heineken no mundo. Isso ficou 268 reais por pessoa. |
| 10 (gravação 15) | Toda semana eu posto dicas, custos e roteiros de viagens aqui no meu perfil, e se você gostou, já me segue aí pra não perder nada. |

Duvidoso para a escuta: na 14 o Whisper ouve "que é o museu" e o wav2vec2 "e o museu" (ficou "e o museu").

## Valores (todos batem com o registro, PTAX 12/03/2026)

Hotel R$ 3.315 o casal · transporte R$ 135 · comida e bebida R$ 575 (R$ 192/dia) · stroopwafel 57, Albert Cuyp 24, batata 42 · passeios R$ 268 · **total R$ 2.636 por pessoa**.

## Imagens

As mesmas da REV2, com os cortes refeitos nas palavras novas: a cena da Anne Frank começa no "E passeios"; o sanduíche do Febo entra em "ficou 575"; o canal à noite vai até "já me segue aí", e a CTA (canal do gancho + placa) fica no fim.

## Medições

| Ponto | Resultado |
|---|---|
| Duração | 59,97 s (render 62,37 s × 1/1,04) |
| Loudness | −14,1 LUFS, pico −1,4 dBTP |
| Cenas | menor 1,92 s na tela (2,00 s antes do multiplicador), maior 7,88 s (gancho + notícia) |
| Cortes no quadro | 17 de 19; não detectados: c02 (atrás da notícia escurecida) e c06 (quarto → quarto, mesma cor); conferidos na folha de 1 s |
| Legendas | 63 grupos, 1 linha, a maior 791 px |

## Pendências

1. Escuta humana: voz acelerada em 1,04 (naturalidade), emendas, "é das" no bloco 1, volume do `keen` e do clack.
2. Febo do dia 3 (preço por unidade?) e o gancho sem ranking que o comprove, como antes.
