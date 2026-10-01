"""Mede a probabilidade de música e fala (AudioSet / AST) exatamente no trecho de cada corte.

Uso: python3 musica_por_corte.py lista_de_cortes.json [inicio-fim ...]
Sem intervalos extras, mede os cortes da lista; com intervalos (s ou mm:ss), mede só eles.
"""
import os
import subprocess
import sys

import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

MODELO = "MIT/ast-finetuned-audioset-10-10-0.4593"


def audio(master, a, z):
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", master, "-vn",
                            "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(bruto, dtype=np.int16).astype(np.float32) / 32768.0


def main():
    edl = R.carregar(sys.argv[1])
    torch.set_num_threads(4)
    ext = ASTFeatureExtractor.from_pretrained(MODELO)
    mod = ASTForAudioClassification.from_pretrained(MODELO).eval()
    idx = {v: int(k) for k, v in mod.config.id2label.items()}
    if len(sys.argv) > 2:
        trechos = [(j, *(R.segundos(x) for x in j.split("-"))) for j in sys.argv[2:]]
    else:
        trechos = [(f"{i + 1:02d} {c['bloco']:<12} {c.get('rotulo', '')[:24]:<24}", c["entrada"], c["saida"])
                   for i, c in enumerate(edl["_cortes"])]
    for nome, a, z in trechos:
        x = audio(edl["master"], a, z)
        with torch.no_grad():
            p = torch.sigmoid(mod(**ext([x], sampling_rate=16000, return_tensors="pt")).logits)[0].numpy()
        top = ", ".join(f"{mod.config.id2label[int(k)]} {p[k]:.2f}" for k in np.argsort(-p)[:4])
        print(f"{nome}  música {p[idx['Music']]:.2f} | fala {p[idx['Speech']]:.2f} | {top}", flush=True)


if __name__ == "__main__":
    main()
