# QA · Reel "Paris não quer você lá" · REV1

**Entrega:** `reel_paris-formigueiro_rev1.mp4` · capa `capa_paris-formigueiro_rev1.jpg` · legenda do post em `legenda_post.md` · créditos em `creditos.md`.
**Pedido do Diego (07/11/2026):** montar o Reel do roteiro v1 (`../ROTEIRO_v1.md`) com as tomadas da pasta do Drive `Youtube/Paris/Reel`. As cenas de cima ilustram a fala ("se falo que tá cheio, imagem cheia; cidade dourada, sol batendo bonito"). Gancho como o de Bruges, com policial, Torre Eiffel e fita zebrada; depois tela cheia em "pelo menos…"; o Diego aponta para cima e o print do ranking cai na tela dividida. Imersivo, animações para construir a fala, **cada imagem 3 s na tela**, acervo quando for muito bom e internet quando não.

**Veredito do Claude:** pronto para a escuta do Diego. Há 3 pontos de conteúdo para ele decidir antes de postar (seção 7).

---

## 1. Fala gravada × roteiro v1

A fala gravada manda (FORMATOS_REELS 9.5). As 10 tomadas (IMG_7845 a IMG_7902) entram inteiras, na ordem do roteiro, cortadas só no silêncio, sem acelerar.

| Bloco | Roteiro v1 | Fala gravada | Efeito na edição |
|---|---|---|---|
| 1 | Paris não quer você lá. Pelo menos, não se você for igual a todo mundo. | Igual (2 tomadas: IMG_7887, IMG_7888) | — |
| 2 | Hospedagem a 514 € (junho de 2025), pressa, tudo cheio, restaurante caro | **Novo:** "Segundo esse ranking aqui do Euromonitor, Paris é o primeiro destino no mundo pelo quinto ano seguido. Você tem ideia do que isso faz com a cidade?" + "Hospedagem cara, pontos turísticos e restaurantes lotados, isso atrapalha a sua experiência e ainda dói na conta bancária." | Sem "514 €/noite" e sem "11 milhões · Notre-Dame" na tela: não foram ditos (regra: nada na tela que não esteja na fala). Entrou o print da Euromonitor |
| 3 | "Eu sei porque fiz assim. Passei dois dias correndo…" | **Não gravado** | A pendência 1 do roteiro (1 ou 2 dias) deixa de existir neste Reel |
| 4 | Mas dá pra fazer diferente. Três pulos do gato… | "Agora, cá entre nós, dá pra fazer diferente, né? Eu vou te dar três pulos do gato pra você não se apertar em Paris." | — |
| 5.1 | Fique no mínimo quatro dias… cada rua dourada da cidade. | "Um, fique no mínimo quatro dias. Você vai querer se encantar com calma de cada rua dourada em Paris." | — |
| 5.2 | Coma num bouillon. No Chartier, a entrada começa em 1 euro. | "Dois, come um bouillon, você vai comer uma comida francesa e ainda vai pesar menos no bolso." | Sem "1 €" na tela. O Chartier aparece na imagem, sem nome escrito |
| 5.3 | Durma no 9º distrito, perto de uma estação de metrô… | "E três, escolha o nono distrito. Você vai estar num bairro mais calmo e ainda assim muito bem localizado." | Sem metrô. **"Mais calmo"** foi dito (ver seção 7) |
| 6 | Assim você curte a Madame Paris, apesar do formigueiro. | "Desse jeito você curte a Madame Paris apesar do formigueiro." | — |
| 7 | Me segue: aqui você descobre… | "E se você está planejando o seu primeiro dia na Europa, já acompanha aqui esse perfil, porque eu solto dica toda semana pra você não passar perrengue." | Placa do CTA tirada da fala: "ACOMPANHA AQUI / PRIMEIRO DIA →" |

