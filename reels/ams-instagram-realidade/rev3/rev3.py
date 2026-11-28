"""Amsterdam · Instagram x Realidade · REV3 = REV2 sem o keen (pedido do Diego, 28/11/2026).
Roda de reels/ams-instagram-realidade:  python3 rev3/rev3.py
Lê o vídeo da REV2 (imagem copiada sem recodificar) e _tmp/ig_ref.wav (áudio do trend, só para a prévia).
Saídas: rev3/ams_instagram_realidade_rev3.mp4 (para postar: sem áudio; o áudio do trend entra no app)
        rev3/ams_instagram_realidade_rev3_previa_com_audio.mp4 (conferência com o áudio do trend)."""
import subprocess
src = "rev2/ams_instagram_realidade_rev2.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:v", "-c:v", "copy", "-an", "-movflags", "+faststart",
                "rev3/ams_instagram_realidade_rev3.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", "_tmp/ig_ref.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest",
                "-movflags", "+faststart", "rev3/ams_instagram_realidade_rev3_previa_com_audio.mp4"], check=True)
print("ok")
