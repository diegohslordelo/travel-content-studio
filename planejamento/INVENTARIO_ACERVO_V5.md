# Inventário do acervo e mapa de uso · v5

**Data:** 14/10/2026 · **Entregas B e D da revisão v5** (`REVISAO_V5.md`) · **Complementa:** `INVENTARIO_ACERVO.md` (09/10: master de Barcelona, transcrição, fotos de Roma no repositório) e o inventário do Drive por miniatura de 11/10 (`INVENTARIO_DRIVE.md`, branch `claude/adoring-hamilton-omilgr`, commit `18064d5`, ainda não está neste branch).

**Regra deste documento:** "analisado" quer dizer que o arquivo foi baixado e que vi os quadros, os metadados e a transcrição automática. "Listado" quer dizer que conheço o nome, o tamanho e a data de envio, mas não o conteúdo. Nenhum material bruto foi alterado, movido ou renomeado (CLAUDE.md, 10).

## 1. Acesso e limites

| Item | Situação |
|---|---|
| Acesso ao Google Drive | **Sim**, pelo conector do Drive, conta do Diego |
| Listagem | Completa para Amsterdam, Bruxelas, Bruges, Paris, Disney, Madrid, Lisboa, Itália (Roma, Florença, Veneza, Milão) e `Barcelona/Youtube`. **Parcial** para a pasta Barcelona (≈ 100 arquivos listados nesta sessão; o inventário de 11/10 conta 357) |
| Download | Só arquivos de **até 10 MB**. Um arquivo de ≈ 9 MB derrubou a conexão; por isso, só baixei arquivos de até ≈ 6,2 MB |
| O que cabe no limite | 397 dos 1.851 vídeos das pastas de cidade (21%). Quase todos têm de 0,2 a 3 s. As exceções são as cópias MP4 de Amsterdam (720p, de 5 a 12 s) |
| Vídeo longo inteiro | **Nenhum** foi visto. O master de Barcelona está analisado no repositório (09/10) |
| Áudio | Transcrição automática (faster-whisper "small", pt). **Não houve escuta humana.** Falas citadas devem ser conferidas antes do corte |
| Hora dos arquivos | É a data de criação gravada no arquivo (`creationdate` do iPhone). Nas cópias MP4 de Amsterdam, a hora **não confere** com a cena (bar à noite marcado às 07h26) e não deve ser usada |

**Para destravar a decupagem completa:** subir cópias leves (720p, até 10 MB) numa pasta `leve/` em cada cidade ou liberar outro meio de acesso (pendência k 50 no painel).

## 2. O que tem em cada pasta (listagem de 14/10)

| Pasta | Arquivos | Tamanho | Até 10 MB | Datas de gravação (arquivos analisados) | Situação |
|---|---:|---:|---:|---|---|
| Amsterdam | 571 (444 .MOV + 127 .MP4; 117 pares MOV + MP4 do mesmo plano) | 18,8 GB | 194 | 13 e 14/03/2026 (prováveis) | Decupada por miniatura (11/10) + 13 cópias MP4 analisadas |
| Madrid | 361 | 13,6 GB | 48 | 19 a 22/03/2026 | **Analisada por inteiro pelo Colab (361 de 361, 14/10)**: ver `DECUPAGEM_MADRID.md` |
| Disney | 244 | 7,6 GB | 40 | 18/03/2026 | **Analisada por inteiro pelo Colab** (`DECUPAGEM_DISNEY_PARIS.md`) |
| Paris | 237 | 7,8 GB | 38 | 17/03/2026 | **Analisada por inteiro pelo Colab** (`DECUPAGEM_DISNEY_PARIS.md`) |
| Bruges | 154 | 5,6 GB | 29 | 16/03/2026 | Decupada por miniatura (11/10) + 3 analisados |
| Lisboa | 146 | 5,6 GB | 12 | 23/03/2026 | Enviada em 14/10 · 2 clipes analisados |
| Bruxelas | 134 | 5,0 GB | 34 | 15/03/2026 | Decupada por miniatura (11/10) + 3 analisados |
| Barcelona | 357 (segundo o inventário de 11/10) | — | — | 09 a 11/03/2026 | Master e transcrição no repositório (09/10) |
| Barcelona › Youtube | 4 (master `Barcelona_3dias`, 10,1 GB; `copy_71526AEF…mov`, 7,5 GB; 1 foto HEIC; 1 JPG) | 17,7 GB | 2 | — | Listada |
| Itália › Roma | 12 fotos (10 HEIC + 2 JPG: IMG_5064 a IMG_6653) + subpasta `Postagem` (17 JPG, `01.jpg` a `17.jpg`) | 0,05 GB | todas | 25 a 27/12/2024 (EXIF, fotos do repositório) | As fotos já estão no repositório e no carrossel de Roma |
| Itália › Florença, Veneza, Milão | **0** | — | — | — | Pastas criadas em 14/10, **vazias** |
| Raiz do Drive | Planilhas de custo ("Custos de Viagens - Europa", "California", "Disney2027") e outros arquivos pessoais | — | — | — | Só as planilhas de custo interessam, e ficam para `OPORTUNIDADES_CUSTOS.md` |

