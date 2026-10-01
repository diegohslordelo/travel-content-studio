"""Revisão 6, arquivos finais: reel_apresentacao_rev6.mp4 (com texto), reel_apresentacao_sem_texto_rev6.mp4 e
reel_apresentacao_previa_leve_rev6.mp4. Não sobrescreve os arquivos da rev. 5.

Base sem texto: montar_video_rev6.py. Texto: render.py lista_de_cortes_rev6.json texto. Áudio: montar_audio_rev6.py.
A base já tem o fade de saída da rev. 5 nos últimos 0,5 s; o texto recebe o mesmo fade só no canal alfa.

Uso: python3 final_rev6.py base_rev6.mkv pasta_texto audio_final.wav
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
video, texto, audio = sys.argv[1:4]
QUADROS = 989
total = QUADROS / R.FPS
fade = 0.5
comum = ["-c:v", "libx264", "-crf", "16", "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
         "-pix_fmt", "yuv420p", "-r", R.FPS, *R.TAGS_COR,
         "-c:a", "aac", "-b:a", "192k", "-ar", R.SR, "-ac", "2", "-movflags", "+faststart"]
sem = os.path.join(BASE, "reel_apresentacao_sem_texto_rev6.mp4")
com = os.path.join(BASE, "reel_apresentacao_rev6.mp4")
leve = os.path.join(BASE, "reel_apresentacao_previa_leve_rev6.mp4")
R.rodar(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-filter_complex",
         f"[0:v]setpts=N/({R.FPS}*TB),format=yuv420p[v]", "-map", "[v]", "-map", "1:a", "-frames:v", QUADROS,
         "-shortest", *comum, sem])
filtro = (f"[0:v]setpts=N/({R.FPS}*TB),format=yuv444p[b];"
          f"[1:v]format=rgba,fade=t=out:st={total - fade:.3f}:d={fade}:alpha=1,"
          f"scale=out_color_matrix=bt709:out_range=tv,format=yuva444p[t];"
          f"[b][t]overlay=0:0:format=yuv444:eof_action=pass,format=yuv420p[v]")
R.rodar(["ffmpeg", "-v", "error", "-y", "-i", video, "-framerate", R.FPS, "-i", os.path.join(texto, "t_%05d.png"),
         "-i", audio, "-filter_complex", filtro, "-map", "[v]", "-map", "2:a", "-frames:v", QUADROS, *comum, com])
# prévia: imagem do arquivo com texto e áudio direto do WAV (evita a segunda geração de AAC, que subia o pico)
R.rodar(["ffmpeg", "-v", "error", "-y", "-i", com, "-i", audio, "-map", "0:v", "-map", "1:a", "-vf",
         "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "23", "-maxrate", "2500k", "-bufsize", "5000k",
         "-preset", "slow", "-profile:v", "high", "-level:v", "3.1", "-pix_fmt", "yuv420p", *R.TAGS_COR,
         "-c:a", "aac", "-b:a", "128k", "-ar", R.SR, "-shortest", "-movflags", "+faststart", leve])
for arq in (com, sem, leve):
    print(arq)
