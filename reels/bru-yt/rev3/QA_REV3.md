# QA · REV3 · Vlog de Bruxelas (vídeo longo do YouTube) — em andamento

| Campo | Valor |
|---|---|
| Parte de | REV2 (`rev2/`, não alterada): mesma decupagem, narrações, mixagem e duração (15:50,3) |
| Data | 06/11/2026 |
| Estado | **Versão final** (render em 1080p, `_tmp/rev3_final_1080p.mp4`, entregue por link). Falta a escuta (`audio/RELATORIO_AUDIO_REV3.md`: AGUARDANDO ESCUTA) e as correções do `.srt` |

## 1. O que mudou

| Pedido do Diego (06/11/2026) | Feito |
|---|---|
| "Quando o primeiro dia aparece, tem que aparecer a data no canto superior esquerdo: 15 de Março de 2026" | A data entra em **0:37,2**, junto com a placa "1 DIA EM BRUXELAS" (que entra 200 ms antes), e fica até 0:40,9 |
| "Coloque a data nas cores do placar, um pouco menor que essa placa" | A 1ª versão (placa de capítulo amarela, "DOMINGO · 2026 / 15 DE MARÇO") virou **"15 DE MARÇO DE 2026" no painel do Placar**: grafite, letras amarelas, fonte do Placar (56 px), 96 px de altura, o mesmo acender (80 ms com 1 quadro de flicker), na posição do Placar no 16:9 (x 96 · y 72). Cabe inteira numa linha (≈ 540 × 96 px, contra ≈ 620 × 164 px da placa). Sem som. Prévia: `previas/rev3_data_540p.mp4` (0:30–0:50) |

| Respostas aos pontos da REV2 (06/11/2026): "F1 remova; F3 mantenha; F4 mantenha; gancho, deixe como tá; deixe 18 euros" | **F1:** saiu "que era do lado" (corte de silêncio a silêncio, 6,09–6,765 s da gravação; o "e" ficou). Uma 2ª transcrição confirma: "…até a Grand Place e passamos pelas três estátuas…". F3 (o "hoje"), F4 (Paris), gancho (36,5 s) e o bilhete (€ 18) ficaram como estavam |
| (achado na legenda) | O take "Não tem condições" do gancho terminava em 457,00 s e pegava o começo do "Vamos" (som em 456,92 s, medido pela energia). Agora termina em 456,79 s, no silêncio, com a mesma duração (62 quadros) |

## 1b. Entregas da versão final

| Arquivo | O que é |
|---|---|
| `rev3_final_1080p.mp4` (link, fora do git) | Vídeo para o YouTube: 1920 × 1080, 30 fps, H.264 (CRF 19, até 12 Mbps), AAC 192 kbps 48 kHz |
| `legenda_rev3.srt` + `legenda_duvidas_rev3.md` | Legenda pt-BR (229 legendas, 0 linhas acima de 42 caracteres) e a lista do que ouvir antes de subir |
| `DESCRICAO_YOUTUBE_REV3.md` | 3 títulos para o teste A/B, descrição e 15 capítulos |
| `thumb/thumb_a.png`, `thumb_b.png`, `thumb_c.png` | 3 thumbnails (1280 × 720), sem valores reais: A = placa "QUANTO CUSTOU BRUXELAS?" + Recibo "€ ???"; B = só a placa; C = só "BRUXELAS" com o Atomium |
| `audio/RELATORIO_AUDIO_REV3.md` | Revisão de áudio no padrão, com os pontos de escuta |

## 2. Decisões e divergências

- **Componente:** a data é uma variação do Placar (DS 2.5), sem relógio e sem valor. O painel usa os mesmos valores do Placar (`estiloPainelPlacar`, exportado de `design-system/remotion/src/ds/Placar.tsx`); nenhum valor visual novo. Pela governança do DS (7.4), variação precisa do seu OK (você pediu).
- **Caixa-alta:** "15 DE MARÇO DE 2026", como os textos de destaque do DS. Se quiser "15 de Março de 2026" com minúsculas, é só trocar.
- **Posição:** é a mesma do Placar. Não há conflito, porque o 1º Placar de gasto só entra em 1:06.
- **Thumbnails:** A e B usam a selfie do Mont des Arts (você à direita, como pede o DS 5.5; a placa no canto superior esquerdo fica sobre o prédio). Nas selfies da Grand Place e do Atomium a placa cobria o seu rosto. A C usa o Atomium, sem placa (o DS pede a placa na thumbnail: decisão sua, como em Amsterdam). Só contraste +10 e brilho +18%, sem o preset de cor (pendência do DS).
- **Divergências que continuam:** música 15 dB abaixo da voz no gancho, no hotel e no fechamento (DS 4.6 pede 8–10 dB; pedido seu); gancho de 36,5 s (doc. do vídeo longo: ~20–25 s; você decidiu manter).
