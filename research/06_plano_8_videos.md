# 06 · Inventário e plano de reaproveitamento dos oito vídeos

**Data:** 08/10/2026 · **Fontes internas:** `planejamento/planejamento-postagens.html` (campo `videos` e posts), `reels/apresentacao/` (transcrição do vlog de Barcelona, transcrições de clipes de chegada, lista de cortes, RESUMO), CLAUDE.md, seções 2 e 10

## 1. O que consegui e o que não consegui analisar

| Vídeo | Arquivo acessível aqui? | O que usei | Nível de conhecimento |
|---|---|---|---|
| **Barcelona** (3 dias, ~34 min) | **Não** (master de 10 GB fica em `fonte/`, fora do git, no gofile citado em RESUMO.md) | **Transcrição automática completa** (`reels/apresentacao/transcricao.srt`, 439 trechos), lista de cortes da REV8, RESUMO | Alto para estrutura e fatos ditos; **nada** sobre imagem, cor, foco ou áudio além do que RESUMO registra |
| **Amsterdam** (3 dias) | Não | 3 clipes de chegada transcritos (IMG_1375, 1384, 1393) + texto do painel | Baixo |
| **Paris** (1 dia) | Não | 3 clipes transcritos (IMG_2730, 2761, 3134) + painel | Baixo |
| **Disneyland Paris** (2 parques, 1 dia) | Não | Só o painel e a fala de véspera (IMG_3134: "amanhã tem Disney") | Mínimo |
| **Madrid** (2 dias) | Não | Só o painel | Mínimo |
| **Bruxelas** (1 dia) | Não | 2 clipes transcritos (IMG_2170: Atomium; IMG_2178: sem fala) + painel | Baixo |
| **Bruges** (1 dia) | Não | 4 clipes transcritos (IMG_2690 a 2693) + painel | Baixo |
| **Lisboa** (1 noite e 1 manhã) | Não | Só o painel | Mínimo |

**Limitações assumidas** (regra do projeto: não afirmar ter analisado o que não foi acessível):
- **Nenhum vídeo foi assistido.** Para os 7 vlogs além de Barcelona, **não sei** se estão editados, qual a duração, o que mostram além do que o painel promete. O painel marca só Barcelona como `pronto: true`.
- A transcrição de Barcelona é **automática** (modelo de reconhecimento de fala): há erros de grafia e de nome (ex.: "Valdir" por Gaudí, "Fontsep" para um app, "R$" onde deve ser "€"). **Atribuição de falante é incerta**: o texto alterna entre "eu", "a gente", "ele" e "ela" sem marcar quem fala.
- **Áudio:** não escuto áudio (CLAUDE.md, 12). O padrão `docs/AUDIO_REVIEW_STANDARD.md` v1.1.0 (08/10/2026) exige revisão de áudio com **escuta humana** antes de publicar vídeo longo, e diz que **ainda não foi testado em nenhum vídeo real**. Se o vlog de Barcelona sai em 10/10, o Diego precisa confirmar se essa revisão foi feita.
- **Trilha:** o RESUMO registra "trilha de violão em quase todo o B-roll" do master de Barcelona. Confirmar a **licença** da trilha antes de publicar (identificação automática de música no YouTube).

---

## 2. Inventário

Legenda: **[T]** extraído da transcrição; **[P]** do texto do painel; **[C]** de clipe transcrito; **[N]** não observado.

### 2.1 Barcelona

