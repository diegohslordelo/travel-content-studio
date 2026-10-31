# QA · Reel da cratera de Darvaza · REV1 (31/10/2026)

**Veredito: pronto para postar, com 1 pendência de material e itens de escuta.** O take do gancho escrito no roteiro ("Imagina encontrar um buraco gigante em chamas no meio do deserto!") não está no Drive; a REV1 abre na fala 2 ("Tem fogo pra todo lado…"), que funciona como gancho sensorial. Se o take existir, é só subir na pasta `Cratera` que a REV2 entra com ele (o pipeline já está pronto: uma linha em `edicao.json`).

## Entrega

| Arquivo | O que é |
|---|---|
| `reel_darvaza_rev1.mp4` | Final: 1080 × 1920, 30 qps, H.264 + AAC 48 kHz 320 kb/s, **38,0 s** |
| `reel_darvaza_rev1_previa.mp4` | Prévia leve (540 × 960) para ver no celular |
| `capa_darvaza_rev1.jpg` | Capa 1080 × 1920 (o título fica dentro do recorte 3:4 do grid, y 285–795) |
| `qa_frames/cenas.jpg` · `qa_frames/um_por_segundo.jpg` | Um quadro por cena · um quadro por segundo |
| `../legenda_post.md` | Legendas do Instagram, TikTok e Shorts + música recomendada |
| `../creditos.md` | Autor e licença de cada foto, mapa, ilustrações e sons |

## Material

- **Fala:** 7 tomadas gravadas no quarto (Drive, `Youtube/Reel/Cratera`: IMG_7537, 7540, 7541, 7542, 7543, 7546, 7547). As cópias repetidas de IMG_7540 e IMG_7542 têm o mesmo tamanho em bytes e não foram usadas em dobro. Brutos em `../fonte/` (fora do git), sem alteração.
- **Imagens da cratera:** não havia vídeo da cratera no Drive. Foram usadas **15 fotos reais da cratera de Darvaza** do Wikimedia Commons (CC BY / CC BY-SA, `../creditos.md`). Não se encontrou vídeo da cratera com licença livre: o Pexels não tinha nenhum identificado como Darvaza; os vídeos do Commons são só de satélite (com data na tela). Nenhuma imagem de outro lugar foi usada.
- **Criado:** ilustrações em traço (perfuração, desabamento, gás, fósforo), mapa (Natural Earth, domínio público), títulos e ícone de envio.

## Roteiro × fala gravada (a fala gravada manda: FORMATOS_REELS.md, 9.5)

| Bloco | Roteiro | Fala gravada (= legenda) |
|---|---|---|
| 1 · gancho | "Imagina encontrar um buraco gigante em chamas no meio do deserto!" | **Não está no Drive** (pendência) |
| 2 | "É fogo por toda parte!" | "Tem fogo pra todo lado," |
| 3 | "com uma perfuração… O solo cedeu, formando uma enorme cratera." | "com a perfuração… e aí o solo cedeu e formou essa enorme cratera." |
| 3 | "acreditando que as chamas se apagariam" | "acreditando que ele se apagaria" |
| 4 | "Manda esse vídeo pra aquela pessoa…" | "Antes de eu falar onde fica, já manda esse vídeo para aquela pessoa…" |
| 5 | "É a cratera de Darvaza, conhecida mundialmente como…" | "É a cratera da Darvaza. Ele também é mundialmente conhecido como…" |
| 6 | "transformando um acidente ligado à exploração de gás em uma das paisagens…" | "o que começou com uma exploração natural se transformando nas paisagens…" |
| 7 | "Segue o perfil para descobrir outros lugares inacreditáveis…" | "Já segue esse perfil para não perder outros lugares imperdíveis pelo mundo!" |

**Começo falso removido:** em IMG_7547 (0,42–1,62 s) você diz "E o mais impressionante é que…", para e recomeça em 2,38 s. Entrou só a 2ª leitura, inteira. Nenhum outro corte dentro de tomada.

## Decupagem (edicao.json)

