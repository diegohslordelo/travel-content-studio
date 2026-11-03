#!/usr/bin/env python3
"""Reel "Primeiro dia em Amsterdam" · TELA VERDE (Trello; docs/FORMATOS_TRELLO.md), com o Diego recortado no canto
inferior direito e a jornada do dia 1 atrás dele. Linguagem do formato (docs/FORMATOS_REELS.md); DS V2 no Placar (pedido
do Diego para este Reel) e no CTA. Pipeline a partir do Reel da Grand-Place (branch claude/reel-bruxelas-grand-place).

Rode de dentro de reels/amsterdam-primeiro-dia/:
    python3 scripts/preparar.py      # voz e Diego recortado nos mesmos trechos → public/voz.wav, public/diego.webm
    python3 scripts/alinhar.py       # palavras com tempo (alinhamento forçado) → _tmp/palavras.json
    python3 scripts/reel.py props    # cenas.json + palavras → _tmp/props.json
    python3 scripts/reel.py broll    # trechos dos vídeos da viagem em 9:16 (mudos, HLG → SDR, velocidade real) → public/broll/
    python3 scripts/reel.py tremor   # mede o tremor de cada trecho usado (correlação de fase) → _tmp/tremor.json
    python3 scripts/reel.py sons     # faixa de efeitos (keen, PDX_*, sons do Placar) → public/sfx.wav
    python3 scripts/reel.py render   # Remotion, composição "ReelAmsterdam1"
    python3 scripts/reel.py master   # −14 LUFS integrados, pico ≤ −1 dBTP → revN/reel_amsterdam-primeiro-dia_revN.mp4
    python3 scripts/reel.py capa     # capa 1080 × 1920 (quadro do gancho completo)
    python3 scripts/reel.py quadros  # folhas de QA (um quadro por cena e um por segundo)
    python3 scripts/reel.py tudo
A revisão de saída é a da variável REV (padrão rev1).
"""
import json, os, re, shutil, subprocess, sys, unicodedata
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
REV = os.environ.get("REV", "rev1")
REMOTION = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "remotion"))
PUBLIC = os.path.join(AQUI, "public")
SONS_EXT = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "sons", "externos"))
SONS_DS = os.path.normpath(os.path.join(AQUI, "..", "..", "design-system", "sons"))
FPS = 30
SR = 48000
CHROMES = ["/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
           "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"]
CHROME = next((c for c in CHROMES if os.path.exists(c)), "")
AMBAR = "#E0AE5C"
NOME = "reel_amsterdam-primeiro-dia"
# HLG (iPhone, BT.2020) → SDR BT.709 (FORMATOS_REELS.md, 8.3: Möbius, sem lavar nem rosar)
TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"


def sh(cmd, cwd=None):
    print("  $", " ".join(cmd)[:220])
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode:
        sys.exit(f"falhou: {cmd[0]}")


def ler(n):
    return json.load(open(n, encoding="utf-8"))


def norm(w):
    w = unicodedata.normalize("NFD", w.lower().replace("\u00a0", " "))
    return re.sub(r"[^a-z ]", "", "".join(c for c in w if unicodedata.category(c) != "Mn")).replace(" ", "")


class Ancoras:
    """Resolve 'fala:palavra#n±s' (início da palavra), números e 'fim' no tempo do Reel."""

    def __init__(self, palavras, total):
        self.p = palavras
        self.total = total

    def palavra(self, ref):
        fala, resto = ref.split(":")
        n = 1
        if "#" in resto:
            resto, n = resto.split("#"); n = int(n)
        alvo = norm(resto)
        achou = [w for w in self.p if w["fala"] == fala and norm(w["texto"]) == alvo]
        if len(achou) < n:
            sys.exit(f"âncora não encontrada: {ref}")
        return achou[n - 1]

    def __call__(self, a):
        if isinstance(a, (int, float)):
            return float(a)
        m = re.match(r"^(.*?)([+-]\d+(?:\.\d+)?)?$", a.strip())
        base, delta = m.group(1), float(m.group(2) or 0)
        if base == "fim":
            return self.total + delta
        if ":" not in base:
            return float(base) + delta
        return self.palavra(base)["ini"] + delta