| Campo | Conteúdo |
|---|---|
| **Identificador** | `bcn` · post `p13` · sábado 10/10/2026, 11:00 · `pronto: true` |
| **Destino e tema** | Barcelona, 3 dias, primeira cidade da série. Tema: "quanto gastamos nos 3 dias e o que eu faria diferente" [P] |
| **Experiência central** | Três dias a pé (cerca de 18 a 20 km no primeiro dia) com ingressos comprados antes, bilhete de 72 h, alimentação econômica e uma opinião clara sobre o que vale entrar e o que ver por fora [T] |
| **História ou conflito** | Camp Nou **em reforma** (o estádio não abre); La Rambla "toda em obra", com britadeira; Boqueria "pega-turista"; cansaço do primeiro dia; Casa Batlló e Casa Vicens vistas por fora por escolha ("não é muito nossa praia") [T] |
| **Momentos relevantes** | Chegada às 1h da manhã e primeiro dia em Gràcia (00:00); Camp Nou e ingresso (01:00); Montjuïc (03:21); Barceloneta e McDonald's (04:34); primeira tapa (10:30); Gótico e Mural do Beijo (12:41); Rambla e Boqueria (18:36 a 20:01); Sagrada Família (23:55); Parc Güell (29:44); balanço no aeroporto (33:20) [T] |
| **Conteúdo informativo (dito no vlog)** | Camp Nou **€ 31** no site oficial · bilhete de metrô e ônibus de **72 h por € 27,50** · Sagrada Família **€ 25** por pessoa, vendas abrem **1 mês antes**, 9:30 já está cheia · promoção de **5 tapas + paella + bebida por € 19** · 100 Montaditos **€ 1** nas quartas · Casa Batlló "acho que cerca de € 15" (não entrou) · café da manhã no mercado para economizar · fontes de água públicas e app de localização · Boqueria é cara. **Todos a conferir** contra o registro real (CLAUDE.md, 9) |
| **Potencial emocional** | Alto no fim ("não é à toa que é a minha cidade preferida"); Sagrada Família ("surreal") [T] |
| **Potencial de humor** | Alto: McDonald's de cada país (Korean BBQ), cerveja que "é como comprimido de remédio", "Bahia é o mundo" (funcionário do museu), brincadeira do Mural do Beijo [T] — **atribuição de falante a confirmar** |
| **Cenas de destaque** | Barceloneta, Montjuïc, Arco do Triunfo ao fim da tarde, Catedral, Plaça Reial, Casa Batlló por fora, Parc Güell com vista, Sagrada Família interior [T] |
| **Oportunidades de abertura** | (a) Aeroporto, balanço final com o total; (b) "Camp Nou: o estádio está em reforma" (01:56); (c) Rambla em obras (18:50) |
| **Cortes verticais possíveis** | Ver 3.2 |
| **Cenas aspiracionais** | Barceloneta, Montjuïc, Parc Güell, Arco, Plaça Reial; evitar o interior da Sagrada Família (música do próprio local) |
| **Limitações** | Master 4K HDR/HLG, 24 fps; trilha de violão em quase todo o B-roll; cena do museu do Barça desfocada (descartada na REV5); alguns brutos têm música de rua (Montjuïc) [RESUMO] |
| **Informações faltantes** | Total real da viagem e câmbio datado; quem fala em cada trecho; ano da viagem; arquivo final do YouTube (se for o mesmo master); licença da trilha; resultado da revisão de áudio |

### 2.2 Amsterdam

| Campo | Conteúdo |
|---|---|
| **Identificador** | `ams` · `p34` · 24/10/2026 · `pronto: false` · "Edição pronta até 17/10" (semana 3) |
| **Destino e tema** | Amsterdam, 3 dias. Tema do painel: "o primeiro dia, o hotel e quanto gastamos" [P] |
| **Experiência central** | Chegada de avião com frio, hotel, "vamos passar 3 dias e acho que vai dar tempo de fazer tudo" [C] |
| **História ou conflito** | Frio ("Tá frio?", "tá muito frio"); decidir museus × centro: "a gente não vai vir aqui hoje" (Praça dos Museus), museus ficam para depois [C] |
| **Momentos relevantes** | Pouso e chegada com a mala (IMG_1375, 1384); passagem pela Praça dos Museus; fome e vontade de cerveja ("terra da Heineken e da Amstel") (IMG_1393) [C] |
| **Conteúdo informativo** | Não observado além do painel (hotel, custo) |
| **Potencial emocional / humor** | Moderado (frio, fome) [C]; demais [N] |
| **Cenas de destaque, abertura e cortes** | Aeroporto com frio; chegada com a mala; Praça dos Museus [C]; restante [N] |
| **Cenas aspiracionais** | Praça dos Museus [C]; restante [N] |
| **Limitações** | Clipes em celular, alguns HDR; áudio dos brutos mistura fala e ambiente [RESUMO] |
| **Informações faltantes** | Tudo que está além dos 3 clipes: o vlog, o hotel, os custos, a edição |

### 2.3 Paris

