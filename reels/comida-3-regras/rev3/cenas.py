"""REV3 · cenas, legenda, efeitos e posições → props.json (rodar de dentro de rev3, depois de preparar.py).

Regras deste Reel (pedidos do Diego, 16/11/2026):
- gancho: prato do bouillon (Paris) em cima, ele embaixo, sem animação na frente da comida (só a legenda na costura);
- "Bora que eu vou te mostrar": ele em tela cheia; depois volta a tela dividida;
- "E nas outras refeições, rapaz, vai ficar sem comer?" em preto e branco, em tela cheia; a resposta volta à cor;
- toda imagem, animação ou texto fica pelo menos 2,5 s na tela; acervo nunca além da duração do plano (sem câmera lenta);
- nada aparece antes de ser dito; nada na frente do rosto (posição pelo rosto medido em cada trecho).
Regras de montagem herdadas de Veneza REV4: troca de imagem no mesmo quadro de um corte da gravação ou a ≥ 0,5 s dele.
"""
import json
import re

import numpy as np

base = json.load(open("base.json"))
P = base["palavras"]
DUR = base["dur"]
CORTES = base["cortes"]
FPS = 30
MIN_CENA = 2.5


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


def rot(take, palavras):
    """Rótulo que entra palavra por palavra: [(texto, palavra falada, ocorrência)] → [{txt, t}]."""
    return [{"txt": txt, "t": round(s(take, w, n), 3)} for txt, w, n in palavras]


J = [c["ini"] for c in CORTES[1:]]


def junto(t):
    """O corte da gravação mais próximo de t (para a troca de imagem cair no mesmo quadro do corte)."""
    j = min(J, key=lambda x: abs(x - t))
    return j if abs(j - t) < 0.5 else t

JT = {(CORTES[k]["take"], CORTES[k + 1]["take"]): CORTES[k + 1]["ini"] for k in range(len(CORTES) - 1)}
INI = {c["take"]: c["ini"] for c in reversed(CORTES)}   # início de cada take na linha do tempo final

# duração de cada plano do acervo (o preparo corta assim; a cena não pode passar disso)
CLIPE = {"prato_bouillon2.mp4": 3.62, "paella.mp4": 3.17, "prato_bouillon.mp4": 4.04, "supermercado.mp4": 4.00,
         "restaurante_madrid.mp4": 3.60, "jantar_bruxelas.mp4": 4.40, "almoco_madrid.mp4": 3.50, "febo.mp4": 4.50,
         "falafel.mp4": 3.80, "albert_cuyp.mp4": 5.00}
VERT = 1080 / 1920   # planos verticais (9:16)
HORIZ = 1920 / 1080  # planos horizontais (16:9)

# Gancho (REV2, pedido do Diego em 17/11/2026): metade no prato do bouillon (Paris), metade na paella (Barcelona), com a
# legenda normal (karaokê na costura) até "restaurantes?"; ele só vai para a tela cheia depois da pergunta.
# Sem texto grande: a 1ª versão da REV2 (pergunta em letras garrafais) foi recusada por ele.
FIM_GANCHO = JT[("T1", "T2")]
TROCA = s("T1", "e", 1) - 0.05          # "…nas suas viagens | e ainda assim conhecer bons restaurantes?"
assert TROCA <= CLIPE["prato_bouillon2.mp4"] and FIM_GANCHO - TROCA <= CLIPE["paella.mp4"]
gancho = {"fim": 0.0, "paginas": []}

