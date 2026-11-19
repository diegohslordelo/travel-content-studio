# QA · Reel da Disney · REV1 (19/11/2026)

**Veredito: pronto para a escuta do Diego.** Formato, áudio, legendas e cortes conferidos (abaixo). Antes de postar: ouvir os itens de "Conferir no ouvido" e decidir sobre a duração (68,5 s).

**Formato:** Narrado (Trello, formato 04) · estrutura AIDA · voz do Diego gravada no quarto (19/11/2026) sobre as imagens da viagem (18/03/2026). DS V2 só no CTA (placa `SEGUE O PERFIL / @PRIMEIRODIAEM` + *clack*).

**Pedidos do Diego (19/11/2026), atendidos assim:**

| Pedido | Como ficou |
|---|---|
| Edição natural, beirando o profissional, sem cara de agência; sem mosaico de vários quadros | Uma imagem por vez, em tela cheia. Corte seco na palavra em 23 das 25 trocas. Só 2 transições, as duas com motivo: a câmera **despenca** depois de "achei que eu ia morrer" (Torre do Terror) e um **chicote** na troca de parque. Mais um efeito: o quadro **congela** na palavra "Frozen". Nada de mosaico, moldura ou efeito de catálogo |
| Legenda que acompanha a voz e vai ficando colorida | Grupos de 1 a 5 palavras curtas, numa linha só de até 800 px medidos na fonte (Inter 800, 66 px, centrados em x 540, y 1320). O grupo entra branco e cada palavra fica âmbar (`#E0AE5C`, o destaque do formato) no início dela, pelo tempo do alinhamento forçado palavra a palavra (wav2vec2 PT) |
| Gancho como o da Grand-Place, com a frase em letras garrafais e depois o vídeo normal; muito forte | "NÃO DÁ PRA IR / PRA DISNEY / DE PARIS / **EM UM DIA.**" em Anton, x 72, uma linha por vez na palavra, sobre o castelo no pôr do sol (IMG_3535, 19h08). O gancho dura 2,33 s; no corte, o som `keen` tem o pico (regra de 01/11/2026) e o vídeo segue normal. A capa é o quadro com as quatro linhas |
| Imagens estabilizadas, nada balançando | Escolha pelos planos de menor tremor (`scripts/estabilidade.py`, 63 clipes medidos; selfies trêmulos de fora). Cada recorte 9:16 é estabilizado: a janela acompanha o tremor dentro da margem do 4K, com precisão de subpixel (ver "Estabilização") |
| Decupar o áudio, sem espaço entre as falas | Entrada 0,05 s antes da voz e saída 0,10 s depois; entre blocos, 0,15 s de tom do quarto (sem silêncio digital). Exceções: 0,30 s no fim do gancho (corte + `keen`) e 0,25 s antes de "Confesso que trapaceamos". A voz nunca foi acelerada |
| A melhor imagem para cada brinquedo | Tabela de cenas abaixo: cada brinquedo aparece no plano que o identifica (placa, personagem ou veículo) |
| Animações só se precisar, no patamar "feito por mim" | Nenhuma animação de grafismo. Os únicos efeitos são os três acima, feitos sobre o próprio vídeo |
| Sem música | Entregue só com voz e efeitos. A música entra no app |
| Imagens exatamente como no Drive, sem nada de cor (pedido no meio da revisão) | Saíram a grade do formato (saturação 0,7, contraste, brilho), o grão de 6%, os degradês escuros e o tom azul do congelamento. Fica só a conversão técnica HDR (HLG) → SDR, tone mapping Möbius sem ajuste criativo |
| Sem o sombreado na base da tela (pedido no meio da revisão, "pra sempre") | Saiu o degradê escuro da legenda para baixo (e o do topo, no gancho); nada de caixa atrás da legenda. A sombra nas letras fica (o Diego confirmou: sem ela não dá para ler). Regra salva na main |

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_disney-atracoes_rev1.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, **68.47 s**, **-14.0 LUFS**, pico **-1.3 dBTP**, 196 MB |
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