| Fala | Tomada | Trecho do bruto (s) | No Reel (s) |
|---|---|---|---|
| f2 | IMG_7537 | 2,07–6,27 | 0,00–4,20 |
| f3a | IMG_7540 | 0,44–5,27 | 4,20–9,03 |
| f3b | IMG_7541 | 0,49–5,29 | 9,03–13,83 |
| f4 | IMG_7542 | 1,97–6,40 | 13,83–18,27 |
| f5 | IMG_7543 | 1,87–8,14 | 18,27–24,53 |
| f6 | IMG_7547 | 2,34–9,73 | 24,53–31,93 |
| f7 | IMG_7546 | 2,13–7,70 (+0,5 s de imagem) | 31,93–38,00 |

- Entrada e saída medidas pela energia da voz em duas bandas (120–3.500 Hz e 3,5–12 kHz, para não perder o "s" final de "dias", "Darvaza"), com folga de 40–80 ms. Cortes só no silêncio.
- **Espaço entre falas:** 0,10–0,18 s (a folga de cada lado), sem respiro extra, como pedido. Nenhuma voz acelerada.
- Voz e vídeo cortados nos mesmos trechos, em número inteiro de quadros: a boca fica em sincronia.
- Cauda de 0,5 s depois de "pelo mundo!": a partir de ≈ 38,0 s do bruto você estica a mão para parar a gravação, então o Reel termina antes.

## Montagem (cenas.json · 25 cenas)

| # | Tempo (s) | Fala | Imagem | Composição |
|---|---|---|---|---|
| 1 | 0,00–1,23 | Tem fogo pra todo lado | Chamas de perto + texto do gancho | Dividida (rosto desde o 1º quadro) |
| 2 | 1,23–2,33 | e quando a noite chega | Brilho da cratera no anoitecer | Dividida |
| 3 | 2,33–4,27 | parece que abriram uma porta direto pro inferno | Borda em chamas, à noite | Tela cheia + **mergulho no fogo** |
| 4 | 4,27–6,87 | A história começou com a perfuração em busca de gás natural | Ilustração: torre perfura até o bolsão de gás | Dividida |
| 5 | 6,87–7,77 | e aí o solo cedeu | Ilustração: o chão desaba, a torre cai | Tela cheia |
| 6 | 7,77–9,03 | e formou essa enorme cratera | Foto real da cratera de dia | Dividida |
| 7 | 9,03–10,43 | Para evitar que o gás se espalhasse | Ilustração: gás saindo e se espalhando | Dividida |
| 8 | 10,43–11,27 | decidiram colocar | Ilustração: fósforo risca e cai | Dividida |
| 9 | 11,27–12,57 | fogo nele, acreditando que ele | Chamas dentro da cratera (*match cut* do fósforo para o fogo real) | Tela cheia |
| 10 | 12,57–13,90 | se apagaria em poucos dias | Cratera com fumaça escurecendo + **POUCOS DIAS** | Tela cheia |
| 11 | 13,90–16,20 | Antes de eu falar onde fica, já manda esse vídeo… | Você + ícone de envio | Diego em tela cheia (2,3 s) |
| 12 | 16,20–17,10 | que teria coragem | Pessoa de braços abertos na borda | Dividida |
| 13 | 17,10–18,30 | de chegar perto desse lugar! | Carro e pessoas na borda à noite | Dividida |
| 14 | 18,30–19,57 | Esse lugar existe de verdade | Cratera no deserto à noite | Tela cheia + **luz de passagem** |
| 15 | 19,57–20,73 | e fica no Turcomenistão. | Mapa: zoom até o país + ponto da cratera + **TURCOMENISTÃO** | Tela cheia |
| 16 | 20,73–22,07 | É a cratera da Darvaza. | Cratera no crepúsculo + **A CRATERA / DARVAZA** | Tela cheia |
| 17 | 22,07–22,97 | Ele também é mundialmente | Silhuetas na borda | Dividida + **clarão de volta** |
| 18 | 22,97–24,60 | conhecido como a Porta do Inferno. | A foto mais icônica + **PORTA DO INFERNO** | Tela cheia |
| 19 | 24,60–26,80 | E o mais impressionante é que a cratera continuou queimando | Você, com corte de zoom em "é que" | Diego em tela cheia (2,2 s) |
| 20 | 26,80–28,27 | durante décadas, o que começou | Rastros de estrelas sobre o brilho da cratera + **DÉCADAS** | Tela cheia |
| 21 | 28,27–29,47 | com uma exploração natural | A torre da ilustração de volta (rima com o bloco 3) | Dividida |
| 22 | 29,47–32,00 | se transformando nas paisagens mais surreais do planeta | Panorama da cratera com movimento lateral | Tela cheia |
| 23 | 32,00–34,30 | Agora me diz, você teria coragem de ver isso de perto? | A câmera se aproxima da cratera ao amanhecer | Dividida |
| 24 | 34,30–36,03 | Já segue esse perfil para não perder outros | Borda à noite + **placa CTA do DS** | Dividida |
| 25 | 36,03–38,00 | lugares imperdíveis pelo mundo! | Chamas de perto (mesmo plano do gancho: loop) + placa | Dividida |

