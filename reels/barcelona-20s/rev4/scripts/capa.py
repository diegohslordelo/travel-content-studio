"""Capa 3:4 (1080 × 1440) do Reel "Barcelona em 20 segundos", REV1.

- fundo: um quadro real do bruto (mesmo recorte e tone mapping do vídeo), sem filtro
- texto: DS 1.2 Display (Barlow Condensed 800, 168 px, entrelinha 0,88, tracking −1%), alinhado à esquerda na
  margem 80 (DS 1.3, 3:4), em papel #FCFBF8 sobre scrim grafite (Display "sempre sobre objeto ou scrim")
- grão de 5% (DS 4.5)

Uso (de dentro de reels/barcelona-20s/):
  python3 rev1/scripts/capa.py --versao a --fontes PASTA [--brutos fonte]
  (o quadro vem de "capa": {"arquivo", "t", "centro_x", "centro_y"} em versao_<x>.json)
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pd  # noqa: E402
import render as R  # noqa: E402

C = pd.CFG["capa"]
CW, CH = C["largura"], C["altura"]


def quadro(arq, t, p):
    filtro, _ = R.filtro_video(arq, p, CW, CH)
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", arq, "-vf", filtro, "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, "<u2").reshape(CH, CW, 3).astype(np.float32) / 65535


def texto(fontes):
    """Bloco de texto Display centralizado no canvas pela tinta (x 540) e com o centro da tinta em
    C["centro_y_tinta"]; as linhas ficam alinhadas à esquerda dentro do bloco (DS 1.2: Display alinhado à esquerda)."""
    S = pd.SS
    f = pd.fonte("BarlowCondensed-ExtraBold.ttf", C["tamanho"] * S, fontes)
    trk = C["tracking_em"] * C["tamanho"] * S
    lh = C["tamanho"] * C["entrelinha"]
    linhas = C["linhas"]

    def mask(dx, dy):
        def desenho(d):
            for i, ln in enumerate(linhas):
                y = (dy + i * lh) * S
                x = dx * S
                for c in ln:
                    d.text((x, y), c, font=f, fill=255, anchor="ls")
                    x += f.getlength(c) + trk
        m = pd.reduzir(pd.mascara((CW * S, CH * S), desenho)[..., None])[..., 0]
        ys, xs = np.nonzero(m > 0.02)
        return m, [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    _, cx = mask(100, 400)                      # 1ª passada: mede a tinta
    dx = 100 + C["centro_x"] - (cx[0] + cx[2]) / 2
    dy = 400 + C["centro_y_tinta"] - (cx[1] + cx[3]) / 2
    return mask(dx, dy)


def simular_instagram(arq, saida):
    """Como a capa 3:4 aparece: (1) inteira, (2) como capa do Reel (a imagem preenche o 9:16 e perde as laterais),
    (3) no grid do perfil (recorte 3:4 central do 9:16)."""
    from PIL import Image as I, ImageDraw as D
    c = I.open(arq).convert("RGB")
    reel = c.resize((1440, 1920), I.LANCZOS).crop((180, 0, 1260, 1920))     # preenche 1080 × 1920
    grid = reel.crop((0, 240, 1080, 1680))
    h = 600
    vs = [c.resize((450, 600)), reel.resize((338, 600)), grid.resize((450, 600)), c.resize((270, 360)).resize((450, 600))]
    rot = ["capa 3:4 inteira", "capa do Reel (9:16)", "grid do perfil", "miniatura 25%"]
    out = I.new("RGB", (sum(v.width for v in vs) + 30 * 3, h + 30), "white")
    x = 0
    d = D.Draw(out)
    for v, r in zip(vs, rot):
        out.paste(v, (x, 0)); d.text((x + 4, h + 8), r, fill=(0, 0, 0)); x += v.width + 30
    out.save(saida, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--versao", required=True)
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--brutos", default="fonte")
    ap.add_argument("--edl", default=None)
    ap.add_argument("--saida-dir", default=None)
    a = ap.parse_args()
    ed = json.load(open(a.edl or os.path.join(pd.REV, f"versao_{a.versao}.json"), encoding="utf-8"))
    cp = ed["capa"]
    b = quadro(os.path.join(a.brutos, cp["arquivo"]), cp["t"], cp)
    img = pd.overlay_blend(b, pd.grao(0, CH, CW), pd.T["op_grain"])
    s = pd.scrim_alfa(CH, C["scrim"]["y0"], C["scrim"]["y1"], C["scrim"]["alfa"])
    img = img * (1 - s) + pd.GRAFITE * s
    m, caixa = texto(a.fontes)
    L = pd.CFG["legenda"]
    sombra = pd.sombra_objeto(m, L["sombra_dura"], {"y": 0, "blur": L["sombra_difusa"]["blur"], "spread": 0,
                                                    "alfa": L["sombra_difusa"]["alfa"]})
    img = img * (1 - sombra[..., None])
    img = img * (1 - m[..., None]) + pd.RECIBO * m[..., None]
    pasta = a.saida_dir or pd.REV
    os.makedirs(pasta, exist_ok=True)
    saida = os.path.join(pasta, "capa_barcelona_pov_v2.jpg")
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(saida, quality=95, subsampling=0)
    # conferência: margem 80 e miniatura a 25%
    ok = caixa[0] >= C["margem"] - 6 and caixa[2] <= CW - C["margem"] and caixa[1] >= C["margem"] and \
        caixa[3] <= CH - C["margem"]
    mini = Image.open(saida).resize((CW // 4, CH // 4), Image.LANCZOS)
    mini.save(saida.replace(".jpg", "_miniatura25.jpg"), quality=90)
    simular_instagram(saida, os.path.join(pd.REV, "_tmp", "capa_simulacao_instagram.jpg"))
    seg = [135, 180, 945, 1260]   # área que sobra nos dois recortes (capa do Reel e grid), em coordenadas da capa
    ok = ok and caixa[0] >= seg[0] and caixa[2] <= seg[2] and caixa[1] >= seg[1] and caixa[3] <= seg[3]
    print(json.dumps({"capa": saida, "texto_caixa": caixa, "dentro_da_margem_80": ok,
                      "palavras": sum(len(x.split()) for x in C["linhas"])}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
