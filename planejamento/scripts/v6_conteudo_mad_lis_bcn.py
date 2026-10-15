# -*- coding: utf-8 -*-
"""Conteúdo do calendário v6 · grupo mad_lis_bcn (Madrid, Lisboa, Barcelona).

Escrito em 15/10/2026 a partir de:
- planejamento/DECUPAGEM_MADRID.md, acervo/madrid/{indice,transcricoes}.tsv
- acervo/lisboa/{linha_do_tempo.md,indice.tsv,transcricoes.tsv}
- reels/apresentacao/analise/transcricao_palavras.tsv (master do vlog de Barcelona, 34:08)
  e planejamento/INVENTARIO_ACERVO.md
- acervo/CORTES_DE_CUSTO.md (trechos com valor falado ficam fora)

Regras aplicadas: nenhum valor tirado de fala; toda fala citada vem da transcrição automática
(ouvir antes de usar); quadros não vistos = "conferir na folha de contato" (Drive,
Youtube/analise/<cidade>/folhas/). Hora = hora do arquivo, no fuso do local
(Madrid +01:00; Lisboa +00:00 em 22 e 23/03/2026).
Formato: BRIEF.md do v6 (PECAS, REVISOES, TIKTOK, SHORT_CAP, STORIES, TT_ADAPT, YT_ADAPT).
"""

# ---------------------------------------------------------------- textos comuns
OUVIR = 'Ouvir o áudio antes de usar: toda fala citada aqui vem da transcrição automática (erra nomes e números)'
FOLHA_MAD = 'Conferir os quadros na folha de contato (Drive, Youtube/analise/Madrid/folhas/): só as folhas 01 e 02 foram vistas'
FOLHA_LIS = 'Conferir os quadros na folha de contato (Drive, Youtube/analise/Lisboa/folhas/): nenhum quadro de Lisboa foi visto por mim'
SEM_VALOR = 'Nenhum valor em € ou R$ na tela, na fala ou na legenda, exceto os do registro do Diego (acervo/CORTES_DE_CUSTO.md)'
MINUTAGEM = 'Localizar a minutagem no corte final do vlog (o Claude não tem o vlog editado: os tempos acima são do arquivo bruto)'
MASTER_BCN = ('Vlog master de Barcelona (34:08, 4K HLG 16:9, 24 fps, em reels/apresentacao/fonte/, fora do git). '
              'O B-roll do master tem trilha de violão embutida e etiquetas gráficas em alguns trechos: '
              'cena sem fala sai do bruto original')
TRANSC_BCN = 'Transcrição com tempo por palavra: reels/apresentacao/analise/transcricao_palavras.tsv'
PLACAR_TXT = ('Placar do Dia em x 72 · y 256, de 2,0 s ao fechamento: `+HH:MM · € 0,00` (hora desde a chegada e gasto '
              'do dia, com Giro a cada gasto). Placar: aguardando dados do Diego (hora de chegada e gastos do dia 1, '
              'item a item com a hora)')
PEND_PLACAR = 'Placar: aguardando dados do Diego (hora de chegada e gastos do dia 1, item a item com a hora)'
FECHO_YT = 'Placa `VÍDEO COMPLETO NO YOUTUBE →` + legenda “sábado, 11h”'


def cus_dia1(cidade, data, extra=None):
    d = ['Hora de chegada em ' + cidade + ' no dia 1 (' + data + '), para o +HH:MM do Placar',
         'Gastos do dia 1, item a item, com a hora de cada um (o que foi, quanto, em €)',
         'Se o gasto é por pessoa ou do casal (vai escrito na tela)',
         'Cotação usada, se a legenda converter para R$ (com a data da cotação)']
    if extra:
        d += extra
    return dict(dados=d, escopo=cidade + ', dia 1 (' + data + '), por pessoa ou por casal (o Diego decide e a tela diz)',
                quando='na produção desta peça')


