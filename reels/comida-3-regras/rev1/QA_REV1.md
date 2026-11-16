# QA · 3 formas de economizar com comida na viagem · REV1 (16/11/2026)

**Entrega:** `comida_3_formas_rev1.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Legendas do post: `legenda_post.md`.
**Fonte:** gravação do Diego no quarto (Drive `Youtube/Reel/Custos`, BAEAA0F8…mp4 → `../fonte/gravacao.mp4`, 124,8 s, HDR HLG). Roteiro de partida: a versão de 60 s combinada no chat (estrutura AIDA, tela dividida); a legenda e as cenas seguem **o que foi gravado**, não o roteiro (FORMATOS_REELS 9.5).
**Composição:** `ComidaReel` (`design-system/remotion/src/reel/ComidaReel.tsx`, modelo de Veneza REV4). Scripts: `transcrever.py` → `preparar.py` (decupagem, voz, apoio) → `cenas.py` (cenas, legenda, posições) → render → `master.py` → `analise_quadros.py`.

**Render:**
```
cd design-system/remotion
npx remotion render src/index.ts ComidaReel ../../reels/comida-3-regras/rev1/render_sem_master.mp4 \
  --props=../../reels/comida-3-regras/rev1/props.json --public-dir=../../reels/comida-3-regras/rev1/public \
  --codec=h264 --crf=16 --audio-bitrate=320k
