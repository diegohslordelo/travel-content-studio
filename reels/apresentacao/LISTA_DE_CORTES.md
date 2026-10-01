# Lista de cortes · Reel de apresentação "Primeiro Dia" (revisão 5, RENDERIZADA)

> **Revisão 5:** só a cena do museu (camisa do Bahia, desfocada) foi trocada, pelo El Vaso de Oro. A narração agora entra inteira na apresentação. O resto da revisão 4 continua igual. O relatório completo está em `REVISAO_5.md`.


Os `.mp4` desta pasta são desta revisão.

Reel: **41,4 s** (994 quadros a 24 fps), 13 cortes. Gancho 0–3 s · apresentação 3–14,9 s · montagem 14,9–35,0 s · fechamento 35,0–41,4 s.

Imagens de apoio nesta pasta:
- `storyboard_lista_de_cortes.jpg`: um quadro de cada corte, com o crop, a cor e os textos finais.
- `teste_voz.mp4` e `teste_voz_lufs.txt`: os trechos com voz já tratados e o loudness medido.
- `analise_outras/folhas_brutos/`: folhas de frames dos 7 brutos de Barcelona.

## 1. Correspondência com os brutos (https://gofile.io/d/UKhCf0Vi)

Pela data de gravação, os 7 brutos são de 09/03, o dia 1 (o master tem o dia 1 até 10:57). A exceção é a Sagrada Família, de 11/03, usada só no gancho.
Achei o trecho exato de cada cena comparando quadro a quadro (correlação de 0,996 a 0,998). A única exceção é o gancho.
Depois conferi o som de cada bruto com o classificador de áudio (AudioSet) e a transcrição por palavra.

| Cena da lista atual (rev. 3) | Bruto | Trecho exato no bruto | Trecho usado | Mesmo momento? |
|---|---|---|---|---|
| 1 · Gancho, Sagrada Família (master 26:12,10) | IMG_1192.MOV | não está no bruto | 2,00–5,00 s | **Momento novo.** O plano do master (palmeira à direita) não está no bruto; usei outro ângulo da Sagrada, no trecho sem música. |
| 2 · Museu do Barça, camisa do Bahia (01:31,75) | IMG_0520.MOV | 0,08–3,08 s | 15,00–16,04 s | **Trocada na revisão 5 pelo El Vaso de Oro (master 475,25 s): desfocada.** O trecho exato tem música do museu (índice 0,5). Depois dela, você posa com o polegar para cima, de camisa do Bahia. |
| 3 · Arco do Triunfo (09:25,83) | IMG_0781.MOV | 3,08–6,08 s | 3,08–7,16 s e 8,92–11,42 s | **Mesmo momento** (estendido até o fim da frase) e **um momento novo** do mesmo bruto: você se vira e volta sorrindo. |
| 4 · Brinde (10:39,40) | IMG_0816.MP4 | 22,00–25,00 s | 23,40–25,03 s | **Mesmo plano, 1,4 s depois.** O trecho exato começa no meio da sua frase ("...uma cerveza para acompanhar."). |
| 5 · Chegando ao Camp Nou (01:11,15) | IMG_0502.MOV | 2,67–5,67 s | 2,67–5,04 s | **Mesmo momento.** |
| 11 · Vista de Montjuïc (03:38,20) | IMG_0586.MOV | 3,38–5,88 s | — | **Saiu.** O som do bruto inteiro tem o músico de rua cantando e tocando. |
| 14 · Praia da Barceloneta, fechamento (07:33,45) | IMG_0690.MOV | 9,96–16,42 s | 9,96–16,42 s (só a imagem) | **Mesmo momento, só a imagem.** O som do bruto tem violão do começo ao fim. |

**Cenas sem bruto correspondente:** nenhuma; os 7 brutos existem. Mas dois deles têm música em todo o som:
- **Montjuïc:** saiu da montagem. A cena não tem fala, e a regra é tirar primeiro as cenas sem fala.
- **Barceloneta (fechamento):** fica com a solução atual, o ambiente de pausas sem música do master. É a **única cena com som emprestado**.

