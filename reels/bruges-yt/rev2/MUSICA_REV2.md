# REV2 · Música do vlog de Bruges: as faixas escolhidas

As 21 faixas que o Claude no Chrome baixou da Biblioteca de áudio do YouTube (Drive, Bruges/Youtube/Música, 20/11/2026) foram separadas em 3 por seção pela ordem do download, que segue a ordem do prompt. "Scale The Mountain" e "Bright Skies" vieram repetidas: usei uma cópia de cada. Medi andamento (BPM), energia segundo a segundo, introdução e brilho de cada uma (`analisar_musicas_rev2.py` → `musicas_medidas_rev2.json`).

**Eu não escuto áudio.** A escolha é por medição + o clima pedido; quem aprova é o seu ouvido. Para aprovar sem ver o vídeo todo: `previas/rev2_musica_secoes.mp4` (só os trechos com música, com o nome da faixa no canto).

## Escolhidas

| Seção | Faixa | Na prévia | Por que essa |
|---|---|---|---|
| **G · Abertura** | Scale The Mountain · Density & Time | 0:00–0:31 | É a que mais cresce até o fim do gancho (+10 dB entre 0:03 e 0:25; as outras, +7 e +9), começa sem introdução e tem o timbre mais escuro das três, o que deixa espaço para a sua voz. Entra em 0,6 s da faixa para uma **batida forte cair exatamente no corte do bilhete**. Termina ali, como você pediu |
| **M1 · Chegada e o primeiro waffle** | Top Of The Morning · TrackTribe | 1:12–1:33 · 1:58–2:16 | 117 BPM e a energia mais estável das três (varia 3 dB): entra e sai duas vezes sem salto. Leve e de manhã |
| **M2 · Markt, Burg e canais** | Powdered Waltz · The Mini Vandals | 2:44–2:57 · 3:46–4:05 · 4:41–5:11 · 5:49–6:12 | **Valsa**: carruagem, praça medieval, "conto de fadas". Estável e suave; tem 2:14, e a seção usa 1:26. É da mesma banda de uma faixa do vlog de Bruxelas (The Mini Vandals), mas é outra música |
| **M3 · Fome, chocolate e a batata** | Fine Dining · TrackTribe | 7:30–7:47 · 8:09–8:27 · 9:51–10:08 | Clima de restaurante (e o nome ajuda), 129 BPM, animada |
| **M4 · Minnewater: o descanso** | The Swan · The Soundlings | 10:56–11:17 | A mais calma das três (menos ataques por segundo); cisne combina com o lago |
| **M5 · O teste dos waffles e a despedida** | Squirm Worm · TrackTribe | 11:17–11:30 · 11:56–12:00 (time-lapse) · 13:02–13:13 | A mais rápida e brincalhona (185 BPM, brilhante): dá a graça do time-lapse da Marina soprando o waffle |
| **F · Fechamento e tela final** | Dusty Road Magic · Chris Haugen | 14:06–15:25 | Estável, sem introdução e com o timbre mais escuro das três: não briga com a narração. Na tela final (sem voz) ela sobe e sai nos últimos 3 s |

## Alternativas (já baixadas, troco em minutos)

| Seção | Alternativas | Por que ficaram atrás |
|---|---|---|
| G | Bright Skies (Audio Hertz) · Taking Flight (Blue Deer Studio) | Crescem menos no gancho; Taking Flight é a mais brilhante e agitada (disputa com a voz) |
| M1 | Clouds Lifting (Telecasted) · No.3 Morning Folk Song (Esther Abrami) | Clouds Lifting é mais lenta (78 BPM); a Morning Folk Song varia 16 dB (some e volta: arriscado nos cortes) |
| M2 | Ripples In Time (Asher Fulero) · Panoramic Arrival (Asher Fulero) | Ripples é estável, mas mais agitada; Panoramic varia 16 dB |
| M3 | Swing Haven 1 (Reed Mathis) · Strollin' (TrackTribe) | Swing Haven é a mais estável de todas (boa opção, mais "swing"); Strollin' perde energia |
| M4 | Starlight on the Water (Chris Haugen) · The Palace Gardens (Asher Fulero) | Mais movimento que The Swan |
| M5 | Bop Walker (Freedom Trail Studio) · Peaked My Interest (Nathan Moore) | Bop Walker é bebop mais "sério"; Peaked My Interest tem 9 s de introdução |
| F | Lily's Song (TrackTribe) · Spring Migration (The Great North Sound Society) | Lily's Song varia muito (11,7 dB); Spring Migration tem 14 s de introdução e cresce 19 dB, demais sob a voz |

## Como entrou (mixagem da prévia)

- Cada seção usa uma faixa só, que **continua de onde parou** a cada trecho (M2, por exemplo, vai de 0:00 a 1:26 da faixa ao longo dos 4 trechos). Entra em 0,25 s e sai em 0,5 s dentro de cada trecho.
- Paisagem sem fala: 3 dB abaixo da fala. Abertura e fechamento, sob a narração: 9 dB abaixo da voz (`docs/VIDEO_LONGO_YOUTUBE.md`, seção 3). As narrações ainda não estão gravadas, então na prévia a abertura e o fechamento soam baixos de propósito: é o nível que vão ter com a sua voz por cima.
- A abertura sobe para o nível de paisagem quando a narração acaba (0:29) e para no corte do bilhete.
- O time-lapse fica sem o som acelerado: só a música.
- Detalhe de cada trecho (minuto do vídeo × ponto da faixa): `musica_rev2.json`.

## O que falta

- **Atribuição:** os MP3 não trazem essa informação, e a tabela do Claude no Chrome não chegou até mim. Me mande a coluna de atribuição das 7 escolhidas, ou confira no Studio. Se alguma for "atribuição obrigatória", o texto de crédito vai na descrição do vídeo.
- **Escuta:** a sua aprovação de cada faixa e dos volumes.
