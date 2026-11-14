"""Reel do Frozen · REV1 · preparação para o Remotion (composição "Frozen", design-system/remotion/src/disney/Frozen.tsx).

Lê edicao.json, transcricao_alinhada.json e cenas.json e gera, em _tmp/public/ (fora do git):
  voz.wav         voz do Diego: as 8 falas (uma tomada cada), cortadas só no silêncio, coladas, sem acelerar
  fala.mp4        vídeo do Diego nos MESMOS trechos (boca em sincronia), HDR → SDR neutro, sem nenhum filtro
  fala_alfa.webm  o mesmo vídeo recortado por IA (VP9 com alfa), para o tela verde
  broll/*.mp4     planos do acervo da Disney (mudos, 1080 × 1920, HDR → SDR, sem mudar a velocidade)
  img/*           prints (comentário com nome borrado, site oficial), imagem do Frozen e quadros desfocados
  sfx.wav         efeitos de transição (kit PDX_*)
  props.json      cenas em quadros, legendas palavra a palavra, gancho e CTA
Roda de dentro de reels/disney-frozen/rev1:  python3 scripts/preparar.py
O Claude não escuta áudio: tudo aqui é medido; a escuta é do Diego.
"""
import hashlib
import json
import os
import re
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
FONTE = os.path.normpath(os.path.join(AQUI, ed["fonte_dir"]))
ACERVO = os.path.normpath(os.path.join(AQUI, cen["acervo_dir"]))
ORIGINAL = os.path.join(FONTE, ed["fonte"])
RECORTE = os.path.join(FONTE, "recorte", "diego_alfa.webm")
# a MESMA conversão do recorte (scripts/recorte.py): o Diego recortado e o inteiro ficam idênticos
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]


