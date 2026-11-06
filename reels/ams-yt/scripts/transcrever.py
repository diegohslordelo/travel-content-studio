"""Transcrição palavra a palavra (faster-whisper large-v3, CPU int8) do vídeo sem música.
Roda de reels/ams-yt:  python scripts/transcrever.py _tmp/voz16k.wav _tmp/transcricao.json
A transcrição é automática: serve de base para decupagem e .srt; a validação auditiva é humana."""
import json
import sys
import time

import soundfile as sf

from faster_whisper import WhisperModel

entrada, saida = sys.argv[1], sys.argv[2]
modelo = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
prompt = (
    "Vlog de viagem em Amsterdam, em português do Brasil. Diego e Marina. Hotel XO Inner, Museumplein, "
    "Dancing Houses, New York Pizza, Praça Dam, Manneken Pis, Tony's Chocolonely, Kalverstraat, "
    "Van Wonderen Stroopwafels, The Old Bell, Red Light District, McDonald's, McCrispy, Anne Frank, "
    "Albert Cuyp Market, Benny's Chicken, Rudi's Original Stroopwafels, Rijksmuseum, Van Gogh Museum, "
    "Moco Museum, Vondelpark, Fabel Friet, Jordaan, Het Molentje, Pizza Beppe, Albert Heijn, "
    "Sarphatipark, De Pijp, FEBO, O'Donnell's, Heineken Experience, stroopwafel, euros."
)
t0 = time.time()
audio, sr = sf.read(entrada, dtype="float32")
assert sr == 16000
segs, info = modelo.transcribe(
    audio,
    language="pt",
    beam_size=5,
    word_timestamps=True,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 300, "speech_pad_ms": 200},
    initial_prompt=prompt,
    condition_on_previous_text=False,
)
out = []
for s in segs:
    out.append({
        "ini": round(s.start, 3), "fim": round(s.end, 3), "texto": s.text.strip(),
        "conf": round(s.avg_logprob, 3), "sem_fala": round(s.no_speech_prob, 3),
        "palavras": [{"p": w.word.strip(), "ini": round(w.start, 3), "fim": round(w.end, 3), "prob": round(w.probability, 3)} for w in s.words],
    })
    print(f"{s.start:8.2f} {s.end:8.2f} {s.text.strip()}", flush=True)
    with open(saida, "w", encoding="utf-8") as f:
        json.dump({"modelo": "faster-whisper large-v3 int8 beam5", "segundos": round(time.time() - t0), "segmentos": out}, f, ensure_ascii=False, indent=1)
print("FIM", round(time.time() - t0), "s", flush=True)
