"""Re-segmenta a transcrição em legendas legíveis a partir das marcas de tempo por palavra.

1. Agrupa palavras em frases (pausa > 0,7 s ou pontuação final).
2. Divide frases com mais de 80 caracteres ou 6 s em partes equilibradas, preferindo vírgulas.
3. Garante duração mínima de 0,8 s por legenda, sem invadir a seguinte.

Uso: python3 resegmentar_srt.py transcricao_palavras.tsv transcricao.srt
"""
import csv
import sys

MAX_CAR, MAX_DUR, MIN_DUR, PAUSA = 80, 6.0, 0.8, 0.7


def carimbo(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def texto(ws):
    return " ".join(w for _, _, w in ws)


def dividir(ws):
    if len(ws) < 2 or (len(texto(ws)) <= MAX_CAR and ws[-1][1] - ws[0][0] <= MAX_DUR):
        return [ws]
    melhor, k_melhor = None, 1
    for k in range(1, len(ws)):
        esq, dir_ = texto(ws[:k]), texto(ws[k:])
        custo = abs(len(esq) - len(dir_))
        if esq[-1] in ",;:":
            custo -= 25
        if ws[k][0] - ws[k - 1][1] > 0.3:  # respiro entre palavras
            custo -= 15
        if melhor is None or custo < melhor:
            melhor, k_melhor = custo, k
    return dividir(ws[:k_melhor]) + dividir(ws[k_melhor:])


def main():
    palavras = []
    with open(sys.argv[1], encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["palavra"]:
                palavras.append((float(r["inicio"]), float(r["fim"]), r["palavra"]))
    frases, atual = [], []
    for w in palavras:
        if atual and w[0] - atual[-1][1] > PAUSA:
            frases.append(atual)
            atual = []
        atual.append(w)
        if w[2][-1] in ".?!":
            frases.append(atual)
            atual = []
    if atual:
        frases.append(atual)
    cues = [(p[0][0], p[-1][1], texto(p)) for f in frases for p in dividir(f)]
    saida = []
    for i, (a, z, t) in enumerate(cues):
        limite = cues[i + 1][0] - 0.05 if i + 1 < len(cues) else z + MIN_DUR
        z = max(z, min(a + MIN_DUR, limite))
        saida.append((a, z, t))
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        for n, (a, z, t) in enumerate(saida, 1):
            f.write(f"{n}\n{carimbo(a)} --> {carimbo(z)}\n{t}\n\n")
    print(f"{len(palavras)} palavras -> {len(saida)} legendas")


if __name__ == "__main__":
    main()
