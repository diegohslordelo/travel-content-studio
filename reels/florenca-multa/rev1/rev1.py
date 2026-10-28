#!/usr/bin/env python3
"""Reel "A multa que salvou o trem" (Florença) · REV1 · Tela verde.

Rode de dentro desta pasta:
    python3 rev1.py voz       # decupagem: voz contínua (_tmp/public/voz.wav), segmentos de vídeo e palavras na linha do tempo final
    python3 rev1.py props     # _tmp/props.json para o Remotion (cenas, legendas, sons)
    python3 rev1.py render    # Remotion (composição "ReelFlorencaMulta")
    python3 rev1.py master    # −14 LUFS integrados, pico ≤ −1 dBTP
    python3 rev1.py previa    # prévia 540 × 960
    python3 rev1.py quadros   # folhas de QA

Feitos uma vez (scripts ao lado): recorte.py (RVM), fala/transcricao.json (faster-whisper large-v3), fala/rosto.json.
Brutos em ../fonte/ (fora do git): gravacao/ (Diego, 28/10/2026), acervo/ (Itália, Drive), recorte/ (alfa).
"""
import json, os, re, shutil, subprocess, sys, wave
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp"); PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SR = 48000
ALVO_VOZ = -16.0  # LUFS de cada tomada antes do master
VERSOES = {"com_rostos": True, "sem_rostos": False}  # pedido do Diego (28/10/2026)


def sh(cmd, capturar=False):
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:] if capturar else "")
        sys.exit("falhou: " + " ".join(cmd[:6]))
    return r


def carregar():
    return json.load(open(os.path.join(AQUI, "rev1.json"), encoding="utf-8"))


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])


def pedacos(tk):
    """Trechos [a, b] (s no bruto) da tomada, já sem as pausas cortadas."""
    p, a = [], tk["ini"]
    for c0, c1 in tk["cortes"]:
        p.append([a, c0]); a = c1
    p.append([a, tk["fim"]])
    return p


def ler_wav(arq):
    with wave.open(arq) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def voz():
    d = carregar(); os.makedirs(PUBLIC, exist_ok=True)
    fala = json.load(open(os.path.join(AQUI, "fala", "transcricao.json"), encoding="utf-8"))
    partes, segs, palavras, t_out = [], [], [], 0.0
    fade = int(0.008 * SR)
    for i, tk in enumerate(d["tomadas"]):
        bruto = os.path.join(FONTE, tk["arquivo"])
        wav = os.path.join(TMP, f"voz_{tk['nome']}.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-vn", "-ac", "1", "-ar", str(SR), "-af", "highpass=f=70", "-c:a", "pcm_s16le", wav])
        x = ler_wav(wav)
        # ganho da tomada: mede só os trechos usados
        usado = np.concatenate([x[int(a * SR):int(b * SR)] for a, b in pedacos(tk)])
        tmpu = os.path.join(TMP, "_usado.wav"); gravar(tmpu, usado)
        ganho = 10 ** ((ALVO_VOZ - lufs(tmpu)[0]) / 20)
        rec_ini = max(0.0, tk["ini"] - 0.5)
        ws = fala[os.path.basename(tk["arquivo"])]
        # Whisper prende a 1ª palavra em 0,00 s: usa o começo real da voz (energia) quando ele é posterior
        if ws and ws[0]["t"] < tk["ini"] + 0.15:
            ws[0]["t"] = max(ws[0]["t"], tk.get("voz_ini", tk["ini"] + 0.1))
        for k, (a, b) in enumerate(pedacos(tk)):
            y = x[int(a * SR):int(b * SR)].copy() * ganho
            y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
            partes.append(y)
            segs.append({"tomada": tk["nome"], "arquivo": f"recorte/{tk['nome']}.webm", "de": round(a - rec_ini, 4),
                         "ini": round(t_out, 4), "dur": round(b - a, 4), "salto": k > 0, "ordem": i})
            for w in ws:
                # a palavra fica no trecho onde ela termina (o Whisper estica o começo para dentro das pausas cortadas)
                if a < w["fim"] <= b + 0.05 and w["fim"] > a + 0.02:
                    palavras.append({"w": w["w"], "t": round(t_out + max(w["t"], a) - a, 3), "fim": round(t_out + min(w["fim"], b) - a, 3), "tomada": tk["nome"]})
            t_out += b - a
    y = np.concatenate(partes)
    gravar(os.path.join(PUBLIC, "voz.wav"), y)
    json.dump({"duracao": round(t_out, 4), "segmentos": segs, "palavras": palavras}, open(os.path.join(TMP, "linha.json"), "w"), ensure_ascii=False, indent=1)
    print(f"voz: {t_out:.2f} s · {len(segs)} segmentos · {len(palavras)} palavras · {lufs(os.path.join(PUBLIC, 'voz.wav'))}")
    for i, p in enumerate(palavras):
        print(f"{i}:{p['w']}@{p['t']:.2f}", end="  ")
    print()


def gravar(arq, y):
    y = np.clip(y, -1, 1)
    with wave.open(arq, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())




