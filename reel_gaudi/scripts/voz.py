"""Voz do Reel: decupagem das 7 tomadas, restauro do fim de "visita.", redução leve de ruído e loudness.

Lê ../edicao.json e ../transcricao_alinhada.json. Gera, em _tmp/:
  voz_bruta.wav (48 kHz, mono) · trechos.json (onde cada pedaço do bruto cai no Reel) · palavras.json (palavras no tempo do Reel)
O vídeo do Diego é cortado com os mesmos trechos (reel.py), para a boca ficar em sincronia com a voz.
Sem voz sintética e sem IA: só a voz gravada do Diego, cortada no silêncio. O Claude não escuta áudio; tudo aqui é medido.
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

SR = 48000
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(AQUI, "_tmp")


def carregar_take(arq):
    """Trilha 0:a:0 (AAC) em mono; a 2ª trilha (áudio espacial APAC) não tem decodificador no ffmpeg."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def piso(x):
    """Ruído de fundo do take: percentil 5 do RMS em janelas de 10 ms (sem o silêncio digital)."""
    n = int(0.01 * SR)
    v = np.array([rms_db(x[i:i + n]) for i in range(0, len(x) - n, n)])
    return float(np.percentile(v[v > -90], 5))


EXTRAS = []  # outros takes (preenchido em montar): tom de sala quando o próprio take não tem pausa limpa


def tom_de_sala(x, dur=0.25):
    """Trecho mais quieto (sem o silêncio digital do começo) do take ou, se ele não tiver pausa limpa, de outro take,
    no nível do ruído de fundo do take: preenche respiro e o fim restaurado."""
    n, passo = int(dur * SR), int(0.01 * SR)
    melhor, trecho = 1e9, None
    for fonte in [x] + EXTRAS:
        for i in range(int(0.08 * SR), len(fonte) - n, passo):
            v = rms_db(fonte[i:i + n])
            if -90 < v < melhor:
                melhor, trecho = v, fonte[i:i + n]
        if fonte is x and melhor < piso(x) + 6:
            break  # o próprio take tem uma pausa limpa
    alvo = piso(x) + 3  # RMS de 250 ms de ruído fica ≈ 3 dB acima do percentil 5 de 10 ms
    return trecho * 10 ** ((min(alvo, melhor) - melhor) / 20)


def loop_tom(tom, n):
    """Repete o tom de sala com cruzamento de 30 ms até n amostras."""
    cf = int(0.03 * SR)
    out = tom.copy()
    while len(out) < n:
        emenda = out[-cf:] * np.linspace(1, 0, cf) + tom[:cf] * np.linspace(0, 1, cf)
        out = np.concatenate([out[:-cf], emenda, tom[cf:]])
    return out[:n]


def periodo(x):
    """Período fundamental (amostras) por autocorrelação, entre 70 e 300 Hz."""
    x = x - x.mean()
    c = np.correlate(x, x, "full")[len(x) - 1:]
    lo, hi = SR // 300, SR // 70
    return lo + int(np.argmax(c[lo:hi]))


def fim_suave(x, r):
    """O áudio do .MOV acaba no começo da última vogal: usa só o que foi gravado, com fade curto dentro da vogal (sem
    clique nem corte seco) e o tom de sala por baixo, no lugar do silêncio digital."""
    corte, q = int(r["corte"] * SR), int(r["fade"] * SR)
    y = x[:corte].copy()
    y[-q:] *= np.linspace(1, 0, q) ** 1.5
    tom = loop_tom(tom_de_sala(x), int(0.4 * SR))
    tom[:q] *= np.linspace(0, 1, q)
    y = np.concatenate([y, np.zeros(len(tom) - q)])
    y[corte - q:] += tom[:len(y) - corte + q]
    return y, {"modo": "fim_suave", "fim_voz_s": r["corte"], "fade_ms": round(1000 * r["fade"])}


def restaurar(x, r, doador):
    """Completa a sílaba que o iPhone cortou com a mesma sílaba falada pelo Diego em outro take (o "-ta." final de
    "pronta.", IMG_7243): emenda dentro da oclusão do "t" (quase silêncio), com cruzamento curto e o ganho igualado
    pela vogal anterior de cada take. Por baixo do fim entra o tom de sala. Sem síntese: só a voz gravada dele.
    (A 1ª tentativa, repetir os períodos glotais do "a" cortado, soou "vizinha" no Whisper; o "a" gravado é curto e rangido.)"""
    corte = int(r["corte"] * SR)
    d0, d1 = int(r["de"] * SR), int(r["ate"] * SR)
    don = doador[d0:d1].copy()
    if r.get("tom_rel", 1.0) != 1.0:
        # tom do doador ajustado ao do take (reamostragem: ≈ 8% mais grave e 8% mais longo)
        from scipy.signal import resample
        don = resample(don, int(len(don) / r["tom_rel"]))
    # ganho: vogal antes da oclusão em cada take (o "i" de "visi-" e o "o/n" de "pron-")
    ref = rms_db(x[int(r["ref"][0] * SR):int(r["ref"][1] * SR)])
    ref_d = rms_db(doador[int(r["ref_doador"][0] * SR):int(r["ref_doador"][1] * SR)])
    g = float(np.clip(ref - ref_d, -8, 8))
    don *= 10 ** (g / 20)
    cf = int(r["cruzar"] * SR)
    q = int(0.04 * SR)
    don[-q:] *= np.linspace(1, 0, q)
    y = x[:corte + cf].copy()
    y[-cf:] = y[-cf:] * np.linspace(1, 0, cf) + don[:cf] * np.linspace(0, 1, cf)
    y = np.concatenate([y, don[cf:]])
    fim = len(y)
    tom = loop_tom(tom_de_sala(x), int(0.3 * SR))
    tom[:int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))
    y = np.concatenate([y, np.zeros(int(0.3 * SR))])
    y[fim - int(0.03 * SR):fim - int(0.03 * SR) + len(tom)] += tom[:len(y) - fim + int(0.03 * SR)]
    return y, {"ganho_doador_db": round(g, 1), "fim_s": round(fim / SR, 3), "emprestado_s": round((d1 - d0) / SR, 3)}


