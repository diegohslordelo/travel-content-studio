"""Prolongamentos na fala (pedido do Diego, 20/11/2026, vlog de Bruges: "corte quando eu prolongo muito na fala… se eu
vou falar algo e fico falando a letra ou 'aí', essas partes você pode decupar também").

Roda de reels/bruges-yt (depois de scripts/hesitacoes.py, para não ter dois Whisper na memória):
    python -I scripts/prolongamentos.py
Entradas: _tmp/transcricao.json (Whisper large-v3, palavra a palavra), _tmp/voz16k.wav
Saída:    _tmp/prolongamentos.json (candidatos, a 2ª transcrição de cada um e a decisão)

Como acha e decide:
1. Palavra CURTA (até 4 letras: "e", "é", "aí", "um", "mas", "num"…) com ≥ 0,6 s e mais de 2,2 vezes a duração
   esperada pelo número de letras (0,09 s por letra + 0,08 s). Palavra longa esticada ("carruagem", "37ª") fica:
   cortar no meio dela pode comer sílaba;
2. O arrasto (da palavra, depois dos primeiros 0,25 s, até 0,06 s antes da palavra seguinte) é transcrito de novo
   sozinho (Whisper large-v3, sem filtro de voz, prompt de hesitações), com 0,2 s de folga de cada lado;
3. Corta o arrasto só se a 2ª transcrição não escrever nenhuma palavra de verdade dentro dele (só "é", "e", "ah",
   "ahn", "hum"…) e ele tiver ≥ 0,2 s. A palavra continua sendo dita (ficam os primeiros 0,25 s).
É medição automática: cada corte vai listado na DECUPAGEM para o Diego conferir na prévia (o Claude não escuta).
"""
import json
import re

import soundfile as sf

from faster_whisper import WhisperModel

SR = 16000
HES = {"é", "e", "eh", "ah", "ahn", "hum", "hã", "ã", "éé", "ééé", "ee", "eee", "hmm", "uhm", "um", "ham", "mm", "aí", "ai"}
FICA = 0.25


def limpa(p):
    return re.sub(r"[^\wáéíóúâêôãõçà]", "", p.lower())


def main():
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    ws = sorted([w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]], key=lambda w: w["ini"])
    x, sr = sf.read("_tmp/voz16k.wav", dtype="float32")
    assert sr == SR
    cand = []
    for i, w in enumerate(ws):
        p = limpa(w["p"])
        dur = w["fim"] - w["ini"]
        if not p or len(p) > 4 or dur < 0.6 or dur <= 2.2 * (0.09 * len(p) + 0.08):
            continue
        prox = ws[i + 1]["ini"] if i + 1 < len(ws) else w["fim"]
        a, b = w["ini"] + FICA, min(w["fim"], prox) - 0.06
        if b - a < 0.2:
            continue
        cand.append({"palavra": w["p"], "de": w["ini"], "ate": w["fim"], "antes": ws[i - 1]["p"] if i else "", "depois": ws[i + 1]["p"] if i + 1 < len(ws) else "", "arrasto": [round(a, 3), round(b, 3)]})
    print(len(cand), "candidatos")
    modelo = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
    prompt = "Ééé... ahn... hum... é... então, ééé, a gente, ahn, foi lá. Hã? Hmm."
    for c in cand:
        a, b = c["arrasto"]
        a0, b0 = max(0, a - 0.2), b + 0.2
        segs, _ = modelo.transcribe(x[int(a0 * SR):int(b0 * SR)], language="pt", beam_size=5, word_timestamps=True, vad_filter=False,
                                    initial_prompt=prompt, condition_on_previous_text=False)
        palavras = [(w.word.strip(), a0 + w.start, a0 + w.end) for s in segs for w in s.words]
        miolo = [p for p, i0, i1 in palavras if i1 > a + 0.04 and i0 < b - 0.04]
        reais = [limpa(p) for p in miolo if limpa(p) and limpa(p) not in HES]
        c["segunda"] = " ".join(p for p, _, _ in palavras)
        c["miolo"] = " ".join(miolo)
        c["cortar"] = not reais
        c["corte"] = c["arrasto"] if c["cortar"] else None
        print(f"{c['de']:7.2f}–{c['ate']:7.2f} [{c['palavra']}] ({c['antes']} _ {c['depois']})  arrasto {a:.2f}–{b:.2f}  miolo [{c['miolo']}]  → {'CORTA' if c['cortar'] else 'mantém'}   ({c['segunda']})", flush=True)
    json.dump(cand, open("_tmp/prolongamentos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
