"""Prepara as 2 camadas da thumbnail (DS V2, 5.5 e 4.5 Parallax) a partir de ../fonte/IMG_1198.HEIC.
Roda de dentro de youtube/barcelona-3-dias/thumbnail/rev1/: python3 scripts/prep.py
Requer: pillow-heif e rembg (modelo birefnet-portrait, baixado na 1ª execução).

Foto: iPhone 17 Pro, 11/03/2026 11:41, 41,4047° N · 2,1754° E (Plaça de Gaudí, em frente à Sagrada Família).
- fundo.jpg  : faixa de cima da foto (céu, Sagrada Família e árvores), sem pessoas, contraste +10.
- pessoas.png: Diego e Marina recortados (máscara do rembg), mesma correção de contraste.
"""
import json
from PIL import Image, ImageOps, ImageEnhance
import pillow_heif

pillow_heif.register_heif_opener()
cfg = json.load(open('thumb.json'))
src = ImageOps.exif_transpose(Image.open('../../fonte/IMG_1198.HEIC')).convert('RGB')
W, H = src.size  # 4284 × 5712


def contraste(im):
    return ImageEnhance.Contrast(im).enhance(1 + cfg['fundo']['contraste'] / 100)


# Fundo: recorte em frações da foto (x0, y0, x1, y1), sem ninguém dentro
x0, y0, x1, y1 = cfg['fundo']['recorte']
fundo = src.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
fundo = contraste(fundo.resize((cfg['fundo']['largura'], round(cfg['fundo']['largura'] * fundo.height / fundo.width)), Image.LANCZOS))
fundo.save('assets/fundo.jpg', quality=92)
print('fundo', fundo.size)

# Pessoas: máscara na foto inteira e recorte justo
from rembg import new_session, remove
base = src.copy()
base.thumbnail((2400, 2400))
mask = remove(base, session=new_session('birefnet-portrait'), only_mask=True)
pessoas = contraste(base)
pessoas.putalpha(mask)
pessoas = pessoas.crop(mask.getbbox())
pessoas.save('assets/pessoas.png')
print('pessoas', pessoas.size, 'bbox na foto de', base.size, mask.getbbox())
