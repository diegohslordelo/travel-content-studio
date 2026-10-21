#!/usr/bin/env python3
"""Reel "Churros em Barcelona: será que vale?" · REV1.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py preparar   # cenas em _tmp/public (corte, HLG→SDR, recorte 9:16, cor, congelamento) + sons
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "ReelChurros")
    python3 rev1.py master     # versões finais: com efeitos, sem áudio e a faixa de efeitos separada
    python3 rev1.py capa       # capa 1080 × 1920 (quadro da bandeja + placa do DS)
    python3 rev1.py qa         # quadros de conferência em qa_frames/
    python3 rev1.py tudo

Entradas: rev1.json (decisões) e o vlog master em ../fonte/ (fora do git; baixar do Drive pelo
`drive_id` em rev1.json). Só usa a biblioteca padrão do Python, ffmpeg e Node.

Áudio: nenhum áudio dos clipes entra. As cenas são exportadas com -an e a composição não tem
<Audio> de clipe; os únicos sons são os efeitos sintetizados aqui (faixa separada, opcional).
"""
import json
import math
import os
import random
import re
import struct
import subprocess
import sys
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_bruto.mov")
SAIDA = os.path.join(AQUI, "reel_churros-barcelona_rev1.mp4")
SAIDA_MUDA = os.path.join(AQUI, "reel_churros-barcelona_rev1_sem_audio.mp4")
SAIDA_PREVIA = os.path.join(AQUI, "reel_churros-barcelona_rev1_previa.mp4")
STEM = os.path.join(AQUI, "efeitos_churros-barcelona_rev1.wav")
CAPA = os.path.join(AQUI, "capa_churros-barcelona_rev1.jpg")
QA = os.path.join(AQUI, "qa_frames")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# Tamanho das cenas preparadas: a largura nativa do recorte 9:16 de um quadro 3840 × 2160 (1215 px),
# arredondada para par. A composição (1080 × 1920) reduz, o que dá folga para a câmera virtual.
CW, CH = 1216, 2160

