#!/usr/bin/env python3
"""Reel narrado "Isso é tudo o que fizemos em uma manhã em Lisboa" · REV3.

A REV3 refaz o corte da REV1 sobre a narração que o Diego gravou (tomadas em ../fonte/narracao_brutos, texto
diferente do roteiro da REV1). Cada fala de rev3.json tem os seus planos; o primeiro plano entra 0,1 s antes da
primeira palavra da fala, e um plano com `corte_em` entra 0,1 s antes da palavra indicada (o corte cai na palavra
que ele ilustra). Os tempos vêm do alinhamento da voz montada com o texto das falas (faster-whisper, tempo por
palavra).

Pipeline (rode de dentro desta pasta):
    python3 rev3.py narracao   # tomadas → _tmp/narracao.wav (passa-alta, redução de ruído, −16 LUFS por tomada, limitador, pausas)
    python3 rev3.py tempos     # tempos das falas, das palavras e das legendas → _tmp/tempos.json
    python3 rev3.py preparar   # cenas em _tmp/public (corte, HLG→SDR, recorte 9:16, quadro congelado) e a narração
    python3 rev3.py render     # Remotion monta o Reel (design-system/remotion, composição "Reel")
    python3 rev3.py master     # −14 LUFS integrados, pico ≤ −1 dBTP (DS V2, 4.6)
    python3 rev3.py capa
    python3 rev3.py tudo

Áudio: só a voz e os sons de marca da 4.6, sem som ambiente (decisão do Diego, 19/10/2026). A trilha entra no
Instagram na hora de postar, 8 a 10 dB abaixo da voz (DS V2, 4.6).

Saída: reel_lisboa-manha_rev3.mp4 e a prévia leve reel_lisboa-manha_rev3_previa.mp4.
"""
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
TMP = os.path.join(AQUI, "_tmp")
PUBLIC = os.path.join(TMP, "public")
REMOTION = os.path.join(RAIZ, "design-system", "remotion")
NARRACAO = os.path.join(TMP, "narracao.wav")
SAIDA_BRUTA = os.path.join(TMP, "reel_sem_master.mov")
SAIDA = os.path.join(AQUI, "reel_lisboa-manha_rev3.mp4")
PREVIA = os.path.join(AQUI, "reel_lisboa-manha_rev3_previa.mp4")
CAPA = os.path.join(AQUI, "capa_lisboa-manha_rev3.jpg")
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
SR = 48000
PRE_CORTE = 0.1  # o plano entra 0,1 s antes da palavra

# HLG (iPhone, BT.2020) → SDR BT.709: linearizar, converter o gamut, tone mapping Möbius (igual aos outros Reels).
TONEMAP = (
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)


def sh(cmd, capturar=False, cwd=None, entrada=None):
    print("  $", " ".join(cmd)[:240])
    r = subprocess.run(cmd, capture_output=capturar, text=entrada is None, cwd=cwd, input=entrada)
    if r.returncode != 0:
        if capturar:
            print(r.stdout[-2000:], r.stderr[-4000:])
        sys.exit(f"falhou: {cmd[0]}")
    return r


def carregar():
    with open(os.path.join(AQUI, "rev3.json"), encoding="utf-8") as f:
        return json.load(f)


def duracao(arq):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capturar=True)
    return float(r.stdout.strip())


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return float(m[-1]), float(p[-1]) if p else None


def ler_mono(arq, sr=SR):
    import numpy
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True)
    return numpy.frombuffer(r.stdout, dtype=numpy.float32)


# ---------------------------------------------------------------- narração

def limites_fala(audio, limiar_db=-40.0, minimo=4):
    """Início e fim da voz numa tomada: primeira e última sequência de pelo menos 4 janelas de 20 ms (80 ms) com RMS
    acima do limiar. Os cliques de iniciar e parar a gravação (1 ou 2 janelas) ficam de fora."""
    import numpy
    jan = SR // 50
    n = len(audio) // jan
    rms = 20 * numpy.log10(numpy.sqrt((audio[: n * jan].reshape(n, jan) ** 2).mean(1)) + 1e-9)
    acima = rms > limiar_db
    seqs, i = [], 0
    while i < n:
        if acima[i]:
            j = i
            while j < n and acima[j]:
                j += 1
            if j - i >= minimo:
                seqs.append((i, j))
            i = j
        else:
            i += 1
    return seqs[0][0] * 0.02, seqs[-1][1] * 0.02


