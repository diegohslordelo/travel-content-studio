"""Converte as fotos do Drive (HEIC/JPG) para JPG em ../../fonte/, com a rotação do EXIF.
Roda de dentro de carrosseis/roma-3-dias/rev1/: python3 scripts/prep.py <pasta_das_fotos>"""
import sys, os
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

USO = {  # foto original -> nome usado nos slides
    'IMG_6651.JPG': 'coliseu_dia.jpg',      # 26/12 08:52
    'IMG_5064.HEIC': 'trevi.jpg',           # 25/12 10:08
    'IMG_5108.HEIC': 'panteao.jpg',         # 25/12 10:50
    'IMG_5220.heic': 'pincio.jpg',          # 25/12 16:37
    'IMG_5319.HEIC': 'forum.jpg',           # 26/12 13:45
    'IMG_6653.HEIC': 'sao_pedro.jpg',       # 27/12 08:25
    'IMG_6650.HEIC': 'santo_inacio.jpg',    # 27/12 12:31
    'IMG_5523.HEIC': 'gianicolo.jpg',       # 27/12 16:45
    # enviadas pelo Diego no chat em 05/10/2026 (sem EXIF):
    'EXTRA_arena_pai.jpg': 'coliseu_arena.jpg',  # Diego e o pai na arena do Coliseu
    'EXTRA_vila_natal.jpg': 'vila_natal.jpg',    # vila de Natal: árvore-carrossel (reserva)
    'EXTRA_vila_natal_ampla.jpg': 'vila_natal_ampla.jpg',  # vila de Natal: vista ampla (usada)
}
src, dst = sys.argv[1], '../fonte'
os.makedirs(dst, exist_ok=True)
for a, b in USO.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, a))).convert('RGB')
    im.thumbnail((2400, 2400))
    im.save(os.path.join(dst, b), quality=92)
    print(a, '->', b, im.size)
