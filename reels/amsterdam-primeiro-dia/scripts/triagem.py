"""Triagem dos brutos da viagem: tremor (correlação de fase entre quadros a 12 qps, 256 × 144) e folha de contato.
Tremor = desvio do movimento em relação ao movimento suavizado (0,5 s): separa câmera tremida de panorâmica lenta.
Saída: _tmp/triagem/<arquivo>.json (tremor por janela de 0,5 s, px a 256 de largura) e _tmp/triagem/<arquivo>.jpg.
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/triagem.py fonte/acervo/IMG_*.MOV"""
import json, os, subprocess, sys
import numpy as np, cv2

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
os.makedirs("_tmp/triagem", exist_ok=True)
W, H, FPS = 256, 144, 12
for arq in sys.argv[1:]:
    nome = os.path.basename(arq).rsplit(".", 1)[0]
    out = f"_tmp/triagem/{nome}.json"
    if os.path.exists(out):
        continue
    r = subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-i", arq, "-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    q = np.frombuffer(r.stdout, np.uint8)
    n = len(q) // (W * H)
    if n < 3:
        continue
    q = q[: n * W * H].reshape(n, H, W).astype(np.float32)
    jan = cv2.createHanningWindow((W, H), cv2.CV_32F)
    d = np.array([cv2.phaseCorrelate(q[i], q[i + 1], jan)[0] for i in range(n - 1)])
    k = FPS // 2
    suave = np.array([d[max(0, i - k): i + k + 1].mean(0) for i in range(len(d))])
    trem = np.linalg.norm(d - suave, axis=1)
    mov = np.linalg.norm(suave, axis=1)
    janelas = [{"t": round(i / FPS, 2), "tremor": round(float(trem[i:i + k].mean()), 2), "mov": round(float(mov[i:i + k].mean()), 2),
                "luz": round(float(q[i].mean()), 1)} for i in range(0, len(trem), k)]
    json.dump({"arquivo": arq, "dur": round(n / FPS, 2), "janelas": janelas}, open(out, "w"))
    # folha: 1 quadro a cada 1,5 s (no máx. 16), com o tempo
    idx = list(range(0, n, int(FPS * 1.5)))[:16]
    tiles = []
    for i in idx:
        im = cv2.cvtColor(q[i].astype(np.uint8), cv2.COLOR_GRAY2BGR)
        tr = trem[min(i, len(trem) - 1)]
        cv2.putText(im, f"{i / FPS:.1f}s t{tr:.1f}", (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255) if tr < 1.5 else (0, 0, 255), 1)
        tiles.append(im)
    while len(tiles) % 8:
        tiles.append(np.zeros_like(tiles[0]))
    linhas = [np.hstack(tiles[j:j + 8]) for j in range(0, len(tiles), 8)]
    cab = np.zeros((18, W * 8, 3), np.uint8)
    cv2.putText(cab, nome, (4, 13), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.imwrite(f"_tmp/triagem/{nome}.jpg", np.vstack([cab] + linhas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(nome, n / FPS, f"tremor med {np.median(trem):.2f}", flush=True)
