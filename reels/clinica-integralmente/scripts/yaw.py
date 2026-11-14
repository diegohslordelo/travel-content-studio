# Mede a rotação horizontal da câmera (yaw) por correlação de fase na metade de cima do quadro.
import subprocess, sys, numpy as np, cv2
f = sys.argv[1]; W, H, FPS = 180, 320, 10
raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-vf",f"fps={FPS},scale={W}:{H}","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
top = fr[:, int(H*0.08):int(H*0.45), :]
win = cv2.createHanningWindow((W, top.shape[1]), cv2.CV_32F)
dx = [0.0]
for a, b in zip(top[:-1], top[1:]):
    (sx, sy), r = cv2.phaseCorrelate(a, b, win); dx.append(sx)
dx = np.array(dx); per_s = np.convolve(dx, np.ones(FPS), 'same')  # px/s em 180 px de largura
cum = np.cumsum(dx)
for i in range(0, len(dx), 5):
    print(f"{i/FPS:6.1f}s  dx/s={per_s[i]:+6.1f}  acum={cum[i]:+7.1f}  " + ("<" * int(max(0,-per_s[i])/3)) + (">" * int(max(0,per_s[i])/3)))
