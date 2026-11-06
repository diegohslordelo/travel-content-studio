"""Decupagem do vídeo de Amsterdam (pedido do Diego, 21/10/2026): tira as pausas das falas sem cortar palavra,
apara o começo e o fim mortos dos planos falados e aplica os cortes manuais da revisão.

Entradas (de reels/ams-yt):
  _tmp/transcricao.json   palavras com tempo (faster-whisper large-v3)
  _tmp/voz_orig.wav       áudio da fonte sem música (48 kHz)
  _tmp/cenas.json         cortes de cena do editado (detectados no proxy)
  rev1/decisoes_rev1.json cortes manuais, quadros congelados, zonas protegidas e parâmetros
Saída:
  rev1/edl_rev1.json      trechos mantidos (quadros da fonte, 24 fps) + lista do que saiu e por quê

Como acha uma pausa (energia, não só a transcrição: o Whisper estica palavras sobre as pausas):
- Energia da voz em janelas de 10 ms na faixa 150–4000 Hz (o grave do vento e da rua não conta).
- "Silêncio" = abaixo de min(piso local + `silencio_acima_do_piso_db`, nível de fala local − 12 dB), com piso
  e fala medidos numa janela de `janela_piso_s` (percentis 10 e 90).
- Só dentro de zonas de fala (palavras com menos de 3 s entre si) e nunca sobre o início de uma palavra.
- Da pausa ficam `pad_fim` depois da fala e `pad_ini` antes da próxima; o resto sai, se tiver ≥ 120 ms.
- Pausa com corte de cena dentro: não corta no meio; apara o fim do plano anterior e o começo do seguinte,
  deixando pelo menos `min_plano` de cada um.
- Zonas protegidas e quadros congelados ficam como estão.
Tudo em quadros inteiros (24 fps): imagem e som cortam no mesmo instante.
"""
import json
import math

import numpy as np
import soundfile as sf
from scipy import signal

FPS = 24


def energia_voz(caminho):
    x, sr = sf.read(caminho, dtype="float32")
    x = x.mean(axis=1) if x.ndim > 1 else x
    sos = signal.butter(4, [150, 4000], btype="bandpass", fs=sr, output="sos")
    v = signal.sosfilt(sos, x)
    n = sr // 100
    m = len(v) // n
    db = 20 * np.log10(np.sqrt((v[: m * n].reshape(m, n) ** 2).mean(axis=1)) + 1e-9)
    return db, len(x) / sr


def percentil_movel(db, meia, q):
    v = np.array([np.percentile(db[max(0, i - meia):i + meia], q) for i in range(0, len(db), 50)])
    return np.repeat(v, 50)[: len(db)]


