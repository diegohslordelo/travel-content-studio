#!/usr/bin/env python3
"""Stories "Caixa de pergunta: o que você quer saber de Amsterdam?" · REV1.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py fundos     # fotogramas 1080 × 1920 dos brutos em _tmp/public (HLG→SDR, recorte 9:16)
    python3 rev1.py telas      # Remotion renderiza as 3 telas e a variante sem data (composição "Story", quadro 45)
    python3 rev1.py tudo

Os brutos são os do Reel das casas tortas (reels/amsterdam-casas-tortas/fonte, fora do git).
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.join(RAIZ, "design-system", "remotion")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

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


def fundos():
    d = carregar()
    os.makedirs(PUBLIC, exist_ok=True)
    for t in d["telas"]:
        f = d["fontes"][t["fonte"]]
        src = os.path.join(RAIZ, f["pasta"], f["arquivo"])
        if not os.path.exists(src):
            sys.exit(f"bruto ausente: {f['pasta']}/{f['arquivo']} (Drive id {f['drive_id']})")
        if f.get("foto"):  # foto do Diego: já é SDR, só recorta [largura, altura, x, y] na resolução original (1:1)
            w, h, x, y = t["recorte_foto"]
            vf = f"crop={w}:{h}:{x}:{y}"
            entrada = ["-i", src]
        else:
            recorte = "" if t["recorte_x"] is None else f",crop=1215:2160:{t['recorte_x']}:0"
            vf = f"{TONEMAP}{recorte},scale=1080:1920:flags=lanczos"
            entrada = ["-ss", str(t["t"]), "-i", src]
        sh(["ffmpeg", "-v", "error", "-y", *entrada, "-vf", vf, "-frames:v", "1", "-q:v", "1",
            os.path.join(PUBLIC, f"fundo_{t['id']}.jpg")])


def render_tela(props, saida):
    arq = os.path.join(TMP, os.path.basename(saida) + ".json")
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False)
    cmd = ["npx", "remotion", "still", "src/index.ts", "Story", saida, f"--props={arq}", f"--public-dir={PUBLIC}", "--frame=45",
           "--image-format=jpeg", "--jpeg-quality=95", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    sh(cmd, cwd=REMOTION)


def telas():
    d = carregar()
    for t in d["telas"]:
        props = {"fundo": f"fundo_{t['id']}.jpg", **{k: t[k] for k in ("placa", "legenda", "bilhete", "legendaBaseY") if k in t}}
        render_tela(props, os.path.join(AQUI, f"story_amsterdam-pergunta_rev1_{t['id']}.jpg"))
        extra = d["variantes"]["sem-data"]["telas"].get(t["id"])
        if extra:
            render_tela({**props, **extra}, os.path.join(AQUI, f"story_amsterdam-pergunta_rev1_{t['id']}_sem-data.jpg"))


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"fundos": [fundos], "telas": [telas], "tudo": [fundos, telas]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
