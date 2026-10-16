#!/usr/bin/env python3
"""Sons da marca Primeiro Dia (DS V2, 4.6), gerados por síntese.

Gera os 9 sons do kit (`PD_*_v1.wav`) e o som de moeda (`PD_moeda_v1.wav`, pedido do
Diego em 16/10/2026, fora da tabela 4.6). Cada som imita o objeto da lista de gravação
(LISTA_DE_GRAVACAO.md): assadeira + régua, carimbo na madeira, taça + furador etc.

Formato: WAV 48 kHz, 24 bits, mono (DS V2, 6.1).
Nível: todos saem com a mesma loudness de evento: −14 LUFS K-ponderados na janela de 50 ms
mais alta (BS.1770), com pico ≤ −1 dBFS. Quando o pico não deixa chegar a −14, o arquivo
fica no pico de −1 dBFS e o relatório (sons_v1.json) mostra o nível real. O volume relativo
à voz (−10 dB do clack, −6 dB do tum…) é aplicado na mixagem, não no arquivo.

Uso (de dentro desta pasta):
    python3 gerar_sons.py            # gera os 10 arquivos aqui
    python3 gerar_sons.py --saida X  # gera em outra pasta

Dependências: numpy, scipy, soundfile, pyloudnorm.
Determinístico: a mesma semente gera os mesmos arquivos.
"""
import argparse
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000
ALVO_LUFS = -14.0
PICO_DBFS = -1.0
rng = np.random.default_rng(20261016)


# ---------- blocos ----------
def t(dur):
    return np.arange(int(dur * SR)) / SR


def silencio(dur):
    return np.zeros(int(dur * SR))


def env_exp(dur, tau, ataque=0.0005):
    """Envelope com ataque linear curto e queda exponencial (tau em s)."""
    tt = t(dur)
    e = np.exp(-tt / tau)
    if ataque > 0:
        a = np.clip(tt / ataque, 0, 1)
        e = e * a
    return e


def parcial(f, dur, tau, fase=None, ataque=0.0005, detune=0.0):
    tt = t(dur)
    ph = rng.uniform(0, 2 * np.pi) if fase is None else fase
    freq = f * (1 + detune * np.exp(-tt / 0.02))
    return np.sin(2 * np.pi * np.cumsum(freq) / SR + ph) * env_exp(dur, tau, ataque)


def ruido(dur):
    return rng.standard_normal(int(dur * SR))


