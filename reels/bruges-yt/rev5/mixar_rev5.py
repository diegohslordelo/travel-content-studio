"""Mixagem FINAL da REV5 do vlog de Bruges (docs/AUDIO_REVIEW_STANDARD.md v1.1.0; DS V2 4.6). Medição, não escuta: o
Claude não escuta áudio; a validação auditiva é do Diego (estado AGUARDANDO ESCUTA até ele ouvir).

Roda de reels/bruges-yt:  python -I rev5/mixar_rev5.py --saida _tmp/final_rev5/mix.wav [--sfx _tmp/final_rev5/sfx.wav]
Lê rev5/linha_do_tempo_rev5.json, _tmp/voz_orig.wav (som da fonte, 48 kHz), _tmp/narr/<P|R>n.48k.wav (narrações),
_tmp/musica_rev5.wav (rev5/musica_rev5.py) e os efeitos do render (--sfx). Escreve o WAV (float) e <saida>_mix.json.

Cadeia (precedentes do vídeo de Amsterdam, `reels/ams-yt/rev3/mixar_rev3.py`, adaptados):
  1. Voz da fonte, no tempo da fonte: diagnóstico por bloco (cada plano da fonte com ≥ 2 s de fala mantida na decupagem):
     loudness da fala (só onde há palavra transcrita). Nível 2 (ganho): bloco mais de 1,5 dB longe da mediana dos blocos
     vai até a mediana, no máximo ±5 dB, com transição de 200 ms em volta do corte de cena. Nível 3: passa-altas 80 Hz.
     Nível 6: compressor leve [PRECEDENTE REV6] (2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, no máximo 3 dB, limiar
     8 dB acima da fala-alvo). Sem redução de ruído (nível 5): nenhum bloco pediu (ver o relatório).
  2. Voz montada no tempo do vídeo pelos trechos da decupagem, com rampas de 12 ms em cada emenda (as da prévia aprovada);
     a fala real da Marina no gancho em 0 dB.
  3. Narrações gravadas: passa-altas 80 Hz, fala levada à fala-alvo (a mediana dos blocos), o mesmo compressor leve,
     recorte de 120 ms antes da fala a 250 ms depois (menos, se a próxima narração estiver perto), rampas de 30/80 ms.
  4. Música (rev5/musica_rev5.py, feita para fala em −20 LUFS): reescalada para a fala-alvo; 3 dB abaixo da fala nas
     paisagens e 9 dB abaixo sob a narração [PROJETO 8–10 dB].
  5. Efeitos do Remotion (feitos para fala em −16 LUFS, refLufs): reescalados para a fala-alvo (volumes do DS 4.6).
  6. Master: ganho para −14 LUFS integrados e limitador de pico verdadeiro (sobreamostragem 4×) com teto de −2,0 dBTP
     (Amsterdam REV3: com −1,6 o AAC passava de −1 dBTP); o pico depois do AAC é corrigido por rev5/corrigir_pico_aac.py.
"""
import argparse
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal
from scipy.ndimage import minimum_filter1d

SR = 48000
TETO_DBTP = -2.0
ALVO_MASTER = -14.0
REF_MUSICA = -20.0  # a música da REV5 foi nivelada para fala em −20 LUFS
REF_SFX = -16.0  # refLufs dos props


def comprime(x, alvo):
    """Compressor leve [PRECEDENTE REV6]: 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, no máximo 3 dB, limiar
    8 dB acima da fala-alvo, ligado nos dois canais. `x` (n, 2). Devolve o sinal e a redução (dB, por ms)."""
    Bc = SR // 1000
    nb = len(x) // Bc
    rms = np.sqrt(np.mean(x[: nb * Bc].reshape(nb, Bc, x.shape[1]) ** 2, axis=(1, 2)))
    lv = 20 * np.log10(np.sqrt(np.convolve(rms ** 2, np.ones(10) / 10, mode="same")) + 1e-9)
    exc = lv - (alvo + 8)
    red = np.minimum(np.where(exc <= -2, 0, np.where(exc >= 2, exc / 2, (exc + 2) ** 2 / 16)), 3.0)
    sm = np.zeros_like(red)
    at, rl = np.exp(-1 / 20), np.exp(-1 / 150)
    for i in range(1, len(red)):
        c = at if red[i] > sm[i - 1] else rl
        sm[i] = c * sm[i - 1] + (1 - c) * red[i]
    g = (10 ** (-np.interp(np.arange(len(x)) / Bc, np.arange(nb), sm) / 20)).astype(np.float32)
    return x * g[:, None], sm


