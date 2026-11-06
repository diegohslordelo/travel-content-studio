# QA · REV3 · Vlog de Bruxelas (vídeo longo do YouTube) — em andamento

| Campo | Valor |
|---|---|
| Parte de | REV2 (`rev2/`, não alterada): mesma decupagem, narrações, mixagem e duração (15:50,3) |
| Data | 06/11/2026 |
| Estado | Em andamento: só a data entrou. Faltam as respostas aos pontos da REV2 (`../rev2/QA_REV2.md`, seção 3, e `../rev2/NARRACOES_REV2.md`), a escuta e o render final |

## 1. O que mudou

| Pedido do Diego (06/11/2026) | Feito |
|---|---|
| "Quando o primeiro dia aparece, tem que aparecer a data no canto superior esquerdo: 15 de Março de 2026" | A data entra em **0:37,2**, junto com a placa "1 DIA EM BRUXELAS" (que entra 200 ms antes), e fica até 0:40,9 |
| "Coloque a data nas cores do placar, um pouco menor que essa placa" | A 1ª versão (placa de capítulo amarela, "DOMINGO · 2026 / 15 DE MARÇO") virou **"15 DE MARÇO DE 2026" no painel do Placar**: grafite, letras amarelas, fonte do Placar (56 px), 96 px de altura, o mesmo acender (80 ms com 1 quadro de flicker), na posição do Placar no 16:9 (x 96 · y 72). Cabe inteira numa linha (≈ 540 × 96 px, contra ≈ 620 × 164 px da placa). Sem som. Prévia: `previas/rev3_data_540p.mp4` (0:30–0:50) |

## 2. Decisões e divergências

- **Componente:** a data é uma variação do Placar (DS 2.5), sem relógio e sem valor. O painel usa os mesmos valores do Placar (`estiloPainelPlacar`, exportado de `design-system/remotion/src/ds/Placar.tsx`); nenhum valor visual novo. Pela governança do DS (7.4), variação precisa do seu OK (você pediu).
- **Caixa-alta:** "15 DE MARÇO DE 2026", como os textos de destaque do DS. Se quiser "15 de Março de 2026" com minúsculas, é só trocar.
- **Posição:** é a mesma do Placar. Não há conflito, porque o 1º Placar de gasto só entra em 1:06.
