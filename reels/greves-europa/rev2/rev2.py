#!/usr/bin/env python3
"""Reel "Greves na Europa: confira antes de sair" · REV2 (voz do Diego): versão Tela Verde e versão Narrada.

Pipeline (rode de dentro desta pasta):
    python3 rev2.py fala       # transcrição com tempo de cada palavra (faster-whisper large-v3) → fala/transcricao.json
    python3 rev2.py recorte    # recorte do Diego (RobustVideoMatting ResNet50, ONNX) → ../fonte/gravacao/recorte/*.webm
    python3 rev2.py rosto      # mede o rosto em cada recorte → valores de `queixo` em rev2.json (legenda fora do rosto)
    python3 rev2.py preparar   # voz, recortes por tomada, cenas, trilha, efeitos e props em _tmp/
    python3 rev2.py props      # só refaz _tmp/props_*.json (reaproveita o que já foi gerado)
    python3 rev2.py render     # Remotion monta as duas versões (composição "ReelGrevesV2")
    python3 rev2.py master     # −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev2.py previa     # prévias 540 × 960
    python3 rev2.py srt        # captions.srt (mesmos grupos da legenda da tela)
    python3 rev2.py quadros    # folhas de quadros para QA (qa_frames/)
    python3 rev2.py tudo       # preparar → quadros (fala e recorte são feitos uma vez)

Entradas: rev2.json (decisões), fala/transcricao.json, ../rev1/assets (mapa e prints), assets/prints (captura da CP)
e os brutos em ../fonte/ (fora do git): gravacao/IMG_70xx.MOV (Drive, pasta "Reel") e mixkit/*.mp4.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
REV1 = os.path.normpath(os.path.join(AQUI, "..", "rev1"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
FALA = os.path.join(AQUI, "fala", "transcricao.json")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SRT = os.path.join(AQUI, "captions.srt")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SR = 48000
MODELO_RECORTE = os.environ.get("RVM_ONNX", "rvm_resnet50_fp32.onnx")  # github.com/PeterL1n/RobustVideoMatting, release v1.0.0

# HLG (iPhone, BT.2020) → SDR BT.709, igual à REV1 (npl 203 + Hable)
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False):
    txt = " ".join(cmd)
    print("  $", txt if len(txt) < 240 else txt[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev2.json"), encoding="utf-8") as f:
        return json.load(f)


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return i, float(p[-1]) if p else None


def bruto(tk):
    return os.path.join(FONTE, tk["arquivo"])


# ---------------------------------------------------------------- fala e recorte (feitos uma vez)

def fala():
    """Transcrição automática com tempo por palavra. Continua sendo automática: a validação auditiva é humana."""
    import numpy as np
    from faster_whisper import WhisperModel
    d = carregar()
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
    out = {}
    for nome, tk in d["tomadas"].items():
        wav = os.path.join(TMP, f"fala_{nome}.wav")
        os.makedirs(TMP, exist_ok=True)
        sh(["ffmpeg", "-v", "error", "-y", "-i", bruto(tk), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])
        with wave.open(wav) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        segs, _ = m.transcribe(a, language="pt", word_timestamps=True, beam_size=5)
        out[nome] = [{"w": x.word.strip(), "t": round(x.start, 2), "fim": round(x.end, 2)} for s in segs for x in s.words]
        print(nome, " ".join(f"{i}:{p['w']}" for i, p in enumerate(out[nome])))
    os.makedirs(os.path.dirname(FALA), exist_ok=True)
    with open(FALA, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


def recorte():
    """Recorte do Diego quadro a quadro (RVM com estado recorrente: estável no tempo) → WebM VP9 com alfa, 1080 × 1920."""
    import numpy as np
    import onnxruntime as ort
    d = carregar()
    W, H = d["largura"], d["altura"]
    for nome, tk in d["tomadas"].items():
        saida = os.path.join(FONTE, tk["recorte"])
        if os.path.exists(saida):
            print(f"{nome}: já existe ({os.path.basename(saida)})")
            continue
        os.makedirs(os.path.dirname(saida), exist_ok=True)
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", bruto(tk), "-vf", f"{TONEMAP},scale={W}:{H}:flags=lanczos,format=rgb24",
                                "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "24", "-i", "-",
                                "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "18", "-row-mt", "1",
                                "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", saida], stdin=subprocess.PIPE)
        s = ort.InferenceSession(MODELO_RECORTE, providers=["CPUExecutionProvider"])
        rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
        dr = np.array([0.25], np.float32)
        n = 0
        while True:
            b = dec.stdout.read(W * H * 3)
            if len(b) < W * H * 3:
                break
            f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
            x = (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]
            fgr, pha, *rec = s.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
            a = (np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8)
            fg = (np.clip(fgr[0].transpose(1, 2, 0), 0, 1) * 255).astype(np.uint8)
            enc.stdin.write(np.dstack([fg, a]).tobytes())
            n += 1
        enc.stdin.close()
        enc.wait()
        print(f"{nome}: {n} quadros → {os.path.basename(saida)}")


def rosto():
    """Mede o rosto do Diego quadro a quadro (YuNet, OpenCV) em cada recorte e imprime o queixo mais baixo (y da
    imagem 1080 × 1920). Esse valor vai em `tomadas.<X>.queixo` do rev2.json: a composição escala o recorte em torno
    dele e o leva para `diego.queixo_y`, acima da zona da legenda. Modelo: opencv_zoo, face_detection_yunet_2023mar."""
    import cv2
    import numpy as np
    d = carregar()
    W, H = d["largura"] // 2, d["altura"] // 2
    det = cv2.FaceDetectorYN.create(os.environ.get("YUNET_ONNX", "face_detection_yunet_2023mar.onnx"), "", (W, H), 0.6)
    for nome in d["tomadas"]:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", os.path.join(PUBLIC, f"diego_{nome}.webm"), "-vf", f"scale={W}:{H}",
                              "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
        queixos, sem = [], 0
        while True:
            b = p.stdout.read(W * H * 3)
            if len(b) < W * H * 3:
                break
            _, fs = det.detect(np.frombuffer(b, np.uint8).reshape(H, W, 3))
            if fs is None:
                sem += 1
                continue
            queixos.append(float(fs[0][1] + fs[0][3]) * 2)
        print(f"{nome}: queixo mais baixo y {max(queixos):.0f} (mediana {np.median(queixos):.0f}; {sem} quadro(s) sem rosto)")


# ---------------------------------------------------------------- tempos ancorados na fala

def carregar_fala():
    with open(FALA, encoding="utf-8") as f:
        return json.load(f)


def cortes(tk):
    """Pausas retiradas de dentro da tomada: [[ini, fim], ...] em segundos do arquivo bruto (alinhados ao quadro de 24 fps)."""
    return tk.get("cortes", [])


def dur_tomada(tk):
    return tk["out"] - tk["in"] - sum(b - a for a, b in cortes(tk))


def no_trecho(tk, t):
    """Tempo do bruto → tempo dentro do trecho já sem as pausas cortadas (contínuo: uma palavra marcada dentro da pausa vai para o ponto do corte)."""
    return t - tk["in"] - sum(min(max(t - a, 0.0), b - a) for a, b in cortes(tk))


def segmentos(tk):
    """Trechos mantidos, relativos ao início da tomada (`in`): [(ini, fim), ...]."""
    pts = [tk["in"]] + [x for c in cortes(tk) for x in c] + [tk["out"]]
    return [(pts[i] - tk["in"], pts[i + 1] - tk["in"]) for i in range(0, len(pts), 2)]


def resolver(d, fl):
    """{"take", "palavra", "desloc"} → segundos absolutos na linha do tempo do Reel (início da palavra)."""
    tks = d["tomadas"]

    def t(v):
        if isinstance(v, (int, float)):
            return float(v)
        tk = tks[v["take"]]
        return round(tk["ini"] + no_trecho(tk, fl[v["take"]][v["palavra"]]["t"]) + v.get("desloc", 0.0), 3)

    def andar(o):
        if isinstance(o, dict):
            if "take" in o and "palavra" in o and set(o) <= {"take", "palavra", "desloc"}:
                return t(o)
            return {k: andar(v) for k, v in o.items()}
        if isinstance(o, list):
            return [andar(x) for x in o]
        return o

    return andar, t


def grupos_legenda(d, fl):
    """Grupos da legenda: início na 1ª palavra, fim no início do grupo seguinte (ou 0,3 s após a última palavra)."""
    _, t = resolver(d, fl)
    gs = d["legendas"]
    out = []
    for i, g in enumerate(gs):
        t0 = t({"take": g["take"], "palavra": g["de"]})
        fim_fala = t({"take": g["take"], "palavra": g["ate"]}) + (fl[g["take"]][g["ate"]]["fim"] - fl[g["take"]][g["ate"]]["t"])
        if i + 1 < len(gs):
            prox = t({"take": gs[i + 1]["take"], "palavra": gs[i + 1]["de"]})
            t1 = prox - 0.04 if prox - fim_fala < 0.6 else fim_fala + 0.3
        else:
            t1 = min(fim_fala + 0.4, d["duracao"])
        item = {"texto": g["texto"], "ini": round(t0, 3), "fim": round(t1, 3)}
        if "destaque" in g:
            item["destaque_em"] = t({"take": g["take"], "palavra": g["destaque"]})
        out.append(item)
    return out


def grupos_uma_linha(d, fl):
    """Mesmos textos, uma linha por vez: cada linha ("|") vira um grupo que entra na 1ª palavra dela."""
    _, t = resolver(d, fl)
    linhas = []
    for g in d["legendas"]:
        w = g["de"]
        for txt in g["texto"].split("|"):
            n = len(txt.split())
            item = {"take": g["take"], "de": w, "ate": w + n - 1, "texto": txt.strip()}
            if "destaque" in g and w <= g["destaque"] <= w + n - 1:
                item["destaque"] = g["destaque"]
            linhas.append(item)
            w += n
    return grupos_legenda(dict(d, legendas=linhas), fl)


def escolher(o, layout, layouts):
    """Valores por layout ({"tela_verde": …, "narrado": …}) → o valor do layout da versão."""
    if isinstance(o, dict):
        if o and set(o) == layouts:
            return escolher(o[layout], layout, layouts)
        return {k: escolher(v, layout, layouts) for k, v in o.items()}
    if isinstance(o, list):
        return [escolher(x, layout, layouts) for x in o]
    return o


# ---------------------------------------------------------------- voz, recortes e cenas

def voz(d):
    """Voz de cada tomada: filtro leve (passa-alta, redução de ruído, compressão suave) e mesmo ganho para as três,
    medido na fala somada até −16 LUFS. Fades de 30 ms nas emendas."""
    filtro = d["mix"]["voz_filtro"]
    partes = []
    for nome, tk in d["tomadas"].items():
        arq = os.path.join(TMP, f"voz_{nome}_f.wav")
        dur = dur_tomada(tk)
        if not cortes(tk):
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{tk['in']:.3f}", "-i", bruto(tk), "-t", f"{dur:.3f}", "-vn", "-ac", "1", "-ar", str(SR),
                "-af", f"{filtro},afade=t=in:d=0.03,afade=t=out:st={dur - 0.06:.3f}:d=0.06", "-c:a", "pcm_s16le", arq])
        else:
            # filtra o trecho inteiro (a redução de ruído precisa de contexto) e só depois tira as pausas, com fades de 20 ms nas emendas
            cheio = os.path.join(TMP, f"voz_{nome}_cheio.wav")
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{tk['in']:.3f}", "-i", bruto(tk), "-t", f"{tk['out'] - tk['in']:.3f}", "-vn", "-ac", "1",
                "-ar", str(SR), "-af", filtro, "-c:a", "pcm_s16le", cheio])
            seg = segmentos(tk)
            fc = ";".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b - a - 0.02:.4f}:d=0.02[s{i}]"
                          for i, (a, b) in enumerate(seg))
            fc += ";" + "".join(f"[s{i}]" for i in range(len(seg))) + f"concat=n={len(seg)}:v=0:a=1,afade=t=in:d=0.03,afade=t=out:st={dur - 0.06:.4f}:d=0.06[o]"
            sh(["ffmpeg", "-v", "error", "-y", "-i", cheio, "-filter_complex", fc, "-map", "[o]", "-c:a", "pcm_s16le", arq])
        partes.append((nome, arq))
    lista = os.path.join(TMP, "voz_lista.txt")
    with open(lista, "w") as f:
        f.writelines(f"file '{a}'\n" for _, a in partes)
    junta = os.path.join(TMP, "voz_junta.wav")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", junta])
    medido, _ = lufs(junta)
    ganho = d["mix"]["voz_lufs"] - medido
    out = {}
    for nome, arq in partes:
        final = f"voz_{nome}.wav"
        sh(["ffmpeg", "-v", "error", "-y", "-i", arq, "-af", f"volume={ganho:.2f}dB", "-ac", "2", "-c:a", "pcm_s16le", os.path.join(PUBLIC, final)])
        out[nome] = final
    print(f"voz: {medido:.1f} LUFS → {d['mix']['voz_lufs']} LUFS ({ganho:+.1f} dB)")
    return out


def recortes_tomadas(d, reaproveitar):
    """Trecho [in, out] de cada recorte com alfa (WebM VP9). O decodificador libvpx-vp9 preserva o canal alfa."""
    out = {}
    for nome, tk in d["tomadas"].items():
        arq = f"diego_{nome}.webm"
        dest = os.path.join(PUBLIC, arq)
        if not (reaproveitar and os.path.exists(dest)):
            ent = ["-c:v", "libvpx-vp9", "-ss", f"{tk['in']:.3f}", "-i", os.path.join(FONTE, tk["recorte"]), "-t", f"{tk['out'] - tk['in'] + 0.05:.3f}"]
            codec = ["-an", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-row-mt", "1", "-deadline", "good",
                     "-cpu-used", "4", "-auto-alt-ref", "0", dest]
            if not cortes(tk):
                sh(["ffmpeg", "-v", "error", "-y"] + ent + codec)
            else:  # corte seco (jump cut) nos pontos de `cortes`, sempre em quadro inteiro
                seg = segmentos(tk)
                fc = ";".join(f"[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS[v{i}]" for i, (a, b) in enumerate(seg))
                fc += ";" + "".join(f"[v{i}]" for i in range(len(seg))) + f"concat=n={len(seg)}:v=1:a=0,format=yuva420p[o]"
                sh(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", fc, "-map", "[o]"] + codec)
        out[nome] = arq
    return out


def expr_recorte(pontos):
    """x(t) do recorte: interpolação suave (smoothstep) entre os pontos [t, x0] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return str(pontos[0][1])
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max((t-{t0})/({t1}-{t0}),0),1)"
        seg = f"({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p}))"
        e = f"if(lt(t,{t1}),{seg},{e})"
    return e


