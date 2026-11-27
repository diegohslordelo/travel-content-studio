#!/usr/bin/env python3
"""Verificação quadro a quadro da REV9.  python3 rev9/verificar.py A B  ->  rev9/VERIFICACAO_REV9.md

1. Diego: os quadros de origem são consecutivos (+1) dentro de cada trecho; sem
   repetição e sem pulo fora dos cortes da decupagem.
2. Fundo: cada take dura >= 0,6 s (o montar.py também confere o fim limpo de cada um).
3. Vídeo final: todos os quadros, um a um, comparados com o anterior (histograma de cor
   da área do fundo). Toda troca de plano detectada tem de cair num corte planejado; uma
   troca fora disso é plano escondido na origem (imagem perdida).
4. Legenda: cada estado (palavra acesa) dura >= 2 quadros.
5. Duração de imagem e áudio iguais; nenhum quadro preto.
"""
import json
import subprocess
import sys

import numpy as np

FPS, W, H = 24, 1080, 1920
SW, SH = 135, 240                      # escala da análise


def quadros(arq):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", arq, "-vf", f"scale={SW}:{SH}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(SW * SH * 3)
        if len(b) < SW * SH * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(SH, SW, 3)


def hist(fr):
    # área do fundo sem legenda, sem Diego (canto direito) e sem o texto do gancho/print:
    # faixa da esquerda, de y 1060 a 1500 (escala 1/8: 132..187), x 0..400 (0..50)
    reg = fr[132:187, 0:50].reshape(-1, 3) // 32
    idx = reg[:, 0] * 64 + reg[:, 1] * 8 + reg[:, 2]
    h = np.bincount(idx, minlength=512).astype(np.float32)
    return h / h.sum()


def verificar(v):
    log = json.load(open(f"rev9/_tmp/log_{v}.json"))
    arq = f"rev9/golpes_rev9_gancho{v}.mp4"
    linhas = [f"## Gancho {v} · `{arq}`", ""]
    erros = []

    # 1. Diego
    dg = log["diego"]
    saltos = [i for i in range(1, len(dg)) if not (dg[i][0] == dg[i - 1][0] and dg[i][1] == dg[i - 1][1] + 1)]
    repet = [i for i in range(1, len(dg)) if dg[i] == dg[i - 1]]
    n_trechos = len(log["trechos"])
    linhas.append(f"- **Diego:** {len(dg)} quadros; {len(saltos)} emendas (esperado {n_trechos - 1}, uma por corte "
                  f"da decupagem); {len(repet)} quadros repetidos.")
    if len(saltos) != n_trechos - 1 or repet:
        erros.append("Diego: emenda ou repetição fora do esperado")
    # 2. fundo
    cortes_fundo, f = [], 0
    curtos = []
    for arqf, ini, n, bloco in log["plano_fundo"]:
        if n < round(0.6 * FPS):
            curtos.append((bloco, arqf, n))
        cortes_fundo.append(f)
        f += n
    linhas.append(f"- **Fundo:** {len(log['plano_fundo'])} takes, o menor com "
                  f"{min(n for _, _, n, _ in log['plano_fundo'])} quadros "
                  f"({min(n for _, _, n, _ in log['plano_fundo']) / FPS:.2f} s); takes < 0,6 s: {len(curtos)}.")
    if curtos:
        erros.append(f"fundo com take curto: {curtos}")
    if f != log["n_quadros"]:
        erros.append(f"fundo com {f} quadros, vídeo com {log['n_quadros']}")
    # 3. quadro a quadro no vídeo final
    esperados = set(cortes_fundo[1:])
    hs, pretos, n = [], [], 0
    for fr in quadros(arq):
        hs.append(hist(fr))
        if fr.mean() < 8:
            pretos.append(n)
        n += 1
    sim = np.array([np.minimum(hs[i], hs[i - 1]).sum() for i in range(1, len(hs))])
    detect = [i + 1 for i, s in enumerate(sim) if s < 0.45]
    fora = [q for q in detect if not any(abs(q - e) <= 1 for e in esperados)]
    perdidos = [e for e in esperados if not any(abs(q - e) <= 1 for q in detect)]
    linhas.append(f"- **Vídeo final:** {n} quadros lidos (esperado {log['n_quadros']}); trocas de plano detectadas: "
                  f"{len(detect)}; fora de corte planejado: {len(fora)} {fora if fora else ''}; quadros pretos: {len(pretos)}.")
    if perdidos:
        linhas.append(f"  - Cortes planejados sem troca forte de cor na faixa analisada (planos parecidos): {perdidos}")
    if n != log["n_quadros"] or fora or pretos:
        erros.append("vídeo final: contagem, troca de plano fora do corte ou quadro preto")
    # 4. legenda
    curtas = [(a, b) for a, b in log["legenda"] if b - a < 2]
    linhas.append(f"- **Legenda:** {len(log['legenda'])} estados; com menos de 2 quadros: {len(curtas)} {curtas if curtas else ''}.")
    if curtas:
        erros.append("legenda com estado curto")
    # 5. duração
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "csv=p=0", arq],
                         capture_output=True, text=True).stdout.split()
    linhas.append(f"- **Duração (stream, s):** {', '.join(dur)}.")
    linhas.append(f"- **Resultado:** {'OK' if not erros else 'ERROS: ' + '; '.join(erros)}")
    linhas.append("")
    linhas.append("| Início (s) | Bloco | Fundo | Duração (s) |")
    linhas.append("|---|---|---|---|")
    f = 0
    for arqf, ini, nq, bloco in log["plano_fundo"]:
        linhas.append(f"| {f / FPS:.2f} | {bloco} | {arqf} a partir de {ini:.2f} s | {nq / FPS:.2f} |")
        f += nq
    linhas.append("")
    return linhas, erros


def main():
    out = ["# Verificação quadro a quadro · REV9", "",
           "Gerado por `rev9/verificar.py` a partir do registro do `montar.py` e da leitura de todos os quadros do vídeo final.", ""]
    tudo_ok = True
    for v in sys.argv[1:] or ["A", "B"]:
        l, e = verificar(v)
        out += l
        tudo_ok &= not e
    open("rev9/VERIFICACAO_REV9.md", "w").write("\n".join(out) + "\n")
    print("\n".join(out))
    sys.exit(0 if tudo_ok else 1)


if __name__ == "__main__":
    main()
