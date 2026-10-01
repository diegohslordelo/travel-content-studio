"""Quadros em pé (orientação corrigida) dos brutos, com a largura do crop 9:16 marcada em faixas de 10%."""
import json, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=reinhard:param=0.5:peak=4.93:desat=0,zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,eq=saturation=0.88,")
# gravados com o celular deitado e salvos como retrato: girar 90° no sentido horário
DEITADOS = {"IMG_2730.MOV", "IMG_2761.MOV", "IMG_3134.MOV"}
FONT = ImageFont.truetype("fontes/Montserrat-Bold.ttf", 26)
def quadro(arq, t, saida, largura=1280):
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                               "stream=color_transfer", "-of", "json", "fonte/outras_cidades/" + arq]))
    hdr = info["streams"][0].get("color_transfer") == "arib-std-b67"
    vf = (TM if hdr else "") + ("transpose=clock," if arq in DEITADOS else "") + f"scale={largura}:-2,format=rgb24"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", "fonte/outras_cidades/" + arq,
                    "-frames:v", "1", "-vf", vf, saida], check=True)
if __name__ == "__main__":
    arq, tempos = sys.argv[1], [float(x) for x in sys.argv[2].split(",")]
    ims = []
    for t in tempos:
        p = f"/tmp/q_{t}.png"; quadro(arq, t, p, 960); ims.append((t, Image.open(p).convert("RGB")))
    w, h = ims[0][1].size
    cols = 3 if w > h else 6
    rows = (len(ims) + cols - 1) // cols
    folha = Image.new("RGB", (cols * w, rows * (h + 36)), (17, 17, 17)); d = ImageDraw.Draw(folha)
    for i, (t, im) in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * (h + 36)
        folha.paste(im, (x, y + 36)); d.text((x + 8, y + 4), f"{arq} {t:.2f}s", fill=(255, 215, 90), font=FONT)
        if w > h:  # régua de x (0.0 a 1.0) para escolher o centro do crop 9:16 (31,6% da largura)
            for k in range(1, 10):
                d.line([(x + w * k / 10, y + 36), (x + w * k / 10, y + 60)], fill=(255, 255, 255), width=2)
                d.text((x + w * k / 10 + 3, y + 38), f".{k}", fill="white", font=FONT)
    folha.save(sys.argv[3], quality=88)
