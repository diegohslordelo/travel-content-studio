"""Carrosséis, fotos, Stories e vídeos longos da V5."""
from pecas_comum import carrossel, foto, stories, TRANSCRICAO, SEM_VALOR

CARROSSEIS = {

'CAR-lisboa-manha': carrossel(
    title='Lisboa em uma manhã: 7 paradas a pé, com a hora real',
    pillar='Roteiro (série oficial)', group='C',
    objective='Salvamento: roteiro de meia manhã montado com as horas reais do acervo.',
    audience='Quem tem poucas horas em Lisboa (escala, último dia).',
    concept='23/03, das 08h49 às 12h14: hotel → pastel de nata (08h59) → Elevador de Santa Justa (08h55, fechado segundo a fala) → Praça do Comércio (09h22) → Sé (09h54) → Miradouro de Santa Luzia (10h08) → Portas do Sol (10h17) → castelo por fora (10h38) → Rua Augusta (12h01).',
    promise='Um roteiro de manhã que coube a pé.',
    slides=['01 Capa: telhados de Santa Luzia + Placa "LISBOA EM / 1 MANHÃ" (máx. 6 palavras).', '02 Rota: 08h49 → 12h14, paradas 1–4 com hora (Rota DS V2, 5.3).', '03 Rota: paradas 5–7.',
            '04 Foto: Praça do Comércio + legenda "17 graus às 9h31, 23 de março".', '05 Dica (Bilhete): "passe do santa luzia: o portas do sol fica logo ali".', '06 O que não deu: castelo por fora (sem preço).', '07 Encerramento: Placa CTA "SALVA PRA VIAGEM →".'],
    cover='Telhados de Alfama (fotograma de IMG_4429) com Placa.',
    caption='Lisboa em uma manhã: 7 paradas a pé, com a hora real.\n\n23 de março, das 08h49 às 12h14, saindo de um hotel no centro. Tudo é perto.\n\nSalva para a sua viagem a Lisboa.\n\n#Lisboa #roteirolisboa #Portugal #oquefazeremlisboa #PrimeiroDia',
    cta='Salva para a sua viagem a Lisboa.', assets='acervo/lisboa (23/03): IMG_4282, 4289–4290, 4298, 4364, 4395, 4405, 4429, 4463, 4489, 4514 (fotogramas 4K).',
    timestamps='Horas do indice.tsv. Fotogramas: escolher na edição.', metric='Salvamentos.', risks=TRANSCRICAO + ' ' + SEM_VALOR + ' Nome da Sé: a transcrição diz "Sete Lisboa"; confirmar.',
    score=(1, 2, 2, 2, 2), scoreNote='Roteiro real com hora; formato de consulta.', ds='Carrossel 5.3: Rota contínua, contador, etiqueta ROTEIRO.'),

'CAR-docs': carrossel(
    title='Checklist de documentos para a Europa (conferido em fonte oficial)',
    pillar='Chegar sabendo · documentos', group='C',
    objective='Peça de consulta com fonte e data, salva antes das férias.',
    audience='Brasileiros indo à Europa.', concept='Uma única versão do checklist (a V4 tinha 3). Cada item com a fonte oficial e a data da consulta.',
    promise='Separar tudo antes de sair de casa.',
    slides=['01 Capa: passaporte + Placa "ANTES DE / EMBARCAR".', '02–06 Um item por slide (passaporte e validade, comprovantes, seguro, passagem de volta, hospedagem), só os confirmados.', '07 Fonte e data + CTA.'],
    cover='Passaporte sobre papel (foto nova ou do Diego).', caption='Checklist de documentos para a Europa, conferido em fonte oficial em [DD/MM].\n\n[Itens.]\n\nSalva para conferir antes do embarque.\n\n#documentosdeviagem #viagemeuropa #passaporte #checklist #PrimeiroDia',
    cta='Salva para conferir antes do embarque.', assets='Foto nova do passaporte (material futuro, simples) ou fotograma de aeroporto do acervo.', timestamps='—',
    metric='Salvamentos.', status='Validar fontes oficiais na produção', risks='Informação volátil: Portal Consular / Itamaraty e travel-europe.europa.eu na semana da publicação.',
    score=(2, 1, 2, 1, 2), scoreNote='Consulta clássica; vale pela fonte.', ds='Carrossel 5.3: slides de informação.',
    notes='Mantém o ID IG-20261108-CAR-geral-022 da V4 (movido de 09/11 para 26/10). As duas repetições da V4 (052 e 100) saíram.'),

'CAR-bruges-rota': carrossel(
    title='Bate-volta para Bruges: 5 paradas das 11h04 às 16h53',
    pillar='Roteiro (série oficial)', group='C', objective='Salvamento de quem faz bate-volta.', audience='Quem vai a Bruxelas e quer Bruges.',
    concept='Markt 11h47 → Burg 12h00 → canais 12h46 → Basílica 12h59 → batata 14h31 → Minnewater 14h47 → waffle 16h10 → McDonald’s medieval 16h53.', promise='O dia de Bruges organizado.',
    slides=['01 Capa: canal + Placa "BRUGES / BATE-VOLTA".', '02–04 Rota com hora.', '05 Dica: a batata que fez a gente voltar.', '06 O que fica para a próxima.', '07 CTA.'],
    cover='Canal (fotograma IMG_2549).', caption='Bate-volta para Bruges: das 11h04 às 16h53, a pé.\n\n16 de março. Markt, Burg, canais, Basílica, batata, Minnewater e waffle.\n\nSalva para o seu bate-volta.\n\n#Bruges #batevolta #Bélgica #roteirobruges #PrimeiroDia',
    cta='Salva para o seu bate-volta.', assets='acervo/bruges (16/03): fotogramas de IMG_2419, 2449, 2474, 2549, 2596, 2633, 2646, 2690, 2705.', timestamps='Horas do indice.tsv.',
    metric='Salvamentos.', risks=TRANSCRICAO + ' ' + SEM_VALOR + ' O trajeto Bruxelas–Bruges (trem? horário?) depende do Diego.', score=(1, 2, 2, 2, 2), scoreNote='Roteiro real.', ds='Carrossel 5.3.'),

'CAR-paris-rota': carrossel(
    title='Paris em 1 dia: 10 pontos, hora por hora',
    pillar='Roteiro (série oficial)', group='C', objective='O carrossel de consulta do dia em Paris.', audience='Quem tem 1 dia em Paris.',
    concept='Champ de Mars 11h29, Trocadéro 12h11, Arco 12h37, Champs-Élysées 13h04, Concorde 13h48, Tulherias/Louvre 14h10, Galeries Lafayette 14h51, Notre-Dame 17h22, Luxemburgo (fechado) 18h53, Torre brilhando 19h59.',
    promise='O dia inteiro numa rota.', slides=['01 Capa: Torre + Placa "PARIS EM / 1 DIA".', '02–05 Rota (máx. 5 paradas por slide).', '06 Carimbo reduzido no Luxemburgo + dica.', '07 Veredito: "Paris está aprovada" + CTA.'],
    cover='Torre (fotograma).', caption='Paris em 1 dia: 10 pontos, hora por hora.\n\n17 de março, das 11h29 às 20h. A pé e de metrô.\n\nSalva para o seu dia em Paris.\n\n#Paris #roteiroparis #1diaemparis #França #PrimeiroDia',
    cta='Salva para o seu dia em Paris.', assets='acervo/paris (17/03): fotogramas das faixas da DECUPAGEM_DISNEY_PARIS, seção 3.', timestamps='Horas do indice.tsv.', metric='Salvamentos.',
    risks=TRANSCRICAO + ' Contagem de 10 conferida na decupagem de 15/10.', score=(2, 2, 2, 1, 2), scoreNote='Roteiro mais pedido; prova real.', ds='Carrossel 5.3.',
    notes='Era a ideia F4 do banco da v5 antiga. Na semana do vlog provável de Paris (07/11) e antes do Reel da série (11/11).'),

'CAR-notas-comida': carrossel(
    title='As notas que a gente deu para a comida da Europa',
    pillar='Como foi de verdade · ranking', group='B', objective='Ranking com lógica explícita: a nota dita no dia.', audience='Quem viaja para comer.',
    concept='Só vereditos ditos nos vídeos: bacalhau "10 de 10" (Lisboa), batata "um dos pratos mais saborosos" (Bruges), pastel de nata "nota mil" (Lisboa), waffle "aprovado" (Bruxelas), churro "o do Brasil ganha" (Madrid), hambúrguer "Salvador dá um banho" (Madrid).',
    promise='O que vale provar.', slides=['01 Capa: Placa "AS NOTAS / DA VIAGEM".', '02–07 Um prato por slide, com cidade, data e a frase do dia (Bilhete).', '08 Quadro de ranking + CTA.'],
    cover='Bacalhau (fotograma IMG_4251).', caption='As notas que a gente deu para a comida da Europa, ditas no dia, sem retoque.\n\nDo bacalhau 10 de 10 ao churro que perdeu para o Brasil.\n\nSalva para a sua próxima viagem.\n\n#comidadeviagem #Europa #gastronomia #ondecomer #PrimeiroDia',
    cta='Salva para a sua próxima viagem.', assets='lisboa/IMG_4251–4253, IMG_4301; bruges/IMG_2634; bruxelas/IMG_2233; madrid/IMG_3954, IMG_3986 (fotogramas).', timestamps='Verificar cada fala.',
    metric='Salvamentos e envios.', risks=TRANSCRICAO + ' ' + SEM_VALOR + ' Nomes de restaurantes só confirmados.', score=(1, 2, 2, 2, 2), scoreNote='Ranking real; não inventa nota.', ds='Carrossel 5.3: Quadro de ranking.'),

'CAR-confira-antes': carrossel(
    title='7 coisas para conferir no site oficial na véspera',
    pillar='Chegar sabendo · checklist', group='C', objective='Transformar os perrengues reais em checklist de consulta.', audience='Quem planeja roteiro.',
    concept='Cada item nasce de um caso real: horário de jardim (Luxemburgo), brinquedo em reforma (Disney), calendário de jogo (Bernabéu), atração sazonal (piscina do Vondelpark), ingresso com hora (Park Güell), venda antecipada (Sagrada Família), elevador/atração fechada (Santa Justa).',
    promise='Não dar com a porta fechada.', slides=['01 Capa: Placa "CONFIRA / NA VÉSPERA".', '02–08 Um item por slide: o que conferir + o caso real (cidade e hora) em Plex Mono.', '09 CTA.'],
    cover='Portão fechado (fotograma IMG_3134).', caption='7 coisas para conferir no site oficial na véspera.\n\nCada item é um caso real da nossa viagem.\n\nSalva para conferir antes da sua.\n\n#planejamentodeviagem #dicasdeviagem #Europa #roteiro #PrimeiroDia',
    cta='Salva para conferir antes da sua.', assets='Fotogramas: paris/IMG_3134; disney/IMG_3232; madrid/IMG_4131; amsterdam/IMG_1743; Barcelona (master); lisboa/IMG_4289.', timestamps='—',
    metric='Salvamentos.', risks=TRANSCRICAO + ' Pareia com o Reel GER-fechado (02/12): mesmo fio, formato de consulta, publicado antes.', score=(2, 2, 2, 2, 2), scoreNote='Autoral e útil.', ds='Carrossel 5.3.'),

'CAR-bruxelas-rota': carrossel(
    title='Bruxelas em 1 dia: a rota das 3 estátuas',
    pillar='Roteiro (série oficial)', group='C', objective='Roteiro do dia com o fio das estátuas.', audience='Quem tem 1 dia em Bruxelas.',
    concept='11h29 chegada → Atomium 12h16 (metrô) → cachorro 13h16 → Fritland 13h53 → Grand-Place 14h13 → menina 14h25 → waffle 14h36 → Galeria 14h49 → Manneken Pis 16h12 → Mont des Arts 16h38.', promise='O dia organizado.',
    slides=['01 Capa: Grand-Place + Placa "BRUXELAS / EM 1 DIA".', '02–04 Rota.', '05 Dica: o sol engana (frio).', '06 CTA.'], cover='Grand-Place (fotograma IMG_2220).',
    caption='Bruxelas em 1 dia, com as 3 estátuas no caminho.\n\n15 de março, das 11h29 às 19h.\n\nSalva para o seu dia em Bruxelas.\n\n#Bruxelas #roteirobruxelas #Bélgica #1dia #PrimeiroDia', cta='Salva para o seu dia em Bruxelas.',
    assets='acervo/bruxelas (15/03): fotogramas.', timestamps='Horas do indice.tsv.', metric='Salvamentos.', risks=TRANSCRICAO + ' ' + SEM_VALOR, score=(1, 2, 2, 2, 2), scoreNote='Roteiro com fio narrativo.', ds='Carrossel 5.3.'),

'CAR-madrid-rota': carrossel(
    title='Madrid em 2 dias e meio: o que coube',
    pillar='Roteiro (série oficial)', group='C', objective='Consulta do roteiro de Madrid.', audience='Quem vai a Madrid.',
    concept='Dia 1 (19/03, desde 15h05): tapas, Sol, Plaza Mayor, San Miguel, Almudena, Palácio por fora, Debod. Dia 2: churros, Prado por fora, Cibeles, Alcalá, Retiro, Cristal, chuva, show. Dia 3: Bernabéu, Gran Vía.', promise='O roteiro por dia.',
    slides=['01 Capa: Placa "MADRID EM / 2 DIAS E MEIO".', '02 Dia 1.', '03 Dia 2.', '04 Dia 3.', '05 Dica: lotado em "baixa temporada" (fala de 19/03 16h15).', '06 CTA.'], cover='Plaza Mayor (fotograma IMG_3648).',
    caption='Madrid em 2 dias e meio: o que coube.\n\n19 a 21 de março, chegando às 15h05 no primeiro dia.\n\nSalva para a sua viagem a Madrid.\n\n#Madrid #roteiromadrid #Espanha #oquefazeremmadrid #PrimeiroDia', cta='Salva para a sua viagem a Madrid.',
    assets='acervo/madrid: fotogramas (ver DECUPAGEM_MADRID, seção 2).', timestamps='Horas do indice.tsv.', metric='Salvamentos.', risks=TRANSCRICAO + ' ' + SEM_VALOR + ' "Almudena: visitação gratuita" fica fora (regra de "grátis").',
    score=(1, 2, 2, 1, 2), scoreNote='Roteiro.', ds='Carrossel 5.3.'),

'CAR-roma-natal': carrossel(
    title='Natal em Roma: o que fizemos no dia 25',
    pillar='Roteiro · data', group='E', objective='Carrossel de fotos da Itália (regra: fotos italianas vão para carrossel).', audience='Quem sonha com Natal na Europa.',
    concept='As fotos com EXIF de 25/12/2024: Fontana di Trevi 10h08, Panteão 10h50, vila de Natal da Villa Borghese, pôr do sol no Pincio 16h37.', promise='O dia 25 em Roma, hora a hora.',
    slides=['01 Capa: Trevi (IMG_5064) + Placa "NATAL EM / ROMA".', '02 Trevi 10h08.', '03 Panteão 10h50.', '04 Villa Borghese (vila de Natal).', '05 Pincio 16h37.', '06 CTA.'],
    cover='IMG_5064.', caption='Natal em Roma: o que a gente fez no dia 25.\n\nTrevi às 10h08, Panteão às 10h50, a vila de Natal da Villa Borghese e o pôr do sol no Pincio às 16h37. 25 de dezembro de 2024.\n\nSalva para o seu Natal em Roma.\n\n#Roma #NatalemRoma #Itália #Natal #PrimeiroDia',
    cta='Salva para o seu Natal em Roma.', assets='Fotos de Roma no Drive (Itália/Roma): IMG_5064 (25/12 10:08), IMG_5108 (10:50), Villa Borghese (vila de Natal), IMG_5220 (16:37).', timestamps='EXIF.',
    metric='Salvamentos.', risks='O carrossel de Roma de 06/10 (custos) já usou parte dessas fotos: este é outro ângulo (o dia 25), sem preços. Não usar IMG_5397 (rostos de terceiros).', score=(1, 2, 2, 1, 2), scoreNote='Sazonal com fotos reais.', ds='Carrossel 5.3.',
    notes='Era a ideia "Natal em Roma: o que fizemos no dia 25" do inventário de 09/10 (verificado).'),

'CAR-frio-marco': carrossel(
    title='Europa em março: o frio de cada cidade',
    pillar='Chegar sabendo · clima e mala', group='C', objective='Consulta para fazer a mala.', audience='Quem vai à Europa no fim do inverno.',
    concept='Só o que foi dito no dia: Amsterdam "11 graus com sensação de 3" (12/03 20h46), Bruxelas "frio desumano" e sol que engana (15/03), Bruges "luvas e casaco" (16/03), Madrid chuva (20/03), Lisboa "17 graus e sol" (23/03 09h31).',
    promise='O que esperar e levar.', slides=['01 Capa: Placa "O FRIO DE / MARÇO".', '02–06 Uma cidade por slide com a frase do dia.', '07 Dica de mala (Bilhete) + CTA.'], cover='Marina com casaco em Bruges (fotograma IMG_2692).',
    caption='Europa em março: o frio de cada cidade, dito no dia.\n\nDe 11 graus com sensação de 3 em Amsterdam a 17 graus e sol em Lisboa.\n\nSalva para fazer a mala.\n\n#Europaemmarço #clima #mala #dicasdeviagem #PrimeiroDia', cta='Salva para fazer a mala.',
    assets='amsterdam/IMG_1516; bruxelas/IMG_2220, IMG_2394; bruges/IMG_2692; madrid/IMG_3935; lisboa/IMG_4395 (fotogramas).', timestamps='—', metric='Salvamentos.', risks=TRANSCRICAO + ' Dado de um dia, não média climática.',
    score=(1, 2, 2, 2, 2), scoreNote='Útil e real.', ds='Carrossel 5.3.'),

'CAR-italia-rota': carrossel(
    title='Itália em 9 dias: Roma, Florença, Veneza e Milão',
    pillar='Roteiro (série oficial)', group='C', objective='Roteiro de virada de ano com as datas reais.', audience='Quem planeja Itália no fim do ano.',
    concept='Datas do acervo: Roma 24–28/12, Florença 28–31/12, Veneza 31/12–02/01, Milão 02–03/01 (confirmar com o Diego as noites). Uma foto/fotograma por cidade.', promise='A divisão dos dias.',
    slides=['01 Capa: Placa "ITÁLIA EM / 9 DIAS".', '02 Mapa simples (Rota).', '03 Roma.', '04 Florença.', '05 Veneza.', '06 Milão.', '07 CTA.'], cover='Roma (foto).',
    caption='Itália em 9 dias: Roma, Florença, Veneza e Milão, de 24/12 a 03/01.\n\n[Noites por cidade confirmadas pelo Diego.]\n\nSalva para a sua viagem à Itália.\n\n#Itália #roteiroitalia #Roma #Veneza #PrimeiroDia', cta='Salva para a sua viagem à Itália.',
    assets='Fotos de Roma (Drive) + fotogramas de acervo/italia (Florença IMG_5554, Veneza IMG_6174, Milão IMG_6281).', timestamps='indice.tsv da Itália.', metric='Salvamentos.', status='Aguardando decisão do Diego',
    risks='As datas por cidade vêm do GPS; confirmar as noites. IMG_5020 (Milão pelo GPS, 24/12/2024 16:24) indica passagem por Milão na ida. Transporte entre cidades: dado do Diego.', score=(2, 2, 2, 1, 2), scoreNote='Roteiro muito buscado.', ds='Carrossel 5.3.'),

'CAR-chegadas': carrossel(
    title='8 primeiros dias para planejar 2027',
    pillar='Marca · panorama', group='D', objective='Peça da primeira semana do ano com a tagline: toda cidade tem um primeiro dia.', audience='Quem planeja viagens do ano.',
    concept='Um slide por cidade com a hora real da chegada e a primeira coisa que fizeram (Amsterdam 14h30, Bruxelas 11h29, Bruges 11h04, Paris 11h27, Disney 09h01, Madrid 15h05, Lisboa 19h16, Barcelona do vlog).', promise='Inspiração com dado.',
    slides=['01 Capa: Placa "8 PRIMEIROS / DIAS".', '02–09 Uma cidade por slide.', '10 Pergunta + CTA.'], cover='Placa sobre Amsterdam.',
    caption='Toda cidade tem um primeiro dia. Estes foram os nossos 8.\n\nA hora em que a gente chegou e a primeira coisa que fez em cada cidade.\n\nSalva para planejar as suas viagens de 2027.\n\n#viagem2027 #Europa #planejamento #inspiração #PrimeiroDia', cta='Salva para planejar as suas viagens de 2027.',
    assets='Fotogramas dos clipes do GER-chegamos.', timestamps='—', metric='Salvamentos.', risks=TRANSCRICAO, score=(1, 2, 2, 2, 2), scoreNote='Tagline em formato de consulta.', ds='Carrossel 5.3.'),

'CAR-quantos-dias': carrossel(
    title='Quantos dias em cada cidade? O que coube e o que faltou',
    pillar='Chegar sabendo · planejamento', group='C', objective='Responder a pergunta mais comum de planejamento com o que aconteceu de verdade.', audience='Quem monta roteiro de várias cidades.',
    concept='Bruxelas 1 dia (Atomium sem subir), Bruges bate-volta, Paris 1 dia (Louvre por fora, jardim fechado), Disney 1 dia (2 parques), Madrid 2,5 dias, Amsterdam 3 dias, Barcelona 3 dias, Lisboa 1 noite + manhã (castelo por fora). O "o que faltou" vem das falas.',
    promise='Dimensionar o roteiro.', slides=['01 Capa: Placa "QUANTOS / DIAS?".', '02–09 Uma cidade por slide: dias, o que coube, o que faltou.', '10 Veredito do Diego + CTA.'], cover='Placa sobre canal.',
    caption='Quantos dias em cada cidade? O que coube e o que faltou na nossa viagem.\n\n[Veredito do Diego por cidade.]\n\nSalva para montar o seu roteiro.\n\n#roteirodeviagem #Europa #quantosdias #planejamento #PrimeiroDia', cta='Salva para montar o seu roteiro.',
    assets='Fotogramas do acervo.', timestamps='—', metric='Salvamentos.', status='Aguardando decisão do Diego', risks='Veredito por cidade é opinião do Diego.', score=(2, 2, 2, 2, 2), scoreNote='Pergunta real de planejamento.', ds='Carrossel 5.3.'),

'CAR-amsterdam-rota': carrossel(
    title='Amsterdam em 3 dias: o que fizemos em cada dia',
    pillar='Roteiro (série oficial)', group='C', objective='Roteiro de consulta de Amsterdam.', audience='Quem vai a Amsterdam.',
    concept='Dia 1 (12/03): Museumplein por fora, casas tortas, Dam, batata, stroopwafel. Dia 2 (13/03): chuva, Anne Frank, Albert Cuyp, Museumplein, Vondelpark, Jordaan. Dia 3 (14/03): De Pijp, Sarphatipark, croquete na parede, Heineken Experience.', promise='3 dias organizados.',
    slides=['01 Capa.', '02 Dia 1.', '03 Dia 2.', '04 Dia 3.', '05 Dica: o vento e o frio.', '06 CTA.'], cover='Canal (fotograma IMG_1403).',
    caption='Amsterdam em 3 dias: o que a gente fez em cada um.\n\n12 a 14 de março.\n\nSalva para a sua viagem a Amsterdam.\n\n#Amsterdam #roteiroamsterdam #Holanda #3dias #PrimeiroDia', cta='Salva para a sua viagem a Amsterdam.',
    assets='acervo/amsterdam: fotogramas.', timestamps='Horas do indice.tsv (usar .MOV).', metric='Salvamentos.', risks=TRANSCRICAO + ' ' + SEM_VALOR, score=(1, 2, 2, 1, 2), scoreNote='Roteiro.', ds='Carrossel 5.3.'),

'CAR-rota-europa': carrossel(
    title='15 dias, 8 cidades: a ordem da nossa viagem',
    pillar='Roteiro · panorama', group='C', objective='Roteiro de viagem longa, a peça mais "salvável" do acervo.', audience='Quem planeja mochilão pela Europa.',
    concept='Barcelona (09–11/03) → Amsterdam (12–14/03) → Bruxelas (15/03) → Bruges (16/03) → Paris (17/03) → Disney (18/03) → Madrid (19–22/03) → Lisboa (22–23/03). Transporte entre cidades: dado do Diego.',
    promise='A rota inteira com datas.', slides=['01 Capa: Placa "15 DIAS / 8 CIDADES".', '02 Mapa (Rota amarela, DS V2 1.6).', '03–09 Trechos com datas e transporte.', '10 CTA.'], cover='Mapa próprio (nunca print do Google Maps).',
    caption='15 dias, 8 cidades: a ordem da nossa viagem pela Europa.\n\nDe Barcelona a Lisboa, de 9 a 23 de março. [Transporte de cada trecho.]\n\nSalva para montar o seu roteiro.\n\n#mochilão #roteiroeuropa #Europa #15dias #PrimeiroDia', cta='Salva para montar o seu roteiro.',
    assets='Datas do acervo/INDICE_GERAL.md; mapa desenhado no padrão do DS V2 (5.4).', timestamps='—', metric='Salvamentos.', status='Aguardando decisão do Diego',
    risks='Transporte entre as cidades e confirmação das datas de Barcelona (09–11/03 pelo inventário v5) dependem do Diego.', score=(2, 2, 2, 1, 1), scoreNote='Alto valor de consulta; depende de dados do Diego e de mapa.', ds='Carrossel 5.3 + mapa 5.4.'),

'CAR-disney-rota': carrossel(
    title='Disney: 2 parques em 1 dia, a ordem que funcionou',
    pillar='Roteiro (série oficial)', group='C', objective='Consulta do dia na Disney.', audience='Quem vai à Disneyland Paris.',
    concept='Studios de manhã (10h04 a 14h14) → Disneyland Park (14h21 em diante) → parada 17h24 → castelo rosado 19h11 → show e saída 22h19. Dicas reais: single rider, sair antes do fim do show.',
    promise='O dia organizado.', slides=['01 Capa.', '02 Manhã no Studios.', '03 Tarde no Disneyland Park.', '04 Noite.', '05 2 dicas (Bilhete).', '06 CTA.'], cover='Castelo rosado (fotograma IMG_3537).',
    caption='Disney de Paris: 2 parques em 1 dia, na ordem que funcionou para a gente.\n\n18 de março, das 10h às 22h19.\n\nSalva para a sua viagem à Disney.\n\n#DisneylandParis #roteirodisney #Disney #Paris #PrimeiroDia', cta='Salva para a sua viagem à Disney.',
    assets='acervo/disney (18/03): fotogramas.', timestamps='Horas do indice.tsv.', metric='Salvamentos.', risks=TRANSCRICAO + ' Nomes de atrações conferidos no mapa oficial.', score=(2, 2, 2, 1, 2), scoreNote='Roteiro muito buscado.', ds='Carrossel 5.3.',
    notes='Substitui as duas peças repetidas da V4 ("O que conferir antes de montar um roteiro para Disneyland Paris", 04/01 e 26/02).'),

'CAR-vale-ou-pula': carrossel(
    title='Vale ou pula: 6 atrações em 6 cidades',
    pillar='Vale ou pula (série oficial)', group='B', objective='Página de consulta da série VALE OU PULA.', audience='Quem decide onde gastar tempo.',
    concept='Heineken Experience (vale), Castelo de São Jorge com pouco tempo (depende), Palácio Real por fora (veredito do Diego), La Boqueria (veredito do Diego), Atomium sem subir (depende), terraço da Galeries Lafayette (veredito do Diego).',
    promise='Decidir rápido.', slides=['01 Capa: Placa "VALE OU / PULA".', '02–07 Uma atração por slide com Status VALE/PULA/DEPENDE (DS V2, 2.7).', '08 CTA.'], cover='Placa série.',
    caption='Vale ou pula: 6 atrações em 6 cidades.\n\n[Vereditos do Diego.]\n\nSalva para decidir a sua.\n\n#valeoupula #Europa #atrações #dicasdeviagem #PrimeiroDia', cta='Salva para decidir a sua.',
    assets='Fotogramas das peças da série.', timestamps='—', metric='Salvamentos.', status='Aguardando decisão do Diego', risks='Vereditos são do Diego.', score=(1, 2, 2, 1, 2), scoreNote='Consulta da série.', ds='Carrossel 5.3: Status VALE/PULA/DEPENDE.'),

'CAR-lisboa-custo': carrossel(
    title='Quanto custou Lisboa: uma noite e uma manhã',
    pillar='Custos reais', group='F', objective='Peça de custo de Lisboa (Recibo).', audience='Quem vai a Lisboa.',
    concept='Recibo longo da noite de 22/03 e da manhã de 23/03 (transporte, jantar, pastéis, almoço). Só com o registro do Diego.', promise='O total e o detalhe.',
    slides=['01 Capa: Recibo com o total.', '02 Transporte.', '03 Jantar.', '04 Manhã.', '05 Total + cotação.', '06 CTA.'], cover='Recibo.',
    caption='[Total real de Lisboa.]\n\n[Detalhe em € e R$, cotação de DD/MM.]\n\nSalva para montar o seu orçamento.\n\n#Lisboa #quantocusta #custodeviagem #Portugal #PrimeiroDia', cta='Salva para montar o seu orçamento.',
    assets='Registro de custos do Diego + fotogramas.', timestamps='—', metric='Salvamentos.', status='Aguardando dados de custos do Diego',
    costData='Aguardando dados de custos do Diego para 22–23/03. Os valores falados nos vídeos (💲) não são fonte.', risks='Sem registro, não sai (DS V2, 2.5).', score=(2, 2, 2, 1, 2), scoreNote='Custo.', ds='Carrossel 5.3: slide de custo.',
    notes='Era o Reel "Quanto custa um dia em Lisboa?" da V4 (IG-20261231-REE-lisboa-067): mudou para carrossel (o recibo é consulta) e saiu de 31/12 (dia do Réveillon).'),

'CAR-onde-comecar': carrossel(
    title='Primeira vez na Europa: por qual cidade começar',
    pillar='Chegar sabendo · decisão', group='C', objective='Responder com critérios honestos uma pergunta de alta busca.', audience='Quem vai à Europa pela primeira vez.',
    concept='Critérios observados na viagem, por cidade: chegada do aeroporto (metrô em Lisboa), andar a pé ("tudo é perto" em Lisboa), clima de março, idioma (Portugal), densidade de atrações (Paris). A escolha final é do Diego.',
    promise='Escolher com critério.', slides=['01 Capa: Placa "POR ONDE / COMEÇAR?".', '02 Os critérios.', '03–07 Cidades.', '08 Escolha do Diego + CTA.'], cover='Placa.',
    caption='Primeira vez na Europa: por qual cidade começar?\n\nOs critérios que a gente usaria, a partir do que viveu em 8 cidades.\n\nSalva para a sua primeira viagem.\n\n#primeiraviagem #Europa #dicasdeviagem #roteiro #PrimeiroDia', cta='Salva para a sua primeira viagem.',
    assets='Fotogramas do acervo.', timestamps='—', metric='Salvamentos.', status='Aguardando decisão do Diego', risks='Opinião do Diego; critérios só com base no que foi vivido.', score=(2, 2, 2, 1, 2), scoreNote='Pergunta de alta busca.', ds='Carrossel 5.3.'),
}

