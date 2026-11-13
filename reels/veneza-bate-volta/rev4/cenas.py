"""REV4 · cenas, legenda, gancho, efeitos e posições → props.json (rodar de dentro de rev4, depois de preparar.py).

Pedidos do Diego (13/11/2026) que este arquivo resolve:
- legenda em caixa normal (maiúscula só no começo da frase e nos nomes), karaokê mantido;
- nada aparece antes de ser dito: cada palavra da legenda, do gancho e dos rótulos entra no início dela
  (tempo do alinhamento forçado; a REV3 tinha rótulos presos à palavra errada, ex.: "5 €" em "São");
- nada no rosto: posição da legenda calculada pelo rosto medido em cada take; na tela dividida o rosto fica a
  42% da metade de baixo (FORMATOS_REELS 2), longe da interface do Instagram; a placa da CTA vai abaixo do queixo.
Regras de montagem mantidas da REV2: troca de imagem no mesmo quadro de um corte da gravação ou a ≥ 0,5 s dele;
nada gravado pelo Diego (acervo, rosto em tela cheia) por menos de 2 s.
"""
import json
import re

import numpy as np

base = json.load(open("base.json"))
P = base["palavras"]
DUR = base["dur"]
CORTES = base["cortes"]
FPS = 30


def norm(w):
    return re.sub(r"[^\wà-üç%-]", "", w.lower())


def idx(take, w, n=1):
    k = 0
    for i, p in enumerate(P):
        if p["take"] == take and norm(p["w"]) == norm(w):
            k += 1
            if k == n:
                return i
    raise KeyError((take, w, n))


def s(take, w, n=1):
    return P[idx(take, w, n)]["s"]


def e(take, w, n=1):
    return P[idx(take, w, n)]["e"]


def rot(take, palavras):
    """Rótulo que entra palavra por palavra: [(texto, take, palavra falada, ocorrência)] → [{txt, t}]."""
    return [{"txt": txt, "t": round(s(take, w, n), 3)} for txt, w, n in palavras]


J = [c["ini"] for c in CORTES[1:]]          # cortes da gravação na linha do tempo final
JT = {(CORTES[k]["take"], CORTES[k + 1]["take"]): CORTES[k + 1]["ini"] for k in range(len(CORTES) - 1)}
SENTA = 100 / FPS                            # o Diego cai na cadeira no quadro 100 da gravação (A1 começa em 0)

