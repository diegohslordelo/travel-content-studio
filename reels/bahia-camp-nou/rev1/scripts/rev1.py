"""REV1 do Reel p201 "Camisa do Bahia no Camp Nou" (Primeiro Dia, Nível B): rev1/reel_bahia_camp_nou_rev1.mp4.

Só brutos 4K HLG da pasta Barcelona (fonte/brutos/, fora do git). Sem o master, sem música, sem a cena da reforma.
A camada visual reaproveita a implementação aprovada na REV8 do Reel de apresentação (placa esmaltada com Chegada,
legenda Padrão sem caixa, mini-placa de Destaque, scrim e grão de 5%) e acrescenta a legenda Narrativa (vidro).

Etapas:
  1. planos   : recorte 9:16 do 4K + HLG → SDR Rec.709 (o mesmo tone mapping do Reel de apresentação), 24 fps
  2. audio    : som direto (faixa AAC 0), passa-altas + redução de ruído leve, ganho por grupo, emendas de 20 ms,
                master −14 LUFS / ≤ −1 dBTP (DS 4.6)
  3. graficos : placa, legendas e narrativa compostas quadro a quadro em float
  4. video    : H.264 High, CRF 16, 1080 × 1920, 24 fps, AAC 48 kHz 192 kbps, sem marca d'água
  5. qa       : testes técnicos, quadros de QA, folha de contato, miniatura, emenda do loop, relatório

Uso (de dentro de reels/bahia-camp-nou/):
  python3 rev1/scripts/rev1.py --fontes PASTA_DAS_TTF [--placa-y 640]
Fontes (SIL OFL, Google Fonts): Barlow-Bold.ttf, Barlow-Medium.ttf, BarlowCondensed-ExtraBold.ttf
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
import pyloudnorm
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage, signal

REEL = os.getcwd()
assert os.path.isdir(os.path.join(REEL, "fonte", "brutos")), "rode de dentro de reels/bahia-camp-nou/"
CFG = json.load(open(os.path.join(REEL, "rev1", "rev1.json"), encoding="utf-8"))
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
SPF = SR // FPS
MS = 1000 / FPS
TMP = os.path.join(REEL, "_tmp", "rev1")
SAIDA = os.path.join(REEL, CFG["saida"])
PREVIA = os.path.join(REEL, CFG["saida_previa"])
QA_DIR = os.path.join(REEL, "rev1", "qa_frames")
SS = 4
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
T = CFG["tokens"]
SAFE = T["safe"]


def cor(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO = cor(T["signal_500"])
GRAFITE = cor(T["night_900"])
RECIBO = cor(T["paper_0"])


def rodar(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def q(t):
    return int(round(t * FPS))


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
E_IN = bezier([0.42, 0.0, 1.0, 1.0])


def kf(chaves, t, curva=E_OUT):
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- 1. linha do tempo

def planos():
    """quadros de cada plano; o loop (último plano) termina exatamente no início do plano 1."""
    out, r = [], 0
    for p in CFG["planos"]:
        n = int(round((p["fim"] - p["inicio"]) * FPS))
        p = dict(p, nq=n)
        if p["cena"] == "Loop":
            p["inicio"] = round(p["fim"] - n / FPS, 4)
        else:
            p["fim"] = round(p["inicio"] + n / FPS, 4)
        p["r0"], p["r1"] = r, r + n
        r += n
        out.append(p)
    return out


PL = planos()
N = PL[-1]["r1"]


def plano(n):
    return next(p for p in PL if p["n"] == n)


def fonte_para_rev(n, t):
    p = plano(n)
    return p["r0"] / FPS + (t - p["inicio"])


def tempos_legendas():
    L0 = CFG["legenda"]
    cortes = [p["r0"] for p in PL[1:]] + [N]
    leg = []
    for L in CFG["legendas"]:
        p = plano(L["plano"])
        pal = L["palavras"]
        item = {"texto": L["texto"], "plano": L["plano"]}
        item["q0"] = max(p["r0"], q(fonte_para_rev(L["plano"], pal[0])))
        item["palavras_q"] = [max(item["q0"], q(fonte_para_rev(L["plano"], t))) for t in pal]
        item["palavras_q"][0] = item["q0"]
        item["palavras_por_s"] = round(len(pal) / max(L["fim_fala"] - pal[0], 1e-3), 2)
        item["modo"] = "palavra" if item["palavras_por_s"] <= L0["palavras_por_s_max_palavra_a_palavra"] else "grupo"
        item["fim_fala_q"] = q(fonte_para_rev(L["plano"], L["fim_fala"]))
        leg.append(item)
    for i, it in enumerate(leg):
        prox = leg[i + 1]["q0"] if i + 1 < len(leg) else N
        it["q1"] = min(prox, min(c for c in cortes if c > it["q0"]))
        assert all(it["q0"] <= x < it["q1"] for x in it["palavras_q"]), it
        it["de"], it["ate"] = round(it["q0"] / FPS, 3), round(it["q1"] / FPS, 3)
    return leg


# ---------------------------------------------------------------- 2. objetos (implementação da REV8)

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


def caminho_seta(lado):
    P = CFG["placa"]
    k = lado * P["seta_fracao"] / 100
    ox = oy = (lado - lado * P["seta_fracao"]) / 2
    pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
    return [(ox + x * k, oy + y * k) for x, y in pts]


def placa_pecas(pasta):
    P = CFG["placa"]
    S = SS
    f = fonte(P["fonte"], P["tamanho"] * S, pasta)
    trk = P["tracking_em"] * P["tamanho"] * S
    larg_txt = sum(f.getlength(c) for c in P["texto"]) + trk * (len(P["texto"]) - 1)
    R1 = P.get("rotulo")
    if R1:
        # variante Abertura (DS 2.1): rótulo label 36 px +8% + destino h1 128 px (entrelinha 0,9), padding 28 × 36;
        # altura e módulo = altura do conteúdo, como no bundle (pd-bundle.css .pd-plate__label/__dest/__mod)
        f1 = fonte(R1["fonte"], R1["tamanho"] * S, pasta)
        trk1 = R1["tracking_em"] * R1["tamanho"] * S
        larg1 = sum(f1.getlength(c) for c in R1["texto"]) + trk1 * (len(R1["texto"]) - 1)
        alt2 = P["tamanho"] * P["entrelinha"]
        hh = int(round(2 * P["padding_v"] + R1["tamanho"] + R1["espaco_px"] + alt2))
        fw = int(round(2 * P["padding_h"] + max(larg_txt, larg1) / S))
        assert fw + hh <= 872, f"placa com {fw + hh} px passa da largura máxima (DS 2.1: 872)"
    else:
        hh = P["altura"]
        fw = int(round(2 * P["padding_h"] + larg_txt / S))
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
    capH = -f.getbbox("H", anchor="ls")[1]
    linhas = []
    if R1:
        cap1 = -f1.getbbox("H", anchor="ls")[1]
        y1 = P["padding_v"] * S + (R1["tamanho"] * S - cap1) / 2 + cap1
        y2 = (P["padding_v"] + R1["tamanho"] + R1["espaco_px"]) * S + (alt2 * S - capH) / 2 + capH
        linhas = [(R1["texto"], f1, trk1, y1), (P["texto"], f, trk, y2)]
    else:
        linhas = [(P["texto"], f, trk, (hh * S - capH) / 2 + capH)]

    def texto(d):
        for txt_, f_, trk_, y_ in linhas:
            x = P["padding_h"] * S
            for c in txt_:
                d.text((x, y_), c, font=f_, fill=255, anchor="ls")
                x += f_.getlength(c) + trk_
    txt = mascara((fw * S, hh * S), texto)
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
    face = premult(rgb, m)
    lado = hh if R1 else P["modulo"]
    mm = mascara((lado * S, hh * S), lambda d: d.rounded_rectangle([0, 0, lado * S - 1, hh * S - 1], radius=r * S,
                                                                   fill=255, corners=(False, True, True, False)))
    seta = mascara((lado * S, hh * S), lambda d: d.polygon([(x * S, y * S + (hh - lado) * S / 2)
                                                            for x, y in caminho_seta(lado)], fill=255))
    mm, seta = [reduzir(a[..., None])[..., 0] for a in (mm, seta)]
    rgbm = np.broadcast_to(GRAFITE, mm.shape + (3,)).copy()
    borda = np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07
    topo_m = np.clip(mm - deslocar(mm, 2), 0, 1) * 0.08
    for camada in (borda, topo_m):
        rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
    rgbm = rgbm * (1 - seta[..., None]) + AMARELO * seta[..., None]
    modulo = premult(rgbm, mm)
    medidas = {"face_largura": fw, "modulo_largura": lado, "altura": hh, "largura_total": fw + lado,
               "x": P["x"], "y": P["y"]}
    return face, modulo, medidas


def soft_light_branco(b, a):
    d = np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
    return b * (1 - a[..., None]) + d * a[..., None]


class Placa:
    PAD = 140

    def __init__(self, pasta):
        self.face, self.modulo, self.medidas = placa_pecas(pasta)
        self.fw = self.face.shape[1]
        self.hh = self.face.shape[0]
        self.cache = {}

    def estado(self, t_ms, saida_ms=None):
        P = CFG["placa"]
        if saida_ms is None:
            c = P["chegada"]
            e = {"dx": kf(c["face_x"], t_ms), "rot": kf(c["rotacao"], t_ms), "blur": kf(c["desfoque_px"], t_ms, LIN),
                 "mx": kf(c["modulo_x"], t_ms), "sy": kf(c["sombra_y"], t_ms), "sa": kf(c["sombra_alfa"], t_ms),
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
        lado = self.modulo.shape[1]
        tela = np.zeros((self.hh + 2 * pad, self.fw + lado + 2 * pad, 4), np.float32)
        mx = e["mx"]
        sobre(tela, deslocar(self.modulo, 0, mx - int(np.floor(mx))), pad + self.fw + int(np.floor(mx)), pad)
        face = self.face
        if e["brilho"] is not None:
            face = self.brilho(e["brilho"])
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


def linha_do_tempo_placa(k):
    """Chegada a partir do quadro 0; parada; saída de 240 ms terminando no corte do plano 1."""
    if not CFG["placa"].get("ativa", True):
        return None
    q_fim = PL[0]["r1"]
    n_sai = int(round(CFG["placa"]["saida"]["duracao_ms"] / MS))
    if k >= q_fim:
        return None
    if k >= q_fim - n_sai + 1:
        return ("saida", (k - (q_fim - n_sai)) * MS)
    return ("chegada", (k + 1) * MS)


# ---------------------------------------------------------------- legendas

def tokens(texto):
    """palavra → (prefixo, núcleo, sufixo, destaque). '*mundo*!”' → ('', 'mundo', '!”', True)."""
    out = []
    for w in texto.split():
        m = re.match(r"^(.*?)\*([^*]+)\*(.*)$", w)
        out.append((m.group(1), m.group(2), m.group(3), True) if m else ("", w, "", False))
    return out


class Legenda:
    """Legenda Padrão do DS V2 (sem caixa), Destaque por mini-placa que pula quando a palavra é dita."""
    MARGEM = 60

    def __init__(self, item, pasta):
        L = CFG["legenda"]
        self.item = item
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S, pasta)
        self.f = f
        lh = L["tamanho"] * L["entrelinha"]
        asc, desc = f.getmetrics()
        D = L["destaque"]
        linhas = item["texto"].split("\n")
        topo = L["base_y"] - len(linhas) * lh
        self.topo = topo
        esp = f.getlength(" ") / S
        palavras = []
        for i, ln in enumerate(linhas):
            toks = tokens(ln)
            larg = []
            for pre, nuc, suf, hl in toks:
                lp, ls = f.getlength(pre) / S, f.getlength(suf) / S
                ln_ = f.getlength(nuc) / S + (2 * D["padding_h"] if hl else 0)
                larg.append((lp, ln_, ls))
            total = sum(sum(x) for x in larg) + esp * (len(toks) - 1)
            x = L["centro_x"] - total / 2
            ltop = topo + i * lh
            base_y = ltop + (lh - (asc + desc) / S) / 2 + asc / S
            for (pre, nuc, suf, hl), (lp, ln_, ls) in zip(toks, larg):
                palavras.append({"pre": pre, "w": nuc, "suf": suf, "hl": hl, "x": x, "lp": lp, "larg": ln_, "ls": ls,
                                 "base_y": base_y, "ltop": ltop})
                x += lp + ln_ + ls + esp
        self.palavras = palavras
        m = self.MARGEM
        self.x0 = int(np.floor(min(p["x"] for p in palavras))) - m
        self.x1 = int(np.ceil(max(p["x"] + p["lp"] + p["larg"] + p["ls"] for p in palavras))) + m
        self.y0 = int(np.floor(topo)) - m - D["padding_v"]
        self.y1 = int(np.ceil(L["base_y"])) + m
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        self.mascaras, self.destaques = [], {}
        for j, p in enumerate(palavras):
            def desenho(d, p=p):
                by = (p["base_y"] - self.y0) * S
                if p["hl"]:
                    if p["pre"]:
                        d.text(((p["x"] - self.x0) * S, by), p["pre"], font=f, fill=255, anchor="ls")
                    if p["suf"]:
                        d.text(((p["x"] + p["lp"] + p["larg"] - self.x0) * S, by), p["suf"], font=f, fill=255, anchor="ls")
                else:
                    d.text(((p["x"] - self.x0) * S, by), p["w"], font=f, fill=255, anchor="ls")
            mk = mascara((cw * S, ch * S), desenho)
            self.mascaras.append(reduzir(mk[..., None])[..., 0])
            if p["hl"]:
                self.destaques[j] = self.mini_placa(p, f)
        self.ret = [min(p["x"] for p in palavras), topo - D["padding_v"],
                    max(p["x"] + p["lp"] + p["larg"] + p["ls"] for p in palavras), L["base_y"]]
        self.chars = len(item["texto"].replace("*", ""))

    def mini_placa(self, p, f):
        L = CFG["legenda"]
        D = L["destaque"]
        S = SS
        lh = L["tamanho"] * L["entrelinha"]
        bx0, by0 = p["x"] + p["lp"], p["ltop"] - D["padding_v"]
        bw, bh = p["larg"], lh + 2 * D["padding_v"]
        m = 40
        cw, ch = int(np.ceil(bw)) + 2 * m, int(np.ceil(bh)) + 2 * m
        ox, oy = int(np.floor(bx0)) - m, int(np.floor(by0)) - m
        fx, fy = bx0 - ox, by0 - oy
        caixa = mascara((cw * S, ch * S), lambda d: d.rounded_rectangle(
            [fx * S, fy * S, (fx + bw) * S - 1, (fy + bh) * S - 1], radius=T["radius_tag"] * S, fill=255))
        txt = mascara((cw * S, ch * S), lambda d: d.text(((fx + D["padding_h"]) * S, (p["base_y"] - oy) * S), p["w"],
                                                         font=f, fill=255, anchor="ls"))
        caixa, txt = [reduzir(a[..., None])[..., 0] for a in (caixa, txt)]
        P = CFG["placa"]
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
        return {"img": out, "x": ox, "y": oy, "cx": fx + bw / 2, "cy": fy + bh / 2,
                "caixa": [bx0, by0, bx0 + bw, by0 + bh]}

    def estado(self, k):
        it = self.item
        L = CFG["legenda"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        nsai = int(round(L["saida_ms"] / MS))
        se = 0.0
        if k >= it["q1"] - nsai:
            se = E_IN((k - (it["q1"] - nsai) + 1) / (nsai + 1))
        ws = []
        for j, p in enumerate(self.palavras):
            if p["hl"]:
                kq, dur = it["palavras_q"][j], L["destaque"]["opacidade_ms"]
            elif it["modo"] == "palavra":
                kq, dur = it["palavras_q"][j], L["palavra_ms"]
            else:
                kq, dur = it["q0"], L["grupo_ms"]
            if k < kq:
                ws.append((0.0, 0.0, 1.0))
                continue
            t = (k - kq + 1) * MS
            op = E_OUT(t / dur)
            dy = (1 - E_OUT(t / dur)) * L["palavra_sobe_px"]
            esc = 1.0
            if p["hl"]:
                dy = 0.0
                esc = kf(L["destaque"]["pop"], t, E_ARR)
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
            if op <= 0 or not mk.any():
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


class Narrativa:
    """Legenda Narrativa (DS 3.2): texto papel sobre vidro (grafite 55% + desfoque 24 px + filete 1 px claro)."""

    def __init__(self, pasta):
        C = CFG["narrativa"]
        S = SS
        f = fonte(C["fonte"], C["tamanho"] * S, pasta)
        self.linhas = C["texto"].split("\n")
        assert len(self.linhas) <= 3 and all(len(x) <= 34 for x in self.linhas)
        lh = C["tamanho"] * C["entrelinha"]
        asc, desc = f.getmetrics()
        pt, px, pb = C["padding"]
        larg = max(f.getlength(x) for x in self.linhas) / S
        self.w = int(np.ceil(2 * px + larg))
        self.h = int(np.ceil(pt + pb + len(self.linhas) * lh))
        self.x0, self.y1 = C["x"], C["base_y"]
        self.y0 = self.y1 - self.h
        self.mascaras = []
        for i, ln in enumerate(self.linhas):
            by = pt + i * lh + (lh - (asc + desc) / S) / 2 + asc / S
            mk = mascara((self.w * S, (self.h + 20) * S),
                         lambda d, ln=ln, by=by: d.text((px * S, by * S), ln, font=f, fill=255, anchor="ls"))
            self.mascaras.append(reduzir(mk[..., None])[..., 0])
        self.forma = reduzir(mascara((self.w * S, self.h * S), lambda d: d.rounded_rectangle(
            [0, 0, self.w * S - 1, self.h * S - 1], radius=T["radius_tag"] * S, fill=255))[..., None])[..., 0]
        miolo = reduzir(mascara((self.w * S, self.h * S), lambda d: d.rounded_rectangle(
            [S, S, self.w * S - 1 - S, self.h * S - 1 - S], radius=(T["radius_tag"] - 1) * S, fill=255))[..., None])[..., 0]
        self.filete = np.clip(self.forma - miolo, 0, 1)
        p = plano(C["plano"])
        # entra_s_no_plano < 0: a animação de entrada "já aconteceu" e o quadro 0 mostra o vidro aberto
        self.q0 = p["r0"] + max(0, q(C["entra_s_no_plano"]))
        self.t_off = max(0.0, -C["entra_s_no_plano"] * 1000)
        self.q1 = p["r1"]
        self.ret = [self.x0, self.y0, self.x0 + self.w, self.y1]

    def aplicar(self, img, k):
        """compõe o vidro e o texto direto no quadro (o vidro desfoca o que está atrás)."""
        C = CFG["narrativa"]
        L = CFG["legenda"]
        if not (self.q0 <= k < self.q1):
            return img, None
        t = (k - self.q0 + 1) * MS + self.t_off
        nsai = int(round(L["saida_ms"] / MS))
        se = E_IN((k - (self.q1 - nsai) + 1) / (nsai + 1)) if k >= self.q1 - nsai else 0.0
        abre = E_OUT(t / C["abre_ms"])
        esc = C["abre_escala_inicial"] + (1 - C["abre_escala_inicial"]) * abre
        op_v = abre * (1 - se)
        sobe = se * L["saida_sobe_px"]
        hh = max(1, int(round(self.h * esc)))
        forma = ndimage.zoom(self.forma, (hh / self.h, 1), order=1)[:hh]
        filete = ndimage.zoom(self.filete, (hh / self.h, 1), order=1)[:hh]
        y1 = int(round(self.y1 - sobe))
        y0 = y1 - forma.shape[0]
        x0, x1 = self.x0, self.x0 + self.w
        pad = 3 * C["desfoque_px"]
        ya, yb = max(0, y0 - pad), min(H, y1 + pad)
        xa, xb = max(0, x0 - pad), min(W, x1 + pad)
        bl = np.dstack([ndimage.gaussian_filter(img[ya:yb, xa:xb, c], C["desfoque_px"]) for c in range(3)])
        bl = bl[y0 - ya:y1 - ya, x0 - xa:x1 - xa]
        vidro = bl * (1 - C["vidro_alfa"]) + GRAFITE * C["vidro_alfa"]
        vidro = vidro * (1 - (filete * C["filete_alfa"])[..., None]) + (filete * C["filete_alfa"])[..., None]
        reg = img[y0:y1, x0:x1]
        a = (forma * op_v)[..., None]
        img[y0:y1, x0:x1] = reg * (1 - a) + vidro * a
        # linhas: sobem 8 px + opacidade, 160 ms, 120 ms de intervalo; recortadas pelo vidro
        texto = np.zeros((self.h + 20, self.w), np.float32)
        for i, mk in enumerate(self.mascaras):
            ti = t - i * C["linha_intervalo_ms"]
            if ti <= 0:
                continue
            p = E_OUT(ti / C["linha_ms"])
            texto = np.maximum(texto, deslocar(mk, (1 - p) * C["linha_sobe_px"]) * p)
        texto = texto[self.h - forma.shape[0]:self.h] if forma.shape[0] < self.h else texto[:self.h]
        ta = (texto[:forma.shape[0]] * forma * (1 - se))[..., None]
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - ta) + RECIBO * ta
        return img, ("narrativa", x0, y0, x1, y1, round(op_v, 3))


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


def compor(placa, legendas, narr, scrim, base_rgb, k, registro):
    img = overlay_blend(base_rgb, grao(k), T["op_grain"])
    img = img * (1 - scrim) + GRAFITE * scrim
    elementos = []
    img, el = narr.aplicar(img, k)
    if el:
        elementos.append(el)
    camada = np.zeros((H, W, 4), np.float32)
    st = linha_do_tempo_placa(k)
    if st:
        e = placa.estado(st[1]) if st[0] == "chegada" else placa.estado(None, saida_ms=st[1])
        im, x, y = placa.camada(e)
        sobre(camada, im, x, y)
        P = CFG["placa"]
        x_face = P["x"] + e["dx"]
        elementos.append(("placa", round(x_face, 1), P["y"], round(x_face + placa.fw + placa.modulo.shape[1], 1),
                          P["y"] + placa.hh, st[0], round(st[1], 1)))
    for lg in legendas:
        ws = lg.estado(k)
        if ws is None:
            continue
        sobre(camada, lg.camada(ws), lg.x0, lg.y0)
        elementos.append(("legenda", *[round(v, 1) for v in lg.ret], lg.item["texto"].replace("*", ""),
                          round(max(o for o, _, _ in ws), 3)))
    registro[k] = elementos
    a = camada[..., 3:4]
    return img * (1 - a) + camada[..., :3]


# ---------------------------------------------------------------- 2. áudio

def audio_fonte(arq):
    """faixa AAC 0 do bruto em 48 kHz estéreo, crua e filtrada (passa-altas + afftdn), atraso do filtro compensado."""
    A = CFG["audio"]
    nome = os.path.basename(arq)
    cru = os.path.join(TMP, f"{nome}.cru.f32")
    fil = os.path.join(TMP, f"{nome}.fil.f32")
    if not os.path.exists(fil):
        rodar(["ffmpeg", "-v", "error", "-y", "-i", arq, "-map", f"0:a:{A['faixa']}", "-ac", 2, "-ar", SR,
               "-f", "f32le", cru])
        rodar(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", 2, "-i", cru, "-af", A["filtro_voz"],
               "-f", "f32le", fil])
    x = np.fromfile(cru, np.float32).reshape(-1, 2)
    y = np.fromfile(fil, np.float32).reshape(-1, 2)
    n = min(len(x), len(y), SR * 8)
    c = signal.correlate(y[:n, 0], x[:n, 0], mode="full", method="fft")
    lag = int(np.argmax(c[n - 1:n - 1 + 4800]))  # atraso do filtro (≥ 0, até 100 ms)
    if lag:
        y = np.vstack([y[lag:], np.zeros((lag, 2), np.float32)])
    return y.astype(np.float64), lag


def montar_audio():
    A = CFG["audio"]
    fontes, atrasos = {}, {}
    for p in PL:
        if p["arquivo"] not in fontes:
            fontes[p["arquivo"]], atrasos[p["arquivo"]] = audio_fonte(os.path.join(REEL, "fonte", "brutos", p["arquivo"]))
    medidor = pyloudnorm.Meter(SR)
    # ganho por grupo: loudness integrada (BS.1770) dos trechos do grupo, sem as alças
    ganhos, medidas = {}, {}
    for g, alvo in A["grupos_lufs"].items():
        partes = [fontes[p["arquivo"]][int(p["inicio"] * SR):int(p["inicio"] * SR) + p["nq"] * SPF]
                  for p in PL if p["audio"] == g]
        lu = medidor.integrated_loudness(np.vstack(partes))
        medidas[g] = round(lu, 2)
        ganhos[g] = round(alvo - lu, 2)
    h = int(round(A["crossfade_ms"] / 1000 * SR / 2))
    mix = np.zeros((N * SPF, 2), np.float64)
    emendas = []
    for i, p in enumerate(PL):
        src = fontes[p["arquivo"]]
        o0 = int(round(p["inicio"] * SR))
        r0, r1 = p["r0"] * SPF, p["r1"] * SPF
        ha = h if i > 0 else 0
        hb = h if i < len(PL) - 1 else 0
        trecho = src[o0 - ha:o0 + (r1 - r0) + hb].copy()
        env = np.ones(len(trecho))
        if ha:
            env[:2 * ha] = np.sin(np.linspace(0, np.pi / 2, 2 * ha))
        if hb:
            env[-2 * hb:] = np.cos(np.linspace(0, np.pi / 2, 2 * hb))
        mix[r0 - ha:r1 + hb] += trecho * env[:, None] * 10 ** (ganhos[p["audio"]] / 20)
        if i > 0:
            emendas.append(round(r0 / SR, 3))
    dc = int(A["declique_ms"] * SR / 1000)
    rampa = np.linspace(0, 1, dc, endpoint=False)
    mix[:dc] *= rampa[:, None]
    mix[-dc:] *= rampa[::-1][:, None]
    # master: −14 LUFS e pico verdadeiro (4x) ≤ master_tp. O limitador (janela de 5 ms) baixa a loudness um pouco,
    # então ganho e limitador se alternam até os dois baterem.
    lim = 10 ** (A["master_tp"] / 20)

    def pico_tp(x):
        return 20 * np.log10(np.abs(signal.resample_poly(x, 4, 1, axis=0)).max())
    limitado = False
    for _ in range(8):
        mix *= 10 ** ((A["master_lufs"] - medidor.integrated_loudness(mix)) / 20)
        if pico_tp(mix) <= A["master_tp"]:
            break
        limitado = True
        ov = np.abs(signal.resample_poly(mix, 4, 1, axis=0)).max(1).reshape(-1, 4).max(1)[:len(mix)]
        g = np.minimum(1, lim / np.maximum(ov, 1e-9))
        g = ndimage.minimum_filter1d(g, int(0.005 * SR))
        g = ndimage.uniform_filter1d(g, int(0.005 * SR))
        mix *= g[:, None]
    for _ in range(4):  # termina sempre com o pico dentro do limite
        if pico_tp(mix) <= A["master_tp"]:
            break
        mix *= 10 ** ((A["master_tp"] - pico_tp(mix) - 0.05) / 20)
    wav = os.path.join(TMP, "audio_rev1.f32")
    mix.astype(np.float32).tofile(wav)
    info = {"atraso_filtro_amostras": atrasos, "lufs_grupos_antes": medidas, "ganhos_db": ganhos,
            "emendas_s": emendas, "limitador": limitado}
    return wav, mix, info


# ---------------------------------------------------------------- 1. planos → vídeo

def filtro_plano(p):
    tm = CFG["tonemap"]
    arq = os.path.join(REEL, "fonte", "brutos", p["arquivo"])
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height", "-of", "json", arq], capture_output=True, text=True).stdout)
    sw, sh = pr["streams"][0]["width"], pr["streams"][0]["height"]
    ch = sh - sh % 2
    cw = int(round(ch * 9 / 16 / 2)) * 2
    cx = int(round(p["centro_x"] * sw - cw / 2))
    cx = max(0, min(sw - cw, cx)) // 2 * 2
    p["recorte"] = {"fonte": [sw, sh], "x": cx, "y": 0, "w": cw, "h": ch}
    return arq, (f"crop={cw}:{ch}:{cx}:0,"
                 f"zscale=w={W}:h={H}:f=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl={tm['npl']},"
                 f"format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:param={tm['param']}:peak={tm['peak']}:desat=0,"
                 f"zscale=t=bt709:m=bt709:r=full,format=gbrpf32le,fps={FPS}")


def saturacao(rgb, s):
    """saturação no R'G'B' (equivale a escalar Cb/Cr como o eq=saturation do ffmpeg)."""
    y = rgb @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    return y[..., None] + s * (rgb - y[..., None])


