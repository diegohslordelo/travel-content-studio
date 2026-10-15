"""Reel "Lisboa: uma manhã", revisão 1: reel_lisboa_uma_manha_rev1.mp4.

A manhã de 23/03/2026 em Lisboa, da Baixa (08:49) ao Castelo de São Jorge (10:30), em 12 planos reais, com a
hora real de cada arquivo. Nível B do DS 5.2 (cortes secos, legenda Padrão, 1 objeto de marca: o Bilhete),
mais as etiquetas Informação (lugar + hora) e a legenda Emocional no fecho.

Fonte do vídeo: os cortes gerados no Colab por ../scripts/colab_cortes.py (pedaços de até 2 s, 1214 x 1920,
HEVC 10 bits HLG), baixados para ../cortes/. Nenhum bruto é alterado.

Etapas:
  1. planos  : cada plano sai dos pedaços (concat + trim no quadro), recorte 1080 x 1920, HLG -> SDR Rec.709
               pelo método aprovado (Reinhard, pico 4,93, saturação 0,88)
  2. objetos : legenda Padrão (com destaque), etiquetas Informação, Bilhete e legenda Emocional, em float sRGB
  3. áudio   : fala do gancho na frente, som real de cada lugar por baixo; master −14 LUFS, pico ≤ −1 dBTP
  4. vídeo   : grão 5% → scrim → objetos → H.264 High BT.709 / AAC 48 kHz + prévia leve 720 × 1280
  5. qa      : relatório técnico, quadros de QA, folha de contato

Uso (de dentro de reels/lisboa-uma-manha/):
  python3 rev1/scripts/rev1.py --fontes PASTA_COM_AS_TTF [--config rev1/rev1.json]
Fontes (SIL OFL, Google Fonts, pasta ofl/): barlow/Barlow-Bold.ttf, barlowcondensed/BarlowCondensed-Bold.ttf,
  BarlowCondensed-ExtraBold.ttf, BarlowCondensed-LightItalic.ttf, ibmplexmono/IBMPlexMono-Medium.ttf,
  reeniebeanie/ReenieBeanie.ttf
"""
import argparse
import glob
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

