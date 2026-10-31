#!/usr/bin/env python3
"""Reel da cratera de Darvaza · tela dividida (docs/FORMATOS_REELS.md). DS V2 só no CTA final.

Rode de dentro de reels/darvaza-cratera/:
    python3 scripts/preparar.py      # voz e vídeo do Diego decupados nos mesmos trechos → public/fala.mp4, public/voz.wav
    python3 scripts/alinhar.py       # palavras com tempo (alinhamento forçado) → _tmp/palavras.json
    python3 scripts/reel.py props    # cenas.json + palavras → _tmp/props.json; fotos e mapa em public/
    python3 scripts/reel.py sons     # faixa de efeitos (PDX_* + cama de fogo) → public/sfx.wav
    python3 scripts/reel.py render   # Remotion, composição "ReelDarvaza"
    python3 scripts/reel.py master   # −14 LUFS integrados, pico ≤ −1 dBTP → revN/reel_darvaza_revN.mp4
    python3 scripts/reel.py capa     # capa 1080 × 1920
    python3 scripts/reel.py quadros  # folhas de QA (um quadro por cena e um por segundo)
    python3 scripts/reel.py tudo
A revisão de saída é a do arquivo REV (padrão rev1).
"""
import json, os, re, shutil, subprocess, sys
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
REV = os.environ.get("REV", "rev1")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "remotion"))
PUBLIC = os.path.join(AQUI, "public")
SONS_DIR = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "sons", "externos"))
FPS = 30
SR = 48000
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")
AMBAR = "#E0AE5C"


def sh(cmd, cwd=None):
    print("  $", " ".join(cmd)[:220])
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode:
        sys.exit(f"falhou: {cmd[0]}")


def ler(n):
    return json.load(open(n, encoding="utf-8"))


def norm(w):
    return re.sub(r"[^a-záàâãéêíóôõúüç]", "", w.lower())


class Ancoras:
    """Resolve 'fala:palavra#n±s' (início da palavra), números e 'fim' no tempo do Reel."""

    def __init__(self, palavras, total):
        self.p = palavras
        self.total = total

    def palavra(self, ref):
        fala, resto = ref.split(":")
        n = 1
        if "#" in resto:
            resto, n = resto.split("#"); n = int(n)
        alvo = norm(resto)
        achou = [w for w in self.p if w["fala"] == fala and norm(w["texto"]) == alvo]
        if len(achou) < n:
            sys.exit(f"âncora não encontrada: {ref}")
        return achou[n - 1]

    def __call__(self, a):
        if isinstance(a, (int, float)):
            return float(a)
        m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)?$", a.strip())
        base, delta = m.group(1), float(m.group(2) or 0)
        if base == "fim":
            return self.total + delta
        if ":" not in base:
            return float(base) + delta
        return self.palavra(base)["ini"] + delta


def contexto():
    pal = ler("_tmp/palavras.json")
    ed = ler("edicao.json")
    voz_s = sf.info("public/voz.wav").duration
    return pal, ed, Ancoras(pal, voz_s), voz_s


