"""Entregáveis e verificações do banner do YouTube.

Rodar depois de render.cjs, de dentro de youtube-banner/:
    python3 verify.py
Requer Pillow e numpy (pip install pillow numpy).
Lê out/_render.png e out/measurements.json; grava os entregáveis em out/ e a tabela em out/verificacao.md.
"""
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageCms, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
W, H = 2560, 1440
MAX_BYTES = 6 * 1024 * 1024

# Zonas da plataforma (conferidas em 03/10/2026)
SAFE = (507.0, 508.5, 2053.0, 931.5)        # 1546 × 423, todos os aparelhos
STRICT = (662.5, 551.0, 1897.5, 889.0)      # 1235 × 338, meta adicional
DESKTOP_Y = (508.5, 931.5)                  # faixa 2560 × 423
TABLET_X = (352.5, 2207.5)                  # 1855 × 423

TOK = {
    "signal-500": (255, 194, 26),
    "night-900": (18, 19, 23),
    "paper-500": (246, 243, 236),
    "stamp-500": (196, 48, 42),
    "ink-500": (31, 59, 179),
    "exit-600": (20, 122, 68),
}

L = json.load(open(os.path.join(OUT, "measurements.json"), encoding="utf-8"))
raw = Image.open(os.path.join(OUT, "_render.png")).convert("RGB")
srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()

rows = []  # (verificação, valor real, critério, resultado)


def check(name, value, criterion, ok):
    rows.append((name, value, criterion, "PASSA" if ok else "FALHA"))
    return ok


def fmt(x, n=1):
    return f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------- 1. Arquivos finais ----------
png_path = os.path.join(OUT, "primeiro-dia_youtube-banner_2560x1440.png")
jpg_path = os.path.join(OUT, "primeiro-dia_youtube-banner_2560x1440.jpg")
raw.save(png_path, "PNG", optimize=True, icc_profile=srgb)
raw.save(jpg_path, "JPEG", quality=92, subsampling=0, icc_profile=srgb)
png = Image.open(png_path)
jpg = Image.open(jpg_path)
png_b, jpg_b = os.path.getsize(png_path), os.path.getsize(jpg_path)
check("PNG: dimensões", f"{png.size[0]} × {png.size[1]}", "2560 × 1440", png.size == (W, H))
check("PNG: tamanho", f"{fmt(png_b / 1048576, 2)} MB ({fmt(png_b, 0)} bytes)", "≤ 6 MB", png_b <= MAX_BYTES)
check("JPG q92: dimensões", f"{jpg.size[0]} × {jpg.size[1]}", "2560 × 1440", jpg.size == (W, H))
check("JPG q92: tamanho", f"{fmt(jpg_b / 1048576, 2)} MB ({fmt(jpg_b, 0)} bytes)", "≤ 6 MB", jpg_b <= MAX_BYTES)
check("Perfil de cor embutido", "sRGB (ICC) em PNG e JPG",
      "sRGB", bool(png.info.get("icc_profile")) and bool(jpg.info.get("icc_profile")))

# ---------- 2. Zona segura ----------
def margins(box, zone):
    return (box["left"] - zone[0], box["top"] - zone[1], zone[2] - box["right"], zone[3] - box["bottom"])


# Tinta real da tagline, medida nos pixels (independente do DOM): a caixa de linha não contém o descendente do "p".
lum8 = np.asarray(raw.convert("L")).astype(int)
t = L["tagline"]
x0, y0, x1, y1 = int(t["left"]) - 20, int(t["top"]), int(t["right"]) + 20, int(t["bottom"]) + 40
ys, xs = np.where(lum8[y0:y1, x0:x1] < 150)
L["taglinePixels"] = {"left": float(xs.min() + x0), "top": float(ys.min() + y0),
                      "right": float(xs.max() + x0 + 1), "bottom": float(ys.max() + y0 + 1)}
pxg = {"left": min(L["plate"]["left"], L["taglinePixels"]["left"]), "right": max(L["plate"]["right"], L["taglinePixels"]["right"]),
       "top": min(L["plate"]["top"], L["taglinePixels"]["top"]), "bottom": max(L["plate"]["bottom"], L["taglinePixels"]["bottom"])}
L["groupPixels"] = pxg

