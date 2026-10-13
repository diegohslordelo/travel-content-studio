"""Reel 'Não compre água em Barcelona', revisão 1: reel_agua_barcelona_rev1.mp4.

Reel 03 do painel (13/10/2026), série Chegar sabendo, Nível A. Material: master de Barcelona, dia 2,
trecho 18:05–18:37 (fala da garrafa e do app de fontes) + print da App Store do app Fonts BCN enviado pelo
Diego. Componentes e valores do Design System REV 2 (2.2.0) e dos tokens; a placa, a legenda Padrão, o scrim
e o grão vêm da REV8 do Reel de apresentação.

Linha do tempo (DS 5.2):
  - gancho   : Placa variante 'Não faça' (NÃO FAÇA ISSO / ÁGUA, módulo ✗ vermelho sobre papel) em x 72 · y 640,
               Chegada no quadro 0; sai pela direita em 240 ms
  - entrega  : 7 planos do master com cortes secos; legenda Padrão no tempo da fala
  - app      : quando o Diego diz o nome do app, corte seco para o print (recorte de foto, DS 2.6) sobre
               grafite: revela da esquerda para a direita em 400 ms e faz zoom sutil 100 → 104% (DS 4.5);
               corte seco de volta no fim de 'a localização das fontes'
  - pico     : Bilhete 'dica: garrafa + / app de fontes.' com a assinatura Escrita (DS 2.4)
  - fecho    : Placa CTA pequena 'SALVA PRA VIAGEM →' (DS 2.7) com Chegada, até o último quadro
  - sempre   : grão 5% e scrim inferior

Uso (de dentro de reels/agua-barcelona/):
  python3 rev1/scripts/rev1.py --fontes PASTA --master CAMINHO_DO_MASTER     render final
  python3 rev1/scripts/rev1.py --fontes PASTA --teste                        só a camada de design, sobre um
                                                                            fundo provisório e sem áudio
O caminho do master também pode vir da variável REEL_MASTER.
Fontes (SIL OFL, Google Fonts): Barlow-Bold.ttf, BarlowCondensed-SemiBold.ttf, BarlowCondensed-ExtraBold.ttf,
ReenieBeanie.ttf (Caneta provisória do DS), em https://raw.githubusercontent.com/google/fonts/main/ofl/…
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

REV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REV, "rev1.json"), encoding="utf-8"))
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
SPF = SR // FPS
MS = 1000 / FPS
TMP = os.path.join(REV, "_tmp")
QA_DIR = os.path.join(REV, "qa_frames")
SS = 4  # supersampling dos objetos
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
T = CFG["tokens"]
SAFE = T["safe"]
FONTES_USADAS = ("Barlow-Bold.ttf", "BarlowCondensed-SemiBold.ttf", "BarlowCondensed-ExtraBold.ttf", "ReenieBeanie.ttf")

# HLG -> SDR Rec.709: a mesma cadeia do render do Reel de apresentação (scripts/render.py), saindo em RGB 16 bits
TONEMAP_RGB = (
    "zscale=w=1080:h=1920:f=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,"
    "format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:param=0.5:peak=4.93:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,eq=saturation=0.88,"
    "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb48le")
SDR_RGB = ("scale=1080:1920:flags=lanczos,"
           "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb48le")


def cor(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO = cor(T["signal_500"])
GRAFITE = cor(T["night_900"])
RECIBO = cor(T["paper_0"])
PAPEL = cor(T["paper_500"])
VERMELHO = cor(T["stamp_500"])
CANETA = cor(T["ink_500"])


def rodar(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def q(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------- curvas e keyframes (iguais à REV8)

def bezier(p):
    x1, y1, x2, y2 = p

    def f(t):
        if t <= 0:
            return 0.0
        if t >= 1:
            return 1.0
        bx = lambda s: 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s ** 2 * x2 + s ** 3  # noqa: E731
        by = lambda s: 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s ** 2 * y2 + s ** 3  # noqa: E731
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if bx(mid) < t else (lo, mid)
        return by((lo + hi) / 2)
    return f


E_OUT = bezier(T["ease_out"])
E_ARR = bezier(T["ease_arrive"])
E_EXIT = bezier(T["ease_exit"])
E_CIN = bezier(T["ease_cinema"])
LIN = lambda t: min(max(t, 0.0), 1.0)  # noqa: E731
E_IN = bezier([0.42, 0.0, 1.0, 1.0])  # 'ease-in' do CSS (saída da legenda)


def kf(chaves, t, curva=E_OUT):
    """valor dos keyframes [(ms, valor), …] no instante t (ms); curva por segmento."""
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- linha do tempo

def planos():
    out, r = [], 0
    for p in CFG["planos"]["lista"]:
        o0, o1 = q(p["origem"][0]), q(p["origem"][1])
        out.append({**p, "o0": o0, "o1": o1, "r0": r, "r1": r + (o1 - o0)})
        r += o1 - o0
    return out


PLANOS = planos()
N = PLANOS[-1]["r1"]


def o2r(t, fim=False):
    """tempo do master (s) → tempo do Reel (s). fim=True aceita o instante final de um plano."""
    meio = 0.5 / FPS  # os limites dos planos são arredondados para o quadro
    for p in PLANOS:
        a, b = p["o0"] / FPS, p["o1"] / FPS
        if a - meio <= t < b or (fim and abs(t - b) < meio):
            return max(t - a, 0.0) + p["r0"] / FPS
    raise ValueError(f"{t} s do master não está em nenhum plano")


def cortes_s():
    return [round(p["r0"] / FPS, 3) for p in PLANOS[1:]]


def tempos_legendas():
    L = CFG["legenda"]
    grupos = CFG["grupos"]["lista"]
    leg = []
    for g in grupos:
        palavras = g["texto"].replace("\n", " ").split()
        assert len(palavras) == len(g["palavras"]), g["texto"]
        ini = o2r(g["palavras"][0])
        fim = o2r(g["fim"], fim=True)
        item = {"texto": g["texto"].replace("\n", " "), "texto_tela": g["texto"], "q0": q(ini),
                "fala_rev": [round(ini, 3), round(fim, 3)],
                "palavras_por_s": round(len(palavras) / max(fim - ini, 1e-3), 2)}
        item["modo"] = g.get("modo") or ("palavra" if item["palavras_por_s"] <= L["palavras_por_s_max_palavra_a_palavra"]
                                         else "grupo")
        if item["modo"] == "palavra":
            item["palavras_q"] = [max(item["q0"], q(o2r(t))) for t in g["palavras"]]
        leg.append(item)
    for i, it in enumerate(leg):
        it["q1"] = leg[i + 1]["q0"] if i + 1 < len(leg) else N
        it["de"], it["ate"] = round(it["q0"] / FPS, 3), round(it["q1"] / FPS, 3)
        if it["modo"] == "palavra":
            assert all(it["q0"] <= x < it["q1"] for x in it["palavras_q"]), it
    return leg


# ---------------------------------------------------------------- utilidades de imagem (iguais à REV8)

def fonte(nome, px, pasta):
    return ImageFont.truetype(os.path.join(pasta, nome), int(round(px)))


def reduzir(a, s=SS):
    h, w = a.shape[0] // s, a.shape[1] // s
    return a[:h * s, :w * s].reshape(h, s, w, s, -1).mean((1, 3))


def mascara(tam, desenho):
    im = Image.new("L", (int(tam[0]), int(tam[1])), 0)
    desenho(ImageDraw.Draw(im))
    return np.asarray(im, np.float32) / 255


def mascara_1x(tam, desenho):
    return reduzir(mascara((tam[0] * SS, tam[1] * SS), desenho)[..., None])[..., 0]


def premult(rgb, a):
    return np.dstack([rgb * a[..., None], a]).astype(np.float32)


def sobre(dst, src, x=0, y=0):
    """src (premultiplicado) sobre dst (premultiplicado), com recorte; posição inteira."""
    h, w = src.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
    if x1 <= x0 or y1 <= y0:
        return dst
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    d *= (1 - s[..., 3:4])
    d += s
    return dst


def deslocar(a, dy=0, dx=0):
    return ndimage.shift(a, (dy, dx) + (0,) * (a.ndim - 2), order=1, mode="constant", cval=0)


def sombra_objeto(alfa, dura, proj):
    """sombra de duas camadas dos tokens: borda dura (y, alfa) + projetada (y, blur, spread, alfa). Preto."""
    s1 = deslocar(alfa, dura[0]) * dura[1]
    a = alfa
    if proj["spread"] < 0:
        a = ndimage.grey_erosion(a, size=(2 * -proj["spread"] + 1,) * 2)
    s2 = ndimage.gaussian_filter(deslocar(a, proj["y"]), proj["blur"] / 2) * proj["alfa"]
    return 1 - (1 - s1) * (1 - s2)


def ruido_fractal(h, w, semente):
    rng = np.random.default_rng(semente)
    n = ndimage.gaussian_filter(rng.standard_normal((h, w)), 0.8) + 0.5 * ndimage.gaussian_filter(
        rng.standard_normal((h, w)), 2.0)
    n = (n - n.min()) / (n.max() - n.min())
    return n.astype(np.float32)


def soft_light_branco(b, a):
    d = np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
    return b * (1 - a[..., None]) + d * a[..., None]


def girar(img, graus_css):
    """rotação no sentido do CSS (positivo = horário), em torno do centro, sem mudar o tamanho."""
    if abs(graus_css) < 1e-3:
        return img
    return np.dstack([ndimage.rotate(img[..., i], -graus_css, reshape=False, order=1) for i in range(img.shape[2])])


def caixa_alfa(a, lim=0.02):
    ys, xs = np.nonzero(a > lim)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None


# ---------------------------------------------------------------- placa (DS 2.1)

def largura_texto(f, txt, trk_px):
    return sum(f.getlength(c) for c in txt) + trk_px * (len(txt) - 1)


def desenhar_texto(d, f, txt, x, base, trk_px):
    for c in txt:
        d.text((x, base), c, font=f, fill=255, anchor="ls")
        x += f.getlength(c) + trk_px


def caminho_seta(lado, frac):
    """seta do bundle do DS (pd-bundle.js, viewBox 100): M8 41h50V18l38 32-38 32V59H8z, em 54% do módulo."""
    k = lado * frac / 100
    o = (lado - lado * frac) / 2
    pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
    return [(o + x * k, o + y * k) for x, y in pts]


def placa_pecas(spec, pasta):
    """Face (esmalte amarelo com 1 ou 2 linhas) e módulo (seta grafite ou ✗ vermelho sobre papel), em 1x.
    Anatomia da DS 2.1 e do pd-bundle (.pd-plate): padding 28 × 36, rótulo label 36 px +8%, destino h1 128 px
    entrelinha 0,9 com 12 px de margem; módulo quadrado com lado = altura da face. 'escala' = variante Pequena."""
    P = CFG["placa"]
    e, S = spec["escala"], SS
    rot, dest = spec["rotulo"], spec["destino"]
    r_px, d_px = P["rotulo_px"] * e * S, P["destino_px"] * e * S
    fd = fonte(P["fonte_destino"], d_px, pasta)
    fr = fonte(P["fonte_rotulo"], r_px, pasta) if rot else None
    trk_d, trk_r = P["destino_tracking_em"] * d_px, P["rotulo_tracking_em"] * r_px
    wd = largura_texto(fd, dest, trk_d)
    wr = largura_texto(fr, rot, trk_r) if rot else 0
    lh_d, lh_r = d_px * P["destino_entrelinha"], r_px * P["rotulo_entrelinha"]
    mg = P["destino_margem_topo"] * e * S
    conteudo = lh_r + mg + lh_d if rot else lh_d
    pv, ph = P["padding_v"] * e * S, P["padding_h"] * e * S
    hh = int(round((conteudo + 2 * pv) / S))
    fw = int(round((max(wd, wr) + 2 * ph) / S))
    HS, FS = hh * S, fw * S
    topo = (HS - conteudo) / 2

    def base_css(top, lh, f):  # baseline de uma linha CSS (meia entrelinha + ascendente)
        asc, desc = f.getmetrics()
        return top + (lh - (asc + desc)) / 2 + asc
    r = T["radius_plate"] * e
    m = mascara((FS, HS), lambda d: d.rounded_rectangle([0, 0, FS - 1, HS - 1], radius=r * S, fill=255,
                                                        corners=(True, False, False, True)))
    i_, rr, lw = P["filete_inset"] * e * S, P["filete_raio"] * e * S, max(P["filete_px"] * e, 1) * S

    def filete(d):  # '[' aberto à direita, cantos esquerdos com raio 8
        d.line([(FS - i_, i_ + lw / 2), (i_ + rr, i_ + lw / 2)], fill=255, width=int(lw))
        d.line([(FS - i_, HS - i_ - lw / 2), (i_ + rr, HS - i_ - lw / 2)], fill=255, width=int(lw))
        d.line([(i_ + lw / 2, i_ + rr), (i_ + lw / 2, HS - i_ - rr)], fill=255, width=int(lw))
        d.arc([i_, i_, i_ + 2 * rr, i_ + 2 * rr], 180, 270, fill=255, width=int(lw))
        d.arc([i_, HS - i_ - 2 * rr, i_ + 2 * rr, HS - i_], 90, 180, fill=255, width=int(lw))
    fil = mascara((FS, HS), filete)

    def texto(d):
        if rot:
            desenhar_texto(d, fr, rot, ph, base_css(topo, lh_r, fr), trk_r)
            desenhar_texto(d, fd, dest, ph, base_css(topo + lh_r + mg, lh_d, fd), trk_d)
        else:
            desenhar_texto(d, fd, dest, ph, base_css(topo, lh_d, fd), trk_d)
    txt = mascara((FS, HS), texto)
    rb, rx, ry = P["rebite_px"] * e * S, P["rebite_x"] * e * S, P["rebite_y"] * e * S
    reb = mascara((FS, HS), lambda d: [d.ellipse([rx, y, rx + rb, y + rb], fill=255) for y in (ry, HS - ry - rb)])
    luz = mascara((FS, HS), lambda d: [d.ellipse([rx + rb * .22, y + rb * .18, rx + rb * .52, y + rb * .48], fill=255)
                                       for y in (ry, HS - ry - rb)])
    m, fil, txt, reb, luz = [reduzir(a[..., None])[..., 0] for a in (m, fil, txt, reb, luz)]
    rgb = np.broadcast_to(AMARELO, m.shape + (3,)).copy()
    rgb *= (1 - T["op_grain"] * ruido_fractal(*m.shape, 7))[..., None]  # grão do esmalte 5%
    bl, ba = P["bevel_luz"]
    bs, bsa = P["bevel_sombra"]
    topo_b = np.clip(m - deslocar(m, bl * e), 0, 1) * ba
    base_b = np.clip(m - deslocar(m, -bs * e), 0, 1) * bsa
    rgb = rgb * (1 - topo_b[..., None]) + topo_b[..., None]
    rgb = rgb * (1 - base_b[..., None])
    rgb = rgb * (1 - (fil * P["filete_alfa"])[..., None]) + GRAFITE * (fil * P["filete_alfa"])[..., None]
    rgb = rgb * (1 - (reb * P["rebite_alfa"])[..., None]) + GRAFITE * (reb * P["rebite_alfa"])[..., None]
    rgb = rgb * (1 - (np.clip(reb - deslocar(reb, -1.5), 0, 1) * 0.35)[..., None])
    rgb = rgb * (1 - (luz * 0.4)[..., None]) + (luz * 0.4)[..., None]
    rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
    face = premult(rgb, m)
    # ---- módulo: quadrado com lado = altura da face
    lado = hh
    LS = lado * S
    mm = mascara((LS, HS), lambda d: d.rounded_rectangle([0, 0, LS - 1, HS - 1], radius=r * S, fill=255,
                                                         corners=(False, True, True, False)))
    if spec["modulo"] == "seta":
        icone = mascara((LS, HS), lambda d: d.polygon([(x * S, y * S) for x, y in caminho_seta(lado, P["seta_fracao"])],
                                                      fill=255))
        fundo, cor_icone = GRAFITE, AMARELO
    else:  # ✗ do bundle: M22 22l56 56M78 22L22 78, traço 16 com ponta redonda, em 54% do módulo
        k = lado * P["x_fracao"] / 100
        o = (lado - lado * P["x_fracao"]) / 2
        tw = P["x_traco"] * k * S

        def xis(d):
            for (x0, y0), (x1, y1) in (((22, 22), (78, 78)), ((78, 22), (22, 78))):
                a = ((o + x0 * k) * S, (o + y0 * k) * S)
                b = ((o + x1 * k) * S, (o + y1 * k) * S)
                d.line([a, b], fill=255, width=int(round(tw)))
                for c in (a, b):
                    d.ellipse([c[0] - tw / 2, c[1] - tw / 2, c[0] + tw / 2, c[1] + tw / 2], fill=255)
        icone = mascara((LS, HS), xis)
        fundo, cor_icone = PAPEL, VERMELHO
    mm, icone = [reduzir(a[..., None])[..., 0] for a in (mm, icone)]
    rgbm = np.broadcast_to(fundo, mm.shape + (3,)).copy()
    if spec["modulo"] == "seta":  # painel: filete claro 2 px (7%) + luz de 2 px em cima (8%)
        for camada in (np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07,
                       np.clip(mm - deslocar(mm, 2), 0, 1) * 0.08):
            rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
    else:  # papel: fibra 4% (multiply)
        rgbm *= (1 - T["op_fiber"] * ruido_fractal(*mm.shape, 11))[..., None]
    rgbm = rgbm * (1 - icone[..., None]) + cor_icone * icone[..., None]
    modulo = premult(rgbm, mm)
    medidas = {"face_largura": fw, "modulo_lado": lado, "altura": hh, "largura_total": fw + lado,
               "destino_px": round(d_px / S, 1), "rotulo_px": round(r_px / S, 1) if rot else None}
    return face, modulo, medidas


class Placa:
    PAD = 140

    def __init__(self, spec, pasta, nome):
        self.spec, self.nome = spec, nome
        self.face, self.modulo, self.medidas = placa_pecas(spec, pasta)
        self.fw, self.hh = self.face.shape[1], self.face.shape[0]
        self.lado = self.modulo.shape[1]
        self.cache = {}

    def estado(self, t_ms, saida_ms=None):
        P = CFG["placa"]
        if saida_ms is None:
            c = P["chegada"]
            mx = [(t, -self.lado if v is None else v) for t, v in c["modulo_x_px"]]
            e = {"dx": kf(c["face_x"], t_ms), "rot": kf(c["rotacao"], t_ms), "blur": kf(c["desfoque_px"], t_ms, LIN),
                 "mx": kf(mx, t_ms), "sy": kf(c["sombra_y"], t_ms), "sa": kf(c["sombra_alfa"], t_ms),
                 "sda": kf(c["sombra_dura_alfa"], t_ms), "brilho": None}
            b0, b1 = c["brilho_ms"]
            if b0 <= t_ms <= b1:
                e["brilho"] = E_CIN((t_ms - b0) / (b1 - b0))
        else:
            s = P["saida"]
            sp = T["shadow_plate"]
            e = {"dx": kf(s["face_x"], saida_ms, E_EXIT), "rot": 0.0, "blur": kf(s["desfoque_px"], saida_ms, LIN),
                 "mx": kf(s["modulo_x"], saida_ms), "sy": sp["projetada"]["y"], "sa": sp["projetada"]["alfa"],
                 "sda": sp["dura"][1], "brilho": None}
        return e

    def camada(self, e):
        chave = tuple(round(v, 2) if isinstance(v, float) else v for v in
                      (e["dx"], e["rot"], e["blur"], e["mx"], e["sy"], e["sa"], e["sda"], e["brilho"]))
        if chave in self.cache:
            return self.cache[chave]
        pad = self.PAD
        tela = np.zeros((self.hh + 2 * pad, self.fw + self.lado + 2 * pad, 4), np.float32)
        mx = e["mx"]
        sobre(tela, deslocar(self.modulo, 0, mx - int(np.floor(mx))), pad + self.fw + int(np.floor(mx)), pad)
        sobre(tela, self.brilho(e["brilho"]) if e["brilho"] is not None else self.face, pad, pad)
        tela = girar(tela, e["rot"])
        if e["blur"] >= 1:
            tela = ndimage.uniform_filter1d(tela, size=int(round(e["blur"])), axis=1, mode="constant")
        a = tela[..., 3]
        sp = T["shadow_plate"]
        sombra = sombra_objeto(a, (sp["dura"][0], e["sda"]), {**sp["projetada"], "y": e["sy"], "alfa": e["sa"]})
        out = premult(np.zeros(a.shape + (3,), np.float32), sombra)
        sobre(out, tela)
        res = (out, int(round(self.spec["x"] + e["dx"])) - pad, self.spec["y"] - pad)
        self.cache[chave] = res
        return res

    def brilho(self, p):
        """brilho de esmalte: faixa branca (34% da face, inclinada −14°) atravessa da esquerda para a direita."""
        c = CFG["placa"]["chegada"]
        fw, hh = self.fw, self.hh
        bw = c["brilho_largura"] * fw
        cx = -bw + (fw + 2 * bw) * p
        yy, xx = np.mgrid[0:hh, 0:fw].astype(np.float32)
        xs = xx + (yy - hh / 2) * np.tan(np.radians(c["brilho_inclinacao_graus"]))
        perfil = np.clip(1 - np.abs(xs - cx) / (bw / 2), 0, 1) * c["brilho_alfa"]
        a = self.face[..., 3]
        rgb = np.where(a[..., None] > 0, self.face[..., :3] / np.maximum(a[..., None], 1e-6), 0)
        return premult(soft_light_branco(rgb, perfil * (a > 0)), a)

    def linha_do_tempo(self, k):
        """('chegada', ms) / ('saida', ms) / None no quadro k."""
        k0 = self.k0
        if k < k0:
            return None
        if self.k_saida is not None:
            n_sai = int(round(CFG["placa"]["saida"]["duracao_ms"] / MS))
            if k >= self.k_saida + n_sai:
                return None
            if k >= self.k_saida:
                return ("saida", (k - self.k_saida + 1) * MS)
        return ("chegada", (k - k0 + 1) * MS)


# ---------------------------------------------------------------- legenda Padrão (igual à REV8)

def segmentos(linha):
    partes = re.split(r"(\*[^*]+\*)", linha)
    return [(p.strip("*"), p.startswith("*")) for p in partes if p]


class Legenda:
    MARGEM = 60

    def __init__(self, item, pasta):
        L = CFG["legenda"]
        self.item = item
        texto = item["texto_tela"]
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S, pasta)
        lh = L["tamanho"] * L["entrelinha"]
        asc, desc = f.getmetrics()
        linhas = texto.split("\n")
        D = L["destaque"]
        topo = L["base_y"] - len(linhas) * lh
        self.topo = topo
        self.linhas = [ln.replace("*", "") for ln in linhas]
        esp = f.getlength(" ") / S
        palavras = []
        for i, ln in enumerate(linhas):
            toks = [(w, hl) for s, hl in segmentos(ln) for w in s.split()]
            larg = [f.getlength(w) / S + (2 * D["padding_h"] if hl else 0) for w, hl in toks]
            total = sum(larg) + esp * (len(toks) - 1)
            x = L["centro_x"] - total / 2  # centro do canvas (W / 2), nunca o da zona segura
            ltop = topo + i * lh
            base_y = ltop + (lh - (asc + desc) / S) / 2 + asc / S
            for (w, hl), lw in zip(toks, larg):
                palavras.append({"w": w, "hl": hl, "x": x, "larg": lw, "base_y": base_y, "ltop": ltop})
                x += lw + esp
        self.palavras = palavras
        m = self.MARGEM
        self.x0 = int(np.floor(min(p["x"] for p in palavras))) - m
        self.x1 = int(np.ceil(max(p["x"] + p["larg"] for p in palavras))) + m
        self.y0 = int(np.floor(topo)) - m
        self.y1 = int(np.ceil(L["base_y"])) + m
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        self.mascaras = []
        for p in palavras:
            assert not p["hl"], "destaque não usado nesta revisão"
            mk = mascara((cw * S, ch * S), lambda d, p=p: d.text(((p["x"] - self.x0) * S, (p["base_y"] - self.y0) * S),
                                                                 p["w"], font=f, fill=255, anchor="ls"))
            self.mascaras.append(reduzir(mk[..., None])[..., 0])
        self.ret = [min(p["x"] for p in palavras), topo, max(p["x"] + p["larg"] for p in palavras), L["base_y"]]
        self.chars_max = max(len(x) for x in self.linhas)
        self.n_linhas = len(self.linhas)
        self.n_palavras = len(palavras)

    def estado(self, k, ultimo=False):
        it = self.item
        L = CFG["legenda"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        nsai = int(round(L["saida_ms"] / MS))
        se = 0.0
        if not ultimo and k >= it["q1"] - nsai:
            se = E_IN((k - (it["q1"] - nsai) + 1) / (nsai + 1))
        ws = []
        for j, p in enumerate(self.palavras):
            if it["modo"] == "palavra":
                kq, dur = it["palavras_q"][j], L["palavra_ms"]
            else:
                kq, dur = it["q0"], L["grupo_ms"]
            if k < kq:
                ws.append((0.0, 0.0))
                continue
            t = (k - kq + 1) * MS
            ws.append((E_OUT(t / dur) * (1 - se), (1 - E_OUT(t / dur)) * L["palavra_sobe_px"] - se * L["saida_sobe_px"]))
        return ws

    def camada(self, ws):
        L = CFG["legenda"]
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        sombra = np.zeros((ch, cw), np.float32)
        texto = np.zeros((ch, cw, 4), np.float32)
        sd, sdi = L["sombra_dura"], L["sombra_difusa"]
        for j, (op, dy) in enumerate(ws):
            if op <= 0:
                continue
            m2 = deslocar(self.mascaras[j], dy) if abs(dy) > 1e-3 else self.mascaras[j]
            s = 1 - (1 - deslocar(m2, sd[0]) * sd[1]) * (1 - ndimage.gaussian_filter(m2, sdi["blur"] / 2) * sdi["alfa"])
            sombra = 1 - (1 - sombra) * (1 - s * op)
            sobre(texto, premult(np.broadcast_to(RECIBO, m2.shape + (3,)), m2 * op))
        out = premult(np.zeros((ch, cw, 3), np.float32), sombra)
        sobre(out, texto)
        return out


# ---------------------------------------------------------------- print do app (recorte de foto, DS 2.6 + 4.5)

class Insercao:
    """Recorte do print da App Store em tela cheia sobre grafite. Revela da esquerda para a direita (máscara
    400 ms, ease-out) e faz zoom sutil 100 → 104% linear ao longo do plano, dentro da moldura fixa."""

    def __init__(self):
        I = CFG["insercao_app"]
        self.cfg = I
        self.src = Image.open(os.path.join(REV, I["arquivo"])).convert("RGB")
        x0, y0, x1, y1 = I["recorte_px"]
        self.box = (x0, y0, x1, y1)
        self.w = I["largura"]
        self.h = int(round(self.w * (y1 - y0) / (x1 - x0)))
        self.x, self.y = I["x"], I["y"]
        r = T["radius_photo"]
        self.mask = mascara_1x((self.w, self.h), lambda d: d.rounded_rectangle(
            [0, 0, self.w * SS - 1, self.h * SS - 1], radius=r * SS, fill=255))
        fl = I["filete"]
        self.filete = np.clip(self.mask - ndimage.grey_erosion(self.mask, size=(2 * fl["px"] + 1,) * 2), 0, 1) * fl["alfa"]
        self.k0 = q(o2r(I["inicio_origem"]))
        self.k1 = q(o2r(I["fim_origem"], fim=True))
        self.n = self.k1 - self.k0
        self.sombra_final = None

    def ativa(self, k):
        return self.k0 <= k < self.k1

    def imagem(self, z):
        """recorte com zoom z em torno do centro, reamostrado para w × h (sRGB, 0–1)."""
        x0, y0, x1, y1 = self.box
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hw, hh = (x1 - x0) / 2 / z, (y1 - y0) / 2 / z
        im = self.src.resize((self.w, self.h), Image.LANCZOS, box=(cx - hw, cy - hh, cx + hw, cy + hh))
        return np.asarray(im, np.float32) / 255

    def estado(self, k):
        t = (k - self.k0 + 1) * MS
        z = 1 + (T["zoom_subtle"] - 1) * (k - self.k0) / max(self.n - 1, 1)
        rv = E_OUT(t / self.cfg["revela_ms"])
        return {"t_ms": t, "zoom": z, "revela": rv}

    def quadro(self, k):
        """quadro inteiro (H × W × 3) do plano do print."""
        e = self.estado(k)
        img = np.broadcast_to(GRAFITE, (H, W, 3)).copy()
        rgb = self.imagem(e["zoom"])
        rgb = rgb * (1 - self.filete[..., None]) + self.filete[..., None]
        xs = np.arange(self.w, dtype=np.float32) + 0.5
        rev = np.clip(e["revela"] * self.w - xs + 0.5, 0, 1)[None, :]
        a = self.mask * rev
        if e["revela"] >= 0.999 and self.sombra_final is not None:
            sombra = self.sombra_final
        else:
            pad = 60
            ap = np.pad(a, pad)
            sp = T["shadow_paper"]
            sombra = sombra_objeto(ap, sp["dura"], sp["projetada"])
            if e["revela"] >= 0.999:
                self.sombra_final = sombra
        pad = 60
        camada = premult(np.zeros(sombra.shape + (3,), np.float32), sombra)
        sobre(camada, np.pad(premult(rgb, a), ((pad, pad), (pad, pad), (0, 0))))
        out = premult(img, np.ones((H, W), np.float32))
        sobre(out, camada, self.x - pad, self.y - pad)
        return out[..., :3], e

    def recorte_png(self, caminho):
        rgb = self.imagem(1.0)
        rgb = rgb * (1 - self.filete[..., None]) + self.filete[..., None]
        Image.fromarray((np.dstack([rgb, self.mask]) * 255 + 0.5).astype(np.uint8), "RGBA").save(caminho)


# ---------------------------------------------------------------- bilhete (DS 2.4, assinatura Escrita)

class Bilhete:
    PAD = 70

    def __init__(self, pasta):
        B = CFG["bilhete"]
        self.cfg = B
        S = SS
        f = fonte(B["fonte"], B["tamanho"] * S, pasta)
        lh = B["tamanho"] * B["entrelinha"]
        asc, desc = f.getmetrics()
        larg = [f.getlength(t) / S for t in B["linhas"]]
        self.w = int(np.ceil(max(larg) + 2 * B["padding_h"]))
        self.h = int(np.ceil(len(B["linhas"]) * lh + 2 * B["padding_v"]))
        papel_m = mascara_1x((self.w, self.h), lambda d: d.rounded_rectangle(
            [0, 0, self.w * S - 1, self.h * S - 1], radius=T["radius_paper"] * S, fill=255))

        def texto(d):
            for i, t in enumerate(B["linhas"]):
                top = B["padding_v"] + i * lh
                base = top + (lh - (asc + desc) / S) / 2 + asc / S
                d.text((B["padding_h"] * S, base * S), t, font=f, fill=255, anchor="ls")
        self.txt = mascara_1x((self.w, self.h), texto)
        rgb = np.broadcast_to(PAPEL, papel_m.shape + (3,)).copy()
        rgb *= (1 - T["op_fiber"] * ruido_fractal(*papel_m.shape, 5))[..., None]  # fibra 4%
        self.papel_rgb, self.papel_m = rgb, papel_m
        self.chars_max = max(len(t) for t in B["linhas"])
        self.k0 = q(o2r(B["inicio_origem"]))
        self.k1 = q(o2r(B["fim_origem"]))
        # posição: zona de objeto (y 880–1220), encostado no limite do lado escolhido depois da rotação de +3°
        larg_girada = self.w * np.cos(np.radians(T["rot_note"])) + self.h * np.sin(np.radians(T["rot_note"]))
        folga = (larg_girada - self.w) / 2
        self.x = int(np.floor(SAFE["x1"] - self.w - folga)) if B["lado"] == "direita" else int(np.ceil(SAFE["x0"] + folga))
        self.y = B["y"]
        self.cache = {}

    def ativo(self, k):
        return self.k0 <= k < self.k1

    def estado(self, k):
        B = self.cfg
        t = (k - self.k0 + 1) * MS
        p = min(t / B["entra_ms"], 1)
        e = {"dy": 24 * (1 - E_ARR(p)), "rot": T["rot_note"] * E_ARR(p), "op": min(E_ARR(p), 1.0),
             "escrita": E_OUT((t - B["entra_ms"]) / B["escreve_ms"]) if t > B["entra_ms"] else 0.0}
        n_sai = int(round(B["sai_ms"] / MS))
        if k >= self.k1 - n_sai:
            ps = E_EXIT((k - (self.k1 - n_sai) + 1) / n_sai)
            e.update({"dy": 40 * ps, "rot": T["rot_note"], "op": 1 - ps})
        return e

    def camada(self, e):
        chave = (round(e["dy"], 1), round(e["rot"], 2), round(e["op"], 3), round(e["escrita"], 3))
        if chave in self.cache:
            return self.cache[chave]
        pad = self.PAD
        xs = np.arange(self.w, dtype=np.float32) + 0.5
        rev = np.clip(e["escrita"] * self.w - xs + 0.5, 0, 1)[None, :]
        t = self.txt * rev
        rgb = self.papel_rgb * (1 - t[..., None]) + CANETA * t[..., None]
        obj = np.pad(premult(rgb, self.papel_m), ((pad, pad), (pad, pad), (0, 0)))
        obj = girar(obj, e["rot"])
        sp = T["shadow_paper"]
        sombra = sombra_objeto(obj[..., 3], sp["dura"], sp["projetada"])
        out = premult(np.zeros(sombra.shape + (3,), np.float32), sombra)
        sobre(out, obj)
        out *= e["op"]
        res = (out, self.x - pad, int(round(self.y + e["dy"])) - pad)
        self.cache[chave] = res
        return res


# ---------------------------------------------------------------- composição

def scrim_alfa():
    S = CFG["scrim"]
    y = np.arange(H, dtype=np.float32)
    return (np.clip((y - S["y0"]) / (S["y1"] - S["y0"]), 0, 1) * T["op_scrim"])[:, None, None]


def grao(k):
    G = CFG["grao"]
    rng = np.random.default_rng(G["semente"] + k)
    z = ndimage.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), G["sigma_px"])
    z /= z.std()
    return np.clip(0.5 + 0.289 * z, 0, 1)[..., None]


def overlay_blend(b, n, op):
    o = np.where(b < 0.5, 2 * b * n, 1 - 2 * (1 - b) * (1 - n))
    return b + op * (o - b)


def aviso_teste(pasta):
    """rótulo do modo teste, no topo (área de interface, fora da peça)."""
    f = fonte("Barlow-Bold.ttf", 30 * SS, pasta)
    txt = "TESTE DE DESIGN · FUNDO PROVISÓRIO · SEM ÁUDIO"
    w = int(f.getlength(txt) / SS) + 40
    m = mascara_1x((w, 60), lambda d: d.text((20 * SS, 42 * SS), txt, font=f, fill=255, anchor="ls"))
    out = premult(np.zeros((60, w, 3), np.float32), np.full((60, w), 0.7, np.float32))
    sobre(out, premult(np.broadcast_to(AMARELO, m.shape + (3,)), m))
    return out, (W - w) // 2, 120


class Cena:
    def __init__(self, pasta, teste):
        self.placa = Placa(CFG["placa_nao_faca"], pasta, "placa_nao_faca")
        self.placa.k0 = q(CFG["placa_nao_faca"]["inicio_s"])
        self.placa.k_saida = q(CFG["placa_nao_faca"]["saida_inicio_s"])
        self.cta = Placa(CFG["placa_cta"], pasta, "placa_cta")
        self.cta.k0 = q(o2r(CFG["placa_cta"]["inicio_origem"]))
        self.cta.k_saida = None
        self.leg = tempos_legendas()
        self.legendas = [Legenda(L, pasta) for L in self.leg]
        self.ins = Insercao()
        self.bil = Bilhete(pasta)
        self.scrim = scrim_alfa()
        self.aviso = aviso_teste(pasta) if teste else None
        self.registro = {}

    def compor(self, base_rgb, k):
        els = []
        if self.ins.ativa(k):
            base_rgb, e = self.ins.quadro(k)
            els.append(("print_app", self.ins.x, self.ins.y, self.ins.x + self.ins.w, self.ins.y + self.ins.h,
                        round(e["revela"], 3), round(e["zoom"], 4)))
        img = overlay_blend(base_rgb, grao(k), T["op_grain"])
        img = img * (1 - self.scrim) + GRAFITE * self.scrim
        camada = np.zeros((H, W, 4), np.float32)
        for pl in (self.placa, self.cta):
            st = pl.linha_do_tempo(k)
            if not st:
                continue
            e = pl.estado(st[1]) if st[0] == "chegada" else pl.estado(None, saida_ms=st[1])
            im, x, y = pl.camada(e)
            sobre(camada, im, x, y)
            xf = pl.spec["x"] + e["dx"]
            els.append((pl.nome, round(xf, 1), pl.spec["y"], round(xf + pl.medidas["largura_total"], 1),
                        pl.spec["y"] + pl.medidas["altura"], st[0], round(st[1], 1)))
        e = self.bil.estado(k) if self.bil.ativo(k) else None
        if e and e["op"] > 1e-3:
            im, x, y = self.bil.camada(e)
            sobre(camada, im, x, y)
            cx = caixa_alfa(im[..., 3] / max(e["op"], 1e-6) * (im[..., 3] > 0), 0.5)
            els.append(("bilhete", x + cx[0], y + cx[1], x + cx[2], y + cx[3], round(e["op"], 3), round(e["escrita"], 3)))
        for lg in self.legendas:
            ws = lg.estado(k, ultimo=(lg.item["q1"] == N))
            if ws is None:
                continue
            sobre(camada, lg.camada(ws), lg.x0, lg.y0)
            els.append(("legenda", *[round(v, 1) for v in lg.ret], lg.item["texto"], round(max(o for o, _ in ws), 3)))
        if self.aviso:
            sobre(camada, *self.aviso)
        self.registro[k] = els
        a = camada[..., 3:4]
        return img * (1 - a) + camada[..., :3]


# ---------------------------------------------------------------- fontes de vídeo e áudio

def info_fonte(arq):
    s = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,color_transfer:stream_side_data=rotation", "-of", "json", arq],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    w, h = s["width"], s["height"]
    rot = next((int(float(d["rotation"])) for d in s.get("side_data_list", []) if "rotation" in d), 0)
    if rot % 180:
        w, h = h, w
    return {"w": w, "h": h, "hdr": s.get("color_transfer") == "arib-std-b67", "fps": s["r_frame_rate"]}


def filtro_crop(centro_x, fw, fh):
    """recorte 9:16 de altura cheia, centrado em centro_x (fração da largura), como no render.py."""
    k = fh // 16
    cw, ch = 9 * k, 16 * k
    x = int(round(min(max(centro_x * fw - cw / 2, 0), fw - cw) / 2)) * 2
    y = int(round((fh - ch) / 2 / 2)) * 2
    return f"crop=w={cw}:h={ch}:x={x}:y={y}"


def decodificador(master, teste):
    if teste:
        fundo = os.path.normpath(os.path.join(REV, CFG["teste"]["fundo"]))
        return subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(CFG["teste"]["fundo_inicio_s"]), "-i", fundo,
                                 "-vf", "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,"
                                 "format=rgb48le", "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"],
                                stdout=subprocess.PIPE)
    inf = info_fonte(master)
    if inf["fps"] != f"{FPS}/1":
        print(f"   aviso: master a {inf['fps']} fps; os quadros são reamostrados para {FPS} fps")
    cadeia = TONEMAP_RGB if inf["hdr"] else SDR_RGB
    entradas, filtros, rot = [], [], []
    for i, p in enumerate(PLANOS):
        entradas += ["-ss", f"{p['o0'] / FPS:.6f}", "-i", master]
        filtros.append(f"[{i}:v]fps={FPS},trim=end_frame={p['o1'] - p['o0']},setpts=PTS-STARTPTS,"
                       f"{filtro_crop(p['centro_x'], inf['w'], inf['h'])},{cadeia}[v{i}]")
        rot.append(f"[v{i}]")
    filtros.append(f"{''.join(rot)}concat=n={len(PLANOS)}:v=1:a=0[v]")
    return subprocess.Popen(["ffmpeg", "-v", "error", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]",
                             "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)


def ler_audio(arq, ini_s, n_amostras):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ini_s:.6f}", "-i", arq, "-map", "0:a:0", "-t",
                        f"{n_amostras / SR + 0.1:.6f}", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.float32).reshape(-1, 2)
    if len(a) < n_amostras:
        a = np.vstack([a, np.zeros((n_amostras - len(a), 2), np.float32)])
    return a[:n_amostras].astype(np.float64)


def ebur128_f32(arq_f32):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", arq_f32,
                        "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1)))


def montar_audio(master, teste):
    """Som direto dos planos com crossfade de potência constante nas emendas, fade-out final e master em
    −14 LUFS / ≤ −1 dBTP (ganho linear; limitador só se o pico passar do limite)."""
    wav = os.path.join(TMP, "audio_rev1.f32")
    if teste:
        np.zeros((N * SPF, 2), np.float32).tofile(wav)
        return wav, {"teste": "silêncio"}
    A = CFG["audio"]
    h = int(round(A["crossfade_ms"] / 1000 * SR / 2))
    mix = np.zeros((N * SPF, 2), np.float64)
    for i, p in enumerate(PLANOS):
        ha = h if i > 0 else 0
        hb = h if i < len(PLANOS) - 1 else 0
        o0, o1, r0, r1 = p["o0"] * SPF, p["o1"] * SPF, p["r0"] * SPF, p["r1"] * SPF
        trecho = ler_audio(master, (o0 - ha) / SR, o1 + hb - (o0 - ha))
        env = np.ones(len(trecho))
        if ha:
            env[:2 * ha] = np.sin(np.linspace(0, np.pi / 2, 2 * ha, endpoint=False) + np.pi / (8 * ha))
        if hb:
            env[-2 * hb:] = np.cos(np.linspace(0, np.pi / 2, 2 * hb, endpoint=False) + np.pi / (8 * hb))
        mix[r0 - ha:r1 + hb] += trecho * env[:, None]
    dc = int(0.005 * SR)
    mix[:dc] *= np.linspace(0, 1, dc, endpoint=False)[:, None]
    nf = int(A["fade_out_ms"] / 1000 * SR)
    mix[-nf:] *= np.cos(np.linspace(0, np.pi / 2, nf))[:, None]
    bruto = os.path.join(TMP, "audio_bruto.f32")
    mix.astype(np.float32).tofile(bruto)
    i0, tp0 = ebur128_f32(bruto)
    ganho = A["lufs_alvo"] - i0
    (mix * 10 ** (ganho / 20)).astype(np.float32).tofile(wav)
    i1, tp1 = ebur128_f32(wav)
    R = {"bruto": {"lufs": i0, "pico_dbtp": tp0}, "ganho_db": round(ganho, 2), "apos_ganho": {"lufs": i1, "pico_dbtp": tp1},
         "limitador": False}
    if tp1 > A["pico_max_dbtp"]:
        lim = os.path.join(TMP, "audio_lim.f32")
        rodar(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav, "-af",
               f"alimiter=limit={A['limitador_amplitude']}:attack=5:release=50:level=0", "-f", "f32le", lim])
        shutil.move(lim, wav)
        R["limitador"] = True
        R["final"] = dict(zip(("lufs", "pico_dbtp"), ebur128_f32(wav)))
    else:
        R["final"] = R["apos_ganho"]
    return wav, R


# ---------------------------------------------------------------- render

def render(cena, master, teste, saida):
    dec = decodificador(master, teste)
    wav, R_audio = montar_audio(master, teste)
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", saida]], stdin=subprocess.PIPE)
    tam = W * H * 3 * 2
    for k in range(N):
        buf = dec.stdout.read(tam)
        assert len(buf) == tam, f"quadro {k} incompleto"
        base = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
        out = cena.compor(base, k)
        enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
        if k % 48 == 0:
            print(f"   quadro {k}/{N}", flush=True)
    dec.stdout.close()
    enc.stdin.close()
    assert dec.wait() == 0 and enc.wait() == 0
    return R_audio


# ---------------------------------------------------------------- QA

def ffprobe(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", arq],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1)))


def qa(cena, saida, teste, R_audio):
    R = {"arquivo": os.path.relpath(saida, os.path.dirname(REV)), "modo": "teste (fundo provisório, sem áudio)" if teste
         else "final (master)"}
    pr = ffprobe(saida)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "duracao_s": round(int(v["nb_read_frames"]) / FPS, 3),
                    "duracao_audio_s": float(a["duration"]), "codec_video": f"{v['codec_name']} ({v.get('profile')})",
                    "cor": f"{v.get('color_primaries')}/{v.get('color_transfer')}/{v.get('color_space')}/{v.get('color_range')}",
                    "tamanho_bytes": int(pr["format"]["size"])}
    R["audio"] = R_audio
    if not teste:
        lufs, tp = ebur128(saida)
        R["audio"]["arquivo_final"] = {"lufs": lufs, "pico_dbtp": tp,
                                       "ok": bool(abs(lufs - CFG["audio"]["lufs_alvo"]) <= 0.5 and tp <= CFG["audio"]["pico_max_dbtp"])}
    R["planos"] = [{"n": p["n"], "origem_s": p["origem"], "reel_s": [round(p["r0"] / FPS, 3), round(p["r1"] / FPS, 3)],
                    "centro_x": p["centro_x"]} for p in PLANOS]
    R["cortes_s"] = cortes_s()
    # objetos parados dentro da zona segura; legenda acima do limite; folgas
    fora, sobrep = [], []
    for k, els in cena.registro.items():
        for e in els:
            nome, x0, y0, x1, y1 = e[:5]
            if nome == "print_app" or (nome.startswith("placa") and (e[5] == "saida" or e[6] < 400)):
                continue
            if nome == "bilhete" and e[5] < 1:
                continue
            if x0 < SAFE["x0"] - 0.5 or x1 > SAFE["x1"] + 0.5 or y0 < SAFE["y0"] or y1 > SAFE["y1"]:
                fora.append((k, *e[:5]))
        objs = [e for e in els if e[0] in ("placa_nao_faca", "placa_cta", "bilhete")]
        for e in els:
            if e[0] == "legenda":
                for o in objs:
                    if e[2] < o[4] and not (o[0].startswith("placa") and o[5] == "saida"):
                        sobrep.append((k, o[0], e[5]))
    entradas = {"placa_nao_faca": cena.placa.k0 / FPS, "bilhete": cena.bil.k0 / FPS, "placa_cta": cena.cta.k0 / FPS}
    seq = sorted(entradas.values())
    pl, ct = cena.placa.medidas, cena.cta.medidas
    R["objetos"] = {
        "placa_nao_faca": {**pl, "x": CFG["placa_nao_faca"]["x"], "y": CFG["placa_nao_faca"]["y"],
                           "chegada_s": 0.0, "saida_s": [round(cena.placa.k_saida / FPS, 3),
                                                         round((cena.placa.k_saida + 6) / FPS, 3)],
                           "area_pct": round(100 * pl["largura_total"] * pl["altura"] / (W * H), 1)},
        "placa_cta": {**ct, "x": CFG["placa_cta"]["x"], "y": CFG["placa_cta"]["y"], "chegada_s": round(cena.cta.k0 / FPS, 3),
                      "x_final": CFG["placa_cta"]["x"] + ct["largura_total"],
                      "largura_max_ds_872": ct["largura_total"] <= 872},
        "print_app": {"de_s": round(cena.ins.k0 / FPS, 3), "ate_s": round(cena.ins.k1 / FPS, 3),
                      "duracao_s": round(cena.ins.n / FPS, 3), "caixa": [cena.ins.x, cena.ins.y, cena.ins.x + cena.ins.w,
                                                                          cena.ins.y + cena.ins.h],
                      "zoom": [1.0, T["zoom_subtle"]], "revela_ms": CFG["insercao_app"]["revela_ms"]},
        "bilhete": {"de_s": round(cena.bil.k0 / FPS, 3), "ate_s": round(cena.bil.k1 / FPS, 3), "x": cena.bil.x,
                    "y": cena.bil.y, "largura": cena.bil.w, "altura": cena.bil.h, "linhas": CFG["bilhete"]["linhas"],
                    "max_caracteres_linha": cena.bil.chars_max},
        "entradas_de_objetos_s": {k: round(v, 3) for k, v in entradas.items()},
        "intervalo_min_entre_entradas_s": round(min(b - a for a, b in zip(seq, seq[1:])), 3),
        "n_fora_da_zona_segura_parado": len(fora), "fora_da_zona_segura_parado": fora[:10],
        "n_legenda_sobre_objeto": len(sobrep), "legenda_sobre_objeto": sobrep[:10]}
    lg = cena.legendas
    R["legendas"] = {"grupos": [{k: L.get(k) for k in ("texto_tela", "de", "ate", "fala_rev", "palavras_por_s", "modo",
                                                          "palavras_q")} for L in cena.leg],
                     "max_caracteres_linha": max(x.chars_max for x in lg), "max_linhas": max(x.n_linhas for x in lg),
                     "max_palavras_grupo": max(x.n_palavras for x in lg),
                     "topo_min_bloco_y": round(min(x.topo for x in lg), 1),
                     "x_min": round(min(x.ret[0] for x in lg), 1), "x_max": round(max(x.ret[2] for x in lg), 1)}
    L = CFG["legenda"]
    R["checagens"] = {
        "legenda_ate_26_caracteres": R["legendas"]["max_caracteres_linha"] <= L["max_caracteres"],
        "legenda_ate_2_linhas": R["legendas"]["max_linhas"] <= L["max_linhas"],
        "legenda_ate_6_palavras": R["legendas"]["max_palavras_grupo"] <= L["max_palavras"],
        "legenda_topo_maior_igual_1250": R["legendas"]["topo_min_bloco_y"] >= L["topo_min_y"],
        "objetos_parados_na_zona_segura": not fora,
        "legenda_sem_sobrepor_objeto": not sobrep,
        "calma_1_5_s_entre_entradas": R["objetos"]["intervalo_min_entre_entradas_s"] >= 1.5,
        "bilhete_ate_22_caracteres": cena.bil.chars_max <= 22,
        "cta_ate_872_px": ct["largura_total"] <= 872,
        "print_acima_da_legenda": cena.ins.y + cena.ins.h <= L["topo_min_y"],
        "transicoes": 0}
    return R


def frames_qa(saida, tag, pasta):
    shutil.rmtree(pasta, ignore_errors=True)
    os.makedirs(pasta)
    lista = []
    for t in CFG["qa_tempos_s"]:
        k = min(q(t), N - 1)
        arq = os.path.join(pasta, f"{tag}_t{t:05.2f}s_quadro{k:03d}.jpg".replace(".", "_", 1))
        rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1, "-q:v", 2, arq])
        lista.append((t, k, arq))
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    folha = Image.new("RGB", (cols * cw, ((len(lista) + cols - 1) // cols) * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (t, k, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc],
                                     outline=(255, 0, 0))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"{t:.2f} s  quadro {k}", fill=(0, 0, 0))
    folha.save(os.path.join(pasta, f"folha_qa_{tag}.jpg"), quality=90)
    return [(t, k, os.path.relpath(a, REV)) for t, k, a in lista]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True, help="pasta com " + ", ".join(FONTES_USADAS))
    ap.add_argument("--master", default=os.environ.get("REEL_MASTER"), help="vlog master de Barcelona (4K HLG)")
    ap.add_argument("--teste", action="store_true", help="só a camada de design, sobre fundo provisório e sem áudio")
    args = ap.parse_args()
    if not args.teste and not (args.master and os.path.exists(args.master)):
        sys.exit("informe o master (--master ou REEL_MASTER) ou rode com --teste")
    os.makedirs(TMP, exist_ok=True)
    print(f"1/4 linha do tempo: {N} quadros = {N / FPS:.3f} s; cortes em {cortes_s()}")
    cena = Cena(args.fontes, args.teste)
    for L in cena.leg:
        print(f"   {L['de']:6.3f}–{L['ate']:6.3f}  {L['modo']:7s} {L['palavras_por_s']:4.1f}/s  {L['texto_tela']!r}")
    print("   placa", cena.placa.medidas, "| cta", cena.cta.medidas)
    print(f"   print do app {cena.ins.k0 / FPS:.3f}–{cena.ins.k1 / FPS:.3f} s · bilhete {cena.bil.k0 / FPS:.3f}–"
          f"{cena.bil.k1 / FPS:.3f} s · CTA {cena.cta.k0 / FPS:.3f} s")
    cena.ins.recorte_png(os.path.join(REV, "assets", "app_fonts_bcn_recorte.png"))
    saida = os.path.join(REV, CFG["saida_teste"] if args.teste else CFG["saida"])
    print("2/4 render")
    R_audio = render(cena, args.master, args.teste, saida)
    print("3/4 QA")
    R = qa(cena, saida, args.teste, R_audio)
    R["frames_qa"] = frames_qa(saida, "teste" if args.teste else "rev1",
                               os.path.join(TMP, "qa_teste") if args.teste else QA_DIR)
    R["sha256"] = hashlib.sha256(open(saida, "rb").read()).hexdigest()
    R["fontes"] = {n: hashlib.sha256(open(os.path.join(args.fontes, n), "rb").read()).hexdigest() for n in FONTES_USADAS}
    rel = os.path.join(TMP if args.teste else REV, "relatorio_teste.json" if args.teste else "relatorio_tecnico_rev1.json")
    json.dump(R, open(rel, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    if not args.teste:
        print("4/4 prévia leve")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
               "-crf", 24, "-preset", "slow", "-pix_fmt", "yuv420p", *TAGS_COR, "-c:a", "aac", "-b:a", "128k",
               "-movflags", "+faststart", os.path.join(REV, CFG["saida_previa"])])
    print(json.dumps({k: R[k] for k in ("formato", "checagens")}, ensure_ascii=False, indent=1, default=str))
    print(saida)


if __name__ == "__main__":
    sys.exit(main())
