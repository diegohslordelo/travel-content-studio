"""Plano v6 (15/10/2026): calendário do feed, lançamentos do YouTube, TikTok, Shorts e Stories até 28/02/2027.

Este arquivo só define O QUE vai para QUAL data. O conteúdo de cada peça nova está em v6_conteudo_*.py
e a montagem do painel em aplicar_v6.py.

Regra de cidades (CLAUDE.md, 7): cada cidade aparece no máximo 2 dias por semana (seg a dom) e nunca
em dias seguidos, em todas as plataformas. Peças do mesmo pacote editorial (mesma peça criativa
distribuída no mesmo dia: Reel + Short + TikTok + Stories de repercussão) contam como 1 aparição.
"""
import datetime as dt

HOJE = '2026-10-15'
FIM = '2027-02-28'

CIDADES = {'bcn': 'Barcelona', 'ams': 'Amsterdam', 'bxl': 'Bruxelas', 'brg': 'Bruges', 'par': 'Paris',
           'dis': 'Disneyland Paris', 'mad': 'Madrid', 'lis': 'Lisboa', 'ita': 'Roma',
           'flo': 'Florença', 'ven': 'Veneza', 'mil': 'Milão'}

# Vídeos longos do YouTube: datas FIXAS (não mudar). id do post, cidade.
VLOGS = {'2026-10-24': ('p34', 'ams'), '2026-11-07': ('p55', 'par'), '2026-11-21': ('p76', 'dis'),
         '2026-12-05': ('p97', 'mad'), '2026-12-19': ('p118', 'bxl'), '2027-01-02': ('p139', 'brg'),
         '2027-01-16': ('p160', 'lis')}

# Eixos editoriais (relatório de equilíbrio). Uma peça pode ter mais de um.
EIXOS = {'ins': 'Inspiração e desejo', 'exp': 'Vlog e experiência pessoal', 'cus': 'Custos e orçamento',
         'rot': 'Roteiro e organização', 'doc': 'Documentação e preparação', 'loc': 'Locomoção e logística',
         'pop': 'Formato popular', 'aut': 'Autoral e storytelling', 'ser': 'Série Primeiro Dia', 'lan': 'Lançamento do YouTube'}

# ───────────── peças fixas do feed (data, hora, id, fmt, cidades, eixos) ─────────────
R, C = 'Reel', 'Carrossel'
FIXOS = [
    ('2026-10-15', '12:30', 'p204', R, ['par'], 'exp pop'),
    ('2026-10-17', '11:00', 'p272', R, ['par'], 'rot pop'),
    ('2026-10-18', '19:00', 'p205', R, ['ita'], 'ins'),
    # lançamentos: trailer (antes), Primeiro dia (no sábado do vlog), teaser (depois)
    ('2026-10-22', '12:30', 'p801', R, ['ams'], 'lan pop'),
    ('2026-10-24', '11:00', 'p207', R, ['ams'], 'ser exp'),
    ('2026-10-25', '19:00', 'p300', R, ['bcn'], 'ser exp'),
    ('2026-10-27', '18:30', 'p802', R, ['ams'], 'lan exp'),
    ('2026-11-05', '12:30', 'p803', R, ['par'], 'lan pop'),
    ('2026-11-07', '11:00', 'p234', R, ['par'], 'ser exp'),
    ('2026-11-10', '18:30', 'p804', R, ['par'], 'lan exp'),
    ('2026-11-19', '12:30', 'p805', R, ['dis'], 'lan pop'),
    ('2026-11-21', '11:00', 'p215', R, ['dis'], 'ser exp'),
    ('2026-11-24', '18:30', 'p806', R, ['dis'], 'lan exp'),
    ('2026-12-03', '12:30', 'p807', R, ['mad'], 'lan pop'),
    ('2026-12-05', '11:00', 'p221', R, ['mad'], 'ser exp'),
    ('2026-12-08', '18:30', 'p607', R, ['mad'], 'lan exp aut'),
    ('2026-12-16', '18:00', 'p248', C, ['ita'], 'rot'),
    ('2026-12-17', '12:30', 'p808', R, ['bxl'], 'lan pop'),
    ('2026-12-19', '11:00', 'p304', R, ['bxl'], 'ser exp'),
    ('2026-12-22', '18:30', 'p809', R, ['bxl'], 'lan exp'),
    ('2026-12-24', '12:30', 'p254', R, ['ita'], 'ser exp'),
    ('2026-12-27', '19:00', 'p247', R, [], 'pop ser'),
    ('2026-12-29', '18:30', 'p810', R, ['brg'], 'lan pop'),
    ('2026-12-31', '12:30', 'p259', R, ['ven'], 'exp aut'),
    ('2027-01-02', '11:00', 'p305', R, ['brg'], 'ser exp'),
    ('2027-01-05', '18:30', 'p811', R, ['brg'], 'lan exp'),
    ('2027-01-14', '12:30', 'p812', R, ['lis'], 'lan pop'),
    ('2027-01-16', '11:00', 'p270', R, ['lis'], 'ser exp'),
    ('2027-01-19', '18:30', 'p813', R, ['lis'], 'lan exp'),
]

