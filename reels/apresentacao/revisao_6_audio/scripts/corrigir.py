"""Revisão 6 do áudio: corrige, a partir do Reel da revisão 5, os erros achados no diagnóstico.

1. Narração re-tratada a partir do original (nada de redução de ruído; EQ e compressão mais leves).
2. Ducking: a pausa "visito, / a chegada" (0,55 s) soltava o ducking e o som da cena subia 12 dB. Refaz a curva
   do ducking da rev. 5 e a de uma versão que segura pausas até 0,8 s; aplica a razão entre as duas ao som da cena.
3. Cena 8 (Amsterdam, antes de "Chegamos!"): som da própria cena +6 dB (era um buraco de ~9 dB).
4. Cena 12 (tapa): canal direito 0,48 ms atrasado em relação ao esquerdo; alinhado (a voz perdia 3 dB em mono).
5. Clique de uma amostra no canal direito em 23,976 s (Torre Eiffel): interpolação só nesse ponto.

Tudo em ../a/. Nada é sobrescrito na pasta do projeto.
"""
import json
import os
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal
from scipy.interpolate import CubicSpline

AQUI = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(AQUI, "..", "a")
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJ, "scripts"))
os.environ["REEL_TMP"] = os.path.join(AQUI, "..", "tmp")
import render as R  # noqa: E402

SR = 48000
LAT = 143            # atraso do mix final da rev. 5 (limitador), medido por correlação
GANHO_FINAL = 4.16   # ganho final da rev. 5 (medido): narração a -18 LUFS -> -13,84 no Reel
edl = R.carregar(os.path.join(PROJ, "lista_de_cortes.json"))
nar = edl["narracao"]
INICIO = float(nar["inicio"])
TOTAL = edl["_frames"] / 24
meter = pyln.Meter(SR)
rel = {}


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def lufs_trecho(x, a, b):
    return float(meter.integrated_loudness(x[int(a * SR):int(b * SR)]))


# ------------------------------------------------------------------ 1. narração
bruta = os.path.join(A, "nar_bruta.wav")
va, vb = nar["voz_trecho"]
a0 = nar["corte_tomada"][0]
VOZ = (va - a0, vb - a0)
xb, _ = sf.read(bruta, always_2d=True)
pre = -18.0 - lufs_trecho(xb, *VOZ)
EQ = "highpass=f=80:poles=2,equalizer=f=300:t=o:w=1.0:g=-2,equalizer=f=3000:t=o:w=1.2:g=2"
COMP = {"ratio": 2, "attack": 20, "release": 150, "knee": 4}


def cadeia(limiar=None):
    c = f"{EQ},volume={pre:.2f}dB"
    if limiar is not None:
        c += (f",acompressor=threshold={limiar}dB:ratio={COMP['ratio']}:attack={COMP['attack']}:"
              f"release={COMP['release']}:knee={COMP['knee']}:makeup=1")
    return c


sem_comp = os.path.join(A, "nar_v6_sem_comp.wav")
ff("-i", bruta, "-af", cadeia(), "-c:a", "pcm_f32le", sem_comp)
xs, _ = sf.read(sem_comp, always_2d=True)


def reducao(xc):
    """Redução de ganho do compressor (dB) em janelas de 10 ms, só onde há voz."""
    J = 480
    n = min(len(xs), len(xc)) // J * J
    a = 20 * np.log10(np.sqrt((xs[:n].mean(1).reshape(-1, J) ** 2).mean(1)) + 1e-10)
    b = 20 * np.log10(np.sqrt((xc[:n].mean(1).reshape(-1, J) ** 2).mean(1)) + 1e-10)
    voz = a > a.max() - 30
    return a[voz] - b[voz]