# =================================================================== PEÇAS NOVAS
PECAS = {

    # ------------------------------------------------------------ MADRID · TRAILER
    'p807': dict(
        fmt='Reel', pilar='Como foi de verdade',
        titulo='Madrid em 2 dias: o que deu e o que não deu (trailer do vlog)',
        gancho='Madrid em 2 dias: nem tudo deu.', gt='Expectativa × realidade',
        nivel='B', prod='dec',
        obj=('Trailer do vlog de Madrid (p97, sábado 05/12, 11h): prometer um episódio honesto, com o que deu certo e '
             'o que deu errado, para levar quem vê o Reel ao YouTube no sábado.'),
        motiv='Quem vai a Madrid e quer saber como é de verdade. Envia para quem vai junto; salva para ver o vlog no sábado.',
        q0='Gran Vía no fim da tarde (IMG_4168, 21/03 17:40, horizontal recortado) com o gancho escrito. Conferir o quadro na folha.',
        sc=[
            ('0–2 s', 'Gancho', 'IMG_4168 (21/03 17:40, 23 s, horizontal): plano de rua da Gran Vía, sem a fala. '
                                'Legenda Padrão com o gancho “madrid em 2 dias: nem tudo deu.”'),
            ('2–6 s', 'Expectativa', 'IMG_3654 (19/03 16:15, vertical), de 6,4 a 10,0 s: “eu achei que era baixa temporada, '
                                     'mas tá extremamente cheio”.'),
            ('6–11 s', 'Não deu 1', 'IMG_3924 (20/03 12:59, vertical, Retiro), de 10,4 a 15,4 s: “não vou te ver hoje… a gente vai '
                                    'ter que voltar aqui para ver ele outro dia” (o Palácio de Cristal em reforma). '
                                    'Legenda Padrão: “palácio de cristal: em reforma.”'),
            ('11–15,5 s', 'Não deu 2', 'IMG_4131 (21/03 12:07, horizontal, Bernabéu), de 5,5 a 10,0 s: “a gente deu azar aqui, '
                                       'mudou a data do jogo”.'),
            ('15,5–20 s', 'Deu', 'IMG_4200 (21/03 21:49, vertical), de 16,0 a 22,0 s: “foi massa, Madrid, massa demais… '
                                 'uma cidade que tem uma energia diferente”.'),
            ('20–23 s', 'Fechamento', FECHO_YT + ' (vlog p97). Placa sobre o último quadro de IMG_4200.'),
        ],
        tela='madrid em 2 dias: nem tudo deu. · palácio de cristal: em reforma. · VÍDEO COMPLETO NO YOUTUBE → · sábado, 11h',
        nar='Sem narração nova. Falas originais do Diego e da Marina.',
        leg=('Madrid em 2 dias: nem tudo deu. 🇪🇸\n\nMadrid lotada em março, o Palácio de Cristal do Retiro em reforma e o jogo '
             'no Bernabéu que mudou de data. E mesmo assim a gente saiu apaixonado.\n\nO vlog completo de Madrid sai no '
             'sábado, 05/12, às 11h, no YouTube. Link na bio.'),
        cta='Assiste o vlog completo no sábado, 11h (YouTube, link na bio).',
        capa='Gran Vía com o texto “NEM TUDO DEU”. Texto dentro da área 3:4.',
        som='Falas originais + música da biblioteca baixa nas trocas de cena (DS V2, 4.6).',
        hip='Trailer com expectativa × realidade gera curiosidade pelo episódio e aumenta as visitas ao YouTube no fim de semana.',
        met='Envios e visitas ao perfil por alcance; visualizações do vlog p97 nas primeiras 48 h (YouTube Analytics).',
        mat=['IMG_4168 (21/03 17:40, 23,4 s, horizontal): Gran Vía (usar sem a fala sobre lojas)',
             'IMG_3654 (19/03 16:15, 24,3 s, vertical): Madrid cheia em março',
             'IMG_3924 (20/03 12:59, 32,9 s, vertical): Palácio de Cristal em reforma',
             'IMG_4131 (21/03 12:07, 24,4 s, horizontal girado 180°): jogo adiado',
             'IMG_4200 (21/03 21:49, 35,0 s, vertical): despedida de Madrid'],
        pend=[OUVIR,
              'IMG_3924: a transcrição diz “todo é cobrado” (5,9 a 7,9 s); pode ser “coberto” (obra). Usar só de 10,4 a 15,4 s e confirmar que era reforma',
              'IMG_3654 tem uma fala de 2 pessoas? Conferir quem fala',
              'Cenas diferentes das do teaser (p607, o show) e do Primeiro dia (p221, dia 1): manter assim',
              'Conferir se as 4 cenas estão no corte final do vlog p97 (um trailer só promete o que o episódio mostra)',
              FOLHA_MAD, SEM_VALOR],
        fonte='Drive · Madrid', trecho='IMG_3654 · IMG_3924 · IMG_4131 · IMG_4168 · IMG_4200',
        cus=None, video_longo='p97', tipo='trailer',
        tt=dict(gancho='Madrid em 2 dias: o que deu errado', muda='Sem a Placa de YouTube; fecha em “vlog completo no YouTube, link no perfil” falado em legenda. Até 20 s.'),
        yt=dict(titulo='Madrid em 2 dias: nem tudo deu certo', muda='Fecha com “vídeo completo no canal” e o card do vlog p97 (Short ligado ao vídeo).'),
    ),

    # ------------------------------------------------------------ LISBOA · TRAILER
    'p812': dict(
        fmt='Reel', pilar='Vontade de ir',
        titulo='Lisboa em 1 noite e 1 manhã (trailer do vlog)',
        gancho='Lisboa: 1 noite e 1 manhã.', gt='Afirmação',
        nivel='B', prod='dec',
        obj=('Trailer do vlog de Lisboa (p160, sábado 16/01, 11h): mostrar o que cabe numa manhã em Lisboa e marcar '
             'o encontro de sábado no YouTube.'),
        motiv='Quem tem escala ou poucos dias em Lisboa. Envia para quem vai a Portugal; salva para ver o vlog.',
        q0='Diego acordando: “Bom dia, Lisboa!” (IMG_4282, 23/03 08:49) com o gancho escrito.',
        sc=[
            ('0–2,5 s', 'Gancho', 'IMG_4282 (23/03 08:49, 39 s, horizontal), de 0,1 a 4,8 s: “Bom dia! Acordamos! Bom dia, Lisboa!”. '
                                  'Legenda Padrão: “lisboa: 1 noite e 1 manhã.”'),
            ('2,5–6 s', 'Promessa', 'IMG_4282, de 11,2 a 15,1 s: “porque é o máximo que a gente vai conhecer, uma manhã praticamente”.'),
            ('6–10 s', 'Entrega 1', 'IMG_4364 (23/03 09:22, vertical), de 0,0 a 5,6 s: “chegamos em um dos principais pontos turísticos '
                                    'aqui de Lisboa, a Praça do Comércio”. Legenda Informação: “praça do comércio · 9h22”.'),
            ('10–14 s', 'Entrega 2', 'IMG_4429 (23/03 10:08, vertical), de 0,2 a 7,2 s: miradouro de Santa Luzia, “uma vista linda… '
                                     'várias casinhas”.'),
            ('14–18 s', 'Entrega 3', 'IMG_4395 (23/03 09:31, vertical), de 8,6 a 19,9 s, encurtado: “sol… 17 graus… tempo muito lindo, '
                                     'ou seja, só vem”.'),
            ('18–21 s', 'Fechamento', FECHO_YT + ' (vlog p160).'),
        ],
        tela='lisboa: 1 noite e 1 manhã. · praça do comércio · 9h22 · VÍDEO COMPLETO NO YOUTUBE → · sábado, 11h',
        nar='Sem narração nova. Falas originais.',
        leg=('Lisboa: 1 noite e 1 manhã. 🇵🇹\n\nA gente chegou no domingo à noite e tinha só a manhã de segunda para '
             'conhecer o centro: Praça do Comércio, Alfama, miradouro e pastel de nata.\n\nO vlog completo de Lisboa sai '
             'no sábado, 16/01, às 11h, no YouTube. Link na bio.'),
        cta='Assiste o vlog completo no sábado, 11h (YouTube, link na bio).',
        capa='Praça do Comércio ou miradouro de Santa Luzia + “1 NOITE, 1 MANHÃ”.',
        som='Falas originais + música da biblioteca baixa.',
        hip='Promessa clara de “quanto cabe em pouco tempo” atrai quem tem escala em Lisboa e leva ao vlog.',
        met='Envios e visitas ao perfil por alcance; visualizações do vlog p160 nas primeiras 48 h.',
        mat=['IMG_4282 (23/03 08:49, 39,4 s, horizontal girado 180°): bom dia, Lisboa',
             'IMG_4364 (23/03 09:22, 43,8 s, vertical): Praça do Comércio',
             'IMG_4429 (23/03 10:08, 31,5 s, vertical): miradouro de Santa Luzia',
             'IMG_4395 (23/03 09:31, 20,8 s, vertical): o tempo em março'],
        pend=[OUVIR,
              'IMG_4395: “17 graus” e “dia 23” vêm da transcrição; confirmar no áudio. É o tempo daquele dia, não previsão',
              'Cenas diferentes do teaser p813 (os 4 restaurantes) e do Primeiro dia p270 (a noite): manter assim',
              'A legenda diz “domingo à noite”: 22/03/2026 foi domingo (conferido no calendário). Confirmar com o Diego',
              'Conferir se as cenas estão no corte final do vlog p160',
              FOLHA_LIS, SEM_VALOR],
        fonte='Drive · Lisboa', trecho='IMG_4282 · IMG_4364 · IMG_4395 · IMG_4429',
        cus=None, video_longo='p160', tipo='trailer',
        tt=dict(gancho='Só 1 manhã em Lisboa. Deu?', muda='Sem a Placa de YouTube; fecha com “vlog completo no YouTube” em legenda. Até 20 s.'),
        yt=dict(titulo='Lisboa em 1 noite e 1 manhã: o que coube', muda='Card do vlog p160 no fim; sem “link na bio”.'),
    ),

    # ------------------------------------------------------------ LISBOA · TEASER
    'p813': dict(
        fmt='Reel', pilar='Como foi de verdade',
        titulo='Lisboa: 4 restaurantes até conseguir jantar (teaser do vlog)',
        gancho='Quatro restaurantes até a gente jantar.', gt='Lista curta',
        nivel='B', prod='dec',
        obj='Teaser do vlog de Lisboa (p160): um perrengue real e engraçado da primeira noite que funciona sozinho e manda para o vlog.',
        motiv='Quem já rodou atrás de restaurante viajando. Comenta a própria história; envia para quem vai a Lisboa.',
        q0='Diego falando para a câmera no restaurante (IMG_4264, 22/03 22:23, vertical) com o gancho escrito.',
        sc=[
            ('0–2 s', 'Gancho', 'IMG_4264 (22/03 22:23, 87,6 s, vertical), de 0,5 a 2,5 s: “e ainda tem um detalhe…”. '
                                'Legenda Padrão com o gancho.'),
            ('2–12 s', 'Lista', 'IMG_4264, de 2,5 a 15,9 s: “a gente saiu do hotel, passou em quatro restaurantes: o primeiro tava fechado… '
                                'o segundo não apeteceu, o terceiro, pouquíssimas opções”. Legenda Informação numerada: '
                                '“1 · fechado” · “2 · não apeteceu” · “3 · poucas opções”.'),
            ('12–15 s', 'Pico', 'IMG_4264, de 15,9 a 23,9 s, encurtado: “sentou na mesa… quando a gente abriu o cardápio…”. '
                                'Cortar antes de 25,3 s (valor do prato). Carimbo `PERRENGUE` com `DIA 1 · [hora] · LISBOA`. '
                                'Legenda: “4 · desistimos”.'),
            ('15–18 s', 'Virada', 'IMG_4264, de 30,8 a 36,3 s: “vamos voltar perto da estação que a gente desceu, que tinha alguns '
                                  'restaurantes por lá”.'),
            ('18–20 s', 'Fecho', 'IMG_4253 (22:16, vertical), de 8,1 a 11,1 s: “10 de 10”. Legenda: “do vlog de lisboa · youtube”.'),
        ],
        tela='quatro restaurantes até a gente jantar. · 1 · fechado · 2 · não apeteceu · 3 · poucas opções · 4 · desistimos · do vlog de lisboa · youtube',
        nar='Sem narração nova. Fala original do Diego (IMG_4264).',
        leg=('Quatro restaurantes até a gente jantar. 😅\n\nPrimeira noite em Lisboa: o primeiro estava fechado, o segundo não '
             'animou, o terceiro tinha pouca opção e no quarto a gente desistiu ao abrir o cardápio. Voltamos para perto da '
             'estação de metrô e acertamos.\n\nA noite inteira está no vlog de Lisboa, no YouTube.\n\nJá rodou assim atrás de '
             'restaurante viajando? Conta aqui.'),
        cta='Conta nos comentários se já passou por isso (comentário).',
        capa='Diego no restaurante + “4 RESTAURANTES”.',
        som='Fala original + música da biblioteca baixa.',
        hip='Perrengue curto e verdadeiro, com contagem na tela, gera identificação e comentários.',
        met='Comentários por alcance.',
        mat=['IMG_4264 (22/03 22:23, 87,6 s, vertical): a história dos 4 restaurantes',
             'IMG_4253 (22/03 22:16, 35,4 s, vertical): “10 de 10”'],
        pend=[OUVIR, MINUTAGEM,
              'Cortar IMG_4264 de 25,3 a 30,8 s (valor do prato) e não usar 39,3 a 56,3 s (trechos na lista de CORTES_DE_CUSTO)',
              'Carimbo: o Diego confirma a hora do perrengue (entre a saída do hotel e 21h40, quando chegam ao restaurante em IMG_4246)',
              'Confirmar quem diz “10 de 10” em IMG_4253 e sobre o quê (a transcrição liga ao bacalhau)',
              'Teaser diferente do trailer p812 (manhã) e do Primeiro dia p270 (que não usa IMG_4264): manter assim',
              FOLHA_LIS, SEM_VALOR],
        fonte='Drive · Lisboa', trecho='IMG_4253 · IMG_4264',
        cus=None, video_longo='p160', tipo='teaser',
        tt=dict(gancho='4 restaurantes pra conseguir jantar em Lisboa', muda='Sem a legenda do vlog no fim; termina em “e você, já passou por isso?”.'),
        yt=dict(titulo='4 restaurantes até conseguir jantar em Lisboa', muda='Card do vlog p160 no fim.'),
    ),

    # ------------------------------------------------------------ MADRID · QUANTO CUSTA
    'p278': dict(
        fmt='Reel', pilar='Quanto custa',
        titulo='Madrid: quanto custou comer em 3 dias',
        gancho='Quanto custou comer em Madrid?', gt='Pergunta',
        nivel='A', prod='cus',
        obj='Salvamento e prova da promessa “quanto custa”: o gasto real com comida em Madrid, refeição por refeição, nos 3 dias (19 a 21/03/2026).',
        motiv='Quem está montando o orçamento de Madrid. Salva para planejar; envia para quem divide a viagem.',
        q0='Tapas ao lado do hotel (IMG_3620, 19/03 15:14, vertical) com o gancho escrito.',
        sc=[
            ('0–2 s', 'Gancho', 'IMG_3620 (19/03 15:14, vertical): tapas na mesa. Placa Série `QUANTO CUSTA` / `MADRID` com Chegada. '
                                'Legenda Padrão com o gancho.'),
            ('2–4 s', 'Contexto', 'Legenda Narrativa: “3 dias · 19 a 21/03 · [por pessoa ou casal]”.'),
            ('4–10 s', 'Dia 1', 'IMG_3621 a 3624 (15:14, tapas) e IMG_3807 (22:49, vertical, de 0,8 a 15,5 s: “bem tradicional daqui”). '
                                'Recibo do dia 1 com os itens e `[valor do Diego]`.'),
            ('10–16 s', 'Dia 2', 'IMG_3814 (10:37, churros, de 0,1 a 11,8 s), IMG_3935 (13:48, falafel, de 6,3 a 12,3 s), IMG_3947 '
                                 '(14:51, iogurte, só até 28,0 s) e IMG_3981 a 3984 (21:27, hambúrguer). Recibo do dia 2 com `[valor do Diego]`.'),
            ('16–20 s', 'Dia 3', 'IMG_4138 a 4145 (21/03 14:07 a 14:25, restaurante italiano, sem a fala de IMG_4149) e IMG_4190 '
                                 '(21:22, focaccia, de 0,0 a 26,0 s). Recibo do dia 3 com `[valor do Diego]`.'),
            ('20–24 s', 'Pico', 'Recibo total: “3 dias de comida: € [valor do Diego]” e, depois que ele sai, Bilhete com a opinião do '
                                'Diego: “[vale / pesou / depende]”.'),
            ('24–26 s', 'Fechamento', 'Placa CTA `SALVA PRA VIAGEM →`.'),
        ],
        tela=('quanto custou comer em madrid? · 3 dias · 19 a 21/03 · [por pessoa ou casal] · dia 1 · € [valor do Diego] · '
              'dia 2 · € [valor do Diego] · dia 3 · € [valor do Diego] · total · € [valor do Diego] · [opinião do Diego]'),
        nar='Sem narração nova. Falas sem preço; as falas com preço só entram se baterem com o registro do Diego.',
        leg=('Quanto custou comer em Madrid? 🇪🇸\n\n3 dias (19 a 21/03), [por pessoa ou casal]:\nDia 1: € [valor do Diego] '
             '(tapas e jantar tradicional)\nDia 2: € [valor do Diego] (churros, falafel, iogurte e hambúrguer)\nDia 3: € '
             '[valor do Diego] (italiano e focaccia)\nTotal: € [valor do Diego]\n\n[Opinião do Diego em 1 frase.]\n\nSalva pra '
             'montar o seu orçamento de Madrid.'),
        cta='Salva pra montar o seu orçamento de Madrid (salvamento).',
        capa='Mesa de tapas + Recibo + “COMER EM MADRID: € [total]”.',
        som='Ambiente das mesas + música da biblioteca + som da impressora térmica do Recibo (DS V2, som).',
        hip='Custo real por dia, com a refeição na tela, é muito salvo por quem monta orçamento.',
        met='Salvamentos por alcance.',
        mat=['IMG_3620 a 3624 (19/03 15:14): tapas ao lado do hotel',
             'IMG_3807 (19/03 22:49, 109,8 s, vertical): jantar tradicional (usar só de 0,8 a 15,5 s)',
             'IMG_3814 (20/03 10:37): churros na chocolateria de 1894',
             'IMG_3935 (20/03 13:48) e IMG_3937 a 3939: falafelaria',
             'IMG_3946 e 3947 (20/03 14:51): iogurte gelado',
             'IMG_3975 a 3985 (20/03 21:25 a 21:29): hambúrguer',
             'IMG_4138 a 4146 (21/03 14:07 a 14:40): restaurante italiano',
             'IMG_4184 a 4199 (21/03 21:05 a 21:30): focaccia'],
        pend=[OUVIR, SEM_VALOR,
              'Falas com preço só entram com os dados do Diego (e só se baterem com o registro): C368E0CF 18,3 a 24,4 s; IMG_3627 9,1 a 23,1 s; IMG_3941 8,1 a 12,1 s; IMG_3947 28,2 a 31,2 s; IMG_4149 14,2 a 36,2 s; IMG_4190 26,0 a 40,4 s',
              'Fora por enquanto: as falas de “comida de graça com a bebida” (IMG_3771 21,0 a 46,8 s; IMG_3807 60,0 a 66,0 s). Diego decide se entram, com a explicação certa',
              'Não citar nome de restaurante sem confirmar (a transcrição deturpa: “Maestro Tabarriro”, “Sangre-Messe”, “Hundred Birgle”)',
              'Confirmar com o Diego se houve refeições sem vídeo (café da manhã, lanches): o total precisa ser o do registro, não o do vídeo',
              'O dia 1 começa às 15h05 e o dia 22/03 tem só 5 vídeos: a tela diz “19 a 21/03”',
              'Escolher os planos na folha de contato', FOLHA_MAD],
        fonte='Drive · Madrid', trecho='IMG_3620–4199',
        cus=dict(dados=['Gasto com comida e bebida em Madrid, item a item, com data, hora e lugar (19, 20 e 21/03/2026)',
                        'Se cada valor é por pessoa ou do casal (e quais refeições foram divididas)',
                        'Total por dia e total dos 3 dias, em €',
                        'Cotação usada, se a legenda converter para R$ (com a data)',
                        'Opinião do Diego em 1 frase (vale, pesou ou depende)'],
                 escopo='Madrid, 19 a 21/03/2026 (3 dias; o dia 1 começa às 15h05), comida e bebida, por pessoa ou por casal',
                 quando='na produção desta peça'),
        video_longo=None, tipo=None,
        tt=dict(gancho='Quanto a gente gastou comendo em Madrid', muda='Mesmo corte; Recibos maiores no centro (sem a zona da direita do Instagram). Pergunta final: “caro ou barato?”.'),
        yt=dict(titulo='Quanto custou comer 3 dias em Madrid', muda='Mesmo corte; total no título só depois do dado do Diego.'),
    ),

    # ------------------------------------------------------------ BARCELONA · METRÔ
    'p250': dict(
        fmt='Reel', pilar='Como se mover',
        titulo='Passe de metrô em Barcelona: vale a pena?',
        gancho='Passe de metrô em Barcelona: vale?', gt='Pergunta',
        nivel='A', prod='cus',
        obj='Utilidade: decidir entre passe e bilhete avulso em Barcelona, com o uso real de 3 dias e a conta do Diego.',
        motiv='Quem vai a Barcelona e está montando o transporte. Salva para decidir; envia para quem vai junto.',
        q0='Gràcia de manhã, a caminho do metrô (master 00:09,9) com a Placa Série e o gancho escrito.',
        sc=[
            ('0–2,5 s', 'Gancho', 'Master 00:09,9–00:15,4 (dia 1, Gràcia): “estamos a caminho do metrô para começar nosso dia hoje”. '
                                  'Placa Série `COMO SE MOVER` / `BARCELONA` com Chegada + Legenda Padrão com o gancho.'),
            ('2,5–9 s', 'O que compramos', 'Master 03:02,2–03:14,3: “por isso a gente comprou um bilhete de metrô e ônibus pra utilizar '
                                           'por 72 horas, que é o período que a gente vai ficar aqui. Está facilitando muito nossa vida”. '
                                           'Cortar em 03:14,5, antes de “a gente vai pagar…”.'),
            ('9–13 s', 'Uso real', 'Master 03:21,7–03:29,8 (Montjuïc): “o metrô deixou a gente bem na estação aqui, a gente vai subir '
                                   'andando”. Legenda Informação: “metrô + ônibus · 72 h”.'),
            ('13–16 s', 'Ressalva', 'Master 10:26,5–10:27,6: “uns 18 quilômetros” sobre a chegada à primeira tapa (IMG_0816). '
                                    'Legenda Padrão: “e mesmo assim: 18 km a pé no dia 1.”'),
            ('16–21 s', 'A conta', 'Recibo: “passe 72 h: € [valor do Diego] · [N] viagens · avulso: € [valor oficial]”. '
                                   'Depois que ele sai, Bilhete com o veredito do Diego: “[vale / não vale / depende]”.'),
            ('21–23 s', 'Fechamento', 'Placa CTA `SALVA PRA VIAGEM →`.'),
        ],
        tela=('passe de metrô em barcelona: vale? · metrô + ônibus · 72 h · e mesmo assim: 18 km a pé no dia 1. · '
              'passe 72 h: € [valor do Diego] · [N] viagens · avulso: € [valor oficial] · [veredito do Diego]'),
        nar='Sem narração nova. Falas do master (com a ressalva da trilha de violão por baixo).',
        leg=('Passe de metrô em Barcelona: vale a pena? 🚇\n\nA gente comprou o bilhete de metrô e ônibus de 72 horas (€ '
             '[valor do Diego] [por pessoa]) e fez [N] viagens em 3 dias. Sem o passe, cada viagem custaria € [valor oficial, '
             'conferir na fonte oficial].\n\nVeredito: [veredito do Diego]. E mesmo com o passe, a gente andou uns 18 km no '
             'primeiro dia.\n\nSalva pra decidir o transporte da sua viagem.'),
        cta='Salva pra decidir o transporte da sua viagem (salvamento).',
        capa='Metrô ou Gràcia + “PASSE: VALE?”.',
        som='Falas do master + música da biblioteca. Onde houver violão sob a fala, procurar o bruto.',
        hip='Decisão de transporte com conta real é salva por quem planeja a viagem.',
        met='Salvamentos por alcance.',
        mat=[MASTER_BCN + ': 00:09,9–00:15,4 (Gràcia, a caminho do metrô), 03:02,2–03:14,3 (o passe de 72 h), 03:21,7–03:29,8 (metrô até Montjuïc), 10:26,5–10:27,6 (“uns 18 quilômetros”)',
             'Cena do metrô Palau Reial no dia 1 (citada no INVENTARIO_ACERVO.md, sem minutagem): localizar na folha de contato do master (reels/apresentacao/contact_sheets/), provavelmente entre 00:15 e 00:56',
             'IMG_0816 (bar à noite, primeira tapa, master 639,4 s)',
             TRANSC_BCN],
        pend=[OUVIR, SEM_VALOR,
              'Não há no material verificado um plano de dentro do trem ou da plataforma: só a fala de Gràcia e a chegada a Montjuïc. Localizar o plano do Palau Reial na folha; se não houver, a peça sai só com as falas e a rua',
              'Cortar o master em 03:14,5 (antes de “a gente vai pagar 27,50”). A frase seguinte (“mas com certeza a gente usaria muito mais”, 03:17,6–03:20,6) só entra junto com o valor do Diego',
              'Tarifas atuais (passe de 72 h e bilhete avulso): conferir na fonte oficial na produção, com a data, e não afirmar como fato atual',
              'Nome comercial do passe: não citar sem confirmar na fonte oficial',
              'Conflito com p271 (09/02, “Por que ficamos em Gràcia”), que usa o master 02:39–03:09 e cita o passe no motivo 3: sugerir ao p271 cortar em 03:02 para não repetir este trecho',
              'O p300 (25/10) abre em Gràcia (master 00:00–00:20): usar aqui outro plano de rua ou só o áudio de 00:09,9–00:15,4'],
        fonte='Barcelona · master do vlog', trecho='Master 00:09–00:16 · 03:02–03:30 · 10:26–10:28',
        cus=dict(dados=['Valor pago pelo bilhete de metrô e ônibus de 72 h, por pessoa, e o tipo exato do bilhete',
                        'Número de viagens de metrô e ônibus feitas nos 3 dias (por pessoa), mesmo que aproximado (dizer se é aproximado)',
                        'Veredito do Diego: vale, não vale ou depende (e para quem)'],
                 escopo='Barcelona, 3 dias, transporte público, por pessoa',
                 quando='na produção desta peça'),
        video_longo=None, tipo=None,
        tt=dict(gancho='Vale comprar passe de metrô em Barcelona?', muda='Mesmo corte; a conta em 1 Recibo grande no centro. Pergunta final: “você compraria?”.'),
        yt=dict(titulo='Passe de metrô em Barcelona: vale a pena?', muda='Mesmo corte; tarifa com a data da fonte oficial na descrição.'),
    ),

    # ------------------------------------------------------------ LISBOA · METRÔ DO AEROPORTO
    'p828': dict(
        fmt='Reel', pilar='Como se mover',
        titulo='Lisboa: do aeroporto ao centro de metrô',
        gancho='Do aeroporto ao centro, de metrô.', gt='Afirmação',
        nivel='A', prod='cus',
        obj='Utilidade: mostrar que o metrô sai de dentro do aeroporto de Lisboa e leva ao centro, com a ida e a volta reais.',
        motiv='Quem vai pousar em Lisboa (inclusive em escala). Salva para a chegada; envia para quem vai junto.',
        q0='Diego na estação do aeroporto: “estamos aqui esperando o metrô que fica dentro do aeroporto” (IMG_4233, 22/03 19:16).',
        sc=[
            ('0–2,5 s', 'Gancho', 'IMG_4233 (22/03 19:16, 34,8 s, vertical; GPS no aeroporto), de 0,3 a 4,3 s: “estamos aqui esperando o '
                                  'metrô que fica dentro do aeroporto”. Placa Série `COMO SE MOVER` / `LISBOA` com Chegada + gancho.'),
            ('2,5–7 s', 'Por quê', 'IMG_4233, de 14,3 a 20,3 s: ficar no centro “porque… vai ter pouco tempo… a gente quer ficar perto '
                                   'de tudo”. Cortar 5,3 a 13,3 s (valor da passagem e nome do hotel).'),
            ('7–11 s', 'Chegada', 'IMG_4235 a 4239 (22/03 19:50 a 19:54, horizontais, GPS no centro): primeiros planos no centro. '
                                  'Legenda Informação: “19h16 aeroporto · 19h50 centro (hora dos arquivos)”.'),
            ('11–15 s', 'A conta', 'Recibo: “metrô aeroporto → centro: € [valor do Diego] [por pessoa]”. Legenda Informação: '
                                   '“linha e estação: [conferir na fonte oficial]”.'),
            ('15–20 s', 'A volta', 'IMG_4526 (23/03 13:03, vertical), de 31,0 a 38,9 s: “agora estamos a caminho do hotel para irmos '
                                   'para o aeroporto de metrô. Acabou, pessoal”.'),
            ('20–22 s', 'Fechamento', 'Placa CTA `SALVA PRA VIAGEM →`.'),
        ],
        tela=('do aeroporto ao centro, de metrô. · 19h16 aeroporto · 19h50 centro (hora dos arquivos) · metrô aeroporto → '
              'centro: € [valor do Diego] · linha e estação: [fonte oficial]'),
        nar='Sem narração nova. Falas originais.',
        leg=('Do aeroporto ao centro de Lisboa, de metrô. 🚇\n\nA estação fica dentro do aeroporto. Às 19h16 a gente estava na '
             'plataforma; o vídeo seguinte, já no centro, é das 19h50 (hora dos arquivos). A passagem: € [valor do Diego] '
             '[por pessoa]. E na volta, fizemos o caminho ao contrário.\n\n[Linha, estação e tarifa atual: conferir na fonte '
             'oficial antes de publicar.]\n\nSalva pra sua chegada em Lisboa.'),
        cta='Salva pra sua chegada em Lisboa (salvamento).',
        capa='Diego na estação + “AEROPORTO → CENTRO”.',
        som='Falas originais + ambiente da estação + música da biblioteca baixa.',
        hip='A primeira dúvida de quem pousa (“como chego ao centro?”), respondida com a ida e a volta reais, é salva.',
        met='Salvamentos por alcance.',
        mat=['IMG_4233 (22/03 19:16, 34,8 s, vertical, GPS +38,7688 −9,1284): na estação do aeroporto',
             'IMG_4234 (22/03 19:19, 35,2 s, vertical, sem GPS, fala ininteligível): talvez dentro do metrô; conferir na folha',
             'IMG_4235 a 4239 (22/03 19:50 a 19:54, horizontais, GPS +38,714 −9,138): primeiros planos no centro',
             'IMG_4526 (23/03 13:03, 56,1 s, vertical): a volta de metrô'],
        pend=[OUVIR, SEM_VALOR, FOLHA_LIS,
              'Cortar IMG_4233 de 5,3 a 13,3 s (valor da passagem e nome do hotel, deturpado na transcrição) e de 27,3 a 32,3 s (comparação de preço). Cortar IMG_4526 antes de 31,0 s (valor da conta)',
              'Linha, estação de destino e tarifa atual: conferir na fonte oficial do Metropolitano de Lisboa na produção, com a data. Não afirmar como fato atual',
              'Ver na folha o que mostram IMG_4234 a 4239 (plataforma, trem, rua?) antes de montar a cena 3',
              'Confirmar com o Diego a estação em que desceram (a fala de IMG_4246 diz “na praça bem na saída do metrô”)',
              'Mesmo tema do tk20 (26/02): o tk20 foi refeito com outra cena de Lisboa (ver TIKTOK)',
              'O p270 (16/01) abre com IMG_4233 0,3 a 4,3 s: aqui o plano pode ser o mesmo, mas a cena 2 e a 3 são novas'],
        fonte='Drive · Lisboa', trecho='IMG_4233–4239 · IMG_4526',
        cus=dict(dados=['Valor pago pela passagem do metrô do aeroporto ao centro em 22/03/2026, por pessoa, e o tipo de bilhete ou cartão',
                        'Valor da volta em 23/03, se foi diferente',
                        'Estação em que desceram no centro'],
                 escopo='Lisboa, 22 e 23/03/2026, aeroporto ↔ centro, por pessoa',
                 quando='na produção desta peça'),
        video_longo=None, tipo=None,
        tt=dict(gancho='Aeroporto de Lisboa: o metrô fica aqui dentro', muda='Mesmo corte, sem a volta (até 15 s). Pergunta final: “vai de metrô ou de táxi?”.'),
        yt=dict(titulo='Lisboa: do aeroporto ao centro de metrô', muda='Mesmo corte; fonte oficial e data da tarifa na descrição.'),
    ),
}


