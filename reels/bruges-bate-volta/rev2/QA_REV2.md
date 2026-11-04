# QA · REV2 · Reel "Bruges não quer você lá"

**Pedido do Diego (04/11/2026) sobre a REV1:**
- Sons horríveis, efeitos ruins e voz que "parece que estoura".
- Legendas em sobreposição.
- Take da praça tremido.
- Efeitos de imagem ruins e imagens que não representam bem a fala.
- Mudanças de imagem dinâmicas demais: "dê tempo pra cada take".
- Trocar o waffle no palito pelo outro waffle.
- Porto da Barra lotado, e não vazio.

**Entrega:**
- `rev2/reel_bruges-bate-volta_rev2.mp4` (master)
- `rev2/reel_bruges-bate-volta_rev2_previa.mp4`
- `rev2/capa_bruges-bate-volta_rev2.jpg`
- `rev2/qa_frames/folha_1s.jpg`

A REV1 continua intacta em `rev1/`.

---

## 1. Análise do áudio

### O que foi medido na gravação original (9 tomadas do quarto)

| Medida | Resultado | Leitura |
|---|---|---|
| Clipping digital (flat factor) | 0 em todas | A gravação **não** estourou no microfone |
| Pico | −0,2 a −5,4 dBFS | Picos curtos de consoante ("t", "p"). Uma plosiva forte na IMG_7696, em 2,9 s ("tanto") |
| Loudness por tomada | **−16,2 a −23,7 LUFS** | **7,5 dB de diferença entre tomadas** (IMG_7696 a mais alta, IMG_7728 a mais baixa) |
| Ruído de fundo | ≈ −78 dBFS | Muito limpo: a redução de ruído da REV1 era desnecessária |

### Por que a REV1 soava estourada (causas, em ordem de peso)

1. **As tomadas não foram igualadas antes de juntar.** O guia manda igualar (FORMATOS_REELS 10.1), e na REV1 isso ficou de fora. As falas mudavam de volume entre si.
2. **O master esmagava as consoantes.** Ganho para −14 LUFS e limitador com teto de −3,3 dBFS cortavam até ~6 dB numa boa parte das sílabas. Além disso, a opção de nível automático do limitador ficou ligada sem querer (`level=disabled` não é um valor válido) e devolvia o sinal a 0 dBFS. Por isso os picos subiam e o master precisou de 4 passadas.
3. **Dois AAC seguidos:** o Remotion codificava o áudio e o master codificava de novo por cima.
4. **8 efeitos sintetizados** (impactos, riser, swish, obturador) a −4 a −8 dB da voz, que somavam picos com a fala.

### Como ficou na REV2

| Etapa | REV1 | REV2 |
|---|---|---|
| Efeitos sonoros | 8 efeitos `PDX_*` | **Nenhum** (pedido do Diego). Só o *clack* da placa do CTA, a −10 dB da voz (DS V2 4.6; antes −6 dB) |
| Tratamento por peça | — | Passa-alta 85 Hz + compressão leve (`acompressor` 2,5:1, limiar −26 dB) |
| Nível por tomada | não igualado | **Cada tomada igualada a −18 LUFS** antes de juntar. O loudness da voz inteira varia só 2,2 LU |
| Redução de ruído | `afftdn` | **Retirada** (piso de −78 dBFS) |
| Master | ganho + limitador pesado com nível automático, 4 passadas, AAC sobre AAC | Voz + clack mixados fora do Remotion. Ganho até −14 LUFS e limitador **leve** (nível automático desligado), que só toca ~2% dos trechos de 10 ms, em até 3,5 dB. **Um único AAC** |

---

## 2. Análise do vídeo

### Take tremido da praça
Medido por correlação de fase quadro a quadro (`scripts/tremor.py`; tremor = desvio do movimento em relação à trajetória suavizada, em px na escala 1080):

