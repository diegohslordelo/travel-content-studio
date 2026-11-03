"""Decupagem: corta a voz e o Diego recortado nos MESMOS trechos (número inteiro de quadros a 30 qps) e iguala o nível
entre tomadas pelo RMS da fala. Saída: public/voz.wav (48 kHz mono, sem loudness final), public/diego.webm (VP9 com alfa,
720 × 1280, 30 qps) e, em _tmp/, trechos.json e texto_falas.json (palavras de cada trecho, texto do Whisper large-v3).
Uso (de dentro de reels/amsterdam-primeiro-dia/): python3 scripts/preparar.py [voz|video|tudo]"""
import glob, json, os, subprocess, sys
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
SR = 48000
d = json.load(open("edicao.json"))
FPS = d["fps"]
W = json.load(open("_tmp/tomadas_alinhadas.json"))
os.makedirs("public", exist_ok=True); os.makedirs("_tmp/clipes", exist_ok=True)
passo = sys.argv[1] if len(sys.argv) > 1 else "tudo"


def bruto(f):
    return glob.glob(f"fonte/quarto/{f}.*")[0]


def take(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-af",
                        f"highpass=f={d['audio']['passa_alta_hz']},{d['audio']['afftdn']}", "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


rms_db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
pedacos, trechos, palavras, t, k = [], [], [], 0.0, 0
fade = int(d["audio"]["fade_ms"] / 1000 * SR)
for fa in d["falas"]:
    x = take(bruto(fa["fonte"]))
    a0, b0 = fa["trechos"][0][0], fa["trechos"][-1][1]
    nivel = rms_db(x[int(a0 * SR):int(b0 * SR)])
    # cada palavra da tomada vai para o trecho mais próximo do centro dela (o alinhamento erra até ~0,2 s perto de pausas;
    # os cortes estão no silêncio medido, então nenhuma palavra fica de fora do áudio)
    for i, w in enumerate(W[fa["fonte"]]):
        c = (w[0] + w[1]) / 2
        dist = [0 if tr[0] <= c <= tr[1] else min(abs(c - tr[0]), abs(c - tr[1])) for tr in fa["trechos"]]
        kt = int(np.argmin(dist))
        palavras.append({"fala": fa["id"], "trecho": f"{fa['id']}.{kt}", "i": i, "texto": w[2].strip()})
    for kt, tr in enumerate(fa["trechos"]):
        a, b = tr[0], tr[1]
        fo = int((tr[2] if len(tr) > 2 else d["audio"]["fade_ms"]) / 1000 * SR)
        nq = round((b - a) * FPS)
        n = int(round(nq / FPS * SR))
        seg = x[int(round(a * SR)):int(round(a * SR)) + n].copy()
        if len(seg) < n:
            seg = np.concatenate([seg, np.zeros(n - len(seg))])
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fo:] *= np.linspace(1, 0, fo)
        pedacos.append((seg, nivel))
        ultimo = fa is d["falas"][-1] and kt == len(fa["trechos"]) - 1
        nqv = nq + (round(d["cauda_s"] * FPS) if ultimo else 0)
        trechos.append({"fala": fa["id"], "trecho": f"{fa['id']}.{kt}", "fonte": fa["fonte"], "in": a, "out": round(a + nq / FPS, 4),
                        "inicio": round(t, 4), "quadros": nq, "quadros_video": nqv})
        t += nq / FPS; k += 1
if passo in ("voz", "tudo"):
    alvo = np.mean([n for _, n in pedacos])
    voz = np.concatenate([s * 10 ** ((alvo - n) / 20) for s, n in pedacos])
    sf.write("public/voz.wav", np.concatenate([voz, np.zeros(int(d["cauda_s"] * SR))]).astype(np.float32), SR, subtype="FLOAT")
    json.dump(trechos, open("_tmp/trechos.json", "w"), indent=1)
    json.dump(palavras, open("_tmp/texto_falas.json", "w"), ensure_ascii=False, indent=1)
    print(f"voz {t:.3f} s + cauda {d['cauda_s']} s em {k} trechos")
    print(" ".join(w["texto"] for w in palavras))
if passo in ("video", "tudo"):
    # Diego: o recorte (RVM) de cada tomada, nos mesmos trechos da voz; a última cena segue pela cauda do CTA (se a tomada
    # acabar antes, o último quadro fica parado: tpad; a fala nunca é esticada)
    lista = []
    for i, tr in enumerate(trechos):
        clip = f"_tmp/clipes/{i:02d}.webm"
        nqv = tr["quadros_video"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", f"fonte/recorte/{tr['fonte']}.webm", "-ss", f"{tr['in']:.4f}",
                        "-t", f"{nqv / FPS + 0.2:.4f}", "-an", "-vf", "fps=30,tpad=stop_mode=clone:stop=30,format=yuva420p", "-frames:v", str(nqv),
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "12", "-row-mt", "1", "-deadline", "good",
                        "-cpu-used", "4", "-auto-alt-ref", "0", clip], check=True)
        n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                "stream=nb_read_frames", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip() or 0)
        if n != nqv:
            sys.exit(f"{clip}: {n} quadros, esperado {nqv} (o trecho passa do fim da tomada?)")
        lista.append(clip)
    with open("_tmp/clipes/lista.txt", "w") as f:
        for c in lista:
            f.write(f"file '{os.path.basename(c)}'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/clipes/lista.txt", "-c", "copy", "public/diego.webm"], check=True)
    print(f"diego.webm: {sum(t['quadros_video'] for t in trechos)} quadros")
