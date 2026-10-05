# QA · Carrossel Roma em 3 dias · REV1 (05/10/2026)

**Veredito:** pronto para revisão do Diego. **Base:** `planejamento/ESTUDO_CARROSSEL_ROMA.md` (estrutura e custos), DS V2.1 (5.3, 2.6, 2.7, 3.x, 7.3) e fotos do Drive do Diego.

## Como gerar

De dentro desta pasta:
1. `python3 scripts/prep.py <pasta_com_as_fotos>` → converte as fotos para `../fonte/` (fora do git).
2. `node scripts/render.mjs` → gera `out/01.jpg` a `out/16.jpg` a partir de `slides.html` (variáveis opcionais: `PLAYWRIGHT_MODULE`, `CHROMIUM`).

`slides.html` usa o `pd-bundle.css` do DS e as fontes em `fonts/` (Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie, OFL 1.1, subconjunto latin). O Chromium do ambiente não alcança o Google Fonts, por isso as fontes foram baixadas.

## Fotos (EXIF confirma Roma de 24 a 27/12/2024)

| Slide | Foto | Data e hora |
|---|---|---|
| 01 | Diego e o pai na arena do Coliseu (enviada no chat) | sem EXIF; dia 2, 26/12 |
| 04 | IMG_5064 (Trevi) | 25/12 10:08 |
| 05 | IMG_5108 (Panteão, fachada) | 25/12 10:50 |
| 07 | IMG_5220 (Pincio) | 25/12 16:37 |
| 08 | Vila de Natal, vista ampla (enviada no chat) | sem EXIF; dia 1, 25/12 |
| 10 | IMG_5319 (Fórum) | 26/12 13:45 |
| 11 | IMG_6652 (Coliseu à noite) | 24/12 22:01 |
| 14 | IMG_6653 (São Pedro) | 27/12 08:25 |
| 15 | IMG_6650 (Sant'Ignazio, Diego e Marina) | 27/12 12:31 |

**Escolhas entre fotos:**
- **Capa:** a da arena com o pai venceu a do Coliseu por fora (IMG_6651). Tem o Diego em primeiro plano (DS 5.3), mostra a arena, que é o que o ingresso de € 24,00 compra, e a camisa do Bahia reforça o "soteropolitano" da apresentação. O pai aparece com autorização do Diego.
- **Villa Borghese:** a vista ampla venceu a árvore-carrossel. A árvore é mais colorida, mas a vista ampla prova a legenda: aparecem a Torre Eiffel de luzes e outras áreas temáticas. Recorte com zoom de 125% para tirar o céu preto.

Não usadas (ficam para Stories): IMG_6651 (Coliseu por fora), árvore-carrossel da vila de Natal, IMG_5132 (Navona), IMG_5397 (selfie em São Pedro com o grupo: tem rosto de terceiros, pedir autorização antes de usar), IMG_5409 (interior de São Pedro), IMG_5523 (Gianicolo).

Não vieram: interior do Panteão e foto no espelho.

## Conformidade com o DS V2.1

- [x] Só tokens oficiais (cores, fontes, tamanhos, espaços, raios, sombras).
- [x] Canvas 3:4, margem 80, contador Plex Mono 30 no canto superior direito, etiqueta de série no superior esquerdo, Rota amarela de 8 px em y 1360 em todos os slides (5.3).
- [x] ≤ 40 palavras por slide (contando palavras, sem números e símbolos).
- [x] Valores com € e ≈ R$, cotação datada no recibo, no slide 11 e na legenda (7.1 e 7.3).
- [x] 1 CTA (`SALVA PRA VIAGEM →`), mesmo verbo da legenda.
- [x] Objetos sobre a foto sobrepõem até 24 px e não cobrem rosto (3.x, Sobreposição).
- [x] Símbolo 1º 96 px em x 904 · y 1264 no encerramento.
- [x] Grão 5% em tudo; fibra 4% no papel.
- [x] Teste de miniatura: placa e valor da capa legíveis a 25% (ver `out/contato.jpg`).

## Desvios e decisões tomadas (precisam de aprovação do Diego)

1. **Capa sem recorte em camadas (parallax):** a foto já traz o Diego em primeiro plano; o recorte de 2 camadas do DS fica para quando houver o kit.
2. **Placa nas fotos em M (75%) e sem rótulo.** A P (50%) é a de Stories e deixaria o rótulo com 18 px, abaixo do mínimo de 30 px do carrossel.
3. **Recibo do slide 02 a 125%** (750 px em vez de 600) para a microcópia chegar a 30 px. O recibo de 600 px do DS foi pensado para vídeo.
4. **Scrim na capa** (componente de Reel) para a microcópia ficar legível sobre a foto.
5. **Status VALE:** o DS cita o componente mas não dá medidas; usei papel recibo, verde, Barlow Condensed 700 40 px, raio de etiqueta e sombra de papel.
6. **Fonte PD Placar** não existe no repositório: os números usam Barlow Condensed (fallback do bundle).
7. **Preset de cor** (PD Chegada) ainda não calibrado: fotos sem preset, só com grão.
8. **Slide 12:** preços de 2026 (site oficial, 05/10/2026) com cotação de 02/10/2026; o resto do carrossel usa preços e cotação de dez/2024.

## Dados a conferir antes de postar

- Os "$" das anotações são euro; todos os valores são por pessoa.
- O € 1,00 do espelho de Sant'Ignazio foi pago (está no total).
- Fatos de contexto: tradição da moeda na Trevi; Rafael, Vittorio Emanuele II, Umberto I e Margherita no Panteão; Vaticano como menor país; regras de venda do ingresso (7 e 30 dias antes) e preços de 2026.
- Datas por dia vêm do EXIF das fotos (dia 1 = 25/12, dia 2 = 26/12, dia 3 = 27/12); saída em 28/12 deduzida das 4 noites.

## Confirmações do Diego (05/10/2026)

- Os "$" das anotações são euro; todos os valores são por pessoa; o € 1,00 do espelho de Sant'Ignazio foi pago.
- O pai do Diego autoriza o uso da foto da capa.
- **Música:** sim, da biblioteca do Instagram, adicionada no app na hora de postar. Motivo: carrossel com música pode aparecer na aba Reels (Mosseri, 17/10/2024). Critério: instrumental, sem letra competindo com a leitura, no tom da marca. O DS não cobre música em carrossel; registrar em Aprendizados ("carrossel com música") para comparar com os próximos.
