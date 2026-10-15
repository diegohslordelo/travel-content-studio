"""Conteúdo v6 · peças gerais (várias cidades): documentação, preparação e custos da viagem de março.

Regras: dicas gerais ficam separadas do relato; regra de entrada, documento e tarifa = conferir em fonte oficial
na produção (prod='ofc'); custo = dado fornecido pelo Diego na produção (prod='cus'), nenhum valor aqui.
Pesquisa de contexto (15/10/2026): o site oficial do ETIAS diz que o sistema não está em operação e que a data será
anunciada com meses de antecedência (Connexion, 2026; schengentraveler.com, jul/2026). Conferir de novo na produção.
"""

OFC = 'Conferir na fonte oficial na produção (regra que muda): site oficial do ETIAS/EES da União Europeia e Itamaraty/consulados. Não publicar como fato atual sem essa conferência.'

PECAS = {
    'p830': dict(
        fmt='Reel', pilar='Antes de ir', titulo='Brasileiro precisa de visto para a Europa?',
        gancho='Precisa de visto pra Europa?', gt='Pergunta', nivel='B', prod='ofc',
        obj='Utilidade de alta busca: responder a dúvida mais comum de quem planeja a primeira viagem à Europa, com a regra conferida na fonte oficial no dia da produção.',
        motiv='Quem está planejando a primeira viagem à Europa. Salva e manda para quem vai junto.',
        q0='Chegada ao aeroporto de Amsterdam (IMG_1375, 12/03/2026 11:3x, “acabamos de pousar”), com o gancho na tela.',
        sc=[('0–2 s', 'Gancho', 'IMG_1375 (Amsterdam, “acabamos de pousar”, primeiros 2 s) + gancho escrito. Placa Marca `PRIMEIRO DIA →` com a Chegada.'),
            ('2–7 s', 'Resposta curta', 'Legenda Informação com a regra para turismo (dias permitidos no espaço Schengen), conferida na fonte oficial. Fundo: IMG_4233 (Lisboa, metrô do aeroporto, 22/03).'),
            ('7–12 s', 'O que muda', 'Legenda: o status do ETIAS no dia da produção (em 15/10/2026 o site oficial dizia que ainda não estava em operação). Fundo: plano de estação ou aeroporto do acervo.'),
            ('12–17 s', 'O que levar', 'Lista curta na tela: passaporte (validade exigida), e o que a fronteira pode pedir. Tudo conferido na fonte oficial.'),
            ('17–19 s', 'Fecho', 'Bilhete: “confere antes de comprar a passagem.”')],
        tela='precisa de visto pra europa? · [regra conferida] · etias: [status no dia] · confere antes de comprar a passagem.',
        nar='Sem narração (texto na tela). Se o Diego gravar uma fala nova, ela é material futuro e fica registrada como tal.',
        leg='Precisa de visto pra Europa? ✈️\n\n[Regra conferida no site oficial no dia da postagem: turismo, dias permitidos, ETIAS.]\n\nIsso é regra geral, não é dica de quem trabalha com imigração: confere sempre na fonte oficial antes de comprar a passagem.\n\nSalva pra quando for planejar.',
        cta='Salva pra quando for planejar (salvamento).', capa='“VISTO?” sobre o plano do aeroporto.', som='Ambiente baixo + música calma da biblioteca.',
        hip='Pergunta de alta busca com resposta conferida gera salvamento e alcance fora da bolha.', met='Salvamentos por alcance',
        mat=['Amsterdam IMG_1375 (12/03/2026, chegada no aeroporto, fala “acabamos de pousar”)', 'Lisboa IMG_4233 (22/03/2026, metrô do aeroporto)', 'Barcelona: master do vlog, trecho do aeroporto (33:20–34:05) como alternativa'],
        pend=[OFC, 'Distinguir regra geral de relato: só dizer “a gente entrou só com passaporte” se o Diego confirmar', 'Fonte e data da conferência na legenda ou no comentário fixado'],
        fonte='Acervo · aeroportos e estações', trecho='IMG_1375 · IMG_4233',
        cus=None, video_longo=None, tipo=None,
        tt=dict(gancho='Brasileiro precisa de visto pra Europa?', muda='Mesma edição; texto maior no primeiro segundo e pergunta para os comentários (“qual foi sua dúvida?”).'),
        yt=dict(titulo='Brasileiro precisa de visto para a Europa?', muda='Mesmo corte; descrição com a fonte oficial e a data da conferência.'),
    ),
    'p831': dict(
        fmt='Carrossel', pilar='Antes de ir', titulo='Antes de embarcar pra Europa: o checklist que a gente faria de novo',
        gancho='8 coisas pra conferir antes de embarcar.', gt='Lista curta', nivel='—', prod='ofc',
        obj='Salvamento: checklist prático que mistura regra geral (conferida na fonte oficial) com 3 lições reais das viagens (frio, ingresso que acabou, horário que fechou).',
        motiv='Quem vai viajar nos próximos meses. Salva e manda para quem viaja junto.',
        q0='Capa de papel com a Placa G `ANTES DE IR` e a Rota.',
        sl=['Capa (papel): Placa G `ANTES DE IR` + “8 coisas pra conferir antes de embarcar”.',
            'Slide 2 (funciona sozinho): a lista inteira em 8 linhas, com o número de parada da Rota (DS V2, 5.3).',
            '1 · Passaporte e validade exigida (regra geral, conferida na fonte oficial). Foto: quadro de aeroporto do acervo (IMG_1375).',
            '2 · Regra de entrada e ETIAS (status no dia da postagem). Texto curto + “fonte oficial e data” no rodapé.',
            '3 · Seguro-viagem: o que conferir na apólice (regra geral). Texto, sem relato.',
            '4 · Ingressos que esgotam: “a gente deixou a Capela Sistina pra depois e não conseguiu” (relato real, carrossel de Roma publicado em 06/10). Foto de Roma.',
            '5 · Horário de parque e jardim muda com a estação: o Jardim de Luxemburgo fechado às 18h53 (relato real, IMG_3134, 17/03/2026). Quadro do vídeo.',
            '6 · Roupa de frio: “sete graus em Bruxelas” (relato real, IMG_2394, 15/03/2026). Quadro do vídeo.',
            '7 · Transporte do aeroporto ao centro: veja antes (em Lisboa foi de metrô, IMG_4233). Quadro do vídeo.',
            '8 · Encerramento: `SALVA PRA VIAGEM →`.'],
        tela='Slides acima.', nar='Não se aplica (carrossel).',
        leg='8 coisas pra conferir antes de embarcar pra Europa. ✈️\n\nAs regras de documento e de entrada vêm da fonte oficial, conferida no dia da postagem. As outras três a gente aprendeu na prática: o ingresso que esgotou, o jardim que fechou e o frio que ninguém avisou.\n\nSalva pra sua próxima viagem.',
        cta='Salva pra viagem (salvamento).', capa='Capa de papel com a Placa G.', som='Música instrumental da biblioteca.',
        hip='Checklist com 3 lições reais diferencia o perfil das listas genéricas: salvamento.', met='Salvamentos por alcance',
        mat=['Amsterdam IMG_1375', 'Roma: foto do carrossel publicado (carrosseis/roma-3-dias/rev1)', 'Paris IMG_3134 (17/03 18:53)', 'Bruxelas IMG_2394 (15/03)', 'Lisboa IMG_4233 (22/03)'],
        pend=[OFC, 'Itens 1, 2 e 3 são regra geral: legenda deixa claro que não é relato', 'Quadros dos vídeos: exportar nítidos (vídeo parado) na decupagem'],
        fonte='Acervo · várias cidades', trecho='IMG_1375 · IMG_3134 · IMG_2394 · IMG_4233',
        cus=None, video_longo=None, tipo=None,
    ),
    'p832': dict(
        fmt='Reel', pilar='Antes de ir', titulo='Seguro-viagem pra Europa: o que conferir antes de contratar',
        gancho='Seguro-viagem: confere isso antes.', gt='Lista curta', nivel='B', prod='ofc',
        obj='Utilidade: 3 pontos para conferir na apólice e a regra de exigência para a Europa, conferida na fonte oficial no dia da produção. Dica geral, sem relato inventado.',
        motiv='Quem está comprando o seguro da primeira viagem internacional. Salva.',
        q0='Plano de mala e saída de estação do acervo com o gancho na tela.',
        sc=[('0–2 s', 'Gancho', 'Plano de estação ou aeroporto do acervo (IMG_4233, Lisboa) + gancho escrito.'),
            ('2–8 s', 'Exigência', 'Legenda Informação: quando o seguro é exigido para entrar no espaço Schengen (regra conferida na fonte oficial).'),
            ('8–15 s', '3 pontos', 'Lista curta na tela, 1 por plano: cobertura médica mínima, cobertura para os países do roteiro, o que fazer em caso de uso. Fundos: ruas de cidades do acervo.'),
            ('15–17 s', 'Fecho', 'Bilhete: “lê a apólice antes de pagar.”')],
        tela='seguro-viagem: confere isso antes. · [regra conferida] · cobertura · países · como acionar · lê a apólice antes de pagar.',
        nar='Sem narração.',
        leg='Seguro-viagem pra Europa: confere isso antes de contratar. 🧳\n\n[Regra de exigência conferida na fonte oficial no dia da postagem.]\n\nIsso é dica geral, não é indicação de seguradora.\n\nSalva pra quando for contratar o seu.',
        cta='Salva pra quando for contratar (salvamento).', capa='“SEGURO” sobre o plano da estação.', som='Música calma da biblioteca.',
        hip='Dúvida prática e recorrente gera salvamento.', met='Salvamentos por alcance',
        mat=['Lisboa IMG_4233 (22/03/2026, estação do aeroporto)', 'Planos de rua do acervo (escolher na decupagem)'],
        pend=[OFC, 'Diego: se vocês tinham seguro e quiser contar como foi, vira relato; sem isso, a peça fica como dica geral', 'Não citar marca de seguradora (sem parceria)'],
        fonte='Acervo · várias cidades', trecho='IMG_4233',
        cus=None, video_longo=None, tipo=None,
        tt=dict(gancho='Seguro-viagem pra Europa: confere isso', muda='Mesma edição, ritmo um pouco mais rápido (1,5 s por item).'),
        yt=dict(titulo='Seguro-viagem para a Europa: o que conferir', muda='Mesmo corte; fonte oficial e data na descrição.'),
    ),
    'p232': dict(
        fmt='Carrossel', pilar='Quanto custa', titulo='A passagem é só o começo: para onde foi o dinheiro da viagem de março',
        gancho='A passagem foi só o começo.', gt='Afirmação', nivel='—', prod='cus',
        obj='Planejamento financeiro: mostrar as categorias de gasto de uma viagem de 15 dias por 6 cidades (hospedagem, comida, passeios, transporte entre cidades, transporte local), com os valores do Diego.',
        motiv='Quem está montando o orçamento da primeira viagem à Europa. Salva para planejar.',
        q0='Capa de papel com o Recibo e a Placa G `QUANTO CUSTOU`.',
        sl=['Capa (papel): Placa G `QUANTO CUSTOU` + “a passagem foi só o começo”.',
            'Slide 2 (funciona sozinho): Recibo com as categorias e o total sem passagem aérea internacional: [valores do Diego], por pessoa ou por casal (escopo escrito no topo).',
            'Hospedagem nas 5 cidades com hotel: [valor do Diego] + foto de uma janela/rua de cada cidade.',
            'Comida: [valor do Diego] + a regra que a gente usou (relato do Diego).',
            'Passeios e ingressos: [valor do Diego] + o que valeu pagar (veredito do Diego).',
            'Transporte entre cidades (trem, avião interno): [valores do Diego].',
            'Transporte dentro das cidades: [valor do Diego].',
            'Etiqueta de valor: cotação usada e data (formato de valores do DS V2).',
            'Encerramento: `SALVA PRA VIAGEM →`.'],
        tela='Slides acima.', nar='Não se aplica (carrossel).',
        leg='A passagem foi só o começo. 🧾\n\n[Resumo do Diego: total sem passagem aérea, escopo, período 08 a 23/03/2026, cotação e data.]\n\nSalva pra montar o seu orçamento.',
        cta='Salva pra montar o seu orçamento (salvamento).', capa='Recibo + Placa G.', som='Música instrumental da biblioteca.',
        hip='Orçamento real por categoria é referência de planejamento: salvamento e envio.', met='Salvamentos por alcance',
        mat=['Fotos e quadros de cada cidade do acervo (um por slide)', 'Valores: fornecidos pelo Diego na produção'],
        pend=['Aguardando dados de custos do Diego (na produção desta peça)', 'A planilha “Custos de Viagens - Europa” (Drive) tem totais por categoria, mas mistura valores pagos e orçamento: o Diego diz quais valores valem', 'Não misturar passagem aérea internacional no total'],
        fonte='Registro de custos do Diego', trecho='Viagem de março de 2026',
        cus=dict(dados=['Total por categoria: hospedagem (por cidade), comida, passeios e ingressos, transporte entre cidades, transporte local', 'Escopo: por pessoa ou por casal', 'Período exato (08 a 23/03/2026?) e se Lisboa entra', 'Cotação usada (data)', 'O que ficou de fora (passagem aérea internacional)'],
                 escopo='Viagem de março de 2026, todas as cidades, sem passagem aérea internacional', quando='na produção desta peça'),
        video_longo=None, tipo=None,
    ),
    'p263': dict(
        fmt='Carrossel', pilar='Quanto custa', titulo='Quanto custou cada cidade por dia',
        gancho='Qual cidade pesou mais no bolso?', gt='Comparação', nivel='—', prod='cus',
        obj='Comparação útil entre destinos, só com dados comparáveis: gasto por dia por pessoa em cada cidade, mesmo critério e mesma cotação.',
        motiv='Quem está escolhendo entre cidades europeias. Salva e manda para quem vai junto.',
        q0='Capa com o Quadro (ranking) do DS V2 e as cidades.',
        sl=['Capa (papel): Placa G `QUANTO CUSTOU` + “qual cidade pesou mais no bolso?”.',
            'Slide 2 (funciona sozinho): Quadro de ranking (DS V2) com o gasto por dia por pessoa de cada cidade: [valores do Diego].',
            'Um slide por cidade (Barcelona, Amsterdam, Bruxelas e Bruges, Paris, Disney, Madrid, Lisboa): foto + [gasto por dia do Diego] + 1 frase do que mais pesou.',
            'Como a gente comparou: mesmo critério (por pessoa, sem passagem aérea, com ou sem hotel) e cotação com data.',
            'Encerramento: `SALVA PRA VIAGEM →`.'],
        tela='Slides acima.', nar='Não se aplica (carrossel).',
        leg='Qual cidade pesou mais no bolso? 💶\n\n[Ranking do Diego, critério e cotação.]\n\nSalva pra escolher o seu roteiro.',
        cta='Salva pra escolher o roteiro (salvamento).', capa='Quadro de ranking.', som='Música instrumental da biblioteca.',
        hip='Comparação com critério claro gera salvamento e comentários.', met='Salvamentos e comentários por alcance',
        mat=['1 foto/quadro por cidade do acervo', 'Valores: fornecidos pelo Diego na produção'],
        pend=['Aguardando dados de custos do Diego (na produção desta peça)', 'Só entra se os dados forem comparáveis (mesmo critério em todas as cidades); se não forem, a peça vira “quanto custou cada cidade” sem ranking'],
        fonte='Registro de custos do Diego', trecho='Viagem de março de 2026',
        cus=dict(dados=['Gasto total de cada cidade e número de dias em cada uma', 'Mesmo critério para todas: por pessoa, com ou sem hotel, sem passagem aérea', 'Cotação e data'],
                 escopo='Cada cidade da viagem de março de 2026', quando='na produção desta peça'),
        video_longo=None, tipo=None,
    ),
}

