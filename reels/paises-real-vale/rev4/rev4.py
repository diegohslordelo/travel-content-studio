"""
Países onde o brasileiro vive como rico · REV4 (tela dividida).

    python3 rev4.py preparar   # cortes (última tomada de cada frase), voz emendada, tempos das palavras, props
    python3 rev4.py render     # Remotion monta o Reel (design-system/remotion, composição "TelaDividida")
    python3 rev4.py master     # loudness −14 LUFS / −1 dBTP e entrega
Roda de dentro de reels/paises-real-vale/rev4. Caminhos relativos.
"""
import json, os, subprocess, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REEL = os.path.dirname(AQUI)
TMP = os.path.join(REEL, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(REEL, "..", "..", "design-system", "remotion"))
FPS = 24  # o bruto é 24 qps; compor em 24 evita trepidação no rosto (FPS de produção: pendência 5)
CFG = json.load(open(os.path.join(AQUI, "rev4.json"), encoding="utf-8"))

def q(t):  # arredonda para o quadro
    return round(t * FPS) / FPS

def cortes():
    al = json.load(open(os.path.join(AQUI, "alinhamento.json"), encoding="utf-8"))
    db = np.load(os.path.join(TMP, "db10ms.npy"))
    out = []
    for t in al:
        p = t["palavras"]
        s, e = p[0]["s"], p[-1]["e"]
        ini = s - CFG["margem"]["antes"]
        fim = e + CFG["margem"]["depois"]
        # não deixa a borda cair em som: recua o início/avança o fim até um quadro de silêncio (< limiar), no máx. 120 ms
        lim = CFG["margem"]["silencio_db"]
        for _ in range(12):
            if db[int(ini * 100)] < lim: break
            ini -= 0.01
        for _ in range(12):
            if db[int(fim * 100)] < lim: break
            fim += 0.01
        out.append({"id": t["id"], "ini": q(ini), "fim": q(fim), "palavras": p,
                    "borda_db": [round(float(db[int(q(ini) * 100)]), 1), round(float(db[int(q(fim) * 100)]), 1)]})
    return out