def narracao():
    """Monta a narração: cada tomada é aparada (0,08 s antes da voz, 0,15 s depois), limpa (passa-alta 80 Hz,
    redução de ruído FFT), levada a −16 LUFS com os picos limitados a −3 dBFS e emendada com a pausa de rev3.json."""
    import numpy
    d = carregar()
    n = d["narracao"]
    os.makedirs(TMP, exist_ok=True)
    pasta = os.path.join(RAIZ, n["pasta"])
    partes, marcas, t = [], [], 0.0
    pausa = numpy.zeros(int(n["pausa_entre_tomadas"] * SR), dtype=numpy.float32)
    for i, nome in enumerate(n["tomadas"]):
        src = next((os.path.join(pasta, a) for a in sorted(os.listdir(pasta)) if os.path.splitext(a)[0] == nome), None)
        if not src:
            sys.exit(f"tomada ausente: {n['pasta']}/{nome}.*")
        bruto = ler_mono(src)
        v0, v1 = limites_fala(bruto)
        ini, fim = max(0.0, v0 - 0.08), min(len(bruto) / SR, v1 + 0.15)
        limpa = os.path.join(TMP, f"tomada_{nome}.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", str(SR),
            "-af", f"atrim={ini:.3f}:{fim:.3f},asetpts=N/SR/TB,highpass=f=80,afftdn=nr=10:nf=-50", "-c:a", "pcm_f32le", limpa])
        medido, _ = lufs(limpa)
        ganho = n.get("voz_lufs_tomada", d["mix"]["voz_lufs"]) - medido
        dur = fim - ini
        final = os.path.join(TMP, f"tomada_{nome}_final.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", limpa, "-af",
            f"volume={ganho:.2f}dB,alimiter=limit=0.708:attack=2:release=50:level=false,"
            f"afade=t=in:d=0.01,afade=t=out:st={max(0, dur - 0.04):.3f}:d=0.04", "-c:a", "pcm_f32le", final])
        if i:
            partes.append(pausa)
            t += len(pausa) / SR
        a = ler_mono(final)
        partes.append(a)
        marcas.append({"tomada": nome, "arquivo": os.path.basename(src), "recorte": [round(ini, 3), round(fim, 3)],
                       "na_narracao": [round(t, 3), round(t + len(a) / SR, 3)], "lufs_bruto": round(medido, 1), "ganho_db": round(ganho, 1)})
        t += len(a) / SR
    tudo = numpy.concatenate(partes)
    sh(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", NARRACAO],
       entrada=tudo.tobytes())
    with open(os.path.join(TMP, "narracao_tomadas.json"), "w", encoding="utf-8") as fp:
        json.dump(marcas, fp, ensure_ascii=False, indent=1)
    i, p = lufs(NARRACAO)
    print(f"narração: {len(n['tomadas'])} tomadas, {t:.2f} s, {i:.1f} LUFS, pico {p:.1f} dBFS → _tmp/narracao.wav")


# ---------------------------------------------------------------- tempos da narração

def normalizar(p):
    p = unicodedata.normalize("NFKD", p.lower())
    return "".join(c for c in p if c.isalnum())


def palavras_fala(d):
    """Lista de (fala, grupo, palavra) na ordem da narração."""
    return [(fi, gi, w) for fi, f in enumerate(d["falas"]) for gi, g in enumerate(f["grupos"]) for w in g["fala"].split()]