def contexto():
    pal = ler("_tmp/palavras.json")
    voz_s = sf.info("public/voz.wav").duration
    return pal, Ancoras(pal, voz_s), voz_s


def corrigidas(pal, corr):
    """Texto da legenda: a fala gravada, com a grafia certa dos nomes que o Whisper escreveu errado."""
    out, usadas = [], set()
    for w in pal:
        k = f"{w['fala']}:{w['texto']}"
        t = w["texto"]
        if k in corr and k not in usadas:
            t = corr[k]; usadas.add(k)
        out.append(dict(w, texto_leg=t))
    falta = set(corr) - usadas
    if falta:
        sys.exit(f"correções sem palavra: {falta}")
    return out


def legendas(spec, pal):
    """Grupos de legenda: cada texto consome o mesmo número de palavras faladas, na ordem."""
    out, k, grupos = [], 0, []
    for g in spec:
        oculto = g.startswith("~")
        toks = g.lstrip("~").split(" ")
        ws = pal[k:k + len(toks)]
        for tok, w in zip(toks, ws):
            if norm(tok.replace("*", "")) != norm(w["texto_leg"]):
                sys.exit(f"legenda fora de ordem: '{tok}' × '{w['texto_leg']}' ({w['ini']:.2f} s)")
        k += len(toks)
        grupos.append((oculto, toks, ws))
    if k != len(pal):
        sys.exit(f"legendas cobrem {k} de {len(pal)} palavras")
    for i, (oculto, toks, ws) in enumerate(grupos):
        ini = ws[0]["ini"] - 0.05
        prox = grupos[i + 1][2][0]["ini"] - 0.05 if i + 1 < len(grupos) else None
        fim = prox if prox is not None and prox - ws[-1]["fim"] < 0.6 else ws[-1]["fim"] + 0.3
        if oculto:
            continue
        palavras, destaque = [], False
        for tok in toks:
            if tok.startswith("*"):
                destaque = True
            palavras.append({"texto": tok.replace("*", ""), "destaque": destaque})
            if tok.rstrip(",.!?").endswith("*"):
                destaque = False
        out.append({"palavras": palavras, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


def medir_lufs(arq):
    import pyloudnorm as pyln
    x, sr = sf.read(arq)
    return pyln.Meter(sr).integrated_loudness(x)


def plano_cenas(c, A, total):
    """Cenas com quadro de entrada/saída, extensão para a fusão e a entrada de cada trecho no bruto."""
    inis = [A(s["ini"]) for s in c["cenas"]]
    fim_cenas = A(c["grades"][1]["ini"])
    g0 = c["grades"][0]
    pop0 = A(g0["ini"]) + g0["pop"][0]
    cenas = []
    for i, s in enumerate(c["cenas"]):
        ini = inis[i]
        fim = inis[i + 1] if i + 1 < len(inis) else fim_cenas
        prox = c["cenas"][i + 1] if i + 1 < len(inis) else None
        ext = 9 if prox and prox.get("entra") == "fusao" else 0
        v = dict(s["video"])
        if v["in"] == "continua":  # a 1ª cena continua o 1º quadro da grade (mergulho): mesmo plano, mesmo instante
            t0 = c["grades"][0]["tiles"][0]
            v["in"] = round(t0["in"] + (round(ini * FPS) - round(pop0 * FPS)) / FPS, 4)
        cenas.append({"id": s["id"], "ini_q": round(ini * FPS), "fim_q": round(fim * FPS), "ext_q": ext, "video": f"broll/{s['id']}.mp4",
                      "kb": s.get("kb", [1.0, 1.03]), "entra": s.get("entra", "corte"), **({"sai": s["sai"]} if "sai" in s else {}), "_v": v})
    return cenas


def plano_grades(c, A, total):
    out = []
    for g in c["grades"]:
        ini, fim = A(g["ini"]), A(g["fim"])
        tiles = []
        for k, t in enumerate(g["tiles"]):
            em = ini + g["pop"][0] + k * g["pop"][1]
            tiles.append({"video": f"broll/grade_{g['id']}_{k}.mp4", "em_q": round(em * FPS), "_v": t, "_nq": round(fim * FPS) - round(em * FPS)})
        e = {"ini_q": round(ini * FPS), "fim_q": round(fim * FPS), "tiles": tiles, "brilho": g["brilho"], "_id": g["id"]}
        if "mergulho" in g:
            e["mergulho_q"] = round(A(g["mergulho"]) * FPS)
        out.append(e)
    return out


def props():
    pal0, A, voz_s = contexto()
    c = ler("cenas.json")
    pal = corrigidas(pal0, c.get("correcoes", {}))
    total = voz_s
    quadros = int(round(total * FPS))
    cenas = plano_cenas(c, A, total)
    grades = plano_grades(c, A, total)
    g = c["gancho"]
    valores = [{"em": round(A(v["em"]) * 1000), "tempo": v["tempo"], "gasto": v["gasto"]} for v in c["placar"]]
    voz_lufs = medir_lufs("public/voz.wav")
    limpa = lambda d: {k: v for k, v in d.items() if not k.startswith("_")}
    p = {
        "fps": FPS, "quadros": quadros,
        "cenas": [limpa(e) for e in cenas],
        "grades": [dict(limpa(e), tiles=[limpa(t) for t in e["tiles"]]) for e in grades],
        "diego": c["diego"], "legendaY": c["legendaY"],
        "legendas": legendas(c["legendas"], pal),
        "gancho": {"linhas": g["linhas"], "tamanhos": g["tamanhos"], "tempos": [round(A(x), 3) for x in g["tempos"]],
                   "cores": [AMBAR if x == "ambar" else None for x in g["cores"]], "topos": g["topos"], "fim": round(A(g["fim"]), 3),
                   "placa": {"destino": g["placa"]["destino"], "entrada": round(A(g["placa"]["entrada"]) * 1000), "saida": round(A(g["placa"]["saida"]) * 1000)}},
        "placar": {"valores": valores, "ligar": valores[0]["em"]},
        "etiquetas": [{"ini": round(A(v["em"]) * 1000) + 50, "fim": round(A(v["em"]) * 1000) + 50 + c["etiqueta"]["dur_ms"], **v["etiqueta"]}
                      for v in c["placar"] if "etiqueta" in v],
        "etiqueta": {k: c["etiqueta"][k] for k in ("x", "y", "escala")},
        "cta": {"ini": round(A(c["grades"][1]["ini"]), 3), "rotulo": c["cta"]["rotulo"], "destino": c["cta"]["destino"],
                "entrada": round((A(c["cta"]["entrada"]) - A(c["grades"][1]["ini"])) * 1000)},
        "mix": {"voz_lufs": round(voz_lufs, 2), "clack_db_rel": -6},
        "sfx": os.path.exists(os.path.join(PUBLIC, "sfx.wav")),
        "transicoes": [{"tipo": t["tipo"], "q": round(A(t["em"]) * FPS)} for t in c["transicoes"]],
    }
    json.dump(p, open("_tmp/props.json", "w"), ensure_ascii=False)
    json.dump({"cenas": cenas, "grades": grades}, open("_tmp/plano.json", "w"), ensure_ascii=False, indent=1)
    print(f"props: {len(cenas)} cenas, {quadros} quadros ({total:.2f} s), {len(p['legendas'])} legendas, voz {voz_lufs:.1f} LUFS")
    for e in cenas:
        d = (e["fim_q"] - e["ini_q"]) / FPS
        aviso = "  ← < 2 s" if d < 2 else ("  ← > 3 s" if d > 3 else "")
        print(f"  {e['ini_q']/FPS:6.2f}–{e['fim_q']/FPS:6.2f} ({d:4.2f} s) {e['entra']:8} {e['id']:22} {e['_v']['fonte']} in {e['_v']['in']}{aviso}")
    return p


def dims(arq):
    """Largura × altura como o vídeo é exibido (com a rotação do iPhone aplicada)."""
    r = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                                   "-show_entries", "format=duration", "-of", "json", arq], capture_output=True, text=True).stdout)
    s = r["streams"][0]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    w, h = s["width"], s["height"]
    if abs(rot) == 90:
        w, h = h, w
    return w, h, float(r["format"]["duration"])


