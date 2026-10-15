# Oportunidades de conteúdo de custo (não desenvolvidas)

**Data:** 14/10/2026 · **Entrega G da revisão v5** (`REVISAO_V5.md`)

**Atualização de 15/10/2026 (v6, decisão do Diego):** os custos voltaram ao calendário. As peças de custo agora têm data e ficam com o status **“Aguardando dados de custos do Diego”**: o painel lista, em cada uma, os dados necessários; os valores são fornecidos pelo Diego na produção de cada peça. Este documento continua **sem valores, cálculos ou estimativas**, e nenhum registro original foi alterado.

**Decisão anterior (14/10, substituída):** nesta revisão não há peças de custo.

## 1. Onde estão os registros (só referência)

| Fonte | Onde | O que tem | Observação |
|---|---|---|---|
| Planilha "Custos de Viagens - Europa" | Google Drive do Diego (raiz) | Registro de custos da viagem de março e das datas | Lida em 14/10 só para o roteiro de datas (carrossel p625). Nenhum valor foi copiado para o plano |
| Planilhas "Custos de Viagens - California", "Custo de Viagens - California" e "Custo de Viagens - Disney2027" | Google Drive (raiz) | Planejamento de outras viagens | Não lidas. Fora do acervo atual |
| Valores falados no master de Barcelona | `INVENTARIO_ACERVO.md` (09/10), seção 2, "Preços e fatos falados no master" | Valores ditos no vídeo, com minutagem | O próprio inventário marca o que é palpite e o que falta confirmar (por pessoa? em euro?) |
| Carrossel de Roma publicado em 06/10 | Painel, p7 (histórico) e `carrosseis/roma-3-dias/` | O custo de Roma já publicado | Histórico preservado, sem alteração |
| Quadros com preço nos vídeos | Ex.: balcão de waffle em Bruges (IMG_2685–2705), stroopwafel no Albert Cuyp (IMG_1610–1615), cardápio em Paris (IMG_3069) | Preços visíveis na imagem | Não foram usados nesta revisão. Na edição, evitar que esses quadros mostrem o preço legível |

## 2. Peças de custo que saíram do calendário v4

| ID | Peça (título do v4) | Ideia guardada | O que precisaria para voltar |
|---|---|---|---|
| p219 | 100 Montaditos às quartas | Comer barato em Barcelona num dia certo da semana | Confirmar o valor e a regra atual no site da rede |
| p250 | Metrô ilimitado em Barcelona por 3 dias | Vale ou não o passe para quem anda muito | Valor do registro + tarifa vigente |
| p252 | A maior parte do custo de Roma | Para onde foi o dinheiro em Roma | Registro de Roma conferido |
| p229 | Amsterdam em 3 dias: o total | Total real da cidade | Registro completo de Amsterdam |
| p233 | Florença em 2 dias: o total | Total real | Registro e material de Florença |
| p243 | Veneza em 2 dias: o total | Total real | Registro e material de Veneza |
| p258 | Milão em 2 dias: o total | Total real | Registro e material de Milão |
| p253 | Disneyland Paris em 1 dia: o total | Quanto custa o dia nos 2 parques | Registro do dia 18/03 |
| p263 | Quanto custou cada cidade (por dia, por pessoa) | Comparação entre as cidades | Todos os registros no mesmo critério (por pessoa ou por casal) |
| p268 | Itália em 9 dias: o total | Total da Itália | Registro da Itália |
| p278 | Madrid em 2 dias: o total | Total real | Registro de Madrid |
| p284 | Qual cidade foi a mais barata? | Ranking por custo | Os mesmos de p263 |
| p232 | A passagem é só o começo | O que pesa além da passagem | Registro completo da viagem |
| p237 | Comida em Roma: a regra que segurou o orçamento | Uma regra prática de comida | Registro de comida de Roma |
| p209 | Roma agora cobra para ver isso | A nova cobrança de entrada na Fontana di Trevi e no Panteão | Confirmar a regra e a data nas fontes oficiais |

## 3. Elementos do DS V2 ligados a custo (para quando a revisão de custos voltar)

- **Placar** (DS V2, 2.5): hora + gasto. Na v5, ele está fora da série (Nível B) e, nos Stories ao vivo, só aparece no estado pausado (sem valor, DS V2, 2.8).
- **Recibo** (DS V2, "Quanto custou?"): não usado na v5.
- **Etiqueta de série `QUANTO CUSTOU`**: não usada na v5. As peças que a usavam passaram para `ROTEIRO`.

## 4. O que fazer quando o Diego liberar o tema

1. Definir o critério único: por pessoa ou por casal, em € e em R$, com a cotação datada (formato de valores do DS V2).
2. Conferir cada valor no registro original. Sem registro, não há Placar (DS V2, 2.5).
3. Escolher as peças desta lista e encaixá-las respeitando a regra de cidades (rodar `scripts/aplicar_v5.py`).
4. Os vlogs (24/10, 07/11, 21/11, 05/12, 19/12, 02/01, 16/01) são editados pelo Diego. Se tiverem um trecho de gastos, a decisão de publicar é dele (pendência registrada em cada vlog no painel).

## 5. No calendário v6 (15/10/2026)

| ID | Data | Formato | Peça | Dados que o Diego fornece na produção |
|---|---|---|---|---|
| p851 | 11/11 | Carrossel | Roma: o que foi de graça e o que foi pago (sucede o p218 adiado) | Confirmação dos valores do registro de Roma (dez/2024, por pessoa) e das regras de 2026 |
| p229 | 17/11 | Reel | Amsterdam em 3 dias: quanto gastamos | Gastos de 12 a 15/03 por categoria, escopo e cotação |
| p250 | 06/12 | Reel | Metrô de Barcelona: passe ou avulso? | O que vocês compraram e quanto pagaram; tarifa atual conferida em fonte oficial |
| p253 | 07/01 | Reel | Quanto custa um dia nos 2 parques da Disney | Ingresso, trem, comida, compras, por pessoa ou casal |
| p278 | 26/01 | Reel | Madrid: quanto custou comer em 3 dias | Gastos de comida de 19 a 21/03 |
| p237 | 03/02 | Carrossel | Comida em Roma: a regra que segurou o orçamento | Confirmação de “comida e bebida” do registro de Roma |
| p829 | 13/02 | Reel | Amsterdam: o passe de transporte | O passe que compraram e o valor |
| p232 | 17/02 | Carrossel | A passagem é só o começo (categorias da viagem de março) | Totais por categoria, sem passagem aérea internacional |
| p263 | 24/02 | Carrossel | Quanto custou cada cidade por dia | Total por cidade e dias, mesmo critério |
| Reels “Primeiro dia” ligados a vlog e os 7 vlogs | ver AUDITORIA_LANCAMENTOS_V6.md | Placar e resumo final | Hora de chegada e cada gasto do dia com a hora; total por dia, do episódio e da viagem sem aéreo |

A planilha “Custos de Viagens - Europa” (Drive) tem totais por categoria e parcelas, mas mistura valores pagos e orçamento: serve de ponto de partida para o Diego, não como fonte final.
