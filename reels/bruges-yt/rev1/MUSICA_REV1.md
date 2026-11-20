# REV1 · Música do vlog de Bruges: mapa das seções e acesso à Biblioteca de áudio do YouTube

Tempos na prévia da REV1 (`previas/rev1_previa_540p.mp4`, 15:17). Na prévia, cada trecho de música aparece marcado no topo da tela ("MÚSICA M1…M5"), sem som de música.

## 1. O que eu preciso para acessar a biblioteca

A Biblioteca de áudio só existe dentro do YouTube Studio, com o canal logado ([Ajuda do YouTube](https://support.google.com/youtube/answer/3376882?hl=pt-BR)). Desta sessão na nuvem eu não tenho login no seu canal nem nenhum computador seu conectado, então não consigo abrir a biblioteca sozinho. Duas formas:

| Opção | O que você faz | O que eu faço |
|---|---|---|
| **A (recomendada, ~10 min)** | No Studio → Biblioteca de áudio, aplica os filtros de cada seção (tabela da seção 2) e baixa 2 ou 3 faixas por seção que te agradarem nos primeiros segundos. Sobe tudo numa pasta `musica` dentro de Bruges/Youtube no Drive, com o nome da seção no arquivo (ex.: `M2_nome-da-faixa.mp3`) | Meço duração, andamento (BPM) e curva de energia de cada faixa, escolho a que encaixa em cada trecho (começo e fim batendo com os cortes) e te mando os cortes de cada seção já com a música para aprovar |
| **B** | Conecta o seu computador a esta sessão (app Claude no computador → Configurações → Claude Code → Remote Control) com o navegador logado no YouTube | Eu mesmo filtro, ouço os metadados e baixo as candidatas pela biblioteca |

**Importante:** eu não escuto áudio. Escolho pelos dados da faixa (gênero, clima, BPM, duração) e pela energia medida; a aprovação final é do seu ouvido. Prefira faixas com **"Atribuição não obrigatória"** (filtro da própria biblioteca): as que pedem atribuição exigem o crédito na descrição.

## 2. As seções (5 no corpo + abertura + final)

Regra que segui (seu pedido): música em toda parte em que vocês não estão falando para a câmera. São exatamente as 10 montagens de paisagem em que você deixou o som mudo (medido: silêncio digital no arquivo), mais o time-lapse da Marina e a cerveja no bar. Onde vocês falam para a câmera, sem música. Cada seção usa **uma faixa só**, que continua de onde parou a cada trecho (como no Bruxelas REV4).

| Seção | Na prévia | Música no total | O que está na tela | Clima | Filtros na biblioteca |
|---|---|---:|---|---|---|
| **G · Abertura** | 0:00–0:28 | 28 s | Gancho narrado: Rozenhoedkaai, carruagens, waffle, batata, Basílica, Belfort, compra do bilhete | Empolgante, sobe e **termina no corte da compra do bilhete** (seu pedido) | Gênero: Cinematográfica ou Pop · Clima: Inspirador ou Feliz · duração ≥ 1:30 |
| **M1 · Chegada e o primeiro waffle** | 1:10–1:30 · 1:55–2:13 | 39 s | Da estação ao Chez Albert (praça, canal no parque, ruazinha, a Marina andando, torre da igreja); vocês comendo o waffle no banco | Leve, curiosa, de manhã | Gênero: Country e folk · Clima: Feliz ou Brilhante · 95–110 BPM |
| **M2 · Markt, Burg e canais: o conto de fadas** | 2:41–2:54 · 3:43–4:02 · 4:38–5:08 · 5:46–6:09 | 86 s | Chegada no Markt, carruagens, fachadas coloridas, Belfort, Burg, Basílica dourada, canais, Rozenhoedkaai, a Marina e a carruagem | Encantadora e empolgante ("achando tudo encantador") | Gênero: Cinematográfica ou Clássica · Clima: Inspirador, Feliz ou Brilhante · duração ≥ 2:00 |
| **M3 · Fome, chocolate e a batata** | 7:31–7:48 · 8:10–8:29 · 9:53–10:10 | 52 s | Canais e chocolateria, fachada do Fritbar; o restaurante e o prato; os waffles do Chez Albert e a carruagem no Begijnhof | Animada, gostosa | Gênero: Jazz e blues · Clima: Funky ou Feliz · 105–120 BPM |
| **M4 · Minnewater: o descanso** | 10:58–11:18 | 20 s | O lago, o castelinho, vocês acenando, a Marina na beira da água | Calma ("a gente vai descansando") | Gênero: Ambiente, Clássica (piano) ou Country e folk · Clima: Calmo ou Romântico · 65–85 BPM |
| **M5 · O teste dos waffles e a despedida** | 11:18–11:32 · 11:58–12:02 · 13:03–13:15 | 29 s | House of Waffles (fachada, cardápio, preparo); o time-lapse da Marina soprando o waffle quente; a cerveja no bar | Brincalhona, quase cômica (o time-lapse pede graça) | Gênero: Infantil ou Jazz e blues · Clima: Funky ou Feliz · 100–120 BPM |
| **F · Fechamento e tela final** | 14:08–15:17 | 69 s | Narração do fechamento sobre as paisagens do dia + 20 s de tela final | Nostálgica, quente | Gênero: Cinematográfica, Pop ou Country e folk · Clima: Inspirador ou Romântico · duração ≥ 1:30 |

**Evite** as duas faixas do vlog de Bruxelas ("Good Mornin' Miss Eliza", The Mini Vandals; "Time", The Grey Room), para cada cidade ter a sua trilha.

## 3. Como vai entrar (mixagem)

`docs/VIDEO_LONGO_YOUTUBE.md`, seção 3:
- Paisagem sem fala: música 3 dB abaixo da fala média do vídeo. Entra em 0,25 s e sai em 0,5 s dentro de cada trecho.
- Com fala (gancho e fechamento, sob a narração): 9 dB abaixo da voz (o documento pede 8–10 dB; em Bruxelas você pediu 15 dB, "voz audível": diga se quer igual a Bruxelas).
- Time-lapse e cerveja no bar: a música entra por cima do som ambiente, que fica baixo.
- Master −14 LUFS, pico ≤ −1 dBTP.

## 4. Decisão sua

- **Torre da igreja (7:10–7:16 na prévia):** você fala "uma das maiores torres de tijolos do mundo" sobre 6 s de plano da torre, entre duas selfies. Pela sua regra caberia música por baixo da fala, mas seriam 6 s de música entrando e saindo entre duas falas para a câmera. Deixei **sem música**. Se quiser, eu ponho a M3 baixinha só nesse plano.