FOTOS = {
    'FOTO-cristal': foto(title='Palácio de Cristal, Madrid, 12h59', pillar='Foto única · memória', group='E', objective='Respiro no feed com imagem forte e contexto verdadeiro.',
        concept='Uma foto do Palácio de Cristal no Retiro antes da chuva (20/03).', assets='Foto original do Diego, se houver; senão, fotograma 4K de acervo/madrid/IMG_3924 (20/03 12:59).',
        caption='Palácio de Cristal, Retiro, Madrid. 20 de março, 12h59. 49 minutos depois, começou a chover.\n\n#Madrid #Retiro #PalácioDeCristal #PrimeiroDia', cta='Sem pedido de ação (respiro).',
        whyPhoto='A imagem sozinha basta; o Reel do mesmo lugar sai em janeiro (MAD-cristal) com movimento e chuva.', metric='Alcance e curtidas por alcance.'),
    'FOTO-munttoren': foto(title='Munttoren ao entardecer, Amsterdam', pillar='Foto única · memória', group='E', objective='Respiro visual entre peças de serviço.',
        concept='A torre ao fim da tarde do primeiro dia.', assets='Fotograma de acervo/amsterdam/IMG_1482 (usar o .MOV; a hora das cópias MP4 não é confiável).',
        caption='Munttoren, Amsterdam, no fim da tarde do nosso primeiro dia.\n\n#Amsterdam #Munttoren #Holanda #PrimeiroDia', cta='Sem pedido de ação.', whyPhoto='Luz de fim de tarde funciona parada.', metric='Curtidas por alcance.'),
    'FOTO-santa-luzia': foto(title='Telhados de Lisboa do Miradouro de Santa Luzia', pillar='Foto única · memória', group='E', objective='Respiro no feed.',
        concept='Os telhados de Alfama às 10h08.', assets='Foto do Diego ou fotograma de acervo/lisboa/IMG_4429 (23/03 10:08).', caption='Miradouro de Santa Luzia, Lisboa, 10h08 de uma segunda-feira de março.\n\n#Lisboa #Alfama #miradouro #PrimeiroDia',
        cta='Sem pedido de ação.', whyPhoto='Vista ampla, melhor parada.', metric='Curtidas por alcance.'),
    'FOTO-canal-bruges': foto(title='Um canal de Bruges, 12h46', pillar='Foto única · memória', group='E', objective='Respiro no feed.', concept='O canal do momento "a cidade tem cheiro de chocolate".',
        assets='Foto do Diego ou fotograma de acervo/bruges/IMG_2549 (16/03 12:46).', caption='Bruges, 12h46. A cidade tinha cheiro de chocolate.\n\n#Bruges #Bélgica #canais #PrimeiroDia', cta='Sem pedido de ação.', whyPhoto='Cartão-postal real.', metric='Curtidas por alcance.'),
    'FOTO-castelo-rosa': foto(title='O castelo da Disney às 19h11', pillar='Foto única · memória', group='E', objective='Respiro no feed.', concept='O castelo rosado ao entardecer.',
        assets='Fotograma de acervo/disney/IMG_3537 (18/03 19:08) ou foto do Diego.', caption='Disneyland Paris, 19h11. O castelo fica assim por poucos minutos.\n\n#DisneylandParis #Disney #PrimeiroDia', cta='Sem pedido de ação.', whyPhoto='A cor é o assunto.', metric='Curtidas por alcance.'),
    'FOTO-atomium': foto(title='Atomium contra o céu azul', pillar='Foto única · memória', group='E', objective='Respiro no feed.', concept='O Atomium às 12h19 do único dia em Bruxelas.',
        assets='Fotograma de acervo/bruxelas/IMG_2178.MOV (15/03 12:19) ou foto do Diego.', caption='Atomium, Bruxelas, 12h19. A câmera não dá conta do tamanho.\n\n#Bruxelas #Atomium #PrimeiroDia', cta='Sem pedido de ação.', whyPhoto='Forma gráfica forte.', metric='Curtidas por alcance.'),
    'FOTO-notre-dame': foto(title='Os vitrais da Notre-Dame', pillar='Foto única · memória', group='E', objective='Respiro no feed com emoção.', concept='O interior às 17h42.',
        assets='Fotograma de acervo/paris/IMG_3114–3119 (17/03 17:42) ou foto do Diego.', caption='Notre-Dame, Paris, 17h42.\n\n#NotreDame #Paris #PrimeiroDia', cta='Sem pedido de ação.', whyPhoto='Luz dos vitrais funciona parada.', metric='Curtidas por alcance.'),
}

