#!/usr/bin/env python3
"""Reel da Disney · Narrado (docs/FORMATOS_TRELLO.md, formato 04; edição: docs/REFERENCIA_EDICAO_FORMATOS.md). DS V2 só no CTA.

Rode de dentro de reels/disney-atracoes/:
    python3 scripts/transcrever.py   # Whisper large-v3 das 15 gravações (texto e tempo de cada palavra)
    python3 scripts/segmentar.py     # trechos com voz → base para edicao.json
    python3 scripts/preparar.py      # voz decupada → public/voz.wav, _tmp/trechos.json
    python3 scripts/alinhar.py       # alinhamento forçado palavra a palavra → _tmp/palavras.json
    python3 scripts/estabilidade.py  # tremor de cada clipe do acervo → _tmp/estabilidade.json (escolha das imagens)
    python3 scripts/reel.py props    # cenas.json + palavras → _tmp/props.json (cenas, legendas, gancho, CTA)
    python3 scripts/reel.py broll    # trechos do acervo recortados em 9:16 e estabilizados (mudos, HDR → SDR) → public/broll/
    python3 scripts/reel.py sons     # faixa de efeitos (keen + PDX_*) → public/sfx.wav
    python3 scripts/reel.py render   # Remotion, composição "ReelDisney"
    python3 scripts/reel.py master   # −14 LUFS integrados, pico ≤ −1 dBTP → revN/reel_disney-atracoes_revN.mp4 (+ prévia)
    python3 scripts/reel.py capa     # capa 1080 × 1920 (quadro do gancho completo)
    python3 scripts/reel.py quadros  # folhas de QA (um quadro por cena e um por segundo)
    python3 scripts/reel.py conferir # medições do QA → _tmp/conferir.json
    python3 scripts/reel.py tudo     # props, broll, sons, props, render, master, capa, quadros, conferir
A revisão de saída é a da variável REV (padrão rev1).
"""
import json, os, re, shutil, subprocess, sys
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
REV = os.environ.get("REV", "rev1")
NOME = "disney-atracoes"
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "remotion"))
PUBLIC = os.path.join(AQUI, "public")
SONS_DIR = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "sons", "externos"))
FPS = 30
SR = 48000
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")
AMBAR = "#E0AE5C"
TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"


def sh(cmd, cwd=None):
    print("  $", " ".join(cmd)[:220])
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode:
        sys.exit(f"falhou: {cmd[0]}")


def ler(n):
    return json.load(open(n, encoding="utf-8"))


def norm(w):
    return re.sub(r"[^a-z0-9áàâãéêíóôõúüç]", "", w.lower())


class Ancoras:
    """Resolve 'fala:palavra#n±s' (início da palavra) e números no tempo do Reel."""

    def __init__(self, palavras):
        self.p = palavras

    def palavra(self, ref):
        fala, resto = ref.split(":")
        n = 1
        if "#" in resto:
            resto, n = resto.split("#"); n = int(n)
        achou = [w for w in self.p if w["fala"] == fala and norm(w["texto"]) == norm(resto)]
        if len(achou) < n:
            sys.exit(f"âncora não encontrada: {ref}")
        return achou[n - 1]

    def __call__(self, a):
        if isinstance(a, (int, float)):
            return float(a)
        m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)?$", a.strip())
        base, delta = m.group(1), float(m.group(2) or 0)
        if ":" not in base:
            return float(base) + delta
        return self.palavra(base)["ini"] + delta


# ---------------------------------------------------------------- legendas (grupos de 1 a 4 palavras, uma linha)
FUNCIONAIS = {"de", "do", "da", "dos", "das", "o", "a", "os", "as", "e", "que", "pra", "pro", "na", "no", "em", "um", "uma", "para",
              "com", "se", "me", "te", "eu", "ao", "isso", "esse", "essa", "mais", "tudo", "ele", "você", "nós", "lá", "aqui"}
PARES = [("disney", "adventure"), ("crush's", "coaster"), ("relâmpago", "mcqueen"), ("torre", "do"), ("do", "terror"), ("main", "street"),
         ("piratas", "do"), ("do", "caribe"), ("star", "wars"), ("hyperspace", "mountain"), ("buzz", "lightyear"), ("big", "thunder"),
         ("pôr", "do"), ("do", "sol"), ("procurando", "nemo"), ("duas", "pernas"), ("um", "sonho"), ("dois", "dias"), ("dois", "parques"),
         ("um", "dia"), ("de", "paris"), ("primeira", "fileira"), ("de", "verdade"), ("ia", "morrer"), ("tava", "lá"), ("final", "de"),
         ("de", "tarde"), ("ainda", "não"), ("não", "existia"), ("área", "nova"), ("nova", "da"), ("cada", "momento"), ("tiro", "ao"),
         ("ao", "alvo"), ("muito", "boa"), ("o", "robô"), ("a", "área"), ("um", "salve"), ("pra", "gente"), ("me", "segue")]