def tempos_alinhados(d, arq):
    """Tempo de cada palavra das falas a partir da gravação (faster-whisper, palavras alinhadas por diferença de sequência)."""
    from faster_whisper import WhisperModel

    audio16 = ler_mono(arq, 16000)
    modelo = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = modelo.transcribe(audio16, language="pt", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    ouvidas = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
    with open(os.path.join(TMP, "narracao_transcrita.json"), "w", encoding="utf-8") as f:
        json.dump([{"ini": a, "fim": b, "palavra": w} for a, b, w in ouvidas], f, ensure_ascii=False, indent=1)
    roteiro = [normalizar(w) for _, _, w in palavras_fala(d)]
    alvo = [normalizar(w) for _, _, w in ouvidas]
    tempos = [None] * len(roteiro)
    for bloco in difflib.SequenceMatcher(None, roteiro, alvo, autojunk=False).get_matching_blocks():
        for k in range(bloco.size):
            a, b, _ = ouvidas[bloco.b + k]
            tempos[bloco.a + k] = (a, b)
    casadas = sum(t is not None for t in tempos)
    faltam = [w for (_, _, w), t in zip(palavras_fala(d), tempos) if t is None]
    print(f"alinhamento: {casadas}/{len(roteiro)} palavras das falas encontradas na gravação; interpoladas: {' '.join(faltam)}")
    if casadas < 0.85 * len(roteiro):
        sys.exit("a gravação não bate com o texto das falas (menos de 85% das palavras): confira rev3.json")
    # palavras não encontradas: interpola entre as vizinhas
    for i, t in enumerate(tempos):
        if t is None:
            ant = next((tempos[j][1] for j in range(i - 1, -1, -1) if tempos[j]), 0.0)
            prox = next((tempos[j][0] for j in range(i + 1, len(tempos)) if tempos[j]), ant + 0.4)
            tempos[i] = (ant, max(ant + 0.05, prox))
    return tempos


def tempos():
    """Linha do tempo: a narração entra em `inicio`; cada fala guarda o tempo das suas palavras e das legendas."""
    d = carregar()
    n = d["narracao"]
    if not os.path.exists(NARRACAO):
        sys.exit("narração não montada: rode antes  python3 rev3.py narracao")
    ts = tempos_alinhados(d, NARRACAO)
    pw = palavras_fala(d)
    # a primeira palavra de cada tomada não começa antes da voz da tomada (o alinhador costuma adiantá-la para a pausa)
    with open(os.path.join(TMP, "narracao_tomadas.json"), encoding="utf-8") as fp:
        voz_ini = {m["tomada"]: m["na_narracao"][0] + 0.06 for m in json.load(fp)}
    ant = None
    for fi, f in enumerate(d["falas"]):
        if f["tomada"] != ant:
            i = next(i for i, (a, _, _) in enumerate(pw) if a == fi)
            a, b = ts[i]
            ts[i] = (max(a, voz_ini[f["tomada"]]), max(b, voz_ini[f["tomada"]] + 0.05))
            ant = f["tomada"]
    desloc = n["inicio"] - ts[0][0]  # tempo na linha do tempo − tempo na gravação
    falas = []
    for fi, f in enumerate(d["falas"]):
        idx_fala = [i for i, (a, _, _) in enumerate(pw) if a == fi]
        grupos = []
        for gi, g in enumerate(f["grupos"]):
            idx = [i for i in idx_fala if pw[i][1] == gi]
            item = {"texto": g["tela"], "ini": round(ts[idx[0]][0] + desloc, 3), "fim": round(ts[idx[-1]][1] + desloc, 3)}
            if "destaque_fala" in g:
                k = next(i for i in idx if normalizar(pw[i][2]) == normalizar(g["destaque_fala"]))
                item["destaque_em"] = round(ts[k][0] + desloc, 3)
            grupos.append(item)
        palavras = [{"palavra": pw[i][2], "ini": round(ts[i][0] + desloc, 3), "fim": round(ts[i][1] + desloc, 3)} for i in idx_fala]
        falas.append({"id": f["id"], "ini": grupos[0]["ini"], "fim": grupos[-1]["fim"], "grupos": grupos, "palavras": palavras})
    # legendas contínuas (máx. 0,4 s de folga depois da última palavra do grupo)
    todos = [g for f in falas for g in f["grupos"]]
    for a, b in zip(todos, todos[1:]):
        a["fim"] = round(min(b["ini"], a["fim"] + 0.4), 3)
    todos[-1]["fim"] = round(todos[-1]["fim"] + 0.4, 3)
    fim_narracao = falas[-1]["fim"]
    with open(os.path.join(TMP, "tempos.json"), "w", encoding="utf-8") as fp:
        json.dump({"narracao": NARRACAO, "desloc": round(desloc, 3), "falas": falas, "fim_narracao": fim_narracao}, fp, ensure_ascii=False, indent=1)
    for f in falas:
        print(f"  {f['id']:14s} {f['ini']:6.2f} → {f['fim']:6.2f}")
    print(f"fim da narração: {fim_narracao:.2f} s · Reel: {fim_narracao + n['cauda']:.2f} s")


# ---------------------------------------------------------------- cenas e áudio

def rotacao_meta(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream_side_data=rotation", "-of", "csv=p=0", arq], capturar=True)
    v = [x for x in r.stdout.strip().replace("\n", ",").split(",") if x.strip()]
    return int(float(v[0])) if v else 0


def sonda(arq):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", arq], capturar=True)
    s = json.loads(r.stdout)["streams"][0]
    return s["width"], s["height"]


def expr_recorte(pontos):
    if len(pontos) == 1:
        return str(pontos[0][1])
    e = str(pontos[-1][1])
    for (t0, x0), (t1, x1) in reversed(list(zip(pontos[:-1], pontos[1:]))):
        p = f"min(max((t-{t0})/({t1}-{t0}),0),1)"
        e = f"if(lt(t,{t1}),({x0}+({x1}-{x0})*{p}*{p}*(3-2*{p})),{e})"
    return e


def inicios_planos(f, ft, ini, fim):
    """Início de cada plano da fala na linha do tempo: o primeiro com a fala; um plano com `corte_em` 0,1 s antes
    da palavra (procurada depois do corte anterior); os demais dividem por peso o trecho entre os cortes vizinhos."""
    planos, pal = f["planos"], ft["palavras"]
    fixos, k = {0: ini}, 1
    for pi, p in enumerate(planos[1:], 1):
        if "corte_em" not in p:
            continue
        alvo = normalizar(p["corte_em"])
        j = next((j for j in range(k, len(pal)) if normalizar(pal[j]["palavra"]) == alvo), None)
        if j is None:
            sys.exit(f"corte_em '{p['corte_em']}' não encontrado na fala '{f['id']}'")
        fixos[pi] = pal[j]["ini"] - PRE_CORTE
        k = j + 1
    marcos = sorted(fixos) + [len(planos)]
    lim = {**fixos, len(planos): fim}
    inicios = [0.0] * len(planos)
    for a, b in zip(marcos, marcos[1:]):
        soma = sum(planos[i].get("peso", 1) for i in range(a, b))
        t = lim[a]
        for i in range(a, b):
            inicios[i] = t
            t += (lim[b] - lim[a]) * planos[i].get("peso", 1) / soma
    return inicios


def preparar():
    d = carregar()
    fps, W, H = d["fps"], d["largura"], d["altura"]
    with open(os.path.join(TMP, "tempos.json"), encoding="utf-8") as fp:
        tm = json.load(fp)
    os.makedirs(PUBLIC, exist_ok=True)
    brutos = os.path.join(RAIZ, d["pasta_brutos"])
    falas_t = {f["id"]: f for f in tm["falas"]}
    ids = [f["id"] for f in d["falas"]]
    fim_total = tm["fim_narracao"] + d["narracao"]["cauda"]

    # início de cada plano (s) → quadros, sem acumular arredondamento
    blocos = []
    for fi, f in enumerate(d["falas"]):
        ini = 0.0 if fi == 0 else falas_t[f["id"]]["palavras"][0]["ini"] - PRE_CORTE
        fim = fim_total if fi == len(ids) - 1 else falas_t[ids[fi + 1]]["palavras"][0]["ini"] - PRE_CORTE
        for pi, t in enumerate(inicios_planos(f, falas_t[f["id"]], ini, fim)):
            blocos.append((f, pi, round(t * fps)))
    q_fim_total = round(fim_total * fps)
    # um plano com `dur_max` (bruto que só serve por pouco tempo) termina antes: o plano seguinte entra mais cedo
    for bi, (f, pi, q_ini) in enumerate(blocos[:-1]):
        lim = f["planos"][pi].get("dur_max")
        if lim and blocos[bi + 1][2] - q_ini > round(lim * fps):
            nf, npi, _ = blocos[bi + 1]
            blocos[bi + 1] = (nf, npi, q_ini + round(lim * fps))

    cenas, transicoes, informacao, sons, placas = [], [], [], [], []
    snaps = []
    for bi, (f, pi, q_ini) in enumerate(blocos):
        p = f["planos"][pi]
        q = (blocos[bi + 1][2] if bi + 1 < len(blocos) else q_fim_total) - q_ini
        dur = q / fps
        cid = f"{f['id']}_{pi + 1}"
        if dur < 0.6:
            print(f"AVISO: plano {cid} ({p['fonte']}) tem só {dur:.2f} s")
        fonte = d["fontes"][p["fonte"]]
        src = os.path.join(brutos, fonte["arquivo"])
        if not os.path.exists(src):
            sys.exit(f"bruto ausente: {d['pasta_brutos']}/{fonte['arquivo']}")
        vf = []
        if fonte["girar"] != "auto":
            # o ffmpeg aplica o metadado de rotação ao decodificar; a correção leva ao giro pedido sobre o quadro bruto
            correcao = (fonte["girar"] + rotacao_meta(src)) % 360
            vf.append({0: "null", 90: "transpose=clock", 180: "hflip,vflip", 270: "transpose=cclock"}[correcao])
        vf.append(TONEMAP if fonte["hdr"] else "null")
        arq_v = f"cena_{cid}.mp4"
        cod = ["-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "15", "-pix_fmt", "yuv420p",
               "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", os.path.join(PUBLIC, arq_v)]
        if "congelar" in p or fonte.get("foto"):
            # foto ou quadro congelado: uma imagem recortada e repetida (o Ken Burns da cena dá o movimento, 100 → 104%)
            r = p["recorte"]
            quadro = os.path.join(TMP, f"quadro_{cid}.png")
            vf += [f"crop={r['w']}:{r['h']}:{r['x']}:{r['y']}", f"scale={W}:{H}:flags=lanczos"]
            if os.path.exists(quadro):
                os.remove(quadro)
            busca = ["-ss", f"{p['congelar']:.4f}"] if "congelar" in p else []  # numa foto, -ss não gera quadro
            sh(["ffmpeg", "-v", "error", "-y", *busca, "-i", src, "-vf", ",".join(vf), "-frames:v", "1", "-pix_fmt", "rgb48be", quadro])
            sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(fps), "-i", quadro, "-vf", "format=yuv420p,setsar=1",
                "-frames:v", str(q), "-an", *cod])
        else:
            if p["in"] + dur > duracao(src) - 0.05:
                sys.exit(f"plano {p['fonte']} curto demais: precisa de {dur:.2f} s a partir de {p['in']} s (fala '{f['id']}')")
            if "recorte_x" in p:
                w0, h0 = sonda(src)
                giro = rotacao_meta(src) if fonte["girar"] == "auto" else fonte["girar"]
                altura = h0 if giro % 180 == 0 else w0
                larg = round(altura * W / H / 2) * 2
                vf.append(f"crop=w={larg}:h={altura}:x='{expr_recorte(p['recorte_x'])}':y=0")
            vf.append(f"scale={W}:{H}:flags=lanczos,fps={fps},format=yuv420p,setsar=1")
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['in']:.4f}", "-i", src, "-vf", ",".join(vf), "-frames:v", str(q), "-an", *cod])
        # sem som ambiente: só a voz e os sons de marca (decisão do Diego, 19/10/2026); a trilha entra no Instagram
        cena = {"id": cid, "fonte": p["fonte"], "in": p.get("in", p.get("congelar")), "arquivo": arq_v, "quadros": q, "dur": dur,
                "audio": "mudo", "kenburns": bool(p.get("kenburns"))}
        cenas.append(cena)
        if pi == 0 and f.get("snap"):
            transicoes.append({"tipo": "snap", "entra": cid})
            snaps.append(cid)
        if "info" in p:
            informacao.append({"cena": cid, "t": 0.15, "fim": 2.2, "rotulo": p["info"]["rotulo"], "numero": p["info"]["numero"]})
        if p.get("cta"):
            c = d["placa_cta"]
            placas.append({"cena": cid, "t": c["t"], "destino": c["destino"], "modulo": c["modulo"], "tamanho": c["tamanho"]})
            sons.append({"nome": "clack", "cena": cid, "t": c["t"] + 0.28, "rel_db": -10})
        print(f"cena {cid}: {q} quadros ({dur:.2f} s)")

    # a Informação fica 2,2 s (passa por cima do corte, a parada é a mesma) e sai antes de a próxima entrar (nunca duas na tela)
    inicio_cena, t = {}, 0.0
    for c in cenas:
        inicio_cena[c["id"]] = t
        t += c["dur"]
    for a, b in zip(informacao, informacao[1:]):
        folga = inicio_cena[b["cena"]] + b["t"] - inicio_cena[a["cena"]] - 0.1
        a["fim"] = min(a["fim"], folga)

    pl = d["placa"]
    primeira = cenas[0]["id"]
    sons.insert(0, {"nome": "clack", "cena": primeira, "t": 0.28, "rel_db": -10})
    # obturador do Snap só no primeiro e no último item da lista (4.6)
    for cid in (snaps[0], snaps[-1]):
        sons.append({"nome": "obturador", "cena": cid, "t": 0.0, "rel_db": -12})

    # a narração inteira entra de uma vez; se a primeira palavra cair antes de `inicio`, o começo do arquivo é cortado
    desloc = tm["desloc"]
    corte = max(0.0, -desloc)
    dur_n = duracao(NARRACAO) - corte
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{corte:.3f}", "-i", NARRACAO, "-c:a", "pcm_s24le", os.path.join(PUBLIC, "narracao.wav")])
    audios = [{"id": "narracao", "fonte": "narracao", "in": corte, "dur": dur_n, "tipo": "voz", "audio_arquivo": "narracao.wav",
               "inicio": {"cena": primeira, "t": round(max(0.0, desloc), 3)}}]

    props = {
        "fps": fps, "largura": W, "altura": H, "cenas": cenas, "audios": audios, "transicoes": transicoes,
        "placa": {"cena": primeira, "t": pl["t"], "saida": pl["saida"], "rotulo": pl["rotulo"], "destino": pl["destino"],
                  "modulo": pl["modulo"], "tamanho": pl["tamanho"]},
        "placas": placas, "tickets": [], "informacao": informacao,
        "legendas": [{"cena": primeira, "modo": "grupo", "grupos": [g for f in tm["falas"] for g in f["grupos"]]}],
        # sem ambiente, os sons da 4.6 são relativos à voz em toda cena
        "sons": sons, "mix": {**d["mix"], "ambiente_lufs": d["mix"]["voz_lufs"]},
        "capa": {"cena": primeira, "t": d["capa"]["t"], "placa": d["capa"]["placa"]},
    }
    with open(os.path.join(TMP, "props.json"), "w", encoding="utf-8") as fp:
        json.dump(props, fp, ensure_ascii=False, indent=1)
    print(f"duração total: {sum(c['quadros'] for c in cenas) / fps:.2f} s · {len(cenas)} planos · props em _tmp/props.json")


