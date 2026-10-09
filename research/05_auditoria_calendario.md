# 05 · Auditoria do calendário

**Data:** 08/10/2026 · **Arquivo auditado:** `planejamento/planejamento-postagens.html` (v2.2, cópia em `planejamento/versoes/painel-v2.2-2026-10-08.html`) · **Resultado aplicado:** v2.3 · **Registro das mudanças:** `13_log_alteracoes_calendario.md`

## 1. Escopo e marco de 08/10/2026

| Item | Situação |
|---|---|
| **Regra de corte** | Tudo planejado até **08/10/2026, inclusive**, é **histórico e executado**. Não foi reprogramado, apagado, substituído, nem tratado como pendência. Não gerei tarefa de produção para ele |
| **O que o pedido descreveu × o que existe** | O pedido fala em `planning-postagens.html` com **191** publicações. O arquivo real é `planejamento/planejamento-postagens.html`, na v2.2, com **193** posts (a v1 tinha 190; a v2 somou 4 posts, n1 a n4, e retirou 1, o p181; ver `planejamento/CHANGELOG_v2.md`). Não achei o número 191 em nenhum documento do repositório. Período: 01/10/2026 a 07/02/2027, **conferido**: 130 dias, nenhum dia faltando ou sobrando |
| **Histórico (10 posts: p0 a p9)** | Setup das contas (01/10), apresentação (01/10), 3 curiosidades (02/10), foto única e Short (03/10), POV de Barcelona (04/10), Short do POV (05/10), carrossel de Roma (06/10), carrossel de 10 fotos (07/10), primeira hora em Barcelona (08/10) |
| **Dados inconsistentes no histórico** | Na v2.2, só p0, p1 e p7 tinham `done: true`; p2 a p6, p8 e p9 apareciam como "atrasados". **Resolvido em 08/10/2026 por autorização do Diego** ("todos os posts até hoje eu fiz"): `done` desses 7 posts passou a `true`. Foi a única alteração em registro histórico (conteúdo intacto). O gancho de p9 ainda traz `€ [valor]` no registro, preservado |
| **Datas fora do período esperado** | Nenhuma encontrada. Nada para investigar |
| **Posts futuros** | **183** (80 Reels, 52 Shorts, 25 carrosséis, 16 Stories de lançamento, 8 vídeos longos, 1 foto, 1 setup) |
| **Status de produção** | Só o vlog de Barcelona consta como `pronto: true`. Os outros 7 vídeos estão `pronto: false`. **Planejado ≠ produzido**: nenhum post futuro foi tratado como feito |

## 2. Retrato do calendário futuro (antes das mudanças)

### 2.1 Carga por semana

| Tipo de semana | Reels | Shorts | Carrosséis | Stories de lançamento | Vlog | Total |
|---|---|---|---|---|---|---|
| **Lançamento** (semana de sábado de vlog) | 5 | 3 | 1 | 2 | 1 | 12 |
| **Desdobramento** | 4 | 3 | 2 | — | — | 9 |
| **Viagem** (20/01 a 07/02) | 5 | 3 | 0 a 2 | 0 a 1 | — | 8 a 12 |

Ciclos de 2 semanas, 8 cidades, 8 vlogs aos sábados 11:00. Na referência da conta, o mínimo é 3 Reels por semana e o ideal inicial é 5. **Buffer** (F23): 3 a 5 posts de feed por semana equilibram crescimento e esforço. O calendário tem 5 a 7 itens de feed por semana (Reels + carrosséis), na faixa alta.

### 2.2 Pilares (campo `pilar` do painel) e tipos

| Pilar (número do painel) | Posts futuros | Tipos principais |
|---|---|---|
| 1 | 52 | Vlog, trailer, primeira hora, primeiro dia, parte dos Shorts, Stories de teaser |
| 2 | 58 | Custo, erro, roteiro, carrosséis de fotos com preço |
| 3 | 48 | Trial (14), momento bruto, comida, curiosidade, expectativa × realidade |
| 4 | 18 | Stories de lançamento, anúncio, orçamento, mala, hotel de escolha |
| 5 | 6 | Retrospectiva, carrosséis da Itália |

Os rótulos dos pilares **não existem no repositório**; foram inferidos (ver `03`, seção 5).

### 2.3 Destinos e itens por cidade

Barcelona 21 itens futuros, Amsterdam 22, Paris 20, Disneyland Paris 20, Madrid 20, Bruxelas 19, Bruges 18, Lisboa 15, viagem de janeiro 22, Itália 4. Cada cidade tem **1 vlog + 1 trailer + 1 primeira hora + 1 primeiro dia + 1 custo + 1 erro + 2 a 3 carrosséis + 5 a 6 Shorts + Reels de apoio**.

