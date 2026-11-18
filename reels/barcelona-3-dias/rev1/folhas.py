"""Folhas de contato do vlog (Barcelona_3dias) para escolher os takes. Rodar de dentro de rev1.

Lê a cópia leve ../fonte/proxy_480.mp4 (480×270, 6 qps, gerada do master) e, para cada janela, grava
_tmp/folha_<nome>.jpg: 1 quadro a cada PASSO s com o tempo do master e a nota de movimento (diferença média
entre quadros, 0–255, mais baixo = mais estático). Também grava _tmp/movimento.json (nota por quadro de 1/6 s).
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROXY = "../fonte/proxy_480.mp4"
os.makedirs("_tmp", exist_ok=True)
Wp, Hp, FPS = 480, 270, 6

if not os.path.exists("_tmp/movimento.npy"):
    raw = subprocess.run(f"ffmpeg -v error -i {PROXY} -vf scale=96:54,format=gray -f rawvideo -", shell=True,
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.int16)
    mov = np.concatenate([[0], np.abs(np.diff(fr, axis=0)).mean((1, 2))])
    np.save("_tmp/movimento.npy", mov)
MOV = np.load("_tmp/movimento.npy")

try:
    FONTE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    FONTE = ImageFont.load_default()


def quadro(t):
    raw = subprocess.run(f"ffmpeg -v error -ss {t:.2f} -i {PROXY} -frames:v 1 -f rawvideo -pix_fmt rgb24 -", shell=True,
                         capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (Wp, Hp), raw)


def folha(nome, t0, t1, passo=1.0, col=6, tw=320):
    ts = list(np.arange(t0, t1, passo))
    th = int(tw * Hp / Wp)
    lin = (len(ts) + col - 1) // col
    img = Image.new("RGB", (col * tw, lin * (th + 4)), "black")
    d = ImageDraw.Draw(img)
    # extrai todos os quadros da janela de uma vez (mais rápido que um ffmpeg por quadro)
    raw = subprocess.run(f"ffmpeg -v error -ss {t0:.2f} -t {t1 - t0:.2f} -i {PROXY} -vf fps=1/{passo} -f rawvideo -pix_fmt rgb24 -",
                         shell=True, capture_output=True, check=True).stdout
    n = len(raw) // (Wp * Hp * 3)
    for i in range(min(n, len(ts))):
        im = Image.frombytes("RGB", (Wp, Hp), raw[i * Wp * Hp * 3:(i + 1) * Wp * Hp * 3]).resize((tw, th))
        x, y = (i % col) * tw, (i // col) * (th + 4)
        img.paste(im, (x, y))
        t = ts[i]
        m = MOV[int(t * FPS):int((t + passo) * FPS)].mean() if int(t * FPS) < len(MOV) else 0
        mm, ss = divmod(t, 60)
        rot = f"{int(mm):02d}:{ss:04.1f} m{m:.0f}"
        d.rectangle([x, y, x + 150, y + 26], fill=(0, 0, 0))
        d.text((x + 4, y + 2), rot, fill=(255, 230, 120) if m < 6 else (255, 255, 255), font=FONTE)
    img.save(f"_tmp/folha_{nome}.jpg", quality=82)
    print("folha", nome, n, "quadros")


if __name__ == "__main__":
    # uso: python3 folhas.py nome t0 t1 [passo]
    a = sys.argv[1:]
    folha(a[0], float(a[1]), float(a[2]), float(a[3]) if len(a) > 3 else 1.0)
