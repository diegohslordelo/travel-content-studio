"""Leva os tempos de uma revisão (cenas.json) para a nova linha do tempo da voz, ancorando nas mesmas palavras
(alinhamento das duas transcrições; interpolação entre palavras). Uso: python3 scripts/remapear.py rev2 rev3"""
import json, re, sys, difflib, numpy as np
A, B = sys.argv[1], sys.argv[2]
wa = json.load(open(f"{A}/transcricao_alinhada.json")); wb = json.load(open(f"{B}/transcricao_alinhada.json"))
da = json.load(open(f"{A}/palavras.json"))["duracao"]; db_ = json.load(open(f"{B}/palavras.json"))["duracao"]
norm = lambda w: re.sub(r"[^\wÀ-ÿ]", "", w["w"].lower())
sm = difflib.SequenceMatcher(a=[norm(w) for w in wa], b=[norm(w) for w in wb], autojunk=False)
xa, xb = [0.0], [0.0]
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        s0, s1 = wa[blk.a + k]["s"], wb[blk.b + k]["s"]
        if s0 > xa[-1] and s1 > xb[-1]:
            xa.append(s0); xb.append(s1)
xa.append(da); xb.append(db_)
f = lambda t: round(float(np.interp(t, xa, xb)), 3)
C = json.load(open(f"{A}/cenas.json"))
for c in C["cenas"]:
    ini_a = c["ini"]
    c["ini"], c["fim"] = f(c["ini"]), f(min(c["fim"], da))
C["cenas"][-1]["fim"] = round(db_ + 0.07, 3)
for l in C["gancho"]["linhas"]:
    for w in l["palavras"]:
        w["em"] = f(w["em"])
C["gancho"]["fim"] = f(C["gancho"]["fim"])
if C.get("fitas"):
    C["fitas"]["fim"] = f(C["fitas"]["fim"]); C["fitas"]["entradas"] = [f(x) for x in C["fitas"]["entradas"]]
for x in C.get("textos", []):
    x["ini"], x["fim"] = f(x["ini"]), f(x["fim"])
    for l in x["linhas"]:
        if "em" in l: l["em"] = f(l["em"])
C["sem_legenda"] = [[f(a), f(b) if b < da else 60] for a, b in C["sem_legenda"]]
C["cta"]["ini"] = f(C["cta"]["ini"])
cmp_ = next(c for c in C["cenas"] if c["tipo"] == "comparar")
# marcos relativos à cena: comparar ("igual") e captura (troca título → trecho)
C2 = json.load(open(f"{A}/cenas.json"))
ca = next(c for c in C2["cenas"] if c["tipo"] == "comparar"); C["comparar"]["marco"] = round(f(ca["ini"] + C2["comparar"]["marco"]) - cmp_["ini"], 3)
cap_a = next(c for c in C2["cenas"] if c["tipo"] == "captura"); cap_b = next(c for c in C["cenas"] if c["tipo"] == "captura")
C["captura"]["troca"] = round(f(cap_a["ini"] + C2["captura"]["troca"]) - cap_b["ini"], 3)
json.dump(C, open(f"{B}/cenas.json", "w"), ensure_ascii=False, indent=1)
for c in C["cenas"]:
    print(f"{c['id']:16s} {c['ini']:6.2f}-{c['fim']:6.2f}  {c['fim']-c['ini']:.2f}")
print("comparar.marco", C["comparar"]["marco"], "captura.troca", C["captura"]["troca"], "cta", C["cta"]["ini"], "textos", [(x["ini"], x["fim"]) for x in C["textos"]])
