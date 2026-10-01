# Revisão 5 · relatório de qualidade

Mudanças em relação à revisão 4:
- **Imagem:** só a cena do museu com a camisa do Bahia (desfocada) foi trocada. Os outros cortes e a montagem continuam iguais, como você pediu.
- **Voz:** a narração entra inteira, com respiro antes do "Eu".
- **Níveis:** novos alvos de loudness e de ducking.

## 1. A cena do museu (camisa do Bahia, "joia")

**Causa do desfoque:** o foco automático do iPhone ficou caçando o telão do museu, atrás de você.
- A nitidez do rosto e da camisa (variância do Laplaciano, medida a cada 0,5 s) fica em **~8** no trecho usado (IMG_0520, 15,0–16,0 s).
- O bruto só fica nítido em **18,0–18,75 s** (~40). Nesse trecho entra o coral do museu (música, índice 0,14), e a regra é não ter música.
- No master, as selfies com a camisa do Bahia têm fala por cima. Por isso, **nenhum trecho com a camisa do Bahia está nítido e limpo ao mesmo tempo.**

**Troca:** master, **El Vaso de Oro**, 475,25–476,50 s (dia 1). Você abaixa a cerveja e olha para a câmera, com o rosto no centro do crop.
- Nitidez de **32 a 56** no trecho (4 a 7 vezes a do museu).
- Sem fala e sem música.
- Mesmo tone mapping HLG→SDR, sem filtro de nitidez.

## 2. Auditoria por cena

Nitidez: variância do Laplaciano na região do rosto e do tronco (YuNet), média do trecho. Os números só servem para comparar cenas.

| # | Arquivo | Trecho | Nitidez | Problema | Decisão |
|---|---|---|---|---|---|
| 1 | IMG_1192.MOV | 2,00–5,00 | 610 | — | manter |
| 2 | ~~IMG_0520.MOV~~ → master | ~~15,00–16,04~~ → 475,25–476,50 | ~~8~~ → 32–56 | foco no telão | **trocar** (feito) |
| 3 | IMG_0781.MOV | 3,08–7,29 | 650 | — | manter |
| 4 | IMG_0502.MOV | 2,67–4,96 | 225 | — | manter |
| 5 | IMG_0816.MP4 | 23,40–25,03 | 49 | bar à noite, pouca luz | manter |
| 6 | IMG_0781.MOV | 8,92–11,46 | 578 | — | manter |
| 7 | master | 0,30–5,01 | 123 | tremida de selfie andando (mínimo 50) | manter |
| 8 | IMG_1384.MOV | 6,30–9,01 | 1511 | chicote de câmera nos primeiros quadros | manter |
| 9 | IMG_2761.MOV | 1,80–4,38 | 208 | — | manter |
| 10 | IMG_2693.MOV | 6,00–8,50 | 157 | — | manter |
| 11 | IMG_2693.MOV | 12,40–15,40 | 92 | movimento ao virar | manter |
| 12 | IMG_0816.MP4 | 12,90–17,44 | 23 | bar à noite; ela sai pela borda nos primeiros 0,9 s | manter |
| 13 | IMG_0690.MOV | 9,96–16,42 | 685 | ambiente de pausas no lugar do som do bruto (que tem violão) | manter |

## 3. Voz

**Transcrição do Reel final** (faster-whisper medium, trecho 2,9–15,2 s do `reel_apresentacao.mp4`):

> Eu sou o Diego, sou soteropolitano, e aqui eu te mostro o primeiro dia em cada cidade que eu visito. A chegada, os meus perrengues e o que mais me surpreende. Até porque o primeiro dia a gente nunca esquece.

Comparada palavra por palavra com o texto gravado, **está completa**: nenhuma palavra falta e nenhuma frase foi cortada.

- Em uma das rodadas, o Whisper ouviu "até porque **é** o primeiro dia" e "dia **e** a gente".
- Transcrevendo só esse trecho, ele ouve exatamente o mesmo no **arquivo original da narração** (`narracao.m4a`).
- Ou seja, é a ligação das vogais na sua pronúncia, já presente na gravação, e não algo que a edição acrescentou. A legenda segue o texto.

- **Começo:** a narração entra em 3,000 s, com o ar da própria gravação, e a primeira palavra vem em **3,370 s (0,37 s de respiro)**.
  - A frase termina em 14,73 s, e a montagem começa em 14,92 s.
  - A apresentação vai de 3,0 a 14,9 s (11,9 s).
