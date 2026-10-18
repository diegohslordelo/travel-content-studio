#!/usr/bin/env python3
"""Reel "De todas as cidades da Europa que eu fui: meu veredito até agora" · REV2 (sem som).

Parte da REV1 (reels/veredito-europa/rev1/rev1.py). Pedido do Diego em 18/10/2026: trechos estáticos,
vídeo sem som, "voltaria com certeza" no formato das outras categorias, "melhor energia: Barcelona" e
duas versões de "melhor comida: Roma": com a foto do prato (zoom lento) e com o vídeo IMG_5855.

Pipeline (rode de dentro desta pasta; variante = foto, video ou ambas):
    python3 rev2.py preparar [variante]   # cenas em _tmp/<variante>/public (corte, HLG→SDR, recorte 9:16 fixo)
    python3 rev2.py render [variante]     # Remotion monta o Reel sem áudio (composição "Reel", --muted)
    python3 rev2.py final [variante]      # MP4 final sem faixa de áudio (faststart)
    python3 rev2.py capa                  # capa 1080 × 1920 (quadro do gancho com a placa estática)
    python3 rev2.py previa [variante]     # prévia leve 540 × 960
    python3 rev2.py tudo [variante]

Entradas: rev2.json (decisões desta revisão) e os brutos em ../fonte/ (fora do git; baixar do Drive
pelo `drive_id` de cada fonte em rev2.json). Só usa a biblioteca padrão do Python, ffmpeg e Node.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
CAPA = os.path.join(AQUI, "capa_veredito-europa_rev2.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
DURACAO_MAX = 30.0  # pedido do Diego: máximo de 30 s, contando a abertura
VARIANTES = ("foto", "video")

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius.
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)
COR_709 = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd, capturar=False):
    print("  $", " ".join(cmd) if len(" ".join(cmd)) < 240 else " ".join(cmd)[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def caminhos(variante):
    tmp = os.path.join(TMP, variante)
    return {
        "tmp": tmp,
        "public": os.path.join(tmp, "public"),
        "props": os.path.join(tmp, "props.json"),
        "bruta": os.path.join(tmp, "reel_bruto.mov"),
        "saida": os.path.join(AQUI, f"reel_veredito-europa_rev2_{variante}.mp4"),
        "previa": os.path.join(AQUI, f"reel_veredito-europa_rev2_{variante}_previa.mp4"),
    }


def carregar(variante):
    """rev2.json com as cenas da variante aplicadas por cima das cenas comuns."""
    with open(os.path.join(AQUI, "rev2.json"), encoding="utf-8") as f:
        d = json.load(f)
    troca = d["variantes"][variante]
    d["cenas"] = [dict(c, **troca.get(c["id"], {})) for c in d["cenas"]]
    d["variante"] = variante
    return d


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def cena_foto(f, src, n, fps, W, H, saida):
    """Foto parada → vídeo de n quadros com zoom lento de 100% a `zoom_final` (Ken Burns, DS 4.5),
    centrado no ponto `foco` (e não no centro do quadro). A foto é ampliada 4× antes do zoompan para o
    zoom não andar aos saltos de 1 px."""
    r, (fx, fy) = f["recorte"], f["foco"]
    k = 4
    z = f"1+{f['zoom_final'] - 1:.4f}*in/{n - 1}"
    vf = (f"crop={r['w']}:{r['h']}:{r['x']}:{r['y']},scale={r['w'] * k}:{r['h'] * k}:flags=lanczos,"
          f"zoompan=z='{z}':x='{fx * k}*(1-1/zoom)':y='{fy * k}*(1-1/zoom)':d=1:s={W}x{H}:fps={fps},format=yuv420p,setsar=1")
    sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(fps), "-i", src, "-vf", vf, "-frames:v", str(n),
        "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", *COR_709, saida])


def preparar(variante):
    d = carregar(variante)
    c_ = caminhos(variante)
    fps, W, H = d["fps"], d["largura"], d["altura"]
    os.makedirs(c_["public"], exist_ok=True)
    usadas = {c["fonte"] for c in d["cenas"]}
    faltando = [f for k, f in d["fontes"].items() if k in usadas and not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/:")
        for f in faltando:
            if f.get("drive_id"):
                print(f"  curl -L -o '../fonte/{f['arquivo']}' 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
            else:
                print(f"  {f['arquivo']}: {f.get('origem', 'sem ID do Drive')}")
        sys.exit(1)

    props = dict(d)
    cenas = []
    for c in d["cenas"]:
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        n = round((c["out"] - c["in"]) * fps)
        arq_v = f"cena_{c['id']}.mp4"
        if f.get("tipo") == "foto":
            cena_foto(f, src, n, fps, W, H, os.path.join(c_["public"], arq_v))
        else:
            vf = []
            if f["girar"] != "auto":
                correcao = (f["girar"] + rotacao_meta(src)) % 360
                vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
            if f["hdr"]:
                vf.append(TONEMAP)
            if "recorte_x" in c:
                # recorte 9:16 fixo (sem panorâmica: a REV2 prioriza plano parado)
                w0, h0 = sonda(src)
                girado = rotacao_meta(src) % 180 != 0 if f["girar"] == "auto" else f["girar"] in (90, 270)
                altura = w0 if girado else h0
                largura_recorte = round(altura * W / H / 2) * 2
                vf.append(f"crop=w={largura_recorte}:h={altura}:x={c['recorte_x']}:y=0")
            if "recorte_retrato" in c:
                # vídeo vertical: recorte parado de uma fração do quadro (fonte 4K: continua sendo redução para 1080)
                r = c["recorte_retrato"]
                vf.append(f"crop=w=iw*{r['fracao']}:h=ih*{r['fracao']}:x=(iw-ow)*{r['x']}:y=(ih-oh)*{r['y']}")
            vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n), "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", *COR_709,
                os.path.join(c_["public"], arq_v)])
        cenas.append(dict(c, arquivo=arq_v, quadros=n, dur=n / fps, audio="mudo"))
        print(f"cena {c['id']}: {n} quadros ({n / fps:.3f} s) · {f['arquivo']}")
    props["cenas"] = cenas
    props["audios"] = []
    props["sons"] = []
    props["duracao"] = sum(c["dur"] for c in cenas)
    with open(c_["props"], "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"[{variante}] duração total: {props['duracao']:.3f} s · props em {os.path.relpath(c_['props'], AQUI)}")
    if props["duracao"] > DURACAO_MAX:
        sys.exit(f"passou de {DURACAO_MAX:.0f} s (limite pedido pelo Diego, contando a abertura)")


def render(variante):
    c_ = caminhos(variante)
    cmd = ["npx", "remotion", "render", "src/index.ts", "Reel", c_["bruta"], f"--props={c_['props']}", f"--public-dir={c_['public']}",
           "--codec=h264", "--crf=14", "--muted", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("render falhou")


def final(variante):
    """Vídeo sem faixa de áudio (pedido do Diego): a música entra pela biblioteca do Instagram ao postar."""
    c_ = caminhos(variante)
    sh(["ffmpeg", "-v", "error", "-y", "-i", c_["bruta"], "-map", "0:v:0", "-c:v", "copy", "-an", "-movflags", "+faststart", c_["saida"]])
    r = sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", c_["saida"]], capturar=True)
    tipos = r.stdout.split()
    if "audio" in tipos:
        sys.exit("o arquivo final ainda tem faixa de áudio")
    print(f"final: {os.path.basename(c_['saida'])} · faixas: {', '.join(tipos)}")


def capa(variante="foto"):
    """A capa é a mesma nas duas versões (quadro do gancho)."""
    c_ = caminhos(variante)
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaReel", CAPA, f"--props={c_['props']}", f"--public-dir={c_['public']}",
           "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("capa falhou")


def previa(variante):
    c_ = caminhos(variante)
    sh(["ffmpeg", "-v", "error", "-y", "-i", c_["saida"], "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-crf", "26", "-preset", "medium",
        "-an", "-movflags", "+faststart", c_["previa"]])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    alvo = sys.argv[2] if len(sys.argv) > 2 else "ambas"
    variantes = VARIANTES if alvo == "ambas" else (alvo,)
    por_variante = {"preparar": [preparar], "render": [render], "final": [final], "previa": [previa],
                    "tudo": [preparar, render, final, previa]}
    if etapa == "capa":
        capa()
    else:
        for v in variantes:
            for fn in por_variante[etapa]:
                print(f"== {fn.__name__} [{v}]")
                fn(v)
        if etapa == "tudo":
            print("== capa")
            capa()
