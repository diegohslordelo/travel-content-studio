"""REV1 · Barcelona 3 dias · decupagem da narração (rodar de dentro de reels/barcelona-3-dias/rev1).

Narração do Diego: 9 gravações (Drive, Barcelona/…/Roteiro, "Praça Ernesto Lebram*.m4a", 17/11/2026),
baixadas para ../fonte/narracao/narr_1..9 (a sem número = 1). Cada gravação é uma frase do roteiro, na ordem.
IDs no Drive (download: https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t):
1 1wX-ShkW7JZ6nWqAVB-5DoxA6-XiR1-fx · 2 1D_fxXWdy0e56McPi6oPrEe2WT6WpJziW · 3 1sGI18MKslLuJ3vVz-mA6JcJWuW_AdHLd
4 13E6kXhVm-w1vr0yxO6h4LYWTunpyobH9 · 5 1r9V27pT9BPp5JdLiXPCnlFDG96FoF54R · 6 1M6UXCSZJNl3yja5co8p-6Io0__Rvnrzc
7 14ynorxcA7HzSQVnO32VlFe7k4VypXGzQ · 8 1KN5-1AloK40rlCbGtdWf2fdnvvW68T_6 · 9 16C9x210il_kwFE-A56j5cAqlqn7g8gAK

- Tempos das palavras: alinhamento forçado wav2vec2 PT + CTC (FORMATOS_REELS 7.2) sobre o texto conferido
  (Whisper large-v3 + leituras testadas contra o áudio, ver QA).
- Decupagem: início e fim de cada fala pela energia da voz em torno da palavra alinhada (folga de 40/60 ms);
  pausa maior que PAUSA_MAX dentro de uma gravação é cortada; entre gravações, ENTRE s de silêncio.
- Voz: passa-alta 70 Hz + loudness −14 LUFS (mesmo tratamento dos Reels narrados aprovados). Sem acelerar nada.
Saídas: public/voz.wav e voz.json (palavras na linha do tempo final, trechos e emendas).
"""
import json
import os
import subprocess

import numpy as np

from alinhar import alinhar

N = "../fonte/narracao"
PUB = "public"
os.makedirs(PUB, exist_ok=True)

# Texto exibido (legenda) por gravação. "exibido|falado" quando a legenda escreve diferente do que o alinhador
# precisa ouvir (número, nome estrangeiro). "_" no exibido = espaço dentro de um item ("La_Rambla").
TAKES = {
    1: "Barcelona acaba com os viajantes que não montam um roteiro com estratégia.",
    2: "Nós fomos passar 3|três dias em uma das cidades mais desejadas da Europa e foi assim que organizamos o nosso roteiro.",
    3: "Nosso primeiro dia em Barcelona, deixamos os pontos turísticos mais distantes. Começamos pelo Camp Nou, "
       "depois Montjuïc,|monjuique que infelizmente não teve o show das fontes da data que estávamos lá.",
    4: "Pausa pro Mequizão e depois partimos pra ver Colombo e a Barceloneta. Fechamos o dia com Parque da Cidadela "
       "e Arco do Triunfo.",
    5: "O dia 2|dois foi focado em história. Nos hospedamos no bairro Gràcia|grácia e logo ali já tinha a Casa "
       "Vicens,|vinces a primeira de Gaudí. Depois fomos pro bairro Gótico, passamos pelo Muro do Beijo, Ponte do "
       "Bispo, Catedral, Praça Real e até que chegamos na La_Rambla,|larambla que estava toda em obra.",
    6: "Lá mesmo fica o Mercado de La Boqueria, que passamos só pra ver, pra não doer no bolso, e depois partimos pra "
       "Passeig|passei de Gràcia,|grácia a rua das compras. A Casa Batlló|batlô e Milà,|milá famosas de Gaudí, ficam por "
       "lá, mas não entramos.",
    7: "Nosso terceiro dia foi exclusivamente reservado pro dono da cidade, Gaudí. Finalmente chegamos na Sagrada "
       "Família e passamos a manhã inteira lá. A energia desse lugar é inexplicável.",
    8: "Paramos para comer um bom churros e fomos passar a tarde no Parque Güell.|guel",
    9: "A energia de Barcelona é realmente diferente, os 3|três dias foram suficientes pra gente sentir isso. "
       "Salva esse roteiro se Barcelona tiver nos seus planos.",
}
PAUSA_MAX = 0.30   # pausa maior que isso entre duas palavras da mesma gravação é cortada
PRE, POS = 0.04, 0.06
ENTRE = 0.12       # silêncio acrescentado entre uma gravação e a seguinte (além das folgas)
FIM = 0.40         # depois de "planos." (a placa do CTA continua na tela)


def run(c):
    subprocess.run(c, shell=True, check=True)


def palavras_do_take(txt):
    out = []
    for tok in txt.split():
        if "|" in tok:
            w, f = tok.split("|")
        else:
            w, f = tok, tok
        out.append({"w": w.replace("_", " "), "fala": f.replace("_", " ")})
    return out


