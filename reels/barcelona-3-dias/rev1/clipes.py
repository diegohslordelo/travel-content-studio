"""Cortes do vlog em vertical para o Reel (rodar de dentro de rev1, depois de escolher os takes em takes.json).

Master: ../fonte/Barcelona_3dias.mov (Drive, pasta Youtube, 10.137.720.126 bytes; 3840×2160 HEVC HLG, 24 qps).
Cada take: recorte 9:16 (1215×2160) na posição horizontal escolhida ("cx", 0 = esquerda, 1 = direita),
conversão HLG→SDR igual à dos Reels aprovados (Veneza REV4, sem grade, sem LUT), 1080×1920, 30 qps, sem áudio.
"""
import json
import os
import subprocess

M = "../fonte/Barcelona_3dias.mov"
PUB = "public"
os.makedirs(PUB, exist_ok=True)
CONV = ("zscale=t=linear:npl=600,format=gbrpf32le,zscale=p=bt709,tonemap=clip:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
TAKES = json.load(open("takes.json"))

for nome, tk in TAKES.items():
    out = f"{PUB}/{nome}.mp4"
    chave = f"{tk['ini']}:{tk['dur']}:{tk['cx']}:{tk.get('cx_fim')}:{tk.get('zoom', 1)}:{tk.get('cy')}"
    marca = f"{PUB}/.{nome}.chave"
    if os.path.exists(out) and os.path.exists(marca) and open(marca).read() == chave:
        continue
    z = tk.get("zoom", 1.0)       # recorte mais fechado (ex.: tirar uma pessoa da borda), ainda ≥ 1080 px de largura
    cw = round(1215 / z / 2) * 2
    ch = round(2160 / z / 2) * 2
    x = round((3840 - cw) * tk["cx"])
    if "cx_fim" in tk:   # recorte que acompanha uma panorâmica (posição linear do início ao fim do take)
        x1 = round((3840 - cw) * tk["cx_fim"])
        x = f"'{x}+({x1}-{x})*t/{tk['dur']:.3f}'"
    y = round((2160 - ch) * tk.get("cy", 0.5))
    subprocess.run(
        f'ffmpeg -v error -y -ss {tk["ini"]:.3f} -t {tk["dur"]:.3f} -i {M} -an '
        f'-vf "crop={cw}:{ch}:{x}:{y},{CONV},scale=1080:1920:flags=lanczos,fps=30" '
        f'-c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 {out}',
        shell=True, check=True)
    open(marca, "w").write(chave)
    print("clipe", nome, tk["ini"], tk["dur"])