### 2.4 Pontos factuais

- **56 posts** têm placeholder entre colchetes no gancho, título ou legenda (`[valor]`, `[total]`, `[Cena real]`, `[cidade]`): trailers 8, custo 8, roteiro em carrossel 8, primeiro dia 8, primeira hora 6, momento bruto 7, Itália 4, diário 5, filas 1 e orçamento 1.
- **41 Reels são de Nível A** (checklist de 25 a 29 itens) e **39 de Nível B** (25 itens).
- **48 de 80 Reels estão às 19:00.** O teste de horário (12:30, 18:30, 21:00) só vale até 01/11 e depois fixa o pico do Insights.
- **14 variações/Trial** semanais sobre o "Reel de melhor retenção da semana anterior". Dois blocos: A = Preço (7), B = Afirmação (7).
- **Shorts:** 44 de 52 são o **mesmo corte do Reel** do dia anterior (`short_reuse`) e 8 são "momento bruto" cortado do vlog.
- **Dependência de dados externos:** o gasto real de cada viagem vem do registro do Diego (CLAUDE.md, 9).

---

## 3. Achados

**Prioridade:** A = alta, M = média, B = baixa. **Confiança:** na **evidência** do problema, não na eficácia da correção.

| ID | Achado | Evidência | Impacto potencial | Prior. | Recomendação | Justificativa | Confiança | Status |
|---|---|---|---|---|---|---|---|---|
| **AUD-01** | **Falta uma linha de desejo e descoberta.** Só o POV de 04/10 (p5, histórico) é aspiracional entre os 84 Reels do painel (4 históricos e 80 futuros) | Contagem do painel; amostra pública (F42): mediana 842 views com cauda longa; experimentos mostram admiração explicando interesse em visitar (F27) | Perder a porta de entrada para quem ainda não precisa de custo | **A** | Adicionar 7 Reels "Primeiro olhar" (Nível B), sem tirar Reel de utilidade | Baixo esforço, material existe, teste com 7 amostras | Média | **Aplicado** (p190 a p196) |
| **AUD-02** | **Shorts repetem Reels de Nível B** (curiosidade, hotel, comida, expectativa × realidade, Trial): 7 casos | Painel (`short_reuse` de Reels de menor função); benchmark: mediana de Shorts de 2,5 a 6 mil nos canais brasileiros de 100 a 500 mil (F40) | Esforço pequeno, retorno baixo; ocupa o slot de teste | **M** | Trocar pelo corte "Primeiro olhar" do Reel de sexta, medindo Reels × Shorts | Mantém a cadência de Shorts e cria comparação | Média-baixa | **Aplicado** (7 substituições) |
| **AUD-03** | **Carga alta com o vlog como gargalo.** 7 dos 8 vlogs ainda `pronto: false`; vlog quinzenal + 41 Reels de Nível A com checklist de 25 a 29 itens | Painel; estimativa de 28 a 46 h/semana no cenário atual (`03`, seção 8; estimativa **minha**) | Atraso do vlog derruba a série inteira | **A** | Manter os marcos "Edição pronta até…" já existentes; adotar a **ordem de corte** (`03`, 8.2); perguntar as horas reais ao Diego (D3) | Evidência de Buffer: mais posts rende menos por post e cobra qualidade (F23) | Alta (fato do painel); Média (estimativa de horas) | **Não alterado.** Regra registrada em `03` e `08` |
| **AUD-04** | **56 posts dependem de dado real** (`[valor]`, `[total]`, `[Cena real]`, `[cidade]`) | Contagem no painel; CLAUDE.md, 9 ("não invente nem arredonde") | Post sem número sai fraco ou, pior, inventado | **A** | Regra: **post com placeholder não é publicado** até receber o dado; o Diego envia o registro por viagem | O próprio painel já trata os `[valores]` como pendência (ANALISE_ESTRATEGICA, D5) | Alta | **Não alterado.** Pendência D4 em `03` |
| **AUD-05** | **Blocos de 2 semanas por cidade** repetem destino (cada cidade tem 18 a 22 itens) | Painel; tema "intercalar" já aprovado (ANALISE D3) | Fadiga de tema; menos exposição de outras cidades | **M** | Manter a ordem, aplicar a intercalação **na Leitura 1 (semana 3)** como já aprovado. Hoje: Trial e momento bruto da cidade anterior e Primeiro olhar da cidade do ciclo cruzam duas cidades por semana | Sem dado, não há como saber se intercalar ajuda; evita refazer 17 semanas | Baixa | **Parcialmente tratado** (Trial e bruto já cruzam cidades) |
| **AUD-06** | **Trial Reels (14)** dependem de elegibilidade não confirmada e comparam gancho sobre Reels-base diferentes | F04 não lista requisitos; blogs citam 1.000 seguidores; painel traz plano B (Reel normal com novo gancho) | Teste sem poder estatístico; slot gasto | **M** | Manter, tratar como **teste** e registrar o par; aceitar leitura só com 10 pares (referência, 8.3) | Já é decisão aprovada; o plano B protege | Média | **Mantido** (classificado "Testar") |
| **AUD-07** | **Títulos de vlog sem promessa ou pouco "buscáveis"**, ex.: "Meu primeiro dia em Amsterdam" | Busca YouTube: "Barcelona roteiro 3 dias" tem dezenas de vídeos (F41); canais brasileiros usam cidade + custo + veredito (F40) | CTR e descoberta | **M** | Acrescentar uma opção "[Cidade] em N dias: quanto gastamos…" em cada vídeo (as 3 antigas ficam) | Ecoa o trailer e a forma de busca; decisão final do Diego | Média | **Aplicado** (8 vídeos) |
| **AUD-08** | **Vlog de Barcelona sai em 10/10 com capítulos e preços ainda não conferidos** | Transcrição automática com erros de grafia (doc 06) | Erro de preço publicado | **A** | Conferir capítulos e valores contra o vídeo final e o registro | CLAUDE.md, 9 | Alta | **Aplicado** (observação em p13) |
| **AUD-09** | **Carnaval cai no último fim de semana** do calendário (sáb 06/02 a ter 09/02/2027); o balanço de 07/02 é domingo de Carnaval | Datas confirmadas em 3 veículos (F37); calendário termina em 07/02 | Alcance menor do último Reel pode ser lido como falha de formato | **B** | Registrar na semana 18; comparar com os domingos anteriores | Hipótese; sem dado | Baixa | **Aplicado** (observação) |
| **AUD-10** | **Black Friday (27/11)** coincide com o 4º Reel aspiracional e um Short | Data fixa | Distorce uma leitura | **B** | Nota na semana 8 | Hipótese | Baixa | **Aplicado** (observação) |
| **AUD-11** | **Mudança do YPP em 01/02/2027** não está no planejamento | F10: 8.000 h ou 20 mi de views de Shorts para novos aplicantes, a partir de 01/02/2027 | Expectativa de monetização errada | **M** | Tratar monetização do YouTube como meta de 2027 e mais; parcerias e afiliados antes, com divulgação (CONAR) | Premissa aritmética em `03`, seção 11 | Média (divergência sobre mínimo de inscritos) | **Não aplicável ao calendário.** Entra em `03` e `08` |
| **AUD-12** | **Reaproveitamento do mesmo vlog em muitas peças**: Barcelona tem 21 itens futuros | Painel | Cortes quase idênticos da mesma cena | **M** | Mapa de cenas por peça em `06` (uma cena de abertura por peça) | Regra de originalidade e de uma ideia por Reel | Média | **Documentado em `06`** |
| **AUD-13** | **Stories** já têm função por dia | `planejamento/CHANGELOG_stories.md` | — | — | Nenhuma mudança além do pós-Reel nos 7 dias que ganharam Reel | Camada aprovada em 05/10 | Alta | **Aplicado** (7 dias) |
| **AUD-14** | **Pilares sem rótulo no repositório** | Campo `pilar` é 1 a 5, sem legenda | Ambiguidade para quem continuar o trabalho | **B** | Rotular (`03`, seção 5) e usar `6` só para o novo pilar | Sem mudar a estrutura | Alta | **Documentado** |
| **AUD-15** | **Posts "Foto" e carrosséis de fotos** (9 + 1) seguem o mesmo molde ("8 fotos, 8 preços") | Painel | Repetição de formato a cada 2 semanas | **B** | Manter: é um formato híbrido (desejo + preço); acompanhar salvamentos; trocar o molde se salvamento cair em 3 leituras | Há evidência de carrossel com engajamento alto (F25), com ressalva de método | Baixa | **Mantido** |
| **AUD-16** | **Vídeos longos a cada 14 dias** | Canais brasileiros observados: 2 a 7 longos por mês, até ~10 em série intensa (F40) | — | — | Manter | Na **borda inferior** da faixa observada (2 por mês; Trip Partiu ~2,4) | Média | **Mantido** |

