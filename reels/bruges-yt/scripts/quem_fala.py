"""Quem fala (pedido do Diego, 23/10/2026: "tem frase que é minha e tem frase que não é; faça a medição pelo tom
da voz"). Mede a frequência fundamental (F0, pYIN) de cada palavra da transcrição e marca Diego (D), Marina (M) ou
dúvida (?).

Como decide:
  - F0 de cada palavra = mediana dos quadros vozeados (pYIN, 85–420 Hz, quadros de 10 ms; mínimo 3 quadros).
  - Limiar = ponto onde as duas populações se cruzam numa mistura de 2 gaussianas sobre log2(F0) de todas as
    palavras do vídeo. Conferido contra referências medidas: as narrações que o Diego gravou (só ele) e trechos em
    que só a Marina fala e a imagem confirma (MARINA_REF).
  - Palavra a menos de 1,5 semitom do limiar = dúvida. Dentro de uma frase, uma palavra isolada entre duas da
    outra pessoa vira a da maioria (o pYIN erra a oitava em sílabas curtas).
A voz sobe quando a pessoa ri ou grita, e o vento confunde o pYIN: o resultado é medição, não escuta.

Roda de reels/ams-yt:  python scripts/quem_fala.py _tmp/voz16k.wav _tmp/transcricao.json _tmp/falantes.json
"""
import glob
import json
import sys
from multiprocessing import Pool

import librosa
import numpy as np
import soundfile as sf

SR = 16000
HOP = 160  # 10 ms
FMIN, FMAX = 85, 420
MARINA_REF = [(1161.0, 1162.6), (227.7, 230.6)]  # "Surreal." (stroopwafel) e "Tomara que não, porque nem guarda-chuva eu tenho"
MARGEM_ST = 1.5


def pyin_trecho(args):
    x, ini = args
    f0, voz, _ = librosa.pyin(x, fmin=FMIN, fmax=FMAX, sr=SR, frame_length=1024, hop_length=HOP)
    f0[~voz] = np.nan
    return ini, f0


def st(a, b):
    return 12 * np.log2(a / b)


def main():
    audio, arq_tr, saida = sys.argv[1], sys.argv[2], sys.argv[3]
    x, sr = sf.read(audio, dtype="float32")
    assert sr == SR
    tr = json.load(open(arq_tr, encoding="utf-8"))
    # F0 só onde há fala (segmentos da transcrição), em paralelo
    trechos = [(x[int(s["ini"] * SR):int(s["fim"] * SR) + 1024], s["ini"]) for s in tr["segmentos"]]
    with Pool(4) as p:
        res = p.map(pyin_trecho, trechos, chunksize=4)
    f0_seg = {round(ini, 3): f0 for ini, f0 in res}

    def f0_palavra(s, w):
        f0 = f0_seg[round(s["ini"], 3)]
        a, b = int((w["ini"] - s["ini"]) * SR / HOP), int((w["fim"] - s["ini"]) * SR / HOP) + 1
        v = f0[max(0, a):b]
        v = v[~np.isnan(v)]
        return float(np.median(v)) if len(v) >= 3 else None

    todas = []
    for s in tr["segmentos"]:
        for w in s["palavras"]:
            w["f0"] = f0_palavra(s, w)
            if w["f0"]:
                todas.append(np.log2(w["f0"]))

    # referências
    dg = []
    for f in sorted(glob.glob("_tmp/narr/*.16k.wav")):
        y, _ = sf.read(f, dtype="float32")
        f0, voz, _ = librosa.pyin(y, fmin=FMIN, fmax=FMAX, sr=SR, frame_length=1024, hop_length=HOP)
        dg += list(f0[voz])
    mr = []
    for a, b in MARINA_REF:
        for s in tr["segmentos"]:
            for w in s["palavras"]:
                if a <= w["ini"] < b and w["f0"]:
                    mr.append(w["f0"])
    ref_d, ref_m = float(np.median(dg)), float(np.median(mr))

    # mistura de 2 gaussianas (EM simples) em log2(F0), começando nas referências
    z = np.array(todas)
    mu = np.log2([ref_d, ref_m])
    sd = np.array([0.25, 0.25])
    pi = np.array([0.6, 0.4])
    for _ in range(200):
        pdf = pi / (sd * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((z[:, None] - mu) / sd) ** 2)
        r = pdf / pdf.sum(axis=1, keepdims=True)
        nk = r.sum(axis=0)
        mu = (r * z[:, None]).sum(axis=0) / nk
        sd = np.sqrt((r * (z[:, None] - mu) ** 2).sum(axis=0) / nk)
        pi = nk / len(z)
    grade = np.linspace(mu[0], mu[1], 2000)
    pdf = pi / (sd * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((grade[:, None] - mu) / sd) ** 2)
    limiar = float(2 ** grade[np.argmin(np.abs(pdf[:, 0] - pdf[:, 1]))])

    frases = []
    for s in tr["segmentos"]:
        ws = s["palavras"]
        rot = []
        for w in ws:
            if not w["f0"]:
                rot.append("?")
            else:
                d = st(w["f0"], limiar)
                rot.append("?" if abs(d) < MARGEM_ST else ("M" if d > 0 else "D"))
        # palavra isolada entre duas da outra pessoa vira a da maioria
        for i in range(1, len(rot) - 1):
            if rot[i] in "DM" and rot[i - 1] == rot[i + 1] and rot[i - 1] in "DM" and rot[i - 1] != rot[i]:
                rot[i] = rot[i - 1]
        # sem medida: herda a vizinha mais próxima da mesma frase
        for i in range(len(rot)):
            if rot[i] == "?":
                viz = [rot[j] for j in (i - 1, i + 1) if 0 <= j < len(rot) and rot[j] in "DM"]
                if len(set(viz)) == 1:
                    rot[i] = viz[0] + "~"
        for w, r_ in zip(ws, rot):
            w["quem"] = r_[0] if r_[0] in "DM" else "?"
        nd = sum(1 for r_ in rot if r_ == "D")
        nm = sum(1 for r_ in rot if r_ == "M")
        quem = "Diego" if nd > 2 * nm else "Marina" if nm > 2 * nd else ("dúvida" if nd + nm else "sem voz medida")
        fs_ = [w["f0"] for w in ws if w["f0"]]
        frases.append({"ini": s["ini"], "fim": s["fim"], "texto": s["texto"], "f0": round(float(np.median(fs_)), 1) if fs_ else None,
                       "quem": quem, "palavras_D": nd, "palavras_M": nm, "mistura": nd >= 2 and nm >= 2,
                       "palavras": [{"p": w["p"], "ini": w["ini"], "fim": w["fim"], "f0": round(w["f0"], 1) if w["f0"] else None, "quem": w["quem"]} for w in ws]})
    out = {"ref_diego_hz": round(ref_d, 1), "ref_marina_hz": round(ref_m, 1), "gmm_hz": [round(float(2 ** m), 1) for m in mu],
           "gmm_peso": [round(float(p), 2) for p in pi], "limiar_hz": round(limiar, 1), "margem_semitons": MARGEM_ST, "frases": frases}
    json.dump(out, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cont = {}
    for f in frases:
        cont[f["quem"]] = cont.get(f["quem"], 0) + 1
    print(f"Diego (narrações) {ref_d:.0f} Hz · Marina (ref.) {ref_m:.0f} Hz · mistura {out['gmm_hz']} pesos {out['gmm_peso']} · limiar {limiar:.0f} Hz · frases {cont}")


if __name__ == "__main__":
    main()
