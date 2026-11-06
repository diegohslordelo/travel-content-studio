# QA · REV3 · Vlog de Bruxelas (vídeo longo do YouTube) — em andamento

| Campo | Valor |
|---|---|
| Parte de | REV2 (`rev2/`, não alterada): mesma decupagem, narrações, mixagem e duração (15:50,3) |
| Data | 06/11/2026 |
| Estado | Em andamento: só a data entrou. Faltam as respostas aos pontos da REV2 (`../rev2/QA_REV2.md`, seção 3, e `../rev2/NARRACOES_REV2.md`), a escuta e o render final |

## 1. O que mudou

| Pedido do Diego (06/11/2026) | Feito |
|---|---|
| "Quando o primeiro dia aparece, tem que aparecer a data no canto superior esquerdo: 15 de Março de 2026" | Placa de capítulo do DS no canto superior esquerdo (x 96 · y 96, a posição da placa de capítulo no 16:9, DS 1.3), em **0:37,2**, junto com a placa "1 DIA EM BRUXELAS" (que entra 200 ms antes), até 0:40,9. Rótulo **"DOMINGO · 2026"**, destino **"15 DE MARÇO"**, seta. Sem *clack* próprio: o da placa da marca toca 200 ms antes (DS 4.6, no máximo 1 efeito a cada 1,5 s). Prévia: `previas/rev3_data_540p.mp4` (0:30–0:50) |

## 2. Decisão minha que precisa do seu OK

| Decisão | Por quê | Alternativa |
|---|---|---|
| A data em 2 linhas: "DOMINGO · 2026" em cima e "15 DE MARÇO" grande | "15 DE MARÇO DE 2026" inteiro na linha grande daria ≈ 1.010 px de placa, acima da largura máxima de 872 px do DS (2.1, que manda abreviar acima de 16 letras). Assim fica com ≈ 826 px e mostra dia, mês e ano | (a) "15 DE MARÇO DE" em cima e "2026" grande (lê na ordem, mas o ano fica mais forte que a data); (b) "15 DE MARÇO DE 2026" inteiro, passando da largura máxima (exceção ao DS, decisão sua) |

A placa é em CAIXA-ALTA, como todas as placas do DS (2.1); por isso "MARÇO" e não "Março".
