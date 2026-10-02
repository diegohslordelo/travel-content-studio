"""Gera exports/legendas.srt com as legendas de tela, nos tempos do Reel (mesma fonte: project/timeline.json).

Rodar de dentro de reels/barcelona/:
    python3 project/scripts/legendas_srt.py
"""
import json

TL = json.load(open("project/timeline.json", encoding="utf-8"))
FPS = TL["fps"]


def ts(q):
    ms = round(q * 1000 / FPS)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    G = TL["legendas"]
    blocos = []
    for i, g in enumerate(G):
        ini = round((g["palavras"][0][1] + g["off"]) * FPS)
        if "sai" in g:
            fim = g["sai"] + 4
        else:
            p = G[i + 1]
            fim = round((p["palavras"][0][1] + p["off"]) * FPS)
        blocos.append((ini, fim, "\n".join(g["linhas"])))
    e = TL["eventos"]["emocional"]
    blocos.append((e["de"], e["saida_de"] + 4, f"{e['texto_leve']} {e['texto_forte']}"))
    fe = TL["eventos"]["fechamento"]
    blocos.append((fe["de"], TL["duracao_quadros"], fe["texto"]))
    with open("exports/legendas.srt", "w", encoding="utf-8") as f:
        for n, (a, b, t) in enumerate(blocos, 1):
            f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
    print(len(blocos), "legendas")


if __name__ == "__main__":
    main()