def banda(x, lo, hi, ordem=4):
    sos = signal.butter(ordem, [lo, hi], btype="bandpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def passa_baixa(x, f, ordem=4):
    sos = signal.butter(ordem, f, btype="lowpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def passa_alta(x, f, ordem=4):
    sos = signal.butter(ordem, f, btype="highpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def ressoador(x, f, q):
    """Filtro de pico (corpo de madeira, plástico)."""
    b, a = signal.iirpeak(f, q, fs=SR)
    return signal.lfilter(b, a, x)


def mix(*partes):
    n = max(int(pos * SR) + len(p) for pos, p in partes)
    out = np.zeros(n)
    for pos, p in partes:
        i = int(pos * SR)
        fim = min(n, i + len(p))
        if i < n:
            out[i:fim] += p[: fim - i]
    return out


def colocar(x, total):
    out = np.zeros(int(total * SR))
    out[: min(len(x), len(out))] = x[: len(out)]
    return out


def fade_out(x, dur=0.01):
    n = min(len(x), int(dur * SR))
    x = x.copy()
    x[-n:] *= np.linspace(1, 0, n) ** 2
    return x


def transiente(dur=0.004, lo=2000, hi=12000, tau=0.0012):
    return banda(ruido(dur), lo, min(hi, SR / 2 - 100)) * env_exp(dur, tau, 0.0001)


# ---------- os sons ----------
def clack():
    """Placa assenta: chapa fina de metal + régua. 80 ms + cauda curta (−10 dB)."""
    d = 0.22
    metal = sum(
        a * parcial(f, d, tau, detune=0.015)
        for f, a, tau in [(1180, 0.55, 0.030), (2730, 0.9, 0.024), (4410, 0.7, 0.018),
                          (6190, 0.45, 0.012), (8350, 0.3, 0.008), (3390, 0.35, 0.040)]
    )
    corpo = parcial(190, d, 0.018, ataque=0.0008) * 0.6
    golpe = transiente(0.006, 1500, 14000, 0.0016) * 1.6
    x = mix((0, metal * 0.5), (0, corpo), (0, golpe))
    return fade_out(passa_alta(x, 90), 0.05)


def tum():
    """Carimbo de borracha em mesa de madeira, abafado. ≈ 160 ms (−6 dB)."""
    d = 0.30
    tt = t(d)
    f = 70 + 75 * np.exp(-tt / 0.018)
    grave = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, 0.055, 0.0015)
    madeira = ressoador(ruido(d) * env_exp(d, 0.012, 0.0005), 230, 6) * 0.9
    madeira += ressoador(ruido(d) * env_exp(d, 0.008, 0.0005), 410, 8) * 0.5
    borracha = banda(ruido(0.03), 250, 1400) * env_exp(0.03, 0.006, 0.0008) * 0.6
    x = mix((0, grave * 1.0), (0, madeira * 0.25), (0, borracha))
    return fade_out(passa_baixa(x, 2200), 0.08)


def ding():
    """Ticket SURPREENDE: taça de vidro fina (≈ 600 ms) + clique do furador logo depois."""
    d = 1.0
    f0 = 1318.5  # Mi6, taça pequena
    vidro = sum(
        a * parcial(f0 * r, d, tau, ataque=0.0008)
        for r, a, tau in [(1.0, 1.0, 0.42), (2.32, 0.45, 0.20), (4.25, 0.22, 0.09),
                          (6.63, 0.10, 0.05), (1.003, 0.35, 0.40)]
    )
    toque = transiente(0.003, 3000, 15000, 0.0008) * 0.5
    # furador: aperto (clique seco) + soltura 45 ms depois
    def clique_furador(ganho):
        snap = transiente(0.005, 1800, 9000, 0.0014) * 1.4
        mola = ressoador(ruido(0.04) * env_exp(0.04, 0.006), 2600, 12) * 0.25
        return (mix((0, snap), (0, mola))) * ganho
    furo = mix((0, clique_furador(1.0)), (0.045, clique_furador(0.45)))
    x = mix((0, vidro * 0.55), (0, toque), (0.11, furo * 0.9))
    return fade_out(passa_alta(x, 150), 0.25)


def clique():
    """Caneta retrátil: 2 cliques com ≈ 0,2 s entre eles (−8 dB)."""
    def um(pitch, ganho):
        snap = transiente(0.003, 2500, 14000, 0.0007) * 1.3
        plastico = ressoador(ruido(0.03) * env_exp(0.03, 0.004), 3400 * pitch, 9) * 0.35
        plastico += ressoador(ruido(0.03) * env_exp(0.03, 0.003), 5600 * pitch, 10) * 0.2
        return mix((0, snap), (0, plastico)) * ganho
    x = mix((0, um(1.0, 1.0)), (0.2, um(0.93, 0.8)))
    return fade_out(colocar(passa_alta(x, 400), 0.30), 0.03)


def tick():
    """Placar/preço girando: clique mecânico baixo, ≈ 40 ms (−14 dB)."""
    snap = transiente(0.003, 1200, 9000, 0.0009)
    roda = parcial(1850, 0.04, 0.006) * 0.5 + parcial(3180, 0.04, 0.004) * 0.3
    dente = parcial(420, 0.04, 0.007, ataque=0.0006) * 0.4
    x = mix((0, snap), (0, roda), (0, dente))
    return fade_out(passa_alta(x, 120), 0.012)


def impressora():
    """Recibo saindo: impressora térmica curta, 300 ms (−14 dB)."""
    d = 0.30
    tt = t(d)
    # motor de passo: trem de pulsos a ≈ 560 Hz com leve variação
    fpasso = 560 + 25 * np.sin(2 * np.pi * 7 * tt)
    fase = np.cumsum(fpasso) / SR
    pulsos = (np.mod(fase, 1.0) < 0.12).astype(float)
    pulsos = banda(pulsos, 400, 6000) * 0.9
    chiado = banda(ruido(d), 2500, 9000) * 0.08
    zumbido = np.sin(2 * np.pi * 2350 * tt) * 0.06
    corpo = (pulsos + chiado + zumbido)
    # avanço do papel: 3 trancos
    am = 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 10 * tt))
    env = np.clip(tt / 0.012, 0, 1) * np.clip((d - tt) / 0.04, 0, 1)
    x = corpo * am * env
    corte = mix((d - 0.035, transiente(0.004, 1500, 8000, 0.001) * 0.8))
    return fade_out(mix((0, x), (0, corte)), 0.02)


