#!/usr/bin/env python3
"""Reel "Greves na Europa: confira antes de sair" · REV1 (narrado).

Pipeline (rode de dentro desta pasta):
    python3 rev1.py narracao   # narração TEMPORÁRIA (síntese): corta pausas e mede cada palavra → _tmp/narracao.json
    python3 rev1.py props      # só refaz _tmp/props.json (reaproveita cenas e trilha já geradas)
    python3 rev1.py preparar   # cenas (HLG→SDR, recorte 9:16, 30 fps), som ambiente, trilha, prints e mapa em _tmp/public
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "ReelGreves")
    python3 rev1.py master     # loudness do master: −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev1.py previa     # prévia leve 540 × 960
    python3 rev1.py srt        # captions.srt a partir dos mesmos grupos de legenda da tela
    python3 rev1.py quadros    # folha de quadros para QA (qa_frames/)
    python3 rev1.py tudo

Entradas: rev1.json (decisões desta revisão), narracao_temp/ (síntese pt-BR, provisória), assets/ (prints e mapa)
e os brutos em ../fonte/ (fora do git; baixar do Drive pelo `drive_id` de cada fonte em rev1.json).
Usa a biblioteca padrão do Python, numpy (trilha e efeitos sintetizados), ffmpeg e Node.
"""
import json
import math
import os
import random
import re
import shutil
import struct
import subprocess
import sys
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
NARR = os.path.join(AQUI, "narracao_temp")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_final.mp4")
PREVIA = os.path.join(AQUI, "reel_preview.mp4")
SRT = os.path.join(AQUI, "captions.srt")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SR = 48000

# HLG (iPhone, BT.2020) → SDR BT.709. Referência de branco 203 nits (ITU-R BT.2408) e curva Hable: no comparativo
# desta revisão, o npl=100 + Möbius do Madrid estourava os claros das estações (vidro, painéis).
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
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return i, float(p[-1]) if p else None


# ---------------------------------------------------------------- áudio PCM (mono float)

def ler_wav(arq):
    with wave.open(arq, "rb") as w:
        n, ch, larg = w.getnframes(), w.getnchannels(), w.getsampwidth()
        assert larg == 2, arq
        dados = struct.unpack(f"<{n * ch}h", w.readframes(n))
    return [dados[i * ch] / 32768.0 for i in range(n)]


def gravar_wav(arq, amostras, canais=1):
    with wave.open(arq, "wb") as w:
        w.setnchannels(canais)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f"<{len(amostras)}h", *[max(-32767, min(32767, int(round(a * 32767)))) for a in amostras]))


# ---------------------------------------------------------------- narração temporária

