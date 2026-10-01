"""Sincronia voz x boca: abertura da boca (FaceMesh, lábios internos 13-14 / altura do rosto 10-152) quadro a quadro
contra o envelope da voz (300-3000 Hz) no mesmo quadro. Defasagem positiva = som adiantado em relação à imagem.

Uso: python3 sincronia_boca.py video.mp4 audio.wav ini:fim:nome [...]
"""
import subprocess
import sys

import mediapipe as mp
import numpy as np
import soundfile as sf
from scipy import signal

FPS = 24
W, H = 540, 960
video, audio = sys.argv[1], sys.argv[2]
x, sr = sf.read(audio, always_2d=True)
v = signal.sosfiltfilt(signal.butter(4, [300, 3000], "bandpass", fs=sr, output="sos"), x.mean(1))
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True,
                                     min_detection_confidence=0.4, min_tracking_confidence=0.4)
for item in sys.argv[3:]:
    a, b, nome = item.split(":")
    a, b = float(a), float(b)
    f0, f1 = round(a * FPS), round(b * FPS)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf",
                          f"select='between(n\\,{f0}\\,{f1 - 1})',scale={W}:{H},format=rgb24", "-vsync", "0",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    ab = []
    for f in fr:
        r = fm.process(f)
        if not r.multi_face_landmarks:
            ab.append(np.nan)
            continue
        lm = r.multi_face_landmarks[0].landmark
        p = lambda i: np.array([lm[i].x * W, lm[i].y * H])
        ab.append(np.linalg.norm(p(13) - p(14)) / np.linalg.norm(p(10) - p(152)))
    ab = np.array(ab)
    J = sr // FPS
    env = np.array([np.sqrt(np.mean(v[(f0 + k) * J:(f0 + k + 1) * J] ** 2)) for k in range(len(ab))])
    env = 20 * np.log10(env + 1e-9)
    ok = ~np.isnan(ab)
    print(f"{nome}: quadros {f0}-{f1 - 1}, rosto em {ok.sum()}/{len(ab)}")
    if ok.sum() < 12:
        continue
    abz = np.where(ok, ab, np.nanmedian(ab))
    res = []
    for L in range(-8, 9):
        # L > 0: a boca no quadro i+L corresponde ao som do quadro i (som adiantado)
        i0, i1 = max(0, -L), min(len(ab), len(ab) - L)
        m = ok[i0 + L:i1 + L] if L >= 0 else ok[i0 + L:i1 + L]
        aa = abz[i0 + L:i1 + L][m]
        ee = env[i0:i1][m]
        if len(aa) > 8:
            res.append((L, float(np.corrcoef(aa, ee)[0, 1])))
    best = max(res, key=lambda r: r[1])
    print("  correlação por defasagem (quadros): " + " ".join(f"{L:+d}:{c:.2f}" for L, c in res))
    print(f"  melhor: {best[0]:+d} quadro(s) ({best[0] / FPS * 1000:+.0f} ms), corr {best[1]:.2f}")
    print("  abertura da boca:", " ".join("--" if np.isnan(q) else f"{q * 100:.0f}" for q in ab))
    print("  voz (dB):         ", " ".join(f"{e:.0f}" for e in env))
