"""Resolve as âncoras de cenas.json, prepara as imagens e os trechos de vídeo (mudos, 30 qps, sem mudar velocidade),
monta as legendas (1 linha, palavra de ênfase nas cores do GTA) e escreve public/props.json para a composição GtaViceCity.
Roda de dentro de reels/gta6-vice-city/rev2, depois de preparar_voz.py e alinhar.py."""
import json, re, subprocess, os, shutil, unicodedata
ESC = float(os.environ.get("ESC", "1.5"))   # resolução das imagens em relação ao painel (4K: ESC=3)
ESC_V = 2 if ESC > 2 else 1                  # trechos de vídeo do jogo: 2x no render 4K
from PIL import Image, ImageFilter, ImageEnhance, ImageFont

FPS = 30
C = json.load(open("cenas.json"))["cenas"]
P = json.load(open("build/palavras.json"))
L = json.load(open("build/linha_voz.json"))
FIM_VOZ = L["duracao"]
W, H, COSTURA = 1080, 1920, 900
os.makedirs("public/planos", exist_ok=True)
# diego.mp4 + 1 s com o último quadro congelado (cobre a cauda final, sem fala)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/diego.mp4", "-vf", "tpad=stop_mode=clone:stop_duration=1", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "public/diego.mp4"], check=True)

def chave(w): return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w)).lower()
def ancora(a):
    if a == "inicio": return 0.0
    m = re.match(r"(\w+):([^#+\-]+?)(?:#(\d+))?([+-][\d.]+)?$", a)
    fala, pal, n, off = m.group(1), chave(m.group(2)), int(m.group(3) or 1), float(m.group(4) or 0)
    hits = [w for w in P if w["fala"] == fala and chave(w["palavra"]) == pal]
    return max(0.0, round(hits[n - 1]["inicio"] + off, 3))
def q(t): return round(t * FPS) / FPS

for c in C: c["ini"] = q(ancora(c["ancora"]))
for i, c in enumerate(C):
    c["fim"] = q(FIM_VOZ + c.get("cauda", 0)) if i == len(C) - 1 else C[i + 1]["ini"]

def cobrir(src, w, h, recorte=None):
    im = Image.open(src).convert("RGB")
    if recorte:
        x0, y0, x1, y1 = recorte; im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))
def conter(src, w, h):
    """Imagem inteira (sem corte) sobre a mesma imagem desfocada e escurecida."""
    im = Image.open(src).convert("RGB")
    fundo = ImageEnhance.Brightness(cobrir(src, w, h).filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
    s = min(w / im.width, h / im.height) * 0.94
    fg = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    fundo.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2)); return fundo
def video(v, dur, saida, w, h):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{v['ss']:.3f}", "-t", f"{dur + 0.1:.3f}", "-i", v["fonte"], "-an", "-vf",
                    (v["precorte"] + "," if v.get("precorte") else "") + f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={FPS},setsar=1",
                    "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", saida], check=True)

cenas = []
for c in C:
    d = {k: c[k] for k in ("id", "tipo", "ini", "fim") }
    for k in ("transicao", "zoom", "zoom_baixo", "origem", "origem_baixo", "tag_cima", "tag_baixo", "numero"):
        if k in c: d[k] = c[k]
    w, h = W, COSTURA
    if "video" in c:
        out = f"planos/{c['id']}.mp4"; video(c["video"], c["fim"] - c["ini"], "public/" + out, w * ESC_V, h * ESC_V); d["video"] = out
    if "foto" in c:
        out = f"planos/{c['id']}.jpg"
        im = conter(c["foto"], int(w * ESC), int(h * ESC)) if c.get("contem") else cobrir(c["foto"], int(w * ESC), int(h * ESC), c.get("recorte"))
        im.save("public/" + out, quality=92); d["foto"] = out
    if "foto_baixo" in c:
        out = f"planos/{c['id']}_real.jpg"
        cobrir(c["foto_baixo"], int(W * ESC), int((H - COSTURA) * ESC), c.get("recorte_baixo")).save("public/" + out, quality=92); d["foto_baixo"] = out
    cenas.append(d)

# ---------- legendas ----------
FUNC = set("a o e de do da em um uma que pra para por na no é eu te os as dos".split())
# ênfase: 1 por grupo (pares fixos ganham as duas palavras)
DESTAQUE = set("carro sofá 19 gta vice miami 3 videogame nostalgia wynwood murais sahara heat kaseya 18 rockstar quadra uniforme ocean 2002 colony y colon lembrar primeiro verdade".split())
PARES = {("vice", "city"), ("gta", "6"), ("miami", "heat"), ("kaseya", "center"), ("sahara", "arena"), ("ocean", "drive"),
         ("colony", "hotel"), ("primeiro", "dia"), ("dia", "19"), ("dia", "18"), ("de", "verdade"), ("vida", "real"), ("3", "lugares")}
FIXOS = PARES | {("pura", "nostalgia"), ("o", "y"), ("comeu", "y")}
OCULTA = [(0.0, cenas[1]["ini"])]  # gancho: o texto grande substitui a legenda
def oculta(t): return any(a - 1e-3 <= t < b - 1e-3 for a, b in OCULTA)

