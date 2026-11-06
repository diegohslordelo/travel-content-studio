"""Confere a decupagem (pedido do Diego: "cuidado pra não comer nenhuma palavra").

Para cada corte em que uma palavra da transcrição atravessa o trecho cortado (o Whisper estica o fim da palavra
sobre a pausa), monta o áudio JÁ CORTADO (1,5 s antes + 1,5 s depois) e transcreve de novo (Whisper large-v3, sem
filtro de voz). Se a palavra continua lá, o corte pegou só o arrasto/silêncio. Roda de reels/bru-yt:
  python scripts/confere_cortes.py   →  _tmp/confere_cortes.json
"""
import json
import re
import unicodedata

import numpy as np
import soundfile as sf

from faster_whisper import WhisperModel


def norm(p):
    p = unicodedata.normalize("NFD", p.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in p if unicodedata.category(c) != "Mn"))


def main():
    edl = json.load(open("rev1/edl_rev1.json"))
    tr = json.load(open("_tmp/transcricao.json"))
    ws = [w for s in tr["segmentos"] for w in s["palavras"]]
    x, sr = sf.read("_tmp/voz16k.wav", dtype="float32")
    m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
    out = []
    for r in edl["removidos"]:
        a = r["de_q"] / 30
        b = r["ate_q"] / 30
        dentro = [w for w in ws if w["ini"] < b - 0.02 and w["fim"] > a + 0.02]
        if not dentro:
            continue
        clip = np.concatenate([x[int((a - 1.5) * sr):int(a * sr)], x[int(b * sr):int((b + 1.5) * sr)]])
        segs, _ = m.transcribe(clip, language="pt", beam_size=5, vad_filter=False, condition_on_previous_text=False)
        txt = " ".join(s.text.strip() for s in segs)
        ok = all(norm(w["p"]) in norm(txt) for w in dentro)
        out.append({"de": round(a, 2), "dur": round(b - a, 2), "palavras": [w["p"] for w in dentro], "depois_do_corte": txt, "palavra_inteira": ok})
        print(f"{a:7.2f} −{b - a:.2f} s  {[w['p'] for w in dentro]}  →  {'OK' if ok else 'CONFERIR'}  «{txt}»", flush=True)
    json.dump(out, open("_tmp/confere_cortes.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
