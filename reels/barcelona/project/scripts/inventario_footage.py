"""Inventário técnico e contact sheets da footage de Barcelona (só leitura).

Rodar de dentro de reels/barcelona/:
    python3 project/scripts/inventario_footage.py

Lê footage/, não altera nenhum arquivo de origem. Gera:
  qa/reports/footage_inventory.json   metadados, SHA-256, verificação de decodificação
  qa/frames/contact_<arquivo>.jpg     1 quadro a cada 2 s, para análise (não é asset)
"""
import glob, hashlib, json, os, subprocess

FOOTAGE = "footage"
FRAMES = "qa/frames"
SAIDA = "qa/reports/footage_inventory.json"
FONTE_ROTULO = "../../design-system/fonts/IBMPlexMono-Medium.ttf"
VIDEO_EXT = {".mp4", ".mov", ".m4v"}
HDR = {"arib-std-b67", "smpte2084"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", p],
                       capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def fps(s):
    n, d = (s or "0/1").split("/")
    return round(int(n) / int(d), 3) if int(d) else None


def rotacao(v):
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            return int(sd["rotation"])
    return int(v.get("tags", {}).get("rotate", 0))


def decodifica(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    erros = [l for l in r.stderr.splitlines() if l.strip()]
    return r.returncode == 0 and not erros, erros[:5]


def contact_sheet(p, nome, dur, hdr):
    n = max(1, int(dur // 2) + 1)
    cols = 6 if n > 6 else n
    linhas = -(-n // cols)
    tm = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
          "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,") if hdr else ""
    rot = (f"drawtext=fontfile={FONTE_ROTULO}:text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:"
           "fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=4,")
    vf = f"fps=1/2,{tm}scale=240:-2,{rot}tile={cols}x{linhas}:padding=4:color=black"
    out = os.path.join(FRAMES, f"contact_{os.path.splitext(nome)[0]}_{os.path.splitext(nome)[1][1:]}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", vf, "-frames:v", "1", "-q:v", "3", out], check=True)
    return out, n


def main():
    itens = []
    for p in sorted(glob.glob(os.path.join(FOOTAGE, "*"))):
        nome = os.path.basename(p)
        if os.path.splitext(nome)[1].lower() not in VIDEO_EXT:
            continue
        j = probe(p)
        fmt = j.get("format", {})
        v = next((s for s in j.get("streams", []) if s["codec_type"] == "video"), {})
        a = next((s for s in j.get("streams", []) if s["codec_type"] == "audio"), {})
        tags = {k.lower(): val for k, val in fmt.get("tags", {}).items()}
        rot = rotacao(v)
        w, h = v.get("width"), v.get("height")
        if abs(rot) in (90, 270):
            w, h = h, w
        dur = float(fmt.get("duration", 0))
        hdr = v.get("color_transfer") in HDR
        ok, erros = decodifica(p)
        sheet, nq = contact_sheet(p, nome, dur, hdr)
        itens.append({
            "arquivo": nome, "extensao": os.path.splitext(nome)[1], "bytes": int(fmt.get("size", 0)),
            "sha256": sha256(p), "duracao_s": round(dur, 3),
            "largura": w, "altura": h, "rotacao": rot, "orientacao": "vertical" if h and w and h > w else "horizontal",
            "fps_real": fps(v.get("r_frame_rate")), "fps_medio": fps(v.get("avg_frame_rate")),
            "codec_video": v.get("codec_name"), "perfil": v.get("profile"), "pix_fmt": v.get("pix_fmt"),
            "transferencia": v.get("color_transfer"), "primarias": v.get("color_primaries"), "hdr": hdr,
            "bitrate_total_kbps": round(int(fmt.get("bit_rate", 0)) / 1000) if fmt.get("bit_rate") else None,
            "codec_audio": a.get("codec_name"), "sample_rate": int(a["sample_rate"]) if a.get("sample_rate") else None,
            "canais": a.get("channels"),
            "criacao": tags.get("creation_time") or tags.get("com.apple.quicktime.creationdate"),
            "data_apple": tags.get("com.apple.quicktime.creationdate"),
            "local_iso6709": tags.get("com.apple.quicktime.location.iso6709") or tags.get("location"),
            "aparelho": " ".join(x for x in (tags.get("com.apple.quicktime.make"), tags.get("com.apple.quicktime.model")) if x) or None,
            "software": tags.get("com.apple.quicktime.software") or tags.get("encoder"),
            "decodifica_sem_erro": ok, "erros_decodificacao": erros,
            "contact_sheet": sheet, "quadros_no_contact_sheet": nq,
        })
        print(f"{nome}: {dur:.2f}s {w}x{h} {itens[-1]['fps_real']}fps {v.get('codec_name')} hdr={hdr} ok={ok}")
    json.dump(itens, open(SAIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(itens), "vídeos ->", SAIDA)


if __name__ == "__main__":
    main()
