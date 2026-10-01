"""Procura trechos de som ambiente limpo (sem fala e sem música) nas pausas entre falas.

Usa as marcas de tempo por palavra da transcrição e confirma cada pausa com o classificador AudioSet.
Uso: python3 achar_ambiente.py MASTER transcricao_palavras.tsv classes_audio_4s.tsv SAIDA.tsv
"""
import csv
import subprocess
import sys

import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

MODELO = "MIT/ast-finetuned-audioset-10-10-0.4593"
PAUSA_MIN = 0.9   # s entre o fim de uma palavra e o início da próxima
FOLGA = 0.15      # s descartados de cada lado da pausa


def main():
    master, arq_pal, arq_cls, saida = sys.argv[1:5]
    palavras = [(float(r["inicio"]), float(r["fim"])) for r in csv.DictReader(open(arq_pal), delimiter="\t")]
    janelas = [(float(r["inicio"]), float(r["fim"]), float(r["Music"]))
               for r in csv.DictReader(open(arq_cls), delimiter="\t")]

    def musica_janela(a, z):
        return max((m for ja, jz, m in janelas if ja < z and jz > a), default=1.0)

    candidatos = []
    for (a0, z0), (a1, _) in zip(palavras, palavras[1:]):
        a, z = z0 + FOLGA, a1 - FOLGA
        if z - a >= PAUSA_MIN - 2 * FOLGA and musica_janela(a, z) < 0.25:
            candidatos.append((a, z))
    print(f"{len(candidatos)} pausas candidatas", flush=True)
    torch.set_num_threads(4)
    ext = ASTFeatureExtractor.from_pretrained(MODELO)
    mod = ASTForAudioClassification.from_pretrained(MODELO).eval()
    idx = {v: int(k) for k, v in mod.config.id2label.items()}
    with open(saida, "w") as f:
        f.write("inicio\tfim\tdur\tmusica\tfala\tinterior\texterior\ttop\n")
        for a, z in candidatos:
            bruto = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", master,
                                    "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                                   capture_output=True, check=True).stdout
            x = np.frombuffer(bruto, dtype=np.int16).astype(np.float32) / 32768.0
            with torch.no_grad():
                p = torch.sigmoid(mod(**ext([x], sampling_rate=16000, return_tensors="pt")).logits)[0].numpy()
            interior = max(p[idx["Inside, small room"]], p[idx["Inside, large room or hall"]], p[idx["Inside, public space"]])
            exterior = max(p[idx["Outside, urban or manmade"]], p[idx["Vehicle"]], p[idx["Traffic noise, roadway noise"]])
            top = "; ".join(f"{mod.config.id2label[int(k)]} {p[k]:.2f}" for k in np.argsort(-p)[:4])
            f.write(f"{a:.2f}\t{z:.2f}\t{z - a:.2f}\t{p[idx['Music']]:.3f}\t{p[idx['Speech']]:.3f}\t"
                    f"{interior:.3f}\t{exterior:.3f}\t{top}\n")
            f.flush()
    print("ok", flush=True)


if __name__ == "__main__":
    main()
