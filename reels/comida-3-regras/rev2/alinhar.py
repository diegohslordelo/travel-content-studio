"""Alinhamento forçado palavra a palavra (wav2vec2 PT + CTC), FORMATOS_REELS 7.2.

alinhar(audio16k, texto_falado) → [(palavra, início, fim)] em segundos relativos ao trecho.
Viterbi CTC em numpy (trellis do tutorial do torchaudio), quadro de 20 ms.
"""
import re
import unicodedata

import numpy as np

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
_m = None


def _modelo():
    global _m
    if _m is None:
        import torch
        from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
        torch.set_num_threads(4)
        p = Wav2Vec2Processor.from_pretrained(MODELO)
        m = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
        _m = (p, m, torch)
    return _m


def normaliza(w):
    w = unicodedata.normalize("NFC", w.lower())
    return re.sub(r"[^a-zà-üç'\-]", "", w)


def alinhar(audio, palavras):
    proc, mod, torch = _modelo()
    voc = proc.tokenizer.get_vocab()
    blank = voc["<pad>"]
    with torch.inference_mode():
        x = proc(audio, sampling_rate=16000, return_tensors="pt").input_values
        em = torch.log_softmax(mod(x).logits[0], -1).numpy()
    T = em.shape[0]
    dt = len(audio) / 16000 / T
    # token e índice da palavra (-1 = separador); separador também no começo e no fim: o modelo emite "|"
    # no silêncio das bordas, e sem ele a última letra "comia" o silêncio até o fim do trecho
    toks, dono = [voc["|"]], [-1]
    for k, w in enumerate(palavras):
        if k:
            toks.append(voc["|"]); dono.append(-1)
        for ch in normaliza(w):
            toks.append(voc[ch]); dono.append(k)
    toks.append(voc["|"]); dono.append(-1)
    N = len(toks)
    tr = np.full((T + 1, N + 1), -np.inf)
    tr[0, 0] = 0
    for t in range(T):
        tr[t + 1, 0] = tr[t, 0] + em[t, blank]
        fica = tr[t, 1:] + np.maximum(em[t, blank], em[t, toks])
        anda = tr[t, :-1] + em[t, toks]
        tr[t + 1, 1:] = np.maximum(fica, anda)
    # volta pelo caminho
    j, ini, fim = N, [None] * N, [None] * N
    for t in range(T, 0, -1):
        if j == 0:
            break
        anda = tr[t - 1, j - 1] + em[t - 1, toks[j - 1]]
        fica = tr[t - 1, j] + max(em[t - 1, blank], em[t - 1, toks[j - 1]])
        emite = anda >= fica or em[t - 1, toks[j - 1]] > np.log(0.3)
        if fim[j - 1] is None and emite:  # fim = último quadro em que a letra foi emitida (não conta o silêncio)
            fim[j - 1] = t
        if anda >= fica:
            ini[j - 1] = t - 1
            j -= 1
    out = []
    for k, w in enumerate(palavras):
        idx = [i for i in range(N) if dono[i] == k]
        out.append((w, ini[idx[0]] * dt, fim[idx[-1]] * dt))
    return out