AP = argparse.ArgumentParser()
AP.add_argument("--fontes", required=True)
AP.add_argument("--config", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rev1.json"))
AP.add_argument("--sem-qa", action="store_true")
ARGS = AP.parse_args()

CFG_PATH = os.path.abspath(ARGS.config)
REV = os.path.dirname(CFG_PATH)
CFG = json.load(open(CFG_PATH, encoding="utf-8"))
FONTES = ARGS.fontes
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
MS = 1000 / FPS
TMP = os.path.join(REV, "_tmp")
CORTES = os.path.normpath(os.path.join(REV, CFG["cortes_dir"]))
SAIDA = os.path.join(REV, CFG["saida"])
PREVIA = os.path.join(REV, CFG["saida_previa"])
QA_DIR = os.path.join(REV, "qa_frames")
SS = 4
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
T = CFG["tokens"]
SAFE = T["safe"]


def cor(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


AMARELO, GRAFITE, ASFALTO = cor(T["signal_500"]), cor(T["night_900"]), cor(T["night_500"])
CONCRETO, RECIBO, PAPEL, CANETA = cor(T["night_300"]), cor(T["paper_0"]), cor(T["paper_500"]), cor(T["ink_500"])


def rodar(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def q(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------- curvas e keyframes (iguais à REV8 do Reel de apresentação)

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
E_IN = bezier([0.42, 0.0, 1.0, 1.0])
LIN = lambda t: min(max(t, 0.0), 1.0)  # noqa: E731


def kf(chaves, t, curva=E_OUT):
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- linha do tempo

def planos():
    out, r = [], 0
    for p in CFG["planos"]:
        n = q(p["out"] - p["in"])
        out.append({**p, "nq": n, "r0": r, "r1": r + n})
        r += n
    return out


PLANOS = planos()
N = PLANOS[-1]["r1"]


def plano(n):
    return next(p for p in PLANOS if p["n"] == n)


def pedacos(arquivo):
    """pedaços do Colab: IMG_xxxx_AAAA-BBBB.mov (centésimos de segundo do arquivo original)."""
    out = []
    for f in sorted(glob.glob(os.path.join(CORTES, arquivo[:-4] + "_*.mov"))):
        m = re.search(r"_(\d{4})-(\d{4})\.mov$", f)
        out.append((int(m.group(1)) / 100, int(m.group(2)) / 100, f))
    out.sort()
    assert out, f"sem cortes de {arquivo} em {CORTES}"
    return out


def fonte_do_plano(p):
    """lista de pedaços que cobrem [in, out] e o deslocamento do in dentro do primeiro."""
    pc = [x for x in pedacos(p["arquivo"]) if x[1] > p["in"] + 1e-6 and x[0] < p["out"] - 1e-6]
    assert pc and pc[0][0] <= p["in"] + 1e-6 and pc[-1][1] >= p["out"] - 1e-3, (p["arquivo"], p["in"], p["out"], pc)
    for a, b in zip(pc, pc[1:]):
        assert abs(a[1] - b[0]) < 1e-6, f"buraco entre pedaços de {p['arquivo']}: {a[1]} → {b[0]}"
    return pc, p["in"] - pc[0][0]


# ---------------------------------------------------------------- utilitários de imagem (iguais à REV8)

def fonte(nome, px):
    return ImageFont.truetype(os.path.join(FONTES, nome), px, layout_engine=ImageFont.Layout.RAQM)


def reduzir(a, s=SS):
    h, w = a.shape[0] // s, a.shape[1] // s
    return a[:h * s, :w * s].reshape(h, s, w, s, -1).mean((1, 3))


def mascara(tam, desenho):
    im = Image.new("L", tam, 0)
    desenho(ImageDraw.Draw(im))
    return np.asarray(im, np.float32) / 255


def mascara_1x(tam, desenho):
    """desenha em SS× e reduz (antisserrilhado)."""
    m = mascara((tam[0] * SS, tam[1] * SS), desenho)
    return reduzir(m[..., None])[..., 0]


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


def ruido(h, w, semente):
    rng = np.random.default_rng(semente)
    n = ndimage.gaussian_filter(rng.standard_normal((h, w)), 0.8) + 0.5 * ndimage.gaussian_filter(
        rng.standard_normal((h, w)), 2.0)
    return ((n - n.min()) / (n.max() - n.min())).astype(np.float32)


def com_sombra_papel(obj):
    """objeto premultiplicado + shadow-paper (token), numa tela com margem."""
    sp = T["shadow_paper"]
    m = 48
    tela = np.zeros((obj.shape[0] + 2 * m, obj.shape[1] + 2 * m, 4), np.float32)
    sobre(tela, obj, m, m)
    s = sombra_objeto(tela[..., 3], sp["dura"], sp["projetada"])
    out = premult(np.zeros(s.shape + (3,), np.float32), s)
    return sobre(out, tela), m


def girar(img, graus):
    if abs(graus) < 1e-3:
        return img
    return np.dstack([ndimage.rotate(img[..., i], -graus, reshape=False, order=1) for i in range(4)])


def com_margem(img, m):
    out = np.zeros((img.shape[0] + 2 * m, img.shape[1] + 2 * m, 4), np.float32)
    out[m:-m, m:-m] = img
    return out


# ---------------------------------------------------------------- legenda Padrão (DS 3.2; mesma construção da REV8)

def segmentos(linha):
    partes = re.split(r"(\*[^*]+\*)", linha)
    return [(p.strip("*"), p.startswith("*")) for p in partes if p]


class Legenda:
    MARGEM = 60

    def __init__(self, item):
        L = CFG["legendas"]
        self.item = item
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S)
        lh = L["tamanho"] * L["entrelinha"]
        asc, desc = f.getmetrics()
        linhas = item["texto"].split("\n")
        D = L["destaque"]
        topo = L["base_y"] - len(linhas) * lh
        self.topo = topo
        self.linhas = [ln.replace("*", "") for ln in linhas]
        esp = f.getlength(" ") / S
        palavras = []
        for i, ln in enumerate(linhas):
            toks = []
            for s, hl in segmentos(ln):
                cola = bool(s) and s[0] in ",.;:!?"  # pontuação logo depois de um destaque: sem espaço
                for k_, w in enumerate(s.split()):
                    toks.append((w, hl, cola and k_ == 0))
            larg = [f.getlength(w) / S + (2 * D["padding_h"] if hl else 0) for w, hl, _ in toks]
            espacos = [0.0 if c else esp for _, _, c in toks[1:]]
            total = sum(larg) + sum(espacos)
            x = L["centro_x"] - total / 2  # centro do canvas (W / 2), CLAUDE.md 12
            ltop = topo + i * lh
            base_y = ltop + (lh - (asc + desc) / S) / 2 + asc / S
            for j_, ((w, hl, _), lw) in enumerate(zip(toks, larg)):
                if j_ > 0:
                    x += espacos[j_ - 1]
                palavras.append({"w": w, "hl": hl, "x": x, "larg": lw, "base_y": base_y, "ltop": ltop})
                x += lw
        self.palavras = palavras
        m = self.MARGEM
        self.x0 = int(np.floor(min(p["x"] for p in palavras))) - m
        self.x1 = int(np.ceil(max(p["x"] + p["larg"] for p in palavras))) + m
        self.y0 = int(np.floor(topo)) - m
        self.y1 = int(np.ceil(L["base_y"])) + m
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        self.mascaras, self.destaques = [], {}
        for j, p in enumerate(palavras):
            if p["hl"]:
                self.mascaras.append(None)
                self.destaques[j] = self.mini_placa(p, f)
            else:
                mk = mascara((cw * S, ch * S), lambda d, p=p: d.text(((p["x"] - self.x0) * S, (p["base_y"] - self.y0) * S),
                                                                     p["w"], font=f, fill=255, anchor="ls"))
                self.mascaras.append(reduzir(mk[..., None])[..., 0])
        self.ret = [min(p["x"] for p in palavras), topo, max(p["x"] + p["larg"] for p in palavras), L["base_y"]]
        self.chars_max = max(len(x) for x in self.linhas)

    def mini_placa(self, p, f):
        L = CFG["legendas"]
        D = L["destaque"]
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
        caixa, txt = [reduzir(a[..., None])[..., 0] for a in (caixa, txt)]
        rgb = np.broadcast_to(AMARELO, caixa.shape + (3,)).copy()
        topo = np.clip(caixa - deslocar(caixa, 2), 0, 1) * 0.45   # shadow-plate-bevel: luz 2 px (45%)
        base = np.clip(caixa - deslocar(caixa, -4), 0, 1) * 0.16  # sombra 4 px (16%)
        rgb = rgb * (1 - topo[..., None]) + topo[..., None]
        rgb = rgb * (1 - base[..., None])
        rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
        sombra = sombra_objeto(caixa, D["sombra_dura"], D["sombra_projetada"])
        out = premult(np.zeros(caixa.shape + (3,), np.float32), sombra)
        sobre(out, premult(rgb, caixa))
        return {"img": out, "x": ox, "y": oy, "cx": fx + bw / 2, "cy": fy + bh / 2}

    def estado(self, k):
        it = self.item
        L = CFG["legendas"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        nsai = int(round(L["saida_ms"] / MS))
        se = E_IN((k - (it["q1"] - nsai) + 1) / (nsai + 1)) if (k >= it["q1"] - nsai and it["q1"] < N) else 0.0
        ws = []
        for j, p in enumerate(self.palavras):
            kq = it["q0"]
            dur = L["grupo_ms"]
            if p["hl"] and it.get("destaque_q") is not None:
                kq, dur = it["destaque_q"], L["destaque"]["opacidade_ms"]
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
        L = CFG["legendas"]
        cw, ch = self.x1 - self.x0, self.y1 - self.y0
        sombra = np.zeros((ch, cw), np.float32)
        texto = np.zeros((ch, cw, 4), np.float32)
        sd, sdi = L["sombra_dura"], L["sombra_difusa"]
        for j, (op, dy, esc) in enumerate(ws):
            mk = self.mascaras[j]
            if mk is None or op <= 0:
                continue
            m2 = deslocar(mk, dy) if abs(dy) > 1e-3 else mk
            s = 1 - (1 - deslocar(m2, sd[0]) * sd[1]) * (1 - ndimage.gaussian_filter(m2, sdi["blur"] / 2) * sdi["alfa"])
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


def itens_legenda():
    L = CFG["legendas"]
    p1 = PLANOS[0]
    out = []
    for g in L["grupos"]:
        t0 = g["de_fonte"] - p1["in"]
        t1 = g["ate_fonte"] - p1["in"]
        it = {"texto": g["texto"], "q0": max(0, q(t0)), "q1": min(p1["r1"], q(t1))}
        if "destaque_fonte" in g:
            it["destaque_q"] = q(g["destaque_fonte"] - p1["in"])
        out.append(it)
    return out


# ---------------------------------------------------------------- etiqueta Informação (DS 3.2)

class Etiqueta:
    """mini-recibo de papel com picote no topo: rótulo (Plex Mono) + hora (PD Placar, algarismos tabulares)."""

    def __init__(self, rotulo, hora, hora_antes):
        I = CFG["informacao"]
        self.rotulo, self.hora, self.antes = rotulo, hora, hora_antes
        fr = fonte(I["fonte_rotulo"], I["rotulo_px"] * SS)
        self.fn = fonte(I["fonte_numero"], I["numero_px"] * SS)
        trk = I["rotulo_tracking_em"] * I["rotulo_px"] * SS
        larg_r = (sum(fr.getlength(c) for c in rotulo) + trk * (len(rotulo) - 1)) / SS
        d = ImageDraw.Draw(Image.new("L", (8, 8)))
        self.dig = d.textlength("0", font=self.fn, features=["tnum"]) / SS        # avanço tabular
        self.dois = d.textlength(":", font=self.fn, features=["tnum"]) / SS
        larg_n = 4 * self.dig + self.dois
        pt, pd, pb, pe = I["padding"]
        self.lh_r = I["rotulo_px"] * 1.3
        self.lh_n = I["numero_px"] * 1.0
        w = int(np.ceil(pe + max(larg_r, larg_n) + pd))
        h = int(np.ceil(pt + self.lh_r + I["gap_px"] + self.lh_n + pb))
        self.w, self.h = w, h
        self.x, self.y = I["x"], I["base_y"] - h
        r = T["radius_paper"]
        forma = mascara_1x((w, h), lambda dd: dd.rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=r * SS, fill=255))
        pc = I["picote"]
        furos = mascara_1x((w, h), lambda dd: [dd.ellipse([(x0 - pc["furo_px"] / 2) * SS, (pc["y_px"] - pc["furo_px"] / 2) * SS,
                                                          (x0 + pc["furo_px"] / 2) * SS, (pc["y_px"] + pc["furo_px"] / 2) * SS], fill=255)
                                              for x0 in np.arange(pc["passo_px"] / 2 + 6, w - 6, pc["passo_px"])])
        base_r = pt + I["rotulo_px"] * 1.0

        def txt_r(dd):
            x = pe * SS
            for c in rotulo:
                dd.text((x, base_r * SS), c, font=fr, fill=255, anchor="ls")
                x += fr.getlength(c) + trk
        rot = mascara_1x((w, h), txt_r)
        rgb = np.broadcast_to(RECIBO, (h, w, 3)).copy()
        rgb *= (1 - T["op_fiber"] * ruido(h, w, 11))[..., None]                # fibra 4%
        rgb = rgb * (1 - furos[..., None]) + CONCRETO * furos[..., None]       # picote (night-300)
        rgb = rgb * (1 - rot[..., None]) + ASFALTO * rot[..., None]            # rótulo night-500
        self.papel = premult(rgb, forma)
        self.forma = forma
        # caixa do número (para o giro dos dígitos)
        self.n_x = pe
        self.n_top = pt + self.lh_r + I["gap_px"]
        asc = -self.fn.getbbox("0", anchor="ls")[1] / SS
        self.n_base = self.n_top + (self.lh_n + asc) / 2
        self.cache = {}

    def glifo(self, c):
        if c not in self.cache:
            larg = self.dig if c != ":" else self.dois
            cw, ch = int(np.ceil(larg)) + 2, int(np.ceil(self.lh_n))
            asc = -self.fn.getbbox("0", anchor="ls")[1] / SS
            by = (self.lh_n + asc) / 2
            self.cache[c] = mascara_1x((cw, ch), lambda dd: dd.text((1 * SS, by * SS), c, font=self.fn, fill=255,
                                                                   anchor="ls", features=["tnum"]))
        return self.cache[c]

    def numero(self, p):
        """máscara do número com o giro: cada dígito que muda rola de baixo para cima (p de 0 a 1)."""
        mk = np.zeros((self.h, self.w), np.float32)
        x = self.n_x
        lh = self.lh_n
        y0 = int(round(self.n_top))
        for a, b in zip(self.antes, self.hora):
            larg = self.dig if b != ":" else self.dois
            cel = np.zeros((int(np.ceil(lh)), int(np.ceil(larg)) + 2), np.float32)
            if a == b or p >= 1:
                g = self.glifo(b)
                cel[:g.shape[0], :g.shape[1]] = np.maximum(cel[:g.shape[0], :g.shape[1]], g)
            else:
                e = E_OUT(p)
                for c, dy in ((a, -e * lh), (b, (1 - e) * lh)):
                    g = deslocar(self.glifo(c), dy)
                    cel[:g.shape[0], :g.shape[1]] = np.maximum(cel[:g.shape[0], :g.shape[1]], g)
            xi = int(round(x)) - 1
            hh, ww = cel.shape
            ww = min(ww, self.w - xi)
            mk[y0:y0 + hh, xi:xi + ww] = np.maximum(mk[y0:y0 + hh, xi:xi + ww], cel[:, :ww])
            x += larg
        return mk * self.forma

    def imagem(self, p_giro):
        num = self.numero(p_giro)
        img = self.papel.copy()
        img[..., :3] = img[..., :3] * (1 - num[..., None]) + GRAFITE * num[..., None]
        return com_sombra_papel(img)

    def camada(self, t_ms, dur_ms):
        """(img, x, y, opacidade) no instante t_ms desde a entrada; None fora."""
        I = CFG["informacao"]
        if t_ms < 0 or t_ms >= dur_ms:
            return None
        p_giro = LIN((t_ms - I["entrada_ms"] / 2) / I["giro_ms"])
        dx, op = 0.0, 1.0
        if t_ms < I["entrada_ms"]:
            e = E_OUT(t_ms / I["entrada_ms"])
            dx, op = I["entrada_dx"] * (1 - e), e
        sai0 = dur_ms - I["saida_ms"]
        if t_ms >= sai0:
            e = E_EXIT((t_ms - sai0) / I["saida_ms"])
            dx, op = I["saida_dx"] * e, 1 - e
        chave = round(p_giro, 3)
        if not hasattr(self, "_img") or self._img[0] != chave:
            self._img = (chave, *self.imagem(p_giro))
        img, m = self._img[1], self._img[2]
        return img * op, int(round(self.x + dx)) - m, self.y - m


def etiquetas():
    I = CFG["informacao"]
    out, antes = [], "00:00"
    for e in I["etiquetas"]:
        p = plano(e["plano"])
        q0 = p["r0"] + q(e["de_s"])
        q1 = q0 + q(e["dur_s"])
        out.append({"obj": Etiqueta(e["rotulo"], e["hora"], antes), "q0": q0, "q1": q1, "rotulo": e["rotulo"], "hora": e["hora"]})
        antes = e["hora"]
    return out


# ---------------------------------------------------------------- Bilhete (DS 2.4)

class Bilhete:
    def __init__(self):
        B = CFG["bilhete"]
        f = fonte(B["fonte"], B["tamanho"] * SS)
        lh = B["tamanho"] * B["entrelinha"]
        pv, ph = B["padding"]
        larg = max(f.getlength(t) for t in B["texto"]) / SS
        w = int(np.ceil(2 * ph + larg))
        h = int(np.ceil(2 * pv + lh * len(B["texto"])))
        asc, desc = f.getmetrics()
        r = T["radius_paper"]
        forma = mascara_1x((w, h), lambda d: d.rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=r * SS, fill=255))

        def txt(d):
            for i, t in enumerate(B["texto"]):
                base = pv + i * lh + (lh - (asc + desc) / SS) / 2 + asc / SS
                d.text((ph * SS, base * SS), t, font=f, fill=255, anchor="ls")
        self.txt = mascara_1x((w, h), txt)
        rgb = np.broadcast_to(PAPEL, (h, w, 3)).copy()
        rgb *= (1 - T["op_fiber"] * ruido(h, w, 23))[..., None]
        self.papel_rgb, self.forma = rgb, forma
        self.w, self.h = w, h
        self.x = min(B["x"], SAFE["x1"] - w)
        self.y = B["topo_y"]
        self.tx0 = ph
        self.tx1 = ph + larg
        p = plano(B["plano"])
        self.q0 = p["r0"] + q(B["de_s"])
        self.q1 = p["r1"] - q(B["ate_fim_do_plano_s"])
        self.cache = {}

    def estado(self, k):
        B = CFG["bilhete"]
        if not (self.q0 <= k < self.q1):
            return None
        t = (k - self.q0 + 1) * MS
        e = E_ARR(t / B["entrada_ms"])
        dy, rot, op = 24 * (1 - e), T["rot_note"] * e, min(1.0, LIN(t / B["entrada_ms"]) * 1.0)
        rev = LIN((t - B["entrada_ms"]) / B["escrita_ms"])
        rev = E_OUT(rev)
        nsai = int(round(B["saida_ms"] / MS))
        if k >= self.q1 - nsai:
            s = E_EXIT((k - (self.q1 - nsai) + 1) / nsai)
            dy, op = 40 * s, 1 - s
            rot = T["rot_note"]
        return {"dy": dy, "rot": rot, "op": op, "rev": rev}

    def camada(self, e):
        chave = (round(e["rot"], 2), round(e["rev"], 3))
        if chave not in self.cache:
            # revelação da letra da esquerda para a direita (máscara com borda suave de 12 px)
            xs = np.arange(self.w, dtype=np.float32)
            frente = self.tx0 + (self.tx1 - self.tx0 + 24) * e["rev"]
            mk = np.clip((frente - xs) / 12, 0, 1)[None, :]
            tinta = self.txt * mk
            rgb = self.papel_rgb * (1 - tinta[..., None]) + CANETA * tinta[..., None]
            img = com_margem(premult(rgb, self.forma), 40)
            img = girar(img, e["rot"])
            img, m = com_sombra_papel(img)
            self.cache[chave] = (img, m + 40)
        img, m = self.cache[chave]
        return img * e["op"], self.x - m, int(round(self.y + e["dy"])) - m


# ---------------------------------------------------------------- legenda Emocional (DS 3.2)

class Emocional:
    def __init__(self):
        E = CFG["emocional"]
        self.linhas = E["linhas"]
        self.f = {300: fonte(E["fonte_300"], E["tamanho"] * SS), 800: fonte(E["fonte_800"], E["tamanho"] * SS)}
        self.lh = E["tamanho"] * E["entrelinha"]
        p = plano(E["plano"])
        self.q0 = p["r0"] + q(E["de_s"])
        self.q1 = p["r1"]
        topo = E["centro_y"] - self.lh * len(self.linhas) / 2
        self.topo = topo
        self.cache = {}
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        sr = E["scrim_radial"]
        d = np.sqrt(((xx - W / 2) / sr["raio_x"]) ** 2 + ((yy - E["centro_y"]) / sr["raio_y"]) ** 2)
        self.radial = (np.clip(1 - d, 0, 1) ** 1.5 * sr["alfa"]).astype(np.float32)

    def linha(self, i, trk_em, blur):
        chave = (i, round(trk_em, 4), round(blur, 2))
        if chave in self.cache:
            return self.cache[chave]
        L = self.linhas[i]
        f = self.f[L["peso"]]
        px = CFG["emocional"]["tamanho"]
        trk = trk_em * px * SS
        txt = L["texto"]
        larg = (sum(f.getlength(c) for c in txt) + trk * (len(txt) - 1)) / SS
        m = 60
        cw, ch = int(np.ceil(larg)) + 2 * m, int(np.ceil(self.lh)) + 2 * m
        asc, desc = f.getmetrics()
        base = m + (self.lh - (asc + desc) / SS) / 2 + asc / SS

        def d(dd):
            x = m * SS
            for c in txt:
                dd.text((x, base * SS), c, font=f, fill=255, anchor="ls")
                x += f.getlength(c) + trk
        mk = mascara_1x((cw, ch), d)
        if blur > 0.2:
            mk = ndimage.gaussian_filter(mk, blur / 2)
        L3 = CFG["legendas"]
        sd, sdi = L3["sombra_dura"], L3["sombra_difusa"]  # sombra de texto da DS 3.1
        s = 1 - (1 - deslocar(mk, sd[0]) * sd[1]) * (1 - ndimage.gaussian_filter(mk, sdi["blur"] / 2) * sdi["alfa"])
        out = premult(np.zeros(mk.shape + (3,), np.float32), s)
        sobre(out, premult(np.broadcast_to(RECIBO, mk.shape + (3,)), mk))
        x = int(round(W / 2 - cw / 2))  # centro do canvas
        y = int(round(self.topo + i * self.lh)) - m
        self.cache[chave] = (out, x, y, (W / 2 - larg / 2, self.topo + i * self.lh, W / 2 + larg / 2, self.topo + (i + 1) * self.lh))
        return self.cache[chave]

    def estado(self, k):
        if not (self.q0 <= k < self.q1):
            return None
        t = (k - self.q0 + 1) * MS
        out = []
        for i, (atraso, dur) in enumerate(((0, 500), (120, 400))):
            p = E_CIN(LIN((t - atraso) / dur))
            out.append({"trk": 0.12 + (-0.01 - 0.12) * p, "blur": 6 * (1 - p), "op": p})
        return out


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


def compor(obj, scrim, base_rgb, k, reg):
    img = overlay_blend(base_rgb, grao(k), T["op_grain"])
    img = img * (1 - scrim) + GRAFITE * scrim
    camada = np.zeros((H, W, 4), np.float32)
    els = []
    emo = obj["emocional"].estado(k)
    if emo:
        a = obj["emocional"].radial * max(e["op"] for e in emo)
        img = img * (1 - a[..., None]) + GRAFITE * a[..., None]
    for et in obj["etiquetas"]:
        r = et["obj"].camada((k - et["q0"]) * MS + MS, (et["q1"] - et["q0"]) * MS)
        if r:
            im, x, y = r
            sobre(camada, im, x, y)
            o = et["obj"]
            els.append(("etiqueta", x + 48, o.y, x + 48 + o.w, o.y + o.h, et["rotulo"]))
    e = obj["bilhete"].estado(k)
    if e:
        im, x, y = obj["bilhete"].camada(e)
        sobre(camada, im, x, y)
        b = obj["bilhete"]
        els.append(("bilhete", b.x, b.y + e["dy"], b.x + b.w, b.y + b.h + e["dy"], " / ".join(CFG["bilhete"]["texto"])))
    for lg in obj["legendas"]:
        ws = lg.estado(k)
        if ws is None:
            continue
        sobre(camada, lg.camada(ws), lg.x0, lg.y0)
        els.append(("legenda", *[round(v, 1) for v in lg.ret], lg.item["texto"].replace("*", "")))
    if emo:
        for i, st in enumerate(emo):
            if st["op"] <= 0:
                continue
            im, x, y, ret = obj["emocional"].linha(i, st["trk"], st["blur"])
            sobre(camada, im * st["op"], x, y)
            els.append(("emocional", *[round(v, 1) for v in ret], obj["emocional"].linhas[i]["texto"]))
    reg[k] = els
    a = camada[..., 3:4]
    return img * (1 - a) + camada[..., :3]


# ---------------------------------------------------------------- vídeo dos planos

def filtro_planos():
    entradas, filtros, rot = [], [], []
    tm = CFG["tone_mapping"]["filtro"]
    i = 0
    for j, p in enumerate(PLANOS):
        pc, off = fonte_do_plano(p)
        lab = []
        for a, b, f in pc:
            entradas += ["-i", f]
            lab.append(f"[{i}:v]")
            i += 1
        cat = f"{''.join(lab)}concat=n={len(lab)}:v=1:a=0," if len(lab) > 1 else lab[0]
        # tpad: o fps pode deixar o último quadro de fora; repete-o (no máximo 1–2 quadros) e o trim fecha no exato
        filtros.append(f"{cat}setpts=PTS-STARTPTS,trim=start={off:.4f},setpts=PTS-STARTPTS,fps={FPS},"
                       f"tpad=stop_mode=clone:stop=3,trim=end_frame={p['nq']},crop=1080:1920:{p['x']}:0,{tm},"
                       f"format=gbrp16le[p{j}]")
        rot.append(f"[p{j}]")
    filtros.append(f"{''.join(rot)}concat=n={len(PLANOS)}:v=1:a=0,setpts=N/({FPS}*TB),format=rgb48le[v]")
    return entradas, ";".join(filtros)


# ---------------------------------------------------------------- áudio

def audio_plano(p):
    pc, off = fonte_do_plano(p)
    ent, lab = [], []
    for i, (a, b, f) in enumerate(pc):
        ent += ["-i", f]
        lab.append(f"[{i}:a]")
    cat = f"{''.join(lab)}concat=n={len(lab)}:v=0:a=1," if len(lab) > 1 else lab[0]
    dur = p["nq"] / FPS
    fc = f"{cat}atrim=start={off:.4f}:duration={dur:.4f},asetpts=PTS-STARTPTS,aresample={SR}[a]"
    r = subprocess.run(["ffmpeg", "-v", "error", *ent, "-filter_complex", fc, "-map", "[a]", "-f", "f32le", "-ac", "2",
                        "-ar", str(SR), "-"], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).astype(np.float64)
    n = p["nq"] * SR // FPS
    if len(x) < n:
        x = np.vstack([x, np.zeros((n - len(x), 2))])
    return x[:n]


def lufs_de(x):
    f = os.path.join(TMP, "medir.f32")
    x.astype(np.float32).tofile(f)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", f,
                        "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", s).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", s).group(1))
    return i, tp


def montar_audio():
    A = CFG["audio"]
    partes, ganhos = [], []
    for p in PLANOS:
        x = audio_plano(p)
        alvo = A["fala_lufs_alvo"] if p["audio"] == "fala" else A["ambiente_lufs_alvo"]
        i, _ = lufs_de(x)
        g = 0.0 if not np.isfinite(i) else max(min(alvo - i, 18.0), -30.0)
        partes.append(x * 10 ** (g / 20))
        ganhos.append({"plano": p["n"], "lufs_origem": i, "ganho_db": round(g, 2)})
    # emendas: rampa curta de 40 ms em cada lado do corte (sem sobrepor planos: os cortes de vídeo são secos)
    h = int(A["transicao_ms"] / 2 * SR / 1000)
    rampa = np.sin(np.linspace(0, np.pi / 2, h)) ** 2
    for i, x in enumerate(partes):
        if i > 0:
            x[:h] *= rampa[:, None]
        if i < len(partes) - 1:
            x[-h:] *= rampa[::-1][:, None]
    mix = np.vstack(partes)
    # master −14 LUFS e pico verdadeiro ≤ −1 dBTP (DS 4.6): ganho até o alvo; se o pico passar, limitador suave
    # (alimiter) e novo ganho, até 6 voltas
    wav = os.path.join(TMP, "audio_rev1.f32")
    lim = os.path.join(TMP, "audio_rev1_lim.f32")
    for _ in range(6):
        i, tp = lufs_de(mix)
        mix *= 10 ** ((A["master_lufs"] - i) / 20)
        i, tp = lufs_de(mix)
        if tp <= A["master_pico_dbtp"]:
            break
        mix.astype(np.float32).tofile(wav)
        rodar(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav, "-af",
               f"alimiter=limit={10 ** ((A['master_pico_dbtp'] - 0.8) / 20):.4f}:level=false:attack=1:release=60",
               "-f", "f32le", "-ar", SR, "-ac", 2, lim])
        mix = np.fromfile(lim, np.float32).reshape(-1, 2).astype(np.float64)
    mix.astype(np.float32).tofile(wav)
    ganhos.append({"master": {"lufs": round(i, 2), "pico_dbtp": round(tp, 2)}})
    return wav, ganhos