def montar(d, fonte_dir):
    """Decupagem: cada fala vira 1 ou mais pedaços do bruto; respiro com o tom de sala do próprio take."""
    au = d["audio"]
    fi, fo = int(au["fade_in_s"] * SR), int(au["fade_out_s"] * SR)
    alin = json.load(open(os.path.join(AQUI, "transcricao_alinhada.json"), encoding="utf-8"))
    pedacos, trechos, palavras, t = [], [], [], 0.0
    EXTRAS[:] = [carregar_take(os.path.join(fonte_dir, d["fontes"][f]["arquivo"])) for f in ("IMG_7243", "IMG_7231")]
    fps = d["fps"]
    for fa in d["falas"]:
        x = carregar_take(os.path.join(fonte_dir, d["fontes"][fa["fonte"]]["arquivo"]))
        info = None
        if "restauro" in fa:
            r = fa["restauro"]
            if r.get("modo") == "fim_suave":
                x, info = fim_suave(x, r)
            else:
                x, info = restaurar(x, r, carregar_take(os.path.join(fonte_dir, d["fontes"][r["fonte"]]["arquivo"])))
            print(f"  restauro {fa['id']}: {info}")
        # nível do take medido na fala (para os takes soarem iguais antes do ganho geral)
        nivel = rms_db(x[int(fa["in"] * SR):int(fa["out"] * SR)])
        cortes = [[fa["in"], fa["out"]]]
        for a, b in fa.get("tirar", []):
            c = cortes.pop()
            cortes += [[c[0], a], [b, c[1]]]
        for j, (a, b) in enumerate(cortes):
            # cada pedaço com número inteiro de quadros: o vídeo do Diego é cortado igual
            nq = round((b - a) * fps)
            b = a + nq / fps
            seg = x[int(round(a * SR)):int(round(a * SR)) + int(round(nq / fps * SR))].copy()
            if len(seg) < int(round(nq / fps * SR)):
                seg = np.concatenate([seg, loop_tom(tom_de_sala(x), int(round(nq / fps * SR)) - len(seg))])
            seg[:fi] *= np.linspace(0, 1, fi)
            seg[-fo:] *= np.linspace(1, 0, fo)
            pedacos.append((seg, nivel))
            trechos.append({"fala": fa["id"], "fonte": fa["fonte"], "in": round(a, 4), "out": round(b, 4), "inicio": round(t, 4), "quadros": nq})
            for w in alin[fa["fonte"]]:
                if a - 0.02 <= w["ini"] < b:
                    palavras.append({"fala": fa["id"], "texto": w["texto"], "ini": round(t + w["ini"] - a, 3),
                                     "fim": round(t + min(w["fim"], b) - a, 3), "prob": w["prob"]})
            t += nq / fps
        if fa.get("respiro_depois"):
            nq = round(fa["respiro_depois"] * fps)
            # o respiro continua o próprio take (som da sala depois da última palavra); o vídeo também continua
            a = cortes[-1][1]
            seg = x[int(a * SR):int(a * SR) + int(nq / fps * SR)].copy()
            if len(seg) < int(nq / fps * SR) or rms_db(seg) > -45:
                seg = loop_tom(tom_de_sala(x), int(nq / fps * SR))
            seg[:fi] *= np.linspace(0, 1, fi)
            seg[-fo:] *= np.linspace(1, 0, fo)
            pedacos.append((seg, None))
            trechos.append({"fala": fa["id"], "fonte": fa["fonte"], "in": round(a, 4), "out": round(a + nq / fps, 4), "inicio": round(t, 4),
                            "quadros": nq, "respiro": True})
            t += nq / fps
    alvo = np.mean([n for _, n in pedacos if n is not None])
    voz = []
    ganho_ant = 0.0
    for seg, n in pedacos:
        g = alvo - n if n is not None else ganho_ant
        ganho_ant = g
        voz.append(seg * 10 ** (g / 20))
    voz = np.concatenate(voz)
    # numerar ocorrências (âncoras "fala:palavra#n")
    cont = {}
    for w in palavras:
        k = (w["fala"], w["texto"].strip(",.").lower())
        cont[k] = cont.get(k, 0) + 1
        w["n"] = cont[k]
    return voz, trechos, palavras, t


def processar(d, fonte_dir):
    voz, trechos, palavras, total = montar(d, fonte_dir)
    bruta = os.path.join(TMP, "voz_bruta.wav")
    sf.write(bruta, voz.astype(np.float32), SR, subtype="FLOAT")
    json.dump(trechos, open(os.path.join(TMP, "trechos.json"), "w"), indent=1)
    json.dump(palavras, open(os.path.join(TMP, "palavras.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  voz: {total:.3f} s em {len(trechos)} trechos")
    return bruta, trechos, palavras, total