- **Leituras automáticas conferidas:** Whisper large-v3 + alinhamento forçado (torchaudio MMS) em `transcricao_alinhada.json`. A tomada IMG_7878 saiu "E 3º e 9º distrito" na 1ª leitura; sem o texto de contexto o Whisper ouve "E três, escolha o nono distrito" (confiança ≥ 0,82 em "escolha" e 0,91 em "nono"). "Bouillon" sai "bulhão" no Whisper (normal para palavra francesa) e está escrito "bouillon" na legenda.
- **Duração:** voz 49,33 s; Reel 50,33 s (1 s de cauda no CTA). O roteiro pedia ordem de corte acima de 50 s; não foi preciso cortar nada: a fala gravada já veio sem o bloco 3.

## 2. Decupagem visual (cena por cena)

Todas as cenas ficam **3 s ou mais** na tela, com 2 exceções registradas no `cenas.json` (`min_excecao`), as duas por pedido direto do Diego: a abertura (2,70 s, o gancho, que emenda no empurrão de 0,63 s com a mesma foto ainda subindo, ou seja, 3,3 s visível) e o Diego em tela cheia depois dela (2,54 s), porque o print tem de cair **enquanto ele aponta para cima** (o gesto vai de 5,14 a 6,14 s; o print cai em 5,24 s). O `preparar.py` recusa a montagem se alguma cena ficar abaixo do mínimo.

| # | Tempo | Fala | Imagem (ilustra o quê) | Fonte | Composição | Entrada · som |
|---|---|---|---|---|---|---|
| 1 | 0,00–2,70 | Paris não quer você lá. Pelo menos… | Policial e viaturas à noite, Torre Eiffel acesa ao fundo; **fita zebrada** atravessa na palavra "lá" e a 2ª em "Pelo". Texto do gancho linha a linha: "PARIS / NÃO QUER / VOCÊ LÁ." (vermelho), depois "PELO / MENOS…" | Commons (CC BY 2.0) + fita desenhada | Tela dividida, Diego desde o 1º quadro | — |
| 2 | 2,70–5,24 | …não se você for igual a todo mundo. Segundo | Diego em tela cheia com a palavra-chave em dupla tipografia: "NÃO SE VOCÊ FOR / *igual a todo mundo*" | Gravação | Diego em tela cheia | **Empurrão** (pedido do Diego) · swish |
| 3 | 5,24–8,90 | esse ranking aqui do Euromonitor, Paris é o primeiro destino no mundo | O print da Euromonitor **cai** da parte de cima no instante em que o Diego aponta para cima (ele continua apontando embaixo), quica e assenta; em "primeiro", marca-texto em "Paris is crowned the world's leading city" e o "1º DESTINO NO MUNDO" entra | Print real + animação | Tela dividida | **Queda** · impacto no pouso |
| 4 | 8,90–13,47 | pelo quinto ano seguido. Você tem ideia do que isso faz com a cidade? | Champs-Élysées lotada; "5º ANO / SEGUIDO" sobe na palavra | Acervo IMG_2895 | Tela dividida | Zoom com desfoque · impacto em "quinto" |
| 5 | 13,47–16,50 | Hospedagem cara, pontos turísticos e restaurantes lotados | 3 cartões, cada um cai na sua palavra: hotel (Hôtel du Louvre à noite), Trocadéro cheio, terraços da Place du Tertre lotados | Commons + acervo IMG_2805 (quadro) | Animação na tela dividida (legenda desligada: os rótulos são a fala) | Corte seco · página no 1º cartão |
| 6 | 16,50–20,13 | isso atrapalha a sua experiência e ainda dói na conta bancária | Turista desanimado no meio da multidão diante da Mona Lisa; "DÓI NA / CONTA" (vermelho) | Commons (CC0) | Tela dividida | Corte seco · impacto em "dói" |
| 7 | 20,13–23,17 | Agora, cá entre nós, dá pra fazer diferente, né? Eu vou te dar | Diego em tela cheia, aproximação lenta | Gravação | Diego em tela cheia | **Clarão de volta** · impacto |
| 8 | 23,17–26,17 | três pulos do gato pra você não se apertar em Paris. Um, | Ilustração: telhados de Paris e a Torre em traço; um gato âmbar dá 3 pulos (1, 2, 3); "3 PULOS DO GATO" | Criada | Animação na tela dividida | Corte seco · swish no 1º pulo |
| 9 | 26,17–30,90 | fique no mínimo quatro dias. Você vai querer se encantar com calma de cada rua dourada em Paris. | Selo "1"; 4 folhas de calendário marcadas e "4 DIAS"; o calendário sai em "encantar" e fica o pôr do sol dourado do Jardim de Luxemburgo | Acervo IMG_3137 + animação | Tela dividida | **Luz de passagem** · ar longo |
| 10 | 30,90–35,17 | Dois, come um bouillon, você vai comer uma comida francesa e ainda vai pesar menos no bolso. | Selo "2"; salão do Bouillon Chartier; em "comida" funde para um bœuf bourguignon de lá | Commons (CC0) | Tela dividida | Chicote · swish |
| 11 | 35,17–38,17 | E três, escolha o nono distrito. Você vai estar num bairro mais calmo e ainda assim | Selo "3"; os 20 distritos se desenham e o 9º acende em âmbar; "9º DISTRITO" | Criada (dados MIT) | Animação na tela dividida | Corte seco · obturador em "nono" |
| 12 | 38,17–41,20 | muito bem localizado. Desse jeito você curte a Madame | Ópera Garnier e a cidade vistas do terraço das Galeries Lafayette (no 9º) | Acervo IMG_3062 | Tela dividida | **Mergulho** no 9º do mapa · ar longo |
| 13 | 41,20–44,23 | Paris apesar do formigueiro. E se você está planejando o seu primeiro dia na | A Torre Eiffel no céu azul; a câmera desce e revela a multidão do Trocadéro | Acervo IMG_2807 | Tela cheia | Corte seco |
| 14 | 44,23–50,33 | Europa, já acompanha aqui esse perfil, porque eu solto dica toda semana pra você não passar perrengue. | Torre acesa e brilhando + **placa do DS V2** "ACOMPANHA AQUI / PRIMEIRO DIA →" (Chegada + *clack*) | Acervo IMG_3171 + DS V2 | Tela cheia + CTA | **Luz de passagem** · ar longo · *clack* |

