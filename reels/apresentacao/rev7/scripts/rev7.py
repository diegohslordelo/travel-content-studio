"""Revisão 7 do Reel de apresentação: reel_apresentacao_rev7.mp4.

Reconstrução visual/editorial da REV6 a partir de reel_apresentacao_sem_texto_rev6.mp4, no Design System v1.0.1
"Placa & Caneta" com as decisões da REV7 (CLAUDE.md §11). Não toca em nenhum arquivo da REV6.

Etapas:
  1. tempos   : legendas da narração pelo SRT da REV6; falas sem SRT medidas na forma de onda (voz do Diego)
  2. graficos : placa PRIMEIRO DIA →, legendas, mini-placas e fechamento @primeirodiaem (PNG RGBA por quadro)
  3. audio    : remontagem da mixagem da base, crossfade de 0,1 s só nas emendas novas, sem ganho
  4. video    : cortes por número de quadro + sobreposição dos gráficos, H.264 / AAC 48 kHz
  5. qa       : testes técnicos, frames de QA, folha de contato, relatorio_tecnico_rev7.json e QA_REV7.md

Uso:
  python3 rev7/scripts/rev7.py --fontes PASTA_COM_AS_TTF
As fontes (Barlow-SemiBold.ttf e BarlowCondensed-ExtraBold.ttf, SIL OFL) vêm do Google Fonts:
  https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-SemiBold.ttf
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

REV7 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REV7, "rev7.json"), encoding="utf-8"))
FPS = CFG["fps"]
SR = CFG["sr"]
W, H = CFG["largura"], CFG["altura"]
N = CFG["quadros_total"]
SPF = SR // FPS  # 2000 amostras por quadro
TMP = os.path.join(REV7, "_tmp")
BASE = os.path.normpath(os.path.join(REV7, CFG["base"]))
SAIDA = os.path.join(REV7, CFG["saida"])
QA_DIR = os.path.join(REV7, "qa_frames")
SS = 4  # supersampling dos gráficos (cantos e seta antialiasados)
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]

# Textos aprovados pelo Diego (handoff da REV7). O QA compara caractere a caractere.
TEXTOS_APROVADOS = [
    "Buenos días, Barcelona!", "Eu sou o Diego,", "sou soteropolitano", "e aqui eu te mostro", "o primeiro dia",
    "em cada cidade que eu visito,", "a chegada,", "os meus perrengues", "e o que mais me surpreende,",
    "até porque o primeiro dia\na gente nunca esquece.", "Chegamos!", "E agora eu acabei",
    "de pedir minha primeira", "tapa de Barcelona.",
]
MINI_PLACAS_APROVADAS = ["soteropolitano", "perrengues"]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


AMARELO = hexrgb(CFG["tokens"]["amarelo"])
GRAFITE = hexrgb(CFG["tokens"]["grafite"])
PAPEL = hexrgb(CFG["tokens"]["papel"])
SAFE = CFG["tokens"]["safe"]


def rodar(cmd, **kw):
    cmd = [str(c) for c in cmd]
    return subprocess.run(cmd, check=True, **kw)


def q(t):
    """segundos → quadro (a grade de 24 fps)"""
    return int(round(t * FPS))


# ---------------------------------------------------------------- linha do tempo

def planos():
    """Planos com quadros de origem e de destino."""
    out, r = [], 0
    for p in CFG["planos"]:
        o0, o1 = q(p["origem"][0]), q(p["origem"][1])
        out.append({**p, "o0": o0, "o1": o1, "r0": r, "r1": r + (o1 - o0)})
        r += o1 - o0
    assert r == N, f"soma dos planos = {r} quadros, esperado {N}"
    return out


def blocos():
    """Planos contíguos na origem formam um bloco; emenda nova = fronteira entre blocos."""
    bl = []
    for p in planos():
        if bl and bl[-1]["o1"] == p["o0"]:
            bl[-1]["o1"], bl[-1]["r1"] = p["o1"], p["r1"]
            bl[-1]["planos"].append(p["n"])
        else:
            bl.append({"o0": p["o0"], "o1": p["o1"], "r0": p["r0"], "r1": p["r1"], "planos": [p["n"]]})
    return bl


def origem_para_rev7(t):
    for p in planos():
        if p["o0"] / FPS <= t < p["o1"] / FPS:
            return t - p["o0"] / FPS + p["r0"] / FPS
    raise ValueError(t)


def cortes_rev7():
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
    """Áudio da base em float32, estéreo, 48 kHz (decodificação única, cache em _tmp)."""
    f = os.path.join(TMP, "base_audio.f32")
    if not os.path.exists(f):
        rodar(["ffmpeg", "-v", "error", "-y", "-i", BASE, "-map", "0:a", "-f", "f32le", "-ac", 2, "-ar", SR, f])
    return np.fromfile(f, dtype=np.float32).reshape(-1, 2)


def trechos_vozeados(mono, t0, t1, f0=(115, 210), r_min=0.5, e_min=-21.0, hop=0.01, win=0.03):
    """Trechos com a voz do Diego: autocorrelação (periodicidade > 0,5) com f0 de 115–210 Hz e nível > −21 dBFS.
    A voz do Diego fica em ~140–175 Hz; o fundo do bar tem vozes em ~190–280 Hz e nível mais baixo."""
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


def fronteira(trechos, t_ref, raio=0.6):
    """Fronteira entre duas legendas: início da palavra que vem depois da maior pausa de voz a ±0,6 s da
    referência (tempo de palavra da REV6). A legenda anterior fica na tela durante a pausa."""
    pausas = [(b[0] - a[1], b[0]) for a, b in zip(trechos, trechos[1:])
              if abs(b[0] - t_ref) <= raio or abs(a[1] - t_ref) <= raio]
    return max(pausas)[1], round(max(pausas)[0], 3)


def tempos_legendas():
    srt = ler_srt(os.path.normpath(os.path.join(REV7, CFG["srt_narracao"])))
    mono = audio_base().mean(1)
    cortes = cortes_rev7()
    leg, medidas = [], []
    grupo_tapa = [L for L in CFG["legendas"] if L.get("grupo") == "tapa"]
    tapa_ini = tapa_fim = None
    for L in CFG["legendas"]:
        item = {"texto": L["texto"], "fonte_tempo": L["fonte_tempo"]}
        if L["fonte_tempo"] == "srt":
            ini_o = srt[L["srt"][0]][0]
            fim_o = srt[L["srt"][-1]][1]
            item["srt"] = L["srt"]
            item["origem"] = [ini_o, fim_o]
        elif L.get("grupo") == "tapa":
            if tapa_ini is None:
                j = grupo_tapa[0]["janela_origem"]
                tv = trechos_vozeados(mono, *j)
                tapa_ini, tapa_fim = tv[0][0], tv[-1][1]
                medidas.append({"fala": "plano 11 (frase inteira, voz do Diego)", "inicio_origem": tapa_ini,
                                "fim_origem": tapa_fim, "trechos_vozeados": tv})
            k = grupo_tapa.index(L)
            if k == 0:
                ini_o = tapa_ini
            else:
                ini_o, pausa = fronteira(tv, L["ref_rev6"][0])
                medidas.append({"fala": f"fronteira antes de {L['texto']!r}", "inicio_origem": ini_o,
                                "pausa_antes_s": pausa, "ref_rev6_origem": L["ref_rev6"][0]})
            fim_o = tapa_fim if k == len(grupo_tapa) - 1 else None
            item["origem"] = [ini_o, fim_o]
            item["ref_rev6_origem"] = L["ref_rev6"]
        else:
            tv1 = trechos_vozeados(mono, *L["janela_origem"])
            ini_o, fim_o = tv1[0][0], tv1[-1][1]
            item["origem"] = [ini_o, fim_o]
            item["ref_rev6_origem"] = L["ref_rev6"]
            medidas.append({"fala": L["texto"], "inicio_origem": ini_o, "fim_origem": fim_o, "trechos_vozeados": tv1})
        leg.append(item)
    # fala → linha do tempo da REV7; quadro de entrada = primeiro quadro que começa depois do início da fala
    for i, L in enumerate(leg):
        ini = origem_para_rev7(L["origem"][0])
        L["fala_rev7"] = [round(ini, 3), round(origem_para_rev7(L["origem"][1] - 1e-6), 3) if L["origem"][1] else None]
        L["q0"] = q(ini)
    # saída: até a próxima legenda, a menos que exista um corte antes; nesse caso, no corte
    for i, L in enumerate(leg):
        prox = leg[i + 1]["q0"] if i + 1 < len(leg) else N
        corte = min(q(c) for c in cortes if q(c) > L["q0"])
        L["q1"] = min(prox, corte)
        L["de"], L["ate"] = round(L["q0"] / FPS, 3), round(L["q1"] / FPS, 3)
    return leg, medidas


# ---------------------------------------------------------------- 2. gráficos

def fonte(nome, px, pasta):
    return ImageFont.truetype(os.path.join(pasta, nome), px)


def cap_height(f):
    l, t, r, b = f.getbbox("H", anchor="ls")
    return -t


def desenhar_placa(pasta):
    """Placa amarela 1 linha 'PRIMEIRO DIA' + seta desenhada (DS 5.5 / 6.2), 4x e reduzida."""
    P = CFG["placa"]
    f = fonte(P["fonte"], P["tamanho"] * SS, pasta)
    trk = CFG["tokens"]["tracking_display"] * P["tamanho"] * SS
    # texto com tracking, numa tela larga, para medir a tinta
    larg = int(f.getlength(P["texto"]) + trk * len(P["texto"]) + 200 * SS)
    alt = P["altura"] * SS
    camada = Image.new("L", (larg, alt), 0)
    d = ImageDraw.Draw(camada)
    capH = cap_height(f)
    base_y = alt / 2 + capH / 2
    x = 100 * SS
    for ch in P["texto"]:
        d.text((x, base_y), ch, font=f, fill=255, anchor="ls")
        x += f.getlength(ch) + trk
    l, _, r, _ = camada.getbbox()
    tinta = camada.crop((l, 0, r, alt))
    pad = P["padding_h"] * SS
    sh, sl = P["seta_altura"] * SS, P["seta_largura_total"] * SS
    ponta = P["seta_ponta_comprimento"] * sh
    haste = P["seta_haste"] * sh
    gap = P["seta_distancia"] * SS
    largura = pad + tinta.width + gap + sl + pad
    img = Image.new("RGBA", (int(round(largura)), alt), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, alt - 1], radius=CFG["tokens"]["raio"] * SS, fill=AMARELO + (255,))
    img.paste(Image.new("RGBA", tinta.size, GRAFITE + (255,)), (pad, 0), tinta)
    # seta: centro vertical = centro da altura de caixa-alta do texto (= centro da placa)
    cy = alt / 2
    x0 = pad + tinta.width + gap
    xp = x0 + sl - ponta  # início da ponta triangular
    d.rectangle([x0, cy - haste / 2, xp + 2 * SS, cy + haste / 2], fill=GRAFITE + (255,))
    d.polygon([(xp, cy - sh / 2), (x0 + sl, cy), (xp, cy + sh / 2)], fill=GRAFITE + (255,))
    final = img.resize((round(img.width / SS), P["altura"]), Image.BOX)
    medidas = {"largura": final.width, "altura": final.height, "texto_tinta_px": round(tinta.width / SS, 1),
               "seta_altura_px": P["seta_altura"], "seta_largura_px": P["seta_largura_total"],
               "haste_px": round(haste / SS, 2), "ponta_comprimento_px": round(ponta / SS, 1)}
    return final, medidas


def segmentos(linha):
    """'sou *soteropolitano*' → [('sou ', False), ('soteropolitano', True)]"""
    partes = re.split(r"(\*[^*]+\*)", linha)
    return [(p.strip("*"), p.startswith("*")) for p in partes if p]


def desenhar_faixa(texto, fonte_nome, px, pasta, mini_pad=0):
    """Faixa grafite de legenda (DS 6.3.5): raio 8, padding 12/24, Barlow SemiBold, papel, centralizada.
    Palavra entre * vira mini-placa (fundo amarelo, texto grafite, raio 8, padding horizontal 8)."""
    L = CFG["legenda"]
    f = fonte(fonte_nome, px * SS, pasta)
    lh = px * L["entrelinha"] * SS
    pv, ph = L["padding_v"] * SS, L["padding_h"] * SS
    mp = mini_pad * SS
    linhas = texto.split("\n")
    larguras = []
    for ln in linhas:
        w = 0
        for s, hl in segmentos(ln):
            w += f.getlength(s) + (2 * mp if hl else 0)
        larguras.append(w)
    bw = max(larguras) + 2 * ph
    bh = len(linhas) * lh + 2 * pv
    img = Image.new("RGBA", (int(np.ceil(bw)), int(np.ceil(bh))), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=CFG["tokens"]["raio"] * SS,
                        fill=GRAFITE + (255,))
    capH = cap_height(f)
    caixas = []
    for i, ln in enumerate(linhas):
        topo = pv + i * lh
        base_y = topo + lh / 2 + capH / 2
        x = (img.width - larguras[i]) / 2
        for s, hl in segmentos(ln):
            if hl:
                caixa = [x, topo, x + f.getlength(s) + 2 * mp, topo + lh]
                d.rounded_rectangle(caixa, radius=CFG["tokens"]["raio"] * SS, fill=AMARELO + (255,))
                caixas.append([c / SS for c in caixa])
                d.text((x + mp, base_y), s, font=f, fill=GRAFITE + (255,), anchor="ls")
                x += f.getlength(s) + 2 * mp
            else:
                d.text((x, base_y), s, font=f, fill=PAPEL + (255,), anchor="ls")
                x += f.getlength(s)
    final = img.resize((round(img.width / SS), round(img.height / SS)), Image.BOX)
    return final, caixas


def ease_enter(t, p=(0.2, 0.8, 0.2, 1.0)):
    """cubic-bezier(0.2, 0.8, 0.2, 1) do token easing.enter: y para um x = t."""
    x1, y1, x2, y2 = p
    bx = lambda s: 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s ** 2 * x2 + s ** 3  # noqa: E731
    by = lambda s: 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s ** 2 * y2 + s ** 3  # noqa: E731
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if bx(mid) < t else (lo, mid)
    return by((lo + hi) / 2)


def graficos(leg, pasta):
    """Gera _tmp/overlay/q_00000.png … (1 por quadro; estados iguais compartilham o arquivo via hard link)."""
    out = os.path.join(TMP, "overlay")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    P = CFG["placa"]
    L = CFG["legenda"]
    F = CFG["fechamento"]
    placa, placa_med = desenhar_placa(pasta)
    cx = (SAFE["x0"] + SAFE["x1"]) / 2  # centro da coluna de conteúdo (508)
    faixas = []
    for item in leg:
        img, caixas = desenhar_faixa(item["texto"], L["fonte"], L["tamanho"], pasta, L["mini_placa_padding_h"])
        x = int(round(cx - img.width / 2))
        faixas.append({"img": img, "x": x, "y": L["topo"], "q0": item["q0"], "q1": item["q1"],
                       "mini": [[x + c[0], L["topo"] + c[1], x + c[2], L["topo"] + c[3]] for c in caixas]})
    fech, _ = desenhar_faixa(F["texto"], F["fonte"], F["tamanho"], pasta)
    fech_x = int(round(cx - fech.width / 2))
    fq0, fq1 = q(F["de"]), q(F["ate"])
    q_saida = q(P["saida_s"])
    nq = P["entrada_quadros"]
    # posições da entrada: quadro f mostra o estado em t = (f+1)/nq (quadro 0 já com a placa entrando)
    x_ini = P["x"] - placa.width
    pos_placa = {f: round(x_ini + (P["x"] - x_ini) * ease_enter((f + 1) / nq)) for f in range(nq)}
    estados, cache, elementos = {}, {}, []
    for k in range(N):
        chave, camadas = [], []
        if k < q_saida:
            px = pos_placa.get(k, P["x"])
            chave.append(("placa", px))
            camadas.append(("placa", placa, px, P["y"]))
        for i, fx in enumerate(faixas):
            if fx["q0"] <= k < fx["q1"]:
                chave.append(("leg", i))
                camadas.append((f"legenda {i + 1}", fx["img"], fx["x"], fx["y"]))
        if fq0 <= k < fq1:
            chave.append(("fech",))
            camadas.append(("fechamento", fech, fech_x, L["topo"]))
        chave = tuple(chave)
        destino = os.path.join(out, f"q_{k:05d}.png")
        if chave in cache:
            os.link(cache[chave], destino)
        else:
            quadro = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for _, img, x, y in camadas:
                quadro.alpha_composite(img, (max(x, 0), y), (max(0, -x), 0))
            # máscara da entrada: nada à esquerda da safe zone (x < 72)
            a = np.array(quadro)
            a[:, :SAFE["x0"], :] = 0
            Image.fromarray(a).save(destino, compress_level=1)
            cache[chave] = destino
        estados[k] = [c[0] for c in camadas]
        elementos.append([(nome, max(x, SAFE["x0"]), y, x + img.width, y + img.height) for nome, img, x, y in camadas])
    info = {"placa": {**placa_med, "x": P["x"], "y": P["y"], "x_final": P["x"] + placa.width,
                      "y_final": P["y"] + placa.height, "entrada_x_por_quadro": pos_placa, "sai_no_quadro": q_saida},
            "legendas": [{"texto": leg[i]["texto"], "rect": [fx["x"], fx["y"], fx["x"] + fx["img"].width,
                                                             fx["y"] + fx["img"].height], "mini_placas": fx["mini"]}
                         for i, fx in enumerate(faixas)],
            "fechamento": {"texto": F["texto"], "rect": [fech_x, L["topo"], fech_x + fech.width,
                                                          L["topo"] + fech.height], "quadros": [fq0, fq1]},
            "estados_unicos": len(cache)}
    return out, info, elementos


# ---------------------------------------------------------------- 3. áudio

def montar_audio():
    A = CFG["audio"]
    src = audio_base()
    h = int(round(A["crossfade_s"] * SR / 2))  # 50 ms de cada lado da emenda
    total = N * SPF
    mix = np.zeros((total, 2), np.float64)
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
    assert emendas == [round(x, 3) for x in A["emendas_novas_s"]], f"emendas {emendas} ≠ aprovadas"
    dc = int(A["declique_ms"] * SR / 1000)
    rampa = np.linspace(0, 1, dc, endpoint=False)
    mix[:dc] *= rampa[:, None]
    mix[-dc:] *= rampa[::-1][:, None]
    mix *= 10 ** (A["ganho_db"] / 20)
    wav = os.path.join(TMP, "audio_rev7.f32")
    mix.astype(np.float32).tofile(wav)
    return wav, mix, src, emendas


# ---------------------------------------------------------------- 4. vídeo

def montar_video(overlay, wav):
    pl = blocos()
    entradas, filtros, rotulos = [], [], []
    for i, b in enumerate(pl):
        entradas += ["-i", BASE]
        filtros.append(f"[{i}:v]trim=start_frame={b['o0']}:end_frame={b['o1']},setpts=PTS-STARTPTS[v{i}]")
        rotulos.append(f"[v{i}]")
    n = len(pl)
    filtros.append(f"{''.join(rotulos)}concat=n={n}:v=1:a=0,setpts=N/({FPS}*TB),format=yuv444p[b]")
    filtros.append(f"[{n}:v]format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva444p[t]")
    filtros.append("[b][t]overlay=0:0:format=yuv444:eof_action=pass,format=yuv420p[v]")
    rodar(["ffmpeg", "-v", "error", "-y", *entradas,
           "-framerate", FPS, "-i", os.path.join(overlay, "q_%05d.png"),
           "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
           "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", f"{n + 1}:a", "-frames:v", N,
           "-c:v", "libx264", "-crf", 16, "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
           "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
           "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", SAIDA])


# ---------------------------------------------------------------- 5. QA

def ffprobe(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json",
                        arq], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af",
                        "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1))
    return i, tp


def quadros_cinza(arq, n_max):
    """Decodifica o vídeo inteiro em 270x480, cinza (para mapeamento de quadros e tela preta)."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", "scale=270:480:flags=area", "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.uint8).reshape(-1, 480, 270)
    return a[:n_max].astype(np.float32)


