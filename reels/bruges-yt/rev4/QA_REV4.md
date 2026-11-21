# QA · REV4 · Vlog de Bruges (vídeo longo do YouTube)

| Campo | Valor |
|---|---|
| Parte de | REV3 (`rev3/`, não alterada): mesmas músicas, mesmos objetos |
| Data | 21/11/2026 |
| Duração | **15:24,3** (REV3: 15:25,1) |
| Estado | Prévia para aprovação (540p, com música, narrações como texto) |

## 1. O que você pediu e o que foi feito

| Pedido | Feito |
|---|---|
| "Tem um momento (acho que no House of Waffles) que ficou meio estranho, acho que você tem algum frame perdido" | Varri a prévia quadro a quadro (trocas de imagem de 1 quadro, movimento forte por 3+ quadros, borrão). Achei 5 trechos de câmera virando/girando que estavam no material e 2 falhas minhas (tabela abaixo). Todos corrigidos |
| "Revise o áudio e os inícios e términos do vídeo e veja se não tem nada fora de lugar" | Conferência medida em `audio/CONFERENCIA_AUDIO_REV4.md`. Achei e corrigi: 2 "E" soltos antes de montagens com música; a música da abertura passando 0,12 s do corte; as duas músicas se sobrepondo na entrada da House of Waffles |
| Tirar a dica do fim e pôr outra: dormir uma noite na cidade para aproveitar Bruges mais vazia | F7 nova (`ROTEIRO_NARRACAO_REV4.md`): "Dica: se puder, durma uma noite em Bruges. De manhã cedo e à noite, quando os grupos de bate-volta vão embora, a cidade fica bem mais vazia." Na tela: rua tranquila e a Marina numa ruela vazia, com a nota "dica: durma 1 noite em Bruges" |

### O que estava fora do lugar

| Na REV3 | Fonte | O que era | Correção |
|---|---|---|---|
| 1:12 | 0:51,5 | "E" solto antes da montagem com música (a frase só continuava 20 s depois) | Cortado: fica "…vamos aproveitar aqui agora." e, depois da música, "Como nossa primeira parada…" |
| 2:16 | 1:58,8 | 1,2 s da câmera virando para o chão (pés) e depois para a selfie, com a fala já começando | A imagem para no último quadro de você comendo o waffle e o som segue (quadro congelado, 1,2 s) |
| 2:57 | 2:40,7 | 5 quadros tortos no começo da selfie do Markt | Cortados (a fala começa depois) |
| 6:12 | 6:06,5 | câmera virando da traseira para a selfie antes da fala da Basílica | Cortada (0,25 s) |
| 9:50 | 10:04,3 | "E…" esticado antes da montagem com música | Cortado |
| 11:09 | 11:29,2 | câmera girando no fim do aceno no Minnewater, 7 s antes da House of Waffles | Cortada (0,54 s) |
| 11:16 | — | **minha:** na entrada da House of Waffles, a música do Minnewater ainda saía quando a dos waffles entrava (0,25 s as duas juntas) | Troca seca no corte: uma termina, a outra começa |
| 12:00 | — | **minha:** o fim do time-lapse encostava na troca de cena da fonte | 1 quadro para dentro de cada lado |
| 13:13 | 13:48,0 | chicote borrado do bar para a rua | Cortado (0,54 s) |
| 0:31 | — | **minha:** a música da abertura passava 0,12 s do corte e encostava no "Acabamos de chegar" | Termina seco no corte |
| 15:05 | — | **minha:** na virada de página do fim, o vídeo continuava rodando 0,7 s depois do take (aparecia a câmera girando e o plano seguinte da fonte) | A página vira sobre o último quadro, congelado; o take do aceno termina antes da câmera girar |

Cada corte perto de fala foi conferido com uma 2ª transcrição: a palavra continua inteira ("…vamos aproveitar aqui agora.", "Chegamos aqui agora na Marketplace", "Uma coisa que eu não mencionei…", "Pra fechar nosso dia…").

## 2. Para aprovar

| O quê | Onde |
|---|---|
| Vídeo inteiro | `previas/rev4_previa_540p.mp4` |
| Fechamento com a F7 nova (contador) | `previas/rev4_fechamento.mp4` |
| Conferência do áudio | `audio/CONFERENCIA_AUDIO_REV4.md` |
| Efeitos e takes | `efeitos_rev4.md`, `takes_rev4.md` |

## 3. Pendências

- Gravar a F7 nova (e o resto do fechamento, se ainda não gravou) — `ROTEIRO_NARRACAO_REV4.md`.
- Mandar a atribuição das 7 faixas (`rev3/MUSICA_REV3.md`).
- Escuta: a medição não acha mais nada, mas a validação auditiva é sua.

## 4. Como refazer

De `reels/bruges-yt/`, com o ambiente de `CONTINUAR_BRUGES.md`: `python -I scripts/decupar.py rev4`, `python -I rev4/montar_rev4.py`, `bash rev4/renderizar_previa_rev4.sh`, `python -I rev4/conferir_audio_rev4.py`, `python -I rev4/previas_narracao_rev4.py fechamento`.
