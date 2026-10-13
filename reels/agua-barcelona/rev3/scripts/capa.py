"""Capa do Reel 'Não compre água em Barcelona' (REV3): capa_reel_agua_barcelona_rev3.jpg (1080 × 1920).

Fórmula de capa do DS (5.5): lugar (placa) + emoção (rosto) + prova (objeto). Aqui:
  - fundo: um quadro real do master (Diego com a garrafa na praça), recorte 9:16 e tone mapping iguais aos do Reel
  - texto do painel (Reel 03, capa): ÁGUA DE GRAÇA, na Placa variante Estática do DS 2.1 (sem animação; brilho de
    esmalte congelado a 30% do percurso): rótulo 'BARCELONA' + destino 'ÁGUA DE GRAÇA' (104 px: 13 caracteres, DS 1.2)
    + módulo de seta, 872 px de largura (máximo do DS), em x 72 · y 640 (dentro da área 3:4 do grid, y 240–1680)
  - scrim inferior e grão de 5% do DS; nenhum outro texto

Uso (de dentro de reels/agua-barcelona/):
  python3 rev3/scripts/capa.py --fontes PASTA --master rev3/_tmp/master_esparso.mov --tempo 1112.0
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rev3 as R  # noqa: E402

PLACA_CAPA = {"rotulo": "BARCELONA", "destino": "ÁGUA DE GRAÇA", "destino_px": 104, "modulo": "seta", "x": 72, "y": 640,
              "escala": 1.0}


def quadro_master(master, t, centro_x):
    inf = R.info_fonte(master)
    cadeia = R.TONEMAP_RGB if inf["hdr"] else R.SDR_RGB
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", master, "-vf",
                        f"{R.filtro_crop(centro_x, inf['w'], inf['h'])},{cadeia}", "-frames:v", "1", "-f", "rawvideo",
                        "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, "<u2").reshape(R.H, R.W, 3).astype(np.float32) / 65535


def compor_capa(fontes, master, t, centro_x):
    placa = R.Placa(PLACA_CAPA, fontes, "placa_capa")
    e = placa.estado(1000)  # assentada, sem desfoque nem rotação
    e["brilho"] = 0.30      # variante Estática
    im, x, y = placa.camada(e)
    camada = np.zeros((R.H, R.W, 4), np.float32)
    R.sobre(camada, im, x, y)
    img = R.overlay_blend(quadro_master(master, t, centro_x), R.grao(0), R.T["op_grain"])
    s = R.scrim_alfa()
    img = img * (1 - s) + R.GRAFITE * s
    a = camada[..., 3:4]
    return np.clip(img * (1 - a) + camada[..., :3], 0, 1), placa


def previa_grid(arq_capa, saida):
    """Como a capa aparece no grid do perfil (3:4, recorte central y 240–1680) e em miniatura de 25%."""
    c = Image.open(arq_capa).convert("RGB")
    f = Image.new("RGB", (540 + 20 + 270, 720 + 24), (255, 255, 255))
    f.paste(c.crop((0, 240, 1080, 1680)).resize((540, 720), Image.LANCZOS), (0, 0))
    f.paste(c.resize((270, 480), Image.LANCZOS), (560, 0))
    d = ImageDraw.Draw(f)
    d.text((4, 726), "grid 3:4 (y 240-1680)", fill=(0, 0, 0))
    d.text((564, 726), "miniatura 25%", fill=(0, 0, 0))
    f.save(saida, quality=92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--master", required=True)
    ap.add_argument("--tempo", type=float, default=1112.0, help="segundo do master")
    ap.add_argument("--centro_x", type=float, default=0.48)
    ap.add_argument("--saida", default=os.path.join(R.REV, "capa_reel_agua_barcelona_rev3.jpg"))
    a = ap.parse_args()
    img, placa = compor_capa(a.fontes, a.master, a.tempo, a.centro_x)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(a.saida, quality=95, subsampling=0)
    previa_grid(a.saida, os.path.join(R.QA_DIR, "capa_grid_e_miniatura.jpg"))
    print(a.saida, placa.medidas)


if __name__ == "__main__":
    sys.exit(main())
