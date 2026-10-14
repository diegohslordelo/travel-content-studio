# Revisão estratégica v5 · Primeiro Dia

**Data:** 14/10/2026 · **Período planejado:** 15/10/2026 a 07/02/2027 (17 semanas) · **Aplicado em:** `planejamento-postagens.html` (painel v5) · **Gerado por:** `scripts/aplicar_v5.py` + `scripts/v5_pecas.py` · **Base:** painel v4 de 14/10 (cópia em `versoes/painel-v4-2026-10-14-antes-da-v5.html`)

Documentos desta revisão:

| Entrega | Arquivo |
|---|---|
| A. Diagnóstico e estratégia | este arquivo |
| B. Inventário do acervo e D. Mapa de uso | `INVENTARIO_ACERVO_V5.md` |
| C. Calendário revisado | `planejamento-postagens.html` (painel) e a tabela da seção 6 |
| E. Auditoria de cidades | `AUDITORIA_CIDADES_V5.md` (gerada pelo script) |
| F. Banco de ideias | `BANCO_DE_IDEIAS_V5.md` |
| G. Oportunidades de custo (sem desenvolver) | `OPORTUNIDADES_CUSTOS.md` |
| H. Relatório de implementação | `CHANGELOG_v5.md` |

Esta revisão não altera o Design System, os tokens, a referência de conteúdo, o CLAUDE.md nem o material bruto. Ela mexe no planejamento, que o Diego pediu.

---

## 1. Diagnóstico (o que estava errado no v4)

| # | Problema | Evidência | Correção na v5 |
|---|---|---|---|
| 1 | **A mesma cidade aparecia em dias seguidos e mais de 2 vezes por semana.** O v4 contava só posts do feed seguidos, não dias, e não contava Shorts, vlogs nem Stories. | Barcelona em 3 dias na semana de 12 a 18/10 (Reel 13/10, Short 14/10, série 18/10). | Regra nova aplicada a todos os formatos, conferida por script. **0 violações** de 12/10/2026 a 07/02/2027 (`AUDITORIA_CIDADES_V5.md`). |
| 2 | **Custos no centro do plano**, sem registro completo e com valores a confirmar (`€ [total]`, "por pessoa?"). | 15 peças de custo e valores em 38 peças (legenda, tela, cena, Placar). | Nenhuma peça de custo nesta revisão (pedido do Diego). As 15 saíram e estão em `OPORTUNIDADES_CUSTOS.md`. Valores removidos das outras peças. |
| 3 | **Florença, Veneza e Milão sem arquivo.** O v4 tinha 3 Reels "Primeiro dia em" e 2 peças dessas cidades. | As pastas do Drive foram criadas em 14/10 e estão vazias. | As 5 peças saem e vão para o banco (`BANCO_DE_IDEIAS_V5.md`). Sem arquivo, não há peça (CLAUDE.md, 10). |
| 4 | **Paris, Disney, Madrid e Lisboa com material "simulado".** No dia 11/10 essas pastas estavam vazias. | Em 14/10 o Diego subiu 988 vídeos dessas 4 cidades. | 37 clipes delas foram analisados (quadros, metadados, áudio). As peças usam os arquivos reais e marcam o que falta decupar. |
| 5 | **Placar sem registro.** A série Nível A dependia do Placar (hora e gasto), e o gasto está fora desta revisão. | DS V2, 2.5: "sem registro, não há placar". | A série passa a Nível B, com a hora real dos arquivos em Legenda Informação. Nos Stories ao vivo, só o Placar mini pausado (sem valor, DS V2, 2.8). |
| 6 | **Shorts soltos do Reel de origem e criando dias novos de cidade.** | Short no dia seguinte ao Reel. | 25 Shorts, cada um no **mesmo dia** do Reel de origem (20:30), com título próprio de até 60 caracteres. |
| 7 | **Stories sem descanso.** | Todos os dias tinham Stories. | 7 sextas sem Stories, de propósito, alternadas com o quiz de sexta. |
| 8 | **Peça duplicada.** O castelo da Disney aparecia em 3 peças. | p225, p608 e p624. | p225 sai e volta ao banco se a decupagem achar uma reação forte. |
| 9 | **Histórico sem evidência.** 11/10 e 13/10 sem marcação. | `PROPOSTA_V4`, seções 5 e 6. | p201 e p202 marcados como publicados, com a evidência citada na observação. 10, 12 e 14/10 ficam como pendência (não há prova). |