def narracao():
    """Corta o silêncio das pontas e encurta pausas internas longas (> pausa_max) de cada frase sintetizada.

    A síntese (edge-tts, voz pt-BR-AntonioNeural, +18%) é só referência de tempo: a narração final é a voz do Diego.
    Saída: _tmp/public/narr_fXX.wav + _tmp/narracao.json com o tempo de cada palavra (relativo ao arquivo cortado)."""
    d = carregar()
    cfg = d["narracao"]
    os.makedirs(PUBLIC, exist_ok=True)
    saida = {}
    for f in cfg["frases"]:
        fid = f["id"]
        mp3 = os.path.join(NARR, f"{fid}.mp3")
        bruto = os.path.join(TMP, f"narr_{fid}_bruto.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", bruto])
        a = ler_wav(bruto)
        palavras = json.load(open(os.path.join(NARR, f"{fid}.json"), encoding="utf-8"))
        # trechos de fala: [início, fim] de cada palavra, com folga
        folga_ini, folga_fim, pausa_max, pausa_nova = 0.04, 0.10, cfg["pausa_max"], cfg["pausa_nova"]
        cortes = []  # (ini_s, fim_s) de áudio mantido, em segundos do arquivo bruto
        ini = max(0.0, palavras[0]["t"] - folga_ini)
        ult_fim = palavras[0]["t"] + palavras[0]["d"]
        for p in palavras[1:]:
            pausa = p["t"] - ult_fim
            if pausa > pausa_max:
                cortes.append((ini, ult_fim + pausa_nova / 2))
                ini = p["t"] - pausa_nova / 2
            ult_fim = max(ult_fim, p["t"] + p["d"])
        cortes.append((ini, min(len(a) / SR, ult_fim + folga_fim)))
        # monta com microfades de 6 ms em cada emenda
        fade = int(0.006 * SR)
        out, mapa = [], []  # mapa: (ini_bruto, ini_saida)
        for c0, c1 in cortes:
            seg = a[int(c0 * SR):int(c1 * SR)]
            for k in range(min(fade, len(seg))):
                g = k / fade
                seg[k] *= g
                seg[-1 - k] *= g
            mapa.append((c0, len(out) / SR, c1))
            out.extend(seg)
        def converter(t):
            for c0, s0, c1 in mapa:
                if t <= c1:
                    return s0 + max(0.0, t - c0)
            return mapa[-1][1] + (t - mapa[-1][0])
        arq = f"narr_{fid}.wav"
        gravar_wav(os.path.join(PUBLIC, arq), out)
        dur = len(out) / SR
        ws = [{"w": p["w"], "t": round(converter(p["t"]), 3), "fim": round(converter(p["t"] + p["d"]), 3)} for p in palavras]
        saida[fid] = {"arquivo": arq, "dur": round(dur, 3), "palavras": ws}
        print(f"{fid}: {palavras[-1]['t'] + palavras[-1]['d']:.2f} s → {dur:.2f} s  ({len(cortes) - 1} pausa(s) encurtada(s))")
    with open(os.path.join(TMP, "narracao.json"), "w", encoding="utf-8") as fp:
        json.dump(saida, fp, ensure_ascii=False, indent=1)
    total = sum(v["dur"] for v in saida.values())
    print(f"fala somada: {total:.2f} s")


# ---------------------------------------------------------------- tempos ancorados na fala

def carregar_narracao():
    with open(os.path.join(TMP, "narracao.json"), encoding="utf-8") as f:
        return json.load(f)


def resolver(d, narr):
    """Converte {"frase", "palavra", "desloc"} em segundos absolutos (início da palavra na linha do tempo)."""
    ini = {f["id"]: f["ini"] for f in d["narracao"]["frases"]}

    def t(v):
        if isinstance(v, (int, float)):
            return float(v)
        return round(ini[v["frase"]] + narr[v["frase"]]["palavras"][v["palavra"]]["t"] + v.get("desloc", 0.0), 3)

    def andar(o):
        if isinstance(o, dict):
            if set(o) <= {"frase", "palavra", "desloc"} and "palavra" in o:
                return t(o)
            return {k: andar(v) for k, v in o.items()}
        if isinstance(o, list):
            return [andar(x) for x in o]
        return o

    return andar, t, ini


def grupos_legenda(d, narr, ini):
    """Grupos da legenda (texto da tela e do .srt) com início na 1ª palavra e fim no início do grupo seguinte."""
    gs = d["legendas"]
    out = []
    for i, g in enumerate(gs):
        ws = narr[g["frase"]]["palavras"]
        t0 = ini[g["frase"]] + ws[g["de"]]["t"]
        if i + 1 < len(gs) and gs[i + 1]["frase"] == g["frase"]:
            t1 = ini[g["frase"]] + ws[gs[i + 1]["de"]]["t"]
        else:
            fim_frase = ini[g["frase"]] + narr[g["frase"]]["dur"]
            prox = ini[gs[i + 1]["frase"]] + narr[gs[i + 1]["frase"]]["palavras"][gs[i + 1]["de"]]["t"] if i + 1 < len(gs) else d["duracao"]
            t1 = min(fim_frase + 0.25, prox - 0.05)
        item = {"texto": g["texto"], "ini": round(t0, 3), "fim": round(t1, 3)}
        if "destaque" in g:
            item["destaque_em"] = round(ini[g["frase"]] + ws[g["destaque"]]["t"], 3)
        out.append(item)
    return out


# ---------------------------------------------------------------- cenas de vídeo

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


ALCA = 0.5  # s de imagem extra depois do fim da cena (transições com sobreposição)


