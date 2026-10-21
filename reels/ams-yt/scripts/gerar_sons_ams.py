#!/usr/bin/env python3
"""Sons próprios do vlog de Amsterdam (pedido do Diego, 21/10/2026), por síntese, no mesmo método do kit
(`design-system/sons/gerar_sons.py`: WAV 48 kHz, 24 bits, mono, −14 LUFS na janela de 50 ms mais alta,
pico ≤ −1 dBFS). NÃO são sons do DS: valem só para este vídeo, até o Diego aprovar.

- AMS_tambor_v1.wav: rufar de tambores (caixa) em crescendo, para logo antes do "não" do McCrispy.
- AMS_fogos_murchos_v1.wav: rojão que sobe, fraqueja, dá um "puf" sem força e cai assobiando para baixo.

Uso (de reels/ams-yt):  python scripts/gerar_sons_ams.py [--tambor 3.2]
"""
import argparse
import json
import os
import sys

import numpy as np
import soundfile as sf
from scipy import signal

sys.path.insert(0, os.path.join("..", "..", "design-system", "sons"))
import gerar_sons as gs  # noqa: E402

SR = gs.SR
rng = np.random.default_rng(20261021)


def ruido(d):
    return rng.standard_normal(int(d * SR))


def golpe(vel):
    """Uma batida de caixa: esteira (ruído 1,2–9 kHz) + corpo (≈ 190 Hz caindo) + casco (330 Hz)."""
    d = 0.16
    tt = gs.t(d)
    esteira = gs.banda(ruido(d), 1200, 9000) * gs.env_exp(d, 0.045, 0.0004)
    f = 175 + 60 * np.exp(-tt / 0.006)
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * gs.env_exp(d, 0.028, 0.0004)
    casco = gs.ressoador(ruido(d) * gs.env_exp(d, 0.01, 0.0003), 330, 6) * 0.6
    ataque = gs.transiente(0.003, 2500, 12000, 0.0008)
    x = gs.mix((0, esteira * 0.55), (0, corpo * 0.5 * (0.6 + 0.4 * vel)), (0, casco * 0.35), (0, ataque * 0.5))
    return x * vel


def sala(x, dur=0.35, mix=0.18):
    """Ambiente curto: convolução com uma cauda de ruído exponencial (sala pequena)."""
    ir = gs.passa_baixa(ruido(dur), 6000) * np.exp(-gs.t(dur) / 0.07)
    ir /= np.sqrt(np.sum(ir ** 2))
    molhado = signal.fftconvolve(x, ir)[: len(x)]
    return x + mix * molhado


def tambor(dur):
    """Rufar em crescendo (pp → ff), com o andamento acelerando de leve (21 → 29 toques/s) e as duas mãos
    alternando. Termina seco, sem prato: o "não" do Diego é o golpe final."""
    n_total = int((dur + 0.2) * SR)
    out = np.zeros(n_total)
    pos = 0.0
    k = 0
    while pos < dur:
        p = pos / dur
        taxa = 21 + 8 * p ** 1.5
        vel = (0.18 + 0.82 * p ** 1.8) * (1.0 if k % 2 == 0 else 0.86) * rng.uniform(0.92, 1.05)
        g = golpe(vel)
        i = int((pos + rng.uniform(-0.002, 0.002)) * SR)
        i = max(0, i)
        fim = min(n_total, i + len(g))
        out[i:fim] += g[: fim - i]
        pos += 1.0 / taxa
        k += 1
    # abafa logo depois do último toque (a mão segura a pele): sem cauda longa antes do "não"
    corte = int((dur + 0.04) * SR)
    env = np.ones(n_total)
    env[corte:] = 0
    rampa = int(0.04 * SR)
    env[corte - rampa:corte] = np.linspace(1, 0, rampa) ** 2
    x = sala(out) * env
    return gs.passa_alta(x[: int((dur + 0.06) * SR)], 80)


