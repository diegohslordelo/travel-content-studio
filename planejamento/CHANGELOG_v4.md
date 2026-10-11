# Registro de alterações · painel v3 → v4 (calendário refeito com o acervo do Drive)

**Data:** 11/10/2026 · **Pedido:** Diego (refazer o cronograma com base nos vídeos das pastas do Drive, mais diverso, começando pelo Reel do Atomium de 10/10; simular as pastas vazias) · **Antes:** `versoes/painel-v3-2026-10-11-antes-da-v4.html` · **Depois:** `planejamento-postagens.html` · **Acervo:** `INVENTARIO_DRIVE.md`

## 1. O que mudou

| | v3 (09/10) | v4 (11/10) |
|---|---|---|
| Base de material | 12 brutos + master de Barcelona | ≈ 1.000 vídeos únicos do Drive (Barcelona, Amsterdam, Bruxelas, Bruges, REELS) + o que já estava no repositório |
| Atomium (10/10) | 2 vídeos (720p) | 9 vídeos: chegada, escala, fala e veredito (Nível A) |
| Peças de 10/10 a 07/02 | 87 | 87 (mesmas datas e horários): **48 novas** + **39 da v3 reaproveitadas** com o material do Drive |
| Reels de Barcelona | 14 | 12 (Barcelona deixou de dominar) |
| Reels de Amsterdam / Bruxelas / Bruges | 5 / 3 / 3 | 10 / 7 / 7 |
| Itália | 9 Reels + 6 carrosséis | 4 carrosséis (o Drive só tem fotos de Roma; CLAUDE.md, 10: Itália serve para carrossel) |
| Maior sequência da mesma cidade | 3 | 2 |
| Formatos editoriais | não registrados | campo novo **Formato** em cada peça: POV, corte do vlog, vale ou pula, curiosidade, comida, sem texto, roteiro, preço, comparação, humor, expectativa × realidade… |
| Corte do vlog | não existia | 8 Reels no domingo seguinte a cada vlog do YouTube (25/10, 08/11, 22/11, 06/12, 19/12, 03/01, 17/01) e o do aeroporto |
| Status de material | ok, decupagem, dados, futuro | + **simulado** (Paris, Disney, Madrid e Lisboa, pastas vazias) |

Não mudou: histórico até 09/10, os 8 vlogs do YouTube e os Stories de lançamento e da viagem, a regra dos Shorts (Reels de terça e sábado, no dia seguinte: 30), os testes T1 a T5, as leituras de dados, a interface do painel (só o selo do status novo), Design System, tokens, CLAUDE.md, material bruto.

**Progresso salvo no navegador:** as peças com o mesmo título de uma peça v3 mantiveram o ID (as marcações continuam); as novas usam IDs a partir de `p500` e os Shorts a partir de `p700`.

## 2. Números

    antes de 10/10 mantidos: 11 | mantidos do futuro (YouTube e Stories): 18 | removidos (v3): 118 | peças v4: 87 | shorts: 30
    novas: 48 | reaproveitadas da v3: 39
    por formato: {'Reel': 70, 'Carrossel': 17}
    por pilar: {'Primeiro Dia (série)': 15, 'Chegar sabendo': 39, 'Como foi de verdade': 15, 'Vontade de ir': 18}
    por destino: {'Bruxelas': 8, 'Barcelona': 14, 'Amsterdam': 12, 'Bruges': 8, 'Paris': 7, 'Disneyland Paris': 7, 'Lisboa': 6, 'Vários destinos': 7, 'Itália': 4, 'Madrid': 7, 'Viagem de janeiro': 7}
    reels por destino: {'Bruxelas': 7, 'Barcelona': 12, 'Amsterdam': 10, 'Bruges': 7, 'Paris': 6, 'Disneyland Paris': 6, 'Lisboa': 5, 'Vários destinos': 6, 'Madrid': 5, 'Viagem de janeiro': 6}
    por status: {'Material verificado (Drive ou repositório)': 47, 'Material simulado (pasta do Drive vazia)': 25, 'Aguarda dados do Diego': 8, 'Material futuro (viagem de janeiro)': 7}
    formato editorial (1ª palavra): {'Primeiro dia + curiosidade': 1, 'Primeiro dia': 4, 'Curiosidade': 4, 'Roteiro': 8, 'POV': 2, 'Dica': 6, 'Primeira hora': 1, 'Perrengue real': 1, 'Sem fala': 2, 'Corte do vlog': 8, 'Vale ou pula': 3, 'Comida': 7, 'Sem texto': 4, 'Série': 1, 'Lista': 3, 'Preço': 8, 'Comparação': 4, 'Desejo': 7, 'Humor': 1, 'Expectativa × realidade': 1, 'Identificação': 1, 'Momento': 1, 'Pergunta': 1, 'Anúncio da viagem': 1, 'Ao vivo': 7}
    testes: {'—:': 29, 'T3:A': 5, 'T5:A': 9, 'T4:A': 9, 'T3:B': 6, 'T1:A': 5, 'T4:B': 6, 'T1:B': 7, 'T2:B': 4, 'T5:B': 5, 'T2:A': 2}
    maior sequência da mesma cidade: 2