| Campo | Conteúdo |
|---|---|
| **Identificador** | `par` · `p55` · 07/11/2026 · `pronto: false` · "Edição pronta até 31/10" |
| **Destino e tema** | Paris em **1 dia**; "se dá pra ver o essencial" [P]; véspera da Disney [C] |
| **Experiência central** | "Um dia turistando" para ver o máximo e "comer das melhores comidas" [C] |
| **História ou conflito** | **Jardim de Luxemburgo fechado**: o plano de ver o pôr do sol lá não deu porque o jardim fecha às 18:30 no dia (horário dito: 7:30 às 18:30); precisou procurar outros pontos de pôr do sol e deixar a Torre Eiffel à noite [C, IMG_3134] |
| **Momentos relevantes** | Chegada ao novo destino, com o plano de "um dia turistando" (IMG_2730); selfie com a Torre Eiffel, **sem fala** (IMG_2761); jardim fechado e dica de horário (IMG_3134) [C] |
| **Conteúdo informativo** | Horário do Jardim de Luxemburgo (vale como dica, **sazonal: conferir**) [C] |
| **Potencial emocional / humor** | Médio (frustração honesta com plano B) [C] |
| **Cenas aspiracionais** | Torre Eiffel à noite (prevista na fala; confirmar se foi gravada) [C] |
| **Perrengue verdadeiro** | **Sim**: jardim fechado. É candidato real a "Não faça isso em Paris" ou "Paris em 1 dia: o que faltou" (p64) |
| **Informações faltantes** | Restante do dia; custos; se a Eiffel à noite foi gravada |

### 2.4 Disneyland Paris

| Campo | Conteúdo |
|---|---|
| **Identificador** | `dis` · `p76` · 21/11/2026 · `pronto: false` · "Edição pronta até 14/11" |
| **Destino e tema** | 2 parques em 1 dia; "se os 2 parques cabem em 1 dia e quanto custou" [P] |
| **Experiência central, história, momentos** | **Não observado.** O painel prevê Reels de fila ("Fila na Disneyland Paris: [X] minutos") e de "momento mais emocionante": ambos dependem de dados que só existem no vlog |
| **Alerta de áudio** | O painel já pede "sem músicas do parque; áudio da biblioteca ou ambiente" |
| **Informações faltantes** | Praticamente todas |

### 2.5 Madrid

| Campo | Conteúdo |
|---|---|
| **Identificador** | `mad` · `p97` · 05/12/2026 · `pronto: false` · "Edição pronta até 28/11" |
| **Destino e tema** | 2 dias; "se 2 dias valem a pena e quanto custou" [P] |
| **Demais** | **Não observado.** Reels de comida e de erro previstos |
| **Informações faltantes** | Praticamente todas |

### 2.6 Bruxelas

| Campo | Conteúdo |
|---|---|
| **Identificador** | `bxl` · `p118` · 19/12/2026 · `pronto: false` · "Edição pronta até 12/12" |
| **Destino e tema** | 1 dia; "se vale a pena parar por 1 dia" [P] |
| **Experiência central** | Primeira parada **Atomium**, de metrô; "obrigatório" mas "mais distante do centro"; optaram por **não subir**; "cristal de ferro aumentado 165 bilhões de vezes, feito para a exposição de 1958" [C, IMG_2170] |
| **Conteúdo informativo** | Atomium: acesso por metrô, fica fora do centro, decidiram não subir (custo do ingresso não dito) [C] |
| **Potencial emocional / humor** | Médio (espanto com a escala e a modernidade de uma obra de 1958) [C] |
| **Cenas aspiracionais** | Atomium (IMG_2170); IMG_2178 sem fala [C] |
| **Observação** | O painel diz "Bruges, bate-volta de Bruxelas" (CLAUDE.md, 10) |
| **Informações faltantes** | Restante do dia, custos, ingresso do Atomium |

### 2.7 Bruges

| Campo | Conteúdo |
|---|---|
| **Identificador** | `brg` · `p139` · 02/01/2027 · `pronto: false` · "Edição pronta até 26/12" |
| **Destino e tema** | 1 dia; "se Bruges é tão bonita quanto dizem" [P] |
| **Experiência central** | Cena de doces e waffle; rua histórica; "Muito, muito, muito, muito" (reação à beleza, voz de Marina) [C, IMG_2690 a 2693] |
| **Potencial emocional / humor** | Alto na reação à beleza [C]; humor no teste de chocolate (fala truncada na transcrição) [C] |
| **Cenas aspiracionais** | Rua histórica (usada na apresentação, IMG_2693 12,4 a 15,4 s); Place de Brugge ao fundo [LISTA_DE_CORTES] |
| **Limitações** | Transcrição de IMG_2690 e 2691 ilegível em parte; IMG_2691 saiu com caracteres de idioma errado |
| **Informações faltantes** | Restante |

### 2.8 Lisboa

