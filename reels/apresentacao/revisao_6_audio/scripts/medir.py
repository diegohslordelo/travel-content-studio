"""Medições de diagnóstico/verificação de áudio (voz e ambiente) por trecho.

Uso: python3 medir.py arquivo.wav saida.json [narracao]
Sem "narracao": trata o arquivo como o Reel (41,4 s) e mede por cena.
"""
import json
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000
# Cenas do Reel (início, fim, nome, trechos de voz no tempo do Reel)
CENAS = [
    (0.000, 3.000, "01 gancho Sagrada (amb.)", []),
    (3.000, 4.250, "02 Vaso de Oro + narração", [(3.365, 4.10)]),
    (4.250, 8.458, "03 Arco + narração", [(4.35, 8.375)]),
    (8.458, 10.750, "04 Camp Nou + narração", [(8.64, 10.695)]),
    (10.750, 12.375, "05 brinde + narração", [(10.875, 12.26)]),
    (12.375, 14.917, "06 Arco + narração", [(12.56, 14.73)]),
    (14.917, 19.625, "07 fala Diego: Buenos días", [(15.20, 16.98), (17.76, 19.44)]),
    (19.625, 22.333, "08 fala Diego: Chegamos!", [(21.66, 22.12)]),
    (22.333, 24.917, "09 Eiffel (amb.)", []),
    (24.917, 27.417, "10 waffle (amb.)", []),
    (27.417, 30.417, "11 fala Diego + ela: Muito", [(27.60, 28.06), (28.40, 30.18)]),
    (30.417, 34.958, "12 fala Diego: tapa", [(30.52, 34.74)]),
    (34.958, 41.417, "13 fechamento (amb.)", []),
]


def banda(x, f1, f2, ordem=4):
    if f1 <= 0:
        sos = signal.butter(ordem, f2, "lowpass", fs=SR, output="sos")
    elif f2 >= SR / 2:
        sos = signal.butter(ordem, f1, "highpass", fs=SR, output="sos")
    else:
        sos = signal.butter(ordem, [f1, f2], "bandpass", fs=SR, output="sos")
    return signal.sosfiltfilt(sos, x)


def db(v):
    return 20 * np.log10(np.maximum(v, 1e-10))


def janelas_rms(x, J):
    n = len(x) // J * J
    return np.sqrt((x[:n].reshape(-1, J) ** 2).mean(1))


def true_peak(x2):
    up = signal.resample_poly(x2, 4, 1, axis=0)
    return float(db(np.max(np.abs(up))))


def short_term(meter, x2, passo=0.1):
    """LUFS short-term (janela 3 s) a cada 100 ms."""
    J, P = int(3 * SR), int(passo * SR)
    if len(x2) < J:
        return [meter.integrated_loudness(np.pad(x2, ((0, J - len(x2)), (0, 0))))] if len(x2) > SR * 0.4 else []
    return [meter.integrated_loudness(x2[i:i + J]) for i in range(0, len(x2) - J + 1, P)]


def lufs(meter, x2):
    if len(x2) < int(0.4 * SR):
        return float("nan")
    return float(meter.integrated_loudness(x2))


def mascara(n, trechos, t0, folga=0.0):
    m = np.zeros(n, bool)
    for a, b in trechos:
        i, j = int((a - t0 - folga) * SR), int((b - t0 + folga) * SR)
        m[max(0, i):max(0, min(n, j))] = True
    return m