def extrair(v, nq, saida, W, H):
    """Recorta o trecho do bruto em W × H (9:16), com o número exato de quadros, mudo, HLG → SDR, na velocidade real.
    Nunca estica o take: se o trecho não cabe no plano, para com erro."""
    arq = f"fonte/acervo/{v['fonte']}.MOV"
    w, h, dur = dims(arq)
    t0 = float(v["in"])
    if t0 + nq / FPS > dur - 0.05:
        sys.exit(f"{saida}: o trecho ({t0:.2f} + {nq / FPS:.2f} s) passa do fim do plano {v['fonte']} ({dur:.2f} s)")
    if w > h:  # horizontal: recorte 9:16 na altura toda, com o centro em 'foco' (e panorâmica até 'foco_fim')
        cw = round(h * 9 / 16); cw -= cw % 2
        f0 = v.get("foco", 0.5); f1 = v.get("foco_fim", f0)
        x0 = min(max(0, f0 * w - cw / 2), w - cw); x1 = min(max(0, f1 * w - cw / 2), w - cw)
        dt = nq / FPS
        xexp = f"{x0:.1f}" if abs(x1 - x0) < 1 else f"'{x0:.1f}+({x1 - x0:.1f})*min(1,t/{dt:.3f})'"
        crop = f"crop={cw}:{h}:{xexp}:0,"
    else:
        # vertical: entra inteiro; 'zoom' + 'foco_y' recortam uma parte (ex.: tirar logos de redes sociais da base do quadro)
        z = v.get("zoom", 1.0)
        crop = f"crop=iw/{z}:ih/{z}:(iw-iw/{z})*{v.get('foco', 0.5)}:(ih-ih/{z})*{v.get('foco_y', 0.5)}," if z > 1 else ""
    base = f"{TM},{crop}scale={W}:{H}:flags=lanczos"
    estab = ""
    if v.get("estabilizar"):
        # selfie na mão: estabilização em 2 passos (vidstab), aproximação fixa de 6% para esconder as bordas; velocidade real
        trf = f"_tmp/vidstab_{os.path.basename(saida)}.trf"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{nq / FPS + 0.2:.3f}", "-i", arq, "-an", "-vf",
            f"{base},vidstabdetect=shakiness=7:accuracy=15:result={trf}", "-f", "null", "-"])
        estab = f",vidstabtransform=input={trf}:smoothing=18:optzoom=0:zoom=6:interpol=bicubic,unsharp=5:5:0.4"
    vf = f"{base}{estab},fps={FPS},setsar=1"
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", arq, "-an", "-vf", vf, "-frames:v", str(nq), "-c:v", "libx264", "-crf", "15",
        "-preset", "fast", "-pix_fmt", "yuv420p", saida])


