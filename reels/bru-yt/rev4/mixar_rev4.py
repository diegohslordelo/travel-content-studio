"""Mixagem da REV4 do vlog de Bruxelas (docs/AUDIO_REVIEW_STANDARD.md; DS V2 4.6). Parte da REV3 (`rev3/mixar_rev3.py`,
não alterada): mesma voz, narrações, níveis e master. Muda a música e duas emendas, pelo retorno do Diego (07/11/2026):

  "depois que você colocou minha fala do hotel, ficou estranho o som de fundo, como se tivesse um cd arranhado";
  "nos takes do restaurante do waffle as músicas também estão sobrepostas"; "no Manneken Pis também tá, parece que o
  vídeo já tava com áudio e vc jogou a música por cima"; "ajuste todos os momentos de música para as partes que eu não
  estou gravando em vlog"; "siga estritamente o minuto das músicas do arquivo (2)"; "você só vai adicionar a música do
  final e do início (The Mini Vandals)"; "waffle, 6:21 tem que entrar a música"; "sem sobreposição".

  - Música do corpo: as faixas LIMPAS que o Diego mandou (musica/musica_time_the_grey_room.mp3 e
    musica/musica_good_mornin_miss_eliza.mp3), nos 8 trechos em que o export com música (fonte/1103_musica.mp4, o "(2)")
    tem música, no mesmo ponto da faixa (correlação cruzada, scripts/achar_musica.py; deslocamento exato, 0 ms de
    dispersão). A REV3 tirava a música da diferença entre os dois exports: sobrava resíduo da voz (o "cd arranhado") e
    6 dos 12 blocos que ela achava não tinham música nenhuma. Em cada trecho, a música toca onde ela está no volume cheio no
    "(2)": ali o Diego deixou o som do clipe mudo e só a música; onde ele fala em vlog, a música do "(2)" some ou fica a
    −28 dB, e na REV4 não toca (pedido dele). Entrada de 0,25 s e saída de 0,5 s, sem encostar em palavra. Waffle: entra às 6:21,0 do vídeo (pedido do Diego).
  - Outros 4 trechos só de música do "(2)" (vídeo 1:03,4, 2:23,2, 11:41,8 e 13:23,9): são de músicas que não estão
    entre as 2 faixas (correlação ≈ 0,1); ali o export de fala é silêncio digital, então o som do "(2)" é a música pura
    e entra direto, no mesmo minuto (sem subtração).
  - Gancho, fechamento e tela final: "Good Mornin' Miss Eliza" (The Mini Vandals) limpa e contínua, sem costura:
    gancho a partir de 45,07 s da faixa e fechamento a partir de 7,50 s (os mesmos pontos de entrada da REV3).
  - Sem sobreposição de voz: plano do gancho sob a narração com fala da fonte (0:10,1–0:12,1, fonte 181,05) fica
    sem o som da fonte; fim de plano que corta a cauda de uma palavra ganha até 150 ms (só quando o começo do plano
    seguinte está em silêncio), com saída de 30 ms.

O Claude não escuta áudio: a escuta é do Diego (relatório da REV4).

Uso (de reels/bru-yt):  python rev4/mixar_rev4.py --saida _tmp/mix_rev4.wav [--sfx clip.wav --de MS --ate MS]
"""
import argparse
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000
NIVEL_REAL = {"gancho_fala": 0.0, "gancho_baixo": -14.0, "fechamento": -14.0, "corpo": 0.0}
MUSICA_ABAIXO = {"corpo": (3.0, 9.0), "pontas": (6.0, 15.0)}  # dB abaixo da fala: (sem voz, com voz)
TETO_DBTP = -2.0
FAIXAS = {"time": "musica/musica_time_the_grey_room.mp3", "eliza": "musica/musica_good_mornin_miss_eliza.mp3"}
# trechos com música no export "(2)" (fonte, s) e o deslocamento tempo-na-faixa − tempo-na-fonte (scripts/achar_musica.py)
BLOCOS = [
    ("T1", "time", 203.0, 229.5, -202.766),   # Fritland → Grand Place
    ("T2", "time", 288.0, 314.0, -267.299),   # Grand Place → hotel (narração H1) → Zinneke
    ("T3", "time", 322.0, 338.0, -267.299),   # Zinneke → waffle
    ("T4", "time", 345.5, 359.5, -267.299),   # waffle (entra às 6:21,0 do vídeo)
    ("T5", "time", 418.5, 441.0, -331.899),   # Galerias Saint-Hubert
    ("E1", "eliza", 463.5, 473.0, -463.031),  # Manneken Pis
    ("E2", "eliza", 517.5, 560.0, -513.199),  # Manneken Pis → Mont des Arts
    ("E3", "eliza", 615.5, 648.5, -573.932),  # Mont des Arts
]
ENTRA_VIDEO_MS = {"T4": 381000}  # "waffle, 6:21 tem que entrar a música"
GANCHO_FAIXA_S = 45.068      # = fonte 619,00 (REV3, trecho B)
FECHAMENTO_FAIXA_S = 7.501   # = fonte 520,70 (REV3, trecho A)


