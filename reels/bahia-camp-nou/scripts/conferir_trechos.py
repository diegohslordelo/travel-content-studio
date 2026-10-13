"""Confere falas curtas dos brutos com o faster-whisper large-v3 (áudio cru, faixa 0). Rodar de reels/bahia-camp-nou/.

Uso: python3 scripts/conferir_trechos.py ARQ:INI:FIM [ARQ:INI:FIM ...]
"""
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
for spec in sys.argv[1:]:
    arq, a, b = spec.split(":")
    pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", a, "-to", b, "-i", f"fonte/brutos/{arq}", "-map", "0:a:0",
                                        "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout,
                        np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(pcm, language="pt", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    pal = [f"{float(a) + w.start:.2f}:{w.word.strip()}({w.probability:.2f})" for s in segs for w in (s.words or [])]
    print(f"{spec}  →  {' '.join(pal)}", flush=True)
