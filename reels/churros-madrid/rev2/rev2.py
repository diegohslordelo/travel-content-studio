#!/usr/bin/env python3
"""Reel "Churros em Madrid: será que vale?" (Chocolatería San Ginés) · REV2.

A REV1 com a narração gravada pelo Diego (12 gravações enviadas à pasta Madrid em 21/10/2026), a voz
original da Marina ("Nada demais, gente.", IMG_3821) sincronizada com a imagem, rufada de tambor antes
dela e trilha de fundo ("Bossa Antigua", Kevin MacLeod, CC BY 4.0) que para no tambor e volta no veredito.

Pipeline (rode de dentro desta pasta):
    python3 rev2.py preparar   # cenas em _tmp/public (corte, HLG→SDR, recorte 9:16, cor) + sons sintetizados
    python3 rev2.py render     # Remotion monta a imagem (design-system/remotion, composição "ReelChurros"), sem áudio
    python3 rev2.py mixar      # narração + voz da Marina + tambor + trilha + efeitos, nos tempos das cenas
    python3 rev2.py master     # vídeo final (−14 LUFS, pico ≤ −1 dBTP), versão sem trilha, faixas separadas e prévia
    python3 rev2.py capa       # capa 1080 × 1920
    python3 rev2.py qa         # folha de contato em qa_frames/
    python3 rev2.py tudo

Entradas: rev2.json (decisões), os brutos de Madrid em ../fonte/, as gravações em ../fonte/narracao/ e a trilha
em ../fonte/trilha/ (tudo fora do git; os IDs do Drive e a URL da trilha estão em rev2.json).
Só usa a biblioteca padrão do Python, ffmpeg e Node.

Áudio dos clipes: só entra o trecho da Marina (IMG_3821, `voz_original` em rev2.json). As cenas de vídeo são
exportadas com -an; nenhum outro som dos clipes chega ao vídeo.
"""
import json
import math
import os
import random
import re
import struct
import subprocess
import sys
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_bruto.mov")
SAIDA = os.path.join(AQUI, "reel_churros-madrid_rev2.mp4")
SAIDA_MUDA = os.path.join(AQUI, "reel_churros-madrid_rev2_sem_audio.mp4")
SAIDA_PREVIA = os.path.join(AQUI, "reel_churros-madrid_rev2_previa.mp4")
SAIDA_SEM_TRILHA = os.path.join(AQUI, "reel_churros-madrid_rev2_sem_trilha.mp4")
MIX = os.path.join(TMP, "mix.wav")
FAIXAS = os.path.join(AQUI, "faixas")
CAPA = os.path.join(AQUI, "capa_churros-madrid_rev2.jpg")
QA = os.path.join(AQUI, "qa_frames")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# Tamanho das cenas preparadas: a largura nativa do recorte 9:16 de um quadro 3840 × 2160 (1215 px),
# arredondada para par. A composição (1080 × 1920) reduz, o que dá folga para a câmera virtual.
CW, CH = 1216, 2160

# Brutos do iPhone em HLG/BT.2020. O tonemap HLG do madrid-show deixa a pele e o churro alaranjados
# sob a luz quente da chocolateria; converter só primárias e matriz (BT.2020 → BT.709, curva tratada
# como SDR) mantém a cor natural (comparação em qa_frames/cor_conversao.jpg: original, escolhida, tonemap).
CONVERSAO = "zscale=min=bt2020nc:pin=bt2020:tin=bt709:rin=tv:m=bt709:p=bt709:t=bt709:r=tv"
# Cor por tipo de plano: comida um pouco mais quente e densa (dourado do churro, chocolate);
# rua só um toque de contraste. Ajustes leves, sem mudar a cor natural.
GRADE = {
    # dentro da San Ginés a luz é de lâmpada quente: corrige a temperatura de cor para a pele não ficar laranja
    "interior": "colortemperature=temperature=10000:mix=0.9,eq=contrast=1.04:saturation=0.88",
    "comida": "colorbalance=rm=-0.01:bm=0.01,eq=contrast=1.05:saturation=1.02",
    "rua": "eq=contrast=1.04:saturation=1.04",
}


