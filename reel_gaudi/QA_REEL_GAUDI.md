# QA · Reel do Gaudí (tela dividida)

**Veredito: pronto para postar depois de 1 escuta do Diego** (≈ 1 min, itens em "Conferir no ouvido"). O Claude mediu tudo, mas não escuta áudio (CLAUDE.md, 12).

| Item | Valor |
|---|---|
| Arquivo final | `reel_gaudi_final.mp4` · 1080 × 1920 · 30 qps · **44,83 s** (1.345 quadros) · H.264 High 19,3 Mb/s + AAC-LC 48 kHz estéreo 252 kb/s (mesmo formato do Reel Anne Frank) |
| Prévia leve | `reel_gaudi_previa.mp4` (540 × 960) |
| Capa | `capa_reel_gaudi.jpg` (gancho com a frase inteira) |
| Áudio | −14,0 LUFS integrados · pico verdadeiro −1,8 dBTP · nenhuma amostra acima de −1 dBFS · só a voz do Diego + *clack* do CTA (a trilha entra no Instagram, 8–10 dB abaixo da voz) |
| Padrão | `padrao.md` (medido no Reel Anne Frank REV2, tela dividida) |
| Arquivos e créditos | `arquivos_encontrados.md` · `creditos.md` |
| Projeto editável | `edicao.json` (falas e áudio) · `cenas.json` (imagem por palavra) · `scripts/reel.py` (pipeline) · composição `ReelGaudi` em `design-system/remotion/src/gaudi/` |
| Conferência | `scripts/conferir.py` → `qa/conferencia.json` · folhas `qa/folha_cenas.jpg` (1 quadro por cena) e `qa/folha_1s.jpg` (1 por segundo) |

## Fala × roteiro

O Diego gravou com palavras próprias e avisou (26/10/2026). **A legenda segue a fala gravada**, com os números escritos como no roteiro ("1926", "1/4", "100"). Diferenças:

| Parte | Roteiro | Fala gravada (= legenda) |
|---|---|---|
| 1 | …e morreu **tratado como mendigo**. | …e morreu **como um morador de rua**. |
| 2 | …atropelado por um bonde. | …atropelado por um bonde **na Gran Via de Barcelona**. |
| 3 | Roupa surrada, sem documento: **todo mundo achou que era mendigo**. | Roupa surrada, sem documento, **ninguém sabia quem era ele**. |
| 4 | **Levaram ele pra um hospital velho, sem saber quem era. Três dias depois, morreu.** | **E aí levaram ele para um hospital simples para tomar cuidados básicos, mas chegando lá ninguém reconheceu. E depois de três dias ele faleceu.** |
| 5 | **Mas ele já foi elegante. Largou tudo pela obra, perdeu o interesse pela aparência** e passou a dormir num **quartinho dentro dela**. | **Nem sempre foi assim, ele largou tudo pela obra, ele se desligou de aparência** e passou a dormir num **quarto dentro da igreja junto com outras maquetes** |
| 6 | E quando ele morreu, nem 1/4 da igreja estava pronta. | igual ("nem um quarto" → legenda "nem 1/4") |
| 7 | **Cem anos depois**, o Papa abençoou a torre mais alta da igreja. **Hoje, milhões visitam.** Mas naquele dia, **ninguém reconheceu o homem**. | **Depois de 100 anos**, o Papa abençoou a torre mais alta da igreja. **Milhões visitam a igreja**, mas naquele dia, **ninguém sabia quem era Gaudí**. |
| 8 | Por trás de todo monumento tem alguém de carne e osso. **Saber a história muda a visita.** | Por trás de todo **o** monumento tem alguém de carne e osso **com a história por trás e saber disso muda a maneira que você vive a visita**. |
| 9 | Salva esse vídeo pra lembrar disso em Barcelona. | **Já** salva esse vídeo pra lembrar disso em Barcelona. |

Nenhuma palavra foi trocada. **Uma frase gravada ficou fora:** "…pra viver o projeto." (fim da parte 5). O iPhone cortou o fim de "projeto" (a trilha de áudio acaba em 7,79 s, no meio da palavra), e ela não está no roteiro. A parte 5 termina em "maquetes", numa pausa natural de 0,24 s.

## Áudio e timing

