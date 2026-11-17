"""Transcrição da gravação (Whisper large-v3, PT, palavra a palavra) → transcricao.json."""
import json
from faster_whisper import WhisperModel

from faster_whisper.audio import decode_audio
import wave, numpy as np
w=wave.open("voz16k.wav"); audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False,
                          initial_prompt="Viagem, Europa, orçamento, restaurante, supermercado, café da manhã, euros.")
out = []
for s in segs:
    out.append({"s": s.start, "e": s.end, "txt": s.text, "w": [(w.word, round(w.start, 2), round(w.end, 2), round(w.probability, 2)) for w in s.words]})
    print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}", flush=True)
json.dump(out, open("transcricao.json", "w"), ensure_ascii=False, indent=0)
