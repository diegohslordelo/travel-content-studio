# QA · Reel "A Disney de Paris não quer você lá" (5 dicas) · REV1

**Entrega:** `reel_disney-5-dicas_rev1.mp4` (78,53 s, 1080 × 1920, 30 qps, H.264 CRF 10, AAC 320 kb/s) · prévia leve `reel_disney-5-dicas_rev1_previa.mp4` (720p, 17 MB) · capa `capa_disney-5-dicas_rev1.jpg` · legendas do post em `legenda_post.md` · créditos em `creditos.md`.
**Pedido do Diego (10/11/2026):** montar o Reel com a gravação da pasta do Drive `Disney/Reel`, na sequência dele (gancho → "pelo menos" na sentada → 11 milhões → parques lotados → 5 pulos do gato → dica 1 → dica 2 → tirar print → 3 → 4 → dica de ouro → perrengue → parte 2 e seguir). Pediu ainda:
- voz decupada com ritmo;
- tela dividida;
- gancho com fita zebrada e o castelo, como nos Reels de Bruges e de Paris;
- você sozinho em tela cheia no "pelo menos", com o corte no meio da sentada;
- print de comprovação dos 11 milhões e o print do app;
- imagens que mostrem exatamente o que é dito;
- o pôr do sol do Big Thunder em tela dividida ou cheia, o que for melhor;
- nada de acelerar ou desacelerar vídeo;
- CTA no DS;
- **sem nenhum take em formato vlog ou selfie com o Diego falando**, com exceção do vídeo do Big Thunder.

**Veredito do Claude:** pronto para a sua escuta. Há 3 pontos para você decidir antes de postar (seção 7).

---

## 1. A fala: sequência pedida × gravação

A gravação (`7BE64B25.mp4`, 125 s) é uma montagem sua de vários takes. Os 13 trechos entram na ordem pedida, cortados só no silêncio e **sem acelerar**. Nenhum trecho cruza um corte de take: os cortes foram detectados por mudança de cena (> 0,3) em 5,2 · 9,07 · 22,0 · 33,93 · 43,7 · 57,7 · 70,4 · 79,1 · 86,73 · 95,23 · 103,67 s.

| # | Sequência do Diego | Trecho da gravação | Fala (como foi dita) |
|---|---|---|---|
| f1 | A Disney de Paris não quer você lá | 0,30–2,70 | A Disney de Paris não quer você lá. |
| f2 | Pelo menos… (sentando) | 5,57–8,67 | Pelo menos não se você for igual a todo mundo. |
| f3 | 11 milhões | 11,83–18,70 | A Disney de Paris recebe quase 11 milhões de visitas no ano e muitas dessas pessoas ainda visitam parques sem estratégia. |
| f4 | Aí você já imagina… | 22,40–33,80 | E aí você já imagina, né? Mar de gente nos parques, pessoas rodando pro lado e pro outro, tentando fugir de fila, chegam nos restaurantes cheios e olha que já não são baratos e aí tentam tirar o atraso comprando caro um fast pass. |
| f5 | Mas calma, 5 pulos do gato | 36,40–41,03 | Mas calma aí que eu vou te ajudar. Eu vou te dar 5 pulos do gato com base na minha experiência no parque. |
| f6 | 1. dica 1 | 44,30–55,47 | Primeiro, vá dia de semana. Você vai comprar ingresso park hopper… menos gente e você vai conseguir aproveitar tudo. |
| f7 | 2. dica 2 | 60,70–68,20 | Dois, baixe o aplicativo da Disney de lá… pedir a comida antes no restaurante. |
| f8 | 3. tira o print | 98,43–101,20 | Aproveita para tirar print aí porque ele foi nosso melhor amigo lá. |
| f9 | 4. (dica) 3 | 103,67–110,90 | Em terceiro, a comida lá dentro é cara mesmo… não gastar muito dinheiro com isso. |
| f10 | 5. (dica) 4 | 116,77–122,13 | Em quarto, deixa a montanha-russa Big Thunder pro final de tarde. Se ligue no visual sinistro que a gente pegou no pôr do sol. |
| f11 | 6. dica de ouro | 70,40–78,03 | E por último, a dica de ouro. Sai um pouco antes do show de fogos acabar… a circulação dos trens. |
| f12 | 7. perrengue | 81,27–84,70 | Eu te garanto que você não vai querer passar perrengue depois de um dia cansativo. |
| f13 | 8. parte 2 e segue o perfil | 88,73–92,77 | Se você quer parte 2, já me segue aí que toda semana tem dicas de viagem no perfil. |