def broll():
    """SO=id1,id2 refaz só essas cenas (e nenhuma grade)."""
    pl = ler("_tmp/plano.json")
    so = os.environ.get("SO")
    os.makedirs(os.path.join(PUBLIC, "broll"), exist_ok=True)
    for e in pl["cenas"]:
        if so and e["id"] not in so.split(","):
            continue
        extrair(e["_v"], e["fim_q"] - e["ini_q"] + e["ext_q"] + 2, os.path.join(PUBLIC, e["video"]), 1080, 1920)
    for g in ([] if so else pl["grades"]):
        for t in g["tiles"]:
            extrair(t["_v"], t["_nq"] + 2, os.path.join(PUBLIC, t["video"]), 360, 640)


def tremor():
    """Tremor de cada trecho usado: deslocamento global entre quadros (correlação de fase, 30 qps, todos os quadros, 144 × 256 no recorte já
    aplicado) e a sua ACELERAÇÃO (diferença entre deslocamentos seguidos). Panorâmica ou travelling suave tem aceleração
    baixa mesmo andando rápido; mão tremendo tem aceleração alta. Medida: p90 da aceleração em px a 144 de largura.
    Referência medida nos planos do Reel: tripé/apoio ≈ 0,1–0,3; panorâmica suave ≈ 0,3–0,9; tremido > 1,5."""
    import cv2
    pl = ler("_tmp/plano.json")
    res = {}
    itens = [(e["id"], e["_v"], (e["fim_q"] - e["ini_q"]) / FPS) for e in pl["cenas"]] + \
            [(f"{g['_id']}_{k}", t["_v"], t["_nq"] / FPS) for g in pl["grades"] for k, t in enumerate(g["tiles"])]
    for nome, v, dur in itens:
        if v.get("estabilizar"):
            arq_ok = next(x for x in [os.path.join(PUBLIC, "broll", nome + ".mp4"), os.path.join(PUBLIC, "broll", "grade_" + nome + ".mp4")] if os.path.exists(x))
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq_ok, "-vf", "mpdecimate=hi=64*4:lo=64:frac=0.1,scale=144:256,format=gray", "-fps_mode", "vfr",
                                "-f", "rawvideo", "-"], capture_output=True)
        # no bruto, na taxa original (24 qps): a conversão para 30 qps repete quadros e cria aceleração falsa
        arq = f"fonte/acervo/{v['fonte']}.MOV"
        w, h, _ = dims(arq)
        crop = ""
        if w > h:
            cw = round(h * 9 / 16); cw -= cw % 2
            f0 = v.get("foco", 0.5); f1 = v.get("foco_fim", f0)
            x0 = min(max(0, f0 * w - cw / 2), w - cw); x1 = min(max(0, f1 * w - cw / 2), w - cw)
            crop = f"crop={cw}:{h}:'{x0:.1f}+({x1 - x0:.1f})*min(1,t/{dur:.3f})':0,"
        if not v.get("estabilizar"):
            r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(v['in']):.3f}", "-t", f"{dur:.3f}", "-i", arq, "-vf", f"{crop}scale=144:256,format=gray",
                                "-f", "rawvideo", "-"], capture_output=True)
        q = np.frombuffer(r.stdout, np.uint8)
        n = len(q) // (144 * 256)
        q = q[: n * 144 * 256].reshape(n, 256, 144).astype(np.float32)
        jan = cv2.createHanningWindow((144, 256), cv2.CV_32F)
        d = np.array([cv2.phaseCorrelate(q[i], q[i + 1], jan)[0] for i in range(n - 1)])
        d = np.clip(d, -40, 40)
        ac = np.linalg.norm(np.diff(d, axis=0), axis=1)
        res[nome] = {"p50": round(float(np.median(ac)), 2), "p90": round(float(np.percentile(ac, 90)), 2), "vel": round(float(np.median(np.linalg.norm(d, axis=1))), 2)}
        flag = "  ← TREMIDO" if res[nome]["p90"] > 1.5 else ""
        print(f"  {nome:26} aceleração p50 {res[nome]['p50']:.2f} · p90 {res[nome]['p90']:.2f} · velocidade {res[nome]['vel']:.2f}{flag}")
    json.dump(res, open("_tmp/tremor.json", "w"), indent=1)


