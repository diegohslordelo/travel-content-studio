# -*- coding: utf-8 -*-
"""Reconstrói o calendário do painel a partir de 10/10/2026 com o acervo do Drive (v4, 11/10/2026).

Uso (de dentro de planejamento/):
  python3 scripts/reconstruir_v4.py --base versoes/painel-v3-2026-10-11-antes-da-v4.html
- Mantém tudo antes de 10/10/2026 como está (histórico e Stories de 09/10).
- Mantém os vídeos longos do YouTube e os Stories de lançamento e da viagem.
- Troca as peças v3 (Reels, carrosséis, Shorts e o setup) de 10/10 em diante pelas peças v4:
  peças novas (v4_pecas_a.py e v4_pecas_b.py) + peças da v3 reaproveitadas com o material do Drive (REUSO, abaixo).
- Regenera Shorts, setup da viagem, dias das semanas, Stories do dia, interações, pendências e metadados.
"""
import copy
import datetime as dt
import json
import os
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import v3_pecas_1, v3_pecas_2, v3_pecas_3, v3_pecas_4  # noqa: E402
import v4_pecas_a, v4_pecas_b  # noqa: E402
from v4_base import drv, SIM, SIM_PE, MINI, DATAS  # noqa: E402
import reconstruir_v3_lib as L  # noqa: E402

PAINEL = os.path.join(AQUI, '..', 'planejamento-postagens.html')
BASE = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else PAINEL
INICIO = '2026-10-10'

