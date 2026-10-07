# QA · Carrossel Barcelona 2027? · REV3 (07/10/2026)

**Parte da REV2.** Pedido do Diego: capa "Barcelona 2027?" no lugar de "10 fotos"; nome das atrações discreto nas fotos, sem a data; paella identificada como Restaurante Momo; slide 11 mantido.

## O que mudou

| Slide | REV2 | REV3 |
|---|---|---|
| 01 | Placa "BARCELONA EM / 10 FOTOS" + datas e coordenadas | Placa "BARCELONA / 2027?" (2 linhas no destino) + só as coordenadas |
| 02–10 | Foto pura | Foto + nome da atração em Plex Mono 30 (microcópia mínima do carrossel, DS 3.x), x 80 · base 80, branco papel com a sombra `on-photo`; degradê grafite 0 → 63% de 320 px na base para a leitura |
| 06 | — | "Paella · Restaurante Momo" (informado pelo Diego) |
| 11 | CTA | Igual |

Todos os slides são renderizados por `slides.html` (`node scripts/render.mjs`); `scripts/fotos.py` da REV2 não é mais necessário.

## Desvios (precisam de aprovação do Diego)

1. **Placa da capa com destino em 2 linhas e sem rótulo:** "BARCELONA 2027?" em 1 linha não cabe na Placa G (passaria de 920 px). O DS não prevê destino em 2 linhas.
2. **Degradê de 320 px** em vez do scrim de Reel (770 px): mesma cor e opacidade do token, só mais baixo, para não escurecer a foto.
3. **Fotos 02–10 sem contador e sem Rota** (vem da REV2, só neste carrossel).

## Conferir antes de postar

- Nome do restaurante: "Momo" (informado pelo Diego).
- Ainda em aberto: o museu ou tour do Camp Nou e o Hotel W (QA_REV1).
