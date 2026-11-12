"""REV1 · cenas, grupos de legenda, gancho e efeitos → props.json (rodar de dentro de rev1)."""
import json

base = json.load(open("base.json"))
P = base["palavras"]
DUR = base["dur"]


def s(i):  # início da palavra i
    return P[i]["s"]


# Cenas na linha do tempo final (s). Troca 0,04–0,12 s antes da palavra (FORMATOS_REELS 7.1).
C = [
    dict(ini=0.0, fim=2.86, tipo="video", src="lotada.mp4", zoom=[1.0, 1.06]),               # gancho
    dict(ini=2.86, fim=s(13) - 0.08, tipo="diego", zoom=[1.0, 1.04]),                        # senta na cadeira · "Em partes."
    dict(ini=s(13) - 0.08, fim=s(22) - 0.06, tipo="graf", graf="milhoes"),                   # 30 milhões
    dict(ini=s(22) - 0.06, fim=s(28) - 0.06, tipo="graf", graf="tres4", dados={"t3": s(24)}),  # três em cada quatro
    dict(ini=s(28) - 0.06, fim=s(39) - 0.1, tipo="graf", graf="print", dados={"t2": s(30)}),  # print Fortune (80%)
    dict(ini=s(39) - 0.1, fim=s(46) - 0.06, tipo="graf", graf="pedagio"),                    # pedágio
    dict(ini=s(46) - 0.06, fim=s(64) - 0.06, tipo="graf", graf="precos", dados={"t10": s(52) - 0.04}),
    dict(ini=s(64) - 0.06, fim=s(70) - 0.04, tipo="graf", graf="multa"),
    dict(ini=s(70) - 0.04, fim=s(83) - 0.04, tipo="video", src="gondolas.mp4"),              # "não é que Veneza não te quer lá"
    dict(ini=s(83) - 0.04, fim=s(95) - 0.04, tipo="video", src="rialto.mp4", zoom=[1.0, 1.06]),  # "ela quer… durma na cidade"
    dict(ini=s(95) - 0.04, fim=27.66, tipo="diego", zoom=[1.0, 1.09]),                         # "E eu fiquei, e não gostei"
    dict(ini=27.66, fim=s(111) - 0.06, tipo="video", src="canal_dia.mp4"),                    # "fazer tudo em um dia"
    dict(ini=s(111) - 0.06, fim=31.72, tipo="video", src="noite_laguna.mp4", zoom=[1.08, 1.02]),  # "à noite… deserta" (trecho vazio)
    dict(ini=31.72, fim=s(139) - 0.04, tipo="diego", zoom=[1.0, 1.07]),                         # "suja… Sim, Diego… taxa?"
    dict(ini=s(139) - 0.04, fim=s(149) - 0.06, tipo="foto", src="Arena_di_Verona.jpg", zoom=[1.0, 1.08]),  # "incluir Verona"
    dict(ini=s(149) - 0.06, fim=s(169) - 0.06, tipo="graf", graf="mapa"),                     # "1 hora e pouquinho"
    dict(ini=s(169) - 0.06, fim=s(176) - 0.06, tipo="foto", src="Ponte_Pietra_Verona.jpg", zoom=[1.08, 1.0]),
    dict(ini=s(176) - 0.06, fim=s(180) - 0.04, tipo="foto", src="Casa_di_Giulietta_Verona.jpg", zoom=[1.0, 1.1]),  # Romeu e Julieta
    dict(ini=s(180) - 0.04, fim=s(200) - 0.06, tipo="graf", graf="barato", dados={"t25": s(190) - 0.04}),
    dict(ini=s(200) - 0.06, fim=s(222) - 0.06, tipo="graf", graf="reserva", dados={"t5": s(212) - 0.04, "tLink": s(219) - 0.06}),
    dict(ini=s(222) - 0.06, fim=DUR + 1, tipo="video", src="campanile.mp4"),                  # CTA
]
for c in C:
    c["ini"] = round(c["ini"], 3)
    c["fim"] = round(c["fim"], 3)

