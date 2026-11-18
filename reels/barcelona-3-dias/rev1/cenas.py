"""REV1 · cenas, legenda, gancho, marcador de dia, efeitos → props.json (rodar de dentro de rev1, depois de voz.py).

Regras do pedido (Diego, 17/11/2026) conferidas aqui:
- cada imagem cai na palavra que mostra (troca 0,06 s antes do início da palavra, FORMATOS_REELS 7.1);
- nenhum vídeo repetido (assert);
- nada gravado pelo Diego em tela cheia por menos de MIN_TAKE s (a não ser dentro de composição: grade ou divisão);
- legenda karaokê de 1–4 palavras (≤ 24 caracteres), nada antes de ser dito; DS só no CTA.
"""
import json
import re

V = json.load(open("voz.json"))
P = V["palavras"]
DUR = V["dur"]
TAKES = json.load(open("takes.json"))
ANT = 0.06       # a imagem troca um pouco antes da palavra
MIN_TAKE = 1.6   # menor duração aceitável de um take em tela cheia (a meta é ≥ 2 s)


def norm(w):
    return re.sub(r"[^\wà-üç%-]", "", w.lower())


def idx(w, n=1, depois=0.0):
    k = 0
    for i, p in enumerate(P):
        if p["s"] >= depois and norm(p["w"]) == norm(w):
            k += 1
            if k == n:
                return i
    raise KeyError((w, n, depois))


def s(w, n=1, depois=0.0):
    return P[idx(w, n, depois)]["s"]


def c(w, n=1, depois=0.0):
    """Instante de corte para a imagem que mostra a palavra w."""
    return round(s(w, n, depois) - ANT, 3)


def rot(itens, depois=0.0):
    """[(texto exibido, palavra falada)] → [{txt, t}] (cada parte entra quando é dita)."""
    return [{"txt": txt, "t": round(s(w, 1, depois), 3)} for txt, w in itens]


def clip(nome):
    return f"{nome}.mp4"


T3 = s("Nosso", 1, 9.0)  # "Nosso primeiro dia…" (o 1º "nosso" é "o nosso roteiro")
T5 = s("O", 1, 22.0)     # "O dia 2…"
T7 = s("Nosso", 1, 45.0) # "Nosso terceiro dia…"

