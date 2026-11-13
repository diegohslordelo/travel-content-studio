# QA · Veneza bate-volta · REV3 (13/11/2026)

**Entrega:** `veneza_bate_volta_rev3.mp4` (1080 × 1920, 30 qps, H.264 + AAC). Capa e legendas iguais às da REV2 (`capa_rev3.jpg`, `legenda_post.md`).
**Parte da REV2** (que não foi alterada). Composição nova `VenezaReel3` (`design-system/remotion/src/reel/VenezaReel3.tsx`); a REV2 continua em `VenezaReel2`.

## Pedidos do Diego (13/11/2026) e o que mudou

| Pedido | Feito |
|---|---|
| Preto e branco em "Sim, Diego, eu vou fazer o quê? Vou pagar a taxa?" | Imagem do Diego em preto e branco (`grayscale(1) contrast(1.08)`) de 35,50 s a 37,53 s: a cena inteira, de um corte da gravação ao outro. A legenda karaokê continua colorida |
| Preto e branco em "E no bolso?" | Idem, de 46,83 s a 48,13 s |
| Final mais enxuto | Medido na energia da voz: do "Se hospedar" ao fim a fala é contínua; a única pausa era o silêncio de 0,27 s entre "legenda." e o "E" fraco de "E se você gostou" (< −62 dBFS). Corte de 57,233 s a 57,500 s, terminando no quadro 1725, que já era um corte da gravação: as duas mudanças viram uma só. E o vídeo termina 0,25 s depois de "aqui." (antes: 0,34 s de silêncio + 0,13 s de imagem sem som). 61,80 s → 61,30 s |
| Cores mais vivas e alegres nos grafismos, sem se apegar ao DS (CTA igual) | Paleta "Veneza ensolarada", só deste Reel: azul laguna (3 em cada 4), coral do pôr do sol (pedágio), amarelo sol (preços), vermelho vivo com carimbo branco (multa), mapa claro (terra verde-clara, mar azul, rota coral), azul céu (hospedagem), turquesa (reserva e link). Destaque da legenda e "TE QUER LÁ" em amarelo vivo `#FFD23F`; véus escuros sobre as fotos mais leves. **CTA idêntica à REV2:** placa do DS, *clack* e legenda com destaque âmbar `#E0AE5C`. Não é regra da marca: vale para este Reel até o Diego decidir se vira padrão do formato |
| Não cortar fala | O fim da voz nova foi transcrito de novo (Whisper large-v3): "E se você reservar com 4 dias de antecedência, você paga só 5 euros na entrada. Vou deixar o link na legenda. E se você gostou, já me segue aí, porque eu dou dicas de viagem toda semana por aqui." Completo |

Todo o resto (cenas, imagens, textos, efeitos, regras de troca no corte) é o da REV2: ver `../rev2/QA_REV2.md`.

## Medições do vídeo final

| Ponto | Resultado |
|---|---|
| Formato | 1080 × 1920, 30 qps, H.264 + AAC 48 kHz, 61,3 s (1.839 quadros) |
| Áudio | −14,2 LUFS integrados, pico −1,5 dBFS (DS 4.6) |
| Quadros pretos | nenhum (luminância mínima 40/255) |
| Trocas de cena | todas no quadro planejado; nenhuma a menos de 0,5 s de um corte da gravação. Fora delas, o detector marca só gestos da mão do Diego (24,67 s, 24,87 s, 27,27 s) e a animação de abertura de duas cenas no mesmo quadro do corte (8,23 s, 18,97 s) |
| Preto e branco | medido: diferença média entre canais R e B = 0 em 35,5–37,5 s e em 46,8–48,1 s; CTA em cor (41,6) |
| Folha de 1 quadro por segundo | conferida: cada imagem e texto batem com a fala; CTA igual à REV2 |
