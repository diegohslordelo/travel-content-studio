# QA · 3 formas de economizar com comida na viagem · REV2 (17/11/2026)

**Entrega:** `comida_3_formas_rev2.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Parte da REV1 (que não muda). Legendas do post: `legenda_post.md` (iguais às da REV1).
**Composição:** `ComidaReel2` (`design-system/remotion/src/reel/ComidaReel2.tsx`). Scripts: `preparar.py` → `cenas.py` → render → `master.py` → `analise_quadros.py`.

```
cd design-system/remotion
npx remotion render src/index.ts ComidaReel2 ../../reels/comida-3-regras/rev2/render_sem_master.mp4 \
  --props=../../reels/comida-3-regras/rev2/props.json --public-dir=../../reels/comida-3-regras/rev2/public \
  --codec=h264 --crf=16 --audio-bitrate=320k
cd ../../reels/comida-3-regras/rev2 && python3 master.py render_sem_master.mp4 comida_3_formas_rev2.mp4
```

## Pedidos do Diego (17/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| "Bora" duas vezes seguidas | Ele falou "Bora…" (9,96 s), parou e recomeçou "Bora que eu vou te mostrar" (10,96 s). A REV1 guardava os dois (o primeiro como um trecho de 0,7 s, com ele em tela cheia). Agora o T2 começa no segundo "Bora". Prova: leitura letra a letra (wav2vec2 sem modelo de língua, que não esconde repetição) de cada trecho do vídeo final |
| "Tem parte que eu apareço" | O trecho do café da manhã começava 2 quadros antes do corte da própria gravação (quadro 524, 17,47 s), com o braço dele passando na frente da câmera. Agora o trecho começa no quadro do corte, e `preparar.py` recusa qualquer trecho que atravesse um corte da gravação (11 cortes medidos, `cortes_gravacao.json`) |
| Revisar todos os cortes | 12 trechos, um por fala, conferidos: (1) leitura letra a letra de cada trecho, sem palavra repetida nem começo falso; (2) primeiro e último quadro de cada trecho, todos com ele sentado e enquadrado; (3) nenhum trecho atravessa corte da gravação; (4) voz final transcrita de novo (Whisper large-v3) |
| Jantar: take de vocês jantando (Bruxelas ou Madrid) | "Geralmente escolhemos o jantar…": Diego jantando no Espago Ristorante, Bruxelas (IMG_2407, 15/03/2026 20:00) |
| Almoço em Madrid | "Mas quem define? Seu roteiro. Se tem algum restaurante que vale a pena ir na hora do…": Marina no almoço do restaurante italiano, Madrid (IMG_4145, 21/03/2026 14:25). "Segunda… no restaurante": Diego no mesmo almoço (IMG_4144) |
| Comida de rua: FEBO, Albert Cuyp ou falafel | "Você vai comer alguma comida de rua, algum lanche rápido…": Marina comendo o croquete do FEBO, Amsterdam (IMG_1922). "…parte de sua experiência conhecendo o local": Marina comendo o falafel da Falafelería, Madrid, com joinha (IMG_3939) |
| Ilustrar mais com acervo | 9 planos reais + a foto do café (REV1: 6 + foto), incluindo a paella de Barcelona no gancho. Animações ficaram só onde não há imagem real: café da manhã no quarto, almoço × jantar ("inverte"), 50 € e a balança |
| Gancho: esperar ele terminar a pergunta | Ele entra em tela cheia em "Bora", depois de "restaurantes?" (REV1: entrava em "conhecer") |
| Gancho: metade bouillon, metade paella de Barcelona, legenda normal | 1ª metade (0–2,66 s, "Você quer saber como economizar com a alimentação nas suas viagens"): prato do Le Petit Bouillon Pharamond (IMG_3075). 2ª metade (2,66–4,77 s, "e ainda assim conhecer bons restaurantes?"): paella, Barcelona (IMG_0995). Legenda karaokê normal na costura. Uma 1ª versão com a pergunta em letras garrafais (Anton) foi recusada pelo Diego e não entrou |

## Fala × imagem

| Final (s) | Fala | Imagem (em cima) |
|---|---|---|
| 0,00–2,66 | Você quer saber como economizar com a alimentação nas suas viagens | Prato do Le Petit Bouillon Pharamond, Paris (IMG_3075) |
| 2,66–4,77 | e ainda assim conhecer bons restaurantes? | Paella, Barcelona (IMG_0995) |
| 4,77–9,23 | Bora que eu vou te mostrar três formas que eu uso pra não gastar uma nota com comida durante a viagem. | Ele em tela cheia |
| 9,23–12,15 | A primeira coisa é economizar no café da manhã. Se não tá incluso no hotel, | Animação: "1", xícara, "CAFÉ DA MANHÃ", "NÃO TÁ INCLUSO" |
| 12,15–15,57 | a gente passa no supermercado e compra algumas coisas para comer no quarto mesmo. | Albert Heijn, Amsterdam (IMG_1842) |
| 15,57–19,93 | O que sobra para comprar na rua é só um menorzinho de toda manhã que não pode faltar, né? | Foto do café na rua, Florença (IMG_5826) |
| 19,93–23,27 | Segunda, escolha uma refeição pra gastar um pouco mais no restaurante. | Diego no restaurante italiano, Madrid (IMG_4144) + "SEGUNDA" |
| 23,27–27,63 | Geralmente escolhemos o jantar porque é mais no final do dia, a gente já fez tudo e pode comer com calma. | Diego jantando, Espago Ristorante, Bruxelas (IMG_2407) |
| 27,63–30,77 | Mas quem define? Seu roteiro. Se tem algum restaurante que vale a pena ir na hora do | Marina no almoço, Madrid (IMG_4145) |
| 30,77–34,67 | almoço por conta de uma vista ou experiência do lugar, aí você inverte. | Animação: ALMOÇO × JANTAR, "VISTA OU EXPERIÊNCIA", moedas pulam para o almoço em "inverte" |
| 34,67–37,27 | E nas outras refeições, rapaz, vai ficar sem comer? (P&B) Claro que não. | Ele em tela cheia |
| 37,27–41,67 | Você vai comer alguma comida de rua, algum lanche rápido, algo mais simples que vai te fazer gastar menos. | Marina com o croquete do FEBO, Amsterdam (IMG_1922) |
| 41,67–45,20 | E eu te garanto que isso vai fazer parte de sua experiência conhecendo o local. | Marina com o falafel, Falafelería, Madrid (IMG_3939) |
| 45,20–49,20 | Por exemplo, vamos supor que você vai para a Europa e quer gastar 50 euros por dia com comida. | Animação: "POR EXEMPLO, VAMOS SUPOR", "EUROPA", "50 €", "POR DIA COM COMIDA" |
| 49,20–53,10 | Então você vai usar esse valor pra balancear suas refeições de acordo com a dica número 2. | Animação: balança, "DICA Nº 2" |
| 53,10–57,03 | Economizar com comida não é comer mal, é você saber onde gastar e onde não gastar. | O prato do gancho, de cima (IMG_3078) |
| 57,03–61,70 | Se você gostou das dicas, me segue aí para aprender a viajar melhor sem gastar dinheiro à toa. | Ele em tela cheia + placa do DS `PRA VIAJAR MELHOR / ME SEGUE` + *clack* |

Acervo sem filtro, sem zoom e na velocidade original; tremor medido (≤ 0,2 px de variação entre quadros em todos os trechos usados).

## Para o Diego saber

- **Gancho, 2ª metade:** a paella fica 2,1 s. A troca cai no início de "e ainda assim" (2,66 s de 4,77 s); trocar mais cedo cortaria a frase "nas suas viagens" no meio.
- **"Três formas…" sem animação:** ele fica em tela cheia de "Bora" até o fim da frase (4,5 s). Voltar à tela dividida no meio deixaria ele ou a animação com menos de 2,5 s na tela.
- **Leituras a conferir no ouvido:** "menorzinho" e "Mas quem define? Seu roteiro." (ver QA da REV1).
- **Moral:** continua o último take ("…onde gastar e onde não gastar").
- **Efeitos (kit PDX, ninguém ouviu):** *swish* em "inverte", impacto em "50", obturador em "dica", *clack* da placa.

## Medições do vídeo final (`analise_quadros.py` + leitura letra a letra)

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz 320 kb/s, 61,7 s (1.851 quadros) |
| Áudio | −14,0 LUFS integrados, pico verdadeiro −2,0 dBTP (DS 4.6) |
| Cortes | 12 trechos; leitura letra a letra (wav2vec2, sem modelo de língua) de cada trecho do vídeo final: todas as frases completas, nenhuma palavra repetida, **um único "Bora"** |
| Quadros pretos | nenhum (luminância mínima 50/255) |
| Preto e branco | só T7 |
| Texto × rosto | menor folga 38 px (placa do CTA); legenda sempre fora do rosto |
| Menor cena | 2,11 s (paella, 2ª metade do gancho); o resto ≥ 2,6 s |
| Folha de 1 quadro por segundo | `qa_folha_1qps.jpg` |
