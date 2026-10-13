"""Folhas de contato dos brutos (1 quadro a cada 1,5 s, tone mapping HLG -> SDR do projeto). Rodar de reels/bahia-camp-nou/."""
import glob
import os
import subprocess

TM = ("zscale=w=384:h=-2:f=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,"
      "format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:param=0.5:peak=4.93:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=saturation=0.88")
for a in sorted(glob.glob("fonte/brutos/*.MOV")):
    nome = os.path.basename(a)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a],
                               capture_output=True, text=True).stdout)
    n = max(1, int(dur / 1.5))
    cols = 6
    linhas = (n + cols - 1) // cols
    vf = (f"fps=1/1.5,{TM},drawtext=fontfile=_tmp/fontes/Barlow-Bold.ttf:text='%{{pts\\:hms}}':x=6:y=6:"
          f"fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6,tile={cols}x{linhas}:padding=4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-vf", vf, "-frames:v", "1", "-q:v", "4",
                    f"analise/folhas/{nome}.jpg"], check=True)
    print(nome, n, flush=True)
