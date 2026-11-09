# QA — REV2 "Tudo que você precisa saber sobre Bruges"

Pedido do Diego (09/11/2026): refazer com as 10 fotos que ele enviou, foto inteira com texto por cima numa caixa semitransparente, letra no estilo de carrossel viral (Barlow), DS só no CTA final. A REV1 continua em `../rev1/` e não foi alterada.

**Entrega:** 10 slides 1080 × 1440 em `slides/`. Render: `NODE_PATH=$(npm root -g) node montar_rev2.js` (textos em `conteudo_rev2.json`).

| # | Foto | Texto |
|---|---|---|
| 01 | Diego e Marina no canal | Tudo que você precisa saber sobre Bruges · antes de ir · arrasta → |
| 02 | Máquina da SNCB (16/03/2026, 09h44) | Bate-volta de Bruxelas · trem direto, cerca de 1 h, uns €17 por pessoa, cada trecho |
| 03 | Canal e torre da Igreja de Nossa Senhora | Parece cenário de filme · centro medieval Patrimônio da UNESCO, torre de 115 m |
| 04 | La Belgique Gourmande | Primeira impressão: a cidade cheira a chocolate |
| 05 | Waffle | Esse waffle foi no Chez Albert · o melhor que eu comi na Bélgica, disparado |
| 06 | Marina com a batata do Fritbar | A melhor batata frita da viagem, disparada · pulled pork, no Fritbar |
| 07 | Grimbergen | As melhores cervejas que eu bebi · cada uma tem o seu copo |
| 08 | Basílica do Sangue Sagrado | Relíquia que seria do sangue de Cristo · entrada grátis |
| 09 | Minnewater | Conselho final: durma uma noite em Bruges |
| 10 | Os dois waffles (escurecida) | CTA do DS: placa `MANDA PRA / QUEM VAI →` + símbolo 1º + @primeirodiaem |

## Decisões de design

- **Caixa:** grafite `#121317` a **72%** atrás de cada linha (estilo legenda de app). Com 50%, texto branco sobre céu claro fica em ~3,5:1 e falha na leitura. Com 72%, o pior caso (céu quase branco) fica em ~7,8:1, e a foto continua aparecendo por trás.
- **Letra:** título em Barlow Condensed 800 caixa-alta (92 px, 118 px na capa); texto em Barlow 700 44 px; palavra-chave em Amarelo Chegada sobre grafite (combinação permitida pelo DS). Uma família só, como recomendam os guias de carrossel.
- **Capa** com menos de 10 palavras e indicação explícita de "arrasta →". Slides 2 a 9 com o contador `N/10`.
- **DS V2** só no slide 10: placa de CTA, símbolo 1º (x 904 · y 1264) e cores da marca. Do 1 ao 9 vale o formato pedido pelo Diego (exceção desta peça, não regra do DS).

## Fatos e origem

| Fato | Origem |
|---|---|
| Trem Bruxelas–Bruges: ~€17 por trecho, 2ª classe | Estimativa de agregadores (everyrail, guias 2026: €17–23). Não achei a tabela oficial da SNCB. O Diego pediu só o valor, sem fonte no slide |
| Cerca de 1 hora | Fala do Diego (IMG_2419: "menos de uma hora") e horários dos agregadores |
| Centro histórico Patrimônio da UNESCO; torre de 115 m da Igreja de Nossa Senhora | Fatos públicos (UNESCO, 2000) |
| Cidade cheira a chocolate | Fala do Diego (IMG_2549) e pedido dele |
| Melhor waffle (Chez Albert), melhor batata (pulled pork, Fritbar), melhores cervejas | Opinião do Diego, nas palavras dele |
| Relíquia do sangue de Cristo, entrada grátis | Fala do Diego (IMG_2596: "realmente é gratuito"). O museu da basílica é pago |
| Quem faz bate-volta vai embora no fim da tarde | Guias de viagem e pedido do Diego |

## A conferir

1. **Preço do trem** é estimativa, não preço oficial. Vale olhar o app da SNCB antes de postar. A máquina da foto não mostra o valor.
2. **"Melhores chocolates do mundo"** saiu como "pra muita gente, o melhor do mundo", porque é opinião e não fato.
3. **Foto 05 × Chez Albert:** a foto foi escolhida pelo Diego para o slide do Chez Albert, e a marca não aparece nela.
