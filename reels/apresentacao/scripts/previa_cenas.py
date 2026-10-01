"""Prévia fiel de cenas do Reel: quadro com crop e cor finais + camada de texto do render naquele instante.

Uso: python3 previa_cenas.py lista_de_cortes.json SAIDA.jpg N:frac [N:frac ...]   (N = número do corte, de 1)
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402


def main():
    edl = R.carregar(sys.argv[1])
    eventos, _ = R.eventos_de_texto(edl)
    por_nome = {e[2]: e for e in eventos}
    telas = []
    for arg in sys.argv[3:]:
        n, frac = arg.split(":")
        c = edl["_cortes"][int(n) - 1]
        frac = float(frac)
        t_src = c["entrada"] + (c["saida"] - c["entrada"]) * frac
        t_reel = c["ini"] + (c["fim"] - c["ini"]) * frac
        tmp = os.path.join(edl["_tmp"], f"previa_{n}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t_src:.3f}", "-i", c["_arq"], "-map", "0:v:0",
                        "-frames:v", "1", "-vf", R.filtro_video(R.corte_parado(c, frac), "rgb24"), tmp], check=True)
        img = Image.open(tmp).convert("RGBA")
        for nome, alfa, dy in R.quadro_de_texto(eventos, t_reel):
            _, _, _, camada, (x, y), _ = por_nome[nome]
            img.alpha_composite(camada, (x, y + dy))
        orig = os.path.basename(c["_arq"]) if c.get("arquivo") else "master BCN"
        telas.append((f"{n}. {t_reel:.1f}s · {c.get('cidade') or c['bloco']}", f"{orig} {t_src:.2f}s", img.convert("RGB")))
    tw, th = 432, 768
    folha = Image.new("RGB", (len(telas) * (tw + 10) + 10, th + 70), (18, 18, 18))
    d = ImageDraw.Draw(folha)
    f1 = ImageFont.truetype(os.path.join(R.FONTES, "Montserrat-Bold.ttf"), 20)
    f2 = ImageFont.truetype(os.path.join(R.FONTES, "Montserrat-SemiBold.ttf"), 16)
    for k, (t1, t2, im) in enumerate(telas):
        x = 10 + k * (tw + 10)
        folha.paste(im.resize((tw, th), Image.LANCZOS), (x, 10))
        d.text((x + 4, th + 16), t1, font=f1, fill=(240, 240, 240))
        d.text((x + 4, th + 42), t2, font=f2, fill=(190, 190, 190))
    folha.save(sys.argv[2], quality=90)
    print(sys.argv[2])


if __name__ == "__main__":
    main()
