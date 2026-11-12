"""Monta rev1/props.json (composição ReelGTA) a partir de decupagem.json e rev1/cenas.json.
Também ajusta a duração de cada plano em rev1/clipes.json à duração da cena (+ 3 quadros de folga) e
grava rev1/sfx.json (efeitos e onde caem) para scripts/mixar.py.
Uso (de dentro de reels/gta6-miami): python3 scripts/montar.py"""
import json, re

FPS = 30
dec = json.load(open("decupagem.json"))
cfg = json.load(open("rev1/cenas.json"))
clipes = json.load(open("rev1/clipes.json"))

# palavras no tempo do Reel, com o trecho e a tomada
pals = []
trecho_ini = {}
cont_tom = {}
for s in dec["trechos"]:
    cont_tom[s["tomada"]] = cont_tom.get(s["tomada"], 0) + 1
    chave = f"{s['tomada']}.{cont_tom[s['tomada']]}"
    trecho_ini[chave] = s["out_q"][0] / FPS
    if cont_tom[s["tomada"]] == 1:
        trecho_ini[s["tomada"]] = s["out_q"][0] / FPS
    for w in s["palavras"]:
        pals.append(dict(w, tomada=s["tomada"]))
fim_fala = dec["quadros"] / FPS


def ancora(a: str, base_padrao=-0.07) -> float:
    m = re.fullmatch(r"([^+\-]*)([+\-][0-9.]+)?", a.strip())
    nome, desl = m.group(1), m.group(2)
    if nome in ("", "0"):
        return float(desl or 0)
    if re.fullmatch(r"T\d\d(\.\d)?", nome):
        return trecho_ini[nome] + float(desl or 0)
    w, n = (nome.split("#") + ["1"])[:2]
    oc = [p for p in pals if p["falado"] == w]
    if len(oc) < int(n):
        raise SystemExit(f"âncora não achada: {a}")
    return oc[int(n) - 1]["ini"] + (float(desl) if desl else base_padrao)


# cenas em quadros
cenas = []
inis = [round(ancora(c["ini"]) * FPS) if c["ini"] != "0" else 0 for c in cfg["cenas"]]
quadros = round((fim_fala + cfg["fim_apos_fala_s"]) * FPS)
dur_clipe = {}
luz = []
for i, c in enumerate(cfg["cenas"]):
    q0, q1 = inis[i], inis[i + 1] if i + 1 < len(inis) else quadros
    assert q1 > q0, c["id"]
    t0 = q0 / FPS
    e = {"id": c["id"], "tipo": c["tipo"], "ini_q": q0, "fim_q": q1}
    if c["tipo"] == "clipe":
        e["arquivo"] = f"clipes/{c['clipe']}.mp4"
        dur_clipe[c["clipe"]] = (q1 - q0 + 3) / FPS
    for k in ("arquivo", "anim", "fotos", "focos", "kb", "foco", "foco_fim", "zoom"):
        if k in c:
            e[k] = c[k]
    if "racha" in c:
        e["racha"] = round(ancora(c["racha"]) - t0, 3)
    if "marcos" in c:
        e["marcos"] = {k: round((ancora(v, 0) if not v.startswith("+") else t0 + float(v)) - t0, 3) for k, v in c["marcos"].items()}
    if c.get("luz"):
        luz.append(t0)
    cenas.append(e)
    print(f"{c['id']:14s} {t0:6.2f}–{q1 / FPS:6.2f} ({(q1 - q0) / FPS:4.2f} s) {e.get('marcos', '')}")

# planos: duração = cena + 3 quadros
for c in clipes["clipes"]:
    if c["id"] in dur_clipe:
        c["dur"] = round(dur_clipe[c["id"]], 3)
json.dump(clipes, open("rev1/clipes.json", "w"), ensure_ascii=False, indent=1)

