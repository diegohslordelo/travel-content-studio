"""Recorte do Diego por IA (RobustVideoMatting ResNet50, ONNX), quadro a quadro, para o tela verde.
A gravação não tem fundo verde (quarto escuro): mesmo método do Reel das greves (rev2.py recorte).
HLG (iPhone, BT.2020) → SDR BT.709 com o tonemap neutro (Hable, npl 100), o mesmo da conversão do vídeo inteiro.
Saída: ../fonte/recorte/diego_alfa.webm (VP9 com alfa, 1080 × 1920, 30 fps), fora do git.
Modelo: github.com/PeterL1n/RobustVideoMatting, release v1.0.0 (rvm_resnet50_fp32.onnx em ../fonte/modelos/).
Roda de dentro de reels/disney-frozen/rev1:  python3 scripts/recorte.py"""
import json, os, subprocess, sys
import numpy as np
import onnxruntime as ort

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
FONTE = os.path.normpath(os.path.join(AQUI, ed["fonte_dir"]))
ENTRADA = os.path.join(FONTE, ed["fonte"])
SAIDA = os.path.join(FONTE, "recorte", "diego_alfa.webm")
MODELO = os.path.join(FONTE, "modelos", "rvm_resnet50_fp32.onnx")
W, H, FPS = 1080, 1920, 30
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv")

if os.path.exists(SAIDA) and "--refazer" not in sys.argv:
    sys.exit(f"já existe: {SAIDA} (use --refazer)")
os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ENTRADA, "-vf", f"{TONEMAP},format=rgb24", "-f", "rawvideo", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-row-mt", "1",
                        "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", SAIDA], stdin=subprocess.PIPE)
op = ort.SessionOptions()
op.intra_op_num_threads = int(os.environ.get("THREADS", "4"))
s = ort.InferenceSession(MODELO, op, providers=["CPUExecutionProvider"])
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
dr = np.array([0.25], np.float32)  # recomendado pelo RVM para vídeo em retrato 1080p (corpo inteiro no quadro)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    x = (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]
    fgr, pha, *rec = s.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
    a = (np.clip(pha[0, 0], 0, 1) * 255).astype(np.uint8)
    # cor: o quadro original no corpo (o Diego fica idêntico ao vídeo inteiro) e a cor estimada pelo RVM só na borda
    # (alfa < 0,98), que tira o escuro do quarto do contorno sobre fundos claros
    fg = np.clip(fgr[0].transpose(1, 2, 0), 0, 1) * 255
    k = np.clip((pha[0, 0] - 0.88) / 0.10, 0, 1)[..., None]
    cor = (f * k + fg * (1 - k)).astype(np.uint8)
    enc.stdin.write(np.dstack([cor, a]).tobytes())
    n += 1
    if n % 60 == 0:
        print(f"{n} quadros", flush=True)
enc.stdin.close()
enc.wait()
print(f"{n} quadros → {SAIDA}")
