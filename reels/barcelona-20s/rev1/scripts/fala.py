"""Etapa 1, filtro 1 — detecção de fala com dois métodos independentes.

1. Silero VAD (via faster_whisper.vad), limiar 0,5: regiões com voz.
2. Whisper small forçado em pt, es, ca e en, sem o filtro de VAD, com timestamps por palavra.
   Palavra "reconhecível" = probabilidade ≥ 0,5, com letras latinas e dentro de região Silero
   (o Whisper inventa texto em ruído; a interseção com o Silero corta isso).

Roda de dentro de reels/barcelona-20s. Saída: rev1/analise/fala.json
Uso: python3 rev1/scripts/fala.py [arquivo.wav ...]   (sem argumento: todos de _tmp/wav)
"""
import json
import os
import re
import sys

from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps

WAV = "_tmp/wav"
SR = 16000
LATINO = re.compile(r"[A-Za-zÀ-ÿ]")


def analisar(modelo, caminho):
    audio = decode_audio(caminho, sampling_rate=SR)
    regioes = [(r["start"] / SR, r["end"] / SR)
               for r in get_speech_timestamps(audio, VadOptions(threshold=0.5, min_speech_duration_ms=200))]
    def dentro(a, b):
        return any(a < r1 and b > r0 for r0, r1 in regioes)
    por_idioma = {}
    for lang in ("pt", "es", "ca", "en"):
        segs, _ = modelo.transcribe(audio, language=lang, word_timestamps=True, vad_filter=False,
                                    condition_on_previous_text=False, temperature=0.0)
        pal = []
        for sg in segs:
            for w in sg.words or []:
                if w.probability >= 0.5 and LATINO.search(w.word) and dentro(w.start, w.end):
                    pal.append({"ini": round(w.start, 2), "fim": round(w.end, 2),
                                "palavra": w.word.strip(), "prob": round(w.probability, 2)})
        por_idioma[lang] = pal
    return {"silero": [[round(a, 2), round(b, 2)] for a, b in regioes], "palavras": por_idioma,
            "duracao": round(len(audio) / SR, 2)}


def main():
    arquivos = sys.argv[1:] or sorted(f"{WAV}/{f}" for f in os.listdir(WAV))
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    saida = "rev1/analise/fala.json"
    res = json.load(open(saida)) if os.path.exists(saida) else {}
    for c in arquivos:
        b = os.path.splitext(os.path.basename(c))[0]
        res[b] = analisar(modelo, c)
        n = {k: len(v) for k, v in res[b]["palavras"].items()}
        print(b, "silero:", res[b]["silero"], "| palavras:", n, flush=True)
        json.dump(res, open(saida, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
