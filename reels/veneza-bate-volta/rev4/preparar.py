"""REV4 · Veneza bate-volta · preparo (rodar de dentro de reels/veneza-bate-volta/rev4).

Pedidos do Diego (13/11/2026), gravações novas no Drive (Itália/Veneza, 1CC52CD5…mp4 → fonte/novas.mp4):
- troca e acrescenta takes (lista EDL abaixo, na ordem do vídeo);
- decupagem sem espaço entre as falas: só uma folga mínima para não cortar palavra;
- NADA de filtro ou cor no vídeo dele. A gravação é HDR (HLG): passa só pela conversão HLG→SDR padrão
  (a mesma da REV1, comparada à prévia do Drive), sem grade, sem LUT, sem contraste.
  O preto e branco só entra nos 3 takes que ele pediu, e vem da composição (grayscale puro).

Tempos das palavras: alinhamento forçado wav2vec2 + CTC (FORMATOS_REELS 7.2) sobre o texto conferido.
O Whisper marcava o início das palavras até 0,4 s antes da voz (era o que fazia legenda aparecer antes da hora).
Cada emenda: início/fim medidos pela energia da voz em torno da palavra alinhada, folga de 30–50 ms.
"""
import json
import os
import subprocess
import wave

import numpy as np

from alinhar import alinhar

