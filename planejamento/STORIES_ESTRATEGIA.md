# Stories no Primeiro Dia: estudo, estratégia e playbook

**Data:** 05/10/2026 · **Escopo:** Instagram Stories de `@primeirodiaem` · **Aplicado em:** `planejamento-postagens.html` (camada de Stories) · **Banco de ideias:** `STORIES_BANCO_DE_IDEIAS.md` · **Registro de alterações:** `CHANGELOG_stories.md`

Este documento não altera o Design System. Todo componente visual de Stories citado aqui já existe no DS V2.1 (seção 5.6, 4.x e 5.1). Onde falta algo, está em "Lacunas e decisões" no fim.

---

## 1. Resumo executivo

1. **Stories não são um canal de descoberta.** A Meta descreve Stories como forma de "crescer mais perto das pessoas e interesses de que você gosta" e ranqueia por histórico de visualização, histórico de engajamento e proximidade com quem postou. Adam Mosseri disse (jan/2025) que, para a maioria dos criadores, o Feed é o melhor caminho para alcançar mais gente. Quem descobre o Primeiro Dia chega por **Reels**.
2. **O papel dos Stories é manter, aproximar e converter** quem já chegou: quem seguiu, quem visitou o perfil depois de um Reel, quem respondeu uma vez. É o único formato em que a audiência conversa com Diego em privado (resposta vira DM), e a resposta é o sinal que a própria Meta diz usar para ordenar Stories.
3. **Para uma conta nova, o custo precisa ser baixo.** Com poucos seguidores, o alcance de Stories é pequeno. Por isso a estratégia é: poucos Stories, cada um com função, quase todos feitos com o que o dia já gera (Reel, edição, planejamento, viagem). Nada de produção própria para Stories.
4. **O painel já tinha uma camada de Stories** (97 de 130 dias e 16 sequências de lançamento, teaser e viagem). O problema era outro: os Stories do dia não conversavam com o Reel do dia (ex.: 13/10, Reel de custo, Story de "bastidores da edição" sem ligação com o número que sai à noite). A integração liga os dois sem trocar o que já estava planejado.
5. **Limite prático: até 7 Stories por dia, tipicamente 2 a 5.** Os dois estudos de mercado que encontrei apontam queda de conclusão acima de 5 a 7 Stories por dia. Não há dado para contas pequenas, então o limite vira teste (seção 10).
6. **Nada aqui prova que Stories fazem uma conta nova crescer.** O que existe é: função clara, custo baixo, métricas próprias e testes para decidir com dados do próprio perfil.

## 2. O papel dos Stories no crescimento (a pergunta central)

> Stories contribuem para o crescimento de uma conta nova?

**Resposta curta: contribuem para reter e converter o que o Reel já trouxe; não contribuem para trazer gente nova.**

| Etapa do funil | Stories ajudam? | Por quê | Grau de evidência |
|---|---|---|---|
| **Descoberta** (quem não conhece encontra o perfil) | **Pouco ou nada** | Meta: Stories servem para "grow closer" com quem se importa; Mosseri: Feed é o melhor para alcançar mais gente; Hootsuite: baixo alcance entre não seguidores | Oficial + mercado |
| **Retenção** (seguidor continua voltando) | **Sim, é a função principal** | O ranking de Stories depende de quanto você já vê e interage com aquele perfil; hábito gera hábito | Oficial |
| **Relacionamento** (proximidade com Diego) | **Sim** | Única superfície com resposta privada; proximidade é sinal de ranking | Oficial |
| **Engajamento** (respostas, sticker, compartilhamento) | **Sim, mas só entre seguidores** | Meta prevê chance de toque, resposta e avanço; resposta é o sinal mais forte | Oficial |
| **Conversão** (seguir, assistir o Reel, visitar, responder, conversar) | **Parcial** | Quem vê o círculo de Story ao visitar o perfil tem mais um motivo para seguir. Isso é hipótese, não dado da Meta | Hipótese |

