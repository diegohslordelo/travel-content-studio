# Transcreve trechos do bruto isoladamente (para conferir lacunas e tomadas). Uso: python3 scripts/trecho.py ini-fim [ini-fim...]
import sys, wave
import numpy as np
from faster_whisper import WhisperModel
w = wave.open("_tmp/audio16k.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
for arg in sys.argv[1:]:
    i, f = map(float, arg.split("-"))
    segs, _ = m.transcribe(a[int(i*16000):int(f*16000)], language="pt", word_timestamps=True, condition_on_previous_text=False, vad_filter=False)
    print(f"== {arg}")
    for s in segs:
        print("  ", " ".join(f"{x.word.strip()}({x.start+i:.2f}-{x.end+i:.2f})" for x in s.words), flush=True)
