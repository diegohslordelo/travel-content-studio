# -*- coding: utf-8 -*-
"""Reconstrói o bloco DATA de planejamento/planejamento-postagens.html para a estratégia v3.

Uso (de dentro de planejamento/):  python3 scripts/reconstruir_v3.py
- Mantém intactas as publicações até 08/10/2026 (marcadas como publicadas, com os números da auditoria de 08/10).
- Mantém os vídeos longos do YouTube, os Stories de lançamento deles e os Stories da viagem.
- Remove o resto do plano futuro antigo e insere as peças de scripts/v3_pecas_*.py a partir de 09/10/2026.
- Gera Shorts (reaproveitamento), semanas, Stories do dia, interações, testes, pendências e metadados.
Lê o painel atual (ou --base caminho) e grava o painel atualizado.
"""
import datetime as dt
import json
import re
import sys
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import v3_pecas_1, v3_pecas_2, v3_pecas_3, v3_pecas_4  # noqa: E402

PAINEL = os.path.join(AQUI, '..', 'planejamento-postagens.html')
BASE = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else PAINEL
CORTE = '2026-10-08'   # marco zero: tudo até aqui foi publicado
INICIO = '2026-10-09'

html = open(BASE, encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\n', html, re.S)
D = json.loads(m.group(1))
OLD = {p['id']: p for p in D['posts']}

# ───────────── metadados ─────────────
DEST = {
 'bcn': 'Barcelona', 'ams': 'Amsterdam', 'bxl': 'Bruxelas', 'brg': 'Bruges', 'par': 'Paris',
 'dis': 'Disneyland Paris', 'mad': 'Madrid', 'lis': 'Lisboa', 'ita': 'Itália', 'multi': 'Vários destinos',
 'jan': 'Viagem de janeiro', 'all': 'Retrospectiva'}
PIL = {
 'DESEJO': 'Vontade de ir',
 'UTIL': 'Chegar sabendo',
 'EXP': 'Como foi de verdade',
 'SERIE': 'Primeiro Dia (série)'}
PIL_DESC = {
 'DESEJO': 'Desejo: fazer a pessoa se imaginar no lugar e mandar para quem iria junto. Descoberta e envios.',
 'UTIL': 'Utilidade: preço real, roteiro, dica e erro. Salvamentos, envios e prova de valor do perfil.',
 'EXP': 'Identificação: a viagem como foi (perrengue, humor, prova, opinião). Comentários e conexão com o Diego.',
 'SERIE': 'Identidade: o primeiro dia de cada cidade e o que o perfil promete. Conversão em seguidores.'}
ST = {'ok': 'Material verificado no repositório', 'dec': 'Decupagem pendente', 'dad': 'Aguarda dados do Diego', 'fut': 'Material futuro (viagem de janeiro)'}

TESTES = [
 dict(id='T1', nome='Desejo puro × desejo com 1 informação', pilar='Vontade de ir',
      variavel='Camada de informação (preço, hora, “grátis”, como chegar) num Reel de desejo de 12 a 16 s',
      hip='Desejo com 1 informação útil converte mais visitantes em seguidores que desejo puro, sem perder envios.',
      met='Seguidores por 1.000 visualizações', sec='Envios por alcance · % de não seguidores · retenção média',
      comp='Médias A × B com 5 Reels cada (conclusão preliminar); conclusão com 10.',
      origem='POV de 04/10: 98% de não seguidores, 1.946 visualizações e só 3 seguidores (≈ 1,5 por 1.000).'),
 dict(id='T2', nome='Gancho escrito × gancho só visual', pilar='Vontade de ir',
      variavel='Texto de gancho (até 7 palavras) nos 2 primeiros segundos; a Placa Marca entra nos dois',
      hip='O gancho escrito segura mais nos 3 primeiros segundos do que só a imagem.',
      met='Retenção média (ou % que passa dos 3 s, se o Insights mostrar)', sec='% de não seguidores · envios',
      comp='4 a 5 Reels por variante, mesmo formato (desejo, 15 s).',
      origem='Pergunta aberta: a amostra de 08/10 não separa gancho de tema.'),
 dict(id='T3', nome='CTA de seguir × CTA de enviar', pilar='Primeiro Dia (série)',
      variavel='Frase final e CTA da legenda: “segue pra ver a próxima” × “manda pra quem…”',
      hip='Nos Reels de série, pedir para seguir traz mais seguidores por 1.000 visualizações; pedir envio traz mais envios.',
      met='Seguidores por 1.000 visualizações', sec='Envios por alcance',
      comp='Reels de série e identidade, 5 por variante.',
      origem='A apresentação (CTA implícito de seguir) trouxe 114 seguidores; o POV, sem CTA, 3.'),
 dict(id='T4', nome='Carrossel: capa de foto × capa de papel', pilar='Chegar sabendo',
      variavel='Capa do carrossel: foto com pessoa/lugar e placa × papel com recibo ou rota',
      hip='Capa de foto alcança mais não seguidores; capa de papel gera mais salvamentos por alcance.',
      met='Salvamentos por alcance', sec='% de não seguidores · envios',
      comp='8 carrosséis por variante até 07/02; todos com música da biblioteca.',
      origem='Roma € 421,50 (06/10): 12% de não seguidores e 2 salvamentos em 628 visualizações.'),
 dict(id='T5', nome='Cidade única × comparação entre cidades', pilar='Chegar sabendo',
      variavel='Assunto do Reel utilitário: uma cidade × duas ou mais cidades',
      hip='Comparar cidades gera mais envios e comentários que um Reel de cidade única.',
      met='Envios por alcance', sec='Comentários por alcance · salvamentos',
      comp='4 a 5 Reels por variante.',
      origem='Sem dado anterior: hipótese nova.'),
]

BASELINE = [
 dict(id='p1', nome='Primeiro Dia (apresentação, fixado)', vis=3590, nseg=77, sav=4, env=41, seg=114, obs='Recebeu envios de pessoas próximas no lançamento'),
 dict(id='p5', nome='POV: 20s em Barcelona', vis=1946, nseg=98, sav=6, env=11, seg=3, obs=''),
 dict(id='p2', nome='3 coisas Barcelona', vis=693, nseg=82, sav=1, env=10, seg=1, obs=''),
 dict(id='p7', nome='Roma € 421,50 (carrossel)', vis=628, nseg=12, sav=2, env=2, seg=0, obs=''),
 dict(id='p3', nome='Barceloneta', vis=524, nseg=42, sav=0, env=3, seg=0, obs='Associação com o post do painel provável, a confirmar'),
 dict(id='p8', nome='Barcelona 2027?', vis=505, nseg=17, sav=1, env=0, seg=0, obs='Associação com o post do painel provável, a confirmar'),
 dict(id='p9', nome='Quanto custa Barcelona', vis=264, nseg=81, sav=2, env=11, seg=0, obs='Medido cerca de 2 h depois de publicar'),
]

LEITURAS = [
 dict(n=1, d='2026-11-01', t='Leitura 1', o='14 Reels v3 + 7 da base. Decidir: horário (Insights > Público), primeiras médias por pilar e se o formato “primeira hora / primeiro dia” converte melhor que desejo puro. Revisar os fixados.'),
 dict(n=2, d='2026-12-06', t='Leitura 2', o='≈ 35 Reels. Conclusões preliminares de T1, T2 e T4. Ajustar a proporção de pilares das semanas 10 a 18 (sem trocar as peças sazonais).'),
 dict(n=3, d='2027-01-10', t='Leitura 3', o='≈ 52 Reels. Fechar T3 e T5. Escolher o tipo de gancho e o CTA padrão dos Reels ao vivo da viagem.'),
 dict(n=4, d='2027-02-07', t='Leitura 4', o='Balanço do ciclo: o que vira regra (registrar na referência de conteúdo, seção 10, com aprovação do Diego) e plano do próximo ciclo.'),
]

PEND = [
 dict(k=30, t='Confirmar o conteúdo exato das 7 publicações até 08/10 (sobretudo “Barceloneta”, “Barcelona 2027?” e “Quanto custa Barcelona”) para não repetir valores e cenas', type='text'),
 dict(k=31, t='Datas das viagens de Barcelona a Lisboa (cotação PTAX e contexto de estação). Ordem real das 8 cidades', type='text'),
 dict(k=32, t='Custos por cidade e por pessoa: Barcelona, Amsterdam, Bruxelas, Bruges, Paris, Disney, Madrid, Lisboa, Florença, Veneza, Milão e trens da Itália', type='text'),
 dict(k=33, t='Decupagem dos brutos de Amsterdam, Bruges, Bruxelas, Paris, Disney, Madrid e Lisboa (lista de planos com minutagem): ver INVENTARIO_ACERVO.md', type='text'),
 dict(k=34, t='Inventário da Itália: vídeos ambientais (quais cidades e lugares) e fotos de Florença, Veneza e Milão; cidade do Réveillon de 2024', type='text'),
 dict(k=35, t='Brutos limpos de Barcelona (o master tem violão sob o B-roll e etiquetas gráficas): localizar os originais do interior da Sagrada Família, Park Güell e Montjuïc', type='text'),
 dict(k=36, t='Viagem de janeiro: cidades, ordem e datas (Alemanha, Áustria e Praga a confirmar)', type='text'),
 dict(k=37, t='Verificar no app se Trial Reels está disponível (fontes divergem: 200 seguidores em conta profissional, segundo a central de ajuda citada por terceiros, ou 1.000). Se estiver, usar nos testes T1 e T2'),
 dict(k=38, t='Aplicar as recomendações de bio, fixados e destaques (ESTRATEGIA_EDITORIAL_V3.md, seção 7)'),
 dict(k=39, t='Gravar os sons PD_*.wav e fechar o kit de PNG (DS, pendência 7 do CLAUDE.md): sem eles, os Reels saem sem os efeitos sonoros'),
]

WEEKS = {
 1: dict(tag='Base publicada + início da v3', obj='Fechar a base (01–08/10, publicada) e começar a v3 em 09/10 com 2 cidades diferentes no fim de semana',
         metas=['Registrar a linha de base de 08/10', 'Bio e fixados revisados', 'Atomium (10/10) e Bahia (11/10)'],
         observe=['Linha de base de seguidores por 1.000 visualizações: apresentação ≈ 31,8; POV ≈ 1,5; demais ≈ 0 a 1,4.', '“Quanto custa Barcelona”: completar os números de 48 h (tinha 11 envios em 2 h).', 'Sábado 10/10: o vlog de Barcelona sai no YouTube; o Instagram segue o plano próprio.']),
 2: dict(tag='Rodízio de cidades', obj='Mostrar em uma semana que o perfil é de várias cidades: Barcelona, Paris, Roma e Bruges',
         metas=['4 Reels + 1 carrossel', 'Decupagem de Bruges, Amsterdam e Paris iniciada', 'Diego envia datas das viagens e custos que faltam'],
         observe=['Envios por alcance da dica da água (13/10): primeiro ponto do teste T5.', 'Salvamentos do roteiro de 18 km (14/10) contra o carrossel de Roma (2 em 628).', 'T1: o Reel de Roma (17/10) é o primeiro ponto B.']),
 3: dict(tag='Texto × imagem', obj='Abrir os testes T2 (gancho escrito × visual) e T3 (CTA de seguir) com Amsterdam, Barcelona, Roma e Bruges',
         metas=['4 Reels + 1 carrossel', 'Decupagem de Disney, Madrid e Lisboa iniciada', 'Responder todos os comentários na 1ª hora'],
         observe=['Sagrada (24/10) × Bruges (25/10): retenção média, mesmo formato.', 'Primeira hora em Amsterdam (20/10): seguidores por 1.000 visualizações contra o POV.']),
 4: dict(tag='Leitura 1 (01/11)', obj='Completar 14 Reels da v3 e fazer a Leitura 1 no domingo',
         metas=['4 Reels + 1 carrossel', 'Leitura 1 registrada em Aprendizados', 'Decidir horários pelo Insights'],
         observe=['Leitura 1: médias por pilar (seguidores por 1.000, envios, salvamentos).', 'Comentários da Casa Batlló (29/10): o Reel de pergunta gerou conversa?', 'Revisar fixados com os dados.']),
 5: dict(tag='Série e conversão', obj='Explicar a série para quem chega (8 cidades, 8 primeiros dias) e testar se isso converte',
         metas=['4 Reels + 1 carrossel', 'Fixar o “8 primeiros dias” se converter mais que a apresentação'],
         observe=['Seguidores por 1.000 visualizações do Reel de 03/11.', 'Roma de graça (04/11): salvamentos com capa de foto (T4, A).']),
 6: dict(tag='Comparações', obj='Primeira comparação entre cidades (Barcelona ou Madrid) e o bate-volta de Bruges',
         metas=['4 Reels + 1 carrossel', 'Custos de Amsterdam recebidos até 12/11'],
         observe=['T5: Barcelona ou Madrid (12/11) × Reels de cidade única.', 'T4: bate-volta (capa de papel) × Roma de graça (capa de foto).']),
 7: dict(tag='Disney e Itália', obj='Disney (carrossel de consulta), Veneza (desejo) e Boqueria (veredito)',
         metas=['4 Reels + 1 carrossel', 'Inventário dos vídeos da Itália concluído'],
         observe=['Primeiro uso de vídeo ambiental da Itália (21/11).', 'Salvamentos da Boqueria (22/11).']),
 8: dict(tag='Black Friday', obj='Custos reais na semana em que muita gente compra passagem',
         metas=['4 Reels + 1 carrossel', 'Custos de Florença recebidos até 18/11'],
         observe=['Envios do Reel “A passagem é só o começo” (24/11).', 'Primeiro dia em Paris (26/11): CTA de seguir com próximo episódio.']),
 9: dict(tag='Leitura 2 (06/12)', obj='Fechar novembro e fazer a Leitura 2',
         metas=['4 Reels + 1 carrossel', 'Leitura 2 registrada', 'Ajustar a proporção de pilares das semanas 10 a 18 se os dados pedirem'],
         observe=['T1, T2 e T4: conclusões preliminares.', 'Quais Reels trouxeram mais seguidores por 1.000 visualizações?']),
 10: dict(tag='Natal na Europa', obj='Começar a sazonalidade de fim de ano com Roma no Natal',
          metas=['4 Reels + 1 carrossel', 'Custos de Veneza recebidos até 02/12'],
          observe=['Roma iluminada (08/12): envios e seguidores (T1, B).', 'McDonald’s (12/12): comentários.']),
 11: dict(tag='Natal em Roma', obj='Roteiro do dia 25 em Roma e ranking dos primeiros dias',
          metas=['4 Reels + 1 carrossel', 'Ranking do Diego definido até 10/12'],
          observe=['Salvamentos do carrossel de Natal (16/12).', 'Comentários do ranking (15/12).']),
 12: dict(tag='Semana do Natal', obj='Hospedagem em Roma, custo da Disney e o primeiro dia em Roma no Natal (24/12)',
          metas=['4 Reels + 1 carrossel', 'Agendar 24/12 e 26/12 com antecedência'],
          observe=['Envios do Reel de 24/12 (data simbólica).', 'Não comparar a semana de festas com as outras sem levar o feriado em conta.']),
 13: dict(tag='Réveillon', obj='Fim de ano com o frio da Europa, Milão e o Réveillon na Itália',
          metas=['4 Reels + 1 carrossel', 'Custos de todas as cidades recebidos até 30/12'],
          observe=['Comentários do Reel do frio (29/12).', 'Semana atípica: registrar, mas não decidir por ela.']),
 14: dict(tag='Leitura 3 (10/01) e anúncio', obj='Planejamento de 2027: custo por cidade, erros que não repetimos e o anúncio da viagem',
          metas=['4 Reels + 1 carrossel', 'Leitura 3 registrada', 'Bio com o próximo destino'],
          observe=['T3 e T5: conclusão.', 'Seguidores do anúncio da viagem (10/01).']),
 15: dict(tag='Pré-viagem', obj='Itália completa, Lisboa e Gràcia; deixar pronto tudo o que sai durante a viagem',
          metas=['4 Reels + 1 carrossel', 'Peças de 19/01 a 04/02 do acervo editadas até 15/01'],
          observe=['Salvamentos do carrossel “Itália em 9 dias” (13/01).']),
 16: dict(tag='Viagem: partida', obj='Começar a viagem com o acervo agendado e o primeiro dia ao vivo em 23/01',
          metas=['3 Reels do acervo agendados', 'Primeiro dia ao vivo com Placar real', 'Registro de campo diário'], trip=True,
          observe=['Primeiro Reel com Placar real (23/01): seguidores por 1.000 visualizações contra os primeiros dias do acervo.']),
 17: dict(tag='Viagem', obj='Alternar ao vivo (primeira hora, primeiro dia) e acervo agendado',
          metas=['2 Reels ao vivo + 2 do acervo + 1 carrossel', 'Editar ao vivo em até 2 dias'], trip=True,
          observe=['Envios da primeira hora ao vivo (26/01).']),
 18: dict(tag='Viagem e Leitura 4', obj='Fechar a viagem, o ciclo e fazer a Leitura 4',
          metas=['3 Reels ao vivo + 1 do acervo + 1 carrossel', 'Leitura 4 em 07/02'], trip=True,
          observe=['Leitura 4: o que vira regra do próximo ciclo.']),
}

PERGUNTAS = {
 2: dict(tipo='Enquete', q='Qual cidade você quer ver primeiro aqui?', opts=['Paris', 'Lisboa'], steps=['Segunda, 19h: enquete nos Stories sobre uma foto de cada cidade.', 'Anotar o resultado: entra como critério de ordem nas semanas 5 a 8 (sem trocar peças já editadas).']),
 4: dict(tipo='Caixa de perguntas', q='O que você quer saber antes da sua primeira viagem à Europa?', steps=['Segunda, 19h: caixa de perguntas.', 'Responder 3 por Story ao longo da semana.', 'Perguntas repetidas viram pauta (registrar em Aprendizados).']),
 6: dict(tipo='Enquete', q='Barcelona ou Madrid?', opts=['Barcelona', 'Madrid'], steps=['Segunda, 19h: enquete (aquece o Reel de 12/11).', 'Mostrar o resultado no Story pós-Reel de 12/11.']),
 8: dict(tipo='Caixa de perguntas', q='Vai comprar passagem na Black Friday? Para onde?', steps=['Segunda, 19h: caixa de perguntas.', 'Responder com o custo real da cidade, quando houver registro.']),
 10: dict(tipo='Enquete', q='Natal na Europa ou no Brasil?', opts=['Europa', 'Brasil'], steps=['Segunda, 19h: enquete com foto da vila de Natal de Roma.']),
 12: dict(tipo='Caixa de perguntas', q='Qual cidade você quer ver o custo completo?', steps=['Segunda, 19h: caixa de perguntas.', 'A mais pedida abre o carrossel de 06/01.']),
 14: dict(tipo='Caixa de perguntas', q='O que você quer ver na viagem de janeiro?', steps=['Segunda, 19h: caixa de perguntas.', 'As 3 mais pedidas entram como roteiro da viagem, se couberem.']),
 16: dict(tipo='Enquete', q='Primeiro dia ao vivo: o que você quer saber primeiro?', opts=['Quanto custou', 'O que deu errado'], steps=['Durante a viagem, no Story da noite do dia 1.']),
}

# ───────────── peças ─────────────
PECAS = v3_pecas_1.PECAS + v3_pecas_2.PECAS + v3_pecas_3.PECAS + v3_pecas_4.PECAS
PECAS.sort(key=lambda x: (x['d'], x['h']))

def mx(pc):
    e = 2 if ('envio' in pc['cta'] or pc['pl'] == 'UTIL') else 1
    g = 1 if pc['gt'].startswith('Visual') else (2 if pc['gt'] in ('Preço', 'Surpresa', 'Não faça isso', 'Comparação', 'Pergunta', 'Vale a pena?') else 1)
    n = 2
    o = 2
    es = {'ok': 2 if pc['nv'] != 'A' else 1, 'dec': 1, 'dad': 1, 'fut': 0}[pc['st']]
    t = e + g + n + o + es
    dec = 'Produzir e publicar como Reel normal' if t >= 8 else ('Produzir e testar' if t >= 5 else 'Reformular')
    if pc['f'] == 'C':
        dec = dec.replace('Reel normal', 'carrossel')
    return dict(e=e, g=g, n=n, o=o, es=es, t=t, dec=dec + ' (pontuação de planejamento: julgamento, não dado)')

CHK_A = ['Conferir as pendências desta peça (lado direito)', 'Selecionar os trechos e anotar a minutagem', 'Abrir o projeto-modelo da série no CapCut', 'Editar no tempo das cenas (até 30 s)', 'Legendas nos 6 estilos (Padrão por padrão), com scrim', 'Objetos de marca nas posições fixas (ver Cenas)', 'Grão 5% e preset PD Chegada v1', 'Criar capa (texto dentro da área 3:4)',
         "100% original, sem marca d'água", 'O gancho prende nos 3 primeiros segundos', 'Hook escrito com até 7 palavras', 'Funciona sem som', 'Tem uma única ideia', 'Sei para quem alguém enviaria', 'Legenda com palavras-chave e 1 CTA', 'Placa em x 72 · y 640 com Chegada', 'No máximo 1 carimbo, 1 ticket e 2 bilhetes, em cenas diferentes', 'Até 3 famílias e 5 transições; 70% de cortes secos', 'Até 3 efeitos ao mesmo tempo (grão conta)', 'Nada nas zonas da interface (topo 256, base 480, direita 136)', 'Teste de miniatura a 25%', 'Placar só com registro real de hora e gasto', 'Valores em € e R$, com a cotação datada na legenda', 'Só fatos e valores registrados (sem inventar)',
         'Publicar', 'Responder todos os comentários na primeira hora', 'Registrar as métricas em 48 horas (inclui visualizações e seguidores)']
GRP_A = [['Produção', 0, 8], ['Pré-publicação (obrigatório)', 8, 24], ['Publicação', 24, 27]]
CHK_B = ['Conferir as pendências desta peça (lado direito)', 'Selecionar os trechos e anotar a minutagem', 'Editar no tempo das cenas (até 30 s)', 'Legenda Padrão, com scrim (Nível B)', '1 objeto de marca na posição fixa, no pico (Nível B)', 'Grão 5% e preset PD Chegada v1', 'Criar capa (texto dentro da área 3:4)',
         "100% original, sem marca d'água", 'O gancho prende nos 3 primeiros segundos', 'Hook escrito com até 7 palavras (ou sem texto, se for a variante visual do T2)', 'Funciona sem som', 'Tem uma única ideia', 'Sei para quem alguém enviaria', 'Legenda com palavras-chave e 1 CTA', 'Até 3 famílias e 5 transições; 70% de cortes secos', 'Nada nas zonas da interface (topo 256, base 480, direita 136)', 'Teste de miniatura a 25%', 'Valores em € e R$, com a cotação datada na legenda', 'Só fatos e valores registrados (sem inventar)',
         'Publicar', 'Responder todos os comentários na primeira hora', 'Registrar as métricas em 48 horas (inclui visualizações e seguidores)']
GRP_B = [['Produção', 0, 7], ['Pré-publicação (obrigatório)', 7, 19], ['Publicação', 19, 22]]
CHK_C = ['Conferir as pendências desta peça (lado direito)', 'Escolher a foto de cada slide (mesma edição de cor)', 'Template 3:4 (1080×1440, margem 80), contador e etiqueta de série', 'Rota amarela em y 1360 atravessando os slides', 'Slide 2 funciona sozinho (segunda chance)', 'Escrever a legenda (gancho, palavras-chave e 1 CTA)',
         'Conteúdo original', 'Tem uma única ideia', 'Até 40 palavras por slide', 'Placa CTA no último slide com o mesmo verbo da legenda', 'Valores em € e R$, com a cotação datada', 'Só fatos e valores registrados (sem inventar)', 'Teste de miniatura a 25%',
         'Publicar com música instrumental da biblioteca', 'Responder todos os comentários na primeira hora', 'Registrar as métricas em 48 horas']
GRP_C = [['Produção', 0, 6], ['Pré-publicação (obrigatório)', 6, 13], ['Publicação', 13, 16]]
CHK_S = ["Exportar o Reel do projeto original, sem marca d'água", 'Título de até 60 caracteres', "Original, sem marca d'água", 'Cena mais forte no primeiro segundo', 'Funciona sem som', 'Publicar', 'Registrar as métricas em 48 horas']
GRP_S = [['Produção', 0, 2], ['Pré-publicação', 2, 5], ['Publicação', 5, 7]]

def to_post(pc, pid, n_fmt):
    reel = pc['f'] == 'R'
    fmt = 'Reel' if reel else 'Carrossel'
    nivel = ('Nível ' + pc['nv']) if reel else 'Carrossel 3:4'
    teste = None
    if pc.get('te'):
        tid, var = pc['te'].split(':')
        teste = dict(id=tid, var=var)
    obs = []
    obs.append('Pilar: ' + PIL[pc['pl']] + '. ' + PIL_DESC[pc['pl']])
    if reel:
        obs.append('Nível A: estrutura completa do DS V2 (5.2) e checklist 7.3 completo.' if pc['nv'] == 'A' else 'Nível B (leve): cortes secos, legenda Padrão com scrim e 1 objeto de marca no pico (DS V2, 5.2). Nenhum valor visual novo.')
        obs.append('Placa `PRIMEIRO DIA EM / CIDADE` só em cenas do primeiro dia real da cidade; nas outras peças, Placa Marca `PRIMEIRO DIA →` ou Série (regra editorial v3).')
    else:
        obs.append('Carrossel 3:4 (DS V2, 5.3): slide 2 funciona sozinho (o Instagram pode reapresentar o carrossel a partir dele). Publicar com música da biblioteca (elegível para a aba Reels).')
    obs.append('Métrica principal: ' + pc['me'] + '.')
    if teste:
        obs.append('Teste ' + teste['id'] + ', variante ' + teste['var'] + ': mantenha iguais as outras variáveis (duração, horário, tipo de cena).')
    return {
        'd': pc['d'], 'hora': pc['h'], 'plat': 'Instagram', 'fmt': fmt, 'pilar': PIL[pc['pl']], 'pl': pc['pl'],
        'video': DEST[pc['k']], 'titulo': pc['t'], 'gancho': pc['g'],
        'como': nivel + '. ' + ST[pc['st']] + '.',
        'leg': pc['lg'], 'cta': pc['cta'], 'met': pc['me'], 'kind': 'v3_reel' if reel else 'v3_car', 'vk': pc['k'],
        'code': '%s %02d · %s · %s' % (fmt, n_fmt, PIL[pc['pl']], nivel), 'id': pid, 'obj': pc['ob'],
        'sc': [{'t': a, 'l': b, 'x': c} for a, b, c in pc.get('sc', [])],
        'sl': [({'n': s.split(' · ', 1)[0], 'x': s.split(' · ', 1)[1]} if ' · ' in s else {'n': '', 'x': s}) for s in pc.get('sl', [])],
        'mat': pc['ma'], 'chk': (CHK_A if pc['nv'] == 'A' else CHK_B) if reel else CHK_C,
        'grp': (GRP_A if pc['nv'] == 'A' else GRP_B) if reel else GRP_C,
        'obs': obs, 'orig': {'fonte': pc['of'], 'trecho': pc['otr'], 'dica': ''}, 'gt': pc['gt'],
        'ativo': 'Ver as cenas: cada objeto de marca está indicado no momento em que entra (DS V2, 2 e 5).',
        'mx': mx(pc), 'v3': True, 'motiv': pc['mo'], 'q0': pc['q0'], 'tela': pc['tl'], 'nar': pc['na'],
        'capa': pc['cp'], 'som': pc['so'], 'hip': pc['hi'], 'teste': teste, 'pend': pc['pe'],
        'nivel': pc['nv'] if reel else '—', 'prod': pc['st'],
    }

# ───────────── montar posts ─────────────
hist = []
for p in D['posts']:
    if p['d'] <= CORTE:
        p['done'] = True
        hist.append(p)
for b in BASELINE:
    OLD[b['id']]['aud'] = {k: b[k] for k in ('nome', 'vis', 'nseg', 'sav', 'env', 'seg', 'obs')}

KEEP_KINDS = {'long', 'stories_launch', 'stories_count', 'stories_partida', 'stories_embarque'}
kept = [p for p in D['posts'] if p['d'] >= INICIO and p['kind'] in KEEP_KINDS]
removed = [p for p in D['posts'] if p['d'] >= INICIO and p['kind'] not in KEEP_KINDS]
for p in kept:
    p['pilar'] = 'YouTube (complementar)' if p['plat'] == 'YouTube' else 'Stories'

new = []
nr = nc = 0
seq = 200
for pc in PECAS:
    if pc['f'] == 'R':
        nr += 1; n = nr
    else:
        nc += 1; n = nc
    new.append(to_post(pc, 'p%d' % seq, n))
    seq += 1

# Shorts: reaproveitam os Reels de terça e sábado (exceto ao vivo), no dia seguinte, 12:00
shorts = []
ns = 0
sseq = 400
for p in new:
    if p['fmt'] != 'Reel' or p['vk'] == 'jan':
        continue
    wd = dt.date.fromisoformat(p['d']).weekday()
    if wd not in (1, 5):
        continue
    ns += 1
    dd = (dt.date.fromisoformat(p['d']) + dt.timedelta(days=1)).isoformat()
    if dd > D['end']:
        continue
    dm = p['d'][8:10] + '/' + p['d'][5:7]
    shorts.append({
        'd': dd, 'hora': '12:00', 'plat': 'YouTube', 'fmt': 'Short', 'pilar': 'YouTube (complementar)', 'video': p['video'],
        'titulo': 'Short: ' + p['titulo'], 'gancho': '—',
        'como': "Mesmo corte do Reel de %s (%s), exportado do projeto original, sem marca d'água. Título de até 60 caracteres com a palavra-chave da cidade. Sem citar o vídeo longo se ele ainda não saiu." % (dm, p['titulo']),
        'leg': p['gancho'] if not p['gancho'].startswith('(') else p['titulo'], 'cta': '—', 'met': 'Visualizações e inscritos', 'kind': 'short_reuse', 'vk': p['vk'],
        'code': 'Short %02d' % ns, 'id': 'p%d' % sseq, 'obj': 'Reaproveitar no YouTube Shorts um Reel do Instagram, sem trabalho novo de edição.',
        'sc': [], 'sl': [], 'mat': ['Projeto do Reel de origem'], 'chk': CHK_S, 'grp': GRP_S,
        'obs': ['YouTube é canal complementar: o Short segue o Reel, não o contrário.'], 'orig': {'fonte': 'Reel do Instagram', 'trecho': None, 'dica': ''},
    })
    sseq += 1

setup = {
    'd': '2027-01-18', 'hora': '—', 'plat': 'Ambos', 'fmt': 'Setup', 'pilar': 'Base', 'video': 'Viagem de janeiro',
    'titulo': 'Agendar as peças do acervo de 19/01 a 04/02 antes de embarcar', 'gancho': '—',
    'como': 'Agendar no Instagram (conta profissional) os Reels e carrosséis do acervo de 19/01 a 04/02 (19/01, 20/01, 21/01, 24/01, 27/01, 28/01, 31/01, 04/02) com capas e legendas prontas. No YouTube Studio, os Shorts do mesmo período. Conferir a cotação e os preços citados.',
    'leg': '—', 'cta': '—', 'met': 'Tudo agendado', 'kind': 'setup', 'vk': 'jan', 'code': 'Setup da viagem', 'id': 'p399',
    'obj': 'Garantir a frequência durante a viagem sem depender de editar no celular.', 'sc': [], 'sl': [],
    'mat': ['Peças do acervo editadas até 15/01'], 'chk': ['Revisar as 8 peças do acervo', 'Agendar no Instagram', 'Agendar os Shorts', 'Conferir cotações e preços', 'Publicar (agendamento confirmado)'],
    'obs': ['A viagem tem 4 Reels e 1 carrossel por semana: metade ao vivo, metade do acervo.'], 'orig': {'fonte': 'Acervo', 'trecho': None, 'dica': ''}, 'grp': [['Tarefas', 0, 5]],
}

posts = hist + kept + new + shorts + [setup]
posts.sort(key=lambda p: (p['d'], '00:00' if p['hora'] == '—' else p['hora']))
PID = {p['id']: p for p in posts}

# ───────────── semanas ─────────────
def stories_for(date, ps, trip):
    reels = [p for p in ps if p['fmt'] == 'Reel' and p['plat'] == 'Instagram']
    cars = [p for p in ps if p['fmt'] == 'Carrossel']
    wd = dt.date.fromisoformat(date).weekday()
    steps = []
    if trip and date >= '2027-01-20':
        steps.append('Parte 01 · MANHÃ · STORYTELLING: abertura `AO VIVO DA VIAGEM` + Placar mini com a hora local.')
        steps.append('Parte 02 · DURANTE O DIA · RELACIONAMENTO: 2 ou 3 Stories do que está acontecendo (sem produção).')
        steps.append('Parte 03 · NOITE · ENGAJAMENTO: custo real do dia (só valores anotados) e enquete nativa “vale ou pula?”.')
        if reels or cars:
            steps.append('Parte 04 · PÓS-POST · CONVERSÃO: compartilhe o post do dia com 1 frase que não está nele.')
        t = 'Diário ao vivo da viagem'
    elif reels or cars:
        p = (reels or cars)[0]
        h = p['hora']
        cta = {'DESEJO': 'enquete “Iria?” (Iria amanhã / Já fui)', 'UTIL': 'caixa de perguntas “Qual a sua dúvida sobre ' + p['video'] + '?”', 'EXP': 'slider de emoji sobre o momento do Reel', 'SERIE': 'enquete “Qual cidade você quer ver o primeiro dia?” (2 opções do acervo)'}.get(p.get('pl'), 'pergunta aberta')
        if p['fmt'] == 'Carrossel':
            cta = 'compartilhe o slide 2 e pergunte “Qual slide você mandaria para alguém que vai?”'
        steps.append('Parte 01 · PÓS-POST · %s · CONVERSÃO: compartilhe o post com 1 frase que não está nele + %s.' % (h, cta))
        steps.append('Parte 02 · NOITE · RELACIONAMENTO: 1 bastidor da edição ou da escolha do material (sem anunciar o que vem).')
        t = 'Pós-post + bastidor'
    else:
        if wd == 0:
            steps.append('Parte 01 · NOITE · ENGAJAMENTO: pergunta da semana (ver card) ou enquete sobre a próxima cidade do feed.')
            t = 'Pergunta da semana'
        else:
            steps.append('Parte 01 · DURANTE O DIA · RELACIONAMENTO: 1 a 3 Stories de bastidor (edição, fotos que não entraram, escolha da capa).')
            t = 'Bastidores'
    steps.append('Métrica do dia: taxa de resposta (respostas ÷ alcance) e saídas do 1º Story.')
    return {'t': t, 'steps': steps}

def inter_for(date, ps, trip):
    wd = dt.date.fromisoformat(date).weekday()
    out = []
    if any(p['plat'] in ('Instagram', 'Ambos') and p['fmt'] in ('Reel', 'Carrossel') for p in ps):
        out.append('Instagram: responder todos os comentários em até 60 minutos depois de postar.')
    if any(p['plat'] == 'YouTube' and p['fmt'] == 'Vídeo longo' for p in ps):
        out.append('YouTube: responder os comentários nas primeiras 2 horas.')
    if wd in (0, 2, 4) and not trip:
        out.append('10 min: deixar 5 comentários de verdade em perfis de viagem (de preferência de quem fala com o mesmo público).')
    if wd == 0:
        out.append('10 min de Insights: registrar as métricas de 48 h dos posts da semana anterior em Aprendizados (inclui visualizações e seguidores).')
    for L in LEITURAS:
        if L['d'] == date:
            out.append(L['t'] + ': ' + L['o'])
    if trip:
        out.append('Responder comentários e mensagens uma vez por dia, à noite.')
    return out

byday = {}
for p in posts:
    byday.setdefault(p['d'], []).append(p['id'])

for w in D['weeks']:
    if w['end'] < INICIO:
        continue
    meta = WEEKS[w['n']]
    w['tag'] = meta['tag']; w['obj'] = meta['obj']; w['metas'] = meta['metas']; w['observe'] = meta['observe']
    w['trip'] = bool(meta.get('trip'))
    q = PERGUNTAS.get(w['n'])
    if q:
        q = dict(q); q['quando'] = w['start']
    w['pergunta'] = q if w['n'] >= 2 else w.get('pergunta')
    days = []
    d0 = dt.date.fromisoformat(w['start'])
    for i in range(7):
        date = (d0 + dt.timedelta(days=i)).isoformat()
        if date > w['end']:
            break
        if date < INICIO:
            old = [x for x in w['days'] if x['date'] == date]
            if old:
                days.append(old[0])
            continue
        ids = byday.get(date, [])
        ps = [PID[i] for i in ids]
        trip = date >= D['trip']['ini']
        days.append({'date': date, 'posts': ids, 'stories': stories_for(date, ps, trip), 'inter': inter_for(date, ps, trip)})
    w['days'] = days

# conferir: todo post está em algum dia
indays = {i for w in D['weeks'] for d in w['days'] for i in d['posts']}
faltam = [p['id'] for p in posts if p['id'] not in indays]
assert not faltam, faltam

D['posts'] = posts
D['versao'] = 'v3 · 09/10/2026'
D['marco'] = CORTE
D['pilares'] = [{'k': k, 'nome': PIL[k], 'desc': PIL_DESC[k]} for k in PIL]
D['testes'] = TESTES
D['base'] = BASELINE
D['leituras'] = LEITURAS
D['pend'] = PEND
D['dest'] = DEST
D['stmat'] = ST

out = html[:m.start(1)] + json.dumps(D, ensure_ascii=False) + html[m.end(1):]
open(PAINEL, 'w', encoding='utf-8').write(out)

# relatório
from collections import Counter
v3 = [p for p in posts if p.get('v3')]
print('histórico mantido:', len(hist), '| mantidos do futuro:', len(kept), '| removidos:', len(removed), '| novas peças:', len(v3), '| shorts:', len(shorts))
print('removidos por formato:', dict(Counter(p['fmt'] for p in removed)))
print('v3 por formato:', dict(Counter(p['fmt'] for p in v3)))
print('v3 por pilar:', dict(Counter(p['pilar'] for p in v3)))
print('v3 por destino:', dict(Counter(p['video'] for p in v3)))
print('v3 por status de material:', dict(Counter(ST[p['prod']] for p in v3)))
print('v3 por teste:', dict(Counter((p['teste'] or {}).get('id', '—') + ':' + (p['teste'] or {}).get('var', '') for p in v3)))
print('reels por gancho:', dict(Counter(p['gt'] for p in v3 if p['fmt'] == 'Reel')))
