"""Revisão 8 do Reel de apresentação: reel_apresentacao_rev8.mp4.

É a REV7 no Design System REV 2 "Objetos do Primeiro Dia" (v2.0.0). Cortes, narração, mixagem e textos vêm da
REV7 (rev7/rev7.json); só a camada visual muda. Não toca em nenhum arquivo da REV6 nem da REV7.

O que muda (DS REV 2):
  - placa esmaltada PRIMEIRO DIA + módulo de seta (relevo, filete, rebites, grão, sombra de duas camadas),
    com a assinatura Chegada (entra pela esquerda, passa 24 px e assenta; o módulo sai de trás da face;
    brilho de esmalte) e saída pela direita em 240 ms
  - legendas no estilo Padrão (sem caixa): Barlow 700 56, #FCFBF8, sombra de texto, scrim grafite, palavra a
    palavra no tempo da fala (grupo inteiro quando a fala passa de 3 palavras/s)
  - destaque por mini-placa esmaltada que pula quando a palavra é dita
  - scrim inferior sempre ligado e grão de 5% no vídeo

Etapas:
  1. tempos   : legendas pela REV7 (SRT + forma de onda) + correções de sincronia e início de cada palavra
  2. graficos : placa, legendas e fechamento, compostos quadro a quadro em float (sRGB)
  3. audio    : a mesma remontagem da REV7, sem ganho
  4. video    : base decodificada em RGB 16 bits → grão → scrim → objetos → H.264 / AAC 48 kHz
  5. qa       : testes técnicos, frames de QA, folha de contato e relatorio_tecnico_rev8.json

Uso:
  python3 rev8/scripts/rev8.py --fontes PASTA_COM_AS_TTF
Fontes (SIL OFL, Google Fonts):
  https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Bold.ttf
  https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/BarlowCondensed-ExtraBold.ttf
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

REV8 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REV8, "rev8.json"), encoding="utf-8"))
C7 = json.load(open(os.path.normpath(os.path.join(REV8, CFG["rev7_json"])), encoding="utf-8"))
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
N = CFG["quadros_total"]
SPF = SR // FPS
MS = 1000 / FPS  # 41,667 ms por quadro
TMP = os.path.join(REV8, "_tmp")
BASE = os.path.normpath(os.path.join(REV8, CFG["base"]))
SAIDA = os.path.join(REV8, CFG["saida"])
PREVIA = os.path.join(REV8, CFG["saida_previa"])
REV7_MP4 = os.path.normpath(os.path.join(REV8, "..", "rev7", C7["saida"]))
QA_DIR = os.path.join(REV8, "qa_frames")
SS = 4  # supersampling dos objetos
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
T = CFG["tokens"]
SAFE = T["safe"]

TEXTOS_APROVADOS = [
    "Buenos días, Barcelona!", "Eu sou o Diego,", "sou soteropolitano", "e aqui eu te mostro", "o primeiro dia",
    "em cada cidade que eu visito,", "a chegada,", "os meus perrengues", "e o que mais me surpreende,",
    "até porque o primeiro dia\na gente nunca esquece.", "Chegamos!", "E agora eu acabei",
    "de pedir minha primeira", "tapa de Barcelona.",
]
MINI_PLACAS_APROVADAS = ["soteropolitano", "perrengues"]


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
    """valor dos keyframes [(ms, valor), …] no instante t (ms); curva por segmento."""
    if t <= chaves[0][0]:
        return chaves[0][1]
    for (t0, v0), (t1, v1) in zip(chaves, chaves[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * curva((t - t0) / (t1 - t0))
    return chaves[-1][1]


# ---------------------------------------------------------------- linha do tempo (igual à REV7)

def planos():
    out, r = [], 0
    for p in C7["planos"]:
        o0, o1 = q(p["origem"][0]), q(p["origem"][1])
        out.append({**p, "o0": o0, "o1": o1, "r0": r, "r1": r + (o1 - o0)})
        r += o1 - o0
    assert r == N, f"soma dos planos = {r} quadros, esperado {N}"
    return out


def blocos():
    bl = []
    for p in planos():
        if bl and bl[-1]["o1"] == p["o0"]:
            bl[-1]["o1"], bl[-1]["r1"] = p["o1"], p["r1"]
            bl[-1]["planos"].append(p["n"])
        else:
            bl.append({"o0": p["o0"], "o1": p["o1"], "r0": p["r0"], "r1": p["r1"], "planos": [p["n"]]})
    return bl


def origem_para_rev(t):
    for p in planos():
        if p["o0"] / FPS <= t < p["o1"] / FPS:
            return t - p["o0"] / FPS + p["r0"] / FPS
    raise ValueError(t)


def cortes():
    return [p["r0"] / FPS for p in planos()][1:] + [N / FPS]


# ---------------------------------------------------------------- 1. tempos das legendas

def ler_srt(caminho):
    txt = open(caminho, encoding="utf-8").read().strip()
    out = {}
    for bloco in re.split(r"\n\s*\n", txt):
        linhas = bloco.strip().splitlines()
        a, b = re.findall(r"(\d+):(\d+):(\d+),(\d+)", linhas[1])
        seg = lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000  # noqa: E731
        out[int(linhas[0])] = (seg(*a), seg(*b), " ".join(linhas[2:]))
    return out


def audio_base():
    f = os.path.join(TMP, "base_audio.f32")
    if not os.path.exists(f):
        rodar(["ffmpeg", "-v", "error", "-y", "-i", BASE, "-map", "0:a", "-f", "f32le", "-ac", 2, "-ar", SR, f])
    return np.fromfile(f, dtype=np.float32).reshape(-1, 2)


def trechos_vozeados(mono, t0, t1, f0=(115, 210), r_min=0.5, e_min=-21.0, hop=0.01, win=0.03):
    """Mesma medida da REV7: voz do Diego por autocorrelação (f0 115–210 Hz, nível > −21 dBFS)."""
    n = int(win * SR)
    lo, hi = int(SR / 300), int(SR / 100)
    out, cur = [], None
    for t in np.arange(t0, t1, hop):
        s = mono[int(t * SR):int(t * SR) + n].astype(np.float64)
        s = np.convolve(s - s.mean(), np.ones(8) / 8, "same")
        ac = np.correlate(s, s, "full")[n - 1:]
        ac /= ac[0] + 1e-12
        k = int(np.argmax(ac[lo:hi])) + lo
        e = 10 * np.log10((s ** 2).mean() + 1e-12)
        v = ac[k] > r_min and f0[0] < SR / k < f0[1] and e > e_min
        if v and cur is None:
            cur = t
        if not v and cur is not None:
            out.append((round(float(cur), 3), round(float(t), 3)))
            cur = None
    if cur is not None:
        out.append((round(float(cur), 3), round(float(t1), 3)))
    return out


def tempos_legendas():
    """Tempos da REV7 (SRT e forma de onda) + as duas correções de sincronia do rev8.json."""
    srt = ler_srt(os.path.normpath(os.path.join(REV8, CFG["srt_narracao"])))
    mono = audio_base().mean(1)
    corr = CFG["correcoes_sincronia"]
    leg, tapa = [], None
    for L in C7["legendas"]:
        item = {"texto": L["texto"], "fonte_tempo": L["fonte_tempo"]}
        if L["fonte_tempo"] == "srt":
            ini_o, fim_o = srt[L["srt"][0]][0], srt[L["srt"][-1]][1]
        elif L.get("grupo") == "tapa":
            if tapa is None:
                tv = trechos_vozeados(mono, *L["janela_origem"])
                tapa = (tv[0][0], tv[-1][1])
            grupo = [x for x in C7["legendas"] if x.get("grupo") == "tapa"]
            k = grupo.index(L)
            ini_o = tapa[0] if k == 0 else corr[L["texto"]]["inicio_origem"]
            fim_o = tapa[1] if k == len(grupo) - 1 else None
            if L["texto"] in corr:
                item["correcao"] = {"rev7_origem": corr[L["texto"]]["rev7"], "rev8_origem": ini_o}
        else:
            tv = trechos_vozeados(mono, *L["janela_origem"])
            ini_o, fim_o = tv[0][0], tv[-1][1]
        item["origem"] = [ini_o, fim_o]
        leg.append(item)
    for L in leg:
        ini = origem_para_rev(L["origem"][0])
        L["fala_rev"] = [round(ini, 3), round(origem_para_rev(L["origem"][1] - 1e-6), 3) if L["origem"][1] else None]
        L["q0"] = q(ini)
    cs = cortes()
    for i, L in enumerate(leg):
        prox = leg[i + 1]["q0"] if i + 1 < len(leg) else N
        L["q1"] = min(prox, min(q(c) for c in cs if q(c) > L["q0"]))
        L["de"], L["ate"] = round(L["q0"] / FPS, 3), round(L["q1"] / FPS, 3)
    # palavras: modo (palavra a palavra ou grupo) pela velocidade da fala (DS 3.3, freio 4)
    po = CFG["palavras_origem"]
    for i, L in enumerate(leg):
        palavras = L["texto"].replace("\n", " ").split()
        fim = L["fala_rev"][1] if L["fala_rev"][1] else leg[i + 1]["q0"] / FPS
        L["palavras_por_s"] = round(len(palavras) / max(fim - L["fala_rev"][0], 1e-3), 2)
        L["modo"] = "palavra" if L["palavras_por_s"] <= CFG["legenda"]["palavras_por_s_max_palavra_a_palavra"] else "grupo"
        if L["modo"] == "palavra":
            assert L["texto"] in po and len(po[L["texto"]]) == len(palavras), L["texto"]
            L["palavras_q"] = [max(L["q0"], q(origem_para_rev(t))) for t in po[L["texto"]]]
            L["palavras_q"][0] = L["q0"]
            assert all(L["q0"] <= x < L["q1"] for x in L["palavras_q"]), (L["texto"], L["palavras_q"], L["q1"])
        L["texto_tela"] = CFG["quebras_de_linha"].get(L["texto"].replace("*", ""), None)
        if L["texto_tela"]:
            # reaplica os * de destaque se houver (não há nas duas frases quebradas)
            assert "*" not in L["texto"]
        else:
            L["texto_tela"] = L["texto"]
    return leg


# ---------------------------------------------------------------- 2. objetos

def fonte(nome, px, pasta):
    return ImageFont.truetype(os.path.join(pasta, nome), px)


def reduzir(a, s=SS):
    """box downscale de um array (h, w, c) por s."""
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
    """shadow-plate / sombra da mini-placa: borda dura (y, alfa) + projetada (y, blur, spread, alfa). Preto."""
    s1 = deslocar(alfa, dura[0]) * dura[1]
    a = alfa
    if proj["spread"] < 0:
        a = ndimage.grey_erosion(a, size=(2 * -proj["spread"] + 1,) * 2)
    s2 = ndimage.gaussian_filter(deslocar(a, proj["y"]), proj["blur"] / 2) * proj["alfa"]
    return 1 - (1 - s1) * (1 - s2)


def ruido_fractal(h, w, semente):
    """grão de esmalte: ruído em 2 oitavas, [0, 1]."""
    rng = np.random.default_rng(semente)
    n = ndimage.gaussian_filter(rng.standard_normal((h, w)), 0.8) + 0.5 * ndimage.gaussian_filter(
        rng.standard_normal((h, w)), 2.0)
    n = (n - n.min()) / (n.max() - n.min())
    return n.astype(np.float32)


def caminho_seta(lado):
    """seta do bundle do DS (pd-bundle.js, viewBox 100): M8 41h50V18l38 32-38 32V59H8z, em 54% do módulo."""
    P = CFG["placa"]
    k = lado * P["seta_fracao"] / 100
    ox = oy = (lado - lado * P["seta_fracao"]) / 2
    pts = [(8, 41), (58, 41), (58, 18), (96, 50), (58, 82), (58, 59), (8, 59)]
    return [(ox + x * k, oy + y * k) for x, y in pts]


def placa_pecas(pasta):
    """Face (amarelo esmaltado com texto) e módulo de seta, premultiplicados, em 1x."""
    P = CFG["placa"]
    S = SS
    f = fonte(P["fonte"], P["tamanho"] * S, pasta)
    trk = P["tracking_em"] * P["tamanho"] * S
    larg_txt = sum(f.getlength(c) for c in P["texto"]) + trk * (len(P["texto"]) - 1)
    hh = P["altura"]
    fw = int(round(2 * P["padding_h"] + larg_txt / S))
    r = T["radius_plate"]
    # ---- face
    m = mascara((fw * S, hh * S), lambda d: d.rounded_rectangle([0, 0, fw * S - 1, hh * S - 1], radius=r * S,
                                                                fill=255, corners=(True, False, False, True)))
    i_ = P["filete_inset"] * S
    rr = P["filete_raio"] * S
    lw = P["filete_px"] * S

    def filete(d):
        # '[': aberto à direita (border-right: 0), cantos esquerdos com raio 8
        d.line([(fw * S - i_, i_ + lw / 2), (i_ + rr, i_ + lw / 2)], fill=255, width=lw)
        d.line([(fw * S - i_, hh * S - i_ - lw / 2), (i_ + rr, hh * S - i_ - lw / 2)], fill=255, width=lw)
        d.line([(i_ + lw / 2, i_ + rr), (i_ + lw / 2, hh * S - i_ - rr)], fill=255, width=lw)
        d.arc([i_, i_, i_ + 2 * rr, i_ + 2 * rr], 180, 270, fill=255, width=lw)
        d.arc([i_, hh * S - i_ - 2 * rr, i_ + 2 * rr, hh * S - i_], 90, 180, fill=255, width=lw)
    fil = mascara((fw * S, hh * S), filete)
    capH = -f.getbbox("H", anchor="ls")[1]
    base_y = (hh * S - capH) / 2 + capH

    def texto(d):
        x = P["padding_h"] * S
        for c in P["texto"]:
            d.text((x, base_y), c, font=f, fill=255, anchor="ls")
            x += f.getlength(c) + trk
    txt = mascara((fw * S, hh * S), texto)
    rb = P["rebite_px"] * S
    rx, ry = P["rebite_x"] * S, P["rebite_y"] * S
    reb = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx, y, rx + rb, y + rb], fill=255)
                                                for y in (ry, hh * S - ry - rb)])
    luz = mascara((fw * S, hh * S), lambda d: [d.ellipse([rx + rb * .22, y + rb * .18, rx + rb * .52, y + rb * .48],
                                                         fill=255) for y in (ry, hh * S - ry - rb)])
    m, fil, txt, reb, luz = [reduzir(a[..., None])[..., 0] for a in (m, fil, txt, reb, luz)]
    rgb = np.broadcast_to(AMARELO, m.shape + (3,)).copy()
    # grão do esmalte (op-grain 5%, multiply)
    g = ruido_fractal(*m.shape, 7)
    rgb *= (1 - T["op_grain"] * g)[..., None]
    # relevo (shadow-plate-bevel): luz de 2 px em cima, sombra de 4 px embaixo, por dentro da forma
    bl, ba = P["bevel_luz"]
    bs, bsa = P["bevel_sombra"]
    topo = np.clip(m - deslocar(m, bl), 0, 1) * ba
    base = np.clip(m - deslocar(m, -bs), 0, 1) * bsa
    rgb = rgb * (1 - topo[..., None]) + topo[..., None]
    rgb = rgb * (1 - base[..., None])
    # filete grafite 25%
    rgb = rgb * (1 - (fil * P["filete_alfa"])[..., None]) + GRAFITE * (fil * P["filete_alfa"])[..., None]
    # rebites: grafite 35% + ponto de luz + sombra interna embaixo
    rgb = rgb * (1 - (reb * P["rebite_alfa"])[..., None]) + GRAFITE * (reb * P["rebite_alfa"])[..., None]
    rb_sombra = np.clip(reb - deslocar(reb, -1.5), 0, 1) * 0.35
    rgb = rgb * (1 - rb_sombra[..., None])
    rgb = rgb * (1 - (luz * 0.4)[..., None]) + (luz * 0.4)[..., None]
    # texto grafite
    rgb = rgb * (1 - txt[..., None]) + GRAFITE * txt[..., None]
    face = premult(rgb, m)
    # ---- módulo de seta
    lado = P["modulo"]
    mm = mascara((lado * S, hh * S), lambda d: d.rounded_rectangle([0, 0, lado * S - 1, hh * S - 1], radius=r * S,
                                                                   fill=255, corners=(False, True, True, False)))
    seta = mascara((lado * S, hh * S), lambda d: d.polygon([(x * S, y * S + (hh - lado) * S / 2)
                                                            for x, y in caminho_seta(lado)], fill=255))
    mm, seta = [reduzir(a[..., None])[..., 0] for a in (mm, seta)]
    rgbm = np.broadcast_to(GRAFITE, mm.shape + (3,)).copy()
    # painel: filete claro 2 px (7%) + luz de 2 px em cima (8%)
    borda = np.clip(mm - ndimage.grey_erosion(mm, size=(5, 5)), 0, 1) * 0.07
    topo_m = np.clip(mm - deslocar(mm, 2), 0, 1) * 0.08
    for camada in (borda, topo_m):
        rgbm = rgbm * (1 - camada[..., None]) + camada[..., None]
    rgbm = rgbm * (1 - seta[..., None]) + AMARELO * seta[..., None]
    modulo = premult(rgbm, mm)
    medidas = {"face_largura": fw, "modulo_largura": lado, "altura": hh, "largura_total": fw + lado,
               "texto_px": P["tamanho"], "texto_avanco_px": round(larg_txt / S, 1), "seta_px": round(lado * P["seta_fracao"], 1)}
    return face, modulo, medidas


def soft_light_branco(b, a):
    """soft-light (W3C) de branco sobre b com alfa a: B = D(b)."""
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
        """Estado da placa em t_ms desde o início da Chegada (ou saida_ms desde o início da saída)."""
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
        """(imagem premultiplicada, x, y) da placa no estado e; arredonda o estado para o cache."""
        chave = tuple(round(v, 2) if isinstance(v, float) else v for v in
                      (e["dx"], e["rot"], e["blur"], e["mx"], e["sy"], e["sa"], e["sda"], e["brilho"]))
        if chave in self.cache:
            return self.cache[chave]
        P = CFG["placa"]
        pad = self.PAD
        lado = self.modulo.shape[1]
        tela = np.zeros((self.hh + 2 * pad, self.fw + lado + 2 * pad, 4), np.float32)
        # módulo atrás da face (sai de trás dela na Chegada)
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
        dx = e["dx"]
        res = (out, int(round(P["x"] + dx)) - pad, P["y"] - pad)
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
        rgb = soft_light_branco(rgb, perfil * (a > 0))
        return premult(rgb, a)


# ---------------------------------------------------------------- legendas

def segmentos(linha):
    partes = re.split(r"(\*[^*]+\*)", linha)
    return [(p.strip("*"), p.startswith("*")) for p in partes if p]


class Legenda:
    """Legenda Padrão do DS REV 2 (sem caixa), com destaque por mini-placa e entrada palavra a palavra."""
    MARGEM = 60

    def __init__(self, item, pasta, texto=None):
        L = CFG["legenda"]
        self.item = item
        texto = texto if texto is not None else item["texto_tela"]
        S = SS
        f = fonte(L["fonte"], L["tamanho"] * S, pasta)
        lh = L["tamanho"] * L["entrelinha"]
        asc, desc = f.getmetrics()
        linhas = texto.split("\n")
        D = L["destaque"]
        # layout (1x, coordenadas do quadro)
        topo = L["base_y"] - len(linhas) * lh
        self.topo, self.base = topo, L["base_y"]
        self.linhas = [ln.replace("*", "") for ln in linhas]
        esp = f.getlength(" ") / S
        palavras = []
        for i, ln in enumerate(linhas):
            toks = []
            for s, hl in segmentos(ln):
                for w in s.split():
                    toks.append((w, hl))
            larg = [f.getlength(w) / S + (2 * D["padding_h"] if hl else 0) for w, hl in toks]
            total = sum(larg) + esp * (len(toks) - 1)
            x = L["centro_x"] - total / 2
            ltop = topo + i * lh
            base_y = ltop + (lh - (asc + desc) / S) / 2 + asc / S
            for (w, hl), lw in zip(toks, larg):
                palavras.append({"w": w, "hl": hl, "x": x, "larg": lw, "base_y": base_y, "ltop": ltop, "linha": i})
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
                self.mascaras.append(reduzir(mk[..., None])[..., 0])
            else:
                self.mascaras.append(None)
                self.destaques[j] = self.mini_placa(p, f)
        # extensão do texto (tinta), para o QA de zona segura
        tinta = [np.nonzero(mk.any(0))[0] for mk in self.mascaras if mk is not None]
        self.ret = [min(p["x"] - (D["padding_h"] if p["hl"] else 0) for p in palavras),
                    topo, max(p["x"] + p["larg"] for p in palavras), L["base_y"]]
        self.chars_max = max(len(x) for x in self.linhas)
        self.n_linhas = len(self.linhas)

    def mini_placa(self, p, f):
        """mini-placa: amarelo, radius-tag, padding 4/14, relevo + sombra; texto grafite (premultiplicado, 1x)."""
        L = CFG["legenda"]
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

    def estado(self, k, ultimo=False):
        """opacidade, subida e escala de cada palavra no quadro k (None = grupo fora da tela)."""
        it = self.item
        L = CFG["legenda"]
        if not (it["q0"] <= k < it["q1"]):
            return None
        # saída do grupo (120 ms, sobe 6 px), terminando no quadro de saída; não há saída no último quadro do vídeo
        nsai = int(round(L["saida_ms"] / MS))
        se = 0.0
        if not ultimo and k >= it["q1"] - nsai:
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
            t = (k - kq + 1) * MS  # o quadro de entrada já mostra a palavra entrando
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
                # escala em torno do centro da caixa
                cy, cx = d["cy"], d["cx"]
                mat = np.array([[1 / esc, 0], [0, 1 / esc]])
                off = np.array([cy, cx]) - mat @ np.array([cy, cx])
                img = np.dstack([ndimage.affine_transform(img[..., i], mat, offset=off, order=1) for i in range(4)])
            img = img * op
            if abs(dy) > 1e-3:
                img = deslocar(img, dy)
            sobre(out, img, d["x"] - self.x0, d["y"] - self.y0)
        return out


# ---------------------------------------------------------------- composição do quadro

def scrim_alfa():
    S = CFG["scrim"]
    y = np.arange(H, dtype=np.float32)
    return (np.clip((y - S["y0"]) / (S["y1"] - S["y0"]), 0, 1) * T["op_scrim"])[:, None, None]


def grao(k):
    """grão de 5% (blend overlay), novo a cada quadro, intensidade fixa."""
    G = CFG["grao"]
    rng = np.random.default_rng(G["semente"] + k)
    z = ndimage.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), G["sigma_px"])
    z /= z.std()
    return np.clip(0.5 + 0.289 * z, 0, 1)[..., None]


def overlay_blend(b, n, op):
    o = np.where(b < 0.5, 2 * b * n, 1 - 2 * (1 - b) * (1 - n))
    return b + op * (o - b)


def linha_do_tempo_placa(k):
    """estado da placa no quadro k: Chegada a partir do quadro 0 (o quadro 0 já mostra t = 1 quadro),
    parada, saída de 240 ms terminando no corte de 2,458 s."""
    P = CFG["placa"]
    q_fim = q(P["saida"]["ultimo_quadro_s"])  # primeiro quadro sem placa (59)
    n_sai = int(round(P["saida"]["duracao_ms"] / MS))  # 6 quadros
    if k >= q_fim:
        return None
    if k >= q_fim - n_sai + 1:
        return ("saida", (k - (q_fim - n_sai)) * MS)
    return ("chegada", (k + 1) * MS)


def compor(placa, legendas, fech, scrim, base_rgb, k, registro):
    img = overlay_blend(base_rgb, grao(k), T["op_grain"])
    img = img * (1 - scrim) + GRAFITE * scrim
    camada = np.zeros((H, W, 4), np.float32)
    elementos = []
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
        ws = lg.estado(k, ultimo=(lg.item["q1"] == N))
        if ws is None:
            continue
        sobre(camada, lg.camada(ws), lg.x0, lg.y0)
        elementos.append(("legenda", *[round(v, 1) for v in lg.ret], lg.item["texto"].replace("*", ""),
                          round(max(o for o, _, _ in ws), 3)))
    registro[k] = elementos
    a = camada[..., 3:4]
    return img * (1 - a) + camada[..., :3]


# ---------------------------------------------------------------- 3. áudio (idêntico à REV7)

def montar_audio():
    A = C7["audio"]
    src = audio_base()
    h = int(round(A["crossfade_s"] * SR / 2))
    mix = np.zeros((N * SPF, 2), np.float64)
    bl = blocos()
    emendas = []
    for i, b in enumerate(bl):
        o0, o1 = b["o0"] * SPF, b["o1"] * SPF
        r0, r1 = b["r0"] * SPF, b["r1"] * SPF
        ha = h if i > 0 else 0
        hb = h if i < len(bl) - 1 else 0
        trecho = src[o0 - ha:o1 + hb].astype(np.float64)
        env = np.ones(len(trecho))
        if ha:
            env[:2 * ha] = np.sin(np.linspace(0, np.pi / 2, 2 * ha, endpoint=False) + np.pi / (8 * ha))
        if hb:
            env[-2 * hb:] = np.cos(np.linspace(0, np.pi / 2, 2 * hb, endpoint=False) + np.pi / (8 * hb))
        mix[r0 - ha:r1 + hb] += trecho * env[:, None]
        if i > 0:
            emendas.append(round(r0 / SR, 3))
    assert emendas == [round(x, 3) for x in A["emendas_novas_s"]]
    dc = int(A["declique_ms"] * SR / 1000)
    rampa = np.linspace(0, 1, dc, endpoint=False)
    mix[:dc] *= rampa[:, None]
    mix[-dc:] *= rampa[::-1][:, None]
    mix *= 10 ** (A["ganho_db"] / 20)
    wav = os.path.join(TMP, "audio_rev8.f32")
    mix.astype(np.float32).tofile(wav)
    return wav, mix, src, emendas


# ---------------------------------------------------------------- 4. vídeo

def montar_video(placa, legendas, fech, wav):
    pl = blocos()
    entradas, filtros, rotulos = [], [], []
    for i, b in enumerate(pl):
        entradas += ["-i", BASE]
        filtros.append(f"[{i}:v]trim=start_frame={b['o0']}:end_frame={b['o1']},setpts=PTS-STARTPTS[v{i}]")
        rotulos.append(f"[v{i}]")
    filtros.append(f"{''.join(rotulos)}concat=n={len(pl)}:v=1:a=0,setpts=N/({FPS}*TB),"
                   "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb48le[v]")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", *entradas, "-filter_complex", ";".join(filtros), "-map", "[v]",
                            "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", SAIDA]], stdin=subprocess.PIPE)
    scrim = scrim_alfa()
    registro = {}
    tam = W * H * 3 * 2
    for k in range(N):
        buf = dec.stdout.read(tam)
        assert len(buf) == tam, f"quadro {k} incompleto"
        base_rgb = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
        out = compor(placa, legendas + [fech], None, scrim, base_rgb, k, registro)
        enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
        if k % 50 == 0:
            print(f"   quadro {k}/{N}", flush=True)
    dec.stdout.close()
    enc.stdin.close()
    assert dec.wait() == 0 and enc.wait() == 0
    # prévia leve (720 × 1280) para celular
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


def quadros_cinza(arq, n_max):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", "scale=270:480:flags=area", "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, 480, 270)[:n_max].astype(np.float32)


def psnr(a, b):
    mse = ((a - b) ** 2).mean()
    return 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def audio_decodificado(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a", "-f", "f32le", "-ac", "2", "-ar", str(SR),
                        "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2)


def qa(leg, legendas, placa, registro, mix, src, emendas):
    R = {"arquivo": os.path.relpath(SAIDA, os.path.dirname(REV8))}
    pr = ffprobe(SAIDA)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "duracao_video_s": float(v["duration"]),
                    "duracao_audio_s": float(a["duration"]), "codec_video": f"{v['codec_name']} ({v.get('profile')})",
                    "pix_fmt": v["pix_fmt"],
                    "cor": f"{v.get('color_primaries')}/{v.get('color_transfer')}/{v.get('color_space')}/{v.get('color_range')}",
                    "codec_audio": f"{a['codec_name']} ({a.get('profile')})", "sr_audio": int(a["sample_rate"]),
                    "canais": a["channels"], "tamanho_bytes": int(pr["format"]["size"])}
    R["previa"] = {"arquivo": os.path.basename(PREVIA), "tamanho_bytes": os.path.getsize(PREVIA)}
    lufs, tp = ebur128(SAIDA)
    R["audio"] = {"lufs_integrado": lufs, "pico_verdadeiro_dbtp": tp}
    # áudio: a REV8 tem de ser a REV7, amostra por amostra (mesma mixagem e mesmo encoder)
    a8, a7 = audio_decodificado(SAIDA), audio_decodificado(REV7_MP4)
    n = min(len(a8), len(a7))
    R["audio"]["comparacao_rev7"] = {"amostras_rev8": len(a8), "amostras_rev7": len(a7),
                                     "diferenca_max": float(np.abs(a8[:n] - a7[:n]).max()),
                                     "identico": bool(len(a8) == len(a7) and np.array_equal(a8, a7))}
    lufs7, tp7 = ebur128(REV7_MP4)
    R["audio"]["rev7"] = {"lufs_integrado": lufs7, "pico_verdadeiro_dbtp": tp7}
    R["audio"]["emendas_s"] = emendas

    # vídeo: cada quadro = quadro de origem da REV7 (região sem objetos e sem scrim, y < 1060)
    out = quadros_cinza(SAIDA, N)
    base = quadros_cinza(BASE, 10 ** 6)
    r7 = quadros_cinza(REV7_MP4, N)
    yl = int(1060 / 4)
    mapa = [p["o0"] + k - p["r0"] for p in planos() for k in range(p["r0"], p["r1"])]
    acertos, ps, piores = 0, [], []
    for k in range(N):
        m = mapa[k]
        cand = {d: psnr(out[k, :yl], base[m + d, :yl]) for d in (-1, 0, 1) if 0 <= m + d < len(base)}
        ps.append(cand[0])
        if max(cand, key=cand.get) == 0:
            acertos += 1
        else:
            piores.append({"quadro": k, "psnr_exato": round(cand[0], 1)})
    mesmo_rev7 = [psnr(out[k, :yl], r7[k, :yl]) for k in range(N)]
    luma = out.mean(axis=(1, 2))
    R["video"] = {"mapeamento_quadros_corretos": acertos, "de": N, "psnr_min_db": round(min(ps), 1),
                  "psnr_mediana_db": round(float(np.median(ps)), 1), "divergencias": piores[:10],
                  "psnr_min_vs_rev7_db": round(min(mesmo_rev7), 1),
                  "diferenca_luma_media_vs_origem_y_menor_1060": round(float(
                      (out[:, :yl].mean() - base[mapa][:, :yl].mean())), 3),
                  "quadros_pretos": int((luma < 16).sum()), "luma_media_min": round(float(luma.min()), 1)}
    cs = [round(c, 3) for c in cortes()[:-1]]
    R["video"]["cortes_s"] = cs
    R["video"]["cortes_iguais_rev7"] = cs == [round(p["r0"] / FPS, 3) for p in planos()][1:]

    # objetos: zona segura, sobreposição, legendas
    fora, sobrep = [], []
    for k in range(N):
        els = registro[k]
        for e in els:
            nome, x0, y0, x1, y1 = e[:5]
            parada = not (nome == "placa" and e[5] == "saida") and not (
                nome == "placa" and e[5] == "chegada" and e[6] < 400)
            if parada and (x0 < SAFE["x0"] - 0.5 or x1 > SAFE["x1"] + 0.5 or y0 < SAFE["y0"] or y1 > SAFE["y1"]):
                fora.append((k, *e))
        pl = [e for e in els if e[0] == "placa"]
        for e in els:
            if pl and e[0] == "legenda" and e[2] < pl[0][4]:
                sobrep.append((k, e[5]))
    P = CFG["placa"]
    R["objetos"] = {
        "placa": {**placa.medidas, "x": P["x"], "y": P["y"], "x_final": P["x"] + placa.medidas["largura_total"],
                  "y_final": P["y"] + placa.medidas["altura"],
                  "quadros_chegada": [k for k in range(N) if linha_do_tempo_placa(k) and linha_do_tempo_placa(k)[0] == "chegada"
                                      and linha_do_tempo_placa(k)[1] < 1300 + MS],
                  "quadros_saida": [k for k in range(N) if linha_do_tempo_placa(k) and linha_do_tempo_placa(k)[0] == "saida"],
                  "primeiro_quadro_sem_placa": q(P["saida"]["ultimo_quadro_s"]),
                  "x_face_por_quadro": {k: registro[k][0][1] for k in range(0, 60) if registro[k] and registro[k][0][0] == "placa"}},
        "fora_da_zona_segura_parado": fora[:10], "n_fora_da_zona_segura_parado": len(fora),
        "legenda_sobre_placa": sobrep[:10], "n_legenda_sobre_placa": len(sobrep)}
    pl_fim = P["y"] + placa.medidas["altura"]
    R["objetos"]["folga_placa_legenda_px"] = round(min(lg.topo for lg in legendas if lg.item["q0"] < q(P["saida"]["ultimo_quadro_s"])) - pl_fim, 1)
    # amostras de cor (camadas sem vídeo)
    fx = placa.face
    R["objetos"]["amostras_cor"] = {
        "face_placa_media": "#%02X%02X%02X" % tuple(int(round(c * 255)) for c in fx[60:110, 20:30, :3].reshape(-1, 3).mean(0)),
        "modulo_media": "#%02X%02X%02X" % tuple(int(round(c * 255)) for c in placa.modulo[20:40, 20:40, :3].reshape(-1, 3).mean(0))}

    # textos
    textos = [L["texto"].replace("*", "") for L in leg]
    minis = [p["w"] for lg in legendas for p in lg.palavras if p["hl"]]
    R["textos"] = {"iguais_aos_aprovados": textos == TEXTOS_APROVADOS,
                   "na_tela_iguais_ignorando_quebra": [" ".join(lg.linhas) for lg in legendas] ==
                   [t.replace("\n", " ") for t in TEXTOS_APROVADOS],
                   "mini_placas": minis, "mini_placas_ok": minis == MINI_PLACAS_APROVADAS,
                   "linhas_na_tela": [lg.linhas for lg in legendas],
                   "max_caracteres_linha": max(lg.chars_max for lg in legendas),
                   "max_linhas": max(lg.n_linhas for lg in legendas),
                   "topo_min_bloco_y": round(min(lg.topo for lg in legendas), 1),
                   "base_bloco_y": CFG["legenda"]["base_y"],
                   "placa": CFG["placa"]["texto"] + " →", "fechamento": CFG["fechamento"]["texto"]}
    R["legendas"] = [{k: L.get(k) for k in ("texto", "texto_tela", "fonte_tempo", "origem", "fala_rev", "de", "ate", "q0",
                                             "q1", "palavras_por_s", "modo", "palavras_q", "correcao")} for L in leg]
    R["planos"] = [{k: p[k] for k in ("n", "origem", "cena")} | {"rev_s": [round(p["r0"] / FPS, 3), round(p["r1"] / FPS, 3)]}
                   for p in planos()]
    return R


def frames_qa():
    shutil.rmtree(QA_DIR, ignore_errors=True)
    os.makedirs(QA_DIR)
    alvos = [(f"t{t:05.2f}s".replace(".", "_"), min(q(t), N - 1)) for t in CFG["qa_tempos_s"]]
    alvos += [(f"q{k:03d}", k) for k in CFG["qa_quadros"]]
    lista = []
    for nome, k in alvos:
        arq = os.path.join(QA_DIR, f"rev8_{nome}_quadro{k:03d}.jpg")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1, "-q:v", 2, arq])
        lista.append((nome, k, arq))
    # rosto × placa no plano 1: 1 a cada 4 quadros, faixa y 860–1320
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
           f"select='lt(n\\,{q(CFG['placa']['saida']['ultimo_quadro_s'])})*not(mod(n\\,4))',crop={W}:460:0:860,"
           "scale=540:230,tile=3x5", "-frames:v", 1, "-q:v", 2, os.path.join(QA_DIR, "rosto_x_placa_plano1_y860-1320.jpg")])
    # Chegada quadro a quadro (0–20) e saída (52–59), faixa y 1000–1460
    for nome, sel in (("chegada_q00-q19", "lt(n\\,20)"), ("saida_q52-q59", "between(n\\,52\\,59)")):
        n = 20 if nome.startswith("chegada") else 8
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
               f"select='{sel}',crop={W}:460:0:1000,scale=540:230,tile=4x{(n + 3) // 4}", "-frames:v", 1,
               "-q:v", 2, os.path.join(QA_DIR, f"placa_{nome}.jpg")])
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
        d.text((x + 4, y + ch + 6), f"{nome}  quadro {k}  {k / FPS:.3f} s", fill=(0, 0, 0))
    folha.save(os.path.join(QA_DIR, "folha_qa_rev8.jpg"), quality=90)
    # REV7 × REV8 lado a lado nos mesmos quadros
    pares = [0, 3, 48, 94, 226, 300, 389, 540, 580, 620]
    lado = Image.new("RGB", (len(pares) * 2 * 216 + (len(pares) - 1) * 12, 384 + 26), (255, 255, 255))
    dd = ImageDraw.Draw(lado)
    for i, k in enumerate(pares):
        for j, arq in enumerate((REV7_MP4, SAIDA)):
            tmp = os.path.join(TMP, f"par_{j}_{k}.png")
            rodar(["ffmpeg", "-v", "error", "-y", "-i", arq, "-vf", f"select=eq(n\\,{k}),scale=216:384", "-frames:v", 1, tmp])
            x = i * (2 * 216 + 12) + j * 216
            lado.paste(Image.open(tmp).convert("RGB"), (x, 0))
            dd.text((x + 4, 390), f"{'REV7' if j == 0 else 'REV8'} q{k}", fill=(0, 0, 0))
    lado.save(os.path.join(QA_DIR, "rev7_x_rev8.jpg"), quality=90)
    return [(n, k, os.path.relpath(a, REV8)) for n, k, a in lista]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True, help="pasta com Barlow-Bold.ttf e BarlowCondensed-ExtraBold.ttf")
    args = ap.parse_args()
    os.makedirs(TMP, exist_ok=True)
    print("1/5 tempos das legendas")
    leg = tempos_legendas()
    for L in leg:
        print(f"   {L['de']:7.3f}–{L['ate']:7.3f}  {L['modo']:7s} {L['palavras_por_s']:4.1f}/s  {L['texto_tela']!r}"
              f"{'  palavras ' + str(L['palavras_q']) if L['modo'] == 'palavra' else ''}")
    print("2/5 objetos")
    placa = Placa(args.fontes)
    legendas = [Legenda(L, args.fontes) for L in leg]
    F = CFG["fechamento"]
    fech = Legenda({"texto": F["texto"], "texto_tela": F["texto"], "q0": q(F["de"]), "q1": q(F["ate"]), "modo": "grupo"},
                   args.fontes)
    print("   placa", placa.medidas)
    print("3/5 áudio")
    wav, mix, src, emendas = montar_audio()
    print("4/5 vídeo")
    registro = montar_video(placa, legendas, fech, wav)
    print("5/5 QA")
    R = qa(leg, legendas, placa, registro, mix, src, emendas)
    R["fechamento"] = {"texto": F["texto"], "quadros": [q(F["de"]), q(F["ate"])], "ret": [round(v, 1) for v in fech.ret]}
    R["frames_qa"] = frames_qa()
    R["sha256"] = hashlib.sha256(open(SAIDA, "rb").read()).hexdigest()
    R["fontes"] = {n: hashlib.sha256(open(os.path.join(args.fontes, n), "rb").read()).hexdigest()
                   for n in ("Barlow-Bold.ttf", "BarlowCondensed-ExtraBold.ttf")}
    json.dump(R, open(os.path.join(REV8, "relatorio_tecnico_rev8.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: R[k] for k in ("formato", "audio", "video", "textos")}, ensure_ascii=False, indent=1, default=str))
    print(SAIDA)


if __name__ == "__main__":
    sys.exit(main())