def limpo(w):
    return w.strip().rstrip(".,:;")


_METRICA = None


def largura_legenda(txt):
    """Largura em px do texto em Inter 800, 66 px (avanço dos glifos da fonte usada no render)."""
    global _METRICA
    if _METRICA is None:
        from fontTools.ttLib import TTFont
        ft = TTFont(os.path.join(REMOTION, "node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2"))
        _METRICA = (ft["head"].unitsPerEm, ft.getBestCmap(), ft["hmtx"])
    upm, cmap, hm = _METRICA
    return sum(hm[cmap.get(ord(ch), cmap[ord("?")])][0] for ch in txt) / upm * 66


LARGURA_MAX = 800  # centrada em x 540, a linha fica dentro da zona segura (x 72–944) até 808 px; 8 px de folga


def custo(grupo):
    txt = " ".join(limpo(w["texto"]) for w in grupo)
    c = 0.0
    if len(grupo) > 5 or largura_legenda(txt) > LARGURA_MAX:
        c += 1000
    if len(grupo) == 5:
        c += 6  # 5 palavras só se forem curtas e evitarem uma quebra ruim (o limite de 4 é julgamento, FORMATOS_REELS.md, 6)
    c += ((len(txt) - 17) / 6) ** 2
    if len(grupo) > 1 and norm(grupo[-1]["texto"]) in FUNCIONAIS:
        c += 20 if norm(grupo[-1]["texto"]) == "e" else 10
    if len(grupo) == 1 and norm(grupo[0]["texto"]) in FUNCIONAIS:
        c += 4
    if len(grupo) == 1 and norm(grupo[0]["texto"]) == "e":
        c += 40  # "e" sozinho na tela
    if all(norm(w["texto"]) in FUNCIONAIS for w in grupo):
        c += 15  # grupo só de palavras funcionais ("e a")
    if any(norm(w["texto"]) == "e" for w in grupo[1:]):
        c += 8  # 'e' no meio do grupo: a oração nova começa no grupo seguinte (FORMATOS_REELS.md, 6)
    return c


def corta_par(a, b):
    return (limpo(a["texto"]).lower(), limpo(b["texto"]).lower()) in PARES


def agrupa(frase):
    """Divisão de custo mínimo (programação dinâmica): ~17 caracteres, não termina em palavra funcional, não separa nomes."""
    n = len(frase)
    melhor = [0.0] + [1e9] * n
    corte = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 5), j):
            c = melhor[i] + custo(frase[i:j])
            if 0 < i < n and corta_par(frase[i - 1], frase[i]):
                c += 20
            if c < melhor[j]:
                melhor[j], corte[j] = c, i
    grupos, j = [], n
    while j > 0:
        grupos.append(frase[corte[j]:j]); j = corte[j]
    return grupos[::-1]


