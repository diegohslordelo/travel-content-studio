"""Mede o rosto do Diego (Haar do OpenCV) a cada 5 quadros da gravação, para posicionar o recorte no tela verde
(cabeça abaixo do material de apoio e legenda abaixo do queixo). Imprime, por tomada, topo da cabeça e queixo (y em 1080 × 1920).
Roda de dentro de reels/disney-frozen/rev1:  python3 scripts/rosto.py"""
import json, os, subprocess
import cv2, numpy as np
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
arq = os.path.normpath(os.path.join(AQUI, ed["fonte_dir"], ed["fonte"]))
W, H = 270, 480
cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", arq, "-vf", f"select='not(mod(n\\,5))',scale={W}:{H}", "-vsync", "0",
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
out, n = [], 0
while True:
    b = p.stdout.read(W * H)
    if len(b) < W * H:
        break
    g = np.frombuffer(b, np.uint8).reshape(H, W)
    fs = cas.detectMultiScale(g, 1.1, 5, minSize=(40, 40))
    t = n * 5 / ed["fps"]
    if len(fs):
        x, y, w, h = max(fs, key=lambda f: f[2] * f[3])
        out.append({"t": round(t, 2), "x": int((x + w / 2) * 4), "topo": int(y * 4), "queixo": int((y + h) * 4), "w": int(w * 4)})
    n += 1
json.dump(out, open(os.path.join(AQUI, "_tmp", "rosto.json"), "w"), indent=0)
tomadas = ed.get("tomadas", [[0, 99]])
for a, b in tomadas:
    s = [o for o in out if a <= o["t"] < b]
    if s:
        tp = np.array([o["topo"] for o in s]); qx = np.array([o["queixo"] for o in s]); cx = np.array([o["x"] for o in s])
        print(f"{a:6.2f}–{b:6.2f}: {len(s):3d} med · topo p10 {np.percentile(tp,10):.0f} med {np.median(tp):.0f} · queixo med {np.median(qx):.0f} p90 {np.percentile(qx,90):.0f} max {qx.max()} · x med {np.median(cx):.0f}")
