"""Diagnóstico de áudio da REV1 (docs/AUDIO_REVIEW_STANDARD.md, seções 4 e 5): mede o ORIGINAL, sem tratar.

Blocos = planos do editado do Diego (cortes de cena detectados), com fala (F), fala + música (F+M) ou só
ambiente/música (A/M). Por bloco: loudness integrada e da fala (BS.1770), piso de ruído (percentil 10 do RMS em
20 ms), relação fala/piso, agudos da voz (4–12 kHz contra 0,3–4 kHz), grave (< 150 Hz) contra a faixa da voz
(indício de vento), amostras perto do teto e correlação entre canais. O agente NÃO escuta: os números apontam onde
ouvir.

Roda de reels/ams-yt:  python rev1/audio_diagnostico_rev1.py
Saídas: rev1/audio/diagnostico_blocos_rev1.csv e _tmp/diag_rev1.json
"""
import csv
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000


def banda_db(x, lo, hi):
    sos = signal.butter(4, [lo, hi] if hi else lo, btype="bandpass" if hi else "lowpass", fs=SR, output="sos")
    y = signal.sosfilt(sos, x)
    return 10 * np.log10(np.mean(y ** 2) + 1e-20)


def main():
    os.makedirs("rev1/audio", exist_ok=True)
    x, sr = sf.read("_tmp/voz_orig.wav", dtype="float32")
    m, _ = sf.read("_tmp/musica_orig.wav", dtype="float32")
    assert sr == SR
    mono = x.mean(axis=1)
    medidor = pyln.Meter(SR)
    dur = len(mono) / SR

    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    palavras = [(w["ini"], w["fim"]) for s in tr["segmentos"] for w in s["palavras"]]
    fala = np.zeros(int(dur * 100) + 1, bool)  # 10 ms
    for a, b in palavras:
        fala[int(a * 100):int(b * 100) + 1] = True
    musica_rms = np.sqrt(np.mean(m.mean(axis=1)[: len(mono) // 480 * 480].reshape(-1, 480) ** 2, axis=1))
    tem_musica = 20 * np.log10(musica_rms + 1e-9) > -50

    cortes = [0.0] + json.load(open("_tmp/cenas.json"))["cortes"] + [dur]
    # junta planos curtos (< 3 s) ao seguinte, para medir com janela útil
    blocos = []
    a = cortes[0]
    for c in cortes[1:]:
        if c - a >= 3 or c == dur:
            blocos.append((a, c))
            a = c
    out = []
    for i, (a, b) in enumerate(blocos):
        ia, ib = int(a * SR), int(b * SR)
        seg = x[ia:ib]
        sm = mono[ia:ib]
        f = fala[int(a * 100):int(b * 100)]
        frac_fala = float(f.mean()) if len(f) else 0.0
        mus = float(tem_musica[int(a * 100):int(b * 100)].mean()) if b > a else 0.0
        tipo = ("F+M" if mus > 0.3 else "F") if frac_fala > 0.25 else ("M" if mus > 0.3 else "A")
        try:
            lufs = medidor.integrated_loudness(seg) if b - a >= 0.5 else float("nan")
        except Exception:
            lufs = float("nan")
        # fala: só janelas de 10 ms com palavra
        mask = np.repeat(f, SR // 100)[: len(sm)]
        voz = sm[: len(mask)][mask[: len(sm)]] if mask.any() else np.zeros(1)
        try:
            lufs_fala = medidor.integrated_loudness(np.column_stack([voz, voz])) if len(voz) > SR else float("nan")
        except Exception:
            lufs_fala = float("nan")
        n20 = SR // 50
        k = len(sm) // n20
        rms = 20 * np.log10(np.sqrt(np.mean(sm[: k * n20].reshape(k, n20) ** 2, axis=1)) + 1e-9) if k else np.array([-120.0])
        piso = float(np.percentile(rms, 10))
        nivel_fala = float(np.percentile(rms, 90))
        agudos = banda_db(voz, 4000, 12000) - banda_db(voz, 300, 4000) if len(voz) > SR else float("nan")
        grave = banda_db(voz, 150, None) - banda_db(voz, 300, 4000) if len(voz) > SR else float("nan")
        teto = int(np.sum(np.abs(seg) > 0.989))
        corr = float(np.corrcoef(seg[:, 0], seg[:, 1])[0, 1]) if len(seg) > 10 and seg[:, 1].std() > 0 else 1.0
        out.append({
            "bloco": f"B{i + 1:03d}", "ini": round(a, 3), "fim": round(b, 3), "tipo": tipo, "fala_frac": round(frac_fala, 2),
            "lufs": round(lufs, 1), "lufs_fala": round(lufs_fala, 1), "piso_db": round(piso, 1), "p90_db": round(nivel_fala, 1),
            "fala_piso_db": round(nivel_fala - piso, 1), "agudos_db": round(agudos, 1), "grave_db": round(grave, 1),
            "amostras_teto": teto, "correlacao": round(corr, 2),
        })
    with open("rev1/audio/diagnostico_blocos_rev1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    json.dump(out, open("_tmp/diag_rev1.json", "w"), indent=1)

    falas = [o for o in out if o["tipo"].startswith("F") and o["lufs_fala"] == o["lufs_fala"]]
    lf = np.array([o["lufs_fala"] for o in falas])
    print(f"blocos {len(out)} (com fala {len(falas)})")
    print(f"fala por bloco: mediana {np.median(lf):.1f} LUFS, p10 {np.percentile(lf, 10):.1f}, p90 {np.percentile(lf, 90):.1f}")
    print(f"total integrado (original): {medidor.integrated_loudness(x):.1f} LUFS")
    print(f"amostras no teto: {sum(o['amostras_teto'] for o in out)}; correlação mín. {min(o['correlacao'] for o in out):.2f}")
    print(f"fala/piso mediana {np.median([o['fala_piso_db'] for o in falas]):.1f} dB; agudos mediana {np.nanmedian([o['agudos_db'] for o in falas]):.1f} dB; grave mediana {np.nanmedian([o['grave_db'] for o in falas]):.1f} dB")
    print("mais baixos:", [(o["bloco"], o["ini"], o["lufs_fala"]) for o in sorted(falas, key=lambda o: o["lufs_fala"])[:8]])
    print("mais altos:", [(o["bloco"], o["ini"], o["lufs_fala"]) for o in sorted(falas, key=lambda o: -o["lufs_fala"])[:5]])
    print("pior fala/piso:", [(o["bloco"], o["ini"], o["fala_piso_db"]) for o in sorted(falas, key=lambda o: o["fala_piso_db"])[:8]])
    print("mais grave (vento?):", [(o["bloco"], o["ini"], o["grave_db"]) for o in sorted(falas, key=lambda o: -o["grave_db"])[:8]])
    print("mais abafado:", [(o["bloco"], o["ini"], o["agudos_db"]) for o in sorted(falas, key=lambda o: o["agudos_db"])[:6]])


if __name__ == "__main__":
    main()