| Take | Tremor médio | p95 | Situação |
|---|---|---|---|
| **IMG_4121** (Markt com o Diego, REV1 em 21 s) | **2,7 px** | **6,5 px** | **Era o tremido. Saiu** |
| IMG_4235 (waffle no palito) | 3,4 px | 8,3 px | Saiu (troca pedida pelo Diego) |
| IMG_4116, 4117, 4128, 4131, 4133, 4227, 4244 | 0,1 a 0,5 px | ≤ 1,3 px | Estáveis |
| **Novos do acervo:** IMG_2439, 2448, 2642 | 0,2 a 0,4 px | ≤ 1,5 px | Estáveis, entram |
| IMG_2438 · IMG_2431 (waffle da Chez Albert) | 0,7 · 0,8 px | 2,4 · 2,0 px | Leves, entram |
| IMG_2447 (carruagens) | 1,3 px | 4,1 px | Entra **estabilizado** (vidstab, 2 passadas) |

### Efeitos de imagem e ritmo

| Ponto | REV1 | REV2 |
|---|---|---|
| Número de cenas | 27 (fotos de 0,9 s, troca a cada ~2 s) | **20**, trocando só entre frases |
| Duração dos takes | 0,9 a 2,9 s | 1,8 a 4,1 s; 16 das 20 entre 2,3 e 4,1 s |
| Movimento | Ken Burns em todo clipe e foto, corte de zoom no rosto, contador girando, relógio girando | **Sem zoom nos vídeos**; fotos com no máximo 2% de aproximação (quase parada); rosto sem zoom |
| Transições | Empurrão, Luz de passagem, Cinema, Clarão, deslize do cartão | **Cortes secos** (só as fitas do gancho continuam entrando, como aprovado) |
| Cor | Dessaturada (`saturate 0.7`) e degradê escuro forte embaixo | **Cor natural** (`contrast 1.03`) e degradê leve, só para a legenda |
| Takes verticais do iPhone | — | Corrigido um erro da preparação: a rotação não era lida e alguns takes saíam recortados e ampliados |

### Imagens trocadas para representar melhor a fala

| Fala | REV1 | REV2 |
|---|---|---|
| "A cidade tem menos de 120 mil habitantes" | Belfort de baixo (IMG_4116) | Belfort + Markt com gente (IMG_2439) |
| "e recebeu mais de 8 milhões de turistas" | Markt (IMG_4116) | Casas coloridas do Markt com o movimento (IMG_2448) |
| "Lotou tanto que a própria Bruges" | Céu e Provinciaal Hof (IMG_4117) | Markt cheio com o Provinciaal Hof (IMG_2438) |
| "Cheguei lá às 11h junto com todo mundo…" | Trem + relógio, depois a praça tremida | Trem (um take só, 3,3 s) |
| "igual um domingo de sol… Porto da Barra" | Porto da Barra lotado | O mesmo Porto da Barra lotado, com contraste corrigido. Corte seco para a tela dividida na palavra "igual" |
| "quando a galera do bate e volta vai embora" | Canal vazio + parque vazio | Begijnhof tranquilo (um take, 4 s) |
| "Dorme uma noite lá" | Belfort à noite + Markt à noite | O **mesmo Rozenhoedkaai do gancho, à noite** |
| "De manhã cedo e à noite os canais são só seus" | 2 fotos (0,9 s e 1,9 s) | Dijver de manhã, vazio (uma foto, 2,8 s) |
| "A cidade cheira a chocolate" | Waffle no palito (tremido) | **Waffle de chocolate belga da Chez Albert (IMG_2431)** |
| "É literalmente a Europa que você imagina…" | Canal + foto | **Carruagens no Markt** (IMG_2447, estabilizada) |

---

## 3. Análise das legendas: sobreposições encontradas na REV1 e correção

| Onde (REV1) | Problema | REV2 |
|---|---|---|
| 2,5–4,8 s (gancho) | Legenda na costura (y 900) sobre a 2ª fita | As fitas ficam só na 1ª frase (0–2,45 s); a 2ª parte mostra os barcos sem fita |
| 9,0–9,6 s | "120 MIL" encolhendo por cima do "8 MILHÕES" que entrava (aparecia "6 MILHÕES" sobre "120 MIL") | Cada número tem a **sua cena**, sem empilhar: "120 MIL HABITANTES" só na cena do Belfort e "8 MILHÕES DE TURISTAS EM 1 ANO" só na das casas. Fade simples, sem contagem. A legenda some enquanto o número está na tela, porque o número já é a legenda |
| 14–16,8 s (captura) | Cartão terminava em y 1260, encostando na legenda (y 1320) | Cartão menor (820 px), que termina em y 1179 |
| 20–21 s | Relógio "11H" disputando com a legenda "às 11 horas" | Relógio retirado |
| 53–55 s (CTA) | — | A legenda some quando a placa entra (já era assim) |

