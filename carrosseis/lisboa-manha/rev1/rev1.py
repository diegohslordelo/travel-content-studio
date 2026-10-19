#!/usr/bin/env python3
"""Carrossel "Lisboa em uma manhã: 7 paradas a pé, com a hora real" · REV1.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py fotos      # fotogramas dos brutos em _tmp/public (HLG→SDR, recorte)
    python3 rev1.py slides     # Remotion renderiza os 7 slides (design-system/remotion, still "Carrossel")
    python3 rev1.py folha      # qa_frames/folha_rev1.jpg (os 7 lado a lado) e teste de miniatura da capa
    python3 rev1.py tudo

Entradas: rev1.json (decisões desta revisão) e os brutos em ../fonte/ (fora do git; baixar do Drive,
pasta Youtube/lisboa). Só usa a biblioteca padrão do Python, ffmpeg e Node.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# HLG (iPhone, BT.2020) → SDR BT.709: o mesmo tone mapping dos Reels (Möbius).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv444p"
)


def sh(cmd, cwd=None):
    print("  $", " ".join(cmd)[:200])
    if subprocess.run(cmd, cwd=cwd).returncode != 0:
        sys.exit(f"falhou: {cmd[0]}")


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def nome_saida(i):
    return os.path.join(AQUI, f"lisboa-manha_rev1_{i + 1:02d}.jpg")


def fotos():
    """Fotograma de cada foto: tempo no bruto, HLG→SDR e recorte [x, y, largura, altura] na imagem já girada."""
    d = carregar()
    os.makedirs(PUBLIC, exist_ok=True)
    for nome, f in d["fotos"].items():
        src = os.path.join(FONTE, f["fonte"])
        if not os.path.exists(src):
            sys.exit(f"bruto ausente: ../fonte/{f['fonte']} (Drive, pasta Youtube/lisboa)")
        x, y, w, h = f["recorte"]
        largura = 1080 if nome == "capa.jpg" else 920  # capa em sangria; foto de slide com margem 80 (5.3)
        altura = round(largura * h / w)
        vf = f"{TONEMAP},crop={w}:{h}:{x}:{y},scale={largura}:{altura}:flags=lanczos"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", str(f["t"]), "-i", src, "-vf", vf, "-frames:v", "1", "-q:v", "1",
            os.path.join(PUBLIC, nome)])


def slides():
    d = carregar()
    props = {"serie": d["serie"], "slides": d["slides"], "indice": 0}
    for i in range(len(d["slides"])):
        props["indice"] = i
        arq = os.path.join(TMP, f"props_{i + 1:02d}.json")
        with open(arq, "w", encoding="utf-8") as f:
            json.dump(props, f, ensure_ascii=False)
        cmd = ["npx", "remotion", "still", "src/index.ts", "Carrossel", nome_saida(i), f"--props={arq}", f"--public-dir={PUBLIC}",
               "--image-format=jpeg", "--jpeg-quality=95", "--log=warn"]
        if os.path.exists(CHROME):
            cmd.append(f"--browser-executable={CHROME}")
        sh(cmd, cwd=REMOTION)


def folha():
    """Os 7 slides lado a lado (para revisão) e a capa a 25% e a 1/3 (teste de miniatura, DS 7.2)."""
    d = carregar()
    n = len(d["slides"])
    os.makedirs(os.path.join(AQUI, "qa_frames"), exist_ok=True)
    ent = sum((["-i", nome_saida(i)] for i in range(n)), [])
    filtro = "".join(f"[{i}]scale=360:480[s{i}];" for i in range(n)) + "".join(f"[s{i}]" for i in range(n)) + f"hstack=inputs={n}"
    sh(["ffmpeg", "-v", "error", "-y", *ent, "-filter_complex", filtro, os.path.join(AQUI, "qa_frames", "folha_rev1.jpg")])
    sh(["ffmpeg", "-v", "error", "-y", "-i", nome_saida(0), "-filter_complex",
        "[0]scale=270:360[a];[0]scale=360:480[b];[a]pad=270:480[a2];[a2][b]hstack", os.path.join(AQUI, "qa_frames", "capa_miniatura.jpg")])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"fotos": [fotos], "slides": [slides], "folha": [folha], "tudo": [fotos, slides, folha]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
