"""Transcreve os brutos (faster-whisper, tempo por palavra). Rodar de dentro de reels/bahia-camp-nou/.

Saída: analise/palavras_brutos.tsv (arquivo, inicio, fim, prob, palavra) e analise/frases_brutos.md.
"""
import glob
import os
import subprocess
import sys
import wave

import numpy as np

from faster_whisper import WhisperModel

MODELO = sys.argv[1] if len(sys.argv) > 1 else "medium"
# arquivos opcionais (nomes); sem lista, transcreve todos
arquivos = [f"fonte/brutos/{n}" for n in sys.argv[2:]] or sorted(glob.glob("fonte/brutos/*.MOV"))
SUF = "_" + "_".join(n.split(".")[0] for n in sys.argv[2:]) if sys.argv[2:] else ""
m = WhisperModel(MODELO, device="cpu", compute_type="int8", cpu_threads=4)
os.makedirs("_tmp/wav16", exist_ok=True)
tsv = open(f"analise/palavras_brutos{SUF}.tsv", "w", encoding="utf-8")
tsv.write("arquivo\tinicio\tfim\tprob\tpalavra\n")
md = open(f"analise/frases_brutos{SUF}.md", "w", encoding="utf-8")
md.write(f"# Frases dos brutos (faster-whisper {MODELO}, pt)\n\n")
for a in arquivos:
    nome = os.path.basename(a)
    wav = f"_tmp/wav16/{nome}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-map", "0:a:0", "-ac", "1", "-ar", "16000", wav], check=True)
    with wave.open(wav) as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(pcm, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
    md.write(f"## {nome}\n\n")
    for s in segs:
        md.write(f"- {s.start:6.2f}–{s.end:6.2f} {s.text.strip()}\n")
        for w in s.words or []:
            tsv.write(f"{nome}\t{w.start:.2f}\t{w.end:.2f}\t{w.probability:.2f}\t{w.word.strip()}\n")
    md.write("\n")
    md.flush(); tsv.flush()
    print(nome, flush=True)
