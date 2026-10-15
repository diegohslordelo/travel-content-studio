"""Conteúdo v6 · grupo Itália (Roma, Florença, Veneza, Milão). Lido por aplicar_v6.py.

Fontes: acervo/italia/ (indice.tsv, transcricoes.tsv, linha_do_tempo.md), carrosseis/roma-3-dias/rev1/ (LEGENDA.md,
QA_REV1.md), planejamento/ESTUDO_CARROSSEL_ROMA.md (registro de custos de Roma), pecas_v5_futuras.json e plano_v6.json.

Como os lugares foram identificados: os vídeos de Roma ainda não foram vistos nas folhas de contato. O lugar de cada
arquivo vem do GPS gravado no próprio arquivo (coluna gps de acervo/italia/indice.tsv), comparado com as coordenadas
dos pontos conhecidos (ex.: IMG_5067–5073 em 41,9008 · 12,4833 = Fontana di Trevi). Isso é dedução, não quadro visto:
toda cena de Roma leva "conferir na folha de contato". Em Florença, Veneza e Milão, os trechos vistos pelo Diego em
15/10 estão marcados como vistos; o resto também é GPS.

Regras aplicadas (BRIEF v6): nada de valores (custo = dado do Diego na produção, marcador [valor do Diego]); fala da
transcrição automática só depois de ouvir; família do Diego (5 pessoas na viagem) só com autorização; fotos da Itália
só em carrossel; vídeos da Itália em Reel, Short, TikTok e Stories.
"""

# ───────────────────────── pendências repetidas ─────────────────────────
OUVIR = 'Fala vem da transcrição automática (ninguém ouviu): ouvir o áudio antes de usar; nomes e números saem errados.'
FAM = ('Viagem em família (5 pessoas): se o pai, a mãe ou outros familiares aparecerem no trecho, Diego autoriza? '
       'Se não, cortar o trecho ou usar só planos sem rosto. Só a foto da capa do carrossel de Roma tem autorização do pai.')
GPS_ROMA = ('Vídeos de Roma não foram vistos nas folhas de contato: o lugar vem do GPS do arquivo (acervo/italia/indice.tsv). '
            'Conferir na folha de contato (Drive, Youtube/analise/…/folhas/) o que aparece em cada trecho antes do corte.')
GPS = 'Lugar deduzido do GPS do arquivo (acervo/italia/indice.tsv), não do quadro: conferir na folha de contato.'
SEM_VALOR = 'Nenhum valor em € ou R$ na peça, na legenda ou na tela; trechos com fala de preço ficam fora (acervo/CORTES_DE_CUSTO.md).'
D1 = None  # D1 resolvida pelo Diego em 15/10: vídeo da Itália pode ir para Reel; fotos da Itália só em carrossel


