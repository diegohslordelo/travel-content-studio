"""Mede as 21 faixas candidatas (Biblioteca de áudio do YouTube, baixadas pelo Claude no Chrome a pedido do Diego,
20/11/2026; Drive Bruges/Youtube/Música) para escolher uma por seção. O Claude não escuta: a escolha é por medição
(andamento, energia, introdução, brilho) + o clima pedido no prompt; a aprovação é do ouvido do Diego.

Roda de reels/bruges-yt:  python -I rev2/analisar_musicas_rev2.py  →  rev2/musicas_medidas_rev2.json
"""
import json
import os

import librosa
import numpy as np

PASTA = "fonte/musica"
# seção de cada candidata: a ordem em que o Claude no Chrome baixou (hora do arquivo no Drive), 3 por seção, na ordem
# do prompt (G, M1, M2, M3, M4, M5, F)
SECAO = {
    "G": ["Scale The Mountain - Density & Time", "Bright Skies - Audio Hertz", "Taking Flight - Blue Deer Studio"],
    "M1": ["Top Of The Morning - TrackTribe", "No.3 Morning Folk Song - Esther Abrami", "Clouds Lifting - Telecasted"],
    "M2": ["Powdered Waltz - The Mini Vandals", "Panoramic Arrival - Asher Fulero", "Ripples In Time - Asher Fulero"],
    "M3": ["Fine Dining - TrackTribe", "Strollin' - TrackTribe", "Swing Haven 1 - Los Angeles - Reed Mathis"],
    "M4": ["Starlight on the Water - Chris Haugen", "The Swan - The Soundlings", "The Palace Gardens - Asher Fulero"],
    "M5": ["Bop Walker - Freedom Trail Studio", "Squirm Worm - TrackTribe", "Peaked My Interest - Nathan Moore"],
    "F": ["Dusty Road Magic - Chris Haugen", "Lily's Song - TrackTribe", "Spring Migration - The Great North Sound Society"],
}


def mede(caminho):
    y, sr = librosa.load(caminho, sr=22050, mono=True)
    dur = len(y) / sr
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
    db = 20 * np.log10(rms + 1e-9)
    por_s = np.array([db[(t >= s) & (t < s + 1)].mean() for s in range(int(dur))])
    med = np.median(por_s)
    intro = next((s for s, v in enumerate(por_s) if v >= med - 6), 0)  # s até chegar perto do nível típico
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    dens = len(librosa.onset.onset_detect(onset_envelope=onset, sr=sr)) / dur
    cent = float(np.median(librosa.feature.spectral_centroid(y=y, sr=sr)[0]))
    corpo = por_s[intro:]
    var = float(np.std(corpo - np.convolve(corpo, np.ones(9) / 9, mode="same")[: len(corpo)])) if len(corpo) > 10 else 0.0
    sub30 = float(por_s[min(25, len(por_s) - 1)] - por_s[min(3, len(por_s) - 1)])  # quanto sobe nos primeiros 30 s
    return {
        "duracao_s": round(dur, 1),
        "bpm": round(float(np.atleast_1d(tempo)[0]), 1),
        "intro_s": int(intro),
        "nivel_mediano_db": round(float(med), 1),
        "faixa_dinamica_db": round(float(np.percentile(por_s, 95) - np.percentile(por_s, 10)), 1),
        "instabilidade_db": round(var, 2),
        "subida_3_25s_db": round(sub30, 1),
        "ataques_por_s": round(dens, 2),
        "brilho_hz": round(cent),
        "curva_db_por_s": [round(float(v), 1) for v in por_s],
        "batidas_s": [round(float(b), 3) for b in librosa.frames_to_time(beats, sr=sr)],
    }


def main():
    out = {}
    for sec, nomes in SECAO.items():
        for n in nomes:
            m = mede(os.path.join(PASTA, n + ".mp3"))
            m["secao"] = sec
            out[n] = m
            print(f"{sec:>2}  {n:<52} {m['duracao_s']:6.1f}s  {m['bpm']:6.1f} BPM  intro {m['intro_s']:3d}s  "
                  f"din {m['faixa_dinamica_db']:5.1f}  instab {m['instabilidade_db']:4.2f}  sobe {m['subida_3_25s_db']:5.1f}  "
                  f"ataques {m['ataques_por_s']:4.2f}/s  brilho {m['brilho_hz']:5d} Hz", flush=True)
    json.dump(out, open("rev2/musicas_medidas_rev2.json", "w", encoding="utf-8"), ensure_ascii=False)


if __name__ == "__main__":
    main()
