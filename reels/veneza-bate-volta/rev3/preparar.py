"""REV3 · Veneza bate-volta · preparo (rodar de dentro de reels/veneza-bate-volta/rev3).

Parte da REV2 (CLAUDE.md, 12). Pedidos do Diego (13/11/2026): final mais enxuto; preto e branco em
"Sim, Diego… vou pagar a taxa?" e em "E no bolso?" (isso fica em cenas.py).

Decupagem do final (sem cortar fala, medido na energia da voz, faixa 80–6.000 Hz):
- corta 57,233–57,500 s: silêncio (< −62 dBFS) entre "legenda." e o "E" fraco de "E se você gostou".
  O corte termina no quadro 1725, que já é um corte da gravação do Diego: vira uma mudança só.
- termina o vídeo 0,25 s depois de "aqui." (antes: 0,34 s de silêncio + 0,13 s de imagem sem som).
"""
import json, os, shutil, subprocess

REV1, REV2 = "../rev1", "../rev2"
PUB = "public"
os.makedirs(PUB, exist_ok=True)
FPS = 30
CORTE = (1717 / FPS, 1725 / FPS)          # quadros inteiros: imagem e voz cortadas juntas
base2 = json.load(open(f"{REV2}/base.json"))
P2 = base2["palavras"]
FIM = round((P2[-1]["e"] + 0.25) * FPS) / FPS   # 0,25 s depois de "aqui."


def run(c):
    subprocess.run(c, shell=True, check=True)


# imagens, clipes e fontes da REV2
for f in os.listdir(f"{REV2}/public"):
    src = f"{REV2}/public/{f}"
    if f in ("diego.mp4", "voz.wav"):
        continue
    if os.path.isdir(src):
        shutil.copytree(src, f"{PUB}/{f}", dirs_exist_ok=True)
    elif not os.path.exists(f"{PUB}/{f}"):
        shutil.copy(src, f"{PUB}/{f}")

a, b = CORTE
# gravação: [0, a) + [b, FIM)
run(f'ffmpeg -v error -y -i {REV1}/public/diego.mp4 -filter_complex '
    f'"[0:v]trim=0:{a},setpts=PTS-STARTPTS[v0];[0:v]trim={b}:{FIM},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1[v]" '
    f'-map "[v]" -c:v libx264 -crf 15 -preset fast -r 30 {PUB}/diego.mp4')
# voz aprovada (REV1), mesmos cortes, fade de 10 ms nas emendas (em silêncio)
run(f'ffmpeg -v error -y -i {REV1}/public/voz.wav -filter_complex '
    f'"[0:a]atrim=0:{a},asetpts=PTS-STARTPTS,afade=t=out:st={a - 0.01:.4f}:d=0.01[a0];'
    f'[0:a]atrim={b}:{FIM},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={FIM - b - 0.06:.4f}:d=0.06[a1];[a0][a1]concat=n=2:v=0:a=1[a]" '
    f'-map "[a]" -c:a pcm_s16le -ar 48000 {PUB}/voz.wav')

# palavras: depois do corte, tudo anda 0,267 s para trás
d = b - a
P = []
for w in P2:
    w = dict(w)
    if w["s"] >= b - 0.06:
        w["s"], w["e"] = round(max(a + 0.04, w["s"] - d), 3), round(w["e"] - d, 3)  # o "E" fraco começa logo depois do corte
    P.append(w)
DUR = round(FIM - d, 3)
json.dump({"dur": DUR, "palavras": P, "corte_final": [round(a, 3), round(b, 3)]}, open("base.json", "w"), ensure_ascii=False)
print("DUR", DUR, "· corte", round(a, 3), "→", round(b, 3), f"({d:.3f} s) · fim antigo {base2['dur']}")
