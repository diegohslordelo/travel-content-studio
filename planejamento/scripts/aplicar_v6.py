"""Aplica a revisão v6 (15/10/2026) ao painel: calendário até 28/02/2027 em todas as plataformas.

Uso (de dentro de planejamento/):  python3 scripts/aplicar_v6.py

- Base: cópia do painel v5 em versoes/painel-v5-2026-10-15-antes-da-v6.html (criada na 1ª execução).
- Datas: scripts/v6_plano.py. Conteúdo novo: scripts/v6_conteudo_*.py.
- Não muda: histórico (até 15/10), datas e títulos dos vídeos longos do YouTube, registros de custo.
- Grava: o painel e os relatórios (AUDITORIA_CIDADES_V6.md, AUDITORIA_LANCAMENTOS_V6.md, EQUILIBRIO_EDITORIAL_V6.md,
  CALENDARIO_V6.md). Não grava nada se a regra de cidades tiver violação.
"""
import datetime as dt
import glob
import importlib.util
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import v6_plano as PL  # noqa: E402

PAINEL = os.path.join(RAIZ, 'planejamento-postagens.html')
BASE = os.path.join(RAIZ, 'versoes', 'painel-v5-2026-10-15-antes-da-v6.html')
if not os.path.exists(BASE):
    shutil.copyfile(PAINEL, BASE)
