# QA · Reel de apresentação · REV7

**Arquivo:** `reels/apresentacao/rev7/reel_apresentacao_rev7.mp4`
**Branch:** `claude/rev7-reel-apresentacao` (base: `claude/wonderful-meitner-1mioxg`, commit `b6439dd`)
**Veredito técnico:** todos os testes obrigatórios passaram. Os pontos de atenção estão na seção 7.

Nenhum arquivo da REV6 foi alterado. Tudo da REV7 fica em `reels/apresentacao/rev7/`.

---

## 1. Formato

| Item | Pedido | Resultado | |
|---|---|---|---|
| Resolução | 1080 × 1920 | 1080 × 1920 | ✅ |
| Quadros por segundo | 24 | 24/1 | ✅ |
| Quadros | 643 | 643 (contados) | ✅ |
| Duração | 26,792 s | vídeo 26,792 s · áudio 26,791 s | ✅ |
| Vídeo | H.264 | H.264 High, yuv420p, BT.709 limitado, CRF 16 | ✅ |
| Áudio | AAC 48 kHz | AAC LC, 48 kHz, estéreo, 192 kbps | ✅ |
| Tamanho | — | 54.893.365 bytes (52,4 MB) | — |
| SHA-256 | — | `188867893caed4a5baffaea8b47715cfd8e964a33989a1881f1abb7ee29068f8` | — |

## 2. Montagem (12 planos)

Cada quadro da REV7 foi comparado com o quadro de origem aprovado e com os quadros vizinhos (±1), na região sem gráficos (y < 1096). Resultado: **643 de 643 quadros** batem com a origem exata. O PSNR mínimo é 48,9 dB e a mediana, 52,8 dB; a diferença vem só da recompressão.

| # | Origem (s) | REV7 (s) | Quadros | Cena |
|---|---|---|---|---|
| 1 | 14,917–17,375 | 0,000–2,458 | 59 | Selfie andando: "Buenos días, Barcelona!" |
| 2 | 3,000–4,125 | 2,458–3,583 | 27 | Balcão do bar |
| 3 | 4,125–6,958 | 3,583–6,417 | 68 | Indo ao Arco do Triunfo |
| 4 | 6,958–8,458 | 6,417–7,917 | 36 | Selfie em Paris |
| 5 | 8,458–10,750 | 7,917–10,208 | 55 | Camp Nou / fila |
| 6 | 10,750–12,375 | 10,208–11,833 | 39 | Brinde / patatas bravas |
| 7 | 12,375–14,917 | 11,833–14,375 | 61 | Diego no Arco |
| 8 | 19,625–22,125 | 14,375–16,875 | 60 | Amsterdam: "Chegamos!" |
| 9 | 22,125–24,000 | 16,875–18,750 | 45 | Selfie com a Torre Eiffel |
| 10 | 24,708–26,208 | 18,750–20,250 | 36 | Bruges: waffle |
| 11 | 30,208–34,750 | 20,250–24,792 | 109 | Selfie no bar: "…primeira tapa de Barcelona." |
| 12 | 38,625–40,625 | 24,792–26,792 | 48 | Barceloneta / Hotel W |

Outros resultados:
- **Tela preta:** nenhum quadro preto. A luma média mínima é 102 (de 0 a 255).
- **Fade:** nenhum. A luma média de cada quadro difere no máximo 0,14 da origem.
- **Fim do plano 12:** termina em 40,625 s da origem, antes do fade para preto que a base tem a partir de 40,708 s.

## 3. Gráficos

### 3.1 Placa `PRIMEIRO DIA →`

| Item | Valor |
|---|---|
| Posição | x 72 · y 1104 (exceção da REV7, CLAUDE.md §11) |
| Tamanho | 649 × 136 px. Ocupa x 72–721 · y 1104–1240 (o handoff previa ~752; ficou 31 px mais curta, medida com a fonte real) |
| Estilo | Fundo `#FFC21A`, texto `#16181D`, raio 8, sem contorno |
| Texto | Barlow Condensed ExtraBold 104, +1% de espaçamento, padding horizontal de 24 px |
| Seta | Desenhada como forma, não digitada. Grafite, 78 px de altura, haste de 12,48 px (16%), ponta cheia de 39 px (50%), 70 px de largura total, a 24 px do texto |
| Entrada | Desliza da esquerda em 3 quadros (120 ms, curva `enter`), começando no quadro 0. Posição x por quadro: −20 → 60 → 72. É recortada em x 72, então nunca sai da safe zone. |
| Saída | Corte seco no quadro 59 (2,458 s), junto com o corte para o bar. Não aparece no plano do bar. |

