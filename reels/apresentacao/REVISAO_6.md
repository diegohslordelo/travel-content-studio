# Revisão 6 · relatório

Pedido de 01/10:
- aprovar o áudio da revisão 6;
- não cortar a fala do "Chegamos!";
- corrigir os erros de transição;
- incluir o vídeo de Paris como mais um corte na narração, sem a fala dele;
- renderizar direto.

Os arquivos da revisão 5 continuam intactos. Os da revisão 6 têm `_rev6` no nome.

## 1. Corte novo na narração: Paris

**Clipe:** `IMG_2978.MOV`.
- Jardim das Tulherias, com o Louvre ao fundo, em 17/03 às 14h16.
- 4K HDR (HLG), gravado com o celular deitado.
- Recebeu o mesmo tratamento das outras cenas: girado 90°, recorte 9:16 centrado no rosto (0,47) e HLG → SDR Rec.709 com o mesmo tone mapping.

**Onde entra:**
- De **6,958 a 8,458 s**, exatamente em "**em cada cidade que eu visito,**". Outra cidade aparece quando a narração fala de cada cidade.
- O corte de entrada cai na fronteira entre "o primeiro dia" e "em cada cidade", localizada no espectrograma: o "dj" de "dia" vai de 6,77 a 6,83 s e o "em" começa em 6,95 s.
- O corte de saída é o mesmo da rev. 5, na pausa depois de "visito,".

**Trecho do clipe:** 5,55 a 7,05 s.
- É o trecho em que você mais sorri e ri olhando para o lado.
- Os 0,5 s iniciais são um movimento rápido de câmera e ficaram de fora.
- A partir de 6,75 s ela entra pela borda direita, mas fica fora do recorte.

**A sua fala não entra.** Você fala de 0,5 a 7,2 s do clipe ("E o mais surreal disso tudo aqui é que você vê a Torre Eiffel de qualquer lugar…").
- O som por baixo da narração é só o **ambiente das pausas do próprio clipe**: 6,10–6,50, 2,66–3,04, 7,26–7,55 e 0,03–0,30 s.
- O trecho de 7,57 a 7,96 s ficou de fora, porque tem toques no celular.
- Esse ambiente recebeu o mesmo ducking e o mesmo nível do ambiente do Arco, com crossfades de 0,2 s nos dois cortes.

**O que mudou em volta:**
- O Arco (de costas) agora cobre "sou soteropolitano, e aqui eu te mostro o primeiro dia" (4,125–6,958 s), com os primeiros 68 quadros do mesmo plano.

## 2. "Chegamos!" (Amsterdam)

**Diagnóstico:**
- A voz não era cortada. "Chegamos" vai de 21,68 a 22,12 s na rev. 5, e a boca e a voz estão sincronizadas.
- O problema era o **"s" final**: é um "Chegamosss!" com uns 0,3 s, de IMG_1384 8,80 até depois de 9,08 s.
- A transição para a Torre Eiffel começava a baixar o som 0,1 s antes do corte, com o vento da Torre Eiffel subindo por cima. O "s" era engolido.

**Correção:** o vídeo original termina em 9,0 s e não há mais imagem, então a solução foi um **corte em L**.
- O som do "Chegamos!" segue **0,12 s por cima da Torre Eiffel** e termina em 22,25 s.
- A Torre Eiffel só entra depois do corte de imagem, em 0,25 s.
- O "s" que fica depois do corte foi recuperado das duas versões antigas em que ele aparece (rev. 3 e rev. 5), desfazendo a curva da transição.
- As duas fontes batem em ±0,5 dB, e a correlação entre elas é de 0,95.

## 3. Erros de transição corrigidos

| Corte | Erro | Correção |
|---|---|---|
| Vaso de Oro → Arco | A boca começava a abrir em 3,75 s e ficava aberta, sem som, até o corte em 4,25 s | Corte em 4,125 s, ainda na pausa depois de "Diego,". A boca que sobra coincide com "o Diego" |
| Entrada de Amsterdam | Os 3 primeiros quadros eram o fim de um movimento de câmera (15 px por quadro, contra 1 a 3 px no resto) | Amsterdam começa 5 quadros depois (IMG 6,508 s), já estável. O Reel ficou 5 quadros mais curto |
| "Buenos días" → Amsterdam | O crossfade misturava o som tratado com o cru | Crossfade de 0,2 s entre o ambiente da própria cena 7 e o som cru de Amsterdam |
| Amsterdam → Torre Eiffel | O "s" de "Chegamos!" era engolido | Corte em L (seção 2) |
| Legendas da narração | "e aqui eu te mostro", "o primeiro dia", "em cada cidade" e "que eu visito," estavam até 0,3 s adiantadas. "a gente nunca esquece." passava 1 quadro para dentro do "Buenos días" | Retemporizadas pela fala real. Agora trocam junto com os cortes (`narracao/narracao_rev6.srt`) |
| Começo do Reel | (da rev. 6 do áudio) degrau na amostra 0 | Entrada de 30 ms |

