"""Reel "Bruges não quer você lá" · prepara e renderiza uma revisão.
Uso (de dentro de reels/bruges-bate-volta): python3 scripts/reel.py rev1 [preparar|render|master|tudo]
Lê revN/cenas.json (cenas, legendas, sons, CTA), revN/edicao.json e os tempos de revN/transcricao_alinhada.json.
Saída: revN/reel_bruges-bate-volta_revN.mp4 (master −14 LUFS, pico ≤ −1 dBTP)."""
import json, os, re, subprocess, sys, unicodedata

REV = sys.argv[1]
ETAPA = sys.argv[2] if len(sys.argv) > 2 else "tudo"
FPS = 30
PUB = "public"
TONE = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
REMOTION = "../../design-system/remotion"
SONS = "../../design-system/sons/externos"
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"  # usado só se existir

C = json.load(open(f"{REV}/cenas.json"))
P = json.load(open(f"{REV}/palavras.json"))
DUR = P["duracao"]


def run(*a):
    subprocess.run(list(a), check=True)


def hdr(arq):
    s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    return "arib-std-b67" in s or "smpte2084" in s


def loudness(arq):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    pk = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    return i, pk


def duracao(arq):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout)


def lufs_evento(arq):
    """Loudness do evento (momentânea máxima, como em design-system/sons/README.md)."""
    r = subprocess.run(["ffmpeg", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    ms = [float(x) for x in re.findall(r"M:\s*(-?[\d.]+)", r)]
    return max(ms) if ms else -20.0


# ---------------------------------------------------------------- preparar
def preparar():
    os.makedirs(f"{PUB}/clipes", exist_ok=True)
    os.makedirs(f"{PUB}/fotos", exist_ok=True)
    # 1) clipes do acervo: mudos, SDR, 30 qps, 1080 de largura, só o trecho da cena (+0,3 s de folga)
    for c in C["cenas"]:
        if c["tipo"] != "broll":
            continue
        src = f"fonte/{c['fonte']}"
        dur = c["fim"] - c["ini"] + 0.3
        saida = f"{PUB}/clipes/{c['id']}.mp4"
        vf = (TONE + "," if hdr(src) else "") + f"fps={FPS},scale=1080:-2"
        run("ffmpeg", "-v", "error", "-y", "-ss", str(c["src"]), "-i", src, "-t", f"{dur:.3f}", "-vf", vf, "-an", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", saida)
        c["arquivo"] = f"clipes/{c['id']}.mp4"
    # 2) fotos (web, com licença em creditos.md) e capturas
    for nome, origem in C["fotos"].items():
        run("ffmpeg", "-v", "error", "-y", "-i", origem, "-vf", "scale='min(2400,iw)':-2", "-q:v", "2", f"{PUB}/fotos/{nome}")
    cap = C["captura_cortes"]
    for nome, (origem, x, y, w, h) in cap.items():
        run("ffmpeg", "-v", "error", "-y", "-i", origem, "-vf", f"crop={w}:{h}:{x}:{y}", "-q:v", "2", f"{PUB}/fotos/{nome}")
    # quadro parado de Bruges lotada (comparação) e fundo da captura
    for nome, (fonte, seg) in C["quadros"].items():
        src = f"fonte/{fonte}"
        vf = (TONE + "," if hdr(src) else "") + "scale=1080:-2"
        run("ffmpeg", "-v", "error", "-y", "-ss", str(seg), "-i", src, "-frames:v", "1", "-vf", vf, "-q:v", "2", f"{PUB}/fotos/{nome}")
    # 3) voz: ganho linear até −14 LUFS (o limitador fica no master)
    i, _ = loudness(f"{PUB}/voz_bruta.wav")
    ganho = -14.0 - i
    run("ffmpeg", "-v", "error", "-y", "-i", f"{PUB}/voz_bruta.wav", "-af", f"volume={ganho:.2f}dB", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", f"{PUB}/voz.wav")
    voz_lufs = -14.0
    # 4) efeitos do formato (PDX_*), relativos à voz (REFERENCIA_EDICAO_FORMATOS 4.1)
    entradas, filtros = [], []
    for k, s in enumerate(C["sons"]):
        arq = f"{SONS}/{s['som']}.wav"
        g = voz_lufs + s["rel_db"] - lufs_evento(arq)
        ini = s["em"] - (duracao(arq) if s.get("ancora_fim") else 0.0)  # riser: termina no corte
        entradas += ["-i", arq]
        filtros.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.2f}dB,adelay={max(0, round(ini * 1000))}|{max(0, round(ini * 1000))}[s{k}]")
    mix = "".join(f"[s{k}]" for k in range(len(C["sons"])))
    filtros.append(f"{mix}amix=inputs={len(C['sons'])}:normalize=0,apad=whole_dur={DUR:.3f}[out]")
    run("ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[out]", "-t", f"{DUR:.3f}", "-c:a", "pcm_s16le", f"{PUB}/sfx.wav")
    # 5) legendas: grupos de 1 a 4 palavras, uma linha (FORMATOS_REELS 6)
    legendas = grupos_legenda()
    # 6) props
    mapa = json.load(open(f"{PUB}/mapa.json"))
    props = {
        "fps": FPS,
        "quadros": round(DUR * FPS),
        "costura": 900,
        "rostoY": C["rostoY"],
        "cenas": [{k: v for k, v in c.items() if k not in ("fonte", "src", "_nota")} for c in C["cenas"]],
        "legendas": legendas,
        "semLegenda": C["sem_legenda"],
        "gancho": C["gancho"],
        "fitas": C.get("fitas"),
        "contador": C["contador"],
        "relogio": C["relogio"],
        "captura": C["captura"],
        "comparar": C["comparar"],
        "mapa": {"paises": {}, "cidades": {}} if not any(c["tipo"] == "mapa" for c in C["cenas"]) else {"paises": mapa["paises"], "cidades": mapa["cidades"]},
        "cta": C["cta"],
        "mix": {"voz_lufs": voz_lufs, "clack_db_rel": C["clack_db_rel"]},
    }
    json.dump(props, open(f"{REV}/props.json", "w"), ensure_ascii=False)
    json.dump(legendas, open(f"{REV}/legendas_queimadas.json", "w"), ensure_ascii=False, indent=1)
    print(f"preparado: {len(C['cenas'])} cenas, {len(legendas)} grupos de legenda, {len(C['sons'])} efeitos")


FUNCIONAIS = {"de", "da", "do", "das", "dos", "que", "e", "a", "o", "os", "as", "um", "uma", "em", "no", "na", "nos", "pra", "para", "com", "se", "é", "eu", "você", "me", "te", "às", "à", "mas", "por", "foi"}


def norm(w):
    return unicodedata.normalize("NFC", w)


def grupos_legenda():
    ws = json.load(open(f"{REV}/transcricao_alinhada.json"))
    troca = C["legenda_texto"]  # correções de grafia da fala gravada (a fala manda; só a escrita muda)
    destaques = [d.lower() for d in C["legenda_destaques"]]
    pal = []
    for i, w in enumerate(ws):
        txt = troca.get(f"{i}", w["w"])
        if txt == "":
            continue
        pal.append({"texto": norm(txt), "ini": w["s"], "fim": w["e"], "i": i})
    # quebra por custo mínimo dentro de cada frase (pontuação fecha a frase)
    frases, cur = [], []
    for w in pal:
        cur.append(w)
        if re.search(r"[.?!,]$", w["texto"]) or (len(cur) and w is pal[-1]):
            frases.append(cur)
            cur = []
    if cur:
        frases.append(cur)
    grupos = []
    for f in frases:
        n = len(f)
        best = [(0.0, -1)] + [(1e9, -1)] * n
        for j in range(1, n + 1):
            for i in range(max(0, j - 4), j):
                g = f[i:j]
                txt = " ".join(x["texto"] for x in g)
                custo = abs(len(txt) - 17) * 0.6 + (8 if len(txt) > 24 else 0)
                ult = re.sub(r"[^\wÀ-ÿ]", "", g[-1]["texto"].lower())
                if j < n and ult in FUNCIONAIS:
                    custo += 16
                for par in C["nao_separar"]:  # expressões que não se separam ("Porto da", "bate e")
                    if j < n and f"{g[-1]['texto']} {f[j]['texto']}".lower().strip(".,?") .startswith(par.lower()):
                        custo += 10
                c = best[i][0] + custo
                if c < best[j][0]:
                    best[j] = (c, i)
        cortes, j = [], n
        while j > 0:
            i = best[j][1]
            cortes.append((i, j))
            j = i
        for i, j in reversed(cortes):
            g = f[i:j]
            grupos.append(g)
    out = []
    for k, g in enumerate(grupos):
        ini = g[0]["ini"] - 0.04
        fim = grupos[k + 1][0]["ini"] - 0.04 if k + 1 < len(grupos) else g[-1]["fim"] + 0.4
        fim = min(fim, g[-1]["fim"] + 0.5)
        palavras = []
        for x in g:
            limpo = re.sub(r"[^\wÀ-ÿ]", "", x["texto"].lower())
            palavras.append({"texto": x["texto"].rstrip(".,") if not x["texto"].endswith("?") else x["texto"], "destaque": limpo in destaques})
        out.append({"palavras": palavras, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


# ---------------------------------------------------------------- render e master
def render():
    os.makedirs("_tmp", exist_ok=True)
    env = dict(os.environ)
    args = ["npx", "remotion", "render", "src/index.ts", "ReelBruges", os.path.abspath(f"_tmp/{REV}_render.mp4"),
            f"--props={os.path.abspath(f'{REV}/props.json')}", f"--public-dir={os.path.abspath(PUB)}", "--concurrency=4", "--crf=16", "--log=error"]
    if os.path.exists(CHROME):
        args.append(f"--browser-executable={CHROME}")
    subprocess.run(args, cwd=REMOTION, check=True, env=env)


def master():
    src = f"_tmp/{REV}_render.mp4"
    i, _ = loudness(src)
    g = -14.0 - i
    out = f"{REV}/reel_bruges-bate-volta_{REV}.mp4"
    # ganho linear + limitador com sobreamostragem 4× (FORMATOS_REELS 10.1)
    af = f"volume={g:.2f}dB,aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=disabled,aresample=48000"
    run("ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", out)
    i2, pk = loudness(out)
    print(f"master: {i2:.1f} LUFS, pico {pk:.1f} dBTP → {out}")


if ETAPA in ("preparar", "tudo"):
    preparar()
if ETAPA in ("render", "tudo"):
    render()
if ETAPA in ("master", "tudo"):
    master()
