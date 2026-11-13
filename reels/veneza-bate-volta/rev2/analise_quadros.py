"""Análise quadro a quadro de um vídeo do Reel (rodar de dentro de rev2): uso python3 analise_quadros.py <video.mp4>.

Mede, quadro a quadro, a diferença entre quadros consecutivos na metade de cima (y < 900), na de baixo e na tela toda.
Lista os cortes (saltos de imagem), a duração de cada plano e os planos curtos (< 1,5 s), além de quadros escuros.
"""
import subprocess, sys
import numpy as np

v = sys.argv[1]
W, H = 108, 192
raw = subprocess.run(f'ffmpeg -v error -i "{v}" -vf scale={W}:{H},format=gray -f rawvideo -', shell=True, capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
n = len(f)
fps = 30
top = np.abs(np.diff(f[:, :90], axis=0)).mean((1, 2))
bot = np.abs(np.diff(f[:, 90:144], axis=0)).mean((1, 2))
full = np.abs(np.diff(f, axis=0)).mean((1, 2))
lum = f.mean((1, 2))


def cortes(d, th):
    return [i + 1 for i in range(len(d)) if d[i] > th and d[i] > 2.5 * np.median(d[max(0, i - 15):i + 15])]


for nome, d, th in [("CIMA", top, 18), ("BAIXO", bot, 14), ("TELA", full, 16)]:
    c = cortes(d, th)
    pts = [0] + c + [n]
    planos = [(pts[k] / fps, (pts[k + 1] - pts[k]) / fps) for k in range(len(pts) - 1)]
    curtos = [(round(a, 2), round(b, 2)) for a, b in planos if b < 1.5]
    print(f"{nome}: {len(c)} cortes · planos < 1,5 s: {curtos}")
esc = [round(i / fps, 2) for i in range(n) if lum[i] < 18]
print("quadros muito escuros:", esc[:20], "…" if len(esc) > 20 else "")
