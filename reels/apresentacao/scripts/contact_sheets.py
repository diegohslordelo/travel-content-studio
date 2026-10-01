"""Monta contact sheets a partir dos frames extraídos (1 a cada 2 s).

Cada miniatura recebe o timestamp do original e uma guia 9:16 centralizada
(retângulo tracejado) para mostrar o que sobra no crop vertical.

Uso: python3 contact_sheets.py PASTA_FRAMES PASTA_SAIDA [intervalo_s] [colunas] [linhas] [largura_miniatura]
Os frames devem se chamar f_00001.jpg, f_00002.jpg... (frame n = (n-1)*intervalo s).
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def hms(t):
    t = int(round(t))
    return f"{t // 3600:d}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def main():
    pasta, saida = sys.argv[1], sys.argv[2]
    intervalo = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    lins = int(sys.argv[5]) if len(sys.argv) > 5 else 5
    os.makedirs(saida, exist_ok=True)
    frames = sorted(glob.glob(os.path.join(pasta, "f_*.jpg")))
    if not frames:
        sys.exit("nenhum frame encontrado")
    amostra = Image.open(frames[0])
    tw = int(sys.argv[6]) if len(sys.argv) > 6 else 320
    th = round(tw * amostra.size[1] / amostra.size[0])
    faixa = 26  # faixa do timestamp
    fonte = ImageFont.truetype(FONTE, 20)
    fonte_tit = ImageFont.truetype(FONTE, 24)
    por_folha = cols * lins
    topo = 40
    for f0 in range(0, len(frames), por_folha):
        lote = frames[f0:f0 + por_folha]
        folha = Image.new("RGB", (cols * (tw + 6) + 6, topo + lins * (th + faixa + 6) + 6), (18, 18, 18))
        d = ImageDraw.Draw(folha)
        t_ini = f0 * intervalo
        t_fim = (f0 + len(lote) - 1) * intervalo
        d.text((8, 8), f"Folha {f0 // por_folha + 1:02d}  |  {hms(t_ini)} a {hms(t_fim)}  |  1 frame a cada {intervalo:g}s  |  tracejado = crop 9:16 centralizado",
               font=fonte_tit, fill=(240, 240, 240))
        for i, caminho in enumerate(lote):
            n = f0 + i
            x = 6 + (i % cols) * (tw + 6)
            y = topo + (i // cols) * (th + faixa + 6)
            img = Image.open(caminho).convert("RGB")
            if img.size != (tw, th):
                img = img.resize((tw, th))
            # guia do crop 9:16 centralizado
            if tw > th:
                gw = round(th * 9 / 16)
                gx = (tw - gw) // 2
                dd = ImageDraw.Draw(img)
                for yy in range(0, th, 8):
                    dd.line([(gx, yy), (gx, yy + 4)], fill=(255, 210, 0), width=1)
                    dd.line([(gx + gw, yy), (gx + gw, yy + 4)], fill=(255, 210, 0), width=1)
            folha.paste(img, (x, y + faixa))
            d.rectangle([x, y, x + tw, y + faixa - 1], fill=(0, 0, 0))
            d.text((x + 6, y + 2), hms(n * intervalo), font=fonte, fill=(255, 220, 90))
            d.text((x + tw - 70, y + 2), f"#{n + 1}", font=fonte, fill=(150, 150, 150))
        destino = os.path.join(saida, f"contact_sheet_{f0 // por_folha + 1:02d}.jpg")
        folha.save(destino, quality=88)
        print(destino)


if __name__ == "__main__":
    main()
