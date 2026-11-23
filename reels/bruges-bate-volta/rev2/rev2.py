#!/usr/bin/env python3
"""Reel "Bruges, bate-volta" · REV2 (os cortes da REV1, em HDR, sem conversão de cor).

Rode de dentro desta pasta:
    python3 rev2.py

Pedido do Diego (23/11/2026): "Deixe o mais fiel ao vídeo original possível". A REV1 convertia o
HDR do iPhone (HLG, BT.2020) para SDR com tone mapping, e as cores mudavam. A REV2 mantém o sinal
HLG 10 bits como saiu do iPhone: só corte, giro, recorte 9:16, escala e FPS.
- Os cortes e as fontes vêm de ../rev1/rev1.json (a REV1 não é alterada).
- A única fonte SDR (IMG_4218.mp4, BT.709) entra no HLG pelo mapeamento de referência do BT.2408:
  branco SDR = 203 nits = 75% do sinal HLG.
- Saída: HEVC Main10, BT.2020 + HLG (arib-std-b67), tag hvc1 (iPhone/Instagram leem como HDR).
  O Dolby Vision (perfil 8.4) dos brutos não é regravado: fica o HLG de base, que é compatível.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REV1 = os.path.normpath(os.path.join(AQUI, "..", "rev1", "rev1.json"))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
SAIDA = os.path.join(AQUI, "reel_bruges-bate-volta_rev2_hdr.mp4")
QA = os.path.join(AQUI, "qa_frames")

SDR_PARA_HLG = (
    "zscale=tin=bt709:min=bt709:pin=bt709:rin=tv:"
    "t=arib-std-b67:m=bt2020nc:p=bt2020:r=tv:npl=203"
)
X265 = [
    "-c:v", "libx265", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p10le", "-profile:v", "main10",
    "-x265-params", "colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:log-level=error",
    "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv",
    "-tag:v", "hvc1",
]
# Só para os quadros de QA (visualização num monitor SDR); não entra no vídeo.
PREVIA_SDR = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(f"falhou: {' '.join(cmd)[:200]}")
    return r.stdout


def transferencia(arq):
    return sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=color_transfer", "-of", "csv=p=0", arq]).strip().split("\n")[0].strip(",")


def cortar(i, c, W, H, fps):
    arq = os.path.join(FONTE, c["fonte"])
    quadros = round(c["dur"] * fps)
    trc = transferencia(arq)
    filtros = []
    if trc == "arib-std-b67":
        filtros.append("format=yuv420p10le")
    elif trc == "bt709":
        filtros.append(SDR_PARA_HLG)
        filtros.append("format=yuv420p10le")
    else:
        sys.exit(f"{c['fonte']}: transferência {trc!r} não prevista")
    filtros.append(f"fps={fps}")
    if "centro_x" in c:
        cx = c["centro_x"]
        filtros.append(f"crop=trunc(ih*9/16/2)*2:ih:'max(0,min(iw-ow,{cx}*iw-ow/2))':0")
    filtros.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1")
    filtros.append("format=yuv420p10le")
    saida = os.path.join(TMP, f"c{i:02d}.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-ss", str(c["in"]), "-i", arq, "-frames:v", str(quadros),
        "-vf", ",".join(filtros), "-an", *X265, "-r", str(fps), saida])
    return saida, quadros


def main():
    with open(REV1, encoding="utf-8") as f:
        cfg = json.load(f)
    W, H, fps = cfg["canvas"]["largura"], cfg["canvas"]["altura"], cfg["canvas"]["fps"]
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(QA, exist_ok=True)

    partes, t, marcas = [], 0, []
    for i, c in enumerate(cfg["cortes"], 1):
        p, q = cortar(i, c, W, H, fps)
        partes.append(p)
        marcas.append((i, c["fonte"], t / fps, (t + q) / fps))
        t += q
    dur = t / fps

    lista = os.path.join(TMP, "lista.txt")
    with open(lista, "w") as f:
        f.writelines(f"file '{p}'\n" for p in partes)
    video = os.path.join(TMP, "video.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-tag:v", "hvc1", video])
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-tag:v", "hvc1", "-c:a", "aac", "-b:a", "128k",
        "-t", f"{dur:.3f}", "-movflags", "+faststart", SAIDA])

    for i, fonte, a, b in marcas:
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", SAIDA, "-frames:v", "1",
            "-vf", f"{PREVIA_SDR},scale=270:480,format=yuvj420p", os.path.join(QA, f"corte_{i:02d}.jpg")])

    print(f"duração: {dur:.2f} s · {len(marcas)} cortes · HDR HLG 10 bits")
    for i, fonte, a, b in marcas:
        print(f"  {i}. {a:5.2f}–{b:5.2f} s ({b - a:.2f} s)  {fonte}")


if __name__ == "__main__":
    main()