# O vlog é um export do CapCut marcado como HLG/BT.2020, mas o conteúdo já vem graduado para SDR:
# o tonemap HLG do madrid-show estoura o dourado para o laranja. Aqui só se convertem as primárias
# e a matriz BT.2020 → BT.709, tratando a curva como SDR (comparação em qa_frames/cor_conversao.jpg).
CONVERSAO = "zscale=min=bt2020nc:pin=bt2020:tin=bt709:rin=tv:m=bt709:p=bt709:t=bt709:r=tv"
# Cor por tipo de plano: comida um pouco mais quente e densa (dourado do churro, chocolate);
# rua só um toque de contraste. Ajustes leves, sem mudar a cor natural.
GRADE = {
    "comida": "colorbalance=rm=0.02:bm=-0.02:rh=0.01:bh=-0.02,eq=contrast=1.05:saturation=1.03",
    "rua": "eq=contrast=1.03:saturation=1.0",
}


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


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def expr_suave(pontos):
    """v(t): interpolação smoothstep entre os pontos [t, v] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return f"{pontos[0][1]:.2f}"
    e = f"{pontos[-1][1]:.2f}"
    for (t0, v0), (t1, v1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max((t-{t0})/({t1}-{t0}),0),1)"
        e = f"if(lt(t,{t1}),({v0:.2f}+({v1:.2f}-{v0:.2f})*{p}*{p}*(3-2*{p})),{e})"
    return e


def preparar():
    d = carregar()
    fps = d["fps"]
    os.makedirs(PUBLIC, exist_ok=True)
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Fonte ausente em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    cenas = []
    for c in d["cenas"]:
        if c.get("grafico"):
            n = round(c["dur"] * fps)
            cenas.append(dict(c, quadros=n, dur=n / fps))
            continue
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        w0, h0 = sonda(src)
        n_corte = round((c["out"] - c["in"]) * fps)
        n_cong = round(c.get("congelar", 0) * fps)
        ch = round(h0 / c.get("zoom", 1.0) / 2) * 2
        cw = round(ch * CW / CH / 2) * 2
        # x do recorte: o centro (fração da largura) vira a borda esquerda, presa dentro do quadro
        xs = [[t, min(max(cx * w0 - cw / 2, 0), w0 - cw)] for t, cx in c["x"]]
        y = min(max(c.get("y", 0.5) * h0 - ch / 2, 0), h0 - ch)
        vel = c.get("velocidade", 1.0)
        n_corte = round((c["out"] - c["in"]) / vel * fps)
        vf = [
            CONVERSAO,
            f"crop=w={cw}:h={ch}:x='{expr_suave(xs)}':y={y:.0f}",
            f"scale={CW}:{CH}:flags=lanczos",
            GRADE[c["grade"]],
        ]
        if vel != 1.0:
            # câmera lenta só em plano de fundo com movimento lento (bandeja atrás da pergunta final)
            vf.append(f"setpts=PTS/{vel}")
        vf.append(f"fps={fps}")
        if n_cong:
            vf.append(f"tpad=stop_mode=clone:stop_duration={n_cong / fps:.4f}")
        vf.append("format=yuv420p,setsar=1")
        arq = f"cena_{c['id']}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n_corte + n_cong),
               "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "12", "-pix_fmt", "yuv420p",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq)]
        # cache: só re-codifica se o comando da cena mudou
        marca = os.path.join(PUBLIC, arq + ".cmd")
        if not (os.path.exists(marca) and open(marca).read() == " ".join(cmd) and os.path.exists(os.path.join(PUBLIC, arq))):
            sh(cmd)
            open(marca, "w").write(" ".join(cmd))
        n = n_corte + n_cong
        cenas.append(dict(c, arquivo=arq, quadros=n, dur=n / fps))
        print(f"cena {c['id']}: {n} quadros ({n / fps:.3f} s) · recorte {cw}×{ch}")

    # contornos do globo
    sh(["cp", os.path.join(AQUI, "geo", "mundo.json"), os.path.join(PUBLIC, "mundo.json")])
    sons()

    props = dict(d, cenas=cenas)
    props["duracao"] = sum(c["dur"] for c in cenas)
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {props['duracao']:.3f} s · {sum(c['quadros'] for c in cenas)} quadros · props em _tmp/props.json")


# ---------------------------------------------------------------- desenho de som (opcional)
SR = 48000


def _grava(nome, amostras):
    pico = max(1e-9, max(abs(a) for a in amostras))
    k = 0.5 / pico  # pico em −6 dBFS: o volume final é decidido na composição
    with wave.open(os.path.join(PUBLIC, nome), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, a * k)) * 32767)) for a in amostras))


def _ruido_filtrado(dur, f0, f1, env, semente):
    """Ruído branco por um passa-banda de 2 polos com centro varrendo f0 → f1 (exponencial)."""
    rnd = random.Random(semente)
    n = int(dur * SR)
    out = []
    y1 = y2 = 0.0
    for i in range(n):
        p = i / n
        fc = f0 * (f1 / f0) ** p
        r = 0.985
        a1 = -2 * r * math.cos(2 * math.pi * fc / SR)
        a2 = r * r
        x = rnd.uniform(-1, 1)
        y = (1 - r) * x - a1 * y1 - a2 * y2
        y2, y1 = y1, y
        out.append(y * env(p))
    return out


def sons():
    # whoosh curto (transições): sobe e cai em 420 ms
    _grava("sfx_whoosh.wav", _ruido_filtrado(0.42, 380, 3200, lambda p: math.sin(math.pi * p) ** 1.6, 1))
    # whoosh grave (mergulho no chocolate → globo)
    _grava("sfx_mergulho.wav", _ruido_filtrado(0.75, 1800, 160, lambda p: (1 - p) ** 1.2 * min(1, p * 10), 2))
    # avião passando (rota): ruído grave com crescendo e efeito Doppler, 2,6 s
    av = _ruido_filtrado(2.6, 900, 420, lambda p: math.sin(math.pi * min(1, p * 1.15)) ** 2, 3)
    av = [a + 0.18 * math.sin(2 * math.pi * (140 - 40 * i / len(av)) * i / SR) * math.sin(math.pi * i / len(av)) ** 2 for i, a in enumerate(av)]
    _grava("sfx_aviao.wav", av)
    # pop de texto: senoide 880 → 660 Hz com decaimento de 70 ms
    _grava("sfx_pop.wav", [math.sin(2 * math.pi * (880 - 220 * i / 4800) * i / SR) * math.exp(-i / (0.018 * SR)) for i in range(4800)])
    # pino em Barcelona: dois toques limpos (1320 e 1760 Hz)
    pin = [0.0] * int(0.5 * SR)
    for atraso, f in ((0, 1320), (0.09, 1760)):
        o = int(atraso * SR)
        for i in range(int(0.4 * SR)):
            pin[o + i] += 0.6 * math.sin(2 * math.pi * f * i / SR) * math.exp(-i / (0.08 * SR))
    _grava("sfx_pin.wav", pin)
    # baque do veredito: 52 Hz com decaimento + estalo
    tum = [math.sin(2 * math.pi * (70 - 18 * min(1, i / (0.12 * SR))) * i / SR) * math.exp(-i / (0.16 * SR)) for i in range(int(0.7 * SR))]
    rnd = random.Random(4)
    for i in range(int(0.006 * SR)):
        tum[i] += rnd.uniform(-0.6, 0.6) * (1 - i / (0.006 * SR))
    _grava("sfx_tum.wav", tum)
    print("  sons: sfx_whoosh, sfx_mergulho, sfx_aviao, sfx_pop, sfx_pin, sfx_tum (sintetizados)")


# ---------------------------------------------------------------- render e entregas
def _remotion(args):
    cmd = ["npx", "remotion", *args, "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    props = os.path.join(TMP, "props.json")
    _remotion(["render", "src/index.ts", "ReelChurros", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
               "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--concurrency=4"])


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def master():
    """Três entregas:
    - com efeitos: os efeitos ficam baixos (≈ −24 LUFS integrados, pico ≤ −6 dBTP), deixando espaço para a narração;
    - sem áudio: só vídeo (para gravar a narração por cima);
    - faixa de efeitos separada (WAV 48 kHz), alinhada ao quadro 0, para a mixagem final com a narração.
    """
    i0, _ = medir(SAIDA_BRUTA)
    ganho = -24.0 - i0
    af = f"volume={ganho:.2f}dB,alimiter=limit={10 ** (-6.5 / 20):.4f}:attack=1:release=60:level=false"
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart", SAIDA])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-an", "-movflags", "+faststart", SAIDA_MUDA])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-vn", "-af", af, "-c:a", "pcm_s24le", "-ar", "48000", STEM])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "slow",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", SAIDA_PREVIA])
    i, tp = medir(SAIDA)
    print(f"efeitos no master: {i:.1f} LUFS integrados · pico {tp:.1f} dBFS")


def capa():
    props = os.path.join(TMP, "props.json")
    _remotion(["still", "src/index.ts", "CapaChurros", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92"])


def qa():
    """Quadros representativos (2 por segundo) e folha de contato do vídeo inteiro."""
    os.makedirs(QA, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
        "fps=2,scale=270:480,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=10x7:padding=4",
        "-frames:v", "1", os.path.join(QA, "folha_de_contato.jpg")])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"preparar": [preparar], "sons": [sons], "render": [render], "master": [master], "capa": [capa], "qa": [qa],
              "tudo": [preparar, render, master, capa, qa]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