def psnr(a, b):
    mse = ((a - b) ** 2).mean()
    return 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def qa(leg, medidas, info, elementos, mix, src, emendas, overlay):
    R = {"arquivo": os.path.relpath(SAIDA, os.path.dirname(REV7))}
    pr = ffprobe(SAIDA)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    R["formato"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "duracao_video_s": float(v["duration"]),
                    "duracao_audio_s": float(a["duration"]), "duracao_container_s": float(pr["format"]["duration"]),
                    "codec_video": f"{v['codec_name']} ({v.get('profile')})", "pix_fmt": v["pix_fmt"],
                    "cor": f"{v.get('color_primaries')}/{v.get('color_transfer')}/{v.get('color_space')}/{v.get('color_range')}",
                    "codec_audio": f"{a['codec_name']} ({a.get('profile')})", "sr_audio": int(a["sample_rate"]),
                    "canais": a["channels"], "tamanho_bytes": int(pr["format"]["size"]),
                    "tags": pr["format"].get("tags", {})}
    lufs, tp = ebur128(SAIDA)
    R["audio"] = {"lufs_integrado": lufs, "pico_verdadeiro_dbtp": tp}
    lufs_b, tp_b = ebur128(BASE)
    R["audio"]["base_rev6"] = {"lufs_integrado": lufs_b, "pico_verdadeiro_dbtp": tp_b}

    # áudio decodificado do MP4: degraus e estalos nas emendas novas
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", SAIDA, "-map", "0:a", "-f", "f32le", "-ac", "2", "-ar", str(SR),
                        "-"], capture_output=True, check=True)
    fin = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).mean(1)
    smix = mix.mean(1)

    def rms_db(x):
        return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)

    def maior_salto(x):
        """maior diferença entre amostras vizinhas, relativa ao p99,9 do entorno (≥ 4 = estalo)"""
        d = np.abs(np.diff(x))
        return float(d.max() / (np.percentile(d, 99.9) + 1e-12))

    em = []
    for t in emendas:
        i = int(round(t * SR))
        w = int(0.1 * SR)
        em.append({"t": t, "rms_antes_db": round(rms_db(fin[i - w:i - int(0.05 * SR)]), 1),
                   "rms_depois_db": round(rms_db(fin[i + int(0.05 * SR):i + w]), 1),
                   "salto_max_rel": round(maior_salto(smix[i - 4800:i + 4800]), 2)})
        em[-1]["degrau_db"] = round(em[-1]["rms_depois_db"] - em[-1]["rms_antes_db"], 1)
    R["audio"]["emendas"] = em
    R["audio"]["inicio_fim"] = {"primeira_amostra": float(smix[0]), "ultima_amostra": float(smix[-1]),
                                "salto_max_rel_inicio": round(maior_salto(smix[:4800]), 2),
                                "salto_max_rel_fim": round(maior_salto(smix[-4800:]), 2)}
    # narração intacta: amostras da REV7 = amostras da base em toda a fala de apresentação
    srt = ler_srt(os.path.normpath(os.path.join(REV7, CFG["srt_narracao"])))
    o0, o1 = srt[1][0], srt[12][1]
    r0 = origem_para_rev7(o0)
    i0, i1 = int(round(r0 * SR)), int(round((r0 + (o1 - o0)) * SR))
    j0 = int(round(o0 * SR))
    dif = np.abs(mix[i0:i1] - src[j0:j0 + (i1 - i0)].astype(np.float64))
    identico_ate = i0 + (np.nonzero(dif.max(1) > 0)[0][0] if (dif > 0).any() else i1 - i0)
    R["audio"]["narracao"] = {"origem_s": [o0, o1], "rev7_s": [round(r0, 3), round(i1 / SR, 3)],
                              "amostras_identicas_ate_s": round(identico_ate / SR, 4),
                              "diferenca_max": float(dif.max())}
    # cada bloco, fora das janelas de crossfade (50 ms) e da rampa de 30 ms, é a mixagem da base amostra por amostra
    h = int(round(CFG["audio"]["crossfade_s"] * SR / 2))
    dc = int(CFG["audio"]["declique_ms"] * SR / 1000)
    bl_r = []
    for i, b in enumerate(blocos()):
        r0, r1 = b["r0"] * SPF + (h if i else dc), b["r1"] * SPF - (h if i < len(blocos()) - 1 else dc)
        o0 = b["o0"] * SPF + (r0 - b["r0"] * SPF)
        d = np.abs(mix[r0:r1] - src[o0:o0 + (r1 - r0)].astype(np.float64)).max()
        bl_r.append({"planos": b["planos"], "rev7_s": [round(r0 / SR, 3), round(r1 / SR, 3)],
                     "diferenca_max": float(d)})
    R["audio"]["blocos_identicos_a_base"] = bl_r
    # falas de som direto, pelos tempos medidos na onda
    falas = []
    for nome, (t0o, t1o) in {"Buenos días, Barcelona!": leg[0]["origem"], "Chegamos!": leg[10]["origem"],
                             "E agora … tapa de Barcelona.": [leg[11]["origem"][0], leg[13]["origem"][1]]}.items():
        falas.append({"fala": nome, "origem_s": [t0o, t1o],
                      "rev7_s": [round(origem_para_rev7(t0o), 3), round(origem_para_rev7(t1o - 1e-6), 3)]})
    R["audio"]["falas_som_direto"] = falas

    # mapeamento de quadros: cada quadro da REV7 = quadro de origem aprovado (região sem gráficos, y < 1096)
    out = quadros_cinza(SAIDA, N)
    base = quadros_cinza(BASE, 10 ** 6)
    yl = int(1096 / 4)
    mapa = []
    for p in planos():
        for k in range(p["r0"], p["r1"]):
            mapa.append(p["o0"] + k - p["r0"])
    acertos, piores, ps_list = 0, [], []
    for k in range(N):
        m = mapa[k]
        cand = {d: psnr(out[k, :yl], base[m + d, :yl]) for d in (-1, 0, 1) if 0 <= m + d < len(base)}
        melhor = max(cand, key=cand.get)
        ps_list.append(cand[0])
        if melhor == 0:
            acertos += 1
        else:
            piores.append({"quadro": k, "psnr_exato": round(cand[0], 1), "melhor_desvio": melhor})
    estaticos = [k for k in range(1, N) if np.abs(base[mapa[k], :yl] - base[mapa[k] - 1, :yl]).mean() < 0.05]
    R["video"] = {"mapeamento_quadros_corretos": acertos, "de": N, "psnr_min_db": round(min(ps_list), 1),
                  "psnr_mediana_db": round(float(np.median(ps_list)), 1), "divergencias": piores[:10],
                  "quadros_estaticos_na_origem": len(estaticos)}
    luma = out.mean(axis=(1, 2))
    R["video"]["luma_media_min"] = round(float(luma.min()), 1)
    R["video"]["quadros_pretos"] = int((luma < 16).sum())
    lum_b = np.array([base[m].mean() for m in mapa])
    R["video"]["diferenca_luma_max_vs_origem"] = round(float(np.abs(out[:, :yl].mean(axis=(1, 2)) -
                                                              base[mapa][:, :yl].mean(axis=(1, 2))).max()), 2)
    R["video"]["luma_inicio_fim"] = [round(float(luma[0]), 1), round(float(luma[-1]), 1),
                                     round(float(lum_b[0]), 1), round(float(lum_b[-1]), 1)]

    # gráficos: safe zone, sobreposição placa × legenda, cores, alfa (sem fade)
    fora, sobrepos, alfa_parcial, cores_fora = [], [], [], set()
    paleta = np.array([AMARELO, GRAFITE, PAPEL], np.float32)
    vistos = set()
    for k in range(N):
        for nome, x0, y0, x1, y1 in elementos[k]:
            if x0 < SAFE["x0"] or x1 > SAFE["x1"] or y0 < SAFE["y0"] or y1 > SAFE["y1"]:
                fora.append((k, nome, x0, y0, x1, y1))
        rects = {n: (x0, y0, x1, y1) for n, x0, y0, x1, y1 in elementos[k]}
        if "placa" in rects:
            for n2, r2 in rects.items():
                if n2 != "placa":
                    p = rects["placa"]
                    if not (r2[1] >= p[3] or r2[3] <= p[1] or r2[0] >= p[2] or r2[2] <= p[0]):
                        sobrepos.append((k, n2))
        arq = os.path.realpath(os.path.join(overlay, f"q_{k:05d}.png"))
        ino = os.stat(os.path.join(overlay, f"q_{k:05d}.png")).st_ino
        if ino in vistos:
            continue
        vistos.add(ino)
        im = np.array(Image.open(arq))
        al = im[..., 3]
        ys, xs = np.nonzero(al)
        if len(xs):
            if xs.min() < SAFE["x0"] or xs.max() >= SAFE["x1"] or ys.min() < SAFE["y0"] or ys.max() >= SAFE["y1"]:
                fora.append((k, "pixels", int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
            opacos = im[al == 255][:, :3].astype(np.float32)
            # pixel opaco = cor da marca ou mistura de antialias entre duas delas (distância ao segmento ≤ 2)
            dmin = np.full(len(opacos), np.inf, np.float32)
            for i in range(3):
                for j in range(i + 1, 3):
                    a_, b_ = paleta[i], paleta[j]
                    u = np.clip(((opacos - a_) @ (b_ - a_)) / ((b_ - a_) @ (b_ - a_)), 0, 1)
                    dmin = np.minimum(dmin, np.linalg.norm(opacos - (a_ + u[:, None] * (b_ - a_)), axis=1))
            if (dmin > 2).any():
                cores_fora.add((k, int((dmin > 2).sum())))
        meio = ((al > 0) & (al < 255)).sum()
        cheio = (al == 255).sum()
        alfa_parcial.append(meio / max(cheio, 1))
    R["graficos"] = {**info, "fora_da_safe_zone": fora[:10], "n_fora_da_safe_zone": len(fora),
                     "placa_sobreposta": sobrepos[:10], "n_placa_sobreposta": len(sobrepos),
                     "estados_com_cor_fora_da_paleta": sorted(cores_fora),
                     "alfa_parcial_max_rel": round(max(alfa_parcial), 4)}
    pl = info["placa"]
    R["graficos"]["distancia_placa_legenda_px"] = min(
        l["rect"][1] - pl["y_final"] for l in info["legendas"])

    # textos
    textos = [L["texto"].replace("*", "") for L in leg]
    minis = [s for L in leg for s, hl in segmentos(L["texto"].replace("\n", " ")) if hl]
    linhas = [ln for L in leg for ln in L["texto"].replace("*", "").split("\n")]
    R["textos"] = {"iguais_aos_aprovados": textos == TEXTOS_APROVADOS,
                   "mini_placas": minis, "mini_placas_ok": minis == MINI_PLACAS_APROVADAS,
                   "max_caracteres_linha": max(len(x) for x in linhas),
                   "max_linhas": max(len(L["texto"].split("\n")) for L in leg),
                   "placa": CFG["placa"]["texto"] + " →", "fechamento": CFG["fechamento"]["texto"],
                   "sem_PRIMEIRO_DIA_EM": "EM" not in CFG["placa"]["texto"].split(),
                   "sem_simbolo_1o": "1º" not in CFG["fechamento"]["texto"]}
    R["legendas"] = [{k: L[k] for k in ("texto", "fonte_tempo", "origem", "fala_rev7", "de", "ate", "q0", "q1")}
                     | ({"ref_rev6_origem": L["ref_rev6_origem"]} if "ref_rev6_origem" in L else {})
                     for L in leg]
    R["medidas_onda"] = medidas
    R["planos"] = [{k: p[k] for k in ("n", "origem", "cena", "o0", "o1", "r0", "r1")} | {
        "rev7_s": [round(p["r0"] / FPS, 3), round(p["r1"] / FPS, 3)]} for p in planos()]
    R["blocos_audio"] = [{"planos": b["planos"], "origem_s": [b["o0"] / FPS, b["o1"] / FPS],
                          "rev7_s": [round(b["r0"] / FPS, 3), round(b["r1"] / FPS, 3)]} for b in blocos()]
    return R


def frames_qa(info):
    shutil.rmtree(QA_DIR, ignore_errors=True)
    os.makedirs(QA_DIR)
    alvos = [(f"t{t:05.2f}s".replace(".", "_"), q(t) if q(t) < N else N - 1, t) for t in CFG["qa_tempos_s"]]
    alvos += [(f"q{k:03d}", k, k / FPS) for k in CFG["qa_quadros"]]
    vistos, lista = set(), []
    for nome, k, t in alvos:
        arq = os.path.join(QA_DIR, f"rev7_{nome}_quadro{k:03d}.jpg")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1,
               "-q:v", 2, arq])
        lista.append((nome, k, t, arq))
    # rosto × placa no plano 1: 1 a cada 4 quadros, faixa y 860–1220 (placa começa em y 1104)
    rodar(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
           f"select='lt(n\\,{q(CFG['placa']['saida_s'])})*not(mod(n\\,4))',crop={W}:360:0:860,scale=540:180,tile=3x5",
           "-frames:v", 1, "-q:v", 2, os.path.join(QA_DIR, "rosto_x_placa_plano1_y860-1220.jpg")])
    # folha de contato com safe zone (vermelho) e retângulos dos elementos (só na folha, não no vídeo)
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    linhas = (len(lista) + cols - 1) // cols
    folha = Image.new("RGB", (cols * cw, linhas * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (nome, k, t, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        dd = ImageDraw.Draw(im)
        dd.rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc], outline=(255, 0, 0))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"{nome}  quadro {k}  {k / FPS:.3f} s", fill=(0, 0, 0))
    folha.save(os.path.join(QA_DIR, "folha_qa_rev7.jpg"), quality=90)
    return [(n, k, os.path.relpath(a, REV7)) for n, k, t, a in lista]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True, help="pasta com Barlow-SemiBold.ttf e BarlowCondensed-ExtraBold.ttf")
    args = ap.parse_args()
    os.makedirs(TMP, exist_ok=True)
    print("1/5 tempos das legendas")
    leg, medidas = tempos_legendas()
    for L in leg:
        print(f"   {L['de']:7.3f}–{L['ate']:7.3f}  {L['texto']!r}")
    print("2/5 gráficos")
    overlay, info, elementos = graficos(leg, args.fontes)
    print("3/5 áudio")
    wav, mix, src, emendas = montar_audio()
    print("4/5 vídeo")
    montar_video(overlay, wav)
    print("5/5 QA")
    R = qa(leg, medidas, info, elementos, mix, src, emendas, overlay)
    R["frames_qa"] = frames_qa(info)
    R["sha256"] = hashlib.sha256(open(SAIDA, "rb").read()).hexdigest()
    R["fontes"] = {n: hashlib.sha256(open(os.path.join(args.fontes, n), "rb").read()).hexdigest()
                   for n in ("Barlow-SemiBold.ttf", "BarlowCondensed-ExtraBold.ttf")}
    json.dump(R, open(os.path.join(REV7, "relatorio_tecnico_rev7.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: R[k] for k in ("formato", "audio")}, ensure_ascii=False, indent=1, default=str))
    print(SAIDA)


if __name__ == "__main__":
    sys.exit(main())