def preparar():
    os.makedirs(PUBLIC, exist_ok=True)
    cs = cortes()
    # voz: concatena as tomadas do proxy SDR, com 12 ms de fade no áudio em cada emenda (sem clique)
    fc, ins = [], []
    for k, c in enumerate(cs):
        d = c["fim"] - c["ini"]
        fc.append(f"[0:v]trim={c['ini']}:{c['fim']},setpts=PTS-STARTPTS[v{k}]")
        fc.append(f"[0:a]atrim={c['ini']}:{c['fim']},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012[a{k}]")
        ins.append(f"[v{k}][a{k}]")
    fc.append("".join(ins) + f"concat=n={len(cs)}:v=1:a=1[v][a]")
    saida = os.path.join(PUBLIC, "voz.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(TMP, "proxy_sdr.mp4"), "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-r", str(FPS), "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-g", str(FPS),
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", saida], check=True)
    # palavras na linha do tempo do Reel (ms)
    acum, pal, tomadas = 0.0, [], []
    for c in cs:
        for w in c["palavras"]:
            pal.append({"txt": w["txt"], "s": round((w["s"] - c["ini"] + acum) * 1000), "e": round((w["e"] - c["ini"] + acum) * 1000), "tomada": c["id"]})
        tomadas.append({"id": c["id"], "de": round(acum * 1000), "ate": round((acum + c["fim"] - c["ini"]) * 1000), "bruto": [c["ini"], c["fim"]], "borda_db": c["borda_db"]})
        acum += c["fim"] - c["ini"]
    voz_ms = round(acum * 1000)
    json.dump({"tomadas": tomadas, "palavras": pal, "voz_ms": voz_ms}, open(os.path.join(AQUI, "linha_do_tempo.json"), "w"), ensure_ascii=False, indent=1)
    for t in tomadas:
        print(f"{t['id']:10s} bruto {t['bruto'][0]:7.3f}–{t['bruto'][1]:7.3f}  reel {t['de']/1000:6.2f}–{t['ate']/1000:6.2f}  borda {t['borda_db']} dB")
    print(f"voz: {voz_ms/1000:.2f} s")
    montar_props(pal, tomadas, voz_ms)

def ancora(pal, ref):
    """'tomada:palavra[#n][+/-ms]' ou 'tomada:palavra@fim' → ms."""
    desloc = 0
    for sinal in ("+", "-"):
        if sinal in ref[1:]:
            base, num = ref.rsplit(sinal, 1)
            if num.isdigit():
                desloc = int(num) * (1 if sinal == "+" else -1); ref = base
            break
    fim = ref.endswith("@fim")
    if fim: ref = ref[:-4]
    tom, w = ref.split(":", 1)
    n = 1
    if "#" in w: w, n = w.split("#"); n = int(n)
    norm = lambda s: s.lower().strip(".,!?")
    ach = [p for p in pal if p["tomada"] == tom and norm(p["txt"]) == norm(w)]
    if len(ach) < n: raise SystemExit(f"âncora não encontrada: {ref}")
    return (ach[n - 1]["e"] if fim else ach[n - 1]["s"]) + desloc

def resolver(obj, pal):
    if isinstance(obj, dict):
        return {k: ([ancora(pal, x) for x in v] if k == "icones" else ancora(pal, v) if isinstance(v, str) and k in ("de", "ate", "em", "fim", "notas", "sonham", "moeda", "xis", "virar", "rico") and ":" in v else resolver(v, pal)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolver(x, pal) for x in obj]
    return obj

def grupos_legenda(pal):
    """Grupos de 1 a 4 palavras, até ~24 caracteres, 1 linha (FORMATOS_REELS.md, 6). Quebra em pontuação e entre tomadas; evita terminar em palavra funcional."""
    func = {"de", "do", "da", "o", "a", "e", "que", "em", "no", "na", "nas", "com", "por", "pra", "para", "as", "os", "um", "uma", "uns", "se", "nem", "te", "me", "eu", "lá", "já", "é"}
    gs, atual = [], []
    def fecha():
        if atual: gs.append(list(atual)); atual.clear()
    for i, p in enumerate(pal):
        atual.append(i)
        txt = " ".join(pal[j]["txt"] for j in atual)
        prox = pal[i + 1] if i + 1 < len(pal) else None
        pontua = p["txt"][-1] in ".,?!"
        if prox is None or prox["tomada"] != p["tomada"] or pontua:
            fecha(); continue
        txt2 = txt + " " + prox["txt"]
        if len(atual) >= 4 or len(txt2) > 24:
            # não termina em palavra funcional: leva a funcional para o próximo grupo
            if p["txt"].lower() in func and len(atual) > 1:
                atual.pop(); fecha(); atual.append(i)
            else:
                fecha()
    fecha()
    return [{"palavras": g, "de": pal[g[0]]["s"], "ate": pal[g[-1]]["e"]} for g in gs]

SONS_DIR = os.path.normpath(os.path.join(REEL, "..", "..", "design-system", "sons"))

def nivel50(x, sr):
    """Loudness K-ponderada máxima em janelas de 50 ms (mesma medida de design-system/sons/gerar_sons.py)."""
    import pyloudnorm as pyln
    m = pyln.Meter(sr, block_size=0.4)
    k = x.copy()
    for f in m._filters.values():
        k = f.apply_filter(k.reshape(-1, 1) if k.ndim == 1 else k)
    k = k[:, 0] if k.ndim > 1 else k
    n = int(0.05 * sr)
    ms = np.convolve(k ** 2, np.ones(n) / n, mode="valid") if len(k) >= n else np.array([np.mean(k ** 2)])
    return -0.691 + 10 * np.log10(np.max(ms) + 1e-20)

def sons_props(sons):
    """Ganho de cada efeito: (loudness integrada da voz + dB relativo, REFERENCIA_EDICAO_FORMATOS.md 4.1) − loudness de evento do arquivo."""
    import pyloudnorm as pyln, soundfile as sf, shutil
    wav = os.path.join(TMP, "voz.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PUBLIC, "voz.mp4"), "-vn", "-ac", "1", "-ar", "48000", wav], check=True)
    v, sr = sf.read(wav)
    voz_lufs = pyln.Meter(sr).integrated_loudness(v)
    os.makedirs(os.path.join(PUBLIC, "sons"), exist_ok=True)
    out = []
    for s in sons:
        arq = s["arq"] + ".wav"
        orig = os.path.join(SONS_DIR, "externos", arq) if s["arq"].startswith("PDX") else os.path.join(SONS_DIR, arq)
        shutil.copy(orig, os.path.join(PUBLIC, "sons", arq))
        x, srx = sf.read(orig)
        if x.ndim > 1: x = x.mean(axis=1)
        ganho = voz_lufs + s["db"] - nivel50(x, srx)
        dur = round(len(x) / srx * 1000)
        em = s["em"] if "em" in s else s["fim"] - dur
        out.append({"src": f"sons/{arq}", "em": em, "ganho_db": round(ganho, 1), "dur": dur})
    print(f"voz: {voz_lufs:.1f} LUFS integrados · {len(out)} efeitos")
    ems = sorted(o["em"] for o in out)
    perto = [(a, b) for a, b in zip(ems, ems[1:]) if b - a < 1500]
    if perto: print("aviso: efeitos a menos de 1,5 s:", perto)
    return out

def montar_props(pal, tomadas, voz_ms):
    grupos = grupos_legenda(pal)
    # cada grupo fica até o próximo começar (no máx. +400 ms), para a legenda não piscar
    for k, g in enumerate(grupos):
        prox = grupos[k + 1]["de"] if k + 1 < len(grupos) else voz_ms
        g["ate"] = min(prox, g["ate"] + 400)
    dur = voz_ms + CFG["cauda_ms"]
    props = {"fps": FPS, "duracao": dur, "voz": "voz.mp4", "diegoY": CFG["diegoY"], "palavras": pal, "grupos": grupos,
             "semLegenda": [resolver(x, pal) for x in CFG["semLegenda"]],
             "cenas": resolver(CFG["cenas"], pal), "sons": sons_props(resolver(CFG["sons"], pal)), "gancho": resolver(CFG["gancho"], pal), "cta": resolver(CFG["cta"], pal), "zooms": resolver(CFG.get("zooms", []), pal), "popLegenda": CFG.get("popLegenda", False)}
    # a última cena vai até o fim
    props["cenas"][-1]["ate"] = dur
    json.dump(props, open(os.path.join(TMP, "props_rev4.json"), "w"), ensure_ascii=False, indent=1)
    print(f"duração total: {dur/1000:.2f} s · {len(grupos)} grupos de legenda · props em _tmp/props_rev4.json")

def render(saida=None, extra=()):
    saida = saida or os.path.join(TMP, "reel_bruto_rev4.mp4")
    cmd = ["npx", "remotion", "render", "src/index.ts", "TelaDividida", saida, f"--props={os.path.join(TMP, 'props_rev4.json')}",
           f"--public-dir={PUBLIC}", "--concurrency=4", "--log=warn", *extra]
    subprocess.run(cmd, cwd=REMOTION, check=True)

def master():
    bruto = os.path.join(TMP, "reel_bruto_rev4.mp4")
    final = os.path.join(AQUI, CFG["saida"])
    # loudnorm em duas passagens: −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", bruto, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex("{"):])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
          f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "256k",
                    "-movflags", "+faststart", final], check=True)
    print("entregue:", final)

if __name__ == "__main__":
    {"preparar": preparar, "render": render, "master": master}[sys.argv[1]]()
