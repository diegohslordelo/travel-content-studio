#!/usr/bin/env python3
"""Decupagem da voz do Diego · REV10.

REV10: NENHUMA palavra cortada (Diego, 27/11/2026: "não corte nenhum áudio meu, nenhuma
frase, nenhuma palavra"). Só sai o silêncio antes e depois de cada take e as pausas entre frases.

Roda de dentro de reels/golpes-europa/:  python3 rev10/decupar.py  ->  rev10/edl.json

Pedido do Diego (27/11/2026): decupagem dinâmica, mas cada frase com início e fim, e
um mínimo de espaço entre um take e outro. Na REV7/8 o limiar único cortava a cauda
da última sílaba (ex.: o gancho) e deixava pedaços de 0,15 s (flash de imagem).

Critério da REV9 (histerese):
- a fala é DETECTADA com limiar alto (pico da fala do take - 26 dB);
- o início e o fim de cada trecho só fecham quando a energia cai ao nível do silêncio
  (o maior entre piso do quarto + 8 dB e pico - 40 dB): a sílaba final fica inteira;
- pausa >= 140 ms é cortada; sobra 120 ms entre frases e 200 ms em fim de frase
  (palavra com ponto antes da pausa, pela transcrição);
- início do take com 50 ms antes do ataque e 120 ms depois do fim da cauda (≈ 0,17 s entre takes);
- nenhum trecho com menos de 0,4 s (se ficar, a pausa vizinha não é cortada);
- nada é acelerado.
"""
import json
import subprocess

import numpy as np

SR = 48000
WIN = 0.010
D = "fonte/diego/"
PAUSA_MIN = 0.140
PAD_ANTES, PAD_DEPOIS = 0.040, 0.080          # entre frases: 120 ms no total
PAD_DEPOIS_PONTO = 0.160                      # fim de frase: 200 ms no total
INICIO_TAKE, FIM_TAKE = 0.050, 0.120
TRECHO_MIN = 0.40

TAKES = {
    "ganchoA": {"arq": "IMG_8818.MOV"},
    "ganchoB": {"arq": "IMG_8821.MOV"},
    "dado": {"arq": "IMG_8822.MOV"},          # frase inteira, sem corte
    "relevancia": {"arq": "IMG_8827.MOV"},
    "abertura": {"arq": "IMG_8828.MOV"},       # "três" volta: agora há o take da petição
    "golpe1": {"arq": "IMG_8832.MOV"},
    "golpe2": {"arq": "IMG_8840.MOV"},         # novo: petição
    "golpe3": {"arq": "IMG_8852.MOV"},         # "E o terceiro é o clássico" inteiro
    "fim": {"arq": "IMG_8872.mov"},
}
ORDEM_CORPO = ["dado", "relevancia", "abertura", "golpe1", "golpe2", "golpe3", "fim"]


def audio(arq):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", D + arq, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32)


def energia_db(x):
    n = int(WIN * SR)
    m = len(x) // n
    return 20 * np.log10(np.sqrt(np.mean(x[: m * n].reshape(m, n) ** 2, axis=1) + 1e-12))


def regioes(db):
    alto, piso = np.percentile(db, 95), np.percentile(db, 10)
    hi, lo = alto - 26.0, max(piso + 8.0, alto - 40.0)
    nucleo = db > hi
    regs, i = [], 0
    while i < len(db):
        if nucleo[i]:
            a = i
            while a > 0 and db[a - 1] > lo:          # recua até o silêncio
                a -= 1
            b = i
            while b < len(db) and (nucleo[b] or db[b] > lo):   # avança até o silêncio
                b += 1
            regs.append([a * WIN, b * WIN])
            i = b
        else:
            i += 1
    out = []
    for r in regs:
        if out and r[0] - out[-1][1] < PAUSA_MIN:
            out[-1][1] = r[1]
        else:
            out.append(r)
    return [r for r in out if r[1] - r[0] >= 0.05], float(hi), float(lo)


def fim_de_frase(t, palavras):
    """A palavra que termina mais perto de t (antes) tem pontuação final?"""
    antes = [w for w in palavras if w["e"] <= t + 0.25]
    return bool(antes) and antes[-1]["w"][-1:] in ".!?"


def decupar(cfg, palavras):
    x = audio(cfg["arq"])
    dur = len(x) / SR
    db = energia_db(x)
    regs, hi, lo = regioes(db)
    # pausas entre regiões: decide o que cortar
    trechos = [[max(0.0, regs[0][0] - INICIO_TAKE), None]]
    for (s0, e0), (s1, e1) in zip(regs, regs[1:]):
        pd = PAD_DEPOIS_PONTO if fim_de_frase(e0, palavras) else PAD_DEPOIS
        trechos[-1][1] = e0 + pd
        trechos.append([s1 - PAD_ANTES, None])
    trechos[-1][1] = min(dur, regs[-1][1] + FIM_TAKE)
    # sem trecho curto: junta com o vizinho (a pausa entre eles fica)
    i = 0
    while i < len(trechos):
        if trechos[i][1] - trechos[i][0] < TRECHO_MIN and len(trechos) > 1:
            j = i - 1 if i > 0 else i + 1
            a, b = sorted((i, j))
            trechos[a] = [trechos[a][0], trechos[b][1]]
            del trechos[b]
            i = 0
        else:
            i += 1
    # cortes de palavra (pontos de silêncio medidos)
    for c0, c1 in cfg.get("cortar", []):
        novo = []
        for s, e in trechos:
            if e <= c0 or s >= c1:
                novo.append([s, e])
            else:
                if s < c0:
                    novo.append([s, c0])
                if e > c1:
                    novo.append([c1, e])
        trechos = novo
    trechos = [[round(s, 3), round(e, 3)] for s, e in trechos if e - s > 0.02]
    return {"arq": cfg["arq"], "trechos": trechos, "dur": round(sum(e - s for s, e in trechos), 3),
            "original": round(dur, 2), "limiar_db": [round(hi, 1), round(lo, 1)]}


def main():
    tr = json.load(open("rev10/transcricao.json"))
    edl = {n: decupar(c, tr[c["arq"]]) for n, c in TAKES.items()}
    json.dump({"ordem_corpo": ORDEM_CORPO, "takes": edl}, open("rev10/edl.json", "w"), ensure_ascii=False, indent=1)
    for n, t in edl.items():
        cur = min(e - s for s, e in t["trechos"])
        print(f"{n:<11} {t['original']:5.2f} -> {t['dur']:5.2f} s · {len(t['trechos'])} trechos "
              f"(menor {cur:.2f} s) · limiares {t['limiar_db']} · {t['trechos']}")


if __name__ == "__main__":
    main()
