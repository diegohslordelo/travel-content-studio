# QA · Reel do Atomium · REV2

**Veredito do Claude: pronto para a sua escuta.** O Claude não escuta áudio. Há 2 palavras para conferir (fim deste documento).

**Entrega:** `reel_atomium_rev2.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, **25,29 s** (607 quadros). Prévia leve: `reel_atomium_rev2_previa_leve.mp4`. Legenda do post: `LEGENDA_POST.md`.

## O que estava errado na REV1 (Diego, 12/10/2026) e a causa

| Problema | Causa | Correção na REV2 |
|---|---|---|
| Falas cortadas antes de terminar | Os cortes seguiam os tempos de palavra da transcrição. Depois de pausa, esses tempos erram até 0,5 s: o "1958" terminava em 48,20 na transcrição, mas a voz vai até 54,05 sem pausa; a reação da Marina "terminava" em 53,84 e vai até 54,05 | **Áudio contínuo e sem emenda:** um único trecho do IMG_2170 (36,85–62,14), a conversa inteira, do início ao fim de cada frase. Início e fim medidos por VAD (Silero) e energia na faixa da voz |
| Fora de contexto | Pedaços de frases de 3 arquivos | Uma conversa só, sem cortar nenhuma frase (a mesma lição da REV2 do trailer de Barcelona) |
| Muitos planos de 2–3 s, sem imersão | 11 planos em 30 s | **4 planos:** 4,8 · 12,7 · 3,7 · 4,1 s. A imagem só muda nas pausas da voz |

## Montagem

| Tempo | Plano | Imagem | O que se ouve (áudio contínuo do IMG_2170) | Na tela |
|---|---|---|---|---|
| 0,00–4,83 | P01 | IMG_2169: o Atomium inteiro no fim da avenida (11:15) | "E aí, basicamente, ele é um cristal de ferro aumentado…" | Placa `PRIMEIRO DIA EM / BRUXELAS` (Chegada, 0–2,4 s) → ticket **SABIA?** (2,6–4,75 s) |
| 4,83–17,50 | P02 | Selfie dos dois (11:16), contínua, com o recorte na Marina, que é quem fala | "…de 165 bilhões de vezes. Ele foi feito com a experiência pra uma exposição aqui em 1958. E eu já falei pro Diego, eu falei: sério, em 1958? Porque você olha de perto e parece uma coisa tão moderna assim." | Destaques **165** e **1958** |
| 17,50–21,17 | P03 | IMG_2178: o Atomium inteiro contra o céu | Diego: "É, ele é realmente muito enorme, muito moderno e muito bonito." | — |
| 21,17–25,29 | P04 | Selfie, com o recorte no Diego | "E aí agora a gente vai continuar a nossa jornada por Bruxelas." O fim volta para a imagem do início (loop) | — |

**Ideia única:** o Atomium é um cristal de ferro de 1958 que parece moderno (Curiosidade, R09 do manual de formatos; gancho do tipo "Você sabia…?", referência 3.3).

**O que saiu, e por quê:**
- "Bom dia, Bélgica!" (IMG_2143) e a fala do Diego sobre subir (IMG_2179): eram pedaços de outros arquivos, e quebravam a conversa e a ideia única.
- O preço da subida ("se eu não me engano, 18 euros") é dito sem certeza e o painel pede para não citar. O fato "dá para subir" ficou na legenda do post.

## Verificação no arquivo final (medida no próprio .mp4)

**Falas inteiras:** o áudio do Reel foi transcrito de novo (large-v3) e traz as 6 frases completas, sem palavra pela metade no início nem no fim.

| Ponto | Voz (VAD do Reel) | Folga |
|---|---|---|
| Início do Reel | a voz começa em 0,42 s; a fala anterior do original termina 0,45 s antes do início | 0,42 s |
| Corte P01 → P02 (4,83 s) | pausa 4,45–5,15 | 0,38 / 0,32 s |
| Corte P02 → P03 (17,50 s) | pausa 17,06–17,79 | 0,44 / 0,29 s |
| Corte P03 → P04 (21,17 s) | pausa 20,77–21,47 | 0,40 / 0,30 s |
| Fim do Reel (25,29 s) | a energia da voz some em 24,72; o VAD marca até 25,02 | 0,57 s |

**Legendas:**
- Todas as falas estão legendadas.
- Cada grupo entra inteiro (DS 3.3, freio 4: fala rápida acima de 3 palavras/s), no início medido da voz. Depois de pausa, o início vem do VAD do Reel. No meio de fala contínua, vem da transcrição do Reel e da janela do original, que concordam em ±0,05 s. Nenhum grupo entra antes da voz.
- Todos os grupos têm até 6 palavras, até 26 caracteres por linha e a linha de cima menor ou igual à de baixo (o script trava se alguma regra falhar).
- Os 2 destaques ficam 3,5 s um do outro.

**Imagem:**
- Na selfie, o Diego (0,31–0,48 da largura) e a Marina (0,51–0,67) não cabem juntos num recorte 9:16 (0,32). As posições foram medidas por detecção de rosto a cada 0,5 s.
- O recorte fica em quem fala: a Marina em P02 e o Diego em P04. O outro aparece em parte.
- Nada fora de x 72–944 · y 256–1440.

**Técnico:** 607 quadros; vídeo e áudio com 25,29 s; −14,2 LUFS; pico −1,5 dBFS (DS 4.6).

## Checklist (referência, 4; DS 7.3)

| Item | Resultado |
|---|---|
| 100% original, sem marca d'água | ✅ |
| Gancho nos 3 primeiros segundos | ✅ O Atomium inteiro no quadro 0 + placa; "ele é um cristal" em 2,0 s e "de ferro" em 3,2 s. O "E aí, basicamente," da abertura é a fala real e não foi cortado. É o ponto mais fraco do gancho |
| Funciona sem áudio | ✅ Todas as falas legendadas |
| Uma ideia | ✅ |
| Duração 7–30 s | ✅ 25,3 s |
| Para quem enviar | Quem vai a Bruxelas ou à Bélgica |
| Placa x 72 · y 640 com Chegada | ✅ |
| 1 ticket, 0 carimbo, em cena sem rosto | ✅ |
| Transições | ✅ 3 cortes secos (100%) |
| Efeitos | ✅ Grão 5% + scrim |
| Placar | — Sem registro de gasto em Bruxelas (DS 2.5) |
| Placa de fechamento + bordão | — Não entra: o Atomium foi a 1ª parada, não o fim do dia, e a conversa termina em "vamos continuar". Decisão do Diego (DS 5.2, Nível A) |

## Para conferir na escuta

1. **0,4–2,7 s:** "E aí, basicamente, ele é um cristal". As transcrições se dividem: large-v3 (5 passadas) e turbo dizem "basicamente, ele é"; medium e large-v2 dizem "ele basicamente é". A legenda usa a primeira.
2. **12,0 s:** "E eu **já** falei pro Diego". As transcrições se dividem: medium, turbo e a passada do arquivo inteiro dizem "já"; as passadas do large-v3 no trecho dizem "até". A legenda usa "já".

## Como renderizar

```
cd reels/atomium
PD_BRUXELAS=PASTA_COM_OS_MOV python3 rev2/scripts/atomium.py --fontes PASTA_TTF --qa
```
