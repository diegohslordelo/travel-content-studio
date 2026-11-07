# QA · REV4 · Vlog de Bruxelas (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV3 (`rev3/`, não alterada). Os cortes, a imagem, os objetos, as narrações, os níveis de voz e a legenda são os mesmos. **Muda só a música, mais duas emendas de voz** |
| Data | 07/11/2026 |
| Estado | **Versão final em 4K** (`_tmp/rev4_final_4k.mp4`, entregue por link; substitui o 4K da REV3). Falta a escuta (`audio/RELATORIO_AUDIO_REV4.md`: AGUARDANDO ESCUTA) |

## 1. Pedido do Diego (07/11/2026) e o que foi feito

| Pedido | Causa encontrada | Feito |
|---|---|---|
| "depois que você colocou minha fala do hotel, ficou estranho o som de fundo, como se tivesse um cd arranhado" | Na REV3, a música do corpo era tirada da **diferença** entre os dois exports (o "(2)", com música, menos o de fala). Onde as duas versões não batem amostra a amostra, sobra resíduo da voz e da compressão: era esse o "arranhado" | A música vem do **arquivo limpo** que o Diego mandou ("Time", The Grey Room / Clark Sims), no ponto exato da faixa |
| "nos takes do restaurante do waffle as músicas também estão sobrepostas"; "no Manneken Pis também tá, parece que o vídeo já tava com áudio e vc jogou a música por cima" | Na REV3, cada bloco de música tocava contínuo do começo ao fim, inclusive debaixo das falas de vlog (de 4:50 a 5:56 da fonte, uma faixa só passando por cima do waffle). Medido: **69 s de música sobre fala de vlog** no corpo | A música só toca onde o "(2)" tem a música no volume cheio. Ali, o Diego deixou o som do clipe mudo (o export de fala é silêncio digital). Onde ele fala, a música do "(2)" some ou fica a −28 dB, e na REV4 não toca. Medido: **0 s de música sobre fala de vlog** |
| "siga estritamente o minuto das músicas do arquivo (2)" | — | Cada trecho foi localizado por correlação cruzada (`scripts/achar_musica.py`): o deslocamento da faixa no "(2)" é exato (dispersão de 0 ms). Conferência no arquivo: correlação de 0,99 a 1,00 com o "(2)", defasagem < 1 ms |
| "waffle, 6:21 tem que entrar a música" | No "(2)", a faixa sobe para o volume cheio em 349,2 s da fonte (6:20,9 do vídeo) | Entra às **6:21,0** |
| "você só vai adicionar a música do final e do início (The Mini Vandals)" | Na REV3, o gancho e o fechamento eram 2 trechos dessa faixa tirados do export e costurados (3 emendas) | "Good Mornin' Miss Eliza" (The Mini Vandals) do arquivo limpo, **contínua e sem costura**. Gancho a partir de 45,07 s da faixa; fechamento e tela final a partir de 7,50 s (os mesmos pontos de entrada da REV3) |
| "revise o áudio do vídeo, tem que estar perfeito, sem sobreposição" | (1) No gancho, 0:10,1–0:12,1 (fonte 181,05), o som da fonte tinha você falando a −14 dB por baixo da narração G2. (2) Em 3:13,2 e 14:36,0, o fim do plano cortava a cauda de uma palavra | (1) Esse plano fica sem o som da fonte. (2) A cauda ganha 90 ms e 60 ms, sobre o começo em silêncio do plano seguinte. Conferido: nenhum plano sob narração com fala da fonte; nenhum buraco de silêncio |

## 2. A música do corpo na REV4

As 8 janelas das faixas limpas (o que o "(2)" tem no volume cheio, entre as falas):