def preparar_cenas(d, reaproveitar=False):
    """Codifica cada cena. Com reaproveitar=True (etapa `props`), mantém o arquivo já gerado se ele existir."""
    fps, W, H = d["fps"], d["largura"], d["altura"]
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)
    cenas = []
    for c in d["cenas"]:
        if c.get("tipo") == "grafico":
            cenas.append(dict(c))
            continue
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                "-show_entries", "format=duration", "-of", "json", src], capturar=True)
        info = json.loads(r.stdout)
        st = info["streams"][0]
        rot = int(float(next((x.get("rotation", 0) for x in st.get("side_data_list", []) if "rotation" in x), 0)))
        w0, h0 = (st["height"], st["width"]) if rot in (90, -90, 270) else (st["width"], st["height"])
        dur_src = float(info["format"]["duration"])
        dur = min(c["dur"] + ALCA, dur_src - c["in"] - 0.02)
        vf = [TONEMAP] if f.get("hdr") else []  # HLG do iPhone → SDR; os clipes do Mixkit já são BT.709
        if w0 / h0 > W / H + 0.01:  # gravado na horizontal: recorte 9:16 que acompanha os pontos x
            largura = round(h0 * W / H / 2) * 2
            vf.append(f"crop=w={largura}:h={h0}:x='{expr_recorte(c.get('recorte_x', [[0, (w0 - largura) // 2]]))}':y=0")
        vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
        arq = f"cena_{c['id']}.mp4"
        if reaproveitar and os.path.exists(os.path.join(PUBLIC, arq)):
            cena = dict(c, arquivo=arq, dur_arquivo=round(dur, 3))
            if c["audio"] == "ambiente":
                cena["audio_arquivo"] = f"amb_{c['id']}.wav"
            cenas.append(cena)
            continue
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.3f}", "-i", src, "-t", f"{dur:.3f}", "-vf", ",".join(vf), "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq)])
        cena = dict(c, arquivo=arq, dur_arquivo=round(dur, 3))
        if c["audio"] == "ambiente":
            cena["audio_arquivo"] = audio_trecho(src, c["in"], c["dur"], f"amb_{c['id']}.wav", d["mix"]["ambiente_lufs"])
        cenas.append(cena)
        print(f"cena {c['id']}: {c['dur']:.2f} s (+{dur - c['dur']:.2f} s de alça) · {w0}×{h0}")
    return cenas


def audio_trecho(src, ini, dur, nome, alvo):
    """Extrai o áudio do trecho em 48 kHz estéreo, iguala a loudness ao alvo e faz fades curtos."""
    bruto = os.path.join(TMP, "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", bruto])
    medido, _ = lufs(bruto)
    ganho = alvo - medido
    af = f"volume={ganho:.2f}dB,afade=t=in:d=0.03,afade=t=out:st={max(0, dur - 0.08):.4f}:d=0.08"
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s16le", os.path.join(PUBLIC, nome)])
    print(f"  {nome}: {medido:.1f} LUFS → {alvo} LUFS ({ganho:+.1f} dB)")
    return nome


def preparar_janelas(d, reaproveitar=False):
    """Clipes das janelas 16:9 da agenda: inteiros (sem recorte), 1080 × 608, para não ampliar fontes de 1080p."""
    out = []
    for j in d.get("janelas", []):
        f = d["fontes"][j["fonte"]]
        arq = f"janela_{j['id']}.mp4"
        if not (reaproveitar and os.path.exists(os.path.join(PUBLIC, arq))):
            vf = ([TONEMAP] if f.get("hdr") else []) + [f"scale=1080:608:flags=lanczos,fps={d['fps']},format=yuv420p,setsar=1"]
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{j['in']:.3f}", "-i", os.path.join(FONTE, f["arquivo"]), "-t", f"{j['dur'] + 0.3:.3f}",
                "-vf", ",".join(vf), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-g", "15", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq)])
        out.append(dict(j, arquivo=arq))
        print(f"janela {j['id']}: {j['dur']:.1f} s de {f['arquivo']}")
    return out


# ---------------------------------------------------------------- trilha e efeitos sintetizados (originais)

def _np():
    import numpy as np
    return np