## 2. Estratégia

**Posicionamento** (DS V2, Plataforma): tirar o medo da chegada. O que só o Primeiro Dia tem é o **primeiro dia real de cada cidade**, com hora, perrengue e veredito. Todo o resto do calendário existe para levar gente a essa série ou para ser útil a quem vai viajar.

**O que muda na v5:**

1. **A série "Primeiro dia em X" é o eixo.** São 18 peças de série no período: 10 primeiros dias do acervo, 3 ao vivo na viagem de janeiro e 5 peças-ponte (trailer, ranking, mapa, anúncio e balanço). Os vlogs saem no sábado junto com o Reel de primeiro dia da mesma cidade. O Reel se sustenta sozinho e o link do vlog vai nos Stories.
2. **Cidade nunca em dias seguidos.** O público vê um perfil de várias cidades, não um "perfil de Barcelona". A regra também protege contra a fadiga de quem já segue.
3. **Utilidade sem preço.** Nesta revisão, a utilidade vem de hora, lugar, erro e veredito: "2 erros que a gente não repete", "o ingresso que esgota antes", "a Torre inteira é daqui", "vale ou pula". As peças que falavam de "grátis" mudaram de ângulo (vista, hora, efeito), sem inventar nenhum fato.
4. **Material real em primeiro lugar.** 24 peças novas nasceram de arquivos do Drive e do repositório: as 3 estátuas de xixi de Bruxelas, o céu rosa no canal de Amsterdam, o show em Madrid, o castelo que muda de cor (14h35 e 19h11), a Notre-Dame reaberta, Roma antes das 9.
5. **Itália só com o que existe:** 12 fotos de Roma no Drive e as fotos do repositório. As peças de Roma usam a hora do EXIF. Florença, Veneza e Milão ficam no banco até o material chegar.

**Pilares** (referência de conteúdo e v3): Vontade de ir (22 peças), Chegar sabendo (27), Como foi de verdade (16), Primeiro Dia (série) (18). Total: 67 Reels e 16 carrosséis no feed.

**Testes** (referência, 8.3, uma variável por vez): T1 a T5 continuam do v3/v4, com as contagens A × B no painel. O T1 passou a usar "hora, lugar ou como chegar" como camada de informação (sem preço).

## 3. Papel de cada formato

| Formato | Frequência | Função | Regra de cidade |
|---|---|---|---|
| **Reel** | 4 por semana (ter, qui ou sex, sáb ou dom) | Alcance e conversão. A série sai no domingo (ou no sábado, nas semanas de vlog) | Conta no dia em que sai |
| **Carrossel** | 1 por semana (quarta) | Salvamento: roteiro, lista, consulta | Conta no dia |
| **YouTube Short** | 25 no período, no mesmo dia do Reel de origem, às 20:30 | Descoberta no YouTube. O Short segue o Reel, não o contrário | Não cria dia novo: sai no mesmo dia do Reel |
| **Vídeo longo (vlog)** | 7, aos sábados | Profundidade e retenção no YouTube | Conta no sábado, junto com o Reel da mesma cidade |
| **Stories** | 109 de 116 dias | Relacionamento e conversão: pós-post (69), pergunta da semana (14), quiz de sexta (7) e diário ao vivo da viagem (19) | Pós-post: a cidade do post do dia. Pergunta da semana: sem cidade central. Quiz: 3 cidades como opções (menção incidental, registrada) |
| **Sem Stories** | 7 dias | Descanso planejado, em sextas de produção alternadas sem post (16/10, 30/10, 13/11, 27/11, 11/12, 25/12 e 08/01). Nas outras sextas sem post, há o quiz | — |

## 4. Decisões que dependem do Diego

