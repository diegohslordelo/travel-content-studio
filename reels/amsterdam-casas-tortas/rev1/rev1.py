#!/usr/bin/env python3
"""Reel "As casas que dançam em Amsterdam" (AMS-casas-tortas) · REV1.

Pipeline (rode de dentro desta pasta):
    python3 rev1.py voz        # narração: transcrição (cache), corte, declip, voz a −16 LUFS, palavras com tempo
    python3 rev1.py planos     # planos 9:16: foto, quadro congelado ou vídeo estabilizado (tripé), HLG → SDR
    python3 rev1.py sons       # efeitos do desenho (síntese) e ambiente de cada plano
    python3 rev1.py props      # linha do tempo (âncoras na fala) → _tmp/props.json
    python3 rev1.py render     # Remotion (design-system/remotion, composição "CasasTortas")
    python3 rev1.py master     # −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP (DS V2, 4.6)
    python3 rev1.py capa       # capa 1080 × 1920
    python3 rev1.py folha      # folha de quadros para a QA
    python3 rev1.py tudo

Entradas: rev1.json (decisões) e ../fonte/ (fora do git): brutos IMG_*.MOV, foto1.jpg, foto2.jpg e
narracao/narracao_N.m4a (baixar do Drive pelo `drive_id`). A transcrição usa faster-whisper large-v3;
o resultado fica em ../fonte/narracao/asr_large-v3.json (cache).

Âncoras (rev1.json): "palavra[#n]@take[±ms]" = início da n-ésima ocorrência da palavra no take;
"fim@take" = fim da fala do take; "<plano>+ms" = início de um plano.
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
NARR = os.path.join(FONTE, "narracao")
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SONS_DS = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "sons", "sons_v1.json"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_amsterdam-casas-tortas_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_amsterdam-casas-tortas_rev1_previa.mp4")
CAPA = os.path.join(AQUI, "capa_amsterdam-casas-tortas_rev1.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SR = 48000

# HLG (iPhone, BT.2020) → SDR BT.709. Hable com nível de referência de 203 nits: no comparativo com Möbius
# (o do Madrid, que estoura o céu de dia), Reinhard e a própria conversão do iPhone, é o que mais se
# aproxima do SDR do iPhone e preserva as nuvens.
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False, entrada=None):
    txt = " ".join(cmd)
    print("  $", txt if len(txt) < 240 else txt[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, input=entrada)
    if r.returncode != 0:
        if capturar:
            print(r.stderr[-3000:] if isinstance(r.stderr, str) else r.stderr[-3000:].decode(errors="ignore"))
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def ler_json(nome):
    with open(os.path.join(TMP, nome), encoding="utf-8") as f:
        return json.load(f)


def salvar_json(nome, dado):
    os.makedirs(TMP, exist_ok=True)
    with open(os.path.join(TMP, nome), "w", encoding="utf-8") as f:
        json.dump(dado, f, ensure_ascii=False, indent=1)


def norm(p):
    """Palavra para comparação: minúsculas, sem acento e sem pontuação."""
    p = unicodedata.normalize("NFD", p.lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", p)


def decodificar(arq, sr=SR, canais=1):
    pcm = sh(["ffmpeg", "-v", "error", "-i", arq, "-ac", str(canais), "-ar", str(sr), "-f", "f32le", "-"], capturar=True).stdout
    x = np.frombuffer(pcm, np.float32)
    return x.reshape(-1, canais) if canais > 1 else x


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(i[-1]), (float(p[-1]) if p else None)


def lufs_50ms(x, sr=SR):
    """Loudness K-ponderada (BS.1770) na janela de 50 ms mais alta: a mesma medida de design-system/sons/sons_v1.json."""
    from scipy.signal import lfilter

    # filtro K a 48 kHz (BS.1770-4): prateleira de agudos + passa-altas
    y = lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585], x.astype(np.float64))
    y = lfilter([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621], y)
    n = int(0.05 * sr)
    e = np.array([np.mean(y[i : i + n] ** 2) for i in range(0, max(1, len(y) - n), n // 4)])
    return float(-0.691 + 10 * np.log10(e.max() + 1e-12))


# ------------------------------------------------------------------ narração

def asr():
    """Transcrição com faster-whisper large-v3 e tempo por palavra (cache em ../fonte/narracao)."""
    cache = os.path.join(NARR, "asr_large-v3.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f)
    from faster_whisper import WhisperModel

    d = carregar()
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
    res = {}
    for tk in d["narracao"]["takes"]:
        audio = decodificar(os.path.join(NARR, tk["arquivo"]), sr=16000)
        segs, _ = m.transcribe(audio, language="pt", word_timestamps=True, beam_size=5,
                               initial_prompt="Amsterdã, Dancing Houses, rua Amstel, estacas de madeira.")
        res[tk["arquivo"]] = [{"w": w.word.strip(), "ini": round(w.start, 3), "fim": round(w.end, 3), "p": round(w.probability, 3)}
                              for s in segs for w in s.words]
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


def envelope(x, passo=0.01):
    n = int(passo * SR)
    k = len(x) // n
    rms = np.sqrt((x[: k * n].reshape(k, n) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(rms)


def limites_fala(x, ultima_palavra):
    """Início e fim da fala pela energia (10 ms): piso = p5, fala = p90, limiar a 35% entre os dois.
    O fim é o do último trecho contínuo (≥ 80 ms) que começa até 0,3 s depois da última palavra do Whisper:
    os estalos isolados do fim da gravação ficam de fora."""
    db = envelope(x)
    piso, fala = np.percentile(db, 5), np.percentile(db, 90)
    on = np.where(db > piso + 0.35 * (fala - piso))[0]
    trechos = np.split(on, np.where(np.diff(on) > 6)[0] + 1)
    validos = [r for r in trechos if len(r) >= 8 and r[0] * 0.01 <= ultima_palavra + 0.3]
    return on[0] * 0.01, validos[-1][-1] * 0.01 + 0.01, db


def refinar(palavras, db, ini, fim):
    """O Whisper prende a 1ª palavra no início do arquivo e erra fronteiras em até ~100 ms. A 1ª palavra
    começa no início da fala; cada fronteira vai para o vale de energia mais próximo (±70 ms)."""
    ws = [dict(w) for w in palavras]
    ws[0]["ini"] = max(ws[0]["ini"], ini)
    for a, b in zip(ws[:-1], ws[1:]):
        f = (a["fim"] + b["ini"]) / 2
        i0, i1 = max(0, int((f - 0.07) / 0.01)), min(len(db) - 1, int((f + 0.07) / 0.01))
        if i1 > i0:
            vale = (i0 + int(np.argmin(db[i0:i1 + 1]))) * 0.01 + 0.005
            if a["ini"] + 0.04 < vale < b["fim"] - 0.04:
                a["fim"] = b["ini"] = round(vale, 3)
    ws[-1]["fim"] = min(max(ws[-1]["fim"], ws[-1]["ini"] + 0.1), fim)
    return ws


def voz():
    d = carregar()
    os.makedirs(PUBLIC, exist_ok=True)
    trans = asr()
    alvo = d["mix"]["voz_lufs"]
    cauda = d["narracao"]["cauda"]
    takes = []
    for i, tk in enumerate(d["narracao"]["takes"], 1):
        src = os.path.join(NARR, tk["arquivo"])
        if not os.path.exists(src):
            sys.exit(f"falta {src}: curl -L -o '{src}' 'https://drive.usercontent.google.com/download?id={tk['drive_id']}&export=download&confirm=t'")
        x = decodificar(src)
        ini, fim, db = limites_fala(x, trans[tk["arquivo"]][-1]["fim"])
        palavras = refinar(trans[tk["arquivo"]], db, ini, fim)
        corte0 = max(0.0, ini - 0.05)
        corte1 = min(len(x) / SR, fim + cauda)
        dur = corte1 - corte0
        bruto = os.path.join(TMP, f"voz_{i}_bruto.wav")
        filtros = (["adeclip"] if tk.get("declip") else []) + ["highpass=f=80", "acompressor=threshold=-24dB:ratio=2:attack=8:release=140:makeup=1"]
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{corte0:.3f}", "-i", src, "-t", f"{dur:.3f}", "-ac", "2", "-ar", str(SR),
            "-af", ",".join(filtros), "-c:a", "pcm_s24le", bruto])
        medido, _ = lufs(bruto)
        ganho = alvo - medido
        af = f"volume={ganho:.2f}dB,afade=t=in:d=0.02,afade=t=out:st={max(0, dur - 0.06):.3f}:d=0.06"
        sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s24le", os.path.join(PUBLIC, f"voz_{i}.wav")])
        ws = [{"w": w["w"], "ini": round(w["ini"] - corte0, 3), "fim": round(w["fim"] - corte0, 3), "p": w["p"]} for w in palavras]
        takes.append({"take": i, "arquivo": f"voz_{i}.wav", "dur": round(dur, 3), "fim_fala": round(fim - corte0, 3),
                      "corte": [round(corte0, 3), round(corte1, 3)], "lufs_medido": round(medido, 1), "ganho_db": round(ganho, 1),
                      "texto": " ".join(w["w"] for w in ws), "palavras": ws})
        print(f"take {i}: {dur:.2f} s · {medido:.1f} → {alvo} LUFS · {takes[-1]['texto']}")
    salvar_json("voz.json", takes)


# ------------------------------------------------------------------ linha do tempo

def linha_do_tempo(d, takes):
    pausas = d["narracao"]["pausas"]
    t = d["narracao"]["inicio"]
    for i, tk in enumerate(takes):
        tk["t0"] = round(t, 3)
        t += tk["dur"] + (pausas[i] if i < len(pausas) else 0)
    return takes


def resolver(ancora, takes, planos_ini=None):
    """Âncora → ms na linha do tempo."""
    m = re.fullmatch(r"(.+?)([+-]\d+)?", ancora.strip())
    base, desloc = m.group(1), int(m.group(2) or 0)
    if planos_ini is not None and base in planos_ini:
        return planos_ini[base] + desloc
    palavra, take = base.split("@")
    tk = takes[int(take) - 1]
    if palavra == "fim":
        return round((tk["t0"] + tk["fim_fala"]) * 1000) + desloc
    n = 1
    if "#" in palavra:
        palavra, n = palavra.split("#")
        n = int(n)
    # na âncora o acento conta ("e" ≠ "é"); só a pontuação e a caixa saem
    exata = lambda p: re.sub(r"[^\w]", "", p.lower())
    achadas = [w for w in tk["palavras"] if exata(w["w"]) == exata(palavra)]
    if len(achadas) < n:
        sys.exit(f"âncora sem palavra: {ancora} (take {take}: {tk['texto']})")
    return round((tk["t0"] + achadas[n - 1]["ini"]) * 1000) + desloc


def legendas(d, takes):
    """Grupos do rev1.json → tempos das palavras ditas. A legenda é a fala, então cada palavra do grupo tem de
    bater com a transcrição (sem acento e pontuação); diferença = erro."""
    padrao, emocional = [], None
    for bloco in d["legendas"]:
        tk = takes[bloco["take"] - 1]
        ws = tk["palavras"]
        k = 0
        itens = []
        for g in bloco["grupos"]:
            emo = isinstance(g, dict)
            texto = g["emocional"] if emo else g
            toks = [x for x in re.split(r"[\s|]+", texto.replace("*", "")) if x]
            ini = ws[k]["ini"]
            tempos = []
            for tok in toks:
                if norm(tok) != norm(ws[k]["w"]):
                    sys.exit(f"legenda ≠ fala no take {bloco['take']}: '{tok}' × '{ws[k]['w']}'")
                tempos.append(round((tk["t0"] + ws[k]["ini"]) * 1000))
                k += 1
            itens.append({"texto": texto, "ini": ini, "emo": emo, "ultima": ws[k - 1]["fim"], "palavras": tempos})
        if k != len(ws):
            sys.exit(f"take {bloco['take']}: sobraram palavras sem legenda: {' '.join(w['w'] for w in ws[k:])}")
        for j, it in enumerate(itens):
            fim = itens[j + 1]["ini"] if j + 1 < len(itens) else min(tk["dur"], it["ultima"] + 0.25)
            ini_ms = round((tk["t0"] + it["ini"]) * 1000)
            fim_ms = round((tk["t0"] + fim) * 1000)
            if it["emo"]:
                emocional = {"texto": it["texto"], "ini": ini_ms, "fim": fim_ms}
            else:
                padrao.append({"texto": it["texto"], "ini": ini_ms, "fim": fim_ms, "palavras": it["palavras"]})
    return padrao, emocional


def montar_planos(d, takes, fps):
    """Início de cada plano (cortes 2 quadros antes da palavra), fim = início do próximo."""
    antecipa = round(2 * 1000 / fps)
    ini = {}
    for p in d["planos"]:
        ms = resolver(p["em"], takes, ini)
        if not re.search(r"\+\d+$", p["em"]):
            ms -= antecipa
        ini[p["id"]] = max(0, ms)
    planos = []
    for i, p in enumerate(d["planos"]):
        a = ini[p["id"]]
        b = ini[d["planos"][i + 1]["id"]] if i + 1 < len(d["planos"]) else a + round(p["dur"] * 1000)
        q = dict(p, ini=a, fim=b)
        planos.append(q)
    return planos, ini


# ------------------------------------------------------------------ planos (imagem)

def quadro(fonte, t):
    from PIL import Image

    if fonte.startswith("foto"):
        return Image.open(os.path.join(FONTE, f"{fonte}.jpg")).convert("RGB")
    arq = os.path.join(TMP, "quadros", f"{fonte}_{t:.3f}.png")
    if not os.path.exists(arq):
        os.makedirs(os.path.dirname(arq), exist_ok=True)
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", os.path.join(FONTE, f"{fonte}.MOV"), "-vf", TONEMAP + ",format=rgb24",
            "-frames:v", "1", arq])
    return Image.open(arq).convert("RGB")


def caixa(cx, cy, w, W, H):
    h = w * 16 / 9
    b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    if b[0] < -0.5 or b[1] < -0.5 or b[2] > W + 0.5 or b[3] > H + 0.5:
        sys.exit(f"recorte fora do quadro: {cx},{cy},{w} em {W}×{H}")
    return b


def foto(p, W, H, destino):
    from PIL import Image, ImageFilter

    im = quadro(p["fonte"], p.get("t", 0))
    b = caixa(*p["recorte"], im.width, im.height)
    out = im.resize((W, H), Image.LANCZOS, box=b)
    if W / (b[2] - b[0]) > 1.2:  # foto do WhatsApp ampliada 1,5×: nitidez leve
        out = out.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    out.save(destino, quality=95)


def video_estavel(p, dur, W, H, destino, fps_fonte=24):
    """Tripé digital: mede a translação da cena quadro a quadro e move o recorte junto com ela. A câmera fica
    parada; barco, água e nuvens continuam se mexendo."""
    import cv2
    from PIL import Image

    src = os.path.join(FONTE, f"{p['fonte']}.MOV")
    SW, SH = 3840, 2160
    nq = int(np.ceil(dur * fps_fonte)) + 2
    x0, y0, x1, y1 = p["estabilizar"]
    cx, cy, w = p["recorte"]
    h = w * 16 / 9

    def quadros():
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{p['t']:.3f}", "-i", src, "-vf", TONEMAP + ",format=rgb24", "-frames:v", str(nq),
                                "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        while True:
            buf = dec.stdout.read(SW * SH * 3)
            if len(buf) < SW * SH * 3:
                break
            yield np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
        dec.wait()

    # 1ª passada: caminho da cena por pontos rastreados (Lucas-Kanade, mediana dos deslocamentos: barco,
    # gente e água não puxam a medida) na faixa `estabilizar`, em volta da janela do recorte
    anterior = pts = None
    dx = dy = 0.0
    caminho = []
    for fr in quadros():
        cinza = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY), (SW // 2, SH // 2), interpolation=cv2.INTER_AREA)
        if anterior is not None and pts is not None and len(pts) >= 30:
            novos, st, _ = cv2.calcOpticalFlowPyrLK(anterior, cinza, pts, None, winSize=(31, 31), maxLevel=3)
            ok = st[:, 0] == 1
            d = (novos[ok] - pts[ok]).reshape(-1, 2)
            mx, my = np.median(d, 0)
            dx += mx * 2
            dy += my * 2
            # fica só com os pontos que andaram junto com a mediana (os da cena parada)
            boa = np.hypot(d[:, 0] - mx, d[:, 1] - my) < 1.0
            pts = novos[ok][boa].reshape(-1, 1, 2)
        if pts is None or len(pts) < 120:
            mascara = np.zeros_like(cinza)
            a0, a1 = int(max(x0, cx + dx - w / 2 - 160)) // 2, int(min(x1, cx + dx + w / 2 + 160)) // 2
            b0, b1 = int(max(0, y0 + dy)) // 2, int(min(SH, y1 + dy)) // 2
            mascara[b0:b1, a0:a1] = 255
            pts = cv2.goodFeaturesToTrack(cinza, 500, 0.01, 12, mask=mascara)
        anterior = cinza
        caminho.append((dx, dy))
    c = np.array(caminho)

    # 2ª passada: recorte que acompanha a cena
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps_fonte), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709", destino], stdin=subprocess.PIPE)
    encostou = 0
    for n, fr in enumerate(quadros()):
        ddx, ddy = c[min(n, len(c) - 1)]
        bx = min(max(cx + ddx - w / 2, 0), SW - w)
        by = min(max(cy + ddy - h / 2, 0), SH - h)
        if abs(bx - (cx + ddx - w / 2)) > 1 or abs(by - (cy + ddy - h / 2)) > 1:
            encostou += 1
        im = Image.fromarray(fr).resize((W, H), Image.LANCZOS, box=(bx, by, bx + w, by + h))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    enc.wait()
    print(f"  {p['id']}: {len(c)} quadros, deslocamento da cena ({c[-1][0]:.0f}, {c[-1][1]:.0f}) px (4K)")
    if encostou:
        sys.exit(f"recorte de {p['id']} encostou na borda em {encostou} quadros: a cena escorregaria; ajuste `recorte`")
    return c.round(1).tolist()


def planos():
    d = carregar()
    W, H, fps = d["largura"], d["altura"], d["fps"]
    takes = linha_do_tempo(d, ler_json("voz.json"))
    lista, _ = montar_planos(d, takes, fps)
    os.makedirs(PUBLIC, exist_ok=True)
    for p in lista:
        dur = (p["fim"] - p["ini"]) / 1000
        if p["tipo"] == "foto":
            foto(p, W, H, os.path.join(PUBLIC, f"plano_{p['id']}.jpg"))
            print(f"plano {p['id']}: foto ({dur:.2f} s)")
        elif p["tipo"] == "video":
            video_estavel(p, dur + 0.15, W, H, os.path.join(PUBLIC, f"plano_{p['id']}.mp4"))


# ------------------------------------------------------------------ sons

def sintese(nome, sr=SR):
    """Efeitos do desenho (só deste Reel; não são sons da marca). Síntese determinística, como design-system/sons/gerar_sons.py."""
    rng = np.random.default_rng({"rangido": 7, "tuc": 11, "estaca": 13, "roldana": 17}[nome])
    t = lambda s: np.arange(int(s * sr)) / sr
    if nome == "tuc":  # nó de madeira batendo em tijolo: ressonância curta 190 Hz + clique
        tt = t(0.16)
        x = 0.9 * np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 38) + 0.35 * np.sin(2 * np.pi * 520 * tt) * np.exp(-tt * 70)
        x[: int(0.004 * sr)] += rng.normal(0, 0.6, int(0.004 * sr))
    elif nome == "estaca":  # estaca entrando na lama: baque grave abafado
        tt = t(0.32)
        f = 70 + 40 * np.exp(-tt * 20)
        x = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 14)
        ruido = rng.normal(0, 1, len(tt))
        ruido = np.convolve(ruido, np.ones(60) / 60, mode="same")
        x += 2.2 * ruido * np.exp(-tt * 25)
    elif nome == "rangido":  # madeira rangendo: pulsos de atrito (stick-slip) a 38→22 Hz filtrados em 700 Hz
        tt = t(0.62)
        taxa = 38 - 16 * tt / tt[-1]
        fase = np.cumsum(taxa) / sr
        pulsos = (np.diff(np.floor(fase), prepend=0) > 0).astype(float)
        idx = np.where(pulsos > 0)[0]
        x = np.zeros_like(tt)
        for i in idx:
            n = min(len(tt) - i, int(0.02 * sr))
            k = np.arange(n) / sr
            x[i:i + n] += np.sin(2 * np.pi * (650 + 120 * rng.random()) * k) * np.exp(-k * 260)
        x *= np.sin(np.pi * tt / tt[-1]) ** 0.6
    else:  # roldana: corda passando na polia, rangido agudo curto repetido
        tt = t(0.9)
        x = np.zeros_like(tt)
        for k0 in np.arange(0.0, 0.78, 0.14):
            i = int(k0 * sr)
            n = min(int(0.09 * sr), len(tt) - i)
            k = np.arange(n) / sr
            f = 1300 + 500 * k / k[-1]
            x[i:i + n] += np.sin(2 * np.pi * np.cumsum(f) / sr) * np.sin(np.pi * k / k[-1]) * 0.5
        ruido = np.convolve(rng.normal(0, 1, len(tt)), np.ones(12) / 12, mode="same")
        x += 0.25 * ruido * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt))
        x *= np.minimum(1, tt / 0.05) * np.minimum(1, (tt[-1] - tt) / 0.12)
    x = x / (np.abs(x).max() + 1e-9) * 0.7
    return x.astype(np.float32)


def salvar_wav(arq, x, sr=SR):
    import soundfile as sf

    sf.write(arq, x, sr, subtype="PCM_24")


def ambiente_de(p):
    """Fonte do som ambiente de um plano: o próprio clipe, ou o Amstel (IMG_1403) nas fotos."""
    if p["fonte"].startswith("foto"):
        return "IMG_1403", 0.5
    return p["fonte"], p.get("t", 0)


def sons():
    d = carregar()
    takes = linha_do_tempo(d, ler_json("voz.json"))
    lista, _ = montar_planos(d, takes, d["fps"])
    niveis = {}
    for nome in ("tuc", "estaca", "rangido", "roldana"):
        x = sintese(nome)
        salvar_wav(os.path.join(PUBLIC, f"sfx_{nome}.wav"), x)
        niveis[nome] = round(lufs_50ms(x), 1)
        print(f"sfx {nome}: {len(x) / SR:.2f} s · {niveis[nome]} LUFS (50 ms)")
    alvo = d["mix"]["ambiente_lufs"]
    amb = {}
    for p in lista:
        if p["tipo"] == "desenho":
            continue
        fonte, t = ambiente_de(p)
        dur = (p["fim"] - p["ini"]) / 1000 + 0.3
        src = os.path.join(FONTE, f"{fonte}.MOV")
        total = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capturar=True).stdout)
        t = max(0.0, min(t, total - dur)) if total > dur else 0.0
        x = decodificar(src, canais=2)[int(t * SR):int((t + dur) * SR)]
        if len(x) < int(dur * SR):  # clipe curto: completa em espelho
            x = np.concatenate([x, x[::-1]])[: int(dur * SR)]
        bruto = os.path.join(TMP, f"amb_{p['id']}_bruto.wav")
        salvar_wav(bruto, x)
        # vento: corta graves (< 140 Hz) e o chiado de cima
        filtrado = os.path.join(TMP, f"amb_{p['id']}_f.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", "highpass=f=140,lowpass=f=9000", "-c:a", "pcm_s24le", filtrado])
        y = decodificar(filtrado, canais=2)
        rms = np.sqrt(np.mean(y ** 2) + 1e-12)
        ganho = 10 ** ((alvo + 3 - 20 * np.log10(rms)) / 20)  # RMS ≈ LUFS + 3 dB num ruído de rua (só para trechos < 0,4 s, sem bloco de LUFS)
        y = np.clip(y * ganho, -1, 1)
        n = int(0.04 * SR)
        y[:n] *= np.linspace(0, 1, n)[:, None]
        y[-n:] *= np.linspace(1, 0, n)[:, None]
        salvar_wav(os.path.join(PUBLIC, f"amb_{p['id']}.wav"), y)
        amb[p["id"]] = {"fonte": fonte, "t": round(t, 2)}
    salvar_json("sons.json", {"sfx": niveis, "ambiente": amb})


# ------------------------------------------------------------------ props

def props():
    d = carregar()
    fps = d["fps"]
    takes = linha_do_tempo(d, ler_json("voz.json"))
    sj = ler_json("sons.json")
    with open(SONS_DS, encoding="utf-8") as f:
        ds = json.load(f)
    lista, ini = montar_planos(d, takes, fps)
    leg, emo = legendas(d, takes)
    voz_lufs = d["mix"]["voz_lufs"]

    # planos reais ≤ 3 s (pedido do Diego)
    for p in lista:
        dur = (p["fim"] - p["ini"]) / 1000
        if p["tipo"] != "desenho" and dur > 3.0 + 1e-6:
            sys.exit(f"plano {p['id']} com {dur:.2f} s: passa de 3 s")

    eventos = {}
    for k, v in d["eventos"].items():
        eventos[k] = [resolver(a, takes, ini) for a in v] if isinstance(v, list) else resolver(v, takes, ini)

    def ganho_som(nome, rel):
        if nome in sj["sfx"]:
            return voz_lufs + rel - sj["sfx"][nome]
        return voz_lufs + rel - ds[f"PD_{nome}_v1.wav"]["lufs_50ms"]

    sons_ = []
    for s in d["sons"]:
        em = resolver(s["em"], takes, ini)
        g = ganho_som(s["nome"], s["rel_db"])
        sons_.append({"nome": s["nome"], "em": em, "volume": round(min(1.0, 10 ** (g / 20)), 4), "ds": s["nome"] not in sj["sfx"], "motivo": s["motivo"]})
    sons_.sort(key=lambda s: s["em"])
    for a, b in zip(sons_[:-1], sons_[1:]):
        if b["em"] - a["em"] < 1500:
            print(f"  aviso: {a['nome']} ({a['em']} ms) e {b['nome']} ({b['em']} ms) a menos de 1,5 s (DS 4.6)")

    cta = next(p for p in lista if p["id"] == "cta")
    props_ = {
        "fps": fps, "largura": d["largura"], "altura": d["altura"],
        "duracao": cta["fim"],
        "planos": [{k: p[k] for k in ("id", "tipo", "ini", "fim") } | ({"desenho": p["desenho"]} if p["tipo"] == "desenho" else {"arquivo": f"plano_{p['id']}.{'mp4' if p['tipo'] == 'video' else 'jpg'}"})
                   | ({"transicao": p["transicao"]} if "transicao" in p else {}) for p in lista],
        "eventos": eventos,
        "legendas": leg,
        "emocional": emo,
        "informacao": [{"rotulo": i["rotulo"], "numero": i["numero"], "ini": resolver(i["em"], takes, ini), "fim": resolver(i["fim"], takes, ini)} for i in d["informacao"]],
        "capa": {k: v for k, v in d["capa"].items() if k != "plano"} | {"arquivo": f"plano_{d['capa']['plano']}.jpg"},
        "cta": {k: d["cta"][k] for k in ("rotulo", "destino", "modulo", "tamanho")} | {"ini": cta["ini"]},
        "voz": [{"arquivo": tk["arquivo"], "ini": round(tk["t0"] * 1000), "dur": round(tk["dur"] * 1000)} for tk in takes],
        "ambientes": [{"arquivo": f"amb_{p['id']}.wav", "ini": p["ini"], "fim": p["fim"], "cinema": p.get("transicao") == "cinema"}
                      for p in lista if p["tipo"] != "desenho"],
        "sons": sons_,
        "mix": d["mix"],
    }
    salvar_json("props.json", props_)
    print(f"duração: {props_['duracao'] / 1000:.2f} s · {len(lista)} planos · {len(leg)} grupos de legenda")
    for p in lista:
        print(f"  {p['ini'] / 1000:6.2f}–{p['fim'] / 1000:6.2f}  {(p['fim'] - p['ini']) / 1000:4.2f} s  {p['id']:<11} {p['tipo']}")


# ------------------------------------------------------------------ render, master, capa, folha

def remotion(args):
    cmd = ["npx", "remotion", *args, f"--public-dir={PUBLIC}", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    remotion(["render", "src/index.ts", "CasasTortas", SAIDA_BRUTA, f"--props={os.path.join(TMP, 'props.json')}",
              "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--concurrency=4"])


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])


def master():
    """Ganho linear até −14 LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP), como no Madrid."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(SAIDA_BRUTA)
    ganho, teto = alvo - i0, pico - 0.4
    for _ in range(5):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", SAIDA])
        i, tp = medir_master(SAIDA)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS · pico {tp:.1f} dBTP → {os.path.basename(SAIDA)}")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "slow",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])


def capa():
    remotion(["still", "src/index.ts", "CapaCasasTortas", CAPA, f"--props={os.path.join(TMP, 'props.json')}", "--image-format=jpeg", "--jpeg-quality=92"])


def folha():
    """Folha de quadros: 1 quadro a cada 1,5 s com o tempo, para a QA."""
    pasta = os.path.join(AQUI, "qa_frames")
    os.makedirs(pasta, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
        "fps=2/3,scale=270:480,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=8x5",
        "-frames:v", "1", os.path.join(pasta, "folha_rev1.jpg")])


if __name__ == "__main__":
    etapas = {"voz": [voz], "planos": [planos], "sons": [sons], "props": [props], "render": [render], "master": [master],
              "capa": [capa], "folha": [folha], "tudo": [voz, planos, sons, props, render, master, capa, folha]}
    for etapa in sys.argv[1:] or ["tudo"]:  # várias etapas em sequência: python3 rev1.py props render master
        for fn in etapas[etapa]:
            print(f"== {fn.__name__}")
            fn()
