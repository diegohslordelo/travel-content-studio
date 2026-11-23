"""Mede o tremor de cada clipe do acervo (pedido do Diego: imagens estabilizadas, nada balançando).
Método: quadros reduzidos (largura 360) a 24 qps; deslocamento global entre quadros por correlação de fase (OpenCV);
trajetória acumulada; tremor = resíduo da trajetória menos a sua média móvel de 0,5 s (o que é balanço da mão),
em % da largura; movimento = velocidade da média móvel (panorâmica intencional), em % da largura por segundo.
Também acha a melhor janela de 2,5 s (menor tremor) de cada clipe.
Uso (de dentro de reels/disney-atracoes/): python3 scripts/estabilidade.py [IMG_xxxx ...]
Saída: _tmp/estabilidade.json"""
import glob, json, os, subprocess, sys
import cv2
import numpy as np

W = 360
FPS = 24


def quadros(arq):
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                           "-of", "json", arq], capture_output=True, text=True).stdout
    s = json.loads(info)["streams"][0]
    w, h = s["width"], s["height"]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    if abs(rot) == 90:
        w, h = h, w
    H = int(round(h * W / w / 2) * 2)
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", f"fps={FPS},scale={W}:{H}", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
                       capture_output=True, check=True).stdout
    n = len(p) // (W * H)
    return np.frombuffer(p, dtype=np.uint8)[:n * W * H].reshape(n, H, W), (w, h)


def media_movel(x, k):
    if len(x) < 3:
        return x.copy()
    k = max(3, min(k, len(x) // 2 * 2 - 1)) | 1
    pad = np.pad(x, (k // 2, k // 2), mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")


def analisa(arq):
    fr, (w, h) = quadros(arq)
    jan = np.hanning(fr.shape[2])[None, :] * np.hanning(fr.shape[1])[:, None]
    prev = fr[0].astype(np.float64)
    dx, dy, resp = [0.0], [0.0], [1.0]
    for f in fr[1:]:
        cur = f.astype(np.float64)
        (sx, sy), r = cv2.phaseCorrelate(prev, cur, jan)
        dx.append(sx); dy.append(sy); resp.append(r)
        prev = cur
    dx, dy = np.array(dx), np.array(dy)
    tx, ty = np.cumsum(dx), np.cumsum(dy)
    k = int(FPS * 0.5)
    sx, sy = media_movel(tx, k), media_movel(ty, k)
    jit = np.hypot(tx - sx, ty - sy) / W * 100  # % da largura, por quadro
    vel = np.hypot(np.gradient(sx), np.gradient(sy)) * FPS / W * 100  # % da largura por segundo
    dur = len(fr) / FPS
    # melhor janela de 2,5 s
    n = int(2.5 * FPS)
    melhor = (0.0, float(np.sqrt(np.mean(jit ** 2))))
    if len(jit) > n:
        c = np.convolve(jit ** 2, np.ones(n) / n, mode="valid")
        i = int(np.argmin(c))
        melhor = (round(i / FPS, 2), round(float(np.sqrt(c[i])), 3))
    return {"dur": round(dur, 2), "w": w, "h": h, "tremor_rms": round(float(np.sqrt(np.mean(jit ** 2))), 3),
            "tremor_p95": round(float(np.percentile(jit, 95)), 3), "movimento_med": round(float(np.median(vel)), 2),
            "movimento_max": round(float(np.percentile(vel, 95)), 2), "melhor_2s5": melhor,
            "tremor_por_s": [round(float(np.sqrt(np.mean(jit[i:i + FPS] ** 2))), 3) for i in range(0, len(jit), FPS)],
            "mov_por_s": [round(float(np.mean(vel[i:i + FPS])), 2) for i in range(0, len(vel), FPS)]}


if __name__ == "__main__":
    os.makedirs("_tmp", exist_ok=True)
    saida = "_tmp/estabilidade.json"
    R = json.load(open(saida)) if os.path.exists(saida) else {}
    nomes = sys.argv[1:] or sorted(os.path.basename(f)[:-4] for f in glob.glob("fonte/clipes/*.MOV"))
    for nm in nomes:
        R[nm] = analisa(f"fonte/clipes/{nm}.MOV")
        r = R[nm]
        print(f"{nm} {r['w']}x{r['h']} {r['dur']:5.2f}s tremor {r['tremor_rms']:.3f}% (p95 {r['tremor_p95']:.3f}) mov {r['movimento_med']:.1f}%/s melhor@{r['melhor_2s5'][0]}s={r['melhor_2s5'][1]:.3f}", flush=True)
        json.dump(R, open(saida, "w"), indent=0)
