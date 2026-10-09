# Registro de alterações e relatório de implementação · painel v2.2 → v3

**Data:** 09/10/2026 · **Pedido:** Diego (reconstrução completa da estratégia do Instagram a partir de 09/10/2026) · **Antes:** `versoes/painel-v2.2-2026-10-09-antes-da-v3.html` · **Depois:** `planejamento-postagens.html` · **Estratégia:** `ESTRATEGIA_EDITORIAL_V3.md` · **Diagnóstico:** `DIAGNOSTICO_V3.md` · **Acervo:** `INVENTARIO_ACERVO.md`

## 1. Arquivos

| Arquivo | O que é |
|---|---|
| `planejamento-postagens.html` | **Modificado.** Bloco `DATA` reconstruído a partir de 09/10 e interface atualizada (ver seção 4) |
| `DIAGNOSTICO_V3.md` | **Novo.** Entregável 1 |
| `ESTRATEGIA_EDITORIAL_V3.md` | **Novo.** Entregável 2 |
| `INVENTARIO_ACERVO.md` | **Novo.** Entregável 3 |
| `CHANGELOG_v3.md` | **Novo.** Este relatório (entregável 6) |
| `versoes/painel-v2.2-2026-10-09-antes-da-v3.html` | **Novo.** Cópia do painel antes da v3 |
| `scripts/v3_pecas_1.py` a `v3_pecas_4.py` | **Novos.** Conteúdo das 87 peças, legível e versionável |
| `scripts/reconstruir_v3.py` | **Novo.** Gera o `DATA` (histórico + peças + Shorts + semanas + Stories + testes) a partir da cópia v2.2 |
| `scripts/painel_v3_js.py` | **Novo.** Aplica as mudanças de interface |

Não alterei: Design System V2, tokens, bundle, referência de conteúdo, CLAUDE.md, `ANALISE_ESTRATEGICA.md` (fica como histórico da v2), material bruto, Reels e carrosséis já produzidos.

**Para refazer o painel** depois de editar uma peça nos scripts (de dentro de `planejamento/`):
```
python3 scripts/reconstruir_v3.py --base versoes/painel-v2.2-2026-10-09-antes-da-v3.html
python3 scripts/painel_v3_js.py
```
Atenção: rodar os scripts apaga edições feitas direto no HTML. Edite nos scripts, ou edite só no HTML e deixe de usar os scripts.
**Para desfazer tudo:** copiar `versoes/painel-v2.2-2026-10-09-antes-da-v3.html` sobre `planejamento-postagens.html`.

## 2. O que aconteceu com o plano antigo (09/10/2026 a 07/02/2027)

| | Quantidade | Detalhe |
|---|---:|---|
| Publicações futuras revisadas | 183 | Todas as que tinham data de 09/10 em diante |
| **Mantidas** | 19 | 8 vlogs do YouTube (mesmas datas), 8 sequências de Stories de lançamento dos vlogs, Stories de 09/10 (contagem do vlog), da véspera (19/01) e do embarque (20/01). Só o campo "pilar" mudou |
| **Removidas** | 164 | 80 Reels, 52 Shorts, 25 carrosséis, 1 foto, 5 Stories de "lembrete do vlog" e 1 tarefa de agendamento |
| **Substituídas por novas** | 87 peças + 30 Shorts + 1 tarefa | Nenhuma peça antiga foi copiada; ideias boas foram refeitas com material real (ex.: "Não faça isso" virou "Não compre água em Barcelona"; "Vale ou pula" virou a série com waffle, Boqueria, Disney e Bruxelas) |
| **Histórico** (01 a 08/10) | 10 | Intacto (verificado campo a campo), todos marcados como publicados; 7 receberam os números da auditoria de 08/10 |

## 3. O novo calendário

**87 peças no Instagram:** 70 Reels + 17 carrosséis, de 10/10/2026 a 07/02/2027 (4 Reels + 1 carrossel por semana; segunda e sexta sem post no feed). Mais 30 Shorts no YouTube (reaproveitam os Reels de terça e sábado) e 1 tarefa de agendamento antes da viagem.

| Por pilar | Reels | Carrosséis |
|---|---:|---:|
| Chegar sabendo (utilidade) | 21 | 17 |
| Vontade de ir (desejo) | 19 | 0 |
| Como foi de verdade (identificação) | 15 | 0 |
| Primeiro Dia (série) | 15 | 0 |

| Por destino | Peças | | Por destino | Peças |
|---|---:|---|---|---:|
| Barcelona | 16 | | Madrid | 6 |
| Itália | 15 | | Lisboa | 5 |
| Vários destinos | 12 | | Bruges | 4 |
| Disneyland Paris | 7 | | Bruxelas | 3 |
| Viagem de janeiro (ao vivo) | 7 | | | |
| Paris | 6 | | | |
| Amsterdam | 6 | | | |

**Nível de edição dos Reels:** 22 Nível A, 48 Nível B. **Ganchos:** 14 tipos; nenhum texto de gancho repetido; todos com até 7 palavras (verificado por script). **Mistura:** no máximo 3 peças seguidas da mesma cidade (verificado por script).

**Status do material** (campo novo em cada peça):

| Status | Peças | O que falta |
|---|---:|---|
| Material verificado no repositório | 30 | Só editar (e conferir as pendências da peça) |
| Decupagem pendente | 31 | Achar os planos nos brutos |
| Aguarda dados do Diego | 19 | Custos, opiniões, datas |
| Material futuro (viagem de janeiro) | 7 | Gravar na viagem |

