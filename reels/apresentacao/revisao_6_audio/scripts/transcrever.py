import sys, json
from faster_whisper import WhisperModel
arq, saida = sys.argv[1], sys.argv[2]
modelo = sys.argv[3] if len(sys.argv) > 3 else "medium"
m = WhisperModel(modelo, device="cpu", compute_type="int8")
segs, _ = m.transcribe(arq, language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                       condition_on_previous_text=False)
pal = []
for s in segs:
    for w in s.words:
        pal.append({"t0": round(w.start, 3), "t1": round(w.end, 3), "p": round(w.probability, 3), "w": w.word.strip()})
json.dump(pal, open(saida, "w"), ensure_ascii=False, indent=0)
print(" ".join(p["w"] for p in pal))
