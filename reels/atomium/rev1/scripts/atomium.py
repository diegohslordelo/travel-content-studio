"""Reel 'Atomium: o cristal de ferro gigante de Bruxelas' (REV1): reel_atomium_rev1.mp4 (1080 × 1920, 24 qps, SDR BT.709).

Monta os planos do rev1.json a partir dos originais do Drive (iPhone 4K HEVC HLG / BT.2020; recorte 9:16 nos planos
horizontais, quadro inteiro nos verticais; tone mapping para BT.709, o mesmo do trailer de Barcelona) e aplica, quadro a
quadro, a camada do DS V2 com componentes que já existem nos pipelines aprovados (sem valor visual novo):
  - placa esmaltada com a assinatura Chegada (youtube/barcelona/rev2/scripts/rev2.py, grade 1:1 no Reel),
    abertura `PRIMEIRO DIA EM / BRUXELAS` em x 72 · y 640, sai pela direita antes do ticket (DS 2.1);
  - legenda Padrão do Reel com destaque por mini-placa (reels/apresentacao/rev8/scripts/rev8.py);
  - scrim sempre ligado e grão 5%;
  - ticket 'SABIA?' (DS 2.3 e 2.6, Curiosidade): papel, entalhes de 28 px, picote, `?` amarelo no canhoto,
    Condensed 800 itálico, Plex Mono; subida e assentamento pelos quadros-chave do bundle (pd-rise, 440 ms),
    sem foil nem furo (a variante não tem estrela); sai subindo 120 px em 240 ms (DS 2.3).
Áudio: o som direto de cada plano (ou a voz da selfie IMG_2170 por cima dos planos do Atomium), fade de 8 ms em cada
corte, master −14 LUFS e pico verdadeiro ≤ −1 dBTP (limitador com sobreamostragem 4×, AAC 256 kbps).

Uso (de dentro de reels/atomium/):
  PD_BRUXELAS=PASTA_COM_OS_MOV python3 rev1/scripts/atomium.py --fontes PASTA_TTF [--qa]
Fontes (SIL OFL, Google Fonts): Barlow-Bold, Barlow-Medium, BarlowCondensed-SemiBold/-Bold/-ExtraBold/-ExtraBoldItalic,
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
CFG = json.load(open(os.path.join(REV, "rev1.json"), encoding="utf-8"))
FPS, W, H = CFG["fps"], CFG["largura"], CFG["altura"]

ap = argparse.ArgumentParser()
ap.add_argument("--fontes", default=os.environ.get("PD_FONTES", ""))
ap.add_argument("--qa", action="store_true", help="salva um quadro por plano em rev1/qa_frames")
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
yt.SOMBRAS["lift"] = [(28, 50, -14, 0.55)]     # token shadow-lift
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
                k1 = min(k_de(p2, g2["palavras"][0]), fim)
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
    return out


# ---------------------------------------------------------------- objetos

def placas():
    out = []
    for pl in CFG["placas"]:
        p = next(x for x in PLANOS if x["id"] == pl["plano"])
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


def ticket_obj(palavra, micro):
    """ticket 'SABIA?' (DS 2.3/2.6; medidas do bundle .pd-ticket): papel paper-500 com entalhes de 28 px nas laterais,
    corpo (micro Plex Mono 28 night-500 + palavra Condensed 800 itálico 96 grafite), canhoto de 150 px com picote
    vertical e `?` amarelo com contorno grafite de 3 px no lugar da estrela; fibra 4%."""
    ml, wl, bl, cl = yt.texto(micro.upper(), yt.FT["mono"], 28, 0.06)
    mw, ww, bw, cw = yt.texto(palavra.upper(), "BarlowCondensed-ExtraBoldItalic.ttf", 96, 0.01)
    pt, pr, pb, pl, ent = 30, 34, 32, 62, 14
    stub, mr = 150, 30
    corpo_w = pl + max(wl, ww) + pr
    hd = 220                                                 # DS 2.3: ≈ 640 × 220
    wd = int(round(corpo_w + stub + mr))
    base = yt.tela(hd, wd)
    r = 28

    def papel(d, s):
        d.rounded_rectangle([0, 0, wd * s - 1, hd * s - 1], radius=yt.tok("radius.paper")["value"] * s, fill=255)
        for cx in (0, wd):
            d.ellipse([(cx - r) * s, (hd / 2 - r) * s, (cx + r) * s, (hd / 2 + r) * s], fill=0)
    yt.pintar(base, yt.forma(wd, hd, papel), yt.PAPEL, 0, 0)
    yt.fibra(base, 23, yt.OP_FIBRA)
    furo = yt.forma(6, 6, lambda d, s: d.ellipse([0, 0, 6 * s - 1, 6 * s - 1], fill=255))
    xs = corpo_w
    for y in np.arange(14, hd - 14, 16):                     # picote: furos de 6 px a cada 16 px (DS 1.6)
        yt.pintar(base, furo, yt.CONCRETO, xs - 3, y)
    alt_txt = 28 + ent + cw
    y_top = (hd - alt_txt) / 2
    yt.pintar(base, ml, yt.ASFALTO, pl - 2, y_top + cl - bl + 2)
    yt.pintar(base, mw, yt.GRAFITE, pl - 2, y_top + 28 + ent + cw - bw)
    mq, wq, bq, cq = yt.texto("?", "BarlowCondensed-ExtraBoldItalic.ttf", 104, 0)
    mq = np.pad(mq, 4)
    contorno = rl.ndimage.grey_dilation(mq, size=(7, 7))     # contorno grafite de 3 px, como o da estrela
    qx = xs + (stub - wq) / 2 - 2 - 4
    qy = (hd - cq) / 2 + cq - bq - 4
    yt.pintar(base, contorno, yt.GRAFITE, qx, qy)
    yt.pintar(base, mq, yt.AMARELO, qx, qy)
    return base


def ticket_quadros():
    tk = CFG["ticket"]
    p = next(x for x in PLANOS if x["id"] == tk["plano"])
    k0 = p["k0"] + q(tk["entra_s"])
    k1 = p["k1"]
    obj = ticket_obj(tk["palavra"], tk["micro"])
    rot_rep = yt.tok("rotation.rot-ticket")
    E_IO = rl.E_OUT if hasattr(rl, "E_OUT") else yt.E_OUT
    marg = 90
    n = k1 - k0
    t_saida = n * 1000 / FPS - yt.D_BASE
    quadros, cache = [], {}
    h, w = obj.shape[:2]
    for k in range(n):
        t = (k + 1) * 1000 / FPS
        if t < t_saida:
            # bundle pd-rise (440 ms, ease-out): 0% y+260 s.9 r0 op0 → 70% y−8 s1.03 r5 op1 → 100% y0 s1 r4
            dy = yt.kf([(0, 260), (308, -8), (440, 0)], t, E_IO)
            esc = yt.kf([(0, 0.9), (308, 1.03), (440, 1.0)], t, E_IO)
            rot = yt.kf([(0, 0.0), (308, 5.0), (440, rot_rep)], t, E_IO)
            op = yt.kf([(0, 0.0), (308, 1.0)], t, E_IO)
            sombra = "lift" if t < 320 else "paper"
        else:                                                 # DS 2.3: continua subindo (−120 px) e some, 240 ms
            ts = t - t_saida
            dy = yt.kf([(0, 0), (240, -120)], ts, yt.E_EXIT)
            op = yt.kf([(0, 1.0), (240, 0.0)], ts, yt.E_EXIT)
            esc, rot, sombra = 1.0, rot_rep, "paper"
        chave = (round(esc, 3), round(rot, 2), round(op, 2), sombra)
        if chave not in cache:
            o = obj
            if abs(esc - 1) > 1e-3:
                nw, nh = max(int(round(w * esc)), 1), max(int(round(h * esc)), 1)
                o = np.dstack([np.asarray(Image.fromarray(np.ascontiguousarray(obj[..., c]), "F").resize((nw, nh), Image.BICUBIC))
                               for c in range(4)]).clip(0, None)
            c = yt.tela(o.shape[0] + 2 * marg, o.shape[1] + 2 * marg)
            yt.sobre(c, o, marg, marg)
            c = yt.girar(c, rot, (c.shape[1] / 2, c.shape[0] / 2))
            core = c[marg // 2:-marg // 2, marg // 2:-marg // 2]
            cache = {chave: yt.com_sombra(core, sombra, marg // 2) * op}
        img = cache[chave]
        # posição: o centro do ticket fica onde estaria em repouso (escala em torno do centro)
        cx, cy = tk["x"] + w / 2, tk["y"] + h / 2 + dy
        quadros.append((img, cx - img.shape[1] / 2, cy - img.shape[0] / 2))
    return {"k0": k0, "quadros": quadros, "caixa": [tk["x"], tk["y"], tk["x"] + w, tk["y"] + h]}


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
    for f in ("Barlow-Bold.ttf", "BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-SemiBold.ttf", "IBMPlexMono-Medium.ttf",
              "BarlowCondensed-ExtraBoldItalic.ttf"):
        assert os.path.exists(os.path.join(A.fontes, f)), f
    LG, PL, TK = legendas(), placas(), ticket_quadros()
    fim_placa = max(pl["k0"] + len(pl["quadros"]) for pl in PL)
    assert fim_placa <= TK["k0"], "DS 2.1: a placa sai antes do ticket entrar"
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
            if TK["k0"] <= k < TK["k0"] + len(TK["quadros"]):
                o, x, y = TK["quadros"][k - TK["k0"]]
                yt.sobre(cam, o, x, y)
                els.append(("ticket", TK["caixa"]))
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
    json.dump(rel, open(os.path.join(REV, "relatorio_tecnico_rev1.json"), "w"), ensure_ascii=False, indent=1)
    print("ok", saida, N, "quadros", round(N / FPS, 2), "s")


main()
