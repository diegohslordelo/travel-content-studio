"""Alinhamento forçado palavra a palavra (wav2vec2 PT, CTC) sobre o texto do Whisper large-v3.

O Whisper acerta o texto, mas prende a 1ª palavra em 0,00 s e erra tempos perto de pausas; o alinhamento forçado mede
início e fim de cada palavra no áudio. Uso (de dentro de reel_gaudi/):
  python3 scripts/alinhar.py   # lê _tmp/words_large-v3.json e _tmp/wav/*.wav → transcricao_alinhada.json
"""
import json
import re
import unicodedata

import numpy as np
import soundfile as sf
import torch
import torchaudio
from scipy.signal import resample_poly
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
NUMEROS = {"1926": "mil novecentos e vinte e seis", "100": "cem"}


def normaliza(w):
    w = NUMEROS.get(re.sub(r"[^\w]", "", w), w).lower()
    return re.sub(r"[^a-záàâãéêíóôõúüç ]", "", w).strip()


def main():
    proc = Wav2Vec2Processor.from_pretrained(MODELO)
    mod = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
    voc = proc.tokenizer.get_vocab()
    sep = voc.get("|")
    tr = json.load(open("_tmp/words_large-v3.json", encoding="utf-8"))
    saida = {}
    for chave, ws in tr.items():
        nome = chave.split("/")[-1].replace(".wav", "")
        a, sr = sf.read(chave)
        x = resample_poly(a, 1, 3).astype(np.float32)  # 48 → 16 kHz
        with torch.inference_mode():
            ent = proc(x, sampling_rate=16000, return_tensors="pt").input_values
            em = torch.log_softmax(mod(ent).logits, dim=-1)
        palavras = [w[2].strip() for w in ws]
        alvo, dono = [], []
        for i, p in enumerate(palavras):
            for parte in normaliza(p).split():
                if alvo:
                    alvo.append(sep); dono.append(None)
                for ch in parte:
                    if ch in voc:
                        alvo.append(voc[ch]); dono.append(i)
        rot, pont = torchaudio.functional.forced_align(em, torch.tensor([alvo]), blank=voc[proc.tokenizer.pad_token])
        rot, pont = rot[0].tolist(), pont[0].exp().tolist()
        quadro = len(x) / 16000 / em.shape[1]
        # sequência de tokens alinhados (sem repetição de blank) → quadros de cada token do alvo
        k, ini, fim, prob = -1, {}, {}, {}
        ant = voc[proc.tokenizer.pad_token]
        for q, (r, s) in enumerate(zip(rot, pont)):
            if r != voc[proc.tokenizer.pad_token] and (r != ant or q == 0):
                k += 1
            if r != voc[proc.tokenizer.pad_token] and k >= 0:
                d = dono[k]
                if d is not None:
                    ini.setdefault(d, q); fim[d] = q + 1; prob.setdefault(d, []).append(s)
            ant = r
        saida[nome] = [{"texto": palavras[i], "ini": round(ini[i] * quadro, 3), "fim": round(fim[i] * quadro, 3),
                        "prob": round(float(np.mean(prob[i])), 3), "whisper": [ws[i][0], ws[i][1]]} for i in range(len(palavras)) if i in ini]
        print(nome, " ".join(f"{w['texto']}[{w['ini']:.2f}-{w['fim']:.2f}]" for w in saida[nome]))
    json.dump(saida, open("transcricao_alinhada.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
