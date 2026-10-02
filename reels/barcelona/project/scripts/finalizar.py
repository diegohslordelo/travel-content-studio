"""Encode final do Reel: vídeo do Remotion + mix de áudio -> exports/.

Rodar de dentro de reels/barcelona/ depois de `npm run render` (em project/) e de montar_audio.py:
    python3 project/scripts/finalizar.py

H.264 High, 1080 × 1920, 30 fps, 14 Mb/s (máx. 16 Mb/s), yuv420p Rec.709; AAC-LC 48 kHz estéreo 256 kb/s.
"""
import subprocess

VIDEO = "project/out/video_sem_audio.mp4"
AUDIO = "project/out/audio_mix.wav"
SAIDA = "exports/2026-10-02_reel_3-coisas-barcelona.mp4"

subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", VIDEO, "-i", AUDIO, "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-b:v", "14M", "-maxrate", "16M", "-bufsize", "16M",
    "-r", "30", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-color_range", "tv", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
    "-shortest", "-movflags", "+faststart", SAIDA], check=True)
print(SAIDA)
