# QA · Carrossel Transporte em Barcelona · REV1 (16/10/2026)

**Veredito:** **pronto para revisão do Diego**. Falta só a aprovação do nome da série e a confirmação de quanto foi pago no Hola (máquina ou online).

**Pedido do Diego (16/10/2026):** série de carrosséis sobre transporte, uma cidade por post (Barcelona primeiro; depois Roma, Madrid, Paris e Amsterdam). Cada post mostra quanto custa e como ir do aeroporto ao centro, quanto custam o bilhete unitário e os passes de 24, 48 e 72 h, e se o passe vale a pena. A ideia original de gancho era "você sabia desses custos?".

**Base:** DS V2.2 (1.3, 1.5, 2.1, 2.4, 2.6, 2.7, 5.1, 5.3, 7.3), referência de conteúdo (3.3, 3.4, 4, 6) e o carrossel de Roma REV1 (`carrosseis/roma-3-dias/rev1/`, commit `77585d3`), que serviu de modelo de layout.

## Como gerar

De dentro desta pasta: `node scripts/render.mjs` gera `out/01.jpg` a `out/09.jpg` a partir de `slides.html`. Variáveis opcionais: `PLAYWRIGHT_MODULE` (neste ambiente, `/opt/node22/lib/node_modules/playwright`) e `CHROMIUM`. O script também confere a largura da placa (≤ 872 px), a margem de 80, a Rota e as palavras por slide. `out/contato.jpg` é a folha de contato a 25% (teste de miniatura).

A foto da capa vai em `../fonte/capa.jpg` (fora do git): a foto da Casa Batlló enviada pelo Diego (`../fonte/casa_batllo_chat.jpg`), cortada em 3:4 pelo topo e redimensionada para 1080 × 1440.

`slides.html` usa o `pd-bundle.css` do DS e as fontes em `fonts/` (as mesmas do carrossel de Roma: Barlow, Barlow Condensed, IBM Plex Mono e Reenie Beanie, OFL 1.1).

## Estrutura (9 slides)

| # | Slide | Tipo (DS 5.3) | Objeto |
|---|---|---|---|
| 01 | Quanto custa andar em Barcelona? | Capa | Placa variante Hook (`?` no módulo), DS 2.1 e 5.1 |
| 02 | Sabia? O trem do aeroporto aceita a T-casual | Informação | Ticket "SABIA?" (DS 2.6, Curiosidade) + Etiqueta de valor |
| 03 | Do aeroporto ao centro | Informação | Quadro (DS 2.6, Ranking) |
| 04 | Qual pegar? | Informação | Pictogramas (DS 1.5) |
| 05 | Quanto custa andar | Custo | Recibo (DS 2.6) |
| 06 | A gente pagou a mais (história real) | Comparação | Dois recibos + ✓ de caneta |
| 07 | Quando o passe compensa | Informação | Quadro |
| 08 | Dica: T-casual não vale no metrô L9 | Dica | Bilhete + Etiqueta de valor |
| 09 | Do aeroporto ao centro por € 1,30 | Encerramento | Bilhete "da próxima vez: t-casual." + CTA `SALVA PRA VIAGEM →` + símbolo 1º |

## Gancho

- **Escolhido (capa):** "Quanto custa andar em Barcelona?" na Placa variante Hook (DS 5.1, tipo Pergunta). Tem 5 palavras, dentro do limite de 6 da capa (DS 5.3), e põe a cidade no maior texto da tela, o que ajuda a busca e o teste de miniatura.
- **O "você sabia?" virou o slide 02:** "Sabia? O trem do aeroporto aceita a T-casual: € 1,30". Usa o componente que o DS já prevê para curiosidade (Ticket "SABIA?") e entrega um número concreto, em vez de prometer "custos" de forma genérica. Se o Instagram mostrar o slide 2 para quem não deslizou, ele funciona sozinho.
- **Alternativas para teste (uma variável por vez, referência 8.3):** (A) Preço: placa `DO AEROPORTO AO CENTRO` / `€ 1,30` (mesmo padrão da capa de Roma, com preço na linha de destino); (B) Vale a pena: placa `VALE O PASSE EM` / `BARCELONA` / `?`.

## Matriz "vale a pena?" (referência, 5)

Enviabilidade 2 (dá para dizer para quem mandar: quem vai a Barcelona) · Gancho 1 · Nicho 2 · Originalidade 1 (tema comum; o ângulo próprio é a conta em € e R$ e o trem a € 1,30) · Esforço 2. **Total 8:** produzir e publicar.

## Fotos

