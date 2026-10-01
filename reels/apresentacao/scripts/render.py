#!/usr/bin/env python3
"""Render do Reel de apresentação "Primeiro Dia" a partir da lista de cortes (JSON).

Uso: python3 render.py lista_de_cortes.json [etapa ...]
Etapas: video, texto, audio, final, capa, verificar (sem etapa = todas, nessa ordem).

- video: recorta cada cena do master ou do bruto indicado em "arquivo" (HDR HLG -> SDR Rec.709 com
  tone mapping Reinhard; brutos SDR ficam como estão; 24 fps; crop 9:16 enquadrando quem está em cena;
  "girar" corrige vídeo gravado com o celular deitado) em intermediários sem perdas.
- texto: camada de texto (PNG por frame) com a identidade visual do canal.
- audio: som ambiente de cada corte com crossfade de 0,2 s centrado no corte, narração
  tratada (passa-altas 80 Hz, redução de ruído leve, compressão suave), mix e -14 LUFS.
- final: reel_apresentacao.mp4 e reel_apresentacao_sem_texto.mp4 (H.264 CRF 18 slow, AAC 192k).
- capa: capa 1080x1920 (Pillow).
- verificar: ffprobe, loudness e contact sheet do resultado.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 24  # nativo do master: sem repetir frames
W, H = 1080, 1920
SR = 48000
AREIA = (0xF4, 0xEF, 0xE6)
AZUL = (0x1F, 0x3A, 0x4D)
TERRACOTA = (0xD9, 0x69, 0x3A)
DOURADO = (0xE8, 0xB2, 0x4A)
ALFA_CAIXA = round(255 * 0.85)

# Zona segura do Instagram: nada de texto nessas faixas.
SEG_TOPO, SEG_BASE, SEG_DIR = 220, 250, 120
MARGEM_ESQ = 60


def x_seguro(larg):
    """x para centralizar um texto na faixa livre (60 px da esquerda até 120 px antes da borda direita)."""
    livre = W - SEG_DIR - MARGEM_ESQ
    if larg > livre:
        print(f"  AVISO: texto com {larg} px não cabe nos {livre} px da zona segura", flush=True)
    return MARGEM_ESQ + (livre - larg) // 2
LARG_MAX_TEXTO = W - SEG_DIR - 120  # texto centralizado em x=540 ocupa no máximo [120, 960]

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(RAIZ, "fontes")
F_TITULO = os.path.join(FONTES, "DMSerifDisplay-Regular.ttf")
F_TEXTO = os.path.join(FONTES, "Montserrat-SemiBold.ttf")

# HLG -> SDR Rec.709. npl=203 põe o branco de referência do HLG (203 nits) em 1,0; o pico do HLG
# (1000 nits) fica em 1000/203 = 4,93 e precisa ser informado ao tonemap, que não o deduz depois da
# linearização. Reinhard comprime só os realces; desat=0 evita que o molho e a pele virem rosa, e a
# saturação uniforme de 0,88 no fim tira o excesso sem mudar o matiz.
TONEMAP = (
    "zscale=w=1080:h=1920:f=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,"
    "format=gbrpf32le,zscale=p=bt709,tonemap=reinhard:param=0.5:peak=4.93:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv:d=error_diffusion,format=yuv444p,eq=saturation=0.88,format=yuv420p"
)
# Brutos já em SDR (Rec.709): só redimensiona, sem conversão de cor.
SDR = "scale=1080:1920:flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709,format=yuv420p"
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


# ---------------------------------------------------------------- utilidades

def rodar(cmd, capturar=False):
    texto = " ".join(str(c) for c in cmd)
    print("$", texto if len(texto) < 400 else texto[:400] + " ...", flush=True)
    r = subprocess.run([str(c) for c in cmd], check=True, text=True,
                       stdout=subprocess.PIPE if capturar else None,
                       stderr=subprocess.PIPE if capturar else None)
    return (r.stdout or "") + (r.stderr or "") if capturar else ""


def segundos(v):
    """Aceita 123.4, "02:03.4" ou "00:02:03.4"."""
    if isinstance(v, (int, float)):
        return float(v)
    s = 0.0
    for parte in str(v).replace(",", ".").split(":"):
        s = s * 60 + float(parte)
    return s


def carregar(arq):
    with open(arq, encoding="utf-8") as f:
        edl = json.load(f)
    base = os.path.dirname(os.path.abspath(arq))
    edl["_base"] = base
    # caminhos relativos ao JSON; REEL_MASTER / REEL_TMP sobrepõem (master de 10 GB e temporários ficam fora do git)
    edl["master"] = os.environ.get("REEL_MASTER") or caminho(edl, edl["master"])
    t = 0
    cortes = []
    for c in edl["cortes"]:
        c = dict(c)
        c["_arq"] = caminho(edl, c["arquivo"]) if c.get("arquivo") else edl["master"]
        c["entrada"], c["saida"] = segundos(c["entrada"]), segundos(c["saida"])
        if "audio_de" in c and c["audio_de"] is not None:
            c["audio_de"] = segundos(c["audio_de"])
        c["frames"] = round((c["saida"] - c["entrada"]) * FPS)
        c["f0"], c["ini"], c["fim"] = t, t / FPS, (t + c["frames"]) / FPS
        t += c["frames"]
        cortes.append(c)
    edl["_cortes"], edl["_frames"] = cortes, t
    blocos = {}
    for c in cortes:
        b = blocos.setdefault(c["bloco"], [c["ini"], c["fim"]])
        b[0], b[1] = min(b[0], c["ini"]), max(b[1], c["fim"])
    edl["_blocos"] = blocos
    edl["_tmp"] =os.environ.get("REEL_TMP") or caminho(edl, edl.get("pasta_tmp", "_tmp"))
    os.makedirs(edl["_tmp"], exist_ok=True)
    return edl


def caminho(edl, p):
    return p if os.path.isabs(p) else os.path.join(edl["_base"], p)


# ---------------------------------------------------------------- vídeo

def filtro_crop(c, fw=3840, fh=2160):
    """Crop 9:16 centrado no assunto (centro_x/centro_y de 0 a 1) numa fonte fw x fh
    (4K deitado, 4K em pé ou 720p). Nunca estica."""
    zoom = float(c.get("zoom", 1.0))
    k = int(min(fw / 9, fh / 16) / zoom) // 2 * 2  # w = 9k, h = 16k: exatamente 9:16 e dimensões pares (4:2:0)
    cw, ch = 9 * k, 16 * k
    def pos(centro, total, lado):
        return int(round(min(max(centro * total - lado / 2, 0), total - lado) / 2)) * 2
    y = pos(float(c.get("centro_y", 0.5)), fh, ch)
    x0 = pos(float(c.get("centro_x", 0.5)), fw, cw)
    dur_in = max(1, round((c["saida"] - c["entrada"]) * 24))  # n = frame de entrada (~24 fps)
    if "centro_x_pontos" in c:  # panorâmica por pontos-chave [[fração do corte, centro_x], ...]
        pts = [(float(f) * dur_in, pos(float(cx), fw, cw)) for f, cx in c["centro_x_pontos"]]
        x = str(pts[-1][1])
        for (na, xa), (nb, xb) in reversed(list(zip(pts, pts[1:]))):
            x = f"if(lt(n,{nb:.1f}),{xa}+({xb - xa})*(n-{na:.1f})/{max(nb - na, 1):.1f},{x})"
        x = f"'{x}'"
    elif "centro_x_fim" in c:  # panorâmica lenta, linear ao longo do corte
        x1 = pos(float(c["centro_x_fim"]), fw, cw)
        x = f"'{x0}+({x1 - x0})*min(n/{dur_in},1)'"
    else:
        x = str(x0)
    return f"crop=w={cw}:h={ch}:x={x}:y={y}"


_INFO = {}


def info_fonte(arq):
    """Dimensões do vídeo na orientação de exibição (o ffmpeg aplica sozinho a rotação gravada pelo
    celular) e se ele é HDR (HLG)."""
    if arq not in _INFO:
        s = json.loads(subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", arq],
            capture_output=True, text=True, check=True).stdout)["streams"][0]
        w, h = s["width"], s["height"]
        rot = next((int(float(d["rotation"])) for d in s.get("side_data_list", []) if "rotation" in d), 0)
        if rot % 180:
            w, h = h, w
        _INFO[arq] = {"w": w, "h": h, "hdr": s.get("color_transfer") == "arib-std-b67"}
    return _INFO[arq]


def filtro_video(c, formato="yuv420p"):
    """Orientação, crop 9:16 e cor de um corte. "girar": 90 corrige vídeo gravado com o celular deitado
    e salvo como retrato. HDR (HLG) passa pelo tone mapping; SDR só é redimensionado."""
    inf = info_fonte(c["_arq"])
    fw, fh, pre = inf["w"], inf["h"], ""
    girar = int(c.get("girar", 0)) % 360
    if girar in (90, 270):
        pre = "transpose=clock," if girar == 90 else "transpose=cclock,"
        fw, fh = fh, fw
    cor = TONEMAP if inf["hdr"] else SDR
    return f"{pre}{filtro_crop(c, fw, fh)},{cor.replace('format=yuv420p', 'format=' + formato)}"


def corte_parado(c, frac):
    """Cópia do corte com o crop fixo na posição que a panorâmica tem em `frac` (0 a 1) do corte,
    para extrair um quadro isolado (storyboard, mockups, capa)."""
    c2 = {k: v for k, v in c.items() if k not in ("centro_x_fim", "centro_x_pontos")}
    if "centro_x_pontos" in c:
        pts = [(float(f), float(x)) for f, x in c["centro_x_pontos"]]
        c2["centro_x"] = pts[-1][1]
        for (fa, xa), (fb, xb) in zip(pts, pts[1:]):
            if frac < fb:
                c2["centro_x"] = xa + (xb - xa) * (frac - fa) / max(fb - fa, 1e-6)
                break
    elif "centro_x_fim" in c:
        c2["centro_x"] = c["centro_x"] + (c["centro_x_fim"] - c["centro_x"]) * frac
    return c2


def etapa_video(edl):
    for i, c in enumerate(edl["_cortes"]):
        saida = os.path.join(edl["_tmp"], f"v_{i:02d}.mkv")
        vf = f"{filtro_video(c)},fps={FPS},setsar=1"  # brutos a 23,976 fps: o fps=24 não repete quadro em cortes curtos
        chave = json.dumps([c["_arq"], c["entrada"], c["frames"], vf])
        if os.path.exists(saida) and open(saida + ".chave").read() == chave:
            continue
        rodar(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['entrada']:.3f}", "-i", c["_arq"],
               "-map", "0:v:0", "-an", "-sn", "-dn", "-vf", vf,
               "-frames:v", c["frames"], "-c:v", "libx264", "-qp", "0", "-preset", "veryfast", *TAGS_COR, saida])
        open(saida + ".chave", "w").write(chave)
    with open(os.path.join(edl["_tmp"], "video.txt"), "w") as f:
        for i in range(len(edl["_cortes"])):
            f.write(f"file 'v_{i:02d}.mkv'\n")


# ---------------------------------------------------------------- texto

def fonte(arq, tam):
    return ImageFont.truetype(arq, tam)


def largura(txt, f, trak=0):
    return f.getlength(txt) + trak * max(0, len(txt) - 1)


def escrever(d, xy, txt, f, cor, trak=0):
    """Texto com espaçamento entre letras (tracking) e origem na linha de base à esquerda."""
    x, y = xy
    if not trak:
        d.text((x, y), txt, font=f, fill=cor, anchor="ls")
        return
    for ch in txt:
        d.text((x, y), ch, font=f, fill=cor, anchor="ls")
        x += f.getlength(ch) + trak


def caixa_arredondada(tam, raio, cor, alfa, escala=4):
    w, h = tam
    img = Image.new("RGBA", (w * escala, h * escala), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, w * escala - 1, h * escala - 1], raio * escala, fill=cor + (alfa,))
    return img.resize((w, h), Image.LANCZOS)


def sombra(camada, raio=10, alfa=0.55, desloc=(0, 4)):
    """Sombra suave a partir do alfa de uma camada RGBA."""
    a = camada.getchannel("A").point(lambda v: int(v * alfa))
    s = Image.new("RGBA", camada.size, (10, 16, 22, 0))
    s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(raio))
    base = Image.new("RGBA", camada.size, (0, 0, 0, 0))
    base.alpha_composite(s, (desloc[0], desloc[1]))
    base.alpha_composite(camada)
    return base


def palavras_com_destaque(texto):
    """'Eu sou o *Diego*,' -> [('Eu', False), ('sou', False), ('o', False), ('Diego,', True)]"""
    out = []
    for p in texto.split():
        destaque = "*" in p
        out.append((p.replace("*", ""), destaque))
    return out


def render_legenda(texto, tam=58):
    """Legenda: Montserrat SemiBold areia em caixa azul 85% com cantos arredondados; *palavra* em terracota."""
    f = fonte(F_TEXTO, tam)
    pal = palavras_com_destaque(texto)
    esp = f.getlength(" ")
    pad_x, pad_y = 30, 20
    # uma linha se couber; senão, duas linhas equilibradas (a mais larga o mais curta possível)
    lim = LARG_MAX_TEXTO - 2 * pad_x
    def larg_linha(ws):
        return sum(f.getlength(w) for w, _ in ws) + esp * (len(ws) - 1)
    linhas = [pal]
    if larg_linha(pal) > lim and len(pal) > 1:
        k = min(range(1, len(pal)), key=lambda i: max(larg_linha(pal[:i]), larg_linha(pal[i:])))
        linhas = [pal[:k], pal[k:]]
    asc, desc = f.getmetrics()
    alt_linha = round(tam * 1.18)
    larg = max(sum(f.getlength(w) for w, _ in l) + esp * (len(l) - 1) for l in linhas)
    cw, ch = round(larg + 2 * pad_x), round(alt_linha * len(linhas) + 2 * pad_y - (alt_linha - tam) * 0.6)
    img = caixa_arredondada((cw, ch), 22, AZUL, ALFA_CAIXA)
    d = ImageDraw.Draw(img)
    for k, l in enumerate(linhas):
        lw = sum(f.getlength(w) for w, _ in l) + esp * (len(l) - 1)
        x = (cw - lw) / 2
        y = pad_y + k * alt_linha + tam * 0.86
        for w, dest in l:
            # no destaque, só a palavra fica terracota; a pontuação final continua areia
            nucleo = w.rstrip(",.;:!?…") if dest else w
            d.text((x, y), nucleo, font=f, fill=TERRACOTA if dest else AREIA, anchor="ls")
            if nucleo != w:
                d.text((x + f.getlength(nucleo), y), w[len(nucleo):], font=f, fill=AREIA, anchor="ls")
            x += f.getlength(w) + esp
    return img


def render_selo():
    """Pílula terracota com "DIA 1" em areia."""
    f = fonte(F_TEXTO, 30)
    txt, trak = "DIA 1", 3
    w, h = round(largura(txt, f, trak) + 2 * 26), 58
    img = caixa_arredondada((w, h), h // 2, TERRACOTA, 255)
    escrever(ImageDraw.Draw(img), (26, h / 2 + 11), txt, f, AREIA, trak)
    return img


def render_cidade(nome, cfg=None):
    """Nome da cidade (montagem): Montserrat SemiBold areia, na mesma linha de base do selo DIA 1,
    com sombra suave para ler sobre céu claro."""
    cfg = cfg or {}
    f = fonte(F_TEXTO, cfg.get("tam", 30))
    txt = nome.upper() if cfg.get("maiusculas", True) else nome
    trak = cfg.get("trak", 3)
    w, h = round(largura(txt, f, trak)) + 24, 58
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    escrever(ImageDraw.Draw(img), (12, h / 2 + 11), txt, f, AREIA, trak)
    return sombra(img, raio=6, alfa=0.85, desloc=(0, 2))


def icone_microfone(tam, cor):
    e = 4
    img = Image.new("RGBA", (tam * e, tam * e), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = tam * e
    d.rounded_rectangle([s * 0.36, s * 0.08, s * 0.64, s * 0.58], s * 0.14, fill=cor)
    d.arc([s * 0.24, s * 0.26, s * 0.76, s * 0.72], 0, 180, fill=cor, width=round(s * 0.07))
    d.line([s * 0.5, s * 0.72, s * 0.5, s * 0.88], fill=cor, width=round(s * 0.07))
    d.line([s * 0.36, s * 0.9, s * 0.64, s * 0.9], fill=cor, width=round(s * 0.07))
    return img.resize((tam, tam), Image.LANCZOS)


def render_aviso_narracao(texto="NARRAÇÃO · A GRAVAR"):
    """Etiqueta pequena indicando que o bloco receberá a narração gravada."""
    f = fonte(F_TEXTO, 24)
    trak = 2
    ico = 26
    w, h = round(18 + ico + 10 + largura(texto, f, trak) + 18), 50
    img = caixa_arredondada((w, h), 14, AZUL, ALFA_CAIXA)
    img.alpha_composite(icone_microfone(ico, TERRACOTA + (255,)), (18, (h - ico) // 2))
    escrever(ImageDraw.Draw(img), (18 + ico + 10, h / 2 + 9), texto, f, AREIA, trak)
    return img


def render_titulo_gancho(cfg):
    """Gancho: "Aqui é o" (Montserrat) + "Primeiro Dia" (DM Serif Display) + fio dourado, com sombra suave."""
    f1 = fonte(F_TEXTO, cfg.get("tam_linha1", 52))
    f2 = fonte(F_TITULO, cfg.get("tam_linha2", 148))
    l1, l2 = cfg.get("linha1", "Aqui é o"), cfg.get("linha2", "Primeiro Dia")
    trak1 = 3
    w1, w2 = largura(l1, f1, trak1), f2.getlength(l2)
    larg = round(max(w1, w2)) + 80
    alt = 330
    img = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    escrever(d, ((larg - w1) / 2, 88), l1, f1, AREIA, trak1)
    d.text((larg / 2, 232), l2, font=f2, fill=AREIA, anchor="ms")
    # fio dourado (detalhe com moderação)
    d.rounded_rectangle([larg / 2 - 70, 268, larg / 2 + 70, 274], 3, fill=DOURADO + (255,))
    texto = sombra(img, raio=12, alfa=0.6)
    # véu escuro bem difuso atrás do título: legível sobre fundo com muito detalhe
    veu = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))
    ImageDraw.Draw(veu).rounded_rectangle([50, 50, larg - 50, alt - 30], 60,
                                          fill=(10, 16, 22, int(cfg.get("veu", 0.42) * 255)))
    veu = veu.filter(ImageFilter.GaussianBlur(34))
    veu.alpha_composite(texto)
    return veu


def render_cartao_final(cfg):
    """Aviso final: "Primeiro vídeo" / "dia 10/10" + pílula "link na bio"."""
    f1 = fonte(F_TITULO, cfg.get("tam_linha1", 104))
    f2 = fonte(F_TITULO, cfg.get("tam_linha2", 132))
    fp = fonte(F_TEXTO, 40)
    l1, l2 = cfg.get("linha1", "Primeiro vídeo"), cfg.get("linha2", "dia 10/10")
    l3 = cfg.get("linha3", "link na bio")
    larg = round(max(f1.getlength(l1), f2.getlength(l2))) + 80
    alt = 470
    img = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((larg / 2, 112), l1, font=f1, fill=AREIA, anchor="ms")
    d.text((larg / 2, 262), l2, font=f2, fill=AREIA, anchor="ms")
    img = sombra(img, raio=12, alfa=0.6)
    # separador "·" dourado + pílula terracota
    pw, ph = round(largura(l3, fp, 1) + 2 * 34), 76
    pilula = caixa_arredondada((pw, ph), ph // 2, TERRACOTA, 255)
    escrever(ImageDraw.Draw(pilula), (34, ph / 2 + 14), l3, fp, AREIA, 1)
    d = ImageDraw.Draw(img)
    d.ellipse([larg / 2 - 7, 300, larg / 2 + 7, 314], fill=DOURADO + (255,))
    img.alpha_composite(sombra(pilula, raio=8, alfa=0.35), ((larg - pw) // 2, 346))
    return img


def ler_srt(arq):
    blocos = re.split(r"\n\s*\n", open(arq, encoding="utf-8").read().strip())
    out = []
    for b in blocos:
        linhas = b.strip().splitlines()
        if len(linhas) < 3:
            continue
        a, z = [segundos(t.strip()) for t in linhas[1].split("-->")]
        out.append((a, z, " ".join(linhas[2:])))
    return out


def aplicar_destaques(texto, destaques):
    """Marca com *palavra* cada palavra das expressões de destaque (sem diferenciar maiúsculas)."""
    palavras = texto.split()
    limpas = [re.sub(r"[^\wÀ-ÿ]", "", p).lower() for p in palavras]
    for expr in destaques:
        alvo = expr.lower().split()
        for i in range(len(palavras) - len(alvo) + 1):
            if limpas[i:i + len(alvo)] == alvo:
                for k in range(i, i + len(alvo)):
                    if "*" not in palavras[k]:
                        palavras[k] = "*" + palavras[k] + "*"
    return " ".join(palavras)


def legendas_das_falas(edl):
    """Converte as legendas de cada corte (tempo do original) para o tempo do Reel.

    Cada tela entra no início da primeira palavra e fica até a próxima tela (ou +0,35 s
    depois da última palavra), sempre dentro do corte e com no mínimo 0,6 s.
    """
    out = []
    for c in edl["_cortes"]:
        legs = c.get("legendas", [])
        for k, lg in enumerate(legs):
            a = c["ini"] + (float(lg["de"]) - c["entrada"])
            z = c["ini"] + (float(lg["ate"]) - c["entrada"]) + 0.35
            if k + 1 < len(legs):  # respiro de ~2 frames antes da tela seguinte
                z = min(z, c["ini"] + (float(legs[k + 1]["de"]) - c["entrada"]) - 0.12)
            a, z = max(a - 0.05, c["ini"]), min(z, c["fim"])
            if z - a < 0.6:
                z = min(a + 0.6, c["fim"])
            out.append((round(a * FPS) / FPS, round(z * FPS) / FPS, lg["texto"]))
    return out


def eventos_de_texto(edl):
    """Lista de (inicio, fim, id, imagem, (x, y), animacao)."""
    ev = []
    blocos = edl["_blocos"]
    total = edl["_frames"] / FPS
    tx = edl.get("textos", {})
    # gancho
    if "gancho" in blocos:
        a, z = blocos["gancho"]
        img = render_titulo_gancho(tx.get("gancho", {}))
        y = tx.get("gancho", {}).get("y", 640)
        ev.append((a, z, "gancho", img, (x_seguro(img.width), y), "sobe"))
    # selo DIA 1 no gancho e na montagem
    selo = render_selo()
    for b in ("gancho", "montagem"):
        if b in blocos:
            ev.append((blocos[b][0], blocos[b][1], "selo_" + b, selo, (MARGEM_ESQ, SEG_TOPO + 24), None))
    # nome da cidade em cada cena da montagem, ao lado do selo: "DIA 1  PARIS"
    for c in edl["_cortes"]:
        if c["bloco"] == "montagem" and c.get("cidade"):
            img = render_cidade(c["cidade"], tx.get("cidade"))
            ev.append((c["ini"], c["fim"], f"cidade_{c['f0']}", img, (MARGEM_ESQ + selo.width + 6, SEG_TOPO + 24), None))
    # narração: legendas + aviso de prévia enquanto não houver arquivo gravado
    nar = edl.get("narracao", {})
    if "apresentacao" in blocos:
        a, z = blocos["apresentacao"]
        if not nar.get("arquivo"):
            aviso = render_aviso_narracao(nar.get("aviso", "NARRAÇÃO · A GRAVAR"))
            ev.append((a, z, "aviso_narracao", aviso, (MARGEM_ESQ, SEG_TOPO + 24), None))
        if nar.get("legendas"):
            for k, (la, lz, txt) in enumerate(ler_srt(caminho(edl, nar["legendas"]))):
                img = render_legenda(aplicar_destaques(txt, nar.get("destaques", [])))
                ev.append((la, lz, f"leg_nar_{k}", img, (x_seguro(img.width), Y_LEGENDA - img.height // 2), None))
    # legendas das falas do Diego nas cenas (definidas por corte, no tempo do original)
    for k, (la, lz, txt) in enumerate(legendas_das_falas(edl)):
        img = render_legenda(txt)
        ev.append((la, lz, f"leg_fala_{k}", img, (x_seguro(img.width), Y_LEGENDA - img.height // 2), None))
    # aviso final
    if "aviso" in blocos:
        a, z = blocos["aviso"]
        cfg = tx.get("aviso", {})
        # "titulo": duas linhas no estilo do gancho (espelha a abertura); senão, o cartão com pílula
        img = render_titulo_gancho(cfg) if cfg.get("estilo") == "titulo" else render_cartao_final(cfg)
        ev.append((a + cfg.get("atraso", 0.25), z, "aviso", img, (x_seguro(img.width), cfg.get("y", 700)), "sobe"))
    for e in ev:  # confere a zona segura
        _, _, nome, img, (x, y), _ = e
        assert y >= SEG_TOPO - 1 and y + img.height <= H - SEG_BASE and x + img.width <= W - SEG_DIR + 60, \
            f"{nome} fora da zona segura: x={x} y={y} w={img.width} h={img.height}"
    return ev, total


Y_LEGENDA = 1420  # centro vertical das legendas (a caixa termina bem acima dos 250 px de baixo)


def quadro_de_texto(eventos, t):
    """Estado da camada de texto no instante t: lista de (id, alfa, dy)."""
    estado = []
    for a, z, nome, img, pos, anim in eventos:
        if a - 1e-6 <= t < z - 1e-6:
            alfa, dy = 1.0, 0
            if anim == "sobe":
                p = min(1.0, (t - a) / 0.35)
                p = 1 - (1 - p) ** 3  # ease-out
                alfa, dy = min(1.0, 0.25 + p), round((1 - p) * 26)
            estado.append((nome, round(alfa, 3), dy))
    return tuple(estado)


def etapa_texto(edl):
    pasta = os.path.join(edl["_tmp"], "texto")
    shutil.rmtree(pasta, ignore_errors=True)
    os.makedirs(pasta)
    eventos, _ = eventos_de_texto(edl)
    por_nome = {e[2]: e for e in eventos}
    anterior, arq_anterior = None, None
    for n in range(edl["_frames"]):
        estado = quadro_de_texto(eventos, n / FPS)
        arq = os.path.join(pasta, f"t_{n:05d}.png")
        if estado == anterior:
            os.link(arq_anterior, arq)
            continue
        quadro = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for nome, alfa, dy in estado:
            _, _, _, img, (x, y), _ = por_nome[nome]
            if alfa < 1:
                img = img.copy()
                img.putalpha(img.getchannel("A").point(lambda v: int(v * alfa)))
            quadro.alpha_composite(img, (x, y + dy))
        quadro.save(arq, compress_level=1)
        anterior, arq_anterior = estado, arq
    print(f"camada de texto: {edl['_frames']} frames", flush=True)


# ---------------------------------------------------------------- áudio

def ler_pcm(master, a, z):
    """Trecho do master como float32 estéreo 48 kHz (numpy, formato [amostras, 2])."""
    import numpy as np
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.4f}", "-t", f"{z - a:.4f}", "-i", master, "-vn",
                            "-af", f"aresample={SR}:resampler=soxr", "-ac", "2", "-f", "f32le", "-"],
                           capture_output=True, check=True).stdout
    return np.frombuffer(bruto, dtype=np.float32).reshape(-1, 2).copy()


def ambiente_substituto(edl, fontes, duracao, destino):
    """Cama de som ambiente sem música, montada com trechos limpos do próprio master.

    Cada trecho recebe nível equalizado (RMS igual à mediana, no máximo ±6 dB) e os trechos são
    encadeados com crossfade de potência constante de 60 ms, repetindo a lista se precisar.
    """
    import wave

    import numpy as np
    xf = int(0.06 * SR)
    trechos = [ler_pcm(edl["master"], float(a), float(z)) for a, z in fontes]
    rms = [float(np.sqrt(np.mean(t ** 2)) + 1e-9) for t in trechos]
    alvo = float(np.median(rms))
    trechos = [t * min(2.0, max(0.5, alvo / r)) for t, r in zip(trechos, rms)]
    n_total = int(round(duracao * SR))
    saida = np.zeros((n_total + xf, 2), dtype=np.float32)
    rampa = np.linspace(0, np.pi / 2, xf, dtype=np.float32)
    entra, sai = np.sin(rampa)[:, None], np.cos(rampa)[:, None]
    pos, k = 0, 0
    while pos < n_total:
        t = trechos[k % len(trechos)].copy()
        k += 1
        if len(t) <= 2 * xf:
            continue
        t[:xf] *= entra
        t[-xf:] *= sai
        fim = min(pos + len(t), len(saida))
        saida[pos:fim] += t[:fim - pos]
        pos += len(t) - xf
    pcm = (np.clip(saida[:n_total], -1, 1) * 32767).astype("<i2")
    with wave.open(destino, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def cadeia_voz(nr, nf, pre_db):
    """Tratamento de voz (narração e falas nas cenas), pensado para soar natural: passa-altas em 80 Hz,
    redução de ruído leve (afftdn com poucos dB, acompanhando o ruído), ganho até perto de -18 LUFS,
    realce sutil de 2,5 dB entre 2 e 5 kHz e compressão suave 2,5:1. Sem gate, pitch, de-esser ou reverb."""
    return (f"highpass=f=80:poles=2,afftdn=nr={nr}:nf={nf:.0f}:tn=1,volume={pre_db:.2f}dB,"
            f"equalizer=f=3200:t=o:w=1.3:g=2.5,"
            f"acompressor=threshold=-22dB:ratio=2.5:attack=12:release=180:knee=4")


def piso_ruido_db(arq, a=None, b=None):
    """Ruído de fundo estimado (percentil 10 do RMS em janelas de 20 ms), em dBFS, limitado ao que o afftdn aceita."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}"] if a is not None else []) + \
          ["-i", arq, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    fr = x[:len(x) // 320 * 320].reshape(-1, 320)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    return float(min(-20.0, max(-80.0, np.percentile(db, 10))))


def tratar_voz(edl, entrada, saida, trecho, nr, alvo):
    """Aplica a cadeia de voz a um wav e ajusta o ganho para a fala (trecho [a, b] do próprio wav) ficar em `alvo` LUFS."""
    a, b = trecho
    l0 = medir_loudness(entrada, a, b)["I"]
    nf = piso_ruido_db(entrada)
    tmp = saida + ".proc.wav"
    rodar(["ffmpeg", "-v", "error", "-y", "-i", entrada, "-af", cadeia_voz(nr, nf, -18.0 - l0),
           "-c:a", "pcm_f32le", "-ar", SR, tmp])
    l1 = medir_loudness(tmp, a, b)["I"]
    ganho = alvo - l1
    # o afftdn atrasa a saída (~25 ms): corta esse atraso no começo e completa o fim, para a voz não "pular" na imagem
    lat = float(edl.get("audio", {}).get("latencia_nr", 0.0))
    rodar(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
           f"atrim=start={lat},asetpts=PTS-STARTPTS,apad=pad_dur={lat},volume={ganho:.2f}dB", "-c:a", "pcm_f32le", saida])
    os.remove(tmp)
    return {"lufs_bruto": l0, "piso_db": nf, "ganho_final_db": ganho, "lufs_fala": medir_loudness(saida, a, b)["I"]}


def etapa_audio(edl):
    """Som de cada cena (original do bruto/master; só o fechamento usa ambiente de pausas, sem bruto utilizável),
    voz tratada nas cenas com fala, narração tratada, ducking por sidechain, crossfade de 0,2 s e -14 LUFS / -1 dBTP."""
    tmp = edl["_tmp"]
    cfg = edl.get("audio", {})
    alvo_fala = float(cfg.get("fala_lufs", -16.0))
    alvo_amb = float(cfg.get("ambiente_lufs", -24.0))
    borda = 0.1  # 0,1 s de cada lado: crossfade de 0,2 s centrado no corte
    entradas, filtros, relatorio = [], [], []
    for i, c in enumerate(edl["_cortes"]):
        dur = c["frames"] / FPS
        origem = c["entrada"]
        antes = min(borda, origem)
        pre = borda - antes
        bruto = os.path.join(tmp, f"a_{i:02d}_bruto.wav")
        arq = os.path.join(tmp, f"a_{i:02d}.wav")
        if c.get("ambiente_de"):  # sem bruto utilizável: ambiente de pausas sem música do master
            ambiente_substituto(edl, c["ambiente_de"], dur + 2 * borda, bruto)
        else:  # som original (0:a:0 = faixa AAC estéreo; o iPhone grava também uma espacial)
            rodar(["ffmpeg", "-v", "error", "-y", "-ss", f"{origem - antes:.4f}", "-i", c["_arq"],
                   "-map", "0:a:0", "-vn", "-t", f"{dur + antes + borda:.4f}", "-af",
                   f"aresample={SR}:resampler=soxr,adelay={int(round(pre * 1000))}:all=1,apad",
                   "-t", f"{dur + 2 * borda:.4f}", "-ac", "2", "-c:a", "pcm_f32le", bruto])
        if c.get("fala"):
            fa, fb = c["fala_trecho"]  # início e fim da fala, no tempo do arquivo de origem
            info = tratar_voz(edl, bruto, arq, (fa - origem + borda, fb - origem + borda),
                              float(cfg.get("fala_nr", 5)), alvo_fala)
            info["tipo"] = "fala"
        else:
            l0 = medir_loudness(bruto, borda, borda + dur)["I"]
            ganho = max(-12.0, min(14.0, alvo_amb - l0))
            rodar(["ffmpeg", "-v", "error", "-y", "-i", bruto, "-af", f"volume={ganho:.2f}dB", "-c:a", "pcm_f32le", arq])
            info = {"tipo": "ambiente", "lufs_bruto": l0, "ganho_final_db": ganho}
        info["corte"] = i + 1
        relatorio.append(info)
        print(f"  corte {i + 1}: {info}", flush=True)
        entradas += ["-i", arq]
        n_amostras = round((dur + 2 * borda) * SR)
        filtros.append(f"[{i}:a]apad,atrim=end_sample={n_amostras}[c{i}]")
    cadeia = "[c0]"
    for i in range(1, len(edl["_cortes"])):
        filtros.append(f"{cadeia}[c{i}]acrossfade=d={2 * borda}:c1=qsin:c2=qsin[x{i}]")
        cadeia = f"[x{i}]"
    total = edl["_frames"] / FPS
    filtros.append(f"{cadeia}atrim=start={borda}:end={borda + total},asetpts=PTS-STARTPTS,asplit=2[cenas][cenas_ref]")
    saidas_extra = ["-map", "[cenas_ref]", "-c:a", "pcm_f32le", "-ar", SR, os.path.join(tmp, "cenas_sem_ducking.wav")]
    nar = edl.get("narracao", {})
    ultimo = "[cenas]"
    if nar.get("arquivo"):
        a, b = nar.get("corte_tomada", [0, None])
        nar_bruto = os.path.join(tmp, "narracao_bruta.wav")
        nar_proc = os.path.join(tmp, "narracao_tratada.wav")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", caminho(edl, nar["arquivo"]), "-af",
               f"atrim=start={a}" + (f":end={b}" if b else "") + f",asetpts=PTS-STARTPTS,aresample={SR}:resampler=soxr,"
               "aformat=channel_layouts=stereo", "-c:a", "pcm_f32le", nar_bruto])
        va, vb = nar["voz_trecho"]  # voz dentro do arquivo original
        info = tratar_voz(edl, nar_bruto, nar_proc, (va - a, vb - a), float(nar.get("voz_nr", 6)), alvo_fala)
        info.update({"tipo": "narracao", "corte": "narração"})
        relatorio.append(info)
        print(f"  narração: {info}", flush=True)
        # limiar do ducking: com razão 20, o som das cenas cai ~11 dB quando a narração está no nível de fala
        rms_voz = rms_ativo_db(nar_proc)
        atenuacao = float(cfg.get("ducking_db", 11.0))
        razao = 20.0
        limiar_db = rms_voz - atenuacao / (1 - 1 / razao)
        k = len(edl["_cortes"])
        entradas += ["-i", nar_proc]
        # fade de saída com início calculado: no ffmpeg 6.1, areverse antes do adelay faz o atraso ser ignorado
        dur_nar = float(rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", nar_proc],
                              capturar=True))
        filtros.append(f"[{k}:a]afade=t=in:d=0.03,afade=t=out:st={dur_nar - 0.1:.3f}:d=0.1,"
                       f"adelay={int(round(float(nar['inicio']) * 1000))}:all=1,apad,atrim=end={total}[voz]")
        # sidechain de nível constante (ruído no nível da voz enquanto ela fala, pausas curtas preenchidas):
        # a redução fica estável em `atenuacao` dB, sem acompanhar cada sílaba nem voltar entre as frases (sem "respirar")
        sc_arq = os.path.join(tmp, "sidechain_ducking.wav")
        sidechain_constante(nar_proc, sc_arq, rms_voz, float(nar["inicio"]), total, float(cfg.get("segurar_pausa", 0.5)))
        entradas += ["-i", sc_arq]
        filtros.append(f"[{k + 1}:a]aformat=channel_layouts=stereo,atrim=end={total}[sc]")
        filtros.append(f"[cenas][sc]sidechaincompress=threshold={10 ** (limiar_db / 20):.5f}:ratio={razao}:attack=50:"
                       f"release={int(cfg.get('release_ms', 300))}:knee=2:detection=rms:makeup=1,asplit=2[cenas_duck][duck_ref]")
        filtros.append("[voz]asplit=2[voz_mix][voz_ref]")
        filtros.append("[cenas_duck][voz_mix]amix=inputs=2:duration=first:normalize=0[mix]")
        saidas_extra += ["-map", "[duck_ref]", "-c:a", "pcm_f32le", "-ar", SR, os.path.join(tmp, "cenas_com_ducking.wav"),
                         "-map", "[voz_ref]", "-c:a", "pcm_f32le", "-ar", SR, os.path.join(tmp, "narracao_no_reel.wav")]
        ultimo = "[mix]"
        edl["_ducking"] = {"rms_voz_db": rms_voz, "limiar_db": limiar_db, "razao": razao}
    fade = float(edl.get("fade_final", 0.5))
    filtros.append(f"{ultimo}afade=t=out:st={total - fade:.3f}:d={fade},atrim=end={total}[pre]")
    pre_lufs = os.path.join(tmp, "audio_pre.wav")
    rodar(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[pre]",
           "-c:a", "pcm_f32le", "-ar", SR, pre_lufs, *saidas_extra])
    # -14 LUFS integrados e pico verdadeiro <= -1 dBTP: ganho linear + limitador, conferido pelo ebur128
    alvo = float(edl.get("lufs", -14.0))
    # margem de 0,6 dB: o AAC do .mp4 sobe um pouco o pico verdadeiro em relação ao wav
    tp_wav = float(edl.get("tp", -1.0)) - 0.6
    ganho, limite = 0.0, 0.84
    for _ in range(6):
        final = os.path.join(tmp, "audio_final.wav")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", pre_lufs, "-af",
               f"volume={ganho:.2f}dB,alimiter=limit={limite:.3f}:attack=3:release=60:level=disabled,aresample={SR}",
               "-c:a", "pcm_s24le", final])
        medida = medir_loudness(final)
        print(f"  loudness: {medida['I']:.2f} LUFS, pico {medida['TP']:.2f} dBTP (ganho {ganho:+.2f} dB, limite {limite:.3f})", flush=True)
        ok_i, ok_tp = abs(medida["I"] - alvo) <= 0.3, medida["TP"] <= tp_wav
        if ok_i and ok_tp:
            break
        if not ok_tp:
            limite *= 10 ** ((tp_wav - 0.1 - medida["TP"]) / 20)
        if not ok_i:
            ganho += alvo - medida["I"]
    edl["_audio_relatorio"] = relatorio
    json.dump({"cortes": relatorio, "ducking": edl.get("_ducking"), "final": medida},
              open(os.path.join(tmp, "audio_relatorio.json"), "w"), indent=1, ensure_ascii=False)


