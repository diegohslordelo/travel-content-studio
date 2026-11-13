"""REV2 · Veneza bate-volta · preparo (rodar de dentro de reels/veneza-bate-volta/rev2).

Parte da REV1 (CLAUDE.md, 12): voz e gravação decupada são as da REV1 (áudio aprovado pelo Diego em 13/11/2026),
copiadas de ../rev1/public. Aqui só entram: novos clipes do acervo, imagens, e as palavras com tempo medido
no áudio final (Whisper large-v3 na voz da REV1, início de cada palavra ajustado pela energia da voz).
"""
import json, os, shutil, subprocess

import numpy as np

FONTE = "../fonte"
REV1 = "../rev1"
PUB = "public"
os.makedirs(f"{PUB}/fontes", exist_ok=True)
# mesma conversão HLG→SDR da REV1 (comparada com a prévia do Drive)
CONV = ("zscale=t=linear:npl=600,format=gbrpf32le,zscale=p=bt709,tonemap=clip:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def run(c):
    subprocess.run(c, shell=True, check=True)


for f in ["diego.mp4", "voz.wav"]:
    if not os.path.exists(f"{PUB}/{f}"):
        shutil.copy(f"{REV1}/public/{f}", f"{PUB}/{f}")
for f in os.listdir(f"{REV1}/public/fontes"):
    shutil.copy(f"{REV1}/public/fontes/{f}", f"{PUB}/fontes/{f}")

# clipes do acervo (mudos, SDR, 1080 de largura). Cada trecho conferido quadro a quadro: sem Diego nem Marina.
CLIPES = {  # nome: (arquivo, início, duração)
    "ducale_lotado": ("IMG_6062", 6.0, 3.6),     # Palácio Ducal lotado (gancho)
    "praca_lotada": ("IMG_6063", 12.3, 3.2),     # Praça São Marcos cheia ("30 milhões")
    "gondolas": ("IMG_6099", 1.0, 2.8),          # gôndolas de dia ("não é que Veneza não te quer lá")
    "noite_luzes": ("IMG_6128", 1.0, 3.4),       # Grande Canal à noite, barcos parados, ninguém ("a cidade fica deserta")
    "canal_dia": ("IMG_6016", 0.0, 2.6),         # Grande Canal de dia ("fazer tudo em um dia")
    "canais": ("IMG_6016", 3.0, 3.0),            # Grande Canal com gôndola, sem ninguém em primeiro plano ("cidade dos canais")
}
for nome, (arq, ini, d) in CLIPES.items():
    out = f"{PUB}/{nome}.mp4"
    if not os.path.exists(out):
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i {FONTE}/acervo/{arq}.MOV -an -vf "{CONV},scale=1080:-2" '
            f'-c:v libx264 -crf 17 -preset fast -r 30 {out}')

# imagens (Wikimedia Commons e prints de referência)
IMAGENS = {
    "arena_verona.jpg": f"{FONTE}/web/Arena_di_Verona.jpg",
    "ponte_pietra.jpg": f"{FONTE}/web/Ponte_Pietra_Verona.jpg",
    "julieta_varanda.jpg": f"{FONTE}/web2/c2.jpg",  # Commons: Verona_-_Juliet_Balcony.jpg
    "salute_noite.jpg": f"{FONTE}/web2/salute_noite.jpg",  # Commons: Santa_Maria_della_Salute_from_Hotel_Monaco_nightview.jpg
    "fortune_titulo.png": f"{FONTE}/web2/fortune_titulo.png",
    "fortune_paragrafo.png": f"{FONTE}/web2/fortune_paragrafo.png",
}
for dst, src in IMAGENS.items():
    shutil.copy(src, f"{PUB}/{dst}")
# título da página oficial "Contributo di Accesso a Venezia" (sem o aviso do fim da temporada 2026 nem o logo quebrado)
from PIL import Image
Image.open(f"{FONTE}/web2/cda_site.png").convert("RGB").crop((0, 320, 1520, 600)).save(f"{PUB}/cda_cabecalho.jpg", quality=95)

# palavras no áudio final: junta "bate -volta" e "25 %", ajusta o início pela energia da voz
pal = json.load(open("palavras_voz_final.json"))
fix = []
for w in pal:
    if fix and (w["w"].startswith("-") or w["w"] == "%"):
        fix[-1]["w"] += w["w"]; fix[-1]["e"] = w["e"]; continue
    fix.append({"w": w["w"], "s": w["s"], "e": w["e"]})
raw = subprocess.run(f'ffmpeg -v error -i {PUB}/voz.wav -af "highpass=f=80,lowpass=f=6000" -ac 1 -ar 16000 -f s16le -',
                     shell=True, check=True, capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
n = len(x) // 160
db = 20 * np.log10(np.sqrt((x[: n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)
for w in fix:
    i0, i1 = int(w["s"] * 100), int(w["e"] * 100)
    if i0 < n and db[i0] < -45:  # começo caiu em silêncio: avança até a voz
        j = i0
        while j < min(i1, n - 1) and db[j] < -45:
            j += 1
        if j < i1:
            w["s"] = j / 100
    w["s"], w["e"] = round(w["s"], 3), round(max(w["e"], w["s"] + 0.08), 3)
DUR = round(float(subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {PUB}/voz.wav",
                                 shell=True, capture_output=True, text=True).stdout), 3)
json.dump({"dur": DUR, "palavras": fix}, open("base.json", "w"), ensure_ascii=False)
print("DUR", DUR, "palavras", len(fix))