| Slide | Foto | Data e hora |
|---|---|---|
| 01 | Casa Batlló ao entardecer, fachada inteira (enviada pelo Diego no chat, 16/10/2026) | sem EXIF (a imagem do chat chega sem metadados) |

**Escolha do Diego (16/10/2026):** a Casa Batlló. Corte 3:4 pelo topo (1717 × 2289 de 1717 × 2576): mantém o céu (onde ficam a etiqueta e o contador), o telhado de dragão e as varandas, e tira a multidão da base (rostos de desconhecidos). A placa cobre as janelas do primeiro andar. Coordenadas da capa: as da Casa Batlló na Wikipédia (41,39158° N · 2,16492° E), arredondadas para 4 casas.

**Desvio:** o DS (5.3) pede o Diego em primeiro plano na capa; esta não tem pessoa. A alternativa com o Diego e a Marina na Sagrada Família (IMG_1198, Drive `Barcelona/Youtube`, 11/03/2026 11:41) foi a REV anterior desta capa e fica registrada como opção para teste. A foto do chat tem 1717 px de largura: basta para 1080, mas o original do celular daria mais nitidez.

## Dados e fontes (conferidos em 16/10/2026)

| Dado | Valor | Fonte |
|---|---|---|
| Bilhete simples (metrô e ônibus TMB, zona 1) | € 2,90 | [TMB, tarifas 2026](https://www.tmb.cat/en/barcelona-fares-metro-bus/transport-ticket-fares), em vigor desde 15/01/2026 |
| T-casual (10 viagens, zona 1) | € 13,00 | TMB, idem |
| T-dia (24 h desde a 1ª validação) | € 12,00 | TMB, idem; regras em [TMB, T-dia](https://www.tmb.cat/en/barcelona-fares-metro-bus/t-dia): individual, inclui 1 ida e 1 volta no metrô do aeroporto |
| Bilhete Aeroport (metrô L9 Sud) | € 5,90 | TMB, tarifas 2026; [TMB, Airport ticket](https://www.tmb.cat/en/barcelona-fares-metro-bus/aeroport-ticket): só metrô, não integrado |
| T-casual: regras | individual; 75 min e até 3 baldeações em 1 zona; não vale nas estações Aeroport T1 e T2 da L9; dá para ir ao aeroporto de Rodalies ou de ônibus | [TMB, T-casual](https://www.tmb.cat/en/barcelona-fares-metro-bus/single-and-integrated/t-casual) e [ATM, T-casual](https://www.atm.cat/en/titols-i-tarifes/t-casual) |
| Hola Barcelona 24 / 48 / 72 / 96 / 120 h | € 12,50 / 18,70 / 27,30 / 35,60 / 43,60 | Loja oficial da TMB (catálogo público usado por holabarcelona.com, preços com vigência desde 01/01/2026). Online, com o desconto de 10% do site: € 11,25 / 16,83 / 24,57 / 32,04 / 39,24 |
| Hola Barcelona: regras | horas contadas da 1ª validação; inclui 1 ida e 1 volta de metrô ao aeroporto e Rodalies na zona 1; não inclui o Aerobús | [Hola Barcelona Travel Card](https://www.holabarcelona.com/tickets/hola-bcn-barcelona-travel-card) e [Aerobús, tarifas](https://aerobusbarcelona.es/en/rates/) (vende combos Hola + Aerobús à parte) |
| Aerobús | € 7,75 só ida · € 13,30 ida e volta (volta vale 90 dias); 24 h; 30 a 35 min até a Plaça Catalunya; A1 no T1, A2 no T2 | [Aerobús, tarifas](https://aerobusbarcelona.es/en/rates/) e FAQ do mesmo site |
| Trem R2 Nord | do Aeroport (T2) a cada 30 min (:08 e :38), das 5h40 às 23h38 em dia útil; ≈ 23 min até Sants e ≈ 28 min até Passeig de Gràcia | [Rodalies, horário R2 de 01/09/2026](https://rodalies.gencat.cat/web/.content/02_Horaris/horaris/R2.pdf) |
| Táxi | bandeirada € 2,80; € 1,35/km (dia útil, 8h–20h) ou € 1,66/km (noite, sábado e feriado); suplemento de aeroporto € 4,60; mínimo de € 21 saindo do aeroporto | [AMB, tarifas do táxi 2026](https://taxi.amb.cat/es/usuaris/tarifes-del-taxi) |
| Câmbio | € 1 = R$ 5,6609 (PTAX venda, fechamento de 15/10/2026); nos slides, R$ 5,66 | Banco Central do Brasil, API PTAX (Olinda) |

**Cuidado com fontes desatualizadas:** guias de viagem ainda mostram o Aerobús a € 7,45 / € 12,85 e o Hola a outros preços. E o domínio `aerobusbcn.com` não é mais o do Aerobús (hoje é uma página de cassino): o site oficial é `aerobusbarcelona.es`. Não citar o primeiro.

**O que é estimativa (e está marcado assim na arte):**
- **Táxi € 30–40:** conta pela tarifa AMB 2026 com distância estimada de 13 a 16 km até o centro (≈ € 25 a € 34 sem trânsito, mais o tempo de espera), conferida com guias de mercado que dão € 35–45. Não há preço fixo para o centro.
- **Metrô L9 "mais lento":** a L9 leva ≈ 32 min do aeroporto até Zona Universitària (guias da UAB e do ISEA, não oficiais) e exige baldeação para o centro. A arte não dá o tempo total.

**História real do slide 06 (Diego, 16/10/2026):** compraram o Hola 72 h; não chegaram pelo aeroporto; ficaram em Gràcia, um pouco mais longe do centro; usaram umas 4 viagens por dia e, no centro, andaram quase tudo a pé. A viagem foi em março de 2026 (EXIF da IMG_1198), já com as tarifas atuais: TMB desde 15/01/2026 e Hola desde 01/01/2026. Então a comparação usa os preços que valiam na viagem.

**Contas dos slides 06 e 07:**
- Preço por viagem na T-casual: € 13,00 ÷ 10 = € 1,30.
- Slide 06 (história real, por pessoa, 3 dias × ≈ 4 viagens = ≈ 12 viagens, sem aeroporto): T-casual € 13,00 + 2 bilhetes simples € 5,80 = **€ 18,80 ≈ R$ 106** contra Hola 72 h **€ 27,30 ≈ R$ 155** (preço de tabela). Diferença € 8,50 por pessoa; **casal € 17,00 ≈ R$ 96**. Mesmo com 2 T-casual por pessoa (20 viagens, € 26,00), ainda sairia mais barato que o Hola.
- **A confirmar com o Diego:** se o Hola foi comprado online, com o desconto de 10%, o preço pago foi € 24,57; aí a diferença cai para € 5,77 por pessoa e € 11,54 para o casal (≈ R$ 65). A arte e a legenda usam o preço de tabela.
- Slide 07 (viagens para o passe empatar com a T-casual): T-dia 12,00 ÷ 1,30 = 9,2 → **10+**; Hola 48 h 18,70 ÷ 1,30 = 14,4 → **15+**; Hola 72 h 27,30 ÷ 1,30 = 21,0 (empata) → **22+**.
- Com metrô L9 ida e volta ao aeroporto dentro do passe (o passe "paga" 2 × € 5,90 = € 11,80): 48 h (18,70 − 11,80) ÷ 1,30 = 5,3 → **6 viagens**; 72 h (27,30 − 11,80) ÷ 1,30 = 11,9 → **12 viagens**.
- Comprando o Hola online (10% a menos), os limites caem para 13 (48 h) e 19 (72 h). Está na legenda só como "10% mais barato online", sem mudar os números da arte.
- A conta usa a T-casual a € 1,30 por viagem. Quem não usa as 10 viagens perde o resto (não há reembolso), e isso favorece um pouco o passe em viagens curtas.

## Conformidade com o DS V2.2 (7.3 e 5.3)

- [x] Só tokens oficiais (cores, fontes, tamanhos, espaços, raios, sombras).
- [x] Canvas 3:4, margem 80, contador Plex Mono 30 no canto superior direito, etiqueta de série no superior esquerdo, Rota amarela de 8 px em y 1360 em todos os slides; no último, ela termina numa parada grafite de 24 px (DS 1.6).
- [x] ≤ 40 palavras por slide (o script conta: 12 a 40).
- [x] Valores com € e ≈ R$, cotação datada nos slides 03, 05 e 06 e na legenda (7.1 e 7.3).
- [x] História real no slide 06 e na legenda, com os dados que o Diego deu (≈ 4 viagens por dia marcado como aproximado).
- [x] 1 CTA na arte (`SALVA PRA VIAGEM →`), mesmo verbo da legenda (2.7). A legenda tem um segundo CTA (vlog no YouTube), a pedido do Diego (desvio 9).
- [x] Placa da capa com 849 px (≤ 872), destino em 128 px (9 letras), de y 1021 a 1240.
- [x] Símbolo 1º 96 px em x 904 · y 1168 no encerramento (mesma posição aprovada no carrossel de Roma).
- [x] Grão 5% em tudo; fibra 4% no papel.
- [x] Teste de miniatura: placa da capa e valores legíveis a 25% (`out/contato.jpg`).
- [x] Seta, `?` e ✓ desenhados em SVG, nunca digitados (1.2).
- [x] Capa com foto em sangria (Casa Batlló, escolha do Diego). Sem o Diego em primeiro plano: desvio registrado em Fotos.

## Desvios e decisões tomadas (precisam de aprovação do Diego)

1. **Nome da série "Chegar sabendo"** (etiqueta de série em todos os slides). Vem da promessa da marca ("Chegar sabendo: quanto custa, o que evitar e o que vale a pena"). Rótulo novo de série depende de aprovação (DS 7.4; mesmo caso da "Nota de soteropolitano" no banco de ideias). Alternativa mais literal: "Do aeroporto ao centro".
2. **Textos dos bilhetes na letra do Diego:** slide 08 "dica: t-casual não vale no metrô l9." (proposta do Claude, a partir das regras da TMB) e slide 09 "da próxima vez: t-casual." (a conclusão que o Diego tirou da própria viagem, 16/10/2026).
3. **Ticket "SABIA?":** o DS cita a variante (2.6, Curiosidade: sem estrela e com `?` no canhoto), mas não dá medidas. Usei a anatomia do ticket do bundle, com o `?` do módulo da placa e microcópia de 30 px (mínimo do carrossel).
4. **Quadro no carrossel:** 920 px de largura, linhas de 128 px (DS: 104) para caber o valor em € e o ≈ R$ embaixo, e nomes em 56 px (H3). No slide 07 o Quadro não é ranking: os números 1, 2 e 3 são os dias do passe.
5. **Recibo e Etiqueta de valor a 125%**, como no carrossel de Roma, para a microcópia chegar a 30 px. No recibo, o ≈ R$ de cada linha vai em Barlow 24 px (30 px na tela) e a linha de total mostra "1 viagem na T-casual", não uma soma.
6. **Pictogramas do slide 04** (trem, ônibus, metrô e táxi): desenhados seguindo a regra do DS 1.5 (cheio, amarelo, em quadrado grafite com raio de etiqueta), a 150% da grade 48/36. Ainda não existem no kit (pendência 7 do CLAUDE.md).
7. **Scrim na capa** (componente de Reel), como no carrossel de Roma, para a microcópia ficar legível sobre a foto.
8. **Fonte PD Placar** não existe no repositório: os números usam Barlow Condensed (fallback do bundle; pendência 1 do CLAUDE.md).
9. **Dois CTAs na legenda** (salvar e ver o vlog no YouTube pela bio), a pedido do Diego (16/10/2026). A arte mantém 1 CTA. A referência (3.4) e o DS (2.7) pedem 1 CTA por peça: exceção deste post, a registrar em Aprendizados para comparar.

## Pendências

- Confirmar o preço pago no Hola 72 h (máquina € 27,30 ou online € 24,57).
- A série não está no painel V5. Encaixar exige pedido do Diego (CLAUDE.md, 7): por exemplo, trocar carrosséis de segunda (18h30) ou somar à grade.
- **Futuro:** a nova linha R-Aeroport (FGC, a cada 15 min, ≈ 20 min do Passeig de Gràcia) está prevista para 2027 e deve tirar o R2 Nord do aeroporto ([NacióDigital, 15/05/2026](https://naciodigital.cat/societat/que-es-lr-aeroport-i-per-que-genera-polemica.html)). Quando entrar em operação, este carrossel fica desatualizado.
- **Rodalies em 2026:** R2 e R2 Nord tiveram cortes ao norte de Barcelona (Montcada, julho e setembro de 2026); o trecho do aeroporto seguiu a partir de Sant Andreu ([3Cat](https://www.3cat.cat/3catinfo/sense-data-de-represa-a-lr2-r2-nord-i-r11-tallades-per-lesvoranc-de-montcada-com-queda-el-servei/noticia/3421774/), [Metrópoli Abierta](https://www.metropoliabierta.cat/mobilitat/20260722/tallades-linies-r2-nord-r11-rodalies-despreniment-obres-montcada/1003742781621_0.html)). Por isso o aviso "confira no app Rodalies".

## Modelo para as próximas cidades da série

Mesma estrutura de 9 slides, trocando os dados. Para cada cidade, conferir em fonte oficial e registrar com data: (1) todas as opções do aeroporto principal ao centro, com preço, tempo, frequência e horário; (2) bilhete unitário e regras de integração; (3) passes de 24, 48 e 72 h e o que cobrem (aeroporto incluso ou não); (4) táxi: tarifa fixa ou taxímetro; (5) o "Sabia?" da cidade, um fato que surpreende e economiza; (6) a conta de quando o passe compensa. Cotação PTAX do dia útil anterior à montagem.
