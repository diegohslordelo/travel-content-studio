"""Revisão 6, imagem: monta a base sem texto (989 quadros) a partir dos quadros do Reel da rev. 5 e do corte novo de Paris.

Os brutos de Barcelona e das outras cidades não estão nesta máquina; o Reel da rev. 5 (sem texto) já tem cada cena
recortada, com tone mapping e cor aprovados. Só o corte novo (IMG_2978, Paris) sai do arquivo original, pelo mesmo
filtro do render (girar 90°, crop 9:16, HLG -> SDR Rec.709).

Uso: python3 montar_video_rev6.py   (REEL_TMP aponta a pasta de trabalho)
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REV5 = os.path.join(BASE, "reel_apresentacao_sem_texto.mp4")
edl = R.carregar(os.path.join(BASE, "lista_de_cortes_rev6.json"))
TMP = os.path.join(edl["_tmp"], "video_rev6")
os.makedirs(TMP, exist_ok=True)

# (origem, primeiro quadro, quadro final exclusivo) na ordem da rev. 6
SEGMENTOS = [
    ("rev5", 0, 99),      # gancho + Vaso de Oro até 4,125 s (antes 4,25 s: a boca abria sem som no fim)
    ("rev5", 102, 170),   # Arco (de costas): os primeiros 68 quadros do mesmo plano, de 4,125 a 6,958 s
    ("paris", 0, 36),     # corte novo: IMG_2978 5,55-7,05 s, de 6,958 a 8,458 s
    ("rev5", 203, 471),   # Camp Nou, brinde, Arco (vira) e "Buenos días" sem mudança
    ("rev5", 476, 536),   # Amsterdam sem os 5 primeiros quadros (fim do movimento de câmera)
    ("rev5", 536, 994),   # Torre Eiffel até o fim, sem mudança
]
COR = R.TAGS_COR
partes = []
for k, (orig, a, b) in enumerate(SEGMENTOS):
    saida = os.path.join(TMP, f"seg_{k}.mkv")
    if orig == "rev5":
        R.rodar(["ffmpeg", "-v", "error", "-y", "-i", REV5, "-map", "0:v:0", "-vf",
                 f"select='between(n\\,{a}\\,{b - 1})',setpts=N/(24*TB)", "-fps_mode", "passthrough",
                 "-frames:v", b - a, "-c:v", "libx264", "-qp", "0", "-preset", "veryfast", *COR, saida])
    else:
        c = [x for x in edl["_cortes"] if x.get("arquivo", "").endswith("IMG_2978.MOV")][0]
        vf = f"{R.filtro_video(c)},fps={R.FPS},setsar=1"
        R.rodar(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['entrada']:.3f}", "-i", c["_arq"], "-map", "0:v:0",
                 "-an", "-sn", "-dn", "-vf", vf, "-frames:v", c["frames"], "-c:v", "libx264", "-qp", "0",
                 "-preset", "veryfast", *COR, saida])
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", saida], capture_output=True, text=True).stdout.strip().split(",")[0])
    assert n == b - a, f"segmento {k}: {n} quadros, esperado {b - a}"
    partes.append(saida)
lista = os.path.join(TMP, "lista.txt")
open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
base = os.path.join(TMP, "base_rev6.mkv")
R.rodar(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-vf", "setpts=N/(24*TB)",
         "-c:v", "libx264", "-qp", "0", "-preset", "veryfast", *COR, base])
n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", base], capture_output=True, text=True).stdout.strip().split(",")[0])
assert n == edl["_frames"], (n, edl["_frames"])
json.dump({"segmentos": SEGMENTOS, "quadros": n}, open(os.path.join(TMP, "base_rev6.json"), "w"))
print(f"base: {base} ({n} quadros = {n / 24:.3f} s)")
