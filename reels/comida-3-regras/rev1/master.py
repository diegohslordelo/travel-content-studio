"""REV1 · master de áudio (DS V2 4.6: −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP). Vídeo copiado sem recodificar.

Uso (de dentro de rev1): python3 master.py render_sem_master.mp4 comida_3_formas_rev1.mp4
Ganho linear até −14 LUFS e limitador com sobreamostragem 4× (192 kHz), como na REV4 de Veneza.
"""
import subprocess
import sys

ent, sai = sys.argv[1], sys.argv[2]


def medir(arq):
    r = subprocess.run(f"ffmpeg -hide_banner -nostats -i {arq} -af ebur128=peak=true -f null -", shell=True,
                       capture_output=True, text=True).stderr.rsplit("Summary:", 1)[1]
    return float(r.split("I:")[1].split("LUFS")[0]), float(r.split("Peak:")[1].split("dBFS")[0])


I0, P0 = medir(ent)
for tentativa in range(4):
    g = -14.0 - I0 + 0.1 * tentativa
    af = f"volume={g:.2f}dB,aresample=192000,alimiter=limit=0.79:level=false:attack=1:release=60,aresample=48000"
    subprocess.run(f'ffmpeg -v error -y -i {ent} -c:v copy -af "{af}" -c:a aac -b:a 320k -ar 48000 {sai}', shell=True, check=True)
    I, P = medir(sai)
    print(f"ganho {g:+.2f} dB → {I:.1f} LUFS, pico verdadeiro {P:.1f} dBTP (antes {I0:.1f} LUFS, {P0:.1f} dBTP)")
    if I >= -14.05:
        break
