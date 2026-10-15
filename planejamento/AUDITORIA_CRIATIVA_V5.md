# Auditoria criativa do calendário · V5

**Data:** 15/10/2026 · **Período:** 15/10/2026 a 28/02/2027 (20 semanas) · **Base:** V4 enviada pelo Diego em 15/10 (`versoes/planejamento-primeiro-dia-v4-cadencia-4-reels.html`, preservada sem alteração) · **Resultado:** `planejamento-primeiro-dia-v5.html`

| Entrega | Arquivo |
|---|---|
| A. Calendário interativo V5 | `planejamento-primeiro-dia-v5.html` |
| B. Esta auditoria | `AUDITORIA_CRIATIVA_V5.md` |
| C. Banco de ideias | `BANCO_DE_IDEIAS_V5.md` |
| D. Auditorias em CSV | `v5/auditoria-semanal-reels.csv`, `v5/auditoria-cidades.csv`, `v5/auditoria-paises.csv`, `v5/mapa-pilares-formato.csv`, `v5/pendencias.csv`, `v5/decisoes-v4-v5.csv` |
| E. Changelog | `CHANGELOG_V5.md` |
| Dados e scripts | `v5/eventos_v5.json`; `scripts/` (grade, peças, auditoria e montagem: `python3 scripts/montar_v5.py`, rodando de dentro de `planejamento/`) |

O caminho sugerido no prompt (`docs/auditoria-criativa-calendario-v5.md`) foi adaptado: `docs/` guarda só documentos de referência (CLAUDE.md, seções 11 e 12), e esta auditoria é do planejamento.

---

## Atualização de 15/10/2026 (respostas do Diego)

- **Ordem dos vlogs confirmada:** Amsterdam 24/10, Bruxelas 07/11, Bruges 21/11, Paris 05/12, Disney 19/12, Madrid 02/01, Lisboa 16/01. 30/01, 13/02 e 27/02 continuam sem destino. A ordem é diferente da do painel de 05/10 usada como "provável" abaixo; a grade foi refeita: os 5 Reels "Primeiro dia em X" e 4 carrosséis de roteiro foram trocados de data para cair na semana do vlog da cidade, e 9 Reels mudaram de dia para manter as regras. Resultado: 0 violações de cidade e de país; 6 transições de país pendentes (só as dos 3 vlogs sem destino).
- **Familiares nos vídeos da Itália:** liberados.
- **Dados de custos:** o Diego envia na montagem de cada peça. As peças de custo continuam como "Aguardando dados de custos do Diego".
- Itens 1, 5 e 6 da seção 11 resolvidos. O texto das seções 1 a 10 descreve a primeira montagem; os números atuais estão no painel e nos CSVs.

## 1. Resumo

- **80 Reels de Instagram** em 20 semanas: 4 por semana, com Reel em **toda quinta e todo domingo**. Mais 19 carrosséis, 7 fotos únicas, 39 sequências de Stories e os 10 vídeos longos nas datas fixas.
- **0 violações** de cidade (no máximo 2 aparições por semana, nunca em dias seguidos) e **0 de país** (peças seguidas de países diferentes), tanto no cenário confirmado quanto no **cenário provável** dos vlogs (ordem do painel original do Diego, 05/10/2026). No cenário provável, a V4 tinha 5 violações.
- **Os 80 Reels citam o arquivo do acervo** (com data e hora do arquivo; em Barcelona, a minutagem do vlog), ou dizem que precisam de gravação nova ou de dados do Diego. Na V4, **0 de 158** peças citavam arquivo.
- **129 de 158 peças da V4 foram substituídas** por ideias diferentes; 10 vídeos longos mantidos; 7 IDs mantidos com a peça reformulada, movida ou com formato novo. Relação completa em `v5/decisoes-v4-v5.csv` e na aba "Mudanças V4 → V5" do painel.

## 2. Fontes lidas