def picos_reais(x):
    """Pico verdadeiro por bloco de 1 ms (sobreamostragem 4×, em pedaços de 10 s)."""
    B = SR // 1000
    nb = len(x) // B + 1
    out = np.zeros(nb, np.float32)
    passo = SR * 10
    for c0 in range(0, len(x), passo):
        c1 = min(len(x), c0 + passo)
        m0, m1 = max(0, c0 - 64), min(len(x), c1 + 64)
        up = np.abs(signal.resample_poly(x[m0:m1], 4, 1, axis=0)).max(axis=1)
        up = up[(c0 - m0) * 4:(c0 - m0) * 4 + (c1 - c0) * 4]
        nbl = (c1 - c0 + B - 1) // B
        pad = np.zeros(nbl * B * 4, np.float32)
        pad[: len(up)] = up
        out[c0 // B:c0 // B + nbl] = pad.reshape(nbl, B * 4).max(axis=1)
    return out


def limita(x, teto_db, estat):
    """Limitador de pico verdadeiro: antecipação de 5 ms, liberação de 80 ms (o de Amsterdam REV3)."""
    B = SR // 1000
    teto = 10 ** (teto_db / 20)
    need = np.minimum(1.0, teto / np.maximum(picos_reais(x), 1e-9))
    g = minimum_filter1d(need, size=11)
    rel = np.exp(-1 / 80)
    for i in range(1, len(g)):
        if g[i] > g[i - 1]:
            g[i] = g[i - 1] * rel + (1 - rel) * g[i]
    g = minimum_filter1d(g, size=3)
    x *= np.interp(np.arange(len(x)) / B, np.arange(len(g)), g).astype(np.float32)[:, None]
    gdb = 20 * np.log10(g + 1e-9)
    estat["reducao_max_db"] = round(float(gdb.min()), 2)
    estat["acima_1db_pct"] = round(float(np.mean(gdb < -1) * 100), 2)
    estat["acima_3db_pct"] = round(float(np.mean(gdb < -3) * 100), 3)
    estat["acima_6db_pct"] = round(float(np.mean(gdb < -6) * 100), 3)
    pior, vistos = np.argsort(gdb)[:4000], []
    for i in pior:
        if all(abs(i - v) > 2000 for v in vistos):
            vistos.append(int(i))
        if len(vistos) == 10:
            break
    estat["piores_ms"] = [(v, round(float(gdb[v]), 1)) for v in vistos]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sfx", default=None)
    a = ap.parse_args()
    lt = json.load(open("rev5/linha_do_tempo_rev5.json", encoding="utf-8"))
    N = int(round(lt["duracao_ms"] * SR / 1000))
    med = pyln.Meter(SR)
    hp80 = signal.butter(2, 80, btype="highpass", fs=SR, output="sos")
    rel = {}

    # ---------- 1. voz da fonte: diagnóstico por bloco ----------
    voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32", always_2d=True)
    assert sr == SR
    n_src = len(voz)
    voz_hp = signal.sosfiltfilt(hp80, voz, axis=0).astype(np.float32)
    mantido = np.zeros(n_src, bool)
    for p in lt["audio"]:
        i0 = int(round(p["src"] / 1000 * SR))
        mantido[i0:i0 + int(round(p["dur"] / 1000 * SR))] = True
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    fala = np.zeros(n_src, bool)
    for s in tr["segmentos"]:
        for w in s["palavras"]:
            if 0 < w["fim"] - w["ini"] < 3:
                fala[int(w["ini"] * SR):int(w["fim"] * SR)] = True
    cortes = [0.0] + json.load(open("_tmp/cenas.json"))["cortes"] + [n_src / SR]
    blocos = []
    for k, (b0, b1) in enumerate(zip(cortes, cortes[1:])):
        m = np.zeros(n_src, bool)
        m[int(b0 * SR):int(b1 * SR)] = True
        m &= mantido & fala
        seg = voz_hp[m]
        d = {"bloco": f"B{k + 1:02d}", "ini": round(b0, 3), "fim": round(b1, 3), "fala_s": round(len(seg) / SR, 1)}
        if len(seg) >= 2 * SR:
            d["lufs_fala"] = round(float(med.integrated_loudness(seg)), 1)
            fora = voz_hp[int(b0 * SR):int(b1 * SR)][~fala[int(b0 * SR):int(b1 * SR)]]
            if len(fora) > SR // 2:  # piso: percentil 10 do RMS de 50 ms fora das palavras
                h = SR // 20
                r = np.sqrt(np.mean(fora[: len(fora) // h * h].reshape(-1, h, 2) ** 2, axis=(1, 2)))
                d["piso_dbfs"] = round(float(20 * np.log10(np.percentile(r, 10) + 1e-9)), 1)
            d["pico_dbfs"] = round(float(20 * np.log10(np.abs(voz[int(b0 * SR):int(b1 * SR)]).max() + 1e-9)), 1)
        blocos.append(d)
    com_fala = [b for b in blocos if "lufs_fala" in b]
    alvo = float(np.median([b["lufs_fala"] for b in com_fala]))
    pts_ms, pts_db = [], []
    for b in blocos:
        g = 0.0
        if "lufs_fala" in b and abs(alvo - b["lufs_fala"]) > 1.5:
            g = float(np.clip(alvo - b["lufs_fala"], -5, 5))
        b["ganho_db"] = round(g, 1)
        pts_ms += [b["ini"] * 1000 + 100, b["fim"] * 1000 - 100]
        pts_db += [g, g]
    t_ms = np.arange(n_src, dtype=np.float64) * 1000 / SR
    ganho = (10 ** (np.interp(t_ms, pts_ms, pts_db) / 20)).astype(np.float32)
    del t_ms
    voz_t, red = comprime(voz_hp * ganho[:, None], alvo)
    del voz_hp, ganho
    rel["voz_fonte"] = {"fala_alvo_lufs": round(alvo, 1), "compressor_reducao_max_db": round(float(red.max()), 2),
                        "compressor_acima_1db_pct": round(float(np.mean(red > 1) * 100), 2)}
    rel["blocos"] = blocos

    # ---------- 2. voz no tempo do vídeo ----------
    V = np.zeros((N, 2), np.float32)
    r = int(0.012 * SR)
    for p in lt["audio"]:
        i0, o0, m = int(round(p["src"] / 1000 * SR)), int(round(p["out"] / 1000 * SR)), int(round(p["dur"] / 1000 * SR))
        m = min(m, N - o0, n_src - i0)
        if m <= 2 * r:
            continue
        x = voz_t[i0:i0 + m].copy()
        x[:r] *= np.linspace(0, 1, r, dtype=np.float32)[:, None]
        x[-r:] *= np.linspace(1, 0, r, dtype=np.float32)[:, None]
        V[o0:o0 + m] += x
    del voz_t, voz

    # ---------- 3. narrações gravadas ----------
    narr = sorted(lt["narracoes"], key=lambda n: n["fala_ini"])
    rel["narracoes"] = []
    for i, n in enumerate(narr):
        x, sr = sf.read(f"_tmp/narr/{n['arq']}.48k.wav", dtype="float32")
        assert sr == SR and x.ndim == 1
        x = signal.sosfiltfilt(hp80, x).astype(np.float32)
        cauda = 0.25
        if i + 1 < len(narr):
            cauda = min(cauda, (narr[i + 1]["fala_ini"] - n["fala_fim"]) / 1000 - 0.14)
        a0 = max(0, int((n["arq_ini_s"] - 0.12) * SR))
        a1 = min(len(x), int((n["arq_fim_s"] + cauda) * SR))
        fala_n = x[int(n["arq_ini_s"] * SR):int(n["arq_fim_s"] * SR)]
        g_db = alvo - med.integrated_loudness(fala_n)
        y, rn = comprime(np.column_stack([x[a0:a1], x[a0:a1]]) * np.float32(10 ** (g_db / 20)), alvo)
        fi, fo = int(0.03 * SR), int(0.08 * SR)
        y[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
        y[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
        o0 = int(round((n["t0_ms"] / 1000 + a0 / SR) * SR))
        m = min(len(y), N - o0)
        V[o0:o0 + m] += y[:m]
        rel["narracoes"].append({"id": n["id"], "arq": n["arq"], "entra_ms": round(o0 / SR * 1000), "sai_ms": round((o0 + m) / SR * 1000), "ganho_db": round(float(g_db), 1),
                                 "compressor_max_db": round(float(rn.max()), 1), "cauda_s": round(cauda, 2)})

    # ---------- 4. música ----------
    M, sr = sf.read("_tmp/musica_rev5.wav", dtype="float32", always_2d=True)
    assert sr == SR
    m = min(len(M), N)
    T = V
    T[:m] += M[:m] * np.float32(10 ** ((alvo - REF_MUSICA) / 20))
    del M
    rel["musica_ganho_db"] = round(alvo - REF_MUSICA, 2)

    # ---------- 5. efeitos ----------
    if a.sfx:
        S, sr = sf.read(a.sfx, dtype="float32", always_2d=True)
        assert sr == SR
        m = min(len(S), N)
        T[:m] += S[:m] * np.float32(10 ** ((alvo - REF_SFX) / 20))
        rel["sfx"] = {"arquivo": a.sfx, "duracao_s": round(len(S) / SR, 3), "ganho_db": round(alvo - REF_SFX, 2)}
        del S
    else:
        rel["sfx"] = None

    # ---------- 6. master ----------
    l_int = med.integrated_loudness(T)
    g_master = ALVO_MASTER - l_int
    base = T
    estat = {}
    for _ in range(4):
        T = base * np.float32(10 ** (g_master / 20))
        limita(T, TETO_DBTP, estat)
        l_fim = med.integrated_loudness(T)
        if abs(l_fim - ALVO_MASTER) <= 0.15:
            break
        g_master += ALVO_MASTER - l_fim
    del base
    sf.write(a.saida, T, SR, subtype="FLOAT")
    rel["master"] = {"integrado_antes_lufs": round(float(l_int), 2), "ganho_db": round(float(g_master), 2), "integrado_final_lufs": round(float(l_fim), 2),
                     "teto_dbtp": TETO_DBTP, "limitador": estat, "duracao_s": round(N / SR, 3)}
    json.dump(rel, open(os.path.splitext(a.saida)[0] + "_mix.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rel.items() if k not in ("blocos",)}, ensure_ascii=False))
    print("blocos com ganho:", [(b["bloco"], b["ini"], b["ganho_db"]) for b in blocos if b.get("ganho_db")])


if __name__ == "__main__":
    main()
