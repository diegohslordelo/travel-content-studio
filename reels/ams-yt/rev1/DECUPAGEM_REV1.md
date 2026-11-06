# REV1 · Decupagem (o que saiu do vídeo e por quê)

Fonte: `1016_sem_musica.mp4` (32:43.8). Corpo decupado: 31:35.7 (−68.1 s em 131 cortes). Gerado por `scripts/decupar.py` a partir de `rev1/decisoes_rev1.json`.

## Cortes manuais (pedidos e acidentes de câmera)

| Fonte | Vídeo final | Dura | Motivo |
|---|---|---:|---|
| 00:47.5–00:47.9 | 01:13.4 | 0.42 s | [visual] giro da câmera com a mão na frente da lente (tour do quarto, 0:47) |
| 05:56.6–06:08.0 | 06:12.0 | 11.36 s | [pedido do Diego] trecho do 'daora' em que a Marina fala 'tira isso daí' (5:56–6:08); a fala segue 'A prioridade aqui é a bicicleta. / As casinhas aqui são muito bonitinhas. Muito massa.' |
| 10:08.2–10:08.5 | 10:10.2 | 0.25 s | [visual] câmera encosta no rosto da Marina (10:08) |
| 13:06.4–13:07.2 | 13:04.4 | 0.88 s | [visual] câmera passando de mão, borrada (13:06); sai junto o 'Segura aqui' |
| 13:31.3–13:34.6 | 13:28.5 | 3.25 s | [McCrispy] encurta a mastigação antes do 'Não' para caber o rufar (ficam a mordida e ≈ 4,2 s de mastigação até o 'Não') |
| 22:34.3–22:34.7 | 22:13.2 | 0.38 s | [visual] câmera girando de cabeça para baixo (22:34) |
| 27:59.3–28:00.2 | 27:30.2 | 0.95 s | [visual] câmera vira para o chão e mostra os pés (27:59) |
| 28:49.8–28:53.2 | 28:18.6 | 3.42 s | [pedido do Diego] 'Saímos, tomamos a cerveja e' (28:50): o trecho começa no 'agora estamos aqui' |
| 08:03.4–08:03.7 | 08:07.3 | 0.25 s | **Congelado, não cortado.** [visual] câmera virando no começo do plano da Kalverstraat (8:03); o 'Ui' já começou, então a imagem congela no primeiro quadro bom em vez de cortar a palavra |

## Pausas tiradas automaticamente

123 cortes, 46.7 s no total. Regra: dentro de trechos falados, a pausa medida pela energia da voz (150–4000 Hz, abaixo do piso local + 8 dB) fica com 180 ms depois da fala e 120 ms antes da próxima; nunca há corte sobre o início de uma palavra; perto de um corte de cena, cada plano fica com pelo menos 0,5 s.

| Tipo | Cortes | Tempo |
|---|---:|---:|
| pausa na fala | 123 | 46.7 s |

Lista completa (quadro a quadro): `rev1/edl_rev1.json`, campo `removidos`.

## Revisados e mantidos

- 00:47 e 00:57 da fonte (tour do quarto): o giro em 00:57 fica, porque você fala durante ele ("é isso, vamos lá").
- 04:28–04:35, 08:33–08:37, 13:07–13:19 e 18:22–18:25: trechos em preto e branco do seu editado. Mantidos como estão.
- 21:25–21:44 (piscina vazia do Vondelpark, plano parado): mantido porque a explicação da piscina é falada sobre ele.
- 28:10–28:12 (câmera perto do rosto na FEBO): mantido porque a fala continua ("você abre a portinha…").
- 08:03: a câmera vira no começo do plano da Kalverstraat, mas o "Ui" já começou. A imagem congela por 6 quadros em vez de cortar a palavra.

## Ordem e o que mudou de lugar

- Nada mudou de ordem. A ordem invertida que você fez na Heineken (fachada antes do O'Donnell's) foi mantida, e o trecho começa em "agora estamos aqui".
- McCrispy: a mastigação entre "do Brasil" e "Não" tinha 7,5 s (a transcrição com filtro de voz errava esse tempo; conferi sem o filtro). Ficaram a mordida e 4,2 s de mastigação, o espaço do rufar.
