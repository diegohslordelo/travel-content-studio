"""Transcrição de apoio (AUDIO_REVIEW_STANDARD 10.3, passo 2): faster-whisper large-v3-turbo, CPU int8, tempos por palavra.
Só rascunho: nada daqui é publicado sem revisão (DS V2 3.4.1; padrão 10.4).
Uso: python transcrever.py AUDIO_16K_MONO.wav SAIDA.json"""
import json, sys, time, wave
import numpy as np
from faster_whisper import WhisperModel

GLOSSARIO = ("Vlog de viagem do Diego e da Marina em Barcelona. Camp Nou, Palau Reial, Montjuïc, Barceloneta, Gràcia, "
             "Gaudí, Casa Vicens, Bairro Gótico, Catedral, Pont del Bisbe, Plaça de Sant Jaume, Plaça Reial, Palau Güell, "
             "La Rambla, La Boqueria, Plaça de Catalunya, Casa Batlló, Casa Milà, Passeig de Gràcia, Sagrada Família, "
             "Park Güell, Mercadona, El Vaso de Oro, L'Anxoveta, Momo, Eden, Xurreria Trebol, La Fàbrica, Tapa Tapa, "
             "100 Montaditos, McDonald's, Bahia, euros.")
w = wave.open(sys.argv[1])
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
m = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
t = time.time()
segs, info = m.transcribe(a, language="pt", beam_size=5, word_timestamps=True, vad_filter=True,
                          condition_on_previous_text=False, initial_prompt=GLOSSARIO)
out = []
for s in segs:
    out.append({"inicio": s.start, "fim": s.end, "texto": s.text.strip(), "avg_logprob": s.avg_logprob,
                "no_speech_prob": s.no_speech_prob, "compression_ratio": s.compression_ratio,
                "palavras": [{"i": x.start, "f": x.end, "p": x.word, "prob": x.probability} for x in s.words]})
    print(f"{s.start:8.2f} {s.text.strip()[:70]}", flush=True)
json.dump({"modelo": (sys.argv[3] if len(sys.argv) > 3 else "large-v3-turbo") + " (faster-whisper 1.2.1, int8)", "idioma": "pt", "vad": True,
           "glossario": GLOSSARIO, "segundos_cpu": round(time.time() - t), "segmentos": out},
          open(sys.argv[2], "w"), ensure_ascii=False, indent=0)