## 4. Classificação dos 183 posts futuros

| Classificação | Quantidade | Quais | Critério |
|---|---|---|---|
| **Manter** | **153** | Reels de série (primeira hora, primeiro dia, trailer, custo, erro, hotel, comida, diário), 45 Shorts, 25 carrosséis, 16 Stories de lançamento, foto e setup | Têm função clara, material existe e nenhuma evidência pede mudança |
| **Ajustar** | **8** | p13 (nota de conferência) e os 7 vlogs seguintes (opção de título) | Melhoria sem mudar a ideia |
| **Substituir** | **7** | p26, p47, p68, p89, p110, p131, p152 (Shorts) | Troca do reaproveitamento de menor valor por "Primeiro olhar" |
| **Testar** | **15** | 14 Trial (p18 … p153) e o balanço de 07/02 (p189) | Mantidos como experimento; decisão só com amostra (ver `07`) |
| **Adiar** | **0** | — | Nenhum conteúdo tem razão para sair da data: não há evidência de que a data atrapalhe |
| **Remover** | **0** | — | Nada foi removido. A troca dos 7 Shorts mantém a cadência e o histórico no log |
| **Adicionar** (fora dos 183) | **7** | p190 a p196 | Linha aspiracional |

**Por que zero "Adiar" e "Remover":** o calendário já tinha passado por uma análise em 05/10 (`ANALISE_ESTRATEGICA.md`) que cortou hooks, trocou teasers e rotulou Nível A e B. A pesquisa nova encontrou **uma lacuna** (aspiracional), **um slot de baixo valor** (Shorts duplicados) e **riscos de execução** (dados, conferência, carga), nenhum dos quais pede remover conteúdo. Gatilhos que **fariam** adiar ou remover estão em `08`, seção 7.

