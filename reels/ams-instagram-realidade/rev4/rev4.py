"""Amsterdam · Instagram x Realidade · REV4.
Roda de reels/ams-instagram-realidade:  python3 rev4/rev4.py
Entradas (fora do git): fonte/IMG_*.MOV (Drive), fonte/internet/pexels_* (Pexels, licença livre), _tmp/ig_ref.wav (áudio do trend, só prévia).
Saídas: rev4/ams_instagram_realidade_rev4.mp4 (para postar, sem áudio) e rev4/ams_instagram_realidade_rev4_previa_com_audio.mp4."""
import json, os, subprocess
from PIL import Image, ImageOps

W, H, FPS, DUR = 1080, 1920, 30, 15.533
HLG = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
plan = json.load(open("rev4/rev4.json"))
os.makedirs("_tmp/seg4", exist_ok=True)

def recorte(SW, SH, s):
    """Recorte 9:16 (altura h, colado na base) em torno de cx."""
    if s.get("retrato") or SW * 16 == SH * 9:
        return 0, 0, SW, SH
    if SW * 16 < SH * 9:  # mais estreito que 9:16 (foto vertical 3:4): corta em altura, centro
        h = round(SW * 16 / 9 / 2) * 2
        return 0, (SH - h) // 2, SW, h
    h = s.get("h", SH); w = round(h * 9 / 16 / 2) * 2
    x = max(0, min(SW - w, round(s["cx"] * SW - w / 2)))
    return x, SH - h, w, h

segs = []
for i, s in enumerate(plan["planos"]):
    d = round(s["fim"] - s["ini"], 3); n = round(d * FPS)
    src = f"fonte/{s['arquivo']}"; out = f"_tmp/seg4/{i:02d}.mp4"
    if src.endswith(".jpg"):  # foto: recorte 9:16 + aproximação lenta (1,00 -> 1,06)
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        x, y, w, h = recorte(*im.size, s)
        im.crop((x, y, x + w, y + h)).resize((W * 2, H * 2), Image.LANCZOS).save("_tmp/seg4/foto.png")
        vf = (f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p,trim=duration={d}")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", "_tmp/seg4/foto.png", "-vf", vf, "-frames:v", str(n)]
    else:
        info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=color_transfer,width,height", "-of", "json", src], capture_output=True, text=True).stdout)["streams"][0]
        conv = HLG if info.get("color_transfer") == "arib-std-b67" else "format=yuv420p"
        x, y, w, h = recorte(info["width"], info["height"], s)
        geo = f"scale={W}:{H}:flags=lanczos" if s.get("retrato") else f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(s["src_in"]), "-t", str(d + 0.2), "-i", src,
               "-vf", f"{geo},{conv},fps={FPS},trim=duration={d},setpts=PTS-STARTPTS", "-an"]
    subprocess.run(cmd + ["-c:v", "libx264", "-crf", "12", "-preset", "medium", out], check=True)
    segs.append(out)

open("_tmp/seg4/lista.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in segs))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/seg4/lista.txt", "-c", "copy", "_tmp/montagem4.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/montagem4.mp4", "-t", str(DUR), "-an", "-c:v", "libx264", "-crf", "16",
                "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "rev4/ams_instagram_realidade_rev4.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "rev4/ams_instagram_realidade_rev4.mp4", "-i", "_tmp/ig_ref.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                "-movflags", "+faststart", "rev4/ams_instagram_realidade_rev4_previa_com_audio.mp4"], check=True)
print("ok")
