"""Conferências de áudio da REV4 (de reels/bru-yt), sobre o cache da mixagem (_tmp/vm_rev4.npz, antes do master):

  1. buracos: trechos ≥ 200 ms abaixo de −70 dBFS (voz + música) no vídeo;
  2. música × fala de vlog: 10 ms com música audível (> −60 dBFS) e palavra da transcrição ao mesmo tempo (corpo);
  3. sincronia com o "(2)": cada janela de música correlacionada com o export com música, no mesmo minuto da fonte
     (correlação normalizada deslizante, ±1,5 s; defasagem em ms);
  4. voz dupla: plano sob narração (gancho/fechamento) com palavras da fonte que não ficou mudo.
Compara com a REV3 quando existe _tmp/vm_rev3.npz.

  python rev4/conferir_audio_rev4.py
"""
import bisect
import json
import os

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
J = SR // 100


def env_db(x):
    n = len(x) // J
    return 10 * np.log10((x[: n * J].reshape(n, J) ** 2).mean(axis=1) + 1e-14)


def main():
    lt = json.load(open("rev3/linha_do_tempo_rev3.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    ws = [w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]]
    fps, G, cf = lt["fps"], lt["gancho_ms"], lt["corpo_fim_ms"]
    manter = lt["manter"]
    ini_src = [x / fps for x, _ in manter]
    acc, ini_out = 0, []
    for x, y in manter:
        ini_out.append(acc)
        acc += y - x

    def ms(ts):
        i = max(0, bisect.bisect_right(ini_src, ts) - 1)
        x, y = manter[i]
        q = ts * fps
        if q >= y or q < x:
            return None
        return G + (ini_out[i] + q - x) * 1000 / fps

    f = lambda s_: f"{int(s_ // 60)}:{s_ % 60:04.1f}"
    res = {}
    for rev in ("rev4", "rev3"):
        arq = f"_tmp/vm_{rev}.npz"
        if not os.path.exists(arq):
            continue
        z = np.load(arq)
        V, M = z["V"].mean(axis=1), z["M"].mean(axis=1)
        e = env_db(V + M)
        idx = np.flatnonzero(e < -70)
        bur = [(g[0] / 100, (g[-1] + 1) / 100) for g in np.split(idx, np.flatnonzero(np.diff(idx) > 1) + 1) if len(idx) and len(g) >= 20]
        em = env_db(M)
        viva = np.zeros(len(em), bool)
        for w in ws:
            a, b = ms(w["ini"]), ms(w["fim"])
            if a is not None and b is not None and 0 < b - a < 3000 and G <= a < cf:
                viva[int(a / 10):int(b / 10) + 1] = True
        sob = np.flatnonzero((em > -60) & viva)
        res[rev] = {"buracos": [(f(a), round(b - a, 2)) for a, b in bur], "musica_sobre_fala_s": round(len(sob) / 100, 2),
                    "musica_no_corpo_s": round(float((em > -60)[int(G / 10):int(cf / 10)].sum()) / 100, 1)}
        if rev == "rev4" and len(sob):
            res[rev]["sobre_fala_onde"] = [f(g[0] / 100) for g in np.split(sob, np.flatnonzero(np.diff(sob) > 1) + 1)]
    print(json.dumps(res, ensure_ascii=False, indent=1))

    # 3. sincronia com o "(2)"
    info = json.load(open("_tmp/vm_rev4.npz.json"))
    M = np.load("_tmp/vm_rev4.npz")["M"].mean(axis=1)
    m2 = sf.read("_tmp/musica_orig.wav", dtype="float32")[0].mean(axis=1)
    sos = signal.butter(2, 150, btype="highpass", fs=SR, output="sos")
    print("sincronia com o (2):")
    for w in info["musica_corpo"] + [dict(x, id="outra") for x in info["musica_outras_do_2"]]:
        o = int(w["video_ms"][0] * SR / 1000) + SR
        s0 = int(w["fonte_s"][0] * SR) + SR + (int(0.05 * SR) if w["id"] == "outra" else 0)
        # correlação normalizada deslizante (±1,5 s) de 2 s da mixagem contra o "(2)"
        a = signal.sosfilt(sos, M[o:o + 2 * SR])
        ref = signal.sosfilt(sos, m2[s0 - int(1.5 * SR):s0 + int(3.5 * SR)])
        cc = signal.correlate(ref, a, mode="valid")
        en = np.sqrt(np.convolve(ref ** 2, np.ones(len(a)), mode="valid"))
        ncc = cc / (np.linalg.norm(a) * en + 1e-9)
        k = int(np.argmax(ncc))
        best = (float(ncc[k]), k - int(1.5 * SR))
        print(f"  {w['id']:5s} vídeo {f(w['video_ms'][0] / 1000)}: correlação {best[0]:.2f}, defasagem {best[1] / SR * 1000:+.1f} ms")

    # 4. voz dupla sob narração
    mudos = {round(p["fonte_s"], 2) for p in info["planos_mudos"]}
    duplas = []
    for p in lt["audio"]:
        if p["tipo"] in ("gancho_baixo", "fechamento") and round(p["src"], 2) not in mudos:
            dentro = [w for w in ws if p["src"] <= w["ini"] and w["fim"] <= p["src"] + p["dur"] / 1000]
            if len(dentro) >= 2:
                duplas.append(f(p["out"] / 1000))
    print("planos sob narração com fala da fonte (voz dupla):", duplas or "nenhum")


if __name__ == "__main__":
    main()
