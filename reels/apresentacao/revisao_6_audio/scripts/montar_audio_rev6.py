"""Revisão 6, áudio: parte do áudio aprovado da rev. 6 (cenas_v6 + narração tratada) e aplica a nova montagem.

1. Corte novo (Paris, 6,958-8,458 s): por baixo da narração entra o ambiente das pausas do próprio clipe IMG_2978
   (sem a fala dele), com o mesmo ducking e o mesmo nível do ambiente do Arco, crossfade de 0,2 s nos dois cortes.
2. Amsterdam começa 5 quadros depois (19,625 s = IMG_1384 6,508 s): som cru do bruto (Reel da rev. 3); a cena
   anterior termina com o próprio ambiente da pausa entre "Barcelona!" e "Chegamos ao", crossfade de 0,2 s.
3. "Chegamos!": o "s" final vai de IMG 8,80 a ~9,08 s e era engolido pelo crossfade para a Torre Eiffel.
   Agora o som da cena continua 0,09 s por cima da Torre Eiffel (corte em L): agudos do "s" recuperados do
   Reel da rev. 3 (dividindo pela curva do crossfade) até 9,03 s, depois decaimento suave; graves = ambiente da
   própria cena. A Torre Eiffel entra só depois do corte de imagem, em 0,25 s.
4. Tudo depois de Amsterdam anda -0,2083 s (5 quadros). Linha do tempo nominal (sem os 3 ms do limitador da rev. 5).
"""
import json
import os
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

from restaurar import alinhar

AQUI = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(AQUI, "..", "a")
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJ, "scripts"))
import render as R  # noqa: E402

SR = 48000
LAT = 143
GANHO_FINAL = 4.16
SHIFT = 5 / 24                    # Amsterdam e tudo depois: -5 quadros
TOTAL = 989 / 24
meter = pyln.Meter(SR)
rel = {}


def s(t):
    return int(round(t * SR))


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def ep(n):
    """Rampas de potência constante (sai, entra) com n amostras."""
    x = (np.arange(n) + 0.5) / n
    return np.cos(np.pi / 2 * x), np.sin(np.pi / 2 * x)


def lufs(x):
    return float(meter.integrated_loudness(x))


def rms_db(x):
    return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12))


cena_old, _ = sf.read(os.path.join(A, "cenas_v6.wav"), always_2d=True)
cena_old = np.vstack([cena_old[LAT:], np.zeros((LAT, 2))])      # linha do tempo nominal
N = s(TOTAL)
cena = np.zeros((N, 2))

# ---------------------------------------------------------------- até Amsterdam: igual à rev. 6 aprovada
cena[:s(19.525)] = cena_old[:s(19.525)]

# ---------------------------------------------------------------- 1. Paris por baixo da narração
pa, _ = sf.read(os.path.join(AQUI, "..", "novo", "audio.wav"), always_2d=True)
PAUSAS = [(6.10, 6.50), (2.66, 3.04), (7.26, 7.55), (0.03, 0.30)]   # sem fala e sem impulsos (7,57-7,96 s tem toques)
pedacos = [pa[s(a):s(b)] for a, b in PAUSAS]
xf = s(0.06)
amb = pedacos[0].copy()
k = 1
while len(amb) < s(1.85):
    p = pedacos[k % len(pedacos)]
    k += 1
    o, i = ep(xf)
    amb = np.vstack([amb[:-xf], amb[-xf:] * o[:, None] + p[:xf] * i[:, None], p[xf:]])
a0, a1 = s(6.958 - 0.1), s(8.458 + 0.1)
amb = amb[:a1 - a0]
g, _ = sf.read(os.path.join(A, "ganho_v6.wav"), always_2d=True)
g = g[:, 0] / 0.5                                                  # ducking da narração (linha nominal)
amb_d = amb * g[a0:a1, None]
alvo = lufs(cena_old[s(7.06):s(8.36)])                             # nível do ambiente do Arco, já abaixado
amb_d *= 10 ** ((alvo - lufs(amb_d[s(0.2):s(1.4)])) / 20)
n = s(0.2)
o, i = ep(n)
seg = cena[a0:a1].copy()
seg[:n] = cena_old[a0:a0 + n] * o[:, None] + amb_d[:n] * i[:, None]
seg[n:-n] = amb_d[n:-n]
seg[-n:] = amb_d[-n:] * o[:, None] + cena_old[a1 - n:a1] * i[:, None]
cena[a0:a1] = seg
rel["paris"] = {"pausas_do_clipe_s": [list(p) for p in PAUSAS], "lufs_alvo_ambiente_abaixado": round(alvo, 2),
                "crossfades_s": [[6.858, 7.058], [8.358, 8.558]]}

