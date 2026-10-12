"""Reel 'POV: 15 segundos no Atomium' (REV2): reel_atomium_pov_rev2.mp4 (1080 × 1920, 24 qps, SDR BT.709).

REV2 (pedido do Diego, 12/10/2026): 3 planos de ≈ 5 s, sem cortes curtos, para dar imersão. Mesmo motor do Reel do
Atomium (reels/atomium/rev2/scripts/atomium.py), sem ticket e sem fala: só som ambiente, nivelado plano a plano antes do master, e o título do POV em legenda Padrão do quadro 0 até o fim.

Monta os planos do rev2.json a partir dos originais do Drive (recorte 9:16, tone mapping HLG → BT.709) com a camada
do DS V2 Nível B: placa de abertura com Chegada no quadro 0 (sai pela direita em 2,4 s), legenda Padrão
fixa com o título do POV, scrim sempre ligado e grão 5%. 2 cortes secos.
Áudio: o som ambiente de cada plano, nivelado por RMS, fade de 40 ms em cada corte, master −14 LUFS e pico
verdadeiro ≤ −1 dBTP (limitador com sobreamostragem 4×, AAC 256 kbps).

Uso (de dentro de reels/atomium-pov/):
  PD_BRUXELAS=PASTA_COM_OS_MOV python3 rev2/scripts/pov.py --fontes PASTA_TTF [--qa]
Fontes (SIL OFL, Google Fonts): Barlow-Bold, Barlow-Medium, BarlowCondensed-SemiBold/-Bold/-ExtraBold,
IBMPlexMono-Medium, ReenieBeanie.
"""
import argparse
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(REV, "..", "..", ".."))
CFG = json.load(open(os.path.join(REV, "rev2.json"), encoding="utf-8"))
FPS, W, H = CFG["fps"], CFG["largura"], CFG["altura"]

ap = argparse.ArgumentParser()
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--qa", action="store_true", help="salva quadros de QA em rev2/qa_frames")
A = ap.parse_args()

sys.path.insert(0, os.path.join(RAIZ, "youtube", "barcelona", "rev2", "scripts"))
sys.argv = sys.argv[:1]
import rev2 as yt  # noqa: E402  (placa, desenho, curvas e cores do DS V2)
sys.path.insert(0, os.path.join(RAIZ, "reels", "apresentacao", "rev8", "scripts"))
import rev8 as rl  # noqa: E402  (legenda Padrão, scrim e grão do Reel)

yt.ARGS_FONTES = A.fontes
yt.K = 1                       # grade do DS = pixels do Reel (1080 de largura)
yt.W, yt.H = W, H
yt.placa_pos = lambda it, info: tuple(CFG["placa_xy"])
FONTE_DIR = os.environ[CFG["fonte_env"]]
TMP = os.path.join(REV, "_tmp")
os.makedirs(TMP, exist_ok=True)


