# Decupagem de Disney e Paris · análise do Drive de 15/10/2026

**Fonte:** pastas `Youtube/Disney` e `Youtube/Paris`, analisadas pelo caderno do Colab (`scripts/colab_analise_drive.ipynb`) e lidas pelo conector do Drive em `Youtube/analise/Disney` e `Youtube/analise/Paris` (`indice.tsv`, `transcricoes.tsv`, `resumo.json`, folhas de contato). Mesmo método e mesmos limites de `DECUPAGEM_MADRID.md`.

## 1. O que foi analisado e o que não foi

| Item | Disney | Paris |
|---|---|---|
| Vídeos analisados | **244 de 244**, 0 erros, 31 min (GPU T4) | **238 de 238**, 0 erros (rodada anterior, sem GPU na última passada) |
| Dia | Qua 18/03/2026, de 08h56 a 23h26 | Ter 17/03/2026, de 11h29 a 21h05 |
| Metadados | Hora com fuso (+01:00), GPS em quase todos, iPhone 17 Pro, 4K HLG (HDR) | Idem |
| Quadros vistos por mim | **Folha 28 de 31** (19h08 a 19h28) | **Folha 25 de 30** (17h30 a 17h44: fachada e interior da Notre-Dame) |
| Folhas ainda não vistas | 30 de 31 | 29 de 30 |
| Quadros girados | Corrigidos nesta rodada (as folhas saem em pé) | **Ainda girados** nos clipes verticais (rodada antiga). O vídeo em si está certo. Para refazer só os quadros: `REFAZER_GIRADOS = True` na célula 4 |
| Transcrição | Automática, não ouvida por ninguém. Nomes saem deturpados ("Crush Pusta", "Catedral de Montenegro", "Mason Alfred") | Idem |

**Cor:** quase tudo é 4K em HLG (HDR, `arib-std-b67`); as exportações de editor (nomes com código `.mp4`) são `bt709`. Converter o HLG para SDR antes de misturar, senão a cor muda no corte.

## 2. Disney · quarta, 18/03 (2 parques em 1 dia)

| Hora | Arquivo | Dur. | O que mostra e o que é dito |
|---|---|---:|---|
| 09:01 a 09:03 | IMG_3200, 3201 | 5 e 32 s | Saída do hotel rumo ao parque, de RER. "Bom dia! O bendito dia chegou!". "E hoje vamos fazer os dois parques em um dia" |
| 09:47 | IMG_3210 | 28 s | Entrada: "são 10 horas da manhã… vamos ver quantos brinquedos a gente consegue ir… a Marina vai chorar no show de fogo hoje" (a aposta) |
| 10:04 a 10:49 | IMG_3220, 3227 | 9 e 21 s | **Primeiro brinquedo** (Walt Disney Studios, área do Nemo): "a gente foi no single rider, tava dando uns 30 minutos de fila" |
| 10:51 a 10:54 | IMG_3232, 3235 | 14 e 13 s | **Brinquedo fechado:** "estamos decepcionados, está em reforma. Era o brinquedo do Ratatouille" (surpresa real) |
| 11:15 | IMG_3256 | 16 s | Atração dos carros: "é bem infantilzinho, mas é bem legal" |
| 11:27 a 11:51 | IMG_3266, 3269 | 14 e 19 s | Hollywood Tower (a "Tower of Terror") e a fila. A hora do clima: "o dia que está fazendo. A gente foi realmente presenteado" |
| 12:08 a 12:33 | IMG_3273, 3283 | 23 e 44 s | Torre vista de fora e o relato de quem acabou de descer. "Você vai 50 vezes e acha que vai morrer" |
| 12:58 | IMG_3297 | 18 s | **Vingadores:** "a mais rápida do parque… vale muito a pena" |
| 13:05 | IMG_3303 | 38 s | Simulador do Homem-Aranha (interativo). "Nosso último brinquedo desse parque" |
| 14:14 a 14:16 | IMG_3318, 3319 | 20 e 33 s | Saem do simulador e explicam a ordem dos parques |
| **14:21** | **IMG_3326** | 32 s | **A dica do dia:** com dois parques no mesmo dia, "comece pelo Studios (o menor), termine no Disneyland Park, que tem o castelo e o show de fogos". Entrada no Disneyland Park |
| 14:34 | IMG_3356 a 3358 | 8 a 18 s | Main Street e o **castelo**: "dá para entrar e ver por dentro" |
| 15:21 | IMG_3383, 3387, 3388 | 15 a 42 s | Piratas do Caribe: "o que mais me impressiona é a perfeição das coisas… os robôs" |
| 16:01 | IMG_3411 | 26 s | Montanha-russa de Star Wars: "foi o mais radical que eles fizeram… primeira fileira" |
| 16:18 a 16:41 | IMG_3420 a 3426 | 4 a 24 s | Atração de tiro (Buzz Lightyear) e a brincadeira de perder a Marina |
| 17:13 | IMG_3451 | 21 s | Pizza do Mickey e sobremesa |
| 17:24 a 17:37 | IMG_3452 a 3465 | 5 a 25 s | Espera pela parada na frente do castelo ("já tá lotado") e a parada |
| 18:04 | IMG_3521 | 30 s | Atração do dragão e o plano: "pegar nosso lugarzinho pro show" |
| **19:08 a 19:11** | **IMG_3537, 3538** | 6 e 1 s | **Castelo rosado ao entardecer**, visto na folha. IMG_3538 é selfie dos dois (vertical, 1 s) |
| 19:25 | IMG_3572, 3573 | 23 s | A Marina e o balde de pipoca da Disney que ela comprou |
| 19:28 | IMG_3574, 3575 | 7 e 3 s | Main Street iluminada (visto na folha) |
| 22:01 a 22:16 | IMG_3587 a 3607 | 14 a 43 s | O show da noite. A transcrição não permite dizer o que é cada trecho |
| **22:19** | **IMG_3608** | 54 s | Saindo "mais cedo para não pegar fila no metrô": "a reação dela diz muito sobre o que foi hoje" (a resposta da aposta da Marina) |
| 23:26 | IMG_3610 | 7 s | Já em Paris (GPS 48,8554 2,2877, perto da Torre) |

