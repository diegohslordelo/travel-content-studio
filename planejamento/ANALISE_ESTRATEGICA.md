# Análise estratégica do painel de conteúdo

**Data:** 05/10/2026 · **Base analisada:** painel v1 (190 posts, 01/10/2026 a 07/02/2027) · **Critério:** `docs/referencia-conteudo-instagram.md` e Design System V2 (seção 5.1) · **Resultado:** `planejamento-postagens.html` (v2) e `CHANGELOG_v2.md`.

## Veredito

**Ajustar.** A estrutura do painel é boa e acima da média: cada post tem matriz de pontuação, checklist, cenas com objetos do DS, plano B e janela de métricas de 48 horas. O que decide crescimento é o **gancho** e a **enviabilidade** de cada Reel, e aí havia problemas concretos, todos corrigidos na v2.

## O que já está certo (manter)

| Ponto | Por que funciona | Referência |
|---|---|---|
| 80 Reels em 19 semanas (3 a 6 por semana) | Dentro da faixa mínima/ideal | Ref. 7 |
| Séries que cumprem a promessa da marca: custo, erro, hotel, "vale a pena" | Utilidade alta, motivo claro para enviar | CLAUDE.md, 2 |
| Cada post tem matriz 0–10, checklist, CTA único e métrica | Decisão por critério, não por gosto | Ref. 4 e 5 |
| Resultados de 48 h + página de Aprendizados | Base para decidir com dado | Ref. 8 e 10 |
| Carrossel 1×/semana para salvamento | Função certa do formato | Ref. 6 |
| Stories diários na viagem, sem prometer alcance | Função certa do formato | Ref. 6 |
| Trial Reel já tratado como condicional | Evita publicar duplicado | Ref. 9 |

## Problemas encontrados e correção

| # | Problema | Evidência | Correção na v2 |
|---|---|---|---|
| 1 | **Hooks acima do limite de 7 palavras** | 31 Reels com hook de 8 a 15 palavras (ex.: p115 com 13, p133 com 14, p1 com 15) | Todos os Reels a partir de 05/10 passaram a ≤ 7 palavras (DS V2, 5.1). Verificado por script |
| 2 | **Promessa duplicada:** trailer e Reel de custo repetem "Quanto custa X" com 3 dias de intervalo, nas 8 cidades | p15 × p19 (Barcelona), p36 × p40 etc. | Trailer mostra o **total** ("Barcelona em 3 dias: € [total]"); o Reel de custo mostra **para onde foi o dinheiro** ("Onde foi o dinheiro em Barcelona?") |
| 3 | **Reels que só anunciam vídeo** têm baixa enviabilidade: teaser (nota 6, enviabilidade 0) e 4 mini-histórias (sem gancho escrito) | p9, p31, p52, p73, p94; CTA "Ative o lembrete" leva para fora da plataforma | Viraram **"Primeira hora em [cidade]: € [valor]"**, Reel que funciona sozinho e que alguém manda a quem vai viajar. O aviso do vídeo fica nos Stories e na bio |
| 4 | **Ganchos sem promessa:** "Meu primeiro dia em X foi assim..." (8 Reels) e "Isso aconteceu de verdade em X" (7 Reels) | Não dizem o que o espectador ganha; são os mais expostos a pulo nos 3 s | Primeiro dia: "O que ninguém avisa de X." (só com fato real). Momento bruto: "[Cena real] em X." (descrever o que acontece) |
| 5 | **Tipo de gancho mal classificado** | 37 posts marcados "Resultado primeiro"; vários eram só descrição | Reclassificados com os nomes do DS V2 (Preço, Pergunta, Afirmação, Não faça isso, Vale a pena?). Sem isso a tabela "Retenção por tipo de gancho" não ensina nada |
| 6 | **Teste de gancho sem método:** 14 Trials semanais com "Novo tipo (escolher)" | Com 5 a 9 tipos e 14 testes, ficam 1 a 3 por tipo; a ref. 8.3 pede 10 por conclusão | Dois blocos de pares (original × variação): **A = Preço** (7), **B = Afirmação** (7). Leitura final com 10 pares |
| 7 | **Trial Reel provavelmente indisponível** | Blogs de mercado citam mínimo de 1.000 seguidores; a conta nasceu em 01/10 | Plano B explícito: Reel normal **novo** (mesmo tema, hook novo, outro recorte), nunca o mesmo vídeo republicado |
| 8 | **Viagem de janeiro com só 3 Reels/semana** | É o período de material novo, e a frequência cai ao mínimo | +4 Reels (n1 a n4), 5 por semana, em edição leve: "Vale ou pula", "Primeira hora" ×2 (trocas de cidade), "Não faça isso" (só se aconteceu) |
| 9 | **Sem pontos de leitura por dados** | O painel registra métricas, mas não diz quando decidir | Leitura 1 (10 Reels, semana 3), 2 (≈35, semana 8), 3 (≈60, semana 13). Meta = **mediana dos seus 10 primeiros Reels**, não benchmark de mercado |
| 10 | **Reel de apresentação desatualizado** | O painel descrevia 27 s e "Aqui é o Primeiro Dia"; o CLAUDE.md (13) define a REV8 com "Buenos días, Barcelona!" | p1 alinhado à REV8. Risco anotado: o hook é saudação, não promessa; conferir a retenção de 3 s em 48 h |

## Riscos que dependem de decisão do Diego