def quadros_plano(p):
    arq, vf = filtro_plano(p)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{p['inicio']:.4f}", "-i", arq, "-vf", vf,
                             "-frames:v", str(p["nq"]), "-f", "rawvideo", "-pix_fmt", "gbrpf32le", "-"],
                            stdout=subprocess.PIPE)
    tam = W * H * 3 * 4
    for i in range(p["nq"]):
        buf = proc.stdout.read(tam)
        assert len(buf) == tam, f"plano {p['n']}: quadro {i} incompleto"
        g, b, r = np.frombuffer(buf, np.float32).reshape(3, H, W)
        rgb = np.clip(np.dstack([r, g, b]), 0, 1)
        yield np.clip(saturacao(rgb, CFG["tonemap"]["saturacao"]), 0, 1)
    proc.stdout.close()
    assert proc.wait() == 0


def montar_video(placa, legendas, narr, wav, so_quadros=None):
    scrim = scrim_alfa()
    registro = {}
    if so_quadros is not None:
        # modo teste: só alguns quadros, salvos em PNG
        out = {}
        for p in PL:
            pedidos = [k for k in so_quadros if p["r0"] <= k < p["r1"]]
            if not pedidos:
                continue
            for i, rgb in enumerate(quadros_plano(p)):
                k = p["r0"] + i
                if k in pedidos:
                    out[k] = compor(placa, legendas, narr, scrim, rgb, k, registro)
                if k >= max(pedidos):
                    break
        return out, registro
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", SAIDA]], stdin=subprocess.PIPE)
    for p in PL:
        for i, rgb in enumerate(quadros_plano(p)):
            k = p["r0"] + i
            out = compor(placa, legendas, narr, scrim, rgb, k, registro)
            enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
            if k % 48 == 0:
                print(f"   quadro {k}/{N}", flush=True)
    enc.stdin.close()
    assert enc.wait() == 0
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
           "-crf", 24, "-preset", "slow", "-pix_fmt", "yuv420p", *TAGS_COR, "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", PREVIA])
    return registro


