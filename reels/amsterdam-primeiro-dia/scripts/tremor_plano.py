"""Aceleração (tremor) segundo a segundo de um bruto inteiro, na taxa original, para escolher o trecho mais firme.
Uso: python3 scripts/tremor_plano.py IMG_1375 [foco]"""
import os, subprocess, sys, json
import numpy as np, cv2
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
arq = f"fonte/acervo/{sys.argv[1]}.MOV"
foco = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
r = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:stream_side_data=rotation", "-of", "json", arq], capture_output=True, text=True).stdout)["streams"][0]
w, h = r["width"], r["height"]
if any(abs(int(s.get("rotation", 0))) == 90 for s in r.get("side_data_list", [])):
    w, h = h, w
fps = eval(r["r_frame_rate"])
crop = ""
if w > h:
    cw = round(h * 9 / 16); x0 = min(max(0, foco * w - cw / 2), w - cw); crop = f"crop={cw}:{h}:{x0:.0f}:0,"
o = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", f"{crop}scale=144:256,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
q = np.frombuffer(o, np.uint8); n = len(q) // (144 * 256); q = q[:n * 144 * 256].reshape(n, 256, 144).astype(np.float32)
jan = cv2.createHanningWindow((144, 256), cv2.CV_32F)
d = np.clip(np.array([cv2.phaseCorrelate(q[i], q[i + 1], jan)[0] for i in range(n - 1)]), -40, 40)
ac = np.linalg.norm(np.diff(d, axis=0), axis=1)
k = int(round(fps / 2))
print(sys.argv[1], " ".join(f"{i / fps:.1f}:{np.percentile(ac[i:i + k], 90):.1f}" for i in range(0, len(ac), k)))