**Equilíbrio:** 14 cenas, média 3,6 s (a mais curta 2,54 s, a mais longa 6,10 s, o CTA). Tela dividida 9, tela cheia de apoio 2, Diego em tela cheia 2, CTA 1. Nunca 3 cenas seguidas da mesma composição de imagem; animações intercaladas com acervo e fotos.

**Transições (7, sempre ≥ 1,5 s entre elas):** empurrão (gancho → fala, pedido do Diego), queda (o print cai quando ele aponta), zoom (ranking → multidão), clarão (virada "cá entre nós"), luz de passagem (dica 1, o dourado; e CTA), chicote (dica 2), mergulho (o mapa entra no 9º e encontra a Ópera). As outras 6 trocas são corte seco. As transições nasceram do Reel (o dedo apontando, o mapa que vira o bairro), como pede a REFERENCIA_EDICAO_FORMATOS 3.2. Ficam abaixo dos 70% de cortes secos do DS 4.4, como no Reel de Bruges REV3 (pedido do Diego de transições profissionais); se preferir mais secos, os candidatos a virar corte seco são o zoom (4) e o chicote (10).

**Imagem que não engana (CLAUDE.md 9):**
- A **fita zebrada é desenho chapado** sobre a foto real (listras lisas, sem textura de foto), um elemento gráfico do gancho, e não algo que estava na cena. Na foto original já existe uma fita de isolamento vermelha e branca atrás das viaturas.
- Gato, calendário e mapa são traço e cor chapada: não se passam por foto.
- O print é a página real da Euromonitor, só recortada (do título à data).

## 3. Voz