# ---------------------------------------------------------------- 5. QA

def ffprobe(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json",
                        arq], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1)))


def quadro_mp4(arq, k, destino, extra=""):
    rodar(["ffmpeg", "-v", "error", "-y", "-i", arq, "-vf", f"select=eq(n\\,{k}){extra}", "-frames:v", 1,
           "-q:v", 2, destino])


def qa(leg, legendas, narr, placa, registro, audio_info):
    R = {"arquivo": os.path.relpath(SAIDA, REEL)}
    pr = ffprobe(SAIDA)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "duracao_video_s": float(v["duration"]),
                    "duracao_audio_s": float(a["duration"]), "codec_video": f"{v['codec_name']} ({v.get('profile')})",
                    "pix_fmt": v["pix_fmt"], "cor": [v.get("color_primaries"), v.get("color_transfer"), v.get("color_space")],
                    "audio": f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} canais",
                    "bitrate_kbps": round(int(pr["format"]["bit_rate"]) / 1000), "tamanho_mb": round(
                        os.path.getsize(SAIDA) / 1e6, 1), "tags": pr["format"].get("tags", {})}
    assert R["formato"]["quadros"] == N, R["formato"]
    lu, tp = ebur128(SAIDA)
    R["audio"] = {"lufs_integrado": lu, "pico_verdadeiro_dbtp": tp, **audio_info,
                  "ok_lufs": abs(lu - CFG["audio"]["master_lufs"]) <= 0.5, "ok_pico": tp <= -1.0}
    # zona segura e posições: tudo dentro de x 72–944 e y 256–1440 (a placa entra e sai pela lateral)
    fora = []
    for k, els in registro.items():
        for e in els:
            if e[0] == "legenda" and (e[1] < SAFE["x0"] or e[3] > SAFE["x1"] or e[2] < 1250 - 8 or e[4] > SAFE["y1"]):
                fora.append((k, e))
            if e[0] == "narrativa" and (e[1] < SAFE["x0"] or e[3] > SAFE["x1"] or e[4] > SAFE["y1"]):
                fora.append((k, e))
            if e[0] == "placa" and e[5] == "chegada" and e[6] >= 400 and (e[3] > SAFE["x1"] or e[4] > SAFE["y1"]):
                fora.append((k, e))
    R["zona_segura"] = {"violacoes": fora[:20], "ok": not fora}
    R["legendas"] = [{"texto": L["texto"], "de": L["de"], "ate": L["ate"], "modo": L["modo"],
                      "palavras_por_s": L["palavras_por_s"], "caracteres": lg.chars,
                      "x": [round(lg.ret[0], 1), round(lg.ret[2], 1)], "centro_x": round((lg.ret[0] + lg.ret[2]) / 2, 1)}
                     for L, lg in zip(leg, legendas)]
    R["narrativa"] = {"texto": CFG["narrativa"]["texto"], "quadros": [narr.q0, narr.q1], "caixa": narr.ret}
    R["placa"] = {**placa.medidas, "quadros": [0, PL[0]["r1"]]}
    R["planos"] = [{k: p[k] for k in ("n", "cena", "arquivo", "inicio", "fim", "nq", "r0", "r1", "recorte")} for p in PL]
    # emenda do loop: último quadro × primeiro quadro (mesmo plano contínuo na origem)
    a0, a1 = os.path.join(TMP, "loop_q0.png"), os.path.join(TMP, "loop_qN.png")
    quadro_mp4(SAIDA, 0, a0)
    quadro_mp4(SAIDA, N - 1, a1)
    i0 = np.asarray(Image.open(a0).convert("L"), np.float32)
    i1 = np.asarray(Image.open(a1).convert("L"), np.float32)
    zona = slice(256, 640)  # acima da placa, só imagem
    mse = ((i0[zona] - i1[zona]) ** 2).mean()
    R["loop"] = {"psnr_db_y256-640": round(10 * np.log10(255 ** 2 / max(mse, 1e-9)), 2)}
    return R


