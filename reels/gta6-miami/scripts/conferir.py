"""Conferência medida do Reel (FORMATOS_REELS.md, 12). Uso: python3 scripts/conferir.py <video_final.mp4>
Grava rev1/qa/conferencia.json e imprime o resumo."""
import io, json, subprocess, sys, wave
import numpy as np
from fontTools.ttLib import TTFont
from PIL import ImageFont

arq = sys.argv[1]
props = json.load(open("rev1/props.json"))
dec = json.load(open("decupagem.json"))
FPS = props["fps"]
R = {}

# 1–2. formato e duração
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", arq], capture_output=True, text=True).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video")
a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
R["formato"] = {"duracao_s": float(pr["format"]["duration"]), "video": f"{v['width']}x{v['height']} {v['codec_name']} {v['r_frame_rate']} {v.get('pix_fmt')}",
                "audio": f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} canais", "quadros": int(v.get("nb_frames", 0))}

# 3. nada gravado pelo Diego em tela cheia por menos de 2 s
R["diego_tela_cheia"] = [{"cena": c["id"], "dur_s": round((c["fim_q"] - c["ini_q"]) / FPS, 2)} for c in props["cenas"] if c["tipo"] == "diego"]

# 5. legendas: 1 linha, largura pela métrica da Inter 800 66 px, centradas em x 540
woff = "../../design-system/remotion/node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2"
f = TTFont(woff); f.flavor = None; buf = io.BytesIO(); f.save(buf); buf.seek(0)
fonte = ImageFont.truetype(buf, 66)
larg = []
for lg in props["legendas"]:
    txt = " ".join(w["texto"] for w in lg["palavras"])
    larg.append((fonte.getlength(txt), txt))
mx = max(larg)
R["legendas"] = {"grupos": len(larg), "maior_px": round(mx[0]), "maior_texto": mx[1], "x_esq": round(540 - mx[0] / 2), "x_dir": round(540 + mx[0] / 2),
                 "dentro_72_944": all(540 - w / 2 >= 72 and 540 + w / 2 <= 944 for w, _ in larg), "max_palavras": max(len(l["palavras"]) for l in props["legendas"])}

# 6. troca de imagem × palavra: cada cena começa 0,07 s antes da palavra-âncora (ou no início da tomada)
pal = [w for s in dec["trechos"] for w in s["palavras"]]
desv = []
for c in props["cenas"][1:]:
    t = c["ini_q"] / FPS
    w = min(pal, key=lambda x: abs(x["ini"] - t))
    desv.append({"cena": c["id"], "troca_s": round(t, 3), "palavra": w["falado"], "palavra_s": w["ini"], "antes_s": round(w["ini"] - t, 3)})
R["sincronia"] = {"max_desvio_s": max(abs(d["antes_s"]) for d in desv), "cenas": desv}

# 9. loudness e picos do arquivo final
out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(out.rsplit("I:", 1)[1].split("LUFS")[0]); TP = float(out.rsplit("Peak:", 1)[1].split("dBFS")[0])
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
R["audio"] = {"lufs_integrado": I, "pico_verdadeiro_dbtp": TP, "amostras_acima_-1dBFS": int((np.abs(x) > 10 ** (-1 / 20)).sum()), "amostras_0dBFS": int((np.abs(x) >= 1).sum())}

# 10. emendas da voz no silêncio: energia 10 ms antes e depois de cada emenda (voz tratada, antes da mixagem)
w_ = wave.open("_tmp/voz_bruta.wav"); vz = np.frombuffer(w_.readframes(w_.getnframes()), "<i2").astype(np.float32) / 32768
emendas = []
for s in dec["trechos"][1:]:
    k = s["out_q"][0] * 1600
    db = lambda seg: round(float(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)), 1)
    emendas.append({"s": round(k / 48000, 3), "antes_db": db(vz[k - 480:k]), "depois_db": db(vz[k:k + 480]), "salto_amostra": round(float(abs(vz[k] - vz[k - 1])), 4)})
R["emendas"] = emendas
R["espaco_entre_tomadas"] = "0 quadros: cada trecho começa no quadro seguinte ao fim do anterior (decupagem.json, out_q contíguos)"
R["out_q_continuos"] = all(a_["out_q"][1] == b_["out_q"][0] for a_, b_ in zip(dec["trechos"], dec["trechos"][1:]))
json.dump(R, open("rev1/qa/conferencia.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("formato", "diego_tela_cheia", "legendas", "audio", "out_q_continuos")}, ensure_ascii=False, indent=1))
print("sincronia: desvio máx", R["sincronia"]["max_desvio_s"], "s")
print("emendas:", [(e["s"], e["antes_db"], e["depois_db"]) for e in emendas])
