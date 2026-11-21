# QA · REV2 · Vlog de Bruges (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV1 (`rev1/`, não alterada): mesma fonte, mesma decupagem (mais 1 corte), mesmos objetos |
| Data | 21/11/2026 |
| Duração da REV2 | **15:25,1** = gancho 30,9 s + corpo 13:35,0 + fechamento 59,2 s + tela final 20 s |
| Estado | **Prévia para aprovação**, 540p, **com música**, narrações ainda como texto (a gravar). Nada definitivo foi renderizado (seu pedido: um render só, depois de aprovar tudo) |

## 1. O que você pediu em 21/11/2026 e o que foi feito

| # | Pedido | Feito |
|---|---|---|
| 1 | Subi os MP3 na pasta música | 21 faixas (25 arquivos, com repetidas), 3 por seção. Escolhi uma por seção, medindo cada uma, e mixei (`MUSICA_REV2.md`) |
| 2 | Tirar o `keen` do início do vídeo | Saiu do gancho (prévias e mixagem) |
| 3 | Mais vídeo de canal no gancho | 4 planos de canal (era 1): Rozenhoedkaai, canal com a torre da igreja, canal com bandeiras e barcos, canal entre casas de tijolo. Carruagens e Belfort foram para o fechamento. Gancho: 28,2 s → 30,9 s |
| 4 | Frases mais impactantes no fim, além dos custos; melhorar "Bruges é o que você imagina da Europa antes de ir pra lá" | Fechamento novo (F1–F9) em `ROTEIRO_NARRACAO_REV2.md`. F1: "Sabe aquela Europa que você imagina antes de conhecer a Europa? Ela existe. E se chama Bruges." Mais: canal em cada esquina, cheiro de chocolate e waffle, Patrimônio Mundial da UNESCO (desde 2000, conferido no site da UNESCO), "um dia é suficiente pra conhecer, mas não pra querer ir embora", "o de Bruges, a gente nunca vai esquecer" |
| 5 | O waffle foi 4,7 | 2ª ida ao Chez Albert: € 4,70 (sem o "a confirmar"). Total do dia € 132,00; com hotel € 275,76; € 137,88 por pessoa ≈ R$ 833,84 |
| 6 | "É 14 às 16, corrija minha frase" | Saiu da sua fala "e ele fica exposto das 12 às 16 horas, e eu não sabia disso" (6:15 da fonte). Ficou: "…a igreja que tem o sangue de Cristo. Nós temos sorte, a gente entrou, era exatamente 12 horas…" (conferido com uma 2ª transcrição). O horário certo entra escrito na tela nesse momento: "horário da relíquia: todo dia, das 14h às 16h" (6:21,7). A dica do fechamento (F7) fala "das 14 às 16 horas" |

## 2. Para aprovar

| O quê | Onde |
|---|---|
| Roteiro novo para gravar (gancho igual, fechamento novo) | `ROTEIRO_NARRACAO_REV2.md` + `previas/rev2_gancho.mp4` e `previas/rev2_fechamento.mp4` (contador) |
| Vídeo inteiro com música | `previas/rev2_previa_540p.mp4` (o nome da faixa aparece no topo em cada trecho de música) |
| Só os trechos com música | `previas/rev2_musica_secoes.mp4` |
| Faixas escolhidas e alternativas | `MUSICA_REV2.md` |
| Efeitos (minutos novos) | `efeitos_rev2.md` · takes: `takes_rev2.md` |

## 3. Decisões minhas que precisam do seu OK

| # | Decisão | Alternativa |
|---|---|---|
| 1 | Uma faixa por seção (7 no total: abertura, 5 no corpo, fechamento), escolhidas por medição | Trocar qualquer uma pelas alternativas de `MUSICA_REV2.md` |
| 2 | Na frase da relíquia, saiu a oração inteira (não só "das 12 às 16"): cortar só os números deixava "ele fica exposto… e eu não sabia disso" sem sentido | Grave uma frase curta para entrar ali, por cima de uma imagem da Basílica: "a relíquia fica exposta das 14 às 16 horas" |
| 3 | Fechamento com 59 s (o documento do vídeo longo pede 30–45 s) | Tirar a F3 (UNESCO) |
| 4 | "Um dia é suficiente pra conhecer, mas não pra querer ir embora" na sua voz | Trocar, se não for o que você sente |

## 4. Divergências registradas

As da REV1 continuam (legenda que acende palavra a palavra e sem scrim; sem grão; Recibo dentro do gancho; Placa + recorte de foto implementado). Nova:
- **`keen`:** o padrão de 19/11 (CLAUDE.md, 12) diz "em todo vídeo, o keen toca no fim do gancho". Você pediu para tirar deste vídeo. Não mexi no CLAUDE.md: se o `keen` não deve entrar em nenhum vídeo longo do YouTube, me peça e eu registro.

## 5. Pendências

**Do Diego**
- [ ] Gravar G1–G5 (se ainda não gravou) e o fechamento novo F1–F9, e subir na pasta Bruges/Youtube.
- [ ] Aprovar as faixas (`previas/rev2_musica_secoes.mp4`) e a prévia inteira.
- [ ] Mandar a atribuição das 7 faixas escolhidas (a tabela do Claude no Chrome, ou conferir no Studio).
- [ ] Responder as decisões da seção 3 e as pendentes da REV1 (`rev1/QA_REV1.md`, seções 4 e 5).

**Do Claude (depois disso)**
- [ ] Encaixar as narrações pelo que foi dito e mixar (voz por cima da música da abertura e do fechamento).
- [ ] Tratamento de áudio, `.srt`, descrição (créditos: foto da relíquia, OpenStreetMap, músicas que pedirem), capítulos, títulos e thumbnails.
- [ ] Render final único depois da aprovação.

## 6. Como refazer

De `reels/bruges-yt/`, com o ambiente da REV1 (`CONTINUAR_BRUGES.md`) e as faixas em `fonte/musica/` (IDs do Drive em `dados/musica_ids_drive.tsv`):

1. `python -I scripts/decupar.py rev2` (71 cortes)
2. `python -I rev2/previas_narracao_rev2.py` (prévias da narração)
3. `python -I rev2/montar_rev2.py` e `bash rev2/renderizar_previa_rev2.sh` (faz a música com `rev2/musica_rev2.py` e mixa)
4. `python -I rev2/cortes_musica_rev2.py` (só os trechos com música)
