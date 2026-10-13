"""Baixa do Google Drive só a parte do master de Barcelona que a REV4 usa.

O master (Barcelona_3dias, 10,1 GB) fica na pasta do Drive do projeto. Em vez de baixar o arquivo inteiro,
este script cria uma cópia local esparsa do mesmo tamanho (o disco só guarda o que foi escrito) com o índice do
arquivo (átomo moov) e os bytes de vídeo e áudio do trecho em rev4.json ("master" → "trecho_s"). O ffmpeg lê
essa cópia como se fosse o master inteiro, desde que só peça tempos dentro do trecho.

Uso (de dentro de reels/agua-barcelona/):
  python3 rev4/scripts/baixar_trecho_master.py
Saída: rev4/_tmp/master_esparso.mov

O link do arquivo precisa estar compartilhado como "qualquer pessoa com o link". O Google limita downloads
anônimos repetidos do mesmo arquivo: se a resposta vier como página HTML ("Quota exceeded"), espere e rode de novo.
"""
import csv
import io
import json
import os
import struct
import subprocess
import time
import urllib.request

REV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(REV, "rev4.json"), encoding="utf-8"))["master"]
URL = f"https://drive.usercontent.google.com/download?id={M['drive_id']}&export=download&confirm=t"
SAIDA = os.path.join(REV, "_tmp", "master_esparso.mov")
BLOCO = 8 * 1024 * 1024


def intervalo(a, b):
    for tentativa in range(6):
        r = urllib.request.urlopen(urllib.request.Request(URL, headers={"Range": f"bytes={a}-{b}"}), timeout=300)
        d = r.read()
        if r.status == 206 and len(d) == b - a + 1:
            return d
        print(f"   resposta inesperada ({r.status}, {len(d)} bytes, {r.headers.get('Content-Type')}); nova tentativa")
        time.sleep(10 * (tentativa + 1))
    raise RuntimeError("o Drive não entregou o intervalo pedido (cota de download?)")


def baixar(f, a, b):
    p = a
    while p <= b:
        q = min(p + BLOCO - 1, b)
        f.seek(p)
        f.write(intervalo(p, q))
        p = q + 1


def main():
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    tam = M["tamanho_bytes"]
    with open(SAIDA, "wb") as f:
        f.truncate(tam)
        pos = 0
        while pos < tam:  # átomos de primeiro nível: acha o moov
            h = intervalo(pos, pos + 15)
            sz, tipo = struct.unpack(">I4s", h[:8])
            sz = struct.unpack(">Q", h[8:16])[0] if sz == 1 else (tam - pos if sz == 0 else sz)
            if tipo in (b"ftyp", b"moov"):
                f.seek(pos)
                f.write(intervalo(pos, pos + sz - 1))
            pos += sz
    t0, t1 = M["trecho_s"]
    r = subprocess.run(["ffprobe", "-v", "error", "-read_intervals", f"{t0}%{t1}", "-show_entries",
                        "packet=stream_index,pos,size", "-of", "csv=p=0", SAIDA], capture_output=True, text=True,
                       check=True)
    faixas = {}
    for st, tamp, posp in csv.reader(io.StringIO(r.stdout)):
        a, b = int(posp), int(posp) + int(tamp)
        lo, hi = faixas.get(st, (a, b))
        faixas[st] = (min(lo, a), max(hi, b))
    with open(SAIDA, "r+b") as f:
        for st, (a, b) in sorted(faixas.items()):
            a, b = max(a - 2_000_000, 0), min(b + 2_000_000, tam - 1)
            print(f"   fluxo {st}: {(b - a) / 1e6:.0f} MB")
            baixar(f, a, b)
    print(SAIDA)


if __name__ == "__main__":
    main()
