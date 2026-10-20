#!/usr/bin/env python3
"""Reel "As casas de Amsterdam são tortas de propósito" · REV3.

Pipeline (rode de dentro desta pasta):
    python3 rev3.py preparar   # cenas e áudios em _tmp/public (corte, giro, HLG→SDR, recorte 9:16, loudness)
    python3 rev3.py render     # Remotion monta o Reel (design-system/remotion, composição "Reel")
    python3 rev3.py master     # loudness do master: −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev3.py capa       # capa 1080 × 1920 (quadro estático com a placa)
    python3 rev3.py sem-data   # variante com o CTA "MANDA PRA QUEM VAI" (se o vlog não sair no sábado)
    python3 rev3.py tudo       # preparar → render → master → capa → sem-data

Entradas: rev3.json (decisões desta revisão) e os brutos em ../fonte/ (fora do git; baixar do Drive
pelo `drive_id` de cada fonte em rev3.json). Só usa a biblioteca padrão do Python, ffmpeg e Node.
"""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_amsterdam-casas-tortas_rev3.mp4")
CAPA = os.path.join(AQUI, "capa_amsterdam-casas-tortas_rev3.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius.
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False):
    print("  $", " ".join(cmd) if len(" ".join(cmd)) < 240 else " ".join(cmd)[:240] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar(bruto=False):
    """rev3.json; depois de `montar`, a montagem derivada (_tmp/montado.json), com cenas, áudio e legendas."""
    arq = os.path.join(TMP, "montado.json")
    if not bruto and os.path.exists(arq):
        arq_json = arq
    else:
        arq_json = os.path.join(AQUI, "rev3.json")
    with open(arq_json, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- montagem (fala decupada + ilustrações)

def montar():
    """Fala do Diego decupada e contínua; o Diego na câmera; as imagens entram na palavra que ilustram.

    1. Cada fala vira pedaços de voz (decupagem.py: corta os silêncios, nunca uma palavra), com a duração
       arredondada para quadros de 24 fps.
    2. Os pedaços são emendados em _tmp/voz.wav (fades de 8 ms nas emendas, que caem no silêncio).
    3. Imagem: o próprio clipe da fala, no mesmo ponto do áudio (sincronia labial), com o recorte fixo no rosto;
       por cima, as ilustrações de rev3.json, da palavra `de` até a palavra `ate` (ou o fim da fala).
    """
    import numpy as np
    sys.path.insert(0, AQUI)
    import decupagem

    d = carregar(bruto=True)
    fps = d["fps"]
    q = lambda t: round(t * fps) / fps  # noqa: E731
    pal_todas = json.load(open(os.path.join(AQUI, "transcricao_large-v3.json"), encoding="utf-8"))
    os.makedirs(PUBLIC, exist_ok=True)

    # 1. pedaços e linha do tempo
    pedacos, palavras, t = [], {}, 0.0
    energias = {}
    for f in d["falas"]:
        arq = d["fontes"][f["fonte"]]["arquivo"]
        if arq not in energias:
            energias[arq] = decupagem.energia(os.path.join(FONTE, arq))
        pal = [p for p in pal_todas[arq] if f["ini"] <= (p[0] + p[1]) / 2 < f["fim"]]  # a palavra é da fala se o meio dela cai dentro
        ped, _, _ = decupagem.pedacos(energias[arq], pal, f["ini"], f["fim"])
        f["_t0"] = t
        for a, b in ped:
            dur = q(b - a)
            pedacos.append({"fala": f["id"], "fonte": f["fonte"], "s": a, "e": a + dur, "t": t})
            t += dur
        f["_t1"] = t

        def mapa(ts, fid=f["id"]):
            """tempo no bruto → tempo na linha do tempo (num silêncio cortado, cai no começo do pedaço seguinte)"""
            ps = [x for x in pedacos if x["fala"] == fid]
            for x in ps:
                if ts < x["s"]:
                    return x["t"]
                if ts <= x["e"]:
                    return x["t"] + ts - x["s"]
            return ps[-1]["t"] + ps[-1]["e"] - ps[-1]["s"]
        palavras[f["id"]] = [(p[2], mapa(p[0]), mapa(p[1])) for p in pal]
    T = t
    print(f"fala decupada: {len(pedacos)} pedaços, {T:.2f} s")

    # 2. voz contínua
    partes = []
    for i, x in enumerate(pedacos):
        src = os.path.join(FONTE, d["fontes"][x["fonte"]]["arquivo"])
        nome = os.path.join(TMP, f"voz_{i:02d}.wav")
        dur = x["e"] - x["s"]
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{x['s']:.4f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", "48000",
            "-af", f"afade=t=in:d=0.008,afade=t=out:st={max(0, dur - 0.008):.4f}:d=0.008,apad,atrim=0:{dur:.4f}", "-c:a", "pcm_s24le", nome])
        partes.append(nome)
    lista = os.path.join(TMP, "voz_lista.txt")
    with open(lista, "w") as fp:
        fp.writelines(f"file '{p}'\n" for p in partes)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c:a", "pcm_s24le", os.path.join(TMP, "voz.wav")])

    # 3. imagem: segmentos A (o Diego falando) e as ilustrações por cima
    def palavra_t(fid, w, ocorr=1):
        if w == 0:
            return next(f["_t0"] for f in d["falas"] if f["id"] == fid)
        n = 0
        for txt, a, _ in palavras[fid]:
            if decupagem_norm(txt) == decupagem_norm(w):
                n += 1
                if n == ocorr:
                    return a
        sys.exit(f"palavra '{w}' não encontrada na fala {fid}")

    fim_reel = T
    ilus = []
    for il in d["ilustracoes"]:
        fala = next(f for f in d["falas"] if f["id"] == il["fala"])
        a = q(max(fala["_t0"], palavra_t(il["fala"], il["de"], il.get("ocorrencia", 1)) - 0.04)) if il["de"] != 0 else fala["_t0"]
        b = q(palavra_t(il["fala"], il["ate"], il.get("ate_ocorrencia", 1)) - 0.04) if il.get("ate") else fala["_t1"]
        if il.get("cauda"):
            b = q(T + il["cauda"])
            fim_reel = b
        if il.get("dur_max"):
            b = min(b, q(a + il["dur_max"]))
        # um corte de fala a menos de 0,3 s vira o corte da ilustração (sem plano relâmpago)
        bordas = [x["t"] for x in pedacos] + [T]
        a = min(bordas, key=lambda z: abs(z - a)) if min(abs(z - a) for z in bordas) < 0.3 else a
        if not il.get("cauda"):
            b = min(bordas, key=lambda z: abs(z - b)) if min(abs(z - b) for z in bordas) < 0.3 else b
        ilus.append(dict(il, a=a, b=b))
    rosto = d["rosto"]

    def recorte_rosto(fonte, ts):
        k = np.array(rosto[fonte])
        cx = float(np.interp(ts, k[:, 0], k[:, 1]))
        return int(min(max(cx - rosto["posicao_no_recorte"], 0), 3840 - 1216))

    cortes = sorted({0.0, fim_reel, *[x["t"] for x in pedacos], *[i["a"] for i in ilus], *[i["b"] for i in ilus]})
    cenas, n_por_fala = [], {}
    for a, b in zip(cortes, cortes[1:]):
        if b - a < 0.5 / fps:
            continue
        il = next((i for i in ilus if i["a"] <= a < i["b"]), None)
        if il:
            fid, cena = il["fala"], {"fonte": il["fonte"], "in": round(il["in"] + a - il["a"], 4), "kenburns": bool(il.get("kenburns"))}
            if "recorte_x" in il:
                cena["recorte_x"] = [[round(tt - (a - il["a"]), 3), x] for tt, x in il["recorte_x"]] if len(il["recorte_x"]) > 1 else il["recorte_x"]
        else:
            x = next(p for p in pedacos if p["t"] - 1e-6 <= a < p["t"] + p["e"] - p["s"] - 1e-6)
            fid = x["fala"]
            ts = x["s"] + a - x["t"]
            cena = {"fonte": x["fonte"], "in": round(ts, 4), "recorte_x": [[0, recorte_rosto(x["fonte"], ts + (b - a) / 2)]]}
        n_por_fala[fid] = n_por_fala.get(fid, 0) + 1
        cena.update(id=f"{fid}_{n_por_fala[fid]}", out=round(cena["in"] + b - a, 4), audio="mudo", _t=a)
        cenas.append(cena)

    def em(tl):
        """tempo da linha do tempo → (cena, t dentro da cena)"""
        c = next(c for c in reversed(cenas) if c["_t"] <= tl + 1e-6)
        return c["id"], round(tl - c["_t"], 3)

    # legendas: os grupos consomem as palavras da fala na ordem
    grupos = []
    for f in d["falas"]:
        pal = palavras[f["id"]]
        k = 0
        for g in f["grupos"]:
            n = g["palavras"] if isinstance(g, dict) else len([w for w in g.replace("|", " ").split() if w])
            g = g["texto"] if isinstance(g, dict) else g
            ws = pal[k:k + n]
            k += n
            item = {"texto": g, "ini": round(ws[0][1], 3), "fim": round(ws[-1][2], 3)}
            dest = next((w for w in g.replace("|", " ").split() if w.startswith("*")), None)
            if dest:  # o Destaque é a palavra com * (contada na mesma posição da transcrição)
                i = [w for w in g.replace("|", " ").split()].index(dest)
                item["destaque_em"] = round(ws[i][1], 3)
            grupos.append(item)
        if k != len(pal):
            sys.exit(f"fala {f['id']}: legendas com {k} palavras, transcrição com {len(pal)}")
    for a, b in zip(grupos, grupos[1:]):
        a["fim"] = round(min(b["ini"], a["fim"] + 0.3), 3)
    grupos[-1]["fim"] = round(min(fim_reel, grupos[-1]["fim"] + 0.4), 3)

    m = {k: v for k, v in d.items() if k not in ("falas", "ilustracoes", "rosto")}
    m["cenas"] = [{k: v for k, v in c.items() if k != "_t"} for c in cenas]
    m["audios"] = [{"id": "voz", "fonte": "VOZ", "in": 0.0, "out": round(T, 4), "tipo": "voz", "inicio": {"cena": cenas[0]["id"], "t": 0}}]
    m["legendas"] = [{"audio": "voz", "modo": "grupo", "grupos": grupos}]
    m["placa"]["cena"] = cenas[0]["id"]
    m["capa"]["cena"] = cenas[0]["id"]
    m["sons"][0]["cena"] = cenas[0]["id"]
    cta_c, cta_t = em(T + 0.15)
    for pl in [m["placas"][0], *m["variantes"]["sem-data"]["placas"]]:
        pl["cena"], pl["t"] = cta_c, cta_t
    m["sons"][1]["cena"], m["sons"][1]["t"] = cta_c, round(cta_t + 0.28, 3)
    for obj in [*m["informacao"], *m["tickets"]]:
        f = next(f for f in d["falas"] if f["id"] == obj["cena"])
        c, tt = em(f["_t0"])
        obj["cena"], obj["t"] = c, round(tt + obj["t"], 3)
    with open(os.path.join(TMP, "montado.json"), "w", encoding="utf-8") as fp:
        json.dump(m, fp, ensure_ascii=False, indent=1)
    for c in cenas:
        print(f"  {c['_t']:6.2f}  {c['id']:12s} {c['fonte']:11s} in {c['in']:6.2f}  {c['out'] - c['in']:4.2f} s")
    print(f"Reel: {fim_reel:.2f} s · {len(cenas)} planos · montagem em _tmp/montado.json")


def decupagem_norm(w):
    import unicodedata
    w = unicodedata.normalize("NFKD", w.lower())
    return "".join(c for c in w if c.isalnum())


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(m[-1]), float(p[-1]) if p else None


def expr_recorte(pontos, desloc=0.0):
    """x(t) do recorte: interpolação suave (smoothstep) entre os pontos [t, x0] (t relativo ao início do trecho)."""
    if len(pontos) == 1:
        return str(pontos[0][1])
    tt = f"(t-{desloc:.4f})"
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max(({tt}-{t0})/({t1}-{t0}),0),1)"
        seg = f"({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p}))"
        e = f"if(lt({tt},{t1}),{seg},{e})"
    return e