Cada peça tem: data e hora, destino, pilar, objetivo, público e motivação, formato, gancho exato e tipo, primeiro quadro, cenas com tempo (Reels) ou slides (carrosséis), texto na tela, narração, legenda completa, CTA, capa, som, métrica principal, hipótese, teste, material, pendências e checklist.

## 4. Sistema de produção (entregável 5): o que mudou no painel

| Onde | Mudança |
|---|---|
| Página da publicação | Novas seções: público e motivação, primeiro quadro, texto na tela, narração, capa e som, hipótese e teste. Card **Produção** com pilar, nível, tipo de gancho, status do material e pendências. Nos posts publicados, card **Auditoria de 08/10** com seguidores por 1.000 visualizações |
| Resultados (48 h) | Campos novos: **Visualizações** e **Visitas ao perfil** (os antigos continuam) |
| Semanas | Filtro por **pilar**; Stories do dia ligados ao post (pós-post com sticker por pilar); pergunta da semana nas semanas pares; leituras de dados nas tarefas |
| "Vídeos" → **Destinos** | Cada destino com peças por pilar e % de material verificado. Os vlogs do YouTube aparecem como canal complementar (com a checklist de edição de antes) |
| Aprendizados | **Linha de base de 08/10**, **testes T1 a T5** (médias A × B de seguidores, envios e salvamentos por 1.000 visualizações, calculadas dos Resultados), **Reels por pilar** e **leituras** |
| Home | Card **Próxima leitura de dados** com os testes; "Próximos vídeos" virou "YouTube (complementar)"; pendências novas |
| Pendências | 10 pendências novas (vêm do `DATA`, não mais do código) |

O progresso salvo no navegador continua valendo: as chaves dos posts históricos e mantidos não mudaram. As peças novas usam IDs novos (`p200` a `p286`, Shorts `p400` em diante), então nenhuma herda marcação antiga.

## 5. Verificações técnicas feitas

- Leitura e regravação do `DATA` sem perda; histórico (01 a 08/10) idêntico campo a campo, exceto `done` e os números da auditoria; dias de 01 a 08/10 idênticos.
- Todo post está em algum dia de semana (assert no script); 130 dias cobertos de 01/10/2026 a 07/02/2027.
- Chromium headless (Playwright), 430 px e 1280 px: 169 rotas abertas (147 publicações, 19 semanas, calendário, destinos, aprendizados) **sem erro de JavaScript e sem rolagem horizontal**; filtro por pilar e marcação de checklist testados (a peça passa para "Em produção").
- Ganchos com até 7 palavras e sem repetição; no máximo 3 peças seguidas da mesma cidade.

**Não testado:** backup e restauração do progresso (código não mudou), tema escuro (só cores já existentes foram usadas), uso num celular real.

## 6. O que ainda precisa ser localizado ou confirmado

Detalhe por peça no card **Produção** de cada uma; resumo:

1. **Hoje (para 10/10):** originais em resolução cheia do Atomium (IMG_2170 e IMG_2178 são 720p). Se não chegarem, trocar o Reel de 10/10 com o de 13/10 (água, 4K).
2. Conteúdo exato dos 7 posts até 08/10 (para não repetir valores e cenas).
3. Datas das viagens e ordem real das 8 cidades (cotação e contexto).
4. Custos por cidade e por pessoa (todas, exceto Roma).
5. Decupagem de Amsterdam, Bruges, Bruxelas, Paris, Disney, Madrid e Lisboa.
6. Inventário dos vídeos ambientais da Itália e fotos de Florença, Veneza e Milão; cidade do Réveillon.
7. Brutos limpos de Barcelona (o master tem violão no B-roll).
8. Valores de Barcelona "por pessoa?" (€ 31, € 27,50) e moeda do McDonald's.
9. Cidades e datas da viagem de janeiro.
10. Trial Reels disponível? (as fontes divergem entre 200 e 1.000 seguidores).

## 7. Testes prioritários

1. **T3 (CTA de seguir × envio):** responde direto ao problema da auditoria (alcance sem conversão). Começa em 11/10.
2. **T1 (desejo puro × com informação):** decide o papel do conteúdo bonito no perfil. Começa em 17/10.
3. **T4 (capa de foto × papel no carrossel):** decide se o carrossel serve para alcance ou só para salvamento. Começa em 14/10.
4. T2 e T5 em paralelo, sem prioridade sobre os três acima.

## 8. Divergências registradas (não resolvidas por mim)

| # | Divergência | Onde |
|---|---|---|
| 1 | Itália: "sem vídeo" (CLAUDE.md, 10, informação de 05/10) × "alguns vídeos dos ambientes" (pedido de 09/10) | Segui o mais recente; o CLAUDE.md deve ser atualizado pelo Diego depois do inventário |
| 2 | A auditoria de 08/10 não está no repositório; usei os números informados no pedido | `DATA.base` e `DIAGNOSTICO_V3.md` |
| 3 | "Barceloneta" e "Barcelona 2027?" foram associados aos posts p3 e p8 do painel por formato e data (provável, a confirmar) | Painel, card Auditoria |
| 4 | Ganchos do tipo "Desejo" e "Visual (sem texto)" e o CTA "seguir" não estão no DS V2 (5.1 e 2.7) | Usados como teste, sem valor visual novo; ver `ESTRATEGIA_EDITORIAL_V3.md`, seção 11 |