def sidechain_constante(voz, destino, nivel_db, inicio, total, segurar):
    """Grava o sinal de controle do ducking: ruído rosa em `nivel_db` dBFS RMS onde há voz (janelas de 20 ms acima de 12 dB
    do ruído de fundo), com as pausas menores que `segurar` s preenchidas, e silêncio no resto."""
    import wave
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", voz, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    J = 960
    fr = x[:len(x) // J * J].reshape(-1, J)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    ativo = db > np.percentile(db, 10) + 12
    idx = np.where(ativo)[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if 1 < b - a <= segurar / 0.02:
            ativo[a:b] = True
    n = int(round(total * 48000))
    mascara = np.zeros(n)
    i0 = int(round(inicio * 48000))
    m = np.repeat(ativo.astype(float), J)[:max(0, n - i0)]
    mascara[i0:i0 + len(m)] = m
    rng = np.random.default_rng(1)
    branco = rng.standard_normal(n + 4096)
    rosa = np.convolve(branco, np.ones(8) / 8, "same")[:n]  # ruído com um pouco menos de agudo; o nível é o que importa
    rosa *= 10 ** (nivel_db / 20) / np.sqrt(np.mean(rosa ** 2))
    pcm = (np.clip(rosa * mascara, -1, 1) * 32767).astype("<i2")
    with wave.open(destino, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes(pcm.tobytes())


def rms_ativo_db(arq):
    """RMS (dBFS) só dos trechos com voz: janelas de 20 ms acima de 12 dB do ruído de fundo."""
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    fr = x[:len(x) // 320 * 320].reshape(-1, 320)
    rms = np.sqrt((fr ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(rms)
    ativo = db > np.percentile(db, 10) + 12
    return float(20 * np.log10(np.sqrt(np.mean(rms[ativo] ** 2))))


def rms_db(arq):
    """Nível RMS (dBFS) de um arquivo de áudio, em mono."""
    import numpy as np
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-ac", "1", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, dtype=np.float32)
    return 20 * math.log10(float(np.sqrt(np.mean(x.astype(np.float64) ** 2))) + 1e-9)


def medir_loudness(arq, a=None, b=None):
    corte = ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}"] if a is not None else []
    txt = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *corte, "-i", arq, "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    resumo = txt[txt.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", resumo).group(1).replace("-inf", "-99"))
    return {"I": i, "TP": tp}


# ---------------------------------------------------------------- final

def etapa_final(edl):
    tmp = edl["_tmp"]
    total = edl["_frames"] / FPS
    fade = float(edl.get("fade_final", 0.5))
    pasta = caminho(edl, edl.get("pasta_saida", "."))
    os.makedirs(pasta, exist_ok=True)
    comum = ["-c:v", "libx264", "-crf", "18", "-preset", "slow", "-profile:v", "high", "-level:v", "4.1",
             "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
             "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-ac", "2", "-movflags", "+faststart"]
    base = ["-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "video.txt")]
    audio = ["-i", os.path.join(tmp, "audio_final.wav")]
    fim = f"fade=t=out:st={total - fade:.3f}:d={fade}"
    # tempo de cada quadro refeito pelo índice (N/24): o concat soma a duração do contêiner de cada
    # intermediário, que às vezes vem 1 quadro maior (fonte a 23,976 fps) e atrasava o vídeo em relação
    # ao texto e ao áudio, que seguem a linha do tempo exata
    retime = f"setpts=N/({FPS}*TB)"
    # com texto
    filtro = (f"[0:v]{retime},format=yuv444p[b];"
              f"[1:v]scale=out_color_matrix=bt709:out_range=tv,format=yuva444p[t];"
              f"[b][t]overlay=0:0:format=yuv444:eof_action=pass,{fim},format=yuv420p[v]")
    rodar(["ffmpeg", "-v", "error", "-y", *base, "-framerate", FPS, "-i", os.path.join(tmp, "texto", "t_%05d.png"),
           *audio, "-filter_complex", filtro, "-map", "[v]", "-map", "2:a", "-frames:v", edl["_frames"], *comum,
           os.path.join(pasta, "reel_apresentacao.mp4")])
    # sem texto
    rodar(["ffmpeg", "-v", "error", "-y", *base, *audio, "-filter_complex", f"[0:v]{retime},{fim},format=yuv420p[v]",
           "-map", "[v]", "-map", "1:a", "-frames:v", edl["_frames"], *comum,
           os.path.join(pasta, "reel_apresentacao_sem_texto.mp4")])


# ---------------------------------------------------------------- capa

def etapa_capa(edl):
    cfg = edl.get("capa")
    if not cfg:
        return
    tmp = edl["_tmp"]
    quadro = os.path.join(tmp, "capa_base.png")
    c = {"entrada": segundos(cfg["tempo"]), "saida": segundos(cfg["tempo"]) + 1,
         "centro_x": cfg.get("centro_x", 0.5), "centro_y": cfg.get("centro_y", 0.5), "zoom": cfg.get("zoom", 1.0)}
    rodar(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['entrada']:.3f}", "-i", edl["master"], "-frames:v", "1",
           "-vf", f"{filtro_crop(c)},{TONEMAP.replace('format=yuv420p', 'format=rgb24')}", quadro])
    img = Image.open(quadro).convert("RGBA")
    # escurecimento suave atrás do título para legibilidade
    grad = Image.new("L", (1, H))
    for yy in range(H):
        grad.putpixel((0, yy), int(150 * max(0.0, 1 - abs(yy - cfg.get("y_titulo", 760)) / 700) ** 1.6))
    veu = Image.new("RGBA", (W, H), (12, 20, 28, 0))
    veu.putalpha(grad.resize((W, H)))
    img.alpha_composite(veu)
    titulo = render_titulo_gancho(cfg.get("titulo", {"linha1": "Aqui é o", "linha2": "Primeiro Dia"}))
    img.alpha_composite(titulo, ((W - titulo.width) // 2, cfg.get("y_titulo", 760) - titulo.height // 2))
    if cfg.get("apoio"):
        leg = render_legenda(cfg["apoio"], tam=46)
        img.alpha_composite(leg, ((W - leg.width) // 2, cfg.get("y_titulo", 760) + titulo.height // 2 + 20))
    img.alpha_composite(render_selo(), (MARGEM_ESQ + 60, 300))
    pasta = caminho(edl, edl.get("pasta_saida", "."))
    img.convert("RGB").save(os.path.join(pasta, "capa_reel_apresentacao.jpg"), quality=95)


# ---------------------------------------------------------------- verificação

def etapa_verificar(edl):
    pasta = caminho(edl, edl.get("pasta_saida", "."))
    for nome in ("reel_apresentacao.mp4", "reel_apresentacao_sem_texto.mp4"):
        arq = os.path.join(pasta, nome)
        info = rodar(["ffprobe", "-v", "error", "-show_entries",
                      "stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels,bit_rate:"
                      "format=duration,size,bit_rate", "-of", "compact", arq], capturar=True)
        m = medir_loudness(arq)
        print(nome, "\n", info.strip(), f"\n  loudness {m['I']:.2f} LUFS | pico {m['TP']:.2f} dBTP", flush=True)
    folha = os.path.join(pasta, "previa_reel_1fps.jpg")
    rodar(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(pasta, "reel_apresentacao.mp4"), "-vf",
           "fps=1,scale=216:384,tile=11x4:padding=4:color=black", "-frames:v", "1", folha])


ETAPAS = {"video": etapa_video, "texto": etapa_texto, "audio": etapa_audio, "final": etapa_final,
          "capa": etapa_capa, "verificar": etapa_verificar}

if __name__ == "__main__":
    edl = carregar(sys.argv[1])
    etapas = sys.argv[2:] or list(ETAPAS)
    print(f"{len(edl['_cortes'])} cortes, {edl['_frames']} frames = {edl['_frames'] / FPS:.2f} s; blocos:",
          {k: [round(v[0], 2), round(v[1], 2)] for k, v in edl["_blocos"].items()}, flush=True)
    for e in etapas:
        ETAPAS[e](edl)
