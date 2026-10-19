# QA · REV1 · Stories "Caixa de pergunta: o que você quer saber de Amsterdam?"

**Veredito: pronto para postar**, se o vlog de Amsterdam estiver confirmado para sábado, 24/10. Se não estiver, troque a tela 1 pela `_sem-data`. Publicação prevista: **segunda, 19/10/2026, 12h30** (planejamento V5, `V5-20261019-STO-w1a`). Não conta para a meta de Reels nem como aparição de cidade.

## As 3 telas, na ordem

| Tela | Arquivo | Na imagem | O que fazer no Instagram |
|---|---|---|---|
| 1 | `story_amsterdam-pergunta_rev1_1.jpg` | **Foto do Diego na ponte** (enviada por ele em 19/10) · Placa G `SAI SÁBADO` / `AMSTERDAM` + seta (x 72 · y 640, acima do rosto) · legenda "o primeiro dia inteiro / no YouTube, **24/10**" (base y 1580) | Postar como está. Opcional: figurinha de **link** para o canal do YouTube, entre y 1450 e 1600 (abaixo da legenda) |
| 2 | `story_amsterdam-pergunta_rev1_2.jpg` | A viga com o gancho no topo da fachada (`IMG_1408`, prévia do Reel de terça) · Placa `ME PERGUNTA` / `AMSTERDAM` + `?` | Adicionar a figurinha **Perguntas** no centro (x ≈ 540, y ≈ 1100), com o texto abaixo |
| 3 | `story_amsterdam-pergunta_rev1_3.jpg` | O canal de longe (`IMG_1403`) · Bilhete "respondo aqui / na sexta, 23/10." | Postar como está |

**Alternativa à tela 1 (pedido do Diego, 19/10):** `story_amsterdam-pergunta_rev1_1-trilha.jpg`, com a foto do Diego apontando numa trilha. Placa G `O PRÓXIMO DESTINO` / `AMSTERDAM` + seta (a seta repete o braço apontando) e legenda "a espera acabou! / próximo **sábado**, 24/10". É a versão curta do texto dele: "Você mesmo que tava esperando o próximo destino, a espera acabou, próximo sábado vamos pra Amsterdam!" (o DS limita a legenda a 2 linhas de 26 caracteres). Exceção de posição só desta arte: a placa fica em y 440, e não em y 640, porque em y 640 ela cobriria a cabeça (precedente: REV7 do Reel de apresentação). Variante `_1-trilha_sem-data.jpg`: "a espera acabou! / Amsterdam vem aí". Escolha uma das duas para a tela 1; não poste as duas.

Variante: `story_amsterdam-pergunta_rev1_1_sem-data.jpg` (Placa `VEM AÍ` / `AMSTERDAM`, legenda "o primeiro dia inteiro no YouTube", sem data).

### Texto da caixa de perguntas (tela 2)

```
O que você quer saber de Amsterdam?
```

As respostas vão para o Stories de sexta, 23/10 ("Respostas da semana + lembrete do vlog", planejamento V5).

## Conformidade com o DS V2 (5.6 e 7.3)

| Item | Situação |
|---|---|
| Zona segura (topo 256 · base 320 · laterais 72) | ✅ Placa em x 72 · y 640; legenda com base em y 1580 (tela 1) e 1420; Bilhete em y 920; espaço da figurinha entre y 1000 e 1300 |
| Objetos | ✅ 1 objeto de marca por tela: Placa (telas 1 e 2) ou Bilhete (tela 3) |
| Legenda | ✅ Padrão com scrim, 2 linhas, linha de cima ≤ linha de baixo, 1 Destaque (a data) |
| Valores | ✅ Nenhum valor ou preço (risco apontado no planejamento) |
| Texto na UI | ✅ Nada no topo (barra de progresso e nome) nem na base (campo de resposta) |

## Decisões e divergências

- **Tamanho da placa: M (75%).** O brand book diverge: a tabela de variantes do 2.1 diz "Pequena (75%) — thumbnail, Stories", e a matriz do 2.8 diz "P (50%, Stories)". Usei os 75% do 2.1, que é a tabela com as medidas da variante (rótulo 28 px, destino 96 px, seta 72 px). Fica registrado para o Diego decidir; não mudei nenhum documento.
- **Telas renderizadas, não feitas no app.** O planejamento previa "telas simples no próprio Instagram". As telas prontas garantem a placa e o bilhete do DS (o app não tem esses objetos). A interação continua nativa (figurinha Perguntas).
- **Tela 1 refeita (19/10, pedido do Diego).** A primeira versão usava uma paisagem de canal sem protagonista e a placa pequena. Agora: foto do Diego em tela cheia (recorte 1:1 do original 1717 × 2576, x 381), olhos em y ≈ 1130 (zona de rosto do 1.3: y 1000–1150), Placa **G** acima da cabeça (a placa nunca cobre o rosto) e legenda descida para y 1580 (o 1.3 permite até y 1600 nos Stories), fora do rosto e do peito. A foto é do Diego, sem tratamento (DS 0.3, "Real antes de bonito"). Foi guardada em `stories/amsterdam-pergunta/fonte/` (fora do git, como todo material bruto); se faltar, peça de novo.
- **Placa `SAI SÁBADO` / `AMSTERDAM`** segue o modelo do anúncio de post do 5.6 (`SAIU AGORA / ROMA`). Nas telas 1 a placa é G (100%, o tamanho do Reel); na 2, M (75%).
- **Implementação:** composição nova `Story` (com `legendaBaseY`) em `design-system/remotion/src/stories/Story.tsx` (fundo + Placa + legenda Padrão + Bilhete), renderizada no quadro 45 para tudo já estar assentado. Nenhum valor visual novo.

## Como refazer

```bash
cd stories/amsterdam-pergunta/rev1
python3 rev1.py tudo        # fundos → telas (inclui a variante sem data)
```

Usa os brutos do Reel das casas tortas (`reels/amsterdam-casas-tortas/fonte/`, fora do git).
