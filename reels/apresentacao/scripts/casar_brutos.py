"""Acha, quadro a quadro, o trecho de cada bruto que corresponde a um corte do master.

Compara miniaturas em tons de cinza (96x54, média zero e variância um) por correlação normalizada,
deslizando o corte do master ao longo do bruto. Uso: casar_brutos.py lista_de_cortes.json PASTA_BRUTOS
"""
import glob, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

W, H = 96, 54


def quadros(arq, a=None, dur=None, fps=24):
    cmd = ["ffmpeg", "-v", "error"]
    if a is not None:
        cmd += ["-ss", f"{a:.3f}"]
    cmd += ["-i", arq]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-map", "0:v:0", "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.uint8).astype(np.float32)
    x = x.reshape(-1, H * W)
    x -= x.mean(1, keepdims=True)
    x /= x.std(1, keepdims=True) + 1e-6
    return x


def casar(seg, bruto):
    n = len(seg)
    melhor = []
    for o in range(0, len(bruto) - n + 1):
        melhor.append(float(np.mean(np.sum(seg * bruto[o:o + n], 1) / seg.shape[1])))
    return np.array(melhor)


if __name__ == "__main__":
    edl = R.carregar(sys.argv[1])
    brutos = {os.path.basename(b): quadros(b) for b in sorted(glob.glob(os.path.join(sys.argv[2], "*")))}
    alvo = [c for c in edl["_cortes"] if c.get("ambiente_de")]
    res = []
    for c in alvo:
        seg = quadros(edl["master"], c["entrada"], c["saida"] - c["entrada"])
        linhas = []
        for nome, b in brutos.items():
            if len(b) < len(seg):
                continue
            s = casar(seg, b)
            o = int(s.argmax())
            linhas.append((float(s.max()), nome, o / 24.0))
        linhas.sort(reverse=True)
        (s1, n1, t1), (s2, n2, _) = linhas[0], linhas[1]
        e = c["entrada"]
        print(f"{c['bloco']:12s} master {int(e // 60):02d}:{e % 60:05.2f} ({c['saida'] - e:.2f} s) {c.get('rotulo', '')[:26]:26s} "
              f"-> {n1} em {t1:6.2f} s (corr {s1:.3f}; 2º: {n2} {s2:.3f})")
        res.append({"entrada_master": e, "rotulo": c.get("rotulo"), "bruto": n1, "t_bruto": t1, "corr": s1, "segundo": [n2, s2]})
    json.dump(res, open(os.path.join(os.path.dirname(sys.argv[1]), "analise_outras", "casamento_brutos.json"), "w"), indent=1, ensure_ascii=False)