def legendas(pal, ocultar_ate):
    vis = [w for w in pal if w["ini"] >= ocultar_ate - 0.02]
    frases, atual = [], []
    for w in vis:
        if atual and atual[-1]["fala"] != w["fala"]:
            frases.append(atual); atual = []
        atual.append(w)
        if re.search(r"[.,:;!?]$", w["texto"]):
            frases.append(atual); atual = []
    if atual:
        frases.append(atual)
    grupos = [g for f in frases for g in agrupa(f)]
    out = []
    for k, g in enumerate(grupos):
        ini = g[0]["ini"] - 0.05
        prox = grupos[k + 1][0]["ini"] - 0.05 if k + 1 < len(grupos) else None
        fim = prox if prox is not None and prox - g[-1]["fim"] < 0.6 else g[-1]["fim"] + 0.3
        out.append({"p": [{"t": limpo(w["texto"]), "i": round(w["ini"], 3), "f": round(w["fim"], 3)} for w in g],
                    "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


# ---------------------------------------------------------------- props
def medir_lufs(arq):
    import pyloudnorm as pyln
    x, sr = sf.read(arq)
    if x.ndim > 1:
        x = x.mean(axis=1)
    return pyln.Meter(sr).integrated_loudness(x)


def contexto():
    pal = ler("_tmp/palavras.json")
    return pal, Ancoras(pal), sf.info("public/voz.wav").duration


def props():
    pal, A, total = contexto()
    c = ler("cenas.json")
    quadros = int(round(total * FPS))
    inis = [A(s["ini"]) for s in c["cenas"]]
    cenas = []
    for k, s in enumerate(c["cenas"]):
        ini = inis[k]
        fim = inis[k + 1] if k + 1 < len(inis) else total
        e = {"id": s["id"], "ini_q": round(ini * FPS), "fim_q": round(fim * FPS), "video": f"broll/{s['id']}.mp4", "kb": s.get("kb", [1.0, 1.04])}
        pre = c["transicoes"][s["entrada"]] if "entrada" in s else 0.0
        e["pre_q"] = round(pre * FPS)
        if "entrada" in s:
            e["entrada"] = s["entrada"]
        if "congelar" in s:
            e["congelar"] = round(A(s["congelar"]) - ini, 3)
        cenas.append(e)
    g = c["gancho"]
    fim_gancho = A(g["fim"])
    cta_ini = A(c["cta"]["ini"])
    p = {
        "fps": FPS, "largura": 1080, "altura": 1920, "quadros": quadros, "cenas": cenas, "transDur": c["transicoes"],
        "gancho": {"topo": g["topo"], "fim": round(fim_gancho, 3),
                   "linhas": [{"texto": l["texto"], "tam": l["tam"], "em": round(A(l["em"]), 3), "cor": AMBAR if l.get("cor") == "ambar" else None} for l in g["linhas"]]},
        "legendas": legendas(pal, fim_gancho), "legendaY": 1320,
        "cta": {"ini": round(cta_ini, 3), "rotulo": c["cta"]["rotulo"], "destino": c["cta"]["destino"], "entrada": round((A(c["cta"]["entrada"]) - cta_ini) * 1000)},
        "mix": {"voz_lufs": round(medir_lufs("public/voz.wav"), 2), "clack_db_rel": -6},
        "sfx": os.path.exists(os.path.join(PUBLIC, "sfx.wav")),
    }
    json.dump(p, open("_tmp/props.json", "w"), ensure_ascii=False)
    print(f"props: {len(cenas)} cenas, {quadros} quadros ({total:.2f} s), {len(p['legendas'])} grupos de legenda, voz {p['mix']['voz_lufs']:.1f} LUFS")
    for e in cenas:
        d = (e["fim_q"] - e["ini_q"]) / FPS
        aviso = "  ← < 2 s" if d < 1.98 else ("  ← > 3 s" if d > 3.05 else "")
        print(f"  {e['ini_q'] / FPS:6.2f}–{e['fim_q'] / FPS:6.2f} ({d:4.2f} s) {e['id']}{aviso}")
    print("  legendas: " + " | ".join(" ".join(w["t"] for w in gr["p"]) for gr in p["legendas"]))
    return p


# ---------------------------------------------------------------- broll estabilizado
def info_video(arq):
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration", "-of", "json", arq],
                                  capture_output=True, text=True).stdout)
    st = s["streams"][0]
    w, h = st["width"], st["height"]
    rot = 0
    for sd in st.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    if abs(rot) == 90:
        w, h = h, w
    num, den = map(int, st["r_frame_rate"].split("/"))
    return w, h, num / den, float(s["format"]["duration"])