**Duas cenas de fala também mudaram por causa das novas regras:**
- **"Minha primeira tapa":** agora vem do bruto IMG_0816, com a frase inteira ("E agora eu acabei de pedir minha primeira tapa de Barcelona.") e sem a trilha da edição.
- **Metrô ("A gente acabou de descer aqui na estação de Palau Real"):** saiu. No master há violão por baixo da fala (índice 0,51), e não veio bruto dessa cena. Se você tiver o bruto, eu recoloco.

## 2. Lista de cortes

"Trecho" é a posição no arquivo de origem, em segundos. Nas falas, o tempo no Reel está entre parênteses.

| # | Bloco | Reel | Arquivo | Trecho | Cidade | Ela aparece? | Descrição | Fala (texto exato, tempo no Reel) |
|---|---|---|---|---|---|---|---|---|
| 1 | Gancho | 0,00–3,00 | IMG_1192.MOV | 2,00–5,00 | Barcelona (dia 3) | não | Sagrada Família de baixo, com a palmeira | — (som da rua) |
| 2 | Apresentação | 3,00–4,25 | master BCN | 475,25–476,50 (07:55) | Barcelona | não | **El Vaso de Oro:** você abaixa a cerveja e olha para a câmera (**troca do museu desfocado**) | narração: "Eu sou o Diego," (3,37–4,10) |
| 3 | Apresentação | 4,25–8,46 | IMG_0781.MOV | 3,08–7,29 | Barcelona | não | De costas, indo até o Arco do Triunfo | narração: "sou soteropolitano, e aqui eu te mostro o primeiro dia em cada cidade que eu visito," (4,35–8,23) |
| 4 | Apresentação | 8,46–10,75 | IMG_0502.MOV | 2,67–4,96 | Barcelona | não | Chegando ao Camp Nou, com a fila | narração: "a chegada, os meus perrengues" (8,64–10,55) |
| 5 | Apresentação | 10,75–12,38 | IMG_0816.MP4 | 23,40–25,03 | Barcelona | não | Brinde com a cerveja, patatas bravas na mesa | narração: "e o que mais me surpreende," (10,88–12,11) |
| 6 | Apresentação | 12,38–14,92 | IMG_0781.MOV | 8,92–11,46 | Barcelona | não | No Arco, você se vira e volta sorrindo | narração: "até porque o primeiro dia a gente nunca esquece." (12,56–14,73) |
| 7 | Montagem | 14,92–19,62 | master BCN | 0,30–5,01 | Barcelona | não | Selfie andando em Gràcia | você: "Buenos días, Barcelona!" (15,20–16,98) · "Chegamos ao nosso primeiro destino." (17,76–19,44) |
| 8 | Montagem | 19,62–22,33 | IMG_1384.MOV | 6,30–9,01 | Amsterdam | **sim**, ao fundo com a mala | Ela chega com a mala, a câmera vira | você: "Chegamos!" (21,66–22,12) |
| 9 | Montagem | 22,33–24,92 | IMG_2761.MOV | 1,80–4,38 | Paris | **sim** (os dois) | Selfie com a Torre Eiffel | — |
| 10 | Montagem | 24,92–27,42 | IMG_2693.MOV | 6,00–8,50 | Bruges | não | Você morde o waffle, "Place de Brugge" atrás | — |
| 11 | Montagem | 27,42–30,42 | IMG_2693.MOV | 12,40–15,40 | Bruges | não (só a voz dela) | Você se vira e sai andando pela rua histórica | você: "Muito," (27,60–28,06) · ela: "muito, muito, muito." (28,40–30,18) |
| 12 | Montagem | 30,42–34,96 | IMG_0816.MP4 | 12,90–17,44 | Barcelona | não* | Selfie no bar de tapas | você: "E agora eu acabei de pedir minha primeira tapa de Barcelona." (30,52–34,74) |
| 13 | Fechamento | 34,96–41,42 | IMG_0690.MOV | 9,96–16,42 | Barcelona | não | Barceloneta: "Segue para acompanhar / a próxima chegada" | — (ambiente de pausas) |

\* **Corte 12:** nos primeiros 0,9 s ela sai pela borda direita do quadro original e nenhum crop 9:16 pega os dois rostos. O crop fica em você.

**Montagem:** 6 cenas, 2 delas de Barcelona. **Ela aparece em 2 cenas** (8 e 9) e só a voz dela entra na 11. Barcelona é só do dia 1, exceto o gancho.

