"""REV4 · QA do vídeo final (rodar de dentro de rev4): formato, loudness, quadros pretos, P&B só nos takes
pedidos, distância entre texto e rosto em todo quadro com o Diego, e folha de 1 quadro por segundo.

Uso: python3 analise_quadros.py veneza_bate_volta_rev4.mp4
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
ROSTO = {"A": json.load(open("rosto_A.json")), "B": json.load(open("rosto_B.json"))}


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True)


# 1. formato
print(sh(f"ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate -show_entries format=duration -of compact {V}").stdout)

# 2. loudness (DS 4.6: −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP)
r = sh(f"ffmpeg -hide_banner -nostats -i {V} -af ebur128=peak=true -f null -").stderr
resumo = r.rsplit("Summary:", 1)[1]
I = float(resumo.split("I:")[1].split("LUFS")[0])
TP = float(resumo.split("Peak:")[1].split("dBFS")[0])
print(f"loudness: {I:.1f} LUFS integrados · pico verdadeiro {TP:.1f} dBTP")

# 3. quadros (1/4 da resolução): luminância e diferença R−B (P&B)
W, H = 270, 480
raw = subprocess.run(f"ffmpeg -v error -i {V} -vf scale={W}:{H} -f rawvideo -pix_fmt rgb24 -", shell=True, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
n = len(fr)
Y = fr.mean((1, 2, 3))
print(f"quadros: {n} · luminância mínima {Y.min():.0f}/255 no quadro {Y.argmin()} ({Y.argmin() / FPS:.2f} s)")
cena_de = lambda t: next((c for c in p["cenas"] if c["ini"] <= t < c["fim"]), p["cenas"][-1])
corte_de = lambda t: next((c for c in p["cortes"] if c["ini"] <= t < c["fim"]), p["cortes"][-1])
pb_err = []
for i in range(0, n, 3):
    t = i / FPS
    c, k = cena_de(t), corte_de(t)
    if c["tipo"] != "diego":
        continue
    rb = np.abs(fr[i, 40:300, :, 0].astype(int) - fr[i, 40:300, :, 2].astype(int)).mean()   # área do rosto, sem a legenda
    if k["pb"] and rb > 1.5 or not k["pb"] and rb < 3:
        pb_err.append((round(t, 2), k["take"], round(rb, 1)))
print("P&B fora do lugar:", pb_err or "nenhum", "· takes em P&B:", [k["take"] for k in p["cortes"] if k["pb"]])

# 4. texto × rosto em todo quadro com o Diego (caixa do detector; barba = base + 5% da altura).
# Falso positivo (mão, rosto + fundo): caixa longe da posição típica do rosto no take, como em cenas.py.
tipico = {}
for ct in base["cortes"]:
    a, b = ct["q_in"] / FPS, ct["q_out"] / FPS
    r = np.array([x[1:] for x in ROSTO[ct["fonte"]] if a <= x[0] <= b and x[1] is not None and 250 < x[4] < 700])
    tipico[ct["ini"]] = (np.median(r[:, 1]), np.median(r[:, 0] + r[:, 2] / 2))
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
    ct = next(x for x in base["cortes"] if abs(x["ini"] - k["ini"]) < 1e-3)
    ts = ct["q_in"] / FPS + (t - ct["ini"])
    caixa = min(ROSTO[ct["fonte"]], key=lambda x: abs(x[0] - ts))
    if caixa[1] is None or abs(caixa[0] - ts) > 0.06 or not (250 < caixa[4] < 700):
        continue
    x0, y0, w, h = caixa[1:]
    ty, cx = tipico[ct["ini"]]
    if abs(y0 - ty) >= 220 or abs(x0 + w / 2 - cx) >= 320:
        continue
    if c["tipo"] == "diego":
        z0, z1 = c.get("zoom", [1, 1])
        z = z0 + (z1 - z0) * (t - c["ini"]) / max(0.01, c["fim"] - c["ini"])
        topo = 614 + (y0 - 614) * z
        barba = 614 + (y0 + 1.05 * h - 614) * z
    else:
        topo = 900 + k["div_off"] + y0
        barba = 900 + k["div_off"] + y0 + 1.05 * h
    g = next((x for x in grupo_em if x[0] <= t < x[1]), None)
    if g and p["gancho"]["fim"] <= t < p["cta"]["leg_fim"]:
        yc = p["gy"][g[2]] if c["tipo"] == "diego" else 900
        a, b = yc - 37, yc + 37
        folga = min(abs(a - barba), abs(topo - b)) if (b < topo or a > barba) else -min(b - topo, barba - a)
        pior.append((folga, round(t, 2), "legenda"))
    if t >= p["cta"]["ini"]:
        folga = p["cta"]["placa_y"] - barba
        pior.append((folga, round(t, 2), "placa"))
pior.sort()
print("texto × rosto: menor folga (px, negativo = encosta):", pior[:5])

# 5. folha de 1 quadro por segundo
cols = 10
ims = [Image.fromarray(fr[min(n - 1, s * FPS)]).resize((135, 240)) for s in range(int(n / FPS) + 1)]
folha = Image.new("RGB", (135 * cols, 240 * ((len(ims) + cols - 1) // cols)), "white")
for s, im in enumerate(ims):
    x, y = (s % cols) * 135, (s // cols) * 240
    folha.paste(im, (x, y))
    ImageDraw.Draw(folha).text((x + 3, y + 3), f"{s}s", fill=(255, 0, 0))
folha.save("qa_folha_1qps.jpg", quality=82)
print("folha: qa_folha_1qps.jpg")