| Campo | Conteúdo |
|---|---|
| **Identificador** | `lis` · `p160` · 16/01/2027 · `pronto: false` · "Edição pronta até 09/01"; **serve de reserva** se outro vídeo atrasar [painel] |
| **Destino e tema** | "1 noite e 1 manhã"; "o que cabe" [P] |
| **Demais** | **Não observado** |

---

## 3. Barcelona: capítulos, fatos e mapa de cenas

### 3.1 Sugestão de capítulos para a descrição (a conferir)

Horários vêm da transcrição automática do master de 34 min. **Se o vídeo publicado for outro corte, os horários mudam.** Capítulos do YouTube precisam começar em `00:00`, ter pelo menos 3 itens e ao menos 10 s cada.

| Horário | Capítulo |
|---|---|
| 00:00 | Chegada em Gràcia e o plano dos 3 dias |
| 00:56 | Camp Nou: ingresso e estádio em reforma |
| 03:04 | Bilhete de transporte de 72 horas |
| 03:21 | Montjuïc |
| 04:34 | Barceloneta e almoço |
| 08:30 | Parc de la Ciutadella e Arco do Triunfo |
| 09:42 | Café da manhã econômico no mercado |
| 10:30 | Primeira tapa e fim do dia 1 |
| 10:57 | Dia 2: Casa Vicens e Bairro Gótico |
| 16:01 | Almoço: promoção de tapas por € 19 |
| 18:36 | La Rambla em obras e Boqueria |
| 20:51 | Casa Batlló e Casa Milà |
| 22:59 | Jantar |
| 23:55 | Dia 3: Sagrada Família |
| 27:30 | Churros e empanadas |
| 29:44 | Parc Güell |
| 32:24 | Tapas, 100 Montaditos e balanço no aeroporto |

### 3.2 Peças derivadas de Barcelona, com **uma cena de abertura por peça**

**Cenas já "gastas" no histórico** (evitar nas peças futuras): Sagrada (plano externo), El Vaso de Oro, Arco com Diego de costas, chegada ao Camp Nou, brinde com patatas bravas, selfie em Gràcia, Barceloneta (fechamento da apresentação). Os brutos IMG_0502 a IMG_1192 estão em `fonte/`.

| # | Peça | Data | Plataforma | Pilar | Cena de abertura e trecho (T) | Gancho (≤ 7 palavras) | Duração teste | Texto de capa | CTA | Métrica principal |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Trailer (`p15`) | 10/10 | Reel | 1 | Aeroporto + placar final (33:20) | "Barcelona em 3 dias: € [total]." | 20–30 s | `€ [TOTAL]` | Ver o vídeo completo | Cliques/visitas ao perfil |
| 2 | Primeiro dia (`p16`) | 11/10 | Reel | 1 | Camp Nou em reforma (01:56) + Rambla em obras (18:50) + Boqueria cara (19:36) | "O que ninguém avisa de Barcelona." | 20–30 s | `NINGUÉM AVISA` | Enviar | Envios por alcance |
| 3 | Custo (`p19`) | 13/10 | Reel | 2 | Recibo com os valores falados (€ 31, € 27,50, € 25, € 19) **conferidos** + total real | "Onde foi o dinheiro em Barcelona?" | 20–30 s | `ONDE FOI?` | Salvar | Salvamentos |
| 4 | Erro (`p22`) | 15/10 | Reel | 2 | **A confirmar com o Diego**: a transcrição não registra um erro claro. Se não houve, usar "Boqueria: pega-turista" como aviso | "Não faça isso em Barcelona." | 20–35 s | `NÃO FAÇA` | Salvar | Retenção |
| 5 | Primeiro olhar (`p190`) | 16/10 | Reel | 6 | Montjuïc, Barceloneta, Güell (3.1 de `04`) | "Barcelona: o primeiro olhar." | 12–20 s | `BARCELONA` | Enviar | Envios por alcance |
| 6 | Curiosidade (`p25`) | 18/10 | Reel | 3 | Fontes de água públicas e app (18:05) | "Barcelona faz isso diferente do Brasil." | 15–25 s | `FONTE DE ÁGUA` | Enviar | Retenção |
| 7 | Carrossel de roteiro (`p21`) | 14/10 | Carrossel | 2 | Roteiro dos 3 dias com paradas e horas | "Barcelona em 3 dias: o que fizemos e quanto custou" | — | `3 DIAS` | Salvar | Salvamentos |
| 8 | Carrossel "se eu voltasse" (`p30`) | 21/10 | Carrossel | 2 | Dicas ditas: comprar Sagrada com 1 mês de antecedência, ver Casa Batlló por fora, almoço com promoção | "Se eu voltasse a Barcelona, faria diferente" | — | `FARIA DIFERENTE` | Salvar | Salvamentos |
| 9 | Momento bruto (Short `p29` e Reel `p33`) | 21 e 23/10 | Short e Reel | 3 | Uma cena de 15 a 20 s: **candidatos** — cerveja de Diego (16:59) ou McDonald's Korean BBQ (05:18) ou Mural do Beijo (13:11). Atribuição de falante a confirmar | "[Cena real] em Barcelona." | 15–20 s | a definir | Enviar | Retenção |
| 10 | Shorts de reaproveitamento (`p17`, `p20`, `p23`) | 12, 14 e 16/10 | Short | 1–2 | Mesmo corte do Reel de origem | título ≤ 60 caracteres | — | — | Ver o vídeo | Viewed vs swiped |
| 11 | Short Primeiro olhar (`p26`) | 19/10 | Short | 6 | Mesmo corte do Reel de 16/10 | "Barcelona: o primeiro olhar." | 12–20 s | — | Ver o vídeo | Viewed vs swiped |