# limiar: o mais baixo (em passos de 1 dB) que mantém a redução nos picos em até 3 dB
escolha = None
for lim in range(-10, -31, -1):
    tmp = os.path.join(A, "nar_v6_teste.wav")
    ff("-i", bruta, "-af", cadeia(lim), "-c:a", "pcm_f32le", tmp)
    xc, _ = sf.read(tmp, always_2d=True)
    gr = reducao(xc)
    if np.percentile(gr, 99.5) > 3.0:
        break
    escolha = (lim, float(np.percentile(gr, 99.5)), float(np.median(gr)))
lim, gr_max, gr_med = escolha
proc = os.path.join(A, "nar_v6.wav")
ff("-i", bruta, "-af", cadeia(lim), "-c:a", "pcm_f32le", proc)
xn, _ = sf.read(proc, always_2d=True)
xn *= 10 ** ((-18.0 - lufs_trecho(xn, *VOZ)) / 20)
sf.write(proc, xn.astype(np.float32), SR, subtype="FLOAT")
rel["narracao"] = {"cadeia": cadeia(lim), "limiar_dB": lim, "reducao_picos_dB": round(gr_max, 2),
                   "reducao_mediana_dB": round(gr_med, 2), "lufs_voz": round(lufs_trecho(xn, *VOZ), 2)}
print("narração:", rel["narracao"])

# ------------------------------------------------------------------ 2. ducking sem soltar nas pausas


def curva_ducking(voz_arq, segurar, nome):
    """Ganho (linear, por amostra) que o sidechaincompress da rev. 5 aplica ao som das cenas."""
    rms_voz = R.rms_ativo_db(voz_arq)
    limiar = rms_voz - float(edl["audio"]["ducking_db"]) / (1 - 1 / 20)
    sc = os.path.join(A, f"sc_{nome}.wav")
    R.sidechain_constante(voz_arq, sc, rms_voz, INICIO, TOTAL, segurar)
    saida = os.path.join(A, f"ganho_{nome}.wav")
    ff("-f", "lavfi", "-i", f"aevalsrc=0.5|0.5:s={SR}:d={TOTAL}", "-i", sc,
       "-filter_complex",
       f"[0:a]aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo[m];"
       f"[1:a]aformat=channel_layouts=stereo,atrim=end={TOTAL}[s];"
       f"[m][s]sidechaincompress=threshold={10 ** (limiar / 20):.5f}:ratio=20:attack=50:"
       f"release={int(edl['audio']['release_ms'])}:knee=2:detection=rms:makeup=1",
       "-c:a", "pcm_f32le", saida)
    g, _ = sf.read(saida, always_2d=True)
    return g[:, 0] / 0.5


nar_rev5 = os.path.join(A, "nar_rev5.wav")
g_old = curva_ducking(nar_rev5, 0.5, "rev5")
g_new = curva_ducking(nar_rev5, 0.8, "v6")
razao = np.ones(int(round(TOTAL * SR)))
n = min(len(g_old), len(g_new), len(razao))
razao[:n] = np.clip(g_new[:n] / np.maximum(g_old[:n], 1e-4), 0.05, 1.0)
razao = np.roll(razao, LAT)
razao[:LAT] = 1
mud = np.where(razao < 0.999)[0]
rel["ducking"] = {"trechos_alterados_s": [round(mud[0] / SR, 3), round(mud[-1] / SR, 3)] if len(mud) else None,
                  "maior_correcao_dB": round(float(20 * np.log10(razao.min())), 2),
                  "reducao_media_rev5_dB": round(float(-20 * np.log10(np.median(g_old[int(3.5 * SR):int(14.5 * SR)]))), 2)}
print("ducking:", rel["ducking"])

# ------------------------------------------------------------------ montagem
mix, _ = sf.read(os.path.join(A, "rev5.wav"), always_2d=True)
v5, _ = sf.read(os.path.join(A, "nar_rev5_no_reel.wav"), always_2d=True)
cena = mix - v5                     # som das cenas da rev. 5 (resíduo limpo, conferido)
cena[:len(razao)] *= razao[:len(cena), None]