C = [
    # gancho, 1ª metade: "Você quer saber como economizar com a alimentação nas suas viagens" — prato do bouillon, Paris
    dict(ini=0.0, fim=TROCA, tipo="video", src="prato_bouillon2.mp4", dados={"ar": HORIZ}),
    # gancho, 2ª metade: "e ainda assim conhecer bons restaurantes?" — paella, Barcelona
    dict(ini=TROCA, fim=FIM_GANCHO, tipo="video", src="paella.mp4", dados={"ar": HORIZ}),
    # "Bora que eu vou te mostrar três formas que eu uso pra não gastar uma nota com comida durante a viagem."  (inteiro)
    dict(ini=FIM_GANCHO, fim=JT[("T2", "T3")], tipo="diego"),
    # "A primeira coisa é economizar no café da manhã. Se não tá incluso no hotel,"
    dict(ini=JT[("T2", "T3")], fim=s("T3", "a", 2) - 0.05, tipo="graf", graf="cafe",
         dados={"t1": s("T3", "primeira"), "thotel": s("T3", "hotel,"), "tincluso": s("T3", "incluso"),
                "cafe": rot("T3", [("CAFÉ", "café", 1), ("DA", "da", 1), ("MANHÃ", "manhã.", 1)]),
                "incluso": rot("T3", [("NÃO", "não", 1), ("TÁ", "tá", 1), ("INCLUSO", "incluso", 1)])}),
    # "a gente passa no supermercado e compra algumas coisas para comer no quarto mesmo."  (Albert Heijn, Amsterdam)
    dict(ini=s("T3", "a", 2) - 0.05, fim=JT[("T3", "T4")], tipo="video", src="supermercado.mp4", dados={"ar": HORIZ}),
    # "O que sobra para comprar na rua é só um menorzinho de toda manhã que não pode faltar, né?"  (foto do café, Florença)
    dict(ini=JT[("T3", "T4")], fim=JT[("T4", "T5")], tipo="foto", src="cafe_eataly.jpg", dados={"foco": "50% 64%"}),
    # "Segunda, escolha uma refeição pra gastar um pouco mais no restaurante."  (restaurante italiano, Madrid)
    dict(ini=JT[("T4", "T5")], fim=s("T5", "Geralmente") - 0.05, tipo="video", src="restaurante_madrid.mp4", dados={"ar": HORIZ},
         rotulo=rot("T5", [("SEGUNDA", "Segunda,", 1)])),
    # "Geralmente escolhemos o jantar porque é mais no final do dia, a gente já fez tudo e pode comer com calma."  (Bruxelas)
    dict(ini=s("T5", "Geralmente") - 0.05, fim=JT[("T5", "T6")], tipo="video", src="jantar_bruxelas.mp4", dados={"ar": HORIZ}),
    # "Mas quem define? Seu roteiro. Se tem algum restaurante que vale a pena ir na hora do"  (almoço em Madrid)
    dict(ini=JT[("T5", "T6")], fim=s("T6", "almoço") - 0.05, tipo="video", src="almoco_madrid.mp4", dados={"ar": HORIZ}),
    # "almoço por conta de uma vista ou experiência do lugar, aí você inverte."  (cartões almoço × jantar)
    dict(ini=s("T6", "almoço") - 0.05, fim=JT[("T6", "T7")], tipo="graf", graf="inverte",
         dados={"troteiro": s("T6", "roteiro."), "talmoco": s("T6", "almoço"), "tinverte": s("T6", "inverte."),
                "quem": rot("T6", [("QUEM", "quem", 1), ("DEFINE?", "define?", 1)]),
                "roteiro": rot("T6", [("SEU", "Seu", 1), ("ROTEIRO", "roteiro.", 1)]),
                "almoco": rot("T6", [("ALMOÇO", "almoço", 1)]),
                "vista": rot("T6", [("VISTA", "vista", 1), ("OU", "ou", 1), ("EXPERIÊNCIA", "experiência", 1)]),
                "inv": rot("T6", [("⇄ INVERTE", "inverte.", 1)])}),
    # "E nas outras refeições, rapaz, vai ficar sem comer?" (P&B) + "Claro que não." (cor)  — ele inteiro
    dict(ini=JT[("T6", "T7")], fim=s("T8", "Você") - 0.05, tipo="diego"),
    # "Você vai comer alguma comida de rua, algum lanche rápido, algo mais simples que vai te fazer gastar menos."  (FEBO)
    dict(ini=s("T8", "Você") - 0.05, fim=junto(s("T8", "E") - 0.05), tipo="video", src="febo.mp4", dados={"ar": HORIZ}),
    # "E eu te garanto que isso vai fazer parte de sua experiência conhecendo o local."  (falafel em Madrid)
    dict(ini=junto(s("T8", "E") - 0.05), fim=JT[("T8", "T9a")], tipo="video", src="falafel.mp4", dados={"ar": HORIZ}),
    # "A terceira dica é só definir uma média de quanto você quer gastar por dia com comida na viagem."  (REV3, arquivo editado)
    dict(ini=JT[("T8", "T9a")], fim=JT[("T9a", "T9")], tipo="graf", graf="terceira",
         dados={"t3": s("T9a", "terceira"),
                "media": rot("T9a", [("UMA", "uma", 1), ("MÉDIA", "média", 1)]),
                "dia": rot("T9a", [("POR", "por", 1), ("DIA", "dia", 1)]),
                "comida": rot("T9a", [("COM", "com", 1), ("COMIDA", "comida", 1)])}),
    # "Por exemplo, vamos supor que você vai para a Europa e quer gastar 50 euros por dia com comida."
    dict(ini=JT[("T9a", "T9")], fim=s("T9", "Então") - 0.05, tipo="graf", graf="cinquenta",
         dados={"t50": s("T9", "50"),
                "supor": rot("T9", [("POR", "Por", 1), ("EXEMPLO,", "exemplo,", 1), ("VAMOS", "vamos", 1), ("SUPOR", "supor", 1)]),
                "europa": rot("T9", [("EUROPA", "Europa", 1)]),
                "dia": rot("T9", [("POR", "por", 2), ("DIA", "dia", 1), ("COM", "com", 1), ("COMIDA", "comida.", 1)])}),
    # "Então você vai usar esse valor pra balancear suas refeições de acordo com a dica número 2."
    dict(ini=s("T9", "Então") - 0.05, fim=JT[("T9", "T9b")], tipo="graf", graf="balanca",
         dados={"tbal": s("T9", "balancear"), "tdica": s("T9", "dica"),
                "valor": rot("T9", [("ESSE", "esse", 1), ("VALOR", "valor", 1)])}),
    # "Mas não é pra você ficar noiado com isso. É só pra você ter uma média e não perder o controle dos gastos durante a
    #  viagem."  (REV3, arquivo editado) — Diego e Marina com o sanduíche no Albert Cuyp, Amsterdam
    dict(ini=JT[("T9", "T9b")], fim=JT[("T9b", "T10")], tipo="video", src="albert_cuyp.mp4", dados={"ar": HORIZ}),
    # "Economizar com comida não é comer mal, é você saber onde gastar e onde não gastar."  (o prato do gancho, de cima)
    dict(ini=JT[("T9b", "T10")], fim=JT[("T10", "T11")], tipo="video", src="prato_bouillon.mp4", foco=0.3, dados={"ar": VERT}),
    # CTA: ele inteiro + placa do DS abaixo do queixo
    dict(ini=JT[("T10", "T11")], fim=DUR + 0.5, tipo="diego"),
]
for c in C:
    c["ini"], c["fim"] = round(c["ini"], 3), round(c["fim"], 3)