def carregar_som(arq):
    y, sr = sf.read(arq)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if sr != SR:
        from scipy.signal import resample_poly
        y = resample_poly(y, SR, sr)
    return y


def sons():
    import pyloudnorm as pyln
    pal, A, voz_s = contexto()
    c = ler("cenas.json")
    n = int(voz_s * SR)
    pista = np.zeros(n + SR)
    med = pyln.Meter(SR)
    voz_lufs = medir_lufs("public/voz.wav")
    eventos = []
    for ev in c["sons"]:
        arq = os.path.join(SONS_EXT, ev["som"] + ".wav")
        eventos.append({"arq": arq, "som": ev["som"], "t": A(ev["em"]), "alinhar": ev.get("alinhar", "inicio"), "rel_db": ev["rel_db"], "nota": ev.get("nota", "")})
    # sons do Placar (como no vlog): moeda em soma de gasto, tick quando só a hora gira; o 1º valor (ligar) não tem som
    sp = c["sons_placar"]
    for a, b in zip(c["placar"], c["placar"][1:]):
        soma = a["gasto"] != b["gasto"]
        eventos.append({"arq": os.path.join(SONS_DS, "PD_moeda_v1.wav" if soma else "PD_tick_v1.wav"), "som": "PD_moeda" if soma else "PD_tick",
                        "t": A(b["em"]) + (0.05 if soma else 0), "alinhar": "inicio", "rel_db": sp["moeda_db"] if soma else sp["tick_db"],
                        "nota": f"Placar {b['tempo']} · {b['gasto']}", "placar": True, "soma": soma})
    # posição real de cada som (início no arquivo de áudio) e o instante que conta para o intervalo de 1,5 s (pico ou início)
    for ev in eventos:
        y = carregar_som(ev["arq"])
        ev["y"] = y
        t = ev["t"]
        if ev["alinhar"] == "pico":
            env = np.convolve(np.abs(y), np.ones(480) / 480, "same")
            t -= int(np.argmax(env)) / SR
        elif ev["alinhar"] == "fim":
            t -= len(y) / SR
        ev["ini"] = t
        ev["marca"] = ev["t"]  # o instante percebido (corte, pico, palavra)
    # regra: no máximo 1 efeito a cada 1,5 s. Um tick do Placar perto de outro efeito sai; uma moeda perto de outro efeito
    # sai também, a não ser que o outro seja um tick (que sai no lugar dela). O riser é subida até o corte: não conta.
    eventos.sort(key=lambda e: e["marca"])
    conta = [e for e in eventos if e["som"] != "PDX_riser"]
    fora = set()
    for i, e in enumerate(conta):
        for f in conta[i + 1:]:
            if f["marca"] - e["marca"] >= 1.5:
                break
            if id(e) in fora or id(f) in fora:
                continue
            # quem sai: tick antes de moeda, Placar antes de efeito de transição
            cand = sorted([e, f], key=lambda x: (0 if x["som"] == "PD_tick" else 1 if x.get("placar") else 2))
            fora.add(id(cand[0]))
    feitos = []
    for ev in eventos:
        if id(ev) in fora:
            feitos.append({"som": ev["som"], "em_s": round(ev["marca"], 3), "rel_db": ev["rel_db"], "nota": ev["nota"] + " (mudo: < 1,5 s de outro efeito)"})
            continue
        y = ev["y"]
        lufs = med.integrated_loudness(np.concatenate([y, np.zeros(SR)]))
        y = y * 10 ** ((voz_lufs + ev["rel_db"] - lufs) / 20)
        k = int(round(ev["ini"] * SR))
        a0 = max(0, -k)
        seg = y[a0:]
        k = max(0, k)
        seg = seg[:len(pista) - k]
        pista[k:k + len(seg)] += seg
        feitos.append({"som": ev["som"], "em_s": round(ev["marca"], 3), "rel_db": ev["rel_db"], "nota": ev["nota"]})
    pista = pista[:n + int(0.05 * SR)]
    sf.write(os.path.join(PUBLIC, "sfx.wav"), np.stack([pista, pista], axis=1).astype(np.float32) * 0.7071, SR, subtype="FLOAT")
    json.dump(feitos, open("_tmp/sons.json", "w"), ensure_ascii=False, indent=1)
    for x in feitos:
        print(f"  {x['em_s']:6.2f} s  {x['som']:16} {x['rel_db']:+d} dB  {x['nota']}")


