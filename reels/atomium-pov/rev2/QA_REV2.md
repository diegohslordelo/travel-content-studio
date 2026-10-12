# QA · Reel POV "15 segundos no Atomium" · REV2

**Veredito do Claude: pronto para a sua escuta.** O Claude não escuta áudio.

**Entrega:** `reel_atomium_pov_rev2.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, **15,00 s** (360 quadros). Prévia leve: `reel_atomium_pov_rev2_previa_leve.mp4`. Legenda do post: `LEGENDA_POST.md`.

## O que mudou da REV1 (pedido do Diego, 12/10/2026)

| REV1 | REV2 |
|---|---|
| 10 planos de 1,0 a 1,6 s: dava para ver pouco, sem imersão | **3 planos de ≈ 5 s** (pedido: no máximo 4; 3 × 5 s ou 4 × 4 s) |
| A panorâmica começava no céu vazio | O recorte acompanha o Atomium durante a panorâmica; ele fica no centro o tempo todo |
| A Marina cortada na borda | O recorte segue a Marina e vira para o Atomium quando ela chega perto |
| Placa até o 1º corte | Placa só até 2,4 s; depois a imagem respira |

Formato: **A02 "Rua com som"** do manual de formatos (`research/04`, 3.1 e 3.2): sem música, som ambiente como protagonista, 2 a 3 planos, quase sem corte, 8 a 15 s, texto mínimo.

## Montagem (ordem real da chegada, 15/03/2026, UTC)

| Tempo | Plano | Arquivo | O que se vê |
|---|---|---|---|
| 0,00–4,92 | P01 | IMG_2169 (o arquivo inteiro, 11:15) | A avenida, o Atomium inteiro no fim; a câmera sobe até ele encher o quadro. Placa `PRIMEIRO DIA EM / BRUXELAS` (Chegada, sai pela direita em 2,4 s) |
| 4,92–9,96 | P02 | IMG_2178 (0,80–5,84; 11:19) | O Atomium contra o céu. A posição da esfera do topo foi medida e o recorte acompanha a panorâmica (0,15 → 0,45 da largura) |
| 9,96–15,00 | P03 | IMG_2180 (2,00–7,04; 11:21) | A Marina caminhando até o Atomium. O recorte segue a cabeça dela (0,30–0,34) e vira para o monumento conforme ele entra (0,42–0,55); termina com o Atomium no alto e ela embaixo. O loop volta para a avenida |

Título do quadro 0 ao fim, em legenda Padrão (DS 3.2): "POV: / 15 segundos no Atomium". A quebra deixa a linha de cima menor (DS 3.1).

## Verificações (no arquivo final)

| Item | Resultado |
|---|---|
| Fala | Nenhuma: VAD Silero sem voz no arquivo final e nos 3 originais |
| Som | Ambiente de cada plano, nivelado: −16,5 / −16,6 / −16,4 dB RMS nos 3 planos (os originais iam de −29,8 a −38,5 LUFS). Cortes com 40 ms de fade. Master −14,1 LUFS, pico −1,5 dBFS (DS 4.6) |
| Duração | 15,00 s |
| DS Nível B (5.2) | 2 cortes secos (100%), legenda Padrão com scrim, grão 5% e 1 objeto de marca (placa de abertura, porque é o primeiro dia real em Bruxelas). Nada fora de x 72–944 · y 256–1440 |
| Verdade | 3 tomadas reais, na ordem em que foram gravadas. Não entra a parada do bonde (IMG_2181), que é da saída |

## Pendências

1. **Escuta do Diego.** O ganho alto deixa o vento e a rua bem presentes, e esse é o som real.
2. **Capa:** não foi feita. Sugestão: um quadro do P02 (o Atomium inteiro contra o céu).
