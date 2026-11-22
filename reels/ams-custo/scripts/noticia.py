"""Recorte da notícia (Brasilturis, 18/11/2026: 'Amsterdã elevará taxa turística para 16% em 2027'), do print da página
(noticia/brasilturis_2026-11-18.png, Playwright, 1080 px a 2×): faixa com o logo, título + linha fina + data e o
1º parágrafo (12,5% → 16%). Só recorte, sem redesenhar nada da página. Saída: public/noticia.png
Uso (de dentro de reels/ams-custo/): python3 scripts/noticia.py"""
import os
from PIL import Image, ImageDraw
P = Image.open("noticia/brasilturis_2026-11-18.png").convert("RGB")
x0, x1 = 56, 1576
logo = P.crop((40, 40, 1576, 210))            # faixa azul com o logo
titulo = P.crop((x0, 820, x1, 1290))          # NOTÍCIAS | DESTINOS, título, linha fina, data
par = P.crop((x0, 2525, x1, 2755))            # 1º parágrafo
W = x1 - x0 + 72                               # margem de 36 px dos dois lados
fundo = P.getpixel((30, 1500))
azul = P.getpixel((20, 250))
so_logo = P.crop((40, 40, 560, 210))           # só o logo (sem as cotações do canto)
H = 170 + 24 + titulo.height + 24 + par.height + 30
C = Image.new("RGB", (W, H), fundo)
ImageDraw.Draw(C).rectangle((0, 0, W, 170), fill=azul)
C.paste(so_logo, (20, 0))
y = 170 + 24
C.paste(titulo, (36, y)); y += titulo.height + 24
C.paste(par, (36, y))
# cantos arredondados (o recorte de papel do celular)
m = Image.new("L", C.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), 28, fill=255)
out = Image.new("RGBA", C.size); out.paste(C, (0, 0), m)
os.makedirs("public", exist_ok=True)
out.save("public/noticia.png")
print("public/noticia.png", out.size)
