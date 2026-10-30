#!/usr/bin/env python3
"""Reel de Socotra · REV1 · tela dividida (docs/FORMATOS_REELS.md), a partir do pipeline do Reel do Gaudí.

Pipeline (rode de dentro de reels/socotra/rev1/):
    python3 scripts/reel.py preparar   # voz (decupagem, restauro, ruído, loudness), vídeo do Diego, B-roll, fotos, legendas → _tmp/public
    python3 scripts/reel.py render     # Remotion (design-system/remotion, composição "ReelSocotra")
    python3 scripts/reel.py master     # −14 LUFS integrados, pico ≤ −1 dBTP → reel_socotra_rev1.mp4
    python3 scripts/reel.py capa       # capa 1080 × 1920
    python3 scripts/reel.py quadros    # folha de QA (qa/) e quadro a cada 1 s
    python3 scripts/reel.py tudo

Entradas: edicao.json (falas e áudio), cenas.json (imagens por fala), transcricao_alinhada.json (palavras com tempo),
imagens/ (fotos do Commons, scripts/baixar_imagens.py) e os brutos em ../fonte/ (fora do git; baixar do Drive pelo drive_id).
"""
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "scripts"))
import sons as SONS  # noqa: E402
import voz as VOZ  # noqa: E402

FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_socotra_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_socotra_rev1_previa.mp4")
CAPA = os.path.join(AQUI, "capa_socotra_rev1.jpg")
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")

# HLG (tomadas do iPhone, BT.2020) → SDR BT.709 com tone mapping Möbius (o mesmo do Reel Anne Frank)
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
           "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv")
SAIDA_X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p",
              "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd, capturar=False):
    texto = " ".join(cmd)
    print("  $", texto if len(texto) < 200 else texto[:200] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def ler(nome):
    with open(os.path.join(AQUI, nome), encoding="utf-8") as f:
        return json.load(f)


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def loudness(entrada, saida, alvo, pico, pre="", video=False, codec=("-c:a", "pcm_s24le")):
    """Ganho linear até `alvo` LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ `pico` dBTP)."""
    i0, _ = medir(entrada)
    ganho, teto = alvo - i0, pico - 0.4
    for _ in range(5):
        af = (f"{pre}volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        extra = ["-c:v", "copy"] if video else []
        sh(["ffmpeg", "-v", "error", "-y", "-i", entrada, *extra, "-af", af, *codec, "-ar", "48000", *(["-movflags", "+faststart"] if video else []), saida])
        i, tp = medir(saida)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    return i0, i, tp, ganho


# ---------------------------------------------------------------- âncoras e legendas

def resolver(ancora, palavras, fim_falas):
    """'f2:Gaudí-0.06' → segundos no Reel. Aceita número, 'fim' e '#n' para a n-ésima ocorrência na fala."""
    if isinstance(ancora, (int, float)):
        return float(ancora)
    if ancora == "fim":
        return fim_falas
    m = re.fullmatch(r"(f\d+):([^#+\-]+?)(?:#(\d+))?([+-][\d.]+)?", ancora)
    if not m:
        sys.exit(f"âncora inválida: {ancora}")
    fala, palavra, n, desloc = m.group(1), m.group(2).lower(), int(m.group(3) or 1), float(m.group(4) or 0)
    for w in palavras:
        if w["fala"] == fala and w["texto"].strip(",.?!").lower() == palavra and w["n"] == n:
            return w["ini"] + desloc
    sys.exit(f"palavra não encontrada: {ancora}")


FUNCIONAIS = {"a", "à", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e", "em", "com", "que", "se", "para", "pra",
              "por", "pela", "num", "na", "no", "nem", "mais", "esse", "foi", "era", "ele", "quem", "aí", "todo", "tem", "sem", "quando",
              "junto", "não", "é", "até", "já", "isso"}
JUNTOS = {("sangue", "de"), ("de", "dragão"), ("lugar", "do"), ("do", "mundo"), ("outro", "lugar"), ("ficção", "científica"), ("não", "é"), ("é", "pandora"), ("nenhum", "planeta"), ("viu", "de"), ("que", "já")}
MAX_CHARS, MAX_PALAVRAS = 24, 4


def quebrar(frase):
    """Divide uma frase (até a pontuação) em grupos de 1 a 4 palavras e até 24 caracteres (1 linha na tela), com o menor
    custo: grupos de tamanho parecido, sem terminar em palavra funcional e sem separar nomes ("Sagrada Família")."""
    n = len(frase)
    melhor = [0.0] + [1e18] * n
    corte = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - MAX_PALAVRAS), j):
            g = frase[i:j]
            chars = sum(len(w["texto"]) for w in g) + len(g) - 1
            if chars > MAX_CHARS and j - i > 1:
                continue
            custo = (MAX_CHARS - chars) ** 2 / 10
            ult = re.sub(r"[,.?!]", "", g[-1]["texto"]).lower()
            if j < n and ult in FUNCIONAIS:
                custo += 60
            if j < n and (ult, re.sub(r"[,.]", "", frase[j]["texto"]).lower()) in JUNTOS:
                custo += 200
            if j - i == 1 and ult in FUNCIONAIS:
                custo += 80
            if any(w["texto"].lower() == "e" for w in g[1:]) and ("carne", "e") not in {(re.sub(r"[,.]", "", a["texto"]).lower(), b["texto"].lower()) for a, b in zip(g, g[1:])}:
                custo += 40  # "e" no meio do grupo: a oração nova começa no grupo seguinte
            if melhor[i] + custo < melhor[j]:
                melhor[j], corte[j] = melhor[i] + custo, i
    grupos, j = [], n
    while j > 0:
        grupos.append(frase[corte[j]:j])
        j = corte[j]
    return grupos[::-1]