def render():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "render", "src/index.ts", "Reel", SAIDA_BRUTA, f"--props={props}", f"--public-dir={PUBLIC}",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("render falhou")


def medir_master(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])


def master():
    """Ganho linear até −14 LUFS + limitador com sobreamostragem 4× (pico verdadeiro ≤ −1 dBTP). O vídeo é
    recodificado em CRF 17 (o Instagram recodifica de novo; o arquivo fica com cerca de metade do tamanho do render)."""
    d = carregar()
    alvo, pico = d["mix"]["master_lufs"], d["mix"]["master_pico_dbtp"]
    i0, _ = medir_master(SAIDA_BRUTA)
    ganho, teto = alvo - i0, pico - 0.4
    audio = os.path.join(TMP, "master_audio.m4a")
    for _ in range(4):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-vn", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", audio])
        i, tp = medir_master(audio)
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= tp - pico + 0.1
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_BRUTA, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow",
        "-crf", "17", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "copy", "-movflags", "+faststart", SAIDA])
    i, tp = medir_master(SAIDA)
    print(f"master: {i:.1f} LUFS integrados · pico verdadeiro {tp:.1f} dBTP → {os.path.basename(SAIDA)}")
    sh(["ffmpeg", "-v", "error", "-y", "-i", SAIDA, "-vf", "scale=540:960:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", PREVIA])


def capa():
    props = os.path.join(TMP, "props.json")
    cmd = ["npx", "remotion", "still", "src/index.ts", "CapaReel", CAPA, f"--props={props}", f"--public-dir={PUBLIC}",
           "--image-format=jpeg", "--jpeg-quality=92", "--log=warn"]
    if os.path.exists(CHROME):
        cmd.append(f"--browser-executable={CHROME}")
    if subprocess.run(cmd, cwd=REMOTION).returncode != 0:
        sys.exit("capa falhou")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    etapas = {"narracao": [narracao], "tempos": [tempos], "preparar": [preparar], "render": [render], "master": [master], "capa": [capa],
              "tudo": [narracao, tempos, preparar, render, master, capa]}
    for fn in etapas[etapa]:
        print(f"== {fn.__name__}")
        fn()