BOXES = (("Placa (caixa)", "plate"), ("Tagline (caixa de linha)", "tagline"),
         ("Tagline (tinta, measureText)", "taglineInk"), ("Tagline (tinta, pixels)", "taglinePixels"),
         ("Grupo (placa + tinta da tagline, pixels)", "groupPixels"))
for label, key in BOXES:
    m = margins(L[key], SAFE)
    check(f"{label} em 1546 × 423 (folga ≥ 40)",
          "folgas E/T/D/B = " + " / ".join(fmt(v) for v in m),
          "todas ≥ 40 px", min(m) >= 40)
for label, key in BOXES:
    m = margins(L[key], STRICT)
    check(f"{label} em 1235 × 338 (meta)",
          "folgas E/T/D/B = " + " / ".join(fmt(v) for v in m),
          "todas ≥ 0 px", min(m) >= 0)
g = L["group"]
gc = ((g["left"] + g["right"]) / 2, (g["top"] + g["bottom"]) / 2)
check("Centro do grupo (placa + tinta da tagline)", f"x {fmt(gc[0], 2)} · y {fmt(gc[1], 2)}", "x 1280 · y 720 (± 0,5)",
      abs(gc[0] - 1280) <= 0.5 and abs(gc[1] - 720) <= 0.5)
gpc = ((pxg["left"] + pxg["right"]) / 2, (pxg["top"] + pxg["bottom"]) / 2)
check("Centro do grupo medido nos pixels", f"x {fmt(gpc[0], 2)} · y {fmt(gpc[1], 2)}", "x 1280 · y 720 (± 1,5)",
      abs(gpc[0] - 1280) <= 1.5 and abs(gpc[1] - 720) <= 1.5)
gl_ = L["groupLineBoxes"]
rows.append(("Centro do grupo por caixas de linha (informativo)",
             f"x {fmt((gl_['left'] + gl_['right']) / 2, 2)} · y {fmt((gl_['top'] + gl_['bottom']) / 2, 2)}",
             "—", "INFO"))
check("Tagline: distância da base da placa", f"{fmt(L['gapPlateTagline'], 2)} px", "32 px",
      abs(L["gapPlateTagline"] - 32) < 0.01)
check("Tagline: alinhada à borda esquerda da face", f"Δ {fmt(L['taglineLeftMinusFaceLeft'], 2)} px", "0 px",
      abs(L["taglineLeftMinusFaceLeft"]) < 0.01)

# ---------- 3. Razão tipográfica ----------
ratio = L["plateFontPx"] / L["taglineFontPx"]
check("Razão placa : tagline (corpo da fonte)",
      f"{fmt(L['plateFontPx'], 0)} : {fmt(L['taglineFontPx'], 0)} = {fmt(ratio, 2)} : 1", "≥ 2 : 1", ratio >= 2 - 1e-9)

# ---------- 4. Contraste WCAG ----------
def lum(rgb):
    c = [v / 255 for v in rgb]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


c1 = contrast(TOK["night-900"], TOK["signal-500"])
c2 = contrast(TOK["night-900"], TOK["paper-500"])
check("Contraste grafite / amarelo", f"{fmt(c1, 2)} : 1", "esperado 11,48 : 1 (AAA ≥ 7)", round(c1, 2) == 11.48)
check("Contraste grafite / papel", f"{fmt(c2, 2)} : 1", "esperado 16,75 : 1 (AAA ≥ 7)", round(c2, 2) == 16.75)