## 3. Calendário v4 (feed do Instagram)

| Data | Hora | Formato | Destino | Peça | Formato editorial | Material |
|---|---|---|---|---|---|---|
| sáb 10/10 | 11:00 | R | Bruxelas | Atomium: o cristal de ferro gigante de Bruxelas | Primeiro dia + curiosidade | verificado |
| dom 11/10 | 19:00 | R | Barcelona | Camisa do Bahia no Camp Nou | Primeiro dia · identidade | verificado |
| ter 13/10 | 18:30 | R | Amsterdam | Tony's: o chocolate dividido errado de propósito | Curiosidade | verificado |
| qua 14/10 | 18:00 | C | Barcelona | Roteiro do primeiro dia em Barcelona: 18 km a pé | Roteiro | verificado |
| qui 15/10 | 12:30 | R | Bruges | Primeira hora em Bruges: do trem ao cartão-postal | POV · primeira hora | verificado |
| sáb 17/10 | 11:00 | R | Barcelona | Não compre água em Barcelona | Dica | verificado |
| dom 18/10 | 19:00 | R | Bruxelas | Bruxelas tem 3 estátuas fazendo xixi | Curiosidade · lista | verificado |
| ter 20/10 | 18:30 | R | Amsterdam | Primeira hora em Amsterdam: frio e fome | Primeira hora · POV | verificado |
| qua 21/10 | 18:00 | C | Bruxelas | Bruxelas em 1 dia: o roteiro a pé que fizemos | Roteiro | verificado |
| qui 22/10 | 12:30 | R | Paris | Paris: chegamos e o jardim estava fechado | Perrengue real | verificado |
| sáb 24/10 | 11:00 | R | Amsterdam | Amsterdam: o céu ficou rosa no canal | Sem fala · desejo | verificado |
| dom 25/10 | 19:00 | R | Amsterdam | Vale ou pula: Heineken Experience | Corte do vlog · vale ou pula | verificado |
| ter 27/10 | 18:30 | R | Bruges | Vale ou pula: waffle de rua em Bruges | Vale ou pula · comida | verificado |
| qua 28/10 | 18:00 | C | Amsterdam | Amsterdam: 7 comidas de rua que a gente provou | Comida · lista | verificado |
| qui 29/10 | 12:30 | R | Barcelona | O beijo escondido no Bairro Gótico | Curiosidade | verificado |
| sáb 31/10 | 11:00 | R | Disneyland Paris | 2 parques da Disneyland Paris em 1 dia | Primeiro dia · mini-vlog | **simulado** |
| dom 01/11 | 19:00 | R | Lisboa | Lisboa à noite (sem texto) | Sem texto | **simulado** |
| ter 03/11 | 18:30 | R | Vários destinos | 8 cidades, 8 primeiros dias | Série · montagem | **simulado** |
| qua 04/11 | 18:00 | C | Itália | Roma de graça (ou quase): o que vimos sem pagar | Lista · de graça | verificado |
| qui 05/11 | 12:30 | R | Barcelona | € 1 cada, só às quartas: 100 Montaditos | Preço | verificado |
| sáb 07/11 | 11:00 | R | Paris | A Torre Eiffel pisca de hora em hora | Curiosidade | **simulado** |
| dom 08/11 | 19:00 | R | Paris | Primeiro dia em Paris (e era o único) | Corte do vlog · primeiro dia | verificado |
| ter 10/11 | 18:30 | R | Bruxelas | Batata frita belga: por que é diferente | Comida · curiosidade | verificado |
| qua 11/11 | 18:00 | C | Bruges | Bate-volta de Bruxelas a Bruges: como fizemos | Roteiro · transporte | dados do Diego |
| qui 12/11 | 12:30 | R | Vários destinos | Barcelona ou Madrid: qual escolher? | Comparação | **simulado** |
| sáb 14/11 | 11:00 | R | Madrid | Primeiro dia em Madrid | Primeiro dia · POV | **simulado** |
| dom 15/11 | 19:00 | R | Amsterdam | Stroopwafel feito na hora no Albert Cuyp | Comida · ASMR | verificado |
| ter 17/11 | 18:30 | R | Disneyland Paris | Como chegar à Disney saindo de Paris | Dica · transporte | **simulado** |
| qua 18/11 | 18:00 | C | Disneyland Paris | 2 parques da Disney em 1 dia: como dividimos o dia | Roteiro | **simulado** |
| qui 19/11 | 12:30 | R | Barcelona | McDonald's da Espanha × do Brasil | Comparação · humor | verificado |
| sáb 21/11 | 11:00 | R | Disneyland Paris | Disneyland Paris: o castelo ao vivo | Desejo · reação | **simulado** |
| dom 22/11 | 19:00 | R | Disneyland Paris | Vale ou pula: Disneyland Paris em 1 dia? | Corte do vlog · vale ou pula | **simulado** |
| ter 24/11 | 18:30 | R | Vários destinos | A passagem é só o começo (antes da Black Friday) | Preço · sazonal | verificado |
| qua 25/11 | 18:00 | C | Itália | Roma agora cobra pra ver isso (e o teto de € 1) | Preço · novidade | verificado |
| qui 26/11 | 12:30 | R | Bruges | A batata que virou almoço em Bruges | Comida · reação | verificado |
| sáb 28/11 | 11:00 | R | Lisboa | Lisboa: a vista de graça mais bonita | Desejo · dica | **simulado** |
| dom 29/11 | 19:00 | R | Barcelona | Vale ou pula: La Boqueria | Vale ou pula | verificado |
| ter 01/12 | 18:30 | R | Amsterdam | Anne Frank: o que a gente viu sem ingresso | Dica · erro | verificado |
| qua 02/12 | 18:00 | C | Lisboa | Lisboa em 1 dia: o que coube | Roteiro | **simulado** |
| qui 03/12 | 12:30 | R | Bruxelas | A vista mais bonita de Bruxelas é de graça | Desejo · dica | verificado |
| sáb 05/12 | 11:00 | R | Madrid | Um templo egípcio em Madrid, de graça | Desejo · dica | **simulado** |
| dom 06/12 | 19:00 | R | Madrid | Madrid em 2 dias: o que deu pra fazer | Corte do vlog · roteiro | **simulado** |
| ter 08/12 | 18:30 | R | Barcelona | Sagrada Família: projetada como uma floresta | Desejo · curiosidade | verificado |
| qua 09/12 | 18:00 | C | Madrid | Madrid de graça: 6 lugares sem ingresso | Lista · de graça | **simulado** |
| qui 10/12 | 12:30 | R | Bruges | O McDonald's mais bonito que eu já vi | Humor · curiosidade | verificado |
| sáb 12/12 | 11:00 | R | Amsterdam | Vondelpark num dia comum (sem texto) | Sem texto | verificado |
| dom 13/12 | 19:00 | R | Paris | Quanto custa um croissant em Paris | Comida · preço | **simulado** |
| ter 15/12 | 18:30 | R | Bruxelas | Grand Place de dia e de noite (sem texto) | Sem texto · antes e depois | verificado |
| qua 16/12 | 18:00 | C | Itália | Natal em Roma: o que fizemos no dia 25 | Roteiro · sazonal | verificado |
| qui 17/12 | 12:30 | R | Disneyland Paris | Paris + Disney em 2 dias: dá? | Comparação · roteiro | **simulado** |
| sáb 19/12 | 11:00 | R | Bruxelas | Bruxelas em 1 dia: vale parar? | Corte do vlog · vale a pena | verificado |
| dom 20/12 | 19:00 | R | Bruxelas | O doce de Bruxelas que a gente não conhecia | Comida · descoberta | verificado |
| ter 22/12 | 18:30 | R | Amsterdam | Expectativa × realidade: Amsterdam | Expectativa × realidade | dados do Diego |
| qua 23/12 | 18:00 | C | Paris | Paris em 1 dia: o roteiro a pé que fizemos | Roteiro | **simulado** |
| qui 24/12 | 12:30 | R | Amsterdam | Amsterdam à noite, sem pressa | Sem fala · desejo | verificado |
| sáb 26/12 | 11:00 | R | Barcelona | Vista de Barcelona do alto do Montjuïc | Desejo | verificado |
| dom 27/12 | 19:00 | R | Lisboa | Vale ou pula: o pastel de nata mais famoso | Vale ou pula · comida | **simulado** |
| ter 29/12 | 18:30 | R | Vários destinos | Ninguém avisou desse frio | Identificação · humor | verificado |
| qua 30/12 | 18:00 | C | Amsterdam | Amsterdam em 3 dias: o roteiro que fizemos | Roteiro | verificado |
| qui 31/12 | 12:30 | R | Disneyland Paris | Disney: o momento em que valeu | Momento · emoção | **simulado** |
| sáb 02/01 | 11:00 | R | Bruges | O lago do amor de Bruges | Desejo · curiosidade | verificado |
| dom 03/01 | 19:00 | R | Bruges | Waffle de Bruges × waffle de Bruxelas | Corte do vlog · comparação | verificado |
| ter 05/01 | 18:30 | R | Barcelona | Sagrada Família: o ingresso que precisa de antecedência | Dica · erro | verificado |
| qua 06/01 | 18:00 | C | Vários destinos | Quanto custou cada cidade (por dia, por pessoa) | Preço · comparação | dados do Diego |
| qui 07/01 | 12:30 | R | Madrid | O Prado de graça: o horário que quase ninguém usa | Dica · de graça | **simulado** |
| sáb 09/01 | 11:00 | R | Barcelona | Casa Batlló: o que você vê nessa janela? | Pergunta | verificado |
| dom 10/01 | 19:00 | R | Vários destinos | Próximo primeiro dia: [cidade 1] | Anúncio da viagem | dados do Diego |
| ter 12/01 | 18:30 | R | Paris | Onde ver a Torre Eiffel de graça | Dica · de graça | verificado |
| qua 13/01 | 18:00 | C | Itália | Itália em 9 dias: € [total] | Preço | dados do Diego |
| qui 14/01 | 12:30 | R | Madrid | Churros com chocolate em Madrid | Comida · desejo | **simulado** |
| sáb 16/01 | 11:00 | R | Lisboa | Primeira noite em Lisboa | Primeiro dia · POV | **simulado** |
| dom 17/01 | 19:00 | R | Lisboa | Elétrico 28: vale a fila? | Corte do vlog · vale ou pula | **simulado** |
| ter 19/01 | 18:30 | R | Amsterdam | Mercado em Amsterdam: o que compramos e quanto deu | Preço · mercado | dados do Diego |
| qua 20/01 | 18:00 | C | Barcelona | Barcelona: o Gaudí que dá pra ver de graça (e o que pagamos) | Lista · de graça | verificado |
| qui 21/01 | 12:30 | R | Barcelona | Vale a pena ir a Barcelona? A resposta no aeroporto | Corte do vlog · veredito | verificado |
| sáb 23/01 | 11:00 | R | Viagem de janeiro | Primeiro dia em [cidade 1], ao vivo | Ao vivo | futuro |
| dom 24/01 | 19:00 | R | Bruges | Bruges em 15 segundos (sem texto) | Sem texto | verificado |
| ter 26/01 | 18:30 | R | Viagem de janeiro | Primeira hora em [cidade 2]: € [valor real] | Ao vivo | futuro |
| qua 27/01 | 18:00 | C | Madrid | Madrid em 2 dias: € [total] | Preço | dados do Diego |
| qui 28/01 | 12:30 | R | Paris | Paris de dia: do Louvre ao Sena | POV · desejo | **simulado** |
| sáb 30/01 | 11:00 | R | Viagem de janeiro | Primeiro dia em [cidade 2 ou 3], ao vivo | Ao vivo | futuro |
| dom 31/01 | 19:00 | R | Barcelona | Paella, 5 tapas e bebida por € 19 em Barcelona | Preço · comida | verificado |
| ter 02/02 | 18:30 | R | Viagem de janeiro | Vale ou pula: [atração da viagem], ao vivo | Ao vivo | futuro |
| qua 03/02 | 18:00 | C | Viagem de janeiro | [Cidade 1]: o primeiro dia em números | Ao vivo · roteiro | futuro |
| qui 04/02 | 12:30 | R | Vários destinos | Qual cidade foi a mais barata? | Comparação · preço | dados do Diego |
| sáb 06/02 | 11:00 | R | Viagem de janeiro | Primeiro dia em [cidade 3], ao vivo | Ao vivo | futuro |
| dom 07/02 | 19:00 | R | Viagem de janeiro | 3 países, [N] primeiros dias: o balanço | Ao vivo · balanço | futuro |

