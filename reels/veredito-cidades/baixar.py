#!/usr/bin/env python3
"""Baixa os brutos listados em fontes.json para fonte/<cidade>/ (fora do git). Rode de dentro da pasta do Reel."""
import json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
fontes = json.load(open(os.path.join(AQUI, "fontes.json")))
filtro = set(sys.argv[1:])
# Arquivos grandes de que só se usa um trecho: baixa cabeçalho, índice (moov, no fim) e o intervalo de bytes,
# num arquivo esparso do mesmo tamanho. (pasta, arquivo, tamanho total, deslocamento do moov, [início, fim] em bytes)
PARCIAIS = [("barcelona_longo", "copy_71526AEF-84EA-49ED-8F07-487197B471F9.mov", 7517714731, 7516723433, [5113691629, 6085109746])]
for cidade, arqs in fontes.items():
    if any(cidade == p[0] for p in PARCIAIS):
        continue
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


def trecho(fid, ini, fim, dest):
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    subprocess.run(["curl", "-sS", "-L", "-m", "900", "-r", f"{ini}-{fim}", "-o", dest, url], check=True)


for pasta, nome, total, moov, (a, b2) in PARCIAIS:
    if filtro and pasta not in filtro:
        continue
    dest = os.path.join(AQUI, "fonte", pasta, nome)
    if os.path.exists(dest):
        continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    fid = fontes[pasta][nome]
    with open(dest, "wb") as f:
        f.truncate(total)
        for ini, fim in [(0, 1023), (moov, total - 1), (a, b2)]:
            trecho(fid, ini, fim, dest + ".parte")
            f.seek(ini)
            with open(dest + ".parte", "rb") as p:
                f.write(p.read())
    os.remove(dest + ".parte")
    print(pasta, nome, "trecho", flush=True)
