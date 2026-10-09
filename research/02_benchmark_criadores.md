# 02 · Benchmark de criadores de viagem

**Coleta:** 08/10/2026 · **Dados brutos:** `research/dados/` · **Resumo reprodutível:** `research/scripts/resumir_benchmark.py` · **Fontes:** F40 a F47 em `09_fontes_e_bibliografia.md`

## 1. Método e o que este benchmark **não** é

**O que foi feito.** Para 14 canais de viagem (9 brasileiros, 5 internacionais) li, na página pública do YouTube, os 20 vídeos longos e os 30 Shorts mais recentes: título, views, duração e idade aproximada. Olhei 6 miniaturas recentes de 8 canais. Li a descrição pública de cada canal. Para 12 deles faço a análise abaixo; Alemanizando (vida de brasileiro na Alemanha, não é canal de destino) e Sorelle Amore (documentário e estilo de vida) ficam só na tabela quantitativa.

**Critério de seleção.** Pedido do Diego (Diego Berlitz, Estevam) + diversidade: brasileiros de tamanhos diferentes (de 1,49 mil a 2,29 mi de inscritos), casais e canais com forte série, internacionais com vídeo vertical forte, e um canal pequeno com sinal de nicho (Viagem Pra Dois).

**Limites que o leitor precisa conhecer.**
1. **Não assisti aos vídeos.** Estrutura narrativa, ganchos de abertura e uso de humor ficam como "não observado" ou como inferência a partir do título, da miniatura e da duração.
2. **Instagram não foi acessível** (erro 429 e exigência de login). Reels, Stories e relação Reels × YouTube **não** foram observados em nenhum criador.
3. **Views de vídeo recente não estão no pico.** Idade vem de textos como "há 2 meses".
4. **Títulos podem aparecer traduzidos automaticamente** nos canais internacionais (a coleta usou o idioma português). Uso só para ler padrão, não para citar o título original.
5. Mediana de views é de **vídeos ≥ 8 minutos**. A "razão views ÷ inscritos" é uma correlação grosseira: depende de idade do canal, do assunto e de quanto da base é ativa.
6. Nenhuma métrica privada foi usada ou estimada.

## 2. Quadro quantitativo

(`research/dados/benchmark_youtube_2026-10-08.tsv`; n = vídeos longos entre os 20 mais recentes)

| Canal | País | Inscritos | n | Mediana de views | Views ÷ inscritos | Mediana de duração | ≥ 30 min | Longos/mês (aprox.) | Mediana de views dos Shorts |
|---|---|---|---|---|---|---|---|---|---|
| Diego Berlitz | BR | 104 mil | 20 | 42 mil | 0,40 | 41,6 min | 85% | 4,0 | 3,7 mil |
| Leo e Fabi | BR | 279 mil | 20 | 94,5 mil | 0,34 | 47,7 | 100% | ~10 (série intensa) | 3,8 mil |
| Marina Guaragna | BR | 477 mil | 20 | 122 mil | 0,26 | 43,4 | 95% | 5,0 | 47,5 mil |
| Trip Partiu | BR | 657 mil | 19 | 138 mil | 0,21 | 41,6 | 74% | 2,4 | 56,5 mil |
| GetOutside (Ale & Duda) | BR | 524 mil | 20 | 108,5 mil | 0,21 | 35,1 | 70% | 6,7 | 2,5 mil |
| Estevam Pelo Mundo | BR | 2,29 mi | 19 | 121 mil | 0,05 | 38,1 | 79% | 3,8 | 6,0 mil |
| Três Viagens | BR | 241 mil | 20 | 16 mil | 0,07 | 26,1 | 40% | 3,3 | 5,5 mil |
| Viagem Pra Dois | BR | 1,49 mil | 16 | 1,35 mil | 0,91 | 31,2 | 56% | 0,7 | n/d |
| Alemanizando | BR | 255 mil | 18 | 8,5 mil | 0,03 | 19,1 | 33% | 4,5 | 3,3 mil |
| Drew Binsky | INT | 7,47 mi | 20 | 3,25 mi | 0,44 | 34,0 | 70% | 2,5 | 207 mil |
| Kara and Nate | INT | 4,54 mi | 20 | 1,4 mi | 0,31 | 43,6 | 80% | 2,5 | 150 mil |
| Lost LeBlanc | INT | 2,29 mi | 20 | 106 mil | 0,05 | 49,6 | 90% | 4,0 | 18 mil |
| Fearless & Far | INT | 3,11 mi | 20 | 225 mil | 0,07 | 29,5 | 45% | 1,6 | 16 mil |
| Sorelle Amore | INT | 1,01 mi | 20 | 33,5 mil | 0,03 | 16,5 | 5% | 1,8 | 12 mil |

