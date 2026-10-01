"""Restauração dos agudos que a redução de ruído da rev. 4/5 tirou das falas.

Mede, nas falas que têm referência crua em revisões antigas, a curva de perda (rev. 5 / cru) por 1/3 de oitava,
monta um EQ de fase linear que desfaz essa perda só acima de 2 kHz e confere cruzando as cenas:
a curva de uma cena aplicada na outra tem que chegar perto do cru.
"""
import json
import sys

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
A = "../a"
CS = np.array([1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000])


def ler(arq):
    x, _ = sf.read(arq, always_2d=True)
    return x


def alinhar(ref, r0, r1, tst, t0, busca):
    bp = signal.butter(4, [300, 3000], "bandpass", fs=SR, output="sos")
    a = signal.sosfiltfilt(bp, ref[int(r0 * SR):int(r1 * SR)].mean(1))
    b0 = int((t0 - busca) * SR)
    b = signal.sosfiltfilt(bp, tst[b0:int((t0 + (r1 - r0) + busca) * SR)].mean(1))
    c = signal.correlate(b, a, mode="valid", method="fft")
    return b0 + int(np.argmax(np.abs(c)))  # amostra do teste que corresponde a r0


def bandas_voz(R, T, J=1024):
    """Diferença T-R (dB) por 1/3 de oitava nas janelas com voz, normalizada em 500-2000 Hz; e a mesma coisa em CS."""
    bp = signal.butter(4, [300, 3000], "bandpass", fs=SR, output="sos")
    nj = len(R) // J
    er = 20 * np.log10(np.sqrt((signal.sosfiltfilt(bp, R)[:nj * J].reshape(nj, J) ** 2).mean(1)) + 1e-10)
    voz = er > er.max() - 18
    f = np.fft.rfftfreq(J, 1 / SR)
    w = np.hanning(J)
    P = lambda x: (np.abs(np.fft.rfft(x[:nj * J].reshape(nj, J)[voz] * w, axis=1)) ** 2).mean(0)
    PR, PT = P(R), P(T)
    def b(Pp, cs):
        return np.array([10 * np.log10(Pp[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].mean()) for c in cs])
    ref_ = np.array([500, 630, 800, 1000, 1250, 1600, 2000])
    off = (b(PT, ref_) - b(PR, ref_)).mean()
    return b(PT, CS) - b(PR, CS) - off


def fir_restauro(perda_db, forca=1.0, taps=1023):
    """EQ de fase linear: ganho = -perda (só o que falta, entre 0 e +6 dB), 0 dB abaixo de 2 kHz."""
    g = np.clip(-perda_db * forca, 0, 6.0)
    g[CS < 2000] = 0
    fs_ = np.r_[0, 1500, CS[CS >= 2000], 20000, SR / 2]
    gs = np.r_[0, 0, g[CS >= 2000], g[-1], g[-1]]
    return signal.firwin2(taps, fs_ / (SR / 2), 10 ** (gs / 20))


def aplicar(x, h):
    return np.stack([signal.fftconvolve(x[:, c], h, mode="same") for c in range(x.shape[1])], 1)


if __name__ == "__main__":
    rev1, rev3, rev5 = ler(f"{A}/rev1.wav"), ler(f"{A}/rev3.wav"), ler(f"{A}/rev5.wav")
    casos = {
        "07": (rev1, 15.30, 16.85, 14.917, 0.3),
        "08": (rev3, 17.00, 19.55, 19.70, 0.3),
        "12": (rev1, 27.00, 30.20, 31.0, 1.5),
    }
    seg, perda = {}, {}
    for k, (ref, r0, r1, t0, busca) in casos.items():
        i = alinhar(ref, r0, r1, rev5, t0, busca)
        R = ref[int(r0 * SR):int(r1 * SR)]
        T = rev5[i:i + len(R)]
        seg[k] = (R, T)
        perda[k] = bandas_voz(R.mean(1), T.mean(1))
        print(f"perda {k}: " + " ".join(f"{c}:{v:+.1f}" for c, v in zip(CS, perda[k])))
    print("\nvalidação cruzada (curva de uma cena aplicada na outra; resto em relação ao cru, ideal = 0):")
    for fonte in perda:
        h = fir_restauro(perda[fonte])
        for alvo in perda:
            R, T = seg[alvo]
            d = bandas_voz(R.mean(1), aplicar(T, h).mean(1))
            print(f"  curva {fonte} em {alvo}: resto " + " ".join(f"{v:+.1f}" for v in d) + f"  | máx |resto| acima de 3 kHz: {np.abs(d[CS >= 3150]).max():.1f} dB")
    media = np.mean([perda["07"], perda["08"]], 0)
    json.dump({"CS": CS.tolist(), "perda": {k: v.tolist() for k, v in perda.items()}, "media_07_08": media.tolist()},
              open("perdas_falas.json", "w"), indent=1)
    h = fir_restauro(media)
    print("\ncurva média (07+08):", " ".join(f"{c}:{v:+.1f}" for c, v in zip(CS, media)))
    for alvo in perda:
        R, T = seg[alvo]
        d = bandas_voz(R.mean(1), aplicar(T, h).mean(1))
        print(f"  média em {alvo}: resto " + " ".join(f"{v:+.1f}" for v in d))
