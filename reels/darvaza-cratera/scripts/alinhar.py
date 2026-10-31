"""Alinhamento forçado palavra a palavra (wav2vec2 PT, CTC) do texto do Whisper sobre a voz já decupada (public/voz.wav).
Saída: _tmp/palavras.json, com início e fim de cada palavra no tempo do Reel.
Uso (de dentro de reels/darvaza-cratera/): python3 scripts/alinhar.py"""
import json, re
import numpy as np
import soundfile as sf
import torch, torchaudio
from scipy.signal import resample_poly
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"


def normaliza(w):
    return re.sub(r"[^a-záàâãéêíóôõúüç ]", "", w.lower()).strip()


proc = Wav2Vec2Processor.from_pretrained(MODELO)
mod = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
voc = proc.tokenizer.get_vocab(); sep = voc.get("|"); blank = voc[proc.tokenizer.pad_token]
pal = json.load(open("_tmp/texto_falas.json", encoding="utf-8"))
a, sr = sf.read("public/voz.wav")
x = resample_poly(a, 1, 3).astype(np.float32)
tre = json.load(open("_tmp/trechos.json"))
edi = {f["id"]: f for f in json.load(open("edicao.json"))["falas"]}
# janelas: cada fala (ou cada trecho, quando edicao.json diz quantas palavras cabem em cada um)
janelas = []
for fid in dict.fromkeys(t["fala"] for t in tre):
    ts = [t for t in tre if t["fala"] == fid]
    idx = [i for i, p in enumerate(pal) if p["fala"] == fid]
    cortes = edi[fid].get("palavras_por_trecho")
    if cortes:
        partes, c0 = [], 0
        for c in cortes + [len(idx)]:
            partes.append(idx[c0:c]); c0 = c
        for t, ii in zip(ts, partes):
            janelas.append((t["inicio"], t["inicio"] + t["quadros"] / 30, ii))
    else:
        janelas.append((ts[0]["inicio"], ts[-1]["inicio"] + ts[-1]["quadros"] / 30, idx))
ini, fim, prob = {}, {}, {}
for j0, j1, ii in janelas:
    s0, s1 = int(max(0, j0 - 0.05) * 16000), int((j1 + 0.05) * 16000)
    with torch.inference_mode():
        em = torch.log_softmax(mod(proc(x[s0:s1], sampling_rate=16000, return_tensors="pt").input_values).logits, dim=-1)
    alvo, dono = [], []
    for i in ii:
        for parte in normaliza(pal[i]["texto"]).split():
            if alvo: alvo.append(sep); dono.append(None)
            for ch in parte:
                if ch in voc: alvo.append(voc[ch]); dono.append(i)
    rot, pont = torchaudio.functional.forced_align(em, torch.tensor([alvo]), blank=blank)
    rot, pont = rot[0].tolist(), pont[0].exp().tolist()
    q_s = (s1 - s0) / 16000 / em.shape[1]
    k, ant = -1, blank
    for q, (r, s) in enumerate(zip(rot, pont)):
        if r != blank and (r != ant or q == 0): k += 1
        if r != blank and k >= 0:
            d = dono[k]
            if d is not None:
                ini.setdefault(d, s0 / 16000 + q * q_s); fim[d] = s0 / 16000 + (q + 1) * q_s; prob.setdefault(d, []).append(s)
        ant = r
out, cont = [], {}
for i, p in enumerate(pal):
    w = dict(p, ini=round(ini[i], 3), fim=round(fim[i], 3), prob=round(float(np.mean(prob[i])), 3))
    c = (w["fala"], normaliza(w["texto"])); cont[c] = cont.get(c, 0) + 1; w["n"] = cont[c]
    out.append(w)
json.dump(out, open("_tmp/palavras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for w in out: print(f"{w['ini']:6.2f}-{w['fim']:5.2f} {w['prob']:.2f} {w['fala']:4} {w['texto']}")