def wav16(src):
    raw = subprocess.run(f"ffmpeg -v error -i {src} -ac 1 -ar 16000 -f s16le -", shell=True, check=True,
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def energia(src):
    raw = subprocess.run(f'ffmpeg -v error -i {src} -af "highpass=f=80,lowpass=f=6000" -ac 1 -ar 16000 -f s16le -',
                         shell=True, check=True, capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(x) // 160
    return 20 * np.log10(np.sqrt((x[: n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)


SRC = {k: f"{N}/narr_{k}.wav" for k in TAKES}
DURS = {k: float(subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {v}", shell=True,
                                capture_output=True, text=True).stdout) for k, v in SRC.items()}
AUD = {k: wav16(v) for k, v in SRC.items()}
DB = {k: energia(v) for k, v in SRC.items()}
LIM = {k: max(np.percentile(DB[k], 10) + 10, -60) for k in DB}


def onset(k, t, t_min):
    db = DB[k]
    i = int(t * 100)
    lim_i = max(int(t_min * 100), int((t - 0.20) * 100))
    while i - 1 >= lim_i and (db[max(lim_i, i - 3):i] > LIM[k]).any():
        i -= 1
    while i < int(t * 100) and db[i] <= LIM[k]:
        i += 1
    return i / 100


def offset(k, t, t_max):
    db = DB[k]
    i = int(t * 100)
    lim_i = min(int(t_max * 100), int((t + 0.35) * 100), len(db))
    while i < lim_i and (db[i:min(lim_i, i + 5)] > LIM[k]).any():
        i += 1
    while i > int(t * 100) and db[i - 1] <= LIM[k]:
        i -= 1
    return i / 100


# ---------------------------------------------------------------- alinhamento (cache)
cache = "alinhamento.json"
AL = json.load(open(cache)) if os.path.exists(cache) else {}
for k, txt in TAKES.items():
    pal = palavras_do_take(txt)
    if AL.get(str(k), {}).get("txt") != txt:
        falado = [p for w in pal for p in w["fala"].split()]
        r = alinhar(AUD[k], falado)
        i, res = 0, []
        for w in pal:
            n = len(w["fala"].split())
            res.append({"w": w["w"], "s": round(r[i][1], 3), "e": round(r[i + n - 1][2], 3)})
            i += n
        AL[str(k)] = {"txt": txt, "palavras": res}
        json.dump(AL, open(cache, "w"), ensure_ascii=False, indent=0)
        print("alinhado", k)

# ---------------------------------------------------------------- trechos
trechos = []
for k in TAKES:
    P = AL[str(k)]["palavras"]
    grupo = [0]
    for i in range(1, len(P)):
        fim_ant = offset(k, P[i - 1]["e"], P[i]["s"])
        ini = onset(k, P[i]["s"], fim_ant)
        if ini - fim_ant > PAUSA_MAX:
            trechos.append((k, grupo))
            grupo = []
        grupo.append(i)
    trechos.append((k, grupo))

cortes = []
for n, (k, grupo) in enumerate(trechos):
    P = AL[str(k)]["palavras"]
    t_in = max(0.0, onset(k, P[grupo[0]]["s"], 0) - PRE)
    ultimo = n == len(trechos) - 1
    t_out = min(DURS[k], offset(k, P[grupo[-1]]["e"], DURS[k]) + (FIM if ultimo else POS))
    novo_take = n + 1 < len(trechos) and trechos[n + 1][0] != k
    cortes.append({"take": k, "a": round(t_in, 3), "b": round(t_out, 3), "palavras": grupo,
                   "silencio_depois": ENTRE if novo_take else 0.0})

# ---------------------------------------------------------------- áudio
partes = []
for i, c in enumerate(cortes):
    d = c["b"] - c["a"]
    run(f'ffmpeg -v error -y -i {SRC[c["take"]]} -af "atrim={c["a"]:.4f}:{c["b"]:.4f},asetpts=PTS-STARTPTS,'
        f'afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.4f}:d=0.008" -ar 48000 -ac 1 -c:a pcm_s24le aseg{i:02d}.wav')
    partes.append(f"aseg{i:02d}.wav")
    if c["silencio_depois"]:
        run(f"ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=mono -t {c['silencio_depois']} -c:a pcm_s24le sil{i:02d}.wav")
        partes.append(f"sil{i:02d}.wav")
open("a.txt", "w").write("".join(f"file {p}\n" for p in partes))
run("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy voz_bruta.wav")
run(f"ffmpeg -v error -y -i voz_bruta.wav -af highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -ac 1 {PUB}/voz.wav")

# ---------------------------------------------------------------- palavras na linha do tempo final
palavras, acc = [], 0.0
for c in cortes:
    k, a, b = c["take"], c["a"], c["b"]
    c["ini"] = round(acc, 4)
    P = AL[str(k)]["palavras"]
    for i in c["palavras"]:
        w = P[i]
        ant_e = P[i - 1]["e"] if i > 0 else a
        prox_s = P[i + 1]["s"] if i + 1 < len(P) else b
        janela = DB[k][int(max(a, ant_e) * 100):int(w["s"] * 100)]
        if len(janela) and (janela <= LIM[k]).any():
            s_real = max(a, ant_e, onset(k, w["s"], max(a, ant_e)))
        else:
            s_real = max(a, w["s"])
        e_real = min(b, prox_s, offset(k, w["e"], min(b, prox_s)))
        palavras.append({"w": w["w"], "s": round(acc + s_real - a, 3), "e": round(acc + max(e_real, s_real + 0.08) - a, 3),
                         "take": k})
    acc += b - a
    c["fim"] = round(acc, 4)
    acc += c["silencio_depois"]
DUR = round(acc, 4)
json.dump({"dur": DUR, "palavras": palavras, "cortes": cortes}, open("voz.json", "w"), ensure_ascii=False, indent=0)
print("DUR", DUR, "trechos", len(cortes), "palavras", len(palavras))
for c in cortes:
    P = AL[str(c["take"])]["palavras"]
    print(f'T{c["take"]} {c["a"]:6.2f}-{c["b"]:6.2f} → {c["ini"]:6.2f}-{c["fim"]:6.2f} | {" ".join(P[i]["w"] for i in c["palavras"])}')
