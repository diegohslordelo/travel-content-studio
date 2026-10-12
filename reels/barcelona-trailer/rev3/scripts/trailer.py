"""Reel trailer do vlog de Barcelona (REV3): reel_barcelona_trailer_rev3.mp4 (1080 × 1920, 24 qps, SDR BT.709).

Monta os planos do rev1.json a partir do original 4K HLG (recorte 9:16, tone mapping para BT.709, o mesmo da QA
da REV2 do YouTube) e aplica, quadro a quadro, a camada do DS V2 com componentes que já existem nos pipelines
aprovados (sem valor visual novo):
  - placa esmaltada com a assinatura Chegada (youtube/barcelona/rev2/scripts/rev2.py, grade 1:1 no Reel),
    abertura `3 DIAS EM / BARCELONA` e CTA `VÍDEO COMPLETO / NO YOUTUBE` (DS 2.7), ambas em x 72 · y 640;
  - etiqueta de valor (DS 2.6, legenda Informação da 3.2) em x 72, acima da legenda, número girando;
  - legenda Padrão do Reel (reels/apresentacao/rev8/scripts/rev8.py), palavra a palavra ou grupo inteiro (3.3);
  - scrim sempre ligado, grão 5% e Snap (flash papel 30% + zoom 104 → 100% em 3 quadros) entre os preços.
Áudio: trechos do áudio do vídeo do YouTube (antes do master), fade de 8 ms em cada corte, master −14 LUFS e
pico verdadeiro ≤ −1 dBTP (limitador com sobreamostragem 4×, AAC 256 kbps).

Uso (de dentro de reels/barcelona-trailer/):
  BCN_ORIGINAL=… BCN_AUDIO=… python3 rev3/scripts/trailer.py --fontes PASTA_TTF [--ate N_PLANOS] [--qa]
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
CFG = json.load(open(os.path.join(REV, "rev3.json"), encoding="utf-8"))
FPS, W, H = CFG["fps"], CFG["largura"], CFG["altura"]

ap = argparse.ArgumentParser()
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--ate", type=int, default=None, help="renderiza só os N primeiros planos (prévia)")
ap.add_argument("--qa", action="store_true", help="salva um quadro por plano em rev1/qa_frames")
A = ap.parse_args()

sys.path.insert(0, os.path.join(RAIZ, "youtube", "barcelona", "rev2", "scripts"))
sys.argv = sys.argv[:1]
import rev2 as yt  # noqa: E402  (placa, etiqueta, curvas e cores do DS V2)
sys.path.insert(0, os.path.join(RAIZ, "reels", "apresentacao", "rev8", "scripts"))
import rev8 as rl  # noqa: E402  (legenda Padrão, scrim e grão do Reel)

yt.ARGS_FONTES = A.fontes
yt.K = 1                       # grade do DS = pixels do Reel (1080 de largura)
yt.W, yt.H = W, H
yt.placa_pos = lambda it, info: tuple(CFG["placa_xy"])
ORIGINAL = os.environ[CFG["original_env"]]
AUDIO = os.environ[CFG["audio_env"]]
TMP = os.path.join(REV, "_tmp")
os.makedirs(TMP, exist_ok=True)


def q(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------- linha do tempo

def linha_do_tempo():
    planos, k = [], 0
    for p in CFG["planos"][:A.ate]:
        v0, v1 = p["video"]
        n = q(v1 - v0)
        a0 = p.get("audio", p["video"])[0]
        if p.get("audio_continua"):                     # o áudio segue o do plano anterior sem emenda
            a0 = planos[-1]["a0"] + planos[-1]["n"] / FPS
        planos.append({**p, "k0": k, "k1": k + n, "n": n, "a0": a0})
        k += n
    return planos, k


PLANOS, N = linha_do_tempo()


def k_de(p, t_audio):
    """quadro global do instante t_audio (segundos do original, na faixa de áudio do plano)."""
    return p["k0"] + q(t_audio - p["a0"])


def legendas():
    """grupos de legenda; um grupo fica até o próximo começar. Quando o áudio continua no plano seguinte (corte só de
    imagem), o grupo atravessa o corte."""
    todos = [(i, p, g) for i, p in enumerate(PLANOS) for g in p["legendas"]]
    out = []
    for n, (i, p, g) in enumerate(todos):
        if True:
            ks = [min(max(k_de(p, t), p["k0"]), p["k1"] - 1) for t in g["palavras"]]
            k0 = ks[0]                                   # a legenda entra com a 1ª palavra dita (DS 3.3), nunca antes
            fim = p["k1"]
            j = i
            while j + 1 < len(PLANOS) and PLANOS[j + 1].get("audio_continua"):
                j += 1
                fim = PLANOS[j]["k1"]                     # mesma fala contínua: pode atravessar o corte de imagem
            if n + 1 < len(todos):
                i2, p2, g2 = todos[n + 1]
                k1 = min(k_de(p2, g2["palavras"][0]), fim) if i2 <= j else p["k1"] if j == i else fim
                if i2 > j:
                    k1 = fim
            else:
                k1 = fim
            nwords = len(g["texto"].split())
            assert nwords == len(ks), g["texto"]
            fala = max((g["palavras"][-1] - g["palavras"][0]) + 0.35, 0.3)
            vel = nwords / fala
            it = {"texto": g["texto"], "texto_tela": g["texto"], "q0": k0, "q1": k1,
                  "modo": g.get("modo", "palavra" if vel <= 3.0 else "grupo"), "palavras_q": [k0] + ks[1:], "plano": p["id"]}
            linhas = g["texto"].split("\n")
            assert len(linhas) <= 2 and max(len(x) for x in linhas) <= 26 and nwords <= g.get("max_palavras", 6), g["texto"]
            out.append(rl.Legenda(it, A.fontes))
    return out


# ---------------------------------------------------------------- objetos

def placas():
    out = []
    for pl in CFG["placas"]:
        p = next(x for x in PLANOS if x["id"] == pl["plano"]) if any(x["id"] == pl["plano"] for x in PLANOS) else None
        if p is None:
            continue
        k0 = p["k0"] + q(pl.get("entra_s", 0.0))
        n = p["k1"] - k0
        it = {"variante": pl["variante"], "linha1": pl["linha1"], "linha2": pl["linha2"], "q_in": 0,
              "q_fim": n if pl["saida"] else n + 12}
        face, modulo, info = yt.placa_pecas(it)
        assert info["w_design"] <= 872, (pl["id"], info["w_design"])       # DS 2.1: largura máxima 872
        quadros = list(yt.quadros_placa(it))[:n]
        x0, y0 = CFG["placa_xy"]
        out.append({"id": pl["id"], "k0": k0, "quadros": quadros, "x": x0 - yt.PLACA_PAD, "y": y0 - yt.PLACA_PAD,
                    "caixa": [x0, y0, x0 + info["w_design"], y0 + info["h_design"]]})
    return out


def etiquetas():
    """etiqueta de valor: desliza da esquerda 160 ms (ease-out) e o número gira até o valor (240 ms)."""
    out = []
    for p in PLANOS:
        e = p.get("etiqueta")
        if not e:
            continue
        base, num, info = yt.etiqueta_obj(e["rotulo"], yt.Decimal(e["eur"]))
        marg = 40
        k0 = p["k0"] + q(e["entra_s"])
        quadros = []
        for k in range(k0, p["k1"]):
            t = (k - k0 + 1) * 1000 / FPS
            dx = yt.kf([(0, -140), (yt.D_FAST, 0)], t)
            op = yt.kf([(0, 0.0), (yt.D_FAST, 1.0)], t)
            giro = min(max((t - yt.D_FAST) / yt.D_BASE, 0), 1)
            o = base.copy()
            cam = yt.tela(o.shape[0], o.shape[1])
            yt.pintar(cam, num["m"], yt.GRAFITE, num["x"], num["y"] + (1 - yt.E_OUT(giro)) * (num["clip"][1] - num["clip"][0]))
            cam[:num["clip"][0]] = 0
            cam[num["clip"][1]:] = 0
            yt.sobre(o, cam, 0, 0)
            o = yt.com_sombra(o, "paper", marg) * op
            quadros.append((o, CFG["etiqueta_x"] - marg + dx, CFG["etiqueta_base_y"] - info["h"] - marg))
        out.append({"plano": p["id"], "k0": k0, "quadros": quadros,
                    "caixa": [CFG["etiqueta_x"], CFG["etiqueta_base_y"] - info["h"], CFG["etiqueta_x"] + info["w"], CFG["etiqueta_base_y"]]})
    return out


# ---------------------------------------------------------------- vídeo de base

TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709,format=gbrpf32le")


def ler_plano(p):
    cw = 1216
    if isinstance(p["cx"], list):                 # recorte que acompanha o rosto: [[t_original, cx], …], interpolação linear
        ks = [(t - p["video"][0], min(max(c * 3840 - cw / 2, 0), 3840 - cw)) for t, c in p["cx"]]
        expr = f"{ks[-1][1]:.1f}"
        for (t0, x0), (t1, x1) in reversed(list(zip(ks, ks[1:]))):
            expr = f"if(lt(t,{t1:.3f}),{x0:.1f}+({x1 - x0:.1f})*max(t-{t0:.3f},0)/{t1 - t0:.3f},{expr})"
        x = f"'{expr}'"
        p["recorte_x"] = [round(v[1]) for v in ks]
    else:
        x = int(round(p["cx"] * 3840 - cw / 2)) // 2 * 2
        x = min(max(x, 0), 3840 - cw)
        p["recorte_x"] = x
    vf = f"crop={cw}:2160:{x}:0,scale={W}:{H}:flags=lanczos,{TM}"
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{p['video'][0]:.4f}", "-i", ORIGINAL, "-frames:v", str(p["n"]), "-an",
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


def snap(img, j):
    """Snap (DS 4.4): 1 quadro de flash papel 30% + zoom 104% → 100% em 3 quadros."""
    if j >= 3:
        return img
    z = 1.04 - 0.04 * j / 3
    cw, ch = int(round(W / z)), int(round(H / z))
    x0, y0 = (W - cw) // 2, (H - ch) // 2
    canais = [np.asarray(Image.fromarray(np.ascontiguousarray(img[y0:y0 + ch, x0:x0 + cw, c]), "F").resize((W, H), Image.BICUBIC))
              for c in range(3)]
    out = np.clip(np.dstack(canais), 0, 1)
    if j == 0:
        out = out * 0.7 + yt.PAPEL * 0.3
    return out


# ---------------------------------------------------------------- áudio

def montar_audio():
    sr = 48000
    pedacos = []
    for p in PLANOS:
        a0 = p["a0"]
        dur = p["n"] / FPS
        f = os.path.join(TMP, f"a_{p['id']}.f32")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a0:.4f}", "-t", f"{dur:.4f}", "-i", AUDIO, "-ac", "2", "-ar", str(sr),
                        "-f", "f32le", f], check=True)
        x = np.fromfile(f, np.float32).reshape(-1, 2)
        n = int(round(dur * sr))
        x = np.pad(x, ((0, max(n - len(x), 0)), (0, 0)))[:n]
        nf = int(CFG["fade_corte_ms"] * sr / 1000)
        rampa = np.linspace(0, 1, nf, dtype=np.float32)[:, None]
        cont_antes = p.get("audio_continua")
        cont_depois = any(o.get("audio_continua") and o["k0"] == p["k1"] for o in PLANOS)
        if not cont_antes:
            x[:nf] *= rampa
        if not cont_depois:
            x[-nf:] *= rampa[::-1]
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
    LG, PL, ET = legendas(), placas(), etiquetas()
    scrim = rl.scrim_alfa()
    video = os.path.join(TMP, "video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-g", "48",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv", video],
                           stdin=subprocess.PIPE)
    registro, qa_dir = {}, os.path.join(REV, "qa_frames")
    os.makedirs(qa_dir, exist_ok=True)
    snap_em = {PLANOS[i + 1]["id"] for i, p in enumerate(PLANOS[:-1]) if p.get("snap_depois")}
    for p in PLANOS:
        for j, base in enumerate(ler_plano(p)):
            k = p["k0"] + j
            if p["id"] in snap_em:
                base = snap(base, j)
            img = rl.overlay_blend(base, rl.grao(k), rl.T["op_grain"])
            img = img * (1 - scrim) + rl.GRAFITE * scrim
            cam = np.zeros((H, W, 4), np.float32)
            els = []
            for e in ET:
                if e["k0"] <= k < e["k0"] + len(e["quadros"]):
                    o, x, y = e["quadros"][k - e["k0"]]
                    yt.sobre(cam, o, x, y)
                    els.append(("etiqueta", e["caixa"]))
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
    saida = os.path.join(REV, CFG["saida"] if A.ate is None else "previa_trailer.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c", "copy",
                    "-map_metadata", "-1", "-movflags", "+faststart", saida], check=True)
    rel = {"quadros": N, "duracao_s": round(N / FPS, 3), "lufs_antes": lufs_bruto, "ganho_db": ganho,
           "planos": [{k: p[k] for k in ("id", "video", "k0", "k1", "cx", "recorte_x")} for p in PLANOS],
           "elementos_por_quadro": {str(k): v for k, v in registro.items() if k % 12 == 0}}
    json.dump(rel, open(os.path.join(REV, "relatorio_tecnico_rev3.json"), "w"), ensure_ascii=False, indent=1)
    print("ok", saida, N, "quadros", round(N / FPS, 2), "s")


main()
