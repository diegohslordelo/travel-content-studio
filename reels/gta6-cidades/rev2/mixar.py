"""Mixagem: voz decupada + efeitos do formato (PDX_*) + clack do CTA (DS), master -14 LUFS / <= -1 dBTP.
Volumes relativos à voz (docs/REFERENCIA_EDICAO_FORMATOS.md 4.1): impacto -4 dB, transição -6 dB, clack -6 dB.
Nível do evento = RMS máximo em 50 ms; nível da voz = percentil 75 do RMS em 50 ms com fala."""
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import resample_poly
P = json.load(open("public/props.json")); W = json.load(open("build/palavras.json"))
S = "../../../design-system/sons"
def t(fala, pal, n=1):
    h = [w for w in W if w["fala"] == fala and w["palavra"].strip(".,:?!").lower() == pal.lower()]
    return h[n-1]["inicio"]
cena = {c["id"]: c for c in P["cenas"]}
EVENTOS = [
    ("externos/PDX_impacto.wav", t("gancho_a", "450") - 0.02, -4, "450 reais"),
    ("externos/PDX_swish.wav",   cena["virada"]["ini"] - 0.03, -6, "clarão: sai do GTA"),
    ("externos/PDX_impacto.wav", t("florenca", "463") - 0.02, -4, "463 degraus"),
    ("externos/PDX_impacto.wav", t("fogo", "3") - 0.02, -4, "3 milhões"),
    ("externos/PDX_ar_longo.wav", cena["veneza_real"]["ini"] - 0.20, -6, "luz de passagem: jogo -> Veneza real"),
    ("PD_clack_v1.wav",          cena["cta"]["ini"] + 0.28, -6, "placa do CTA (DS)"),
]
voz, sr = sf.read("build/voz.wav", dtype="float64")
dur = P["duracao"]; N = int(round(dur * sr)) + sr // 2
mix = np.zeros(N); mix[:len(voz)] += voz
def rms50(x):
    h = int(0.05 * sr); v = [np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0, len(x)-h, h)]
    return 20*np.log10(np.array(v) + 1e-12)
rv = rms50(voz); ref = np.percentile(rv[rv > rv.max()-30], 75)
log = []
for arq, em, rel, nome in EVENTOS:
    x, s2 = sf.read(f"{S}/{arq}", dtype="float64")
    if x.ndim > 1: x = x.mean(axis=1)
    if s2 != sr: x = resample_poly(x, sr, s2)
    g = ref + rel - rms50(x).max(); x = x * 10**(g/20)
    i = int(round(em * sr)); mix[i:i+len(x)] += x[:N-i]
    log.append({"som": arq, "em_s": round(em, 3), "rel_db": rel, "ganho_db": round(g, 1), "funcao": nome})
sf.write("build/mix.wav", mix, sr, subtype="FLOAT")
# master: ganho linear até -14 LUFS e limitador com sobreamostragem 4x
def lufs(f):
    o = subprocess.run(["ffmpeg","-v","info","-i",f,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    I = float(o.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0]); TP = float(o.split("True peak:")[1].split("Peak:")[1].split("dBFS")[0])
    return I, TP
I0, _ = lufs("build/mix.wav")
ganho = -14.0 - I0
subprocess.run(["ffmpeg","-v","error","-y","-i","build/mix.wav","-af",
    f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit=0.76:attack=1:release=60:level=disabled,aresample=48000",
    "-c:a","pcm_s24le","build/master.wav"],check=True)
I1, TP1 = lufs("build/master.wav")
if abs(I1 + 14) > 0.15:
    subprocess.run(["ffmpeg","-v","error","-y","-i","build/master.wav","-af",f"volume={-14-I1:.2f}dB","-c:a","pcm_s24le","build/master2.wav"],check=True)
    import os; os.replace("build/master2.wav","build/master.wav"); I1, TP1 = lufs("build/master.wav")
json.dump({"ref_voz_rms50_db": round(ref,1), "eventos": log, "master_lufs": I1, "master_true_peak_dbtp": TP1}, open("build/mix_log.json","w"), ensure_ascii=False, indent=1)
print(json.dumps({"eventos": log, "LUFS": I1, "TP": TP1}, ensure_ascii=False, indent=1))
