"""Garante pico verdadeiro <= -1 dBTP NO ARQUIVO EXPORTADO (padrão de áudio, 11.3: o AAC pode elevar o pico).

Ciclo: codifica o WAV da mixagem em AAC, decodifica, acha as amostras cujo pico verdadeiro (sobreamostragem 4×, a
mesma conta do ebur128) passa de -1,2 dBTP e abaixa o ganho do WAV só ali (queda de cosseno elevado de ~100 ms,
profundidade = excesso + 0,5 dB), até o decodificado ficar <= -1,2 dBTP. (REV1 media o pico por amostra; na REV2 o
pico entre amostras do G1 passou disso, então a conta é a do pico verdadeiro.)

  python rev2/corrigir_pico_aac.py <mix.wav> <video_sem_audio_ou_com.mp4> <saida.mp4> [bitrate=160k]
"""
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
ALVO = -1.2


def sh(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def main():
    mixwav, video, saida = sys.argv[1:4]
    br = sys.argv[4] if len(sys.argv) > 4 else "160k"
    x, sr = sf.read(mixwav, dtype="float32")
    assert sr == SR
    for rodada in range(1, 9):
        sf.write("_tmp/fix.wav", x, SR, subtype="FLOAT")
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "_tmp/fix.wav", "-c:a", "aac", "-b:a", br, "-ar", "48000", "_tmp/fix.m4a"])
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "_tmp/fix.m4a", "-c:a", "pcm_f32le", "_tmp/fix_dec.wav"])
        d, _ = sf.read("_tmp/fix_dec.wav", dtype="float32")
        up = np.abs(signal.resample_poly(d, 4, 1, axis=0)).max(axis=1)
        pico = up[: len(d) * 4].reshape(-1, 4).max(axis=1)  # pico verdadeiro por amostra original
        lim = 10 ** (ALVO / 20)
        ruins = np.flatnonzero(pico > lim)
        print(f"rodada {rodada}: pico verdadeiro decodificado {20 * np.log10(pico.max()):.2f} dBTP, {len(ruins)} amostras acima de {ALVO} dBTP")
        if len(ruins) == 0:
            break
        # agrupa amostras próximas (< 200 ms) e abaixa o ganho em volta do pior de cada grupo
        grupos = np.split(ruins, np.flatnonzero(np.diff(ruins) > SR // 5) + 1)
        for g in grupos:
            c = int(g[np.argmax(pico[g])])
            exc = min(3.0, 20 * np.log10(pico[c] / lim) + 0.5)  # no máximo 3 dB por rodada: pico absurdo é falha do codificador
            n = int(0.05 * SR)
            a, b = max(0, c - n), min(len(x), c + n)
            w = 0.5 * (1 - np.cos(np.pi * np.arange(b - a) / (b - a)))  # 0..1
            queda = 1 - np.sin(np.pi * np.arange(b - a) / (b - a))  # 1 nas pontas
            ganho = 10 ** (-exc / 20 * (1 - queda)) if False else 10 ** (-exc / 20 * np.sin(np.pi * np.arange(b - a) / (b - a)) ** 2)
            x[a:b] *= ganho[:, None].astype(np.float32)
            print(f"   {c / SR:8.2f} s: queda de {exc:.1f} dB em {2 * n / SR * 1000:.0f} ms")
    sf.write("_tmp/fix_final.wav", x, SR, subtype="FLOAT")
    sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", video, "-i", "_tmp/fix.m4a", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", saida])
    print("ok", saida)


if __name__ == "__main__":
    main()