# legendas
L = cfg["legenda"]
toks = []
i = 0
falas = [(p["falado"], p) for p in pals]
multi = sorted([k for k in L["escrita"] if " " in k], key=lambda k: -len(k.split()))
while i < len(pals):
    p = pals[i]
    feito = False
    for mw in multi:
        n = len(mw.split())
        if " ".join(x["falado"] for x in pals[i:i + n]) == mw and len({x["tomada"] for x in pals[i:i + n]}) == 1:
            toks.append({"t": L["escrita"][mw], "ini": p["ini"], "fim": pals[i + n - 1]["fim"], "tomada": p["tomada"], "f": mw})
            i += n
            feito = True
            break
    if feito:
        continue
    txt = L["troca_palavra"].get(f"{p['tomada']}:{p['falado']}", L["escrita"].get(p["falado"], p["falado"]))
    toks.append({"t": txt, "ini": p["ini"], "fim": p["fim"], "tomada": p["tomada"], "f": p["falado"]})
    i += 1

juntos = {tuple(j) for j in L["juntos"]}
# fim de frase: pontuação da transcrição de conferência (Whisper na voz já cortada) e mudança de tomada / pausa
conf = json.load(open("transcricao_conferencia.json"))  # Whisper na voz já cortada (scripts/transcrever.py)
pont = [w["e"] for s_ in conf for w in s_["words"] if w["w"][-1:] in ",.?!"]
for k, tk in enumerate(toks):
    prox = toks[k + 1] if k + 1 < len(toks) else None
    tk["fim_frase"] = prox is None or prox["tomada"] != tk["tomada"] or prox["ini"] - tk["fim"] > 0.35
for e in pont:  # cada pontuação marca só a palavra cujo fim está mais perto dela
    k = min(range(len(toks)), key=lambda j: abs(toks[j]["fim"] - e))
    if abs(toks[k]["fim"] - e) < 0.25:
        if k + 1 < len(toks) and (toks[k]["f"], toks[k + 1]["f"]) in juntos:
            k += 1  # nome composto (Miami Heat, Vice City): o fim de frase fica no 2º nome
        toks[k]["fim_frase"] = True
# divisão de custo mínimo (FORMATOS_REELS 6): grupo perto de ~16 caracteres, sem terminar em palavra funcional,
# sem atravessar fim de frase, sem separar nomes compostos
def custo(gr):
    txt = " ".join(x["t"] for x in gr)
    if len(gr) > L["max_palavras"] or (len(txt) > L["max_chars"] and len(gr) > 1):
        return 1e9
    c_ = (len(txt) - 16) ** 2 / 8
    if any(x["fim_frase"] for x in gr[:-1]):
        c_ += 400
    if gr[-1]["f"] in L["funcionais"] and not gr[-1]["fim_frase"]:
        c_ += 60
    return c_
n = len(toks)
best = [0.0] + [1e18] * n
de = [0] * (n + 1)
for j in range(1, n + 1):
    for i in range(max(0, j - L["max_palavras"]), j):
        if i > 0 and (toks[i - 1]["f"], toks[i]["f"]) in juntos:
            continue
        v = best[i] + custo(toks[i:j])
        if v < best[j]:
            best[j], de[j] = v, i
grupos = []
j = n
while j > 0:
    grupos.append(toks[de[j]:j])
    j = de[j]
grupos.reverse()

gancho_fim = round(inis[1] / FPS, 3)
num_ini, num_fim = cenas[[c["id"] for c in cenas].index("975_camera")]["ini_q"] / FPS, cenas[[c["id"] for c in cenas].index("banana")]["ini_q"] / FPS
destaques = [d.lower() for d in L["destaques"]]
legendas = []
for k, gr in enumerate(grupos):
    ini = gr[0]["ini"] - 0.05
    prox = grupos[k + 1][0]["ini"] - 0.05 if k + 1 < len(grupos) else fim_fala
    fim = min(prox, gr[-1]["fim"] + 0.6)
    pal = [{"texto": x["t"], "destaque": False} for x in gr]
    cand = [j for j, x in enumerate(gr) if x["t"].lower() in destaques]
    if " ".join(x["t"] for x in gr).lower().find("vice city") >= 0:
        cand = [j for j, x in enumerate(gr) if x["t"] in ("Vice", "City")] or cand
        for j in cand:
            pal[j]["destaque"] = True
    elif cand:
        best = min(cand, key=lambda j: destaques.index(gr[j]["t"].lower()))  # a primeira da lista de destaques vence
        pal[best]["destaque"] = True
    legendas.append({"ini": round(ini, 3), "fim": round(fim, 3), "palavras": pal})