# ---------------------------------------------------------------- render

def montar_video(obj, wav):
    ent, fc = filtro_planos()
    dec = subprocess.Popen(["ffmpeg", "-v", "error", *ent, "-filter_complex", fc, "-map", "[v]", "-frames:v", str(N),
                            "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-shortest", "-movflags", "+faststart", SAIDA]],
        stdin=subprocess.PIPE)
    scrim = scrim_alfa()
    reg = {}
    tam = W * H * 3 * 2
    for k in range(N):
        buf = dec.stdout.read(tam)
        assert len(buf) == tam, f"quadro {k} incompleto"
        base = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
        out = compor(obj, scrim, base, k, reg)
        enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
        if k % 48 == 0:
            print(f"   quadro {k}/{N}", flush=True)
    dec.stdout.close()
    enc.stdin.close()
    assert dec.wait() == 0 and enc.wait() == 0
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
           "-crf", 24, "-preset", "slow", "-pix_fmt", "yuv420p", *TAGS_COR, "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", PREVIA])
    return reg


# ---------------------------------------------------------------- QA

def ffprobe(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", arq],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", s).group(1)))


def qa(reg, obj, ganhos):
    R = {"arquivo": os.path.relpath(SAIDA, os.path.dirname(REV))}
    pr = ffprobe(SAIDA)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"], "quadros": int(v["nb_read_frames"]),
                    "duracao_video_s": float(v["duration"]), "duracao_audio_s": float(a["duration"]),
                    "codec_video": f"{v['codec_name']} ({v.get('profile')})", "pix_fmt": v["pix_fmt"],
                    "cor": f"{v.get('color_primaries')}/{v.get('color_transfer')}/{v.get('color_space')}/{v.get('color_range')}",
                    "codec_audio": f"{a['codec_name']} ({a.get('profile')})", "sr_audio": int(a["sample_rate"]),
                    "tamanho_bytes": int(pr["format"]["size"])}
    R["previa"] = {"arquivo": os.path.basename(PREVIA), "tamanho_bytes": os.path.getsize(PREVIA)}
    lufs, tp = ebur128(SAIDA)
    R["audio"] = {"lufs_integrado": lufs, "pico_verdadeiro_dbtp": tp, "ganhos_por_plano": ganhos,
                  "validacao_auditiva": "pendente (humana)"}
    fora = []
    for k, els in reg.items():
        for e in els:
            nome, x0, y0, x1, y1 = e[:5]
            if nome == "etiqueta":
                continue  # a etiqueta entra e sai pela borda; a posição parada é conferida abaixo
            if x0 < SAFE["x0"] - 0.5 or x1 > SAFE["x1"] + 0.5 or y0 < SAFE["y0"] or y1 > SAFE["y1"]:
                fora.append((k, *e))
    R["objetos"] = {"fora_da_zona_segura": fora[:10], "n_fora_da_zona_segura": len(fora),
                    "etiquetas": [{"rotulo": et["rotulo"], "hora": et["hora"], "quadros": [et["q0"], et["q1"]],
                                   "x": et["obj"].x, "y": et["obj"].y, "w": et["obj"].w, "h": et["obj"].h,
                                   "dentro_da_zona_segura_parada": bool(et["obj"].x >= SAFE["x0"] and et["obj"].x + et["obj"].w <= SAFE["x1"]
                                                                         and et["obj"].y >= SAFE["y0"] and et["obj"].y + et["obj"].h <= SAFE["y1"])}
                                  for et in obj["etiquetas"]],
                    "bilhete": {"x": obj["bilhete"].x, "y": obj["bilhete"].y, "w": obj["bilhete"].w, "h": obj["bilhete"].h,
                                "quadros": [obj["bilhete"].q0, obj["bilhete"].q1]},
                    "emocional": {"quadros": [obj["emocional"].q0, obj["emocional"].q1]}}
    # calma entre eventos de marca (DS 4.2: ≥ 1,5 s entre entradas de objetos)
    entradas = sorted([("etiqueta " + et["rotulo"], et["q0"]) for et in obj["etiquetas"]] +
                      [("bilhete", obj["bilhete"].q0), ("emocional", obj["emocional"].q0)], key=lambda x: x[1])
    R["calma"] = [{"de": a[0], "para": b[0], "intervalo_s": round((b[1] - a[1]) / FPS, 3)} for a, b in zip(entradas, entradas[1:])]
    R["calma_minima_s"] = min(c["intervalo_s"] for c in R["calma"])
    R["textos"] = {"legendas": [lg.item["texto"] for lg in obj["legendas"]],
                   "max_caracteres_linha": max(lg.chars_max for lg in obj["legendas"]),
                   "etiquetas": [f"{et['rotulo']} {et['hora']}" for et in obj["etiquetas"]],
                   "bilhete": CFG["bilhete"]["texto"], "emocional": [L["texto"] for L in CFG["emocional"]["linhas"]]}
    R["planos"] = [{"n": p["n"], "arquivo": p["arquivo"], "trecho_s": [p["in"], round(p["in"] + p["nq"] / FPS, 3)],
                    "reel_s": [round(p["r0"] / FPS, 3), round(p["r1"] / FPS, 3)], "hora": p["hora"], "cena": p["cena"]}
                   for p in PLANOS]
    luma = []
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", SAIDA, "-vf", "scale=54:96", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True, check=True)
    luma = np.frombuffer(r.stdout, np.uint8).reshape(-1, 96, 54).mean((1, 2))
    R["video"] = {"quadros_pretos": int((luma < 16).sum()), "luma_media_min": round(float(luma.min()), 1)}
    return R


