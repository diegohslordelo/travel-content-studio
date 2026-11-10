# Disney Paris · "5 dicas" · Roteiro · v2 (proposta, aguardando aprovação do Diego)

**Pedido do Diego (10/11/2026):** Reel da Disney com 5 dicas, abrindo com conflito e gancho forte. Roteiro feito **sem partir do acervo** (CLAUDE.md, 7, decisão de 04/11/2026); a imagem se escolhe depois, no backlog de paisagens.
**As 5 dicas são do Diego** (vivência dele e da Marina). Nenhum número de preço entra na fala: o valor pago não foi informado e não é inventado.
**DS só no CTA** (decisão do Diego, 28/10/2026): do gancho até antes do CTA vale a linguagem do formato (`docs/FORMATOS_REELS.md`); o DS entra só na placa final.
**v2 (10/11/2026, pedido do Diego):** o conflito da Opção A passou a mostrar logo no começo, com clareza, o jeito errado que todo mundo faz. A v1 está no histórico do git.
**Suposição:** "Disney" = Disneyland Paris (acervo: 1 dia, 2 parques). O Big Thunder Mountain fica no Disneyland Park (Frontierland).

---

## Opção A (recomendada) · Jeito Errado × Jeito Certo · Tela dividida · ≈ 44 s

**Ideia em 1 frase:** quase todo mundo faz a Disney Paris do jeito errado e paga por isso; 5 escolhas resolvem.
**Como o conflito funciona (v2):** o gancho diz o problema ("do jeito errado") e a fala 2 mostra **o jeito errado em 5 cenas, uma para cada dica**: sábado lotado → dia de semana; fortuna na comida → snack; rodar atrás de fila → app; passar frio → agasalho; ir embora antes da melhor parte → pôr do sol. Cada erro dito no começo é pago por uma dica, e a última ("a melhor parte") fecha o loop. É a estrutura do Trello na ordem: Conflito → Jeito Errado → Virada → Jeito Certo → Mudança.
**Sinal que favorece:** envio. O CTA ("manda pra quem vai fazer a Disney do jeito errado") dá à pessoa um motivo com humor para marcar o amigo. Salvamento como sinal secundário.

### Texto para gravar (no quarto)

```
1. Todo mundo faz a Disney Paris do jeito errado. E paga caro por isso.
2. Vai no sábado lotado, gasta uma fortuna na comida, passa o dia rodando atrás de fila, congela de frio... e vai embora antes da melhor parte.
3. O jeito certo é esse.
4. Um: se der, vai em dia de semana. Sai mais barato e tem menos gente. Cheio sempre tá, mas bem menos.
5. Dois: a comida lá dentro é cara mesmo. Leva um snack na mochila.
6. Três: baixa o app da Disney. Mostra o tempo de cada fila, ajuda no roteiro e dá até pra pedir comida. Foi nosso melhor amigo lá.
7. Quatro: não subestima o frio. Lá venta muito e a sensação despenca.
8. E a melhor parte, que muita gente perde: o pôr do sol do Big Thunder Mountain. Você não vai se arrepender.
9. Manda pra quem vai fazer a Disney do jeito errado.
```

### Roteiro de montagem

| # | Tempo | Etapa | Fala | Imagem (metade de cima / fundo) | Transição | Som |
|---|---|---|---|---|---|---|
| 1 | 0–3,5 s | Conflito (gancho) | "Todo mundo faz a Disney Paris do jeito errado. E paga caro por isso." | Castelo; texto grande na metade de cima, **"TODO MUNDO FAZ A DISNEY PARIS ERRADO"** (palavra de peso: ERRADO). Você embaixo desde o 1º quadro | Corte seco | — |
| 2 | 3,5–11 s | Jeito errado | "Vai no sábado lotado, gasta uma fortuna na comida, passa o dia rodando atrás de fila, congela de frio… e vai embora antes da melhor parte." | 5 imagens rápidas (≈ 1,5 s cada; nenhuma gravada por você abaixo de 2 s, então fotos/animação onde faltar): multidão → bandeja de comida → placa de tempo de fila → vento/gente encolhida → saída do parque de dia. Cada erro ganha um **✕** do formato (cor de destaque âmbar, não o DS) | Corte seco no ritmo da lista | `PDX_impacto` só em "melhor parte" (−4 dB) |
| 3 | 11–12,5 s | Virada | "O jeito certo é esse." | **Você em tela cheia** (respiro) | Empurrão da tela dividida | — |
| 4 | 12,5–18,5 s | Jeito certo 1 | Dica 1 (dia de semana) | Animação: calendário, os dias de semana acendem em âmbar → parque mais vazio. Número **1** no canto | Corte seco | — |
| 5 | 18,5–22 s | Jeito certo 2 | Dica 2 (snack) | Snack saindo da mochila (foto ou ilustração) | Corte seco | — |
| 6 | 22–29,5 s | Jeito certo 3 | Dica 3 (app) | Celular ilustrado com tempos de fila (não imitar print do app) → você e a Marina no parque em "nosso melhor amigo" | Corte seco | `PDX_obturador` no celular (−8 dB) |
| 7 | 29,5–33,5 s | Jeito certo 4 | Dica 4 (frio) | Vento (bandeiras, árvores) + termômetro caindo em "despenca" | **Arrasto** seguindo o vento | `PDX_swish` (−6 dB) |
| 8 | 33,5–40,5 s | Mudança | "E a melhor parte, que muita gente perde: o pôr do sol do Big Thunder Mountain. Você não vai se arrepender." | **Tela cheia** do pôr do sol no Big Thunder Mountain | `PDX_riser` até "pôr do sol" + **Luz de passagem** (a luz do próprio pôr do sol) | Ponte de som: ambiente do parque −8 dB |
| 9 | 40,5–44 s | CTA (DS) | "Manda pra quem vai fazer a Disney do jeito errado." | Pôr do sol continua + placa do DS **MANDA PRA QUEM VAI PRA / DISNEY →** | Chegada da placa | *Clack* (−6 dB), único som do DS |

