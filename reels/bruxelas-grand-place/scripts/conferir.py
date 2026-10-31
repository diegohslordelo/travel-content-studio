"""Relatório medido da revisão (docs/FORMATOS_REELS.md, 12): formato, loudness, amostras, cortes detectados × cenas,
linha da costura, largura das legendas e transcrição da voz final (Whisper large-v3).
Uso (de dentro de reels/bruxelas-grand-place/): REV=rev1 python3 scripts/conferir.py  → _tmp/conferir_<rev>.json"""
import json, os, re, subprocess
import numpy as np
from PIL import Image, ImageFont

REV = os.environ.get("REV", "rev1")
vid = f"{REV}/reel_grand-place_{REV}.mp4"
p = json.load(open("_tmp/props.json"))
FPS = p["fps"]
out = {}

# 1–2 formato
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", vid], capture_output=True, text=True).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video"); a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
out["formato"] = {"duracao_s": round(float(pr["format"]["duration"]), 3), "video": f"{v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} {v['pix_fmt']}",
                  "audio": f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} canais {int(a.get('bit_rate', 0)) // 1000} kb/s", "tamanho_mb": round(int(pr["format"]["size"]) / 1e6, 1)}

# 9 loudness e amostras
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", vid, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-f", "f32le", "-ac", "2", "-ar", "48000", "-"], capture_output=True).stdout, dtype=np.float32)
out["audio"] = {"lufs_integrado": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]), "pico_verdadeiro_dbtp": float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]),
                "amostras_acima_-1dBFS": int((np.abs(x) > 10 ** (-1 / 20)).sum()), "amostras_em_0dBFS": int((np.abs(x) >= 0.99999).sum())}

# 6 cortes detectados (metade de cima e quadro inteiro) × início das cenas
def cortes(filtro):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", vid, "-vf", f"{filtro}select='gt(scene,0.18)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(t) for t in re.findall(r"pts_time:([\d.]+)", r)]
det = sorted(set(round(t, 2) for t in cortes("crop=1080:880:0:0,") + cortes("")))
ini = [c["ini_q"] / FPS for c in p["cenas"]][1:]
desvio = []
for t in ini:
    perto = [d for d in det if abs(d - t) < 0.35]
    desvio.append({"cena_s": round(t, 2), "detectado_s": round(min(perto, key=lambda d: abs(d - t)), 2) if perto else None})
out["cortes"] = {"detectados": det, "cenas": desvio, "sem_deteccao": [d["cena_s"] for d in desvio if d["detectado_s"] is None]}
durs = [(c["fim_q"] - c["ini_q"]) / FPS for c in p["cenas"]]
out["cenas"] = {"n": len(durs), "media_s": round(sum(durs) / len(durs), 2), "menor_s": round(min(durs), 2), "maior_s": round(max(durs), 2)}

# 8 linha da costura (6 px escuros em y 897–902) nas cenas divididas
fr = []
for c in [c for c in p["cenas"] if c["layout"] == "split" and c["tipo"] != "fala"][:6]:
    t = (c["ini_q"] + c["fim_q"]) / 2 / FPS
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", vid, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    g = np.frombuffer(raw, dtype=np.uint8).reshape(1920, 1080).astype(float)
    fr.append({"cena": c["id"], "linha_media": round(g[897:903].mean(), 1), "acima": round(g[880:890].mean(), 1), "abaixo": round(g[910:920].mean(), 1)})
out["costura"] = fr

# 5 largura das legendas (Inter 800 66 px): 1 linha dentro de x 72–944 com centro em x 540
fonte = None
for cand in ["../../design-system/remotion/node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2"]:
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(cand); f.flavor = None; f.save("/tmp/inter800.ttf"); fonte = ImageFont.truetype("/tmp/inter800.ttf", 66)
    except Exception as e:
        out["legendas_erro"] = str(e)
if fonte:
    larg = [(" ".join(w["texto"] for w in g["palavras"]), fonte.getlength(" ".join(w["texto"] for w in g["palavras"]))) for g in p["legendas"]]
    m = max(larg, key=lambda z: z[1])
    out["legendas"] = {"n": len(larg), "maior": m[0], "largura_px": round(m[1]), "x": [round(540 - m[1] / 2), round(540 + m[1] / 2)], "cabe_em_872": m[1] <= 872}

# 11 transcrição da voz final (Whisper large-v3 no áudio do render)
from faster_whisper import WhisperModel
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(np.frombuffer(pcm, dtype=np.float32), language="pt", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
ws = [w for s in segs for w in s.words]
out["transcricao_final"] = "".join(w.word for w in ws).strip()
out["palavras_baixa_confianca"] = [f"{w.word.strip()} {w.start:.2f}s ({w.probability:.2f})" for w in ws if w.probability < 0.6]
json.dump(out, open(f"_tmp/conferir_{REV}.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
