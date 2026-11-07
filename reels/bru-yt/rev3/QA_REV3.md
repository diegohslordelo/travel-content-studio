# QA · REV3 · Vlog de Bruxelas (vídeo longo do YouTube) — em andamento

| Campo | Valor |
|---|---|
| Parte de | REV2 (`rev2/`, não alterada): mesma decupagem, narrações, mixagem e duração (15:50,3) |
| Data | 06/11/2026 |
| Estado | **Versão final em 4K** (07/11/2026, `_tmp/rev3_final_4k.mp4`, entregue por link; o 1080p de 06/11 fica substituído). Falta a escuta (`audio/RELATORIO_AUDIO_REV3.md`: AGUARDANDO ESCUTA) e as correções do `.srt` |

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
| `rev3_final_4k.mp4` (link, fora do git) | **Vídeo para o YouTube, em 4K** (pedido do Diego, 07/11/2026): 3840 × 2160, 30 fps, H.264 High (CRF 19, até 20 Mbps), AAC 192 kbps 48 kHz; 15:50,27, 28.508 quadros, −14,1 LUFS, −1,2 dBTP, 2,42 GB, MD5 `fa6c3e8ffd4c72d9735a5345eff525cd`. Script: `renderizar_final4k_rev3.sh` |
| `rev3_final_1080p.mp4` (06/11, fora do git) | Substituído pelo 4K |
| `thumb/thumb_d.png`, `thumb_e.png`, `thumb_f.png` | 3 thumbnails novas com a selfie do Atomium (pedido do Diego, 07/11/2026): D = placa "BRUXELAS" + seta; E = placa + Recibo "€ ???"; F = só "BRUXELAS" em Condensed 800 amarelo, sem placa |
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

## 3. Render final em 4K (07/11/2026)

| Item | Resultado |
|---|---|
| Receita | A do 4K de Amsterdam, a 30 fps: 16 partes em escala 2 lidas da fonte 4K (HEVC 10 bits, pelo `<OffthreadVideo>`), `CONCURRENCY=3`, `OFFTHREAD_CACHE_MB=1500`, x264 fast, CRF 19, até 20 Mbps; ~14 min por parte |
| Reinícios | O container reiniciou 3 vezes no meio de partes (10, 13 e 14). As partes prontas ficaram no disco e o script retomou do que faltava; as partes 14 a 16 saíram em 4 pedaços cada (`SUBPARTES=4`) |
| Sincronia | O 1º vídeo juntado tinha os quadros a partir de 12:52 (1º quadro da parte 14, a 1ª montada de pedaços) 42 ms atrasados em relação ao som (ou seja, o som adiantado). Corrigido nos timestamps, sem recodificar (pacotes idênticos), e a conferência entrou no script (`corrigir_ts_video.py`) |
| Medição | 28.508 quadros, imagem e som com 950,27 s, −14,1 LUFS, −1,2 dBTP, decodificação sem erro (relatório de áudio, seção 10) |
| Imagem | Conferida em 0:38 (data no painel do Placar e placa), 0:10 (recorte 1:1, detalhe da fonte 4K), 13:40 e 15:40 (tela final) |
| Ressalva | A imagem sai em faixa completa (`yuvj420p`, padrão do Remotion), como nos renders anteriores; o YouTube lê a marcação |

## 4. Thumbnails do Atomium (07/11/2026)

Foto enviada pelo Diego (selfie no Atomium, 1932 × 2576), recortada em 16:9 pela composição `ThumbYT` (contraste +10, brilho +18%, como nas outras). D e E têm a placa "M" no canto superior esquerdo, com margem 48 e acima do Atomium; o Recibo da E fica à direita, fora da zona proibida. A F tem o nome em Condensed 800, 168 px, amarelo, sem placa, no céu (x 48 · y 26), longe do sol. Para posicionar o nome, `ThumbYT` ganhou `tituloX`, `tituloY` e `tituloCentro` (o padrão continua x 48 · y 40; nenhum valor visual novo). **Divergência do DS 5.5:** nessa foto o Diego está à esquerda (o DS pede à direita). Não espelhei a foto, porque o Atomium e o cenário ficariam invertidos (contexto verdadeiro).