def grupos_legenda(c, palavras):
    """Legenda de 1 a 4 palavras por vez (padrão do Reel Anne Frank: 1–3 palavras, 1 linha), frase a frase.
    A fala do gancho (f1) fica de fora: o gancho é o próprio texto na tela."""
    escrita = c["legenda"]["escrita"]
    dest = {x.lower() for x in c["legenda"]["destaques"]}
    frases, atual = [], []
    for w in palavras:
        if w["fala"] in c["legenda"]["sem_legenda"]:
            continue
        texto = w["texto"]
        if texto.startswith("-") and atual:  # "guarda" + "-chuva" (o Whisper separa): uma palavra só na legenda
            atual[-1]["texto"] += texto
            atual[-1]["fim"] = w["fim"]
            atual[-1]["destaque"] = atual[-1]["texto"].lower().strip(",.?") in dest
            continue
        nucleo, pont = re.match(r"^(.*?)([,.?!]?)$", texto).groups()
        chave = f"{w['fala']}:{nucleo}"
        if chave in escrita or nucleo in escrita:
            nucleo = escrita.get(chave, escrita.get(nucleo))
            if not nucleo:
                continue  # "um quarto" → "1/4": a palavra sai da legenda, a fala não muda
            texto = nucleo + pont
        if atual and atual[0]["fala"] != w["fala"]:
            frases.append(atual)
            atual = []
        atual.append({"texto": texto, "ini": w["ini"], "fim": w["fim"], "destaque": nucleo.lower() in dest, "fala": w["fala"]})
        if pont:
            frases.append(atual)
            atual = []
    if atual:
        frases.append(atual)
    grupos = [{"palavras": [dict(w) for w in g], "ini": g[0]["ini"]} for f in frases for g in quebrar(f)]
    for i, g in enumerate(grupos):
        prox = grupos[i + 1]["ini"] if i + 1 < len(grupos) else g["palavras"][-1]["fim"] + 0.5
        g["fim"] = round(min(prox, g["palavras"][-1]["fim"] + 0.5), 3)
        for w in g["palavras"]:
            w.pop("fala", None)
    return grupos