C = [
    # gancho: Palácio Ducal lotado em cima, Diego embaixo, texto do gancho palavra por palavra
    dict(ini=0.0, fim=SENTA, tipo="video", src="ducale_lotado.mp4", zoom=[1.0, 1.06], foco=0.9),
    # senta · "Em partes."
    dict(ini=SENTA, fim=JT[("A1", "A2")], tipo="diego", zoom=[1.0, 1.03]),
    # "Veneza recebe quase 30 milhões de pessoas no ano,"
    dict(ini=JT[("A1", "A2")], fim=s("A2", "sendo") - 0.05, tipo="graf", graf="milhoes", src="praca_lotada.mp4", foco=0.9,
         dados={"quase": s("A2", "quase"), "n30": s("A2", "30"), "milhoes": s("A2", "milhões"),
                "rot": rot("A2", [("DE", "de", 1), ("PESSOAS", "pessoas", 1), ("NO", "no", 1), ("ANO", "ano,", 1)])}),
    # "sendo que três em cada quatro desses visitantes vão de bate-volta."
    dict(ini=s("A2", "sendo") - 0.05, fim=s("A2", "Por") - 0.05, tipo="graf", graf="tres4",
         dados={"t3": s("A2", "três"), "tp": s("A2", "desses") - 0.05, "tb": s("A2", "bate-volta."),
                "rot": rot("A2", [("3", "três", 1), ("EM", "em", 1), ("CADA", "cada", 1), ("4", "quatro", 1)])}),
    # "Por isso a cidade criou um pedágio pra quem vai e não dorme."
    dict(ini=s("A2", "Por") - 0.05, fim=JT[("A2", "A3")], tipo="graf", graf="pedagio",
         dados={"tped": s("A2", "pedágio"), "tvai": s("A2", "vai"), "tnao": s("A2", "não"), "tdorme": s("A2", "dorme.")}),
    # "São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar,"
    dict(ini=JT[("A2", "A3")], fim=J[2], tipo="graf", graf="precos",
         dados={"t5": s("A3", "cinco"), "tprog": s("A3", "programados,"), "tsao": s("A3", "são", 2) - 0.05,
                "t10": s("A3", "dez"),
                "hora": rot("A3", [("NA", "na", 1), ("HORA", "hora,", 1)]),
                "np": rot("A3", [("E", "e", 1), ("SE", "se", 1), ("NÃO", "não", 1), ("PAGAR?", "pagar,", 1)])}),
    # "multa pra doer no bolso, pai."  (o corte J[2] é a pausa tirada antes de "multa")
    dict(ini=J[2], fim=JT[("A3", "B1")], tipo="graf", graf="multa",
         dados={"tmulta": s("A3", "multa"),
                "rot": rot("A3", [("PRA", "pra", 2), ("DOER", "doer", 1), ("NO", "no", 1), ("BOLSO", "bolso,", 1)])}),
    # "Ou seja, Veneza quer que você fique na cidade."  Veneza à noite vista de um hotel
    dict(ini=JT[("A3", "B1")], fim=s("B1", "E") - 0.05, tipo="foto", src="salute_noite.jpg", zoom=[1.0, 1.1]),
    # "E eu fiquei por duas noites. | Não gostei. Não faça isso. | Não me leve a mal."  Diego inteiro
    dict(ini=s("B1", "E") - 0.05, fim=s("B2", "Veneza") - 0.05, tipo="diego", zoom=[1.0, 1.03]),
    # "Veneza de dia é o cenário de filme que você sempre sonhou. Mas à noite eu acho a cidade deserta."
    dict(ini=s("B2", "Veneza") - 0.05, fim=JT[("B2", "A7")], tipo="video", src="por_do_sol.mp4", src2="noite_luzes.mp4",
         tx=s("B2", "Mas") - 0.05, zoom=[1.0, 1.05]),
    # "Sim, Diego, eu vou fazer o quê? Vou pagar a taxa?" (P&B) + "Exatamente." (cor)
    dict(ini=JT[("B2", "A7")], fim=s("A8", "Você") - 0.05, tipo="diego", zoom=[1.0, 1.0]),
    # "Você vai incluir Verona no seu roteiro da Itália,"
    dict(ini=s("A8", "Você") - 0.05, fim=s("A8", "uma") - 0.05, tipo="foto", src="arena_verona.jpg", zoom=[1.0, 1.08],
         rotulo=rot("A8", [("VERONA", "Verona", 1)])),
    # "uma cidade que fica só uma hora e pouquinho de Veneza, e um dia você faz um bate-volta pra lá"
    dict(ini=s("A8", "uma") - 0.05, fim=s("A8", "e", 3) - 0.05, tipo="graf", graf="mapa",
         dados={"t1h": s("A8", "uma", 2), "te": s("A8", "e", 1), "tpouq": s("A8", "pouquinho"), "tde": s("A8", "de", 1),
                "tveneza": s("A8", "Veneza,"), "tbate": s("A8", "bate-volta")}),
    # "e no outro você conhece a cidade do Romeu e Julieta."
    dict(ini=s("A8", "e", 3) - 0.05, fim=JT[("A8", "A9")], tipo="foto", src="julieta_varanda.jpg", zoom=[1.0, 1.08],
         rotulo=rot("A8", [("ROMEU", "Romeu", 1), ("E", "e", 4), ("JULIETA", "Julieta.", 1)])),
    # "E no bolso?" (P&B) + "Aí que tá o macete. Quem dorme" (cor)
    dict(ini=JT[("A8", "A9")], fim=s("B3", "em") - 0.05, tipo="diego", zoom=[1.0, 1.0]),
    # "em Veneza já paga a taxa no valor da hospedagem."
    dict(ini=s("B3", "em") - 0.05, fim=s("B3", "Então") - 0.05, tipo="graf", graf="dorme",
         dados={"titulo": [{"txt": "QUEM", "t": 0}, {"txt": "DORME", "t": 0}] + rot("B3", [("EM", "em", 1), ("VENEZA", "Veneza", 1)]),
                "taxa": rot("B3", [("JÁ", "já", 1), ("PAGA", "paga", 1), ("A", "a", 1), ("TAXA", "taxa", 1)]),
                "valor": rot("B3", [("NO", "no", 1), ("VALOR", "valor", 1), ("DA", "da", 1), ("HOSPEDAGEM", "hospedagem.", 1)])}),
    # "Então ficar em Verona pode ser até 25% mais barato do que dormir na cidade dos canais."
    dict(ini=s("B3", "Então") - 0.05, fim=JT[("B3", "B4")], tipo="graf", graf="hospedagem",
         dados={"tverona": s("B3", "Verona"), "tcanais": s("B3", "dormir") - 0.1,
                "p25": rot("B3", [("ATÉ", "até", 1), ("25%", "25%", 1)]),
                "barato": rot("B3", [("MAIS", "mais", 1), ("BARATO", "barato", 1)]),
                "cidade": rot("B3", [("CIDADE", "cidade", 1), ("DOS", "dos", 1), ("CANAIS", "canais.", 1)])}),
    # "E reservar o pedágio quatro dias de antecedência, você paga só cinco euros. Eu vou deixar o link na legenda."
    dict(ini=JT[("B3", "B4")], fim=JT[("B4", "B5")], tipo="graf", graf="reserva",
         dados={"t4": s("B4", "quatro"), "t5": s("B4", "cinco"), "tlink": s("B4", "link"),
                "dias": rot("B4", [("DIAS", "dias", 1), ("DE", "de", 1), ("ANTECEDÊNCIA", "antecedência,", 1)]),
                "link": rot("B4", [("LINK", "link", 1), ("NA", "na", 1), ("LEGENDA ↓", "legenda.", 1)])}),
    # "Ah, Diego, mas eu quero dormir na cidade." (P&B) + "Durma e tire suas próprias conclusões." (cor)
    dict(ini=JT[("B4", "B5")], fim=s("B6", "Aí") - 0.05, tipo="diego", zoom=[1.0, 1.03]),
    # "Aí que tá a magia da viagem. Cada experiência toca a pessoa de uma maneira diferente."  fogos do Ano-Novo
    dict(ini=s("B6", "Aí") - 0.05, fim=JT[("B6", "A11")], tipo="video", src="fogos.mp4", zoom=[1.0, 1.06], foco=0.45),
    # CTA: Diego inteiro (sem tela dividida, sem zoom) + placa do DS abaixo do queixo
    dict(ini=JT[("B6", "A11")], fim=DUR + 0.5, tipo="diego", zoom=[1.0, 1.0]),
]
for c in C:
    c["ini"], c["fim"] = round(c["ini"], 3), round(c["fim"], 3)

