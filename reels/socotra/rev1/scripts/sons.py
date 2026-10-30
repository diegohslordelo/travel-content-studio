"""Efeitos sonoros do Reel de Socotra: o kit de transição PDX_* (design-system/sons/externos, CC0) nos volumes de trabalho de
docs/REFERENCIA_EDICAO_FORMATOS.md (4.1), mais um "drone" de ficção científica sintetizado aqui, só sob o gancho (corta na palavra
"real"). Os sons do DS V2 só entram no CTA (clack, tocado pela composição). Ninguém ouviu ainda: a escuta é do Diego (CLAUDE.md, 12).

Base: sons.py do Reel do Gaudí (impacto, sino e whoosh sintetizados ficam disponíveis, mas este Reel usa os PDX_*).

  impacto · golpe grave com harmônicos (a maior parte da energia em 80–400 Hz, para soar no alto-falante do celular), nas datas e
            números em tela cheia ("1926", "TRÊS DIAS", "1/4", "100 ANOS")
  sino    · duas batidas curtas de sino de bonde, quando o bonde entra
  whoosh  · ar, sem graves, nas 2 transições com movimento (fotos lado a lado; cartão da bênção saindo da torre)

Uso (reel.py): mixar(lista, resolver, total, voz_lufs, saida). O nível de cada som é relativo ao loudness da voz.
Para gerar os arquivos soltos (para ouvir): python3 scripts/sons.py → sons/*.wav
"""
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import butter, istft, sosfilt, stft

SR = 48000
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RNG = np.random.default_rng(1926)


def _bp(x, lo, hi):
    return sosfilt(butter(4, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def _fade(y, ms_in=2, ms_out=30):
    a, b = int(SR * ms_in / 1000), int(SR * ms_out / 1000)
    y[:a] *= np.linspace(0, 1, a)
    y[-b:] *= np.linspace(1, 0, b)
    return y


def impacto(dur=1.4):
    t = np.arange(int(dur * SR)) / SR
    f = 85 + (190 - 85) * np.exp(-t / 0.08)  # tom cai rápido de 190 para 85 Hz
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.24)
    corpo = np.tanh(5.0 * corpo) / np.tanh(5.0)  # saturação: harmônicos de 120–500 Hz, audíveis no celular
    batida = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.08) * 0.8  # "toque" do golpe
    estalo = _bp(RNG.standard_normal(len(t)), 600, 4000) * np.exp(-t / 0.018) * 0.6
    ar = sosfilt(butter(2, 500, "lowpass", fs=SR, output="sos"), RNG.standard_normal(len(t))) * np.exp(-t / 0.5) * 0.12
    y = sosfilt(butter(2, 40, "highpass", fs=SR, output="sos"), 0.85 * corpo + batida + estalo + ar)
    return _fade(y / np.abs(y).max() * 0.9, 1, 60)


def sino(dur=1.7):
    t = np.arange(int(dur * SR)) / SR
    f0 = 1180.0
    parciais = [(1.0, 1.0, 1.1), (2.0, 0.32, 0.65), (2.76, 0.48, 0.5), (4.1, 0.2, 0.3), (5.4, 0.12, 0.2)]
    def batida(t0, ganho):
        tt = np.clip(t - t0, 0, None)
        on = (t >= t0).astype(float)
        s = sum(a * np.sin(2 * np.pi * f0 * r * tt + r) * np.exp(-tt / d) for r, a, d in parciais)
        s += 0.15 * np.sin(2 * np.pi * (f0 * 1.004) * tt) * np.exp(-tt / 1.0)  # batimento lento, como metal real
        clique = _bp(RNG.standard_normal(len(t)), 2000, 7000) * np.exp(-tt / 0.004) * 0.25
        return on * ganho * (s + clique)
    y = batida(0.0, 1.0) + batida(0.21, 0.72)
    return _fade(y / np.abs(y).max() * 0.9, 1, 80)


