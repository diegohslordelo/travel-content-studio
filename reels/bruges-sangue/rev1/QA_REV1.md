# QA · Reel "Basílica do Sangue Sagrado" (Bruges) · REV1

**Entrega:** `reel_bruges-sangue_rev1.mp4` · capa `capa_bruges-sangue_rev1.jpg` · legenda do post em `legenda_post.md` · créditos em `creditos.md`.
**Pedido do Diego (29/10/2026):** Reel em tela dividida, vlog de viagem com curiosidade histórica, seguindo o processo das referências; voz preservada sem corte de palavra; mistura de acervo, internet e animação; DS só na CTA final; melhor qualidade possível (o Instagram reduz).

**Veredito do Claude:** pronto para a escuta do Diego. Dois pontos de conteúdo precisam da decisão dele antes de postar (seção 6).

---

## 1. Fontes

| O quê | De onde |
|---|---|
| Voz e imagem do Diego | As 5 tomadas gravadas no quarto: Drive `Youtube/Bruges/Reels Igreja` (IMG_7349, 7371, 7373, 7405, 7407, 28/10/2026). Decisão do Diego: vídeos dele falando, só dessa pasta |
| Acervo (mudo) | Bruges, 16/03/2026: IMG_2490 (canal até o Rozenhoedkaai), IMG_2479 (fachada da basílica), IMG_2603 (vitrine de chocolate), IMG_2476 (Burg com a basílica), IMG_2486 (canal, CTA) |
| Internet | 11 imagens do Wikimedia Commons (`creditos.md`) |
| Criadas | Mapa da Bélgica, rota até Bruges, corte desenhado das duas capelas, "DESDE A IDADE MÉDIA", "PATRIMÔNIO CULTURAL IMATERIAL", círculo e "?" desenhados |
| Referências de edição | As 3 referências de tela dividida analisadas em `docs/referencias/analise_reels_referencia_2026-10-28.md` (o pedido citava referências "que vou fornecer"; nenhuma nova chegou, então valeram essas) |

## 2. Voz (decupagem)

As 5 tomadas entram **inteiras e em ordem**. Nenhum corte dentro da fala, nenhuma pausa interna removida, nenhuma aceleração. Só foram aparados o silêncio antes da 1ª palavra e depois da última de cada tomada, medidos pela energia da voz.

| Fala | Tomada | Trecho do bruto | No Reel | Fala gravada |
|---|---|---|---|---|
| f1 | IMG_7349 | 1,05 → 7,75 s | 0,00 → 6,70 | Você sabia que no meio de uma cidade que parece ter saído de um conto de fadas existe uma basílica que guarda o sangue de Jesus Cristo? |
| f2 | IMG_7371 | 1,12 → 10,35 s | 6,70 → 15,93 | Hoje estou falando da Basílica do Sangue Sagrado em Bruges, na Bélgica. Lá tem duas capelas, uma mais simples, que é em estilo romântico, e tem outra gótica, que é onde a relíquia é venerada. |
| f3 | IMG_7373 | 0,75 → 9,22 s | 15,93 → 24,40 | Segundo a tradição, essa relíquia teria chegado a Bruges depois das cruzadas, mas tem um ponto aí. Essa história é muito antiga, então sua origem não é comprovada com certeza. |
| f4 | IMG_7405 | 0,55 → 11,10 s | 24,40 → 34,93 | E essa tradição continua viva até hoje. Desde a Idade Média, a cidade celebra uma procissão em homenagem ao sangue sagrado, que inclusive foi reconhecida pela UNESCO como um patrimônio cultural imaterial da humanidade. |
| f5 | IMG_7407 | 0,38 → 10,00 s | 34,93 → 44,57 | É impressionante como a cidade que cheira a chocolate reúne arquitetura medieval, fé e histórias que atravessam séculos. Agora me diz aí, você colocaria Bruges no seu roteiro da Europa? |

