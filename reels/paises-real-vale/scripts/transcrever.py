# Transcreve o bruto (Whisper large-v3, PT) com tempo por palavra. Roda de dentro da pasta do Reel.
import json, sys, wave
import numpy as np
from faster_whisper import WhisperModel
modelo = sys.argv[1] if len(sys.argv) > 1 else "large-v3"
m = WhisperModel(modelo, device="cpu", compute_type="int8", cpu_threads=4)
w = wave.open("_tmp/audio16k.wav")
audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
segs, info = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False,
                          condition_on_previous_text=False, beam_size=5,
                          initial_prompt="Vietnã, Tailândia, Egito, dong, baht, koshari, IOF, dólar, euro, milionário.")
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text,
                "words": [{"w": w.word, "s": w.start, "e": w.end, "p": w.probability} for w in s.words]})
    print(f"{s.start:7.2f}-{s.end:7.2f} {s.text}", flush=True)
json.dump(out, open(f"_tmp/transcricao_{modelo}.json", "w"), ensure_ascii=False, indent=1)