| # | Tempo (s) | Dur. | Fala | Imagem (plano · trecho do bruto) | Entrada |
|---|---|---|---|---|---|
| 1 | 0.00–2.33 | 2.33 | Não dá pra ir pra Disney de Paris em um dia. | castelo da Bela Adormecida no pôr do sol · IMG_3535 0.60–2.93 | início |
| 2 | 2.33–5.10 | 2.77 | Isso foi o que me falaram e nós tínhamos duas pernas e um sonho. | 'duas pernas e um sonho': o povo andando para os parques às 9h45 · IMG_3209 0.70–3.47 | corte seco |
| 3 | 5.10–7.67 | 2.57 | Vem comigo que eu vou te mostrar tudo o que fizemos e o que você | 'Vem comigo': a Marina andando para a entrada do Studios e virando para a câmera · IMG_3211 0.60–3.17 | corte seco |
| 4 | 7.67–10.43 | 2.77 | pode fazer para conhecer os dois parques da Disney em um dia. | 'os dois parques': o castelo de dia · IMG_3345 0.10–2.87 | corte seco |
| 5 | 10.43–12.57 | 2.13 | Começamos pelo Disney Adventure e fomos direto | 'Disney Adventure': a fachada de entrada do Walt Disney Studios · IMG_3212 0.30–2.43 | corte seco |
| 6 | 12.57–15.63 | 3.07 | pro brinquedo Crush's Coaster, que é o da tartaruga do Procurando Nemo. | Crush's Coaster: os carrinhos em casco de tartaruga no embarque · IMG_3226 1.20–4.27 | corte seco |
| 7 | 15.63–18.80 | 3.17 | Depois fomos no Relâmpago McQueen. Esse é infantil, mas é legal. | Relâmpago McQueen, Luigi e Guido vistos do bonde da Cars ROAD TRIP · IMG_3249 0.40–3.57 | corte seco |
| 8 | 18.80–21.40 | 2.60 | De lá fomos pra Torre do Terror e aqui eu achei que eu ia morrer. | Hollywood Tower Hotel · IMG_3267 1.20–3.80 | corte seco |
| 9 | 21.40–23.50 | 2.10 | E fechamos o parque na área dos Avengers. Primeiro | o prédio do Avengers Campus · IMG_3286 0.10–2.50 | queda (a câmera despenca) |
| 10 | 23.50–25.73 | 2.23 | fomos na montanha-russa, que é muito boa, e depois | 'montanha-russa': a armadura do Homem de Ferro na fila da Avengers Assemble: Flight Force · IMG_3295 1.60–3.83 | corte seco |
| 11 | 25.73–27.83 | 2.10 | fomos pro brinquedo do Homem-Aranha. Confesso que esperava | prédio WEB do Spider-Man W.E.B. Adventure · IMG_3281 0.40–2.50 | corte seco |
| 12 | 27.83–31.20 | 3.37 | mais do melhor herói da Marvel. Pelo menos ele tava lá e deu um salve pra gente. | 'melhor herói da Marvel… deu um salve pra gente': o Spider-Man no telhado · IMG_3315 3.15–6.52 | corte seco |
| 13 | 31.20–33.20 | 2.00 | Segundo parque: começamos na Main Street e | segundo parque: a Main Street com o castelo no fim · IMG_3338 3.77–6.00 | chicote |
| 14 | 33.20–35.30 | 2.10 | depois fomos ver o interior do castelo. Depois fomos pro | o interior do castelo: abóbada e árvores esculpidas · IMG_3373 3.20–5.30 | corte seco |
| 15 | 35.30–38.53 | 3.23 | Piratas do Caribe, e o robô parece gente de verdade, véi. Depois, | placa do Pirates of the Caribbean, sem zoom e centrada em 'PIRATES' · IMG_3380 0.00–3.23 | corte seco |
| 16 | 38.53–41.57 | 3.03 | montanha-russa do Star Wars, a Hyperspace Mountain. Essa foi a mais | cartaz de Star Wars na fila · IMG_3402 0.10–3.13 | corte seco |
| 17 | 41.57–43.77 | 2.20 | radical do dia, e ainda fomos na primeira fileira. | 'a mais radical do dia… primeira fileira': os cartazes de naves na fila escura da Hyperspa · IMG_3410 2.08–4.28 | corte seco |
| 18 | 43.77–46.93 | 3.17 | Buzz Lightyear: tiro ao alvo com placar, e aqui eu tomei uma surra. | o Buzz Lightyear animado na fila da Buzz Lightyear Laser Blast · IMG_3424 5.00–8.17 | corte seco |
| 19 | 46.93–49.80 | 2.87 | Para fechar, fomos na montanha-russa Big Thunder no final de tarde | Big Thunder Mountain às 18h04 · IMG_3518 0.50–3.37 | corte seco |
| 20 | 49.80–51.83 | 2.03 | e pegamos esse pôr do sol surreal aí. | o pôr do sol na Big Thunder Mountain · IMG_3526 0.80–2.83 | corte seco |
| 21 | 51.83–53.87 | 2.03 | Confesso que trapaceamos: o Ratatouille tava em | 'Confesso que trapaceamos': os dois fazendo careta na fila escura da Hyperspace · IMG_3409 0.15–2.18 | corte seco |
| 22 | 53.87–56.03 | 2.17 | reforma e a área nova da Frozen ainda não existia. | a área do Ratatouille · IMG_3233 2.00–4.17 · congela em "Frozen" | corte seco |
| 23 | 56.03–58.30 | 2.27 | Provavelmente hoje dividiríamos isso em dois dias. | a Main Street acendendo · IMG_3574 0.60–2.87 | corte seco |
| 24 | 58.30–61.17 | 2.87 | Se você tem, faça. Se você não tem, não se desespere. | o castelo iluminado à noite · IMG_3590 2.00–4.87 | corte seco |
| 25 | 61.17–64.77 | 3.60 | A Disney é mágica e você vai aproveitar cada momento lá. Se você gostou desse vídeo, | 'A Disney é mágica': os fogos do show do castelo · IMG_3595 12.60–16.20 | corte seco |
| 26 | 64.77–68.47 | 3.70 | me segue aí para mais dicas e roteiros de viagem. | fecho: a câmera desce até o castelo inteiro, o mesmo quadro do gancho · IMG_3536 1.50–5.20 | corte seco |

