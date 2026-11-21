"""Thumbnail "lago" do vlog de Bruges (pedido do Diego, 21/11/2026): "Me recorte nessa foto comendo waffle e coloque nessa
foto […] com o lago atrás […] coloque só Bruges escrito e o recibo do lado. Agora de uma forma que não cubra minha cara.
Nem o waffle."

Roda de reels/bruges-yt:  python -I rev5/thumb/lago/montar_thumb_lago.py
  1. o quadro de 10:12,5 da fonte (`fonte/1120.mp4`, 612,54 s: o mesmo momento do print que o Diego mandou, em 4K) já está
     em `diego_waffle_4k.jpg`; o recorte (você + garfo + caixinha do waffle + óculos) sai do BiRefNet (rembg,
     modelo `birefnet-general`) e fica em `_tmp/recorte_birefnet-general.png` (refeito se faltar);
  2. fundo: `minnewater_IMG_2671.jpg` (foto do Diego, Minnewater, retrato 1932 × 2576), faixa 16:9 com o céu, a torre da
     Igreja de Nossa Senhora, o salgueiro e o lago; sem ajuste de cor;
  3. você à esquerda, encostado na borda de baixo e na da esquerda (como no quadro original, sem corte flutuando), com o
     rosto e o waffle fora da área do título e do Recibo; a torre fica livre entre o waffle e o Recibo.
Saída: `foto_lago_diego.jpg` (2560 × 1440), usada por `props_thumb_lago.json` (ThumbYT) → `../thumb_lago.png`.
"""
import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 2560, 1440  # 2× o quadro da thumbnail (1280 × 720)
RECORTE = "_tmp/recorte_birefnet-general.png"
# faixa do fundo na foto (px da foto original): largura 1500 a partir da esquerda → a torre cai em ~64% da largura
FUNDO = (0, 760, 1500, 760 + round(1500 * 9 / 16))
ESCALA_DIEGO = 0.28 * 2  # altura do quadro 4K (2160) → 605 px na thumbnail de 720


def main():
    if not os.path.exists(RECORTE):
        from rembg import new_session, remove
        remove(Image.open(os.path.join(AQUI, "diego_waffle_4k.jpg")), session=new_session("birefnet-general"), post_process_mask=False).save(RECORTE)
    fundo = Image.open(os.path.join(AQUI, "minnewater_IMG_2671.jpg")).convert("RGB").crop(FUNDO).resize((W, H), Image.LANCZOS).convert("RGBA")
    d = Image.open(RECORTE).convert("RGBA")
    d = d.resize((round(d.width * ESCALA_DIEGO), round(d.height * ESCALA_DIEGO)), Image.LANCZOS)
    fundo.alpha_composite(d, (0, H - d.height))
    fundo.convert("RGB").save(os.path.join(AQUI, "foto_lago_diego.jpg"), quality=95)
    a = np.asarray(d)[:, :, 3] > 128
    ys, xs = np.nonzero(a)
    print(f"você ocupa x {xs.min() / 2:.0f}–{xs.max() / 2:.0f}, y {(H - d.height + ys.min()) / 2:.0f}–720 na thumbnail")


if __name__ == "__main__":
    main()
