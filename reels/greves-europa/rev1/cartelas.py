#!/usr/bin/env python3
"""Recorta os prints de 22/10/2026 (Playwright, 1200 px de largura, escala 2×) em cartelas legíveis para o Reel.

    python3 cartelas.py <pasta com os prints brutos>

As capturas inteiras (evidência) ficam em research/capturas/. Os recortes não alteram texto, cor ou ordem do material jornalístico: só escolhem a área (veículo, título, data e
foto) e empilham o cabeçalho do site sobre o corpo, com uma linha fina separando as duas partes.
Saída: assets/prints/*.png
"""
import os
import sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "assets", "prints")

# (arquivo, [(x0, y0, x1, y1), ...]) em pixels do print 2×; as partes são empilhadas de cima para baixo
CARTELAS = {
    "it_leggo": ("it_leggo.png", [(200, 0, 2190, 132), (200, 430, 2190, 1760)]),
    "fr_sortiraparis": ("fr_sortiraparis.png", [(40, 40, 1720, 380), (40, 1060, 1720, 2760)]),
    "es_euronews": ("es_euronews.png", [(60, 70, 1600, 1700)]),
    "pt_sol": ("pt_sol.png", [(0, 680, 2370, 900), (380, 1290, 1700, 2480)]),
    "of_mit": ("of_mit.png", [(0, 0, 2400, 1800)]),
    "of_renfe": ("of_renfe.png", [(0, 0, 2400, 1800)]),
    "of_stib": ("of_stib.png", [(0, 0, 2400, 1800)]),
}


def main():
    src = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    for nome, (arq, partes) in CARTELAS.items():
        im = Image.open(os.path.join(src, arq)).convert("RGB")
        cortes = [im.crop(p) for p in partes]
        w = max(c.width for c in cortes)
        h = sum(c.height for c in cortes) + 4 * (len(cortes) - 1)
        card = Image.new("RGB", (w, h), (226, 228, 232))
        y = 0
        for c in cortes:
            card.paste(c, ((w - c.width) // 2, y))
            y += c.height + 4
        # largura final de 1600 px (a cartela ocupa no máximo ~900 px na tela)
        if card.width > 1600:
            card = card.resize((1600, round(card.height * 1600 / card.width)), Image.LANCZOS)
        card.save(os.path.join(OUT, f"{nome}.jpg"), quality=90, optimize=True)
        print(nome, card.size)


if __name__ == "__main__":
    main()
