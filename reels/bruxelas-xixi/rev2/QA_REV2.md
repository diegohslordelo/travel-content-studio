# QA · REV2 · "Bruxelas tem 3 estátuas fazendo xixi" (narração do Diego)

**Veredito: pronto para postar, depois de 1 escuta do Diego** (itens em "Conferir no ouvido"). Planejamento V5 `V5-20261016-BRU-xixi`, previsto para 16/10/2026, 19h00. Esse horário passou; a nova data é decisão do Diego (o planejamento só muda a pedido dele).

| Item | Valor |
|---|---|
| Arquivo final | `reel_bruxelas-xixi_rev2.mp4` · 1080 × 1920 · 30 fps · 25,7 s · H.264 + AAC 320 kbps |
| Prévia leve | `reel_bruxelas-xixi_rev2_previa.mp4` (540 × 960) |
| Capa | `capa_bruxelas-xixi_rev2.jpg` (a mesma da rev1: Placa M `XIXI EM BRUXELAS` / `3 ESTÁTUAS` + `?` sobre a multidão) |
| Áudio | voz −16 LUFS, ambiente −30 LUFS · master −14,0 LUFS integrados, pico verdadeiro −1,4 dBTP (DS V2, 4.6) · nenhum trecho em silêncio digital (nenhuma janela de 0,1 s abaixo de −60 dBFS) |
| Narração | 5 tomadas do Diego (`../narracao/originais/`, sem tomada 4), emendadas em `../narracao/narracao_rev2.wav` (24,85 s) |
| Nível de edição | B (DS V2, 5.2): 1 objeto de marca (Ticket `SABIA?`) + legenda Padrão com scrim + legenda Informação (contador) |
| Decisões | `rev2.json` · pipeline `rev2.py` · composição `Reel` em `design-system/remotion` |
| Folha de quadros | `qa_frames/folha_rev2.jpg` |

## O que mudou da rev1

A rev1 era a guia de leitura do roteiro proposto. O Diego gravou outro texto, e a edição foi refeita em cima dele:

| rev1 (roteiro proposto) | rev2 (narração gravada) |
|---|---|
| "Bruxelas tem três estátuas fazendo xixi." | "Você sabia que Bruxelas tem três pontos turísticos inusitados?" |
| "Agachada desde 87." | "…e tá fazendo agachamento desde 1987." |
| "faz xixi desde 1619 · mais de mil roupas · mais roupa que eu" | "Reza a lenda que esse menino salvou a cidade fazendo xixi em uma bomba." |
| "Dá pra ver as três a pé, numa tarde." | "E o melhor é que dá pra ver as três em uma tarde." |
| 8 cenas, 21 s | 10 cenas, 25,7 s: **entram** o Diego na rua do beco (`IMG_2226`, para "que fica num beco") e Diego e Marina rindo na rua de sol (`IMG_2188`, para "o melhor… em uma tarde") |

## Narração: transcrição e montagem

**Transcrição** (CLAUDE.md, 10: retranscrever e não declarar validação auditiva). 3 modelos Whisper em cada tomada, sem texto de dica:

| Tomada | Texto usado na legenda | Divergência entre os modelos |
|---|---|---|
| 1 | Você sabia que Bruxelas tem três pontos turísticos inusitados? | Nenhuma |
| 2 | São três estátuas fazendo xixi e a primeira é um cachorro que **tá** com a perna levantada desde **99**. | large-v3 e turbo: "que **está** com… desde 1999"; medium: "que **tá** com… desde **99**". "Está" dura 0,12 s no large-v3 (curto demais para 2 sílabas) e o alinhamento com o texto ouviu "tá": ficou **"tá"** |
| 3 | A segunda é uma menina que fica num beco e tá fazendo agachamento desde 1987. | Nenhuma |
| 5 | E a terceira é a mais famosa, o Manneken Pis. Reza a lenda que esse menino salvou a cidade fazendo xixi em uma bomba. | medium: "E a terceira, a mais famosa"; turbo: "fazendo **um** xixi". Ficou a maioria (2 de 3) nos dois casos. "Mannequin Peace/Piece" é a pronúncia: a legenda escreve o nome certo, Manneken Pis |
| 6 | E o melhor é que dá pra ver as três em uma tarde. Já salva pro seu roteiro de Bruxelas. | large-v3 ouviu "às três e uma à tarde"; turbo e medium: "as três em uma tarde" (ficou este) |

