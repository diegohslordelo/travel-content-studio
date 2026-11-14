"""Borra o nome e a foto do seguidor no print do comentário (pedido do Diego: só o comentário aparece).
O print original fica fora do git (../fonte/prints/); só a versão borrada entra em imagens/.
Uso (de dentro de reels/disney-frozen/rev1):
  python3 scripts/borrar.py ../fonte/prints/comentario.png x,y,w,h [x,y,w,h ...] [--recorte x,y,w,h]
Cada x,y,w,h é uma área a borrar (px do print). --recorte corta o print antes (só o bloco do comentário).
O borrão é forte (pixela 24 px + desfoque 18 px): o nome não pode ser lido nem reconstruído."""
import os
import sys

from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
if len(args) < 2:
    sys.exit(__doc__)
src = args[0]
caixas, recorte = [], None
i = 1
while i < len(args):
    if args[i] == "--recorte":
        recorte = tuple(int(v) for v in args[i + 1].split(","))
        i += 2
        continue
    caixas.append(tuple(int(v) for v in args[i].split(",")))
    i += 1
im = Image.open(src).convert("RGB")
for x, y, w, h in caixas:
    area = im.crop((x, y, x + w, y + h))
    pequeno = area.resize((max(1, w // 24), max(1, h // 24)), Image.BILINEAR)
    area = pequeno.resize((w, h), Image.NEAREST).filter(ImageFilter.GaussianBlur(18))
    im.paste(area, (x, y))
if recorte:
    x, y, w, h = recorte
    im = im.crop((x, y, x + w, y + h))
out = os.path.join(AQUI, "imagens", "comentario_borrado.png")
im.save(out)
print(f"{out} ({im.width} × {im.height})")