def origem_ruido(x, m_voz):
    """Espectro das janelas mais silenciosas fora da voz: diz de onde vem o ruído."""
    J = 2048
    fora = x.copy()
    fora[m_voz] = 0
    n = len(fora) // J
    if n < 2:
        return {}
    fr = fora[:n * J].reshape(n, J)
    e = (fr ** 2).mean(1)
    ok = e > 0
    if ok.sum() < 2:
        return {}
    idx = np.argsort(np.where(ok, e, np.inf))[:max(2, int(ok.sum() * 0.3))]
    f, P = signal.welch(fr[idx].ravel(), SR, nperseg=min(16384, len(fr[idx].ravel())), nfft=32768)
    tot = P.sum() + 1e-20
    fr_b = lambda a, b: float(P[(f >= a) & (f < b)].sum() / tot)
    # zumbido: pico em 50/60 Hz e harmônicos acima do vizinho
    hum = {}
    for base in (50, 60):
        exc = []
        for k in (1, 2, 3):
            fc = base * k
            pk = P[(f > fc - 3) & (f < fc + 3)].max()
            viz = np.median(P[((f > fc - 15) & (f < fc - 5)) | ((f > fc + 5) & (f < fc + 15))])
            exc.append(float(10 * np.log10(pk / (viz + 1e-20))))
        hum[base] = exc
    return {"<200Hz": fr_b(0, 200), "200-2k": fr_b(200, 2000), "2k-8k": fr_b(2000, 8000), ">8k": fr_b(8000, 24000),
            "hum50_dB": hum[50], "hum60_dB": hum[60]}


def cliques(x):
    """Descontinuidades: resíduo de predição de 2ª ordem acima de 12x a mediana local (MAD)."""
    r = np.abs(x[2:] - 2 * x[1:-1] + x[:-2])
    hp = banda(x, 6000, SR / 2)
    mad = np.median(np.abs(r)) + 1e-9
    loc = signal.medfilt(np.abs(hp[:len(r)]), 481) + 1e-9
    cand = np.where((r > 25 * mad) & (np.abs(hp[:len(r)]) > 8 * loc))[0]
    evs = []
    for c in cand:
        if not evs or c - evs[-1] > SR * 0.01:
            evs.append(int(c))
    return evs


def plosivas(x, m_voz):
    """Estouros de grave (<120 Hz) curtos na voz: janela de 10 ms 12 dB acima da mediana do grave na fala."""
    lo = banda(x, 20, 120)
    r = db(janelas_rms(lo, 480))
    mv = mascara(len(r), [], 0)
    mv = m_voz[:len(r) * 480].reshape(-1, 480).any(1) if m_voz.any() else mv
    if mv.sum() < 5:
        return []
    ref = np.median(r[mv])
    pos = np.where(mv & (r > ref + 12))[0]
    evs = []
    for p in pos:
        if not evs or p - evs[-1] > 5:
            evs.append(int(p))
    return [(p * 0.01, float(r[p] - ref)) for p in evs]


def sibilancia(x, m_voz):
    """Energia 5-9 kHz em relação a 1-4 kHz nas janelas de voz (20 ms): p95 e nº de janelas com sibilante > +3 dB."""
    J = 960
    s = db(janelas_rms(banda(x, 5000, 9000), J))
    p = db(janelas_rms(banda(x, 1000, 4000), J))
    mv = m_voz[:len(s) * J].reshape(-1, J).all(1)
    if mv.sum() < 5:
        return None
    d = s[mv] - p[mv]
    return {"p95_dB": float(np.percentile(d, 95)), "max_dB": float(d.max()), "janelas_>+3dB": int((d > 3).sum()),
            "janelas_voz": int(mv.sum())}


def vento(x):
    """Grave < 200 Hz: fração da energia e oscilação (desvio padrão do nível em janelas de 50 ms)."""
    lo = db(janelas_rms(banda(x, 20, 200), 2400))
    tot = db(janelas_rms(x, 2400))
    return {"frac_grave_dB": float(np.median(lo - tot)), "oscil_grave_dB": float(np.std(lo))}


def reverb(x, m_voz):
    """Queda nos 150 ms após o fim de cada trecho de voz (dB). Queda rápida (>20 dB) = sala seca."""
    J = 480
    r = db(janelas_rms(x, J))
    mv = m_voz[:len(r) * J].reshape(-1, J).any(1)
    quedas = []
    for i in range(1, len(mv)):
        if mv[i - 1] and not mv[i] and i + 15 < len(r):
            quedas.append(float(r[i - 3:i].max() - r[i + 12:i + 15].mean()))
    return float(np.median(quedas)) if quedas else None