# ---------------------------------------------------------------- conferências da montagem
for k, c in enumerate(C):
    assert c["fim"] > c["ini"], c
    if k:
        assert abs(C[k - 1]["fim"] - c["ini"]) < 1e-6, ("buraco", c)
    for j in J:  # troca de cena no corte (mesmo quadro) ou a ≥ 0,5 s
        dq = abs(round(c["ini"] * FPS) - round(j * FPS))
        assert dq == 0 or dq >= 15, f"troca a {dq} quadros de um corte: cena {k} em {c['ini']}"
    d = min(c["fim"], DUR) - c["ini"]
    if c["tipo"] in ("diego", "video"):
        assert d >= 1.95, f"cena gravada pelo Diego com {d:.2f} s: {k}"

# ---------------------------------------------------------------- posições pelo rosto
ROSTO = {"A": json.load(open("rosto_A.json")), "B": json.load(open("rosto_B.json"))}
ORIG_Y = 0.32 * 1920      # origem do zoom do Diego em tela cheia
CENTRO_DIVIDIDA = 900 + 0.42 * 1020   # rosto a 42% da metade de baixo (FORMATOS_REELS 2)
MEIA_LINHA = 37            # metade da altura da linha da legenda (Inter 800, 66 px × 1,1)
# Calibrado nos quadros (qa_rosto_apertos.jpg e qa_cta_queixo.jpg): a base da caixa do detector fica no queixo ou logo acima;
# barba ≈ base + 5% da altura da caixa. Cabelo ≈ topo − 22% da altura.


def rosto_janela(t0, t1):
    """Caixas do rosto entre t0 e t1 da linha do tempo final (quadros das gravações de cada trecho)."""
    out = []
    for c in CORTES:
        a = max(t0, c["ini"]); b = min(t1, c["fim"])
        if b <= a:
            continue
        s0 = c["q_in"] / FPS + (a - c["ini"]) - 0.1
        s1 = c["q_in"] / FPS + (b - c["ini"]) + 0.1
        out += [x[1:] for x in ROSTO[c["fonte"]] if s0 <= x[0] <= s1 and x[1] is not None and 250 < x[4] < 700]
    r = np.array(out)
    if len(r):  # descarta falso positivo (mão, objeto): caixa longe da posição típica do rosto no take
        ty, cx = np.median(r[:, 1]), np.median(r[:, 0] + r[:, 2] / 2)
        r = r[(np.abs(r[:, 1] - ty) < 220) & (np.abs(r[:, 0] + r[:, 2] / 2 - cx) < 320)]
    return r


