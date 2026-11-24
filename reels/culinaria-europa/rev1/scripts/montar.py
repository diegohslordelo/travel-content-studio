"""Gera as props do Remotion (legendas palavra a palavra) e as duas mixagens (sem bipe / com bipe).
Roda de reels/culinaria-europa:  python3 rev1/scripts/montar.py
Voz: a do vídeo do Diego, sem corte nem aceleração (ele já editou). Efeitos: keen no fim do gancho
(CLAUDE.md 12), impacto em "porta", clack da placa do CTA (DS). Master -14 LUFS, pico <= -1 dBTP (DS 4.6)."""
import json, re, subprocess
import numpy as np, soundfile as sf, pyloudnorm as pyln

R = "rev1"
cen = json.load(open(f"{R}/cenas.json"))
ali = json.load(open(f"{R}/transcricao_alinhada.json"))["palavras"]
SR = 48000

# ---------- tempos das palavras ----------
ws = []
for w in ali:
    t = w["ini"] if w["conf"] >= 0.3 else w["whisper_ini"]
    ws.append({"raw": w["p"], "ini": t, "fim": w["fim"]})
for i in range(1, len(ws)):
    ws[i]["ini"] = max(ws[i]["ini"], ws[i - 1]["ini"] + 0.03)

FUNC = {"a", "o", "e", "de", "da", "do", "que", "em", "no", "na", "pra", "pro", "um", "uma", "ao", "é", "se", "por", "eu", "te", "lá"}
def limpa(p): return re.sub(r"[.,!]+$", "", p)

