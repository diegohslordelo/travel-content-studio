"""Alinhamento forçado (wav2vec2 PT) do texto do Whisper sobre cada tomada BRUTA, para escolher os pontos de corte.
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/alinhar_tomadas.py  → _tmp/tomadas_alinhadas.json"""
import json, re, subprocess
import numpy as np, torch, torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
proc = Wav2Vec2Processor.from_pretrained(MODELO); mod = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
voc = proc.tokenizer.get_vocab(); sep = voc.get("|"); blank = voc[proc.tokenizer.pad_token]
norm = lambda w: re.sub(r"[^a-záàâãéêíóôõúüç ]", "", w.lower()).strip()
W = json.load(open("_tmp/words_large-v3.json")); S = json.load(open("_tmp/segmentos.json"))
out = {}
for f, ws in W.items():
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", __import__("glob").glob(f"fonte/quarto/{f}.*")[0], "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, dtype=np.float32)
    segs = [s for s in S[f]["segs"] if s[1] - s[0] > 0.3]
    j0, j1 = max(0, segs[0][0] - 0.25), segs[-1][1] + 0.25
    with torch.inference_mode():
        em = torch.log_softmax(mod(proc(x[int(j0 * 16000):int(j1 * 16000)], sampling_rate=16000, return_tensors="pt").input_values).logits, dim=-1)
    alvo, dono = [], []
    for i, w in enumerate(ws):
        for parte in norm(w[2]).split():
            if alvo: alvo.append(sep); dono.append(None)
            for ch in parte:
                if ch in voc: alvo.append(voc[ch]); dono.append(i)
    rot, pont = torchaudio.functional.forced_align(em, torch.tensor([alvo]), blank=blank)
    rot, pont = rot[0].tolist(), pont[0].exp().tolist()
    q_s = (j1 - j0) / em.shape[1]; ini, fim, pr = {}, {}, {}
    k, ant = -1, blank
    for q, (r, s) in enumerate(zip(rot, pont)):
        if r != blank and (r != ant or q == 0): k += 1
        if r != blank and k >= 0 and dono[k] is not None:
            d = dono[k]; ini.setdefault(d, j0 + q * q_s); fim[d] = j0 + (q + 1) * q_s; pr.setdefault(d, []).append(s)
        ant = r
    out[f] = [[round(ini[i], 3), round(fim[i], 3), w[2].strip(), round(float(np.mean(pr[i])), 2)] for i, w in enumerate(ws)]
    print(f, " ".join(f"{a}@{s:.2f}-{e:.2f}" for s, e, a, p in out[f]))
json.dump(out, open("_tmp/tomadas_alinhadas.json", "w"), ensure_ascii=False, indent=0)
