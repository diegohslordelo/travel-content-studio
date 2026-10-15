"""Validação da V5. Rodar de dentro de planejamento/: python3 scripts/validar_v5.py
Falha (código 1) se algum critério de aceitação verificável por script não for cumprido."""
import json, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from auditoria import auditar

ev = json.load(open('v5/eventos_v5.json', encoding='utf-8'))
erros = []
ids = [e['id'] for e in ev]
if len(ids) != len(set(ids)):
    erros.append('IDs repetidos')

OBRIG_REEL = ['title', 'pillar', 'group', 'objective', 'audience', 'concept', 'hook', 'hookAlts', 'visualHook', 'promise', 'payoff',
              'retention', 'shareMechanism', 'cta', 'structure', 'overlay', 'assets', 'timestamps', 'newRecording', 'duration', 'cover',
              'caption', 'platformAdaptation', 'metric', 'risks', 'score', 'scoreNote', 'status', 'ds']
OBRIG_CAR = ['title', 'objective', 'audience', 'concept', 'promise', 'slides', 'cover', 'caption', 'cta', 'assets', 'metric', 'status']
OBRIG_FOTO = ['title', 'concept', 'assets', 'caption', 'cta', 'whyPhoto', 'status']
OBRIG_STO = ['title', 'structure', 'objective', 'cta']
for e in ev:
    obr = {'Reel': OBRIG_REEL, 'Carrossel': OBRIG_CAR, 'Foto': OBRIG_FOTO, 'Stories': OBRIG_STO}.get(e['format'], [])
    for k in obr:
        if not e.get(k):
            erros.append(f'{e["id"]}: campo vazio {k}')
    if e['format'] == 'Reel':
        if len(e['hookAlts']) != 2:
            erros.append(f'{e["id"]}: precisa de 2 ganchos alternativos')
        if len(e['structure']) < 3:
            erros.append(f'{e["id"]}: storyboard curto')
        if not re.search(r'IMG_|\.mp4|\.mov|Master|talking head|registro|Gravação|Gravar|fotograma', e['assets'], re.I):
            erros.append(f'{e["id"]}: sem arquivo, gravação ou dado identificado')
        if e['cta'].rstrip('.') not in e['caption']:
            erros.append(f'{e["id"]}: CTA não está na legenda')
        if e['scoreTotal'] < 5:
            erros.append(f'{e["id"]}: nota {e["scoreTotal"]} (reformular)')
    if e['format'] in ('Reel', 'Carrossel', 'Foto'):
        texto = ' '.join(str(e.get(k, '')) for k in ('title', 'hook', 'caption', 'overlay'))
        if re.search(r'€\s?\d|R\$\s?\d|\d+\s?euros?', texto):
            erros.append(f'{e["id"]}: valor em texto publicável')
        if re.search(r'\bgrátis\b|\bde graça\b', texto, re.I) and 'não dizer' not in texto:
            erros.append(f'{e["id"]}: "grátis" em texto publicável')
    if e['format'] == 'Reel' and e['date'] < '2026-10-15':
        erros.append(f'{e["id"]}: data passada')

for prov in (False, True):
    r = auditar(ev, prov)
    if r['violacoes']:
        erros += [('provável: ' if prov else '') + v for v in r['violacoes']]
    if any(s['status'] != 'CONFORME' for s in r['semanas']):
        erros.append('cadência fora da regra')

longos = sorted(e['date'] for e in ev if e.get('anchor'))
esperado = ['2026-10-24', '2026-11-07', '2026-11-21', '2026-12-05', '2026-12-19', '2027-01-02', '2027-01-16', '2027-01-30', '2027-02-13', '2027-02-27']
if longos != esperado:
    erros.append(f'datas dos vídeos longos mudaram: {longos}')

reels = [e for e in ev if e['format'] == 'Reel']
print(f'{len(ev)} eventos · {len(reels)} Reels · {len(erros)} erros')
for x in erros:
    print(' -', x)
sys.exit(1 if erros else 0)
