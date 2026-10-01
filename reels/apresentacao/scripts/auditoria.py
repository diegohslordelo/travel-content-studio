"""Auditoria de imagem de trechos do Reel, medida no quadro final (crop 9:16 em 1080x1920, com o tone mapping).

Por quadro: nitidez = variância do laplaciano na região do rosto + camisa (rosto achado com YuNet; sem rosto,
região central); tremida = deslocamento entre quadros (correlação de fase, em px do quadro final);
exposição = % de pixels estourados (luma >= 250) e pretos (<= 6).
Uso como módulo: auditar(corte) -> dict; ou CLI: auditoria.py ARQ INICIO FIM [centro_x] [girar] (imprime janelas de 0,5 s)
"""
import os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

W, H = 1080, 1920
_DET = None


def detector():
    global _DET
    if _DET is None:
        _DET = cv2.FaceDetectorYN.create(os.path.join(R.RAIZ, "_tmp", "yunet.onnx"), "", (270, 480), 0.6)
    return _DET


def quadros(c):
    vf = R.filtro_video(c, "gray") + f",fps=24"
    dur = c["saida"] - c["entrada"]
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{c['entrada']:.3f}", "-i", c["_arq"], "-map", "0:v:0", "-t", f"{dur:.3f}",
                        "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, H, W)


def auditar(c):
    fr = quadros(c)
    det = detector()
    res = []
    ant = None
    for k, g in enumerate(fr):
        pq = cv2.resize(g, (270, 480), interpolation=cv2.INTER_AREA)
        _, faces = det.detect(cv2.cvtColor(pq, cv2.COLOR_GRAY2BGR))
        if faces is not None and len(faces):
            fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])[:4] * 4
            x0, x1 = int(max(0, fx - 0.6 * fw)), int(min(W, fx + 1.6 * fw))
            y0, y1 = int(max(0, fy - 0.2 * fh)), int(min(H, fy + 3.0 * fh))
            rosto = True
        else:
            x0, x1, y0, y1, rosto = W // 4, 3 * W // 4, int(H * 0.3), int(H * 0.8), False
        roi = g[y0:y1, x0:x1]
        nit = float(cv2.Laplacian(roi, cv2.CV_64F).var()) if roi.size else 0.0
        mov = 0.0
        pf = pq.astype(np.float32)
        if ant is not None:
            (dx, dy), _ = cv2.phaseCorrelate(ant, pf)
            mov = float(np.hypot(dx, dy) * 4)
        ant = pf
        res.append({"t": c["entrada"] + k / 24, "nit": nit, "rosto": rosto, "mov": mov,
                    "estouro": float(np.mean(g >= 250) * 100), "preto": float(np.mean(g <= 6) * 100), "luma": float(g.mean())})
    return res


def janelas(res, passo=0.5):
    t0 = res[0]["t"]
    out = []
    k = 0
    while k < len(res):
        bloco = [r for r in res if t0 + k * 0 <= r["t"] < t0 + 99]  # placeholder
        break
    for i in range(int(np.ceil((res[-1]["t"] - t0 + 1e-6) / passo))):
        b = [r for r in res if t0 + i * passo <= r["t"] < t0 + (i + 1) * passo]
        if b:
            out.append({"de": t0 + i * passo, "nit": float(np.median([r["nit"] for r in b])), "mov": float(max(r["mov"] for r in b)),
                        "rosto": float(np.mean([r["rosto"] for r in b])), "estouro": float(max(r["estouro"] for r in b)),
                        "preto": float(max(r["preto"] for r in b)), "luma": float(np.mean([r["luma"] for r in b]))})
    return out


if __name__ == "__main__":
    arq, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    c = {"_arq": arq, "entrada": a, "saida": b, "centro_x": float(sys.argv[4]) if len(sys.argv) > 4 else 0.5,
         "girar": int(sys.argv[5]) if len(sys.argv) > 5 else 0}
    res = auditar(c)
    for j in janelas(res):
        print(f"{j['de']:6.2f}s  nitidez {j['nit']:7.1f}  rosto {j['rosto'] * 100:3.0f}%  tremida máx {j['mov']:5.1f} px/q  "
              f"estouro {j['estouro']:4.1f}%  preto {j['preto']:4.1f}%  luma {j['luma']:5.1f}")
