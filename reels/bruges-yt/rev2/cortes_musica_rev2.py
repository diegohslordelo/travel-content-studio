"""Sequência só com os trechos de música da prévia da REV2 (pedido do Diego, 20/11/2026: "me manda para eu aprovar um corte
dos momentos para eu ver os vídeos e aprovar com a música"). Corta da prévia inteira (rev2/previas/rev2_previa_540p.mp4)
cada janela de música (rev2/musica_rev2.json), com 0,8 s antes e depois, e escreve no canto a seção, a faixa e o minuto.

Roda de reels/bruges-yt:  python -I rev2/cortes_musica_rev2.py  →  rev2/previas/rev2_musica_secoes.mp4
"""
import json
import os
import subprocess

PREVIA = "rev2/previas/rev2_previa_540p.mp4"
SAIDA = "rev2/previas/rev2_musica_secoes.mp4"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NOMES = {"G": "Abertura", "M1": "Chegada", "M2": "Markt, Burg e canais", "M3": "Fome e batata", "M4": "Minnewater", "M5": "Waffles e despedida", "F": "Fechamento"}


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def limpa(t):
    return t.replace("\\", "").replace(":", "\\:").replace("'", "").replace("%", "")


def main():
    r = json.load(open("rev2/musica_rev2.json", encoding="utf-8"))
    os.makedirs("_tmp/cortes_mus", exist_ok=True)
    lista = []
    for i, j in enumerate(r["janelas"]):
        a, b = j["video_s"]
        a, b = max(0.0, a - 0.8), b + 0.8
        rot = limpa(f"{j['id']} · {NOMES[j['id']]} · {j['faixa']} · prévia {mmss(a + 0.8)}")
        out = f"_tmp/cortes_mus/c{i:02d}.mp4"
        vf = f"drawtext=fontfile={FONTE}:text='{rot}':x=16:y=h-40:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", PREVIA, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "27", "-r", "24", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", out], check=True)
        lista.append(out)
    with open("_tmp/cortes_mus/lista.txt", "w") as f:
        for x in lista:
            f.write(f"file '{os.path.basename(x)}'\n")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/cortes_mus/lista.txt", "-c", "copy", "-movflags", "+faststart", SAIDA], check=True)
    print("ok", SAIDA, os.path.getsize(SAIDA) // 1024, "KB")


if __name__ == "__main__":
    main()