def rampa_ganho(n_total, pontos):
    """Curva de ganho em dB por pontos (tempo s, dB), linear entre eles; 0 dB fora."""
    t = np.arange(n_total) / SR
    ts, gs = zip(*pontos)
    g = np.interp(t, ts, gs, left=0, right=0)
    return 10 ** (g / 20)


# 3. cena 8 ("Chegamos!"): refeita com o som CRU do bruto (está intacto no Reel da rev. 3, que não tratava as falas),
#    só com passa-altas de 80 Hz e o mesmo nível de voz da rev. 5; depois +6 dB no som da própria cena antes da fala
from restaurar import alinhar, aplicar, fir_restauro  # noqa: E402
d = LAT / SR
r3, _ = sf.read(os.path.join(A, "rev3.wav"), always_2d=True)
i5 = alinhar(r3, 17.0, 19.55, cena, 19.70, 0.3)          # amostra da rev. 5 que corresponde a 17,0 s da rev. 3
desloc = i5 - int(17.0 * SR)
XF = int(0.03 * SR)
ia, ib = int((19.725 + d) * SR), int((22.233 + d) * SR)   # miolo da cena (fora dos crossfades de 0,2 s)
cru = r3[ia - desloc - XF:ib - desloc + XF].copy()
sos_hp = signal.butter(2, 80, "highpass", fs=SR, output="sos")
cru = signal.sosfilt(sos_hp, cru, axis=0)
va8, vb8 = int((21.65 + d) * SR), int((22.13 + d) * SR)  # "Chegamos!"
g8 = meter.integrated_loudness(cena[va8:vb8]) - meter.integrated_loudness(cru[va8 - ia + XF:vb8 - ia + XF])
cru *= 10 ** (g8 / 20)
w = np.ones(len(cru))
w[:XF] = np.sin(np.linspace(0, np.pi / 2, XF)) ** 2
w[-XF:] = np.cos(np.linspace(0, np.pi / 2, XF)) ** 2
seg = cena[ia - XF:ib + XF]
cena[ia - XF:ib + XF] = seg * (1 - w[:, None]) + cru * w[:, None]
cena *= rampa_ganho(len(cena), [(19.625 + d, 0), (19.775 + d, 6), (21.40 + d, 6), (21.62 + d, 0)])[:, None]
rel["cena8"] = {"fonte": "som cru do bruto IMG_1384 (Reel da rev. 3), passa-altas 80 Hz, sem redução de ruído/EQ/compressão",
                "ganho_nivel_dB": round(float(g8), 2), "alinhamento_amostras": int(desloc),
                "ambiente_antes_da_fala_dB": 6, "trecho_s": [19.625, 21.62]}

# 4. cena 12: alinha o canal direito (atrasado 23 amostras) só dentro da cena, com transição de 40 ms
a12, b12 = int((30.417 + d) * SR), int((34.958 + d) * SR)
k = 23
Ralin = np.roll(cena[:, 1], -k)
peso = np.zeros(len(cena))
x40 = int(0.04 * SR)
peso[a12:b12] = 1
peso[a12 - x40:a12] = np.linspace(0, 1, x40)
peso[b12:b12 + x40] = np.linspace(1, 0, x40)
cena[:, 1] = cena[:, 1] * (1 - peso) + Ralin * peso
rel["cena12"] = {"alinhamento_amostras": k, "ms": round(k / SR * 1000, 2)}

# 5. clique no canal direito em 23,976 s: interpola 12 amostras
c0 = 1150841 + LAT * 0  # posição medida já no arquivo da rev. 5
a_, b_ = c0 - 6, c0 + 6
viz = np.r_[np.arange(a_ - 24, a_), np.arange(b_, b_ + 24)]
cena[a_:b_, 1] = CubicSpline(viz, cena[viz, 1])(np.arange(a_, b_))
rel["clique"] = {"tempo_s": round(c0 / SR, 4), "amostras": int(b_ - a_), "canal": "direito"}

