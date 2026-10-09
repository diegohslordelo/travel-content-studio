#!/usr/bin/env python3
"""Resume os dados públicos de research/dados/ (coletados em 08/10/2026).

Rode de dentro de research/:  python3 scripts/resumir_benchmark.py
Entrada : dados/videos_youtube_2026-10-08.tsv, dados/shorts_youtube_2026-10-08.tsv,
          dados/shorts_amostra_2026-10-08.tsv
Saída   : dados/benchmark_youtube_2026-10-08.tsv e um texto no terminal.

Só lê arquivos locais. Idades vêm de textos como "há 2 meses" e são aproximadas
(1 mês = 30 dias, 1 ano = 365). Não há dado privado."""
import csv
import re
import statistics as st

INSCRITOS = {  # lidos na página pública de cada canal em 08/10/2026
    "Diego Berlitz": ("BR", "104 mil", 104e3), "Estevam Pelo Mundo": ("BR", "2,29 mi", 2.29e6),
    "Alemanizando": ("BR", "255 mil", 255e3), "Leo e Fabi": ("BR", "279 mil", 279e3),
    "Marina Guaragna": ("BR", "477 mil", 477e3), "Trip Partiu": ("BR", "657 mil", 657e3),
    "GetOutside (Ale & Duda)": ("BR", "524 mil", 524e3), "Três Viagens": ("BR", "241 mil", 241e3),
    "Viagem Pra Dois": ("BR", "1,49 mil", 1.49e3), "Drew Binsky": ("INT", "7,47 mi", 7.47e6),
    "Kara and Nate": ("INT", "4,54 mi", 4.54e6), "Lost LeBlanc": ("INT", "2,29 mi", 2.29e6),
    "Fearless & Far": ("INT", "3,11 mi", 3.11e6), "Sorelle Amore": ("INT", "1,01 mi", 1.01e6),
}
CHEGADA = re.compile(r"CHEGAMOS|CHEGUEI|PRIMEIR|24 ?H|24 HORAS|48 ?H|72 ?H|FIRST (DAY|24|48|72|IMPRESS)", re.I)


def views(s):
    s = s.replace("visualizações", "").replace("de ", "").strip()
    m = re.match(r"([\d.,]+)\s*(mil|mi)?", s)
    if not m:
        return None
    n, suf = m.groups()
    if suf:
        x = float(n.replace(",", "."))
    elif re.match(r"^\d{1,3}(\.\d{3})+$", n):
        x = float(n.replace(".", ""))
    else:
        x = float(n.replace(",", "."))
    return x * {"mil": 1e3, "mi": 1e6, None: 1}[suf]


def idade_dias(s):
    m = re.match(r"há\s+(\d+)\s+(\w+)", s)
    if not m:
        return None
    n, u = int(m.group(1)), m.group(2)
    unidade = {"h": 1 / 24, "dia": 1, "dias": 1, "sem": 7, "mês": 30, "meses": 30, "ano": 365, "anos": 365}
    return n * unidade[u] if u in unidade else None


def minutos(s):
    if not re.match(r"^\d+(:\d+)+$", s):
        return None
    t = 0
    for x in s.split(":"):
        t = t * 60 + int(x)
    return t / 60


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


videos = {}
for r in ler("dados/videos_youtube_2026-10-08.tsv"):
    v, i, d = views(r["views_texto"]), idade_dias(r["publicado_texto"]), minutos(r["duracao"])
    if v is None or i is None or d is None or d < 8:  # só vídeos longos (>= 8 min)
        continue
    videos.setdefault(r["canal"], []).append((r["titulo_exibido"], v, i, d))

shorts = {}
for r in ler("dados/shorts_youtube_2026-10-08.tsv"):
    v = views(r["views_texto"])
    if v is not None:
        shorts.setdefault(r["canal"], []).append(v)

saida = []
razoes = []
for canal, (pais, txt, n_insc) in INSCRITOS.items():
    vs = videos.get(canal, [])
    if len(vs) < 3:
        continue
    med = st.median(v for _, v, _, _ in vs)
    janela = max(i for _, _, i, _ in vs)
    por_mes = len(vs) / janela * 30 if janela else None
    sh = shorts.get(canal, [])
    cheg = [v for t, v, _, _ in vs if CHEGADA.search(t)]
    if len(vs) >= 8:
        razoes += [v / med for v in cheg]
    saida.append({
        "canal": canal, "pais": pais, "inscritos": txt, "n_videos_longos": len(vs),
        "mediana_views": round(med), "views_sobre_inscritos": round(med / n_insc, 3),
        "mediana_duracao_min": round(st.median(d for *_, d in vs), 1),
        "pct_30min_ou_mais": round(sum(1 for *_, d in vs if d >= 30) / len(vs), 2),
        "janela_dias": round(janela), "longos_por_mes_aprox": round(por_mes, 1) if por_mes else "",
        "n_shorts": len(sh), "mediana_views_shorts": round(st.median(sh)) if sh else "",
        "n_chegada_24h": len(cheg),
    })

with open("dados/benchmark_youtube_2026-10-08.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0].keys()), delimiter="\t")
    w.writeheader()
    w.writerows(saida)

for r in saida:
    print(" | ".join(str(x) for x in r.values()))
print("\nRazão mediana (vídeos de chegada/24h ÷ mediana do canal): %.2f (n=%d)" % (st.median(razoes), len(razoes)))

amostra = [float(r["visualizacoes"]) for r in ler("dados/shorts_amostra_2026-10-08.tsv")]
q = st.quantiles(amostra, n=4)
print("Amostra de Shorts: n=%d mediana=%.0f p25=%.0f p75=%.0f >=10k=%.1f%% >=100k=%.1f%% >=1M=%.1f%%" % (
    len(amostra), st.median(amostra), q[0], q[2],
    100 * sum(x >= 1e4 for x in amostra) / len(amostra), 100 * sum(x >= 1e5 for x in amostra) / len(amostra),
    100 * sum(x >= 1e6 for x in amostra) / len(amostra)))