**Montagem** (`rev2.py montar`): cada tomada é cortada 60 ms antes do começo da fala até 80 ms depois do fim (energia do sinal), igualada a −18 LUFS, e a pausa até a próxima tomada é o som de sala da própria gravação, não silêncio digital: 0,30 s depois da pergunta, 0,45 s depois de "desde 99" e de "desde 1987" (a piada respira), 0,40 s antes de "E o melhor". O ruído de fundo das tomadas é baixo (−48 a −55 dBFS).

**Alinhamento** (`rev2.py narracao`): Whisper large-v3 com tempo por palavra; 100% das palavras de cada fala encontradas. Correções feitas pelo próprio script: o começo de cada tomada vem da montagem (o Whisper encostava "A segunda" e "E a terceira" na tomada anterior, até 1,7 s antes); o fim de cada fala vai até o fim da voz contínua (ele encurtava "mil novecentos e oitenta e sete" para 0,5 s); o que ele "ouve" depois que a voz acaba é descartado. Ele escreveu um "Tchau, tchau" em cima do fim de "Bruxelas" (24,6 s): os outros modelos não ouviram, é alucinação típica de fim de áudio, e a legenda não usa.

### Conferir no ouvido (≈ 1 min)

O Claude não escuta áudio: a validação auditiva é humana (CLAUDE.md, 12).

1. **3,5 s:** a tomada 2 começa com a fala já no 1º instante do arquivo. O "São" está inteiro ou foi cortado na gravação?
2. **6,4 s:** "que **tá** com a perna" ou "que **está** com"? (a legenda diz "tá")
3. **7,9 s:** você fala "noventa e nove" ou "mil novecentos e noventa e nove"? A legenda escreve **1999** nos dois casos.
4. **Emendas** (nas pausas de ≈ 3,4 s, 8,9 s, 14,2 s e 20,6 s): a passagem de uma tomada para a outra soa natural (respiração, tom de voz)?
5. **Mixagem:** a voz clara do começo ao fim; os 2 obturadores (6,4 s e 15,6 s) sem incomodar (sons v1 sintetizados, ninguém ouviu); a multidão voltando nos últimos ≈ 2 s e emendando no gancho.

Se algum texto estiver errado: corrigir `fala` e `texto` no `rev2.json` e rodar `rev2.py narracao`, `rev2.py tudo`.

## Roteiro de cortes

| Tempo | Cena | Trecho do bruto | Narração | Na tela | Som |
|---|---|---|---|---|---|
| 0,00–3,53 | **gancho**: multidão fotografando o Manneken Pis | `IMG_2255` 0,00–3,53 s, recorte acompanhando o nicho | "Você sabia que Bruxelas tem três pontos turísticos inusitados?" | "você sabia que / Bruxelas tem **3**" · "pontos turísticos / inusitados?" | ambiente −30 LUFS |
| 3,55–6,42 | Diego apontando, Marina ao lado | `IMG_2186` 1,80–4,70 s, girado 180° | "São três estátuas fazendo xixi e a primeira é um cachorro" | "são 3 estátuas / fazendo xixi" · "e a primeira / é um cachorro" | — |
| 6,42–9,09 | Snap → **Zinneke Pis**, da cabeça até a perna levantada | `IMG_2187` 0,30–2,97 s, panorâmica | "que tá com a perna levantada desde 99." | `15/03 · 13H17` / `1/3` · "que tá com / a perna levantada" · "desde **1999**" | obturador −12 dB da voz |
| 9,09–10,83 | Diego na rua estreita ao lado do beco | `IMG_2226` 7,50–9,23 s, girado 180° | "A segunda é uma menina que fica num beco" | "a segunda é uma menina" · "que fica num beco" | — |
| 10,83–14,38 | **Jeanneke Pis** agachada (o corte cai em "agachamento") | `IMG_2224` 0,00–3,53 s, Ken Burns | "e tá fazendo agachamento desde 1987." | `15/03 · 14H24` / `2/3` · "e tá fazendo agachamento" · "desde **1987**" | — |
| 14,38–15,60 | Diego acenando na multidão, Marina ao lado | `IMG_2258` 0,90–2,13 s, girado 180° | "E a terceira é a mais famosa," | "e a terceira / é a mais famosa" | — |
| 15,60–17,88 | Snap → **Manneken Pis** de jogador de futebol (close) | `IMG_2253` 0,00–2,27 s | "o Manneken Pis. Reza a lenda que esse menino" | `15/03 · 16H09` / `3/3` · "o Manneken Pis" · "reza a lenda / que esse menino" | obturador −12 dB · ambiente −30 LUFS |
| 17,88–20,79 | Manneken Pis, close vertical | `IMG_2251` 0,20–3,13 s, Ken Burns | "salvou a cidade fazendo xixi em uma bomba." | "salvou a cidade" · "fazendo xixi / em uma **bomba**" | ambiente −30 LUFS |
| 20,79–22,76 | Diego e Marina rindo numa rua de sol | `IMG_2188` 21,60–23,57 s, girado 180° | "E o melhor é que dá pra ver as três em uma tarde." | "e o melhor é que / dá pra ver as 3" · "em uma tarde" | — |
| 22,76–25,70 | **fim**: a multidão do gancho | `IMG_2255` 3,60–6,53 s | "Já salva pro seu roteiro de Bruxelas." | Ticket `SABIA?` / `ZINNEKE · JEANNEKE · MANNEKEN` (23,01–25,36 s) · "já salva" · "pro seu / roteiro de Bruxelas" | ambiente da multidão a partir de 23,76 s (entra em 0,4 s) |
| 25,70 → 0,00 | loop: multidão → mesma multidão no gancho | — | — | — | o ambiente emenda |

