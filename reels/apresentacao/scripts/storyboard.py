"""Storyboard da lista de cortes: um quadro 9:16 por corte (crop e tone mapping iguais aos do render).

Uso: python3 storyboard.py lista_de_cortes.json SAIDA.jpg
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CORES = {"gancho": (217, 105, 58), "apresentacao": (31, 58, 77), "montagem": (232, 178, 74), "aviso": (120, 160, 90)}


def mmss(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def main():
    edl = R.carregar(sys.argv[1])
    tmp = os.path.join(edl["_tmp"], "story")
    os.makedirs(tmp, exist_ok=True)
    tw, th = 216, 384
    cortes = edl["_cortes"]
    cols = min(len(cortes), 9)
    lins = (len(cortes) + cols - 1) // cols
    faixa = 92
    folha = Image.new("RGB", (cols * (tw + 8) + 8, lins * (th + faixa + 8) + 8), (18, 18, 18))
    d = ImageDraw.Draw(folha)
    f1, f2 = ImageFont.truetype(FONTE, 15), ImageFont.truetype(FONTE, 13)
    for i, c in enumerate(cortes):
        frac = float(c.get("quadro_story", 0.5))
        meio = c["entrada"] + (c["saida"] - c["entrada"]) * frac
        arq = os.path.join(tmp, f"s_{i:02d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{meio:.3f}", "-i", c["_arq"], "-map", "0:v:0", "-frames:v", "1",
                        "-vf", f"{R.filtro_video(R.corte_parado(c, frac), 'rgb24')},scale={tw}:{th}", arq], check=True)
        x = 8 + (i % cols) * (tw + 8)
        y = 8 + (i // cols) * (th + faixa + 8)
        folha.paste(Image.open(arq).convert("RGB"), (x, y))
        cor = CORES.get(c["bloco"], (90, 90, 90))
        d.rectangle([x, y + th, x + tw, y + th + faixa], fill=(30, 30, 30))
        d.rectangle([x, y + th, x + tw, y + th + 22], fill=cor)
        d.text((x + 6, y + th + 3), f"{i + 1}. {c['bloco'].upper()}  {c['ini']:.1f}-{c['fim']:.1f}s", font=f1, fill=(255, 255, 255))
        d.text((x + 6, y + th + 28), f"{mmss(c['entrada'])} > {mmss(c['saida'])}", font=f2, fill=(230, 230, 230))
        d.text((x + 6, y + th + 48), (c.get("cidade", "") + " · " if c.get("cidade") else "") + c.get("rotulo", "")[:30], font=f2, fill=(255, 220, 120))
        d.text((x + 6, y + th + 68), c.get("rotulo2", "")[:30], font=f2, fill=(200, 200, 200))
    folha.save(sys.argv[2], quality=90)
    print(sys.argv[2])


if __name__ == "__main__":
    main()
