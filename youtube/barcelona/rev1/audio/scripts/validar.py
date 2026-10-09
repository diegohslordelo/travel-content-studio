"""Validação técnica do áudio tratado contra o original (AUDIO_REVIEW_STANDARD 8.1, 9.3, 11.3). Só medição.
Uso: python3 rev1/audio/scripts/validar.py ORIGINAL.flac TRATADO.m4a DIAGNOSTICO.json SRT_APOIO SAIDA.json"""
import json, re, subprocess, sys
import numpy as np
orig, trat, diag, srt, saida = sys.argv[1:6]
SR = 44100
dec = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],  # noqa: E731
                                             capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)
a, b = dec(orig), dec(trat)
n = min(len(a), len(b)); a, b = a[:n], b[:n]
D = json.load(open(diag))
txt = open(srt, encoding="utf-8").read()
s = lambda v: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*v.split(":"))  # noqa: E731
fala = [(s(x), s(y)) for x, y in re.findall(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", txt)]

def agudos(seg):
    m = seg.mean(axis=1); N = 4096
    if len(m) < 2 * N: return None
    fr = np.lib.stride_tricks.sliding_window_view(m, N)[::N // 2][:300] * np.hanning(N)
    P = (np.abs(np.fft.rfft(fr, axis=1)) ** 2).mean(axis=0); f = np.fft.rfftfreq(N, 1 / SR)
    return 10 * np.log10(P[(f >= 4000) & (f < 12000)].sum() / P[(f >= 300) & (f < 4000)].sum())

def piso(seg):
    w = int(0.02 * SR); m = seg[: len(seg) // w * w].mean(axis=1).reshape(-1, w)
    return float(np.percentile(10 * np.log10((m ** 2).mean(axis=1) + 1e-12), 10))

def rms(seg): return 10 * np.log10((seg ** 2).mean() + 1e-12)

def so_fala(x0, x1):
    idx = [(max(p, x0), min(q, x1)) for p, q in fala if q > x0 and p < x1]
    return np.concatenate([np.arange(int(p * SR), int(q * SR)) for p, q in idx]) if idx else None

blocos = []
for bl in D["blocos"]:
    i0, i1 = int(bl["inicio"] * SR), int(bl["fim"] * SR)
    sa, sb = a[i0:i1], b[i0:i1]
    g = rms(sb) - rms(sa)
    ag_a, ag_b = agudos(sa), agudos(sb)
    ix = so_fala(bl["inicio"], bl["fim"])
    fa = rms(b[ix]) if ix is not None and len(ix) > SR else None
    # mono: perda de nível ao somar L+R (antes × depois)
    mono = lambda x: 10 * np.log10((x.mean(axis=1) ** 2).mean() + 1e-12) - rms(x)  # noqa: E731
    blocos.append({"bloco": bl["bloco"], "inicio": bl["inicio"], "fim": bl["fim"], "ganho_medio_dB": round(g, 2),
                   "agudos_antes": None if ag_a is None else round(ag_a, 2), "agudos_depois": None if ag_b is None else round(ag_b, 2),
                   "delta_agudos_dB": None if ag_a is None else round(ag_b - ag_a, 2),
                   "piso_antes": round(piso(sa), 1), "piso_depois": round(piso(sb), 1),
                   "rms_fala_depois_dBFS": None if fa is None else round(fa, 1),
                   "perda_mono_antes": round(mono(sa), 2), "perda_mono_depois": round(mono(sb), 2)})
inicio = 20 * np.log10(np.abs(b[:int(0.01 * SR)]).max() + 1e-12)
fim = 20 * np.log10(np.abs(b[-int(0.01 * SR):]).max() + 1e-12)
dag = [x["delta_agudos_dB"] for x in blocos if x["delta_agudos_dB"] is not None]
fl = [x["rms_fala_depois_dBFS"] for x in blocos if x["rms_fala_depois_dBFS"] is not None]
fa0 = []
for bl in D["blocos"]:
    ix = so_fala(bl["inicio"], bl["fim"])
    if ix is not None and len(ix) > SR: fa0.append(rms(a[ix]))
out = {"blocos": blocos, "pico_primeiros_10ms_dBFS": round(inicio, 1), "pico_ultimos_10ms_dBFS": round(fim, 1),
       "delta_agudos_dB": {"min": min(dag), "max": max(dag), "mediana": float(np.median(dag))},
       "fala_rms_por_bloco_dBFS": {"antes_p10_p90": [round(float(np.percentile(fa0, 10)), 1), round(float(np.percentile(fa0, 90)), 1)],
                                   "depois_p10_p90": [round(float(np.percentile(fl, 10)), 1), round(float(np.percentile(fl, 90)), 1)]}}
json.dump(out, open(saida, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "blocos"}, ensure_ascii=False, indent=1))
for x in blocos:
    if x["delta_agudos_dB"] is not None and abs(x["delta_agudos_dB"]) > 0.5: print("agudos mudaram:", x["bloco"], x["delta_agudos_dB"])
