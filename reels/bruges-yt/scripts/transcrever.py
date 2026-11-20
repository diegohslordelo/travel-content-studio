"""Transcrição palavra a palavra (faster-whisper large-v3, CPU int8) do vídeo sem música.
Roda de reels/bruges-yt:  python scripts/transcrever.py _tmp/voz16k.wav _tmp/transcricao.json
A transcrição é automática: serve de base para decupagem e .srt; a validação auditiva é humana."""
import json
import sys
import time

import soundfile as sf

from faster_whisper import WhisperModel

entrada, saida = sys.argv[1], sys.argv[2]
modelo = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
prompt = (
    "Vlog de viagem em Bruges, na Bélgica, bate-volta de Bruxelas, em português do Brasil. Diego e Marina. "
    "Estação de trem, SNCB, bilhete de trem, Brugge, Markt, Belfort, torre do Belfort, Burg, prefeitura, "
    "Basílica do Sangue Sagrado, Basilica of the Holy Blood, relíquia, sangue de Cristo, canais, Rozenhoedkaai, "
    "Chez Albert, waffle, House of Waffles, waffle no palito, Gofre Belgian Waffles, batata frita, fritas, "
    "Minnewater, Lago do Amor, Begijnhof, Onze-Lieve-Vrouwekerk, chocolate belga, cerveja, McDonald's, euros."
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