**O que é hipótese e não fato:**
- "Stories aumentam o alcance dos Reels." A Meta não confirma. O que ela diz é que Stories alimentam o ranking *da bandeja de Stories*. Blogs de mercado extrapolam para Reels; não há fonte oficial.
- "Stories fazem a conta nova crescer mais rápido." Nenhum dos dados encontrados é de conta com menos de 1.000 seguidores.

**Decisão:** tratar Stories como camada de retenção e relacionamento, com custo baixo, e medir a conversão (visita ao perfil e seguidores ganhos por Story) no próprio Insights antes de investir mais.

## 3. Funil: Reel → Story → interação → DM → comunidade

```
REEL ─ descoberta ──────────────► (quem não conhece chega)
   │
   ▼  perfil visitado (círculo de Story visível)
STORY ─ contexto e personalidade ─► (Diego fala, mostra o que ficou de fora)
   │
   ▼
INTERAÇÃO ─ palpite, enquete, vale ou pula, caixa de perguntas
   │
   ▼
DM ─ Diego responde a quem respondeu (relacionamento de 1 para 1)
   │
   ▼
COMUNIDADE ─ resposta vira Story ("comentário que virou ideia"), vira pauta
   │
   ▼
NOVO REEL ─ a pauta nasceu da audiência; quem participou volta para ver
```

**Como cada elo conversa com o seguinte (regras que o painel aplica):**

| De → Para | Mecânica | Onde está no painel |
|---|---|---|
| Reel → Story | Story pós-Reel (compartilhar o Reel com 1 frase que não está no vídeo) | "Parte NN · PÓS-REEL" |
| Story → Reel | Palpite pré-Reel ("quanto custou?", "qual foi o erro?") cria expectativa; o número só aparece no Reel | "Parte 01 · PRÉ-REEL" |
| Story → Interação | 1 sticker por dia (enquete, quiz, slider ou caixa) | Etiqueta ENGAJAMENTO |
| Interação → DM | Responder a quem respondeu, com nome ou contexto | Pós-Reel de custo: "responda por DM a 3 palpites" |
| DM → Comunidade | "Comentário que virou ideia" e resposta da caixa viram Story | Domingo: "Republicar e agradecer" (preservado) |
| Comunidade → Reel | Pergunta recorrente vira Reel (Primeira hora, Erro, Custo) | Registro de Aprendizados |

## 4. O que funciona em Stories: taxonomia aplicada ao Primeiro Dia

Para cada categoria: o que é, função e a restrição do projeto (CLAUDE.md, seções 9 e 10).

| Categoria | Função típica | Aplicação no Primeiro Dia | Restrição |
|---|---|---|---|
| **Bastidores** (gravação, erro, edição, making of) | Relacionamento | Print da timeline, dificuldade real da edição, montagem da identidade | Só o que existe hoje; não encenar |
| **Storytelling** (história do dia, imprevisto, descoberta) | Retenção | Micro-história de uma foto de Barcelona; o que ficou fora do Reel | Acervo é passado: marcar como lembrança, nunca como "agora" (CLAUDE.md, 10) |
| **Interação** (enquete, quiz, caixa, slider, duas opções) | Engajamento | Palpite, "vale ou pula?", "onde foi isso?" | 1 sticker de alta fricção por dia |
| **Curiosidade** ("vocês sabem quanto custa?") | Retenção + engajamento | Palpite antes do Reel; revelar só no Reel | Valor real só do registro da viagem (CLAUDE.md, 9) |
| **Personalidade** (opinião, humor, reação) | Relacionamento | Reação a uma resposta, opinião curta em câmera | "Direto, transparente, curioso, bem-humorado" (DS V2, Plataforma) |
| **Viagem** (aeroporto, transporte, hotel, comida, preços, perrengue) | Storytelling | Diário ao vivo em janeiro, com Placar ao vivo e selo `AO VIVO DA VIAGEM` | Só durante a viagem de 20/01 a 07/02 |
| **Continuação de Reels** | Retenção | Pós-Reel: contexto, o que ficou fora, resultado do palpite | Não repetir o Reel |
| **Comunidade** (perguntas, DMs, recomendações) | Conversão + relacionamento | Caixa de perguntas semanal, resposta em vídeo, "comentário que virou ideia" | Pedir permissão antes de mostrar nome ou DM |

