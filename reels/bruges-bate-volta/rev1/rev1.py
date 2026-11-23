#!/usr/bin/env python3
"""Reel "Bruges, bate-volta" · REV1 (só cortes).

Rode de dentro desta pasta:
    python3 rev1.py            # cortes → reel_bruges-bate-volta_rev1.mp4 + prévia + quadros de QA

Entradas: rev1.json (cortes desta revisão) e os brutos em ../fonte/ (fora do git; baixar do Drive
pelo `drive_id` de cada fonte em rev1.json). Usa só a biblioteca padrão do Python e o ffmpeg.

Padrão de edição (CLAUDE.md, 12): imagens sem tratamento de cor. Só entra o técnico: giro do iPhone,
HLG → SDR (tone mapping Möbius, docs/FORMATOS_REELS.md) e enquadramento 1080 × 1920.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
SAIDA = os.path.join(AQUI, "reel_bruges-bate-volta_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_bruges-bate-volta_rev1_previa.mp4")
QA = os.path.join(AQUI, "qa_frames")

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius.
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(f"falhou: {' '.join(cmd)[:200]}")
    return r.stdout


def transferencia(arq):
    return sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=color_transfer", "-of", "csv=p=0", arq]).strip()


def cortar(i, c, W, H, fps):
    arq = os.path.join(FONTE, c["fonte"])
    quadros = round(c["dur"] * fps)
    filtros = []
    if transferencia(arq) == "arib-std-b67":
        filtros.append(TONEMAP)
    filtros.append(f"fps={fps}")
    if c.get("estabilizar"):
        trf = os.path.join(TMP, f"c{i:02d}.trf")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", str(c["in"]), "-i", arq, "-frames:v", str(quadros),
            "-vf", f"fps={fps},vidstabdetect=shakiness=6:accuracy=15:result={trf}", "-f", "null", "-"])
        filtros.append(f"vidstabtransform=input={trf}:smoothing=20:optzoom=1:interpol=bicubic")
    # Enquadramento 9:16 sem distorção. Plano horizontal (acervo 4K): recorte de ih × 9/16 com o
    # centro em `centro_x` (fração da largura), escolhido para manter o Diego no quadro.
    if "centro_x" in c:
        cx = c["centro_x"]
        filtros.append(f"crop=trunc(ih*9/16/2)*2:ih:'max(0,min(iw-ow,{cx}*iw-ow/2))':0")
    filtros.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1")
    saida = os.path.join(TMP, f"c{i:02d}.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-ss", str(c["in"]), "-i", arq, "-frames:v", str(quadros),
        "-vf", ",".join(filtros), "-an", *X264, "-r", str(fps), saida])
    return saida, quadros


def main():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
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
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", video])

    # Sem som próprio: a música entra no app (CLAUDE.md, 12). Faixa de silêncio para o app aceitar o arquivo.
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-t", f"{dur:.3f}",
        "-movflags", "+faststart", SAIDA])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26",
        "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", PREVIA])

    # QA: um quadro no meio de cada corte.
    for i, fonte, a, b in marcas:
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", SAIDA, "-frames:v", "1",
            "-vf", "scale=270:480", os.path.join(QA, f"corte_{i:02d}.jpg")])
    sh(["ffmpeg", "-v", "error", "-y", "-pattern_type", "glob", "-i", os.path.join(QA, "corte_*.jpg"),
        "-vf", f"tile={len(marcas)}x1", "-frames:v", "1", os.path.join(QA, "folha_cortes.jpg")])

    print(f"duração: {dur:.2f} s · {len(marcas)} cortes")
    for i, fonte, a, b in marcas:
        print(f"  {i}. {a:5.2f}–{b:5.2f} s ({b - a:.2f} s)  {fonte}")


if __name__ == "__main__":
    main()
