"""Inventário dos brutos: formato de cada arquivo, folha de contato (1 quadro a cada 0,5 s, já em SDR) e nível
de áudio por segundo. Só lê os brutos; não altera, move nem renomeia nada.

Uso (de dentro de reels/barcelona-20s/):
  python3 rev1/scripts/inventario.py [--brutos fonte] [--saida rev1/inventario]
"""
import argparse
import glob
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

EXT = (".mov", ".mp4", ".m4v")


def nivel_por_segundo(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.float32)
    if not len(a):
        return []
    n = len(a) // 16000
    return [round(float(20 * np.log10(np.sqrt((a[i * 16000:(i + 1) * 16000] ** 2).mean()) + 1e-9)), 1)
            for i in range(n)]


def folha(arq, inf, saida):
    passo = 0.5
    n = int(inf["duracao"] / passo)
    tw, th = 135, 240
    filtro, _ = R.filtro_video(arq, {}, tw * 4, th * 4) if inf["w"] / inf["h"] < 1 else (None, None)
    if inf["w"] / inf["h"] >= 1:  # horizontal: mostra o quadro inteiro (o recorte 9:16 é decidido depois)
        tw, th = 240, 135
        filtro, _ = R.filtro_video(arq, {}, tw * 4, th * 4)
    filtro = filtro.replace("format=rgb48le", "format=rgb24") + f",fps=1/{passo},scale={tw}:{th}"
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", filtro, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    q = np.frombuffer(r.stdout, np.uint8).reshape(-1, th, tw, 3)[:n + 1]
    cols = 10 if th > tw else 6
    linhas = (len(q) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, linhas * (th + 16) + 20), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.text((4, 4), f"{os.path.basename(arq)}  {inf['w']}x{inf['h']}  {inf['fps']:.2f} fps  {inf['duracao']:.2f} s  "
                   f"hdr={inf['hdr']}  audio={inf['audio']}", fill=(0, 0, 0))
    for i, fr in enumerate(q):
        x, y = (i % cols) * tw, 20 + (i // cols) * (th + 16)
        im.paste(Image.fromarray(fr), (x, y))
        d.text((x + 3, y + th + 2), f"{i * passo:.1f}s", fill=(0, 0, 0))
    im.save(saida, quality=85)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brutos", default="fonte")
    ap.add_argument("--saida", default=os.path.join("rev1", "inventario"))
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    arqs = sorted(f for f in glob.glob(os.path.join(a.brutos, "**", "*"), recursive=True) if f.lower().endswith(EXT))
    tab = []
    for arq in arqs:
        inf = R.info(arq)
        rel = os.path.relpath(arq, a.brutos)
        print(f"{rel:30s} {inf['w']}x{inf['h']} {inf['fps']:.2f}fps {inf['duracao']:6.2f}s hdr={inf['hdr']} "
              f"{inf['codec']} audio={inf['audio']}", flush=True)
        folha(arq, inf, os.path.join(a.saida, os.path.splitext(rel.replace(os.sep, "_"))[0] + ".jpg"))
        tab.append({"arquivo": rel, **inf, "nivel_dbfs_por_s": nivel_por_segundo(arq)})
    json.dump(tab, open(os.path.join(a.saida, "inventario.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(tab)} arquivos")


if __name__ == "__main__":
    sys.exit(main())
