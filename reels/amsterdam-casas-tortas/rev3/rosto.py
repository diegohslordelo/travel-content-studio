#!/usr/bin/env python3
"""Recorte 9:16 que segue o rosto do Diego (selfie andando): o rosto fica parado no quadro e o tremor da mão some.

1. Acha o rosto (Haar, OpenCV) e acompanha pontos dele quadro a quadro (fluxo óptico Lucas-Kanade);
   a cada 12 quadros a detecção corrige a deriva.
2. Suaviza a trajetória do rosto (média de 5 quadros, só para tirar o ruído da medida).
3. Recorta 1216 × 2160 (altura inteira, a mesma ampliação da rev1) com o rosto no centro horizontal.

uso: python3 rosto.py entrada.mp4 saida.mp4 [ini fim]   (entrada SDR já girada, 3840 × 2160)
"""
import subprocess
import sys

import cv2
import numpy as np

W, H, ALVO_Y = 1216, 2160, 0  # altura inteira, como na rev1; o rosto é seguido só na horizontal
ESC = 0.25  # escala da análise


def detectar(cinza, cascata, perto=None):
    rostos = cascata.detectMultiScale(cinza, 1.1, 6, minSize=(60, 60))
    if len(rostos) == 0:
        return None
    if perto is None:
        return max(rostos, key=lambda r: r[2] * r[3])
    return min(rostos, key=lambda r: abs(r[0] + r[2] / 2 - perto[0]) + abs(r[1] + r[3] / 2 - perto[1]))


def trajetoria(arq, ini, fim):
    cap = cv2.VideoCapture(arq)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_MSEC, ini * 1000)
    cascata = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    pts, ant, centro, traj = None, None, None, []
    n = 0
    while True:
        ok, q = cap.read()
        if not ok or (fim and n / fps > fim - ini):
            break
        cinza = cv2.cvtColor(cv2.resize(q, None, fx=ESC, fy=ESC, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        if pts is not None and len(pts) >= 8:
            novos, st, _ = cv2.calcOpticalFlowPyrLK(ant, cinza, pts, None, winSize=(21, 21), maxLevel=3)
            bons = st.ravel() == 1
            if bons.sum() >= 8:
                desl = np.median(novos[bons] - pts[bons], axis=0).ravel()
                centro = centro + desl
                pts = novos[bons].reshape(-1, 1, 2)
            else:
                pts = None
        if pts is None or n % 12 == 0:
            r = detectar(cinza, cascata, centro)
            if r is not None:
                c = np.array([r[0] + r[2] / 2, r[1] + r[3] / 2], float)
                centro = c if centro is None or pts is None else 0.7 * centro + 0.3 * c  # corrige a deriva sem pular
                masc = np.zeros_like(cinza)
                masc[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = 255
                pts = cv2.goodFeaturesToTrack(cinza, 80, 0.01, 4, mask=masc)
        traj.append(None if centro is None else centro / ESC)
        ant = cinza
        n += 1
    cap.release()
    # buracos (antes da primeira detecção) recebem o primeiro valor conhecido
    prim = next(t for t in traj if t is not None)
    traj = np.array([prim if t is None else t for t in traj])
    k = 9  # ~0,37 s: o recorte acompanha o rosto sem herdar a vibração da medida
    pad = np.pad(traj, ((k // 2, k // 2), (0, 0)), mode="edge")
    return np.stack([np.convolve(pad[:, j], np.ones(k) / k, mode="valid") for j in range(2)], axis=1), fps


def recortar(arq, saida, ini=0.0, fim=None):
    traj, fps = trajetoria(arq, ini, fim)
    cap = cv2.VideoCapture(arq)
    cap.set(cv2.CAP_PROP_POS_MSEC, ini * 1000)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", saida], stdin=subprocess.PIPE)
    for cx, cy in traj:
        ok, q = cap.read()
        if not ok:
            break
        h, w = q.shape[:2]
        x = int(round(min(max(cx - W / 2, 0), w - W)))
        y = int(round(min(max(cy - ALVO_Y, 0), h - H)))
        enc.stdin.write(np.ascontiguousarray(q[y:y + H, x:x + W]).tobytes())
    enc.stdin.close()
    enc.wait()
    np.save(saida + ".traj.npy", traj)
    print(f"{saida}: {len(traj)} quadros · rosto x {traj[:, 0].min():.0f}–{traj[:, 0].max():.0f} · y {traj[:, 1].min():.0f}–{traj[:, 1].max():.0f}")


if __name__ == "__main__":
    a = sys.argv[1:]
    recortar(a[0], a[1], float(a[2]) if len(a) > 2 else 0.0, float(a[3]) if len(a) > 3 else None)
