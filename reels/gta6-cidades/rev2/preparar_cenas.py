"""Resolve as âncoras de cenas.json, corta os planos (mudos, 30 qps, sem mudar velocidade),
gera as fotos e escreve public/props.json para a composição GtaCidades.
Roda de dentro de reels/gta6-cidades/rev1, depois de preparar_voz.py e alinhar.py."""
import json, re, subprocess, os, shutil, unicodedata
FPS = 30
C = json.load(open("cenas.json"))["cenas"]
P = json.load(open("build/palavras.json"))
L = json.load(open("build/linha_voz.json"))
FIM_VOZ = L["duracao"]
os.makedirs("public/planos", exist_ok=True)

def chave(w): return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w)).lower()
def ancora(a):
    if a == "inicio": return 0.0
    if a == "fim": return FIM_VOZ
    m = re.match(r"(\w+):([^#+\-]+?)(?:#(\d+))?([+-][\d.]+)?$", a)
    fala, pal, n, off = m.group(1), chave(m.group(2)), int(m.group(3) or 1), float(m.group(4) or 0)
    hits = [w for w in P if w["fala"] == fala and chave(w["palavra"]) == pal]
    return round(hits[n-1]["inicio"] + off, 3)
def q(t): return round(t * FPS) / FPS

for c in C: c["ini"] = q(ancora(c["ancora"]))
for i, c in enumerate(C):
    c["fim"] = q(c["ini"] + c["dur"]) if c["id"] == "cta" else C[i+1]["ini"]
    c["dur_s"] = round(c["fim"] - c["ini"], 3)

TONEMAP = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
GRADE = "eq=saturation=0.85:contrast=1.04"
def vf_cobrir(w, h, escalaAltura=None, cortaY=None, hdr=False, precorte=None):
    pre = (TONEMAP + "," + GRADE + ",") if hdr else ""
    if precorte: pre += precorte + ","
    if escalaAltura:
        return pre + f"scale=-2:{escalaAltura},crop={w}:{h}:(iw-{w})/2:{cortaY}"
    return pre + f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
def corta(fonte, ss, dur, saida, w, h, **k):
    if SO_LEG and os.path.exists(saida): return
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{ss:.3f}","-t",f"{dur+0.1:.3f}","-i",fonte,"-an",
        "-vf", vf_cobrir(w,h,**k)+f",fps={FPS},setsar=1","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p",saida],check=True)
def quadro(fonte, ss, saida, w, h, hdr=False):
    if SO_LEG and os.path.exists(saida): return
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{ss:.3f}","-i",fonte,"-frames:v","1","-vf",vf_cobrir(w,h,hdr=hdr),"-q:v","2",saida],check=True)
def foto(fonte, saida, w, h):
    if SO_LEG and os.path.exists(saida): return
    subprocess.run(["ffmpeg","-v","error","-y","-i",fonte,"-vf",vf_cobrir(w,h),"-q:v","2",saida],check=True)