def normalizar(arq_in, arq_out, alvo):
    medido, _ = lufs(arq_in)
    sh(["ffmpeg", "-v", "error", "-y", "-i", arq_in, "-af", f"volume={alvo - medido:.2f}dB", "-c:a", "pcm_s16le", arq_out])
    print(f"  {os.path.basename(arq_out)}: {medido:.1f} → {alvo} LUFS")


def gravar_np(arq, x):
    np = _np()
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    pcm = (x * 32767).astype("<i2")
    with wave.open(arq, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def trilha(d):
    """Cama musical original: 0–17 s tensão (drone grave em lá, pulso de 100 bpm, ruído de trilho filtrado e um
    "relógio" agudo); 17 s em diante resolve num pad de lá maior com dedilhado leve. Sem melodia que dispute com a voz."""
    np = _np()
    rng = np.random.default_rng(7)
    T = d["duracao"]
    n = int(T * SR)
    t = np.arange(n) / SR
    virada = next(c["ini"] for c in d["cenas"] if c["id"] == "trem_cidade")  # "Mas calma"
    bpm = 100.0
    batida = 60.0 / bpm

    def env(t0, a, r, dur):
        e = np.zeros(n)
        i0 = int(t0 * SR)
        k = np.arange(int((a + dur + r) * SR))
        tt = k / SR
        v = np.where(tt < a, tt / a, np.where(tt < a + dur, 1.0, np.maximum(0, 1 - (tt - a - dur) / r)))
        i1 = min(n, i0 + len(v))
        e[i0:i1] = v[: i1 - i0]
        return e

    def lp(x, fc):
        # passa-baixa de 1 polo, simples e suficiente para a cama
        a = math.exp(-2 * math.pi * fc / SR)
        y = np.empty_like(x)
        acc = 0.0
        for i in range(len(x)):
            acc = (1 - a) * x[i] + a * acc
            y[i] = acc
        return y

    tensao = np.clip((virada - t) / 0.6, 0, 1) * np.clip(t / 0.4, 0, 1)
    calma = np.clip((t - (virada - 0.3)) / 1.2, 0, 1) * np.clip((T - t) / 1.5, 0, 1)
    sub = 0.0 * t
    # drone grave (lá 55 Hz + quinta), com leve crescendo até a virada
    cres = 0.6 + 0.4 * np.clip(t / virada, 0, 1)
    sub += (0.30 * np.sin(2 * math.pi * 55 * t) + 0.14 * np.sin(2 * math.pi * 82.41 * t + 0.4) + 0.05 * np.sin(2 * math.pi * 110 * t)) * cres * tensao
    # pulso grave a cada batida (kick macio)
    k = np.zeros(n)
    for i in range(int(virada / batida) + 1):
        t0 = 0.12 + i * batida
        i0 = int(t0 * SR)
        L = int(0.32 * SR)
        if i0 >= n:
            break
        tt = np.arange(min(L, n - i0)) / SR
        f = 48 + 40 * np.exp(-tt * 30)
        k[i0:i0 + len(tt)] += 0.55 * np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    sub += k * tensao
    # "relógio": clique agudo nas semicolcheias pares, bem baixo
    clk = np.zeros(n)
    for i in range(int(virada / (batida / 2)) + 1):
        t0 = 0.12 + i * batida / 2 + batida / 4
        i0 = int(t0 * SR)
        L = int(0.03 * SR)
        if i0 + L >= n:
            break
        clk[i0:i0 + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 220) * 0.05
    hp = clk - lp(clk, 3000)
    sub += hp * tensao
    # ruído de trilho filtrado (respiração da estação), entra e sai devagar
    ruido = lp(rng.standard_normal(n) * 0.10, 380) * (0.5 + 0.5 * np.sin(2 * math.pi * 0.18 * t)) * tensao
    sub += ruido
    # resolução: pad de lá maior (A3, C#4, E4, A4) com batimento lento + dedilhado leve
    pad = np.zeros(n)
    for f0, a in ((220.0, 0.16), (277.18, 0.11), (329.63, 0.11), (440.0, 0.06)):
        pad += a * (np.sin(2 * math.pi * f0 * t) + 0.5 * np.sin(2 * math.pi * (f0 * 1.003) * t + 1.0))
    pad = lp(pad, 1800)
    sub += pad * calma
    notas = [440.0, 554.37, 659.25, 554.37, 493.88, 554.37, 659.25, 880.0]
    pl = np.zeros(n)
    passo = batida
    i = 0
    tp = virada + 0.35
    while tp < T - 1.2:
        f0 = notas[i % len(notas)]
        i0 = int(tp * SR)
        L = int(1.1 * SR)
        tt = np.arange(min(L, n - i0)) / SR
        pl[i0:i0 + len(tt)] += 0.10 * np.sin(2 * math.pi * f0 * tt) * np.exp(-tt * 4.5) * (1 - np.exp(-tt * 300))
        tp += passo
        i += 1
    sub += pl * calma
    # baixo da resolução
    sub += 0.16 * np.sin(2 * math.pi * 110 * t) * calma * (0.7 + 0.3 * np.sin(2 * math.pi * t / (2 * batida)))
    bruto = os.path.join(TMP, "trilha_bruta.wav")
    gravar_np(bruto, sub * 0.6)
    normalizar(bruto, os.path.join(PUBLIC, "trilha.wav"), d["mix"]["trilha_lufs"])


def efeitos():
    """Efeitos curtos originais (os da marca vêm de design-system/sons). Loudness de evento medida depois."""
    np = _np()
    rng = np.random.default_rng(3)
    out = {}
    # painel: 7 "lâminas" de split-flap (cliques de plástico) em 260 ms
    L = int(0.45 * SR)
    x = np.zeros(L)
    for i in range(7):
        i0 = int((0.012 + i * 0.038 + rng.uniform(-0.004, 0.004)) * SR)
        m = int(0.018 * SR)
        tt = np.arange(m) / SR
        burst = rng.standard_normal(m) * np.exp(-tt * 380) + 0.6 * np.sin(2 * math.pi * 1900 * tt) * np.exp(-tt * 260)
        x[i0:i0 + m] += burst * (0.9 - i * 0.07)
    out["painel"] = x * 0.5
    # blip: seno 1320 Hz com quinta, 110 ms
    tt = np.arange(int(0.16 * SR)) / SR
    out["blip"] = (np.sin(2 * math.pi * 1320 * tt) + 0.35 * np.sin(2 * math.pi * 1980 * tt)) * np.exp(-tt * 30) * (1 - np.exp(-tt * 900)) * 0.4
    # ping: duas notas (mi5 → lá5), notificação suave
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
    """Loudness K-ponderada máxima em 400 ms (momentânea) do arquivo: referência para o volume relativo."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "apad=pad_dur=1,ebur128", "-f", "null", "-"], capture_output=True, text=True)
    ms = [float(x) for x in re.findall(r"M:\s*(-?[\d.]+)", r.stderr)]
    return max(ms) if ms else -30.0


# ---------------------------------------------------------------- preparar → props.json

def preparar(reaproveitar=False):
    d = carregar()
    os.makedirs(PUBLIC, exist_ok=True)
    if not os.path.exists(os.path.join(TMP, "narracao.json")):
        narracao()
    narr = carregar_narracao()
    andar, t, ini = resolver(d, narr)
    props = {k: d[k] for k in ("fps", "largura", "altura", "duracao", "mix")}
    props["cenas"] = preparar_cenas(d, reaproveitar)
    props["janelas"] = preparar_janelas(d, reaproveitar)
    props["creditos_janelas"] = {
        j["id"]: d["fontes"][j["fonte"]].get("credito", "MIXKIT · LICENÇA LIVRE")
        for j in d.get("janelas", [])}
    props["narracao"] = [{"id": f["id"], "ini": f["ini"], "arquivo": narr[f["id"]]["arquivo"], "dur": narr[f["id"]]["dur"]}
                         for f in d["narracao"]["frases"]]
    for i, f in enumerate(props["narracao"][:-1]):
        prox = props["narracao"][i + 1]
        if f["ini"] + f["dur"] > prox["ini"] - 0.1:
            sys.exit(f"narração {f['id']} invade {prox['id']}: fim {f['ini'] + f['dur']:.2f} s")
    props["legendas"] = grupos_legenda(d, narr, ini)
    props["graficos"] = andar(d["graficos"])
    # assets (prints e mapa) → public
    for sub in ("prints",):
        shutil.copytree(os.path.join(AQUI, "assets", sub), os.path.join(PUBLIC, sub), dirs_exist_ok=True)
    shutil.copy(os.path.join(AQUI, "assets", "mapa_europa.json"), os.path.join(PUBLIC, "mapa_europa.json"))
    if not (reaproveitar and os.path.exists(os.path.join(PUBLIC, "trilha.wav"))):
        trilha(d)
    props["trilha"] = "trilha.wav"
    sfx = efeitos()
    sons = []
    for s in d["sons"]:
        item = {"nome": s["nome"], "em": t(s["em"]), "rel_db": s["rel_db"]}
        if s["nome"] in sfx:
            arq = os.path.join(PUBLIC, sfx[s["nome"]])
            item["arquivo"] = sfx[s["nome"]]
            item["nivel"] = round(nivel_evento(arq), 1)
        sons.append(item)
    props["sons"] = sons
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração: {d['duracao']:.2f} s · props em _tmp/props.json")


# ---------------------------------------------------------------- render, master, prévia, srt, quadros

def render():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "render", "src/index.ts", "ReelGreves", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
           "--codec=h264", "--crf=14", "--pixel-format=yuv420p", "--audio-codec=pcm-16", "--log=warn", "--concurrency=4"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("render falhou")


def master():
    """Ganho linear até −14 LUFS + limitador de pico com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP).

    O vídeo do Remotion sai em faixa cheia (yuvj420p); aqui ele é convertido uma vez para faixa limitada BT.709
    (yuv420p, o padrão de entrega), e o áudio é refeito por cima com cópia do vídeo."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = lufs(SAIDA_BRUTA)
    ganho = alvo - i0
    teto = pico - 0.4
    video_tv = os.path.join(TMP, "video_bt709_tv.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-an", "-vf", "scale=in_range=pc:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709,format=yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-colorspace", "bt709", "-color_range", "tv", video_tv])
    for _ in range(4):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", video_tv, "-i", SAIDA_BRUTA, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", SAIDA])
        i, tp = lufs(SAIDA)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {ganho:+.1f} dB) → {os.path.basename(SAIDA)}")


