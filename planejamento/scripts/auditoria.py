"""Auditoria do calendário editorial (cadência de Reels, cidades e países).

Uso: python3 auditoria.py <eventos.json> [--cenario-provavel]
Funciona com a V4 (campo `city` texto) e com a V5 (campo `cities` lista).
Regras (prompt de revisão, seção 10):
- >= 4 Reels de Instagram por semana (seg a dom); quinta e domingo com Reel.
- Cidade: até 2 aparições por semana e nunca em dias seguidos (todos os formatos).
  Pacote multiplataforma = 1 aparição. Stories de apoio no mesmo dia da peça = mesmo pacote.
- País: duas peças editoriais seguidas (ordem de data e hora) não podem ser do mesmo país.
  Peça geral ou panorama (4+ cidades de 3+ países) é neutra. Vídeo longo sem destino = pendente.
"""
import json, sys, datetime as dt
from collections import defaultdict

PAIS = {'Barcelona': 'Espanha', 'Madrid': 'Espanha', 'Lisboa': 'Portugal',
        'Amsterdam': 'Países Baixos', 'Bruxelas': 'Bélgica', 'Bruges': 'Bélgica',
        'Paris': 'França', 'Disneyland Paris': 'França', 'Roma': 'Itália',
        'Florença': 'Itália', 'Veneza': 'Itália', 'Milão': 'Itália'}
INICIO, FIM = dt.date(2026, 10, 12), dt.date(2027, 2, 28)


def d(s):
    return dt.date.fromisoformat(s)


def semana(s):
    x = d(s)
    return (x - dt.timedelta(days=x.weekday())).isoformat()


def cidades(e, provavel=False):
    if provavel and e.get('probableCity'):
        return [e['probableCity']]
    if 'cities' in e:
        return [c for c in e['cities'] if c != 'Várias']
    c = e.get('city', '')
    return [] if c in ('', 'Geral', 'Várias') else [c]


def eh_reel_ig(e):
    return e['format'] == 'Reel' and 'Instagram Reels' in (e.get('platforms') or ['Instagram Reels'])


def aparicoes(ev, provavel=False):
    """Lista de (cidade, data, id). Stories marcados como apoio (supportOf) não contam à parte."""
    out = []
    for e in ev:
        if e.get('supportOf') or e.get('removed'):
            continue
        cs = cidades(e, provavel)
        if len(cs) >= 4:  # panorama: neutro
            continue
        for c in cs:
            out.append((c, e['date'], e['id'], e['format']))
    return out


def auditar(ev, provavel=False):
    ev = [e for e in ev if not e.get('removed')]
    res = {'semanas': [], 'cidades': [], 'paises': [], 'violacoes': []}
    # Cadência
    w = INICIO
    while w <= FIM:
        k = w.isoformat()
        rs = sorted([e for e in ev if eh_reel_ig(e) and semana(e['date']) == k], key=lambda e: e['date'])
        dias = {d(e['date']).weekday() for e in rs}
        qui = w + dt.timedelta(days=3)
        ok_qui = 3 in dias or qui < dt.date(2026, 10, 15)
        ok_dom = 6 in dias
        st = 'CONFORME' if len(rs) >= 4 and ok_qui and ok_dom else 'CORRIGIR'
        res['semanas'].append({'semana': k, 'reels': len(rs), 'datas': [e['date'] for e in rs],
                               'ids': [e['id'] for e in rs], 'quinta': ok_qui, 'domingo': ok_dom, 'status': st})
        if st != 'CONFORME':
            res['violacoes'].append(f'Cadência {k}: {len(rs)} Reels, quinta={ok_qui}, domingo={ok_dom}')
        w += dt.timedelta(days=7)
    # Cidades
    ap = aparicoes(ev, provavel)
    porcid = defaultdict(list)
    for c, data, i, f in ap:
        porcid[c].append((data, i, f))
    for c, lst in sorted(porcid.items()):
        lst.sort()
        datas = sorted({x[0] for x in lst})
        porsem = defaultdict(set)
        for x in datas:
            porsem[semana(x)].add(x)
        for s, ds in sorted(porsem.items()):
            viol = []
            if len(ds) > 2:
                viol.append(f'{len(ds)} aparições')
            res['cidades'].append({'cidade': c, 'pais': PAIS.get(c, ''), 'semana': s, 'datas': sorted(ds),
                                   'ids': [x[1] for x in lst if semana(x[0]) == s],
                                   'formatos': [x[2] for x in lst if semana(x[0]) == s],
                                   'contagem': len(ds), 'violacao': '; '.join(viol)})
            if viol:
                res['violacoes'].append(f'Cidade {c} semana {s}: {"; ".join(viol)}')
        for a, b in zip(datas, datas[1:]):
            if (d(b) - d(a)).days == 1:
                res['violacoes'].append(f'Cidade {c} em dias seguidos: {a} e {b}')
                for row in res['cidades']:
                    if row['cidade'] == c and b in row['datas']:
                        row['violacao'] = (row['violacao'] + '; ' if row['violacao'] else '') + f'dias seguidos {a}/{b}'
        # mesma cidade 2x no mesmo dia em pacotes diferentes
        cont = defaultdict(int)
        for x in lst:
            cont[x[0]] += 1
        for data, n in cont.items():
            if n > 1:
                res['violacoes'].append(f'Cidade {c}: {n} peças independentes no mesmo dia {data}')
    # Países
    seq = sorted([e for e in ev if not e.get('supportOf')], key=lambda e: (e['date'], e.get('recommendedTime') or '23:59'))
    prev, prev_label, pend = {'Espanha'}, 'Barcelona (última publicação real)', False
    for e in seq:
        cs = cidades(e, provavel)
        longo_sem = e.get('anchor') and not cs
        ps = {PAIS[c] for c in cs if c in PAIS}
        if len(cs) >= 4 and len(ps) >= 3:  # panorama de vários países: neutro
            ps = set()
        if longo_sem:
            r, det = 'PENDENTE', 'Vídeo longo sem destino confirmado'
            prev, pend = set(), True
        elif not ps:
            r, det = 'NEUTRO', 'Geral ou panorama: quebra a sequência'
            prev, pend = set(), False
        elif pend:
            r, det = 'PENDENTE', 'Peça anterior é vídeo longo sem destino'
            prev, pend = ps, False
        elif prev & ps:
            r, det = 'VIOLAÇÃO', f'Anterior: {prev_label}'
            res['violacoes'].append(f'País seguido {e["date"]} {e["id"]}: {sorted(prev & ps)}')
            prev = ps
        else:
            r, det = 'OK', (f'{"/".join(sorted(prev))} → {"/".join(sorted(ps))}' if prev else 'nova sequência')
            prev = ps
        prev_label = f'{e["id"]} ({"/".join(sorted(ps)) or "—"})'
        res['paises'].append({'data': e['date'], 'hora': e.get('recommendedTime') or '', 'id': e['id'],
                              'formato': e['format'], 'cidades': ' + '.join(cs) or 'Geral',
                              'paises': ' + '.join(sorted(ps)) or '—', 'resultado': r, 'detalhe': det})
    return res


if __name__ == '__main__':
    ev = json.load(open(sys.argv[1]))
    prov = '--cenario-provavel' in sys.argv
    r = auditar(ev, prov)
    print(f'Semanas: {len(r["semanas"])} · conformes: {sum(s["status"]=="CONFORME" for s in r["semanas"])}')
    print(f'Reels IG: {sum(s["reels"] for s in r["semanas"])}')
    print(f'Violações: {len(r["violacoes"])}')
    for v in r['violacoes']:
        print('  -', v)
