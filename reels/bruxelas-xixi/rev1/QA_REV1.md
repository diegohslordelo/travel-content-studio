# QA · REV1 · "Bruxelas tem 3 estátuas fazendo xixi"

**Veredito: ajustar. Falta a narração do Diego.** A edição, a capa e a legenda do post estão prontas, e o pipeline já encaixa a voz. Com o áudio, são cerca de 5 min até o arquivo final: alinhar, renderizar, master e capa. Publicação prevista: **sexta, 16/10/2026, 19h00** (planejamento V5, `V5-20261016-BRU-xixi`).

| Item | Valor |
|---|---|
| Formato | Narração (voz em off do Diego) sobre o material de 15/03/2026. Texto em `ROTEIRO_NARRACAO.md` |
| Guia de leitura | `guia_narracao_rev1.mp4` (540 × 960, sem voz): edição completa, com as legendas nos tempos-guia, para gravar no ritmo |
| Arquivo final | `reel_bruxelas-xixi_rev1.mp4` · 1080 × 1920 · 30 fps · ≈ 21 s (sai depois da narração) |
| Capa | `capa_bruxelas-xixi_rev1.jpg` (1080 × 1920; no grid 3:4 a placa fica dentro do recorte, entre y 240 e 1680) |
| Áudio | voz −16 LUFS, ambiente −30 LUFS, master −14 LUFS e pico ≤ −1 dBTP (DS V2, 4.6). Medir no arquivo final |
| Nível de edição | B (DS V2, 5.2): 1 objeto de marca (Ticket `SABIA?`) no pico de utilidade + legenda Padrão com scrim + legenda Informação (contador) |
| Decisões | `rev1.json` · pipeline `rev1.py` · composição `Reel` em `design-system/remotion` (ganhou o Ticket nesta revisão) |
| Folha de quadros | `qa_frames/folha_rev1.jpg` (da guia) |

## Roteiro de cortes (tempos-guia; o corte acompanha a voz real)

| Tempo | Cena | Trecho do bruto | Narração | Na tela | Som |
|---|---|---|---|---|---|
| 0,00–2,60 | **gancho**: multidão fotografando o Manneken Pis no nicho | `IMG_2255` 0,00–2,60 s, recorte acompanhando o nicho (x 1272 → 792) | "Bruxelas tem três estátuas fazendo xixi." | "Bruxelas tem **3** estátuas" · "fazendo xixi" | ambiente −30 LUFS |
| 2,60–3,95 | Diego apontando, Marina ao lado | `IMG_2186` 2,00–3,33 s, girado 180°, recorte x 966 | "A primeira é um cachorro." | Informação `15/03 · 13H16` / `1/3` | — |
| 3,95–6,40 | Snap → **Zinneke Pis**, da cabeça até a perna levantada | `IMG_2187` 0,30–2,77 s, panorâmica x 240 → 1600 | "Perna levantada desde noventa e nove." | "perna levantada desde **1999**" | obturador −12 dB da voz |
| 6,40–10,20 | **Jeanneke Pis** agachada no nicho | `IMG_2224` 0,00–3,80 s, recorte x 1592, Ken Burns | "A segunda é uma menina, num beco. Agachada desde oitenta e sete." | `15/03 · 14H24` / `2/3` · "num beco, / agachada desde **1987**" | — |
| 10,20–11,55 | Diego acenando na multidão, Marina ao lado | `IMG_2258` 0,90–2,23 s, girado 180°, recorte x 560 → 760 | "E a terceira é a famosa:" | `15/03 · 16H12` / `3/3` | — |
| 11,55–13,70 | Snap → **Manneken Pis** de jogador de futebol (close) | `IMG_2253` 0,00–2,17 s, recorte x 1178 | "faz xixi desde mil seiscentos e dezenove." | "faz xixi desde **1619**" | obturador −12 dB · ambiente −30 LUFS |
| 13,70–16,45 | Manneken Pis, close vertical | `IMG_2251` 0,20–2,97 s, Ken Burns | "Tem mais de mil roupas. Mais roupa que eu." | "tem mais de mil roupas" · "mais roupa que eu" | ambiente −30 LUFS |
| 16,45–21,00 | **fim**: a multidão do gancho de novo | `IMG_2255` 3,20–7,73 s, recorte x 600 → 0 | "Dá pra ver as três a pé, numa tarde. Salva pro seu roteiro de Bruxelas." | Ticket `SABIA?` / `ZINNEKE · JEANNEKE · MANNEKEN` (18,35–20,65 s) | — |
| 21,00 → 0,00 | loop: multidão → mesma multidão no gancho | — | — | — | — |

