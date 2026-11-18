"""Confere o recorte vertical de cada take: quadro do meio do take (cópia leve) com o retângulo 9:16 desenhado."""
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
T = json.load(open("takes.json")); Wp, Hp = 480, 270
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
nomes = list(T); col = 5; tw, th = 384, 216
img = Image.new("RGB", (col * tw, ((len(nomes) + col - 1) // col) * (th * 2 + 6)), "black"); d = ImageDraw.Draw(img)
for k, n in enumerate(nomes):
    tk = T[n]; x0, y0 = (k % col) * tw, (k // col) * (th * 2 + 6)
    for j, frac in enumerate([0.08, 0.92]):
        t = tk["ini"] + tk["dur"] * frac
        raw = subprocess.run(f"ffmpeg -v error -ss {t:.2f} -i ../fonte/proxy_480.mp4 -frames:v 1 -f rawvideo -pix_fmt rgb24 -", shell=True, capture_output=True).stdout
        im = Image.frombytes("RGB", (Wp, Hp), raw).resize((tw, th)); dd = ImageDraw.Draw(im)
        z = tk.get("zoom", 1); cw = tw * (1215 / z) / 3840; ch = th / z
        cx = (tw - cw) * tk["cx"]; cy = (th - ch) * tk.get("cy", 0.5)
        dd.rectangle([cx, cy, cx + cw, cy + ch], outline=(255, 210, 0), width=3)
        img.paste(im, (x0, y0 + j * th))
    d.rectangle([x0, y0, x0 + 230, y0 + 20], fill=(0, 0, 0)); d.text((x0 + 3, y0 + 1), f"{n} cx{tk['cx']}", fill=(255, 230, 120), font=F)
img.save("_tmp/recortes.jpg", quality=80)
