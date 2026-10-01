"""Folha de frames por arquivo bruto: 1 frame/s (HDR com o mesmo tone mapping do Reel; SDR sem conversão)."""
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,eq=saturation=0.88,")
# gravados com o celular deitado e salvos como retrato: girar 90° no sentido horário
DEITADOS = {"IMG_2730.MOV", "IMG_2761.MOV", "IMG_3134.MOV"}
FONT = ImageFont.truetype("fontes/Montserrat-Bold.ttf", 22)
os.makedirs("analise_outras/folhas", exist_ok=True)
for f in sorted(glob.glob("fonte/outras_cidades/*")):
    if len(sys.argv) > 1 and os.path.basename(f) not in sys.argv[1:]:
        continue
    nome = os.path.splitext(os.path.basename(f))[0]
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=color_transfer:format=duration", "-of", "json", f]))
    hdr = info["streams"][0].get("color_transfer") == "arib-std-b67"
    dur = float(info["format"]["duration"])
    passo = 1.0 if dur <= 40 else 1.5
    tmp = f"/tmp/cs_{nome}"; os.makedirs(tmp, exist_ok=True)
    for p in glob.glob(tmp + "/*.jpg"): os.remove(p)
    vf = (TM if hdr else "") + ("transpose=clock," if os.path.basename(f) in DEITADOS else "") + f"fps=1/{passo},scale='if(gt(iw,ih),480,-2)':'if(gt(iw,ih),-2,480)',format=rgb24"
    subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", vf, "-q:v", "3", tmp + "/%03d.jpg"], check=True)
    fr = sorted(glob.glob(tmp + "/*.jpg"))
    ims = [Image.open(p) for p in fr]
    w, h = ims[0].size; cols = 8 if w > h else 10
    rows = (len(ims) + cols - 1) // cols
    folha = Image.new("RGB", (cols * w, rows * (h + 30) + 40), (17, 17, 17))
    d = ImageDraw.Draw(folha)
    d.text((8, 8), f"{nome} | {dur:.1f}s | {'HDR→SDR' if hdr else 'SDR'} | 1 frame a cada {passo:g}s", fill="white", font=FONT)
    for i, im in enumerate(ims):
        x, y = (i % cols) * w, 40 + (i // cols) * (h + 30)
        d.text((x + 6, y + 2), f"{i * passo:.1f}s", fill=(255, 215, 90), font=FONT)
        folha.paste(im, (x, y + 30))
    folha.thumbnail((2400, 2400))
    folha.save(f"analise_outras/folhas/{nome}.jpg", quality=85)
    print(nome, len(ims), "frames")