PECAS = {
    # ═════════════════════════ CARROSSÉIS DE CUSTO (Roma) ═════════════════════════
    'p218': dict(
        fmt='Carrossel', pilar='Quanto custa', titulo='Roma: o que foi de graça e o que foi pago',
        gancho='Roma: de graça × pago.', gt='Comparação', nivel='—', prod='cus',
        obj=('Salvamento: separar, com o registro real de dez/2024, o que em Roma não custou nada e o que foi pago, '
             'e avisar o que mudou desde então (Trevi e Panteão). Era o p218 "Roma de graça", adiado em 14/10.'),
        motiv='Quem vai a Roma com orçamento curto. Salva para montar o roteiro; manda para quem divide a viagem.',
        q0='Capa: pôr do sol no Pincio (IMG_5220, 25/12/2024 16:37), que foi de graça, com o título na Placa.',
        sl=["Capa: foto IMG_5220 (Pincio, 25/12 16:37) + Placa `ROMA: DE GRAÇA × PAGO` e microcópia `dez/2024 · por pessoa`. "
            "Não usar a arena do Coliseu (foi a capa do carrossel de 06/10).",
            "Slide 2 (segunda capa, funciona sozinho): duas colunas no papel. GRÁTIS: Fontana di Trevi*, Piazza Navona, Piazza di Spagna, "
            "Piazza del Popolo e Pincio, Basílica de São Pedro, igreja de Sant'Ignazio, Gianicolo, Ponte Sant'Angelo. "
            "PAGO: Coliseu + Fórum + Palatino [valor do Diego] · Panteão [valor do Diego] · vila de Natal da Villa Borghese [valor do Diego] · "
            "espelho de Sant'Ignazio [valor do Diego] · passe de 72 h [valor do Diego]. *Rodapé: 'a Trevi passou a cobrar para chegar perto: ver slide 3'.",
            "Slide 3 · GRÁTIS (com aviso): IMG_5064 (Trevi, 25/12 10:08). Legenda: 'Em dez/2024, de graça. Hoje: [regra e valor oficiais conferidos na produção] para chegar perto da bacia.'",
            "Slide 4 · GRÁTIS: IMG_5220 (Pincio, 16:37). Legenda: 'O pôr do sol mais bonito do dia 1 não custou nada.'",
            "Slide 5 · GRÁTIS: IMG_6653 (São Pedro, 27/12 08:25). Legenda: 'Entrar na basílica: grátis [conferir regra atual]. Chegamos às 8h25: fila curta.'",
            "Slide 6 · GRÁTIS, COM PEGADINHA: IMG_6650 (Sant'Ignazio, 27/12 12:31, Diego e Marina). Legenda: 'A igreja é grátis. O espelho pra ver o teto: [valor do Diego].'",
            "Slide 7 · PAGO: IMG_5108 (Panteão, 25/12 10:50). Legenda: 'Em 2024: [valor do Diego]. Hoje: [valor oficial conferido na produção].'",
            "Slide 8 · PAGO: IMG_6651 (Coliseu por fora, 26/12 08:52). Legenda: 'Coliseu com arena: [valor do Diego]. Inclui Fórum e Palatino.'",
            "Slide 9 · PAGO: vila de Natal, vista ampla (foto do slide 08 do carrossel de 06/10). Legenda: 'Vila de Natal da Villa Borghese (só no Natal): [valor do Diego].'",
            "Slide 10 · PAGO (papel): passe de transporte de 72 h. Legenda: '[valor do Diego] por pessoa. [Diego: valeu a pena? sim/não e por quê]'.",
            "Slide 11 · Recibo (papel): 'Pago por pessoa: [valor do Diego] · Grátis: 9 lugares · Cotação: [data e valor da cotação]'.",
            "Slide 12 · Encerramento: Placa `SALVA PRA VIAGEM →` + símbolo 1º."],
        tela='Slides acima.', nar='Não se aplica (carrossel).',
        leg=("Roma: o que foi de graça e o que foi pago. 🇮🇹\n\n"
             "Nos 3 dias em Roma (dezembro de 2024), 9 lugares não custaram nada: Trevi, Navona, Piazza di Spagna, Popolo, Pincio, "
             "São Pedro, a igreja de Sant'Ignazio, o Gianicolo e a Ponte Sant'Angelo.\n\n"
             "Pagamos: Coliseu com Fórum e Palatino, Panteão, a vila de Natal, o espelho de Sant'Ignazio e o passe de 72 h. "
             "Total pago por pessoa: [valor do Diego].\n\n"
             "O que mudou desde a nossa viagem: [regra atual da Fontana di Trevi e do Panteão, conferida na fonte oficial no dia da postagem].\n\n"
             "Cotação: [valor e data].\n\nSalva pra sua viagem a Roma!"),
        cta='Salva pra viagem (salvamento).', capa='Pincio ao pôr do sol + “ROMA: DE GRAÇA × PAGO”.',
        som='Música instrumental da biblioteca do Instagram (decisão do Diego para carrossel, 05/10/2026).',
        hip='Separar grátis × pago é mais salvável que o custo total já publicado em 06/10, porque responde “o que dá pra fazer sem pagar”.',
        met='Salvamentos por alcance',
        mat=['Fotos de Roma do repositório (EXIF em carrosseis/roma-3-dias/rev1/QA_REV1.md): IMG_5220 (Pincio 25/12 16:37), IMG_5064 (Trevi 25/12 10:08), '
             'IMG_6653 (São Pedro 27/12 08:25), IMG_6650 (Sant\'Ignazio 27/12 12:31), IMG_5108 (Panteão 25/12 10:50), IMG_6651 (Coliseu 26/12 08:52), vila de Natal (vista ampla)',
             'Registro de custos de Roma: planejamento/ESTUDO_CARROSSEL_ROMA.md, seção 4 (por pessoa, dez/2024). Os valores entram só depois da confirmação do Diego nesta produção'],
        pend=['Regras de 2026 da Fontana di Trevi e do Panteão: conferidas em 06/10/2026 (QA_REV1, “Preços de 2026”). Reconferir na fonte oficial (Turismo Roma, site do Panteão) no dia da produção e citar fonte e data',
              'Basílica de São Pedro “grátis”: conferir a regra atual em vatican.va na produção',
              'Diego confirma a lista do que foi grátis e do que foi pago (o slide 2 segue o registro de 05/10)',
              'O carrossel de 06/10 já usou estas fotos: capa e ordem diferentes para não parecer repost',
              SEM_VALOR + ' Exceção desta peça: os valores que o Diego confirmar na produção, com € e ≈ R$ e cotação datada (DS V2, 7.1 e 7.3)'],
        fonte='Repositório · fotos de Roma', trecho='IMG_5064 · IMG_5108 · IMG_5220 · IMG_6650 · IMG_6651 · IMG_6653',
        cus=dict(dados=['Valor pago por pessoa em dez/2024: Panteão; Coliseu + Fórum + Palatino com arena; vila de Natal da Villa Borghese; espelho de Sant\'Ignazio; passe de transporte de 72 h',
                        'Total pago por pessoa (soma dos 5 itens)',
                        'Confirmar que foram de graça: Trevi, Navona, Piazza di Spagna, Popolo, Pincio, Basílica de São Pedro, igreja de Sant\'Ignazio, Gianicolo, Ponte Sant\'Angelo',
                        'Cotação a usar (valor e data) para o ≈ R$',
                        'Se o passe de 72 h valeu a pena (sim/não e por quê)'],
                 escopo='Roma, 3 dias (25 a 27/12/2024), por pessoa', quando='na produção desta peça'),
        video_longo=None, tipo=None,
    ),
    'p237': dict(
        fmt='Carrossel', pilar='Quanto custa', titulo='Comida em Roma: a regra que segurou o orçamento',
        gancho='A regra da comida em Roma.', gt='Afirmação', nivel='—', prod='cus',
        obj=('Salvamento: a regra real de comida da viagem (mercado de manhã, comida de rua de dia, jantar com calma à noite), '
             'já contada na legenda do carrossel de 06/10, agora com o gasto de cada parte, fornecido pelo Diego.'),
        motiv='Quem vai à Itália e tem medo do gasto com comida. Salva a regra; manda para quem viaja junto.',
        q0='Capa: IMG_5132 (Piazza Navona, 25/12, não usada no carrossel de 06/10) com a Placa do título. Trocar por foto de comida se o Diego tiver.',
        sl=["Capa: foto IMG_5132 (Navona) ou foto de comida de Roma enviada pelo Diego + Placa `A REGRA DA COMIDA EM ROMA` e microcópia `dez/2024 · por pessoa`.",
            "Slide 2 (segunda capa, papel): a regra em 3 linhas com a Rota: '1 · de manhã: mercado · 2 · de dia: comida de rua · 3 · à noite: jantar com calma'.",
            "Slide 3 · Recibo (papel): comida e bebida por pessoa, 3 dias: cafés [valor do Diego] · mercado [valor do Diego] · almoços [valor do Diego] · "
            "sorvetes [valor do Diego] · jantares [valor do Diego] · total [valor do Diego] · '[% do total da viagem, do Diego]'.",
            "Slide 4 · Manhã, mercado (papel ou foto do Diego): 'Toda manhã, mercado: snacks e bebidas na bolsa. Água, refri e o vinho do fim de tarde não pesaram.' + '[valor do Diego] em 3 dias'.",
            "Slide 5 · Dia, comida de rua: 'De dia, comida de rua, que também mostra o melhor da culinária italiana.' + '[o que comeram, nas palavras do Diego]' + '[valor do Diego]'.",
            "Slide 6 · Noite, jantar: 'À noite, sentar e jantar com calma, gastando mais nos pratos.' + '[valor do Diego]'.",
            "Slide 7 · Contexto (papel): 'Fim de ano, 5 pessoas, dezembro de 2024. Fim de ano deixa tudo mais caro: por isso a regra.'",
            "Slide 8 · Encerramento: Placa `SALVA PRA VIAGEM →` + símbolo 1º."],
        tela='Slides acima.', nar='Não se aplica (carrossel).',
        leg=("A regra da comida em Roma. 🍝\n\n"
             "Como era fim de ano (e tudo fica mais caro), a gente criou uma regra:\n"
             "🛒 de manhã, mercado: snacks e bebidas na bolsa;\n"
             "🥙 de dia, comida de rua;\n"
             "🍷 à noite, sentar e jantar com calma.\n\n"
             "Em 3 dias, comida e bebida deram [valor do Diego] por pessoa.\n\n"
             "Cotação: [valor e data].\n\nSalva pra sua viagem à Itália!"),
        cta='Salva pra viagem (salvamento).', capa='Navona (ou foto de comida do Diego) + “A REGRA DA COMIDA EM ROMA”.',
        som='Música instrumental da biblioteca do Instagram.',
        hip='Uma regra simples com o gasto real de cada parte gera mais salvamentos que o custo total.',
        met='Salvamentos por alcance',
        mat=['IMG_5132 (Piazza Navona, 25/12/2024; não usada no carrossel de 06/10; EXIF em QA_REV1.md)',
             'A regra (mercado, comida de rua, jantar): carrosseis/roma-3-dias/rev1/LEGENDA.md',
             'Categorias do gasto (cafés, mercado, almoços, sorvetes, jantares): planejamento/ESTUDO_CARROSSEL_ROMA.md, seção 4; valores só com a confirmação do Diego'],
        pend=['Diego: há fotos de comida de Roma além das 12 do Drive? Sem elas, a peça fica com a Navona na capa e slides de papel',
              'Quadros de vídeo (ex.: IMG_5379, 26/12 19:52, possível jantar) não entram sem decisão do Diego: a regra do v6 deixa fotos da Itália para carrossel, e quadro de vídeo em carrossel não está definido',
              'Não citar prato, restaurante ou mercado sem o Diego dizer qual foi',
              'O carrossel de 06/10 já contou a regra: aqui o novo é o gasto por parte; não repetir a capa nem a estrutura',
              'Sai em 03/02/2027: a legenda fala de dez/2024; nada de “preço atual”'],
        fonte='Repositório · fotos de Roma + registro de custos', trecho='IMG_5132',
        cus=dict(dados=['Comida e bebida por pessoa, Roma, 3 dias: cafés, mercado, almoços, sorvetes, jantares (valor de cada) e o total',
                        'Percentual da comida no total da viagem a Roma (ou o total, para calcular)',
                        'O que comeram de dia (comida de rua) e onde jantaram, se quiser citar',
                        'Cotação a usar (valor e data)'],
                 escopo='Roma, 3 dias (25 a 27/12/2024), por pessoa', quando='na produção desta peça'),
        video_longo=None, tipo=None,
    ),

    # ═════════════════════════ REELS NOVOS ═════════════════════════
    'p822': dict(
        fmt='Reel', pilar='Como se mover', titulo='Chegar em Veneza com mala',
        gancho='POV: você chega em Veneza com mala.', gt='POV', nivel='B', prod='dec',
        obj=('Utilidade de chegada: o que é sair da estação de Veneza com mala, contado com a fala real do Diego em 31/12/2024 '
             '(as malas, as subidas e o combinado do apartamento). A dica final é do Diego.'),
        motiv='Quem vai a Veneza com mala grande. Manda para quem vai junto; salva para decidir onde ficar.',
        q0='Saída da estação de Veneza com as malas (IMG_5998, 31/12 10:59, GPS na estação Santa Lucia), com o gancho na tela.',
        sc=[('0–2 s', 'Gancho', 'IMG_5998 (31/12 10:59, 49 s; GPS na estação Santa Lucia), trecho 0–2 s do arquivo + gancho escrito, Legenda Padrão.'),
            ('2–5 s', 'Contexto', 'IMG_5998, trecho 2–5 s (fala “ai, Veneza”, se o áudio confirmar). Legenda Informação `VENEZA · 31/12 · 10:59`.'),
            ('5–12 s', 'O perrengue', 'IMG_5999 (11:05, 19,5 s; GPS junto à Ponte degli Scalzi), trecho 4,4–12,2 s: fala “subi… 90% do caminho com duas malas na mão… perrengue chique”. '
                                       'Carimbo PERRENGUE no fim do trecho, só se o áudio confirmar e as malas aparecerem.'),
            ('12–18 s', 'O combinado', 'IMG_6004 (11:47, 29,5 s), trecho 0,7–14,2 s: fala sobre o apartamento perto da estação “pra não andar com a mala”. Legenda Padrão com a fala, só depois de ouvir.'),
            ('18–21 s', 'Dica', 'IMG_6004, trecho 17–20 s (fala “ai, Veneza”) + Bilhete com a dica do Diego: “[dica confirmada pelo Diego]”.')],
        tela='pov: você chega em veneza com mala. · veneza · 31/12 · 10:59 · [fala das malas] · [dica do Diego]',
        nar='Falas dos brutos (IMG_5998, IMG_5999, IMG_6004), só depois de ouvir. Sem narração nova.',
        leg=("POV: você chega em Veneza com mala. 🧳\n\n"
             "31/12/2024, 10h59, estação de Veneza. Daqui pra frente é a pé, com ponte de degrau no caminho.\n\n"
             "[Dica do Diego: onde ficar / o que fazer com a mala.]\n\n"
             "Manda pra quem vai pra Veneza com você."),
        cta='Manda pra quem vai pra Veneza com você (envio).', capa='Malas na saída da estação + “VENEZA COM MALA”.',
        som='Áudio original das falas + música calma da biblioteca baixa.',
        hip='Perrengue real com uma dica prática gera envios para quem vai viajar junto.', met='Envios por alcance',
        mat=['Veneza, 31/12/2024: IMG_5998 (10:59, 49,2 s, GPS 45,4411 · 12,3211, estação), IMG_5999 (11:05, 19,5 s), IMG_6001 (11:44, 10,8 s), '
             'IMG_6004 (11:47, 29,5 s), IMG_6007 (11:57, 9,8 s): vistos pelo Diego na folha (ruelas e ponte)',
             'Contexto: IMG_6234 (01/01 19:00, 38 s), fala sobre Cannaregio, “perto da estação”, “5 minutos” (não usar sem ouvir)'],
        pend=[OUVIR, FAM + ' Em IMG_6001 e IMG_6007 aparecem familiares (“vira aí, mãe”): fora, salvo autorização',
              'Diego conta onde deixaram as malas e onde dormiram em 31/12 e 01/01 (IMG_6004 fala do apartamento perto da estação; IMG_6234, de 01/01, fala de Cannaregio): a dica final sai daí',
              '“Ponte de degrau” e “a pé” na legenda são fatos gerais de Veneza: confirmar antes de publicar',
              'Carimbo PERRENGUE só se aconteceu (DS V2): depende do áudio de IMG_5999',
              SEM_VALOR, D1],
        fonte='Drive · Itália (Veneza)', trecho='IMG_5998–6007',
        cus=None, video_longo=None, tipo=None,
        tt=dict(gancho='Chegar em Veneza com duas malas', muda='Mesmo corte, fala original mais alta e legenda grande; pergunta final: “você levaria mala grande?”.'),
        yt=dict(titulo='Chegar em Veneza com mala: como foi', muda='Mesmo corte; descrição com a dica do Diego.'),
    ),
    'p840': dict(
        fmt='Reel', pilar='Vontade de ir', titulo='O pôr do sol de Florença',
        gancho='Florença, 17h04. Olha esse céu.', gt='Afirmação', nivel='B', prod='dec',
        obj='Desejo puro, teste T2 variante A (com texto no gancho): o pôr do sol de 29/12/2024 visto da beira do Arno, com a hora real do arquivo.',
        motiv='Quem sonha com a Itália. Manda para quem iria junto; salva como destino.',
        q0='Céu do pôr do sol em Florença (IMG_5808, 29/12 17:04), com o gancho escrito nos 2 primeiros segundos.',
        sc=[('0–2 s', 'Gancho', 'IMG_5808 (29/12 17:04, 17 s; GPS à beira do Arno, perto da Ponte Santa Trinita), trecho 0–2 s + gancho escrito, Legenda Padrão (T2, A).'),
            ('2–5 s', 'Fala', 'IMG_5808, trecho 2–5 s: fala “estou vendo aqui o pôr do sol com essa vista maravilhosa”, se o áudio confirmar; se não, só imagem.'),
            ('5–9 s', 'Desejo', 'IMG_5810 (17:07, 11,3 s), trecho 2–6 s. Legenda Informação `FLORENÇA · 29/12 · 17:07`.'),
            ('9–13 s', 'Pico', 'IMG_5812 (17:08, 46 s, 1080 × 1920), trecho 10–14 s, sem fala. Bilhete: “29/12, 17h08.”'),
            ('13–15 s', 'Loop', 'Volta a IMG_5808, trecho 0–2 s.')],
        tela='florença, 17h04. olha esse céu. · florença · 29/12 · 17:07 · 29/12, 17h08.',
        nar='Fala de IMG_5808 (0–5 s), só se o áudio confirmar. Sem narração nova.',
        leg=("Florença, 17h04. Olha esse céu. 🌅\n\n"
             "Pôr do sol de 29 de dezembro de 2024, na beira do Arno.\n\n"
             "Manda pra quem veria esse pôr do sol com você."),
        cta='Manda pra quem veria esse pôr do sol com você (envio).', capa='Céu do pôr do sol + “FLORENÇA, 17H04”.',
        som='Ambiente + música calma da biblioteca.',
        hip='Texto curto com a hora no gancho segura mais que o mesmo plano sem texto (T2, A).',
        met='Seguidores por 1.000 visualizações e % de não seguidores',
        mat=['Florença, 29/12/2024: IMG_5808 (17:04, 17 s), IMG_5809 (17:05, 6,3 s), IMG_5810 (17:07, 11,3 s), IMG_5811 (17:08, 10,7 s), '
             'IMG_5812 (17:08, 46 s, 1080 × 1920), IMG_5813 e 5814 (17:19). GPS de todos entre 43,7686 · 11,2498 e 43,7694 · 11,2501 (beira do Arno)'],
        pend=[GPS + ' Não citar “Ponte Santa Trinita” na tela sem confirmar no quadro',
              'IMG_5811 tem fala com nome de outra pessoa (“Gabriel, ela canta?”): usar sem o áudio', OUVIR, FAM,
              'T2, variante A: manter iguais duração, horário e tipo de cena em relação à variante B', D1],
        fonte='Drive · Itália (Florença)', trecho='IMG_5808–5812',
        cus=None, video_longo=None, tipo=None,
        tt=dict(gancho='Pôr do sol em Florença, 17h04', muda='Mesmo corte, sem Bilhete; som em alta do TikTok, instrumental.'),
        yt=dict(titulo='Pôr do sol em Florença (17h04, dezembro)', muda='Mesmo corte, com o título no primeiro quadro.'),
    ),
    'p842': dict(
        fmt='Reel', pilar='Vontade de ir', titulo='A caminho da Ponte Vecchio',
        gancho='Estamos indo pra Ponte Vecchio.', gt='POV', nivel='B', prod='dec',
        obj='Desejo em movimento: a caminhada real até a Ponte Vecchio e a travessia, em 29/12/2024 (14:51 a 15:09), com a fala do Diego anunciando o destino.',
        motiv='Quem vai a Florença. Manda para quem atravessaria a ponte junto.',
        q0='A rua a caminho da ponte (IMG_5687, 29/12 14:51), com a fala “estamos indo para a Ponte Vecchio” e o gancho escrito.',
        sc=[('0–2 s', 'Gancho', 'IMG_5687 (29/12 14:51, 20,9 s; GPS perto da Piazza della Signoria), trecho 5,0–7,0 s: fala “estamos indo para a Ponte Vecchio” + gancho escrito.'),
            ('2–6 s', 'Caminho', 'IMG_5687, trecho 9–13 s (sem a fala “chegou minha…”, que não se entende). Legenda Informação `FLORENÇA · 29/12 · 14:51`.'),
            ('6–10 s', 'Chegada', 'IMG_5688 (14:54, 14,1 s; GPS na cabeceira norte da Ponte Vecchio), trecho 0–4 s.'),
            ('10–14 s', 'Travessia', 'IMG_5718 (15:08, 28,1 s; GPS já do outro lado do rio) trecho 4–8 s, ou IMG_5719 (15:09, 34,5 s) se o quadro for melhor.'),
            ('14–16 s', 'Fecho', 'Bilhete: “ponte vecchio, 14h54.” sobre o último plano; loop para o quadro 0.')],
        tela='estamos indo pra ponte vecchio. · florença · 29/12 · 14:51 · ponte vecchio, 14h54.',
        nar='Fala de IMG_5687 (5,0–7,0 s), só se o áudio confirmar.',
        leg=("Estamos indo pra Ponte Vecchio. 🇮🇹\n\n"
             "Florença, 29 de dezembro de 2024: 14h51 a caminho, 14h54 na ponte.\n\n"
             "Manda pra quem atravessaria essa ponte com você."),
        cta='Manda pra quem atravessaria essa ponte com você (envio).', capa='Ponte Vecchio + “14H54”.',
        som='Ambiente + música calma da biblioteca.',
        hip='POV de caminhada com o destino anunciado prende até a chegada (retenção).', met='Retenção média e envios por alcance',
        mat=['Florença, 29/12/2024: IMG_5680 (14:39, 24,6 s), IMG_5681 (14:44, 30,3 s), IMG_5683 (14:46), IMG_5687 (14:51, 20,9 s), '
             'IMG_5688 (14:54, 14,1 s), IMG_5717 a 5719 (15:08–15:09, 2,4 / 28,1 / 34,5 s)'],
        pend=[OUVIR + ' A transcrição diz “ponte veca”',
              GPS + ' IMG_5688 (43,7683 · 11,2537) é a cabeceira norte da ponte; IMG_5718–5719 (43,7669–43,7662) ficam do outro lado',
              FAM, 'Florença tem p840 em 16/02: cenas e gancho diferentes (aqui é dia, caminhada)', D1],
        fonte='Drive · Itália (Florença)', trecho='IMG_5680–5719',
        cus=None, video_longo=None, tipo=None,
        tt=dict(gancho='Indo pra Ponte Vecchio', muda='Mesmo corte; texto maior; pergunta: “já atravessou essa ponte?”.'),
        yt=dict(titulo='A caminho da Ponte Vecchio, em Florença', muda='Mesmo corte.'),
    ),
}