def frames_qa(registro):
    shutil.rmtree(QA_DIR, ignore_errors=True)
    os.makedirs(QA_DIR)
    alvos = [(f"t{t:05.2f}s".replace(".", "_"), min(q(t), N - 1)) for t in CFG["qa_tempos_s"]]
    alvos += [(f"q{k:03d}", k) for k in (0, 3, 6, 9, 12, 17, PL[0]["r1"] - 4, PL[0]["r1"] - 1, N - 1)]
    lista = []
    for nome, k in sorted(set(alvos), key=lambda x: x[1]):
        arq = os.path.join(QA_DIR, f"rev1_{nome}_quadro{k:03d}.jpg")
        quadro_mp4(SAIDA, k, arq)
        lista.append((nome, k, arq))
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    folha = Image.new("RGB", (cols * cw, ((len(lista) + cols - 1) // cols) * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (nome, k, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        dd = ImageDraw.Draw(im)
        dd.rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc], outline=(255, 0, 0))
        dd.line([(W / 2 * esc, 0), (W / 2 * esc, ch)], fill=(0, 200, 255))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"{nome}  q{k}  {k / FPS:.3f} s", fill=(0, 0, 0))
    folha.save(os.path.join(QA_DIR, "folha_qa_rev1.jpg"), quality=90)
    # miniatura: o Reel no feed/Explorar (~ 1/6 da largura) para testar legibilidade e enquadramento
    mini = [k for _, k, _ in lista][::2]
    tira = Image.new("RGB", (len(mini) * 180, 320), (0, 0, 0))
    for i, k in enumerate(mini):
        im = Image.open(next(a for _, kk, a in lista if kk == k)).convert("RGB").resize((180, 320), Image.LANCZOS)
        tira.paste(im, (i * 180, 0))
    tira.save(os.path.join(QA_DIR, "miniatura_180x320.jpg"), quality=90)
    if CFG["placa"].get("ativa", True):
        # placa: Chegada quadro a quadro (0–19) e saída
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
               f"select='lt(n\\,20)',crop={W}:560:0:{CFG['placa']['y'] - 190},scale=540:280,tile=4x5", "-frames:v", 1,
               "-q:v", 2, os.path.join(QA_DIR, "placa_chegada_q00-q19.jpg")])
        r1 = PL[0]["r1"]
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
               f"select='between(n\\,{r1 - 8}\\,{r1})',crop={W}:560:0:{CFG['placa']['y'] - 190},scale=540:280,tile=3x3",
               "-frames:v", 1, "-q:v", 2, os.path.join(QA_DIR, f"placa_saida_q{r1 - 8}-q{r1}.jpg")])
    # loop: último quadro e primeiro lado a lado
    lado = Image.new("RGB", (2 * 540, 960))
    for j, k in enumerate((N - 1, 0)):
        lado.paste(Image.open(next(a for _, kk, a in lista if kk == k)).convert("RGB").resize((540, 960)), (j * 540, 0))
    lado.save(os.path.join(QA_DIR, "loop_ultimo_x_primeiro.jpg"), quality=90)
    return [(n, k, os.path.relpath(a, REEL)) for n, k, a in lista]


