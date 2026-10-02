"""Prepara os planos do Reel para o Remotion (intermediários, fora do git).

Rodar de dentro de reels/barcelona/:
    python3 project/scripts/preparar_clipes.py [s01 s05 ...]

Para cada plano de project/timeline.json: corta o trecho, recorta 9:16 no centro_x, converte HLG -> SDR
Rec.709 (curva Hable com o pico real de cada plano), escala para
1080 x 1920 e converte para 30 fps (repetição de quadros: a footage é 24 fps). Sem áudio.
Também copia as fontes do DS de design-system/fonts/ para project/public/fonts/.
Não altera nenhum arquivo de footage/.
"""
import json, os, shutil, subprocess, sys

import numpy as np

TL = json.load(open("project/timeline.json", encoding="utf-8"))
SAIDA = "project/public/clips"
FONTES_DS = "../../design-system/fonts"
FONTES = ["Barlow-Bold.ttf", "BarlowCondensed-ExtraBold.ttf", "BarlowCondensed-Bold.ttf",
          "BarlowCondensed-SemiBold.ttf", "BarlowCondensed-LightItalic.ttf",
          "BarlowCondensed-ExtraBoldItalic.ttf", "IBMPlexMono-Medium.ttf"]

# HLG -> SDR Rec.709 (revisão de cor, 02/10/2026).
# 1. Linearização HLG (BT.2100) com o branco de referência de 203 nits (HLG 75%) em 1,0 (BT.2408).
# 2. BT.2020 -> BT.709 em luz linear.
# 3. Curva Hable, sem dessaturação, com o PICO REAL DO PLANO: o p99,9 do canal mais forte, medido em todo o
#    trecho usado. É o papel do metadado L1 do Dolby Vision (os arquivos são DV 8.4): cada plano é comprimido
#    só até o pico que ele tem de fato. Com o pico fixo de 1000 nits (4,93), planos com pico menor (ex.: o
#    gancho nublado, ≈390 nits) eram comprimidos à toa e ficavam cinza, com os brancos longe do branco.
# 4. Volta para BT.709 com dither. Teste e medições: qa/reports/teste_cor.md.
def hlg_sdr(pico):
    return ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
            f"zscale=p=bt709,tonemap=hable:peak={pico:.3f}:desat=0,"
            "zscale=w=1080:h=1920:f=spline36:t=bt709:m=bt709:r=tv:d=error_diffusion,"
            "format=yuv444p")


def pico_hdr(src, inicio, dur):
    """Pico do trecho em luz linear (1,0 = 203 nits): p99,9 do canal mais forte, amostras a cada 0,25 s."""
    lin = ("zscale=w=480:h=270:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,"
           "format=gbrpf32le,zscale=p=bt709,format=gbrpf32le")
    vals = []
    t = inicio
    while t < inicio + dur:
        r = subprocess.run(["ffmpeg", "-v", "error", "-noautorotate", "-ss", f"{t:.3f}", "-i", src, "-vf", lin,
                            "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True, check=True)
        a = np.frombuffer(r.stdout, dtype=np.float32).reshape(3, -1)
        vals.append(float(np.percentile(a.max(axis=0), 99.9)))
        t += 0.25
    return max(1.0, max(vals))


SDR = "scale=1080:1920:flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709"


PICOS = {}


def hdr(p):
    # -of default=nw=1:nk=1 devolve só o valor. Com csv, os arquivos Dolby Vision do iPhone saem como
    # "arib-std-b67," (vírgula do side data) e a detecção falhava: o HLG passava sem conversão (bug corrigido
    # na revisão de cor de 02/10/2026).
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    return r.stdout.strip().split(",")[0].strip() in ("arib-std-b67", "smpte2084")


def main():
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs("project/public/fonts", exist_ok=True)
    for f in FONTES:
        shutil.copyfile(os.path.join(FONTES_DS, f), os.path.join("project/public/fonts", f))
    fps = TL["fps"]
    so = set(sys.argv[1:])  # opcional: ids dos planos a refazer (ex.: s05)
    for p in TL["planos"]:
        if so and p["id"] not in so:
            continue
        src = os.path.join("footage", p["arquivo"])
        cx = p["centro_x"]
        crop = f"crop=w='trunc(ih*9/16/2)*2':h=ih:x='trunc(min(max(iw*{cx}-ow/2,0),iw-ow)/2)*2':y=0"
        if hdr(src):
            pk = pico_hdr(src, p["entrada_s"], p["quadros"] / fps)
            PICOS[p["id"]] = {"arquivo": p["arquivo"], "pico_linear": round(pk, 3), "pico_nits": round(pk * 203)}
            cor = hlg_sdr(pk)
        else:
            cor = SDR
        vf = f"{crop},{cor},fps={fps},format=yuv420p"
        out = os.path.join(SAIDA, p["id"] + ".mp4")
        dur = p["quadros"] / fps + 0.5
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['entrada_s']:.3f}", "-i", src, "-t", f"{dur:.3f}",
                        "-vf", vf, "-frames:v", str(p["quadros"]), "-an", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "12", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart", out], check=True)
        n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
        print(f"{p['id']} {p['arquivo']} {p['entrada_s']}s +{p['quadros']}q -> {out} ({n} quadros)", flush=True)
        if int(n.strip(",")) != p["quadros"]:
            raise SystemExit(f"{p['id']}: esperado {p['quadros']} quadros, gerado {n}")


def capa():
    """Quadro-base da capa (sem textos), com a mesma conversão de cor dos planos."""
    c = TL["capa"]
    src = os.path.join("footage", c["arquivo"])
    crop = f"crop=w='trunc(ih*9/16/2)*2':h=ih:x='trunc(min(max(iw*{c['centro_x']}-ow/2,0),iw-ow)/2)*2':y=0"
    if hdr(src):
        pk = pico_hdr(src, max(0.0, c["tempo_s"] - 0.5), 1.0)
        PICOS["capa"] = {"arquivo": c["arquivo"], "pico_linear": round(pk, 3), "pico_nits": round(pk * 203)}
        cor = hlg_sdr(pk)
    else:
        cor = SDR
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["tempo_s"]), "-i", src, "-vf", f"{crop},{cor},format=rgb24",
                    "-frames:v", "1", "project/public/capa_base.png"], check=True)
    print("capa_base.png")


if __name__ == "__main__":
    main()
    if len(sys.argv) == 1:
        capa()
    json.dump(PICOS, open("qa/reports/picos_hdr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(PICOS, ensure_ascii=False))
