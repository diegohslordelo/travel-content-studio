# QA · REV1 · Stories "Caixa de pergunta: o que você quer saber de Amsterdam?"

**Veredito: pronto para postar**, se o vlog de Amsterdam estiver confirmado para sábado, 24/10. Se não estiver, troque a tela 1 pela `_sem-data`. Publicação prevista: **segunda, 19/10/2026, 12h30** (planejamento V5, `V5-20261019-STO-w1a`). Não conta para a meta de Reels nem como aparição de cidade.

## As 3 telas, na ordem

| Tela | Arquivo | Na imagem | O que fazer no Instagram |
|---|---|---|---|
| 1 | `story_amsterdam-pergunta_rev1_1.jpg` | Casas tortas do canal (`IMG_1403-1`) · Placa `SAI SÁBADO` / `AMSTERDAM` + seta · legenda "o vlog completo / no YouTube, **24/10**" | Postar como está. Opcional: figurinha de **link** para o canal do YouTube, entre y 1450 e 1600 (abaixo da legenda) |
| 2 | `story_amsterdam-pergunta_rev1_2.jpg` | A viga com o gancho no topo da fachada (`IMG_1408`, prévia do Reel de terça) · Placa `ME PERGUNTA` / `AMSTERDAM` + `?` | Adicionar a figurinha **Perguntas** no centro (x ≈ 540, y ≈ 1100), com o texto abaixo |
| 3 | `story_amsterdam-pergunta_rev1_3.jpg` | O canal de longe (`IMG_1403`) · Bilhete "respondo aqui / na sexta, 23/10." | Postar como está |

Variante: `story_amsterdam-pergunta_rev1_1_sem-data.jpg` (Placa `VEM AÍ` / `AMSTERDAM`, legenda "o vlog completo no YouTube", sem data).

### Texto da caixa de perguntas (tela 2)

```
O que você quer saber de Amsterdam?
```

As respostas vão para o Stories de sexta, 23/10 ("Respostas da semana + lembrete do vlog", planejamento V5).

## Conformidade com o DS V2 (5.6 e 7.3)

| Item | Situação |
|---|---|
| Zona segura (topo 256 · base 320 · laterais 72) | ✅ Placa em x 72 · y 640; legenda com base em y 1420; Bilhete em y 920; espaço da figurinha entre y 1000 e 1300 |
| Objetos | ✅ 1 objeto de marca por tela: Placa (telas 1 e 2) ou Bilhete (tela 3) |
| Legenda | ✅ Padrão com scrim, 2 linhas, linha de cima ≤ linha de baixo, 1 Destaque (a data) |
| Valores | ✅ Nenhum valor ou preço (risco apontado no planejamento) |
| Texto na UI | ✅ Nada no topo (barra de progresso e nome) nem na base (campo de resposta) |

## Decisões e divergências

- **Tamanho da placa: M (75%).** O brand book diverge: a tabela de variantes do 2.1 diz "Pequena (75%) — thumbnail, Stories", e a matriz do 2.8 diz "P (50%, Stories)". Usei os 75% do 2.1, que é a tabela com as medidas da variante (rótulo 28 px, destino 96 px, seta 72 px). Fica registrado para o Diego decidir; não mudei nenhum documento.
- **Telas renderizadas, não feitas no app.** O planejamento previa "telas simples no próprio Instagram". As telas prontas garantem a placa e o bilhete do DS (o app não tem esses objetos). A interação continua nativa (figurinha Perguntas).
- **Placa `SAI SÁBADO` / `AMSTERDAM`** segue o modelo do anúncio de post do 5.6 (`SAIU AGORA / ROMA`).
- **Implementação:** composição nova `Story` em `design-system/remotion/src/stories/Story.tsx` (fundo + Placa + legenda Padrão + Bilhete), renderizada no quadro 45 para tudo já estar assentado. Nenhum valor visual novo.

## Como refazer

```bash
cd stories/amsterdam-pergunta/rev1
python3 rev1.py tudo        # fundos → telas (inclui a variante sem data)
```

Usa os brutos do Reel das casas tortas (`reels/amsterdam-casas-tortas/fonte/`, fora do git).