def sh(cmd):
    subprocess.run(cmd, check=True)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def carregar(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def medir_lufs(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


# ---------------------------------------------------------------- cortes (decupagem colada, sem cortar palavra)
def cortes():
    """Cada fala é uma tomada. O trecho vai do silêncio antes da 1ª palavra ao silêncio depois da última
    (energia da voz 120–4.000 Hz < −45 dB, no máximo 0,15 s de folga), sempre dentro da tomada.
    Exceções em edicao.json: 'out_fixo' (a cena do preto e branco guarda a cara do Diego até o fim da tomada; o fim do CTA)."""
    x = carregar(ORIGINAL)
    from scipy.signal import butter, sosfilt
    xb = sosfilt(butter(4, [120, 4000], btype="band", fs=SR, output="sos"), x)
    n = int(0.01 * SR)
    env = np.array([rms_db(xb[i:i + n]) for i in range(0, len(xb) - n, n)])  # 10 ms
    tomadas = ed["tomadas"]
    out = []
    for f in ed["falas"]:
        ws = alin[f["id"]]
        t0, t1 = next((a, b) for a, b in tomadas if a - 0.01 <= ws[0]["ini"] < b)
        a = ws[0]["ini"]
        k = int(a / 0.01)
        while k > 0 and a - k * 0.01 < 0.15 and env[k - 1] > -45:
            k -= 1
        ini = max(t0, k * 0.01 - 0.03)
        if "in_fixo" in f:
            ini = f["in_fixo"]
        b = ws[-1]["fim"]
        k = int(b / 0.01)
        while k < len(env) - 1 and k * 0.01 - b < 0.15 and env[k] > -45:
            k += 1
        fim = min(t1, k * 0.01 + 0.04)
        if "out_fixo" in f:
            fim = f["out_fixo"]
        # quadros inteiros do vídeo de origem
        q0 = round(ini * FPS)
        q1 = round(fim * FPS)
        out.append({"fala": f["id"], "q0": q0, "q1": q1, "in": q0 / FPS, "out": q1 / FPS})
    # duas falas seguidas na mesma tomada: o corte das duas cai no ponto mais quieto entre a última palavra de uma
    # e a 1ª da outra (nada de áudio repetido nem perdido)
    for i in range(len(out) - 1):
        a, b = out[i], out[i + 1]
        if a["q1"] > b["q0"]:
            fim_a = alin[a["fala"]][-1]["fim"]
            ini_b = alin[b["fala"]][0]["ini"]
            k0, k1 = int(fim_a / 0.01), max(int(fim_a / 0.01) + 1, int(ini_b / 0.01))
            k = k0 + int(np.argmin(env[k0:k1]))
            qb = round(k * 0.01 * FPS)
            a["q1"] = b["q0"] = qb
            a["out"] = b["in"] = qb / FPS
    return out


def voz_e_fala(trechos):
    """Voz: passa-alta, cada FRASE no mesmo loudness (±6 dB), compressor suave 2:1 e −16 LUFS (o master leva a −14).
    A gravação já é limpa (ruído ≈ 57 dB abaixo da fala, medido): sem redução de ruído.
    Vídeo: os mesmos quadros, do original (fala.mp4) e do recorte com alfa (fala_alfa.webm)."""
    os.makedirs(PUB, exist_ok=True)
    chave = hashlib.md5(json.dumps([trechos, alin], sort_keys=True).encode()).hexdigest()
    cache = os.path.join(TMP, "voz.json")
    pronto = all(os.path.exists(os.path.join(PUB, a)) for a in ("voz.wav", "fala.mp4", "fala_alfa.webm"))
    if pronto and os.path.exists(cache) and json.load(open(cache)).get("chave") == chave:
        print("voz e vídeo do Diego: reaproveitados do cache")
        return json.load(open(cache))["palavras"]
    x = carregar(ORIGINAL)
    fade = int(0.012 * SR)
    pedacos, palavras, t = [], [], 0.0
    for tr in trechos:
        nq = tr["q1"] - tr["q0"]
        m = int(round(nq / FPS * SR))
        seg = x[int(round(tr["in"] * SR)):int(round(tr["in"] * SR)) + m].copy()
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        pedacos.append(seg)
        tr["inicio"] = round(t, 4)
        for w in alin[tr["fala"]]:
            palavras.append({"fala": tr["fala"], "texto": w["texto"], "ini": round(t + w["ini"] - tr["in"], 3),
                             "fim": round(t + w["fim"] - tr["in"], 3), "prob": w["prob"]})
        t += nq / FPS
    voz = np.concatenate(pedacos)
    ent, sai = os.path.join(TMP, "_voz_ent.wav"), os.path.join(TMP, "_voz_sai.wav")
    sf.write(ent, voz.astype(np.float32), SR)
    sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-af", "highpass=f=80", "-c:a", "pcm_f32le", sai])
    voz, _ = sf.read(sai)
    voz, frases = nivelar_frases(voz, palavras)
    sf.write(ent, voz.astype(np.float32), SR)
    sh(["ffmpeg", "-v", "error", "-y", "-i", ent, "-af", "acompressor=threshold=-26dB:ratio=2:attack=8:release=160:makeup=1:knee=4",
        "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", sai])
    v, _ = sf.read(sai)
    v = v[:len(voz)] * 10 ** ((-16 - medir_lufs(sai)) / 20)
    sf.write(os.path.join(PUB, "voz.wav"), v.astype(np.float32), SR)
    json.dump({"frases": frases}, open(os.path.join(AQUI, "voz_medicao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # vídeo do Diego: trim por quadro nas duas fontes, no mesmo filtro (concat), para os quadros baterem 1:1
    sel = "+".join(f"between(n\\,{tr['q0']}\\,{tr['q1'] - 1})" for tr in trechos)
    sh(["ffmpeg", "-v", "error", "-y", "-i", ORIGINAL, "-vf", f"{TONEMAP},select='{sel}',setpts=N/{FPS}/TB,fps={FPS}",
        "-an", *X264, os.path.join(PUB, "fala.mp4")])
    sh(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", RECORTE, "-vf", f"select='{sel}',setpts=N/{FPS}/TB,fps={FPS}",
        "-an", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "16", "-row-mt", "1", "-deadline", "good",
        "-cpu-used", "4", "-auto-alt-ref", "0", os.path.join(PUB, "fala_alfa.webm")])
    json.dump({"chave": chave, "palavras": palavras}, open(cache, "w"), ensure_ascii=False)
    return palavras


def medidor():
    import pyloudnorm as pyln
    return pyln.Meter(SR, block_size=0.2)


def lufs_trecho(m, x, ini, fim):
    a, b = int(ini * SR), int(fim * SR)
    y = x[a:b]
    if len(y) < int(0.4 * SR):
        y = np.pad(y, (0, int(0.4 * SR) - len(y)))
    return float(m.integrated_loudness(y))


def nivelar_frases(voz, palavras, limite_db=6.0):
    """Mesmo método da Parte 2: ganho por frase até a mediana (±6 dB), rampa cosseno centrada na pausa."""
    m = medidor()
    fr, cur = [], [palavras[0]]
    for a, b in zip(palavras, palavras[1:]):
        if b["ini"] - a["fim"] >= 0.22 or a["texto"][-1] in ".,?!" or a["fala"] != b["fala"]:
            fr.append(cur)
            cur = []
        cur.append(b)
    fr.append(cur)
    med = [lufs_trecho(m, voz, f[0]["ini"], f[-1]["fim"]) for f in fr]
    alvo = float(np.median(med))
    ganhos = [float(np.clip(alvo - L, -limite_db, limite_db)) for L in med]
    fronts = [0.0] + [(fr[k][-1]["fim"] + fr[k + 1][0]["ini"]) / 2 for k in range(len(fr) - 1)] + [len(voz) / SR]
    env = np.zeros(len(voz))
    for k, g in enumerate(ganhos):
        env[int(fronts[k] * SR):int(fronts[k + 1] * SR)] = g
    for k in range(1, len(fr)):
        pausa = max(0.0, fr[k][0]["ini"] - fr[k - 1][-1]["fim"])
        r = int(np.clip(pausa * 0.9, 0.02, 0.08) * SR / 2)
        c = int(fronts[k] * SR)
        a, b = max(0, c - r), min(len(voz), c + r)
        env[a:b] = ganhos[k - 1] + (ganhos[k] - ganhos[k - 1]) * (1 - np.cos(np.linspace(0, np.pi, b - a))) / 2
    rel = [{"texto": " ".join(w["texto"] for w in f), "antes_lufs": round(L, 1), "ganho_db": round(g, 1)} for f, L, g in zip(fr, med, ganhos)]
    return voz * 10 ** (env / 20), rel


# ---------------------------------------------------------------- âncoras
INICIOS = {}


def limpa(s):
    return re.sub(r"[^\wÀ-ÿ]", "", s.lower())


def resolver(anc, palavras):
    """'f2:seguidor', 'f5:dois#2', 'f3:fogos-0.25', 'f2:^', número em s. Devolve segundos no tempo do Reel."""
    if isinstance(anc, (int, float)):
        return float(anc)
    m = re.match(r"^(f\d+):([^#+\-]+)(?:#(\d+))?([+\-][\d.]+)?$", anc)
    if not m:
        raise ValueError(anc)
    fala, pal, n, desl = m.group(1), m.group(2), int(m.group(3) or 1), float(m.group(4) or 0)
    if pal == "^":
        return INICIOS[fala] + desl
    achadas = [w for w in palavras if w["fala"] == fala and limpa(w["texto"]) == limpa(pal)]
    if len(achadas) < n:
        raise ValueError(f"âncora não achada: {anc}")
    return achadas[n - 1]["ini"] + desl


# ---------------------------------------------------------------- acervo e imagens
def plano(arquivo, ini_src, nq):
    """Plano do acervo inteiro (vertical do iPhone, rotação pela etiqueta), 1440 × 2560 (a composição aproxima até 1,35×
    sem perder nitidez; a fonte é 4K), HDR → SDR, mudo, sem mudar a velocidade."""
    b = cen["broll"][arquivo]
    dur = nq / FPS
    if ini_src + dur > b["fim_limpo"] + 1e-6:
        raise SystemExit(f"plano curto demais: {arquivo} precisa de {dur:.2f} s desde {ini_src} (limpo até {b['fim_limpo']})")
    nome = f"broll/{os.path.splitext(arquivo)[0]}_{ini_src:.2f}_{nq}_1440.mp4"
    out = os.path.join(PUB, nome)
    if not os.path.exists(out):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini_src:.3f}", "-i", os.path.join(ACERVO, arquivo), "-vf",
            f"scale=1440:2560:flags=lanczos,{TONEMAP},fps={FPS}", "-frames:v", str(nq), "-an", *X264, out])
    return nome


def quadro(arquivo, t):
    nome = f"img/{os.path.splitext(arquivo)[0]}_{t:.2f}.jpg"
    out = os.path.join(PUB, nome)
    if not os.path.exists(out):
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", os.path.join(ACERVO, arquivo), "-frames:v", "1",
            "-vf", f"scale=1080:1920:flags=lanczos,{TONEMAP}", "-q:v", "3", out])
    return nome


