"""Folha de contato para escolher planos: 4 quadros por clipe (15/40/65/90% da duração), com a conversão técnica
HLG → SDR (Reinhard, npl 203), o nome e a orientação. Uso: python3 scripts/folha.py saida.jpg CLIPE [CLIPE ...]"""
import json, subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
TM = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
saida, clipes = sys.argv[1], sys.argv[2:]
H = 300
linhas = []
fnt = ImageFont.load_default(size=26)
for c in clipes:
    arq = f"fonte/clipes/{c}"
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout)
    ims = []
    for f in (0.15, 0.4, 0.65, 0.9):
        tmp = tempfile.mktemp(suffix=".jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d * f:.2f}", "-i", arq, "-frames:v", "1", "-vf", f"scale=-2:{H}:flags=bilinear,{TM}", tmp], check=True)
        ims.append(Image.open(tmp).convert("RGB")); os.remove(tmp)
    w = sum(i.width for i in ims) + 8 * 3
    L = Image.new("RGB", (w + 260, H), (20, 20, 20))
    x = 260
    for i in ims:
        L.paste(i, (x, 0)); x += i.width + 8
    dr = ImageDraw.Draw(L)
    o = "V" if ims[0].height > ims[0].width else "H"
    dr.text((10, 10), f"{c}\n{d:.1f}s {o}\n{ims[0].width}x{ims[0].height}", fill=(255, 255, 0), font=fnt)
    linhas.append(L)
W = max(l.width for l in linhas)
F = Image.new("RGB", (W, sum(l.height + 6 for l in linhas)), (0, 0, 0))
y = 0
for l in linhas:
    F.paste(l, (0, y)); y += l.height + 6
F.save(saida, quality=80)
print(saida, F.size)
