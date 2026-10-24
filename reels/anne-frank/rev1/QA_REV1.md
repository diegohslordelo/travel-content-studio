# QA · REV1 · "Casa de Anne Frank" (tela dividida)

**Veredito: pronto para postar depois de 1 escuta do Diego** (itens em "Conferir no ouvido").

| Item | Valor |
|---|---|
| Arquivo final | `reel_anne-frank_rev1.mp4` · 1080 × 1920 · 30 fps · 50,3 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_anne-frank_rev1_previa.mp4` (540 × 960) |
| Capa | `capa_anne-frank_rev1.jpg` (quadro do gancho com a frase inteira) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,4 dBTP (DS V2, 4.6) · faixa única: voz original + *clack* do CTA |
| Transcrição | `TRANSCRICAO.md` (+ `transcricao_large-v3.json` e `transcricao_large-v2.json`) |
| Projeto editável | `rev1.json` (decisões) · `rev1.py` (pipeline) · composição `ReelAnneFrank` em `design-system/remotion/src/annefrank/` |
| Folha de quadros | `qa_frames/folha_rev1.jpg` |

## Pedido (24/10/2026)

Reel em tela dividida a partir dos 7 takes gravados pelo Diego em 23/10/2026 (pasta do Drive "Reel Anne Frank"), com dois Reels de referência (Daniel Lopez, `De2hbGYR9DL`; Hanah Franklin, `DPAM7t8jWR5`). Regras do pedido que valem só para este Reel:

- **DS V2 só no CTA final.** Gancho, capa, legendas, rótulos e animações usam linguagem própria (abaixo).
- **Nenhuma imagem do Diego ou da Marina como apoio.** O Diego aparece só no take em que fala.
- **Áudio das imagens de apoio 100% mudo.** Só a voz original.
- **CTA na tela no fim**, porque não foi gravado.

O terceiro link enviado (`criadoresdofuturo.short.gy/hanahfranklin5` → Reel `DElIlC7Sg0l`) não baixou: o Instagram respondeu 429 (limite de acesso). A análise usou os dois Reels que o pedido chama de referência.

## O que as referências ensinaram (e como entrou aqui)

| Princípio observado | Daniel Lopez | Hanah Franklin | Neste Reel |
|---|---|---|---|
| Tela dividida: apoio em cima, quem fala embaixo | Base da edição | Só na abertura | Base da edição (costura em y 900) |
| Imagem de apoio toma a tela inteira em momentos-chave | Sim | Sim | Ilustração da casa, data da prisão, 8 pessoas, anexo vazio, entardecer final |
| Cartão flutuante sobre fundo desfocado em P&B | Sim (livros, fotos) | Sim (prints) | Anne (1942) e Otto Frank sobre o Diego desfocado |
| Fala em tela cheia com aproximação | Pouco | Muito (*punch-in*) | 2 vezes, nos momentos de fala direta ("E tem um detalhe…" e "…de conhecer qualquer outro ponto turístico") |
| Legenda curta (1–3 palavras), sempre no mesmo lugar | Sim, na costura | Sim, no centro | Sim, na costura (tela dividida) ou no terço de baixo |
| Palavra-chave grande sobre a imagem | Pouco | Muito | "13 ANOS", "2 ANOS", "AGOSTO DE 1944", "1 DE 8", "1960" |
| Ritmo variado | Cortes a cada 1,5–4 s | Cortes e zooms a cada 1–3 s | 25 cenas em 50 s: de 0,8 s (canal) a 3,9 s (ilustração), mais lento na parte sensível |

## Roteiro de cortes

| Tempo (s) | Fala | Composição | Imagem |
|---|---|---|---|
| 0,00–3,70 | "A melhor atração de Amsterdã também é uma das mais tristes da cidade." | **Gancho**, tela cheia | Canal ao entardecer com a torre da Westerkerk, vizinha da casa (`IMG_2068`), Ken Burns 100 → 109%. Texto do gancho (a frase falada) em 2 blocos; o 2º entra linha a linha no tempo da fala |
| 3,70–5,60 | "Por fora parece só mais uma casa bonita…" | Tela dividida | Porta e fachada da Prinsengracht 263, câmera subindo (`IMG_1556`, 2× mais rápido) |
| 5,60–6,43 | "…à beira de um canal," | Tela dividida | Canal ao lado da casa (`IMG_1561`) |
| 6,43–10,30 | "mas por dentro, atrás de um armário, havia uma passagem para um anexo…" | **Ilustração em tela cheia** | Casa em corte: a câmera aproxima do armário quando ele é dito, o armário gira e revela a luz, o pontilhado percorre a passagem e o anexo acende com "ANEXO SECRETO" |
| 10,30–11,63 | "…secreto da casa." | Tela dividida | Os fundos do anexo, hoje (foto) |
| 11,63–12,57 | "Foi ali que Anne Frank," | **Cartão** sobre o Diego desfocado | Anne Frank, maio de 1942 |
| 12,57–13,87 | "com apenas 13 anos," | Tela dividida | A mesma foto, com "13 ANOS" |
| 13,87–16,00 | "passou dois anos de sua vida escondida" | Tela dividida | Linha do tempo: "2 ANOS" · JUL 1942 → AGO 1944 |
| 16,00–18,33 | "com a sua família e outras quatro pessoas." | Tela dividida | As 8 pessoas: Família Frank (4) entram em "família", + 4 em "outras quatro" |
| 18,33–19,87 | "Durante esse período, ela escreveu um diário" | Tela dividida | Anne escrevendo, 1940 |
| 19,87–22,07 | "que se tornou um dos relatos mais conhecidos…" | Tela dividida | O diário em exposição (Kiel, 2019) |
| 22,07–24,63 | "…perseguição aos judeus durante o nazismo." | Tela cheia, tom escuro | O mesmo diário bem de perto, quase P&B |
| 24,63–26,23 | "Em agosto de 1944," | **Tela cheia** | "AGOSTO DE 1944" |
| 26,23–28,30 | "as pessoas foram descobertas e presas." | Tela cheia | As 8 pessoas apagam para cinza |
| 28,30–30,07 | "Otto Frank, que era o pai de Anne," | Cartão | Otto Frank, 1961 |
| 30,07–33,10 | "foi o único das oito pessoas escondidas que retornou." | Tela cheia | Só o Otto acende de novo, com "1 DE 8" |
| 33,10–34,77 | "E tem um detalhe que muita gente não conhece," | **Diego em tela cheia**, aproximação 110 → 116% | — |
| 34,77–36,63 | "em 1960, quando o museu abriu," | Tela dividida | Abertura do museu, 3/5/1960, com "1960" |
| 36,63–37,83 | "a pedido do pai de Frank," | Tela dividida | Otto Frank |
| 37,83–39,40 | "o esconderijo foi mantido vazio." | Tela cheia | O anexo vazio, 1957 |
| 39,40–41,07 | "Por isso que visitar essa casa é diferente" | Tela dividida | Porta com a placa "Anne Frank Huis" (`IMG_1555`) |
| 41,07–43,10 | "de conhecer qualquer outro ponto turístico," | Diego em tela cheia | — |
| 43,10–44,97 | "porque você se conecta com a história real" | Tela dividida | Estátua de Anne Frank na Westermarkt (`IMG_1558`, aproximada para tirar a obra do quadro) |
| 44,97–47,07 | "que ainda preserva suas marcas." | Tela cheia | Canal ao entardecer (`IMG_2070`) |
| 47,07–50,27 | — | **CTA (DS V2)** | O mesmo plano continua; placa `MANDA PRA QUEM VAI PRA / AMSTERDAM →` com Chegada e *clack* |

## Imagens usadas e licenças

### Acervo do Diego (Drive, `Youtube/Amsterdam`; áudio mudo)

| Arquivo | O que é | Gravado |
|---|---|---|
| `IMG_1555.MOV` | Porta verde com a placa "Anne Frank Huis" | 13/03/2026 10:56 |
| `IMG_1556.MOV` | Porta e fachada da Prinsengracht 263 | 13/03/2026 10:56 |
| `IMG_1558.MOV` | Estátua de Anne Frank, Westermarkt | 13/03/2026 11:11 |
| `IMG_1561.MOV` | Canal perto da casa | 13/03/2026 11:24 |
| `IMG_2068.MOV` | Canal ao entardecer com a Westerkerk | 14/03/2026 18:53 |
| `IMG_2070.MOV` | Canal ao entardecer | 14/03/2026 18:54 |

Descartados por mostrarem o Diego ou a Marina: `IMG_1543`, `IMG_1566`, `IMG_1568`, `IMG_1570` (mesma manhã, perto da casa).

### Imagens externas (Wikimedia Commons; arquivos em `imagens/`)

| No Reel | Arquivo | Autor | Licença | Fonte |
|---|---|---|---|---|
| Anne Frank · maio de 1942 | `anne_1942.jpg` | Autor desconhecido (coleção Anne Frank House) | Domínio público (obra anônima com mais de 70 anos, UE) | [Commons](https://commons.wikimedia.org/wiki/File:Anne_Frank_passport_photo,_May_1942.jpg) |
| Anne Frank · 1940 | `anne_1940_escrevendo.jpg` | Autor desconhecido (Coleção Anne Frank Stichting) | Domínio público (obra anônima com mais de 70 anos, UE) | [Commons](https://commons.wikimedia.org/wiki/File:AnneFrank1940_crop.jpg) |
| O diário em exposição · Kiel, 2019 | `diario_kiel_2019.jpg` | Diego Delso | CC BY-SA 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Diario_de_Anne_Frank,_Iglesia_de_San_Nicol%C3%A1s,_Kiel,_Alemania,_2019-09-10,_DD_22.jpg) |
| Otto Frank · 1961 | `otto_frank_1961.jpg` | Jack de Nijs / Anefo | CC BY-SA 3.0 NL | [Commons](https://commons.wikimedia.org/wiki/File:Otto_Frank_(1961).jpg) |
| Abertura do museu · 3/5/1960 | `abertura_1960.jpg` | Henk Lindeboom / Anefo (Nationaal Archief) | CC0 | [Commons](https://commons.wikimedia.org/wiki/File:Woonkamer_van_de_familie_Frank,_Bestanddeelnr_911-2116.jpg) |
| O anexo vazio · 1957 | `anexo_vazio_1957.jpg` | Wim van Rossem / Anefo (Nationaal Archief) | CC0 | [Commons](https://commons.wikimedia.org/wiki/File:Raampartij_in_het_achterhuis_van_Anne_Frank,_Bestanddeelnr_908-4340.jpg) |
| Os fundos do anexo, hoje | `anexo_fundos_2026.jpg` | Hannolans | CC BY 4.0 | [Commons](https://commons.wikimedia.org/wiki/File:Achterzijde_Achterhuis.jpg) |

- **Crédito:** cada foto mostra na tela o que é, o ano, o autor e a licença. Os créditos completos também estão na legenda do post (`legenda_post.md`). As licenças CC BY e CC BY-SA pedem crédito; a CC BY-SA vale para a foto adaptada (recorte, cor), não para o Reel inteiro.
- **Domínio público das fotos de Anne:** vale na UE (obra anônima, mais de 70 anos). Nos EUA, algumas fotos de Anne Frank têm status discutido no próprio Commons. Para um perfil brasileiro no Instagram, o risco é baixo, mas fica registrado.
- **Datas conferidas no Nationaal Archief (via Commons):** a série "Anne Frank Huis geopend" (Otto Frank discursando) é de **01/05/1961**, não da abertura. Por isso a foto da abertura é a de **03/05/1960** (visitantes no dia da reabertura) e o Otto aparece rotulado como **1961**.

### Gerado para o vídeo

| No Reel | O que é |
|---|---|
| Casa em corte | Ilustração esquemática feita em código (SVG), com "ILUSTRAÇÃO" na tela. Não é planta nem reconstrução fiel: mostra casa da frente, armário, passagem e anexo |
| 8 pessoas, linha do tempo, "AGOSTO DE 1944", "1 DE 8" | Gráficos com dados históricos: Otto, Edith, Margot e Anne Frank; Hermann, Auguste e Peter van Pels; Fritz Pfeffer. Esconderijo de 6/7/1942 a 4/8/1944 |

**Nenhuma imagem gerada por IA.** Não foi preciso: a lacuna do interior do museu foi coberta com fotos de arquivo reais (anexo vazio em 1957, abertura em 1960) e com a ilustração identificada como tal.

## Linguagem visual própria (fora do DS)

| Elemento | Valor | Por quê |
|---|---|---|
| Gancho, números, títulos | Anton (OFL), branco, caixa-alta | Pesada e condensada, como a capa de referência, sem usar a Barlow Condensed do DS |
| Legendas e rótulos | Inter 800/700 (OFL), branco com sombra | Leitura rápida, neutra, editorial |
| Destaque | âmbar `#E0AE5C` | Luz de lamparina: única cor quente, usada na palavra-chave da legenda, no caminho secreto e no anel do Otto |
| Fundos das animações | `#14120F` (quase preto quente) | Sobriedade; as fotos de arquivo são P&B |
| Imagens de apoio | Saturação 70%, contraste 106% | Tira o rosa do entardecer convertido do HDR e aproxima o vídeo das fotos de arquivo |

