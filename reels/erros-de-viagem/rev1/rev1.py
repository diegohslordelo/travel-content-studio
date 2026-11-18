#!/usr/bin/env python3
"""Reel "Erros de viagem" · REV1 (tela dividida, gravação do Diego no quarto de 18/11/2026).

Pipeline (rode de dentro desta pasta):
    python3 rev1.py imagens    # baixa as fotos da internet (licenças em rev1.json) e prepara a do gancho
    python3 rev1.py preparar   # decupagem (10 blocos), voz tratada, legendas, cenas e sons em _tmp/public
    python3 rev1.py render     # Remotion monta o Reel (design-system/remotion, composição "ReelErrosViagem")
    python3 rev1.py master     # −14 LUFS integrados, pico verdadeiro ≤ −1 dBTP
    python3 rev1.py capa       # capa 1080 × 1920 (quadro do gancho completo)
    python3 rev1.py quadros    # folha de QA (qa_frames/)
    python3 rev1.py hdr        # versão final: gravação crua (HDR HLG, como o Diego mandou) por baixo dos gráficos
    python3 rev1.py tudo

Entradas: rev1.json (decisões), transcricao_large-v3.json (palavras com tempo, Whisper large-v3 da gravação inteira),
imagens/ (fotos baixadas), serasa/ (print real do release), o bruto em ../fonte/diego_serasa.mp4 (fora do git; Drive,
pasta "Serasa", id em rev1.json). Usa numpy, soundfile, Pillow, ffmpeg e Node.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.normpath(os.path.join(AQUI, "..", "fonte"))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
IMAGENS = os.path.join(AQUI, "imagens")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "remotion"))
SONS_EXT = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "design-system", "sons", "externos"))
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_erros-de-viagem_rev1.mp4")
PREVIA = os.path.join(AQUI, "reel_erros-de-viagem_rev1_previa.mp4")
CAPA = os.path.join(AQUI, "capa_erros-de-viagem_rev1.jpg")
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")
UA = "PrimeiroDiaReel/1.0 (editorial video)"

# Sem tratamento de imagem na gravação (pedido do Diego, 18/11/2026: "eu já mandei ele pronto para ser usado").
# Só a conversão técnica de 10 para 8 bits (H.264 do Reel); cor, brilho e enquadramento ficam como ele mandou.
SAIDA_X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-g", "15", "-pix_fmt", "yuv420p",
              "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd, capturar=False):
    texto = " ".join(cmd)
    print("  $", texto if len(texto) < 220 else texto[:220] + " …")
    r = subprocess.run(cmd, capture_output=capturar, text=True)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev1.json"), encoding="utf-8") as f:
        return json.load(f)


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


# ---------------------------------------------------------------- imagens

def baixar(url, destino):
    if "upload.wikimedia.org" in url:
        # o servidor de originais devolve 429; o thumb.php do Commons entrega a mesma foto (FORMATOS_REELS, 8.5)
        nome = urllib.parse.unquote(url.split("?")[0].split("/")[-1])
        url = f"https://commons.wikimedia.org/w/thumb.php?f={urllib.parse.quote(nome)}&w=2000"
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                dados = r.read()
            if len(dados) < 5000:
                raise RuntimeError("arquivo vazio")
            with open(destino, "wb") as f:
                f.write(dados)
            return
        except Exception as e:  # 429 do Wikimedia, oscilação do Flickr
            print(f"    tentativa {i + 1}: {e}")
            time.sleep(6 * (i + 1))
    sys.exit(f"não baixou: {url}")


def imagens():
    from PIL import Image
    d = carregar()
    os.makedirs(IMAGENS, exist_ok=True)
    for k, im in d["imagens"].items():
        dest = os.path.join(IMAGENS, im["arquivo"])
        if os.path.exists(dest) or "url" not in im:
            continue
        print(f"  {k}: {im['url'][:90]}")
        bruto = dest + ".bruto"
        baixar(im["url"], bruto)
        with Image.open(bruto) as x:
            x = x.convert("RGB")
            # até 2160 px no lado maior: sobra para o Ken Burns sem pesar o render
            x.thumbnail((2160, 2160), Image.LANCZOS)
            x.save(dest, quality=92)
        os.remove(bruto)
        time.sleep(2)
    # foto do gancho (enviada pelo Diego, 620 × 430): só ampliada para a largura do Reel, sem tratamento
    g = d["imagens"]["gancho"]
    orig = os.path.join(IMAGENS, g["original"])
    with Image.open(orig) as x:
        x = x.convert("RGB")
        w = 1080
        h = round(x.height * w / x.width)
        x = x.resize((w, h), Image.LANCZOS)
        x.save(os.path.join(IMAGENS, g["arquivo"]), quality=94)
    print("imagens ok")


# ---------------------------------------------------------------- linha do tempo

def limpa(txt):
    return re.sub(r"[,.?!]", "", txt.strip())


def linha_do_tempo(d):
    """Blocos no Reel (alinhados a quadros) e as palavras com tempo no Reel (o '%' do Whisper junta ao número)."""
    fps = d["fps"]
    with open(os.path.join(AQUI, "transcricao_large-v3.json"), encoding="utf-8") as f:
        tr = json.load(f)
    todas = []
    for s in tr:
        for w in s["words"]:
            txt = w["w"].strip()
            if txt == "%" and todas:
                todas[-1]["w"] += "%"
                todas[-1]["e"] = w["e"]
                continue
            todas.append({"w": txt, "s": w["s"], "e": w["e"], "p": w["p"]})
    blocos, palavras = [], []
    t = 0.0
    for b in d["blocos"]:
        qi, qo = round(b["in"] * fps), round(b["out"] * fps)
        ini, fim = qi / fps, qo / fps
        dur = (qo - qi) / fps
        ws = [w for w in todas if w["s"] >= ini - 0.6 and w["e"] <= fim + 0.3 and w["s"] < fim]
        cont = {}
        for j, w in enumerate(ws):
            s = max(w["s"], b["inicio_voz"]) if j == 0 else w["s"]  # o Whisper adianta a 1ª palavra do bloco
            e = max(w["e"], s + 0.05)
            chave = limpa(w["w"]).lower()
            cont[chave] = cont.get(chave, 0) + 1
            palavras.append({"bloco": b["id"], "texto": w["w"], "chave": chave, "n": cont[chave],
                             "ini": round(t + s - ini, 3), "fim": round(t + min(e, fim) - ini, 3), "prob": w["p"]})
        blocos.append(dict(b, qi=qi, qo=qo, dur=dur, inicio=round(t, 4)))
        t += dur
    return blocos, palavras, t


def resolver(ancora, palavras, fim):
    """'b06:Fica-0.08' → segundos no Reel. Aceita número, 'fim' e '#n' (n-ésima ocorrência no bloco)."""
    if isinstance(ancora, (int, float)):
        return float(ancora)
    if ancora == "fim":
        return fim
    m = re.fullmatch(r"(b\d+):([^#+\-]+?)(?:#(\d+))?([+-][\d.]+)?", ancora)
    if not m:
        sys.exit(f"âncora inválida: {ancora}")
    bloco, pal, n, desl = m.group(1), m.group(2).lower(), int(m.group(3) or 1), float(m.group(4) or 0)
    for w in palavras:
        if w["bloco"] == bloco and w["chave"] == pal and w["n"] == n:
            return w["ini"] + desl
    sys.exit(f"palavra não encontrada: {ancora}")


FUNCIONAIS = {"a", "à", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e", "em", "no", "na", "nos", "com", "que",
              "se", "para", "por", "sua", "seu", "só", "pelo", "é", "era", "não", "já", "você", "te", "mais", "toda", "aquela", "esse"}


def grupos_legenda(d, palavras):
    """Legenda de 1 a 4 palavras (≤ 24 caracteres, 1 linha), sem terminar em palavra funcional. O gancho fica de fora."""
    corr = d["correcoes_legenda"]
    dest = {x.lower() for x in d["destaques"]}
    quebrar_antes = set(d.get("quebrar_antes", []))  # 'b07:tem#3': começa grupo novo nesta palavra
    nao_quebrar_depois = set(d.get("nao_quebrar_depois", []))  # 'b08:fala#1': o grupo não fecha depois desta palavra
    grupos, atual = [], []

    def fecha():
        if atual:
            grupos.append({"palavras": [dict(w) for w in atual], "ini": atual[0]["ini"], "bloco": atual[0]["bloco"]})
            atual.clear()

    for w in palavras:
        if w["bloco"] == "b01":
            continue
        chave = f"{w['bloco']}:{w['chave']}#{w['n']}"
        texto = w["texto"]
        if chave in corr:
            pont = re.findall(r"[,.?!]$", texto)
            texto = corr[chave] + (pont[0] if pont else "")
        item = {"texto": texto, "ini": w["ini"], "fim": w["fim"], "destaque": limpa(texto).lower() in dest, "bloco": w["bloco"]}
        if atual and (atual[0]["bloco"] != w["bloco"] or chave in quebrar_antes):
            fecha()
        if atual and sum(len(x["texto"]) + 1 for x in atual) + len(texto) > 24:
            fecha()
        atual.append(item)
        chars = sum(len(x["texto"]) + 1 for x in atual)
        solta = limpa(texto).lower() in FUNCIONAIS
        if chave in nao_quebrar_depois:
            continue
        if re.search(r"[,.?!]$", texto) or len(atual) >= 6 or ((len(atual) >= 3 or chars > 15) and not solta):
            fecha()
    fecha()
    for i, g in enumerate(grupos):
        prox = grupos[i + 1]["ini"] if i + 1 < len(grupos) else g["palavras"][-1]["fim"] + 0.4
        g["fim"] = round(min(prox, g["palavras"][-1]["fim"] + 0.45), 3)
        # 1 destaque por grupo: o 1º marcado
        visto = False
        for w in g["palavras"]:
            if w["destaque"] and not visto:
                visto = True
            else:
                w["destaque"] = False
            w.pop("bloco", None)
        g.pop("bloco", None)
    return grupos


# ---------------------------------------------------------------- preparar

def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    src = os.path.join(FONTE, d["fonte"]["arquivo"])
    if not os.path.exists(src):
        sys.exit(f"bruto ausente: curl -L -o ../fonte/{d['fonte']['arquivo']} "
                 f"'https://drive.usercontent.google.com/download?id={d['fonte']['drive_id']}&export=download&confirm=t'")
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "img"))
    os.makedirs(os.path.join(PUBLIC, "sfx"))
    blocos, palavras, fim_falas = linha_do_tempo(d)

    # 1. Fala: cada bloco recortado no quadro (HLG → SDR, 1080 × 1920) e concatenado em corte seco.
    lista_v, lista_a = [], []
    for b in blocos:
        n = b["qo"] - b["qi"]
        v = os.path.join(TMP, f"fala_{b['id']}.mp4")
        a = os.path.join(TMP, f"fala_{b['id']}.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['qi'] / fps:.4f}", "-i", src, "-vf",
            f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1", "-frames:v", str(n), "-an", *SAIDA_X264, v])
        fi = b.get("fade_in", 0.012)
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['qi'] / fps:.4f}", "-i", src, "-map", "0:a:0", "-ac", "1", "-ar", "48000", "-af",
            f"apad,atrim=0:{b['dur']:.5f},afade=t=in:d={fi},afade=t=out:st={b['dur'] - 0.05:.4f}:d=0.05", "-c:a", "pcm_s24le", a])
        lista_v.append(v)
        lista_a.append(a)
    with open(os.path.join(TMP, "concat.txt"), "w") as f:
        f.writelines(f"file '{v}'\n" for v in lista_v)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "concat.txt"), "-c", "copy", os.path.join(PUBLIC, "fala.mp4")])
    voz_bruta = os.path.join(TMP, "voz_bruta.wav")
    entradas = sum((["-i", a] for a in lista_a), [])
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", f"concat=n={len(lista_a)}:v=0:a=1", "-c:a", "pcm_s24le", voz_bruta])
    medido, _ = medir(voz_bruta)
    mix = d["mix"]
    alvo = mix["voz_lufs"]
    ganho = alvo - medido
    teto = mix["voz_pico_dbtp"] - 0.4
    voz = os.path.join(PUBLIC, "voz.wav")
    for _ in range(5):
        sh(["ffmpeg", "-v", "error", "-y", "-i", voz_bruta, "-af",
            f"highpass=f=70,volume={ganho:.2f}dB,pan=stereo|c0=0.7071*c0|c1=0.7071*c0,aresample=192000,"
            f"alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000", "-c:a", "pcm_s24le", voz])
        i, tp = medir(voz)
        if abs(i - alvo) <= 0.1 and tp <= mix["voz_pico_dbtp"]:
            break
        ganho += alvo - i
        if tp > mix["voz_pico_dbtp"]:
            teto -= tp - mix["voz_pico_dbtp"] + 0.1
    print(f"voz: {medido:.1f} → {i:.1f} LUFS ({ganho:+.1f} dB) · pico {tp:.1f} dBTP · falas {fim_falas:.3f} s")

    # 2. Cenas: início de cada uma resolvido pela palavra; a cena vai até o início da seguinte.
    cauda = d["cta"]["cauda_s"]
    total = fim_falas + cauda
    cenas = []
    for c in d["cenas"]:
        cc = {k: v for k, v in c.items() if k not in ("ini", "marcos")}
        cc["ini_s"] = 0.0 if c["ini"] == 0 else resolver(c["ini"], palavras, fim_falas)
        if "marcos" in c:
            cc["marcos"] = {n: round(resolver(v, palavras, fim_falas) - cc["ini_s"], 3) if isinstance(v, str) else v for n, v in c["marcos"].items()}
        cenas.append(cc)
    for i, cc in enumerate(cenas):
        fim = cenas[i + 1]["ini_s"] if i + 1 < len(cenas) else total
        cc["ini_q"] = round(cc["ini_s"] * fps)
        cc["fim_q"] = round(fim * fps)
        if cc["fim_q"] - cc["ini_q"] < 12:
            sys.exit(f"cena {cc['id']} curta demais ({(cc['fim_q'] - cc['ini_q']) / fps:.2f} s)")

    # 3. Fotos e print da Serasa
    imgs = {}
    for k, im in d["imagens"].items():
        orig = os.path.join(AQUI, im.get("pasta", "imagens"), im["arquivo"])
        shutil.copy(orig, os.path.join(PUBLIC, "img", im["arquivo"]))
        imgs[k] = {"arquivo": "img/" + im["arquivo"]}

    # 4. Sons de transição (PDX_*, CC0) no volume de trabalho relativo à voz (REFERENCIA_EDICAO_FORMATOS, 4.1)
    sons = []
    for s in d["sons"]:
        shutil.copy(os.path.join(SONS_EXT, s["arquivo"]), os.path.join(PUBLIC, "sfx", s["arquivo"]))
        em = resolver(s["em"], palavras, fim_falas)
        ganho_db = mix["voz_lufs"] + s["rel_db"] - d["nivel_l50"][s["arquivo"]]
        sons.append({"arquivo": "sfx/" + s["arquivo"], "em": round(em, 3), "ganho_db": round(ganho_db, 1)})
    sons.sort(key=lambda s: s["em"])
    for a, b in zip(sons, sons[1:]):
        if b["em"] - a["em"] < 1.5:
            print(f"  aviso: dois efeitos a menos de 1,5 s ({a['arquivo']} {a['em']} · {b['arquivo']} {b['em']})")

    gancho = [dict(l, em=round(resolver(l["em"], palavras, fim_falas), 3) if isinstance(l["em"], str) else l["em"]) for l in d["gancho"]]
    legendas = grupos_legenda(d, palavras)
    cta_ini = resolver(d["cta"]["ini"], palavras, fim_falas)
    props = {
        "fps": fps, "largura": W, "altura": H, "costura": d["costura_y"], "rostoY": d["rosto_y"], "quadros": round(total * fps),
        "cenas": cenas, "imagens": imgs, "gancho": gancho, "legendas": legendas, "sons": sons,
        "cta": {"ini": round(cta_ini, 3), "entrada_ms": d["cta"]["entrada_ms"], "rotulo": d["cta"]["rotulo"], "destino": d["cta"]["destino"],
                "clack_db_rel": mix["clack_db_rel"]},
        "voz_lufs": mix["voz_lufs"],
    }
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    with open(os.path.join(TMP, "palavras.json"), "w", encoding="utf-8") as fp:
        json.dump(palavras, fp, ensure_ascii=False, indent=1)
    with open(os.path.join(TMP, "blocos.json"), "w", encoding="utf-8") as fp:
        json.dump(blocos, fp, ensure_ascii=False, indent=1)
    print(f"duração: {total:.3f} s ({round(total * fps)} quadros)")
    for cc in cenas:
        print(f"  {cc['ini_q'] / fps:6.2f}–{cc['fim_q'] / fps:6.2f} ({(cc['fim_q'] - cc['ini_q']) / fps:4.2f} s)  {cc['id']:<16} {cc['tipo']:<6} {cc['layout']}")


# ---------------------------------------------------------------- render, master, capa, quadros

def remotion(args):
    cmd = ["npx", "remotion", *args]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("remotion falhou")


def render():
    remotion(["render", "src/index.ts", "ReelErrosViagem", SAIDA_BRUTA, f"--props={os.path.join(TMP, 'props.json')}", f"--public-dir={PUBLIC}",
              "--codec=h264", "--crf=15", "--audio-codec=pcm-16", "--log=warn", "--concurrency=4"])


def master():
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir(SAIDA_BRUTA)
    ganho = alvo - i0
    teto = pico - 0.4
    for _ in range(5):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart", SAIDA])
        i, tp = medir(SAIDA)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    print(f"master: {i:.1f} LUFS · pico verdadeiro {tp:.1f} dBTP → {os.path.basename(SAIDA)}")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "26", "-preset", "medium",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])


def capa():
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    q = min(round((p["gancho"][-1]["em"] + 0.3) * p["fps"]), p["cenas"][1]["ini_q"] - 1)
    remotion(["still", "src/index.ts", "ReelErrosViagem", CAPA, f"--frame={q}", f"--props={os.path.join(TMP, 'props.json')}",
              f"--public-dir={PUBLIC}", "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"])


def quadros():
    from PIL import Image, ImageDraw
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    pasta = os.path.join(AQUI, "qa_frames")
    os.makedirs(pasta, exist_ok=True)
    fps = p["fps"]
    tempos = []
    for c in p["cenas"]:
        a, b = c["ini_q"] / fps, c["fim_q"] / fps
        tempos.append((c["id"], a + min(0.9, (b - a) * 0.6)))
    tempos.append(("cta_fim", p["quadros"] / fps - 0.3))
    tiles = []
    for nome, t in tempos:
        arq = os.path.join(TMP, f"q_{nome}.jpg")
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", SAIDA, "-frames:v", "1", "-vf", "scale=216:384", arq])
        im = Image.open(arq)
        t2 = Image.new("RGB", (216, 404), "white")
        t2.paste(im, (0, 20))
        ImageDraw.Draw(t2).text((3, 3), f"{t:5.2f} {nome}"[:34], fill="black")
        tiles.append(t2)
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    folha = Image.new("RGB", (216 * cols, 404 * rows), "white")
    for i, t2 in enumerate(tiles):
        folha.paste(t2, ((i % cols) * 216, (i // cols) * 404))
    folha.save(os.path.join(pasta, "folha_rev1.jpg"), quality=82)
    print("folha em qa_frames/folha_rev1.jpg")


# ---------------------------------------------------------------- HDR: gravação crua por baixo dos gráficos

SAIDA_HDR = os.path.join(AQUI, "reel_erros-de-viagem_rev1_hdr.mp4")


def hdr():
    """Pedido do Diego (18/11/2026): a gravação entra exatamente como ele mandou (HLG, BT.2020, 10 bits).
    O Remotion gera só a camada de gráficos (fotos, animações, legendas, placa) com transparência; o ffmpeg põe a
    gravação crua por baixo (corte, deslocamento e enquadramento sem mexer em pixel) e converte só os gráficos para
    HLG (branco no nível de referência de 75%, npl 203). Áudio: o do master."""
    d = carregar()
    fps = d["fps"]
    with open(os.path.join(TMP, "props.json"), encoding="utf-8") as f:
        p = json.load(f)
    with open(os.path.join(TMP, "blocos.json"), encoding="utf-8") as f:
        blocos = json.load(f)
    pg = dict(p, soGraficos=True)
    arq_pg = os.path.join(TMP, "props_graficos.json")
    with open(arq_pg, "w", encoding="utf-8") as f:
        json.dump(pg, f, ensure_ascii=False)
    graf = os.path.join(TMP, "graficos.mov")
    if not os.path.exists(graf) or os.path.getmtime(graf) < os.path.getmtime(arq_pg):
        remotion(["render", "src/index.ts", "ReelErrosViagem", graf, f"--props={arq_pg}", f"--public-dir={PUBLIC}", "--codec=prores",
                  "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png", "--muted", "--log=warn", "--concurrency=4"])
    src = os.path.join(FONTE, d["fonte"]["arquivo"])
    entradas, fc = [], []
    for i, b in enumerate(blocos):
        entradas += ["-ss", f"{b['qi'] / fps:.4f}", "-t", f"{b['dur'] + 0.5:.4f}", "-i", src]
        fc.append(f"[{i}:v]trim=end_frame={b['qo'] - b['qi']},setpts=PTS-STARTPTS[b{i}]")
    n = len(blocos)
    cauda = p["quadros"] / fps - sum(b["dur"] for b in blocos)
    rosto_top = round(1020 * 0.42 - p["rostoY"]) * -1  # 212: linha da gravação que fica no topo da metade de baixo
    rosto_top -= rosto_top % 2
    fc.append("".join(f"[b{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,tpad=stop_mode=clone:stop_duration={cauda + 0.1:.3f},split=2[fa][fb]")
    fc.append(f"[fa]crop=1080:1020:0:{rosto_top},pad=1080:1920:0:{p['costura']}:black[sp]")
    cheias = [c for c in p["cenas"] if c["tipo"] == "diego"]
    en = "+".join(f"between(n,{c['ini_q']},{c['fim_q'] - 1})" for c in cheias)
    fc.append(f"[sp][fb]overlay=x=0:y=0:enable='{en}':format=yuv420p10[base]")
    g = n
    entradas += ["-i", graf]
    fc.append(f"[{g}:v]split=2[gc][ga]")
    fc.append("[gc]zscale=min=bt709:rin=limited:tin=iec61966-2-1:pin=bt709:m=gbr:r=full:t=linear:p=bt709:npl=203,format=gbrpf32le,"
              "zscale=t=arib-std-b67:p=bt2020:m=gbr:r=full:npl=203,zscale=m=bt2020nc:r=limited,format=yuv444p10le[gcor]")
    fc.append("[ga]alphaextract,format=gray10le[galfa]")
    fc.append("[gcor][galfa]alphamerge[gfin]")
    fc.append(f"[base][gfin]overlay=x=0:y=0:format=yuv420p10:eof_action=pass,trim=end_frame={p['quadros']},format=yuv420p10le[out]")
    entradas += ["-i", SAIDA]
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fc), "-map", "[out]", "-map", f"{g + 1}:a", "-c:a", "copy",
        "-c:v", "libx265", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p10le", "-tag:v", "hvc1",
        "-x265-params", "colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:log-level=error",
        "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv",
        "-movflags", "+faststart", SAIDA_HDR])
    print(f"HDR (HLG) → {os.path.basename(SAIDA_HDR)}")


if __name__ == "__main__":
    passo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    passos = {"imagens": imagens, "preparar": preparar, "render": render, "master": master, "capa": capa, "quadros": quadros, "hdr": hdr}
    if passo == "tudo":
        for f in (imagens, preparar, render, master, capa, quadros):
            f()
    else:
        passos[passo]()
