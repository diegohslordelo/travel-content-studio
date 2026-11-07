"""Acha onde uma faixa de música (arquivo limpo) toca dentro de um áudio (export do CapCut), e em que ponto da faixa.

Para cada janela de 4 s do áudio (passo 0,5 s), correlação cruzada normalizada (8 kHz, mono) contra a faixa inteira:
devolve, por janela, o melhor deslocamento (tempo na faixa) e a correlação. Uma janela "tem a faixa" quando a
correlação passa do limiar; janelas seguidas com o mesmo mapeamento (tempo na faixa − tempo no áudio constante)
viram blocos. Mede também o ganho da faixa no áudio (regressão por bloco).

  python scripts/achar_musica.py <audio.wav> <faixa.wav> <saida.json>
"""
import json
import sys

import numpy as np
import soundfile as sf
from scipy import signal

SR = 8000
JAN = 4.0
PASSO = 0.5


def carrega(arq):
    x, sr = sf.read(arq, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    return signal.resample_poly(x, SR, sr).astype(np.float32)


def main():
    arq, faixa, saida = sys.argv[1:4]
    a, f = carrega(arq), carrega(faixa)
    # passa-altas leve: tira grave de vento/rua, que domina a energia e não é da música
    sos = signal.butter(2, 150, btype="highpass", fs=SR, output="sos")
    a, f = signal.sosfilt(sos, a).astype(np.float32), signal.sosfilt(sos, f).astype(np.float32)
    n = int(JAN * SR)
    nfft = 1 << int(np.ceil(np.log2(len(f) + n)))
    F = np.fft.rfft(f, nfft)
    e = np.concatenate([[0.0], np.cumsum(f.astype(np.float64) ** 2)])
    en_local = np.sqrt(np.maximum(e[n:] - e[:-n], 1e-12))  # energia da faixa em cada deslocamento
    res = []
    for i in range(0, len(a) - n, int(PASSO * SR)):
        w = a[i:i + n]
        nw = float(np.linalg.norm(w))
        if nw < 1e-4:
            res.append((i / SR, None, 0.0))
            continue
        c = np.fft.irfft(F * np.conj(np.fft.rfft(w, nfft)), nfft)[: len(f) - n + 1]
        ncc = c / (nw * en_local[: len(c)])
        k = int(np.argmax(ncc))
        res.append((i / SR, k / SR, float(ncc[k])))
    json.dump({"janela_s": JAN, "passo_s": PASSO, "janelas": [{"t": round(t, 2), "faixa_t": None if k is None else round(k, 3), "ncc": round(r, 3)} for t, k, r in res]},
              open(saida, "w"))
    # resumo: blocos com ncc > 0,3 e deslocamento constante (±40 ms)
    blocos = []
    for t, k, r in res:
        if k is None or r < 0.3:
            continue
        off = k - t
        if blocos and abs(off - blocos[-1]["off"]) < 0.04 and t - blocos[-1]["ate"] <= 2.0:
            blocos[-1]["ate"] = t + JAN
            blocos[-1]["ncc"].append(r)
        else:
            blocos.append({"de": t, "ate": t + JAN, "off": off, "ncc": [r]})
    for b in blocos:
        if b["ate"] - b["de"] >= 6:
            print(f"  {b['de']:7.1f}–{b['ate']:7.1f} s  faixa {b['de'] + b['off']:6.1f}–{b['ate'] + b['off']:6.1f} s  ncc mediana {np.median(b['ncc']):.2f}")


if __name__ == "__main__":
    main()
