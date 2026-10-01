"""Tira 5 quadros ao longo de um trecho com o crop 9:16 final, para vários centros de crop.

Uso: python3 testar_crop.py MASTER SAIDA.jpg entrada saida centro [centro ...]
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402


def main():
    master, saida = sys.argv[1], sys.argv[2]
    a, z = R.segundos(sys.argv[3]), R.segundos(sys.argv[4])
    centros = [float(x) for x in sys.argv[5:]]
    tw, th, n = 180, 320, 5
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    folha = Image.new("RGB", (n * (tw + 4) + 70, len(centros) * (th + 4)), (15, 15, 15))
    d = ImageDraw.Draw(folha)
    tmp = saida + ".png"
    for i, cx in enumerate(centros):
        d.text((4, i * (th + 4) + th // 2), f"x={cx:.2f}", font=f, fill=(255, 230, 120))
        for k in range(n):
            t = a + (z - a) * (k + 0.5) / n
            c = {"entrada": t, "saida": t + 1, "centro_x": cx}
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", master, "-frames:v", "1", "-vf",
                            f"{R.filtro_crop(c)},{R.TONEMAP.replace('format=yuv420p', 'format=rgb24')},scale={tw}:{th}",
                            tmp], check=True)
            folha.paste(Image.open(tmp).convert("RGB"), (70 + k * (tw + 4), i * (th + 4)))
    os.remove(tmp)
    folha.save(saida, quality=88)


if __name__ == "__main__":
    main()