**O que fica de fora de propósito:** sequência de fotos da mesma atração, repost integral do Feed, enquete sem consequência, pergunta genérica ("o que vocês acham?"), Story só promocional.

## 5. Frequência e fadiga

**O que os dados dizem (todos de mercado, nenhum de conta nova):**

| Dado | Fonte | Leitura |
|---|---|---|
| 1 a 7 Stories por dia mantêm a conclusão mais alta; acima de 7 ela cai | Metricool (resumindo Socialinsider 2025) e Buffer (9,6 mi de posts) | Teto de 7 |
| Visualizações podem cair depois do 5º Story do dia | Buffer | Faixa típica de 2 a 5 |
| Saída é maior no 1º Story (23,8%) e cai até o 9º (13,3%) | Socialinsider 2025 (161.180 Stories) | O 1º Story decide: abrir com o gancho do dia |
| Média das contas analisadas: 2 Stories por dia, conclusão 70%, saída 5% | Dash Social (jan–jun/2025, mais de 2.000 marcas com 1.000+ seguidores) | Não são metas: marcas ≠ conta nova |

**Ponto em aberto que não escondo:** o Socialinsider também mostra que o alcance sobe com o número de Stories na sequência (até 13 Stories). Isso mede alcance por tamanho de sequência, não retenção por dia, e as duas leituras não se contradizem, mas também não se resolvem sozinhas. Por isso o teste T1 (seção 10).

**Regra do projeto:**

| Tipo de dia | Quantidade | Estrutura |
|---|---|---|
| Sem post no Instagram | 0 a 2 | Só se houver função clara; dia vazio é permitido |
| Dia de Reel ou carrossel | 2 a 5 | Pré-Reel (quando o tipo pede) + 1 bloco do dia + pós-Reel |
| Dia de lançamento de vídeo longo | 4 a 5 | Sequência já planejada (`stories_launch`), preservada |
| Viagem (20/01 a 07/02) | 4 a 7 | Manhã (contexto) · durante (experiência) · final (custo e vale ou pula) |
| **Nunca** | mais de 7 | Cai a conclusão |

## 6. Métricas

**O que o Instagram entrega por Story** (Insights > Conteúdo que você compartilhou > Stories): alcance, impressões, visitas ao perfil, seguidores ganhos, respostas, compartilhamentos, toques em sticker, toques em link, navegação (avançar, voltar, próximo Story, sair).

**Métricas que importam, em ordem:**

| # | Métrica | Fórmula | Por que importa | Sinal |
|---|---|---|---|---|
| 1 | **Taxa de resposta** | respostas ÷ alcance | Resposta é um dos três sinais que a Meta diz usar para ordenar Stories (toque, curtida, resposta) e é o que abre DM | Positivo |
| 2 | **Story Engagement Rate (SER)** | (respostas + toques em sticker + compartilhamentos + curtidas) ÷ alcance | Resume a interação de um Story em um número comparável entre dias | Positivo |
| 3 | **Taxa de conclusão do dia** | alcance do último Story ÷ alcance do 1º Story do dia | O Instagram não entrega "conclusão" pronta; este é o substituto. Mostra se a sequência segura | Positivo |
| 4 | **Taxa de saída** | saídas ÷ impressões (por Story) | A Meta prevê a chance de o usuário sair; acima da sua mediana é sinal de que o Story não segurou | Negativo |
| 5 | **Taxa de avanço** | toques para avançar ÷ impressões | Avanço alto = conteúdo longo ou sem gancho. Em Story de contexto, algum avanço é normal | Negativo |
| 6 | **Visitas ao perfil por Story** | visitas ao perfil ÷ alcance | Mede se o Story leva a olhar o perfil | Conversão |
| 7 | **Seguidores ganhos por Story** | seguidores ganhos (Insights) ÷ alcance | Mede conversão direta; esperar número muito pequeno no começo | Conversão |
| 8 | **Conversas de DM por semana** | contagem manual de DMs iniciadas a partir de Stories | Mede relacionamento, que o Insights não mostra | Relacionamento |
| 9 | **Toques para voltar** | toques para voltar ÷ impressões | Alto = quiseram rever (bom em informação com número ou preço) | Positivo, se for conteúdo de utilidade |

