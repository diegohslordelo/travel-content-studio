# QA · Carrossel Florença em 3 dias · REV1 (03/11/2026)

**Veredito:** pronto para revisão do Diego, **com custos pendentes** (`x` no lugar dos valores). **Base:** roteiro passado pelo Diego em 03/11/2026, vídeos do acervo (hora e GPS), molde do carrossel Roma REV1 (commit `77585d3`) e DS V2 (5.3, 2.6, 2.7, 7.3).

## Como gerar

De dentro desta pasta:
1. `python3 scripts/prep.py <pasta_com_os_MOV> <florenca_duomo.jpg>` → quadros dos vídeos em `../fonte/` (fora do git).
2. `node scripts/render.mjs` → `out/01.jpg` a `out/14.jpg` a partir de `slides.html`.

## Imagens (não há fotos de Florença no Drive: são quadros de vídeo, 2160 × 3840, HDR convertido para SDR)

| Slide | Origem | Data e hora | GPS |
|---|---|---|---|
| 01 capa | `florenca_duomo.jpg`, foto real (carrossel de documentos, branch `claude/laughing-noether-ce0kzt`) | sem EXIF; vista da Piazzale Michelangelo | — |
| 04 | `IMG_5554` 12,5 s | 28/12 12:32 | praça do Duomo |
| 05 | `IMG_5582` 4,5 s | 28/12 13:16 | Piazza della Signoria |
| 06 | `IMG_5649` 0,1 s | 28/12 16:54 | Ponte alle Grazie, olhando a Ponte Vecchio |
| 09 | `IMG_5774` 8,2 s | 29/12 15:59 | Boboli, túnel verde |
| 10 | `IMG_5812` 20 s | 29/12 17:08 | Lungarno, perto da Santa Trinita |
| 12 | `IMG_5832` 11,2 s | 30/12 10:42 | dentro do Duomo (0 m) |
| 13 | `IMG_5939` 23,2 s | 30/12 16:03 | Piazzale Michelangelo |

Sem imagem no acervo (por isso sem slide de foto): almoço no All'Antico Vinaio, Mercato Centrale (o primeiro vídeo de 29/12 é às 14:39), janelinha do vinho, San Lorenzo, jantares de 29 e 30/12.

## Divergências entre o roteiro e os vídeos (para o Diego decidir)

1. **Dia 3: "catedral de Santa Croce" × Duomo.** O vídeo de 30/12 às 10:41–10:42 é **dentro do Duomo** (GPS a 0 m da catedral; nave do Santa Maria del Fiore). O motivo dado ("não fomos no primeiro dia porque estava muito cheio") também bate com o Duomo, lotado em 28/12. O carrossel usa **Duomo por dentro**. Se foi mesmo Santa Croce, a entrada é paga e o slide 12 muda.
2. **Ponte Santa Trinita:** o pôr do sol fica a oeste, então a ponte no quadro (`IMG_5812`) é a Ponte alla Carraia. A Ponte Vecchio fica do lado oposto. Por isso a legenda diz "pôr do sol de um lado, Ponte Vecchio do outro".
3. **Multa do ônibus (€ 40 por pessoa + passagem, 31/12):** é fato confirmado (28/10), mas **não entrou no recibo**, que mostra só "Ônibus: x". Ela aparece como dica no slide 14. Se o Diego quiser no total, vira uma linha a mais no recibo.
4. **Boboli:** antes, o Diego disse que a única atração era o Duomo. O roteiro novo inclui o Boboli e o recibo traz a linha "Jardins de Boboli: x". Se tiver sido grátis, a linha sai.

## Custos pendentes (`x`)

- Hotel: **R$ 4.721 para 5 pessoas = R$ 944,20 por pessoa** (Civico 71, Via dell'Agnolo 71, Santa Croce; endereço por agregadores, não pelo site oficial). Falta o valor em euro ou a cotação do pagamento.
- Comida por dia (1, 2 e 3), All'Antico Vinaio, Mercato Centrale, janelinha do vinho, vinhos do mercado, ônibus, Boboli, total, ≈ R$ e cotação com data.
- Duomo: **€ 0,00** (catedral gratuita e sem reserva; cúpula, campanário e batistério pagos, segundo tickets.duomo.firenze.it, consultado em 03/11/2026).

## Conformidade com o DS V2

- [x] Só tokens e componentes do bundle (mesmo CSS do Roma REV1, sem valor novo).
- [x] Canvas 3:4, margem 80, contador Plex Mono 30, etiqueta de série, Rota amarela em y 1360 em todos os slides (5.3).
- [x] ≤ 40 palavras por slide.
- [ ] Valores com € e ≈ R$ e cotação datada: **pendente** (placeholders).
- [x] 1 CTA (`SALVA PRA VIAGEM →`), o mesmo verbo da legenda.
- [x] Símbolo 1º 96 px no encerramento, acima da Rota (como no Roma).
- [x] Grão 5%, fibra 4%.
- [x] Teste de miniatura: placa da capa legível a 25% (`out/contato.jpg`).

## Desvios (iguais aos do Roma REV1, já vistos pelo Diego)

1. **Capa sem o Diego em primeiro plano** (o DS 5.3 pede): não há foto dele em Florença com boa leitura. A capa é a foto do Duomo visto da Piazzale (com zoom de 155%). A foto original tem **manchas da lente no céu**, visíveis em tela grande.
2. Placa M (75%) nas fotos, scrim na capa e status `VALE`, como no Roma.
3. Fonte PD Placar ausente (números em Barlow Condensed).
4. Quadros de vídeo têm menos nitidez que foto; os 4K aguentam o recorte de 920 px.

## Fatos de contexto a conferir

- All'Antico Vinaio fica na Via dei Neri, perto da Signoria.
- Antiga casa de Galileu na Costa San Giorgio, no caminho para o Boboli.
- Palazzo Pitti fica dentro do Boboli (é a entrada do jardim); ingresso à parte.
- Galleria dell'Accademia (o David) perto do Mercato Centrale.
