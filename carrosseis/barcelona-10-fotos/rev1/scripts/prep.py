"""Converte as fotos do Drive (HEIC/JPG) para JPG em ../fonte/, com a rotação do EXIF.
Roda de dentro de carrosseis/barcelona-10-fotos/rev1/: python3 scripts/prep.py <pasta_das_fotos>"""
import sys, os
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

USO = {  # foto original (Drive "Fotos") -> nome usado nos slides · data e hora do EXIF
    'IMG_1198.HEIC': 'selfie_sagrada.jpg',                           # 11/03 11:41 · capa
    'grdr 2026-03-09 102340388AC421F1BD.JPG': 'museu_barca.jpg',    # 09/03 10:23
    'IMG_0699.HEIC': 'barceloneta.jpg',                              # 09/03 15:43
    'grdr 2026-03-09 165630560589B7CCDD.JPG': 'ciutadella_casal.jpg',  # 09/03 16:56
    'grdr 2026-03-10 1252014FE50CC6030B.JPG': 'gotico_diego.jpg',   # 10/03 12:52
    '60112E8A-3EB6-4695-B3DA-828209F42E78.JPG': 'paella.jpg',       # 10/03 14:28
    'IMG_6620.HEIC': 'boqueria.jpg',                                 # 10/03 15:54
    'grdr 2026-03-10 1841241FEF6DB8AB8E.JPG': 'batllo.jpg',         # 10/03 18:41
    'grdr 2026-03-11 1038285D9ECDF968ED.JPG': 'sagrada_teto.jpg',   # 11/03 10:38
    'IMG_6716.HEIC': 'park_guell.jpg',                               # 11/03 16:21
}
src, dst = sys.argv[1], '../fonte'
os.makedirs(dst, exist_ok=True)
for a, b in USO.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, a))).convert('RGB')
    im.thumbnail((2400, 2400))
    im.save(os.path.join(dst, b), quality=92)
    print(a, '->', b, im.size)