# =================================================================== REVISÕES
REVISOES = {

    # ---------------------------------------------- p607 → TEASER do vlog de Madrid
    'p607': dict(
        titulo='Madrid à noite: o show que ninguém entendeu (teaser do vlog)',
        gancho='Ninguém entendeu que show era esse.', gt='Afirmação',
        nivel='B', prod='dec', video_longo='p97', tipo='teaser',
        obj=('Teaser do vlog de Madrid (p97): um imprevisto real da noite de sexta (20/03), na praça Pedro Zerolo, que funciona '
             'sozinho e puxa comentários de quem sabe o que era.'),
        q0='Multidão e palco com luzes à noite (FD2CF314.mp4) com o gancho escrito.',
        sc=[
            ('0–2 s', 'Gancho', 'FD2CF314 (exportação, 5,9 s, 1080 × 1920), de 0 a 2 s: multidão e palco. Legenda Padrão com o gancho.'),
            ('2–7 s', 'Contexto', 'IMG_3959 (20/03 19:41, vertical), de 18,2 a 23,2 s: “tá tendo um show aqui de alguma coisa na praça em '
                                  'frente a esse restaurante”. Legenda Narrativa: “madrid, sexta, 19h45.”'),
            ('7–14 s', 'Pico', 'IMG_3963 (20/03 19:45, vertical, GPS 40,4207 −3,6993), de 9,0 a 16,4 s: “descobrimos o que é? … parece '
                               'música eletrônica, mas ao mesmo tempo tem um carro parado ali, a gente não entendeu muito bem o que é”. '
                               'Ticket `SURPREENDE` no pico (surpresa real).'),
            ('14–17 s', 'Clima', '961C4420 (exportação, 10,2 s) ou FB3F63B4 (exportação, 7,7 s): a multidão. Legenda Padrão: '
                                 '“sabe o que era? conta aqui.”'),
            ('17–18 s', 'Fecho', 'Legenda: “do vlog de madrid · youtube”.'),
        ],
        tela='ninguém entendeu que show era esse. · madrid, sexta, 19h45. · sabe o que era? conta aqui. · do vlog de madrid · youtube',
        nar='Sem narração nova. Falas originais (IMG_3959 e IMG_3963).',
        leg=('Ninguém entendeu que show era esse. 🎶\n\nSexta à noite em Madrid, praça Pedro Zerolo, chuva, e de repente: palco, '
             'luzes, música eletrônica e um carro parado no meio. A gente parou para ver e até hoje não sabe o que era.\n\nA noite '
             'inteira está no vlog de Madrid, no YouTube.\n\nSabe o que era? Conta aqui.'),
        cta='Conta nos comentários o que era (comentário).',
        capa='Palco com luzes + “QUE SHOW É ESSE?”.',
        som='Som direto do evento baixo (música com possíveis direitos) + falas originais.',
        hip='Mistério real e sem resposta convida quem conhece Madrid a explicar nos comentários.',
        met='Comentários por alcance.',
        mat=['FD2CF314-30AE-46D6-B3AD-008640946373.mp4 (exportação, 5,9 s, 1080 × 1920; data da exportação, não da gravação; verificado em v5)',
             'IMG_3959 (20/03 19:41, 37,0 s, vertical): a chegada à praça',
             'IMG_3963 (20/03 19:45, 30,7 s, vertical): “a gente não entendeu muito bem o que é”',
             '961C4420….mp4 (10,2 s) e FB3F63B4….mp4 (7,7 s): exportações da mesma noite (decupagem M3)',
             'IMG_3960 a 3962 (19:42 a 19:43, horizontais): planos vizinhos'],
        pend=[OUVIR, MINUTAGEM,
              'Não explicar o que era o evento sem confirmar. “Até hoje não sabe o que era” só fica se o Diego confirmar',
              'Nome da praça: a transcrição diz “Xerolo” e, antes, “Kalao”; o GPS de IMG_3963 é 40,4207 −3,6993 (praça Pedro Zerolo, conferir no mapa)',
              'Os arquivos FD2CF314, 961C4420 e FB3F63B4 são exportações: confirmar que são da mesma noite (folha de contato)',
              'Música do evento pode ter direitos autorais: manter o ambiente baixo',
              'Teaser diferente do trailer p807 (expectativa × realidade, sem o show): manter assim',
              'IMG_3965 (20:47, 0,5 s) saiu: é uma hora depois do show e curto demais',
              FOLHA_MAD],
        fonte='Drive · Madrid', trecho='IMG_3959–3963 · FD2CF314 · 961C4420 · FB3F63B4',
        tt=dict(gancho='Que show era esse em Madrid?', muda='Mesmo corte, sem a legenda do vlog; pergunta fixa na tela até o fim.'),
        yt=dict(titulo='Caímos num show na rua em Madrid', muda='Card do vlog p97 no fim (é o Short p710 do mesmo dia).'),
    ),

    # ---------------------------------------------- p221 → Nível A com Placar
    'p221': dict(
        nivel='A', prod='cus', tipo='serie', video_longo='p97',
        sc=[
            ('0–2 s', 'Gancho', 'IMG_3617 (19/03 15:05, vertical), de 0,5 a 2,5 s: “Buenos días! Estamos aqui em Madrid” + Placa '
                                '`PRIMEIRO DIA EM / MADRID` com Chegada (x 72 · y 640).'),
            ('2 s ao fim', 'Placar', PLACAR_TXT),
            ('2–5 s', 'Contexto', 'Legenda Narrativa: “madrid, dia 1. 15h05.” sobre o resto da fala de abertura (até 12,6 s; '
                                  'não usar 15,6 a 19,6 s, “última parada dessa EuroTrip”).'),
            ('5–9 s', 'Entrega', 'Tapas ao lado do hotel (IMG_3620 a 3624, 15h14). O Placar gira com o primeiro gasto.'),
            ('9–14 s', 'Entrega', 'Puerta del Sol (IMG_3630 a 3633, 15h47) e Plaza Mayor (IMG_3648, 16h11, de 0,0 a 9,8 s: “a praça mais '
                                  'vermelha do mundo”). Legenda Informação com o nome do lugar.'),
            ('14–19 s', 'Entrega', 'Catedral da Almudena (IMG_3715, 17h02, sem a fala de 5,3 a 11,1 s) e Palácio Real por fora '
                                   '(IMG_3727, 17h11, até 13,8 s: “não compramos a visitação”).'),
            ('19–23 s', 'Pico', 'Ticket `SURPREENDE`: Templo de Debod vazio (IMG_3771, 19h25, de 0,0 a 7,0 s: “achei que ele ia estar com '
                                'água, mas ele está vazio”), se o Diego confirmar a surpresa.'),
            ('23–26 s', 'Fechamento', 'Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + Nascer do 1º + bordão. O Placar fica com o total do dia.'),
        ],
        tela='buenos días, madrid! · 15h05 · puerta del sol · plaza mayor · palácio real · templo de debod · +HH:MM · € [valor do Diego]',
        leg=('Buenos días, Madrid! ☀️\n\nChegamos ao hotel perto da Plaza Mayor às 15h05 do dia 19/03 e saímos andando: tapas ao '
             'lado do hotel, Puerta del Sol, Plaza Mayor, Palácio Real por fora e o Templo de Debod no fim da tarde.\n\nGasto do '
             'dia 1: € [valor do Diego] [por pessoa ou casal]. O vlog completo de Madrid está no YouTube.\n\nManda pra quem vai '
             'pra Madrid.'),
        capa='Chegada em Madrid com a Placa e o Placar. Texto da capa: “DIA 1: MADRID”.',
        mat=['Madrid, dia 1 (19/03/2026, hora do arquivo, fuso de Madrid): IMG_3617 (15:05, 33 s, vertical 4K, fala de abertura), IMG_3620 a 3624 (tapas, 15:14), IMG_3630 a 3634 (Puerta del Sol, 15:47), IMG_3648 (Plaza Mayor, 16:11), IMG_3715 (Almudena, 17:02), IMG_3727 (Palácio Real, 17:11), IMG_3771 (Debod, 19:25); `C368E0CF….mp4` (selfie na Plaza Mayor, 29 s, até 18 s). Transcrição e metadados lidos; quadros das folhas 01 e 02 vistos (DECUPAGEM_MADRID.md)'],
        pend=[PEND_PLACAR, OUVIR, SEM_VALOR,
              'Hora de chegada: 15h05 é o check-in no hotel (IMG_3617); o +HH:MM do Placar conta da chegada à cidade, que o Diego informa',
              'Cortar fora os trechos com preço: `C368E0CF…` (18 a 24 s), IMG_3627 (9 a 23 s), IMG_3686 (11 a 18 s), IMG_3727 (15 a 18 s)',
              'Não usar a frase “nossa última parada dessa EuroTrip” (IMG_3617, 15,6 a 19,6 s): Lisboa vem depois',
              'Não usar a frase da Almudena sobre visitação gratuita (IMG_3715, 5,3 a 11,1 s)',
              'Não citar o nome do bar do primeiro almoço: a transcrição o deturpa (“Maestro Tabarriro”)',
              'Ver na folha os planos de Almudena, Palácio Real e Debod antes do corte (só as folhas 01 e 02 foram vistas)',
              'Confirmar com o Diego que o Debod vazio foi a surpresa do dia',
              'Sai no mesmo dia do vlog de Madrid (05/12); cenas diferentes do trailer p807 e do teaser p607'],
        cus=cus_dia1('Madrid', '19/03/2026'),
    ),

    # ---------------------------------------------- p270 → Nível A com Placar (a noite existiu)
    'p270': dict(
        nivel='A', prod='cus', tipo='serie', video_longo='p160',
        obj=('Série: a primeira noite em Lisboa (22/03/2026), do metrô no aeroporto ao jantar, com o Placar. A noite existiu: '
             '37 vídeos de 19h16 a 23h55.'),
        q0='Diego na estação do aeroporto (IMG_4233, 22/03 19:16) com a Placa `PRIMEIRO DIA EM / LISBOA`.',
        sc=[
            ('0–2,5 s', 'Gancho', 'IMG_4233 (22/03 19:16, vertical), de 0,3 a 4,3 s: “estamos aqui esperando o metrô que fica dentro do '
                                  'aeroporto” + Placa `PRIMEIRO DIA EM / LISBOA` com Chegada (x 72 · y 640) + gancho.'),
            ('2 s ao fim', 'Placar', PLACAR_TXT),
            ('2,5–6 s', 'Contexto', 'Legenda Narrativa: “1 noite e 1 manhã.” sobre o plano do quarto (EE52D542, exportação, de 0,0 a '
                                    '18,7 s, encurtado: “minha mala sobreviveu… o único banheiro da Europa que tem chuveirinho”).'),
            ('6–10 s', 'Entrega', 'IMG_4246 (21:40, horizontal), de 0,0 a 6,6 s: “depois de muita procura, na praça bem na saída do metrô” '
                                  '(cortar antes do nome do restaurante, 6,6 s).'),
            ('10–15 s', 'Entrega', 'IMG_4251 (21:57, vertical), de 6,1 a 11,9 s: “bacalhau com batata gratinada e queijo por cima” e '
                                   'IMG_4253 (22:16), de 8,1 a 11,1 s: “10 de 10”. O Placar gira com o jantar.'),
            ('15–20 s', 'Pico', 'IMG_4257 (22:20, vertical), de 0,3 a 9,7 s: “sem palavras, sem palavras”. Bilhete: “sem palavras.”'),
            ('20–24 s', 'Fecho do dia', 'IMG_4270 (22:27, horizontal), de 0,6 a 7,6 s: “agora vamos descansar porque amanhã nós temos a '
                                        'jornada intensa por Lisboa”.'),
            ('24–27 s', 'Fechamento', 'Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + Nascer do 1º + bordão.'),
        ],
        tela='chegamos em lisboa à noite. e agora? · 1 noite e 1 manhã. · sem palavras. · +HH:MM · € [valor do Diego]',
        nar='Sem narração nova. Falas originais.',
        leg=('Chegamos em Lisboa à noite. E agora? 🇵🇹\n\nDomingo, 22/03: metrô de dentro do aeroporto até o centro, check-in, '
             'uma boa procura por restaurante e um bacalhau gratinado que deixou a gente sem palavras. No dia seguinte, só uma '
             'manhã para o resto.\n\nGasto do dia 1: € [valor do Diego] [por pessoa ou casal]. O vlog completo de Lisboa está '
             'no YouTube.\n\nManda pra quem vai pra Lisboa.'),
        capa='Diego na estação do aeroporto com a Placa e o Placar. Texto da capa: “1ª NOITE: LISBOA”.',
        mat=['IMG_4233 (22/03 19:16, 34,8 s, vertical, GPS no aeroporto)',
             'EE52D542-D823-4E20-9E77-D8ACDFA96E60.mp4 (exportação, 33,1 s, 1080 × 1920: o quarto do hotel; data da exportação, não da gravação)',
             'IMG_4246 (21:40, 31,4 s), IMG_4251 (21:57, 16,1 s), IMG_4253 (22:16, 35,4 s), IMG_4257 (22:20, 39,7 s), IMG_4270 (22:27, 9,2 s)',
             'Vizinhos da noite sem fala para cortes: IMG_4247, 4249, 4254 a 4256, 4272 a 4278'],
        pend=[PEND_PLACAR, OUVIR, SEM_VALOR, FOLHA_LIS,
              'A noite existiu: 37 vídeos de 22/03, de 19h16 a 23h55 (acervo/lisboa/linha_do_tempo.md). Resolve a pendência da v5',
              'Cortes de custo: IMG_4233 5,3 a 13,3 s e 27,3 a 32,3 s; IMG_4251 0,7 a 6,1 s (lista de CORTES_DE_CUSTO); IMG_4257 a partir de 9,7 s (fala sobre gastar dinheiro); IMG_4264 e IMG_4268 fora',
              'EE52D542 é exportação: confirmar que é o quarto de Lisboa e usar só até 18,7 s (o resto da transcrição é confuso)',
              'Não citar o nome do restaurante (“Nicola” na transcrição) sem confirmar',
              'Confirmar quem fala em IMG_4253 e IMG_4257',
              'IMG_4264 (os 4 restaurantes) fica para o teaser p813; a manhã fica para o trailer p812',
              'Sai no mesmo dia do vlog de Lisboa (16/01)'],
        fonte='Drive · Lisboa', trecho='IMG_4233–4270 · EE52D542',
        cus=cus_dia1('Lisboa', '22/03/2026', ['Valor da passagem do metrô do aeroporto (usado também no p828)']),
    ),

    # ---------------------------------------------- p300 → Nível A com Placar
    'p300': dict(
        nivel='A', prod='cus', tipo='serie', video_longo='p13',
        sc=[
            ('0–2,5 s', 'Gancho', 'Gràcia (master, dia 1, 00:00–00:20), num plano sem etiqueta gráfica e diferente do usado na '
                                  'apresentação + Placa `PRIMEIRO DIA EM / BARCELONA` com Chegada (x 72 · y 640). Legenda Padrão com '
                                  'o gancho e Destaque em “a pé”.'),
            ('2 s ao fim', 'Placar', PLACAR_TXT),
            ('2,5–7 s', 'Camp Nou', 'IMG_0502 (chegada, fila; master 71,15 s). Legenda Informação com o nome do lugar.'),
            ('7–10 s', 'Montjuïc', 'IMG_0586 (vista; master 218,2 s). Trocar o áudio do músico de rua pela música da biblioteca.'),
            ('10–13 s', 'Barceloneta', 'IMG_0690 (praia, frio, jet ski; master 453,45 s).'),
            ('13–16 s', 'Arco do Triunfo', 'IMG_0781, fim da tarde (master 565,8 s).'),
            ('16–23 s', 'Pico', 'Master 10:20,7–10:40,0: “hoje a gente andou demais… uns 18 quilômetros… acabei de pedir a minha primeira '
                                'tapa de Barcelona, pedi uma papa brava com uma cerveza” (IMG_0816). O Placar gira com a tapa. '
                                'Bilhete: “valeu cada km.”'),
            ('23–26 s', 'Fechamento', 'Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + Nascer do 1º + bordão. Legenda: “segue pra ver o próximo.”'),
        ],
        tela=('primeiro dia em barcelona, só a pé. · gràcia → camp nou → montjuïc → barceloneta → primeira tapa · '
              '+HH:MM · € [valor do Diego] · e isso foi só o primeiro dia.'),
        leg=('Gràcia, Camp Nou, Montjuïc, Barceloneta, Ciutadella e Arco do Triunfo, quase tudo a pé. No fim, a primeira tapa: '
             'patatas bravas e cerveza.\n\nGasto do dia 1: € [valor do Diego] [por pessoa ou casal]. O roteiro completo, parada '
             'por parada, sai no carrossel de quarta.\n\nSou o Diego e aqui eu mostro o primeiro dia em cada cidade. Segue pra '
             'ver o próximo.'),
        pend=[PEND_PLACAR, OUVIR, SEM_VALOR,
              'Hora de chegada: a fala do master (00:06,6–00:09,0) diz que chegaram “bem tarde ontem, uma da manhã”. O Diego decide de onde conta o +HH:MM (chegada à 1h ou saída de casa no dia 1) e informa a hora exata',
              'Valores falados no master (museu do Barça 01:02, passe 03:09, McDonald’s 06:20) não entram por fala: no Placar só os valores do registro do Diego',
              'Não repetir os planos da camisa do Bahia (Reel de 11/10)',
              'Vlog p13 com data de 10/10: confirmar com o Diego se foi publicado. Se não foi, ajustar “o vlog está no YouTube” (a legenda atual não cita o vlog)'],
        cus=cus_dia1('Barcelona', 'dia 1 da viagem, data a confirmar pelo Diego',
                     ['Data do dia 1 em Barcelona (o master não traz a data)']),
    ),

    # ---------------------------------------------- p265 → TEASER do vlog de Barcelona
    'p265': dict(
        titulo='Vale a pena ir a Barcelona? A resposta no aeroporto (teaser do vlog)',
        gancho='Barcelona vale a pena? Respondemos no aeroporto.', gt='Pergunta',
        nivel='B', prod='ok', video_longo='p13', tipo='teaser',
        obj=('Teaser do vlog de Barcelona (p13): a cena de despedida no aeroporto, com o veredito e a brincadeira dos dois, '
             'inteira numa cena só. Leva quem vê ao vlog e gera envios para quem está decidindo a viagem.'),
        sc=[
            ('0–2 s', 'Gancho', 'Master 33:20,7–33:23,8: “é, pessoal, já estamos no aeroporto de Barcelona” + Placa Hook `VALE A PENA?` / '
                                '`BARCELONA`.'),
            ('2–9 s', 'Humor', 'Master 33:28,7–33:36,0: “cidade surreal, energia muito boa.” “Já virou sua preferida?” “Ainda não. Eu vou '
                               'esperar a nossa tripzinha acabar.”'),
            ('9–16 s', 'Resposta', 'Master 33:38,2–33:45,6: “quem estiver planejando vir para Barcelona ou já estiver com viagem marcada: '
                                   'vale muito a pena, saiba que você não vai se arrepender”. Bilhete `vale.` com ✓ no pico.'),
            ('16–20 s', 'Fechamento', 'Master 33:56,7–34:00,5: “e para quem não tem Barcelona nos planos: coloque”. Legenda: “manda pra '
                                      'quem precisa de um empurrão.” e “do vlog de barcelona · youtube”.'),
        ],
        tela='barcelona vale a pena? · respondemos no aeroporto · vale. · manda pra quem precisa de um empurrão. · do vlog de barcelona · youtube',
        leg=('Barcelona vale a pena? A gente respondeu no aeroporto. ✈️\n\nTrês dias, 18 km no primeiro, Gaudí, tapas e muito frio '
             'na praia. A resposta: vale muito a pena. Quem tem Barcelona nos planos não vai se arrepender. Quem não tem, '
             'coloca.\n\nOs 3 dias inteiros estão no vlog de Barcelona, no YouTube.\n\nManda pra quem precisa de um empurrão pra ir.'),
        mat=[MASTER_BCN + ': uma cena só, 33:20,7–34:00,5 (dia 3, aeroporto)', TRANSC_BCN],
        pend=[OUVIR, MINUTAGEM.replace('o Claude não tem o vlog editado: os tempos acima são do arquivo bruto',
                                       'os tempos acima já são do master do vlog p13; conferir se a versão publicada é a mesma'),
              'Teaser = uma cena: saiu a montagem de 4 planos dos 3 dias (Snap) da versão anterior',
              'Checar trilha de violão sob a fala no aeroporto',
              'Confirmar quem pergunta “já virou sua preferida?” e quem responde',
              'Não usar 34:03,4–34:06,2 (“minha cidade preferida”): contradiz o “ainda não” da cena sem contexto',
              'Trailer de Barcelona não se aplica (vlog p13 de 10/10). Confirmar com o Diego se o p13 foi publicado',
              'O Short p714 (09/01) usa a mesma cena: diferenciar o Reel pela cena de humor (2–9 s)'],
        tt=dict(gancho='Barcelona vale a pena? Resposta no aeroporto', muda='Mesmo corte; sem a legenda do vlog; pergunta final “qual cidade você colocaria nos planos?”.'),
        yt=dict(titulo='Vale a pena ir a Barcelona? A resposta no aeroporto', muda='Já existe como Short p714 (09/01): card do vlog p13 no fim.'),
    ),
}


