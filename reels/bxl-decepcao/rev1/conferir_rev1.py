"""Conferência medida da REV1 (FORMATOS_REELS 12). Roda de reels/bxl-decepcao depois do render final:
    python3 -I rev1/conferir_rev1.py

Gera rev1/qa_frames/cenas_rev1.jpg (1 quadro no meio de cada cena, com o id e o tempo),
rev1/qa_frames/por_segundo_rev1.jpg (1 quadro por segundo) e rev1/conferencia_rev1.json (medidas).
"""
import io
import json
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

VID = "rev1/reel_bxl-decepcao_rev1.mp4"
props = json.load(open("rev1/props_rev1.json"))
FPS = props["fps"]
fonte = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)


def quadro(t, w=270):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", VID, "-frames:v", "1", "-vf", f"scale={w}:-2",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(out)).convert("RGB")


def folha(itens, colunas, saida):
    w, h = itens[0][1].size
    linhas = (len(itens) + colunas - 1) // colunas
    img = Image.new("RGB", (colunas * (w + 6), linhas * (h + 34)), (25, 25, 25))
    d = ImageDraw.Draw(img)
    for i, (rot, im) in enumerate(itens):
        x, y = (i % colunas) * (w + 6), (i // colunas) * (h + 34)
        img.paste(im, (x, y + 30))
        d.text((x + 4, y + 4), rot, fill=(255, 220, 0), font=fonte)
    img.save(saida, quality=85)


def medir(arq):
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                      "stream=codec_name,width,height,r_frame_rate,sample_rate,channels,bit_rate:format=duration",
                                      "-of", "json", arq], capture_output=True, text=True).stdout)
    log = subprocess.run(["ffmpeg", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    resumo = log[log.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", resumo).group(1))
    lra = float(re.search(r"LRA:\s+(-?[\d.]+) LU", resumo).group(1))
    return dict(arquivo=arq, streams=info["streams"], duracao=float(info["format"]["duration"]), lufs=i, true_peak_dbtp=tp, lra=lra)


def main():
    import os
    os.makedirs("rev1/qa_frames", exist_ok=True)
    cenas = []
    for c in props["cenas"]:
        meio = (c["ini"] + c["fim"]) / 2 / FPS
        cenas.append((f"{c['id'][:16]} {c['ini'] / FPS:.1f}s", quadro(meio)))
    folha(cenas, 7, "rev1/qa_frames/cenas_rev1.jpg")
    dur = props["duracao"] / FPS
    seg = [(f"{t:.0f}s", quadro(t + 0.5, 180)) for t in range(int(dur))]
    folha(seg, 12, "rev1/qa_frames/por_segundo_rev1.jpg")
    # quadros-chave em tamanho cheio: gancho completo, notícia com marca-texto, virada (quadro mais claro), CTA
    chave = {
        "gancho": props["gancho"]["linhas"][-1]["em"] + 6,
        "noticia": props["noticia"]["destaque"] + 10,
        "virada_luz": props["luz"]["corte"],
        "virada_depois": props["luz"]["corte"] + 14,
        "cta": props["duracao"] - 10,
    }
    for nome, q in chave.items():
        quadro(q / FPS, 1080).save(f"rev1/qa_frames/{nome}_rev1.jpg", quality=90)
    med = dict(com_trilha=medir(VID), sem_trilha=medir("rev1/reel_bxl-decepcao_rev1_sem_trilha.mp4"),
               previa=medir("rev1/reel_bxl-decepcao_rev1_previa.mp4"))
    durs = [((c["fim"] - c["ini"]) / FPS, c["id"]) for c in props["cenas"]]
    med["cenas"] = dict(total=len(durs), media_s=round(sum(d for d, _ in durs) / len(durs), 2),
                        abaixo_2s=[(i, round(d, 2)) for d, i in durs if d < 2],
                        acima_3s=[(i, round(d, 2)) for d, i in durs if d > 3])
    json.dump(med, open("rev1/conferencia_rev1.json", "w"), ensure_ascii=False, indent=1)
    for k in ("com_trilha", "sem_trilha", "previa"):
        m = med[k]
        print(f"{k}: {m['duracao']:.2f} s · {m['lufs']} LUFS · TP {m['true_peak_dbtp']} dBTP · LRA {m['lra']}")
    print(med["cenas"])


if __name__ == "__main__":
    main()