def transcrever_render():
    """confere a fala do render (faster-whisper medium): nada cortado ou trocado."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    wav = os.path.join(TMP, "render16k.wav")
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-ac", 1, "-ar", 16000, wav])
    import wave
    with wave.open(wav) as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = m.transcribe(pcm, language="pt", word_timestamps=True, beam_size=5)
    return [{"de": round(s.start, 2), "ate": round(s.end, 2), "texto": s.text.strip()} for s in segs]


def main():
    global CFG
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--placa-y", type=int, default=None, help="sobrescreve placa.y (teste)")
    ap.add_argument("--teste", default=None, help="só renderiza estes quadros (ex.: 0,20,60) em PNG")
    args = ap.parse_args()
    if args.placa_y is not None:
        CFG["placa"]["y"] = args.placa_y
    os.makedirs(TMP, exist_ok=True)
    print(f"1/5 linha do tempo: {N} quadros = {N / FPS:.3f} s")
    for p in PL:
        print(f"   plano {p['n']} {p['cena']:22s} {p['arquivo']} {p['inicio']:.3f}–{p['fim']:.3f}  q{p['r0']}–{p['r1']}")
    leg = tempos_legendas()
    for L in leg:
        print(f"   {L['de']:7.3f}–{L['ate']:7.3f}  {L['modo']:7s} {L['palavras_por_s']:4.1f}/s  {L['texto']!r}")
    print("2/5 objetos")
    placa = Placa(args.fontes)
    legendas = [Legenda(L, args.fontes) for L in leg]
    narr = Narrativa(args.fontes)
    print("   placa", placa.medidas, " narrativa", narr.ret)
    if args.teste:
        ks = [int(x) for x in args.teste.split(",")]
        out, reg = montar_video(placa, legendas, narr, None, so_quadros=ks)
        os.makedirs(os.path.join(TMP, "teste"), exist_ok=True)
        for k, im in out.items():
            Image.fromarray((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8)).save(
                os.path.join(TMP, "teste", f"q{k:03d}_placa{CFG['placa']['y']}.png"))
        print("teste:", sorted(out), reg)
        return
    print("3/5 áudio")
    wav, mix, audio_info = montar_audio()
    print("  ", audio_info)
    print("4/5 vídeo")
    registro = montar_video(placa, legendas, narr, wav)
    print("5/5 QA")
    R = qa(leg, legendas, narr, placa, registro, audio_info)
    R["frames_qa"] = frames_qa(registro)
    R["transcricao_render"] = transcrever_render()
    R["sha256"] = hashlib.sha256(open(SAIDA, "rb").read()).hexdigest()
    R["fontes"] = {n: hashlib.sha256(open(os.path.join(args.fontes, n), "rb").read()).hexdigest()
                   for n in ("Barlow-Bold.ttf", "Barlow-Medium.ttf", "BarlowCondensed-ExtraBold.ttf")}
    json.dump(R, open(os.path.join(REEL, "rev1", "relatorio_tecnico_rev1.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: R[k] for k in ("formato", "audio", "zona_segura", "loop", "transcricao_render")},
                     ensure_ascii=False, indent=1, default=str))
    print(SAIDA)


if __name__ == "__main__":
    sys.exit(main())