for lg in legendas:
    if lg["ini"] < gancho_fim or num_ini <= lg["ini"] < num_fim:
        continue
    print(f"  {lg['ini']:6.2f} {' '.join(('*' + w['texto'] + '*') if w['destaque'] else w['texto'] for w in lg['palavras'])}")

G = cfg["gancho"]
props = {
    "fps": FPS,
    "quadros": quadros,
    "costura": 900,
    "rostoY": 760,
    "cenas": cenas,
    "gancho": {"topo": G["topo"], "fim": gancho_fim, "linhas": [dict(l, ini=round(ancora(l["ini"], 0) if l["ini"] != "0" else 0, 3)) for l in G["linhas"]]},
    "legendas": legendas,
    "numero": {"ini": num_ini, "fim": num_fim, "partes": [{"texto": p_["texto"], "em": round(ancora(p_["em"]), 3)} for p_ in cfg["numero"]["partes"]]},
    "batidas": cfg["batidas"]["s"],
    "luz": luz,
    "cta": {"ini": cenas[-1]["ini_q"] / FPS, "rotulo": cfg["cta"]["rotulo"], "destino": cfg["cta"]["destino"], "entrada": cfg["cta"]["entrada_ms"]},
}
json.dump(props, open("rev1/props.json", "w"), ensure_ascii=False, indent=1)

# efeitos sonoros (scripts/mixar.py): s = segundo do Reel, db = em relação à voz (REFERENCIA_EDICAO_FORMATOS 4.1)
cena_t = {c["id"]: c["ini_q"] / FPS for c in cenas}
marco = lambda cid, k: cena_t[cid] + next(c for c in cenas if c["id"] == cid)["marcos"][k]
sfx = [
    {"som": "PDX_swish", "s": cena_t["racha"] + next(c for c in cenas if c["id"] == "racha")["racha"] - 0.05, "db": -6, "nota": "racha ao meio ('partindo')"},
    {"som": "PDX_impacto", "s": ancora(cfg["impacto_dolares"], 0), "db": -4, "nota": "DÓLARES"},
] + [{"som": "PDX_impacto", "s": b, "db": -4, "nota": "batida do 975 mil"} for b in cfg["batidas"]["s"]] + [
    {"som": "PDX_obturador", "s": marco("votacao", "gap"), "db": -8, "nota": "25 MIL"},
    {"som": "PDX_swish", "s": marco("condado", "espalha"), "db": -6, "nota": "a marca se espalha"},
    {"som": "PDX_impacto", "s": marco("xerife", "crime"), "db": -4, "nota": "CRIME"},
    {"som": "PDX_impacto", "s": marco("carta", "nao"), "db": -4, "nota": "carimbo NÃO"},
    {"som": "PDX_ar_longo", "s": luz[0], "db": -6, "nota": "Luz de passagem (pico no corte)", "pico": True},
    {"som": "PD_clack", "s": props["cta"]["ini"] + (props["cta"]["entrada"] + 280) / 1000, "db": -6, "nota": "placa do CTA (DS V2)"},
]
json.dump({"_doc": "Efeitos: s = segundo do Reel; db relativo ao loudness da voz.", "fim_s": quadros / FPS, "efeitos": sfx}, open("rev1/sfx.json", "w"), ensure_ascii=False, indent=1)
print(f"quadros {quadros} ({quadros / FPS:.2f} s) · legendas {len(legendas)} · efeitos {len(sfx)}")
