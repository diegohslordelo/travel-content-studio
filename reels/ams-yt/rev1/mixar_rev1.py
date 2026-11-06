"""Mixagem da REV1 (docs/AUDIO_REVIEW_STANDARD.md; DS V2 4.6): voz decupada e tratada + música do Diego com ducking
+ efeitos sonoros, master em −14 LUFS integrados e pico verdadeiro ≤ −1 dBTP (medidos no arquivo exportado).

Cadeia (sempre a partir do original, R2):
  1. Voz: passa-altas 80 Hz, 2 polos [PRECEDENTE REV6]; 110 Hz só nos blocos com vento (grave ≥ −4 dB contra a
     faixa da voz no diagnóstico). Ganho por bloco (plano) para levar a fala à mediana dos blocos (−21,2 LUFS),
     limitado a ±5 dB e só quando a diferença passa de 1,5 dB, com rampas de 200 ms. Sem redução de ruído e sem
     compressor (o ruído é de rua, variável: T3 para redução; a dinâmica da fala é natural).
  2. Cortes: 8 ms de fade em cada emenda que não é contínua na fonte.
  3. Gancho: falas reais em 0 dB; os outros clipes com o som real 14 dB abaixo (cama para a narração).
     Fechamento: som real 12 dB abaixo, música por baixo da narração.
  4. Música (a do Diego, `1016(1).mp4`): cada bloco toca contínuo a partir do início mapeado e termina com fade de
     600 ms onde o trecho de imagem acaba. Nível: 3 dB abaixo da fala sem fala; 9 dB abaixo com fala [PROJETO 8–10 dB],
     transição de 500 ms e pausas de até 0,8 s seguram o ducking.
  5. Efeitos: os do Remotion (gerados para voz em −16 LUFS) recebem a diferença para a voz desta mixagem; rufar −8 dB
     e fogos −6 dB da voz (provisórios, calibrar na escuta).
  6. Master: ganho único para −14,0 LUFS e limitador (pico ≤ −1,5 dBFS antes do AAC; conferido em dBTP no exportado).

Uso (de reels/ams-yt):
  python rev1/mixar_rev1.py --sfx _tmp/sfx.wav --saida _tmp/mix.wav [--de MS --ate MS]
"""
import argparse
import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000
ALVO_FALA = None  # mediana dos blocos, lida do diagnóstico
sys.path.insert(0, "rev1")
import montar_rev1 as mt  # noqa: E402


def env_interp(ms_pts, db_pts, n):
    """Curva de ganho (linear) por amostra a partir de pontos (ms, dB)."""
    t = np.arange(n, dtype=np.float64) * 1000 / SR
    return (10 ** (np.interp(t, ms_pts, db_pts) / 20)).astype(np.float32)


