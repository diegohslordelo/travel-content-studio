#!/usr/bin/env python3
"""Tremor de cada plano de rev3.json, medido no bruto com o recorte do Reel (../../_ferramentas/tremor.py).

Para cada plano: o tremor no trecho usado hoje (a partir de `in`) e o trecho mais estável do bruto com a mesma
duração. Rode depois de `python3 rev3.py tempos`.

uso: python3 tremor_planos.py            # todos os planos
     python3 tremor_planos.py IMG_4367 3.0 1.5 1650   # um bruto: fonte, in (ignorado), duração, recorte_x
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_ferramentas"))
import rev3  # noqa: E402
from tremor import LIMITE_PICO, LIMITE_RMS, tremor  # noqa: E402


def filtro(d, fonte, recorte_x):
    f = d["fontes"][fonte]
    src = os.path.join(rev3.RAIZ, d["pasta_brutos"], f["arquivo"])
    vf = []
    if f["girar"] != "auto":
        corr = (f["girar"] + rev3.rotacao_meta(src)) % 360
        vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[corr])
    w0, h0 = rev3.sonda(src)
    giro = rev3.rotacao_meta(src) if f["girar"] == "auto" else f["girar"]
    larg, alt = (w0, h0) if giro % 180 == 0 else (h0, w0)
    if recorte_x is not None and larg > alt:
        vf.append(f"crop={round(alt * 9 / 16 / 2) * 2}:{alt}:{recorte_x}:0")
    else:
        vf.append("null")
    return src, ",".join(vf)


def duracoes(d):
    tm = json.load(open(os.path.join(rev3.TMP, "tempos.json"), encoding="utf-8"))
    ft = {f["id"]: f for f in tm["falas"]}
    ids = [f["id"] for f in d["falas"]]
    fim_total = tm["fim_narracao"] + d["narracao"]["cauda"]
    blocos = []
    for fi, f in enumerate(d["falas"]):
        ini = 0.0 if fi == 0 else ft[f["id"]]["palavras"][0]["ini"] - rev3.PRE_CORTE
        fim = fim_total if fi == len(ids) - 1 else ft[ids[fi + 1]]["palavras"][0]["ini"] - rev3.PRE_CORTE
        for pi, t in enumerate(rev3.inicios_planos(f, ft[f["id"]], ini, fim)):
            blocos.append([f, pi, t])
    for i, b in enumerate(blocos):
        lim = b[0]["planos"][b[1]].get("dur_max")
        prox = blocos[i + 1][2] if i + 1 < len(blocos) else fim_total
        if lim and prox - b[2] > lim:
            blocos[i + 1][2] = b[2] + lim
    return [(f, pi, (blocos[i + 1][2] if i + 1 < len(blocos) else fim_total) - t) for i, (f, pi, t) in enumerate(blocos)]


if __name__ == "__main__":
    d = rev3.carregar()
    if len(sys.argv) > 1:
        fonte, _, dur, rx = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
        src, vf = filtro(d, fonte, None if rx == "-" else int(rx))
        r = tremor(src, janela=dur, filtro=vf)
        print(f"{fonte} todo: rms {r['rms']} · melhor {r.get('melhor')}")
        sys.exit()
    for f, pi, dur in duracoes(d):
        p = f["planos"][pi]
        cid = f"{f['id']}_{pi + 1}"
        if "fonte" not in p or d["fontes"][p["fonte"]].get("foto"):
            print(f"{cid:16s} foto/congelado")
            continue
        rx = p.get("recorte_x", [[0, None]])[0][1]
        src, vf = filtro(d, p["fonte"], rx)
        r = tremor(src, janela=dur, filtro=vf)
        fps = 1 / (r["dur"] / (len(r["rms_janelas"]) + round(dur * 30)))  # aproximado
        i_in = min(len(r["rms_janelas"]) - 1, round(p["in"] * len(r["rms_janelas"]) / max(0.01, r["dur"] - dur)))
        atual = r["rms_janelas"][i_in] if r.get("rms_janelas") else None
        alerta = "TREMIDO" if atual is None or atual > LIMITE_RMS else "ok     "
        print(f"{alerta} {cid:16s} {p['fonte']} in {p['in']:5.2f} dur {dur:4.2f} · rms atual {atual} · melhor {r.get('melhor')}", flush=True)