| Trecho | Faixa | Fonte (s) | Vídeo | Ponto da faixa (s) |
|---|---|---|---|---|
| T1 Fritland → Grand Place | Time | 203,00–226,30 | 3:55,9–4:19,2 | 0,23–23,53 |
| T2 Grand Place → hotel (narração H1) | Time | 290,85–310,85 | 5:23,3–5:43,2 | 23,55–43,50 |
| T3 Zinneke → waffle | Time | 325,75–334,19 | 5:57,8–6:06,2 | 58,45–66,89 |
| T4 waffle | Time | 349,34–356,59 | **6:21,0**–6:28,3 | 82,04–89,29 |
| T5 Galerias Saint-Hubert | Time | 421,25–437,70 | 7:31,6–7:48,0 | 89,35–105,80 |
| E1 Manneken Pis | Mini Vandals | 463,05–470,70 | 8:13,4–8:21,0 | 0,02–7,67 |
| E2 Manneken Pis → Mont des Arts | Mini Vandals | 520,75–557,45 | 9:11,1–9:47,8 | 7,55–44,25 |
| E3 Mont des Arts | Mini Vandals | 618,50–645,40 | 10:46,7–11:13,2 | 44,57–71,07 |

Mais 4 trechos só de música do "(2)", com **outras músicas** que não são das 2 faixas (correlação ≈ 0,1 com as duas; o de 11:41 e o de 13:23 parecem ser a mesma música). Nesses trechos o export de fala é silêncio digital, então o som do "(2)" é a música pura e entra direto, no mesmo minuto, sem subtração: vídeo 1:03,4–1:22,5 (Atomium), 2:23,2–2:33,7, 11:41,8–11:52,1 e 13:23,9–13:39,1. **Pendência:** os nomes dessas músicas (licença: precisam ser da Biblioteca de áudio do YouTube).

**Nível:** o mesmo da REV3. Corpo: música 3 dB abaixo da fala-alvo (−20,9 LUFS), com um ganho único por faixa; sob a narração do hotel, 15 dB abaixo. Gancho e fechamento: 6 dB abaixo sem voz e 15 dB abaixo com voz. Entrada em 0,25 s e saída em 0,5 s, dentro da janela.

## 3. Conferências (`rev4/conferir_audio_rev4.py`)

| Conferência | REV3 | REV4 |
|---|---|---|
| Música sobre fala de vlog (corpo) | 69,0 s | **0 s** |
| Música no corpo | 291,2 s | 201,1 s (só os 12 trechos de música do "(2)") |
| Buracos de silêncio (≥ 200 ms abaixo de −70 dBFS) | 0 | 0 |
| Sincronia com o "(2)" | — | 12 janelas: correlação 0,99–1,00, defasagem −0,3 a +0,7 ms |
| Plano sob narração com fala da fonte | 1 (0:10,1) | 0 |
| Arquivo final | 28.508 quadros, −14,1 LUFS, −1,2 dBTP | 28.508 quadros, imagem e som com 950,27 s, timestamps exatos, **−14,2 LUFS, −1,2 dBTP**, som decodificado sem erro |

## 4. Entregas

| Arquivo | O que é |
|---|---|
| `rev4_final_4k.mp4` (link, fora do git) | Vídeo para o YouTube: 3840 × 2160, 30 fps, H.264 (a imagem da REV3, copiada sem recodificar), AAC 192 kbps 48 kHz; MD5 `861beb91f0928a640ff16439188f8a17` |
| `rev4/mixar_rev4.py`, `rev4/finalizar_rev4.sh`, `rev4/conferir_audio_rev4.py` | Mixagem, montagem do arquivo final e conferências |
| `musica/` | As 2 faixas limpas que o Diego mandou (07/11/2026) |
| Legenda, descrição e thumbnails | As da REV3 (`rev3/legenda_rev3.srt`, `rev3/DESCRICAO_YOUTUBE_REV3.md`, `rev3/thumb/`): a fala não mudou |

## 5. Decisões e limites

- **Ambiente nos trechos de música:** segue o "(2)", onde o som do clipe fica mudo. Nas montagens, a música toca sozinha, como você editou.
- **Entre as janelas:** onde o "(2)" deixa a música baixinha sob a fala (−28 dB no waffle, por exemplo), a REV4 não põe música ("só nas partes que eu não estou gravando em vlog").
- **O Claude não escuta:** as conferências são medições. O ponto a ouvir com atenção é cada entrada e saída de música, porque agora a música começa e para junto com as falas, em vez de tocar contínua.
