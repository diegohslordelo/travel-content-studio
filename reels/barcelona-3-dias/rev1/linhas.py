"""Folha fina: uma linha por candidato, 1 quadro a cada 0,5 s (rodar de dentro de rev1). uso: python3 linhas.py saida nome:t0:t1 ..."""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
PROXY = "../fonte/proxy_480.mp4"; Wp, Hp = 480, 270
MOV = np.load("_tmp/movimento.npy")
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
saida, itens = sys.argv[1], sys.argv[2:]
tw, th, col = 240, 135, 10
img = Image.new("RGB", (130 + col * tw, len(itens) * (th + 4)), "black"); d = ImageDraw.Draw(img)
for r, it in enumerate(itens):
    nome, t0, t1 = it.split(":"); t0, t1 = float(t0), float(t1)
    raw = subprocess.run(f"ffmpeg -v error -ss {t0} -t {t1 - t0} -i {PROXY} -vf fps=2 -f rawvideo -pix_fmt rgb24 -", shell=True, capture_output=True).stdout
    n = min(col, len(raw) // (Wp * Hp * 3)); y = r * (th + 4)
    d.text((4, y + 50), nome[:12], fill=(255, 230, 120), font=F)
    for i in range(n):
        im = Image.frombytes("RGB", (Wp, Hp), raw[i * Wp * Hp * 3:(i + 1) * Wp * Hp * 3]).resize((tw, th)); x = 130 + i * tw
        img.paste(im, (x, y)); t = t0 + i * 0.5; m = MOV[int(t * 6):int(t * 6) + 3].mean()
        d.rectangle([x, y, x + 120, y + 20], fill=(0, 0, 0)); d.text((x + 3, y + 1), f"{int(t // 60)}:{t % 60:04.1f} m{m:.0f}", fill=(255, 255, 255), font=F)
img.save(saida, quality=80)