ALCA = 0.5


def preparar_cenas(d, t, reaproveitar):
    fps, W, H = d["fps"], d["largura"], d["altura"]
    cenas = []
    for c in d["cenas"]:
        c = dict(c, ini=t(c["ini"]), fim=t(c["fim"]))
        if c.get("tipo") == "grafico":
            cenas.append(c)
            continue
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        if not os.path.exists(src):
            sys.exit(f"bruto ausente: {src} (baixe de {f['url']})")
        r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-show_entries", "format=duration",
                "-of", "json", src], capturar=True)
        info = json.loads(r.stdout)
        w0, h0 = info["streams"][0]["width"], info["streams"][0]["height"]
        dur = min(c["fim"] - c["ini"] + ALCA, float(info["format"]["duration"]) - c["in"] - 0.02)
        largura = round(h0 * W / H / 2) * 2
        vf = [f"crop=w={largura}:h={h0}:x='{expr_recorte(c['recorte_x'])}':y=0", f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1"]
        arq = f"cena_{c['id']}.mp4"
        if not (reaproveitar and os.path.exists(os.path.join(PUBLIC, arq))):
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.3f}", "-i", src, "-t", f"{dur:.3f}", "-vf", ",".join(vf), "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "12", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq)])
        cenas.append(dict(c, arquivo=arq))
        print(f"cena {c['id']}: {c['ini']:.2f}–{c['fim']:.2f} s · {w0}×{h0}")
    return cenas