# ───────────── peças flexíveis (ordem = prioridade), com data mínima e máxima ─────────────
# (id, fmt, cidades, eixos, cedo, tarde)
POOL = [
    ('p208', C, ['bcn'], 'rot ins', '2026-10-21', None),
    ('p206', R, ['brg'], 'pop exp', '2026-10-20', None),
    ('p264', R, [], 'rot exp aut', '2026-10-20', None),
    ('p830', R, [], 'doc', '2026-10-26', '2026-11-15'),
    ('p203', C, ['bcn'], 'rot loc', '2026-10-28', None),
    ('p611', R, ['bxl'], 'ins pop', '2026-10-27', None),
    ('p246', R, ['par'], 'ins', '2026-10-29', None),
    ('p217', R, [], 'ser aut', '2026-10-30', '2026-11-08'),
    ('p222', R, ['ita'], 'pop exp', '2026-11-01', None),
    ('p621', C, ['ams'], 'rot', '2026-11-03', None),
    ('p601', R, ['ams'], 'ins', '2026-11-03', None),
    ('p229', R, ['ams'], 'cus', '2026-11-03', None),
    ('p603', R, ['ams'], 'pop', '2026-11-09', None),
    ('p218', C, ['ita'], 'cus rot', '2026-11-09', None),
    ('p224', R, ['bcn', 'mad'], 'rot pop', '2026-11-10', None),
    ('p608', R, ['dis'], 'ins', '2026-11-12', None),
    ('p213', C, ['par'], 'rot', '2026-11-11', None),
    ('p612', R, [], 'exp aut', '2026-11-13', None),
    ('p227', R, ['lis'], 'exp pop', '2026-11-15', None),
    ('p627', C, ['ita'], 'rot', '2026-11-16', None),
    ('p609', R, ['lis'], 'ins', '2026-11-16', None),
    ('p606', R, ['mad'], 'ins', '2026-11-20', None),
    ('p250', R, ['bcn'], 'loc cus', '2026-11-22', None),
    ('p231', R, ['bcn'], 'pop exp', '2026-11-22', None),
    ('p821', C, ['par'], 'rot loc', '2026-11-23', None),
    ('p220', R, ['par'], 'ins rot', '2026-11-25', None),
    ('p242', R, ['ita'], 'ins', '2026-11-28', '2026-12-20'),
    ('p214', R, ['bcn'], 'pop aut', '2026-11-28', None),
    ('p302', R, ['ven'], 'ser exp', '2026-11-29', None),
    ('p831', C, [], 'doc', '2026-11-30', None),
    ('p820', R, ['dis'], 'loc', '2026-11-30', None),
    ('p620', C, ['bxl'], 'rot loc', '2026-12-01', None),
    ('p253', R, ['dis'], 'cus', '2026-12-01', None),
    ('p273', C, ['ams'], 'rot', '2026-12-07', None),
    ('p244', R, ['mad'], 'rot', '2026-12-07', None),
    ('p301', R, ['flo'], 'ser exp', '2026-12-07', None),
    ('p241', R, ['ams', 'brg'], 'pop ins', '2026-12-07', None),
    ('p600', R, ['bxl'], 'pop', '2026-12-08', None),
    ('p260', R, ['par', 'dis'], 'rot', '2026-12-10', None),
    ('p605', R, ['bcn', 'mad'], 'exp pop', '2026-12-14', None),
    ('p278', R, ['mad'], 'cus', '2026-12-14', None),
    ('p230', R, ['ven'], 'ins loc', '2026-12-14', None),
    ('p623', C, ['brg'], 'ins', '2026-12-21', None),
    ('p303', R, ['mil'], 'ins', '2026-12-21', None),
    ('p257', R, ['bcn', 'ams', 'brg'], 'exp pop', '2026-12-21', None),
    ('p622', C, ['mad'], 'rot', '2026-12-28', None),
    ('p279', R, ['dis'], 'exp', '2026-12-28', None),
    ('p262', R, ['bcn'], 'doc rot', '2027-01-04', None),
    ('p624', C, ['dis'], 'rot', '2027-01-04', None),
    ('p265', R, ['bcn'], 'lan exp', '2027-01-06', None),
    ('p826', R, ['bxl'], 'loc', '2027-01-06', None),
    ('p822', R, ['ven'], 'loc exp', '2027-01-08', None),
    ('p271', R, ['bcn'], 'rot', '2027-01-10', None),
    ('p238', C, ['lis'], 'rot', '2027-01-18', None),
    ('p237', C, ['ita'], 'cus', '2027-01-04', None),
    ('p274', R, ['lis'], 'ins', '2027-01-20', None),
    ('p829', R, ['ams'], 'loc cus', '2027-01-11', None),
    ('p625', C, [], 'ser rot', '2027-01-18', None),
    ('p614', R, ['par'], 'exp aut', '2027-01-18', None),
    ('p840', R, ['flo'], 'ins', '2027-01-18', None),
    ('p832', R, [], 'doc', '2027-01-20', None),
    ('p615', R, ['ita'], 'ins rot', '2027-01-24', None),
    ('p232', C, [], 'cus rot', '2027-01-25', None),
    ('p828', R, ['lis'], 'loc', '2027-01-25', None),
    ('p281', R, [], 'pop', '2027-01-29', None),
    ('p616', R, ['ams'], 'pop exp', '2027-02-01', None),
    ('p269', R, ['ams'], 'loc ins', '2027-02-08', None),
    ('p842', R, ['flo'], 'ins', '2027-02-06', None),
    ('p263', C, [], 'cus', '2027-02-08', None),
]

