#!/usr/bin/env python3
"""Versão com trilha do Reel de Socotra REV2: "Echoes of Time v2" (Kevin MacLeod, incompetech.com, CC BY 4.0) sob a voz.

A trilha entra na palavra "real" (onde o drone de ficção corta), usa o trecho 12–51 s da faixa (crescendo sem picos) e fica
18 dB abaixo da voz (docs/REFERENCIA_EDICAO_FORMATOS.md, 4.1: música −18 dB sob a fala), com fade de 1,2 s no fim.
Mixa sobre o áudio do render (voz + efeitos + clack) e refaz o master (−14 LUFS, pico ≤ −1 dBTP). Ninguém ouviu: escuta do Diego.

Uso (de dentro de reels/socotra/rev2/, depois de reel.py render e master): python3 scripts/trilha.py
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "scripts"))
import reel as R  # noqa: E402

MUSICA = os.path.join(AQUI, "musica", "echoes_of_time_v2.mp3")
TRECHO_INI, REL_DB, FADE_IN, FADE_OUT = 12.0, -18.0, 0.4, 1.2


def main():
    with open(os.path.join(R.TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    entra = p["gancho"][-1]["tempos"][-1]  # "real"
    total = p["quadros"] / p["fps"]
    dur = total - entra
    trecho = os.path.join(R.TMP, "trilha_trecho.wav")
    R.sh(["ffmpeg", "-v", "error", "-y", "-ss", str(TRECHO_INI), "-t", f"{dur:.3f}", "-i", MUSICA, "-ac", "2", "-ar", "48000",
          "-af", f"afade=t=in:d={FADE_IN},afade=t=out:st={dur - FADE_OUT:.3f}:d={FADE_OUT}", "-c:a", "pcm_s24le", trecho])
    lufs, _ = R.medir(trecho)
    voz = p["mix"]["voz_lufs"]
    ganho = voz + REL_DB - lufs
    mix = os.path.join(R.TMP, "reel_com_trilha_sem_master.mov")
    R.sh(["ffmpeg", "-v", "error", "-y", "-i", R.SAIDA_BRUTA, "-i", trecho, "-filter_complex",
          f"[1:a]volume={ganho:.2f}dB,adelay={round(entra * 1000)}|{round(entra * 1000)}[m];[0:a][m]amix=inputs=2:normalize=0:duration=first[a]",
          "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "pcm_s24le", mix])
    master = os.path.join(R.TMP, "reel_com_trilha_master.mov")
    i0, i, tp, g = R.loudness(mix, master, -14.0, -1.0, video=True)
    saida = os.path.join(AQUI, "reel_socotra_rev2_com_trilha.mp4")
    R.sh(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AQUI, "reel_socotra_rev2.mp4"), "-i", master, "-map", "0:v", "-map", "1:a",
          "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", saida])
    i2, tp2 = R.medir(saida)
    print(f"trilha: {lufs:.1f} LUFS no trecho, ganho {ganho:+.1f} dB (voz {voz} LUFS, {REL_DB} dB) · entra em {entra:.2f} s")
    print(f"master com trilha: {i2:.1f} LUFS · pico verdadeiro {tp2:.1f} dBTP → {os.path.basename(saida)}")


if __name__ == "__main__":
    main()
