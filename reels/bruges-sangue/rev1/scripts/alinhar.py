"""Alinhamento forçado palavra a palavra (torchaudio MMS_FA) sobre o texto conferido de cada tomada.
Lê ../edicao.json (texto e janela de cada tomada) e grava ../transcricao_alinhada.json (tempos no arquivo bruto).
Roda de dentro de reels/bruges-sangue/rev1:  python scripts/alinhar.py
"""
import json, os, subprocess, unicodedata, re
import numpy as np, torch, torchaudio

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
FONTE = os.path.join(AQUI, ed["fonte_dir"])

bundle = torchaudio.pipelines.MMS_FA
modelo = bundle.get_model(with_star=False)
dic = bundle.get_dict(star=None)
alinhar = bundle.get_aligner()
tok = bundle.get_tokenizer()

def roman(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z']", "", w)

saida = {}
for f in ed["falas"]:
    arq = os.path.join(FONTE, ed["fontes"][f["fonte"]])
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True)
    a = np.frombuffer(r.stdout, dtype=np.float32)
    i0, i1 = int(f["in"] * 16000), int(f["out"] * 16000)
    wav = torch.from_numpy(a[i0:i1].copy()).unsqueeze(0)
    palavras = f["texto"].split()
    rom = [roman(w) for w in palavras]
    with torch.inference_mode():
        em, _ = modelo(wav)
        spans = alinhar(em[0], tok(rom))
    razao = wav.shape[1] / em.shape[1] / 16000
    lista = []
    for w, sp in zip(palavras, spans):
        ini = f["in"] + sp[0].start * razao
        fim = f["in"] + sp[-1].end * razao
        sc = float(np.mean([s.score for s in sp]))
        lista.append({"texto": w, "ini": round(ini, 3), "fim": round(fim, 3), "prob": round(sc, 3)})
    saida[f["fonte"]] = lista
    print(f["fonte"], " ".join(f"{x['texto']}[{x['ini']:.2f}-{x['fim']:.2f}|{x['prob']:.2f}]" for x in lista))
json.dump(saida, open(os.path.join(AQUI, "transcricao_alinhada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
