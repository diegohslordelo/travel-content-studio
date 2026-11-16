"""REV1 · Comida: 3 formas de economizar · preparo (rodar de dentro de reels/comida-3-regras/rev1).

Gravação do Diego no Drive (Youtube/Reel/Custos, BAEAA0F8…mp4 → ../fonte/gravacao.mp4, 124,8 s, 16/11/2026).
Pedidos do Diego (16/11/2026):
- seguir estritamente a sequência da gravação; quando ele regravou a mesma fala, vale o último take
  ("Claro que não", moral e CTA);
- decupagem sem espaço entre as falas, sem cortar nenhuma palavra;
- nenhuma cor no vídeo dele (já vem tratado): só a conversão de formato HLG→SDR, a mesma da REV1 de Veneza,
  sem grade, sem LUT, sem contraste. O preto e branco entra só na pergunta da "terceira pessoa" (T7);
- acervo sem efeito nenhum (sem zoom, sem câmera lenta ou rápida): só a mesma conversão HLG→SDR.

Tempos das palavras: alinhamento forçado wav2vec2 + CTC (FORMATOS_REELS 7.2) sobre o texto conferido.
"""
import json
import os
import subprocess

import numpy as np

from alinhar import alinhar

FONTE = "../fonte"
PUB = "public"
FPS = 30
os.makedirs(f"{PUB}/fontes", exist_ok=True)
CONV = ("zscale=t=linear:npl=600,format=gbrpf32le,zscale=p=bt709,tonemap=clip:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
SRC = f"{FONTE}/gravacao.mp4"


def run(c):
    subprocess.run(c, shell=True, check=True)


# ---------------------------------------------------------------- takes
# Gravação contínua (o Diego levanta e senta entre as falas; não há corte de câmera). Cada take: janela em
# segundos que contém só aquela fala, e o texto. "palavra|falado" quando a legenda escreve diferente do que se
# fala (números). Escolhas "para"/"pra", "tá", "de sua" pelo alinhador (maior verossimilhança CTC).
TAKES = {
    "T1": (0.00, 5.60, "Você quer saber como economizar com a alimentação nas suas viagens e ainda assim conhecer "
                       "bons restaurantes?"),
    "T2": (9.00, 16.00, "Bora que eu vou te mostrar três formas que eu uso pra não gastar uma nota com comida "
                        "durante a viagem."),
    "T3": (16.50, 25.00, "A primeira coisa é economizar no café da manhã. Se não tá incluso no hotel, a gente passa "
                         "no supermercado e compra algumas coisas para comer no quarto mesmo."),
    "T4": (27.30, 33.50, "O que sobra para comprar na rua é só um menorzinho de toda manhã que não pode faltar, né?"),
    "T5": (35.80, 44.60, "Segunda, escolha uma refeição pra gastar um pouco mais no restaurante. Geralmente escolhemos "
                         "o jantar porque é mais no final do dia, a gente já fez tudo e pode comer com calma."),
    "T6": (45.30, 54.00, "Mas quem define? Seu|seu roteiro. Se tem algum restaurante que vale a pena ir na hora do "
                         "almoço por conta de uma vista ou experiência do lugar, aí você inverte."),
    "T7": (57.20, 61.50, "E nas outras refeições, rapaz, vai ficar sem comer?"),
    "T8": (65.62, 75.50, "Claro que não. Você vai comer alguma comida de rua, algum lanche rápido, algo mais simples "
                         "que vai te fazer gastar menos. E eu te garanto que isso vai fazer parte de sua experiência "
                         "conhecendo o local."),
    "T9": (78.60, 88.50, "Por exemplo, vamos supor que você vai para a Europa e quer gastar 50|cinquenta euros por dia "
                         "com comida. Então você vai usar esse valor pra balancear suas refeições de acordo com a dica "
                         "número 2.|dois"),
    "T10": (98.20, 103.50, "Economizar com comida não é comer mal, é você saber onde gastar e onde não gastar."),
    "T11": (117.30, 123.60, "Se você gostou das dicas, me segue aí para aprender a viajar melhor sem gastar dinheiro "
                            "à toa."),
}
# Takes regravados que ficaram de fora (o último take vale): "Claro que não." 64,64–65,52 s · moral 90,32–94,14 s
# ("…onde gastar e onde dá para economizar.") · CTA 108,28–112,62 s.
EDL = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11"]
PB = {"T7"}   # "E nas outras refeições, rapaz, vai ficar sem comer?" (a terceira pessoa falando com ele)

PAUSA_MAX = 0.30   # pausa maior que isso entre duas palavras do mesmo take é cortada
PRE, POS = 0.04, 0.05   # folga antes do início e depois do fim da fala (só para não cortar palavra)
FIM_VIDEO = 0.40   # depois de "à toa." (a placa do CTA precisa de tempo na tela)


def palavras_do_take(txt):
    out = []
    for tok in txt.split():
        if tok.startswith("|"):
            out.append({"w": "", "fala": tok[1:]})
        elif "|" in tok:
            w, f = tok.split("|")
            out.append({"w": w, "fala": f.replace("_", " ")})
        else:
            out.append({"w": tok, "fala": tok.replace("-", " ")})
    return out


# ---------------------------------------------------------------- áudio e energia
def wav16(src):
    raw = subprocess.run(f"ffmpeg -v error -i {src} -vn -ac 1 -ar 16000 -f s16le -", shell=True, check=True,
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def energia(src):
    raw = subprocess.run(f'ffmpeg -v error -i {src} -af "highpass=f=80,lowpass=f=6000" -ac 1 -ar 16000 -f s16le -',
                         shell=True, check=True, capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(x) // 160
    return 20 * np.log10(np.sqrt((x[: n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)


AUD = wav16(SRC)
DB = energia(SRC)
LIM = max(np.percentile(DB, 10) + 8, -62)   # "fim da fala": 8 dB acima do ruído da sala


def onset(t, t_min):
    """Início real da fala: volta do início alinhado enquanto houver voz (até 0,20 s)."""
    i = int(t * 100)
    lim_i = max(int(t_min * 100), int((t - 0.20) * 100))
    while i - 1 >= lim_i and (DB[max(lim_i, i - 3):i] > LIM).any():
        i -= 1
    while i < int(t * 100) and DB[i] <= LIM:
        i += 1
    return i / 100


def offset(t, t_max):
    """Fim real da fala: avança do fim alinhado enquanto houver voz (até 0,35 s); só termina depois de 50 ms de silêncio."""
    i = int(t * 100)
    lim_i = min(int(t_max * 100), int((t + 0.35) * 100), len(DB))
    while i < lim_i and (DB[i:min(lim_i, i + 5)] > LIM).any():
        i += 1
    while i > int(t * 100) and DB[i - 1] <= LIM:
        i -= 1
    return i / 100


# ---------------------------------------------------------------- alinhamento
cache = "alinhamento.json"
AL = json.load(open(cache)) if os.path.exists(cache) else {}
for tid, (a, b, txt) in TAKES.items():
    pal = palavras_do_take(txt)
    chave = f"{tid}:{a}:{b}:{txt}"
    if AL.get(tid, {}).get("chave") != chave:
        falado = [p for w in pal for p in w["fala"].split()]
        r = alinhar(AUD[int(a * 16000):int(b * 16000)], falado)
        k, res = 0, []
        for w in pal:
            n = len(w["fala"].split())
            res.append({"w": w["w"], "s": round(r[k][1] + a, 3), "e": round(r[k + n - 1][2] + a, 3)})
            k += n
        AL[tid] = {"chave": chave, "palavras": res}
        json.dump(AL, open(cache, "w"), ensure_ascii=False, indent=0)
        print("alinhado", tid)

# ---------------------------------------------------------------- trechos (decupagem)
trechos = []
for tid in EDL:
    P = AL[tid]["palavras"]
    grupo = [0]
    for i in range(1, len(P)):
        fim_ant = offset(P[i - 1]["e"], P[i]["s"])
        ini = onset(P[i]["s"], fim_ant)
        if ini - fim_ant > PAUSA_MAX:
            trechos.append((tid, grupo))
            grupo = []
        grupo.append(i)
    trechos.append((tid, grupo))

cortes = []
for tid, grupo in trechos:
    a, b = TAKES[tid][0], TAKES[tid][1]
    P = AL[tid]["palavras"]
    p0, p1 = P[grupo[0]], P[grupo[-1]]
    t_in = max(a, onset(p0["s"], a) - PRE)
    fim_extra = FIM_VIDEO if (tid == EDL[-1] and grupo[-1] == len(P) - 1) else POS
    t_out = min(b, offset(p1["e"], b) + fim_extra)
    f_in = int(np.floor(t_in * FPS + 1e-6))
    f_out = int(np.ceil(t_out * FPS - 1e-6))
    cortes.append({"take": tid, "q_in": f_in, "q_out": f_out, "palavras": grupo, "pb": tid in PB})
for x, y in zip(cortes, cortes[1:]):
    assert y["q_in"] >= x["q_out"] or x["take"] != y["take"], ("trechos sobrepostos", x, y)

# ---------------------------------------------------------------- vídeo (sem nenhum filtro além do HLG→SDR)
if not os.path.exists("sdr_A.mp4"):
    run(f'ffmpeg -v error -y -i {SRC} -vf "scale=1080:1920,{CONV}" -an -c:v libx264 -crf 14 -preset fast -r 30 '
        f'-colorspace bt709 -color_primaries bt709 -color_trc bt709 sdr_A.mp4')
partes_v, partes_a = [], []
for i, c in enumerate(cortes):
    run(f'ffmpeg -v error -y -i sdr_A.mp4 -vf "trim=start_frame={c["q_in"]}:end_frame={c["q_out"]},setpts=PTS-STARTPTS" '
        f'-an -c:v libx264 -crf 14 -preset fast -r 30 seg{i:02d}.mp4')
    partes_v.append(f"seg{i:02d}.mp4")
open("v.txt", "w").write("".join(f"file {p}\n" for p in partes_v))
run(f"ffmpeg -v error -y -f concat -safe 0 -i v.txt -c copy {PUB}/diego.mp4")

# ---------------------------------------------------------------- voz (passa-alta 70 Hz + loudness, como em Veneza)
if not os.path.exists("full_A.wav"):
    run(f"ffmpeg -v error -y -i {SRC} -vn -ac 2 -ar 48000 -c:a pcm_s24le full_A.wav")
for i, c in enumerate(cortes):
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    run(f'ffmpeg -v error -y -i full_A.wav -af "atrim={a:.6f}:{b:.6f},asetpts=PTS-STARTPTS,'
        f'afade=t=in:d=0.008,afade=t=out:st={b - a - 0.008:.4f}:d=0.008" -c:a pcm_s24le aseg{i:02d}.wav')
    partes_a.append(f"aseg{i:02d}.wav")
open("a.txt", "w").write("".join(f"file {p}\n" for p in partes_a))
run("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy voz_bruta.wav")
run(f"ffmpeg -v error -y -i voz_bruta.wav -af highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 {PUB}/voz.wav")

# ---------------------------------------------------------------- palavras na linha do tempo final
palavras, acc = [], 0
for c in cortes:
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    c["ini"], c["fim"] = round(acc, 4), round(acc + b - a, 4)
    P = AL[c["take"]]["palavras"]
    for i in c["palavras"]:
        w = P[i]
        ant_e = P[i - 1]["e"] if i > 0 else a
        prox_s = P[i + 1]["s"] if i + 1 < len(P) else b
        janela = DB[int(max(a, ant_e) * 100):int(w["s"] * 100)]
        if len(janela) and (janela <= LIM).any():
            s_real = max(a, ant_e, onset(w["s"], max(a, ant_e)))
        else:
            s_real = max(a, w["s"])
        e_real = min(b, prox_s, offset(w["e"], min(b, prox_s)))
        if not w["w"]:
            continue
        palavras.append({"w": w["w"], "s": round(acc + s_real - a, 3), "e": round(acc + max(e_real, s_real + 0.08) - a, 3),
                         "take": c["take"]})
    acc += b - a
DUR = round(acc, 4)

rosto = json.load(open("rosto_A.json"))
for c in cortes:
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    r = [x for x in rosto if a - 0.05 <= x[0] <= b + 0.05 and x[1] is not None and 250 < x[4] < 760]
    c["rosto"] = {"topo": min(x[2] for x in r), "queixo": max(x[2] + x[4] for x in r), "n": len(r)} if r else None

json.dump({"dur": DUR, "palavras": palavras, "cortes": cortes}, open("base.json", "w"), ensure_ascii=False, indent=0)

# ---------------------------------------------------------------- apoio (acervo do Diego)
# Mudos, só a conversão HLG→SDR (sem grade de cor, sem zoom, sem mudar a velocidade: pedido do Diego).
# Conferidos quadro a quadro: sem tremor e sem o rosto dele nem da Marina nos trechos usados.
CLIPES = {  # nome: (arquivo, início, duração)
    "prato_bouillon": ("IMG_3078", 0.0, 4.04),     # bife com fritas, Le Petit Bouillon Pharamond, Paris, 17/03/2026 16:24 (moral)
    "supermercado": ("IMG_1842", 0.0, 4.00),       # Albert Heijn, Amsterdam, 13/03/2026 20:03 (Marina de costas com a cestinha)
    "pharamond_salao": ("IMG_3071", 0.0, 3.99),    # salão do Pharamond (mesmo almoço)
    "prato_bouillon2": ("IMG_3075", 0.0, 3.62),    # o mesmo prato, de lado (gancho: mostra o prato inteiro)
    "waffle_bruges": ("IMG_2431", 0.0, 4.17),      # waffle no balcão, Bruges, 16/03/2026 11:27
    "feira_fila": ("IMG_1609", 0.0, 4.92),         # barraca de comida de rua (stroopwafel), Amsterdam, 13/03/2026 12:26
}
for nome, (arq, ini, d) in CLIPES.items():
    out = f"{PUB}/{nome}.mp4"
    if not os.path.exists(out):
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i {FONTE}/acervo/{arq}.MOV -an -vf "{CONV},scale=1080:-2" '
            f'-c:v libx264 -crf 17 -preset fast {out}')
# foto do Diego (enviada no chat em 16/11/2026): café na rua em Florença, copo da Eataly. Sem filtro.
run(f"ffmpeg -v error -y -i {FONTE}/fotos/IMG_5826.jpeg -q:v 2 {PUB}/cafe_eataly.jpg")
NM = "../../../design-system/remotion/node_modules/@fontsource"
for f in ["anton/files/anton-latin-400-normal.woff2", "inter/files/inter-latin-800-normal.woff2", "inter/files/inter-latin-600-normal.woff2"]:
    run(f"cp {NM}/{f} {PUB}/fontes/")
print("DUR", DUR, "· trechos", len(cortes), "· palavras", len(palavras))
for c in cortes:
    print(f'{c["take"]:4s} q{c["q_in"]:5d}-{c["q_out"]:5d}  final {c["ini"]:6.2f}-{c["fim"]:6.2f} {"P&B" if c["pb"] else ""}')