## 4. Lista de cortes da revisão 6

| # | Reel (s) | Origem | Trecho | O que é |
|---|---|---|---|---|
| 1 | 0,000–3,000 | IMG_1192 | 2,00–5,00 | Sagrada Família (gancho) |
| 2 | 3,000–4,125 | master | 475,25–476,38 | El Vaso de Oro: "Eu sou o Diego," |
| 3 | 4,125–6,958 | IMG_0781 | 3,08–5,91 | Arco, de costas: "sou soteropolitano, e aqui eu te mostro o primeiro dia" |
| 4 | **6,958–8,458** | **IMG_2978** | **5,55–7,05** | **Paris (novo): "em cada cidade que eu visito,"** |
| 5 | 8,458–10,750 | IMG_0502 | 2,67–4,96 | Camp Nou: "a chegada, os meus perrengues" |
| 6 | 10,750–12,375 | IMG_0816 | 23,40–25,03 | Brinde: "e o que mais me surpreende," |
| 7 | 12,375–14,917 | IMG_0781 | 8,92–11,46 | Arco, vira: "até porque o primeiro dia a gente nunca esquece." |
| 8 | 14,917–19,625 | master | 0,30–5,01 | "Buenos días, Barcelona! Chegamos ao nosso primeiro destino." |
| 9 | 19,625–22,125 | IMG_1384 | **6,51**–9,01 | Amsterdam: "Chegamos!" |
| 10 | 22,125–24,708 | IMG_2761 | 1,80–4,38 | Torre Eiffel |
| 11 | 24,708–27,208 | IMG_2693 | 6,00–8,50 | Waffle |
| 12 | 27,208–30,208 | IMG_2693 | 12,40–15,40 | "Muito," / "muito, muito, muito." |
| 13 | 30,208–34,750 | IMG_0816 | 12,90–17,44 | "E agora eu acabei de pedir minha primeira tapa de Barcelona." |
| 14 | 34,750–41,208 | IMG_0690 | 9,96–16,42 | Barceloneta: "Segue para acompanhar / a próxima chegada" |

**Total:** 41,21 s (989 quadros a 24 fps).

## 5. Conferido no arquivo final

- **Formato:** 1080x1920, 24 fps, 989 quadros, H.264 High 4.1, Rec.709, AAC 48 kHz 192 kbps (prévia leve: 540x960, AAC 128 kbps).
  - A imagem das cenas que não mudaram vem do Reel da rev. 5. Os brutos não estão nesta máquina.
  - Ela foi copiada quadro a quadro, com diferença zero conferida, e recodificada em CRF 16 em vez de 18, para compensar a segunda compressão.
- **Volume:** −15,2 LUFS integrados, pico verdadeiro −2,2 dBTP, nenhuma amostra em 0 dBFS (prévia leve: −1,8 dBTP).
- **Transcrição** (faster-whisper medium, tempo por palavra, em estéreo, alto-falante de celular e mono):
  - a narração está inteira, de "Eu sou o Diego" a "nunca esquece";
  - as falas também: "Buenos días, Barcelona", "Chegamos ao nosso primeiro destino", "Chegamos", "muito, muito…" e "E agora eu acabei de pedir minha primeira tapa de Barcelona";
  - nenhuma palavra do clipe de Paris aparece ("surreal", "Torre Eiffel", "qualquer lugar", "incrível").
- **Sincronia boca × voz:** igual à rev. 5. No "m" de "Chegamos" os lábios fecham no mesmo quadro do vale da voz, e na "tapa" a defasagem medida é 0.
- **Zona segura:** o render confere os 989 quadros da camada de texto. Veja também `qa_frames_por_cena_rev6.jpg`.
- **Transições:**
  - sob a narração, o nível do ambiente varia no máximo 2,3 dB entre cortes;
  - não há estalo novo: o impulso do clipe de Paris foi evitado, e os demais pontos são sons reais que já existiam.

