"""Sequência só com as partes animadas da prévia da REV1 (pedido do Diego: "me mande as partes editadas e todas as
partes animadas para eu aprovar"). Corta da prévia inteira (rev1/previas/rev1_previa_540p.mp4) cada trecho com objeto
ou efeito, com 1 s antes e depois, e escreve no canto o minuto da prévia e o que é.

Roda de reels/bruges-yt:  python -I rev1/cortes_animados_rev1.py  →  rev1/previas/rev1_partes_animadas.mp4
"""
import os
import subprocess

PREVIA = "rev1/previas/rev1_previa_540p.mp4"
SAIDA = "rev1/previas/rev1_partes_animadas.mp4"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (início, fim, rótulo) no relógio da prévia (s); tempos de rev1/efeitos_rev1.md
CORTES = [
    (22.0, 33.5, "Recibo do trem + Placar, placa e data"),
    (49.0, 57.5, "Mapa Bruxelas - Bruges"),
    (89.5, 114.0, "Legenda 1:12-1:40 + Recibo Chez Albert"),
    (160.8, 166.5, "Etiqueta Markt"),
    (225.4, 231.0, "Instagram (1a vez)"),
    (242.4, 248.0, "Etiqueta Burg"),
    (290.0, 296.0, "Like e inscrição"),
    (307.8, 313.5, "Etiqueta Rozenhoedkaai"),
    (378.6, 399.5, "Nota horario oficial + foto da reliquia"),
    (416.3, 422.0, "Etiqueta Igreja de Nossa Senhora"),
    (451.1, 457.0, "Instagram (2a vez)"),
    (469.7, 495.5, "Legenda 7:55-fim da fala + etiqueta Fritbar"),
    (550.9, 571.0, "Recibos Fritbar e Chez Albert (2a vez)"),
    (657.3, 663.0, "Etiqueta Minnewater"),
    (677.3, 695.0, "Bilhete do novo waffle + Recibo House of Waffles"),
    (716.8, 734.5, "Time-lapse + legenda 'O outro, por muito!'"),
    (781.8, 789.0, "Recibo do bar"),
    (814.4, 841.0, "Recibos Chez Albert (3a vez) e Gofre"),
]


def mmss(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def main():
    os.makedirs("_tmp/cortes", exist_ok=True)
    lista = []
    for i, (a, b, rot) in enumerate(CORTES):
        out = f"_tmp/cortes/c{i:02d}.mp4"
        txt = f"prévia {mmss(a + 1)} · {rot}".replace(":", "\\:").replace("'", "")
        vf = f"drawtext=fontfile={FONTE}:text='{txt}':x=16:y=h-40:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=8"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", PREVIA, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "26", "-r", "24", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", out], check=True)
        lista.append(out)
    with open("_tmp/cortes/lista.txt", "w") as f:
        for x in lista:
            f.write(f"file '{os.path.basename(x)}'\n")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/cortes/lista.txt", "-c", "copy", "-movflags", "+faststart", SAIDA], check=True)
    dur = sum(b - a for a, b, _ in CORTES)
    print("ok", SAIDA, f"{dur:.0f} s", os.path.getsize(SAIDA) // 1024, "KB")


if __name__ == "__main__":
    main()