# ---------------------------------------------------------------- trilha e efeitos sintetizados (originais)

def gravar_np(arq, x):
    import numpy as np
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    with wave.open(arq, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def trilha(d, print_ini, print_fim):
    """Mesma cama da REV1 (drone em lá + pulso de 100 bpm → pad de lá maior), com a virada no "Mas calma" (fim do
    print). No quadro do print o pulso para e fica só o drone com um "relógio" de 1 clique por segundo: é o respiro
    em que a pessoa tira o print, sem disputar com a leitura."""
    import numpy as np
    from scipy.signal import lfilter
    rng = np.random.default_rng(7)
    T = d["duracao"]
    n = int(T * SR)
    t = np.arange(n) / SR
    virada = print_fim
    batida = 60.0 / 100

    def lp(x, fc):
        a = math.exp(-2 * math.pi * fc / SR)
        return lfilter([1 - a], [1, -a], x)

    tensao = np.clip((virada - t) / 0.5, 0, 1) * np.clip(t / 0.3, 0, 1)
    calma = np.clip((t - (virada - 0.2)) / 1.0, 0, 1) * np.clip((T - t) / 1.2, 0, 1)
    no_print = (t >= print_ini) & (t < print_fim)
    pulso_on = np.where(no_print, 0.0, 1.0)
    sub = np.zeros(n)
    cres = 0.6 + 0.4 * np.clip(t / print_ini, 0, 1)
    sub += (0.30 * np.sin(2 * math.pi * 55 * t) + 0.14 * np.sin(2 * math.pi * 82.41 * t + 0.4) + 0.05 * np.sin(2 * math.pi * 110 * t)) * cres * tensao
    k = np.zeros(n)
    for i in range(int(print_ini / batida) + 1):
        i0 = int((0.12 + i * batida) * SR)
        if i0 >= n:
            break
        tt = np.arange(min(int(0.32 * SR), n - i0)) / SR
        f = 48 + 40 * np.exp(-tt * 30)
        k[i0:i0 + len(tt)] += 0.55 * np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    sub += k * tensao * pulso_on
    clk = np.zeros(n)
    for i in range(int(print_ini / (batida / 2)) + 1):
        i0 = int((0.12 + i * batida / 2 + batida / 4) * SR)
        L = int(0.03 * SR)
        if i0 + L >= n:
            break
        clk[i0:i0 + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 220) * 0.05
    # relógio do print: 1 clique por segundo, um pouco mais presente
    tp = print_ini + 0.5
    while tp < print_fim - 0.3:
        i0 = int(tp * SR)
        L = int(0.04 * SR)
        clk[i0:i0 + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 160) * 0.09
        tp += 1.0
    sub += (clk - lp(clk, 3000)) * tensao
    sub += lp(rng.standard_normal(n) * 0.10, 380) * (0.5 + 0.5 * np.sin(2 * math.pi * 0.18 * t)) * tensao
    pad = np.zeros(n)
    for f0, a in ((220.0, 0.16), (277.18, 0.11), (329.63, 0.11), (440.0, 0.06)):
        pad += a * (np.sin(2 * math.pi * f0 * t) + 0.5 * np.sin(2 * math.pi * (f0 * 1.003) * t + 1.0))
    sub += lp(pad, 1800) * calma
    notas = [440.0, 554.37, 659.25, 554.37, 493.88, 554.37, 659.25, 880.0]
    pl = np.zeros(n)
    i, tp = 0, virada + 0.35
    while tp < T - 1.0:
        i0 = int(tp * SR)
        tt = np.arange(min(int(1.1 * SR), n - i0)) / SR
        pl[i0:i0 + len(tt)] += 0.10 * np.sin(2 * math.pi * notas[i % len(notas)] * tt) * np.exp(-tt * 4.5) * (1 - np.exp(-tt * 300))
        tp += batida
        i += 1
    sub += pl * calma
    sub += 0.16 * np.sin(2 * math.pi * 110 * t) * calma * (0.7 + 0.3 * np.sin(2 * math.pi * t / (2 * batida)))
    # respiro do print: a cama sobe alguns dB enquanto não há voz
    ganho_print = 10 ** (d["mix"]["trilha_print_db"] / 20)
    rampa = np.clip(np.minimum((t - print_ini) / 0.3, (print_fim - t) / 0.3), 0, 1)
    sub *= 1 + (ganho_print - 1) * rampa
    b = os.path.join(TMP, "trilha_bruta.wav")
    gravar_np(b, sub * 0.6)
    medido, _ = lufs(b)
    sh(["ffmpeg", "-v", "error", "-y", "-i", b, "-af", f"volume={d['mix']['trilha_lufs'] - medido:.2f}dB", "-c:a", "pcm_s16le", os.path.join(PUBLIC, "trilha.wav")])


def efeitos():
    """Painel (split-flap), blip e ping: os mesmos efeitos originais da REV1."""
    import numpy as np
    rng = np.random.default_rng(3)
    out = {}
    L = int(0.45 * SR)
    x = np.zeros(L)
    for i in range(7):
        i0 = int((0.012 + i * 0.038 + rng.uniform(-0.004, 0.004)) * SR)
        m = int(0.018 * SR)
        tt = np.arange(m) / SR
        x[i0:i0 + m] += (rng.standard_normal(m) * np.exp(-tt * 380) + 0.6 * np.sin(2 * math.pi * 1900 * tt) * np.exp(-tt * 260)) * (0.9 - i * 0.07)
    out["painel"] = x * 0.5
    tt = np.arange(int(0.16 * SR)) / SR
    out["blip"] = (np.sin(2 * math.pi * 1320 * tt) + 0.35 * np.sin(2 * math.pi * 1980 * tt)) * np.exp(-tt * 30) * (1 - np.exp(-tt * 900)) * 0.4
    tt = np.arange(int(0.6 * SR)) / SR
    a = np.sin(2 * math.pi * 659.25 * tt) * np.exp(-tt * 9)
    b = np.zeros_like(tt)
    j = int(0.09 * SR)
    b[j:] = np.sin(2 * math.pi * 880 * tt[: len(tt) - j]) * np.exp(-tt[: len(tt) - j] * 7)
    out["ping"] = (a + b) * (1 - np.exp(-tt * 600)) * 0.35
    nomes = {}
    for nome, sinal in out.items():
        arq = f"sfx_{nome}.wav"
        gravar_np(os.path.join(PUBLIC, arq), sinal)
        nomes[nome] = arq
    return nomes


def nivel_evento(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "apad=pad_dur=1,ebur128", "-f", "null", "-"], capture_output=True, text=True)
    ms = [float(x) for x in re.findall(r"M:\s*(-?[\d.]+)", r.stderr)]
    return max(ms) if ms else -30.0


