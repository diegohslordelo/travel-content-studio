"""REV4: monta a fonte única da voz e do vídeo do Diego.
O Diego regravou as falas 2 e 3 num take novo (Drive Disney/Reel/Frozen, E934789A…, 15/11/2026, 1440 × 2560, HLG),
corrigindo a informação: o show no mesmo horário do castelo é o Disney Cascade of Lights, não um show do Frozen.
Fonte da REV4 = gravação original 0–3,9667 s (tomada 1, o gancho) + take novo inteiro + gravação original de 14,7333 s
ao fim (tomadas 3 a 7). As tomadas 2 da gravação original (falas 2 e 3 antigas) saem inteiras.
Saídas em ../fonte/ (fora do git):
  diego_rev4_sdr.mkv            vídeo já convertido HDR → SDR (a MESMA conversão do recorte), 1080 × 1920, 30 qps, áudio PCM
  recorte/diego_rev4_alfa.webm  o recorte por IA nos mesmos quadros (original + take novo + original)
Roda de dentro de reels/disney-frozen/rev4:  python3 scripts/montar_fonte.py  (depois de scripts/recorte.py no take novo)"""
import os
import subprocess

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
ORIG, NOVO = os.path.join(F, "diego_frozen.mp4"), os.path.join(F, "diego_take_novo.mp4")
A_ORIG, A_NOVO = os.path.join(F, "recorte", "diego_alfa.webm"), os.path.join(F, "recorte", "take_novo_alfa.webm")
FPS = 30
Q1, Q3 = 119, 442  # quadros da gravação original: fim da tomada 1 (3,9667 s) e início da tomada 3 (14,7333 s)
TONEMAP = ("scale=1080:1920:flags=lanczos,zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def sh(cmd):
    print(" ".join(cmd)[:200])
    subprocess.run(cmd, check=True)


# vídeo SDR + áudio (cortes por quadro e por amostra, sem mudar velocidade)
fc = (f"[0:v]{TONEMAP},trim=end_frame={Q1},setpts=PTS-STARTPTS[v0];"
      f"[1:v]{TONEMAP},setpts=PTS-STARTPTS[v1];"
      f"[0:v]{TONEMAP},trim=start_frame={Q3},setpts=PTS-STARTPTS[v2];"
      f"[0:a]aresample=48000,atrim=end={Q1 / FPS},asetpts=PTS-STARTPTS[a0];"
      f"[1:a]aresample=48000,asetpts=PTS-STARTPTS[a1];"
      f"[0:a]aresample=48000,atrim=start={Q3 / FPS},asetpts=PTS-STARTPTS[a2];"
      "[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]")
sh(["ffmpeg", "-v", "error", "-y", "-i", ORIG, "-i", NOVO, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", str(FPS),
    "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-colorspace", "bt709", "-c:a", "pcm_s16le", "-ac", "1", os.path.join(F, "diego_rev4_sdr.mkv")])

# recorte com alfa nos mesmos quadros
fa = (f"[0:v]trim=end_frame={Q1},setpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[a1];"
      f"[0:v]trim=start_frame={Q3},setpts=PTS-STARTPTS[a2];[a0][a1][a2]concat=n=3:v=1:a=0,format=yuva420p[v]")
sh(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", A_ORIG, "-c:v", "libvpx-vp9", "-i", A_NOVO, "-filter_complex", fa,
    "-map", "[v]", "-r", str(FPS), "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-row-mt", "1",
    "-deadline", "good", "-cpu-used", "4", "-auto-alt-ref", "0", os.path.join(F, "recorte", "diego_rev4_alfa.webm")])
print("ok")
