#!/usr/bin/env python3
"""Sons próprios do vlog de Amsterdam (pedido do Diego, 21/10/2026), por síntese, no mesmo método do kit
(`design-system/sons/gerar_sons.py`: WAV 48 kHz, 24 bits, mono, −14 LUFS na janela de 50 ms mais alta,
pico ≤ −1 dBFS). NÃO são sons do DS: valem só para este vídeo, até o Diego aprovar.

- AMS_tambor_v1.wav: rufar de tambores (caixa) em crescendo, para logo antes do "não" do McCrispy.
- AMS_fogos_murchos_v1.wav: rojão que sobe, fraqueja, dá um "puf" sem força e cai assobiando para baixo.

v2 (pedido do Diego, 23/10/2026: "os fogos não; um confete murcho, daqueles que palhaço estoura; tambores mais
graves, com ar de mistério, no mesmo andamento"):
- AMS_tambor_v2.wav: o mesmo rufar (andamento, crescendo e parada seca iguais ao v1), em tambor grave (surdo/tímpano)
  com um bordão grave crescendo por baixo e sala maior. Os harmônicos ficam em 150–600 Hz para o rufar continuar
  audível no alto-falante do celular.
- AMS_confete_murcho_v1.wav: lança-confete que falha: "pfft" sem pressão, língua de sogra murchando e o papel
  caindo devagar.

Uso (de reels/ams-yt):  python scripts/gerar_sons_ams.py [--tambor 3.2] [--versao 2]
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


# ---------- v2 (23/10/2026) ----------
rng2 = np.random.default_rng(20261023)  # semente própria: o v1 continua saindo igual


def ruido2(d):
    return rng2.standard_normal(int(d * SR))


def golpe_grave(vel):
    """Uma batida de tambor grave (surdo/tímpano): membrana em 104 Hz caindo para 96 Hz, modos inarmônicos da
    pele (1,59×, 2,14×, 2,65×) que dão a altura no celular, pele (ruído 180–1800 Hz) e quase nada de agudo."""
    d = 0.32
    tt = gs.t(d)
    f = 96 + 8 * np.exp(-tt / 0.03)
    fase = 2 * np.pi * np.cumsum(f) / SR
    corpo = np.sin(fase) * gs.env_exp(d, 0.11, 0.002)
    modos = sum(a * np.sin(fase * r + rng2.uniform(0, 6.28)) * gs.env_exp(d, tau, 0.002) for r, a, tau in [(1.59, 0.55, 0.06), (2.14, 0.4, 0.045), (2.65, 0.25, 0.03)])
    pele = gs.banda(ruido2(d), 180, 1800) * gs.env_exp(d, 0.02, 0.0008)
    ataque = gs.passa_baixa(gs.banda(ruido2(0.004), 600, 4000) * gs.env_exp(0.004, 0.0012, 0.0001), 3000)
    x = gs.mix((0, corpo * 0.35), (0, modos * 1.0), (0, pele * 0.9), (0, ataque * 0.35))
    return x * (0.55 + 0.45 * vel) * vel


def sala_grande(x, dur=0.9, mix=0.32):
    """Sala maior que a do v1 (o mistério vem do espaço): cauda de ruído escura, decaimento de 0,22 s."""
    ir = gs.passa_baixa(ruido2(dur), 2500) * np.exp(-gs.t(dur) / 0.22)
    ir /= np.sqrt(np.sum(ir ** 2))
    return x + mix * signal.fftconvolve(x, ir)[: len(x)]


def tambor_grave(dur):
    """Rufar v2: mesmo andamento do v1 (21 → 29 toques/s), mesmo crescendo e a mesma parada seca antes do "não";
    timbre de tambor grave, mais um bordão em Lá1 + Mi2 (55 e 82 Hz, com o 2º e o 3º harmônicos para o celular)
    que cresce junto e corta com o rufar."""
    n_total = int((dur + 0.2) * SR)
    out = np.zeros(n_total)
    pos = 0.0
    k = 0
    while pos < dur:
        p = pos / dur
        taxa = 21 + 8 * p ** 1.5
        vel = (0.18 + 0.82 * p ** 1.8) * (1.0 if k % 2 == 0 else 0.86) * rng2.uniform(0.92, 1.05)
        g = golpe_grave(vel)
        i = max(0, int((pos + rng2.uniform(-0.002, 0.002)) * SR))
        fim = min(n_total, i + len(g))
        out[i:fim] += g[: fim - i]
        pos += 1.0 / taxa
        k += 1
    tt = gs.t(n_total / SR)
    swell = np.clip(tt / dur, 0, 1) ** 1.6
    trem = 1 + 0.08 * np.sin(2 * np.pi * 3.1 * tt)
    bordao = sum(a * np.sin(2 * np.pi * f * tt + rng2.uniform(0, 6.28)) for f, a in [(55, 0.2), (82.4, 0.2), (110, 0.3), (164.8, 0.25), (247.2, 0.12)])
    out += bordao * swell * trem * 0.16
    corte = int((dur + 0.04) * SR)
    env = np.ones(n_total)
    env[corte:] = 0
    rampa = int(0.04 * SR)
    env[corte - rampa:corte] = np.linspace(1, 0, rampa) ** 2
    x = sala_grande(out) * env
    return gs.passa_alta(x[: int((dur + 0.06) * SR)], 40)


def confete_murcho():
    """≈ 2,1 s: (1) cordinha puxada (estalo de papelão) e um "pfft" sem pressão, em vez do estouro; (2) língua
    de sogra murchando: zumbido de papel (dente de serra filtrado em formantes de 950 e 2.400 Hz) que desce de
    430 para 170 Hz, perdendo o ar, com uma tremida no fim; (3) o confete caindo devagar (papel picado: estalinhos
    finos e espaçados) e um último papelzinho que pousa."""
    d = 2.15
    out = np.zeros(int(d * SR))

    # 1) cordinha + "pfft" fraco
    corda = gs.ressoador(ruido2(0.03) * gs.env_exp(0.03, 0.004, 0.0002), 520, 5) * 0.5
    corda[:144] += gs.transiente(0.003, 1500, 7000, 0.0008) * 0.35
    pfft = gs.banda(ruido2(0.26), 350, 2600) * gs.env_exp(0.26, 0.07, 0.008) * 0.75
    tok = gs.ressoador(ruido2(0.05) * gs.env_exp(0.05, 0.006, 0.0005), 380, 4) * 0.4
    out[: len(corda)] += corda
    i = int(0.04 * SR)
    out[i:i + len(pfft)] += pfft
    out[i:i + len(tok)] += tok

    # 2) língua de sogra murchando
    dl = 0.95
    tt = gs.t(dl)
    f = 430 * (170 / 430) ** (tt / dl) ** 1.3
    f = f * (1 + 0.035 * np.sin(2 * np.pi * (7 - 4 * tt / dl) * tt) * np.clip((tt - 0.5) / 0.3, 0, 1))
    fase = np.cumsum(f) / SR
    serra = 2 * (fase % 1.0) - 1
    zumbido = gs.ressoador(serra, 950, 3) * 0.6 + gs.ressoador(serra, 2400, 4) * 0.35 + gs.passa_baixa(serra, 600) * 0.3
    ar = gs.banda(ruido2(dl), 800, 4000) * 0.12
    env = np.clip(tt / 0.04, 0, 1) * (1 - tt / dl) ** 0.8 * (1 - 0.25 * tt / dl)
    lingua = (zumbido + ar) * env * 0.5
    i = int(0.16 * SR)
    out[i:i + len(lingua)] += lingua

    # 3) papel picado caindo: estalinhos finos, cada vez mais espaçados e fracos
    pos, gap, amp = 0.2, 0.035, 0.22
    while pos < 1.85:
        dur_p = 0.006
        p = gs.banda(ruido2(dur_p), 3000, 11000) * gs.env_exp(dur_p, 0.0015, 0.0002) * amp * rng2.uniform(0.5, 1.0)
        j = int(pos * SR)
        out[j:j + len(p)] += p
        pos += gap * rng2.uniform(0.5, 1.6)
        gap *= 1.07
        amp *= 0.97
    pousa = gs.banda(ruido2(0.02), 1500, 6000) * gs.env_exp(0.02, 0.004, 0.0005) * 0.2
    j = int(1.95 * SR)
    out[j:j + len(pousa)] += pousa
    return gs.fade_out(gs.passa_alta(sala(out, 0.35, 0.15), 100), 0.06)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tambor", type=float, default=3.2, help="duração do rufar em s (até o golpe final)")
    ap.add_argument("--saida", default="sons")
    ap.add_argument("--versao", type=int, default=1, choices=[1, 2])
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    medidor = gs.pyln.Meter(SR, block_size=0.4)
    arq_rel = os.path.join(a.saida, "sons_ams.json")
    rel = json.load(open(arq_rel, encoding="utf-8")) if os.path.exists(arq_rel) else {}
    if a.versao == 1:
        sons = [
            ("AMS_tambor_v1.wav", tambor(a.tambor), f"McCrispy: rufar em crescendo de {a.tambor:.2f} s, para logo antes do \"não\""),
            ("AMS_fogos_murchos_v1.wav", fogos_murchos(), "McCrispy: fogos murchos logo depois do \"não\""),
        ]
    else:
        sons = [
            ("AMS_tambor_v2.wav", tambor_grave(a.tambor), f"McCrispy: rufar grave em crescendo de {a.tambor:.2f} s (andamento do v1), para logo antes do \"não\""),
            ("AMS_confete_murcho_v1.wav", confete_murcho(), "McCrispy: lança-confete que falha, logo depois do \"não\" (substitui os fogos)"),
        ]
    for nome, x, evento in sons:
        x = np.concatenate([gs.silencio(0.002), x])
        y, l50, pico = gs.normalizar(x, medidor)
        sf.write(os.path.join(a.saida, nome), y.astype(np.float32), SR, subtype="PCM_24")
        rel[nome] = {"evento": evento, "duracao_s": round(len(y) / SR, 3), "lufs_50ms": round(l50, 1), "pico_dbfs": round(pico, 1)}
        print(nome, rel[nome])
    with open(os.path.join(a.saida, "sons_ams.json"), "w", encoding="utf-8") as f:
        json.dump(rel, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