**Som dos brutos:** as selfies (`IMG_2186`, `IMG_2258`), o cachorro (`IMG_2187`, Diego falando atrás da câmera) e a menina (`IMG_2224`, alguém gritando "7 de julho!", segundo a transcrição) ficam mudos para a fala original não brigar com a narração. Ambiente só onde não há fala no trecho: o gancho e os dois planos do Manneken Pis. No fim, o ambiente também fica mudo, porque em 3,6–4,6 s do `IMG_2255` alguém fala "Dá tchau aqui!".

## Verificação dos fatos (CLAUDE.md, 9)

| Na narração ou na tela | Fonte | Situação |
|---|---|---|
| Cachorro "desde 1999" | visit.brussels: o Zinneke "anda pelas ruas da capital desde 1999", na Rue des Chartreux | ✅ Fonte oficial de turismo. A Wikipédia e alguns guias dizem 1998; vale o visit.brussels |
| Menina "desde 1987", "num beco" | visit.brussels: apresentada ao público em 1987, no Impasse de la Fidélité (impasse = beco sem saída) | ✅ |
| Menino "faz xixi desde 1619" | visit.brussels: Jérôme Duquesnoy fez a estátua de bronze em 1619 | ✅ Com ressalva: a estátua da fonte é uma reprodução, e a original fica na Maison du Roi. "Faz xixi desde 1619" vale para o Manneken Pis, não para a peça de bronze que está na rua. A ressalva está no comentário para fixar (`legenda_post.md`) |
| "Mais de mil roupas" | Regulamento da Cidade de Bruxelas (mannekenpis.brussels): 1.141 roupas no fim de 2023; visit.brussels: 1.000 peças | ✅ O PDF do regulamento devolveu 403 na leitura direta; o número veio do resumo da busca. bruxelles.be ainda diz "mais de 900" (página desatualizada) |
| "Dá pra ver as três a pé, numa tarde" | GPS e hora dos próprios vídeos: cachorro 13h16 (50,8487 · 4,3457), menina 14h24 (50,8485 · 4,3540), menino 16h12 (50,8450 · 4,3499) | ✅ ≈ 580 m e ≈ 480 m em linha reta entre elas. Entre uma e outra houve almoço, Grand-Place e waffle, por isso a tarde inteira |
| Contadores `13H16`, `14H24`, `16H12` | Hora de criação dos arquivos (+01:00) mais o início do trecho: `IMG_2186` 13:16:51 + 2,0 s; `IMG_2224` 14:24:58; `IMG_2258` 16:12:06 + 0,9 s | ✅ Planejamento dizia 14h25 (da selfie `IMG_2225`, fora do corte) |
| Nomes no Ticket | visit.brussels: Manneken-Pis, Jeanneke-Pis, Zinneke-Pis | ✅ |

**Legenda × fala:** os anos são falados curtos ("desde noventa e nove", "desde oitenta e sete") e escritos inteiros na legenda (**1999**, **1987**). É a única diferença proposital entre o que se ouve e o que se lê, para o número no Destaque ficar inequívoco.

## Narração: o que falta e como entra

1. O Diego grava o texto de `ROTEIRO_NARRACAO.md` (≈ 21 s, uma tomada) e manda o arquivo.
2. `python3 rev1.py narracao <arquivo>`: copia para `../narracao/`, transcreve com faster-whisper large-v3 (tempo por palavra), alinha ao texto do `rev1.json` e grava `narracao_alinhada.json`. Mostra as **diferenças** entre o roteiro e o que foi dito: se ele trocar uma palavra, o `texto` da fala no `rev1.json` é corrigido para a legenda seguir o áudio.
3. `python3 rev1.py tudo`: cada cena passa a começar 0,10 s antes da fala que a ancora; a voz entra com a 1ª palavra em 0,20 s; o Ticket entra 0,40 s antes de "Salva…" e fica 2,9 s; o Reel termina 0,6 s depois da última palavra.