**Ficou de fora** (não estava na sequência):
- "Se você gostou desse vídeo, já comenta aqui": era um 2º pedido, e o post tem CTA único.
- "Um beijo e até o próximo vídeo": transcrito com confiança baixa, provavelmente sem fala real.

**Ritmo:** voz de 77,53 s. As junções entre trechos têm 0,07–0,15 s de respiro, e o vídeo fecha com 1 s de cauda no CTA. As pausas internas eram curtas (a maior, 0,36 s), então não precisaram de corte dentro da frase (FORMATOS_REELS 7.3).

**Leitura automática conferida:** Whisper large-v3 na gravação e de novo no vídeo final, mais o alinhamento forçado MMS para o tempo de cada palavra. Nos trechos em dúvida, as alternativas foram comparadas pela verossimilhança acústica (CTC) na própria gravação:

| Trecho | Escrito na legenda | Por quê |
|---|---|---|
| "ingresso park hopper" | park hopper | O Whisper ouve "parque roupa", que é a pronúncia de "park hopper"; você confirmou a palavra |
| "consegue comprar em tempo real a fila" | comprar | "Comprar" ganhou de "acompanhar" nas duas leituras. É o que foi dito (ver seção 7) |
| "pro lado e pro outro", "vai tá", "já tá perto", "sai um pouco" | como falado | As duas leituras preferem a forma falada à formal |
| "a montanha-russa Big Thunder pro final de tarde" | sem "Mountain" | O primeiro Whisper escreveu "Manda aí para"; o alinhamento confirma "Big Thunder pro" |
| "nem é lá essas coisas" | nem é lá | Empate técnico com "nem lá" |

## 2. Decupagem visual (cena por cena)

Todo plano de acervo e todo trecho seu em tela cheia fica **2 s ou mais** na tela (decisão do Diego). Animações e prints ficam entre 1,1 e 4,9 s. Cada troca de imagem cai numa palavra, de 0,05 a 0,2 s antes dela.