## 4. Verificações

- Datas e horários idênticos aos da v3 (assert no script); nenhum gancho repetido; no máximo 2 peças seguidas da mesma cidade.
- Chromium headless em 430 px e 1280 px: 159 rotas (todas as publicações de 10/10 em diante, 19 semanas, calendário, destinos, aprendizados) sem erro de JavaScript e sem rolagem horizontal.
- **Não verificado:** o áudio dos brutos (decupagem por miniatura) e o conteúdo das pastas vazias.

## 5. Para refazer ou desfazer

De dentro de `planejamento/`:
```
python3 scripts/reconstruir_v4.py --base versoes/painel-v3-2026-10-11-antes-da-v4.html
```
Peças novas em `scripts/v4_pecas_a.py` e `v4_pecas_b.py`; as reaproveitadas e as semanas em `scripts/reconstruir_v4.py`; funções comuns em `scripts/reconstruir_v3_lib.py`. Rodar o script apaga edições feitas direto no HTML.
**Desfazer:** copiar `versoes/painel-v3-2026-10-11-antes-da-v4.html` sobre `planejamento-postagens.html`.

## 6. Divergências e decisões para o Diego

| # | Ponto | O que fiz |
|---|---|---|
| 1 | “Corte do vlog” cita o vlog na última linha da legenda; a v3 dizia que nenhum Reel existe para anunciar vlog | O corte é conteúdo próprio (gancho, entrega, CTA de envio ou salvamento); o vlog só aparece como informação no fim. Se preferir, tirar a linha |
| 2 | Itália: a v3 tinha 9 Reels de fotos; o CLAUDE.md (10) diz “serve para carrosséis, não para Reels” e o Drive só tem fotos | Segui o CLAUDE.md: Itália só em carrossel |
| 3 | Lisboa: CLAUDE.md diz 1 dia; o painel do YouTube diz “1 noite e 1 manhã” | Mantive “1 dia” nas peças e deixei a pergunta na pendência |
| 4 | Peças simuladas | Nenhuma sai sem trocar os planos [simulado] pelos reais; se o lugar não foi gravado, a peça muda |
| 5 | O Atomium era de 10/10 (ontem) | Se não foi ao ar, publicar hoje às 11:00; o Bahia segue às 19:00 |
