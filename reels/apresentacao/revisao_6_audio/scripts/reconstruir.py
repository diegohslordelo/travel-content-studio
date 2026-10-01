"""Reconstrói a narração tratada da revisão 5 (mesma cadeia do render.py) e mede quanto dela está no Reel.

Saídas em ../a/: nar_bruta.wav (tomada cortada, sem tratamento), nar_rev5.wav (tratada como na rev. 5),
nar_rev5_no_reel.wav (na linha do tempo do Reel, com o ganho e o atraso achados no mix).
"""
import os
import sys

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJ, "scripts"))
os.environ["REEL_TMP"] = os.path.join(AQUI, "..", "tmp")
import render as R  # noqa: E402

A = os.path.join(AQUI, "..", "a")
edl = R.carregar(os.path.join(PROJ, "lista_de_cortes.json"))
nar = edl["narracao"]
a, b = nar["corte_tomada"]
bruta = os.path.join(A, "nar_bruta.wav")
R.rodar(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PROJ, nar["arquivo"]), "-af",
         f"atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aresample=48000:resampler=soxr,aformat=channel_layouts=stereo",
         "-c:a", "pcm_f32le", bruta])
proc = os.path.join(A, "nar_rev5.wav")
va, vb = nar["voz_trecho"]
info = R.tratar_voz(edl, bruta, proc, (va - a, vb - a), float(nar["voz_nr"]), float(edl["audio"]["fala_lufs"]))
print("tratar_voz:", info)

# coloca na linha do tempo do Reel (fades como no render) e acha ganho/atraso por correlação com o mix
v, sr = sf.read(proc, always_2d=True)
n = len(v)
f_in, f_out = int(0.03 * sr), int(0.1 * sr)
env = np.ones(n)
env[:f_in] = np.linspace(0, 1, f_in)
env[-f_out:] = np.linspace(1, 0, f_out)
v = v * env[:, None]
mix, _ = sf.read(os.path.join(A, "rev5.wav"), always_2d=True)
t0 = int(float(nar["inicio"]) * sr)
seg = mix[t0 - 2400:t0 + n + 2400].mean(1)
vm = v.mean(1)
# atraso fino: correlação cruzada em ±50 ms
best = None
for d in range(-2400, 2401, 1):
    s = seg[2400 + d:2400 + d + n]
    c = float(np.dot(s, vm))
    if best is None or c > best[1]:
        best = (d, c)
d = best[0]
s = seg[2400 + d:2400 + d + n]
g = float(np.dot(s, vm) / np.dot(vm, vm))
res = s - g * vm
print(f"atraso {d} amostras ({d / sr * 1000:.2f} ms), ganho {20 * np.log10(g):+.2f} dB")
m_voz = np.abs(vm) > 0
def rmsdb(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
print(f"mix na narração {rmsdb(s):.1f} dBFS | voz estimada {rmsdb(g * vm):.1f} | resíduo (cena + erro) {rmsdb(res):.1f}")
no_reel = np.zeros_like(mix)
no_reel[t0 + d:t0 + d + n] = g * v
sf.write(os.path.join(A, "nar_rev5_no_reel.wav"), no_reel.astype(np.float32), sr, subtype="FLOAT")
print("ok")