def grupos(censurar):
    """Grupos escritos à mão (rev1/grupos_legenda.txt); cada palavra herda o tempo do alinhamento forçado."""
    from PIL import ImageFont
    fonte = ImageFont.truetype(f"{R}/public/fontes/Inter-ExtraBold.otf", 66)
    linhas = [l.strip() for l in open(f"{R}/grupos_legenda.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
    pal = [w for w in ws if w["ini"] >= cen["gancho"]["fim"] - 0.05]
    norm = lambda x: re.sub(r"[^\wáéíóúâêôãõçà]", "", x.lower())
    out, k = [], 0
    for l in linhas:
        ps = []
        for tk in l.split():
            w = pal[k]; k += 1
            assert norm(w["raw"]) == norm(tk), f"legenda difere da fala: {tk!r} x {w['raw']!r} ({w['ini']:.2f}s)"
            t = "p*rra" if (censurar and norm(tk) == "porra") else tk
            ps.append({"t": t, "ini": round(w["ini"], 3), "fim": w["fim"]})
        # um grupo não atravessa troca de composição (a legenda muda de altura): divide na troca
        pos = lambda tt: next(("baixo" if (c["tipo"] == "diego" or c.get("layout") == "cheia") else "costura") for c in cen["cenas"] if c["ini"] - 0.001 <= tt < c["fim"] + 1e-6)
        partes, cur = [], [ps[0]]
        for q_ in ps[1:]:
            if pos(q_["ini"]) != pos(cur[0]["ini"]): partes.append(cur); cur = []
            cur.append(q_)
        partes.append(cur)
        for pp in partes:
            txt = " ".join(p["t"] for p in pp); larg = fonte.getlength(txt)
            out.append({"palavras": [{"t": p["t"], "ini": p["ini"]} for p in pp], "ini": round(pp[0]["ini"] - 0.06, 3), "fim_fala": pp[-1]["fim"], "px": 66 if larg <= 840 else int(66 * 840 / larg), "largura": round(larg)})
            if len(partes) > 1: print("grupo dividido na troca de composição:", txt)
    assert k == len(pal), f"sobraram palavras: {[w['raw'] for w in pal[k:]]}"
    for a, b in zip(out, out[1:]):
        a["fim"] = round(min(b["ini"], a["fim_fala"] + 0.9), 3)
    out[-1]["fim"] = round(out[-1]["fim_fala"] + 0.6, 3)
    for g in out: g.pop("fim_fala")
    return out

# ---------- áudio ----------
voz, sr = sf.read("_tmp/voz48k.wav", dtype="float64"); assert sr == SR
if voz.ndim == 1: voz = np.stack([voz, voz], 1)
meter = pyln.Meter(SR)
lv = meter.integrated_loudness(voz)
def carrega(p):
    x, s = sf.read(p, dtype="float64")
    if x.ndim > 1: x = x.mean(1)
    if s != SR:
        n = int(len(x) * SR / s); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x
def ev_lufs(x):  # loudness do evento: maior janela de 400 ms
    best = -99
    for i in range(0, max(1, len(x) - int(0.4 * SR)), int(0.05 * SR)):
        seg = x[i:i + int(0.4 * SR)]
        if len(seg) < int(0.4 * SR): seg = np.pad(seg, (0, int(0.4 * SR) - len(seg)))
        best = max(best, meter.integrated_loudness(np.stack([seg, seg], 1)))
    return best
def poe(mix, x, t, rel):
    g = 10 ** ((lv + rel - ev_lufs(x)) / 20); i = int(round(t * SR))
    seg = x[: max(0, len(mix) - i)] * g; mix[i:i + len(seg)] += seg[:, None]
    return g

efeitos = [
    ("design-system/sons/externos/keen.wav", cen["gancho"]["fim"] - 0.96, -6, "keen: pico (0,96 s) no corte do gancho"),
    ("design-system/sons/externos/PDX_impacto.wav", 39.41, -8, "impacto em 'porta'"),
    ("design-system/sons/PD_clack_v1.wav", cen["cta"]["entrada"] + 0.28, -6, "clack da placa (DS), na chegada"),
]
def mixa(bipe):
    mix = voz.copy(); log = []
    for p, t, rel, nome in efeitos:
        g = poe(mix, carrega("../../" + p), t, rel); log.append({"som": nome, "em_s": round(t, 3), "rel_voz_db": rel, "ganho_lin": round(g, 4)})
    if bipe:
        a, b = cen["bipe"]["ini"], cen["bipe"]["fim"]; i, j = int(a * SR), int(b * SR)
        n = j - i; tt = np.arange(n) / SR; tone = np.sin(2 * np.pi * 1000 * tt)
        ramp = np.minimum(1, np.minimum(np.arange(n), n - np.arange(n)) / (0.008 * SR))
        g = 10 ** ((lv - 4 - meter.integrated_loudness(np.stack([tone, tone], 1))) / 20)
        fade = np.ones(len(mix)); fade[i:j] = 1 - ramp  # a voz sai sob o bipe
        mix = mix * fade[:, None]; mix[i:j] += (tone * ramp * g)[:, None]
        log.append({"som": "bipe 1 kHz sobre 'porra'", "de_s": a, "ate_s": b, "rel_voz_db": -4})
    l = meter.integrated_loudness(mix); mix *= 10 ** ((-14.0 - l) / 20)
    return mix, log

def master(mix, saida):
    """Ganho linear + limitador; repete até -14,0 LUFS integrados com pico verdadeiro <= -1 dBTP."""
    extra = 0.0
    for _ in range(6):
        sf.write("_tmp/pre.wav", (mix * 10 ** (extra / 20)).astype(np.float32), SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/pre.wav", "-af", "alimiter=limit=0.79:attack=1:release=60:level=disabled", "-c:a", "pcm_s24le", saida], check=True)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", saida, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
        if abs(I + 14.0) <= 0.05: break
        extra += -14.0 - I
    return I, tp

props_base = {
    "dur": round(len(voz) / SR, 3),
    "diego": {"src": "cenas/diego.mp4", "offsetY": 668, "zoomCheia": [1.0, 1.05]},
    "cenas": [{k: c[k] for k in ("id", "tipo", "ini", "fim") } | {"layout": c.get("layout", "dividida")} | ({"src": f'cenas/{c["id"]}.mp4'} if c["tipo"] == "video" else {}) | ({"src": f'fotos/{c["fonte"]}', "zoom": c.get("zoom", [1, 1]), "cx": c.get("cx", 0.5), "cy": c.get("cy", 0.5)} if c["tipo"] == "foto" else {}) for c in cen["cenas"]],
    "gancho": {"linhas": [{"t": cen["gancho"]["texto"][0], "px": 104}, {"t": cen["gancho"]["texto"][1], "px": 180, "cor": "#E0AE5C"}, {"t": cen["gancho"]["texto"][2], "px": 104}], "ini": 0, "fim": cen["gancho"]["fim"], "topo": 300},
    "pb": {"ini": cen["pb"]["ini"], "fim": cen["pb"]["fim"]},
    "cta": {"destino": cen["cta"]["destino"], "modulo": cen["cta"]["modulo"], "entrada": cen["cta"]["entrada"]},
    "estilo": {"destaque": "#E0AE5C", "fonteLegenda": "fontes/Inter-ExtraBold.otf", "fonteGancho": "fontes/anton-latin-400-normal.woff2"},
}
relatorio = {"voz_lufs_original": round(lv, 2)}
for nome, bipe in [("sem_pi", False), ("com_pi", True)]:
    mix, log = mixa(bipe)
    I, tp = master(mix, f"{R}/public/audio/mix_{nome}.wav")
    log.append({"master_lufs": I, "pico_verdadeiro_dbtp": tp})
    p = dict(props_base, audio=f"audio/mix_{nome}.wav", legendas=grupos(bipe))
    json.dump(p, open(f"{R}/props_{nome}.json", "w"), ensure_ascii=False, indent=1)
    relatorio[nome] = log
json.dump(relatorio, open(f"{R}/mixagem.json", "w"), ensure_ascii=False, indent=1)
for g in json.load(open(f"{R}/props_com_pi.json"))["legendas"]:
    print(f'{g["ini"]:6.2f}-{g["fim"]:6.2f}  {" ".join(w["t"] for w in g["palavras"])}')
