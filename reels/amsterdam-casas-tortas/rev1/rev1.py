#!/usr/bin/env python3
"""Reel "As casas de Amsterdam são tortas de propósito" · REV1.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py preparar   # cenas e áudios em _tmp/public (corte, giro, HLG→SDR, recorte 9:16, loudness)
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "Reel")
    python3 rev1.py master     # loudness do master: −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev1.py capa       # capa 1080 × 1920 (quadro estático com a placa)
    python3 rev1.py sem-data   # variante com o CTA "MANDA PRA QUEM VAI" (se o vlog não sair no sábado)
    python3 rev1.py tudo       # preparar → render → master → capa → sem-data

Entradas: rev1.json (decisões desta revisão) e os brutos em ../fonte/ (fora do git; baixar do Drive
pelo `drive_id` de cada fonte em rev1.json). Só usa a biblioteca padrão do Python, ffmpeg e Node.
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_amsterdam-casas-tortas_rev1.mp4")
CAPA = os.path.join(AQUI, "capa_amsterdam-casas-tortas_rev1.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius.
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False):
    print("  $", " ".join(cmd) if len(" ".join(cmd)) < 240 else " ".join(cmd)[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(m[-1]), float(p[-1]) if p else None


def expr_recorte(pontos, desloc=0.0):
    """x(t) do recorte: interpolação suave (smoothstep) entre os pontos [t, x0] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return str(pontos[0][1])
    tt = f"(t-{desloc:.4f})"
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max(({tt}-{t0})/({t1}-{t0}),0),1)"
        seg = f"({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p}))"
        e = f"if(lt({tt},{t1}),{seg},{e})"
    return e


def alcas(d):
    """Alças de 100 ms nas cenas vizinhas a um Arrasto (a transição sobrepõe as duas cenas)."""
    q = round(0.1 * d["fps"])
    ids = [c["id"] for c in d["cenas"]]
    out = {i: [0, 0] for i in ids}
    for t in d["transicoes"]:
        if t["tipo"] == "arrasto":
            k = ids.index(t["entra"])
            out[ids[k - 1]][1] = q
            out[t["entra"]][0] = q
    return out


