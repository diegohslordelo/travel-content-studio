# QA — Carrossel "Dicas sobre Bruges" (REV1)

Pedido do Diego (09/11/2026): carrossel "dicas sobre Bruges" com dormir na cidade, batata frita, Chez Albert, parque da ponte do amor e a cerveja "fermentada no bar…" (frase cortada).

**Entrega:** 7 slides 1080 × 1440 em `slides/` · fotos recortadas em `fotos/` · textos em `conteudo_rev1.json` · legenda e alt em `legenda_post_rev1.md`. Render: `./extrair_fotos_rev1.sh && python3 -I recortar_fotos_rev1.py && node montar_rev1.js` (brutos em `../fonte/`, fora do git).

## Estrutura (DS V2, 5.3)

| # | Slide | Tipo do DS | Conteúdo |
|---|---|---|---|
| 01 | Capa | Capa | Foto do Diego no canal (IMG_2549, 12h46) · Placa `DICAS / BRUGES` (base y 1240) · coordenadas Plex Mono |
| 02 | Dormir | Informação + bilhete | H2, 38 palavras, bilhete "dormir lá vale a pena" + lua desenhada |
| 03 | Fritbar | Fotografia | IMG_2624 (14h04) · bilhete "vale o hype." |
| 04 | Chez Albert | Fotografia | IMG_2700 (16h45) |
| 05 | Minnewater | Fotografia | IMG_2650 (14h50) · bilhete "muito bonito mesmo." |
| 06 | Brugse Zot | Fotografia | IMG_2696 (16h18) |
| 07 | Encerramento | Encerramento | Bilhete "voltaria mil vezes pra essa cidade." · CTA `SALVA PRA / VIAGEM →` · símbolo 1º (x 904 · y 1264) |

Rota amarela de 8 px em y 1360, contínua entre os slides; contador `NN / 07` em Plex Mono 30 px; etiqueta de série no canto superior esquerdo.

## De onde vem cada fato

| Fato | Origem |
|---|---|
| Batata: porco desfiado, barbecue, cebola crocante, repolho; "vale o hype"; dividiram uma e saíram satisfeitos | Fala do Diego e da Marina, transcrição automática de IMG_2633/2634 (não ouvida por ninguém). Letreiro "FRITBAR" visível no palito do prato (IMG_2624) |
| Fritbar fica na Katelijnestraat 3 | Web (tablejourney, wanderlog), 09/11/2026. O GPS do clipe (51.2037, 3.2246) é compatível |
| Chez Albert: janelinha de waffle na Breidelstraat, entre a Markt e a Burg | Web (st-christophers, tablejourney), 09/11/2026 |
| Minnewater = Lago do Amor; ponte de pedra = Ponte do Amor; grátis, aberto o ano todo | Web (visit-bruges.be, livetheworld, wanderlog), 09/11/2026 |
| "Ficou ouvindo a água", "muito bonito mesmo" | Fala do Diego em IMG_2646 (transcrição automática) |
| Brugse Zot: blond 6%, alta fermentação, refermentada na garrafa, feita em Bruges pela De Halve Maan | Web (brugsezot.be, halvemaan.be, varejistas), 09/11/2026. O copo "Brugse Zot" e o cartaz "Café 't Klein Venetië" aparecem em IMG_2696 |
| Depois das 17h os bate-voltas vão embora e a cidade fica mais calma | Guias de viagem (web, 09/11/2026). É relato de guia, não medição: o slide diz "segundo guias" |
| "voltaria mil vezes pra essa cidade" | Fala do Diego em IMG_2701 (transcrição automática) |

## Suposições e pontos a conferir (nada disso foi inventado; só não foi possível confirmar)

1. **Frase da cerveja cortada.** "A cerveja que é fermentada no bar…" não aparece em nenhuma fala do acervo e não consegui confirmar. O slide 06 só traz o que está verificado (alta fermentação, refermentada na garrafa, De Halve Maan). Se a ideia era outra, é só me dizer.
2. **Dormir.** O acervo é de bate-volta (11h04 às 16h53, voltaram para Bruxelas). O slide 02 diz isso e apresenta o "dormir lá" como dica, não como experiência. O bilhete está em caneta por pedido seu.
3. **Chez Albert: a foto não prova que é lá.** A transcrição de IMG_2694 cita "Chez Albert" e diz que comeram duas vezes, mas o áudio não foi ouvido. O clipe de IMG_2430 (11h27) tem GPS ~400 m da Breidelstraat, então não usei. IMG_2700 (16h45, GPS compatível com a Breidelstraat) é o waffle do final do dia. Vale ouvir IMG_2694 e IMG_2701 antes de postar.
4. **Preço fica fora.** A fala "15 euros a batata, 23 com bebidas" existe (IMG_2633), mas o acervo mantém falas de valor fora de peças até a revisão de custos. Com os valores confirmados, o slide 03 pode ganhar `€` e `R$` com cotação e data (DS 5.3, slide Custo).
5. **Série "DICAS".** O DS lista `QUANTO CUSTOU`, `VALE OU PULA` e `ROTEIRO` como séries. "DICAS" é rótulo novo no mesmo componente (Placa e Etiqueta de série). Sinalizo para o Diego decidir se entra no DS.
6. **Capa sem recorte do Diego.** O DS pede Diego recortado com parallax de 2 camadas. Usei a foto inteira (o rosto já fica em primeiro plano) e não fiz recorte automático.
7. **Fontes.** `design-system/fonts/` está vazia (pendência 1). Usei Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie (a caneta provisória do DS) em woff2 do npm `@fontsource`. `PD Placar` não foi necessária (não há número animado).
8. **H3 nas fotos.** O slide Fotografia do DS prevê foto, legenda de 40 px e sticker. Acrescentei o nome do lugar em H3 (56 px, "lugar em card") acima da legenda. É a única leitura minha do componente.

## Checklist (DS V2, 5.3 e seção 8 do CLAUDE.md)

| Item | Resultado |
|---|---|
| Formato 1080 × 1440, margem 80 | ok (medido: nada além de x 1000 nem de y 1330, exceto Rota e símbolo) |
| Alinhamento à esquerda em x 80 | ok (H2, corpo, H3 e legendas) |
| Informação ≤ 40 palavras | ok (slide 02: 38) |
| 1 CTA | ok (`SALVA PRA VIAGEM →`) |
| Mínimos de fonte (32 px essencial, 30 px microcopy) | ok (menor texto: 28 px da etiqueta de série, que é o tamanho definido no DS 2.7) |
| Proporção papel/grafite/amarelo | ok (papel predomina; vermelho, azul e verde somados < 5%) |
| Sombra de cima, fibra 4%, sem textura falsa | ok |
| Sem filtro nas fotos | ok (recorte e redimensionamento apenas) |
| Funciona sem som | n/a (estático) |
| Quem aparece | Diego em todas; Marina em 03 e 06 (cenas dos dois, regra padrão) |
| Dados reais, nada que contradiga o que aconteceu | ok, com os pontos acima |
