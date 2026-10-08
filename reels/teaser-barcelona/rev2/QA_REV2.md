# QA · Reel teaser de Barcelona · REV2

**Arquivo:** `reels/teaser-barcelona/rev2/reel_teaser_barcelona_rev2.mp4` (prévia: `reel_teaser_barcelona_rev2_previa_leve.mp4`) · **Capa:** `capa_reel_teaser_barcelona_rev2.jpg`
**O que é:** a REV1 com o **câmbio real da viagem** nos valores em R$ (pedido do Diego, 08/10/2026). Cortes, som, textos, legendas, placas e posições: iguais à REV1. A REV1 não foi alterada.

## Câmbio

| Item | Valor | Fonte |
|---|---|---|
| Cotação base | PTAX de venda de 09/03/2026: **R$ 6,0445** | Banco Central do Brasil, boletim de fechamento (API Olinda) |
| IOF | 3,5% sobre o valor convertido | Diego; confirmado na calculadora da Wise (`BRL_TAX` 3,5%) |
| Tarifa da Wise | 0,64% sobre o valor convertido (tarifa variável total 4,14% − 3,5% de IOF) | Calculadora da Wise, BRL → EUR, Pix, consultada em 08/10/2026. A Wise usa o câmbio comercial, sem spread embutido; a tarifa aparece separada. A tarifa de março/2026 pode ter sido um pouco diferente |
| **Câmbio final** | **€ 1 = 6,0445 × 1,0414 = R$ 6,2947** | |

A Wise soma IOF e tarifa sobre o mesmo valor convertido. Na consulta de R$ 1.000: R$ 960,21 convertidos, R$ 33,61 de IOF e R$ 6,15 de tarifa; € 171,01 recebidos. Por isso a conta é 1 + 0,035 + 0,0064, e não 1,035 × 1,0064.

## Valores na tela

| Etiqueta | REV1 (PTAX 08/10/2026) | REV2 (câmbio real) | Conta |
|---|---|---|---|
| Tour do Camp Nou | € 31 ≈ R$ 174 | **€ 31 ≈ R$ 195** | 195,14 |
| 5 tapas + paella + bebida | € 19 ≈ R$ 107 | **€ 19 ≈ R$ 120** | 119,60 |
| Sagrada Família · por pessoa | € 25 ≈ R$ 140 | **€ 25 ≈ R$ 157** | 157,37 |
| Montadito · quarta-feira | € 1 ≈ R$ 5,61 | **€ 1 ≈ R$ 6,29** | 6,29 |

## Conferências automáticas (`relatorio_tecnico_rev2.json`)

Iguais às da REV1 (seção 4 de `rev1/QA_REV1.md`): formato, duração, loudness, zona segura, legendas e objetos. Os números estão no relatório.

## Observação para o Diego

O carrossel de Roma usou a PTAX pura (sem IOF nem tarifa). A partir daqui, os dois conteúdos usam critérios diferentes para o R$. Vale decidir uma regra única, por exemplo "câmbio efetivo pago, com IOF e tarifa", e registrá-la na referência de conteúdo.
