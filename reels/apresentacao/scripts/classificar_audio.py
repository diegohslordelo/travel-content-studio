"""Classifica o áudio do vídeo em janelas (AudioSet / AST) para achar música, fala e sons de cena.

Uso: python3 classificar_audio.py AUDIO_16K_MONO.wav SAIDA.tsv [janela_s] [passo_s]
"""
import sys
import wave

import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

MODELO = "MIT/ast-finetuned-audioset-10-10-0.4593"
ROTULOS = [
    "Music", "Speech", "Singing", "Musical instrument", "Vehicle", "Train", "Rail transport",
    "Subway, metro, underground", "Aircraft", "Fixed-wing aircraft, airplane", "Car", "Bus",
    "Traffic noise, roadway noise", "Wind noise (microphone)", "Crowd", "Chatter", "Walk, footsteps",
    "Waves, surf", "Ocean", "Laughter", "Dishes, pots, and pans", "Cutlery, silverware",
    "Inside, small room", "Inside, public space", "Outside, urban or manmade", "Bird", "Bell",
]


def main():
    entrada, saida = sys.argv[1], sys.argv[2]
    janela = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    passo = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    torch.set_num_threads(4)
    with wave.open(entrada) as w:
        sr = w.getframerate()
        audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    assert sr == 16000
    extrator = ASTFeatureExtractor.from_pretrained(MODELO)
    modelo = ASTForAudioClassification.from_pretrained(MODELO).eval()
    id2label = modelo.config.id2label
    idx = {v: int(k) for k, v in id2label.items()}
    faltando = [r for r in ROTULOS if r not in idx]
    if faltando:
        print("rótulos inexistentes:", faltando, file=sys.stderr)
    rotulos = [r for r in ROTULOS if r in idx]
    n_jan = int(janela * sr)
    inicios = np.arange(0, max(1, len(audio) - n_jan // 2), int(passo * sr))
    with open(saida, "w") as f:
        f.write("inicio\tfim\t" + "\t".join(rotulos) + "\ttop5\n")
        lote = 8
        for i in range(0, len(inicios), lote):
            trechos = [audio[s:s + n_jan] for s in inicios[i:i + lote]]
            feats = extrator(trechos, sampling_rate=sr, return_tensors="pt")
            with torch.no_grad():
                prob = torch.sigmoid(modelo(**feats).logits).numpy()
            for s, p in zip(inicios[i:i + lote], prob):
                top = np.argsort(-p)[:5]
                top5 = "; ".join(f"{id2label[int(k)]} {p[k]:.2f}" for k in top)
                f.write(f"{s / sr:.1f}\t{(s + n_jan) / sr:.1f}\t" + "\t".join(f"{p[idx[r]]:.3f}" for r in rotulos) + f"\t{top5}\n")
            f.flush()
            print(f"{inicios[min(i + lote, len(inicios)) - 1] / sr:.0f}s", end=" ", flush=True)
    print("\nok")


if __name__ == "__main__":
    main()
