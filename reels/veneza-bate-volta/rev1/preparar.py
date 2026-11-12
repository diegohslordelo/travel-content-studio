"""REV1 · Veneza bate-volta · preparo (rodar de dentro de reels/veneza-bate-volta/rev1).

Decupagem da gravação (sem espaço entre takes, nenhuma fala cortada), HDR→SDR, clipes do acervo,
palavras remapeadas para a linha do tempo final e props.json para a composição VenezaReel.
"""
import json, os, subprocess

FONTE = "../fonte"
PUB = "public"
os.makedirs(PUB, exist_ok=True)
# Diego já tratou a cor da gravação (12/11/2026): nenhuma correção de cor; só a conversão HLG→SDR padrão, a mesma
# que o Drive mostra. A mesma conversão vale para o acervo, sem grade extra.
CONV = ("zscale=t=linear:npl=600,format=gbrpf32le,zscale=p=bt709,tonemap=clip:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")  # HLG→SDR igual à prévia do Drive (comparada à miniatura do Drive, erro médio 7,5/255)
TM = CONV

# Trechos falados da gravação. Pedido do Diego: nenhuma fala cortada e nenhum espaço entre takes.
# REV1b (12/11/2026): a 1ª decupagem usava limiar −47 dB e cortou sílabas fracas (fim de "verdade", "e", "E").
# Agora só sai o trecho em que TODO quadro de 10 ms está abaixo de −62 dBFS (80–6.000 Hz: respiração e sala),
# deixando 100 ms de folga em cada lado; cada corte foi conferido no perfil de energia. Do início até o Diego sentar (0–5,5 s) nada sai.
def _trechos():
    import numpy as np
    raw = subprocess.run(f'ffmpeg -v error -i {FONTE}/gravacao.mp4 -af "highpass=f=80,lowpass=f=6000" -ac 1 -ar 16000 -f s16le -',
                         shell=True, check=True, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop = 160
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    sil = db < -62
    dur = n / 100
    cortes = []
    i = 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]:
                j += 1
            a0, b0 = i / 100 + 0.10, j / 100 - 0.10
            if b0 - a0 >= 0.10 and a0 > 5.6 and j < n:
                cortes.append((a0, b0))
            i = j
        else:
            i += 1
    tr, ini = [], 0.0
    for a0, b0 in cortes:
        tr.append((ini, a0))
        ini = b0
    tr.append((ini, dur))
    return tr, cortes


TRECHOS, CORTES = _trechos()
FPS = 30


def q(t):  # alinha ao quadro
    return round(t * FPS) / FPS


TRECHOS = [(q(a), q(b)) for a, b in TRECHOS]


def run(c):
    subprocess.run(c, shell=True, check=True)


# vídeo + áudio decupados: 1) SDR 1080×1920 inteiro; 2) cada trecho com trim exato; 3) concat
if not os.path.exists(f"{PUB}/diego.mp4"):
    if not os.path.exists("sdr.mp4"):
        run(f'ffmpeg -v error -y -i {FONTE}/gravacao.mp4 -vf "scale=1080:1920,{CONV}" -c:v libx264 -crf 14 -preset fast -r 30 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a pcm_s16le -ar 48000 sdr.mov'.replace("sdr.mov", "sdr.mp4").replace("pcm_s16le", "aac -b:a 320k"))
    run(f"ffmpeg -v error -y -i {FONTE}/gravacao.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s24le full.wav")
    lst = []
    for i, (a, b) in enumerate(TRECHOS):
        run(f'ffmpeg -v error -y -i sdr.mp4 -vf "trim={a}:{b},setpts=PTS-STARTPTS" -an -c:v libx264 -crf 16 -preset fast seg{i}.mp4')
        run(f'ffmpeg -v error -y -i full.wav -af "atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b - a - 0.012:.3f}:d=0.012" -c:a pcm_s24le aseg{i}.wav')
        lst.append(i)
    open("v.txt", "w").write("".join(f"file seg{i}.mp4\n" for i in lst))
    open("a.txt", "w").write("".join(f"file aseg{i}.wav\n" for i in lst))
    run(f"ffmpeg -v error -y -f concat -safe 0 -i v.txt -c copy {PUB}/diego.mp4")
    run("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy voz_bruta.wav")
    run("ffmpeg -v error -y -i voz_bruta.wav -af highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 public/voz.wav")

# palavras → linha do tempo final
pal = json.load(open(f"{FONTE}/palavras.json"))
off = []
acc = 0
for a, b in TRECHOS:
    off.append((a, b, acc))
    acc += b - a
DUR = acc


def mapa(t):
    for a, b, o in off:
        if t < b + 0.001:
            return o + max(0, t - a)
    return DUR


palavras = []
for w in pal:
    s, e = mapa(w["s"]), mapa(w["e"])
    palavras.append({"w": w["w"], "s": round(s, 3), "e": round(max(e, s + 0.08), 3)})
# correções de grafia (fala conferida): o Whisper separa "bate -volta" e "25 %"
fix = []
for w in palavras:
    if fix and w["w"].startswith("-"):
        fix[-1]["w"] += w["w"]; fix[-1]["e"] = w["e"]; continue
    if fix and w["w"] == "%":
        fix[-1]["w"] += "%"; fix[-1]["e"] = w["e"]; continue
    fix.append(dict(w))
palavras = fix
json.dump(palavras, open("palavras_final.json", "w"), ensure_ascii=False, indent=0)

# clipes do acervo (mudos, SDR, 1080 de largura)
CLIPES = {  # nome: (arquivo, início, duração)
    "lotada": ("IMG_6062", 0.5, 6.0),
    "praca": ("IMG_6063", 12.3, 6.0),  # começa em 12,3 s: antes disso passa uma mulher de cabelo comprido em primeiro plano
    "gondolas": ("IMG_6099", 1.0, 6.0),
    "noite_laguna": ("IMG_6128", 0.0, 6.5),
    "canal_dia": ("IMG_6016", 0.0, 6.0),
    "rialto": ("IMG_6174", 12.0, 7.0),
    "noite_vazia": ("IMG_6234", 10.0, 2.8),  # Grande Canal à noite da ponte, sem ninguém (10,0–12,8 s)
    "campanile": ("IMG_6060", 0.0, 5.0),
}
for nome, (arq, ini, d) in CLIPES.items():
    out = f"{PUB}/{nome}.mp4"
    if not os.path.exists(out):
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i {FONTE}/acervo/{arq}.MOV -an -vf "{TM},scale=1080:-2" '
            f'-c:v libx264 -crf 18 -preset fast -r 30 {out}')

for f in ["fortune_titulo.png", "fortune_80.png", "Arena_di_Verona.jpg", "Casa_di_Giulietta_Verona.jpg", "Ponte_Pietra_Verona.jpg"]:
    if not os.path.exists(f"{PUB}/{f}"):
        run(f"cp {FONTE}/web/{f} {PUB}/{f}")

print("DUR", round(DUR, 3))
json.dump({"dur": DUR, "palavras": palavras}, open("base.json", "w"), ensure_ascii=False)