**Transições:** Empurrão da tela dividida, Arrasto e Luz de passagem (3 não secas, ≥ 1,5 s entre elas; o resto em corte seco). A Luz de passagem nasce do tema: a luz do pôr do sol entra na tela no momento do pôr do sol (`REFERENCIA_EDICAO_FORMATOS.md`, 3.2).
**Duração:** ≈ 44 s (135 palavras a ≈ 3 por segundo), no limite do formato (≤ 45 s) e acima dos 7–30 s da referência de conteúdo. Se passar: (1) apertar pausas; (2) encurtar a dica 3 para "Três: baixa o app. Filas, roteiro e até comida. Foi nosso melhor amigo lá."; (3) nunca acelerar a voz.
**Contexto verdadeiro:** a virada diz "O jeito certo é esse", e não "a gente fez diferente", porque não está registrado se vocês foram em dia de semana nem se passaram frio. Se vocês viveram algum desses erros, dá para trocar por "A gente aprendeu do jeito difícil" (me confirme qual erro aconteceu de verdade).

---

## Opção B · AIDA · Narrado · ≈ 28 s

**Ideia em 1 frase:** 5 coisas para saber antes de ir à Disney Paris, a última é a que vale a viagem.
**Por que essa estrutura:** Atenção (gancho + curiosidade da "última dica"), Interesse (dicas 1 a 4), Desejo (o pôr do sol), Ação (salvar). Narrado: voz do Diego sobre imagens do parque, nenhuma cena com mais de 3 s.
**Sinal que favorece:** salvamento (lista para consultar na viagem). Mais curto, dentro dos 7–30 s.

### Texto para gravar (no quarto)

```
1. Não vá pra Disney Paris sem ver isso: a maioria paga mais, pega fila e perde a melhor parte.
2. Um: se der, vai em dia de semana. Ingresso mais barato e menos gente. Cheio sempre tá.
3. Dois: a comida lá dentro é cara mesmo. Leva um snack.
4. Três: baixa o app. Mostra as filas, ajuda no roteiro e ainda pede comida. Foi nosso melhor amigo lá.
5. Quatro: não subestima o frio. Venta muito e a sensação cai.
6. E cinco: no fim do dia, vai pro Big Thunder Mountain ver o pôr do sol. Não tem como se arrepender.
7. Salva esse vídeo pra tua viagem.
```

### Roteiro de montagem

| # | Tempo | Etapa AIDA | Fala | Imagem | Transição | Som |
|---|---|---|---|---|---|---|
| 1 | 0–3,5 s | Atenção | "Não vá pra Disney Paris sem ver isso: a maioria paga mais, pega fila e perde a melhor parte." | Castelo; texto grande **"NÃO VÁ PRA DISNEY PARIS SEM VER ISSO"** | Corte seco | — |
| 2 | 3,5–8,5 s | Interesse | Dica 1 | Multidão (2,5 s) → parque mais vazio (2,5 s); número **1** grande no canto | Corte seco | `PDX_impacto` no "Um" (−4 dB) |
| 3 | 8,5–11,5 s | Interesse | Dica 2 | Comida do parque | Corte seco | — |
| 4 | 11,5–17 s | Interesse | Dica 3 | Placa de fila → ilustração de celular com filas → Diego e Marina | Corte seco no ritmo | `PDX_obturador` (−8 dB) |
| 5 | 17–20 s | Interesse | Dica 4 | Vento (bandeiras, árvores) | Arrasto | `PDX_swish` (−6 dB) |
| 6 | 20–25 s | Desejo | Dica 5 | Pôr do sol no Big Thunder Mountain, tela cheia | Luz de passagem | `PDX_riser` até "pôr do sol" |
| 7 | 25–28 s | Ação (DS) | "Salva esse vídeo pra tua viagem." | Plano do pôr do sol + placa **SALVA PRA TUA / VIAGEM →** | Chegada da placa | *Clack* (−6 dB) |