# =================================================================== TIKTOK
TIKTOK = {
    'tk04': dict(
        titulo='Churro de Madrid × churro do Brasil',
        gancho='Churro de Madrid × churro do Brasil.',
        conceito=('Comparação com humor e sem preço: o segundo churro de Madrid (20/03 16:51), recheado de doce de leite, '
                  'provado “para comparar com o Brasil”, e o veredito: “é bom, mas o do Brasil ainda ganha”.'),
        estrutura=[('0–2 s', 'IMG_3953 (20/03 16:51, vertical), de 21,4 a 28,8 s: “a gente pediu um churro aqui… de doce de leite… para '
                             'comparar com o Brasil”. Texto: “churro de madrid × churro do brasil.”'),
                   ('2–7 s', 'IMG_3954 (16:54, horizontal recortado), de 0,0 a 7,0 s: “primeiro ponto negativo: não tem açúcar e canela, '
                             'e eu amo açúcar e canela”.'),
                   ('7–12 s', 'IMG_3954, de 7,0 a 15,9 s: a primeira mordida e a reação.'),
                   ('12–16 s', 'IMG_3954, de 30,9 a 33,9 s: “é bom. Mas o do Brasil ainda ganha.” Texto: “o do brasil ainda ganha.”'),
                   ('16–18 s', 'Pergunta na tela: “qual churro é o melhor do brasil?”')],
        mat=['IMG_3952 (20/03 16:51, 12,9 s, horizontal)', 'IMG_3953 (16:51, 33,2 s, vertical)', 'IMG_3954 (16:54, 43,1 s, horizontal)',
             'Opcional: IMG_3821 (10:56, vertical), de 6,7 a 8,2 s: “nada demais, gente” sobre o churro famoso da manhã'],
        legenda='Churro de Madrid × churro do Brasil 🇪🇸🇧🇷 O veredito foi rápido. Qual é o melhor churro que você já comeu no Brasil? #madrid #churros #viagem #espanha',
        obj='Comentários e identificação brasileira (orgulho do churro daqui), sem custo.',
        met='Comentários e compartilhamentos por visualização.',
        prod='dec',
        pend=[OUVIR, 'Confirmar quem fala em IMG_3954 (Diego ou Marina) e se a reação de 7 a 15 s é “não é bom” ou “é bom” (a transcrição diz “não é bom” em 7,0 a 14,9 s)',
              'Não citar o nome da churrería (a transcrição deturpa: “maestro churro”, “Sangre-Messe”)', FOLHA_MAD],
    ),
    'tk09': dict(
        titulo='Lisboa: a atração que a gente não sabia que era paga',
        gancho='A gente não sabia que era pago.',
        conceito=('Perrengue leve e útil, sem valor: chegaram ao Castelo de São Jorge (23/03 10:38) achando que dava para ver por '
                  'fora, descobriram que a entrada é paga e, sem tempo, trocaram por um bolinho de bacalhau ao lado.'),
        estrutura=[('0–2 s', 'IMG_4489 (23/03 10:38, vertical), de 8,2 a 13,5 s, começando em “o castelo paga pra entrar”. Texto: '
                             '“a gente não sabia que era pago.”'),
                   ('2–6 s', 'IMG_4489, de 9,5 a 13,5 s: “eu achava que tinha uma fachada pra gente ver”. Cortar antes de 15,5 s (valor).'),
                   ('6–12 s', 'IMG_4490 (10:39, horizontal recortado), de 8,4 a 23,4 s, encurtado: “por tempo… a gente achou melhor otimizar… '
                              'o pastel de bacalhau pra eles é o nosso bolinho de bacalhau”.'),
                   ('12–17 s', 'IMG_4498 (11:06, vertical), de 0,2 a 9,9 s: “não conseguimos entrar, mas estou abastecido”.'),
                   ('17–19 s', 'Texto: “confere antes se a entrada é paga.” + pergunta “já passou por isso?”')],
        mat=['IMG_4489 (23/03 10:38, 24,1 s, vertical, GPS no castelo)', 'IMG_4490 (10:39, 37,0 s, horizontal)', 'IMG_4498 (11:06, 33,3 s, vertical)'],
        legenda='A gente subiu até o Castelo de São Jorge achando que dava pra ver por fora. Não dava. Sem tempo, trocamos por bolinho de bacalhau 😅 Confere antes de subir. #lisboa #portugal #viagem',
        obj='Comentários e utilidade: evitar a mesma surpresa, sem citar preço.',
        met='Comentários e salvamentos por visualização.',
        prod='dec',
        pend=[OUVIR, SEM_VALOR,
              'Cortar IMG_4489 de 15,5 a 22,0 s e IMG_4490 de 4,4 a 8,4 s (valor da entrada)',
              'Não citar o nome do restaurante (IMG_4489, 0,2 a 6,3 s) sem confirmar',
              'Regras de entrada e horário do castelo mudam: não afirmar nada atual; “confere antes” é o conselho, não um dado',
              FOLHA_LIS],
    ),
    'tk12': dict(
        titulo='O “melhor hambúrguer do mundo” × os de Salvador',
        gancho='Melhor hambúrguer do mundo? Salvador ganha.',
        conceito=('Veredito sincero e soteropolitano: foram ao hambúrguer que o Diego chamou de “o melhor do mundo” (20/03 21:06, '
                  'fila e horário marcado) e o veredito na volta ao hotel: “os hambúrgueres de Salvador dão um banho”.'),
        estrutura=[('0–2 s', 'IMG_3957 (20/03 19:38, vertical), de 8,1 a 13,1 s: “agora a gente vai experimentar o melhor hambúrguer do '
                             'mundo”. Cortar antes do nome (13,1 s). Texto: o gancho.'),
                   ('2–5 s', 'IMG_3981 a 3984 (21:27, horizontais): o pedido e o hambúrguer na mão.'),
                   ('5–12 s', 'IMG_3986 (22:23, vertical), de 8,2 a 23,2 s, encurtado: “hambúrguer é muito bom… porém a carne não estava bem '
                              'temperada”.'),
                   ('12–15 s', 'IMG_3986, de 26,2 a 32,5 s: “a batata… 50 vezes melhor do que o hambúrguer”.'),
                   ('15–21 s', 'IMG_3986, de 58,3 a 71,3 s: “os hambúrgueres de Salvador… dão um banho”. Texto: “salvador dá um banho.”'),
                   ('21–23 s', 'Pergunta na tela: “qual hamburgueria de salvador ganha?”')],
        mat=['IMG_3957 (20/03 19:38, 22,8 s)', 'IMG_3971 (21:06, 51,7 s): fila e horário marcado (opcional)',
             'IMG_3975 a 3985 (21:25 a 21:29)', 'IMG_3986 (22:23, 82,0 s, vertical): o veredito'],
        legenda='Fomos no hambúrguer que eu chamei de “o melhor do mundo” em Madrid. A batata ganhou do hambúrguer, e os de Salvador dão um banho 🍔 Qual hamburgueria de Salvador você indica? #madrid #salvador #hamburguer #viagem',
        obj='Comentários de Salvador e do Brasil: identidade soteropolitana do Diego.',
        met='Comentários por visualização.',
        prod='dec',
        pend=[OUVIR, 'Confirmar quem fala cada parte de IMG_3986 (há duas vozes: de 42 a 58 s parece a Marina falando do hambúrguer do Diego)',
              'Não citar o nome da hamburgueria (a transcrição diz “Hundred Birgle”)', FOLHA_MAD],
    ),
    'tk20': dict(
        titulo='Lisboa em 1 manhã, tudo a pé',
        gancho='Lisboa em 1 manhã, tudo a pé.',
        conceito=('Troca de tema, mantendo o eixo “como se mover”: o metrô do aeroporto já é o Reel p828 de 21/02, 5 dias antes, '
                  'com o mesmo arquivo (IMG_4233). Aqui entra outra cena real de Lisboa: a manhã de 23/03 feita a pé, do hotel à '
                  'Praça do Comércio, Alfama, castelo e Rua Augusta, com o Elevador de Santa Justa fechado no caminho.'),
        estrutura=[('0–2 s', 'IMG_4289 (23/03 08:55, vertical), de 0,0 a 2,7 s: “o legal aqui de Portugal é que é tudo muito pertinho”. '
                             'Texto: o gancho.'),
                   ('2–6 s', 'IMG_4289, de 2,7 a 8,1 s: o Elevador de Santa Justa “parece que está fechado, a gente não vai conseguir subir”.'),
                   ('6–10 s', 'IMG_4364 (09:22, vertical), de 0,0 a 5,6 s: Praça do Comércio. Texto: “9h22”.'),
                   ('10–15 s', 'IMG_4431 (10:10, horizontal recortado), de 0,1 a 7,1 s: “pelas ruazinhas de Alfama… o bairro mais antigo”. '
                               'Texto: “10h10”.'),
                   ('15–19 s', 'IMG_4514 (12:01, vertical), de 22,0 a 28,7 s: Rua Augusta, “bem no final lá é a Praça do Comércio”. Texto: “12h01”.'),
                   ('19–21 s', 'Pergunta na tela: “a pé ou de elétrico?”')],
        mat=['IMG_4289 (23/03 08:55, 11,4 s, vertical)', 'IMG_4364 (09:22, 43,8 s, vertical)', 'IMG_4431 (10:10, 27,6 s, horizontal)',
             'IMG_4514 (12:01, 54,1 s, vertical)'],
        legenda='Uma manhã em Lisboa, tudo a pé: Praça do Comércio, Alfama, castelo e Rua Augusta. O Elevador de Santa Justa estava fechado quando a gente passou. Você faria a pé ou de elétrico? #lisboa #portugal #viagem',
        obj='Utilidade e comentários: mostrar que o centro histórico cabe numa manhã a pé, sem repetir o p828.',
        met='Salvamentos e comentários por visualização.',
        prod='dec',
        pend=[OUVIR,
              'Diego confirma que a manhã foi toda a pé (sem elétrico, tuk-tuk ou metrô)',
              'Elevador de Santa Justa: dizer só que estava fechado naquele dia (23/03/2026). Funcionamento atual: conferir na fonte oficial; não afirmar',
              'Alternativa, se o Diego preferir manter o tema do plano (metrô do aeroporto): a volta de metrô (IMG_4526 31,0 a 56,2 s, “acabou, pessoal… já quero voltar”) como despedida em POV, sem repetir a cena da ida do p828',
              FOLHA_LIS],
    ),
}


