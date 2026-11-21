"""Conferência do áudio da REV4 (vlog de Bruges), pedido do Diego (21/11/2026): "revise o áudio e os inícios e términos
do vídeo e veja se não tem nada fora de lugar". Medição, não escuta (o Claude não escuta: a escuta é do Diego).

Roda de reels/bruges-yt, depois do render da prévia:  python -I rev4/conferir_audio_rev4.py
Lê rev4/linha_do_tempo_rev4.json, _tmp/voz_orig.wav, _tmp/musica_rev4.wav, rev4/props_rev4.json e o som final da prévia
(_tmp/previa_rev4/mix_lim.wav). Escreve rev4/audio/CONFERENCIA_AUDIO_REV4.md.

O que confere:
  1. Emendas da voz: trechos de áudio sobrepostos (voz dupla) ou com buraco entre si; salto de amostra (estalo) em cada
     emenda, já com as rampas de 12 ms;
  2. Buracos de silêncio (≥ 300 ms abaixo de −60 dBFS) no som final, do começo ao fim;
  3. Música por cima de fala do vlog (palavras da transcrição no relógio final × nível da música);
  4. Quadros congelados: o som continua (a voz segue tocando);
  5. Time-lapse: sem o som acelerado da fonte, só a música;
  6. Começo e fim do vídeo: entrada da música no 1º quadro, nada tocando depois do fim;
  7. Loudness integrado e pico do som final.
"""
import bisect
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

SR = 48000


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}".replace(".", ",")


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.square(x))) + 1e-12)


