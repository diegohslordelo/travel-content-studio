"""Capa do Reel p201 (REV1): rev1/capa_reel_bahia_camp_nou_rev1.jpg (1080 × 1920).

  - fundo: um quadro real do gancho (IMG_0552, 4K HLG → SDR com o mesmo tone mapping e recorte do Reel)
  - texto "BAHIA NO CAMP NOU" numa placa de duas linhas (estrutura da variante Abertura do DS 2.1:
    rótulo Condensed 600 36 px +8% + destino h1 Condensed 800 128 px), variante Estática (brilho congelado a 30%)
  - mesma posição da placa no Reel (x 72 · y 1104), dentro da área 3:4 do grid (y 240–1680)
  - scrim inferior e grão de 5% do DS; nenhum outro texto

Uso (de dentro de reels/bahia-camp-nou/):
  python3 rev1/scripts/capa.py --fontes PASTA --t 3.2 [--saida arquivo.jpg]
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rev1 as R  # noqa: E402

CAPA = {"rotulo": "BAHIA NO", "destino": "CAMP NOU", "rotulo_px": 36, "rotulo_tracking_em": 0.08,
        "destino_px": 128, "destino_lh": 0.9, "espaco_px": 12, "padding_v": 28,
        "_bundle": "estrutura de 2 linhas e módulo = altura da face (pd-bundle.css .pd-plate__label/__dest/__mod)"}


def placa_duas_linhas(pasta):
    """Face amarela com rótulo + destino e módulo de seta com lado = altura da face. Mesmo material da placa do Reel."""
    P = R.CFG["placa"]
    S = R.SS
    f1 = R.fonte("BarlowCondensed-SemiBold.ttf", CAPA["rotulo_px"] * S, pasta)
    f2 = R.fonte(P["fonte"], CAPA["destino_px"] * S, pasta)
    t1 = CAPA["rotulo_tracking_em"] * CAPA["rotulo_px"] * S
    t2 = P["tracking_em"] * CAPA["destino_px"] * S
    l1 = sum(f1.getlength(c) for c in CAPA["rotulo"]) + t1 * (len(CAPA["rotulo"]) - 1)
    l2 = sum(f2.getlength(c) for c in CAPA["destino"]) + t2 * (len(CAPA["destino"]) - 1)
    alt1 = CAPA["rotulo_px"]
    alt2 = CAPA["destino_px"] * CAPA["destino_lh"]
    hh = int(round(2 * CAPA["padding_v"] + alt1 + CAPA["espaco_px"] + alt2))
    fw = int(round(2 * P["padding_h"] + max(l1, l2) / S))
    assert fw + hh <= 872, f"placa com {fw + hh} px passa da largura máxima (872)"
    r = R.T["radius_plate"]
    m = R.mascara((fw * S, hh * S), lambda d: d.rounded_rectangle([0, 0, fw * S - 1, hh * S - 1], radius=r * S,
                                                                  fill=255, corners=(True, False, False, True)))
    i_, rr, lw = P["filete_inset"] * S, P["filete_raio"] * S, P["filete_px"] * S

    def filete(d):
        d.line([(fw * S - i_, i_ + lw / 2), (i_ + rr, i_ + lw / 2)], fill=255, width=lw)
        d.line([(fw * S - i_, hh * S - i_ - lw / 2), (i_ + rr, hh * S - i_ - lw / 2)], fill=255, width=lw)
        d.line([(i_ + lw / 2, i_ + rr), (i_ + lw / 2, hh * S - i_ - rr)], fill=255, width=lw)
        d.arc([i_, i_, i_ + 2 * rr, i_ + 2 * rr], 180, 270, fill=255, width=lw)
        d.arc([i_, hh * S - i_ - 2 * rr, i_ + 2 * rr, hh * S - i_], 90, 180, fill=255, width=lw)
    fil = R.mascara((fw * S, hh * S), filete)
    cap1 = -f1.getbbox("H", anchor="ls")[1]
    cap2 = -f2.getbbox("H", anchor="ls")[1]
    y_l1 = CAPA["padding_v"] * S + (alt1 * S - cap1) / 2 + cap1
    y_l2 = (CAPA["padding_v"] + alt1 + CAPA["espaco_px"]) * S + (alt2 * S - cap2) / 2 + cap2

    def texto(d):
        for txt, f, trk, y in ((CAPA["rotulo"], f1, t1, y_l1), (CAPA["destino"], f2, t2, y_l2)):
            x = P["padding_h"] * S
            for c in txt:
                d.text((x, y), c, font=f, fill=255, anchor="ls")
                x += f.getlength(c) + trk
    txt = R.mascara((fw * S, hh * S), texto)
    rb, rx, ry = P["rebite_px"] * S, P["rebite_x"] * S, P["rebite_y"] * S
    reb = R.mascara((fw * S, hh * S), lambda d: [d.ellipse([rx, y, rx + rb, y + rb], fill=255)
                                                  for y in (ry, hh * S - ry - rb)])
    luz = R.mascara((fw * S, hh * S), lambda d: [d.ellipse([rx + rb * .22, y + rb * .18, rx + rb * .52, y + rb * .48],
                                                           fill=255) for y in (ry, hh * S - ry - rb)])
    m, fil, txt, reb, luz = [R.reduzir(a[..., None])[..., 0] for a in (m, fil, txt, reb, luz)]
    rgb = np.broadcast_to(R.AMARELO, m.shape + (3,)).copy()
    rgb *= (1 - R.T["op_grain"] * R.ruido_fractal(*m.shape, 7))[..., None]
    bl, ba = P["bevel_luz"]
    bs, bsa = P["bevel_sombra"]
    topo = np.clip(m - R.deslocar(m, bl), 0, 1) * ba
    base = np.clip(m - R.deslocar(m, -bs), 0, 1) * bsa
    rgb = rgb * (1 - topo[..., None]) + topo[..., None]
    rgb = rgb * (1 - base[..., None])
    rgb = rgb * (1 - (fil * P["filete_alfa"])[..., None]) + R.GRAFITE * (fil * P["filete_alfa"])[..., None]
    rgb = rgb * (1 - (reb * P["rebite_alfa"])[..., None]) + R.GRAFITE * (reb * P["rebite_alfa"])[..., None]
    rgb = rgb * (1 - (np.clip(reb - R.deslocar(reb, -1.5), 0, 1) * 0.35)[..., None])
    rgb = rgb * (1 - (luz * 0.4)[..., None]) + (luz * 0.4)[..., None]
    rgb = rgb * (1 - txt[..., None]) + R.GRAFITE * txt[..., None]
    face = R.premult(rgb, m)
    lado = hh
    mm = R.mascara((lado * S, hh * S), lambda d: d.rounded_rectangle([0, 0, lado * S - 1, hh * S - 1], radius=r * S,
                                                                     fill=255, corners=(False, True, True, False)))
    seta = R.mascara((lado * S, hh * S), lambda d: d.polygon([(x * S, y * S) for x, y in R.caminho_seta(lado)], fill=255))
    mm, seta = [R.reduzir(a[..., None])[..., 0] for a in (mm, seta)]
    rgbm = np.broadcast_to(R.GRAFITE, mm.shape + (3,)).copy()
    from scipy import ndimage
    for camada in (np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07,
                   np.clip(mm - R.deslocar(mm, 2), 0, 1) * 0.08):
        rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
    rgbm = rgbm * (1 - seta[..., None]) + R.AMARELO * seta[..., None]
    return face, R.premult(rgbm, mm), {"face": [fw, hh], "modulo": lado, "largura_total": fw + lado}


class PlacaCapa(R.Placa):
    def __init__(self, pasta):
        self.face, self.modulo, self.medidas = placa_duas_linhas(pasta)
        self.fw, self.hh = self.face.shape[1], self.face.shape[0]
        self.cache = {}


def quadro(t):
    p = dict(R.plano(1))
    p["inicio"], p["nq"] = t, 1
    return next(R.quadros_plano(p)), p["recorte"]


def previa_grid(arq_capa, saida):
    c = Image.open(arq_capa).convert("RGB")
    grid = c.crop((0, 240, 1080, 1680))
    f = Image.new("RGB", (540 + 20 + 270 + 20 + 270, 720 + 24), (255, 255, 255))
    f.paste(grid.resize((540, 720), Image.LANCZOS), (0, 0))
    f.paste(c.resize((270, 480), Image.LANCZOS), (560, 0))
    f.paste(c.resize((90, 160), Image.LANCZOS).resize((270, 480), Image.NEAREST), (850, 0))
    d = ImageDraw.Draw(f)
    d.text((4, 726), "grid 3:4 (y 240-1680)", fill=(0, 0, 0))
    d.text((564, 726), "miniatura 25%", fill=(0, 0, 0))
    d.text((854, 726), "miniatura 8%", fill=(0, 0, 0))
    f.save(saida, quality=92)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--t", type=float, required=True, help="instante no IMG_0552 (s)")
    ap.add_argument("--saida", default=os.path.join(R.REEL, "rev1", "capa_reel_bahia_camp_nou_rev1.jpg"))
    a = ap.parse_args()
    placa = PlacaCapa(a.fontes)
    e = placa.estado(1000)
    e["brilho"] = 0.30
    im, x, y = placa.camada(e)
    camada = np.zeros((R.H, R.W, 4), np.float32)
    R.sobre(camada, im, x, y)
    b, recorte = quadro(a.t)
    img = R.overlay_blend(b, R.grao(0), R.T["op_grain"])
    s = R.scrim_alfa()
    img = img * (1 - s) + R.GRAFITE * s
    al = camada[..., 3:4]
    img = np.clip(img * (1 - al) + camada[..., :3], 0, 1)
    Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(a.saida, quality=95, subsampling=0)
    previa_grid(a.saida, a.saida.replace(".jpg", "_grid_e_miniatura.jpg"))
    print(a.saida, placa.medidas, "placa x", R.CFG["placa"]["x"], "y", R.CFG["placa"]["y"], "recorte", recorte)


if __name__ == "__main__":
    sys.exit(main())