**Rosto livre:** conferido em todos os quadros do plano 1, 1 a cada 4 (`qa_frames/rosto_x_placa_plano1_y860-1220.jpg`). O queixo fica sempre acima da placa. Em **2,0 s** (quadro 48) o queixo termina em y ≈ 1070, cerca de **34 px acima** do topo da placa. A placa fica sobre o suéter.

### 3.2 Legendas

**Estilo:**
- Faixa `#16181D` com raio 8 e padding 12/24.
- Barlow SemiBold 52 em `#F6F3EC`, entrelinha 1,2, topo em y 1272.
- Centralizada na coluna de conteúdo do DS 5.3 (x 72–944).

**Limites:**
- No máximo 2 linhas: só "até porque o primeiro dia / a gente nunca esquece." tem duas, e a base da faixa fica em y 1421, dentro do limite de 1440.
- A linha mais longa tem 29 caracteres, abaixo do máximo de 32.

**Mini-placas:**
- Só em **soteropolitano** e **perrengues**.
- Barlow SemiBold 52 grafite sobre caixa `#FFC21A`, raio 8, padding horizontal de 8 px.
- A caixa fica dentro da faixa, com 12 px de grafite acima e abaixo.

**Textos:** comparados caractere a caractere com a lista aprovada. São **idênticos**.

| Legenda | Na tela (REV7, s) | Fala (REV7, s) | Origem do tempo |
|---|---|---|---|
| Buenos días, Barcelona! | 0,292–2,458 | 0,290–1,810 | forma de onda |
| Eu sou o Diego, | 2,833–3,583 | 2,823–3,583 | SRT nº 1 |
| sou **soteropolitano** | 3,792–5,000 | 3,788–5,005 | SRT nº 2 |
| e aqui eu te mostro | 5,000–5,750 | 5,005–5,758 | SRT nº 3 |
| o primeiro dia | 5,750–6,417 | 5,758–6,416 | SRT nº 4 |
| em cada cidade que eu visito, | 6,417–7,917 | 6,416–7,833 | SRT nº 5 + 6 (uma legenda só, como aprovado) |
| a chegada, | 8,083–9,083 | 8,098–8,973 | SRT nº 7 |
| os meus **perrengues** | 9,083–10,208 | 9,092–10,153 | SRT nº 8 |
| e o que mais me surpreende, | 10,333–11,833 | 10,333–11,718 | SRT nº 9 + 10 |
| até porque o primeiro dia / a gente nunca esquece. | 12,000–14,375 | 11,998–14,333 | SRT nº 11 + 12 |
| Chegamos! | 16,208–16,875 | 16,210–16,640 | forma de onda |
| E agora eu acabei | 20,833–21,417 | 20,820–… | forma de onda |
| de pedir minha primeira | 21,417–22,833 | 21,420–… | forma de onda |
| tapa de Barcelona. | 22,833–24,792 | 22,840–24,720 | forma de onda |

**Regra de tempo:**
- Cada legenda entra no quadro mais próximo do início da fala, no máximo 1 quadro antes.
- Sai quando entra a próxima ou no corte seguinte, o que vier primeiro.
- Nenhuma legenda atravessa um corte.

**Como as falas sem SRT foram medidas:**
- Usei os trechos com a voz do Diego (autocorrelação; f0 de 115–210 Hz, a dele fica em ~140–175 Hz; nível acima de −21 dBFS).
- Medidas na origem (s), com a referência por palavra da REV6 (whisper) entre parênteses:

| Fala | Medido | Referência REV6 |
|---|---|---|
| "Buenos días, Barcelona!" | 15,207–16,727 | 15,197–16,977 |
| "Chegamos!" | 21,460–21,890 | 21,417–21,917 |
| Plano 11, frase inteira | 30,778–34,678 | 30,308–34,528 |

- **Início do plano 11:** a referência da REV6 indicava 30,308. Entre 30,20 e 30,45 s há outra voz no fundo do bar (f0 ~190–280 Hz). A voz do Diego começa em 30,778.
- **Fronteira antes de "de pedir minha primeira":** em 31,378, depois de uma pausa de 0,22 s (referência: 31,428).
- **Fronteira antes de "tapa de Barcelona.":** em 32,798, depois de uma pausa de 0,56 s (referência: 33,008).