Os valores ficam em `design-system/remotion/src/annefrank/estilo.ts`, separados do DS. **Não são valores da marca** e não devem ser reaproveitados em outras peças sem decisão do Diego.

## Verificação final

| Ponto do pedido | Situação |
|---|---|
| O gancho é a 1ª frase real | ✅ "A melhor atração de Amsterdã também é uma das mais tristes da cidade." (take 1, os 2 modelos concordam) |
| A composição varia com intenção | ✅ Tela dividida (13 cenas), tela cheia de apoio (8), cartão (2), Diego em tela cheia (2) |
| As imagens ilustram a fala | ✅ Cada troca cai na palavra (tabela acima) |
| Nenhuma imagem do Diego ou da Marina como apoio | ✅ Conferido na folha `qa_frames/folha_rev1.jpg` (um quadro por cena) e na escolha dos clipes do acervo |
| Áudio das imagens de apoio mudo | ✅ Todos os B-rolls saem do `preparar` com `-an`; a única faixa é `voz.wav` (+ *clack* do CTA) |
| Voz original preservada | ✅ Sem voz sintética, sem corte dentro das frases; só ganho, passa-alta em 70 Hz e o master |
| DS V2 só no CTA | ✅ Placa CTA (2.7), Chegada e *clack* (4.6) só a partir de 47,07 s. O resto usa Anton, Inter e a paleta acima |
| Animações não escondem informação | ✅ Rótulos no topo da imagem, legenda na costura ou no terço de baixo, nada na faixa da interface do Instagram (y 1440–1920) |
| Render conferido | ✅ Render completo (1.508 quadros, 50,27 s), conferido por quadros (folha de 26 quadros, um por cena) e pela medição do áudio (B-rolls sem faixa de som; depois da fala, só o *clack* em 47,5 s). A escuta é do Diego |

