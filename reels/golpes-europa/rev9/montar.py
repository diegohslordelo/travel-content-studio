#!/usr/bin/env python3
"""3 golpes na Europa · REV9 · Reel completo (tela verde montada pelo Claude).

REV9 = REV8 com (pedido do Diego, 27/11/2026): take novo do 2º golpe (petição, IMG_8840),
"três" e "terceiro" de volta; frases com início e fim (decupagem nova, rev9/decupar.py);
24 fps (as gravações e o acervo são 24 fps: a 30 fps um quadro se repetia a cada 4);
imagem do Diego extraída por número de quadro; registro e verificação quadro a quadro.

REV8 = REV7 com (pedido do Diego, 27/11/2026): só o Diego no canto direito; legenda
centralizada logo acima da cabeça dele; print da Eurostat durante o dado (14 mil por dia).

Roda de dentro de reels/golpes-europa/, depois de rev9/decupar.py:
    python3 rev9/montar.py            # 2 vídeos: gancho A e gancho B, Diego à direita
    python3 rev9/montar.py A:dir      # só um

Pedido do Diego (27/11/2026): o Diego recortado (sem fundo) no canto inferior esquerdo,
sobre o fundo de golpes; voz decupada bem apertada; 2 vídeos, um por gancho; "GOLPES NA
EUROPA" fixo na tela durante o gancho; legenda desde o início, logo abaixo do texto do
gancho, sem cobrir o rosto do Diego.

Padrão de edição (CLAUDE.md, 12): legenda que acompanha a voz (grupo branco, palavra
colorida quando é dita), sem degradê na base, imagens sem tratamento, keen no fim do
gancho, sem música. DS só no CTA (CLAUDE.md, 6): aqui não entra componente do DS.
"""
import json
import os
import subprocess
import sys

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR = 1080, 1920, 24, 48000
FPS_DIEGO = 24                          # IMG_88xx: 24/1
G, A, D = "fonte/golpes/", "fonte/acervo/", "fonte/diego/"
TMP = "rev9/_tmp/"
RVM = os.environ.get("RVM_ONNX", "/tmp/claude-0/-home-user-travel-content-studio/"
                     "ab5afc7e-560c-53a8-a338-2cf94134f548/scratchpad/models/rvm_resnet50_fp32.onnx")

TONEMAP = (  # HLG do iPhone -> SDR, igual a reels/madrid-show/rev1/rev1.py
    "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
    "zscale=p=bt709,tonemap=tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv"
)
CROP = {  # gravações de tela: sem barra de status, interface, nomes e textos
    "g1_0738": "1056:1878:75:278", "g2_0739": "1206:2144:0:200", "g3_0740": "1122:1996:42:160",
    "g4_0742": "1206:2144:0:180", "g5_0744": "1206:2144:0:180", "g6_1357": "1206:2144:0:180",
    "g7_1538@metro": "953:1694:200:346", "g7_1538@veneza": "1206:2144:0:200",
}
CROP_X_ACERVO = {"IMG_3744": 1900}   # personagem azul inteiro

# Fundo de cada bloco: (arquivo, início, duração, fim_limpo). O último take do bloco fica
# com o que sobrar; fim_limpo é o último instante sem interface, texto ou troca de plano
# no arquivo de origem (medido quadro a quadro nas REV1–REV6). Take < 0,6 s é erro.
FUNDO = {
    "gancho": [("g6_1357", 1.75, None, 5.50)],
    "gancho_longo": [("g6_1357", 1.75, 2.90, 5.50), ("g2_0739", 0.60, None, 7.40)],   # gancho > 3,7 s
    "dado": [("g7_1538@metro", 1.90, 2.30, 4.40), ("g7_1538@veneza", 10.20, None, 15.30)],
    "relevancia": [("IMG_3647", 0.50, 3.00, 8.60), ("g2_0739", 2.00, 1.80, 7.40), ("g1_0738", 9.00, None, 30.80)],
    "abertura": [("g4_0742", 6.40, None, 22.90)],
    "golpe1": [("g5_0744", 6.15, 3.25, 9.40), ("g5_0744", 29.95, None, 34.60)],
    "golpe2": [("g3_0740", 1.40, 1.80, 10.50), ("g3_0740", 14.95, 1.00, 15.95), ("g3_0740", 3.20, None, 10.50)],
    "golpe3": [("IMG_3734", 0.40, 2.20, 4.04), ("IMG_3743", 0.30, 1.60, 4.50), ("IMG_3744", 2.20, None, 5.08)],
    "moral": [("IMG_3634", 0.20, None, 5.75)],
    "cta": [("IMG_3630", 0.20, 2.60, 3.08), ("IMG_3647", 3.50, None, 8.60)],
}
TAKE_MIN = 0.6

