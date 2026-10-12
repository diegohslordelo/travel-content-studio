# QA · Reel trailer de Barcelona · REV3

**Entrega:** `reel_barcelona_trailer_rev3.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, 28,50 s (684 quadros).

**Pedido do Diego (11/10/2026):** trocar só o plano da Catedral por paisagem de Barcelona, com a voz dele ou da Marina por cima. O resto é a REV2 sem mudança (mesmos planos, cortes, legendas e posições).

## Mudança

| REV2 | REV3 |
|---|---|
| P04 · Catedral, os dois falando para a câmera (6,46 s) | **P04** · passeio até o Arco do Triunfo, Diego de costas (9:25,85–9:28,78) + **P04b** · Arco de baixo para cima (9:28,88–9:32,12) = 6,17 s |
| Voz: "Essa catedral é bem famosa… Game of Thrones." | Voz por cima: "E viemos ver o Arco do Triunfo daqui de Barcelona, que é lindíssimo. Olhem o visual." (9:15,04–9:20,76, gravada no mesmo passeio, pouco antes dessas tomadas) |

- **Contexto verdadeiro:** a fala é sobre o Arco do Triunfo e a imagem é o Arco, no mesmo passeio, sem trocar de lugar.
- **Voz e imagem:** a voz não sincroniza com nenhuma boca, porque não há ninguém falando para a câmera.
- **Corte entre as duas tomadas:** é só de imagem, no meio da frase. O áudio continua sem emenda.

## Verificação do arquivo final

| Item | Resultado |
|---|---|
| Falas inteiras | Áudio do Reel transcrito de novo (large-v3): todas as frases completas |
| Barceloneta → passeio | Só ambiente no corte (−30 a −34 dB); a voz começa 0,24 s depois |
| Passeio → Arco | Corte só de imagem; áudio contínuo |
| Arco → pombos | O "visual" termina 0,2 s antes do corte; só ambiente no corte (−29 dB) |
| Margens da voz | 0,24 s antes ("né?" termina em 9:14,46, o corte é em 9:14,80) e 0,2 s depois (próxima fala em 9:21,52) |
| Legendas | "E viemos ver / o Arco do Triunfo" entra em 9:15,04, no início medido da voz. "daqui de Barcelona, / que é lindíssimo." entra na fala contínua (transcrição) e atravessa o corte de imagem até "Olhem o visual." (9:19,98, início medido depois do silêncio) |
| Técnico | 684 quadros; vídeo e áudio 28,50 s; −14,2 LUFS; pico −1,5 dBTP (DS 4.6: ≤ −1 dBTP) |
| Imagem | Folha de quadros revisada; P04 com o Arco centrado (recorte x 1388), P04b x 1312; nenhum quadro de outra tomada nas bordas (cortes de cena do original em 565,79, 568,83 e 572,17) |

**Exceção registrada:** o grupo "E viemos ver / o Arco do Triunfo" tem 7 palavras, e o DS 3.2 pede até 6. Separar quebraria "Arco | do Triunfo" (DS 3.1: nunca no meio de expressão), e "E viemos ver" sozinho ficaria só 0,4 s na tela. Cada linha tem até 17 caracteres (limite: 26).

## Pendências

1. **Escuta do Diego antes de postar.** O Claude não escuta áudio: cortes e sincronia foram verificados por medição e transcrição.
2. **Trilha:** biblioteca do Instagram, 8 a 10 dB abaixo da voz (DS 4.6).