| # | Tempo | Fala | Imagem (ilustra o quê) | Fonte | Composição | Entrada · som |
|---|---|---|---|---|---|---|
| 1 | 0,00–2,40 | A Disney de Paris não quer você lá. | Castelo da Bela Adormecida de dia. As fitas zebradas atravessam em "não" e "lá". Texto do gancho linha a linha: A DISNEY / DE PARIS / NÃO QUER / VOCÊ LÁ. (vermelho) | Acervo IMG_3356 + fita desenhada | Tela dividida, você desde o 1º quadro | — |
| 2 | 2,40–5,50 | Pelo menos não se você for igual a todo mundo. | **Corte no meio da sentada**: você entra na cadeira em movimento. Palavra-chave PELO MENOS… / NÃO SE VOCÊ FOR / *igual a todo mundo* | Gravação | Você em tela cheia | Corte seco · swish na sentada |
| 3 | 5,50–9,07 | A Disney de Paris recebe quase 11 milhões de visitas no ano | **Print** da AirMagique (índice TEA 2025) cai, quica e assenta. Marca-texto em "Disneyland Park drew 10.8 million visits" e na célula 10,8 milhões. Ao lado: QUASE / 11 / MILHÕES / DE VISITAS / NO ANO | Print real | Animação na tela dividida | Queda · impacto no pouso e em "11" |
| 4 | 9,07–12,37 | e muitas dessas pessoas ainda visitam parques sem estratégia. | Main Street cheia, castelo ao fundo; SEM / ESTRATÉGIA | Acervo IMG_3337 | Tela dividida | Zoom |
| 5 | 12,37–14,87 | E aí você já imagina, né? Mar de gente nos parques, | Multidão diante do castelo; MAR DE / GENTE | Acervo IMG_3453 | Tela dividida | Corte seco |
| 6 | 14,87–18,87 | pessoas rodando pro lado e pro outro, tentando fugir de fila, chegam nos restaurantes cheios | 3 cartões, cada um cai na sua palavra: gente andando no Studios · aglomeração na Frontierland · restaurante lotado (desenho) | Acervo IMG_3228 e IMG_3522 (quadros) + desenho | Animação (sem legenda: os rótulos são a fala) | Corte seco · página nos 2 primeiros cartões |
| 7 | 18,87–23,77 | e olha que já não são baratos e aí tentam tirar o atraso comprando caro um fast pass. | A carteira se esvazia (JÁ NÃO SÃO / BARATOS). Em "comprando", entra o passe de fila; carimbo CARO na palavra; FAST PASS na palavra | Desenho | Animação | Impacto no carimbo |
| 8 | 23,77–25,80 | Mas calma aí que eu vou te ajudar. Eu vou te dar 5 | Você em tela cheia, aproximação lenta | Gravação | Você em tela cheia | **Clarão** |
| 9 | 25,80–28,40 | pulos do gato com base na minha experiência no parque. | O castelo se desenha em traço; um gato âmbar dá 5 pulos pelas torres (1 a 5); 5 PULOS / DO GATO | Desenho | Animação | Swish no 1º pulo |
| 10 | 28,40–30,73 | Primeiro, vá dia de semana. Você vai comprar ingresso | Selo 1. Sete colunas de calendário: as 5 do meio da semana acendem e o fim de semana fica apagado; DIA DE / SEMANA | Desenho | Animação | — |
| 11 | 30,73–33,90 | park hopper que te dá acesso aos dois parques em um único dia, | Ingresso PARK HOPPER; os dois castelinhos acendem em "dois"; 2 PARQUES / 1 DIA na palavra | Desenho | Animação | Swish |
| 12 | 33,90–36,13 | vai pagar mais barato e ainda vai ter menos gente. | Walt Disney Studios às 10h, pouca gente; MAIS BARATO / MENOS GENTE | Acervo IMG_3219 | Tela dividida | Corte seco |
| 13 | 36,13–38,17 | Cheio sempre vai tá, mas vai ter menos gente e | Rua coberta do Studios lotada; CHEIO / SEMPRE VAI TÁ | Acervo IMG_3214 | Tela dividida | Corte seco |
| 14 | 38,17–39,57 | você vai conseguir aproveitar tudo. | Três atrações (castelo, montanha-russa, fogos) ganham o visto; APROVEITAR TUDO | Desenho | Animação | — |
| 15 | 39,57–43,73 | Dois, baixe o aplicativo da Disney de lá. Você consegue comprar em tempo real a fila dos brinquedos. | Selo 2. O celular com o **seu print da App Store** cai em "aplicativo"; em "fila" a tela rola até a prévia da fila rápida (Premier Access), marcada em âmbar | Print do Diego | Animação | Impacto no pouso |
| 16 | 43,73–47,07 | Ele ajuda no roteiro e ainda dá para pedir a comida antes no restaurante. | Mapa em traço com 4 pinos e a rota que se desenha (ROTEIRO); em "pedir", o pedido no celular com o visto (PEDIR A / COMIDA / ANTES) | Desenho | Animação | — |
| 17 | 47,07–49,83 | Aproveita para tirar print aí porque ele foi nosso melhor amigo lá. | O celular volta e **pisca como captura de tela** em "print"; TIRAR PRINT → NOSSO MELHOR / AMIGO | Print do Diego | Animação | Obturador |
| 18 | 49,83–53,33 | Em terceiro, a comida lá dentro é cara mesmo. E olha que nem é lá essas coisas. | Selo 3. Bandeja com hambúrguer, batata e refrigerante; CARA / MESMO e, em "nem", o lanche murcha (NEM É LÁ / ESSAS / COISAS) | Desenho | Animação | — |
| 19 | 53,33–57,07 | Então, leva um lanche na mochila para você tapear a barriga e não gastar muito dinheiro com isso. | Mochila; a barra de cereal cai dentro dela em "lanche"; LANCHE / NA MOCHILA; NÃO GASTAR MUITO | Desenho | Animação | Swish |
| 20 | 57,07–59,73 | Em quarto, deixa a montanha-russa Big Thunder pro final de tarde. | Selo 4. A montanha-russa no fim da tarde: frente do carrinho e o horizonte dourado | IMG_4525 (63,0 s) | Tela dividida | Corte seco |
| 21 | 59,73–62,43 | Se ligue no visual sinistro que a gente pegou no pôr do sol. | **O pôr do sol do Big Thunder em tela cheia**: a rocha mais alta preenche a tela (ver nota abaixo) | IMG_4525 (57,4 s) | Tela cheia | **Luz de passagem** · ar longo |
| 22 | 62,43–63,57 | E por último, a dica de ouro. | Medalha de ouro; DICA DE / OURO | Desenho | Animação | Impacto em "dica" |
| 23 | 63,57–65,93 | Sai um pouco antes do show de fogos acabar. Eu sei que é difícil, | Fogos sobre o castelo, o público na frente; SAI UM POUCO / ANTES | Acervo IMG_3595 | Tela cheia | Corte seco |
| 24 | 65,93–67,93 | mas todo mundo sai junto, fica muito cheio | O público dos fogos (a multidão que sai junto); TODO MUNDO / SAI JUNTO | Acervo IMG_3595 (17 s) | Tela dividida | Corte seco |
| 25 | 67,93–70,07 | e já tá perto do horário de acabar a circulação dos trens. | Painel do RER A "Marne-la-Vallée – Chessy" (o relógio 09:42 fica fora do recorte); CIRCULAÇÃO / DOS TRENS | Acervo IMG_3205 | Tela dividida | Corte seco |
| 26 | 70,07–73,50 | Eu te garanto que você não vai querer passar perrengue depois de um dia cansativo. | Você em tela cheia; NÃO VAI QUERER / *passar perrengue* | Gravação | Você em tela cheia | **Clarão** · impacto |
| 27 | 73,50–78,53 | Se você quer parte 2, já me segue aí que toda semana tem dicas de viagem no perfil. | Fogos sobre o castelo; PARTE 2 em "parte"; **placa do DS V2** JÁ ME SEGUE AÍ / PRIMEIRO DIA → em "segue" (Chegada + *clack*) | Acervo IMG_3607 + DS V2 | Tela cheia + CTA | **Luz de passagem** · *clack* |