As legendas continuam com 1 a 4 palavras em uma linha (máx. 23 caracteres), centradas em x 540, agora só com fade, sem a escala de entrada.

---

## 4. Roteiro de cortes (REV2, 55,1 s)

| Tempo | Fala | Imagem |
|---|---|---|
| 0,00–2,45 | Bruges não quer você lá. | Dividida: Rozenhoedkaai ao amanhecer + fitas POLITIE · POLICE + texto do gancho |
| 2,45–4,85 | Pelo menos não da maneira que todo mundo vai. | Dividida: barcos lotados (IMG_4128) |
| 4,85–8,62 | A cidade tem menos de 120 mil habitantes | Belfort + Markt (IMG_2439) · **120 MIL HABITANTES** |
| 8,62–11,62 | e recebeu mais de 8 milhões de turistas em um ano. | Casas do Markt (IMG_2448) · **8 MILHÕES DE TURISTAS EM 1 ANO** |
| 11,62–13,88 | Lotou tanto que a própria Bruges | Markt cheio (IMG_2438) |
| 13,88–16,80 | parou de fazer propaganda em Bruxelas e em Paris. | Captura da Afar |
| 16,80–19,32 | E eu sei qual o jeito errado. Porque eu fiz. | Diego |
| 19,32–22,62 | Cheguei lá às 11 horas junto com todo mundo e saí no final da tarde. | Trem (IMG_4244) |
| 22,62–26,74 | Eu não contava que Bruges era igual um domingo de sol, duas horas, no Porto da Barra de Salvador. | Markt lotado; em "igual", corte para Bruges em cima, Porto da Barra lotado embaixo e "=" |
| 26,74–29,70 | Ela tá lá, linda. Mas você só vê gente. | Rozenhoedkaai com os barcos cheios (IMG_4128) |
| 29,70–33,72 | Só que Bruges é outra cidade quando a galera do bate e volta vai embora. | Begijnhof (IMG_2642) |
| 33,72–36,40 | Por isso eu vou te dar um conselho aqui. Olho no olho. | Diego |
| 36,40–38,88 | Dorme uma noite lá. Você não vai se arrepender. | Rozenhoedkaai à noite (foto) |
| 38,88–41,66 | De manhã cedo e à noite os canais são só seus. | Dijver de manhã (foto) |
| 41,66–43,50 | O centro inteiro é patrimônio da humanidade. | Canal com a torre (IMG_4131) |
| 43,50–45,40 | A cidade cheira a chocolate. | Waffle da Chez Albert (IMG_2431) |
| 45,40–47,42 | Foi a cidade mais bonita que eu vi na Bélgica. | Minnewater (IMG_4218) |
| 47,42–50,95 | É literalmente a Europa que você imagina antes de ir pra Europa. | Carruagens no Markt (IMG_2447) |
| 50,95–53,00 | Agora me diz aí, você colocaria | Diego |
| 53,00–55,13 | Bruges no seu roteiro da Bélgica? | Dividida: o amanhecer do gancho, sem fitas, com a placa do DS "NO SEU ROTEIRO / BRUGES ?" e o clack |

**Abaixo de 2 s:** "patrimônio" (1,84 s) e "chocolate" (1,90 s). As frases são curtas; esticar poria a imagem fora da palavra.

---

## 5. Medições (vídeo final)
(preenchidas após o render)

## 6. Conferir no ouvido (o Claude não escuta áudio)
- [ ] A voz não estoura mais, principalmente "tanto" (≈ 12,5 s) e "Olho no olho" (≈ 35,3 s).
- [ ] O volume está parelho entre as falas.
- [ ] O corte "humanidade. / A cidade cheira a chocolate" (≈ 43,5 s).
- [ ] O clack da placa (≈ 53,4 s) baixo o suficiente.
