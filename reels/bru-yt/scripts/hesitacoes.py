"""Hesitações ("ééé", "ahn", "hum") do vlog de Bruxelas, para a decupagem (pedido do Diego, 06/11/2026: "corte momentos
vazios e momentos como 'eee', mas cuidado pra não comer nenhuma palavra").

Roda de reels/bru-yt:  python scripts/hesitacoes.py
Entradas: _tmp/transcricao.json (Whisper large-v3, palavra a palavra), _tmp/voz16k.wav
Saída:    _tmp/hesitacoes.json  (candidatos, com a 2ª transcrição de cada um e a decisão: cortar ou manter)

Como acha (o Whisper costuma NÃO escrever a hesitação: ela fica num buraco entre palavras, ou estica a palavra vizinha):
1. Buraco ≥ 0,30 s entre duas palavras em que há VOZ (energia 150–4000 Hz acima do piso + periodicidade de 75–400 Hz),
   ou palavra "é"/"e"/"ah" esticada (≥ 0,55 s) com probabilidade baixa;
2. Cada candidato é transcrito de novo sozinho (Whisper large-v3, sem filtro de voz, com um prompt cheio de hesitações),
   com 0,25 s de folga de cada lado;
3. Corta só se a 2ª transcrição do miolo ESCREVER a hesitação e nenhuma palavra de verdade (só "é", "eh", "ah",
   "ahn", "hum", "hã", "e"). Miolo vazio não corta (em trecho curto o Whisper alucina: o filtro fica em
   scripts/decupar.py). Qualquer palavra = mantém. O corte deixa 0,08 s de cada lado (não encosta na palavra vizinha).
   Palavra esticada ("E…" de "E viemos", "É…"): não some, ENCURTA: ficam os primeiros 0,22 s da palavra (ela continua
   sendo dita) e sai o resto do arrasto até 0,08 s antes da palavra seguinte.
É medição automática: os cortes vão listados na DECUPAGEM para o Diego conferir na prévia.
"""
import json
import re

import numpy as np
import soundfile as sf
from scipy import signal

from faster_whisper import WhisperModel

SR = 16000
HES = {"é", "e", "eh", "ah", "ahn", "hum", "hã", "ã", "éé", "ééé", "ee", "eee", "hmm", "uhm", "um", "ham", "mm"}


def main():
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    ws = sorted([w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]], key=lambda w: w["ini"])
    x, sr = sf.read("_tmp/voz16k.wav", dtype="float32")
    assert sr == SR
    sos = signal.butter(4, [150, 4000], btype="bandpass", fs=SR, output="sos")
    v = signal.sosfilt(sos, x)
    n = SR // 100
    m = len(v) // n
    db = 20 * np.log10(np.sqrt((v[: m * n].reshape(m, n) ** 2).mean(axis=1)) + 1e-9)
    piso = np.array([np.percentile(db[max(0, i - 500):i + 500], 10) for i in range(0, m, 50)]).repeat(50)[:m]

    def vozeado(a, b):
        """Fração de janelas de 30 ms com periodicidade de voz (autocorrelação ≥ 0,45 em 75–400 Hz) e energia."""
        i0, i1 = int(a * SR), int(b * SR)
        L = int(0.03 * SR)
        ok = tot = 0
        for k in range(i0, i1 - L, L // 2):
            fr = x[k:k + L] - x[k:k + L].mean()
            e = 20 * np.log10(np.sqrt((fr ** 2).mean()) + 1e-9)
            tot += 1
            if e < piso[min(m - 1, k // n)] + 10:
                continue
            ac = np.correlate(fr, fr, "full")[L - 1:]
            if ac[0] <= 0:
                continue
            ac = ac / ac[0]
            lo, hi = SR // 400, SR // 75
            if ac[lo:hi].max() >= 0.45:
                ok += 1
        return ok / max(tot, 1)

    cand = []
    for a, b in zip(ws, ws[1:]):
        g0, g1 = a["fim"], b["ini"]
        if g1 - g0 >= 0.30 and g1 - g0 <= 3.0:
            f = vozeado(g0 + 0.05, g1 - 0.05)
            if f >= 0.35:
                cand.append({"tipo": "buraco com voz", "de": g0, "ate": g1, "vozeado": round(f, 2), "antes": a["p"], "depois": b["p"]})
    for i, w in enumerate(ws):
        p = w["p"].lower().strip(".,!?…")
        if p in {"é", "e", "ah", "eh"} and w["fim"] - w["ini"] >= 0.55 and w["prob"] < 0.75:
            cand.append({"tipo": f"palavra esticada [{w['p']}]", "de": w["ini"], "ate": w["fim"], "vozeado": round(vozeado(w["ini"], w["fim"]), 2),
                         "antes": ws[i - 1]["p"] if i else "", "depois": ws[i + 1]["p"] if i + 1 < len(ws) else ""})
    cand.sort(key=lambda c: c["de"])
    print(len(cand), "candidatos")

    modelo = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
    prompt = "Ééé... ahn... hum... é... então, ééé, a gente, ahn, foi lá. Hã? Hmm."
    for c in cand:
        a, b = max(0, c["de"] - 0.25), c["ate"] + 0.25
        segs, _ = modelo.transcribe(x[int(a * SR):int(b * SR)], language="pt", beam_size=5, word_timestamps=True, vad_filter=False,
                                    initial_prompt=prompt, condition_on_previous_text=False)
        palavras = [(w.word.strip(), a + w.start, a + w.end) for s in segs for w in s.words]
        miolo = [p for p, i0, i1 in palavras if i1 > c["de"] + 0.04 and i0 < c["ate"] - 0.04]
        limpas = [re.sub(r"[^\wáéíóúâêôãõç]", "", p.lower()) for p in miolo]
        reais = [p for p in limpas if p and p not in HES]
        c["segunda"] = " ".join(p for p, _, _ in palavras)
        c["miolo"] = " ".join(miolo)
        c["cortar"] = not reais
        if c["tipo"].startswith("palavra"):
            c["corte"] = [round(c["de"] + 0.22, 3), round(c["ate"] - 0.02, 3)] if c["cortar"] and c["ate"] - c["de"] >= 0.45 else None
        else:
            c["corte"] = [round(c["de"] + 0.08, 3), round(c["ate"] - 0.08, 3)] if c["cortar"] else None
        print(f"{c['de']:7.2f}–{c['ate']:7.2f} {c['tipo']:<24} voz {c['vozeado']:.2f}  miolo [{c['miolo']}]  → {'CORTA' if c['cortar'] else 'mantém'}   ({c['segunda']})", flush=True)
    json.dump(cand, open("_tmp/hesitacoes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