FONTE = "../fonte"
PUB = "public"
FPS = 30
os.makedirs(f"{PUB}/fontes", exist_ok=True)
CONV = ("zscale=t=linear:npl=600,format=gbrpf32le,zscale=p=bt709,tonemap=clip:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
FONTES = {"A": f"{FONTE}/gravacao.mp4", "B": f"{FONTE}/novas.mp4"}


def run(c):
    subprocess.run(c, shell=True, check=True)


# ---------------------------------------------------------------- takes
# Cortes do próprio Diego nas gravações (1º quadro do take novo), medidos pela diferença entre quadros:
# A (gravacao.mp4, 63,27 s): 174 432 642 851 908 1082 1150 1444 1484 1773
# B (novas.mp4, 47,17 s):    139 316 614 910 1117
# Cada take: (id, fonte, quadro inicial, quadro final, texto exibido). "palavra|falado" quando a legenda
# escreve diferente do que se fala (números); "|a" = palavra falada que não vai para a legenda.
TAKES = {
    "A1": ("A", 0, 174, "Veneza não te quer lá e dessa vez é de verdade. Em partes."),
    "A2": ("A", 174, 432, "Veneza recebe quase 30|trinta milhões de pessoas no ano, sendo que três em cada quatro desses "
                          "visitantes vão de bate-volta.|bate_volta Por isso a cidade criou um pedágio pra quem vai e não dorme."),
    "A3": ("A", 432, 642, "São cinco euros pros programados, são dez euros pra quem paga na hora, e se você não pagar, "
                          "multa pra doer no bolso, pai."),
    "B1": ("B", 0, 139, "Ou seja, |a Veneza quer que você fique na cidade. E eu fiquei por duas noites."),
    "A5": ("A", 851, 908, "Não|não gostei.|gostei Não faça isso."),
    "B2": ("B", 139, 316, "Não me leve a mal. Veneza de dia é o cenário de filme que você sempre sonhou. "
                          "Mas à noite eu acho a cidade deserta."),
    "A7": ("A", 1082, 1150, "Sim, Diego, eu vou fazer o quê? Vou pagar a taxa?"),
    "A8": ("A", 1150, 1444, "Exatamente. Você vai incluir Verona no seu roteiro da Itália, uma cidade que fica só uma hora "
                            "e pouquinho de Veneza, e um dia você faz um bate-volta|bate_volta pra lá e no outro você conhece "
                            "a cidade do Romeu e Julieta."),
    "A9": ("A", 1444, 1484, "E no bolso?"),
    "B3": ("B", 316, 614, "Aí que tá o macete. Quem dorme em Veneza já paga a taxa no valor da hospedagem. Então ficar em "
                          "Verona pode ser até 25%|vinte_e_cinco_por_cento mais barato do que dormir na cidade dos canais."),
    "B4": ("B", 614, 910, "E reservar o pedágio quatro dias de antecedência, você paga só cinco euros. "
                          "Eu vou deixar o link na legenda."),
    "B5": ("B", 910, 1117, "Ah, Diego, mas eu quero dormir na cidade."),
    "B6": ("B", 1117, 1415, "Durma e tire suas próprias conclusões. Aí que tá a magia da viagem. "
                            "Cada experiência toca a pessoa de uma maneira diferente."),
    "A11": ("A", 1773, 1898, "E se você gostou, já me segue aí, porque eu dou dicas de viagem toda semana por aqui."),
}
# ordem do vídeo (pedido do Diego) e preto e branco (só onde ele pediu)
EDL = ["A1", "A2", "A3", "B1", "A5", "B2", "A7", "A8", "A9", "B3", "B4", "B5", "B6", "A11"]
PB = {"A7", "A9", "B5"}
# pausa protegida: o Diego senta na cadeira entre "verdade." e "Em partes." (pedido da REV1)
PROTEGE = {("A1", "verdade.")}

PAUSA_MAX = 0.30   # pausa maior que isso entre duas palavras do mesmo take é cortada
PRE, POS = 0.04, 0.05   # folga antes do início e depois do fim da fala (só para não cortar palavra)
FIM_VIDEO = 0.30   # depois de "aqui."


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


AUD = {k: wav16(v) for k, v in FONTES.items()}
DB = {k: energia(v) for k, v in FONTES.items()}
# limiar do "fim da fala": 8 dB acima do ruído da sala de cada gravação (A −66, B −83 dBFS no p10)
LIM = {k: max(np.percentile(DB[k], 10) + 8, -62) for k in DB}


def onset(fonte, t, t_min):
    """Início real da fala: volta do início alinhado enquanto houver voz (até 0,20 s; o alinhador chegou a marcar
    um "Não" 0,15 s depois do "N"). Um vale de até 30 ms no meio não conta como silêncio."""
    db = DB[fonte]
    i = int(t * 100)
    lim_i = max(int(t_min * 100), int((t - 0.20) * 100))
    while i - 1 >= lim_i and (db[max(lim_i, i - 3):i] > LIM[fonte]).any():
        i -= 1
    while i < int(t * 100) and db[i] <= LIM[fonte]:  # não começa num quadro de silêncio
        i += 1
    return i / 100


def offset(fonte, t, t_max):
    """Fim real da fala: avança do fim alinhado enquanto houver voz (cauda fraca de "s", "o"…, até 0,35 s).
    Só termina depois de 50 ms seguidos de silêncio (um vale curto no fim do "isso" não é o fim)."""
    db = DB[fonte]
    i = int(t * 100)
    lim_i = min(int(t_max * 100), int((t + 0.35) * 100), len(db))
    while i < lim_i and (db[i:min(lim_i, i + 5)] > LIM[fonte]).any():
        i += 1
    while i > int(t * 100) and db[i - 1] <= LIM[fonte]:  # termina no último quadro com voz
        i -= 1
    return i / 100


# ---------------------------------------------------------------- alinhamento
cache = "alinhamento.json"
AL = json.load(open(cache)) if os.path.exists(cache) else {}
for tid, (f, q0, q1, txt) in TAKES.items():
    pal = palavras_do_take(txt)
    chave = f"{tid}:{q0}:{q1}:{txt}"
    if AL.get(tid, {}).get("chave") != chave:
        a, b = q0 / FPS, q1 / FPS
        falado = [p for w in pal for p in w["fala"].split()]
        r = alinhar(AUD[f][int(a * 16000):int(b * 16000)], falado)
        # volta para as palavras exibidas (uma exibida pode ter várias faladas: "25%" = "vinte e cinco por cento")
        k, res = 0, []
        for w in pal:
            n = len(w["fala"].split())
            res.append({"w": w["w"], "s": round(r[k][1] + a, 3), "e": round(r[k + n - 1][2] + a, 3)})
            k += n
        AL[tid] = {"chave": chave, "palavras": res}
        json.dump(AL, open(cache, "w"), ensure_ascii=False, indent=0)
        print("alinhado", tid)

# ---------------------------------------------------------------- trechos (decupagem)
trechos = []   # (take, fonte, t_in, t_out, [palavras])
for tid in EDL:
    f, q0, q1, _ = TAKES[tid]
    a, b = q0 / FPS, q1 / FPS
    P = AL[tid]["palavras"]
    grupo = [0]
    for i in range(1, len(P)):
        fim_ant = offset(f, P[i - 1]["e"], P[i]["s"])
        ini = onset(f, P[i]["s"], fim_ant)
        if ini - fim_ant > PAUSA_MAX and (tid, P[i - 1]["w"]) not in PROTEGE:
            trechos.append((tid, f, grupo))
            grupo = []
        grupo.append(i)
    trechos.append((tid, f, grupo))

cortes = []
for tid, f, grupo in trechos:
    q0, q1 = TAKES[tid][1], TAKES[tid][2]
    a, b = q0 / FPS, q1 / FPS
    P = AL[tid]["palavras"]
    p0, p1 = P[grupo[0]], P[grupo[-1]]
    t_in = max(a, onset(f, p0["s"], a) - PRE)
    fim_extra = FIM_VIDEO if (tid == EDL[-1] and grupo[-1] == len(P) - 1) else POS
    t_out = min(b, offset(f, p1["e"], b) + fim_extra)
    # quadros inteiros (imagem e voz cortadas juntas): entrada arredonda para trás, saída para frente
    f_in = max(q0, int(np.floor(t_in * FPS + 1e-6)))
    f_out = min(q1, int(np.ceil(t_out * FPS - 1e-6)))
    cortes.append({"take": tid, "fonte": f, "q_in": f_in, "q_out": f_out, "palavras": grupo, "pb": tid in PB})

# ---------------------------------------------------------------- vídeo (sem nenhum filtro além do HLG→SDR)
for k, src in FONTES.items():
    if not os.path.exists(f"sdr_{k}.mp4"):
        run(f'ffmpeg -v error -y -i {src} -vf "scale=1080:1920,{CONV}" -an -c:v libx264 -crf 14 -preset fast -r 30 '
            f'-colorspace bt709 -color_primaries bt709 -color_trc bt709 sdr_{k}.mp4')
partes_v, partes_a = [], []
for i, c in enumerate(cortes):
    run(f'ffmpeg -v error -y -i sdr_{c["fonte"]}.mp4 -vf "trim=start_frame={c["q_in"]}:end_frame={c["q_out"]},setpts=PTS-STARTPTS" '
        f'-an -c:v libx264 -crf 14 -preset fast -r 30 seg{i:02d}.mp4')
    partes_v.append(f"seg{i:02d}.mp4")
open("v.txt", "w").write("".join(f"file {p}\n" for p in partes_v))
run(f"ffmpeg -v error -y -f concat -safe 0 -i v.txt -c copy {PUB}/diego.mp4")

# ---------------------------------------------------------------- voz
# mesmo tratamento da voz aprovada na REV1 (passa-alta 70 Hz + loudness); antes, as duas gravações são
# igualadas em volume (a nova veio ≈ 4 dB mais baixa), medindo só a fala usada de cada uma.
for k, src in FONTES.items():
    if not os.path.exists(f"full_{k}.wav"):
        run(f"ffmpeg -v error -y -i {src} -vn -ac 2 -ar 48000 -c:a pcm_s24le full_{k}.wav")


def lufs(arq):
    r = subprocess.run(f"ffmpeg -hide_banner -nostats -i {arq} -af ebur128 -f null -", shell=True, capture_output=True, text=True).stderr
    return float(r.rsplit("I:", 1)[1].split("LUFS")[0])


ganho = {}
for k in FONTES:
    sel = [c for c in cortes if c["fonte"] == k]
    expr = "+".join(f"between(t,{c['q_in'] / FPS:.4f},{c['q_out'] / FPS:.4f})" for c in sel)
    run(f"ffmpeg -v error -y -i full_{k}.wav -af \"aselect='{expr}',asetpts=N/SR/TB\" medir_{k}.wav")
    ganho[k] = lufs(f"medir_{k}.wav")
ref = ganho["A"]
for i, c in enumerate(cortes):
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    g = ref - ganho[c["fonte"]]
    run(f'ffmpeg -v error -y -i full_{c["fonte"]}.wav -af "atrim={a:.6f}:{b:.6f},asetpts=PTS-STARTPTS,volume={g:.2f}dB,'
        f'afade=t=in:d=0.008,afade=t=out:st={b - a - 0.008:.4f}:d=0.008" -c:a pcm_s24le aseg{i:02d}.wav')
    partes_a.append(f"aseg{i:02d}.wav")
open("a.txt", "w").write("".join(f"file {p}\n" for p in partes_a))
run("ffmpeg -v error -y -f concat -safe 0 -i a.txt -c copy voz_bruta.wav")
run(f"ffmpeg -v error -y -i voz_bruta.wav -af highpass=f=70,loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 {PUB}/voz.wav")

# ---------------------------------------------------------------- palavras na linha do tempo final
palavras, acc, mapa = [], 0, []
for c in cortes:
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    c["ini"], c["fim"] = round(acc, 4), round(acc + b - a, 4)
    P = AL[c["take"]]["palavras"]
    for i in c["palavras"]:
        w = P[i]
        # cada palavra fica entre o fim alinhado da anterior e o início alinhado da seguinte: na fala contínua
        # vale o tempo do alinhador; depois de silêncio, o início real pela energia (nunca antes da voz)
        ant_e = P[i - 1]["e"] if i > 0 else a
        prox_s = P[i + 1]["s"] if i + 1 < len(P) else b
        janela = DB[c["fonte"]][int(max(a, ant_e) * 100):int(w["s"] * 100)]
        if len(janela) and (janela <= LIM[c["fonte"]]).any():   # houve silêncio antes: início real pela energia
            s_real = max(a, ant_e, onset(c["fonte"], w["s"], max(a, ant_e)))
        else:                                                    # fala contínua: tempo do alinhador
            s_real = max(a, w["s"])
        e_real = min(b, prox_s, offset(c["fonte"], w["e"], min(b, prox_s)))
        if not w["w"]:
            continue
        palavras.append({"w": w["w"], "s": round(acc + s_real - a, 3), "e": round(acc + max(e_real, s_real + 0.08) - a, 3),
                         "take": c["take"]})
    acc += b - a
DUR = round(acc, 4)

# rosto do Diego por trecho (detecção a cada 0,1 s nas gravações, rosto.py) → linha do tempo final
rosto = {k: json.load(open(f"rosto_{k}.json")) for k in FONTES}
for c in cortes:
    a, b = c["q_in"] / FPS, c["q_out"] / FPS
    r = [x for x in rosto[c["fonte"]] if a - 0.05 <= x[0] <= b + 0.05 and x[1] is not None and 250 < x[4] < 700]
    c["rosto"] = {"topo": min(x[2] for x in r), "queixo": max(x[2] + x[4] for x in r), "n": len(r)} if r else None

json.dump({"dur": DUR, "palavras": palavras, "cortes": cortes, "ganho_lufs": ganho}, open("base.json", "w"), ensure_ascii=False, indent=0)

# ---------------------------------------------------------------- apoio
# Clipes do acervo do Diego: mudos, só a conversão HLG→SDR (sem grade de cor, pedido do Diego), conferidos
# quadro a quadro sem o rosto dele nem da Marina.
CLIPES = {  # nome: (arquivo, início, duração)
    "ducale_lotado": ("IMG_6062", 6.0, 3.6),   # Palácio Ducal lotado (gancho)
    "praca_lotada": ("IMG_6063", 12.3, 3.2),   # Praça São Marcos cheia ("30 milhões")
    "por_do_sol": ("IMG_6098", 7.0, 3.5),      # Grande Canal no pôr do sol, 31/12/2024 15:50 ("cenário de filme")
    "noite_luzes": ("IMG_6128", 1.0, 3.4),     # Grande Canal à noite, barcos parados, ninguém ("deserta")
    "canais": ("IMG_6016", 3.0, 3.0),          # Grande Canal com gôndola ("cidade dos canais")
    "fogos": ("IMG_6156", 9.3, 4.4),           # fogos do Ano-Novo na laguna, 01/01/2025 00:11 ("magia da viagem")
}
for nome, (arq, ini, d) in CLIPES.items():
    out = f"{PUB}/{nome}.mp4"
    if not os.path.exists(out):
        run(f'ffmpeg -v error -y -ss {ini} -t {d} -i {FONTE}/acervo/{arq}.MOV -an -vf "{CONV},scale=1080:-2" '
            f'-c:v libx264 -crf 17 -preset fast -r 30 {out}')
# fotos (Wikimedia Commons) e prints de referência (Fortune; título do site oficial cda.ve.it)
IMAGENS = {
    "arena_verona.jpg": f"{FONTE}/web/Arena_di_Verona.jpg",
    "ponte_pietra.jpg": f"{FONTE}/web/Ponte_Pietra_Verona.jpg",
    "julieta_varanda.jpg": f"{FONTE}/web/Verona_-_Juliet_Balcony.jpg",
    "salute_noite.jpg": f"{FONTE}/web/Santa_Maria_della_Salute_from_Hotel_Monaco_nightview.jpg",
    "fortune_titulo.png": f"{FONTE}/web2/fortune_titulo.png",
    "fortune_paragrafo.png": f"{FONTE}/web2/fortune_paragrafo.png",
    "cda_cabecalho.png": f"{FONTE}/web2/cda_cabecalho.png",
}
for dst, src in IMAGENS.items():
    run(f"cp {src} {PUB}/{dst}")
NM = "../../../design-system/remotion/node_modules/@fontsource"
for f in ["anton/files/anton-latin-400-normal.woff2", "inter/files/inter-latin-800-normal.woff2", "inter/files/inter-latin-600-normal.woff2"]:
    run(f"cp {NM}/{f} {PUB}/fontes/")
print("DUR", DUR, "· trechos", len(cortes), "· palavras", len(palavras), "· LUFS da fala", ganho)
for c in cortes:
    print(f'{c["take"]:4s} {c["fonte"]} q{c["q_in"]:5d}-{c["q_out"]:5d}  final {c["ini"]:6.2f}-{c["fim"]:6.2f} {"P&B" if c["pb"] else ""}')
