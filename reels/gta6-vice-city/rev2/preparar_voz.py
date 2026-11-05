"""REV4 · Decupagem justa + aceleração leve (pedido do Diego, 05/11/2026).
1. Dentro de cada trecho de edicao.json, acha as regiões de fala (energia 100–9.000 Hz > -62 dB, 5 ms).
   Pausas internas >= 0,15 s viram corte; cada região ganha 20 ms antes e 30 ms depois (só silêncio),
   arredondados para fora no quadro da fonte. Resultado: ~0,07 s entre falas, nenhuma palavra comida.
2. Voz e vídeo do Diego cortados nos MESMOS pontos e acelerados juntos (TEMPO), voz com rubberband
   (formantes preservados, sem mudar o tom).
Roda de dentro de reels/gta6-vice-city/rev2. Fonte SDR (bt709): sem tonemap. Limiar por arquivo (piso + 14 dB, no mínimo -62 dB)."""
import json, math, subprocess, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

E = json.load(open("edicao.json"))
TEMPO = E.get("tempo", 1.07)
FPS = E["fps"]
FPS_FONTE = 30000 / 1001
LIMIAR_MIN, PAUSA_MIN, PRE, POS = -62.0, 0.12, 0.020, 0.030
os.makedirs("build", exist_ok=True)

def regioes(x, sr, a, b):
    y = sosfilt(butter(4, [100, 9000], btype="band", fs=sr, output="sos"), x)
    hop = sr // 200
    i0, i1 = int(a * sr) // hop, int(b * sr) // hop
    d = np.array([20 * np.log10(np.sqrt(np.mean(y[i*hop:(i+1)*hop] ** 2)) + 1e-12) for i in range(i0, i1)])
    piso = np.percentile(np.array([20 * np.log10(np.sqrt(np.mean(y[i*hop:(i+1)*hop] ** 2)) + 1e-12) for i in range(len(y) // hop)]), 10)
    on = d > max(LIMIAR_MIN, piso + 14)
    regs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            regs.append([(i0 + i) * hop / sr, (i0 + j) * hop / sr]); i = j
        else:
            i += 1
    regs = [r for r in regs if r[1] - r[0] >= 0.03]          # cliques soltos fora
    m = []
    for r in regs:
        if m and r[0] - m[-1][1] < PAUSA_MIN: m[-1][1] = r[1]
        else: m.append(r)
    return m

segs = []  # (arquivo, ini, fim, fala_id)
for f in E["falas"]:
    x, sr = sf.read(f"../_tmp/wav48/{f['arquivo']}.wav", dtype="float32")
    rs = regioes(x, sr, f["entrada"], f["saida"])
    for k, (a, b) in enumerate(rs):
        on, off = a, b
        a = max(f["entrada"], a - PRE); b = min(f["saida"], b + POS)
        if k + 1 < len(rs): b = min(b, rs[k + 1][0] - PRE)
        # quadro da fonte mais próximo que ainda fica no silêncio (>= 10 ms antes da fala, >= 15 ms depois)
        ac = math.ceil(a * FPS_FONTE) / FPS_FONTE; a = ac if ac <= on - 0.010 else math.floor(a * FPS_FONTE) / FPS_FONTE
        bf = math.floor(b * FPS_FONTE) / FPS_FONTE; b = bf if bf >= off + 0.015 else math.ceil(b * FPS_FONTE) / FPS_FONTE
        segs.append((f["arquivo"], a, b, f["id"]))

# ---- áudio ----
partes, t, linha = [], 0.0, []
cur = None
for arq, a, b, fid in segs:
    x, sr = sf.read(f"../_tmp/wav48/{arq}.wav", dtype="float32")
    s = x[int(round(a * sr)):int(round(b * sr))].copy()
    n = int(0.008 * sr); r = np.linspace(0, 1, n); s[:n] *= r; s[-n:] *= r[::-1]
    partes.append(s)
    if cur is None or cur["id"] != fid:
        cur = {**next(f for f in E["falas"] if f["id"] == fid), "inicio": t}; linha.append(cur)
    t += len(s) / sr; cur["fim"] = t
voz = np.concatenate(partes)
sf.write("build/voz_lenta.wav", voz, sr, subtype="PCM_24")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/voz_lenta.wav", "-af",
                f"rubberband=tempo={TEMPO}:formant=preserved:pitchq=quality", "-c:a", "pcm_s24le", "build/voz_crua.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/voz_crua.wav", "-af",
                f"highpass=f={E['audio']['passa_alta_hz']},afftdn={E['audio']['afftdn']}", "-c:a", "pcm_s24le", "build/voz.wav"], check=True)
dur = sf.info("build/voz_crua.wav").duration
for l in linha:
    l["inicio"] = round(l["inicio"] / TEMPO, 4); l["fim"] = round(l["fim"] / TEMPO, 4)
json.dump({"duracao": round(dur, 4), "tempo": TEMPO, "falas": linha,
           "segmentos": [{"arquivo": s[0], "entrada": round(s[1], 4), "saida": round(s[2], 4), "fala": s[3]} for s in segs]},
          open("build/linha_voz.json", "w"), ensure_ascii=False, indent=1)

# ---- vídeo do Diego: mesmos segmentos, HDR -> SDR, acelerado igual ----
arqs = sorted({s[0] for s in segs})
ins = []
for a in arqs: ins += ["-i", f"../fonte/fala/{a}.MOV"]
TM = "format=yuv420p"
filt = []
for i, (arq, a, b, _) in enumerate(segs):
    filt.append(f"[{arqs.index(arq)}:v]trim=start={a:.5f}:end={b:.5f},setpts=PTS-STARTPTS[s{i}]")
filt.append("".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,setpts=(PTS-STARTPTS)/{TEMPO},"
            + TM + f",scale=1080:1920,fps={FPS}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(filt), "-map", "[out]",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "build/diego.mp4"], check=True)
print(f"{len(segs)} segmentos · voz {sum(s[2]-s[1] for s in segs):.2f} s -> {dur:.2f} s (x{TEMPO})")
