"""Espectrogramas (PNG) de trechos de áudio, com forma de onda e marcas de fala.

Uso: python3 espectro.py saida.png titulo "arq.wav:inicio:fim:rotulo[:marcas]" ...
marcas = "a-b,c-d" (trechos de voz, no tempo do arquivo)
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from scipy import signal  # noqa: E402

FUNDO, TINTA, SUAVE = "#101418", "#E8E6E1", "#8A9199"
# sequencial de um matiz só (azul, do escuro ao claro): mais claro = mais energia
CMAP = LinearSegmentedColormap.from_list("azul", ["#101418", "#16324A", "#1F5C8A", "#4A90C8", "#A9D3F2", "#F2F8FC"])
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": TINTA, "axes.labelcolor": SUAVE,
                     "xtick.color": SUAVE, "ytick.color": SUAVE, "axes.edgecolor": "#2A3038"})

saida, titulo, itens = sys.argv[1], sys.argv[2], sys.argv[3:]
fig, eixos = plt.subplots(len(itens) * 2, 1, figsize=(12, 3.4 * len(itens)),
                          gridspec_kw={"height_ratios": [1, 4] * len(itens)}, facecolor=FUNDO)
for k, item in enumerate(itens):
    p = item.split("|")
    arq, a, b, rot = p[0], float(p[1]), float(p[2]), p[3]
    marcas = [tuple(map(float, m.split("-"))) for m in p[4].split(",")] if len(p) > 4 and p[4] else []
    x, sr = sf.read(arq, start=int(a * 48000), stop=int(b * 48000), always_2d=True)
    x = x.mean(1)
    t = a + np.arange(len(x)) / sr
    ax_w, ax_s = eixos[2 * k], eixos[2 * k + 1]
    for ax in (ax_w, ax_s):
        ax.set_facecolor(FUNDO)
    ax_w.plot(t, x, color="#4A90C8", lw=0.5)
    ax_w.set_xlim(a, b)
    ax_w.set_ylim(-1, 1)
    ax_w.set_yticks([-1, 0, 1])
    ax_w.set_xticklabels([])
    ax_w.set_title(rot, loc="left", color=TINTA, fontsize=10, pad=4)
    for m0, m1 in marcas:
        ax_w.axvspan(m0, m1, color="#E8B24A", alpha=0.18, lw=0)
    f, tt, S = signal.spectrogram(x, sr, nperseg=2048, noverlap=1792, window="hann")
    Sdb = 10 * np.log10(S + 1e-14)
    top = np.percentile(Sdb, 99.7)
    ax_s.pcolormesh(tt + a, f / 1000, Sdb, shading="auto", cmap=CMAP, vmin=top - 80, vmax=top, rasterized=True)
    ax_s.set_yscale("symlog", linthresh=1.0, linscale=0.6)
    ax_s.set_ylim(0.03, 20)
    ax_s.set_yticks([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
    ax_s.set_yticklabels(["50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax_s.set_ylabel("Hz")
    ax_s.set_xlabel("segundos", color=SUAVE)
    for fr in (5, 9):
        ax_s.axhline(fr, color="#D9693A", lw=0.4, alpha=0.5)
fig.suptitle(titulo, x=0.01, ha="left", color=TINTA, fontsize=12)
fig.text(0.99, 0.995, "mais claro = mais energia (escala de 80 dB) · faixa amarela = voz · linhas laranja = 5 e 9 kHz (sibilância)",
         ha="right", va="top", color=SUAVE, fontsize=8)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(saida, dpi=110, facecolor=FUNDO)
print(saida)
