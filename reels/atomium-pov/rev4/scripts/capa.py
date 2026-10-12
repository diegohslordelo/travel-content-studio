"""Capa 3:4 (1080 × 1440) do Reel "POV: você chegou no Atomium" (REV4): capa_reel_atomium_pov_rev4.jpg.

Pedido do Diego (12/10/2026): a fonte da capa deve ser a da capa do "Barcelona em 20 segundos"
(reels/barcelona-20s/rev4/scripts/capa.py, branch claude/youthful-darwin-edqo3m). Mesmos valores:
  - fundo: quadro real do original (recorte 3:4 e o mesmo tone mapping do vídeo), sem filtro; grão 5% (DS 4.5)
  - texto: DS 1.2 Display (Barlow Condensed 800, 168 px, entrelinha 0,88, tracking −1%), em papel #FCFBF8, linhas
    alinhadas à esquerda dentro do bloco; o bloco é centralizado no canvas pela tinta (x 540) com o centro da tinta
    em y 1000, dentro da área que sobrevive aos dois recortes do Instagram (capa do Reel 9:16 e grid 3:4:
    x 135–945 · y 180–1260)
  - sombra de texto da legenda (DS 3.1) e scrim grafite 0 → 63% de y 760 a 1440 (Display "sempre sobre objeto ou scrim")

Uso (de dentro de reels/atomium-pov/):
  PD_BRUXELAS=PASTA python3 rev4/scripts/capa.py --fontes PASTA_TTF [--arq IMG_2169.MOV] [--t 3.6] [--cx 0.47]
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(REV, "..", "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--arq", default="IMG_2169.MOV")
ap.add_argument("--t", type=float, default=3.6, help="instante do original (s)")
ap.add_argument("--cx", type=float, default=0.47, help="centro do recorte 3:4 (fração da largura do quadro 4K)")
ap.add_argument("--saida", default="capa_reel_atomium_pov_rev4.jpg")
A = ap.parse_args()

sys.path.insert(0, os.path.join(RAIZ, "reels", "apresentacao", "rev8", "scripts"))
sys.argv = sys.argv[:1]
import rev8 as rl  # noqa: E402  (grão, cores e sombra de texto do DS)

CW, CH = 1080, 1440
C = {"linhas": ["POV: VOCÊ", "CHEGOU NO", "ATOMIUM"], "tamanho": 168, "entrelinha": 0.88, "tracking_em": -0.01,
     "centro_x": 540, "centro_y_tinta": 1000, "scrim": {"y0": 760, "y1": 1440, "alfa": 0.63},
     "area_segura": [135, 180, 945, 1260]}
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=rgb48le")

# ---- fundo: recorte 3:4 do quadro 4K (2160 de altura → 1620 de largura)
cw = 1620
x = min(max(int(round(A.cx * 3840 - cw / 2)) // 2 * 2, 0), 3840 - cw)
r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{A.t:.3f}", "-i", os.path.join(os.environ["PD_BRUXELAS"], A.arq),
                    "-frames:v", "1", "-vf", f"crop={cw}:2160:{x}:0,scale={CW}:{CH}:flags=lanczos,{TM}", "-f", "rawvideo", "-"],
                   capture_output=True, check=True, stdin=subprocess.DEVNULL)
base = np.frombuffer(r.stdout, "<u2").reshape(CH, CW, 3).astype(np.float32) / 65535

# ---- texto Display, medido pela tinta
S = 4
f = ImageFont.truetype(os.path.join(A.fontes, "BarlowCondensed-ExtraBold.ttf"), C["tamanho"] * S)
trk = C["tracking_em"] * C["tamanho"] * S
lh = C["tamanho"] * C["entrelinha"]


def mascara(dx, dy):
    img = Image.new("L", (CW * S, CH * S), 0)
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(C["linhas"]):
        xx, yy = dx * S, (dy + i * lh) * S
        for ch in ln:
            d.text((xx, yy), ch, font=f, fill=255, anchor="ls")
            xx += f.getlength(ch) + trk
    m = np.asarray(img.resize((CW, CH), Image.BOX), np.float32) / 255
    ys, xs = np.nonzero(m > 0.02)
    return m, [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


_, c0 = mascara(100, 400)
m, caixa = mascara(100 + C["centro_x"] - (c0[0] + c0[2]) / 2, 400 + C["centro_y_tinta"] - (c0[1] + c0[3]) / 2)

# ---- composição: grão → scrim → sombra de texto → texto
img = rl.overlay_blend(base, rl.grao(0)[:CH, :CW], rl.T["op_grain"])
y = np.arange(CH, dtype=np.float32)
sc = (np.clip((y - C["scrim"]["y0"]) / (C["scrim"]["y1"] - C["scrim"]["y0"]), 0, 1) * C["scrim"]["alfa"])[:, None, None]
img = img * (1 - sc) + rl.GRAFITE * sc
L = rl.CFG["legenda"]
s1 = rl.deslocar(m, L["sombra_dura"][0]) * L["sombra_dura"][1]
s2 = ndimage.gaussian_filter(m, L["sombra_difusa"]["blur"] / 2) * L["sombra_difusa"]["alfa"]
sombra = 1 - (1 - s1) * (1 - s2)
img = img * (1 - sombra[..., None])
img = img * (1 - m[..., None]) + rl.RECIBO * m[..., None]
saida = os.path.join(REV, A.saida)
Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(saida, quality=95, subsampling=0)

# ---- conferência: área que sobrevive aos recortes; simulação do Instagram e miniatura a 25%
a = C["area_segura"]
ok = caixa[0] >= a[0] and caixa[2] <= a[2] and caixa[1] >= a[1] and caixa[3] <= a[3]
c_ = Image.open(saida).convert("RGB")
reel = c_.resize((1440, 1920), Image.LANCZOS).crop((180, 0, 1260, 1920))
grid = reel.crop((0, 240, 1080, 1680))
h = 600
vs = [c_.resize((450, 600)), reel.resize((338, 600)), grid.resize((450, 600)), c_.resize((270, 360)).resize((450, 600))]
rot = ["capa 3:4 inteira", "capa do Reel (9:16)", "grid do perfil", "miniatura 25%"]
out = Image.new("RGB", (sum(v.width for v in vs) + 30 * 3, h + 30), "white")
xx = 0
d = ImageDraw.Draw(out)
for v, t in zip(vs, rot):
    out.paste(v, (xx, 0))
    d.text((xx + 4, h + 8), t, fill=(0, 0, 0))
    xx += v.width + 30
os.makedirs(os.path.join(REV, "qa_frames"), exist_ok=True)
out.save(os.path.join(REV, "qa_frames", "capa_simulacao_instagram.jpg"), quality=88)
print(json.dumps({"capa": saida, "texto_caixa": caixa, "dentro_da_area_segura": ok,
                  "centro_tinta": [(caixa[0] + caixa[2]) / 2, (caixa[1] + caixa[3]) / 2]}, ensure_ascii=False))
