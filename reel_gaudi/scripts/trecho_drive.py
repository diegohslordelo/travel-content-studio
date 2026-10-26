"""Baixa do Google Drive só um trecho de um vídeo grande (cópia local esparsa: índice moov + bytes do trecho).

Mesma técnica de reels/agua-barcelona/rev5/scripts/baixar_trecho_master.py (branch claude/reel-agua-barcelona).
Uso (de dentro de reel_gaudi/):
  python3 scripts/trecho_drive.py <drive_id> <saida.mov> [t0 t1]   # sem t0/t1: só o índice (para o ffprobe)
O ffmpeg lê a cópia como se fosse o arquivo inteiro, desde que só peça tempos dentro dos trechos baixados.
"""
import csv
import io
import os
import struct
import subprocess
import sys
import time
import urllib.request

BLOCO = 8 * 1024 * 1024


def intervalo(url, a, b):
    for tentativa in range(6):
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"}), timeout=300)
        d = r.read()
        if r.status == 206 and len(d) == b - a + 1:
            return d
        print(f"   resposta inesperada ({r.status}, {len(d)} bytes); nova tentativa")
        time.sleep(10 * (tentativa + 1))
    raise RuntimeError("o Drive não entregou o intervalo pedido")


def tamanho(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=0-0"}), timeout=60)
    return int(r.headers["Content-Range"].split("/")[1])


def main():
    did, saida = sys.argv[1], sys.argv[2]
    url = f"https://drive.usercontent.google.com/download?id={did}&export=download&confirm=t"
    tam = tamanho(url)
    if not os.path.exists(saida) or os.path.getsize(saida) != tam:
        with open(saida, "wb") as f:
            f.truncate(tam)
            pos = 0
            while pos < tam:  # átomos de primeiro nível: guarda ftyp e moov
                h = intervalo(url, pos, pos + 15)
                sz, tipo = struct.unpack(">I4s", h[:8])
                sz = struct.unpack(">Q", h[8:16])[0] if sz == 1 else (tam - pos if sz == 0 else sz)
                f.seek(pos)
                f.write(h)  # cabeçalho de todo átomo (o mdat de 64 bits precisa dele para o ffprobe achar o moov)
                if tipo in (b"ftyp", b"moov"):
                    f.seek(pos)
                    f.write(intervalo(url, pos, pos + sz - 1))
                pos += sz
    if len(sys.argv) < 5:
        print(saida, tam)
        return
    t0, t1 = sys.argv[3], sys.argv[4]
    r = subprocess.run(["ffprobe", "-v", "error", "-read_intervals", f"{t0}%{t1}", "-show_entries", "packet=stream_index,pos,size",
                        "-of", "csv=p=0", saida], capture_output=True, text=True, check=True)
    faixas = {}
    for st, tp, pp in csv.reader(io.StringIO(r.stdout)):
        if pp == "N/A":
            continue
        a, b = int(pp), int(pp) + int(tp)
        lo, hi = faixas.get(st, (a, b))
        faixas[st] = (min(lo, a), max(hi, b))
    with open(saida, "r+b") as f:
        for st, (a, b) in sorted(faixas.items()):
            a, b = max(a - 2_000_000, 0), min(b + 2_000_000, tam - 1)
            print(f"   fluxo {st}: {(b - a) / 1e6:.0f} MB")
            p = a
            while p <= b:
                q = min(p + BLOCO - 1, b)
                f.seek(p)
                f.write(intervalo(url, p, q))
                p = q + 1
    print(saida)


if __name__ == "__main__":
    main()
