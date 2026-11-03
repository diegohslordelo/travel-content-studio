# QA · Reel "Primeiro dia em Amsterdam" · REV1 (03/11/2026)

**Veredito: pronto para a escuta do Diego.** Tudo o que dá para medir passou (formato, loudness, tremor, tempo das cenas, legendas na zona segura). Faltam a escuta humana dos sons e de 6 palavras, e 2 decisões sobre valores (fim deste documento).

**Pedido do Diego (02/11/2026):** Reel do primeiro dia em Amsterdam em **tela verde**, com ele no **canto inferior direito**, gravado no quarto (Drive, `Amsterdam/Reel primeiro dia`). Atrás dele, a jornada do dia 1 na ordem da narração, com as melhores cenas, **sem imagem tremida e sem câmera lenta**; pode usar o material do vlog. Só o CTA do **YouTube** (o de seguir, IMG_7632, foi descartado). **Placar igual ao do vlog** (hora de cada ponto e gasto). Efeitos que agreguem valor, decupado e fluido, sem comer palavra. Pedido de 03/11/2026, durante a edição: a Tony's mostra a loja **por dentro**.

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_amsterdam-primeiro-dia_rev1.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **60,57 s** |
| `reel_amsterdam-primeiro-dia_rev1_previa.mp4` | Prévia leve (540 × 960) |
| `capa_amsterdam-primeiro-dia_rev1.jpg` | Capa: o quadro do gancho completo ("ISSO É TUDO… AMSTERDÃ") sobre a grade do dia |
| `qa_frames/cenas.jpg` · `qa_frames/um_por_segundo.jpg` | Um quadro por cena · um quadro por segundo |
| `../legenda_post.md` | Legendas do Instagram, TikTok e Shorts |

## Estrutura e formato

- **Formato:** Tela verde (Trello; `docs/FORMATOS_TRELLO.md`), variação "apresentador no canto inferior" (referências 5 e 6, `docs/REFERENCIA_EDICAO_FORMATOS.md`, 10.2). Recorte sem fundo verde, por IA (RobustVideoMatting ResNet50, `scripts/recorte.py`), como nas greves.
- **Estrutura:** AIDA, como no roteiro do Diego. Atenção = "Isso é tudo o que fizemos…" com a grade do dia; Interesse = as paradas na ordem real; Desejo = o Placar fechando em € 90,84 e o McDonald's como "ponto turístico mais importante"; Ação = o vídeo completo no YouTube.
- **Ideia central:** tudo o que coube no primeiro dia em Amsterdam e quanto custou.

## Tela

| Item | Valor |
|---|---|
| Diego | Recorte 720 × 1280 mostrado em 560 × 996 em **x 540 · y 924** (canto inferior direito, rosto ≈ y 1390, à esquerda da coluna de botões do Instagram); tamanho fixo, sem zoom; sombra leve para separar do fundo |
| Fundo | Vídeos da viagem em tela cheia (planos horizontais recortados em 9:16; os verticais entram inteiros), mudos, HLG → SDR, grade do formato, aproximação lenta e linear |
| Legenda | Linguagem do formato (Inter 800 66 px, destaque âmbar, 1 a 4 palavras), centrada em **x 540**, **y 1075** (acima da cabeça do Diego). Maior grupo: ver Medido |
| Gancho | Anton, x 72, linha a linha na palavra: "ISSO É / **TUDO** / O QUE FIZEMOS NO NOSSO / PRIMEIRO DIA EM / **AMSTERDÃ**", sobre a **grade do dia** (9 vídeos que entram um a um em "tudo") |
| Placar do Dia (DS V2, 2.5) | x 72 · y 256, liga em "pousou" e fica até o fim. Hora de cada ponto + gasto acumulado do dia, **com os valores do Placar do vlog** |
| CTA | Grade do dia de novo (os dois ao longo do dia), escurecida; **placa do DS V2** "ASSISTA NO / YOUTUBE →" com Chegada em "YouTube" e *clack*. O Placar fica com o total, € 90,84 |
| Grão | 6% (formato) |

**Exceção deste Reel (não é regra geral):** o DS V2 aparece **antes do CTA** só no Placar, por pedido explícito do Diego ("o mesmo placar que aparece no vídeo do YouTube"). A regra "DS só no CTA" (CLAUDE.md, 6) não muda.

## Cenas (21 + gancho + CTA)

