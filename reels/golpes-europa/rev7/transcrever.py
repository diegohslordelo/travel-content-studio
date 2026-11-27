"""Transcreve as gravações do Diego (fonte/diego) com tempo por palavra -> rev7/transcricao.json."""
import glob, json, os, subprocess
import numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
out = {}
for f in sorted(glob.glob("fonte/diego/IMG_*")):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
    words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)}
             for s in segs for w in s.words]
    out[os.path.basename(f)] = words
    print(os.path.basename(f), " ".join(x["w"] for x in words), flush=True)
json.dump(out, open("rev7/transcricao.json", "w"), ensure_ascii=False, indent=1)
