"""Compara o timbre da mesma fala em duas versões (referência crua x tratada), alinhadas por correlação.

Uso: python3 timbre.py nome ref.wav ref_ini ref_fim teste.wav teste_ini_aprox busca_s
Mostra, por 1/3 de oitava, quanto a versão tratada tem a mais/menos que a crua (normalizado em 500-2000 Hz),
separando janelas com voz e sem voz.
"""
import sys

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
nome, ref_arq, r0, r1, tst_arq, t0, busca = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:5]), sys.argv[5], *map(float, sys.argv[6:8])
ref, _ = sf.read(ref_arq, always_2d=True)
tst, _ = sf.read(tst_arq, always_2d=True)
import os
CH = os.environ.get("CANAL")
ref, tst = (ref.mean(1), tst.mean(1)) if CH is None else (ref[:, int(CH)], tst[:, int(CH)])
bp = signal.butter(4, [300, 3000], "bandpass", fs=SR, output="sos")
a = signal.sosfiltfilt(bp, ref[int(r0 * SR):int(r1 * SR)])
b0 = int((t0 - busca) * SR)
b = signal.sosfiltfilt(bp, tst[b0:int((t0 + (r1 - r0) + busca) * SR)])
c = signal.correlate(b, a, mode="valid", method="fft")
k = int(np.argmax(np.abs(c)))
norm = c[k] / np.sqrt(np.sum(a ** 2) * np.sum(b[k:k + len(a)] ** 2))
ini = (b0 + k) / SR
print(f"{nome}: trecho {r0:.2f}-{r1:.2f} da referência = {ini:.3f}-{ini + r1 - r0:.3f} no teste (correlação {norm:.2f})")
R = ref[int(r0 * SR):int(r1 * SR)]
T = tst[b0 + k:b0 + k + len(R)]
J = 1024
nj = len(R) // J
fr = lambda x: x[:nj * J].reshape(nj, J)
er = 20 * np.log10(np.sqrt((signal.sosfiltfilt(bp, R)[:nj * J].reshape(nj, J) ** 2).mean(1)) + 1e-10)
voz = er > er.max() - 18
win = np.hanning(J)
def espectro(x, m):
    X = np.abs(np.fft.rfft(fr(x)[m] * win, axis=1)) ** 2
    return X.mean(0)
f = np.fft.rfftfreq(J, 1 / SR)
cs = [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]
def bandas(P):
    return np.array([10 * np.log10(P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].mean() + 1e-20) for c in cs])
for rot, m in (("voz", voz), ("sem voz", ~voz)):
    if m.sum() < 3:
        continue
    d = bandas(espectro(T, m)) - bandas(espectro(R, m))
    d -= d[(np.array(cs) >= 500) & (np.array(cs) <= 2000)].mean()
    print(f"  {rot} ({m.sum()} janelas): " + " ".join(f"{c if c < 1000 else str(c // 1000) + 'k' if c % 1000 == 0 else str(c / 1000) + 'k'}:{v:+.1f}" for c, v in zip(cs, d)))
def hf(x, m):
    P = espectro(x, m)
    return 10 * np.log10(P[(f >= 4000) & (f < 12000)].sum() / P[(f >= 300) & (f < 4000)].sum())
print(f"  agudos 4-12k / 300-4k na voz: referência {hf(R, voz):.1f} dB, teste {hf(T, voz):.1f} dB (diferença {hf(T, voz) - hf(R, voz):+.1f} dB)")