# Diego recortado no canto inferior esquerdo ou direito (pedido do Diego: as duas versões)
DIEGO_ESC = 0.60                       # 1080x1920 -> 648x1152
DW, DH = int(W * DIEGO_ESC), int(H * DIEGO_ESC)
DY = H - DH
DX_LADO = {"esq": 0, "dir": W - DW}
BORDA = 70                             # px de esmaecimento no corte vertical do lado de dentro

# Texto do gancho: fixo, sem entrar por partes (pedido do Diego, REV7)
FONTE_GANCHO = "rev9/fontes/Anton-Regular.ttf"
GANCHO = [("GOLPES", 220, (229, 57, 53)), ("NA EUROPA", 150, (255, 255, 255))]
GANCHO_X, GANCHO_Y, GANCHO_GAP = 72, 200, 20

# Legenda (docs/FORMATOS_REELS.md, 6, com o padrão de 19/11/2026): Inter 800, 66 px,
# branca, palavra dita em âmbar; centrada em x 540, logo acima da cabeça do Diego.
# Topo da cabeça medido no recorte: y >= 1037 no canvas (mediana 1088) -> legenda de y 925 a ~1000.
LEG_Y = 925

# Print da fonte do dado (Eurostat, Crime statistics, PDF oficial, dados de abril de 2026),
# com a frase dos 5 261 267 furtos grifada; entra seco durante o bloco do dado.
PRINT = "rev9/print_eurostat.png"
PRINT_Y = 290
FONTE_LEG = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
LEG_PX, LEG_COR, LEG_DITA = 66, (255, 255, 255), (224, 174, 92)
LEG_MAX_PAL, LEG_MAX_CAR, LEG_LARG_MAX = 3, 18, 872

KEEN = "../../design-system/sons/externos/keen.wav"
KEEN_PICO, KEEN_DB = 0.96, -6.0       # dB relativos à voz (CLAUDE.md, 12)

