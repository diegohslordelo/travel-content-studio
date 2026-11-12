"""Decupagem da fala: calcula os trechos (sem espaço entre falas), gera fala.mp4 (vídeo do Diego, SDR, 30 qps, sem áudio)
e voz.wav (48 kHz mono), e o mapa palavra a palavra no tempo do Reel (decupagem.json).
Uso (de dentro de reels/gta6-miami): python3 scripts/decupar.py [--render]"""
import json, math, subprocess, sys
import numpy as np

ed = json.load(open("edicao.json"))
W = json.load(open("transcricao_alinhada.json"))
FPS = 30
SR = 16000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", ed["fonte"], "-af", "highpass=f=120,lowpass=f=4000", "-f", "f32le", "-ac", "1",
                                  "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
hop = SR // 100
db = 20 * np.log10(np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "valid")[::hop]) + 1e-9)  # 10 ms
ENTRA, SAI = ed["bordas"]["entra_db"], ed["bordas"]["sai_db"]


def inicio(t):  # do início da palavra (CTC) volta até 30 ms de silêncio; se o CTC caiu no silêncio, avança até a voz
    i = int(t * 100) + 3
    while i > 0 and not (db[i - 1] < ENTRA and db[i - 2] < ENTRA and db[i - 3] < ENTRA):
        i -= 1
    while db[i] < ENTRA:
        i += 1
    return i / 100


def fim(w_ini, w_fim):  # último quadro de 10 ms com voz dentro da palavra (o CTC passa do fim), depois 30 ms abaixo de SAI
    i = int((w_fim + 0.12) * 100)
    while i > int(w_ini * 100) and db[i] < SAI:
        i -= 1
    while i < len(db) - 3 and not (db[i] < SAI and db[i + 1] < SAI and db[i + 2] < SAI):
        i += 1
    return i / 100


# palavras que ficam (tira os cortes)
corte = {c["tomada"]: c for c in ed["cortes"]}
fica = []
for t in ed["tomadas"]:
    ws = [w for w in W if w["tomada"] == t["id"]]
    if t["id"] in corte:
        k = [w["falado"] for w in ws].index(corte[t["id"]]["de_palavra"])
        ws = ws[:k]
    fica.append((t["id"], ws))

# trechos: quebra a tomada nas pausas internas de silêncio
trechos = []
for tid, ws in fica:
    grupo = [ws[0]]
    for x, y in zip(ws, ws[1:]):
        gap_min = db[int(x["fim"] * 100):int(y["ini"] * 100)].min() if y["ini"] - x["fim"] > 0.02 else 0
        if y["ini"] - x["fim"] > ed["pausas_internas"]["limiar_s"] and gap_min < SAI:
            trechos.append((tid, grupo)); grupo = []
        grupo.append(y)
    trechos.append((tid, grupo))

saida, out_t = [], 0.0
for tid, ws in trechos:
    ini = inicio(ws[0]["ini"])
    f = corte[tid]["fim_antes"] if (tid in corte and ws[-1] is fica[[i for i, _ in fica].index(tid)][1][-1]) else ed.get("fim_manual", {}).get(tid + ":" + ws[-1]["falado"], fim(ws[-1]["ini"], ws[-1]["fim"]))
    qi, qf = math.floor(ini * FPS), math.ceil(f * FPS)
    dur_q = qf - qi
    saida.append({"tomada": tid, "src_q": [qi, qf], "src_s": [round(qi / FPS, 4), round(qf / FPS, 4)], "medido": [ini, f],
                  "out_q": [round(out_t * FPS), round(out_t * FPS) + dur_q],
                  "palavras": [{"falado": w["falado"], "ini": round(w["ini"] - qi / FPS + out_t, 3), "fim": round(min(w["fim"], qf / FPS) - qi / FPS + out_t, 3),
                                "conf": w["conf"]} for w in ws]})
    out_t += dur_q / FPS
for s in saida:
    print(f"{s['tomada']} src {s['src_s'][0]:6.3f}-{s['src_s'][1]:6.3f} (medido {s['medido'][0]:.2f}-{s['medido'][1]:.2f})  out q {s['out_q']}  "
          f"{s['palavras'][0]['falado']} … {s['palavras'][-1]['falado']}")
print(f"duração da fala: {out_t:.3f} s ({round(out_t * FPS)} quadros)")
json.dump({"fps": FPS, "quadros": round(out_t * FPS), "trechos": saida}, open("decupagem.json", "w"), ensure_ascii=False, indent=1)

if "--render" in sys.argv:
    # um trecho por vez (abrir os 12 trechos num só grafo estoura a memória com HEVC 10 bits)
    import os, wave
    os.makedirs("_tmp/trechos", exist_ok=True)
    lista = []
    for i, s in enumerate(saida):
        q0, q1 = s["src_q"]
        arq = f"_tmp/trechos/t{i:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{q0 / FPS - 0.005:.4f}", "-i", ed["fonte"], "-frames:v", str(q1 - q0), "-an",
                        "-vf", ed["hdr_para_sdr"], "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", str(FPS), arq], check=True)
        n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                                "-of", "csv=p=0", arq], capture_output=True, text=True).stdout)
        assert n == q1 - q0, (arq, n, q1 - q0)
        lista.append(f"file '{os.path.basename(arq)}'")
    open("_tmp/trechos/lista.txt", "w").write("\n".join(lista) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "_tmp/trechos/lista.txt", "-c", "copy", "public/fala.mp4"], check=True)
    # voz: 48 kHz mono, 1600 amostras por quadro, fades curtos nas bordas (as bordas já estão no silêncio)
    A = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", ed["fonte"], "-f", "f32le", "-ac", "1", "-ar", "48000", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    partes = []
    for s in saida:
        q0, q1 = s["src_q"]
        x = A[q0 * 1600:q1 * 1600].copy()
        fi, fo = int(0.006 * 48000), int(0.012 * 48000)
        x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo)
        partes.append(x)
    v = np.concatenate(partes)
    with wave.open("_tmp/voz_bruta.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes((np.clip(v, -1, 1) * 32767).astype("<i2").tobytes())
    print("ok: public/fala.mp4 e _tmp/voz_bruta.wav", len(v) / 48000, "s")