**Total nas pastas de cidade:** 1.851 vídeos, ≈ 81,7 GB (sem contar Barcelona).

**Ordem da viagem pela numeração:** Barcelona (IMG_0487–1341) → Amsterdam (1369–2096) → Bruxelas (2096–2411) → Bruges (2411–2705) → Paris (2731–3194) → Disney (3200–3610) → Madrid (3617–4228) → Lisboa (4233–4526).

## 3. Duplicatas e arquivos fora do lugar

| Caso | Arquivos | O que fazer |
|---|---|---|
| Mesmo arquivo (nome e tamanho iguais) em duas pastas | IMG_2096, IMG_2142, IMG_2143, IMG_2144, IMG_2145, IMG_2167 e `copy_0032E90A…mov` (543 MB) em **Amsterdam e Bruxelas** · IMG_2411 em **Bruxelas e Bruges** | Pela numeração, IMG_2142–2167 são de Bruxelas (o Atomium é o IMG_2170). Usar a cópia da pasta Bruxelas. Não apagar nada sem o Diego |
| Cópias MP4 dos .MOV | 117 pares em Amsterdam (ex.: IMG_1384.MOV e IMG_1384.MP4) | Editar com o .MOV (original, 4K HDR). O .MP4 é 720p |
| Sufixos "-1" e "(2)" | Vários em Amsterdam e Barcelona (ex.: IMG_0707, IMG_0707-1, "IMG_0707 (3)") | Tamanhos diferentes: podem ser cortes ou exportações. Conferir antes de usar |
| Arquivo de outra cidade | IMG_2730 (selfie de Paris, já usada na apresentação) está na pasta **Bruges** | Usar como Paris |
| Registro sem pasta identificada | Um segundo IMG_3102.MOV (sem tamanho na listagem), além do de Paris | Usar o de Paris |

## 4. Clipes analisados (55) e onde cada um é usado (mapa de uso)

Quadros em 3 ou 4 pontos do clipe (25%, 50% e 75%, ou equivalente), metadados e transcrição. "Uso": peças futuras do painel que citam o arquivo ou a faixa dele.

### Paris (17/03/2026)

| Arquivo | Hora | Duração e formato | O que mostra | Fala (automática) | Uso |
|---|---|---|---|---|---|
| IMG_2808 | 12:24 | 0,96 s · 4K horizontal | Colunata (Madeleine ou similar), céu azul | — | p234 (12h24, colunata) |
| IMG_2842 | 12:45 | 0,96 s · 4K horizontal | Selfie do Diego de óculos escuros, avenida com árvores | — | p234 (12h45, selfie) |
| IMG_3035 | 14:50 | 0,67 s · 4K horizontal | Interior de galeria ou estação com teto de vidro | — | não usado |
| IMG_3069 | 16:08 | 1,04 s · 4K vertical | Cardápio impresso em francês | — | não usado (tem preços: fora desta revisão) |
| IMG_3102 | 17:22 | 0,29 s · 4K horizontal | **Fachada da Notre-Dame** | — | p614 (24/01) |
| IMG_3138 | 18:56 | 0,5 s · 4K vertical | Selfie de lado, desfocada | — | não usado (inutilizável) |

### Disney (18/03/2026)

