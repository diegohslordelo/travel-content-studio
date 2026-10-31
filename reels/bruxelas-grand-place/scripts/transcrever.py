"""Transcreve as tomadas do quarto com Whisper large-v3 (faster-whisper, CPU, int8), com o tempo de cada palavra.
Uso (de dentro de reels/bruxelas-grand-place/): python3 scripts/transcrever.py IMG_7518 IMG_7523 ...
Saída: _tmp/words_large-v3.json  {tomada: [[ini, fim, palavra, prob], ...]} e _tmp/texto_large-v3.txt"""
import json, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
os.makedirs("_tmp", exist_ok=True)
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
saida = "_tmp/words_large-v3.json"
W = json.load(open(saida)) if os.path.exists(saida) else {}
with open("_tmp/texto_large-v3.txt", "a") as txt:
    for f in sys.argv[1:]:
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/{f}.mov", "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        segs, info = m.transcribe(np.frombuffer(pcm, dtype=np.float32), language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                                  condition_on_previous_text=False)
        ws = []
        for s in segs:
            for w in s.words:
                ws.append([round(w.start, 3), round(w.end, 3), w.word, round(w.probability, 3)])
        W[f] = ws
        json.dump(W, open(saida, "w"), ensure_ascii=False, indent=0)
        linha = f"{f}: " + "".join(w[2] for w in ws)
        print(linha, flush=True); txt.write(linha + "\n")
