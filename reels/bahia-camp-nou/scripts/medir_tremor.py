"""Tremor de câmera por janela: deslocamento global quadro a quadro (correlação de fase em cinza 480 px) e o resíduo
de alta frequência (deslocamento menos a média móvel de 0,5 s), em px de um quadro 1080 de largura. Rodar de reels/bahia-camp-nou/.

Uso: python3 scripts/medir_tremor.py JANELA_S ARQ [ARQ ...]
"""
import subprocess
import sys

import numpy as np
from scipy import ndimage

jan = float(sys.argv[1])
for arq in sys.argv[2:]:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/brutos/{arq}", "-vf", "scale=480:-2,format=gray", "-f",
                        "rawvideo", "-"], capture_output=True, check=True)
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                         "-of", "csv=p=0"], input=None, capture_output=True, text=True)
    w = 480
    n = len(r.stdout)
    h = None
    for hh in (270, 853, 854, 852):
        if n % (w * hh) == 0:
            h = hh
            break
    q = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
    win = np.outer(np.hanning(h), np.hanning(w))
    d = []
    for a, b in zip(q[:-1], q[1:]):
        A, B = np.fft.fft2((a - a.mean()) * win), np.fft.fft2((b - b.mean()) * win)
        c = np.fft.ifft2(A * np.conj(B) / (np.abs(A * np.conj(B)) + 1e-6)).real
        y, x = np.unravel_index(np.argmax(c), c.shape)
        d.append((x if x < w / 2 else x - w, y if y < h / 2 else y - h))
    d = np.array(d, np.float32) * (1080 / w)
    pos = np.cumsum(d, 0)
    res = pos - ndimage.uniform_filter1d(pos, 12, axis=0)
    fps = 24
    k = int(jan * fps)
    out = []
    for i in range(0, len(res) - k, 6):
        out.append((i / fps, float(np.sqrt((res[i:i + k] ** 2).sum(1).mean())), float(np.abs(d[i:i + k]).mean())))
    out.sort(key=lambda x: x[1])
    print(arq, f"{len(q) / fps:.1f}s", "melhores:", " ".join(f"{t:.2f}s(trem {j:.1f}, mov {m:.1f})" for t, j, m in out[:6]))