**Leituras que o dado sustenta:**
- **Duração:** entre os canais brasileiros com mediana acima de 90 mil views, a mediana de duração é de **35 a 48 minutos** e 70% a 100% dos vídeos têm 30 minutos ou mais. O vlog de Barcelona (34 min) está na faixa.
- **Cadência:** 2 a 7 longos por mês (Leo e Fabi, em série intensa, ~10). Publicar 1 longo a cada 14 dias (≈ 2 por mês) fica na **borda inferior** da faixa dos canais médios (Trip Partiu, ~2,4) e acima de um canal de 1,5 mil inscritos (0,7 por mês). A coleta não mostra se esses canais têm equipe.
- **Shorts:** a mediana de Shorts de canais brasileiros com 100 a 500 mil inscritos fica entre **2,5 e 6 mil views** (Berlitz, Leo e Fabi, GetOutside, Três Viagens, Estevam). Duas exceções com mediana de 47 a 57 mil: Marina Guaragna (Shorts de curiosidade e explicação) e Trip Partiu (Shorts de pergunta curta, com um de 1,2 mi). Nos canais internacionais grandes, 150 a 207 mil. **Short não é garantia de descoberta; o tema e o gancho decidem.**
- **Razão views ÷ inscritos:** de 21% a 40% em canais brasileiros de 100 a 650 mil inscritos que misturam lugar + preço + opinião + pessoa; 5% a 7% em canais maiores ou mais genéricos. Para o Primeiro Dia isso só serve de **ordem de grandeza** e **não** é meta.
- **Vídeos de "chegada, 24 horas, primeiras impressões"** (25 vídeos de 9 canais, selecionados por palavras no título: "chegamos", "primeiras", "24h", "48h", "72h"; o filtro é frouxo e inclui vídeos que não são de chegada, como o voo de 62 horas do Estevam): mediana de **1,20 vez** a mediana do canal. Marina Guaragna, com a série "CHEGAMOS EM / NA…" (7 vídeos), fica em 1,46; Leo e Fabi, "Caóticas PRIMEIRAS 24 HORAS EM NÁPOLES" (146 mil contra mediana de 94,5 mil), em 1,5. Diego Berlitz tem 2 vídeos desse tipo abaixo da mediana (0,23), ambos sobre destinos asiáticos recentes. **Conclusão defensável:** o ângulo é neutro a ligeiramente favorável. Não é uma alavanca por si só.

## 3. Matriz qualitativa (12 criadores)

Legenda: **[O]** observado nos dados públicos · **[I]** inferido de título, miniatura ou descrição · **[N]** não observado.

**Personalidade, humor e público aparente foram inferidos de títulos e descrições públicas, sem assistir aos vídeos: confiança baixa.** Só a identidade visual (miniaturas), os títulos, as durações e os números são observação direta.

### 3.1 Brasileiros