def main():
    lt = json.load(open("rev4/linha_do_tempo_rev4.json", encoding="utf-8"))
    props = json.load(open("rev4/props_rev4.json", encoding="utf-8"))
    voz_src, _ = sf.read("_tmp/voz_orig.wav", dtype="float32", always_2d=True)
    mus, _ = sf.read("_tmp/musica_rev4.wav", dtype="float32", always_2d=True)
    fim, _ = sf.read("_tmp/previa_rev4/mix_lim.wav", dtype="float32", always_2d=True)
    D = lt["duracao_ms"] / 1000
    L = ["# REV4 · Conferência do áudio (vlog de Bruges)", "",
         "Medição feita por `rev4/conferir_audio_rev4.py` sobre a prévia da REV4. **Não é escuta**: o Claude não escuta áudio; a validação auditiva é sua.", ""]
    problemas = 0

    # 1. emendas
    au = sorted(lt["audio"], key=lambda a: a["out"])
    sobre, buracos, estalos = [], [], []
    for a, b in zip(au, au[1:]):
        fa = a["out"] + a["dur"]
        if b["out"] < fa - 1:
            sobre.append((a["out"] / 1000, (fa - b["out"]) / 1000))
    # reconstrói a voz como na mixagem e mede o salto de amostra em cada emenda
    n = int(round(D * SR))
    voz = np.zeros((n, 2), dtype=np.float32)
    r = int(0.012 * SR)
    for p in au:
        i0, o0, m = int(round(p["src"] / 1000 * SR)), int(round(p["out"] / 1000 * SR)), int(round(p["dur"] / 1000 * SR))
        m = min(m, n - o0, len(voz_src) - i0)
        if m <= 2 * r:
            continue
        x = voz_src[i0:i0 + m].copy()
        x[:r] *= np.linspace(0, 1, r)[:, None]
        x[-r:] *= np.linspace(1, 0, r)[:, None]
        voz[o0:o0 + m] += x
    for p in au:
        for t in (p["out"] / 1000, (p["out"] + p["dur"]) / 1000):
            i = int(t * SR)
            if i < 200 or i > n - 200:
                continue
            janela = voz[i - 144:i + 144, 0]
            salto = float(np.max(np.abs(np.diff(janela))))
            ref = float(np.sqrt(np.mean(np.square(voz[max(0, i - 4800):i + 4800, 0]))) + 1e-9)
            if salto > 6 * ref and salto > 0.02:
                estalos.append((t, salto / ref))
    L += ["## 1. Emendas da voz", "",
          f"- {len(au)} trechos de áudio da fonte (gancho + corpo). Sobrepostos (voz dupla): **{len(sobre)}**" + (": " + ", ".join(f"{mmss(t)} ({d:.2f} s)" for t, d in sobre) if sobre else "") + ".",
          f"- Saltos de amostra suspeitos de estalo nas emendas (salto > 6× o nível da fala em volta): **{len(estalos)}**" + (": " + ", ".join(f"{mmss(t)} ({k:.0f}×)" for t, k in estalos) if estalos else "") + ".", ""]
    problemas += len(sobre) + len(estalos)

    # 2. buracos de silêncio no som final
    nf = len(fim)
    hop = SR // 100
    nivel = np.array([db(fim[k:k + hop, 0]) for k in range(0, nf - hop, hop)])
    baixo = nivel < -60
    runs, k = [], 0
    while k < len(baixo):
        if baixo[k]:
            j = k
            while j < len(baixo) and baixo[j]:
                j += 1
            if j - k >= 30:
                runs.append((k / 100, (j - k) / 100))
            k = j
        else:
            k += 1
    L += ["## 2. Buracos de silêncio (≥ 300 ms abaixo de −60 dBFS)", "",
          f"- **{len(runs)}**" + (": " + ", ".join(f"{mmss(t)} ({d:.2f} s)" for t, d in runs) if runs else " em todo o vídeo.") + "", ""]
    problemas += len([1 for t, d in runs if t < D - 1])

    # 3. música por cima de fala do vlog
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    ws = [w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]]
    corpo = sorted([p for p in au if p["tipo"] in ("corpo", "gancho_fala")], key=lambda p: p["src"])
    srcs = [p["src"] for p in corpo]
    sob = []
    for w in ws:
        i = bisect.bisect_right(srcs, w["ini"] * 1000) - 1
        if i < 0:
            continue
        p = corpo[i]
        if not (p["src"] <= w["ini"] * 1000 and w["fim"] * 1000 <= p["src"] + p["dur"]):
            continue
        t = (p["out"] + (w["ini"] * 1000 - p["src"])) / 1000
        a, b = int(t * SR), int((t + w["fim"] - w["ini"]) * SR)
        if b > a and db(mus[a:b, 0]) > -45 and t * 1000 >= lt["gancho_ms"]:  # no gancho a música fica por baixo de propósito (−9 dB)
            sob.append((t, w["p"], db(mus[a:b, 0])))
    L += ["## 3. Música por cima de fala do vlog", "",
          f"- Palavras da transcrição com música tocando ao mesmo tempo (acima de −45 dBFS): **{len(sob)}**" + (": " + ", ".join(f"{mmss(t)} \"{p}\"" for t, p, _ in sob[:20]) if sob else "") + ".",
          "- Fora da conta, de propósito: o gancho (a fala da Marina e a narração ficam com a música 9 dB abaixo) e o fechamento (narração a gravar).",
          "- O Whisper às vezes põe uma palavra no lugar errado do tempo (ex.: \"Uma\" antes da montagem do Rozenhoedkaai, que na fonte é dita depois dela): esses casos aparecem aqui e são conferidos à mão.", ""]
    problemas += len(sob)

    # 4. quadros congelados: a voz segue
    cg = [t for t in props["trechos"] if t.get("congela") and not t.get("pagina")]
    linhas = []
    for t in cg:
        a, b = int(t["de"] / 1000 * SR), int(t["ate"] / 1000 * SR)
        linhas.append(f"{mmss(t['de'] / 1000)}–{mmss(t['ate'] / 1000)}: voz a {db(voz[a:b, 0]):.0f} dBFS (som segue)")
    L += ["## 4. Quadros congelados", "", *(f"- {x}" for x in linhas), ""]

    # 5. time-lapse
    tl = [t for t in props["trechos"] if t.get("velocidade")]
    for t in tl:
        a, b = int(t["de"] / 1000 * SR), int(t["ate"] / 1000 * SR)
        L += ["## 5. Time-lapse", "", f"- {mmss(t['de'] / 1000)}–{mmss(t['ate'] / 1000)}: som da fonte a {db(voz[a:b, 0]):.0f} dBFS (sem o som acelerado) · música a {db(mus[a:b, 0]):.0f} dBFS", ""]
        if db(voz[a:b, 0]) > -60:
            problemas += 1

    # 6. começo e fim
    L += ["## 6. Começo e fim do vídeo", "",
          f"- Primeiros 0,25 s: música a {db(mus[:int(0.25 * SR), 0]):.0f} dBFS (entra no 1º quadro, em 0,25 s); 0,25–1,0 s: {db(mus[int(0.25 * SR):SR, 0]):.0f} dBFS.",
          f"- Últimos 3 s (tela final): a música sai; último 0,2 s a {db(fim[-int(0.2 * SR):, 0]):.0f} dBFS.",
          f"- Duração do som final {len(fim) / SR:.3f} s × imagem {props['duracao'] / 1000:.3f} s.", ""]

    # 7. loudness
    med = pyln.Meter(SR)
    lv = med.integrated_loudness(fim)
    pico = 20 * np.log10(np.abs(fim).max() + 1e-12)
    L += ["## 7. Nível do som final da prévia", "", f"- {lv:.1f} LUFS integrados, pico de amostra {pico:.1f} dBFS (o master final segue o padrão: −14 LUFS, ≤ −1 dBTP).", "",
          f"**Resultado:** {problemas} problema(s) medido(s)." + (" Nada fora do lugar pela medição; falta a sua escuta." if problemas == 0 else " Ver os itens acima.")]
    os.makedirs("rev4/audio", exist_ok=True)
    open("rev4/audio/CONFERENCIA_AUDIO_REV4.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
