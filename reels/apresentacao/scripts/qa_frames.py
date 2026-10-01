"""Folha de conferência: primeiro, meio e último frame de cada cena do Reel final, com a zona segura em vermelho."""
import glob
import io
import json
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

reel = sys.argv[1] if len(sys.argv) > 1 else "reel_apresentacao.mp4"
d = json.load(open("lista_de_cortes.json"))
cenas, t = [], 0
for c in d["cortes"]:
    n = round((c["saida"] - c["entrada"]) * 24)
    cenas.append((t / 24, (t + n) / 24, c["rotulo"]))
    t += n
fnt = ImageFont.truetype(glob.glob("/usr/share/fonts/**/DejaVuSans-Bold.ttf", recursive=True)[0], 22)
cols, TW, TH = 5, 216, 384
W = 3 * TW + 12
sheet = Image.new("RGB", (cols * W, ((len(cenas) + cols - 1) // cols) * (TH + 30)), (20, 20, 20))
ds = ImageDraw.Draw(sheet)
for k, (a, b, rot) in enumerate(cenas):
    x, y = (k % cols) * W, (k // cols) * (TH + 30)
    ds.text((x + 4, y + 2), f"{k + 1}. {rot[:30]}", font=fnt, fill=(255, 255, 255))
    for j, tt in enumerate((a + 0.5 / 24, (a + b) / 2, b - 1.5 / 24)):
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{tt:.4f}", "-i", reel, "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im = Image.open(io.BytesIO(png)).convert("RGB")
        dr = ImageDraw.Draw(im, "RGBA")
        for r in ([0, 0, 1080, 220], [0, 1670, 1080, 1920], [960, 0, 1080, 1920]):
            dr.rectangle(r, fill=(255, 0, 0, 50))
        im = im.resize((TW, TH))
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, TH - 26, TW, TH], fill=(0, 0, 0))
        dr.text((4, TH - 24), f"{tt:.2f}s", font=fnt, fill=(255, 220, 80))
        sheet.paste(im, (x + j * TW, y + 30))
sheet.save("qa_frames_por_cena.jpg", quality=88)
print(sheet.size)