# =================================================================== SHORT (capítulo do vlog)
SHORT_CAP = {
    'lis': dict(
        titulo='Dois pastéis de nata na mesma manhã: qual ganhou?',
        gancho='Dois pastéis de nata. Qual ganhou?',
        trecho=('IMG_4290 (23/03 08:56) 19,9–36,9 s · IMG_4298 (08:59) 0,0–10,0 s · IMG_4301 (09:09) 0,4–3,4 s · '
                'IMG_4469 (10:24) 0,0–11,0 s · IMG_4471 (10:24) 0,0–27,4 s'),
        estrutura=('0–3 s: IMG_4290, “vou experimentar o meu primeiro pastel de nata aqui em Portugal” (texto: o gancho) · 3–10 s: '
                   'IMG_4298, a prova e a reação · 10–13 s: IMG_4301, “nota mil… super aprovado” · 13–20 s: IMG_4469, “no meio do '
                   'caminho nós paramos para provar mais um pastelzinho de nata… está quentinho” · 20–32 s: IMG_4471, “a pastelaria '
                   'em frente ao miradouro… eu acho melhor que o outro… um pouquinho mais doce… estou apaixonado” · 32–35 s: '
                   'pergunta “qual o seu favorito?” + card do vlog p160. Capítulo independente: não usa a noite nem os 4 restaurantes '
                   '(teaser p813).'),
        mat=['IMG_4290 (23/03 08:56, 37,2 s, horizontal: recortar 9:16)', 'IMG_4298 (08:59, 32,9 s, vertical)', 'IMG_4301 (09:09, 3,6 s, vertical)',
             'IMG_4469 (10:24, 20,1 s, vertical)', 'IMG_4471 (10:24, 27,4 s, vertical)'],
        pend=[OUVIR,
              'Cortar IMG_4469 de 11,0 a 12,1 s (lista de CORTES_DE_CUSTO, por precaução)',
              'Nomes das pastelarias: a transcrição diz “o chamado manteigaria” (IMG_4471); a primeira não tem nome. Confirmar antes de escrever',
              'IMG_4290 de 27,4 a 33,4 s confunde pastel de Belém e pastel de nata: usar só se o áudio estiver claro',
              'Confirmar quem prova e quem diz “acho melhor que o outro”',
              'Localizar a minutagem no corte final do vlog p160', FOLHA_LIS],
    ),
}


