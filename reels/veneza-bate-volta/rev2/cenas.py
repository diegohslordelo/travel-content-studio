"""REV2 · cenas, legenda, gancho e efeitos → props.json (rodar de dentro de rev2).

Regra de montagem da REV2 (pedido do Diego, 13/11/2026: "cortes em frações de segundo estragam a fluidez"):
toda troca de imagem cai no MESMO quadro de um corte da gravação (lista J) ou a ≥ 0,5 s dele. Assim cada
mudança visual acontece uma vez só. Cenas de pelo menos ≈ 1,3 s; a maioria tem 2–4 s.
"""
import json

base = json.load(open("base.json"))
P = base["palavras"]
DUR = base["dur"]
FPS = 30


def s(i):  # início da palavra i (tempo medido no áudio final)
    return P[i]["s"]


def e(i):
    return P[i]["e"]


# Cortes no rosto do Diego na gravação decupada (quadro do 1º quadro depois do corte), medidos quadro a quadro
# (diferença entre quadros + conferência visual): 5 do próprio Diego (174, 837, 894, 1126, 1725) e 5 da limpeza
# de pausas da REV1 (428, 632, 1065, 1405, 1444).
J = [q / FPS for q in (174, 428, 632, 837, 894, 1065, 1126, 1405, 1444, 1725)]
J1, J2, J3, J4, J5, J6, J7, J8, J9, J10 = J

