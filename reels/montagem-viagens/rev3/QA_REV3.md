# Montagem de viagens · REV3 (13/11/2026)

Parte da REV2. Pedidos do Diego: (1) incluir os 3 takes enviados por ele (IMG_0455 asa do avião, IMG_0452 selfie no avião, IMG_3406 brinquedo); (2) **asa do avião como abertura**; (3) variar os takes dele com a Marina, que estavam quase iguais (todos selfies); (4) verificar a centralização de tudo; (5) IMG_3406 na vertical original, sem girar.

Mesmos 25 cortes da referência (10,667 s, 30 fps): detecção de cena no arquivo final = 24 cortes nos mesmos quadros. Sem música, texto ou CTA.

**Takes de Diego e Marina (variados):** selfie no avião (2) · Marina se virando na praça de Bruges, câmera de fora (5) · selfie com a Torre Eiffel (6) · Diego de costas andando no Louvre (18) · Marina andando à noite em Lisboa (21) · os dois gritando no brinquedo, visto de baixo (22) · Marina emocionada no show (24). Saíram as selfies parecidas da Disney, de Florença e de Amsterdam.

| # | Início–fim (s) | Quadros | Take | Arquivo · entrada (s) · centro x |
|---|---|---|---|---|
| 1 | 0.000–0.833 | 25 | asa do avião (abertura) | Upload__IMG_0455.mov · 2.0 · centro |
| 2 | 0.833–1.833 | 30 | Diego e Marina no avião | Upload__IMG_0452.mov · 0.0 · centro |
| 3 | 1.833–2.233 | 12 | Lisboa, pastéis de nata | Lisboa__IMG_4291.MOV · 0.8 · 0.72 |
| 4 | 2.233–3.000 | 23 | Veneza, gôndola no Grande Canal | Italia__IMG_6098.MOV · 0.0 · centro |
| 5 | 3.000–3.467 | 14 | Marina se vira na praça de Bruges | Bruges__IMG_2475.MOV · 2.75 · 0.59 |
| 6 | 3.467–3.833 | 11 | Diego e Marina com a Torre Eiffel | Paris__IMG_2761.MOV · 2.3 · 0.38 |
| 7 | 3.833–3.967 | 4 | Paris, Torre Eiffel | Paris__IMG_2754.MOV · 1.0 · 0.48 |
| 8 | 3.967–4.067 | 3 | Barcelona, Sagrada Família | Bruxelas__copy_0032E90A-CE40-40B8-9412-68C1B1BEC5F9.mov · 10.0 · centro |
| 9 | 4.067–4.200 | 4 | Roma, Coliseu | Italia__IMG_5260.MOV · 4.3 · centro |
| 10 | 4.200–4.333 | 4 | Amsterdam, canal | Amsterdam__IMG_1403-1.MOV · 3.5 · centro |
| 11 | 4.333–4.500 | 5 | Bruxelas, Atomium | Bruxelas__IMG_2168.MOV · 3.0 · 0.47 |
| 12 | 4.500–4.600 | 3 | Madrid, Palácio Real | Madrid__IMG_3722.MOV · 4.5 · 0.45 |
| 13 | 4.600–4.767 | 5 | Bruges, Rozenhoedkaai | Bruges__IMG_2491.MOV · 0.5 · centro |
| 14 | 4.767–4.867 | 3 | Lisboa, Praça do Comércio | Lisboa__IMG_4308.MOV · 0.5 · 0.62 |
| 15 | 4.867–5.067 | 6 | Roma, Fontana di Trevi | Italia__IMG_5071.MOV · 8.4 · centro |
| 16 | 5.067–5.267 | 6 | Bruxelas, Grand-Place | Bruxelas__IMG_2213.MOV · 1.0 · 0.52 |
| 17 | 5.267–5.500 | 7 | Disney, castelo | Disney__IMG_3346.MOV · 0.0 · 0.54 |
| 18 | 5.500–6.100 | 18 | Diego andando até a pirâmide do Louvre | Paris__IMG_3019.MOV · 1.5 · 0.8 |
| 19 | 6.100–6.867 | 23 | Disney, Main Street à noite | Disney__IMG_3575.MOV · 0.0 · 0.62 |
| 20 | 6.867–7.333 | 14 | Paris, Torre Eiffel iluminada | Paris__IMG_3177.MOV · 2.0 · centro |
| 21 | 7.333–7.667 | 10 | Marina andando à noite em Lisboa | Lisboa__IMG_4239.MOV · 1.8 · 0.4 |
| 22 | 7.667–8.100 | 13 | Diego e Marina gritando no brinquedo (vertical original, visto de baixo) | Upload__IMG_3406.mov · 1.1 · centro |
| 23 | 8.100–8.433 | 10 | fogos de Ano-Novo em Veneza | Italia__IMG_6157.MOV · 0.0 · centro |
| 24 | 8.433–9.233 | 24 | Marina emocionada no show, Diego ao lado | Disney__F2660F17-CD2A-4D28-8540-5E490866CCE3.mp4 · 13.6 · centro |
| 25 | 9.233–10.667 | 43 | fogos no castelo (final) | Disney__IMG_3607.MOV · 14.6 · 0.48 |

## Centralização
- `cx` = posição horizontal (0 a 1) do assunto na fonte. O recorte 9:16 é centrado nele, então o assunto cai no centro do canvas (x 540). Sem `cx`, o recorte é centrado na fonte.
- Verificado em `qa_frames/centralizacao_fonte_rev3.jpg` (janela de recorte na fonte, em vermelho) e em `qa_frames/folha_takes_rev3.jpg` (quadro do meio de cada plano no vídeo final, com o eixo x 540 em amarelo).
- Fontes já verticais (1, 2, 4, 8, 9, 10, 15, 22, 23, 24) entram inteiras. Não há como deslocar o enquadramento sem dar zoom: a asa (1) fica à esquerda e a Trevi (15) à direita, como foram filmadas.
- IMG_3406 (22): vertical original, sem rotação, como o Diego pediu.

## A confirmar
- Plano 8 (Sagrada Família): vem de uma compilação já editada de Barcelona (`copy_0032E90A…`, na pasta Bruxelas do Drive). Confirmar se é gravação do Diego e da Marina.
