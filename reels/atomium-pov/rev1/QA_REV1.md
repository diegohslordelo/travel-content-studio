# QA · Reel POV "15 segundos no Atomium" · REV1

**Entrega:** `reel_atomium_pov_rev1.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, 15,04 s (361 quadros). Prévia leve: `reel_atomium_pov_rev1_previa_leve.mp4`. Folha de quadros: `qa_frames/folha_de_quadros.jpg`.

**Pedido do Diego (12/10/2026):** um Reel POV do Atomium, sem falas, só com som ambiente e cortes rápidos, "apenas chegando". Simples, guiado pelo DS. Vai ser postado como "POV: 15 segundos no Atomium".

## Montagem (10 cortes secos, 1,0 a 1,6 s; o último plano longo é a chegada)

| Tempo | Plano | Arquivo (trecho) | Na tela |
|---|---|---|---|
| 0,00–1,58 | P01 | IMG_2169 (0,00), Atomium no fim da avenida | Placa `PRIMEIRO DIA EM / BRUXELAS` (Chegada; sai pela direita no corte) |
| 1,58–2,79 | P02 | IMG_2168 (0,40), avenida | — |
| 2,79–3,88 | P03 | IMG_2167 (0,00), esfera do topo com a bandeira | — |
| 3,88–5,08 | P04 | IMG_2169 (2,40), a câmera sobe | — |
| 5,08–6,29 | P05 | IMG_2178 (0,70), panorâmica revelando | — |
| 6,29–7,29 | P06 | IMG_2167 (2,20), esfera do topo | — |
| 7,29–8,50 | P07 | IMG_2178 (2,60), Atomium inteiro | — |
| 8,50–9,71 | P08 | IMG_2168 (3,00), avenida | — |
| 9,71–13,63 | P09 | IMG_2180 (2,60), Marina caminhando até o Atomium | — |
| 13,63–15,04 | P10 | IMG_2178 (4,40), Atomium inteiro (loop com o quadro 0) | — |

Título fixo do quadro 0 ao fim, em legenda Padrão (DS 3.2): "POV: / 15 segundos no Atomium". A quebra deixa a linha de cima menor (DS 3.1), e as linhas têm 4 e 22 caracteres.

## Verificações

- **Sem fala:** nenhum dos 5 arquivos tem voz (transcrição sem texto).
- **Som:** é o som ambiente de cada plano, nivelado por RMS antes do master, para o nível não saltar a cada corte (os originais vão de −27,6 a −38,5 LUFS). O master fica em −14,0 LUFS, com pico de −1,5 dBFS (DS 4.6). Por causa do ganho alto, vento e ruído de rua ficam bem presentes.
- **DS Nível B (5.2):** cortes secos, legenda Padrão com scrim, grão 5% e 1 objeto de marca (a placa de abertura no quadro 0, porque é o primeiro dia real em Bruxelas). Não há Placar nem ticket.
- **Contexto verdadeiro:** os planos estão na ordem real em que a chegada aconteceu, de 11:15 a 11:21 UTC, com duas exceções para dar ritmo: o IMG_2168 e o IMG_2169 se alternam com o IMG_2167, e os três foram gravados no mesmo minuto. Não entra a parada do bonde (IMG_2181), que é da saída.

## Pendências

1. **Escuta do Diego** (o Claude não escuta áudio). A alternativa é trocar por uma música da biblioteca do Instagram com o ambiente baixo, mas o pedido foi só som ambiente.
2. **Capa:** não foi feita. Sugestão: o quadro do P07 (Atomium inteiro contra o céu).

## Como renderizar

```
cd reels/atomium-pov
PD_BRUXELAS=PASTA_COM_OS_MOV python3 rev1/scripts/pov.py --fontes PASTA_TTF --qa
```