**Teste do alinhamento (16/10/2026):** rodado sobre a fala real do Diego no `IMG_2258` (0–8,5 s, com e sem 0,8 s de silêncio na frente). As 3 frases de teste foram encontradas palavra a palavra, e a 1ª palavra caiu em 1,04 s no arquivo com silêncio (o Whisper sozinho marcava 0,00 s; o início vem da energia do sinal). As palavras que faltavam no áudio foram listadas como diferença, como esperado.

**Validação humana (CLAUDE.md, 12):** o Claude não escuta áudio. Depois do render final, o Diego confere no ouvido: (1) a voz clara do início ao fim; (2) os 2 obturadores (≈ 3,9 s e ≈ 11,5 s) sem incomodar (sons v1 sintetizados, ninguém ouviu); (3) se a legenda bate com o que ele falou.

## Conformidade com o DS V2 (7.3, Nível B)

| Item | Situação |
|---|---|
| Só tokens oficiais | ✅ Valores lidos de `primeiro-dia-tokens-v2.json` pelo Remotion; nenhum valor novo |
| 1 objeto de marca na posição fixa, no pico | ✅ Ticket `SABIA?` (DS 2.6, Curiosidade) na zona de objeto (x 72 · y 900), no pico de utilidade (os 3 nomes para salvar), Subida curta, 2,3–2,9 s na tela, sai subindo antes do loop |
| Carimbo, ticket e bilhetes | ✅ 1 ticket, nenhum carimbo, nenhum bilhete |
| Legendas | ✅ Scrim sempre ligado · ≤ 2 linhas · ≤ 26 caracteres por linha (o `rev1.py` recusa acima disso) · ≤ 6 palavras por grupo · linha de cima ≤ a de baixo · 1 Destaque por grupo, ≥ 3 s entre Destaques (o `rev1.py` tira o que ficar mais perto) · grupo inteiro (fala > 3 palavras/s, freio 4 da 3.3) · centradas em x 540 · minúsculas, sem emoji |
| Informação | ✅ 1 dado por etiqueta (contador `1/3`, `2/3`, `3/3` com hora real), x 72, acima da legenda |
| Transições | ✅ 1 família (Snap, lista de 3), 2 transições: no 1º e no último item, com obturador só neles (DS 4.6). 6 de 8 cortes secos (75%) |
| Efeitos simultâneos | ✅ Máximo 3: grão + Ken Burns (menina, close vertical) ou grão + flash + zoom do Snap (o close do Snap ficou sem Ken Burns por isso) |
| UI do Instagram | ✅ Nada essencial no topo (0–256), na base (1440–1920) nem na direita (944–1080). Ticket (girado +4°) de x ≈ 60 até ≈ x 890 |
| Valores com € e R$ | ➖ Não há valor nesta peça |
| Som | ✅ Só `PD_obturador` nos 2 Snaps (≈ 7,6 s entre eles); Ticket `SABIA?` sem som, porque não tem estrela para furar (a 4.6 liga o *ding* ao furo) · master a medir no final |
| Teste de miniatura | ✅ Capa a 25% (270 × 480): "3 ESTÁTUAS" legível; o "XIXI EM BRUXELAS" (rótulo, 27 px) some a 10%, como todo rótulo |
| Hook | ✅ 6 palavras escritas (máx. 7, DS 5.1), sem saudação, logo ou vinheta; é o gancho do planejamento |
| Bordão e placa de fechamento | ➖ Não se aplica (Nível B, curiosidade) |
| Teste dos 3 segundos | ⚠️ Nos 3 primeiros segundos há legenda com Destaque (mini-placa) e o contador de papel aos 2,7 s, mas não a Placa: o objeto de marca é o Ticket do fim. É o que o Nível B e o planejamento pedem; a capa leva a Placa |

## Critérios de qualidade (CLAUDE.md, 8)

