"""Reel "Basílica do Sangue Sagrado" (Bruges) · REV4 · preparação para o Remotion.

Lê edicao.json, transcricao_alinhada.json e cenas.json e gera, em _tmp/public/ (fora do git):
  voz.wav      voz do Diego: as 5 tomadas do quarto, cortadas só no silêncio, sem acelerar, sem cortar palavra
  fala.mp4     vídeo do Diego cortado nos MESMOS trechos da voz (boca em sincronia), HDR → SDR
  broll/*.mp4  planos do acervo de Bruges (mudos, recortados para a camada, HDR → SDR)
  img/*.jpg    fotos da web
  sfx.wav      efeitos de transição (kit PDX_*, volumes da REFERENCIA_EDICAO_FORMATOS 4.1)
  props.json   cenas em quadros, legendas, gancho, mapas e CTA
Roda de dentro de reels/bruges-sangue/rev4:  python scripts/preparar.py
O Claude não escuta áudio: tudo aqui é medido; a escuta é do Diego.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

SR = 48000
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(AQUI, "_tmp")
PUB = os.path.join(TMP, "public")
REPO = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))

ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
alin = json.load(open(os.path.join(AQUI, "transcricao_alinhada.json"), encoding="utf-8"))
cen = json.load(open(os.path.join(AQUI, "cenas.json"), encoding="utf-8"))
FPS = ed["fps"]
MIN_CENA = 2.0  # s: padrão; o cenas.json pode subir (REV4: 3 s, pedido do Diego)
# quadros que a cena que sai continua na tela por baixo/por cima da que entra, por tipo de transição
SAIDA_Q = {"whip": 8, "dissolve": 12, "mergulho": 14, "zoom": 12, "empurrao": 19}
FONTE = os.path.normpath(os.path.join(AQUI, ed["fonte_dir"]))
ACERVO = os.path.normpath(os.path.join(AQUI, cen["acervo_dir"]))

# HLG (iPhone) → SDR BT.709, tone mapping Möbius (FORMATOS_REELS 8.3.5)
TONEMAP = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd):
    subprocess.run(cmd, check=True)


def carregar(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def nivel_evento(x):
    """Nível de um som curto: RMS dos 100 ms mais fortes (mesma medida para voz e efeitos)."""
    n = int(0.1 * SR)
    if len(x) <= n:
        return rms_db(x)
    v = [rms_db(x[i:i + n]) for i in range(0, len(x) - n, n // 4)]
    return float(max(v))


# ---------------------------------------------------------------- voz e vídeo do Diego
RUIDO_ALVO = 52  # dB abaixo do loudness da fala
BANDAS = [(200, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000)]  # timbre comparado entre tomadas


def espectro(x):
    """Energia por banda (dB, relativa à banda mais forte) das palavras de uma tomada."""
    S = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    b = np.array([10 * np.log10(S[(fr >= lo) & (fr < hi)].sum() + 1e-20) for lo, hi in BANDAS])
    return b - b.max()


def piso_ruido(x):
    n = int(0.05 * SR)
    v = np.array([rms_db(x[i:i + n]) for i in range(0, len(x) - n, n)])
    return float(np.percentile(v[v > -100], 5))


def lufs_de(x):
    arq = os.path.join(TMP, "_medir.wav")
    sf.write(arq, x.astype(np.float32), SR)
    return medir_lufs(arq)


def filtrar(x, filtros):
    ent, sai = os.path.join(TMP, "_ent.wav"), os.path.join(TMP, "_sai.wav")
    sf.write(ent, x.astype(np.float32), SR)
    sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-af", filtros, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", sai])
    y, _ = sf.read(sai)
    return y[:len(x)] if len(y) >= len(x) else np.concatenate([y, np.zeros(len(x) - len(y))])


def voz_e_fala():
    """REV4: cada tomada é tratada sozinha para as 5 soarem iguais (pedido do Diego, 29/10/2026):
    1. equalização que aproxima o timbre de cada tomada da média das 5 (bandas de 200 Hz a 8 kHz, ±4 dB, só diferenças ≥ 1 dB);
    2. redução de ruído proporcional ao ruído de fundo da tomada (a mais ruidosa recebe mais);
    3. ganho até o mesmo loudness de fala (LUFS medido só nas palavras).
    Depois: compressor suave (2:1) na voz inteira e ganho linear até −16 LUFS (o master leva a −14)."""
    fade = int(ed["audio"]["fade_ms"] / 1000 * SR)
    tomadas, trechos, palavras, t = [], [], [], 0.0
    for fa in ed["falas"]:
        x = carregar(os.path.join(FONTE, ed["fontes"][fa["fonte"]]))
        nq = round((fa["out"] - fa["in"]) * FPS)  # número inteiro de quadros: o vídeo é cortado igual
        a = fa["in"]
        n = int(round(nq / FPS * SR))
        seg = x[int(round(a * SR)):int(round(a * SR)) + n].copy()
        if len(seg) < n:  # trilha do iPhone acaba antes do vídeo (FORMATOS_REELS 10.2): completa com silêncio após fade
            seg = np.concatenate([seg, np.zeros(n - len(seg))])
        ws = alin[fa["fonte"]]
        # palavras no tempo do trecho (para medir só a fala)
        rel = [(int((w["ini"] - a) * SR), int((w["fim"] - a) * SR)) for w in ws]
        seg[:fade] *= np.linspace(0, 1, fade)
        fim_real = len(x) - int(round(a * SR))
        q = int(0.025 * SR) if fa.get("fim_suave") else fade
        fim = min(n, fim_real)
        seg[fim - q:fim] *= np.linspace(1, 0, q)
        seg[fim:] = 0
        tomadas.append({"fa": fa, "seg": seg, "rel": rel, "bruto": x, "palavras_bruto": [(w["ini"], w["fim"]) for w in ws]})
        trechos.append({"fala": fa["id"], "fonte": fa["fonte"], "in": a, "out": round(a + nq / FPS, 4), "inicio": round(t, 4), "quadros": nq})
        for w in ws:
            palavras.append({"fala": fa["id"], "texto": w["texto"], "ini": round(t + w["ini"] - a, 3), "fim": round(t + w["fim"] - a, 3), "prob": w["prob"]})
        t += nq / FPS
    os.makedirs(TMP, exist_ok=True)

    def so_fala(tm, y=None):
        y = tm["seg"] if y is None else y
        return np.concatenate([y[max(0, i):j] for i, j in tm["rel"]])

    # 1. timbre: média das tomadas como referência
    esp = {tm["fa"]["id"]: espectro(so_fala(tm)) for tm in tomadas}
    ref = np.mean(list(esp.values()), axis=0)
    relatorio = []
    tratadas = []
    import noisereduce as nrd
    for tm in tomadas:
        fid = tm["fa"]["id"]
        antes = {"lufs_fala": round(lufs_de(so_fala(tm)), 1), "piso_db": round(piso_ruido(tm["seg"]), 1), "timbre_vs_media_db": [round(v, 1) for v in esp[fid] - ref]}
        # 2. ruído: perfil aprendido no trecho mais quieto da própria tomada (0,4 s longe de qualquer palavra);
        #    a redução é a que leva o ruído a ≈ RUIDO_ALVO dB abaixo da fala (limitada a 92% para não criar artefato)
        x, n = tm["bruto"], int(0.4 * SR)
        livre = [i for i in range(int(0.1 * SR), len(x) - n, int(0.05 * SR))
                 if not any(i / SR - 0.15 < b and (i + n) / SR + 0.15 > a for a, b in tm["palavras_bruto"])]
        amostra = min((x[i:i + n] for i in livre), key=rms_db)
        abaixo = antes["lufs_fala"] - rms_db(amostra)  # quantos dB o ruído fica abaixo da fala
        prop = round(min(0.92, max(0.4, 1 - 10 ** (-(RUIDO_ALVO - abaixo) / 20))), 2)
        y = nrd.reduce_noise(y=tm["seg"], sr=SR, y_noise=amostra, stationary=True, prop_decrease=prop, n_fft=2048)
        y = filtrar(y, f"highpass=f={ed['audio']['passa_alta_hz']}")
        # 1. timbre: equalização em 2 passadas até a tomada ficar a ±1 dB da média
        eq_total = np.zeros(len(BANDAS))
        base = y
        for _ in range(2):
            d = ref - espectro(so_fala(tm, y))
            eq_total = np.clip(eq_total + np.where(np.abs(d) >= 0.7, d, 0), -5, 5)
            eq = [f"equalizer=f={round((lo * hi) ** 0.5)}:t=o:w=1:g={g:.1f}" for (lo, hi), g in zip(BANDAS, eq_total) if abs(g) >= 0.7]
            y = filtrar(base, ",".join(eq)) if eq else base
        tratadas.append((tm, y))
        r_ruido = nrd.reduce_noise(y=amostra, sr=SR, y_noise=amostra, stationary=True, prop_decrease=prop, n_fft=2048)
        relatorio.append({"fala": fid, "fonte": tm["fa"]["fonte"], "antes": antes, "eq": eq, "reducao_ruido": prop,
                          "_ruido_antes": rms_db(amostra) - antes["lufs_fala"], "_ruido": rms_db(r_ruido[n // 4:])})
    # 3. mesmo loudness de fala em todas as tomadas
    niveis = [lufs_de(so_fala(tm, y)) for tm, y in tratadas]
    alvo = float(np.mean(niveis))
    pedacos = []
    for (tm, y), nv, r in zip(tratadas, niveis, relatorio):
        g = alvo - nv
        y = y * 10 ** (g / 20)
        pedacos.append(y)
        r["ganho_db"] = round(g, 1)
    voz = np.concatenate(pedacos)
    bruta = os.path.join(TMP, "voz_igualada.wav")
    sf.write(bruta, voz.astype(np.float32), SR)
    # compressor suave: aproxima palavras fortes e fracas sem "bombear" (ataque 8 ms, retorno 160 ms)
    sh(["ffmpeg", "-v", "error", "-y", "-i", bruta, "-af", "acompressor=threshold=-26dB:ratio=2:attack=8:release=160:makeup=1:knee=4",
        "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", os.path.join(TMP, "voz_tratada.wav")])
    v, _ = sf.read(os.path.join(TMP, "voz_tratada.wav"))
    v = v[:len(voz)]
    lufs = medir_lufs(os.path.join(TMP, "voz_tratada.wav"))
    v = v * 10 ** ((-16 - lufs) / 20)
    for r in relatorio:  # ruído de fundo relativo à fala (dB abaixo do loudness da fala): antes e depois
        r["antes"]["ruido_abaixo_da_fala_db"] = round(-r.pop("_ruido_antes"), 1)
        r["ruido_abaixo_da_fala_db"] = round(-((r.pop("_ruido") + r["ganho_db"] + (-16 - lufs)) - (-16)), 1)
    sf.write(os.path.join(PUB, "voz.wav"), v.astype(np.float32), SR)
    # medição depois do tratamento, na voz final
    k = 0
    for tm, r in zip(tomadas, relatorio):
        y = v[k:k + len(tm["seg"])]
        k += len(tm["seg"])
        r["depois"] = {"lufs_fala": round(lufs_de(so_fala(tm, y)), 1), "piso_db": round(piso_ruido(y), 1),
                       "timbre_vs_media_db": None}
        r["_esp"] = espectro(so_fala(tm, y))
    ref2 = np.mean([r["_esp"] for r in relatorio], axis=0)
    for r in relatorio:
        r["depois"]["timbre_vs_media_db"] = [round(x, 1) for x in r.pop("_esp") - ref2]
    json.dump(relatorio, open(os.path.join(AQUI, "voz_medicao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"trechos": trechos, "palavras": palavras}, open(os.path.join(TMP, "voz.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # vídeo do Diego: mesmos trechos, 1080 × 1920, 30 qps, SDR
    partes = []
    for i, tr in enumerate(trechos):
        p = os.path.join(TMP, f"fala_{i}.mp4")
        if not os.path.exists(p):
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{tr['in']:.4f}", "-i", os.path.join(FONTE, ed["fontes"][tr["fonte"]]),
                "-vf", f"{TONEMAP},scale=1080:1920:flags=lanczos,fps={FPS}", "-frames:v", str(tr["quadros"]), "-an", *X264, p])
        partes.append(p)
    lst = os.path.join(TMP, "fala.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in partes))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(PUB, "fala.mp4")])
    return trechos, palavras, t


def medir_lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


# ---------------------------------------------------------------- âncoras
def resolver(anc, palavras):
    """'f2:Bruges', 'f2:que#3', 'f3:mas-0.05', 'fim', número em s. Devolve segundos no tempo do Reel."""
    if isinstance(anc, (int, float)):
        return float(anc)
    m = re.match(r"^(f\d):([^#+\-]+)(?:#(\d+))?([+\-][\d.]+)?$", anc)
    if not m:
        raise ValueError(anc)
    fala, pal, n, desl = m.group(1), m.group(2), int(m.group(3) or 1), float(m.group(4) or 0)
    achadas = [w for w in palavras if w["fala"] == fala and limpa(w["texto"]) == limpa(pal)]
    if len(achadas) < n:
        raise ValueError(f"âncora não achada: {anc}")
    return achadas[n - 1]["ini"] + desl


def limpa(s):
    return re.sub(r"[^\wÀ-ÿ]", "", s.lower())


# ---------------------------------------------------------------- planos do acervo
def broll(c, ini_q, fim_q):
    """Recorta o trecho do plano do acervo na proporção da camada (tela dividida 1080×900 ou cheia 1080×1920)."""
    b = cen["broll"][c["arquivo"]]
    w, h = (1080, 900) if c["layout"] == "split" else (1080, 1920)
    nq = fim_q - ini_q
    dur = nq / FPS
    if b["ini"] + dur > b["fim_limpo"] + 1e-6:
        raise SystemExit(f"plano curto demais: {c['id']} precisa de {dur:.2f} s de {c['arquivo']} (limpo até {b['fim_limpo']})")
    nome = f"broll/{c['id']}.mp4"
    out = os.path.join(PUB, nome)
    # recorte: o plano de origem (3840×2160, paisagem) é cortado em torno de foco_x (0–1)
    fx = c.get("foco_x", b.get("foco_x", 0.5))
    crop = f"crop=w='min(iw,ih*{w}/{h})':h='min(ih,iw*{h}/{w})':x='(iw-min(iw,ih*{w}/{h}))*{fx}':y='(ih-min(ih,iw*{h}/{w}))*0.5'"
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['ini']:.3f}", "-i", os.path.join(ACERVO, c["arquivo"]),
        "-vf", f"{TONEMAP},{crop},scale={w}:{h}:flags=lanczos,fps={FPS}", "-frames:v", str(nq), "-an", *X264, out])
    return nome


# ---------------------------------------------------------------- legendas
LARGURA_MAX = 800  # px; 540 + 808/2 = 944 (limite direito da zona segura)
_fonte = None


def largura_legenda(txt):
    """Largura real da legenda (Inter 800, 66 px), pela métrica da fonte usada no render."""
    global _fonte
    if _fonte is None:
        from fontTools.ttLib import TTFont
        from PIL import ImageFont
        ttf = os.path.join(TMP, "inter800.ttf")
        if not os.path.exists(ttf):
            f = TTFont(os.path.join(REPO, "design-system", "remotion", "node_modules", "@fontsource", "inter", "files", "inter-latin-800-normal.woff2"))
            f.flavor = None
            f.save(ttf)
        _fonte = ImageFont.truetype(ttf, 66)
    return _fonte.getlength(txt)


FUNCIONAIS = {"de", "da", "do", "das", "dos", "a", "o", "as", "os", "e", "que", "em", "na", "no", "um", "uma", "ao", "pela", "pelo", "com", "para", "se", "me", "é", "seu", "sua", "como"}


def grupos_legenda(palavras, destaques, troca, quebrar_antes=()):
    """1 a 4 palavras, ~24 caracteres, sempre 1 linha; custo mínimo por frase (FORMATOS_REELS 6).
    quebrar_antes: âncoras de palavra ('f2:em#1') que sempre abrem grupo novo."""
    antes = {(round(resolver(x, palavras), 3)) for x in quebrar_antes}  # 'f2:em#1' = 1ª ocorrência
    frases, atual = [], []
    for w in palavras:
        if atual and round(w["ini"], 3) in antes:
            frases.append(atual)
            atual = []
        atual.append(w)
        if re.search(r"[.?!,]$", w["texto"]) or w is palavras[-1]:
            frases.append(atual)
            atual = []
    grupos = []
    for fr in frases:
        n = len(fr)
        custo = [0.0] + [1e9] * n
        de = [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(max(0, j - 4), j):
                g = fr[i:j]
                txt = re.sub(r"[,.]", "", " ".join(troca.get(limpa(x["texto"]), x["texto"]) for x in g))
                c = (len(txt) - 18) ** 2 / 20
                if largura_legenda(txt) > LARGURA_MAX:  # centrada em x 540, a linha tem de caber até x 944 (CLAUDE.md 14.13)
                    c += 400
                if limpa(g[-1]["texto"]) in FUNCIONAIS and j < n:
                    c += 60
                if any(limpa(x["texto"]) == "e" for x in g[1:]):
                    c += 40
                if custo[i] + c < custo[j]:
                    custo[j], de[j] = custo[i] + c, i
        cortes, j = [], n
        while j > 0:
            cortes.append((de[j], j))
            j = de[j]
        for i, j in reversed(cortes):
            grupos.append(fr[i:j])
    out = []
    for k, g in enumerate(grupos):
        ini = g[0]["ini"] - 0.05
        fim = grupos[k + 1][0]["ini"] - 0.05 if k + 1 < len(grupos) else g[-1]["fim"] + 0.4
        fim = min(fim, g[-1]["fim"] + 0.6)  # não deixa legenda parada no respiro longo
        ps = []
        for x in g:
            t = troca.get(limpa(x["texto"]), x["texto"])
            t = re.sub(r"[,.]$", "", t)
            ps.append({"texto": t, "ini": x["ini"], "fim": x["fim"], "destaque": limpa(x["texto"]) in destaques.get(x["fala"], [])})
        out.append({"palavras": ps, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


# ---------------------------------------------------------------- mapas (Natural Earth 1:50m via world-atlas, domínio público)
def mapas():
    topo = json.load(open(os.path.join(AQUI, "dados", "countries-50m.json")))
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for a in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def anel(idx):
        pts = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts += seg if not pts else seg[1:]
        return pts

    paises = {}
    for g in topo["objects"]["countries"]["geometries"]:
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]] if g["type"] == "Polygon" else []
        paises[g["properties"]["name"]] = [[anel(r) for r in p] for p in polys]

    def projeta(caixa, w, h):
        lon0, lat0, lon1, lat1 = caixa
        k = np.cos(np.radians((lat0 + lat1) / 2))
        esc = min(w / ((lon1 - lon0) * k), h / (lat1 - lat0))
        ox = (w - (lon1 - lon0) * k * esc) / 2
        oy = (h - (lat1 - lat0) * esc) / 2
        return lambda lon, lat: (round(ox + (lon - lon0) * k * esc, 1), round(oy + (lat1 - lat) * esc, 1))

    def caminhos(caixa, w, h, destaque):
        p = projeta(caixa, w, h)
        lon0, lat0, lon1, lat1 = caixa
        saida = []
        for nome, polys in paises.items():
            d = []
            for poly in polys:
                for r in poly:
                    if not any(lon0 - 8 < lo < lon1 + 8 and lat0 - 8 < la < lat1 + 8 for lo, la in r):
                        continue
                    xy = [p(lo, la) for lo, la in r]
                    d.append("M" + "L".join(f"{x},{y}" for x, y in xy) + "Z")
            if d:
                saida.append({"nome": nome, "d": "".join(d), "destaque": nome in destaque})
        return saida, p

    BRUGES = (3.2247, 51.2093)
    JERUSALEM = (35.2137, 31.7683)
    m1, p1 = caminhos((-1.5, 48.6, 8.5, 53.6), 1080, 900, ["Belgium"])
    m2, p2 = caminhos((-6, 27.5, 41, 57.5), 1080, 1920, [])
    return {
        "belgica": {"w": 1080, "h": 900, "paises": m1, "bruges": p1(*BRUGES)},
        "rota": {"w": 1080, "h": 1920, "paises": m2, "bruges": p2(*BRUGES), "jerusalem": p2(*JERUSALEM)},
    }


# ---------------------------------------------------------------- efeitos sonoros
def efeitos(sons, total_q, ref_voz):
    n = int(total_q / FPS * SR) + SR
    mix = np.zeros(n)
    dirx = os.path.join(REPO, "design-system", "sons", "externos")
    usados = []
    for s in sons:
        x, sr = sf.read(os.path.join(dirx, s["arquivo"]))
        if x.ndim > 1:
            x = x.mean(axis=1)
        if sr != SR:  # parte do kit está em 192 kHz
            from math import gcd
            from scipy.signal import resample_poly
            k = gcd(SR, sr)
            x = resample_poly(x, SR // k, sr // k)
        g = ref_voz + s["rel_db"] - nivel_evento(x)
        x = x * 10 ** (g / 20)
        # o pico do som cai no instante pedido (pico do movimento), não o começo do arquivo
        pico = int(np.argmax(np.abs(x))) if s.get("alinhar") == "pico" else 0
        i = int(s["t"] * SR) - pico
        if s.get("alinhar") == "fim":
            i = int(s["t"] * SR) - len(x)
        i = max(0, i)
        mix[i:i + len(x)] += x[:n - i]
        usados.append({**s, "ganho_db": round(g, 1)})
    sf.write(os.path.join(PUB, "sfx.wav"), mix.astype(np.float32), SR)
    return usados


# ---------------------------------------------------------------- montagem
def main():
    os.makedirs(os.path.join(PUB, "broll"), exist_ok=True)
    os.makedirs(os.path.join(PUB, "img"), exist_ok=True)
    trechos, palavras, total = voz_e_fala()
    voz_q = sum(t["quadros"] for t in trechos)
    quadros = voz_q + round(cen["cta"]["cauda"] * FPS)

    def q(anc):
        return round(resolver(anc, palavras) * FPS) if anc != "fim" else quadros

    cenas = []
    min_cena = cen.get("min_cena", MIN_CENA)
    proxima = {c["id"]: (cen["cenas"][i + 1].get("transicao") if i + 1 < len(cen["cenas"]) else None) for i, c in enumerate(cen["cenas"])}
    for c in cen["cenas"]:
        ini_q, fim_q = q(c["ini"]), q(c["fim"])
        c2 = {k: v for k, v in c.items() if k not in ("ini", "fim", "nota", "extra")}
        c2.update(ini_q=ini_q, fim_q=fim_q)
        if "marcos" in c:
            c2["marcos"] = {k: round(resolver(v, palavras) - ini_q / FPS, 3) for k, v in c["marcos"].items()}
        saida = proxima[c["id"]]
        extra = SAIDA_Q.get(saida, 0) if c["tipo"] != "fala" else 0  # a cena que sai fica mais alguns quadros (transição)
        c2["extra_q"] = extra
        c2["saida"] = saida
        if "letreiro" in c:
            c2["letreiro"] = [{**l, "em": round(resolver(l["em"], palavras) - ini_q / FPS, 3)} for l in c["letreiro"]]
        if c["tipo"] == "broll":
            c2["arquivo"] = broll(c, ini_q, fim_q + extra)
        cenas.append(c2)
    for a, b in zip(cenas, cenas[1:]):
        if a["fim_q"] != b["ini_q"]:
            raise SystemExit(f"buraco/sobreposição entre {a['id']} e {b['id']}: {a['fim_q']} × {b['ini_q']}")
    curtas = [f"{c['id']} ({(c['fim_q'] - c['ini_q']) / FPS:.2f} s)" for c in cenas if c["fim_q"] - c["ini_q"] < round(min_cena * FPS)]
    if curtas:  # combinado com o Diego: nenhuma cena com menos de 2 s na tela (REV4, 29/10/2026)
        raise SystemExit("cenas curtas demais: " + ", ".join(curtas))
    if cenas[0]["ini_q"] != 0 or cenas[-1]["fim_q"] != quadros:
        raise SystemExit("cenas não cobrem o Reel inteiro")

    for k in cen["imagens"]:
        shutil.copy(os.path.join(AQUI, "imagens", f"{k}.jpg"), os.path.join(PUB, "img", f"{k}.jpg"))

    gancho = []
    for b in cen["gancho"]["blocos"]:
        gancho.append({"linhas": [l["texto"] for l in b["linhas"]], "tamanhos": [l["tam"] for l in b["linhas"]],
                       "cores": [l.get("cor", "branco") for l in b["linhas"]],
                       "tempos": [round(resolver(l["em"], palavras), 3) if l["em"] != 0 else 0 for l in b["linhas"]],
                       "ini": round(resolver(b["ini"], palavras), 3) if b["ini"] != 0 else 0})
    fim_gancho = resolver(cen["gancho"]["fim"], palavras)

    legendas = grupos_legenda(palavras, cen["legenda"]["destaques"], cen["legenda"]["troca"], cen["legenda"].get("quebrar_antes", []))
    # durante o gancho o texto grande é a legenda; durante a palavra-chave em dupla tipografia, também
    sem = [(0, fim_gancho)] + [(resolver(a, palavras), resolver(b, palavras)) for a, b in cen["legenda"].get("sem_legenda", [])]
    legendas = [g for g in legendas if not any(a - 0.01 <= g["ini"] < b - 0.01 for a, b in sem)]

    ref_voz = nivel_evento_voz()
    sons = [{**s, "t": round(resolver(s["em"], palavras) + s.get("desl", 0), 3)} for s in cen["sons"]]
    sons_usados = efeitos(sons, quadros, ref_voz)

    cta = cen["cta"]
    props = {
        "fps": FPS, "largura": 1080, "altura": 1920, "costura": 900, "rostoY": cen["rostoY"], "quadros": quadros,
        "cenas": cenas, "imagens": {k: {"arquivo": f"img/{k}.jpg"} for k in cen["imagens"]},
        "gancho": gancho, "fimGancho": round(fim_gancho, 3), "ganchoLayout": cen["gancho"]["layout"],
        "legendas": legendas, "chaves": [{**k, "ini": round(resolver(k["ini"], palavras), 3), "fim": round(resolver(k["fim"], palavras), 3),
                    "tempos": [round(resolver(l["em"], palavras), 3) for l in k["linhas"]]} for k in cen.get("chaves", [])],
        "mapas": mapas(),
        "cta": {"ini": round(resolver(cta["ini"], palavras), 3), "rotulo": cta["rotulo"], "destino": cta["destino"], "modulo": cta["modulo"], "entrada": cta["entrada_ms"]},
        "mix": {"voz_lufs": -16, "clack_db_rel": cta["clack_db_rel"]},
        "sfx": True,
    }
    json.dump(props, open(os.path.join(PUB, "props.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"palavras": palavras, "trechos": trechos, "sons": sons_usados, "legendas": legendas,
               "cenas": [{"id": c["id"], "tipo": c["tipo"], "layout": c.get("layout"), "ini_s": round(c["ini_q"] / FPS, 3),
                          "fim_s": round(c["fim_q"] / FPS, 3), "dur_s": round((c["fim_q"] - c["ini_q"]) / FPS, 3)} for c in cenas]},
              open(os.path.join(TMP, "montagem.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"voz {voz_q} q ({voz_q / FPS:.2f} s) · Reel {quadros} q ({quadros / FPS:.2f} s) · {len(cenas)} cenas · {len(legendas)} legendas")
    for c in cenas:
        print(f"  {c['id']:<14} {c['tipo']:<6} {str(c.get('layout')):<6} {c['ini_q'] / FPS:6.2f} → {c['fim_q'] / FPS:6.2f}  ({(c['fim_q'] - c['ini_q']) / FPS:.2f} s)")


def nivel_evento_voz():
    """Nível de referência da voz na mesma medida dos efeitos: mediana dos 100 ms com fala."""
    v, _ = sf.read(os.path.join(PUB, "voz.wav"))
    n = int(0.1 * SR)
    xs = np.array([rms_db(v[i:i + n]) for i in range(0, len(v) - n, n)])
    return float(np.median(xs[xs > np.max(xs) - 25]))


if __name__ == "__main__":
    main()
