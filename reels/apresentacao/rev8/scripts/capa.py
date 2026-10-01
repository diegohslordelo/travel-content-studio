"""Capa do Reel de apresentação no Design System REV 2: capa_reel_apresentacao_rev8.jpg (1080 × 1920).

Fórmula de capa do DS (5.5): lugar (placa) + emoção (rosto) + prova (objeto). Aqui:
  - fundo: um quadro real da selfie "Buenos días, Barcelona!" (base sem texto da REV6), sem filtro
  - placa PRIMEIRO DIA → na variante Estática do DS 2.1 (sem animação; brilho de esmalte congelado a 30% do percurso),
    na mesma posição do Reel (x 72 · y 1104)
  - scrim inferior e grão de 5% do DS; nenhum outro texto

Uso:
  python3 rev8/scripts/capa.py --fontes PASTA --quadro 402 [--saida arquivo.jpg]
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rev8 as R  # noqa: E402


def quadro_base(k):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", R.BASE, "-vf",
                        f"select=eq(n\\,{k}),scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,"
                        "format=rgb48le", "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, "<u2").reshape(R.H, R.W, 3).astype(np.float32) / 65535


def compor_capa(fontes, k):
    placa = R.Placa(fontes)
    e = placa.estado(1000)  # assentada, sem desfoque nem rotação
    e["brilho"] = 0.30      # variante Estática: brilho congelado a 30% do percurso
    im, x, y = placa.camada(e)
    camada = np.zeros((R.H, R.W, 4), np.float32)
    R.sobre(camada, im, x, y)
    b = quadro_base(k)
    img = R.overlay_blend(b, R.grao(0), R.T["op_grain"])
    s = R.scrim_alfa()
    img = img * (1 - s) + R.GRAFITE * s
    a = camada[..., 3:4]
    img = img * (1 - a) + camada[..., :3]
    return np.clip(img, 0, 1), placa


def previa_grid(arq_capa, saida):
    """Como a capa aparece no grid do perfil (3:4, recorte central 1080 × 1440 de y 240 a 1680) e na miniatura de 25%."""
    c = Image.open(arq_capa).convert("RGB")
    grid = c.crop((0, 240, 1080, 1680))
    mini = c.resize((270, 480), Image.LANCZOS)
    f = Image.new("RGB", (540 + 20 + 270 + 20 + 270, 720 + 24), (255, 255, 255))
    f.paste(grid.resize((540, 720), Image.LANCZOS), (0, 0))
    f.paste(mini, (560, 0))
    f.paste(c.resize((270, 480), Image.LANCZOS).resize((90, 160), Image.LANCZOS).resize((270, 480), Image.NEAREST), (850, 0))
    d = ImageDraw.Draw(f)
    d.text((4, 726), "grid 3:4 (y 240–1680)", fill=(0, 0, 0))
    d.text((564, 726), "miniatura 25%", fill=(0, 0, 0))
    d.text((854, 726), "miniatura 8%", fill=(0, 0, 0))
    f.save(saida, quality=92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--quadro", type=int, required=True, help="número do quadro na base REV6 (24 fps)")
    ap.add_argument("--saida", default=os.path.join(R.REV8, "capa_reel_apresentacao_rev8.jpg"))
    a = ap.parse_args()
    img, placa = compor_capa(a.fontes, a.quadro)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(a.saida, quality=95, subsampling=0)
    print(a.saida, placa.medidas)


if __name__ == "__main__":
    sys.exit(main())
