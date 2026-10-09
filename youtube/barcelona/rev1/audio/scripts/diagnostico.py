"""Diagnóstico de áudio (AUDIO_REVIEW_STANDARD v1.1.0, seções 4–5): só medição, nada é alterado.

Uso (de dentro de youtube/barcelona/):
  python3 rev1/audio/scripts/diagnostico.py ARQ_ANALISE.flac EBUR128_VERBOSE.log SRT_APOIO CORTES.json SAIDA.json
- ARQ_ANALISE: cópia sem perda da faixa do original (FLAC, taxa original)
- EBUR128_VERBOSE.log: saída de `ffmpeg -af ebur128=peak=true:framelog=verbose` sobre o mesmo arquivo
- SRT_APOIO: transcrição automática de apoio (só para separar trechos com e sem fala; não é verdade)
- CORTES.json: cortes de cena detectados (blocos = cenas, divididas em até 60 s)
"""
import json, re, subprocess, sys
import numpy as np

flac, log, srt, cortes_arq, saida = sys.argv[1:6]
SR = 44100

# --- áudio em float32
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", flac, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2)
dur = len(x) / SR

# --- ebur128 por 100 ms
M, S_, TP = [], [], []
for l in open(log, errors="ignore"):
    m = re.search(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.inf]+)\s+S:\s*(-?[\d.inf]+).*?FTPK:\s*(-?[\d.inf]+)\s+(-?[\d.inf]+)", l)
    if m:
        t, mm, ss, a, b = m.groups()
        f = lambda v: -120.0 if "inf" in v else float(v)  # noqa: E731
        M.append((float(t), f(mm))); S_.append(f(ss)); TP.append(max(f(a), f(b)))
tE = np.array([m[0] for m in M]); Mv = np.array([m[1] for m in M]); Sv = np.array(S_); TPv = np.array(TP)

# --- fala (apoio): eventos do SRT
fala = []
txt = open(srt, encoding="utf-8").read()
for a, b in re.findall(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", txt):
    s = lambda v: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*v.split(":"))  # noqa: E731
    fala.append((s(a), s(b)))
eh_fala = np.zeros(len(tE), bool)
for a, b in fala:
    eh_fala |= (tE >= a + 0.3) & (tE <= b)

# --- blocos por cena (máx. 60 s)
cortes = [0.0] + [c for c in json.load(open(cortes_arq))["cortes_s"] if c > 0.5] + [dur]
blocos = []
for a, b in zip(cortes, cortes[1:]):
    n = max(1, int(np.ceil((b - a) / 60)))
    for k in range(n):
        blocos.append((a + (b - a) * k / n, a + (b - a) * (k + 1) / n))
# junta cenas curtas (< 8 s) com a anterior, para medir com significado
fund = []
for a, b in blocos:
    if fund and (b - a < 8 or fund[-1][1] - fund[-1][0] < 8) and (b - fund[-1][0]) <= 60:
        fund[-1] = (fund[-1][0], b)
    else:
        fund.append((a, b))
blocos = fund

def rms_db(seg):
    return 10 * np.log10(np.mean(seg.astype(np.float64) ** 2) + 1e-12)

