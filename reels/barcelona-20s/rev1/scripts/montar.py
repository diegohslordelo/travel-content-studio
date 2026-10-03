"""Etapa 2 — montagem sem camada de marca: trechos (cortes secos) + áudio ambiente + grão 5%.

Roda de dentro de reels/barcelona-20s. Lê rev1/cortes.yaml.
  python3 rev1/scripts/montar.py --largura 540 --saida rev1/previa/previa_sem_marca_540x960.mp4 --usar-proposta
  python3 rev1/scripts/montar.py --largura 1080 --saida rev1/reel_bcn_v1_sem_marca.mp4

Vídeo: recorte 9:16 pelo reenquadre_x (fonte 3840×2160 → 1215×2160 → largura × 16/9, sem upscale),
       24 → 30 fps por repetição de quadro (fps=30), cortes secos, grão 5% (op-grain) em blend overlay,
       novo a cada quadro e com intensidade fixa (mesma receita do rev8.py).
Áudio: som do próprio trecho (ou ambiente substituto marcado em cortes.yaml), crossfade de 80 ms
       (potência constante, centrado no corte), trechos aproximados da média (NIVELAR), normalizado para
       −14 LUFS integrados (pyloudnorm, BS.1770) com limitador de pico verdadeiro em −1 dBTP.
"""
import argparse
import json
import os
import subprocess

import numpy as np
import pyloudnorm
import yaml
from scipy import ndimage
from scipy.signal import resample_poly

FPS = 30
SR = 48000
XFADE = 0.080
LUFS = -14.0
NIVELAR = 0.7    # aproxima cada trecho da média de loudness em 70% (o ônibus a −10 e a vista a −28 LUFS saltavam 18 LU)
TETO_TP = -1.5   # dBTP após normalizar (margem de 0,5 dB para o AAC; alvo de entrega −1 dBTP) (limitador com pico verdadeiro 4× sobreamostrado)
OP_GRAIN = 0.05        # tokens: opacity.op-grain
GRAO_SIGMA_1080 = 0.7  # mesma textura do rev8 (px a 1080 de largura)
SEMENTE = 20261003
RAIZ = "../.."

def trechos(cortes, usar_proposta):
    out = []
    for e in cortes["espacos"]:
        t = e["vencedor"]
        if t is None:
            if not usar_proposta or not e.get("proposta", {}).get("trecho"):
                raise SystemExit(f"Espaço {e['espaco']} vazio: pare e decida antes de montar (use --usar-proposta "
                                 "só para a prévia)")
            t = dict(e["proposta"]["trecho"], proposta=True)
        dur = t["duracao"] + (t.get("fechamento") or {}).get("duracao", 0.0)
        out.append(dict(t, espaco=e["espaco"], tipo=e["tipo"], dur_total=dur))
    return out


def video_cmd(ts, W, H):
    args, filtros = [], []
    for i, t in enumerate(ts):
        args += ["-ss", f"{t['inicio']:.3f}", "-t", f"{t['dur_total'] + 0.5:.3f}", "-i", f"{RAIZ}/{t['arquivo']}"]
        n = int(round(t["dur_total"] * FPS))
        crop = f"crop=1215:2160:{t['reenquadre_x']}:0," if "reenquadre_x" in t else ""
        filtros.append(f"[{i}:v:0]{crop}scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},"
                       f"trim=end_frame={n},setpts=N/{FPS}/TB[v{i}]")
    filtros.append("".join(f"[v{i}]" for i in range(len(ts))) + f"concat=n={len(ts)}:v=1:a=0,format=rgb24[v]")
    return ["ffmpeg", "-v", "error", *args, "-filter_complex", ";".join(filtros), "-map", "[v]",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]


def ler_audio(arq, ini, dur):
    pre = min(ini, XFADE / 2)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ini - pre:.4f}", "-t", f"{dur + pre + XFADE:.4f}",
                          "-i", f"{RAIZ}/{arq}", "-map", "0:a:0", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2), pre


def fonte_audio(t):
    """Áudio do próprio trecho, ou o ambiente substituto escolhido em selecionar.py (cortes.yaml)."""
    if t["audio"] == "substituir":
        if not t.get("audio_substituto"):
            raise SystemExit(f"Espaço {t['espaco']}: áudio a substituir sem ambiente substituto aprovado")
        s = t["audio_substituto"]
        return s["arquivo"], s["inicio"] + XFADE / 2
    return t["arquivo"], t["inicio"]


def limitar(x, teto_db):
    """Limitador de pico verdadeiro: envelope de ganho com ataque 2 ms e soltura 80 ms."""
    teto = 10 ** (teto_db / 20)
    up = np.abs(resample_poly(x, 4, 1, axis=0)).max(axis=1).reshape(-1, 4).max(axis=1)[:len(x)]
    alvo = np.minimum(1.0, teto / np.maximum(up, 1e-9))
    alvo = ndimage.minimum_filter1d(alvo, int(0.002 * SR) * 2 + 1)  # olha 2 ms à frente
    g = np.empty_like(alvo)
    a_sol = np.exp(-1 / (0.080 * SR))
    v = 1.0
    for i, t in enumerate(alvo):
        v = t if t < v else t + (v - t) * a_sol
        g[i] = v
    return (x * g[:, None]).astype(np.float32), float(20 * np.log10(up.max()))