## Conformidade com o DS V2 (só o CTA)

| Item | Situação |
|---|---|
| CTA "botão" (2.7) | ✅ Placa com o verbo + módulo de seta: `MANDA PRA QUEM VAI PRA` / `AMSTERDAM →`. 1 CTA na peça. Mesmo verbo na legenda do post |
| Posição | ✅ x 72 · y 640 (posição fixa da placa no Reel, 1.3) |
| Movimento e som | ✅ Chegada (560 ms) + brilho de esmalte; *clack* no quadro 8, −10 dB da voz (4.6) |
| Sobre a cena, não sobre tela preta | ✅ Sobre o canal ao entardecer |
| Master | ✅ −14,0 LUFS integrados · −1,4 dBTP |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Contraste "melhor × mais triste" no quadro 0, em letras grandes |
| 2 | Uma ideia central | ✅ "A casa de Anne Frank não é um ponto turístico qualquer: o anexo ainda guarda a história real." |
| 3 | Funciona sem som | ✅ Gancho escrito e legenda em toda a fala |
| 4 | Motivo de envio | ✅ Para quem vai a Amsterdam (CTA); salvamento pela dica do ingresso na legenda |
| 5 | Valor ou emoção | ✅ Emoção (história) + utilidade (como visitar) |
| 6 | Marca reconhecível | ⚠️ Só a placa do CTA, por decisão do pedido. É menos marca que o padrão do DS |
| 7 | Conformidade DS V2 | ✅ No CTA (acima) |
| 8 | Identidade verbal | ✅ Direto e preciso; sem bordão (não é Reel de primeiro dia) |
| 9 | Originalidade | ✅ Fala e vídeos próprios; fotos de arquivo com licença e crédito |
| 10 | Formato e duração | ⚠️ **50,3 s**, acima da duração padrão de 7–30 s da referência de conteúdo (3.1). Toda a fala ficou, porque cada frase leva a história adiante. Ver "Riscos" |