LONGOS_INFO = {
    '2026-10-24': ('Amsterdam', 'Amsterdam', 'Data fixa — sábado, 24/10'),
    '2026-11-07': (None, 'Paris (1 dia)', None), '2026-11-21': (None, 'Disneyland Paris (2 parques em 1 dia)', None),
    '2026-12-05': (None, 'Madrid (2 dias)', None), '2026-12-19': (None, 'Bruxelas (1 dia)', None),
    '2027-01-02': (None, 'Bruges (1 dia)', None), '2027-01-16': (None, 'Lisboa (1 noite e 1 manhã)', None),
    '2027-01-30': (None, None, None), '2027-02-13': (None, None, None), '2027-02-27': (None, None, None),
}

# Stories: Geral (não aparecem como cidade), ligados às peças da semana. Não contam para os Reels.
STORIES = {
    'STO-w0': ('Bastidor: o primeiro post depois de 1 dia sem postar', ['Tela 1: print do Reel de ontem (peixinhos) com "saiu ontem".', 'Tela 2: enquete "você já pediu um prato sem saber o que era?" (sim/não).', 'Tela 3: link para o Reel.'], 'Enquete', 'Retomar a conversa e levar ao Reel de 15/10.'),
    'STO-w1a': ('Caixa de pergunta: o que você quer saber de Amsterdam?', ['Tela 1: "o vlog de Amsterdam sai sábado".', 'Tela 2: caixa de pergunta.', 'Tela 3: "respondo na sexta".'], 'Caixa de pergunta', 'Pesquisa de pauta; aquece o lançamento sem contar como aparição de cidade (a sequência é geral: anúncio do canal).'),
    'STO-w1b': ('Respostas da semana + lembrete do vlog', ['Telas 1–3: 3 respostas da caixa de segunda.', 'Tela 4: figurinha de lembrete (contagem regressiva) para sábado.'], 'Contagem regressiva', 'Relacionamento e lembrete.'),
    'STO-w2a': ('Bastidor: como a gente decupa 1.946 vídeos', ['Tela 1: print da planilha do acervo (sem dados pessoais).', 'Tela 2: "8 cidades, 1.946 vídeos".', 'Tela 3: enquete "qual cidade primeiro?" (4 opções).'], 'Enquete', 'Mostrar o método e pesquisar pauta.'),
    'STO-w2b': ('Quiz: em que cidade estava esse banheiro?', ['Tela 1: porta do banheiro (sem revelar).', 'Tela 2: quiz com 3 cidades.', 'Tela 3: resposta + link do Reel de quinta.'], 'Quiz', 'Levar ao LIS-chuveirinho.'),
    'STO-w3a': ('Pergunta: qual é o seu maior medo na chegada?', ['Tela 1: "tirar o medo da chegada é o motivo deste perfil".', 'Tela 2: caixa de pergunta.', 'Tela 3: "as respostas viram vídeo".'], 'Caixa de pergunta', 'Pesquisa direta do propósito da marca (alimenta GER-imigracao e GER-metodo).'),
    'STO-w3b': ('Teste de gancho: qual você assistiria?', ['Tela 1: gancho A do próximo Reel.', 'Tela 2: gancho B.', 'Tela 3: enquete A/B.'], 'Enquete A/B', 'Teste de uma variável (referência 8.3) com quem já segue.'),
    'STO-w4a': ('Enquete: vale ou pula?', ['Tela 1: foto de uma atração da semana.', 'Tela 2: enquete vale/pula.', 'Tela 3: "o meu veredito sai no Reel".'], 'Enquete', 'Aquecer a série VALE OU PULA.'),
    'STO-w4b': ('Bastidor: o arquivo que quase ninguém veria', ['Tela 1: um plano bruto da semana.', 'Tela 2: "por que ele entrou no Reel".', 'Tela 3: figurinha de reação.'], 'Reação', 'Relacionamento.'),
    'STO-w5a': ('Pergunta: o que você nunca come quando viaja?', ['Tela 1: carrossel de notas da semana.', 'Tela 2: caixa de pergunta.', 'Tela 3: link do carrossel.'], 'Caixa de pergunta', 'Levar ao CAR-notas-comida.'),
    'STO-w5b': ('Quiz: a que horas fechava o jardim?', ['Tela 1: portão fechado.', 'Tela 2: quiz 17h30 / 18h30 / 19h30 (resposta conferida).', 'Tela 3: link do PAR-luxemburgo.'], 'Quiz', 'Reforçar a dica da semana.'),
    'STO-w6a': ('Checklist da véspera (prévia do carrossel)', ['Tela 1: "a gente não conferiu. Você confere?".', 'Tela 2: enquete sim/não.', 'Tela 3: link do carrossel.'], 'Enquete', 'Levar ao CAR-confira-antes.'),
    'STO-w6b': ('Respostas: perguntas sobre custos', ['Tela 1: "a série de custos vem quando a planilha estiver revisada".', 'Tela 2: caixa "qual custo você quer ver?".'], 'Caixa de pergunta', 'Pesquisa para as peças de custo (sem valores).'),
    'STO-w7a': ('Enquete: você confere horário antes de sair?', ['Tela 1: prévia do Reel das portas fechadas.', 'Tela 2: enquete.', 'Tela 3: "quarta sai o vídeo".'], 'Enquete', 'Aquecer GER-fechado.'),
    'STO-w7b': ('Bastidor: a Torre às 19h48', ['Tela 1: a espera na ponte.', 'Tela 2: contagem "20h00".', 'Tela 3: link do Reel.'], 'Contagem', 'Levar ao PAR-torre-brilha.'),
    'STO-w8a': ('Pergunta: qual cidade você quer em 2 dias e meio?', ['Tela 1: carrossel de Madrid.', 'Tela 2: caixa de pergunta.'], 'Caixa de pergunta', 'Levar ao CAR-madrid-rota.'),
    'STO-w8b': ('Quiz: ela chorou ou não?', ['Tela 1: a aposta (09h47).', 'Tela 2: quiz sim/não.', 'Tela 3: link do DIS-aposta.'], 'Quiz', 'Retenção do Reel narrativo.'),
    'STO-w9a': ('Bastidor: o Natal de Roma em fotos', ['Tela 1–2: duas fotos do carrossel.', 'Tela 3: enquete "Natal na Europa: sim ou não?".'], 'Enquete', 'Levar ao CAR-roma-natal.'),
    'STO-w9b': ('Explicação rápida: o que é o EES', ['Tela 1: "a fronteira mudou".', 'Tela 2: 1 ponto do site oficial.', 'Tela 3: link do GER-ees.'], 'Link', 'Utilidade.'),
    'STO-w10a': ('Pergunta: vai viajar nas férias? Para onde?', ['Tela 1: carrossel do frio.', 'Tela 2: caixa de pergunta.'], 'Caixa de pergunta', 'Pesquisa de público (hipótese do DS a validar).'),
    'STO-w10b': ('Feliz Natal (leve)', ['Tela 1: Roma na manhã de Natal (fotograma).', 'Tela 2: "feliz natal" em Bilhete de caneta.'], 'Nenhum', 'Relacionamento na data.'),
    'STO-w11a': ('Enquete: Réveillon em casa ou viajando?', ['Tela 1: prévia de Veneza.', 'Tela 2: enquete.', 'Tela 3: "quinta tem a nossa virada".'], 'Enquete', 'Aquecer VEN-reveillon.'),
    'STO-w11b': ('Todo ano tem um primeiro dia', ['Tela 1: "1º de janeiro: o primeiro dia do ano".', 'Tela 2: caixa "qual vai ser o seu primeiro dia em 2027?".'], 'Caixa de pergunta', 'Tagline na data perfeita.'),
    'STO-w12a': ('Respostas: os primeiros dias de 2027 de vocês', ['Telas 1–3: respostas.', 'Tela 4: link do CAR-chegadas.'], 'Link', 'Relacionamento.'),
    'STO-w12b': ('Teste de gancho: método', ['Tela 1: gancho A do GER-metodo.', 'Tela 2: gancho B.', 'Tela 3: enquete.'], 'Enquete A/B', 'Teste de uma variável.'),
    'STO-w13a': ('Pergunta: quantos dias você daria para Paris?', ['Tela 1: carrossel dos dias.', 'Tela 2: controle deslizante 1–7.'], 'Controle deslizante', 'Levar ao CAR-quantos-dias.'),
    'STO-w13b': ('Quiz: qual batata ganhou?', ['Tela 1: os 3 cones.', 'Tela 2: quiz Amsterdam/Bruxelas/Bruges.', 'Tela 3: link.'], 'Quiz', 'Levar ao GER-batata-3.'),
    'STO-w14a': ('Bastidor: a noite dos 4 restaurantes', ['Tela 1: plano da rua à noite.', 'Tela 2: "quarta sai a história".', 'Tela 3: enquete "já rodou atrás de jantar?".'], 'Enquete', 'Aquecer LIS-primeira-noite.'),
    'STO-w14b': ('Vale ou pula com vocês', ['Tela 1: Heineken Experience.', 'Tela 2: enquete vale/pula.', 'Tela 3: link do Reel.'], 'Enquete', 'Série VALE OU PULA.'),
    'STO-w15a': ('Pergunta: qual trecho da rota você quer detalhado?', ['Tela 1: mapa do carrossel.', 'Tela 2: caixa de pergunta.'], 'Caixa de pergunta', 'Pesquisa de pauta para depois de fevereiro.'),
    'STO-w15b': ('Enquete: qual cidade primeiro?', ['Tela 1: prévia do GER-qual-primeiro.', 'Tela 2: enquete 4 opções.'], 'Enquete', 'Levar aos comentários do Reel.'),
    'STO-w16a': ('Bastidor: as dicas da Disney numa tela', ['Tela 1: carrossel.', 'Tela 2: figurinha de link.'], 'Link', 'Levar ao CAR-disney-rota.'),
    'STO-w16b': ('Pergunta: qual tradição de viagem você tem?', ['Tela 1: a tradição da Marina (McDonald’s).', 'Tela 2: caixa de pergunta.'], 'Caixa de pergunta', 'Aquecer GER-mcdonalds e puxar histórias do público.'),
    'STO-w17a': ('Vereditos: vocês concordam?', ['Telas 1–3: 3 vereditos do carrossel com enquete.'], 'Enquete', 'Levar ao CAR-vale-ou-pula.'),
    'STO-w17b': ('Respostas: tradições de viagem', ['Telas 1–3: respostas.', 'Tela 4: link do Reel.'], 'Link', 'Relacionamento.'),
    'STO-w18a': ('Bastidor: a planilha (sem números)', ['Tela 1: estrutura borrada.', 'Tela 2: enquete "você anota gastos?".'], 'Enquete', 'Aquecer GER-planilha.'),
    'STO-w18b': ('Quiz: em que cidade foi esta despedida?', ['Tela 1: plano final de uma cidade.', 'Tela 2: quiz.', 'Tela 3: "domingo tem as 8".'], 'Quiz', 'Aquecer GER-despedidas.'),
    'STO-w19a': ('Pergunta: por onde você começaria?', ['Tela 1: carrossel.', 'Tela 2: caixa de pergunta.'], 'Caixa de pergunta', 'Levar ao CAR-onde-comecar.'),
    'STO-w19b': ('Fim do ciclo: o que vem agora', ['Tela 1: "o acervo de 2026 acabou aqui".', 'Tela 2: caixa "qual primeiro dia você quer ver?".'], 'Caixa de pergunta', 'Fechamento do ciclo e pauta do próximo.'),
}