# ═════════════════════════ REVISÕES: Reels de Roma de foto → vídeo ═════════════════════════
REVISOES = {
    'p205': dict(
        titulo='Roma tem dois pores do sol perfeitos', gancho='Pincio 16h36. Gianicolo 16h29.', gt='Afirmação', nivel='B', prod='dec',
        obj=('Desejo com utilidade leve: dois mirantes de pôr do sol em Roma, agora em VÍDEO, com a hora real do arquivo '
             '(Pincio 25/12 16:36; Gianicolo 27/12 16:29). Troca as fotos IMG_5220 e IMG_5523 pelos vídeos dos mesmos fins de tarde.'),
        motiv='Quem sonha com Roma e quem planeja a viagem. Envia para quem iria junto; salva os dois lugares.',
        q0='Pôr do sol no Pincio (IMG_5215, 25/12 16:36), com o gancho escrito.',
        sc=[('0–2 s', 'Gancho', 'IMG_5215 (25/12 16:36, 25 s; GPS na Terrazza del Pincio), trecho 0–2 s + gancho escrito, Legenda Padrão, Destaque em “16h36”.'),
            ('2–5 s', 'Pincio', 'IMG_5215, trecho 8–11 s. Legenda Informação `PINCIO · 25/12 · 16:36`.'),
            ('5–8 s', 'Muda o dia', 'IMG_5508 (27/12 15:40, 21,3 s; GPS no Gianicolo), trecho 0–3 s, sem a fala (ela começa em 9,2 s).'),
            ('8–12 s', 'Gianicolo', 'IMG_5519 (27/12 16:29, 17,6 s; GPS no Gianicolo), trecho 2–6 s. Legenda Informação `GIANICOLO · 27/12 · 16:29`.'),
            ('12–14 s', 'Dica', 'IMG_5519, trecho 10–12 s + Bilhete: “chegue antes das 16h30.” (só depois de conferir a hora do pôr do sol).'),
            ('14–15 s', 'Loop', 'Volta a IMG_5215, trecho 0–1 s.')],
        tela='pincio 16h36. gianicolo 16h29. · pincio · 25/12 · 16:36 · gianicolo · 27/12 · 16:29 · chegue antes das 16h30.',
        nar='Sem narração. Plano B do trecho 8–12 s: IMG_5508, 12,7–16,3 s, com a fala “coisa linda… Hello Roma!” (só depois de ouvir).',
        leg=("Dois pores do sol em Roma. 🌅\n\n"
             "1. Terrazza del Pincio, em cima da Piazza del Popolo: 16h36 do dia 25 de dezembro.\n"
             "2. Gianicolo, no alto de Trastevere: 16h29 do dia 27.\n\n"
             "Em dezembro o sol se põe cedo em Roma ([hora conferida no timeanddate]): chegue antes das 16h30.\n\n"
             "Manda pra quem vai ver o pôr do sol com você em Roma."),
        cta='Manda pra quem vai ver o pôr do sol com você (envio).', capa='Céu do Pincio (IMG_5215) + “16H36 EM ROMA”.',
        som='Música instrumental da biblioteca (sem letra). Sem efeitos sonoros.',
        hip='Desejo com 1 informação útil (a hora) converte mais que desejo puro (T1, B).', met='Envios por alcance e seguidores por 1.000 visualizações',
        mat=['Pincio, 25/12/2024 (GPS 41,9110–41,9114 · 12,4779–12,4796, altitude 40–52 m): IMG_5205 (15:58, 17 s), IMG_5206 (15:59, 10,9 s, 1080p), IMG_5213 (16:05, 24,5 s), IMG_5215 (16:36, 25 s)',
             'Gianicolo, 27/12/2024 (GPS 41,8918–41,8926 · 12,4606–12,4609, altitude 68–83 m): IMG_5508 (15:40, 21,3 s), IMG_5519 (16:29, 17,6 s). '
             'IMG_5537 (17:50) tem fala com valor e IMG_5540 (18:01) tem familiares: fora'],
        pend=['URGENTE (sai em 18/10): abrir a folha de contato de IMG_5205–5215 e IMG_5508–5519 hoje. ' + GPS_ROMA,
              'Plano B se IMG_5215 não mostrar o sol: IMG_5213 (16:05), trecho 0–3 s. Se IMG_5519 não mostrar o céu: IMG_5508, 12,7–16,3 s',
              'Conferir o horário do pôr do sol em Roma em 25–27/12 (timeanddate) antes de publicar a dica das 16h30; se o pôr do sol for depois das 16h40, a dica fica; se não, trocar a hora',
              FAM, D1],
        fonte='Drive · Itália (Roma)', trecho='IMG_5205–5215 · IMG_5508–5519',
    ),
    'p222': dict(
        titulo='Expectativa em Roma: o monumento em obra', gancho='Expectativa: Roma. Realidade: tudo em obra.', gt='Expectativa × realidade',
        pilar='Como foi de verdade', nivel='B', prod='dec',
        obj=('Conceito trocado: o teto de Sant\'Ignazio não tem vídeo com GPS na igreja (só as fotos IMG_6650, que ficam para carrossel). '
             'O vídeo sustenta outro momento real: em 26/12/2024, no Vittoriano e na Coluna de Trajano, o Diego grava “perrengue chique… tudo em obra”. '
             'Humor e identificação, com o contraste do Fórum na mesma tarde.'),
        motiv='Quem já viajou e pegou um monumento em reforma. Manda para quem vai a Roma; comenta o próprio perrengue.',
        q0='O Fórum Romano (IMG_5312, 26/12 13:13), com “expectativa:” na tela.',
        sc=[('0–3 s', 'Expectativa', 'IMG_5312 (26/12 13:13, 15,8 s; GPS no Fórum Romano), trecho 0–3 s + gancho escrito, Legenda Padrão, Destaque em “expectativa”.'),
            ('3–9 s', 'Realidade', 'IMG_5343 (26/12 14:48, 21,8 s; GPS entre o Vittoriano e a Coluna de Trajano), trecho 0,1–5,4 s: fala “é galera, um dia aqui no perrengue chique… monumento de Vittorio Emanuele”.'),
            ('9–14 s', 'Pico', 'IMG_5343, trecho 5,4–10,5 s: fala “tudo em obra, coluna de Trajano… em obra”. Carimbo PERRENGUE (aconteceu: obra no quadro, a conferir).'),
            ('14–16 s', 'Loop', 'Legenda Padrão “roma, dezembro de 2024.” e volta ao Fórum (IMG_5312, 0–1 s).')],
        tela='expectativa: roma. realidade: tudo em obra. · [fala do Diego] · roma, dezembro de 2024.',
        nar='Fala de IMG_5343 (0,1–10,5 s), só depois de ouvir. Sem narração nova.',
        leg=("Expectativa: Roma. Realidade: tudo em obra. 🚧\n\n"
             "26 de dezembro de 2024: Vittoriano e Coluna de Trajano em reforma no dia em que a gente passou. Perrengue chique.\n\n"
             "Qual foi o monumento que te recebeu em obra? Conta aqui."),
        cta='Conta nos comentários qual monumento te recebeu em obra (comentário).', capa='Monumento com tapume + “EM OBRA”.',
        som='Áudio original da fala + música da biblioteca baixa. *tum* do Carimbo quando o som existir.',
        hip='Perrengue real e engraçado gera comentários de identificação e envios.', met='Comentários e envios por alcance',
        mat=['IMG_5343 (26/12/2024 14:48, 21,8 s, GPS 41,8956 · 12,4834)', 'IMG_5312 (26/12/2024 13:13, 15,8 s, Fórum Romano, GPS 41,8922 · 12,4858)',
             'Alternativa de expectativa: IMG_5310 (13:12, 16,1 s, 1080p, fala “velho, é muito grande”)'],
        pend=[GPS_ROMA + ' A peça depende de a obra aparecer no quadro de IMG_5343 (tapume, andaime)', OUVIR,
              'Não dizer que o monumento continua em obra hoje: a legenda é datada (dez/2024)',
              'Plano B (conceito original): a exportação 295537DD-…mp4 (21,9 s, sem GPS, data de exportação 27/12) tem a fala “estamos na igreja… vai tirar uma foto aqui, aí tem que pegar uma fila”. '
              'Se a folha mostrar o teto de Sant\'Ignazio, o Diego pode escolher voltar ao “Essa cúpula não existe.” com esse vídeo',
              'Mudança de eixo no plano v6: de “pop ins” para “pop exp” (aplicar_v6)', FAM, D1],
        fonte='Drive · Itália (Roma)', trecho='IMG_5312 · IMG_5343',
    ),
    'p242': dict(
        titulo='Roma iluminada no Natal', gancho='Natal em Roma é assim.', gt='Afirmação', nivel='B', prod='dec',
        obj='Desejo sazonal em VÍDEO: a vila de Natal da Villa Borghese na noite de 25/12/2024 e o centro à noite em 26/12, publicado perto do Natal.',
        motiv='Quem sonha com Natal na Europa; casais e famílias. Envia para quem passaria o Natal junto.',
        q0='A vila de Natal iluminada (IMG_5234, 25/12 18:04), com o gancho escrito.',
        sc=[('0–2 s', 'Gancho', 'IMG_5234 (25/12 18:04, 23,9 s; GPS na Villa Borghese, área da vila de Natal), trecho 0–2 s + gancho escrito.'),
            ('2–5 s', 'Desejo', 'IMG_5227 (16:58, 28,6 s), trecho 10–13 s: a vila ao anoitecer.'),
            ('5–8 s', 'Desejo', 'IMG_5230 (17:02, 19 s), trecho 5–8 s.'),
            ('8–11 s', 'Pico', 'IMG_5240 (18:10, 8,1 s), trecho 0–3 s + Bilhete: “25/12/2024.”'),
            ('11–14 s', 'Centro', 'IMG_5376 (26/12 18:35, 29,6 s; GPS no centro, região da Via del Corso), trecho 0–3 s, só se as luzes aparecerem no quadro.'),
            ('14–15 s', 'Loop', 'Volta a IMG_5234, trecho 0–1 s.')],
        tela='natal em roma é assim. · 25/12/2024',
        nar='Sem narração.',
        leg=("Natal em Roma é assim. 🎄\n\n"
             "A vila de Natal da Villa Borghese na noite de 25 de dezembro de 2024 e as ruas do centro no dia seguinte.\n\n"
             "Manda pra quem passaria o Natal em Roma com você."),
        cta='Manda pra quem passaria o Natal em Roma com você (envio).', capa='Vila de Natal iluminada + “NATAL EM ROMA”.',
        som='Música instrumental da biblioteca, clima de fim de ano (sem música natalina com direitos fora da biblioteca).',
        hip='Desejo sazonal com a data real gera envios no começo das festas (T1, B).', met='Envios por alcance e seguidores por 1.000 visualizações',
        mat=['Villa Borghese, 25/12/2024 (GPS 41,9103–41,9114 · 12,4844–12,4874): IMG_5226 (16:56, 9,2 s), IMG_5227 (16:58, 28,6 s), IMG_5230 (17:02, 19 s), '
             'IMG_5234 (18:04, 23,9 s), IMG_5240 (18:10, 8,1 s). IMG_5233 (17:51) tem fala com familiar: fora',
             'Centro, 26/12/2024: IMG_5376 (18:35, 29,6 s, GPS 41,9075 · 12,4777)'],
        pend=[GPS_ROMA, 'A vila de Natal é a mesma do slide 08 do carrossel de 06/10 (QA_REV1): confirmar no quadro',
              'Não dizer que a vila acontece em 2026 (a legenda fala de 2024)',
              'p254 (24/12) também passa pela Villa Borghese: usa IMG_5226; este Reel usa os outros arquivos', FAM, D1],
        fonte='Drive · Itália (Roma)', trecho='IMG_5227–5240 · IMG_5376',
    ),
    'p254': dict(
        titulo='Nosso primeiro dia em Roma foi no Natal', gancho='Primeiro dia em Roma: no Natal.', gt='Afirmação', nivel='B', prod='cus',
        obj=('Série e conversão no dia mais simbólico do ano, agora em VÍDEO: o dia 25/12/2024 inteiro, em ordem, com a hora de cada arquivo '
             '(Trevi 10:09 → Panteão 10:50 → Navona 11:20 → Ponte Sisto 12:18 → Popolo 15:11 → Pincio 16:05 → vila de Natal 16:56) e o Placar.'),
        motiv='Quem acompanha o perfil e quem sonha com Natal na Europa. Segue pela série; envia para a família.',
        q0='Fontana di Trevi na manhã de Natal (IMG_5067, 25/12 10:09) com a Placa `PRIMEIRO DIA EM / ROMA` (Chegada).',
        sc=[('0–2 s', 'Gancho', 'IMG_5067 (25/12 10:09, 12,8 s; GPS na Fontana di Trevi), trecho 0–2 s + Placa `PRIMEIRO DIA EM / ROMA` com a Chegada + gancho, Destaque em “Natal”.'),
            ('2 s até o fecho', 'Placar', 'Placar: aguardando dados do Diego (hora de chegada e gastos do dia 1, item a item com a hora). Painel `+HH:MM · € 0,00` em x 72 · y 256.'),
            ('2–4 s', 'Trevi', 'IMG_5071 (10:13, 13,5 s), trecho 4–6 s. Legenda Informação `10:09 · TREVI`.'),
            ('4–6 s', 'Panteão', 'IMG_5110 (10:50, 6,8 s; GPS na Piazza della Rotonda), trecho 0,6–2,6 s; fala “não dá pra ter dimensão, mas isso aqui é muito grande” se o áudio confirmar. `10:50 · PANTEÃO`.'),
            ('6–8 s', 'Navona', 'IMG_5133 (11:20, 13,1 s; GPS na Piazza Navona), trecho 2–4 s, sem a fala. `11:20 · NAVONA`.'),
            ('8–10 s', 'Ponte Sisto', 'IMG_5151 (12:18, 17 s; GPS na Ponte Sisto), trecho 0–2 s. `12:18 · PONTE SISTO`.'),
            ('10–12 s', 'Popolo', 'IMG_5195 (15:11, 6,1 s; GPS na Piazza del Popolo), trecho 0–2 s. `15:11 · POPOLO`.'),
            ('12–14 s', 'Pincio', 'IMG_5213 (16:05, 24,5 s; GPS na Terrazza del Pincio), trecho 4–6 s. `16:05 · PINCIO`. (IMG_5215 fica para o p205.)'),
            ('14–17 s', 'Pico', 'IMG_5226 (16:56, 9,2 s; GPS na vila de Natal da Villa Borghese), trecho 0–3 s. Legenda Emocional: “um natal DIFERENTE”.'),
            ('17–20 s', 'Fechamento', 'Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + 1º + bordão. Legenda: “feliz natal.”')],
        tela='primeiro dia em roma: no natal. · 10:09 trevi · 10:50 panteão · 11:20 navona · 12:18 ponte sisto · 15:11 popolo · 16:05 pincio · um natal diferente · e isso foi só o primeiro dia.',
        nar='Fala de IMG_5110 (Panteão), se o áudio confirmar. Opcional: o Diego grava o bordão “E isso foi só o primeiro dia.” (3 s), registrado como material futuro.',
        leg=("Nosso primeiro dia em Roma foi no Natal. 🎄\n\n"
             "25 de dezembro de 2024: Trevi às 10h09, Panteão às 10h50, Navona, Ponte Sisto, Piazza del Popolo, o Pincio e a vila de Natal da Villa Borghese.\n\n"
             "Gasto do dia: [valor do Diego] por pessoa.\n\n"
             "Feliz Natal! Sou o Diego e aqui eu mostro o primeiro dia em cada cidade. Segue pra ver os próximos."),
        cta='Segue pra ver os próximos primeiros dias (seguir).', capa='Trevi com a placa + “1º DIA: NATAL”.',
        som='Música instrumental de clima natalino da biblioteca do Instagram.',
        hip='Data simbólica + série + Placar real aumentam seguidores (T3, A).', met='Seguidores por 1.000 visualizações',
        mat=['Roma, 25/12/2024 (GPS de cada arquivo em acervo/italia/indice.tsv): IMG_5058–5062 (08:44–09:02, rua perto do Coliseu), IMG_5067/5071–5073 (10:09–10:14, Trevi), '
             'IMG_5098–5104 (10:37–10:45, entre Trevi e Panteão), IMG_5110/5111/5115 (10:50–10:54, Panteão), IMG_5133/5137 (11:20–11:32, Navona), IMG_5151 (12:18, Ponte Sisto), '
             'IMG_5195/5196 (15:11–15:47, Popolo), IMG_5205–5215 (15:58–16:36, Pincio), IMG_5226–5240 (16:56–18:10, Villa Borghese)',
             'Exportação b73fb8d3….mov (fala sobre batedor de carteira): sem GPS, data de exportação; fora desta peça'],
        pend=[GPS_ROMA,
              'Placar: Roma tem registro por pessoa da viagem (ESTUDO_CARROSSEL_ROMA.md, seção 4, com um total por dia sem hora por item), mas não item a item com a hora. Sem esse registro, não há Placar: Diego fornece na produção ou a peça sai sem Placar (decisão dele)',
              'Hora de chegada: hotel de 4 noites (24 a 28/12) e o GPS de IMG_5020 está na Estação Central de Milão às 16:24 de 24/12. A chegada a Roma foi na noite de 24/12? Diego define a hora zero do Placar',
              'Placa `PRIMEIRO DIA EM / ROMA`: 25/12 é o primeiro dia inteiro em Roma (QA_REV1: dia 1 = 25/12). Confirmar com o Diego',
              OUVIR, FAM, SEM_VALOR + ' (exceto o Placar e a linha de gasto da legenda, com os dados do Diego)',
              'Publicar na véspera (24/12, 12h30)', D1],
        fonte='Drive · Itália (Roma)', trecho='IMG_5067–5226 (25/12/2024)',
        cus=dict(dados=['Hora de chegada a Roma (24/12 à noite ou outra)', 'Gastos do dia 25/12/2024 item a item, com a hora de cada um (inclui Panteão e vila de Natal, que foram pagos)',
                        'Confirmar se os valores são por pessoa', 'Cotação a usar (valor e data)'],
                 escopo='Roma, dia 1 (25/12/2024), por pessoa', quando='na produção desta peça'),
    ),
    'p615': dict(
        titulo='Roma antes das 9 da manhã', gancho='Roma às 8h22.', gt='Afirmação', nivel='B', prod='dec',
        obj='Desejo com 1 informação (o horário), agora em VÍDEO: Praça São Pedro às 8h22 (27/12) e o caminho do Coliseu às 8h49 (26/12), contra o Fórum às 13h36.',
        motiv='Quem vai a Roma e odeia multidão. Salva a dica do horário; envia para quem iria.',
        q0='Praça São Pedro às 8h22 (IMG_5387, 27/12), com “08h22” na tela.',
        sc=[('0–3 s', 'Gancho', 'IMG_5387 (27/12 08:22, 11 s; GPS na Praça São Pedro), trecho 0–3 s + gancho escrito. Legenda Informação `08:22`.'),
            ('3–6 s', 'São Pedro', 'IMG_5392 (08:25, 5,6 s), trecho 0–3 s. `SÃO PEDRO · 08:25`.'),
            ('6–10 s', 'Coliseu', 'IMG_5252 (26/12 08:49, 15,4 s; GPS a caminho do Coliseu), trecho 8–12 s; depois IMG_5255 (08:54, 30,2 s), trecho 0–2 s (fala “as redondezas do Coliseu…”, se o áudio confirmar). `COLISEU · 08:54`.'),
            ('10–13 s', 'Contraste', 'IMG_5315 (26/12 13:36, 31,9 s; GPS no Fórum Romano), trecho 0–3 s, só se o quadro mostrar mais gente. `FÓRUM · 13:36`.'),
            ('13–15 s', 'Fecho', 'Bilhete: “vai cedo.”')],
        tela='roma às 8h22. · são pedro · 08:25 · coliseu · 08:54 · fórum · 13:36 · vai cedo.',
        nar='Sem narração (fala de IMG_5255 opcional, depois de ouvir).',
        leg=("Roma às 8h22. 🇮🇹\n\n"
             "A Praça São Pedro e o caminho do Coliseu antes das 9 da manhã, no fim de dezembro de 2024. Às 13h36, no Fórum, já era outra história.\n\n"
             "Salva a dica: em Roma, vai cedo."),
        cta='Salva pra sua viagem a Roma (salvamento).', capa='Praça São Pedro de manhã + “8H22”.',
        som='Música calma da biblioteca.',
        hip='Horário real como informação (T1, A) gera salvamento e seguidores.', met='Seguidores por 1.000 visualizações',
        mat=['São Pedro, 27/12/2024: IMG_5386 (08:20, sem GPS), IMG_5387 (08:22, 11 s, GPS 41,9015 · 12,4567), IMG_5392 (08:25, 5,6 s), IMG_5401 (08:45, 37,2 s, GPS dentro da basílica), IMG_5404 e 5407 (08:48–08:51, sem GPS)',
             'Coliseu, 26/12/2024: IMG_5251 (08:46, 40,1 s), IMG_5252 (08:49, 15,4 s), IMG_5255 (08:54, 30,2 s), IMG_5260–5261 (09:16–09:20)',
             'Fórum, 26/12/2024: IMG_5310–5334 (13:12–13:57)', 'Alternativa: 25/12 08:59–09:02, IMG_5060–5062 (rua perto do Coliseu, fala “running club”)'],
        pend=[GPS_ROMA, 'O contraste depende de o Fórum aparecer mais cheio no quadro; plano B: fechar no Coliseu às 08:54 e cortar a cena das 13:36',
              'IMG_5401 (dentro da basílica) tem fala de outras pessoas: fora', OUVIR, FAM, D1],
        fonte='Drive · Itália (Roma)', trecho='IMG_5387–5392 · IMG_5252–5255 · IMG_5315',
    ),
}


