"""Confere e corrige os timestamps da imagem de um vídeo juntado por partes (sem recodificar).

No render 4K da REV3 (07/11/2026), a parte 14, montada de 4 pedaços (SUBPARTES=4, depois de o container reiniciar
no meio de partes), entrou no vídeo juntado com +3.780 tiques (42 ms, base 1/90000): todos os quadros dali em diante
ficaram 42 ms atrasados em relação ao som. Os quadros estavam todos lá; só os timestamps estavam errados.

Este script ordena os quadros pela apresentação (o quadro i deve estar em i / fps), acha os trechos de pacotes
(em ordem de decodificação) com o mesmo desvio e, se houver desvio, reescreve pts e dts com o bitstream filter `setts`
(cópia dos pacotes, sem recodificar). Termina com erro se sobrar desvio ou se o número de quadros não bater.

  python rev3/corrigir_ts_video.py <video.mp4> <fps> <quadros_esperados>
"""
import json
import os
import subprocess
import sys


def pacotes(arq):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=time_base:packet=pts,dts",
                          "-of", "json", arq], check=True, capture_output=True, text=True).stdout
    j = json.loads(out)
    num, den = map(int, j["streams"][0]["time_base"].split("/"))
    return [(int(p["pts"]), int(p["dts"])) for p in j["packets"]], num, den


def desvios(pk, fps, num, den):
    tick = den / (num * fps)
    assert abs(tick - round(tick)) < 1e-9, f"base de tempo {num}/{den} não divide 1/{fps}"
    tick = round(tick)
    ordem = sorted(range(len(pk)), key=lambda j: pk[j][0])
    d = [0] * len(pk)
    for i, j in enumerate(ordem):
        d[j] = i * tick - pk[j][0]
    return d


def main():
    arq, fps, esperado = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    pk, num, den = pacotes(arq)
    if len(pk) != esperado:
        sys.exit(f"{arq}: {len(pk)} quadros, esperado {esperado}")
    d = desvios(pk, fps, num, den)
    if not any(d):
        print(f"timestamps ok ({len(pk)} quadros em i / {fps})")
        return
    # trechos de pacotes (ordem de decodificação) com desvio constante; o B-frame reordena dentro do GOP, então o
    # desvio só pode mudar num quadro-chave da emenda
    trechos, ini = [], 0
    for j in range(1, len(d) + 1):
        if j == len(d) or d[j] != d[ini]:
            trechos.append((ini, d[ini]))
            ini = j
    print("desvios (pacote inicial, tiques):", [(a, x) for a, x in trechos if x])
    expr = "0"
    for a, x in trechos:  # o trecho mais tardio que já começou vale (inclusive os de desvio 0 depois de um desvio)
        expr = f"if(gte(N\\,{a})\\,{x}\\,{expr})"
    tmp = arq + ".ts.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", arq, "-map", "0", "-c", "copy",
                    "-bsf:v", f"setts=pts=PTS+{expr}:dts=DTS+{expr}", "-movflags", "+faststart", tmp], check=True)
    pk2, num, den = pacotes(tmp)
    if len(pk2) != esperado or any(desvios(pk2, fps, num, den)):
        os.remove(tmp)
        sys.exit("a correção não zerou o desvio")
    os.replace(tmp, arq)
    print(f"timestamps corrigidos ({len(pk2)} quadros em i / {fps})")


if __name__ == "__main__":
    main()
