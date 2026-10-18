"""Movimento de câmera por clipe: deslocamento global entre quadros vizinhos (correlação de fase),
em pixels do Reel final (1080 × 1920), e a janela mais estática de cada clipe.

Usado na REV2 para escolher os trechos parados (pedido do Diego, 18/10/2026). Precisa de numpy e ffmpeg.
Limite: não mede câmera andando para a frente (vira zoom, não deslocamento); conferir sempre no olho.

uso: python3 analise_movimento.py <pasta> <janela_s> <saida.json> arquivo [arquivo ...]
"""
import json
import subprocess
import sys

import numpy as np

pasta, janela_s, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
arquivos = sys.argv[4:]
LARG = 480  # largura de análise


def sonda(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:stream_side_data=rotation", "-of", "json", arq],
                       capture_output=True, text=True)
    s = json.loads(r.stdout)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    w, h = s["width"], s["height"]
    if rot % 180:
        w, h = h, w
    return w, h, float(num) / float(den)


def quadros(arq, w, h):
    alt = round(h * LARG / w / 2) * 2
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", f"scale={LARG}:{alt}:flags=area,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    v = np.frombuffer(p.stdout, dtype=np.uint8)
    n = v.size // (LARG * alt)
    return v[: n * LARG * alt].reshape(n, alt, LARG).astype(np.float32), alt


def desloc(a, b, jan):
    A = np.fft.fft2((a - a.mean()) * jan)
    B = np.fft.fft2((b - b.mean()) * jan)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-6
    c = np.real(np.fft.ifft2(R))
    iy, ix = np.unravel_index(np.argmax(c), c.shape)

    def sub(cm, cz, cp):
        d = cm - 2 * cz + cp
        return 0.0 if abs(d) < 1e-9 else 0.5 * (cm - cp) / d

    H, W = c.shape
    dy = iy + sub(c[(iy - 1) % H, ix], c[iy, ix], c[(iy + 1) % H, ix])
    dx = ix + sub(c[iy, (ix - 1) % W], c[iy, ix], c[iy, (ix + 1) % W])
    if dy > H / 2:
        dy -= H
    if dx > W / 2:
        dx -= W
    return dx, dy


res = {}
for nome in arquivos:
    arq = f"{pasta}/{nome}"
    w, h, fps = sonda(arq)
    q, alt = quadros(arq, w, h)
    jan = np.outer(np.hanning(alt), np.hanning(LARG)).astype(np.float32)
    # px de análise → px do Reel: retrato ocupa a largura toda (1080 / w);
    # paisagem é recortada em 9:16 na altura toda (1920 / h)
    fator = (w / LARG) * (1080 / w if h > w else 1920 / h)
    m = []
    for i in range(1, len(q)):
        dx, dy = desloc(q[i], q[i - 1], jan)
        m.append(float(np.hypot(dx, dy) * fator))
    m = np.array(m)
    n = max(1, round(janela_s * fps))
    if len(m) < n:
        res[nome] = {"fps": fps, "dur": len(q) / fps, "curto": True, "media_total": float(m.mean()) if len(m) else None}
        print(f"{nome:18s} curto ({len(q) / fps:.2f} s)")
        continue
    medias = np.convolve(m, np.ones(n) / n, mode="valid")
    i0 = int(np.argmin(medias))
    res[nome] = {
        "fps": fps, "dur": round(len(q) / fps, 3), "media_total": round(float(m.mean()), 2),
        "melhor_ini": round(i0 / fps, 2), "melhor_fim": round((i0 + n) / fps, 2),
        "melhor_media": round(float(medias[i0]), 2), "melhor_max": round(float(m[i0:i0 + n].max()), 2),
        "por_quadro": [round(x, 2) for x in m.tolist()],
    }
    print(f"{nome:18s} dur {len(q) / fps:5.2f} s · média {m.mean():6.2f} px/q · melhor {i0 / fps:5.2f}–{(i0 + n) / fps:5.2f} s:"
          f" média {medias[i0]:5.2f} · máx {m[i0:i0 + n].max():5.2f}", flush=True)
with open(saida, "w") as f:
    json.dump(res, f)
