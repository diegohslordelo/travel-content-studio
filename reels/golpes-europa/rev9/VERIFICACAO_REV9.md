# Verificação quadro a quadro · REV9

Gerado por `rev9/verificar.py` a partir do registro do `montar.py` e da leitura de todos os quadros do vídeo final.

**Conferência visual das trocas "fora de corte" que sobraram** (quadros vizinhos, um a um): todas são movimento dentro do mesmo plano, sem corte nem imagem perdida.
- A 88 / B 111 (dado, metrô de Barcelona): uma mão passa na frente da câmera.
- A 623 / B 646 (petição): a câmera gira da árvore para o rapaz de chapéu.

Os "cortes planejados sem troca forte" (A 1036 e 1098, B 1059 e 1121) são trocas entre planos de cor parecida (Puerta del Sol → Tío Pepe → Plaza Mayor). Os cortes existem; só a faixa de cor analisada muda pouco.

**Problemas da REV8 corrigidos aqui:**
- Quadros repetidos: a REV8 saía a 30 fps com gravações de 24 fps (1 quadro repetido a cada 4). A REV9 sai a 24 fps, com 0 quadros repetidos do Diego.
- Flashes: trechos de 0,15 a 0,2 s na decupagem. Agora o mínimo é 0,4 s.
- Fim de frase cortado. Agora a decupagem usa histerese e a última sílaba fica inteira.
- Chicotes de câmera no vídeo da petição. Agora só entram os trechos estáveis.
- Legenda piscando: 25 palavras de 1 quadro. Agora são 0.

## Gancho A · `rev9/golpes_rev9_ganchoA.mp4`

- **Diego:** 1120 quadros; 9 emendas (esperado 9, uma por corte da decupagem); 0 quadros repetidos.
- **Fundo:** 19 takes, o menor com 22 quadros (0.92 s); takes < 0,6 s: 0.
- **Vídeo final:** 1120 quadros lidos (esperado 1120); trocas de plano detectadas: 18; fora de corte planejado: 2 [88, 623]; quadros pretos: 0.
  - Cortes planejados sem troca forte de cor na faixa analisada (planos parecidos): [1098, 1036]
- **Legenda:** 174 estados; com menos de 2 quadros: 0 .
- **Duração (stream, s):** video,46.666667, audio,46.658000.
- **Resultado:** ERROS: vídeo final: contagem, troca de plano fora do corte ou quadro preto

| Início (s) | Bloco | Fundo | Duração (s) |
|---|---|---|---|
| 0.00 | gancho | g6_1357 a partir de 1.75 s | 3.00 |
| 3.00 | dado | g7_1538@metro a partir de 1.90 s | 2.29 |
| 5.29 | dado | g7_1538@veneza a partir de 10.20 s | 1.58 |
| 6.88 | relevancia | IMG_3647 a partir de 0.50 s | 3.00 |
| 9.88 | relevancia | g2_0739 a partir de 2.00 s | 1.79 |
| 11.67 | relevancia | g1_0738 a partir de 9.00 s | 1.96 |
| 13.62 | abertura | g4_0742 a partir de 6.40 s | 4.04 |
| 17.67 | golpe1 | g5_0744 a partir de 6.15 s | 3.25 |
| 20.92 | golpe1 | g5_0744 a partir de 29.95 s | 4.12 |
| 25.04 | golpe2 | g3_0740 a partir de 1.50 s | 1.25 |
| 26.29 | golpe2 | g3_0740 a partir de 4.00 s | 0.92 |
| 27.21 | golpe2 | g3_0740 a partir de 7.75 s | 2.71 |
| 29.92 | golpe2 | g7_1538@cachecol a partir de 18.60 s | 1.96 |
| 31.88 | golpe3 | IMG_3734 a partir de 0.40 s | 2.21 |
| 34.08 | golpe3 | IMG_3743 a partir de 0.30 s | 1.58 |
| 35.67 | golpe3 | IMG_3744 a partir de 2.20 s | 2.75 |
| 38.42 | moral | IMG_3634 a partir de 0.20 s | 4.75 |
| 43.17 | cta | IMG_3630 a partir de 0.20 s | 2.58 |
| 45.75 | cta | IMG_3647 a partir de 3.50 s | 0.92 |

## Gancho B · `rev9/golpes_rev9_ganchoB.mp4`

- **Diego:** 1143 quadros; 9 emendas (esperado 9, uma por corte da decupagem); 0 quadros repetidos.
- **Fundo:** 20 takes, o menor com 22 quadros (0.92 s); takes < 0,6 s: 0.
- **Vídeo final:** 1143 quadros lidos (esperado 1143); trocas de plano detectadas: 19; fora de corte planejado: 2 [111, 646]; quadros pretos: 0.
  - Cortes planejados sem troca forte de cor na faixa analisada (planos parecidos): [1059, 1121]
- **Legenda:** 177 estados; com menos de 2 quadros: 0 .
- **Duração (stream, s):** video,47.625000, audio,47.617000.
- **Resultado:** ERROS: vídeo final: contagem, troca de plano fora do corte ou quadro preto

| Início (s) | Bloco | Fundo | Duração (s) |
|---|---|---|---|
| 0.00 | gancho | g6_1357 a partir de 1.75 s | 2.92 |
| 2.92 | gancho | g2_0739 a partir de 0.60 s | 1.04 |
| 3.96 | dado | g7_1538@metro a partir de 1.90 s | 2.29 |
| 6.25 | dado | g7_1538@veneza a partir de 10.20 s | 1.62 |
| 7.88 | relevancia | IMG_3647 a partir de 0.50 s | 3.00 |
| 10.88 | relevancia | g2_0739 a partir de 2.00 s | 1.79 |
| 12.67 | relevancia | g1_0738 a partir de 9.00 s | 1.96 |
| 14.62 | abertura | g4_0742 a partir de 6.40 s | 4.04 |
| 18.67 | golpe1 | g5_0744 a partir de 6.15 s | 3.25 |
| 21.92 | golpe1 | g5_0744 a partir de 29.95 s | 4.08 |
| 26.00 | golpe2 | g3_0740 a partir de 1.50 s | 1.25 |
| 27.25 | golpe2 | g3_0740 a partir de 4.00 s | 0.92 |
| 28.17 | golpe2 | g3_0740 a partir de 7.75 s | 2.71 |
| 30.88 | golpe2 | g7_1538@cachecol a partir de 18.60 s | 1.96 |
| 32.83 | golpe3 | IMG_3734 a partir de 0.40 s | 2.21 |
| 35.04 | golpe3 | IMG_3743 a partir de 0.30 s | 1.58 |
| 36.62 | golpe3 | IMG_3744 a partir de 2.20 s | 2.75 |
| 39.38 | moral | IMG_3634 a partir de 0.20 s | 4.75 |
| 44.12 | cta | IMG_3630 a partir de 0.20 s | 2.58 |
| 46.71 | cta | IMG_3647 a partir de 3.50 s | 0.92 |