Mesmo tratamento do Bruges REV3/REV4: cada tomada tratada sozinha (redução de ruído com perfil da própria tomada, equalização até o timbre da média, ganho até o mesmo loudness de fala) e compressor suave (2:1) na voz inteira. Medição completa em `voz_medicao.json`.

| Fala | Tomada | Loudness da fala (antes → depois) | Ruído abaixo da fala (antes → depois) |
|---|---|---|---|
| f1 | IMG_7887 | −15,3 → −15,1 | 61,3 → 57,1 dB |
| f2 | IMG_7888 | −12,2 → −15,4 | 61,9 → 62,2 dB |
| f3 | IMG_7845 | −22,4 → −14,9 | **33,2 → 41,9 dB** |
| f4 | IMG_7902 | −18,8 → −15,7 | 55,5 → 53,4 dB |
| f5 | IMG_7891 | −20,4 → −15,8 | 47,7 → 54,0 dB |
| f6 | IMG_7872 | −16,5 → −15,1 | 57,3 → 53,9 dB |
| f7 | IMG_7876 | −16,2 → −15,3 | 52,7 → 51,0 dB |
| f8 | IMG_7878 | −18,1 → −15,2 | 56,0 → 49,7 dB |
| f9 | IMG_7880 | −15,8 → −15,2 | 60,1 → 55,4 dB |
| f10 | IMG_7883 | −19,1 → −15,6 | 58,3 → 58,1 dB |

As 10 falas ficam dentro de 0,9 LU. **A tomada do ranking (IMG_7845) é diferente das outras:** chegou 7 dB mais baixa, com ruído de fundo só 33 dB abaixo da fala e +13 dB de agudo (2–8 kHz) em relação à média; a equalização tem limite de ±5 dB e ela continua ≈ 5–8 dB mais brilhante. Provavelmente foi gravada com o celular mais longe (ele aponta para cima e mexe o braço). Ver "Conferir no ouvido".

## 4. Identidade visual

- **Do gancho até antes do CTA:** linguagem do formato tela dividida (FORMATOS_REELS): Anton, Inter 800, destaque âmbar `#E0AE5C`, grão 6%, fundo `#14120F`, serifa itálica Cormorant Garamond na palavra-chave (como no Bruges). Nenhum componente, cor ou som `PD_*` do DS.
- **Acréscimos deste Reel** (não são regra do formato): vermelho `#D63A2F` só na fita, em "VOCÊ LÁ." e em "CONTA"; o "º" dos ordinais em Anton foi redesenhado como "o" pequeno sublinhado, porque o glifo da fonte fazia "1º" ler "10".
- **CTA:** placa do DS V2 (rótulo "ACOMPANHA AQUI" + destino "PRIMEIRO DIA" + módulo de seta), posição fixa do DS, Chegada e *clack* (−6 dB da voz, volume de trabalho da REFERENCIA_EDICAO_FORMATOS 4.1). Texto tirado da fala. Como "PRIMEIRO DIA" tem 11 letras e cabe em 128 px, o tamanho é o padrão.