def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    os.makedirs(PUBLIC, exist_ok=True)
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    props = dict(d)
    cenas = []
    al = alcas(d)
    for c in d["cenas"]:
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        n = round((c["out"] - c["in"]) * fps)
        dur = n / fps
        antes, depois = al[c["id"]]
        vf = []
        entrada = ["-ss", f"{c['in'] - antes / fps:.4f}"]
        if f["girar"] != "auto":
            # O ffmpeg aplica o metadado de rotação ao decodificar (−90 → 90° horário). Com -noautorotate
            # ele copiaria o metadado errado para a saída; por isso deixamos girar e corrigimos aqui.
            correcao = (f["girar"] + rotacao_meta(src)) % 360
            vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
        if f["hdr"]:
            vf.append(TONEMAP)
        if "recorte_x" in c:
            w0, h0 = sonda(src)
            giro = rotacao_meta(src) if f["girar"] == "auto" else f["girar"]
            altura = h0 if giro % 180 == 0 else w0
            largura_recorte = round(altura * W / H / 2) * 2
            vf.append(f"crop=w={largura_recorte}:h={altura}:x='{expr_recorte(c['recorte_x'], antes / fps)}':y=0")
        vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
        arq_v = f"cena_{c['id']}.mp4"
        sh(["ffmpeg", "-v", "error", "-y", *entrada, "-i", src, "-vf", ",".join(vf), "-frames:v", str(n + antes + depois), "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq_v)])
        cena = dict(c, arquivo=arq_v, quadros=n, dur=dur, alca_antes_q=antes, alca_depois_q=depois)
        if c["audio"] in ("voz", "ambiente"):
            cena.update(audio_trecho(src, c["in"], dur, f"cena_{c['id']}.wav", d["mix"][f"{c['audio']}_lufs"]))
        cenas.append(cena)
        print(f"cena {c['id']}: {n} quadros ({dur:.3f} s)" + (f" + alças {antes}/{depois}" if antes or depois else ""))
    props["cenas"] = cenas

    # áudios extras (J-cut)
    inicio = {}
    acum = 0.0
    for c in cenas:
        inicio[c["id"]] = acum
        acum += c["dur"]
    auds = []
    for a in d["audios"]:
        f = d["fontes"][a["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        dur = a["out"] - a["in"]
        aa = dict(a, dur=dur)
        aa.update(audio_trecho(src, a["in"], dur, f"audio_{a['id']}.wav", d["mix"][f"{a['tipo']}_lufs"]))
        t0 = inicio[a["inicio"]["cena"]] + a["inicio"]["t"]
        # sincronia labial: se a mesma fonte aparece numa cena enquanto o áudio toca, a fala tem de cair no mesmo ponto
        for c in cenas:
            sobrepoe = inicio[c["id"]] < t0 + dur and t0 < inicio[c["id"]] + c["dur"]
            if c["fonte"] == a["fonte"] and sobrepoe:
                desvio = (inicio[c["id"]] - t0) - (c["in"] - a["in"])
                print(f"sincronia {a['id']} × cena {c['id']}: desvio {desvio * 1000:+.1f} ms")
                if abs(desvio) > 1000 / fps / 2:
                    sys.exit("áudio fora de sincronia com a imagem")
        auds.append(aa)
    props["audios"] = auds
    props["duracao"] = acum
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {acum:.3f} s · props em _tmp/props.json")


def audio_trecho(src, ini, dur, nome, alvo):
    """Extrai o áudio do trecho em 48 kHz estéreo, iguala a loudness ao alvo da mixagem e faz fades curtos."""
    bruto = os.path.join(TMP, "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", bruto])
    medido, _ = lufs(bruto)
    ganho = alvo - medido
    af = f"volume={ganho:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={max(0, dur - 0.025):.4f}:d=0.025,apad,atrim=0:{dur:.4f}"
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s24le", os.path.join(PUBLIC, nome)])
    print(f"  {nome}: {medido:.1f} LUFS → {alvo} LUFS ({ganho:+.1f} dB)")
    return {"audio_arquivo": nome, "lufs_medido": round(medido, 1), "ganho_db": round(ganho, 1), "lufs": alvo}


def render(props=os.path.join(TMP, "props.json"), saida_bruta=SAIDA_BRUTA):
    cmd = ["npx", "remotion", "render", "src/index.ts", "Reel", saida_bruta, f"--props={props}", f"--public-dir={PUBLIC}",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    r = subprocess.run(cmd, cwd=REMOTION)
    if r.returncode != 0:
        sys.exit("render falhou")


def master(saida_bruta=SAIDA_BRUTA, saida=SAIDA):
    """Ganho linear até −14 LUFS + limitador de pico com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP).

    Não usa o loudnorm dinâmico: ele comprime e muda o equilíbrio voz × música feito na mixagem."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(saida_bruta)
    ganho = alvo - i0
    teto = pico - 0.4  # margem para o AAC
    for _ in range(4):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", saida_bruta, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", saida])
        i, tp = medir_master(saida)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {ganho:+.1f} dB) → {os.path.basename(saida)}")


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def capa():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaReel", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("capa falhou")


def sem_data():
    """Variante com outro CTA na placa do fim (rev1.json, "variantes"): mesmas cenas, legendas e sons."""
    d = carregar()
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        props = json.load(f)
    props["placas"] = d["variantes"]["sem-data"]["placas"]
    arq = os.path.join(TMP, "props_sem-data.json")
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=1)
    bruta = os.path.join(TMP, "reel_sem-data_sem_master.mov")
    render(arq, bruta)
    master(bruta, SAIDA.replace(".mp4", "_sem-data.mp4"))


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"preparar": [preparar], "render": [render], "master": [master], "capa": [capa], "sem-data": [sem_data],
              "tudo": [preparar, render, master, capa, sem_data]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