- **Causa real do "começo cortado" na revisão 4:** no ffmpeg 6.1, o `areverse`, usado para o fade de saída, fazia o `adelay` ser ignorado.
  - A narração tocava a partir de ~0,05 s, embaixo do gancho, e na apresentação só sobrava o fim da frase.
  - Corrigi o filtro e conferi pela forma de onda (`_tmp/narracao_no_reel.wav`): a primeira amostra está em 3,000 s.
- **Atraso do afftdn:** 24,75 ms (medido por correlação), compensado na voz da narração e das falas.

## 4. Loudness

| Trecho | LUFS |
|---|---|
| **Reel inteiro (.mp4)** | **−15,2 LUFS integrados, pico −2,2 dBTP** (as duas versões) |
| Narração (3,37–14,73) | −13,8 |
| "Buenos días, Barcelona!…" | −13,8 |
| "Chegamos!" | −13,4 |
| "Muito, muito…" | −14,5 |
| "E agora eu acabei de pedir…" | −13,9 |
| Short-term (3 s) durante a narração | mín. −15,1 / mediana −14,1 / máx. −13,2 |
| Cenas sem fala (Sagrada, Eiffel, waffle, Barceloneta) | −17,8 a −18,1 |

- **Antes da normalização final:** narração em **−18,0 LUFS** e ambiente da apresentação sem ducking em **−22,0 LUFS**, uma diferença de **4,0 dB**.
- **Ducking** (sidechaincompress, ataque de 50 ms, liberação de 400 ms): redução de **9,8 dB** durante a narração (p10 10,0 / p90 9,5).
  - A variação média entre janelas de 50 ms é de **0,22 dB**, então não há "respiração" do ambiente.
  - Na primeira medição, o ambiente voltava a 0 dB em cada pausa entre as frases (10 saltos de mais de 3 dB).
  - Corrigi com um sinal de controle de nível constante enquanto você fala, que preenche as pausas menores que 0,5 s.
  - O ducking acaba junto com "esquece.", e "Buenos días" entra sem redução.
- A narração e as falas das cenas ficam no mesmo nível (−13,4 a −14,5). Não há salto de volume entre elas.

**Sobre "−18 short-term" e "−15 integrado":** as duas metas não cabem juntas.
- A voz ocupa a maior parte do Reel, então, para o arquivo dar −15 integrado, a voz precisa ficar perto de −14 short-term.
- Mantive a relação que você pediu: voz em −18 e ambiente 4 dB abaixo antes do ganho final. Depois, o ganho final de +4,2 dB leva tudo para −15.
- Se preferir a voz em −18 de fato, o Reel inteiro fica em ~−19 LUFS, e o Instagram tende a deixá-lo mais baixo que os outros vídeos.

## 5. Conferência depois do render

- **Frames:** `qa_frames_por_cena.jpg` mostra o primeiro, o do meio e o último frame de cada cena, com a zona segura em vermelho.
  - Foco, enquadramento e cor estão consistentes entre as cenas.
  - Nenhum rosto foi cortado. Ela aparece inteira nas cenas 8 e 9.
- **Zona segura:** conferi os 994 frames da camada de texto e nenhum pixel está fora (máximo x = 943, limite 960).
  - Na revisão 4, o título do gancho passava 9 px na margem direita e o card final passava 38 px.
  - Reduzi um pouco a fonte (gancho de 140 para 132 px, "a próxima chegada" de 100 para 94 px) e centralizei na faixa segura.
  - As legendas também passaram a ser centralizadas na faixa segura.
- **Duração:** 41,42 s, 1080x1920, 24 fps, H.264 + AAC 48 kHz.

## 6. O que ainda não está perfeito

1. **Cena 12 (tapa):** o rosto está macio (bar escuro, nitidez 23), e ela sai pela borda nos primeiros 0,9 s. Ficou como estava, a seu pedido.
2. **Cena 5 (brinde) e cena 12:** há música ambiente baixa do próprio bar por baixo. É o som real do lugar.
3. **Cena 8 (Amsterdam):** o primeiro quadro pega o fim de um chicote de câmera.
4. **Fechamento:** usa ambiente de pausas do master, porque o som do bruto da Barceloneta tem violão.
5. **Cena 2 (Vaso de Oro):** no último 0,5 s a sua boca começa a abrir, como quem vai falar, enquanto a narração diz "Diego,". Não se ouve nada, mas quem olhar com atenção pode notar.
6. **Loudness da voz:** −14 short-term no arquivo final em vez de −18 (explicado na seção 4).
7. **Transcrição:** o Whisper às vezes ouve um "é" em "porque o" e um "e" em "dia a gente". Isso também acontece no arquivo original (seção 3).