| Etapa | O que foi feito |
|---|---|
| Transcrição | Whisper large-v3 nas 7 tomadas + **alinhamento forçado** palavra a palavra (wav2vec2 PT, `scripts/alinhar.py` → `transcricao_alinhada.json`). O Whisper prende a 1ª palavra em 0,00 s; o alinhamento mede o início real |
| Decupagem | Cada tomada aparada no silêncio antes e depois da fala (início e fim medidos pela energia na faixa da voz). Cada uma tinha só 1 tomada, então não houve escolha entre tomadas |
| Pausas | 2 pausas longas encurtadas no silêncio: depois de "básicos," (0,34 → 0,18 s) e de "naquele dia," (0,41 → 0,22 s). Os 2 cortes caem em cenas sem o Diego na tela (sem pulo de imagem) |
| Respiração | Mantida curta entre as partes 4→5 (0,36 s entre "faleceu." e "Nem") e 7→8 (0,38 s entre "Gaudí." e "Por"); nas outras emendas, 0,19–0,28 s |
| Fim de "visita." | O iPhone cortou a trilha ≈ 35 ms dentro do "a" final. Ficou só o que foi gravado, com fade de 25 ms dentro da vogal e tom de sala depois (sem corte seco). Testados e descartados: continuar a vogal com os períodos do próprio "a" e emprestar o "-ta"/"a" de outras palavras do Diego ("pronta.", "rua.", "Família,", "sabia", "igreja."). Em todos, o Whisper passou a ouvir "vizinha", "visão" ou "vida"; com o original, ouve "visita." (0,88) |
| Ruído e nível | Passa-alta 70 Hz, redução leve de ruído (`afftdn`, 8 dB), tomadas igualadas no nível, voz a −14 LUFS com limitador (pico −1,9 dBTP), master −14,0 LUFS / −1,8 dBTP |
| Velocidade | **Voz sem aceleração** (1,0×). Duração 44,83 s: não foi preciso tirar a parte 6 |

## Roteiro de cortes (31 cenas, média 1,45 s, de 0,83 a 3,80 s)

| Tempo (s) | Fala | Composição | Imagem |
|---|---|---|---|
| 0,00–3,80 | Ele desenhou o cartão postal de Barcelona e morreu como um morador de rua. | Gancho · tela cheia | acervo · fachada da Natividade com guindaste |
| 3,80–5,07 | Em 1926, | Tela cheia · animação | criada · 1926 |
| 5,07–6,20 | Gaudí, o arquiteto | Cartão | web · Gaudí em 1924 (Corpus Christi) |
| 6,20–7,07 | da Sagrada Família, | Tela dividida | acervo · esculturas da Natividade |
| 7,07–8,27 | foi atropelado por um bonde | Tela dividida | criada · ilustração do bonde |
| 8,27–9,67 | na Gran Via de Barcelona. | Tela dividida | web · Gran Via de les Corts Catalanes |
| 9,67–11,37 | Roupa surrada, sem documento, | Tela dividida | web · Gaudí em 1924 (Brangulí) |
| 11,37–12,67 | ninguém sabia quem era ele. | Diego em tela cheia (zoom 1,10→1,16) | — |
| 12,67–14,13 | E aí levaram ele para um hospital simples | Tela dividida | web · claustro do Hospital de la Santa Creu |
| 14,13–15,43 | para tomar cuidados básicos, | Tela dividida | web · pátio do Hospital de la Santa Creu |
| 15,43–17,20 | mas chegando lá ninguém reconheceu. | Tela cheia | web · claustro do Hospital de la Santa Creu |
| 17,20–18,70 | E depois de três dias | Tela cheia · animação | criada · TRÊS DIAS |
| 18,70–19,73 | ele faleceu. | Cartão | web · Gaudí em 1924 (Corpus Christi) |
| 19,73–20,57 | Nem sempre foi assim, | Cartão | web · Gaudí em 1878 |
| 20,57–21,77 | ele largou tudo pela obra, | Tela dividida | web · canteiro da Sagrada, c. 1915 |
| 21,77–23,13 | ele se desligou de aparência | Tela dividida · animação | web · 1878 × 1924 lado a lado |
| 23,13–24,40 | e passou a dormir num quarto | Tela dividida | web · casa-oficina de Gaudí no canteiro, 1906 |
| 24,40–25,33 | dentro da igreja | Tela dividida | web · oficina com maquetes, 1926 |
| 25,33–26,60 | junto com outras maquetes | Tela dividida | acervo · maquete da Sagrada no museu |
| 26,60–29,20 | E quando ele morreu, nem um quarto da igreja estava pronta. | Tela cheia · animação | criada · 1/4 sobre o canteiro c. 1915 |
| 29,20–30,37 | Depois de 100 anos, | Tela cheia · animação | criada · 100 ANOS |
| 30,37–31,20 | o Papa abençoou | Tela dividida | web · missa da bênção da torre, 10/06/2026 |
| 31,20–32,70 | a torre mais alta da igreja. | Tela cheia | acervo · Torre de Jesus Cristo com a cruz, mar/2026 |
| 32,70–34,07 | Milhões visitam a igreja, | Tela dividida | acervo · colunas e teto da nave |
| 34,07–35,00 | mas naquele dia, | Tela dividida | web · Gaudí em 1924 (Brangulí) |
| 35,00–36,83 | ninguém sabia quem era Gaudí. | Tela cheia | web · Gaudí em 1878 |
| 36,83–37,97 | Por trás de todo o monumento | Tela cheia | acervo · fachada da Paixão com guindaste |
| 37,97–39,03 | tem alguém de carne e osso | Diego em tela cheia (zoom 1,00→1,05) | — |
| 39,03–40,03 | com a história por trás | Tela dividida | web · oficina com maquetes, 1926 |
| 40,03–42,47 | e saber disso muda a maneira que você vive a visita. | Diego em tela cheia (zoom 1,08→1,14) | — |
| 42,47–44,83 | Já salva esse vídeo pra lembrar disso em Barcelona. | CTA (DS V2) · tela cheia | acervo · o mesmo plano do gancho (loop) |