# ---------- 5. Contagem de pixels ----------
a = np.asarray(raw).astype(np.float32)
r, gch, b = a[..., 0] / 255, a[..., 1] / 255, a[..., 2] / 255
mx, mn = np.max(a / 255, axis=2), np.min(a / 255, axis=2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
d = mx - mn
hue = np.zeros_like(mx)
nz = d > 1e-6
idx = nz & (mx == r)
hue[idx] = (60 * ((gch[idx] - b[idx]) / d[idx]) + 360) % 360
idx = nz & (mx == gch) & ~(mx == r)
hue[idx] = 60 * ((b[idx] - r[idx]) / d[idx]) + 120
idx = nz & (mx == b) & ~(mx == r) & ~(mx == gch)
hue[idx] = 60 * ((r[idx] - gch[idx]) / d[idx]) + 240
total = W * H

yellow = (hue >= 30) & (hue <= 60) & (sat >= 0.45) & (mx >= 0.55)
red = ((hue <= 15) | (hue >= 345)) & (sat >= 0.35) & (mx >= 0.25)
green = (hue >= 90) & (hue <= 170) & (sat >= 0.35) & (mx >= 0.20)
blue = (hue >= 200) & (hue <= 260) & (sat >= 0.35) & (mx >= 0.20)


def near(tok, tol=48):
    t = np.array(TOK[tok], dtype=np.float32)
    return np.sqrt(((a - t) ** 2).sum(axis=2)) <= tol


pct = lambda m: 100 * m.sum() / total
check("Amarelo (família, matiz 30–60°, sat ≥ 45%)", f"{fmt(pct(yellow), 2)} % ({fmt(int(yellow.sum()), 0)} px)",
      "≤ 10 % da área", pct(yellow) <= 10)
for name, m, tok in (("Vermelho", red, "stamp-500"), ("Azul", blue, "ink-500"), ("Verde", green, "exit-600")):
    nm = near(tok)
    check(f"{name}: matiz + distância ao token {tok}",
          f"matiz {fmt(pct(m), 4)} % ({int(m.sum())} px) · ΔRGB ≤ 48: {fmt(pct(nm), 4)} % ({int(nm.sum())} px)",
          "≤ 0,01 %", pct(m) <= 0.01 and pct(nm) <= 0.01)
yel_rows = np.where(yellow.any(axis=1))[0]
check("Pixels amarelos fora da faixa desktop", f"y {yel_rows.min()}–{yel_rows.max()}",
      "dentro de y 508,5–931,5", yel_rows.min() >= DESKTOP_Y[0] and yel_rows.max() <= DESKTOP_Y[1])

# ---------- 6. Rota e pin na faixa desktop ----------
rb, pw = L["routeBBox"], L["pin"]["wrapper"]
check("Rota (traço de 16 px) na faixa desktop, folga ≥ 24",
      f"y {fmt(rb['top'])}–{fmt(rb['bottom'])} · folgas {fmt(rb['top'] - DESKTOP_Y[0])} / {fmt(DESKTOP_Y[1] - rb['bottom'])}",
      "≥ 24 px", rb["top"] - DESKTOP_Y[0] >= 24 and DESKTOP_Y[1] - rb["bottom"] >= 24)
check("Pin na faixa desktop, folga ≥ 24",
      f"y {fmt(pw['top'])}–{fmt(pw['bottom'])} · folgas {fmt(pw['top'] - DESKTOP_Y[0])} / {fmt(DESKTOP_Y[1] - pw['bottom'])}",
      "≥ 24 px", pw["top"] - DESKTOP_Y[0] >= 24 and DESKTOP_Y[1] - pw["bottom"] >= 24)
check("Pin: altura", f"{fmt(L['pin']['heightPx'], 2)} px", "≈ 140 px", abs(L["pin"]["heightPx"] - 140) < 1)
check("Pin: ponta no fim da rota", f"ponta ({fmt(L['pin']['drop']['left'] + L['pin']['drop']['width'] / 2, 2)}, "
      f"{fmt(L['pin']['drop']['bottom'], 2)}) · fim da rota ({L['routePoints'][-1][0]}, {L['routePoints'][-1][1]})",
      "Δ < 0,5 px",
      abs(L["pin"]["drop"]["left"] + L["pin"]["drop"]["width"] / 2 - L["routePoints"][-1][0]) < 0.5
      and abs(L["pin"]["drop"]["bottom"] - L["routePoints"][-1][1]) < 0.5)

# Ângulos da rota: todos os segmentos são horizontais ou a 45°
pts = L["routePoints"]
ang_ok = all((p[1] == q[1]) or abs(abs(q[1] - p[1]) - abs(q[0] - p[0])) < 1e-6 for p, q in zip(pts, pts[1:]))
check("Rota: segmentos só horizontais ou a 45°", "pontos " + " → ".join(f"({fmt(p[0])}, {fmt(p[1])})" for p in pts),
      "0° ou 45°", ang_ok)

# ---------- 7. Previews ----------
def half_up(x):
    # Arredonda ,5 para cima (o round() do Python arredonda ,5 para o par e mudaria a largura do recorte)
    return int(x + 0.5)


def crop(x0, x1):
    # Bordas em ,5 px: as duas bordas sobem 0,5 px, o que mantém a largura e a altura exatas
    return raw.crop((half_up(x0), half_up(DESKTOP_Y[0]), half_up(x1), half_up(DESKTOP_Y[1])))


cel = crop(*SAFE[0::2])
tab = crop(*TABLET_X)
desk = crop(0, W)
mini = cel.resize((half_up(cel.width * 0.25), half_up(cel.height * 0.25)), Image.LANCZOS)
for im, name in ((cel, "preview_celular_1546x423.png"), (tab, "preview_tablet_1855x423.png"),
                 (desk, "preview_desktop_2560x423.png"), (mini, "preview_miniatura_25pct.png")):
    im.save(os.path.join(OUT, name), "PNG", optimize=True, icc_profile=srgb)
check("Previews: tamanhos", f"celular {cel.size} · tablet {tab.size} · desktop {desk.size} · miniatura {mini.size}",
      "1546×423 · 1855×423 · 2560×423 · ≈ 387×106",
      cel.size == (1546, 423) and tab.size == (1855, 423) and desk.size == (2560, 423) and mini.size == (387, 106))

# ---------- 8. Overlay de zona segura (NÃO subir) ----------
ov = raw.copy().convert("RGBA")
lay = Image.new("RGBA", ov.size, (0, 0, 0, 0))
dr = ImageDraw.Draw(lay)
dr.rectangle((0, DESKTOP_Y[0], W - 1, DESKTOP_Y[1]), fill=(0, 160, 255, 28))                         # desktop
dr.rectangle((TABLET_X[0], DESKTOP_Y[0], TABLET_X[1], DESKTOP_Y[1]), outline=(0, 120, 255, 255), width=3)  # tablet
dr.rectangle(SAFE, outline=(255, 0, 170, 255), width=5)                                              # 1546 × 423
dr.rectangle(STRICT, outline=(0, 170, 120, 255), width=3)                                            # 1235 × 338
dr.rectangle((g["left"], g["top"], g["right"], g["bottom"]), outline=(120, 0, 255, 255), width=2)     # grupo
dr.line((1280, 0, 1280, H), fill=(255, 0, 170, 120), width=1)
dr.line((0, 720, W, 720), fill=(255, 0, 170, 120), width=1)
dr.text((SAFE[0] + 8, SAFE[1] + 6), "1546 x 423 (todos os aparelhos)", fill=(255, 0, 170, 255))
dr.text((STRICT[0] + 8, STRICT[3] - 16), "1235 x 338 (meta)", fill=(0, 140, 100, 255))
dr.text((TABLET_X[0] + 8, DESKTOP_Y[1] - 16), "tablet 1855 x 423", fill=(0, 120, 255, 255))
dr.text((8, DESKTOP_Y[0] + 6), "desktop 2560 x 423", fill=(0, 120, 255, 255))
Image.alpha_composite(ov, lay).convert("RGB").save(os.path.join(OUT, "check_zona-segura.png"), "PNG", optimize=True)

# ---------- 9. Textura (medida, para a inspeção visual) ----------
def std(box):
    reg = np.asarray(raw.crop(box).convert("L")).astype(np.float32)
    return float(reg.std()), float(reg.mean())


paper_std = std((100, 100, 500, 400))           # papel liso, longe de tudo
face_box = (int(L["face"]["left"] + 30), int(L["face"]["top"] + 60), int(L["face"]["left"] + 70), int(L["face"]["bottom"] - 60))
face_std = std(face_box)

# ---------- Relatório ----------
fail = [r for r in rows if r[3] == "FALHA"]
md = ["| Verificação | Valor real | Critério | Resultado |", "|---|---|---|---|"]
md += [f"| {a_} | {b_} | {c_} | {('**' + d_ + '**') if d_ != 'INFO' else 'informativo'} |" for a_, b_, c_, d_ in rows]
md += ["", f"Fibra do papel: desvio-padrão de luminância {fmt(paper_std[0], 2)} (média {fmt(paper_std[1], 1)}) numa área lisa de 400 × 300 px.",
       f"Grão do esmalte: desvio-padrão {fmt(face_std[0], 2)} (média {fmt(face_std[1], 1)}) numa faixa da face sem texto."]
open(os.path.join(OUT, "verificacao.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("\n".join(md))
n = sum(r[3] != "INFO" for r in rows)
print(f"\n{n - len(fail)}/{n} verificações passaram.")
sys.exit(1 if fail else 0)