---

## Recomendação: Opção A

O problema fica claro em 3 s ("do jeito errado") e concreto em 11 s (as 5 cenas do erro). Cada erro vira uma promessa que a dica paga, o que segura até o fim, e o pôr do sol fecha o "vai embora antes da melhor parte". O rosto aparece desde o 1º quadro (o gancho dividido é o que mais prende, `FORMATOS_REELS.md`, 4.2).

**Sobre os dois ganchos que você sugeriu:**
- **"A Disney não quer você lá"** chama atenção, mas não diz qual é o problema: a pessoa precisa esperar para entender. Na v2 o gancho nomeia o erro direto ("do jeito errado") e a fala 2 o descreve. Se quiser testar a sua frase, ela entra como texto na tela do gancho sobre a mesma fala.
- **"Não vá pra Disney Paris sem ver isso antes"** é uma fórmula muito repetida no nicho. Funciona, mas é genérica. Ficou na Opção B, com a curiosidade da "última dica" para segurar até o fim.

**Teste sugerido** (referência de conteúdo, 8.3): se publicar A agora, a B pode virar Trial Reel depois, para comparar gancho de conflito × gancho de lista. Só vale como comparação se as duas forem do mesmo formato. Como A e B diferem em formato e gancho, o resultado indica tendência, não prova.

---

## Como gravar

- **Opção A (tela dividida):** do peito para cima, olhando para a lente, celular na vertical, luz de frente. Tom de quem conta um segredo para um amigo, com energia no "todo mundo".
- **Opção B (narrado):** celular perto da boca, lugar silencioso, tom de áudio de WhatsApp.
- Nas duas: **1 tomada por bloco**, **1 s de pausa entre blocos** e **1 s de silêncio antes de parar** (o iPhone corta ≈ 0,27 s do fim do áudio).
- Bloco 1: grave **duas tomadas** (uma séria, uma com meio sorriso). A capa sai do quadro em que o gancho está completo.

## A confirmar antes da montagem

1. **Plano do pôr do sol no Big Thunder Mountain:** é o pagamento do Reel. Conferir se existe no acervo da Disney. Se não existir, não se cria cena falsa (CLAUDE.md, 10): a alternativa é foto com licença livre, com crédito, e a fala continua verdadeira porque é a dica de vocês.
2. **Planos com vento e com multidão / parque vazio:** conferir no acervo na fase de imagem.
3. **Print do app:** usar ilustração, não imitar a tela do app como se fosse captura real, a menos que exista print de vocês.
4. **Número de preço (opcional):** se quiser precisão em euros na dica 1, me passe quanto pagaram ou confirmo no calendário oficial na semana da postagem. Hoje fica sem número.

## Fatos externos conferidos (10/11/2026)

| Fato usado | Situação | Fonte |
|---|---|---|
| O ingresso datado muda de preço por dia; dia de semana fora de alta costuma sair mais barato | Confirmado em guias de terceiros e no calendário de preços 2026–2027 (períodos a partir de 80 €, 93 € e 100 € por adulto, conferido por eles em 29/10/2026). A fala diz "sai mais barato", sem número | [tarifs.org, calendário](https://tarifs.org/en/disneyland-paris-price-calendar) · [DLP Guide, ingressos](https://dlpguide.com/planning/booking/park-tickets) |
| Pode levar lanche e bebida (sem cooler grande, sem vidro, nada que precise esquentar) | Guias de terceiros; não achei a página oficial. Conferir no FAQ oficial antes de postar | [DLP Tips](https://dlptips.com/taking-food-to-disneyland-paris-rules-money-saving-advice/) · [Sortiraparis](https://www.sortiraparis.com/en/what-to-visit-in-paris/walks/articles/351513-are-you-allowed-to-bring-your-own-picnic-to-disneyland-paris) |
| O app mostra tempo de fila e permite pedir comida (Mobile Order em restaurantes selecionados) | Página do app na App Store + guias | [App Store](https://apps.apple.com/app/id396908589) · [dein-dlrp](https://www.dein-dlrp.de/en/disneyland-paris-holiday/services/disneyland-paris-app.html) |
| Frio e vento; pôr do sol no Big Thunder | Vivência do Diego (dica pessoal, não fato externo) | Diego, 10/11/2026 |