# ---------------------------------------------------------------- preparar

def preparar():
    d, c = ler("edicao.json"), ler("cenas.json")
    fps, W, H = d["fps"], d["largura"], d["altura"]
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "img"))
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em fonte/. Baixe do Drive:")
        for f in faltando:
            if f["arquivo"].startswith("acervo/"):
                print(f"  python3 scripts/trecho_drive.py {f['drive_id']} fonte/{f['arquivo']} 1410 1620")
            else:
                print(f"  curl -L -o fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    # 1. Voz: decupagem e restauro (voz.py) → redução leve de ruído, passa-alta, loudness e limitador
    bruta, trechos, palavras, fim_falas = VOZ.processar(d, FONTE)
    au = d["audio"]
    limpa = os.path.join(TMP, "voz_limpa.wav")
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruta, "-af", f"highpass=f={au['passa_alta_hz']},{au['reducao_ruido']}", "-c:a", "pcm_s24le", limpa])
    # mono → estéreo (−3 dB por canal) antes do limitador, para o teto valer em cada canal
    i0, i, tp, g = loudness(limpa, os.path.join(PUBLIC, "voz.wav"), au["voz_lufs"], au["voz_pico_dbtp"], pre="pan=stereo|c0=0.7071*c0|c1=0.7071*c0,")
    print(f"voz: {i0:.1f} → {i:.1f} LUFS ({g:+.1f} dB) · pico verdadeiro {tp:.1f} dBTP · {fim_falas:.3f} s")

    # 2. Vídeo do Diego: os mesmos trechos da voz (sincronia), 1080 × 1920, concatenados com corte seco
    lista = []
    for k, tr in enumerate(trechos):
        src = os.path.join(FONTE, d["fontes"][tr["fonte"]]["arquivo"])
        v = os.path.join(TMP, f"fala_{k:02d}.mp4")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{tr['in']:.4f}", "-i", src, "-vf",
            f"{TONEMAP},scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1", "-frames:v", str(tr["quadros"]), "-an", *SAIDA_X264, v])
        lista.append(v)
    with open(os.path.join(TMP, "concat.txt"), "w") as f:
        f.writelines(f"file '{v}'\n" for v in lista)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "concat.txt"), "-c", "copy", os.path.join(PUBLIC, "fala.mp4")])

    # 3. Cenas: tempos pelas palavras
    total = fim_falas + c["cta"]["cauda"]
    if total > d["duracao_max"] + 1e-6:
        sys.exit(f"duração {total:.3f} s > {d['duracao_max']} s")
    cenas = []
    for cc0 in c["cenas"]:
        cc = dict(cc0)
        cc["ini_s"] = resolver(cc0["ini"], palavras, fim_falas)
        if "marcos" in cc0:
            cc["marcos"] = {n: round(resolver(v, palavras, fim_falas) - cc["ini_s"], 3) for n, v in cc0["marcos"].items()}
        cenas.append(cc)
    for k, cc in enumerate(cenas):
        fim = cenas[k + 1]["ini_s"] if k + 1 < len(cenas) else total
        cc["ini_q"] = round(cc["ini_s"] * fps)
        cc["fim_q"] = round(fim * fps)
        if cc["fim_q"] <= cc["ini_q"]:
            sys.exit(f"cena {cc['id']} sem duração")

    # 4. B-roll do acervo: trecho mudo, recortado na proporção da camada (tela cheia ou metade de cima)
    costura = d["costura_y"]
    for cc in cenas:
        if cc["tipo"] != "broll":
            continue
        b = c["broll"][cc["broll"]]
        src = os.path.join(FONTE, d["fontes"][b["fonte"]]["arquivo"])
        n = (round(total * fps) if cc.get("continua") else cc["fim_q"]) - cc["ini_q"]
        lw, lh = (W, H) if cc["layout"] == "full" else (W, costura)
        w0, h0 = 3840, 2160
        # recorte: altura = fração `quadro` da altura do original, na proporção da camada, centrado em foco
        ch = round(h0 * b.get("quadro", 1.0) / 2) * 2
        cw = round(ch * lw / lh / 2) * 2
        if cw > w0:
            cw, ch = w0, round(w0 * lh / lw / 2) * 2
        cx = min(max(0, round(b["foco"][0] * w0 - cw / 2)), w0 - cw)
        cy = min(max(0, round(b["foco"][1] * h0 - ch / 2)), h0 - ch)
        vf = []
        if b.get("vel", 1) != 1:
            vf.append(f"setpts=PTS/{b['vel']}")
        vf += [TONEMAP, f"crop={cw}:{ch}:{cx}:{cy},scale={lw}:{lh}:flags=lanczos,fps={fps},format=yuv420p,setsar=1"]
        arq = f"broll_{cc['id']}.mp4"
        dur_src = n / fps * b.get("vel", 1) + 0.5
        if b["in"] + dur_src > b["max"] + 0.5:
            print(f"  ATENÇÃO {cc['id']}: precisa de {dur_src:.2f} s do bruto a partir de {b['in']} (limite {b['max']})")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['in']:.3f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n), "-an", *SAIDA_X264,
            os.path.join(PUBLIC, arq)])
        cc["arquivo"] = arq
        print(f"b-roll {cc['id']}: {b['fonte']} {b['in']}s · {n} quadros ({lw}×{lh}, recorte {cw}×{ch})")

    # 5. Fotos e ilustrações
    imgs = {}
    for k, im in c["imagens"].items():
        # até 2600 px no lado maior: sobra para o Ken Burns em tela cheia sem pesar no render
        sh(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AQUI, "imagens", im["arquivo"]), "-vf",
            "scale='if(gt(iw,ih),min(2600,iw),-2)':'if(gt(iw,ih),-2,min(2600,ih))':flags=lanczos", "-q:v", "2",
            os.path.join(PUBLIC, "img", os.path.basename(im["arquivo"]))])
        imgs[k] = {"arquivo": "img/" + os.path.basename(im["arquivo"])}

    # 6. Gancho e legendas
    gancho = []
    for b in c["gancho"]["blocos"]:
        gancho.append({"linhas": b["linhas"], "tamanhos": b["tamanhos"], "tempos": [round(resolver(x, palavras, fim_falas), 3) for x in b["tempos"]]})
    legendas = grupos_legenda(c, palavras)
    cta_ini = resolver(c["cta"]["ini"], palavras, fim_falas)

    # 7. Efeitos sonoros (REV2): "cena:<id>±s" = início da cena; "marco:<id>:<nome>" = marco da cena; ou âncora de palavra
    por_id = {cc["id"]: cc for cc in cenas}

    def quando(ancora):
        if isinstance(ancora, str) and ancora.startswith("cena:"):
            m = re.fullmatch(r"cena:([\w]+)([+-][\d.]+)?", ancora)
            return por_id[m.group(1)]["ini_q"] / fps + float(m.group(2) or 0)
        if isinstance(ancora, str) and ancora.startswith("marco:"):
            m = re.fullmatch(r"marco:([\w]+):([a-z_]+)([+-][\d.]+)?", ancora)
            return por_id[m.group(1)]["ini_q"] / fps + por_id[m.group(1)]["marcos"][m.group(2)] + float(m.group(3) or 0)
        return resolver(ancora, palavras, fim_falas)

    sons = []
    if c.get("sons"):
        sons = SONS.mixar(c["sons"], quando, total, au["voz_lufs"], os.path.join(PUBLIC, "sfx.wav"))
        print("efeitos:", ", ".join(f"{x['som']} {x['em_s']:.2f} s ({x['rel_db']} dB)" for x in sons))

    props = {
        "fps": fps, "largura": W, "altura": H, "costura": costura, "rostoY": d["rosto_y"], "quadros": round(total * fps),
        "cenas": cenas, "imagens": imgs, "gancho": gancho, "fimGancho": round(cenas[1]["ini_q"] / fps, 3), "legendas": legendas,
        "ganchoLayout": {"split": c["gancho"].get("layout") == "split", "topo": c["gancho"].get("topo", 690)}, "sfx": bool(sons), "sons": sons,
        "cta": {"ini": round(cta_ini, 3), "rotulo": c["cta"]["rotulo"], "destino": c["cta"]["destino"], "entrada": c["cta"]["entrada_ms"]},
        "mix": {"voz_lufs": au["voz_lufs"], "clack_db_rel": au["clack_db_rel"]},
    }
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {total:.3f} s ({round(total * fps)} quadros) · props em _tmp/props.json")
    for cc in cenas:
        print(f"  {cc['ini_q'] / fps:6.2f}–{cc['fim_q'] / fps:6.2f}  {cc['id']:<14} {cc['tipo']:<6} {cc.get('layout', '')}")