def whoosh(dur=0.55):
    n = int(dur * SR)
    x = RNG.standard_normal(n + 4096)
    f, tt, Z = stft(x, fs=SR, nperseg=1024)
    p = np.clip(tt / dur, 0, 1)
    centro = 450 + 2300 * np.sin(np.pi * np.clip(p / 0.72, 0, 1) / 2) ** 2 * (1 - 0.6 * np.clip((p - 0.72) / 0.28, 0, 1))
    banda = np.exp(-0.5 * (np.log(np.maximum(f[:, None], 1) / centro[None, :]) / 0.45) ** 2)
    env = np.where(p < 0.7, np.sin(np.pi * p / 1.4) ** 1.6, np.cos(np.pi * (p - 0.7) / 0.6) ** 2)
    _, y = istft(Z * banda * env[None, :], fs=SR, nperseg=1024)
    y = sosfilt(butter(2, 180, "highpass", fs=SR, output="sos"), y[:n])
    return _fade(y / np.abs(y).max() * 0.9, 5, 40)


EXTERNOS = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "sons", "externos"))


def _pdx(nome):
    def ler():
        y, sr = sf.read(os.path.join(EXTERNOS, f"PDX_{nome}.wav"), always_2d=True)
        y = y.mean(axis=1)
        if sr != SR:
            from scipy.signal import resample_poly
            y = resample_poly(y, SR, sr)
        return y
    return ler


def drone(dur=5.0):
    """Pad grave de "ficção científica": 55 Hz + quinta + oitava com batimento lento e brilho filtrado que sobe."""
    t = np.arange(int(dur * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.17 * t * (i + 1))) for i, (f, a) in enumerate([(55, 1.0), (55.4, 0.6), (82.4, 0.5), (110, 0.35), (164.8, 0.18)]))
    ar = _bp(RNG.standard_normal(len(t)), 1800, 5200) * (0.04 + 0.05 * t / dur)
    y = y / 2.6 + ar
    y *= np.minimum(1, t / 0.6)
    return _fade(y / np.abs(y).max() * 0.9, 1, 20)


SONS = {"impacto": _pdx("impacto"), "swish": _pdx("swish"), "riser": _pdx("riser"), "ar_longo": _pdx("ar_longo"),
        "pagina": _pdx("pagina"), "obturador": _pdx("obturador"), "drone": drone, "impacto_sint": impacto, "sino": sino, "whoosh": whoosh}


def mixar(lista, resolver, total, voz_lufs, saida):
    """lista: [{"som": nome, "em": âncora/segundos, "rel_db": dB abaixo da voz}] → WAV estéreo com o comprimento do Reel."""
    medidor = pyln.Meter(SR)
    pista = np.zeros(int(total * SR) + SR)
    feitos = []
    cache = {}
    for ev in lista:
        if ev["som"] not in cache:
            cache[ev["som"]] = SONS[ev["som"]]()
        y = cache[ev["som"]].copy()
        lufs = medidor.integrated_loudness(np.concatenate([y, np.zeros(int(0.5 * SR))]))
        alvo = voz_lufs + ev["rel_db"]
        y *= 10 ** ((alvo - lufs) / 20)
        if "ate" in ev:  # corta no instante (ex.: o drone acaba seco na palavra "real")
            n = max(0, int((float(resolver(ev["ate"])) - float(resolver(ev.get("em", 0)))) * SR))
            y = y[:n]
            y[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
        if "em_fim" in ev:  # o som termina na âncora (riser: sobe até o corte)
            t = float(resolver(ev["em_fim"])) - len(y) / SR
        else:
            t = float(resolver(ev["em"]))
        k = int(round(t * SR))
        fim = min(len(pista), k + len(y))
        pista[k:fim] += y[:fim - k]
        feitos.append({"som": ev["som"], "em_s": round(t, 3), "lufs": round(alvo, 1), "rel_db": ev["rel_db"]})
    pista = pista[:int(total * SR)]
    estereo = np.stack([pista, pista], axis=1) * 0.7071  # mono centralizado, como a voz
    sf.write(saida, estereo.astype(np.float32), SR, subtype="FLOAT")
    return feitos


if __name__ == "__main__":
    os.makedirs(os.path.join(AQUI, "sons"), exist_ok=True)
    for nome, fn in SONS.items():
        sf.write(os.path.join(AQUI, "sons", f"{nome}.wav"), fn().astype(np.float32), SR, subtype="PCM_24")
        print(f"sons/{nome}.wav")
    sys.exit(0)
