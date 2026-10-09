# Inventário do acervo · Primeiro Dia

**Data:** 09/10/2026 · **Para que serve:** ligar cada peça do calendário v3 a material concreto e mostrar o que ainda falta localizar · **Regra:** só entra como "verificado" o que foi inspecionado neste repositório (arquivo, folha de quadros, transcrição ou foto). O que é citado em documento, mas não foi visto, está na seção 3.

Os brutos e o master **não estão no git** (`reels/apresentacao/fonte/` e `carrosseis/roma-3-dias/fonte/`, fora do repositório). O que existe aqui são as análises deles: transcrições com tempo, folhas de quadros e casamento quadro a quadro. Material bruto não pode ser alterado, movido ou renomeado (CLAUDE.md, 10).

## 1. Restrições técnicas que valem para várias peças

| Restrição | Arquivos | O que fazer |
|---|---|---|
| **Trilha de violão embutida no B-roll** do master de Barcelona; algumas cenas têm etiquetas gráficas do vlog (ex.: "Bairro Gótico" em 12:42) | Master de Barcelona | Cena sem fala sai do bruto original. Nas falas, ouvir antes: onde houver violão por baixo, procurar o bruto |
| **Cópias 720p SDR** (ampliadas a 1080 × 1920 ficam suaves) | IMG_2170, IMG_2178 (Bruxelas), IMG_2690, IMG_2691, IMG_2692 (Bruges) | Pedir os originais em resolução cheia ao Diego |
| **Selfies horizontais com os dois**: o recorte 9:16 não cabe os dois em parte dos quadros (medido na apresentação) | IMG_1375, IMG_1393 (Amsterdam), IMG_2730, IMG_3134 (Paris) | Recorte que acompanha quem fala; conferir quadro a quadro; não cortar a Marina no meio do rosto |
| **Gravados com o celular deitado e salvos como retrato** | IMG_2730, IMG_2761, IMG_3134 | Girar 90° na edição (o `render.py` da apresentação já faz) |
| **HDR (HLG) do iPhone** | Master e `.MOV` | Converter para SDR Rec.709 com o tone mapping aprovado (zscale + Reinhard, pico 4,93, saturação 0,88) |
| **Músico de rua** no áudio | IMG_0586 (Montjuïc) | Trocar o áudio por música da biblioteca |

## 2. Material verificado, por destino

### Barcelona (3 dias)

| Material | Tipo | Duração e formato | Áudio | Conteúdo útil (minutagem do master) |
|---|---|---|---|---|
| Master do vlog | Vídeo | 34:08, 4K HLG 16:9, 24 fps | Falas + trilha no B-roll | Transcrição completa em `reels/apresentacao/analise/transcricao_palavras.tsv`; 35 folhas de quadros (1 a cada 2 s) em `reels/apresentacao/contact_sheets/` |
| IMG_0502.MOV | Bruto | 4K HDR | Ambiente | Chegada ao Camp Nou, fila (master 71,15 s) |
| IMG_0520.MOV | Bruto | 4K HDR | Fala | Museu do Barça com a camisa do Bahia; **desfocado** (o foco caçou o telão) |
| IMG_0586.MOV | Bruto | 4K HDR | Músico de rua | Vista de Montjuïc (master 218,2 s) |
| IMG_0690.MOV | Bruto | 4K HDR | Violão | Praia da Barceloneta (master 453,45 s) |
| IMG_0781.MOV | Bruto | 4K HDR | Ambiente | De costas no Arco do Triunfo (master 565,8 s) |
| IMG_0816.MP4 | Bruto | — | Fala | Bar à noite, brinde, "minha primeira tapa" (master 639,4 s) |
| IMG_1192.MOV | Bruto | 4K HDR | Ambiente | Sagrada Família de baixo, dia 3 (ângulo que não está no master) |

