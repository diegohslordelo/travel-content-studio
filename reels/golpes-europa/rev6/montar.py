#!/usr/bin/env python3
"""Fundo de tela verde · "3 golpes na Europa" · REV6 (dado da UE + vídeo novo no dado).

Roda de dentro de reels/golpes-europa/:  python3 rev6/montar.py
Gera rev6/golpes_fundo_rev6.mp4 (1080x1920, 30 fps, só o keen no áudio) e
rev6/golpes_fundo_rev6_mudo.mp4 (mesma imagem, sem som).

Só corte seco entre takes, sem animação. Os recortes tiram a barra de status
da gravação de tela, a interface do app e os textos/nomes gravados nos vídeos.
Imagens do acervo: só a conversão HLG -> SDR (técnica) e o recorte 9:16.
"""
import os
import subprocess

W, H, FPS = 1080, 1920, 30
G = "fonte/golpes/"
A = "fonte/acervo/"
TMP = "rev6/_tmp/"

# HLG (iPhone, BT.2020) -> SDR BT.709, a mesma conversão de reels/madrid-show/rev1/rev1.py
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)

# Recorte de cada gravação de tela (w:h:x:y), já sem barra de status e sem interface
CROP = {
    "g1_0738": "1056:1878:75:278",   # metrô de Paris (imagem de y 277 a 2156)
    "g2_0739": "1206:2144:0:200",    # Termini, Roma
    "g3_0740": "1122:1996:42:160",   # petição, Paris
    "g5_0744": "1206:2144:0:180",    # pulseira, Roma e Milão
    "g6_1357": "1206:2144:0:180",    # furto na bolsa, Milão
    "g4_0742": "1206:2144:0:180",    # jogo dos copinhos, Roma
    "g7_1538@metro": "953:1694:200:346",  # metrô de Barcelona: sem título e sem brasão do topo
    "g7_1538@veneza": "1206:2144:0:200",  # Veneza, vaporetto
}

# (bloco, arquivo, início, fim)
TAKES = [
    # 1 GANCHO
    ("gancho", "g6_1357", 1.75, 5.55),
    ("gancho", "g2_0739", 0.60, 1.80),
    # 2 DADO
    ("dado", "g7_1538@metro", 1.90, 4.40),
    ("dado", "g7_1538@veneza", 10.20, 13.70),
    # 3 ABERTURA · roda de golpistas sorrindo (jogo dos copinhos, Roma)
    ("abertura", "g4_0742", 6.40, 9.60),
    # 4 RELEVÂNCIA · turistas na Plaza Mayor -> batedoras no Termini
    ("relevancia", "IMG_3647", 0.50, 3.00),
    ("relevancia", "g2_0739", 2.00, 4.50),
    # 5 GOLPE 1 · pulseira
    ("golpe1", "g5_0744", 6.15, 9.40),
    ("golpe1", "g5_0744", 29.95, 32.70),
    # 6 GOLPE 2 · petição
    ("golpe2", "g3_0740", 1.40, 7.70),
    ("golpe2", "g3_0740", 14.95, 15.95),
    # 7 GOLPE 3 · fotos com personagens (acervo Madrid, Palácio Real)
    ("golpe3", "IMG_3734", 0.40, 3.60),
    ("golpe3", "IMG_3743", 0.30, 2.00),
    ("golpe3", "IMG_3744", 2.20, 4.40),
    # 8 MORAL · Puerta del Sol, calma
    ("moral", "IMG_3634", 0.20, 5.50),
    # 9 CTA · Tío Pepe (Sol) -> Plaza Mayor
    ("cta", "IMG_3630", 0.20, 2.90),
    ("cta", "IMG_3647", 3.50, 7.50),
]

# Posição x do recorte 9:16 (1215 px) no quadro 3840 do acervo; padrão = centro
CROP_X_ACERVO = {
    "IMG_3744": 1900,   # fantasia azul entre x 2280 e 2820: o centro (1312) cortava metade
}

# Texto do gancho · linguagem do formato (docs/FORMATOS_REELS.md, 4.1): Anton, caixa-alta,
# branco, alinhado em x 72, linha a linha (160 ms de opacidade + 24 px). Sem degradê na tela;
# só a sombra nas letras (CLAUDE.md, 12, padrão de 19/11/2026).
FONTE = "rev6/fontes/Anton-Regular.ttf"
GANCHO_LINHAS = [("GOLPES", 250, None, (229, 57, 53, 255)), ("NA EUROPA", 175, 0.40, (255, 255, 255, 255))]   # (texto, px, entrada em s, cor RGBA)
# GOLPES em vermelho #E53935: decisão do Diego (27/11/2026), só neste Reel; não é valor do DS nem do formato.
GANCHO_X, GANCHO_Y, GANCHO_GAP = 72, 210, 24
ENTRADA, SUBIDA = 0.16, 24


