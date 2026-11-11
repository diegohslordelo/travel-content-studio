"""Alinhamento forçado palavra a palavra (torchaudio MMS_FA) sobre o texto conferido de cada fala.
Números e siglas são escritos como aparecem na legenda ("2025", "5,7%") e alinhados pela forma falada (FALADO).
Lê ../edicao.json e grava ../transcricao_alinhada.json. Roda de dentro de reels/disney-parte2/rev1: python scripts/alinhar.py"""
import json, os, subprocess, unicodedata, re
import numpy as np, torch, torchaudio

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
FONTE = os.path.join(AQUI, ed["fonte_dir"])
FALADO = {"2025": "dois mil e vinte e cinco", "5,7%": "cinco virgula sete por cento", "16": "dezesseis", "40": "quarenta",
          "30": "trinta", "5": "cinco", "2": "dois", "rer": "rer", "4": "quatro"}
bundle = torchaudio.pipelines.MMS_FA
modelo = bundle.get_model(with_star=False)
alinhar = bundle.get_aligner()
tok = bundle.get_tokenizer()

def roman(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z']", "", w)

arq = os.path.join(FONTE, ed["fontes"]["Q"])
r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True)
a = np.frombuffer(r.stdout, dtype=np.float32)
saida = {}
for f in ed["falas"]:
    i0, i1 = int(f["in"] * 16000), int(f["out"] * 16000)
    wav = torch.from_numpy(a[i0:i1].copy()).unsqueeze(0)
    palavras = f["texto"].split()
    faladas, dono = [], []
    for k, w in enumerate(palavras):
        chave = re.sub(r"[,.!?:;]$", "", w).lower()
        partes = FALADO.get(chave, w).split()
        for p in partes:
            rp = roman(p)
            if rp:
                faladas.append(rp)
                dono.append(k)
    with torch.inference_mode():
        em, _ = modelo(wav)
        spans = alinhar(em[0], tok(faladas))
    razao = wav.shape[1] / em.shape[1] / 16000
    lista = []
    for k, w in enumerate(palavras):
        sp = [s for d, s in zip(dono, spans) if d == k]
        ini = f["in"] + sp[0][0].start * razao
        fim = f["in"] + sp[-1][-1].end * razao
        sc = float(np.mean([x.score for s in sp for x in s]))
        lista.append({"texto": w, "ini": round(ini, 3), "fim": round(fim, 3), "prob": round(sc, 3)})
    saida[f["id"]] = lista
    print(f["id"], " ".join(f"{x['texto']}[{x['ini']:.2f}-{x['fim']:.2f}|{x['prob']:.2f}]" for x in lista))
json.dump(saida, open(os.path.join(AQUI, "transcricao_alinhada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