def legendas(spec, pal):
    """Grupos de legenda: cada texto consome o mesmo número de palavras faladas, na ordem."""
    out, k = [], 0
    grupos = []
    for g in spec:
        oculto = g.startswith("~")
        toks = g.lstrip("~").split()
        ws = pal[k:k + len(toks)]
        for tok, w in zip(toks, ws):
            if norm(tok.replace("*", "")) != norm(w["texto"]) and not (tok.strip("*,.") == "solo" and norm(w["texto"]) == "sol"):
                sys.exit(f"legenda fora de ordem: '{tok}' × '{w['texto']}' ({w['ini']:.2f} s)")
        k += len(toks)
        grupos.append((oculto, toks, ws))
    if k != len(pal):
        sys.exit(f"legendas cobrem {k} de {len(pal)} palavras")
    for i, (oculto, toks, ws) in enumerate(grupos):
        ini = ws[0]["ini"] - 0.05
        prox = grupos[i + 1][2][0]["ini"] - 0.05 if i + 1 < len(grupos) else None
        fim = prox if prox is not None and prox - ws[-1]["fim"] < 0.6 else ws[-1]["fim"] + 0.3
        if oculto:
            continue
        palavras = []
        destaque = False
        for tok in toks:
            if tok.startswith("*"):
                destaque = True
            palavras.append({"texto": tok.replace("*", ""), "destaque": destaque})
            if tok.rstrip(",.!?").endswith("*"):
                destaque = False
        out.append({"palavras": palavras, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


def props():
    pal, ed, A, voz_s = contexto()
    c = ler("cenas.json")
    total = voz_s
    quadros = int(round(total * FPS))
    lista = ler("imagens/lista_commons.json")
    os.makedirs(os.path.join(PUBLIC, "img"), exist_ok=True)
    for k, v in lista.items():
        dst = os.path.join(PUBLIC, "img", k + ".jpg")
        if not os.path.exists(dst):
            shutil.copy(os.path.join("imagens", v["arquivo"]), dst)
    inis = {s["id"]: A(s["ini"]) for s in c["cenas"]}
    cenas = []
    for i, s in enumerate(c["cenas"]):
        ini = inis[s["id"]]
        fim = inis[c["cenas"][i + 1]["id"]] if i + 1 < len(c["cenas"]) else total
        e = {k: v for k, v in s.items() if k not in ("ini", "base", "marcos", "titulo", "apagar", "envio", "punch")}
        e["ini_q"], e["fim_q"] = round(ini * FPS), round(fim * FPS)
        e.setdefault("layout", "full")
        origem = inis[s["base"]] if "base" in s else ini
        if "base" in s:
            e["desloc"] = round(ini - origem, 4)
        if "foto" in s:
            e["foto"] = f"img/{s['foto']}.jpg"
        if "marcos" in s:
            e["marcos"] = {k: round(A(v) - origem, 4) for k, v in s["marcos"].items()}
        if "apagar" in s:
            e["apagar"] = [round(A(s["apagar"][0]) - ini, 4), round(A(s["apagar"][1]) - ini, 4), s["apagar"][2]]
        if "titulo" in s:
            e["titulo"] = {"centroY": s["titulo"]["centroY"],
                           "linhas": [dict(l, em=round(A(l["em"]) - ini, 4), **({"cor": AMBAR} if l.get("cor") == "ambar" else {})) for l in s["titulo"]["linhas"]]}
            if "sai" in s["titulo"]:
                e["titulo"]["sai"] = round(A(s["titulo"]["sai"]) - ini, 4)
        if "envio" in s:
            v = s["envio"]
            e["envio"] = {"entra": round(A(v["entra"]) - ini, 4), "voa": round(A(v["voa"]) - ini, 4), "x": v["x"], "y": v["y"]}
        if "punch" in s:
            e["punch"] = {"em": round(A(s["punch"]["em"]) - ini, 4), "z": s["punch"]["z"]}
        cenas.append(e)
    g = c["gancho"]
    cta_ini = A(c["cta"]["ini"])
    voz_lufs = medir_lufs("public/voz.wav")
    p = {
        "fps": FPS, "largura": 1080, "altura": 1920, "costura": c["costura"], "rostoY": c["rostoY"], "rostoX": c["rostoX"],
        "quadros": quadros, "cenas": cenas,
        "gancho": [{"linhas": b["linhas"], "tamanhos": b["tamanhos"], "tempos": [round(A(x), 3) for x in b["tempos"]]} for b in g["blocos"]],
        "fimGancho": round(A(g["fim"]), 3), "ganchoTopo": g["topo"],
        "legendas": legendas(c["legendas"], pal),
        "cta": {"ini": round(cta_ini, 3), "rotulo": c["cta"]["rotulo"], "destino": c["cta"]["destino"], "entrada": round((A(c["cta"]["entrada"]) - cta_ini) * 1000)},
        "mix": {"voz_lufs": round(voz_lufs, 2), "clack_db_rel": -6},
        "sfx": os.path.exists(os.path.join(PUBLIC, "sfx.wav")),
        "transicoes": [{"tipo": t["tipo"], "q": round(A(t["em"]) * FPS)} for t in c["transicoes"]],
        "mapa": ler("mapa/paises.json"),
    }
    json.dump(p, open("_tmp/props.json", "w"), ensure_ascii=False)
    print(f"props: {len(cenas)} cenas, {quadros} quadros ({total:.2f} s), {len(p['legendas'])} legendas, voz {voz_lufs:.1f} LUFS")
    for e in cenas:
        print(f"  {e['ini_q']/FPS:6.2f}–{e['fim_q']/FPS:6.2f} ({(e['fim_q']-e['ini_q'])/FPS:4.2f} s) {e['tipo']:5} {e['layout']:5} {e['id']}")


def medir_lufs(arq):
    import pyloudnorm as pyln
    x, sr = sf.read(arq)
    return pyln.Meter(sr).integrated_loudness(x)


def fogo(n, rng):
    """Cama de fogo sintetizada: rumor grave (ruído marrom filtrado, respirando devagar) + estalos (rajadas curtas)."""
    from scipy.signal import butter, sosfilt
    w = rng.standard_normal(n)
    marrom = np.cumsum(w); marrom -= np.convolve(marrom, np.ones(4801) / 4801, "same")
    rumor = sosfilt(butter(2, [40, 320], "bandpass", fs=SR, output="sos"), marrom)
    rumor /= np.abs(rumor).max()
    t = np.arange(n) / SR
    rumor *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.31 * t) * np.sin(2 * np.pi * 0.17 * t + 1)
    sopro = sosfilt(butter(2, [300, 1800], "bandpass", fs=SR, output="sos"), w) * 0.05
    estalos = np.zeros(n)
    k = 0
    while True:
        k += int(rng.exponential(SR / 14))
        if k >= n - 2000:
            break
        d = int(SR * rng.uniform(0.001, 0.006))
        a = min(1.0, rng.pareto(2.2) * 0.25 + 0.05)
        b = rng.standard_normal(d) * np.exp(-np.arange(d) / (d / 4)) * a
        estalos[k:k + d] += b
    estalos = sosfilt(butter(2, [900, 7000], "bandpass", fs=SR, output="sos"), estalos)
    estalos /= np.abs(estalos).max()
    return 0.8 * rumor + sopro + 0.55 * estalos


def sons():
    import pyloudnorm as pyln
    pal, ed, A, voz_s = contexto()
    c = ler("cenas.json")
    total = voz_s
    n = int(total * SR)
    pista = np.zeros(n + SR)
    med = pyln.Meter(SR)
    voz_lufs = medir_lufs("public/voz.wav")
    feitos = []
    for ev in c["sons"]:
        y, sr = sf.read(os.path.join(SONS_DIR, ev["som"] + ".wav"))
        if y.ndim > 1:
            y = y.mean(axis=1)
        if sr != SR:
            from scipy.signal import resample_poly
            y = resample_poly(y, SR, sr)
        lufs = med.integrated_loudness(np.concatenate([y, np.zeros(SR)]))
        y = y * 10 ** ((voz_lufs + ev["rel_db"] - lufs) / 20)
        t = A(ev["em"])
        al = ev.get("alinhar", "inicio")
        if al == "pico":
            env = np.convolve(np.abs(y), np.ones(480) / 480, "same")
            t -= int(np.argmax(env)) / SR
        elif al == "fim":
            t -= len(y) / SR
        k = int(round(t * SR))
        a0 = max(0, -k)
        pista[max(0, k):max(0, k) + len(y) - a0] += y[a0:a0 + len(pista) - max(0, k)][:len(pista) - max(0, k)]
        feitos.append({"som": ev["som"], "em_s": round(t, 3), "rel_db": ev["rel_db"], "nota": ev.get("nota", "")})
    # cama de fogo
    f = c["fogo"]
    rng = np.random.default_rng(40)
    cama = fogo(len(pista), rng)
    l_cama = med.integrated_loudness(cama[:SR * 10])
    ganho = np.full(len(pista), voz_lufs + f["base_rel_db"] - l_cama)
    for r in f["realces"]:
        a, b = int(A(r["de"]) * SR), int(A(r["ate"]) * SR)
        ganho[a:b] = voz_lufs + r["rel_db"] - l_cama
    for r in f["silencio"]:
        a, b = int(A(r["de"]) * SR), int(A(r["ate"]) * SR)
        ganho[a:b] = -90
    lin = 10 ** (ganho / 20)
    lin = np.convolve(lin, np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")  # rampas de 250 ms
    pista += cama * lin
    pista = pista[:n + int(0.05 * SR)]
    sf.write(os.path.join(PUBLIC, "sfx.wav"), np.stack([pista, pista], axis=1).astype(np.float32) * 0.7071, SR, subtype="FLOAT")
    json.dump(feitos, open("_tmp/sons.json", "w"), ensure_ascii=False, indent=1)
    for x in feitos:
        print(f"  {x['em_s']:6.2f} s  {x['som']:14} {x['rel_db']:+d} dB  {x['nota']}")


def render():
    os.makedirs("_tmp", exist_ok=True)
    cmd = ["npx", "remotion", "render", "src/index.ts", "ReelDarvaza", os.path.join(AQUI, "_tmp", "reel_sem_master.mov"),
           f"--props={os.path.join(AQUI, '_tmp', 'props.json')}", f"--public-dir={PUBLIC}", "--concurrency=4",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--audio-bitrate=320k", "--log=warn"]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    for a in sys.argv[2:]:
        cmd.append(a)
    sh(cmd, cwd=REMOTION)


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def master():
    os.makedirs(REV, exist_ok=True)
    ent = "_tmp/reel_sem_master.mov"
    sai = f"{REV}/reel_darvaza_{REV}.mp4"
    i0, _ = medir(ent)
    ganho, alvo, pico = -14.0 - i0, -14.0, -1.0
    teto = pico - 0.4
    for _ in range(6):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", sai])
        i, tp = medir(sai)
        print(f"  master: {i:.2f} LUFS, pico {tp:.2f} dBTP (ganho {ganho:.2f})")
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= 0.3
    # prévia leve para o celular
    sh(["ffmpeg", "-v", "error", "-y", "-i", sai, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", f"{REV}/reel_darvaza_{REV}_previa.mp4"])


def capa():
    c = ler("cenas.json")
    # o Diego na capa: quadro do gancho (boca fechada, olhar na câmera), escolhido em _tmp/capa_quadro.txt (segundo do fala.mp4)
    t = float(open("_tmp/capa_quadro.txt").read().strip()) if os.path.exists("_tmp/capa_quadro.txt") else 0.5
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", "public/fala.mp4", "-frames:v", "1", "-q:v", "2", "public/capa_quadro.jpg"])
    pr = {"foto": "img/porta_inferno.jpg", "quadro": "capa_quadro.jpg", "centroY": 545, "costura": c["costura"], "rostoY": c["rostoY"],
          "linhas": [{"texto": "A PORTA", "tam": 190, "em": 0}, {"texto": "DO INFERNO", "tam": 190, "em": 0, "cor": AMBAR}, {"texto": "EXISTE", "tam": 120, "em": 0}]}
    json.dump(pr, open("_tmp/capa_props.json", "w"), ensure_ascii=False)
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaDarvaza", os.path.join(AQUI, REV, f"capa_darvaza_{REV}.jpg"),
           f"--props={os.path.join(AQUI, '_tmp', 'capa_props.json')}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    sh(cmd, cwd=REMOTION)


def quadros():
    p = ler("_tmp/props.json")
    vid = f"{REV}/reel_darvaza_{REV}.mp4"
    d = f"{REV}/qa_frames"
    os.makedirs(d, exist_ok=True)
    tmp = "_tmp/qa"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i, c in enumerate(p["cenas"]):
        meio = (c["ini_q"] + c["fim_q"]) / 2 / FPS
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{meio:.3f}", "-i", vid, "-frames:v", "1", "-vf",
            f"scale=360:640,drawtext=text='{i + 1} {c['id']} {c['ini_q'] / FPS:.1f}s':x=8:y=8:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6", f"{tmp}/c{i:02d}.png"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/c%02d.png", "-vf", "tile=7x4:padding=4", "-frames:v", "1", f"{d}/cenas.jpg"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vf", "fps=1,scale=270:480,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=8x5:padding=3",
        "-frames:v", "1", f"{d}/um_por_segundo.jpg"])


if __name__ == "__main__":
    passo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    passos = {"props": props, "sons": sons, "render": render, "master": master, "capa": capa, "quadros": quadros}
    if passo == "tudo":
        for k in ["sons", "props", "render", "master", "capa", "quadros"]:
            passos[k]()
    else:
        passos[passo]()
