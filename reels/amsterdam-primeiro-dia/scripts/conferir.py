"""Conferência medida do vídeo final (FORMATOS_REELS.md, 12): formato, duração, loudness e picos, duração de cada cena,
largura das legendas (métrica da fonte Inter 800 66 px) e transcrição da voz final (Whisper large-v3).
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/conferir.py → _tmp/conferir.json"""
import json, os, re, subprocess
import numpy as np

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
REV = os.environ.get("REV", "rev1")
VID = f"{REV}/reel_amsterdam-primeiro-dia_{REV}.mp4"
FONTE = "../../design-system/remotion/node_modules/@fontsource/inter/files/inter-latin-800-normal.woff"
out = {}

pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate:format=duration",
                                "-of", "json", VID], capture_output=True, text=True).stdout)
out["formato"] = {"duracao_s": round(float(pr["format"]["duration"]), 2), "streams": pr["streams"]}

r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", VID, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
out["lufs"] = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
out["pico_dbtp"] = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VID, "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
out["amostras_acima_-1dBFS"] = int((np.abs(a) > 10 ** (-1 / 20)).sum())
out["amostras_0dBFS"] = int((np.abs(a) >= 0.9999).sum())

p = json.load(open("_tmp/props.json"))
out["cenas"] = [{"id": c["id"], "dur_s": round((c["fim_q"] - c["ini_q"]) / 30, 2)} for c in p["cenas"]]

try:
    from PIL import ImageFont
    f = ImageFont.truetype(FONTE, 66)
    larg = []
    for g in p["legendas"]:
        txt = " ".join(w["texto"] for w in g["palavras"])
        larg.append((round(f.getlength(txt)), txt))
    larg.sort(reverse=True)
    out["legenda_maior_px"] = larg[0]
    out["legendas_acima_808px"] = [x for x in larg if x[0] > 808]
except Exception as e:  # noqa: BLE001
    out["legenda_maior_px"] = f"não medido: {e}"

from faster_whisper import WhisperModel
voz = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "public/voz.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(voz, language="pt", word_timestamps=True, beam_size=5)
ws = [(round(w.start, 2), w.word.strip(), round(w.probability, 2)) for s in segs for w in s.words]
out["transcricao_voz_final"] = " ".join(w[1] for w in ws)
out["palavras_confianca_baixa"] = [w for w in ws if w[2] < 0.6]
json.dump(out, open("_tmp/conferir.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "formato"}, ensure_ascii=False, indent=1)[:6000])
print(out["formato"])
