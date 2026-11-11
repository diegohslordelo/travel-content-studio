"""Trailer de 45 s do vlog de Bruxelas para Reel de teste (pedido do Diego, 11/11/2026): uma versão vertical (1080 × 1920)
e uma horizontal (1920 × 1080), com o MESMO corte, a mesma voz e as mesmas legendas (só muda o enquadramento).

Base: o gancho do vlog aprovado pelo Diego (REV3, 0–24,3 s: G1, cachorro, G2, ovos de € 26, "não tem condições"),
3 reações reais do corpo (waffle, Manneken Pis, 1ª cerveja belga) e o começo da G3 ("Eu anotei cada euro… e se
realmente vale a pena"), cortada no silêncio antes do "então fique com a gente". Fecha no CTA do DS V2
(`VÍDEO COMPLETO NO YOUTUBE →`, DS V2 2.7), o único elemento da marca no Reel (CLAUDE.md, 6).

Lê de ../bru-yt (fonte 4K, transcrição, linha do tempo e a voz tratada da REV3 em _tmp/vm_rev3.npz) e escreve em
rev1/_tmp (fora do git): base_v.mp4, base_h.mp4, voz e mix. Props das 2 versões em rev1/props_{v,h}.json.

Uso (de reels/bru-trailer):  python3 -I rev1/montar_trailer.py [--sem-video]
"""
import argparse
import importlib.util
import json
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

YT = "../bru-yt"
TMP = "rev1/_tmp"
SR = 48000
FPS = 30

spec = importlib.util.spec_from_file_location("mixar_rev3", f"{YT}/rev3/mixar_rev3.py")
mx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mx)

