"""Recorte do Diego (gravações do quarto) por IA: RobustVideoMatting ResNet50 (ONNX, github.com/PeterL1n/RobustVideoMatting,
release v1.0.0), com estado recorrente (estável no tempo). Mesmo método do Reel das greves (tela verde sem fundo verde).
Saída: fonte/recorte/<tomada>.webm (VP9 com alfa, 720 × 1280, 24 qps, mesmo tempo da tomada).
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/recorte.py <modelo.onnx> [tomadas...]"""
import os, subprocess, sys
import numpy as np
import onnxruntime as ort

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
W, H = 720, 1280
HLG = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,")
modelo = sys.argv[1]
tomadas = sys.argv[2:] or sorted(f[:-4] for f in os.listdir("fonte/quarto"))
s = ort.InferenceSession(modelo, providers=["CPUExecutionProvider"])
for tk in tomadas:
    arq = next(f"fonte/quarto/{f}" for f in os.listdir("fonte/quarto") if f.startswith(tk))
    saida = f"fonte/recorte/{tk}.webm"
    if os.path.exists(saida):
        continue
    hdr = "arib-std-b67" in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                                            "-of", "csv=p=0", arq], capture_output=True, text=True).stdout
    vf = (HLG if hdr else "") + f"scale={W}:{H}:flags=lanczos,format=rgb24"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", arq, "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "24", "-i", "-",
                            "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-row-mt", "1",
                            "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", saida + ".tmp.webm"], stdin=subprocess.PIPE)
    rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    dr = np.array([0.375], np.float32)
    n = 0
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        x = (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        fgr, pha, *rec = s.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
        a = (np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8)
        # cor do primeiro plano: a original (fgr só onde o alfa é parcial, para não tingir a borda com o fundo do quarto)
        fg = np.where((a[..., None] > 0) & (a[..., None] < 250), (np.clip(fgr[0].transpose(1, 2, 0), 0, 1) * 255).astype(np.uint8), f)
        enc.stdin.write(np.dstack([fg, a]).tobytes())
        n += 1
    enc.stdin.close(); enc.wait()
    os.rename(saida + ".tmp.webm", saida)
    print(f"{tk}: {n} quadros", flush=True)
