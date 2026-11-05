"""Luz roxa do GTA, muito leve, nas gravações do Diego (pedido do Diego, 05/11/2026). Gera public/diego_fundo.mp4: efeito só no fundo (parede, quadro, sofá); o Diego fica sem efeito.
(A versão com o efeito no quadro inteiro foi testada e descartada pelo Diego, 05/11/2026.)
Efeito: cor #8A3CFF em soft-light a 18% + luz radial do canto superior direito em screen a 10%.
Recorte do Diego: MediaPipe Image Segmenter (selfie_multiclass_256x256), máscara suavizada no espaço e no tempo.
Roda de dentro de reels/gta6-vice-city/rev2, depois de preparar_cenas.py (usa public/diego.mp4)."""
import os, subprocess, urllib.request
import numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

COR = np.array([0x8A, 0x3C, 0xFF], np.float32) / 255.0   # RGB
OPAC_SOFT, OPAC_LUZ = 0.18, 0.10
W, H = 1080, 1920
MODELO = "build/selfie_multiclass_256x256.tflite"
if not os.path.exists(MODELO):
    urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite", MODELO)

def soft_light(cb, cs):
    d = np.where(cb <= 0.25, ((16 * cb - 12) * cb + 4) * cb, np.sqrt(cb))
    return np.where(cs <= 0.5, cb - (1 - 2 * cs) * cb * (1 - cb), cb + (2 * cs - 1) * (d - cb))
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
radial = np.clip(1 - np.sqrt(((xx - 0.88 * W) / (0.75 * W)) ** 2 + ((yy - 0.18 * H) / (0.60 * H)) ** 2) / 0.70, 0, 1)[..., None]
def efeito(rgb):
    cb = rgb.astype(np.float32) / 255.0
    out = cb + (soft_light(cb, COR) - cb) * OPAC_SOFT
    out = 1 - (1 - out) * (1 - COR * radial * OPAC_LUZ)
    return out

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODELO), running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True))
fps = 30
leitor = subprocess.Popen(["ffmpeg", "-v", "error", "-i", "public/diego.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
def gravador(saida):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", saida], stdin=subprocess.PIPE)
g_fundo, g_mask = gravador("public/diego_fundo.mp4"), gravador("build/mascara_diego.mp4")
ema, n = None, 0
while True:
    buf = leitor.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)), int(n * 1000 / fps))
    fundo = r.confidence_masks[0].numpy_view().astype(np.float32)        # classe 0 = fundo
    pessoa = cv2.resize(1 - fundo, (W, H), interpolation=cv2.INTER_LINEAR)
    pessoa = cv2.GaussianBlur(pessoa, (0, 0), 3)                          # borda macia (sem serrilhado)
    ema = pessoa if ema is None else 0.6 * pessoa + 0.4 * ema             # sem tremor entre quadros
    m = np.clip((ema - 0.15) / 0.7, 0, 1)[..., None]
    fx = efeito(rgb)
    base = rgb.astype(np.float32) / 255.0
    g_fundo.stdin.write((np.clip(fx * (1 - m) + base * m, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    g_mask.stdin.write((np.repeat(m, 3, axis=2) * 255).astype(np.uint8).tobytes())
    n += 1
for g in (g_fundo, g_mask): g.stdin.close(); g.wait()
print(f"{n} quadros")
