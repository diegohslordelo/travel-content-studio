"""Voz × música da REV3: em cada trecho com fala (janelas de 400 ms, passo de 100 ms), quantos dB a voz fica acima
da música, medidos nas trilhas separadas (antes do master; nível com ênfase nos agudos, como a percepção).
Roda de reels/bru-yt depois de `rev3/mixar_rev3.py`:  python rev3/medir_voz_musica_rev3.py  →  _tmp/voz_musica_rev3.json"""
import json

import numpy as np
from scipy import signal

SR = 48000
z = np.load("_tmp/vm_rev3.npz")
lt = json.load(open("rev3/linha_do_tempo_rev3.json"))
fala = np.load("_tmp/fala_rev3.npy")


def kw(x):
    b, a = signal.butter(2, 1500 / (SR / 2), "high")
    x1 = signal.lfilter(b, a, x) * 0.5 + x * 0.5
    b2, a2 = signal.butter(2, 38 / (SR / 2), "high")
    return signal.lfilter(b2, a2, x1)


Vk, Mk = kw(z["V"].mean(1)), kw(z["M"].mean(1))
W, H = int(0.4 * SR), int(0.1 * SR)
G, C, F = lt["gancho_ms"], lt["corpo_fim_ms"], lt["fechamento_fim_ms"]
h0, h1 = lt["hotel_ms"]
reg = {"gancho": (0, G), "corpo (sem o hotel)": (G, C), "hotel (H1)": (h0, h1), "fechamento": (C, F)}
rel = {}
for nome, (a, b) in reg.items():
    d = []
    for i in range(int(a * SR / 1000), int(b * SR / 1000) - W, H):
        if nome.startswith("corpo") and h0 - 500 <= i * 1000 / SR <= h1 + 500:
            continue
        if fala[int(i / SR * 100):int((i + W) / SR * 100)].mean() > 0.8:
            lv = 10 * np.log10(np.mean(Vk[i:i + W] ** 2) + 1e-12)
            lm = 10 * np.log10(np.mean(Mk[i:i + W] ** 2) + 1e-12)
            if lv > -60:
                d.append(lv - lm)
    d = np.array(d)
    rel[nome] = {"janelas_com_fala": int(len(d)), "mediana_db": round(float(np.median(d)), 1), "p10_db": round(float(np.percentile(d, 10)), 1), "abaixo_de_6db_pct": round(float(np.mean(d < 6) * 100), 1)}
    print(nome, rel[nome])
json.dump(rel, open("_tmp/voz_musica_rev3.json", "w"), ensure_ascii=False, indent=1)
