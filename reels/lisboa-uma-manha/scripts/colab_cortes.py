#!/usr/bin/env python3
"""Cortes do Reel "Lisboa: uma manhã" para o Claude baixar pelo conector do Drive.

Por quê: o conector do Drive só entrega arquivos pequenos (na prática ~2,5 MB passam; 8 MB já falham) e os
vídeos de Lisboa são 4K HEVC (~2,7 MB por segundo). O Colab lê o Drive por dentro do Google e grava só o
trecho usado de cada plano, em pedaços pequenos.

Roda no Google Colab (Drive montado) ou em qualquer computador com ffmpeg + libx265.
Só LÊ os vídeos de Lisboa (não altera, não move, não renomeia). Grava em Youtube/cortes/lisboa_uma_manha/:
  - só a janela usada de cada plano (com ~0,4 s de folga), em pedaços de até 2 s;
  - já em retrato: recorte 1366 x 2160 do 4K deitado (9:16 + 151 px de folga para reenquadrar),
    redimensionado para 1214 x 1920 (a altura final do Reel, sem ampliar nada);
  - HEVC 10 bits a 9,5 Mbps com o HDR (HLG, BT.2020) intacto: o tone mapping HLG -> SDR é feito no render,
    pelo método aprovado no Reel de apresentação;
  - áudio AAC 48 kHz 192 kbps;
  - cada pedaço com no máximo 2,8 MB (se passar, refaz com 80% do bitrate).

Uso no Colab (depois de montar o Drive):
    !python colab_cortes.py --origem "/content/drive/MyDrive/Youtube/Lisboa"
"""
import argparse
import json
import math
import os
import subprocess
import sys

# arquivo, início (s), fim (s), centro do recorte (fração da largura), plano
CORTES = [
    ("IMG_4282.MOV", 11.0, 15.6, 0.52, "P1 gancho: 'o máximo que a gente vai conseguir conhecer em uma manhã praticamente'"),
    ("IMG_4284.MOV", 0.6, 2.6, 0.40, "P2 Marina entrando na rua (08:51)"),
    ("IMG_4292.MOV", 1.0, 2.6, 0.50, "P3 bandeja de pastéis de nata (08:58)"),
    ("IMG_4309.MOV", 0.6, 3.4, 0.45, "P4 elétrico na Praça do Comércio (09:14)"),
    ("IMG_4367.MOV", 2.5, 8.5, 0.60, "P5 estátua e arco da Praça do Comércio (09:23)"),
    ("IMG_4402.MOV", 1.0, 4.4, 0.48, "P6 Sé com o elétrico (09:52)"),
    ("IMG_4412.MOV", 0.5, 3.0, 0.45, "P7 violões no miradouro de Santa Luzia (10:03)"),
    ("IMG_4423.MOV", 3.5, 8.5, 0.50, "P8 azulejos e vista de Santa Luzia (10:05)"),
    ("IMG_4461.MOV", 0.5, 3.0, 0.50, "P9 vista das Portas do Sol (10:17)"),
    ("IMG_4472.MOV", 1.5, 4.5, 0.50, "P10 placa 'Castelo de S. Jorge' na escadaria (10:26)"),
    ("IMG_4476.MOV", 2.5, 7.0, 0.55, "P11 Marina e o mural de olhos (10:27)"),
    ("IMG_4478.MOV", 0.0, 4.6, 0.45, "P12 arco do castelo (10:30)"),
]
PEDACO_S = 2.0
KBPS = 9500
MAX_BYTES = int(2.8 * 1024 * 1024)
CROP_W, SRC_H = 1366, 2160
OUT_W, OUT_H = 1214, 1920


def achar(origem, nome):
    for dp, _, fs in os.walk(origem):
        if nome in fs:
            return os.path.join(dp, nome)
    raise FileNotFoundError(f"{nome} não está em {origem}")


def info(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", arq],
                       capture_output=True, text=True, check=True)
    s = json.loads(r.stdout)["streams"][0]
    rot = next((int(d.get("rotation", 0)) for d in s.get("side_data_list", []) if "rotation" in d), 0)
    w, h = s["width"], s["height"]
    if abs(rot) % 180 == 90:
        w, h = h, w
    return w, h, s.get("color_transfer")


def cortar(arq, t0, t1, cx, saida, kbps):
    w, h, trc = info(arq)  # dimensões já giradas (o ffmpeg aplica o giro sozinho)
    if w > h:  # deitado: recorte 9:16 com folga
        cw = int(round(CROP_W * h / SRC_H / 2)) * 2
        x = int(round(min(max(cx * w - cw / 2, 0), w - cw) / 2)) * 2
        vf = f"crop={cw}:{h}:{x}:0,scale={OUT_W}:{OUT_H}:flags=lanczos"
    else:      # já em pé
        vf = f"scale=-2:{OUT_H}:flags=lanczos,crop={OUT_W}:{OUT_H}"
    x265 = f"vbv-maxrate={int(kbps * 1.25)}:vbv-bufsize={int(kbps * 1.5)}:log-level=error"
    if trc == "arib-std-b67":
        x265 += ":colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", arq, "-t", f"{t1 - t0:.3f}",
                    "-map", "0:v:0", "-map", "0:a:0", "-vf", vf, "-c:v", "libx265", "-preset", "medium",
                    "-b:v", f"{kbps}k", "-pix_fmt", "yuv420p10le", "-tag:v", "hvc1", "-x265-params", x265,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", saida], check=True)
    return os.path.getsize(saida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--origem", required=True, help="pasta com os vídeos de Lisboa (Youtube/Lisboa)")
    ap.add_argument("--saida", help="padrão: <pasta acima da origem>/cortes/lisboa_uma_manha")
    a = ap.parse_args()
    saida = a.saida or os.path.join(os.path.dirname(a.origem.rstrip("/")), "cortes", "lisboa_uma_manha")
    os.makedirs(saida, exist_ok=True)
    n = 0
    for nome, t0, t1, cx, plano in CORTES:
        arq = achar(a.origem, nome)
        partes = math.ceil((t1 - t0) / PEDACO_S - 1e-6)
        for i in range(partes):
            p0, p1 = t0 + i * PEDACO_S, min(t0 + (i + 1) * PEDACO_S, t1)
            destino = os.path.join(saida, f"{nome[:-4]}_{int(round(p0 * 100)):04d}-{int(round(p1 * 100)):04d}.mov")
            if os.path.exists(destino) and os.path.getsize(destino) <= MAX_BYTES:
                print("já existe:", os.path.basename(destino))
                n += 1
                continue
            tam = cortar(arq, p0, p1, cx, destino, KBPS)
            if tam > MAX_BYTES:
                tam = cortar(arq, p0, p1, cx, destino, int(KBPS * 0.8))
            print(f"{os.path.basename(destino):30s} {tam / 1048576:4.2f} MB  {plano}", flush=True)
            n += 1
    print(f"\n{n} pedaços em {saida}. Pronto: avise o Claude.")


if __name__ == "__main__":
    sys.exit(main())