def suaviza(v, ms_subida, ms_descida, passo_ms=10):
    out = np.zeros_like(v, dtype=np.float64)
    up, dn = passo_ms / ms_subida, passo_ms / ms_descida
    a = 0.0
    for i, x in enumerate(v):
        a = min(x, a + up) if x > a else max(x, a - dn)
        out[i] = a
    return out


def comprime(x, alvo):
    """Compressor leve [PRECEDENTE REV6] de Amsterdam: 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, máx. 3 dB."""
    Bc = SR // 1000
    nb = len(x) // Bc
    rms = np.sqrt(np.mean(x[: nb * Bc].reshape(nb, Bc) ** 2, axis=1))
    lv = 20 * np.log10(np.sqrt(np.convolve(rms ** 2, np.ones(10) / 10, mode="same")) + 1e-9)
    exc = lv - (alvo + 8)
    red = np.minimum(np.where(exc <= -2, 0, np.where(exc >= 2, exc / 2, (exc + 2) ** 2 / 16)), 3.0)
    sm = np.zeros_like(red)
    at, rl = np.exp(-1 / 20), np.exp(-1 / 150)
    for i in range(1, len(red)):
        c = at if red[i] > sm[i - 1] else rl
        sm[i] = c * sm[i - 1] + (1 - c) * red[i]
    g = (10 ** (-np.interp(np.arange(len(x)) / Bc, np.arange(nb), sm) / 20)).astype(np.float32)
    return g, float(sm.max())


def narracao(n, alvo, medidor):
    """Narração tratada (estéreo) e onde começa (ms): passa-altas 80 Hz, fala no nível-alvo, compressor leve, recorte
    de 120 ms antes a 250 ms depois da fala, rampas de 30/80 ms (cadeia de Amsterdam, rev3/mixar_rev3.py)."""
    nome = n["arq"].split("/")[-1].replace(".m4a", "")
    x, sr = sf.read(f"_tmp/narr/{nome}.48k.wav", dtype="float32")
    assert sr == SR
    x = signal.sosfiltfilt(signal.butter(2, 80, btype="highpass", fs=SR, output="sos"), x).astype(np.float32)
    a0 = max(0, int((n["arq_ini_s"] - 0.12) * SR))
    a1 = min(len(x), int((n["arq_fim_s"] + 0.25) * SR))
    fala = x[int(n["arq_ini_s"] * SR):int(n["arq_fim_s"] * SR)]
    g_db = alvo - medidor.integrated_loudness(fala)
    y = x[a0:a1] * np.float32(10 ** (g_db / 20))
    # cortes internos (REV3: "que era do lado" na F1), de silêncio a silêncio, com fusão de 10 ms
    for c0, c1 in sorted(n.get("cortes", []), reverse=True):
        i0, i1 = int(c0 * SR) - a0, int(c1 * SR) - a0
        xf = int(0.01 * SR)
        rampa = np.linspace(0, 1, xf, dtype=np.float32)
        junta = y[i0 - xf:i0] * (1 - rampa) + y[i1 - xf:i1] * rampa
        y = np.concatenate([y[:i0 - xf], junta, y[i1:]])
    gc, red = comprime(y, alvo)
    y = y * gc
    fi, fo = int(0.03 * SR), int(0.08 * SR)
    y[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
    y[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
    inicio_ms = n["fala_ini"] - (n["arq_ini_s"] - a0 / SR) * 1000
    return np.column_stack([y, y]), inicio_ms, g_db, red


def carrega_faixa(arq):
    """Faixa limpa (mp3 do Diego) em estéreo 48 kHz float32."""
    wav = "_tmp/mus4/" + os.path.basename(arq).replace(".mp3", ".48k.wav")
    if not os.path.exists(wav):
        os.makedirs("_tmp/mus4", exist_ok=True)
        import subprocess
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", arq, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", wav], check=True)
    x, sr = sf.read(wav, dtype="float32")
    assert sr == SR
    return x


