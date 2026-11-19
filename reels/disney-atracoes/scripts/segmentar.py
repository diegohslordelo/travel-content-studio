"""Acha os trechos com voz em cada bloco gravado (energia na faixa 120–4.000 Hz, janelas de 10 ms) e as pausas internas.
Serve para escrever edicao.json (entrada, saída e cortes de pausa no silêncio).
Uso (de dentro de reels/disney-atracoes/): python3 scripts/segmentar.py
Saída: _tmp/segmentos.json e um resumo por bloco"""
import glob, json, os, subprocess
import numpy as np
from scipy.signal import butter, sosfiltfilt

SR = 48000
H = int(0.01 * SR)


def le(f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, dtype=np.float32).astype(np.float64)


R = {}
for f in sorted(glob.glob("fonte/voz/voz_*.m4a")):
    nm = os.path.basename(f)[:-4]
    x = le(f)
    y = sosfiltfilt(butter(4, [120, 4000], "bandpass", fs=SR, output="sos"), x)
    n = len(y) // H
    e = 10 * np.log10(np.mean(y[:n * H].reshape(n, H) ** 2, axis=1) + 1e-12)
    pico = np.percentile(e, 98)
    piso = np.percentile(e, 10)
    lim = max(piso + 10, pico - 38)
    voz = e > lim
    # fecha buracos < 80 ms (oclusivas) e tira ilhas < 60 ms (estalos)
    def fecha(v, k, val):
        v = v.copy(); i = 0
        while i < len(v):
            if v[i] == (not val):
                j = i
                while j < len(v) and v[j] == (not val): j += 1
                if j - i < k and i > 0 and j < len(v): v[i:j] = val
                i = j
            else:
                i += 1
        return v
    voz = fecha(voz, 8, True)
    voz = fecha(voz, 6, False)
    seg, i = [], 0
    while i < n:
        if voz[i]:
            j = i
            while j < n and voz[j]: j += 1
            seg.append([round(i * 0.01, 2), round(j * 0.01, 2)])
            i = j
        else:
            i += 1
    R[nm] = {"dur": round(len(x) / SR, 3), "piso_db": round(piso, 1), "pico_db": round(pico, 1), "limiar_db": round(lim, 1), "segmentos": seg,
             "pausas": [[seg[k][1], seg[k + 1][0], round(seg[k + 1][0] - seg[k][1], 2)] for k in range(len(seg) - 1)]}
    fala = sum(b - a for a, b in seg)
    print(f"{nm} dur {R[nm]['dur']:.2f} fala {seg[0][0]:.2f}–{seg[-1][1]:.2f} ({fala:.2f} s de voz) piso {piso:.0f} dB pico {pico:.0f} dB · pausas>0.15: "
          + ", ".join(f"{a:.2f}+{d:.2f}" for a, b, d in R[nm]["pausas"] if d > 0.15))
os.makedirs("_tmp", exist_ok=True)
json.dump(R, open("_tmp/segmentos.json", "w"), indent=0)
