# -*- coding: utf-8 -*-
"""Aplica a revisão v5 (REVISAO_V5.md) sobre o painel v4.

Uso (de dentro de planejamento/):  python3 scripts/aplicar_v5.py
- Lê o painel v4 em versoes/painel-v4-2026-10-14-antes-da-v5.html (cópia criada na primeira execução).
- Mantém intacto tudo até 14/10/2026 (histórico e o dia de hoje).
- De 15/10/2026 a 07/02/2027: calendário do feed de scripts/v5_pecas.py (CAL), sem peças de custo.
- Shorts no mesmo dia do Reel de origem (20:30), para não criar um dia novo da cidade.
- Stories de cada dia com as cidades centrais registradas (st.cid).
- Regra de cidades (Diego, 14/10; ampliada em 14/10 para todos os formatos): no máximo 2 dias por semana
  (seg a dom) e nunca em dias seguidos, inclusive na virada de semana. O script falha se houver violação
  e grava AUDITORIA_CIDADES_V5.md.
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import v5_pecas as V  # noqa: E402

RAIZ = os.path.join(AQUI, '..')
PAINEL = os.path.join(RAIZ, 'planejamento-postagens.html')
BASE = os.path.join(RAIZ, 'versoes', 'painel-v4-2026-10-14-antes-da-v5.html')
AUDIT = os.path.join(RAIZ, 'AUDITORIA_CIDADES_V5.md')
HOJE = '2026-10-14'
INICIO = '2026-10-15'

if not os.path.exists(BASE):
    shutil.copyfile(PAINEL, BASE)
html = open(BASE, encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\n', html, re.S)
D = json.loads(m.group(1))
P = {p['id']: p for p in D['posts']}
NOME = dict(V.CIDADES, **V.NOME_JAN)

# ───────────── 1. o que fica de antes ─────────────
# Histórico até hoje fica como está. Do futuro, ficam os vlogs, os Stories de lançamento e de viagem e a tarefa de 18/01.
FICA_FUTURO = {'long', 'stories_launch', 'stories_partida', 'stories_embarque', 'setup'}
hist = [p for p in D['posts'] if p['d'] <= HOJE]
futuro_fixo = [p for p in D['posts'] if p['d'] > HOJE and p['kind'] in FICA_FUTURO]
saem_v4 = [p for p in D['posts'] if p['d'] > HOJE and p['kind'] not in FICA_FUTURO]

# ───────────── 1b. ajustes do dia 14/10 (autorizados pelo Diego em 14/10) ─────────────
P['p218']['adiado'] = True
P['p218']['pend'] = ['ADIADO em 14/10 por decisão do Diego: o carrossel traz valores, cotação e a etiqueta `QUANTO CUSTOU`, e os valores de Trevi e Panteão não foram reconferidos. Não publicar como está.',
                     'A versão sem valores é o p627 (Roma em 3 dias: o roteiro pela hora das fotos), em 18/11.'] + P['p218'].get('pend', [])
P['p218']['obs'] = P['p218']['obs'] + ['Adiado na revisão v5 (14/10/2026): peça de custo fora desta revisão. Conteúdo original preservado acima; ideia guardada em OPORTUNIDADES_CUSTOS.md.']
P['p401']['pend'] = ['Sem confirmação de publicação em 14/10 (pendência k 52). Se não subiu, deixar de lado: Barcelona já apareceu em 13 e 14/10.'] + P['p401'].get('pend', [])
for _w in D['weeks']:
    for _d in _w['days']:
        if _d['date'] == '2026-10-14':
            _d['stories'] = {'t': 'Dia sem post: pergunta', 'cid': [],
                             'steps': ['Parte 01 · NOITE · ENGAJAMENTO: enquete nativa “Qual cidade você quer ver primeiro aqui?” (sem cidade central e sem anunciar o que vem).',
                                       'Métrica do dia: taxa de resposta (respostas ÷ alcance) e saídas do 1º Story.']}

# Publicações com evidência registrada em PROPOSTA_V4_SERIE_PRIMEIRO_DIA.md (14/10): 11/10 publicado; 13/10 "saiu".
for pid, ev in (('p201', 'publicado em 11/10 (PROPOSTA_V4, seção 5: “11/10 ✓”)'),
                ('p202', 'publicado em 13/10 (PROPOSTA_V4, seção 6: “em 13/10 saiu Barcelona”)')):
    P[pid]['done'] = True
    P[pid]['obs'] = P[pid]['obs'] + ['Marcado como publicado na v5: ' + ev + '.']

# ───────────── 2. limpeza de custo ─────────────
RX_VAL = [re.compile(r'\s*\(≈ ?R\$[^)]*\)'), re.compile(r'€ ?\[?[\w\.,]*\]?(\s*\[[^\]]*\])?'), re.compile(r'R\$ ?\[?[\w\.,]*\]?')]
RESIDUOS = [
    (' Passe de metrô e ônibus de 72 h:.', ''), (' no site oficial [confirmar se por pessoa].', '.'), (' É a regra que segurou o orçamento.', ''),
    (', com preço quando houver', ''), ('Destaque em “18 km”', 'Destaque em “a pé”'), (', foi 25 euros por pessoa', ''),
    ('Master 25:51–26:10', 'Master 25:51–26:05 (cortar antes de “foi 25 euros”)'), (' ( confirmar se por pessoa)', ''),
]
CHK_TROCA = {
    'Valores em € e R$, com a cotação datada na legenda': 'Sem valores de custo (revisão v5: custos ficam para depois)',
    'Valores em € e R$, com a cotação datada': 'Sem valores de custo (revisão v5: custos ficam para depois)',
    'Placar só com registro real de hora e gasto': 'Sem Placar nesta revisão (ele mostra o gasto do dia)',
}


def sem_valor(t):
    if not isinstance(t, str):
        return t
    for rx in RX_VAL:
        t = rx.sub('', t)
    return re.sub(r'  +', ' ', t).replace(' .', '.').replace(' ,', ',').strip()


def limpar(p):
    tinha = False
    if isinstance(p.get('leg'), str):
        linhas = p['leg'].split('\n')
        boas = [l for l in linhas if not re.search(r'€|R\$|[Cc]otação|PTAX|orçamento|quanto custou|custo', l)]
        tinha |= len(boas) != len(linhas)
        p['leg'] = re.sub(r'\n{3,}', '\n\n', '\n'.join(boas)).strip()
    if isinstance(p.get('tela'), str) and re.search(r'€|R\$', p['tela']):
        p['tela'] = ' · '.join(s for s in p['tela'].split(' · ') if not re.search(r'€|R\$', s))
        tinha = True
    for k in ('sc', 'sl'):
        for it in p.get(k, []):
            for f in ('x', 't', 's'):
                if isinstance(it.get(f), str) and re.search(r'€|R\$|Placar', it[f]) and not (f == 't' and k == 'sc'):
                    it[f] = sem_valor(it[f].replace('Placar', 'Legenda Informação com a hora'))
                    tinha = True
    for f in ('gancho', 'titulo', 'q0', 'capa'):
        if isinstance(p.get(f), str) and re.search(r'€|R\$', p[f]):
            p[f] = sem_valor(p[f])
            tinha = True
    for k in ('sc', 'sl'):
        for it in p.get(k, []):
            x = it.get('x')
            if not isinstance(x, str):
                continue
            if 'gira a cada gasto' in x:
                x = 'Legenda Informação com a hora real do arquivo em cada lugar (sem Placar e sem valores nesta revisão).'
            for a, b in RESIDUOS:
                x = x.replace(a, b)
            x = re.sub(r'\s*Etiqueta de valor[^.]*\.?', '', x)
            x = re.sub(r'\s*e o Legenda Informação com a hora gira\.?', '.', x)
            it['x'] = re.sub(r'  +', ' ', x).strip()
            if it.get('l') == 'Placar':
                it['l'] = 'Hora'
    if isinstance(p.get('tela'), str):
        p['tela'] = ' · '.join(t for t in p['tela'].split(' · ') if not re.search(r'preço|valores registrados|\[valor', t))
    if isinstance(p.get('leg'), str):
        for a, b in RESIDUOS:
            p['leg'] = p['leg'].replace(a, b)
        n = [0]

        def renum(mm):
            n[0] += 1
            return '%d. ' % n[0]
        p['leg'] = re.sub(r'(?m)^\d+\. ', renum, p['leg'])
    p['chk'] = [CHK_TROCA.get(c, c) for c in p.get('chk', [])]
    p['pend'] = [x for x in p.get('pend', []) if not re.search(r'[Cc]usto|gasto|€|PTAX|cotação|[Vv]alor', x)]
    if tinha or p['id'] in V.LIMPAR_CUSTO:
        p['pend'].insert(0, V.SEM_CUSTO_PEND)
    p['obs'] = [o for o in p.get('obs', []) if 'Placar (registro do Diego)' not in o]
    return p


# ───────────── 3. peças novas: modelo a partir da v4 ─────────────
REF_B = next(p for p in D['posts'] if p.get('nivel') == 'B' and p['kind'] == 'v3_reel')
REF_C = P['p203']
PIL = {x['nome']: x for x in D['pilares']}
PLK = {'Vontade de ir': 'DESEJO', 'Chegar sabendo': 'UTIL', 'Como foi de verdade': 'EXP', 'Primeiro Dia (série)': 'SERIE'}
seq_reel, seq_car = Counter(), Counter()


def nova(n):
    car = n['fmt'] == 'Carrossel'
    ref = REF_C if car else REF_B
    k = n['vk']
    p = {
        'd': '', 'hora': '', 'plat': 'Instagram', 'fmt': n['fmt'], 'pilar': n['pilar'], 'pl': PLK[n['pilar']],
        'video': V.CIDADES.get(k, 'Vários destinos'), 'titulo': n['titulo'], 'gancho': n['gancho'] or '—',
        'como': ('Carrossel 3:4.' if car else 'Nível ' + n.get('nivel', 'B') + '.') + ' ' + D['stmat'][n['prod']] + '. Peça nova da v5.',
        'leg': n['leg'], 'cta': n['cta'], 'met': n['met'], 'kind': 'v3_car' if car else 'v3_reel', 'vk': k,
        'code': '', 'id': n['id'], 'obj': n['obj'],
        'sc': [] if car else [{'t': a, 'l': b, 'x': c} for a, b, c in n['sc']],
        'sl': [{'n': str(i + 1), 'x': x} for i, x in enumerate(n.get('sl', []))],
        'mat': n['mat'], 'chk': [CHK_TROCA.get(c, c) for c in ref['chk']], 'grp': ref['grp'],
        'obs': [('Pilar: %s. %s' % (n['pilar'], PIL[n['pilar']]['desc'])),
                ('Carrossel 3:4 (DS V2, 5.3): slide 2 funciona sozinho. Publicar com música da biblioteca (elegível para a aba Reels).' if car else
                 'Nível B (leve): cortes secos, legenda Padrão com scrim e 1 objeto de marca no pico (DS V2, 5.2).'),
                'Peça nova da revisão v5 (14/10/2026), criada a partir do acervo do Drive. Ver INVENTARIO_ACERVO_V5.md.',
                'Métrica principal: ' + n['met'] + '.'],
        'orig': {'fonte': n['fonte'], 'trecho': n['trecho'], 'dica': ''}, 'gt': n['gt'],
        'ativo': 'Ver as cenas: cada objeto de marca está indicado no momento em que entra (DS V2, 2 e 5).',
        'mx': dict(e=2, g=2 if n['gancho'] else 1, n=2, o=2, es=1, t=9 if n['gancho'] else 8,
                   dec='Produzir e publicar (pontuação de planejamento: julgamento, não dado)'),
        'v3': True, 'v5': True, 'motiv': n['motiv'],
        'q0': n.get('q0', ''), 'tela': n.get('tela', 'Slides acima.' if car else ''),
        'nar': n.get('nar', 'Não se aplica (carrossel).' if car else 'Sem narração.'),
        'capa': n['capa'], 'som': n['som'], 'hip': n['hip'], 'teste': n.get('teste'),
        'pend': n['pend'], 'nivel': '—' if car else n.get('nivel', 'B'), 'prod': n['prod'],
    }
    if p['teste']:
        p['obs'].append('Teste %s, variante %s: mantenha iguais as outras variáveis (duração, horário, tipo de cena).' % (p['teste']['id'], p['teste']['var']))
    if 'cid' in n:
        p['cid'] = n['cid']
    return p


NOVAS = {n['id']: nova(n) for n in V.NOVAS}

# ───────────── 4. calendário do feed ─────────────
feed = []
for d, hora, pid in V.CAL:
    p = json.loads(json.dumps(NOVAS[pid] if pid in NOVAS else P[pid]))
    assert pid not in V.SAEM, pid
    p['d'], p['hora'] = d, hora
    for k, v in V.REVISAO.get(pid, {}).items():
        p[k] = v
    if pid in V.REVISAO and 'como' not in V.REVISAO[pid] and p.get('fmt') == 'Reel':
        p['como'] = re.sub(r'Nível A', 'Nível ' + p.get('nivel', 'B'), p['como'])
    if p.get('pl') == 'SERIE' and p.get('nivel') == 'A':
        p['nivel'] = 'B'
        p['como'] = re.sub(r'^Nível A\.?', 'Nível B (revisão v5: sem Placar).', p['como'])
    if 'cid' not in p:
        p['cid'] = V.CID_V4.get(pid, [p['vk']] if p['vk'] in V.CIDADES else [])
    p['v5'] = True
    limpar(p)
    feed.append(p)

# códigos sequenciais
nr = nc = 0
for p in feed:
    if p['fmt'] == 'Reel':
        nr += 1
        p['code'] = 'Reel %02d · %s · Nível %s' % (nr, p['pilar'], p.get('nivel', 'B'))
    else:
        nc += 1
        p['code'] = 'Carrossel %02d · %s · Carrossel 3:4' % (nc, p['pilar'])

# ───────────── 5. Shorts (mesmo dia do Reel) ─────────────
shorts = []
for i, p in enumerate([x for x in feed if x['id'] in V.SHORTS]):
    sid = 'p%d' % (700 + i)
    t = V.SHORTS[p['id']]
    assert len(t) <= 60, t
    desc = (p['leg'].split('\n')[0] + '\n\n' + 'Primeiro Dia: o primeiro dia de cada cidade, do jeito que foi. #shorts')
    s = {
        'd': p['d'], 'hora': '20:30', 'plat': 'YouTube', 'fmt': 'Short', 'pilar': 'YouTube (complementar)', 'video': p['video'],
        'titulo': 'Short: ' + t, 'gancho': '—',
        'como': 'Mesmo corte do Reel de %s (%s), exportado do projeto original, sem marca d\'água. Sai no mesmo dia do Reel, às 20:30, para não criar um dia novo da cidade (regra de cidades). '
                'Adaptação: título do YouTube abaixo; se a legenda escrita usar gíria ou CTA do Instagram ("manda pra…"), trocar a frase final da tela por "segue o canal pra ver a próxima cidade".' % (p['d'][8:] + '/' + p['d'][5:7], p['titulo']),
        'leg': desc, 'cta': 'Inscrever-se no canal (fixar comentário com a pergunta do Reel).', 'met': 'Visualizações e % que assiste em vez de deslizar',
        'kind': 'short_reuse', 'vk': p['vk'], 'code': 'Short %02d' % (i + 1), 'id': sid,
        'obj': 'Descoberta no YouTube a partir de um Reel que se entende sem conhecer o perfil.',
        'sc': [], 'sl': [], 'mat': ['Projeto do Reel de origem (%s)' % p['id']],
        'chk': ['Exportar o Reel do projeto original, sem marca d\'água', 'Título de até 60 caracteres: ' + t,
                'Trocar o CTA final se for do Instagram', 'Cena mais forte no primeiro segundo', 'Funciona sem som', 'Publicar', 'Registrar as métricas em 48 horas'],
        'grp': [['Produção', 0, 3], ['Pré-publicação', 3, 5], ['Publicação', 5, 7]],
        'obs': ['YouTube é canal complementar: o Short segue o Reel, não o contrário.', 'Derivado de ' + p['id'] + ' (' + p['titulo'] + '). Comparar o desempenho dos dois em Aprendizados.'],
        'orig': {'fonte': 'Reel do Instagram', 'trecho': None, 'dica': ''}, 'cid': p['cid'], 'src': p['id'], 'v5': True,
    }
    p.setdefault('deriv', []).append(sid)
    shorts.append(s)

for p in futuro_fixo:
    p['cid'] = [p['vk']] if p['vk'] in V.CIDADES else []
    p['v5'] = True
    if p['kind'] == 'long':
        p['obs'] = p['obs'] + ['Regra de cidades: o vlog conta como aparição da cidade no sábado. O Reel do sábado é da mesma cidade; o de domingo, de outra.']

def trocar(o):
    if isinstance(o, str):
        for a, b in V.TROCAS_FINAIS:
            o = o.replace(a, b)
        return o
    if isinstance(o, list):
        return [trocar(x) for x in o]
    if isinstance(o, dict):
        return {k: trocar(x) for k, x in o.items()}
    return o


for p in futuro_fixo + feed + shorts:
    for k in list(p):
        if k not in ('id', 'd', 'hora', 'kind', 'vk'):
            p[k] = trocar(p[k])
    if isinstance(p.get('pend'), list):
        p['pend'] = [x for x in p['pend'] if x not in V.REMOVER_PEND]
    if p['id'] in V.PEND_EXTRA and isinstance(p.get('pend'), list):
        p['pend'] = p['pend'] + [x for x in V.PEND_EXTRA[p['id']] if x not in p['pend']]
    if p['kind'] == 'long' and V.PEND_VLOG not in p.get('pend', []):
        p['pend'] = (p.get('pend') or []) + [V.PEND_VLOG]

posts = hist + sorted(futuro_fixo + feed + shorts, key=lambda p: (p['d'], p['hora']))
PID = {p['id']: p for p in posts}

# ───────────── 6. Stories, interações e semanas ─────────────
TRIP0, TRIP1 = D['trip']['ini'], D['trip']['fim']


def stories_for(date, ps, nsem):
    wd = dt.date.fromisoformat(date).weekday()
    feedp = [p for p in ps if p['plat'] == 'Instagram' and p['fmt'] in ('Reel', 'Carrossel')]
    vlog = [p for p in ps if p['fmt'] == 'Vídeo longo']
    cid = sorted({c for p in feedp + vlog for c in p.get('cid', [])})
    steps = []
    if TRIP0 <= date <= TRIP1:
        steps = ['Parte 01 · MANHÃ · STORYTELLING: abertura `AO VIVO DA VIAGEM` + Placar mini só com a hora local (sem valor).',
                 'Parte 02 · DURANTE O DIA · RELACIONAMENTO: 2 ou 3 Stories do que está acontecendo, sem produção.',
                 'Parte 03 · NOITE · ENGAJAMENTO: enquete nativa “vale ou pula?” sobre o lugar do dia.']
        if feedp:
            steps.append('Parte 04 · PÓS-POST · CONVERSÃO: compartilhe o post do dia com 1 frase que não está nele.')
        return {'t': 'Diário ao vivo da viagem', 'steps': steps + ['Cidade dos Stories: a cidade onde o Diego está (cobertura ao vivo, ver decisão D3 em REVISAO_V5.md).'],
                'cid': cid, 'nota': 'ao vivo'}
    if feedp:
        p = feedp[0]
        cta = {'DESEJO': 'enquete “Iria?” (Iria amanhã / Já fui)', 'UTIL': 'caixa de perguntas “Qual a sua dúvida sobre ' + p['video'] + '?”',
               'EXP': 'slider de emoji sobre o momento do post', 'SERIE': 'enquete “Qual primeiro dia você quer ver?” (2 cidades do acervo)'}.get(p.get('pl'), 'pergunta aberta')
        if p['fmt'] == 'Carrossel':
            cta = 'compartilhe o slide 2 e pergunte “Qual slide você mandaria para alguém que vai?”'
        steps.append('Parte 01 · PÓS-POST · %s · CONVERSÃO: compartilhe o post com 1 frase que não está nele + %s.' % (p['hora'], cta))
        if vlog:
            steps.append('Parte 02 · NOITE · RELACIONAMENTO: “o dia inteiro está no vlog” + sticker de link para o YouTube.')
        elif p.get('pl') == 'SERIE':
            steps.append('Parte 02 · NOITE · RELACIONAMENTO: 1 cena do mesmo primeiro dia que ficou de fora do Reel (mesma cidade, mesmo dia).')
        else:
            steps.append('Parte 02 · NOITE · RELACIONAMENTO: 1 bastidor da edição ou da escolha do material, da mesma cidade do post.')
        t = 'Pós-post + bastidor'
    elif wd == 0:
        steps.append('Parte 01 · NOITE · ENGAJAMENTO: pergunta da semana (ver card). Sem cidade central.')
        t = 'Pergunta da semana'
    elif wd == 4:
        if nsem % 2:
            steps.append('Parte 01 · DURANTE O DIA · RELACIONAMENTO: quiz “Onde foi isso?” com 1 foto e 3 opções de cidade. As 3 cidades são opções do quiz, não o tema (menção incidental).')
            t = 'Lembrança com quiz'
        else:
            return {'t': 'Sem Stories', 'steps': ['Dia sem Stories de propósito: sexta de produção, sem motivo editorial para postar (STORIES_ESTRATEGIA.md, 1).'], 'cid': []}
    else:
        steps.append('Parte 01 · DURANTE O DIA · RELACIONAMENTO: 1 a 3 Stories de bastidor (edição, escolha da capa), sem cidade central.')
        t = 'Bastidores'
    steps.append('Métrica do dia: taxa de resposta (respostas ÷ alcance) e saídas do 1º Story.')
    return {'t': t, 'steps': steps, 'cid': cid}


def inter_for(date, ps):
    wd = dt.date.fromisoformat(date).weekday()
    trip = TRIP0 <= date <= TRIP1
    out = []
    if any(p['plat'] == 'Instagram' and p['fmt'] in ('Reel', 'Carrossel') for p in ps):
        out.append('Instagram: responder todos os comentários em até 60 minutos depois de postar.')
    if any(p['fmt'] == 'Vídeo longo' for p in ps):
        out.append('YouTube: responder os comentários nas primeiras 2 horas.')
    if any(p['fmt'] == 'Short' for p in ps):
        out.append('YouTube Shorts: fixar comentário com a pergunta do Reel de origem.')
    if wd in (0, 2, 4) and not trip:
        out.append('10 min: deixar 5 comentários de verdade em perfis de viagem (de preferência de quem fala com o mesmo público).')
    if wd == 0:
        out.append('10 min de Insights: registrar as métricas de 48 h dos posts da semana anterior em Aprendizados (inclui visualizações e seguidores).')
    for L in D['leituras']:
        if L['d'] == date:
            out.append(L['t'] + ': ' + L['o'])
    if trip:
        out.append('Responder comentários e mensagens uma vez por dia, à noite.')
    return out


SEM = {
    2: ('Paris e Roma', 'Paris (o jardim fechado e a Torre inteira) e os dois pores do sol de Roma no domingo'),
    3: ('Vlog de Amsterdam · estreia da série', 'Waffle de Bruges, o Gaudí da calçada, os 2 erros, o primeiro dia em Amsterdam no sábado (com o vlog) e a estreia da série com Barcelona no domingo (25/10)'),
    4: ('Leitura 1 (01/11)', "Tony's, o roteiro de Barcelona, a Grand Place de dia e à noite, Paris sem texto e o trailer da série"),
    5: ('Vlog de Paris', 'Roma (o teto que engana), as comidas de Amsterdam, Bruges sem texto, o primeiro dia em Paris no sábado e o céu rosa de Amsterdam'),
    6: ('Comparações', 'Beijo escondido, Paris em 1 dia, Barcelona ou Madrid (T5), o castelo que muda de cor e a primeira mordida'),
    7: ('Vlog da Disney', 'Lisboa, o roteiro de Roma, Bruxelas em planos, o primeiro dia na Disney e o Retiro'),
    8: ('Fim de novembro', 'Boqueria, o dia da Disney em carrossel, a Torre que pisca, os cisnes de Bruges e a janela da Casa Batlló'),
    9: ('Vlog de Madrid · Leitura 2 (06/12)', 'Amsterdam, o roteiro de Bruxelas, o Park Güell, o primeiro dia em Madrid e Roma iluminada'),
    10: ('Madrid em destaque', 'O show em Madrid, o roteiro de Amsterdam, Madrid em 2 dias, o McDonald\'s e os canais'),
    11: ('Vlog de Bruxelas', 'Os 3 xixis de Bruxelas, Natal em Roma, Paris + Disney, o primeiro dia em Bruxelas e Camp Nou × Bernabéu'),
    12: ('Semana do Natal', 'Amsterdam de bicicleta, Bruges em fotos, o primeiro dia em Roma no Natal (24/12), o Montjuïc e o ranking'),
    13: ('Vlog de Bruges', 'O frio, o roteiro de Madrid, a trilha de Lisboa, o primeiro dia em Bruges e a Disney'),
    14: ('Leitura 3 (10/01) e anúncio', 'Sagrada com antecedência, o dia da Disney pelo relógio, o stroopwafel, o aeroporto e o anúncio da viagem'),
    15: ('Vlog de Lisboa · pré-viagem', 'Madrid a pé, Lisboa, as galerias de chocolate, a primeira noite em Lisboa e Gràcia'),
    16: ('Viagem: partida', 'Bruges, o mapa dos 9 primeiros dias, Lisboa de manhã, o primeiro dia ao vivo e a Notre-Dame'),
    17: ('Viagem', 'Ao vivo + acervo: Bairro Gótico, Roma às 8h25 e a pergunta dos destinos'),
    18: ('Viagem e Leitura 4', 'Ao vivo, Heineken (vale ou pula) e o balanço do ciclo'),
}
PERG_TROCA = {8: {'q': 'Qual cidade você quer ver primeiro aqui no perfil?', 'tipo': 'Enquete'},
              12: {'q': 'Qual primeiro dia você quer ver de novo, com mais detalhes?', 'tipo': 'Caixa de perguntas'}}

byday = defaultdict(list)
for p in posts:
    byday[p['d']].append(p['id'])
for w in D['weeks']:
    if w['end'] < INICIO:
        continue
    if w['n'] in SEM:
        w['tag'], w['obj'] = SEM[w['n']]
        ps = [PID[i] for d in w['days'] for i in byday.get(d['date'], [])]
        nre = sum(1 for p in ps if p['fmt'] == 'Reel' and p['plat'] == 'Instagram')
        nca = sum(1 for p in ps if p['fmt'] == 'Carrossel')
        cids = Counter(c for p in ps if p['plat'] == 'Instagram' for c in p.get('cid', []))
        w['metas'] = ['%d Reels + %d carrossel' % (nre, nca) if nca == 1 else '%d Reels + %d carrosséis' % (nre, nca),
                      'Nenhuma cidade em 3 dias da semana nem em dias seguidos (auditoria v5)', 'Nenhuma peça de custo nesta revisão']
        w['observe'] = ['%s: %s' % (PID[i]['titulo'], PID[i]['met']) for d in w['days'] for i in byday.get(d['date'], [])
                        if PID[i]['plat'] == 'Instagram' and PID[i]['fmt'] in ('Reel', 'Carrossel')][:4]
    if w['n'] in PERG_TROCA and w.get('pergunta'):
        w['pergunta'].update(PERG_TROCA[w['n']])
    for d in w['days']:
        if d['date'] < INICIO:
            continue
        ps = [PID[i] for i in byday.get(d['date'], [])]
        d['posts'] = [p['id'] for p in ps]
        d['stories'] = stories_for(d['date'], ps, w['n'])
        d['inter'] = inter_for(d['date'], ps)

indays = {i for w in D['weeks'] for d in w['days'] for i in d['posts']}
faltam = [p['id'] for p in posts if p['id'] not in indays]
assert not faltam, faltam

# ───────────── 7. auditoria da regra de cidades ─────────────
dias = defaultdict(lambda: defaultdict(list))  # data -> cidade -> [itens]
for p in posts:
    if p['d'] < '2026-10-12' or p['fmt'] == 'Setup':
        continue
    cs = p.get('cid')
    if cs is None:
        cs = [p['vk']] if p['vk'] in V.CIDADES else []
    for c in cs:
        dias[p['d']][c].append('%s %s' % (p['fmt'], p['id']))
for w in D['weeks']:
    for d in w['days']:
        st = d.get('stories') or {}
        if d['date'] >= '2026-10-12' and st.get('cid'):
            for c in st['cid']:
                dias[d['date']][c].append('Stories')

viol = []
datas = sorted(dias)
for c in sorted({c for d in dias.values() for c in d}):
    ds = sorted(d for d in datas if c in dias[d])
    for a, b in zip(ds, ds[1:]):
        if (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days == 1 and b >= INICIO:
            viol.append('%s em dias seguidos: %s e %s' % (NOME.get(c, c), a, b))
    sem = Counter(dt.date.fromisoformat(d).isocalendar()[:2] for d in ds if d >= '2026-10-12')
    for k, n in sem.items():
        if n > 2:
            viol.append('%s em %d dias na semana %s' % (NOME.get(c, c), n, k))

# tabela
lin = ['# Auditoria da distribuição de cidades · v5', '',
       '**Gerado por** `scripts/aplicar_v5.py` em 14/10/2026 · **Período:** 12/10/2026 (semana em curso) a 07/02/2027 · **Regra:** cada cidade em no máximo 2 dias por semana (seg a dom) e nunca em dias seguidos, inclusive na virada de semana. Conta todos os formatos: Reels, carrosséis, YouTube Shorts, vlogs, Stories de lançamento e Stories com cidade central.', '',
       '**Como cada formato conta:** Short sai no mesmo dia do Reel de origem (não cria dia novo). Vlog conta no sábado em que sai. Comparação de 2 ou 3 cidades conta para cada uma. Panorama (4 cidades ou mais, nenhuma dominante: trailer, ranking, mapa, 2 erros, primeira mordida, perguntas de destino e balanço) conta como "Várias" e não soma para nenhuma cidade. Quiz "Onde foi isso?" de sexta: as 3 cidades são opções, não o tema (menção incidental, registrada assim nos Stories). Cidades da viagem de janeiro: "cidade 1, 2 e 3" até o Diego definir.', '',
       '**Resultado:** ' + ('nenhuma violação.' if not viol else '%d violações (ver fim).' % len(viol)), '']
semana_atual = None
for d in datas:
    k = dt.date.fromisoformat(d).isocalendar()[:2]
    if k != semana_atual:
        semana_atual = k
        seg = dt.date.fromisocalendar(k[0], k[1], 1)
        lin += ['', '### Semana de %s a %s' % (seg.strftime('%d/%m'), (seg + dt.timedelta(days=6)).strftime('%d/%m/%Y')), '',
                '| Data | Dia | Cidade | Itens | Dias da cidade na semana | OK |', '|---|---|---|---|---:|:-:|']
    for c, its in sorted(dias[d].items()):
        n = sum(1 for x in datas if c in dias[x] and dt.date.fromisoformat(x).isocalendar()[:2] == k)
        dw = 'seg ter qua qui sex sáb dom'.split()[dt.date.fromisoformat(d).weekday()]
        lin.append('| %s | %s | %s | %s | %d | %s |' % (d[8:] + '/' + d[5:7], dw, NOME.get(c, c), ', '.join(its), n, '✓' if n <= 2 else '✗'))
lin += ['', '## Dias seguidos e virada de semana', '', 'Verificado para todas as cidades, de 15/10/2026 a 07/02/2027, contando o domingo e a segunda seguinte: ' +
        ('nenhuma cidade aparece em dois dias seguidos.' if not any('seguidos' in v for v in viol) else 'ver violações.'), '']
tot = Counter(c for d in datas if d >= INICIO for c in dias[d])
lin += ['## Dias de cada cidade no período (15/10 a 07/02)', '', '| Cidade | Dias |', '|---|---:|'] + ['| %s | %d |' % (NOME.get(c, c), n) for c, n in tot.most_common()]
if viol:
    lin += ['', '## Violações', ''] + ['- ' + v for v in viol]
open(AUDIT, 'w', encoding='utf-8').write('\n'.join(lin) + '\n')
if viol:
    print('\n'.join(viol))
    sys.exit('VIOLAÇÕES na regra de cidades: painel não gravado.')

# ───────────── 8. metadados e gravação ─────────────
TROCA_SEM = [('Responder com o custo real da cidade, quando houver registro.', 'Responder com o que aconteceu de verdade na cidade (sem valores nesta revisão).'),
             ('"Quanto custou"', '"Onde comer"')]
for w in D['weeks']:
    if w['end'] >= INICIO:
        w2 = json.dumps(w, ensure_ascii=False)
        for a, b in TROCA_SEM:
            w2 = w2.replace(a, b)
        w.clear()
        w.update(json.loads(w2))
for t in D['testes']:
    if t['id'] == 'T1':
        t['variavel'] = 'Camada de informação (hora, lugar ou como chegar; sem preço nesta revisão) num Reel de desejo de 12 a 16 s'
D['posts'] = posts
D['versao'] = 'v5 · 14/10/2026'
D['dest'].update({'ita': 'Roma (Itália)'})
D['stmat']['dec'] = 'Decupagem pendente'
D['saem_v5'] = [{'id': k, 'titulo': P[k]['titulo'], 'motivo': v} for k, v in V.SAEM.items() if k in P]
NOVAS_PEND = [
    {'k': 50, 't': 'Acervo: a análise do Colab de 15/10 cobre 1.945 vídeos de 8 cidades e está em acervo/ (índice, transcrição e linha do tempo). Só algumas folhas de contato foram vistas: cada peça marca o que foi visto e o que falta ver', 'type': 'text'},
    {'k': 51, 't': 'Florença, Veneza e Milão reabertas em 15/10 com os vídeos da pasta Itália (p301, p302, p303, p230 e p259). Em Veneza aparecem outras pessoas além de vocês dois: confirmar se podem aparecer. Milão tem pouco vídeo e não tem “primeiro dia” gravado', 'type': 'text'},
    {'k': 52, 't': 'Confirmar o que saiu de 10 a 14/10: Atomium (10/10), POV do Atomium (pedido de 12/10), Short de 11/10 e Short de 14/10. O carrossel “Roma de graça” (14/10) foi adiado por decisão do Diego: a versão sem valores é o p627, em 18/11', 'type': 'text'},
    {'k': 53, 't': 'D3: Stories ao vivo durante a viagem mostram a cidade onde você está todos os dias. Aceitar como exceção da regra de cidades ou limitar a 2 dias por cidade? (REVISAO_V5.md)', 'type': 'text'},
    {'k': 54, 't': 'Viagem de janeiro: cidades e ordem (as peças usam “cidade 1, 2 e 3”); a auditoria é refeita quando chegarem', 'type': 'text'},
    {'k': 55, 't': 'Lisboa: confirmar se houve noite em 22/03 (os arquivos verificados são de 23/03 de manhã); o Reel “Primeira noite em Lisboa” depende disso', 'type': 'text'},
    {'k': 56, 't': 'Madrid 20/03 à noite: o que era o show e onde foi (Reel de 08/12)', 'type': 'text'},
]
D['pend'] = [x for x in D['pend'] if x['k'] not in (32, 34, 40, 42)] + NOVAS_PEND
for x in D['pend']:
    if x['k'] == 41:
        x['t'] = 'D1: a Itália tem 214 vídeos (CLAUDE.md, seção 10, atualizado em 15/10). Confirmar que vídeo da Itália pode virar Reel, e se os Reels de fotos de Roma continuam'
out = html[:m.start(1)] + json.dumps(D, ensure_ascii=False) + html[m.end(1):]
out = out.replace("' peças no plano v4'", "' peças no plano v5'").replace('painel de conteúdo (v3)', 'painel de conteúdo (v5)')
open(PAINEL, 'w', encoding='utf-8').write(out)

# ───────────── relatório ─────────────
ig = [p for p in feed]
print('feed:', Counter(p['fmt'] for p in ig), '| shorts:', len(shorts), '| novas:', len(NOVAS), '| saem:', len(V.SAEM))
print('por pilar:', dict(Counter(p['pilar'] for p in ig)))
print('por cidade (peças do feed):', dict(Counter(','.join(p['cid']) or 'Várias' for p in ig)))
print('status:', dict(Counter(p['prod'] for p in ig)))
print('testes:', dict(Counter((p.get('teste') or {}).get('id', '—') + ':' + (p.get('teste') or {}).get('var', '') for p in ig)))
print('ganchos >7 palavras:', [(p['id'], p['gancho']) for p in ig if p['gancho'] != '—' and len(p['gancho'].split()) > 7])
dup = [g for g, n in Counter(p['gancho'] for p in ig if p['gancho'] != '—').items() if n > 1]
print('ganchos repetidos:', dup)
resto = [(p['id'], f) for p in ig for f in ('leg', 'tela', 'gancho', 'titulo') if isinstance(p.get(f), str) and re.search(r'€|R\$', p[f])]
print('restos de valor em €/R$:', resto)
print('violações:', len(viol))