def energia_voz():
    """Energia da fonte na banda de voz (300–3400 Hz), em dB, a cada 10 ms (de _tmp/voz16k.wav)."""
    x, sr = sf.read("_tmp/voz16k.wav", dtype="float32")
    x = signal.sosfilt(signal.butter(4, [300, 3400], btype="band", fs=sr, output="sos"), x)
    J = sr // 100
    m = len(x) // J
    return 10 * np.log10((x[: m * J].reshape(m, J) ** 2).mean(axis=1) + 1e-12)


def cauda(e10, fim_s, prox_s, prox_mudo):
    """Quanto (s, até 0,15) estender um fim de plano que corta a cauda de uma palavra: a energia no corte passa 8 dB do
    piso local e o começo do plano seguinte está em silêncio (até 6 dB do piso dele) ou mudo. 0 se não precisar."""
    k = int(fim_s * 100)
    piso = np.percentile(e10[max(0, k - 200):k + 200], 15)
    if e10[max(0, k - 2):k].mean() - piso <= 8:
        return 0.0
    kq = int(prox_s * 100)
    piso_q = np.percentile(e10[max(0, kq - 200):kq + 200], 15)
    if not prox_mudo and e10[kq:kq + 15].mean() - piso_q > 6:
        return 0.0
    for d in range(1, 16):
        if e10[k + d] - piso <= 6:
            return d / 100 + 0.03
    return 0.15