def suaviza(v, ms_subida, ms_descida, passo_ms=10):
    """Envelope 0..1 em passos de 10 ms com subida/descida lineares."""
    out = np.zeros_like(v, dtype=np.float64)
    up, dn = passo_ms / ms_subida, passo_ms / ms_descida
    a = 0.0
    for i, x in enumerate(v):
        a = min(x, a + up) if x > a else max(x, a - dn)
        out[i] = a
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sfx", default=None, help="áudio do render do Remotion (só efeitos)")
    ap.add_argument("--sfx-inicio", type=float, default=0.0, help="ms do vídeo final em que o áudio de --sfx começa")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--de", type=float, default=None)
    ap.add_argument("--ate", type=float, default=None)
    ap.add_argument("--cache", action="store_true", help="reaproveita voz + música já montadas (_tmp/vm_rev1.npy)")
    a = ap.parse_args()

    lt = json.load(open("rev1/linha_do_tempo_rev1.json", encoding="utf-8"))
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))
    diag = json.load(open("_tmp/diag_rev1.json"))
    voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32")
    mus, _ = sf.read("_tmp/musica_orig.wav", dtype="float32")
    assert sr == SR
    n_src = len(voz)
    dur_ms = lt["duracao_ms"]
    N = int(round(dur_ms * SR / 1000))

    cache = "_tmp/vm_rev1.npy"
    if a.cache and os.path.exists(cache):
        VM = np.load(cache)
        info = json.load(open(cache + ".json"))
        alvo, decisoes, blocos, nivel_mus, comp_stats = info["alvo"], info["decisoes"], info["blocos"], info["nivel_mus"], info["comp_stats"]
        medidor = pyln.Meter(SR)
    else:
        # ---------- 1. voz tratada, ainda no tempo da fonte ----------
        falas = [b for b in diag if b["tipo"].startswith("F") and b["lufs_fala"] == b["lufs_fala"]]
        alvo = float(np.median([b["lufs_fala"] for b in falas]))
        pts_ms, pts_db = [], []
        vento = np.zeros(n_src, bool)
        decisoes = []
        for b in diag:
            g = 0.0
            if b in falas and abs(alvo - b["lufs_fala"]) > 1.5:
                g = float(np.clip(alvo - b["lufs_fala"], -5, 5))
            pts_ms += [b["ini"] * 1000 + 100, b["fim"] * 1000 - 100]
            pts_db += [g, g]
            if b in falas and b["grave_db"] >= -4:
                vento[int(b["ini"] * SR):int(b["fim"] * SR)] = True
            if g or (b in falas and b["grave_db"] >= -4):
                decisoes.append({"bloco": b["bloco"], "ini": b["ini"], "fim": b["fim"], "ganho_db": round(g, 1), "passa_altas_hz": 110 if b in falas and b["grave_db"] >= -4 else 80})
        ganho = env_interp(pts_ms, pts_db, n_src)
        hp80 = signal.butter(2, 80, btype="highpass", fs=SR, output="sos")
        hp110 = signal.butter(2, 110, btype="highpass", fs=SR, output="sos")
        v80 = signal.sosfiltfilt(hp80, voz, axis=0).astype(np.float32)
        v110 = signal.sosfiltfilt(hp110, voz, axis=0).astype(np.float32)
        mix_v = np.convolve(vento.astype(np.float32), np.ones(SR // 5, np.float32) / (SR // 5), mode="same")[:, None]  # rampa de 200 ms
        voz_t = (v80 * (1 - mix_v) + v110 * mix_v) * ganho[:, None]
        del v80, v110, mix_v
        # compressor leve [PRECEDENTE REV6]: 2:1, joelho 4 dB, ataque 20 ms, liberação 150 ms, no máximo 3 dB, limiar
        # 8 dB acima do nível-alvo da fala (só as sílabas mais fortes e os golpes de vento/manuseio)
        Bc = SR // 1000
        nb = len(voz_t) // Bc
        rms = np.sqrt(np.mean(voz_t[: nb * Bc].reshape(nb, Bc, 2) ** 2, axis=(1, 2)))
        rms10 = np.sqrt(np.convolve(rms ** 2, np.ones(10) / 10, mode="same"))
        lv = 20 * np.log10(rms10 + 1e-9)
        thr, joelho = alvo + 8, 4.0
        exc = lv - thr
        red = np.where(exc <= -joelho / 2, 0, np.where(exc >= joelho / 2, exc / 2, (exc + joelho / 2) ** 2 / (4 * joelho)))
        red = np.minimum(red, 3.0)
        sm = np.zeros_like(red)
        at, rl = np.exp(-1 / 20), np.exp(-1 / 150)
        for i in range(1, len(red)):
            c = at if red[i] > sm[i - 1] else rl
            sm[i] = c * sm[i - 1] + (1 - c) * red[i]
        comp_stats = {"compressor_reducao_max_db": round(float(sm.max()), 2), "compressor_acima_1db_pct": round(float(np.mean(sm > 1) * 100), 2)}
        voz_t *= (10 ** (-np.interp(np.arange(len(voz_t)) / Bc, np.arange(nb), sm) / 20)).astype(np.float32)[:, None]

        # ---------- 2/3. monta a voz no tempo do vídeo ----------
        V = np.zeros((N, 2), np.float32)
        fade = int(0.008 * SR)
        anterior_fim = None
        for p in lt["audio"]:
            s0 = int(round(p["src"] * SR))
            o0 = int(round(p["out"] * SR / 1000))
            n = int(round(p["dur"] * SR / 1000))
            n = min(n, n_src - s0, N - o0)
            if n <= 0:
                continue
            pedaco = voz_t[s0:s0 + n].copy()
            g = {"gancho_fala": 1.0, "gancho_baixo": 10 ** (-14 / 20), "fechamento": 10 ** (-12 / 20)}.get(p["tipo"], 1.0)
            pedaco *= g
            continuo = anterior_fim is not None and abs(anterior_fim - s0) <= 2 and p["tipo"] == "corpo"
            if not continuo:
                r = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                pedaco[:fade] *= r
                if o0 > 0:
                    V[o0 - fade:o0] *= r[::-1]
            V[o0:o0 + n] += pedaco
            anterior_fim = s0 + n
        del voz_t

        # ---------- atividade de fala no tempo do vídeo (10 ms) ----------
        m10 = int(dur_ms / 10) + 1
        fala = np.zeros(m10)
        mp = mt.Mapa(edl, lt["gancho_ms"])
        tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
        for s_ in tr["segmentos"]:
            for w in s_["palavras"]:
                i0 = mp.ms(w["ini"])
                i1 = mp.ms(w["fim"])
                if i1 > i0 and i1 - i0 < 3000:
                    fala[int(i0 / 10):int(i1 / 10) + 1] = 1
        for p in lt["audio"]:
            if p["tipo"] == "gancho_fala":
                fala[int(p["out"] / 10):int((p["out"] + p["dur"]) / 10)] = 1
        for ini, fim, _t in lt["narracao_gancho"] + lt["narracao_fechamento"]:
            fala[int(ini / 10):int(fim / 10)] = 1
        # segura pausas curtas (≤ 0,8 s)
        idx = np.flatnonzero(fala)
        for x, y in zip(idx, idx[1:]):
            if 1 < y - x <= 80:
                fala[x:y] = 1
        duck = suaviza(fala, 500, 500)  # 0 = sem fala, 1 = com fala

        # ---------- 4. música ----------
        mm = np.sqrt(np.mean(mus.mean(axis=1)[: n_src // 480 * 480].reshape(-1, 480) ** 2, axis=1))
        tem = 20 * np.log10(mm + 1e-9) > -50
        blocos = []
        i = 0
        while i < len(tem):
            if tem[i]:
                j = i
                while j < len(tem) and (tem[j] or (j + 100 < len(tem) and tem[j:j + 100].any())):
                    j += 1
                blocos.append((i / 100, j / 100))
                i = j
            else:
                i += 1
        M = np.zeros((N, 2), np.float32)
        medidor = pyln.Meter(SR)
        nivel_mus = []

        def coloca(src_a, src_b, out_a, out_fim, fade_in=0.15, fade_out=0.6):
            n = int(min((src_b - src_a) * SR, (out_fim - out_a) * SR / 1000, n_src - src_a * SR))
            s0, o0 = int(src_a * SR), int(out_a * SR / 1000)
            n = min(n, N - o0)
            if n <= SR // 10:
                return
            seg = mus[s0:s0 + n].copy()
            try:
                l = medidor.integrated_loudness(seg)
            except Exception:
                l = -40
            nivel_mus.append(l)
            g = 10 ** ((alvo - 3 - l) / 20)  # sem fala: 3 dB abaixo da fala
            fi, fo = int(fade_in * SR), int(fade_out * SR)
            seg *= g
            seg[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
            seg[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            M[o0:o0 + n] += seg

        corpo_fim = lt["corpo_fim_ms"]
        for b0, b1 in blocos:
            out_a = mp.ms(b0)
            out_b = mp.ms(b1)
            coloca(b0, b1, out_a, min(out_b, corpo_fim))
        # fechamento + tela final (provisório: a música da tela final é escolha do Diego)
        f0 = corpo_fim
        coloca(1902.0, 1923.5, f0, f0 + 21500, 0.4, 1.5)
        coloca(1788.5, 1827.0, f0 + 20000, dur_ms, 1.5, 3.0)
        # ducking: com fala, mais 6 dB abaixo (total 9 dB abaixo da fala)
        g_duck = (10 ** (-6 * duck / 20)).astype(np.float32)
        t10 = np.arange(N) / (SR / 100)
        M *= np.interp(t10, np.arange(len(g_duck)), g_duck).astype(np.float32)[:, None]

        VM = V + M
        del V, M
        np.save(cache, VM)
        json.dump({"alvo": alvo, "decisoes": decisoes, "blocos": blocos, "nivel_mus": [float(x) for x in nivel_mus], "comp_stats": comp_stats}, open(cache + ".json", "w"))

    # ---------- 5. efeitos ----------
    S = np.zeros((N, 2), np.float32)
    if a.sfx:
        sfx, srx = sf.read(a.sfx, dtype="float32")
        if srx != SR:
            sfx = signal.resample_poly(sfx, SR, srx, axis=0).astype(np.float32)
        if sfx.ndim == 1:
            sfx = np.column_stack([sfx, sfx])
        o0 = int(a.sfx_inicio * SR / 1000)
        n = min(len(sfx), N - o0)
        S[o0:o0 + n] += sfx[:n] * 10 ** ((alvo - (-16)) / 20)
    for nome, rel, em in [("AMS_tambor_v1.wav", -8, None), ("AMS_fogos_murchos_v1.wav", -6, None)]:
        info = json.load(open("sons/sons_ams.json", encoding="utf-8"))[nome]
        x, _ = sf.read(f"sons/{nome}", dtype="float32")
        ev = [e for e in lt["sons"] if e["arquivo"] == nome][0]
        o0 = int(ev["em"] * SR / 1000)
        n = min(len(x), N - o0)
        S[o0:o0 + n] += (x[:n] * 10 ** ((alvo + rel - info["lufs_50ms"]) / 20))[:, None]

    # ---------- 6. master ----------
    T = VM + S
    del VM, S
    from scipy.ndimage import minimum_filter1d

    B = SR // 1000  # blocos de 1 ms

    def picos_reais(x):
        """Pico verdadeiro por bloco de 1 ms (sobreamostragem 4×, em pedaços de 10 s)."""
        nb = len(x) // B + 1
        out = np.zeros(nb, np.float32)
        passo = SR * 10
        for c0 in range(0, len(x), passo):
            c1 = min(len(x), c0 + passo)
            m0, m1 = max(0, c0 - 64), min(len(x), c1 + 64)
            up = np.abs(signal.resample_poly(x[m0:m1], 4, 1, axis=0)).max(axis=1)
            up = up[(c0 - m0) * 4:(c0 - m0) * 4 + (c1 - c0) * 4]
            nbl = (c1 - c0 + B - 1) // B
            pad = np.zeros(nbl * B * 4, np.float32)
            pad[: len(up)] = up
            out[c0 // B:c0 // B + nbl] = pad.reshape(nbl, B * 4).max(axis=1)
        return out

    def limita(x, teto_db):
        teto = 10 ** (teto_db / 20)
        pico = picos_reais(x)
        need = np.minimum(1.0, teto / np.maximum(pico, 1e-9))
        g = minimum_filter1d(need, size=11)  # antecipação de 5 ms
        rel = np.exp(-1 / 80)  # liberação de 80 ms
        for i in range(1, len(g)):
            if g[i] > g[i - 1]:
                g[i] = g[i - 1] * rel + (1 - rel) * g[i]
        g = minimum_filter1d(g, size=3)  # a interpolação entre blocos não deixa passar pico
        x *= np.interp(np.arange(len(x)) / B, np.arange(len(g)), g).astype(np.float32)[:, None]
        gdb = 20 * np.log10(g + 1e-9)
        estat["acima_1db_pct"] = round(float(np.mean(gdb < -1) * 100), 2)
        estat["acima_3db_pct"] = round(float(np.mean(gdb < -3) * 100), 3)
        estat["acima_6db_pct"] = round(float(np.mean(gdb < -6) * 100), 3)
        pior = np.argsort(gdb)[:4000]
        vistos = []
        for i in pior:
            if all(abs(i - v) > 2000 for v in vistos):
                vistos.append(int(i))
            if len(vistos) == 10:
                break
        estat["piores_ms"] = [(v, round(float(gdb[v]), 1)) for v in vistos]
        return 20 * np.log10(float(np.min(g)) + 1e-9)

    estat = {}
    l_int = medidor.integrated_loudness(T)
    g_master = -14.0 - l_int
    base = T.copy()
    for _ in range(3):  # o limitador baixa a loudness: corrige o ganho e limita de novo a partir da mesma mistura
        T = base * np.float32(10 ** (g_master / 20))
        reducao = limita(T, -1.6)
        l_fim = medidor.integrated_loudness(T)
        if abs(l_fim + 14.0) <= 0.15:
            break
        g_master += -14.0 - l_fim
    del base

    i0 = int((a.de or 0) * SR / 1000)
    i1 = int((a.ate or dur_ms) * SR / 1000)
    sf.write(a.saida, T[i0:i1], SR, subtype="FLOAT")
    rel_json = {"alvo_fala_lufs": round(alvo, 1), "integrado_antes_master": round(float(l_int), 2), "ganho_master_db": round(float(g_master), 2), "limitador_reducao_max_db": round(float(reducao), 2), "integrado_final": round(float(l_fim), 2), "limitador": estat, **comp_stats,
                "blocos_tratados": decisoes, "musica_blocos": [(round(x, 2), round(y, 2)) for x, y in blocos], "nivel_musica_lufs": [round(float(x), 1) for x in nivel_mus]}
    json.dump(rel_json, open(os.path.splitext(a.saida)[0] + "_mix.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in rel_json.items() if k not in ("blocos_tratados", "musica_blocos", "nivel_musica_lufs")}), f"blocos tratados {len(decisoes)}, música {len(blocos)} blocos")


if __name__ == "__main__":
    main()