# ---------------------------------------------------------------- conferências da montagem
avisos = []
for k, c in enumerate(C):
    assert c["fim"] > c["ini"], c
    if k:
        assert abs(C[k - 1]["fim"] - c["ini"]) < 1e-6, ("buraco", c)
    for j in J:
        dq = abs(round(c["ini"] * FPS) - round(j * FPS))
        if not (dq == 0 or dq >= 15):
            avisos.append(f"troca a {dq} quadros de um corte: cena {k} em {c['ini']}")
    d = min(c["fim"], DUR) - c["ini"]
    if d < MIN_CENA - 0.05:
        avisos.append(f"cena {k} ({c.get('graf') or c.get('src') or c['tipo']}) com {d:.2f} s (< 2,5 s)")
    if c["tipo"] == "video":
        assert d <= CLIPE[c["src"]] + 1e-3, f"cena {k} ({c['src']}) com {d:.2f} s passa do plano ({CLIPE[c['src']]} s)"

# ---------------------------------------------------------------- posições pelo rosto
ROSTO = {k: json.load(open(f"rosto_{k}.json")) for k in ("A", "B")}
CENTRO_DIVIDIDA = 900 + 0.42 * 1020
MEIA_LINHA = 37


def rosto_janela(t0, t1):
    out = []
    for c in CORTES:
        a = max(t0, c["ini"]); b = min(t1, c["fim"])
        if b <= a:
            continue
        s0 = c["q_in"] / FPS + (a - c["ini"]) - 0.1
        s1 = c["q_in"] / FPS + (b - c["ini"]) + 0.1
        out += [x[1:] for x in ROSTO[c["fonte"]] if s0 <= x[0] <= s1 and x[1] is not None and 250 < x[4] < 760]
    r = np.array(out)
    if len(r):
        ty, cx = np.median(r[:, 1]), np.median(r[:, 0] + r[:, 2] / 2)
        r = r[(np.abs(r[:, 1] - ty) < 220) & (np.abs(r[:, 0] + r[:, 2] / 2 - cx) < 320)]
    return r


FOLGA_COSTURA = 50   # o topo do rosto fica pelo menos 50 px abaixo da base da legenda da costura (y 937)


def topos(r):
    """Topo do rosto com filtro de mediana de 3 amostras (uma caixa isolada fora do lugar não conta)."""
    y = r[:, 1]
    return np.array([np.median(y[max(0, i - 1):i + 2]) for i in range(len(y))]) if len(y) else y


for c in CORTES:
    r = rosto_janela(c["ini"], c["fim"])
    centro = round(CENTRO_DIVIDIDA - 900 - float(np.median(r[:, 1] + r[:, 3] / 2)))
    minimo = round(937 + FOLGA_COSTURA - 900 - float(topos(r).min()))
    c["div_off"] = max(centro, minimo)