| # | Tempo (s) | Dur. | Fala | Imagem (acervo, hora do arquivo) | Tremor p90 |
|---|---|---|---|---|---|
| — | 0,00–2,93 | 2,93 | Isso é tudo o que fizemos no nosso primeiro dia em Amsterdã. | Grade do dia (9 planos) → **mergulho** no 1º quadro (aeroporto) | ≤ 0,84 |
| 1 | 2,93–4,83 | 1,90* | A gente pousou às duas e meia e pegamos um ônibus a | Selfie no aeroporto (IMG_1375, 14:30), estabilizada | 1,11 |
| 2 | 4,83–6,87 | 2,03 | caminho do hotel. A gente já estava morrendo de | Janela do ônibus (IMG_1381) | 0,24 |
| 3 | 6,87–9,43 | 2,57 | fome, então deixamos as coisas no hotel e fomos procurar algo para comer. | Quarto do hotel (IMG_1390, 15:20) → **chicote** | 0,61 |
| 4 | 9,43–11,93 | 2,50 | Só que no caminho a gente passou pelas Dancing Houses | Dancing Houses, vertical (IMG_1403-1, 16:27) | 0,28 |
| 5 | 11,93–14,20 | 2,27 | e a Praça Dam, que é a praça onde tem o Palácio Real, | Palácio Real (IMG_1421, 17:09) | 0,05 |
| 6 | 14,20–16,63 | 2,43 | o Museu Madame Tussauds e o Monumento Nacional. | Prédio do Madame Tussauds → panorâmica até o Monumento (IMG_1432) | 0,52 |
| 7 | 16,63–19,57 | 2,93 | Pra forrar a barriga a gente encontrou logo uma das batatas mais famosas da cidade, | Marina comendo a batata, vertical (IMG_1449-1, 17:36) | 0,83 |
| 8 | 19,57–21,63 | 2,07 | que é a Manneken Pis. E de lá, nós fomos para a | Letreiro da Manneken Pis (IMG_1444) → **chicote** | 0,10 |
| 9 | 21,63–23,87 | 2,23 | loja de chocolate mais famosa da cidade, a Tony's, | **Dentro da Tony's** (IMG_1456, 13,0 s: sala vermelha → corredor das barras) | 0,73 |
| 10 | 23,87–26,53 | 2,67 | e na minha opinião, a melhor chocolate do mundo. De lá, nós vamos dar um passeio | Barras de chocolate (IMG_1462) | 0,40 |
| 11 | 26,53–28,90 | 2,37 | na Kalverstraat, que é uma rua cheia de lojas. | Kalverstraat ao anoitecer (IMG_1464, 18:29) · **luz de passagem** dia → noite | 0,61 |
| 12 | 28,90–31,27 | 2,37 | Mas a gente só estava a passeio e acabou não comprando nada | Lojas da rua (IMG_1472) | 0,10 |
| 13 | 31,27–33,80 | 2,53 | E lá bem pertinho nós fomos comer o biscoito mais famoso de Amsterdã, | Fachada da Hans Egstorf (IMG_1477) | 0,12 |
| 14 | 33,80–36,10 | 2,30 | o Stroopwafel, que é um biscoito recheado com caramelo | Vitrine de stroopwafels, vertical (IMG_1476-1), com zoom no topo | 0,41 |
| 15 | 36,10–38,27 | 2,17 | nessa Hans Egstorf. A gente pegou esse | Balcão, a atendente montando (IMG_1480) | 0,59 |
| 16 | 38,27–40,33 | 2,07 | com top de chocolate e estava muito bom. | Marina com o stroopwafel (IMG_1479) | 0,17 |
| 17 | 40,33–42,53 | 2,20 | Depois paramos no barzinho pra eu ser batizado com a minha prim- | Praça à noite (IMG_1491) | 0,26 |
| 18 | 42,53–44,73 | 2,20 | -eira cerveja de Amsterdã e Marina pegou um vinho | A cerveja na mesa e a taça de vinho atrás (IMG_1497) → **fusão** | 0,06 |
| 19 | 44,73–47,77 | 3,03 | E depois nós vamos dar uma volta na famosa Red Light Street. | Selfie dos dois com o neon vermelho atrás (IMG_1519, 20:57) | 0,80 |
| 20 | 47,77–51,27 | 3,50* | E por último, nós fechamos o nosso passeio no ponto turístico mais importante da cidade, | Canal à noite (IMG_1523), aproximação lenta até 108% (suspense) | 0,79 |
| 21 | 51,27–53,50 | 2,23 | o McDonald's de Amsterdã. Esse foi só o primeiro dos | McDonald's (IMG_1527, 21:21) | 0,36 |
| CTA | 53,50–60,57 | 7,07 | três dias… é só clicar no link da bio e assistir. | Grade do dia (os dois ao longo do dia) + placa do YouTube | ≤ 1,32 |