def obturador():
    """Transição Snap: obturador mecânico, ≈ 100 ms (−12 dB)."""
    def cortina(ganho, cor):
        golpe = transiente(0.006, 900, 9000, 0.0018) * 1.2
        mec = ressoador(ruido(0.05) * env_exp(0.05, 0.008), cor, 7) * 0.4
        baque = parcial(160, 0.05, 0.010, ataque=0.0008) * 0.35
        return mix((0, golpe), (0, mec), (0, baque)) * ganho
    x = mix((0, cortina(1.0, 1900)), (0.055, cortina(0.75, 2300)))
    return fade_out(colocar(passa_alta(x, 80), 0.13), 0.02)


def whoosh():
    """Só no Arrasto: ar, sem graves, 200 ms (−16 dB)."""
    d = 0.20
    tt = t(d)
    n = ruido(d)
    # filtro de banda que varre 900 → 3800 → 1600 Hz (passagem da vareta)
    centro = 900 + 2900 * np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.5
    out = np.zeros_like(n)
    bloco = 256
    zi = None
    for i in range(0, len(n), bloco):
        c = float(np.mean(centro[i:i + bloco]))
        sos = signal.butter(2, [c * 0.75, min(c * 1.35, SR / 2 - 100)], btype="bandpass", fs=SR, output="sos")
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        out[i:i + bloco], zi = signal.sosfilt(sos, n[i:i + bloco], zi=zi)
    env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 2.2
    return fade_out(passa_baixa(passa_alta(out * env, 300, 6), 9000), 0.02)


def nascer():
    """Fechamento (opcional): nota grave suave, Dó3, dura o Nascer (≈ 700 ms)."""
    d = 1.4
    f0 = 130.81
    tt = t(d)
    nota = sum(
        a * np.sin(2 * np.pi * f0 * k * tt * (1 + 0.0004 * k * k) + rng.uniform(0, 6.28)) * np.exp(-tt / tau)
        for k, a, tau in [(1, 1.0, 0.75), (2, 0.42, 0.5), (3, 0.2, 0.32), (4, 0.09, 0.22), (5, 0.04, 0.15)]
    )
    ataque = np.clip(tt / 0.018, 0, 1)
    martelo = passa_baixa(ruido(d) * env_exp(d, 0.006), 900) * 0.05
    x = (nota * ataque + martelo)
    x = passa_baixa(x, 1800)
    return fade_out(x, 0.5)