## Estabilização

Método (`scripts/reel.py broll`): o deslocamento quadro a quadro é medido por correlação de fase **só dentro da janela 9:16 da cena** (para a paralaxe do resto do quadro não entrar na conta). O tremor é a trajetória menos a sua média de 1,2 s, e a janela acompanha esse tremor com precisão de subpixel (warpAffine, Lanczos). Panorâmica e inclinação lentas ficam. Nos planos 4K horizontais, a janela tem 1.104 × 1.962 px (zoom 1,10, com margem para a correção) e nunca é ampliada: 1.962 → 1.920 px.

Verificação em três planos (tremor medido do mesmo jeito no recorte sem e com estabilização, em % da largura): Piratas 0,50 → 0,27 · Crush 0,26 → 0,16 · Cars 1,16 → 0,91 (no Cars o bonde anda e a cena se move junto). Primeira tentativa (ffmpeg `sendcmd`, pixel inteiro e um quadro de atraso): **piorava** o tremor e foi descartada.

| Cena | Plano | Tremor medido (px no bruto) | Depois |
|---|---|---|---|
| gancho_castelo | IMG_3535 | 18.2 | 0.0 px |
| multidao_chegada | IMG_3209 | 22.8 | 0.0 px |
| marina_vem_comigo | IMG_3211 | 31.8 | 0.0 px |
| castelo_dia | IMG_3345 | 11.9 | 0.0 px |
| studios_entrada | IMG_3212 | 13.4 | 0.0 px |
| crush | IMG_3226 | 40.3 | 0.0 px |
| cars | IMG_3249 | 79.6 | 0.0 px |
| torre | IMG_3267 | 39.8 | 0.0 px |
| avengers_campus | IMG_3286 | 6.8 | 0.0 px |
| homem_de_ferro | IMG_3295 | 25.8 | 0.0 px |
| web | IMG_3281 | 24.6 | 0.0 px |
| spiderman_telhado | IMG_3315 | 60.3 | 0.9 px |
| main_street | IMG_3338 | 2.6 | 0.0 px |
| castelo_interior | IMG_3373 | 19.5 | 0.0 px |
| piratas | IMG_3380 | 0.0 | sem estabilização (a câmera se aproxima da placa) |
| star_wars | IMG_3402 | 44.5 | 0.0 px |
| hyperspace | IMG_3410 | 53.0 | 0.0 px |
| buzz | IMG_3424 | 44.4 | 0.0 px |
| big_thunder | IMG_3518 | 13.6 | 0.0 px |
| por_do_sol | IMG_3526 | 18.7 | 0.0 px |
| trapaceamos | IMG_3409 | 9.2 | 0.0 px |
| ratatouille | IMG_3233 | 28.2 | 0.0 px |
| main_street_noite | IMG_3574 | 8.5 | 0.0 px |
| castelo_noite | IMG_3590 | 4.5 | 0.0 px |
| fogos | IMG_3595 | 8.7 | 0.0 px |
| cta_castelo | IMG_3536 | 21.4 | 0.0 px |