def alcas(d):
    """Alças de 100 ms nas cenas vizinhas a um Arrasto (a transição sobrepõe as duas cenas)."""
    q = round(0.1 * d["fps"])
    ids = [c["id"] for c in d["cenas"]]
    out = {i: [0, 0] for i in ids}
    for t in d["transicoes"]:
        if t["tipo"] == "arrasto":
            k = ids.index(t["entra"])
            out[ids[k - 1]][1] = q
            out[t["entra"]][0] = q
    return out


def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    os.makedirs(PUBLIC, exist_ok=True)
    faltando = [f for f in d["fontes"].values() if not os.path.exists(os.path.join(FONTE, f["arquivo"]))]
    if faltando:
        print("Brutos ausentes em ../fonte/. Baixe do Drive (pasta do CLAUDE.md, seção 10):")
        for f in faltando:
            print(f"  curl -L -o ../fonte/{f['arquivo']} 'https://drive.usercontent.google.com/download?id={f['drive_id']}&export=download&confirm=t'")
        sys.exit(1)

    props = dict(d)
    cenas = []
    al = alcas(d)
    for c in d["cenas"]:
        f = d["fontes"][c["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        n = round((c["out"] - c["in"]) * fps)
        dur = n / fps
        antes, depois = al[c["id"]]
        vf = []
        entrada = ["-ss", f"{c['in'] - antes / fps:.4f}"]
        if f["girar"] != "auto":
            # O ffmpeg aplica o metadado de rotação ao decodificar (−90 → 90° horário). Com -noautorotate
            # ele copiaria o metadado errado para a saída; por isso deixamos girar e corrigimos aqui.
            correcao = (f["girar"] + rotacao_meta(src)) % 360
            vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
        if f["hdr"]:
            vf.append(TONEMAP)
        if "recorte_x" in c:
            w0, h0 = sonda(src)
            giro = rotacao_meta(src) if f["girar"] == "auto" else f["girar"]
            altura = h0 if giro % 180 == 0 else w0
            largura_recorte = round(altura * W / H / 2) * 2
            vf.append(f"crop=w={largura_recorte}:h={altura}:x='{expr_recorte(c['recorte_x'], antes / fps)}':y=0")
        vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
        arq_v = f"cena_{c['id']}.mp4"
        sh(["ffmpeg", "-v", "error", "-y", *entrada, "-i", src, "-vf", ",".join(vf), "-frames:v", str(n + antes + depois), "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq_v)])
        cena = dict(c, arquivo=arq_v, quadros=n, dur=dur, alca_antes_q=antes, alca_depois_q=depois)
        if c["audio"] in ("voz", "ambiente"):
            cena.update(audio_trecho(src, c["in"], dur, f"cena_{c['id']}.wav", d["mix"][f"{c['audio']}_lufs"]))
        cenas.append(cena)
        print(f"cena {c['id']}: {n} quadros ({dur:.3f} s)" + (f" + alças {antes}/{depois}" if antes or depois else ""))
    props["cenas"] = cenas

    # áudios extras (J-cut)
    inicio = {}
    acum = 0.0
    for c in cenas:
        inicio[c["id"]] = acum
        acum += c["dur"]
    auds = []
    for a in d["audios"]:
        f = d["fontes"][a["fonte"]]
        src = os.path.join(FONTE, f["arquivo"])
        dur = a["out"] - a["in"]
        aa = dict(a, dur=dur)
        aa.update(audio_trecho(src, a["in"], dur, f"audio_{a['id']}.wav", d["mix"][f"{a['tipo']}_lufs"]))
        t0 = inicio[a["inicio"]["cena"]] + a["inicio"]["t"]
        # sincronia labial: se a mesma fonte aparece numa cena enquanto o áudio toca, a fala tem de cair no mesmo ponto
        for c in cenas:
            sobrepoe = inicio[c["id"]] < t0 + dur and t0 < inicio[c["id"]] + c["dur"]
            if c["fonte"] == a["fonte"] and sobrepoe:
                desvio = (inicio[c["id"]] - t0) - (c["in"] - a["in"])
                print(f"sincronia {a['id']} × cena {c['id']}: desvio {desvio * 1000:+.1f} ms")
                if abs(desvio) > 1000 / fps / 2:
                    sys.exit("áudio fora de sincronia com a imagem")
        auds.append(aa)
    props["audios"] = auds
    props["duracao"] = acum
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {acum:.3f} s · props em _tmp/props.json")


def audio_trecho(src, ini, dur, nome, alvo):
    """Extrai o áudio do trecho em 48 kHz estéreo, iguala a loudness ao alvo da mixagem e faz fades curtos."""
    bruto = os.path.join(TMP, "bruto_" + nome)
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini:.3f}", "-i", src, "-t", f"{dur:.4f}", "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", bruto])
    medido, _ = lufs(bruto)
    ganho = alvo - medido
    af = f"volume={ganho:.2f}dB,afade=t=in:d=0.015,afade=t=out:st={max(0, dur - 0.025):.4f}:d=0.025,apad,atrim=0:{dur:.4f}"
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", af, "-c:a", "pcm_s24le", os.path.join(PUBLIC, nome)])
    print(f"  {nome}: {medido:.1f} LUFS → {alvo} LUFS ({ganho:+.1f} dB)")
    return {"audio_arquivo": nome, "lufs_medido": round(medido, 1), "ganho_db": round(ganho, 1), "lufs": alvo}


def render(props=os.path.join(TMP, "props.json"), saida_bruta=SAIDA_BRUTA):
    cmd = ["npx", "remotion", "render", "src/index.ts", "Reel", saida_bruta, f"--props={props}", f"--public-dir={PUBLIC}",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    print("  (em", REMOTION, ")")
    r = subprocess.run(cmd, cwd=REMOTION)
    if r.returncode != 0:
        sys.exit("render falhou")


def master(saida_bruta=SAIDA_BRUTA, saida=SAIDA):
    """Ganho linear até −14 LUFS + limitador de pico com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP).

    Não usa o loudnorm dinâmico: ele comprime e muda o equilíbrio voz × música feito na mixagem."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(saida_bruta)
    ganho = alvo - i0
    teto = pico - 0.4  # margem para o AAC
    for _ in range(4):
        af = (f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,"
              "aresample=48000")
        sh(["ffmpeg", "-v", "error", "-y", "-i", saida_bruta, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", saida])
        i, tp = medir_master(saida)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP (ganho {ganho:+.1f} dB) → {os.path.basename(saida)}")


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def capa():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaReel", CAPA, f"--props={props}", f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("capa falhou")


def sem_data():
    """Variante com outro CTA na placa do fim (rev3.json, "variantes"): mesmas cenas, legendas e sons."""
    d = carregar()
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        props = json.load(f)
    props["placas"] = d["variantes"]["sem-data"]["placas"]
    arq = os.path.join(TMP, "props_sem-data.json")
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=1)
    bruta = os.path.join(TMP, "reel_sem-data_sem_master.mov")
    render(arq, bruta)
    master(bruta, SAIDA.replace(".mp4", "_sem-data.mp4"))


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"montar": [montar], "preparar": [preparar], "render": [render], "master": [master], "capa": [capa], "sem-data": [sem_data],
              "tudo": [montar, preparar, render, master, capa, sem_data]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