def zoom_em(t):
    c = next((x for x in C if x["ini"] <= t < x["fim"]), C[-1])
    z = c.get("zoom", [1, 1])
    return z[0] + (z[1] - z[0]) * (t - c["ini"]) / max(0.01, c["fim"] - c["ini"])


for c in CORTES:
    r = rosto_janela(c["ini"], c["fim"])
    c["div_off"] = round(CENTRO_DIVIDIDA - 900 - float(np.median(r[:, 1] + r[:, 3] / 2)))   # tela dividida


def posicao_legenda(t0, t1):
    r = rosto_janela(t0, t1)
    if not len(r):
        return 1320, "sem rosto", None
    z = max(zoom_em(t0), zoom_em(t1))
    barba = ORIG_Y + (float((r[:, 1] + r[:, 3] * 1.05).max()) - ORIG_Y) * z
    cabelo = ORIG_Y + (float((r[:, 1] - 0.22 * r[:, 3]).min()) - ORIG_Y) * z
    abaixo = max(1320, barba + 30 + MEIA_LINHA)
    if abaixo + MEIA_LINHA <= 1440:
        return round(abaixo), "abaixo", round(barba)
    if cabelo - 30 - 2 * MEIA_LINHA >= 256:
        return round(cabelo - 30 - MEIA_LINHA), "acima", round(cabelo)
    return 1440 - MEIA_LINHA, "APERTO", round(barba)


# placa da CTA: abaixo da barba a partir de "me segue", base ≤ y 1440 (zona segura do DS)
PLACA_ALT = 2 * 28 + 36 * 1 + 12 + 128 * 0.9   # DS 2.1: padding 28 + rótulo 36 + 12 + destino 128 × 0,9 ≈ 219 px
cta_ini = round(s("A11", "me"), 3)    # a placa entra em "me segue" (REV3 entrava em "E se", antes da hora)
r_cta = rosto_janela(cta_ini, DUR)
# neste take a base da caixa coincide com a barba (conferido em resolução cheia no pior quadro, 62,37 s da
# gravação, em "toda semana": barba termina em y ≈ 1190; a placa em y 1220 fica 25–30 px abaixo)
barba_cta = float((r_cta[:, 1] + r_cta[:, 3]).max())
placa_y = int(min(1440 - PLACA_ALT, barba_cta + 30))
assert placa_y >= barba_cta + 20, ("placa encosta no queixo", placa_y, barba_cta)

# ---------------------------------------------------------------- legenda (grupos de 1–4 palavras, ≤ 24 caracteres)
FUNC = {"de", "da", "do", "dos", "das", "a", "o", "e", "que", "pra", "pros", "em", "no", "na", "um", "uma", "se", "por", "com",
        "à", "eu", "te", "me", "é", "ela", "só", "até", "cada", "sendo", "mas", "suas", "seu", "já", "quem", "você", "vou"}
LIM = 24
txt = lambda ids: " ".join(P[j]["w"] for j in ids)
grupos, g = [], []
for i, w in enumerate(P):
    novo_trecho = g and (P[g[-1]]["take"] != w["take"] or any(P[g[-1]]["e"] <= j <= w["s"] + 0.01 for j in J))
    if novo_trecho:
        grupos.append(g); g = []
    if g and len(txt(g + [i])) > LIM:
        k = len(g)
        while k > 1 and norm(P[g[k - 1]]["w"]) in FUNC:
            k -= 1
        grupos.append(g[:k]); g = g[k:]
    g.append(i)
    if w["w"][-1] in ".?!" or (w["w"][-1] == "," and len(txt(g)) >= 10) or len(g) >= 4 and norm(w["w"]) not in FUNC:
        grupos.append(g); g = []
if g:
    grupos.append(g)
assert sorted(i for x in grupos for i in x) == list(range(len(P)))
for gr in grupos:
    assert len(txt(gr)) <= 26, txt(gr)

# ---------------------------------------------------------------- gancho (caixa normal, palavra por palavra)
gancho = {"fim": SENTA, "linhas": [
    {"tam": 128, "palavras": rot("A1", [("Veneza", "Veneza", 1), ("não", "não", 1)])},
    {"tam": 160, "cor": "#FFD23F", "palavras": rot("A1", [("te", "te", 1), ("quer", "quer", 1), ("lá", "lá", 1)])},
    {"tam": 96, "palavras": rot("A1", [("e", "e", 1), ("dessa", "dessa", 1), ("vez", "vez", 1)])},
    {"tam": 96, "palavras": rot("A1", [("é", "é", 1), ("de", "de", 1), ("verdade.", "verdade.", 1)])},
]}