| # | Critério | Situação |
|---|---|---|
| 1 | Gancho forte | ✅ Quadro 0 na multidão fotografando o nicho, com a afirmação que ninguém espera ("3 estátuas") |
| 2 | Uma ideia central | ✅ "Bruxelas tem 3 estátuas fazendo xixi, e dá pra ver as 3 a pé numa tarde." |
| 3 | Funciona sem som | ✅ Legenda em toda a narração + contador `1/3 · 2/3 · 3/3` |
| 4 | Motivo de envio ou salvamento | ✅ Salvar: os 3 nomes no Ticket e os endereços na legenda. Envio: "você sabia que tinha 3?" para quem vai à Bélgica |
| 5 | Valor ou emoção | ✅ Curiosidade com humor (a série de anos "desde 99, desde 87, desde 1619" e o "mais roupa que eu") |
| 6 | Marca reconhecível | ✅ Ticket `SABIA?` no pico de utilidade + etiqueta de papel (Informação) + mini-placa no Destaque |
| 7 | Conformidade DS V2 | ✅ Tabela acima |
| 8 | Identidade verbal | ✅ Direto e bem-humorado sem ser palhaço: a piada está nos fatos (anos, roupas), não em exagero. Números exatos |
| 9 | Originalidade | ✅ Material próprio, sem marca d'água |
| 10 | Formato e duração | ⚠️ ≈ 21 s; o planejamento previa 16–20 s. A narração precisa de ≈ 1 s a mais; continua dentro de 7–30 s (referência de conteúdo, 3.1) |

## Decisões desta revisão (valem só para este Reel)

- **Narração em vez da fala original** (pedido do Diego, 16/10/2026). A fala gravada na hora fica muda; só entra ambiente onde não há fala.
- **Tom cômico, com vontade de ir:** a piada é a sequência de anos, contada séria ("perna levantada desde 99", "agachada desde 87", "faz xixi desde 1619"), e o "mais roupa que eu". A vontade de ir vem do fecho: as 3 cabem numa tarde a pé, no centro.
- **Estrutura "apresenta → revela":** Diego apresenta (cachorro, a famosa) e o Snap corta para a estátua, como quem tira a foto. Na menina não há selfie boa (`IMG_2225` é um close cortando a testa): a cena é só a estátua, com corte seco.
- **Manneken Pis em close (`IMG_2253`) e não no plano aberto (`IMG_2254`):** no aberto, a estátua fica embaixo do quadro e a legenda a cobria.
- **Fim na mesma multidão do gancho:** o corte seco do fim para o início fecha o loop no mesmo lugar.
- **Contador como legenda Informação** (planejamento: "1/3 · 13H16"): número `1/3` e hora no rótulo. Os nomes só aparecem no Ticket do fim (planejamento).
- **Capa:** a Placa pequena (M) `XIXI EM BRUXELAS` / `3 ESTÁTUAS` com o `?` no módulo, sobre a multidão (planejamento: "3 ESTÁTUAS" + "?"; o rótulo foi acrescentado para a capa se explicar sozinha). A placa fica acima do Manneken, sem cobri-lo.
- **Clipes deitados:** `IMG_2186` e `IMG_2258` foram filmados na horizontal com metadado de retrato (−90); o `rev1.py` gira 180° sobre a rotação automática (`girar: 180`), como no MAD-show.
- **HLG → SDR:** todos os clipes são HDR (HLG) do iPhone; mesma conversão Möbius do MAD-show REV1. A luz estourada da selfie do cachorro (sol de frente) é a real.
- **30 fps:** o FPS de produção não está definido (CLAUDE.md, pendência 5); 30 é o das receitas do DS.
- **Remotion:** a composição `Reel` ganhou o Ticket (prop `ticket`) e passou a usar a voz como referência dos sons quando há voz tocando (antes, o obturador numa cena muda ficaria −12 dB do ambiente, 14 dB abaixo do que a 4.6 manda). O MAD-show REV1 não muda: os sons dele caem nos mesmos casos de antes.

## Riscos

- **Prazo:** o arquivo final depende da voz. Sem ela até ≈ 18h30, não dá para publicar às 19h00 com folga para a escuta.
- **"Desde 1619":** quem conhece a história pode comentar que a estátua da rua é réplica. É verdade, e é bom comentário: a resposta está pronta no comentário para fixar.
- **Zinneke 1998 × 1999:** se alguém corrigir para 1998, a fonte usada é o site oficial de turismo (visit.brussels, "desde 1999").
- **Rostos de terceiros:** turistas aparecem de costas e de lado na multidão, sem destaque, como em qualquer plano de rua.

## Como refazer

```bash
cd reels/bruxelas-xixi/rev1
python3 rev1.py narracao ../narracao/<arquivo>   # precisa de faster-whisper (pip install faster-whisper)
python3 rev1.py tudo                              # preparar → render → master → capa → folha
```

Sem `narracao_alinhada.json`, o `tudo` refaz a guia de leitura. Os brutos ficam em `../fonte/` (fora do git); se faltarem, o `preparar` imprime o comando de download de cada um pelo ID do Drive.