cenas = []
SO_LEG = __import__("os").environ.get("SO_LEG")
for c in C:
    d = {"id": c["id"], "tipo": c["tipo"], "ini": c["ini"], "fim": c["fim"], "transicao": c.get("transicao")}
    W, H = (1080, 1920) if c["tipo"] == "cheia" else (1080, 900)
    if "fonte" in c and c["tipo"] in ("topo", "cta"):
        out = f"planos/{c['id']}.mp4"
        corta(c["fonte"], c["ss"], c["dur_s"], "public/"+out, W, H, escalaAltura=c.get("escalaAltura"), cortaY=c.get("cortaY"), hdr=c.get("hdr", False), precorte=c.get("precorte"))
        d["video"] = out
    if "foto" in c:
        out = f"planos/{c['id']}.jpg"; foto(c["foto"], "public/"+out, int(W*1.5), int(H*1.5)); d["foto"] = out
    if "foto_de_video" in c:
        f = c["foto_de_video"]; out = f"planos/{c['id']}.jpg"
        quadro(f["fonte"], f["ss"], "public/"+out, int(W*1.5), int(H*1.5), hdr=f.get("hdr", False)); d["foto"] = out
    if "zoom" in c: d["zoom"] = c["zoom"]
    if c["tipo"] == "grade":
        d["fotos"] = []
        for i, f in enumerate(c["fotos"]):
            out = f"planos/{c['id']}_{i}.jpg"; quadro(f["fonte"], f["ss"], "public/"+out, 540*2, 450*2, hdr=f.get("hdr", False)); d["fotos"].append(out)
        d["entra_em"] = [ancora(a) for a in c["entra_em"]]
    if "numero" in c:
        n = c["numero"]; d["numero"] = {"linhas": n["linhas"], "em": ancora(n["em"])}
        d["numero"]["linhas_em"] = [ancora(a) for a in n.get("linhas_em", [n["em"]] + ([n["segunda_em"]] if "segunda_em" in n else []))]
    if c["tipo"] == "cta":
        g = c["diego"]; out = "planos/cta_diego.mp4"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{g['ss']:.3f}","-t",f"{g['dur']:.3f}","-i",g["fonte"],"-an","-vf",
            TONEMAP+f",scale=1080:1920,fps={FPS},tpad=stop_mode=clone:stop_duration={c['dur_s']:.3f}","-c:v","libx264","-crf","16","-pix_fmt","yuv420p","public/"+out],check=True)
        d["diego"] = out; d["placa"] = c["placa"]
    cenas.append(d)

shutil.copy("build/diego.mp4", "public/diego.mp4")

# ---------- legendas ----------
FUNC = set("a o e de do da em um uma que pra para por na no é eu te os as".split())
DESTAQUE = set("19 450 mentira existe quatro florença veneza cúpula segundos 463 degraus roma coliseu paris notre dame jogo fogo ubisoft graça 3 milhões downloads semana dinheiro ensaio mapa primeiro dia gta vice city miami".split())
OCULTA = []  # intervalos sem legenda (gancho, número em tela cheia, contador)
gancho_fim = ancora("gancho_b:E-0.06")
OCULTA.append((0, gancho_fim))
for d in cenas:
    if d["tipo"] == "cheia" and "numero" in d: OCULTA.append((d["numero"]["em"], d["fim"]))
    if d["tipo"] == "contador": OCULTA.append((d["ini"], d["fim"]))
def oculta(t): return any(a - 1e-3 <= t < b - 1e-3 for a, b in OCULTA)

frases = []  # por pontuação final
cur = []
for w in P:
    if oculta(w["inicio"]):
        if cur: frases.append(cur); cur = []
        continue
    cur.append(w)
    if re.search(r"[.?!:]$", w["palavra"]) or w is P[-1]:
        frases.append(cur); cur = []
if cur: frases.append(cur)

def limpa(p): return re.sub(r"[,.?!:]$", "", p)
from PIL import ImageFont
FONTE_LEG = ImageFont.truetype("build/inter800.ttf", 66)  # Inter 800 66 px (fonte da legenda do formato)
LARG_LEG = 800  # centrada em x 540, cabe em x 140-940 (zona segura x 72-944)
def largura(txt): return FONTE_LEG.getlength(txt.upper())
def custo(g):
    txt = " ".join(limpa(w["palavra"]) for w in g); n = len(txt)
    lw = largura(txt)
    c = abs(lw - 600) / 20 + (1000 if lw > LARG_LEG else 0) + (100 if len(g) > 5 else 0)
    dur = g[-1]["fim"] - g[0]["inicio"]
    if dur < 0.55: c += 45
    if dur < 0.35: c += 150
    if len(g) == 1 and n < 8: c += 20
    if chave(g[-1]["palavra"]) in FUNC and len(g) > 1: c += 45
    if chave(g[-1]["palavra"]) in FUNC and len(g) == 1: c += 15
    for i in range(1, len(g)):
        if g[i-1]["palavra"].endswith(","): c += 100   # vírgula no meio do grupo
    # não separar pares fixos
    return c