REVISOES = {
    'p625': dict(
        obj='Conversão e memória de marca: o mapa da viagem de março (e de Roma) com o primeiro dia de cada lugar. Sem anúncio de viagem futura.',
        leg='9 primeiros dias, 1 mapa. 🗺️\n\nBarcelona, Amsterdam, Bruxelas, Bruges, Paris, Disney, Madrid e Lisboa em março. Roma no Natal.\n\nQual primeiro dia você quer ver de novo? Conta aqui.',
        cta='Conta nos comentários (comentário).',
    ),
}

TIKTOK, SHORT_CAP, STORIES, TT_ADAPT, YT_ADAPT = {}, {}, {}, {}, {}
YT_ADAPT['p264'] = dict(titulo='2 erros de viagem que a gente não repete', muda='Mesmo corte; CTA final trocado por “segue o canal”.')
TT_ADAPT['p264'] = dict(gancho='2 erros que a gente não repete', muda='Mesma edição; pergunta final “qual erro você já cometeu?”.')
TT_ADAPT['p281'] = dict(gancho='(sem texto)', muda='Mesma edição; pergunta na legenda “qual você visitaria primeiro?”.')
YT_ADAPT['p281'] = dict(titulo='Qual dessas cidades você visitaria primeiro?', muda='Mesmo corte.')
TT_ADAPT['p612'] = dict(gancho='A primeira coisa que comemos aqui', muda='Mesma edição; texto mais curto por cidade.')
YT_ADAPT['p612'] = dict(titulo='A primeira coisa que comemos em 6 cidades', muda='Mesmo corte.')
TT_ADAPT['p217'] = dict(gancho='9 primeiros dias. Qual é o seu?', muda='Mesma edição.')
TT_ADAPT['p247'] = dict(gancho='O melhor primeiro dia do ano', muda='Mesma edição; pede para comentar o favorito.')
YT_ADAPT['p247'] = dict(titulo='Ranking: o melhor primeiro dia de 2026', muda='Mesmo corte.')