**Pôr do sol do Big Thunder (pedido do Diego, tela dividida ou cheia):** foi em **tela cheia**. A rocha mais alta é vertical e ocupa a tela inteira, que é o "visual sinistro" da fala. Na tela dividida ela viraria uma faixa estreita. O vídeo original é 1080p na horizontal, então o recorte vertical é ampliado 1,8×: o quadro conferido em tamanho real está nítido. O plano anterior (frente do carrinho e horizonte dourado) fica na tela dividida, para mostrar o pôr do sol de fato.

**Takes de vlog (pedido do Diego):**
- **Nenhum** plano do acervo com você ou a Marina falando para a câmera entrou.
- A única exceção é o vídeo do Big Thunder, e dele entraram só os dois trechos do cenário, sem vocês.
- Ficaram de fora: IMG_3608 (vocês saindo mais cedo à noite), 3210, 3327, 3451, 3452, 3355, 3358, 3201, 3220, 3227, 3266, 3269 e F2660F17.
- Comida, restaurante, fila e fast pass não existiam no acervo sem ser em vlog. O Commons (fotos com licença livre) recusou as buscas desta sessão por limite de acesso (erro 429). Essas cenas viraram **desenho do formato**, que não se passa por foto.

**Planos sem esticar:** nenhum plano teve a velocidade mudada. Todos foram cortados dentro do trecho limpo de cada arquivo (o `preparar.py` recusa a montagem se o plano for curto).

**Rotação:** muitos vídeos da Disney (inclusive o do Big Thunder) têm a etiqueta de rotação do iPhone trocada. Cada plano foi conferido na folha de contato e recebeu a orientação certa (`rot` no `cenas.json`).

**Equilíbrio:**
- **Contagem:** 27 cenas, com média de 2,9 s.
- **Por composição:** tela dividida com acervo 8, animação 12, tela cheia de acervo 4, você em tela cheia 3.
- **Animações:** são muitas por falta de acervo sem vlog. Ficam sobre o parque desfocado (castelo, Studios ou castelo à noite), para não parecerem chapadas.

**Transições (7, sempre ≥ 1,5 s entre elas):**

| Transição | Onde | Por que nasceu do Reel |
|---|---|---|
| Corte seco no meio da sentada | Gancho → "pelo menos" | O seu movimento é a transição |
| Queda do print | Cena 3 | — |
| Zoom | Print → Main Street | — |
| Clarão | "Mas calma aí" e "Eu te garanto" | — |
| Captura de tela | "Tirar print" | O celular pisca como print |
| Luz de passagem | Pôr do sol e CTA | É a luz do próprio pôr do sol e dos fogos |

