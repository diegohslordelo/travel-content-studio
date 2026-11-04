"""Envelope de energia da voz (120–4000 Hz) por tomada e silêncios internos. Uso: python3 scripts/energia.py"""
import json, subprocess, numpy as np
SR = 16000
TOMADAS = ["IMG_7694", "IMG_7695", "IMG_7696", "IMG_7713", "IMG_7720", "IMG_7722", "IMG_7728", "IMG_7733", "IMG_7734"]

def env(take):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/{take}.MOV", "-vn", "-ac", "1", "-ar", str(SR),
                          "-af", "highpass=f=120,lowpass=f=4000", "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    hop = SR // 100
    n = len(a) // hop
    rms = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(rms), len(a) / SR

def silencios(db, limiar, minimo=0.12):
    s = db < limiar
    out, i = [], 0
    while i < len(s):
        if s[i]:
            j = i
            while j < len(s) and s[j]:
                j += 1
            if (j - i) / 100 >= minimo:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out

if __name__ == "__main__":
    res = {}
    for t in TOMADAS:
        db, dur = env(t)
        fala = np.percentile(db, 90)
        lim = fala - 28
        sil = silencios(db, lim)
        res[t] = {"dur": dur, "fala_db": float(fala), "limiar": float(lim), "silencios": sil}
        print(t, f"dur {dur:.2f} fala {fala:.1f} dB lim {lim:.1f}", " ".join(f"[{a:.2f}-{b:.2f}]" for a, b in sil))
    json.dump(res, open("_tmp/energia.json", "w"), indent=1)