C = [
    # gancho: "Barcelona acaba com os viajantes que não montam um roteiro com estratégia."
    dict(ini=0.0, fim=c("Nós"), tipo="video", src=clip("gancho"), zoom=[1.0, 1.08]),
    # "Nós fomos passar 3 dias em uma das cidades mais desejadas da Europa"
    dict(ini=c("Nós"), fim=c("e", 1, 7.0), tipo="video", src=clip("tres_dias"), zoom=[1.0, 1.06],
         rotulo=rot([("3", "3"), ("DIAS", "dias")]), rotuloY=640),
    # "e foi assim que organizamos o nosso roteiro. Nosso primeiro dia em Barcelona, deixamos os pontos turísticos mais distantes."
    dict(ini=c("e", 1, 7.0), fim=c("Começamos"), tipo="mapa",
         dados={"rotas": s("organizamos"), "destaque": 0, "tDestaque": T3, "barcelona": s("Barcelona,", 1, 9.5), "distantes": s("distantes.")}),
    # "Começamos pelo Camp Nou, depois Montjuïc, que infelizmente não teve o"
    dict(ini=c("Começamos"), fim=c("show"), tipo="split", src=clip("camp_nou"), srcB=clip("montjuic"),
         tB=c("Montjuïc,"), tC=c("que", 1, 13.8)),
    # "show das fontes da data que estávamos lá."  (Palau Nacional/MNAC, o "castelo", com a escadaria da Font Màgica)
    dict(ini=c("show"), fim=c("Pausa"), tipo="video", src=clip("fonte")),
    # "Pausa pro Mequizão"
    dict(ini=c("Pausa"), fim=c("Colombo"), tipo="video", src=clip("mequi")),
    # "e depois partimos pra ver Colombo e a Barceloneta."
    dict(ini=c("Colombo"), fim=c("Parque"), tipo="split", src=clip("colombo"), srcB=clip("barceloneta"),
         tB=c("Barceloneta."), tC=c("Fechamos")),
    # "Fechamos o dia com Parque da Cidadela e Arco do Triunfo. O dia 2 foi focado em história."
    dict(ini=c("Parque"), fim=c("Nos"), tipo="split", src=clip("cidadela"), srcB=clip("arco"),
         tB=c("Arco"), tC=c("Triunfo.") + 0.25),
    # "Nos hospedamos no bairro Gràcia e logo ali já tinha a"
    dict(ini=c("Nos"), fim=c("Casa"), tipo="video", src=clip("gracia")),
    # "Casa Vicens, a primeira de Gaudí."
    dict(ini=c("Casa"), fim=c("Depois", 1, 27.0), tipo="video", src=clip("vicens")),
    # "Depois fomos para o bairro Gótico,"
    dict(ini=c("Depois", 1, 27.0), fim=c("Muro"), tipo="video", src=clip("gotico")),
    # "passamos pelo Muro do Beijo, Ponte do Bispo, Catedral, Praça Real e até que chegamos na"
    dict(ini=c("Muro"), fim=c("e", 1, 32.0), tipo="grade", tiles=[
        {"src": clip("beijo"), "t": s("Muro") - 0.04, "nome": rot([("Muro", "Muro"), ("do", "do"), ("Beijo", "Beijo,")], 29.0)},
        {"src": clip("ponte_bispo"), "t": s("Ponte") - 0.04, "nome": rot([("Ponte", "Ponte"), ("do", "do"), ("Bispo", "Bispo,")], 30.0)},
        {"src": clip("catedral"), "t": s("Catedral,") - 0.04, "nome": rot([("Catedral", "Catedral,")])},
        {"src": clip("praca_real"), "t": s("Praça") - 0.04, "nome": rot([("Praça", "Praça"), ("Real", "Real")])},
    ]),
    # "e até que chegamos na La Rambla, que estava toda em obra."
    dict(ini=c("e", 1, 32.0), fim=c("Lá", 1, 34.0), tipo="video", src=clip("rambla")),
    # "Lá mesmo fica o Mercado de La Boqueria,"
    dict(ini=c("Lá", 1, 34.0), fim=c("que", 1, 36.5), tipo="video", src=clip("boqueria")),
    # "que passamos só pra ver, pra não doer no bolso,"
    dict(ini=c("que", 1, 36.5), fim=c("e", 1, 38.5), tipo="video", src=clip("boqueria_precos")),
    # "e depois partimos pra Passeig de Gràcia, a rua das compras."
    dict(ini=c("e", 1, 38.5), fim=c("A", 1, 41.4), tipo="video", src=clip("passeig")),
    # "A Casa Batlló e Milà, famosas de Gaudí, ficam por lá, mas não entramos."
    dict(ini=c("A", 1, 41.4), fim=c("Nosso", 1, 45.0), tipo="split", src=clip("batllo"), srcB=clip("mila"),
         tB=c("Milà,"), tC=c("famosas")),
    # "Nosso terceiro dia foi exclusivamente reservado para"  (o mapa volta com a rota do dia 3 em destaque)
    dict(ini=c("Nosso", 1, 45.0), fim=c("pro", 1, 47.0), tipo="mapa",
         dados={"rotas": 0.0, "destaque": 2, "tDestaque": T7, "distantes": s("exclusivamente")}),
    # "pro dono da cidade, Gaudí."
    dict(ini=c("pro", 1, 47.0), fim=c("Finalmente"), tipo="retrato", src="gaudi_1878.jpg"),
    # "Finalmente chegamos na Sagrada Família"
    dict(ini=c("Finalmente"), fim=round(s("passamos", 1, 50.0), 3), tipo="video", src=clip("sagrada_fora")),
    # "passamos a manhã inteira lá. A energia desse lugar é inexplicável." (a floresta de colunas entra em "passamos")
    dict(ini=round(s("passamos", 1, 50.0), 3), fim=c("Paramos"), tipo="video", src=clip("sagrada_dentro"), zoom=[1.0, 1.1], mergulhoEntra=0.45),
    # "Paramos para comer um bom churros e fomos passar a tarde no"
    dict(ini=c("Paramos"), fim=c("Parque", 1, 57.0), tipo="video", src=clip("churros")),
    # "Parque Güell. A energia de Barcelona é realmente diferente,"
    dict(ini=c("Parque", 1, 57.0), fim=c("os", 1, 60.0), tipo="video", src=clip("guell")),
    # "os 3 dias foram suficientes para a gente sentir isso."
    dict(ini=c("os", 1, 60.0), fim=c("Salva"), tipo="video", src=clip("vista")),
    # CTA (DS): "Salva esse roteiro se Barcelona estiver nos seus planos."
    dict(ini=c("Salva"), fim=DUR, tipo="video", src=clip("final"), zoom=[1.02, 1.08]),
]
# mergulho: a fachada da Sagrada "puxa" para dentro (zoom através do portal) nos últimos 0,4 s
sf = next(x for x in C if x.get("src") == clip("sagrada_fora"))
sf["mergulhoSai"] = {"t": round(sf["fim"] - 0.4, 3), "x": TAKES["sagrada_fora"].get("portal_x", 0.5), "y": TAKES["sagrada_fora"].get("portal_y", 0.55)}