# Slots do feed por dia da semana (0 = segunda)
SLOTS = {1: ('18:30', R), 2: ('18:00', C), 3: ('12:30', R), 5: ('11:00', R), 6: ('19:00', R)}


def dias(a, b):
    d = dt.date.fromisoformat(a)
    while d <= dt.date.fromisoformat(b):
        yield d.isoformat()
        d += dt.timedelta(days=1)


def semana(d):
    x = dt.date.fromisoformat(d)
    return (x - dt.timedelta(days=x.weekday())).isoformat()


class Agenda:
    """Aparições editoriais por cidade: {cidade: {data: set(pacotes)}}"""

    def __init__(self):
        self.ap = {}

    def add(self, d, cids, pac):
        for c in cids:
            self.ap.setdefault(c, {}).setdefault(d, set()).add(pac)

    def cabe(self, d, cids, pac=None):
        for c in cids:
            dias_c = self.ap.get(c, {})
            if d in dias_c and pac in dias_c[d]:
                continue          # mesmo pacote no mesmo dia: não conta de novo
            if d in dias_c:
                return False      # outra peça da mesma cidade no mesmo dia conta como 2ª aparição: evitar
            x = dt.date.fromisoformat(d)
            for v in (x - dt.timedelta(days=1), x + dt.timedelta(days=1)):
                if v.isoformat() in dias_c:
                    return False
            s = semana(d)
            n = sum(len(p) for dd, p in dias_c.items() if semana(dd) == s)
            if n >= 2:
                return False
        return True


