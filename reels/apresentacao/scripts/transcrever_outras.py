"""Transcreve os brutos das outras cidades (idioma detectado por arquivo) -> analise_outras/transcricao_outras.tsv"""
import glob, os
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
with open("analise_outras/transcricao_outras.tsv", "w") as out:
    out.write("arquivo\tidioma\tprob_idioma\tinicio\tfim\ttexto\n")
    for f in sorted(glob.glob("fonte/outras_cidades/*")):
        segs, info = m.transcribe(f, vad_filter=True, word_timestamps=False)
        segs = list(segs)
        if not segs:
            out.write(f"{os.path.basename(f)}\t{info.language}\t{info.language_probability:.2f}\t-\t-\t(sem fala)\n")
        for s in segs:
            out.write(f"{os.path.basename(f)}\t{info.language}\t{info.language_probability:.2f}\t{s.start:.2f}\t{s.end:.2f}\t{s.text.strip()}\n")
        out.flush()