def previa():
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "26", "-preset", "slow",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])
    print(f"prévia: {os.path.getsize(PREVIA) / 1e6:.1f} MB")


def srt():
    d = carregar()
    narr = carregar_narracao()
    _, _, ini = resolver(d, narr)
    def ts(s):
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    linhas = []
    for i, g in enumerate(grupos_legenda(d, narr, ini), 1):
        texto = g["texto"].replace("*", "").replace("|", "\n")
        linhas.append(f"{i}\n{ts(g['ini'])} --> {ts(g['fim'])}\n{texto}\n")
    with open(SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"{len(linhas)} legendas → {os.path.basename(SRT)}")


def quadros():
    """Folha com 1 quadro a cada 0,5 s (para QA visual) e quadros-chave em tamanho cheio."""
    pasta = os.path.join(AQUI, "qa_frames")
    os.makedirs(pasta, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "fps=2,scale=216:384,tile=12x6:padding=4:color=black", "-frames:v", "1",
        os.path.join(pasta, "folha_rev1.jpg")])
    for s in (0.5, 3.0, 5.0, 6.4, 8.2, 9.6, 11.2, 13.0, 14.4, 16.4, 18.2, 22.6, 24.8, 26.4, 28.9, 33.8):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{s}", "-i", SAIDA, "-frames:v", "1", "-q:v", "3",
            os.path.join(pasta, f"q_{s:05.1f}s.jpg")])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    def props_rapido():
        preparar(reaproveitar=True)
    etapas = {"narracao": [narracao], "preparar": [preparar], "props": [props_rapido], "render": [render], "master": [master], "previa": [previa],
              "srt": [srt], "quadros": [quadros], "tudo": [narracao, preparar, render, master, previa, srt, quadros]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