def imagem(chave):
    """Print ou foto em imagens/. Se ainda não chegou, gera um cartão provisório claramente marcado."""
    from PIL import Image, ImageDraw, ImageFont
    im = cen["imagens"][chave]
    src = os.path.join(AQUI, "imagens", im["arquivo"])
    out = os.path.join(PUB, "img", im["arquivo"] if os.path.exists(src) else f"provisorio_{chave}.png")
    if os.path.exists(src):
        Image.open(src).convert("RGB").save(out)
        w, h = Image.open(src).size
        return os.path.relpath(out, PUB), w, h, False
    w, h = im["w0"], im["h0"]
    fundo = (236, 233, 226) if chave != "frozen" else (24, 40, 62)
    cor = (90, 86, 80) if chave != "frozen" else (200, 222, 240)
    img = Image.new("RGB", (w, h), fundo)
    d = ImageDraw.Draw(img)
    for i in range(-h, w, 60):  # listras: lê como "falta material", nunca como print de verdade
        d.line([(i, 0), (i + h, h)], fill=tuple(max(0, c - 10) for c in fundo), width=18)
    f = ImageFont.truetype(os.path.join(TMP, "inter800.ttf"), 64 if chave != "frozen" else 96)
    d.multiline_text((w / 2, h / 2 if chave != "frozen" else h * 0.24), im["provisorio"], font=f, fill=cor, anchor="mm", align="center", spacing=18)
    img.save(out)
    return os.path.relpath(out, PUB), w, h, True