cd ../../reels/comida-3-regras/rev1 && python3 master.py render_sem_master.mp4 comida_3_formas_rev1.mp4
```

## Pedidos do Diego (16/11/2026) e o que foi feito

| Pedido | Feito |
|---|---|
| Seguir estritamente a sequência da gravação | 11 falas na ordem gravada. Onde ele regravou a mesma fala, ficou **o último take**: "Claro que não." (64,6 s fora, 65,8 s dentro), moral (90,3 s fora, 98,8 s dentro) e CTA (108,3 s fora, 117,8 s dentro). Ver "Para o Diego decidir" |
| Sem espaço entre as falas, sem cortar palavra | 13 trechos. Pausas maiores que 0,30 s saem; cada emenda cai no silêncio, com 40 ms antes e 50 ms depois da voz. Início medido pela energia: "Você" começa em 0,24 s (corte em 0,20 s) e "Bora" em 9,88 s (corte em 9,83 s) |
| Legenda com a cor no momento em que ele fala | Karaokê de Veneza REV4: caixa normal, a palavra dita fica amarela, nada aparece antes de ser dito (tempos do alinhamento forçado wav2vec2) |
| Nada na frente da cara | Tela dividida: rosto a 42% da metade de baixo e topo do rosto ≥ 50 px abaixo da legenda da costura (o ajuste entrou porque no gancho ele levanta o rosto). Tela cheia: legenda abaixo do queixo (y 1320–1333). CTA: placa abaixo da barba. Medido quadro a quadro em `analise_quadros.py` |
| Tela dividida × tela cheia | "…conhecer bons restaurantes? / Bora que eu vou te mostrar": ele inteiro; volta à tela dividida em "três formas". "E nas outras refeições, rapaz, vai ficar sem comer? / Claro que não.": ele inteiro. CTA: ele inteiro. O resto em tela dividida |
| Preto e branco só na pergunta da "terceira pessoa" | Só T7 ("E nas outras refeições, rapaz, vai ficar sem comer?"), `grayscale(1)` puro. A resposta "Claro que não." volta à cor |
| Variar acervo, ilustrações e animações | 6 planos e 1 foto do acervo, 7 animações próprias do Reel |
| Acervo sem tremor e sem efeito (sem zoom, sem câmera lenta ou rápida) | Tremor medido por correlação de fase (todos ≤ 0,2 px de variação entre quadros); nenhum zoom, nenhuma mudança de velocidade; nenhum plano usado além da própria duração |
| 2,5 a 3 s no mínimo por imagem/animação | Menor cena: 2,61 s (ele em tela cheia na pergunta em P&B); imagens e animações de 3,0 a 7,0 s |
| Gancho com o prato do bouillon, sem animação na frente | Le Petit Bouillon Pharamond, Paris (17/03/2026 16:24), plano de lado (IMG_3075), que mostra o prato inteiro; só a legenda na costura |
| Vídeo dele sem nenhuma cor | Só a conversão de formato HLG→SDR (a mesma de Veneza), sem grade, LUT ou contraste. Acervo idem |
| O "menorzinho de toda manhã" é o café preto | Foto dele com o café na rua em Florença (IMG_5826, enviada no chat), parada e sem filtro |
| O que aparece em cima sempre ilustra a fala | Ver "Fala × imagem" |
| Imagens reais do acervo (mercado) | Supermercado Albert Heijn, Amsterdam (13/03/2026 20:03): Marina de costas com a cestinha nos corredores |

## Fala × imagem

| Final (s) | Fala | Imagem (em cima) |
|---|---|---|
| 0,00–3,12 | Você quer saber como economizar com a alimentação nas suas viagens e ainda assim | Prato do bouillon (IMG_3075), sem nada na frente |
| 3,12–6,45 | conhecer bons restaurantes? Bora que eu vou te mostrar | Ele em tela cheia |
| 6,45–9,93 | três formas que eu uso pra não gastar uma nota com comida durante a viagem. | Animação: "3 FORMAS" + nota de euro + "NÃO GASTAR UMA NOTA" |
| 9,93–12,93 | A primeira coisa é economizar no café da manhã. Se não tá incluso no hotel, | Animação: "1", xícara, "CAFÉ DA MANHÃ", sino de hotel riscado + "NÃO TÁ INCLUSO" |
| 12,93–16,33 | a gente passa no supermercado e compra algumas coisas para comer no quarto mesmo. | Supermercado Albert Heijn, Amsterdam (IMG_1842) |
| 16,33–20,70 | O que sobra para comprar na rua é só um menorzinho de toda manhã que não pode faltar, né? | Foto do café preto na rua, Florença (IMG_5826) |
| 20,70–24,03 | Segunda, escolha uma refeição pra gastar um pouco mais no restaurante. | Salão do Pharamond, Paris (IMG_3071) + "SEGUNDA" |
| 24,03–28,40 | Geralmente escolhemos o jantar porque é mais no final do dia, a gente já fez tudo e pode comer com calma. | Animação: o sol desce, a lua sobe, "JANTAR", "NO FINAL DO DIA", "COM CALMA" |
| 28,40–35,43 | Mas quem define? Seu roteiro. Se tem algum restaurante que vale a pena ir na hora do almoço por conta de uma vista ou experiência do lugar, aí você inverte. | Animação: "QUEM DEFINE? SEU ROTEIRO", cartões ALMOÇO × JANTAR, "VISTA OU EXPERIÊNCIA"; as moedas pulam do jantar para o almoço em "inverte" |
| 35,43–38,04 | E nas outras refeições, rapaz, vai ficar sem comer? (P&B) Claro que não. | Ele em tela cheia |
| 38,04–42,43 | Você vai comer alguma comida de rua, algum lanche rápido, algo mais simples que vai te fazer gastar menos. | Barraca de comida de rua, Amsterdam (IMG_1609) |
| 42,43–45,97 | E eu te garanto que isso vai fazer parte de sua experiência conhecendo o local. | Waffle com a bandeira belga, Bruges (IMG_2431) |
| 45,97–49,97 | Por exemplo, vamos supor que você vai para a Europa e quer gastar 50 euros por dia com comida. | Animação: "POR EXEMPLO, VAMOS SUPOR", "EUROPA", "50 €", "POR DIA COM COMIDA" |
| 49,97–53,87 | Então você vai usar esse valor pra balancear suas refeições de acordo com a dica número 2. | Animação: balança (sol × lua) que equilibra em "balancear", "DICA Nº 2" |
| 53,87–57,80 | Economizar com comida não é comer mal, é você saber onde gastar e onde não gastar. | O prato do bouillon de cima (IMG_3078): fecha com o prato do gancho |
| 57,80–62,47 | Se você gostou das dicas, me segue aí para aprender a viajar melhor sem gastar dinheiro à toa. | Ele em tela cheia + placa do DS `PRA VIAJAR MELHOR / ME SEGUE` em "me segue" + *clack* |

**Os 50 € são exemplo** ("vamos supor"), como ele falou; a tela diz "VAMOS SUPOR" antes do número.

## Leituras a conferir no ouvido (Diego)

1. **"menorzinho"** (16,9 s): Whisper large-v3 e o alinhador wav2vec2 ouvem "menorzinho" com folga (CTC −146 contra −176 de "melhorzinho" e −218 de "cafezinho"). O Diego confirmou que é o café preto; a legenda escreve "menorzinho".
2. **"Mas quem define? Seu roteiro."** (28,4 s): o Whisper escreve "Mas quem definir seu roteiro?" e o alinhador prefere "definir". A legenda escreve "define? Seu roteiro." pelo sentido.
3. "pra"/"para", "tá incluso" e "de sua experiência": escolhidos pelo alinhador em cada ocorrência.

## Para o Diego decidir

- **Takes regravados:** ficou sempre o último. Na moral, o 1º take terminava "…e onde dá para economizar" (90,3 s) e o 2º, que entrou, termina "…e onde não gastar". Se preferir o 1º, é só trocar a janela de T10 em `preparar.py`.
- **Gancho:** o plano de lado do prato tem 3,62 s; o gancho falado tem 4,77 s. Sem esticar o plano, ele entra em tela cheia em "conhecer bons restaurantes?" (≈ 1,7 s antes do "Bora").
- **Composições:** nunca 3 animações seguidas: formas → café da manhã → supermercado (real) → café (foto).

## Efeitos (kit PDX; ninguém ouviu)

Impacto em "três" (−6 dB) e em "50" (−6 dB); obturador em "nota" e em "dica" (−9 dB); *swish* em "inverte" (−8 dB); *clack* da placa em "me segue" (−6 dB). Escuta humana obrigatória antes de postar (CLAUDE.md, 12).

## Medições do vídeo final (`analise_quadros.py` + nova transcrição)

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz 320 kb/s, 62,5 s (1.875 quadros) |
| Áudio | −14,0 LUFS integrados, pico verdadeiro −2,0 dBTP (DS 4.6). Voz: passa-alta 70 Hz + loudness (como em Veneza); master com ganho linear e limitador com sobreamostragem 4× |
| Palavras | Voz final transcrita de novo (Whisper large-v3): 257 de 264 palavras iguais; as 7 diferenças são de grafia do Whisper ("3"/"três", "pra"/"para", "segundo"/"segunda", "definir"/"define") e um "rapaz" que ele pulou no áudio inteiro, mas ouve no trecho isolado (36,2 s). Nenhuma palavra cortada |
| Quadros pretos | nenhum (luminância mínima 51/255) |
| Preto e branco | só T7 (diferença R−B medida a cada 3 quadros nas cenas com ele) |
| Texto × rosto | menor folga 38 px (placa do CTA, 60,6 s); legenda sempre fora do rosto, na dividida e em tela cheia |
| Menor cena | 2,61 s (ele em tela cheia na pergunta em P&B); imagens e animações ≥ 3,0 s |
| Folha de 1 quadro por segundo | `qa_folha_1qps.jpg` |

## Imagens: origem

- **Acervo do Diego:** IMG_3075 e IMG_3078 (prato, Le Petit Bouillon Pharamond, Paris, 17/03/2026) · IMG_3071 (salão do Pharamond) · IMG_1842 (Albert Heijn, Amsterdam, 13/03/2026, Marina de costas) · IMG_1609 (barraca de rua, Amsterdam, 13/03/2026) · IMG_2431 (waffle, Bruges, 16/03/2026) · IMG_5826 (foto do café, Florença; enviada pelo Diego no chat). Tudo sem filtro, sem zoom e na velocidade original.
- **Animações:** desenhos próprios do Reel (paleta "Mesa", só deste Reel; fora do DS V2). DS V2 só no CTA (placa + *clack*).