def montar_feed():
    ag = Agenda()
    for d, (pid, c) in VLOGS.items():
        ag.add(d, [c], 'pac:' + d + ':' + c)
    feed = {}
    for d, h, pid, f, cids, e in FIXOS:
        pac = ('pac:' + d + ':' + cids[0]) if (cids and d in VLOGS and VLOGS[d][1] == cids[0]) else pid
        ag.add(d, cids, pac)
        feed[(d, h)] = (pid, f, cids, e, pac)
    pool = list(POOL)
    sobras = []
    for d in dias('2026-10-16', FIM):
        wd = dt.date.fromisoformat(d).weekday()
        if wd not in SLOTS:
            continue
        h, f = SLOTS[wd]
        if any(k[0] == d and v[1] == f for k, v in feed.items()):
            continue
        for i, (pid, pf, cids, e, cedo, tarde) in enumerate(pool):
            if pf != f or d < cedo or (tarde and d > tarde):
                continue
            if ag.cabe(d, cids):
                ag.add(d, cids, pid)
                feed[(d, h)] = (pid, f, cids, e, pid)
                pool.pop(i)
                break
        else:
            sobras.append((d, h, f))
    return feed, ag, pool, sobras


# ───────────── TikTok: ideias próprias (sexta, 19:00) ─────────────
# (id, cidades, eixos, conceito-semente). O conteúdo completo fica em v6_conteudo_*.py.
TT_ORIGINAIS = [
    ('tk01', ['par'], 'pop loc', 'POV: você sai do metrô e dá de cara com o Arco do Triunfo (IMG_2811, 17/03 12:37).'),
    ('tk02', ['ams'], 'exp aut', 'O Brasil não sai da gente: a C&A em Amsterdam (IMG_1474).'),
    ('tk03', ['dis'], 'exp pop', 'Perdi a Marina no brinquedo do Buzz Lightyear (IMG_3425–3426, 18/03 16:40).'),
    ('tk04', ['mad'], 'pop aut', 'O churro de Madrid × o do Brasil: “o do Brasil ainda ganha” (IMG_3952–3954, 20/03 16:51).'),
    ('tk05', ['bxl'], 'exp pop', 'Sete graus em Bruxelas e a gente de casaco fino (IMG_2394, 15/03).'),
    ('tk06', ['ven'], 'loc exp', 'Não tem lugar no trem: a saída de Veneza em 02/01 (IMG_6249, 11:05).'),
    ('tk07', ['flo'], 'pop ins', 'Formigueiro de turista: o Duomo de Florença ao meio-dia (IMG_5555–5560, 28/12 12:35).'),
    ('tk08', ['mil'], 'aut exp', '“Se fosse Salvador…”: a feira de Milão vista por um soteropolitano (IMG_6352, 03/01 10:32).'),
    ('tk09', ['lis'], 'exp pop', 'A atração que a gente não sabia que era paga (IMG_4489–4490, 23/03 10:38), sem citar valor.'),
    ('tk10', ['ams'], 'exp', 'Perrengue chique: o guarda-chuva novo em Amsterdam (IMG_1537).'),
    ('tk11', ['dis'], 'exp pop', 'Nervoso antes da Tower of Terror (IMG_3273, 18/03 12:08) e a reação depois (IMG_3283).'),
    ('tk12', ['mad'], 'exp pop', 'O veredito do hambúrguer: “os de Salvador dão um banho” (IMG_3986, 20/03 22:23).'),
    ('tk13', ['bxl'], 'pop', 'O Manneken Pis vestido de jogador (IMG_2258, 15/03).'),
    ('tk14', ['mil'], 'loc exp', 'O trem da madrugada saindo da Itália (IMG_6370, 04/01 00:20).'),
    ('tk15', ['ita'], 'ins pop', 'Roma: uma cena de Natal do acervo de vídeo de 25/12 (escolher no acervo/italia).'),
    ('tk16', ['brg'], 'ins pop', 'Bruges: a praça Markt chegando de manhã (IMG_2449, 16/03 11:47), POV de chegada.'),
    ('tk17', ['par'], 'pop', 'A Torre Eiffel que aparece de qualquer lugar de Paris (IMG_2978, 17/03 14:16).'),
    ('tk18', ['dis'], 'exp', 'O balde de pipoca que não cabe na mala (IMG_3572–3573, 18/03 19:25).'),
    ('tk19', ['ven'], 'ins', 'Veneza no 1º dia do ano: o Grande Canal às 11h19 (IMG_6174).'),
    ('tk20', ['lis'], 'loc', 'Lisboa: do aeroporto de metrô (IMG_4233, 22/03).'),
    ('tk21', ['flo'], 'ins', 'Florença: o pôr do sol de 29/12 (IMG_5808–5812, 17:04).'),
    ('tk22', ['brg'], 'exp', 'Bruges: a primeira parada correndo de fome (IMG_2430, 16/03 11:27).'),
]

