"""Monta a voz (voz_bruta.wav) e o vídeo do Diego (fala.mp4) com os MESMOS trechos, em número inteiro de quadros.
Também gera as palavras com tempo na linha do tempo final (palavras.json).
Uso (de dentro de reels/bruges-bate-volta): python3 scripts/voz.py revN
Tratamento: REV1 = passa-alta 70 Hz + redução de ruído no conjunto. A partir da REV2 (edicao.json → "tratamento"),
cada peça passa por passa-alta + compressão leve e cada tomada é igualada no mesmo loudness antes de juntar."""
import json, re, subprocess, sys, os
rev = sys.argv[1]
E = json.load(open(f"{rev}/edicao.json"))
W = json.load(open("_tmp/transcricao_whisper.json"))
fps = E["fps"]
tmp = "_tmp/voz"; os.makedirs(tmp, exist_ok=True)
TONE = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
pecas, palavras, t = [], [], 0.0
for f in E["falas"]:
    ws = W[f["tomada"] + ".MOV"]
    n = len(f["trechos"])
    for k, (a, b) in enumerate(f["trechos"]):
        a0 = max(0.0, a - (E["pad_ini"] if k == 0 else 0.0))
        b0 = b + (E["pad_fim"] + f["pausa_depois"] if k == n - 1 else 0.0)
        q = round((b0 - a0) * fps)          # duração em quadros inteiros
        dur = q / fps
        pecas.append({"fala": f["id"], "tomada": f["tomada"], "ini": round(a0, 3), "dur": dur, "t": round(t, 4), "q": q})
        for w in ws:
            meio = (w["s"] + w["e"]) / 2
            if a0 <= meio < a0 + dur:
                palavras.append({"w": w["w"], "s": round(t + max(w["s"], a0) - a0, 3), "e": round(t + min(w["e"], a0 + dur) - a0, 3), "p": w["p"], "fala": f["id"]})
        t += dur
TRAT = E.get("tratamento")


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])


# corta cada peça (vídeo 30 qps SDR + áudio 48 kHz mono)
lista_v, lista_a = [], []
for i, p in enumerate(pecas):
    v, a = f"{tmp}/v{i:02d}.mp4", f"{tmp}/a{i:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(p["ini"]), "-i", f"fonte/{p['tomada']}.MOV", "-t", f"{p['dur']:.4f}",
                    "-vf", f"{TONE},fps={fps},scale=1080:1920", "-frames:v", str(p["q"]), "-an", "-c:v", "libx264", "-crf", "16", "-preset", "fast", v], check=True)
    cadeia = "anull" if not TRAT else f"highpass=f={TRAT['passa_alta_hz']},{TRAT['compressor']}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(p["ini"]), "-i", f"fonte/{p['tomada']}.MOV", "-t", f"{p['dur']:.4f}",
                    "-vn", "-ac", "1", "-ar", "48000", "-af", cadeia, "-c:a", "pcm_f32le", a], check=True)
    lista_v.append(v); lista_a.append(a)
# REV2+: iguala o loudness de cada tomada (as tomadas variam de −16 a −24 LUFS na gravação)
if TRAT:
    for tom in sorted({p["tomada"] for p in pecas}):
        idx = [i for i, p in enumerate(pecas) if p["tomada"] == tom]
        open(f"{tmp}/t.txt", "w").write("".join(f"file '{os.path.abspath(lista_a[i])}'\n" for i in idx))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/t.txt", "-c:a", "pcm_f32le", f"{tmp}/t.wav"], check=True)
        g = TRAT["alvo_tomada_lufs"] - lufs(f"{tmp}/t.wav")
        for i in idx:
            pecas[i]["ganho_db"] = round(g, 2)
# fades curtos em toda emenda (sem clique)
for i, a in enumerate(lista_a):
    g = pecas[i].get("ganho_db", 0.0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", f"volume={g}dB,afade=t=in:d=0.012,areverse,afade=t=in:d=0.02,areverse", "-c:a", "pcm_f32le", a.replace(".wav", "_f.wav")], check=True)
    lista_a[i] = a.replace(".wav", "_f.wav")
open(f"{tmp}/lv.txt", "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in lista_v))
open(f"{tmp}/la.txt", "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in lista_a))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/lv.txt", "-c", "copy", "public/fala.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/la.txt", "-c:a", "pcm_f32le", f"{tmp}/voz_concat.wav"], check=True)
if TRAT:
    # sem redução de ruído: o piso da gravação é −78 dBFS e o filtro só criaria artefato
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/voz_concat.wav", "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", "public/voz_bruta.wav"], check=True)
else:
    # REV1: passa-alta 70 Hz, redução leve de ruído (FORMATOS_REELS 10.1); o ganho final é no master
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/voz_concat.wav", "-af", "highpass=f=70,afftdn=nr=8:nf=-58:tn=1",
                    "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", "public/voz_bruta.wav"], check=True)
json.dump({"duracao": round(t, 4), "pecas": pecas, "palavras": palavras}, open(f"{rev}/palavras.json", "w"), ensure_ascii=False, indent=1)
print(f"duração {t:.2f} s · {len(pecas)} peças · {len(palavras)} palavras")
