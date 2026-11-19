"""Transcreve as narrações gravadas no quarto com Whisper large-v3 (faster-whisper, CPU, int8), com o tempo de cada palavra.
Uso (de dentro de reels/disney-atracoes/): python3 scripts/transcrever.py
Entrada: fonte/voz/voz_NN.m4a (15 blocos do roteiro, baixados do Drive: Youtube/Disney/Reel/Roteiro)
Saída: _tmp/words_large-v3.json  {bloco: [[ini, fim, palavra, prob], ...]} e _tmp/texto_large-v3.txt"""
import glob, json, os, subprocess
import numpy as np
from faster_whisper import WhisperModel

os.makedirs("_tmp", exist_ok=True)
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
W = {}
linhas = []
for f in sorted(glob.glob("fonte/voz/voz_*.m4a")):
    nome = os.path.basename(f)[:-4]
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    segs, info = m.transcribe(np.frombuffer(pcm, dtype=np.float32), language="pt", word_timestamps=True, beam_size=5,
                              vad_filter=False, condition_on_previous_text=False)
    ws = [[round(w.start, 3), round(w.end, 3), w.word, round(w.probability, 3)] for s in segs for w in s.words]
    W[nome] = ws
    linha = f"{nome}: " + "".join(w[2] for w in ws)
    print(linha, flush=True)
    linhas.append(linha)
json.dump(W, open("_tmp/words_large-v3.json", "w"), ensure_ascii=False, indent=0)
open("_tmp/texto_large-v3.txt", "w").write("\n".join(linhas) + "\n")
