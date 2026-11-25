#!/usr/bin/env python3
"""Reel "Veredito das cidades da Europa" · REV1. Rode de dentro desta pasta:

    python3 baixar.py          # brutos do Drive para fonte/ (fora do git)
    node cta.mjs               # placas do CTA (DS V2, Remotion) em _tmp/cta/
    python3 montar.py          # cenas, texto, CTA, som e master em rev1/

Decisões do Diego (ROTEIRO.md): sem fala, sem música (ele coloca no app), edição de corte seco, imagens sem
tratamento (só HDR→SDR e enquadramento), sem sombreado na base. DS V2 só no CTA. Som `keen` no fim do gancho.
Só usa a biblioteca padrão, Pillow, ffmpeg.
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "fonte")
TMP = os.path.join(AQUI, "_tmp")
SEG = os.path.join(TMP, "seg")
TXT = os.path.join(TMP, "txt")
SAIDA_DIR = os.path.join(AQUI, "rev1")
SAIDA = os.path.join(SAIDA_DIR, "reel_veredito-cidades_rev1.mp4")
for d in (SEG, TXT, SAIDA_DIR):
    os.makedirs(d, exist_ok=True)

W, H, FPS = 1080, 1920, 30
AMBAR = (224, 174, 92)  # #E0AE5C, destaque do formato (docs/FORMATOS_REELS.md, 5.4 e 6)
BRANCO = (255, 255, 255)
ANTON = os.path.join(TMP, "fontes", "Anton-Regular.ttf")    # só no gancho (decisão do Diego, 25/11/2026)
BARLOW_800 = os.path.join(TMP, "fontes", "Barlow-800.ttf")   # categoria (branca) e cidade (mostarda)
BARLOW_700 = os.path.join(TMP, "fontes", "Barlow-700.ttf")   # frase do veredito (branca)
KEEN = os.path.join(AQUI, "..", "..", "design-system", "sons", "externos", "keen.wav")
CLACK = os.path.join(AQUI, "..", "..", "design-system", "sons", "PD_clack_v1.wav")

# HLG (iPhone, BT.2020) → SDR BT.709, sem ajuste criativo (mesma conversão de reels/madrid-show).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
)

# cenas: (id, pasta, arquivo, início no bruto, duração, foco horizontal do recorte 9:16 em planos horizontais)
# Preferência por takes verticais: entram inteiros, sem recorte (decisão do Diego, 25/11/2026: "igual ao original").
# Gancho: o Diego andando em terceira pessoa. Cartões: paisagem + Diego em terceira pessoa, mostrando o porquê.
HOOK = ("gancho", "amsterdam_v", "IMG_1984-1.MOV", 4.50, 3.00, 0.5)
CARTOES = [
    {
        "id": "c1", "categoria": "MAIS BARATA", "cidade": "LISBOA",
        "cenas": [("c1a", "lisboa_v", "IMG_4416.MOV", 0.5, 2.60, 0.5), ("c1b", "lisboa_v", "IMG_4470.MOV", 0.5, 2.40, 0.5)],
        "grupos": [("Barata, e todo mundo\nte entende.", 0.4, 5.0)],
    },
    {
        "id": "c2", "categoria": "MELHOR COMIDA", "cidade": "ROMA",
        "cenas": [("c2a", "italia", "IMG_5260.MOV", 1.0, 5.00, 0.5)],
        "grupos": [("Foge do Coliseu e\ncome muito bem.", 0.4, 5.0)],
    },
    {
        "id": "c3", "categoria": "MAIS ARMADILHA DE TURISTA", "cidade": "VENEZA",
        "cenas": [("c3a", "italia", "IMG_6016.MOV", 4.0, 2.50, 0.5), ("c3b", "italia", "IMG_6062.MOV", 5.5, 2.50, 0.5)],
        "grupos": [("Linda,", 0.3, 2.5), ("mas o cartão-postal\né caro.", 2.5, 5.0)],
    },
    {
        "id": "c4", "categoria": "MAIS SUPERESTIMADA", "cidade": "BRUXELAS",
        "cenas": [("c4a", "bruxelas", "IMG_2217.MOV", 0.5, 2.60, 0.5), ("c4b", "bruxelas", "IMG_2251.MOV", 0.4, 2.40, 0.5)],
        "grupos": [("Grand-Place linda.", 0.3, 2.6), ("Manneken Pis?\nPequeno demais.", 2.6, 5.0)],
    },
    {
        "id": "c5", "categoria": "NÃO VOLTARIA", "cidade": "AMSTERDAM",
        "cenas": [("c5a", "amsterdam_v", "IMG_1403-1.MOV", 0.0, 2.60, 0.5), ("c5b", "amsterdam_v", "IMG_1459-1.MOV", 1.0, 2.40, 0.5)],
        "grupos": [("Já vi de tudo.", 0.3, 2.6), ("E é caro pra voltar\ntão cedo.", 2.6, 5.0)],
    },
    {
        "id": "c6", "categoria": "VOLTARIA AMANHÃ", "cidade": "BARCELONA",
        "cenas": [("c6a", "barcelona2", "IMG_0986-1.MOV", 1.0, 1.80, 0.5), ("c6b", "barcelona", "IMG_0941.MOV", 0.2, 1.60, 0.5),
                  ("c6c", "barcelona2", "IMG_1029-1.MOV", 2.0, 1.60, 0.5)],
        "grupos": [("Praia, comida e cidade\ngrande no mesmo dia.", 0.4, 5.0)],
    },
]
CTA_CENA = ("cta", "barcelona2", "IMG_0986-1.MOV", 6.0, 4.70, 0.5)
CTA_PLACAS = [("placa_cta.mov", 0.0), ("placa_perfil.mov", 2.40)]  # (arquivo, início no CTA, s)


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(" ".join(cmd)[:400])
        print(r.stderr[-3000:])
        sys.exit("falhou: " + cmd[0])
    return r


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", arq])
    s = json.loads(r.stdout)["streams"][0]
    rot = 0
    for sd in s.get("side_data_list", []):
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = s["width"], s["height"]
    if abs(rot) == 90:
        w, h = h, w
    return w, h, s.get("color_transfer", "")


def cena(c):
    """Corta o trecho e leva a 1080 × 1920 sem mexer na imagem: take vertical entra inteiro (só escala);
    horizontal (só quando não há vertical do lugar) leva recorte 9:16. HDR→SDR só se o arquivo for HLG."""
    cid, pasta, arq, ini, dur, foco = c
    saida = os.path.join(SEG, f"{cid}.mp4")
    if os.path.exists(saida):
        return saida
    bruto = os.path.join(FONTE, pasta, arq)
    w, h, trc = sonda(bruto)
    if w > h:  # horizontal: recorte 9:16 centrado no foco
        enq = f"crop=w=ih*9/16:h=ih:x=(iw-ih*9/16)*{foco}:y=0,scale={W}:{H}:flags=lanczos"
    else:
        enq = f"scale={W}:{H}:flags=lanczos"
    cor = TONEMAP + "," if trc == "arib-std-b67" else ""
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini}", "-t", f"{dur}", "-i", bruto, "-an",
        "-vf", f"{cor}{enq},fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "14",
        "-preset", "medium", "-movflags", "+faststart", saida])
    return saida


def sombra(img, texto, xy, fonte, cor, ancora):
    """Texto com a sombra do formato (docs/FORMATOS_REELS.md, 6): 0 3px 0 .35 + 0 4px 22px .85. Sem degradê na tela."""
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    sx, sy = xy
    s1 = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(s1).multiline_text((sx, sy + 4), texto, font=fonte, fill=(0, 0, 0, 255), anchor=ancora, align="center", spacing=int(fonte.size * 0.1))
    s1 = s1.filter(ImageFilter.GaussianBlur(11))
    a = s1.getchannel("A").point(lambda v: min(255, int(v * 1.6)))
    s1.putalpha(a)
    s2 = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(s2).multiline_text((sx, sy + 3), texto, font=fonte, fill=(0, 0, 0, 255), anchor=ancora, align="center", spacing=int(fonte.size * 0.1))
    s2.putalpha(s2.getchannel("A").point(lambda v: int(v * 0.35)))
    img.alpha_composite(s1)
    img.alpha_composite(s2)
    d = ImageDraw.Draw(img)
    d.multiline_text(xy, texto, font=fonte, fill=cor, anchor=ancora, align="center", spacing=int(fonte.size * 0.1))


def ajustar(texto, caminho, maximo, largura):
    tam = maximo
    while tam > 20:
        f = ImageFont.truetype(caminho, tam)
        if max(f.getlength(l) for l in texto.split("\n")) <= largura:
            return f
        tam -= 2
    return ImageFont.truetype(caminho, 20)


def png_rotulo(cartao):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f_cat = ajustar(cartao["categoria"], BARLOW_800, 68, 872)
    sombra(img, cartao["categoria"], (72, 256), f_cat, BRANCO, "la")
    f_cid = ajustar(cartao["cidade"], BARLOW_800, 190, 872)
    sombra(img, cartao["cidade"], (72, 256 + int(f_cat.size * 1.15)), f_cid, AMBAR, "la")
    arq = os.path.join(TXT, f"{cartao['id']}_rotulo.png")
    img.save(arq)
    return arq


def png_grupo(cid, i, texto):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = ImageFont.truetype(BARLOW_700, 66)
    sombra(img, texto, (540, 1320), f, BRANCO, "mm")
    arq = os.path.join(TXT, f"{cid}_g{i}.png")
    img.save(arq)
    return arq


def concat(arquivos, saida):
    lista = saida + ".txt"
    with open(lista, "w") as f:
        for a in arquivos:
            f.write(f"file '{a}'\n")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", saida])
    return saida


def cartao_video(c):
    saida = os.path.join(SEG, f"{c['id']}_texto.mp4")
    base = concat([cena(x) for x in c["cenas"]], os.path.join(SEG, f"{c['id']}_base.mp4"))
    dur = sum(x[4] for x in c["cenas"])
    pngs = [(png_rotulo(c), 0.0, dur)] + [(png_grupo(c["id"], i, t), a, b) for i, (t, a, b) in enumerate(c["grupos"])]
    entradas = ["-i", base]
    fg = []
    for i, (p, a, b) in enumerate(pngs, start=1):
        entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur}", "-i", p]
        # entrada de 120 ms (opacidade 0 → 1); saída curta no fim do grupo (docs/FORMATOS_REELS.md, 6)
        fg.append(f"[{i}:v]format=rgba,fade=t=in:st={a}:d=0.12:alpha=1,fade=t=out:st={max(a, b - 0.10)}:d=0.10:alpha=1[t{i}]")
    cadeia = "[0:v]"
    for i in range(1, len(pngs) + 1):
        saida_no = f"[v{i}]"
        fg.append(f"{cadeia}[t{i}]overlay=0:0:format=auto{saida_no}")
        cadeia = saida_no
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fg), "-map", cadeia, "-an",
        "-t", f"{dur}", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", saida])
    return saida


def gancho_video():
    saida = os.path.join(SEG, "gancho_texto.mp4")
    base = cena(HOOK)
    linhas = [("MINHA OPINIÃO", BRANCO, 0.10), ("IMPOPULAR", BRANCO, 0.90), ("SOBRE A EUROPA", BRANCO, 1.70)]
    f = ajustar("\n".join(l[0] for l in linhas), ANTON, 230, 872)
    entradas = ["-i", base]
    fg = []
    y = 300
    for i, (t, cor, ini) in enumerate(linhas, start=1):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sombra(img, t, (72, y), f, cor, "la")
        arq = os.path.join(TXT, f"gancho_l{i}.png")
        img.save(arq)
        entradas += ["-loop", "1", "-framerate", str(FPS), "-t", "3", "-i", arq]
        fg.append(f"[{i}:v]format=rgba,fade=t=in:st={ini}:d=0.12:alpha=1[t{i}]")
        y += int(f.size * 1.05)
    cadeia = "[0:v]"
    for i in range(1, len(linhas) + 1):
        fg.append(f"{cadeia}[t{i}]overlay=0:0:format=auto[v{i}]")
        cadeia = f"[v{i}]"
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fg), "-map", cadeia, "-an", "-t", "3",
        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", saida])
    return saida


def cta_video():
    saida = os.path.join(SEG, "cta_ds.mp4")
    base = cena(CTA_CENA)
    entradas = ["-i", base]
    fg = []
    for i, (arq, ini) in enumerate(CTA_PLACAS, start=1):
        entradas += ["-i", os.path.join(TMP, "cta", arq)]
        fg.append(f"[{i}:v]format=rgba,setpts=PTS+{ini}/TB[p{i}]")
    cadeia = "[0:v]"
    for i in range(1, len(CTA_PLACAS) + 1):
        fg.append(f"{cadeia}[p{i}]overlay=0:0:format=auto:eof_action=pass[v{i}]")
        cadeia = f"[v{i}]"
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fg), "-map", cadeia, "-an",
        "-t", f"{CTA_CENA[4]}", "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", saida])
    return saida


def montar():
    pecas = [gancho_video()] + [cartao_video(c) for c in CARTOES] + [cta_video()]
    video = concat(pecas, os.path.join(TMP, "video_sem_som.mp4"))
    total = 3.0 + sum(sum(x[4] for x in c["cenas"]) for c in CARTOES) + CTA_CENA[4]
    # Som: `keen` com o pico (0,96 s do arquivo) no corte gancho → 1º cartão (t = 3,0 s), −6 dB; `clack` da placa em −10 dB
    # (DS V2, 4.6: no quadro 8 da Chegada). Sem voz e sem música: valores relativos ao pico do `keen` original.
    t_keen = 3.0 - 0.96
    t_cta = 3.0 + sum(sum(x[4] for x in c["cenas"]) for c in CARTOES)
    clacks = [t_cta + ini + 8 / 30 for _, ini in CTA_PLACAS]
    entradas = ["-i", video, "-i", KEEN, "-i", CLACK]
    fg = [f"[1:a]volume=-6dB,adelay={int(t_keen*1000)}|{int(t_keen*1000)}[k]"]
    nomes = ["[k]"]
    for i, t in enumerate(clacks):
        fg.append(f"[2:a]volume=-10dB,adelay={int(t*1000)}|{int(t*1000)}[c{i}]")
        nomes.append(f"[c{i}]")
    fg.append(f"{''.join(nomes)}amix=inputs={len(nomes)}:normalize=0,aresample=48000,apad=whole_dur={total},atrim=0:{total}[a]")
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fg), "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", SAIDA])
    print("✓", SAIDA, f"{total:.2f} s")


if __name__ == "__main__":
    montar()