def trajetoria(arq, t0, dur, w, h, fps_src, regiao, larg=360):
    """Deslocamento quadro a quadro (correlação de fase) medido só na região que vai aparecer (a janela 9:16 da cena),
    para que a paralaxe do resto do quadro (um poste em primeiro plano, o bonde andando) não entre na conta. Em pixels da fonte."""
    import cv2
    x0, y0, rw, rh = [int(v) // 2 * 2 for v in regiao]
    H = int(round(rh * larg / rw / 2) * 2)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", arq, "-t", f"{dur:.3f}", "-vf", f"crop={rw}:{rh}:{x0}:{y0},scale={larg}:{H}", "-pix_fmt", "gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    n = len(pcm) // (larg * H)
    fr = np.frombuffer(pcm, dtype=np.uint8)[:n * larg * H].reshape(n, H, larg).astype(np.float64)
    jan = np.hanning(larg)[None, :] * np.hanning(H)[:, None]
    dx, dy = [0.0], [0.0]
    for a, b in zip(fr[:-1], fr[1:]):
        (sx, sy), _ = cv2.phaseCorrelate(a, b, jan)
        dx.append(sx); dy.append(sy)
    esc = rw / larg
    return np.cumsum(dx) * esc, np.cumsum(dy) * esc


def suave(x, sigma):
    if len(x) < 3 or sigma <= 0:
        return x.copy()
    r = int(3 * sigma)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
    # pontas por reflexão ímpar (extrapolação linear): numa panorâmica a média não "trava" no começo e no fim do trecho
    return np.convolve(np.pad(x, (r, r), mode="reflect", reflect_type="odd"), k, mode="valid")


def recorta(arq, t0, dur, w, h, fps_src, xs, ys, cw, ch, nq, saida):
    """Decodifica o trecho em resolução cheia (HLG → SDR) e tira, de cada quadro, a janela (xs[i], ys[i], cw, ch) com
    precisão de subpixel (warpAffine, Lanczos), já em 1080 × 1920; o ffmpeg converte para 30 qps e codifica."""
    import cv2
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", arq, "-t", f"{dur:.3f}", "-an", "-vf", f"{TM},format=rgb24",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", f"{fps_src:.6f}", "-i", "-",
                            "-vf", "fps=30,setsar=1", "-frames:v", str(nq), "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-pix_fmt", "yuv420p", saida],
                           stdin=subprocess.PIPE)
    tam = w * h * 3
    s = cw / 1080.0
    i = 0
    while True:
        buf = dec.stdout.read(tam)
        if len(buf) < tam:
            break
        q = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
        k = min(i, len(xs) - 1)
        M = np.array([[s, 0, xs[k]], [0, s, ys[k]]], dtype=np.float64)  # saída (1080 × 1920) → fonte
        out = cv2.warpAffine(q, M, (1080, 1920), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
        try:
            enc.stdin.write(out.tobytes())
        except BrokenPipeError:
            break  # o codificador já tem os nq quadros
        i += 1
    dec.stdout.close(); dec.wait()
    try:
        enc.stdin.close()
    except BrokenPipeError:
        pass
    if enc.wait():
        sys.exit(f"falhou a codificação de {saida}")


def broll():
    """Cada trecho do acervo vira um vídeo 1080 × 1920 a 30 qps, mudo, com tone mapping HLG → SDR (Möbius), recortado em
    9:16 no foco da cena. Estabilização: a janela 9:16 acompanha o tremor (a trajetória menos a sua média de 1,2 s), dentro
    da margem do quadro 4K; o movimento intencional (panorâmica) fica. Nunca estica o take: se o trecho não cabe no plano,
    para com erro."""
    p = ler("_tmp/props.json")
    c = {s["id"]: s for s in ler("cenas.json")["cenas"]}
    os.makedirs(os.path.join(PUBLIC, "broll"), exist_ok=True)
    os.makedirs("_tmp/broll", exist_ok=True)
    so = set(sys.argv[2:])  # reel.py broll <cena> ... refaz só essas cenas (dá para rodar listas diferentes em paralelo)
    for e in p["cenas"]:
        if so and e["id"] not in so:
            continue
        s = c[e["id"]]
        v = s["video"]
        arq = f"fonte/clipes/{v['fonte']}.MOV"
        nq = e["fim_q"] - e["ini_q"] + e["pre_q"]
        t0 = v["in"] - e["pre_q"] / FPS
        w, h, fps_src, dur = info_video(arq)
        if t0 < 0 or t0 + nq / FPS > dur - 0.02:
            sys.exit(f"{e['id']}: o trecho ({t0:.2f} + {nq / FPS:.2f} s) não cabe no plano {v['fonte']} ({dur:.2f} s): troque a entrada ou a imagem")
        z = v.get("zoom", 1.10 if w > h else 1.0)
        if w / h > 9 / 16:
            ch = h / z; cw = ch * 9 / 16
        else:
            cw = w / z; ch = cw * 16 / 9
        cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
        fx, fy = v.get("foco", [0.5, 0.5])
        bx = min(max(0, fx * w - cw / 2), w - cw)
        by = min(max(0, fy * h - ch / 2), h - ch)
        dur_dec = nq / FPS + 0.1
        tx, ty = trajetoria(arq, t0, dur_dec, w, h, fps_src, (bx, by, cw, ch))
        sig = 1.2 * fps_src  # o que oscila em menos de ~1 s é balanço da mão; panorâmica e inclinação lentas ficam
        rx, ry = tx - suave(tx, sig), ty - suave(ty, sig)
        if not v.get("estabilizar", True):
            # plano em que a câmera se aproxima (escala, não deslocamento): a correlação de fase lê a aproximação como
            # tremor e empurraria a janela; fica o recorte fixo
            rx, ry = np.zeros_like(rx), np.zeros_like(ry)
        xs = np.clip(bx + rx, 0, w - cw); ys = np.clip(by + ry, 0, h - ch)
        resto = float(np.sqrt(np.mean((rx - (xs - bx)) ** 2 + (ry - (ys - by)) ** 2)))
        recorta(arq, t0, dur_dec, w, h, fps_src, xs, ys, cw, ch, nq, os.path.join(PUBLIC, "broll", e["id"] + ".mp4"))
        tremor = float(np.sqrt(np.mean(rx ** 2 + ry ** 2)))
        r = {"cena": e["id"], "fonte": v["fonte"], "in": round(t0, 3), "out": round(t0 + nq / FPS, 3), "plano_s": round(dur, 2),
             "recorte": [cw, ch], "tremor_px_fonte": round(tremor, 2), "tremor_restante_px_fonte": round(resto, 2)}
        json.dump(r, open(f"_tmp/broll/{e['id']}.json", "w"))
        print(f"  {e['id']:20} {v['fonte']} {t0:.2f}–{t0 + nq / FPS:.2f} de {dur:.2f} s · recorte {cw}×{ch} · tremor {tremor:.1f} px → resta {resto:.1f} px")
    feitos = [ler(f"_tmp/broll/{e['id']}.json") for e in p["cenas"] if os.path.exists(f"_tmp/broll/{e['id']}.json")]
    json.dump(feitos, open("_tmp/broll.json", "w"), indent=1)


# ---------------------------------------------------------------- sons
def sons():
    import pyloudnorm as pyln
    from scipy.signal import resample_poly
    pal, A, total = contexto()
    c = ler("cenas.json")
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
            y = resample_poly(y, SR, sr)
        lufs = med.integrated_loudness(np.concatenate([y, np.zeros(SR)]))
        y = y * 10 ** ((voz_lufs + ev["rel_db"] - lufs) / 20)
        t = A(ev["em"])
        if ev.get("alinhar") == "pico":
            env = np.convolve(np.abs(y), np.ones(480) / 480, "same")
            t -= int(np.argmax(env)) / SR
        k = int(round(t * SR))
        a0 = max(0, -k)
        seg = y[a0:]
        k = max(0, k)
        m = min(len(seg), len(pista) - k)
        pista[k:k + m] += seg[:m]
        feitos.append({"som": ev["som"], "inicio_s": round(t, 3), "rel_db": ev["rel_db"], "nota": ev.get("nota", "")})
    pista = pista[:n + int(0.05 * SR)]
    sf.write(os.path.join(PUBLIC, "sfx.wav"), np.stack([pista, pista], axis=1).astype(np.float32) * 0.7071, SR, subtype="FLOAT")
    json.dump(feitos, open("_tmp/sons.json", "w"), ensure_ascii=False, indent=1)
    for x in feitos:
        print(f"  {x['inicio_s']:6.2f} s  {x['som']:14} {x['rel_db']:+d} dB  {x['nota']}")


# ---------------------------------------------------------------- render, master, capa, quadros
def render():
    cmd = ["npx", "remotion", "render", "src/index.ts", "ReelDisney", os.path.join(AQUI, "_tmp", "reel_sem_master.mov"),
           f"--props={os.path.join(AQUI, '_tmp', 'props.json')}", f"--public-dir={PUBLIC}", "--concurrency=4",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn"]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    cmd += sys.argv[2:]
    sh(cmd, cwd=REMOTION)


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def master():
    os.makedirs(REV, exist_ok=True)
    ent = "_tmp/reel_sem_master.mov"
    sai = f"{REV}/reel_{NOME}_{REV}.mp4"
    i0, _ = medir(ent)
    ganho, alvo, pico = -14.0 - i0, -14.0, -1.0
    teto = pico - 0.4
    for _ in range(6):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", sai])
        i, tp = medir(sai)
        print(f"  master: {i:.2f} LUFS, pico {tp:.2f} dBTP (ganho {ganho:.2f})")
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= 0.3
    sh(["ffmpeg", "-v", "error", "-y", "-i", sai, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", f"{REV}/reel_{NOME}_{REV}_previa.mp4"])


def capa():
    p = ler("_tmp/props.json")
    q = int(p["gancho"]["fim"] * FPS) - 10  # as três linhas do gancho já na tela
    cmd = ["npx", "remotion", "still", "src/index.ts", "ReelDisney", os.path.join(AQUI, REV, f"capa_{NOME}_{REV}.jpg"), f"--frame={q}",
           f"--props={os.path.join(AQUI, '_tmp', 'props.json')}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    sh(cmd, cwd=REMOTION)


def quadros():
    p = ler("_tmp/props.json")
    vid = f"{REV}/reel_{NOME}_{REV}.mp4"
    d = f"{REV}/qa_frames"
    os.makedirs(d, exist_ok=True)
    tmp = "_tmp/qa"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i, c in enumerate(p["cenas"]):
        meio = (c["ini_q"] + c["fim_q"]) / 2 / FPS
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{meio:.3f}", "-i", vid, "-frames:v", "1", "-vf",
            f"scale=360:640,drawtext=text='{i + 1} {c['id']} {c['ini_q'] / FPS:.1f}s':x=8:y=8:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6", f"{tmp}/c{i:02d}.png"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/c%02d.png", "-vf", "tile=9x3:padding=4", "-frames:v", "1", f"{d}/cenas.jpg"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vf", "fps=1,scale=216:384,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=10x7:padding=3",
        "-frames:v", "1", f"{d}/um_por_segundo.jpg"])


def conferir():
    """Medições do QA: formato, loudness, duração de cada cena, largura das legendas, cortes no quadro certo."""
    from fontTools.ttLib import TTFont
    p = ler("_tmp/props.json")
    vid = f"{REV}/reel_{NOME}_{REV}.mp4"
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate",
                                    "-of", "json", vid], capture_output=True, text=True).stdout)
    i, tp = medir(vid)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-af", "astats=metadata=0:reset=0", "-f", "null", "-"], capture_output=True, text=True)
    ft = TTFont(os.path.join(REMOTION, "node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2"))
    upm, cmap, hm = ft["head"].unitsPerEm, ft.getBestCmap(), ft["hmtx"]
    larg = lambda s: sum(hm[cmap.get(ord(ch), cmap[ord("?")])][0] for ch in s) / upm * 66
    leg = [(" ".join(w["t"] for w in g["p"]), round(larg("\u00a0".join(w["t"] for w in g["p"])))) for g in p["legendas"]]
    durs = [(c["id"], round((c["fim_q"] - c["ini_q"]) / FPS, 2)) for c in p["cenas"]]
    # cortes detectados no vídeo final × início das cenas
    sc = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-vf", "scale=270:480,select='gt(scene,0.25)',metadata=print:file=-", "-an", "-f", "null", "-"],
                        capture_output=True, text=True).stdout
    cortes = [float(x) for x in re.findall(r"pts_time:([\d.]+)", sc)]
    desvios = []
    for c in p["cenas"][1:]:
        t = c["ini_q"] / FPS
        perto = min(cortes, key=lambda x: abs(x - t)) if cortes else None
        desvios.append({"cena": c["id"], "inicio": round(t, 3), "corte_detectado": perto, "desvio_s": round(abs(perto - t), 3) if perto is not None else None})
    out = {"arquivo": vid, "ffprobe": pr, "lufs": i, "pico_dbtp": tp, "cenas": durs, "legendas": leg, "maior_legenda_px": max(x[1] for x in leg),
           "cortes": desvios}
    json.dump(out, open("_tmp/conferir.json", "w"), ensure_ascii=False, indent=1)
    print(f"  {vid}: {float(pr['format']['duration']):.2f} s · {i:.1f} LUFS · pico {tp:.1f} dBTP")
    print(f"  cenas: menor {min(d for _, d in durs):.2f} s, maior {max(d for _, d in durs):.2f} s, média {np.mean([d for _, d in durs]):.2f} s")
    print(f"  legendas: {len(leg)} grupos, a maior {out['maior_legenda_px']} px")
    ok = [d for d in desvios if d["desvio_s"] is not None and d["desvio_s"] <= 0.05]
    print(f"  cortes: {len(ok)} de {len(desvios)} no quadro da cena (±0,05 s); sem corte detectado: "
          + ", ".join(f"{d['cena']}({d['desvio_s']})" for d in desvios if d not in ok))


if __name__ == "__main__":
    passo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    passos = {"props": props, "broll": broll, "sons": sons, "render": render, "master": master, "capa": capa, "quadros": quadros, "conferir": conferir}
    if passo == "tudo":
        for k in ["props", "broll", "sons", "props", "render", "master", "capa", "quadros", "conferir"]:
            passos[k]()
    else:
        passos[passo]()