def montar_audio(ts):
    total = sum(t["dur_total"] for t in ts)
    medidor = pyloudnorm.Meter(SR)
    niveis = [medidor.integrated_loudness(ler_audio(*fonte_audio(t), t["dur_total"])[0]) for t in ts]
    media = float(np.mean(niveis))
    ganhos = [10 ** (NIVELAR * (media - n) / 20) for n in niveis]
    mix = np.zeros((int(round(total * SR)) + SR, 2), np.float32)
    h = XFADE / 2
    t0 = 0.0
    fontes = []
    for i, t in enumerate(ts):
        arq, ini = fonte_audio(t)
        a, pre = ler_audio(arq, ini, t["dur_total"])
        # janela: começa h antes do corte (exceto no 1º trecho) e termina h depois do corte seguinte
        ini_rel = 0.0 if i == 0 else pre - h
        fim_rel = pre + t["dur_total"] + (h if i < len(ts) - 1 else 0.0)
        seg = a[int(round(ini_rel * SR)):int(round(fim_rel * SR))].copy()
        seg *= ganhos[i]
        nx = int(round(XFADE * SR))
        rampa = np.sin(np.linspace(0, np.pi / 2, nx, dtype=np.float32)) ** 2  # potência constante (sin²+cos²)
        if i > 0:
            seg[:nx] *= rampa[:, None]
        if i < len(ts) - 1:
            seg[-nx:] *= rampa[::-1, None]
        pos = int(round((t0 - (0.0 if i == 0 else h)) * SR))
        mix[pos:pos + len(seg)] += seg
        fontes.append({"espaco": t["espaco"], "audio_de": arq, "inicio_fonte": round(ini, 3),
                       "substituto": t["audio"] == "substituir", "lufs_trecho": round(niveis[i], 1),
                       "ganho_nivelamento_db": round(20 * np.log10(ganhos[i]), 1)})
        t0 += t["dur_total"]
    mix = mix[:int(round(total * SR))]
    # bordas do loop: 20 ms de rampa para não estalar na volta ao início
    nb = int(0.02 * SR)
    mix[:nb] *= np.linspace(0, 1, nb, dtype=np.float32)[:, None]
    mix[-nb:] *= np.linspace(1, 0, nb, dtype=np.float32)[:, None]
    antes = medidor.integrated_loudness(mix)
    mix = (mix * 10 ** ((LUFS - antes) / 20)).astype(np.float32)
    mix, tp_antes = limitar(mix, TETO_TP)
    # o limitador baixa um pouco o integrado: uma segunda passada recupera o alvo
    for _ in range(3):
        d = LUFS - medidor.integrated_loudness(mix)
        if abs(d) < 0.05:
            break
        mix, _ = limitar((mix * 10 ** (d / 20)).astype(np.float32), TETO_TP)
    return mix, {"lufs_antes": round(antes, 2), "lufs_alvo": LUFS, "lufs_final": round(medidor.integrated_loudness(mix), 2),
                 "tp_antes_limitador_dbtp": round(tp_antes, 2), "teto_dbtp": TETO_TP, "nivelamento": NIVELAR,
                 "fontes": fontes}


def grao(k, W, H):
    rng = np.random.default_rng(SEMENTE + k)
    z = ndimage.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), GRAO_SIGMA_1080 * W / 1080)
    z /= z.std()
    return np.clip(0.5 + 0.289 * z, 0, 1)[..., None]


def overlay(b, n, op):
    o = np.where(b < 0.5, 2 * b * n, 1 - 2 * (1 - b) * (1 - n))
    return b + op * (o - b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--largura", type=int, default=1080)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--usar-proposta", action="store_true", help="preenche espaço vazio com a proposta (só prévia)")
    ap.add_argument("--bitrate", default="14M")
    a = ap.parse_args()
    W = a.largura
    H = W * 16 // 9
    cortes = yaml.safe_load(open("rev1/cortes.yaml"))
    ts = trechos(cortes, a.usar_proposta)
    os.makedirs(os.path.dirname(a.saida) or ".", exist_ok=True)
    audio, info_audio = montar_audio(ts)
    wav = a.saida + ".tmp.f32"
    audio.tofile(wav)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav,
                            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
                            "-b:v", a.bitrate, "-minrate", a.bitrate, "-maxrate", a.bitrate, "-bufsize", a.bitrate,
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR),
                            "-movflags", "+faststart", "-shortest", a.saida], stdin=subprocess.PIPE)
    dec = subprocess.Popen(video_cmd(ts, W, H), stdout=subprocess.PIPE)
    k = 0
    tam = W * H * 3
    while True:
        buf = dec.stdout.read(tam)
        if len(buf) < tam:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        f = overlay(f, grao(k, W, H), OP_GRAIN)
        enc.stdin.write((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        k += 1
    dec.wait()
    enc.stdin.close()
    enc.wait()
    os.remove(wav)
    linha, t0 = [], 0.0
    for t in ts:
        linha.append({"espaco": t["espaco"], "tipo": t["tipo"], "arquivo": t["arquivo"], "inicio_fonte": t["inicio"],
                      "duracao": t["dur_total"], "no_reel": [round(t0, 3), round(t0 + t["dur_total"], 3)],
                      "proposta": t.get("proposta", False), "audio": t["audio"]})
        t0 += t["dur_total"]
    json.dump({"saida": a.saida, "quadros": k, "fps": FPS, "w": W, "h": H, "linha_do_tempo": linha,
               "audio": info_audio}, open(a.saida + ".json", "w"), ensure_ascii=False, indent=1)
    print(a.saida, k, "quadros", info_audio["lufs_antes"], "→", LUFS, "LUFS")


if __name__ == "__main__":
    main()
