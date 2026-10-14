# Changelog do painel · v5 (14/10/2026)

**Entrega H da revisão v5** · **Base:** painel v4 de 14/10, guardado em `versoes/painel-v4-2026-10-14-antes-da-v5.html` · **Scripts:** `scripts/v5_pecas.py` (peças, calendário e revisões) e `scripts/aplicar_v5.py` (lê a base, aplica, valida e grava) · **Estratégia:** `REVISAO_V5.md`

Para refazer o painel do zero: `python3 scripts/aplicar_v5.py`, rodado de dentro de `planejamento/`. O script parte da cópia da v4 e **não grava o painel se houver violação da regra de cidades**.

## 1. Arquivos

| Arquivo | Situação |
|---|---|
| `planejamento-postagens.html` | Regenerado (v5). Mesmo código, rotas, filtros e chave de `localStorage`; só o bloco `DATA` muda |
| `REVISAO_V5.md` | Novo (A: diagnóstico e estratégia) |
| `INVENTARIO_ACERVO_V5.md` | Novo (B: inventário e D: mapa de uso) |
| `AUDITORIA_CIDADES_V5.md` | Novo, gerado pelo script (E) |
| `BANCO_DE_IDEIAS_V5.md` | Novo (F) |
| `OPORTUNIDADES_CUSTOS.md` | Novo (G) |
| `CHANGELOG_v5.md` | Este arquivo (H) |
| `scripts/v5_pecas.py`, `scripts/aplicar_v5.py` | Novos |
| `versoes/painel-v4-2026-10-14-antes-da-v5.html` | Cópia de segurança da v4 |

Não foram alterados: o Design System, os tokens, o bundle, a referência de conteúdo, o CLAUDE.md, os documentos v3 e v4, os registros de custo e o material bruto (no Drive, nada foi movido, renomeado, apagado ou recompartilhado).

## 2. O que mudou no painel

1. **Regra de cidades em todos os formatos:** no máximo 2 dias por semana (seg a dom) e nunca em dias seguidos, inclusive na virada de semana. Shorts, vlogs, comparações e Stories com cidade central contam. **0 violações** de 12/10/2026 a 07/02/2027.
2. **Calendário do feed refeito** de 15/10/2026 a 07/02/2027: 67 Reels e 16 carrosséis (4 Reels e 1 carrossel por semana).
3. **24 peças novas** feitas de arquivos do Drive e do repositório (lista em `INVENTARIO_ACERVO_V5.md` e no painel, com o campo `v5`).
4. **52 itens da v4 saem** com o motivo registrado no painel (`saem_v5`): 15 peças de custo, 5 peças de Florença, Veneza e Milão (pastas vazias), 1 duplicada (castelo), 3 sem vaga depois da regra de cidades e os 28 Shorts da v4, refeitos no mesmo dia do Reel.
5. **25 Shorts** (p700 a p724), cada um no mesmo dia do Reel de origem, às 20:30, com título de até 60 caracteres e o campo `src` apontando para o Reel.
6. **Custos fora:** nenhum valor em € ou R$ nas peças futuras; as peças de "grátis" mudaram de ângulo sem mudar fatos; o Placar sai da série (Nível B). Os vlogs ganharam a pendência "se a edição tiver trecho de gastos, o Diego decide".
7. **Stories:** a camada de Stories foi refeita dia a dia, com a cidade central registrada (`cid`): pós-post (69 dias), pergunta da semana (14), quiz de sexta (7), diário ao vivo da viagem (19) e **7 sextas sem Stories**, de propósito.
8. **Semanas:** o objetivo e as metas de cada semana foram reescritos para a ordem nova.
9. **Histórico:** p201 (11/10) e p202 (13/10) marcados como publicados, com a evidência citada na observação de cada um. Nada mais do histórico mudou (conferido por script).
10. **Pendências novas** no painel: k 50 a 56 (Drive, Itália, o que saiu de 10 a 14/10, D3, viagem de janeiro, noite em Lisboa e o show de Madrid); k 41 reescrita (D1).

## 2b. Ajuste de 14/10 à tarde (pedido do Diego)

- **p218 (carrossel "Roma de graça", 14/10 18:00) marcado como adiado.** O conteúdo original fica preservado; o painel mostra o aviso e o motivo (valores, cotação e etiqueta `QUANTO CUSTOU`; valores de Trevi e Panteão sem reconferência).
- **Novo p627, "Roma em 3 dias: o roteiro pela hora das fotos" (carrossel, 12 slides, 18/11 18:00):** a versão sem valores. Usa só fotos verificadas do repositório, com a hora do arquivo. Capa de papel com a Rota (T4, variante B). Ocupa a quarta de 18/11, que era do p223 (Bruxelas a Bruges, que dependia de dados do Diego e foi para o banco).
- **Stories de 14/10:** dia sem post, com a enquete "Qual cidade você quer ver primeiro aqui?" (sem cidade central).
- **p401 (Short de 14/10):** sem confirmação de publicação; a observação foi registrada.
- Regra de cidades: continua com 0 violações. T4 continua com 8 carrosséis A e 6 B.

## 3. Testes rodados

| Teste | Resultado |
|---|---|
| Regra de cidades (script, todos os formatos) | 0 violações |
| Valores em € ou R$ nas peças futuras | 0 |
| Varredura de palavras de custo (legenda, tela, capa, cenas, slides, objetivo, hipótese) | Só instruções ("sem preço nesta revisão") e o fato da Tony's ("o dinheiro do cacau") |
| Ganchos com mais de 7 palavras | 0 |
| Ganchos repetidos | Só o marcador dos Reels sem texto do T2 |
| Histórico até 14/10 | Igual à v4, menos p201 e p202 (publicados) |
| IDs da v4 | Todos presentes ou com motivo de saída; nenhum ID duplicado |
| Campos de cada peça do feed (título, gancho, legenda, tela, capa, CTA, objetivo, motivo, hipótese, material, checklist, cenas ou slides, pilar, hora, métrica) | Nenhum vazio |
| Shorts | Todos no dia do Reel de origem; títulos com até 60 caracteres |
| Painel no Chromium headless, a 430 px e a 1.280 px | 0 erros de JavaScript; 19 rotas abertas (início, semanas, semana, calendário, destinos, cidades, aprendizados e peças); sem rolagem horizontal; os 10 filtros respondem |

## 4. Pendências

- **D1** (Reels de fotos de Roma × CLAUDE.md, 10), **D3** (Stories ao vivo × regra de cidades) e **D4** (cidades de janeiro): decisões do Diego (`REVISAO_V5.md`, 4).
- **Decupagem:** 46 peças estão em "Decupagem pendente"; 11 aguardam dados do Diego; 7 são material futuro.
- **Drive:** o limite de 10 MB impede a análise dos vídeos longos (pendência k 50).
- **Duas peças "ok" ainda têm texto entre colchetes** para conferir em site oficial antes de publicar: p248 (o que fecha em 25/12) e p262 (antecedência da venda em 2027).
- **Inventário de 11/10** (`INVENTARIO_DRIVE.md`) está só no branch `claude/adoring-hamilton-omilgr`. Não foi trazido para cá, para não misturar a outra v4.