- **Respiro entre tomadas:** 0,26 a 0,35 s (silêncio real de cada tomada), na faixa de 0,3–0,4 s entre blocos (FORMATOS_REELS 10.1).
- **Emendas medidas:** −45 a −74 dB nos 30 ms em volta de cada emenda (a fala típica está em −18 dBFS); salto de amostra ≤ 0,0001: sem clique.
- **Tempo de cada palavra:** Whisper large-v3 + alinhamento forçado (torchaudio MMS) em `transcricao_alinhada.json`.
- **Vídeo do Diego:** cortado nos mesmos trechos, em número inteiro de quadros (boca em sincronia).
- **Tratamento:** passa-alta 70 Hz, redução leve de ruído, níveis das tomadas igualados pela fala, ganho linear.

## 3. Decupagem visual (o que entra em cada frase)

| # | Tempo | Fala | Imagem | Fonte | Composição | Transição / som |
|---|---|---|---|---|---|---|
| 1 | 0,00–3,87 | Você sabia que no meio de uma cidade… conto de fadas | Canal até o Rozenhoedkaai; texto do gancho linha a linha ("CONTO DE FADAS" em âmbar) | Acervo IMG_2490 | Tela dividida (Diego desde o 1º quadro) | — |
| 2 | 3,87–6,70 | existe uma basílica que guarda o sangue de Jesus Cristo? | Fachada da basílica; o **frasco da relíquia** entra numa faixa na palavra "sangue" ("O SANGUE" em vermelho) | Acervo IMG_2479 + Commons | Tela dividida + cartão | Impacto em "sangue" |
| 3 | 6,70–9,17 | Hoje estou falando da Basílica do Sangue Sagrado | Diego; palavra-chave "BASÍLICA DO / *Sangue Sagrado*" em dupla tipografia | Gravação | **Empurrão** da tela dividida para o Diego em tela cheia (ref. 1) | Swish |
| 4 | 9,17–10,20 | em Bruges, na Bélgica | Mapa: Bélgica em âmbar, pino em Bruges, "BRUGES" e "BÉLGICA" na palavra | Criado (Natural Earth) | Tela dividida | — |
| 5 | 10,20–14,23 | Lá tem duas capelas, uma mais simples… outra gótica | Corte desenhado da basílica: o andar de baixo enche com a capela de baixo em "uma", o de cima com a capela gótica em "outra" | Criado + Commons | Animação em tela cheia | — |
| 6 | 14,23–17,47 | que é onde a relíquia é venerada. Segundo a tradição, essa relíquia | Relíquia sendo manuseada → **dissolve** para gravura antiga do relicário (selo GRAVURA ANTIGA) | Commons | Cartão sobre o Diego desfocado | Página no dissolve |
| 7 | 17,47–18,53 | teria chegado a Bruges | Rota desenhada da Terra Santa até Bruges | Criado | Animação em tela cheia | — |
| 8 | 18,53–19,63 | depois das cruzadas | Iluminura de Jean Fouquet (≈1455), selo REPRESENTAÇÃO ARTÍSTICA | Commons | Tela cheia | — |
| 9 | 19,63–22,10 | mas tem um ponto aí. Essa história é muito antiga | Diego; **corte de zoom** em "Essa história" (ref. 2) | Gravação | Tela cheia | **Clarão** de volta + impacto |
| 10 | 22,10–24,40 | então sua origem não é comprovada com certeza | Relicário; círculo desenhado e "?" em "comprovada" | Commons + desenho | Tela dividida | — |
| 11 | 24,40–26,50 | E essa tradição continua viva até hoje | Procissão atual | Commons | Tela cheia | **Luz de passagem** (pico no corte) + ar longo |
| 12 | 26,50–28,10 | Desde a Idade Média, a cidade celebra | "DESDE A / IDADE / MÉDIA" sobe na palavra | Criado | Animação em tela cheia | Impacto em "Idade" |
| 13 | 28,10–30,20 | uma procissão em homenagem ao sangue sagrado | Relicário carregado na procissão | Commons | Cartão | — |
| 14 | 30,20–32,20 | que inclusive foi reconhecida pela UNESCO | Procissão (figurantes de soldados romanos) | Commons | Tela dividida | — |
| 15 | 32,20–34,93 | como um patrimônio cultural imaterial da humanidade | "UNESCO" + "PATRIMÔNIO / CULTURAL / IMATERIAL / DA HUMANIDADE", cada linha na palavra | Criado | Animação em tela cheia | — |
| 16 | 34,93–37,43 | É impressionante como a cidade que cheira a chocolate | Vitrine de chocolate | Acervo IMG_2603 | Tela dividida | — |
| 17 | 37,43–39,53 | reúne arquitetura medieval, fé | Praça Burg com a basílica | Acervo IMG_2476 | Tela dividida | — |
| 18 | 39,53–41,33 | e histórias que atravessam séculos | Cartaz da procissão de 1913 (selo REGISTRO HISTÓRICO) | Commons | Cartão | — |
| 19 | 41,33–46,17 | Agora me diz aí, você colocaria Bruges no seu roteiro da Europa? | Volta ao canal (loop com a abertura) + **placa do DS V2** "ME DIZ AÍ / BRUGES ?" | Acervo IMG_2486 + DS | Tela cheia + CTA | *Clack* da placa |

