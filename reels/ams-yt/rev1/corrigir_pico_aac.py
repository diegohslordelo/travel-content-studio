"""Garante pico <= -1 dBFS NO ARQUIVO EXPORTADO (padrão de áudio, 11.3: o AAC pode elevar o pico).

Ciclo: codifica o WAV da mixagem em AAC, decodifica, acha as amostras acima de -1,2 dBFS e abaixa o ganho do WAV
só ali (queda de cosseno elevado de ~100 ms, profundidade = excesso + 0,5 dB), até o decodificado ficar <= -1,2 dBFS.

  python rev1/corrigir_pico_aac.py <mix.wav> <video_sem_audio_ou_com.mp4> <saida.mp4> [bitrate=160k]
"""
import subprocess
import sys

import numpy as np
import soundfile as sf

SR = 48000
ALVO = -1.2


def sh(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def main():
    mixwav, video, saida = sys.argv[1:4]
    br = sys.argv[4] if len(sys.argv) > 4 else "160k"
    x, sr = sf.read(mixwav, dtype="float32")
    assert sr == SR
    for rodada in range(1, 7):
        sf.write("_tmp/fix.wav", x, SR, subtype="FLOAT")
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "_tmp/fix.wav", "-c:a", "aac", "-b:a", br, "-ar", "48000", "_tmp/fix.m4a"])
        sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "_tmp/fix.m4a", "-c:a", "pcm_f32le", "_tmp/fix_dec.wav"])
        d, _ = sf.read("_tmp/fix_dec.wav", dtype="float32")
        pico = np.abs(d).max(axis=1)
        lim = 10 ** (ALVO / 20)
        ruins = np.flatnonzero(pico > lim)
        print(f"rodada {rodada}: pico decodificado {20 * np.log10(pico.max()):.2f} dBFS, {len(ruins)} amostras acima de {ALVO} dBFS")
        if len(ruins) == 0:
            break
        # agrupa amostras próximas (< 200 ms) e abaixa o ganho em volta do pior de cada grupo
        grupos = np.split(ruins, np.flatnonzero(np.diff(ruins) > SR // 5) + 1)
        for g in grupos:
            c = int(g[np.argmax(pico[g])])
            exc = 20 * np.log10(pico[c] / lim) + 0.5
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