**Som dos brutos:** ficam mudos os clipes com fala gravada no trecho (as selfies `IMG_2186`, `IMG_2226`, `IMG_2258` e `IMG_2188`, e o cachorro `IMG_2187`, com Diego falando atrás da câmera) e a menina (`IMG_2224`: um modelo ouviu "Obrigado", outro "7 de julho", ambos com baixa confiança; na dúvida, mudo). No fim, o ambiente entra depois do "Dá tchau aqui" que existe em 3,48–4,32 s do `IMG_2255`.

## Verificação dos fatos (CLAUDE.md, 9)

| Na narração ou na tela | Fonte | Situação |
|---|---|---|
| Cachorro "desde 1999" | visit.brussels: o Zinneke "anda pelas ruas da capital desde 1999", na Rue des Chartreux | ✅ Alguns guias e a Wikipédia dizem 1998; vale a fonte oficial de turismo |
| Menina "num beco", "desde 1987" | visit.brussels: apresentada ao público em 1987, no Impasse de la Fidélité (impasse = beco sem saída) | ✅ |
| "Reza a lenda que esse menino salvou a cidade fazendo xixi em uma bomba" | visit.brussels: entre "muitas lendas", a "mais comum" é a de um menino que, com a cidade cercada e sem água por perto, apagou com xixi o pavio aceso pelos invasores | ✅ Contada como lenda ("reza a lenda"). "Bomba" simplifica "pavio de uma carga de explosivos": a versão exata está no comentário para fixar (`legenda_post.md`) |
| "Três pontos turísticos" | visit.brussels trata as três como atrações (Manneken-Pis, Jeanneke-Pis, Zinneke-Pis) | ✅ |
| "Dá pra ver as três em uma tarde" | GPS e hora dos próprios clipes: cachorro 13h17, menina 14h24, menino 16h09, todos em 15/03; ≈ 580 m e ≈ 480 m em linha reta entre eles | ✅ |
| Contadores `13H17`, `14H24`, `16H09` | Hora de criação dos clipes das estátuas (+01:00): `IMG_2187` 13:17:14 + 0,3 s; `IMG_2224` 14:24:58; `IMG_2253` 16:09:52 (`IMG_2251`, o 2º plano, 16:09:06) | ✅ Mudou da rev1 (que usava a hora das selfies) para a hora da própria estátua |
| Nomes no Ticket | visit.brussels | ✅ O `SABIA?` responde ao "Você sabia…?" do gancho |

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion; nenhum valor novo |
| 1 objeto de marca na posição fixa, no pico | ✅ Ticket `SABIA?` na zona de objeto (x 72 · y 900) no pico de utilidade (os 3 nomes para salvar), 2,35 s na tela, sai subindo 0,34 s antes do loop |
| Carimbo, ticket e bilhetes | ✅ 1 ticket |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha · 1 Destaque por grupo (**3**, **1999**, **1987**, **bomba**), ≥ 4 s entre eles · grupo inteiro (fala > 3 palavras/s) · centradas em x 540 · ⚠️ 3 exceções registradas abaixo |
| Informação | ✅ Contador `1/3`, `2/3`, `3/3` com a hora real, entrando junto com a estátua |
| Transições | ✅ 1 família (Snap) no 1º e no último item da lista, com obturador só neles (4.6); 7 de 9 cortes secos (78%) |
| Efeitos simultâneos | ✅ Máximo 3 (grão + flash + zoom do Snap; grão + Ken Burns) |
| UI do Instagram | ✅ Nada essencial no topo (0–256), na base (1440–1920) nem na direita (944–1080) |
| Som | ✅ Só `PD_obturador` nos 2 Snaps (9,2 s entre eles) · master −14,0 LUFS e −1,4 dBTP |
| Teste de miniatura | ✅ Capa legível a 25% |
| Hook | ⚠️ Falado em 9 palavras ("Você sabia que Bruxelas tem três pontos turísticos inusitados?"); o DS 5.1 pede até 7 no hook **escrito**. Aqui não há hook escrito à parte: a legenda transcreve a fala, em 2 grupos de 6 e 3 palavras. Tipo de hook: pergunta direta (referência 3.3) |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B) |

