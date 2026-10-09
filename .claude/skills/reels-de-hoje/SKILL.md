---
name: reels-de-hoje
description: Monta o pacote do Reel do Primeiro Dia (@primeirodiaem) previsto no painel para hoje (ou para a data indicada): gancho, roteiro de cortes, textos na tela, capa, legenda, horário, checklist do Design System e o que medir. Use quando o Diego pedir "criar reels de hoje", "reel de hoje", "o reel do dia" ou "criar o reel de DD/MM".
---

# Reels de hoje

Entrega o Reel do dia **pronto para editar e publicar**, a partir do que o painel já planejou e das regras da marca. Não inventa valor, cena nem erro.

## 1. Descobrir o dia e o post

Rode da raiz do repositório (o fuso é o de Salvador, UTC-3):

```bash
python3 planejamento/scripts/post_do_dia.py --fmt Reel          # hoje
python3 planejamento/scripts/post_do_dia.py 2026-10-16 --fmt Reel   # outra data
```

- Se a data for **até 08/10/2026**, é histórico e já foi publicado: avise e não produza.
- Se **não houver Reel** no dia, diga isso e mostre o próximo Reel do painel; pergunte se quer adiantá-lo.
- Se houver **mais de um Reel**, faça um pacote por Reel, na ordem do horário.
- O `PLACEHOLDERS EM ABERTO` do script lista o que falta (`[valor]`, `[total]`, `[Cena real]`, `[cidade]`).

## 2. Ler as fontes, nesta ordem (consulte, não copie de memória)

1. `CLAUDE.md`: seções 2 (quem aparece), 6 (centralização x 540), 9 (dados reais), 10 (acervo: **não refilmar**, **não criar cena falsa**), 12.
2. `design-system/design-system-primeiro-dia-v2.md`: 0 (cartão de bolso), componente usado no post (2.1 a 2.6), 3.2 (6 estilos de legenda), 5.1 (hooks), 5.2 (estrutura e níveis A e B), 7.3 (checklist). Valores sempre de `design-system/primeiro-dia-tokens-v2.json`; **não crie valor fora dele**.
3. `docs/referencia-conteudo-instagram.md`: 3 (estrutura), 4 (checklist pré-publicação), 8 (métricas).
4. `research/04_manual_de_formatos.md`: o formato do post (R01 a R13, A01 a A10) e as estruturas N1 a N6. `research/03_estrategia_primeiro_dia.md`: pilar e série. `research/07_metricas_e_experimentos.md`: o experimento ligado (E1, E5, E6…) e a regra de decisão.
5. Para Reel de cidade com vlog: `research/06_plano_8_videos.md` (cenas já usadas, para **não repetir a cena de abertura**).

## 3. Perguntar ao Diego antes de montar (uma mensagem só)

Pergunte **só o que falta** e que muda o resultado:

- **Valores reais** de cada placeholder: data, local, valor, moeda e cotação datada. Sem o dado, o Reel não sai com número: ofereça trocar o gancho (outro tipo do DS 5.1) ou o item da semana.
- **Cena ou trecho**: minutagem no vlog ou nome do bruto. Se ele não souber, proponha candidatos do `research/06` ou da transcrição e **diga que são da transcrição automática e precisam de conferência**.
- Se o post é de **erro, perrengue ou surpresa**: isso aconteceu de verdade? Se não, troque; nunca invente.
- Trial Reel: o Diego **não tem Trial** (08/10/2026). Em post de variação, use o plano B do painel: **Reel normal novo**, mesmo tema, gancho novo, outro recorte; **nunca o mesmo vídeo republicado**.
- O foco é só o Diego? Padrão: cenas dos dois juntos servem (CLAUDE.md, 2).

Se ele pedir "faça com o que tiver", assuma o mais provável e **diga a suposição**.

## 4. Montar a entrega (Português do Brasil, direto, comece pela entrega)

1. **Resumo em 3 linhas:** formato, nível (A ou B), objetivo e métrica principal.
2. **Hook:** texto (até 7 palavras) e tipo do DS 5.1. Dê **2 alternativas** de hook só se o Diego pedir ou se o gancho do painel for fraco (diga o motivo).
3. **Tabela de cortes:** tempo · cena e trecho · o que aparece na tela (objeto de marca na posição fixa, estilo de legenda) · som. Cortes de 1,5 a 3 s, no máximo 3 famílias de transição, 70% de cortes secos.
4. **Textos na tela**, exatos, na ordem. Centralizado = x 540.
5. **Capa:** até 4 palavras, dentro da área 3:4.
6. **Legenda do post** em bloco de código: 1ª linha = reforço do gancho, palavras-chave da cidade e do tema, **1 CTA**, no máximo 5 hashtags no fim.
7. **Horário** do painel e o que registrar em 48 h (retenção, envios, salvamentos, seguidores, % de não seguidores, duração).
8. **Story pós-Reel** do dia (está no `post_do_dia.py`).
9. **Checklist de conformidade** (DS 7.3 e referência 4), marcando o que ficou pendente e por quê.
10. **Pendências** (dados, conferência de cena, licença de música).

## 5. Regras que não se quebram

- Dados reais: valor, hora, data e lugar vêm do registro. Não arredonde sem avisar.
- Sem refilmar, sem cena falsa, sem inserir gravação de hoje em experiência passada (CLAUDE.md, 10). Gravação nova só como "material futuro".
- Material bruto (`fonte/`): pode ser analisado, **não** alterado, movido nem apagado.
- Sem repost, marca d'água, introdução, logo ou vinheta; sem engajamento artificial.
- Música: biblioteca do Instagram em volume baixo, ou só som ambiente. Não afirme horário de pôr do sol que não conste no material.
- Gancho fraco, capa ilegível ou ideia fora da marca: **diga com franqueza, com o motivo e a alternativa**.
- Não prometa viralização.
- **Não altere o Design System, os tokens, a referência de conteúdo, o painel** nem revisões anteriores de um Reel sem pedido explícito. Conflito entre documentos: registre a divergência e pergunte ao Diego.

## 6. Depois

- Ofereça **salvar o pacote** em `reels/<cidade-ou-tema>/` (uma pasta por Reel, uma por revisão).
- Se o Diego pedir **render ou edição**, lembre que a divisão entre Claude e CapCut ainda não está definida (CLAUDE.md, 14.9) e pergunte; scripts usam caminho relativo.
- Lembre do registro de 48 h na aba "Resultados" do painel. Só atualize o painel se ele pedir.