# ---------------------------------------------------------------- conferências
for a, b in zip(C, C[1:]):
    assert abs(a["fim"] - b["ini"]) < 1e-6, ("buraco entre cenas", a, b)
for x in C:
    assert x["fim"] - x["ini"] > 0.8, ("cena curta ou invertida", x)
    if x["tipo"] == "split":
        assert x["ini"] < x["tB"] < x["tC"] < x["fim"], ("divisão fora de ordem", x)
    for tl in x.get("tiles", []):
        assert x["ini"] <= tl["t"] + 0.05 < x["fim"], ("quadro da grade fora da cena", x)
usados = []
for x in C:
    for k in ("src", "srcB"):
        if x.get(k, "").endswith(".mp4"):
            usados.append(x[k])
    for tl in x.get("tiles", []):
        usados.append(tl["src"])
assert len(usados) == len(set(usados)), ("vídeo repetido", [u for u in usados if usados.count(u) > 1])
for u in usados:
    nome = u[:-4]
    assert nome in TAKES, ("take sem definição", nome)
# duração de cada take x tempo de tela (o clipe precisa durar o tempo que fica na tela)
tela = {}
for x in C:
    if x["tipo"] == "video":
        tela[x["src"]] = x["fim"] - x["ini"]
    if x["tipo"] == "split":
        tela[x["src"]] = x["tC"] + 0.38 - x["ini"]
        tela[x["srcB"]] = x["fim"] - x["tB"]
    for tl in x.get("tiles", []):
        tela[tl["src"]] = x["fim"] - tl["t"]
curtos, curtos_dur = [], []
for u, d in tela.items():
    nome = u[:-4]
    if TAKES[nome]["dur"] < round(d + 0.034, 3):   # 1 quadro de folga a 30 qps
        curtos_dur.append((nome, TAKES[nome]["dur"], round(d + 0.05, 2)))
assert not curtos_dur, ("takes mais curtos que o tempo de tela (nome, dur, precisa)", curtos_dur)
for x in C:
    if x["tipo"] == "video" and x["fim"] - x["ini"] < MIN_TAKE:
        curtos.append((x["src"], round(x["fim"] - x["ini"], 2)))

# ---------------------------------------------------------------- legenda (grupos de 1–4 palavras, ≤ 24 caracteres)
FUNC = {"de", "da", "do", "dos", "das", "a", "o", "os", "e", "que", "pra", "pro", "em", "no", "na", "nos", "um", "uma", "se",
        "por", "com", "para", "pra", "pelo", "já", "só", "até", "mas", "esse", "desse", "seus"}
LIM = 24
txt = lambda ids: " ".join(P[j]["w"] for j in ids)
grupos, g = [], []
for i, w in enumerate(P):
    if g and (P[g[-1]]["take"] != w["take"] or w["s"] - P[g[-1]]["e"] > 0.35):
        grupos.append(g); g = []
    if g and len(txt(g + [i])) > LIM:
        k = len(g)
        while k > 1 and norm(P[g[k - 1]]["w"]) in FUNC:
            k -= 1
        grupos.append(g[:k]); g = g[k:]
    g.append(i)
    if w["w"][-1] in ".?!" or (w["w"][-1] == "," and len(txt(g)) >= 8) or (len(g) >= 4 and norm(w["w"]) not in FUNC):
        grupos.append(g); g = []
