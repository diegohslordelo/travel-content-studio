"""Storyboard com textos: um quadro de cada corte (crop e cor finais) com a camada de texto do render naquele instante.

Uso: python3 storyboard_texto.py lista_de_cortes.json SAIDA.jpg
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

CORES = {"gancho": (217, 105, 58), "apresentacao": (31, 58, 77), "montagem": (232, 178, 74), "aviso": (120, 160, 90)}


def main():
    edl = R.carregar(sys.argv[1])
    ev, _ = R.eventos_de_texto(edl)
    por = {e[2]: e for e in ev}
    cortes = edl["_cortes"]
    tw, th, cols = 270, 480, 7
    rows = (len(cortes) + cols - 1) // cols
    folha = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 74) + 8), (18, 18, 18))
    d = ImageDraw.Draw(folha)
    f1 = ImageFont.truetype(os.path.join(R.FONTES, "Montserrat-Bold.ttf"), 15)
    f2 = ImageFont.truetype(os.path.join(R.FONTES, "Montserrat-SemiBold.ttf"), 13)
    for i, c in enumerate(cortes):
        # quadro no meio do corte, ou no meio da primeira legenda da fala
        if c.get("legendas"):
            lg = c["legendas"][-1]
            t_src = (float(lg["de"]) + float(lg["ate"])) / 2
        else:
            t_src = c["entrada"] + (c["saida"] - c["entrada"]) * float(c.get("quadro_story", 0.5))
        frac = (t_src - c["entrada"]) / (c["saida"] - c["entrada"])
        t_reel = c["ini"] + (c["fim"] - c["ini"]) * frac
        if c["bloco"] == "apresentacao":  # meio do trecho de narração que cai nesse corte
            t_reel = (c["ini"] + c["fim"]) / 2
            t_src = c["entrada"] + (t_reel - c["ini"])
            frac = (t_src - c["entrada"]) / (c["saida"] - c["entrada"])
        tmp = os.path.join(edl["_tmp"], f"sbt_{i:02d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t_src:.3f}", "-i", c["_arq"], "-map", "0:v:0", "-frames:v", "1",
                        "-vf", R.filtro_video(R.corte_parado(c, frac), "rgb24"), tmp], check=True)
        img = Image.open(tmp).convert("RGBA")
        for nome, alfa, dy in R.quadro_de_texto(ev, t_reel):
            _, _, _, cam, (x, y), _ = por[nome]
            if alfa < 1:
                cam = cam.copy(); cam.putalpha(cam.getchannel("A").point(lambda v: int(v * alfa)))
            img.alpha_composite(cam, (x, y + dy))
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 74)
        folha.paste(img.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.rectangle([x, y + th, x + tw, y + th + 20], fill=CORES[c["bloco"]])
        d.text((x + 5, y + th + 2), f"{i + 1}. {c['bloco'].upper()} {c['ini']:.2f}–{c['fim']:.2f}s", font=f1, fill=(255, 255, 255))
        d.text((x + 5, y + th + 24), (c.get("cidade") or "Barcelona") + (" · com ela" if c.get("com_ela") else ""), font=f2, fill=(255, 220, 120))
        orig = os.path.basename(c["_arq"]) if c.get("arquivo") else "master BCN"
        d.text((x + 5, y + th + 44), f"{orig} {c['entrada']:.2f}–{c['saida']:.2f}s", font=f2, fill=(200, 200, 200))
    folha.save(sys.argv[2], quality=88)
    print(sys.argv[2], folha.size)


if __name__ == "__main__":
    main()