## Conferência final (medida, `qa/conferencia.json`)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração ≤ 45,0 s | ✅ 44,83 s (ffprobe) |
| 2 | Legendas dentro das áreas seguras, sem cortar palavras | ✅ 55 grupos, todos em 1 linha. O mais largo tem 744 px (x 168–912, dentro de x 72–944). Centro dos blocos em y 900, 1320 e 1375, dentro de y 256–1440; nada na faixa da interface (y 1440–1920) |
| 3 | Cada imagem corresponde à fala do momento | ✅ 30 trocas. Desvio médio de 0,04 s entre o corte e a palavra; o maior é 0,16 s ("mas", antes do corte de pausa). Todas dentro de 0,3 s. Conferidas também nas folhas de quadros |
| 4 | Áudio sem clipping e sem corte seco no meio de palavra | ✅ 0 amostras acima de −1 dBFS. As emendas que eu fiz caem no ruído da sala (−40 a −56 dB). A transcrição da voz final (Whisper large-v3) bate palavra por palavra com a fala gravada, inclusive "visita." |
| 5 | Divisão de tela igual ao padrão | ✅ Costura em y 900 com a linha escura de 6 px em y 897–902, medida em 6 cenas. Diego embaixo, apoio em cima |

## Conferir no ouvido (≈ 1 min)

1. **42,3 s · "…você vive a visi**ta.**"**: o "-ta" final é curtinho, porque é só o que o iPhone gravou. Se soar cortado, a solução definitiva é regravar só a parte 8 com 1 s de silêncio no fim (material futuro).
2. **19,7 s "Nem", 36,8 s "Por" e 42,5 s "Já"**: as tomadas 7242, 7244 e 7245 começam com a voz já no 1º quadro de áudio. Conferir se o começo da palavra não ficou comido.
3. **15,5 s e 35,0 s**: as duas pausas encurtadas soam naturais?
4. **Ritmo**: as imagens trocam em média a cada 1,45 s, contra 2,03 s no Anne Frank, porque cada imagem acompanha a fala.

## Decisões deste Reel (não são regra da marca)

- **Linguagem visual do Reel Anne Frank** (Anton, Inter, âmbar `#E0AE5C`, fundo `#14120F`, grão 6%), copiada sem mudar valores porque o pedido é o padrão dos Reels antigos. **DS V2 só no CTA**: Placa `SALVA ESSE VÍDEO` / `BARCELONA →` em x 72 · y 640, com Chegada e *clack*. O texto vem da fala da parte 9.
- **Sem rótulo de crédito na tela** (regra do pedido: nada de texto fora da fala). O crédito vai na legenda do post (`creditos.md`).
- **Degradê escuro na base** das tomadas claras em tela cheia, para a legenda se ler sobre a pedra da Sagrada.
- **Loop**: o CTA volta ao plano do gancho (fachada da Natividade).
- **30 qps**, como o Anne Frank (FPS de produção ainda não definido, CLAUDE.md, 14.5).

## Riscos

- **Fatos**: só o que está na fala. A bênção de 10/06/2026 foi conferida na web (`creditos.md`). A foto da missa é do dia da bênção; a torre vista por fora é do acervo, de março/2026.
- **Foto c. 1915** no fundo do "1/4": é do canteiro em vida de Gaudí, não do dia da morte. Não aparece data na tela.
- **Duração de 44,8 s**: acima dos 7–30 s da referência de conteúdo (3.1), como o Anne Frank. Se a retenção cair, a próxima versão pode tirar a parte 6 (≈ 2,6 s) ou 3–4 (uma variável por teste, 8.3).

## Como refazer

```bash
cd reel_gaudi
# brutos (fora do git): as 7 tomadas da pasta Barcelona › Reels › Gaudi e o trecho do master
python3 scripts/trecho_drive.py 1caei0riSf82pYiGAhi_Zuhp6ByJLdi5k fonte/acervo/master_barcelona.mov 1410 1620
python3 scripts/reel.py tudo      # preparar → render → master → capa → quadros
python3 scripts/conferir.py       # conferência medida → qa/conferencia.json
```

O `preparar` imprime o comando de download de cada tomada que faltar. Requer ffmpeg, Node (Remotion em `design-system/remotion`, `npm install`), Python com numpy, scipy, soundfile e Pillow, e faster-whisper/torch só para `alinhar.py` e `conferir.py`.
