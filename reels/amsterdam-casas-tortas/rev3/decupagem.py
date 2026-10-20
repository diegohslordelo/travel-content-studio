#!/usr/bin/env python3
"""Decupagem da fala do Diego: corta os silêncios e mantém cada palavra inteira.

Para cada trecho de fala (rev3.json, "falas"): a voz é achada pela energia em janelas de 10 ms (acima do piso
de vento + 6 dB). Toda palavra da transcrição (large-v3, tempo por palavra) tem de ficar coberta: se uma
palavra é dita baixo demais para o limiar, entra o trecho dela acima do piso + 3 dB, e, se nem isso, a
palavra inteira. Pausas maiores que 0,20 s saem; cada pedaço de voz leva 0,06 s antes e 0,10 s depois.

uso: python3 decupagem.py transcricao.json   → _tmp/decupagem.json (lista de pedaços por fala)
"""
import json
import os
import subprocess
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "..", "fonte")
ANTES, DEPOIS, PAUSA_MAX = 0.06, 0.10, 0.20


def energia(arq):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    j = 480
    n = len(x) // j
    return 20 * np.log10(np.sqrt((x[: n * j].reshape(n, j) ** 2).mean(1)) + 1e-9)


def pedacos(r, palavras, ini, fim):
    piso = float(np.percentile(r[int(ini * 100):int(fim * 100)], 10))
    voz = np.zeros(len(r), bool)
    a, b = int(ini * 100), int(fim * 100)
    voz[a:b] = r[a:b] > piso + 6
    faltou = []
    for p0, p1, w, _ in palavras:
        i0, i1 = int(p0 * 100), max(int(p0 * 100) + 1, int(p1 * 100))
        if voz[i0:i1].any():
            continue
        baixo = r[i0:i1] > piso + 3
        if baixo.any():
            voz[i0:i1] |= baixo
        else:
            voz[i0:i1] = True
        faltou.append(w)
    # intervalos de voz → pedaços com folga; pausas curtas ficam
    idx = np.nonzero(voz)[0]
    out = []
    for k in idx:
        t = k / 100
        if out and t - out[-1][1] <= PAUSA_MAX:
            out[-1][1] = t + 0.01
        else:
            out.append([t, t + 0.01])
    out = [[max(ini, s - ANTES), min(fim, e + DEPOIS)] for s, e in out if e - s >= 0.03]
    # junta pedaços que a folga encostou
    j = []
    for s, e in out:
        if j and s <= j[-1][1]:
            j[-1][1] = max(j[-1][1], e)
        else:
            j.append([s, e])
    return [[round(s, 3), round(e, 3)] for s, e in j], round(piso, 1), faltou


if __name__ == "__main__":
    T = json.load(open(sys.argv[1]))
    d = json.load(open(os.path.join(AQUI, "rev3.json")))
    cache, res = {}, []
    for f in d["falas"]:
        arq = d["fontes"][f["fonte"]]["arquivo"]
        if arq not in cache:
            cache[arq] = energia(os.path.join(FONTE, arq))
        pal = [p for s in T[arq]["large-v3"] for p in s["palavras"] if f["ini"] <= (p[0] + p[1]) / 2 < f["fim"]]
        ped, piso, faltou = pedacos(cache[arq], pal, f["ini"], f["fim"])
        # conferência: toda palavra tem de cair dentro de um pedaço (pelo menos 60% dela)
        for p0, p1, w, _ in pal:
            cob = sum(max(0, min(p1, e) - max(p0, s)) for s, e in ped)
            if cob < 0.6 * (p1 - p0) and p1 - p0 > 0.05:
                print(f"  atenção: '{w}' ({p0:.2f}–{p1:.2f}) coberta só {cob:.2f} s (fala {f['id']})")
        tot = sum(e - s for s, e in ped)
        print(f"{f['id']:10s} {f['ini']:6.2f}–{f['fim']:6.2f} → {len(ped)} pedaços, {tot:.2f} s (de {f['fim'] - f['ini']:.2f}) · piso {piso} dB"
              + (f" · palavras baixas: {' '.join(faltou)}" if faltou else ""))
        res.append({"id": f["id"], "fonte": f["fonte"], "pedacos": ped})
    os.makedirs(os.path.join(AQUI, "_tmp"), exist_ok=True)
    json.dump(res, open(os.path.join(AQUI, "_tmp", "decupagem.json"), "w"), indent=1)