def posicao_legenda(t0, t1):
    r = rosto_janela(t0, t1)
    if not len(r):
        return 1320, "sem rosto", None
    barba = float((r[:, 1] + r[:, 3] * 1.05).max())
    cabelo = float((r[:, 1] - 0.22 * r[:, 3]).min())
    abaixo = max(1320, barba + 30 + MEIA_LINHA)
    if abaixo + MEIA_LINHA <= 1440:
        return round(abaixo), "abaixo", round(barba)
    if cabelo - 30 - 2 * MEIA_LINHA >= 256:
        return round(cabelo - 30 - MEIA_LINHA), "acima", round(cabelo)
    return 1440 - MEIA_LINHA, "APERTO", round(barba)


# placa da CTA: abaixo da barba a partir de "me segue", base ≤ y 1440 (zona segura do DS)
PLACA_ALT = 2 * 28 + 36 * 1 + 12 + 128 * 0.9
cta_ini = round(s("T11", "me"), 3)
r_cta = rosto_janela(cta_ini, DUR)
barba_cta = float((r_cta[:, 1] + r_cta[:, 3] * 1.05).max())
placa_y = int(min(1440 - PLACA_ALT, barba_cta + 30))
if placa_y < barba_cta + 20:
    avisos.append(f"placa encosta no queixo: placa {placa_y}, barba {barba_cta:.0f}")

# ---------------------------------------------------------------- legenda (grupos de 1–4 palavras, ≤ 24 caracteres)
FUNC = {"de", "da", "do", "dos", "das", "a", "o", "e", "que", "pra", "para", "em", "no", "na", "um", "uma", "se", "por", "com",
        "à", "eu", "te", "me", "é", "só", "até", "mas", "suas", "seu", "sua", "já", "quem", "você", "vou", "vai", "algum",
        "alguma", "algumas", "esse", "não", "nas", "mais"}
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

# ---------------------------------------------------------------- efeitos (kit PDX; ninguém ouviu: conferir no ouvido)
cena = {c.get("graf") or c.get("src") or c["tipo"] + str(k): c for k, c in enumerate(C)}
sfx = [
        {"t": s("T6", "inverte.") - 0.05, "som": "swish", "db": -8},
    {"t": s("T9", "50") - 0.03, "som": "impacto", "db": -6},
    {"t": s("T9", "dica") - 0.05, "som": "obturador", "db": -9},
]
sfx = sorted(sfx, key=lambda x: x["t"])
for x, y in zip(sfx, sfx[1:]):
    assert y["t"] - x["t"] >= 1.4, ("efeitos muito juntos", x, y)

# posição de cada grupo da legenda quando ele está em tela cheia (na dividida fica na costura, y 900)
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
        if y - MEIA_LINHA < 256:
            avisos.append(f"legenda não cabe acima no take {take} (y {y})")
        for k in ks:
            lados[k] = lados[k][:2] + (y, "acima (take)", round(cabelo))
for k, gr in enumerate(grupos):
    t0, t1, y, lado, ref = lados[k]
    if next(x for x in C if x["ini"] <= t0 + 0.01 < x["fim"])["tipo"] == "grafcheio":
        y = 1320
    gy.append(y)
    cena_g = next(x for x in C if x["ini"] <= t0 + 0.01 < x["fim"])
    if cena_g["tipo"] == "diego" and not (t0 >= cta_ini):
        rel.append((round(t0, 2), txt(gr), y, lado, ref))
leg_fim = round(min(P[gr[0]]["s"] for gr in grupos if any(P[i]["s"] >= cta_ini - 0.01 for i in gr)), 3)
cortes_props = [{"ini": c["ini"], "fim": c["fim"], "take": c["take"], "fonte": c["fonte"], "pb": c["pb"], "div_off": c["div_off"]} for c in CORTES]
props = {"dur": DUR, "palavras": P, "cenas": C, "gancho": gancho, "grupos": grupos, "gy": gy, "sfx": sfx, "cortes": cortes_props,
         "cta": {"ini": cta_ini, "placa_y": placa_y, "leg_fim": leg_fim}}
json.dump(props, open("props.json", "w"), ensure_ascii=False)

for c in C:
    print(f"{c['ini']:6.2f}-{c['fim']:6.2f} {min(c['fim'], DUR) - c['ini']:4.2f} {c['tipo']:5} {c.get('graf') or c.get('src') or ''}")
print("\nlegenda com ele em tela cheia (tempo, grupo, y do centro, lado, referência do rosto):")
for x in rel:
    print("  ", x)
print("tela dividida, deslocamento por trecho:", [(c["take"], c["div_off"]) for c in CORTES])
print("placa da CTA: y", placa_y, "→", round(placa_y + PLACA_ALT), "· barba máx. depois de \"me segue\":", round(barba_cta), "· entra em", cta_ini, "s")
print("grupos:", len(grupos), "· maior:", max((txt(g) for g in grupos), key=len))
print("\nAVISOS:" if avisos else "\nsem avisos")
for a in avisos:
    print("  ", a)