| # | Decisão | O que está no plano até lá |
|---|---|---|
| **D1** | O CLAUDE.md, 10, diz que a Itália "serve para carrosséis, não para Reels". Desde a v3, o plano tem Reels feitos de fotos de Roma (p205, p222, p242 e p254; a v5 acrescenta o p615). | Os Reels ficam, com a pendência registrada no painel (k 41). Se a resposta for "não", cada um vira carrossel na mesma data, sem mudar a auditoria de cidades. |
| **D2** | Nada de custo nesta revisão. | Aplicado. As ideias de custo estão em `OPORTUNIDADES_CUSTOS.md`. |
| **D3** | Na viagem de janeiro, os Stories ao vivo mostram todos os dias a cidade onde você está. Isso é exceção à regra de cidades? | Tratado como cobertura ao vivo (registrado nos Stories e no painel, pendência k 53). Os posts do feed da viagem cumprem a regra. |
| **D4** | Cidades e ordem da viagem de janeiro. | As peças usam "cidade 1, 2 e 3", e a auditoria é refeita quando as cidades chegarem. |
| **D5** | A série sem Placar (Nível B) enquanto não houver registro de gasto. | Aplicado. Volta a Nível A quando houver registro e a revisão de custos for liberada. |

## 5. Limitações (o que não foi feito)

- **Drive:** a listagem das pastas de cidade está completa (veja `INVENTARIO_ACERVO_V5.md`), mas o conector só baixa arquivos de até 10 MB, e um download de ≈ 9 MB caiu. Foram analisados **55 clipes** (quadros, metadados e transcrição). Os clipes que cabem no limite são, em geral, curtos (de 0,2 a 3 s), exceto as cópias MP4 de Amsterdam (de 5 a 12 s). **Não vi nenhum vídeo longo inteiro.**
- **Áudio:** a transcrição é automática (faster-whisper "small"). Nos primeiros 37 clipes, ela falhou por um erro de biblioteca e foi refeita no fim. Não ouvi nada: falas citadas devem ser conferidas antes do corte.
- **Hora dos arquivos:** a hora vem da data de criação gravada no arquivo. Nas cópias MP4 de Amsterdam, a hora não bate com a cena (Story noturno marcado às 07h26) e **não deve ser usada** como hora real.
- **Barcelona:** listei a pasta só em parte nesta sessão (o conector devolve de 5 em 5 por pasta). A decupagem de Barcelona continua sendo a do master e do inventário de 11/10.

## 6. Calendário do feed (resumo)

O calendário completo, com todos os campos de cada peça, está no painel. A tabela por semana, com cidades e formatos, está em `AUDITORIA_CIDADES_V5.md`. A série:

| Data | Peça da série |
|---|---|
| 24/10 (sáb) | p207 · Primeiro dia em Amsterdam (com o vlog) |
| 25/10 (dom) | p300 · Primeiro dia em Barcelona (estreia da série dos domingos) |
| 01/11 | p217 · 9 primeiros dias. Qual é o seu? (trailer) |
| 07/11 (sáb) | p234 · Primeiro dia em Paris (com o vlog) |
| 21/11 (sáb) | p215 · Primeiro dia na Disneyland Paris (com o vlog) |
| 05/12 (sáb) | p221 · Primeiro dia em Madrid (com o vlog) |
| 19/12 (sáb) | p304 · Primeiro dia em Bruxelas (com o vlog) |
| 24/12 | p254 · Nosso primeiro dia em Roma foi no Natal |
| 27/12 | p247 · 9 primeiros dias: qual foi o melhor? |
| 02/01 (sáb) | p305 · Primeiro dia em Bruges (com o vlog) |
| 09/01 | p265 · Vale a pena ir a Barcelona? A resposta no aeroporto |
| 10/01 | p266 · Próximo primeiro dia: [cidade 1] (anúncio da viagem) |
| 16/01 (sáb) | p270 · Primeira noite em Lisboa (com o vlog) |
| 20/01 | p625 · 9 primeiros dias no mapa (carrossel) |
| 23/01 | p275 · Primeiro dia em [cidade 1], ao vivo |
| 30/01 | p280 · Primeiro dia em [cidade 2], ao vivo |
| 06/02 | p285 · Primeiro dia em [cidade 3], ao vivo |
| 07/02 | p286 · 3 países, [N] primeiros dias: o balanço |
