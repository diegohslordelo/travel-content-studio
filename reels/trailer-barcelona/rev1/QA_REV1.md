# QA · Reel trailer de Barcelona · REV1

**Arquivo:** `reels/trailer-barcelona/rev1/reel_trailer_barcelona_rev1.mp4` (prévia: `reel_trailer_barcelona_rev1_previa_leve.mp4`) · **Capa:** `capa_reel_trailer_barcelona_rev1.jpg`
**Postagem:** Instagram, sábado 10/10/2026, 18:30 (p15), depois do vlog no YouTube às 11h.
**Pedido:** Diego, 08/10/2026: "baseado na programação de sábado, já monte o trailer do vídeo de Barcelona".
**Nível:** A (DS V2, 5.2). Mesmo motor do teaser (`reels/teaser-barcelona/rev3/scripts/teaser.py`).

## Ideia

O teaser deu os preços; o trailer vende a experiência e o veredito, com a voz de vocês: "Barcelona é praticamente de Gaudí", "todo canto daqui é sem nenhum defeito", "eu achei surreal", "vale muito a pena". Fecha com "VÍDEO COMPLETO NO YOUTUBE / SAIU HOJE". Não repete nenhum preço nem plano do teaser.

## Roteiro de cortes (24 fps, 462 quadros, 19,25 s)

| Reel | Imagem (master) | Som (master) | Na tela |
|---|---|---|---|
| 0–3,1 s | Fachada do Nascimento, Sagrada Família (24:24) | Diego no Park Güell (29:52): "Barcelona é praticamente de **Gaudí**" | Placa `3 DIAS EM / BARCELONA` + seta, com Chegada |
| 3,1–7,0 s | Marina perto do Arco do Triunfo (9:03) | a própria fala | "Eu juro," · "todo canto daqui" · "é sem nenhum defeito." |
| 7,0–7,7 s | Bairro Gótico (14:30) | Marina, contínua | "As ruas são" |
| 7,7–8,3 s | Casa Batlló (21:05) | Marina, contínua | "lindas, lindas, lindas." |
| 8,3–9,0 s | La Pedrera (22:16) | Marina, contínua | |
| 9,0–13,5 s | Diego saindo do Park Güell (32:05) | a própria fala | "Eu nunca tinha vindo aqui," · "ela já tinha vindo." · "Eu achei **surreal**" · "Surreal, de verdade." |
| 13,5–16,5 s | Aeroporto (33:42) | a própria fala | "**Vale** muito a pena." · "Saiba que você" · "não vai se arrepender." |
| 16,5–19,25 s | Sagrada Família por fora (25:48) | mudo (música do Instagram) | Placa `VÍDEO COMPLETO NO YOUTUBE / SAIU HOJE` + seta, com Chegada |

7 cortes secos, nenhum freeze e nenhuma transição.

## Decisões (com o motivo)

| Decisão | Motivo |
|---|---|
| **Sem `€ [total]` no gancho** | O vlog não mostra o total dos 3 dias (CLAUDE.md, 9: não inventar). O gancho virou uma Afirmação falada (DS 5.1), com 6 palavras |
| **Fala do Park Güell sobre a fachada da Sagrada Família** | É a mesma viagem e o mesmo dia; a Sagrada Família é obra de Gaudí, então a frase não muda o sentido. A selfie do Park Güell é bem mais fraca como primeira imagem |
| **3 cortes rápidos (0,6–0,75 s) sob "as ruas são lindas"** | São as "3 melhores imagens" do plano p15, ditas pela Marina. O som dela é contínuo; só a imagem troca |
| **Crops e zoom para esconder textos antigos do vlog** | Os pins queimados ("Casa Batlló", "Pont del Bisbe", "(La Pedrera)") ficam fora do quadro: trechos sem o pin e, em La Pedrera, zoom 1,2 com crop pelo alto |
| **La Pedrera em 1336,3 s** | Trecho mais nítido do plano; em 1346 s a câmera está virando e o prédio borra |
| **Sem Carimbo nem Ticket** | O plano p15 pede "se o vídeo tiver". Nenhum perrengue real e nenhuma surpresa sem repetir o teaser |
| **Plano final mudo** | A Sagrada por fora tem a trilha do vlog; a música entra pela biblioteca do Instagram |

## Conferências automáticas (`relatorio_tecnico_rev1.json`)

| Teste | Resultado | |
|---|---|---|
| Formato | 1080 × 1920 · 24 fps · 462 quadros · 19,250 s · H.264 High + AAC 48 kHz | ✅ |
| Loudness | −14,2 LUFS, pico verdadeiro −1,0 dBTP (DS 4.6: ≤ −1) | ✅ (no limite) |
| Objeto parado fora da zona segura | 0 quadros | ✅ |
| Legenda sobre objeto | 0 quadros | ✅ |
| Legendas | ≤ 2 linhas · ≤ 26 caracteres · centradas em x 540 · mini-placas: Gaudí, surreal, Vale | ✅ |
| Placa de abertura | 849 × 219 px (máx. 872), x 72 · y 640 | ✅ |
| Placa CTA | 775 × 219 px, x 72 · y 640 | ✅ |

## O que fica com o Diego

1. **Música:** escolher na biblioteca do Instagram, baixa. O último plano está mudo de propósito.
2. **Sincronia:** os tempos vêm da transcrição automática; vale assistir uma vez com som.
3. **"Saiu hoje":** o texto só vale se o vídeo estiver no ar quando o trailer for postado (sábado, 18:30).