Exportações com nome de código (`CFEAD1F0…`, `558F19BD…`, `C334E0DB…`, `F2660F17…`): data de exportação, não de gravação. Pelo conteúdo, `F2660F17…` é da noite fria ("a gente esqueceu o casaco") e `C334E0DB…` é de compras.

### Trechos com valor falado (ficam fora de qualquer peça)

| Arquivo | Trecho | O que é |
|---|---|---|
| IMG_3201 | 15,8 a 17,9 s | o valor do trem de ida e volta |
| IMG_3451 | 9,9 a 14,1 s | o valor da sobremesa |
| IMG_3327 | 8,2 a 13,2 s | "ver se acha algo barato porque na Disney é difícil" (opinião de preço, sem valor; evitar por segurança) |

### Conflitos e atenção

1. **Aposta da Marina (IMG_3210, 17 a 22 s):** só vira peça se a reação em IMG_3608 confirmar. Ver os quadros antes de prometer "ela chorou".
2. **Hora de saída:** IMG_3608 é às 22h19. O p624 dizia "10h → 21h" e agora diz "10h → 22h".
3. **Castelo de dia às 14h35:** o clipe verificado (IMG_3359) tem 0,9 s. A IMG_3358 (17 s, 14h34) tem o castelo e a fala.
4. **Nomes das atrações:** vêm da transcrição automática. Conferir no mapa do parque antes de escrever na tela.

## 3. Paris · terça, 17/03 (um dia)