**Equilíbrio:** 19 cenas; tela dividida 8, tela cheia (foto, plano ou animação) 7, cartão 3, Diego em tela cheia 2 (respiro na apresentação e na virada). Nenhuma sequência de 3 cenas da mesma composição. Média de 2,4 s por imagem.

**Transições (4 em 46 s, ≥ 1,5 s entre elas; o resto é corte seco):**
- **Empurrão** (6,70 s, 19 quadros): sai do gancho dividido para o Diego em tela cheia (referência 1, T1).
- **Dissolve da foto para a gravura** (16,1 s): "Segundo a tradição" volta no tempo dentro do mesmo cartão.
- **Clarão de volta** (19,63 s, 5 quadros): a virada "mas tem um ponto aí" volta ao rosto (referência 1, T6).
- **Luz de passagem** (24,40 s, 11 quadros, pico 85% por 4 quadros, corte escondido no mais claro): o passado vira presente, "continua viva até hoje" (referência 1, T2; intensidade da REFERENCIA_EDICAO_FORMATOS 10.4).

**Imagem que não engana:** a iluminura (selo REPRESENTAÇÃO ARTÍSTICA), a gravura (GRAVURA ANTIGA) e o cartaz de 1913 (REGISTRO HISTÓRICO) estão marcados. Mapas e corte das capelas são desenho em traço. As demais fotos são atuais.

## 4. Identidade visual

- **Do gancho até antes do CTA:** linguagem do formato tela dividida (FORMATOS_REELS): Anton, Inter 800, destaque âmbar `#E0AE5C`, grão 6%, fundo `#14120F`. Nenhum componente, cor ou som `PD_*` do DS.
- **Acréscimos deste Reel** (não são regra do formato): serifa itálica Cormorant Garamond na 2ª linha da palavra-chave (dupla tipografia da referência 1, com ar medieval) e vermelho `#C8352E` só em "O SANGUE" no gancho.
- **CTA:** placa do DS V2 (verbo "ME DIZ AÍ" + destino "BRUGES" + módulo de interrogação), posição fixa do DS, Chegada e *clack* (−6 dB da voz, volume de trabalho da REFERENCIA_EDICAO_FORMATOS 4.1). Texto tirado da fala.

## 5. Medições

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 46,17 s (voz 44,57 s + 1,6 s de cauda do CTA). Passa da meta de 45 s do formato porque nenhuma frase foi cortada (pedido do Diego) |
| 2 | Formato | 1080 × 1920, 9:16, 30 qps, H.264 High (CRF 10, ≈ 29 Mb/s), AAC 320 kb/s 48 kHz, BT.709. 167 MB, sem redução: o Instagram recomprime |
| 3 | Material do Diego ≥ 2 s | Planos do acervo 2,1–4,8 s; Diego em tela cheia 2,47 s (2×). Nenhum take esticado (nada em câmera lenta) |
| 4 | Takes dentro do corte real | Os 5 planos do acervo não têm corte de cena (medido) e cada trecho cabe no plano |
| 5 | Legendas | 1 linha, 1–4 palavras, centradas em x 540, largura máxima 791 px (limite 808 px: x 136–944), medida com a métrica da Inter 800 |
| 6 | Imagem na palavra | Cortes medidos no vídeo final = cortes planejados (Δ 0,00 s); cada cena começa 0,08 s antes da palavra |
| 7 | Pessoas nas imagens | Nenhuma imagem de apoio com o Diego ou a Marina. Há desconhecidos (barco no canal, procissão, praça) |
| 9 | Áudio | −14,0 LUFS integrados, pico verdadeiro −1,5 dBTP, 0 amostras acima de −1 dBFS, 0 em 0 dBFS |
| 10 | Emendas | No silêncio, sem clique (seção 2) |
| 11 | Transcrição da voz final | Bate com a fala gravada. O Whisper ouviu "Eu estou" no lugar de "Hoje estou", "os séculos" e "cultural e material" (ver seção 6) |
| 12 | Texto na tela | Só palavras da fala, mais os 3 selos que diferenciam imagem histórica e artística (pedido do Diego nesta revisão) |
| 13 | Créditos | `creditos.md` |

