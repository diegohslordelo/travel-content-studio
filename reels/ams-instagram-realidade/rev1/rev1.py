"""Amsterdam · Instagram x Realidade · REV1.
Roda de reels/ams-instagram-realidade:  python3 rev1/rev1.py
Entradas: fonte/IMG_*.MOV (Drive) e fonte/internet/pexels_*.mp4 (Pexels, licença livre), fora do git; e _tmp/ig_ref.wav (áudio do Reel de referência, só para a prévia).
Saídas: rev1/ams_instagram_realidade_rev1.mp4 (para postar: só o keen; o áudio do trend entra no app)
        rev1/ams_instagram_realidade_rev1_previa_com_audio.mp4 (conferência de sincronia com o áudio do trend)."""
import json, os, subprocess

W, H, FPS = 1080, 1920, 30
DUR = 15.533  # duração do áudio de referência
T = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
     "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
plan = json.load(open("rev1/rev1.json"))
os.makedirs("_tmp/seg", exist_ok=True)

segs = []
for i, s in enumerate(plan["planos"]):
    d = round(s["fim"] - s["ini"], 3)
    pre = "transpose=2," if s.get("girar") else ""
    src = f"fonte/{s['arquivo']}"
    trc = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer,width,height",
                          "-of", "json", src], capture_output=True, text=True).stdout
    info = json.loads(trc)["streams"][0]
    conv = T if info.get("color_transfer") == "arib-std-b67" else "format=yuv420p"  # HLG do iPhone -> SDR; o resto já é SDR
    SW, SH = (info["height"], info["width"]) if s.get("girar") else (info["width"], info["height"])
    if SW * 16 == SH * 9:  # já é 9:16
        geo = f"scale={W}:{H}:flags=lanczos"
    else:  # horizontal: recorte 9:16 (altura h, colado na base) em torno de cx
        h = s.get("h", SH); w = round(h * 9 / 16 / 2) * 2
        x = max(0, min(SW - w, round(s["cx"] * SW - w / 2)))
        geo = f"crop={w}:{h}:{x}:{SH - h},scale={W}:{H}:flags=lanczos"
    out = f"_tmp/seg/{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["src_in"]), "-t", str(d + 0.2), "-i", src,
                    "-vf", f"{pre}{geo},{conv},fps={FPS},trim=duration={d},setpts=PTS-STARTPTS", "-an",
                    "-c:v", "libx264", "-crf", "12", "-preset", "medium", out], check=True)
    segs.append(out)

open("_tmp/seg/lista.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in segs))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/seg/lista.txt", "-c", "copy", "_tmp/montagem.mp4"], check=True)

# Sem letreiro nem legenda: o Diego coloca o texto no app.

# keen: pico (0,96 s do arquivo) no corte Instagram -> Realidade
k = plan["keen"]; atraso = int(round((k["corte"] - 0.96) * 1000))
keen = f"[1:a]volume={k['volume_db']}dB,adelay={atraso}|{atraso},apad,atrim=0:{DUR}[k]"
base = ["ffmpeg", "-v", "error", "-y", "-i", "_tmp/montagem.mp4", "-i", "../../design-system/sons/externos/keen.wav"]
vf = "[0:v]format=yuv420p[v]"
subprocess.run(base + ["-filter_complex", f"{vf};{keen}", "-map", "[v]", "-map", "[k]",
                       "-t", str(DUR), "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-profile:v", "high",
                       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "rev1/ams_instagram_realidade_rev1.mp4"], check=True)
subprocess.run(base + ["-i", "_tmp/ig_ref.wav", "-filter_complex",
                       f"{vf};{keen};[2:a]aresample=48000[m];[m][k]amix=inputs=2:normalize=0[a]", "-map", "[v]", "-map", "[a]",
                       "-t", str(DUR), "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
                       "-movflags", "+faststart", "rev1/ams_instagram_realidade_rev1_previa_com_audio.mp4"], check=True)
print("ok")