### Onde entra cada corte na fala (folgas conferidas pela energia da voz, resolução de 5 ms)

| Corte no Reel | Pausa | Folga depois / antes |
|---|---|---|
| 3,00 (gancho → Vaso de Oro) | **respiro antes de "Eu" (3,37)**: a narração começa com o ar da própria gravação | — / 0,37 s |
| 4,25 | "Diego," → "sou" | 0,15 / 0,10 s |
| 8,46 | "visito," → "a chegada" | 0,23 / 0,18 s |
| 10,75 | "perrengues" → "e o que mais" | 0,20 / 0,13 s |
| 12,38 | "surpreende," → "até porque" | 0,27 / 0,19 s |
| 14,92 (apresentação → montagem) | depois de "esquece." (14,73), antes de "Buenos" (15,20) | 0,19 / 0,28 s |
| 19,62 · 22,33 · 27,42 · 30,42 · 34,96 | mesmas pausas da revisão 4 (a montagem só andou +0,29 s) | ≥ 0,18 / ≥ 0,10 s |

Total: **41,42 s** (994 frames).

## 3. Cena no lugar de Bruxelas

**Corte 11, Bruges, "rua":** o fim do mesmo plano do waffle (IMG_2693, 12,40–15,40 s). Você reage ("Muito,"), se vira e sai andando pela rua histórica.
Ela responde "muito, muito, muito." atrás da câmera. A cena entra logo depois da mordida no waffle.

**Por quê:**
- **Com ela:** das cenas de outras cidades que eu tinha, as selfies de Paris (Bonjour, Jardim de Luxemburgo) e de Amsterdam (aeroporto, Museumplein) não cabem no 9:16 sem cortar ela. Medi quadro a quadro com detecção de rosto.
- **720p:** os outros arquivos (Bruxelas e os waffles dela em Bruges) são 720p, o mesmo problema visual de Bruxelas.
- **Curta demais:** o plano de rua de Amsterdam dura só 1,3 s.
- **A escolhida:** esta é a única cena em 4K, com fala inteira e sem ela no quadro, que funciona.

Se você tiver outro vídeo em 4K de outra cidade, eu troco.

## 4. Áudio (revisão 5)

- **Voz** (narração e falas das cenas): passa-altas em 80 Hz, afftdn leve (6 dB na narração e 5 dB nas falas), +2,5 dB em 2–5 kHz e compressão de 2,5:1.
  Sem gate, pitch, de-esser nem reverb. O atraso de 25 ms do afftdn (medido: 24,75 ms) agora é compensado, então a voz não "pula" na imagem.
- **Níveis antes da normalização:** narração e falas em **−18 LUFS**; som das cenas sem fala em **−22 LUFS**, 4 dB abaixo da voz.
- **Ducking:** sidechaincompress com ataque de 50 ms e liberação de 400 ms, controlado por um sinal de nível constante enquanto você fala (preenche pausas menores que 0,5 s). Redução medida: **9,8 dB**, estável (variação média de 0,22 dB).
- **Final:** **−15,2 LUFS** integrados e pico de **−2,2 dBTP** no `.mp4`.
- **Correção importante:** na revisão 4, o `areverse` antes do `adelay` fazia o ffmpeg 6.1 ignorar o atraso da narração.
  Com isso, ela tocava a partir de ~0,05 s, embaixo do gancho, e dava a impressão de "começo cortado / sem a apresentação".
  Agora ela entra em 3,000 s, com a voz em 3,370 s.
- Os LUFS por trecho estão em `REVISAO_5.md`.

## 5. Textos

- **Narração:** legendas pelo tempo real das palavras (`narracao/narracao.srt`, até 5 palavras por tela).
  Destaque em terracota em "Diego", "soteropolitano", "primeiro dia" e "perrengues".
  O texto segue o que você gravou, não o roteiro antigo.
- **Falas da montagem:** legendas com o texto exato acima e o nome da cidade ao lado do selo ("DIA 1 · AMSTERDAM").
- **Fechamento:** "Segue para acompanhar / a próxima chegada", sem data. Capa sem mudanças.

## Sem mudanças

24 fps; o mesmo tone mapping HLG→SDR em todos os brutos HDR (os brutos de Barcelona são HLG); identidade visual; zona segura; as duas versões (com e sem texto) e a capa.
