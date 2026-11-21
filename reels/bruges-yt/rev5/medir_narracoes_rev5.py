"""Medição das narrações gravadas pelo Diego (vlog de Bruges, REV5): onde a fala começa e termina em cada arquivo, pausas
internas, loudness da fala, pico, piso de ruído fora da fala e peso dos graves. Medição, não escuta.

Roda de reels/bruges-yt, depois de converter os arquivos (fonte/narracao/*.m4a → _tmp/narr/<id>.48k.wav, mono 48 kHz):
    python -I rev5/medir_narracoes_rev5.py
Escreve dados/narracao_fala.json (lido por rev5/roteiro_rev5.py e rev5/mixar_rev5.py).

Arquivos (Drive, Bruges/Youtube, 21/11/2026; IDs em dados/narracao_ids_drive.tsv, SHA-256 em dados/sha256_narracao.txt):
P1–P5 = gancho (gravados juntos, estéreo), R1–R8 = fechamento (mono). A frase do hotel (F5 do roteiro) o Diego não gravou
("eu tirei a parte dos custos da hospedagem da narração").

Início/fim da fala: energia na banda da voz (150–4000 Hz) em janelas de 10 ms, limiar = o maior entre piso + 12 dB e
o topo (percentil 95) − 30 dB. (O Whisper põe a 1ª palavra em 0,00 s, por isso o tempo da fala sai da energia; o tempo
das palavras do meio sai do Whisper: dados/transcricao_narracoes.json.)
"""
import glob
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000


def main():
    med = pyln.Meter(SR)
    bp = signal.butter(4, [150, 4000], btype="band", fs=SR, output="sos")
    out = {}
    for f in sorted(glob.glob("_tmp/narr/*.48k.wav")):
        k = os.path.basename(f).split(".")[0]
        x, sr = sf.read(f, dtype="float32")
        assert sr == SR and x.ndim == 1
        y = signal.sosfiltfilt(bp, x)
        hop = SR // 100
        e = np.array([20 * np.log10(np.sqrt(np.mean(y[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(y) - hop, hop)])
        thr = max(np.percentile(e, 8) + 12, np.percentile(e, 95) - 30)
        on = e > thr
        idx = np.flatnonzero(on)
        ini, fim = idx[0] / 100, (idx[-1] + 1) / 100
        pausas, k0 = [], None
        for i in range(idx[0], idx[-1] + 1):
            if not on[i]:
                k0 = i if k0 is None else k0
            else:
                if k0 is not None and i - k0 >= 20:
                    pausas.append([round(k0 / 100, 2), round((i - k0) / 100, 2)])
                k0 = None
        fala = x[int(ini * SR):int(fim * SR)]
        fora = np.concatenate([x[:max(int((ini - 0.05) * SR), 0)], x[int((fim + 0.1) * SR):]])
        fw, P = signal.welch(fala, SR, nperseg=4096)
        out[k] = {"dur_s": round(len(x) / SR, 3), "fala_ini_s": float(ini), "fala_fim_s": float(fim), "pausas_s": pausas,
                  "lufs_fala": round(float(med.integrated_loudness(fala)), 1), "pico_dbfs": round(float(20 * np.log10(np.abs(x).max())), 1),
                  "piso_dbfs": round(float(20 * np.log10(np.sqrt(np.mean(fora ** 2)) + 1e-9)), 1) if len(fora) > SR // 20 else None,
                  "graves_abaixo_100hz_db": round(float(10 * np.log10(P[fw < 100].sum() / P.sum())), 1)}
        print(k, out[k])
    json.dump(out, open("dados/narracao_fala.json", "w"), indent=1)


if __name__ == "__main__":
    main()