| Dimensão | **Diego Berlitz** | **Estevam Pelo Mundo** | **Leo e Fabi** | **Marina Guaragna** |
|---|---|---|---|---|
| Posicionamento [O/I] | Guias de cidade na Itália, Flórida, Sudeste Asiático e Austrália; um título diz que o roteiro de Sydney é "de quem já morou aqui" [I] | Milhas, classe executiva, destinos incomuns na Europa e roteiros completos com preços | Viagem + gastronomia + rotina e "experiências reais", casal | Viajante e cultura, com o marido; estilo de documentário leve |
| Proposta de valor [I] | "O que fazer, onde comer e como chegar", com profundidade | Economizar e viajar melhor (milhas) + curiosidade geopolítica | Companhia de casal e comparação com o Brasil (supermercado, McDonald's, preço) | Curiosidade cultural + comida de rua + "chegada" |
| Público aparente [I] | Planejador de Itália e Europa | Planejador com interesse em milhas | Curioso e companheiro de viagem | Curioso e companheiro de viagem |
| Personalidade [I] | Didático, entusiasmado | Direto, sarcástico, explicativo | Humor de casal, autoironia | Descontraída, com opinião |
| Identidade visual (miniaturas) [O] | **Nome da cidade em letras grandes brancas, uma frase curta em barra preta, Diego na cena.** Foto limpa e luminosa | Rosto em reação, nome da cidade e bandeira, pós de cor forte e dramático | Selfie do casal com expressão, bandeira, "EP. 01…" na série | Casal ou pessoa em primeiro plano, **uma palavra gigante** ("LÍTIO", "MENDOZA", "BÉLGICA"), frase de preço "TÁ CARO MESMO?" |
| Estrutura / gancho [N/I] | Não observado; títulos de promessa ("dá pra ver tudo em 2 dias?", "Sonho ou pesadelo?") | Não observado; títulos de pergunta e tensão | Não observado; títulos de pergunta e "A realidade de…" | Não observado; títulos de chegada e de curiosidade |
| Humor, emoção, curiosidade [I] | Curiosidade e utilidade | Curiosidade e indignação | Humor e emoção ("NOS SEPARAMOS" com 102 mil) | Curiosidade e comida |
| Títulos [O] | `[CIDADE]: pergunta ou promessa + (O Que Fazer e Roteiro)`; letras maiúsculas parciais; bandeira de país em alguns | `PERGUNTA EM CAIXA ALTA + bandeira`; "24H EM BUDAPESTE", "PRAGA EM 24 HORAS: O QUE FAZER E QUANTO CUSTA" | Bandeira + frase de curiosidade ("Como é um supermercado na Itália \| Preços…"), série numerada | Frases de chegada ("CHEGAMOS EM AMSTERDAM") e curiosidade ("ELE QUERIA VIR PRA ARGENTINA SÓ PRA ISSO") |
| Duração dos longos [O] | 41,6 min (22 a 96) | 38,1 | 47,7 | 43,4 |
| Shorts / Reels / Stories [O/N] | Shorts de 1 a 7 mil views, mini-guias e opinião ("Minha opinião sincera sobre o Keukenhof"). Reels e Stories **[N]** | Shorts de baixo alcance (6 mil mediana), vários de "notícia/curiosidade" fora de viagem | Shorts de baixo alcance (3,8 mil), mistura promoção de cartão e cortes | **Shorts de 47,5 mil de mediana** (um de 258 mil: "de onde surgiu o doce de leite?"): curiosidade que **responde a uma pergunta** |
| Relação vertical × longo [I] | Shorts sobre o mesmo destino do vídeo da semana | Pouco ligados ao longo | Pouco ligados | Shorts fora do assunto do longo (cultura geral); funcionam como canal de descoberta próprio |
| Séries [O] | "Itália" com sequência de cidades | Séries de destinos e voos | **"ITÁLIA \| EP. 01…", "Japão", "China"** em sequência | "Chegamos em…" + série de países |
| Aspiracional / contemplativo [I] | Capri, Costa Amalfitana: paisagem de miniatura | Cidade ao pôr do sol em miniatura | Pouco | Paisagem em miniatura, sem filmes contemplativos observados |
| Diferenciação [I] | Profundidade e roteiro de cidade pequena | Milhas e voo | Casal em quem se confia + comparação com o Brasil | Documentário leve + cultura |
| **Adaptável ao Primeiro Dia** | Miniatura com **uma palavra de lugar + uma frase curta** é o que o DS já define (placa + máx. 4 palavras) | Pergunta provocadora como título | **Série numerada de uma viagem** ("EP. 01") ajuda o retorno | Série "Chegamos em…" encaixa direto no conceito |
| **Não copiar** | Duração acima de 55 min sem capítulos | Tom de indignação e sensacionalismo geopolítico | Casamento de Shorts com promoção de cartão | Temas políticos nos Shorts |

| Dimensão | **Trip Partiu** | **GetOutside (Ale & Duda)** | **Três Viagens** | **Viagem Pra Dois** |
|---|---|---|---|---|
| Posicionamento [I] | Guia de destino com preços ("melhor roteiro + preços"), apresentadora única | Casal aventureiro; Etiópia, ilhas isoladas, Itália | Família de viajantes; dicas práticas (mala, Wise, internet no exterior) | Casal brasileiro morando na Espanha; custo de vida, compras e festas locais |
| Proposta de valor [I] | "O que ninguém te conta" + preço | Curiosidade extrema e "notas" (ex.: "Fontana di Trevi, nota 5") | Utilidade pura | Preço real e vida local ("Quanto custa um carrinho cheio na Espanha em 2026?" com 77 mil views) |
| Identidade visual [O] | **Template extremamente repetido:** nome do lugar grande + "O QUE NINGUÉM TE CONTA" + bandeira + apresentadora em ponto turístico | Rosto em primeiro plano com texto-gancho numérico ("187 METROS"), setas e mapa | Nome do lugar + bandeira + pessoa; fundo de interior para vídeos de dica | Colorida, muito texto, emojis, preço na capa ("€€€??") |
| Títulos [O] | `LUGAR: melhor roteiro + dicas para economizar` / `vale a pena?` | Frases de situação ("Passamos uma noite no lugar mais quente da terra") | `LUGAR 2026: Roteiro Completo, Quanto Custa` | Pergunta de preço ou de tendência ("PREÇOS NA ESPANHA: Nike, Adidas e Zara são mais baratos?") |
| Duração (mediana) [O] | 41,6 min | 35,1 | 26,1 | 31,2 |
| Shorts [O] | **56,5 mil de mediana** (um de 1,2 mi). Perguntas curtas: "Achou caro ou barato?" | 2,5 mil | 5,5 mil | n/d |
| Série / recorrência [O] | Rótulo "O QUE NINGUÉM TE CONTA" em todas as capas | Séries por país (Etiópia) | Série de dicas de viagem | Série de preço |
| Diferenciação [I] | **Reconhecimento visual** pela repetição do template | Humor e aventura | Dica fácil de achar | Um nicho (Espanha) em que o criador vive |
| **Adaptável** | Template consistente: a **Placa** do DS faz esse papel | Gancho com número na capa | Palavra do ano ("2026") no título de utilidade | Capa com o preço |
| **Não copiar** | Excesso de texto na miniatura | Aventura de risco | Ritmo de dicas sem personalidade | Densidade de emoji |

### 3.2 Internacionais

| Dimensão | **Drew Binsky** | **Kara and Nate** | **Lost LeBlanc** | **Fearless & Far** |
|---|---|---|---|---|
| Posicionamento [I] | Histórias de pessoas e lugares; 197 países; vídeo e Shorts como máquinas de descoberta | Casal de Nashville; aventura e viagens de grande produção; série longa (Mongol Rally) | Largou o emprego para viajar; travessia da África em série | Aventura e tribos |
| Duração [O] | 34 min | 43,6 | 49,6 | 29,5 |
| Mediana de views [O] | 3,25 mi | 1,4 mi | 106 mil | 225 mil |
| Shorts [O] | 207 mil de mediana | 150 mil | 18 mil (vários de bastidor e de produto, como câmera) | 16 mil |
| Série / recorrência [O] | "Um dia com…" | **"Mongol Rally Ep. 1 a 6"** | **"Cruzando a África"** | Séries por país |
| Títulos [I] | Afirmação-choque ("o homem mais solitário do mundo") | Número + tempo ("72 horas na Turquia") | "Perdi meu amigo atravessando a África" | "24 h com a tribo…" |
| Identidade visual [N] | Miniaturas não inspecionadas | idem | idem | idem |
| Aspiracional [I] | Pouco: o forte é história de pessoa | Alto valor de produção em Shorts de "lugar" (trens, hotéis) | Pouco; Shorts de bastidor e de produto | Pouco |
| **Adaptável** | Pergunta direta ao rosto na abertura | **Série com episódios numerados e tempo no título** | Série de uma longa viagem ("Cruzando a África") parecida com a viagem de janeiro | Reconhecimento por assunto |
| **Não copiar** | Risco e sensacionalismo | Custo de produção | Dependência de risco | Estereótipo cultural |

## 4. Padrões que se repetem (e o que viram no Primeiro Dia)

| # | Padrão observado | Onde | Como adaptar | Confiança |
|---|---|---|---|---|
| 1 | **Nome do lugar em 1–2 palavras na miniatura**, rosto visível, bandeira ou objeto de contexto | 8 de 8 canais com miniatura vista | Já no DS 5.5 ("lugar + emoção + prova", máx. 4 palavras) | Alta |
| 2 | **Template recorrente** na miniatura (Trip Partiu, Leo e Fabi, Marina) | 3 de 8 | Placa do DS como elemento fixo; **não** forçar o mesmo texto em todos | Média |
| 3 | **Pergunta de preço** ("tá caro mesmo?", "quanto custa?") | Marina, Três Viagens, Viagem Pra Dois, Berlitz | Alinhado ao Placar e ao Recibo | Alta |
| 4 | **Duração de 35 a 50 min** nos canais brasileiros com mediana acima de 90 mil views | 6 canais | Manter os vlogs de ~34 min; não encurtar para ficar "dinâmico" | Média |
| 5 | **Série numerada de uma viagem** | Leo e Fabi, Kara and Nate, Lost LeBlanc | Viagem de janeiro como série numerada | Média |
| 6 | **Dispersão enorme de Shorts em canais do mesmo porte**: medianas de 2,5 mil (GetOutside) a 56,5 mil (Trip Partiu) com 500 a 650 mil inscritos. Os Shorts mais fortes são de curiosidade com resposta (Marina) e perguntas curtas (Trip Partiu), mas GetOutside também usa perguntas e fica em 2,5 mil | Marina, Trip Partiu, GetOutside | **Não há padrão causal claro.** Tratar o Short como teste de tema, não como fórmula | Baixa |
| 7 | **Títulos de chegada** funcionam acima da média em alguns canais | Marina, Leo e Fabi | Série "Primeiro dia" como já planejado | Baixa-média |
| 8 | Canal pequeno (1,5 mil) tem views ≈ inscritos nos longos, e picos em temas de **preço** | Viagem Pra Dois (77 mil em "carrinho cheio na Espanha") | Custo é mais "alcançável" que beleza | Baixa (1 canal) |

## 5. Diferenciais possíveis do Primeiro Dia frente ao conjunto

1. **Recibo e cotação datada** (DS): nas miniaturas e nos títulos observados, nenhum canal mostra o gasto como objeto visual recorrente com hora (os vídeos em si não foram assistidos). É a diferença mais concreta e já existe.
2. **Chegada como unidade editorial** (não só "roteiro de 3 dias"): lacuna aparente em F41.
3. **Perrengue carimbado** e **ticket de surpresa** (DS): linguagem própria.
4. **Casal sem virar canal de casal**: Leo e Fabi e GetOutside são canais de casal, com audiência que os acompanha como casal. O Primeiro Dia tem decisão editorial diferente (CLAUDE.md, 2). **Risco:** perder o benefício de identificação do casal; **ganho:** coerência com a marca.

## 6. Práticas que **não** copiar

| Prática | Por quê |
|---|---|
| Títulos de risco ou indignação | Conflita com o tom ("curioso, mas não deslumbrado; transparente, mas não reclamão") |
| Miniatura com mais de 4 palavras | Quebra o DS 5.5 |
| Shorts de promoção de cartão ou desconto sem divulgação | Exige identificação (CONAR 2026, F32) |
| Miniatura ou título que promete o que o vídeo não entrega | Prejudica tempo assistido valorizado (F07) |
| Publicar Short com a marca d'água de outra rede | Política de originalidade (F01, F08) |

## 7. Visuais e aspiracionais: o que este benchmark **não** conseguiu cobrir

A parte pedida de **benchmarking visual aspiracional** (criadores só de imagem, música e atmosfera, sem fala) não foi feita por perfil. A razão: esse tipo de conteúdo mora no Instagram, que não foi acessível. O que foi possível:

- **Amostra pública do YouTube** (F42): 283 Shorts de estética de cidade europeia. Mediana de 842 views; 18% acima de 10 mil; 10,6% acima de 100 mil; 1,1% acima de 1 milhão. Vencedores típicos têm **gancho de pergunta, lista ou comparação** ("IG vs Reality: Paris" com 31 mi; "5 things to do in Paris" com 2,8 mi) e não só imagem bonita.
- **Filmes de viagem cinematográficos** (F41): mediana por cidade entre 1,3 mil e 6 mil views, com poucos acima de 100 mil. Mediana da busca "cinematic Lisbon travel": 2,3 mil views (13 resultados).
- **Caminhadas ambientais longas** (sunset walking tours): 141 mil a 2 mi de views em vídeos de 40 a 80 minutos. Formato diferente: sem edição, som ambiente, longa duração.

**Viés conhecido:** são resultados de busca ordenados por relevância; **não** são uma amostra aleatória, e a seleção favorece vídeos populares. Mesmo assim, a mediana é baixa. Para o Primeiro Dia isso significa: **o aspiracional entra com expectativa realista e com um teste**, como descrito em `04` e `07`.

## 8. Oportunidades de teste derivadas

| ID | Teste | Origem |
|---|---|---|
| B1 | Título com **pergunta de preço** × título com **afirmação de chegada** nos vlogs (usar Test & Compare se disponível) | Padrões 3 e 7 |
| B2 | Short **feito para o YouTube** (tema de busca ou curiosidade, cortado do vlog) × Short que **repete o Reel** | Padrão 6 |
| B3 | Série numerada da viagem de janeiro × episódios soltos | Padrão 5 |
| B4 | Miniatura com Placa fixa × miniatura sem Placa | Padrão 2 |
