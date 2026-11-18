"""QA da voz final: (1) transcrição nova com Whisper large-v3 comparada ao texto da legenda; (2) emendas em silêncio."""
import json, subprocess, re, difflib
import numpy as np
from faster_whisper import WhisperModel

V = json.load(open("voz.json"))
a = np.frombuffer(subprocess.run("ffmpeg -v error -i reel_barcelona_3dias_rev1.mp4 -vn -ac 1 -ar 16000 -f f32le -", shell=True,
                                 capture_output=True).stdout, np.float32)
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a, language="pt", beam_size=5, condition_on_previous_text=False)
ouvido = " ".join(s.text.strip() for s in segs)
n = lambda t: re.sub(r"[^\wà-üç ]", " ", t.lower()).split()
leg = " ".join(p["w"] for p in V["palavras"])
A, B = n(leg), n(ouvido)
dif = [(op, " ".join(A[i1:i2]), " ".join(B[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B).get_opcodes() if op != "equal"]
# emendas: energia nos 20 ms antes e depois de cada junção da voz (no arquivo final, antes da master)
x = np.frombuffer(subprocess.run("ffmpeg -v error -i public/voz.wav -ac 1 -ar 48000 -f f32le -", shell=True, capture_output=True).stdout, np.float32)
db = lambda s: 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)
emendas = []
for c in V["cortes"]:
    for t in (c["ini"], c["fim"]):
        if 0 < t < V["dur"] - 0.01:
            i = int(t * 48000)
            emendas.append((round(t, 2), round(float(db(x[max(0, i - 960):i])), 1), round(float(db(x[i:i + 960])), 1)))
json.dump({"ouvido": ouvido, "diferencas": dif, "emendas": emendas}, open("qa_voz.json", "w"), ensure_ascii=False, indent=1)
print("OUVIDO:", ouvido)
print("DIFERENÇAS legenda × ouvido:", dif)
print("EMENDAS (t, dB antes, dB depois):", emendas)
print("pior emenda:", max(max(e[1], e[2]) for e in emendas))