# =================================================================== STORIES
STORIES = {
    'sq03': dict(
        t='Lisboa: a primeira noite em 5 telas',
        telas=['Tela 1 · vídeo · IMG_4233 (22/03 19:16), de 0,3 a 4,3 s · texto “22/03, 19h16: o metrô sai de dentro do aeroporto”',
               'Tela 2 · vídeo · EE52D542 (exportação, quarto do hotel), de 10,8 a 18,7 s · texto “o único banheiro da europa com chuveirinho?” + figurinha de enquete “sim / não”',
               'Tela 3 · vídeo · IMG_4251 (21:57), de 6,1 a 11,9 s · texto “bacalhau com batata gratinada e queijo”',
               'Tela 4 · vídeo · IMG_4257 (22:20), de 0,3 a 9,7 s · texto “sem palavras.”',
               'Tela 5 · vídeo · noite na rua, IMG_4272 a 4278 (22:33 a 22:43, conferir na folha) · figurinha caixinha de perguntas “o que comer em lisboa?”'],
        mat=['IMG_4233', 'EE52D542-D823-4E20-9E77-D8ACDFA96E60.mp4 (exportação)', 'IMG_4251', 'IMG_4257', 'IMG_4272 a 4278',
             'Pendências: ' + OUVIR + '; cortar IMG_4233 de 5,3 a 13,3 s e IMG_4251 de 0,7 a 6,1 s; não usar IMG_4248 (fica para o p227); ' + FOLHA_LIS],
        obj='Conexão e caixinha de perguntas: recolher dicas de comida de Lisboa (material para o p227 de 29/11 e o p270).',
    ),
    'sq08': dict(
        t='Madrid: Retiro e Cibeles em 5 telas',
        telas=['Tela 1 · vídeo · IMG_3875 (20/03 12:05), de 0,1 a 9,9 s · texto “praça de cibeles, 12h05”',
               'Tela 2 · vídeo · IMG_3885 (12:15), de 11,0 a 19,0 s · texto “a puerta de alcalá tem 2 fachadas diferentes”',
               'Tela 3 · vídeo · IMG_3889 (12:18), de 0,2 a 11,3 s · texto “do nada: policiais a cavalo”',
               'Tela 4 · vídeo · IMG_3924 (12:59), de 10,4 a 15,4 s · texto “o palácio de cristal estava em reforma”',
               'Tela 5 · vídeo · IMG_3935 (13:48), de 0,3 a 6,3 s · texto “e aí começou a chover” + figurinha de enquete “parque na chuva: fica / vai embora”'],
        mat=['IMG_3875, IMG_3885, IMG_3889, IMG_3924, IMG_3935 (20/03/2026, 12h05 a 13h48)',
             'Pendências: ' + OUVIR + '; a história das 2 fachadas e “dizem que o Palácio de Linares é mal-assombrado” (IMG_3875, 28,1 a 35,5 s) são falas do Diego, não dados conferidos: não transformar em informação; a reforma era em 20/03/2026, não dizer que continua; ' + FOLHA_MAD],
        obj='Conexão e enquete leve; reaproveita o Retiro do p606 sem repetir o lago.',
    ),
}