# ---------------------------------------------------------------- render, master, capa, quadros

def remotion(args):
    cmd = ["npx", "remotion", *args]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")", " ".join(args)[:200])
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    remotion(["render", "src/index.ts", "ReelSocotra", SAIDA_BRUTA, f"--props={os.path.join(TMP, 'props.json')}", f"--public-dir={PUBLIC}",
              "--codec=h264", "--crf=12", "--x264-preset=slow", "--audio-codec=pcm-16", "--log=warn", "--concurrency=4"])


def master():
    d = ler("edicao.json")["audio"]
    i0, i, tp, g = loudness(SAIDA_BRUTA, SAIDA, d["master_lufs"], d["master_pico_dbtp"], video=True, codec=("-c:a", "aac", "-b:a", "320k"))
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {g:+.1f} dB) → {os.path.basename(SAIDA)}")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])


def capa():
    """Quadro do gancho com a frase inteira na tela."""
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    quadro = round((p["gancho"][-1]["tempos"][-1] + 0.19) * p["fps"])  # "REAL." completo, rosto nítido (REV1: 0,35 s caía no Diego se inclinando)
    remotion(["still", "src/index.ts", "ReelSocotra", CAPA, f"--frame={quadro}", f"--props={os.path.join(TMP, 'props.json')}", f"--public-dir={PUBLIC}",
              "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"])


