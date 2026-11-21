# REV4 · Conferência do áudio (vlog de Bruges)

Medição feita por `rev4/conferir_audio_rev4.py` sobre a prévia da REV4. **Não é escuta**: o Claude não escuta áudio; a validação auditiva é sua.

## 1. Emendas da voz

- 80 trechos de áudio da fonte (gancho + corpo). Sobrepostos (voz dupla): **0**.
- Saltos de amostra suspeitos de estalo nas emendas (salto > 6× o nível da fala em volta): **0**.

## 2. Buracos de silêncio (≥ 300 ms abaixo de −60 dBFS)

- **0** em todo o vídeo.

## 3. Música por cima de fala do vlog

- Palavras da transcrição com música tocando ao mesmo tempo (acima de −45 dBFS): **3**: 5:47,8 "Uma", 10:06,0 "agora", 10:54,0 "Vai,".
- Fora da conta, de propósito: o gancho (a fala da Marina e a narração ficam com a música 9 dB abaixo) e o fechamento (narração a gravar).
- O Whisper às vezes põe uma palavra no lugar errado do tempo (ex.: "Uma" antes da montagem do Rozenhoedkaai, que na fonte é dita depois dela): esses casos aparecem aqui e são conferidos à mão.

## 4. Quadros congelados

- 2:15,3–2:16,4: voz a -24 dBFS (som segue)

## 5. Time-lapse

- 11:53,7–11:57,7: som da fonte a -240 dBFS (sem o som acelerado) · música a -25 dBFS

## 6. Começo e fim do vídeo

- Primeiros 0,25 s: música a -49 dBFS (entra no 1º quadro, em 0,25 s); 0,25–1,0 s: -40 dBFS.
- Últimos 3 s (tela final): a música sai; último 0,2 s a -49 dBFS.
- Duração do som final 924.274 s × imagem 924.274 s.

## 7. Nível do som final da prévia

- -16.6 LUFS integrados, pico de amostra -1.0 dBFS (o master final segue o padrão: −14 LUFS, ≤ −1 dBTP).

**Resultado:** 3 problema(s) medido(s). Ver os itens acima.

## Conferido à mão (os 3 itens do item 3)

| Na prévia | Palavra | O que é |
|---|---|---|
| 5:47,8 | "Uma" | Tempo errado do Whisper: o "Uma coisa que eu não mencionei" é dito depois da montagem do Rozenhoedkaai (6:06,8 da fonte), não antes. Não há fala por baixo da música |
| 10:06,0 | "agora" | A música da montagem termina exatamente quando você volta a falar ("agora que nós nos alimentamos…"); na fonte, até ali é silêncio digital (a montagem que você editou). Não há fala por baixo da música |
| 10:54,0 | "Vai," | Tempo errado do Whisper: o "Vai, Jacquin" da Marina é dito na House of Waffles (11:54,8 da fonte); no ponto marcado, a fonte é ruído baixo |

**Resultado final:** nenhum problema de áudio pela medição. Falta a sua escuta.
