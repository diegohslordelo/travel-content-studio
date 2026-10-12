# QA · Reel "POV: você chegou no Atomium" · REV4

**Veredito do Claude: pronto para a sua escuta.** O Claude não escuta áudio.

**Entrega:** `reel_atomium_pov_rev4.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, **12,08 s** (290 quadros). Prévia leve: `reel_atomium_pov_rev4_previa_leve.mp4`. **Capa:** `capa_reel_atomium_pov_rev4.jpg` (nova, abaixo). **Legenda do post:** a da REV3, sem mudança (`../rev3/LEGENDA_POST.md`).

## Pedido do Diego (12/10/2026) e o que foi possível

**Pedido:** estender o take em que o Diego filma a Marina e depois o Atomium, com mais ≈ 2 s de Atomium nesse take, se houver; e incluir os 2 quadros finais que a REV3 deixava de folga.

**Não existe filmagem depois da Marina.** O IMG_2180 tem 7,125 s (171 quadros) e é a única cópia no Drive; a REV3 já ia até 7,03. Em vez disso:

| | REV3 | REV4 |
|---|---|---|
| Take 1 (IMG_2180) | 2,40–7,03 s (111 quadros) | **0,000–7,125 s, o take inteiro (171 quadros)** |
| Atomium na tela no take 1 | ≈ 3,1 s (entrava em ≈ 1,5 s do vídeo) | **≈ 4,1 s**: o recorte segue a Marina até 2,2 s e vira para o Atomium entre 2,4 e 3,4 s; a Marina volta ao quadro, embaixo dele, a partir de ≈ 5 s |
| Take 2 (IMG_2169) | 118 de 119 quadros | **119 de 119 quadros** |
| Duração | 9,54 s | **12,08 s** |

**Quadros finais:** os 171 quadros do IMG_2180 e os 119 do IMG_2169 foram conferidos por hash: todos são válidos e diferentes entre si. A REV3 deixava 2 e 1 quadros de folga contra erro de leitura, e agora entram. O áudio de cada arquivo é 1–2 ms mais curto que o vídeo e é completado com silêncio.

## Montagem

| Tempo | Take | O que se vê |
|---|---|---|
| 0,00–7,13 | IMG_2180, inteiro | A Marina caminhando; o recorte vira para o Atomium em 2,4–3,4 s e o acompanha até o último quadro |
| 7,13–12,08 | IMG_2169, inteiro | O Atomium na avenida, a câmera subindo. **Símbolo 1º** (Nascer) a partir de 9,83 s, até o fim. O corte volta ao início (loop) |

Texto "POV: / você chegou no Atomium" do quadro 0 ao fim (legenda Padrão, DS 3.2). O símbolo 1º é o mesmo da REV3, com a mesma exceção registrada (solto, sem fundo escuro, "1" na cor papel com sombra de texto).

## Verificações (no arquivo final)

| Item | Resultado |
|---|---|
| Quadros | 290 = 171 + 119; vídeo e áudio com 12,08 s |
| Som | Só ambiente, nivelado; −14,0 LUFS, pico −1,5 dBFS (DS 4.6) |
| Gancho | Texto desde o quadro 0. O Atomium entra em ≈ 3 s (na REV3, em ≈ 1,5 s): é o custo de usar o take inteiro, que começa com a Marina |
| Takes | 2 |

## Capa (pedido do Diego, 12/10/2026: "a fonte da capa deve ser essa", a capa do Barcelona em 20 s)

`capa_reel_atomium_pov_rev4.jpg`, **1080 × 1440 (3:4)**, com os mesmos valores da capa do "Barcelona em 20 segundos" (`reels/barcelona-20s/rev4/scripts/capa.py`, branch `claude/youthful-darwin-edqo3m`):

| Item | Valor |
|---|---|
| Texto | "POV: VOCÊ / CHEGOU NO / ATOMIUM" |
| Fonte | DS 1.2 Display: Barlow Condensed 800, 168 px, entrelinha 0,88, tracking −1%, papel `#FCFBF8` |
| Posição | Linhas alinhadas à esquerda dentro do bloco; bloco centralizado pela tinta em x 540, com centro da tinta em y 1000 (tinta em x 211–869 · y 777–1223) |
| Área segura | O texto fica dentro de x 135–945 · y 180–1260, a área que sobrevive à capa do Reel (9:16) e ao grid do perfil. Conferido em `qa_frames/capa_simulacao_instagram.jpg`, com a miniatura a 25% |
| Contraste | Sombra de texto da legenda (DS 3.1) + scrim grafite de 0 a 63% entre y 760 e 1440 |
| Fundo | IMG_2169 em 3,6 s: o Atomium contra o céu, recorte 3:4, sem filtro, grão 5% |

**Decisões a confirmar:**
1. **Sem a placa amarela:** a capa de referência não tem placa. A da REV3 (com a placa) continua em `../rev3/` se você preferir.
2. **5 palavras:** o painel pede no máximo 4 palavras na capa. Ficaram 5 para repetir o texto do vídeo.

## Pendências

1. **Escuta do Diego.**
2. **Gancho:** se a entrada do Atomium em ≈ 3 s parecer tarde, a alternativa é começar o take em ≈ 1,0 s (mais curto no início, com o mesmo fim).