def frames_qa(obj):
    shutil.rmtree(QA_DIR, ignore_errors=True)
    os.makedirs(QA_DIR)
    alvos = []
    for p in PLANOS:
        alvos.append((f"plano{p['n']:02d}_meio", (p["r0"] + p["r1"]) // 2))
    for et in obj["etiquetas"]:
        alvos.append((f"etiqueta_{et['hora'].replace(':', 'h')}", et["q0"] + 10))
    alvos += [("q000", 0), ("bilhete", obj["bilhete"].q0 + 20), ("emocional", obj["emocional"].q0 + 16), ("ultimo", N - 1)]
    alvos += [(f"legenda{i + 1}", (lg.item["q0"] + lg.item["q1"]) // 2) for i, lg in enumerate(obj["legendas"])]
    alvos = sorted(set(alvos), key=lambda x: x[1])
    lista = []
    for nome, k in alvos:
        arq = os.path.join(QA_DIR, f"rev1_q{k:03d}_{nome}.jpg")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1, "-q:v", 2, arq])
        lista.append((nome, k, arq))
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    folha = Image.new("RGB", (cols * cw, ((len(lista) + cols - 1) // cols) * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (nome, k, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc], outline=(255, 0, 0))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"{nome} q{k} {k / FPS:.2f}s", fill=(0, 0, 0))
    folha.save(os.path.join(QA_DIR, "folha_qa_rev1.jpg"), quality=90)
    return [(n, k, os.path.relpath(a, REV)) for n, k, a in lista]


def main():
    os.makedirs(TMP, exist_ok=True)
    print(f"{len(PLANOS)} planos, {N} quadros, {N / FPS:.3f} s")
    for p in PLANOS:
        print(f"   P{p['n']:02d} {p['arquivo']} {p['in']:.2f}–{p['in'] + p['nq'] / FPS:.2f} s → {p['r0'] / FPS:6.3f}–{p['r1'] / FPS:6.3f}  {p['cena']}")
    obj = {"legendas": [Legenda(it) for it in itens_legenda()], "etiquetas": etiquetas(), "bilhete": Bilhete(),
           "emocional": Emocional()}
    print("áudio")
    wav, ganhos = montar_audio()
    print("vídeo")
    reg = montar_video(obj, wav)
    if ARGS.sem_qa:
        return
    print("QA")
    R = qa(reg, obj, ganhos)
    R["frames_qa"] = frames_qa(obj)
    R["sha256"] = hashlib.sha256(open(SAIDA, "rb").read()).hexdigest()
    R["fontes"] = {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest()
                   for f in sorted(glob.glob(os.path.join(FONTES, "*.ttf")))}
    R["cortes"] = {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest()
                   for p in PLANOS for _, _, f in fonte_do_plano(p)[0]}
    json.dump(R, open(os.path.join(REV, "relatorio_tecnico_rev1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: R[k] for k in ("formato", "audio", "video", "calma_minima_s")}, ensure_ascii=False, indent=1, default=str))
    print(SAIDA)


if __name__ == "__main__":
    sys.exit(main())