def quadros():
    """Folha de QA: um quadro por cena (no meio) e a folha de 1 quadro por segundo."""
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    pasta = os.path.join(AQUI, "qa")
    os.makedirs(pasta, exist_ok=True)
    tempos = [((cc["ini_q"] + cc["fim_q"]) / 2) / p["fps"] for cc in p["cenas"]]
    arqs = []
    for k, t in enumerate(tempos):
        o = os.path.join(TMP, f"q_{k:02d}.jpg")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", SAIDA, "-frames:v", "1", "-vf",
            f"scale=270:480,drawtext=text='{t:.1f}s':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", o])
        arqs.append(o)
    cols = 8
    entradas = sum((["-i", a] for a in arqs), [])
    layout = "|".join(f"{(k % cols) * 270}_{(k // cols) * 480}" for k in range(len(arqs)))
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", f"xstack=inputs={len(arqs)}:layout={layout}:fill=black", "-frames:v", "1",
        os.path.join(pasta, "folha_cenas.jpg")])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "fps=1,scale=216:384,tile=9x5", "-frames:v", "1", os.path.join(pasta, "folha_1s.jpg")])
    print(f"folhas: qa/folha_cenas.jpg ({len(arqs)} cenas) e qa/folha_1s.jpg")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"preparar": [preparar], "render": [render], "master": [master], "capa": [capa], "quadros": [quadros],
              "tudo": [preparar, render, master, capa, quadros]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