def props():
    d = carregar(); L = json.load(open(os.path.join(TMP, "linha.json"), encoding="utf-8"))
    rosto = json.load(open(os.path.join(AQUI, "fala", "rosto.json")))
    W, H = d["largura"], d["altura"]; wa, ya = d["diego"]["face_alvo_largura"], d["diego"]["face_alvo_y"]
    tr = {}
    for t, r in rosto.items():
        x, y, w, h = r["face"]; cx, cy = x + w / 2, y + h / 2
        s = max(wa / w, (H - ya) / (H - cy))  # o corpo tem de encostar na borda de baixo
        tr[t] = {"s": round(s, 4), "tx": round(W / 2 - s * cx, 1), "ty": round(ya - s * cy, 1)}
    for sg in L["segmentos"]:
        sg.update(tr[sg["tomada"]])
    P = L["palavras"]
    leg = []
    for a, b, txt in d["legendas"]:
        fim = P[b + 1]["t"] if b + 1 < len(P) and P[b + 1]["t"] - P[b]["fim"] < 0.6 else P[b]["fim"] + 0.25
        leg.append({"ini": round(P[a]["t"] - 0.04, 3), "fim": round(fim - 0.04, 3), "texto": txt})
    props = {"duracao": round(L["duracao"] + 2.1, 3), "fala_fim": L["duracao"], "segmentos": L["segmentos"],
             "palavras": [{"w": p["w"], "t": p["t"], "fim": p["fim"]} for p in P], "legendas": leg,
             "voz": "voz.wav", "trilha": None,  # sem música no vídeo: o Diego põe na plataforma (28/10/2026)
             "voz_lufs": ALVO_VOZ}
    for nome, rostos in VERSOES.items():
        json.dump({**props, "rostos": rostos}, open(os.path.join(TMP, f"props_{nome}.json"), "w"), ensure_ascii=False, indent=1)
    print("props:", props["duracao"], "s ·", len(leg), "legendas ·", tr)


def trilha():
    """Cama: "Sneaky Snitch" (Kevin MacLeod, CC BY 4.0). Some no Murphy e no suspense; volta na revelação. −18 dB da voz sob a fala."""
    d = carregar(); L = json.load(open(os.path.join(TMP, "linha.json"), encoding="utf-8"))
    P = L["palavras"]; dur = L["duracao"] + 2.1
    src = os.path.join(FONTE, "musica", "Sneaky_Snitch.mp3"); wav = os.path.join(TMP, "_musica.wav")
    sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", wav])
    with wave.open(wav) as w:
        m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    nivel = lufs(src)[0]
    g = lambda rel: 10 ** ((ALVO_VOZ + rel - nivel) / 20)
    n = int(dur * SR); out = np.zeros((n, 2), np.float32)
    def bloco(t0, t1, off, rel, fi=0.3, fo=0.3):
        a, b = int(t0 * SR), int(t1 * SR); seg = m[int(off * SR):int(off * SR) + (b - a)].copy()
        k = len(seg); env = np.ones(k, np.float32)
        nfi, nfo = int(fi * SR), int(fo * SR)
        if nfi: env[:nfi] = np.linspace(0, 1, nfi)
        if nfo: env[-nfo:] = np.minimum(env[-nfo:], np.linspace(1, 0, nfo))
        out[a:a + k] += seg * env[:, None] * g(rel)
    murphy, fiscal = P[85]["t"] - 0.1, P[100]["t"] - 0.1
    ironia, frente = P[166]["t"] + 0.6, P[175]["t"] - 0.02
    bloco(0, murphy, 0.0, -18, fi=0.05, fo=0.25)
    bloco(fiscal, ironia, murphy, -18, fi=0.4, fo=0.7)
    bloco(frente, L["duracao"], 75.0, -18, fi=0.03, fo=0.0)
    bloco(L["duracao"], dur, 75.0 + (L["duracao"] - frente), -9, fi=0.0, fo=1.2)
    gravar_st(os.path.join(PUBLIC, "trilha.wav"), out)
    print("trilha:", round(dur, 2), "s · música", round(nivel, 1), "LUFS · cortes em", round(murphy, 2), round(fiscal, 2), round(ironia, 2), round(frente, 2))


def gravar_st(arq, y):
    y = np.clip(y, -1, 1)
    with wave.open(arq, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())


CHROME = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"


def render(so=None):
    so = so or (sys.argv[2] if len(sys.argv) > 2 else None)
    for nome in VERSOES:
        if so and nome != so:
            continue
        cmd = ["npx", "remotion", "render", "src/index.ts", "ReelFlorencaMulta", os.path.join(TMP, f"{nome}_sem_master.mov"),
               f"--props={os.path.join(TMP, f'props_{nome}.json')}", f"--public-dir={PUBLIC}", "--codec=h264", "--crf=14",
               "--pixel-format=yuv420p", "--audio-codec=pcm-16", "--log=warn", "--concurrency=3", f"--browser-executable={CHROME}"]
        print("render", nome)
        if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
            sys.exit("render falhou")


def master():
    """−14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6). Vídeo copiado; áudio AAC 320 kbps."""
    for nome in VERSOES:
        ent = os.path.join(TMP, f"{nome}_sem_master.mov")
        if not os.path.exists(ent):
            continue
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", ent, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
        m = json.loads(r.stderr[r.stderr.rindex("{"):])
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
              f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
        saida = os.path.join(AQUI, f"reel_florenca-multa_rev1_{nome}.mp4")
        sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", saida])
        print(nome, lufs(saida))


def previa():
    for nome in VERSOES:
        ent = os.path.join(AQUI, f"reel_florenca-multa_rev1_{nome}.mp4")
        sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-c:a", "aac", "-b:a", "128k",
            os.path.join(AQUI, f"reel_florenca-multa_rev1_{nome}_previa.mp4")])


if __name__ == "__main__":
    globals()[sys.argv[1]]()