| Arquivo | Hora | Duração | O que mostra | Fala | Uso |
|---|---|---|---|---|---|
| IMG_3216 | 10:00 | 1,7 s · 4K horiz. | Entrada do Disney Village com a escultura de vidro | — | p215, p624 |
| IMG_3229 | 10:50 | 0,9 s · vert. | Main Street com personagens | "É uma razão brisinha" (confusa) | p624 |
| IMG_3243, 3244 | 11:05 | 0,5 e 0,8 s · horiz. | Fila ou brinquedo coberto, os dois | — | p624 |
| IMG_3252 | 11:12 | 1,5 s · horiz. | Câmera virada para a roupa (sem uso visual) | — | p624 (faixa; trocar o plano) |
| IMG_3288 | 12:36 | 1,0 s · vert. | Personagem de vestido amarelo (Bela) | — | p624 |
| IMG_3357 | 14:34 | 1,4 s · horiz. | Selfie girada, céu | "Como o bicho tem cabelo?" | p608, p624 |
| IMG_3359, 3360 | 14:35 | 0,9 e 1,1 s · vert. | **Selfie dos dois com o castelo de dia** | — | p608, p215, p624 |
| IMG_3447 | 16:57 | 0,25 s · horiz. | Interior escuro de brinquedo | — | p624 |
| IMG_3517 | 18:00 | 1,0 s · horiz. | Área temática com árvores secas | — | p624 |
| IMG_3538 | 19:11 | 1,0 s · vert. | **Selfie dos dois com o castelo rosa ao pôr do sol** | — | p608, p215, p624 |
| IMG_3571 | 19:25 | 0,5 s · vert. | Chão e a mão (sem uso visual) | — | p608 (faixa), p624 |

### Madrid (19 a 21/03/2026)

| Arquivo | Hora | Duração | O que mostra | Fala | Uso |
|---|---|---|---|---|---|
| IMG_3689 | 19/03 16:35 | 0,9 s · horiz. | Os dois numa praça com árvores | — | p622 |
| IMG_3697 | 19/03 16:43 | 1,0 s · horiz. | Estátua e fachada (Palácio Real, a confirmar) | — | p622 |
| IMG_3793 | 19/03 20:47 | 2,0 s · horiz. | Prato de cogumelos ou frango | "Escrou que é isso, né?" (confusa) | p612, p622 |
| IMG_3796 | 19/03 20:47 | 2,0 s · horiz. | Prato de batatas | "É porque é tudo creme." | p612 |
| 97B4D6E2….mp4 | 20/03 12:39 | 2,7 s · 1080 × 1920 | Rua de pedestres molhada, Marina de costas | — | não usado |
| IMG_3877 | 20/03 12:06 | 1,0 s · horiz. | Escada e portão, câmera inclinada | "Eu não sei o que dizer." | não usado |
| IMG_3882 | 20/03 12:14 | 1,3 s · horiz. | **Puerta de Alcalá** | — | p606, p622 |
| IMG_3909 | 20/03 12:46 | 1,7 s · horiz. | **Lago do Retiro e o monumento a Alfonso XII**, dia nublado | — | p606, p622 |
| IMG_3912 | 20/03 12:47 | 1,0 s · vert. | O mesmo lago, vertical | — | p606, p622 |
| FD2CF314….mp4 | 20/03 19:48 | 5,9 s · 1080 × 1920 | **Show ao ar livre, palco com luz roxa e multidão** | — (música) | p607, p622 |
| IMG_3965 | 20/03 20:47 | 0,5 s · vert. | O mesmo show, luz roxa | — | p607, p622 |
| IMG_3976 | 20/03 21:25 | 0,9 s · horiz. | Hambúrguer no prato | — | p622 |
| IMG_3980 | 20/03 21:26 | 1,0 s · horiz. | Marina comendo, reação | "Seu." | não usado (candidato a reação) |
| IMG_3990 | 21/03 10:00 | 1,3 s · horiz. | **Fachada metálica do Santiago Bernabéu** | — | p605, p622 |
| IMG_4142 | 21/03 14:11 | 2,6 s · horiz. | Sobremesa no prato | — | p622 |
| IMG_4196 | 21/03 21:29 | 0,2 s · horiz. | Lanche e bebida (curto demais) | — | não usado |

### Lisboa (23/03/2026)

| Arquivo | Hora | Duração | O que mostra | Fala | Uso |
|---|---|---|---|---|---|
| IMG_4479 | 10:30 | 1,0 s · horiz. | Prédios claros e céu azul | — | p609, p274 |
| IMG_4503 | 11:12 | 1,4 s · horiz. | **Violoncelista tocando na rua** | — (música) | p609 |

### Amsterdam (cópias MP4 720p · data provável 13/03/2026; hora não confiável)