C = [
    # gancho: Palácio Ducal lotado + texto do gancho
    dict(ini=0.0, fim=3.15, tipo="video", src="ducale_lotado.mp4", zoom=[1.0, 1.06], foco=0.9),
    # Diego senta na cadeira · "Em partes."
    dict(ini=3.15, fim=J1, tipo="diego", zoom=[1.0, 1.04]),
    # "Veneza recebe quase 30 milhões de pessoas no ano": praça lotada + contador
    dict(ini=J1, fim=s(22) - 0.05, tipo="graf", graf="milhoes", src="praca_lotada.mp4", foco=0.9, dados={"tquase": s(15), "t30": s(16), "tpessoas": s(19)}),
    # "sendo que três em cada quatro desses visitantes vão de bate-volta": bonecos + print da Fortune
    dict(ini=s(22) - 0.05, fim=s(33) - 0.05, tipo="graf", graf="tres4", dados={"t3": s(24), "tp": s(28) - 0.05, "tb": s(30)}),
    # "Por isso a cidade criou um pedágio pra quem vai e não dorme."
    dict(ini=s(33) - 0.05, fim=J2, tipo="graf", graf="pedagio", dados={"tped": s(39), "tvai": s(42) - 0.05, "tdorme": s(44) - 0.05}),
    # "São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar,"
    dict(ini=J2, fim=s(64) - 0.08, tipo="graf", graf="precos", dados={"t5": s(47), "tprog": s(50), "tsao": s(51) - 0.05, "t10": s(52), "thora": s(57), "tnp": s(60) - 0.05}),
    # "multa pra doer no bolso, pai."
    dict(ini=s(64) - 0.08, fim=J3, tipo="graf", graf="multa", dados={"tbolso": s(66) - 0.05}),
    # "Ou seja, é que tá, não é que Veneza não te quer lá,"
    dict(ini=J3, fim=s(83) - 0.05, tipo="video", src="gondolas.mp4", zoom=[1.0, 1.06]),
    # "ela quer você lá e quer que você fique, durma na cidade.": Veneza à noite (Salute vista de um hotel)
    dict(ini=s(83) - 0.05, fim=s(95) - 0.04, tipo="foto", src="salute_noite.jpg", zoom=[1.0, 1.1]),
    # "E eu fiquei, e não gostei, não faça isso." Diego inteiro na tela até o fim de "isso"
    dict(ini=s(95) - 0.04, fim=J4, tipo="diego", zoom=[1.0, 1.03]),
    dict(ini=J4, fim=J5, tipo="diego", zoom=[1.12, 1.15]),   # corte da gravação → corte de zoom
    # "Você consegue fazer tudo em um dia, à noite a cidade fica deserta": dia → noite em dissolve
    dict(ini=J5, fim=s(117) - 0.04, tipo="video", src="canal_dia.mp4", src2="noite_luzes.mp4", tx=s(111) - 0.05, zoom=[1.0, 1.05]),
    # "e fica suja por causa da rebarba da galera do bate-volta." (sem imagem real de sujeira: Diego)
    dict(ini=s(117) - 0.04, fim=J6, tipo="diego", zoom=[1.0, 1.04]),
    # "Sim, Diego, eu vou fazer o quê? Vou pagar a taxa?" (ele faz o seguidor: corte de zoom)
    dict(ini=J6, fim=J7, tipo="diego", zoom=[1.12, 1.15]),
    # "Exatamente, você vai incluir Verona no seu roteiro da Itália,"
    dict(ini=J7, fim=s(149) - 0.05, tipo="foto", src="arena_verona.jpg", zoom=[1.0, 1.08], rotulo={"txt": "VERONA", "t": s(143) - 0.05}),
    # "uma cidade que fica só uma hora e pouquinho de Veneza, e um dia você faz um bate-volta pra lá"
    dict(ini=s(149) - 0.05, fim=s(169) - 0.05, tipo="graf", graf="mapa", dados={"thora": s(155) + 0.2, "tdeveneza": s(158), "tveneza": s(159), "tbate": s(164) - 0.1, "trotulo": s(166)}),
    # "e no outro você conhece a cidade do Romeu e Julieta."
    dict(ini=s(169) - 0.05, fim=J8, tipo="foto", src="julieta_varanda.jpg", zoom=[1.0, 1.08], rotulo={"txt": "ROMEU E JULIETA", "t": s(177) - 0.05}),
    # "E no bolso?"
    dict(ini=J8, fim=J9, tipo="diego", zoom=[1.10, 1.13]),
    # "Se hospedar em Verona pode ser até 25% mais barato do que ficar na cidade dos canais."
    dict(ini=J9, fim=s(200) - 0.05, tipo="graf", graf="hospedagem", dados={"tverona": s(186), "t25": s(190), "tmais": s(191), "tcanais": s(195) - 0.05, "tcidade": s(197)}),
    # "E se você reservar com quatro dias de antecedência, você paga só cinco euros na entrada, vou deixar o link na legenda."
    dict(ini=s(200) - 0.05, fim=J10, tipo="graf", graf="reserva", dados={"t4": s(205) - 0.05, "t5": s(212) - 0.05, "tlink": s(216) - 0.05}),
    # CTA: Diego inteiro (sem tela dividida) + placa do DS
    dict(ini=J10, fim=DUR + 0.5, tipo="diego", zoom=[1.0, 1.05]),
]
for c in C:
    c["ini"] = round(c["ini"], 3)
    c["fim"] = round(c["fim"], 3)

# conferências da regra de montagem
for k, c in enumerate(C):
    assert c["fim"] > c["ini"], c
    if k:
        assert abs(C[k - 1]["fim"] - c["ini"]) < 1e-6, ("buraco", c)
    for j in J:  # troca de cena no corte (mesmo quadro) ou a ≥ 0,5 s
        dq = abs(round(c["ini"] * FPS) - round(j * FPS))
        assert dq == 0 or dq >= 15, f"troca a {dq} quadros de um corte: cena {k} em {c['ini']}"

