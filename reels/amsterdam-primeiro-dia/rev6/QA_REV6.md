# QA · Reel "Primeiro dia em Amsterdam" · REV6 (03/11/2026) · versão para postar

**Veredito: pronto.** A REV6 é a REV5 (`../rev5/QA_REV5.md`, não alterada) com o gancho de volta ao ritmo da REV3, a pedido do Diego (03/11/2026): "O gancho no começo tem que ser como antes, aparecendo na medida que eu falo. Mas com o 'primeiro dia' aparecendo como logotipo". Mesma qualidade máxima (H.264 CRF 10, AAC 320 kb/s).

## O gancho

| Tempo | Entra | Como |
|---|---|---|
| 0,00 s | "ISSO É" | Anton branco |
| 0,00–0,36 s | Grade do dia | 9 vídeos, um a cada 0,045 s; fecha em "TUDO" |
| 0,36 s | "TUDO" | Anton branco, com o soco seco |
| 0,54 s | "O QUE FIZEMOS NO NOSSO" | Anton branco |
| 1,45 s | **Logotipo `PRIMEIRO DIA →`** | Placa da marca (DS V2, 2.1, Marca), x 72 · y 640, Chegada de 560 ms e brilho de esmalte |
| 2,19 s | "EM AMSTERDÃ" | Anton branco |
| 2,62 s | Saída da placa (240 ms, pela direita) | O mergulho no aeroporto começa em 2,54 s |

Tudo numa cor só (branco) e o logotipo no lugar das palavras "primeiro dia", como pedido na REV3. A capa é o quadro com a frase inteira e o logotipo (2,52 s).

## Sem o Placar

Pedido do Diego (03/11/2026): "tire o placar, só vai ter isso no vídeo do YouTube". Saem do Reel o Placar do Dia, as etiquetas de valor ao lado dele e os sons de moeda e tique (`cenas.json`: `sem_placar`). Os valores continuam registrados no `cenas.json` e na legenda do post, que volta ao total real do dia (€ 90,84, com a pizza).

O resto (cenas, Marina com o vinho, legendas, sons de transição e CTA) é igual à REV5.

## Medido no vídeo final

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 CRF 10 + AAC 320 kb/s 48 kHz, **60,57 s**, 322 MB ✅ |
| Áudio | **−14,1 LUFS**, pico **−1,3 dBTP**, 0 amostras acima de −1 dBFS, 0 em 0 dBFS ✅ |
| Legendas | 88 grupos de 1 linha; a maior com 806 px ✅ |
| Gancho | Quadros em 0,2 · 1,0 · 1,8 · 2,5 s: as linhas entram na fala e o logotipo em "primeiro dia" ✅ |
| Placar | Nenhum Placar, etiqueta ou som de moeda no vídeo ✅ |

Arquivos: `reel_amsterdam-primeiro-dia_rev6.mp4` (final), `reel_amsterdam-primeiro-dia_rev6_previa.mp4`, `capa_amsterdam-primeiro-dia_rev6.jpg`, `qa_frames/`. Legendas do post: `../legenda_post.md`.

## Pendências (decisão do Diego)

1. **Batata da Manneken Pis:** € 7,15 (Placar do vlog) ou € 7,50 (Recibo do vlog)? O Reel não mostra mais valores; só a legenda do post usa € 7,15.
2. **Escuta:** `keen` (2,72 s), volumes dos efeitos e as palavras de transcrição duvidosa ("um/o ônibus", "estava/tava", "vamos/fomos").