# ═════════════════════════ TIKTOK (sexta, 19h) ═════════════════════════
TIKTOK = {
    'tk06': dict(
        titulo='Não tem lugar no trem', gancho='Não tem lugar no trem.',
        conceito='Saída de Veneza em 02/01/2025: o trem cheio e a reação real (IMG_6249, 11:05, GPS perto da estação Santa Lucia).',
        estrutura=[('0–2 s', 'IMG_6249, trecho 5,2–7,2 s: fala “não tem lugar no trem” + o gancho escrito'),
                   ('2–10 s', 'IMG_6249, trecho 15,0–24,5 s: a fala repete, a situação no vagão'),
                   ('10–14 s', 'IMG_6249, trecho 24,5–28 s (“sorri aí”), só se não mostrar rosto de terceiros sem autorização'),
                   ('14–16 s', 'Texto: “[como terminou: Diego conta]”')],
        mat=['IMG_6249 (02/01/2025 11:05, 37,9 s, GPS 45,4409 · 12,3229, perto da estação)'],
        legenda='Não tem lugar no trem. 🚆 Saindo de Veneza em 2 de janeiro. [Como terminou, nas palavras do Diego.] Já passou por isso?',
        obj='Identificação e humor com logística real; comentários.', met='Comentários e compartilhamentos',
        prod='dec', pend=[OUVIR, FAM, 'Diego: para onde ia o trem (o próximo vídeo é em Milão às 15:33) e como terminou', GPS],
    ),
    'tk07': dict(
        titulo='Formigueiro de turista', gancho='Formigueiro de turista.',
        conceito='O Duomo de Florença ao meio-dia de 28/12/2024 e a fala espontânea “formigueiro de turista” (IMG_5560).',
        estrutura=[('0–2 s', 'IMG_5560 (12:38, 11,5 s), trecho 0,8–2,9 s: fala “formigueiro de turista” + texto'),
                   ('2–7 s', 'IMG_5554 (12:32, 16,6 s), trecho 0–5 s: o Duomo de baixo para cima (visto na folha)'),
                   ('7–12 s', 'IMG_5555 (12:35, 28,4 s), trecho 16,9–18,9 s: fala “a catedral é quase do tamanho de um mar”, depois 2–5 s de praça'),
                   ('12–14 s', 'IMG_5560, trecho 3,9–4,8 s: “formigueiro” de novo (loop)')],
        mat=['Florença, 28/12/2024: IMG_5554 (12:32), IMG_5555 (12:35), IMG_5560 (12:38): vistos na folha'],
        legenda='Formigueiro de turista. 🐜 Duomo de Florença, 28 de dezembro, meio-dia. Vale ir mesmo assim? Eu digo que sim.',
        obj='Humor e identificação com um ícone; comentários.', met='Retenção e comentários',
        prod='dec', pend=[OUVIR, 'A transcrição diz “furmigueiro”: confirmar a fala', FAM + ' (IMG_5555: “dá um sorriso, meu amor”, a Marina)'],
    ),
    'tk08': dict(
        titulo='Se fosse Salvador…', gancho='Se fosse Salvador, estaria como?',
        conceito='A feira de Milão em 03/01/2025 vista por um soteropolitano (IMG_6352, 10:32): a comparação vira pergunta para os comentários.',
        estrutura=[('0–2 s', 'IMG_6352 (22 s), trecho 15,9–17,9 s: fala “se fosse Salvador, estaria como?” + texto'),
                   ('2–11 s', 'IMG_6352, trecho 0–9 s: a feira (sem fala)'),
                   ('11–15 s', 'IMG_6352, trecho 11,4–15,1 s: fala sobre a feira, se o áudio confirmar'),
                   ('15–17 s', 'Texto: “comenta: como seria em Salvador?”')],
        mat=['Milão, 03/01/2025: IMG_6352 (10:32, 22 s, GPS 45,4767 · 9,1976)'],
        legenda='Se fosse Salvador, estaria como? 😂 Uma feira em Milão, 3 de janeiro. Soteropolitano, me ajuda: como seria aí?',
        obj='Identidade (soteropolitano) e comentários.', met='Comentários por visualização',
        prod='dec', pend=[OUVIR + ' A transcrição do trecho 11,4–15,1 s é ininteligível', 'Diego: que feira era (não nomear sem confirmar)', GPS, FAM],
    ),
    'tk14': dict(
        titulo='O trem da madrugada saindo da Itália', gancho='00h20 e a gente no trem.',
        conceito='A saída da Itália na madrugada de 04/01/2025 (IMG_6370, 00:20): “quer vir pra Itália? perrengue chique”.',
        estrutura=[('0–2 s', 'IMG_6370 (19,7 s), trecho 0–2 s + texto “00h20 e a gente no trem”'),
                   ('2–8 s', 'IMG_6370, trecho 2,8–8,8 s: fala “quer vir pra Itália? … perrengue chique”'),
                   ('8–12 s', 'IMG_6370, trecho 8,8–10,8 s: fala “… estamos no trem”'),
                   ('12–15 s', 'Texto: “[para onde e por quê: Diego conta]”')],
        mat=['Milão, 04/01/2025: IMG_6370 (00:20, 19,7 s, GPS 45,4708 · 9,2068)'],
        legenda='00h20 e a gente no trem. 🚆 Último dia na Itália: [o que era, nas palavras do Diego]. Perrengue chique.',
        obj='Perrengue real e identificação; comentários.', met='Comentários e compartilhamentos',
        prod='dec', pend=[OUVIR, 'O trecho 10,8–16,8 s diz “6.50”: pode ser hora (voo?) ou valor. Se for valor, cortar (SEM_VALOR)',
                          'Diego: para onde ia o trem (aeroporto?) e de onde saiu; o GPS (45,4708 · 9,2068) não é a Estação Central', FAM],
    ),
    'tk15': dict(
        titulo='Manhã de Natal na Fontana di Trevi', gancho='Manhã de Natal na Fontana di Trevi.',
        conceito='Roma em 25/12/2024: a Fontana di Trevi às 10h09 da manhã de Natal (IMG_5067, IMG_5071–5073, GPS na fonte).',
        estrutura=[('0–2 s', 'IMG_5067 (10:09, 12,8 s), trecho 0–2 s + texto do gancho'),
                   ('2–7 s', 'IMG_5067, trecho 4–9 s'),
                   ('7–11 s', 'IMG_5071 (10:13, 13,5 s), trecho 2–6 s'),
                   ('11–14 s', 'IMG_5073 (10:14, 7,5 s), trecho 0–3 s + texto “25/12/2024, 10h09”')],
        mat=['Roma, 25/12/2024: IMG_5067 (10:09, 12,8 s), IMG_5071 (10:13, 13,5 s), IMG_5072 (10:14, 4,2 s), IMG_5073 (10:14, 7,5 s); GPS 41,9008 · 12,4833'],
        legenda='Manhã de Natal na Fontana di Trevi. 🎄 25 de dezembro de 2024, 10h09. Passaria o Natal em Roma?',
        obj='Desejo sazonal; envios e alcance fora da bolha.', met='Compartilhamentos e visualizações completas',
        prod='dec', pend=[GPS_ROMA, 'Não falar de entrada grátis ou paga (a regra da Trevi mudou em 2026)', FAM, 'Escolhido no acervo por ter 4 arquivos no mesmo lugar e a data de Natal'],
    ),
    'tk19': dict(
        titulo='Veneza no 1º dia do ano', gancho='1º de janeiro, 11h19, Veneza.',
        conceito='O Grande Canal na manhã de 01/01/2025 (IMG_6174, 11:19, visto na folha; GPS na Ponte dell\'Accademia).',
        estrutura=[('0–2 s', 'IMG_6174 (24,9 s), trecho 0–2 s + texto do gancho'),
                   ('2–8 s', 'IMG_6174, trecho 4–10 s: barco no Grande Canal'),
                   ('8–12 s', 'IMG_6165 (11:14, 17,3 s; GPS no Campo Santo Stefano), trecho 2–6 s, sem a fala'),
                   ('12–15 s', 'IMG_6174, trecho 14–17 s + texto “primeiro dia do ano.”')],
        mat=['Veneza, 01/01/2025: IMG_6174 (11:19, 24,9 s), IMG_6165 (11:14, 17,3 s), IMG_6166 (11:16, 27,8 s): vistos na folha'],
        legenda='1º de janeiro, 11h19, Veneza. 🛶 Como começou o seu ano?',
        obj='Desejo e comentários.', met='Visualizações completas e comentários',
        prod='dec', pend=['Nome da ponte (Accademia) vem do GPS: não citar sem conferir', FAM, 'IMG_6164 tem fala com possível valor: fora'],
    ),
}

