# Estudo: vídeo longo no YouTube (base da DS 2.2.0)

**Data:** 06/10/2026 · **Pedido do Diego:** levar os componentes dos Reels (perrengue, surpreende, vale/pula, valores, bilhetes) para o vídeo do YouTube, com a estrutura que ele já usa, e pesquisar o que ajuda e o que atrapalha. **Resultado:** seção 5.4 da `design-system-primeiro-dia-v2.md` (versão 2.2.0, proposta) e tokens `layout.yt` / `component.yt-*`.

Este estudo não cria regra. As regras ficam no DS depois da aprovação do Diego.

---

## 1. O que o YouTube mede (com fonte e data)

| Sinal | O que diz | Status | Fonte (consultada em 06/10/2026) |
|---|---|---|---|
| Recomendação | Usa histórico de visualização, curtidas, descurtidas, inscrições e **pesquisas de satisfação** ("feedback, including from satisfaction surveys") | **Confirmado pelo YouTube** | [How YouTube Works: Recommendations](https://www.youtube.com/howyoutubeworks/product-features/recommendations/) |
| Retenção: "Intro" | O Studio mede **quantos % ainda assistem depois dos primeiros 30 s**; mostra quedas (abandono), picos (reassistir/compartilhar) e trechos planos | **Confirmado pelo YouTube** | [Ajuda do YouTube: momentos-chave da retenção](https://support.google.com/youtube/answer/9314415) |
| Teste de thumbnail e título | O "Testar e comparar" (A/B) escolhe o vencedor por **participação no tempo de exibição** (watch time share), não por CTR | **Confirmado pelo YouTube** | [Ajuda: Test & compare](https://support.google.com/youtube/answer/13861714) |
| Capítulos | 1º marcador em 00:00, **no mínimo 3**, cada um com **≥ 10 s** | **Confirmado pelo YouTube** | [Ajuda: capítulos](https://support.google.com/youtube/answer/9884579) |
| Tela final | Só nos **últimos 5–20 s**; vídeo com ≥ 25 s; até **4 elementos** em 16:9 | **Confirmado pelo YouTube** | [Ajuda: telas finais](https://support.google.com/youtube/answer/6388789) |
| Volume | Normaliza para baixo o que passa de ≈ −14 LUFS (só abaixa, não sobe) | **Estimativa de mercado** (medido em "Estatísticas para nerds"; o YouTube não publica o número) | [Production Advice](https://productionadvice.co.uk/stats-for-nerds/) |
| Satisfação acima de tempo bruto | "Satisfação pesa mais que tempo de exibição" | **Estimativa de mercado** (atribuído ao Creator Insider/Rene Ritchie; não achei o texto oficial) | [SocialPilot, ago/2026](https://www.socialpilot.co/youtube-marketing/youtube-algorithm) |
| Intro curta | Cortar a intro para ~3 s levou a retenção em 30 s de 52% para 78% (caso relatado) | **Caso isolado, não verificável** | [Subscribr](https://subscribr.ai/youtube-strategy/youtube-analytics-improve-video-hooks-intros) |
| 1º minuto | "O primeiro minuto é o mais importante de cada vídeo" (é onde mais gente sai); depois, minutos 3–6 | **Prática de produtora** (documento interno da MrBeast, vazado em 2024) | [Alexander Jarvis](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/) |
| Legenda automática | Erra muito com barulho e música (60–78% de acerto vs. 94–96% em fala limpa) | **Estimativa de mercado** | [Blitzcut, 2026](https://blitzcutai.com/blog/caption-accuracy-comparison-2026) |
| Legenda profissional (PT-BR) | **42 caracteres por linha**, **17 car/s**, **2 linhas**, evento de **5/6 s a 7 s**, centralizada | **Padrão da Netflix** (referência de mercado, não regra do YouTube) | [Netflix PT-BR](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide) · [Netflix geral](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617) |
| Excesso de edição | Transição, *zoom* e efeito sonoro em todo corte cansam; abrir com paisagem impessoal afasta; rosto cedo aproxima | **Opinião de mercado** | [Splice, jun/2026](https://spliceapp.com/blog/common-mistakes-in-travel-vlog-intros-and-how-to-avoid-them/) |

**Leitura:** o YouTube não premia "viralizar" por um truque. Ele premia **clique que cumpre a promessa** (thumbnail/título → conteúdo) e **satisfação** (a pessoa acha que valeu o tempo). Para um canal de "custo real e primeiro dia", isso joga a favor: o recibo, o veredito e o perrengue verdadeiro são exatamente o que faz alguém achar que o vídeo valeu.

---

## 2. A estrutura que o Diego já usa, analisada

| # | Trecho | O que ajuda | Risco | Ajuste proposto |
|---|---|---|---|---|
| 1 | **Fundo preto + digitação** `Barcelona, Espanha — 9 de março de 2026` | Assinatura própria, situa lugar e data (prova do "real") | É uma intro antes do conteúdo: a referência de conteúdo (9) proíbe "introduções longas, logos ou vinhetas no início" e a pesquisa mostra queda forte nos primeiros 30 s | Manter, mas **≤ 3 s**, com o **som da primeira cena já entrando** por baixo (corte em J). Fundo Grafite Noite, letra Plex Mono (a "máquina de escrever" da marca). Nada de logo aqui |
| 2 | **Diego aparece** e diz quantos dias vai ficar | Rosto cedo = conexão; promessa clara | Se virar "oi, pessoal", perde o 1º minuto | Abrir já na frase útil ("4 dias em Barcelona, e eu vou te mostrar quanto custou cada um"). O número de dias vira **Destaque** (mini-placa) na legenda, sem placa extra |
| 3 | **Takes / melhores momentos** | É o *trailer*: mostra o que vem, segura até o fim | Montagem só de paisagem afasta | Incluir 1 perrengue e 1 surpresa (sem revelar o desfecho) e 1 preço → abre perguntas que o vídeo responde |
| 4 | **Nome "Primeiro Dia" sobre a montagem** | Construção de marca no pico de energia | Se for vinheta em tela preta, vira "logo no início" | **Título de Marca**: Placa `PRIMEIRO DIA →` com Chegada **sobre** os takes, 2,4 s, sai pela direita. Não é vinheta: o vídeo não para |
| 5 | **Legenda de lugar** ao lado | Contexto, busca, memória | Texto solto sem padrão | **Placa de Lugar** (lower third) em posição fixa |
| 6 | **Valor** na tela | É a promessa da marca | Valor só em euro, ou arredondado | **Etiqueta de valor** / **Recibo** com € e ≈ R$ e cotação datada |
| 7 | **Vale / não vale, perrengue, surpreendeu** | Emoção de alta ativação + utilidade | Usar demais tira o valor | Os mesmos objetos do Reel, com cota **por capítulo** |
| 8 | **Legenda em momentos de barulho** | Acessibilidade e retenção onde a fala some | Legenda queimada no vídeo todo cansa em vídeo longo | **Legenda de Fala** só nos trechos com barulho, fala estrangeira ou áudio ruim; no resto, legenda fechada (CC) enviada ao YouTube |
| 9 | **Fade-out, escuro, símbolo sobe** | Fechamento reconhecível | — | Encaixa direto na assinatura **Nascer** do 1º. Vira o **Encerramento** do YouTube, seguido da tela final escura |

---

## 3. O que observamos em outros canais (padrões de mercado)

Observação de formato, sem números de desempenho verificados.

| Padrão | Onde aparece | Usar? | Como no Primeiro Dia |
|---|---|---|---|
| Lugar e data datilografados na abertura | Muito comum em vlogs de viagem (estilo "diário") | **Sim** (já é do Diego) | Abertura Datilografada |
| *Cold open* com o melhor momento antes de tudo | Canais grandes de viagem e entretenimento | **Testar** | Variante B da abertura (seção 4) |
| Lower third com nome do lugar | Padrão de documentário e vlog | **Sim** | Placa de Lugar |
| Custo na tela e resumo de gastos no fim | Canais de "quanto custa" (ex.: Quanto Custa Viajar) | **Sim, é a nossa promessa** | Placar do Dia + Recibo do Dia + Recibo da Viagem |
| Mapa animado entre cidades/bairros | Vlogs de roteiro | **Sim, com o nosso mapa** | Mapa (já no DS) |
| Pacotes de *lower thirds* prontos, *glitch*, *zoom* com giro, *whoosh* em todo corte | Templates de editor | **Não** | Proibido no DS (4.4 e 4.5) |
| Legenda queimada palavra a palavra o vídeo inteiro | Shorts e Reels | **Não** no longo | Só nos trechos de barulho |

---

## 4. Ideias criativas propostas (entram como componentes ou testes)

1. **Recibo do Dia:** no fim de cada capítulo (dia), o recibo do dia é "impresso" com o total. Fecha o capítulo, cria um ponto de salvamento e um motivo para ver o próximo dia.
2. **Recibo da Viagem:** antes do encerramento, o recibo longo com o total da viagem por categoria. É o "pagamento" da promessa e o momento mais compartilhável.
3. **Pergunta aberta na abertura:** um Bilhete curto na montagem, por exemplo `no fim: vale ou pula?`, abre um ciclo que só fecha no veredito final. Mantém gente até o fim sem enganar.
4. **Placar zera a cada dia:** na troca de capítulo, o placar desliga, entra a placa `DIA 2` e ele religa em `+00:00 · € 0,00`. Marca a passagem do tempo com o próprio objeto da marca.
5. **Teste de abertura (1 variável):** A = estrutura atual (datilografia → Diego → montagem → título). B = montagem de 5–10 s primeiro → datilografia → Diego. Comparar a retenção em 30 s (Studio, "Intro") em blocos de vídeos iguais.

---

## 5. Efeitos: o que ajuda e o que atrapalha

| Ajuda | Por quê | Atrapalha | Por quê |
|---|---|---|---|
| Corte seco na maioria | Ritmo sem cansar | Transição em todo corte | Vira barulho; o DS já limita a 30% |
| Som ambiente real sob as transições | Prova do "real", imersão | *Whoosh* e efeito sonoro em toda palavra | Cansa; parece template |
| Objeto da marca no pico (carimbo, ticket) | Emoção de alta ativação | Objeto toda hora | Perde valor; cota por capítulo |
| Speed ramp em deslocamento | Encurta sem perder contexto | *Zoom punch-in* em toda fala | Cansa em vídeo longo |
| Freeze no perrengue e no preço | Dá tempo de ler e marca o momento | Aberração cromática, *glitch*, "teal & orange" | Contradiz o "real" (proibido no DS) |
| Trilha 8–10 dB abaixo da voz | A fala é o conteúdo | Trilha alta | Força a legenda e afasta |
| Legenda queimada só onde a fala some | Acessível sem poluir | Legenda queimada no vídeo todo | Duplica a CC do YouTube e cobre a imagem |
| Master −14 LUFS, pico ≤ −1 dBTP | Não perde volume na normalização | Master acima de −14 LUFS | O YouTube abaixa (estimativa de mercado) |

---

## 6. Decisões que dependem do Diego

| # | Decisão | Minha recomendação |
|---|---|---|
| D1 | Nome da versão: "REV 3" ou **2.2.0** | **2.2.0.** Pela governança do DS (7.4), componente novo é MINOR; "REV 3" seria MAJOR e quebraria o congelamento até abril/2027 (0.1). Nenhum ativo central muda |
| D2 | Abertura em tela preta | Manter, com ≤ 3 s, som da cena por baixo e sem logo. A tela é Grafite Noite (`#121317`), não preto puro (o preto não é token) |
| D3 | "Vale / não vale" | Manter o vocabulário do DS: **VALE / PULA / DEPENDE** (2.7). "Não vale" não entra para não criar dois nomes para a mesma coisa |
| D4 | "Notas" | Se for **nota de 0 a 10**, é componente novo (não existe no DS). Hoje "nota" = Bilhete (opinião na letra do Diego). Não criei a nota numérica |
| D5 | Teste de abertura A × B | Rodar depois de ter pelo menos 2 vídeos de cada |
| D6 | FPS 24 e módulo de seta 221 × 221 | Registrados na 2.2.0 a partir das respostas de 06/10/2026 ("24 fps" e "qual vc achar melhor") |
