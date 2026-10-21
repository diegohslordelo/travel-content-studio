"""Junta a imagem renderizada pelo Remotion com a mixagem final (voz + música + efeitos) e mede o arquivo exportado.

  python rev1/finalizar_rev1.py <video_remotion.mp4> <inicio_ms> <saida.mp4>

<inicio_ms> = onde o trecho renderizado começa no vídeo final. O áudio do render (só efeitos sonoros) entra na
mixagem (`mixar_rev1.py --cache`), a imagem é copiada sem recodificar, o áudio sai em AAC 192 kbps 48 kHz e o
loudness/pico verdadeiro são medidos no arquivo exportado (padrão de áudio, seção 11.3).
"""
import json
import re
import subprocess
import sys


def roda(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def main():
    video, inicio, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    dur = float(roda(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]).stdout)
    sfx = "_tmp/sfx_trecho.wav"
    roda(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", video, "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_f32le", sfx])
    mix = "_tmp/mix_trecho.wav"
    roda([sys.executable, "rev1/mixar_rev1.py", "--cache", "--sfx", sfx, "--sfx-inicio", str(inicio), "--de", str(inicio), "--ate", str(inicio + dur * 1000), "--saida", mix])
    roda(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", video, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", saida])
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", saida, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    info = {"arquivo": saida, "inicio_ms": inicio, "duracao_s": round(dur, 3), "lufs_integrado": float(i), "pico_verdadeiro_dbtp": float(tp)}
    print(json.dumps(info, ensure_ascii=False))
    json.dump(info, open(saida + ".medida.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