| Fonte | Situação |
|---|---|
| V4 (HTML enviado em 15/10) | Lida inteira: 158 eventos extraídos e auditados por script |
| `auditoria-semanal-reels-primeiro-dia-v4.csv` | **Não estava disponível** (não veio com o HTML nem existe no repositório). A auditoria foi refeita a partir dos eventos |
| V3 e versões anteriores do painel, revisão v5 antiga, banco de ideias v5, inventários, decupagens de Madrid, Disney e Paris, oportunidades de custo | No histórico do git (commit `77585d3`, removidos do branch em 15/10 a pedido do Diego). Lidos para recuperar decisões e material verificado |
| `acervo/` (8 cidades + Itália, 1.946 vídeos) | Linhas do tempo, transcrições e cortes de custo lidos. É a base das ideias |
| Referência de conteúdo Instagram, DS V2 2.2.0 e tokens | Lidos (estrutura do Reel, hooks, níveis A/B, componentes, checklist 7.3) |
| Calendário oficial do canal no YouTube | **Não encontrado como arquivo próprio.** A única fonte com os destinos é o painel original do Diego (05/10/2026, commit `77585d3`): Barcelona 10/10, Amsterdam 24/10, Paris 07/11, Disney 21/11, Madrid 05/12, Bruxelas 19/12, Bruges 02/01, Lisboa 16/01. A V5 mantém esses destinos como **prováveis** (não confirmados) e audita os dois cenários |
| Registros de custos | Não lidos nesta revisão (planilha "Custos de Viagens - Europa" no Drive). Nenhum valor foi usado |

## 3. Diagnóstico da V4

**O que a V4 resolveu bem e foi mantido:** a meta de 4 Reels por semana com quinta e domingo como âncoras; terça 19h, quarta 18h, quinta 9h e domingo 20h30 como hipótese de horário (a fonte Buffer foi reconferida, seção 6); carrossel na segunda; datas fixas dos vídeos longos; o Reel de 15/10 em Lisboa para alternar o país depois de Barcelona; adaptação para Shorts e TikTok sem somar na meta; custos sem número inventado; Amsterdam em 24/10 com trailer 4 dias antes.

**Problemas encontrados (com número):**

| # | Problema | Evidência |
|---|---|---|
| 1 | **Nenhuma peça ligada a material real.** | 0 de 158 eventos citam arquivo, embora o acervo tenha 1.946 vídeos catalogados com hora e fala |
| 2 | **Modelos repetidos trocando só a cidade.** | 20 Stories "Quiz visual", 19 "O que você salvaria deste destino?", e cerca de 60 Reels em 20 modelos de título ("A cidade em 3 cenas", "3 motivos visuais para lembrar de X", "X sem pressa: um respiro no feed", "Você enviaria essa vista para quem?" ×4, "A atmosfera de X em 15 segundos" ×3, "Expectativa x realidade — somente com cenas que comprovem" ×3…). Um modelo que serve para qualquer cidade não diz nada de nenhuma |
| 3 | **Reels gerais de conselho abstrato.** | 22 Reels "Geral" com ganchos como "Seu roteiro não precisa ter tudo: precisa fazer sentido" e "Deixar tempo livre também é planejar", sem experiência, fonte nem prova. Dois se repetem ("Roteiro inteligente" em 16/10 e 17/02; "Documentos antes de embarcar" em 17/10 e 24/02) |
| 4 | **Duplicatas.** | Checklist de documentos 3 vezes (09/11, 14/12, 08/02); "O que conferir antes de montar um roteiro para Disneyland Paris" 2 vezes (04/01 e 26/02); "Quanto gastei em um dia em Paris?" 2 vezes (16/11 e 11/01), mais um Reel de custo de Paris |
| 5 | **Itália ausente.** | 214 vídeos da Itália no acervo (Réveillon em Veneza, Natal em Roma) e nenhuma peça, nem em 24/12 e 31/12 |
| 6 | **Stories com cidade contavam como aparição** e limitavam o calendário sem dar nada em troca | 39 Stories com cidade |
| 7 | **Risco escondido nos vlogs.** | Com os destinos prováveis, a V4 teria Bruges em 02/01 e 03/01, Lisboa em 15/01 e 16/01, e 3 sequências de mesmo país |
| 8 | **IDs desalinhados.** | 47 IDs com cidade ou data diferente do evento (ex.: `IG-20261128-REE-barcelona-039` é Amsterdam em 29/11). A V5 manteve os IDs que continuaram a mesma peça e deu ID novo às peças novas |
| 9 | **Sem Design System na peça.** | Nenhum briefing dizia Nível A/B, Placa, Carimbo, Ticket ou Bilhete |

