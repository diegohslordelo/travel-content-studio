# QA · Reel GTA 6 × Miami · REV1 (12/11/2026)

**Entrega:** `rev1/reel_gta6_miami_rev1.mp4` (1080 × 1920, 30 qps, 57,6 s, H.264 + AAC 48 kHz). Também:
- prévia leve `rev1/reel_gta6_miami_rev1_previa.mp4` (720p);
- capa `rev1/capa_reel_gta6_miami_rev1.jpg`, o quadro de 2,7 s com o gancho completo;
- legenda do post `rev1/legenda_post.md`;
- créditos `rev1/creditos.md`.

**Formato:** tela dividida (`docs/FORMATOS_REELS.md`), estrutura AIDA (roteiro da Opção B aprovado na conversa de 11/11/2026, com as mudanças que o Diego fez na gravação: sem a dica do Metromover, frases próprias).

**Fonte da fala:** `fonte/diego_E194BAEE.mp4` (pasta do Drive "GTA 12/11", 90,7 s, HLG/BT.2020 10 bits). Os vídeos de apoio são as 3 gravações de tela da mesma pasta. As fotos das lanchonetes foram baixadas do X; ver `creditos.md`.

## 1. Pedidos do Diego (12/11/2026) e como foram atendidos

| Pedido | Como ficou |
|---|---|
| Tela dividida; em cima, ilustrar o que é dito, de preferência com coisa real de Miami | 14 das 22 cenas são vídeo ou foto real de Miami: letreiro e drone do Kaseya Center, Ocean Drive, carros, cadeiras, dirigível, avião com faixa, salva-vidas, ônibus, Burger Shot e Cluckin' Bell. As partes sem imagem real (valor, votação, proposta do condado, xerife, carta da Justiça, "preço de banana") viraram animação |
| Gancho com imagem impactante | Letreiro "Welcome to Vice City" e a fachada roxa com o VI, à noite. A câmera sobe da fachada até o letreiro enquanto o texto do gancho entra |
| Lanchonetes: pegar de qualquer lugar | Fotos reais do balcão do Burger Shot (Joel Franco, X, 21/10) e do Cluckin' Bell (Lucía Caminos, X, 22/10), lado a lado |
| Decupagem sem espaço entre as falas, sem cortar palavra | 12 trechos colados sem nenhum quadro de silêncio entre eles (seção 3). Conferido com nova transcrição da voz cortada: todas as palavras presentes |
| Sem edição de cor no vídeo do Diego | Só a conversão técnica de HDR para SDR (seção 4). Grão, luz e flash ficam só na metade de cima ou nos quadros do 975 MIL |
| Listras, animações e destaque da legenda nas cores do jogo | Pôr do sol do GTA VI (amarelo → laranja → rosa → roxo), néon rosa e ciano. Costura em 3 listras, destaque da legenda em rosa néon. Valores em `design-system/remotion/src/gta/estilo.ts` |
| Efeito de martelo ou batida em cada entonação do "975 mil" para a câmera | 5 batidas (`PDX_impacto`, −4 dB da voz) com chacoalho, soco de zoom e flash rosa, nas sílabas fortes: NO (15,64 s), CEN (16,10), TEN (17,18), CIN (17,55), MIL (17,76). Na 1ª menção ("pagou 975 mil dólares") há uma batida só, no "DÓLARES" |

## 2. Decisão editorial que o Diego precisa conferir

**Saiu "incluindo de tribunais"** (fim da tomada T06, 49,75–51,08 s da gravação). Nenhuma fonte diz que o condado quis pôr a marca em tribunais. A carta da Justiça (NBC 6) pediu que os tribunais ficassem expressamente fora, de forma preventiva, e a fala seguinte já conta isso ("jogo de crime dentro do fórum, não").
- O corte cai no fim do "s" de "públicos", medido pela energia acima de 4 kHz em 49,67–49,75 s.
- Para voltar o trecho: em `edicao.json`, tire o item de `cortes` e rode `scripts/decupar.py --render`, `montar.py`, `mixar.py` e o render.

## 3. Decupagem (`edicao.json` → `decupagem.json`, `scripts/decupar.py`)

Bordas medidas pela energia da voz (banda 120–4.000 Hz, quadros de 10 ms):
- **Entrada:** 1º quadro acima de −60 dB, arredondada para baixo no quadro de vídeo.
- **Saída:** 30 ms abaixo de −62 dB, arredondada para cima.