### 3.3 Fechamento

- Somente `@primeirodiaem`, em Barlow SemiBold 40 `#F6F3EC`.
- Faixa grafite com a mesma anatomia da legenda (raio 8, padding 12/24), centralizada.
- Ocupa x 338–677 · y 1272–1344.
- Vai de **24,792 a 26,792 s** (quadros 595–642), sobre a Barceloneta.
- Sem símbolo 1º e sem preset de cor.

### 3.4 Conferências automáticas (em todos os 643 quadros)

| Teste | Resultado |
|---|---|
| Algum pixel gráfico fora da safe zone (x 72–944 · y 256–1440) | **0** ✅ |
| Placa sobreposta a legenda | **0**. Folga de 32 px (placa termina em y 1240, legenda começa em y 1272) ✅ |
| Cores | Todo pixel opaco é `#FFC21A`, `#16181D`, `#F6F3EC` ou mistura de antialias entre dois deles ✅ |
| Fontes | Só Barlow SemiBold e Barlow Condensed ExtraBold, baixadas do Google Fonts (hash no relatório) ✅ |
| Transparência parcial | Só nas bordas antialiasadas (≤ 0,5% dos pixels). Nenhum elemento semitransparente e nenhum fade ✅ |

## 4. Áudio

| Item | Resultado | |
|---|---|---|
| Fonte | A mixagem do vídeo sem texto da REV6. Sem música e sem ganho (0 dB) | ✅ |
| Pico verdadeiro (MP4) | **−2,6 dBTP** (limite: −1 dBTP; a base tem −2,2) | ✅ |
| Loudness integrada | −14,5 LUFS. A base tem −15,2 com outros trechos; não houve ganho | — |
| Amostras iguais à base | 6 de 6 blocos, **diferença 0,0** fora das janelas de 50 ms das emendas e da rampa de 30 ms | ✅ |
| Fala de apresentação completa | "Eu sou o Diego, … a gente nunca esquece." (REV7 2,823–14,333 s) está idêntica à base, amostra por amostra, até 14,325 s. Os 8 ms finais do intervalo do SRT entram no início do crossfade da emenda de 14,375 s (seção 7) | ✅ |
| Emendas internas da narração | Preservadas: os planos 2–7 são um bloco contínuo da origem | ✅ |

**Emendas novas:** crossfade equal-power de 0,1 s, centrado na emenda, com 50 ms da própria origem de cada lado. A duração não muda.

| Emenda (s) | RMS antes → depois (dBFS) | Maior salto entre amostras (relativo ao p99,9 do entorno; ≥ 4 seria estalo) | |
|---|---|---|---|
| 2,458 | −18,8 → −22,3 | 1,25 | ✅ |
| 14,375 | −22,0 → −33,7 | 1,17 | ✅ (seção 7) |
| 18,750 | −22,1 → −22,8 | 1,37 | ✅ |
| 20,250 | −24,4 → −23,8 | 1,22 | ✅ |
| 24,792 | −18,9 → −20,3 | 1,31 | ✅ |

- **Começo e fim do arquivo:** rampa de 30 ms, a mesma entrada de 30 ms da REV6. É só um declique: a primeira e a última amostra valem 0,0 e não há degrau. Não é fade audível.

## 5. Elementos proibidos

Todos ausentes. O pipeline só desenha placa, legendas, mini-placas e assinatura, e a contagem de cores do item 3.4 confirma.

- **Elementos da REV6/v0:**
  - título "Aqui é o / Primeiro Dia";
  - pílula "DIA 1" e nomes de cidade;
  - faixa azul-petróleo;
  - palavras em terracota;
  - DM Serif Display e Montserrat;
  - sublinhado âmbar;
  - sombra do cartão;
  - "Segue para acompanhar / a próxima chegada";
  - fade do título e fade para preto.
- **Planos removidos:**
  - "Chegamos ao nosso primeiro destino." (o plano 1 termina em 17,375 da origem, antes de 17,757, onde a frase começa);
  - "Muito, muito, muito, muito." (origem 27,208–30,208 não entra).
