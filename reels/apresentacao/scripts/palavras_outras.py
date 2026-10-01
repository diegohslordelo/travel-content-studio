"""Tempo de cada palavra nos brutos com fala -> analise_outras/palavras_outras.tsv"""
import glob, os
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
with open("analise_outras/palavras_outras.tsv", "w") as out:
    out.write("arquivo\tinicio\tfim\tprob\tpalavra\n")
    for n in ["IMG_1375.MOV", "IMG_1384.MOV", "IMG_1393.MOV", "IMG_2170.MP4", "IMG_2693.MOV", "IMG_2730.MOV", "IMG_3134.MOV"]:
        segs, _ = m.transcribe("fonte/outras_cidades/" + n, language="pt", word_timestamps=True, vad_filter=True)
        for s in segs:
            for w in s.words:
                out.write(f"{n}\t{w.start:.2f}\t{w.end:.2f}\t{w.probability:.2f}\t{w.word.strip()}\n")