# ───────────── Stories: sequências próprias de cidade (segunda-feira) ─────────────
ST_CIDADE = [
    ('sq01', ['bxl'], 'Bruxelas em 6 telas: a Grand Place de dia e à noite (fotodump de vídeo).'),
    ('sq02', ['flo'], 'Florença: 5 telas do primeiro dia (28/12) + enquete “Florença ou Veneza?”.'),
    ('sq03', ['lis'], 'Lisboa: a primeira noite em 5 telas (22/03) + caixinha “o que comer em Lisboa?”.'),
    ('sq04', ['ita'], 'Roma no Natal: 5 telas de vídeo de 25/12 + quiz.'),
    ('sq05', ['brg'], 'Bruges: 5 telas de canal + enquete “Bruges ou Amsterdam?”.'),
    ('sq06', ['mil'], 'Milão numa tarde: 4 telas do castelo + pergunta.'),
    ('sq07', ['ven'], 'Veneza: 5 telas do Grande Canal + quiz “quantas pontes tem Veneza?” (resposta em fonte oficial).'),
    ('sq08', ['mad'], 'Madrid: 5 telas do Retiro e de Cibeles + enquete.'),
    ('sq09', ['ams'], 'Amsterdam: 5 telas de canais + caixinha.'),
    ('sq10', ['par'], 'Paris: 5 telas do Trocadéro e da Torre + enquete “de dia ou de noite?”.'),
    ('sq11', ['dis'], 'Disney: 5 telas do castelo + quiz.'),
    ('sq12', ['bcn'], 'Barcelona: 5 telas do master (Gràcia, Montjuïc) + caixinha.'),
]


def montar_resto(feed, ag):
    """Distribui TikTok próprio (sex), Short-capítulo (semana do teaser) e Stories de cidade (seg)."""
    extra = []
    # Short-capítulo do vlog na semana do teaser: sábado (ou domingo) da semana seguinte ao vlog
    for dv, (vid, c) in VLOGS.items():
        x = dt.date.fromisoformat(dv)
        for k in (7, 8, 6):
            d = (x + dt.timedelta(days=k)).isoformat()
            if d <= FIM and ag.cabe(d, [c]):
                ag.add(d, [c], 'cap:' + c)
                extra.append((d, '20:30', 'SH-CAP', 'YouTube', 'Short', [c], 'lan exp', 'Capítulo do vlog de %s (corte independente)' % CIDADES[c], vid))
                break
    tt = list(TT_ORIGINAIS)
    st = list(ST_CIDADE)
    for d in dias('2026-10-16', FIM):
        wd = dt.date.fromisoformat(d).weekday()
        if wd == 4:
            for i, (tid, cids, e, conc) in enumerate(tt):
                if ag.cabe(d, cids):
                    ag.add(d, cids, tid)
                    extra.append((d, '19:00', tid, 'TikTok', 'TikTok', cids, e, conc, None))
                    tt.pop(i)
                    break
        if wd == 0 and d > '2026-10-18':
            # alterna: semana par = sequência de cidade; ímpar = relacionamento sem cidade
            n = (dt.date.fromisoformat(d) - dt.date(2026, 10, 19)).days // 7
            if n % 2 == 0:
                for i, (sid, cids, conc) in enumerate(st):
                    if ag.cabe(d, cids):
                        ag.add(d, cids, sid)
                        extra.append((d, '—', sid, 'Instagram', 'Stories', cids, 'ins pop', conc, None))
                        st.pop(i)
                        break
    return extra, tt, st


if __name__ == '__main__':
    feed, ag, pool, sobras = montar_feed()
    for (d, h), (pid, f, cids, e, pac) in sorted(feed.items()):
        print(d, dt.date.fromisoformat(d).strftime('%a'), h, pid, f[:3], ','.join(cids) or '—', e)
    print('NÃO ENTRARAM:', [p[0] for p in pool])
    print('SLOTS VAZIOS:', sobras)
    extra, tt, st = montar_resto(feed, ag)
    for x in extra:
        print('EXTRA', x[0], dt.date.fromisoformat(x[0]).strftime('%a'), x[2], ','.join(x[5]), x[7][:60])
    print('TikTok sem vaga:', [t[0] for t in tt], '| Stories sem vaga:', [t[0] for t in st])