**Preços e fatos falados no master** (valores a confirmar se foram por pessoa e em euro): museu do Barça € 31 (01:02) · passe de metrô e ônibus de 72 h € 27,50 (03:09) · McDonald's "9,70" e "13,60" (06:20; a transcrição registrou "R$") · promoção 5 tapas + paella + bebida € 19 (16:13) · Sagrada Família € 25 por pessoa, "abre as vendas um mês antes" (25:51) · Park Güell com hora marcada 13h30 (28:18; preço não dito) · 100 Montaditos € 1 cada na quarta (32:58) · "uns 18 km" no dia 1 (10:12) · Casa Batlló "acho que em torno de 15 euros" (21:39; **palpite, não usar**).

**Cenas por momento:** dia 1 (00:00–10:57): Gràcia, metrô Palau Reial, Camp Nou, Bola de Ouro, camisa do Bahia, Montjuïc, Colombo, McDonald's, Barceloneta (frio, jet ski), El Vaso de Oro, Ciutadella, Arco do Triunfo, mercado, primeira tapa · dia 2 (10:57–23:55): Gràcia, Casa Vicens, Bairro Gótico, Mural do Beijo, Catedral, Pont del Bisbe, Plaça Sant Jaume, Plaça Reial, Palau Güell, promoção de tapas, Marina provando cerveja, fontes de água e app, La Rambla em obra, Boqueria, Plaça de Catalunya, Casa Batlló, Casa Milà, pizzaria · dia 3 (23:55–34:08): Sagrada Família (9h30, interior), museu do Barça, churros, empanadas, Park Güell (sala hipóstila), Tapa Tapa, 100 Montaditos, aeroporto.

### Amsterdam (3 dias)

| Material | Tipo | Duração e formato | Áudio | Conteúdo |
|---|---|---|---|---|
| IMG_1375.MOV | Bruto | ≈ 17 s, 4K HDR, horizontal | Fala | "Chegamos em Amsterdam, acabamos de pousar… com frio… 3 dias" (aeroporto) |
| IMG_1384.MOV | Bruto | 11,3 s, 4K HDR, **vertical** | Fala | Rua de tijolos com malas: "Tá frio? Chegamos!" |
| IMG_1393.MOV | Bruto | 33,3 s, 4K HDR, horizontal | Fala | Museumplein: deixar os museus para depois, "tá muito frio", fome, "terra da Heineken e da Amstel" |

### Bruxelas (1 dia)

| Material | Tipo | Duração e formato | Áudio | Conteúdo |
|---|---|---|---|---|
| IMG_2170.MP4 | Bruto | 62 s, **720p** SDR | Fala | Atomium: chegaram de metrô, cristal de ferro ampliado 165 bilhões de vezes, Expo 1958, não subiram (longe do centro) |
| IMG_2178.MP4 | Bruto | 5,9 s, **720p** SDR | Sem fala | Atomium contra o céu azul, panorâmica lenta |

### Bruges (1 dia, bate-volta)

| Material | Tipo | Duração e formato | Áudio | Conteúdo |
|---|---|---|---|---|
| IMG_2690.MP4 | Bruto | 26,6 s, **720p** | Fala (transcrição confusa: comparação de dois chocolates, um "com álcool") | Marina com waffle em pedaços no balcão take away |
| IMG_2691.MP4 | Bruto | 11,7 s, **720p** | Sem fala útil | Marina provando |
| IMG_2692.MP4 | Bruto | 23,8 s, **720p** | Fala curta | Marina provando na rua, luvas e casaco |
| IMG_2693.MOV | Bruto | 15,5 s, 4K HDR | "Muito, muito, muito" | Diego comendo waffle na rua de compras do centro |

### Paris (1 dia)

| Material | Tipo | Duração e formato | Áudio | Conteúdo |
|---|---|---|---|---|
| IMG_2730.MOV | Bruto | ≈ 53 s, 4K HDR, girar 90° | Fala | Chegada: "um dia só em Paris… amanhã é Disney" |
| IMG_2761.MOV | Bruto | 4,5 s, 4K HDR, girar 90° | Sem fala | Selfie dos dois com a Torre Eiffel, céu azul (Champ de Mars, pelo fundo) |
| IMG_2978.MOV | Bruto | — | Sem fala usada | Torre Eiffel (usado na apresentação REV6–REV8) |
| IMG_3134.MOV | Bruto | 65,5 s, 4K HDR, girar 90° | Fala | Jardim de Luxemburgo fechado (fecha 18h30 naquele dia), dica "venham mais cedo", vão ver a Torre brilhar, "amanhã tem Disney" |

