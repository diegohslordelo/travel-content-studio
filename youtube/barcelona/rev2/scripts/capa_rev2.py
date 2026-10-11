"""Thumbnail da REV2 (DS V2 5.5, 1280 × 720): foto real (IMG_1198.HEIC, Drive), contraste +10, placa pequena (75%)
`3 DIAS EM / BARCELONA` no canto superior esquerdo com margem 48, estática (brilho congelado a 30%).

Uso (de dentro de youtube/barcelona/):  python3 rev2/scripts/capa_rev2.py FOTO --fontes DIR [--recorte x0,y0,largura] [--saida ARQ]
Capa 2 (foto da praça, corpo inteiro): --recorte 219,1470,1185 --saida capa_barcelona_rev2_b.jpg
Saídas: rev2/capa_barcelona_rev2.jpg (1280 × 720) e rev2/qa_frames/capa_teste_168x94.png (teste de miniatura).
"""
import argparse
import os
import sys

import numpy as np
import pillow_heif
from PIL import Image, ImageEnhance, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
ap = argparse.ArgumentParser()
ap.add_argument("foto")
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--recorte", default="0,1480,3560", help="x0,y0,largura do recorte 16:9 na foto")
ap.add_argument("--saida", default="capa_barcelona_rev2.jpg")
a = ap.parse_args()

import rev2  # noqa: E402  (tokens, cores e a placa do pipeline; K = 2 → desenho em 2560 × 1440)
from scipy import ndimage  # noqa: E402

rev2.ARGS_FONTES = a.fontes
K = rev2.K
TW, TH = 1280, 720

# ---- foto: recorte 16:9 com o casal à direita do centro e a Sagrada Família ao fundo; contraste +10
pillow_heif.register_heif_opener()
foto = ImageOps.exif_transpose(Image.open(a.foto)).convert("RGB")      # 4284 × 5712
x0, y0, cw = (int(v) for v in a.recorte.split(","))
recorte = foto.crop((x0, y0, x0 + cw, y0 + cw * 9 // 16)).resize((TW * K, TH * K), Image.LANCZOS)
recorte = ImageEnhance.Contrast(recorte).enhance(1.10)
base = np.asarray(recorte, np.float32) / 255

# ---- placa pequena (variante 'cta' = linhas de 28 e 96 px, seta 72), estática
it = {"variante": "cta", "linha1": "3 DIAS EM", "linha2": "BARCELONA"}
face, modulo, info = rev2.placa_pecas(it)
fw, hh, lado = info["fw"], info["hh"], info["lado"]
pad = 90 * K
c = rev2.tela(hh + 2 * pad, fw + lado + 2 * pad)
rev2.sobre(c, modulo, pad + fw, pad)
# brilho de esmalte congelado a 30% do percurso (DS 2.1, variante Estática)
bw = rev2.PLACA["brilho_largura"] * fw
cx = -bw + (fw + 2 * bw) * 0.30
yy, xx = np.mgrid[0:hh, 0:fw].astype(np.float32)
xs = xx + (yy - hh / 2) * np.tan(np.radians(rev2.PLACA["brilho_incl"]))
perfil = np.clip(1 - np.abs(xs - cx) / (bw / 2), 0, 1) * rev2.PLACA["brilho_alfa"]
al = face[..., 3]
rgb = np.where(al[..., None] > 0, face[..., :3] / np.maximum(al[..., None], 1e-6), 0)
rev2.sobre(c, rev2._premult(rev2._soft_light_branco(rgb, perfil * (al > 0)), al), pad, pad)
alfa = c[..., 3]
sp = rev2.PLACA["sombra_proj"]
s1 = rev2._desl(alfa, rev2.PLACA["sombra_dura"][0] * K) * rev2.PLACA["sombra_dura"][1]
s2 = ndimage.gaussian_filter(rev2._desl(ndimage.grey_erosion(alfa, size=(2 * 10 * K + 1,) * 2), sp["y"] * K), sp["blur"] * K / 2) * sp["alfa"]
out = rev2._premult(np.zeros(alfa.shape + (3,), np.float32), 1 - (1 - s1) * (1 - s2))
rev2.sobre(out, c, 0, 0)

# ---- composição em sRGB (a foto é SDR): placa em x 48 · y 48 (margem do token layout.yt-thumb.margin)
m = rev2.tok("layout.yt-thumb.margin")["value"]
tela = rev2.tela(TH * K, TW * K)
tela[..., :3] = base
tela[..., 3] = 1
rev2.sobre(tela, out, m * K - pad, m * K - pad)
img = Image.fromarray((np.clip(tela[..., :3], 0, 1) * 255 + 0.5).astype(np.uint8)).resize((TW, TH), Image.LANCZOS)
assert (m + info["w_design"]) <= rev2.tok("layout.yt-thumb.timestamp-free-x")["value"]
rev = os.path.dirname(AQUI)
img.save(os.path.join(rev, a.saida), quality=92)
os.makedirs(os.path.join(rev, "qa_frames"), exist_ok=True)
img.resize((168, 94), Image.LANCZOS).save(os.path.join(rev, "qa_frames", a.saida.replace(".jpg", "_teste_168x94.png")))
print("placa:", round(info["w_design"]), "×", round(info["h_design"]), "px na grade 1280")