SHORT_CAP = {}


# ═════════════════════════ STORIES ═════════════════════════
STORIES = {
    'sq02': dict(
        t='Florença: o primeiro dia em 5 telas',
        telas=['Tela 1 · vídeo · IMG_5554 (28/12 12:32), 0–5 s · “florença, dia 1. 12h32.”',
               'Tela 2 · vídeo · IMG_5560 (12:38), 0,8–4,8 s, com áudio · “formigueiro de turista” (só depois de ouvir)',
               'Tela 3 · vídeo · IMG_5570 (12:56), 0–5 s, sem áudio · “o duomo de perto”',
               'Tela 4 · vídeo · IMG_5573 (13:03), 0–5 s · a Marina numa rua do centro · “13h03”',
               'Tela 5 · vídeo · IMG_5572 (13:00), 0–5 s · figurinha de enquete “Florença ou Veneza?”'],
        mat=['Florença, 28/12/2024: IMG_5554, 5560, 5570, 5572, 5573 (vistos na folha)'],
        obj='Aquecer Florença (Reels em 10/01, 16/02 e 28/02) e medir interesse com a enquete.',
        pend=[OUVIR, FAM, 'IMG_5570 tem fala com nomes de bar e loja: sem áudio'],
    ),
    'sq04': dict(
        t='Roma no Natal: 5 telas + quiz',
        telas=['Tela 1 · vídeo · IMG_5067 (25/12 10:09, Trevi pelo GPS), 0–5 s · “25/12, 10h09.”',
               'Tela 2 · vídeo · IMG_5110 (10:50, Panteão pelo GPS), 0–6 s, com áudio (“isso aqui é muito grande”, depois de ouvir)',
               'Tela 3 · vídeo · IMG_5215 (16:36, Pincio pelo GPS), 0–5 s · “pôr do sol às 16h36”',
               'Tela 4 · vídeo · IMG_5234 (18:04, vila de Natal pelo GPS), 0–5 s · figurinha de quiz “O Coliseu abre no dia 25 de dezembro?” (sim / não)',
               'Tela 5 · vídeo · IMG_5255 (26/12 08:54, a caminho do Coliseu), 0–5 s · resposta do quiz “[resposta da fonte oficial]” + “por isso o nosso Coliseu foi no dia 26.”'],
        mat=['Roma, 25 e 26/12/2024: IMG_5067, IMG_5110, IMG_5215, IMG_5234, IMG_5255'],
        obj='Aquecer o Natal em Roma (p242 em 20/12 e p254 em 24/12) com interação de quiz.',
        pend=[GPS_ROMA, 'Resposta do quiz: conferir no site oficial do Coliseu (colosseo.it) na produção', OUVIR, FAM],
    ),
    'sq06': dict(
        t='Milão numa tarde: 4 telas do castelo',
        telas=['Tela 1 · vídeo · IMG_6281 (02/01 16:17), 0–5 s · “milão, 16h17.”',
               'Tela 2 · vídeo · IMG_6301 (16:29), 0–5 s · a torre atrás da fonte',
               'Tela 3 · vídeo · IMG_6302 (16:42), 0–5 s · as muralhas',
               'Tela 4 · vídeo · IMG_6318 (16:51), 0–5 s · figurinha de caixinha “o que não pode faltar em Milão?”'],
        mat=['Milão, 02/01/2025: IMG_6281, 6301, 6302, 6318 (vistos na folha)'],
        obj='Manter Milão vivo entre o p303 e o fim do ano, com caixinha de perguntas.',
        pend=['Nome “Castelo Sforzesco” só na tela depois de confirmar (o áudio não cita)', FAM],
    ),
    'sq07': dict(
        t='Veneza: 5 telas do Grande Canal + quiz',
        telas=['Tela 1 · vídeo · IMG_6016 (31/12 12:14, perto da Ponte de Rialto pelo GPS), 0–5 s · “veneza, 12h14.”',
               'Tela 2 · vídeo · IMG_6174 (01/01 11:19), 0–5 s · barco no Grande Canal',
               'Tela 3 · vídeo · IMG_6060 (31/12 12:44), 0–5 s · Praça São Marcos',
               'Tela 4 · vídeo · IMG_6062 (12:48), 0–5 s · figurinha de quiz “Quantas pontes tem Veneza?” (3 opções montadas a partir da resposta oficial)',
               'Tela 5 · vídeo · IMG_6186 (01/01 11:44, a igreja), 0–5 s · resposta: “[número e fonte oficial]”'],
        mat=['Veneza: IMG_6016 (31/12 12:14), IMG_6060 (12:44), IMG_6062 (12:48), IMG_6174 (01/01 11:19), IMG_6186 (01/01 11:44): vistos na folha'],
        obj='Aquecer Veneza (p230 em 24/01) com quiz que gera resposta e envio.',
        pend=['Resposta do quiz: número de pontes de Veneza em fonte oficial (Comune di Venezia) com data; as opções erradas só depois de ter a certa', FAM + ' (IMG_6001 e IMG_6007 ficam fora)'],
    ),
}


