# QA · Reel da Disney · REV1 (19/11/2026)

**Veredito: [VEREDITO]**

**Formato:** Narrado (Trello, formato 04) · estrutura AIDA · voz do Diego gravada no quarto (19/11/2026) sobre as imagens da viagem (18/03/2026). DS V2 só no CTA (placa `SEGUE O PERFIL / @PRIMEIRODIAEM` + *clack*).

**Pedidos do Diego (19/11/2026), atendidos assim:**

| Pedido | Como ficou |
|---|---|
| Edição natural, beirando o profissional, sem cara de agência; sem mosaico de vários quadros | Uma imagem por vez, em tela cheia. Corte seco na palavra em 23 das 25 trocas. Só 2 transições, as duas com motivo: a câmera **despenca** depois de "achei que eu ia morrer" (Torre do Terror) e um **chicote** na troca de parque. Mais um efeito: o quadro **congela** na palavra "Frozen". Nada de mosaico, moldura ou efeito de catálogo |
| Legenda que acompanha a voz e vai ficando colorida | Grupos de 1 a 4 palavras, numa linha só (Inter 800, 66 px, centrados em x 540, y 1320). O grupo entra branco e cada palavra fica âmbar (`#E0AE5C`, o destaque do formato) no início dela, pelo tempo do alinhamento forçado palavra a palavra (wav2vec2 PT) |
| Gancho como o da Grand-Place, com a frase em letras garrafais e depois o vídeo normal; muito forte | "NÃO DÁ PRA IR / PRA DISNEY / DE PARIS / **EM UM DIA.**" em Anton, x 72, uma linha por vez na palavra, sobre o castelo no pôr do sol (IMG_3535, 19h08). O gancho dura 2,33 s; no corte, o som `keen` tem o pico (regra de 01/11/2026) e o vídeo segue normal. A capa é o quadro com as quatro linhas |
| Imagens estabilizadas, nada balançando | Escolha pelos planos de menor tremor (`scripts/estabilidade.py`, 63 clipes medidos; selfies trêmulos de fora). Cada recorte 9:16 é estabilizado: a janela acompanha o tremor dentro da margem do 4K, com precisão de subpixel (ver "Estabilização") |
| Decupar o áudio, sem espaço entre as falas | Entrada 0,05 s antes da voz e saída 0,10 s depois; entre blocos, 0,15 s de tom do quarto (sem silêncio digital). Exceções: 0,30 s no fim do gancho (corte + `keen`) e 0,25 s antes de "Confesso que trapaceamos". A voz nunca foi acelerada |
| A melhor imagem para cada brinquedo | Tabela de cenas abaixo: cada brinquedo aparece no plano que o identifica (placa, personagem ou veículo) |
| Animações só se precisar, no patamar "feito por mim" | Nenhuma animação de grafismo. Os únicos efeitos são os três acima, feitos sobre o próprio vídeo |
| Sem música | Entregue só com voz e efeitos. A música entra no app |

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_disney-atracoes_rev1.mp4` | [ENTREGA] |
| `reel_disney-atracoes_rev1_previa.mp4` | Prévia leve (540 × 960) |
| `capa_disney-atracoes_rev1.jpg` | Capa: o gancho completo sobre o castelo no pôr do sol |
| `qa_frames/` | Um quadro por cena · um quadro por segundo |
| `../legenda_post.md` | Legendas do post (Instagram, TikTok, Shorts), com fatos e fontes |

## Roteiro × fala gravada

A fala gravada manda (`docs/FORMATOS_REELS.md`, 9.5). O Diego gravou um texto mais longo que o roteiro aprovado (≈ 38 s): **a voz decupada tem 66,9 s, e o Reel tem 68,5 s**.

| Bloco | Roteiro aprovado | Fala gravada |
|---|---|---|
| 1 | "Não dá pra ir pra Disney de Paris em um dia. Foi o que me falaram. E nós tínhamos duas pernas e um sonho." | Igual, com "**Isso** foi o que me falaram **e** nós tínhamos…" (sem pausa) |
| 2 | — | "Vem comigo que eu vou te mostrar tudo o que fizemos e o que você pode fazer para conhecer os dois parques da Disney em um dia." (novo) |
| 3 | "Começamos pelo Walt Disney Studios. Crush's Coaster, a da tartaruga." | "Começamos pelo **Disney Adventure** e fomos direto pro brinquedo Crush's Coaster, que é o da tartaruga do Procurando Nemo." |
| 4 | "Cars: infantil, mas é legal." | "Depois fomos no Relâmpago McQueen. Esse é infantil, mas é legal." |
| 5 | "Tower of Terror: eu sabia que cai e achei que ia morrer." | "De lá fomos pra Torre do Terror e aqui eu achei que eu ia morrer." |
| 6–7 | "Avengers Flight Force: vale muito a pena." / "Spider-Man: você joga teia e faz pontos." | "…montanha-russa, que é muito boa… brinquedo do Homem-Aranha. **Confesso que esperava mais do melhor herói da Marvel. Pelo menos ele tava lá e deu um salve pra gente.**" |
| 8 | "Segundo parque. Piratas do Caribe…" | "Segundo parque: começamos na Main Street e depois fomos ver **o interior do castelo**." (novo) |
| 9–11 | Piratas, Hyperspace, Buzz | Iguais no sentido; o Buzz ganhou "e aqui eu tomei uma surra" |
| 12 | — | "Para fechar, fomos na montanha-russa **Big Thunder** no final de tarde e pegamos esse pôr do sol surreal aí." (a atração das 18h04, que estava em aberto) |
| 13 | "Confesso: trapaceamos. A área nova ainda não estava aberta quando fomos." | "Confesso que trapaceamos: o Ratatouille tava em reforma e a área nova da **Frozen** ainda não existia." |
| 14 | "E acho que hoje tem que dividir pra aproveitar tudo." | "Provavelmente hoje dividiríamos isso em dois dias. Se você tem, faça. Se você não tem, não se desespere. A Disney é mágica e você vai aproveitar cada momento lá." |
| 15 | CTA "Manda pra quem vai pra Disney de Paris" | "Se você gostou desse vídeo, **me segue** aí para mais dicas e roteiros de viagem." → a placa segue a fala: `SEGUE O PERFIL / @PRIMEIRODIAEM` |

**Gancho:** no pedido, o Diego escreveu "me disseram que não dá para conhecer a Disney de Paris em um dia", mas a gravação diz "Não dá pra ir pra Disney de Paris em um dia". O texto na tela segue a gravação.

## Cenas (26)

[CENAS]

## Estabilização

[ESTAB]

## Áudio

| Ponto | Resultado |
|---|---|
| Voz | 15 blocos, 16 trechos; passa-alta 70 Hz, redução leve de ruído (`afftdn nr=8`), nível igualado pelo RMS de cada bloco |
| Emendas | 15 emendas, todas no silêncio (−53 a −82 dB nos 10 ms em volta) e sem salto de amostra (fades de 10/30 ms) |
| Efeitos (`_tmp/sons.json`) | `keen` −6 dB (pico no corte do gancho, 2,33 s) · `PDX_ar_longo` −6 dB (a queda, 21,1 s) · `PDX_swish` −6 dB (chicote, 31,1 s) · `PDX_obturador` −8 dB ("Frozen", 55,0 s) · *clack* da placa −6 dB. Volumes de trabalho de `docs/REFERENCIA_EDICAO_FORMATOS.md`, 4.1 |
| Música | Nenhuma (pedido do Diego) |
| Master | [MASTER] |

## Medido no vídeo final (`scripts/reel.py conferir`)

[MEDIDO]

## Conferir no ouvido (o Claude não escuta áudio)

1. **"Depois fomos no Relâmpago McQueen"** (15,6 s): o Whisper ouviu "Somozeiro Relâmpago Marquinhos" e o wav2vec2 "fomos er u relâmpago". Se for outra coisa (ex.: "fomos no do"), troco a legenda.
2. **"o Ratatouille tava em reforma"** (53,3 s): o Whisper ouviu "também reforma". Se for "tá em reforma", troco.
3. **"tiro ao alvo com placar"** (44,5 s): o Whisper ouviu "tira o alvo com o placar".
4. **"pro brinquedo Crush's Coaster"** e **"Procurando Nemo"** (12,6 e 14,9 s).
5. **As emendas sem pausa:** a voz ficou corrida como pedido; confira se alguma passagem entre blocos ficou apertada demais (ex.: 18,7 s, Cars → Torre).
6. **Os efeitos:** `keen`, a queda, o chicote e o obturador nunca foram ouvidos pelo repositório; volumes provisórios.

## Pendências e observações

- **Duração: 68,5 s.** A referência de conteúdo recomenda 7 a 30 s, e os formatos de história até ≈ 45 s. O texto gravado tem 15 blocos e todos ficaram; a voz não foi acelerada nem cortada. Se a retenção cair antes da metade, a ordem de corte sugerida é: (1) bloco 2 ("Vem comigo…", −5,3 s); (2) a 2ª metade do bloco 14 ("Se você tem, faça…", −3,2 s); (3) o bloco 8 (castelo por dentro, −3,5 s). Isso dá ≈ 56 s. Não foi feito: depende do Diego.
- **Cenas acima de 3 s:** 7 das 26 ficam entre 3,03 e 3,70 s (alvo do Narrado: até 3 s, regra do Trello). Nenhuma fica abaixo de 2 s (regra do Diego). As longas são falas inteiras sobre um plano só (Spider-Man, Piratas, Buzz, fogos, CTA) e não tinham onde cortar sem quebrar a regra dos 2 s.
- **Nome do parque:** na fala, "Disney Adventure", o nome de hoje; em 18/03/2026 ainda era Walt Disney Studios. A legenda do post explica.
- **Marina na imagem:** aparece em duas cenas ("Vem comigo" e "Confesso que trapaceamos"), como parceira de viagem (CLAUDE.md, 2: cenas dos dois podem ser usadas).