**O que não vale a pena acompanhar sozinho:** curtidas (sinal mais fraco), impressões (inclui repetição), número bruto de visualizações (depende do tamanho da audiência).

**Meta:** a mediana dos seus 10 primeiros dias com 3 ou mais Stories, não benchmark de mercado. Os números de mercado (conclusão 68% a 70%, saída 5% a 6%) vêm de marcas com mais de 1.000 seguidores e servem só como ordem de grandeza.

**Quando ler:** junto das Leituras 1, 2 e 3 do painel (semanas 3, 8 e 13). Registrar na página de Aprendizados.

## 7. Pilares de Stories do Primeiro Dia

Nove pilares. Cada um foi ligado ao que o painel já tinha (coluna "No painel").

| # | Pilar | Objetivo | Quando usar | Exemplo | CTA | Métrica principal | Relação com Reels | Frequência | No painel |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Palpite antes do Reel** | Criar expectativa e dar motivo para voltar | 2 h antes de Reel de custo, primeira hora, erro, filas, orçamento | "Quanto você acha que custaram os dias em Barcelona?" | Responder o palpite | Taxa de resposta | Direto: o número real só aparece no Reel | 1 a 2 por semana | "PRÉ-REEL" (novo) |
| 2 | **Pós-Reel: o que ficou de fora** | Reter quem assistiu e puxar quem não viu | Logo depois de publicar | "Faltou isto no corte: [fato real]" | Ver o Reel | Conclusão do dia | Complementa, não repete | Todo dia de Reel que couber | "PÓS-REEL" (novo; substitui "Republique o Reel do dia") |
| 3 | **Vale ou pula** | Gerar opinião rápida com a promessa da marca | Comida, hotel, passeio, fila | Enquete nativa com o prato do Reel | Votar | Taxa de resposta e SER | Serve de gancho para "Vale ou pula" | 1 a 2 por semana | Pós-Reel de comida; fechamento do dia na viagem |
| 4 | **Bastidores da edição** | Aproximar e mostrar processo | Dia de edição de vídeo longo | Print da timeline, dificuldade real | "Qual corte você manteria?" | Retenção (conclusão) | Mostra o vídeo da semana em construção | 1 por semana | "Bastidores da edição" (preservado) |
| 5 | **Lembrança com quiz** | Reativar o acervo e treinar o olhar da audiência | Dias sem Reel forte | "Onde foi isso?" com 3 cidades | Responder o quiz | Taxa de resposta | Usa o acervo sem inventar cena nova | 1 por semana | "Lembrança com quiz" (preservado) |
| 6 | **Planejamento da próxima viagem** | Co-criar: a audiência decide e acompanha | Até 20/01 | Enquete de cidade, hotel, roupa para o frio | Votar | SER e DMs | Alimenta Reels de orçamento, mala, anúncio | 1 por semana | "Planejamento" (preservado) |
| 7 | **Pergunta da semana** | Gerar DM e pauta | 1 por semana (já definido por semana) | Caixa de perguntas | Perguntar | Conversas de DM | Respostas viram Reels e carrosséis | 1 por semana | `pergunta` da semana (preservado) |
| 8 | **Diário ao vivo da viagem** | Retenção e urgência durante a viagem | 20/01 a 07/02 | Selo `AO VIVO DA VIAGEM` + Placar ao vivo | "Vale ou pula?" | Conclusão do dia | Diário em Reel e Short no mesmo dia | 4 a 7 por dia | "Diário do dia" (preservado e estruturado) |
| 9 | **Comunidade: comentário que virou ideia** | Mostrar que a audiência é ouvida | Domingo | Comentário real (com permissão) virando pauta | Mandar a próxima | Conversas de DM | Fecha o ciclo do funil | 1 por semana | "Republicar e agradecer" (preservado) |

