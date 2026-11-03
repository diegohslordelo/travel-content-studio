"""Folhas de contato coloridas dos brutos (só quadros-chave: rápido), com o tempo de cada quadro.
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/folhas.py fonte/acervo/IMG_*.MOV → _tmp/folhas/<arquivo>.jpg"""
import os, subprocess, sys
import numpy as np, cv2
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
os.makedirs("_tmp/folhas", exist_ok=True)
for arq in sys.argv[1:]:
    nome = os.path.basename(arq).rsplit(".", 1)[0]
    if os.path.exists(f"_tmp/folhas/{nome}.jpg"):
        continue
    r = subprocess.run(["ffmpeg", "-v", "info", "-skip_frame", "nokey", "-i", arq, "-fps_mode", "vfr",
                        "-vf", "scale=240:240:force_original_aspect_ratio=decrease,pad=240:240:(ow-iw)/2:(oh-ih)/2,showinfo,format=bgr24",
                        "-f", "rawvideo", "-"], capture_output=True)
    ts = [float(x.split("pts_time:")[1].split()[0]) for x in r.stderr.decode(errors="ignore").split("\n") if "pts_time:" in x]
    q = np.frombuffer(r.stdout, np.uint8)
    n = len(q) // (240 * 240 * 3)
    q = q[: n * 240 * 240 * 3].reshape(n, 240, 240, 3)
    tiles = []
    for i in range(n):
        im = q[i].copy()
        cv2.putText(im, f"{ts[i] if i < len(ts) else -1:.1f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        tiles.append(im)
    tiles = tiles[:24]
    while len(tiles) % 12:
        tiles.append(np.zeros((240, 240, 3), np.uint8))
    linhas = [np.hstack(tiles[j:j + 12]) for j in range(0, len(tiles), 12)]
    cab = np.zeros((20, 240 * 12, 3), np.uint8)
    cv2.putText(cab, nome, (4, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imwrite(f"_tmp/folhas/{nome}.jpg", np.vstack([cab] + linhas), [cv2.IMWRITE_JPEG_QUALITY, 75])
    print(nome, n, flush=True)
