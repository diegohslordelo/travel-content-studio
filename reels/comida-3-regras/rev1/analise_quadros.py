"""REV1 · QA do vídeo final (rodar de dentro de rev1): formato, loudness, quadros pretos, P&B só no take pedido,
distância entre texto e rosto em todo quadro com o Diego, duração das cenas e folha de 1 quadro por segundo.

Uso: python3 analise_quadros.py comida_3_formas_rev1.mp4
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

V = sys.argv[1]
FPS = 30
p = json.load(open("props.json"))
base = json.load(open("base.json"))
ROSTO = json.load(open("rosto_A.json"))


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True)


print(sh(f"ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate -show_entries format=duration -of compact {V}").stdout)
r = sh(f"ffmpeg -hide_banner -nostats -i {V} -af ebur128=peak=true -f null -").stderr
resumo = r.rsplit("Summary:", 1)[1]
print(f"loudness: {float(resumo.split('I:')[1].split('LUFS')[0]):.1f} LUFS integrados · pico verdadeiro {float(resumo.split('Peak:')[1].split('dBFS')[0]):.1f} dBTP")

W, H = 270, 480
raw = subprocess.run(f"ffmpeg -v error -i {V} -vf scale={W}:{H} -f rawvideo -pix_fmt rgb24 -", shell=True, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
n = len(fr)
Y = fr.mean((1, 2, 3))
print(f"quadros: {n} · luminância mínima {Y.min():.0f}/255 no quadro {Y.argmin()} ({Y.argmin() / FPS:.2f} s)")
cena_de = lambda t: next((c for c in p["cenas"] if c["ini"] <= t < c["fim"]), p["cenas"][-1])
corte_de = lambda t: next((c for c in p["cortes"] if c["ini"] <= t < c["fim"]), p["cortes"][-1])

# P&B: no Diego em tela cheia, área do rosto; na tela dividida, metade de baixo
pb_err = []
for i in range(0, n, 3):
    t = i / FPS
    c, k = cena_de(t), corte_de(t)
    if c["tipo"] == "grafcheio":
        continue
    zona = fr[i, 40:300] if c["tipo"] == "diego" else fr[i, 260:400]
    rb = np.abs(zona[..., 0].astype(int) - zona[..., 2].astype(int)).mean()
    if k["pb"] and rb > 1.5 or not k["pb"] and rb < 3:
        pb_err.append((round(t, 2), k["take"], round(rb, 1)))
print("P&B fora do lugar:", pb_err or "nenhum", "· takes em P&B:", [k["take"] for k in p["cortes"] if k["pb"]])

# texto × rosto em todo quadro com o Diego
tipico = {}
for ct in base["cortes"]:
    a, b = ct["q_in"] / FPS, ct["q_out"] / FPS
    rr = np.array([x[1:] for x in ROSTO if a <= x[0] <= b and x[1] is not None and 250 < x[4] < 760])
    tipico[ct["ini"]] = (np.median(rr[:, 1]), np.median(rr[:, 0] + rr[:, 2] / 2))
grupo_em = []
for k, g in enumerate(p["grupos"]):
    a = p["palavras"][g[0]]["s"]
    fim = p["palavras"][g[-1]]["e"] + 0.3
    b = min(p["palavras"][p["grupos"][k + 1][0]]["s"], fim) if k + 1 < len(p["grupos"]) else fim
    grupo_em.append((a, b, k))
pior = []
for i in range(n):
    t = i / FPS
    c, k = cena_de(t), corte_de(t)
    if c["tipo"] == "grafcheio":   # ele fora da tela (grafismo em tela cheia)
        continue
    ct = next(x for x in base["cortes"] if abs(x["ini"] - k["ini"]) < 1e-3)
    ts = ct["q_in"] / FPS + (t - ct["ini"])
    caixa = min(ROSTO, key=lambda x: abs(x[0] - ts))
    if caixa[1] is None or abs(caixa[0] - ts) > 0.06 or not (250 < caixa[4] < 760):
        continue
    x0, y0, w, h = caixa[1:]
    ty, cx = tipico[ct["ini"]]
    if abs(y0 - ty) >= 220 or abs(x0 + w / 2 - cx) >= 320:
        continue
    viz = [x for x in ROSTO if abs(x[0] - caixa[0]) < 0.15 and x[1] is not None]   # mediana de 3 amostras, como em cenas.py
    if len(viz) >= 2:
        y0 = float(np.median([x[2] for x in viz])); h = float(np.median([x[4] for x in viz]))
    if c["tipo"] == "diego":
        topo, barba = y0, y0 + 1.05 * h
    else:
        topo = 900 + k["div_off"] + y0
        barba = topo + 1.05 * h
    g = next((x for x in grupo_em if x[0] <= t < x[1]), None)
    if g and t < p["cta"]["leg_fim"]:
        yc = p["gy"][g[2]] if c["tipo"] == "diego" else 900
        a, b = yc - 37, yc + 37
        folga = min(abs(a - barba), abs(topo - b)) if (b < topo or a > barba) else -min(b - topo, barba - a)
        pior.append((round(folga), round(t, 2), "legenda"))
    if t >= p["cta"]["ini"]:
        pior.append((round(p["cta"]["placa_y"] - barba), round(t, 2), "placa"))
pior.sort()
print("texto × rosto: menor folga (px, negativo = encosta):", pior[:6])

durs = [(round(min(c["fim"], p["dur"]) - c["ini"], 2), c.get("graf") or c.get("src") or c["tipo"]) for c in p["cenas"]]
print("menor cena:", min(durs), "· cenas:", len(durs))

cols = 10
ims = [Image.fromarray(fr[min(n - 1, s * FPS)]).resize((135, 240)) for s in range(int(n / FPS) + 1)]
folha = Image.new("RGB", (135 * cols, 240 * ((len(ims) + cols - 1) // cols)), "white")
for s, im in enumerate(ims):
    x, y = (s % cols) * 135, (s // cols) * 240
    folha.paste(im, (x, y))
    ImageDraw.Draw(folha).text((x + 3, y + 3), f"{s}s", fill=(255, 0, 0))
folha.save("qa_folha_1qps.jpg", quality=82)
print("folha: qa_folha_1qps.jpg")