# ---------------------------------------------------------------- 2. fim da cena 7 + Amsterdam cru (IMG 6,508 s em diante)
# fim da cena 7: depois de 19,525 s só há mistura com a cena seguinte; continua com o ambiente da pausa 17,10-17,30 s
x20 = s(0.02)
o2, i2 = ep(x20)
emp = cena_old[s(17.10) - x20:s(17.30)].copy()                      # 20 ms a mais no começo para a emenda
emp *= 10 ** ((rms_db(cena_old[s(19.46):s(19.525)]) - rms_db(emp)) / 20)
# emenda de 20 ms antes de 19,525 s (o real ainda está limpo ali) e o emprestado segue sozinho depois
cena[s(19.525) - x20:s(19.525)] = cena_old[s(19.525) - x20:s(19.525)] * o2[:, None] + emp[:x20] * i2[:, None]
s7 = emp[x20:]                                                      # começa em 19,525 s

r3, _ = sf.read(os.path.join(A, "rev3.wav"), always_2d=True)
c6, _ = sf.read(os.path.join(A, "cenas_v6.wav"), always_2d=True)
desloc = alinhar(r3, 17.0, 19.55, c6, 19.70, 0.3) - int(17.0 * SR)


def r3_idx(img_t):
    """Amostra do Reel da rev. 3 para o instante img_t do IMG_1384 (alinhamento medido por correlação)."""
    return int(round((img_t + 13.325) * SR + LAT - desloc))


rv = json.load(open(os.path.join(A, "v6_relatorio.json")))
g8 = rv["cena8"]["ganho_nivel_dB"]
IMG0, IMG_FIM, IMG_LIMPO = 6.5083 - 0.1, 9.13, 8.9083       # IMG_LIMPO: depois disso a rev. 3 já está no crossfade
pre = 0.2                                                   # pré-rolagem para o passa-altas
raw = r3[r3_idx(IMG0 - pre):r3_idx(IMG_FIM)].copy()
t_img = IMG0 - pre + np.arange(len(raw)) / SR
# "s" final: agudos (>2,5 kHz) da mistura da rev. 3 divididos pela curva de saída do crossfade (qsin) até 9,03 s
c3 = np.cos(np.pi / 2 * np.clip((t_img - IMG_LIMPO) / 0.2, 0, 1))
sos_lp = signal.butter(6, 2500, "lowpass", fs=SR, output="sos")
lp = signal.sosfiltfilt(sos_lp, raw, axis=0)
hp = raw - lp
hp_rec = hp / np.maximum(c3, 0.5)[:, None]
# segunda fonte para o "s" depois de 9,00 s: o Reel da rev. 5, onde o mesmo trecho cruza com a Torre Eiffel (bem menos
# agudos que o metrô da rev. 3). As duas estimativas batem em ±0,5 dB até 9,03 s; a da rev. 5 segue estável até 9,08 s.
r5, _ = sf.read(os.path.join(A, "rev5.wav"), always_2d=True)
i5 = lambda t: int(round((t + 13.325) * SR + LAT))
x5 = r5[i5(IMG0 - pre) + 4:i5(IMG0 - pre) + 4 + len(raw)].copy()    # +4 amostras: defasagem medida (0,086 ms)
hp5 = x5 - signal.sosfiltfilt(sos_lp, x5, axis=0)
ok = (t_img >= 8.82) & (t_img < 8.90)                         # trecho limpo nas duas versões: casa nível e timbre
g5 = rms_db(hp[ok]) - rms_db(hp5[ok])
hp5 *= 10 ** (g5 / 20)
hp5_rec = hp5 / np.maximum(c3, 0.2)[:, None]
w5 = np.clip((t_img - 9.00) / 0.02, 0, 1)[:, None]            # troca rev. 3 -> rev. 5 em 9,00-9,02 s
hf = hp_rec * (1 - w5) + hp5_rec * w5
env_hf = np.clip((9.13 - t_img) / 0.05, 0, 1)                 # final do "s": 9,08 -> 9,13 s (cosseno)
env_hf = np.where(t_img < 9.08, 1.0, 0.5 - 0.5 * np.cos(np.pi * env_hf))
rel["s_ganho_rev5_dB"] = round(float(g5), 2)
# graves depois de 8,908 s: ambiente da própria cena (IMG 7,95-8,17 s, antes da fala), no mesmo nível
lp_emp_src = signal.sosfiltfilt(sos_lp, r3[r3_idx(7.95):r3_idx(8.17)], axis=0)
ref = lp[(t_img >= 8.83) & (t_img < 8.905)]
lp_emp_src *= 10 ** ((rms_db(ref) - rms_db(lp_emp_src)) / 20)
m = t_img >= IMG_LIMPO - 0.01
idx = np.where(m)[0]
lp_tail = lp.copy()
seg_emp = np.resize(lp_emp_src, (len(idx), 2)) if len(idx) > len(lp_emp_src) else lp_emp_src[:len(idx)]
w = np.clip((t_img[idx] - (IMG_LIMPO - 0.01)) / 0.02, 0, 1)[:, None]   # troca de 20 ms
lp_tail[idx] = lp[idx] * (1 - w) + seg_emp * w
env_lf = np.where(t_img < 9.0083, 1.0, 0.5 + 0.5 * np.cos(np.pi * np.clip((t_img - 9.0083) / (IMG_FIM - 9.0083), 0, 1)))
s8 = lp_tail * env_lf[:, None] + hf * env_hf[:, None]
s8 = signal.sosfilt(signal.butter(2, 80, "highpass", fs=SR, output="sos"), s8, axis=0)
s8 = s8[s(pre):] * 10 ** (g8 / 20)                              # começa em IMG 6,4083 s = 19,525 s no Reel
t8 = 19.525 + np.arange(len(s8)) / SR
ramp = np.interp(t8, [19.625, 19.775, 21.19, 21.41], [0, 6, 6, 0], left=0, right=0)   # ambiente +6 dB antes da fala
s8 *= 10 ** (ramp / 20)[:, None]
fim8 = s(19.525) + len(s8)
rel["amsterdam"] = {"inicio_img_s": 6.5083, "fim_som_img_s": IMG_FIM, "ganho_dB": g8,
                    "s_final": "agudos da rev. 3 / curva qsin até 9,00 s e da rev. 5 / curva qsin de 9,02 a 9,08 s, final suave até 9,13 s; graves do ambiente IMG 7,95-8,17 s",
                    "fim_da_cena_7": "ambiente 17,10-17,30 s no lugar da mistura de 19,525-19,725 s"}