- **Elementos não aprovados para a REV7:**
  - Placar do Dia;
  - Bilhete;
  - Varredura amarela;
  - placas de cidade;
  - etiqueta de valor;
  - símbolo 1º;
  - `PRIMEIRO DIA EM / BARCELONA →`.
- **Marca d'água:** nenhuma. Só há os gráficos acima sobre a base da REV6.

## 6. Frames de QA

Pasta: `reels/apresentacao/rev7/qa_frames/` (JPG em qualidade máxima, 1080 × 1920).

| Arquivo | O que conferir |
|---|---|
| `rev7_q000_quadro000.jpg` · `q001` · `q002` | Entrada da placa (quadros 0, 1 e 2), recortada em x 72 |
| `rev7_q003_quadro003.jpg` | Placa parada em x 72 · y 1104 |
| `rev7_t00_00s` … `rev7_t02_40s` | Gancho: rosto livre, placa + "Buenos días, Barcelona!" |
| `rev7_t02_00s_quadro048.jpg` | Distância queixo × placa (~34 px) |
| `rev7_q058_quadro058.jpg` / `rev7_q059_quadro059.jpg` | Último quadro com placa / primeiro quadro do bar, sem placa |
| `rev7_t06_40s` | "o primeiro dia" (último quadro do plano 3) |
| `rev7_t14_30s` | Legenda de 2 linhas no Arco |
| `rev7_t16_80s` | "Chegamos!" |
| `rev7_t20_20s` | Bruges, sem texto |
| `rev7_t24_70s` | "tapa de Barcelona." |
| `rev7_t25_50s` · `rev7_t26_70s` | Fechamento `@primeirodiaem` |
| `folha_qa_rev7.jpg` | Todos os frames acima com a safe zone em vermelho (a linha só existe na folha) |
| `rosto_x_placa_plano1_y860-1220.jpg` | Faixa y 860–1220 em 15 quadros do plano 1 |

## 7. Pontos de atenção (não bloqueiam a entrega)

1. **Emenda de 14,375 s (−11,7 dB):** é diferença de conteúdo, não estalo.
   - Antes do corte ainda está o fim da voz da narração ("esquece.").
   - Depois vem o ambiente baixo de Amsterdam, no nível original da cena (o ruído de fundo dela já era −32 dBFS na REV6).
   - O maior salto entre amostras é 1,17, sem impulso.
   - O SRT da REV6 dá o fim de "esquece." em 14,333 s, 8 ms dentro do crossfade. Nesses 8 ms o ganho fica acima de 0,99.
2. **"E agora eu acabei" fica só 0,58 s na tela**, porque o Diego fala rápido nesse trecho.
   - A fronteira com "de pedir minha primeira" (31,378 s na origem) foi escolhida pela pausa de voz mais próxima da referência da REV6.
   - A outra pausa candidata, em 31,638 s, deixaria a legenda 0,17 s a mais na tela.
   - O texto não foi alterado.
3. **Áudio herdado da REV6:** as limitações registradas em `REVISAO_6.md` §6 continuam (por exemplo, o "s" modelado de "Chegamos!" e o resto do tratamento da rev. 5 em "Buenos días" e na "tapa"). A REV7 não mexe nisso.
4. **Placa mais curta que no handoff:** termina em x 721, não em ~752. A largura sai da fonte real com os paddings e a seta aprovados.

## 8. Como reproduzir

```bash
cd reels/apresentacao
python3 rev7/scripts/rev7.py --fontes PASTA_COM_AS_TTF
```

- **Requisitos:** Python 3.11, Pillow, numpy e FFmpeg 6.1.
- **Fontes:** Barlow-SemiBold.ttf e BarlowCondensed-ExtraBold.ttf (SIL OFL), do Google Fonts. Os links estão no cabeçalho do script.
- **Configuração:** fica em `rev7/rev7.json` (planos, textos, tokens e posições).
- **Temporários:** vão para `rev7/_tmp/`, fora do Git.

| Arquivo | O que é |
|---|---|
| `rev7/reel_apresentacao_rev7.mp4` | Entrega |
| `rev7/rev7.json` | Configuração da REV7 |
| `rev7/scripts/rev7.py` | Pipeline completo: tempos, gráficos, áudio, vídeo e QA |
| `rev7/relatorio_tecnico_rev7.json` | Todas as medidas deste relatório, geradas pelo pipeline |
| `rev7/qa_frames/` | Frames de QA |
| `rev7/QA_REV7.md` | Este relatório |