### Áudio por cena (arquivo .mp4 final)

| Cena | Ruído de fundo (dBFS) | LUFS da voz | LUFS fora da voz | Curto prazo, mediana | Pico verdadeiro (dBTP) |
|---|---|---|---|---|---|
| 01 gancho Sagrada (amb.) | −23,5 | — | −17,9 | −17,9 | −2,7 |
| 02 Vaso de Oro + narração | −27,6 | −11,0 | — | −12,7 | −2,7 |
| 03 Arco + narração | −29,4 | −14,6 | — | −14,7 | −2,9 |
| 04 Paris + narração (novo) | −32,3 | −14,0 | — | −14,7 | −2,7 |
| 05 Camp Nou + narração | −33,6 | −14,6 | — | −14,8 | −2,8 |
| 06 Brinde + narração | −35,0 | −12,8 | — | −13,3 | −2,2 |
| 07 Arco + narração | −32,5 | −12,2 | — | −12,9 | −2,8 |
| 08 Fala: Buenos días | −25,7 | −13,2 | −16,0 | −13,5 | −2,9 |
| 09 Fala: Chegamos! | −32,4 | −13,9 | −24,4 | −19,1 | −4,8 |
| 10 Torre Eiffel (amb.) | −27,1 | — | −17,7 | −18,0 | −5,1 |
| 11 Waffle (amb.) | −25,5 | — | −17,6 | −17,9 | −5,4 |
| 12 Fala: Muito (Diego + ela) | −30,4 | −13,5 | −21,5 | −14,2 | −2,8 |
| 13 Fala: tapa | −24,5 | −13,8 | — | −13,8 | −2,9 |
| 14 Fechamento (amb.) | −25,8 | — | −18,0 | −17,7 | −2,8 |

Reel inteiro (arquivo .mp4): **−15,2 LUFS integrados, pico verdadeiro −2,2 dBTP**, 0 amostras em 0 dBFS.

- **Voz no curto prazo:** fica em torno de −13 a −15 LUFS, e não em −18, para o Reel fechar em −15 integrado (como explicado na rev. 5).
- **Cena 09:** a mediana mais baixa (−19,1) se deve ao trecho sem fala antes do "Chegamos!".

## 6. O que ainda não está perfeito

1. **Paris:**
   - Você fala quase o clipe inteiro, então a boca se mexe, sem som, por cerca de 0,25 s no começo e 0,15 s no fim do plano.
   - No meio dele você sorri e ri.
2. **"tapa":** a imagem corta 0,09 s depois de "Barcelona.". Para ganhar 2 quadros de folga, é preciso o bruto IMG_0816.
3. **"Buenos días", Bruges e "tapa":** ainda carregam o resto do tratamento da rev. 5. Os agudos foram devolvidos na rev. 6. Para ficarem 100% crus, é preciso os brutos (master 0–6 s, IMG_2693 e IMG_0816).
4. **"Chegamos!":** o "s" depois de IMG 9,08 s não existe em nenhuma versão guardada. O final de 50 ms foi modelado.
5. **Waffle → "Muito":** é um corte seco dentro do mesmo plano (jump cut, estilo vlog). Foi mantido.

## Arquivos

| Arquivo | O que é |
|---|---|
| `reel_apresentacao_rev6.mp4` | **Versão final com texto** |
| `reel_apresentacao_sem_texto_rev6.mp4` | A mesma edição sem textos |
| `reel_apresentacao_previa_leve_rev6.mp4` | Cópia leve (540x960) para ver no celular |
| `qa_frames_por_cena_rev6.jpg` | Primeiro, meio e último quadro de cada cena, com a zona segura |
| `previa_reel_1fps_rev6.jpg` | Um quadro por segundo |
| `lista_de_cortes_rev6.json`, `narracao/narracao_rev6.srt` | Lista de cortes e legendas da narração da rev. 6 |
| `revisao_6_audio/audio_reel_rev6_final.flac` | Áudio final do Reel |
| `scripts/montar_video_rev6.py`, `scripts/final_rev6.py`, `revisao_6_audio/scripts/montar_audio_rev6.py` | Montagem da imagem, codificação e montagem do áudio |
| `capa_reel_apresentacao.jpg`, `legenda.txt` | Sem mudança |
