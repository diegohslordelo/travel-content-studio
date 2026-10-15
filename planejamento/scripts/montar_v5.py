"""Monta a V5 do planejamento: eventos, auditorias (CSV) e painel HTML.

Rodar de dentro de planejamento/:  python3 scripts/montar_v5.py
Lê: versoes/planejamento-primeiro-dia-v4-cadencia-4-reels.html (V4 preservada) e os módulos de peças.
Escreve: planejamento-primeiro-dia-v5.html e v5/*.csv, v5/eventos_v5.json.
"""
import csv, json, os, re, sys, datetime as dt
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from grade_v5 import GRADE, LONGOS
from pecas_reels_1 import REELS_1
from pecas_reels_2 import REELS_2
from pecas_reels_3 import REELS_3
from pecas_outros import CARROSSEIS, FOTOS, STORIES, LONGOS_INFO
from pecas_comum import stories as mk_stories
from auditoria import auditar, PAIS, semana

V4_HTML = 'versoes/planejamento-primeiro-dia-v4-cadencia-4-reels.html'
SAIDA_HTML = 'planejamento-primeiro-dia-v5.html'
PASTA = 'v5'
RAMO = 'claude/eager-archimedes-dmwfex'

PECAS = {**REELS_1, **REELS_2, **REELS_3, **CARROSSEIS, **FOTOS}

# IDs da V4 mantidos (mesma peça) e a decisão registrada.
MANTIDOS = {
    'AMS-casas-tortas': ('IG-20261020-REE-amsterdam-trailer', 'reformular'),
    'AMS-primeiro-dia': ('IG-20261028-REE-amsterdam-first-day', 'reformular'),
    'PAR-custo': ('IG-20261126-REE-paris-037', 'mover de data'),
    'AMS-custo': ('IG-20270211-REE-amsterdam-103', 'reformular'),
    'GER-planilha': ('IG-20261021-REEL-general-04', 'mover de data'),
    'CAR-docs': ('IG-20261108-CAR-geral-022', 'mover de data'),
    'CAR-lisboa-custo': ('IG-20261231-REE-lisboa-067', 'mudar de formato'),
}

# Motivos por modelo de título da V4 (diagnóstico da auditoria criativa).
MOTIVOS = [
    (r'^Quiz visual', 'Modelo repetido 20 vezes; Stories com cidade contavam como aparição. Na V5 os Stories são gerais e ligados às peças da semana.'),
    (r'^O que você salvaria', 'Modelo repetido 19 vezes, sem assunto próprio. Substituído por Stories ligados às peças da semana.'),
    (r'^Lançamento do vídeo longo|^ESTREIA', 'Data fixa preservada.'),
    (r'motivos visuais|sem pressa|em 3 cenas|contado pelas imagens|enviaria essa vista|Vale guardar|^POV: você chegou|Um minuto\? Não|atmosfera de|textura, a luz|ficou na memória|lembrança em movimento|quase deixaria passar|mostraria para alguém|abriria um diário|muda de um plano|detalhes de .* merecem|explorar sem pressa|Expectativa x realidade|POV —',
     'Modelo genérico que só trocava o nome da cidade, sem fato, arquivo nem promessa. Trocado por uma peça com material identificado no acervo.'),
    (r'pesquisaria antes de ir|O que conferir antes de montar|Como organizar um dia|em 6 imagens|Pequenas cenas',
     'Carrossel genérico repetido em várias cidades. Trocado por roteiro com hora real ou checklist nascido de um caso real.'),
    (r'^Checklist de documentos', 'Repetido 3 vezes na V4. Fica uma versão (26/10), com fonte oficial.'),
    (r'^Quanto gastei|^Quanto custa', 'Peça de custo duplicada ou sem dados. A V5 mantém 4 peças de custo como "Aguardando dados de custos do Diego".'),
    (r'^Foto única', 'Foto genérica sem imagem definida. Trocada por foto com imagem e contexto identificados.'),
    (r'^Trailer|^Teaser', 'Trailer mantido como curiosidade completa; o teaser pós-lançamento repetia a função do trailer e do Reel da série.'),
]
MOTIVO_GERAL = ('Reel geral de conselho abstrato, sem experiência ou fonte (ex.: "Seu roteiro não precisa ter tudo"). '
                'A V5 usa o horário para uma peça com material real ou para serviço com fonte oficial.')