## 5. Avaliação por critério pedido

| Critério | Estado | Observação |
|---|---|---|
| **Distribuição por plataforma** | Instagram 129, YouTube 62, Ambos 2 | Instagram concentra o desejo e a utilidade; YouTube, a profundidade |
| **Alternância de formatos** | Boa: Reel Nível A × Nível B, carrossel a cada 2 a 4 dias, vlog aos sábados | Falta o formato de desejo (corrigido) |
| **Repetição de temas** | Alta por cidade; baixa entre cidades | AUD-05 |
| **Relação Reels × vídeo longo** | Trailer no mesmo dia do vlog; Reels de apoio 3 a 7 dias depois; Shorts no dia seguinte | Funil claro; **conversão Short → vlog é fraca** em canais observados |
| **Reaproveitamento dos oito vídeos** | Cobertura alta | AUD-12, doc 06 |
| **Sazonalidade** | Não explícita | Notas de Carnaval e Black Friday adicionadas |
| **Coerência com o posicionamento** | Alta com "Chegada com recibo" (`03`) | Faltava o "desejo", agora presente |
| **Potencial de séries** | Alto | Seis séries nomeadas em `03` |
| **Esforço** | Alto | AUD-03; ordem de corte |
| **Conteúdos ausentes** | Aspiracional; sequência de Stories para "compartilhar aspiracional" | Primeiro: aplicado. Segundo: no `04`, S7 |
| **Oportunidades aspiracionais** | 7 Reels e 7 Shorts | `04`, seção 3 |
| **Hipóteses a testar** | 12 experimentos | `07` |
| **Viabilidade** | Condicional às horas do Diego | D3 em `03` |

## 6. O que **não** foi aplicado e por quê

| Ideia | Motivo |
|---|---|
| Reestruturar as 17 semanas em "intercalação" de cidades | A decisão já foi aprovada para depois da Leitura 1; sem dado, não há como saber se melhora |
| Tirar Shorts ou carrosséis para reduzir carga | Custo baixo e função clara; a válvula de corte está definida |
| Trocar horários de postagem | Sem dado da conta; estudos divergem (F24) |
| Mudar checklists dos posts existentes | O progresso salvo no navegador usa a posição de cada item |
| Alterar o DS | Congelado até abril/2027 (DS, 0.1) |
| Marcar p2 a p9 como publicados | Registro histórico; só o Diego decide (D6) |
| Preencher qualquer `[valor]` | Não há registro; CLAUDE.md, 9 |
| Criar posts para cenas sem material (ex.: cena de "amanhecer" nas cidades) | CLAUDE.md, 10: não criar cenas falsas |

## 7. Revisão cruzada deste documento

Conferi: os números de posts e semanas contra o painel original (script); a soma da classificação (153 + 8 + 7 + 15 = 183); a data de cada achado; as referências a `F..` contra `09`; e que nenhum item do histórico foi tocado (`13`, seção Verificação).
