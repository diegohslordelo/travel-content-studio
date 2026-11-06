"""Mixagem da REV1 do vlog de Bruxelas (docs/AUDIO_REVIEW_STANDARD.md; DS V2 4.6; cadeia de Amsterdam,
`reels/ams-yt/rev3/mixar_rev3.py`). ESTA REVISÃO É PRÉVIA: as narrações (G1–G3, H1, F1–F6) ainda não existem; os
trechos delas entram na mixagem só como "fala" para a música abaixar (ducking), e o texto aparece na tela.

O Diego mandou 2 exports do mesmo projeto (06/11/2026): `1103_fala.mp4` (música silenciada) e `1103_musica.mp4`
(1080p, com a música). A música sozinha sai da diferença: música = (arquivo com música) − g × (arquivo de fala), com g
estimado por mínimos quadrados em janelas de 1 s (onde o export com música tem a voz igual, g ≈ 1,00; medido em
06/11/2026). O resíduo de voz fica ≥ 25 dB abaixo da fala.

Cadeia:
  1. Voz da fonte: passa-altas 80 Hz; ganho por plano (corte de cena) para a fala ficar na mediana dos planos
     (±5 dB, só se a diferença passar de 1,5 dB; rampas de 200 ms); compressor leve (2:1, máx. 3 dB). Sem redução de
     ruído nesta prévia (o diagnóstico do padrão de áudio entra na revisão com as narrações).
  2. Som real dos clipes: falas reais do gancho em 0 dB; outros clipes do gancho e do fechamento 14 dB abaixo.
  3. Música do Diego no corpo (blocos onde ela existe na fonte, tocando contínua a partir do início do bloco, sem
     pular nos cortes da decupagem): 3 dB abaixo da fala sem fala; 9 dB abaixo com fala (transição de 500 ms).
     Gancho e fechamento: trechos da mesma música (PROVISÓRIO: o export só tem 5 s de música depois de 14:22; a faixa
     do fechamento é decisão do Diego, da Biblioteca de áudio do YouTube).
  4. Efeitos: vêm do render do Remotion (`--sfx`), somados como estão.
  5. Master: −14 LUFS integrados, limitador com teto de −2,0 dBTP (a correção pós-AAC vem no render final).

Uso (de reels/bru-yt):  python rev1/mixar_rev1.py --saida _tmp/mix_rev1.wav [--sfx clip.wav --de MS --ate MS]
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
TETO_DBTP = -2.0
# música do gancho e do fechamento (PROVISÓRIO): trechos só de música do export do Diego (fonte, s)
MUS_GANCHO = (619.00, 645.50)   # montagem do Mont des Arts, depois do violonista de rua (a música do Diego entra em 10:19)
MUS_FECHAMENTO = [(521.00, 557.30), (27.10, 46.20)]  # Manneken Pis → Mont des Arts; abertura (metrô → Atomium)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sfx", default=None)
    ap.add_argument("--de", type=float, default=None, help="ms do vídeo final (com --sfx: onde o áudio do clipe começa)")
    ap.add_argument("--ate", type=float, default=None)
    ap.add_argument("--sem-master", action="store_true")
    a = ap.parse_args()
    lt = json.load(open("rev1/linha_do_tempo_rev1.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    cenas = json.load(open("_tmp/cenas.json"))["cortes"]
    dur_ms = lt["duracao_ms"]
    N = int(round(dur_ms * SR / 1000))
    medidor = pyln.Meter(SR)

    cache = "_tmp/vm_rev1.npy"
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime("rev1/linha_do_tempo_rev1.json"):
        VM = np.load(cache)
        info = json.load(open(cache + ".json"))
    else:
        voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32")
        mus_full, _ = sf.read("_tmp/musica_orig.wav", dtype="float32")
        assert sr == SR
        n_src = len(voz)
        if os.path.exists("_tmp/musica_stem.npy"):
            mus = np.load("_tmp/musica_stem.npy")
        else:
            mus, gs = separa_musica(mus_full, voz)
            np.save("_tmp/musica_stem.npy", mus)
            print(f"g (voz no export com música): mediana {np.median(gs[gs > 0]):.3f}")
        del mus_full

        # ---------- 1. voz: ganho por plano ----------
        palavras = [w for s_ in tr["segmentos"] for w in s_["palavras"] if w["fim"] > w["ini"]]
        bordas = [0.0] + [c for c in cenas] + [n_src / SR]
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
        niveis = [p[2] for p in planos if p[2] is not None]
        alvo = float(np.median(niveis))
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

        # ---------- 2. voz no tempo do vídeo ----------
        V = np.zeros((N, 2), np.float32)
        fade = int(0.008 * SR)
        anterior_fim = None
        for p in lt["audio"]:
            s0, o0 = int(round(p["src"] * SR)), int(round(p["out"] * SR / 1000))
            n = min(int(round(p["dur"] * SR / 1000)), n_src - s0, N - o0)
            if n <= 0:
                continue
            ped = voz_t[s0:s0 + n] * np.float32(10 ** (NIVEL_REAL.get(p["tipo"], 0.0) / 20))
            continuo = anterior_fim is not None and abs(anterior_fim - s0) <= 2 and p["tipo"] == "corpo"
            if not continuo:
                r = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                ped[:fade] *= r
                if o0 >= fade:
                    V[o0 - fade:o0] *= r[::-1]
            V[o0:o0 + n] += ped
            anterior_fim = s0 + n
        del voz_t

        # ---------- atividade de fala no vídeo (10 ms): palavras do corpo + falas reais do gancho + narrações ----------
        m10 = int(dur_ms / 10) + 1
        fala = np.zeros(m10)
        manter = lt["manter"]
        G = lt["gancho_ms"]
        ini_src = [x / lt["fps"] for x, _ in manter]
        acc, ini_out = 0, []
        for x, y in manter:
            ini_out.append(acc)
            acc += y - x

        def ms(ts):
            i = max(0, np.searchsorted(ini_src, ts, side="right") - 1)
            x, y = manter[i]
            q = ts * lt["fps"]
            if q >= y:
                return None
            return G + (ini_out[i] + q - x) * 1000 / lt["fps"]

        for w in palavras:
            i0, i1 = ms(w["ini"]), ms(w["fim"])
            if i0 is not None and i1 is not None and 0 < i1 - i0 < 3000 and i0 < lt["corpo_fim_ms"]:
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

        # ---------- 3. música ----------
        M = np.zeros((N, 2), np.float32)
        # blocos de música: nível em janelas de 100 ms acima de −42 dBFS, buracos ≤ 1,5 s fechados, blocos < 2 s fora
        # (o resíduo da subtração nas falas sem música fica abaixo disso)
        J = SR // 10
        mm = np.sqrt(np.mean(mus.mean(axis=1)[: n_src // J * J].reshape(-1, J) ** 2, axis=1))
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

        def coloca(src_a, src_b, out_a, out_fim, fade_in=0.15, fade_out=0.6):
            n = int(min((src_b - src_a) * SR, (out_fim - out_a) * SR / 1000))
            s0, o0 = int(src_a * SR), int(out_a * SR / 1000)
            n = min(n, N - o0, len(mus) - s0)
            if n <= SR // 10:
                return 0
            seg = mus[s0:s0 + n].copy()
            try:
                lv_ = medidor.integrated_loudness(seg)
            except ValueError:
                lv_ = -40.0
            if not np.isfinite(lv_):
                return 0
            nivel_mus.append(lv_)
            seg *= np.float32(10 ** ((alvo - 3 - lv_) / 20))
            fi, fo = min(int(fade_in * SR), n // 2), min(int(fade_out * SR), n // 2)
            if fi:
                seg[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
            if fo:
                seg[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            M[o0:o0 + n] += seg
            return n / SR

        corpo_fim = lt["corpo_fim_ms"]
        for b0, b1 in blocos:
            if b0 >= 862.2:
                continue
            o_a = ms(b0) if ms(b0) is not None else ms(b0 + 0.05)
            o_b = ms(min(b1, 862.19))
            if o_a is None:
                continue
            o_b = o_b if o_b is not None else corpo_fim
            coloca(b0, b1, o_a, min(o_b, corpo_fim))
        coloca(MUS_GANCHO[0], MUS_GANCHO[1], 0, G + 900, 0.02, 1.2)
        pos = corpo_fim
        for k, (x, y) in enumerate(MUS_FECHAMENTO):
            dur = coloca(x, y, pos, dur_ms, 0.8 if k == 0 else 1.0, 1.0)
            pos += max(0, dur - 1.0) * 1000
        g_duck = (10 ** (-6 * duck / 20)).astype(np.float32)
        t10 = np.arange(N) / (SR / 100)
        M *= np.interp(t10, np.arange(len(g_duck)), g_duck).astype(np.float32)[:, None]
        VM = V + M
        del V, M
        info = {"alvo": alvo, "planos_com_ganho": decisoes, "compressor_max_db": round(red_max, 2), "blocos_musica": [(round(x, 2), round(y, 2)) for x, y in blocos], "nivel_musica_lufs": [round(float(x), 1) for x in nivel_mus]}
        np.save(cache, VM)
        json.dump(info, open(cache + ".json", "w"), ensure_ascii=False, indent=1)

    # ---------- recorte, efeitos, master ----------
    i0 = int((a.de or 0) * SR / 1000)
    i1 = int((a.ate or dur_ms) * SR / 1000)
    out = VM[i0:i1].copy()
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
        # limitador simples (pico amostral, com folga para o true peak): 4× sobreamostragem para medir
        teto = 10 ** (TETO_DBTP / 20)
        env = np.abs(signal.resample_poly(out.mean(axis=1), 4, 1)).reshape(-1, 4).max(axis=1)[: len(out)]
        env = np.maximum(env, np.abs(out).max(axis=1)[: len(env)])
        g = np.minimum(1.0, teto / np.maximum(env, 1e-9))
        k = int(0.005 * SR)
        g = -signal.convolve(-np.pad(g, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")  # suaviza
        g = np.minimum(g, np.minimum(1.0, teto / np.maximum(env, 1e-9)))
        out *= g.astype(np.float32)[:, None]
    sf.write(a.saida, out, SR, subtype="PCM_24")
    print(json.dumps({"saida": a.saida, "seg": round(len(out) / SR, 2), "lufs": round(medidor.integrated_loudness(out), 1), "pico_dbfs": round(float(20 * np.log10(np.abs(out).max() + 1e-9)), 1),
                      "alvo_fala": round(info["alvo"], 1), "planos_com_ganho": len(info["planos_com_ganho"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