# ═════════════════════════ VERSÕES TIKTOK E SHORTS dos Reels italianos ═════════════════════════
TT_ADAPT = {
    'p205': dict(gancho='Dois pores do sol em Roma, com a hora', muda='Mesmo corte; gancho maior no 1º segundo; pergunta final “Pincio ou Gianicolo?”; som instrumental em alta do TikTok.'),
    'p222': dict(gancho='Expectativa: Roma. Realidade: obra.', muda='Fala original mais alta e legenda grande; pergunta “qual monumento te recebeu em obra?”.'),
    'p242': dict(gancho='Natal em Roma é assim', muda='Mesmo corte, sem Bilhete; som instrumental de fim de ano do TikTok.'),
    'p254': dict(gancho='Passei o Natal em Roma', muda='Mesmo corte; sem Placar se os dados do Diego não estiverem prontos; texto “primeiro dia em roma” maior.'),
    'p302': dict(gancho='Primeiro dia em Veneza: 10h59', muda='Mesmo corte, ritmo um pouco mais rápido; pergunta “você iria no Réveillon?”.'),
    'p259': dict(gancho='Réveillon em Veneza: 00h11', muda='Som direto dos fogos; texto “há dois anos” no fim; pergunta “onde foi o seu?”.'),
    'p301': dict(gancho='Primeiro dia em Florença: 12h32', muda='Mesmo corte; fala “é muito grande” no meio, se o áudio confirmar.'),
    'p230': dict(gancho='Veneza: sem carro, só barco', muda='Mesmo corte; gancho sem “moto” até confirmar o fato.'),
    'p303': dict(gancho='Milão em uma tarde', muda='Fala “cenário de Game of Thrones” no fim, se o áudio confirmar.'),
    'p615': dict(gancho='Roma às 8h22 da manhã', muda='Mesmo corte; texto “vai cedo” maior no fim.'),
}