def moeda():
    """Moeda caindo no balcão: tilintar metálico com 2 quiques (pedido do Diego, 16/10/2026)."""
    def batida(ganho, dur, brilho=1.0):
        metal = sum(
            a * parcial(f * brilho, dur, tau, ataque=0.0003)
            for f, a, tau in [(3620, 1.0, 0.16), (5870, 0.7, 0.11), (8140, 0.45, 0.07),
                              (10250, 0.25, 0.05), (2190, 0.3, 0.09)]
        )
        golpe = transiente(0.003, 3000, 16000, 0.0007) * 0.8
        return mix((0, metal * 0.5), (0, golpe)) * ganho
    x = mix((0, batida(1.0, 0.5)), (0.115, batida(0.55, 0.35, 1.01)), (0.19, batida(0.3, 0.3, 1.015)),
            (0.235, batida(0.14, 0.25, 1.02)))
    return fade_out(passa_alta(x, 600), 0.15)


SONS = {
    # nome: (função, evento, duração final de referência na lista de gravação)
    "clack": (clack, "Placa assenta (Chegada, 280 ms) e Varredura de Placa", "80 ms + cauda curta"),
    "tum": (tum, "Carimbo PERRENGUE, no impacto", "≈ 160 ms"),
    "ding": (ding, "Ticket SURPREENDE, furo da estrela (ding + furador)", "≈ 600 ms + 100 ms"),
    "clique": (clique, "Bilhete: início da escrita (2 cliques)", "≈ 300 ms"),
    "tick": (tick, "Placar e preço girando (1 por giro)", "≈ 40 ms"),
    "impressora": (impressora, "Recibo saindo impresso", "300 ms"),
    "obturador": (obturador, "Transição Snap", "≈ 100 ms"),
    "whoosh": (whoosh, "Só na transição Arrasto", "200 ms"),
    "nascer": (nascer, "Fechamento: o 1º nasce (opcional)", "≈ 700 ms"),
    "moeda": (moeda, "Fora da tabela 4.6: evento a definir pelo Diego", "≈ 400 ms"),
}


def nivel_curto(x, medidor):
    """Loudness K-ponderada (BS.1770) máxima em janelas de 50 ms, em LUFS.

    A janela de 400 ms da loudness momentânea mede mal um clique de 3 ms; 50 ms
    aproxima o que o ouvido percebe num evento curto e vale igual para todos os sons."""
    k = x.copy()
    for filtro in medidor._filters.values():
        k = filtro.apply_filter(k)
    n = int(0.05 * SR)
    ms = np.convolve(k ** 2, np.ones(n) / n, mode="valid") if len(k) >= n else np.array([np.mean(k ** 2)])
    return -0.691 + 10 * np.log10(np.max(ms) + 1e-20)


def normalizar(x, medidor):
    x = x / (np.max(np.abs(x)) + 1e-12)
    ganho_nivel = 10 ** ((ALVO_LUFS - nivel_curto(x, medidor)) / 20)
    ganho_pico = 10 ** (PICO_DBFS / 20)  # x já tem pico 1,0
    y = x * min(ganho_nivel, ganho_pico)
    return y, nivel_curto(y, medidor), 20 * np.log10(np.max(np.abs(y)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    medidor = pyln.Meter(SR, block_size=0.4)
    relatorio = {}
    for nome, (fn, evento, ref) in SONS.items():
        x = fn()
        # 2 ms de silêncio antes do ataque: o evento começa no quadro certo
        x = np.concatenate([silencio(0.002), x])
        y, mom, pico = normalizar(x, medidor)
        arq = os.path.join(args.saida, f"PD_{nome}_v1.wav")
        sf.write(arq, y.astype(np.float32), SR, subtype="PCM_24")
        relatorio[f"PD_{nome}_v1.wav"] = {
            "evento": evento, "duracao_ref": ref, "duracao_s": round(len(y) / SR, 3),
            "lufs_50ms": round(mom, 1), "pico_dbfs": round(pico, 1),
        }
        print(f"PD_{nome}_v1.wav  {len(y) / SR:5.3f} s  L50 {mom:6.1f} LUFS  pico {pico:5.1f} dBFS")
    with open(os.path.join(args.saida, "sons_v1.json"), "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
