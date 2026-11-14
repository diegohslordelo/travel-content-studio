"""Gera o vídeo com velocidade variável (rampas suaves entre trechos) e o mapa de tempos para o Remotion.
Rodar de dentro de reels/clinica-integralmente:  python3 scripts/remap.py"""
import json, subprocess, numpy as np, os
cfg = json.load(open("scripts/rota.json")); FPS = cfg["fps"]; R = cfg["rampa_s"]
W, H = 1080, 1920
os.makedirs("remotion/public", exist_ok=True)

def frames_do_arquivo(arq, trechos):
    """Lista de índices de quadro do bruto (30 fps) para cada quadro de saída, com rampa de velocidade."""
    # velocidade em função do tempo do bruto, com rampa linear de R*vel segundos em torno das fronteiras
    bounds = [(t["ini"], t["fim"], t["vel"]) for t in trechos]
    def vel(ts):
        for i, (a, b, v) in enumerate(bounds):
            if a <= ts < b or (i == len(bounds) - 1 and ts >= a):
                # rampa na entrada
                if i > 0 and ts < a + R * max(v, bounds[i-1][2]) / 2:
                    w = (ts - a) / (R * max(v, bounds[i-1][2]) / 2)
                    return bounds[i-1][2] + (v - bounds[i-1][2]) * (0.5 + 0.5 * w)
                if i < len(bounds) - 1 and ts > b - R * max(v, bounds[i+1][2]) / 2:
                    w = (b - ts) / (R * max(v, bounds[i+1][2]) / 2)
                    return bounds[i+1][2] + (v - bounds[i+1][2]) * (0.5 + 0.5 * w)
                return v
        return bounds[-1][2]
    ts, out = bounds[0][0], []
    end = bounds[-1][1]
    while ts < end:
        out.append(ts); ts += vel(ts) / FPS
    return out

saida, eventos, t_out = [], [], 0.0
arqs = []
for t in cfg["trechos"]:
    if t["arq"] not in arqs: arqs.append(t["arq"])
for arq in arqs:
    tr = [t for t in cfg["trechos"] if t["arq"] == arq]
    tempos = frames_do_arquivo(arq, tr)
    base = len(saida)
    saida += [(arq, s) for s in tempos]
    for t in tr:
        i0 = base + next(i for i, s in enumerate(tempos) if s >= t["ini"] - 1e-6)
        i1 = base + next((i for i, s in enumerate(tempos) if s >= t["fim"] - 1e-6), len(tempos))
        ev = {"de": i0, "ate": i1, "vel": t["vel"]}
        if "seta" in t: ev["seta"] = t["seta"]
        if t.get("chegada"): ev["chegada"] = True
        eventos.append(ev)

# escreve o vídeo: decodifica cada bruto em 30 fps e repete/pula quadros conforme a lista
enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","remotion/public/rota_base.mp4"], stdin=subprocess.PIPE)
for arq in arqs:
    alvo = [int(round(s * FPS)) for a, s in saida if a == arq]
    dec = subprocess.Popen(["ffmpeg","-v","error","-i",f"fonte/{arq}","-vf",f"fps={FPS},scale={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
    n, buf, k = -1, None, 0
    for idx in alvo:
        while n < idx:
            b = dec.stdout.read(W * H * 3)
            if len(b) < W * H * 3: break
            buf, n = b, n + 1
        enc.stdin.write(buf)
    dec.stdout.close(); dec.wait()
enc.stdin.close(); enc.wait()

# quadro da placa para o fechamento
p = cfg["placa"]
subprocess.run(["ffmpeg","-v","error","-y","-ss",str(p["t"]),"-i",f"fonte/{p['arq']}","-frames:v","1","-vf",f"scale={W}:{H}","-q:v","2","remotion/public/placa.jpg"])
marcos = {k: next(i for i, (a, s) in enumerate(saida) if a == v[0] and s >= v[1]) for k, v in cfg.get("marcos", {}).items()}
json.dump({"fps": FPS, "quadros": len(saida), "eventos": eventos, "marcos": marcos}, open("remotion/src/mapa.json","w"), indent=1)
print("quadros:", len(saida), "=", round(len(saida)/FPS, 2), "s")
for e in eventos: print(e)
