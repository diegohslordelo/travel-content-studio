#!/usr/bin/env python3
"""Restauro do fim de palavra que o iPhone não gravou (Reel "Casa de Anne Frank" · REV2).

Nos 7 takes, a trilha de áudio do .MOV acaba ≈ 0,27 s antes do vídeo. Em dois takes a fala ainda soava nesse ponto:
- take 1 (IMG_7143): o áudio para no meio do "DA" de "ci-DA-de." (3,72 s); o vídeo mostra a boca terminando "-de" até ≈ 3,90 s;
- take 6 (IMG_7116): o áudio para no meio do "ZI" de "va-ZI-o." (6,46 s); o vídeo mostra os lábios fechando o "-o" até ≈ 6,56 s.

O restauro completa só o que falta, com a voz do próprio Diego, sem voz sintética:
1. a vogal cortada continua por repetição de períodos glotais do próprio trecho (PSOLA no domínio do tempo), com o tom caindo
   como num fim de frase;
2. o que vem depois sai de outro trecho real do Diego: a fricativa de "tristes" (mesmo take) para o "-de", e o "-o" final
   de "nazismo." (take 4) para o "-o";
3. o ruído da sala (do início do próprio take) preenche o resto do quadro, no lugar do silêncio digital.

Uso (numpy): python3 restauro.py <entrada.f32> <saida.f32> '<json do plano>' <pasta com os .f32 dos takes>
Em geral é chamado pelo rev2.py (etapa preparar). Áudio mono, float32, 48 kHz.
"""
import json
import os
import sys

import numpy as np

SR = 48000


def carregar(arq):
    return np.fromfile(arq, dtype=np.float32).astype(np.float64)


def passa_baixa(x, fc):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[f > fc] *= np.exp(-((f[f > fc] - fc) / (0.25 * fc)) ** 2)
    return np.fft.irfft(X, len(x))


def f0_yin(seg, fmin=70, fmax=320):
    seg = seg - seg.mean()
    tmax = int(SR / fmin)
    W = len(seg) - tmax
    d = np.array([np.sum((seg[:W] - seg[t:t + W]) ** 2) for t in range(tmax)])
    cm = np.ones(tmax)
    cm[1:] = d[1:] * np.arange(1, tmax) / np.maximum(np.cumsum(d[1:]), 1e-12)
    tmin = int(SR / fmax)
    for t in range(tmin, tmax - 1):
        if cm[t] < 0.3 and cm[t] < cm[t + 1]:
            return SR / t
    return SR / (tmin + np.argmin(cm[tmin:]))


def epocas(x, t0, t1):
    """Marcas glotais (amostras) entre t0 e t1: picos do sinal filtrado a cada período local."""
    a, b = int(t0 * SR), int(t1 * SR)
    lp = passa_baixa(x[a - 2400:b + 2400], 900)[2400:2400 + b - a]
    T = int(SR / f0_yin(lp))
    # polaridade: a que tem os picos mais fortes
    pol = 1 if np.max(lp) >= -np.min(lp) else -1
    s = pol * lp
    e = [int(np.argmax(s[:T]))]
    while True:
        alvo = e[-1] + T
        lo, hi = alvo - T // 4, alvo + T // 4
        if hi >= len(s):
            break
        k = lo + int(np.argmax(s[lo:hi]))
        T = int(0.7 * T + 0.3 * (k - e[-1]))
        e.append(k)
    return [a + k for k in e]


def grao(x, e, k):
    """Grão de 2 períodos centrado na época k, janela de Hann assimétrica (soma 1 entre épocas vizinhas)."""
    l, c, r = e[k - 1], e[k], e[k + 1]
    sobe = 0.5 - 0.5 * np.cos(np.pi * np.arange(c - l) / (c - l))
    desce = 0.5 + 0.5 * np.cos(np.pi * np.arange(r - c) / (r - c))
    return x[l:r] * np.concatenate([sobe, desce]), c - l


def rms_db(v):
    return 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-12)


def vai_e_volta(n_ini, n_fim, passos):
    """Índices de épocas indo e voltando entre n_ini e n_fim (evita repetir sempre o mesmo período)."""
    ida = list(range(n_fim, n_ini - 1, -1)) + list(range(n_ini + 1, n_fim + 1))
    return [ida[i % len(ida)] for i in range(passos)]


