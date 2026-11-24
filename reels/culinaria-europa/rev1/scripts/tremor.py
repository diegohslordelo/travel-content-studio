"""Mede o tremor de um trecho (proxy 10 qps): deslocamento global quadro a quadro por correlação de fase.
Uso: python3 tremor.py proxy.mp4 ini dur"""
import sys, cv2, numpy as np
f, ini, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
cap = cv2.VideoCapture(f); fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(ini * fps))
prev = None; d = []; sharp = []
for i in range(int(dur * fps)):
    ok, fr = cap.read()
    if not ok: break
    g = cv2.cvtColor(cv2.resize(fr, (fr.shape[1] // 2, fr.shape[0] // 2)), cv2.COLOR_BGR2GRAY).astype(np.float32)
    sharp.append(cv2.Laplacian(g, cv2.CV_32F).var())
    if prev is not None:
        (dx, dy), _ = cv2.phaseCorrelate(prev, g); d.append((dx * dx + dy * dy) ** 0.5 * 2)
    prev = g
d = np.array(d)
print(f"{f.split('/')[-1]:22s} {ini:5.1f}+{dur:.1f}s  mov_med={np.median(d):5.1f}px  mov_p90={np.percentile(d,90):5.1f}px  nitidez={np.median(sharp):6.0f}")