FIXOS = [("vice","city"),("assassins","creed"),("de","verdade"),("de","mentira"),("de","graça"),("de","viagem"),("notre","dame"),("gta","6"),("3","milhões"),("463","degraus"),("450","reais"),("dia","19"),("primeiro","dia")]
def corte_ruim(a, b): return (chave(a["palavra"]), chave(b["palavra"])) in FIXOS
grupos = []
# quebras manuais (tamanho de cada grupo) quando a regra automática separa um nome fixo
MANUAL = {"Roma é o Assassin's Creed Brotherhood.": [3, 2, 1],
          "E Paris é o Assassin's Creed Unity.": [4, 2, 1],
          "Então, de forma alguma é dinheiro jogado fora.": [1, 3, 2, 2]}
for f in frases:
    txt = " ".join(w["palavra"] for w in f)
    if txt in MANUAL:
        k = 0
        for t in MANUAL[txt]: grupos.append(f[k:k+t]); k += t
        continue
    n = len(f); best = [0] + [1e9]*n; prev = [0]*(n+1)
    for j in range(1, n+1):
        for i in range(max(0, j-5), j):
            c = best[i] + custo(f[i:j]) + (150 if 0 < i < n and corte_ruim(f[i-1], f[i]) else 0)
            if c < best[j]: best[j], prev[j] = c, i
    j = n; gs = []
    while j > 0: gs.append(f[prev[j]:j]); j = prev[j]
    grupos += gs[::-1]
leg = []
for k, g in enumerate(grupos):
    ini = round(g[0]["inicio"] - 0.04, 3)
    fim = round(g[-1]["fim"] + 0.25, 3)
    if k + 1 < len(grupos): fim = min(fim, round(grupos[k+1][0]["inicio"] - 0.04, 3)) if grupos[k+1][0]["inicio"] - g[-1]["fim"] < 0.6 else fim
    for a, b in OCULTA:
        if ini < a < fim: fim = a
    pal = [{"t": limpa(w["palavra"]).upper(), "destaque": False} for w in g]
    for p in pal:
        if chave(p["t"]) in DESTAQUE: p["destaque"] = True; break
    leg.append({"ini": ini, "fim": fim, "palavras": pal})
# não sobrepor
for a, b in zip(leg, leg[1:]):
    if a["fim"] > b["ini"]: a["fim"] = b["ini"]

# ---------- texto do gancho ----------
A = ancora
gancho = [
  {"ini": A("gancho_a:milhões-0.06"), "fim": A("gancho_a:pra-0.06"), "linhas": [
      {"t": "MILHÕES DE PESSOAS", "em": A("gancho_a:milhões-0.04"), "tam": 84},
      {"t": "VÃO PAGAR MAIS DE", "em": A("gancho_a:vão-0.04"), "tam": 84},
      {"t": "450 REAIS", "em": A("gancho_a:450-0.04"), "tam": 160, "grad": True}]},
  {"ini": A("gancho_a:pra-0.06"), "fim": gancho_fim, "linhas": [
      {"t": "PRA PASSEAR EM", "em": A("gancho_a:pra-0.04"), "tam": 84},
      {"t": "UMA CIDADE", "em": A("gancho_a:uma-0.04"), "tam": 110},
      {"t": "QUE NEM EXISTE", "em": A("gancho_a:que-0.04"), "tam": 140, "grad": True}]},
]
props = {"fps": FPS, "duracao": round(cenas[-1]["fim"], 3), "fimGta": A("virada:Mas-0.06"), "voz": FIM_VOZ,
         "cenas": cenas, "legendas": leg, "gancho": gancho}
json.dump(props, open("public/props.json", "w"), ensure_ascii=False, indent=1)
for d in cenas: print(f"{d['ini']:6.2f}-{d['fim']:6.2f} {d['fim']-d['ini']:4.2f}s {d['tipo']:8s} {d['id']}")
print("legendas:", len(leg))
for l in leg: print(f"  {l['ini']:6.2f}-{l['fim']:6.2f} " + " ".join(("*" if p["destaque"] else "") + p["t"] for p in l["palavras"]))
