"""Mixagem da REV3 do vlog de Bruxelas (docs/AUDIO_REVIEW_STANDARD.md; DS V2 4.6). Igual à da REV2 (`rev2/mixar_rev2.py`,
não alterada), que partiu da REV1 e aplicou o retorno do Diego de 06/11/2026:

  - "no início a música fica muito alta… diminua tanto no início quanto no final, para não sobrepor a minha voz";
    "quando você coloca um take do vídeo mesmo, da minha voz em vlog, não dá para escutar quase nada":
    no gancho e no fechamento, a música fica 6 dB abaixo da fala sem voz e 15 dB abaixo com voz (no corpo, 3 e 9 dB,
    como antes); as falas reais do gancho são levadas ao nível da fala (ganho por take, até +8 dB);
  - "não precisa mudar a música no final… um take que deixa ela tocando o resto todo": fechamento e tela final com a
    MESMA faixa do começo (a do Mont des Arts, 10:19 da fonte, que é a mesma da montagem do Manneken Pis, 8:41),
    costurando 3 trechos dela com fusão de 1,5 s alinhada pela batida (envelope de ataques); o gancho também;
  - narrações gravadas (N01–N12): passa-altas 80 Hz, fala no nível da fala do vídeo, compressor leve, recorte de
    120 ms antes a 250 ms depois da fala, rampas de 30/80 ms (cadeia de Amsterdam).

A música sozinha sai da diferença entre os dois exports do Diego (ver `rev1/mixar_rev1.py`). O Claude não escuta
áudio: as costuras da música e os níveis entram na lista de escuta do relatório.

Uso (de reels/bru-yt):  python rev3/mixar_rev3.py --saida _tmp/mix_rev3.wav [--sfx clip.wav --de MS --ate MS]
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
# a mesma faixa nos dois trechos só de música da fonte (s): A = Manneken Pis → Mont des Arts; B = Mont des Arts, depois
# do violonista de rua (a música do Diego entra em 10:19). Gancho: B → A. Fechamento + tela final: A → B → A.
TRECHO_A = (520.70, 557.40)
TRECHO_B = (619.00, 645.50)


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


def separa_musica(m, v):
    """música = m − g·v, g por janela de 1 s (passo 0,5 s), limitado a [0; 1,1] e suavizado."""
    mm, vv = m.mean(axis=1), v.mean(axis=1)
    W, H = SR, SR // 2
    cs, gs = [], []
    for i in range(0, len(vv) - W, H):
        a, b = vv[i:i + W], mm[i:i + W]
        den = float(np.dot(a, a))
        gs.append(float(np.clip(np.dot(a, b) / den, 0, 1.1)) if den > 1e-6 else 0.0)
        cs.append(i + W // 2)
    gs = signal.medfilt(np.array(gs), 5)
    g = np.interp(np.arange(len(vv)), cs, gs).astype(np.float32)
    return m - v * g[:, None], gs


def envelope_ataques(x):
    """Envelope de ataques (fluxo espectral positivo, 10 ms) de um trecho mono 48 kHz."""
    f, t, Z = signal.stft(x, SR, nperseg=2048, noverlap=2048 - 480)
    M = np.log1p(np.abs(Z))
    return np.maximum(0, np.diff(M, axis=1)).sum(axis=0)


def costura(mus, trechos, dur_s, xf=1.5):
    """Uma faixa contínua de `dur_s` com os `trechos` (fonte, s) em sequência, repetindo a lista se precisar. Cada
    emenda é uma fusão de igual potência de `xf` s; o começo do trecho seguinte anda até 1 s para que os ataques
    (batidas) das duas pontas caiam juntos na fusão. Devolve o áudio e a lista de emendas (s na faixa)."""
    n_xf = int(xf * SR)
    out = np.zeros((0, 2), np.float32)
    emendas = []
    k = 0
    while len(out) < dur_s * SR:
        a, b = trechos[k % len(trechos)]
        if len(out) == 0:
            seg = np.asarray(mus[int(a * SR):int(b * SR)], np.float32)
            out = seg.copy()
        else:
            cauda = out[-n_xf:].mean(axis=1)
            ec = envelope_ataques(cauda)
            melhor, desl = -1, 0
            for d in range(0, int(1.0 * SR), SR // 100):
                cab = np.asarray(mus[int(a * SR) + d:int(a * SR) + d + n_xf], np.float32).mean(axis=1)
                eh = envelope_ataques(cab)
                n = min(len(ec), len(eh))
                sc = float(np.dot(ec[:n], eh[:n]) / (np.linalg.norm(ec[:n]) * np.linalg.norm(eh[:n]) + 1e-9))
                if sc > melhor:
                    melhor, desl = sc, d
            seg = np.asarray(mus[int(a * SR) + desl:int(b * SR)], np.float32)
            # nível igual dos dois lados da emenda (RMS dos 3 s em volta)
            r1 = np.sqrt(np.mean(out[-3 * SR:] ** 2)) + 1e-9
            r2 = np.sqrt(np.mean(seg[:3 * SR] ** 2)) + 1e-9
            seg = seg * np.float32(r1 / r2)
            th = np.linspace(0, np.pi / 2, n_xf, dtype=np.float32)[:, None]
            mist = out[-n_xf:] * np.cos(th) + seg[:n_xf] * np.sin(th)
            emendas.append({"em_s": round((len(out) - n_xf) / SR, 2), "de_fonte": [round(a, 2), round(b, 2)], "deslocamento_s": round(desl / SR, 2), "semelhanca_batida": round(melhor, 2)})
            out = np.concatenate([out[:-n_xf], mist, seg[n_xf:]])
        k += 1
    return out[: int(dur_s * SR)], emendas


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

    cache = "_tmp/vm_rev3.npz"
    if os.path.exists(cache) and os.path.getmtime(cache) > max(os.path.getmtime("rev3/linha_do_tempo_rev3.json"), os.path.getmtime(__file__)):
        z = np.load(cache)
        V, M = z["V"], z["M"]
        info = json.load(open(cache + ".json"))
    else:
        voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32")
        assert sr == SR
        n_src = len(voz)
        mus = np.load("_tmp/musica_stem.npy", mmap_mode="r")

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
        for p in lt["audio"]:
            s0, o0 = int(round(p["src"] * SR)), int(round(p["out"] * SR / 1000))
            n = min(int(round(p["dur"] * SR / 1000)), n_src - s0, N - o0)
            if n <= 0:
                continue
            ped = voz_t[s0:s0 + n] * np.float32(10 ** (NIVEL_REAL.get(p["tipo"], 0.0) / 20))
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
            continuo = anterior_fim is not None and abs(anterior_fim - s0) <= 2 and p["tipo"] == "corpo"
            if not continuo:
                r = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                ped[:fade] *= r
                if o0 >= fade:
                    V[o0 - fade:o0] *= r[::-1]
            V[o0:o0 + n] += ped
            anterior_fim = s0 + n
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
        np.save("_tmp/fala_rev3.npy", fala)

        # ---------- 3. música ----------
        M = np.zeros((N, 2), np.float32)
        mm = np.sqrt(np.mean(np.asarray(mus).mean(axis=1)[: n_src // (SR // 10) * (SR // 10)].reshape(-1, SR // 10) ** 2, axis=1))
        tem = 20 * np.log10(mm + 1e-9) > -42
        blocos, i = [], 0
        while i < len(tem):
            if tem[i]:
                j = i
                while j < len(tem) and (tem[j] or tem[j:j + 15].any()):
                    j += 1
                if j - i >= 20:
                    blocos.append((i / 10, j / 10))
                i = j
            else:
                i += 1
        nivel_mus = []

        def poe(seg, out_a_ms, abaixo, fade_in=0.15, fade_out=0.6, ref=None):
            o0 = int(out_a_ms * SR / 1000)
            n = min(len(seg), N - o0)
            if n <= SR // 10:
                return
            seg = np.asarray(seg[:n], np.float32).copy()
            try:
                lv_ = medidor.integrated_loudness(ref if ref is not None else seg)
            except ValueError:
                return
            if not np.isfinite(lv_):
                return
            nivel_mus.append(round(float(lv_), 1))
            seg *= np.float32(10 ** ((alvo - abaixo - lv_) / 20))
            # nivelamento (REV3): a música do export sobe e desce dentro do mesmo bloco (alta nas montagens, baixa sob a
            # fala do Diego); o envelope de 3 s é levado à mediana do trecho (−12 a +4 dB, suavizado em 1,5 s)
            mono = seg.mean(axis=1)
            J = SR // 100
            m_ = len(mono) // J
            e10 = mono[: m_ * J].reshape(m_, J)
            w3 = max(1, min(300, m_))
            e10 = 10 * np.log10(np.convolve((e10 ** 2).mean(axis=1), np.ones(w3) / w3, mode="same") + 1e-12)
            vivo = e10 > np.max(e10) - 30
            if vivo.any():
                ref_ = np.median(e10[vivo])
                gdb = np.clip(ref_ - e10, -12, 4)
                gdb[~vivo] = 0
                w15 = max(1, min(150, m_))
                gdb = np.convolve(gdb, np.ones(w15) / w15, mode="same")
                seg *= (10 ** (np.interp(np.arange(n) / J, np.arange(m_), gdb) / 20)).astype(np.float32)[:, None]
            fi, fo = min(int(fade_in * SR), n // 2), min(int(fade_out * SR), n // 2)
            if fi:
                seg[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
            if fo:
                seg[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            M[o0:o0 + n] += seg

        for b0, b1 in blocos:  # música do Diego no corpo (contínua a partir do início de cada bloco)
            if b0 >= 862.2:
                continue
            o_a = ms(b0) if ms(b0) is not None else ms(b0 + 0.05)
            if o_a is None:
                continue
            o_b = ms(min(b1, 862.19))
            o_b = min(o_b if o_b is not None else corpo_fim, corpo_fim)
            poe(mus[int(b0 * SR):int(b0 * SR) + int((o_b - o_a) * SR / 1000)], o_a, MUSICA_ABAIXO["corpo"][0])
        # gancho: B → A; fechamento + tela final: A → B → A (a mesma faixa)
        mg, emendas_g = costura(mus, [TRECHO_B, TRECHO_A], (G + 900) / 1000)
        poe(mg, 0, MUSICA_ABAIXO["pontas"][0], 0.02, 1.2, ref=mg)
        mf, emendas_f = costura(mus, [TRECHO_A, TRECHO_B], (dur_ms - corpo_fim) / 1000)
        poe(mf, corpo_fim, MUSICA_ABAIXO["pontas"][0], 0.8, 3.0, ref=mf)
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
                "blocos_musica": [(round(x, 2), round(y, 2)) for x, y in blocos], "nivel_musica_lufs": nivel_mus,
                "emendas_gancho": emendas_g, "emendas_fechamento": [{**e, "no_video_ms": round(corpo_fim + e["em_s"] * 1000)} for e in emendas_f]}
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
