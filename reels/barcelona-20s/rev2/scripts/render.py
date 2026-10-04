"""Render do Reel "Barcelona em 20 segundos (POV)", REV2: 4 planos longos, cortes secos, placa de abertura e
símbolo 1º no fechamento.

Lê rev2.json (comum) e versao_unica.json (planos). Não altera nenhum bruto.

Etapas:
  1. planos  : probe de cada bruto (resolução, rotação, fps, HDR), recorte 9:16 e tempos em quadros (30 fps)
  2. audio   : som ambiente de cada plano, crossfade curto no corte, equilíbrio entre planos, nível final
  3. video   : bruto decodificado em RGB 16 bits (HLG → SDR com o tone mapping aprovado) → Arrasto → grão 5%
               → placa PRIMEIRO DIA → (Chegada/saída, 0–2 s) → símbolo 1º (Nascer) nos últimos 2 s
               → H.264 High CRF 14 + AAC 48 kHz
  4. qa      : medidas (formato, loudness, cortes, transições, zona segura) e frames de QA

Uso (de dentro de reels/barcelona-20s/):
  python3 rev1/scripts/render.py --versao a --fontes PASTA_DAS_FONTES [--brutos fonte]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np
import pyloudnorm
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pd  # noqa: E402
from pd import CFG, FPS, MS, W, H, T, SAFE  # noqa: E402

REV = pd.REV
SR = CFG["sr"]
SPF = SR // FPS
TAGS_COR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


def rodar(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def q(t):
    return int(round(t * FPS))


# ---------------------------------------------------------------- 1. planos

_INFO = {}


def info(arq):
    if arq in _INFO:
        return _INFO[arq]
    r = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", arq],
                                  capture_output=True, text=True, check=True).stdout)
    v = next(s for s in r["streams"] if s["codec_type"] == "video")
    a = next((s for s in r["streams"] if s["codec_type"] == "audio"), None)
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            rot = int(sd["rotation"])
    rot = int(v.get("tags", {}).get("rotate", rot))
    w, h = v["width"], v["height"]
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    trc = v.get("color_transfer")
    _INFO[arq] = {"w": w, "h": h, "rot": rot, "fps": num / den, "trc": trc,
                  "hdr": "hlg" if trc == "arib-std-b67" else ("pq" if trc == "smpte2084" else None),
                  "duracao": float(r["format"]["duration"]), "codec": v["codec_name"],
                  "bits": v.get("bits_per_raw_sample") or v.get("pix_fmt"), "audio": a is not None,
                  "audio_canais": a["channels"] if a else 0}
    return _INFO[arq]


def filtro_video(arq, p, largura=W, altura=H):
    """recorte para a proporção largura:altura (centro_x / centro_y do plano) + escala + cor → rgb48le."""
    inf = info(arq)
    w, h = inf["w"], inf["h"]
    alvo = largura / altura
    zoom = p.get("zoom", 1.0)
    if w / h > alvo:
        ch = h / zoom
        cw = ch * alvo
    else:
        cw = w / zoom
        ch = cw / alvo
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    cx = int(np.clip(p.get("centro_x", 0.5) * w - cw / 2, 0, w - cw))
    cy = int(np.clip(p.get("centro_y", 0.5) * h - ch / 2, 0, h - ch))
    f = [f"crop={cw}:{ch}:{cx}:{cy}"]
    if inf["fps"] > FPS + 0.5:
        f.insert(0, f"fps={FPS}")
    if inf["hdr"]:
        tm = CFG["tonemap"][inf["hdr"]]
        f.append(tm.replace("zscale=tin=", f"zscale=w={largura}:h={altura}:f=spline36:tin=", 1))
        f.append("scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb48le")
    else:
        f.append(f"scale={largura}:{altura}:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:"
                 "in_range=tv,format=rgb48le")
    return ",".join(f), {"recorte": [cw, ch, cx, cy], "escala": round(largura / cw, 3)}


def montar_planos(ed, brutos):
    out, r = [], 0
    for i, p in enumerate(ed["planos"]):
        arq = os.path.join(brutos, p["arquivo"])
        if not os.path.exists(arq):
            sys.exit(f"bruto não encontrado: {arq}")
        inf = info(arq)
        n = q(p["duracao"])
        if p["entrada"] + n / FPS > inf["duracao"] + 1e-3:
            sys.exit(f"plano {i + 1}: {p['arquivo']} tem {inf['duracao']:.3f} s; pedido até {p['entrada'] + n / FPS:.3f} s")
        filtro, rec = filtro_video(arq, p)
        out.append({**p, "n": i + 1, "caminho": arq, "q": n, "r0": r, "r1": r + n, "filtro": filtro, **rec,
                    "info": inf, "transicao": p.get("transicao", "seco")})
        r += n
    return out, r


# ---------------------------------------------------------------- 2. áudio

def ler_audio(arq, t0, dur):
    """trecho do bruto em float32 estéreo 48 kHz; preenche com silêncio fora do arquivo."""
    pre = max(0.0, -t0)
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t0, 0):.6f}", "-i", arq, "-t", f"{dur - pre:.6f}",
                        "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    a = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).astype(np.float64)
    n = int(round(dur * SR))
    out = np.zeros((n, 2))
    i0 = int(round(pre * SR))
    m = min(len(a), n - i0)
    out[i0:i0 + m] = a[:m]
    return out


def montar_audio(planos, N, tmp):
    A = CFG["audio"]
    E = A["equilibrio"]
    med = pyloudnorm.Meter(SR)
    h = int(round(A["crossfade_ms"] / 1000 * SR / 2))
    mix = np.zeros((N * SPF, 2))
    rel = []
    for i, p in enumerate(planos):
        ha = h if i > 0 else 0
        hb = h if i < len(planos) - 1 else 0
        r0, r1 = p["r0"] * SPF, p["r1"] * SPF
        if not p["info"]["audio"]:
            rel.append({"plano": p["n"], "sem_audio": True})
            continue
        trecho = ler_audio(p["caminho"], p["entrada"] - ha / SR, (r1 - r0 + ha + hb) / SR)
        try:
            lufs = med.integrated_loudness(trecho[ha:len(trecho) - hb]) if (r1 - r0) / SR >= 0.4 else -70.0
        except ValueError:
            lufs = -70.0
        if lufs < -60:
            ganho = 0.0
        else:
            ganho = float(np.clip((E["alvo_lufs"] - lufs) * E["fracao"], -E["limite_db"], E["limite_db"]))
        ganho += p.get("ganho_db", 0.0)
        env = np.ones(len(trecho))
        if ha:
            env[:2 * ha] = np.sin(np.linspace(0, np.pi / 2, 2 * ha, endpoint=False) + np.pi / (8 * ha))
        if hb:
            env[-2 * hb:] = np.cos(np.linspace(0, np.pi / 2, 2 * hb, endpoint=False) + np.pi / (8 * hb))
        mix[r0 - ha:r1 + hb] += trecho * env[:, None] * 10 ** (ganho / 20)
        rel.append({"plano": p["n"], "lufs_bruto": round(float(lufs), 1), "ganho_db": round(ganho, 1)})
    # bordas do loop: rampas curtas para o corte seco do fim para o início não estalar
    nb = int(A["fade_bordas_ms"] / 1000 * SR)
    rampa = np.linspace(0, 1, nb, endpoint=False)
    mix[:nb] *= rampa[:, None]
    mix[-nb:] *= rampa[::-1][:, None]
    lufs = med.integrated_loudness(mix)
    g = A["master_lufs"] - lufs
    mix *= 10 ** (g / 20)
    wav = os.path.join(tmp, "audio.f32")
    mix.astype(np.float32).tofile(wav)
    return wav, {"planos": rel, "lufs_antes_do_master": round(float(lufs), 1), "ganho_master_db": round(float(g), 1)}


# ---------------------------------------------------------------- 3. vídeo

class Fonte:
    """Lê os quadros de cada plano em ordem; permite olhar os primeiros quadros do plano seguinte (Arrasto)."""

    def __init__(self, planos):
        self.planos = planos
        self.proc = {}
        self.lidos = {}
        self.cache = {}

    def _abrir(self, i):
        p = self.planos[i]
        self.proc[i] = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-ss", f"{p['entrada']:.6f}", "-i", p["caminho"], "-vf", p["filtro"],
             "-frames:v", str(p["q"]), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)
        self.lidos[i] = 0

    def get(self, i, j):
        if (i, j) in self.cache:
            return self.cache[(i, j)]
        if i not in self.proc:
            self._abrir(i)
        tam = W * H * 6
        while self.lidos[i] <= j:
            buf = self.proc[i].stdout.read(tam)
            if len(buf) < tam:
                # bruto terminou antes: repete o último quadro (registrado no QA)
                ult = self.cache.get((i, self.lidos[i] - 1))
                assert ult is not None, f"plano {i + 1}: nenhum quadro decodificado"
                self.cache[(i, self.lidos[i])] = ult
                self.planos[i].setdefault("quadros_repetidos", 0)
                self.planos[i]["quadros_repetidos"] += 1
            else:
                self.cache[(i, self.lidos[i])] = np.frombuffer(buf, "<u2").reshape(H, W, 3).astype(np.float32) / 65535
            self.lidos[i] += 1
        # mantém só o necessário: o último quadro do plano anterior, os quadros recentes deste e os do seguinte
        for (a, b) in list(self.cache):
            if a < i - 1 or (a == i - 1 and b < self.planos[a]["q"] - 1) or (a == i and b < j - 4):
                del self.cache[(a, b)]
        return self.cache[(i, j)]

    def fechar(self):
        for p in self.proc.values():
            p.stdout.close()
            p.wait()


def deslizar(img, s, vizinho, lado):
    """img deslocada s px para a esquerda (s > 0) ou direita (s < 0); o vazio mostra a borda do vizinho
    (a cena seguinte entra pela direita, a anterior fica à esquerda), como uma tira contínua."""
    s = int(round(s))
    out = np.empty_like(img)
    if s > 0:      # cena que sai: anda para a esquerda, a próxima aparece à direita
        out[:, :W - s] = img[:, s:]
        out[:, W - s:] = vizinho[:, :s]
    elif s < 0:    # cena que entra: vem da direita, a anterior ainda aparece à esquerda
        s = -s
        out[:, s:] = img[:, :W - s]
        out[:, :s] = vizinho[:, W - s:]
    else:
        out[:] = img
    return out


def quadro_base(fonte, planos, k):
    """quadro k da montagem, já com o Arrasto aplicado quando o corte pede."""
    A = CFG.get("arrasto", {"quadros": 0, "desloc_frac": 0, "desfoque_px": 1})
    n_sai, n_entra = (A["quadros"] + 1) // 2, A["quadros"] // 2
    D = A["desloc_frac"] * W
    i = next(n for n, p in enumerate(planos) if p["r0"] <= k < p["r1"])
    p = planos[i]
    j = k - p["r0"]
    img = fonte.get(i, j)
    efeito = None
    if i + 1 < len(planos) and planos[i + 1]["transicao"] == "arrasto" and j >= p["q"] - n_sai:
        m = j - (p["q"] - n_sai)                           # 0..n_sai-1
        s = D * pd.E_IN((m + 1) / n_sai)
        img = deslizar(img, s, fonte.get(i + 1, 0), "sai")
        efeito = ("arrasto_sai", round(s, 1))
    elif p["transicao"] == "arrasto" and i > 0 and j < n_entra:
        s = D * (1 - pd.E_OUT(j / n_entra))
        img = deslizar(img, -s, fonte.get(i - 1, planos[i - 1]["q"] - 1), "entra")
        efeito = ("arrasto_entra", round(s, 1))
    if efeito:  # a REV2 não usa Arrasto (só cortes secos); o código fica para a configuração pedir
        img = ndimage.uniform_filter1d(img, size=A["desfoque_px"], axis=1, mode="nearest")
    return img, efeito


def linha_placa_abertura(k, q_fim):
    """Chegada a partir do quadro 0 (o quadro 0 já mostra t = 1 quadro); saída de 240 ms terminando em q_fim."""
    P = CFG["placa"]
    n_sai = int(round(P["saida"]["duracao_ms"] / MS))
    if k >= q_fim:
        return None
    if k >= q_fim - n_sai + 1:
        return ("saida", (k - (q_fim - n_sai)) * MS)
    return ("chegada", (k + 1) * MS)


def compor(k, base, ctx, registro):
    img = pd.overlay_blend(base, pd.grao(k), T["op_grain"])
    s = ctx["scrim"]
    if s is not None:
        img = img * (1 - s) + pd.GRAFITE * s
    camada = np.zeros((H, W, 4), np.float32)
    el = []
    st = linha_placa_abertura(k, ctx["q_fim_placa"])
    if st:
        pl = ctx["placa"]
        e = pl.estado(st[1]) if st[0] == "chegada" else pl.estado(None, saida_ms=st[1])
        im, x, y = pl.camada(e)
        pd.sobre(camada, im, x, y)
        xf = CFG["placa"]["x"] + e["dx"]
        el.append(["placa_abertura", round(xf, 1), CFG["placa"]["y"], round(xf + pl.fw + pl.lado, 1),
                   CFG["placa"]["y"] + pl.hh, st[0], round(st[1], 1)])
    if k >= ctx["q_fech"]:
        sb = ctx["simbolo"]
        t = (k - ctx["q_fech"] + 1) * MS
        pd.sobre(camada, sb.camada(t), sb.x0, sb.y0)
        if sb.tinta:
            el.append(["simbolo_1", *sb.tinta, round(min(t, sb.fim), 1)])
    registro[k] = el
    a = camada[..., 3:4]
    return img * (1 - a) + camada[..., :3]


def montar_video(planos, N, ctx, wav, saida):
    fonte = Fonte(planos)
    enc = subprocess.Popen([str(c) for c in [
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", FPS, "-i", "-",
        "-f", "f32le", "-ar", SR, "-ac", 2, "-i", wav,
        "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-af", f"alimiter=limit={10 ** (CFG['audio']['pico_dbtp'] / 20):.4f}:attack=5:release=60:level=disabled",
        "-map", "0:v", "-map", "1:a", "-frames:v", N,
        "-c:v", "libx264", "-crf", CFG["crf"], "-preset", CFG["preset_x264"], "-profile:v", "high", "-level:v", "4.2",
        "-pix_fmt", "yuv420p", "-r", FPS, *TAGS_COR,
        "-c:a", "aac", "-b:a", "256k", "-ar", SR, "-ac", 2, "-movflags", "+faststart", saida]], stdin=subprocess.PIPE)
    registro, efeitos = {}, {}
    for k in range(N):
        base, ef = quadro_base(fonte, planos, k)
        if ef:
            efeitos[k] = ef
        out = compor(k, base, ctx, registro)
        enc.stdin.write((np.clip(out, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
        if k % 60 == 0:
            print(f"   quadro {k}/{N}", flush=True)
    fonte.fechar()
    enc.stdin.close()
    assert enc.wait() == 0
    return registro, efeitos


# ---------------------------------------------------------------- 4. QA

def ebur128(arq):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-map", "0:a", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr[r.stderr.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", resumo).group(1)),
            float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resumo).group(1)))


def qa(saida, planos, N, registro, efeitos, audio_rel, ctx, pasta_qa, nome):
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_streams", "-of", "json", saida],
                                   capture_output=True, text=True, check=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    lufs, tp = ebur128(saida)
    cortes = [p["r0"] for p in planos[1:]]
    arrastos = [p["r0"] for p in planos if p["transicao"] == "arrasto"]
    duracoes = [round(p["q"] / FPS, 3) for p in planos]
    # zona segura: objeto parado (placa assentada, legenda) dentro de x 72–944 · y 256–1440
    fora = []
    for k, els in registro.items():
        for e in els:
            if e[0].startswith("placa") and (len(e) > 5 and e[5] == "saida" or abs(e[1] - CFG["placa"]["x"]) > 0.5):
                continue  # entrando ou saindo (a Chegada começa fora da tela, como o DS define)
            x0, y0, x1, y1 = e[1:5]
            if x0 < SAFE["x0"] - 0.5 or x1 > SAFE["x1"] + 0.5 or y0 < SAFE["y0"] or y1 > SAFE["y1"]:
                fora.append([k, *e[:5]])
    R = {
        "arquivo": os.path.basename(saida),
        "formato": {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"],
                    "quadros": int(v["nb_read_frames"]), "duracao_s": round(int(v["nb_read_frames"]) / FPS, 3),
                    "codec": f"{v['codec_name']} {v.get('profile')}", "pix_fmt": v["pix_fmt"],
                    "audio": f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} canais",
                    "tamanho_mb": round(os.path.getsize(saida) / 1e6, 1)},
        "audio": {"lufs_integrado": lufs, "pico_real_dbtp": tp, **audio_rel},
        "montagem": {"planos": len(planos), "cortes": len(cortes), "cortes_s": [round(c / FPS, 3) for c in cortes],
                     "duracao_planos_s": duracoes, "duracao_media_s": round(float(np.mean(duracoes)), 2),
                     "arrastos": len(arrastos), "arrastos_s": [round(c / FPS, 3) for c in arrastos],
                     "transicoes_total": len(arrastos),
                     "cortes_secos_pct": round(100 * (len(cortes) - len(arrastos)) / max(len(cortes), 1), 1),
                     "loop": "corte seco do último quadro para o quadro 0 (o Instagram repete o Reel)",
                     "quadros_arrasto": {str(k): v for k, v in efeitos.items()}},
        "planos": [{"n": p["n"], "arquivo": p["arquivo"], "entrada_s": p["entrada"],
                    "saida_s": round(p["entrada"] + p["q"] / FPS, 3), "no_reel_s": [round(p["r0"] / FPS, 3),
                                                                                    round(p["r1"] / FPS, 3)],
                    "categoria": p.get("categoria"), "descricao": p.get("descricao"), "transicao": p["transicao"],
                    "recorte": p["recorte"], "escala": p["escala"], "hdr": p["info"]["hdr"],
                    "fps_bruto": round(p["info"]["fps"], 3), "resolucao_bruto": [p["info"]["w"], p["info"]["h"]],
                    "quadros_repetidos": p.get("quadros_repetidos", 0)} for p in planos],
        "objetos": {"placa": ctx["placa"].medidas, "placa_abertura_quadros": [0, ctx["q_fim_placa"]],
                    "simbolo_1_quadros": [ctx["q_fech"], N], "simbolo_1_tinta": ctx["simbolo"].tinta,
                    "textos_na_tela": []},
        "zona_segura_violacoes": fora[:20],
        "zona_segura_ok": not fora,
    }
    # frames de QA
    shutil.rmtree(pasta_qa, ignore_errors=True)
    os.makedirs(pasta_qa)
    alvos = sorted(set([0, 4, 8, 12, 17, 30, ctx["q_fim_placa"] - 3] + [p["r0"] + p["q"] // 2 for p in planos] +
                       [ctx["q_fech"] + d for d in (4, 17, 25, 40)] + [N - 1]))
    lista = []
    for k in alvos:
        arq = os.path.join(pasta_qa, f"{nome}_q{k:03d}.jpg")
        rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", f"select=eq(n\\,{k})", "-frames:v", 1, "-q:v", 2, arq])
        lista.append((k, arq))
    esc = 0.25
    cw, ch = int(W * esc), int(H * esc)
    cols = 6
    folha = Image.new("RGB", (cols * cw, ((len(lista) + cols - 1) // cols) * (ch + 28)), (255, 255, 255))
    d = ImageDraw.Draw(folha)
    for i, (k, arq) in enumerate(lista):
        im = Image.open(arq).convert("RGB").resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle([SAFE["x0"] * esc, SAFE["y0"] * esc, SAFE["x1"] * esc, SAFE["y1"] * esc],
                                     outline=(255, 0, 0))
        x, y = (i % cols) * cw, (i // cols) * (ch + 28)
        folha.paste(im, (x, y))
        d.text((x + 4, y + ch + 6), f"quadro {k} · {k / FPS:.2f} s", fill=(0, 0, 0))
    folha.save(os.path.join(pasta_qa, f"folha_qa_{nome}.jpg"), quality=90)
    # Chegada (0–19), saída da placa e Nascer do 1º, faixa y 560–900
    for rot, k0, n in (("chegada", 0, 20), ("saida", ctx["q_fim_placa"] - 8, 8), ("nascer", ctx["q_fech"], 44)):
        rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf",
               f"select='between(n\\,{k0}\\,{k0 + n - 1})*not(mod(n-{k0}\\,{2 if rot == 'nascer' else 1}))',"
               f"crop={W}:340:0:{820 if rot == 'nascer' else 560},scale=540:170,tile=4x{(n // (2 if rot == 'nascer' else 1) + 3) // 4}",
               "-frames:v", 1, "-q:v", 2, os.path.join(pasta_qa, f"placa_{rot}_{nome}.jpg")])
    # Arrasto: os 6 quadros de cada um
    for c in arrastos:
        rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf",
               f"select='between(n\\,{c - 4}\\,{c + 3})',scale=270:480,tile=8x1", "-frames:v", 1, "-q:v", 2,
               os.path.join(pasta_qa, f"arrasto_q{c:03d}_{nome}.jpg")])
    R["frames_qa"] = [os.path.basename(a) for _, a in lista]
    return R


# ---------------------------------------------------------------- principal

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--versao", default="unica")
    ap.add_argument("--edl", default=None, help="outro arquivo de planos (teste)")
    ap.add_argument("--fontes", required=True, help="pasta com Barlow-Bold.ttf e BarlowCondensed-ExtraBold.ttf")
    ap.add_argument("--brutos", default="fonte", help="pasta dos brutos (padrão: fonte/, fora do git)")
    ap.add_argument("--saida-dir", default=None, help="pasta de saída (padrão: rev1/)")
    args = ap.parse_args()
    ed = json.load(open(args.edl or os.path.join(REV, "versao_unica.json"), encoding="utf-8"))
    nome = "barcelona20s_rev2"
    pasta = args.saida_dir or REV
    os.makedirs(pasta, exist_ok=True)
    saida = os.path.join(pasta, nome + ".mp4")
    tmp = os.path.join(REV, "_tmp", args.versao)
    os.makedirs(tmp, exist_ok=True)

    print("1/4 planos")
    planos, N = montar_planos(ed, args.brutos)
    for p in planos:
        print(f"   {p['n']:2d} {p['arquivo']:14s} {p['entrada']:7.3f}+{p['q'] / FPS:5.3f}s  reel {p['r0'] / FPS:6.3f}"
              f"  {p['transicao']:7s} {p['info']['w']}x{p['info']['h']} {p['info']['fps']:.2f}fps hdr={p['info']['hdr']}"
              f"  {p.get('categoria', '')}")
    print(f"   total {N} quadros = {N / FPS:.3f} s")

    assert len(planos) <= 4, "pedido da REV2: no máximo 4 vídeos"
    assert all(p["transicao"] == "seco" for p in planos), "REV2: só cortes secos"

    ctx = {"scrim": pd.scrim_alfa() if CFG["scrim"].get("ligado", True) else None,
           "placa": pd.Placa(args.fontes, "seta"), "simbolo": pd.Simbolo()}
    g = ed.get("gancho", {})
    q_fim = q(g.get("ate_s", planos[0]["q"] / FPS))
    ctx["q_fim_placa"] = q_fim
    ctx["q_fech"] = N - q(CFG["fechamento"]["duracao_s"])
    print("   placa", ctx["placa"].medidas)

    print("2/4 áudio")
    wav, audio_rel = montar_audio(planos, N, tmp)
    print("  ", audio_rel)

    print("3/4 vídeo")
    registro, efeitos = montar_video(planos, N, ctx, wav, saida)

    print("4/4 QA")
    R = qa(saida, planos, N, registro, efeitos, audio_rel, ctx, os.path.join(pasta, "qa_frames"),
           nome)
    R["versao"] = ed.get("versao")
    R["conceito"] = ed.get("conceito")
    R["sha256"] = hashlib.sha256(open(saida, "rb").read()).hexdigest()
    json.dump(R, open(os.path.join(pasta, "relatorio_tecnico_rev2.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    # prévia leve para celular
    rodar(["ffmpeg", "-v", "error", "-y", "-i", saida, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
           "-crf", 23, "-preset", "slow", "-pix_fmt", "yuv420p", *TAGS_COR, "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", os.path.join(pasta, nome + "_previa_leve.mp4")])
    print(json.dumps({k: R[k] for k in ("formato", "audio", "montagem", "zona_segura_ok")}, ensure_ascii=False,
                     indent=1, default=str)[:3000])
    print(saida)


if __name__ == "__main__":
    sys.exit(main())