\* **Fora dos 2–3 s, de propósito:** o aeroporto fica 1,90 s em tela cheia, mas o mesmo plano já aparece desde 2,5 s no mergulho da grade (≈ 2,4 s no total). O canal fica 3,5 s para segurar o suspense até o McDonald's.

**Tremor** (`scripts/reel.py tremor`): aceleração do movimento quadro a quadro, medida no bruto na taxa original (24 qps), no recorte usado. Panorâmica suave dá aceleração baixa; mão tremendo, alta. Todos os trechos ficaram em **p90 ≤ 1,32** (limite usado: 1,5). Trocados por tremerem: o ônibus (IMG_1378 → IMG_1381), o trecho do aeroporto (IMG_1375 de 0,3 s → 11,5 s) e dois quadros da grade do CTA. As 3 selfies na mão que restaram (aeroporto e 2 quadros das grades) foram **estabilizadas** (vidstab, aproximação fixa de 6%), sem mudar a velocidade. Nenhum plano está em câmera lenta.

## Placar (valores do Placar do vlog, REV3)

| Entra em | Hora | Gasto acumulado | Som |
|---|---|---|---|
| "pousou" | 14:30 | € 0,00 | — (ligar não tem som) |
| "ônibus" | 14:38 | € 13,00 | moeda |
| "hotel" | 15:20 | € 13,00 | tick |
| "Dancing Houses" | 16:30 | € 13,00 | (mudo: a 1,5 s do chicote) |
| "Praça Dam" | 17:10 | € 24,99 | moeda (inclui a pizza, ver pendência 2) |
| "Manneken Pis" | 17:36 | € 32,14 | moeda |
| "Tony's" | 17:41 | € 52,14 | moeda |
| "Kalverstraat" | 18:29 | € 52,14 | (mudo: a 0,2 s da luz de passagem) |
| "Hans Egstorf" | 18:49 | € 61,64 | moeda |
| "barzinho" | 19:29 | € 78,24 | moeda |
| "Red Light" | 20:55 | € 78,24 | tick |
| "McDonald's" | 21:21 | **€ 90,84** | moeda |

Horas: as do vlog (etiquetas e Placar). 14:30 é a hora do arquivo IMG_1375 no aeroporto; o Diego diz "duas e meia".

## Transições (5, o resto em corte seco)

| Onde | Transição | Por quê |
|---|---|---|
| Gancho → aeroporto | **Mergulho na grade**: a câmera entra no 1º quadro (o aeroporto), que vira a tela | "Isso é tudo" → a viagem começa de dentro do resumo do dia. O `keen` tem o pico no corte |
| Hotel → Dancing Houses | **Chicote** (`PDX_swish`) | Sair do hotel para a rua |
| Manneken Pis → Tony's | **Chicote** (`PDX_woosh`) | "E de lá, nós fomos…": deslocamento |
| Tony's → Kalverstraat | **Luz de passagem** (`PDX_ar_longo`) | O dia vira noite (17:41 → 18:29) |
| Bar → Red Light | **Fusão** de 9 quadros (`PDX_ar_longo`) | Noite → noite, mesma caminhada |

≥ 1,5 s entre transições; nenhuma de catálogo proibida.

## Som

Voz: passa-alta 70 Hz, redução leve de ruído, níveis igualados por tomada; **nunca acelerada**. Efeitos (`_tmp/sons.json`, volumes de `docs/REFERENCIA_EDICAO_FORMATOS.md`, 4.1), no máximo 1 a cada 1,5 s:

