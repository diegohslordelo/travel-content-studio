"""Prévia de enquadramento: 3 quadros por plano (início, meio, fim) no recorte 9:16, com a zona da placa (x 72–942 ·
y 640–816), a zona segura do Reel e a faixa da legenda. Uso: python3 rev1/scripts/storyboard.py --versao a"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R, pd  # noqa: E401,E402
ap = argparse.ArgumentParser(); ap.add_argument("--versao", required=True); ap.add_argument("--brutos", default="fonte/drive/Reels 1")
a = ap.parse_args()
ed = json.load(open(os.path.join(pd.REV, f"versao_{a.versao}.json"), encoding="utf-8"))
tw, th = 216, 384
cols = []
for i, p in enumerate(ed["planos"]):
    arq = os.path.join(a.brutos, p["arquivo"]); f, rec = R.filtro_video(arq, p, tw * 2, th * 2)
    f = f.replace("format=rgb48le", "format=rgb24") + f",scale={tw}:{th}"
    col = []
    for t in (p["entrada"] + 0.05, p["entrada"] + p["duracao"] / 2, p["entrada"] + p["duracao"] - 0.08):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", arq, "-vf", f, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
        im = Image.fromarray(np.frombuffer(r.stdout, np.uint8).reshape(th, tw, 3)); d = ImageDraw.Draw(im); k = tw / 1080
        d.rectangle([72 * k, 256 * k, 944 * k, 1440 * k], outline=(255, 0, 0))
        if i == 0 or i == len(ed["planos"]) - 1:
            d.rectangle([72 * k, 640 * k, 942 * k, 816 * k], outline=(255, 200, 0), width=2)
        if i == 0:
            d.rectangle([200 * k, 1360 * k, 880 * k, 1420 * k], outline=(0, 255, 255))
        col.append(im)
    cols.append((p, col))
W_ = len(cols) * (tw + 8); H_ = 3 * (th + 4) + 40
S = Image.new("RGB", (W_, H_), "white"); d = ImageDraw.Draw(S)
for i, (p, col) in enumerate(cols):
    for j, im in enumerate(col): S.paste(im, (i * (tw + 8), j * (th + 4)))
    d.text((i * (tw + 8) + 2, 3 * (th + 4) + 2), f"{i+1} {p['arquivo']}\n{p.get('categoria','')[:28]}", fill=(0, 0, 0))
out = os.path.join(pd.REV, "_tmp", f"storyboard_{a.versao}.jpg"); S.save(out, quality=85); print(out)