def analisar(x2, t0, trechos_voz):
    meter = pyln.Meter(SR)
    x = x2.mean(1)
    n = len(x)
    m_voz = mascara(n, trechos_voz, t0)
    rms20 = db(janelas_rms(x, 960))
    mv20 = m_voz[:len(rms20) * 960].reshape(-1, 960).any(1)
    fora = rms20[~mv20] if (~mv20).sum() > 10 else rms20
    st = short_term(meter, x2)
    L, R = x2[:, 0], x2[:, 1]
    corr = float(np.corrcoef(L, R)[0, 1]) if np.std(L) > 0 and np.std(R) > 0 else 1.0
    lado = float(db(np.sqrt(np.mean(((L - R) / 2) ** 2))) - db(np.sqrt(np.mean(((L + R) / 2) ** 2))))
    clip = int((np.abs(x2) >= 0.999).sum())
    # trechos achatados: >= 4 amostras seguidas iguais com |x| > 0.5
    flat = 0
    for ch in (L, R):
        d = np.abs(np.diff(ch)) < 1e-7
        big = np.abs(ch[1:]) > 0.5
        run = 0
        for v in d & big:
            run = run + 1 if v else 0
            if run == 3:
                flat += 1
    voz = x2[m_voz] if m_voz.sum() > SR * 0.4 else None
    amb = x2[~m_voz]
    res = {
        "piso_ruido_dBFS": float(np.percentile(fora, 10)),
        "origem_ruido": origem_ruido(x, m_voz),
        "LUFS_I": lufs(meter, x2),
        "LUFS_voz": lufs(meter, voz) if voz is not None else None,
        "LUFS_fora_da_voz": lufs(meter, amb) if len(amb) > SR * 0.4 else None,
        "ST_min": float(np.min(st)) if st else None, "ST_med": float(np.median(st)) if st else None,
        "ST_max": float(np.max(st)) if st else None,
        "TP_dBTP": true_peak(x2),
        "clip_amostras": clip, "achatados": flat,
        "cliques_s": [round(t0 + c / SR, 3) for c in cliques(x)],
        "plosivas": [(round(t0 + t, 2), round(d, 1)) for t, d in plosivas(x, m_voz)],
        "sibilancia": sibilancia(x, m_voz),
        "vento": vento(x),
        "dc": float(np.mean(x2)),
        "corr_LR": corr, "lado_vs_meio_dB": lado,
        "queda_150ms_dB": reverb(x, m_voz),
        "HF_4k_rel_dB": float(db(np.sqrt(np.mean(banda(x[m_voz] if m_voz.sum() > SR * 0.3 else x, 4000, 12000) ** 2)))
                              - db(np.sqrt(np.mean(banda(x[m_voz] if m_voz.sum() > SR * 0.3 else x, 300, 4000) ** 2)))),
    }
    return res


if __name__ == "__main__":
    arq, saida = sys.argv[1], sys.argv[2]
    x2, sr = sf.read(arq, dtype="float64", always_2d=True)
    assert sr == SR, sr
    if x2.shape[1] == 1:
        x2 = np.repeat(x2, 2, 1)
    out = {}
    if len(sys.argv) > 3 and sys.argv[3] == "narracao":
        # voz no arquivo original: 0,74-12,105 s (lista_de_cortes.json)
        out["narracao"] = analisar(x2, 0.0, [(0.74, 12.105)])
    else:
        for a, b, nome, tv in CENAS:
            out[nome] = analisar(x2[int(a * SR):int(b * SR)], a, tv)
        meter = pyln.Meter(SR)
        tv_all = [t for c in CENAS for t in c[3]]
        out["REEL INTEIRO"] = {"LUFS_I": float(meter.integrated_loudness(x2)), "TP_dBTP": true_peak(x2),
                               "clip_amostras": int((np.abs(x2) >= 0.999).sum()), "dc": float(np.mean(x2))}
    json.dump(out, open(saida, "w"), indent=1, ensure_ascii=False)
    for k, v in out.items():
        print(k, {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()})