YT_ADAPT = {
    'p205': dict(titulo='Dois pores do sol em Roma: Pincio e Gianicolo', muda='Mesmo corte; horários na descrição.'),
    'p222': dict(titulo='Roma em obra: expectativa × realidade', muda='Mesmo corte; data (dez/2024) na descrição.'),
    'p242': dict(titulo='Roma iluminada no Natal', muda='Mesmo corte.'),
    'p254': dict(titulo='Nosso primeiro dia em Roma foi no Natal', muda='Mesmo corte; Placar só com os dados do Diego.'),
    'p302': dict(titulo='Primeiro dia em Veneza', muda='Mesmo corte.'),
    'p259': dict(titulo='Réveillon em Veneza: os fogos da virada', muda='Mesmo corte; “virada de 2024 para 2025” na descrição.'),
    'p301': dict(titulo='Primeiro dia em Florença: o Duomo às 12h32', muda='Mesmo corte.'),
    'p230': dict(titulo='Veneza: a cidade onde o transporte é o barco', muda='Mesmo corte.'),
    'p303': dict(titulo='Milão em uma tarde: o castelo', muda='Mesmo corte; nome do castelo só depois de confirmar.'),
    'p615': dict(titulo='Roma antes das 9 da manhã', muda='Mesmo corte.'),
}