html = open(BASE, encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\n', html, re.S)
D = json.loads(m.group(1))

V3 = {p['t']: p for p in v3_pecas_1.PECAS + v3_pecas_2.PECAS + v3_pecas_3.PECAS + v3_pecas_4.PECAS}

# ───────────── peças da v3 reaproveitadas ─────────────
# (título v3, data, hora, mudanças). ma+/pe+ = itens acrescentados no início da lista de material / pendências.
REUSO = [
 ("Camisa do Bahia no Camp Nou", "2026-10-11", "19:00", dict(fm="Primeiro dia · identidade", te="T3:A",
   **{'ma+': [drv("Barcelona", "IMG_0549 a IMG_0562 (Diego de camisa do Bahia na Barça Store, no metrô e na Plaça d'Espanya, com a Marina), IMG_0502 a IMG_0543 (chegada ao estádio e salas do museu: troféus, telão, sala imersiva)")],
      'pe+': ["Cenas sem fala saem dos brutos do Drive (IMG_0502–0562), não do master", MINI]})),
 ("Roteiro do primeiro dia em Barcelona: 18 km a pé", "2026-10-14", "18:00", dict(fm="Roteiro", te="T4:A",
   **{'ma+': [drv("Barcelona", "dia 1 completo, IMG_0487 a IMG_0816: metrô (0489–0493), Camp Nou (0495–0543), Barça Store (0549–0552), Plaça d'Espanya e MNAC (0555–0581), vista de Montjuïc (0584–0594), Colombo e Port Vell (0623–0639), McDonald's (0640–0651), El Vaso de Oro (0661–0665), Barceloneta (0688–0697), Ciutadella (0702–0735), Arco do Triunfo (0775–0783), patatas bravas (0816)")],
      'pe+': ["Fotos dos slides: quadros dos brutos 4K do Drive no lugar do master", MINI]})),
 ("Não compre água em Barcelona", "2026-10-17", "11:00", dict(fm="Dica", te="T5:A",
   **{'ma+': [drv("Barcelona", "IMG_1029 (Diego enchendo a garrafa na fonte de Canaletes, na Rambla; também na pasta REELS), IMG_1029-1, IMG_1030 (outros ângulos), IMG_0869 (Marina bebendo da garrafa)")],
      'pe+': ["Plano da fonte encontrado (IMG_1029): abrir o Reel com ele e usar o master só para a fala do app", MINI]})),
 ("Primeira hora em Amsterdam: frio e fome", "2026-10-20", "18:30", dict(fm="Primeira hora · POV", te="T3:A",
   **{'ma+': [drv("Amsterdam", "IMG_1369 a IMG_1373 (asa do avião, nuvens e turbinas eólicas na descida), IMG_1375 (aeroporto), IMG_1376 a IMG_1380 (ônibus para a cidade), IMG_1384 e IMG_1385 (rua com malas, frio), IMG_1393 (Museumplein), IMG_1414 a IMG_1417 (primeira pizza: New York Pizza)")],
      'pe+': ["Fechar com a pizza (IMG_1416–1417): é a resposta real à fome do gancho", MINI]})),
 ("Paris: chegamos e o jardim estava fechado", "2026-10-22", "12:30", dict(fm="Perrengue real")),
 ("Vale ou pula: waffle de rua em Bruges", "2026-10-27", "18:30", dict(fm="Vale ou pula · comida",
   **{'ma+': [drv("Bruges", "IMG_2685 a IMG_2703 (balcão com o quadro “Classics”, waffle na chapa, Marina e Diego comendo na rua) e IMG_2635 a IMG_2640 (vitrine e waffle com bandeirinha)")],
      'pe+': ["Os IMG_2690–2692.MOV do Drive devem ser os originais (as cópias do repositório eram 720p): conferir a resolução", "O quadro “Classics” (IMG_2685) mostra os preços: conferir o do waffle comprado", MINI]})),
 ("8 cidades, 8 primeiros dias", "2026-11-03", "18:30", dict(fm="Série · montagem", te="T3:A", st="sim",
   **{'pe+': ["Barcelona, Amsterdam, Bruxelas e Bruges já têm planos no Drive; Paris (parcial), Disney, Madrid e Lisboa ainda não: trocar os planos simulados quando subirem"]})),
 ("Roma de graça (ou quase): o que vimos sem pagar", "2026-11-04", "18:00", dict(fm="Lista · de graça", te="T4:A")),
 ("€ 1 cada, só às quartas: 100 Montaditos", "2026-11-05", "12:30", dict(fm="Preço", te="T5:A",
   **{'ma+': [drv("REELS", "IMG_1339 (montaditos na mesa, com o cardápio) e IMG_1341 (tapa de perto)")], 'pe+': [MINI]})),
 ("A Torre Eiffel pisca de hora em hora", "2026-11-07", "11:00", dict(fm="Curiosidade", te="T1:B", st="sim",
   **{'ma+': [SIM], 'pe+': [SIM_PE]})),
 ("Primeiro dia em Paris (e era o único)", "2026-11-08", "19:00", dict(fm="Corte do vlog · primeiro dia", te="T3:A",
   **{'pe+': ["Sai no dia seguinte ao vlog de Paris (07/11): a última linha da legenda pode citar o vlog no YouTube"]})),
 ("Bate-volta de Bruxelas a Bruges: como fizemos", "2026-11-11", "18:00", dict(fm="Roteiro · transporte", te="T4:B",
   **{'ma+': [drv("Bruges", "IMG_2417 (máquina de bilhete da estação), IMG_2420 a IMG_2427 (caminho a pé), IMG_2641 a IMG_2681 (Begijnhof e Minnewater), IMG_2438 a IMG_2482 (Markt e Burg), IMG_2484 a IMG_2494 (canais)")],
      'pe+': ["Ida e volta de trem e o caminho a pé estão filmados; falta só o preço do bilhete e os horários"]})),
 ("Barcelona ou Madrid: qual escolher?", "2026-11-12", "12:30", dict(fm="Comparação", te="T5:B", st="sim",
   **{'ma+': [SIM + " (lado de Madrid)"], 'pe+': [SIM_PE]})),
 ("McDonald's da Espanha × do Brasil", "2026-11-19", "12:30", dict(fm="Comparação · humor", te="T5:B",
   **{'ma+': [drv("Barcelona", "IMG_0640 e IMG_0641 (Marina no totem), IMG_0642 a IMG_0651 (os dois comendo, sanduíche de perto)")], 'pe+': [MINI]})),
 ("A passagem é só o começo (antes da Black Friday)", "2026-11-24", "18:30", dict(fm="Preço · sazonal")),
 ("Vale ou pula: La Boqueria", "2026-11-29", "19:00", dict(fm="Vale ou pula", te="T5:A",
   **{'ma+': [drv("Barcelona", "IMG_1035 a IMG_1047 (entrada da Boqueria, banca Vidal Pons, corredor cheio, selfies dos dois)")], 'pe+': [MINI]})),
 ("Sagrada Família: projetada como uma floresta", "2026-12-08", "18:30", dict(fm="Desejo · curiosidade", te="T2:A", st="ok",
   **{'ma+': [drv("REELS", "IMG_1152, IMG_1154 (colunas e teto da Sagrada por dentro), IMG_1174 (vitrais coloridos), IMG_1192 e IMG_1208 (fachadas)")], 'pe+': [MINI]})),
 ("Natal em Roma: o que fizemos no dia 25", "2026-12-16", "18:00", dict(fm="Roteiro · sazonal", te="T4:B")),
 ("Expectativa × realidade: Amsterdam", "2026-12-22", "18:30", dict(fm="Expectativa × realidade",
   **{'ma+': [drv("Amsterdam", "chuva: IMG_1536 e IMG_1537 (Marina de guarda-chuva), IMG_1647 a IMG_1652 (Museumplein com poças); sol: IMG_1874 a IMG_1908; frio: IMG_1384, IMG_1385")],
      'pe+': ["Material de “realidade” encontrado; falta a “expectativa” nas palavras do Diego"]})),
 ("Vista de Barcelona do alto do Montjuïc", "2026-12-26", "11:00", dict(fm="Desejo", te="T1:A", st="ok",
   **{'ma+': [drv("Barcelona", "IMG_0584 a IMG_0590 (vista do alto do MNAC, músico na escadaria), IMG_0555 a IMG_0581 (Plaça d'Espanya, colunas e MNAC)")], 'pe+': ["IMG_0586 tem músico de rua no áudio: trocar o som por música da biblioteca", MINI]})),
 ("Ninguém avisou desse frio", "2026-12-29", "18:30", dict(fm="Identificação · humor",
   **{'ma+': [drv("Amsterdam", "IMG_1384, IMG_1385 (rua com malas, frio)"), drv("Bruges", "IMG_2692, IMG_2697 a IMG_2700 (Marina de luvas e casaco)")]})),
 ("Amsterdam em 3 dias: o roteiro que fizemos", "2026-12-30", "18:00", dict(fm="Roteiro", te="T4:B", st="ok",
   **{'ma+': [drv("Amsterdam", "dia 1 provável (IMG_1369–1531): chegada, canais, Dam, New York Pizza, batata da Manneken Pis, Tony's, Kalverstraat, Munttoren, bar à noite; dia 2 (IMG_1536–1845): chuva, Anne Frank, Albert Cuyp, stroopwafel, Rijksmuseum, Vondelpark, Bloemenmarkt, Fabel Friet, pizzaria, Albert Heijn; dia 3 (IMG_1866–2096): parque, bar, Heineken Experience, pôr do sol rosa, Dam à noite, malas")],
      'pe+': ["Divisão por dia inferida pela numeração e pela luz: confirmar com o Diego", MINI]})),
 ("Sagrada Família: o ingresso que precisa de antecedência", "2027-01-05", "18:30", dict(fm="Dica · erro",
   **{'ma+': [drv("REELS", "IMG_1152, IMG_1154, IMG_1174 (interior), IMG_1192 (fachada)")]})),
 ("Quanto custou cada cidade (por dia, por pessoa)", "2027-01-06", "18:00", dict(fm="Preço · comparação", te="T4:B")),
 ("Casa Batlló: o que você vê nessa janela?", "2027-01-09", "11:00", dict(fm="Pergunta",
   **{'ma+': [drv("Barcelona", "IMG_1083 a IMG_1096 (Casa Batlló de dia e no fim da tarde, selfies dos dois), IMG_1099 a IMG_1105 (Casa Milà)")], 'pe+': [MINI]})),
 ("Próximo primeiro dia: [cidade 1]", "2027-01-10", "19:00", dict(fm="Anúncio da viagem", te="T3:A")),
 ("Onde ver a Torre Eiffel de graça", "2027-01-12", "18:30", dict(fm="Dica · de graça")),
 ("Itália em 9 dias: € [total]", "2027-01-13", "18:00", dict(fm="Preço", te="T4:A")),
 ("Barcelona: o Gaudí que dá pra ver de graça (e o que pagamos)", "2027-01-20", "18:00", dict(fm="Lista · de graça", te="T4:A",
   **{'ma+': [drv("Barcelona", "IMG_0862 a IMG_0864 (Casa Vicens), IMG_0986 (poste do Gaudí na Plaça Reial), IMG_1083 a IMG_1105 (Batlló e Milà)"), drv("REELS", "IMG_1246, IMG_1286, IMG_1320, IMG_1331 (Park Güell: vista, sala hipóstila, dragão)")], 'pe+': [MINI]})),
 ("Vale a pena ir a Barcelona? A resposta no aeroporto", "2027-01-21", "12:30", dict(fm="Corte do vlog · veredito", te="T3:B")),
 ("Madrid em 2 dias: € [total]", "2027-01-27", "18:00", dict(fm="Preço", st="dad")),
 ("Qual cidade foi a mais barata?", "2027-02-04", "12:30", dict(fm="Comparação · preço", te="T5:B")),
 # viagem de janeiro (sem mudança de conteúdo)
 ("Primeiro dia em [cidade 1], ao vivo", "2027-01-23", "11:00", dict(fm="Ao vivo")),
 ("Primeira hora em [cidade 2]: € [valor real]", "2027-01-26", "18:30", dict(fm="Ao vivo")),
 ("Primeiro dia em [cidade 2 ou 3], ao vivo", "2027-01-30", "11:00", dict(fm="Ao vivo")),
 ("Vale ou pula: [atração da viagem], ao vivo", "2027-02-02", "18:30", dict(fm="Ao vivo")),
 ("[Cidade 1]: o primeiro dia em números", "2027-02-03", "18:00", dict(fm="Ao vivo · roteiro")),
 ("Primeiro dia em [cidade 3], ao vivo", "2027-02-06", "11:00", dict(fm="Ao vivo")),
 ("3 países, [N] primeiros dias: o balanço", "2027-02-07", "19:00", dict(fm="Ao vivo · balanço")),
]

def reuso(t, d, h, mud):
    pc = copy.deepcopy(V3[t])
    pc['d'], pc['h'] = d, h
    pc['te'] = mud.get('te', pc.get('te'))
    for k in ('fm', 'st', 'pl'):
        if k in mud:
            pc[k] = mud[k]
    pc['ma'] = mud.get('ma+', []) + pc['ma']
    pc['pe'] = mud.get('pe+', []) + pc['pe']
    pc['reuso'] = True
    return pc

PECAS = v4_pecas_a.PECAS + v4_pecas_b.PECAS + [reuso(*r) for r in REUSO]
PECAS.sort(key=lambda x: (x['d'], x['h']))

# ───────────── conferências ─────────────
datas = [p['d'] for p in PECAS]
assert len(datas) == len(set(datas)), [d for d, n in Counter(datas).items() if n > 1]
v3_slots = {(p['d'], p['h'], p['f']) for p in V3.values() if p['d'] >= INICIO}
v4_slots = {(p['d'], p['h'], p['f']) for p in PECAS}
assert v3_slots == v4_slots, (sorted(v3_slots - v4_slots), sorted(v4_slots - v3_slots))
seq, run, pior = None, 0, 0
for p in PECAS:
    run = run + 1 if p['k'] == seq else 1
    seq = p['k']
    pior = max(pior, run)
    assert run <= 3, ('mais de 3 seguidas', p['d'], p['k'])
ganchos = [p['g'] for p in PECAS if not p['g'].startswith('(')]
assert len(ganchos) == len(set(ganchos)), [g for g, n in Counter(ganchos).items() if n > 1]

# ───────────── metadados ─────────────
ST = {'ok': 'Material verificado (Drive ou repositório)', 'dec': 'Decupagem pendente', 'dad': 'Aguarda dados do Diego',
      'sim': 'Material simulado (pasta do Drive vazia)', 'fut': 'Material futuro (viagem de janeiro)'}
L.ST.clear(); L.ST.update(ST)

WEEKS = {
 1: dict(tag='Base publicada + Atomium refeito', obj='Fechar a base e recomeçar a v4 pelo Atomium (10/10), agora com os 15 vídeos de Bruxelas do Drive',
         metas=['Atomium refeito (10/10; se não saiu, sai hoje às 11:00)', 'Bahia no Camp Nou (11/10)', 'Linha de base de 08/10 registrada'],
         observe=['Atomium v4 × a versão de 2 vídeos: retenção média e envios por alcance.', 'Sábado 10/10: o vlog de Barcelona saiu no YouTube.']),
 2: dict(tag='Quatro cidades numa semana', obj='Amsterdam, Barcelona, Bruges e Bruxelas em 6 dias: o perfil é de várias cidades',
         metas=['4 Reels + 1 carrossel', 'Diego sobe Paris, Disney, Madrid e Lisboa no Drive', 'Ouvir o áudio dos brutos das peças da semana 3'],
         observe=['Tony\'s (13/10): primeiro Reel de curiosidade de marca.', 'Primeira hora em Bruges (15/10): seguidores por 1.000 (T3, B).', '3 estátuas (18/10): comentários.']),
 3: dict(tag='Amsterdam no YouTube', obj='Amsterdam na semana do vlog (24/10) e o primeiro “corte do vlog” no domingo',
         metas=['4 Reels + 1 carrossel', 'Primeiro corte do vlog (25/10)'],
         observe=['Corte do vlog (25/10) × Reels feitos do bruto: retenção e salvamentos.', 'Primeira hora em Amsterdam (20/10): seguidores por 1.000 (T3, A).']),
 4: dict(tag='Leitura 1 (01/11)', obj='Comida de Amsterdam, beijo de Barcelona, Disney no Halloween e Lisboa à noite; Leitura 1 no domingo',
         metas=['4 Reels + 1 carrossel', 'Leitura 1 registrada', 'Decidir horários pelo Insights'],
         observe=['Carrossel de comida (28/10, capa papel) × roteiro de Bruxelas (21/10, capa foto): T4.', 'Primeiras médias por formato editorial (POV, curiosidade, comida, corte do vlog).']),
 5: dict(tag='Série e Paris', obj='Explicar a série (8 cidades) e abrir Paris na semana do vlog (07/11)',
         metas=['4 Reels + 1 carrossel', 'Fixar o “8 primeiros dias” se converter mais que a apresentação'],
         observe=['Seguidores por 1.000 do Reel de 03/11.', 'Corte do vlog de Paris (08/11).']),
 6: dict(tag='Comparações e Madrid', obj='Bruges em bate-volta, Barcelona × Madrid e o primeiro dia em Madrid',
         metas=['4 Reels + 1 carrossel', 'Custos de Amsterdam recebidos'],
         observe=['T5: Barcelona ou Madrid (12/11) × Reels de cidade única.', 'Batata frita belga (10/11): envios.']),
 7: dict(tag='Semana da Disney', obj='Disney de ponta a ponta na semana do vlog (21/11): trem, roteiro, castelo e veredito',
         metas=['4 Reels + 1 carrossel', 'Pasta da Disney preenchida até 14/11'],
         observe=['Salvamentos do RER (17/11) e do roteiro (18/11).', 'Corte do vlog da Disney (22/11).']),
 8: dict(tag='Black Friday', obj='Custos reais na semana em que muita gente compra passagem',
         metas=['4 Reels + 1 carrossel'],
         observe=['Envios do “A passagem é só o começo” (24/11).', 'Roma 2026 (25/11): salvamentos com capa papel.']),
 9: dict(tag='Leitura 2 (06/12)', obj='Fechar novembro, abrir Madrid no YouTube e fazer a Leitura 2',
         metas=['4 Reels + 1 carrossel', 'Leitura 2 registrada', 'Pasta de Madrid preenchida até 28/11'],
         observe=['T1, T2 e T4: conclusões preliminares.', 'Qual formato editorial trouxe mais seguidores por 1.000?']),
 10: dict(tag='Desejo e humor', obj='Sagrada por dentro, McDonald\'s de Bruges, Vondelpark e o croissant de Paris',
          metas=['4 Reels + 1 carrossel'],
          observe=['Sagrada (08/12, T2 A) × Vondelpark (12/12, T2 B): retenção.', 'Comentários do McDonald\'s (10/12) e do croissant (13/12).']),
 11: dict(tag='Bruxelas no YouTube', obj='Bruxelas na semana do vlog (19/12) e Natal em Roma no carrossel',
          metas=['4 Reels + 1 carrossel'],
          observe=['Salvamentos do carrossel de Natal (16/12).', 'Corte do vlog de Bruxelas (19/12).']),
 12: dict(tag='Semana do Natal', obj='Amsterdam à noite na véspera, Paris em 1 dia e Montjuïc',
          metas=['4 Reels + 1 carrossel', 'Agendar 24/12 e 27/12 com antecedência'],
          observe=['Envios do Reel de 24/12.', 'Não comparar a semana de festas com as outras sem levar o feriado em conta.']),
 13: dict(tag='Réveillon', obj='Frio, Amsterdam em 3 dias, Disney no fim do ano e Bruges no YouTube (02/01)',
          metas=['4 Reels + 1 carrossel', 'Custos de todas as cidades recebidos até 30/12'],
          observe=['Comentários do frio (29/12).', 'Semana atípica: registrar, mas não decidir por ela.']),
 14: dict(tag='Leitura 3 (10/01) e anúncio', obj='Planejamento de 2027: ingresso da Sagrada, custo por cidade, Prado e o anúncio da viagem',
          metas=['4 Reels + 1 carrossel', 'Leitura 3 registrada', 'Bio com o próximo destino'],
          observe=['T3 e T5: conclusão.', 'Seguidores do anúncio da viagem (10/01).']),
 15: dict(tag='Lisboa no YouTube e pré-viagem', obj='Lisboa na semana do vlog (16/01) e todas as peças do acervo até 04/02 prontas',
          metas=['4 Reels + 1 carrossel', 'Peças de 19/01 a 04/02 do acervo editadas até 15/01'],
          observe=['Corte do vlog de Lisboa (17/01).', 'Salvamentos do “Itália em 9 dias” (13/01).']),
 16: dict(tag='Viagem: partida', obj='Começar a viagem com o acervo agendado e o primeiro dia ao vivo em 23/01',
          metas=['3 Reels do acervo agendados', 'Primeiro dia ao vivo com Placar real', 'Registro de campo diário'], trip=True,
          observe=['Primeiro Reel com Placar real (23/01): seguidores por 1.000 contra os primeiros dias do acervo.']),
 17: dict(tag='Viagem', obj='Alternar ao vivo (primeira hora, primeiro dia) e acervo agendado',
          metas=['2 Reels ao vivo + 2 do acervo + 1 carrossel', 'Editar ao vivo em até 2 dias'], trip=True,
          observe=['Envios da primeira hora ao vivo (26/01).']),
 18: dict(tag='Viagem e Leitura 4', obj='Fechar a viagem, o ciclo e fazer a Leitura 4',
          metas=['3 Reels ao vivo + 1 do acervo + 1 carrossel', 'Leitura 4 em 07/02'], trip=True,
          observe=['Leitura 4: o que vira regra do próximo ciclo.']),
}

PEND = [
 dict(k=30, t='Subir no Drive os vídeos de Paris, Disney, Madrid e Lisboa (pastas vazias em 11/10). As peças dessas cidades estão com material simulado e mudam quando os vídeos chegarem', type='text'),
 dict(k=31, t='Ouvir o áudio dos brutos antes de cortar: a decupagem de 11/10 foi feita por miniatura (1 quadro por arquivo)', type='text'),
 dict(k=32, t='Datas das viagens (a ordem BCN → AMS → BXL → BRG → PAR → DIS → MAD → LIS vem da numeração dos arquivos; datas prováveis em março de 2026) para a cotação PTAX', type='text'),
 dict(k=33, t='Custos por cidade e por pessoa: Barcelona, Amsterdam (inclui Heineken), Bruxelas, Bruges (trem), Paris, Disney, Madrid, Lisboa, Florença, Veneza, Milão', type='text'),
 dict(k=34, t='Confirmar o conteúdo exato das 7 publicações até 08/10 para não repetir valores e cenas', type='text'),
 dict(k=35, t='Barcelona, dia 3: a pasta Barcelona vai até o dia 2; Sagrada, Park Güell, churros e 100 Montaditos só estão na pasta REELS. Há mais brutos do dia 3?', type='text'),
 dict(k=36, t='Itália: o Drive tem só as fotos de Roma (sem vídeo). Itália fica em carrossel (CLAUDE.md, 10). Fotos e custos de Florença, Veneza e Milão ainda não chegaram', type='text'),
 dict(k=37, t='Viagem de janeiro: cidades, ordem e datas', type='text'),
 dict(k=38, t='Verificar no app se Trial Reels está disponível; se estiver, usar nos testes T1 e T2'),
 dict(k=39, t='Gravar os sons PD_*.wav e fechar o kit de PNG (CLAUDE.md, pendência 7)'),
]

# ───────────── montar posts ─────────────
hist = [p for p in D['posts'] if p['d'] < INICIO]
KEEP_KINDS = {'long', 'stories_launch', 'stories_count', 'stories_partida', 'stories_embarque'}
kept = [p for p in D['posts'] if p['d'] >= INICIO and p['kind'] in KEEP_KINDS]
removed = [p for p in D['posts'] if p['d'] >= INICIO and p['kind'] not in KEEP_KINDS]

# IDs: a peça que tem o mesmo título de uma peça v3 herda o ID dela (o progresso salvo no navegador continua valendo)
ID_V3 = {p['titulo']: p['id'] for p in removed if p['kind'] in ('v3_reel', 'v3_car')}
new = []
nr = nc = 0
for i, pc in enumerate(PECAS):
    if pc['f'] == 'R':
        nr += 1; n = nr
    else:
        nc += 1; n = nc
    p = L.to_post(pc, ID_V3.get(pc['t'], 'p%d' % (500 + i)), n)
    p['fmed'] = pc.get('fm', '')
    p['como'] = ('Formato: ' + pc['fm'] + ' · ' if pc.get('fm') else '') + p['como']
    p['v4'] = True
    if pc.get('reuso'):
        p['obs'].append('Peça da v3 reaproveitada na v4, com o material do Drive acrescentado em Material e Pendências.')
    new.append(p)

shorts = L.make_shorts(new, D['end'], 700)
setup = L.make_setup()
setup['id'] = 'p699'

posts = hist + kept + new + shorts + [setup]
posts.sort(key=lambda p: (p['d'], '00:00' if p['hora'] == '—' else p['hora']))
L.fill_weeks(D, posts, WEEKS, INICIO)

D['posts'] = posts
D['versao'] = 'v4 · 11/10/2026 (acervo do Drive)'
D['pend'] = PEND
D['stmat'] = ST

out = html[:m.start(1)] + json.dumps(D, ensure_ascii=False) + html[m.end(1):]
# selo do status "simulado" no card Produção
out = out.replace("({ok:'b-pub',dec:'b-warn',dad:'b-warn',fut:'b-info'}[p.prod]||'')", "({ok:'b-pub',dec:'b-warn',dad:'b-warn',sim:'b-info',fut:'b-info'}[p.prod]||'')")
open(PAINEL, 'w', encoding='utf-8').write(out)

# ───────────── relatório ─────────────
v4 = [p for p in posts if p.get('v4')]
print('antes de 10/10 mantidos:', len(hist), '| mantidos do futuro (YouTube e Stories):', len(kept), '| removidos (v3):', len(removed), '| peças v4:', len(v4), '| shorts:', len(shorts))
print('novas:', sum(1 for p in PECAS if not p.get('reuso')), '| reaproveitadas da v3:', sum(1 for p in PECAS if p.get('reuso')))
print('por formato:', dict(Counter(p['fmt'] for p in v4)))
print('por pilar:', dict(Counter(p['pilar'] for p in v4)))
print('por destino:', dict(Counter(p['video'] for p in v4)))
print('reels por destino:', dict(Counter(p['video'] for p in v4 if p['fmt'] == 'Reel')))
print('por status:', dict(Counter(ST[p['prod']] for p in v4)))
print('formato editorial (1ª palavra):', dict(Counter(p['fmed'].split(' ·')[0] for p in v4)))
print('testes:', dict(Counter((p['teste'] or {}).get('id', '—') + ':' + (p['teste'] or {}).get('var', '') for p in v4)))
print('maior sequência da mesma cidade:', pior)
