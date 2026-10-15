"""Junta as análises de todas as cidades (Youtube/analise/<cidade>) em 3 arquivos grandes:
acervo_indice.tsv, acervo_transcricoes.tsv e acervo_resumos.json. Só lê e grava na pasta _acervo.

Uso:  python consolidar_analises.py --base PASTA_ANALISE [--saida PASTA_ANALISE/_acervo]
"""
import argparse, csv, json, os, sys

COLS = ['pasta', 'arquivo', 'criado', 'dur_s', 'largura', 'altura', 'giro', 'fps', 'codec', 'cor', 'audio',
        'volume_db', 'gps', 'aparelho', 'cidade_detectada', 'cidade_origem', 'fala']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--saida', default='')
    a = ap.parse_args()
    base = os.path.abspath(a.base)
    saida = os.path.abspath(a.saida or os.path.join(base, '_acervo'))
    os.makedirs(saida, exist_ok=True)
    pastas = [d for d in sorted(os.listdir(base)) if not d.startswith('_') and os.path.isfile(os.path.join(base, d, 'indice.tsv'))]
    if not pastas:
        sys.exit('Nenhuma pasta com indice.tsv em %s' % base)
    resumos, n_idx, n_tr = {}, {}, {}
    with open(os.path.join(saida, 'acervo_indice.tsv'), 'w', encoding='utf-8', newline='') as fi, \
            open(os.path.join(saida, 'acervo_transcricoes.tsv'), 'w', encoding='utf-8', newline='') as ft:
        wi = csv.writer(fi, delimiter='\t', lineterminator='\n')
        wt = csv.writer(ft, delimiter='\t', lineterminator='\n')
        wi.writerow(COLS)
        wt.writerow(['pasta', 'arquivo', 'inicio_s', 'fim_s', 'texto', 'prob_sem_fala'])
        for p in pastas:
            n_idx[p] = n_tr[p] = 0
            with open(os.path.join(base, p, 'indice.tsv'), encoding='utf-8', newline='') as f:
                for r in csv.DictReader(f, delimiter='\t'):
                    wi.writerow([p] + [(r.get(c) or '').replace('\t', ' ').replace('\n', ' ') for c in COLS[1:]])
                    n_idx[p] += 1
            tp = os.path.join(base, p, 'transcricoes.tsv')
            if os.path.isfile(tp):
                with open(tp, encoding='utf-8', newline='') as f:
                    for r in csv.DictReader(f, delimiter='\t'):
                        wt.writerow([p, r['arquivo'], r['inicio_s'], r['fim_s'], (r.get('texto') or '').replace('\t', ' '), r.get('prob_sem_fala', '')])
                        n_tr[p] += 1
            rp = os.path.join(base, p, 'resumo.json')
            if os.path.isfile(rp):
                resumos[p] = json.load(open(rp, encoding='utf-8'))
    json.dump({'pastas': pastas, 'videos': n_idx, 'trechos_de_fala': n_tr, 'resumos': resumos},
              open(os.path.join(saida, 'acervo_resumos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Pronto em', saida)
    for p in pastas:
        print('  %-10s %4d vídeos, %5d trechos de fala' % (p, n_idx[p], n_tr[p]))


if __name__ == '__main__':
    main()
