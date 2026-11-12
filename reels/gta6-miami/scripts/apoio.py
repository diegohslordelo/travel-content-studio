"""Recorta os planos de apoio (rev1/clipes.json) para public/clipes/ (1080 x 900, 30 qps, mudos, sem ajuste de cor)
e extrai as fotos paradas para public/imagens/. Gera _tmp/apoio_conferir.jpg (1º, meio e último quadro de cada plano).
Uso (de dentro de reels/gta6-miami): python3 scripts/apoio.py [id ...]"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw

cfg = json.load(open("rev1/clipes.json"))
os.makedirs("public/clipes", exist_ok=True)
os.makedirs("public/imagens", exist_ok=True)
so = set(sys.argv[1:])
FPS = 30
for c in cfg["clipes"]:
    if so and c["id"] not in so:
        continue
    x, y, w = c["crop"]
    h = round(w / 1.2)
    n = round(c["dur"] * FPS)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['ini']:.3f}", "-i", cfg["fontes"][c["fonte"]], "-frames:v", str(n), "-an",
                    "-vf", f"fps={FPS},crop={w}:{h}:{x}:{y},scale=1080:900:flags=lanczos,setsar=1", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"public/clipes/{c['id']}.mp4"], check=True)
for f in cfg["fotos"]:
    if so and f["id"] not in so:
        continue
    x, y, w, h = f["crop"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(f["t"]), "-i", cfg["fontes"][f["fonte"]], "-frames:v", "1",
                    "-vf", f"crop={w}:{h - y}:{x}:{y}", "-q:v", "2", f"public/imagens/{f['id']}.jpg"], check=True)
# folha de conferência
linhas = []
for c in cfg["clipes"]:
    arq = f"public/clipes/{c['id']}.mp4"
    n = round(c["dur"] * FPS)
    qs = []
    for q in (0, n // 2, n - 1):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", arq, "-vf", f"select=eq(n\\,{q}),scale=270:225", "-frames:v", "1", "_tmp/q.png"], check=True)
        qs.append(Image.open("_tmp/q.png").copy())
    linhas.append((c["id"], qs))
W, H = 270 * 3 + 10, 225 + 18
folha = Image.new("RGB", (W * 3, H * ((len(linhas) + 2) // 3)), "black")
d = ImageDraw.Draw(folha)
for k, (nome, qs) in enumerate(linhas):
    ox, oy = (k % 3) * W, (k // 3) * H
    d.text((ox + 4, oy + 3), nome, fill="yellow")
    for j, im in enumerate(qs):
        folha.paste(im, (ox + j * 270, oy + 18))
folha.save("_tmp/apoio_conferir.jpg", quality=85)
print("ok")