if g:
    grupos.append(g)
assert sorted(i for x in grupos for i in x) == list(range(len(P)))
for gr in grupos:
    assert len(txt(gr)) <= 26, txt(gr)

# ---------------------------------------------------------------- gancho (as palavras da 1ª frase, em linhas)
g0 = [i for i, p in enumerate(P) if p["take"] == 1]
assert txt(g0) == "Barcelona acaba com os viajantes que não montam um roteiro com estratégia.", txt(g0)
gancho = {"fim": C[0]["fim"], "linhas": [
    {"tam": 128, "palavras": g0[0:2]},     # Barcelona acaba (≈ 853 px: termina antes de x 944)
    {"tam": 104, "palavras": g0[2:5]},     # com os viajantes
    {"tam": 104, "palavras": g0[5:8]},     # que não montam
    {"tam": 104, "palavras": g0[8:11]},    # um roteiro com
    {"tam": 150, "palavras": g0[11:12]},   # estratégia.
]}

# ---------------------------------------------------------------- marcador do dia (entra quando o dia é dito)
dias = [{"t": round(s("primeiro"), 3), "txt": "DIA 1"}, {"t": round(s("2"), 3), "txt": "DIA 2"},
        {"t": round(s("terceiro"), 3), "txt": "DIA 3"}]

# ---------------------------------------------------------------- efeitos (kit PDX; ninguém ouviu: conferir no ouvido)
cena = {}
for x in C:
    cena.setdefault(x.get("src") or x["tipo"], x)
sfx = [
    {"t": s("3") - 0.03, "som": "impacto", "db": -6},
    {"t": cena["mapa"]["ini"] + 0.05, "som": "swish", "db": -8},
    {"t": dias[0]["t"] - 0.02, "som": "obturador", "db": -10},
    {"t": cena[clip("camp_nou")]["tB"] + 0.1, "s": 0, "som": "swish", "db": -10},
    {"t": dias[1]["t"] - 0.02, "som": "obturador", "db": -10},
    {"t": cena["grade"]["tiles"][0]["t"], "som": "pagina", "db": -10},
    {"t": cena[clip("batllo")]["tB"] + 0.1, "som": "swish", "db": -10},
    {"t": dias[2]["t"] - 0.02, "som": "obturador", "db": -10},
    # riser termina no corte do mergulho (PDX_riser tem 0,82 s); um efeito só, para respeitar 1 a cada 1,5 s
    {"t": round(cena[clip("sagrada_fora")]["fim"] - 0.82, 3), "som": "riser", "db": -8},
]
for x in sfx:
    x.pop("s", None)
sfx = sorted(sfx, key=lambda x: x["t"])
for a, b in zip(sfx, sfx[1:]):
    assert b["t"] - a["t"] >= 1.4, ("efeitos muito juntos", a, b)

cta = {"ini": round(s("Salva"), 3), "rotulo": "SE BARCELONA TIVER NOS SEUS PLANOS", "destino": "SALVA"}
props = {"dur": DUR, "palavras": [{"w": p["w"], "s": p["s"], "e": p["e"]} for p in P], "cenas": C, "grupos": grupos,
         "gancho": gancho, "dias": dias, "sfx": sfx, "cta": cta}
json.dump(props, open("props.json", "w"), ensure_ascii=False)

for x in C:
    extra = f" B {x['srcB']} em {x['tB']:.2f}, cheia {x['tC']:.2f}" if x["tipo"] == "split" else ""
    print(f"{x['ini']:6.2f}-{x['fim']:6.2f} {x['fim'] - x['ini']:4.2f} {x['tipo']:7} {x.get('src', '')}{extra}")
print("cenas", len(C), "· vídeos", len(usados), "· grupos de legenda", len(grupos), "· maior:", max((txt(g) for g in grupos), key=len))
print("takes em tela cheia abaixo de", MIN_TAKE, "s:", curtos)
