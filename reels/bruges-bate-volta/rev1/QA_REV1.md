# QA · REV1 · Reel "Bruges não quer você lá"

**Entrega:** `rev1/reel_bruges-bate-volta_rev1.mp4` (master) e folhas de quadros em `rev1/qa_frames/`.
**Formato:** Jeito Errado × Jeito Certo (Trello) em tela dividida no gancho e paisagens em tela cheia depois, pedido do Diego (04/11/2026). DS V2 só no CTA (placa + clack).
**Pipeline:** `scripts/energia.py` → `scripts/voz.py rev1` → `scripts/alinhar.py rev1` → `scripts/reel.py rev1` (preparar, render, master). Composição: `design-system/remotion/src/bruges/`.

## Decisões desta revisão

| Decisão | Origem |
|---|---|
| Gancho B: cartão-postal do Rozenhoedkaai ao amanhecer cruzado por duas fitas de isolamento "POLITIE · POLICE", com o Diego embaixo desde o 1º quadro | Diego escolheu entre 3 prints (04/11/2026) |
| Texto do gancho = fala gravada: "BRUGES NÃO QUER / VOCÊ LÁ.", palavra por palavra. Sem regravação | Diego (04/11/2026), "manter a fala atual" |
| Não usar a foto de agência que o Diego mandou como referência (policial com cachorro). Ela é de agência de notícias e, pela placa do colete (ZPZ), de uma operação real em Bruxelas. Pôr uma placa na mão de um policial real seria adulterar a foto de uma pessoa real | FORMATOS_REELS 8.1 (proibido foto de agência) · CLAUDE.md 9 (contexto verdadeiro) |
| Fitas desenhadas, com a inscrição real da fita da polícia belga | Julgamento do Claude: não acrescenta texto que não foi dito ("PROIBIDO ENTRAR" ficou de fora) |
| **Vermelho #D7262E** só nas fitas: cor da fita de verdade, fora da paleta do formato | Valor novo registrado aqui; vale só para este Reel |
| CTA = placa do DS "NO SEU ROTEIRO / BRUGES" + módulo "?", sobre o mesmo cartão-postal do gancho, agora sem fitas (loop). A placa espelha a pergunta gravada ("você colocaria Bruges no seu roteiro?"), e o CTA é **comentar** | DS V2 2.7 · CLAUDE.md 6 |
| Fim em tela dividida porque a placa fica na posição fixa do DS (x 72 · y 640) e cobriria o rosto em tela cheia | DS V2, tokens `layout.reel.zone-plate-y` |
| Cortado "Você faz tudo a pé" (1,1 s), para cada imagem casar com a fala sem quebrar a regra de 2 s do material gravado. O corte de 4,39 s da IMG_7733 é um vale raso (−15 dB) e precisa de escuta | FORMATOS_REELS 9.2 (ordem de corte) |
| Mantidas as duas falas do jeito errado (IMG_7713 "eu fiz…" e IMG_7720 "Porto da Barra"), na ordem gravada | A fala gravada manda (FORMATOS_REELS 9.5) |
| Noite e amanhecer em **fotos** do Commons com licença livre e movimento de câmera, não em vídeo. O YouTube bloqueou o download nesta sessão ("sign in to confirm you're not a bot") e o Commons não tem vídeo de Bruges à noite ou ao amanhecer | Pedido do Diego: "busque na internet" |
| Prova na tela: captura real da Afar (18/06/2019) com selo "CAPTURA REAL" e a frase destacada | REFERENCIA_EDICAO_FORMATOS 6 |

## Roteiro de cortes (linha do tempo final, 55,1 s)