**Regra:** dois itens não usam a mesma cena de abertura. As linhas 2, 3, 4, 6 e 9 usam **cenas diferentes** do vlog.

### 3.3 O que **não** fazer com o vlog

- Não produzir vários cortes quase idênticos de Camp Nou ou de Sagrada (as duas cenas mais gravadas e mais "óbvias").
- Não inserir gravação nova de Barcelona em Reel de experiência passada (CLAUDE.md, 10).
- Não afirmar horário de pôr do sol sem constar no material.

---

## 4. Plano por vídeo: peças já previstas e o que fica a decidir

(As peças em si estão no painel; aqui está o que cada vídeo precisa de decisão.)

| Vídeo | Data | Peças previstas no painel (futuras) | Decisão de cena a registrar | Dependência |
|---|---|---|---|---|
| Barcelona | 10/10 | 21 | Seção 3.2 | Total real; erro real; licença da trilha |
| Amsterdam | 24/10 | 22 | Abertura única por peça; "frio" e "museus depois" como material de primeiro dia | Hotel, custos, vlog |
| Paris | 07/11 | 20 | **Jardim de Luxemburgo fechado** como "Não faça isso" ou "o que faltou"; Eiffel à noite como Primeiro olhar se existir | Custos, vlog |
| Disneyland Paris | 21/11 | 20 | Fila: **só** se houver registro de minutos; sem música do parque | Registro de filas e valores |
| Madrid | 05/12 | 20 | A definir após ver o vlog | Tudo |
| Bruxelas | 19/12 | 19 | Atomium como Primeiro olhar e como "vale ou pula" (não subir) | Custos |
| Bruges | 02/01 | 18 | Reação "muito, muito" e rua histórica; evitar repetir a cena usada na apresentação | Custos |
| Lisboa | 16/01 | 15 | A definir; **reserva do calendário** | Tudo |

## 5. Ordem de trabalho recomendada para o Diego e o editor

1. **Antes de 10/10:** conferir capítulos e preços de Barcelona; confirmar licença da trilha; confirmar revisão de áudio (`docs/AUDIO_REVIEW_STANDARD.md`); conferir se `€ [total]` do trailer está preenchido.
2. **Até 17/10:** mapear Amsterdam (minutagem, preços, 3 cenas de abertura distintas) usando o mesmo formato da seção 2.1. Repetir a cada vlog, uma semana antes da data de "edição pronta".
3. **Sempre:** registrar, por vlog, os valores reais em uma tabela (data, local, valor, moeda, cotação datada). É o que destrava os 56 posts com placeholder (`05`, AUD-04).
4. **Ao editar cada vlog:** marcar 3 trechos de 12 a 20 s para Primeiro olhar e 1 trecho de 15 a 25 s para "momento bruto".

## 6. Peças extras que **não** criei no painel

| Ideia | Por que ainda não |
|---|---|
| Série numerada "Primeiro Dia · Temporada 1: Europa" para os 8 vlogs | Os vlogs não são sequenciais no tempo (os brutos de Barcelona são de março, ano a confirmar; o custo da Itália tem cotação de 24/12/2024); sem decisão do Diego sobre a narrativa |
| Compilado "Os 8 primeiros dias" como vídeo longo | Depende de ter os 8 editados |
| Reel de Itália sem vídeo | CLAUDE.md, 10: Itália só tem foto e custo. Já coberto em carrosséis |
