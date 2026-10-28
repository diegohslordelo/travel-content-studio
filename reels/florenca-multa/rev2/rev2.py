#!/usr/bin/env python3
"""Reel "A multa que salvou o trem" · REV2: mesmo corte da REV1 com o ritmo acelerado de modo uniforme (pedido do Diego, 28/10/2026).

O Diego achou 1,1x acelerado demais e pediu entre 1,0x e 1,1x, com o vídeo final entre 56 e 58 s. A velocidade vale para tudo
ao mesmo tempo (imagem, voz e efeitos), então cortes, legendas e impactos continuam presos às palavras; a voz usa atempo
(mantém o tom). A música não está no arquivo: o Diego a coloca na plataforma.

Rode de dentro desta pasta:   python3 rev2.py ritmo | master | previa | tudo
Entrada: ../rev1/_tmp/com_rostos_sem_master.mov (render da REV1, 24 fps, voz a −16 LUFS, sem música).
"""
import json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REV1 = os.path.normpath(os.path.join(AQUI, "..", "rev1"))
ENTRADA = os.path.join(REV1, "_tmp", "com_rostos_sem_master.mov")
TMP = os.path.join(AQUI, "_tmp")
VEL = 1.07  # 61,04 s ÷ 1,07 = 57,05 s (alvo 56–58 s)
SAIDA = os.path.join(AQUI, "reel_florenca-multa_rev2.mp4")


def sh(cmd, cap=False):
    r = subprocess.run(cmd, capture_output=cap, text=True)
    if r.returncode:
        print(r.stderr[-2000:] if cap else "")
        sys.exit("falhou: " + cmd[0])
    return r


def ritmo():
    os.makedirs(TMP, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", ENTRADA, "-filter_complex",
        f"[0:v]setpts=PTS/{VEL},fps=24[v];[0:a]atempo={VEL}[a]", "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le",
        os.path.join(TMP, "ritmo.mov")])


def master():
    ent = os.path.join(TMP, "ritmo.mov")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", ent, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", SAIDA])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", SAIDA, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    print("loudness:", re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1], "LUFS · pico", re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])


def previa():
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-c:a", "aac", "-b:a", "128k",
        os.path.join(AQUI, "reel_florenca-multa_rev2_previa.mp4")])


def tudo():
    ritmo(); master(); previa()


if __name__ == "__main__":
    globals()[sys.argv[1]]()