## Conferir no ouvido (≈ 2 min)

A transcrição é automática e a validação auditiva é humana (CLAUDE.md, 12).

1. **3,9 s:** é "por fora **parece**" (como está na legenda) ou "**aparece**"?
2. **3,5 s e 39,3 s:** "cidade." e "vazio." estão inteiros? Os dois takes terminam logo depois da palavra.
3. **37,4 s:** "a pedido do pai de **Frank**": a legenda reproduz o que foi dito.
4. **Mixagem:** a voz é a única faixa; os takes têm volumes parecidos (−22,5 LUFS antes do ganho). O *clack* do CTA (47,6 s) é o som sintetizado v1 do DS.

Se algo estiver errado: corrigir `correcoes_legenda` em `rev1.json` e rodar `python3 rev1.py tudo`.

## Decisões desta revisão (valem só para este Reel)

- **Sem trilha no render.** A trilha entra na hora de postar (biblioteca do Instagram, 8 a 10 dB abaixo da voz), como o DS indica (4.6). Sugestão: piano ou cordas lentas, sem batida.
- **"Armário" na fala, "estante" na legenda do post.** A passagem era escondida por uma estante giratória. A fala ficou como foi dita; a ilustração mostra um móvel com livros.
- **Linha do tempo com datas exatas** (6/7/1942 → 4/8/1944) sob o "2 ANOS" que o Diego fala: deixa o número verificável.
- **Nomes das 8 pessoas na tela:** dado histórico público. Ajuda a entender "outras quatro pessoas" e "o único das oito".
- **Sem imagem para "perseguição aos judeus"**. A foto da estrela amarela encontrada no Commons era a versão belga ("J"), errada para Amsterdam; a holandesa ("Jood") não baixou (o Commons limitou o acesso). Em vez disso, o diário fica na tela, bem de perto e escurecido.
- **30 fps** (FPS de produção não definido, pendência 5).

## Riscos

- **Duração (50,3 s).** Se a retenção cair antes da metade no Insights, a próxima versão pode cortar o take 4 (diário, 6,3 s) ou o take 6 (1960, 6,3 s) e ficar em ≈ 38–44 s. É **uma variável por teste** (referência de conteúdo, 8.3).
- **Tema sensível.** Nada de humor, efeito sonoro ou figurinha na divulgação. Os gráficos usam só dados históricos.
- **Fotos de Anne Frank:** domínio público na UE; status discutido nos EUA (ver "Imagens externas").

## Como refazer

```bash
cd reels/anne-frank/rev1
python3 rev1.py tudo        # preparar → render → master → capa → quadros
```

Os brutos ficam em `../fonte/` (fora do git); os do acervo em `../fonte/acervo/`. Se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