def piso(seg):   # [PRECEDENTE] percentil 10 do RMS em janelas de 20 ms
    n = int(0.02 * SR)
    m = seg[: len(seg) // n * n].mean(axis=1).reshape(-1, n).astype(np.float64)
    r = 10 * np.log10((m ** 2).mean(axis=1) + 1e-12)
    return float(np.percentile(r, 10))

def bandas(seg):  # energia relativa por faixa (média do espectro em janelas de 4096)
    mono = seg.mean(axis=1)
    n = 4096
    if len(mono) < n * 2:
        return None
    w = np.hanning(n)
    fr = np.lib.stride_tricks.sliding_window_view(mono, n)[:: n // 2][:400] * w
    P = (np.abs(np.fft.rfft(fr, axis=1)) ** 2).mean(axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    tot = P[(f > 20)].sum()
    q = lambda lo, hi: float(10 * np.log10(P[(f >= lo) & (f < hi)].sum() / tot + 1e-12))  # noqa: E731
    return {"<200": q(20, 200), "200-2k": q(200, 2000), "2k-5k": q(2000, 5000), ">5k": q(5000, 20000),
            "agudos_4-12k_vs_0.3-4k": float(10 * np.log10(P[(f >= 4000) & (f < 12000)].sum() / P[(f >= 300) & (f < 4000)].sum()))}

def corr(seg):
    a, b = seg[:, 0].astype(np.float64), seg[:, 1].astype(np.float64)
    return float(np.corrcoef(a, b)[0, 1]) if a.std() > 1e-6 and b.std() > 1e-6 else 1.0

res = []
for i, (a, b) in enumerate(blocos, 1):
    seg = x[int(a * SR): int(b * SR)]
    sel = (tE >= a) & (tE < b)
    f_sel = sel & eh_fala
    nf_sel = sel & ~eh_fala
    frac_fala = float(f_sel.sum() / max(sel.sum(), 1))
    tipo = "F" if frac_fala > 0.5 else ("F/A" if frac_fala > 0.15 else "A/M")
    clip = int((np.abs(seg) >= 0.9999).sum())
    res.append({
        "bloco": f"B{i:03d}", "inicio": round(a, 3), "fim": round(b, 3), "tipo_aprox": tipo, "fracao_fala": round(frac_fala, 2),
        "S_mediana_LUFS": round(float(np.median(Sv[sel])) if sel.any() else -120, 1),
        "M_fala_mediana_LUFS": round(float(np.median(Mv[f_sel])) if f_sel.any() else float("nan"), 1),
        "M_sem_fala_mediana_LUFS": round(float(np.median(Mv[nf_sel])) if nf_sel.any() else float("nan"), 1),
        "TP_max_dBTP": round(float(TPv[sel].max()) if sel.any() else -120, 2),
        "amostras_no_teto": clip,
        "piso_dBFS": round(piso(seg), 1), "rms_dBFS": round(rms_db(seg), 1),
        "correlacao_LR": round(corr(seg), 3), "bandas_dB": bandas(seg),
    })

# --- picos acima do limite e de quanto o limitador precisaria com ganho G
picos = []
acima = TPv > -1.0
i = 0
while i < len(acima):
    if acima[i]:
        j = i
        while j + 1 < len(acima) and acima[j + 1]:
            j += 1
        picos.append({"inicio": round(float(tE[i] - 0.1), 1), "fim": round(float(tE[j]), 1), "TP_max": round(float(TPv[i:j + 1].max()), 2),
                      "fala": bool(eh_fala[i:j + 1].any())})
        i = j + 1
    else:
        i += 1

I_fala = float(np.median(Mv[eh_fala & (Mv > -70)]))
I_sem = float(np.median(Mv[~eh_fala & (Mv > -70)]))
G = -14.0 - (-19.3)
reducao = np.maximum(TPv + G - (-1.5), 0)
out = {
    "duracao_s": dur, "blocos": res, "picos_acima_-1dBTP": picos,
    "M_mediana_fala_LUFS": round(I_fala, 1), "M_mediana_sem_fala_LUFS": round(I_sem, 1),
    "simulacao_ganho_dB": round(G, 1),
    "limitador_reducao_necessaria": {"janelas_100ms_com_reducao": int((reducao > 0).sum()),
                                     "acima_2dB": int((reducao > 2).sum()), "acima_4dB": int((reducao > 4).sum()),
                                     "max_dB": round(float(reducao.max()), 1),
                                     "fracao_do_tempo_%": round(100 * float((reducao > 0).mean()), 2)},
}
json.dump(out, open(saida, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("blocos", "picos_acima_-1dBTP")}, ensure_ascii=False, indent=1))
print("blocos:", len(res), " grupos de picos > -1 dBTP:", len(picos))