# grupos de legenda: 1–4 palavras, ≤ 24 caracteres, uma linha; quebra em pontuação; não termina em palavra
# funcional; número fica com a unidade ("30 milhões", "25% mais", "cinco euros")
FUNC = {"de", "da", "do", "dos", "das", "a", "o", "e", "que", "pra", "pros", "em", "no", "na", "um", "uma", "se", "por", "com", "à", "eu", "te", "me", "é", "ela", "só", "até", "30", "25%", "cinco", "dez", "quatro", "três", "cada", "sendo"}
LIM = 24
grupos, g = [], []
txt = lambda ids: " ".join(P[j]["w"] for j in ids)
for i, w in enumerate(P):
    if g and len(txt(g + [i])) > LIM:
        # recua até a última palavra não funcional
        k = len(g)
        while k > 1 and P[g[k - 1]]["w"].lower().strip(".,?!") in FUNC:
            k -= 1
        grupos.append(g[:k]); g = g[k:]
    g.append(i)
    if w["w"][-1] in ".,?!" or len(g) >= 4 and w["w"].lower().strip(".,?!") not in FUNC:
        grupos.append(g); g = []
if g: grupos.append(g)
# ajustes manuais de leitura (índices de palavra)
AJUSTE = [[22, 23], [24, 25, 26, 27], [28, 29], [30, 31, 32], [40, 41, 42], [43, 44, 45], [59, 60, 61, 62, 63],
          [113, 114], [115, 116], [117, 118, 119], [120, 121], [128, 129], [183, 184, 185, 186], [187, 188], [189, 190, 191, 192], [193, 194, 195]]
for aj in AJUSTE:
    grupos = [x for x in grupos if not set(x) & set(aj)]
    sobra = []
grupos += AJUSTE
cob = set(i for x in grupos for i in x)
for i in range(len(P)):
    if i not in cob:
        grupos.append([i])
grupos = sorted(grupos, key=lambda x: x[0])
# palavras soltas que perderam o grupo viram grupo próprio; une sozinhos vizinhos sem pontuação
assert sorted(i for x in grupos for i in x) == list(range(len(P))), "grupos inconsistentes"
# o gancho já é o texto: palavras 0–10 sem legenda (gancho escrito); "Em partes." tem legenda
gancho = [{
    "fim": 2.86,
    "linhas": [
        {"txt": "VENEZA NÃO", "t": s(0), "tam": 128},
        {"txt": "TE QUER LÁ", "t": s(2), "tam": 160, "cor": "#E0AE5C"},
        {"txt": "E DESSA VEZ", "t": s(5), "tam": 96},
        {"txt": "É DE VERDADE.", "t": s(8), "tam": 96},
    ],
}]

sfx = [
    {"t": s(17) - 0.05, "som": "impacto", "db": -6},
    {"t": s(24) - 0.03, "som": "obturador", "db": -8},
    {"t": s(39) - 0.1, "som": "swish", "db": -8},
    {"t": s(47) - 0.03, "som": "obturador", "db": -9},
    {"t": s(64) - 0.05, "som": "impacto", "db": -5},
    {"t": s(95) - 1.0, "som": "riser", "db": -10},
    {"t": s(149) + 0.25, "som": "swish", "db": -8},
    {"t": s(190) - 0.05, "som": "impacto", "db": -6},
    {"t": s(212) - 0.05, "som": "obturador", "db": -9},
]

props = {"dur": round(DUR, 3), "palavras": P, "cenas": C, "grupos": grupos, "gancho": gancho, "sfx": sfx, "cta": {"ini": round(s(222) - 0.06, 3)}}
json.dump(props, open("props.json", "w"), ensure_ascii=False)
for c in C:
    print(f"{c['ini']:6.2f}-{c['fim']:6.2f} {c['fim']-c['ini']:4.2f} {c['tipo']:5} {c.get('src') or c.get('graf') or ''}")
print(len(grupos), "grupos;", " | ".join(" ".join(P[j]["w"] for j in gg) for gg in grupos[:12]))