# (fonte s, quadros, centro do recorte vertical em fração da largura, de onde vem a voz)
# voz: ("vlog", ms) = a voz tratada da REV3 a partir desse ms do vlog; o gancho (1–8) e a G3 (12–14) vêm em bloco.
PLANOS = [
    (108.40, 90, 0.30),   # Atomium (G1)
    (294.25, 72, 0.50),   # fachada da Grand Place (G1)
    (134.75, 141, 0.42),  # Zinneke Pis: "Ponto turístico de Bruxelas. Um cachorro mijando."
    (181.05, 60, 0.45),   # sanduíche de batata frita (G2)
    (331.40, 60, 0.50),   # waffle (G2)
    (426.42, 100, 0.55),  # ovos de chocolate na vitrine (G2 + "seis ovos de")
    (448.35, 144, 0.43),  # "páscoa, menores que meu dedo, estão a 26 euros pela vitrine."
    (454.72, 62, 0.46),   # "Não tem condições"
    (356.62, 61, 0.46),   # waffle: "bom, extremamente aprovado" (61 quadros: termina antes da fala seguinte)
    (482.05, 96, 0.50),   # Manneken Pis: "O que será? O que será? O menino fazendo xixi"
    (656.74, 78, 0.56),   # Brasserie: "a minha primeira cerveja belga, na Bélgica."
    (217.94, 132, 0.50),  # Grand Place de dia (G3)
    (528.25, 84, 0.50),   # Manneken Pis, a estátua (G3)
    (862.25, 150, 0.50),  # Grand Place à noite (fim da G3 + CTA)
]
GRUPOS = [
    (None, 11, None),  # "Será que vale a pena passar um dia inteiro em Bruxelas?" = texto do gancho
    ("E quanto será", 3, None), ("que custa isso?", 3, "custa"),
    ("Ponto turístico", 2, None), ("de Bruxelas.", 2, "Bruxelas."), ("Um cachorro mijando.", 3, "cachorro"),
    ("Bom, teve", 2, None), ("batata frita,", 2, "batata"), ("waffle, chocolate", 2, "chocolate"),
    ("e alguns", 2, None), ("que a gente não teve", 5, None), ("nem coragem", 2, "coragem"), ("de chegar perto.", 3, None),
    ("seis ovos de páscoa,", 4, "seis"), ("menores que meu dedo,", 4, "dedo,"), ("estão a 26 euros", 4, "26"), ("pela vitrine.", 2, None),
    ("Não tem condições", 3, "condições"),
    ("Bom,", 1, None), ("extremamente aprovado", 2, "aprovado"), (None, 1, None),
    ("O que será? O que será?", 6, None), ("O menino fazendo xixi", 4, "xixi"),
    ("a minha primeira", 3, None), ("cerveja belga,", 2, "cerveja"), ("na Bélgica.", 2, None),
    ("Eu anotei cada euro", 4, "euro"), ("que a gente gastou", 4, None), ("nesse nosso rolê", 3, None), ("em Bruxelas.", 2, "Bruxelas."),
    ("No final do vídeo", 4, None), ("você vai ver", 3, None), ("quanto custou tudo", 3, "custou"),
    ("e se realmente", 3, None), ("vale a pena.", 3, "vale"),
]
G3_FIM_ARQ = 8.10  # s no N12: silêncio entre "pena" (termina 7,96) e "então" (começa 8,52), medido na energia
FALA_EXTRA = [(356.62, 61), (482.05, 96), (656.74, 78)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-video", action="store_true")
    a = ap.parse_args()
    os.makedirs(TMP, exist_ok=True)
    lt = json.load(open(f"{YT}/rev3/linha_do_tempo_rev3.json", encoding="utf-8"))
    tr = json.load(open(f"{YT}/_tmp/transcricao.json", encoding="utf-8"))
    narr = json.load(open(f"{YT}/_tmp/narr/transcricao_narracoes.json", encoding="utf-8"))
    info = json.load(open(f"{YT}/_tmp/vm_rev3.npz.json"))
    alvo = info["alvo"]
    G = lt["gancho_ms"]
    manter, fps_lt = lt["manter"], lt["fps"]
    ini_src = [x / fps_lt for x, _ in manter]
    acc, ini_out = 0, []
    for x, y in manter:
        ini_out.append(acc)
        acc += y - x

    def vlog_ms(ts):  # fonte (s) → ms no vlog (corpo decupado)
        i = max(0, np.searchsorted(ini_src, ts, side="right") - 1)
        x, y = manter[i]
        q = ts * fps_lt
        assert x <= q < y, ts
        return G + (ini_out[i] + q - x) * 1000 / fps_lt

    q_ini = np.cumsum([0] + [p[1] for p in PLANOS])
    n_q = int(q_ini[-1])
    dur = n_q / FPS
    N = int(round(dur * SR))
    t_bloco_b = q_ini[11] / FPS  # onde a G3 começa no trailer (= 24,3 s + extras)
    desl_b = t_bloco_b - 24.3

    # ---------- voz (a da REV3, já tratada) ----------
    z = np.load(f"{YT}/_tmp/vm_rev3.npz", mmap_mode="r")
    Vv = z["V"]
    fala_v = np.load(f"{YT}/_tmp/fala_rev3.npy")
    V = np.zeros((N, 2), np.float32)
    fala = np.zeros(int(dur * 100) + 1)
    fade = int(0.008 * SR)

    def cola(t_out, vlog_de_ms, seg_s, fade_fim=0.008):
        o0, s0, n = int(round(t_out * SR)), int(round(vlog_de_ms * SR / 1000)), int(round(seg_s * SR))
        n = min(n, N - o0)
        ped = np.asarray(Vv[s0:s0 + n], np.float32).copy()
        r = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
        ped[:fade] *= r
        ff = int(fade_fim * SR)
        ped[-ff:] *= np.linspace(1, 0, ff, dtype=np.float32)[:, None]
        V[o0:o0 + n] += ped
        f0 = int(vlog_de_ms / 10)
        fala[int(t_out * 100):int(t_out * 100) + int(seg_s * 100)] = fala_v[f0:f0 + int(seg_s * 100)][: len(fala) - int(t_out * 100)]

    cola(0.0, 0.0, 24.3)
    for (src, q), qi in zip(FALA_EXTRA, q_ini[8:11]):
        cola(qi / FPS, vlog_ms(src), q / FPS)
    g3 = next(n_ for n_ in lt["narracoes"] if n_["id"] == "G3")
    g3_fim_vlog = g3["fala_ini"] / 1000 + (G3_FIM_ARQ - g3["arq_ini_s"])
    cola(t_bloco_b, 24300.0, g3_fim_vlog - 24.3, fade_fim=0.06)
    fim_voz = t_bloco_b + g3_fim_vlog - 24.3

    # ---------- música: a mesma faixa do gancho do vlog (B → A), nivelada e abaixada sob a voz (6/15 dB) ----------
    mus = np.load(f"{YT}/_tmp/musica_stem.npy", mmap_mode="r")
    M, emendas = mx.costura(mus, [mx.TRECHO_B, mx.TRECHO_A], dur + 0.5)
    M = np.asarray(M[:N], np.float32).copy()
    medidor = pyln.Meter(SR)
    M *= np.float32(10 ** ((alvo - 6.0 - medidor.integrated_loudness(M)) / 20))
    mono = M.mean(axis=1)
    J = SR // 100
    m_ = len(mono) // J
    e10 = 10 * np.log10(np.convolve((mono[: m_ * J].reshape(m_, J) ** 2).mean(axis=1), np.ones(300) / 300, mode="same") + 1e-12)
    vivo = e10 > e10.max() - 30
    gdb = np.where(vivo, np.clip(np.median(e10[vivo]) - e10, -12, 4), 0)
    gdb = np.convolve(gdb, np.ones(150) / 150, mode="same")
    M *= (10 ** (np.interp(np.arange(N) / J, np.arange(m_), gdb) / 20)).astype(np.float32)[:, None]
    idx = np.flatnonzero(fala)
    for x, y in zip(idx, idx[1:]):
        if 1 < y - x <= 80:
            fala[x:y] = 1
    duck = mx.suaviza(fala, 500, 500)
    M *= np.interp(np.arange(N) / (SR / 100), np.arange(len(duck)), 10 ** (-9.0 * duck / 20)).astype(np.float32)[:, None]
    fi, fo = int(0.02 * SR), int(1.5 * SR)
    M[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)[:, None]
    M[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]

    # ---------- CTA: placa com Chegada e clack (o único som do DS, −6 dB da voz: REFERENCIA_EDICAO_FORMATOS 4.1) ----------
    cta_ms = round((fim_voz + 0.25) * 1000)
    clack, srx = sf.read("../../design-system/sons/PD_clack_v1.wav", dtype="float32")
    assert srx == SR
    if clack.ndim == 1:
        clack = np.column_stack([clack, clack])
    pico = 20 * np.log10(np.abs(clack).max() + 1e-9)
    try:
        lv_c = medidor.integrated_loudness(np.concatenate([clack, np.zeros((SR, 2), np.float32)]))
    except ValueError:
        lv_c = pico - 12
    clack *= np.float32(10 ** ((alvo - 6.0 - lv_c) / 20))
    o0 = int((cta_ms + 280) * SR / 1000)  # a placa assenta aos 280 ms da Chegada
    n = min(len(clack), N - o0)
    S = np.zeros_like(V)
    S[o0:o0 + n] += clack[:n]

    # ---------- master −14 LUFS, limitador −2 dBTP (a correção pós-AAC é a de ../bru-yt/rev3/corrigir_pico_aac.py) ----------
    sf.write(f"{TMP}/voz.wav", V, SR, subtype="PCM_24")
    out = V + M + S
    lv = medidor.integrated_loudness(out)
    out *= np.float32(10 ** ((-14 - lv) / 20))
    teto = 10 ** (-2.0 / 20)
    env = np.abs(signal.resample_poly(out.mean(axis=1), 4, 1)).reshape(-1, 4).max(axis=1)[: len(out)]
    env = np.maximum(env, np.abs(out).max(axis=1)[: len(env)])
    g = np.minimum(1.0, teto / np.maximum(env, 1e-9))
    k = int(0.005 * SR)
    g = -signal.convolve(-np.pad(g, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
    g = np.minimum(g, np.minimum(1.0, teto / np.maximum(env, 1e-9)))
    out *= g.astype(np.float32)[:, None]
    sf.write(f"{TMP}/mix.wav", out, SR, subtype="PCM_24")

    # ---------- legendas: palavras com tempo (transcrição da fonte e das narrações) no tempo do trailer ----------
    palavras = []

    def de_fonte(src, de_s, ate_s, t_out):
        for s_ in tr["segmentos"]:
            for w in s_["palavras"]:
                if de_s - 0.02 <= w["ini"] < ate_s - 0.12:
                    palavras.append({"p": w["p"], "ini": t_out + w["ini"] - de_s, "fim": t_out + min(w["fim"], ate_s) - de_s})

    def de_narr(n_id, arq_ini, arq_fim, t_fala):
        for w in narr[n_id]:
            if arq_ini - 0.05 <= max(w["ini"], arq_ini) < arq_fim and w["fim"] <= arq_fim + 0.3:
                palavras.append({"p": w["p"], "ini": t_fala + max(w["ini"], arq_ini) - arq_ini, "fim": t_fala + w["fim"] - arq_ini})

    n_ = {x["id"]: x for x in lt["narracoes"]}
    de_narr("N10", n_["G1"]["arq_ini_s"], n_["G1"]["arq_fim_s"], n_["G1"]["fala_ini"] / 1000)
    de_fonte(134.75, 134.75, 139.45, 5.4)
    de_narr("N11", n_["G2"]["arq_ini_s"], n_["G2"]["arq_fim_s"], n_["G2"]["fala_ini"] / 1000)
    for p in lt["audio"]:
        if p["tipo"] == "gancho_fala" and p["out"] >= 16000:
            de_fonte(p["src"], p["src"], p["src"] + p["dur"] / 1000, p["out"] / 1000)
    for (src, q), qi in zip(FALA_EXTRA, q_ini[8:11]):
        de_fonte(src, src, src + q / FPS, qi / FPS)
    de_narr("N12", n_["G3"]["arq_ini_s"], G3_FIM_ARQ, n_["G3"]["fala_ini"] / 1000 + desl_b)
    palavras.sort(key=lambda w: w["ini"])
    json.dump(palavras, open(f"{TMP}/palavras.json", "w"), ensure_ascii=False, indent=0)

    # grupos de 1 a 4 palavras (até ~24 caracteres, 1 linha), na ordem da fala; o nº diz quantas palavras o grupo
    # consome. None = palavras que não entram (o gancho vira o texto grande; o "E" do waffle é só ruído da rua).
    grupos = []
    k = 0
    for texto, n_p, dest in GRUPOS:
        ws = palavras[k:k + n_p]
        k += n_p
        if texto is None:
            continue
        grupos.append({"texto": texto, "destaque": dest, "ini": round(ws[0]["ini"] * 1000), "fim_fala": round(ws[-1]["fim"] * 1000),
                       "confere": " ".join(w["p"] for w in ws)})
    assert k == len(palavras), (k, len(palavras))
    for g_, prox in zip(grupos, grupos[1:] + [None]):
        lim = prox["ini"] if prox else round(fim_voz * 1000) + 300
        g_["fim"] = min(lim, g_["fim_fala"] + 400) if prox is None or prox["ini"] - g_["fim_fala"] > 400 else prox["ini"]
    gancho = [{"texto": "SERÁ QUE VALE", "em": round(palavras[0]["ini"] * 1000), "tam": 1},
              {"texto": "A PENA PASSAR", "em": round(palavras[3]["ini"] * 1000), "tam": 1},
              {"texto": "1 DIA INTEIRO", "em": round(palavras[6]["ini"] * 1000), "tam": 1},
              {"texto": "EM BRUXELAS?", "em": round(palavras[9]["ini"] * 1000), "tam": 2}]
    for o, (w, h) in {"v": (1080, 1920), "h": (1920, 1080)}.items():
        json.dump({"layout": o, "largura": w, "altura": h, "video": "base.mp4", "duracao": round(dur * 1000), "fps": FPS, "gancho": gancho, "ganchoFim": 3000,
                   "legendas": grupos, "cta": {"rotulo": "VÍDEO COMPLETO", "destino": "NO YOUTUBE", "entrada": cta_ms}},
                  open(f"rev1/props_{o}.json", "w"), ensure_ascii=False, indent=1)

    props_base = {"duracao": round(dur * 1000), "fps": FPS, "fimVoz": round(fim_voz * 1000), "cta": cta_ms,
                  "cortes": [round(q / FPS * 1000) for q in q_ini[:-1]]}
    json.dump({"planos": [{"fonte": p[0], "quadros": p[1], "entra_ms": round(q / FPS * 1000)} for p, q in zip(PLANOS, q_ini)], **props_base,
               "musica_emendas": emendas, "voz_alvo_lufs": round(alvo, 1)}, open(f"{TMP}/linha.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"seg": round(dur, 3), "quadros": n_q, "fim_voz": round(fim_voz, 2), "cta_ms": cta_ms, "lufs": round(medidor.integrated_loudness(out), 1),
                      "emendas_musica": emendas}, ensure_ascii=False))

    # ---------- imagem: cortes da fonte 4K (vertical: recorte 1215 × 2160 → 1080 × 1920; horizontal: 1920 × 1080) ----------
    if a.sem_video:
        return
    for o in ("v", "h"):
        partes = []
        for i, (src, q, cx) in enumerate(PLANOS):
            arq = f"{TMP}/p_{o}_{i:02d}.mp4"
            if o == "v":
                x0 = int(np.clip(cx * 3840 - 1215 / 2, 0, 3840 - 1215)) // 2 * 2
                vf = f"crop=1216:2160:{x0}:0,scale=1080:1920:flags=lanczos,format=yuv420p"
            else:
                vf = "scale=1920:1080:flags=lanczos,format=yuv420p"
            if not os.path.exists(arq):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src:.3f}", "-i", f"{YT}/fonte/1103_fala.mp4", "-frames:v", str(q), "-vf", vf, "-r", str(FPS),
                                "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-g", "30", arq], check=True)
            partes.append(arq)
        with open(f"{TMP}/lista_{o}.txt", "w") as f:
            f.writelines(f"file '{os.path.basename(x)}'\n" for x in partes)
        os.makedirs(f"{TMP}/publico_{o}", exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/lista_{o}.txt", "-c", "copy", "-movflags", "+faststart",
                        f"{TMP}/publico_{o}/base.mp4"], check=True)


if __name__ == "__main__":
    main()
