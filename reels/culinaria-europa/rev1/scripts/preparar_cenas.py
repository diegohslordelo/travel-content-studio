"""Prepara as cenas de apoio (metade de cima, 1080 x 900, 30 qps, sem áudio).
Só técnica: HLG -> SDR (branco de referência 203 nits, BT.2408), rotação, corte, estabilização (vidstab).
Nenhum ajuste de cor. Roda de reels/culinaria-europa:  python3 rev1/scripts/preparar_cenas.py"""
import json, os, subprocess, sys
CENAS = json.load(open("rev1/cenas.json"))
TM = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
      "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
W, H = 1080, 900
os.makedirs("rev1/public/cenas", exist_ok=True); os.makedirs("_tmp/stab", exist_ok=True)
so = sys.argv[1:]
for c in CENAS["cenas"]:
    if c["tipo"] != "video" or (so and c["id"] not in so):
        continue
    src = f'fonte/acervo/{c["fonte"]}'
    out = f'rev1/public/cenas/{c["id"]}.mp4'
    dur = round(c["fim"] - c["ini"] + 0.1, 3)  # alça de 0,1 s
    rot = {"cw": "transpose=1,", "ccw": "transpose=2,", "180": "hflip,vflip,"}.get(c.get("girar", ""), "")
    z = c.get("zoom", 1.0); cx = c.get("cx", 0.5); cy = c.get("cy", 0.5)
    # escala para cobrir 1080x900 * zoom, depois corta centrado em (cx, cy)
    crop = (f"scale=w='if(gt(iw/ih,{W/H}),-2,{int(W*z)})':h='if(gt(iw/ih,{W/H}),{int(H*z)},-2)':flags=lanczos,"
            f"crop={W}:{H}:'min(max(iw*{cx}-{W/2},0),iw-{W})':'min(max(ih*{cy}-{H/2},0),ih-{H})'")
    base = f"{rot}scale=-2:1440:flags=lanczos,{TM},fps=30"
    if c.get("estabilizar"):
        trf = f'_tmp/stab/{c["id"]}.trf'
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["in"]), "-t", str(dur), "-i", src, "-an",
                        "-vf", f"{base},vidstabdetect=shakiness=6:accuracy=15:result={trf}", "-f", "null", "-"], check=True)
        base += f",vidstabtransform=input={trf}:smoothing=30:optzoom=1:interpol=bicubic,unsharp=5:5:0.4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["in"]), "-t", str(dur), "-i", src, "-an",
                    "-vf", f"{base},{crop},setsar=1", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out], check=True)
    print("ok", c["id"], flush=True)