def q(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------- linha do tempo

def linha_do_tempo():
    planos, k = [], 0
    for p in CFG["planos"]:
        p = dict(p)
        n = q(p["dur"])
        if p.get("video_continua"):
            src, v0 = planos[-1]["video"]
            p["video"] = [src, v0 + planos[-1]["n"] / FPS]
        if p.get("audio_continua"):
            src, a0 = planos[-1]["audio"]
            p["audio"] = [src, a0 + planos[-1]["n"] / FPS]
        elif "audio" not in p:
            p["audio"] = list(p["video"])
        planos.append({**p, "k0": k, "k1": k + n, "n": n})
        k += n
    return planos, k


PLANOS, N = linha_do_tempo()


def k_de(p, t_audio):
    return p["k0"] + q(t_audio - p["audio"][1])


def legendas():
    """um grupo fica até o próximo começar; quando o áudio continua no plano seguinte, o grupo atravessa o corte."""
    todos = [(i, p, g) for i, p in enumerate(PLANOS) for g in p["legendas"]]
    out = []
    for n, (i, p, g) in enumerate(todos):
        if "inicio" in g:                                 # REV2: grupo inteiro, no início medido da voz (DS 3.3, freio 4)
            g = {**g, "palavras": [g["inicio"]] * len(g["texto"].split()), "modo": "grupo"}
            todos[n] = (i, p, g)
        ks = [min(max(k_de(p, t), p["k0"]), p["k1"] - 1) for t in g["palavras"]]
        k0 = ks[0]
        fim, j = p["k1"], i
        while j + 1 < len(PLANOS) and PLANOS[j + 1].get("audio_continua"):
            j += 1
            fim = PLANOS[j]["k1"]
        k1 = fim
        if n + 1 < len(todos):
            i2, p2, g2 = todos[n + 1]
            if i2 <= j:
                ini2 = g2["inicio"] if "inicio" in g2 else g2["palavras"][0]
                k1 = min(k_de(p2, ini2), fim)
        nwords = len(g["texto"].split())
        assert nwords == len(ks), g["texto"]
        fala = max((g["palavras"][-1] - g["palavras"][0]) + 0.35, 0.3)
        vel = nwords / fala
        it = {"texto": g["texto"], "texto_tela": g["texto"], "q0": k0, "q1": k1,
              "modo": g.get("modo", "palavra" if vel <= 3.0 else "grupo"), "palavras_q": [k0] + ks[1:], "plano": p["id"]}
        linhas = g["texto"].replace("*", "").split("\n")
        assert len(linhas) <= 2 and max(len(x) for x in linhas) <= 26 and nwords <= 6, g["texto"]
        assert len(linhas) == 1 or len(linhas[0]) <= len(linhas[1]), g["texto"]      # DS 3.1: linha de cima ≤ de baixo
        out.append(rl.Legenda(it, A.fontes))
    tf = CFG.get("texto_fixo")
    if tf:
        linhas = tf["texto"].split("\n")
        assert len(linhas) <= 2 and max(len(x) for x in linhas) <= 26 and len(tf["texto"].split()) <= 6
        assert len(linhas) == 1 or len(linhas[0]) <= len(linhas[1])
        it = {"texto": tf["texto"], "texto_tela": tf["texto"], "q0": tf["de_quadro"], "q1": N, "modo": "grupo",
              "palavras_q": [tf["de_quadro"]] * len(tf["texto"].split()), "plano": "fixo"}
        out.append(rl.Legenda(it, A.fontes))
    return out


# ---------------------------------------------------------------- objetos

def placas():
    out = []
    for pl in CFG["placas"]:
        p = next(x for x in PLANOS if x["id"] == pl["plano"])
        k0 = p["k0"] + q(pl.get("entra_s", 0.0))
        n = (q(pl["sai_s"]) - (k0 - p["k0"])) if "sai_s" in pl else p["k1"] - k0
        it = {"variante": pl["variante"], "linha1": pl["linha1"], "linha2": pl["linha2"], "q_in": 0,
              "q_fim": n if pl["saida"] else n + 12}
        face, modulo, info = yt.placa_pecas(it)
        assert info["w_design"] <= 872, (pl["id"], info["w_design"])       # DS 2.1: largura máxima 872
        quadros = list(yt.quadros_placa(it))[:n]
        x0, y0 = CFG["placa_xy"]
        out.append({"id": pl["id"], "k0": k0, "quadros": quadros, "x": x0 - yt.PLACA_PAD, "y": y0 - yt.PLACA_PAD,
                    "caixa": [x0, y0, x0 + info["w_design"], y0 + info["h_design"]]})
    return out


# ---------------------------------------------------------------- vídeo de base

TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709,format=gbrpf32le")


def ler_plano(p):
    src, v0 = p["video"]
    arq = os.path.join(FONTE_DIR, src)
    if p["cx"] is None:                            # vertical: o arquivo é 3840 × 2160 com rotação −90 nos metadados, que este
        vf = f"transpose=clock,scale={W}:{H}:flags=lanczos,{TM}"   # ffmpeg não aplica sozinho; gira 90° no sentido horário
        p["recorte_x"] = None
    else:
        cw = 1216
        if isinstance(p["cx"], list):              # recorte que acompanha a cena: [[t no plano, cx], …]
            ks = [(t, min(max(c * 3840 - cw / 2, 0), 3840 - cw)) for t, c in p["cx"]]
            if p.get("video_continua"):            # mesma tomada do plano anterior: o tempo segue
                desl = v0 - PLANOS[PLANOS.index(p) - 1]["video"][1]
                ks = [(t - desl, x) for t, x in ks]
            expr = f"{ks[-1][1]:.1f}"
            for (t0, x0), (t1, x1) in reversed(list(zip(ks, ks[1:]))):
                expr = f"if(lt(t,{t1:.3f}),{x0:.1f}+({x1 - x0:.1f})*max(t-{t0:.3f},0)/{t1 - t0:.3f},{expr})"
            x = f"'{expr}'"
            p["recorte_x"] = [round(v[1]) for v in ks]
        else:
            x = min(max(int(round(p["cx"] * 3840 - cw / 2)) // 2 * 2, 0), 3840 - cw)
            p["recorte_x"] = x
        vf = f"crop={cw}:2160:{x}:0,scale={W}:{H}:flags=lanczos,{TM}"
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{v0:.4f}", "-i", arq, "-frames:v", str(p["n"]), "-an",
           "-vf", vf, "-f", "rawvideo", "-pix_fmt", "gbrpf32le", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
    tam = W * H * 4 * 3
    for _ in range(p["n"]):
        b = pr.stdout.read(tam)
        assert len(b) == tam, (p["id"], "quadros a menos")
        g, bl, r = np.frombuffer(b, np.float32).reshape(3, H, W)
        yield np.clip(np.dstack([r, g, bl]), 0, 1)
    pr.stdout.close()
    pr.wait()


# ---------------------------------------------------------------- áudio

def montar_audio():
    sr = 48000
    pedacos = []
    for i, p in enumerate(PLANOS):
        src, a0 = p["audio"]
        dur = p["n"] / FPS
        f = os.path.join(TMP, f"a_{p['id']}.f32")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.4f}", "-t", f"{dur:.4f}", "-i", os.path.join(FONTE_DIR, src),
                        "-vn", "-ac", "2", "-ar", str(sr), "-f", "f32le", f], check=True)
        x = np.fromfile(f, np.float32).reshape(-1, 2)
        n = int(round(dur * sr))
        x = np.pad(x, ((0, max(n - len(x), 0)), (0, 0)))[:n]
        nf = int(CFG["fade_corte_ms"] * sr / 1000)
        rampa = np.linspace(0, 1, nf, dtype=np.float32)[:, None]
        if not p.get("audio_continua"):
            x[:nf] *= rampa
        if not (i + 1 < len(PLANOS) and PLANOS[i + 1].get("audio_continua")):
            x[-nf:] *= rampa[::-1]
        if CFG.get("nivelar_planos"):                     # ambiente: cada plano no mesmo nível RMS antes do master
            x = x / max(float(np.sqrt((x ** 2).mean())), 1e-6) * 0.05
        pedacos.append(x)
    mix = np.concatenate(pedacos)
    bruto = os.path.join(TMP, "audio_bruto.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", bruto],
                   input=mix.tobytes(), check=True)
    medida = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", bruto, "-af", "ebur128=peak=true", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    i = float(medida.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])
    ganho = CFG["lufs_alvo"] - i
    lim = 10 ** (CFG["pico_dbfs"] / 20)
    final = os.path.join(TMP, "audio_final.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af",
                    f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={lim:.4f}:attack=5:release=80:level=0,aresample=48000",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", final], check=True)
    return final, round(i, 1), round(ganho, 2)


