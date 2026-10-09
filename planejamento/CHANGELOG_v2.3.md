# Registro de alterações: painel v2.2 → v2.3

**Data:** 08/10/2026 (mudanças a partir de 09/10/2026) · **Base:** `versoes/painel-v2.2-2026-10-08.html` (cópia idêntica do painel antes desta mudança) · **Resultado:** `planejamento-postagens.html` · **Pesquisa:** `../research/` · **Log completo, com antes, depois, motivo e fonte:** `../research/13_log_alteracoes_calendario.md`

## O que mudou (resumo)

| O que | Quantidade | Posts |
|---|---|---|
| Reels novos "Primeiro olhar" (Nível B, pilar 6, sexta 19:00) | 7 | p190 a p196 |
| Shorts de segunda trocados por "Primeiro olhar" (mesmo corte do Reel de sexta) | 7 | p26, p47, p68, p89, p110, p131, p152 |
| Dias de sexta com pós-Reel nos Stories e tarefa de comentários | 7 | 16/10, 30/10, 13/11, 27/11, 11/12, 25/12, 08/01 |
| Opção extra de título nos 8 vídeos longos | 8 | campo `videos[].titulos` |
| Observação de conferência de capítulos e preços | 1 | p13 |
| Observações de semana (Leituras 1, 2, 3, Black Friday, Carnaval) | 5 | semanas 2, 3, 8, 13 e 18 |

Total: 42 registros (35 da pesquisa + 7 marcações `done` autorizadas pelo Diego). **Nenhum post removido.** A contagem de posts passou de 193 para 200.

## O que foi preservado

- Posts, dias e semanas **até 08/10/2026**: idênticos (exceto o `done` acima) (comparação campo a campo por script).
- **Checklists** dos posts existentes: não mudaram (o progresso salvo no navegador usa a posição de cada item).
- Campos `done`: **só mudaram p2, p3, p4, p5, p6, p8 e p9, para `true`, por autorização expressa do Diego** ("todos os posts até hoje eu fiz"). Conteúdo e checklist desses posts ficaram iguais.
- Fora do bloco `DATA`, o HTML (CSS, JavaScript, ícones) é idêntico byte a byte.
- Design System, CLAUDE.md e referência de conteúdo: não alterados.

## Verificação

- `python3 research/scripts/aplicar_mudancas_calendario.py --verificar`: sem problemas.
- Painel aberto em Chromium headless (430 px): 200 posts, 19 semanas e 8 vídeos renderizam, sem erro de JavaScript.

## Como desfazer

Copiar `versoes/painel-v2.2-2026-10-08.html` sobre `planejamento-postagens.html`, ou `git revert` do commit desta pesquisa.

## Pendências desta mudança

Os 7 Reels "Primeiro olhar" dependem da aprovação do pilar 6 pelo Diego (D1 em `research/03`). Se não aprovar, trocar cada um por outro Reel de série da cidade; os 7 Shorts de segunda seguem a mesma decisão.
