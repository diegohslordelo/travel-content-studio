"""Tempo de cada palavra na voz final (Whisper large-v3 sobre public/voz_bruta.wav), com início refinado pela energia
(120–4000 Hz) quando a palavra vem depois de silêncio. Uso: python3 scripts/alinhar.py rev1"""
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
rev = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "public/voz_bruta.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.float32).copy()
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a, language="pt", word_timestamps=True, beam_size=5, initial_prompt="Bruges, Porto da Barra, Salvador, bate e volta, Bélgica.")
ws = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]
# energia em 10 ms
f = subprocess.run(["ffmpeg", "-v", "error", "-i", "public/voz_bruta.wav", "-ac", "1", "-ar", "16000", "-af", "highpass=f=120,lowpass=f=4000", "-f", "f32le", "-"], capture_output=True).stdout
b = np.frombuffer(f, np.float32); hop = 160; n = len(b) // hop
db = 20 * np.log10(np.sqrt(np.mean(b[: n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
lim = np.percentile(db, 90) - 28
for i, w in enumerate(ws):
    # se a palavra começa num trecho de silêncio, empurra o início até a voz começar
    k = int(w["s"] * 100)
    while k < min(n - 1, int(w["e"] * 100)) and db[k] < lim:
        k += 1
    w["s"] = round(max(w["s"], k / 100), 3)
json.dump(ws, open(f"{rev}/transcricao_alinhada.json", "w"), ensure_ascii=False, indent=1)
print(" ".join(f"{w['w']}@{w['s']:.2f}" for w in ws))