| Hora | Arquivo | Dur. | O que mostra e o que é dito |
|---|---|---:|---|
| 11:29 a 11:49 | IMG_2731 a 2765 | 3 a 26 s | **Champ de Mars** e a Torre: "ela é ainda maior pessoalmente. Mais tarde a gente passa aqui de noite para ver ela brilhar" |
| 11:56 a 11:58 | IMG_2771, 2778 | 18 e 37 s | Ponte sobre o Sena. O ônibus turístico vermelho (**fala com valor**, ver abaixo) e a escolha de andar a pé e de metrô |
| 12:11 a 12:24 | IMG_2780 a 2810 | 4 a 23 s | **Trocadéro:** "cheio de vida, muita música, muita gente" |
| 12:37 a 12:46 | IMG_2811 a 2844 | 2 a 30 s | **Arco do Triunfo:** "saindo da estação do metrô, damos de cara com ele" |
| 13:04 a 13:16 | IMG_2892 a 2895 | 9 a 21 s | **Champs-Élysées** a pé: "mar de gente" |
| 13:48 a 13:55 | IMG_2914 a 2926 | 11 a 32 s | **Praça da Concórdia:** o obelisco e a história da praça (as falas históricas do Diego precisam de conferência) |
| 14:10 a 14:36 | IMG_2957 a 3034 | 4 a 39 s | **Jardim das Tulherias** e **Louvre**: foto da pirâmide, "a gente não vai entrar, o tempo está corrido" |
| 14:51 a 15:10 | IMG_3038 a 3067 | 4 a 28 s | **Galeries Lafayette**: o terraço e a vista, com a Ópera Garnier e a Torre |
| 16:21 a 16:51 | IMG_3074 a 3083 | 3 a 56 s | Almoço num restaurante francês (**fala com valor** em IMG_3082) |
| 17:11 a 17:23 | IMG_3090 a 3108 | 0,3 a 8 s | Chegada à **Île de la Cité** e à praça da Notre-Dame (fachada de 17:22) |
| 17:30 | IMG_3109 | 101 s | Os dois sentados em frente à catedral, conversa sobre o incêndio de 2019 e a reconstrução |
| 17:32 | IMG_3110, 3111 | 5 e 4,5 s | Fachada da Notre-Dame com céu azul (vista na folha) |
| **17:42 a 17:51** | **IMG_3114 a 3125** | 3 a 10 s | **Interior da Notre-Dame**: nave, vitrais e lustres (visto na folha) |
| **18:53** | **IMG_3134** | 65 s | **Jardim de Luxemburgo fechado:** "infelizmente a gente não conseguiu entrar… fica aberto até as 18h30… aqui não dá pra ver o pôr do sol" |
| 18:57 a 18:59 | IMG_3139 a 3144 | 3 a 29 s | Crepe em frente ao jardim |
| 19:33 a 19:36 | IMG_3147 a 3150 | 1 a 37 s | Volta à Torre: "ela brilha de hora em hora, por 5 minutos" |
| 19:48 a 19:49 | IMG_3153, 3154 | 14 e 17 s | **Ponte de Bir-Hakeim**, para ver a Torre brilhar |
| **19:59 a 20:02** | **IMG_3170 a 3185** | 3 a 66 s | **A Torre brilhando**. IMG_3170 (66 s) tem giro +90 |
| 20:19 | IMG_3192 | 61 s | Fecho do dia: "conhecemos 10 pontos turísticos hoje… Paris está aprovada" |
| 21:05 | IMG_3194 | 74 s | Sorveteria (escolha de sabores) |

### Trechos com valor falado (ficam fora de qualquer peça)

| Arquivo | Trecho | O que é |
|---|---|---|
| IMG_2778 | 8,7 a 18,7 s | o preço do ônibus turístico |
| IMG_3082 | 29,3 a 32,0 s | o valor dos dois pratos do almoço (a opinião "valor justo", 25,2 a 29,3 s, também sai) |

### Conflitos e atenção

1. **Dia único em Paris:** na IMG_3134 e na IMG_3192 a fala é "amanhã tem Disney". As peças dizem "único dia em Paris", e está certo.
2. **Contagem de pontos:** o Diego diz "10 pontos turísticos". Pela linha do tempo: Champ de Mars, Trocadéro, Arco do Triunfo, Champs-Élysées, Concórdia, Tulherias/Louvre, Galeries Lafayette, Notre-Dame, Jardim de Luxemburgo (de fora) e a Torre à noite. A conta fecha em 10.
3. **Horário do Jardim de Luxemburgo:** o Diego diz "até as 18h30" (a fala é confusa: "vai 7,5 até as 18h30"). O horário muda com a estação: conferir no site oficial antes de citar um número.
4. **Torre brilhando:** a fala diz "de hora em hora, por 5 minutos". Confirmar na fonte oficial antes de afirmar como regra.
5. **Falas históricas** (obelisco, execuções, Napoleão, a reconstrução da agulha): são da fala dos dois e a transcrição erra nomes. Não publicar como fato sem conferir.

## 4. Como isso mexe no plano

| Peça | Data | O que mudou |
|---|---|---|
| p608 · O castelo da Disney muda de cor | 14/11 | **Confirmado nas folhas:** castelo rosado às 19h08 e 19h11. Entrou IMG_3537 (6,3 s) como plano principal; o gancho "14h35 e 19h11" continua |
| p614 · Notre-Dame reabriu. A gente foi. | — | **Entraram:** interior em IMG_3114 a 3119 (17h42). Cenas, legenda e pendências reescritas |
| p624 · Disneyland Paris: o dia pelo relógio | 06/01 | Roteiro refeito com horas reais (10h04, 11h27, 12h58, 14h21, 14h34, 19h11, 22h19). Gancho "Disney das 10h às 22h." A dica é a do Diego: comece pelo Studios. Saíram "personagens" e "interior às 16h57", que eram palpites |
| p234 · Primeiro dia em Paris | 07/11 | Aviso dos cortes de preço (IMG_3082 e IMG_2778) |
| p264 · 2 erros que a gente não repete | — | Jardim de Luxemburgo comprovado: IMG_3134, 18h53 |

Regra de cidades: sem mudança de datas, **0 violações**.