def janelas_musica(palavras, ms):
    """Janelas (fonte, s) com música, copiadas do export "(2)": onde a faixa está no volume cheio nele (ganho da faixa
    acima de −12 dB, medido a cada 50 ms por regressão de ("(2)" − export de fala) sobre a faixa limpa; buracos de até
    0,5 s unidos; janelas de pelo menos 1 s). Nesses trechos o Diego deixou o som do clipe mudo (o export de fala é
    silêncio) e a música sozinha; onde ele fala, a música do "(2)" some ou fica a −28 dB (não entra aqui). Por
    segurança, a janela ainda fica entre as palavras da transcrição (±50 ms). Devolve (id, faixa, de, ate, desl)."""
    m2 = sf.read("_tmp/musica_orig.wav", dtype="float32")[0].mean(axis=1)
    v = sf.read("_tmp/voz_orig.wav", dtype="float32")[0].mean(axis=1)
    trk = {k: carrega_faixa(f).mean(axis=1) for k, f in FAIXAS.items()}
    P = 0.05
    n = int(P * SR)
    J = SR // 20
    ev = 10 * np.log10((v[: len(v) // J * J].reshape(-1, J) ** 2).mean(axis=1) + 1e-14)  # export de fala, 50 ms
    out = []
    for bid, fx, b0, b1, desl in BLOCOS:
        ts = np.arange(b0 - 3, b1 + 3, P)
        g = np.full(len(ts), -99.0)
        for i, t in enumerate(ts):
            s0, k = int(t * SR), int((t + desl) * SR)
            if k < 0 or k + n > len(trk[fx]):
                continue
            f = trk[fx][k:k + n]
            r = m2[s0:s0 + n] - v[s0:s0 + n]
            g[i] = 20 * np.log10(max(float(np.dot(r, f) / (np.dot(f, f) + 1e-9)), 1e-5))
        idx = np.flatnonzero(g > -12)
        if not len(idx):
            continue
        for gr in np.split(idx, np.flatnonzero(np.diff(idx) > int(0.5 / P)) + 1):
            a, b = float(ts[gr[0]]), float(ts[gr[-1]] + P)
            # a música do "(2)" entra e sai em rampa junto com o trecho mudo do clipe: a janela vai até as bordas do
            # silêncio do export de fala (até 1 s), para não ficar buraco de silêncio
            ka, kb = int(a * 20), int(b * 20)
            while ka > 0 and int(a * 20) - ka < 20 and ev[ka - 1] < -90:
                ka -= 1
            while kb < len(ev) and kb - int(b * 20) < 20 and ev[kb] < -90:
                kb += 1
            a, b = min(a, ka / 20), max(b, kb / 20)
            # fora das palavras (a música não encosta em fala de vlog)
            for w in palavras:
                if w["fim"] > a - 0.05 and w["ini"] < b + 0.05:
                    if w["ini"] <= a:
                        a = w["fim"] + 0.05
                    elif w["fim"] >= b:
                        b = w["ini"] - 0.05
            if b - a < 1.0:
                continue
            if bid in ENTRA_VIDEO_MS:
                for tt in np.arange(a, b, 0.01):
                    m_ = ms(tt)
                    if m_ is not None and m_ >= ENTRA_VIDEO_MS[bid]:
                        a = float(tt)
                        break
            out.append((bid, fx, a, b, desl))
    return out


def trechos_so_musica_2(janelas):
    """Trechos em que o export de fala é silêncio digital (< −90 dB por 50 ms, buracos de até 0,1 s unidos, pelo menos
    3 s) e o "(2)" tem som: ali o Diego deixou só a música, e o "(2)" é a música pura (sem voz, sem subtração). Os que
    já caem numa janela das faixas limpas ficam de fora. São músicas que não estão entre as 2 faixas que o Diego mandou
    (correlação ≈ 0,1 com as duas). Devolve (de, ate) na fonte."""
    v = sf.read("_tmp/voz_orig.wav", dtype="float32")[0].mean(axis=1)
    J = SR // 20
    n = len(v) // J
    ev = 10 * np.log10((v[: n * J].reshape(n, J) ** 2).mean(axis=1) + 1e-14)
    idx = np.flatnonzero(ev < -90)
    out = []
    for g in np.split(idx, np.flatnonzero(np.diff(idx) > 2) + 1):
        if len(g) < 60:
            continue
        a, b = g[0] / 20, (g[-1] + 1) / 20
        if any(a < jb and ja < b for _, _, ja, jb, _ in janelas):
            continue
        out.append((float(a), float(b)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sfx", default=None)
    ap.add_argument("--de", type=float, default=None, help="ms do vídeo final (com --sfx: onde o áudio do clipe começa)")
    ap.add_argument("--ate", type=float, default=None)
    ap.add_argument("--sem-master", action="store_true")
    a = ap.parse_args()
    lt = json.load(open("rev3/linha_do_tempo_rev3.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    cenas = json.load(open("_tmp/cenas.json"))["cortes"]
    dur_ms = lt["duracao_ms"]
    N = int(round(dur_ms * SR / 1000))
    medidor = pyln.Meter(SR)
    G, corpo_fim, F_fim = lt["gancho_ms"], lt["corpo_fim_ms"], lt["fechamento_fim_ms"]

    cache = "_tmp/vm_rev4.npz"
    if os.path.exists(cache) and os.path.getmtime(cache) > max(os.path.getmtime("rev3/linha_do_tempo_rev3.json"), os.path.getmtime(__file__)):
        z = np.load(cache)
        V, M = z["V"], z["M"]
        info = json.load(open(cache + ".json"))
    else:
        voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32")
        assert sr == SR
        n_src = len(voz)
        faixa = {k: carrega_faixa(v) for k, v in FAIXAS.items()}

        # ---------- 1. voz da fonte: ganho por plano (igual à REV1) ----------
        palavras = [w for s_ in tr["segmentos"] for w in s_["palavras"] if w["fim"] > w["ini"]]
        bordas = [0.0] + list(cenas) + [n_src / SR]
        planos = []
        for b0, b1 in zip(bordas, bordas[1:]):
            ws = [w for w in palavras if b0 <= w["ini"] < b1]
            if b1 - b0 < 1.0 or len(ws) < 3:
                planos.append((b0, b1, None))
                continue
            fala = np.concatenate([voz[int(w["ini"] * SR):int(w["fim"] * SR)] for w in ws])
            try:
                lv = medidor.integrated_loudness(fala) if len(fala) > SR // 2 else None
            except ValueError:
                lv = None
            planos.append((b0, b1, lv if lv is not None and np.isfinite(lv) else None))
        alvo = float(np.median([p_[2] for p_ in planos if p_[2] is not None]))
        pts_ms, pts_db, decisoes = [], [], []
        for b0, b1, lv in planos:
            g = float(np.clip(alvo - lv, -5, 5)) if lv is not None and abs(alvo - lv) > 1.5 else 0.0
            pts_ms += [b0 * 1000 + 100, b1 * 1000 - 100]
            pts_db += [g, g]
            if g:
                decisoes.append({"de": round(b0, 2), "ate": round(b1, 2), "lufs_fala": round(lv, 1), "ganho_db": round(g, 1)})
        t = np.arange(n_src, dtype=np.float64) * 1000 / SR
        ganho = (10 ** (np.interp(t, pts_ms, pts_db) / 20)).astype(np.float32)
        del t
        voz_t = signal.sosfiltfilt(signal.butter(2, 80, btype="highpass", fs=SR, output="sos"), voz, axis=0).astype(np.float32) * ganho[:, None]
        gc, red_max = comprime(voz_t.mean(axis=1), alvo)
        voz_t *= gc[:, None]
        del voz, ganho, gc

        # ---------- 2. voz no tempo do vídeo; falas reais do gancho no nível da fala ----------
        V = np.zeros((N, 2), np.float32)
        fade = int(0.008 * SR)
        anterior_fim = None
        ganho_gancho = []
        e10 = energia_voz()  # banda de voz da fonte, 10 ms (dB)
        aud = lt["audio"]
        # REV4: plano sob narração (gancho/fechamento, −14 dB) com fala da fonte fica sem o som da fonte (sem duas vozes)
        mudos = set()
        for k, p in enumerate(aud):
            if p["tipo"] in ("gancho_baixo", "fechamento"):
                dentro = [w for w in palavras if p["src"] <= w["ini"] and w["fim"] <= p["src"] + p["dur"] / 1000]
                if len(dentro) >= 2:
                    mudos.add(k)
        estendido = False
        extensoes = []
        for k, p in enumerate(aud):
            s0, o0 = int(round(p["src"] * SR)), int(round(p["out"] * SR / 1000))
            n = min(int(round(p["dur"] * SR / 1000)), n_src - s0, N - o0)
            if n <= 0:
                continue
            # REV4: fim de plano que corta a cauda de uma palavra ganha até 150 ms (sobre o começo, em silêncio, do plano
            # seguinte), com saída de 30 ms
            q = aud[k + 1] if k + 1 < len(aud) else None
            fim_s = p["src"] + p["dur"] / 1000
            ext = 0
            if q is not None and k not in mudos and abs(q["src"] - fim_s) > 0.01:
                ext = cauda(e10, fim_s, q["src"], k + 1 in mudos)
                o_fim = p["out"] + p["dur"]
                if any(o_fim - 20 <= nn["fala_ini"] <= o_fim + ext * 1000 + 20 for nn in lt["narracoes"]):
                    ext = 0
                if ext:
                    extensoes.append({"video_ms": round(o_fim), "fonte_s": round(fim_s, 2), "estende_ms": round(ext * 1000)})
            n_ext = min(n + int(ext * SR), n_src - s0, N - o0)
            ganho_tipo = 0.0 if k in mudos else 10 ** (NIVEL_REAL.get(p["tipo"], 0.0) / 20)
            ped = voz_t[s0:s0 + n_ext] * np.float32(ganho_tipo)
            if p["tipo"] == "gancho_fala":
                ws = [w for w in palavras if p["src"] <= w["ini"] and w["fim"] <= p["src"] + p["dur"] / 1000]
                if ws:
                    fala = np.concatenate([voz_t[int(w["ini"] * SR):int(w["fim"] * SR)] for w in ws])
                    try:
                        lv = medidor.integrated_loudness(fala)
                        g = float(np.clip(alvo - lv, -3, 8))
                    except ValueError:
                        g = 0.0
                    ped = ped * np.float32(10 ** (g / 20))
                    ganho_gancho.append({"fonte": round(p["src"], 2), "ganho_db": round(g, 1)})
            if n_ext > n:
                fo = int(0.03 * SR)
                ped[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            continuo = anterior_fim is not None and abs(anterior_fim - s0) <= 2 and p["tipo"] == "corpo"
            if not continuo:
                r = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                ped[:fade] *= r
                if o0 >= fade and not estendido:
                    V[o0 - fade:o0] *= r[::-1]
            V[o0:o0 + n_ext] += ped
            anterior_fim = s0 + n
            estendido = n_ext > n
        del voz_t

        # ---------- 2b. narrações ----------
        narr_info = []
        for n_ in lt["narracoes"]:
            y, ini_ms, g_db, red = narracao(n_, alvo, medidor)
            o0 = int(round(ini_ms * SR / 1000))
            V[o0:o0 + len(y)] += y[: N - o0]
            narr_info.append({"id": n_["id"], "arq": n_["arq"], "ganho_db": round(float(g_db), 1), "compressor_max_db": round(red, 1), "entra_ms": round(ini_ms)})

        # ---------- atividade de fala no vídeo (10 ms) ----------
        m10 = int(dur_ms / 10) + 1
        fala = np.zeros(m10)
        manter = lt["manter"]
        ini_src = [x / lt["fps"] for x, _ in manter]
        acc, ini_out = 0, []
        for x, y in manter:
            ini_out.append(acc)
            acc += y - x

        def ms(ts):
            i = max(0, np.searchsorted(ini_src, ts, side="right") - 1)
            x, y = manter[i]
            q = ts * lt["fps"]
            if q >= y or q < x:
                return None
            return G + (ini_out[i] + q - x) * 1000 / lt["fps"]

        for w in palavras:
            i0, i1 = ms(w["ini"]), ms(w["fim"])
            if i0 is not None and i1 is not None and 0 < i1 - i0 < 3000 and i0 < corpo_fim:
                fala[int(i0 / 10):int(i1 / 10) + 1] = 1
        for p in lt["audio"]:
            if p["tipo"] == "gancho_fala":
                fala[int(p["out"] / 10):int((p["out"] + p["dur"]) / 10)] = 1
        for n_ in lt["narracoes"]:
            fala[int(n_["fala_ini"] / 10):int(n_["fala_fim"] / 10)] = 1
        idx = np.flatnonzero(fala)
        for x, y in zip(idx, idx[1:]):
            if 1 < y - x <= 80:
                fala[x:y] = 1
        duck = suaviza(fala, 500, 500)
        np.save("_tmp/fala_rev4.npy", fala)

        # ---------- 3. música (REV4: faixas limpas, nos trechos e pontos da faixa do export "(2)") ----------
        M = np.zeros((N, 2), np.float32)

        def poe(seg, out_a_ms, nivel_lufs, fade_in, fade_out):
            o0 = int(round(out_a_ms * SR / 1000))
            n = min(len(seg), N - o0)
            seg = np.asarray(seg[:n], np.float32) * np.float32(10 ** (nivel_lufs / 20))
            fi, fo = min(int(fade_in * SR), n // 2), min(int(fade_out * SR), n // 2)
            if fi:
                seg[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
            if fo:
                seg[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            M[o0:o0 + n] += seg
            return o0, o0 + n

        pecas = []
        jans = janelas_musica(palavras, ms)
        for bid, fx, a_, b_, desl in jans:
            o_a = ms(a_) if ms(a_) is not None else ms(a_ + 0.05)
            o_b = ms(b_) if ms(b_) is not None else ms(b_ - 0.05)
            if o_a is None or o_b is None:
                continue
            o_b = min(o_b, corpo_fim)
            t0 = a_ + desl  # ponto da faixa = o mesmo do export "(2)" nesse minuto da fonte
            n = int((o_b - o_a) * SR / 1000)
            pecas.append((bid, fx, a_, b_, o_a, faixa[fx][int(round(t0 * SR)):int(round(t0 * SR)) + n], t0))
        # trechos só de música do "(2)" com outras músicas (som do "(2)" direto, no mesmo minuto)
        m2 = None
        outros = []
        for a_, b_ in trechos_so_musica_2(jans):
            o_a, o_b = ms(a_ + 0.05), ms(b_ - 0.05)
            if o_a is None or o_b is None or o_a >= corpo_fim:
                continue
            if m2 is None:
                m2 = sf.read("_tmp/musica_orig.wav", dtype="float32", always_2d=True)[0]
            o_b = min(o_b, corpo_fim)
            n = int((o_b - o_a) * SR / 1000)
            seg = m2[int(round((a_ + 0.05) * SR)):int(round((a_ + 0.05) * SR)) + n]
            g_db = alvo - MUSICA_ABAIXO["corpo"][0] - medidor.integrated_loudness(seg)
            i0, i1 = poe(seg, o_a, g_db, 0.25, 0.5)
            outros.append({"fonte_s": [round(a_, 2), round(b_, 2)], "video_ms": [round(i0 * 1000 / SR), round(i1 * 1000 / SR)], "ganho_db": round(g_db, 1)})
        # um ganho por faixa (o mesmo em todos os trechos dela): a faixa fica 3 dB abaixo da fala-alvo (corpo, REV3)
        lufs_faixa = {fx: medidor.integrated_loudness(np.concatenate([pc[5] for pc in pecas if pc[1] == fx])) for fx in faixa}
        info_mus = []
        for bid, fx, a_, b_, o_a, seg, t0 in pecas:
            g_db = alvo - MUSICA_ABAIXO["corpo"][0] - lufs_faixa[fx]
            # entra em 0,25 s e sai em 0,5 s, dentro da janela (as rampas do "(2)" levam de 0,5 a 1 s)
            i0, i1 = poe(seg, o_a, g_db, 0.25, 0.5)
            info_mus.append({"id": bid, "faixa": fx, "fonte_s": [round(a_, 2), round(b_, 2)], "faixa_s": [round(t0, 2), round(t0 + (i1 - i0) / SR, 2)],
                             "video_ms": [round(i0 * 1000 / SR), round(i1 * 1000 / SR)], "ganho_db": round(g_db, 1)})
        # gancho; fechamento + tela final: The Mini Vandals limpa e contínua (sem costura)
        # a música do gancho passa 0,9 s do gancho (como na REV3), mas termina 50 ms antes da 1ª fala do corpo
        prim = min((ms(w["ini"]) for w in palavras if ms(w["ini"]) is not None and ms(w["ini"]) >= G), default=G + 900)
        mg = faixa["eliza"][int(GANCHO_FAIXA_S * SR):int(GANCHO_FAIXA_S * SR) + int((min(G + 900, prim - 50)) / 1000 * SR)]
        g_g = alvo - MUSICA_ABAIXO["pontas"][0] - medidor.integrated_loudness(mg)
        poe(mg, 0, g_g, 0.02, 1.2)
        mf = faixa["eliza"][int(FECHAMENTO_FAIXA_S * SR):int(FECHAMENTO_FAIXA_S * SR) + int((dur_ms - corpo_fim) / 1000 * SR) + SR]
        g_f = alvo - MUSICA_ABAIXO["pontas"][0] - medidor.integrated_loudness(mf)
        poe(mf[: int((dur_ms - corpo_fim) / 1000 * SR)], corpo_fim, g_f, 0.8, 3.0)
        # ducking: com voz, mais 6 dB (corpo, total 9) ou mais 9 dB (gancho e fechamento, total 15)
        extra = np.full(len(duck), MUSICA_ABAIXO["corpo"][1] - MUSICA_ABAIXO["corpo"][0])
        extra[: int(G / 10)] = MUSICA_ABAIXO["pontas"][1] - MUSICA_ABAIXO["pontas"][0]
        extra[int(corpo_fim / 10):] = MUSICA_ABAIXO["pontas"][1] - MUSICA_ABAIXO["pontas"][0]
        for n_ in lt["narracoes"]:  # narração no corpo (hotel): a música desce como no gancho e no fechamento
            extra[int(n_["fala_ini"] / 10) - 50:int(n_["fala_fim"] / 10) + 50] = MUSICA_ABAIXO["corpo"][1] - MUSICA_ABAIXO["corpo"][0] + 6
        extra = np.convolve(extra, np.ones(50) / 50, mode="same")
        g_duck = (10 ** (-extra * duck / 20)).astype(np.float32)
        t10 = np.arange(N) / (SR / 100)
        M *= np.interp(t10, np.arange(len(g_duck)), g_duck).astype(np.float32)[:, None]
        info = {"alvo": alvo, "planos_com_ganho": decisoes, "compressor_max_db": round(red_max, 2), "falas_reais_gancho": ganho_gancho, "narracoes": narr_info,
                "musica_corpo": info_mus, "musica_outras_do_2": outros, "lufs_faixa": {k: round(v, 1) for k, v in lufs_faixa.items()},
                "musica_pontas": {"gancho_faixa_s": GANCHO_FAIXA_S, "fechamento_faixa_s": FECHAMENTO_FAIXA_S, "ganho_db": [round(g_g, 1), round(g_f, 1)]},
                "planos_mudos": [{"video_ms": aud[k]["out"], "fonte_s": aud[k]["src"]} for k in sorted(mudos)], "extensoes": extensoes}
        np.savez(cache, V=V, M=M)
        json.dump(info, open(cache + ".json", "w"), ensure_ascii=False, indent=1)

    # ---------- recorte, efeitos, master ----------
    i0 = int((a.de or 0) * SR / 1000)
    i1 = int((a.ate or dur_ms) * SR / 1000)
    out = V[i0:i1] + M[i0:i1]
    if a.sfx:
        sfx, srx = sf.read(a.sfx, dtype="float32")
        assert srx == SR, srx
        if sfx.ndim == 1:
            sfx = np.column_stack([sfx, sfx])
        n = min(len(sfx), len(out))
        out[:n] += sfx[:n]
    if not a.sem_master:
        lv = medidor.integrated_loudness(out)
        out *= np.float32(10 ** ((-14 - lv) / 20))
        teto = 10 ** (TETO_DBTP / 20)
        env = np.abs(signal.resample_poly(out.mean(axis=1), 4, 1)).reshape(-1, 4).max(axis=1)[: len(out)]
        env = np.maximum(env, np.abs(out).max(axis=1)[: len(env)])
        g = np.minimum(1.0, teto / np.maximum(env, 1e-9))
        k = int(0.005 * SR)
        g = -signal.convolve(-np.pad(g, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
        g = np.minimum(g, np.minimum(1.0, teto / np.maximum(env, 1e-9)))
        out *= g.astype(np.float32)[:, None]
    sf.write(a.saida, out, SR, subtype="PCM_24")
    print(json.dumps({"saida": a.saida, "seg": round(len(out) / SR, 2), "lufs": round(medidor.integrated_loudness(out), 1), "pico_dbfs": round(float(20 * np.log10(np.abs(out).max() + 1e-9)), 1),
                      "alvo_fala": round(info["alvo"], 1)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