| Tempo | Fala | Imagem | Transição · som |
|---|---|---|---|
| 0,00–2,45 | Bruges não quer você lá. | **Tela dividida:** amanhecer no Rozenhoedkaai, as fitas batem em "quer" | `PDX_impacto` −4 dB em 0,80 s |
| 2,45–4,85 | Pelo menos não da maneira que todo mundo vai. | Dividida: barcos lotados no Rozenhoedkaai (IMG_4128), fitas na tela | — |
| 4,85–7,30 | A cidade tem menos de 120 mil | Belfort (IMG_4116), com contador **120 MIL** | Empurrão: a paisagem cresce e cobre o Diego · `PDX_swish` −6 dB |
| 7,30–9,30 | habitantes e recebeu | Canal (IMG_4128 início), **HABITANTES** | — |
| 9,30–11,88 | mais de 8 milhões de turistas em um ano. | Markt e Provinciaal Hof (IMG_4116), **8 MILHÕES · DE TURISTAS · EM 1 ANO** | `PDX_impacto` −4 dB |
| 11,88–13,88 | Lotou tanto que a própria Bruges | Multidão no Markt (IMG_4117) | — |
| 13,88–16,80 | parou de fazer propaganda em Bruxelas e em Paris. | Captura da Afar: título, depois o trecho destacado | `PDX_obturador` −8 dB |
| 16,80–19,32 | E eu sei qual o jeito errado. Porque eu fiz. | Diego em tela cheia | — |
| 19,32–21,32 | Cheguei lá às 11 horas | Janela do trem (IMG_4244) + relógio **11H** | — |
| 21,32–23,32 | junto com todo mundo e saí no final da tarde. | Markt lotado (IMG_4121) | — |
| 23,32–25,22 | Eu não contava que Bruges era igual um domingo de sol | Comparação: Bruges lotada em cima, o Porto da Barra sobe em "igual" com um **=** | `PDX_swish` −6 dB |
| 25,22–26,80 | duas horas no Porto da Barra de Salvador. | Porto da Barra lotado (foto) | — |
| 26,80–29,70 | Ela tá lá, linda. Mas você só vê gente. | Rozenhoedkaai: casas, depois barcos cheios (IMG_4128) | — |
| 29,70–31,72 | Só que Bruges é outra cidade | Canal vazio (IMG_4133) | Luz de passagem · `PDX_riser` −8 dB até o corte |
| 31,72–33,72 | quando a galera do bate e volta vai embora. | Parque vazio (IMG_4227) | — |
| 33,72–36,40 | Por isso eu vou te dar um conselho aqui. Olho no olho. | Diego em tela cheia, corte de zoom em "Olho" | — |
| 36,40–37,80 | Dorme uma noite lá. | Belfort à noite (foto) | Cinema: escurece e abre · `PDX_ar_longo` −6 dB |
| 37,80–38,88 | Você não vai se arrepender. | Markt à noite (foto) | — |
| 38,88–39,78 | De manhã cedo | Dijver de manhã (foto) | — |
| 39,78–41,66 | e à noite os canais são só seus. | Rozenhoedkaai na hora azul (foto) | — |
| 41,66–43,42 | O centro inteiro é patrimônio da humanidade. | Stadhuis à noite (foto) | — |
| 43,42–45,42 | A cidade cheira a chocolate. | Waffle com chocolate (IMG_4235) | — |
| 45,42–47,42 | Foi a cidade mais bonita que eu vi na Bélgica. | Minnewater com o castelinho (IMG_4218) | — |
| 47,42–49,50 | É literalmente a Europa que você imagina | Canal com a torre da Onze-Lieve-Vrouwekerk (IMG_4131) | — |
| 49,50–50,95 | antes de ir pra Europa. | Canal de manhã (foto) | — |
| 50,95–53,00 | Agora me diz aí, você colocaria | Diego em tela cheia | Clarão de volta · `PDX_impacto` −4 dB |
| 53,00–55,13 | Bruges no seu roteiro da Bélgica? | **Tela dividida:** o amanhecer do gancho, sem fitas, com a placa do DS "NO SEU ROTEIRO / BRUGES ?" | Chegada da placa · `PD_clack_v1` −6 dB |

## Pontos de atenção (franco)

1. **Duração de 55,1 s.** A referência pede 7–30 s, e o guia do formato aceita até ~45 s em Reel de história. Cada frase leva a história adiante e você gravou todas, então mantive. Se a retenção cair antes da metade, o próximo teste é uma versão sem o bloco "Eu não contava… Porto da Barra" (−7 s) ou sem "Por isso eu vou te dar um conselho aqui" (−1,5 s).
2. **Trem (19,3 s).** O clipe IMG_4244 é de 17/03, 08h32: provavelmente a ida de Bruxelas para Paris, não a chegada em Bruges. Ilustra "cheguei lá" como imagem de trem. Se isso incomodar, troco pelo Belfort.
3. **Fotos de terceiros.** As fotos CC BY e CC BY-SA exigem o crédito publicado. O bloco está em `legenda_post.md`; se tirar, a licença deixa de ser cumprida.
4. **Captura da Afar.** É matéria de 2019. A frase falada ("parou de fazer propaganda") é o que a matéria diz.

## Conferir no ouvido (o Claude não escuta áudio)

- [ ] O corte entre "humanidade." e "A cidade cheira a chocolate" (≈ 43,45 s): não pode sobrar sílaba de "você".
- [ ] Os efeitos `PDX_*` e o clack nos volumes da seção 4.1. Nenhum foi ouvido.
- [ ] As pausas entre as falas (0,24 a 0,38 s): naturais ou corridas?
- [ ] O fim (54,1–55,1 s): 1 s de silêncio com a placa na tela.

## Medições (vídeo final)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 55,1 s (acima do alvo de 45 s do formato; ver Pontos de atenção, 1) |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz 320 kb/s |
| 3 | Material gravado ≥ 2 s · nenhuma cena > 3 s | 27 cenas: a menor gravada tem 2,00 s; as fotos e grafismos ficam entre 0,90 e 1,90 s; a maior cena tem 2,92 s (captura) |
| 5 | Legendas | 65 grupos de 1 a 4 palavras, em uma linha (máx. 23 caracteres), centro x 540 |
| 6 | Imagem na palavra | Toda troca é ancorada no tempo da palavra (transcrição alinhada na voz final) |
| 9 | Áudio | −14,1 LUFS integrados, pico −1,0 dBTP (master em 4 passadas: o AAC sobe os picos depois do limitador) |
| 11 | Transcrição da voz final | Whisper large-v3 = fala gravada; o corte "humanidade. / A cidade" foi transcrito limpo |
| 12 | Nada na tela fora da fala | Gancho, números, 11H e placa vêm da fala. Exceções registradas: fitas "POLITIE · POLICE" (inscrição da fita real) e selo "CAPTURA REAL" |
| 13 | Créditos | `creditos.md` e bloco de crédito em `legenda_post.md` |

Arquivos: `reel_bruges-bate-volta_rev1.mp4` (master), `reel_bruges-bate-volta_rev1_previa.mp4` (540 px, leve), `capa_bruges-bate-volta_rev1.jpg` (quadro de 1,9 s, gancho completo) e `qa_frames/folha_1s.jpg`.