### Itália (Roma verificada; Florença, Veneza e Milão a inventariar)

| Material | Tipo | Data (EXIF) | Uso |
|---|---|---|---|
| Diego e o pai na arena do Coliseu | Foto | 26/12/2024 (sem EXIF) | Capa do carrossel de 06/10 |
| IMG_5064 | Foto | 25/12/2024 10:08 | Fontana di Trevi |
| IMG_5108 | Foto | 25/12/2024 10:50 | Panteão (fachada) |
| IMG_5132 | Foto | — | Piazza Navona (não usada no carrossel) |
| IMG_5220 | Foto | 25/12/2024 16:37 | Pôr do sol no Pincio |
| Vila de Natal da Villa Borghese (vista ampla e árvore-carrossel) | Fotos | 25/12/2024 | Slide 08; a árvore não foi usada |
| IMG_5319 | Foto | 26/12/2024 13:45 | Fórum Romano |
| IMG_6651 | Foto | 26/12/2024 08:52 | Coliseu por fora, manhã |
| IMG_6652 | Foto | — | Coliseu à noite (não usada) |
| IMG_6653 | Foto | 27/12/2024 08:25 | São Pedro |
| IMG_6650 | Foto | 27/12/2024 12:31 | Sant'Ignazio, Diego e Marina sob o teto |
| IMG_5409 | Foto | — | Interior de São Pedro (não usada) |
| IMG_5397 | Foto | — | Selfie com o grupo em São Pedro: **tem rostos de terceiros, pedir autorização** |
| IMG_5523 | Foto | 27/12/2024 16:45 | Pôr do sol no Gianicolo |

