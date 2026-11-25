#!/usr/bin/env python3
"""3 opções de visual para o gancho clássico (3 s, com o som `keen` no fim). Rode de dentro da pasta do Reel.
Texto: "Depois da minha eurotrip, esse é o meu VEREDITO DA EUROPA", Anton, inteiro desde o 1º quadro,
"VEREDITO DA EUROPA" bem maior que o resto. Saída: rev1/ganchos/gancho_opcao_N.mp4."""
import os
import montar as m
from PIL import Image

PASTA = os.path.join(m.SAIDA_DIR, "ganchos")
os.makedirs(PASTA, exist_ok=True)

OPCOES = [
    ("g1", ("g1", "bruges", "IMG_2489.MOV", 0.40, 3.00, 0.45), "o Diego andando em Bruges"),
    ("g2", ("g2", "paris_v", "IMG_3171.MOV", 1.00, 3.00, 0.5), "Torre Eiffel iluminada à noite"),
    ("g3", ("g3", "italia", "IMG_5067.MOV", 1.50, 3.00, 0.5), "Fontana di Trevi, em Roma"),
]
PEQUENO = ["DEPOIS DA MINHA EUROTRIP,", "ESSE É O MEU"]
GRANDE = ["VEREDITO", "DA EUROPA"]


def texto_png(arq):
    fp = m.ajustar("\n".join(PEQUENO), m.ANTON, 100, 872)
    fg = m.ajustar("\n".join(GRANDE), m.ANTON, 300, 872)
    img = Image.new("RGBA", (m.W, m.H), (0, 0, 0, 0))
    y = 290
    for linha in PEQUENO:
        m.sombra(img, linha, (72, y), fp, m.BRANCO, "la")
        y += int(fp.size * 1.08)
    y += int(fp.size * 0.25)
    for linha in GRANDE:
        m.sombra(img, linha, (72, y), fg, m.BRANCO, "la")
        y += int(fg.size * 1.02)
    img.save(arq)
    print("tamanhos:", fp.size, fg.size, "base do bloco em y", y)


def main():
    png = os.path.join(m.TXT, "gancho_classico.png")
    texto_png(png)
    for n, (cid, spec, desc) in enumerate(OPCOES, start=1):
        base = m.cena(spec)
        saida = os.path.join(PASTA, f"gancho_opcao_{n}.mp4")
        t_keen = 3.0 - 0.96
        m.sh(["ffmpeg", "-v", "error", "-y", "-i", base, "-loop", "1", "-framerate", str(m.FPS), "-t", "3", "-i", png,
              "-i", m.KEEN,
              "-filter_complex", f"[1:v]format=rgba[t];[0:v][t]overlay=0:0:format=auto[v];"
              f"[2:a]volume=-6dB,adelay={int(t_keen*1000)}|{int(t_keen*1000)},apad=whole_dur=3,atrim=0:3[a]",
              "-map", "[v]", "-map", "[a]", "-t", "3", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida])
        print("✓", saida, "·", desc)


if __name__ == "__main__":
    main()