- **Regra dos 3 segundos:** o gancho (rosto + "TEM FOGO" + chamas) está completo no 1º quadro; nenhuma cena passa de 3 s (máxima 2,87 s; média 1,52 s). Material gravado por você em tela cheia: 2,3 s e 2,2 s (mínimo de 2 s).
- **Palco para as imagens:** as 5 telas cheias com título caem nas palavras de maior peso (POUCOS DIAS, TURCOMENISTÃO, DARVAZA, PORTA DO INFERNO, DÉCADAS), cada uma no instante da palavra.
- **CTA de envio antes do nome:** o pedido de envio (13,9–18,3 s) vem imediatamente antes da revelação (18,3 s) e ainda sem dizer onde é; o CTA final pede para seguir. Objetivos diferentes, como pedido.
- **Nada na tela fora da fala:** todos os títulos repetem palavras ditas. A placa do CTA traz "SEGUE O PERFIL / @PRIMEIRODIAEM" (o @ é o ativo da marca no CTA).

## Transições (3, nas viradas; o resto é corte seco)

| Em | Transição | Por quê (ligada ao tema) |
|---|---|---|
| 4,27 s | **Mergulho no fogo** | Da "porta pro inferno" para o passado: a câmera afunda nas chamas, o corte fica no quadro mais claro e a ilustração da perfuração nasce do brilho |
| 18,30 s | **Luz de passagem** (pico 85% por 4 quadros) | A revelação: luz quente de fogo na ida para o lugar real |
| 22,07 s | **Clarão de volta** | Par da luz de passagem, na volta para o rosto |

Mais um *match cut* seco (fósforo da ilustração → fogo real, 11,27 s) e um corte de zoom no rosto (25,6 s), que não contam na cota.

## Som (nada disso foi ouvido)

| Em (s) | Som | Nível (relativo à voz) |
|---|---|---|
| 4,1 | `PDX_ar_longo` (pico no corte do mergulho) | −6 dB |
| 7,5 | `PDX_impacto` ("cedeu") | −4 dB |
| 11,1 | `PDX_ar_longo` (fogo acende) | −8 dB |
| 13,0 | `PDX_swish` (POUCOS DIAS) | −8 dB |
| 15,6 | `PDX_swish` (avião de envio sai voando) | −8 dB |
| 17,5–18,3 | `PDX_riser` (sobe até a revelação) | −8 dB |
| 18,2 | `PDX_ar_longo` (luz de passagem) | −6 dB |
| 21,3 · 23,7 · 27,2 | `PDX_impacto` (DARVAZA, PORTA DO INFERNO, DÉCADAS) | −4, −4, −6 dB |
| 34,6 | *Clack* da placa (único som do DS) | −6 dB |
| contínua | Cama de fogo sintetizada (rumor grave + estalos); some nas ilustrações (é o passado) e sobe nas telas cheias de fogo | −24 dB (realces −14 a −17 dB) |

