"""Quais frases recebem legenda de reforço (DS V2 3.4.2; AUDIO_REVIEW_STANDARD 10.2): só onde, no áudio TRATADO,
a voz ficou baixa ou o ruído ficou alto, e o entendimento é difícil (reconhecedores incertos ou discordando).

Uso: python3 selecionar_trechos.py AUDIO_TRATADO.m4a PRINCIPAL.json COMPARACAO.json SAIDA.json
Medidas por frase (palavras com pausas < 0,5 s, até 6 s), na faixa da voz (300 Hz–3,4 kHz):
  - nível da fala: potência nos intervalos das palavras
  - fundo: potência nas pausas sem palavra a até 4 s da frase (percentil 30 de janelas de 50 ms)
  - voz/fundo (dB) = 10·log10((P_fala − P_fundo) / P_fundo)
"""
import json, re, subprocess, sys, unicodedata
import numpy as np

aud, princ, comp, saida = sys.argv[1:5]
SR = 16000
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", aud, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).astype(np.float64)
# filtro de faixa da voz no domínio da frequência, em blocos
def faixa(sig):
    n = len(sig)
    F = np.fft.rfft(sig)
    f = np.fft.rfftfreq(n, 1 / SR)
    F[(f < 300) | (f > 3400)] = 0
    return np.fft.irfft(F, n)
B = np.concatenate([faixa(x[i:i + SR * 60]) for i in range(0, len(x), SR * 60)])
W = int(0.05 * SR)
pw = (B[: len(B) // W * W].reshape(-1, W) ** 2).mean(axis=1)      # potência por janela de 50 ms
tj = np.arange(len(pw)) * 0.05


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^\w]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def palavras(arq):
    out = []
    for s in json.load(open(arq, encoding="utf-8"))["segmentos"]:
        for p in s["palavras"]:
            if out and not p["p"].startswith(" "):
                out[-1]["t"] += p["p"]; out[-1]["f"] = p["f"]; continue
            out.append({"i": p["i"], "f": p["f"], "t": p["p"].strip(), "prob": p["prob"]})
    for w in out:
        if w["f"] - w["i"] > 1.2:
            w["i"] = w["f"] - 0.8
    return out


P, C = palavras(princ), palavras(comp)
ocup = np.zeros(len(pw), bool)
for w in P + C:
    ocup[int(w["i"] / 0.05):int(w["f"] / 0.05) + 1] = True

frases, cur = [], []
for w in P:
    if cur and (w["i"] - cur[-1]["f"] >= 0.5 or w["f"] - cur[0]["i"] > 6):
        frases.append(cur); cur = []
    cur.append(w)
if cur:
    frases.append(cur)

res = []
for fr in frases:
    a, b = fr[0]["i"], fr[-1]["f"]
    idx = np.zeros(len(pw), bool)
    for w in fr:
        idx[int(w["i"] / 0.05):int(w["f"] / 0.05) + 1] = True
    pf = pw[idx].mean()
    viz = (~ocup) & (tj > a - 4) & (tj < b + 4)
    pb = np.percentile(pw[viz], 30) if viz.sum() >= 6 else np.nan
    snr = 10 * np.log10(max(pf - pb, 1e-12) / pb) if pb == pb and pb > 0 else np.nan
    cn = [norm(w["t"]) for w in C if w["i"] < b + 0.5 and w["f"] > a - 0.5]
    acordo = np.mean([norm(w["t"]) in cn for w in fr])
    res.append({"inicio": round(a, 2), "fim": round(b, 2), "texto": " ".join(w["t"] for w in fr),
                "nivel_fala_dB": round(10 * np.log10(pf + 1e-12), 1), "voz_fundo_dB": None if snr != snr else round(float(snr), 1),
                "prob_media": round(float(np.mean([w["prob"] for w in fr])), 2), "acordo_modelos": round(float(acordo), 2),
                "n_palavras": len(fr)})
med = float(np.median([r["nivel_fala_dB"] for r in res]))
json.dump({"mediana_nivel_fala_dB": med, "frases": res}, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(res), "frases; mediana do nível da fala", round(med, 1), "dB")
