"""Mockups estáticos dos textos sobre os crops reais da lista de cortes (com e sem guias de zona segura).

Uso: python3 mockups_edl.py lista_de_cortes.json SAIDA.jpg
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402


def quadro(edl, idx, frac, destino):
    c = edl["_cortes"][idx]
    t = c["entrada"] + (c["saida"] - c["entrada"]) * frac
    c2 = R.corte_parado(c, frac)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", c["_arq"], "-map", "0:v:0", "-frames:v", "1",
                    "-vf", R.filtro_video(c2, "rgb24"), destino], check=True)
    return Image.open(destino).convert("RGBA")


def colar_legenda(img, texto):
    leg = R.render_legenda(texto)
    img.alpha_composite(leg, ((R.W - leg.width) // 2, R.Y_LEGENDA - leg.height // 2))


def guias(img):
    d = ImageDraw.Draw(img)
    cor = (255, 60, 60, 255)
    for y in (R.SEG_TOPO, R.H - R.SEG_BASE):
        for x in range(0, R.W, 24):
            d.line([x, y, x + 12, y], fill=cor, width=4)
    for y in range(0, R.H, 24):
        d.line([R.W - R.SEG_DIR, y, R.W - R.SEG_DIR, y + 12], fill=cor, width=4)
    return img


def main():
    edl = R.carregar(sys.argv[1])
    tmp = os.path.join(edl["_tmp"], "_mock.png")
    telas = []
    tx = edl.get("textos", {})

    img = quadro(edl, 0, 0.5, tmp)  # gancho
    t = R.render_titulo_gancho(tx.get("gancho", {}))
    img.alpha_composite(t, ((R.W - t.width) // 2, tx.get("gancho", {}).get("y", 640)))
    img.alpha_composite(R.render_selo(), (R.MARGEM_ESQ, R.SEG_TOPO + 24))
    telas.append(("0-3s gancho", img))

    img = quadro(edl, 2, 0.3, tmp)  # apresentação
    if not edl["narracao"].get("arquivo"):
        img.alpha_composite(R.render_aviso_narracao(edl["narracao"].get("aviso") or "NARRAÇÃO · A GRAVAR"),
                            (R.MARGEM_ESQ, R.SEG_TOPO + 24))
    colar_legenda(img, R.aplicar_destaques("sou soteropolitano", edl["narracao"].get("destaques", [])))
    telas.append(("3-15s apresentação", img))

    # montagem: uma cena de outra cidade, com o selo e o nome da cidade ao lado
    i = next(i for i, c in enumerate(edl["_cortes"]) if c["bloco"] == "montagem" and c.get("cidade") == "Paris")
    img = quadro(edl, i, 0.5, tmp)
    selo = R.render_selo()
    img.alpha_composite(selo, (R.MARGEM_ESQ, R.SEG_TOPO + 24))
    img.alpha_composite(R.render_cidade("Paris", tx.get("cidade")), (R.MARGEM_ESQ + selo.width + 6, R.SEG_TOPO + 24))
    telas.append(("15-35s montagem", img))
    # montagem com fala: legenda + cidade
    i = next(i for i, c in enumerate(edl["_cortes"]) if c["bloco"] == "montagem" and c.get("legendas") and c.get("arquivo"))
    c = edl["_cortes"][i]
    lg = c["legendas"][0]
    img = quadro(edl, i, (float(lg["de"]) + 0.3 - c["entrada"]) / (c["saida"] - c["entrada"]), tmp)
    img.alpha_composite(selo, (R.MARGEM_ESQ, R.SEG_TOPO + 24))
    img.alpha_composite(R.render_cidade(c["cidade"], tx.get("cidade")), (R.MARGEM_ESQ + selo.width + 6, R.SEG_TOPO + 24))
    colar_legenda(img, lg["texto"])
    telas.append(("15-35s montagem (fala)", img))

    ult = len(edl["_cortes"]) - 1
    cfg = tx.get("aviso", {})
    a, z = edl["_blocos"]["aviso"]
    img = quadro(edl, ult, 0.7, tmp)
    c = R.render_titulo_gancho(cfg) if cfg.get("estilo") == "titulo" else R.render_cartao_final(cfg)
    img.alpha_composite(c, ((R.W - c.width) // 2, cfg.get("y", 700)))
    telas.append((f"{a:.0f}-{z:.1f}s fechamento", img))

    lado = []
    for nome, im in telas:
        g = guias(im.copy()).resize((360, 640), Image.LANCZOS).convert("RGB")
        lado.append((nome, g))
    folha = Image.new("RGB", (len(lado) * 368 + 8, 690), (20, 20, 20))
    d = ImageDraw.Draw(folha)
    from PIL import ImageFont
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    for k, (nome, g) in enumerate(lado):
        folha.paste(g, (8 + k * 368, 8))
        d.text((12 + k * 368, 656), nome, font=f, fill=(240, 240, 240))
    folha.save(sys.argv[2], quality=90)
    os.remove(tmp)
    print(sys.argv[2], "| tracejado vermelho = limites da zona segura do Instagram")


if __name__ == "__main__":
    main()
