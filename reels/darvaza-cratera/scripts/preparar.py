"""Decupagem: corta a voz e o vídeo do Diego nos MESMOS trechos (número inteiro de quadros a 30 qps), iguala o nível
entre tomadas pelo RMS da fala e gera, em public/: fala.mp4 (Diego, 1080 × 1920, mudo) e voz.wav (48 kHz mono, sem
loudness final); em _tmp/: trechos.json e palavras.json (palavras no tempo do Reel, a partir do Whisper large-v3).
Uso (de dentro de reels/darvaza-cratera/): python3 scripts/preparar.py"""
import json, os, subprocess
import numpy as np
import soundfile as sf

SR = 48000
d = json.load(open("edicao.json"))
FPS = d["fps"]
W = json.load(open("_tmp/words_large-v3.json"))
os.makedirs("public", exist_ok=True); os.makedirs("_tmp/clipes", exist_ok=True)


def take(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-af",
                        f"highpass=f={d['audio']['passa_alta_hz']},{d['audio']['afftdn']}", "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


pedacos, trechos, palavras, t, k = [], [], [], 0.0, 0
fade = int(d["audio"]["fade_ms"] / 1000 * SR)
for fa in d["falas"]:
    arq = f"fonte/{fa['fonte']}.mov"
    x = take(arq)
    a0, b0 = fa["trechos"][0][0], fa["trechos"][-1][1]
    nivel = rms_db(x[int(a0 * SR):int(b0 * SR)])
    # texto da fala (Whisper large-v3): todas as palavras da tomada entre a entrada e a saída; o tempo de cada palavra
    # no Reel vem do alinhamento forçado (scripts/alinhar.py), porque o Whisper erra perto de pausas
    if "texto" in fa:
        palavras += [{"fala": fa["id"], "texto": p, "prob_whisper": None} for p in fa["texto"].split()]
    else:
        palavras += [{"fala": fa["id"], "texto": w[2].strip(), "prob_whisper": w[3]} for w in W[fa["fonte"]] if w[1] > a0 + 0.03 and w[0] < b0 - 0.03]
    for a, b in fa["trechos"]:
        nq = round((b - a) * FPS)
        n = int(round(nq / FPS * SR))
        seg = x[int(round(a * SR)):int(round(a * SR)) + n].copy()
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        pedacos.append((seg, nivel))
        clip = f"_tmp/clipes/{k:02d}.mp4"
        ultimo = fa is d["falas"][-1] and (a, b) == tuple(fa["trechos"][-1])
        nqv = nq + (round(d["cauda_s"] * FPS) if ultimo else 0)  # o vídeo do último trecho continua pela cauda do CTA
        # vídeo: rotação aplicada pelo ffmpeg (iPhone, -90°), 30 qps, só os quadros do trecho
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", arq, "-t", f"{nqv / FPS:.4f}", "-an",
                        "-vf", "fps=30,scale=1080:1920,setsar=1", "-frames:v", str(nqv), "-c:v", "libx264", "-crf", "14", "-preset", "fast",
                        "-pix_fmt", "yuv420p", clip], check=True)
        trechos.append({"fala": fa["id"], "fonte": fa["fonte"], "in": a, "out": round(a + nq / FPS, 4), "inicio": round(t, 4), "quadros": nq})
        t += nq / FPS; k += 1
alvo = np.mean([n for _, n in pedacos])
voz = np.concatenate([s * 10 ** ((alvo - n) / 20) for s, n in pedacos])
cauda = np.zeros(int(d["cauda_s"] * SR))
sf.write("public/voz.wav", np.concatenate([voz, cauda]).astype(np.float32), SR, subtype="FLOAT")
with open("_tmp/clipes/lista.txt", "w") as f:
    for i in range(k): f.write(f"file '{i:02d}.mp4'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/clipes/lista.txt", "-c", "copy", "public/fala.mp4"], check=True)
json.dump(trechos, open("_tmp/trechos.json", "w"), indent=1)
json.dump(palavras, open("_tmp/texto_falas.json", "w"), ensure_ascii=False, indent=1)
print(f"voz {t:.3f} s + cauda {d['cauda_s']} s em {k} trechos")
print(" ".join(w["texto"] for w in palavras))
