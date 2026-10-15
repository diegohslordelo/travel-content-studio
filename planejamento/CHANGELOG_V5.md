# Changelog · planejamento V5

## V5 · 15/10/2026

**Base:** V4 enviada pelo Diego em 15/10/2026 (`versoes/planejamento-primeiro-dia-v4-cadencia-4-reels.html`, preservada sem alteração). **Pedido:** revisão profunda do calendário, da criatividade das peças e da estratégia (prompt de 15/10/2026).

### Arquivos

| Arquivo | Situação |
|---|---|
| `planejamento-primeiro-dia-v5.html` | Novo. Painel interativo V5 (mesmo layout e funções da V4) |
| `versoes/planejamento-primeiro-dia-v4-cadencia-4-reels.html` e `versoes/prompt-revisao-profunda-planejamento-primeiro-dia.md` | Novos no repositório; cópias fiéis da V4 e do prompt enviados |
| `AUDITORIA_CRIATIVA_V5.md` | Novo. Diagnóstico, decisões, pesquisa, critérios, limitações |
| `BANCO_DE_IDEIAS_V5.md` | Novo. 41 ideias com material, fora do calendário, e 5 formatos para testar |
| `v5/*.csv` | Novos. Auditoria semanal de Reels, cidades, países, mapa de formato e grupo por semana, pendências e decisões V4 → V5 |
| `v5/eventos_v5.json` | Novo. Os 155 eventos da V5 |
| `scripts/` | Novos. `grade_v5.py` (datas), `pecas_*.py` (briefings), `auditoria.py`, `montar_v5.py`, `validar_v5.py`, `painel_v5.js` |

### Calendário

- 80 Reels (4 por semana em 20 semanas, com quinta e domingo sempre), 19 carrosséis, 7 fotos, 39 Stories e 10 vídeos longos.
- Os 10 vídeos longos ficaram com as mesmas datas e IDs. Destinos depois de Amsterdam continuam a confirmar; o calendário foi auditado também com a ordem provável do painel original de 05/10/2026.
- 15/10 continua em Lisboa (alternância com Barcelona) com uma peça nova: "Pedimos 'peixinhos' em Lisboa. Não era peixe."
- Stories passaram a ser gerais, ligados às peças da semana. Não contam como aparição de cidade.
- Entraram a Itália (10 Reels de vídeo e 2 carrosséis, com as fotos só em carrossel), o Natal em Roma (24/12) e o Réveillon em Veneza (31/12).

### Peças da V4

- Mantidos: 10 vídeos longos.
- Reformulados com o mesmo ID: trailer de Amsterdam (`IG-20261020-REE-amsterdam-trailer`), Reel da série de Amsterdam (`IG-20261028-REE-amsterdam-first-day`), custo de Amsterdam (`IG-20270211-REE-amsterdam-103`).
- Movidos com o mesmo ID: custo de Paris (`IG-20261126-REE-paris-037`, 26/11 → 29/11), "Custo planejado sem chute" (`IG-20261021-REEL-general-04`, 21/10 → 18/02, agora "A planilha que a gente usa em toda viagem"), checklist de documentos (`IG-20261108-CAR-geral-022`, 09/11 → 26/10).
- Formato novo com o mesmo ID: custo de Lisboa (`IG-20261231-REE-lisboa-067`, Reel de 31/12 → carrossel de 15/02).
- Substituídos: 138. Removidos (horário liberado): 3. Relação peça a peça em `v5/decisoes-v4-v5.csv`.

### Painel

- Briefing completo em cada peça: grupo criativo, público, conceito, gancho principal, 2 alternativos, gancho visual, promessa, payoff, retenção, envio ou salvamento, storyboard, texto na tela, componentes do DS V2, arquivos e trecho do acervo, gravação nova, duração, capa, legenda completa, CTA, adaptação para TikTok e Shorts, métrica, riscos, nota na matriz e relação com a V4.
- Novo filtro por grupo criativo e nova aba "Mudanças V4 → V5".
- A matriz rápida abre com a nota da revisão (antes começava zerada).
- A auditoria de cidades e países considera comparações de várias cidades e mostra os dois cenários de vlog.
- Os status da V4 ligados a datas antigas ("Planejado — trailer em 20/10", "após a estreia") saíram; entraram "Planejado — verificar no acervo", "Aguardando decisão do Diego" e "Gravar talking head".
- Chave de armazenamento local nova (`primeirodia_multiplatform_plan_v5`): status salvos na V4 não passam para a V5.

### Validação (15/10/2026)

- `python3 scripts/validar_v5.py`: 155 eventos, 0 erros (campos obrigatórios, 2 ganchos alternativos, CTA dentro da legenda, nenhum valor em € ou R$ e nenhum "grátis" em texto publicável, IDs únicos, datas dos vlogs, cadência e regras de cidade e país nos dois cenários).
- Painel aberto no Chromium headless: 0 erros de JavaScript, 7 abas renderizadas, modal aberto, filtro por grupo funcionando, sem rolagem horizontal a 390 px. A auditoria do painel bate com a do script (0 violações; 18 transições de país pendentes por causa dos destinos não confirmados).

### Fora do escopo desta revisão

- O Design System, os tokens, a referência de conteúdo e o acervo não foram alterados.
- Nenhum valor de custo foi lido ou usado.
- Nada foi marcado como publicado.

## V5.1 · 15/10/2026 (respostas do Diego)

- Ordem dos vlogs confirmada: Amsterdam 24/10, Bruxelas 07/11, Bruges 21/11, Paris 05/12, Disney 19/12, Madrid 02/01, Lisboa 16/01 (30/01, 13/02 e 27/02 sem destino).
- Os 5 Reels "Primeiro dia em X" foram para a quarta seguinte ao vlog da cidade (Bruxelas 11/11, Bruges 25/11, Paris 09/12, Disney 23/12, Madrid 06/01; Lisboa já estava em 20/01). Os carrosséis de roteiro de Bruxelas, Bruges, Paris, Disney e Madrid foram para a semana do vlog ou para perto dela.
- 11 Reels trocaram de dia para manter cidade e país: LIS-pastel-nata 12/11, BRG-cheiro 15/11, MIL-sforzesco 22/11, PAR-ficou-de-fora 24/11, AMS-de-pijp 10/12, DIS-aposta 13/12, AMS-stroopwafel 22/12, PAR-maior 27/12, LIS-alfama 03/01, BCN-park-guell 10/01, BRU-atomium 17/01.
- Familiares nos vídeos da Itália liberados.
- Validação: 0 erros; 0 violações de cidade e de país; 6 transições de país pendentes (vlogs sem destino).