# ---------------------------------------------------------------- composição

def main():
    for f in ("Barlow-Bold.ttf", "BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-SemiBold.ttf", "IBMPlexMono-Medium.ttf"):
        assert os.path.exists(os.path.join(A.fontes, f)), f
    LG, PL = legendas(), placas()
    scrim = rl.scrim_alfa()
    video = os.path.join(TMP, "video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-g", "48",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv", video],
                           stdin=subprocess.PIPE)
    registro, qa_dir = {}, os.path.join(REV, "qa_frames")
    os.makedirs(qa_dir, exist_ok=True)
    for p in PLANOS:
        for j, base in enumerate(ler_plano(p)):
            k = p["k0"] + j
            img = rl.overlay_blend(base, rl.grao(k), rl.T["op_grain"])
            img = img * (1 - scrim) + rl.GRAFITE * scrim
            cam = np.zeros((H, W, 4), np.float32)
            els = []
            for pl in PL:
                if pl["k0"] <= k < pl["k0"] + len(pl["quadros"]):
                    yt.sobre(cam, pl["quadros"][k - pl["k0"]], pl["x"], pl["y"])
                    els.append(("placa", pl["id"], pl["caixa"]))
            for lg in LG:
                ws = lg.estado(k, ultimo=(lg.item["q1"] == N))
                if ws is not None:
                    rl.sobre(cam, lg.camada(ws), lg.x0, lg.y0)
                    els.append(("legenda", lg.item["texto"], [round(v, 1) for v in lg.ret]))
            a = cam[..., 3:4]
            img = img * (1 - a) + cam[..., :3]
            enc.stdin.write((np.clip(img, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
            registro[k] = els
            if A.qa and j == min(p["n"] - 1, int(p["n"] * 0.6)):
                Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(qa_dir, f"{k:04d}_{p['id']}.jpg"), quality=88)
        print(p["id"], p["k0"], p["k1"], "recorte x", p["recorte_x"], flush=True)
    enc.stdin.close()
    assert enc.wait() == 0
    audio, lufs_bruto, ganho = montar_audio()
    saida = os.path.join(REV, CFG["saida"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c", "copy",
                    "-map_metadata", "-1", "-movflags", "+faststart", saida], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "28", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", os.path.join(REV, CFG["saida_previa"])], check=True)
    rel = {"quadros": N, "duracao_s": round(N / FPS, 3), "lufs_antes": lufs_bruto, "ganho_db": ganho,
           "planos": [{k: p[k] for k in ("id", "video", "audio", "k0", "k1", "cx", "recorte_x")} for p in PLANOS],
           "elementos_por_quadro": {str(k): v for k, v in registro.items() if k % 12 == 0}}
    json.dump(rel, open(os.path.join(REV, "relatorio_tecnico_rev2.json"), "w"), ensure_ascii=False, indent=1)
    print("ok", saida, N, "quadros", round(N / FPS, 2), "s")


main()