def ler_v4():
    linhas = open(V4_HTML, encoding='utf-8').read().split('\n')
    j = linhas[44][len('const INITIAL_EVENTS = '):].rstrip().rstrip(';')
    return json.loads(j)


def motivo(t):
    for pat, m in MOTIVOS:
        if re.search(pat, t):
            return m
    return MOTIVO_GERAL


def montar():
    v4 = ler_v4()
    v4_por_id = {e['id']: e for e in v4}
    eventos = []
    usados_v4 = {}
    semana_n = {}
    for i, s in enumerate(sorted({semana(g[0]) for g in GRADE})):
        semana_n[s] = i
    for data, hora, fmt, chave, cidades in GRADE:
        if fmt == 'Stories':
            w = semana_n[semana(data)]
            tit, telas, sticker, func = STORIES[chave]
            e = mk_stories(title=tit, structure=telas, cta=f'Interação: {sticker}.', objective=func, pillar='Relacionamento', group='',
                           concept='Sequência curta, geral (sem destacar cidade), ligada às peças da semana. Não conta para a meta de Reels nem como aparição de cidade.',
                           duration=f'{len(telas)} telas', metric='Respostas, votos e conclusão da sequência.', risks='Nenhum valor ou preço nas telas.')
        else:
            e = dict(PECAS[chave])
        e['key'] = chave
        e['date'], e['recommendedTime'] = data, hora
        cs = [c for c in cidades]
        e['cities'] = cs
        e['city'] = 'Geral' if not cs else ('Várias' if cs == ['Várias'] else ' + '.join(cs))
        e['weekStart'] = semana(data)
        e['anchor'] = False
        if chave in MANTIDOS:
            vid, dec = MANTIDOS[chave]
            e['id'] = vid
            e['v4Ref'] = vid
            e['v4Decision'] = dec
            usados_v4[vid] = (e, dec)
        else:
            e['id'] = f'V5-{data.replace("-", "")}-{chave}'
        eventos.append(e)
    # Vídeos longos: IDs e datas da V4.
    for data, cidade, provavel in LONGOS:
        base = next(x for x in v4 if x['anchor'] and x['date'] == data)
        e = dict(base)
        info = LONGOS_INFO[data]
        e['cities'] = [cidade] if cidade else []
        e['city'] = cidade or 'Geral'
        if provavel and not cidade:
            e['probableCity'] = provavel
            e['notes'] = (f'Destino a confirmar no calendário do canal. O painel original do Diego (05/10/2026) listava: {info[1]}. '
                          'A V5 foi auditada também nesse cenário (0 violações). Stories do dia: só "vídeo novo no canal" (geral) até o destino ser confirmado.')
        elif not cidade:
            e['notes'] = 'Destino a confirmar no calendário do canal; o painel original de 05/10/2026 não chegava a esta data. Não planejar peça que dependa da viagem de janeiro de 2027.'
        else:
            e['notes'] = 'Data fixa confirmada. Peças de apoio: AMS-casas-tortas (20/10, função de trailer) e AMS-primeiro-dia (28/10). Stories do dia são o pacote do lançamento (mesma aparição).'
        e['v4Ref'], e['v4Decision'] = e['id'], 'manter'
        e['weekStart'] = semana(data)
        e['structure'] = e.get('structure') or []
        usados_v4[e['id']] = (e, 'manter')
        eventos.append(e)
    # Ligação com a V4 por data e formato.
    por_data_fmt = defaultdict(list)
    for e in eventos:
        por_data_fmt[(e['date'], e['format'])].append(e)
    decisoes = {}
    pendentes = []
    for x in sorted(v4, key=lambda x: (x['date'], x['format'])):
        if x['id'] in usados_v4:
            e, dec = usados_v4[x['id']]
            why = {'manter': 'Data fixa do vídeo longo preservada.',
                   'reformular': 'Mesma peça e mesma função; conceito, gancho e briefing refeitos com arquivo real.',
                   'mover de data': f'Mesma peça; movida de {x["date"]} para {e["date"]} para cumprir a regra de cidade/país ou a sequência editorial.',
                   'mudar de formato': f'Mesma pauta; virou {e["format"].lower()} em {e["date"]}.'}[dec]
            decisoes[x['id']] = dict(date=x['date'], v4Id=x['id'], v4Title=x['title'], decision=dec, v5Id=e['id'], v5Title=e['title'], reason=why)
            continue
        alvo = [e for e in por_data_fmt.get((x['date'], x['format']), []) if 'v4Ref' not in e]
        if alvo:
            e = alvo[0]
            e['v4Ref'], e['v4Decision'] = x['id'], 'substitui peça da V4'
            decisoes[x['id']] = dict(date=x['date'], v4Id=x['id'], v4Title=x['title'], decision='substituir', v5Id=e['id'], v5Title=e['title'], reason=motivo(x['title']))
        else:
            pendentes.append(x)
    for x in pendentes:  # segunda passada: mesmo dia, outro formato, ou horário liberado
        livres = [e for e in eventos if e['date'] == x['date'] and not e.get('anchor') and 'v4Ref' not in e]
        ocupados = [e for e in eventos if e['date'] == x['date'] and not e.get('anchor') and e['format'] != 'Stories']
        if livres:
            e = livres[0]
            e['v4Ref'], e['v4Decision'] = x['id'], 'substitui peça da V4 (outro formato)'
            dec = 'substituir (formato mudou)'
        elif ocupados:
            e = ocupados[0]
            dec = 'substituir (horário ocupado por peça movida)'
        else:
            e, dec = None, 'remover (horário liberado)'
        decisoes[x['id']] = dict(date=x['date'], v4Id=x['id'], v4Title=x['title'], decision=dec, v5Id=e['id'] if e else '', v5Title=e['title'] if e else '', reason=motivo(x['title']))
    decisoes = sorted(decisoes.values(), key=lambda d: (d['date'], d['v4Id']))
    for e in eventos:
        e.setdefault('v4Decision', 'nova na V5')
    eventos.sort(key=lambda e: (e['date'], e.get('recommendedTime') or '99'))
    return v4, eventos, decisoes