# ---------------------------------------------------------------- preparar → props_<versão>.json

def preparar(reaproveitar=False):
    d = carregar()
    os.makedirs(PUBLIC, exist_ok=True)
    fl = carregar_fala()
    andar, t = resolver(d, fl)
    vozes = voz(d) if not (reaproveitar and all(os.path.exists(os.path.join(PUBLIC, f"voz_{n}.wav")) for n in d["tomadas"])) else {n: f"voz_{n}.wav" for n in d["tomadas"]}
    diego = recortes_tomadas(d, reaproveitar)
    base = {k: d[k] for k in ("fps", "largura", "altura", "duracao", "mix")}
    base["tomadas"] = [{"id": n, "ini": tk["ini"], "dur": round(dur_tomada(tk), 3), "voz": vozes[n], "recorte": diego[n], "queixo": tk["queixo"]}
                      for n, tk in d["tomadas"].items()]
    base["cenas"] = preparar_cenas(d, t, reaproveitar)
    base["print"] = andar(d["print"])
    base["graficos"] = andar(d["graficos"])
    for sub in ("prints",):
        shutil.copytree(os.path.join(REV1, "assets", sub), os.path.join(PUBLIC, sub), dirs_exist_ok=True)
        shutil.copytree(os.path.join(AQUI, "assets", sub), os.path.join(PUBLIC, sub), dirs_exist_ok=True)
    shutil.copy(os.path.join(REV1, "assets", "mapa_europa.json"), os.path.join(PUBLIC, "mapa_europa.json"))
    if not (reaproveitar and os.path.exists(os.path.join(PUBLIC, "trilha.wav"))):
        trilha(d, base["print"]["ini"], base["print"]["fim"])
    base["trilha"] = "trilha.wav"
    sfx = efeitos()
    sons = []
    for s in d["sons"]:
        item = {"nome": s["nome"], "em": t(s["em"]), "rel_db": s["rel_db"]}
        if s["nome"] in sfx:
            item["arquivo"] = sfx[s["nome"]]
            item["nivel"] = round(nivel_evento(os.path.join(PUBLIC, sfx[s["nome"]])), 1)
        sons.append(item)
    base["sons"] = sons
    legendas = {False: grupos_legenda(d, fl), True: grupos_uma_linha(d, fl)}
    layouts = {v["layout"] for v in d["versoes"].values()}
    for nome, v in d["versoes"].items():
        props = escolher(dict(base, modo=nome), v["layout"], layouts)
        props["diego"] = andar(d["diego"][v["diego"]]) if v["diego"] else None
        props["legendas"] = legendas[v["legenda"]["uma_linha"]]
        props["legenda_base_y"] = v["legenda"]["base_y"]
        with open(os.path.join(TMP, f"props_{nome}.json"), "w", encoding="utf-8") as fp:
            json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração: {d['duracao']:.2f} s · print {base['print']['ini']:.2f}–{base['print']['fim']:.2f} s · props em _tmp/props_*.json")