frases, cur = [], []
for w in P:
    if oculta(w["inicio"]):
        if cur: frases.append(cur); cur = []
        continue
    cur.append(w)
    if re.search(r"[.?!:]$", w["palavra"]) or w is P[-1]:
        frases.append(cur); cur = []
if cur: frases.append(cur)

def limpa(p): return re.sub(r"[,.?!:]$", "", p)
FONTE_LEG = ImageFont.truetype("build/inter800.ttf", 66)
LARG_LEG = 800   # centrada em x 540: cabe em x 140-940 (zona segura x 72-944)
def largura(txt): return FONTE_LEG.getlength(txt.upper())
def custo(g):
    txt = " ".join(limpa(w["palavra"]) for w in g); lw = largura(txt)
    c = abs(lw - 560) / 20 + (1000 if lw > LARG_LEG else 0) + (100 if len(g) > 5 else 0)
    dur = g[-1]["fim"] - g[0]["inicio"]
    if dur < 0.55: c += 45
    if dur < 0.35: c += 150
    if len(g) == 1 and len(txt) < 8: c += 20
    if chave(g[-1]["palavra"]) in FUNC and len(g) > 1: c += 45
    for i in range(1, len(g)):
        if g[i - 1]["palavra"].endswith(","): c += 100
    return c
def corte_ruim(a, b): return (chave(a["palavra"]), chave(b["palavra"])) in FIXOS
grupos = []
# quebras manuais (tamanho de cada grupo) quando a regra automática deixa um grupo curto demais
MANUAL = {"E tem o Colony Hotel, que no jogo comeu Y, virou Colon.": [3, 2, 3, 2, 2]}
for f in frases:
    txt = " ".join(w["palavra"] for w in f)
    if txt in MANUAL:
        k = 0
        for t in MANUAL[txt]: grupos.append(f[k:k + t]); k += t
        continue
    n = len(f); best = [0] + [1e9] * n; prev = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 5), j):
            cc = best[i] + custo(f[i:j]) + (150 if 0 < i < n and corte_ruim(f[i - 1], f[i]) else 0)
            if cc < best[j]: best[j], prev[j] = cc, i
    j, gs = n, []
    while j > 0: gs.append(f[prev[j]:j]); j = prev[j]
    grupos += gs[::-1]

leg = []
for k, g in enumerate(grupos):
    ini = round(g[0]["inicio"] - 0.04, 3)
    fim = round(g[-1]["fim"] + 0.25, 3)
    if k + 1 < len(grupos) and grupos[k + 1][0]["inicio"] - g[-1]["fim"] < 0.6: fim = min(fim, round(grupos[k + 1][0]["inicio"] - 0.04, 3))
    pal = [{"t": limpa(w["palavra"]).upper(), "destaque": False} for w in g]
    ks = [chave(w["palavra"]) for w in g]
    for i, kk in enumerate(ks):
        if kk in DESTAQUE:
            pal[i]["destaque"] = True
            if i + 1 < len(ks) and (kk, ks[i + 1]) in PARES: pal[i + 1]["destaque"] = True
            elif i > 0 and (ks[i - 1], kk) in PARES: pal[i - 1]["destaque"] = True
            break
    leg.append({"ini": ini, "fim": fim, "palavras": pal})
for a, b in zip(leg, leg[1:]):           # nunca duas legendas ao mesmo tempo
    if a["fim"] > b["ini"]: a["fim"] = b["ini"]
leg[-1]["fim"] = round(cenas[-1]["fim"], 3)

# ---------- texto do gancho (Anton, x 72) ----------
A = ancora
gancho = [{"ini": 0.0, "fim": cenas[1]["ini"], "linhas": [
    {"t": "ESSE MÊS EU VOU", "em": A("gancho:Esse-0.04"), "tam": 96},
    {"t": "ROUBAR", "em": A("gancho:roubar-0.04"), "tam": 200, "forte": True},
    {"t": "UM CARRO", "em": A("gancho:um-0.04"), "tam": 200, "forte": True}]}]

# vídeo do Diego com a luz roxa só no fundo (aplicar_roxo.py; versão escolhida pelo Diego, 05/11/2026)
props = {"fps": FPS, "duracao": round(cenas[-1]["fim"], 3), "voz": round(FIM_VOZ, 3), "roxo": 0, "diego": "diego_fundo.mp4",
         "cenas": cenas, "legendas": leg, "gancho": gancho}
json.dump(props, open("public/props.json", "w"), ensure_ascii=False, indent=1)
for d in cenas: print(f"{d['ini']:6.2f}-{d['fim']:6.2f} {d['fim'] - d['ini']:4.2f}s {d['tipo']:9s} {d['id']}")
print("legendas:", len(leg))
for l in leg: print(f"  {l['ini']:6.2f}-{l['fim']:6.2f} {largura(' '.join(p['t'] for p in l['palavras'])):4.0f}px " + " ".join(("*" if p["destaque"] else "") + p["t"] for p in l["palavras"]))