## 8. Estrutura de um dia (quando aplicar)

Não é fixa. O painel só usa as partes que o dia pede.

| Momento | Função | Exemplo |
|---|---|---|
| **Manhã** | Contexto, expectativa | Enquete que será respondida à noite; selo `AO VIVO` na viagem |
| **2 h antes do Reel** | Retenção, engajamento | Palpite que o Reel responde |
| **Durante o dia** | Experiência, bastidor, personalidade | Edição, planejamento, lembrança com quiz |
| **Reel entrou** | Retenção, conversão | Compartilhar o Reel com 1 frase que não está no vídeo |
| **Final do dia** | Resumo e interação | Resultado da enquete; na viagem, custo do dia e "vale ou pula" |

**Dia de Reel:** pré-Reel → bloco do dia → pós-Reel.
**Dia de carrossel:** bloco do dia → pós-carrossel com pergunta "qual slide você mandaria?" (dá motivo de envio).
**Trial Reel:** sem Story. Mostrar um Trial para seguidores contamina o teste, cuja função é falar com quem não segue.

## 9. Playbook (Story Playbook · Primeiro Dia)

| Tema | Regra |
|---|---|
| **Quando postar** | Pré-Reel 2 h antes do Reel; pós-Reel até 5 min depois; bloco do dia em horário livre; na viagem, espaçado ao longo do dia, não em rajada |
| **Quando não postar** | Dia sem função clara; quando o Story só repete o Reel; para anunciar o vídeo longo antes de 09/10 (regra do painel); quando o fato não aconteceu (CLAUDE.md, 9) |
| **Quantidade** | 2 a 5 por dia; máximo 7. Dia vazio é permitido |
| **Primeiro Story do dia** | O que mais perde gente (saída 23,8% no 1º). Abrir com o gancho do dia, sem "oi, pessoal" |
| **Enquete** | 2 opções reais, ambas defensáveis; mostrar o resultado depois (Story de fechamento). Baixa fricção: usar no começo do dia |
| **Quiz** | Só com resposta verificável no acervo. Resposta certa marcada |
| **Slider** | Para palpite numérico; nunca revelar o número real antes do Reel |
| **Caixa de perguntas** | 1 por semana; Plano B do painel (menos de 3 perguntas reais: usar enquete). Responder em vídeo curto |
| **Curiosidade** | Prometer só o que o Reel entrega; o número real vem do registro, não de estimativa |
| **Stories ↔ Reels** | Pré-Reel cria a pergunta; Reel responde; pós-Reel mostra o resultado do palpite |
| **Estimular DM** | Responder a quem respondeu; "chegou perto" ou "passou longe"; pedir permissão para mostrar nome |
| **Evitar queda de retenção** | Máx. 1 sticker de alta fricção por dia; 1 ideia por Story; texto até 3 linhas; sem sequência acima de 7 |
| **Repetição** | Nunca 2 Stories seguidos da mesma atração; nunca o Reel inteiro como Story |
| **Casal** | Marina pode aparecer de vez em quando, quando está de fato na cena, sem frequência fixa (decisão do Diego, 05/10/2026). O foco do perfil é Diego (CLAUDE.md, 2). Não há "Story de casal" como pilar |
| **Visual** | Só componentes do DS V2.1: placa P (50%), Placar mini, selo `AO VIVO DA VIAGEM`, etiqueta de série, legenda Narrativa em vidro, enquete "vale ou pula?". Zona segura: topo 256, base 320, laterais 72 (DS V2, 5.6). Capas de destaque pelo DS (círculo amarelo com IATA) |
| **Análise** | Taxas da seção 6; ler nas semanas 3, 8 e 13; registrar em Aprendizados |

