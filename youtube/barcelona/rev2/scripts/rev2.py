"""REV2 do vlog de Barcelona (YouTube, 16:9): a REV1 adequada ao DS V2 5.4 (abertura, capítulos com Varredura,
recibos, chamada, símbolo 1º, cobertura dos gráficos antigos do CapCut). Parte de rev1/scripts/rev1.py.

O que entra (DS V2, 5.4 YouTube; componentes da seção 2):
  - lugar      : lower third "placa de direção pequena" (painel grafite, H3 + Plex Mono amarelo + seta ↗),
                 x 96 · base y 960, Chegada curta 320 ms, fica 4 s, sai pela direita (240 ms)
  - preco      : etiqueta de valor (recibo de 1 linha): rótulo Plex Mono 30, € em PD Placar 64, ≈ R$ em
                 Barlow 500 40, picote no topo; desliza da esquerda (160 ms), o número gira (240 ms)
  - recibo     : recibo curto (2 linhas + total), impresso de cima para baixo (320 ms por etapa)
  - hospedagem : etiqueta de bagagem (furo, cordão, pictograma de cama), balança 8° → −3° (480 ms)
  - humor      : bilhete com a letra do Diego (Caneta, provisória Reenie Beanie), assinatura Escrita

Cor: o original é HEVC Main 10 HLG / BT.2020. Os gráficos são desenhados em sRGB (valores dos tokens) e convertidos
para HLG pelo mapeamento de gráficos do BT.2408 (branco de referência 203 cd/m² = 75% do sinal HLG), depois para
Y'CbCr BT.2020 10 bits (faixa limitada) aqui mesmo, sem depender da matriz padrão do swscale.

Etapas:
  python3 rev2/scripts/rev2.py plano   --cortes rev1/analise/cortes_de_cena.json   # tempos finais
  python3 rev2/scripts/rev2.py sprites --fontes DIR    # um clipe FFV1 com alfa por item (em _tmp/)
  python3 rev2/scripts/rev2.py previa                  # trechos editados em SDR 1280×720 + quadros de QA
  python3 rev2/scripts/rev2.py final                   # vídeo 4K HLG completo (x265) + áudio original copiado
Rode de dentro de youtube/barcelona/. O original vem de $BCN_ORIGINAL (ou fonte/barcelona_original.mov).
Fontes (SIL OFL, Google Fonts): Barlow-Medium, Barlow-Bold, BarlowCondensed-SemiBold/-Bold/-ExtraBold,
IBMPlexMono-Medium, ReenieBeanie.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REV, "rev2.json"), encoding="utf-8"))
TOK = json.load(open(os.path.normpath(os.path.join(REV, CFG["tokens"])), encoding="utf-8"))
TMP = os.path.join(REV, "_tmp")
QA_DIR = os.path.join(REV, "qa_frames")
PLANO = os.path.join(REV, "plano_rev2.json")
FPS = CFG["original"]["fps"]
NQ = CFG["original"].get("quadros_saida", CFG["original"]["quadros"])   # REV2: sem a vinheta do CapCut
K = CFG["escala"]  # grade do DS 1920 × 1080 → 3840 × 2160
W, H = 1920 * K, 1080 * K
RATE = Decimal(CFG["cotacao"]["eur_brl"])
ORIGINAL = os.environ.get(CFG["original"]["variavel_ambiente"],
                          os.path.join(os.path.dirname(REV), CFG["original"]["arquivo_padrao"]))


# ---------------------------------------------------------------- tokens

def tok(caminho):
    n = TOK
    for p in caminho.split("."):
        n = n[p]
    v = n["$value"]
    while isinstance(v, str) and v.startswith("{"):
        v = tok(v.strip("{}"))
    return v


def hexcor(caminho):
    v = tok(caminho)
    h = v["hex"].lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO = hexcor("color.signal.500")
GRAFITE = hexcor("color.night.900")
ASFALTO = hexcor("color.night.500")
CONCRETO = hexcor("color.night.300")
PAPEL = hexcor("color.paper.500")
RECIBO = hexcor("color.paper.0")
CANETA = hexcor("color.ink.500")
BRANCO = np.ones(3, np.float32)
PRETO = np.zeros(3, np.float32)


def estilo(nome):
    s = tok(f"font.style.{nome}")
    ls = s.get("letterSpacing", {"value": 0})
    ls = ls["$value"]["value"] if isinstance(ls, dict) and "$value" in ls else (ls.get("value", 0) if isinstance(ls, dict) else ls)
    return {"px": s["fontSize"]["$value"]["value"], "peso": s["fontWeight"], "lh": s["lineHeight"], "track": ls}


def bezier(p):
    x1, y1, x2, y2 = p

    def f(t):
        if t <= 0:
            return 0.0
        if t >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            bx = 3 * (1 - m) ** 2 * m * x1 + 3 * (1 - m) * m ** 2 * x2 + m ** 3
            lo, hi = (m, hi) if bx < t else (lo, m)
        s = (lo + hi) / 2
        return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s ** 2 * y2 + s ** 3
    return f


E_OUT = bezier(tok("easing.ease-out"))
E_ARR = bezier(tok("easing.ease-arrive"))
E_EXIT = bezier(tok("easing.ease-exit"))
D_FAST = tok("duration.dur-fast")["value"]      # 160
D_BASE = tok("duration.dur-base")["value"]      # 240
D_SLOW = tok("duration.dur-slow")["value"]      # 400
OP_FIBRA = tok("opacity.op-fiber")
OP_GRAO = tok("opacity.op-grain")


def kf(chaves, t, curva=E_OUT):
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- valores

def brl(eur):
    v = (Decimal(eur) * RATE).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def eurfmt(eur):
    v = Decimal(eur).quantize(Decimal("0.01"))
    return "€ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def seg(t):
    m, s = t.split(":")
    return int(m) * 60 + float(s)


def tc(s):
    return f"{int(s // 60):02d}:{s % 60:06.3f}"


# ---------------------------------------------------------------- desenho (float, pré-multiplicado, escala K)

FONTES = {}


def fonte(arq, px):
    chave = (arq, px)
    if chave not in FONTES:
        FONTES[chave] = ImageFont.truetype(os.path.join(ARGS_FONTES, arq), int(round(px * K)))
    return FONTES[chave]


def texto(s, arq, px, track=0.0, tnum=False):
    """máscara do texto (float) com tracking; devolve (máscara, largura, linha_de_base, altura_de_caixa_alta)."""
    f = fonte(arq, px)
    feats = ["tnum"] if tnum else None
    tam = px * K
    larg = 0.0
    pos = []
    for ch in s:
        pos.append(larg)
        larg += f.getlength(ch, features=feats) + track * tam
    larg -= track * tam
    asc, desc = f.getmetrics()
    img = Image.new("L", (int(math.ceil(larg)) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(img)
    for ch, x in zip(s, pos):
        d.text((x + 2, 2 + asc), ch, font=f, fill=255, anchor="ls", features=feats)
    caixa = f.getbbox("H", anchor="ls")
    return np.asarray(img, np.float32) / 255, larg, 2 + asc, -caixa[1]


def tela(h, w):
    return np.zeros((h, w, 4), np.float32)


def pintar(dst, mask, rgb, x, y, op=1.0):
    """mask (float) pintada com rgb em (x, y), por cima de dst (pré-multiplicado)."""
    h, w = mask.shape
    x, y = int(round(x)), int(round(y))
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    a = mask[y0 - y:y1 - y, x0 - x:x1 - x, None] * op
    reg = dst[y0:y1, x0:x1]
    reg[..., :3] = rgb * a + reg[..., :3] * (1 - a)
    reg[..., 3:] = a + reg[..., 3:] * (1 - a)


def sobre(dst, src, x, y):
    h, w = src.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    d[:] = s + d * (1 - s[..., 3:])


def forma(w, h, desenho, ss=4):
    img = Image.new("L", (int(w * ss), int(h * ss)), 0)
    desenho(ImageDraw.Draw(img), ss)
    return np.asarray(img.resize((int(w), int(h)), Image.BOX), np.float32) / 255


def retangulo(w, h, r):
    return forma(w, h, lambda d, s: d.rounded_rectangle([0, 0, w * s - 1, h * s - 1], radius=r * s, fill=255))


def caixa_borrada(a, r, eixo):
    if r < 1:
        return a
    r = int(r)
    p = np.pad(a, [(r + 1, r) if i == eixo else (0, 0) for i in range(a.ndim)], mode="constant")
    c = np.cumsum(p, axis=eixo, dtype=np.float64)
    n = a.shape[eixo]
    sl = lambda i0, i1: tuple(slice(i0, i1) if i == eixo else slice(None) for i in range(a.ndim))  # noqa: E731
    return ((c[sl(2 * r + 1, 2 * r + 1 + n)] - c[sl(0, n)]) / (2 * r + 1)).astype(np.float32)


def gauss(a, sigma):
    """gaussiana aproximada por 3 caixas (sem scipy)."""
    if sigma <= 0:
        return a
    w = math.sqrt(4 * sigma * sigma / 3 + 1)
    r = max(int((w - 1) / 2), 1)
    for _ in range(3):
        a = caixa_borrada(caixa_borrada(a, r, 0), r, 1)
    return a


def erodir(a, r):
    r = int(r)
    if r <= 0:
        return a
    out = a.copy()
    for _ in range(r):
        p = np.pad(out, 1, mode="constant")
        out = np.minimum.reduce([p[1:-1, 1:-1], p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]])
    return out


def deslocar(a, dy):
    out = np.zeros_like(a)
    dy = int(round(dy))
    if dy >= 0:
        out[dy:] = a[:a.shape[0] - dy]
    else:
        out[:dy] = a[-dy:]
    return out


SOMBRAS = {
    # tokens shadow-*: (deslocamento y, desfoque CSS, espalhamento, opacidade) em px da grade 1920
    "plate": [(3, 0, 0, 0.28), (18, 32, -10, 0.55)],
    "paper": [(1, 1, 0, 0.20), (14, 26, -10, 0.50)],
}


def com_sombra(obj, tipo, margem):
    """obj pré-multiplicado → mesmo objeto com a sombra do token (luz de cima), numa tela com margem."""
    m = int(margem * K)
    h, w = obj.shape[:2]
    out = tela(h + 2 * m, w + 2 * m)
    alfa = np.pad(obj[..., 3], m, mode="constant")
    for dy, blur, spread, op in SOMBRAS[tipo]:
        a = erodir(alfa, -spread * K) if spread < 0 else alfa
        a = gauss(deslocar(a, dy * K), blur * K / 2)
        pintar(out, a, PRETO, 0, 0, op)
    sobre(out, obj, m, m)
    return out


def ruido(h, w, semente, op):
    rng = np.random.default_rng(semente)
    n = rng.random((h, w), dtype=np.float32)
    return 1 - op * gauss(n, 0.6)


def fibra(obj, semente, op):
    obj[..., :3] *= ruido(obj.shape[0], obj.shape[1], semente, op)[..., None]


def seta(lado):
    """seta de placa (haste 16% + ponta triangular cheia) em 45° (↗): máscara lado × lado."""
    ss = 4
    img = Image.new("L", (lado * ss, lado * ss), 0)
    d = ImageDraw.Draw(img)
    s = lado * ss
    hh = 0.16 * s
    d.rectangle([0.10 * s, s / 2 - hh / 2, 0.58 * s, s / 2 + hh / 2], fill=255)
    d.polygon([(0.50 * s, 0.20 * s), (0.92 * s, 0.50 * s), (0.50 * s, 0.80 * s)], fill=255)
    img = img.rotate(45, resample=Image.BICUBIC, center=(s / 2, s / 2))
    return np.asarray(img.resize((lado, lado), Image.BOX), np.float32) / 255


def girar(img, ang, centro):
    """gira img (pré-multiplicada) em graus (positivo = horário, como CSS) em torno de centro (x, y)."""
    out = np.empty_like(img)
    for c in range(4):
        out[..., c] = np.asarray(Image.fromarray(np.ascontiguousarray(img[..., c]), "F").rotate(-ang, resample=Image.BILINEAR, center=centro))
    return np.clip(out, 0, None)


# ---------------------------------------------------------------- componentes

FT = {"h3": "BarlowCondensed-SemiBold.ttf", "cond700": "BarlowCondensed-Bold.ttf", "placar": "BarlowCondensed-Bold.ttf",
      "mono": "IBMPlexMono-Medium.ttf", "b500": "Barlow-Medium.ttf", "b700": "Barlow-Bold.ttf", "caneta": "ReenieBeanie.ttf"}


def lugar_obj(nome, micro):
    """placa de direção pequena (lower third): painel grafite + H3 papel + Plex Mono amarelo + seta ↗."""
    h3, mi = estilo("h3"), estilo("micro")
    m1, w1, b1, c1 = texto(nome, FT["h3"], h3["px"], h3["track"])
    m2, w2, b2, c2 = texto(micro, FT["mono"], mi["px"], mi["track"])
    pt, pr, pb, pl, gap, sl = 26, 30, 26, 36, 28, 80   # padding do .pd-dir do bundle (o DS não fixa)
    lh1, lh2, ent = h3["px"] * h3["lh"], mi["px"] * mi["lh"], 8
    tw = max(w1, w2) / K
    wd, hd = pl + tw + gap + sl + pr, pt + lh1 + ent + lh2 + pb
    w, h = int(round(wd * K)), int(round(hd * K))
    obj = tela(h, w)
    painel = retangulo(w, h, tok("radius.tag")["value"] * K)
    pintar(obj, painel, GRAFITE, 0, 0)
    filete = painel - np.pad(retangulo(w - 4 * K, h - 4 * K, (tok("radius.tag")["value"] - 2) * K), 2 * K)
    pintar(obj, np.clip(filete, 0, 1), BRANCO, 0, 0, 0.08)
    y1 = (pt + lh1 / 2) * K + c1 / 2 - b1
    y2 = (pt + lh1 + ent + lh2 / 2) * K + c2 / 2 - b2
    pintar(obj, m1, RECIBO, pl * K - 2, y1)
    pintar(obj, m2, AMARELO, pl * K - 2, y2)
    xs = (pl + tw + gap) * K
    return obj, {"seta": seta(sl * K), "seta_xy": (xs, (hd - sl) / 2 * K), "w": wd, "h": hd}


def etiqueta_obj(rotulo, eur):
    """etiqueta de valor (recibo de 1 linha): rótulo Plex Mono 30 · € PD Placar 64 · ≈ R$ Barlow 500 40."""
    mi = estilo("micro")
    ml, wl, bl, cl = texto(rotulo, FT["mono"], mi["px"], mi["track"])
    mn, wn, bn, cn = texto(eurfmt(eur), FT["placar"], 64, 0, tnum=True)
    mr, wr, br, cr = texto("≈ " + brl(eur), FT["b500"], 40, 0)
    pt, pr, pb, pl, ent, gap = 32, 30, 20, 30, 8, 16
    lhl = mi["px"] * mi["lh"]
    wd = pl + max(wl, wn + gap * K + wr) / K + pr
    hd = pt + lhl + ent + 64 + pb
    w, h = int(round(wd * K)), int(round(hd * K))
    base = tela(h, w)
    pintar(base, retangulo(w, h, tok("radius.paper")["value"] * K), RECIBO, 0, 0)
    fibra(base, 11, OP_FIBRA)
    furo = forma(6 * K, 6 * K, lambda d, s: d.ellipse([0, 0, 6 * K * s - 1, 6 * K * s - 1], fill=255))
    for x in np.arange(12 * K, w - 12 * K, 16 * K):   # picote: furos de 6 px a cada 16 px (DS 1.6)
        pintar(base, furo, CONCRETO, x, 10 * K)
    pintar(base, ml, ASFALTO, pl * K - 2, (pt + lhl / 2) * K + cl / 2 - bl)
    ybase = (pt + lhl + ent + 64 / 2) * K + cn / 2        # linha de base do número e do R$
    pintar(base, mr, ASFALTO, pl * K + wn + gap * K - 2, ybase - br)
    num = {"m": mn, "x": pl * K - 2, "y": ybase - bn, "clip": (int((pt + lhl + ent - 4) * K), int((pt + lhl + ent + 64 + 6) * K))}
    return base, num, {"w": wd, "h": hd}


def recibo_obj(item):
    """recibo (DS 2.6, 5.4): cabeçalho (lugar), micro Plex Mono (bairro · data; sem hora: o Diego não tem o horário),
    linhas item × € (Barlow 500 38 · PD Placar 48), TOTAL (ou POR PESSOA) em PD Placar 96 + ≈ R$ Barlow 500 40,
    rodapé da cotação. Papel térmico 600 px, borda serrilhada embaixo."""
    wd, pt, px_, pb, dente = 600, 40, 44, 26, 16
    util = wd - 2 * px_
    w = wd * K
    els, y = [], pt
    mh, wh, bh, ch = texto(item["cabecalho"], FT["cond700"], 52, 0.02)
    assert wh / K <= util, item["cabecalho"]
    els.append((mh, GRAFITE, px_, y + 52 / 2, ch, bh)); y += 52 + 10
    mm, wm, bm, cm = texto(item["micro"], FT["mono"], 26, 0.04)
    els.append((mm, ASFALTO, px_, y + 35 / 2, cm, bm)); y += 35 + 18
    tracejadas = [y]; y += 3 + 6
    total = Decimal(0)
    cortes = []
    for ln in item["linhas"]:
        y += 12
        mi_, wi, bi, ci = texto(ln["item"], FT["b500"], 38, 0)
        mv, wv, bv, cv = texto(eurfmt(ln["eur"]), FT["placar"], 48, 0, tnum=True)
        els.append((mi_, GRAFITE, px_, y + 48 / 2, cv, bi))
        if (wi + wv) / K + 24 > util:      # item longo: o valor desce para a linha de baixo
            y += 48 + 4
        els.append((mv, GRAFITE, wd - px_ - wv / K, y + 48 / 2, cv, bv)); y += 48
        cortes.append(y + 10)
        total += Decimal(ln["eur"])
    y += 24
    linha_total = y; y += 3 + 16
    mt, wt, bt, ct = texto(item.get("rotulo_total", "TOTAL"), FT["h3"], 32, 0.08)
    mv, wv, bv, cv = texto(eurfmt(total), FT["placar"], 96, 0, tnum=True)
    assert (wt + wv) / K + 24 <= util
    els.append((mt, GRAFITE, px_, y + 96 - 32 / 2, ct, bt))
    num = {"m": mv, "x": (wd - px_) * K - wv, "y": (y + 96 / 2) * K + cv / 2 - bv, "clip": (int((y - 4) * K), int((y + 100) * K))}
    y += 96 + 8
    mr, wr, br, cr = texto("≈ " + brl(total), FT["b500"], 40, 0)
    els.append((mr, ASFALTO, wd - px_ - wr / K, y + 40 / 2, cr, br)); y += 40 + 22
    mf, wf, bf, cf = texto(f"cotação € 1 = R$ {str(RATE).replace('.', ',')} · {CFG['cotacao']['data'][:5]}", FT["mono"], 24, 0.03)
    els.append((mf, ASFALTO, px_, y + 31 / 2, cf, bf)); y += 31 + pb
    hd = y + dente
    h = int(hd * K)
    base = tela(h, w)
    corpo = np.zeros((h, w), np.float32)
    corpo[:int((hd - dente) * K)] = 1
    dentes = forma(w, dente * K, lambda d, s: [d.polygon([(x * s, 0), ((x + dente * K / 2) * s, dente * K * s), ((x + dente * K) * s, 0)], fill=255)
                                               for x in range(0, w, dente * K)])
    corpo[int((hd - dente) * K):] = dentes[:h - int((hd - dente) * K)]
    pintar(base, corpo, RECIBO, 0, 0)
    fibra(base, 23, OP_FIBRA)
    for yy in tracejadas:
        for x in range(px_ * K, (wd - px_) * K, 16 * K):
            pintar(base, np.ones((3 * K, 9 * K), np.float32), CONCRETO, x, yy * K)
    pintar(base, np.ones((3 * K, (wd - 2 * px_) * K), np.float32), GRAFITE, px_ * K, linha_total * K)
    for m, rgb, x, ymeio, cap, b in els:
        pintar(base, m, rgb, x * K - 2, ymeio * K + cap / 2 - b)
    return base, num, {"w": wd, "h": hd, "cortes": cortes}


def pictograma_cama(lado):
    """pictograma de hospedagem: quadrado grafite radius-tag com cama amarela (grade 48, ícone 36)."""
    q = retangulo(lado, lado, tok("radius.tag")["value"] * K)
    s = lado / 48

    def cama(d, ss):
        f = lambda v: v * s * ss  # noqa: E731
        d.rectangle([f(7), f(14), f(11), f(37)], fill=255)          # cabeceira
        d.rectangle([f(7), f(27), f(41), f(32)], fill=255)          # estrado
        d.rectangle([f(37), f(27), f(41), f(37)], fill=255)         # pé
        d.rounded_rectangle([f(13), f(20), f(21), f(26)], radius=f(2), fill=255)   # travesseiro
        d.rounded_rectangle([f(22), f(19), f(41), f(26)], radius=f(2), fill=255)   # colchão
    return q, forma(lado, lado, cama)


def hospedagem_obj(item):
    """etiqueta de bagagem (DS 2.6): furo de 28 px, cordão grafite, cama, H3, micro, valor, nota de caneta."""
    h3, mi = estilo("h3"), estilo("micro")
    mn, wn, bn, cn = texto(item["nome"], FT["h3"], h3["px"], h3["track"])
    mm, wm, bm, cm = texto(item["micro"], FT["mono"], mi["px"], mi["track"])
    sufixo = "/noite" if item.get("por_noite") else ""
    mv, wv, bv, cv = texto(eurfmt(item["eur"]) + sufixo, FT["placar"], 64, 0, tnum=True)
    mr, wr, br, cr = texto("≈ " + brl(item["eur"]) + sufixo, FT["b500"], 40, 0)
    mc, wc, bc, cc = texto(item["caneta"], FT["caneta"], 72, 0)
    pic = 48
    pl = 40
    inner = max(pic * K + 16 * K + wn, wm, wv, wr, wc) / K
    wd = max(440, pl * 2 + inner)
    y = 110
    rows = []
    rows.append(("pic", y)); rows.append(("h3", y)); y += 56 + 14
    rows.append(("micro", y)); y += 39 + 18
    rows.append(("v", y)); y += 64 + 6
    rows.append(("r", y)); y += 48 + 6
    rows.append(("c", y)); y += 72 + 30
    hd = y
    w, h = int(round(wd * K)), int(round(hd * K))
    corte = 0.12 * hd
    silh = forma(w, h, lambda d, s: d.polygon([(0.22 * w * s, 0), (0.78 * w * s, 0), (w * s, corte * K * s), (w * s, h * s),
                                               (0, h * s), (0, corte * K * s)], fill=255))
    furo_r = 14 * K
    cx, cy = w / 2, 38 * K + furo_r
    furo = forma(w, h, lambda d, s: d.ellipse([(cx - furo_r) * s, (cy - furo_r) * s, (cx + furo_r) * s, (cy + furo_r) * s], fill=255))
    anel = forma(w, h, lambda d, s: d.ellipse([(cx - furo_r - 7 * K) * s, (cy - furo_r - 7 * K) * s,
                                               (cx + furo_r + 7 * K) * s, (cy + furo_r + 7 * K) * s], fill=255))
    obj = tela(h, w)
    pintar(obj, silh, PAPEL, 0, 0)
    fibra(obj, 31, OP_FIBRA)
    pintar(obj, np.clip(anel - furo, 0, 1), CONCRETO, 0, 0)
    obj *= (1 - furo)[..., None]
    q, cama = pictograma_cama(pic * K)
    yy = dict((k, v) for k, v in rows)
    pintar(obj, q, GRAFITE, pl * K, yy["pic"] * K + 4 * K)
    pintar(obj, cama, AMARELO, pl * K, yy["pic"] * K + 4 * K)
    pintar(obj, mn, GRAFITE, (pl + pic + 16) * K - 2, (yy["h3"] + 28) * K + cn / 2 - bn)
    pintar(obj, mm, ASFALTO, pl * K - 2, (yy["micro"] + 19.5) * K + cm / 2 - bm)
    pintar(obj, mv, GRAFITE, pl * K - 2, (yy["v"] + 32) * K + cv / 2 - bv)
    pintar(obj, mr, ASFALTO, pl * K - 2, (yy["r"] + 24) * K + cr / 2 - br)
    pintar(obj, mc, CANETA, pl * K - 2, (yy["c"] + 46) * K - bc)
    return obj, {"w": wd, "h": hd, "furo": (cx, cy)}


def bilhete_obj(linhas):
    """bilhete de humor (DS 2.4 / 3.2): papel, Caneta 72 px, Azul Caneta, máx. 2 linhas × 22 caracteres."""
    ms = [texto(l, FT["caneta"], 72, 0) for l in linhas]
    pv, ph, lh = 24, 32, 72 * 1.05
    wd = 2 * ph + max(m[1] for m in ms) / K
    hd = 2 * pv + lh * len(ms) + 8
    w, h = int(round(wd * K)), int(round(hd * K))
    papel = tela(h, w)
    pintar(papel, retangulo(w, h, tok("radius.paper")["value"] * K), PAPEL, 0, 0)
    fibra(papel, 41, OP_FIBRA)
    tinta = tela(h, w)
    for i, (m, wl, b, c) in enumerate(ms):
        pintar(tinta, m, CANETA, ph * K - 2, (pv + lh * (i + 0.78)) * K - b)
    return papel, tinta, {"w": wd, "h": hd}


# ---------------------------------------------------------------- cor: sRGB → HLG BT.2020 → Y'CbCr 10 bits

M709_2020 = np.array([[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]], np.float32)
HLG_A, HLG_B, HLG_C = 0.17883277, 0.28466892, 0.55991073


def srgb_para_hlg(rgb):
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    lin = lin @ M709_2020.T
    fd = 0.203 * np.clip(lin, 0, None)                          # BT.2408: branco gráfico = 203 cd/m² (de 1000)
    yd = fd @ np.array([0.2627, 0.6780, 0.0593], np.float32)
    es = fd * np.power(np.maximum(yd, 1e-6), -0.2 / 1.2)[..., None]   # OOTF inversa, gama 1,2
    es = np.clip(es, 0, 1)
    return np.where(es <= 1 / 12, np.sqrt(3 * es), HLG_A * np.log(np.maximum(12 * es - HLG_B, 1e-6)) + HLG_C)


def para_yuva16(img):
    """pré-multiplicado sRGB → planos yuva444p16le (Y'CbCr BT.2020 NCL, faixa limitada 10 bits, ×64)."""
    a = img[..., 3]
    rgb = np.where(a[..., None] > 1e-5, img[..., :3] / np.maximum(a[..., None], 1e-5), 0)
    e = srgb_para_hlg(np.clip(rgb, 0, 1))
    y = e @ np.array([0.2627, 0.6780, 0.0593], np.float32)
    cb = (e[..., 2] - y) / 1.8814
    cr = (e[..., 0] - y) / 1.4746
    planos = [64 + 876 * y, 512 + 896 * cb, 512 + 896 * cr, 1023 * np.clip(a, 0, 1)]
    return np.stack([np.clip(np.round(p) * 64, 0, 65535).astype("<u2") for p in planos]).tobytes()


# ---------------------------------------------------------------- linha do tempo

def ler_cortes(arq):
    if arq.endswith(".json"):
        return json.load(open(arq))["cortes_s"]
    return [float(m) for m in re.findall(r"pts_time:([\d.]+)", open(arq).read())]


def planejar(cortes):
    tp = CFG["tempos"]
    itens = []
    vis_tipo = {"lugar": tp["lugar_visivel_s"], "preco": tp["preco_visivel_s"], "recibo": tp["recibo_visivel_s"],
                "hospedagem": tp["hospedagem_visivel_s"], "humor": tp["humor_visivel_s"], "placa": tp["placa_visivel_s"]}
    for it in CFG["itens"]:
        nota = []
        if it["tipo"] == "varredura":
            qc = int(round(it["corte_s"] * FPS))
            itens.append({**it, "t_in": (qc - 4) / FPS, "t_fim": (qc + 5) / FPS, "saida_s": 0, "notas": ["4 quadros antes do corte, 5 depois"]})
            continue
        t_in = seg(it.get("entrada", it["t"]))
        if it["tipo"] == "um":
            itens.append({**it, "t_in": t_in, "t_fim": NQ / FPS, "saida_s": 0, "notas": ["fica até o último quadro"]})
            continue
        vis = it.get("visivel_s", vis_tipo[it["tipo"]])
        saida = 0.2 if it["tipo"] == "humor" else D_BASE / 1000
        t_fim = t_in + vis + saida
        # termina no corte de cena se ele vier depois do mínimo visível (o objeto não atravessa para outra cena),
        # exceto placas (abertura, capítulo, chamada), que têm tempo próprio
        cs = [c for c in cortes if t_in + tp["minimo_visivel_s"] + saida <= c < t_fim - 0.05] if it["tipo"] != "placa" else []
        if it["id"] in ("L01", "L17"):
            cs = []      # cobertura: atravessa o corte dentro do trecho em zoom
        if "fim" in it:
            t_fim, cs = seg(it["fim"]), []
            nota.append("fim definido na configuração")
        if cs:
            t_fim = cs[0]
            nota.append(f"encerra no corte de cena {tc(cs[0])}")
        itens.append({**it, "t_in": t_in, "t_fim": t_fim, "saida_s": saida, "notas": nota})
    for lg in CFG.get("legendas_reforco", {}).get("itens", []):
        itens.append({**lg, "tipo": "legenda", "t": tc(lg["eventos"][0]["i"]), "t_in": lg["eventos"][0]["i"],
                      "t_fim": lg["eventos"][-1]["f"], "saida_s": 0.12, "notas": []})
    itens.sort(key=lambda i: i["t_in"])
    zona = {"lugar": "esq", "hospedagem": "esq", "recibo": "dir", "humor": "topo", "legenda": "base", "placa": "topo_esq",
            "varredura": "tela", "um": "topo_esq"}
    for i, a in enumerate(itens):
        for b in itens[i + 1:]:
            if "fim" not in a and zona[b["tipo"]] == zona[a["tipo"]] and b["t_in"] < a["t_fim"] + 0.3 and a["tipo"] not in ("varredura", "um"):
                novo = b["t_in"] - 0.3
                if novo - a["t_in"] >= tp["minimo_visivel_s"]:
                    a["notas"].append(f"encurtado para sair antes de {b['id']}")
                    a["t_fim"] = novo
    marca = [x for x in itens if x["tipo"] != "legenda"]
    for a, b in zip(marca, marca[1:]):
        dt = b["t_in"] - a["t_in"]
        if dt < tp["calma_entre_entradas_s"] and not (a["tipo"] == "varredura" and b["tipo"] == "placa"):
            b["notas"].append(f"ALERTA: entra {dt:.2f} s depois de {a['id']} (calma do DS: 1,5 s)")
    for a in marca:   # sobreposição na tela (mesma zona)
        for b in marca:
            if a is not b and a["t_in"] < b["t_in"] < a["t_fim"] and zona[a["tipo"]] == zona[b["tipo"]]:
                b["notas"].append(f"ALERTA: entra com {a['id']} ainda na mesma zona")
    for it in itens:
        it["q_in"] = int(round(it["t_in"] * FPS))
        it["q_fim"] = min(int(round(it["t_fim"] * FPS)), NQ)
        it["visivel_s"] = round((it["q_fim"] - it["q_in"]) / FPS, 3)
    return itens


# ---------------------------------------------------------------- quadros de cada item

MARG_PLACA = 56   # folga para a sombra shadow-plate (18 px + 32 px de desfoque)


def quadros_lugar(it):
    base, info = lugar_obj(it["nome"], it["micro"])
    x_fin, marg = 96, MARG_PLACA
    hh = base.shape[0] + 2 * marg * K
    sx, sy = info["seta_xy"]
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - D_BASE
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        if t < 320:   # Chegada curta: passa +24 px do ponto em 160 ms, assenta em 230 ms, a seta empurra 10 px
            dx = kf([(0, -(x_fin + info["w"] + marg + 40)), (160, 24), (230, 0)], t)
            empurra = 10 * math.sin(math.pi * min(max((t - 230) / 90, 0), 1))
            borrao = 12 * max(0, 1 - t / 160)
        elif t < t_saida:
            dx, empurra, borrao = 0, 0, 0
        else:         # saída 240 ms: a seta empurra (80 ms) e a placa sai pela direita com ease-exit e desfoque
            ts = t - t_saida
            empurra = 10 * math.sin(math.pi * ts / 80) if ts < 80 else 0
            p = min(max((ts - 80) / 160, 0), 1)
            dx = E_EXIT(p) * (1920 - x_fin + marg)
            borrao = 12 * p
        chave = (round(dx * K), round(empurra * K), int(round(borrao * K)))
        if chave not in cache:
            o = base.copy()
            pintar(o, info["seta"], AMARELO, sx + chave[1], sy)
            c = com_sombra(o, "plate", marg)
            if chave[2] >= 2:
                c = caixa_borrada(c, chave[2] // 2, 1)
            q = tela(hh, W)
            sobre(q, c, (x_fin - marg) * K + chave[0], 0)
            cache = {chave: q}
        yield cache[chave]


def x_direita(w):
    """lado direito (DS 5.4: preço em x 1400); se não couber, encosta na margem de título (x 1824)."""
    return min(1400, 1920 - 96 - w)


def quadros_preco(it):
    base, num, info = etiqueta_obj(it["rotulo"], it["eur"])
    marg = 40
    x0 = x_direita(info["w"])
    y0 = 960 - info["h"]
    largura = int((info["w"] + 2 * marg + 140 + 140) * K)
    caixa_x = int((x0 - marg - 140) * K)
    hh = int((info["h"] + 2 * marg) * K)
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - D_BASE
    pronto = None
    for k in range(n):
        t = k * 1000 / FPS
        if t < D_FAST:
            dx, op = kf([(0, -140), (D_FAST, 0)], t), kf([(0, 0.0), (D_FAST, 1.0)], t)
        elif t < t_saida:
            dx, op = 0, 1
        else:
            p = E_EXIT((t - t_saida) / D_BASE)
            dx, op = 120 * p, 1 - p
        giro = min(max((t - D_FAST) / D_BASE, 0), 1)       # o número gira até o valor (240 ms) depois de entrar
        if giro >= 1 and pronto is not None and t_saida > t >= D_FAST:
            o = pronto
        else:
            o = base.copy()
            m = num["m"]
            dy = (1 - E_OUT(giro)) * (num["clip"][1] - num["clip"][0])
            camada = tela(o.shape[0], o.shape[1])
            pintar(camada, m, GRAFITE, num["x"], num["y"] + dy)
            camada[:num["clip"][0]] = 0
            camada[num["clip"][1]:] = 0
            sobre(o, camada, 0, 0)
            o = com_sombra(o, "paper", marg)
            if giro >= 1:
                pronto = o
        q = tela(hh, largura)
        sobre(q, o * op, (140 + dx) * K, 0)
        yield q


def caixa_preco(it):
    base, num, info = etiqueta_obj(it["rotulo"], it["eur"])
    marg = 40
    x0 = x_direita(info["w"])
    y0 = 960 - info["h"]
    return (int((x0 - marg - 140) * K), int((y0 - marg) * K), int((info["w"] + 2 * marg + 280) * K), int((info["h"] + 2 * marg) * K))


RECIBO_MARG, RECIBO_FOLGA = 40, 160


def recibo_pos(it, info):
    """DS 5.4: recibo à direita, borda direita na margem de título (x 1824 = 1920 − 96), base y 960 (a mesma do lower
    third). Exceção por item ("lado": "esq") para cobrir gráfico antigo ou não cobrir rosto: x 96."""
    x0 = 96 if it.get("lado") == "esq" else 1920 - 96 - info["w"]
    y0 = it.get("base_y", 960) - info["h"]
    return x0, y0


def quadros_recibo(it):
    """entrada 'imprimir' (padrão): o papel sai impresso de cima para baixo (máscara 320 ms) enquanto encosta vindo da
    direita (40 px, ease-out); 'deslizar': inteiro, desliza 140 px em 160 ms (cobertura). Depois o total gira (240 ms).
    Saída: 240 ms para a direita com ease-exit."""
    base, num, info = recibo_obj(it)
    marg, folga = RECIBO_MARG, RECIBO_FOLGA
    hh = base.shape[0] + 2 * marg * K
    largura = base.shape[1] + 2 * (marg + folga) * K
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - D_BASE
    imp = 320
    deslizar = it.get("entrada_tipo") == "deslizar"
    sentido = 1 if it.get("lado") == "esq" else -1           # de onde vem: esquerda (−) ou direita (+)
    t_giro0 = D_FAST if deslizar else imp
    # impressão em 2 etapas quando uma linha tem tempo próprio (ex.: McDonald's, pedido 2 em 06:38): até a 1ª linha,
    # depois o resto (linha 2 + total) a partir desse tempo
    t2 = next(((seg(ln["t"]) - it["t_in"]) * 1000 for ln in it["linhas"][1:] if "t" in ln), None)
    corte1 = int(info["cortes"][0] * K) if t2 is not None else None
    if t2 is not None:
        t_giro0 = t2 + imp
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        if deslizar:
            p = E_OUT(min(t / D_FAST, 1))
            limite, dx, op = base.shape[0], -sentido * 140 * (1 - p), p
        elif t2 is not None:
            p = E_OUT(min(t / imp, 1))
            dx, op = -sentido * 40 * (1 - p), 1.0
            limite = int(corte1 * p) if t < t2 else corte1 + int((base.shape[0] - corte1) * E_OUT(min((t - t2) / imp, 1)))
        else:
            p = E_OUT(min(t / imp, 1))
            limite, dx, op = int(base.shape[0] * p), -sentido * 40 * (1 - p), 1.0
        giro = min(max((t - t_giro0) / D_BASE, 0), 1)
        if t >= t_saida:
            ps = E_EXIT(min((t - t_saida) / D_BASE, 1))
            dx, op = 120 * ps, 1 - ps
        chave = (limite, round(dx, 1), round(op, 3), round(giro, 3))
        if chave not in cache:
            o = base.copy()
            camada = tela(o.shape[0], o.shape[1])
            pintar(camada, num["m"], GRAFITE, num["x"], num["y"] + (1 - E_OUT(giro)) * (num["clip"][1] - num["clip"][0]))
            camada[:num["clip"][0]] = 0
            camada[num["clip"][1]:] = 0
            sobre(o, camada, 0, 0)
            o[limite:] = 0
            o = com_sombra(o, "paper", marg)
            q = tela(hh, largura)
            sobre(q, o * op, (folga + dx) * K, 0)
            cache = {chave: q}
        yield cache[chave]


def caixa_recibo(it):
    base, num, info = recibo_obj(it)
    x0, y0 = recibo_pos(it, info)
    marg, folga = RECIBO_MARG, RECIBO_FOLGA
    return (int((x0 - marg - folga) * K), int((y0 - marg) * K), base.shape[1] + 2 * (marg + folga) * K, base.shape[0] + 2 * marg * K)


CORDAO = 150


def quadros_hospedagem(it):
    obj, info = hospedagem_obj(it)
    marg = 60
    ow, oh = obj.shape[1], obj.shape[0]
    # tela de trabalho: objeto + cordão acima, com folga para girar em torno do topo do cordão
    pad = int(0.35 * oh)
    tw, th = ow + 2 * pad, oh + CORDAO * K + pad
    piv = (tw / 2, 0)
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - D_BASE
    rot_rep = tok("rotation.rot-tag")
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        if t < 480:
            ang = kf([(0, 8.0), (260, -6.0), (480, rot_rep)], t)      # 8° → −3° com 1 oscilação (480 ms)
            op = min(t / 120, 1)
        else:
            ang, op = rot_rep, 1
        sai = E_EXIT((t - t_saida) / D_BASE) if t >= t_saida else 0
        chave = (round(ang, 2), round(op, 2), round(sai, 3))
        if chave not in cache:
            base = tela(th, tw)
            sobre(base, obj, pad, CORDAO * K)
            cx, cy = info["furo"]
            pintar(base, np.ones((int(CORDAO * K + cy), 4 * K), np.float32), GRAFITE, tw / 2 - 2 * K, 0)
            g = girar(base, ang, piv)
            g = com_sombra(g, "paper", marg)
            q = tela(g.shape[0], g.shape[1] + 200 * K)
            sobre(q, g * op * (1 - sai), 160 * sai * K, 0)
            cache = {chave: q}
        yield cache[chave], sai


def caixa_hospedagem(it):
    obj, info = hospedagem_obj(it)
    marg = 60
    pad = int(0.35 * obj.shape[0])
    tw, th = obj.shape[1] + 2 * pad, obj.shape[0] + CORDAO * K + pad
    x = 96 * K - pad - marg * K
    y_obj_base = 960 * K
    y = y_obj_base - obj.shape[0] - CORDAO * K - marg * K
    return (x, y, tw + 2 * marg * K + 200 * K, th + 2 * marg * K)


def quadros_humor(it):
    papel, tinta, info = bilhete_obj(it["linhas"])
    marg = 40
    w, h = papel.shape[1], papel.shape[0]
    pad = int(0.12 * w)
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - 200
    rot = tok("rotation.rot-note")
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        if t < D_BASE:
            p = E_ARR(t / D_BASE)
            dy, ang, op = 24 * (1 - p), rot * p, min(t / D_BASE * 1.5, 1)
        else:
            dy, ang, op = 0, rot, 1
        rev = min(max((t - D_BASE) / D_SLOW, 0), 1)                 # a letra aparece da esquerda para a direita
        if t >= t_saida:
            p = E_EXIT((t - t_saida) / 200)
            dy, op = 40 * p, 1 - p
        chave = (round(dy, 1), round(ang, 2), round(op, 2), round(rev, 3))
        if chave not in cache:
            o = tela(h + 2 * pad, w + 2 * pad)
            sobre(o, papel, pad, pad)
            ti = tinta.copy()
            ti[:, int(w * rev):] = 0
            sobre(o, ti, pad, pad)
            o = girar(o, ang, ((w + 2 * pad) / 2, (h + 2 * pad) / 2))
            o = com_sombra(o, "paper", marg) * op
            q = tela(o.shape[0] + 50 * K, o.shape[1])
            sobre(q, o, 0, dy * K)
            cache = {chave: q}
        yield cache[chave]


def caixa_humor(it):
    papel, tinta, info = bilhete_obj(it["linhas"])
    marg = 40
    w, h = papel.shape[1], papel.shape[0]
    pad = int(0.12 * w)
    x, y = it["posicao"]
    return (x * K - pad - marg * K, y * K - pad - marg * K, w + 2 * pad + 2 * marg * K, h + 2 * pad + 2 * marg * K + 50 * K)


# ---------------------------------------------------------------- REV2: placa esmaltada, Varredura, símbolo 1º

from scipy import ndimage  # noqa: E402

PLACA = {   # DS 2.1 (anatomia) e bundle .pd-plate; mesmos valores do rev8.json do Reel de apresentação
    "pad_v": 28, "pad_h": 36, "filete_inset": 10, "filete_px": 2, "filete_alfa": 0.25, "filete_raio": 8,
    "rebite_px": 10, "rebite_x": 22, "rebite_y": 22, "rebite_alfa": 0.35, "bevel_luz": (2, 0.45), "bevel_sombra": (4, 0.16),
    "sombra_dura": (3, 0.28), "sombra_proj": {"y": 18, "blur": 32, "spread": -10, "alfa": 0.55},
    "brilho_ms": (700, 1300), "brilho_alfa": 0.4, "brilho_largura": 0.34, "brilho_incl": -14,
}
SS2 = 2   # superamostragem das máscaras da placa


def _mask(w, h, desenho):
    im = Image.new("L", (int(w * SS2), int(h * SS2)), 0)
    desenho(ImageDraw.Draw(im), SS2)
    a = np.asarray(im, np.float32) / 255
    return a.reshape(int(h), SS2, int(w), SS2).mean((1, 3))


def _premult(rgb, a):
    return np.dstack([rgb * a[..., None], a]).astype(np.float32)


def _desl(a, dy=0.0, dx=0.0):
    return ndimage.shift(a, (dy, dx) + (0,) * (a.ndim - 2), order=1, mode="constant", cval=0)


def _ruido_esmalte(h, w, semente):
    rng = np.random.default_rng(semente)
    n = ndimage.gaussian_filter(rng.standard_normal((h, w)), 0.8 * K) + 0.5 * ndimage.gaussian_filter(rng.standard_normal((h, w)), 2.0 * K)
    return ((n - n.min()) / (n.max() - n.min())).astype(np.float32)


VARIANTES = {
    # linha: (arquivo da fonte, px, tracking em em, entrelinha, margem acima)
    "abertura": {"linhas": [("label", "BarlowCondensed-SemiBold.ttf", 36, 0.08, 1.0, 0), ("dest", "BarlowCondensed-ExtraBold.ttf", 128, 0.005, 0.9, 12),
                            ("micro", "IBMPlexMono-Medium.ttf", 30, 0.04, 1.3, 14)], "seta": 96},
    "capitulo": {"linhas": [("dest", "BarlowCondensed-ExtraBold.ttf", 104, 0.005, 0.9, 0)], "seta": 96},
    "cta": {"linhas": [("label", "BarlowCondensed-SemiBold.ttf", 28, 0.08, 1.0, 0), ("dest", "BarlowCondensed-ExtraBold.ttf", 96, 0.005, 0.9, 10)], "seta": 72},
}


def placa_pecas(it):
    """face amarela esmaltada (relevo, filete, rebites, grão 5%, texto grafite) + módulo de seta grafite, em px de 4K."""
    var = VARIANTES[it["variante"]]
    P = PLACA
    textos = {"label": it.get("linha1", ""), "dest": it.get("linha2", ""), "micro": it.get("linha3", "")}
    linhas = [(textos[n], f, px, tr, lh, mt) for n, f, px, tr, lh, mt in var["linhas"] if textos[n]]
    larg = 0
    for t, f, px, tr, lh, mt in linhas:
        ft = ImageFont.truetype(os.path.join(ARGS_FONTES, f), int(px * K))
        larg = max(larg, sum(ft.getlength(c) for c in t) + tr * px * K * (len(t) - 1))
    hh_d = 2 * P["pad_v"] + sum(px * lh + mt for t, f, px, tr, lh, mt in linhas)
    fw_d = 2 * P["pad_h"] + larg / K
    fw, hh = int(round(fw_d * K)), int(round(hh_d * K))
    r = tok("radius.plate")["value"] * K
    m = _mask(fw, hh, lambda d, s: d.rounded_rectangle([0, 0, fw * s - 1, hh * s - 1], radius=r * s, fill=255, corners=(True, False, False, True)))
    i_, rr, lw = P["filete_inset"] * K, P["filete_raio"] * K, P["filete_px"] * K

    def filete(d, s):
        I, R, L = i_ * s, rr * s, lw * s
        d.line([(fw * s - I, I + L / 2), (I + R, I + L / 2)], fill=255, width=int(L))
        d.line([(fw * s - I, hh * s - I - L / 2), (I + R, hh * s - I - L / 2)], fill=255, width=int(L))
        d.line([(I + L / 2, I + R), (I + L / 2, hh * s - I - R)], fill=255, width=int(L))
        d.arc([I, I, I + 2 * R, I + 2 * R], 180, 270, fill=255, width=int(L))
        d.arc([I, hh * s - I - 2 * R, I + 2 * R, hh * s - I], 90, 180, fill=255, width=int(L))
    fil = _mask(fw, hh, filete)

    def escrever(d, s):
        y = P["pad_v"] * K * s
        for t, f, px, tr, lh, mt in linhas:
            ft = ImageFont.truetype(os.path.join(ARGS_FONTES, f), int(px * K * s))
            y += mt * K * s
            cap = -ft.getbbox("H", anchor="ls")[1]
            base_y = y + (px * lh * K * s + cap) / 2
            x = P["pad_h"] * K * s
            for c in t:
                d.text((x, base_y), c, font=ft, fill=255, anchor="ls")
                x += ft.getlength(c) + tr * px * K * s
            y += px * lh * K * s
    txt = _mask(fw, hh, escrever)
    rb, rx, ry = P["rebite_px"] * K, P["rebite_x"] * K, P["rebite_y"] * K
    reb = _mask(fw, hh, lambda d, s: [d.ellipse([rx * s, yy * s, (rx + rb) * s, (yy + rb) * s], fill=255) for yy in (ry, hh - ry - rb)])
    luz = _mask(fw, hh, lambda d, s: [d.ellipse([(rx + rb * .22) * s, (yy + rb * .18) * s, (rx + rb * .52) * s, (yy + rb * .48) * s], fill=255)
                                      for yy in (ry, hh - ry - rb)])
    rgb = np.broadcast_to(AMARELO, m.shape + (3,)).copy()
    rgb *= (1 - OP_GRAO * _ruido_esmalte(hh, fw, 7))[..., None]
    bl, ba = P["bevel_luz"]
    bs, bsa = P["bevel_sombra"]
    topo = np.clip(m - _desl(m, bl * K), 0, 1) * ba
    baixo = np.clip(m - _desl(m, -bs * K), 0, 1) * bsa
    rgb = rgb * (1 - topo[..., None]) + topo[..., None]
    rgb = rgb * (1 - baixo[..., None])
    for camada, cor_, a in ((fil, GRAFITE, P["filete_alfa"]), (reb, GRAFITE, P["rebite_alfa"])):
        rgb = rgb * (1 - (camada * a)[..., None]) + cor_ * (camada * a)[..., None]
    rgb = rgb * (1 - (np.clip(reb - _desl(reb, -1.5 * K), 0, 1) * 0.35)[..., None])
    rgb = rgb * (1 - (luz * 0.4)[..., None]) + (luz * 0.4)[..., None]
    rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
    face = _premult(rgb, m)
    lado = hh                                    # DS 2.1: módulo com lado = altura do conteúdo
    modulo = modulo_grafite(lado, hh, (False, True, True, False), "seta", var["seta"])
    return face, modulo, {"fw": fw, "hh": hh, "lado": lado, "w_design": (fw + lado) / K, "h_design": hh / K}


def modulo_grafite(lado, hh, cantos, icone, tam_icone_px, fase=1.0, op_num=1.0):
    """módulo grafite (filete claro 2 px 7% + luz 2 px em cima) com a seta da placa (bundle: M8 41h50V18l38 32-38 32V59H8z)
    ou o símbolo 1º (bundle: '1' papel, sol amarelo, traço amarelo); fase = progresso do Nascer (0 → 1)."""
    r = tok("radius.plate")["value"] * K
    mm = _mask(lado, hh, lambda d, s: d.rounded_rectangle([0, 0, lado * s - 1, hh * s - 1], radius=r * s, fill=255, corners=cantos))
    rgbm = np.broadcast_to(GRAFITE, mm.shape + (3,)).copy()
    borda = np.clip(mm - ndimage.grey_erosion(mm, size=(2 * K + 1, 2 * K + 1)), 0, 1) * 0.07
    topo_m = np.clip(mm - _desl(mm, 2 * K), 0, 1) * 0.08
    for c in (borda, topo_m):
        rgbm = rgbm * (1 - c[..., None]) + c[..., None]
    lado_ic = tam_icone_px * K
    ox, oy = (lado - lado_ic) / 2, (hh - lado_ic) / 2
    k = lado_ic / 100
    if icone == "seta":
        pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
        seta_m = _mask(lado, hh, lambda d, s: d.polygon([((ox + x * k) * s, (oy + y * k) * s) for x, y in pts], fill=255))
        rgbm = rgbm * (1 - seta_m[..., None]) + AMARELO * seta_m[..., None]
    else:
        num = [(26, 4), (48, 4), (48, 100), (26, 100), (26, 30), (12, 37), (12, 16)]
        cy = 38 + 15 + (17 - 53) * E_CIN(fase)        # o sol sobe de trás do traço (y 38) até cy 17
        sol = _mask(lado, hh, lambda d, s: d.ellipse([(ox + 61 * k) * s, (oy + (cy - 15) * k) * s, (ox + 91 * k) * s, (oy + (cy + 15) * k) * s], fill=255))
        sol[int(oy + 38 * k):] = 0                    # recorte: abaixo do horizonte o sol não aparece
        traco = _mask(lado, hh, lambda d, s: d.rectangle([(ox + 58.7 * k) * s, (oy + 38 * k) * s, (ox + 93.2 * k) * s, (oy + 43.5 * k) * s], fill=255))
        um = _mask(lado, hh, lambda d, s: d.polygon([((ox + x * k) * s, (oy + y * k) * s) for x, y in num], fill=255)) * op_num
        for c, cor_ in ((sol, AMARELO), (traco, AMARELO), (um, RECIBO)):
            rgbm = rgbm * (1 - c[..., None]) + cor_ * c[..., None]
    return _premult(rgbm, mm)


E_CIN = bezier(tok("easing.ease-cinema"))

CHEGADA = {   # DS 2.1, assinatura Chegada (560 ms), os mesmos quadros-chave da REV8 (ms)
    "face_x": [(0, None), (267, 24), (345, -4), (400, 0)], "rot": [(0, -3.0), (267, 0.6), (345, -0.15), (400, 0.0)],
    "blur": [(0, 12), (267, 0)], "mod_x": [(0, -1.0), (400, -1.0), (467, 10), (567, 0)],
    "sombra_y": [(0, 40), (400, 18)], "sombra_a": [(0, 0.15), (400, 0.55)], "dura_a": [(0, 0.0), (400, 0.28)],
}
LIN = lambda t: t  # noqa: E731
PLACA_PAD = 90


def placa_pos(it, info):
    if it.get("posicao") == "base":
        return 96, 984 - info["h_design"]          # margem de título embaixo (1080 − 96)
    return 96, 96                                     # DS 5.4: placa de capítulo x 96 · y 96


def _soft_light_branco(b, a):
    d = np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
    return b * (1 - a[..., None]) + d * a[..., None]


def quadros_placa(it):
    face, modulo, info = placa_pecas(it)
    x0, y0 = placa_pos(it, info)
    fw, hh, lado = info["fw"], info["hh"], info["lado"]
    pad = PLACA_PAD * K
    n = it["q_fim"] - it["q_in"]
    t_saida = n / FPS * 1000 - D_BASE
    W_caixa = W - int((x0 - PLACA_PAD) * K)
    chaves = dict(CHEGADA)
    chaves["face_x"] = [(0, -(x0 + info["w_design"] + 60))] + CHEGADA["face_x"][1:]
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        if t < t_saida:
            e = {"dx": kf(chaves["face_x"], t), "rot": kf(chaves["rot"], t), "blur": kf(chaves["blur"], t, LIN),
                 "mx": kf([(a, (v * lado / K if v == -1.0 else v)) for a, v in chaves["mod_x"]], t),
                 "sy": kf(chaves["sombra_y"], t), "sa": kf(chaves["sombra_a"], t), "sda": kf(chaves["dura_a"], t), "br": None}
            b0, b1 = PLACA["brilho_ms"]
            if b0 <= t <= b1:
                e["br"] = round(E_CIN((t - b0) / (b1 - b0)), 2)
        else:                                          # saída 240 ms: a seta empurra (80 ms) e a placa sai pela direita
            ts = t - t_saida
            e = {"dx": kf([(80, 0), (240, 1920 - x0 + 40)], ts, E_EXIT), "rot": 0.0, "blur": kf([(80, 0), (240, 12)], ts, LIN),
                 "mx": kf([(0, 0), (40, 10), (80, 0)], ts), "sy": 18, "sa": 0.55, "sda": 0.28, "br": None}
        chave = tuple(round(v, 1) if isinstance(v, float) else v for v in e.values())
        if chave not in cache:
            c = tela(hh + 2 * pad, fw + lado + 2 * pad)
            mx = e["mx"] * K
            sobre(c, _desl(modulo, 0, mx - math.floor(mx)), pad + fw + math.floor(mx), pad)
            f = face
            if e["br"] is not None:                    # brilho de esmalte (faixa branca 40%, soft-light)
                bw = PLACA["brilho_largura"] * fw
                cx = -bw + (fw + 2 * bw) * e["br"]
                yy, xx = np.mgrid[0:hh, 0:fw].astype(np.float32)
                xs = xx + (yy - hh / 2) * math.tan(math.radians(PLACA["brilho_incl"]))
                perfil = np.clip(1 - np.abs(xs - cx) / (bw / 2), 0, 1) * PLACA["brilho_alfa"]
                a = face[..., 3]
                rgb = np.where(a[..., None] > 0, face[..., :3] / np.maximum(a[..., None], 1e-6), 0)
                f = _premult(_soft_light_branco(rgb, perfil * (a > 0)), a)
            sobre(c, f, pad, pad)
            if abs(e["rot"]) > 1e-3:
                c = np.dstack([ndimage.rotate(c[..., i], -e["rot"], reshape=False, order=1) for i in range(4)])
            if e["blur"] >= 1:
                c = ndimage.uniform_filter1d(c, size=int(round(e["blur"] * K)), axis=1, mode="constant")
            a = c[..., 3]
            sp = PLACA["sombra_proj"]
            s1 = _desl(a, PLACA["sombra_dura"][0] * K) * e["sda"]
            s2 = ndimage.gaussian_filter(_desl(ndimage.grey_erosion(a, size=(2 * 10 * K + 1,) * 2), e["sy"] * K), sp["blur"] * K / 2) * e["sa"]
            sombra = 1 - (1 - s1) * (1 - s2)
            out = _premult(np.zeros(a.shape + (3,), np.float32), sombra)
            sobre(out, c, 0, 0)
            q = tela(out.shape[0], W_caixa)
            sobre(q, out, int(round(e["dx"] * K)), 0)
            cache = {chave: q}
        yield cache[chave]


def caixa_placa(it):
    face, modulo, info = placa_pecas(it)
    x0, y0 = placa_pos(it, info)
    pad = PLACA_PAD * K
    return (int((x0 - PLACA_PAD) * K), int(y0 * K) - pad, W - int((x0 - PLACA_PAD) * K), info["hh"] + 2 * pad)


VARREDURA_MOD = 240   # largura da faixa grafite do módulo na borda dianteira (px da grade 1920)


def quadros_varredura(it):
    """Varredura de Placa (DS 4.4): painel amarelo esmaltado com o módulo de seta na borda dianteira atravessa a tela
    da esquerda para a direita; a cena nova aparece atrás dele. 4 quadros antes do corte e 5 depois (≈ 375 ms);
    desfoque direcional 12 px. O corte nunca aparece: antes dele só a parte da direita (cena velha) fica descoberta,
    depois só a da esquerda (cena nova)."""
    mod = VARREDURA_MOD
    lado_seta = 130
    painel_w, painel_h = 1920 * K, H
    face = np.broadcast_to(AMARELO, (painel_h, painel_w, 3)).copy()
    face *= (1 - OP_GRAO * _ruido_esmalte(painel_h // 4, painel_w // 4, 9).repeat(4, 0).repeat(4, 1))[..., None]
    face = _premult(face, np.ones((painel_h, painel_w), np.float32))
    modulo = modulo_grafite(mod * K, painel_h, (False, False, False, False), "seta", lado_seta)
    sombra_borda = np.clip(1 - np.arange(48 * K) / (48 * K), 0, 1) ** 2 * 0.45
    v = (1920 + mod - 120) / 180                         # px por ms: cobre a tela inteira no quadro do corte
    q_corte = int(round(it["corte_s"] * FPS))
    for q in range(it["q_in"], it["q_fim"]):
        tau = (q - q_corte) * 1000 / FPS                  # ms em relação ao primeiro quadro da cena nova
        borda = (1920 + mod - 120) + tau * v              # borda dianteira (px da grade)
        out = tela(H, W)
        xm = int(round((borda - mod) * K))
        xf = xm - painel_w
        sobre(out, face, xf, 0)
        sobre(out, modulo, xm, 0)
        sb = sombra_borda[None, :, None] * np.ones((H, 1, 1), np.float32)
        sobre(out, _premult(np.zeros((H, sb.shape[1], 3), np.float32), sb[..., 0]), int(round(borda * K)), 0)
        sobre(out, _premult(np.zeros((H, sb.shape[1], 3), np.float32), sb[:, ::-1, 0]), xf - sb.shape[1], 0)
        out = ndimage.uniform_filter1d(out, size=12 * K, axis=1, mode="constant")
        yield out


def quadros_um(it):
    """símbolo 1º (DS 0.2.3, ativo nº 4) no módulo grafite de 176 px (kit: PD_placa_modulo_1.png), x 96 · y 96:
    o módulo acende (160 ms) e o sol nasce atrás do traço (Nascer, 700 ms, ease-cinema); o '1' aparece ao lado."""
    lado = 176 * K
    marg = 60
    n = it["q_fim"] - it["q_in"]
    cache = {}
    for k in range(n):
        t = k * 1000 / FPS
        op = E_OUT(min(t / D_FAST, 1))
        fase = min(max((t - 120) / 700, 0), 1)
        op_num = min(max((t - 470) / 350, 0), 1)
        chave = (round(op, 3), round(fase, 3), round(op_num, 3))
        if chave not in cache:
            m = modulo_grafite(lado, lado, (True, True, True, True), "um", 176 * 0.70, fase=fase, op_num=op_num)
            c = com_sombra(m, "plate", marg)
            cache = {chave: c * op}
        yield cache[chave]


def caixa_um(it):
    return (int((96 - 60) * K), int((96 - 60) * K), (176 + 120) * K, (176 + 120) * K)


LG_Y0, LG_Y1 = 730, 1080   # scrim: 0% em y 730 → 63% em y 1080 (layout.yt.scrim-top-y)


def legenda_camadas(linhas):
    """texto da legenda Padrão YouTube: Barlow 700 56 px, caption-text, centro x 960, base do bloco y 984,
    sombra de texto da 3.1 (0 2px 0 35% + 0 0 24px 45%). Devolve (imagem pré-multiplicada da faixa, sem scrim)."""
    cap = estilo("caption")
    lh = cap["px"] * cap["lh"]
    h = int((LG_Y1 - LG_Y0) * K)
    txt = tela(h, W)
    base_bloco = (tok("layout.yt.caption-base-y")["value"] - LG_Y0) * K
    cx = tok("layout.yt.caption-center-x")["value"] * K
    alfa = np.zeros((h, W), np.float32)
    for n, l in enumerate(reversed(linhas)):
        m, w, b, c = texto(l, FT["b700"], cap["px"], cap["track"])
        assert w <= tok("layout.yt.caption-max-width")["value"] * K, l
        y_base_linha = base_bloco - n * lh * K - (lh - cap["px"]) / 2 * K - 0.22 * cap["px"] * K
        x = cx - w / 2 - 2
        y = y_base_linha - b
        tmp = np.zeros((h, W), np.float32)
        hh, ww = m.shape
        y0, x0 = int(round(y)), int(round(x))
        tmp[max(y0, 0):y0 + hh, x0:x0 + ww] = m[max(-y0, 0):h - y0, :]
        alfa = np.maximum(alfa, tmp)
    sombra = np.zeros_like(alfa)
    s1 = deslocar(alfa, 2 * K) * 0.35
    s2 = gauss(alfa, 12 * K) * 0.45 * 1.6
    sombra = np.clip(np.maximum(s1, s2), 0, 0.8)
    pintar(txt, sombra, PRETO, 0, 0)
    pintar(txt, alfa, RECIBO, 0, 0)
    return txt


def scrim_faixa():
    h = int((LG_Y1 - LG_Y0) * K)
    g = np.linspace(0, tok("opacity.op-scrim"), h, dtype=np.float32)[:, None] * np.ones((1, W), np.float32)
    sc = tela(h, W)
    pintar(sc, g, GRAFITE, 0, 0)
    return sc


def quadros_legenda(it):
    """Padrão YouTube (DS 3.4.2): grupo inteiro entra 120 ms (0 → 1 e sobe 10 px), sai 120 ms (1 → 0 e sobe 6 px);
    o scrim entra e sai com a legenda e fica entre eventos seguidos."""
    sc = scrim_faixa()
    camadas = [legenda_camadas(e["linhas"]) for e in it["eventos"]]
    n = it["q_fim"] - it["q_in"]
    t0 = it["q_in"] / FPS
    h = sc.shape[0]
    cache = {}
    for k in range(n):
        t = t0 + k / FPS
        q = tela(h, W)
        # scrim do grupo
        a_ini, a_fim = it["eventos"][0]["i"], it["eventos"][-1]["f"]
        op_s = min(min((t - a_ini) / 0.12, 1), min((a_fim - t) / 0.12, 1))
        op_s = max(op_s, 0)
        txt_op, dy, idx = 0.0, 0.0, None
        for j, e in enumerate(it["eventos"]):
            if e["i"] <= t < e["f"]:
                idx = j
                if t - e["i"] < 0.12:
                    p = E_OUT((t - e["i"]) / 0.12)
                    txt_op, dy = p, 10 * (1 - p)
                elif e["f"] - t < 0.12:
                    p = 1 - (e["f"] - t) / 0.12
                    txt_op, dy = 1 - p, -6 * p
                else:
                    txt_op, dy = 1.0, 0.0
        chave = (round(op_s, 3), idx, round(txt_op, 3), round(dy, 1))
        if chave not in cache:
            sobre(q, sc * op_s, 0, 0)
            if idx is not None and txt_op > 0:
                sobre(q, camadas[idx] * txt_op, 0, dy * K)
            cache = {chave: q}
        yield cache[chave]


# ---------------------------------------------------------------- sprites (FFV1 com alfa)

def caixa_item(it):
    if it["tipo"] == "lugar":
        obj, info = lugar_obj(it["nome"], it["micro"])
        marg = MARG_PLACA
        return (0, int(960 * K - obj.shape[0] - marg * K), W, obj.shape[0] + 2 * marg * K)
    if it["tipo"] == "legenda":
        return (0, int(LG_Y0 * K), W, int((LG_Y1 - LG_Y0) * K))
    if it["tipo"] == "varredura":
        return (0, 0, W, H)
    return {"preco": caixa_preco, "recibo": caixa_recibo, "hospedagem": caixa_hospedagem, "humor": caixa_humor,
            "placa": caixa_placa, "um": caixa_um}[it["tipo"]](it)


def gerar_quadros(it):
    if it["tipo"] == "lugar":
        yield from quadros_lugar(it)
    elif it["tipo"] == "preco":
        yield from quadros_preco(it)
    elif it["tipo"] == "recibo":
        yield from quadros_recibo(it)
    elif it["tipo"] == "humor":
        yield from quadros_humor(it)
    elif it["tipo"] == "legenda":
        yield from quadros_legenda(it)
    elif it["tipo"] == "hospedagem":
        for q, _ in quadros_hospedagem(it):
            yield q
    elif it["tipo"] == "placa":
        yield from quadros_placa(it)
    elif it["tipo"] == "varredura":
        yield from quadros_varredura(it)
    elif it["tipo"] == "um":
        yield from quadros_um(it)


def ajustar(q, cw, ch, ox=0, oy=0):
    """recorta o quadro do item para a caixa fixa (ox, oy = parte da caixa que cai fora da tela)."""
    out = tela(ch, cw)
    sobre(out, q[oy:oy + ch, ox:ox + cw], 0, 0)
    return out


def sprite(it):
    os.makedirs(TMP, exist_ok=True)
    arq = os.path.join(TMP, f"sprite_{it['id']}.mkv")
    x, y, cw, ch = (int(v) for v in caixa_item(it))
    ox, oy = max(-x, 0), max(-y, 0)
    x, y = (x + ox) // 2 * 2, (y + oy) // 2 * 2
    cw = (min(cw - ox, W - x)) // 2 * 2
    ch = (min(ch - oy, H - y)) // 2 * 2
    it["caixa"] = [x, y, cw, ch]
    if os.path.exists(arq) and os.path.exists(arq + ".json") and json.load(open(arq + ".json")) == assinatura(it):
        return arq
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuva444p16le", "-s", f"{cw}x{ch}",
                          "-r", str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3", "-pix_fmt", "yuva444p16le", arq],
                         stdin=subprocess.PIPE)
    ultimo, ultimo_b, n = None, None, 0
    for q in gerar_quadros(it):
        if q is not ultimo:
            ultimo, ultimo_b = q, para_yuva16(ajustar(q, cw, ch, ox, oy))
        p.stdin.write(ultimo_b)
        n += 1
    p.stdin.close()
    assert p.wait() == 0
    assert n == it["q_fim"] - it["q_in"], (it["id"], n)
    json.dump(assinatura(it), open(arq + ".json", "w"))
    return arq


def assinatura(it):
    campos = {k: v for k, v in it.items() if not k.startswith("_") and k not in ("notas", "evidencia")}
    return hashlib.sha256(json.dumps(campos, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ---------------------------------------------------------------- composição

TM_SDR = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
          "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv420p")


def zoom_filtros(t0, t1):
    """trechos de cobertura (rev2.json, zoom_cobertura) que tocam [t0, t1): enquadramento mais fechado, ancorado no topo,
    centrado, aplicado de corte a corte. Devolve a cadeia de filtros para o vídeo de base (ou '')."""
    z = CFG["zoom_cobertura"]
    tr = [x for x in z["trechos"] if x["de_s"] < t1 and x["ate_s"] > t0]
    if not tr:
        return ""
    cw = int(W / z["escala"]) // 2 * 2
    ch = int(H / z["escala"]) // 2 * 2
    cx = (W - cw) // 2 // 2 * 2
    cond = "+".join(f"between(t,{(round(x['de_s'] * FPS) - 0.5) / FPS - t0:.4f},{(round(x['ate_s'] * FPS) - 0.5) / FPS - t0:.4f})" for x in tr)
    return (f"split[zb][zz];[zz]crop={cw}:{ch}:{cx}:0,scale={W}:{H}:flags=lanczos,setsar=1[zc];"
            f"[zb][zc]overlay=x=0:y=0:format=yuv420p10:enable='{cond}'")


def grafo(itens, t0, t1=None):
    """overlay em cadeia, no domínio HLG 10 bits; t0 = início do trecho (s). Antes, o zoom de cobertura (se houver)."""
    partes, ant = [], "0:v"
    zf = zoom_filtros(t0, t1 if t1 is not None else t0 + 3600)
    if zf:
        partes.append(f"[0:v]{zf}[vz]")
        ant = "vz"
    for i, it in enumerate(itens, start=1):
        x, y, cw, ch = it["caixa"]
        partes.append(f"[{i}:v]format=yuva420p10le,setpts=PTS-STARTPTS+{(it['q_in'] / FPS - t0):.6f}/TB[s{i}]")
        partes.append(f"[{ant}][s{i}]overlay=x={x}:y={y}:format=yuv420p10:eof_action=pass:repeatlast=0[v{i}]")
        ant = f"v{i}"
    return ";".join(partes), ant


def carregar_plano():
    plano = json.load(open(PLANO, encoding="utf-8"))
    return plano["itens"]


def cmd_plano(a):
    cortes = ler_cortes(a.cortes)
    itens = planejar(cortes)
    os.makedirs(os.path.join(REV, "analise"), exist_ok=True)
    json.dump({"cortes_s": cortes}, open(os.path.join(REV, "analise", "cortes_de_cena.json"), "w"), indent=0)
    json.dump({"itens": itens}, open(PLANO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for it in itens:
        txt = it.get("nome") or it.get("rotulo") or it.get("cabecalho") or " / ".join(it.get("linhas", []))
        if isinstance(txt, list):
            txt = str(txt)
        print(f"{it['id']}  {it['t']}  {tc(it['t_in'])} → {tc(it['t_fim'])}  ({it['visivel_s']:.2f} s)  {txt}  {'; '.join(it['notas'])}")


def cmd_sprites(a):
    itens = carregar_plano()
    sel = set(a.itens.split(",")) if a.itens else None
    for it in itens:
        if sel and it["id"] not in sel:
            continue
        sprite(it)
        print(it["id"], it["caixa"], flush=True)
    json.dump({"itens": itens}, open(PLANO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def cmd_previa(a):
    """trechos editados: original 4K HLG + gráficos → SDR 1280×720 (só para revisão) e quadros de QA em 1920×1080."""
    itens = carregar_plano()
    sel = set(a.itens.split(",")) if a.itens else None
    os.makedirs(QA_DIR, exist_ok=True)
    pv = os.path.join(TMP, "previa")
    os.makedirs(pv, exist_ok=True)
    janelas = []
    for it in itens:
        if sel and it["id"] not in sel:
            continue
        t0, t1 = max(it["q_in"] / FPS - 1.0, 0.0), min(it["q_fim"] / FPS + 1.0, NQ / FPS)
        if janelas and t0 <= janelas[-1][1]:
            janelas[-1][1] = max(janelas[-1][1], t1)
            janelas[-1][2].append(it)
        else:
            janelas.append([t0, t1, [it]])
    for t0, t1, its in janelas:
        viz = [i for i in itens if i["q_in"] / FPS < t1 and i["q_fim"] / FPS > t0]
        for i in viz:
            sprite(i)
        nome = "_".join(i["id"] for i in its)
        saida = os.path.join(pv, f"previa_{nome}.mp4")
        if os.path.exists(saida) and all(os.path.exists(os.path.join(QA_DIR, f"{i['id']}_saida.jpg")) for i in its) and not a.refazer:
            continue
        g, ult = grafo(viz, t0, t1)
        g = (g + ";" if g else "") + f"[{ult}]zscale=w=1920:h=1080:f=spline36,{TM_SDR},split[q][p];[p]scale=1280:720[pp]"
        ins = ["-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", ORIGINAL]
        for i in viz:
            ins += ["-i", os.path.join(TMP, f"sprite_{i['id']}.mkv")]
        qa = os.path.join(pv, f"qa_{nome}.mkv")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", g,
                        "-map", "[q]", "-c:v", "libx264", "-crf", "10", "-preset", "ultrafast", qa,
                        "-map", "[pp]", "-map", "0:a?", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                        "-c:a", "aac", "-b:a", "128k", saida], check=True)
        for i in its:   # quadros de QA: meio da entrada, assentado, perto do fim, meio da saída (1920×1080 SDR)
            rel = i["q_in"] / FPS - t0
            fim = i["q_fim"] / FPS - t0
            for rot, ts in (("entrada", rel + 0.12), ("assentado", rel + 1.2), ("final", fim - 0.6), ("saida", fim - 0.1)):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", qa, "-frames:v", "1", "-q:v", "2",
                                os.path.join(QA_DIR, f"{i['id']}_{rot}.jpg")], check=True)
        os.remove(qa)
        print(nome, flush=True)


X265 = ("crf=18:vbv-maxrate=45000:vbv-bufsize=90000:keyint=48:min-keyint=24:colorprim=bt2020:transfer=arib-std-b67:"
        "colormatrix=bt2020nc:range=limited:log-level=error")
BLOCOS = os.path.join(TMP, "blocos")


def plano_blocos(itens, alvo_s=60):
    """divide o vídeo em blocos de ~1 min com fronteira num quadro sem nenhum gráfico na tela (±1 s)."""
    ocupado = np.zeros(NQ + 1, bool)
    for i in [x for x in itens if x["tipo"] != "legenda"]:
        ocupado[max(i["q_in"] - FPS, 0):min(i["q_fim"] + FPS, NQ)] = True
    fronteiras, q = [0], 0
    while q + alvo_s * FPS < NQ - 30 * FPS:
        c = q + alvo_s * FPS
        while ocupado[c]:
            c += 1
        fronteiras.append(c)
        q = c
    fronteiras.append(NQ)
    return list(zip(fronteiras, fronteiras[1:]))


def contar_quadros(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-count_packets", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", arq], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def cmd_final(a):
    """vídeo 4K HLG em blocos retomáveis (x265, mesmos parâmetros em todos) → concatenação sem recodificar + áudio."""
    itens = carregar_plano()
    for i in itens:
        sprite(i)
    os.makedirs(BLOCOS, exist_ok=True)
    blocos = plano_blocos(itens)
    lista = []
    for n, (q0, q1) in enumerate(blocos, 1):
        arq = os.path.join(BLOCOS, f"bloco_{n:03d}.mp4")
        lista.append(arq)
        if os.path.exists(arq) and contar_quadros(arq) == q1 - q0:
            continue
        t0 = q0 / FPS
        viz = [i for i in itens if i["q_in"] < q1 and i["q_fim"] > q0]
        assert all(q0 <= i["q_in"] and i["q_fim"] <= q1 for i in viz), "fronteira dentro de um gráfico"
        ins = ["-ss", f"{t0:.6f}", "-i", ORIGINAL]
        for i in viz:
            ins += ["-i", os.path.join(TMP, f"sprite_{i['id']}.mkv")]
        mapa = ["-map", "0:v"]
        fc = []
        g, ult = grafo(viz, t0, q1 / FPS)
        if g:
            fc, mapa = ["-filter_complex", g], ["-map", f"[{ult}]"]
        tmp = arq + ".parcial.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-stats", "-y", *ins, *fc, *mapa, "-frames:v", str(q1 - q0), "-an",
                        "-c:v", "libx265", "-preset", a.preset, "-pix_fmt", "yuv420p10le", "-x265-params", X265, "-tag:v", "hvc1",
                        "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv",
                        "-map_metadata", "-1", tmp], check=True)
        assert contar_quadros(tmp) == q1 - q0, (arq, contar_quadros(tmp), q1 - q0)
        os.replace(tmp, arq)
        print(f"bloco {n}/{len(blocos)} pronto ({q0}–{q1})", flush=True)
    txt = os.path.join(BLOCOS, "lista.txt")
    open(txt, "w").write("".join(f"file '{os.path.basename(l)}'\n" for l in lista))
    audio = ["-map", "0:a"] if not a.audio else []
    ins = ["-f", "concat", "-safe", "0", "-i", txt]
    if a.audio:
        ins += ["-i", a.audio]
        audio = ["-map", "1:a"]
    saida = os.path.join(REV, a.saida)
    dur = NQ / FPS   # áudio cortado no último quadro do vídeo (sem a vinheta do CapCut), fade de 80 ms
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-map", "0:v", *audio, "-c:v", "copy", "-tag:v", "hvc1",
                    "-af", f"atrim=0:{dur:.6f},afade=t=out:st={dur - 0.08:.6f}:d=0.08,volume=-0.3dB", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-map_metadata", "-1", saida], check=True)
    print("final:", saida, contar_quadros(saida), "quadros", flush=True)


def cmd_remendar(a):
    """recodifica (a partir do ORIGINAL) só os blocos que recebem legenda e monta o novo final: os demais blocos
    são copiados do final anterior (concat com inpoint/outpoint nas fronteiras, que são quadros IDR)."""
    itens = carregar_plano()
    blocos = plano_blocos(itens)
    leg = [i for i in itens if i["tipo"] == "legenda"]
    alvo = sorted({n for n, (q0, q1) in enumerate(blocos, 1) for i in leg if i["q_in"] < q1 and i["q_fim"] > q0})
    os.makedirs(BLOCOS, exist_ok=True)
    antigo = os.path.join(REV, a.anterior)
    for n in alvo:
        q0, q1 = blocos[n - 1]
        arq = os.path.join(BLOCOS, f"bloco_{n:03d}_leg.mp4")
        if os.path.exists(arq) and contar_quadros(arq) == q1 - q0:
            continue
        viz = [i for i in itens if i["q_in"] < q1 and i["q_fim"] > q0]
        for i in viz:
            sprite(i)
        t0 = q0 / FPS
        ins = ["-ss", f"{t0:.6f}", "-i", ORIGINAL]
        for i in viz:
            ins += ["-i", os.path.join(TMP, f"sprite_{i['id']}.mkv")]
        g, ult = grafo(viz, t0)
        tmp = arq + ".parcial.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-stats", "-y", *ins, "-filter_complex", g, "-map", f"[{ult}]",
                        "-frames:v", str(q1 - q0), "-an", "-c:v", "libx265", "-preset", a.preset, "-pix_fmt", "yuv420p10le",
                        "-x265-params", X265, "-tag:v", "hvc1", "-color_primaries", "bt2020", "-color_trc", "arib-std-b67",
                        "-colorspace", "bt2020nc", "-color_range", "tv", "-map_metadata", "-1", tmp], check=True)
        assert contar_quadros(tmp) == q1 - q0
        os.replace(tmp, arq)
        print(f"bloco {n} com legenda pronto", flush=True)
    if a.so_blocos:
        return
    # blocos sem legenda: extraídos do final anterior por contagem de quadros (cada bloco é um encode fechado,
    # então os N pacotes a partir do seu IDR são exatamente os seus quadros); concat de arquivos inteiros
    lista = []
    for n, (q0, q1) in enumerate(blocos, 1):
        if n in alvo:
            lista.append(os.path.join(BLOCOS, f"bloco_{n:03d}_leg.mp4"))
            continue
        arq = os.path.join(BLOCOS, f"bloco_{n:03d}_copia.mp4")
        if not (os.path.exists(arq) and contar_quadros(arq) == q1 - q0):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{q0 / FPS:.6f}", "-i", antigo, "-map", "0:v",
                            "-frames:v", str(q1 - q0), "-c", "copy", "-tag:v", "hvc1", arq], check=True)
            assert contar_quadros(arq) == q1 - q0, (arq, contar_quadros(arq), q1 - q0)
        lista.append(arq)
    if a.so_extrair:
        print("blocos extraídos:", len(lista), flush=True)
        return
    txt = os.path.join(BLOCOS, "lista_remendo.txt")
    open(txt, "w").write("".join(f"file '{l}'\n" for l in lista))
    saida = os.path.join(REV, a.saida)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-i", a.audio,
                    "-map", "0:v", "-map", "1:a", "-c", "copy", "-tag:v", "hvc1", "-map_metadata", "-1", saida], check=True)
    print("final com legendas:", saida, contar_quadros(saida), "quadros", flush=True)


def main():
    global ARGS_FONTES
    ap = argparse.ArgumentParser()
    ap.add_argument("etapa", choices=["plano", "sprites", "previa", "final", "remendar"])
    ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
    ap.add_argument("--cortes")
    ap.add_argument("--itens")
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--preset", default="fast")
    ap.add_argument("--saida", default="barcelona_rev2.mp4")
    ap.add_argument("--anterior", default="barcelona_rev1_sem_legenda.mp4")
    ap.add_argument("--so-blocos", action="store_true")
    ap.add_argument("--so-extrair", action="store_true")
    ap.add_argument("--audio", help="faixa de áudio tratada (.m4a); sem ela, o áudio original é copiado")
    a = ap.parse_args()
    ARGS_FONTES = a.fontes
    {"plano": cmd_plano, "sprites": cmd_sprites, "previa": cmd_previa, "final": cmd_final, "remendar": cmd_remendar}[a.etapa](a)


ARGS_FONTES = ""
if __name__ == "__main__":
    main()