Nenhuma música no arquivo: a sugestão para pôr no app está em `../legenda_post.md`.

## Checklist (medido)

| # | Ponto | Resultado |
|---|---|---|
| 1 | Duração | 38,0 s (o guia do formato pede ≤ 45 s) ✅ |
| 2 | Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz ✅ |
| 3 | Material seu em tela cheia ≥ 2 s; nada esticado | 2,3 s e 2,2 s; nenhum take esticado nem voz acelerada ✅ |
| 5 | Legendas | 1 linha, 1–4 palavras, Inter 800 66 px, centro em x 540, y 900 (dividida) / 1320 (tela cheia) / 970 no CTA (abaixo da placa). Maior grupo: 21 caracteres (largura não medida pixel a pixel nesta revisão; no formato, 21 caracteres medem ≈ 750 px) |
| 6 | Imagem na palavra | Cenas ancoradas no alinhamento forçado (wav2vec2), 0,02–0,06 s antes da palavra ✅ |
| 7 | Pessoas nas imagens | Só silhuetas e pessoas de costas, sem rosto identificável; foto com rosto descartada ✅ |
| 8 | Linha da tela dividida | 6 px a 55% em y 897–902 ✅ |
| 9 | Áudio | **−14,0 LUFS**, pico verdadeiro **−1,4 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS ✅ |
| 11 | Transcrição do vídeo final | Whisper large-v3 no áudio final reproduz a fala inteira, sem palavra cortada. Confiança < 0,6: "Tem" (0,0 s), "pra" (0,5 s), "solo" (7,1 s), "ele" (22,0 s), "começou" (28,2 s) |
| 12 | Nada na tela fora da fala | ✅ (títulos = palavras ditas) |
| 13 | Créditos | `../creditos.md` e bloco de crédito na legenda ✅ |

## Conferir no ouvido (Diego)

1. **"o solo cedeu"** (7,1 s): o Whisper ouve "o sol cedeu". A legenda diz "solo".
2. **"Ele também é mundialmente conhecido"** (22,0 s): você disse "Ele" (o lugar). A legenda segue a fala.
3. **"o que começou com uma exploração natural"** (28,0 s): o roteiro dizia "exploração de gás"; a fala gravada é "exploração natural" e a legenda segue a fala. O sentido fica um pouco solto; se incomodar, regrave só essa frase no quarto.
4. **"para aquela pessoa"** (15,6 s): pode ter sido "pra"; a legenda diz "para".
5. Sons `PDX_*`, cama de fogo e *clack*: ninguém ouviu. Se algum competir com a voz, me diga qual e em quanto baixar.

## Fatos (fontes)

- Origem: "perfuração em busca de gás natural" é a versão mais contada. A Wikipedia registra também "campo de petróleo" (1971) e a hipótese de geólogos locais (desabamento nos anos 1960, fogo nos anos 1980). A fala não cita data; a legenda do post diz "na versão mais contada, em 1971".
- "continuou queimando durante décadas": correto. Em junho de 2025, a Turkmengaz disse que o fogo diminuiu quase 3 vezes (RFE/RL, Popular Science, The Week). Isso está na legenda do post, para o vídeo não sugerir que hoje está igual às fotos.
- Localização (Karakum, ≈ 260 km de Ashgabat) e medidas (60–70 m × 30 m): Wikipedia, "Darvaza gas crater".

## Pendências

1. **Take do gancho** (bloco 1): não está no Drive. Se você subir, entra como `f1` e a REV2 sai com ele (o gancho de texto passa a ser "IMAGINA ENCONTRAR / UM BURACO GIGANTE / EM CHAMAS").
2. **Escuta** dos itens acima.
3. **Linguagem do formato** (Anton, Inter, âmbar, grão): é a mesma dos Reels em tela dividida do perfil, fora do DS V2 (CLAUDE.md, 6: DS só no CTA).