**Exceções de legenda (só neste Reel):**
1. "pontos turísticos / inusitados?" e "são 3 estátuas / fazendo xixi": a linha de cima ficou maior que a de baixo (3.1). A alternativa seria quebrar "pontos / turísticos" e "3 / estátuas", e a regra "nunca no meio de expressão" pesa mais.
2. "e o melhor é que / dá pra ver as 3": 9 palavras num grupo (3.1 pede 2 a 6). A fala aqui é rápida: separado, "e o melhor é que" ficaria 0,4 s na tela, um piscar ilegível.

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Pergunta direta sobre a multidão fotografando o nicho; a resposta ("estátuas fazendo xixi") vem em 3,5 s |
| 2 | Uma ideia central | ✅ "Bruxelas tem 3 estátuas fazendo xixi, e dá pra ver as 3 numa tarde." |
| 3 | Funciona sem som | ✅ Legenda em toda a narração + contador |
| 4 | Motivo de envio ou salvamento | ✅ Salvar (3 nomes no Ticket, endereços na legenda) · enviar ("você sabia?") |
| 5 | Valor ou emoção | ✅ Curiosidade com humor: o "agachamento" em cima da estátua agachada, a lenda da bomba |
| 6 | Marca reconhecível | ✅ Ticket `SABIA?` (que fecha o "Você sabia?" do gancho) + etiqueta de papel + mini-placa |
| 7 | Conformidade DS V2 | ✅ com as exceções registradas |
| 8 | Identidade verbal | ✅ Direto, curioso e bem-humorado, na voz do próprio Diego |
| 9 | Originalidade | ✅ Material e voz próprios, sem marca d'água |
| 10 | Formato e duração | ⚠️ 25,7 s; o planejamento previa 16–20 s. É o tempo da narração gravada (24,9 s); continua dentro de 7–30 s (referência 3.1) |

## Decisões desta revisão (valem só para este Reel)

- **Estrutura "apresenta → revela" nas 3 estátuas:** o Diego apresenta em cena e o corte mostra a estátua na palavra-chave. Cachorro e Manneken com Snap e obturador (1º e último item); menina com corte seco caindo em "agachamento".
- **Cenas novas:** `IMG_2226` (14h26, a ≈ 35 m da Jeanneke pelo GPS) para "que fica num beco", e `IMG_2188` (13h17, Diego e Marina rindo na rua de sol, a caminho das outras duas) para "o melhor… em uma tarde". Nenhuma cena encenada da lenda: ela é contada sobre o próprio Manneken Pis.
- **Loop no som e na imagem:** o fim volta à multidão do gancho, com o ambiente real entrando nos últimos ≈ 2 s.
- **Sem silêncio digital:** as pausas entre as tomadas são o som de sala da gravação do Diego.
- Mantidos da rev1: recortes, HLG → SDR (Möbius), 30 fps, capa, Ticket, Snap, ambiente a −30 LUFS só onde o bruto não tem fala.

## Riscos

- **Horário:** o slot de 16/10, 19h00, passou.
- **"Bomba":** quem conhece a lenda pode corrigir para "pavio". A resposta está pronta no comentário para fixar.
- **Zinneke 1998 × 1999:** a fonte usada é o site oficial de turismo.
- **Rostos de terceiros:** turistas de costas e de lado na multidão, sem destaque.

## Como refazer

```bash
cd reels/bruxelas-xixi/rev2
python3 rev2.py montar      # numpy
python3 rev2.py narracao    # faster-whisper (pip install faster-whisper)
python3 rev2.py tudo        # preparar → render → master → capa → folha
```

Os brutos ficam em `../fonte/` (fora do git); se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