def escrever_csv(nome, linhas, campos):
    with open(os.path.join(PASTA, nome), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        w.writeheader()
        for l in linhas:
            w.writerow({k: (' | '.join(v) if isinstance(v, list) else v) for k, v in l.items()})


def pendencias(eventos):
    out = []
    for e in eventos:
        tipos = []
        txt = ' '.join(str(e.get(k, '')) for k in ('assets', 'timestamps', 'risks', 'status', 'costData', 'newRecording'))
        if 'verificar' in txt.lower() or e.get('status', '').startswith('Planejado — verificar'):
            tipos.append('verificar arquivo/trecho no acervo')
        if 'Gravar' in e.get('status', '') or (e.get('newRecording') and not e['newRecording'].startswith('Nenhuma') and not e['newRecording'].startswith('Telas simples')):
            tipos.append('gravação nova')
        if 'Validar fontes' in e.get('status', '') or 'fonte oficial' in txt or 'site oficial' in txt:
            tipos.append('fonte oficial')
        if e.get('costData') or 'custos do Diego' in e.get('status', ''):
            tipos.append('dados de custos do Diego')
        if 'decisão do Diego' in e.get('status', '') or 'autorização do Diego' in txt or 'confirmação do Diego' in txt or 'Destino a confirmar' in e.get('notes', ''):
            tipos.append('decisão do Diego')
        if 'Família' in txt or 'terceiros' in txt:
            tipos.append('pessoas no vídeo (autorização)')
        if tipos:
            out.append(dict(id=e['id'], data=e['date'], formato=e['format'], cidade=e['city'], titulo=e['title'], status=e.get('status', ''),
                            pendencias='; '.join(dict.fromkeys(tipos)), detalhe=(e.get('costData') or '') + ' ' + (e.get('risks') or '')[:400]))
    return out


def main():
    os.makedirs(PASTA, exist_ok=True)
    v4, eventos, decisoes = montar()
    json.dump(eventos, open(os.path.join(PASTA, 'eventos_v5.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    r = auditar(eventos, False)
    rp = auditar(eventos, True)
    # CSVs
    sem = [dict(semana=s['semana'], reels=s['reels'], datas=s['datas'], ids=s['ids'], quinta='sim' if s['quinta'] else 'não',
                domingo='sim' if s['domingo'] else 'não', status=s['status']) for s in r['semanas']]
    escrever_csv('auditoria-semanal-reels.csv', sem, ['semana', 'reels', 'datas', 'ids', 'quinta', 'domingo', 'status'])
    cid = []
    for cen, rr in (('confirmado', r), ('provável', rp)):
        for c in rr['cidades']:
            cid.append(dict(cenario=cen, cidade=c['cidade'], pais=c['pais'], semana=c['semana'], datas=c['datas'], formatos=c['formatos'], ids=c['ids'],
                            contagem=c['contagem'], violacoes=c['violacao'] or 'nenhuma'))
    escrever_csv('auditoria-cidades.csv', cid, ['cenario', 'cidade', 'pais', 'semana', 'datas', 'formatos', 'ids', 'contagem', 'violacoes'])
    pai = [dict(cenario=cen, **p) for cen, rr in (('confirmado', r), ('provável', rp)) for p in rr['paises']]
    escrever_csv('auditoria-paises.csv', pai, ['cenario', 'data', 'hora', 'id', 'formato', 'cidades', 'paises', 'resultado', 'detalhe'])
    mapa = defaultdict(Counter)
    for e in eventos:
        mapa[e['weekStart']][f"{e['format']}"] += 1
        if e.get('group'):
            mapa[e['weekStart']]['grupo ' + e['group']] += 1
    cols = ['semana', 'Reel', 'Carrossel', 'Foto', 'Stories', 'Vídeo longo (marco fixo)'] + [f'grupo {g}' for g in 'ABCDEF']
    escrever_csv('mapa-pilares-formato.csv', [dict(semana=w, **{k: mapa[w].get(k, 0) for k in cols[1:]}) for w in sorted(mapa)], cols)
    escrever_csv('pendencias.csv', pendencias(eventos), ['id', 'data', 'formato', 'cidade', 'titulo', 'status', 'pendencias', 'detalhe'])
    escrever_csv('decisoes-v4-v5.csv', decisoes, ['date', 'v4Id', 'v4Title', 'decision', 'v5Id', 'v5Title', 'reason'])
    # HTML
    html = open(V4_HTML, encoding='utf-8').read().split('\n')
    js = open(os.path.join(AQUI, 'painel_v5.js'), encoding='utf-8').read()
    cab = '\n'.join(html[:44])
    dados = 'const INITIAL_EVENTS = ' + json.dumps(eventos, ensure_ascii=False) + ';\nconst DECISOES_V4 = ' + json.dumps(decisoes, ensure_ascii=False) + ';'
    trocas = [
        ('<title>Primeiro Dia — Planejamento Multiplataforma V4 | Out 2026–Fev 2027</title>', '<title>Primeiro Dia — Planejamento V5</title>'),
        ('tree/claude/kind-maxwell-952bcy/acervo', f'tree/{RAMO}/acervo'),
        ('<h1>Uma viagem.<br>Vários jeitos de contar.</h1>', '<h1>Toda cidade tem<br>um primeiro dia.</h1>'),
        ('A grade foi revisada para garantir no mínimo 4 Reels originais de Instagram em cada semana, com terça, quarta, quinta e domingo como cadência-base. Stories, carrosséis e fotos complementam o feed; repostar em Shorts/TikTok não aumenta a contagem semanal. Datas de vídeos longos do YouTube foram preservadas.',
         'V5: cada peça nasce de um arquivo real do acervo (com hora), de uma fonte oficial ou de um dado que o Diego vai enviar. 4 Reels por semana, quinta e domingo sempre com Reel, cidades e países auditados nos dois cenários de vlog. Datas dos vídeos longos preservadas.'),
        ('<option value="all">Todos os status</option></select>', '<option value="all">Todos os status</option></select>\n     <select id="groupFilter" class="control"><option value="all">Todos os grupos criativos</option></select>'),
        ('<button class="tab" data-tab="cadence">Cadência de Reels</button>', '<button class="tab" data-tab="cadence">Cadência de Reels</button><button class="tab" data-tab="changes">Mudanças V4 → V5</button>'),
        ('<div class="view hidden" id="cadenceView"><div id="cadenceContent"></div></div>', '<div class="view hidden" id="cadenceView"><div id="cadenceContent"></div></div>\n   <div class="view hidden" id="changesView"><div id="changesContent"></div></div>'),
        ('Pontue antes de produzir; os números começam zerados.', 'Vem com a nota da revisão V5; ajuste se a avaliação mudar.'),
        ('Documento de trabalho • V4 • 15/10/2026', 'Documento de trabalho • V5 • 15/10/2026 • V4 preservada em versoes/'),
        ('<strong>Base usada:</strong> Referência de Decisão para Instagram + prompt do calendário definitivo + adendo editorial/custos + cadência de YouTube informada em 15/10/2026.',
         '<strong>Base usada:</strong> V4 de 15/10/2026, acervo/ (análise do Colab de 14 e 15/10), referência de conteúdo Instagram, DS V2 2.2.0 e auditoria em planejamento/AUDITORIA_CRIATIVA_V5.md.'),
    ]
    for a, b in trocas:
        assert a in cab, a[:60]
        cab = cab.replace(a, b)
    cab = re.sub(r'<strong>Revisão V4 — cadência mínima de 4 Reels por semana</strong>.*?</div><div class="monthbar">',
                 '<strong>Revisão V5 — ideias com arquivo, hora e promessa</strong>Os modelos genéricos da V4 (o mesmo título trocando só a cidade) saíram. Cada Reel tem gancho principal, 2 alternativas, storyboard, arquivo e hora do acervo, legenda completa, CTA único e nota na matriz. "Verificar no acervo" quer dizer que o trecho ainda precisa ser visto e ouvido. Peças de custo esperam os dados do Diego. Veja a aba "Mudanças V4 → V5".</div><div class="monthbar">', cab, flags=re.S)
    open(SAIDA_HTML, 'w', encoding='utf-8').write(cab + '\n' + dados + '\n' + js + '</script>\n</body>\n</html>\n')
    # Resumo
    print('eventos', len(eventos), Counter(e['format'] for e in eventos))
    print('Reels IG', sum(s['reels'] for s in r['semanas']), 'semanas conformes', sum(s['status'] == 'CONFORME' for s in r['semanas']), '/', len(r['semanas']))
    print('violações (confirmado):', r['violacoes'] or 'nenhuma')
    print('violações (provável):', rp['violacoes'] or 'nenhuma')
    print('países pendentes:', sum(p['resultado'] == 'PENDENTE' for p in r['paises']))
    print('decisões', Counter(d['decision'] for d in decisoes))


if __name__ == '__main__':
    main()
