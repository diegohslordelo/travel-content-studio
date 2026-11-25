#!/usr/bin/env python3
"""Baixa os brutos listados em fontes.json para fonte/<cidade>/ (fora do git). Rode de dentro da pasta do Reel."""
import json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
fontes = json.load(open(os.path.join(AQUI, "fontes.json")))
filtro = set(sys.argv[1:])
for cidade, arqs in fontes.items():
    if filtro and cidade not in filtro:
        continue
    pasta = os.path.join(AQUI, "fonte", cidade)
    os.makedirs(pasta, exist_ok=True)
    for nome, fid in arqs.items():
        dest = os.path.join(pasta, nome)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            continue
        url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
        r = subprocess.run(["curl", "-sS", "-L", "-m", "300", "-o", dest, url])
        print(cidade, nome, os.path.getsize(dest) if os.path.exists(dest) else "FALHOU", flush=True)