def sh(cmd, capturar=False):
    txt = " ".join(cmd)
    print("  $", txt if len(txt) < 240 else txt[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev2.json"), encoding="utf-8") as f:
        return json.load(f)


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def expr_suave(pontos):
    """v(t): interpolação smoothstep entre os pontos [t, v] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return f"{pontos[0][1]:.2f}"
    e = f"{pontos[-1][1]:.2f}"
    for (t0, v0), (t1, v1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max((t-{t0})/({t1}-{t0}),0),1)"
        e = f"if(lt(t,{t1}),({v0:.2f}+({v1:.2f}-{v0:.2f})*{p}*{p}*(3-2*{p})),{e})"
    return e


def preparar():
    d = carregar()
    fps = d["fps"]
    os.makedirs(PUBLIC, exist_ok=True)
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Fonte ausente em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    cenas = []
    for c in d["cenas"]:
        if c.get("grafico"):
            n = round(c["dur"] * fps)
            cenas.append(dict(c, quadros=n, dur=n / fps))
            continue
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        # gravado na horizontal com metadado de giro errado (−90): gira 90° depois da autorrotação
        extra_giro = ["transpose=clock"] if f.get("girar") == "horario" else []
        # dimensões depois dos giros: a autorrotação do ffmpeg troca largura e altura em ±90°, e o giro extra troca de novo
        w0, h0 = sonda(src)
        if rotacao_meta(src) in (90, -90, 270, -270):
            w0, h0 = h0, w0
        if extra_giro:
            w0, h0 = h0, w0
        n_corte = round((c["out"] - c["in"]) * fps)
        n_cong = round(c.get("congelar", 0) * fps)
        ch = round(h0 / c.get("zoom", 1.0) / 2) * 2
        cw = round(ch * CW / CH / 2) * 2
        if cw > w0:  # plano já vertical: o recorte 9:16 não pode passar da largura
            cw = w0 - w0 % 2
            ch = round(cw * CH / CW / 2) * 2
        # x do recorte: o centro (fração da largura) vira a borda esquerda, presa dentro do quadro
        xs = [[t, min(max(cx * w0 - cw / 2, 0), w0 - cw)] for t, cx in c["x"]]
        y = min(max(c.get("y", 0.5) * h0 - ch / 2, 0), h0 - ch)
        vel = c.get("velocidade", 1.0)
        n_corte = round((c["out"] - c["in"]) / vel * fps)
        vf = [
            *extra_giro,
            CONVERSAO,
            f"crop=w={cw}:h={ch}:x='{expr_suave(xs)}':y={y:.0f}",
            f"scale={CW}:{CH}:flags=lanczos",
            GRADE[c["grade"]],
        ]
        if vel != 1.0:
            # câmera lenta só em plano de fundo com movimento lento (bandeja atrás da pergunta final)
            vf.append(f"setpts=PTS/{vel}")
        vf.append(f"fps={fps}")
        if n_cong:
            vf.append(f"tpad=stop_mode=clone:stop_duration={n_cong / fps:.4f}")
        vf.append("format=yuv420p,setsar=1")
        arq = f"cena_{c['id']}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(n_corte + n_cong),
               "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "12", "-pix_fmt", "yuv420p",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq)]
        # cache: só re-codifica se o comando da cena mudou
        marca = os.path.join(PUBLIC, arq + ".cmd")
        if not (os.path.exists(marca) and open(marca).read() == " ".join(cmd) and os.path.exists(os.path.join(PUBLIC, arq))):
            sh(cmd)
            open(marca, "w").write(" ".join(cmd))
        n = n_corte + n_cong
        cenas.append(dict(c, arquivo=arq, quadros=n, dur=n / fps))
        print(f"cena {c['id']}: {n} quadros ({n / fps:.3f} s) · recorte {cw}×{ch}")

    # contornos do globo
    sh(["cp", os.path.join(AQUI, "geo", "mundo.json"), os.path.join(PUBLIC, "mundo.json")])
    sons()

    props = dict(d, cenas=cenas)
    props["duracao"] = sum(c["dur"] for c in cenas)
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {props['duracao']:.3f} s · {sum(c['quadros'] for c in cenas)} quadros · props em _tmp/props.json")


# ---------------------------------------------------------------- desenho de som (opcional)
SR = 48000


def _grava(nome, amostras):
    pico = max(1e-9, max(abs(a) for a in amostras))
    k = 0.5 / pico  # pico em −6 dBFS: o volume final é decidido na composição
    with wave.open(os.path.join(PUBLIC, nome), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, a * k)) * 32767)) for a in amostras))


def _ruido_filtrado(dur, f0, f1, env, semente):
    """Ruído branco por um passa-banda de 2 polos com centro varrendo f0 → f1 (exponencial)."""
    rnd = random.Random(semente)
    n = int(dur * SR)
    out = []
    y1 = y2 = 0.0
    for i in range(n):
        p = i / n
        fc = f0 * (f1 / f0) ** p
        r = 0.985
        a1 = -2 * r * math.cos(2 * math.pi * fc / SR)
        a2 = r * r
        x = rnd.uniform(-1, 1)
        y = (1 - r) * x - a1 * y1 - a2 * y2
        y2, y1 = y1, y
        out.append(y * env(p))
    return out


def sons():
    # whoosh curto (transições): sobe e cai em 420 ms
    _grava("sfx_whoosh.wav", _ruido_filtrado(0.42, 380, 3200, lambda p: math.sin(math.pi * p) ** 1.6, 1))
    # whoosh grave (mergulho no chocolate → globo)
    _grava("sfx_mergulho.wav", _ruido_filtrado(0.75, 1800, 160, lambda p: (1 - p) ** 1.2 * min(1, p * 10), 2))
    # avião passando (rota): ruído grave com crescendo e efeito Doppler, 2,6 s
    av = _ruido_filtrado(2.6, 900, 420, lambda p: math.sin(math.pi * min(1, p * 1.15)) ** 2, 3)
    av = [a + 0.18 * math.sin(2 * math.pi * (140 - 40 * i / len(av)) * i / SR) * math.sin(math.pi * i / len(av)) ** 2 for i, a in enumerate(av)]
    _grava("sfx_aviao.wav", av)
    # pop de texto: senoide 880 → 660 Hz com decaimento de 70 ms
    _grava("sfx_pop.wav", [math.sin(2 * math.pi * (880 - 220 * i / 4800) * i / SR) * math.exp(-i / (0.018 * SR)) for i in range(4800)])
    # pino em Barcelona: dois toques limpos (1320 e 1760 Hz)
    pin = [0.0] * int(0.5 * SR)
    for atraso, f in ((0, 1320), (0.09, 1760)):
        o = int(atraso * SR)
        for i in range(int(0.4 * SR)):
            pin[o + i] += 0.6 * math.sin(2 * math.pi * f * i / SR) * math.exp(-i / (0.08 * SR))
    _grava("sfx_pin.wav", pin)
    # baque do veredito: 52 Hz com decaimento + estalo
    tum = [math.sin(2 * math.pi * (70 - 18 * min(1, i / (0.12 * SR))) * i / SR) * math.exp(-i / (0.16 * SR)) for i in range(int(0.7 * SR))]
    rnd = random.Random(4)
    for i in range(int(0.006 * SR)):
        tum[i] += rnd.uniform(-0.6, 0.6) * (1 - i / (0.006 * SR))
    _grava("sfx_tum.wav", tum)
    print("  sons: sfx_whoosh, sfx_mergulho, sfx_aviao, sfx_pop, sfx_pin, sfx_tum (sintetizados)")


# ---------------------------------------------------------------- render e entregas
def _remotion(args):
    cmd = ["npx", "remotion", *args, "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    props = os.path.join(TMP, "props.json")
    _remotion(["render", "src/index.ts", "ReelChurros", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
               "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--concurrency=4"])


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


# ---------------------------------------------------------------- mixagem (narração, Marina, tambor, trilha, efeitos)
def tambor(dur, nome, semente=7):
    """Rufada de caixa crescente (som autoral, sintetizado aqui): golpes que aceleram de 12 para 28 por segundo e
    crescem em volume, sobre o chiado da esteira. Termina seco, com fade de 12 ms, para não invadir a fala seguinte."""
    rnd = random.Random(semente)
    n = int(dur * SR)
    out = [0.0] * n
    t = 0.0
    k = 0
    while t < dur - 0.03:
        p = t / dur
        vel = (0.10 + 0.90 * p ** 2.0) * (0.88 + 0.24 * rnd.random())
        ini = int(t * SR)
        f = 182 + 12 * (k % 2)  # as duas mãos soam um pouco diferentes
        for i in range(int(0.09 * SR)):
            j = ini + i
            if j >= n:
                break
            tt = i / SR
            out[j] += vel * (0.8 * rnd.uniform(-1, 1) * math.exp(-tt / 0.026) + 0.45 * math.sin(2 * math.pi * f * tt) * math.exp(-tt / 0.016))
        t += (1 / (12 + 16 * p ** 1.3)) * (1 + rnd.uniform(-0.06, 0.06))
        k += 1
    # esteira: chiado contínuo que cresce junto
    for i in range(n):
        out[i] += 0.10 * (i / n) ** 2 * rnd.uniform(-1, 1)
    # passa-altas leve (a caixa vive nos médios-agudos) e fade final curtíssimo
    y, ant = 0.0, 0.0
    for i in range(n):
        x = out[i]
        y = 0.97 * (y + x - ant)
        ant = x
        out[i] = y
    for i in range(int(0.012 * SR)):
        out[n - 1 - i] *= i / (0.012 * SR)
    _grava(nome, out)


def _lufs(arq, ini=None, fim=None):
    cmd = ["ffmpeg", "-hide_banner", "-nostats"]
    if ini is not None:
        cmd += ["-ss", f"{ini:.3f}", "-to", f"{fim:.3f}"]
    r = subprocess.run(cmd + ["-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def _clipe_voz(src, ini, fim, alvo, nome, medir=None, fade_in=0.01, fade_out=0.05):
    """Recorta a fala, tira o grave de manuseio (passa-altas 80 Hz) e iguala a loudness ao alvo.
    `medir` = (ini, fim) do trecho que define o ganho (ex.: só a fala da Marina, sem o ambiente)."""
    bruto = os.path.join(TMP, "audio", "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-to", f"{fim:.3f}", "-i", src, "-vn", "-ac", "2", "-ar", str(SR), "-af", "highpass=f=80", "-c:a", "pcm_s24le", bruto])
    medido = _lufs(bruto, *(medir if medir else (None, None)))
    ganho = alvo - medido
    dur = fim - ini
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", f"volume={ganho:.2f}dB,afade=t=in:d={fade_in},afade=t=out:st={max(0, dur - fade_out):.3f}:d={fade_out}",
        "-c:a", "pcm_s24le", os.path.join(TMP, "audio", nome)])
    print(f"  {nome}: {medido:.1f} → {alvo} LUFS ({ganho:+.1f} dB)")
    return os.path.join(TMP, "audio", nome)


def eventos_audio():
    """Monta a lista de eventos (arquivo, início global, ganho, grupo) a partir das cenas medidas em props.json."""
    d = carregar()
    props = json.load(open(os.path.join(TMP, "props.json"), encoding="utf-8"))
    ini = {}
    acc = 0.0
    for c in props["cenas"]:
        ini[c["id"]] = acc
        acc += c["quadros"] / props["fps"]
    total = acc
    cena = {c["id"]: c for c in props["cenas"]}
    os.makedirs(os.path.join(TMP, "audio"), exist_ok=True)
    ev = []
    pasta_n = os.path.join(FONTE, "narracao")

    # narração do Diego (as gravações originais, só recortadas no começo e no fim)
    fala = []
    for n in d["narracao"]:
        arq = _clipe_voz(os.path.join(pasta_n, n["arquivo"]), n["in"], n["out"], d["mix"]["voz_lufs"], f"{n['id']}.wav")
        t0 = ini[n["cena"]] + n["t"]
        ev.append({"arq": arq, "t": t0, "db": 0, "grupo": "voz"})
        fala.append((t0, t0 + n["out"] - n["in"], n["id"]))
    fala.sort()
    for (a0, a1, ia), (b0, b1, ib) in zip(fala, fala[1:]):
        if a1 > b0 + 0.01:
            sys.exit(f"falas se sobrepõem: {ia} termina em {a1:.2f} s e {ib} começa em {b0:.2f} s")

    # voz original da Marina, sincronizada com a imagem: a posição vem do próprio corte do vídeo
    v = d["voz_original"]
    c = cena[v["cena"]]
    t_marina = ini[v["cena"]] + (v["in"] - c["in"])
    src = os.path.join(FONTE, d["fontes"][v["fonte"]]["arquivo"])
    # o ganho é medido só sobre a fala dela (6,78–7,62 s); o ambiente e a reação vêm junto, no mesmo ganho
    arq = _clipe_voz(src, v["in"], v["out"], d["mix"]["marina_lufs"], "marina.wav", medir=(6.78 - v["in"], 7.62 - v["in"]), fade_in=0.03, fade_out=0.25)
    ev.append({"arq": arq, "t": t_marina, "db": 0, "grupo": "voz"})
    print(f"  Marina: bruto {v['in']:.2f}–{v['out']:.2f} s → vídeo {t_marina:.3f}–{t_marina + v['out'] - v['in']:.3f} s (sincronizado pelo corte)")

    # tambor: termina `folga` antes da voz dela
    tb = d["tambor"]
    t_tambor = t_marina - tb["folga"] - tb["dur"]
    tambor(tb["dur"], "tambor.wav")
    ev.append({"arq": os.path.join(PUBLIC, "tambor.wav"), "t": t_tambor, "db": d["mix"]["tambor_pico_db"] + 6, "grupo": "efeitos"})
    fim_fala_antes = max(f[1] for f in fala if f[1] <= t_marina)
    print(f"  tambor: {t_tambor:.3f}–{t_tambor + tb['dur']:.3f} s (última fala antes dele termina em {fim_fala_antes:.3f} s)")
    if fim_fala_antes > t_tambor + 0.02:
        sys.exit("a narração invade o tambor")

    # trilha: para no tambor e volta, do mesmo ponto, no veredito
    tr = d["trilha"]
    musica = os.path.join(FONTE, tr["arquivo"])
    ganho_m = tr["lufs_cama"] - _lufs(musica, 0, 60)
    corte = t_tambor + tr["pausa_fade_s"] / 2
    volta = ini[tr["volta_cena"]]
    resto = total - volta
    m1 = os.path.join(TMP, "audio", "trilha_1.wav")
    m2 = os.path.join(TMP, "audio", "trilha_2.wav")
    sh(["ffmpeg", "-v", "error", "-y", "-i", musica, "-t", f"{corte:.3f}", "-ac", "2", "-ar", str(SR),
        "-af", f"volume={ganho_m:.2f}dB,afade=t=out:st={corte - tr['pausa_fade_s']:.3f}:d={tr['pausa_fade_s']}", "-c:a", "pcm_s24le", m1])
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{corte:.3f}", "-i", musica, "-t", f"{resto:.3f}", "-ac", "2", "-ar", str(SR),
        "-af", f"volume={ganho_m:.2f}dB,afade=t=in:d={tr['volta_fade_s']},afade=t=out:st={resto - tr['fim_fade_s']:.3f}:d={tr['fim_fade_s']}", "-c:a", "pcm_s24le", m2])
    ev.append({"arq": m1, "t": 0.0, "db": 0, "grupo": "trilha"})
    ev.append({"arq": m2, "t": volta, "db": 0, "grupo": "trilha"})
    print(f"  trilha: 0–{corte:.2f} s, pausa até {volta:.2f} s (tambor + Marina + respiro), volta do ponto {corte:.2f} s da faixa")

    # efeitos sintetizados
    for e in d["efeitos_mix"]:
        ev.append({"arq": os.path.join(PUBLIC, e["arq"]), "t": max(0.0, ini[e["cena"]] + e["t"]), "db": e["db"], "grupo": "efeitos"})
    return ev, total


def _mixa(ev, total, saida):
    entradas, filtros, rotulos = [], [], []
    for i, e in enumerate(ev):
        entradas += ["-i", e["arq"]]
        ms = int(round(e["t"] * 1000))
        filtros.append(f"[{i}:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume={e['db']}dB,adelay={ms}|{ms}[a{i}]")
        rotulos.append(f"[a{i}]")
    filtros.append(f"{''.join(rotulos)}amix=inputs={len(ev)}:normalize=0:dropout_transition=0,apad,atrim=0:{total:.4f}[out]")
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[out]", "-c:a", "pcm_s24le", "-ar", str(SR), saida])


def mixar():
    ev, total = eventos_audio()
    _mixa(ev, total, MIX)
    os.makedirs(FAIXAS, exist_ok=True)
    for g in ("voz", "trilha", "efeitos"):
        _mixa([e for e in ev if e["grupo"] == g], total, os.path.join(FAIXAS, f"{g}_churros-madrid_rev2.wav"))
    _mixa([e for e in ev if e["grupo"] != "trilha"], total, os.path.join(TMP, "mix_sem_trilha.wav"))
    print(f"mix: {total:.3f} s → {os.path.relpath(MIX, AQUI)} + faixas/voz, trilha, efeitos")


def _masteriza(video, audio, saida):
    """Ganho linear até −14 LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP), como no madrid-show."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    ganho = alvo - _lufs(audio)
    teto = pico - 0.4
    for _ in range(4):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", "-movflags", "+faststart", saida])
        i, tp = medir(saida)
        if abs(i - alvo) <= 0.15 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"  {os.path.basename(saida)}: {i:.1f} LUFS · pico {tp:.1f} dBTP")


def master():
    _masteriza(SAIDA_BRUTA, MIX, SAIDA)
    _masteriza(SAIDA_BRUTA, os.path.join(TMP, "mix_sem_trilha.wav"), SAIDA_SEM_TRILHA)
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-map", "0:v", "-c:v", "copy", "-an", "-movflags", "+faststart", SAIDA_MUDA])
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "slow",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", SAIDA_PREVIA])


def capa():
    props = os.path.join(TMP, "props.json")
    _remotion(["still", "src/index.ts", "CapaChurros", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92"])


def qa():
    """Quadros representativos (2 por segundo) e folha de contato do vídeo inteiro."""
    os.makedirs(QA, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf",
        "fps=2,scale=270:480,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=10x7:padding=4",
        "-frames:v", "1", os.path.join(QA, "folha_de_contato.jpg")])


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"preparar": [preparar], "sons": [sons], "render": [render], "mixar": [mixar], "master": [master], "capa": [capa], "qa": [qa],
              "tudo": [preparar, render, mixar, master, capa, qa]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
