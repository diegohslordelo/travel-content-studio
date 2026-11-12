"""Transcrição palavra a palavra da gravação do Diego (Whisper large-v3, faster-whisper, CPU int8).
Uso: python3 scripts/transcrever.py <wav16k> <saida.json>  (rodar de dentro de reels/gta6-miami)"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

wav, saida = sys.argv[1], sys.argv[2]
# PyAV desta máquina não aceita a leitura do faster-whisper: o áudio é lido pelo ffmpeg (16 kHz mono float32)
audio = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout, np.float32)
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(audio, language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                          condition_on_previous_text=False)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for w in s.words]})
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}", flush=True)
json.dump(out, open(saida, "w"), ensure_ascii=False, indent=1)