# transição 7 -> 8 (crossfade de 0,2 s centrado em 19,625 s)
n = s(0.2)
o, i = ep(n)
b0 = s(19.525)
cena[b0:b0 + n] = s7[:n] * o[:, None] + s8[:n] * i[:, None]
cena[b0 + n:fim8] += s8[n:]

# ---------------------------------------------------------------- 3. Torre Eiffel entra depois do corte (22,125 s)
corte = 22.125
eif = np.zeros((N, 2))
desl = s(SHIFT)
ini_limpo = s(22.4333) - desl                                         # 22,225 s no Reel novo
eif[ini_limpo:] = cena_old[ini_limpo + desl:ini_limpo + desl + (N - ini_limpo)]
L = ini_limpo - s(corte)
emp_e = cena_old[s(22.60):s(22.60) + L + x20]                       # Torre Eiffel limpa, emprestada para 22,125-22,225 s
eif[s(corte):ini_limpo] = emp_e[:L]
eif[ini_limpo:ini_limpo + x20] = emp_e[L:L + x20] * o2[:, None] + cena_old[ini_limpo + desl:ini_limpo + desl + x20] * i2[:, None]
n_in = s(0.25)
fade_in = np.zeros(N)
fade_in[s(corte):s(corte) + n_in] = np.sin(np.pi / 2 * (np.arange(n_in) + 0.5) / n_in)
fade_in[s(corte) + n_in:] = 1
cena[s(corte):] += eif[s(corte):] * fade_in[s(corte):, None]
rel["torre_eiffel"] = {"entra_em_s": corte, "fade_in_s": 0.25, "som_do_chegamos_ate_s": round(19.525 + len(s8) / SR, 3)}

# ---------------------------------------------------------------- narração (mesma da rev. 6 aprovada, sem os 3 ms)
nar, _ = sf.read(os.path.join(A, "nar_v6.wav"), always_2d=True)
f_in, f_out = s(0.03), s(0.1)
nar[:f_in] *= np.linspace(0, 1, f_in)[:, None]
nar[-f_out:] *= np.linspace(1, 0, f_out)[:, None]
voz = np.zeros((N, 2))
voz[s(3.0):s(3.0) + len(nar)] = nar[:N - s(3.0)] * 10 ** (GANHO_FINAL / 20)
mix = cena + voz
n30 = s(0.03)
mix[:n30] *= np.sin(np.linspace(0, np.pi / 2, n30))[:, None] ** 2
sf.write(os.path.join(A, "rev6b_cena.wav"), cena.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(A, "rev6b_voz.wav"), voz.astype(np.float32), SR, subtype="FLOAT")
pre_arq = os.path.join(A, "rev6b_pre.wav")
sf.write(pre_arq, mix.astype(np.float32), SR, subtype="FLOAT")

# ---------------------------------------------------------------- -15 LUFS e pico verdadeiro com margem para o AAC
alvo_i, tp_wav = -15.0, -2.2
ganho, limite = 0.0, 0.9
final = os.path.join(A, "rev6b_final.wav")
for _ in range(8):
    ff("-i", pre_arq, "-af", f"volume={ganho:.2f}dB,alimiter=limit={limite:.3f}:attack=5:release=80:level=disabled:latency=1",
       "-c:a", "pcm_s24le", final)
    mm = R.medir_loudness(final)
    print(f"  final: {mm['I']:.2f} LUFS, pico {mm['TP']:.2f} dBTP (ganho {ganho:+.2f}, limite {limite:.3f})")
    ok_i, ok_tp = abs(mm["I"] - alvo_i) <= 0.2, mm["TP"] <= tp_wav
    if ok_i and ok_tp:
        break
    if not ok_tp:
        limite *= 10 ** ((tp_wav - 0.1 - mm["TP"]) / 20)
    if not ok_i:
        ganho += alvo_i - mm["I"]
rel["final"] = {"ganho_dB": round(ganho, 2), "limite": round(limite, 3), **mm, "duracao_s": round(N / SR, 4)}
json.dump(rel, open(os.path.join(A, "rev6b_relatorio.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(rel, indent=1, ensure_ascii=False))