def fogos_murchos():
    """≈ 2,4 s: (1) o rojão sobe chiando e assobiando, mas o assobio perde força e desafina; (2) "puf" abafado,
    sem estouro; (3) o assobio desce triste (1,3 kHz → 330 Hz), com estalinhos falhando; (4) um "plic" no chão."""
    d = 2.45
    out = np.zeros(int(d * SR))

    # 1) subida: chiado (ruído com centro subindo) + assobio que sobe e fraqueja no fim
    ds = 0.95
    tt = gs.t(ds)
    env_sobe = np.clip(tt / 0.08, 0, 1) * (1 - 0.35 * (tt / ds) ** 3)
    chiado = np.zeros(len(tt))
    for lo, hi, a in [(1500, 3200, 0.5), (2800, 6500, 0.35)]:
        chiado += gs.banda(ruido(ds), lo, hi) * a
    chiado *= env_sobe * np.linspace(0.7, 1.0, len(tt))
    f = 950 + 1250 * (tt / ds) ** 0.8
    f = f - 520 * np.clip((tt - 0.72) / 0.23, 0, 1) ** 2          # perde força: o tom cai antes do fim
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 9 * tt))               # tremidinho
    assobio = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_sobe * 0.32
    sobe = chiado * 0.6 + assobio
    out[: len(sobe)] += sobe

    # 2) "puf": baixo e abafado (não é estouro)
    dp = 0.22
    puf = gs.passa_baixa(ruido(dp), 420) * gs.env_exp(dp, 0.045, 0.002) * 1.4
    puf += np.sin(2 * np.pi * 95 * gs.t(dp)) * gs.env_exp(dp, 0.05, 0.003) * 0.35
    i = int(0.97 * SR)
    out[i:i + len(puf)] += puf

    # 3) assobio triste descendo, com vibrato que vai ficando lento
    dd = 1.05
    tt = gs.t(dd)
    f = 1300 * (330 / 1300) ** (tt / dd) ** 0.9
    vib = 1 + 0.02 * np.sin(2 * np.pi * (6 - 3 * tt / dd) * tt)
    env = np.clip(tt / 0.05, 0, 1) * (1 - tt / dd) ** 1.3
    desce = np.sin(2 * np.pi * np.cumsum(f * vib) / SR) * env * 0.38
    desce += gs.banda(ruido(dd), 600, 2600) * env * 0.05
    i = int(1.08 * SR)
    out[i:i + len(desce)] += desce

    # estalinhos falhando (cada vez mais espaçados e fracos)
    pos = 1.12
    gap = 0.05
    amp = 0.45
    while pos < 1.95:
        one = gs.transiente(0.003, 2500, 12000, 0.0008) * amp
        j = int(pos * SR)
        out[j:j + len(one)] += one
        pos += gap * rng.uniform(0.7, 1.4)
        gap *= 1.35
        amp *= 0.8

    # 4) "plic" no chão
    pl = gs.mix((0, gs.parcial(2600, 0.12, 0.025, ataque=0.0005) * 0.25), (0, gs.transiente(0.003, 3000, 10000, 0.0007) * 0.3))
    j = int(2.22 * SR)
    out[j:j + len(pl)] += pl[: len(out) - j]
    return gs.fade_out(gs.passa_alta(sala(out, 0.5, 0.25), 90), 0.08)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tambor", type=float, default=3.2, help="duração do rufar em s (até o golpe final)")
    ap.add_argument("--saida", default="sons")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    medidor = gs.pyln.Meter(SR, block_size=0.4)
    rel = {}
    for nome, x, evento in [
        ("AMS_tambor_v1.wav", tambor(a.tambor), f"McCrispy: rufar em crescendo de {a.tambor:.2f} s, para logo antes do \"não\""),
        ("AMS_fogos_murchos_v1.wav", fogos_murchos(), "McCrispy: fogos murchos logo depois do \"não\""),
    ]:
        x = np.concatenate([gs.silencio(0.002), x])
        y, l50, pico = gs.normalizar(x, medidor)
        sf.write(os.path.join(a.saida, nome), y.astype(np.float32), SR, subtype="PCM_24")
        rel[nome] = {"evento": evento, "duracao_s": round(len(y) / SR, 3), "lufs_50ms": round(l50, 1), "pico_dbfs": round(pico, 1)}
        print(nome, rel[nome])
    with open(os.path.join(a.saida, "sons_ams.json"), "w", encoding="utf-8") as f:
        json.dump(rel, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