def pngs_gancho():
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    saidas, y = [], GANCHO_Y
    for i, (txt, px, _, cor) in enumerate(GANCHO_LINHAS):
        f = ImageFont.truetype(FONTE, px)
        x0, y0, x1, y1 = f.getbbox(txt)
        assert GANCHO_X + (x1 - x0) <= 944, f"{txt} passa de x 944"
        pos = (GANCHO_X - x0, y - y0)
        sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).text((pos[0], pos[1] + 4), txt, font=f, fill=(0, 0, 0, 200))
        sombra = sombra.filter(ImageFilter.GaussianBlur(14))
        dura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(dura).text((pos[0], pos[1] + 4), txt, font=f, fill=(0, 0, 0, 110))
        img = Image.alpha_composite(sombra, dura)
        ImageDraw.Draw(img).text(pos, txt, font=f, fill=cor)
        out = f"{TMP}gancho_{i}.png"
        img.save(out)
        saidas.append(out)
        y += (y1 - y0) + GANCHO_GAP
    return saidas


KEEN = "../../design-system/sons/externos/keen.wav"
KEEN_PICO = 0.96          # s, pico do arquivo
KEEN_GANHO_DB = -6        # volume de trabalho (CLAUDE.md, 12), a calibrar na escuta


def filtro(nome):
    if nome.startswith("IMG_"):
        # 3840x2160 HLG -> recorte 9:16 (1215x2160) -> 1080x1920
        x = CROP_X_ACERVO.get(nome, (3840 - 1215) // 2)
        return f"{TONEMAP},crop=1215:2160:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p"
    return f"crop={CROP[nome]},scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p"


def caminho(nome):
    nome = nome.split("@")[0]
    return (A + nome + ".MOV") if nome.startswith("IMG_") else (G + nome + ".mp4")


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    os.makedirs(TMP, exist_ok=True)
    partes, t, inicio_bloco = [], 0.0, {}
    for i, (bloco, nome, a, b) in enumerate(TAKES):
        inicio_bloco.setdefault(bloco, t)
        n = round((b - a) * FPS)
        out = f"{TMP}{i:02d}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", caminho(nome),
             "-vf", filtro(nome), "-frames:v", str(n), "-an",
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", str(FPS),
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out])
        partes.append(out)
        t += n / FPS

    with open(f"{TMP}lista.txt", "w") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in partes)
    video = f"{TMP}video.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}lista.txt",
         "-c", "copy", video])

    total = t
    fim_gancho = inicio_bloco["dado"]
    pngs = pngs_gancho()
    entradas, cadeia, ult = [], [], "[0:v]"
    for i, (p, (_, _, st, _c)) in enumerate(zip(pngs, GANCHO_LINHAS)):
        entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{fim_gancho + 1}", "-i", p]
        if st is None:
            cadeia.append(f"[{i+1}:v]format=rgba[l{i}]")
            y = "0"
        else:
            cadeia.append(f"[{i+1}:v]format=rgba,fade=t=in:st={st}:d={ENTRADA}:alpha=1[l{i}]")
            y = f"'{SUBIDA}*(1-min(max(t-{st},0)/{ENTRADA},1))'"
        cadeia.append(f"{ult}[l{i}]overlay=x=0:y={y}:enable='lt(t,{fim_gancho})':eof_action=pass[v{i}]")
        ult = f"[v{i}]"
    com_texto = f"{TMP}video_texto.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", video, *entradas, "-filter_complex", ";".join(cadeia),
         "-map", ult, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", com_texto])
    video = com_texto
    corte_keen = inicio_bloco["relevancia"]       # fim da abertura (gancho em 3 frases)
    atraso_ms = int(round((corte_keen - KEEN_PICO) * 1000))

    run(["ffmpeg", "-v", "error", "-y", "-i", video,
         "-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=48000:cl=stereo", "-i", KEEN,
         "-filter_complex",
         f"[2]aformat=sample_rates=48000:channel_layouts=stereo,volume={KEEN_GANHO_DB}dB,"
         f"adelay={atraso_ms}|{atraso_ms}[k];[1][k]amix=inputs=2:duration=first:normalize=0[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", "rev6/golpes_fundo_rev6.mp4"])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-f", "lavfi", "-t", f"{total}",
         "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-shortest", "-movflags", "+faststart", "rev6/golpes_fundo_rev6_mudo.mp4"])

    print(f"duração total: {total:.2f} s · keen com pico em {corte_keen:.2f} s")
    for bloco, s in inicio_bloco.items():
        print(f"  {bloco:<11} {s:6.2f} s")


if __name__ == "__main__":
    main()
