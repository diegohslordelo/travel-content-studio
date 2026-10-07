"""Exporta as fotos sem identidade (slides 02 a 10) em 3:4, 1080 × 1440, a partir de ../fonte/.
Roda de dentro de carrosseis/barcelona-10-fotos/rev2/: python3 scripts/fotos.py"""
from PIL import Image
FOTOS = [  # slide, foto, posição vertical do recorte (0 = topo, 1 = base)
    (2, 'museu_barca', .40), (3, 'barceloneta', .60), (4, 'ciutadella_casal', .55),
    (5, 'gotico_diego', .60), (6, 'paella', .55), (7, 'boqueria', .60),
    (8, 'batllo', .50), (9, 'sagrada_teto', .50), (10, 'park_guell', .70),
]
for n, nome, py in FOTOS:
    im = Image.open(f'../fonte/{nome}.jpg')
    w, h = im.size
    if w / h > 3 / 4:  # mais larga que 3:4: corta as laterais no centro
        cw = round(h * 3 / 4); box = ((w - cw) // 2, 0, (w - cw) // 2 + cw, h)
    else:              # mais alta: corta em cima e embaixo
        ch = round(w * 4 / 3); y = round((h - ch) * py); box = (0, y, w, y + ch)
    im.crop(box).resize((1080, 1440), Image.LANCZOS).save(f'out/{n:02d}.jpg', quality=95)
    print(f'{n:02d}', nome, box)