## 10. Sistema de testes

Regras: uma variável por vez; comparar dias parecidos (mesmo tipo de Reel); alternar os braços para não confundir com o dia da semana; não rodar durante a viagem (diário não é comparável). Com audiência pequena, o resultado é **direção**, não prova.

| # | Teste | Hipótese | Braços | Métrica | Duração | Critério de sucesso | Janela sugerida |
|---|---|---|---|---|---|---|---|
| T1 | **Quantidade** | 3 a 4 Stories seguram mais que 6 a 7 | A: 3 a 4 · B: 6 a 7 (não testo 8 a 10: os estudos indicam queda) | Taxa de conclusão do dia | 8 dias por braço | B só vence se a conclusão for ao menos 5 pontos maior; senão fica A | Semanas 2 e 3 |
| T2 | **CTA** | Enquete (baixa fricção) tem taxa de resposta maior que caixa de perguntas | A: enquete · B: caixa | Taxa de resposta | 8 dias por braço (alternando) | Vence quem tiver taxa de resposta mediana ao menos 30% maior e ganhar em 6 de 8 pares; empate = enquete | Semanas 4 e 5 |
| T3 | **Formato** | Texto + vídeo (legenda Narrativa) tem menos saída que Diego falando | A: Diego falando · B: texto + vídeo | Taxa de saída do 1º Story | 8 dias por braço | Menor saída mediana em 6 de 8 pares | Semanas 6 e 7 |
| T4 | **Storytelling** | História curta (2 a 3 partes) conclui mais que sequência longa (5 a 7) | A: curta · B: longa | Conclusão da sequência e respostas ao último Story | 6 sequências por braço | Maior conclusão com respostas iguais ou maiores | Semanas 8 e 9 |
| T5 | **Horário** | O horário em que mais seguidores veem Stories muda o alcance | Manhã · tarde · noite | Alcance do 1º Story ÷ seguidores | 7 dias por faixa | Faixa com maior alcance mediano; confirmar no Insights > Público | Semanas 10 a 12 |

**Mudança em relação ao pedido:** o braço "6 a 10 Stories" do T1 vira "6 a 7". Os dois estudos de mercado encontrados indicam queda de retenção acima de 7; testar 8 a 10 gastaria dias de audiência pequena num cenário que o dado já desaconselha. Se A vencer com folga, o teto cai para 5.

## 11. Fontes e referências

Grau de confiança: **Oficial** (Meta/Instagram), **Reportado** (jornalismo que cita fala oficial), **Mercado** (estudo ou blog; trato como estimativa, CLAUDE.md, 4).

