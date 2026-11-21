"""Faixa de música da REV5 (FINAL, vlog de Bruges; igual à da REV4 aprovada, agora sob as narrações gravadas), no relógio do vídeo final: uma faixa por seção (rev5/montar_rev5.py, FAIXA),
mesmas faixas da REV3; REV5: troca seca entre duas seções coladas (ver o corpo).
nas janelas de rev5/linha_do_tempo_rev5.json. REV3 (Diego, 21/11/2026: "músicas um pouco mais animadas"): faixas mais
animadas e cada seção começa no ponto da faixa em que ela já está cheia (INICIO, sem as introduções calmas).

Roda de reels/bruges-yt:  python -I rev5/musica_rev5.py  →  _tmp/musica_rev5.wav (48 kHz, estéreo) + rev5/musica_rev5.json

Regras (docs/VIDEO_LONGO_YOUTUBE.md, seção 3; pedidos do Diego de 20/11/2026):
  - corpo: cada seção usa UMA faixa, que continua de onde parou a cada janela (como no Bruxelas REV5); entra em 0,25 s
    e sai em 0,5 s dentro da janela; nível 3 dB abaixo da fala-alvo (−20 LUFS na prévia → −23 LUFS);
  - abertura (G): por baixo da narração, 9 dB abaixo da fala (−29 LUFS); quando a narração acaba, sobe para −23 LUFS e
    termina NO CORTE da compra do bilhete ("a música de abertura… finalize com essa filmagem"): o ponto de entrada na
    faixa é escolhido para uma batida forte cair exatamente no corte; depois do corte, 120 ms de saída;
  - fechamento (F): −29 LUFS sob a narração; na tela final (sem voz), −23 LUFS; sai nos últimos 3 s.
Ganho único por faixa (loudness integrado da faixa inteira, pyloudnorm). O Claude não escuta: a escuta é do Diego.
"""
import json
import os
import subprocess

import librosa
import numpy as np
import pyloudnorm as pyln
import soundfile as sf

SR = 48000
PASTA = "fonte/musica"
ALVO_PAISAGEM = -23.0
ALVO_SOB_VOZ = -29.0
ENTRA, SAI = 0.25, 0.5


def decodifica(nome):
    os.makedirs("_tmp/mus", exist_ok=True)
    wav = f"_tmp/mus/{nome}.wav"
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{PASTA}/{nome}.mp3", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", wav], check=True)
    x, sr = sf.read(wav, dtype="float32", always_2d=True)
    assert sr == SR
    return x


def ganho_para(x, alvo):
    lv = pyln.Meter(SR).integrated_loudness(x)
    return 10 ** ((alvo - lv) / 20), lv


def rampa(n, a, b):
    return np.linspace(a, b, max(n, 1), dtype=np.float32)


def entrada_no_corte(nome, dur_s, base=0.0, folga=2.5):
    """Ponto de entrada (s) na faixa, a partir de `base`, para uma batida forte cair em `dur_s` (o corte do gancho)."""
    y, sr = librosa.load(f"{PASTA}/{nome}.mp3", sr=22050, mono=True, duration=base + dur_s + folga + 5)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    _, beats = librosa.beat.beat_track(onset_envelope=onset, sr=sr)
    tb = librosa.frames_to_time(beats, sr=sr)
    cand = [(onset[b], t) for b, t in zip(beats, tb) if base + dur_s <= t <= base + dur_s + folga]
    if not cand:
        return base
    _, t = max(cand)
    return round(float(t - dur_s), 3)