Folhas: `qa_frames/folha_1s.jpg` (1 quadro por segundo) e `qa_frames/transicao_*.jpg` (quadro a quadro em cada transição).

**Efeitos sonoros** (kit `PDX_*`, CC0, volumes da REFERENCIA_EDICAO_FORMATOS 4.1): impacto em "sangue" (5,46 s), swish no empurrão (7,00 s), página no dissolve (16,17 s), impacto no clarão (19,64 s), ar longo na luz (24,40 s), impacto em "Idade Média" (26,82 s), *clack* do CTA. Um a cada ≥ 1,5 s.

## 6. Decisões do Diego antes de postar

1. **"estilo romântico" (f2, 12,55 s).** A capela de baixo é em estilo **românico** (séc. XII). "Romântico" é outro estilo (séc. XIX) e é um erro de fato. A legenda segue a fala gravada (regra do formato, 9.5) e mostra "romântico". Opções: (a) **regravar só a frase** "Lá tem duas capelas, uma mais simples, que é em estilo românico, e tem outra gótica, que é onde a relíquia é venerada." (troca 1 tomada, o resto fica igual) — **recomendado**; (b) manter a voz e escrever "românico" na legenda; (c) manter como está.
2. **"cultural imaterial" (f4, 33,6 s).** O Whisper ouve "cultural e material"; a legenda e a animação escrevem **IMATERIAL**, que é o título certo da lista da UNESCO. Confira no ouvido se a fala soa como "imaterial".

## 7. Conferir no ouvido (o Claude não escuta)

- "**Hoje** estou falando" (6,9 s): o Whisper ouviu "Eu estou". O corte começa 0,18 s antes da palavra, então nada foi cortado; confira se o "Hoje" está claro.
- "com **certeza**" (24,1 s): a palavra termina a 0,02 s do fim da trilha do iPhone (o áudio do .MOV acaba antes do vídeo). Foi feito só um fade de 25 ms no fim, sem restauro. Confira se o "-za" está inteiro.
- "atravessam séculos" (40,3 s): o Whisper ouviu "atravessam **os** séculos"; a legenda segue o alinhamento ("atravessam séculos").
- Volume dos 6 efeitos e do *clack* (sintetizados/CC0, ninguém ouviu).

## 8. Fatos externos conferidos (29/10/2026)

- Capela de baixo românica (São Basílio) e de cima gótica, onde fica a relíquia; a chegada da relíquia na 2ª Cruzada (Thierry da Alsácia) é **tradição**, sem comprovação: [Wikipedia, Basilica of the Holy Blood](https://en.wikipedia.org/wiki/Basilica_of_the_Holy_Blood).
- Procissão do Sangue Sagrado inscrita em 2009 na Lista Representativa do Patrimônio Cultural Imaterial da Humanidade: [UNESCO](https://ich.unesco.org/en/RL/procession-of-the-holy-blood-in-bruges-00263). A procissão é citada desde pelo menos 1304 ("desde a Idade Média" está correto): [VRT](https://www.vrt.be/vrtnws/en/2023/05/19/40-000-spectators-watch-holy-blood-procession-in-bruges).

## 9. Como refazer

De dentro de `reels/bruges-sangue/rev1`, com os brutos em `../fonte/` (fora do git): `PY=<python com numpy, soundfile, scipy, pillow, fonttools> bash scripts/render.sh`. A composição é `design-system/remotion/src/bruges/`. Decisões editáveis sem mexer no código: `edicao.json` (voz) e `cenas.json` (cenas, gancho, legendas, sons, CTA). Alinhamento: `scripts/alinhar.py` (torchaudio).