# ---------------------------------------------------------------- efeitos (kit PDX; ninguém ouviu: conferir no ouvido)
cena = {c.get("graf") or c.get("src") or c["tipo"] + str(k): c for k, c in enumerate(C)}
sfx = [
    {"t": s("A2", "30") - 0.03, "som": "impacto", "db": -6},
    {"t": s("A2", "desses") - 0.05, "som": "obturador", "db": -8},
    {"t": s("A2", "pedágio") - 0.03, "som": "impacto", "db": -8},
    {"t": s("A3", "cinco") - 0.05, "som": "obturador", "db": -9},
    {"t": s("A3", "dez") - 0.05, "som": "obturador", "db": -9},
    {"t": s("A3", "multa") - 0.02, "som": "impacto", "db": -5},
    {"t": s("B1", "E") - 1.0, "som": "riser", "db": -10},
    {"t": cena["mapa"]["ini"] + 0.3, "som": "swish", "db": -9},
    {"t": s("A8", "bate-volta") - 0.1, "som": "swish", "db": -9},
    {"t": s("B3", "taxa") - 0.03, "som": "impacto", "db": -9},
    {"t": s("B3", "25%") - 0.05, "som": "impacto", "db": -6},
    {"t": s("B4", "cinco") - 0.05, "som": "obturador", "db": -9},
]
sfx = sorted(sfx, key=lambda x: x["t"])
for x, y in zip(sfx, sfx[1:]):
    assert y["t"] - x["t"] >= 1.4, ("efeitos muito juntos", x, y)

# posição de cada grupo da legenda quando o Diego está em tela cheia (na dividida fica na costura, y 900)
gy, rel, lados = [], [], []
for k, gr in enumerate(grupos):
    t0 = P[gr[0]]["s"]
    t1 = min(P[grupos[k + 1][0]]["s"] if k + 1 < len(grupos) else DUR, P[gr[-1]]["e"] + 0.3)
    lados.append((t0, t1) + posicao_legenda(t0, t1))
for take in {P[gr[0]]["take"] for gr in grupos}:
    ks = [k for k, gr in enumerate(grupos) if P[gr[0]]["take"] == take]
    if any(lados[k][3] != "abaixo" for k in ks):   # algum grupo não cabe abaixo do queixo: o take todo vai acima
        r = rosto_janela(min(lados[k][0] for k in ks), max(lados[k][1] for k in ks))
        cabelo = float((r[:, 1] - 0.22 * r[:, 3]).min())
        y = round(cabelo - 30 - MEIA_LINHA)
        assert y - MEIA_LINHA >= 256, ("não cabe acima", take, y)
        for k in ks:
            lados[k] = lados[k][:2] + (y, "acima (take)", round(cabelo))
for k, gr in enumerate(grupos):
    t0, t1, y, lado, ref = lados[k]
    gy.append(y)
    cena_g = next(x for x in C if x["ini"] <= t0 + 0.01 < x["fim"])
    if cena_g["tipo"] == "diego" and not (t0 >= cta_ini):
        rel.append((round(t0, 2), txt(gr), y, lado, ref))
# a legenda sai no início do grupo que tem "me segue" (a placa ocupa o lugar dela e diz o mesmo que a fala)
leg_fim = round(min(P[gr[0]]["s"] for gr in grupos if any(P[i]["s"] >= cta_ini - 0.01 for i in gr)), 3)
cortes_props = [{"ini": c["ini"], "fim": c["fim"], "take": c["take"], "pb": c["pb"], "div_off": c["div_off"]} for c in CORTES]
props = {"dur": DUR, "palavras": P, "cenas": C, "grupos": grupos, "gy": gy, "gancho": gancho, "sfx": sfx, "cortes": cortes_props,
         "cta": {"ini": cta_ini, "placa_y": placa_y, "leg_fim": leg_fim}}
json.dump(props, open("props.json", "w"), ensure_ascii=False)

for c in C:
    print(f"{c['ini']:6.2f}-{c['fim']:6.2f} {min(c['fim'], DUR) - c['ini']:4.2f} {c['tipo']:5} {c.get('graf') or c.get('src') or ''}")
print("\nlegenda com o Diego em tela cheia (tempo, grupo, y do centro, lado, referência do rosto):")
for x in rel:
    print("  ", x)
print("tela dividida, deslocamento por trecho:", [(c["take"], c["div_off"]) for c in CORTES])
print("placa da CTA: y", placa_y, "→", round(placa_y + PLACA_ALT), "· barba máx. depois de \"me segue\":", round(barba_cta), "· entra em", cta_ini, "s")
print("grupos:", len(grupos), "· maior:", max((txt(g) for g in grupos), key=len))