| Fonte | Link | Data | Grau | Principal aprendizado |
|---|---|---|---|---|
| Instagram, *Instagram Ranking Explained* | https://about.instagram.com/blog/announcements/instagram-ranking-explained | 31/05/2023 | **Oficial** | Stories são ranqueados por histórico de visualização, histórico de engajamento (curtida, DM) e proximidade; a Meta prevê chance de tocar, responder ou avançar. Lido na página |
| Social Media Today, *Instagram Shares Notes on Stories Ranking* | https://www.socialmediatoday.com/news/instagram-stories-ranking-factors-2025/738541/ | 28/01/2025 | **Reportado** (Mosseri) | Sinais: toque, curtida, resposta por DM. Stories feitos para conectar com amigos; Feed alcança mais gente. Lido na página |
| Buffer, *How the Instagram Algorithm Works* | https://buffer.com/resources/instagram-algorithms/ | 24/03/2026 | **Reportado/Mercado** | Repete os sinais de Stories; "Stories não são o melhor caminho para alcançar gente nova — Mosseri confirmou"; envios por DM pesam muito para Reels. Lido na página; a atribuição a Mosseri não é datada no texto |
| Dash Social, *Instagram Stories Benchmarks (2026)* | https://www.dashsocial.com/blog/every-instagram-stories-performance-benchmark-you-need-to-know | jan–jun/2025 (dados) | **Mercado** (2.000+ marcas com 1.000+ seguidores) | Conclusão 70%, saída 5%, 2 Stories por dia em média; contas pequenas (abaixo de 190 mil): conclusão 68,3%, saída 6,0%. Lido na página |
| Hootsuite, *Instagram Story Analytics* | https://blog.hootsuite.com/instagram-stories-analytics/ | sem data legível | **Mercado** | Definição das métricas de alcance, navegação, respostas, visitas e seguidores. Lido na página; não traz benchmark |
| Metricool, *Instagram Stories Metrics* | https://metricool.com/instagram-stories-metrics/ | sem data legível | **Mercado** | Mesmas definições; recomenda lotes pequenos e espaçados. Lido na página; "enquetes e quizzes elevam engajamento em mais de 50%" sem fonte, **não usei** |
| Hootsuite, *How to get more Instagram followers* | https://blog.hootsuite.com/get-more-instagram-followers/ | 2026 | **Mercado** | Stories têm baixo alcance entre não seguidores e servem para nutrir; Reels trazem seguidores. **Lido só no resumo da busca** |
| Buffer, estudo de 9,6 mi de posts | https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/ | atualizado em 2026 | **Mercado** | 1 a 7 Stories por dia; queda possível depois do 5º. **Lido só no resumo da busca** |
| Socialinsider, *2025 Instagram Stories Benchmarks* | https://www.socialinsider.io/social-media-benchmarks/instagram-stories-benchmarks | jan–mai/2025 (dados) | **Mercado** (161.180 Stories) | Saída por posição: 23,8% no 1º, 20,5% no 2º, 18,5% no 3º, 13,3% no 9º; alcance sobe com o tamanho da sequência. **Lido só no resumo da busca** |
| Later (poll 15–25% de resposta) e Sprout Social (contagem + link +35% de cliques) | citados por resumos de busca | sem data | **Mercado, não verificado** | Não usei nenhum número deles nas regras |

**Conflitos e lacunas nas fontes:**
- Nenhum dado de mercado cobre conta com menos de 1.000 seguidores.
- A tese "enviar por DM pesa 3 a 5 vezes mais que curtida" (sinais citados em resumos da busca como sendo de Mosseri, jan/2025) vale para Reels e Feed, não para a bandeja de Stories. Não usei para Stories.
- Hootsuite e Metricool não dão fórmula de conclusão; a fórmula da seção 6 é minha.

## 12. Lacunas e decisões para o Diego

| # | Tema | Situação | Recomendação |
|---|---|---|---|
| S1 | **Marina nos Stories** | **Resolvido (05/10/2026):** Marina pode aparecer de vez em quando, sem frequência fixa e sem virar pilar. O foco continua sendo o Diego (CLAUDE.md, 2) | Nada a mudar. As ideias "casal e personalidade" entram quando ela está na cena |
| S2 | **Template de Stories no DS** | O DS V2 (5.6) define zona segura, placa P, Placar mini, selo e capas de destaque, mas não define posição fixa de sticker nem modelo de Story pós-Reel (`SAIU AGORA / ROMA` está descrito só em texto) | Registrar a lacuna; não criei valor novo. Se quiser, o Diego aprova um modelo de Story pós-Reel pela governança do DS |
| S3 | **Compartilhar Reel em Story** | O painel dizia "republique o Reel do dia". Mudei para "compartilhe com 1 frase que não está no vídeo" para evitar repetir o Reel | Aprovar ou voltar ao texto original |
| S4 | **Custo de produção** | O plano não exige gravar nada só para Stories: usa edição, planejamento, acervo e a viagem | Manter assim até a Leitura 1 |
| S5 | **Conta com poucos seguidores** | Nos primeiros dias o público de Stories é amigos e família | Não interpretar taxa de resposta antes de 100 seguidores; usar contagem de DMs |