# Correções da transcrição na legenda, por take (1ª ocorrência). O Whisper do áudio já
# decupado erra nas emendas; a forma certa vem da transcrição do take inteiro.
CORRIGIR = {
    "golpe2": [("segundo", "Segundo"), ("você", "quando você")],   # take inteiro: "Quando você se comove"
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


# ---------------------------------------------------------------- voz e decupagem
def audio_take(arq):
    pcm = run(["ffmpeg", "-v", "error", "-i", D + arq, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
              capture_output=True).stdout
    return np.frombuffer(pcm, np.float32)


def montar_voz(seq, edl):
    """Concatena os trechos de cada take (5 ms de fade nas emendas). Devolve a voz, a lista
    de trechos com início na linha do tempo nova e o início de cada bloco."""
    partes, trechos, blocos, t = [], [], {}, 0
    fade = int(0.005 * SR)
    rampa = np.linspace(0, 1, fade, dtype=np.float32)
    for nome in seq:
        tk = edl[nome]
        x = audio_take(tk["arq"])
        blocos[nome] = t / SR
        for s, e in tk["trechos"]:
            a, b = int(round(s * SR)), int(round(e * SR))
            seg = x[a:b].copy()
            seg[:fade] *= rampa
            seg[-fade:] *= rampa[::-1]
            trechos.append({"bloco": nome, "arq": tk["arq"], "s": s, "e": e, "t0": t / SR})
            partes.append(seg)
            t += len(seg)
    return np.concatenate(partes), trechos, blocos, t / SR


def palavras_take(nome, tk, cache):
    """Retranscreve o take já decupado: os tempos ficam certos na linha do tempo nova."""
    if nome in cache:
        return cache[nome]
    from faster_whisper import WhisperModel
    global _WM
    if "_WM" not in globals():
        _WM = WhisperModel("large-v3", device="cpu", compute_type="int8")
    x = audio_take(tk["arq"])
    y = np.concatenate([x[int(round(s * SR)):int(round(e * SR))] for s, e in tk["trechos"]])
    y16 = y[:: SR // 16000]
    segs, _ = _WM.transcribe(y16, language="pt", word_timestamps=True, beam_size=5)
    pal = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    cache[nome] = pal
    return pal


# ---------------------------------------------------------------- legenda
def corrigir(nome, pal):
    pal = [dict(w) for w in pal]
    for velho, novo in CORRIGIR.get(nome, []):
        for w in pal:
            if w["w"].strip(".,!?;:…") == velho:
                w["w"] = w["w"].replace(velho, novo)
                break
    return pal


def grupos_legenda(pal):
    """Grupos de até 3 palavras / 18 letras; quebra depois de pontuação."""
    out, g = [], []
    for w in pal:
        txt = w["w"].strip(".,!?;:…")
        if not txt:
            continue
        cand = " ".join(x["t"] for x in g + [{"t": txt}])
        if g and (len(g) >= LEG_MAX_PAL or len(cand) > LEG_MAX_CAR):
            out.append(g)
            g = []
        g.append({"t": txt, "s": w["s"], "e": w["e"]})
        if w["w"][-1:] in ".,!?;:…":
            out.append(g)
            g = []
    if g:
        out.append(g)
    return out


def sombra_texto(img, xy, txt, font, cor, blur=12, off=4, alfa=(200, 110)):
    s = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).text((xy[0], xy[1] + off), txt, font=font, fill=(0, 0, 0, alfa[0]))
    s = s.filter(ImageFilter.GaussianBlur(blur))
    d = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(d).text((xy[0], xy[1] + off - 1), txt, font=font, fill=(0, 0, 0, alfa[1]))
    img.alpha_composite(s)
    img.alpha_composite(d)
    ImageDraw.Draw(img).text(xy, txt, font=font, fill=cor + (255,))


def img_gancho():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = GANCHO_Y
    for txt, px, cor in GANCHO:
        f = ImageFont.truetype(FONTE_GANCHO, px)
        x0, y0, x1, y1 = f.getbbox(txt)
        assert GANCHO_X + x1 - x0 <= 944
        sombra_texto(img, (GANCHO_X - x0, y - y0), txt, f, cor, blur=14)
        y += (y1 - y0) + GANCHO_GAP
    return img, y                      # y = base do texto do gancho


def img_legenda(grupo, n_ditas, y_topo, font):
    """Imagem RGBA (recortada) do grupo com as n primeiras palavras já ditas."""
    txts = [w["t"] for w in grupo]
    esp = font.getlength(" ")
    largs = [font.getlength(t) for t in txts]
    total = sum(largs) + esp * (len(txts) - 1)
    assert total <= LEG_LARG_MAX, f"legenda larga demais: {' '.join(txts)}"
    pad = 40
    img = Image.new("RGBA", (int(total) + 2 * pad, LEG_PX + 2 * pad), (0, 0, 0, 0))
    x = pad
    asc = font.getbbox("Ág")[1]
    for i, (t, lw) in enumerate(zip(txts, largs)):
        cor = LEG_DITA if i < n_ditas else LEG_COR
        sombra_texto(img, (x, pad - asc), t, font, cor, blur=10, off=3, alfa=(215, 90))
        x += lw + esp
    x0 = int(W / 2 - total / 2) - pad          # centro no canvas (x 540), CLAUDE.md, 12
    return img, (x0, y_topo - pad)


# ---------------------------------------------------------------- fundo
def filtro(nome):
    base = nome.split("@")[0]
    if base.startswith("IMG_"):
        x = CROP_X_ACERVO.get(base, (3840 - 1215) // 2)
        return f"{TONEMAP},crop=1215:2160:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS},format=rgb24"
    return f"crop={CROP[nome]},scale={W}:{H}:flags=lanczos,fps={FPS},format=rgb24"


def caminho(nome):
    base = nome.split("@")[0]
    return (A + base + ".MOV") if base.startswith("IMG_") else (G + base + ".mp4")


def plano_fundo(blocos_t, total):
    """Lista (arquivo, início, n_quadros, bloco) com os cortes de bloco no quadro certo."""
    ordem = list(blocos_t.items()) + [("_fim", total)]
    plano = []
    for (bloco, t0), (_, t1) in zip(ordem, ordem[1:]):
        f0, f1 = round(t0 * FPS), round(t1 * FPS)
        takes = FUNDO[bloco]
        if bloco == "gancho" and (f1 - f0) / FPS > (5.50 - 1.75):
            takes = FUNDO["gancho_longo"]
        f = f0
        for i, (arq, ini, dur, fim_limpo) in enumerate(takes):
            n = (f1 - f) if (dur is None or i == len(takes) - 1) else min(round(dur * FPS), f1 - f)
            assert n >= round(TAKE_MIN * FPS), f"take curto no fundo: {bloco} {arq} {n} quadros"
            assert ini + n / FPS <= fim_limpo + 1e-6, f"{bloco} {arq}: passa do fim limpo ({ini + n / FPS:.2f} > {fim_limpo})"
            plano.append((arq, ini, n, bloco))
            f += n
    return plano


def fundo_frames(plano):
    for arq, ini, n, _ in plano:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ini}", "-i", caminho(arq), "-vf", filtro(arq),
                             "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        lidos = 0
        while lidos < n:
            buf = p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                raise RuntimeError(f"fundo curto: {arq} {ini} ({lidos}/{n} quadros)")
            yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            lidos += 1
        p.stdout.close()
        p.wait()


def diego_frames(trechos, total, log):
    """Imagem do Diego pelo número exato do quadro de origem (24 fps -> 24 fps, 1:1)."""
    for i, tr in enumerate(trechos):
        t1 = trechos[i + 1]["t0"] if i + 1 < len(trechos) else total
        n = round(t1 * FPS) - round(tr["t0"] * FPS)
        if n <= 0:
            continue
        q0 = round(tr["s"] * FPS_DIEGO)
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", D + tr["arq"], "-vf",
                              f"trim=start_frame={q0},setpts=PTS-STARTPTS,scale={DW}:{DH}:flags=lanczos,format=rgb24",
                              "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for k in range(n):
            buf = p.stdout.read(DW * DH * 3)
            assert len(buf) == DW * DH * 3, f"faltou quadro do Diego: {tr['arq']} quadro {q0 + k}"
            log.append((tr["arq"], q0 + k))
            yield np.frombuffer(buf, np.uint8).reshape(DH, DW, 3)
        p.stdout.close()
        p.wait()


# ---------------------------------------------------------------- render
def render(versao, gancho, lado, edl, cache_pal):
    DX = DX_LADO[lado]
    seq = [gancho] + edl["ordem_corpo"]
    takes = edl["takes"]
    voz, trechos, blocos, total = montar_voz(seq, takes)

    # blocos do fundo: "fim" se divide em moral e CTA no início de "Se você gostou"
    blocos_t = {"gancho": blocos[gancho]}
    for b in edl["ordem_corpo"]:
        if b == "fim":
            tr_fim = [t for t in trechos if t["bloco"] == "fim"]
            blocos_t["moral"] = tr_fim[0]["t0"]
            blocos_t["cta"] = tr_fim[-1]["t0"]      # último trecho = "Se você gostou..."
        else:
            blocos_t[b] = blocos[b]
    plano = plano_fundo(blocos_t, total)
    n_total = round(total * FPS)

    # legenda: palavras retranscritas por take, deslocadas para a linha do tempo
    font_leg = ImageFont.truetype(FONTE_LEG, LEG_PX)
    gancho_img, base_gancho = img_gancho()
    y_leg = LEG_Y
    estados = []                                     # (f0, f1, img, xy)
    for nome in seq:
        pal = palavras_take(nome, takes[nome], cache_pal)
        off = blocos[nome]
        gs = grupos_legenda(corrigir(nome, pal))
        for gi, g in enumerate(gs):
            g_ini = g[0]["s"] + off
            g_fim = (gs[gi + 1][0]["s"] + off) if gi + 1 < len(gs) else min(g[-1]["e"] + off + 0.25,
                                                                            off + takes[nome]["dur"])
            for k in range(len(g)):
                s = (g[k]["s"] + off) if k else g_ini
                e = (g[k + 1]["s"] + off) if k + 1 < len(g) else g_fim
                img, xy = img_legenda(g, k + 1, y_leg, font_leg)
                estados.append((round(s * FPS), round(e * FPS), img, xy))
    estados.sort(key=lambda x: x[0])
    json.dump(cache_pal, open(f"{TMP}palavras.json", "w"), ensure_ascii=False, indent=1)

    f_fim_gancho = round(blocos_t["dado"] * FPS)
    f_print = (round(blocos_t["dado"] * FPS), round(blocos_t["relevancia"] * FPS))
    pr = np.asarray(Image.open(PRINT).convert("RGBA")).astype(np.float32) / 255
    ph, pw = pr.shape[:2]
    px = (W - pw) // 2
    gancho_np = np.asarray(gancho_img).astype(np.float32) / 255

    # esmaecimento do corte vertical à direita do recorte do Diego
    borda = np.ones((DH, DW), np.float32)
    rampa = np.linspace(1, 0, BORDA, dtype=np.float32)
    if lado == "esq":
        borda[:, DW - BORDA:] = rampa[None, :]
    else:
        borda[:, :BORDA] = rampa[::-1][None, :]

    rvm = ort.InferenceSession(RVM, providers=["CPUExecutionProvider"])
    rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
    dsr = np.array([0.4], np.float32)

    video = f"{TMP}video_{versao}_{lado}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", video], stdin=subprocess.PIPE)
    fg = fundo_frames(plano)
    log_diego = []
    dg = diego_frames(trechos, total, log_diego)
    ei = 0
    for f in range(n_total):
        bg = next(fg).astype(np.float32) / 255
        dfr = next(dg)
        src = (dfr.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        fgr, pha, *rec = rvm.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                        "downsample_ratio": dsr})
        a = (pha[0, 0] * borda)[..., None]
        reg = bg[DY:DY + DH, DX:DX + DW]
        bg[DY:DY + DH, DX:DX + DW] = dfr.astype(np.float32) / 255 * a + reg * (1 - a)
        if f < f_fim_gancho:
            ga = gancho_np[..., 3:4]
            bg = gancho_np[..., :3] * ga + bg * (1 - ga)
        if f_print[0] <= f < f_print[1]:
            al = pr[..., 3:4]
            r = bg[PRINT_Y:PRINT_Y + ph, px:px + pw]
            bg[PRINT_Y:PRINT_Y + ph, px:px + pw] = pr[..., :3] * al + r * (1 - al)
        while ei + 1 < len(estados) and estados[ei + 1][0] <= f:
            ei += 1
        if estados and estados[ei][0] <= f < estados[ei][1]:
            _, _, img, (x0, y0) = estados[ei]
            li = np.asarray(img).astype(np.float32) / 255
            h, w = li.shape[:2]
            xa, ya = max(0, x0), max(0, y0)
            sub = li[ya - y0:ya - y0 + min(h, H - ya), xa - x0:xa - x0 + min(w, W - xa)]
            al = sub[..., 3:4]
            r = bg[ya:ya + sub.shape[0], xa:xa + sub.shape[1]]
            bg[ya:ya + sub.shape[0], xa:xa + sub.shape[1]] = sub[..., :3] * al + r * (1 - al)
        enc.stdin.write((np.clip(bg, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if f % 150 == 0:
            print(f"  {versao} {lado}: quadro {f}/{n_total}", flush=True)
    enc.stdin.close()
    enc.wait()

    # áudio: voz + keen no corte gancho -> dado, normalizado para -14 LUFS / -1 dBTP
    voz_wav = f"{TMP}voz_{versao}.wav"
    import wave
    with wave.open(voz_wav, "wb") as wv:
        wv.setnchannels(1)
        wv.setsampwidth(2)
        wv.setframerate(SR)
        wv.writeframes((np.clip(voz, -1, 1) * 32767).astype(np.int16).tobytes())
    atraso = int(round((blocos_t["dado"] - KEEN_PICO) * 1000))
    lufs_voz = medir_lufs(voz_wav)
    lufs_keen = medir_lufs(KEEN)
    ganho_keen = (lufs_voz + KEEN_DB) - lufs_keen
    mix = f"{TMP}mix_{versao}.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", voz_wav, "-i", KEEN, "-filter_complex",
         f"[0]aformat=sample_rates={SR}:channel_layouts=stereo[v];"
         f"[1]aformat=sample_rates={SR}:channel_layouts=stereo,volume={ganho_keen:.2f}dB,adelay={atraso}|{atraso}[k];"
         f"[v][k]amix=inputs=2:duration=first:normalize=0[m]", "-map", "[m]", mix])
    fin = f"rev9/golpes_rev9_gancho{versao}.mp4"
    m = medir_lufs(mix, json_out=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mix, "-af",
         f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
         f"aresample={SR}", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", fin])
    json.dump({"plano_fundo": plano, "diego": log_diego, "trechos": trechos, "blocos": blocos_t,
               "legenda": [(a, b, ) for a, b, _, _ in estados], "n_quadros": n_total},
              open(f"{TMP}log_{versao}.json", "w"))
    print(f"{fin}: {total:.2f} s · keen com pico em {blocos_t['dado']:.2f} s ({ganho_keen:+.1f} dB no arquivo)")
    for b, t in blocos_t.items():
        print(f"  {b:<11} {t:6.2f} s")
    return blocos_t, total


def medir_lufs(arq, json_out=False):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", arq, "-af", "loudnorm=I=-14:TP=-1:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    return j if json_out else float(j["input_i"])


def main():
    os.makedirs(TMP, exist_ok=True)
    edl = json.load(open("rev9/edl.json"))
    cache_f = f"{TMP}palavras.json"
    cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    versoes = {"A": "ganchoA", "B": "ganchoB"}
    pedidos = sys.argv[1:] or [f"{v}:dir" for v in versoes]   # só canto direito (pedido do Diego)
    for p in pedidos:
        v, l = p.split(":")
        render(v, versoes[v], l, edl, cache)


if __name__ == "__main__":
    main()