# ---------------------------------------------------------------- render, master, prévia, srt, quadros

def render(so=None):
    d = carregar()
    for nome in d["versoes"]:
        if so and nome != so:
            continue
        props = os.path.join(TMP, f"props_{nome}.json")
        saida = os.path.join(TMP, f"{nome}_sem_master.mov")
        cmd = ["npx", "remotion", "render", "src/index.ts", "ReelGrevesV2", saida, f"--props={props}", f"--public-dir={PUBLIC}",
               "--codec=h264", "--crf=14", "--pixel-format=yuv420p", "--audio-codec=pcm-16", "--log=warn", "--concurrency=4"]
        if os.path.exists(CHROME):
            cmd.append(f"--browser-executable={CHROME}")
        print(f"  render {nome} (em {REMOTION})")
        if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
            sys.exit("render falhou")


def master():
    """Mesmo master da REV1: faixa limitada BT.709 + ganho até −14 LUFS e limitador com sobreamostragem 4×."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    for nome, v in d["versoes"].items():
        bruta = os.path.join(TMP, f"{nome}_sem_master.mov")
        saida = os.path.join(AQUI, v["saida"])
        i0, _ = lufs(bruta)
        ganho = alvo - i0
        teto = pico - 0.4
        video_tv = os.path.join(TMP, f"{nome}_bt709_tv.mp4")
        sh(["ffmpeg", "-v", "error", "-y", "-i", bruta, "-an", "-vf", "scale=in_range=pc:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709,format=yuv420p",
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-color_range", "tv", video_tv])
        for _ in range(4):
            af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
            sh(["ffmpeg", "-v", "error", "-y", "-i", video_tv, "-i", bruta, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
                "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", saida])
            i, tp = lufs(saida)
            if abs(i - alvo) <= 0.1 and tp <= pico:
                break
            ganho += alvo - i
            if tp > pico:
                teto -= tp - pico + 0.1
        print(f"master {nome}: {i:.1f} LUFS · pico {tp:.1f} dBTP → {v['saida']}")


def previa():
    d = carregar()
    for v in d["versoes"].values():
        sh(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AQUI, v["saida"]), "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "26",
            "-preset", "slow", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", os.path.join(AQUI, v["previa"])])


def srt():
    d = carregar()
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    linhas = [f"{i}\n{ts(g['ini'])} --> {ts(g['fim'])}\n{g['texto'].replace('*', '').replace('|', chr(10))}\n"
              for i, g in enumerate(grupos_legenda(d, carregar_fala()), 1)]
    with open(SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"{len(linhas)} legendas → captions.srt")


def quadros():
    d = carregar()
    pasta = os.path.join(AQUI, "qa_frames")
    os.makedirs(pasta, exist_ok=True)
    for nome, v in d["versoes"].items():
        sh(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AQUI, v["saida"]), "-vf", "fps=2,scale=216:384,tile=11x6:padding=4:color=black",
            "-frames:v", "1", os.path.join(pasta, f"folha_{nome}.jpg")])
        for s in (0.6, 3.9, 7.2, 9.9, 11.8, 13.9, 16.3, 18.3, 20.2, 23.2, 25.0, 28.2):
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{s}", "-i", os.path.join(AQUI, v["saida"]), "-frames:v", "1", "-q:v", "3",
                os.path.join(pasta, f"{nome}_{s:04.1f}s.jpg")])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"fala": [fala], "recorte": [recorte], "rosto": [rosto], "preparar": [preparar], "props": [lambda: preparar(reaproveitar=True)],
              "render": [lambda: render(sys.argv[2] if len(sys.argv) > 2 else None)], "master": [master], "previa": [previa],
              "srt": [srt], "quadros": [quadros], "tudo": [preparar, render, master, previa, srt, quadros]}
    for fn in etapas[etapa]:
        print(f"== {etapa}")
        fn()
