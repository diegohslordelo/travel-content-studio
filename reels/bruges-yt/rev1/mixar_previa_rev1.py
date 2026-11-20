"""Som da prévia da REV1 (vlog de Bruges): voz da fonte nos trechos mantidos da decupagem (com rampas de 12 ms em cada
emenda), a fala da Marina no gancho, os efeitos do render (Recibo, Placa, mapa, like…) e o `keen` no fim do gancho.
SEM música (as faixas da Biblioteca de áudio do YouTube ainda não foram escolhidas) e sem as narrações (a gravar).
Não é a mixagem final (essa segue o docs/AUDIO_REVIEW_STANDARD.md): só nivela a fala em −20 LUFS e o todo em −16 LUFS.

Roda de reels/bruges-yt:  python -I rev1/mixar_previa_rev1.py --sfx <efeitos.wav> --saida <mix.wav>
"""
import argparse
import json

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

SR = 48000
KEEN = "../../design-system/sons/externos/keen.wav"
KEEN_PICO = 0.96


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sfx", required=True)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()
    lt = json.load(open("rev1/linha_do_tempo_rev1.json", encoding="utf-8"))
    voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32", always_2d=True)
    assert sr == SR
    n = int(round(lt["duracao_ms"] / 1000 * SR))
    out = np.zeros((n, 2), dtype=np.float32)
    r = int(0.012 * SR)
    for p in lt["audio"]:
        i0 = int(round(p["src"] / 1000 * SR))
        o0 = int(round(p["out"] / 1000 * SR))
        m = int(round(p["dur"] / 1000 * SR))
        m = min(m, n - o0, len(voz) - i0)
        if m <= 2 * r:
            continue
        x = voz[i0:i0 + m].copy()
        x[:r] *= np.linspace(0, 1, r)[:, None]
        x[-r:] *= np.linspace(1, 0, r)[:, None]
        out[o0:o0 + m] += x
    med = pyln.Meter(SR)
    out *= 10 ** ((-20.0 - med.integrated_loudness(out)) / 20)
    k, ksr = sf.read(KEEN, dtype="float32", always_2d=True)
    if ksr != SR:
        idx = np.arange(0, len(k), ksr / SR)
        k = np.stack([np.interp(idx, np.arange(len(k)), k[:, c]) for c in range(k.shape[1])], axis=1).astype(np.float32)
    if k.shape[1] == 1:
        k = np.repeat(k, 2, axis=1)
    k *= 10 ** ((-26.0 - med.integrated_loudness(k)) / 20)  # −6 dB da voz
    i0 = int(round((lt["keen_ms"] / 1000 - KEEN_PICO) * SR))
    out[i0:i0 + len(k)] += k[: n - i0]
    s, _ = sf.read(a.sfx, dtype="float32", always_2d=True)
    m = min(len(s), n)
    out[:m] += s[:m]
    out *= 10 ** ((-16.0 - med.integrated_loudness(out)) / 20)
    pico = np.abs(out).max()
    if pico > 0.89:
        out *= 0.89 / pico
    sf.write(a.saida, out, SR, subtype="FLOAT")
    print("ok", a.saida, f"{n / SR:.1f} s")


if __name__ == "__main__":
    main()
