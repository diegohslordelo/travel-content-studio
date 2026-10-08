"""REV2 do Reel teaser de Barcelona: reel_teaser_barcelona_rev2.mp4 (a REV1 com o câmbio real da viagem).

Teaser do vlog de Barcelona (YouTube, sábado 10/10/2026, 11h), no Design System V2.1 "Objetos do Primeiro Dia".
Ideia: 4 preços reais ditos no próprio vlog (cada um com a Etiqueta de valor) e, no fim, a placa CTA com o dia e a hora.
O motor de placa, legenda, scrim e grão é o mesmo da REV8 do Reel de apresentação (reels/apresentacao/rev8/scripts/rev8.py),
copiado para cá para este Reel não depender de outra pasta.

Etapas:
  1. tempos   : planos, legendas (início de cada palavra no master) e objetos
  2. objetos  : placas (hook e CTA), etiquetas de valor e legendas, em float (sRGB)
  3. audio    : som direto dos planos, emendas de 20 ms, −14 LUFS e pico ≤ −1 dBTP
  4. video    : master 4K HLG → crop 9:16 → tone mapping (o mesmo do Reel de apresentação) → grão → scrim → objetos
  5. qa       : testes técnicos, frames de QA, folha de contato, capa e relatorio_tecnico_rev2.json

Uso (de dentro de reels/teaser-barcelona/):
  python3 rev2/scripts/teaser.py --fontes PASTA_COM_AS_TTF [--master CAMINHO_DO_MASTER]
Fontes (SIL OFL, Google Fonts, https://raw.githubusercontent.com/google/fonts/main/ofl/...):
  barlow/Barlow-Bold.ttf · barlow/Barlow-Medium.ttf · barlowcondensed/BarlowCondensed-ExtraBold.ttf ·
  barlowcondensed/BarlowCondensed-SemiBold.ttf · barlowcondensed/BarlowCondensed-Bold.ttf · ibmplexmono/IBMPlexMono-Medium.ttf
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
CFG = json.load(open(os.path.join(REV, "rev2.json"), encoding="utf-8"))
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
SPF = SR // FPS
MS = 1000 / FPS
TMP = os.path.join(REV, "_tmp")
SAIDA = os.path.join(REV, CFG["saida"])
PREVIA = os.path.join(REV, CFG["saida_previa"])
CAPA = os.path.join(REV, CFG["capa"])
QA_DIR = os.path.join(REV, "qa_frames")
SS = 4  # supersampling dos objetos
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
T = CFG["tokens"]
SAFE = T["safe"]
FONTES = None

# HLG → SDR Rec.709: o mesmo tone mapping aprovado no Reel de apresentação (reels/apresentacao/scripts/render.py).
TONEMAP = (
    "zscale=w=1080:h=1920:f=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,"
    "format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:param=0.5:peak=4.93:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,eq=saturation=0.88,"
    "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb48le"
)


def cor(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO = cor(T["signal_500"])
AMARELO_300 = cor(T["signal_300"])
GRAFITE = cor(T["night_900"])
ASFALTO = cor(T["night_500"])
CONCRETO = cor(T["night_300"])
RECIBO = cor(T["paper_0"])


def rodar(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def q(t):
    return int(round(t * FPS))


def fonte(nome, px):
    return ImageFont.truetype(os.path.join(FONTES, nome), px)


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
E_IN = bezier([0.42, 0.0, 1.0, 1.0])  # 'ease-in' do CSS (saída da legenda)


def kf(chaves, t, curva=E_OUT):
    """valor dos keyframes [(ms, valor), …] no instante t (ms)."""
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- 1. linha do tempo

def planos():
    out, r = [], 0
    for p in CFG["planos"]:
        o0, o1 = q(p["origem"][0]), q(p["origem"][1])
        nf = q(p.get("congelar_s", 0))  # freeze frame no fim do plano (DS 4.5)
        v0 = q(p["video_origem"]) if "video_origem" in p else o0  # imagem de cobertura: vídeo de outro trecho
        out.append({**p, "o0": o0, "o1": o1, "v0": v0, "nf": nf, "r0": r, "r1": r + (o1 - o0) + nf})
        r += o1 - o0 + nf
    return out


PL = planos()
N = PL[-1]["r1"]


def plano_de(t):
    for p in PL:
        if p["o0"] / FPS <= t < p["o1"] / FPS:
            return p
    raise ValueError(f"{t} s não está em nenhum plano")


def rev(t):
    """tempo do master (s) → quadro do Reel."""
    p = plano_de(t)
    return p["r0"] + q(t) - p["o0"]


def tempos_legendas():
    L = CFG["legenda"]
    leg = []
    for item in CFG["legendas"]:
        x = {"texto": item["texto"]}
        if "palavras" in item:
            p = plano_de(item["palavras"][0])
            x["plano"] = p["n"]
            x["palavras_q"] = [rev(t) for t in item["palavras"]]
            x["q0"] = x["palavras_q"][0]
            n = len(item["texto"].replace("\n", " ").split())
            assert n == len(item["palavras"]), item["texto"]
            dur = item["palavras"][-1] - item["palavras"][0] + 0.3
            x["palavras_por_s"] = round(n / dur, 2)
            x["modo"] = "palavra" if x["palavras_por_s"] <= L["palavras_por_s_max_palavra_a_palavra"] else "grupo"
        else:
            p = next(pp for pp in PL if pp["n"] == item["plano"])
            x["plano"] = p["n"]
            x["q0"] = p["r0"] + q(item["de_plano"])
            x["modo"] = "grupo"
            x["palavras_por_s"] = None
        i = PL.index(p)
        while i + 1 < len(PL) and PL[i + 1]["o0"] == PL[i]["o1"]:  # fala contínua em planos seguidos (5 → 6)
            i += 1
        x["_r1"] = PL[i]["r1"]
        leg.append(x)
    for i, x in enumerate(leg):
        prox = leg[i + 1]["q0"] if i + 1 < len(leg) else N
        x["q1"] = min(prox, x.pop("_r1"))
        if x["modo"] == "palavra":
            assert all(x["q0"] <= k < x["q1"] for k in x["palavras_q"]), x
        x["de"], x["ate"] = round(x["q0"] / FPS, 3), round(x["q1"] / FPS, 3)
    return leg


# ---------------------------------------------------------------- 2. objetos (utilidades)

def reduzir(a, s=SS):
    h, w = a.shape[0] // s, a.shape[1] // s
    return a[:h * s, :w * s].reshape(h, s, w, s, -1).mean((1, 3))


def mascara(tam, desenho):
    im = Image.new("L", tam, 0)
    desenho(ImageDraw.Draw(im))
    return np.asarray(im, np.float32) / 255


def red1(m):
    return reduzir(m[..., None])[..., 0]


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
    """sombra de duas camadas: borda dura (y, alfa) + projetada (y, blur, spread, alfa). Preto."""
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


def texto_rastreado(d, x, y, txt, f, trk, fill=255, anchor="ls"):
    for c in txt:
        d.text((x, y), c, font=f, fill=fill, anchor=anchor)
        x += f.getlength(c) + trk


def largura_rastreada(txt, f, trk):
    return sum(f.getlength(c) for c in txt) + trk * (len(txt) - 1)


def soft_light_branco(b, a):
    d = np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
    return b * (1 - a[..., None]) + d * a[..., None]


# ---------------------------------------------------------------- placa (2 linhas, módulo de seta ou '?')

def caminho_seta(lado):
    """seta do bundle do DS (pd-bundle.js, viewBox 100): M8 41h50V18l38 32-38 32V59H8z, em 54% do módulo."""
    k = lado * CFG["placa"]["seta_fracao"] / 100
    ox = oy = (lado - lado * CFG["placa"]["seta_fracao"]) / 2
    pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
    return [(ox + x * k, oy + y * k) for x, y in pts]


class Placa:
    PAD = 150

    def __init__(self, spec):
        P = CFG["placa"]
        S = SS
        self.spec = spec
        fl = fonte(P["rotulo_fonte"], P["rotulo_px"] * S)
        trk_l = P["rotulo_tracking_em"] * P["rotulo_px"] * S
        larg_l = largura_rastreada(spec["rotulo"], fl, trk_l)
        px = P["destino_px"]
        while True:
            fd = fonte(P["destino_fonte"], px * S)
            trk_d = P["destino_tracking_em"] * px * S
            larg_d = largura_rastreada(spec["destino"], fd, trk_d)
            hh = round(2 * P["padding_v"] + P["rotulo_px"] + P["espaco_rotulo_destino"] + px * P["destino_entrelinha"])
            fw = int(round(2 * P["padding_h"] + max(larg_l, larg_d) / S))
            if fw + hh <= P["largura_max"] or px == P["destino_px_longo"]:
                break
            px = P["destino_px_longo"]
        assert fw + hh <= P["largura_max"], (spec, fw + hh)
        self.px_destino = px
        r = T["radius_plate"]
        m = mascara((fw * S, hh * S), lambda d: d.rounded_rectangle([0, 0, fw * S - 1, hh * S - 1], radius=r * S,
                                                                    fill=255, corners=(True, False, False, True)))
        i_, rr, lw = P["filete_inset"] * S, P["filete_raio"] * S, P["filete_px"] * S

        def filete(d):
            d.line([(fw * S - i_, i_ + lw / 2), (i_ + rr, i_ + lw / 2)], fill=255, width=lw)
            d.line([(fw * S - i_, hh * S - i_ - lw / 2), (i_ + rr, hh * S - i_ - lw / 2)], fill=255, width=lw)
            d.line([(i_ + lw / 2, i_ + rr), (i_ + lw / 2, hh * S - i_ - rr)], fill=255, width=lw)
            d.arc([i_, i_, i_ + 2 * rr, i_ + 2 * rr], 180, 270, fill=255, width=lw)
            d.arc([i_, hh * S - i_ - 2 * rr, i_ + 2 * rr, hh * S - i_], 90, 180, fill=255, width=lw)
        fil = mascara((fw * S, hh * S), filete)
        # linhas: caixa do rótulo (36/1) e do destino (128/0,9), texto centrado na caixa pela altura de maiúscula
        y_l = P["padding_v"] * S
        cap_l = -fl.getbbox("H", anchor="ls")[1]
        base_l = y_l + (P["rotulo_px"] * S - cap_l) / 2 + cap_l
        y_d = y_l + (P["rotulo_px"] + P["espaco_rotulo_destino"]) * S
        cap_d = -fd.getbbox("H", anchor="ls")[1]
        lh_d = px * P["destino_entrelinha"] * S
        base_d = y_d + (lh_d - cap_d) / 2 + cap_d
        x0 = P["padding_h"] * S
        txt = mascara((fw * S, hh * S), lambda d: (texto_rastreado(d, x0, base_l, spec["rotulo"], fl, trk_l),
                                                   texto_rastreado(d, x0, base_d, spec["destino"], fd, trk_d)))
        rb, rx, ry = P["rebite_px"] * S, P["rebite_x"] * S, P["rebite_y"] * S
        reb = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx, y, rx + rb, y + rb], fill=255)
                                                    for y in (ry, hh * S - ry - rb)])
        luz = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx + rb * .22, y + rb * .18, rx + rb * .52, y + rb * .48],
                                                             fill=255) for y in (ry, hh * S - ry - rb)])
        m, fil, txt, reb, luz = [red1(a) for a in (m, fil, txt, reb, luz)]
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
        self.face = premult(rgb, m)
        # módulo: quadrado com lado = altura da placa
        lado = hh
        mm = mascara((lado * S, hh * S), lambda d: d.rounded_rectangle([0, 0, lado * S - 1, hh * S - 1], radius=r * S,
                                                                       fill=255, corners=(False, True, True, False)))
        caixa = lado * P["seta_fracao"]
        cx0 = (lado - caixa) / 2
        if spec["modulo"] == "seta":
            glifo = mascara((lado * S, hh * S), lambda d: d.polygon([(x * S, y * S) for x, y in caminho_seta(lado)],
                                                                    fill=255))
        else:  # '?' do bundle: Barlow Condensed 800, font-size 128 num viewBox 100, base em y 94, centrado
            fq = fonte(P["destino_fonte"], int(round(1.28 * caixa * S)))
            glifo = mascara((lado * S, hh * S), lambda d: d.text(((cx0 + caixa / 2) * S, (cx0 + 0.94 * caixa) * S),
                                                                 spec["modulo"], font=fq, fill=255, anchor="ms"))
        mm, glifo = red1(mm), red1(glifo)
        rgbm = np.broadcast_to(GRAFITE, mm.shape + (3,)).copy()
        borda = np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07
        topo_m = np.clip(mm - deslocar(mm, 2), 0, 1) * 0.08
        for camada in (borda, topo_m):
            rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
        rgbm = rgbm * (1 - glifo[..., None]) + AMARELO * glifo[..., None]
        self.modulo = premult(rgbm, mm)
        self.fw, self.hh, self.lado = fw, hh, lado
        self.medidas = {"face_largura": fw, "modulo_lado": lado, "altura": hh, "largura_total": fw + lado,
                        "rotulo_px": P["rotulo_px"], "destino_px": px,
                        "rotulo_avanco_px": round(larg_l / S, 1), "destino_avanco_px": round(larg_d / S, 1)}
        self.cache = {}

    def estado(self, t_ms=None, saida_ms=None):
        P = CFG["placa"]
        if saida_ms is None:
            c = P["chegada"]
            mxk = [(t, v * self.lado if -1 <= v < 0 else v) for t, v in c["modulo_x"]]
            e = {"dx": kf(c["face_x"], t_ms), "rot": kf(c["rotacao"], t_ms), "blur": kf(c["desfoque_px"], t_ms, LIN),
                 "mx": kf(mxk, t_ms), "sy": kf(c["sombra_y"], t_ms), "sa": kf(c["sombra_alfa"], t_ms),
                 "sda": kf(c["sombra_dura_alfa"], t_ms), "brilho": None}
            b0, b1 = c["brilho_ms"]
            if b0 <= t_ms <= b1:
                e["brilho"] = E_CIN((t_ms - b0) / (b1 - b0))
        else:
            s = P["saida"]
            sp = P["sombra_projetada"]
            e = {"dx": kf(s["face_x"], saida_ms, E_EXIT), "rot": 0.0, "blur": kf(s["desfoque_px"], saida_ms, LIN),
                 "mx": kf(s["modulo_x"], saida_ms), "sy": sp["y"], "sa": sp["alfa"], "sda": P["sombra_dura"][1],
                 "brilho": None}
        return e

    def camada(self, e):
        chave = tuple(round(v, 2) if isinstance(v, float) else v for v in
                      (e["dx"], e["rot"], e["blur"], e["mx"], e["sy"], e["sa"], e["sda"], e["brilho"]))
        if chave in self.cache:
            return self.cache[chave]
        P = CFG["placa"]
        pad = self.PAD
        tela = np.zeros((self.hh + 2 * pad, self.fw + self.lado + 2 * pad, 4), np.float32)
        mx = e["mx"]
        sobre(tela, deslocar(self.modulo, 0, mx - int(np.floor(mx))), pad + self.fw + int(np.floor(mx)), pad)
        face = self.brilho(e["brilho"]) if e["brilho"] is not None else self.face
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
        if len(self.cache) < 400:
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

    def ret(self, e):
        P = CFG["placa"]
        x = P["x"] + e["dx"]
        return [round(x, 1), P["y"], round(x + self.fw + self.lado, 1), P["y"] + self.hh]


# ---------------------------------------------------------------- etiqueta de valor

class Etiqueta:
    def __init__(self, spec):
        E = CFG["etiqueta"]
        S = SS
        self.spec = spec
        fr = fonte(E["rotulo_fonte"], E["rotulo_px"] * S)
        trk = E["rotulo_tracking_em"] * E["rotulo_px"] * S
        fn = ImageFont.truetype(os.path.join(FONTES, E["numero_fonte"]), E["numero_px"] * S)
        fb = fonte(E["brl_fonte"], E["brl_px"] * S)
        self.num = f"€ {spec['eur']}"
        self.brl = f"≈ R$ {spec['brl']}"
        pt, pr, pb, pl = E["padding"]
        lr = largura_rastreada(spec["rotulo"], fr, trk) / S
        ln = fn.getlength(self.num, features=["tnum"]) / S
        lb = fb.getlength(self.brl) / S
        w = int(np.ceil(pl + max(lr, ln + E["espaco_numero_brl"] + lb) + pr))
        h = int(round(pt + E["rotulo_px"] + E["espaco_rotulo_numero"] + E["numero_px"] + pb))
        self.w, self.h = w, h
        cap_r = -fr.getbbox("H", anchor="ls")[1] / S
        base_r = pt + (E["rotulo_px"] - cap_r) / 2 + cap_r
        cap_n = -fn.getbbox("8", anchor="ls")[1] / S
        y_n = pt + E["rotulo_px"] + E["espaco_rotulo_numero"]
        base_n = y_n + (E["numero_px"] - cap_n) / 2 + cap_n
        self.caixa_num = (pl, y_n, pl + ln, y_n + E["numero_px"])
        m = 40  # margem para a sombra
        cw, ch = w + 2 * m, h + 2 * m
        self.m = m
        corpo = mascara((cw * S, ch * S), lambda d: d.rounded_rectangle(
            [m * S, m * S, (m + w) * S - 1, (m + h) * S - 1], radius=T["radius_paper"] * S, fill=255))
        furos = mascara((cw * S, ch * S), lambda d: [d.ellipse(
            [(m + x - E["picote_furo"] / 2) * S, (m + E["picote_y"] - E["picote_furo"] / 2) * S,
             (m + x + E["picote_furo"] / 2) * S, (m + E["picote_y"] + E["picote_furo"] / 2) * S], fill=255)
            for x in np.arange(E["picote_passo"] / 2, w, E["picote_passo"])])
        rot = mascara((cw * S, ch * S), lambda d: texto_rastreado(d, (m + pl) * S, (m + base_r) * S, spec["rotulo"],
                                                                  fr, trk))
        brl = mascara((cw * S, ch * S), lambda d: d.text(((m + pl + ln + E["espaco_numero_brl"]) * S, (m + base_n) * S),
                                                         self.brl, font=fb, fill=255, anchor="ls"))
        numero = mascara((cw * S, ch * S), lambda d: d.text(((m + pl) * S, (m + base_n) * S), self.num, font=fn,
                                                            fill=255, anchor="ls", features=["tnum"]))
        corpo, furos, rot, brl, numero = [red1(a) for a in (corpo, furos, rot, brl, numero)]
        rgb = np.broadcast_to(RECIBO, corpo.shape + (3,)).copy()
        rgb *= (1 - T["op_fiber"] * ruido_fractal(*corpo.shape, 11))[..., None]
        for msk, c in ((furos, CONCRETO), (rot, ASFALTO), (brl, ASFALTO)):
            rgb = rgb * (1 - msk[..., None]) + c * msk[..., None]
        s1, s2 = E["sombra"]
        sombra = sombra_objeto(corpo, (s1["y"], s1["alfa"]), s2)
        base = premult(np.zeros(corpo.shape + (3,), np.float32), sombra)
        sobre(base, premult(rgb, corpo))
        self.base = base
        self.numero = numero
        self.cw, self.ch = cw, ch
        self.cache = {}

    def camada(self, rolo):
        """rolo: 0 → 1 (Giro do número: sobe de baixo para o lugar, de amarelo 300 para grafite)."""
        chave = round(rolo, 3)
        if chave in self.cache:
            return self.cache[chave]
        img = self.base.copy()
        x0, y0, x1, y1 = self.caixa_num
        m = self.m
        dy = (1 - rolo) * (y1 - y0)
        nm = deslocar(self.numero, dy) if dy > 1e-3 else self.numero
        clip = np.zeros_like(nm)
        clip[int(m + y0 - 6):int(np.ceil(m + y1 + 6)), :] = 1
        nm = nm * clip
        c = AMARELO_300 * (1 - rolo) + GRAFITE * rolo
        sobre(img, premult(np.broadcast_to(c, nm.shape + (3,)), nm))
        self.cache[chave] = img
        return img


# ---------------------------------------------------------------- legendas (DS 3.2 Padrão, igual à REV8)

def segmentos(linha):
    partes = re.split(r"(\*[^*]+\*)", linha)
    return [(p.strip("*"), p.startswith("*")) for p in partes if p]


class Legenda:
    MARGEM = 60

    def __init__(self, item):
        L = CFG["legenda"]
        self.item = item
        texto = item["texto"]
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S)
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
            x = L["centro_x"] - total / 2  # centro do canvas (CLAUDE.md, seção 12)
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
        self.mascaras, self.destaques = [], {}
        for j, p in enumerate(palavras):
            if not p["hl"]:
                mk = mascara((cw * S, ch * S), lambda d, p=p: d.text(((p["x"] - self.x0) * S, (p["base_y"] - self.y0) * S),
                                                                     p["w"], font=f, fill=255, anchor="ls"))
                self.mascaras.append(red1(mk))
            else:
                self.mascaras.append(None)
                self.destaques[j] = self.mini_placa(p, f)
        self.ret = [min(p["x"] for p in palavras), topo, max(p["x"] + p["larg"] for p in palavras), L["base_y"]]
        self.chars_max = max(len(x) for x in self.linhas)

    def mini_placa(self, p, f):
        L = CFG["legenda"]
        D = L["destaque"]
        P = CFG["placa"]
        S = SS
        lh = L["tamanho"] * L["entrelinha"]
        bx0, by0 = p["x"], p["ltop"] - D["padding_v"]
        bw, bh = p["larg"], lh + 2 * D["padding_v"]
        m = 40
        cw, ch = int(np.ceil(bw)) + 2 * m, int(np.ceil(bh)) + 2 * m
        ox, oy = int(np.floor(bx0)) - m, int(np.floor(by0)) - m
        fx, fy = bx0 - ox, by0 - oy
        caixa = mascara((cw * S, ch * S), lambda d: d.rounded_rectangle(
            [fx * S, fy * S, (fx + bw) * S - 1, (fy + bh) * S - 1], radius=T["radius_tag"] * S, fill=255))
        txt = mascara((cw * S, ch * S), lambda d: d.text(((fx + D["padding_h"]) * S, (p["base_y"] - oy) * S), p["w"],
                                                         font=f, fill=255, anchor="ls"))
        caixa, txt = red1(caixa), red1(txt)
        rgb = np.broadcast_to(AMARELO, caixa.shape + (3,)).copy()
        bl, ba = P["bevel_luz"]
        bs, bsa = P["bevel_sombra"]
        topo = np.clip(caixa - deslocar(caixa, bl), 0, 1) * ba
        base = np.clip(caixa - deslocar(caixa, -bs), 0, 1) * bsa
        rgb = rgb * (1 - topo[..., None]) + topo[..., None]
        rgb = rgb * (1 - base[..., None])
        rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
        sombra = sombra_objeto(caixa, D["sombra_dura"], D["sombra_projetada"])
        out = premult(np.zeros(caixa.shape + (3,), np.float32), sombra)
        sobre(out, premult(rgb, caixa))
        return {"img": out, "x": ox, "y": oy, "cx": fx + bw / 2, "cy": fy + bh / 2}

    def estado(self, k):
        it = self.item
        L = CFG["legenda"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        nsai = int(round(L["saida_ms"] / MS))
        se = 0.0
        if it["q1"] < N and k >= it["q1"] - nsai:
            se = E_IN((k - (it["q1"] - nsai) + 1) / (nsai + 1))
        ws = []
        for j, p in enumerate(self.palavras):
            if it["modo"] == "palavra":
                kq = it["palavras_q"][j]
                dur = L["destaque"]["opacidade_ms"] if p["hl"] else L["palavra_ms"]
            else:
                kq = it["q0"]
                dur = L["grupo_ms"]
            if k < kq:
                ws.append((0.0, 0.0, 1.0))
                continue
            t = (k - kq + 1) * MS
            op = E_OUT(t / dur)
            dy = (1 - E_OUT(t / dur)) * L["palavra_sobe_px"]
            esc = 1.0
            if p["hl"]:
                dy = 0.0
                kh = it["palavras_q"][j] if "palavras_q" in it else it["q0"]
                # no grupo inteiro a mini-placa entra com o grupo e pula quando o número é dito (DS 3.2 Destaque)
                esc = 1.0 if k < kh else kf(L["destaque"]["pop"], (k - kh + 1) * MS, E_ARR)
            ws.append((op * (1 - se), dy - se * L["saida_sobe_px"], esc))
        return ws

    def camada(self, ws):
        L = CFG["legenda"]
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        sombra = np.zeros((ch, cw), np.float32)
        texto = np.zeros((ch, cw, 4), np.float32)
        sd, sdi = L["sombra_dura"], L["sombra_difusa"]
        for j, (op, dy, esc) in enumerate(ws):
            mk = self.mascaras[j]
            if mk is None or op <= 0:
                continue
            m2 = deslocar(mk, dy) if abs(dy) > 1e-3 else mk
            s1 = deslocar(m2, sd[0]) * sd[1]
            s2 = ndimage.gaussian_filter(m2, sdi["blur"] / 2) * sdi["alfa"]
            s = 1 - (1 - s1) * (1 - s2)
            sombra = 1 - (1 - sombra) * (1 - s * op)
            sobre(texto, premult(np.broadcast_to(RECIBO, m2.shape + (3,)), m2 * op))
        out = premult(np.zeros((ch, cw, 3), np.float32), sombra)
        sobre(out, texto)
        for j, d in self.destaques.items():
            op, dy, esc = ws[j]
            if op <= 0:
                continue
            img = d["img"]
            if abs(esc - 1) > 1e-3:
                cy, cx = d["cy"], d["cx"]
                mat = np.array([[1 / esc, 0], [0, 1 / esc]])
                off = np.array([cy, cx]) - mat @ np.array([cy, cx])
                img = np.dstack([ndimage.affine_transform(img[..., i], mat, offset=off, order=1) for i in range(4)])
            img = img * op
            if abs(dy) > 1e-3:
                img = deslocar(img, dy)
            sobre(out, img, d["x"] - self.x0, d["y"] - self.y0)
        return out


# ---------------------------------------------------------------- linha do tempo dos objetos

def linhas_placas():
    """quadros de cada placa: Chegada no 1º quadro do plano; saída de 240 ms terminando no corte (se houver)."""
    out = []
    n_sai = int(round(CFG["placa"]["saida"]["duracao_ms"] / MS))
    for spec in CFG["placas"]:
        p = next(pp for pp in PL if pp["n"] == spec["plano"])
        out.append({"spec": spec, "q0": p["r0"], "q1": p["r1"], "n_sai": n_sai if spec["saida"] else 0})
    return out


def estado_placa(lp, placa, k):
    if not (lp["q0"] <= k < lp["q1"]):
        return None
    if lp["n_sai"] and k >= lp["q1"] - lp["n_sai"]:
        return ("saida", (k - (lp["q1"] - lp["n_sai"]) + 1) * CFG["placa"]["saida"]["duracao_ms"] / lp["n_sai"])
    return ("chegada", (k - lp["q0"] + 1) * MS)


def linhas_etiquetas():
    out = []
    n_sai = int(round(T["dur_base"] / MS))
    for spec in CFG["etiquetas"]:
        p = next(pp for pp in PL if pp["n"] == spec["plano"])
        k0 = rev(spec["entra_origem"])
        assert p["r0"] <= k0 < p["r1"] - n_sai
        out.append({"spec": spec, "q0": k0, "q1": p["r1"], "n_sai": n_sai})
    return out


def estado_etiqueta(le, k):
    """(dx, opacidade, rolo) da etiqueta no quadro k: entra da esquerda (160 ms, ease-out), número gira (240 ms),
    sai pela direita (240 ms, ease-exit) terminando no corte."""
    if not (le["q0"] <= k < le["q1"]):
        return None
    E = CFG["etiqueta"]
    t = (k - le["q0"] + 1) * MS
    a = E_OUT(t / T["dur_fast"])
    dx = (1 - a) * E["entrada_dx"]
    op = a
    rolo = E_OUT(t / T["dur_base"])
    if k >= le["q1"] - le["n_sai"]:
        s = E_EXIT((k - (le["q1"] - le["n_sai"]) + 1) / le["n_sai"])
        dx = s * E["saida_dx"]
        op = 1 - s
    return dx, op, rolo


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


def compor(obj, scrim, base_rgb, k, registro, com_grao=True):
    img = overlay_blend(base_rgb, grao(k), T["op_grain"]) if com_grao else base_rgb
    img = img * (1 - scrim) + GRAFITE * scrim
    camada = np.zeros((H, W, 4), np.float32)
    els = []
    for le, et in obj["etiquetas"]:
        st = estado_etiqueta(le, k)
        if st is None:
            continue
        dx, op, rolo = st
        im = et.camada(rolo) * op
        x = int(round(CFG["etiqueta"]["x"] + dx)) - et.m
        y = CFG["etiqueta"]["base_y"] - et.h - et.m
        if le["spec"].get("lado") == "direita":  # DS 1.3: objeto no lado oposto ao rosto
            x = int(round(SAFE["x1"] - et.w + dx)) - et.m
        sobre(camada, im, x, y)
        els.append(("etiqueta", x + et.m, y + et.m, x + et.m + et.w, y + et.m + et.h, round(op, 3)))
    for lp, pl in obj["placas"]:
        st = estado_placa(lp, pl, k)
        if st is None:
            continue
        e = pl.estado(st[1]) if st[0] == "chegada" else pl.estado(saida_ms=st[1])
        im, x, y = pl.camada(e)
        sobre(camada, im, x, y)
        els.append(("placa:" + lp["spec"]["nome"], *pl.ret(e), st[0], round(st[1], 1)))
    for lg in obj["legendas"]:
        ws = lg.estado(k)
        if ws is None:
            continue
        sobre(camada, lg.camada(ws), lg.x0, lg.y0)
        els.append(("legenda", *[round(v, 1) for v in lg.ret], lg.item["texto"].replace("*", ""),
                    round(max(o for o, _, _ in ws), 3)))
    registro[k] = els
    a = camada[..., 3:4]
    return img * (1 - a) + camada[..., :3]


# ---------------------------------------------------------------- 3. áudio

def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1)))


def montar_audio(master):
    A = CFG["audio"]
    h = int(A["crossfade_ms"] * SR / 2000)
    mix = np.zeros((N * SPF, 2), np.float64)
    for i, p in enumerate(PL):
        # emendas de 20 ms só entre trechos diferentes do master (plano 5 → 6 é a mesma fala, sem emenda)
        ha = h if i > 0 and PL[i - 1]["o1"] != p["o0"] else 0
        hb = h if i < len(PL) - 1 and PL[i + 1]["o0"] != p["o1"] else 0
        ini = p["o0"] / FPS - ha / SR
        n = (p["o1"] - p["o0"] + p["nf"]) * SPF + ha + hb
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ini:.6f}", "-i", master, "-map", "0:a", "-t",
                            f"{n / SR + 0.05:.6f}", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                           capture_output=True, check=True)
        tr = np.frombuffer(r.stdout, np.float32).reshape(-1, 2)[:n].astype(np.float64)
        assert len(tr) == n, (p["n"], len(tr), n)
        env = np.ones(n)
        if ha:
            env[:2 * ha] = np.sin(np.linspace(0, np.pi / 2, 2 * ha))
        if hb:
            env[-2 * hb:] = np.cos(np.linspace(0, np.pi / 2, 2 * hb))
        if p["nf"]:  # no freeze o som do master continua e some em 250 ms
            i0 = ha + (p["o1"] - p["o0"]) * SPF
            nfd = int(0.25 * SR)
            env[i0:i0 + nfd] *= np.cos(np.linspace(0, np.pi / 2, nfd))
            env[i0 + nfd:] = 0
        g = 0.0 if p["audio"] == "mudo" else 1.0
        r0 = p["r0"] * SPF
        mix[r0 - ha:r0 - ha + n] += tr * env[:, None] * g
    dc = int(A["declique_ms"] * SR / 1000)
    rampa = np.linspace(0, 1, dc, endpoint=False)
    mix[:dc] *= rampa[:, None]
    mix[-dc:] *= rampa[::-1][:, None]
    bruto = os.path.join(TMP, "audio_bruto.wav")
    escrever_wav(bruto, mix)
    lufs, tp = ebur128(bruto)
    ganho = A["lufs_alvo"] - lufs
    final = os.path.join(TMP, "audio_final.wav")
    limite = A["pico_max_dbtp"] - 0.5
    for _ in range(6):
        rodar(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af",
               f"volume={ganho:.3f}dB,aresample=192000,alimiter=limit={10 ** (limite / 20):.5f}:attack=1:release=60:"
               f"level=disabled,aresample={SR}", "-c:a", "pcm_f32le", final])
        l2, tp2 = ebur128(final)
        if abs(l2 - A["lufs_alvo"]) <= 0.3 and tp2 <= A["pico_max_dbtp"] - 0.3:
            break
        ganho += A["lufs_alvo"] - l2
        if tp2 > A["pico_max_dbtp"] - 0.3:
            limite -= 0.5
    return final, {"bruto_lufs": lufs, "bruto_pico_dbtp": tp, "ganho_db": round(ganho, 2), "limitador_dbfs": limite,
                   "wav_lufs": l2, "wav_pico_dbtp": tp2}


def escrever_wav(arq, x):
    raw = os.path.join(TMP, "tmp.f32")
    x.astype(np.float32).tofile(raw)
    rodar(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", 2, "-i", raw, "-c:a", "pcm_f32le", arq])
    os.remove(raw)


# ---------------------------------------------------------------- 4. vídeo

def filtro_crop(p, fw=3840, fh=2160):
    zoom = float(p.get("zoom", 1.0))
    k = int(min(fw / 9, fh / 16) / zoom) // 2 * 2
    cw, ch = 9 * k, 16 * k

    def pos(centro, total, lado):
        return int(round(min(max(centro * total - lado / 2, 0), total - lado) / 2)) * 2
    y = pos(float(p.get("centro_y", 0.5)), fh, ch)
    x0 = pos(float(p["centro_x"]), fw, cw)
    n = p["o1"] - p["o0"]
    if "centro_x_fim" in p:
        x1 = pos(float(p["centro_x_fim"]), fw, cw)
        x = f"'{x0}+({x1 - x0})*min(n/{n},1)'"
    else:
        x = str(x0)
    crop = f"crop=w={cw}:h={ch}:x={x}:y={y}"
    if "delogo" in p:  # apaga uma tag gráfica antiga queimada no master (não é imagem da cena)
        dx, dy, dw, dh = p["delogo"]
        crop = f"delogo=x={dx}:y={dy}:w={dw}:h={dh}," + crop
    return crop


def decodificar(master, p):
    n = p["o1"] - p["o0"]
    return subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{p['v0'] / FPS:.6f}", "-i", master, "-map", "0:v",
                             "-vf", f"{filtro_crop(p)},{TONEMAP}", "-frames:v", str(n), "-f", "rawvideo",
                             "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)


def objetos():
    return {"placas": [(lp, Placa(lp["spec"])) for lp in linhas_placas()],
            "etiquetas": [(le, Etiqueta(le["spec"])) for le in linhas_etiquetas()],
            "legendas": [Legenda(x) for x in tempos_legendas()]}


def montar_video(master, obj, wav):
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", SAIDA]], stdin=subprocess.PIPE)
    scrim = scrim_alfa()
    registro = {}
    tam = W * H * 3 * 2
    k = 0
    for p in PL:
        dec = decodificar(master, p)
        for i in range(p["o1"] - p["o0"] + p["nf"]):
            if i < p["o1"] - p["o0"]:  # nos quadros de freeze repete o último quadro do plano
                buf = dec.stdout.read(tam)
                assert len(buf) == tam, f"quadro {k} incompleto"
                base = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
            out = compor(obj, scrim, base, k, registro)
            enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
            if k % 48 == 0:
                print(f"   quadro {k}/{N}", flush=True)
            k += 1
        dec.stdout.close()
        assert dec.wait() == 0
    enc.stdin.close()
    assert enc.wait() == 0 and k == N
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
           "-crf", 24, "-preset", "slow", "-pix_fmt", "yuv420p", *TAGS_COR, "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", PREVIA])
    return registro


# ---------------------------------------------------------------- capa

def capa(master, obj):
    """Capa 1080 × 1920: quadro do gancho com a placa Hook parada (estática: brilho congelado a 30% do percurso).
    Texto só o da placa (3 palavras), dentro da área 3:4 do grid (y 240–1680)."""
    C = CFG["capa_quadro"]
    p = next(pp for pp in PL if pp["n"] == C["plano"])
    pc = {**p, "v0": p["v0"] + C["quadro_no_plano"], "o0": p["o0"] + C["quadro_no_plano"], "o1": p["o0"] + C["quadro_no_plano"] + 1}
    pc.pop("centro_x_fim", None)
    if "centro_x_fim" in p:
        f = C["quadro_no_plano"] / (p["o1"] - p["o0"])
        pc["centro_x"] = p["centro_x"] + (p["centro_x_fim"] - p["centro_x"]) * f
    dec = decodificar(master, pc)
    buf = dec.stdout.read(W * H * 6)
    dec.stdout.close()
    dec.wait()
    base = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
    img = overlay_blend(base, grao(0), T["op_grain"])
    lp, pl = next((lp, pl) for lp, pl in obj["placas"] if lp["spec"]["nome"] == "hook")
    e = pl.estado(10_000)
    e["brilho"] = 0.30
    camada = np.zeros((H, W, 4), np.float32)
    im, x, y = pl.camada(e)
    sobre(camada, im, x, y)
    img = img * (1 - camada[..., 3:4]) + camada[..., :3]
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(CAPA, quality=93)


# ---------------------------------------------------------------- 5. QA

def ffprobe(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json",
                        arq], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def qa(obj, registro, info_audio):
    R = {"arquivo": os.path.basename(SAIDA)}
    pr = ffprobe(SAIDA)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "esperado": N, "duracao_video_s": float(v["duration"]),
                    "duracao_audio_s": float(a["duration"]), "codec_video": f"{v['codec_name']} ({v.get('profile')})",
                    "cor": f"{v.get('color_primaries')}/{v.get('color_transfer')}/{v.get('color_space')}/{v.get('color_range')}",
                    "codec_audio": f"{a['codec_name']} ({a.get('profile')})", "sr_audio": int(a["sample_rate"]),
                    "tamanho_bytes": int(pr["format"]["size"])}
    R["previa"] = {"arquivo": os.path.basename(PREVIA), "tamanho_bytes": os.path.getsize(PREVIA)}
    lufs, tp = ebur128(SAIDA)
    R["audio"] = {"lufs_integrado": lufs, "pico_verdadeiro_dbtp": tp, **info_audio}
    # zona segura (objetos parados) e sobreposições
    fora, sobrep = [], []
    for k in range(N):
        els = registro[k]
        for e in els:
            nome, x0, y0, x1, y1 = e[:5]
            parado = True
            if nome.startswith("placa"):
                parado = e[5] == "chegada" and e[6] >= 400
            if nome == "etiqueta":
                parado = e[5] >= 0.999
            if parado and (x0 < SAFE["x0"] - 0.5 or x1 > SAFE["x1"] + 0.5 or y0 < SAFE["y0"] or y1 > SAFE["y1"]):
                fora.append((k, *e[:5]))
        caixas = [e for e in els if e[0] != "legenda"]
        for e in els:
            if e[0] == "legenda":
                for c in caixas:
                    if e[2] < c[4] and c[2] < e[4] and e[1] < c[3] and c[1] < e[3]:
                        sobrep.append((k, c[0], e[5]))
    R["objetos"] = {
        "placas": {lp["spec"]["nome"]: {**pl.medidas, "x": CFG["placa"]["x"], "y": CFG["placa"]["y"],
                                         "x_final": CFG["placa"]["x"] + pl.medidas["largura_total"],
                                         "y_final": CFG["placa"]["y"] + pl.medidas["altura"],
                                         "quadros": [lp["q0"], lp["q1"]]} for lp, pl in obj["placas"]},
        "etiquetas": [{"rotulo": le["spec"]["rotulo"], "valor": f"{et.num} {et.brl}", "w": et.w, "h": et.h,
                       "x": SAFE["x1"] - et.w if le["spec"].get("lado") == "direita" else CFG["etiqueta"]["x"],
                       "y": CFG["etiqueta"]["base_y"] - et.h, "lado": le["spec"].get("lado", "esquerda"),
                       "quadros": [le["q0"], le["q1"]], "entra_s": round(le["q0"] / FPS, 3)}
                      for le, et in obj["etiquetas"]],
        "n_fora_da_zona_segura_parado": len(fora), "fora_da_zona_segura_parado": fora[:10],
        "n_legenda_sobre_objeto": len(sobrep), "legenda_sobre_objeto": sobrep[:10]}
    leg = obj["legendas"]
    R["textos"] = {"legendas": [lg.linhas for lg in leg], "max_caracteres_linha": max(lg.chars_max for lg in leg),
                   "max_linhas": max(len(lg.linhas) for lg in leg),
                   "topo_min_bloco_y": round(min(lg.topo for lg in leg), 1),
                   "mini_placas": [p["w"] for lg in leg for p in lg.palavras if p["hl"]]}
    R["legendas"] = [{k: lg.item.get(k) for k in ("texto", "plano", "de", "ate", "q0", "q1", "modo", "palavras_por_s",
                                                   "palavras_q")} for lg in leg]
    R["planos"] = [{"n": p["n"], "cena": p["cena"], "origem_s": p["origem"], "quadros_origem": [p["o0"], p["o1"]],
                    "reel_s": [round(p["r0"] / FPS, 3), round(p["r1"] / FPS, 3)], "audio": p["audio"],
                    "freeze_s": round(p["nf"] / FPS, 3),
                    "crop_centro_x": p["centro_x"], "video_origem_s": p.get("video_origem"),
                    "delogo": p.get("delogo")} for p in PL]
    luma = quadros_cinza(SAIDA).mean(axis=(1, 2))
    R["video"] = {"quadros_pretos": int((luma < 16).sum()), "luma_media_min": round(float(luma.min()), 1),
                  "cortes_s": [round(p["r0"] / FPS, 3) for p in PL[1:]]}
    return R


def quadros_cinza(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", "scale=270:480:flags=area", "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, 480, 270).astype(np.float32)


def frames_qa():
    shutil.rmtree(QA_DIR, ignore_errors=True)
    os.makedirs(QA_DIR)
    alvos = []
    for p in PL:
        for f, nome in ((0.0, "ini"), (0.5, "meio"), (0.97, "fim")):
            k = min(p["r0"] + int(f * (p["r1"] - p["r0"])), p["r1"] - 1)
            alvos.append((f"p{p['n']}_{nome}", k))
    for le in linhas_etiquetas():
        alvos.append((f"etiqueta_p{le['spec']['plano']}", min(le["q0"] + 8, le["q1"] - 7)))
    alvos.append(("placa_hook_assentada", 12))
    lista = []
    for nome, k in alvos:
        arq = os.path.join(QA_DIR, f"rev2_{nome}_quadro{k:03d}.jpg")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1, "-q:v", 2, arq])
        lista.append((nome, k, arq))
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    folha = Image.new("RGB", (cols * cw, ((len(lista) + cols - 1) // cols) * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (nome, k, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc],
                                     outline=(255, 0, 0))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"{nome}  q{k}  {k / FPS:.2f} s", fill=(0, 0, 0))
    folha.save(os.path.join(QA_DIR, "folha_qa_rev2.jpg"), quality=90)
    # Chegada da placa do gancho, quadro a quadro (0–19)
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
           f"select='lt(n\\,20)',crop={W}:420:0:540,scale=540:210,tile=4x5", "-frames:v", 1, "-q:v", 2,
           os.path.join(QA_DIR, "placa_hook_chegada_q00-q19.jpg")])
    # teste de miniatura a 25% (DS 7.2)
    return [(n, k, os.path.relpath(a, REV)) for n, k, a in lista]


def main():
    global FONTES
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--master", default=os.path.normpath(os.path.join(REV, CFG["master"])))
    ap.add_argument("--so-capa", action="store_true")
    args = ap.parse_args()
    FONTES = args.fontes
    os.makedirs(TMP, exist_ok=True)
    print(f"1/5 tempos: {N} quadros ({N / FPS:.3f} s)")
    print("2/5 objetos")
    obj = objetos()
    for lg in obj["legendas"]:
        it = lg.item
        print(f"   {it['de']:7.3f}–{it['ate']:7.3f}  {it['modo']:7s}  {it['texto']!r}")
    for lp, pl in obj["placas"]:
        print("   placa", lp["spec"]["nome"], pl.medidas)
    if args.so_capa:
        capa(args.master, obj)
        return
    print("3/5 áudio")
    wav, info_audio = montar_audio(args.master)
    print("  ", info_audio)
    print("4/5 vídeo")
    registro = montar_video(args.master, obj, wav)
    print("5/5 QA e capa")
    capa(args.master, obj)
    R = qa(obj, registro, info_audio)
    R["frames_qa"] = frames_qa()
    R["cotacao"] = CFG["cotacao"]
    R["sha256"] = hashlib.sha256(open(SAIDA, "rb").read()).hexdigest()
    R["fontes"] = {n: hashlib.sha256(open(os.path.join(FONTES, n), "rb").read()).hexdigest()[:16]
                   for n in sorted(os.listdir(FONTES)) if n.endswith(".ttf")}
    json.dump(R, open(os.path.join(REV, "relatorio_tecnico_rev2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: R[k] for k in ("formato", "audio", "video", "textos")}, ensure_ascii=False, indent=1,
                     default=str))
    print(json.dumps({k: v for k, v in R["objetos"].items() if k.startswith("n_")}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