| # | Tema | Situação | Minha recomendação |
|---|---|---|---|
| D1 | **Itália** (Roma, Florença, Veneza, Milão: 5 carrosséis) | **Resolvido:** há fotos e custos, sem vídeo | Carrosséis com promessa de custo (ver abaixo) |
| D2 | **12 posts "Foto"/photo dump** | Formato sem distribuição para não seguidores; custo de produção baixo | Manter no máximo 1 a cada 2 semanas e usar carrossel (salvamento). Não mexi: é trade-off de grid × tempo |
| D3 | **Organização por cidade em ciclos de 2 semanas** | Quem não te segue não busca "Madrid em 2 dias" de um perfil novo; busca a dor ("quanto custa", "o que evitar") | Já corrigi o gancho. A decisão maior é manter a ordem cronológica das cidades ou intercalar séries (ex.: 1 Reel "Onde foi o dinheiro" por semana de cidades diferentes). Sugiro intercalar após a Leitura 1 |
| D4 | **Carga de produção** | 80 Reels + 54 Shorts + 8 vídeos longos + 18 carrosséis, com checklist de 26 itens por post | Definir **Tier A** (hero, DS completo) e **Tier B** (corte seco + legenda Padrão + 1 objeto). Precisa de aprovação, pois mexe no checklist do DS |
| D5 | **Valores reais** | Ganchos de preço usam `[total]`, `[valor]`, `[X]` | Preencher só com o registro real da viagem (CLAUDE.md, 9). Sem registro, trocar o tipo de gancho |
| D6 | **Teste de horário** (12:30, 18:30, 21:00 até 01/11) | Cada horário recebe temas diferentes, então o resultado mistura horário e tema | Aceitar como sinal fraco; só reforçar se o mesmo horário ganhar em tipos de Reel iguais |

## Regras da plataforma conferidas (05/10/2026)

| Regra | Fonte | Grau de confiança |
|---|---|---|
| Hashtags: limite de 5 por post ou Reel (desde dez/2025); a legenda é indexada | [Instagram Creators no Threads](https://www.threads.com/@creators/post/DSalXGPCWM4/new-hashtag-guidance-starting-today-instagram-will-allow-up-to-hashtags-in-a), [Social Media Today](https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/) | Oficial (@creators) |
| Trial Reels: conta profissional pública, mínimo de 1.000 seguidores | [Metricool](https://metricool.com/instagram-trial-reels/), [uCompares](https://ucompares.com/social-media/instagram/instagram-trial-reels/) | **Estimativa de mercado.** Confirmar no app |
| Republicar vídeo quase idêntico reduz alcance; retrabalhar a própria ideia é permitido | [uCompares](https://ucompares.com/social-media/instagram/instagram-trial-reels/), [CreatorFlow](https://creatorflow.so/blog/instagram-algorithm-2026/) | Estimativa de mercado; consistente com a política de originalidade na ref. 2 |

O painel v1 não usa hashtags nas legendas; se usar, no máximo 3 a 5, no fim.

## Decisões do Diego e atualização v2.1 (05/10/2026)

| Tema | Decisão | O que mudou no painel |
|---|---|---|
| D1 Itália | Há fotos e registro de custos, sem vídeo | Os 5 carrosséis viraram "[cidade] em N dias: € [total]", com slide de Custo. O Diego envia os custos por cidade (pendência no painel). Itália entra no acervo do CLAUDE.md como fotos e custos, não como vídeo |
| D2 Valores | O Diego envia os valores na hora de editar cada vídeo | Os `[valores]` ficam como estão até lá |
| D4 Níveis de edição | Aprovados | Cada Reel ganhou o rótulo **Nível A** (43 Reels: checklist completo do DS) ou **Nível B** (39: corte seco, legenda Padrão, 1 objeto de marca no pico). O B não cria valor visual novo e tem o checklist enxuto |
| D2 Fotos | Aprovado | 8 photo dumps de cidade + o das fotos finais viraram carrossel "[cidade]: 8 fotos, 8 preços". O de 30/01 foi removido (no máximo 1 a cada 2 semanas). Ficam as 2 fotos únicas de Barcelona (03/10 e 09/10) |
| D3 Intercalar | Aprovado, decidido pela Leitura 1 | Regra registrada na semana 3. Os vídeos longos seguem a ordem atual |

**Nível A:** trailer, custo, primeiro dia, primeira hora (fora da viagem), erro, anúncio, orçamento, retrospectiva, hotel, filas e expectativa × realidade.
**Nível B:** momento bruto, curiosidade, mala, escolha de hotel, comida, emoção, trajeto, variações do melhor Reel e todo o diário da viagem.

## Como usar a base

1. Abra `planejamento/planejamento-postagens.html` no navegador. O progresso fica no navegador (use o botão de backup para levar de um aparelho a outro).
2. Antes de produzir cada post: confira o acervo (CLAUDE.md, 10), preencha os `[valores]` e rode o checklist.
3. Nas Leituras 1, 2 e 3 (semanas 3, 8 e 13), decidir pela tabela da ref. 8.2 e registrar em Aprendizados.
4. Não alterar posts já publicados; mudanças novas entram em `versoes/` com data.

## Limites desta análise

Não há dados reais de desempenho (a conta tem 5 dias), então nada aqui prevê viralização. O que a v2 faz é aumentar as chances: hooks claros e curtos, Reels que funcionam sozinhos, utilidade que gera envio e um método para aprender com os primeiros 10 Reels. A pontuação das matrizes dos posts novos (9/10) é julgamento meu, não dado.