def render():
    os.makedirs("_tmp", exist_ok=True)
    cmd = ["npx", "remotion", "render", "src/index.ts", "ReelAmsterdam1", os.path.join(AQUI, "_tmp", "reel_sem_master.mov"),
           f"--props={os.path.join(AQUI, '_tmp', 'props.json')}", f"--public-dir={PUBLIC}", "--concurrency=4",
           "--codec=h264", "--crf=14", "--audio-codec=pcm-16", "--log=warn", "--timeout=120000"]
    if CHROME:
        cmd.append(f"--browser-executable={CHROME}")
    cmd += sys.argv[2:]
    sh(cmd, cwd=REMOTION)


def medir(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    return i, tp


def master():
    os.makedirs(REV, exist_ok=True)
    ent = "_tmp/reel_sem_master.mov"
    sai = f"{REV}/{NOME}_{REV}.mp4"
    i0, _ = medir(ent)
    ganho, alvo, pico = -14.0 - i0, -14.0, -1.0
    teto = pico - 0.4
    for _ in range(6):
        af = f"volume={ganho:.2f}dB,aresample=192000,alimiter=limit={10 ** (teto / 20):.4f}:attack=1:release=60:level=false,aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", sai])
        i, tp = medir(sai)
        print(f"  master: {i:.2f} LUFS, pico {tp:.2f} dBTP (ganho {ganho:.2f})")
        if abs(i - alvo) <= 0.1 and tp <= pico:
            break
        ganho += alvo - i
        if tp > pico:
            teto -= 0.3
    sh(["ffmpeg", "-v", "error", "-y", "-i", sai, "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", f"{REV}/{NOME}_{REV}_previa.mp4"])