A V4 passava nas próprias regras (20 de 20 semanas com 4 Reels, 0 violações no cenário confirmado). O problema não era a grade: era o conteúdo.

## 4. O que foi mantido, reformulado, substituído ou movido

| Decisão | Peças da V4 |
|---|---:|
| Manter (vídeos longos, datas fixas) | 10 |
| Reformular, mesmo ID (trailer de Amsterdam, Reel da série de Amsterdam, custo de Amsterdam) | 3 |
| Mover de data, mesmo ID (custo de Paris 26/11 → 29/11; "Custo planejado sem chute" 21/10 → 18/02, agora "A planilha que a gente usa"; checklist de documentos 09/11 → 26/10) | 3 |
| Mudar de formato, mesmo ID (custo de Lisboa: Reel de 31/12 → carrossel de 15/02) | 1 |
| Substituir por ideia nova no mesmo horário | 134 |
| Substituir (horário ocupado por peça movida) | 4 |
| Remover (horário liberado) | 3 |

Os motivos de cada uma estão no CSV. A troca mais importante: **15/10 continua em Lisboa** (alternância com Barcelona), mas o "POV: Lisboa faz você querer explorar sem roteiro" virou **"Pedimos 'peixinhos' em Lisboa. Não era peixe."** (IMG_4246 e IMG_4248, 22/03 21h40), uma peça curta, engraçada, útil e com prova, que dá para editar hoje. Plano B, se o áudio não confirmar a fala: "Fim de março em Lisboa: 17 graus e sol às 9h30" (IMG_4395).

## 5. Territórios criativos novos

Todos saem do acervo, não de suposição:

1. **"Primeiro dia em X" com o relógio** (série principal, DS V2 Nível A). Cada cidade tem a hora real de chegada e de cada parada. 8 Reels de série no período (Amsterdam, Paris, Disney, Madrid, Barcelona, Bruxelas, Bruges, Lisboa), cada um na semana seguinte ao vlog provável da cidade. O Placar está previsto e espera os dados de custos; sem eles, a peça sai em Nível B com a hora na legenda.
2. **"Nota de soteropolitano"** (série editorial nova). Vereditos reais comparando com o Brasil e com Salvador: churros ("o do Brasil ainda ganha"), hambúrguer ("os de Salvador dão um banho"), o chuveirinho de Lisboa, "o Brasil não sai da gente". É identidade pessoal (CLAUDE.md, 2) e envio fácil. Usa só o Bilhete; **o rótulo na tela depende de aprovação do Diego** (governança do DS V2).
3. **O que estava fechado.** 8 portas fechadas reais (Luxemburgo às 18h53, Ratatouille em reforma, piscina vazia, roseiral sem rosas, Debod sem água, jogo adiado, Vittoriano em obra, Santa Justa). Vira Reel autoral (GER-fechado) e carrossel de consulta (CAR-confira-antes). É a promessa da marca ("o que evitar") com humor honesto.
4. **Vale ou pula** (série oficial do DS V2) com vereditos ditos no dia: Heineken Experience ("vale para quem não bebe também"), Castelo de São Jorge ("depende": não entraram por tempo), Palácio Real por fora, La Boqueria.
5. **Espelhos de marca:** "8 cidades, 8 'chegamos'" (21/10) e "8 cidades, 8 despedidas" (21/02) abrem e fecham o ciclo com o bordão.
6. **Narrativa no mesmo dia:** a aposta da Disney ("a Marina vai chorar no show", 09h47 → resposta às 22h19).
7. **Rituais de viagem:** a tradição da Marina de provar o McDonald's exclusivo de cada país; voltar na mesma barraca de batata 8 minutos depois.
8. **Datas reais:** Natal em Roma (gravado num 25/12, publicado em 24/12), Réveillon em Veneza (fogos às 00h11, publicado em 31/12), "todo ano tem um primeiro dia" nos Stories de 01/01.

