# QA · Reel "POV: você chegou no Atomium" · REV3

**Veredito do Claude: pronto para a sua escuta.** O Claude não escuta áudio.

**Entrega:**
- Vídeo: `reel_atomium_pov_rev3.mp4`, 1080 × 1920, 24 qps, H.264 SDR BT.709, AAC 48 kHz 256 kbps, **9,54 s** (229 quadros).
- Capa: `capa_reel_atomium_pov_rev3.jpg`; alternativa `capa_reel_atomium_pov_rev3_alt_marina.jpg`.
- Prévia leve: `reel_atomium_pov_rev3_previa_leve.mp4`. Legenda do post: `LEGENDA_POST.md`.

## Pedido do Diego (12/10/2026)

"POV: você chegou no Atomium" em 2 takes: a Marina chegando, do ponto de vista do Diego gravando, e depois um take só do Atomium. Sem a placa amarela no vídeo (só na capa). O texto vai na fonte do DS, mais embaixo, sem ocupar o meio da tela. No fim, o símbolo 1º aparece igual ao do DS, mas sem escurecer, com o Atomium ao fundo, e o vídeo volta ao início para puxar o gancho.

## Montagem

| Tempo | Take | Arquivo | O que se vê |
|---|---|---|---|
| 0,00–4,63 | 1 | IMG_2180 (2,40–7,03; 15/03/2026, 11:21 UTC) | A Marina caminhando, filmada pelo Diego. O recorte segue a Marina (centro medido 0,30 → 0,48 da largura) e vira para o Atomium, que entra no quadro em ≈ 1,5 s |
| 4,63–9,54 | 2 | IMG_2169 (0,00–4,92; 11:15 UTC) | O Atomium no fim da avenida; a câmera sobe até ele ocupar a vertical. **Símbolo 1º** com o Nascer a partir de 7,33 s, até o fim (2,2 s). O corte volta ao início (loop) |

**Texto:** "POV: / você chegou no Atomium" do quadro 0 ao fim, em legenda Padrão (DS 3.2: Barlow 700 56 px, centro x 540, base y 1420, scrim + sombra de texto). Fica na parte de baixo e não cobre o centro. A quebra é obrigatória (27 caracteres; o máximo é 26), com a linha de cima menor (DS 3.1).

## Símbolo 1º (DS 0.2.3, 4.3; bundle `PD.one`)

| Item | Valor |
|---|---|
| Desenho | O do bundle (viewBox 100): o "1", o sol e o traço do horizonte |
| Nascer | O traço se desenha (300 ms, ease-out), o sol sobe de trás do traço (700 ms, ease-cinema, recortado abaixo do horizonte) e o "1" entra em 500 ms (240 ms) |
| Cor | Sol e traço amarelos (`signal-500`). O "1" na cor papel (`#FCFBF8`, a variante do bundle usada no módulo), com a sombra de texto da legenda (DS 3.1). O "1" grafite padrão sumia sobre as esferas metálicas (testado) |
| Fundo | **Nenhum**: sem módulo grafite e sem escurecer a cena (pedido do Diego). O scrim de baixo é o mesmo de todo Reel |
| Tamanho e posição | Altura 176 px (o lado do módulo da placa, DS 2.1); centro em x 540 · y 960 (o centro do DS) |

**Fora do DS (registrado, decisão do Diego):** no DS, o 1º nasce dentro da placa de fechamento, no módulo grafite. Aqui ele aparece solto sobre a cena e sem a placa. Vale só para este Reel; não muda a regra geral.

## Verificações (no arquivo final)

| Item | Resultado |
|---|---|
| Fala | Nenhuma (VAD Silero sem voz no arquivo final) |
| Som | Ambiente dos 2 takes, nivelado; 40 ms de fade no corte; −14,1 LUFS, pico −1,5 dBFS (DS 4.6) |
| Gancho (referência 3.2) | O Atomium entra no quadro em ≈ 1,5 s; o texto está na tela desde o quadro 0 |
| Takes | 2 (pedido: no máximo 3, ideal 2) |
| Zona segura | Texto e símbolo dentro de x 72–944 · y 256–1440 |
| Verdade | Os 2 takes são reais e do mesmo lugar, com 6 minutos de diferença. O take do Atomium (11:15) foi gravado antes do take da Marina (11:21); a montagem não afirma ordem nem horário |

**Atomium "completo":** em nenhum take o Atomium cabe inteiro na largura do 9:16 (ele ocupa ≈ 0,5 da largura do quadro 4K, e o recorte vertical pega 0,32). O IMG_2169 é o que mais mostra: do pé ao topo, com a câmera subindo.

## Capa

`capa_reel_atomium_pov_rev3.jpg`: o IMG_2169 em 3,6 s, o Atomium contra o céu, com a placa `PRIMEIRO DIA EM / BRUXELAS` na variante Estática (DS 2.1) em x 72 · y 640 (778 × 219 px), scrim e grão do DS. Grid 3:4 e miniaturas em `qa_frames/capa_grid_e_miniaturas.jpg`.

**Alternativa** com a Marina (`_alt_marina`): perde porque tem uma van e várias pessoas no quadro.

## Pendências

1. **Escuta do Diego.**
2. **Duração:** 9,5 s, dentro de 7 a 30 s (referência 3.1). Para chegar perto de 15 s, só com um 3º take, que você limitou.
