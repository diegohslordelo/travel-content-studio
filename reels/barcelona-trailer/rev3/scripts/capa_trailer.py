"""Capa do Reel trailer de Barcelona: capa_reel_barcelona_trailer_rev3.jpg (1080 × 1920).

Fórmula de capa do DS (5.5): lugar (placa) + emoção (rosto). Fundo: quadro real do Park Güell (30:36,6 do original), recorte 9:16
com o rosto do Diego centrado, sem filtro. Placa `3 DIAS EM / BARCELONA` na variante Estática do DS 2.1 (brilho de esmalte
congelado a 30% do percurso), scrim inferior e grão de 5%. Nenhum outro texto.

Exceção de posição (só nesta capa): placa em x 72 · y 1136 (mesma ideia da exceção da capa do Reel de apresentação, y 1104, com 32 px a mais para folgar do queixo), e não em y 640,
porque o rosto ocupa y 330–1100 e a placa cobriria o queixo e a boca. A regra geral do DS não muda.

Uso (de dentro de reels/barcelona-trailer/):
  BCN_ORIGINAL=… python3 rev3/scripts/capa_trailer.py --fontes PASTA_TTF [--t 1836.6] [--cx 0.42]
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(REV, "..", "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--t", type=float, default=1836.6, help="instante do original (s)")
ap.add_argument("--cx", type=float, default=0.42, help="centro do recorte 9:16 (fração da largura do quadro 4K)")
ap.add_argument("--saida", default="capa_reel_barcelona_trailer_rev3.jpg")
A = ap.parse_args()

sys.path.insert(0, os.path.join(RAIZ, "youtube", "barcelona", "rev2", "scripts"))
sys.argv = sys.argv[:1]
import rev2 as yt  # noqa: E402
sys.path.insert(0, os.path.join(RAIZ, "reels", "apresentacao", "rev8", "scripts"))
import rev8 as rl  # noqa: E402

yt.ARGS_FONTES = A.fontes
yt.K = 1
W, H = 1080, 1920
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=rgb48le")
cw = 1216
x = min(max(int(round(A.cx * 3840 - cw / 2)) // 2 * 2, 0), 3840 - cw)
r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{A.t:.3f}", "-i", os.environ["BCN_ORIGINAL"], "-frames:v", "1",
                    "-vf", f"crop={cw}:2160:{x}:0,scale={W}:{H}:flags=lanczos,{TM}", "-f", "rawvideo", "-"],
                   capture_output=True, check=True, stdin=subprocess.DEVNULL)
base = np.frombuffer(r.stdout, "<u2").reshape(H, W, 3).astype(np.float32) / 65535

# ---- placa estática (a mesma construção da capa do YouTube, na grade 1:1 do Reel)
face, modulo, info = yt.placa_pecas({"variante": "abertura", "linha1": "3 DIAS EM", "linha2": "BARCELONA"})
fw, hh, lado = info["fw"], info["hh"], info["lado"]
pad = 90
c = yt.tela(hh + 2 * pad, fw + lado + 2 * pad)
yt.sobre(c, modulo, pad + fw, pad)
bw = yt.PLACA["brilho_largura"] * fw
cx_ = -bw + (fw + 2 * bw) * 0.30
yy, xx = np.mgrid[0:hh, 0:fw].astype(np.float32)
xs = xx + (yy - hh / 2) * np.tan(np.radians(yt.PLACA["brilho_incl"]))
perfil = np.clip(1 - np.abs(xs - cx_) / (bw / 2), 0, 1) * yt.PLACA["brilho_alfa"]
al = face[..., 3]
rgb = np.where(al[..., None] > 0, face[..., :3] / np.maximum(al[..., None], 1e-6), 0)
yt.sobre(c, yt._premult(yt._soft_light_branco(rgb, perfil * (al > 0)), al), pad, pad)
alfa = c[..., 3]
sp = yt.PLACA["sombra_proj"]
s1 = yt._desl(alfa, yt.PLACA["sombra_dura"][0]) * yt.PLACA["sombra_dura"][1]
s2 = ndimage.gaussian_filter(yt._desl(ndimage.grey_erosion(alfa, size=(21, 21)), sp["y"]), sp["blur"] / 2) * sp["alfa"]
out = yt._premult(np.zeros(alfa.shape + (3,), np.float32), 1 - (1 - s1) * (1 - s2))
yt.sobre(out, c, 0, 0)

PX, PY = 72, 1136
img = rl.overlay_blend(base, rl.grao(0), rl.T["op_grain"])
s = rl.scrim_alfa()
img = img * (1 - s) + rl.GRAFITE * s
cam = np.zeros((H, W, 4), np.float32)
yt.sobre(cam, out, PX - pad, PY - pad)
a = cam[..., 3:4]
img = np.clip(img * (1 - a) + cam[..., :3], 0, 1)
assert PX + info["w_design"] <= 944, info["w_design"]            # zona segura x 72–944
assert PY + info["h_design"] <= 1440, info["h_design"]           # base da zona segura y 1440
arq = os.path.join(REV, A.saida)
Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(arq, quality=95, subsampling=0)

# ---- prévia: grid 3:4 do perfil (recorte central y 240–1680) e miniaturas de 25% e 8%
c_ = Image.open(arq).convert("RGB")
f = Image.new("RGB", (540 + 20 + 270 + 20 + 270, 744), (255, 255, 255))
f.paste(c_.crop((0, 240, 1080, 1680)).resize((540, 720), Image.LANCZOS), (0, 0))
f.paste(c_.resize((270, 480), Image.LANCZOS), (560, 0))
f.paste(c_.resize((90, 160), Image.LANCZOS).resize((270, 480), Image.NEAREST), (850, 0))
d = ImageDraw.Draw(f)
for xx_, t in ((4, "grid 3:4 (y 240–1680)"), (564, "miniatura 25%"), (854, "miniatura 8%")):
    d.text((xx_, 726), t, fill=(0, 0, 0))
os.makedirs(os.path.join(REV, "qa_frames"), exist_ok=True)
f.save(os.path.join(REV, "qa_frames", "capa_grid_e_miniaturas.jpg"), quality=92)
print(arq, "placa", round(info["w_design"]), "×", round(info["h_design"]), "em x", PX, "y", PY)
