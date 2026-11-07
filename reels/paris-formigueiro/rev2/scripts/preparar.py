"""Reel "Paris não quer você lá" · REV2 · preparação para o Remotion (parte do preparar.py do Reel de Bruges, REV4).

Lê edicao.json, transcricao_alinhada.json e cenas.json e gera, em _tmp/public/ (fora do git):
  voz.wav      voz do Diego: as 10 tomadas do quarto, cortadas só no silêncio, sem acelerar, sem cortar palavra
  fala.mp4     vídeo do Diego cortado nos MESMOS trechos da voz (boca em sincronia), HDR → SDR
  broll/*.mp4  planos do acervo de Paris (mudos, recortados para a camada, HDR → SDR)
  img/*        fotos da web, print da Euromonitor e quadros do acervo
  sfx.wav      efeitos de transição (kit PDX_*, volumes da REFERENCIA_EDICAO_FORMATOS 4.1)
  props.json   cenas em quadros, legendas, gancho, mapa dos distritos e CTA
Roda de dentro de reels/paris-formigueiro/rev2:  python scripts/preparar.py
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
MIN_CENA = 2.0  # s: padrão; o cenas.json sobe para 3 s (pedido do Diego, 07/11/2026)
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
        x = tm["bruto"]
        livre = []
        for dur_s, folga in ((0.4, 0.15), (0.25, 0.06), (0.15, 0.04)):  # tomadas com pouco silêncio usam janela menor
            n = int(dur_s * SR)
            livre = [i for i in range(int(0.03 * SR), len(x) - n, int(0.02 * SR))
                     if not any(i / SR - folga < b and (i + n) / SR + folga > a for a, b in tm["palavras_bruto"])]
            if livre:
                break
        if not livre:  # tomada sem pausa: os 100 ms mais quietos
            n = int(0.1 * SR)
            livre = list(range(0, len(x) - n, int(0.01 * SR)))
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
    # REV2 (pedido do Diego, 07/11/2026: "todas as vozes no mesmo volume"): além de igualar cada tomada,
    # iguala cada FRASE ao mesmo loudness; as rampas de ganho caem nas pausas entre frases.
    voz, frases_rel = nivelar_frases(voz, palavras)
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
    # medição por frase na voz final (depois do compressor e do ganho)
    m = medidor()
    for f in frases_rel:
        f["depois_lufs"] = round(lufs_trecho(m, v, f["ini"], f["fim"]), 1)
    ds = np.array([f["depois_lufs"] for f in frases_rel])
    an = np.array([f["antes_lufs"] for f in frases_rel])
    resumo = {"frases": len(frases_rel), "antes": {"min": float(an.min()), "max": float(an.max()), "desvio": round(float(an.std()), 2)},
              "depois": {"min": float(ds.min()), "max": float(ds.max()), "desvio": round(float(ds.std()), 2)}}
    print("frases: antes", resumo["antes"], "· depois", resumo["depois"])
    json.dump({"tomadas": relatorio, "frases": frases_rel, "resumo_frases": resumo},
              open(os.path.join(AQUI, "voz_medicao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
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


def medidor():
    import pyloudnorm as pyln
    return pyln.Meter(SR, block_size=0.2)


def lufs_trecho(m, x, ini, fim):
    """Loudness (LUFS, BS.1770) de um trecho; trechos < 0,4 s são completados com silêncio (só a fala conta no gate)."""
    a, b = int(ini * SR), int(fim * SR)
    y = x[a:b]
    if len(y) < int(0.4 * SR):
        y = np.pad(y, (0, int(0.4 * SR) - len(y)))
    return float(m.integrated_loudness(y))


def frases_de(palavras):
    """Frase = palavras seguidas sem pausa >= 0,22 s, sem pontuação no meio e na mesma tomada."""
    fr, cur = [], [palavras[0]]
    for a, b in zip(palavras, palavras[1:]):
        if b["ini"] - a["fim"] >= 0.22 or a["texto"][-1] in ".,?!" or a["fala"] != b["fala"]:
            fr.append(cur)
            cur = []
        cur.append(b)
    fr.append(cur)
    return fr


def nivelar_frases(voz, palavras, limite_db=6.0):
    """Ganho por frase até o loudness mediano das frases (limitado a ±6 dB). Cada ganho vale da metade da pausa
    anterior até a metade da pausa seguinte, com rampa cosseno de até 80 ms centrada na pausa (nunca no meio da palavra)."""
    m = medidor()
    fr = frases_de(palavras)
    med = []
    for f in fr:
        med.append(lufs_trecho(m, voz, f[0]["ini"], f[-1]["fim"]))
    alvo = float(np.median(med))
    ganhos = [float(np.clip(alvo - L, -limite_db, limite_db)) for L in med]
    # fronteiras: meio da pausa entre a última palavra de uma frase e a 1ª da seguinte
    fronts = [0.0] + [(fr[k][-1]["fim"] + fr[k + 1][0]["ini"]) / 2 for k in range(len(fr) - 1)] + [len(voz) / SR]
    env = np.zeros(len(voz))
    for k, g in enumerate(ganhos):
        a, b = int(fronts[k] * SR), int(fronts[k + 1] * SR)
        env[a:b] = g
    # suaviza cada degrau com rampa proporcional à pausa disponível (20 a 80 ms)
    for k in range(1, len(fr)):
        pausa = fr[k][0]["ini"] - fr[k - 1][-1]["fim"]
        r = int(np.clip(pausa * 0.9, 0.02, 0.08) * SR / 2)
        c = int(fronts[k] * SR)
        a, b = max(0, c - r), min(len(voz), c + r)
        g0, g1 = ganhos[k - 1], ganhos[k]
        env[a:b] = g0 + (g1 - g0) * (1 - np.cos(np.linspace(0, np.pi, b - a))) / 2
    saida = voz * 10 ** (env / 20)
    rel = [{"fala": f[0]["fala"], "ini": round(f[0]["ini"], 3), "fim": round(f[-1]["fim"], 3),
            "texto": " ".join(w["texto"] for w in f), "antes_lufs": round(L, 1), "ganho_db": round(g, 1)}
           for f, L, g in zip(fr, med, ganhos)]
    return saida, rel


def medir_lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


# ---------------------------------------------------------------- âncoras
def resolver(anc, palavras):
    """'f2:Bruges', 'f2:que#3', 'f3:mas-0.05', 'fim', número em s. Devolve segundos no tempo do Reel."""
    if isinstance(anc, (int, float)):
        return float(anc)
    m = re.match(r"^(f\d+):([^#+\-]+)(?:#(\d+))?([+\-][\d.]+)?$", anc)
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
def broll(c, ini_q, fim_q, tam=None):
    """Recorta o trecho do plano do acervo na proporção da camada (tela dividida 1080×900 ou cheia 1080×1920)."""
    b = dict(cen["broll"][c["arquivo"]])
    if "ini_src" in c:
        b["ini"] = c["ini_src"]
    w, h = tam or ((1080, 900) if c["layout"] == "split" else (1080, 1920))
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


def trocar(troca, w):
    """Escrita da legenda: 'f6:um' vale só naquela fala; 'quatro' vale em todas."""
    return troca.get(f"{w['fala']}:{limpa(w['texto'])}", troca.get(limpa(w["texto"]), w["texto"]))


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
                txt = re.sub(r"[,.]", "", " ".join(trocar(troca, x) for x in g))
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
            t = trocar(troca, x)
            t = re.sub(r"[,.]$", "", t)
            ps.append({"texto": t, "ini": x["ini"], "fim": x["fim"], "destaque": limpa(x["texto"]) in destaques.get(x["fala"], [])})
        out.append({"palavras": ps, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


# ---------------------------------------------------------------- mapa dos 20 distritos (Code for America, licença MIT)
def mapa9():
    """Contorno dos 20 arrondissements projetado na metade de cima (x 40–780, y 300–880; o rótulo 9º DISTRITO fica à direita)."""
    geo = json.load(open(os.path.join(AQUI, "dados", "paris_arrondissements.geojson"), encoding="utf-8"))
    aneis = []
    for f in geo["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        aneis.append((int(f["properties"]["cartodb_id"]), [p[0] for p in polys]))
    lons = [lo for _, ps in aneis for r in ps for lo, la in r]
    lats = [la for _, ps in aneis for r in ps for lo, la in r]
    lon0, lon1, lat0, lat1 = min(lons), max(lons), min(lats), max(lats)
    k = np.cos(np.radians((lat0 + lat1) / 2))
    x0, x1, y0, y1 = 40, 780, 300, 880
    esc = min((x1 - x0) / ((lon1 - lon0) * k), (y1 - y0) / (lat1 - lat0))
    ox = x0 + ((x1 - x0) - (lon1 - lon0) * k * esc) / 2
    oy = y0 + ((y1 - y0) - (lat1 - lat0) * esc) / 2
    pj = lambda lo, la: (round(ox + (lo - lon0) * k * esc, 1), round(oy + (lat1 - la) * esc, 1))
    out = []
    for n, ps in sorted(aneis):
        d, xs, ys = "", [], []
        for r in ps:
            xy = [pj(lo, la) for lo, la in r]
            d += "M" + "L".join(f"{x},{y}" for x, y in xy) + "Z"
            xs += [x for x, _ in xy]
            ys += [y for _, y in xy]
        out.append({"n": n, "d": d, "cx": round(float(np.mean(xs)), 1), "cy": round(float(np.mean(ys)), 1)})
    return {"w": 1080, "h": 900, "distritos": out}


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
        if "cartao" in c:  # REV2: vídeo num cartão por cima do apoio, a partir do marco "cartao"
            k = c["cartao"]
            rel = c2["marcos"]["cartao"]
            nq = fim_q + extra - ini_q - round(rel * FPS)
            fake = {"id": c["id"] + "_cartao", "arquivo": k["arquivo"], "layout": "cartao", "ini_src": k["ini_src"]}
            c2["cartao"] = {"arquivo": broll(fake, 0, nq, (k["w"], k["h"])), "w": k["w"], "h": k["h"]}
        cenas.append(c2)
    for a, b in zip(cenas, cenas[1:]):
        if a["fim_q"] != b["ini_q"]:
            raise SystemExit(f"buraco/sobreposição entre {a['id']} e {b['id']}: {a['fim_q']} × {b['ini_q']}")
    exc = cen.get("min_excecao", {})  # cenas com mínimo próprio (só o gancho; registrado na QA)
    curtas = [f"{c['id']} ({(c['fim_q'] - c['ini_q']) / FPS:.2f} s)" for c in cenas
              if c["fim_q"] - c["ini_q"] < round(exc.get(c["id"], min_cena) * FPS) - 1e-9]
    if curtas:  # combinado com o Diego: nenhuma cena com menos de 2 s na tela (REV4, 29/10/2026)
        raise SystemExit("cenas curtas demais: " + ", ".join(curtas))
    if cenas[0]["ini_q"] != 0 or cenas[-1]["fim_q"] != quadros:
        raise SystemExit("cenas não cobrem o Reel inteiro")

    for k, arq in cen["imagens"].items():
        shutil.copy(os.path.join(AQUI, "imagens", arq), os.path.join(PUB, "img", arq))

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
        "cenas": cenas, "imagens": {k: {"arquivo": f"img/{arq}"} for k, arq in cen["imagens"].items()},
        "gancho": gancho, "fimGancho": round(fim_gancho, 3), "ganchoLayout": cen["gancho"]["layout"],
        "legendas": legendas, "chaves": [{**k, "ini": round(resolver(k["ini"], palavras), 3), "fim": round(resolver(k["fim"], palavras), 3),
                    "tempos": [round(resolver(l["em"], palavras), 3) for l in k["linhas"]]} for k in cen.get("chaves", [])],
        "mapa9": mapa9(),
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