# =================================================================== TT_ADAPT (Reels existentes)
TT_ADAPT = {
    'p227': dict(gancho='Pedimos peixe em Lisboa. Não era peixe.',
                 muda='Usar a primeira comida real de Lisboa: “peixinhos da horta” (IMG_4246 9,1 a 18,0 s e IMG_4248 0,2 a 15,2 s, 22/03 21:40: “a gente achou que era peixe, mas está muito bom”). Veredito no fim; pergunta “vale ou pula?” fixa.'),
    'p609': dict(gancho='Lisboa tem trilha sonora na rua',
                 muda='Som original do violoncelo em vez de música da biblioteca; texto só no fim (“lisboa, 11h12”). Até 12 s, em loop.'),
    'p606': dict(gancho='Madrid também tem isso',
                 muda='Abrir direto no lago (IMG_3912); “entrada livre” como texto grande; sem Placa. Até 12 s.'),
    'p224': dict(gancho='Barcelona ou Madrid? Fiz as duas.',
                 muda='Formato de tela dividida mantido; termina com a pergunta “qual você escolheria?” fixa por 3 s.'),
    'p231': dict(gancho='La Boqueria é pega-turista?',
                 muda='Abrir na fala “conhecido como pega-turista” (master 19:27); comparação com o Mercadão em texto grande.'),
    'p214': dict(gancho='O que você vê nessa janela?',
                 muda='Pergunta fixa na tela desde o início; respostas do Diego aparecem uma a uma. Até 15 s.'),
    'p244': dict(gancho='2 dias em Madrid: o roteiro real',
                 muda='Lista numerada maior no centro; sem Placa CTA; fecha com “salva pra viagem” em texto.'),
    'p605': dict(gancho='Camp Nou ou Bernabéu? Fui nos dois.',
                 muda='Tela dividida mantida; veredito do Diego no fim e pergunta “qual você visitaria?”.'),
    'p262': dict(gancho='Sagrada Família: não deixa pra depois',
                 muda='Sem preço (corte antes da frase do ingresso); antecedência só depois de conferida no site oficial.'),
    'p271': dict(gancho='Por que não ficamos no centro de Barcelona',
                 muda='Os 3 motivos em lista grande; terminar em 03:02 do master para não repetir o passe do p250.'),
    'p274': dict(gancho='Lisboa de manhã cedo',
                 muda='Sem texto até o fim; a informação real entra em 1 linha no último plano.'),
    'p257': dict(gancho='Ninguém avisou desse frio na Europa',
                 muda='Uma cidade por fala, com o nome em texto grande; pergunta final “qual foi o lugar mais frio?”.'),
}


