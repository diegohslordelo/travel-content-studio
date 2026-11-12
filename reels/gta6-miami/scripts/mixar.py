"""Mixagem do Reel: voz decupada + efeitos (rev1/sfx.json) + master −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP (DS V2, 4.6).
Volume de cada efeito relativo à voz (REFERENCIA_EDICAO_FORMATOS 4.1), pela conta do design-system/sons/README.md:
  ganho do som (dB) = loudness da voz + volume relativo − loudness do evento (BS.1770 na janela de 50 ms mais alta).
Saída: public/voz.wav (voz tratada) e rev1/audio_master.wav. Uso (de dentro de reels/gta6-miami): python3 scripts/mixar.py"""
import json, subprocess
import numpy as np, pyloudnorm as pyln

SR = 48000
SONS = {"PD_clack": "../../design-system/sons/PD_clack_v1.wav"}
for n in ("PDX_impacto", "PDX_swish", "PDX_ar_longo", "PDX_obturador", "PDX_riser", "PDX_pagina"):
    SONS[n] = f"../../design-system/sons/externos/{n}.wav"


def ler(arq, filtros=None):
    cmd = ["ffmpeg", "-v", "error", "-i", arq] + (["-af", filtros] if filtros else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()


def grava(arq, x, canais=1):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(canais), "-i", "-", "-c:a", "pcm_s24le", arq],
                   input=x.astype(np.float32).tobytes(), check=True)


med = pyln.Meter(SR)
def evento(x):  # loudness do evento: janela de 50 ms mais alta (com o filtro K do medidor em blocos de 400 ms não dá: usa RMS K-ponderado)
    k = pyln.Meter(SR, block_size=0.05)
    return k.integrated_loudness(np.pad(x, (0, max(0, int(0.4 * SR) - len(x))))) if len(x) else -70


voz = ler("_tmp/voz_bruta.wav", "highpass=f=70")
lufs_voz = med.integrated_loudness(voz)
cfg = json.load(open("rev1/sfx.json"))
n = int(round(cfg["fim_s"] * SR))
pista = np.zeros(n, np.float32)
pista[:len(voz)] += voz[:n]
efeitos = np.zeros(n, np.float32)
rel = []
for e in cfg["efeitos"]:
    x = ler(SONS[e["som"]])
    # loudness do evento: maior loudness de curto prazo em janelas de 50 ms (K-ponderada)
    w = int(0.05 * SR)
    kx = pyln.IIRfilter(4.0, 1 / np.sqrt(2), 1500.0, SR, "high_shelf").apply_filter(x)
    kx = pyln.IIRfilter(0.0, 0.5, 38.0, SR, "high_pass").apply_filter(kx)
    ms = max(np.mean(kx[i:i + w] ** 2) for i in range(0, max(1, len(kx) - w), w // 4))
    ev = -0.691 + 10 * np.log10(ms + 1e-12)
    g = 10 ** ((lufs_voz + e["db"] - ev) / 20)
    ini = e["s"]
    if e.get("pico"):  # o pico do som cai no instante marcado
        ini -= np.argmax(np.abs(x)) / SR
    a = int(round(ini * SR))
    b = min(n, a + len(x))
    efeitos[max(0, a):b] += (x * g)[max(0, -a):b - a]
    rel.append(f"{e['som']:14s} {e['s']:6.2f} s  {e['db']:+.0f} dB rel. voz  (evento {ev:.1f} LUFS, ganho {20 * np.log10(g):+.1f} dB)  {e['nota']}")
mix = pista + efeitos
# master (estéreo, voz no centro): ganho antes do limitador com sobreamostragem 4×, ajustado até −14,0 LUFS; nada de ganho depois
est = np.stack([mix, mix], 1)
alvo = -14.0
pre = alvo - med.integrated_loudness(est)
for _ in range(4):
    grava("_tmp/mix_pre.wav", (est * 10 ** (pre / 20)).reshape(-1), canais=2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_tmp/mix_pre.wav", "-af",
                    "aresample=192000,alimiter=limit=0.83:attack=1:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s24le",
                    "rev1/audio_master.wav"], check=True)
    m = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "rev1/audio_master.wav", "-f", "f32le", "-"], capture_output=True).stdout,
                      np.float32).reshape(-1, 2)
    l = med.integrated_loudness(m)
    if abs(l - alvo) < 0.05:
        break
    pre += alvo - l
grava("public/voz.wav", voz)
out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", "rev1/audio_master.wav", "-af", "ebur128=peak=true", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
I = float(out.rsplit("I:", 1)[1].split("LUFS")[0])
TP = float(out.rsplit("Peak:", 1)[1].split("dBFS")[0])
print(f"voz {lufs_voz:.1f} LUFS")
print("\n".join(rel))
print(f"master: {I:.1f} LUFS integrados, pico verdadeiro {TP:.1f} dBTP")
json.dump({"voz_lufs": round(lufs_voz, 2), "master_lufs": I, "master_tp": TP, "efeitos": rel}, open("rev1/audio_medido.json", "w"), ensure_ascii=False, indent=1)
