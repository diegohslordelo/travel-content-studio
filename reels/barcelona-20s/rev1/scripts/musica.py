"""Etapa 1, complemento do filtro 1 — música no áudio (o briefing pede zero música).

O Silero e o Whisper procuram fala; música de rua (violão, sax, canto) escapa dos dois.
Medida: periodicidade (pico da autocorrelação normalizada, 80–1000 Hz) em janelas de 64 ms,
na banda 150–3000 Hz. Ruído de rua, vento e passos ficam abaixo de 0,5; nota sustentada de
instrumento ou canto passa de 0,7. "Trecho musical" = ≥ 0,5 s seguidos com periodicidade ≥ 0,7.

Roda de dentro de reels/barcelona-20s. Saída: rev1/analise/musica.json
"""
import json
import os
import subprocess

import numpy as np
from scipy.signal import butter, sosfiltfilt

SR = 16000
JAN = int(0.064 * SR)
PASSO = int(0.032 * SR)
LIM = 0.7
MIN_S = 0.5


def periodicidade(x):
    sos = butter(4, [150, 3000], btype="band", fs=SR, output="sos")
    x = sosfiltfilt(sos, x)
    lmin, lmax = SR // 1000, SR // 80
    out = []
    for i in range(0, len(x) - JAN - lmax, PASSO):
        a = x[i:i + JAN + lmax]
        f0 = a[:JAN]
        e0 = np.dot(f0, f0)
        if e0 < 1e-8:
            out.append(0.0)
            continue
        best = 0.0
        for lag in range(lmin, lmax):
            f1 = a[lag:lag + JAN]
            r = np.dot(f0, f1) / np.sqrt(e0 * np.dot(f1, f1) + 1e-12)
            best = max(best, r)
        out.append(best)
    return np.array(out)


def trechos(p):
    t = np.arange(len(p)) * PASSO / SR
    on = p >= LIM
    res, ini = [], None
    for i, v in enumerate(np.append(on, False)):
        if v and ini is None:
            ini = i
        elif not v and ini is not None:
            if (i - ini) * PASSO / SR >= MIN_S:
                res.append([round(t[ini], 2), round(t[i - 1] + JAN / SR, 2)])
            ini = None
    return res


def main():
    res = {}
    for f in sorted(os.listdir("_tmp/wav")):
        b = os.path.splitext(f)[0]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"_tmp/wav/{f}", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        p = periodicidade(np.frombuffer(raw, np.float32).astype(np.float64))
        res[b] = {"mediana": round(float(np.median(p)), 3), "p90": round(float(np.percentile(p, 90)), 3),
                  "pct_acima": round(float((p >= LIM).mean() * 100), 1), "trechos_musicais": trechos(p),
                  "serie_32ms": [round(float(v), 2) for v in p]}
        print(b, {k: v for k, v in res[b].items() if k != "serie_32ms"}, flush=True)
    json.dump(res, open("rev1/analise/musica.json", "w"))


if __name__ == "__main__":
    main()