Nada da palavra é cortado; sobra no máximo 33 ms. Fades de 6 ms (entrada) e 12 ms (saída) dentro dessa sobra. Duas pausas de silêncio digital dentro de tomadas (T07 depois de "crime", T08 depois de "Vice City") também saíram.

| Tomada | Gravação (s) | Reel (s) | Fala |
|---|---|---|---|
| T01 | 2,133–4,933 | 0,00–2,80 | esse … videogames |
| T02 | 9,233–15,833 | 2,80–9,40 | Vice City … meio |
| T03 | 19,900–26,100 | 9,40–15,60 | a Rockstar … Heat |
| T04 | 30,267–33,033 | 15,60–18,37 | 975 mil (para a câmera) |
| T05 | 36,800–42,633 | 18,37–24,20 | beleza … votar |
| T06 | 44,800–49,767 | 24,20–29,17 | e o condado … públicos |
| T07 | 53,433–57,233 | 29,17–32,97 | e aí veio … crime |
| T07 | 57,500–62,267 | 32,97–37,73 | e a própria Justiça … não |
| T08 | 64,367–70,100 | 37,73–43,47 | mas a cidade … Vice City |
| T08 | 70,133–72,600 | 43,47–45,93 | e até placas … cidade |
| T09 | 75,233–83,200 | 45,93–53,90 | mas quem ganha … cidade |
| T10 | 85,633–88,367 | 53,90–56,63 | manda … isso |

**Fim da T04:** depois de "mil" há um som em 33,2–33,45 s que o Whisper não reconhece como palavra. Ficou de fora: o corte é em 33,03 s, quando a voz já caiu a −55 dB.

**Tempos das palavras:**
- Whisper large-v3 dá o texto.
- O alinhamento forçado (wav2vec2 PT) dá o tempo de cada palavra (`transcricao_alinhada.json`).
- A conferência foi uma nova transcrição da voz já cortada.

## 4. Imagem do Diego

A gravação é HLG/BT.2020. A conversão para SDR/BT.709 usa branco de referência de 203 nits (BT.2408) e tone mapping Hable, sem nenhum ajuste de cor. Comparei 4 conversões; esta foi a que manteve o tom de pele e a cor como gravados. Foi a única mudança na imagem, e precisa ser conferida no celular.

**Posição:**
- Na tela dividida, o rosto fica a 42% da metade de baixo.
- Em tela cheia aparece 2 vezes: no 975 MIL (2,77 s) e no "e aí veio a reação" (2,27 s). As duas passam de 2 s.

## 5. Checklist medido (`scripts/conferir.py` → `qa/conferencia.json`)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | **57,6 s**: acima do alvo de 45 s do formato. A fala gravada tem 56,6 s, e a regra é não cortar frase nem acelerar a voz |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 yuv420p, AAC 48 kHz estéreo ✅ |
| 3 | Rosto do Diego em tela cheia ≥ 2 s | 2,77 s e 2,27 s ✅ |
| 4 | Planos dentro do corte real do vídeo de origem | Cortes de cena medidos (detecção de cena); nenhum plano esticado ✅ |
| 5 | Legendas | 69 grupos, 1 linha, até 4 palavras; maior 773 px (x 153–927), dentro de x 72–944, centradas em x 540 ✅ |
| 6 | Imagem cai na palavra | Cada troca é ancorada numa palavra (0,07 s antes); maior desvio 0,20 s (no 975 MIL, que entra no início real da voz) ✅ |
| 7 | Imagens sem interface de app nem marca d'água | Recortes conferidos no 1º, no meio e no último quadro de cada plano (`qa/folha_cenas.jpg`, `qa/folha_1s.jpg`) ✅ |
| 8 | Costura da tela dividida | Listras laranja, rosa e roxo em y 895–905 ✅ |
| 9 | Áudio | −14,0 LUFS integrados, pico verdadeiro −1,3 dBTP, 0 amostras acima de −1 dBFS ✅ |
| 10 | Emendas sem espaço | Trechos contíguos (0 quadro entre eles). Uma emenda cai depois do "s" de "públicos" (−31 dB antes do corte, com fade de 12 ms) ✅ |
| 11 | Transcrição da voz final = fala gravada | Sim, palavra por palavra (`transcricao_conferencia.json`) ✅ |
| 12 | Nada na tela fora da fala | Os textos das animações vêm da fala. Duas adaptações: "OBRIGA A VOTAR" (fala: "obrigaria o conselho a votar") e "US$" ao lado do número (fala: "dólares") |
| 13 | Créditos | `creditos.md` ✅ |

