"""Divide cada tomada em blocos de voz (entre silêncios medidos pela energia) e transcreve cada bloco SOZINHO.
Assim repetições e falsos começos aparecem (o Whisper junta repetições quando ouve a tomada inteira).
Uso: python3 scripts/blocos.py"""
import json, subprocess, numpy as np
from faster_whisper import WhisperModel
TOMADAS = ["IMG_7694", "IMG_7695", "IMG_7696", "IMG_7713", "IMG_7720", "IMG_7722", "IMG_7728", "IMG_7733", "IMG_7734"]
SR = 16000
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
out = {}
for t in TOMADAS:
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/{t}.MOV", "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    f = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"fonte/{t}.MOV", "-vn", "-ac", "1", "-ar", str(SR), "-af", "highpass=f=120,lowpass=f=4000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    hop = SR // 100; n = len(f) // hop
    db = 20 * np.log10(np.sqrt(np.mean(f[: n * hop].reshape(n, hop) ** 2, 1)) + 1e-9)
    voz = db > np.percentile(db, 90) - 30
    # blocos: voz separada por silêncio ≥ 0,15 s
    blocos, i = [], 0
    while i < n:
        if voz[i]:
            j = i
            while j < n:
                k = j
                while k < n and not voz[k]: k += 1
                if k - j >= 15 or k >= n: break
                j = k + 1 if k > j else j + 1
                while j < n and voz[j]: j += 1
            blocos.append((i / 100, j / 100)); i = j
        else:
            i += 1
    res = []
    for (s, e) in blocos:
        if e - s < 0.12: continue
        seg = a[int(max(0, s - 0.05) * SR): int((e + 0.05) * SR)]
        segs, _ = m.transcribe(seg, language="pt", beam_size=5, condition_on_previous_text=False, vad_filter=False)
        txt = " ".join(x.text.strip() for x in segs)
        res.append({"ini": s, "fim": e, "texto": txt})
        print(f"{t} {s:6.2f}-{e:6.2f}  {txt}", flush=True)
    out[t] = res
json.dump(out, open("_tmp/blocos.json", "w"), ensure_ascii=False, indent=1)
