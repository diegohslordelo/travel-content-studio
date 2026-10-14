# -*- coding: utf-8 -*-
"""Aplica a proposta v4 (PROPOSTA_V4_SERIE_PRIMEIRO_DIA.md) sobre o painel v3.

Uso (de dentro de planejamento/):  python3 scripts/aplicar_v4.py
- Lê o painel v3 em versoes/painel-v3-2026-10-14-antes-da-v4.html (cópia criada na primeira execução).
- Série "Primeiro dia em X" todo domingo às 19:00; Florença, Veneza e Milão no modelo de Roma.
- Remove 6 peças que repetiam a função da série e move as demais pelo menor deslocamento.
- Regra de diversidade (Diego, 14/10): nenhuma cidade em 2 posts seguidos e no máximo 2 por semana
  (seg a dom). Peças de várias cidades e a viagem de janeiro ao vivo ficam fora da regra. O script confere.
- Regenera os Shorts a partir de 15/10 e os Stories e as interações de cada dia a partir de 14/10.
"""
import datetime as dt
import json
import os
import re
import shutil
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
PAINEL = os.path.join(AQUI, '..', 'planejamento-postagens.html')
BASE = os.path.join(AQUI, '..', 'versoes', 'painel-v3-2026-10-14-antes-da-v4.html')
HOJE = '2026-10-14'

if not os.path.exists(BASE):
    shutil.copyfile(PAINEL, BASE)
