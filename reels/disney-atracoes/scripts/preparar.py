"""Decupagem da voz: corta cada bloco nos trechos de edicao.json (número inteiro de quadros a 30 qps), aplica passa-alta e
redução leve de ruído, iguala o nível entre blocos pelo RMS da fala e junta tudo, sem silêncio digital (o espaço entre
blocos é o tom do quarto que sobra nas pontas de cada trecho). A voz nunca é acelerada.
Uso (de dentro de reels/disney-atracoes/): python3 scripts/preparar.py
Saída: public/voz.wav (48 kHz mono, sem loudness final) e _tmp/trechos.json (onde cada trecho cai no Reel)"""
import json, os, subprocess
import numpy as np
import soundfile as sf

SR = 48000
d = json.load(open("edicao.json", encoding="utf-8"))
FPS = d["fps"]
A = d["audio"]
os.makedirs("public", exist_ok=True); os.makedirs("_tmp", exist_ok=True)


def le(fonte):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/voz/{fonte}.m4a", "-ac", "1", "-ar", str(SR), "-af",
                        f"highpass=f={A['passa_alta_hz']},{A['afftdn']}", "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


fi, fo = int(A["fade_in_ms"] / 1000 * SR), int(A["fade_out_ms"] / 1000 * SR)
pedacos, trechos, t = [], [], 0.0
for fa in d["falas"]:
    x = le(fa["fonte"])
    nivel = rms_db(np.concatenate([x[int(a * SR):int(b * SR)] for a, b in fa["trechos"]]))
    for k, (a, b) in enumerate(fa["trechos"]):
        nq = round((b - a) * FPS)
        n = int(round(nq / FPS * SR))
        seg = x[int(round(a * SR)):int(round(a * SR)) + n].copy()
        seg[:fi] *= np.linspace(0, 1, fi); seg[-fo:] *= np.linspace(1, 0, fo)
        pedacos.append((seg, nivel))
        trechos.append({"fala": fa["id"], "trecho": f"{fa['id']}.{k}", "fonte": fa["fonte"], "in": a, "out": round(a + nq / FPS, 4),
                        "inicio": round(t, 4), "quadros": nq})
        t += nq / FPS
alvo = float(np.mean([nv for _, nv in pedacos]))
voz = np.concatenate([s * 10 ** ((alvo - nv) / 20) for s, nv in pedacos])
voz = np.concatenate([voz, np.zeros(int(d["cauda_s"] * SR))])
sf.write("public/voz.wav", voz.astype(np.float32), SR, subtype="FLOAT")
json.dump(trechos, open("_tmp/trechos.json", "w"), indent=1)
print(f"voz {t:.3f} s + cauda {d['cauda_s']} s = {len(voz) / SR:.3f} s em {len(trechos)} trechos (nível alvo {alvo:.1f} dB RMS)")
for fa in d["falas"]:
    ts = [x for x in trechos if x["fala"] == fa["id"]]
    print(f"  {fa['id']} {ts[0]['inicio']:6.2f}–{ts[-1]['inicio'] + ts[-1]['quadros'] / FPS:6.2f}  {fa['texto'][:70]}")
