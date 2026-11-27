#!/usr/bin/env python3
"""Decupagem da voz do Diego · REV7.

Roda de dentro de reels/golpes-europa/:  python3 rev7/decupar.py
Saída: rev7/edl.json (trechos de cada take, já sem pausas, e o tempo de cada palavra
na linha do tempo nova) para o montar.py.

Critério (pedido do Diego, 27/11/2026): decupagem bem apertada, "atropelando" as
palavras, sem comer palavra. As pausas são achadas pela energia do áudio (janela
de 10 ms) e cortadas até sobrar ~60 ms; nada é acelerado.
"""
import json
import subprocess

import numpy as np

SR = 48000
WIN = 0.010                 # janela da energia (s)
PAUSA_MIN = 0.100           # pausa menor que isso não é cortada (fechamento de consoante fica)
ANTES, DEPOIS = 0.015, 0.025  # margem mantida antes do ataque e depois da cauda (sobra ~40 ms de pausa)
D = "fonte/diego/"

# Ordem do vídeo. "cortar": trechos falados que saem (s, s), em pontos de silêncio
# medidos no perfil de energia (não no tempo do Whisper, que é impreciso).
TAKES = {
    "ganchoA": {"arq": "IMG_8818.MOV"},
    "ganchoB": {"arq": "IMG_8821.MOV"},
    # "vêm crescendo" sai: pela Eurostat, os furtos na UE caíram 2,0% em 2024.
    "dado": {"arq": "IMG_8822.MOV", "cortar": [(1.015, 2.48)]},
    "relevancia": {"arq": "IMG_8827.MOV"},
    # "três" sai (2,73–2,97 s; "mostrar" termina em 2,63 s): não há take da petição, são 2 golpes.
    "abertura": {"arq": "IMG_8828.MOV", "cortar": [(2.66, 3.03)]},
    "golpe1": {"arq": "IMG_8832.MOV"},
    # "o terceiro é" sai pelo mesmo motivo: fica "E o clássico, que é o das fantasias..."
    "golpe3": {"arq": "IMG_8852.MOV", "cortar": [(0.80, 1.24)]},
    "fim": {"arq": "IMG_8872.mov"},
}
ORDEM_CORPO = ["dado", "relevancia", "abertura", "golpe1", "golpe3", "fim"]


def audio(arq):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", D + arq, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32)


def energia_db(x):
    n = int(WIN * SR)
    m = len(x) // n
    rms = np.sqrt(np.mean(x[: m * n].reshape(m, n) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(rms)


def falas(db):
    """Regiões com fala (em s), pela energia com limiar adaptado ao take."""
    alto = np.percentile(db, 95)
    lim = alto - 26.0
    voz = db > lim
    regs, i = [], 0
    while i < len(voz):
        if voz[i]:
            j = i
            while j < len(voz) and voz[j]:
                j += 1
            regs.append([float(i * WIN), float(j * WIN)])
            i = j
        else:
            i += 1
    # junta regiões separadas por menos que PAUSA_MIN e descarta estalos < 40 ms
    out = []
    for r in regs:
        if out and r[0] - out[-1][1] < PAUSA_MIN:
            out[-1][1] = r[1]
        else:
            out.append(r)
    return [r for r in out if r[1] - r[0] >= 0.04], lim


def vale(db, t, raio=0.08):
    """Ponto de menor energia a até `raio` s de t."""
    a, b = max(0, int((t - raio) / WIN)), min(len(db) - 1, int((t + raio) / WIN))
    return float((a + int(np.argmin(db[a:b + 1]))) * WIN)


def decupar(nome, cfg, palavras):
    x = audio(cfg["arq"])
    dur = len(x) / SR
    db = energia_db(x)
    regs, lim = falas(db)
    trechos = [[max(0.0, s - ANTES), min(dur, e + DEPOIS)] for s, e in regs]
    for c0, c1 in cfg.get("cortar", []):
        a, b = c0, c1
        novo = []
        for s, e in trechos:
            if e <= a or s >= b:
                novo.append([s, e])
            else:
                if s < a:
                    novo.append([s, a])
                if e > b:
                    novo.append([b, e])
        trechos = novo
    trechos = [t for t in trechos if t[1] - t[0] >= 0.05]
    # palavras do Whisper mapeadas para a linha do tempo nova (só as que caem num trecho)
    mapa, t_novo = [], 0.0
    for s, e in trechos:
        for w in palavras:
            meio = (w["s"] + w["e"]) / 2
            if s <= meio < e:
                mapa.append({"w": w["w"], "s": round(t_novo + max(w["s"], s) - s, 3),
                             "e": round(t_novo + min(w["e"], e) - s, 3)})
        t_novo += e - s
    return {"arq": cfg["arq"], "trechos": [[round(s, 3), round(e, 3)] for s, e in trechos],
            "dur": round(t_novo, 3), "original": round(dur, 2), "palavras": mapa, "limiar_db": round(float(lim), 1)}


def main():
    tr = json.load(open("rev7/transcricao.json"))
    edl = {n: decupar(n, c, tr[c["arq"]]) for n, c in TAKES.items()}
    json.dump({"ordem_corpo": ORDEM_CORPO, "takes": edl}, open("rev7/edl.json", "w"), ensure_ascii=False, indent=1)
    for n, t in edl.items():
        print(f"{n:<11} {t['original']:5.2f} s -> {t['dur']:5.2f} s  ({len(t['trechos'])} trechos)  "
              + " ".join(w["w"] for w in t["palavras"]))


if __name__ == "__main__":
    main()