def capa():
    """Capa: o quadro em que o gancho está completo (FORMATOS_REELS.md, 4.1), tirado do vídeo final."""
    p = ler("_tmp/props.json")
    t = p["gancho"]["placa"]["saida"] / 1000 - 0.1  # tudo na tela (texto e placa), antes da saída da placa e do mergulho
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", f"{REV}/{NOME}_{REV}.mp4", "-frames:v", "1", "-q:v", "2", f"{REV}/capa_amsterdam-primeiro-dia_{REV}.jpg"])


def quadros():
    p = ler("_tmp/props.json")
    vid = f"{REV}/{NOME}_{REV}.mp4"
    d = f"{REV}/qa_frames"
    os.makedirs(d, exist_ok=True)
    tmp = "_tmp/qa"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    marcos = [("gancho", 1.4)] + [(c["id"], (c["ini_q"] + c["fim_q"]) / 2 / FPS) for c in p["cenas"]] + [("cta", p["quadros"] / FPS - 0.5)]
    for i, (nome, t) in enumerate(marcos):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", vid, "-frames:v", "1", "-vf",
            f"scale=360:640,drawtext=text='{i + 1} {nome} {t:.1f}s':x=8:y=8:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6", f"{tmp}/c{i:02d}.png"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/c%02d.png", "-vf", "tile=8x3:padding=4", "-frames:v", "1", f"{d}/cenas.jpg"])
    sh(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vf", "fps=1,scale=270:480,drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=10x7:padding=3",
        "-frames:v", "1", f"{d}/um_por_segundo.jpg"])


if __name__ == "__main__":
    passo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    passos = {"props": props, "broll": broll, "tremor": tremor, "sons": sons, "render": render, "master": master, "capa": capa, "quadros": quadros}
    if passo == "tudo":
        for k in ["props", "broll", "tremor", "sons", "props", "render", "master", "capa", "quadros"]:
            passos[k]()
    else:
        passos[passo]()
