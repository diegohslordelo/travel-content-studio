"""teste_voz_v2.mp4 (rev. 6 tratada) e teste_voz_v2_original.mp4 (sem tratamento onde existe original):
só a apresentação com a narração e as cenas com fala, na imagem do Reel, 540x960, com rótulo em cada trecho.

Na versão "original":
- narração: narracao.m4a sem tratamento nenhum, só com o mesmo nível de loudness da tratada, sobre o som das cenas da rev. 5;
- "Chegamos!": som cru do bruto (Reel da rev. 3), mesmo nível de voz;
- "Buenos días", Bruges e "tapa": como na rev. 5, porque não há versão crua completa desses trechos.
Os dois arquivos passam pelo mesmo ganho final e pelo mesmo limitador, para comparar timbre e não volume.
"""
import json
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

from restaurar import alinhar

SR = 48000
A = "../a"
OUT = "out"
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VIDEO = os.path.join(PROJ, "reel_apresentacao_sem_texto.mp4")
FONTE = os.path.join(PROJ, "fontes", "Montserrat-SemiBold.ttf")
LAT = 143
rel = json.load(open(os.path.join(A, "v6_relatorio.json")))
meter = pyln.Meter(SR)


def ff(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


# ---------- áudio "original" na linha do tempo do Reel
mix5, _ = sf.read(os.path.join(A, "rev5.wav"), always_2d=True)
v5, _ = sf.read(os.path.join(A, "nar_rev5_no_reel.wav"), always_2d=True)
v6, _ = sf.read(os.path.join(A, "nar_v6_no_reel.wav"), always_2d=True)
bruta, _ = sf.read(os.path.join(A, "nar_bruta.wav"), always_2d=True)
orig = mix5 - v5
# narração crua no mesmo lugar e com a mesma loudness da tratada
t0 = int(3.0 * SR) + LAT
nb = bruta.copy()
f_in, f_out = int(0.03 * SR), int(0.1 * SR)
nb[:f_in] *= np.linspace(0, 1, f_in)[:, None]
nb[-f_out:] *= np.linspace(1, 0, f_out)[:, None]
voz_ini, voz_fim = int(3.37 * SR), int(14.75 * SR)
alvo = meter.integrated_loudness(v6[voz_ini:voz_fim])
cru_reel = np.zeros_like(orig)
cru_reel[t0:t0 + len(nb)] = nb
cru_reel *= 10 ** ((alvo - meter.integrated_loudness(cru_reel[voz_ini:voz_fim])) / 20)
orig += cru_reel
# "Chegamos!" cru (mesmo recorte e nível da rev. 6, sem o passa-altas e sem o +6 dB no ambiente)
r3, _ = sf.read(os.path.join(A, "rev3.wav"), always_2d=True)
d = LAT / SR
i5 = alinhar(r3, 17.0, 19.55, orig, 19.70, 0.3)
desloc = i5 - int(17.0 * SR)
XF = int(0.03 * SR)
ia, ib = int((19.725 + d) * SR), int((22.233 + d) * SR)
cru = r3[ia - desloc - XF:ib - desloc + XF] * 10 ** (rel["cena8"]["ganho_nivel_dB"] / 20)
w = np.ones(len(cru))
w[:XF] = np.sin(np.linspace(0, np.pi / 2, XF)) ** 2
w[-XF:] = np.cos(np.linspace(0, np.pi / 2, XF)) ** 2
orig[ia - XF:ib + XF] = orig[ia - XF:ib + XF] * (1 - w[:, None]) + cru * w[:, None]
sf.write(os.path.join(A, "original_pre.wav"), orig.astype(np.float32), SR, subtype="FLOAT")
fin = rel["final"]
ff("-i", os.path.join(A, "original_pre.wav"), "-af",
   f"volume={fin['ganho_dB']:.2f}dB,alimiter=limit={fin['limite']:.3f}:attack=5:release=80:level=disabled:latency=1",
   "-c:a", "pcm_s24le", os.path.join(A, "original_final.wav"))

# ---------- vídeos
TRECHOS = [
    (3.000, 14.917, "Narração|(com o som das cenas por baixo)", "narração sem tratamento", "narração tratada · rev. 6"),
    (14.917, 19.625, "Buenos días, Barcelona!|Chegamos ao nosso primeiro destino.", "rev. 5 (não há versão crua completa)", "rev. 6 · agudos devolvidos"),
    (19.625, 22.333, "Chegamos!", "som cru do bruto", "rev. 6 · som cru + passa-altas 80 Hz"),
    (27.417, 30.417, "Muito, muito, muito, muito.", "rev. 5 (não há versão crua)", "rev. 6 · agudos devolvidos"),
    (30.417, 34.958, "E agora eu acabei de pedir|minha primeira tapa de Barcelona.", "rev. 5 (não há versão crua completa)", "rev. 6 · agudos devolvidos, canais alinhados"),
]


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,")


def montar(audio, idx, nome, tmp):
    partes = []
    for k, (a, z, texto, rot_o, rot_t) in enumerate(TRECHOS):
        rot = (rot_o, rot_t)[idx]
        parte = os.path.join(tmp, f"{nome}_{k}.mp4")
        linhas = texto.split("|")
        vf = f"scale=540:960,setsar=1,drawbox=x=0:y=40:w=iw:h={40 + 26 * len(linhas)}:color=black@0.6:t=fill"
        for j, l in enumerate(linhas):
            vf += f",drawtext=fontfile={FONTE}:text='{esc(l)}':fontcolor=white:fontsize=17:x=14:y={50 + 26 * j}"
        vf += f",drawtext=fontfile={FONTE}:text='{esc(rot.upper())}':fontcolor=0xE8B24A:fontsize=15:x=14:y={54 + 26 * len(linhas)}"
        ff("-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", VIDEO, "-ss", f"{a:.3f}", "-t", f"{z - a:.3f}", "-i", audio,
           "-filter_complex", f"[0:v]{vf},tpad=stop_mode=clone:stop_duration=0.4[v];[1:a]apad=pad_dur=0.4[a]",
           "-map", "[v]", "-map", "[a]", "-t", f"{z - a + 0.4:.3f}", "-r", "24",
           "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", SR, parte)
        partes.append(parte)
    lista = os.path.join(tmp, f"{nome}.txt")
    open(lista, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in partes))
    saida = os.path.join(OUT, f"{nome}.mp4")
    ff("-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-movflags", "+faststart", saida)
    return saida


tmp = os.path.join(A, "tv2")
os.makedirs(tmp, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
for audio, idx, nome in [(os.path.join(A, "original_final.wav"), 0, "teste_voz_v2_original"),
                         (os.path.join(A, "v6_final.wav"), 1, "teste_voz_v2")]:
    s = montar(audio, idx, nome, tmp)
    print(s, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "csv=p=0", s],
                            capture_output=True, text=True).stdout.strip())