html = open(BASE, encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\n', html, re.S)
D = json.loads(m.group(1))
P = {p['id']: p for p in D['posts']}

# ───────────── 1. peças que saem ─────────────
SAEM = {
    'p226': 'absorvida pelo Primeiro dia em Barcelona (18/10), como pico',
    'p236': 'absorvida pelo Primeiro dia em Bruxelas (20/12)',
    'p240': 'absorvida pelo Primeiro dia na Disneyland Paris (22/11), como veredito',
    'p256': 'Madrid tinha 6 peças; se o momento foi no dia 1, entra no Primeiro dia em Madrid (06/12)',
    'p216': 'usava as mesmas cenas da Primeira noite em Lisboa (17/01)',
    'p261': 'sem vaga e dependente de dados; volta ao banco de pautas',
}

# ───────────── 2. datas novas (otimização da proposta v4) ─────────────
NOVAS_DATAS = {
    'p218': '2026-10-14', 'p214': '2026-10-24', 'p207': '2026-10-25', 'p210': '2026-10-27', 'p212': '2026-10-29',
    'p217': '2026-11-01', 'p208': '2026-11-04', 'p220': '2026-11-05', 'p219': '2026-11-07', 'p234': '2026-11-08',
    'p213': '2026-11-11', 'p223': '2026-10-28', 'p233': '2026-11-18', 'p215': '2026-11-22', 'p228': '2026-11-25', 'p231': '2026-11-26',
    'p243': '2026-12-02', 'p251': '2026-12-05', 'p221': '2026-12-06', 'p273': '2026-12-09', 'p241': '2026-12-15',
    'p247': '2026-12-27', 'p270': '2027-01-17', 'p271': '2027-01-16', 'p238': '2027-01-20', 'p276': '2027-01-21',
    'p274': '2027-01-24', 'p206': '2026-10-20', 'p203': '2026-10-21', 'p211': '2026-11-03', 'p246': '2026-10-31',
}
HORA = {1: '18:30', 2: '18:00', 3: '12:30', 5: '11:00', 6: '19:00'}

# ───────────── 3. textos comuns da série ─────────────
PLACAR = ('Placar `+HH:MM · € 0,00` liga em 2,0 s e gira a cada gasto registrado (DS V2, 2.5). '
          'Hora pelo horário do arquivo ou EXIF; gasto pelo registro do Diego. Sem registro, sem Placar.')
FECHO = 'Placa `E ISSO FOI SÓ O / PRIMEIRO DIA.` + 1º nascendo + bordão.'
PEND_PLACAR = ['Diego: hora de chegada no dia 1 (o `+00:00` do Placar)',
               'Diego: gastos do dia 1 na ordem (o quê, valor, moeda, por pessoa ou do casal)',
               'Data do dia 1 (cotação PTAX do dia e legenda)']
REF_A = P['p217']  # Reel Nível A: checklist e grupos
OBS_SERIE = [
    'Pilar: Primeiro Dia (série). Identidade: o primeiro dia de cada cidade e o que o perfil promete. Conversão em seguidores.',
    'Série v4: um primeiro dia todo domingo às 19:00 (PROPOSTA_V4_SERIE_PRIMEIRO_DIA.md). O Reel se sustenta sozinho; o link do vlog vai nos Stories.',
    'Nível A: estrutura completa do DS V2 (5.2) e checklist 7.3 completo, com Placar (registro do Diego).',
    'Placa `PRIMEIRO DIA EM / CIDADE` só em cenas do primeiro dia real da cidade.',
    'Métrica principal: Seguidores por 1.000 visualizações.',
]
ST = D['stmat']


def serie(pid, d, k, video, titulo, gancho, gt, var, prod, obj, motiv, q0, sc, tela, nar, leg, cta, capa, som, mat,
          pend, fonte, trecho, code):
    obs = list(OBS_SERIE) + ['Teste T3, variante %s: mantenha iguais as outras variáveis (duração, horário, tipo de cena).' % var]
    return {
        'd': d, 'hora': '19:00', 'plat': 'Instagram', 'fmt': 'Reel', 'pilar': 'Primeiro Dia (série)', 'pl': 'SERIE',
        'video': video, 'titulo': titulo, 'gancho': gancho, 'como': 'Nível A. ' + ST[prod] + '.', 'leg': leg, 'cta': cta,
        'met': 'Seguidores por 1.000 visualizações', 'kind': 'v3_reel', 'vk': k, 'code': code, 'id': pid, 'obj': obj,
        'sc': [{'t': a, 'l': b, 'x': c} for a, b, c in sc], 'sl': [], 'mat': mat, 'chk': REF_A['chk'], 'grp': REF_A['grp'],
        'obs': obs, 'orig': {'fonte': fonte, 'trecho': trecho, 'dica': ''}, 'gt': gt,
        'ativo': 'Ver as cenas: cada objeto de marca está indicado no momento em que entra (DS V2, 2 e 5).',
        'mx': dict(e=1, g=2, n=2, o=2, es=1, t=8, dec='Produzir e publicar como Reel normal (pontuação de planejamento: julgamento, não dado)'),
        'v3': True, 'v4': True, 'motiv': motiv, 'q0': q0, 'tela': tela, 'nar': nar, 'capa': capa, 'som': som,
        'hip': 'Um primeiro dia por semana, com Placar real, converte mais visitantes em seguidores que os outros pilares (série v4; T3 compara seguir × envio).',
        'teste': {'id': 'T3', 'var': var}, 'pend': pend, 'nivel': 'A', 'prod': prod,
    }


BCN_MASTER = REF_A['mat'][0].split(': 00:00')[0]
OUTRAS = REF_A['mat'][-1]
ITA_FOTOS = 'Fotos de {c} (a enviar pelo Diego; o painel ainda não tem o inventário). Hora de cada foto pelo EXIF'
CTA_SEGUIR = 'Segue pra ver o próximo primeiro dia (seguir).'

NOVAS = [
    serie('p300', '2026-10-18', 'bcn', 'Barcelona', 'Primeiro dia em Barcelona', '18 km a pé e € [total].', 'Resultado primeiro', 'A', 'dad',
          'Série e conversão: o dia 1 de Barcelona inteiro em 25 s, com o Placar mostrando hora e gasto reais. Estreia a série dos domingos.',
          'Quem vai a Barcelona e quem sonha com a primeira Europa. Segue porque entende a série; envia para quem vai junto.',
          'Primeira cena do dia 1 no master (Gràcia, 00:00–00:20), num plano sem etiqueta gráfica e diferente do usado na apresentação, com a Placa `PRIMEIRO DIA EM / BARCELONA` (Chegada) e o gancho escrito.',
          [('0–2,5 s', 'Gancho', 'Gràcia (master, dia 1) + Placa de abertura. Legenda Padrão com o gancho e Destaque em “18 km”.'),
           ('2–25 s', 'Placar', PLACAR),
           ('2,5–7 s', 'Camp Nou', 'IMG_0502 (chegada, fila). Etiqueta de valor do museu (€ 31, confirmar se por pessoa) e o Placar gira.'),
           ('7–10 s', 'Montjuïc', 'IMG_0586 (vista). Trocar o áudio do músico de rua pela música da biblioteca.'),
           ('10–13 s', 'Barceloneta', 'IMG_0690 (praia, frio, jet ski). Legenda Informação.'),
           ('13–16 s', 'Arco do Triunfo', 'IMG_0781, fim da tarde.'),
           ('16–23 s', 'Pico', 'Master 10:12–10:57: “a gente andou demais, uns 18 quilômetros” e a primeira tapa (patatas bravas e cerveza). Bilhete: “valeu cada km.” Absorve o Reel “Primeira tapa depois de 18 km”.'),
           ('23–26 s', 'Fechamento', FECHO + ' Legenda: “segue pra ver o próximo.”')],
          '18 km a pé e € [total] · camp nou · montjuïc · barceloneta · arco do triunfo · valeu cada km · e isso foi só o primeiro dia.',
          'Sem narração nova (falas do master).',
          '18 km a pé e € [total] no primeiro dia em Barcelona. 👟\n\nGràcia, Camp Nou, Montjuïc, Barceloneta, Ciutadella e Arco do Triunfo, quase tudo a pé. No fim, a primeira tapa: patatas bravas e cerveza.\n\nO roteiro completo, parada por parada, sai no carrossel de quarta.\n\nCotação: € 1 = R$ [PTAX da data do dia 1].\n\nSou o Diego e aqui eu mostro o primeiro dia em cada cidade. Segue pra ver o próximo.',
          CTA_SEGUIR, 'Barceloneta ou Arco do Triunfo com a Placa. Texto da capa: “18 KM A PÉ”.',
          'Falas do master + música da biblioteca nas cenas sem fala (DS 4.6).',
          [BCN_MASTER + ': dia 1 (00:00–10:57)', 'IMG_0502, IMG_0586, IMG_0690, IMG_0781, IMG_0816', 'Transcrição com tempo por palavra: reels/apresentacao/analise/transcricao_palavras.tsv'],
          PEND_PLACAR + ['Não repetir os planos da camisa do Bahia (Reel de 11/10)', 'Se o carrossel do roteiro já tiver saído antes, trocar o gancho por “Gastamos € [total] no primeiro dia.”'],
          'Barcelona, dia 1', 'Master 00:00–10:57', 'Reel · Primeiro Dia (série) · Nível A · Barcelona'),
    serie('p301', '2026-11-15', 'ita', 'Itália', 'Primeiro dia em Florença', 'Florença, dia 1: [fato real].', 'Afirmação', 'B', 'dad',
          'Série: o primeiro dia em Florença no modelo de Roma (fotos na ordem do dia com a hora do EXIF), agora com Placar.',
          'Quem vai à Itália e monta roteiro por várias cidades. Envia para quem vai junto.',
          'Primeira foto do dia 1 em Florença com a Placa `PRIMEIRO DIA EM / FLORENÇA` (Chegada) e o gancho.',
          [('0–2 s', 'Gancho', 'Primeira foto + Placa de abertura. Legenda Padrão com o gancho.'),
           ('2–19 s', 'Placar', PLACAR),
           ('2–12 s', 'O dia', 'Fotos na ordem do dia 1, de 1,5 a 2 s cada, com zoom de 100% a 104% (DS V2, 4.5). Legenda Informação com a hora de cada foto.'),
           ('12–16 s', 'Pico', 'A foto mais forte do dia + 1 objeto de papel conforme o fato (Ticket, Carimbo com data e hora, ou Bilhete).'),
           ('16–19 s', 'Fechamento', FECHO)],
          'florença, dia 1 · [hora] [lugar] · … · e isso foi só o primeiro dia.', 'Opcional: o Diego grava o bordão (3 s).',
          'Primeiro dia em Florença: [fato real]. 🇮🇹\n\n[data do dia 1]: [lugares na ordem, com hora].\n\nGastamos € [total do dia] por pessoa. Cotação: € 1 = R$ [PTAX da data].\n\nManda pra quem vai pra Itália com você.',
          'Manda pra quem vai pra Itália (envio).', 'A foto mais forte do dia com a Placa. Texto da capa: “DIA 1: FLORENÇA”.',
          'Música instrumental da biblioteca.', [ITA_FOTOS.format(c='Florença')],
          PEND_PLACAR + ['Fotos de Florença com EXIF', 'Gancho final: definir com o fato real do dia (até 7 palavras)'],
          'Fotos da Itália', 'Florença, dia 1', 'Reel · Primeiro Dia (série) · Nível A · Florença'),
    serie('p302', '2026-11-29', 'ita', 'Itália', 'Primeiro dia em Veneza', 'Veneza, dia 1: [fato real].', 'Afirmação', 'A', 'dad',
          'Série: o primeiro dia em Veneza no modelo de Roma, com Placar. É a cidade de maior desejo do acervo.',
          'Quem sonha com Veneza e quem monta roteiro pela Itália. Segue pela série; envia para quem iria junto.',
          'Primeira foto do dia 1 em Veneza com a Placa `PRIMEIRO DIA EM / VENEZA` (Chegada) e o gancho.',
          [('0–2 s', 'Gancho', 'Primeira foto + Placa de abertura.'),
           ('2–19 s', 'Placar', PLACAR),
           ('2–12 s', 'O dia', 'Fotos na ordem do dia 1, de 1,5 a 2 s cada, zoom de 100% a 104%, hora do EXIF na legenda Informação.'),
           ('12–16 s', 'Pico', 'A foto mais forte + 1 objeto de papel conforme o fato.'),
           ('16–19 s', 'Fechamento', FECHO + ' Legenda: “segue pra ver o próximo.”')],
          'veneza, dia 1 · [hora] [lugar] · … · e isso foi só o primeiro dia.', 'Opcional: o Diego grava o bordão (3 s).',
          'Primeiro dia em Veneza: [fato real]. 🇮🇹\n\n[data do dia 1]: [lugares na ordem, com hora].\n\nGastamos € [total do dia] por pessoa. Cotação: € 1 = R$ [PTAX da data].\n\nSou o Diego e aqui eu mostro o primeiro dia em cada cidade. Segue pra ver o próximo.',
          CTA_SEGUIR, 'A foto mais forte do dia com a Placa. Texto da capa: “DIA 1: VENEZA”.', 'Música instrumental da biblioteca.',
          [ITA_FOTOS.format(c='Veneza'), 'Vídeos ambientais da Itália, se o inventário confirmar planos do dia 1 em Veneza'],
          PEND_PLACAR + ['Fotos de Veneza com EXIF', 'Não repetir os planos do Reel “Veneza: sem carro, sem moto, só barco” (21/11)'],
          'Fotos da Itália', 'Veneza, dia 1', 'Reel · Primeiro Dia (série) · Nível A · Veneza'),
    serie('p303', '2026-12-13', 'ita', 'Itália', 'Primeiro dia em Milão', 'Milão, dia 1: [fato real].', 'Afirmação', 'B', 'dad',
          'Série: o primeiro dia em Milão no modelo de Roma, com Placar.',
          'Quem vai à Itália e decide se Milão vale mais que uma escala. Envia para quem vai junto.',
          'Primeira foto do dia 1 em Milão com a Placa `PRIMEIRO DIA EM / MILÃO` (Chegada) e o gancho.',
          [('0–2 s', 'Gancho', 'Primeira foto + Placa de abertura.'),
           ('2–19 s', 'Placar', PLACAR),
           ('2–12 s', 'O dia', 'Fotos na ordem do dia 1, de 1,5 a 2 s cada, zoom de 100% a 104%, hora do EXIF na legenda Informação.'),
           ('12–16 s', 'Pico', 'A foto mais forte + 1 objeto de papel conforme o fato.'),
           ('16–19 s', 'Fechamento', FECHO)],
          'milão, dia 1 · [hora] [lugar] · … · e isso foi só o primeiro dia.', 'Opcional: o Diego grava o bordão (3 s).',
          'Primeiro dia em Milão: [fato real]. 🇮🇹\n\n[data do dia 1]: [lugares na ordem, com hora].\n\nGastamos € [total do dia] por pessoa. Cotação: € 1 = R$ [PTAX da data].\n\nManda pra quem vai pra Milão.',
          'Manda pra quem vai pra Milão (envio).', 'A foto mais forte do dia com a Placa. Texto da capa: “DIA 1: MILÃO”.',
          'Música instrumental da biblioteca.', [ITA_FOTOS.format(c='Milão')],
          PEND_PLACAR + ['Fotos de Milão com EXIF'], 'Fotos da Itália', 'Milão, dia 1', 'Reel · Primeiro Dia (série) · Nível A · Milão'),
    serie('p304', '2026-12-20', 'bxl', 'Bruxelas', 'Primeiro dia em Bruxelas', 'Vale parar 1 dia em Bruxelas?', 'Vale a pena?', 'A', 'dad',
          'Série: o único dia em Bruxelas, do Atomium ao centro, com Placar e o veredito. Absorve “Bruxelas em 1 dia: vale parar?”.',
          'Quem monta roteiro Paris–Amsterdam ou pela Bélgica. Segue pela série; salva para decidir o roteiro.',
          'Melhor plano do centro de Bruxelas (decupagem) com a Placa `PRIMEIRO DIA EM / BRUXELAS` (Chegada) e o gancho.',
          [('0–2 s', 'Gancho', 'Plano do centro + Placa de abertura.'),
           ('2–25 s', 'Placar', PLACAR),
           ('2–6 s', 'Contexto', 'IMG_2170 (0,2–5,0 s): “primeira parada, Atomium… viemos de metrô”. Usar outro trecho que não o do Reel de 10/10.'),
           ('6–18 s', 'O dia', 'Paradas reais do dia (decupagem), de 1,5 a 3 s cada, na ordem.'),
           ('18–22 s', 'Veredito', 'Bilhete veredito (`vale.` / `depende:` / `pula.`) com a opinião real do Diego.'),
           ('22–25 s', 'Fechamento', FECHO + ' Legenda: “segue pra ver o próximo.”')],
          'vale parar 1 dia em bruxelas? · [paradas] · [veredito] · e isso foi só o primeiro dia.', 'Opcional: narração curta com o veredito (até 6 s).',
          'Vale parar 1 dia em Bruxelas? 🇧🇪\n\nNosso dia: [paradas reais]. Começamos pelo Atomium, de metrô.\n\nGastamos € [total do dia] por pessoa. Cotação: € 1 = R$ [PTAX da data].\n\nVeredito: [vale/depende/pula], porque [motivo real].\n\nSou o Diego e aqui eu mostro o primeiro dia em cada cidade. Segue pra ver o próximo.',
          CTA_SEGUIR, 'Centro de Bruxelas com a Placa. Texto da capa: “1 DIA VALE?”.', 'Falas + música da biblioteca baixa.',
          ['IMG_2170.MP4, IMG_2178.MP4 (720p: pedir os originais em resolução cheia)', 'Brutos de Bruxelas (decupagem pendente)', OUTRAS],
          PEND_PLACAR + ['Decupagem de Bruxelas: paradas do dia', 'Veredito do Diego', 'Originais em resolução cheia (as cópias são 720p)'],
          'Bruxelas', 'IMG_2170 + decupagem', 'Reel · Primeiro Dia (série) · Nível A · Bruxelas'),
    serie('p305', '2027-01-03', 'brg', 'Bruges', 'Primeiro dia em Bruges', 'Bate-volta pra Bruges: € [total].', 'Preço', 'B', 'dad',
          'Série: o bate-volta de Bruxelas a Bruges (o dia inteiro na cidade), com Placar do trem ao waffle.',
          'Quem vai à Bélgica e decide se vale o bate-volta. Envia para quem vai junto.',
          'Chegada em Bruges (decupagem) com a Placa `PRIMEIRO DIA EM / BRUGES` (Chegada) e o gancho.',
          [('0–2 s', 'Gancho', 'Chegada + Placa de abertura.'),
           ('2–25 s', 'Placar', PLACAR + ' Inclui o trem de ida e volta.'),
           ('2–16 s', 'O dia', 'Canal, centro e rua de compras, na ordem (decupagem), de 1,5 a 3 s cada.'),
           ('16–21 s', 'Pico', 'IMG_2693: Diego comendo waffle na rua (“muito, muito, muito”). Usar trecho diferente do Reel de 20/10.'),
           ('21–25 s', 'Fechamento', FECHO)],
          'bate-volta pra bruges: € [total] · trem · canal · waffle · e isso foi só o primeiro dia.', 'Sem narração nova.',
          'Bate-volta pra Bruges: € [total] por pessoa. 🇧🇪\n\n[trem de Bruxelas, horário de chegada e o que fizemos, na ordem].\n\nCotação: € 1 = R$ [PTAX da data].\n\nManda pra quem vai pra Bélgica com você.',
          'Manda pra quem vai pra Bélgica (envio).', 'Canal de Bruges com a Placa. Texto da capa: “BATE-VOLTA: € [TOTAL]”.', 'Falas + música da biblioteca.',
          ['IMG_2690 a IMG_2692 (720p) e IMG_2693 (4K)', 'Brutos de Bruges (decupagem pendente)', OUTRAS],
          PEND_PLACAR + ['Decupagem de Bruges: chegada, canal, centro', 'Preço do trem Bruxelas–Bruges', 'Não repetir os planos do waffle usados em 20/10'],
          'Bruges', 'Decupagem', 'Reel · Primeiro Dia (série) · Nível A · Bruges'),
]

# ───────────── 4. peças da série que mudam ─────────────
def nivel_a(p, extra_pend=()):
    p['nivel'] = 'A'
    p['chk'] = REF_A['chk']; p['grp'] = REF_A['grp']
    p['como'] = 'Nível A. ' + ST[p['prod']] + '.'
    p['obs'] = [o for o in p['obs'] if not o.startswith('Nível ')]
    p['obs'].insert(1, 'Série v4: um primeiro dia todo domingo às 19:00. Nível A com Placar (registro do Diego).')
    if not any(s['l'] == 'Placar' for s in p['sc']):
        p['sc'].insert(1, {'t': '2 s até o fim', 'l': 'Placar', 'x': PLACAR})
    p['pend'] = list(p['pend']) + PEND_PLACAR + list(extra_pend)
    p['code'] = p['code'].replace('Nível B', 'Nível A')
    p['v4'] = True


def troca(p, velho, novo):
    for k in ('leg', 'tela', 'cta'):
        p[k] = p[k].replace(velho, novo)
    for s in p['sc']:
        s['x'] = s['x'].replace(velho, novo)


a = P['p207']
a['titulo'] = 'Primeiro dia em Amsterdam'
a['gancho'] = 'Pousamos com frio e fome.'
a['gt'] = 'Identificação'
a['obj'] = 'Série e conversão: o primeiro dia em Amsterdam, aberto pela primeira hora real (aeroporto, frio e fome), com Placar.'
troca(a, 'primeira hora em amsterdam: frio e fome', 'pousamos com frio e fome')
a['leg'] = a['leg'].replace('Primeira hora em Amsterdam: frio e fome.', 'Primeiro dia em Amsterdam: pousamos com frio e fome.')
nivel_a(a, ['Se houver decupagem do resto do dia 1, trocar o Bilhete do pico pela primeira comida e cerveja'])

t = P['p217']
t['titulo'] = '12 cidades, 12 primeiros dias'
t['gancho'] = '12 cidades, 12 primeiros dias.'
t['obj'] = 'Conversão: o trailer da série dos domingos. Deixa clara a promessa do perfil para quem chegou por um Reel de outra cidade.'
for s in t['sc']:
    s['x'] = s['x'].replace('Destaque em “8”', 'Destaque em “12”').replace('Madrid, Lisboa.', 'Madrid, Lisboa, Roma, Florença, Veneza, Milão (Itália em fotos, 1,5 s cada).').replace('2 s cada', '1,5 s cada')
t['tela'] = '12 cidades, 12 primeiros dias · barcelona · amsterdam · bruxelas · bruges · paris · disneyland paris · madrid · lisboa · roma · florença · veneza · milão · segue pra ver a próxima'
t['leg'] = ('12 cidades, 12 primeiros dias. ✈️\n\nBarcelona, Amsterdam, Bruxelas, Bruges, Paris, Disneyland Paris, Madrid, Lisboa, Roma, Florença, Veneza e Milão. '
            'Em cada uma, eu mostro o primeiro dia como ele foi: a chegada, quanto custou, o que deu errado e o que valeu.\n\n'
            'Todo domingo sai um primeiro dia novo.\n\nSegue pra ver o primeiro dia de cada uma.')
t['pend'] = list(t['pend']) + ['Uma foto de chegada de Florença, Veneza e Milão']

pa = P['p234']
troca(pa, 'segue pra ver a disney.', 'segue pra ver o próximo.')
pa['leg'] = pa['leg'].replace('Segue pra ver o dia da Disney.', 'Segue pra ver o próximo primeiro dia.')
pa['cta'] = CTA_SEGUIR
nivel_a(pa, ['Sai no dia seguinte ao vlog de Paris (07/11): link do vlog só nos Stories'])

di = P['p215']
di['titulo'] = 'Primeiro dia na Disneyland Paris'
di['gancho'] = '2 parques em 1 dia: € [total].'
di['gt'] = 'Preço'
di['obj'] = 'Série: o dia na Disney (os 2 parques) com Placar e o veredito. Absorve “Vale ou pula: Disneyland Paris em 1 dia?”.'
for s in di['sc']:
    if s['l'] == 'Fechamento':
        s['x'] = 'Bilhete veredito (`vale.` / `depende:` / `pula.`) com a opinião real do Diego + ' + FECHO
di['leg'] = di['leg'].replace('2 parques da Disneyland Paris em 1 dia. 🏰', '2 parques da Disneyland Paris em 1 dia: € [total] por pessoa. 🏰')
di['pend'] = list(di['pend']) + ['Veredito do Diego (vale, depende ou pula)']
nivel_a(di, ['Sai no dia seguinte ao vlog da Disney (21/11)'])

ma = P['p221']
nivel_a(ma, ['Se “o momento que eu não esperava” foi no dia 1, ele é o pico deste Reel', 'Sai no dia seguinte ao vlog de Madrid (05/12)'])

ra = P['p247']
ra['titulo'] = '12 primeiros dias: qual foi o melhor?'
ra['gancho'] = 'Ranking: o melhor primeiro dia.'
ra['obj'] = 'Retrospectiva de fim de ano: ranking pessoal dos 12 primeiros dias. Reforça a série e gera discussão.'
for s in ra['sc']:
    s['x'] = s['x'].replace('8 linhas', '12 linhas').replace('Do 8º ao 2º: 2 s por cidade', 'Do 12º ao 2º: 1,5 s por cidade').replace('cidade nº 8', 'cidade nº 12').replace('cidade em 8º', 'cidade em 12º')
ra['tela'] = 'ranking: o melhor primeiro dia · 12º [cidade] … 1º [cidade] · [motivo]'
ra['q0'] = ra['q0'].replace('8 linhas', '12 linhas').replace('nº 8', 'nº 12')
ra['leg'] = ('Ranking: o melhor primeiro dia das nossas viagens. 🏆\n\n'
             + '\n'.join('%d. [cidade]' % n for n in range(12, 1, -1))
             + '\n1. [cidade]: [motivo em 1 frase]\n\nConcorda? Segue pra ver o primeiro dia da próxima cidade.')
ra['pend'] = ['Diego: ranking das 12 cidades e o motivo do 1º lugar']

ro = P['p254']
nivel_a(ro, ['D4: se o Diego preferir Roma sem Placar, voltar ao Nível B (e os outros 3 italianos seguem igual)'])

li = P['p270']
nivel_a(li, ['Sai no dia seguinte ao vlog de Lisboa (16/01)'])

for i, nd in NOVAS_DATAS.items():
    p = P[i]
    p['d'] = nd
    p['hora'] = HORA[dt.date.fromisoformat(nd).weekday()]

# ───────────── 5. montar a lista de posts ─────────────
posts = [p for p in D['posts'] if p['id'] not in SAEM]
removidos_shorts = [p for p in posts if p['kind'] == 'short_reuse' and p['d'] > HOJE]
posts = [p for p in posts if not (p['kind'] == 'short_reuse' and p['d'] > HOJE)]
posts += NOVAS

# Shorts: reaproveitam os Reels de terça e sábado (exceto ao vivo), no dia seguinte, 12:00
ns = max(int(p['code'].split()[-1]) for p in posts if p['kind'] == 'short_reuse' and p['code'].split()[-1].isdigit())
sseq = 500
modelo_s = {k: v for k, v in next(p for p in D['posts'] if p['kind'] == 'short_reuse' and not p.get('done')).items() if k not in ('done', 'aud', 'res')}
for p in sorted([p for p in posts if p['fmt'] == 'Reel' and p['plat'] == 'Instagram' and p.get('v3') and p['vk'] != 'jan'], key=lambda p: p['d']):
    if p['d'] < HOJE or dt.date.fromisoformat(p['d']).weekday() not in (1, 5):
        continue
    dd = (dt.date.fromisoformat(p['d']) + dt.timedelta(days=1)).isoformat()
    if dd > D['end']:
        continue
    ns += 1
    dm = p['d'][8:10] + '/' + p['d'][5:7]
    s = dict(modelo_s)
    s.update({'d': dd, 'video': p['video'], 'titulo': 'Short: ' + p['titulo'], 'vk': p['vk'], 'code': 'Short %02d' % ns, 'id': 'p%d' % sseq,
              'como': "Mesmo corte do Reel de %s (%s), exportado do projeto original, sem marca d'água. Título de até 60 caracteres com a palavra-chave da cidade. Sem citar o vídeo longo se ele ainda não saiu." % (dm, p['titulo']),
              'leg': p['gancho'] if not p['gancho'].startswith('(') else p['titulo']})
    posts.append(s)
    sseq += 1

posts.sort(key=lambda p: (p['d'], '00:00' if p['hora'] == '—' else p['hora']))
PID = {p['id']: p for p in posts}

# ───────────── 6. conferências ─────────────
CIDADE = {'p205': 'rom', 'p209': 'rom', 'p218': 'rom', 'p222': 'rom', 'p237': 'rom', 'p242': 'rom', 'p248': 'rom', 'p252': 'rom', 'p254': 'rom',
          'p230': 'ven', 'p243': 'ven', 'p302': 'ven', 'p233': 'flo', 'p301': 'flo', 'p258': 'mil', 'p303': 'mil'}
feed = [p for p in posts if p['plat'] == 'Instagram' and p['fmt'] in ('Reel', 'Carrossel', 'Foto')]
slots = Counter((p['d'], p['hora']) for p in feed if p['d'] >= HOJE)
assert all(v == 1 for v in slots.values()), [k for k, v in slots.items() if v > 1]
prev, semana = None, Counter()
for p in feed:
    c = CIDADE.get(p['id'], p['vk'])
    if c in ('multi', 'jan', 'ita'):
        prev = None
        continue
    if p['d'] >= HOJE:
        assert c != prev, ('cidade repetida em sequência', p['d'], c)
    if p['d'] >= '2026-10-12':  # a semana de hoje conta o post de 13/10
        semana[(dt.date.fromisoformat(p['d']).isocalendar()[:2], c)] += 1
        assert semana[(dt.date.fromisoformat(p['d']).isocalendar()[:2], c)] <= 2, ('mais de 2 na semana', p['d'], c)
    prev = c
serie_dom = [p for p in feed if p.get('pl') == 'SERIE' and p['d'] >= HOJE]

# ───────────── 7. semanas, Stories e interações ─────────────
LEITURAS = D['leituras']


def stories_for(date, ps, trip):
    reels = [p for p in ps if p['fmt'] == 'Reel' and p['plat'] == 'Instagram']
    cars = [p for p in ps if p['fmt'] == 'Carrossel']
    steps = []
    wd = dt.date.fromisoformat(date).weekday()
    if trip and date >= '2027-01-20':
        steps.append('Parte 01 · MANHÃ · STORYTELLING: abertura `AO VIVO DA VIAGEM` + Placar mini com a hora local.')
        steps.append('Parte 02 · DURANTE O DIA · RELACIONAMENTO: 2 ou 3 Stories do que está acontecendo (sem produção).')
        steps.append('Parte 03 · NOITE · ENGAJAMENTO: custo real do dia (só valores anotados) e enquete nativa “vale ou pula?”.')
        if reels or cars:
            steps.append('Parte 04 · PÓS-POST · CONVERSÃO: compartilhe o post do dia com 1 frase que não está nele.')
        t = 'Diário ao vivo da viagem'
    elif reels or cars:
        p = (reels or cars)[0]
        cta = {'DESEJO': 'enquete “Iria?” (Iria amanhã / Já fui)', 'UTIL': 'caixa de perguntas “Qual a sua dúvida sobre ' + p['video'] + '?”',
               'EXP': 'slider de emoji sobre o momento do Reel', 'SERIE': 'enquete “Qual cidade você quer ver o primeiro dia?” (2 opções do acervo)'}.get(p.get('pl'), 'pergunta aberta')
        if p['fmt'] == 'Carrossel':
            cta = 'compartilhe o slide 2 e pergunte “Qual slide você mandaria para alguém que vai?”'
        steps.append('Parte 01 · PÓS-POST · %s · CONVERSÃO: compartilhe o post com 1 frase que não está nele + %s.' % (p['hora'], cta))
        if p.get('pl') == 'SERIE' and wd == 6:
            steps.append('Parte 02 · NOITE · RELACIONAMENTO: “o dia inteiro está no vlog” + sticker de link para o YouTube, quando houver vlog da cidade (o link fica nos Stories, não no Reel).')
        else:
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


SEMANAS = {
    2: ('Rodízio + estreia da série', 'Barcelona, Roma e Paris na semana e a estreia do “Primeiro dia em X” no domingo (18/10)',
        ['4 Reels + 1 carrossel', 'Diego envia hora de chegada e gastos do dia 1 de Barcelona até sexta (16/10)', 'Nenhuma cidade em 2 posts seguidos'],
        ['Envios da dica da água (13/10): primeiro ponto do T5.', 'Roma de graça (14/10): salvamentos com capa de foto (T4, A) contra Roma € 421,50 (2 em 628).', 'Primeiro dia em Barcelona (18/10): seguidores por 1.000 contra a apresentação (31,8) e o POV (1,5).']),
    3: ('Série no domingo', 'Carrossel do roteiro logo depois do Reel de Barcelona e o primeiro dia em Amsterdam', ['4 Reels + 1 carrossel', 'Decupagem de Disney, Madrid e Lisboa iniciada', 'Dados do dia 1 de Amsterdam até 23/10'],
        ['Roteiro de 18 km (21/10): salvamentos do carrossel publicado depois do Reel.', 'Primeiro dia em Amsterdam (25/10): segundo ponto da série.']),
    4: ('Leitura 1 (01/11)', 'Trailer da série no domingo e a Leitura 1', ['4 Reels + 1 carrossel', 'Leitura 1 registrada em Aprendizados', 'Decidir horários pelo Insights'],
        ['Leitura 1: a série (Bahia, Barcelona, Amsterdam) converte acima do desejo puro (1,5 por 1.000)?', 'Sagrada (27/10) × Bruges 15 s (03/11): T2.', 'Trailer (01/11): fixar se converter mais que a apresentação.']),
    5: ('Paris', 'Vlog de Paris no sábado e o primeiro dia em Paris no domingo', ['4 Reels + 1 carrossel', 'Dados do dia 1 de Paris até 06/11'],
        ['Primeiro dia em Paris (08/11): T3 com o vlog saindo na véspera.', 'Gaudí de graça (04/11): T4, A.']),
    6: ('Comparações e Itália', 'Barcelona ou Madrid (T5) e o primeiro dia italiano em fotos (Florença)', ['4 Reels + 1 carrossel', 'Fotos e dados de Florença até 12/11'],
        ['T5: Barcelona ou Madrid (12/11) × Reels de cidade única.', 'Primeiro dia em Florença (15/11): o modelo de fotos com Placar converte como os de vídeo?']),
    7: ('Disney', 'Carrossel de Florença, Veneza em desejo e o primeiro dia na Disney', ['4 Reels + 1 carrossel', 'Inventário dos vídeos da Itália concluído'],
        ['Primeiro uso de vídeo ambiental da Itália (21/11).', 'Primeiro dia na Disney (22/11): envios (T3, B).']),
    8: ('Black Friday', 'Custos reais na semana em que muita gente compra passagem; primeiro dia em Veneza', ['4 Reels + 1 carrossel', 'Fotos e dados de Veneza até 26/11'],
        ['Envios do Reel “A passagem é só o começo” (24/11).', 'Salvamentos da Boqueria (26/11).']),
    9: ('Leitura 2 (06/12)', 'Fechar novembro, o primeiro dia em Madrid e a Leitura 2', ['4 Reels + 1 carrossel', 'Leitura 2 registrada', 'Decidir a cadência da série'],
        ['Leitura 2: se a mediana de seguidores por 1.000 da série ficar abaixo da dos outros pilares, a série passa a domingo sim, domingo não.', 'T1, T2 e T4: conclusões preliminares.']),
    10: ('Natal na Europa', 'Roma iluminada e o primeiro dia em Milão', ['4 Reels + 1 carrossel', 'Fotos e dados de Milão até 10/12'],
         ['Roma iluminada (08/12): envios e seguidores (T1, B).', 'McDonald’s (12/12): comentários.']),
    11: ('Natal em Roma', 'Roteiro do dia 25 em Roma e o primeiro dia em Bruxelas', ['4 Reels + 1 carrossel', 'Ranking do Diego definido até 20/12'],
         ['Salvamentos do carrossel de Natal (16/12).', 'Primeiro dia em Bruxelas (20/12): veredito e seguidores.']),
    12: ('Semana do Natal', 'Primeiro dia em Roma no Natal (24/12) e o ranking de fim de ano (27/12)', ['4 Reels + 1 carrossel', 'Agendar 24/12, 26/12 e 27/12 com antecedência'],
         ['Envios do Reel de 24/12 (data simbólica).', 'Comentários do ranking (27/12).', 'Não comparar a semana de festas com as outras sem levar o feriado em conta.']),
    13: ('Réveillon', 'Fim de ano com o frio da Europa, Milão, o Réveillon e o primeiro dia em Bruges', ['4 Reels + 1 carrossel', 'Dados do bate-volta de Bruges até 30/12'],
         ['Comentários do Reel do frio (29/12).', 'Semana atípica: registrar, mas não decidir por ela.']),
}

byday = {}
for p in posts:
    byday.setdefault(p['d'], []).append(p['id'])
for w in D['weeks']:
    if w['end'] < HOJE:
        continue
    if w['n'] in SEMANAS:
        w['tag'], w['obj'], w['metas'], w['observe'] = SEMANAS[w['n']]
    if w['n'] == 15:
        w['observe'] = ['Salvamentos do carrossel “Itália em 9 dias” (13/01).', 'Primeira noite em Lisboa (17/01): último primeiro dia do acervo antes da viagem.']
    days = []
    d0 = dt.date.fromisoformat(w['start'])
    for i in range(7):
        date = (d0 + dt.timedelta(days=i)).isoformat()
        if date > w['end']:
            break
        if date < HOJE:
            old = [x for x in w['days'] if x['date'] == date]
            if old:
                days.append(old[0])
            continue
        ps = [PID[i] for i in byday.get(date, [])]
        trip = date >= D['trip']['ini']
        days.append({'date': date, 'posts': byday.get(date, []), 'stories': stories_for(date, ps, trip), 'inter': inter_for(date, ps, trip)})
    w['days'] = days

indays = {i for w in D['weeks'] for d in w['days'] for i in d['posts']}
faltam = [p['id'] for p in posts if p['id'] not in indays]
assert not faltam, faltam
assert not (indays - set(PID)), indays - set(PID)

# ───────────── 8. metadados ─────────────
D['posts'] = posts
D['versao'] = 'v4 · 14/10/2026'
for pd in D['pend']:
    if pd['k'] == 32:
        pd['t'] = 'Custos do dia 1 de cada cidade (o Diego tem todos): hora de chegada e gastos na ordem, por pessoa ou do casal. Prioridade: Barcelona (até 16/10), Amsterdam (até 23/10), Paris, Florença, Disney, Veneza, Madrid, Milão, Bruxelas, Roma, Bruges, Lisboa'
D['pend'] += [
    {'k': 40, 't': 'Fotos de Florença, Veneza e Milão com EXIF e a data do primeiro dia de cada cidade (série v4: 15/11, 29/11 e 13/12)', 'type': 'text'},
    {'k': 41, 't': 'D1: atualizar o CLAUDE.md, seção 10 (a Itália passa a ter Reels de fotos, decisão do Diego em 14/10)', 'type': 'text'},
    {'k': 42, 't': 'D4: Roma com Placar (Nível A, aplicado) ou sem Placar (Nível B)? Os 4 italianos seguem a mesma escolha', 'type': 'text'},
]

out = html[:m.start(1)] + json.dumps(D, ensure_ascii=False) + html[m.end(1):]
out = out.replace("' peças no plano v3'", "' peças no plano v4'")
open(PAINEL, 'w', encoding='utf-8').write(out)

# ───────────── relatório ─────────────
print('saem:', len(SAEM), '| novas:', len(NOVAS), '| datas movidas:', len(NOVAS_DATAS), '| shorts refeitos:', len(removidos_shorts), '->', sseq - 500)
print('série a partir de hoje:', [(p['d'][8:] + '/' + p['d'][5:7], p['titulo']) for p in serie_dom])
v = [p for p in posts if p.get('v3')]
print('testes:', dict(Counter((p.get('teste') or {}).get('id', '—') + ':' + (p.get('teste') or {}).get('var', '') for p in v)))