html = open(BASE, encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\n', html, re.S)
D = json.loads(m.group(1))
P = {p['id']: p for p in D['posts']}
HOJE, INI, FIM = PL.HOJE, '2026-10-16', PL.FIM
NOME = dict(PL.CIDADES)

# ───────────── conteúdo dos grupos ─────────────
C = dict(PECAS={}, REVISOES={}, TIKTOK={}, SHORT_CAP={}, STORIES={}, TT_ADAPT={}, YT_ADAPT={})
for f in sorted(glob.glob(os.path.join(AQUI, 'v6_conteudo_*.py'))):
    spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for k in C:
        for kk, vv in (getattr(mod, k, {}) or {}).items():
            C[k][kk] = vv
# o p218 do histórico (adiado em 14/10) continua; a versão nova de Roma com custos ganha outro id
RENOMEIA = {'p218': 'p851'}
for k_old, k_new in RENOMEIA.items():
    if k_old in C['PECAS']:
        C['PECAS'][k_new] = C['PECAS'].pop(k_old)

# ───────────── base: o que fica ─────────────
JAN = {'p266', 'p275', 'p277', 'p280', 'p282', 'p283', 'p285', 'p286', 'p399', 'p168', 'p171'}
hist = [p for p in D['posts'] if p['d'] <= HOJE]
longos = [p for p in D['posts'] if p['kind'] == 'long']
lanc_st = [p for p in D['posts'] if p['d'] > HOJE and p['kind'] == 'stories_launch']
futuro_v5 = {p['id']: p for p in D['posts'] if p['d'] > HOJE and p['kind'] not in ('long', 'stories_launch')}

# ───────────── pilares, status e textos ─────────────
D['pilares'] += [
    {'k': 'CUSTO', 'nome': 'Quanto custa', 'desc': 'Custos e orçamento: quanto custou, o que valeu pagar e o que foi de graça, sempre com dados reais fornecidos pelo Diego na produção. Salvamentos e envios.'},
    {'k': 'LOCO', 'nome': 'Como se mover', 'desc': 'Locomoção e logística: como a gente se deslocou de verdade (metrô, trem, a pé, barco) e como organizar os trajetos. Salvamentos.'},
    {'k': 'PREP', 'nome': 'Antes de ir', 'desc': 'Documentação e preparação: o que conferir antes de embarcar, sempre conferido na fonte oficial no dia da produção. Salvamentos e envios.'},
]
PLK = {'Vontade de ir': 'DESEJO', 'Chegar sabendo': 'UTIL', 'Como foi de verdade': 'EXP', 'Primeiro Dia (série)': 'SERIE',
       'Quanto custa': 'CUSTO', 'Como se mover': 'LOCO', 'Antes de ir': 'PREP'}
PIL = {x['nome']: x for x in D['pilares']}
D['stmat'].update({'cus': 'Aguardando dados de custos do Diego', 'ofc': 'Conferir fonte oficial na produção',
                   'fut': 'Material futuro'})
D['dest'].pop('jan', None)
D['trip'] = None
D['end'] = FIM
D['versao'] = 'v6 · 15/10/2026'

SEM_CUSTO = 'Revisão v5: nenhum valor em € ou R$ na peça, na legenda ou na tela (custos ficam para depois).'
PEND_VLOG_V5 = [x for p in longos for x in p.get('pend', []) if 'trecho de gastos' in x]
PEND_CUS = 'CUSTOS: aguardando dados de custos do Diego na produção desta peça (nenhum valor foi inventado ou tirado dos vídeos).'
CHK_CUS = 'Valores só com os dados do Diego para esta peça (escopo, por pessoa ou casal, cotação com data)'
CHK_PLACAR = 'Placar só com registro real de hora e gasto fornecido pelo Diego (DS V2, 2.5)'
CHK_OFC = 'Regra de documento, entrada ou tarifa conferida na fonte oficial no dia (data e fonte na legenda)'


def sc_dicts(sc):
    return [x if isinstance(x, dict) else {'t': x[0], 'l': x[1], 'x': x[2]} for x in (sc or [])]


def sl_dicts(sl):
    return [x if isinstance(x, dict) else {'n': str(i + 1), 'x': x} for i, x in enumerate(sl or [])]


def cus_pend(n):
    c = n.get('cus')
    if not c:
        return []
    return [PEND_CUS, 'Dados necessários: ' + '; '.join(c.get('dados', [])),
            'Escopo: ' + c.get('escopo', '—') + ' · Quando: ' + c.get('quando', 'na produção desta peça')]


REF_R = next(p for p in D['posts'] if p.get('nivel') == 'B' and p['kind'] == 'v3_reel')
REF_C = P['p203']
CHK_TROCA = {'Valores em € e R$, com a cotação datada na legenda': CHK_CUS}


def chk_para(fmt, n):
    ref = REF_C if fmt == 'Carrossel' else REF_R
    chk = [c for c in ref['chk'] if 'nenhum valor' not in c.lower()]
    extra = []
    if n.get('prod') == 'cus' or n.get('cus'):
        extra.append(CHK_CUS)
    if n.get('tipo') == 'serie' or 'Placar' in json.dumps(n.get('sc', []), ensure_ascii=False):
        extra.append(CHK_PLACAR)
    if n.get('prod') == 'ofc':
        extra.append(CHK_OFC)
    i = ref['grp'][1][2] if len(ref['grp']) > 1 else len(chk)
    chk = chk[:i] + extra + chk[i:]
    grp = [[g[0], g[1] + (len(extra) if g[1] >= i else 0), g[2] + (len(extra) if g[2] >= i else 0)] for g in ref['grp']]
    return chk, grp


def nova(pid, n):
    car = n['fmt'] == 'Carrossel'
    chk, grp = chk_para(n['fmt'], n)
    pil = n.get('pilar', 'Vontade de ir')
    nivel = '—' if car else n.get('nivel', 'B')
    p = {
        'd': '', 'hora': '', 'plat': 'Instagram', 'fmt': n['fmt'], 'pilar': pil, 'pl': PLK.get(pil, 'DESEJO'),
        'video': '', 'titulo': n['titulo'], 'gancho': n.get('gancho') or '—',
        'como': ('Carrossel 3:4.' if car else 'Nível %s.' % nivel) + ' ' + D['stmat'].get(n.get('prod', 'dec'), '') + '. Peça nova da v6.',
        'leg': n.get('leg', ''), 'cta': n.get('cta', ''), 'met': n.get('met', ''), 'kind': 'v3_car' if car else 'v3_reel',
        'vk': 'ita', 'code': '', 'id': pid, 'obj': n.get('obj', ''),
        'sc': [] if car else sc_dicts(n.get('sc')), 'sl': sl_dicts(n.get('sl')) if car else [],
        'mat': n.get('mat', []), 'chk': chk, 'grp': grp,
        'obs': ['Pilar: %s. %s' % (pil, PIL.get(pil, {}).get('desc', '')),
                'Peça da revisão v6 (15/10/2026), feita a partir do acervo (acervo/ e planejamento/DECUPAGEM_*.md).',
                'Métrica principal: ' + n.get('met', '') + '.'],
        'orig': {'fonte': n.get('fonte', ''), 'trecho': n.get('trecho'), 'dica': ''}, 'gt': n.get('gt', 'Afirmação'),
        'ativo': 'Ver as cenas: cada objeto de marca está indicado no momento em que entra (DS V2, 2 e 5).',
        'mx': dict(e=2, g=2, n=2, o=2, es=1, t=9, dec='Produzir e publicar (pontuação de planejamento: julgamento, não dado)'),
        'v3': True, 'v6': True, 'motiv': n.get('motiv', ''), 'q0': n.get('q0', ''),
        'tela': n.get('tela', 'Slides acima.' if car else ''), 'nar': n.get('nar', 'Não se aplica (carrossel).' if car else 'Sem narração.'),
        'capa': n.get('capa', ''), 'som': n.get('som', ''), 'hip': n.get('hip', ''), 'teste': n.get('teste'),
        'pend': cus_pend(n) + list(n.get('pend', [])), 'nivel': nivel, 'prod': n.get('prod', 'dec'),
    }
    for k in ('cus', 'video_longo', 'tipo'):
        if n.get(k):
            p[k] = n[k]
    return p


def revisar(p, r):
    for k, v in r.items():
        if k in ('tt', 'yt'):
            continue
        if k == 'sc':
            p['sc'] = sc_dicts(v)
        elif k == 'sl':
            p['sl'] = sl_dicts(v)
        elif k == 'pend':
            p['pend'] = list(v)
        else:
            p[k] = v
    if r.get('pilar'):
        p['pl'] = PLK.get(r['pilar'], p.get('pl'))
    if r.get('cus') or r.get('prod') == 'cus':
        p['pend'] = cus_pend(p) + [x for x in p.get('pend', []) if x not in cus_pend(p)]
        if CHK_CUS not in p['chk']:
            p['chk'] = p['chk'][:3] + [CHK_CUS] + p['chk'][3:]
            p['grp'] = [[g[0], g[1] + (1 if g[1] >= 3 else 0), g[2] + 1] for g in p['grp']]
    if r.get('tipo') == 'serie':
        p['nivel'] = 'A'
        p['como'] = 'Nível A (v6: Placar de custos obrigatório, dados do Diego na produção). ' + D['stmat'].get(p.get('prod', 'cus'), '') + '.'
        if CHK_PLACAR not in p['chk']:
            p['chk'] = p['chk'][:3] + [CHK_PLACAR] + p['chk'][3:]
            p['grp'] = [[g[0], g[1] + (1 if g[1] >= 3 else 0), g[2] + 1] for g in p['grp']]
    return p


# ───────────── 1. feed (Instagram) ─────────────
feed_plan, ag, sobra_pool, sobras = PL.montar_feed()
assert not sobras, sobras
extra_plan, tt_sobra, st_sobra = PL.montar_resto(feed_plan, ag)
feed, faltando = [], []
for (d, h), (pid0, fmt, cids, eixos, pac) in sorted(feed_plan.items()):
    pid = RENOMEIA.get(pid0, pid0)
    if pid in C['PECAS']:
        p = nova(pid, C['PECAS'][pid])
    elif pid in futuro_v5:
        p = json.loads(json.dumps(futuro_v5[pid]))
    elif d <= HOJE and pid in P:
        continue
    elif os.environ.get('V6_STUB'):
        p = nova(pid, dict(fmt=fmt, titulo='[stub] ' + pid, gancho='stub', prod='dec'))
    else:
        faltando.append(pid)
        continue
    if pid in C['REVISOES']:
        revisar(p, C['REVISOES'][pid])
    p['pend'] = [x for x in p.get('pend', []) if x != SEM_CUSTO]
    p['d'], p['hora'], p['cid'], p['eixos'], p['pac'] = d, h, cids, eixos.split(), RENOMEIA.get(pac, pac)
    p['video'] = ' + '.join(NOME[c] for c in cids) if cids else 'Vários destinos'
    if cids and not p.get('vk'):
        p['vk'] = cids[0]
    p['v6'] = True
    feed.append(p)
assert not faltando, 'sem conteúdo: %s' % faltando
FEED = {p['id']: p for p in feed}
nr = nc = 0
for p in sorted(feed, key=lambda x: (x['d'], x['hora'])):
    if p['fmt'] == 'Reel':
        nr += 1
        p['code'] = 'Reel %02d · %s · Nível %s' % (nr, p['pilar'], p.get('nivel', 'B'))
    else:
        nc += 1
        p['code'] = 'Carrossel %02d · %s' % (nc, p['pilar'])

# ───────────── 2. vídeos longos: datas intactas, requisitos de Placar e resumo ─────────────
VLOG_DE = {vid: (d, c) for d, (vid, c) in PL.VLOGS.items()}
LANC = defaultdict(dict)
for p in feed:
    if p.get('video_longo') and p.get('tipo'):
        LANC[p['video_longo']][p['tipo']] = p
for p in longos:
    d0 = (p['d'], p['hora'], p['titulo'])
    c = p['vk']
    p['cid'] = [c]
    p['pend'] = [x for x in p.get('pend', []) if x not in PEND_VLOG_V5]
    lan = LANC.get(p['id'], {})
    req = ['PLACAR no vídeo longo (DS V2, 2.5; no 16:9, Placar em x 96 · y 72): aguardando dados de custos do Diego — hora de chegada e cada gasto do dia com a hora. Coerente com o Placar do Reel “Primeiro dia”.',
           'RESUMO DE GASTOS no encerramento: gasto de cada dia, total do episódio (cidade e período) e total da viagem de março sem passagens aéreas, separados. Aguardando dados de custos do Diego. Não misturar com outras viagens.',
           'Lançamento v6: trailer %s · Primeiro dia %s · teaser %s.' % tuple(
               ('%s (%s)' % (lan[t]['id'], lan[t]['d'][8:] + '/' + lan[t]['d'][5:7])) if t in lan else 'não se aplica' for t in ('trailer', 'serie', 'teaser'))]
    if p['d'] <= HOJE:
        req.insert(0, 'Publicação sem evidência registrada no painel. Se já saiu, o vídeo publicado não é alterado: o Placar e o resumo ficam como pendência para a próxima versão; se não saiu, aplicar antes de publicar.')
    p['pend'] = req + [x for x in p['pend'] if x not in req]
    p['cus'] = dict(dados=['Hora de chegada e cada gasto de cada dia, com a hora (para o Placar)', 'Total de cada dia e total do episódio', 'Total da viagem de março sem passagens aéreas', 'Escopo: por pessoa ou por casal; cotação e data'],
                    escopo='Vídeo longo de ' + NOME[c], quando='na produção da edição')
    p['pac'] = 'pac:' + p['d'] + ':' + c
    assert (p['d'], p['hora'], p['titulo']) == d0
for p in lanc_st:
    p['cid'] = [p['vk']]
    p['pac'] = 'pac:' + p['d'] + ':' + p['vk']

# ───────────── 3. Shorts (YouTube) e TikTok ─────────────
v5_short = {s.get('src'): s['id'] for s in futuro_v5.values() if s.get('kind') == 'short_reuse' and s.get('src')}
VL_DATAS = sorted(PL.VLOGS)
TEASER_SEM = {PL.semana(p['d']) for p in feed if p.get('tipo') == 'teaser'}
VLOG_SEM = {PL.semana(d) for d in PL.VLOGS}
CAP = {x[0]: x for x in extra_plan if x[2] == 'SH-CAP'}
CHK_SHORT = ['Exportar do projeto do Reel, sem marca d\'água', 'Título do YouTube (até 60 caracteres)', 'Trocar o CTA final do Instagram por “segue o canal”',
             'Cena mais forte no primeiro segundo', 'Funciona sem som', 'Publicar', 'Registrar as métricas em 48 horas']
CHK_TT = ['Conferir as pendências da peça de origem', 'Exportar sem marca d\'água de outro app', 'Trocar o texto do gancho pelo do TikTok',
          'Áudio: só som original ou som conferido na Central de Criadores do TikTok no dia (não usar tendência sem conferir)',
          'Legenda curta com 3 a 5 palavras de busca', 'Publicar', 'Responder os comentários na primeira hora', 'Registrar as métricas em 48 horas']
seq_s = [max([int(i[1:]) for i in P if re.fullmatch(r'p9\d\d', i)] + [899])]


def novo_id_short(src):
    if src in v5_short:
        return v5_short[src]
    seq_s[0] += 1
    return 'p%d' % seq_s[0]


def short_de(p, titulo=None, muda=None):
    ya = C['YT_ADAPT'].get(p['id']) or (C['PECAS'].get(p['id'], {}) or {}).get('yt') or {}
    t = (titulo or ya.get('titulo') or p['titulo'])[:60]
    sid = novo_id_short(p['id'])
    return {
        'd': p['d'], 'hora': '20:30', 'plat': 'YouTube', 'fmt': 'Short', 'pilar': 'YouTube (complementar)', 'video': p['video'],
        'titulo': 'Short: ' + t, 'gancho': p.get('gancho', '—'),
        'como': 'Mesmo pacote do %s de %s (%s). %s' % (p['fmt'], p['d'][8:] + '/' + p['d'][5:7], p['titulo'], muda or ya.get('muda') or 'Mesmo corte; CTA final trocado por “segue o canal pra ver a próxima cidade”.'),
        'leg': p.get('leg', '').split('\n')[0] + '\n\nPrimeiro Dia: o primeiro dia de cada cidade, do jeito que foi. #shorts',
        'cta': 'Inscrever-se no canal (comentário fixado com a pergunta).', 'met': 'Visualizações e % que assiste em vez de deslizar',
        'kind': 'short_reuse', 'vk': p.get('vk'), 'code': '', 'id': sid, 'obj': 'Descoberta no YouTube a partir de uma peça que se entende sem conhecer o perfil.' + (' Leva ao vídeo longo (link do vídeo relacionado).' if p.get('video_longo') else ''),
        'sc': [], 'sl': [], 'mat': ['Projeto da peça de origem (%s): %s' % (p['id'], '; '.join(p.get('mat', [])[:2]))],
        'chk': CHK_SHORT[:1] + ['Título: ' + t] + CHK_SHORT[2:], 'grp': [['Produção', 0, 3], ['Pré-publicação', 3, 5], ['Publicação', 5, 7]],
        'obs': ['Pacote editorial de %s: mesma peça, mesmo dia, conta como 1 aparição da cidade.' % p['id'], 'Origem: ' + p['titulo'] + '.'],
        'orig': {'fonte': 'Peça %s' % p['id'], 'trecho': (p.get('orig') or {}).get('trecho'), 'dica': ''},
        'cid': p['cid'], 'src': p['id'], 'pac': p['pac'], 'v6': True, 'pend': ['Ver as pendências da peça de origem (%s)' % p['id']],
        'trecho': (p.get('orig') or {}).get('trecho'), 'video_longo': p.get('video_longo'),
    }


def tiktok_de(p):
    ta = C['TT_ADAPT'].get(p['id']) or (C['PECAS'].get(p['id'], {}) or {}).get('tt') or {}
    return {
        'd': p['d'], 'hora': '21:00', 'plat': 'TikTok', 'fmt': 'TikTok', 'pilar': p['pilar'], 'pl': p.get('pl'), 'video': p['video'],
        'titulo': 'TikTok: ' + p['titulo'], 'gancho': ta.get('gancho') or p.get('gancho', '—'),
        'como': 'Mesmo pacote do Reel de %s. Adaptação: %s' % (p['d'][8:] + '/' + p['d'][5:7], ta.get('muda') or 'mesma edição; gancho escrito maior no 1º segundo, legenda curta com palavras de busca e pergunta para os comentários.'),
        'leg': p.get('leg', '').split('\n')[0], 'cta': 'Comentário com a pergunta do vídeo.', 'met': 'Retenção média e compartilhamentos',
        'kind': 'tiktok', 'vk': p.get('vk'), 'code': '', 'id': 'tk' + p['id'], 'obj': 'Alcance no TikTok com a mesma peça criativa, adaptada à plataforma.',
        'sc': [], 'sl': [], 'mat': ['Projeto do Reel de origem (%s)' % p['id']], 'chk': CHK_TT, 'grp': [['Produção', 0, 3], ['Pré-publicação', 3, 5], ['Publicação', 5, 8]],
        'obs': ['Pacote editorial de %s: mesma peça, mesmo dia, conta como 1 aparição da cidade.' % p['id']],
        'orig': {'fonte': 'Reel %s' % p['id'], 'trecho': (p.get('orig') or {}).get('trecho'), 'dica': ''},
        'cid': p['cid'], 'src': p['id'], 'pac': p['pac'], 'v6': True, 'pend': ['Ver as pendências do Reel de origem (%s)' % p['id']], 'pilar_tt': p['pilar'],
    }


shorts, tiktoks = [], []
for p in sorted(feed, key=lambda x: (x['d'], x['hora'])):
    if p['fmt'] != 'Reel':
        continue
    s, wd = PL.semana(p['d']), dt.date.fromisoformat(p['d']).weekday()
    if s in VLOG_SEM:
        sh = p.get('tipo') in ('trailer', 'serie')
        tk = sh
    elif s in TEASER_SEM:
        sh = p.get('tipo') == 'teaser' or (wd == 6 and not any(PL.semana(x[0]) == s for x in CAP.values()))
        tk = p.get('tipo') == 'teaser' or wd == 6
    else:
        sh = wd in (1, 5) and 'doc' not in p['eixos'] or (wd == 3 and p.get('tipo') == 'teaser')
        tk = wd in (1, 6)
    if p['d'] == '2026-10-17':
        sh = True
    if sh:
        shorts.append(short_de(p))
    if tk:
        tiktoks.append(tiktok_de(p))
# capítulos dos vlogs (Short independente) e TikTok próprios
for x in extra_plan:
    d, h, xid, plat, fmt, cids, eixos, conc, vid = x
    if xid == 'SH-CAP':
        c = cids[0]
        cap = C['SHORT_CAP'].get(c, {})
        seq_s[0] += 1
        sid = 'p%d' % seq_s[0]
        shorts.append({
            'd': d, 'hora': h, 'plat': 'YouTube', 'fmt': 'Short', 'pilar': 'YouTube (complementar)', 'video': NOME[c],
            'titulo': 'Short: ' + (cap.get('titulo') or 'Capítulo do vlog de ' + NOME[c])[:60], 'gancho': cap.get('gancho', '—'),
            'como': 'Short próprio: um capítulo do vlog de %s (%s), cortado do vídeo longo e diferente do teaser. %s' % (NOME[c], vid, cap.get('estrutura', '')),
            'leg': (cap.get('titulo') or '') + '\n\nVídeo completo no canal. #shorts', 'cta': 'Assistir ao vídeo completo (link do vídeo relacionado).',
            'met': 'Visualizações e cliques para o vídeo longo', 'kind': 'short_cap', 'vk': c, 'code': '', 'id': sid,
            'obj': 'Levar quem chega pelo Shorts ao vídeo longo, com uma cena que funciona sozinha.', 'sc': [], 'sl': [],
            'mat': cap.get('mat', ['Vlog de %s (%s)' % (NOME[c], vid)]), 'chk': CHK_SHORT, 'grp': [['Produção', 0, 3], ['Pré-publicação', 3, 5], ['Publicação', 5, 7]],
            'obs': ['Conta como aparição própria de %s (não é pacote de outra peça).' % NOME[c]],
            'orig': {'fonte': 'Vídeo longo ' + vid, 'trecho': cap.get('trecho'), 'dica': ''},
            'cid': [c], 'src': vid, 'pac': 'cap:' + c, 'v6': True, 'pend': cap.get('pend', ['Escrever o corte (conteúdo não recebido)']),
            'trecho': cap.get('trecho'), 'video_longo': vid,
        })
    elif plat == 'TikTok':
        t = C['TIKTOK'].get(xid, {})
        tiktoks.append({
            'd': d, 'hora': h, 'plat': 'TikTok', 'fmt': 'TikTok', 'pilar': 'Como foi de verdade', 'pl': 'EXP', 'video': NOME[cids[0]],
            'titulo': 'TikTok: ' + t.get('titulo', conc), 'gancho': t.get('gancho', '—'),
            'como': 'TikTok próprio (não é cópia do Instagram). ' + t.get('conceito', conc),
            'leg': t.get('legenda', ''), 'cta': 'Comentário.', 'met': t.get('met', 'Retenção média e compartilhamentos'),
            'kind': 'tiktok', 'vk': cids[0], 'code': '', 'id': xid, 'obj': t.get('obj', ''),
            'sc': sc_dicts([(a, 'Cena', b) for a, b in t.get('estrutura', [])]), 'sl': [], 'mat': t.get('mat', []),
            'chk': CHK_TT, 'grp': [['Produção', 0, 3], ['Pré-publicação', 3, 5], ['Publicação', 5, 8]],
            'obs': ['Ideia própria do TikTok: conta como aparição de %s.' % NOME[cids[0]]],
            'orig': {'fonte': 'Acervo · ' + NOME[cids[0]], 'trecho': None, 'dica': ''},
            'cid': cids, 'pac': xid, 'v6': True, 'pend': t.get('pend', ['Conteúdo não recebido: escrever a peça']), 'eixos': eixos.split(), 'prod': t.get('prod', 'dec'),
        })
for i, s in enumerate(sorted(shorts, key=lambda x: x['d'])):
    s['code'] = 'Short %02d' % (i + 1)
for i, t in enumerate(sorted(tiktoks, key=lambda x: x['d'])):
    t['code'] = 'TikTok %02d' % (i + 1)

# ───────────── 4. Stories (dia a dia) ─────────────
SQ = {x[0]: x for x in extra_plan if x[3] == 'Instagram' and x[4] == 'Stories'}
REL = ['Enquete “Qual cidade você quer ver primeiro aqui?” (sem imagem de cidade: fundo de papel do DS)',
       'Caixinha “Qual sua maior dúvida pra montar uma viagem?” (as respostas viram pauta de “Antes de ir”)',
       'Quiz de viagem sem cidade central (pergunta geral de planejamento) + resposta no dia seguinte',
       'Enquete “Você viaja com roteiro fechado ou improvisa?”',
       'Caixinha “Qual foi o seu primeiro dia mais marcante?” (repostar 3 respostas, com autorização)']
stories_dia = {}
por_dia = defaultdict(list)
for p in feed + longos + lanc_st:
    if p['d'] >= INI:
        por_dia[p['d']].append(p)
for i, d in enumerate(PL.dias(INI, FIM)):
    wd = dt.date.fromisoformat(d).weekday()
    ps = [p for p in por_dia.get(d, []) if p['kind'] in ('v3_reel', 'v3_car')]
    if d in PL.VLOGS:
        vid, c = PL.VLOGS[d]
        stories_dia[d] = {'t': 'Lançamento do vlog de %s' % NOME[c], 'cid': [c], 'pac': 'pac:%s:%s' % (d, c),
                          'steps': ['Sequência de lançamento do vídeo longo (post %s): 5 telas, do jeito registrado no painel.' % next((p['id'] for p in lanc_st if p['d'] == d), '—'),
                                    'Tela extra · noite: enquete “Você já assistiu?” + link do vídeo. Mesmo pacote do vlog e do Reel “Primeiro dia”.']}
    elif ps:
        p = ps[0]
        mat0 = (p.get('mat') or ['arquivo da peça'])[0]
        q = 'caixinha de perguntas sobre o tema' if set(p.get('eixos', [])) & {'cus', 'doc', 'loc', 'rot'} else 'enquete ou slider sobre o momento'
        stories_dia[d] = {'t': 'Repercussão: ' + p['titulo'], 'cid': p['cid'], 'pac': p['pac'],
                          'steps': ['Tela 1 · %s · o post do dia com 1 frase que não está nele (arquivo: %s)' % (p['hora'], mat0),
                                    'Tela 2 · bastidor real do mesmo dia: um plano vizinho que não entrou no corte (mesma pasta, ver mat da peça); nada gravado agora',
                                    'Tela 3 · %s' % q,
                                    'Métrica: respostas ÷ alcance e saídas na tela 1. Mesmo pacote da peça: não conta como nova aparição da cidade.']}
    elif d in SQ:
        x = SQ[d]
        st = C['STORIES'].get(x[2], {})
        stories_dia[d] = {'t': st.get('t', x[7]), 'cid': x[5], 'pac': x[2],
                          'steps': list(st.get('telas', [x[7]])) + ['Objetivo: ' + st.get('obj', 'relacionamento e desejo pela cidade') + '. Sequência própria: conta como aparição de ' + NOME[x[5][0]] + '.']}
    elif wd == 0:
        stories_dia[d] = {'t': 'Relacionamento (sem cidade)', 'cid': [], 'pac': None,
                          'steps': ['Tela 1 · ' + REL[i % len(REL)], 'Tela 2 · resposta ou bastidor de planejamento do perfil (sem cidade central)', 'Métrica: respostas ÷ alcance.']}
    elif wd == 4:
        stories_dia[d] = ({'t': 'Sem Stories', 'cid': [], 'pac': None, 'steps': ['Dia sem Stories de propósito (sexta de produção; o TikTok próprio sai às 19h).']}
                          if (i // 7) % 2 else
                          {'t': 'Pergunta de sexta (sem cidade)', 'cid': [], 'pac': None, 'steps': ['Tela 1 · caixinha “O que você quer ver no fim de semana?”', 'Métrica: respostas ÷ alcance.']})
    else:
        stories_dia[d] = {'t': 'Sem Stories', 'cid': [], 'pac': None, 'steps': ['Dia sem Stories: nada a repercutir.']}

# ───────────── 5. auditoria de cidades (todas as plataformas) ─────────────
ap = defaultdict(lambda: defaultdict(set))   # cidade -> data -> {(pacote, rótulo)}
linhas = []


def reg(d, cids, pac, rot):
    for c in cids:
        ap[c][d].add((pac, rot))
        linhas.append((d, c, rot, pac))


for p in feed:
    if p['d'] >= INI:
        reg(p['d'], p['cid'], p['pac'], '%s %s (%s)' % (p['fmt'], p['id'], p['titulo'][:40]))
for p in longos:
    if p['d'] >= INI:
        reg(p['d'], p['cid'], p['pac'], 'Vídeo longo %s' % p['id'])
for s in shorts:
    reg(s['d'], s['cid'], s['pac'], 'Short %s' % s['id'])
for t in tiktoks:
    reg(t['d'], t['cid'], t['pac'], 'TikTok %s' % t['id'])
for d, st in stories_dia.items():
    if st.get('cid'):
        reg(d, st['cid'], st['pac'], 'Stories (%s)' % st['t'][:30])
viol = []
for c, dd in ap.items():
    for d, s in dd.items():
        if len({x[0] for x in s}) > 1:
            viol.append('%s: %s tem %d pacotes no mesmo dia' % (NOME[c], d, len({x[0] for x in s})))
        x = dt.date.fromisoformat(d)
        if (x + dt.timedelta(days=1)).isoformat() in dd:
            viol.append('%s: dias seguidos %s e %s' % (NOME[c], d, (x + dt.timedelta(days=1)).isoformat()))
    sem = Counter(PL.semana(d) for d in dd)
    for s, n in sem.items():
        if n > 2:
            viol.append('%s: %d dias na semana de %s' % (NOME[c], n, s))
# transição com o histórico (15/10 e antes)
for p in hist:
    for c in ([p['vk']] if p.get('vk') in NOME else []):
        if p['d'] == HOJE and '2026-10-16' in ap.get(c, {}):
            viol.append('%s: 15/10 (histórico) e 16/10' % NOME[c])

# ───────────── 6. semanas ─────────────
sem_old = {w['start']: w for w in D['weeks']}
semanas = [w for w in D['weeks'] if w['end'] < '2026-10-12']
todos = hist + feed + longos + lanc_st + shorts + tiktoks
by_day = defaultdict(list)
for p in todos:
    by_day[p['d']].append(p['id'])
x = dt.date(2026, 10, 12)
n = len(semanas)
while x.isoformat() <= FIM:
    s, e = x.isoformat(), (x + dt.timedelta(days=6)).isoformat()
    ps = [p for p in feed if s <= p['d'] <= e]
    vl = [p for p in longos if s <= p['d'] <= e]
    tag = ('Vlog de ' + NOME[vl[0]['vk']]) if vl else (('Teaser de ' + NOME[next(p for p in ps if p.get('tipo') == 'teaser')['cid'][0]]) if any(p.get('tipo') == 'teaser' for p in ps) else 'Acervo')
    eix = Counter(e2 for p in ps for e2 in p.get('eixos', []))
    days = []
    for d in PL.dias(s, e):
        if d <= HOJE:
            old = next((dd for w in D['weeks'] for dd in w['days'] if dd['date'] == d), None)
            if old:
                days.append(old)
                continue
        inter = ['Instagram: responder todos os comentários em até 60 minutos depois de postar.'] if any(p['plat'] == 'Instagram' and p['d'] == d for p in feed) else ['10 min: comentar de verdade em 5 perfis de viagem.']
        if any(t['d'] == d for t in tiktoks):
            inter.append('TikTok: responder os comentários na primeira hora.')
        days.append({'date': d, 'posts': sorted(set(by_day.get(d, [])), key=lambda i: next((q['hora'] for q in todos if q['id'] == i), '')),
                     'stories': {k: v for k, v in stories_dia.get(d, {'t': 'Sem Stories', 'steps': [], 'cid': []}).items() if k != 'pac'}, 'inter': inter})
    old = sem_old.get(s, {})
    semanas.append({'n': n, 'trip': False, 'start': s, 'end': e,
                    'obj': '; '.join('%s %s' % (p['d'][8:] + '/' + p['d'][5:7], p['titulo']) for p in sorted(ps, key=lambda q: q['d'])),
                    'metas': ['%d Reels + %d carrossel · %d Shorts · %d TikToks' % (sum(p['fmt'] == 'Reel' for p in ps), sum(p['fmt'] == 'Carrossel' for p in ps),
                                                                                  sum(s <= q['d'] <= e for q in shorts), sum(s <= q['d'] <= e for q in tiktoks)),
                              'Eixos: ' + ', '.join('%s %d' % (PL.EIXOS[k], v) for k, v in eix.most_common()),
                              'Regra de cidades: auditada em todas as plataformas (AUDITORIA_CIDADES_V6.md)'],
                    'observe': ['%s: %s' % (p['titulo'], p.get('met', '')) for p in ps[:4]],
                    'tag': tag, 'pergunta': old.get('pergunta'), 'days': days})
    n += 1
    x += dt.timedelta(days=7)
D['weeks'] = semanas

# ───────────── 7. dados gerais ─────────────
saem = {}
for pid, p in futuro_v5.items():
    if p['kind'] in ('v3_reel', 'v3_car') and pid not in FEED:
        saem[pid] = None
MOTIVOS = {
    'p211': 'Reel sem texto (T2, B) cedeu a vaga aos lançamentos do YouTube; o T2 foi rebalanceado com p840 e p230 (A).',
    'p239': 'Reel sem texto de Barcelona (T2, B): Barcelona tinha excesso de peças e o T2 estava desequilibrado.',
    'p604': 'Barcelona tinha excesso de peças; a vaga foi para custos, locomoção e preparação (banco de ideias).',
    'p613': 'Bruxelas ganhou trailer, teaser e locomoção (metrô até o Atomium); a peça das Galerias vai para o banco.',
    'p276': 'A vaga de 19/01 é do teaser de Lisboa; Bruges ganhou trailer e teaser.',
    'p267': 'Repetia o p244 (Madrid em 2 dias); vaga para custos e locomoção.',
    'p610': 'Bruges ganhou trailer, teaser e capítulo; os cisnes vão para o banco.',
    'p602': 'Amsterdam ganhou trailer, teaser, custos e locomoção; o stroopwafel vai para o banco.',
    'p228': 'Repetia o p624 (Disney: o dia pelo relógio).',
    'p626': 'Barcelona tinha excesso de peças; o carrossel do Bairro Gótico vai para o banco.',
}
for pid in JAN:
    if pid in futuro_v5:
        MOTIVOS[pid] = 'Dependia da viagem de janeiro, que saiu desta revisão por decisão do Diego (15/10). Nada foi reservado para ela.'
D['saem_v6'] = [{'id': k, 'titulo': futuro_v5[k]['titulo'], 'motivo': MOTIVOS.get(k, 'Substituída no calendário v6 (ver CHANGELOG_v6.md).')}
                for k in sorted(set(MOTIVOS) | set(saem)) if k in futuro_v5 and futuro_v5[k]['kind'] not in ('short_reuse',)]
NOVAS_PEND = [
    {'k': 60, 't': 'Custos: as peças de custo, os Placares dos Reels “Primeiro dia” e o resumo final dos vlogs estão como “Aguardando dados de custos do Diego”. Cada peça lista os dados necessários; os valores são pedidos na produção de cada uma', 'type': 'text'},
    {'k': 61, 't': 'Vlog de Amsterdam: o painel registra 24/10 (sábado). Se “este sábado” era 17/10, confirmar: a data foi mantida como estava registrada', 'type': 'text'},
    {'k': 62, 't': 'Vlog de Barcelona (10/10): sem evidência de publicação no painel. Confirmar se saiu (o Placar e o resumo só entram se ainda não saiu)', 'type': 'text'},
    {'k': 63, 'type': 'text', 't': 'Itália: em Veneza e Roma aparecem familiares (viagem em família, 5 pessoas). Confirmar quem pode aparecer nas peças com vídeo da Itália'},
    {'k': 64, 'type': 'text', 't': 'Documentação e preparação (p830, p831, p832): conferir as regras na fonte oficial no dia da produção (o ETIAS não estava em operação em 15/10/2026, segundo o site oficial citado por Connexion)'},
    {'k': 65, 'type': 'text', 't': 'TikTok: confirmar o perfil (@primeirodiaem?) e se o Diego vai publicar a partir de 16/10; o painel planeja 3 TikToks por semana'},
]
D['pend'] = [x for x in D['pend'] if x['k'] not in (36, 41, 53, 54, 55)] + NOVAS_PEND
D['posts'] = hist + sorted([p for p in feed + longos + lanc_st + shorts + tiktoks if p['d'] > HOJE] + [p for p in feed if p['d'] <= HOJE and p['id'] not in {q['id'] for q in hist}],
                           key=lambda p: (p['d'], p['hora']))
ids = [p['id'] for p in D['posts']]
dups = [k for k, v in Counter(ids).items() if v > 1]
assert not dups, dups

# ───────────── 8. relatórios ─────────────
def fmt_d(d):
    x = dt.date.fromisoformat(d)
    return '%s %s' % (d[8:] + '/' + d[5:7] + '/' + d[:4], ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'][x.weekday()])


A = ['# Auditoria de cidades · v6 (gerada por scripts/aplicar_v6.py)', '',
     'Regra (CLAUDE.md, 7): cada cidade aparece no máximo **2 dias por semana** (seg a dom) e **nunca em dias seguidos**, inclusive na virada de semana e de mês. Contam Reels, carrosséis, Stories próprios, Shorts, TikToks, vídeos longos, trailers e teasers. Peças do **mesmo pacote** (mesma peça criativa no mesmo dia em várias plataformas, e a repercussão dela nos Stories) contam **1** aparição; peças diferentes da mesma cidade contam separado.', '',
     'Período: %s a %s. **Violações: %d.**' % (fmt_d(INI), fmt_d(FIM), len(viol)), '']
A += ['- ' + v for v in viol] or ['Nenhuma violação.']
A += ['', '## Validação semanal', '', '| Semana | Cidade | Dias (pacote) | Formatos | Dias na semana | Dias seguidos | Resultado |', '|---|---|---|---|---:|---|---|']
for c in sorted(ap, key=lambda k: NOME[k]):
    sem = defaultdict(list)
    for d in sorted(ap[c]):
        sem[PL.semana(d)].append(d)
    for s, ds in sorted(sem.items()):
        cons = any((dt.date.fromisoformat(a) + dt.timedelta(days=1)).isoformat() in ap[c] for a in ds)
        rot = '; '.join('%s: %s' % (d[8:] + '/' + d[5:7], ', '.join(sorted({r for _, r in ap[c][d]}))[:160]) for d in ds)
        A.append('| %s | %s | %s | %s | %d | %s | %s |' % (s[8:] + '/' + s[5:7], NOME[c], ' · '.join(d[8:] + '/' + d[5:7] for d in ds), rot.replace('|', '/'),
                                                       len(ds), 'sim' if cons else 'não', 'OK' if len(ds) <= 2 and not cons else 'VIOLAÇÃO'))
A += ['', '## Sequência diária (todas as plataformas)', '', '| Data | Cidade | Item | Pacote |', '|---|---|---|---|']
for d, c, rot, pac in sorted(linhas):
    A.append('| %s | %s | %s | %s |' % (fmt_d(d), NOME[c], rot.replace('|', '/'), pac))
open(os.path.join(RAIZ, 'AUDITORIA_CIDADES_V6.md'), 'w', encoding='utf-8').write('\n'.join(A) + '\n')

L = ['# Auditoria dos lançamentos do YouTube · v6', '',
     'Datas dos vídeos longos conferidas contra o painel v5 (cópia em `versoes/`). Os valores de custo **não** estão no painel: o Placar e o resumo final dependem dos dados que o Diego fornece na produção (adendo de 15/10).', '',
     '| Vídeo longo | Data (preservada) | Trailer | Primeiro dia (Placar) | Teaser | Capítulo (Short) | Placar no Reel | Placar no vídeo longo | Resumo por dia e total sem aéreo | Dados de custo |', '|---|---|---|---|---|---|---|---|---|---|']
base_long = {p['id']: p for p in json.loads(m.group(1))['posts'] if p['kind'] == 'long'}
for p in sorted(longos, key=lambda q: q['d']):
    lan = LANC.get(p['id'], {})
    cap = next((s for s in shorts if s.get('kind') == 'short_cap' and s.get('src') == p['id']), None)
    ser = lan.get('serie')
    ok_d = 'sim' if (base_long[p['id']]['d'], base_long[p['id']]['hora']) == (p['d'], p['hora']) else 'NÃO'
    f = lambda q: '%s · %s' % (q['id'], q['d'][8:] + '/' + q['d'][5:7]) if q else '—'
    L.append('| %s (%s) | %s %s · %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        p['titulo'], p['id'], fmt_d(p['d']), p['hora'], ok_d, f(lan.get('trailer')) if lan.get('trailer') else ('não se aplica (vlog já passou)' if p['d'] <= HOJE else 'FALTA'),
        f(ser), f(lan.get('teaser')), f(cap), ('previsto (dados pendentes)' if ser and CHK_PLACAR in ser['chk'] else 'FALTA'),
        'previsto (pendência no post)', 'previsto (pendência no post)', 'Aguardando dados de custos do Diego'))
L += ['', 'Notas:', '- Barcelona (p13, 10/10): vídeo anterior a esta revisão, sem evidência de publicação. Trailer não se aplica; teaser = p265 (corte do master); Primeiro dia = p300 com Placar.',
      '- Paris, Disney e Madrid: não houve vaga para um Short-capítulo sem quebrar a regra de cidades; o teaser cumpre o papel de corte do vídeo longo.',
      '- Os Reels “Primeiro dia” sem vlog (Veneza p302, Florença p301, Roma p254) não pedem Placar pela regra; o p254 tem a dependência de custos registrada.']
open(os.path.join(RAIZ, 'AUDITORIA_LANCAMENTOS_V6.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# equilíbrio
fut_feed = [p for p in feed if p['d'] >= INI]
E = ['# Equilíbrio editorial · v6', '', 'Contagem das peças de %s a %s (gerada por scripts/aplicar_v6.py). Uma peça pode ter mais de um eixo.' % (fmt_d(INI), fmt_d(FIM)), '',
     '## Por plataforma e formato', '', '| Plataforma | Formato | Peças |', '|---|---|---:|']
cnt = Counter((p['plat'], p['fmt']) for p in fut_feed + shorts + tiktoks + [q for q in longos if q['d'] >= INI])
for (pl, fm), v in sorted(cnt.items()):
    E.append('| %s | %s | %d |' % (pl, fm, v))
E.append('| Instagram | Stories (dias com sequência) | %d de %d dias |' % (sum(1 for st in stories_dia.values() if st['t'] != 'Sem Stories'), len(stories_dia)))
E += ['', '## Por eixo editorial (feed do Instagram)', '', '| Eixo | Peças | % do feed |', '|---|---:|---:|']
ce = Counter(e2 for p in fut_feed for e2 in p.get('eixos', []))
for k, v in ce.most_common():
    E.append('| %s | %d | %.0f%% |' % (PL.EIXOS[k], v, 100 * v / len(fut_feed)))
E += ['', '## Por pilar do painel', '', '| Pilar | Peças |', '|---|---:|']
for k, v in Counter(p['pilar'] for p in fut_feed).most_common():
    E.append('| %s | %d |' % (k, v))
E += ['', '## Por cidade (feed)', '', '| Cidade | Peças |', '|---|---:|']
for k, v in Counter(c for p in fut_feed for c in (p['cid'] or ['multi'])).most_common():
    E.append('| %s | %d |' % (NOME.get(k, 'Várias'), v))
E += ['', '## Semana a semana (eixos do feed)', '', '| Semana | Peças | Eixos | Alerta |', '|---|---|---|---|']
for w in semanas:
    if w['end'] < INI:
        continue
    ps = [p for p in fut_feed if w['start'] <= p['d'] <= w['end']]
    ex = Counter(e2 for p in ps for e2 in p.get('eixos', []))
    top = ex.most_common(1)
    al = ('concentração de %s' % PL.EIXOS[top[0][0]]) if top and top[0][1] >= 4 and top[0][0] not in ('lan',) else ''
    E.append('| %s | %s | %s | %s |' % (w['start'][8:] + '/' + w['start'][5:7], ' · '.join(p['id'] for p in ps), ', '.join('%s %d' % (k, v) for k, v in ex.most_common()), al))
open(os.path.join(RAIZ, 'EQUILIBRIO_EDITORIAL_V6.md'), 'w', encoding='utf-8').write('\n'.join(E) + '\n')

# calendário completo
K = ['# Calendário editorial v6 · %s a %s' % (fmt_d(INI), fmt_d(FIM)), '',
     'Gerado por `scripts/aplicar_v6.py` a partir do painel. Detalhes de cada peça (cenas, slides, legenda, checklist, pendências) no painel: `planejamento-postagens.html#/post/<id>`.', '',
     '| Data | Hora | Plataforma | Formato | Cidade | Pilar · eixos | ID | Peça | Arquivos de origem | Status |', '|---|---|---|---|---|---|---|---|---|---|']
for p in sorted([q for q in feed + longos + shorts + tiktoks if q['d'] >= INI], key=lambda q: (q['d'], q['hora'])):
    K.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        fmt_d(p['d']), p['hora'], p['plat'], p['fmt'], ', '.join(NOME.get(c, c) for c in p.get('cid', [])) or 'Várias',
        (p.get('pilar', '') + (' · ' + ', '.join(p.get('eixos', [])) if p.get('eixos') else '')), p['id'], p['titulo'].replace('|', '/'),
        '; '.join(p.get('mat', [])[:2]).replace('|', '/')[:180], D['stmat'].get(p.get('prod', ''), 'ver peça de origem' if p.get('src') else '—')))
K += ['', '## Stories (dia a dia)', '', '| Data | Sequência | Cidade | Telas |', '|---|---|---|---|']
for d in sorted(stories_dia):
    st = stories_dia[d]
    K.append('| %s | %s | %s | %s |' % (fmt_d(d), st['t'], ', '.join(NOME[c] for c in st.get('cid', [])) or '—', ' / '.join(st['steps']).replace('|', '/')[:400]))
open(os.path.join(RAIZ, 'CALENDARIO_V6.md'), 'w', encoding='utf-8').write('\n'.join(K) + '\n')

print('feed:', Counter(p['fmt'] for p in fut_feed), '| shorts:', len(shorts), '| tiktok:', len(tiktoks), '| stories:', sum(1 for s in stories_dia.values() if s['t'] != 'Sem Stories'))
print('eixos:', dict(ce))
print('ganchos >7 palavras:', [p['id'] for p in fut_feed if p.get('gancho') and p['gancho'] not in ('—',) and not p['gancho'].startswith('(') and len(p['gancho'].split()) > 7])
print('TikTok sem conteúdo:', [t['id'] for t in tiktoks if t['kind'] == 'tiktok' and not t.get('src') and t['id'] not in C['TIKTOK']])
print('Stories sem conteúdo:', [x[2] for x in SQ.values() if x[2] not in C['STORIES']], '| capítulos sem conteúdo:', [c for c in (x[5][0] for x in CAP.values()) if c not in C['SHORT_CAP']])
print('violações:', len(viol))
for v in viol[:20]:
    print('  ', v)
if viol:
    sys.exit('Painel NÃO gravado: há violação da regra de cidades.')

out = html[:m.start(1)] + json.dumps(D, ensure_ascii=False) + html[m.end(1):]
# TikTok no painel (rótulo, ícone, filtro) e os novos pilares e status
out = out.replace("const platLabel=p=>p.fmt==='Short'?'YouTube Shorts':",
                  "const platLabel=p=>p.plat==='TikTok'?'TikTok':p.fmt==='Short'?'YouTube Shorts':")
out = out.replace("const platCls=p=>p.plat==='Instagram'?'ig':(p.plat==='YouTube'?'yt':'');",
                  "const platCls=p=>p.plat==='Instagram'?'ig':(p.plat==='YouTube'?'yt':(p.plat==='TikTok'?'tt':''));")
out = out.replace("if(UI.plat==='yt'&&p.plat!=='YouTube') return false;",
                  "if(UI.plat==='yt'&&p.plat!=='YouTube') return false;   if(UI.plat==='tt'&&p.plat!=='TikTok') return false;")
out = out.replace('aria-pressed="\'+(UI.plat===\'yt\')+\'">YouTube</button>',
                  'aria-pressed="\'+(UI.plat===\'yt\')+\'">YouTube</button><button type="button" data-flt="plat" data-v="tt" aria-pressed="\'+(UI.plat===\'tt\')+\'">TikTok</button>')
out = out.replace("'Primeiro Dia (série)':'pil-s'}", "'Primeiro Dia (série)':'pil-s','Quanto custa':'pil-u','Como se mover':'pil-u','Antes de ir':'pil-u'}")
out = out.replace("{ok:'b-pub',dec:'b-warn',dad:'b-warn',fut:'b-info'}", "{ok:'b-pub',dec:'b-warn',dad:'b-warn',fut:'b-info',cus:'b-warn',ofc:'b-info'}")
out = out.replace("(p.plat==='YouTube'?ic('yt',15):ic('tool',15))", "(p.plat==='YouTube'?ic('yt',15):(p.plat==='TikTok'?ic('film',15):ic('tool',15)))")
out = out.replace('--yt:#B8433A;', '--yt:#B8433A;--tt:#1F7A75;').replace('--yt:#F09088;', '--yt:#F09088;--tt:#6CC5BE;')
out = out.replace('.ci.yt{background:var(--yt)}', '.ci.yt{background:var(--yt)}.plat.tt svg,.pi.tt{color:var(--tt)}.ci.tt svg{color:var(--tt)}.ci.tt{background:var(--tt)}', 1)
out = out.replace("' peças no plano v5'", "' peças no plano v6'").replace('painel de conteúdo (v5)', 'painel de conteúdo (v6)')
if os.environ.get('V6_STUB'):
    PAINEL = PAINEL.replace('.html', '_stub.html')
open(PAINEL, 'w', encoding='utf-8').write(out)
print('painel gravado:', PAINEL)