**Transições:**
- **Racha ao meio:** no "partindo a cidade no meio", a imagem do drone parte por uma rachadura de néon rosa.
- **Luz de passagem:** no "mas a cidade continuou", saindo do carimbo NÃO.
- **Placa do DS:** no CTA.
- O resto é corte seco na palavra.

**Efeitos sonoros** (`rev1/sfx.json`, volumes da `REFERENCIA_EDICAO_FORMATOS.md` 4.1):
- `PDX_swish` na racha e na marca se espalhando;
- `PDX_impacto` no "DÓLARES", nas 5 batidas, no "CRIME" e no "NÃO";
- `PDX_obturador` no "25 MIL";
- `PDX_ar_longo` na Luz de passagem;
- `PD_clack` na placa do CTA.

## 6. Exceções e regras deste Reel (não viram regra geral)

- **Cores do GTA VI:** fora do DS V2, só neste Reel, a pedido do Diego. O DS entra só no CTA (placa "MANDA ESSE VÍDEO / MIAMI →", Chegada, clack), como manda a decisão de 28/10/2026.
- **Batidas do 975 MIL:** 5 efeitos em 2,1 s, contra a regra de no máximo 1 efeito a cada 1,5 s (DS 4.6 e REFERENCIA_EDICAO_FORMATOS 2). É pedido explícito do Diego.
- **Imagens de terceiros sem licença:** uso autorizado pelo Diego. Risco de alcance e de direito autoral registrado em `creditos.md`.
- **Duração de 57,6 s:** acima do alvo de 45 s do formato e dos 7–30 s da referência de conteúdo. Se a retenção cair antes da metade, a próxima revisão pode tirar o bloco "beleza que isso é preço de banana… conselho do condado a votar" (≈ 5,8 s).

## 7. Conferir no ouvido (o Claude não escuta; a escuta é do Diego)

1. As 12 emendas, principalmente "públicos" → "e aí veio a reação" (29,17 s), onde saiu "incluindo de tribunais".
2. O fim do "975 mil" para a câmera (18,37 s): se ficou algum resto do som que veio depois.
3. **Legenda a confirmar contra a fala:**
   - "agora Miami **está** se transformando" (as transcrições oscilam entre "está" e "tá");
   - "mas **está** partindo" (uma delas ouviu "mas isso tá partindo");
   - "vai viver **o** momento" (uma delas ouviu "um").
   Se alguma estiver errada, mude em `rev1/cenas.json` → `legenda.troca_palavra` e rode `scripts/montar.py` e o render.
4. Volume das batidas e dos efeitos (`PDX_*` e `PD_clack` nunca foram ouvidos).
5. A cor do vídeo do Diego depois da conversão HDR → SDR, no celular.

## 8. Fatos usados na fala e na legenda

| Fato | Fonte |
|---|---|
| GTA 6 sai em 19/11/2026 | Rockstar, rockstargames.com/VI |
| Letreiro "Welcome to Vice City" no telhado do Kaseya Center, US$ 975 mil, 25 mil abaixo do limite de US$ 1 milhão que exige votação | Fortune (19/10/2026), Notebookcheck (24/09/2026) |
| Proposta do condado: aeroporto, trens (Metromover), prédios públicos | Fortune, NBC 6 |
| Xerife: "GTA é uma franquia construída em torno de atividade criminosa" | NBC 6 (03/09/2026) |
| Carta da escrivã do tribunal e da juíza-chefe à prefeita: tribunais fora da campanha | NBC 6 |
| Burger Shot e Cluckin' Bell dentro do Kaseya Center | Dexerto, VGC (22/10/2026), posts no X |
| Cadeiras de praia, carros com placa de Vice City | VGC (relatos de fãs); fotos e vídeos de fãs |
| "Maior lançamento da história dos videogames" | **Opinião do Diego** (o jogo ainda não saiu); mantida por decisão dele |

## 9. Como refazer

De dentro de `reels/gta6-miami`, com os brutos em `fonte/`:
1. `python3 scripts/transcrever.py` (Whisper).
2. `scripts/alinhar.py`.
3. `scripts/decupar.py --render`.
4. `scripts/apoio.py`.
5. `scripts/montar.py`.
6. `scripts/mixar.py`.
7. Render no `design-system/remotion`, com `--props=reels/gta6-miami/rev1/props.json --public-dir=reels/gta6-miami/public`. A composição é a `ReelGTA` e sai muda.
8. Junte o vídeo com `rev1/audio_master.wav` no ffmpeg.
9. `scripts/conferir.py`.
