"""Alinhamento forçado palavra a palavra (wav2vec2 PT, CTC; scripts/alinhamento.py) do texto de cada bloco (edicao.json,
'texto' = a fala gravada, com as variantes e leituras decididas por scripts/cortes.py) sobre a voz já decupada
(public/voz.wav). É o tempo da legenda que acende palavra a palavra.
Uso (de dentro de reels/madrid-custo/): python3 scripts/alinhar.py
Saída: _tmp/palavras.json  [{fala, texto, ini, fim, prob}] no tempo do Reel"""
import json, os, sys
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alinhamento import PRONUNCIA, alinhar, alvo, chave, emissoes

d = json.load(open("edicao.json", encoding="utf-8"))
tre = json.load(open("_tmp/trechos.json"))
a, sr = sf.read("public/voz.wav")
x = resample_poly(a, 1, 3).astype(np.float32)  # 48 kHz → 16 kHz
saida = []
for fa in d["falas"]:
    ts = [t for t in tre if t["fala"] == fa["id"]]
    j0 = ts[0]["inicio"]; j1 = ts[-1]["inicio"] + ts[-1]["quadros"] / d["fps"]
    s0, s1 = int(max(0, j0 - 0.03) * 16000), int((j1 + 0.03) * 16000)
    em = emissoes(x[s0:s1])
    ws = fa["texto"].split()
    lei = {i: PRONUNCIA[chave(w)].index(fa["leituras"][w]) for i, w in enumerate(ws) if w in fa.get("leituras", {})}
    seq, dono = alvo(ws, lei)
    al = alinhar(em, seq, dono, len(ws), s0 / 16000, (s1 - s0) / 16000 / em.shape[1])
    for w, (t0, t1, p) in zip(ws, al):
        saida.append({"fala": fa["id"], "texto": w, "ini": round(t0, 3), "fim": round(t1, 3), "prob": round(p, 3)})
json.dump(saida, open("_tmp/palavras.json", "w"), ensure_ascii=False, indent=0)
fracas = [p for p in saida if p["prob"] < 0.5]
print(f"{len(saida)} palavras alinhadas; {len(fracas)} com probabilidade < 0,5: " + ", ".join(f"{p['texto']}({p['prob']})" for p in fracas))
for fa in d["falas"]:
    print(f"  {fa['id']}: " + " ".join(f"{w['texto']}[{w['ini']:.2f}]" for w in saida if w["fala"] == fa["id"]))
