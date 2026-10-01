"""Transcrição com tempo por palavra (faster-whisper, word_timestamps=True) de arquivos de áudio/vídeo.
Uso: palavras_brutos.py SAIDA.tsv ARQUIVO [ARQUIVO ...]"""
import os, sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
with open(sys.argv[1], "w") as out:
    out.write("arquivo\tinicio\tfim\tprob\tpalavra\n")
    for f in sys.argv[2:]:
        segs, info = m.transcribe(f, language="pt", word_timestamps=True, vad_filter=True)
        n = 0
        for s in segs:
            for w in s.words:
                out.write(f"{os.path.basename(f)}\t{w.start:.2f}\t{w.end:.2f}\t{w.probability:.2f}\t{w.word.strip()}\n"); n += 1
        if not n:
            out.write(f"{os.path.basename(f)}\t-\t-\t-\t(sem fala)\n")
        out.flush()
