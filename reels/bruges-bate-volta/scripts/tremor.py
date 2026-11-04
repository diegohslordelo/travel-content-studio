"""Mede a tremedeira de cada take (deslocamento quadro a quadro por correlação de fase; tremor = desvio do
movimento em relação à trajetória suavizada). Uso: python3 -I scripts/tremor.py arquivo ini fim"""
import sys, subprocess, numpy as np, cv2
arq, ini, fim = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
w, h = 270, 480
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ini), "-i", arq, "-t", str(fim - ini), "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
win = cv2.createHanningWindow((w, h), cv2.CV_32F)
dx, dy = [], []
for a, b in zip(fr[:-1], fr[1:]):
    (sx, sy), _ = cv2.phaseCorrelate(a, b, win)
    dx.append(sx); dy.append(sy)
dx, dy = np.array(dx), np.array(dy)
def suave(v, k=9):
    return np.convolve(np.pad(v, k // 2, mode="edge"), np.ones(k) / k, mode="valid")
tx, ty = np.cumsum(dx), np.cumsum(dy)
jit = np.hypot(tx - suave(tx), ty - suave(ty)) * (1080 / w)  # px na escala 1080
print(f"{arq} {ini:.1f}-{fim:.1f}s  tremor médio {jit.mean():.1f} px  p95 {np.percentile(jit,95):.1f} px  movimento {np.hypot(dx,dy).mean()*1080/w:.1f} px/q")
