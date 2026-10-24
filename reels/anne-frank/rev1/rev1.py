#!/usr/bin/env python3
"""Reel "Casa de Anne Frank" · REV1 (tela dividida).

Pipeline (rode de dentro desta pasta):
    python3 rev1.py preparar   # fala (7 takes), B-roll mudo, fotos e legendas em _tmp/public
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "ReelAnneFrank")
    python3 rev1.py master     # loudness do master: −14 LUFS integrados, pico ≤ −1 dBTP
    python3 rev1.py capa       # capa 1080 × 1920
    python3 rev1.py quadros    # folha de quadros para QA (qa_frames/)
    python3 rev1.py tudo

Entradas: rev1.json (decisões), transcricao_large-v3.json (palavras com tempo) e os brutos em ../fonte/
(fora do git; baixar do Drive pelo `drive_id` de cada fonte). Só usa a biblioteca padrão do Python, ffmpeg e Node.
"""
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_anne-frank_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_anne-frank_rev1_previa.mp4")
CAPA = os.path.join(AQUI, "capa_anne-frank_rev1.jpg")
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")

# HLG (iPhone, BT.2020) → SDR BT.709 com tone mapping Möbius (o mesmo do madrid-show/rev1).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)
SAIDA_X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p",
              "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd, capturar=False):
    texto = " ".join(cmd)
    print("  $", texto if len(texto) < 240 else texto[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,color_transfer:stream_side_data=rotation",
            "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    w, h = s["width"], s["height"]
    if rot % 180:
        w, h = h, w
    return w, h, s.get("color_transfer", "")


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return i, float(p[-1]) if p else None


# ---------------------------------------------------------------- linha do tempo

def linha_do_tempo(d):
    """Início de cada fala no Reel (s), alinhado a quadros, e as palavras com tempo no Reel."""
    fps = d["fps"]
    with open(os.path.join(AQUI, "transcricao_large-v3.json"), encoding="utf-8") as f:
        tr = json.load(f)
    falas, palavras = [], []
    t = 0.0
    for fa in d["falas"]:
        n = round((fa["out"] - fa["in"]) * fps)
        dur = n / fps
        ws = tr[fa["fonte"]]["palavras"]
        cont = {}
        for j, (ini, fim, txt, prob) in enumerate(ws):
            # O Whisper prende a 1ª palavra em 0,00 s; a voz começa de fato em `inicio_voz` (energia do áudio).
            if j == 0:
                ini = fa["inicio_voz"]
            limpo = txt.strip()
            cont[limpo] = cont.get(limpo, 0) + 1
            palavras.append({"fala": fa["id"], "texto": limpo, "n": cont[limpo], "ini": round(t + ini - fa["in"], 3),
                             "fim": round(t + min(fim, fa["out"]) - fa["in"], 3), "prob": prob})
        falas.append(dict(fa, quadros=n, dur=dur, inicio=round(t, 4)))
        t += dur
    return falas, palavras, t


def resolver(ancora, palavras, fim_falas):
    """'f2:mas-0.06' → segundos no Reel. Aceita número, 'fim' e '#n' para a n-ésima ocorrência."""
    if isinstance(ancora, (int, float)):
        return float(ancora)
    if ancora == "fim":
        return fim_falas
    m = re.fullmatch(r"(f\d+):([^#+\-]+)(?:#(\d+))?([+-][\d.]+)?", ancora)
    if not m:
        sys.exit(f"âncora inválida: {ancora}")
    fala, palavra, n, desloc = m.group(1), m.group(2), int(m.group(3) or 1), float(m.group(4) or 0)
    for w in palavras:
        if w["fala"] == fala and re.sub(r"[,.]", "", w["texto"]) == palavra and w["n"] == n:
            return w["ini"] + desloc
    sys.exit(f"palavra não encontrada: {ancora}")


FUNCIONAIS = {"a", "à", "o", "as", "os", "aos", "um", "uma", "de", "da", "do", "das", "dos", "e", "em", "com", "que", "se",
              "para", "por", "sobre", "sua", "suas", "mais", "essa", "esse", "foi", "é", "era",
              "anne", "otto", "13", "dois", "história"}  # e nomes e números que pedem a palavra seguinte


def grupos_legenda(d, palavras):
    """Legenda de 1 a 3 palavras (como nas referências), quebrando na pontuação. A fala do gancho fica de fora:
    o próprio gancho é o texto na tela."""
    corr = d["correcoes_legenda"]
    dest = set(d["destaques"])
    grupos, atual = [], []

    def fecha():
        if atual:
            grupos.append({"palavras": [dict(w) for w in atual], "ini": atual[0]["ini"]})
            atual.clear()

    for w in palavras:
        if w["fala"] == "f1":
            continue
        chave = f"{w['fala']}:{re.sub(r'[,.]', '', w['texto'])}"
        texto = w["texto"]
        if chave in corr:
            pont = re.findall(r"[,.]$", texto)
            texto = corr[chave] + (pont[0] if pont else "")
        item = {"texto": texto, "ini": w["ini"], "fim": w["fim"], "destaque": w["texto"] in dest}
        if atual and (atual[0]["fala"] if "fala" in atual[0] else None) != w["fala"]:
            fecha()
        item["fala"] = w["fala"]
        if atual and sum(len(x["texto"]) + 1 for x in atual) + len(texto) > 24:
            fecha()  # grupo de no máximo ~24 caracteres (1 linha na tela)
        atual.append(item)
        chars = sum(len(x["texto"]) + 1 for x in atual)
        # não termina grupo em artigo, preposição ou conjunção ("casa bonita à" / "beira de um")
        solta = texto.lower() in FUNCIONAIS
        if re.search(r"[,.]$", texto) or len(atual) >= 5 or ((len(atual) >= 3 or chars > 16) and not solta):
            fecha()
    fecha()
    for i, g in enumerate(grupos):
        prox = grupos[i + 1]["ini"] if i + 1 < len(grupos) else g["palavras"][-1]["fim"] + 0.4
        g["fim"] = round(min(prox, g["palavras"][-1]["fim"] + 0.5), 3)
        for w in g["palavras"]:
            w.pop("fala", None)
    return grupos


# ---------------------------------------------------------------- preparar

def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "img"))
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/. Baixe do Drive:")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    falas, palavras, fim_falas = linha_do_tempo(d)

    # 1. Fala: cada take recortado no quadro, HLG → SDR, 1080 × 1920; depois concatenados (corte seco).
    lista_v, lista_a = [], []
    for fa in falas:
        src = os.path.join(FONTE, d["fontes"][fa["fonte"]]["arquivo"])
        v = os.path.join(TMP, f"fala_{fa['id']}.mp4")
        a = os.path.join(TMP, f"fala_{fa['id']}.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{fa['in']:.3f}", "-i", src, "-vf",
            f"{TONEMAP},scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1", "-frames:v", str(fa["quadros"]), "-an", *SAIDA_X264, v])
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{fa['in']:.3f}", "-i", src, "-vn", "-ac", "2", "-ar", "48000", "-af",
            f"apad,atrim=0:{fa['dur']:.5f},afade=t=in:d=0.012,afade=t=out:st={fa['dur'] - 0.06:.4f}:d=0.06", "-c:a", "pcm_s24le", a])
        lista_v.append(v)
        lista_a.append(a)
    with open(os.path.join(TMP, "concat.txt"), "w") as f:
        f.writelines(f"file '{v}'\n" for v in lista_v)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "concat.txt"), "-c", "copy",
        os.path.join(PUBLIC, "fala.mp4")])
    voz_bruta = os.path.join(TMP, "voz_bruta.wav")
    entradas = sum((["-i", a] for a in lista_a), [])
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", f"concat=n={len(lista_a)}:v=0:a=1", "-c:a", "pcm_s24le", voz_bruta])
    medido, _ = lufs(voz_bruta)
    ganho = d["mix"]["voz_lufs"] - medido
    sh(["ffmpeg", "-v", "error", "-y", "-i", voz_bruta, "-af", f"highpass=f=70,volume={ganho:.2f}dB", "-c:a", "pcm_s24le",
        os.path.join(PUBLIC, "voz.wav")])
    print(f"voz: {medido:.1f} LUFS → {d['mix']['voz_lufs']} LUFS ({ganho:+.1f} dB) · {fim_falas:.3f} s")

    # 2. Cenas: tempos resolvidos pelas palavras.
    cta_dur = d["cta"]["duracao"]
    total = fim_falas + cta_dur
    cenas = []
    for c in d["cenas"]:
        cc = dict(c)
        cc["ini_s"] = resolver(c["ini"], palavras, fim_falas)
        for k in ("marcos",):
            if k in c:
                cc[k] = {n: round(resolver(v, palavras, fim_falas) - cc["ini_s"], 3) for n, v in c[k].items()}
        if "numero" in c:
            cc["numero"] = dict(c["numero"], em=round(resolver(c["numero"]["em"], palavras, fim_falas) - cc["ini_s"], 3))
        cenas.append(cc)
    for i, cc in enumerate(cenas):
        fim = cenas[i + 1]["ini_s"] if i + 1 < len(cenas) else total
        cc["ini_q"] = round(cc["ini_s"] * fps)
        cc["fim_q"] = round(fim * fps)
        if cc["fim_q"] <= cc["ini_q"]:
            sys.exit(f"cena {cc['id']} sem duração")

    # 3. B-roll: o trecho de cada cena, mudo, no enquadramento da camada (tela cheia ou metade de cima).
    costura = d["costura_y"]
    for cc in cenas:
        if cc["tipo"] != "broll" and not (cc["tipo"] == "cta"):
            continue
        b = d["broll"][cc["broll"] if cc["tipo"] == "broll" else "entardecer"]
        if cc["tipo"] == "cta":
            # o CTA continua o último plano (entardecer) sem corte
            continue
        src = os.path.join(FONTE, d["fontes"][b["fonte"]]["arquivo"])
        w0, h0, trc = sonda(src)
        n = cc["fim_q"] - cc["ini_q"]
        # o plano do entardecer segue por baixo do CTA
        if cc["id"] == "marcas":
            n = round(total * fps) - cc["ini_q"]
        lw, lh = (W, H) if b["layout"] == "full" else (W, costura)
        # recorte na proporção da camada, centrado em foco_x
        if w0 / h0 > lw / lh:
            cw, ch = round(h0 * lw / lh / 2) * 2, h0
        else:
            cw, ch = w0, round(w0 * lh / lw / 2) * 2
        cx = min(max(0, round(b["foco_x"] * w0 - cw / 2)), w0 - cw)
        cy = (h0 - ch) // 2
        vf = []
        if b.get("vel", 1) != 1:
            vf.append(f"setpts=PTS/{b['vel']}")
        if "b67" in trc:
            vf.append(TONEMAP)
        vf.append(f"crop={cw}:{ch}:{cx}:{cy},scale={lw}:{lh}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
        arq = f"broll_{cc['id']}.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['in']:.3f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n), "-an",
            *SAIDA_X264, os.path.join(PUBLIC, arq)])
        cc["arquivo"] = arq
        cc["layout"] = b["layout"]
        print(f"b-roll {cc['id']}: {b['fonte']} {n} quadros ({lw}×{lh})")

    # 4. Fotos (licenças em QA_REV1.md)
    imgs = {}
    for k, im in d["imagens"].items():
        shutil.copy(os.path.join(AQUI, "imagens", im["arquivo"]), os.path.join(PUBLIC, "img", im["arquivo"]))
        imgs[k] = dict(im, arquivo="img/" + im["arquivo"])

    # 5. Gancho e legendas
    gancho = [dict(b, em=round(resolver(b["em"], palavras, fim_falas), 3)) for b in d["gancho"]["blocos"]]
    legendas = grupos_legenda(d, palavras)

    props = {
        "fps": fps, "largura": W, "altura": H, "costura": costura, "rostoY": d["rosto_y"],
        "quadros": round(total * fps), "fimFalas": round(fim_falas, 3),
        "falas": [{"id": f["id"], "inicio": f["inicio"], "dur": f["dur"]} for f in falas],
        "cenas": cenas, "imagens": imgs, "gancho": gancho, "legendas": legendas,
        "cta": dict(d["cta"], ini=round(fim_falas, 3)),
        "mix": d["mix"],
    }
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    with open(os.path.join(TMP, "palavras.json"), "w", encoding="utf-8") as fp:
        json.dump(palavras, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {total:.3f} s ({round(total * fps)} quadros) · props em _tmp/props.json")
    for cc in cenas:
        print(f"  {cc['ini_q'] / fps:6.2f}–{cc['fim_q'] / fps:6.2f}  {cc['id']:<12} {cc['tipo']}")


# ---------------------------------------------------------------- render, master, capa

def remotion(args):
    cmd = ["npx", "remotion", *args]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")", " ".join(args)[:200])
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    props = os.path.join(TMP, "props.json")
    remotion(["render", "src/index.ts", "ReelAnneFrank", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
              "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn", "--concurrency=4"])


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def master():
    """Ganho linear até −14 LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP)."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(SAIDA_BRUTA)
    ganho = alvo - i0
    teto = pico - 0.4
    for _ in range(4):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", SAIDA])
        i, tp = medir_master(SAIDA)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {ganho:+.1f} dB) → {os.path.basename(SAIDA)}")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])


def capa():
    props = os.path.join(TMP, "props.json")
    remotion(["still", "src/index.ts", "CapaAnneFrank", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg",
              "--jpeg-quality=92", "--log=warn"])


def quadros():
    """Folha de QA: um quadro por cena (no meio) e um no início do CTA."""
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    pasta = os.path.join(AQUI, "qa_frames")
    os.makedirs(pasta, exist_ok=True)
    tempos = [((c["ini_q"] + c["fim_q"]) / 2) / p["fps"] for c in p["cenas"]] + [p["cta"]["ini"] + 2.0]
    arqs = []
    for i, t in enumerate(tempos):
        o = os.path.join(TMP, f"q_{i:02d}.jpg")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", SAIDA, "-frames:v", "1", "-vf",
            f"scale=270:480,drawtext=text='{t:.1f}s':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", o])
        arqs.append(o)
    cols = 7
    linhas = (len(arqs) + cols - 1) // cols
    entradas = sum((["-i", a] for a in arqs), [])
    layout = "|".join(f"{(k % cols) * 270}_{(k // cols) * 480}" for k in range(len(arqs)))
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex",
        f"xstack=inputs={len(arqs)}:layout={layout}:fill=black", "-frames:v", "1", os.path.join(pasta, "folha_rev1.jpg")])
    print(f"folha: qa_frames/folha_rev1.jpg ({len(arqs)} quadros, {linhas} linhas)")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"preparar": [preparar], "render": [render], "master": [master], "capa": [capa], "quadros": [quadros],
              "tudo": [preparar, render, master, capa, quadros]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
