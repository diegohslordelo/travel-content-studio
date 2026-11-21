# QA · REV3 · Vlog de Bruges (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV2 (`rev2/`, não alterada). **Só a música muda**: cortes, objetos, gancho, fechamento e roteiro das narrações são os da REV2 |
| Data | 21/11/2026 |
| Duração | 15:25,1 (a mesma da REV2) |
| Estado | Prévia para aprovação, 540p, com música; narrações ainda como texto (roteiro em `rev2/ROTEIRO_NARRACAO_REV2.md`) |

## O que você pediu e o que foi feito

| Pedido | Feito |
|---|---|
| "Coloque músicas um pouco mais animadas, achei muito lentas" | 6 das 7 faixas trocadas pelas mais animadas do lote, medidas por andamento, percussão, ataques e força da batida. Cada seção agora entra na parte cheia da faixa, sem as introduções calmas. Detalhes e o antes/depois em `MUSICA_REV3.md` |

## Para aprovar

| O quê | Onde |
|---|---|
| Só os trechos com música (nome da faixa no canto) | `previas/rev3_musica_secoes.mp4` |
| Vídeo inteiro | `previas/rev3_previa_540p.mp4` |
| Faixas, porquê e prompt opcional para buscar faixas ainda mais animadas | `MUSICA_REV3.md` |

## Pendências

As da REV2 continuam (`rev2/QA_REV2.md`, seção 5): gravar o fechamento novo (F1–F9), mandar a atribuição das faixas escolhidas (agora as 7 da REV3) e responder as decisões pendentes.

## Como refazer

De `reels/bruges-yt/`, com o ambiente de `CONTINUAR_BRUGES.md`: `python -I scripts/decupar.py rev3`, `python -I rev3/montar_rev3.py`, `bash rev3/renderizar_previa_rev3.sh`, `python -I rev3/cortes_musica_rev3.py`.
