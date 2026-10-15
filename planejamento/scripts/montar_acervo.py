"""Monta o acervo de conteúdo do repositório a partir dos arquivos consolidados do Colab.

Entrada:  acervo_indice.tsv, acervo_transcricoes.tsv, acervo_resumos.json (de consolidar_analises.py)
Saída:    <raiz>/acervo/<cidade>/{indice.tsv, transcricoes.tsv, linha_do_tempo.md}, acervo/INDICE_GERAL.md, acervo/CORTES_DE_CUSTO.md

Uso (de dentro de planejamento/scripts/):
    python3 montar_acervo.py --entrada PASTA_COM_OS_3_ARQUIVOS --saida ../../acervo
"""
import argparse, csv, json, os, re
from collections import defaultdict

VALOR = re.compile(r'€|\beuros?\b|\breais\b|R\$|\bbarat|\bcaro\b|\bcara\b|\bcaros\b|pre[çc]o|custou|custo|ingresso|bilhete|gratuit|gr[áa]tis|\bpagu|\bpago\b|\bconta\b|\bdeu \d|\d+ ?(euros?|reais)', re.I)
GUID = re.compile(r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-|^[0-9a-f]{32}\.|^ScreenRecording', re.I)
DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']


def dia_semana(d):
    import datetime
    try:
        return DIAS[datetime.date.fromisoformat(d).weekday()]
    except Exception:
        return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--entrada', required=True)
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()
    ent, saida = os.path.abspath(a.entrada), os.path.abspath(a.saida)
    idx = list(csv.DictReader(open(os.path.join(ent, 'acervo_indice.tsv'), encoding='utf-8', newline=''), delimiter='\t'))
    trs = list(csv.DictReader(open(os.path.join(ent, 'acervo_transcricoes.tsv'), encoding='utf-8', newline=''), delimiter='\t'))
    rp = os.path.join(ent, 'acervo_resumos.json')
    resumos = json.load(open(rp, encoding='utf-8')).get('resumos', {}) if os.path.isfile(rp) else {}
    fala = defaultdict(list)
    for t in trs:
        fala[(t['pasta'], t['arquivo'])].append(t)
    por_pasta = defaultdict(list)
    for r in idx:
        por_pasta[r['pasta']].append(r)
    os.makedirs(saida, exist_ok=True)
    cortes, geral = [], []
    for pasta, rows in sorted(por_pasta.items()):
        d = os.path.join(saida, pasta.lower().replace('ç', 'c').replace('ã', 'a'))
        os.makedirs(d, exist_ok=True)
        rows.sort(key=lambda r: (r.get('cidade_detectada') or '', r.get('criado') or '', r['arquivo']))
        cols = [c for c in rows[0].keys() if c != 'pasta']
        with open(os.path.join(d, 'indice.tsv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n')
            w.writerow(cols)
            for r in rows:
                w.writerow([r[c] for c in cols])
        with open(os.path.join(d, 'transcricoes.tsv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n')
            w.writerow(['arquivo', 'inicio_s', 'fim_s', 'texto', 'prob_sem_fala'])
            for r in rows:
                for t in fala[(pasta, r['arquivo'])]:
                    w.writerow([t['arquivo'], t['inicio_s'], t['fim_s'], t['texto'], t['prob_sem_fala']])
        # linha do tempo
        L = ['# %s · linha do tempo do acervo' % pasta, '',
             'Gerado de `indice.tsv` e `transcricoes.tsv` (Colab, faster-whisper "small"). **A transcrição é automática e ninguém ouviu o áudio**: nomes de lugares e de pessoas saem deturpados. A hora é a do arquivo (fuso do local). Arquivos com nome de código são exportações: a data é a da exportação. 💲 = fala com possível valor/preço (fica fora de peças, ver `../CORTES_DE_CUSTO.md`).', '']
        rs = resumos.get(pasta, {})
        if rs:
            L += ['Análise: %s vídeos, %s s, GPU %s, %s erros.' % (rs.get('total_com_resultado'), rs.get('segundos'), rs.get('gpu'), len(rs.get('erros', []))), '']
        grupos = defaultdict(list)
        for r in rows:
            grupos[((r.get('cidade_detectada') or ''), (r.get('criado') or '')[:10])].append(r)
        sub = ''
        for (cid, dia), grp in sorted(grupos.items()):
            if cid != sub:
                sub = cid
                if cid:
                    L += ['## Cidade detectada: %s' % cid, '']
            tempo = sum(float(r['dur_s'] or 0) for r in grp)
            L += ['### %s %s · %d vídeos · %.0f min' % (dia or 'sem data no arquivo', dia_semana(dia), len(grp), tempo / 60), '',
                  '| Hora | Arquivo | Dur. | Fala (automática) |', '|---|---|---:|---|']
            for r in grp:
                ft = fala[(pasta, r['arquivo'])]
                txt = ' '.join(t['texto'] for t in ft if float(t['prob_sem_fala'] or 0) < 0.6).strip()
                flag = ''
                for t in ft:
                    if VALOR.search(t['texto']):
                        flag = ' 💲'
                        cortes.append((pasta, r['arquivo'], t['inicio_s'], t['fim_s'], t['texto']))
                nome = r['arquivo'] + (' ⚠ exportação' if GUID.match(r['arquivo']) else '')
                extra = ''
                if r.get('cidade_origem') in ('hora', 'pasta'):
                    extra = ' [cidade por %s]' % r['cidade_origem']
                L.append('| %s | %s%s | %s s | %s%s |' % ((r.get('criado') or '')[11:16], nome, extra, r['dur_s'],
                                                          (txt[:170] + '…') if len(txt) > 170 else txt, flag))
            L.append('')
        open(os.path.join(d, 'linha_do_tempo.md'), 'w', encoding='utf-8').write('\n'.join(L))
        dias = sorted({(r.get('criado') or '')[:10] for r in rows if not GUID.match(r['arquivo']) and (r.get('criado') or '')[:10]})
        geral.append((pasta, len(rows), sum(float(r['dur_s'] or 0) for r in rows) / 60, sum(1 for r in rows if fala[(pasta, r['arquivo'])]),
                      sum(1 for r in rows if GUID.match(r['arquivo'])), dias[0] if dias else '', dias[-1] if dias else ''))
    G = ['# Acervo de conteúdo · índice geral', '',
         'Base de acervo do projeto, gerada da análise do Colab em 15/10/2026 (`scripts/consolidar_analises.py` e `scripts/montar_acervo.py`). Cada pasta tem `indice.tsv` (metadados por vídeo), `transcricoes.tsv` (fala automática com tempo) e `linha_do_tempo.md` (dia a dia). Os vídeos e as folhas de contato ficam no Drive (`Youtube/<cidade>` e `Youtube/analise/<cidade>`); o repositório guarda só texto.', '',
         '| Cidade | Vídeos | Minutos gravados | Com fala | Exportações (data não confiável) | Primeiro dia | Último dia |', '|---|---:|---:|---:|---:|---|---|']
    for p, n, mi, cf, ex, d0, d1 in geral:
        G.append('| [%s](%s/linha_do_tempo.md) | %d | %.0f | %d | %d | %s | %s |' % (p, p.lower().replace('ç', 'c').replace('ã', 'a'), n, mi, cf, ex, d0, d1))
    G += ['', 'Limites: a transcrição não foi ouvida por ninguém; só algumas folhas de contato foram vistas por mim (ver `planejamento/DECUPAGEM_*.md`); a Itália foi separada por cidade pelo GPS do vídeo (ou subpasta, ou hora do vizinho: `[cidade por hora]` é palpite).']
    open(os.path.join(saida, 'INDICE_GERAL.md'), 'w', encoding='utf-8').write('\n'.join(G) + '\n')
    C = ['# Cortes de custo · trechos com fala de valor, preço ou "grátis"', '',
         'Lista automática (palavras-chave) de falas que podem conter valor. **Regra desta revisão:** nenhum valor em peça futura (`planejamento/OPORTUNIDADES_CUSTOS.md`). Estes trechos ficam fora dos cortes. A lista pode ter falso positivo (ex.: "caro" como adjetivo) e pode **não** pegar todos os valores: a transcrição erra números.', '',
         '| Cidade | Arquivo | De (s) | Até (s) | Fala |', '|---|---|---:|---:|---|']
    for p, f, i, j, t in cortes:
        C.append('| %s | %s | %s | %s | %s |' % (p, f, i, j, t.replace('|', '/')))
    open(os.path.join(saida, 'CORTES_DE_CUSTO.md'), 'w', encoding='utf-8').write('\n'.join(C) + '\n')
    print('acervo em', saida, '·', len(geral), 'cidades ·', len(cortes), 'falas com possível valor')


if __name__ == '__main__':
    main()