## Áudio

| Ponto | Resultado |
|---|---|
| Voz | 15 blocos, 16 trechos; passa-alta 70 Hz, redução leve de ruído (`afftdn nr=8`), nível igualado pelo RMS de cada bloco |
| Emendas | 15 emendas, todas no silêncio (−53 a −82 dB nos 10 ms em volta) e sem salto de amostra (fades de 10/30 ms) |
| Efeitos (`_tmp/sons.json`) | `keen` −6 dB (pico no corte do gancho, 2,33 s) · `PDX_ar_longo` −6 dB (a queda, 21,1 s) · `PDX_swish` −6 dB (chicote, 31,1 s) · `PDX_obturador` −8 dB ("Frozen", 55,0 s) · *clack* da placa −6 dB. Volumes de trabalho de `docs/REFERENCIA_EDICAO_FORMATOS.md`, 4.1 |
| Música | Nenhuma (pedido do Diego) |
| Master | -14.0 LUFS integrados, pico -1.3 dBTP (alvo −14 LUFS, ≤ −1 dBTP; DS V2, 4.6) |

## Medido no vídeo final (`scripts/reel.py conferir`)

| Ponto | Resultado |
|---|---|
| Duração e formato | 68.47 s · H.264 1080 × 1920 30 qps · AAC 48 kHz ✅ |
| Áudio | -14.0 LUFS · pico -1.3 dBTP ✅ |
| Cenas | 26 · menor 2.00 s, maior 3.70 s, média 2.63 s · nenhuma abaixo de 2 s ✅ |
| Cortes no quadro da cena | 23 de 25 detectados no quadro exato (±0,05 s). As 2 restantes são as transições com movimento (queda em 21,4 s e chicote em 31,2 s), que não são corte seco; a troca Main Street → castelo por dentro (33,2 s) foi conferida no quadro (33,13 × 33,23 s) ✅ |
| Legendas | 98 grupos, 1 linha cada; a maior tem 794 px (≤ 808 px: centrada em x 540, fica em x 72–944) ✅ |
| Legenda × fala | O texto de cada grupo é a fala gravada (edicao.json), alinhada palavra a palavra; as palavras incertas estão em "Conferir no ouvido" |
| Sem tratamento de imagem | Sem grade, grão, tom ou degradê sobre a imagem (código: `design-system/remotion/src/disney/ReelDisney.tsx`) ✅ |

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
