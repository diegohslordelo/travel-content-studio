"""Thumbnail "lago" do vlog de Bruges.

Pedidos do Diego (21/11/2026):
  - "Me recorte nessa foto comendo waffle e coloque nessa foto […] com o lago atrás […] e o recibo do lado. Agora de uma
    forma que não cubra minha cara. Nem o waffle."
  - "Não precisa colocar nada escrito no recibo […] igual você fez com o de Barcelona" (Recibo sem texto: `reciboMudo`).
  - "Tem que ser o design system igual dos outros, com a placa. […] meu cabelo ficou cortado e o fundo tá com umas cores
    aí editadas que ficaram ruins. Coloque a imagem exatamente como eu te mandei […] Cuidado pra não me cortar."

Roda de reels/bruges-yt:  python -I rev5/thumb/lago/montar_thumb_lago.py   (depois: thumb.mjs com props_thumb_lago.json)
  1. Você: quadro de 10:12,5 da fonte (`fonte/1120.mp4`, 612,54 s, o mesmo momento do print, em 4K: `diego_waffle_4k.jpg`),
     recortado pelo BiRefNet (rembg `birefnet-general`; `_tmp/recorte_birefnet-general.png`, refeito se faltar), sem
     nenhum ajuste de cor. No vídeo, o topo da sua cabeça (cabelo e óculos) encosta na borda de cima do quadro: por
     isso o recorte entra na ALTURA INTEIRA da thumbnail, com o topo na borda de cima e a base na de baixo, e nada
     aparece cortado. A borda esquerda do recorte (a jaqueta, cortada pelo quadro do vídeo) some num degradê de 160 px,
     atrás do Recibo (o mesmo recurso da thumbnail de Barcelona).
  2. Fundo: `minnewater_IMG_2671.jpg`, a foto como veio (sem contraste, brilho, filtro ou escurecimento); só a faixa
     16:9 (a foto é vertical) com a torre da Igreja de Nossa Senhora, o salgueiro e o lago.
  3. Composição de Barcelona (DS V2, 5.5): Placa Pequena (75%) no canto superior esquerdo (margem 48), você à direita,
     Recibo na base esquerda (70%, margem 48), na frente da borda do recorte.
Saída: `foto_lago_diego.jpg` (2560 × 1440).
"""
import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 2560, 1440  # 2× o quadro da thumbnail (1280 × 720)
RECORTE = "_tmp/recorte_birefnet-general.png"
FUNDO_Y = 900  # faixa da foto (largura inteira, 1932 px): y 900 → 1987
DIEGO_X = 580  # canto esquerdo do recorte (px de 2560): o rosto fica em x ≈ 890 da thumbnail
DEGRADE = 320  # 160 px da thumbnail


def main():
    if not os.path.exists(RECORTE):
        from rembg import new_session, remove
        remove(Image.open(os.path.join(AQUI, "diego_waffle_4k.jpg")), session=new_session("birefnet-general"), post_process_mask=False).save(RECORTE)
    foto = Image.open(os.path.join(AQUI, "minnewater_IMG_2671.jpg")).convert("RGB")
    alt = round(foto.width * 9 / 16)
    fundo = foto.crop((0, FUNDO_Y, foto.width, FUNDO_Y + alt)).resize((W, H), Image.LANCZOS).convert("RGBA")
    d = Image.open(RECORTE).convert("RGBA").resize((round(3840 * H / 2160), H), Image.LANCZOS)  # altura inteira
    px = np.asarray(d).copy()
    px[:, :DEGRADE, 3] = (px[:, :DEGRADE, 3] * np.linspace(0, 1, DEGRADE)[None, :]).astype(np.uint8)
    fundo.alpha_composite(Image.fromarray(px), (DIEGO_X, 0))
    fundo.convert("RGB").save(os.path.join(AQUI, "foto_lago_diego.jpg"), quality=95)
    a = px[:, :, 3] > 128
    ys, xs = np.nonzero(a)
    print(f"você: x {(DIEGO_X + xs.min()) / 2:.0f}–{(DIEGO_X + xs.max()) / 2:.0f}, y {ys.min() / 2:.0f}–{ys.max() / 2:.0f} da thumbnail")


if __name__ == "__main__":
    main()
