"""Rosto do Diego por quadro (a cada 0,1 s) nas gravações, em coordenadas do quadro 1080×1920 (Haar, OpenCV 4).

Uso (de dentro de rev4): python3 rosto.py ../fonte/gravacao.mp4 rosto_A.json · python3 rosto.py ../fonte/novas.mp4 rosto_B.json
Saída: [t, x, y, w, h]; a base da caixa fica na boca ou no queixo (a barba vai ≈ 50 px abaixo)."""
import sys, json, subprocess, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
W, H = 270, 480  # 1/4 de 1080×1920
raw = subprocess.run(f'ffmpeg -v error -i {src} -vf "fps=10,scale={W}:{H},format=gray" -f rawvideo -', shell=True, check=True, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
res = []
for i, f in enumerate(fr):
    f = cv2.equalizeHist(f)
    fs = cas.detectMultiScale(f, scaleFactor=1.08, minNeighbors=5, minSize=(40, 40))
    if len(fs):
        x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
        res.append([round(i / 10, 2), int(x * 4), int(y * 4), int(w * 4), int(h * 4)])
    else:
        res.append([round(i / 10, 2), None, None, None, None])
json.dump(res, open(out, "w"))
ok = [r for r in res if r[1] is not None]
ys = np.array([[r[2], r[2] + r[4]] for r in ok])
print(src.split('/')[-1], "quadros", len(res), "com rosto", len(ok), "topo p5/p50", np.percentile(ys[:, 0], [5, 50]).round(), "base(queixo) p50/p95/max", np.percentile(ys[:, 1], [50, 95, 100]).round())