def fonte_inter():
    ttf = os.path.join(TMP, "inter800.ttf")
    if not os.path.exists(ttf):
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(REPO, "design-system", "remotion", "node_modules", "@fontsource", "inter", "files", "inter-latin-800-normal.woff2"))
        f.flavor = None
        f.save(ttf)
    return ttf


# ---------------------------------------------------------------- legendas
LARGURA_MAX = 800  # px; centrada em x 540, a linha cabe até x 944 (CLAUDE.md 14.13)
FUNCIONAIS = {"de", "da", "do", "das", "dos", "a", "o", "as", "os", "e", "que", "em", "na", "no", "um", "uma", "ao",
              "pela", "pelo", "com", "para", "pra", "pro", "se", "me", "é", "seu", "sua", "como", "nem", "eu", "te"}
_fonte = None


def largura_legenda(txt):
    global _fonte
    if _fonte is None:
        from PIL import ImageFont
        _fonte = ImageFont.truetype(fonte_inter(), 66)
    return _fonte.getlength(txt)


def grupos_legenda(palavras, troca):
    """1 a 4 palavras, ~18–24 caracteres, sempre 1 linha; custo mínimo por frase (FORMATOS_REELS 6)."""
    frases, atual = [], []
    for w in palavras:
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
                txt = re.sub(r"[,.?!]", "", " ".join(troca.get(limpa(x["texto"]), x["texto"]) for x in g))
                c = (len(txt) - 18) ** 2 / 20
                if largura_legenda(txt) > LARGURA_MAX:
                    c += 400
                if limpa(g[-1]["texto"]) in FUNCIONAIS and j < n:
                    c += 60
                if custo[i] + c < custo[j]:
                    custo[j], de[j] = custo[i] + c, i
        cortes_, j = [], n
        while j > 0:
            cortes_.append((de[j], j))
            j = de[j]
        for i, j in reversed(cortes_):
            grupos.append(fr[i:j])
    out = []
    for k, g in enumerate(grupos):
        ini = g[0]["ini"] - 0.05
        fim = grupos[k + 1][0]["ini"] - 0.05 if k + 1 < len(grupos) else g[-1]["fim"] + 0.4
        fim = min(fim, g[-1]["fim"] + 0.6)
        ps = [{"texto": re.sub(r"[,.]$", "", troca.get(limpa(x["texto"]), x["texto"])), "ini": x["ini"], "fim": x["fim"]} for x in g]
        out.append({"palavras": ps, "ini": round(ini, 3), "fim": round(fim, 3)})
    return out