| Arquivo | Duração | O que mostra | Fala (automática) | Uso |
|---|---|---|---|---|
| IMG_1384 | 11,3 s · vert. | Rua de tijolos, malas, selfie do Diego | "Tá frio? Chegamos!" | p207, p217, p251, p273, p241, p257 |
| IMG_1403 | 5,7 s · horiz. | Panorâmica de canal largo com barcos | — | não usado |
| IMG_1422 | 9,5 s · horiz. | **Praça Dam e o Palácio Real** | — | não usado (faixa 1421–1433 no banco) |
| IMG_1445 | 5,6 s · horiz. | Fachada da batata **Manneken Pis** ("Verse Vlaamse Friet") | — | p621 (faixa) |
| IMG_1463 | 10,9 s · horiz. | Loja de interior vermelho, Marina (Tony's, pela faixa de 11/10) | — | p603, p621 |
| IMG_1474 | 7,8 s · horiz. | **Marina em frente à C&A**, rua de compras | "A gente sai do Brasil, mas o Brasil não sai da gente, não." | p621 (faixa) · **ideia nova** (banco, A3) |
| IMG_1482 | 8,0 s · horiz. | **Munttoren** ao entardecer | — | p621 (faixa) |
| IMG_1499 | 9,8 s · horiz. | Marina bebendo num terraço com luz vermelha, à noite | Fala confusa | não usado |
| IMG_1513 | 5,8 s · horiz. | Interior de bar tradicional à noite | — | não usado |
| IMG_1517 | 11,5 s · vert. (girado) | Selfie noturna dos dois, escura | "Trarei reviews…" (confusa) | não usado |
| IMG_1536 | 11,5 s · vert. | **Os dois sob o guarda-chuva** | "Bom dia! Estamos indo para o nosso primeiro ponto turístico de hoje. Casa de [Anne] Frank na chuva!" | não usado · **ideia nova** (banco, A2 e A1) |
| IMG_1537 | 9,8 s · vert. | **Marina abrindo o guarda-chuva novo**, rua molhada | "Perrengue chique: compramos um guarda-chuva. Se tá chovendo em Amsterdam…" | não usado · **ideia nova** (banco, A1) |

### Bruxelas (15/03/2026) e Bruges (16/03/2026)

| Arquivo | Hora | Duração | O que mostra | Fala | Uso |
|---|---|---|---|---|---|
| AC2A8D11….mp4 | 15/03 16:34 | 2,4 s · 1080 × 1920 | Copo de Hoegaarden na mesa | — | não usado |
| IMG_2291 | 15/03 16:41 | 0,4 s · 4K | Rua em contraluz (Mont des Arts, pelo GPS) | — | não usado (curto) |
| IMG_2406 | 15/03 20:00 | 0,6 s · vert. | Prato desfocado | — | não usado |
| IMG_2471 | 16/03 12:00 | 1,6 s · 4K | Prédio com bandeira numa praça de Bruges | — | p223, p623 (faixa) |
| IMG_2632 | 16/03 14:27 | 1,6 s · 4K | Selfie dos dois e a câmera girando para o chão | "Valeu!" | p623 (faixa) · serve de transição |
| IMG_2695 | 16/03 16:18 | 1,3 s · vert. (girado) | Selfie com bebida | — | p223, p623 (faixa) |

## 5. Mapa de uso por cidade (peças futuras do feed)

| Cidade | Peças do feed (15/10 a 07/02) | Material verificado nesta revisão | Ainda a decupar |
|---|---:|---|---|
| Barcelona | 13 (+ 2 Barcelona ou Madrid e 1 com 3 cidades) | Master e transcrição (repositório) | Brutos para cenas sem fala (trilha de violão no master) |
| Amsterdam | 9 (+ 1 com Bruges e 1 com 3 cidades) | 13 cópias MP4 | Faixas do inventário de 11/10 (.MOV) |
| Paris | 7 (+ 1 com a Disney) | 6 clipes | Vizinhos de IMG_3095–3110 (Notre-Dame), Torre (IMG_2761, IMG_2978 no repositório) |
| Bruges | 7 | 3 clipes + 4 brutos do repositório | Faixas 2417–2705 |
| Roma | 6 | 12 fotos com EXIF | — |
| Bruxelas | 6 | 3 clipes + IMG_2170 e IMG_2178 (repositório) | Faixas 2167–2411 |
| Madrid | 6 (+ 2 com Barcelona) | 17 clipes | Vizinhos dos clipes verificados |
| Disney | 5 (+ 1 com Paris) | 13 clipes | Vizinhos de IMG_3530–3575 |
| Lisboa | 5 | 2 clipes | Confirmar se houve noite em 22/03 (pendência k 55) |
| Viagem de janeiro | 6 | Material futuro | — |
| Várias cidades (panorama) | 8 | Quadros já usados nas peças | — |

**Material bom ainda sem peça** (vai para o banco): o "perrengue chique" do guarda-chuva e a Casa de Anne Frank na chuva (IMG_1536 e IMG_1537), "o Brasil não sai da gente" na C&A (IMG_1474), a Praça Dam (IMG_1422), o canal largo (IMG_1403), a reação da Marina em Madrid (IMG_3980) e a rua molhada de Madrid (97B4D6E2).