**Custos de Roma (por pessoa, dez/2024, € 1 = R$ 6,40):** total € 421,50 · hospedagem € 221,60 (4 noites, apartamento no Monti dividido por 5) · comida e bebida € 130,30 (cafés 13,10, mercado 27,30, almoços 33,70, sorvetes 13,20, jantares 43,00) · ingressos € 47,60 (Panteão 5,00, vila de Natal 17,60, Coliseu com arena 24,00, espelho de Sant'Ignazio 1,00) · passe de 72 h € 22,00. Fonte: `planejamento/ESTUDO_CARROSSEL_ROMA.md`, seção 4. Preços de 2026 conferidos em 06/10/2026: Trevi € 2 (desde 02/02/2026), Panteão € 7 (desde 01/07/2026).

**Viagem:** 24/12/2024 a 04/01/2025; Roma de 24 a 28/12 (dia 1 = 25/12).

## 3. Citado nos documentos, mas não inspecionado

| Material | Onde é citado | Situação |
|---|---|---|
| Brutos de Barcelona além dos 7 baixados (interior da Sagrada, Park Güell, ruas) | Pedido da v3; master mostra os planos | Localizar os originais sem trilha |
| Brutos dos outros dias de Amsterdam, Bruxelas, Bruges e Paris | "12 vídeos" do primeiro dia foram baixados; o resto não | Decupagem pendente |
| Brutos da Disneyland Paris, de Madrid e de Lisboa | Planejamento e vlogs do YouTube (21/11, 05/12, 16/01) | Nada inspecionado; decupagem pendente |
| Vlogs editados de Amsterdam a Lisboa | Painel (YouTube) | Em edição (só Barcelona está pronto) |
| Vídeos ambientais da Itália | Informado pelo Diego em 09/10 ("alguns vídeos dos ambientes e pontos turísticos") | Não inspecionados. **Diverge do CLAUDE.md (10), que diz "sem vídeo"**: registrar e atualizar o CLAUDE.md quando confirmado |
| Fotos e custos de Florença, Veneza e Milão | Pendência do painel desde 05/10 | Não recebidos |
| Interior do Panteão e foto no espelho de Sant'Ignazio | QA do carrossel REV1 | "Não vieram" |
| Registro de custos das 8 cidades (exceto Roma) | Painel v2 ("o Diego envia na hora de editar") | Não recebido; datas das viagens também não |
| Conteúdo exato dos posts publicados até 08/10 | Auditoria | Títulos conhecidos; valores e cenas usados não registrados no repositório |

## 4. O que cada destino sustenta (peças v3 ligadas ao material)

Status: **verificado** (material inspecionado) · **decupagem** (o material existe, falta achar os planos) · **dados do Diego** (falta custo, opinião ou data) · **futuro** (viagem de janeiro).

**Barcelona** · 11/10 R Camisa do Bahia no Camp Nou (verificado); 13/10 R Não compre água em Barcelona (verificado); 14/10 C Roteiro do primeiro dia em Barcelona: 18 km a pé (verificado); 21/10 C Barcelona: o Gaudí que dá pra ver de graça (e o que pagamos) (verificado); 24/10 R Sagrada Família: projetada como uma floresta (decupagem); 29/10 R Casa Batlló: o que você vê nessa janela? (verificado); 05/11 R € 1 cada, só às quartas: 100 Montaditos (verificado); 15/11 R Primeira tapa depois de 18 km (verificado); 22/11 R Vale ou pula: La Boqueria (verificado); 03/12 R Park Güell (sem texto) (decupagem); 12/12 R McDonald's da Espanha × do Brasil (verificado); 19/12 R Metrô ilimitado em Barcelona: € 27,50 por 3 dias (verificado); 26/12 R Vista de Barcelona do alto do Montjuïc (decupagem); 05/01 R Sagrada Família: o ingresso que precisa de antecedência (verificado); 09/01 R Vale a pena ir a Barcelona? A resposta no aeroporto (verificado); 17/01 R Por que ficamos em Gràcia (e não no centro) (verificado)

**Itália** · 17/10 R Dois pores do sol de graça em Roma (decupagem); 22/10 R Roma agora cobra pra ver isso (verificado); 04/11 C Roma de graça (ou quase): o que vimos sem pagar (verificado); 10/11 R € 1 pra ver esse teto em Roma (verificado); 21/11 R Veneza: sem carro, sem moto, só barco (decupagem); 25/11 C Florença em 2 dias: € [total] (dados do Diego); 01/12 R Comida em Roma: a regra que segurou o orçamento (verificado); 08/12 R Roma iluminada no Natal (verificado); 09/12 C Veneza em 2 dias: € [total] (dados do Diego); 16/12 C Natal em Roma: o que fizemos no dia 25 (verificado); 22/12 R 52% do custo de Roma foi isso (verificado); 24/12 R Nosso primeiro dia em Roma foi no Natal (verificado); 30/12 C Milão em 2 dias: € [total] (dados do Diego); 31/12 R Réveillon na Itália: como foi (dados do Diego); 13/01 C Itália em 9 dias: € [total] (dados do Diego)

**Paris** · 15/10 R Paris: chegamos e o jardim estava fechado (verificado); 28/10 C Paris em 1 dia: o que deu e o que faltou (decupagem); 07/11 R A Torre Eiffel pisca de hora em hora (decupagem); 26/11 R Primeiro dia em Paris (e era o único) (verificado); 13/12 R Paris de dia, sem informação (decupagem); 19/01 R Onde ver a Torre Eiffel de graça (verificado)

**Disneyland Paris** · 31/10 R 2 parques da Disneyland Paris em 1 dia (decupagem); 14/11 R Disneyland Paris: o castelo ao vivo (decupagem); 18/11 C 2 parques da Disney em 1 dia: como dividimos o dia (dados do Diego); 05/12 R Vale ou pula: Disneyland Paris em 1 dia? (dados do Diego); 23/12 C Disneyland Paris em 1 dia: € [total] (dados do Diego); 02/01 R Paris + Disney em 2 dias: dá? (dados do Diego); 28/01 R Disney: o momento em que valeu (decupagem)

**Amsterdam** · 20/10 R Primeira hora em Amsterdam: frio e fome (verificado); 27/10 R Amsterdam: imagina morar nessa rua (decupagem); 19/11 R Amsterdam em 3 dias: € [total] (dados do Diego); 20/12 R Expectativa × realidade: Amsterdam (dados do Diego); 14/01 R Amsterdam de bicicleta e canal (decupagem); 20/01 C Amsterdam em 3 dias: o roteiro que fizemos (decupagem)

**Madrid** · 08/11 R Primeiro dia em Madrid (decupagem); 28/11 R Madrid em planos (sem informação) (decupagem); 10/12 R Madrid em 2 dias: o que deu pra fazer (decupagem); 27/12 R Madrid: o momento que eu não esperava (decupagem); 12/01 R Madrid de graça: o que vimos sem pagar (decupagem); 27/01 C Madrid em 2 dias: € [total] (dados do Diego)

**Lisboa** · 01/11 R Lisboa à noite (sem texto) (decupagem); 17/11 R Vale ou pula: a primeira comida em Lisboa (decupagem); 02/12 C Lisboa em 1 noite e 1 manhã: o que coube (decupagem); 16/01 R Primeira noite em Lisboa (decupagem); 21/01 R Lisboa de manhã, com 1 informação (decupagem)

**Bruges** · 18/10 R Vale ou pula: waffle de rua em Bruges (verificado); 25/10 R Bruges em 15 segundos (sem texto) (decupagem); 11/11 C Bate-volta de Bruxelas a Bruges: como fizemos (dados do Diego); 24/01 R Bruges vista do canal (decupagem)

**Bruxelas** · 10/10 R Atomium: o cristal de ferro gigante de Bruxelas (verificado); 29/11 R Bruxelas em 1 dia: vale parar? (decupagem); 17/12 R Bruxelas em planos (decupagem)

**Vários destinos** · 03/11 R 8 cidades, 8 primeiros dias (decupagem); 12/11 R Barcelona ou Madrid: qual escolher? (dados do Diego); 24/11 R A passagem é só o começo (antes da Black Friday) (verificado); 06/12 R Canais: Amsterdam ou Bruges? (decupagem); 15/12 R Qual primeiro dia foi o melhor? (dados do Diego); 29/12 R Ninguém avisou desse frio (verificado); 03/01 R Comida de rua na Europa: nossa nota sincera (dados do Diego); 06/01 C Quanto custou cada cidade (por dia, por pessoa) (dados do Diego); 07/01 R 2 erros que a gente não repete (verificado); 10/01 R Próximo primeiro dia: [cidade 1] (dados do Diego); 31/01 R Qual dessas você visitaria primeiro? (sem texto) (decupagem); 04/02 R Qual cidade foi a mais barata? (dados do Diego)

**Viagem de janeiro** · 23/01 R Primeiro dia em [cidade 1], ao vivo (futuro); 26/01 R Primeira hora em [cidade 2]: € [valor real] (futuro); 30/01 R Primeiro dia em [cidade 2 ou 3], ao vivo (futuro); 02/02 R Vale ou pula: [atração da viagem], ao vivo (futuro); 03/02 C [Cidade 1]: o primeiro dia em números (futuro); 06/02 R Primeiro dia em [cidade 3], ao vivo (futuro); 07/02 R 3 países, [N] primeiros dias: o balanço (futuro)

## 5. Como manter este inventário

1. Ao decupar um bruto, registrar no campo **Notas** da peça no painel (arquivo e minutagem) e, se o material servir para mais de uma peça, acrescentar uma linha na seção 2.
2. Quando um custo chegar, atualizar a peça (tirar os colchetes) e a seção 2.
3. Uma peça só passa de "decupagem" ou "dados do Diego" para "verificado" quando o material foi visto e o dado confirmado.
4. Gravação nova é "material futuro" e não é requisito para editar o acervo (CLAUDE.md, 10).
