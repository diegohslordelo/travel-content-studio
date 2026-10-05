# Registro de alterações: camada de Stories (painel v2.1 → v2.2)

**Data:** 05/10/2026 · **Base:** `versoes/painel-v2.1-2026-10-05.html` (cópia do painel antes desta mudança) · **Resultado:** `planejamento-postagens.html` · **Estudo:** `STORIES_ESTRATEGIA.md` · **Ideias:** `STORIES_BANCO_DE_IDEIAS.md`

## O que mudou

Só o campo `stories` dentro de `weeks[].days[]` dos dias de **05/10/2026 em diante** que já tinham Stories planejados: **93 de 97 dias** (os 4 restantes são de 01 a 04/10 e ficam como estavam, pela regra do changelog v2: posts anteriores a 05/10 não são alterados).

| O que | Antes | Depois |
|---|---|---|
| Ligação com o post do dia | Nenhuma. Ex.: 13/10, Reel de custo às 12:30, Story "bastidores da edição" sem relação | Pré-Reel 2 h antes e pós-Reel até 5 min depois, por tipo de post (custo, primeira hora, primeiro dia, erro, momento bruto, comida, filas, curiosidade, expectativa × realidade, orçamento, carrosséis) |
| Função de cada Story | Não indicada | Cada parte traz uma etiqueta: RETENÇÃO · RELACIONAMENTO · ENGAJAMENTO · CONVERSÃO · STORYTELLING |
| Momento | Só "publique de manhã" em alguns | MANHÃ · PRÉ-REEL hh:mm · DURANTE O DIA · PÓS-REEL hh:mm · NOITE · FINAL DO DIA |
| Métrica | Nenhuma por dia | Linha "Métrica do dia" (taxa de resposta, ou conclusão e saídas) |
| Viagem (20/01 a 07/02) | "Diário do dia": 3 a 6 Stories | Mantido, com abertura `AO VIVO DA VIAGEM` + Placar ao vivo e fechamento com custo real e "vale ou pula?" |
| Título | "Enquete de decisão" etc. | Mesmo título + " + pré e pós-Reel" ou " + pós-carrossel" quando entra Story ligado ao post |

## O que foi preservado

- **Todos os posts** (193), datas, horários, ganchos, legendas, checklists, vídeos, semanas, `pergunta` da semana e tarefas de interação: idênticos (comparação campo a campo por script).
- **Os 16 posts de Stories** (lançamento, teaser, contagem, partida, embarque): sem alteração.
- **Dias sem Stories** (33): sem alteração, inclusive os dias com caixa de perguntas da semana.
- **Texto original dos Stories:** mantido literalmente em 236 das 251 linhas (94%). A única linha substituída é "Republique o Reel do dia." (15 domingos), trocada pelo Story pós-Reel, que compartilha o Reel com 1 frase que não está no vídeo (decisão S3 na estratégia).
- **Progresso salvo no navegador:** as chaves por data (`s:AAAA-MM-DD`) não mudaram, então quem já marcou "Stories do dia publicados" não perde a marcação.
- **Resto do HTML** (CSS, JavaScript, ícones, painel): idêntico, byte a byte, fora do bloco `DATA`.

## Regras aplicadas na geração

1. Trial Reel não recebe Story (contaminaria o teste, que fala com quem não segue).
2. No máximo 1 sticker de alta fricção por dia: se o bloco do dia já tem enquete ou quiz, o pós-Reel vira só contexto.
3. Máximo de 5 partes por dia no plano atual; teto de 7 por regra.
4. Na viagem não há pré-Reel (é ao vivo).
5. Nada de valor inventado: palpites são perguntas, o número real só vem do registro da viagem.
6. "Sem anunciar até 09/10" continua como regra nos dias de pré-lançamento.

## Verificação

- JSON do painel lido e regravado sem perda; tudo fora de `days[].stories` é idêntico ao original.
- Painel aberto em Chromium headless (430 px) antes e depois: sem erro de JavaScript; bloco de Stories do dia 13/10 renderiza com as 5 partes.
- Nenhum placeholder (`{c}`, `{em}`) sobrou no texto.
- Não alterei o Design System, o CLAUDE.md nem a referência de conteúdo.

## Como desfazer

Copiar `versoes/painel-v2.1-2026-10-05.html` sobre `planejamento-postagens.html`.

## Pendências desta camada

S1 (Marina nos Stories), S2 (modelo de Story pós-Reel no DS), S3 (compartilhar Reel em vez de republicar), S4 e S5: ver `STORIES_ESTRATEGIA.md`, seção 12.
