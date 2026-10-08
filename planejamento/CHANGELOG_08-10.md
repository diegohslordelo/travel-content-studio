# Registro de alterações: teaser de Barcelona em 08/10 (p9, Stories de 08/10 e p11)

**Data:** 08/10/2026 · **Pedido:** Diego ("vamos mudar para o Reel de teaser do vídeo do YouTube de Barcelona") · **Arquivo:** `planejamento-postagens.html`

Só mudaram os posts `p9` e `p11` e os Stories de 08/10. O resto do arquivo (CSS, JavaScript e todos os outros posts, dias, semanas e vídeos) está idêntico, conferido por script.

| Onde | Antes | Depois |
|---|---|---|
| **p9** · 08/10, 12:30, Reel | "Primeira hora em Barcelona: quanto gastei" (gancho `Primeira hora em Barcelona: € [valor].`) | **"Teaser: 4 preços reais de Barcelona"**, gancho `4 preços que a gente pagou`. Arquivo pronto em `reels/teaser-barcelona/rev1/`. Legenda com os 4 valores em € e R$ e a cotação datada (PTAX de 08/10/2026: € 1 = R$ 5,61) |
| | Matriz "vale a pena?" do Reel de primeira hora | Removida (era do outro Reel) |
| **Stories de 08/10** | Palpite "Qual foi o primeiro gasto em Barcelona?" e regra "Sem anunciar até 09/10" | Palpite "Quanto você acha que custa o ingresso da Sagrada Família?" (a resposta, € 25, está no Reel). O anúncio do vídeo começa hoje, com o teaser |
| **p11** · 09/10, 12:00, Short | "Reaproveitar o Reel de 08/10…, fixar comentário com o link do vídeo longo" | Sobe o próprio teaser, com título pronto. O comentário fixado avisa "amanhã, 11h", e o link só entra em 10/10: vídeo agendado ainda não abre para o público |

**Checklists:** não alterados. O progresso salvo no navegador usa a posição de cada item.

## Por que "Primeira hora em Barcelona" não foi realocado

O vlog começa na manhã do dia 1: "a gente chegou bem tarde ontem, uma da manhã" (0:06). A primeira hora em Barcelona não foi gravada, então esse Reel não tem material (CLAUDE.md, seção 10: não criar cena que não foi gravada). A ideia fica para as cidades em que a chegada foi filmada.

## Risco registrado

A análise estratégica (achado 3) apontou que um Reel que só anuncia vídeo gera poucos envios. A decisão de voltar ao teaser é do Diego. Para reduzir o risco, o teaser entrega 4 preços úteis, ditos no próprio vlog, e não fica só no "sai sábado".

## Pontos a decidir (não alterados)

1. **p13 (vlog, 10/10):** o título planejado "Quanto custa passar 3 dias em Barcelona? Anotei tudo" promete um total, mas o vlog não mostra o total dos 3 dias, só preços soltos. O painel já diz "escolher a que for verdadeira".
2. **p15 (trailer, 10/10, 18:30):** o gancho `Barcelona em 3 dias: € [total].` precisa do total real, que não está no vídeo. Sem esse número, o gancho tem de mudar.

Para desfazer: `git revert` do commit.

## 08/10/2026 (2ª alteração) · câmbio real da viagem

Pedido do Diego: usar o câmbio que eles pagaram de verdade, ou seja, euro comprado na Wise em 09/03/2026, com IOF de 3,5%.

- **Base:** PTAX de venda do Banco Central de 09/03/2026, R$ 6,0445.
- **Custos:** a Wise cobra sobre o valor convertido o IOF (3,5%) e a tarifa de conversão dela (0,64%), num total de 4,14%. Os percentuais vêm da calculadora da Wise (BRL → EUR, Pix), consultada em 08/10/2026. A tarifa pode ter sido um pouco diferente em março.
- **Câmbio final:** € 1 = 6,0445 × 1,0414 = **R$ 6,2947**.
- **Valores:** € 31 ≈ R$ 195 · € 19 ≈ R$ 120 · € 25 ≈ R$ 157 · € 1 ≈ R$ 6,29 (antes: 174 · 107 · 140 · 5,61, com a PTAX de 08/10/2026).
- **p9:** o arquivo passa a ser `reels/teaser-barcelona/rev2/` e a legenda traz o câmbio novo.
- **p11:** o Short sobe a REV2 e a descrição traz o câmbio novo.

## 08/10/2026 (3ª alteração) · sem freeze

Pedido do Diego: a imagem parava na troca do plano do Camp Nou para o restaurante, e ele quer o corte direto.

- **REV3:** sai o freeze de 1 s dos planos 2 (€ 31) e 3 (€ 19); todos os cortes ficam secos. Duração: 27,5 s → 25,5 s.
- **Etiquetas de € 31 e € 19:** passam a entrar no começo da frase do preço ("a gente pagou…", "por…"), para continuar ~1,4 s na tela.
- **p9 e p11:** apontam para `reels/teaser-barcelona/rev3/`, com os tempos novos de cada cena.