| s | Som | dB da voz | Para quê |
|---|---|---|---|
| 0,38 | `PDX_punch_seco` | −4 | "TUDO": a grade do dia fecha |
| 2,92 | `keen` (pico no corte) | −6 | Fim do gancho (regra do Diego de 01/11/2026) |
| 9,43 / 21,64 | `PDX_swish` / `PDX_woosh` | −6 | Chicotes |
| 18,07 | `PDX_magic_brilho` | −6 | "uma das batatas mais famosas" |
| 26,52 | `PDX_ar_longo` | −6 | Luz de passagem |
| 30,72 | `PDX_punch_seco` | −8 | "não comprando **nada**" (batida de humor) |
| 33,80 | `PDX_magic_reveal` | −8 | A vitrine dos stroopwafels |
| 44,72 | `PDX_ar_longo` | −8 | Fusão para a Red Light |
| 51,27 | `PDX_riser` (termina no corte) | −8 | "o ponto turístico mais importante…" → McDonald's |
| 53,49 | `PDX_woosh` | −6 | A grade volta (CTA) |
| Placar | `PD_moeda` −8 · `PD_tick` −14 | | Como no vlog |
| CTA | `PD_clack` | −6 | Placa do YouTube |

Sem trilha: a música entra pelo app do Instagram, em volume baixo.

## Decupagem

13 trechos das 12 tomadas (`edicao.json`). Cortes no silêncio medido (energia 120–4.000 Hz). Só uma pausa interna cortada: 0,33 s entre "Praça Dam," e "que é a praça" (IMG_7606). Entre tomadas ficaram ≈ 0,12 s. **Nenhuma palavra cortada**: a transcrição da voz final tem todas as frases, na ordem.

## Medido no vídeo final (`scripts/conferir.py`)

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, 60,57 s ✅ |
| Áudio | **−14,0 LUFS**, pico **−1,3 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS ✅ |
| Legendas | 88 grupos de 1 linha; o maior cabe em 808 px (x 136–944) depois de dividir "e o Monumento / Nacional." ✅ |
| Tremor | Todos os trechos com p90 ≤ 1,32 ✅ |
| Velocidade | Nenhum trecho esticado ou acelerado ✅ |
| Diego no fim | A tomada do CTA acaba 0,47 s antes do fim do Reel: o último quadro do Diego fica parado sob a placa (a fala não é esticada) |

## Fala gravada × roteiro

A legenda segue a fala. Diferenças em relação ao roteiro: abre com "Isso é tudo o que fizemos no nosso primeiro dia em Amsterdã" (o roteiro listava batata, chocolate, cerveja e McDonald's); acrescenta ônibus, Monumento Nacional, "a melhor chocolate do mundo", "não comprando nada" e o McDonald's como "ponto turístico mais importante". Fica de fora (fora do pedido): IMG_7632, o CTA de seguir.

## Conferir no ouvido

1. **Volumes dos efeitos** e o `keen`: ninguém ouviu os `PDX_*`, o `keen` nem os `PD_*_v1` pelo repositório.
2. Palavras que as duas transcrições (tomada × voz final) ouviram diferente, todas com confiança baixa. A legenda usa a 1ª coluna:

| s | Legenda | A voz final ouviu |
|---|---|---|
| 4,4 | pegamos **um** ônibus | pegamos **o** ônibus |
| 5,9 / 29,4 / 39,5 | **estava** | **tava** |
| 26,0 / 45,4 | nós **vamos** dar | nós **fomos** dar |
| 41,4 | pra **eu** ser batizado | pra ser batizado |
| 46,6 | **Red Light** Street | "Headlight" Street (as duas) |
| 24,5 | a melhor chocolate | (igual) |

Se alguma estiver errada, me diga qual: troco só o texto da legenda.

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** o Placar do vlog soma **€ 7,15** e o Recibo do vlog diz **€ 7,50**. Usei € 7,15 (fecha o total de € 90,84). Se o certo for € 7,50, o total vira € 91,19 aqui e no vlog.
2. **Pizza (16:48, € 11,99):** não é citada na fala, mas entra no gasto da Praça Dam (17:10), para o Placar bater com o vlog e com o total. A legenda do post explica. Alternativa: tirar a pizza e fechar em € 78,85 (aí o total diverge do vlog).
3. **Duração de 60,6 s:** acima dos 7–30 s da referência de conteúdo (3.1). Mantive todas as falas (pedido do Diego). Se a retenção cair antes da metade, a versão curta tira os blocos 6 (Kalverstraat) e 9 (Red Light), ≈ 9 s.
4. **Sons e regra do `keen`:** o kit "SFX virais" (branch `claude/sons-sfx-virais`) e o `keen` (branch `claude/reel-bruxelas-grand-place`) foram trazidos para este branch; a regra do `keen` no CLAUDE.md está só no branch da Grand-Place.