# 6. falas 7, 11 e 12: devolve os agudos que a redução de ruído da rev. 5 tirou (EQ de fase linear, só acima de 2 kHz,
#    calibrado pela perda medida contra o som cru das revisões 1 e 3; Bruges não tem cru: usa a média de 7 e 8)
perdas = json.load(open(os.path.join(AQUI, "perdas_falas.json")))
c07 = np.array(perdas["perda"]["07"])
c12 = np.convolve(np.pad(np.array(perdas["perda"]["12"]), 1, mode="edge"), np.ones(3) / 3, mode="valid")
media = np.array(perdas["media_07_08"])
restauro = []
for a_s, b_s, curva, nome in [(14.917, 19.625, c07, "07 Buenos días"), (27.417, 30.417, media, "11 Bruges"),
                             (30.417, 34.958, c12, "12 tapa")]:
    h = fir_restauro(curva)
    eqd = aplicar(cena, h)
    t_ = np.arange(len(cena)) / SR
    peso = np.interp(t_, [a_s - 0.05 + d, a_s + 0.05 + d, b_s - 0.05 + d, b_s + 0.05 + d], [0, 1, 1, 0], left=0, right=0)
    cena = cena + peso[:, None] * (eqd - cena)
    g = np.clip(-curva, 0, 6)
    restauro.append({"cena": nome, "ganho_por_banda_dB": {int(c): round(float(v), 1) for c, v in zip(perdas["CS"], g) if c >= 2000}})
rel["restauro_agudos"] = restauro

# 1b. narração nova no mesmo lugar da antiga (mesmos fades do render)
v = xn.copy()
f_in, f_out = int(0.03 * SR), int(0.1 * SR)
v[:f_in] *= np.linspace(0, 1, f_in)[:, None]
v[-f_out:] *= np.linspace(1, 0, f_out)[:, None]
t0 = int(INICIO * SR) + LAT
voz_reel = np.zeros_like(cena)
voz_reel[t0:t0 + len(v)] = v[:len(cena) - t0] * 10 ** (GANHO_FINAL / 20)
sf.write(os.path.join(A, "nar_v6_no_reel.wav"), voz_reel.astype(np.float32), SR, subtype="FLOAT")
sf.write(os.path.join(A, "cenas_v6.wav"), cena.astype(np.float32), SR, subtype="FLOAT")
pre_mix = cena + voz_reel
# entrada de 30 ms no começo do Reel: o som da cena começava cheio na amostra 0 (degrau = clique ao dar play e pico no AAC)
n15 = int(0.030 * SR)
pre_mix[:n15] *= np.sin(np.linspace(0, np.pi / 2, n15))[:, None] ** 2
pre_arq = os.path.join(A, "v6_pre.wav")
sf.write(pre_arq, pre_mix.astype(np.float32), SR, subtype="FLOAT")

# ------------------------------------------------------------------ -15 LUFS / pico verdadeiro <= -1,5 dBTP (margem p/ AAC)
alvo, tp_wav = -15.0, -2.2
ganho, limite = 0.0, 0.9
final = os.path.join(A, "v6_final.wav")
for _ in range(8):
    ff("-i", pre_arq, "-af", f"volume={ganho:.2f}dB,alimiter=limit={limite:.3f}:attack=5:release=80:level=disabled:latency=1",
       "-c:a", "pcm_s24le", final)
    m = R.medir_loudness(final)
    print(f"  final: {m['I']:.2f} LUFS, pico {m['TP']:.2f} dBTP (ganho {ganho:+.2f}, limite {limite:.3f})")
    ok_i, ok_tp = abs(m["I"] - alvo) <= 0.2, m["TP"] <= tp_wav
    if ok_i and ok_tp:
        break
    if not ok_tp:
        limite *= 10 ** ((tp_wav - 0.1 - m["TP"]) / 20)
    if not ok_i:
        ganho += alvo - m["I"]
rel["final"] = {"ganho_dB": round(ganho, 2), "limite": round(limite, 3), **m}
json.dump(rel, open(os.path.join(A, "v6_relatorio.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(rel, indent=1, ensure_ascii=False))