As outras trocas são corte seco.

**Imagem que não engana (CLAUDE.md 9):**
- A fita zebrada é desenho chapado sobre a imagem real.
- Carteira, ingresso, gato, calendário, mapa, bandeja e mochila são traço e cor chapada.
- Os dois prints são páginas reais. Só foram recortados; no da AirMagique, a foto de abertura e o player de podcast foram ocultados, sem mudar texto.
- O painel do RER é da manhã (09:42). O recorte deixa o relógio de fora, porque a fala trata do fim da noite.

## 3. Voz

| Medida | Valor |
|---|---|
| Fonte | Uma gravação (iPhone, HLG → SDR no vídeo) |
| Ruído de fundo da gravação | 57,7 dB abaixo da fala: sala silenciosa. Redução de ruído leve (40%), uma vez no arquivo inteiro, com o perfil do trecho mais quieto |
| Tratamento | Passa-alta de 70 Hz · cada frase no mesmo loudness (39 frases; ganho limitado a ±6 dB, com rampas nas pausas) · compressor 2:1 · master |
| Frases antes → depois | −27,6 a −12,4 LUFS (desvio de 3,1 LU) → −17,2 a −14,5 LUFS (desvio de 0,45 LU) |
| Emendas | 12 junções no silêncio (−47 a −69 dB antes do corte). Duas encostam na fala por causa da sua montagem: f11 (o take já começa no "E") e f13 (nos primeiros 17 ms, silenciados, sobrava o fim do "aqui" da frase cortada) |

## 4. Identidade visual

- **Do gancho até antes do CTA:** linguagem do formato tela dividida, a mesma do Reel de Paris: Anton, Inter 800, âmbar `#E0AE5C`, grão 6%, fundo `#14120F` e serifa itálica na palavra-chave. Nenhum componente, cor ou som `PD_*` do DS.
- **Acréscimos deste Reel** (não viram regra do formato): vermelho `#D63A2F` na fita, em "VOCÊ LÁ.", no carimbo CARO e nos desenhos (refrigerante, batata, fita da medalha).
- **CTA:** placa do DS V2 (rótulo "JÁ ME SEGUE AÍ" + destino "PRIMEIRO DIA" + módulo de seta), posição fixa x 72 · y 640, Chegada e *clack* a −6 dB da voz (volume de trabalho da REFERENCIA_EDICAO_FORMATOS 4.1). O rótulo vem da fala, como no Reel de Paris ("ACOMPANHA AQUI / PRIMEIRO DIA"). "PRIMEIRO DIA" tem 11 letras, então fica no tamanho padrão.
- **Composição:** `design-system/remotion/src/disney/` (`Disney.tsx` e `Graficos.tsx`), id `Disney` no `Root.tsx`. Usa a fita, o selo de número e o estilo de `src/paris/`. A composição de Paris veio do branch do Reel de Paris, que ainda não está na `main`.