def restaurar(x, plano, pasta):
    """Devolve o áudio do take com o fim restaurado. `plano` vem de rev2.json (restauro.<fala>)."""
    corte = plano["corte"]
    total = int(plano["ate"] * SR)
    y = np.zeros(max(total, len(x)))

    # Ruído da sala do próprio take: em loop com cruzamento, por baixo de tudo o que vem depois do corte.
    amb = plano["ambiente"]
    rt = x[int(amb[0] * SR):int(amb[1] * SR)]
    cf = int(0.02 * SR)
    leito = np.zeros(len(y) + len(rt))
    pos = 0
    jan = np.ones(len(rt))
    jan[:cf] = np.linspace(0, 1, cf)
    jan[-cf:] = np.linspace(1, 0, cf)
    while pos < len(y):
        leito[pos:pos + len(rt)] += rt * jan
        pos += len(rt) - cf
    leito = leito[:len(y)]

    # 1. Vogal: original até a época de emenda; depois, grãos dos últimos períodos com o tom caindo até f0_fim.
    v = plano["vogal"]
    e = epocas(x, v["de"], corte)
    e = [k for k in e if k + 2 < int(corte * SR)]
    j = len(e) - 3  # emenda 2 períodos antes do corte (o último período do arquivo pode estar incompleto)
    emenda = e[j]
    desce = 0.5 + 0.5 * np.cos(np.pi * np.arange(emenda - e[j - 1]) / (emenda - e[j - 1]))
    y[:e[j - 1]] = x[:e[j - 1]]
    y[e[j - 1]:emenda] = x[e[j - 1]:emenda] * desce
    T0 = np.median(np.diff(e[-6:]))
    f0_ini = SR / T0
    n_vogal = int(v["estender"] * SR) + (int(corte * SR) - emenda)
    morfo = plano.get("morfo")
    if morfo:
        xd = carregar(os.path.join(pasta, morfo["fonte"] + ".f32"))
        ed = epocas(xd, morfo["de"], morfo["ate"])
        alvo_db = rms_db(x[e[-5]:e[-1]])
        ganho_d = 10 ** ((alvo_db - rms_db(xd[ed[1]:ed[-2]])) / 20)
        n_vogal += int(morfo["dur"] * SR)
    t = emenda
    passos = []
    while t < emenda + n_vogal:
        passos.append(t)
        p = (t - emenda) / n_vogal
        f0 = f0_ini + (v["f0_fim"] - f0_ini) * p
        t += int(SR / f0)
    fonte_v = vai_e_volta(max(1, len(e) - 6), len(e) - 2, len(passos))
    fonte_v[0] = j
    for i, t in enumerate(passos):
        p = i / max(1, len(passos) - 1)
        g, esq = grao(x, e, fonte_v[i])
        # ganho: estável até `queda_de` (fração da vogal) e depois cai até ganho_fim (dB)
        q0 = v.get("queda_de", 0.5)
        ganho = 10 ** ((v["ganho_fim_db"] * max(0.0, (p - q0) / (1 - q0)) ** 1.5) / 20)
        if morfo:
            # mistura de grãos: a vogal original vira a vogal doadora (ex.: "i" → "u") a partir de `morfo.de_p`
            m = min(1.0, max(0.0, (p - morfo["de_p"]) / (1 - morfo["de_p"]) * 1.6))
            if m > 0:
                kd = vai_e_volta(1, len(ed) - 2, len(passos))[i]
                gd, esq_d = grao(xd, ed, kd)
                n = max(len(g), len(gd))
                a = np.zeros(n)
                b = np.zeros(n)
                a[:len(g)] = g
                b[:len(gd)] = gd * ganho_d
                # alinha os centros (épocas) dos dois grãos
                b = np.roll(b, esq - esq_d)
                # mistura com a energia interpolada (sem buraco de volume no meio da transição)
                mix = (1 - m) * a + m * b
                alvo_rms = (1 - m) * np.sqrt(np.mean(a ** 2)) + m * np.sqrt(np.mean(b ** 2))
                g = mix * alvo_rms / (np.sqrt(np.mean(mix ** 2)) + 1e-12)
        ini = t - esq
        y[ini:ini + len(g)] += g * ganho
    fim_vogal = passos[-1] + int(SR / v["f0_fim"])

    # 2. Fechamento (oclusão do "d") e fricativa doadora, com a queda natural dela.
    fr = plano.get("fricativa")
    fim_fala = fim_vogal
    if fr:
        ini_f = fim_vogal + int(plano["fechamento"] * SR)
        xf = carregar(os.path.join(pasta, fr["fonte"] + ".f32"))
        f = xf[int(fr["de"] * SR):int(fr["ate"] * SR)].copy()
        sobe = int(0.004 * SR)
        f[:sobe] *= np.linspace(0, 1, sobe)
        q = int(fr["queda"] * SR)
        f[-q:] *= np.linspace(1, 0, q) ** 2
        alvo = rms_db(x[e[-5]:e[-1]]) + fr["rel_db"]
        f *= 10 ** ((alvo - rms_db(f[: len(f) // 2])) / 20)
        y[ini_f:ini_f + len(f)] += f
        fim_fala = ini_f + len(f)

    # 3. Ruído da sala entra no corte e segue até o fim; antes do corte o próprio take já tem o seu.
    entra = np.clip((np.arange(len(y)) - emenda) / (0.03 * SR), 0, 1)
    y += leito * entra
    return y[:total], {"emenda_s": round(emenda / SR, 4), "f0_ini": round(f0_ini, 1), "fim_vogal_s": round(fim_vogal / SR, 4),
                       "fim_fala_s": round(fim_fala / SR, 4), "periodos": len(passos)}


if __name__ == "__main__":
    ent, sai, plano, pasta = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), sys.argv[4]
    y, info = restaurar(carregar(ent), plano, pasta)
    y.astype(np.float32).tofile(sai)
    print(json.dumps(info, ensure_ascii=False))