def main():
    lt = json.load(open("rev5/linha_do_tempo_rev5.json", encoding="utf-8"))
    faixas = lt["faixas"]
    n = int(round(lt["duracao_ms"] / 1000 * SR))
    out = np.zeros((n, 2), dtype=np.float32)
    relatorio = {"faixas": {}, "janelas": []}
    cache = {}

    def faixa(sec):
        nome = faixas[sec]
        if nome not in cache:
            x = decodifica(nome)
            g, lv = ganho_para(x, ALVO_PAISAGEM)
            cache[nome] = (x, g, lv)
            relatorio["faixas"][sec] = {"faixa": nome, "lufs_faixa": round(lv, 1), "duracao_s": round(len(x) / SR, 1)}
        return cache[nome]

    # ---------- abertura ----------
    G = lt["gancho_ms"] / 1000
    x, g, _ = faixa("G")
    inicio = lt.get("inicio_faixa_s", {})
    o = entrada_no_corte(faixas["G"], G, base=inicio.get("G", 0.0))
    narr_fim = lt["narracao_fim_gancho_ms"] / 1000 + 0.3
    m = int(round(G * SR))
    pedaco = x[int(o * SR):int(o * SR) + m].copy() * g
    env = np.full(m, 10 ** ((ALVO_SOB_VOZ - ALVO_PAISAGEM) / 20), dtype=np.float32)
    # REV5: a G5 gravada acaba 0,4 s antes do corte; a subida começa 0,3 s depois da fala e é interrompida pelo corte
    i0, i1 = int(narr_fim * SR), int((narr_fim + 0.5) * SR)
    if i0 < m:
        env[i0:min(i1, m)] = rampa(i1 - i0, env[0], 1.0)[:min(i1, m) - i0]
        env[i1:] = 1.0
    env[: int(ENTRA * SR)] *= rampa(int(ENTRA * SR), 0, 1)
    # REV5: termina seco no corte (60 ms de saída antes dele), sem cauda: na REV3 os 120 ms depois do corte encostavam
    # no "Acabamos de chegar" da chegada
    env[m - int(0.06 * SR):] *= rampa(int(0.06 * SR), 1, 0)
    out[:m] += pedaco * env[:, None]
    relatorio["janelas"].append({"id": "G", "faixa": faixas["G"], "video_s": [0.0, round(G, 3)], "faixa_s": [o, round(o + G, 3)],
                                 "nota": f"entrada em {o:.2f} s da faixa: batida forte no corte do gancho; −29 LUFS sob a narração, −23 LUFS de {narr_fim:.1f} s ao corte; termina no corte"})

    # ---------- corpo ----------
    # REV5: onde uma seção termina exatamente onde outra começa (Minnewater → House of Waffles), a troca é seca no corte:
    # a faixa que sai some em 0,3 s até o corte e a que entra começa em 40 ms, sem as duas tocarem juntas (na REV3 a de
    # saída ainda estava saindo quando a outra entrava)
    corpo_j = [j for j in lt["musica"] if j["id"].startswith("M")]
    pos = {}
    for j in lt["musica"]:
        sec = j["id"]
        if not sec.startswith("M"):
            continue
        x, g, _ = faixa(sec)
        a, b = j["ini"] / 1000, j["fim"] / 1000
        m = int(round((b - a) * SR))
        p = pos.get(sec, inicio.get(sec, 0.0))
        if int(p * SR) + m > len(x):  # a faixa acabou: volta ao começo (não deve acontecer: todas são mais longas que a seção)
            p = 0.0
        pedaco = x[int(p * SR):int(p * SR) + m].copy() * g
        env = np.ones(m, dtype=np.float32)
        emenda_ini = any(o["id"] != sec and abs(o["fim"] - j["ini"]) <= 50 for o in corpo_j)
        emenda_fim = any(o["id"] != sec and abs(o["ini"] - j["fim"]) <= 50 for o in corpo_j)
        ne = min(int((0.04 if emenda_ini else ENTRA) * SR), m // 3)
        ns = min(int((0.3 if emenda_fim else SAI) * SR), m // 3)
        env[:ne] = rampa(ne, 0, 1)
        env[m - ns:] = rampa(ns, 1, 0)
        o0 = int(round(a * SR))
        out[o0:o0 + m] += pedaco * env[:, None]
        relatorio["janelas"].append({"id": sec, "faixa": faixas[sec], "video_s": [round(a, 3), round(b, 3)], "faixa_s": [round(p, 3), round(p + (b - a), 3)]})
        pos[sec] = p + (b - a)

    # ---------- fechamento + tela final ----------
    x, g, _ = faixa("F")
    B = lt["corpo_fim_ms"] / 1000
    D = lt["duracao_ms"] / 1000
    nf = lt["fechamento_narr_fim_ms"] / 1000 + 0.3
    m = int(round((D - B) * SR))
    oF = inicio.get("F", 0.0)
    pedaco = x[int(oF * SR):int(oF * SR) + m].copy() * g
    env = np.full(m, 10 ** ((ALVO_SOB_VOZ - ALVO_PAISAGEM) / 20), dtype=np.float32)
    i0, i1 = int((nf - B) * SR), int((nf - B + 0.8) * SR)
    env[i0:i1] = rampa(i1 - i0, env[0], 1.0)
    env[i1:] = 1.0
    env[: int(0.8 * SR)] *= rampa(int(0.8 * SR), 0, 1)
    env[m - 3 * SR:] *= rampa(3 * SR, 1, 0)
    o0 = int(round(B * SR))
    out[o0:o0 + m] += pedaco * env[:, None]
    relatorio["janelas"].append({"id": "F", "faixa": faixas["F"], "video_s": [round(B, 3), round(D, 3)], "faixa_s": [oF, round(oF + D - B, 3)],
                                 "nota": f"−29 LUFS sob a narração (até {nf:.1f} s), −23 LUFS na tela final, sai nos últimos 3 s"})

    sf.write("_tmp/musica_rev5.wav", out, SR, subtype="FLOAT")
    json.dump(relatorio, open("rev5/musica_rev5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for jn in relatorio["janelas"]:
        print(f"{jn['id']:>2}  vídeo {jn['video_s'][0]:7.2f}–{jn['video_s'][1]:7.2f}  faixa {jn['faixa_s'][0]:6.2f}–{jn['faixa_s'][1]:6.2f}  {jn['faixa']}")


if __name__ == "__main__":
    main()
