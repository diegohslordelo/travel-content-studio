"""Hora real de cada fala do vídeo editado: casa cada segmento da transcrição nova (large-v3) com as falas do
acervo (`acervo/amsterdam/transcricoes.tsv`, faster-whisper small) e soma o início da fala no clipe à hora do
arquivo (`indice.tsv`, "criado"). A hora é a do arquivo (fuso local); a casa por texto pode errar em falas
curtas, por isso só vale com similaridade ≥ 0,55 e mais de 4 palavras.
Uso (de reels/ams-yt): python scripts/horarios.py _tmp/transcricao.json _tmp/horarios.json"""
import csv
import difflib
import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta

ACERVO = "../../acervo/amsterdam"


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


criado = {}
with open(f"{ACERVO}/indice.tsv", encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r["criado"]:
            criado[r["arquivo"]] = datetime.fromisoformat(r["criado"])
falas = []
with open(f"{ACERVO}/transcricoes.tsv", encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        if r["arquivo"] in criado:
            falas.append((r["arquivo"], float(r["inicio_s"]), norm(r["texto"])))

segs = json.load(open(sys.argv[1], encoding="utf-8"))["segmentos"]
out = []
for s in segs:
    w = norm(s["texto"])
    if len(w) < 4:
        continue
    melhor = (0, None)
    for arq, ini, fw in falas:
        if not fw:
            continue
        r = difflib.SequenceMatcher(None, w, fw).ratio()
        if r > melhor[0]:
            melhor = (r, (arq, ini))
    if melhor[0] >= 0.55:
        arq, ini = melhor[1]
        hora = criado[arq] + timedelta(seconds=ini)
        out.append({"t": s["ini"], "texto": s["texto"], "arquivo": arq, "sim": round(melhor[0], 2), "hora": hora.strftime("%Y-%m-%d %H:%M:%S")})
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for o in out:
    print(f"{o['t']:8.1f}  {o['hora']}  {o['arquivo']:<14} {o['sim']:.2f}  {o['texto'][:70]}")