# =================================================================== YT_ADAPT (Reels existentes)
YT_ADAPT = {
    'p227': dict(titulo='Primeira comida em Lisboa: vale ou pula?',
                 muda='Já previsto como Short p707: mesma base dos peixinhos da horta (IMG_4246 e 4248); card do vlog p160.'),
    'p609': dict(titulo='Um violoncelo na rua de Lisboa',
                 muda='Mesmo corte, som original; card do vlog p160.'),
    'p606': dict(titulo='Madrid: o lago do Retiro, de graça',
                 muda='Mesmo corte; “entrada livre” conferida na fonte oficial antes de publicar; card do vlog p97.'),
    'p224': dict(titulo='Barcelona ou Madrid: qual escolher?',
                 muda='Mesmo corte; cards dos vlogs p13 e p97.'),
    'p231': dict(titulo='La Boqueria, Barcelona: vale ou pula?',
                 muda='Já previsto como Short p708; card do vlog p13.'),
    'p214': dict(titulo='Casa Batlló: o que você vê nessa janela?',
                 muda='Mesmo corte; pergunta fixa para comentários; card do vlog p13.'),
    'p244': dict(titulo='Madrid em 2 dias: o que deu pra fazer',
                 muda='Mesmo corte; card do vlog p97.'),
    'p605': dict(titulo='Camp Nou × Bernabéu: fui nos dois',
                 muda='Mesmo corte; cards dos vlogs p13 e p97.'),
    'p262': dict(titulo='Sagrada Família: o ingresso que esgota antes',
                 muda='Já previsto como Short p713; antecedência conferida no site oficial; sem preço.'),
    'p271': dict(titulo='Barcelona: por que ficamos em Gràcia',
                 muda='Mesmo corte, terminando em 03:02 do master; card do vlog p13.'),
    'p274': dict(titulo='Lisboa de manhã cedo',
                 muda='Mesmo corte; card do vlog p160.'),
    'p257': dict(titulo='Ninguém avisou desse frio na Europa',
                 muda='Já previsto como Short p712; mesmo corte.'),
}


if __name__ == '__main__':
    # checagens rápidas: gancho ≤ 7 palavras e títulos de Short ≤ 60 caracteres
    def palavras(t):
        return len([w for w in t.replace('×', ' ').split() if w.strip('.,:?!—')])
    for k, v in list(PECAS.items()) + list(REVISOES.items()):
        if 'gancho' in v:
            assert palavras(v['gancho']) <= 7, (k, v['gancho'])
        if 'yt' in v:
            assert len(v['yt']['titulo']) <= 60, (k, v['yt']['titulo'])
    for k, v in TIKTOK.items():
        assert palavras(v['gancho']) <= 7, (k, v['gancho'])
    for k, v in list(YT_ADAPT.items()) + list(SHORT_CAP.items()):
        assert len(v['titulo']) <= 60, (k, v['titulo'])
    print('ok', len(PECAS), len(REVISOES), len(TIKTOK), len(SHORT_CAP), len(STORIES), len(TT_ADAPT), len(YT_ADAPT))
