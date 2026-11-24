"""Conferência medida do render (FORMATOS_REELS 12). Roda de reels/culinaria-europa:
python3 rev1/scripts/conferir.py <video_sem_pi> <video_com_pi>"""
import json, re, subprocess, sys
import numpy as np, soundfile as sf
sem, com = sys.argv[1], sys.argv[2]
rel = {}
def sh(*a): return subprocess.run(a, capture_output=True, text=True)
for nome, f in [("sem_pi", sem), ("com_pi", com)]:
    pr = json.loads(sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate:format=duration", "-of", "json", f).stdout)
    lo = sh("ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    rel[nome] = {"duracao_s": float(pr["format"]["duration"]), "video": pr["streams"][0], "audio": pr["streams"][1],
                 "lufs": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lo)[-1]), "pico_verdadeiro_dbtp": float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lo)[-1])}
# bipe: a faixa 23,21–24,12 s da versão com bipe é tom de 1 kHz; na sem bipe é voz
cen = json.load(open("rev1/cenas.json"))
for nome, f in [("sem_pi", sem), ("com_pi", com)]:
    sh("ffmpeg", "-v", "error", "-y", "-i", f, "-vn", "-ac", "1", "-ar", "48000", f"_tmp/conf_{nome}.wav")
    a, sr = sf.read(f"_tmp/conf_{nome}.wav")
    i, j = int((cen["bipe"]["ini"] + 0.05) * sr), int((cen["bipe"]["fim"] - 0.05) * sr)
    X = np.abs(np.fft.rfft(a[i:j])); fr = np.fft.rfftfreq(j - i, 1 / sr)
    rel[nome]["bipe_fracao_1khz"] = round(float((X[(fr > 950) & (fr < 1050)] ** 2).sum() / (X ** 2).sum()), 3)
# legendas: largura e grupos
for nome in ["sem_pi", "com_pi"]:
    g = json.load(open(f"rev1/props_{nome}.json"))["legendas"]
    rel[nome]["legendas"] = {"grupos": len(g), "maior_largura_px": max(x["largura"] for x in g), "menor_px_fonte": min(x["px"] for x in g)}
cs = cen["cenas"]
rel["cenas"] = {"total": len(cs), "menor_video_s": min(round(c["fim"] - c["ini"], 2) for c in cs if c["tipo"] != "foto"),
                "composicoes": {k: sum(1 for c in cs if (("diego" if c["tipo"] == "diego" else c.get("layout", "dividida")) == k)) for k in ["dividida", "cheia", "diego"]}}
json.dump(rel, open("rev1/conferencia.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(rel, ensure_ascii=False, indent=1))
