"""Mede onde a voz começa e termina em cada tomada (energia 120–4.000 Hz, janelas de 10 ms) e lista as pausas.
Uso (de dentro de reels/darvaza-cratera/): python3 scripts/segmentar.py  → _tmp/segmentos.json"""
import subprocess, json, sys
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
TOMADAS = ["IMG_7537", "IMG_7540", "IMG_7541", "IMG_7542", "IMG_7543", "IMG_7547", "IMG_7546"]
sos = butter(4, [120, 4000], btype="band", fs=SR, output="sos")
W = json.load(open("_tmp/words_large-v3.json"))
out = {}
for f in TOMADAS:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/{f}.mov", "-map", "0:a:0", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True)
    x = np.frombuffer(r.stdout, dtype=np.float32).astype(float)
    y = sosfilt(sos, x); n = 480
    db = np.array([20 * np.log10(np.sqrt(np.mean(y[i:i + n] ** 2)) + 1e-9) for i in range(0, len(y) - n, n)])
    floor = float(np.percentile(db[db > -100], 10)); thr = floor + 15
    sp = db > thr
    segs = []; i = 0
    while i < len(sp):
        if sp[i]:
            j = i
            while j < len(sp) and sp[j]: j += 1
            segs.append([i / 100, j / 100]); i = j
        else: i += 1
    m = []
    for s in segs:
        if m and s[0] - m[-1][1] < 0.08: m[-1][1] = s[1]
        else: m.append(s)
    m = [s for s in m if s[1] - s[0] > 0.04]
    out[f] = {"dur": len(x) / SR, "piso_db": floor, "segs": m, "db10ms": [round(v, 1) for v in db]}
    print(f, f"dur {len(x)/SR:.2f} piso {floor:.0f}")
    print("  segs:", " ".join(f"{a:.2f}-{b:.2f}" for a, b in m))
    print("  words:", " ".join(f"{w[2].strip()}@{w[0]:.2f}-{w[1]:.2f}" for w in W[f]))
json.dump(out, open("_tmp/segmentos.json", "w"))