## 5. Medições

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 78,53 s (voz de 77,53 s + 1 s de cauda) |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 CRF 10 (≈ 54 Mb/s), AAC 320 kb/s 48 kHz |
| 3 | Tempo na tela | Acervo e rosto ≥ 2,0 s em todas as cenas (a mais curta tem 2,0 s); animações ≥ 1,13 s |
| 4 | Planos do acervo | Trechos dentro da duração limpa; nenhum esticado; nenhum take de vlog (exceto o do Big Thunder, só cenário) |
| 5 | Legendas | 1 linha, ≤ 4 palavras; maior largura de 792 px pela métrica da fonte (limite de 800); centradas em x 540 |
| 6 | Imagem na palavra | Todas as trocas ancoradas em palavra (`cenas.json`) |
| 9 | Áudio | **−14,0 LUFS** integrados, LRA de 1,8 LU, pico verdadeiro de **−1,5 dBTP**, 0 amostra acima de −1 dBFS, 0 em 0 dBFS |
| 11 | Transcrição da voz final | O Whisper large-v3 no vídeo final repete a fala gravada, nas 13 partes e na ordem. Palavras com confiança < 0,6: "o" (11,1 s), "pro" (15,5 s), "que" (31,4 s), "tá" (36,9 s), "porque" (48,3 s), "e" e "não" (51,6–52,3 s), "deixa" (57,7 s). Nenhuma palavra cortada |
| 12 | Nada na tela fora da fala | Textos na tela: A DISNEY DE PARIS NÃO QUER VOCÊ LÁ · PELO MENOS… NÃO SE VOCÊ FOR igual a todo mundo · QUASE 11 MILHÕES DE VISITAS NO ANO · SEM ESTRATÉGIA · MAR DE GENTE · PESSOAS RODANDO · FUGIR DE FILA · RESTAURANTES CHEIOS · JÁ NÃO SÃO BARATOS · FAST PASS · CARO · 5 PULOS DO GATO · DIA DE SEMANA · PARK HOPPER · 2 PARQUES · 1 DIA · MAIS BARATO · MENOS GENTE · CHEIO SEMPRE VAI TÁ · APROVEITAR TUDO · APLICATIVO DA DISNEY · A FILA EM TEMPO REAL · ROTEIRO · PEDIR A COMIDA ANTES · TIRAR PRINT · NOSSO MELHOR AMIGO · CARA MESMO · NEM É LÁ ESSAS COISAS · LANCHE NA MOCHILA · NÃO GASTAR MUITO · DICA DE OURO · SAI UM POUCO ANTES · TODO MUNDO SAI JUNTO · CIRCULAÇÃO DOS TRENS · NÃO VAI QUERER passar perrengue · PARTE 2 · JÁ ME SEGUE AÍ / PRIMEIRO DIA. Todos ditos. Os números 1 a 4 nos selos correspondem a "Primeiro", "Dois", "Em terceiro" e "Em quarto" |
| 13 | Créditos | `creditos.md` |

Folha de quadros: `qa_frames/folha_1s.jpg` (1 quadro por segundo).

## 6. Arquivos

| Arquivo | O quê |
|---|---|
| `edicao.json` | Trechos (in/out) e texto conferido de cada fala |
| `transcricao_alinhada.json` | Tempo de cada palavra (alinhamento forçado) |
| `cenas.json` | Cenas ancoradas em palavras, planos (com rotação), gancho, palavras-chave, legendas, sons e CTA |
| `voz_medicao.json` | Medição da voz (gravação e frases) |
| `scripts/` | `alinhar.py`, `preparar.py`, `render.sh` (rodam de dentro de `rev1/`) |
| `imagens/` | Prints (AirMagique, App Store) e quadros do acervo (fundos desfocados e fotos dos cartões) |

Brutos em `../fonte/` (fora do git): `fonte/quarto/` (gravação, IMG_4525 do Big Thunder e o print do app) e `fonte/acervo/` (planos da Disney).

## 7. Decisões do Diego antes de postar

1. **"Você consegue comprar em tempo real a fila dos brinquedos" (dica 2).** As duas leituras ouvem "comprar", e a legenda segue a fala. A imagem mostra a prévia da fila rápida (Premier Access), que de fato se compra no app. Mas, se você quis dizer "acompanhar", a frase dá a ideia errada (e no começo do vídeo o fast pass é tratado como caro). Se for o caso, regrave só essa frase.
2. **"A Disney de Paris recebe quase 11 milhões de visitas."** Os 10,8 milhões são do Disneyland Park, o parque do castelo. Somando os dois parques, a TEA conta ≈ 16,7 milhões. O número dito fica **abaixo** do total, não exagera, e a legenda do post deixa claro que é o parque principal. O print mostra a linha do Disneyland Park.
3. **Duração de 78,5 s.** A referência de conteúdo recomenda até 30 s (e < 3 min de máximo). Com 5 dicas inteiras não dá para chegar perto disso sem cortar dica. Se a retenção cair antes da metade, a próxima versão pode virar duas partes, como a própria fala sugere ("parte 2").

## 8. Conferir no ouvido (o Claude não escuta)

- **Início do CTA (73,5 s):** os primeiros 17 ms foram silenciados para tirar o fim do "aqui". Confira se não sobra um "e" antes do "Se". Se sobrar, a legenda pode ganhar o "E".
- **"E por último" (62,4 s):** na sua montagem, o take já começa colado no "E". Confira se a primeira sílaba está inteira.
- **"pro lado e pro outro", "vai tá", "já tá perto" e "sai um pouco":** a legenda segue a forma falada. Confira se bate com o que você ouve.
- **Volume dos efeitos `PDX_*` e do *clack*:** nenhum foi ouvido por humano.