# legenda: grupos de 1–4 palavras, ≤ 24 caracteres (mesma regra e ajustes da REV1; índices iguais)
FUNC = {"de", "da", "do", "dos", "das", "a", "o", "e", "que", "pra", "pros", "em", "no", "na", "um", "uma", "se", "por", "com", "à", "eu", "te", "me", "é", "ela", "só", "até", "30", "25%", "cinco", "dez", "quatro", "três", "cada", "sendo"}
LIM = 24
txt = lambda ids: " ".join(P[j]["w"] for j in ids)
grupos, g = [], []
for i, w in enumerate(P):
    if g and len(txt(g + [i])) > LIM:
        k = len(g)
        while k > 1 and P[g[k - 1]]["w"].lower().strip(".,?!") in FUNC:
            k -= 1
        grupos.append(g[:k]); g = g[k:]
    g.append(i)
    if w["w"][-1] in ".,?!" or len(g) >= 4 and w["w"].lower().strip(".,?!") not in FUNC:
        grupos.append(g); g = []
if g:
    grupos.append(g)
AJUSTE = [[22, 23], [24, 25, 26, 27], [28, 29], [30, 31, 32], [40, 41, 42], [43, 44, 45], [59, 60, 61, 62, 63],
          [113, 114], [115, 116], [117, 118, 119], [120, 121], [128, 129], [183, 184, 185, 186], [187, 188], [189, 190, 191, 192], [193, 194, 195]]
for aj in AJUSTE:
    grupos = [x for x in grupos if not set(x) & set(aj)]
grupos += AJUSTE
cob = set(i for x in grupos for i in x)
grupos += [[i] for i in range(len(P)) if i not in cob]
grupos = sorted(grupos, key=lambda x: x[0])
assert sorted(i for x in grupos for i in x) == list(range(len(P)))

gancho = [{
    "fim": 3.15,
    "linhas": [
        {"txt": "VENEZA NÃO", "t": s(0), "tam": 128},
        {"txt": "TE QUER LÁ", "t": s(2), "tam": 160, "cor": "#E0AE5C"},
        {"txt": "E DESSA VEZ", "t": s(5), "tam": 96},
        {"txt": "É DE VERDADE.", "t": s(8), "tam": 96},
    ],
}]

cena = {c.get("graf") or c.get("src") or c["tipo"] + str(k): c for k, c in enumerate(C)}
sfx = [
    {"t": s(16) - 0.03, "som": "impacto", "db": -6},                      # "30 milhões" entra na tela
    {"t": s(28) - 0.05, "som": "obturador", "db": -8},                    # print da Fortune
    {"t": s(39) - 0.03, "som": "impacto", "db": -8},                     # "PEDÁGIO" carimba no bilhete
    {"t": s(47) - 0.05, "som": "obturador", "db": -9},                    # 5 €
    {"t": s(52) - 0.05, "som": "obturador", "db": -9},                    # 10 €
    {"t": cena["multa"]["ini"], "som": "impacto", "db": -5},              # MULTA
    {"t": s(95) - 1.0, "som": "riser", "db": -10},                        # sobe até "E eu fiquei"
    {"t": cena["mapa"]["ini"] + 0.3, "som": "swish", "db": -9},           # linha do trem
    {"t": s(164) - 0.1, "som": "swish", "db": -9},                        # trem do bate-volta
    {"t": s(190) - 0.05, "som": "impacto", "db": -6},                     # 25%
    {"t": s(212) - 0.05, "som": "obturador", "db": -9},                   # 5 € na entrada
]
sfx = sorted(sfx, key=lambda x: x["t"])
for a, b in zip(sfx, sfx[1:]):
    assert b["t"] - a["t"] >= 1.4, ("efeitos muito juntos", a, b)

props = {"dur": DUR, "palavras": P, "cenas": C, "grupos": grupos, "gancho": gancho, "sfx": sfx, "cta": {"ini": round(s(227) - 0.05, 3)}}
json.dump(props, open("props.json", "w"), ensure_ascii=False)
for c in C:
    print(f"{c['ini']:6.2f}-{c['fim']:6.2f} {c['fim'] - c['ini']:4.2f} {c['tipo']:5} {c.get('graf') or c.get('src') or ''}")