## 5. Medições

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 50,33 s (voz 49,33 s + 1 s de cauda no CTA) |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 CRF 10 (≈ 57 Mb/s), AAC 320 kb/s 48 kHz |
| 3 | Tempo na tela | Todas as cenas ≥ 3 s, menos as 2 exceções do gancho pedidas pelo Diego (2,70 s e 2,53 s) |
| 4 | Planos do acervo | Nenhum corte de cena dentro dos 6 planos (detecção `scene > 0,25`); nenhum esticado; trechos dentro da duração limpa de cada arquivo |
| 5 | Legendas | 1 linha, ≤ 4 palavras, largura medida pela fonte ≤ 800 px, centradas em x 540 |
| 6 | Imagem na palavra | Todas as trocas ancoradas em palavra (`cenas.json`), de 0,05 a 0,3 s antes |
| 7 | Pessoas | Nenhum apoio com o rosto do Diego ou da Marina (IMG_3023, com a Marina, ficou de fora) |
| 9 | Áudio | **−14,0 LUFS** integrados, LRA 2,6 LU, pico verdadeiro **−1,5 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS |
| 11 | Transcrição da voz final | Whisper large-v3 no vídeo final repete a fala gravada. Palavras com confiança < 0,6: "você" (27,3 s), "o nono" (ouvido "uma no", 35,8 s), "Madame" (40,6 s), "está", "o", "porque", "pra". Nenhuma palavra cortada |
| 12 | Nada na tela fora da fala | Textos na tela: PARIS / NÃO QUER / VOCÊ LÁ, PELO MENOS, NÃO SE VOCÊ FOR / igual a todo mundo, 1º DESTINO NO MUNDO, 5º ANO SEGUIDO, HOSPEDAGEM CARA / PONTOS TURÍSTICOS / RESTAURANTES LOTADOS, DÓI NA CONTA, 3 PULOS DO GATO, 1 / 2 / 3, 4 DIAS, 9º DISTRITO, ACOMPANHA AQUI / PRIMEIRO DIA. Todos ditos |
| 13 | Créditos | `creditos.md` e `imagens/creditos/` |

Folhas: `qa_frames/folha_1s.jpg` (1 quadro por segundo) e `qa_frames/queda_do_print.jpg` (o print cai enquanto o Diego aponta, 5,1–6,1 s, 10 qps).

## 6. Arquivos

| Arquivo | O quê |
|---|---|
| `edicao.json` | Tomadas, trechos (in/out) e texto conferido de cada fala |
| `transcricao_alinhada.json` | Tempo de cada palavra (alinhamento forçado) |
| `cenas.json` | Cenas ancoradas em palavras, gancho, legendas, sons e CTA |
| `voz_medicao.json` | Medição da voz antes e depois do tratamento |
| `scripts/` | `alinhar.py`, `preparar.py`, `render.sh` (rodam de dentro de `rev1/`) |
| `imagens/` | Fotos da web, print da Euromonitor e quadro do acervo; `imagens/creditos/` com os metadados |
| `dados/paris_arrondissements.geojson` | Contorno dos distritos |
| Composição | `design-system/remotion/src/paris/` (`Paris.tsx`, `Graficos.tsx`, `estilo.tsx`), id `Paris` no `Root.tsx` |

Brutos em `../fonte/` (fora do git): `fonte/quarto/` (10 tomadas) e `fonte/acervo/` (planos de Paris).

## 7. Decisões do Diego antes de postar

1. **"Bairro mais calmo" (dica 3):** está na fala. O roteiro v1 registrou que não há fonte para isso (Pigalle e Grands Boulevards, no 9º, têm vida noturna). Se você ficou no 9º e achou calmo, é experiência sua e vale; se não, vale regravar só essa frase ("…e ainda assim muito bem localizado").
2. **Foto do gancho:** a única foto livre encontrada com policial, viaturas e a Torre Eiffel juntos tem só 675 × 452 px. Na metade de cima ela fica ampliada ≈ 1,6×: dá para ver, mas é a imagem mais macia do Reel. Se você tiver (ou quiser comprar) uma foto melhor, troca-se só `imagens/policia_noite.jpg`.
3. **Crédito obrigatório** de 3 fotos (CC BY e CC BY-SA): o texto pronto está em `creditos.md` e já entrou na `legenda_post.md`.

## 8. Conferir no ouvido (o Claude não escuta)

- A fala do ranking (f3, 4,8–13,7 s): timbre mais brilhante e mais ruído que as outras (seção 3). Se incomodar, a saída é regravar essa tomada mais perto do celular.
- Início das tomadas que começam colado no arquivo: "Agora" (f5), "E três" (f8), "Desse" (f9), "E se" (f10). Confira se a 1ª sílaba está inteira.
- O fim de "bolso" (f7) e "localizado" (f8): encostam no fim da trilha do iPhone (fade de 25 ms).
- Volume dos efeitos `PDX_*` e do *clack*: nenhum foi ouvido por humano.
