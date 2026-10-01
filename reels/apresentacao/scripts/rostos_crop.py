"""Detecta rostos (YuNet) quadro a quadro e diz onde o crop 9:16 (31,6% da largura) cabe com todos os rostos inteiros.
Uso: rostos_crop.py ARQUIVO INICIO FIM"""
import json, os, subprocess, sys
import numpy as np, cv2
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,")
DEITADOS = {"IMG_2730.MOV", "IMG_2761.MOV", "IMG_3134.MOV"}
arq, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
f = arq if os.path.exists(arq) else "fonte/outras_cidades/" + arq; arq = os.path.basename(arq)
hdr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
      "stream=color_transfer", "-of", "json", f]))["streams"][0].get("color_transfer") == "arib-std-b67"
W, H = 960, 540
vf = (TM if hdr else "") + ("transpose=clock," if arq in DEITADOS else "") + f"scale={W}:{H},fps=24,format=bgr24"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", f, "-vf", vf, "-f", "rawvideo", "-"],
                     stdout=subprocess.PIPE)
det = cv2.FaceDetectorYN.create("_tmp/yunet.onnx", "", (W, H), 0.6)
LARG = (2160 * 9 / 16) / 3840  # 0.316
i = 0; ruins = []
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    _, faces = det.detect(img)
    t = a + i / 24; i += 1
    if faces is None: print(f"{t:6.2f}s  sem rosto"); continue
    caixas = sorted([(fx / W, (fx + fw) / W) for fx, fy, fw, fh, *_ in faces if fw * fh > 900])
    esq = min(c[0] for c in caixas); dir_ = max(c[1] for c in caixas)
    marg = 0.01
    lo, hi = dir_ + marg - LARG / 2, esq - marg + LARG / 2   # faixa de centros possíveis
    ok = lo <= hi
    if not ok: ruins.append(t)
    rost = "  ".join(f"[{x0:.2f}-{x1:.2f}]" for x0, x1 in caixas)
    print(f"{t:6.2f}s  {len(caixas)} rosto(s) {rost:40s} centro possível: " + (f"{lo:.3f}–{hi:.3f}" if ok else f"NÃO CABE (falta {lo-hi:.3f})"))
print("quadros em que não cabe:", len(ruins), [f"{x:.2f}" for x in ruins][:40])