# ---------------------------------------------------------------- efeitos sonoros
def nivel_evento(x):
    n = int(0.1 * SR)
    if len(x) <= n:
        return rms_db(x)
    return float(max(rms_db(x[i:i + n]) for i in range(0, len(x) - n, n // 4)))


def efeitos(sons, total_q):
    v, _ = sf.read(os.path.join(PUB, "voz.wav"))
    n = int(0.1 * SR)
    xs = np.array([rms_db(v[i:i + n]) for i in range(0, len(v) - n, n)])
    ref = float(np.median(xs[xs > np.max(xs) - 25]))
    mix = np.zeros(int(total_q / FPS * SR) + SR)
    usados = []
    for s in sons:
        x, sr = sf.read(os.path.join(REPO, "design-system", "sons", "externos", s["arquivo"]))
        if x.ndim > 1:
            x = x.mean(axis=1)
        if sr != SR:
            from math import gcd
            from scipy.signal import resample_poly
            k = gcd(SR, sr)
            x = resample_poly(x, SR // k, sr // k)
        g = ref + s["rel_db"] - nivel_evento(x)
        x = x * 10 ** (g / 20)
        pico = int(np.argmax(np.abs(x))) if s.get("alinhar") == "pico" else 0
        i = max(0, int(s["t"] * SR) - pico)
        mix[i:i + len(x)] += x[:len(mix) - i]
        usados.append({**s, "ganho_db": round(g, 1)})
    sf.write(os.path.join(PUB, "sfx.wav"), mix.astype(np.float32), SR)
    return usados


# ---------------------------------------------------------------- montagem
def main():
    for d in ("broll", "img"):
        os.makedirs(os.path.join(PUB, d), exist_ok=True)
    fonte_inter()
    trechos = cortes()
    palavras = voz_e_fala(trechos)
    t = 0.0
    for tr in trechos:
        INICIOS[tr["fala"]] = t
        t += (tr["q1"] - tr["q0"]) / FPS
    quadros = sum(tr["q1"] - tr["q0"] for tr in trechos)

    def q(anc):
        return quadros if anc == "fim" else round(resolver(anc, palavras) * FPS)

    def rel(anc, ini_q):
        return round(resolver(anc, palavras) - ini_q / FPS, 3)

    provisorios = []
    cenas = []
    for c in cen["cenas"]:
        ini_q, fim_q = q(c["ini"]), q(c["fim"])
        nq = fim_q - ini_q
        c2 = {"id": c["id"], "modo": c["modo"], "ini_q": ini_q, "fim_q": fim_q}
        if c.get("pb"):
            c2["pb"] = True
        if c["modo"] == "verde":
            c2["desl"] = c.get("desl", cen["desl_verde"])
        if "fita" in c:
            c2["fita"] = [{**f, "em": rel(f["em"], ini_q)} for f in c["fita"]]
        f = c.get("fundo")
        if f:
            f2 = {"tipo": f["tipo"]}

            def plano_de(p):
                p2 = {k: v for k, v in p.items() if k not in ("arquivo", "ini_src", "img", "foco")}
                p2["arquivo"] = plano(p["arquivo"], p["ini_src"], nq)
                p2["fundo"] = quadro(p["arquivo"], p["ini_src"] + nq / FPS / 2)
                return p2

            if "plano" in f:
                f2["plano"] = plano_de(f["plano"])
            if "img_fundo" in f:
                arq, tt = f["img_fundo"].split("@")
                f2["img"] = quadro(arq, float(tt))
            if "cartao" in f:
                k = dict(f["cartao"])
                src, w0, h0, prov = imagem(k["img"])
                if prov:
                    provisorios.append(k["img"])
                k.update(img=src, w0=w0, h0=h0, entra=rel(k["entra"], ini_q))
                if "sai" in k:
                    k["sai"] = rel(k["sai"], ini_q)
                k["marcas"] = [{**m, "em": rel(m["em"], ini_q)} for m in k.get("marcas", [])]
                if "zoom" in k:
                    k["zoom"] = {**k["zoom"], "em": rel(k["zoom"]["em"], ini_q)}
                f2["cartao"] = k
            if "escurecer" in f:
                f2["escurecer"] = {"ate": rel(f["escurecer"]["ate"], ini_q)}
            if f["tipo"] == "dois":
                for lado in ("esq", "dir"):
                    p = f[lado]
                    if "img" in p:
                        src, _, _, prov = imagem(p["img"])
                        if prov:
                            provisorios.append(p["img"])
                        f2[lado] = {"img": src, "foco": p.get("foco", [0.5, 0.3]), "arquivo": ""}
                    else:
                        f2[lado] = plano_de(p)
                f2["marcos"] = {k: rel(v, ini_q) for k, v in f["marcos"].items()}
            c2["fundo"] = f2
        cenas.append(c2)
    for a, b in zip(cenas, cenas[1:]):
        if a["fim_q"] != b["ini_q"]:
            raise SystemExit(f"buraco/sobreposição entre {a['id']} e {b['id']}")
    curtas = [f"{c['id']} ({(c['fim_q'] - c['ini_q']) / FPS:.2f} s)" for c in cenas
              if c["fim_q"] - c["ini_q"] < round(cen.get("min_excecao", {}).get(c["id"], cen["min_cena"]) * FPS)]
    if curtas:  # regra dos 3 s do Diego
        raise SystemExit("cenas curtas demais: " + ", ".join(curtas))

    gancho = []
    for b in cen["gancho"]["blocos"]:
        gancho.append({"linhas": [l["texto"] for l in b["linhas"]], "tamanhos": [l["tam"] for l in b["linhas"]],
                       "cores": [l.get("cor", "branco") for l in b["linhas"]],
                       "tempos": [round(resolver(l["em"], palavras), 3) if l["em"] != 0 else 0 for l in b["linhas"]],
                       "ini": 0})
    fim_gancho = resolver(cen["gancho"]["fim"], palavras)
    legendas = grupos_legenda(palavras, cen["legenda"]["troca"])
    sem = [(0, fim_gancho)] + [(resolver(a, palavras), quadros / FPS if b == "fim" else resolver(b, palavras))
                               for a, b in cen["legenda"]["sem_legenda"]]
    legendas = [g for g in legendas if not any(a - 0.01 <= g["ini"] < b - 0.01 for a, b in sem)]
    for g in legendas:
        for a, b in sem:
            if g["ini"] < a < g["fim"]:
                g["fim"] = round(a - 0.02, 3)
                g["palavras"] = [w for w in g["palavras"] if w["ini"] < a - 0.02]
    sons = [{**s, "t": round(resolver(s["em"], palavras) + s.get("desl", 0), 3)} for s in cen["sons"]]
    sons_usados = efeitos(sons, quadros)
    cta = cen["cta"]
    props = {
        "fps": FPS, "largura": 1080, "altura": 1920, "quadros": quadros, "cenas": cenas,
        "gancho": gancho, "ganchoTopo": cen["gancho"]["topo"], "fimGancho": round(fim_gancho, 3),
        "legendas": legendas, "legendaY": cen["legendaY"],
        "cta": {"ini": round(resolver(cta["ini"], palavras), 3), "rotulo": cta["rotulo"], "destino": cta["destino"],
                "modulo": cta["modulo"], "entrada": cta["entrada_ms"], "x": cta.get("x"), "y": cta.get("y")},
        "mix": {"voz_lufs": -16, "clack_db_rel": cta["clack_db_rel"]},
        "sfx": True,
    }
    json.dump(props, open(os.path.join(PUB, "props.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"trechos": trechos, "palavras": palavras, "sons": sons_usados, "legendas": legendas, "provisorios": provisorios,
               "cenas": [{"id": c["id"], "modo": c["modo"], "ini_s": round(c["ini_q"] / FPS, 3), "fim_s": round(c["fim_q"] / FPS, 3),
                          "dur_s": round((c["fim_q"] - c["ini_q"]) / FPS, 3)} for c in cenas]},
              open(os.path.join(TMP, "montagem.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Reel {quadros} q ({quadros / FPS:.2f} s) · {len(cenas)} cenas · {len(legendas)} legendas · provisórios: {provisorios or 'nenhum'}")
    for tr in trechos:
        print(f"  {tr['fala']}: {tr['in']:.3f} → {tr['out']:.3f} ({(tr['q1'] - tr['q0']) / FPS:.2f} s)")
    for c in cenas:
        print(f"  {c['id']:<13} {c['modo']:<8} {c['ini_q'] / FPS:6.2f} → {c['fim_q'] / FPS:6.2f}  ({(c['fim_q'] - c['ini_q']) / FPS:.2f} s)")


if __name__ == "__main__":
    main()