## 6. Pesquisa externa (consulta em 15/10/2026)

| Tipo | O que diz | Fonte | Uso na V5 |
|---|---|---|---|
| **Oficial (Meta), por fonte secundária** | Tempo assistido, curtidas por alcance e envios por alcance são os sinais que o Mosseri confirmou (jan/2025). A página oficial não abriu nesta sessão; a confirmação vem de várias análises que citam o mesmo pronunciamento | [Dataslayer](https://dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers), [SocialPilot](https://www.socialpilot.co/?p=563048) | Cada Reel tem "mecanismo de retenção" e "mecanismo de envio" no briefing |
| **Oficial (Meta), por imprensa** | Conteúdo original é favorecido; agregadores que repostam 10+ vezes em 30 dias saem das recomendações (abr/2024) | [Gigazine](https://www.gigazine.net/gsc_news/en/20240502-instagram-updated-algorithm-prioritizes-original-content), [Tubefilter](https://www.tubefilter.com/2022/04/21/instagram-adam-mosseri-algorithm-change-original-content/) | Todo material é do acervo; nenhum repost |
| **Oficial (Meta), por fonte secundária** | Trial Reels podem ser agendados desde fev/2026; vão primeiro para não seguidores. Números de desempenho são da própria Meta | [Publer](https://publer.com/blog/instagram-trial-reels-guide/), [Tagembed](https://tagembed.com/blog/instagram-updates/) | Peças com nota 5–7 na matriz ficam marcadas como teste (Trial Reel) |
| **Estudo agregado** | Buffer, 9,6 milhões de posts (jan/2024 a dez/2025), publicado em 23/09/2026, horários normalizados para o fuso local: quinta 9h, quarta 12h e 18h, terça 19h; domingo 21h–20h é a melhor faixa do fim de semana (moderada); sexta e sábado são os mais fracos | [Buffer](https://buffer.com/resources/when-is-the-best-time-to-post-on-instagram/) (página conferida) | Confirma a cadência da V4 como hipótese inicial |
| **Estudo agregado** | Socialinsider, 35 milhões de posts de 447.613 páginas (2025), publicado em 20/02/2026: carrossel 0,55% de engajamento, Reels 0,52%, imagem 0,37%; carrossel lidera salvamentos; métrica por seguidores (não por alcance) | [Socialinsider](https://www.socialinsider.io/blog/instagram-benchmarks/) (página conferida) | Mantém 1 carrossel por semana com função de consulta (salvamento) |
| **Tendência** | Guias de 2026 citam conteúdo localizado (referências e humor locais) e o "antes e depois" como formatos de identificação; nenhuma fonte trouxe dado de criadores de viagem brasileiros | [Taggbox](https://taggbox.com/pt/blog/instagram-trends/), [Rafael Terra](https://rafaelterra.com.br/como-viralizar-reels-em-2026/) (blogs com interesse comercial) | Apoio fraco para "Nota de soteropolitano" e para o castelo 14h35 × 19h11. Tratados como hipótese |
| **Documentos (volátil)** | O EES (registro biométrico na fronteira Schengen) está em operação desde 12/10/2025 segundo fonte secundária; o ETIAS não tem data oficial confirmada (há relato de adiamento para 2027). O site oficial não respondeu nesta sessão | [Navan](https://navan.com/blog/when-does-etias-go-into-effect), [Afar](https://www.afar.com/magazine/europes-etias-travel-entry-requirement-delayed-until-2026) | GER-ees e GER-imigracao ficam como "Validar fontes oficiais na produção" |

**Hipóteses a testar no perfil** (registrar no Registro de Aprendizados da referência, seção 10): humor de identificação brasileira gera mais envios que dica pura; a série com relógio retém mais que a montagem de atmosfera; CTA de comentário com dúvida real (MAD-show, BRU-doce) gera mais comentários que pergunta genérica (GER-qual-primeiro). Uma variável por vez, em blocos de 10 Reels.

## 7. Mistura escolhida

| Grupo (prompt, seção 6) | Reels | Peças do feed |
|---|---:|---:|
| A. Autoral e inesperada | 16 | 16 |
| B. Clichê estratégico (POV, expectativa × realidade, comparação, ranking, vale ou pula, pergunta) | 12 | 14 |
| C. Utilidade e serviço | 18 | 32 |
| D. Storytelling e marca | 14 | 15 |
| E. Desejo e descoberta | 17 | 25 |
| F. Custos (aguardando dados) | 3 | 4 |

**Clichês usados de propósito, e o que os torna próprios:** POV (a saída do metrô de frente para o Arco do Triunfo às 12h37), expectativa × realidade (Debod sem água, Vondelpark em março: contraste dito no vídeo, sem foto de terceiros), comparação (dois pastéis de nata na mesma manhã, 3 batatas em 3 cidades), ranking (notas ditas no dia, sem nota inventada), pergunta de comentário (o show que ninguém entendeu), "vale ou pula" (vereditos reais).

**Cidades nos Reels:** Amsterdam 11 (+2 comparações), Lisboa 9, Madrid 9, Paris 9, Disney 6, Bruges 6 (+2), Bruxelas 5 (+1), Barcelona 4 (+1), Itália 10 (Veneza 4, Roma 3, Florença 2, Milão 1), panoramas e gerais 9. Amsterdam tem mais peças porque tem o lançamento e o maior acervo (454 vídeos). Barcelona tem menos porque o vlog já saiu e o master tem trilha no B-roll.

## 8. Critérios de seleção e pontuação

Matriz da referência de conteúdo (seção 5), sem mudança: enviabilidade, força do gancho, aderência ao nicho, originalidade e esforço inverso, de 0 a 2. A V5 acrescenta no briefing (sem mudar a matriz) os critérios do prompt: especificidade, prova, retenção, envio, salvamento, clareza da promessa, viabilidade e coerência de marca, que aparecem nos campos "promessa", "payoff", "mecanismo de retenção", "envio ou salvamento", "arquivos" e "riscos".

| Nota | Reels | Decisão |
|---:|---:|---|
| 10 | 9 | Reel normal |
| 9 | 25 | Reel normal |
| 8 | 38 | Reel normal |
| 7 | 7 | Teste (Trial Reel): GER-imigracao, GER-ees, BCN-park-guell, BCN-boqueria, BRG-minnewater, GER-planilha, LIS-17-graus |
| 6 | 1 | Teste: GER-qual-primeiro (clichê de plataforma, originalidade 0) |

Nenhuma peça ficou abaixo de 5. As notas são da revisão; o painel deixa o Diego reavaliar. Pontuação é ferramenta de escolha, não previsão de alcance.

## 9. Estrutura do calendário

- **Semana-padrão:** segunda carrossel (18h30) e Stories (12h30); terça Reel 19h; quarta Reel 18h; quinta Reel 9h; sexta Stories e, em 7 semanas, uma foto única; sábado vídeo longo a cada 14 dias; domingo Reel 20h30.
- **Stories:** todos gerais (sem cidade em destaque), ligados às peças da semana: pesquisa de pauta, teste A/B de gancho com quem já segue, quiz que leva ao Reel, bastidor. Não contam como Reel nem como aparição de cidade.
- **Vlogs:** datas da V4. Peças da série "Primeiro dia em X" saem na quarta da semana seguinte ao vlog provável da cidade, para funcionar sozinhas mesmo que o destino mude.
- **Lançamento de Amsterdam:** 20/10 curiosidade completa com CTA para o sábado (função de trailer, ID mantido), 24/10 vlog, 28/10 Reel da série. O teaser de 26/10 da V4 saiu (repetia a função do trailer e da série).

## 10. Limitações e dependências

1. **Ninguém viu nem ouviu os trechos.** O acervo tem transcrição automática e hora do arquivo. Todo Reel diz o arquivo e a hora, mas o trecho exato está como "verificar no acervo" (80 peças em `v5/pendencias.csv`). Nenhum timestamp foi inventado: quando há segundos, eles vêm da transcrição ou da lista de cortes de custo.
2. **Falas citadas** estão entre aspas como saíram da transcrição e precisam ser conferidas no áudio antes de virar texto na tela.
3. **Custos:** 4 peças de custo e o Placar das 8 peças de série esperam os dados do Diego. Sem dados até 7 dias antes, a peça é trocada por uma do banco.
4. **Fatos voláteis** (horário de jardim, brilho da Torre, regra de ingresso, EES, documentos): 13 peças com "Validar fontes oficiais na produção".
5. **Pessoas no vídeo:** a família do Diego aparece em clipes da Itália; terceiros em Roma e no trem. Usar planos sem eles ou pedir a autorização do Diego.
6. **Destinos dos vlogs** depois de Amsterdam: prováveis, não confirmados. 30/01, 13/02 e 27/02 sem destino. A auditoria de país marca 18 transições como "pendente" até a confirmação.
7. **Status de publicação:** nada foi marcado como publicado. A última publicação considerada é Barcelona (informação da V4). Os Reels de 11/10 (camisa do Bahia) e 13/10 (água em Barcelona) constam como publicados no painel antigo; a V5 não repete esses temas.
8. **Fontes do DS V2** continuam fora do repositório (CLAUDE.md, 14.1); isso afeta a produção, não o calendário.

## 11. Decisões que dependem do Diego

| # | Decisão | O que a V5 faz até lá |
|---|---|---|
| 1 | ~~Confirmar os destinos dos vlogs~~ | **Resolvido em 15/10:** ordem confirmada; faltam 30/01, 13/02 e 27/02 |
| 2 | Aprovar a série editorial "Nota de soteropolitano" (nome e rótulo) | As peças usam só o Bilhete, sem rótulo novo na tela |
| 3 | Aprovar a variante de Placa "PRIMEIRA NOITE EM / LISBOA" | Sem aprovação, usa "PRIMEIRO DIA EM / LISBOA" |
| 4 | Vereditos e opiniões (La Boqueria, Palácio Real, quantos dias por cidade, por onde começar, a "melhor primeira mordida", as 4 regras do método) | 9 peças com "Aguardando decisão do Diego" |
| 5 | ~~Familiares nos clipes da Itália~~ | **Resolvido em 15/10:** pode mostrar |
| 6 | Enviar os dados de custos (Paris, Amsterdam, Lisboa e o Placar das séries) | "Aguardando dados de custos do Diego" |
| 7 | Gravações novas curtas (talking head do método, da imigração, do EES; tela da planilha) | Marcadas como material futuro; não travam o resto |
| 8 | Itália em Reel | O prompt de 15/10 libera vídeo da Itália em Reel depois de verificado (resolve a pendência D1 para vídeo); fotos italianas só em carrossel |