def main():
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    palavras = sorted([w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]], key=lambda w: w["ini"])
    cenas = json.load(open("_tmp/cenas.json", encoding="utf-8"))["cortes"]
    dec = json.load(open("rev1/decisoes_rev1.json", encoding="utf-8"))
    p = dec["parametros"]

    db, dur = energia_voz("_tmp/voz_orig.wav")
    meia = int(p["janela_piso_s"] * 100 / 2)
    piso = percentil_movel(db, meia, 10)
    fala = percentil_movel(db, meia, 90)
    limiar = np.minimum(piso + p["silencio_acima_do_piso_db"], fala - 12)
    baixo = db < limiar

    def silencioso(a, b):
        i, j = int(a * 100), int(math.ceil(b * 100))
        return j <= i or bool(np.all(baixo[i:j]))

    def mais_baixo(janela):
        a, b = janela
        i, j = int(a * 100), int(b * 100)
        m = np.convolve(db[i:j], np.ones(6) / 6, mode="same")
        return (i + int(np.argmin(m))) / 100

    protegidas = [(z["de"], z["ate"]) for z in dec.get("zonas_protegidas", [])]
    protegidas += [(c["de"] - 0.05, c["ate"] + 0.05) for c in dec.get("congelar", [])]

    def protegido(a, b):
        return any(a < zb and b > za for za, zb in protegidas)

    # zonas de fala
    zonas = []
    a, b = palavras[0]["ini"], palavras[0]["fim"]
    for w in palavras[1:]:
        if w["ini"] - b < 3:
            b = max(b, w["fim"])
        else:
            zonas.append((a, b))
            a, b = w["ini"], w["fim"]
    zonas.append((a, b))
    inicios = np.array([w["ini"] for w in palavras])

    remover = []
    for za, zb in zonas:
        i0, i1 = int(za * 100), int(zb * 100)
        k = i0
        while k < i1:
            if not baixo[k]:
                k += 1
                continue
            r = k
            while r < i1 and baixo[r]:
                r += 1
            a, b = k / 100, r / 100  # pausa medida
            k = r
            if b - a < p["pad_fim"] + p["pad_ini"] + 0.12:
                continue
            if np.any((inicios > a + 0.05) & (inicios < b - 0.05)):
                continue  # há início de palavra dentro: pode ser fala baixa (Marina longe do microfone)
            if protegido(a, b):
                continue
            dentro = [c for c in cenas if a < c < b]
            if len(dentro) >= 2:
                continue
            if len(dentro) == 1:
                c = dentro[0]
                x, y = a + p["pad_fim"], c - p["min_plano"]
                if y - x >= 0.12:
                    remover.append((x, y, "fim parado do plano (pausa antes do corte)"))
                x, y = c + p["min_plano"], b - p["pad_ini"]
                if y - x >= 0.12:
                    remover.append((x, y, "começo parado do plano (pausa depois do corte)"))
                continue
            remover.append((a + p["pad_fim"], b - p["pad_ini"], "pausa na fala"))

    manuais = []
    for c in dec["cortes_manuais"]:
        a = mais_baixo(c["de"]) if isinstance(c["de"], list) else c["de"]
        b = mais_baixo(c["ate"]) if isinstance(c["ate"], list) else c["ate"]
        if c.get("verificar_silencio"):
            while b - a >= 0.08 and not silencioso(a, b):
                a += 0.02
                b -= 0.02
            if b - a < 0.08:
                print(f"  manual {c['de']}–{c['ate']} descartado: não há silêncio")
                continue
        remover.append((a, b, c["motivo"]))
        manuais.append({"de": round(a, 3), "ate": round(b, 3), "motivo": c["motivo"]})

    # em quadros: tira [qa, qb) com qa arredondado para cima e qb para baixo
    quadros = []
    for a, b, m in remover:
        qa, qb = math.ceil(a * FPS), math.floor(b * FPS)
        if qb - qa >= 3 or (m.startswith("[") and qb > qa):
            quadros.append((qa, qb, m))
    quadros.sort()
    unidos = []
    for qa, qb, m in quadros:
        if unidos and qa <= unidos[-1][1]:
            unidos[-1] = (unidos[-1][0], max(unidos[-1][1], qb), unidos[-1][2] if unidos[-1][2].startswith("[") else m)
        else:
            unidos.append((qa, qb, m))
    total_q = int(round(dur * FPS))
    manter = []
    pos = 0
    for qa, qb, _ in unidos:
        if qa > pos:
            manter.append([pos, qa])
        pos = max(pos, qb)
    if pos < total_q:
        manter.append([pos, total_q])

    saiu = sum(qb - qa for qa, qb, _ in unidos) / FPS
    out = {
        "fps": FPS,
        "duracao_fonte_s": round(dur, 3),
        "duracao_saida_s": round(sum(b - a for a, b in manter) / FPS, 3),
        "removido_s": round(saiu, 3),
        "manter": manter,
        "removidos": [{"de_q": qa, "ate_q": qb, "de_s": round(qa / FPS, 3), "dur_s": round((qb - qa) / FPS, 3), "motivo": m} for qa, qb, m in unidos],
        "cortes_manuais_aplicados": manuais,
        "congelar": dec.get("congelar", []),
    }
    json.dump(out, open("rev1/edl_rev1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    por = {}
    for qa, qb, m in unidos:
        k = m[:70]
        por.setdefault(k, [0, 0.0])
        por[k][0] += 1
        por[k][1] += (qb - qa) / FPS
    print(f"fonte {dur:.1f} s → saída {out['duracao_saida_s']:.1f} s (−{saiu:.1f} s em {len(unidos)} cortes)")
    for k, (n, s) in sorted(por.items(), key=lambda x: -x[1][1]):
        print(f"  {n:4d} × {s:7.1f} s  {k}")


if __name__ == "__main__":
    main()
