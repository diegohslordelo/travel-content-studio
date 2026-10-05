"""Objetos do Design System V2 usados no Reel "Barcelona em 20 segundos" (REV4, v2).

Placa, módulo de seta, módulo 1º (Nascer), legenda Padrão, scrim e grão. A placa, a legenda, o scrim e o grão
são os mesmos da REV8 do Reel de apresentação (reels/apresentacao/rev8/scripts/rev8.py), que já implementa o
DS 2.1 e 3.2; aqui eles leem a configuração de rev4.json. Na REV3 a placa usa a variante Abertura (rótulo + destino) e o
fechamento é o módulo 1º do kit do DS (classe Modulo1) com Chegada + Nascer. O módulo 1º e o Arrasto são novos neste Reel e seguem
o DS 4.3, 4.4 e o pd-bundle.js (função one()).
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

REV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REV, "rev4.json"), encoding="utf-8"))
FPS = CFG["fps"]
W, H = CFG["largura"], CFG["altura"]
MS = 1000 / FPS
SS = 4  # supersampling dos objetos
T = CFG["tokens"]
SAFE = T["safe"]


def cor(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO = cor(T["signal_500"])
GRAFITE = cor(T["night_900"])
RECIBO = cor(T["paper_0"])


# ---------------------------------------------------------------- curvas e keyframes

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
E_IN = bezier([0.42, 0.0, 1.0, 1.0])  # 'ease-in' do CSS (saída da legenda, cena que sai no Arrasto)


def kf(chaves, t, curva=E_OUT):
    """valor dos keyframes [(ms, valor), …] no instante t (ms); curva por segmento."""
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- utilidades de imagem

def fonte(nome, px, pasta):
    return ImageFont.truetype(os.path.join(pasta, nome), px)


def reduzir(a, s=SS):
    h, w = a.shape[0] // s, a.shape[1] // s
    return a[:h * s, :w * s].reshape(h, s, w, s, -1).mean((1, 3))


def mascara(tam, desenho):
    im = Image.new("L", tam, 0)
    desenho(ImageDraw.Draw(im))
    return np.asarray(im, np.float32) / 255


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


# ---------------------------------------------------------------- placa

def caminho_seta(lado):
    """seta do bundle (pd-bundle.js, viewBox 100): M8 41h50V18l38 32-38 32V59H8z, em 54% do módulo."""
    P = CFG["placa"]
    k = lado * P["seta_fracao"] / 100
    ox = oy = (lado - lado * P["seta_fracao"]) / 2
    pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
    return [(ox + x * k, oy + y * k) for x, y in pts]


def _linha(d, texto, f, x, base, trk):
    for c in texto:
        d.text((x, base), c, font=f, fill=255, anchor="ls")
        x += f.getlength(c) + trk


def _largura(texto, f, trk):
    return sum(f.getlength(c) for c in texto) + trk * (len(texto) - 1)


def face_placa(pasta):
    """Face esmaltada da variante Abertura (DS 2.1): rótulo (label 36 px) + destino (h1 128 px), relevo, filete,
    rebites e grão; premultiplicada, 1x. Define a altura da placa e o lado do módulo (quadrado) em CFG["placa"]."""
    P = CFG["placa"]
    S = SS
    fd = fonte(P["fonte"], P["tamanho"] * S, pasta)
    fr = fonte(P["fonte_rotulo"], P["tamanho_rotulo"] * S, pasta)
    trk_d = P["tracking_em"] * P["tamanho"] * S
    trk_r = P["tracking_rotulo_em"] * P["tamanho_rotulo"] * S
    larg_d, larg_r = _largura(P["texto"], fd, trk_d), _largura(P["rotulo"], fr, trk_r)
    lh_r = P["tamanho_rotulo"] * 1.0                 # label: entrelinha 1,0
    lh_d = P["tamanho"] * 0.90                       # h1: entrelinha 0,90
    hh = int(round(2 * P["padding_v"] + lh_r + P["espaco_linhas"] + lh_d))
    P["altura"], P["modulo"] = hh, hh
    fw = int(round(2 * P["padding_h"] + max(larg_d, larg_r) / S))
    r = T["radius_plate"]
    m = mascara((fw * S, hh * S), lambda d: d.rounded_rectangle([0, 0, fw * S - 1, hh * S - 1], radius=r * S,
                                                                fill=255, corners=(True, False, False, True)))
    i_ = P["filete_inset"] * S
    rr = P["filete_raio"] * S
    lw = P["filete_px"] * S

    def filete(d):
        d.line([(fw * S - i_, i_ + lw / 2), (i_ + rr, i_ + lw / 2)], fill=255, width=lw)
        d.line([(fw * S - i_, hh * S - i_ - lw / 2), (i_ + rr, hh * S - i_ - lw / 2)], fill=255, width=lw)
        d.line([(i_ + lw / 2, i_ + rr), (i_ + lw / 2, hh * S - i_ - rr)], fill=255, width=lw)
        d.arc([i_, i_, i_ + 2 * rr, i_ + 2 * rr], 180, 270, fill=255, width=lw)
        d.arc([i_, hh * S - i_ - 2 * rr, i_ + 2 * rr, hh * S - i_], 90, 180, fill=255, width=lw)
    fil = mascara((fw * S, hh * S), filete)
    # cada linha com a altura de maiúscula centrada na sua caixa de linha
    cap_r = -fr.getbbox("H", anchor="ls")[1]
    cap_d = -fd.getbbox("H", anchor="ls")[1]
    topo_r = P["padding_v"] * S
    base_r = topo_r + (lh_r * S + cap_r) / 2
    topo_d = topo_r + (lh_r + P["espaco_linhas"]) * S
    base_d = topo_d + (lh_d * S + cap_d) / 2
    x0 = P["padding_h"] * S
    txt = mascara((fw * S, hh * S), lambda d: (_linha(d, P["rotulo"], fr, x0, base_r, trk_r),
                                               _linha(d, P["texto"], fd, x0, base_d, trk_d)))
    rb = P["rebite_px"] * S
    rx, ry = P["rebite_x"] * S, P["rebite_y"] * S
    reb = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx, y, rx + rb, y + rb], fill=255)
                                                for y in (ry, hh * S - ry - rb)])
    luz = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx + rb * .22, y + rb * .18, rx + rb * .52, y + rb * .48],
                                                         fill=255) for y in (ry, hh * S - ry - rb)])
    m, fil, txt, reb, luz = [reduzir(a[..., None])[..., 0] for a in (m, fil, txt, reb, luz)]
    rgb = np.broadcast_to(AMARELO, m.shape + (3,)).copy()
    g = ruido_fractal(*m.shape, 7)
    rgb *= (1 - T["op_grain"] * g)[..., None]
    bl, ba = P["bevel_luz"]
    bs, bsa = P["bevel_sombra"]
    topo = np.clip(m - deslocar(m, bl), 0, 1) * ba
    base = np.clip(m - deslocar(m, -bs), 0, 1) * bsa
    rgb = rgb * (1 - topo[..., None]) + topo[..., None]
    rgb = rgb * (1 - base[..., None])
    rgb = rgb * (1 - (fil * P["filete_alfa"])[..., None]) + GRAFITE * (fil * P["filete_alfa"])[..., None]
    rgb = rgb * (1 - (reb * P["rebite_alfa"])[..., None]) + GRAFITE * (reb * P["rebite_alfa"])[..., None]
    rb_sombra = np.clip(reb - deslocar(reb, -1.5), 0, 1) * 0.35
    rgb = rgb * (1 - rb_sombra[..., None])
    rgb = rgb * (1 - (luz * 0.4)[..., None]) + (luz * 0.4)[..., None]
    rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
    return premult(rgb, m), round(max(larg_d, larg_r) / S, 1)


def painel_modulo(lado=None, hh=None, cantos=(False, True, True, False)):
    """Módulo grafite vazio (painel: filete claro 7% + luz de 2 px em cima 8%): (rgb, alfa) em 1x."""
    P = CFG["placa"]
    S = SS
    lado = P["modulo"] if lado is None else lado
    hh = P["altura"] if hh is None else hh
    r = T["radius_plate"]
    mm = mascara((lado * S, hh * S), lambda d: d.rounded_rectangle([0, 0, lado * S - 1, hh * S - 1], radius=r * S,
                                                                   fill=255, corners=cantos))
    mm = reduzir(mm[..., None])[..., 0]
    rgbm = np.broadcast_to(GRAFITE, mm.shape + (3,)).copy()
    borda = np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07
    topo_m = np.clip(mm - deslocar(mm, 2), 0, 1) * 0.08
    for camada in (borda, topo_m):
        rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
    return rgbm, mm


def modulo_seta():
    P = CFG["placa"]
    S = SS
    lado, hh = P["modulo"], P["altura"]
    rgbm, mm = painel_modulo()
    seta = mascara((lado * S, hh * S), lambda d: d.polygon([(x * S, y * S + (hh - lado) * S / 2)
                                                            for x, y in caminho_seta(lado)], fill=255))
    seta = reduzir(seta[..., None])[..., 0]
    rgbm = rgbm * (1 - seta[..., None]) + AMARELO * seta[..., None]
    return premult(rgbm, mm)


def modulo_um(t_ms):
    """Módulo com o símbolo 1º do bundle, no instante t_ms da assinatura Nascer (None ou < 0: módulo vazio)."""
    P = CFG["placa"]
    F = CFG["fechamento"]
    U, N_ = F["modulo_1"], F["nascer"]
    S = SS
    lado, hh = P["modulo"], P["altura"]
    rgbm, mm = painel_modulo()
    if t_ms is None or t_ms < 0:
        return premult(rgbm, mm)
    k = lado * U["fracao"] / 100 * S              # px (supersampled) por unidade do viewBox 100
    ox = (lado - lado * U["fracao"]) / 2 * S
    oy = (hh - lado * U["fracao"]) / 2 * S
    pt = lambda x, y: (ox + x * k, oy + y * k)  # noqa: E731
    # sol: sobe de +120% da própria altura (30 unidades) até o lugar, recortado na base da barra (horizonte)
    p_sol = E_CIN(t_ms / N_["sol_ms"])
    cy = 17 + 30 * N_["sol_desloc_frac"] * (1 - p_sol)
    sol = mascara((lado * S, hh * S), lambda d: d.ellipse([*pt(76 - 15, cy - 15), *pt(76 + 15, cy + 15)], fill=255))
    horizonte = int(round(oy + 43.5 * k))
    sol[horizonte:] = 0
    # barra: cresce da esquerda
    p_bar = E_OUT(t_ms / N_["barra_ms"])
    barra = mascara((lado * S, hh * S), lambda d: d.rectangle([*pt(58.7, 38), *pt(58.7 + 34.5 * p_bar, 43.5)], fill=255)
                    if p_bar > 0 else None)
    # número: sobe 10 px e aparece, depois de 500 ms
    tn = (t_ms - N_["numero_atraso_ms"]) / N_["numero_ms"]
    p_num = E_OUT(tn) if tn > 0 else 0.0
    dy = (1 - p_num) * N_["numero_sobe_px"] * S
    pts = [(26, 4), (48, 4), (48, 100), (26, 100), (26, 30), (12, 37), (12, 16)]
    num = mascara((lado * S, hh * S), lambda d: d.polygon([(x, y + dy) for x, y in (pt(*p) for p in pts)], fill=255))
    sol, barra, num = [reduzir(a[..., None])[..., 0] for a in (sol, barra, num)]
    num *= p_num
    rgbm = rgbm * (1 - sol[..., None]) + AMARELO * sol[..., None]
    rgbm = rgbm * (1 - barra[..., None]) + AMARELO * barra[..., None]
    rgbm = rgbm * (1 - num[..., None]) + cor(U["cor_numero"]) * num[..., None]
    return premult(rgbm, mm)


class Placa:
    """Placa PRIMEIRO DIA (variante Marca) com módulo de seta ou módulo 1º. Chegada, saída e (no 1º) Nascer."""
    PAD = 140

    def __init__(self, pasta, modulo="seta"):
        self.tipo = modulo
        self.face, self.texto_avanco = face_placa(pasta)
        self.seta = modulo_seta() if modulo == "seta" else None
        c = CFG["placa"]["chegada"]
        lado = CFG["placa"]["modulo"]
        c["modulo_x"] = [[t, (-lado if v == -176 else v)] for t, v in c["modulo_x"]]
        self.fw = self.face.shape[1]
        self.hh = self.face.shape[0]
        self.lado = CFG["placa"]["modulo"]
        self.cache = {}
        self.medidas = {"face_largura": self.fw, "modulo_largura": self.lado, "altura": self.hh,
                        "largura_total": self.fw + self.lado, "texto_avanco_px": self.texto_avanco}

    def estado(self, t_ms, saida_ms=None):
        P = CFG["placa"]
        if saida_ms is None:
            c = P["chegada"]
            e = {"dx": kf(c["face_x"], t_ms), "rot": kf(c["rotacao"], t_ms), "blur": kf(c["desfoque_px"], t_ms, LIN),
                 "mx": kf(c["modulo_x"], t_ms), "sy": kf(c["sombra_y"], t_ms), "sa": kf(c["sombra_alfa"], t_ms),
                 "sda": kf(c["sombra_dura_alfa"], t_ms), "brilho": None, "nascer": None}
            b0, b1 = c["brilho_ms"]
            if b0 <= t_ms <= b1:
                e["brilho"] = E_CIN((t_ms - b0) / (b1 - b0))
            if self.tipo == "um":
                N_ = CFG["fechamento"]["nascer"]
                tn = t_ms - N_["inicio_ms"]
                fim = max(N_["sol_ms"], N_["numero_atraso_ms"] + N_["numero_ms"], N_["barra_ms"])
                e["nascer"] = None if tn < 0 else min(tn, fim)
                # no 1º o empurrão da seta não existe: o módulo só sai de trás da face (sem o +10 px)
                e["mx"] = min(e["mx"], 0.0)
        else:
            s = P["saida"]
            sp = P["sombra_projetada"]
            e = {"dx": kf(s["face_x"], saida_ms, E_EXIT), "rot": 0.0, "blur": kf(s["desfoque_px"], saida_ms, LIN),
                 "mx": kf(s["modulo_x"], saida_ms), "sy": sp["y"], "sa": sp["alfa"], "sda": P["sombra_dura"][1],
                 "brilho": None, "nascer": None}
        return e

    def camada(self, e):
        chave = tuple(round(v, 2) if isinstance(v, float) else v for v in
                      (e["dx"], e["rot"], e["blur"], e["mx"], e["sy"], e["sa"], e["sda"], e["brilho"], e["nascer"]))
        if chave in self.cache:
            return self.cache[chave]
        P = CFG["placa"]
        pad = self.PAD
        tela = np.zeros((self.hh + 2 * pad, self.fw + self.lado + 2 * pad, 4), np.float32)
        modulo = self.seta if self.tipo == "seta" else modulo_um(e["nascer"])
        mx = e["mx"]
        sobre(tela, deslocar(modulo, 0, mx - int(np.floor(mx))), pad + self.fw + int(np.floor(mx)), pad)
        face = self.face if e["brilho"] is None else self.brilho(e["brilho"])
        sobre(tela, face, pad, pad)
        if abs(e["rot"]) > 1e-3:
            tela = np.dstack([ndimage.rotate(tela[..., i], -e["rot"], reshape=False, order=1) for i in range(4)])
        if e["blur"] >= 1:
            tela = ndimage.uniform_filter1d(tela, size=int(round(e["blur"])), axis=1, mode="constant")
        a = tela[..., 3]
        sp = P["sombra_projetada"]
        sombra = sombra_objeto(a, (P["sombra_dura"][0], e["sda"]),
                               {"y": e["sy"], "blur": sp["blur"], "spread": sp["spread"], "alfa": e["sa"]})
        out = premult(np.zeros(a.shape + (3,), np.float32), sombra)
        sobre(out, tela)
        res = (out, int(round(P["x"] + e["dx"])) - pad, P["y"] - pad)
        if len(self.cache) > 400:
            self.cache.clear()
        self.cache[chave] = res
        return res

    def brilho(self, p):
        c = CFG["placa"]["chegada"]
        fw, hh = self.fw, self.hh
        bw = c["brilho_largura"] * fw
        cx = -bw + (fw + 2 * bw) * p
        yy, xx = np.mgrid[0:hh, 0:fw].astype(np.float32)
        xs = xx + (yy - hh / 2) * np.tan(np.radians(c["brilho_inclinacao_graus"]))
        perfil = np.clip(1 - np.abs(xs - cx) / (bw / 2), 0, 1) * c["brilho_alfa"]
        a = self.face[..., 3]
        rgb = np.where(a[..., None] > 0, self.face[..., :3] / np.maximum(a[..., None], 1e-6), 0)
        rgb = soft_light_branco(rgb, perfil * (a > 0))
        return premult(rgb, a)


# ---------------------------------------------------------------- legenda Padrão (sem destaque por padrão)

class Legenda:
    """Legenda Padrão do DS V2 (sem caixa). item: {texto, q0, q1}; entra como grupo (120 ms), sai subindo 6 px."""
    MARGEM = 60

    def __init__(self, item, pasta):
        L = CFG["legenda"]
        self.item = item
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S, pasta)
        lh = L["tamanho"] * L["entrelinha"]
        asc, desc = f.getmetrics()
        linhas = item["texto"].split("\n")
        topo = L["base_y"] - len(linhas) * lh
        self.linhas = linhas
        palavras = []
        esp = f.getlength(" ") / S
        for i, ln in enumerate(linhas):
            toks = ln.split()
            larg = [f.getlength(w) / S for w in toks]
            total = sum(larg) + esp * (len(toks) - 1)
            x = L["centro_x"] - total / 2
            ltop = topo + i * lh
            base_y = ltop + (lh - (asc + desc) / S) / 2 + asc / S
            for w, lw in zip(toks, larg):
                palavras.append({"w": w, "x": x, "larg": lw, "base_y": base_y})
                x += lw + esp
        m = self.MARGEM
        self.x0 = int(np.floor(min(p["x"] for p in palavras))) - m
        self.x1 = int(np.ceil(max(p["x"] + p["larg"] for p in palavras))) + m
        self.y0 = int(np.floor(topo)) - m
        self.y1 = int(np.ceil(L["base_y"])) + m
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        mk = mascara((cw * S, ch * S), lambda d: [d.text(((p["x"] - self.x0) * S, (p["base_y"] - self.y0) * S), p["w"],
                                                         font=f, fill=255, anchor="ls") for p in palavras])
        self.mk = reduzir(mk[..., None])[..., 0]
        self.ret = [min(p["x"] for p in palavras), topo, max(p["x"] + p["larg"] for p in palavras), L["base_y"]]
        ys, xs = np.nonzero(self.mk > 0.02)
        self.tinta = [self.x0 + xs.min(), self.y0 + ys.min(), self.x0 + xs.max() + 1, self.y0 + ys.max() + 1]
        self.chars_max = max(len(x) for x in linhas)

    def estado(self, k):
        it = self.item
        L = CFG["legenda"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        nsai = int(round(L["saida_ms"] / MS))
        se = E_IN((k - (it["q1"] - nsai) + 1) / (nsai + 1)) if k >= it["q1"] - nsai else 0.0
        t = (k - it["q0"] + 1) * MS
        op = E_OUT(t / L["grupo_ms"])
        dy = (1 - op) * L["palavra_sobe_px"]
        return op * (1 - se), dy - se * L["saida_sobe_px"]

    def camada(self, st):
        L = CFG["legenda"]
        op, dy = st
        m2 = deslocar(self.mk, dy) if abs(dy) > 1e-3 else self.mk
        sd, sdi = L["sombra_dura"], L["sombra_difusa"]
        s1 = deslocar(m2, sd[0]) * sd[1]
        s2 = ndimage.gaussian_filter(m2, sdi["blur"] / 2) * sdi["alfa"]
        sombra = (1 - (1 - s1) * (1 - s2)) * op
        out = premult(np.zeros(m2.shape + (3,), np.float32), sombra)
        sobre(out, premult(np.broadcast_to(RECIBO, m2.shape + (3,)), m2 * op))
        return out


# ---------------------------------------------------------------- scrim e grão

def scrim_alfa(h=H, y0=None, y1=None, alfa=None):
    S = CFG["scrim"]
    y0 = S["y0"] if y0 is None else y0
    y1 = S["y1"] if y1 is None else y1
    alfa = T["op_scrim"] if alfa is None else alfa
    y = np.arange(h, dtype=np.float32)
    return (np.clip((y - y0) / (y1 - y0), 0, 1) * alfa)[:, None, None]


def grao(k, h=H, w=W):
    """grão de 5% (blend overlay), novo a cada quadro, intensidade fixa (DS 4.5)."""
    G = CFG["grao"]
    rng = np.random.default_rng(G["semente"] + k)
    z = ndimage.gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), G["sigma_px"])
    z /= z.std()
    return np.clip(0.5 + 0.289 * z, 0, 1)[..., None]


def overlay_blend(b, n, op):
    o = np.where(b < 0.5, 2 * b * n, 1 - 2 * (1 - b) * (1 - n))
    return b + op * (o - b)


# ---------------------------------------------------------------- símbolo 1º sozinho (fechamento da REV2)

class Simbolo:
    """Símbolo 1º do bundle (pd-bundle.js, one()): '1' em papel, sol e barra em amarelo, com a assinatura Nascer
    (DS 4.3: o sol sobe de trás da linha do horizonte, a barra cresce, o '1' entra). Sombra da legenda Emocional do
    bundle (mesma posição, centro y 960)."""
    MARGEM = 60

    def __init__(self):
        F = CFG["fechamento"]
        self.S_ = F["simbolo"]
        self.N_ = F["nascer"]
        h = self.S_["altura"]
        self.lado = h + 2 * self.MARGEM
        # centro pela tinta do desenho (x 12–91, y 2–100 no viewBox 100), não pela caixa
        self.x0 = int(round(self.S_["centro_x"] - (self.MARGEM + 51.5 * h / 100)))
        self.y0 = int(round(self.S_["centro_y"] - (self.MARGEM + 51.0 * h / 100)))
        self.cache = {}
        self.fim = max(self.N_["sol_ms"], self.N_["numero_atraso_ms"] + self.N_["numero_ms"], self.N_["barra_ms"])

    def camada(self, t_ms):
        t_ms = min(max(t_ms, 0.0), self.fim)
        chave = round(t_ms, 1)
        if chave in self.cache:
            return self.cache[chave]
        S, N_ = SS, self.N_
        h, m, L = self.S_["altura"], self.MARGEM, self.lado
        k = h / 100 * S
        pt = lambda x, y: (m * S + x * k, m * S + y * k)  # noqa: E731
        p_sol = E_CIN(t_ms / N_["sol_ms"])
        cy = 17 + 30 * N_["sol_desloc_frac"] * (1 - p_sol)
        sol = mascara((L * S, L * S), lambda d: d.ellipse([*pt(76 - 15, cy - 15), *pt(76 + 15, cy + 15)], fill=255))
        sol[int(round(m * S + 43.5 * k)):] = 0   # nasce de trás da linha do horizonte (base da barra)
        p_bar = E_OUT(t_ms / N_["barra_ms"])
        barra = mascara((L * S, L * S), lambda d: d.rectangle([*pt(58.7, 38), *pt(58.7 + 34.5 * p_bar, 43.5)], fill=255)
                        if p_bar > 0 else None)
        tn = (t_ms - N_["numero_atraso_ms"]) / N_["numero_ms"]
        p_num = E_OUT(tn) if tn > 0 else 0.0
        dy = (1 - p_num) * N_["numero_sobe_px"] * S
        pts = [(26, 4), (48, 4), (48, 100), (26, 100), (26, 30), (12, 37), (12, 16)]
        num = mascara((L * S, L * S), lambda d: d.polygon([(x, y + dy) for x, y in (pt(*q) for q in pts)], fill=255))
        sol, barra, num = [reduzir(a[..., None])[..., 0] for a in (sol, barra, num)]
        num *= p_num
        amarelo = np.clip(sol + barra, 0, 1)
        forma = np.clip(amarelo + num, 0, 1)
        sb = self.S_["sombra"]
        sd, sdi = sb["dura"], sb["difusa"]
        s1 = deslocar(forma, sd[0]) * sd[1]
        s2 = ndimage.gaussian_filter(forma, sdi["blur"] / 2) * sdi["alfa"]
        out = premult(np.zeros(forma.shape + (3,), np.float32), 1 - (1 - s1) * (1 - s2))
        sobre(out, premult(np.broadcast_to(AMARELO, forma.shape + (3,)), amarelo))
        sobre(out, premult(np.broadcast_to(cor(self.S_["cor_numero"]), forma.shape + (3,)), num))
        self.cache[chave] = out
        ys, xs = np.nonzero(forma > 0.02)
        self.tinta = [self.x0 + int(xs.min()), self.y0 + int(ys.min()), self.x0 + int(xs.max()) + 1,
                      self.y0 + int(ys.max()) + 1] if len(xs) else None
        return out


# ---------------------------------------------------------------- módulo 1º sozinho (fechamento da REV3)

class Modulo1:
    """PD_placa_modulo_1 do kit do DS (6.1): módulo grafite 176 × 176 com o símbolo 1º (bundle one(): '1' em papel,
    sol e barra em amarelo, 70% do módulo). Entra com a Chegada (DS 2.1, mesmos keyframes da face da placa) em
    x 72 · y 640 e, assentado, o 1º nasce (DS 4.3 Nascer: sol sobe de trás da linha do horizonte em 700 ms
    ease-cinema, barra cresce em 300 ms, o '1' entra a 500 ms)."""
    PAD = 140

    def __init__(self):
        self.M = CFG["fechamento"]["modulo_1"]
        self.N_ = CFG["fechamento"]["nascer"]
        self.lado = self.M["lado"]
        self.cache = {}
        self.fim_nascer = max(self.N_["sol_ms"], self.N_["numero_atraso_ms"] + self.N_["numero_ms"], self.N_["barra_ms"])

    def _modulo(self, tn):
        L, S = self.lado, SS
        rgbm, mm = painel_modulo(L, L, (True, True, True, True))
        if tn is None or tn < 0:
            return premult(rgbm, mm)
        N_ = self.N_
        k = L * self.M["fracao"] / 100 * S
        o = (L - L * self.M["fracao"]) / 2 * S
        pt = lambda x, y: (o + x * k, o + y * k)  # noqa: E731
        cy = 17 + 30 * N_["sol_desloc_frac"] * (1 - E_CIN(tn / N_["sol_ms"]))
        sol = mascara((L * S, L * S), lambda d: d.ellipse([*pt(61, cy - 15), *pt(91, cy + 15)], fill=255))
        sol[int(round(o + 43.5 * k)):] = 0       # nasce de trás da linha do horizonte (a barra do ordinal)
        p_bar = E_OUT(tn / N_["barra_ms"])
        barra = mascara((L * S, L * S), lambda d: d.rectangle([*pt(58.7, 38), *pt(58.7 + 34.5 * p_bar, 43.5)], fill=255)
                        if p_bar > 0 else None)
        t1 = (tn - N_["numero_atraso_ms"]) / N_["numero_ms"]
        p_num = E_OUT(t1) if t1 > 0 else 0.0
        dy = (1 - p_num) * N_["numero_sobe_px"] * S
        pts = [(26, 4), (48, 4), (48, 100), (26, 100), (26, 30), (12, 37), (12, 16)]
        num = mascara((L * S, L * S), lambda d: d.polygon([(x, y + dy) for x, y in (pt(*q) for q in pts)], fill=255))
        sol, barra, num = [reduzir(a[..., None])[..., 0] for a in (sol, barra, num)]
        num = num * p_num
        am = np.clip(sol + barra, 0, 1)
        rgbm = rgbm * (1 - am[..., None]) + AMARELO * am[..., None]
        rgbm = rgbm * (1 - num[..., None]) + cor(self.M["cor_numero"]) * num[..., None]
        return premult(rgbm, mm)

    def estado(self, t_ms):
        c = CFG["placa"]["chegada"]
        tn = t_ms - self.M["nascer_inicio_ms"]
        return {"dx": kf(c["face_x"], t_ms), "rot": kf(c["rotacao"], t_ms), "blur": kf(c["desfoque_px"], t_ms, LIN),
                "sy": kf(c["sombra_y"], t_ms), "sa": kf(c["sombra_alfa"], t_ms), "sda": kf(c["sombra_dura_alfa"], t_ms),
                "nascer": None if tn < 0 else min(tn, self.fim_nascer)}

    def camada(self, e):
        chave = tuple(round(v, 2) if isinstance(v, float) else v for v in
                      (e["dx"], e["rot"], e["blur"], e["sy"], e["sa"], e["sda"], e["nascer"]))
        if chave in self.cache:
            return self.cache[chave]
        P = CFG["placa"]
        pad, L = self.PAD, self.lado
        tela = np.zeros((L + 2 * pad, L + 2 * pad, 4), np.float32)
        sobre(tela, self._modulo(e["nascer"]), pad, pad)
        if abs(e["rot"]) > 1e-3:
            tela = np.dstack([ndimage.rotate(tela[..., i], -e["rot"], reshape=False, order=1) for i in range(4)])
        if e["blur"] >= 1:
            tela = ndimage.uniform_filter1d(tela, size=int(round(e["blur"])), axis=1, mode="constant")
        a = tela[..., 3]
        sp = P["sombra_projetada"]
        sombra = sombra_objeto(a, (P["sombra_dura"][0], e["sda"]),
                               {"y": e["sy"], "blur": sp["blur"], "spread": sp["spread"], "alfa": e["sa"]})
        out = premult(np.zeros(a.shape + (3,), np.float32), sombra)
        sobre(out, tela)
        res = (out, int(round(self.M["x"] + e["dx"])) - pad, self.M["y"] - pad)
        self.cache[chave] = res
        return res
